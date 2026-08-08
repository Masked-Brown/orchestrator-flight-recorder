# MANIFEST 2 — COMPLETE

status: complete-with-questions

summary: The scored substance is written — `rules.md`, the eight failure-mode files,
`report-schema.md` and `verdict-classes.md`. The deliverable folder is now self-contained and
usable: a stranger can drop it into a project and get a diagnosis, and the only thing missing
is worked examples, which are deliberately left for the real runs. Two decisions carry the most
weight. First, M1's open question 3 is answered: the investigator **may** quote the model's
private reasoning, but every quotation carries its channel, a speech verb may never be used for
it, and — the rule that does the real work — a party cannot be faulted for missing a sign that
existed only on a channel they could not see. Second, the report format now pins down exactly
what a "quoted passage" is, so M3's fabrication check has something deterministic to match
against: quotations live in block quotes, block quotes are used for nothing else, and quotation
marks are never used to quote the record. Partway through the session the human's
`M4-INTAKE.md` appeared in the working directory. It closes M1's open question about the
flagship incident, carries one instruction aimed directly at `rules.md` (acted on, decision 58),
and contains an off-by-one hazard between its zero-based windows and the parser's 1-based
message numbers that will corrupt the flagship run if nobody reconciles it first. All of it is
set out under "the M4 intake landed during this session" below.

---

## files-created

- `diagnostician/rules.md` — the method. Fourteen numbered sections: what recorder you have,
  the order of work, scope-fixing, anchoring and the channel rules, surface-then-walk-back, the
  stopping rule, the but-for test, cause versus symptom, anti-compression, verdict versus
  mechanism, when the record cannot say, the reporter's hypothesis, the no-prescription
  invariant, and stopping.
- `diagnostician/reference/report-schema.md` — the seven sections with their fixed lines, the
  citation format in full, and a skeleton template marked ILLUSTRATIVE.
- `diagnostician/reference/verdict-classes.md` — the five verdicts, what the record must show
  for each, what each one is *not*, the debiasing check before `pilot-error`, and a table for
  choosing between neighbours.
- `diagnostician/reference/failure-modes/ambiguous-instruction.md`
- `diagnostician/reference/failure-modes/missing-context.md`
- `diagnostician/reference/failure-modes/stale-constraint.md`
- `diagnostician/reference/failure-modes/vocabulary-mismatch.md`
- `diagnostician/reference/failure-modes/thread-overload.md`
- `diagnostician/reference/failure-modes/premature-parallelism.md`
- `diagnostician/reference/failure-modes/scope-injection.md`
- `diagnostician/reference/failure-modes/unverified-claim-accepted.md`

Each mode file carries four sections: what it is, what it looks like in the record, a
comparison table against the modes it is confused with, and what would rule it out. Each ends
with a marked placeholder for the worked example that M5 adds from a real run.

## files-changed

- `diagnostician/reference/failure-modes/README.md` — replaced the planned-set list with the
  real index, added a "narrowing down" guide (six questions, each splitting the set roughly in
  half), and added the rule for adding a mode later.
- `diagnostician/README.md` — the under-construction note now says what is actually true after
  M2 (identity, rules and reference written; examples deliberately absent until there are real
  ones). Added a short paragraph under "What you get back" explaining that every claim points at
  a message and carries its channel. Table updated; `examples.md` marked as not yet written.
- `diagnostician/identity.md` — one line. Its closing pointer promised the report's shape in
  `rules.md` *and* the report format in `reference/`, which was double-attributed. It now points
  at `rules.md` for method and `reference/` for the report's shape, the verdicts and the modes.
  M1 asked that the promise be kept accurate; this keeps it.

---

## decisions-made

Every rule authored in this manifest, with why. Grouped by file.

### rules.md — reading the recorder

1. **Read the header before the messages.** The window, the reasoning coverage, the forks and
   the provenance all bound what can be concluded. An investigator who does not know which
   instruments were recording will over-read the ones that were. This also makes M1's coverage
   header load-bearing rather than decorative.
