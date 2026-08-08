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

The second rule: the export is a tree, not a list
-------------------------------------------------
`chat_messages` is a flat array, but every message carries `parent_message_uuid`.
When a message is edited or a reply regenerated, the export keeps every version in
that one array. Read as a list, an abandoned draft sits between two live turns and
looks like part of the conversation. So the array is walked as a tree: each message
records its parent, its children, and whether it is on the line the conversation
actually continued from or on a branch that was abandoned.

Message numbers still count array positions, because that is the one identifier
that is stable, reproducible and independent of any inference this file makes about
which branch survived. The tree is recorded alongside, never substituted for it.

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
import os
import re
import sys

SCHEMA_VERSION = "2"

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

# Where a message sits in the tree relative to the line the conversation continued on.
BRANCH_LIVE = "live"           # on the path the conversation actually followed
BRANCH_ABANDONED = "abandoned" # a version of a turn that was superseded

# How much of a long string parse.py will show inside a tool-call summary before it
# gives up and reports a length instead. Paths, shell commands and descriptions are
# short and are the informative part of a tool call; a pasted file body is neither.
TOOL_INPUT_INLINE_LIMIT = 300


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

    # Empty shells are dropped before anything else, unless one was asked for by
    # position or uuid. A real export carries conversations with no messages at all —
    # duplicates of a real chat, sharing its name and holding nothing. Left in, they
    # turn an unambiguous --name into "2 conversations matched" and send the user
    # hunting for a distinction that does not exist. Named explicitly, they are still
    # selectable, and main() then says plainly that there is nothing in there to read.
    if args.uuid is None and args.index is None:
        candidates = [(i, c) for i, c in candidates if (c.get("chat_messages") or [])]

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
        lines = ["%d conversations matched; narrow it down with --uuid, which is the "
                 "only\nidentifier that is unique — names repeat in a real export:"
                 % len(candidates)]
        for i, conv in candidates[:20]:
            messages = conv.get("chat_messages") or []
            lines.append("  --uuid %s  %s  msgs=%-4d  %s"
                         % (conv.get("uuid", "?"), (conv.get("created_at") or "")[:10],
                            len(messages), conv.get("name", "")))
        if len(candidates) > 20:
            lines.append("  ... and %d more" % (len(candidates) - 20))
        die("\n".join(lines))

    return candidates[0]


# --------------------------------------------------------------------------
# structure the export actually has
# --------------------------------------------------------------------------

