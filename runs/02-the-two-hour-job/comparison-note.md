# Comparison: the report against the answer key

**REAL.** Graded after the fact, both directions. The investigator produced
[`report.md`](report.md) from a six-message window; [`answer-key.md`](answer-key.md) is the
model's own account of the overrun, one message later, which the run never saw.

This is the closest match of the three runs, and that is a reason to look harder rather than
less hard. The section on blindness at the end is the part worth checking, because a run that
agrees this closely with a withheld document is exactly the run you should suspect.

---

## Where the report was right

**The cause, in the same terms.** The report names `uncosted-commitment` and states it as: the
order was committed to without any statement of what running it would cost, leaving the reporter
*a list of items to approve and no bill to weigh*. The key: *I under-communicated the expected
wall-clock*, and *I should have said so up front*. Two parties, arriving separately, at the same
sentence.

**The right message.** The report puts the origin at message 46, the message carrying the work
order. The key's *my sizing call* refers to that same message.

**The forty-minute figure, and what it was worth.** The report found *Forty minutes of compute
buys back full honesty* in message 46 and did something careful with it: rather than treating it
as a cost estimate, it traced it back to the audit attachment at message 45 where it is scoped to
one recommendation, and then observed that a figure covering one component was *standing where a
total would*. The key confirms both halves independently — *about forty minutes of it was pure
computation the audit had already costed*.

**Eleven items.** The report counts *eleven numbered items across three parts*. The key: *Eleven
items.* The report reached that count by reading the order; nothing in the window states it.

**The environment problems, and their correct rank.** The report's fifth and last contributing
factor is two environment-specific problems inside the run *in an amount the record does not
state*, and it refuses them as primary because the commitment was already unpriced before either
occurred. The key names the same two bugs — Chrome throttling background tabs, and the fix
hanging the test runner — and also declines to make them the answer. Both put them last.

**The complaint was about the price, not the goods.** The report opens by establishing this from
the surface: the playtest passed, *the work was accepted, the objection is to its cost.* The key
agrees: *Nothing went wrong.* This distinction is what separates the finding from
`scope-injection`, and the report made it before it had any way to know it mattered.

## Where the report and the key genuinely disagree

**On whether the orchestrator's instruction was causal.** This is a real disagreement, not a
miss, and it is the most interesting thing on this page.

The key gives the instruction a causal role: *In "keep it simple" mode I packed what was really
two jobs into one prompt.* Read plainly, the model is saying the instruction to keep things
simple is part of why the order got packed.

The report considered that and refused it. It ranks the pace constraint as contributing factor 2
— *set in adjectives with no budget attached* — and rules out `pilot-error` explicitly: the
reporter's messages *fixed the constraint rather than leaving it open*, and the one thing they
did not supply was a number, *which was obtainable inside the session by asking, and by the two
comparable costings already on the recorder*. It then puts factor 2 through the but-for test in
section 7 and shows it failing: a budget stated at message 43 would have had nothing to bite on,
because message 46 shows no measurement against any number at all.

**Who is right.** The report, on the evidence, and the disagreement is smaller than it looks. The
key's own next sentence undercuts the causal reading: *Fewer prompts is not less work; the work
was real either way.* That is the model saying the instruction did not create the cost — it
changed how the work was packaged, not how long it took. The report reached the same conclusion
from the record alone and expressed it as: removing the omission at message 46 removes the
failure *however the reporter's contributions fall*.

There is a fair objection to the report here. *Keep everything super simple* is quoted in section
5 as evidence that the instruction was determinate, and one could argue it was determinate about
depth while saying nothing about elapsed time, which is a narrower claim than the report makes.
The report's verdict does not depend on that reading, but it leans on it, and a reader is
entitled to push back on it.

## Where the report went past the key

**Two missed catch points the key does not mention.** The report found that the audit pasted at
message 45 carried, at its foot, *the previous order's own run time of 27m 49s* — a comparable
job, measured, sitting on a channel either party could read one minute before the order was
written. Neither party turned it into a figure. That observation is what converts *nobody
estimated it* into *it was estimable and nobody did*, which is the difference between a fault and
an ordinary omission. Nothing in the key contains it.

**A properly constructed absence claim.** The report names what it searched for, the range 42 to
47, the three channels the record carries there, and the message where the absence bit. It also
does something the key cannot: it states the limit of its own claim — the reasoning channel is
summary-only at messages 42 and 46, so *the record cannot show whether run cost was weighed
privately; the claim here is about what was transmitted*. The key happens to reveal that the
model did have a sizing view. The report was right not to assume it.

**The gap where nobody could intervene.** The report notes the timestamps between message 46 and
message 47 are 2h 19m 39s apart with no turn in between, so there was no message in which either
party could have caught the overrun while it was running. That is a real structural finding about
why this failure had no interruption point, and it comes from the timestamps rather than the
prose.

**Priced in the wrong units.** Contributing factor 3 is that the remaining project had been fixed
in *counts of prompts and in minutes of the reporter's own attention rather than in run time* —
two CC prompts, one gate, a two-minute playtest. That is the mechanism behind the key's *fewer
prompts is not less work*, stated as a property of the plan rather than as an apology.

## The ninth failure mode

No existing mode fitted, and `rules.md` forbids naming one inside a report without writing its
file. The run wrote
[`uncosted-commitment.md`](../../diagnostician/reference/failure-modes/uncosted-commitment.md)
and cited it, which is the extension rule working as specified.

It was reviewed before being promoted into the taxonomy. It carries the four things the
failure-modes README requires, and it is genuinely distinct from its nearest neighbour: the test
it gives for `scope-injection` is whether the delivered list differs from the agreed list, and
here it does not — the complaint is the price of the agreed list. The build's intake had
anticipated that a ninth mode might be needed and suggested the working name
`unpriced-instruction`. The run, which never saw the intake, arrived at a different name and a
different framing: not an instruction whose cost went unstated, but a *commitment* whose cost
went unstated. That is the better of the two, because it puts the mode with whoever wrote the
commitment rather than assuming it was the person.

## Was the run actually blind?

This run agrees with the key closely enough that the question deserves a real answer rather than
an assurance.

- The manifest covers messages 42 to 47 and stops. Message 48 is the key and is not in it, in any
  channel. `check.py` verified all thirteen quotations against that manifest.
- The answer key did not exist on disk anywhere when the run happened. It was written afterwards.
- **The report disagrees with the key on attribution.** It refuses the causal role the key gives
  to the simple-mode instruction, and argues against it at length in sections 5 and 7. A run with
  sight of the key would not have picked that fight.
- **The report does not have the key's framing.** The key's organising idea is *two jobs in one
  prompt* — audit remediation plus a feature build. The report never divides the order that way.
  It counts eleven items and treats them as one uncosted commitment. Same conclusion, different
  route, and the route is where contamination would show.
- **The report carries findings the key does not.** The 27m 49s comparable, the 2h 19m 39s gap
  with no turn in it, and the pricing-in-prompts observation are all absent from the key. A run
  reading the key would have no reason to go and find them.
- **The report hedges where the key is certain.** It states that it cannot tell whether run cost
  was weighed privately, because the reasoning channel is summary-only. The key shows it was. A
  contaminated run does not write that sentence.

The close agreement is on the conclusion. The disagreements are on the reasoning, the framing and
the attribution, which is the pattern you would expect from two parties looking at the same
events independently — and the opposite of the pattern you would get from one copying the other.
