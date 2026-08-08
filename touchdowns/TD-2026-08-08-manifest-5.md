# Touchdown: manifest-5

date: 2026-08-08
window: Manifest 5 (the ship layer)

prompt-received:
```
You are Manifest 5 of the orchestrator-flight-recorder build, the ship layer.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

Poll for build/handover/MANIFEST-4-COMPLETE.md. Read it, then the four seed files, then the
three run folders in full.

Execute Manifest M5 per build/plan.md, with these corrections:

1. diagnostician/examples.md: generated from the three real runs only. Never invent.

2. README.md rewrite, and this is the front door so get it exactly right, in plain English:
   - What this is, in three sentences: you tell it what went wrong, you give it your Claude
     export, it reads the black box and tells you why, quoting your own conversation back
     at you, and stops. It never rewrites your prompts or hands you fixes.
   - What you get back: the seven-section report, each section named in one plain line.
   - How to use it, two paths: (a) no-code: drop the diagnostician folder into a Claude
     project, paste your incident statement, attach your export or the relevant
     conversation; (b) full: run parse.py to window the export, run the diagnostician on
     the manifest, run check.py over the report.
   - How to get your export: Claude Settings, Privacy, Export data, with one line on what
     arrives and that exports cover recent history in batches.
   - The three shipped runs, one line each, with links.
   - Honesty note: verdicts can find against you, against the model, against the
     environment, or come back undetermined. All are real outcomes.

3. writeup.md: the build story. IMPORTANT CORRECTION: earlier planning claimed the flagship
   run would be the session that built the previous competition entry. That is not true;
   the export batch did not contain those sessions. The actual story is stronger stated
   honestly: three live incidents from the builder's own working week, run blind, two with
   in-conversation answer keys written by the participants before this tool existed. Also
   tell the recursion that IS true: the build of this tool was itself orchestrated, its
   touchdown and handover files are in build/, and any failure in this build is a future
   test case. Cut any claim anywhere in the repo that a fresh clone cannot verify.

4. JUDGE_GUIDE.md: 60-second no-install path first (read run 1's report next to its answer
   key), then the full battery (verify.py, the negative fixtures, re-running a blind run).

5. OPEN-DEFECTS.md, honest, at minimum: prescription detection is heuristic; the evidence
   base is one orchestrator's week and generalisation is unproven; export schema may drift;
   thinking is partially observable (37% summary-only in this batch) which bounds reasoning
   claims; corrections delivered as prompt-edits destroy their own failure signal (the
   branch problem), which a transcript diagnostician inherits; adjacent uses (security
   audit, general chat review) are out of scope.

6. Submission post draft: 2-3 sentences, what it diagnoses and who it is for, plus the
   repo link placeholder.

git status check (no export, no scout material), commit, push, write
build/handover/MANIFEST-5-COMPLETE.md and your touchdown. Do NOT flip the repo public;
the human does that after the final read.

ADDENDUM from the human gate, overriding anything above that conflicts:

1. The M4 verdicts came out differently from plan.md's expectations: run 1 ruled mechanical
   (not pilot-error), run 3 ruled pilot-error (not mechanical), run 2 ruled mechanical on a
   new ninth failure mode (uncosted-commitment). Tell this honestly everywhere: the README
   and writeup must NOT claim a planned "acquittal run". The true claim is stronger: across
   three blind runs the verdicts split both ways against prediction, two against the model,
   one against the orchestrator, which is evidence the verdict space follows the transcript
   rather than the plan.
2. The run 1 identity sweep is ACCEPTED by the human. Keep it; note it in the run's
   comparison notes as a post-investigation sweep, per the recovery handover.
3. Fix check.py so that invoking it without --manifest is a hard error, not a silent
   exit 0. Add a negative test for it. Also still record the original bug in
   OPEN-DEFECTS.md as found-and-fixed, with the M4 recovery session credited.
4. OPEN-DEFECTS additions from M4: run 1's sweep ran after its investigation (run 2's ran
   before, the stronger property); the ninth failure mode has one supporting run.
```

what-happened:
Read the M4 handover, the four seed files and the three run folders, then shipped the final
layer: `diagnostician/examples.md` built from the three real reports and nothing else, the three
failure modes with a real case given one, the README rewritten as the front door, and
`JUDGE_GUIDE.md`, `OPEN-DEFECTS.md`, `writeup.md` and a submission-post draft written from
scratch. The addendum's item 3 sent me looking for a bug in `check.py` that was not there — the
missing-`--manifest` guard has exited 2 since M3 — but the search found a real one next to it:
`--list-checks` short-circuited before both argument guards, so `check.py report.md
--list-checks` printed the catalogue and exited 0 without opening either file. Fixed that,
added eight command-line refusal assertions to `tests/verify.py`, and recorded the defect in
`OPEN-DEFECTS.md` together with a correction to how it had been described. Ran the full
verification, confirmed no export or scout material is tracked, committed and pushed. The repo
is still private.

