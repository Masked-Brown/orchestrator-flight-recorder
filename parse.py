#!/usr/bin/env python3
"""
parse.py — deterministic reader for the Claude data export.

Turns the export's conversations JSON into a numbered message manifest: the flight
recorder read-out that the diagnostician works from. Same input, same output, every
time. No third-party packages; Python 3.8+.

Why this exists
---------------
Everything deterministic belongs in a script, not on model diligence. Message
numbering, channel separation, branch detection and reasoning-coverage accounting
are all mechanical, so they happen here. The investigator reads the manifest; it
never reads the raw export.

The one rule that shapes the whole file
---------------------------------------
Each message in the export carries BOTH a flattened `text` field and a structured
`content` block list. They are not the same thing. The flattened field splices the
assistant's private reasoning together with the prose it actually sent, with no
marker between them. Building a manifest from it would let an investigator quote a
thought as though it were a statement. So this parser reads `content` blocks only,
and keeps each channel labelled and separate:

    SAID       text the party actually sent
    REASONING  assistant thinking, where the export carries it
    ACTION     a tool call
    RESULT     what the tool returned
    ATTACHMENT a file supplied with the message

Usage
-----
    python parse.py conversations.json --list
    python parse.py conversations.json --name "my-session" --out manifest.md
    python parse.py conversations.json --index 15 --messages 20-32
    python parse.py conversations.json --name "my-session" --json --out manifest.json

Run with --help for the full option list.
"""

import argparse
import hashlib
import json
import sys

SCHEMA_VERSION = "1"

# Channel labels. Kept as module constants because check.py (M3) parses them.
CH_SAID = "SAID"
CH_REASONING = "REASONING"
CH_REASONING_SUMMARY = "REASONING-SUMMARY"
CH_ACTION = "ACTION"
CH_RESULT = "RESULT"
CH_ATTACHMENT = "ATTACHMENT"

# Per-message reasoning availability, three states.
REASONING_FULL = "full"            # thinking text present in the export
REASONING_SUMMARY = "summary-only" # thinking redacted, summaries survive
REASONING_ABSENT = "absent"        # no thinking block at all


# --------------------------------------------------------------------------
# loading and selection
# --------------------------------------------------------------------------

