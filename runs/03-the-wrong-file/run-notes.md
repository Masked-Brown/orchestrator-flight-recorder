# Run notes — how this run was set up, isolated and checked

**REAL.** Run on 2026-08-08 during build stage M4.

## The record

    conversation   AI voice training and qualitative reinforcement framework
    uuid           6b43b0d6-cdaf-4ccd-b8c1-43c62c4604ab
    window         messages 1-9 of 14
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575

Built with:

    python parse.py conversations.json \
      --uuid 6b43b0d6-cdaf-4ccd-b8c1-43c62c4604ab \
      --messages 1-9 --include-tool-io --include-attachments --tool-io-limit 2000 \
      --out runs/03-the-wrong-file/message-manifest.md

and the same command with `--json`. The intake identified this window by the export's array
indices as `idx 0 to 8`; `parse.py` numbers from 1, so those are messages 1 to 9 here.

**Why tool output matters more in this run than in the others.** The question is which file was
produced, and the answer is inside the tool calls that produced it. This is the run that caused
a change to `parse.py`: the parser previously summarised every string argument as a character
count, so a manifest recorded that a file had been written without recording *which* file. It
now shows short string arguments — paths, commands, descriptions — as they are. Without that
change this incident would have been undiagnosable from the manifest, which is a fair test of
whether a recorder is reading enough. The 2,000-character cap still applies to the long
arguments, so the written documents are read here through their opening text and their section
headings rather than in full, and the report says so in section 2.

## Sensitivity

The intake records the whole of this conversation as verified clean, so no windowing judgement
was needed and no redaction rules were applied. Re-checked here by script against filesystem
paths, repository URLs, account handles, credentials, database endpoints, e-mail addresses and
currency figures. Nothing matched.

## How the run was isolated

Identical protocol to the other two runs. A working folder outside the repository containing a
copy of `diagnostician/`, the two manifest files and `incident-statement.md`, and nothing else;
an instruction that the folder was the whole case and that the repository, the raw export and
every build document were off limits; and an inspection afterwards confirming no extra files
were written and the copy of `diagnostician/` was unmodified.

**This run had no answer key to withhold.** The failure is fully contained in the window: the
request is at message 5, the delivery at message 6, and the orchestrator states the mismatch
himself at message 9. There was nothing outside the window to hide, so the isolation here
protects against a different thing — the run reading the intake, the build plan or this
repository's own expectations about what it was supposed to find. That mattered, because there
were expectations, and the run did not meet them. See [comparison-note.md](comparison-note.md).

## The gate

    python check.py runs/03-the-wrong-file/report.md \
      --manifest runs/03-the-wrong-file/message-manifest.json

    PASS  7 quotations checked

Passed first time, unedited.

**One thing the gate did not catch, worth stating.** The report quotes the record in three
places using italics inside running prose rather than a block quote — the reasoning at message
6, and two phrases in its contributing factors. `check.py` verifies block quotes and does not
look inside prose, so those passages went unverified. They were checked by hand here and are
accurate. But the report schema's rule is that quote blocks are the only quoting device
precisely so that every quotation gets checked, and a report can currently follow the spirit of
that rule in italics and escape the machinery. That is a real hole in the gate rather than a
fault in this report, and it belongs in `OPEN-DEFECTS.md`.
