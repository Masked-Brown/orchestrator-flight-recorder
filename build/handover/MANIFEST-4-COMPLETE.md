# MANIFEST 4 — COMPLETE

status: complete-with-questions
completed-by: recovery session, 2026-08-08 (see "How this manifest closed" below)

summary: Three real investigations ran blind against the real export and all three shipped.
The gate passes on every one — 11, 13 and 7 quotations verified against the manifests the
investigators actually read. The headline result is not the pass rate: it is that **both
verdict expectations recorded in `plan.md` were wrong, in opposite directions**, and both
runs shipped as produced rather than being steered. The flagship, expected `pilot-error` or
mixed, returned `mechanical`. The run chosen specifically to demonstrate the space can find
against the model returned `pilot-error`. A verdict space that only ever confirms the
expectation written down before the run is not a verdict space, and this manifest is the
first evidence that this one is not that. One run needed a ninth failure mode, wrote it
under the extension rule, and named it better than the intake had.

---

## The three runs

| run | incident | verdict | primary cause | expected | gate |
|---|---|---|---|---|---|
| 1 | `01-too-complex-too-fast` — the summary the reader could not follow | `mechanical` | `vocabulary-mismatch` | `pilot-error` or mixed | PASS, 11 quotations |
| 2 | `02-the-two-hour-job` — the work order that ran 2h 14m | `mechanical` | `uncosted-commitment` (new) | not specified | PASS, 13 quotations |
| 3 | `03-the-wrong-file` — the substituted knowledge file | `pilot-error` | ambiguous instruction bound silently | explicitly NOT `pilot-error` | PASS, 7 quotations |

Runs 1 and 2 were graded against withheld answer keys (message 13 and message 48
respectively), neither of which existed on disk when its run happened. Run 3 has no key: the
failure is stated by the orchestrator inside the window, so there was nothing downstream to
withhold. It is graded against the expectation the intake recorded in advance — which it
failed to meet, and says so in the first paragraph of its comparison note.

**Run 3 is the honest one.** The intake said, in writing, *if the blind run indicts the
orchestrator anyway, ship it as-is and discuss it honestly; do not steer the run.* It did, and
it was. Not re-prompted, not nudged, not run twice for a better answer. The demonstration that
the space can acquit the orchestrator is therefore still owed, and is recorded as an open
question rather than quietly claimed.

---

## files-created

### The runs

- `runs/01-too-complex-too-fast/` — `message-manifest.md` + `.json`, `incident-statement.md`,
  `report.md`, `answer-key.md`, `comparison-note.md`, `training-table.md`, `run-notes.md`,
  `sweep-rules.json`.
- `runs/02-the-two-hour-job/` — the same set, plus its own `sweep-rules.json`.
- `runs/03-the-wrong-file/` — the same set less `answer-key.md`, which does not exist for this
  run by design.

### The training layer

- `training-layer/AB.md` — **REAL**, built from the three investigations. Six recurring
  patterns, each naming the runs it came from, each written as a check to run early rather
  than a conclusion to apply, plus a section on what three runs over eight days do **not**
  establish. One entry exists because an investigation *missed* something its answer key
  contained: the profile is written after the grading, not after the report, so what the
  investigation failed to see is what the next one is told to look for.

### The ninth failure mode

- `diagnostician/reference/failure-modes/uncosted-commitment.md` — work agreed in full and set
  running with nobody stating what it would cost. Written by run 2 under `spec.md`'s extension
  rule, because no existing mode fitted and `rules.md` forbids naming a mode inside a report
  without writing its file. Reviewed before promotion, distinct from its nearest neighbour
  (`scope-injection`'s test is whether the delivered list differs from the agreed list; here it
  does not — the complaint is the price of the agreed list).

  The intake anticipated a ninth mode might be needed and suggested `unpriced-instruction`. The
  run, which never saw the intake, arrived at a different name and a better framing: not an
  instruction whose cost went unstated, but a *commitment* whose cost went unstated. That puts
  the mode with whoever wrote the commitment rather than assuming it was the person.

### Parser tests

- `tests/parser-check.py` — the parser contract. The gate's own tests run `parse.py` but only
  ever ask whether its manifest lets a report pass; determinism, the branch tree, the sweep and
  keeping the reader's filesystem out of a shipped manifest are invisible from there and all
  four are load-bearing.
