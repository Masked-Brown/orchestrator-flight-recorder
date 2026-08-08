# plan.md — Build Pipeline for orchestrator-flight-recorder

Five manifests, run in separate Claude Code windows, chained on handover files. One human
halt at M4 intake. The way this repo is built is itself an ICM demonstration.

**Delivery target.** `diagnostician/` is the deliverable: a self-contained markdown folder a
stranger drops into a Claude project so Claude becomes the investigator. Everything else
(enforcement, runs, build record) lives at root. Lesson inherited from #9: the drop-in folder
is unmistakable and self-contained; nothing inside it points outside it.

## Build philosophy: 20/80

The four seed files (this file, communitycompetitions.md, spec.md, brainwave.md) are authored
by hand and carry the decisions. Manifests read all four before acting. Freedom on
scaffolding; no freedom on scored substance (rules.md, the taxonomy, report schema). Where a
manifest touches substance, every decision goes in its handover with justification.

## The handover loop

Each manifest ends by writing `build/handover/MANIFEST-<N>-COMPLETE.md`:

```
# MANIFEST <N> — COMPLETE
status: complete | complete-with-questions
summary: <2-4 sentences>
files-created: <list, one-line purpose each>
files-changed: <list, what and why>
decisions-made: <numbered, each justified>
disagreements: <divergences from seed files, and why>
open-questions: <numbered, each needing a human or later manifest>
next-manifest-needs: <what M<N+1> reads first and assumes>
```

The next prompt polls for the prior handover file. Absent: wait and re-check. Present: read
it, then the seed files, then proceed. Flag disagreements; never silently override.

## The manifests

### M1 — Scaffold and parser

- **Goal.** Repo skeleton, investigator persona, and a working deterministic export parser.
- **Inputs.** Seed files. The real export, already unzipped in the repo folder (gitignored).
- **Tasks.**
  1. Verify `.gitignore` exists and covers the export before anything else. If absent, stop
     and write it first.
  2. Scaffold the layout in section 6.
  3. Inspect the real export's schema by script (never load raw JSON into context): top-level
     structure, message shape, whether assistant thinking content is present. Record the
     schema in the handover.
  4. `parse.py` — stdlib only. Input: export JSON path, plus conversation name and/or date
     window. Output: a numbered message manifest (index, role, timestamp, text; thinking
     content included where the export carries it, and its absence recorded when not).
     Deterministic: same input, same manifest.
  5. Draft `diagnostician/identity.md` (the investigator, per spec.md) and README skeleton.
- **Guardrails.** No rules substance. No invented schema; parse what is actually there.
- **Done when.** `parse.py` runs clean against the real export and produces a manifest for a
  named conversation; the skeleton shows the intended shape.

### M2 — Substance: rules, taxonomy, report schema

- **Goal.** The scored substance.
- **Inputs.** M1 handover, seed files.
- **Tasks.**
  - `diagnostician/rules.md` — how the investigator works: evidence standard for pinning a
    primary cause; the counterfactual (but-for) test; the undetermined fallback and when to
    take it; the acquittal discipline (verdict space includes not-the-orchestrator); the
    no-prescription invariant justified in-domain (cause reports and recommendations are
    different documents); anti-compression instruction (hold distinct factors distinct; rank,
    do not merge); reporter's hypothesis tested, never privileged.
  - `diagnostician/reference/failure-modes/` — the eight files from spec.md. Each: definition,
    transcript signature, distinguishing test. Written in plain English; a stranger who has
    never seen this build must be able to recognise the mode in their own transcript.
  - `diagnostician/reference/report-schema.md` — the seven sections, verbatim from spec.md,
    with a skeleton template.
  - `diagnostician/reference/verdict-classes.md` — the five classes with their standards of
    evidence.
- **Guardrails.** No examples yet (M5, from real runs). Plain English throughout; jargon was
  the #9 build's named stall.
- **Done when.** rules.md teaches diagnosis, never repair, and every rule is justified in the
  handover.

### M3 — Enforcement

- **Goal.** Make the invariant a property.
- **Inputs.** M2 handover, spec.md gate rules.
- **Tasks.**
  - `check.py` — the blocking gate, exit 1 on any spec.md gate rule. Reads a report plus the
    message manifest it claims to be about; the fabrication check matches every quoted
    passage verbatim against the manifest.
  - `tests/cases/` — clean reports that must pass.
  - `tests/negative/` — deliberately broken reports, each failing on a named check: a
    fabricated quote; two primary causes; a prescription smuggled into a contributing factor;
    a missing counterfactual; an unanchored factor; an invented failure mode. Verify the
    verifier: N/N known-bad rejected on the right check.
  - `tests/verify.py` — runs both directions, asserts the contract.
  - `.github/workflows/verify.yml` — CI on push.