2. **Degrade gracefully to a plain transcript.** `diagnostician/README.md` already promises the
   folder works on an ordinary transcript, so the rules must survive one: everything is `SAID`,
   say so in the report, and do not treat a channel you never had as one you checked and found
   empty. Without this the folder's own README overclaims.
3. **A fixed order of work, eleven steps, with the reporter's hypothesis read last.** Makes the
   method reproducible rather than a matter of taste, and the ordering is doing real work — see
   rule 26.

### rules.md — scope

4. **Turn the complaint into one line naming something findable in the record.** A complaint is
   not a specification. Without this step the investigation has no fixed point and the report
   drifts into whatever was most interesting.
5. **Investigate the incident as stated, not the most interesting thing found.** This is the
   structural defence against the audit-tool failure named in the brief. A report that quietly
   widens its own scope has become an inventory.
6. **"Nothing in this window matches the complaint" is a legitimate finding.** Otherwise the
   only way to satisfy the format is to find something, which manufactures causes. Requires
   naming what was searched for and where.

### rules.md — anchoring and the channels (this group answers M1's open question 3)

7. **Citation form: `msg N (role, CHANNEL)` followed by a block quote.** Message number because
   findings must be checkable; role because writing the wrong one is a mistake worth catching;
   channel because of rules 8–12. Uses the manifest's own words (`human`/`assistant`, and M1's
   six channel labels) so the rules and the evidence share one vocabulary, as M1 asked.
8. **A table of what each channel can support.** The channels are not interchangeable evidence
   and the differences are not obvious. `SAID` supports anything; `ACTION`/`RESULT` support that
   something happened and whether it errored; the reasoning channels are governed by 9–12.
9. **Never use a speech verb for the reasoning channel.** The model did not say, tell, claim or
   state anything there — it was working out, weighing, settling on. **This is the answer to
   M1's open question 3, and it is the same error the export's own flattened text field makes.**
   The parser refuses to merge the channels; the report must not merge them back in prose.
10. **Nobody could see the reasoning channel except the model.** So a missed catch point cannot
    rest on it. If the only sign at that moment was in `REASONING`, the person could not have
    noticed, and faulting them for it is hindsight, not a finding. This is the load-bearing half
    of the answer to open question 3 — quoting reasoning is safe, but *reasoning from* it about
    what someone should have seen is not — and it is exactly right in-domain: the cockpit voice
    recorder is not available to anyone outside the cockpit.
11. **A `REASONING-SUMMARY` is not the model's words.** M1 established these are the export's own
    compressed summaries, produced because the reasoning was withheld. Citing one as verbatim
    model phrasing would be fabrication with an extra step. It may establish that something was
    considered, never how it was expressed; and if the primary cause rests on one with nothing
    corroborating, the report says so in a sentence. Disclosure rather than prohibition, because
    a summary can still be the right evidence and the reader is entitled to know how thin the
    ground is.
12. **A withheld reasoning block with no summary is not evidence.** M1 found 24 of these. You
    know one thing: something was thought. You may state the channel was withheld; you may not
    characterise it.
13. **Check what your manifest actually inlines.** M1's decision 9 leaves tool arguments, tool
    output and attachment text out by default, recording only presence, name, size and the error
    flag. So "the tool reported an error at msg 31" is supportable and "the tool returned X" is
    not. Without this rule an investigator will narrate the contents of a file it was only told
    the size of — a fabrication the quote-checker cannot catch, because nothing was quoted.
14. **An absence claim needs three parts:** what you searched for, the exact range and channels
    you searched, and the message where a party had to proceed without it, quoted. spec.md
    explicitly permits an absence as the causal origin, and absences are often the truest answer
    — but a loosely stated absence is unfalsifiable, and an unfalsifiable finding is worthless.
    The third part also guarantees section 3 always carries a quotation, which keeps the gate
    uniform.
