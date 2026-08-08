# The build story

How this repo was made, what was planned that turned out to be false, and what the evidence
actually is once the false part is removed.

Everything asserted here can be checked against something in the repo. Where a claim rests on
material that is not in the repo — a personal export, mostly — it says so.

---

## The shape, and why this shape

The brief was to build a folder-based diagnostician that reads something broken and says **why**
it broke. Not how to fix it.

Two decisions did most of the work.

**The investigator is an air accident investigator, and that is not costume.** The competition's
bar — one primary cause, contributing factors ranked beneath it, reasoning shown, cause separated
from symptom, no fix, stop — is the literal professional structure of an accident report. It
means the no-prescription rule has an in-domain justification rather than an arbitrary one: in
that profession the cause report and the recommendations are two separate documents, written by
different people at different times, and mixing them is how an investigator ends up committed to
a cause they never proved. It also hands over the acquittal verdict for free. Pilot error versus
mechanical failure versus environment is the working vocabulary of the field, and a diagnostician
that can only ever find against the person asking is not diagnosing.

**The input is a machine artefact, not pasted text.** Most entries in a competition like this
diagnose something a person copies into a box. This one ingests the Claude data export — the
actual JSON — through a deterministic parser. That buys three things nothing else could:

- **The channels stay apart.** Each message in an export carries a flattened `text` field *and* a
  structured list of content blocks, and they are not the same thing: the flattened field splices
  the model's private reasoning into the prose it actually sent, with no marker between them.
  Anything built on that field can quote a thought as a statement. `parse.py` reads the blocks and
  labels every segment `SAID`, `REASONING`, `REASONING-SUMMARY`, `ACTION`, `RESULT`, `ATTACHMENT`,
  and the gate refuses a quotation that welds two of them together.
- **The propagation trace becomes possible.** A turn-by-turn path from causal origin to failure
  surface, including the points where either party could have caught it, requires the whole log.
  No pasted excerpt supports it.
- **Fabrication fails mechanically.** Every quoted passage must appear verbatim in the parsed
  manifest, matched by `check.py`, not by the model remembering to be careful. The persuasive
  force of one of these reports is entirely that it hands someone their own sentence back. A
  fabricated quote is not a small defect; it is the whole product failing.

---

## The correction: the flagship that was not there

**The planning documents for this build named a flagship run that does not exist, and the repo
does not pretend otherwise.**

The intended headline was that the diagnostician's first case would be *the session that built
the previous competition entry* — a real stall in that build, with an independent answer key in
the form of a journal written months earlier by a different process. `build/plan.md` still says
so, in the M4 section, and it is left there rather than edited, because a plan quietly corrected
after the fact is not a plan, it is a press release.

The scout pass over the export is where it broke. Those sessions were not in the export batch.
Claude exports arrive as increments covering recent history, not as the whole account: the batch
available covered 2026-08-01 to 08, the build in question had happened weeks earlier, and its
transcripts were simply absent. What the scout found instead were four or five *mentions* of that
build — retrospective journal prose sitting inside a tool result in a later conversation, which is
a description of a failure and not a record of one.

Running the diagnostician on a retrospective account of an incident, and then grading it against
the same account, would have been a demonstration with the evidence removed and the shape left
behind.

**So the flagship was dropped, and what replaced it is stronger.** Three live incidents from the
builder's own working week, chosen from that eight-day export by a scout pass and confirmed by a
human, run blind. And two of them turned out to carry something better than a journal written
later: an answer key written **inside the conversation itself**, by the participants, before this
tool existed and with no idea anything would ever grade against it.

- **Run 1's key is the orchestrator's own next message.** He says whether the problem was fixed
  and what fixed it — *wording is much better in that last message*, *Now I understand the full
  things* — and grants the decision the session had been blocked on.
- **Run 2's key is the model's own retrospective**, given in the session one minute after the
  complaint: *I under-communicated the expected wall-clock*, *I should have said so up front*.

Neither existed on disk anywhere at the time its run happened. Both were written into the repo
afterwards. That is a cleaner ground truth than the planned one, for the reason the planned one
was attractive in the first place: it was written by a different party, at a different time, for
a different purpose. Here that is also *contemporaneous* — the participants speaking about the
event in the event, not remembering it later.

Run 3 has no key, because its failure is stated by the orchestrator inside its own window. There
was nothing downstream to withhold. It is graded against the expectation recorded for it in
advance, which it failed to meet — see below.

---

## The verdicts came out against prediction, in both directions

This is the part of the build that could not have been designed.

`build/plan.md` recorded expectations for two of the three runs before any of them ran. **Both
were wrong, in opposite directions.**

| Run | Expected | Returned |
|---|---|---|
| 1 — the summary the reader could not follow | `pilot-error` or mixed | **`mechanical`** |
| 2 — the two-hour work order | not specified | `mechanical`, on a mode that did not exist yet |
| 3 — the substituted file | explicitly **not** `pilot-error` | **`pilot-error`** |

Run 3 is the one that matters. The intake chose that incident for exactly one reason, stated in
writing and in advance: *the verdict here should NOT be pilot-error. This run exists to
demonstrate the verdict space can find against the model.* And the same intake said what to do if
it went the other way: *If the blind run indicts the orchestrator anyway, ship it as-is and
discuss it honestly in the comparison note; do not steer the run.*