- **Guardrails.** Architecture may copy #9's shape; code written fresh against this schema.
- **Done when.** verify.py passes: all clean cases clear, all negative cases fail on their
  named check.

### M4 — Real runs  ⛔ HUMAN HALT

- **Halt.** M4 begins by polling for `build/handover/M4-INTAKE.md`, written by the human. It
  contains: the chosen incidents (from the scout report), each with conversation name, date,
  message window, the incident statement as the reporter would give it, and the sensitivity
  ruling on excerpts. M4 does not start without it.
- **Goal.** Two REAL runs, shipped in full.
- **Planned incidents** (subject to intake confirmation):
  1. **Flagship — the M3 jargon stall** from the #9 build. Expected verdict: pilot-error or
     mixed; expected mode: vocabulary-mismatch. Independent answer key: the #9 journal, written
     before this entry existed. Ship the journal's relevant lines as `answer-key.md` and a
     comparison note.
  2. **The acquittal — the confident wrong explanation** from the #9 build. Expected verdict:
     mechanical (the model offered a wrong confident claim; checking the source caught it).
     Demonstrates the verdict space can acquit the orchestrator.
- **Tasks per run.** `parse.py` the window → `message-manifest.md`; run the diagnostician in a
  fresh chat with only the diagnostician folder, the manifest, and the incident statement;
  ship `report.md`; run `check.py` over it; write the five-column training table with REAL
  rows; sweep excerpts per the intake sensitivity ruling.
- **The training table** (per run, `runs/<incident>/training-table.md`): Input window and
  incident statement | Investigator reasoning (which lens fired, what it checked) | Finding
  as handed back | Training-layer impact (what was written to the orchestrator's profile) |
  Future-run benefit (how the next investigation of this orchestrator starts sharper).
  Accumulated profile: `training-layer/<orchestrator-id>.md`, populated from these runs, REAL.
- **Guardrails.** Fresh-chat runs, no answer key in view. Labels REAL only because the export
  is real. Raw export stays out of git; only swept excerpts ship.
- **Done when.** Both reports pass the gate, the comparison against the answer key is written
  honestly (including where the diagnostician missed), and the human has approved the
  excerpts.

### M5 — Ship

- **Inputs.** M4 handover, human approval.
- **Tasks.** `diagnostician/examples.md` regenerated from the real runs (never invented);
  README rewrite to final (the crystal-clear front door: what you give it, what you get back,
  the seven-section report, how to export your data, how to run parse.py, how to run it with
  no install at all); `JUDGE_GUIDE.md` (60-second no-install verify, then the full battery);
  `OPEN-DEFECTS.md` (honest holes: heuristic prescription detection, single-orchestrator
  evidence base, export schema drift risk, out-of-scope adjacent uses); README claims audit;
  `writeup.md` (build story, lineage from #9, the recursion); submission post draft (2-3
  sentences).
- **Done when.** A stranger cloning cold verifies the headline claims in six minutes.
  Repo flips public only after this manifest and the human's final read.

## The human gates

Two: the M4 intake halt (incidents chosen, sensitivity ruled), and the final read before
public. Everything else chains unattended.

## Target repo layout

```
orchestrator-flight-recorder/
  README.md
  diagnostician/                 # THE deliverable, self-contained
    identity.md
    rules.md
    examples.md                  # M5, from real runs
    reference/
      failure-modes/             # 8 files
      report-schema.md
      verdict-classes.md
    README.md                    # drop-in usage, no-code path
  parse.py
  check.py
  tests/ (cases/, negative/, verify.py)
  .github/workflows/verify.yml
  runs/
    <incident-id>/
      message-manifest.md
      incident-statement.md
      report.md
      answer-key.md              # flagship only
      training-table.md          # REAL rows
  training-layer/
    README.md
    <orchestrator-id>.md         # populated, REAL
  JUDGE_GUIDE.md
  OPEN-DEFECTS.md
  writeup.md
  build/ (seed files, handover/)
```

## Risk register (carry through every manifest)

- **Export in git.** The catastrophic one. .gitignore verified before first commit; M1 task 1;
  every manifest re-checks `git status` shows no export files before committing.
- **Empty memory.** training-layer ships populated from M4, REAL, or not at all.
- **Fabrication.** Quote-matching is check.py's job, never model diligence.
- **Blame machine.** The acquittal run is mandatory. A diagnostician with one verdict is not
  diagnosing.
- **Jargon.** Plain-English at every reporting point; the flagship incident IS this failure,
  and the entry must not commit it while diagnosing it.
- **Pitch outrunning repo.** M5 audit; OPEN-DEFECTS names every hole.
- **Schema drift.** parse.py built against the real export, schema recorded; drift named in
  OPEN-DEFECTS.