def load_export(path):
    """Read the conversations file. Returns (conversations, sha256 of the file)."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        die("could not open %s: %s" % (path, exc.strerror or exc))
    digest = hashlib.sha256(raw).hexdigest()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        die("could not read %s as JSON: %s" % (path, exc))

    # The export ships several JSON files side by side and they all parse. Check the
    # shape, not just the syntax, so pointing at the wrong one fails here instead of
    # producing an empty manifest that looks like a finding.
    wrong_file = ("%s is valid JSON but does not look like the conversations file.\n"
                  "The export contains several JSON files; the one you want is the list of\n"
                  "conversations, where each entry has a 'chat_messages' list." % path)
    if not isinstance(data, list):
        die(wrong_file + "\nThis file holds a %s at the top level." % type(data).__name__)
    if data:
        if not all(isinstance(entry, dict) for entry in data):
            die(wrong_file)
        if not any("chat_messages" in entry for entry in data):
            die(wrong_file)
    return data, digest


def conversation_rows(convs):
    """One summary row per conversation, in file order. Used by --list and by errors."""
    rows = []
    for index, conv in enumerate(convs):
        messages = conv.get("chat_messages") or []
        rows.append({
            "index": index,
            "uuid": conv.get("uuid", ""),
            "name": conv.get("name", ""),
            "created": (conv.get("created_at") or "")[:10],
            "messages": len(messages),
            "branches": len(find_branch_points(messages)),
        })
    return rows


def select_conversation(convs, args):
    """Pick exactly one conversation, or fail with something the user can act on."""
    candidates = list(enumerate(convs))

    if args.uuid:
        candidates = [(i, c) for i, c in candidates if c.get("uuid") == args.uuid]
    if args.index is not None:
        candidates = [(i, c) for i, c in candidates if i == args.index]
    if args.name:
        needle = args.name.lower()
        candidates = [(i, c) for i, c in candidates
                      if needle in (c.get("name") or "").lower()]
    if args.since:
        candidates = [(i, c) for i, c in candidates
                      if (c.get("created_at") or "")[:10] >= args.since]
    if args.until:
        candidates = [(i, c) for i, c in candidates
                      if (c.get("created_at") or "")[:10] <= args.until]

    if not candidates:
        die("no conversation matched those selectors.\n"
            "Run with --list to see what is in this export.")
    if len(candidates) > 1:
        lines = ["%d conversations matched; narrow it down with --index or --uuid:" % len(candidates)]
        for i, conv in candidates[:20]:
            messages = conv.get("chat_messages") or []
            lines.append("  --index %-3d  %s  msgs=%-4d  %s"
                         % (i, (conv.get("created_at") or "")[:10],
                            len(messages), conv.get("name", "")))
        if len(candidates) > 20:
            lines.append("  ... and %d more" % (len(candidates) - 20))
        die("\n".join(lines))

    return candidates[0]


# --------------------------------------------------------------------------
# structure the export actually has
# --------------------------------------------------------------------------

def find_branch_points(messages):
    """
    Find messages that share a parent with a sibling.

    A shared parent means the conversation forked: a message was edited or a reply
    regenerated, and the export keeps every version in one flat list. Read linearly
    and un-flagged, a fork looks like someone repeating themselves. That is a
    causal misreading waiting to happen, so every fork is marked in the manifest.

    Returns {message_index (1-based): [sibling indices]}.
    """
    by_parent = {}
    for position, message in enumerate(messages):
        parent = message.get("parent_message_uuid")
        by_parent.setdefault(parent, []).append(position + 1)
    branches = {}
    for _parent, children in by_parent.items():
        if len(children) > 1:
            for child in children:
                branches[child] = [c for c in children if c != child]
    return branches


def describe_tool_input(payload):
    """One deterministic line describing a tool's arguments, without dumping them."""
    if isinstance(payload, dict):
        if not payload:
            return "(no arguments)"
        parts = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, str):
                parts.append("%s=<%d chars>" % (key, len(value)))
            elif isinstance(value, (list, dict)):
                parts.append("%s=<%s, %d items>" % (key, type(value).__name__, len(value)))
            else:
                parts.append("%s=%r" % (key, value))
        return ", ".join(parts)
    if isinstance(payload, str):
        return "<%d chars>" % len(payload)
    return "(none)" if payload is None else repr(payload)


def tool_result_text(content):
    """Pull readable text out of a tool result, whatever shape it arrived in."""
    if isinstance(content, list):
        chunks = []
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                chunks.append(block["text"])
        return "\n".join(chunks)
    if isinstance(content, str):
        return content
    return ""


def reasoning_state(message):
    """Which of the three reasoning states this message is in."""
    thinking_blocks = [b for b in message.get("content") or []
                       if isinstance(b, dict) and b.get("type") == "thinking"]
    if not thinking_blocks:
        return REASONING_ABSENT
    if any(b.get("thinking") for b in thinking_blocks):
        return REASONING_FULL
    if any(b.get("summaries") for b in thinking_blocks):
        return REASONING_SUMMARY
    return REASONING_ABSENT