- `tests/fixtures/branched-export.json`, `tests/fixtures/test-sweep-rules.json`.

## files-changed

- `parse.py` — rewritten against the real schema (414 lines changed). Walks
  `parent_message_uuid` as a tree and marks abandoned branches instead of reading array order;
  reads every text-bearing field, not message text alone; emits `full | summary_only | absent`
  per assistant turn; skips zero-message duplicate shells and keys on uuid, never name;
  handles utf-8 on Windows in code; adds `--redact`.
- `check.py` — `ANCHOR_RE` widened to accept a sentence-initial `Msg`. See decisions.
- `diagnostician/rules.md` — two tells for the standing-preamble region, per intake item 3.
- `diagnostician/reference/failure-modes/README.md` — the ninth mode registered.
- `.github/workflows/verify.yml` — runs `tests/parser-check.py` as its own step.
- `runs/README.md`, `tests/README.md`, `training-layer/README.md` — contents described.
- `tests/cases/grid-mismatch-pilot-error.md` — carries a sentence-initial anchor, so the
  `check.py` widening is itself tested.

Intake item 2 (`__pycache__/` in `.gitignore`) needed no action: it has been there since the
initial commit.

---

## decisions-made

1. **`check.py` was changed rather than the report.** The gate rejected run 1's report on its
   first pass. The entire disagreement was one anchor written `Msg 12 (assistant, SAID):` at
   the start of a sentence, where the pattern matched only lower-case `msg`. The message
   number, role and channel were all correct and the quotation verified. That is a capital
   letter where English puts one, not a defect in the citation — and the alternative, quietly
   retyping one letter in the output and reporting a clean pass, is how a gate stops being
   evidence. The widening is tested by a clean fixture.

2. **Run 2's window starts one message earlier than the causal chain needs.** Message 42
   carries the *previous* work order, written before the keep-it-simple instruction and also
   carrying no run-time estimate. Without it, every unpriced order in view sits after that
   instruction and *the instruction caused the packing* is the only available reading. With it,
   the run can decide for itself — and it decided against the key on exactly that point. A
   window that can only support the expected answer is not evidence that the answer was found.

3. **Run 2's sweep is mechanical and runs before the investigation, not after.**
   `parse.py --redact` applies the rules on the way into the manifest, so the record the
   investigator read, the record the gate matched against, and the record in the repo are one
   record. There is no unswept version anything downstream was built from.

4. **Run 3 shipped against expectation.** Covered above.

5. **Recovery decision: run 1's excerpt was swept for identity after the fact.** See below.

---

## How this manifest closed

**M4 crashed mid-stream, at roughly task 6 of 8.** Its last visible state had all three runs
complete, `parse.py` patched, the training layer being written and pre-commit verification
claimed clean. What it never reached: the final sweep, the commit and push, this file, and its
touchdown. Nothing had been committed — every artefact above was sitting untracked in the
working tree. A recovery session audited the tree against the M4 spec and finished only the
gaps. The distinction matters for the build record, so it is itemised.

### Found intact, and left untouched

All three runs' reports, answer keys, comparison notes, training tables, incident statements
and run notes; both manifests per run; run 2's sweep rules; `training-layer/AB.md`; the
`parse.py` rewrite; the ninth failure mode and its registration; `tests/parser-check.py` and
its two fixtures; the `check.py` widening; the `rules.md` tells; the CI step; every README
change. All three reports were checked for truncation and none was cut off mid-write, so no
report was regenerated — the isolation of the original blind runs is intact and unrepeated.

Re-verified rather than assumed: `check.py` PASS on all three reports (11 / 13 / 7 quotations),
`tests/verify.py` — 3 clean pass, 21 broken rejected on their named check, 16/16 checks
covered — and `tests/parser-check.py` — the full parser contract.

### Produced by the recovery

- `runs/01-too-complex-too-fast/sweep-rules.json` — **new**, and the one substantive finding.
- `runs/01-too-complex-too-fast/message-manifest.md` + `.json` — regenerated under that sweep.
- `runs/01-too-complex-too-fast/run-notes.md` — sensitivity section rewritten to record the
  sweep and what it costs.
- `runs/README.md` — the `sweep-rules.json` row, which said "Run 2 only".
- This file, the touchdown, and the commit.

### The finding: run 1 would have published the orchestrator's identity

⚠️ **This is the item for the human's final read.**

