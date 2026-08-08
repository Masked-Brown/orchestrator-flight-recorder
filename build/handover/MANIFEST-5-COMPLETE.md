# MANIFEST 5 — COMPLETE

status: complete-with-questions
completed-by: M5, 2026-08-08

summary: The ship layer. `diagnostician/examples.md` written from the three real runs and
nothing else; the three failure modes that have a real case now carry one and the other six say
plainly that they do not; README rewritten as the front door; `JUDGE_GUIDE.md`,
`OPEN-DEFECTS.md`, `writeup.md` and a submission-post draft written. The claims audit removed the
last stale statements and, more importantly, removed the planned flagship: the story now told
everywhere is the true one, which is stronger. The human's addendum item 3 turned out to be
right about the disease and wrong about the symptom — see decisions 1. **The repo has not been
flipped public.** That is the human's call after the final read.

---

## files-created

- `diagnostician/examples.md` — three worked investigations, drawn only from `runs/`. Each one
  carries what the run got right, the move that made it, and where it came off worse: run 1's
  elided contradiction, run 2's disagreement with its own answer key, run 3's verdict against
  the expectation recorded for it. Closes with what three runs do **not** establish. No links
  out of the folder, so the deliverable stays self-contained.
- `JUDGE_GUIDE.md` — sixty seconds with nothing installed (run 1's report, then its answer key,
  then the grading, with the miss named as the thing to look for), then the full battery:
  `verify.py`, `parser-check.py`, the gate over all three shipped reports, breaking a quote by
  hand, the three negative fixtures worth reading, the accretion layer and its sources, and
  re-running a blind investigation on the reader's own export. Ends with what a cold clone
  cannot verify.
- `OPEN-DEFECTS.md` — fourteen numbered defects plus scope boundaries and housekeeping.
- `writeup.md` — the build story, with the flagship correction as its second section.
- `build/submission-post.md` — three drafts, the first recommended, with a `<REPO_URL>`
  placeholder and a pre-post checklist.

## files-changed

- `check.py` — `--list-checks` alongside a report or a manifest is now refused with exit 2. See
  decisions 1.
- `tests/verify.py` — a fourth contract block: eight invocations that cannot check anything must
  exit 2 and must never print `PASS`. Nothing in the first three blocks changed.
- `tests/README.md` — the fourth assertion described.
- `README.md` — rewritten end to end.
- `diagnostician/README.md` — the "not finished yet" banner replaced with the self-containment
  statement; `examples.md` row filled; eight modes → nine.
- `diagnostician/rules.md`, `diagnostician/identity.md` — footers point at `examples.md`.
- `diagnostician/reference/failure-modes/` — `vocabulary-mismatch`, `uncosted-commitment` and
  `ambiguous-instruction` carry a real worked case; the other six say no investigation has
  landed on them and none is invented; the README notes which is which.
- `runs/01-too-complex-too-fast/comparison-note.md` — a closing section recording the sweep as a
  post-investigation sweep, accepted by the human, with what the ordering costs this grading.
- `runs/01-too-complex-too-fast/run-notes.md` — sweep recorded as accepted rather than pending.
- `runs/README.md` — run 1's sweep named as the exception to the sweep-before-investigation
  property.
- `training-layer/README.md` — the write step recorded as manual.

---

## decisions-made

1. **The gate defect was real, and it was not the one the addendum described. Both facts are in
   `OPEN-DEFECTS.md`.** The addendum said `check.py` exits 0 when invoked without `--manifest`.
   It does not: that guard has been in the file since M3 and exits 2, which `git log -S` on the
   guard's text shows in one command. But the flag was right that a silent-pass route existed —
   `--list-checks` short-circuited before both guards, so `check.py report.md --list-checks`
   printed the catalogue and exited **0** without opening either file. That is the worse of the
   two: a missing manifest at least produces an error a person reads, whereas this produces
   plausible output and success, which is all a CI step or a wrapper script looks at.

   Fixed, tested, and recorded as defect 4 **including the correction to its description**. The
   alternative — writing "found and fixed a bug where check.py exited 0 without `--manifest`",
   as instructed — would have put a claim in a public repo that the repo's own git history
   refutes, in the one document whose entire job is being trustworthy about weaknesses. The
   underlying instruction was right and is honoured: the real defect was that **nothing tested
   the command line at all**, so either route could have regressed unnoticed. Eight invocations
   are now asserted.

   Credit is assigned to what the record supports: the human's final read caused this to be
   found; the M4 recovery session is credited where it earned it, which is defect 11 (the run 1
   identity sweep).