def build_segments(message, include_tool_io, include_attachments):
    """
    Walk one message's content blocks in order and turn each into a labelled segment.

    Order is preserved deliberately: the interleaving of speech and tool calls is
    how a fault travels through a turn, and a propagation trace needs to see it.
    """
    segments = []
    for block in message.get("content") or []:
        if not isinstance(block, dict):
            segments.append({"channel": CH_SAID, "note": "unreadable content block", "text": ""})
            continue

        kind = block.get("type")

        if kind == "text":
            segments.append({"channel": CH_SAID, "text": block.get("text") or ""})

        elif kind == "thinking":
            if block.get("thinking"):
                segments.append({"channel": CH_REASONING, "text": block["thinking"]})
            else:
                summaries = [s.get("summary", "") for s in (block.get("summaries") or [])
                             if isinstance(s, dict)]
                if summaries:
                    segments.append({
                        "channel": CH_REASONING_SUMMARY,
                        "text": "\n".join(summaries),
                        "note": "reasoning text withheld from the export; "
                                "these are the export's own summaries",
                    })
                else:
                    segments.append({
                        "channel": CH_REASONING,
                        "text": "",
                        "note": "reasoning block present but withheld from the export, "
                                "with no summary",
                    })

        elif kind == "tool_use":
            segment = {
                "channel": CH_ACTION,
                "tool": block.get("name") or "(unnamed tool)",
                "text": "",
                "note": describe_tool_input(block.get("input")),
            }
            if include_tool_io:
                segment["text"] = json.dumps(block.get("input"), indent=2, sort_keys=True,
                                             ensure_ascii=False)
            segments.append(segment)

        elif kind == "tool_result":
            body = tool_result_text(block.get("content"))
            segment = {
                "channel": CH_RESULT,
                "tool": block.get("name") or "(unnamed tool)",
                "error": bool(block.get("is_error")),
                "text": body if include_tool_io else "",
                "note": ("tool reported an error" if block.get("is_error") else "ok")
                        + ", %d chars returned" % len(body)
                        + ("" if include_tool_io or not body
                           else "; not inlined (use --include-tool-io)"),
            }
            segments.append(segment)

        else:
            segments.append({
                "channel": CH_SAID,
                "text": "",
                "note": "content block of unrecognised type %r, recorded but not read"
                        % (kind,),
            })

    for attachment in message.get("attachments") or []:
        if not isinstance(attachment, dict):
            continue
        extracted = attachment.get("extracted_content") or ""
        segment = {
            "channel": CH_ATTACHMENT,
            "name": attachment.get("file_name") or "(unnamed)",
            "text": extracted if include_attachments else "",
            "note": "%s, %d chars of extracted text%s" % (
                attachment.get("file_type") or "unknown type",
                len(extracted),
                "" if include_attachments else "; not inlined (use --include-attachments)"),
        }
        segments.append(segment)

    for supplied in message.get("files") or []:
        if isinstance(supplied, dict):
            segments.append({
                "channel": CH_ATTACHMENT,
                "name": supplied.get("file_name") or "(unnamed)",
                "text": "",
                "note": "file supplied with the message; no text in the export",
            })

    return segments


def build_manifest(conv, conv_index, source_path, source_digest, args):
    """Assemble the whole manifest as data. Rendering happens separately."""
    messages = conv.get("chat_messages") or []
    branches = find_branch_points(messages)

    first, last = 1, len(messages)
    if args.messages:
        first, last = args.messages

    entries = []
    for position, message in enumerate(messages):
        number = position + 1
        if number < first or number > last:
            continue
        entries.append({
            "index": number,
            "role": message.get("sender") or "unknown",
            "timestamp": message.get("created_at") or "",
            "reasoning": reasoning_state(message),
            "branch_siblings": branches.get(number, []),
            "segments": build_segments(message, args.include_tool_io,
                                       args.include_attachments),
        })

    assistant_total = sum(1 for m in messages if m.get("sender") == "assistant")
    coverage = {"full": 0, "summary-only": 0, "absent": 0}
    for message in messages:
        if message.get("sender") == "assistant":
            coverage[reasoning_state(message)] += 1

    return {
        "schema_version": SCHEMA_VERSION,
        "source_file": source_path,
        "source_sha256": source_digest,
        "conversation": {
            "index": conv_index,
            "uuid": conv.get("uuid", ""),
            "name": conv.get("name", ""),
            "created_at": conv.get("created_at", ""),
            "updated_at": conv.get("updated_at", ""),
            "message_count": len(messages),
        },
        "window": {"first": first, "last": last,
                   "is_full_conversation": (first == 1 and last == len(messages))},
        "reasoning_coverage": {"assistant_messages": assistant_total, **coverage},
        "branch_points": {str(k): v for k, v in sorted(branches.items())},
        "messages": entries,
    }


# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------

def fence_for(text):
    """
    Pick a code fence longer than any backtick run inside the text.

    Transcripts of build sessions are full of code blocks, so a fixed ``` fence gets
    closed early by the message's own content and the manifest stops being readable
    from that point on. CommonMark allows any fence of three or more backticks, so
    the fence just has to outrun the longest run in the body.
    """
    longest = 0
    run = 0
    for character in text:
        if character == "`":
            run += 1
            longest = max(longest, run)
        else:
            run = 0
    return "`" * max(3, longest + 1)


def render_markdown(manifest):
    out = []
    add = out.append
    conv = manifest["conversation"]
    window = manifest["window"]
    coverage = manifest["reasoning_coverage"]

    add("# Message manifest")
    add("")
    add("Produced by parse.py from a Claude data export. Message numbers are stable: they")
    add("count from the start of the whole conversation, so they still line up when only a")
    add("window is shown.")
    add("")
    add("    conversation      %s" % (conv["name"] or "(unnamed)"))
    add("    conversation-uuid %s" % conv["uuid"])
    add("    started           %s" % conv["created_at"])
    add("    last-updated      %s" % conv["updated_at"])
    add("    messages          %d in the conversation" % conv["message_count"])
    if window["is_full_conversation"]:
        add("    window            whole conversation")
    else:
        add("    window            messages %d-%d of %d"
            % (window["first"], window["last"], conv["message_count"]))
    add("    source-file       %s" % manifest["source_file"])
    add("    source-sha256     %s" % manifest["source_sha256"])
    add("    parser-schema     v%s" % manifest["schema_version"])
    add("")

    add("## What the recorder captured")
    add("")
    add("The export does not always carry the assistant's reasoning. Where it is missing,")
    add("that is a gap in the recording, not evidence of anything. Do not infer reasoning")
    add("that is not here.")
    add("")
    add("    assistant messages          %d" % coverage["assistant_messages"])
    add("    reasoning recorded in full  %d" % coverage["full"])
    add("    summary only                %d" % coverage["summary-only"])
    add("    no reasoning recorded       %d" % coverage["absent"])
    add("")

    add("## Forks in the record")
    add("")
    if manifest["branch_points"]:
        add("Some messages share a parent, which means the conversation was forked at that")
        add("point: a message was edited, or a reply regenerated. The export keeps every")
        add("version in one flat list. These are alternative versions of the same turn, not")
        add("someone saying the same thing twice. Treat them accordingly.")
        add("")
        for number, siblings in sorted(manifest["branch_points"].items(), key=lambda kv: int(kv[0])):
            add("    message %s shares its parent with %s"
                % (number, ", ".join(str(s) for s in siblings)))
    else:
        add("None. Every message has its own parent, so the conversation runs as one line.")
    add("")
    add("---")
    add("")

    for entry in manifest["messages"]:
        add("## [%d] %s — %s" % (entry["index"], entry["role"], entry["timestamp"]))
        if entry["branch_siblings"]:
            add("")
            add("*Fork: an alternative version of the same turn as message %s.*"
                % ", ".join(str(s) for s in entry["branch_siblings"]))
        if entry["role"] == "assistant":
            add("")
            add("*Reasoning on the recorder: %s.*" % entry["reasoning"])
        add("")

        if not entry["segments"]:
            add("*(This message is empty in the export: no content was recorded.)*")
            add("")
            continue

        for segment in entry["segments"]:
            channel = segment["channel"]
            header = channel
            if channel == CH_ACTION:
                header = "%s — %s" % (channel, segment.get("tool", ""))
            elif channel == CH_RESULT:
                header = "%s — %s%s" % (channel, segment.get("tool", ""),
                                        " (error)" if segment.get("error") else "")
            elif channel == CH_ATTACHMENT:
                header = "%s — %s" % (channel, segment.get("name", ""))
            add("**%s**" % header)
            if segment.get("note"):
                add("")
                add("*%s*" % segment["note"])
            text = segment.get("text") or ""
            if text:
                fence = fence_for(text)
                add("")
                add(fence + "text")
                add(text)
                add(fence)
            add("")

    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def use_utf8_streams():
    """
    Force UTF-8 on stdout and stderr.

    Real transcripts contain arrows, box drawing and emoji. A Windows console
    defaults to a legacy codepage that cannot encode any of them, so printing a
    manifest there dies partway through with UnicodeEncodeError — after having
    already printed several thousand lines, which makes it look like a parsing bug.
    Writing with --out was always safe; this makes the terminal safe too.
    """
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):  # not a reconfigurable stream
            pass


