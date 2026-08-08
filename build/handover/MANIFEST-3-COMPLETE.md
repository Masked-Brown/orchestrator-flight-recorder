# MANIFEST 3 — COMPLETE

status: complete-with-questions

summary: The invariant is now a property. `check.py` enforces sixteen checks — spec.md's
seven gate rules, which expand to eight mechanical checks, plus eight more that M1 and M2
established and asked for. `tests/verify.py` runs the gate in both directions and asserts
a contract stronger than the manifest required: every broken report must fail on the check
it was built to break **and on no other**, which is provable because each negative fixture
differs from a passing report by exactly one mutation. The suite is 3 clean reports passing
and 21 broken reports rejected on their named check, with a third assertion that fails the
build if any check the gate can report has no fixture behind it. Two of the three findings
that shaped the final code came from the gate rejecting my own first clean report, which is
the tests doing their job before CI ever ran.

---

## files-created

- `check.py` — the blocking gate. Reads a report plus the manifest it claims to be about;
  exit 0 if every rule held, 1 if any did not, 2 if it could not run. Stdlib only, 3.8+.
- `tests/verify.py` — runs both directions and asserts the contract. Exit 0 or 1.
- `tests/fixtures/synthetic-export.json` — a CONSTRUCTED export in the real export's shape.
  Two conversations: a ten-message session where an instruction with two available readings
  is bound silently, and a four-message session with a thin recorder and a tool error.
- `tests/cases/` — three clean reports, all of which must pass:
  `grid-mismatch-pilot-error.md` (a `pilot-error` finding with ranked contributing factors,
  quotation from both the speech and reasoning channels, and shortening with `[...]`),
  `thin-record-undetermined.md` (an `undetermined` finding with both `none.` forms), and
  `windowed-origin-outside.md` (an `undetermined` finding on a manifest windowed to messages
  6-10, where the origin is upstream of the window).
- `tests/negative/` — 21 deliberately broken reports, listed under decision 4.
- `.github/workflows/verify.yml` — CI. The suite on Linux (3.9 and 3.13) and Windows (3.13),
  plus a separate job that fails the build if any raw export file is ever tracked.
- `.gitattributes` — stops git normalising the fixture export's line endings.

## files-changed

- `tests/README.md` — replaced M1's placeholder with what is actually there: how to run the
  suite, what the three assertions are, and the one maintenance trap (editing the fixture
  export by one byte fails every test on `record-pairing` until the new fingerprint is
  written into each report).

---

## decisions-made

### The shape of the gate

1. **Sixteen checks, and each one traceable to a seed file or a prior handover.** spec.md's
   seven gate rules expand to eight mechanical checks, because "missing counterfactual, or a
   report that continues past it" is two different failures with two different messages.
   The other eight were asked for upstream, not invented here:

   | check | where it comes from |
   |---|---|
   | `primary-cause-count` | spec.md — more than one primary cause, or zero |
   | `quote-verbatim` | spec.md — the fabrication check |
   | `verdict-enum` | spec.md — verdict outside the enum |
   | `prescription` | spec.md — prescription patterns |
   | `factor-anchor` | spec.md — a contributing factor with no anchor |
   | `counterfactual-missing` | spec.md — missing counterfactual |
   | `report-continues` | spec.md — a report that continues past it |
   | `failure-mode-file` | spec.md — a named mode with no file |
   | `quote-anchor` | M2 next-manifest-needs, "two extra checks are available and cheap" |
   | `undetermined-resolution` | M2 next-manifest-needs, the same pair |
   | `reasoning-attribution` | M2 decision 9 and next-manifest-needs, "mechanically detectable from the anchor" |
   | `record-pairing` | M2 open question 3 — its recommendation was hard failure |
   | `heading-block` | M2 decision 40 — the provenance lines |
   | `section-quote-required` | M2 decision 43 — sections 2 and 3 each need a quotation |
   | `missed-catch-points` | M2 decision 42 — an omission and a finding of none must be distinguishable |
   | `section-order` | structural prerequisite; nothing else can be located without it |

2. **The manifest is required; there is no structural-only mode.** A `--no-manifest` flag
   would produce a cheaper pass that looks like a pass, and the one guarantee this entry
   makes is the one it would skip. Consequence in open question 2.

3. **`--list-checks`, so the test suite can ask the gate what it enforces.** This is what
   makes the coverage assertion possible: a check added without a fixture fails the build
   instead of sitting there looking like enforcement.

### Verifying the verifier

