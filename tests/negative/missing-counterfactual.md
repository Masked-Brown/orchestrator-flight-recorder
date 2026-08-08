# Investigation: dashboard and report page built on different grids

*NEGATIVE fixture — deliberately broken, and expected to fail the gate on `counterfactual-missing`.*
*The but-for reasoning is absent, so nothing separates cause from symptom.*

    record         synthetic-grid-mismatch (CONSTRUCTED fixture)
    source-sha256  b8a439f55d6acbdc153fa1063e04bd1667eb412365ee8215faca510fb1d73133
    window         messages 1-10 of "synthetic-grid-mismatch"

## 1. Incident statement

The dashboard was rebuilt on the v2 grid while the report page stayed on the v1 grid, and
the two stopped matching; first visible at msg 9.

Reporter's hypothesis: none offered.

## 2. Failure surface

Where the mismatch is first raised, msg 9 (human, SAID):

> the dashboard looks nothing like the report page

The state of the work at that point, msg 10 (assistant, SAID):

> The dashboard is on the v2 grid and the report page is on the v1 grid, so they do not match.

Naming the surface is not the diagnosis. It is the fixed point the rest is measured from,
and it sits four messages downstream of where the fault entered.

## 3. Causal origin

The instruction that admitted two readings, msg 5 (human, SAID):

> make the dashboard work like before

Both readings were already on the record when this was written. The layouts were named
together at the start, msg 1 (human, SAID):

> There are two layouts in this repo: the v1 grid and the v2 grid. Build the report page on the v1 grid.

So at msg 5 the word before had two available referents: the v1 grid, in use for the report
page since msg 2, and the v2 grid, named at msg 1 and not since used. Nothing between msg 1
and msg 5 fixes which one is meant. Where the model worked that out for itself, msg 6
(assistant, REASONING):

> Before could mean the v1 grid we used for the report page, or the v2 grid the rest of the app is on. [...] The v2 grid is newer, so I will use that.

## 4. Propagation trace

- **msg 5 (human, SAID)** — the instruction enters with two available referents and nothing marking which is meant
- **msg 6 (assistant, REASONING)** — the ambiguity is recognised and settled on one referent, on a channel no one else could read
- **msg 6 (assistant, SAID)** — the chosen grid is transmitted as work in progress rather than as a choice between two candidates
- **msg 8 (assistant, SAID)** — the choice is carried through the rest of the dashboard
- **msg 9 (human, SAID)** — the two pages no longer match, and the fault becomes visible

Missed catch points:

- **msg 7 (human, SAID)** — the grid selected was on the record one message earlier at msg 6 (assistant, SAID), on the channel both parties could read, and the reply carried the work forward without addressing it

## 5. Verdict class

Verdict: pilot-error

Read by someone who knew only what was on the record, msg 5 admitted both readings, and the
record contains no earlier message that closes it.

The two neighbouring classes were checked against the window before settling here.
`mechanical` would require the instruction to have been determinate and the model to have
departed from it; it was not determinate, because msg 1 puts both grids on the record and
nothing between msg 1 and msg 5 chooses between them. `environment` would require a tool or
context failure in the path from origin to surface; both tool calls in the window returned
without error, at msg 2 (assistant, RESULT) and msg 6 (assistant, RESULT).

## 6. Primary cause

Failure mode: ambiguous-instruction

The dashboard was built on the wrong grid because msg 5 identified its target by reference
to a previous state that the record admits two readings of.

Contributing factors:

1. The ambiguity was resolved on a channel nobody else could read, so the binding was never put where it could be confirmed or corrected — msg 6 (assistant, REASONING)
2. The transmitted reply named the grid being used but not that a selection between two candidates had been made — msg 6 (assistant, SAID)