15. **Forks are alternative versions of one turn, and are never evidence of repetition.**
    Resolves the question M1 flagged in its decision 5. M1 chose to flag forks and not
    reconstruct a main path; this says what the investigator does with the flag. The specific
    prohibition matters: read linearly, a fork looks like the orchestrator saying the same thing
    twice, which invites a manufactured cause about insistence or frustration. If which branch
    was live would change the finding, the finding cannot be settled — see rule 25.

### rules.md — finding the origin

16. **Surface first, then walk back; most of what you pass is travel, and travel is not cause.**
    The surface is the one thing locatable with certainty because the reporter supplied it.
    Naming the travel as travel is what makes section 4 a path rather than a list.
17. **First-in-time is not cause.** Real transcripts contain false starts and tangents that go
    nowhere. The earliest odd-looking thing is not the origin by virtue of being early — a
    genuinely tempting error, because early oddities are easy to find and look explanatory.
18. **The stopping rule: stop at the last point that is both on the recorder and inside the
    session** — the latest message at which a different message would have prevented the failure.
    Two consequences stated explicitly: the recorder is the boundary of the investigation (no
    walking back into anyone's mood, workload or intent, because there is no instrument for
    them), and it is the *last* such point, not the first (walking back to the earliest
    contributing influence is how investigations end up blaming the weather). plan.md asks
    rules.md for a stopping rule; this is it, and it is the rule that stops causal chains
    running backwards forever.

### rules.md — the tests

19. **The but-for test must name a specific message and a specific change**, with three named
    ways it fails: the failure happens anyway (not the cause), a different failure happens
    (contributing factor), or the record cannot say (route to undetermined). "Had the instruction
    been clearer" is not a counterfactual because every instruction could have been clearer and
    nothing can check it.
20. **Cause versus symptom, stated once:** remove the cause and the symptoms go with it; remove a
    symptom and the cause is still there producing others. This is the separator the brief scores
    hardest and it needs to be one sentence an investigator can actually apply.
21. **Two candidates that each survive the other's removal are independent — do not merge them.**
    Either two separate incidents (investigate the one you were asked about) or a genuinely mixed
    verdict.
22. **Anti-compression, made testable: delete half your primary-cause sentence.** If the
    remaining half still explains the failure, the deleted half was a separate factor and belongs
    ranked beneath. plan.md asks for "hold distinct factors distinct; rank, do not merge"; a bare
    instruction to that effect is easy to agree with and impossible to apply, so it needed a
    test. The "and" versus "which led to" check follows from it.
23. **Rank contributing factors by how much the outcome depended on each**, not by how bad each
    looks and not chronologically. Without a stated criterion, ranking becomes a list in the
    order they were noticed, which is a list.
24. **Verdict and failure mode are separate questions and neither decides the other.** The mode
    names the mechanism; the verdict names whose failure it was. The same mechanism appears under
    different verdicts depending on the record — set out concretely at the foot of
    `unverified-claim-accepted.md`. Collapsing them would quietly turn each mode into a verdict
    and destroy the acquittal space.

### rules.md — undetermined, hypothesis, prescription, stopping

25. **Four concrete triggers for `undetermined`**, each drawn from the export's actual shape
    rather than invented: origin outside the window, reasoning absent exactly where the decision
    must have happened, a fork whose branches imply different causes, or decisive material in an
    attachment or tool result the record does not carry. Plus what it is *not*: a finding you
    would rather not write. M1 asked that the fallback connect explicitly to the coverage header;
    it does, in both `rules.md` and `verdict-classes.md`.
26. **An undetermined finding must enumerate the live candidates and name obtainable resolving
    evidence.** Two possibilities laid out with anchors is a real investigative result; a shrug
    is not. "We would need to know what they were thinking" is not obtainable and is not an
    answer.