def build_tree(messages):
    """
    Walk `parent_message_uuid` and return the conversation's actual shape.

    Everything downstream that could be misled by array order is decided here, once:

      parent / children  which message each one replies to, by number
      reading_order      depth-first from each root, children in array order
      live_path          the chain the conversation actually continued along
      abandoned          every message not on that chain
      branch_points      messages that share a parent with a sibling

    The live path is the chain ending at the newest leaf. A regenerated reply and its
    replacement both hang off the same parent; the one the conversation carried on
    from is the one whose descendants are still being written, which is the newest.
    Ties break on the later array position, so the result is deterministic.

    Numbers here are 1-based message numbers, matching the manifest.
    """
    count = len(messages)
    by_uuid = {}
    for position, message in enumerate(messages):
        uuid = message.get("uuid")
        if uuid and uuid not in by_uuid:
            by_uuid[uuid] = position

    parent = {}
    children = dict((i, []) for i in range(count))
    roots = []
    for position, message in enumerate(messages):
        found = by_uuid.get(message.get("parent_message_uuid"))
        if found is None or found == position:
            parent[position] = None
            roots.append(position)
        else:
            parent[position] = found
            children[found].append(position)

    # A malformed export could point two messages at each other. Nothing downstream
    # survives a cycle, so break it here and treat the entry point as a root rather
    # than looping forever on a file we were handed.
    for position in range(count):
        seen = set()
        walker = position
        while parent.get(walker) is not None:
            if walker in seen:
                stuck = walker
                if stuck in children.get(parent[stuck], []):
                    children[parent[stuck]].remove(stuck)
                parent[stuck] = None
                roots.append(stuck)
                break
            seen.add(walker)
            walker = parent[walker]

    order = []
    for root in sorted(set(roots)):
        stack = [root]
        while stack:
            node = stack.pop()
            order.append(node)
            stack.extend(reversed(children[node]))

    leaves = [i for i in range(count) if not children[i]]
    live = set()
    tip = None
    if leaves:
        tip = max(leaves, key=lambda i: ((messages[i].get("created_at") or ""), i))
        walker = tip
        while walker is not None:
            live.add(walker)
            walker = parent[walker]

    branch_points = {}
    for _node, kids in children.items():
        if len(kids) > 1:
            for kid in kids:
                branch_points[kid + 1] = [k + 1 for k in kids if k != kid]

    return {
        "parent": dict((i + 1, None if parent[i] is None else parent[i] + 1)
                       for i in range(count)),
        "children": dict((i + 1, [k + 1 for k in children[i]]) for i in range(count)),
        "reading_order": [i + 1 for i in order],
        "live_path": sorted(i + 1 for i in live),
        "abandoned": sorted(i + 1 for i in range(count) if i not in live),
        "live_tip": None if tip is None else tip + 1,
        "roots": [i + 1 for i in sorted(set(roots))],
        "branch_points": branch_points,
    }


def find_branch_points(messages):
    """Messages that share a parent with a sibling. Kept for --list's fork column."""
    return build_tree(messages)["branch_points"]


def describe_tool_input(payload):
    """
    One deterministic line describing a tool's arguments.

    Short string arguments are shown as they are. This matters more than it looks:
    a tool call's informative content is almost always the path it touched, the
    command it ran or the description it gave itself, and all three are short. An
    earlier version reported every string as a character count, which meant a
    manifest could record that a file was written without recording which file —
    and "which file" is exactly the question some investigations turn on. Long
    strings are still reported by length, because a pasted file body is not a
    summary of anything; use --include-tool-io to put those in the record.
    """
    if isinstance(payload, dict):
        if not payload:
            return "(no arguments)"
        parts = []
        for key in sorted(payload):
            value = payload[key]
            if isinstance(value, str):
                if len(value) <= TOOL_INPUT_INLINE_LIMIT:
                    parts.append("%s=%s" % (key, " ".join(value.split())))
                else:
                    parts.append("%s=<%d chars>" % (key, len(value)))
            elif isinstance(value, (list, dict)):
                parts.append("%s=<%s, %d items>" % (key, type(value).__name__, len(value)))
            else:
                parts.append("%s=%r" % (key, value))
        return ", ".join(parts)
    if isinstance(payload, str):
        if len(payload) <= TOOL_INPUT_INLINE_LIMIT:
            return " ".join(payload.split())
        return "<%d chars>" % len(payload)
    return "(none)" if payload is None else repr(payload)


def tool_result_text(content):
    """
    Pull readable text out of a tool result, whatever shape it arrived in.

    Three shapes appear in real exports: a list of content blocks, a bare string,
    and a single block on its own. Missing the third would silently drop a tool's
    entire output, and a recorder that drops a channel without saying so is worse
    than one that never had it.
    """
    if isinstance(content, list):
        chunks = []
        for block in content:
            if isinstance(block, dict) and isinstance(block.get("text"), str):
                chunks.append(block["text"])
            elif isinstance(block, str):
                chunks.append(block)
        return "\n".join(chunks)
    if isinstance(content, dict) and isinstance(content.get("text"), str):
        return content["text"]
    if isinstance(content, str):
        return content
    return ""


