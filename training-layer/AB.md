# Orchestrator profile: AB

**REAL.** Every line below is drawn from the three investigations in [`runs/`](../runs/), each
run blind on a genuine export. Nothing here is inferred from acquaintance, and nothing is carried
over from a session that was not investigated.

    investigations   3
    sessions         yt-wor-1.2-future-crons, nbs-wor-1.0-z,
                     AI voice training and qualitative reinforcement framework
    dates            2026-08-05 to 2026-08-08
    verdicts         mechanical, mechanical, pilot-error
    modes            vocabulary-mismatch, uncosted-commitment, ambiguous-instruction
    first built      2026-08-08 (build stage M4)

Read this before starting a fourth investigation of this orchestrator. It is a set of things to
**check for early**, not a set of conclusions to apply. Every entry names the runs it came from
so a future investigator can go and disagree with it.

---

## What recurs across the three

### 1. Constraints are set in adjectives, and adjectives cannot be checked

Across all three sessions the orchestrator states what he wants in qualitative terms and almost
never in a quantity. *Keep everything super simple*, *not too long*, *fully comprehensive*, *go to
hell and back on this*, *really educational*. Where a number does appear it measures his own
attention — a two-minute playtest, a ten-minute gate — never the machine's work.

This is the single most productive thing to look for, because it is upstream of two of the three
findings. An adjectival constraint has to be converted into some unit before anyone can act on
it, the conversion happens silently, and the unit chosen is where the failure enters. In run 2
*simple* was converted into prompt count, which is the one unit that does not bound elapsed time.

*From runs [1](../runs/01-too-complex-too-fast/training-table.md),
[2](../runs/02-the-two-hour-job/training-table.md),
[3](../runs/03-the-wrong-file/training-table.md).*

**Check first:** find the constraint, then find the unit the other party converted it into. The
gap between them is usually the origin.

### 2. Requests carry their reason in the same sentence, and the reason widens the request

He explains why he wants something as part of asking for it. That is ordinarily good practice and
here it is a specific hazard: the justification is often broader than the ask, and a careful
reader binds to the justification.

Run 3 is the clearest instance. The request was for a file *of our end conditions* — narrow — with
a reason clause attached saying every chat could get up to date from it *because we've discussed
kind of all of the fundamentals*. A file that brings a new chat up to date on the fundamentals has
to contain the fundamentals, so the reason clause specified a much larger document than the ask
did, and that is the one that was built.

*From run [3](../runs/03-the-wrong-file/training-table.md); the same shape appears in run 1, where
the request for a ruling arrives attached to the whole case for it.*

**Check first:** separate the ask from the reason attached to it and read them as two
specifications. If they disagree about size, the failure is usually already there.

### 3. He accepts the goods and disputes the cost

In every session where something went wrong, the deliverables survived review. Run 2: *I've done
the two-minute play test of v1.2. That's fine* — in the same message as the complaint. Run 1: the
four findings were never disputed, only their wording. Run 3 is the exception that confirms the
shape, and even there the objection is that the wrong document was produced rather than that the
document was bad.

*From runs [1](../runs/01-too-complex-too-fast/training-table.md),
[2](../runs/02-the-two-hour-job/training-table.md).*

**Check first:** ask whether the complaint is about what was built or about what it took. This
orchestrator's complaints are usually about the second, which routes an investigation away from
`scope-injection` and quality findings before any time is spent there.

### 4. The evidence needed to prevent the failure is often already in the window

This is the pattern that most changes how an investigation should be run, because it turns
omissions into findings.

Run 2: a measured run time for a comparable job, 27m 49s, sat in an attachment one message before
the uncosted order — pasted by the orchestrator himself. Run 1: the model had read both source
documents successfully before writing the summary that could not be followed. Run 3: the HTML
covering the same ground had been delivered one message earlier.

He pastes job output containing exactly the figures nobody then uses.

*From runs [1](../runs/01-too-complex-too-fast/training-table.md),
[2](../runs/02-the-two-hour-job/training-table.md),
[3](../runs/03-the-wrong-file/training-table.md).*

**Check first:** before concluding something could not have been known, search the window for it.
In these three sessions it was there twice.

### 5. Overload shows as action taken ahead of reading

**This entry exists because an investigation missed it**, and it is the most valuable line on this
page for that reason.

Run 1's answer key contains *I already ran 2B before I read through your whole response* — the
orchestrator fired the next job without finishing the message explaining it. The signal was
available in the window: message 11 says in consecutive sentences that work order 2B has been run
and that it is about to be run. The report quoted around that passage twice and never read it.

Behaviour is stronger evidence of overload than complaint is, and this orchestrator produces both.

*From run [1](../runs/01-too-complex-too-fast/comparison-note.md).*

**Check first:** read his messages for self-contradiction about what he has already done. Where a
message reports an action and then asks a question presupposing the action has not happened, that
is a load-bearing overload signal — quote it rather than eliding it.

### 6. He states pace and comprehension problems explicitly, and separately

He does not suffer in silence and he does not conflate the two complaints. Run 1's answer key
distinguishes *wording is much better in that last message* from *I'm happy that we've stabilized
this pace* as two separate clauses about two separate things. The surface message likewise names
one specific term he could not follow.

This makes him an unusually easy orchestrator to diagnose on register, and an unusually easy one
to over-read: because the complaint is explicit, the temptation is to stop at it. In run 1 the
complaint was accurate and still not the most interesting thing in the window.

*From run [1](../runs/01-too-complex-too-fast/training-table.md).*

**Check first:** take his stated complaint as a reliable pointer to the surface, and then keep
going. It has been right about where, and incomplete about what, in the one case there is a key
for.

---

## What the three runs do not establish

Stated so this profile is not read as more than it is.

- **Three sessions, one orchestrator, one eight-day window.** Two of the three are Claude Code
  build sessions of a similar shape; the third is a planning conversation. Nothing here is known
  to generalise to other kinds of work he does.
- **Two of the three verdicts are `mechanical`.** That is not evidence he rarely errs. It is three
  incidents, chosen by a human for a build, and the selection was not random.
- **Only one of the patterns above has been tested against evidence outside its own window** —
  pattern 5, which came from an answer key and was missed by the investigation. The rest are
  observations from the records the reports were built on.
- **Pattern 1 is the only one that appears in all three runs.** Patterns 3 and 6 rest on two runs
  and one run respectively.

## How this file is meant to be used

It is a set of first checks, and it is allowed to be wrong. An investigator who reads it and then
finds the record says otherwise should say so in the report and this file should change. A profile
that only ever accumulates is a profile that has stopped being tested.

What it must never do is supply a finding. Nothing here is anchored to the record of a *new*
session, so nothing here can be cited in a report about one. It tells you where to look first. The
record still has to say it.