27. **Test the reporter's hypothesis last, then resolve it explicitly — confirmed, refined, or
    set aside with the reason.** plan.md requires it be tested and never privileged. Reading it
    last is the mechanism that makes "never privileged" real: a hypothesis read first becomes the
    shape the evidence gets fitted to, and you do not notice yourself doing it. Requiring explicit
    resolution stops the opposite failure of quietly ignoring it.
28. **No prescription, justified in-domain with two reasons.** A proposed fix smuggles in a
    conclusion you have not finished proving; and the report is read by the person whose
    decisions it examines, so a report ending in advice reads as a judgment on them and stops
    being usable. Both reasons are about why the report gets worse, not about a rule being
    obeyed — which is the difference between an invariant and a preference.
29. **The line between a counterfactual and a prescription is tense and target.** Past, this
    session, checkable against the record → required. Future, or any session other than this one
    → cut. With a usable field test: a sentence that would still make sense pasted into someone
    else's transcript is a recommendation. This matters because section 7 is *made of* sentences
    that superficially resemble advice, and without a stated distinction an investigator either
    writes prescriptions or becomes unable to write the counterfactual at all.
30. **Stopping is the last place the discipline can fail, and it is where it usually does.**
    Named as a rule rather than left as a formatting note.

### verdict-classes.md

31. **A mandatory check before writing `pilot-error`: state what `mechanical` and `environment`
    would each require here, and go and look for them.** The person who commissioned the report
    is usually the one who was steering, and that expectation is a current running one way. This
    is the concrete mechanism behind the acquittal discipline plan.md asks for — "remember
    acquittal is available" is not a mechanism; a pre-commit check is.
32. **`pilot-error` requires both halves:** the message showing what it did or did not determine,
    *and* the downstream point where that bit.
33. **"A better message was possible" is not a cause.** True of every message ever written, so it
    explains nothing. Vagueness becomes a cause only at the point it forces a choice. Without
    this, `pilot-error` is always available and the verdict space collapses.
34. **`mechanical` requires proving the instruction was determinate** — the half people skip —
    *and* showing the departure. Otherwise acquittal becomes the easy verdict instead of the
    honest one.
35. **The stranger test separates `pilot-error` from `mechanical`:** read the instruction as
    someone who does not know what was wanted. If the model's reading is available to that
    stranger, the instruction admitted it.
36. **`environment` requires a direct trace, not an inference**, in one of four named forms. "The
    model seemed to lose track" is a guess in a technical costume. Also noted that this verdict is
    under-used because tool failures are unglamorous, with an instruction to check the `RESULT`
    channel for errors before concluding anyone made a mistake.
37. **`mixed` requires demonstrated independence, and has a stated tie-break:** the one whose
    removal alone would have prevented it; failing that, the earlier one. spec.md requires a
    primary still be named under `mixed`, so the tie-break had to be written down or it becomes
    arbitrary.
38. **`mixed` is not a diplomatic setting** and `undetermined` is not a hedge. Both are the same
    failure — declining to state what the record supports — and both needed saying out loud,
    because both are the comfortable option.
39. **A neighbour-disambiguation table**, one question per confusable pair. The verdict is chosen
    under exactly the conditions where a general principle is hardest to apply.

### report-schema.md

40. **A heading block before section 1 carrying the record's name, its fingerprint and the
    window.** A report and the record it claims to be about are checked as a pair; without a
    fingerprint in the report there is nothing tying them together, and a report checked against
    the wrong manifest passes or fails for no reason. Uses the fingerprint M1 already puts in
    every manifest header.
41. **Six fixed lines with exact labels:** `Reporter's hypothesis:`, `Missed catch points:`,
    `Verdict:`, `Would resolve it:`, `Failure mode:`, `Contributing factors:`. Each corresponds
    to a spec.md gate rule and gives M3 something deterministic to find. In particular, `Failure
    mode:` appearing exactly once is the mechanical form of "more than one primary cause, or
    zero".