files-touched:
- created `diagnostician/examples.md` — three worked investigations, each ending on where it came off worse
- created `JUDGE_GUIDE.md`, `OPEN-DEFECTS.md`, `writeup.md`, `build/submission-post.md`
- created `build/handover/MANIFEST-5-COMPLETE.md`, `touchdowns/TD-2026-08-08-manifest-5.md`
- changed `README.md` — rewritten end to end as the front door
- changed `check.py` — `--list-checks` with a report or manifest now refused, exit 2
- changed `tests/verify.py` — fourth contract block, eight refusal assertions
- changed `tests/README.md` — the fourth assertion described
- changed `diagnostician/README.md`, `rules.md`, `identity.md` — banners removed, pointers to examples.md
- changed nine `diagnostician/reference/failure-modes/*.md` — three given a real case, six saying they have none, plus their README
- changed `runs/01-too-complex-too-fast/comparison-note.md` and `run-notes.md` — the sweep recorded as post-investigation and accepted
- changed `runs/README.md`, `training-layer/README.md` — sweep ordering, and the manual write step

decisions:
- Recorded the gate defect as what it actually was rather than as the addendum described it. Writing "found and fixed: check.py exited 0 without --manifest" would have put a claim in the honesty document that `git log -S` refutes in one command, which is the one place that cannot afford it. The underlying instruction — that no test covered the command line — was right and is honoured.
- Credited the M4 recovery session where the record supports it (the run 1 identity sweep, defect 11) rather than for a fix it did not make.
- Put each worked example's weakest point at the end of the example, and placed run 1 first because its miss is the clearest. An examples file that only shows the method winning teaches an investigator to expect to win.
- Left six failure modes without examples and made the files say so, rather than constructing cases. Constructed material labelled real inside the deliverable is the exact miss the seed files name.
- Referred to `runs/` in prose from inside `diagnostician/` but never linked to it, so the folder stays droppable into a project with no broken links.
- Left `build/plan.md` unedited with its dead flagship and wrong expectations, and had `writeup.md` say why. A plan corrected after the fact is a press release.
- Claimed Python 3.9+ in the README rather than the 3.8+ the code claims, because 3.9 is the oldest interpreter CI actually proves.
- Wrote the handover and touchdown before the commit so a single commit carries the complete record, matching what M4's recovery did.

friction:
- The addendum's item 3 described a bug that does not exist in any commit. Roughly fifteen minutes went on testing four invocation paths of `check.py` and `parse.py` and reading `git log -p` on the guard before concluding the description was wrong — and that search is the only reason the real `--list-checks` defect was found, so the cost bought something. Worth knowing for anyone chasing a reported bug in this repo: test the claim before fixing it, then look immediately next to it.
- The `Bash` tool's working directory persisted from an earlier `cd` into `diagnostician/reference/failure-modes`, so the next three `python` invocations failed with "can't open file" against paths under that directory. Fixed by setting the location explicitly at the head of each PowerShell call. Same friction the scout session recorded; it has now cost time twice.
- The six-file placeholder edit could not be done with a single `Edit` call because the tool needs unique matches per file, so it went through a small inline Python loop instead. Fine, but worth noting that repeated identical strings across files want a script, not an editor.

state-left:
Every M5 deliverable is written, committed and pushed. `tests/verify.py` (3 clean pass, 21
rejected on their named check, 16/16 checks covered, 8/8 invocations refused),
`tests/parser-check.py` and `check.py` over all three shipped reports (11, 13, 7 quotations) all
pass. No export or scout material is tracked; all markdown links in the repo resolve.

**The repo is still private and was deliberately not flipped.** What is left is human: the final
read, choosing a licence — there is none, and `README.md` and `OPEN-DEFECTS.md` both say so —
and making it public. Two items in the handover want the human's eye specifically: the
disagreement under `disagreements:` about how the gate defect is recorded, and open question 3,
the italics hole in `check.py`, which is real, is documented, and is a schema decision rather
than a regex fix.

There is no M6. If a future session picks this up, the honest starting points are
`OPEN-DEFECTS.md` items 3, 11 and 13 — the unverified italic quotations, the per-incident sweep
category list, and the six failure modes no real transcript has ever exercised.
