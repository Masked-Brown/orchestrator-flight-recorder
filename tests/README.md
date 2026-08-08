# Tests

The gate is only worth having if it demonstrably catches things, and the parser is only
worth trusting if it gives the same answer twice. Two suites, both stdlib, both quick:

    python tests/verify.py        # the gate discriminates
    python tests/parser-check.py  # the parser reads the record correctly

Exit 0 means the contract holds. Exit 1 means it does not, and the output says where.
No packages to install, and nothing here touches a real conversation export.

## What is in here

- **`fixtures/synthetic-export.json`** — a small CONSTRUCTED export in the same shape as
  a real Claude data export: two conversations, both channels of assistant output, a
  message carrying two separate stretches of speech either side of a tool call, a
  reasoning block withheld with only a summary surviving, two withheld with nothing
  surviving, and a tool call that returned an error. Invented for these tests. It is not
  a record of anything that happened.
- **`fixtures/branched-export.json`** — a second CONSTRUCTED export, used only by
  `parser-check.py`. Six messages in which one reply was regenerated, so the conversation
  forks and one branch is abandoned, plus an empty conversation sharing its name. Kept
  separate from the export above on purpose: see the note at the end of this file.
- **`fixtures/test-sweep-rules.json`** — redaction rules for `parser-check.py`, including
  one deliberately written to match nothing.
- **`cases/`** — well-formed reports. Every one must pass.
- **`negative/`** — deliberately broken reports. Every one must fail, on the check it was
  built to break.
- **`verify.py`** — runs both directions and asserts the gate's contract.
- **`parser-check.py`** — asserts the parser's contract.

## The gate's contract

Four things are asserted, and the second is the one that matters.

**One — every clean report passes.** Three of them: a `pilot-error` finding with ranked
contributing factors, an `undetermined` finding on a record too thin to settle, and an
`undetermined` finding where the origin sits outside the window supplied. Between them
they exercise quotation from the speech and reasoning channels, shortening with `[...]`,
the explicit `none.` forms, and message numbering that stays global when only a window is
given.

**Two — every broken report fails on its own check, and on nothing else.** Merely failing
proves nothing: a gate that rejected all input would do that too, and would also reject
every clean report above. So each negative fixture is derived from a clean one by exactly
one mutation, and the assertion is that the set of checks it trips is exactly the one
check that mutation should trip. That is what makes this evidence rather than decoration.

**Three — every check has a fixture behind it.** `verify.py` asks `check.py` what checks it
can report and fails if any of them has no negative fixture. Without this a check could be
added, never exercised, and quietly do nothing while looking like enforcement.

**Four — an invocation that checks nothing must not exit 0.** All of the above is worth
nothing if the gate can be run in a way that reads neither the report nor a record and
still returns success, because the exit code is the only thing a CI step or a shell script
reads. Eight such invocations are asserted to exit 2 and to never print `PASS`: a report
with no `--manifest`, no arguments, a manifest with no report, a manifest that does not
exist, a JSON file that is not a manifest, a report that does not exist, and `--list-checks`
handed a report or a manifest. That last pair is the one this was written for — see
`OPEN-DEFECTS.md`.

## The parser's contract

`verify.py` runs `parse.py` on the way to everything it does, but it only ever asks
whether the resulting manifest lets a report pass or fail. Four properties are invisible
from there and all four are load-bearing, so `parser-check.py` asserts them directly:

**The tree.** The export is a flat array in which every message names its parent. When a
reply is regenerated, both versions sit in that array, and read as a list the abandoned
one appears between two live turns as though it were part of the conversation. The test
asserts the manifest says which branch the conversation actually continued down, which
message is abandoned, and where a reply attaches when it is not to the message above it.

**Every channel is read.** Speech, reasoning, withheld reasoning that left only a summary,
tool calls, tool output and attachment text each get an assertion, because a recorder that
silently drops a channel is worse than one that never had it. Including the small one that
bit: a tool call whose *path* is missing from the record tells you a file was written but
not which file.

**The sweep is counted.** Redaction is what makes shipping a real excerpt safe. The test
checks that the sensitive strings are gone, that the replacement markers are there, that
the counts are right, and that a rule matching nothing still reports itself as zero —
because a sweep that quietly matched nothing looks identical to one that worked.

**Determinism, and whose machine it ran on.** Same export, same manifest, byte for byte.
And the manifest records the export's *name*, never the path it was read from, so parsing
`/home/someone/Downloads/conversations.json` cannot put a real person's directory layout
into a file written to be published.

## The manifests are built, not stored

`verify.py` runs `parse.py` over the synthetic export to produce the manifests the reports
are checked against, rather than committing manifests alongside them. Two reasons: the
tests then exercise the real parser-to-gate path instead of a stored approximation of it,
and a stored manifest could drift from what `parse.py` actually emits without anything
noticing.

One consequence worth knowing: the reports carry the export's `source-sha256` in their
heading block, and the gate fails a report whose fingerprint does not match the record it
is handed. So **editing `fixtures/synthetic-export.json` by even one byte will fail every
test** on `record-pairing` until the new fingerprint is written into each report. That is
the check doing its job. `.gitattributes` keeps the file's bytes identical across
platforms, which is why the suite also runs on Windows in CI.

That is also why `parser-check.py` has a fixture of its own rather than adding a fork to
the export above. A parser test needs to change its input to test anything, and every
change to that file costs twenty-four report edits. Two fixtures is the cheaper answer.
