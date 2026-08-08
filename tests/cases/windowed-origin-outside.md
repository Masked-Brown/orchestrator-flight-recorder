# Investigation: dashboard grid change with its instruction outside the window

*CONSTRUCTED fixture. Written to exercise the gate against a record that is itself
constructed. Not a real session and not a finding about any person.*

    record         synthetic-grid-mismatch (CONSTRUCTED fixture)
    source-sha256  b8a439f55d6acbdc153fa1063e04bd1667eb412365ee8215faca510fb1d73133
    window         messages 6-10 of "synthetic-grid-mismatch"

## 1. Incident statement

The dashboard was moved to the v2 grid and stopped matching the report page; first visible
at msg 9. The window supplied begins at msg 6, after the instruction that prompted the
move.

Reporter's hypothesis: none offered.

## 2. Failure surface

Where the mismatch is raised, msg 9 (human, SAID):

> the dashboard looks nothing like the report page

The state of the work at that point, msg 10 (assistant, SAID):

> The dashboard is on the v2 grid and the report page is on the v1 grid, so they do not match.

## 3. Causal origin

The origin is upstream of the window.

What was searched for: the instruction that set the dashboard's target, and any statement
fixing which grid it was to match. Where: messages 6 to 10, in every channel this manifest
carries. The window opens with the choice already being made and never contains the
instruction that prompted it.

Where the model had to proceed without it, msg 6 (assistant, REASONING):

> Before could mean the v1 grid we used for the report page, or the v2 grid the rest of the app is on. They did not say which. The v2 grid is newer, so I will use that.

This locates the fault upstream without reaching it. The working-out at msg 6 refers to an
instruction, and to a report page built earlier, neither of which is on this stretch of the
recorder. Message numbers here are global, so the missing material sits at messages 1 to 5
of the same conversation.

## 4. Propagation trace

- **msg 6 (assistant, REASONING)** — an ambiguity that entered upstream is settled on one referent
- **msg 6 (assistant, SAID)** — the chosen grid is transmitted as work in progress
- **msg 8 (assistant, SAID)** — the choice is carried through the rest of the dashboard
- **msg 9 (human, SAID)** — the two pages no longer match

Missed catch points:

- **msg 7 (human, SAID)** — the grid selected was on the record one message earlier at msg 6 (assistant, SAID), on the channel both parties could read, and the reply carried the work forward without addressing it

## 5. Verdict class

Verdict: undetermined

The failure surface is in this window and the origin is not, which is the plainest form of
a record that cannot settle its own question. The working-out at msg 6 (assistant,
REASONING) establishes that an instruction existed and that it admitted two readings, but
the instruction itself is outside the window, so whether it was genuinely ambiguous or
whether a determinate instruction was departed from cannot be read off this record.

The candidates the record admits, both live:

1. The upstream instruction admitted both readings, and the fault is that it was bound without being raised — msg 6 (assistant, REASONING)
2. The upstream instruction was determinate and was departed from, in which case the working-out at msg 6 mischaracterises it — msg 6 (assistant, REASONING)

Would resolve it: messages 1 to 5 of the same conversation, which this manifest excludes
and which carry the instruction the working-out at msg 6 refers to.

## 6. Primary cause

Failure mode: ambiguous-instruction

Both live candidates run through the same mechanism at msg 6, where a target identified by
reference to an earlier state was resolved to one of two available readings.

Contributing factors:

1. The resolution happened on a channel nobody else could read, so the binding was never put where it could be corrected — msg 6 (assistant, REASONING)
2. The transmitted reply named the grid being used but not that a selection had been made — msg 6 (assistant, SAID)

The primary cause here rests on a reasoning channel with nothing in the transmitted record
corroborating what it refers to, because the material it refers to is outside the window.
That is thin ground and the verdict above reflects it.

## 7. Counterfactual test

Had the instruction referred to at msg 6 named which of the two grids the dashboard was to
match, the mismatch reported at msg 9 does not occur.

Reading forward from msg 6 on that basis: there is nothing left to resolve, so msg 6
(assistant, SAID) reports work on the named grid, msg 8 (assistant, SAID) carries that same
grid forward, and at msg 9 both pages sit on one grid. This is checkable within the window
even though the message it names is not, because the working-out at msg 6 records both
readings and the record shows which one was taken.

This is upstream of both contributing factors: remove the ambiguity and nothing is bound
silently at msg 6, and nothing goes unmentioned in the reply, because no selection occurs.
Remove either factor and the dashboard still moves to the v2 grid.