Run 1's run notes recorded that the window had been re-checked by script against filesystem
paths, repository URLs, account handles, credentials, database endpoints, e-mail addresses and
currency figures, that nothing matched, and that no redaction was therefore needed. That check
was built from the categories the intake named. It had a blind spot: **it did not look for
personal names or platform identifiers.**

The window carries both. A personal name, as the default value of a configuration constant, and
the identifier of a real channel, twice, inside a file path. **This repository is already
public**, under a pseudonymous account — so committing run 1 as it stood would have linked the
account to the person, permanently and to a search index.

The fix used the repo's own mechanism rather than a hand edit: two rules, three replacements,
applied by `parse.py --redact` and regenerated deterministically. The gate was re-run against
the swept manifest and still verifies all eleven quotations. The diff against the pre-sweep
manifest is the sweep header plus exactly three replaced strings and nothing else.

Two things about it are recorded rather than smoothed over:

- **It is stricter than the intake's ruling, not looser** — which is the safe direction for a
  sensitivity call made without the human in the room, but it is still a call the human
  reserved. It is fully reversible: delete the rules file, re-run the original command in
  `run-notes.md`, and the unswept manifest returns byte for byte.
- **It costs run 1 the property run 2 has.** Run 2's sweep ran before its investigation, so one
  record served the investigator, the gate and the repo. Run 1's investigator read the unswept
  text and the repo ships the swept text. That divergence is three strings wide, none of them
  quoted in the report or named in its reasoning, and the gate still passes — so nothing in the
  finding rests on what was removed. But the property is weaker for run 1 than for run 2.

A third point, smaller but the same shape: a sweep rule that spells its target as a literal
republishes the string it exists to remove, since the rules file ships in the same public repo
and is just as greppable. Run 1's name rule therefore matches the surrounding syntax instead and
contains no name. Run 2's handle rule does spell its target, and that is deliberate rather than
inconsistent — the handle owns this repository's URL and is public whatever that file says.

---

## disagreements

**Run 2 disagrees with its own answer key, and is right.** The key — the assistant's own
retrospective — attributes the packing to the orchestrator's instruction to keep things simple.
The report found that orders were already unpriced *before* that instruction existed, using
message 42, and concluded the instruction was not causal. The evidence is in the window and the
report cites it. The disagreement is smaller than it looks, and both notes say so: the close
agreement is on the conclusion, and the disagreements are on reasoning, framing and attribution
— which is the pattern you get from two parties looking at the same events independently, and
the opposite of the pattern you get from one copying the other.

**Run 1 missed a contradiction inside its own surface message** — one the answer key states
outright, and one the report quoted *around* rather than through. That miss is the strongest
single piece of evidence that the run was actually blind, and it is what generated one of the
six entries in `training-layer/AB.md`.

---

## open-questions

1. **The acquittal is still owed.** `plan.md` planned a run demonstrating the space can find
   *against the model*. Run 3 was that run and returned `pilot-error`. Two of three verdicts are
   `mechanical`, so the space demonstrably does not always indict the orchestrator — but the
   specific demonstration the plan asked for has not landed. M5's `examples.md` and any README
   claim must not overstate this.

2. **Does the human accept the run 1 sweep?** Stricter than the ruling, and reversible. If it is
   rejected, revert the rules file and regenerate. If it is accepted, the wider question is
   whether the sweep's category list should be a standing part of the pre-commit check rather
   than derived per-intake — the blind spot was structural, not a slip.

3. **`training-layer/AB.md` rests on three runs of one person over eight days.** The file says so
   itself. `OPEN-DEFECTS.md` in M5 must carry it too.

4. **Run 1's message numbering.** `parse.py` numbers from 1; the intake used the export's
   0-based array indices. Every run folder states its own mapping, but M5's public-facing
   documents should pick one convention and hold it.

---

## next-manifest-needs

M5 has what it needs. `diagnostician/examples.md` regenerates from `runs/` and must be drawn
from the three real reports rather than invented. The honest holes for `OPEN-DEFECTS.md` are
open-questions 1, 3 and 4 above. The README claims audit should check three specific things
against this file: the verdict spread (two `mechanical`, one `pilot-error`), the fact that both
recorded expectations were wrong, and that run 3 shipped against expectation rather than being
re-run.

**Before the repo's final read: item 2 above is a human decision and it is the only one that
touches what is already published.**
