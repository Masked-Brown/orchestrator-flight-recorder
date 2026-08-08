# Runs

Three real investigations, shipped whole. Run in build stage M4 on 2026-08-08.

Each folder holds the incident statement as it was actually given, the message manifest the
investigator worked from, the report it produced, the result of putting that report through
`check.py`, and an honest grading of the finding against something the run could not see.

| Run | The complaint | Verdict | Failure mode | Gate |
|---|---|---|---|---|
| [01](01-too-complex-too-fast/) | too complex, too fast | `mechanical` | `vocabulary-mismatch` | PASS, 11 quotations |
| [02](02-the-two-hour-job/) | the two-hour job | `mechanical` | `uncosted-commitment` | PASS, 13 quotations |
| [03](03-the-wrong-file/) | the wrong file | `pilot-error` | `ambiguous-instruction` | PASS, 7 quotations |

Three incidents, three mechanisms, two verdict classes, none of them chosen in advance. Run 3
was the run designated to produce a verdict other than `pilot-error` and it produced
`pilot-error` anyway; the acquittal arrived in run 1, which nobody had designed for one. Both
outcomes are discussed in the runs' comparison notes rather than tidied away.

## What is in each folder

| File | What it is |
|---|---|
| `incident-statement.md` | The complaint, as the person brought it. One or two lines, not a specification. |
| `message-manifest.md` | The record the investigator read, produced by `parse.py` from the real export. |
| `message-manifest.json` | The same record, machine-readable. This is what `check.py` matches quotations against. |
| `report.md` | What the investigation produced. Unedited. |
| `run-notes.md` | How the window was chosen, how the excerpt was swept, how the run was isolated, and what the gate said. |
| `answer-key.md` | Runs 1 and 2: the withheld message, written into the repo only after the report was finished and gated. |
| `comparison-note.md` | The grading, both directions — where the report was right, where it missed, where it went past the key. |
| `training-table.md` | The five-column row: window and complaint, reasoning, finding, what went to the profile, what the next investigation gains. |
| `sweep-rules.json` | Runs 1 and 2: the redaction rules applied to that run's excerpts, with what each rule replaced recorded in the manifest header. |

## The rules these runs were held to

**They are real.** A genuine export of genuine working sessions, not scenarios written to make
the tool look good. Every row is labelled `REAL`. Anything constructed to demonstrate a mechanism
is labelled `CONSTRUCTED` wherever it appears, and none of it is in this folder.

**They were blind.** Each investigation ran in a fresh context whose entire world was a copy of
`diagnostician/`, that run's manifest, and its incident statement. No answer key, no build plan,
no handover, no seed file, and no knowledge of what the incident was expected to show. For runs 1
and 2 the answer key did not exist on disk anywhere at the time the run happened — it was written
afterwards. Each `run-notes.md` records the protocol and states plainly what the isolation does
*not* guarantee.

**The reports were not edited.** Not for the gate, not for style, not to improve a finding. Run 1
failed `check.py` on its first pass over one anchor written `Msg` at the start of a sentence where
the gate matched only `msg`; the gate was changed to accept both and the report was left alone.
That is recorded in run 1's notes, because quietly retyping one letter and reporting a clean pass
is how a gate stops being evidence.

**The excerpts are windowed and swept.** Only the stretch relevant to the incident ships. Run 2's
window was not pre-cleared, so its excerpts were swept by rule rather than by reading —
`parse.py --redact` applies the rules on the way *into* the manifest, so the record the
investigator read, the record the gate checked, and the record in this folder are the same swept
record. The replacement counts are printed in that manifest's own header, including the rule that
matched nothing. The raw export never enters version control.

**The comparisons are honest in both directions.** A perfect score would be a reason to suspect
the run rather than to celebrate it. Run 1 missed a contradiction sitting in its own window that
the answer key states outright, and its comparison note says so at length — that miss is the best
evidence in this folder that the run was genuinely blind, because it is the sort of thing a
contaminated run could not have got wrong.

## Reproducing the gate

The manifests ship, so a stranger with no export can re-run every check in this folder:

    python check.py runs/01-too-complex-too-fast/report.md --manifest runs/01-too-complex-too-fast/message-manifest.json
    python check.py runs/02-the-two-hour-job/report.md    --manifest runs/02-the-two-hour-job/message-manifest.json
    python check.py runs/03-the-wrong-file/report.md      --manifest runs/03-the-wrong-file/message-manifest.json

Exit 0 on all three. The manifests themselves cannot be reproduced without the raw export, which
is gitignored and stays that way; each `run-notes.md` records the exact command that produced its
manifest and the export's fingerprint, so the person holding the export can rebuild them byte for
byte.
