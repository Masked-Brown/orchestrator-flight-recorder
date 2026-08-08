# Touchdown: manifest-4-recovery

date: 2026-08-08
window: Manifest 4, recovery session (M4 crashed mid-stream at roughly task 6 of 8)

prompt-received:
```
You are the M4 recovery session for the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

CONTEXT
Manifest 4 (three real diagnostic runs) crashed mid-stream at roughly task 6 of 8. Its
last visible state: all three runs completed, parse.py patched, training-layer being
written, pre-commit verification claimed clean. What it did NOT visibly finish: the final
sweep, git commit and push, build/handover/MANIFEST-4-COMPLETE.md, and its touchdown.
Nothing is confirmed committed. Your job: establish the true state, finish ONLY what is
missing, and close M4 out. Do not redo work that exists and passes.

READ FIRST
build/handover/M4-INTAKE.md, then build/plan.md (Manifest M4 section), then
build/handover/MANIFEST-3-COMPLETE.md.

STEP 1 — AUDIT, read-only, report before acting
- git status and git log --oneline -5: what is committed vs untracked/modified.
- Inventory against the M4 spec: for each of the three runs (runs/<incident>/), does it
  contain message-manifest.md, incident-statement.md, report.md, answer-key.md (runs 1-2),
  training-table.md with REAL rows, and a comparison note? Does
  training-layer/<orchestrator-id>.md exist with content? Is parse.py patched (tree walk,
  all-fields, reasoning flag)? Is __pycache__/ in .gitignore?
- Run check.py over each of the three reports. Run tests/verify.py.
- Print a short table: item, present/absent, passes/fails.

STEP 2 — COMPLETE, only the gaps
- Anything absent or failing from the M4 spec: finish it, following M4-INTAKE.md exactly
  (sensitivity sweeps included). Anything present and passing: leave untouched.
- If a report was cut off mid-write (check for truncated files), that run's report is
  suspect: state so, and regenerate ONLY that report via a fresh blind run per the intake's
  isolation rules.

STEP 3 — VERIFY AND CLOSE
- The full pre-commit verification: sensitivity sweep on all shipped excerpts, check.py on
  all three reports, tests/verify.py, then git status confirming no raw export files, no
  scout material, no __pycache__.
- Commit and push everything.
- Write build/handover/MANIFEST-4-COMPLETE.md per plan.md's format. Include a note that M4
  crashed and was completed by a recovery session, and list which items the recovery
  actually produced vs found intact: the difference matters for the build record.
- End with the plain-English summary of the three verdicts for the human review gate, and
  write a touchdown covering this recovery session, with the crash in the friction field.
```

what-happened: Audited the tree against the M4 spec and found the crashed session had
actually finished almost everything — all three runs complete with every required artefact,
parse.py rewritten, the ninth failure mode written and registered, the training layer
populated, parser tests added, CI updated. Nothing was committed; it was all sitting
untracked. Re-ran every verifier rather than trusting the crashed session's claim: check.py
PASS on all three reports, tests/verify.py and tests/parser-check.py both holding. No report
was truncated, so no blind run was repeated. The one real gap was the final sweep, and it
found something: run 1's shipped manifest carried the orchestrator's real name and a real
channel identifier, on a repository that is *already public* under a pseudonym. Wrote a
sweep-rules file for run 1, regenerated its manifests through parse.py --redact, confirmed
the gate still verifies all eleven quotations, then wrote the handover and committed.

files-touched:
- created runs/01-too-complex-too-fast/sweep-rules.json — two rules, three replacements
- changed runs/01-too-complex-too-fast/message-manifest.md + .json — regenerated under the sweep
- changed runs/01-too-complex-too-fast/run-notes.md — sensitivity section rewritten honestly
- changed runs/README.md — the sweep-rules row said "Run 2 only"
- created build/handover/MANIFEST-4-COMPLETE.md
- created touchdowns/TD-2026-08-08-manifest-4-recovery.md
- everything else the crashed session left: committed unchanged

decisions:
- Did not regenerate any report. All three were complete and passed the gate; re-running a
  blind investigation that already succeeded would have destroyed its isolation for nothing.
- Swept run 1 for identity even though the intake had cleared that window. The intake named
  only database identifiers and revenue figures as run 1's hazards and placed both outside the
  window; it did not anticipate a personal name or a channel ID inside it. Stricter than the
  ruling is the safe direction for a sensitivity call made without the human present, and the
  repo being public already made the alternative irreversible.
- Used parse.py --redact rather than hand-editing the manifest, so the change is deterministic,
  counted in the manifest header, and reversible by deleting one file.
- Wrote run 1's name rule to match surrounding syntax rather than the name itself, after
  noticing the first draft of the rules file republished the exact string it redacts. Left run
  2's handle rule spelling its target: that handle owns the repository URL and is public
  regardless.
- Recorded in run-notes.md that run 1's sweep ran *after* its investigation, so it lacks the
  one-record property run 2 has. Disclosing the weaker property beats letting the two runs look
  equivalent.

friction:
- **The crash itself.** M4 died at roughly task 6 of 8 with everything uncommitted. Cost was
  low only because the work survived in the working tree — an untracked tree is one `git clean`
  from total loss, and the session had produced three blind investigations that cannot be
  cheaply reproduced. The lesson for future manifests: commit after the expensive irreversible
  step (the blind runs), not at the end.
- **The crashed session's "verification clean" claim was not reliable.** It was broadly true —
  every gate did pass — but its sweep had a category blind spot that would have published the
  orchestrator's identity. Re-running verification rather than trusting the claim is what caught
  it. A handover that says "verified clean" should say *against what patterns*.
- **check.py needs `--manifest` and says so, but exits 0 when invoked without it.** The first
  audit pass looked like three clean passes when it had actually run nothing. Caught it on the
  output text, not the exit code. That is a gate that can report success without checking
  anything, and it belongs in M5's OPEN-DEFECTS.
- Repo-wide greps hit the 33MB gitignored conversations.json and blew up the output. Scoping
  every sweep to `git ls-files -co --exclude-standard` fixed it and is the correct scope anyway:
  it sweeps exactly what git would commit.

state-left: M4 closed and pushed. All three runs shipped and passing the gate; both test suites
green; the sweep clean over everything git would commit. `build/handover/MANIFEST-4-COMPLETE.md`
carries the full record including the produced-vs-intact split. **One item waits on the human:**
the run 1 identity sweep is stricter than the intake's ruling and is flagged as open-question 2
in the handover — accept it or revert it. The other standing item is that the acquittal run the
plan asked for did not land: run 3 was chosen to find against the model and returned
`pilot-error`, shipped as produced. M5 must not overstate that in the README. Next stop is the
M5 ship manifest, which needs the human's final read before the repo's claims go out.
