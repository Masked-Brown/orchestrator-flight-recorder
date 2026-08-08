# The five verdicts

The verdict says **whose failure it was**. It is a separate question from what mechanism
produced the failure — that is the job of `failure-modes/` — and neither answer decides the
other. The same mechanism turns up under different verdicts depending on what the record shows.

Exactly one verdict per report, written in section 5, spelled exactly as it appears here:

`pilot-error` · `mechanical` · `environment` · `mixed` · `undetermined`

---

## Before you commit: the standing pull

The person who asked for this report is almost always the person who was steering. They came to
you because something they were running went wrong, and they half expect to be told what they
did. That expectation is a current, and it runs one way.

So there is one mandatory check before you write `pilot-error`. **Write down, for yourself, what
`mechanical` would require here and what `environment` would require here, and go and look for
each in the record.** Not as a formality — actually look. If neither is there, `pilot-error`
stands and it stands on stronger ground for having been tested.

An investigation whose verdict is the same every time is not an investigation. It is a
formality with a conclusion attached.

---

## `pilot-error` — the person steering

**What it means.** The instruction as written caused the failure: it admitted the reading the
model took, or it left out something the model demonstrably needed and had no way to obtain.

**What the record must show.** Both halves, anchored:

1. The message, quoted, showing what it did or did not determine.
2. The point downstream where the model acted on that gap or that second reading — the moment
   the under-determination actually bit.

**What is not pilot error.** *A better message was possible.* Every message ever written could
have been better, so it explains nothing and cannot be a cause. Vagueness only becomes a cause
at the point it forces a choice. If the model resolved an ambiguous instruction correctly and
the session failed elsewhere, the ambiguity is not your cause no matter how visible it is.

Nor is it pilot error that the person did not anticipate a behaviour nobody would predict. The
question is whether the message as written left the door open, not whether a more suspicious
person might have nailed it shut.

**Usually pairs with.** `ambiguous-instruction`, `missing-context`, `scope-injection`,
`premature-parallelism`, `thread-overload`.

## `mechanical` — the model

**What it means.** The instruction was determinate — one reasonable reading, everything needed
present — and the model went outside it, or asserted something checkable and false.

**What the record must show.** Both halves, anchored:

1. That the instruction was determinate. This is the half people skip. You have to show the
   message did fix the thing that later went wrong, not merely that it existed.
2. Where the model departed from it: the output that does not follow from the instruction, or
   the claim the record itself contradicts.

**What is not mechanical.** A model doing something surprising with an instruction that turns
out, on a careful reading, to permit it. Test yourself: read the instruction as a stranger
with no idea what was wanted. If the model's reading is available to that stranger, this is
not a mechanical failure — the instruction admitted it.

Also not mechanical: work you disagree with but which the instruction did not exclude.

**This is the acquittal verdict**, and it exists because it is sometimes simply true. When the
record shows it, say it plainly and without hedging. A diagnostician that can only find one
kind of fault is not diagnosing.

**Usually pairs with.** `unverified-claim-accepted`, and occasionally `ambiguous-instruction`
where the record shows the model itself noticed the ambiguity and resolved it silently instead
of asking.

## `environment` — the tooling, the files, the limits

**What it means.** Something outside both parties failed or constrained them: a tool errored, a
file was not in the state either of them believed, earlier material fell out of view, a
capability was not available.

**What the record must show.** A direct trace, not an inference. One of:

- An `ACTION` and its `RESULT` where the result reports an error, and the failure follows from
  that result.
- A `RESULT` showing the world was not as either party believed — a file absent, contents
  different from what was assumed.
- An explicit statement in the record that a limit was reached.
- A demonstrable gap in what was visible: material established earlier in the conversation and
  plainly no longer being used, in a way the record itself shows.

**What is not environment.** "The model seemed to lose track" is not an environment finding, it
is a guess with a technical costume on. If you cannot point at the mechanism in the record,
this is not your verdict — it may well be `undetermined`.

This verdict is under-used, because tool failures are unglamorous and often several turns
upstream of anything interesting. Check the `RESULT` channel for errors before you conclude
anyone made a mistake.

**Usually pairs with.** `stale-constraint`, `missing-context`.

## `mixed` — more than one, and you still name which came first

**What it means.** Two or more independent causes were each necessary. Remove either and the
failure does not happen in the form it did.

**What the record must show.** That they really are independent: each one survives the other's
removal under the but-for test. If removing one takes the other with it, you do not have a
mixed verdict — you have a cause and a symptom, and you should go back to the test.

**You still name one primary cause** in section 6. The tie-break, in order:

1. The one whose removal alone would have prevented the failure, if only one of them does that.
2. If neither alone suffices, **the earlier one** — the fault that was already in the air when
   the second arrived.

**What is not mixed.** A reluctance to choose. `mixed` is a finding about the record, not a
diplomatic setting. If one candidate clearly survives the but-for test better than the other,
that is your primary cause and the other is a contributing factor — which is where most
"mixed" impulses actually belong.

## `undetermined` — the recorder does not support a finding

**What it means.** The record genuinely admits more than one cause and contains nothing that
chooses between them.

**What the record must show.** The reason it cannot say, named specifically. In practice:

- The surface is in your window but the origin is not — the work continues from an earlier
  session or from material referred to and not carried.
- The model's reasoning is missing exactly across the turns where the decision must have
  happened, and what it transmitted fits two different causes equally.
- The record forks, and the branches imply different causes with nothing showing which was live.
- The deciding material sits in an attachment or a tool result whose text the record does not
  carry.

**What is required alongside it.** Two things, both in section 5:

1. **The live candidates**, each anchored. An undetermined finding that lays out the two
   possible causes is a real result. A shrug is not.
2. **What would resolve it**, and it has to be obtainable: the earlier session, a record
   carrying the attachment text, the reasoning channel, the other branch. Evidence nobody could
   ever produce is not an answer.

**What is not undetermined.** A finding you would rather not write. Difficulty is not the same
as insufficiency. If the record supports a cause you can defend to the person reading it, name
it — reaching for `undetermined` to avoid an uncomfortable conclusion is the same failure as
reaching for a confident answer the record cannot carry, pointed the other way.

---

## Choosing between neighbours

| If you are torn between | Ask |
|---|---|
| `pilot-error` and `mechanical` | Read the instruction as a stranger who does not know what was wanted. Was the model's reading available to that stranger? If yes → `pilot-error`. If no → `mechanical`. |
| `pilot-error` and `environment` | Would the same instruction have worked if the tool had returned what it was supposed to? If yes → `environment`. |
| `mechanical` and `environment` | Did the model act on something false that it produced, or on something false that a tool handed it? Producer of the falsehood decides. |
| `mixed` and a ranked single cause | Apply the but-for test to each separately. If removing one removes the other, it is not mixed. |
| anything and `undetermined` | Can you state a counterfactual and check it forward against the record? If yes, you have a finding. If the record runs out before the check does, you do not. |
