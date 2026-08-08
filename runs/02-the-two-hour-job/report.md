# Investigation: the two-hour work order

    record         message-manifest.md
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575
    window         messages 42-47 of "nbs-wor-1.0-z"

## 1. Incident statement

The work order set out at msg 46 and fired by the reporter ran for 2h 14m 54s, against a plan
that contained no estimate of its run time anywhere; the overrun becomes visible at msg 47.

Reporter's hypothesis: none offered.

## 2. Failure surface

The complaint as it lands, msg 47 (human, SAID):

> Okay, cool, the job just finished. It took over two hours, which I'm not sure was what you had
> imagined. It's certainly not what I imagined, so I want you to tell me why and what went
> wrong, because I'm a bit confused as to why it took so long. That wasn't really part of the
> plan, so that's that.

The run's own account of itself, msg 47 (human, ATTACHMENT):

> ✻ Cogitated for 2h 14m 54s · 3 shells still running

What is not in dispute, in the same message, msg 47 (human, SAID):

> I've done the two-minute play test of v1.2. That's fine.

The work was accepted. The objection is to its cost.

## 3. Causal origin

The fault entered at msg 46, where the job was committed to in full and never priced.

The commitment, msg 46 (assistant, SAID):

> **In (one combined CC prompt):** the leak fix and clean re-runs, the honest re-wording of the
> two affected findings, confidence intervals on the ladder (one script, invalidates nothing),
> the CSS fix, your post-game stats breakdown, the accuracy grader, the composite score, and the
> next-steps file.

That message then sets out the order itself: eleven numbered items across three parts, plus a
five-point verification list.

**The absence.** I searched for any statement of what running that order would take — a figure, a
range, an order of magnitude, covering the eleven items as a whole. I searched every message in
the window, 42 to 47, in every channel this record carries: SAID, ATTACHMENT and
REASONING-SUMMARY. There is none. The reasoning channel is summary-only at msg 42 and msg 46 and
absent at msg 44, so the record cannot show whether run cost was weighed privately; the claim
here is about what was transmitted, which is the only channel the reporter could read.

The one cost figure attached to the order covers the first of its eleven items, msg 46 (assistant, SAID):

> Forty minutes of compute buys back full honesty.

Its source, and its scope, msg 45 (human, ATTACHMENT):

> 1. Before publish — leak-free expectimax versions (d2-v2/d3-v2, expectation or zero for
> next-merge-ready at leaves) and re-run both eval rows (~40 min at 6 workers). Gates F001's
> "strong" tier.

The other figures in msg 46 price the reporter's own attention rather than the run, msg 46 (assistant, SAID):

> 3. Your two-minute playtest of v1.2 when it lands.

Where the absence bit is the surface quoted in section 2: the reporter learned the cost from the
finished job.

## 4. Propagation trace

- **msg 46 (assistant, SAID)** — the fault enters: eleven numbered items are committed to in one
  order, presented under the session's simple-mode heading, with no figure anywhere for what
  running them costs; the only figure attached, forty minutes, covers the first item alone and
  stands where a total would.
- **msg 47 (human, ATTACHMENT)** — the fault surfaces as a bill: 2h 14m 54s, three shells still
  running, and every ordered item delivered — the attachment's closing note opens by stating that
  all eleven work-order items are done and verified.
- **msg 47 (human, SAID)** — the reporter measures the bill against the plan, finds no
  expectation to measure it against, and disputes none of the work.

Between msg 46 and msg 47 the recorder carries no turn at all — the timestamps are 2h 19m 39s
apart — so there was no message in which either party could have noticed the overrun while it was
happening.

Missed catch points:

- **msg 45 (human, ATTACHMENT)** — the pasted audit carried both a costing for its most expensive
  recommendation and, at its foot, the previous order's own run time of 27m 49s. Both were on a
  channel either party could read, and neither became a figure for the order that followed a
  minute later.
- **msg 45 (human, SAID)** — two further items were added into the same single prompt, one of them
  specified as fully comprehensive, without its size being asked about; the shape of that combined
  prompt had been set out at msg 44 on a channel the reporter could read.

## 5. Verdict class

Verdict: mechanical

The instruction was determinate on the thing that later went wrong, msg 43 (human, SAID):

> It's coming into multiple hours into the session now, so operator fatigue is starting to set in.
> I just want to keep things really simple from now on. I'm fine to sacrifice a bit of depth just
> to finish this game off.

