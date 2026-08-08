# Run notes — how this run was set up, isolated and checked

**REAL.** Run on 2026-08-08 during build stage M4.

## The record

    conversation   nbs-wor-1.0-z
    uuid           e19178eb-10e5-4d3f-aebd-9cbbba5b33ce
    window         messages 42-47 of 56
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575

Built with:

    python parse.py conversations.json \
      --uuid e19178eb-10e5-4d3f-aebd-9cbbba5b33ce \
      --messages 42-47 --include-tool-io --include-attachments \
      --redact runs/02-the-two-hour-job/sweep-rules.json \
      --out runs/02-the-two-hour-job/message-manifest.md

and the same command with `--json`. The intake identified this window by the export's array
indices, which count from 0; `parse.py` numbers from 1. The withheld answer key is `idx 47` in
the intake and message 48 here.

**Why the window starts where it does.** The intake fixed the end of the window at the
complaint and left the start to judgement: *include enough preceding context for causal tracing
(the work-order messages)*. The window runs from message 42, one message earlier than the
minimum that covers the causal chain, and the extra message is deliberate. Message 42 carries the
*previous* work order — written before the instruction to keep things simple, and also carrying
no run-time estimate.

That matters because it gives the run the material to reach the opposite conclusion from the one
the answer key holds. With only messages 43 to 47, every unpriced order in view sits after the
simple-mode instruction, and *the instruction caused the packing* is the only available reading.
With message 42 in view, the run can see that orders were unpriced before that instruction
existed, and can decide for itself whether the instruction is causal. It decided it was not, and
argued against the key on exactly that point. A window that can only support the expected answer
is not evidence that the answer was found.

**No cap on tool or attachment text here.** Unlike the other two runs, the large channel in this
window is not machine-generated file dumps but pasted job output — the audit report, the post
draft, the finished job's own close-out — which is primary evidence and is quoted by the report.
It ships whole.

## Sensitivity — the sweep

This is the only run whose window the intake did **not** clear as verified. The preceding
context was flagged as carrying local filesystem paths, a repository URL under a real account
handle, and a replay identifier. The intake's ruling was that every shipped excerpt from before
the complaint must be swept for exactly those patterns and redacted as `[path]`, `[url]`, `[id]`.

That sweep is mechanical, not manual. [`sweep-rules.json`](sweep-rules.json) holds four rules;
`parse.py --redact` applies them to every text-bearing field **on the way into the manifest**.
The consequence is the point: the record the investigator read, the record `check.py` matched
its thirteen quotations against, and the record in this folder are all the same swept record.
There is no unswept version that anything downstream was built from.

What it replaced, as recorded in the manifest's own header:

    account-handle           1 replacement
    local-filesystem-path    0 replacements
    replay-identifier        3 replacements
    repository-url           1 replacement

The zero is reported rather than omitted on purpose: a rule that matched nothing looks identical
to a rule that worked unless the count is shown. Here it means the flagged paths were in messages
outside this window, which is what the intake said. The shipped manifest was then re-scanned
independently for all four patterns plus credentials, database endpoints, e-mail addresses and
currency figures. Nothing matched.

The intake named three patterns and those three were applied. Two things were deliberately not
redacted: commit hashes appearing in the pasted audit, which identify nothing once the repository
they belong to is redacted, and the orchestrator's own initials, which the intake rules ship
as-is along with everything else in his own words.

## How the run was isolated

Identical protocol to the other two runs: a working folder outside the repository holding a copy
of `diagnostician/`, the two manifest files and `incident-statement.md`; an instruction that the
folder was the whole case and that the repository, the raw export and every build document were
off limits; and an inspection afterwards.

**The answer key did not exist anywhere on disk when the run happened.**
`runs/02-the-two-hour-job/answer-key.md` was written after `report.md` was finished and gated.

The inspection found two working files the run wrote for itself while checking its own
quotations, and one file inside its copy of `diagnostician/` — see below. Nothing else was
touched.

**The honest limit**, as with the other runs: the raw export was present and readable on the
machine, and nothing mechanically prevented the investigator from finding the source
conversation. The reasons to believe it did not are in
[comparison-note.md](comparison-note.md), and for this run they carry more weight than usual
because this run agreed with the key most closely. The load-bearing ones are that the report
argues *against* the key's attribution, does not share its organising framing, and hedges on a
question the key answers.

## The ninth failure mode

The report names `uncosted-commitment`, which did not exist when the run started. `rules.md`
forbids naming a mode inside a report without its file, and `spec.md` makes the taxonomy
extensible, so the run was permitted to write the file first if no existing mode fitted — after
checking all eight. It wrote
[`uncosted-commitment.md`](../../diagnostician/reference/failure-modes/uncosted-commitment.md)
into its sandbox and cited it.

The file was reviewed before being promoted into `diagnostician/`, against the four things the
failure-modes README requires of a new mode and against the nearest existing mode. It was
promoted unedited. The gate is the check that this rule is real rather than aspirational: run
against the taxonomy without the new file, the report fails on `failure-mode-file` and on
nothing else. Both results are recorded below.

## The gate

    python check.py runs/02-the-two-hour-job/report.md \
      --manifest runs/02-the-two-hour-job/message-manifest.json

    PASS  13 quotations checked

Passed first time, unedited, once the ninth mode was in place. Run against the original eight
modes it fails on exactly one check:

    [failure-mode-file] failure mode 'uncosted-commitment' has no file

which is the taxonomy's extension rule being enforced rather than trusted.