It indicted the orchestrator. It was shipped as produced — not re-prompted, not nudged, not run a
second time for a better answer. Its comparison note opens by saying so, then checks the verdict
against the documented tie-break for that pair (*read the instruction as a stranger who does not
know what was wanted; was the model's reading available to that stranger?*), finds that it was,
and records the strongest available argument against its own finding.

So **there is no planned acquittal run in this repo, and the earlier plan to have one is not
claimed anywhere.** The acquittal arrived in run 1, which nobody had designed for one, and the
indictment arrived in the run designed for an acquittal.

That is better evidence than the plan would have produced. A verdict space that acquits when the
build wanted an acquittal proves very little. One that indicts where the build hoped for an
acquittal, and acquits where the build was not looking, is a verdict space reading the transcript
rather than the room. Two of three verdicts landed against the model, one against the
orchestrator, and neither split was the one written down.

**Run 2 also disagreed with its own answer key, and was right to.** The key — the model's
retrospective — attributes the packing to the orchestrator's instruction to keep things simple.
The report refused that attribution, having found that orders were already unpriced *before* that
instruction existed, using a message the window had been deliberately extended to include. The
key's own next sentence, *fewer prompts is not less work; the work was real either way*, supports
the report. A run that agrees with a withheld document on the conclusion and disagrees with it on
the attribution is a run that read the record.

---

## The recursion that is actually true

The original pitch had a neat recursion: the diagnostician's first case would be the build of its
predecessor. That one is gone with the flagship.

Here is the one that survives, and it is checkable.

**This tool was itself built by orchestration, and the build kept its own black box.** Five
manifests plus a scout, each run in a separate context, chained on handover files, with two human
gates. `build/handover/` holds a completion handover per manifest plus the human's intake for the
run stage; `touchdowns/` holds a journal record per session, written to a fixed format under a
standing instruction, including the prompt each session was given verbatim.

That record is not a highlight reel. It contains, among other things:

- **A session that crashed mid-manifest.** M4 died at roughly task six of eight, with three
  completed investigations and a rewritten parser sitting untracked in the working tree and
  nothing committed. A recovery session audited the tree against the specification and finished
  only the gaps, and the handover itemises what was found intact versus what the recovery
  produced — because "M4 completed" and "M4 crashed and was completed by someone else" are
  different facts about the build.
- **A near-miss that would have been permanent.** The recovery's pre-commit sweep found that run
  1's window carried a personal name and a real channel identifier that the intake's sensitivity
  check had not been built to look for. This repository is public under a pseudonymous account, so
  committing it as it stood would have linked the account to the person, to a search index,
  irreversibly. It is recorded as defect 11 in `OPEN-DEFECTS.md`, including what the fix cost that
  run in evidentiary strength.
- **A gate that rejected an honest report over a capital letter.** Run 1's report was refused on
  its first pass because one anchor was written `Msg 12` at the start of a sentence where the
  pattern matched only lower-case `msg`. The gate was widened and the report was left exactly as
  the run produced it, because quietly retyping one letter in the output and reporting a clean
  pass is how a gate stops being evidence. A clean fixture now carries a sentence-initial anchor,
  so the widening is itself tested.
- **A silent-pass route in the gate's own command line**, found in the final stage while writing a
  test the human's read had asked for, and recorded as defect 4 — including a correction to how
  the defect was first described, since the first description named the wrong path.

**Every one of those is a future test case.** A session that stalls, crashes, or ships something
it should not is exactly the artefact this tool exists to read, and this build produced several.
That is the correct relationship between a diagnostician and its maker, and it is the reason the
build record ships alongside the deliverable instead of being cleaned up.

---

## What was inherited, and what was not

This is the same builder's second entry of this kind. The previous one — a review tool for
teaching material — contributed machinery: a deterministic extractor turning a binary artefact
into a checkable text record, verbatim citation as the load-bearing invariant, negative tests that
verify the verifier, blind runs in fresh chats, and a populated accretion layer.

Its named weakness was the reason for this build's central decision: **no real user existed, and
every run was constructed.** Here the orchestrator is real, the corpus is his own export, the
incidents are things that actually went wrong in his working week, and two of them were graded
against what the participants said at the time.

Nothing in this repo depends on that previous entry existing, and no claim here rests on it. It
is lineage, not evidence.

One deliberate omission is worth recording: no diagnostic pass was run over that older repo before
starting. Its own handover already named what to lift and what to leave, and re-deriving
information that had been written down would have been an instance of one of the failure modes in
this taxonomy — context that existed, was recorded, and was ignored. Skipping it was cheaper and
was also a demonstration of the lesson.

---

## What this build is not evidence of

Held here rather than left implicit, and expanded in `OPEN-DEFECTS.md`.

- **One orchestrator, three sessions, eight days.** The method works on real transcripts and
  produced findings that survived grading against withheld evidence. It is not known to
  generalise — not to other people, other work, other models, or longer horizons.
- **Three incidents chosen by a human**, not sampled. The verdict split across them says nothing
  about verdicts in general.
- **The gate proves form, never correctness.** Thirty-one quotations verified verbatim across
  three reports means no quotation was invented. It does not mean any report named the right
  cause. What tests that is the comparison notes, graded by a human against something the run
  never saw — and one of those gradings found a real miss, which is on the front page of
  `examples.md` rather than in a footnote.
- **The blind runs were isolated by protocol plus evidence, not by mechanism.** The raw export was
  readable on the same machine. The load-bearing evidence is that the reports are wrong in ways a
  contaminated run would not have been.
- **Six of the nine failure modes have never been used in a real investigation.** Their files say
  so.

The strongest single thing in this repository is not the pass rate. It is that three blind runs
produced one miss, one disagreement with the party being investigated, and one verdict against
the expectation written down before it ran — and all three shipped exactly as produced.