4. **Every negative fixture is derived from a clean report by exactly one mutation**, by
   script, with the script asserting each target string occurs exactly once. A hand-written
   broken report proves only that something in it was wrong. A one-mutation diff proves the
   gate reacted to *that*. The 21 fixtures and the check each must trip:

   `fabricated-quote`, `quote-welded-across-channels`, `quote-stitched-segments`,
   `wrong-role-anchor` → `quote-verbatim`; `two-primary-causes`, `no-primary-cause` →
   `primary-cause-count`; `prescription-in-factor`, `prescription-future-advice` →
   `prescription`; and one each for `failure-mode-file`, `counterfactual-missing`,
   `report-continues`, `factor-anchor`, `quote-anchor`, `reasoning-attribution`,
   `verdict-enum`, `record-pairing`, `missed-catch-points`, `section-order`,
   `heading-block`, `section-quote-required`, `undetermined-resolution`.

5. **The assertion is exact-set equality, not membership.** `verify.py` requires the set of
   checks a negative fixture trips to be exactly `{expected}`. Asserting only that the
   expected check is *among* the failures would pass a sloppy fixture that breaks four
   things at once, and the point of the exercise is that the gate discriminates.

6. **Manifests are built at test time by running `parse.py`, not committed.** The tests then
   exercise the real parser-to-gate path, and a stored manifest cannot drift from what
   `parse.py` actually emits. This caught nothing yet; it is insurance against M1's schema
   and M3's reader disagreeing silently later.

7. **The synthetic export carries a message with two separate stretches of speech either
   side of a tool call.** Added specifically so the cross-segment stitching branch has a
   fixture — untested code in a gate is a small lie. It is also what real assistant messages
   look like, which M1's decision 3 is about.

8. **`.gitattributes` marks `tests/fixtures/**` as not-text.** The fixture export is hashed
   byte-for-byte and its fingerprint is written into every clean report, so git's end-of-line
   normalisation would fail `record-pairing` on one platform and pass on the other. This is
   the failure mode that would have cost a day to diagnose from a red CI badge alone, so
   Windows gets its own CI job to prove the fix rather than assume it.

9. **A CI job that fails if any raw export file is tracked.** `.gitignore` is the first
   defence, but it can be edited and `git add -f` ignores it entirely. This is the risk
   register's catastrophic item, so it gets a check that does not depend on anyone's care.

### The quote check — answering M1's open question 2 and M2's open question 2

10. **Normalisation: line endings unified, runs of whitespace collapsed to one space, ends
    trimmed. Nothing else.** Rewrapping a long quotation to fit the page has not altered it,
    and failing a report for where its margin fell would train people to fight the gate. A
    changed word, a fixed typo, a dropped clause and altered punctuation all still fail.

11. **A quotation must match inside a single segment of a single message on a single
    channel.** This is the half that does the real work. Without it a report could weld the
    model's private working-out onto the reply it actually sent and still pass, which is
    exactly the merge the flattened `text` field makes and the whole design exists to
    prevent. `quote-welded-across-channels` is the fixture.

12. **When a quotation matches only if two segments of the same channel are run together,
    the gate says so specifically** rather than reporting a generic mismatch. Same-channel
    stitching is a plausible honest mistake — the two stretches really are both in that
    message — so the message has to explain why it is still not a quotation.

13. **`[...]` splits the quotation into fragments that must each appear, in order, without
    overlapping, inside the same segment.** M2 decision 49 permits shortening; this is the
    implementation. Fragments cannot bridge messages because the whole match is confined to
    one segment already.

14. **A quote against a channel whose text the manifest does not carry fails, but with a
    different message naming `--include-tool-io` and `--include-attachments`.** `parse.py`
    leaves tool and attachment text out by default, so this is usually a manifest built
    without the right flag rather than a fabrication. Verified in both directions: the same
    report fails against a default manifest and passes against one built with the flag.
    Reporting it as fabrication would be an accusation the record does not support.

### Anchors — answering M2's open question 3

15. **The role element is enforced.** M2 offered to relax it to advisory if brittle. It is
    not brittle: the role comes from the manifest and a mis-citation is a real error worth
    catching. `wrong-role-anchor` is the fixture.

16. **A `source-sha256` mismatch is a hard failure**, per M2's recommendation, and the
    literal `not recorded` passes for a report built from a plain transcript. A report
    checked against the wrong manifest passes or fails for no reason at all, so the pairing
    has to be established before any message number means anything.

17. **Anchors are resolved at paragraph level, not line level.** Found by the gate rejecting
    my own first clean report: reports are written in wrapped prose, and an anchor routinely
    splits across a line break with `msg 6` at the end of one line and `(assistant,
    REASONING):` at the start of the next. A line-based reader fails honest reports for
    where their margin fell. The same fix applies to the prescription check's anchored
    exemption.

