# Training layer

A profile per person whose sessions have been investigated, built up from the real runs in
`runs/`. The idea is that the second investigation of the same person starts sharper than the
first: patterns that showed up before are known, and can be checked for early.

Populated in build stage M4, from real runs only.

**This ships populated or it does not ship.** A memory design that never ran is a diagram, and
a diagram of a learning loop is not a learning loop. If the runs do not produce real rows,
this folder and its claim come out of the repo rather than shipping empty.

## What is here

- [`AB.md`](AB.md) — built from the three investigations in [`../runs/`](../runs/). Six recurring
  patterns, each naming the runs it came from, each written as a check to run early rather than a
  conclusion to apply. It carries a section on what the three runs do **not** establish, because
  a profile of one person over eight days is a small evidence base and saying so is part of the
  claim.

One entry in it exists because an investigation *missed* something the answer key contained. That
is the loop working: the profile is written after the grading, not after the report, so what the
investigation failed to see is exactly what the next one is told to look for.

## The honest limit

The rows are real and every one names the runs it came from. The **write step is manual**: a
person writes the profile after grading a run against whatever the run could not see. Nothing in
this repository updates this folder automatically, and there is no code path from a report to a
profile. It is an accretion layer that accreted, not a mechanism that accretes. Recorded as
defect 7 in [`../OPEN-DEFECTS.md`](../OPEN-DEFECTS.md).

## The one rule

A profile says **where to look first**. It can never supply a finding. Nothing in it is anchored
to the record of a new session, so nothing in it may be cited in a report about one — the record
still has to say it. A profile that starts producing conclusions has become a way of deciding the
answer before reading the evidence, which is the failure this whole entry exists to diagnose.
