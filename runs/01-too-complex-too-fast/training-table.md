# Training table — run 1

One row per investigation. The row is written from what the run actually produced, after the
gate and after the comparison against the answer key, so the middle column records the lenses
that fired rather than the lenses that were available.

| | |
|---|---|
| **Label** | **REAL** |

---

### Input window and incident statement

Messages 10-12 of `yt-wor-1.2-future-crons`, three messages of a 32-message session, plus the
tool reads inside message 10 capped at 2,000 characters each. Reasoning present in full on both
assistant turns.

> Partway through a build chat I stopped understanding the responses. Too much technical
> language and the pace kept climbing. I had to stop the session and ask for a reset. Why did
> this happen?

No hypothesis beyond the complaint itself. The answer key, message 13, was withheld.

### Investigator reasoning — which lens fired, what it checked

**Recorder first.** Read the header before the messages and stated its bounds: three of
thirty-two, nothing before message 10 available, five tool results shortened by the manifest,
15,745 characters withheld from one. Declared that no part of the finding rests on withheld text.

**Surface located, then the phrase traced.** Message 11 names one term it could not follow. The
run searched for that phrase and found it occurs in exactly one place in the record, inside the
section message 11 identifies.

**Origin tested against the stopping rule.** Rather than walking back to a message it could not
see, it applied the rule that the origin is the *latest* message where a different message
avoids the failure, and showed message 10 qualifies regardless of what messages 1-9 contain:
the turn sets its own plain-English standard in its opening line and breaks it in the next
section, so both halves are inside one message.

**Reasoning channel searched for the decision, and found an absence.** Message 10's reasoning is
recorded in full. The run searched it for any weighing of whether the wording could be followed
and reported that the question does not appear there at all — the register was never chosen as a
choice.

**Verdict argued against its neighbours, as `verdict-classes.md` requires before an indictment
and, here, before an acquittal.** `environment` refused because all five tool reads returned
success, so nothing forced the register — with message 12 as proof the same material could be
said plainly. `pilot-error` refused because no human turn exists in the window before the surface
to anchor it to, and *the person never specified a plain register* is the unfalsifiable form of
claim the method excludes.

**Channel discipline held on the missed catch points.** It found the fault was visible forming
only in message 10's reasoning, and ruled that out as a missed catch point for the orchestrator
because he could not read that channel.

**Hypothesis resolved as refined, with the untestable half named.** Language confirmed; *the pace
kept climbing* set aside as unprovable on three messages, with `thread-overload` and
`premature-parallelism` each checked and each refused on the record, and messages 1-9 named as
what would settle it.

### Finding as handed back

    Verdict:       mechanical
    Failure mode:  vocabulary-mismatch
    Gate:          PASS, 11 quotations verified

Message 10 stated the findings supporting a decision it was asking the orchestrator to make in
terms it never defined, so he could not judge the decision and stopped the work at message 11.
Contributing factors, ranked: the volume of one turn (two job reviews, four findings, two scope
additions, a revised sequence and a full work order); and the request being buried in the last
line behind all of it.

**Against the answer key:** cause confirmed, counterfactual confirmed by the orchestrator running
it in real life one turn later, factor ranking confirmed. **Missed** the contradiction inside
message 11 — the orchestrator says in consecutive sentences that he has run job 2B and that he is
about to run it — which the key states outright as *I already ran 2B before I read through your
whole response*. It was in the window, on the SAID channel, and the report quoted around it with
`[...]` twice.

### Training-layer impact — what was written to the profile

- **Register, not volume, is the thing that breaks comprehension first.** Named as a recurring
  pattern with this run as its first instance.
- **The model sets a plain-English standard and then breaks it inside the same turn.** Recorded
  as a specific, checkable behaviour rather than a general tendency.
- **The decision being asked for is placed last, behind the material justifying it.**
- **Overload shows up as action before reading, not only as complaint** — added from the answer
  key rather than from the report, and flagged in the profile as the signal this investigation
  missed.

### Future-run benefit — how the next investigation starts sharper

The next investigation of this orchestrator opens by reading his messages for **self-contradiction
about what he has already done**, not only for what he says about the model. That is the check
this run had the evidence for and did not run. Concretely: where a message reports an action and
then asks a question that presupposes the action has not happened, the profile now says to treat
that as a load-bearing overload signal and quote it rather than eliding it.

Second: where a turn promises plain English, the profile says to compare the promise against the
section that follows it, because this pairing has now been observed once and it puts the standard
and the breach in the same message, which is where the stopping rule can settle without needing
upstream context.