18. **Where an introducing paragraph carries more than one anchor, the last one wins.** It
    is nearest the quotation and it is the one a reader would take as introducing it.

### Prescription — answering M2's open question 5, and its caution

19. **Two tiers.** Hard patterns fail wherever they appear: `next time`, `you should`,
    `in future`, `to fix this`, `lessons learned`, `improved version` and about thirty more.
    Soft constructions — `should have`, `ought to have`, `would have been better` — fail
    only when the surrounding paragraph carries no message anchor. That is M2's decision 29
    made mechanical: past tense and this session is a counterfactual and is required;
    the same words with nothing anchoring them are advice about a session nothing can check.

20. **spec.md's bare token `try` is not matched literally**, per M2's caution in its
    disagreement 5. Matched literally it fires on "the model tried to open the file". The
    phrasings `try this`, `try instead` and `you could try` are matched instead. Logged as a
    disagreement below because it is a departure from the literal text of a locked file.

21. **Block quotes are never scanned for prescriptions.** An orchestrator who wrote "next
    time, use v2" inside the transcript is evidence, and failing a report for quoting it
    accurately would be perverse. The `Reporter's hypothesis:` line is exempt for the same
    reason — it is recorded as they put it.

### Reasoning attribution

22. **The speech-verb list was cut back to twenty unambiguous verbs.** The first version
    included the bare forms `say`, `state`, `write`, `tell` and `claim`, and it rejected my
    own clean report for the phrase "put where it could be confirmed" — `confirmed` in the
    sense of verified, not spoken. These words carry ordinary non-speech senses that appear
    constantly in honest investigative prose. A gate that fails good reports gets worked
    around, and then it enforces nothing.

23. **The check runs on the paragraph introducing a quotation, and on any other single line
    carrying a reasoning anchor.** The introducing paragraph is where a thought gets dressed
    as speech most often and most damagingly. Broadening the whole check to paragraph level
    was tried and rejected: a paragraph that legitimately mentions what the orchestrator said
    *and* separately anchors to the reasoning channel would false-positive.

### What was deliberately not done

24. **`check.py` is not mentioned anywhere inside `diagnostician/`.** M2 established the
    folder is self-contained and that the gate is evidence *about* the deliverable rather
    than part of it. Verified still true.

25. **The "one sentence" primary-cause rule is not machine-checked**, per M2's decision 52.
    Sentence-counting would fire on a semicolon or an abbreviation and would be enforcing
    punctuation rather than discipline. The mechanical form of the rule is the single
    `Failure mode:` line, which is checked.

26. **`parse.py` was not changed**, so M2's open question 4 is still open. Reasons in open
    question 3 below.

---

## disagreements

None with the locked anchors in spec.md. The seven gate rules are all enforced, the verdict
enum is unchanged, and the report shape is M2's as written. Three departures, logged:

1. **spec.md's prescription pattern list includes the bare token `try`, and the gate does not
   match it literally.** M2 raised this in its disagreement 5 and recommended phrases; I
   agree and have implemented phrases. Matched literally, `try` rejects "the model tried to
   open the file at msg 12" and "a second attempt at msg 31", which are ordinary
   investigative prose. spec.md describes *patterns* rather than mandating literals, so this
   is a reading rather than an override — but it is the one place the gate does less than the
   locked text says on a plain reading, and it should be a conscious choice rather than an
   assumption. If the intent was literal, this is the line to change.

2. **Nine checks beyond spec.md's seven gate rules.** Every one is justified in decision 1
   and traceable to M1 or M2, and none of them contradicts anything locked. Flagged because
   the cumulative effect is a stricter gate than spec.md alone describes, and a stricter gate
   is a real cost to M4: a report that is substantively correct can still be rejected for a
   missing `Missed catch points:` line. That cost is deliberate — every one of these was
   asked for by the manifest that wrote the rule — but it is a cost.

3. **The negative fixture count is 21, against plan.md's six named fixtures.** plan.md names
   a fabricated quote, two primary causes, a smuggled prescription, a missing counterfactual,
   an unanchored factor and an invented failure mode. All six exist. The other fifteen cover
   the checks plan.md's list does not reach, including the two spec.md gate rules that had no
   fixture named — zero primary causes, and a verdict outside the enum. Verifying seven rules
   with six fixtures would have left two rules unverified.

---

## open-questions

