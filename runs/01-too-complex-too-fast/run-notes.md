# Run notes — how this run was set up, isolated and checked

**REAL.** Run on 2026-08-08 during build stage M4.

## The record

    conversation   yt-wor-1.2-future-crons
    uuid           006f1fc0-127e-4eb3-8fce-00afe65fa7b3
    window         messages 10-12 of 32
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575

Built with:

    python parse.py conversations.json \
      --uuid 006f1fc0-127e-4eb3-8fce-00afe65fa7b3 \
      --messages 10-12 --include-tool-io --include-attachments --tool-io-limit 2000 \
      --out runs/01-too-complex-too-fast/message-manifest.md

and the same command with `--json` for the machine-readable copy the gate reads. Running it
again reproduces both files byte for byte; that property is asserted in
`tests/parser-check.py`.

**Message numbering.** `parse.py` numbers messages from 1. The intake that chose this incident
identified the window by the export's own array indices, which count from 0, as `idx 9 to 11`.
Those are the same three messages. Everything in this folder uses the manifest's numbering, so
the withheld answer key is `idx 12` in the intake and message 13 here.

**Why the tool output is capped.** Message 10 contains six tool calls that read two documents
totalling roughly 48,000 characters. Inlining them whole would have quadrupled the manifest with
machine-read source material, so each is kept to its first 2,000 characters. The cap keeps a
true prefix rather than a summary, so a quotation falling inside what was kept still verifies
and one falling outside fails honestly instead of half-matching. Each capped segment records how
much was withheld, and the report noticed: it states that 15,745 characters were withheld from
one of them and that nothing in its finding rests on that text.

## Sensitivity

The M4 intake records this window as verified clean by the scout, and it was re-checked during
the run by script against filesystem paths, repository URLs, account handles, credentials,
database endpoints, e-mail addresses and currency figures. Nothing matched, so no redaction rules
were applied at the time. The intake flags that messages 3 to 5, 24 and 29 of this conversation
carry database identifiers and revenue figures; all of them are outside the window and none of
them is in this folder.

**A sweep was added afterwards, and this is the honest account of it.** The pattern set above was
built from the categories the intake named. It had a blind spot: it did not look for personal
names or platform identifiers. The window carries both — the orchestrator's own real name, as the
default value of a configuration constant, and the identifier of a real channel, twice, inside a
file path. This repository is public under a pseudonymous account, so shipping those two strings
would have linked the account to the person. The M4 recovery session caught this in the
pre-commit sweep and applied [`sweep-rules.json`](sweep-rules.json), two rules, three
replacements:

    python parse.py conversations.json \
      --uuid 006f1fc0-127e-4eb3-8fce-00afe65fa7b3 \
      --messages 10-12 --include-tool-io --include-attachments --tool-io-limit 2000 \
      --redact runs/01-too-complex-too-fast/sweep-rules.json \
      --out runs/01-too-complex-too-fast/message-manifest.md

This is stricter than the intake's ruling rather than looser, which is the safe direction for a
sensitivity call made without the human in the room. It is flagged in the M4 handover for the
human's final read, and it is reversible: deleting the rules file and re-running the original
command restores the unswept manifest exactly.

**What it costs, stated plainly.** Run 2's sweep has a property this one does not: it ran *before*
the investigation, so the record the investigator read, the record the gate matched against, and
the record in this folder are all one record. Here the investigator read the unswept text and the
folder ships the swept text. That divergence is three strings wide. Neither string is quoted in
[report.md](report.md), neither is named in its reasoning, and the gate re-run against the swept
manifest still verifies all eleven quotations — so nothing in the finding rests on what was
removed. But the property is weaker for this run than for run 2, and the difference is recorded
rather than smoothed over.

## How the run was isolated

The investigation ran in a fresh context with no access to this repository's build materials.

1. A working folder was created outside the repository containing exactly four things: a copy
   of `diagnostician/`, `message-manifest.md`, `message-manifest.json`, and
   `incident-statement.md`. Nothing else was in it.
2. The investigator was told that folder was the whole of the case, and was instructed not to
   read, search or list anything outside it — naming the repository, the raw export, and any
   build plan, handover or journal as off limits.
3. **The answer key did not exist anywhere on disk when the run happened.**
   `runs/01-too-complex-too-fast/answer-key.md` was written after `report.md` was finished and
   gated. This is the part of the isolation that does not rest on instructions being obeyed.
4. Afterwards the sandbox was inspected: no files were created beyond `report.md`, and every
   file under its copy of `diagnostician/` was unmodified.

**The honest limit.** The investigator ran on a machine where the raw export was present and
readable. Nothing prevented it mechanically from going and finding the source conversation. What
can be said is that it was told not to, that it wrote no file suggesting it did, and — the load
bearing part — that the report is wrong in ways a contaminated run would not have been. Those
are set out in [comparison-note.md](comparison-note.md), and the strongest of them is that the
report missed a contradiction sitting inside its own window that the answer key states outright.

## The gate

    python check.py runs/01-too-complex-too-fast/report.md \
      --manifest runs/01-too-complex-too-fast/message-manifest.json

    PASS  11 quotations checked

**The report was not edited to achieve that**, and the first run of the gate rejected it. The
whole of the disagreement was one anchor written `Msg 12 (assistant, SAID):` at the start of a
sentence, where `check.py` matched only a lower-case `msg`. That is a capital letter where
English puts one, not a defect in the citation: the message number, the role and the channel were
all correct and the quotation verified.

`check.py` was changed to accept both cases and the report was left exactly as the run produced
it. Recorded here because the alternative — quietly retyping one letter in the output and
reporting a clean pass — is how a gate stops being evidence. One of the clean fixtures in
`tests/cases/` now carries a sentence-initial anchor, so the widening is itself tested.