class Redactor(object):
    """
    The sweep, done by script rather than by care.

    spec.md requires shipped excerpts to be swept before they enter the repo, and a
    sweep performed by reading carefully is a sweep that works until the day someone
    is tired. Rules are regular expressions with fixed replacements, applied to every
    text-bearing field on the way into the manifest — so the record the investigator
    reads, the record the gate matches quotations against, and the record that ships
    are all the same swept record. Counts are reported, so a rule that matched
    nothing is visible rather than assumed effective.
    """

    def __init__(self, rules, source_name, source_digest):
        self.rules = rules
        self.source_name = source_name
        self.source_digest = source_digest
        self.counts = dict((rule["name"], 0) for rule in rules)

    def __call__(self, text):
        if not text:
            return text
        for rule in self.rules:
            text, hits = rule["regex"].subn(rule["replacement"], text)
            if hits:
                self.counts[rule["name"]] += hits
        return text

    def summary(self):
        return {"rules_file": self.source_name,
                "rules_sha256": self.source_digest,
                "replacements": dict(self.counts)}


def load_redaction_rules(path):
    """Read a redaction rules file: a list of {name, pattern, replacement}."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        die("could not open the redaction rules %s: %s" % (path, exc.strerror or exc))
    digest = hashlib.sha256(raw).hexdigest()
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        die("could not read %s as JSON: %s" % (path, exc))
    if isinstance(data, dict):
        data = data.get("rules")
    if not isinstance(data, list) or not data:
        die("%s should hold a list of rules, each with name, pattern and "
            "replacement." % path)

    rules = []
    for position, entry in enumerate(data):
        if not isinstance(entry, dict):
            die("rule %d in %s is not an object." % (position, path))
        for field in ("name", "pattern", "replacement"):
            if not isinstance(entry.get(field), str) or not entry[field]:
                die("rule %d in %s is missing %s." % (position, path, field))
        try:
            regex = re.compile(entry["pattern"], re.IGNORECASE)
        except re.error as exc:
            die("rule %r in %s has an unusable pattern: %s"
                % (entry["name"], path, exc))
        rules.append({"name": entry["name"], "regex": regex,
                      "replacement": entry["replacement"],
                      "pattern": entry["pattern"]})
    return Redactor(rules, path, digest)


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


def build_segments(message, options):
    """
    Walk one message's content blocks in order and turn each into a labelled segment.

    Order is preserved deliberately: the interleaving of speech and tool calls is
    how a fault travels through a turn, and a propagation trace needs to see it.
    """
    include_tool_io = options["include_tool_io"]
    include_attachments = options["include_attachments"]
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

        elif kind == "image":
            segments.append({
                "channel": CH_ATTACHMENT,
                "name": "(image)",
                "text": "",
                "note": "an image was in this message; the export carries no text for "
                        "it, so the recorder cannot say what it showed",
            })

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

    limit = options["tool_io_limit"]
    redact = options["redact"]
    for segment in segments:
        # Truncation keeps a true prefix rather than a summary, so a quotation that
        # falls inside what was kept still verifies verbatim and one that falls
        # outside it fails honestly instead of half-matching.
        if limit and segment["channel"] in (CH_ACTION, CH_RESULT, CH_ATTACHMENT):
            body = segment.get("text") or ""
            if len(body) > limit:
                segment["text"] = body[:limit]
                segment["note"] = ((segment.get("note") or "")
                                   + "; kept to the first %d chars, %d withheld from "
                                     "this manifest" % (limit, len(body) - limit))
        if redact is not None:
            for field in ("text", "note", "name", "tool"):
                if isinstance(segment.get(field), str):
                    segment[field] = redact(segment[field])

    return segments


def build_manifest(conv, conv_index, source_path, source_digest, args, redact=None):
    """Assemble the whole manifest as data. Rendering happens separately."""
    messages = conv.get("chat_messages") or []
    tree = build_tree(messages)
    branches = tree["branch_points"]
    live = set(tree["live_path"])

    first, last = 1, len(messages)
    if args.messages:
        first, last = args.messages

    options = {
        "include_tool_io": args.include_tool_io,
        "include_attachments": args.include_attachments,
        "tool_io_limit": args.tool_io_limit,
        "redact": redact,
    }

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
            "parent": tree["parent"][number],
            "children": tree["children"][number],
            "branch_status": BRANCH_LIVE if number in live else BRANCH_ABANDONED,
            "branch_siblings": branches.get(number, []),
            "segments": build_segments(message, options),
        })

    assistant_total = sum(1 for m in messages if m.get("sender") == "assistant")
    coverage = {"full": 0, "summary-only": 0, "absent": 0}
    for message in messages:
        if message.get("sender") == "assistant":
            coverage[reasoning_state(message)] += 1

    text = (lambda value: redact(value)) if redact is not None else (lambda value: value)

    manifest = {
        "schema_version": SCHEMA_VERSION,
        # The file's name, never the path it was read from. A manifest is written to be
        # shipped, and `parse.py /home/someone/Downloads/...` would put a real person's
        # directory layout into it. The fingerprint below identifies the file exactly;
        # the path it happened to sit at identifies its owner and nothing else.
        "source_file": text(os.path.basename(source_path) or source_path),
        "source_sha256": source_digest,
        "conversation": {
            "index": conv_index,
            "uuid": conv.get("uuid", ""),
            "name": text(conv.get("name", "")),
            "created_at": conv.get("created_at", ""),
            "updated_at": conv.get("updated_at", ""),
            "message_count": len(messages),
        },
        "window": {"first": first, "last": last,
                   "is_full_conversation": (first == 1 and last == len(messages))},
        "reasoning_coverage": {"assistant_messages": assistant_total, **coverage},
        "branch_points": {str(k): v for k, v in sorted(branches.items())},
        "tree": {
            "roots": tree["roots"],
            "reading_order": tree["reading_order"],
            "live_tip": tree["live_tip"],
            "abandoned": tree["abandoned"],
        },
        "messages": entries,
    }
    if redact is not None:
        manifest["redaction"] = redact.summary()
    return manifest


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
    if manifest.get("redaction"):
        redaction = manifest["redaction"]
        total = sum(redaction["replacements"].values())
        add("    swept-with        %s (sha256 %s)"
            % (redaction["rules_file"], redaction["rules_sha256"][:16]))
        add("    replacements      %d across %d rules"
            % (total, len(redaction["replacements"])))
    add("")

    if manifest.get("redaction"):
        add("## What was swept out of this record")
        add("")
        add("Passages matching the rules below were replaced before this manifest was")
        add("written, so the text here is the text everything downstream reads: the")
        add("investigator, the quotation check, and anyone reading the repo. A rule")
        add("that replaced nothing is shown too, because a sweep that quietly matched")
        add("nothing looks identical to one that worked.")
        add("")
        for name, count in sorted(manifest["redaction"]["replacements"].items()):
            add("    %-24s %d replacement%s" % (name, count, "" if count == 1 else "s"))
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

    tree = manifest.get("tree") or {}
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
        add("")
        add("The conversation carried on down one of those branches and not the others.")
        add("Messages on the branch it carried on down are marked *live* below; the rest")
        add("are marked *abandoned* and are not part of what either party went on to")
        add("read. A causal trace that runs through an abandoned message is tracing a")
        add("path the conversation never took.")
        add("")
        if tree.get("abandoned"):
            add("    abandoned         %s"
                % ", ".join(str(n) for n in tree["abandoned"]))
        add("    conversation ends %s" % (tree.get("live_tip") or "unknown"))
    else:
        add("None. Every message has its own parent, so the conversation runs as one line,")
        add("and reading it in message order is reading it in the order it happened.")
    if len(tree.get("roots") or []) > 1:
        add("")
        add("Note: this conversation has %d separate starting points in the export rather"
            % len(tree["roots"]))
        add("than one. That is unusual and worth knowing before reading anything into the")
        add("order. The line the conversation ended on runs to message %s."
            % (tree.get("live_tip"),))
    add("")
    add("---")
    add("")

    for entry in manifest["messages"]:
        add("## [%d] %s — %s" % (entry["index"], entry["role"], entry["timestamp"]))
        if entry["branch_siblings"]:
            add("")
            add("*Fork: an alternative version of the same turn as message %s.*"
                % ", ".join(str(s) for s in entry["branch_siblings"]))
        if entry.get("branch_status") == BRANCH_ABANDONED:
            add("")
            add("*Abandoned: the conversation did not continue from this message. Nothing "
                "after it read it.*")
        # Only worth saying when it is not the message immediately above. Printing it
        # on every turn of a linear conversation is noise that trains the reader to
        # skip the line, which is the line that matters on the one turn it differs.
        if entry.get("parent") is not None and entry["parent"] != entry["index"] - 1:
            add("")
            add("*Replies to message %d, not the message above it.*" % entry["parent"])
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
    picker.add_argument("--include-empty", action="store_true",
                        help="with --list, also show conversations that hold no "
                             "messages (hidden by default: a real export carries "
                             "empty duplicate shells of real chats)")

    shaping = parser.add_argument_group("what goes in the manifest")
    shaping.add_argument("--include-tool-io", action="store_true",
                         help="inline tool arguments and tool output (off by default: verbose)")
    shaping.add_argument("--include-attachments", action="store_true",
                         help="inline the text extracted from attached files (off by default)")
    shaping.add_argument("--tool-io-limit", type=int, default=0, metavar="N",
                         help="keep only the first N characters of each tool or "
                              "attachment text, and say so in the record")
    shaping.add_argument("--redact", metavar="RULES.json",
                         help="apply a redaction rules file to every text field on "
                              "the way in, and record what it replaced")
    shaping.add_argument("--json", action="store_true",
                         help="emit JSON instead of markdown (this is what check.py reads)")
    shaping.add_argument("--out", metavar="PATH", help="write here instead of standard output")

    args = parser.parse_args(argv)
    use_utf8_streams()

    if args.tool_io_limit < 0:
        die("--tool-io-limit takes a positive number of characters.")

    convs, digest = load_export(args.export)

    if args.list:
        rows = conversation_rows(convs)
        shown = [r for r in rows if r["messages"] or args.include_empty]
        hidden = len(rows) - len(shown)
        lines = ["%d conversations in %s" % (len(rows), args.export), ""]
        lines.append("index  started     msgs  forks  uuid                                  name")
        for row in shown:
            lines.append("%5d  %s  %4d  %5d  %-36s  %s"
                         % (row["index"], row["created"], row["messages"],
                            row["branches"], row["uuid"], row["name"]))
        if hidden:
            lines.append("")
            lines.append("%d conversation%s with no messages hidden. They are empty "
                         "duplicates of real" % (hidden, "" if hidden == 1 else "s"))
            lines.append("chats and share their names; --include-empty shows them.")
        lines.append("")
        lines.append("Names repeat in a real export. --uuid is the only selector that "
                     "cannot be ambiguous.")
        write_output("\n".join(lines) + "\n", args.out)
        return 0

    redact = load_redaction_rules(args.redact) if args.redact else None

    conv_index, conv = select_conversation(convs, args)
    messages = conv.get("chat_messages") or []
    if not messages:
        die("that conversation has no messages in the export, so there is nothing to\n"
            "read. Empty shells sharing a name with a real conversation are in the\n"
            "export; the real one has the same name and a different uuid. Run --list.")
    if args.messages and args.messages[0] > len(messages):
        die("--messages starts at %d but the conversation only has %d messages."
            % (args.messages[0], len(messages)))

    manifest = build_manifest(conv, conv_index, args.export, digest, args, redact)

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