42. **Explicit `none.` forms** for missed catch points and contributing factors. An omission and
    a finding of "none" look identical otherwise, and only one of them is a statement. This also
    lets the gate tell a missing section from an empty one.
43. **Sections 2 and 3 each require at least one anchored quotation**, including when the origin
    is an absence — rule 14 guarantees there is always something to quote.
44. **A fixed line format for propagation-trace steps**, each anchored, so the trace is a
    sequence of located events rather than a narrative.
45. **A missed catch point requires that the party could actually have seen the sign** — rule 10,
    restated where it will actually be applied.
46. **Block quotes are only ever quotations from the record, and every one is preceded
    immediately by its anchor.** This is what makes spec.md's fabrication check implementable: it
    defines "quoted passage" as a syntactic object a script can extract without guessing.
47. **Quotation marks are never used to quote the record.** The alternative — checking every
    double-quoted run — false-positives on ordinary prose (naming a verdict, a term of art) and
    would fail honest reports. Making block quotes the only quoting device removes the ambiguity
    entirely, at the cost of a slightly more formal writing style. Worth it: this is the entry's
    load-bearing guarantee.
48. **One block = one message = one channel = one continuous stretch.** No stitching. Assembling
    a quotation from two channels is precisely how a thought becomes a statement, which is the
    failure this whole design exists to prevent.
49. **Shortening with `[...]` is allowed; every fragment must be exact and in order, and it may
    never bridge two messages.** Long messages are common and unabridged quotation would make
    reports unreadable, so a prohibition here would just be ignored.
50. **Rewrapping lines is fine; nothing else about a quotation may be altered, including a typo.**
    Fixing someone's typo inside a quote is a small, well-meant fabrication.
51. **The file ends at section 7** — no summary, no appendix, no closing note.
52. **"One sentence" for the primary cause is a discipline for the writer, not a machine check.**
    Recorded so M3 does not attempt sentence-counting; the mechanical check is the single
    `Failure mode:` line.

### failure-modes/

53. **Every mode file carries the same four sections, and the fourth is "what would rule it
    out".** spec.md asks for definition, transcript signature and distinguishing test. The fourth
    is an addition: a mode with no falsifying condition will absorb every case offered to it, and
    a taxonomy containing one stops distinguishing anything. This is also what lets an
    investigator eliminate rather than only match.
54. **Three modes carry a specific evidentiary burden**, because they are the three most easily
    asserted from impression: `thread-overload` requires the open items to be listed with the
    message each entered at; `unverified-claim-accepted` requires the cheapness of the missed
    check to be anchored (quote the message where that same tool is used routinely);
    `scope-injection` requires the start-versus-surface difference to be written out item by
    item. Each converts a feeling into something checkable.
55. **The two sequence-level modes are separated by count versus order.** `thread-overload` is
    about how many things are unresolved at once and can happen on a single thread;
    `premature-parallelism` is about starting before finishing and can happen with a low open
    count. Without this they blur, and a taxonomy with two interchangeable entries is worse than
    one with a single entry.
56. **A "narrowing down" guide in the failure-modes README**, six questions each splitting the
    set roughly in half. Eight files is enough that a linear read is a poor way in.
57. **`vocabulary-mismatch.md` carries a note that this is the mode the report itself is most at
    risk of committing.** plan.md names jargon as the #9 build's stall and requires this entry not
    commit the failure it diagnoses; putting the warning inside the mode file puts it where it
    will actually be read.

### rules.md — added after the M4 intake landed mid-session

