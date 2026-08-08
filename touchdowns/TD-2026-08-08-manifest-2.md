# Touchdown: manifest-2

date: 2026-08-08

window: Manifest 2 of the orchestrator-flight-recorder build (Substance: rules, taxonomy,
report schema)

prompt-received:

```
You are Manifest 2 of the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

Poll for build/handover/MANIFEST-1-COMPLETE.md. If absent, wait 60 seconds and check again;
loop until present. When present, read it first, then the four seed files in build/
(communitycompetitions.md, spec.md, plan.md, brainwave.md).

Execute Manifest M2 exactly as specified in build/plan.md (Substance: rules, taxonomy,
report schema). Plain English throughout; the reader must be able to evaluate the system
without the system's vocabulary.

List every rule you author with its justification in your handover. Flag disagreements with
the seed files; never silently override.

Finish by writing build/handover/MANIFEST-2-COMPLETE.md. Commit and push (verify git status
shows no export files first).
```

what-happened: Polled for the M1 handover — it was absent at session start, so a background
watcher was armed and the session picked up the moment the file landed. Read the handover, then
all four seed files, then M1's actual output (identity.md, the two READMEs, and parse.py in
full) so the substance could be written against the artifact that exists rather than the one the
plan describes. Wrote the scored substance: rules.md, the eight failure-mode files,
report-schema.md and verdict-classes.md. Answered M1's open question 3 (the investigator may
quote the model's private reasoning, with channel attribution, no speech verbs, and a hard rule
that nobody can be faulted for missing a sign only the model could see) and resolved the fork
question M1 flagged in its decision 5. Pinned down what a "quoted passage" actually is so M3's
fabrication gate has something deterministic to match. Updated the three M1 files whose promises
had gone out of date, verified the deliverable folder is self-contained and all internal links
resolve. At the safety check before committing, `build/handover/M4-INTAKE.md` turned up — the
human had written it while the session was running. Read it, added the one rule it asks the
diagnostician's rules to carry, and rewrote the handover's open questions around what it
closes and what it introduces, including an off-by-one hazard in it that would corrupt the
flagship run. Then committed.

files-touched:

- created diagnostician/rules.md — the method, fourteen sections
- created diagnostician/reference/report-schema.md — seven sections, citation format, template
- created diagnostician/reference/verdict-classes.md — five verdicts and their evidence standards
- created diagnostician/reference/failure-modes/ambiguous-instruction.md
- created diagnostician/reference/failure-modes/missing-context.md
- created diagnostician/reference/failure-modes/stale-constraint.md
- created diagnostician/reference/failure-modes/vocabulary-mismatch.md
- created diagnostician/reference/failure-modes/thread-overload.md
- created diagnostician/reference/failure-modes/premature-parallelism.md
- created diagnostician/reference/failure-modes/scope-injection.md
- created diagnostician/reference/failure-modes/unverified-claim-accepted.md
- created build/handover/MANIFEST-2-COMPLETE.md
- created touchdowns/TD-2026-08-08-manifest-2.md (this file)
- changed diagnostician/reference/failure-modes/README.md — real index replacing the planned
  set, plus a narrowing-down guide and the rule for adding a mode later
- changed diagnostician/README.md — under-construction note now matches reality, citation
  paragraph added, file table corrected
- changed diagnostician/identity.md — one line: its closing pointer double-attributed the
  report's shape to both rules.md and reference/

decisions: the full list with justifications is in the handover (58 numbered rules). The ones
that shaped everything else:

- Read parse.py in full before writing any rule. The rules had to speak the manifest's own
  vocabulary, and guessing at the channel labels would have produced a rulebook that does not
  match the evidence it governs.
- Quoting is restricted to block quotes, and quotation marks may never be used to quote the
  record. spec.md requires every quoted passage be verbatim but never defines what makes
  something a quoted passage, and the gate cannot be built until that is answered. The
  alternative (check every double-quoted run) would reject honest reports that put quote marks
  around a verdict name.
- Nobody could see the reasoning channel except the model, so a missed catch point may never
  rest on it. This is the half of the reasoning-quotation answer that does real work, and it is
  correct in-domain — the cockpit voice recorder is not available outside the cockpit.
