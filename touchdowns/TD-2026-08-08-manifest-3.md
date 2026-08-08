# Touchdown: manifest-3

date: 2026-08-08

window: Manifest 3 (Enforcement)

prompt-received:

    You are Manifest 3 of the orchestrator-flight-recorder build.

    Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

    Poll for build/handover/MANIFEST-2-COMPLETE.md. If absent, wait 60 seconds and check again;
    loop until present. When present, read it first, then the four seed files in build/.

    Execute Manifest M3 exactly as specified in build/plan.md (Enforcement): check.py, the test
    cases, the negative fixtures that verify the verifier, tests/verify.py, and CI. Every
    negative fixture must fail on its named check; assert N/N in verify.py.

    Finish by writing build/handover/MANIFEST-3-COMPLETE.md. Commit and push (verify git status
    shows no export files first).

what-happened: Waited for M2 through a polling monitor, reading the seed files and M1's
parser in the meantime. Built `check.py` with sixteen checks — spec.md's seven gate rules
expanded to eight, plus eight more that M1 and M2 had explicitly asked the enforcement
manifest to add. Built a CONSTRUCTED two-conversation export as the test record, wrote three
clean reports against it, then generated 21 negative fixtures by script, each derived from a
clean report by exactly one mutation. `tests/verify.py` asserts three things: clean reports
pass, each broken report fails on its own check *and no other*, and every check the gate can
report has a fixture behind it. The suite went green at 3/3, 21/21, 16/16 and CI runs it on
Linux and Windows plus a job that fails the build if a raw export file is ever tracked.

files-touched:

- created `check.py` — the blocking gate, sixteen checks, stdlib only
- created `tests/verify.py` — both directions plus the coverage assertion
- created `tests/fixtures/synthetic-export.json` — CONSTRUCTED record, two conversations
- created `tests/cases/` — 3 clean reports (pilot-error, undetermined, windowed-undetermined)
- created `tests/negative/` — 21 one-mutation broken reports
- created `.github/workflows/verify.yml` — suite on 3 platform/version combinations, plus a privacy job
- created `.gitattributes` — stops git normalising the hashed fixture's line endings
- created `build/handover/MANIFEST-3-COMPLETE.md`
- changed `tests/README.md` — replaced M1's placeholder with the real contract

decisions:

- Sixteen checks rather than seven, every extra traceable to M1 or M2 — inventing enforcement would have been overreach, but ignoring what the prior manifests asked for would have been worse.
- `verify.py` asserts exact-set equality on the failing checks, not membership — asserting only that the right check is *among* the failures would pass a fixture that breaks four things.
- Negative fixtures generated from clean ones by a single scripted mutation — a one-mutation diff proves the gate reacted to that mutation rather than to general brokenness.
- Manifests built at test time by running `parse.py`, not committed — the tests then exercise the real parser-to-gate path and cannot drift from what the parser emits.
- Quote matching normalises only line endings and whitespace runs, and must match inside a single segment — rewrapping is presentation, but welding a thought onto a statement is the fabrication the whole design exists to prevent.
- Speech-verb list cut to twenty unambiguous verbs after it rejected an honest report — a gate that fails good reports gets worked around, and then it enforces nothing.
- spec.md's bare token `try` matched as phrases rather than literally, per M2's caution — logged as a disagreement because it is a departure from the locked text on a plain reading.
- `parse.py` left unchanged despite M2 flagging fork parentage for M3 — out of remit, and changing it would invalidate M1's byte-identical verification without re-running M1's checks.

friction:

- M2 was not finished at session start. A background `until` loop was the obvious poll, but the Bash tool's timeout caps at ten minutes and the wait was longer than that, so it was replaced with a persistent monitor emitting a heartbeat every fifteen minutes. Worth knowing for M4 and M5: for a chained wait, use the persistent monitor, not a background sleep loop.
- The gate rejected my own first clean report on three counts. Two were real bugs: anchors were being read line by line, and reports are written in wrapped prose, so `msg 6` at the end of one line and `(assistant, REASONING):` at the start of the next read as no anchor at all. That would have failed honest reports for where their margin fell. The third was a false positive — `confirmed` in the sense of verified, caught by an over-broad speech-verb list. All three were found by the tests before CI existed, which is the argument for the tests.
- `--list-checks` was unusable on first run because argparse still required the positional report and `--manifest`. Fixed by making them optional and validating by hand.
- Adding a second speech segment to the fixture export (needed so the cross-segment stitching branch had a test) changed the file's sha256, which invalidated the fingerprint already written into the clean reports. Cheap here, but it is the maintenance trap in this design and it is now documented in `tests/README.md`.
- The fixture-generating script failed once on a target string that turned out to be split across a line break in the source file — the same wrapping problem as the anchor bug, in a different costume.
- Noticed and headed off before it could bite: the fixture export is hashed byte-for-byte, so git's end-of-line normalisation would have failed `record-pairing` on Windows and passed on Linux, or the reverse. `.gitattributes` pins the bytes and a Windows CI job proves it rather than assuming it.

state-left: M3 is complete and committed. `python tests/verify.py` from a fresh clone
prints `CONTRACT HOLDS 3 clean reports pass, 21 broken reports rejected on their named
check, 16 checks covered.` with no install, no export and no network. M1, M2 and M3 are all
on `main`; `git status` is clean and no export file is tracked, verified by hand and now by
CI. `build/handover/M4-INTAKE.md` exists and is committed, so the human halt appears to be
resolved and M4 is unblocked — I did not read it, as it is M4's input. Three items are
worded ready to lift into `OPEN-DEFECTS.md` at M5: prescription detection stays heuristic; a
report built from a plain transcript cannot have its quotations verified, which does not
match what the deliverable's README implies; and two tuned-toward-missing limits in the
reasoning-attribution check. M2's open question about exposing fork parentage in the parser
is still open and was consciously left, with reasons in the handover so the next manifest can
overrule it cheaply.