and, at the end of the same message, msg 43 (human, SAID):

> Keep everything super simple, and hopefully we should be done in not too long.

That fixes pace as the governing priority and names depth as the thing to be traded for it. Only
one reading was in play, and the record shows the model receiving that reading and restating it in
its own words, msg 44 (assistant, SAID):

> Understood. Simple mode from here: minimum steps, no added depth, finish the game.

The departure is at msg 46: an eleven-item order was committed to under that constraint with no
measure of what it would cost to run, while the material for the measurement sat in the message
immediately before it — a costing of ~40 min for one recommendation, and the previous, smaller,
read-only order's recorded run of 27m 49s, both quoted above.

Not pilot-error: the reporter's messages fixed the constraint rather than leaving it open, and the
one thing they did not supply was a number — which was obtainable inside the session by asking,
and by the two comparable costings already on the recorder. The pilot-error class is reserved for
what the model needed and had no way to obtain.

Not environment: two environment problems are reported inside the run, msg 47 (human, ATTACHMENT):

> Two live-verification findings the tests wouldn't have caught: grading took over forty seconds
> in a backgrounded tab (Chrome throttles setTimeout there — now a MessageChannel), and that fix
> then hung node --test because a live MessagePort keeps Node's event loop alive.

The record does not quantify either, and the order was already uncosted before they occurred.

Not mixed: removing the omission at msg 46 removes the failure however the reporter's
contributions fall, so the two are not independent.

## 6. Primary cause

Failure mode: uncosted-commitment

The order at msg 46 was committed to without any statement of what running it would cost, leaving
the reporter a list of items to approve and no bill to weigh.

Contributing factors:

1. The order took in the audit's entire before-publish list on the model's own judgement,
   including new agent versions re-run across both eval rows and a full uncertainty analysis,
   neither of which the reporter had asked for — msg 46 (assistant, SAID)
2. The pace constraint was set in adjectives with no budget attached, so there was no number for
   the order to be checked against — msg 43 (human, SAID)
3. The remaining project had been fixed in counts of prompts and in minutes of the reporter's own
   attention rather than in run time — msg 44 (assistant, SAID)
4. Two further items were added into the same single prompt, one of them specified as fully
   comprehensive — msg 45 (human, SAID)
5. Two environment-specific problems inside the run added time the order could not have
   anticipated, in an amount the record does not state — msg 47 (human, ATTACHMENT)

The primary cause rests on the SAID channel throughout. The reasoning at msg 46 survives only as a
summary and nothing here relies on it.

## 7. Counterfactual test

Had msg 46 stated what the eleven-item order would cost to run, the surprise reported at msg 47
does not occur.

Reading forward from 46, msg 47 is the only message that follows, and its complaint is comparative
rather than absolute: the reporter objects to the distance between the plan and the outcome, and
accepts the work in the same breath. A figure at msg 46 gives that comparison something to land
on. The record shows both the willingness to cut and the machinery already running for it — the
willingness at msg 43 (human, SAID):

> I'm fine to sacrifice a bit of depth just to finish this game off.

and the machinery in the same message that carried the order, msg 46 (assistant, SAID):

> **Out (written into the next-steps file, not built):** everything touching rules or spawn odds
> (two-block preview, spawn sweeps), the clutch-rescue study, strand-risk ablation, RL baseline,
> leaderboard. Exactly per your no-rule-changes call.

Items were being moved out of the run and into a backlog file at that very message; a stated cost
gives that same filter something to act on.

This sits upstream of every factor above. Remove the primary cause — a figure is stated — and the
factors stop mattering: a large order, a plan counted in prompts, two added items and even the two
environment problems all land inside an expectation the reporter had accepted before firing, and
msg 47 disputes none of the work.

Remove any factor and the failure still arrives. Factor 2 is the strongest of them, and it fails
the test: nothing in msg 46 shows the order being measured against any number, and msg 46 carries
a cost figure for one item while still producing no total — so a budget stated at msg 43 would
have had nothing to bite on. Factor 1 fails it too: with the audit's items dropped, the order
still contains the browser grader, which is where both of the run's environment problems arose,
and it is still fired without a price. Factor 5 fails it for the plainest reason — the two
environment problems are unquantified in the record, and the commitment was already unpriced
before either of them happened.