58. **"Standing material is not a turn"** — a new subsection in §4. Saved preferences, standing
    instructions, pasted briefs and carried-over handovers arrive inside a message and read like
    something someone just typed. They are evidence of what the parties were operating under, not
    of what passed between them, and the damage is worst when reading for tone: a standing
    preference of the form *push back if I am wrong* becomes, read as a live turn, a correction
    or a flash of frustration that never happened. Two rules follow — identify the standing
    material before reading anything for tone, and never cite it as a reaction, though it may be
    quoted as a constraint in force.

    **Provenance, stated plainly:** this rule is not M2's idea. `build/handover/M4-INTAKE.md`
    appeared in the working directory partway through this session, and its standing correction 3
    reports that the scout hit exactly this false positive on this exact phrase, and asks that
    "the diagnostician's rules should name it". The intake is addressed to M4, but the file it
    asks to change is M2's, so acting on it here is better than leaving a known-needed rule out
    of the rulebook for a later manifest to patch in. Generalised from the specific phrase to the
    class of material, since the specific phrase is one orchestrator's preference and the failure
    is general. It also connects usefully to `stale-constraint`, which is where standing material
    most often goes wrong.

---

## disagreements

None with the locked anchors in spec.md. The seven sections are as specified, in order, with the
report ending at the counterfactual; the verdict enum is unchanged; the eight modes are the eight
named. Four additions and one caution, logged rather than assumed:

1. **The heading block is an addition to the report.** spec.md specifies seven sections and says
   nothing about what precedes them. Three provenance lines now sit above section 1. Justified in
   decision 40: without them a report cannot be paired with the record it is about, and M3's
   fabrication check has no way to know it is reading the right manifest. Nothing in spec.md is
   contradicted — the seven sections and the ending are untouched.

2. **`Reporter's hypothesis:` is placed in section 1.** spec.md's intake section says the
   reporter's guess is "recorded" but does not say where, and section 1 is described only as the
   incident statement. Putting it there keeps the scope-fixing material together and gives the
   gate a fixed place to look. Flagged because it is a choice, not a reading.

3. **Quotation is restricted to block quotes, and quotation marks may not be used to quote the
   record.** This is the most consequential addition in the manifest and it constrains how the
   investigator writes, not just what it may claim. spec.md requires that every quoted passage
   appear verbatim in the manifest; it does not say what makes something a quoted passage, and
   that question has to be answered before the rule can be enforced at all. The cost is a
   slightly more formal register in reports. The alternative — treating every double-quoted run
   as a quotation — would fail honest reports that put quote marks around a verdict name.

4. **Each failure-mode file has a fourth section spec.md does not ask for** ("what would rule it
   out"). Reason in decision 53.

5. **A caution about one of spec.md's gate rules, for M3.** The prescription patterns list
   includes the bare token `"try"`. Matched literally that will fire on ordinary investigative
   prose — "the model tried to open the file", "a second attempt at msg 31". Recommend matching
   phrases (`try this`, `you could try`, `try instead`) rather than the bare word, and using the
   tense-and-target test from decision 29 as the actual specification. Not a divergence, since
   spec.md describes patterns rather than mandating literals — but implemented literally it would
   reject clean reports.

---

## the M4 intake landed during this session

`build/handover/M4-INTAKE.md` was not present when M2 started and appeared before M2 committed.
It is the human's file and M2 has not modified it. It changes the picture in four ways that the
next manifest needs to know about, and one of them is a hazard.

**It closes M1's open question 1.** M1 was right that the #9 jargon stall is not in this export.
The human has re-chosen from what is actually here: three runs, not two — a flagship
("too complex, too fast"), an attribution run ("the two-hour job"), and a run explicitly built to
land somewhere other than `pilot-error` ("the wrong file"). Each has an answer key held back from
the diagnostician — the next message after the window, in the session's own words. That is a
better evidence shape than M1 hoped for and it is available three times over.

**It closes M2's open question about forks** (numbered 4 in the draft of this handover, now
folded into the list below). The intake instructs the parser to walk `parent_message_uuid` as a
tree and mark abandoned branches. That is the parser-side fix M2 identified and declined to make.
`rules.md` §4 keeps its conservative fork rule regardless: it is correct whether or not the
record marks the live branch, and it degrades safely if someone runs the folder against a record
that does not.

