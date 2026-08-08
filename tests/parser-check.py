#!/usr/bin/env python3
"""
parser-check.py — assert the properties of parse.py that nothing else can check.

    python tests/parser-check.py

`verify.py` proves the gate discriminates. It runs parse.py on the way, but only ever
asks whether the resulting manifest lets a report pass or fail. Four things parse.py
guarantees are invisible from there, and all four were either established by an earlier
build stage or added in M4, so all four need an assertion that outlives the person who
remembers why:

- **Determinism.** M1 verified same-input-same-output by hand. M4 rewrote the branch
  logic, which invalidated that verification. Asserting it here means the next person to
  touch the parser cannot quietly break it.
- **The tree.** The export is a flat array with `parent_message_uuid` on every message.
  Read as a list, an abandoned draft sits between two live turns and reads as part of the
  conversation. The whole point of walking the tree is that the manifest says which
  messages the conversation actually continued from, so that is what gets asserted.
- **The sweep.** Redaction is what makes shipping a real excerpt safe. A sweep that
  silently matched nothing looks exactly like one that worked, so both the replacement
  and the count are checked, including a rule that is supposed to match nothing.
- **Not leaking the reader's own machine.** A manifest is written to be shipped. The
  export's *name* goes in it; the path it was read from does not.

Reads its own fixture. It must never read `synthetic-export.json`: every clean report
carries that file's fingerprint, so a test that touched it would fail the whole suite on
`record-pairing` instead of on itself.

Stdlib only. Python 3.8+. Exit 0 if every property holds, 1 if any does not.
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORT = os.path.join(HERE, "fixtures", "branched-export.json")
RULES = os.path.join(HERE, "fixtures", "test-sweep-rules.json")
PARSE = os.path.join(ROOT, "parse.py")

CONV = "11111111-0000-4000-8000-000000000001"
EMPTY_SHELL = "22222222-0000-4000-8000-000000000002"

failures = []


def use_utf8_streams():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def run(argv, cwd=ROOT):
    process = subprocess.Popen([sys.executable, PARSE] + argv, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=cwd)
    out, err = process.communicate()
    return (process.returncode, out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))


def check(name, condition, detail=""):
    if condition:
        print("  pass  %s" % name)
    else:
        print("  FAIL  %s%s" % (name, ("  — " + detail) if detail else ""))
        failures.append(name)


def manifest(extra, export=EXPORT):
    code, out, err = run([export, "--uuid", CONV, "--json"] + extra)
    if code != 0:
        raise SystemExit("parser-check.py: parse.py exited %d:\n%s" % (code, err))
    return json.loads(out)


def main():
    use_utf8_streams()
    print("The tree — a fork is marked, not flattened")

    data = manifest([])
    by_number = dict((m["index"], m) for m in data["messages"])
    tree = data["tree"]

    check("message 5 is the live branch",
          by_number[5]["branch_status"] == "live",
          "got %r" % by_number[5]["branch_status"])
    check("message 4 is marked abandoned",
          by_number[4]["branch_status"] == "abandoned",
          "got %r" % by_number[4]["branch_status"])
    check("messages 4 and 5 are recorded as siblings",
          by_number[4]["branch_siblings"] == [5] and by_number[5]["branch_siblings"] == [4],
          "got %r and %r" % (by_number[4]["branch_siblings"],
                             by_number[5]["branch_siblings"]))
    check("message 6 replies to 5, not to the message above it",
          by_number[6]["parent"] == 5, "got %r" % by_number[6]["parent"])
    check("message 3 is the fork point, with two children",
          by_number[3]["children"] == [4, 5], "got %r" % by_number[3]["children"])
    check("the abandoned set is exactly {4}",
          tree["abandoned"] == [4], "got %r" % tree["abandoned"])
    check("the conversation ends at message 6",
          tree["live_tip"] == 6, "got %r" % tree["live_tip"])
    check("one root",
          tree["roots"] == [1], "got %r" % tree["roots"])
    check("the markdown says which message was abandoned",
          "abandoned" in run([EXPORT, "--uuid", CONV])[1].lower())

    print("\nAll the text-bearing fields, not the message text alone")
    full = manifest(["--include-tool-io", "--include-attachments"])
    segments = dict((m["index"], m["segments"]) for m in full["messages"])
    channels = [s["channel"] for s in segments[2]]
    check("message 2 carries a reasoning summary, speech, an action and a result",
          channels == ["REASONING-SUMMARY", "SAID", "ACTION", "RESULT"],
          "got %r" % channels)
    check("the tool's path is in the record even without --include-tool-io",
          "notes.md" in json.dumps(manifest([])["messages"]),
          "a manifest that records a file was written but not which file is not a record")
    check("the tool result's text is carried",
          any("the notes say to publish" in (s.get("text") or "") for s in segments[2]))
    check("the attachment's extracted text is carried",
          any(s["channel"] == "ATTACHMENT" and "the brief lives at" in (s.get("text") or "")
              for s in segments[3]))
    check("withheld reasoning is labelled summary-only",
          [m for m in full["messages"] if m["index"] == 2][0]["reasoning"] == "summary-only")
    check("present reasoning is labelled full",
          [m for m in full["messages"] if m["index"] == 5][0]["reasoning"] == "full")
    check("the header counts both, and the absent one",
          full["reasoning_coverage"] == {"assistant_messages": 3, "full": 1,
                                         "summary-only": 1, "absent": 1},
          "got %r" % full["reasoning_coverage"])

    print("\nThe sweep — what it replaced, and what it did not")
    swept = manifest(["--include-tool-io", "--include-attachments", "--redact", RULES])
    body = json.dumps(swept["messages"])
    check("no filesystem path survives", "testperson" not in body)
    check("no repository url survives", "github.com/" not in body)
    check("the replacement marker is there", "[path]" in body and "[url]" in body)
    counts = swept["redaction"]["replacements"]
    check("every replacement is counted",
          counts["local-filesystem-path"] == 4 and counts["repository-url"] == 1,
          "got %r" % counts)
    check("a rule that matched nothing still reports itself",
          counts.get("matches-nothing-on-purpose") == 0,
          "a sweep that quietly matched nothing must not look like one that worked")
    check("the rules file is fingerprinted in the manifest",
          swept["redaction"]["rules_sha256"]
          == hashlib.sha256(open(RULES, "rb").read()).hexdigest())

    print("\nTruncation is a true prefix, and says so")
    capped = manifest(["--include-tool-io", "--tool-io-limit", "10"])
    result = [s for s in dict((m["index"], m["segments"])
                             for m in capped["messages"])[2]
              if s["channel"] == "RESULT"][0]
    check("the kept text is a prefix of the real text",
          result["text"] == "the notes ", "got %r" % result["text"])
    check("the record says how much was withheld", "withheld" in result["note"])

    print("\nEmpty shells, and uuid as the only safe key")
    code, listing, _err = run([EXPORT, "--list"])
    check("--list hides the empty shell",
          EMPTY_SHELL[:8] not in listing and CONV[:8] in listing)
    check("--list says how many it hid", "no messages hidden" in listing)
    code, _out, err = run([EXPORT, "--name", "forked-session", "--json"])
    check("a name shared with an empty shell still resolves",
          code == 0, "exited %d: %s" % (code, err.strip()))
    code, _out, err = run([EXPORT, "--uuid", EMPTY_SHELL, "--json"])
    check("naming the empty shell outright fails with an explanation",
          code == 2 and "no messages" in err)

    print("\nDeterminism, and not shipping the reader's own filesystem")
    workdir = tempfile.mkdtemp(prefix="ofr-parser-")
    try:
        digests = []
        for run_number in (1, 2):
            target = os.path.join(workdir, "m%d.json" % run_number)
            run([EXPORT, "--uuid", CONV, "--include-tool-io", "--include-attachments",
                 "--redact", RULES, "--json", "--out", target])
            digests.append(hashlib.sha256(open(target, "rb").read()).hexdigest())
        check("same input, same manifest, byte for byte", digests[0] == digests[1])

        # The same conversation reached by an absolute path and by a relative one is the
        # same conversation, and the manifest must not be able to tell you whose machine
        # it was read on.
        relative = os.path.relpath(EXPORT, ROOT)
        code, out, _err = run([relative, "--uuid", CONV, "--json"])
        by_relative = json.loads(out)
        by_absolute = manifest([])
        check("the export's path is not in the manifest",
              by_absolute["source_file"] == "branched-export.json",
              "got %r" % by_absolute["source_file"])
        check("relative and absolute paths give the same manifest",
              by_relative == by_absolute)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print("")
    if failures:
        print("PARSER CONTRACT BROKEN")
        for name in failures:
            print("  - %s" % name)
        return 1
    print("PARSER CONTRACT HOLDS  the tree is walked, every channel is read, the sweep "
          "is counted,\n                       and the same export gives the same "
          "manifest every time.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