2. **`examples.md` teaches through the misses, not around them.** The obvious shape is three
   clean demonstrations. Instead each example ends on where that investigation was weakest, and
   run 1 — which has the clearest miss — is placed first. A worked-examples file that only shows
   the method succeeding trains an investigator to expect success.

3. **Six failure modes were left without examples rather than given constructed ones.** The
   files say no investigation has landed on them. Filling them with invented cases would have
   been the exact label failure the seed files name, in the deliverable itself.

4. **`examples.md` mentions `runs/` but does not link to it.** The self-containment rule is that
   nothing in `diagnostician/` may *depend* on a file outside it. Prose references to the wider
   project are useful to a reader who has the repo and harmless to one who has only the folder;
   a relative link is a broken link the moment the folder is dropped into a project.

5. **`build/plan.md` was left unedited.** It still names a flagship run that does not exist and
   still expects verdicts that did not arrive. `writeup.md` says so explicitly and says why the
   file was not corrected: a plan quietly rewritten after the fact is not a plan.

6. **The README makes no claim about the acquittal being planned.** It states what happened —
   both recorded expectations were wrong, in opposite directions, two verdicts against the model
   and one against the orchestrator — and argues that this is the stronger claim. Same in
   `writeup.md`, `runs/README.md` and `examples.md`.

7. **Python version stated as 3.9+ rather than 3.8+.** The code claims 3.8; CI's oldest job is
   3.9. The README claims what CI proves.

8. **The submission post went to `build/`, not root.** It is build material, not part of the
   deliverable or the evidence.

---

## disagreements

**One, and it is decision 1.** The addendum's item 3 asked for the original bug to be recorded
"as found-and-fixed, with the M4 recovery session credited." The bug as described did not exist
in any commit, and the M4 recovery did not touch that code path. Recording it as asked would
have been unverifiable from a fresh clone, which is the standard this same prompt set. What is
recorded instead is the real defect, the correction to its description, and the fact that the
human's read is what caused it to be found. This is flagged rather than silently resolved.

---

## open-questions

1. **The repo is still private.** M5 did not flip it, per instruction. The final read is the
   remaining gate, and `build/submission-post.md` carries the reminder in its checklist.

2. **No licence is chosen.** `README.md` and `OPEN-DEFECTS.md` both say so. Until one is picked,
   the default applies and nobody may reuse this. A judged public repo probably wants one.

3. **The italics hole in the gate is open** (defect 3). `check.py` verifies block quotes and does
   not look inside prose, so a report can quote the record in italics and escape verification.
   Run 3 does this in three places, checked by hand. Closing it properly is a schema decision —
   what may a report do with a three-word phrase? — not a regex, so it was recorded rather than
   patched in the ship stage.

4. **The sweep category list is still per-incident** (defect 11, second half). Run 1's blind spot
   was structural: the categories came from the intake rather than from a standing pre-commit
   check. Nothing in M5 changed that. The next person shipping an excerpt can make the same miss.

5. **Six of nine failure modes are untested against a real transcript.** Recorded as defect 13.
   Only more real runs close it.

---

## verification at close

    python tests/verify.py         CONTRACT HOLDS — 3 clean pass, 21 rejected on their named
                                   check, 16/16 checks covered, 8/8 invocations refused
    python tests/parser-check.py   PARSER CONTRACT HOLDS
    python check.py × 3            PASS — 11, 13 and 7 quotations

    git ls-files | grep -E '<export patterns>|ofr-scout'   → nothing tracked

All markdown links in the repo checked programmatically: 0 broken.

## next-manifest-needs

There is no M6. What remains is human: the final read, the licence, and the decision to flip the
repo public. The two things worth reading first are `writeup.md`'s flagship correction and
`OPEN-DEFECTS.md` items 4 and 11 — one is a disagreement with the addendum, the other is the
near-miss that would have been permanent.