**⚠ The indexing hazard, and it is expensive if missed.** The intake specifies windows as
zero-based array indices — "idx 9 to 11", "idx 0 to 8", "ends at idx 46". `parse.py` numbers
messages from **1**, and every message number in a report refers to that 1-based number. Running
`--messages 9-11` against a window the human wrote as `idx 9-11` produces a window shifted by one
and, in the flagship's case, would pull in part of the withheld answer key at idx 12. Someone has
to reconcile this explicitly before M4 runs — either by converting in the intake or by stating
the convention in each run folder. Do not let it be discovered from a confusing report.

**Several of its standing corrections are already satisfied**, and rewriting working code to meet
them would be a waste and a risk. `parse.py` already reads all the text-bearing fields it names
(text blocks, thinking, attachment extracted text, tool result content — the last two behind
flags), already emits the three-state reasoning coverage per assistant turn, already keys on uuid
and supports `--uuid`, already refuses zero-message conversations, and `__pycache__/` is already
in `.gitignore`. What is genuinely outstanding is the branch-tree walk and the Windows stdout
encoding. Read M1's handover before touching the parser: its schema section was produced by
script against the real file, and the intake's framing that the parser "was built before the
schema was known" is not quite right — where the two differ, the intake is asking for more, not
correcting an error.

**One thing to decide before the repo goes public, for M5 and the human.** M2 has committed the
intake unmodified, because it is a handover file, plan.md puts handover files in the build record,
and the repo is private until M5's final read. But the intake is not covered by the sweep it
orders. It discloses the replay id `nbs-replay-121496` in the same sentence that instructs every
shipped excerpt to redact it, and it points at which message indices in the private export hold
Neon project ids and revenue figures. None of that is exploitable — the export never ships — but
a file that names an identifier while telling you to redact that identifier should not be
published without someone deciding it deliberately. The options are to redact the intake before
the repo flips, or to keep it out of the public tree entirely. That is a human call, not M3's or
M4's, and it should not be made by default.

**On the proposed ninth failure mode.** The intake suggests `unpriced-instruction.md` — an
instruction satisfied literally with its cost never surfaced — if run 2's cause fits none of the
eight. M2 has deliberately not written it. The extension rule in `failure-modes/README.md` says a
mode earns a file when a real session fails in a way none of the existing files describes, not
when one merely fits awkwardly, and writing it now would be inventing a mode with no case behind
it — which is the thing the rule exists to prevent. Forward view, offered as information rather
than a decision: on M2's reading it does look like a real gap. `scope-injection` is the nearest
neighbour and it does not fit, because the job did not change size — it was carried out exactly
as written, and what went unsaid was the price. M4 should expect to write the file, from the
record, after the run.

## open-questions

1. **For M3 — how exact is the quote match?** M2 has narrowed M1's open question 2 as far as the
   schema can. Settled here: a quoted passage is a block quote; it must fall inside a single
   segment of a single message on a single channel; `[...]` splits it into fragments that must
   each match, in order, within that same segment; rewrapped lines are acceptable and altered
   words are not. Left to M3: the normaliser itself. Recommendation unchanged from M1 —
   normalise line endings and collapse runs of whitespace before comparing. M3 owns the call.