- Each failure-mode file gained a fourth section spec.md does not ask for: what would rule it
  out. A mode nothing can falsify absorbs every case offered to it, and a taxonomy containing
  one has stopped distinguishing anything.
- Did not touch parse.py despite finding a real limitation (forks are flagged but the parent
  ids are not exposed, so an investigator cannot tell which branch was live). M2's remit is
  substance; the rules handle it honestly and the improvement is flagged for M3, which is the
  next manifest that touches code.
- Acted on one item from M4-INTAKE.md even though that file is addressed to M4, because it asks
  that "the diagnostician's rules should name" a specific false positive — and the rules are
  M2's file. Generalised it from the one phrase the scout tripped on to the class of material
  it belongs to (standing preferences, pasted briefs, carried handovers), since the phrase is
  one person's preference and the failure is general. Leaving a known-needed rule out so a
  later manifest could patch it would have been worse.
- Did not write the ninth failure mode the intake proposes. It is conditional on what run 2
  actually shows, and writing a mode with no case behind it is precisely what the extension
  rule in failure-modes/README.md exists to prevent. Recorded the forward view instead: on M2's
  reading it does look like a genuine gap, and M4 should expect to write it after the run.
- Did not modify M4-INTAKE.md. It is the human's file. Committed it as found.

friction:

- The M1 handover was not present at session start, so the first several minutes were spent
  waiting on a poll rather than working. Reading the seed files during the wait was avoidable
  but was skipped deliberately, since the prompt specifies the handover is read first and the
  ordering exists so M1's decisions frame the seeds rather than the other way round. Cost: a
  few idle minutes. Cheap, and the right call.
- identity.md's closing pointer promised the report's shape in rules.md and the report format
  in reference/ — the same thing attributed to two places. Small, but M1 explicitly asked that
  the promise be kept accurate, and it could not be kept accurate without changing it. Fixed
  with a one-line edit rather than left to drift.
- spec.md's prescription-pattern list includes the bare token "try", which matched literally
  would fire on ordinary investigative prose ("the model tried to open the file"). Not a
  blocker for M2 but it would have made M3 build a gate that rejects clean reports. Logged as a
  caution in the disagreements section rather than silently reinterpreted.
- The M4 intake arriving mid-session meant the handover had to be partly rewritten after it was
  finished: two open questions were already answered by a file that did not exist when they were
  written. No work was wasted, but it is a reminder that a handover written before the final
  `git status` can be stale by the time it is committed. Checking the working directory again
  before writing the handover, not just before committing, would have caught it earlier.
- The intake specifies message windows as zero-based array indices while parse.py numbers from
  1. Nobody has reconciled this yet. For the flagship run the difference pulls the withheld
  answer key into the input window, which would quietly invalidate the strongest piece of
  evidence in the entry. Flagged hard in the handover; it is M3's to fix and it is the kind of
  thing that is very cheap now and very expensive after a run.
- Nothing errored. No tooling friction, no failed commands.

state-left: The deliverable folder is complete apart from worked examples. `diagnostician/`
holds identity.md, rules.md, README.md, and reference/ with report-schema.md,
verdict-classes.md and eight failure-mode files — 1,359 lines of substance. It is
self-contained: nothing inside it points outward except one sentence in its README explaining
where a message manifest comes from, and every internal cross-reference was verified to
resolve. `examples.md` does not exist and both READMEs now say so plainly, which is honest
rather than a gap — it is filled from the real runs at M5.

M3 is unblocked and has more to work with than plan.md anticipated: the handover carries a
table mapping each of spec.md's seven gate rules onto a specific syntactic check, plus two
extra checks worth adding and two negative test cases beyond the six spec.md implies. Four open
questions are logged, all M3's: quote normalisation, how hard to enforce the anchor format, not
weakening the fork rule once the parser improves, and prescription-detection edges.

The human gate at M4 has already been passed — `build/handover/M4-INTAKE.md` is written and
approved-to-run, which M2 did not expect to see. It names three incidents rather than plan.md's
two, each with an answer key held back from the diagnostician, and it settles M1's worry that
the flagship was not in this export. M3 should read it: it constrains what the gate has to
handle, it lists standing corrections for the parser (several of which M1 has already
satisfied — check before rewriting), and it carries the zero-based indexing hazard above.