def die(message):
    sys.stderr.write("parse.py: %s\n" % message)
    raise SystemExit(2)


def parse_window(value):
    """--messages 12-30, or a single number."""
    text = value.strip()
    try:
        if "-" in text:
            low, high = text.split("-", 1)
            first, last = int(low), int(high)
        else:
            first = last = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError("expected N or N-M, got %r" % value)
    if first < 1 or last < first:
        raise argparse.ArgumentTypeError("expected 1 <= N <= M, got %r" % value)
    return first, last


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="parse.py",
        description="Turn a Claude data export into a numbered message manifest.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Pick a conversation with --list first, then re-run with --index or --name.")
    parser.add_argument("export", help="path to the conversations JSON file from the export")

    picker = parser.add_argument_group("choosing a conversation")
    picker.add_argument("--list", action="store_true",
                        help="list the conversations in the export and exit")
    picker.add_argument("--name", help="conversation whose name contains this text")
    picker.add_argument("--uuid", help="conversation with this exact uuid")
    picker.add_argument("--index", type=int, help="conversation at this position in the export")
    picker.add_argument("--since", metavar="YYYY-MM-DD", help="started on or after this date")
    picker.add_argument("--until", metavar="YYYY-MM-DD", help="started on or before this date")
    picker.add_argument("--messages", type=parse_window, metavar="N-M",
                        help="only these message numbers (numbering stays global)")

    shaping = parser.add_argument_group("what goes in the manifest")
    shaping.add_argument("--include-tool-io", action="store_true",
                         help="inline tool arguments and tool output (off by default: verbose)")
    shaping.add_argument("--include-attachments", action="store_true",
                         help="inline the text extracted from attached files (off by default)")
    shaping.add_argument("--json", action="store_true",
                         help="emit JSON instead of markdown (this is what check.py reads)")
    shaping.add_argument("--out", metavar="PATH", help="write here instead of standard output")

    args = parser.parse_args(argv)
    use_utf8_streams()

    convs, digest = load_export(args.export)

    if args.list:
        rows = conversation_rows(convs)
        lines = ["%d conversations in %s" % (len(rows), args.export), ""]
        lines.append("index  started     msgs  forks  name")
        for row in rows:
            lines.append("%5d  %s  %4d  %5d  %s"
                         % (row["index"], row["created"], row["messages"],
                            row["branches"], row["name"]))
        write_output("\n".join(lines) + "\n", args.out)
        return 0

    conv_index, conv = select_conversation(convs, args)
    messages = conv.get("chat_messages") or []
    if not messages:
        die("that conversation has no messages in the export, so there is nothing to read.")
    if args.messages and args.messages[0] > len(messages):
        die("--messages starts at %d but the conversation only has %d messages."
            % (args.messages[0], len(messages)))

    manifest = build_manifest(conv, conv_index, args.export, digest, args)

    if args.json:
        payload = json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    else:
        payload = render_markdown(manifest)

    write_output(payload, args.out)
    return 0


def write_output(payload, path):
    if path:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(payload)
        sys.stderr.write("parse.py: wrote %s\n" % path)
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    raise SystemExit(main())