2. **For M3 — how hard should the anchor format be enforced?** The anchor is `msg N (role,
   CHANNEL)`. The message number and the channel are load-bearing. The role element is redundant
   with the manifest and exists to catch mis-citation. If it proves brittle in practice, relaxing
   the role to advisory is a reasonable call and does not weaken anything else. Related: decide
   whether a `source-sha256` mismatch between report and manifest is a hard failure or a warning.
   M2's recommendation is hard failure for a mismatch, and a pass for the literal string `not
   recorded` when the input was a plain transcript.

3. **For M3 — the fork work is now specified, and `rules.md` must keep working without it.** The
   manifest flags forks but does not expose parent message ids, so an investigator reading a
   manifest alone cannot tell which branch was live. M2 identified this and declined to patch the
   parser (it is M1's artifact; M2's remit is substance). The intake has since instructed M4 to
   walk `parent_message_uuid` as a tree and mark abandoned branches, which resolves it at source.
   The open part is for M3: when the parser gains branch marking, **do not weaken the rule in
   `rules.md` §4 to match**. It is written to be correct on a record that marks the live branch
   *and* on one that does not, because the folder is a drop-in that strangers will point at
   records this project never produced. Flagged because the temptation to simplify a rule once
   the tooling improves is exactly how a drop-in folder quietly acquires a dependency on its
   birthplace.

4. **For M3 and M5 — prescription detection is heuristic and will stay heuristic.** Decision 29
   gives a real specification (tense and target), but the edge is genuinely thin: "had msg 14
   named the build" is required and "msg 14 should have named the build" is borderline. Suggest
   M3's detector permits past-subjunctive constructions that carry a message anchor and rejects
   bare imperatives and future-tense advice. Whatever remains uncaught belongs in `OPEN-DEFECTS.md`
   at M5, named plainly.

---

## next-manifest-needs

M3 reads this file, then M1's handover, then the seed files — spec.md's gate rules in particular
— and then `build/handover/M4-INTAKE.md`, which is already written and already constrains what
M3 builds. The indexing hazard flagged above is M3's first practical problem, because M3 is the
last manifest before anyone runs the parser against a chosen window in anger.

What M3 can assume is already true:

- **The report format is fixed and deterministic where it needs to be.** Section headings are
  `## 1. Incident statement` through `## 7. Counterfactual test`. Six fixed lines carry the
  labels listed in decision 41. Every gate rule in spec.md maps onto something syntactic:

  | spec.md gate rule | What to check |
  |---|---|
  | more than one primary cause, or zero | count of lines beginning `Failure mode:` — must be exactly 1 |
  | quoted passage not verbatim | every block quote, matched against the manifest per decision 46–50 |
  | verdict outside the enum | the `Verdict:` line against the five names |
  | prescription patterns | see open question 5; decision 29 is the specification |
  | contributing factor with no anchor | each numbered item under `Contributing factors:` must contain `msg N` — unless the line is `Contributing factors: none.` |
  | missing counterfactual, or continuing past it | `## 7. Counterfactual test` present; nothing after its content |
  | named mode with no file | the `Failure mode:` value must match a filename in `reference/failure-modes/` |

- **Two extra checks are available and cheap**, beyond spec.md's list: every block quote must be
  immediately preceded by a valid anchor line (an unanchored quotation is unattributed), and the
  `Would resolve it:` line must be present when the verdict is `undetermined`. Both are M2
  requirements; treat them as gate rules unless there is a reason not to.
- **The eight mode files exist**, named exactly as spec.md lists them. The `Failure mode:` value
  is the filename without `.md`.
- **The deliverable folder is self-contained.** Nothing inside `diagnostician/` points outward
  except one sentence in its README explaining where a manifest comes from. Verified. `check.py`
  is deliberately not mentioned inside the folder — the gate is evidence *about* the deliverable,
  not part of it.

For M3's negative test cases, the six spec.md rules map cleanly onto six broken reports. Two more
worth building, because they are the failures this manifest's rules exist to prevent: a report
that quotes the `REASONING` channel with a speech verb and no channel in its anchor, and a report
whose missed catch point rests on evidence only the model could see. The first is mechanically
detectable from the anchor. The second is not detectable and should be a documented limit rather
than a test — worth stating in `OPEN-DEFECTS.md`.

For M4: `rules.md` §1 assumes the investigator is handed a manifest with a coverage header. If a
run's window is chosen where the reasoning channel is thin, that is not a problem to work around
— it is the condition the undetermined path was written for, and a run that exercises it honestly
would be strong evidence.
