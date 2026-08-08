# Comparison: the report against what this run was expected to show

**REAL.** There is no answer key for this run — the failure is stated by the orchestrator
himself inside the window, so there was nothing downstream to withhold. What this run is graded
against instead is the expectation recorded for it before it happened, and it did not meet that
expectation.

## What was expected, and what happened

The build's intake chose this incident for one reason, stated plainly and in advance:

> the verdict here should NOT be pilot-error. This run exists to demonstrate the verdict space
> can find against the model. If the blind run indicts the orchestrator anyway, ship it as-is
> and discuss it honestly in the comparison note; do not steer the run.

The run returned **`pilot-error`**.

It is shipped exactly as produced. The run was not re-prompted, not nudged toward another
verdict, and not run twice to get a better answer. This note exists because that instruction
anticipated this outcome, and honouring it is worth more than the demonstration it cost.

## Was the verdict right?

The relevant standard is not a matter of taste. `verdict-classes.md` gives one tie-break for
this exact pair:

> Read the instruction as a stranger who does not know what was wanted. Was the model's reading
> available to that stranger? If yes → `pilot-error`. If no → `mechanical`.

The report applies that test explicitly and answers it: *That reading is available to a stranger,
so the model did not depart from a fixed instruction.* It supports the answer by quoting the
request in full and reading both bindings out of it — the narrower one from *of our end
conditions* and *the point we're at*, the wider one from *basically just like a knowledge file*,
from *fully comprehensive*, and above all from the reason clause, that every chat can get up to
date from this file *because we've discussed kind of all of the fundamentals and the foundations
as to what every chat is going to build off*. A file that lets a new chat get up to date on the
fundamentals has to contain the fundamentals.

It also ran the check `verdict-classes.md` makes mandatory before writing `pilot-error` — write
down what `mechanical` and `environment` would each require here, and go and look. Both are in
section 5, refused with anchors: `mechanical` because the request was not determinate in the
first place, `environment` because every `RESULT` in the window reports success and every shell
call returns zero.

There is one route to `mechanical` the report closes off correctly. `verdict-classes.md` allows
that verdict with `ambiguous-instruction` in one circumstance: *where the record shows the model
itself noticed the ambiguity and resolved it silently instead of asking.* The reasoning channel
at message 6 is recorded in full, which is exactly where that noticing would have to appear, and
the report reads it and reports that it is not there — the first thing the reasoning does is fix
the file's job, and nothing in the channel weighs a second, narrower document. Had the model
weighed the two readings and picked one without asking, this would have been `mechanical`. It
did not weigh them.

**So the verdict follows the method as written.** The expectation, not the run, is what turned
out to be wrong.

## The alternative reading, stated fairly

The strongest case against the report is not that the instruction was determinate. It is that
`mixed` was available and was dismissed a little quickly.

One message earlier the model had delivered a long HTML document over the same material, and the
file it then wrote describes itself, in its own opening lines, as *same content, presentation
format*. An investigator could argue that producing a second comprehensive document over
material already covered is a departure no reading of the request compelled, and that this is
independently causal alongside the under-determination.

The report considers `mixed` and refuses it on the but-for test, holding that the other things
that went wrong *shaped how long it stood, not that it happened*. That is a defensible
application of the test. It is not the only defensible one. Recorded here so the reader can
disagree with the report on the evidence rather than take it on trust.

## What this cost, and what it did not

**What it cost.** This run was the designated demonstration that the verdict space can acquit
the person steering, and it did not deliver it.

**What it did not cost.** The demonstration happened anyway, one folder over.
[Run 1](../01-too-complex-too-fast/report.md) returned `mechanical` — blind, on a real incident,
with the acquittal argued against its neighbours rather than assumed. The acquittal arrived in
the run that was not designed to produce one, and the indictment in the run that was.

That is better evidence than the plan would have produced. A verdict space that acquits when the
build wanted an acquittal proves very little. One that indicts where the build hoped for an
acquittal, and acquits somewhere the build was not looking, is a verdict space that is reading
the record rather than the room.

## What the report found that no expectation had framed

**The delivery was opaque, and that is why it stood for two turns.** The report's first
contributing factor is that message 6 announced the finished document by its structural
properties — *11 sections, canonical, versioned, with a change log* — and never by what was in
it. Nothing on a channel the orchestrator could read named the document's subject, which is why
the mismatch took until message 9 to surface.

**A properly built absence claim.** The report searched messages 5 to 8 across every channel the
manifest carries for any statement naming which of the two documents was wanted, or any question
asking, and reports there is none — then anchors where the absence bit, at message 7, where the
orchestrator commits to attaching the file to every spawned chat without ever having said what
it should contain.

**The model was faithful to the reading it took.** Section 7 reads forward and shows the rest of
message 6 executing that binding correctly, down to catching and fixing 59 em-dashes against a
style constraint it was operating under. That matters: it separates *chose the wrong document*
from *worked badly*, and only the first is the finding.
