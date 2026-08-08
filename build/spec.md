# spec.md — Locked Specification: orchestrator-flight-recorder

These anchors are locked. A manifest that diverges must log it under `disagreements:` in its
handover, never silently override.

## One-line purpose

You tell it what went wrong. You give it the session's export. It reads the black box and
tells you why, anchored to your own words, and stops.

## Domain (locked)

Diagnoses why an AI-orchestrated build session failed, tracing the failure to a specific
behaviour in the conversation, from the session's own Claude data export. One session, one
stated incident, one investigation. Not a security auditor, not a general chat reviewer, not
a prompt improver. Adjacent uses are named in OPEN-DEFECTS as out of scope.

## Identity (locked)

An air accident investigator reading the flight recorder. The export JSON is the black box:
the complete record of what was said, and, where the export includes it, what the model was
thinking. The investigator's professional discipline IS the competition's bar:

- Determines probable cause. Never redesigns the aircraft, never retrains the pilot.
  Recommendations are a different document written by different people; this report ends at
  cause.
- One probable cause, contributing factors ranked beneath it.
- Every claim anchored to the recorder. If it is not in the log, it is not in the report.
- Distinguishes pilot error from mechanical failure from environment. Acquittal is a
  legitimate finding.
- When the recorder is insufficient, the finding is "undetermined", stated plainly, with what
  additional evidence would resolve it. Real investigations end this way too.

## Intake (locked)

The user supplies:
1. **Incident statement.** One or two lines: what went wrong, or what they are unhappy with.
2. **The export.** The Claude data-export JSON (conversations file), plus the conversation
   name or date window if the export holds more than one conversation.
3. Optional: where they think it went wrong. Recorded as the reporter's hypothesis, tested
   like any other hypothesis, never privileged.

## Report schema (locked) — seven sections, in order

1. **Incident statement.** The failure restated in one line, fixing investigation scope.
2. **Failure surface.** The message(s) where the failure materialised. Verbatim quotes with
   message indices.
3. **Causal origin.** The message where the cause entered the conversation, quoted. May be the
   orchestrator's, the model's, or an absence ("no message in the window defines X; the model
   was forced to guess at msg 23"). Origin is rarely the surface.
4. **Propagation trace.** Turn-by-turn path from origin to surface: how the fault travelled,
   which messages compounded it, and the missed catch points where either party could have
   stopped it and did not.
5. **Verdict class.** One of: `pilot-error` (orchestrator), `mechanical` (model),
   `environment` (tooling, context limits, file state), `mixed` (primary still named),
   `undetermined`.
6. **Primary cause.** One sentence, citing exactly one named failure mode from
   reference/failure-modes/. Then contributing factors, ranked, each with its own anchor.
7. **Counterfactual test.** The but-for reasoning that separates cause from symptom: "had msg
   N specified X, the drift at msg M does not occur." Shows why the primary cause is upstream
   of every contributing factor.

The report ends at section 7. Nothing after the counterfactual.

## Failure-mode taxonomy (initial set, one file each in reference/failure-modes/)

Seeded from real observation in the #9 build journal. Each file: definition, transcript
signature (what it looks like in a log), distinguishing test (what separates it from its
neighbours), one anchored example once runs exist.

1. `ambiguous-instruction.md` — an instruction with multiple valid bindings; the model bound
   silently instead of asking.
2. `missing-context.md` — a decision the model needed was never in the window.
3. `stale-constraint.md` — a constraint set for an old environment inherited without
   re-deciding after the environment changed.
4. `vocabulary-mismatch.md` — output in a register the reader cannot evaluate; the report
   about the system requires the system's own jargon.
5. `thread-overload.md` — individually correct turns collectively opening more threads than
   they close; overload at sequence level, not message level.
6. `premature-parallelism.md` — generation outrunning landing; loops opened before any one
   loop is closed.
7. `scope-injection.md` — one party enlarging or shrinking scope without the decision being
   surfaced as a decision.
8. `unverified-claim-accepted.md` — a confident explanation accepted without checking the
   source; the check would have been cheap.

The taxonomy is extensible; runs may add modes. A run may never invent a mode inline without
adding its file.

## Gate rules (check.py blocks, exit 1)

- More than one primary cause, or zero.
- Any quoted passage not verbatim in the parsed message manifest (fabrication check).
- Verdict class outside the enum.
- Prescription patterns: rewritten prompts, "instead you should", "next time", "try", fix
  lists, improved versions of the orchestrator's messages.
- Any contributing factor with no message anchor.
- Missing counterfactual section, or a report that continues past it.
- A named failure mode with no corresponding file in reference/failure-modes/.

## Evidence labelling (locked)

`REAL` — from a genuine export of a genuine session, excerpts swept before shipping.
`CONSTRUCTED` — author-built to demonstrate a mechanism, labelled everywhere it appears.
`ILLUSTRATIVE` — schema demonstrations only, exactly one per table, marked.
A CONSTRUCTED row labelled REAL is the pitch-outrunning-the-repo miss. This build ships REAL.

## Privacy (locked)

The raw export never enters version control. `.gitignore` covers it from the first commit.
Shipped excerpts in runs/ are windowed to the diagnosed incident and swept for names,
credentials, client detail. The sweep is a named M4 gate task, decided by the human.
