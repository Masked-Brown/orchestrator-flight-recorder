# Premature parallelism

**In one line.** New work started before existing work was finished and checked, so nothing quite
lands and mistakes in the unfinished parts get built on.

## What it is

A failure of **ordering**. Things are being produced faster than they are being confirmed to
work, and each new strand is founded on something nobody has verified.

It feels like speed, from inside. Every new strand is visible progress and the session looks
productive right up to the point where the first unverified thing turns out to be wrong — at
which stage the correction has to be applied in four places, because it has already been reused.

Either party can start this. A person opening a second task while the first has produced nothing
confirmed, and a model beginning the next piece before the previous piece has been run, are the
same mode.

## What it looks like in the record

- **Strand B opens while strand A has no confirmed output.** Mark where each piece of work starts
  and where it is first shown to work. In this mode the starts get ahead of the confirmations and
  stay ahead.
- **Something produced and then immediately built upon**, with no run, no check, and no
  acknowledgement from either party in between — just a move to the next thing.
- **In the tool channels, where you have them:** a run of creations with no executions between
  them; things written, then written on top of, before anything is tried.
- **Corrections arriving late and landing in several places at once.** This is the clearest
  downstream signature, because it shows how far the unverified thing had already spread.
- **Explicit forward references to work that has not been done yet**, treated as though it has.

## Telling it apart

| Easily confused with | The question that separates them |
|---|---|
| `thread-overload` | **Order** or **count**? Parallelism is about starting before finishing — it can happen with only two strands. Overload is about the number of unresolved items, and can happen on a single thread. Ask whether things are being started too early or merely accumulating. |
| `unverified-claim-accepted` | Was the unverified thing a **statement** or a **piece of work**? An assertion taken on trust → unverified claim. A deliverable built on before being checked → premature parallelism. |
| `scope-injection` | Was the extra work part of the job, begun too early (parallelism), or not part of the job at all (scope injection)? |
| `stale-constraint` | New work on unchecked foundations, or an old rule still in force over changed ground? |

## What rules it out

- **The strands were genuinely independent.** If nothing in the later work depended on the
  earlier work, doing them at once did not cause anything. Show the dependency or drop the mode.
- **The earlier work was verified.** If the record contains the run, the check, or a confirmation
  from either party, it was not premature. Look for it before you claim it is absent.
- **The failure is in one strand and has nothing to do with the others.** Then the ordering was
  not load-bearing, and you are looking at whatever went wrong inside that strand.

---

*Example: none yet. Worked examples are added from real investigations.*