1. **Prescription detection is heuristic and will stay heuristic — for `OPEN-DEFECTS.md` at
   M5.** M2 predicted this and it is confirmed. The tense-and-target rule is a real
   specification, but the gate implements it as a phrase list plus an anchored-paragraph
   exemption, and a determined writer can prescribe in words no list contains: "the target
   was never named, and naming it is what this needed." Nothing in that sentence is on any
   list. The honest statement for OPEN-DEFECTS is that the gate catches the recognisable
   shapes of advice and does not decide intent.

2. **A report built from a plain transcript cannot be gate-checked — for `OPEN-DEFECTS.md`.**
   `rules.md` §1 and `diagnostician/README.md` both promise the folder degrades gracefully to
   an ordinary pasted transcript. It does, as a method. But `check.py` requires a `parse.py`
   JSON manifest, so a report produced that way can carry `source-sha256 not recorded` and
   pass the pairing check while its quotations are never verified against anything. The
   deliverable's promise and the gate's coverage do not line up, and the README should not
   imply that they do. Options for M5: accept a plain-text file as a match target, or state
   the limit plainly. I did not widen the gate here because inventing an input format is not
   an enforcement decision.

3. **M2's open question 4 is still open: the parser does not expose fork parentage, and I
   did not change it.** M2 flagged it for M3 as "the next manifest that touches code". I
   judged it out of remit and left it. Three reasons, offered so the next manifest can
   overrule me cheaply: M1 verified byte-identical output across runs and I would be
   invalidating that verification without re-running M1's checks; the current behaviour is
   correct and merely conservative, which M2 itself says; and no test fixture or gate rule
   needs it, so a change now would be untested by the suite I was asked to build. It is a
   ten-line change to `find_branch_points` and the manifest entry, and it belongs to whoever
   next has a reason to re-verify the parser.

4. **Two known limits in `reasoning-attribution`, both deliberate.** It will miss a speech
   verb that sits in a different paragraph from the anchor it belongs to, and it will fire on
   a sentence that legitimately reports what one party said in a paragraph that also anchors
   to the reasoning channel. The check was tuned toward missing rather than false-firing,
   because a gate that rejects honest reports stops being used. Worth a line in OPEN-DEFECTS.

5. **Unchanged and still for the human: M1's open question 1 about the flagship incident.**
   I note that `build/handover/M4-INTAKE.md` now exists and is committed, so the halt may
   already be resolved; I did not read it, as it is M4's input and not M3's.

---

## next-manifest-needs

M4 reads its intake file, then this one, then M1's and M2's, then the seed files.

**How to run the gate:**

    python parse.py <export> --index N --messages A-B --json --out manifest.json
    python check.py runs/<incident>/report.md --manifest manifest.json

Exit 0 means shippable. `--json` gives machine-readable failures; `--list-checks` lists what
it enforces. The full suite is `python tests/verify.py`.

**What M4 must get right for a real report to pass**, in rough order of how easy each is to
get wrong:

- **Section headings are exact**: `## 1. Incident statement` through `## 7. Counterfactual
  test`, in order, all seven present, nothing after section 7.
- **Six fixed lines, spelled exactly**: `Reporter's hypothesis:`, `Missed catch points:`,
  `Verdict:`, `Would resolve it:` (when undetermined), `Failure mode:`, `Contributing
  factors:`. The two list lines need their explicit `none.` form when there are none.
- **The heading block above section 1** needs all three lines, and `source-sha256` must be
  the fingerprint of the manifest actually being checked. Copy it from the manifest header.
- **Every quotation is a block quote preceded by an anchor** of the form `msg N (role,
  CHANNEL)`, with role and channel matching the record. Quotation marks are never used to
  quote the record.
- **If a report needs to quote a tool result or an attachment**, the manifest must be built
  with `--include-tool-io` or `--include-attachments`, or the quote cannot be verified. Decide
  this before the run, not after, because the fingerprint changes with the flags.

**One thing worth knowing about the fresh-chat runs.** The gate is strict about form and
knows nothing about quality: a report can pass all sixteen checks and still be a bad
diagnosis, and it can fail on a missing `Missed catch points:` line while being an excellent
one. If a blind run produces a good finding in slightly the wrong shape, the honest record is
that the run produced it and the shape was corrected — not a silent reformat. That
distinction is worth keeping in the run notes, because a gate that quietly launders output is
worth less than one that logs what it rejected.

**For M5.** Open questions 1, 2 and 4 above are `OPEN-DEFECTS.md` entries, already worded to
be lifted. The 60-second `JUDGE_GUIDE.md` protocol has an obvious spine: clone, run
`python tests/verify.py`, read `CONTRACT HOLDS 3 clean reports pass, 21 broken reports
rejected on their named check, 16 checks covered.` No install, no export, no network.
