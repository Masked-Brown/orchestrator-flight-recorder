# Failure modes

One file per named way an AI working session goes wrong. Each file defines the mode, describes
what it looks like in a transcript, gives the tests that separate it from the modes it is easily
confused with, and — just as importantly — says what would rule it out.

The investigator names **exactly one** of these as the primary cause. A mode may not be invented
mid-report: if a session fails in a way none of these files covers, the file gets written first.

A mode says what mechanism produced the failure. It does not say whose failure it was — that is
the verdict, and it is decided separately. See `../verdict-classes.md`.

## The set

| Mode | In one line |
|---|---|
| [`ambiguous-instruction`](ambiguous-instruction.md) | An instruction with more than one reasonable reading; the model picked one silently instead of asking. |
| [`missing-context`](missing-context.md) | A fact or decision the model needed was never put in front of it, so it supplied one. |
| [`stale-constraint`](stale-constraint.md) | A rule set for an earlier situation, carried forward after the situation changed, without anyone re-deciding it. |
| [`vocabulary-mismatch`](vocabulary-mismatch.md) | An answer in words the reader cannot evaluate, so the check that would have caught the problem never happens. |
| [`thread-overload`](thread-overload.md) | Turns that are each fine but together open more questions than they close, until something gets dropped. |
| [`premature-parallelism`](premature-parallelism.md) | New work started before existing work is finished and checked. |
| [`scope-injection`](scope-injection.md) | The job quietly got bigger or smaller without the change ever being surfaced as a decision. |
| [`unverified-claim-accepted`](unverified-claim-accepted.md) | A confident explanation taken at face value when checking it would have been cheap. |
| [`uncosted-commitment`](uncosted-commitment.md) | Work agreed in full and set running with nobody stating what it would cost, so the party who set the budget had nothing to weigh. |

## Narrowing down

The fastest route to the right file is usually one of these questions. Each one splits the set
roughly in half; then read the two or three candidate files and use their own comparison tables.

- **Is the failure in one message, or in the shape of the sequence?** Sequence →
  `thread-overload`, `premature-parallelism`. One message → everything else.
- **Did the model have too many readings, or none?** Too many → `ambiguous-instruction`. None →
  `missing-context`.
- **Was the needed thing absent, or present and out of date?** Absent → `missing-context`.
  Present and old → `stale-constraint`.
- **Who could not understand whom?** The model could not read the person →
  `ambiguous-instruction`. The person could not evaluate the model → `vocabulary-mismatch`.
- **Was something believed that should have been checked?** → `unverified-claim-accepted`.
- **Is the job being worked on the job that was agreed?** → `scope-injection`.
- **Is the complaint about the goods, or about the bill?** The work itself is disputed →
  `scope-injection` and its neighbours. The work is accepted and its cost is the objection →
  `uncosted-commitment`.

If two modes still both fit after reading their files, that is usually a sign the but-for test
has not been finished. Go back to it: the mode you want is the one attached to the message whose
removal takes the failure with it.

## Adding a mode

The taxonomy is meant to grow. A new mode earns a file when a real session fails in a way none of
these describes — not when an existing one merely fits awkwardly.

A new file carries the same four things as the others: what it is, what it looks like in a
record, how to tell it apart from its nearest neighbours, and what would rule it out. The last
one is not optional. A mode that nothing can rule out will absorb every case it is offered, and a
taxonomy with a mode like that in it stops distinguishing anything.
