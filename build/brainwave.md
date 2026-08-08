# brainwave.md — The Reasoning Behind the Shape

For downstream agents: inherit the why, not just the what.

## Why an accident investigator

The comp's bar (one primary cause, reasoning shown, cause not symptom, no fix, stop) is not a
rule we impose on a persona; it is the actual professional discipline of accident
investigation. Probable cause plus ranked contributing factors is the literal structure of an
accident report. "The report ends at cause; recommendations are a different document" is why
no-prescription is correct in-domain rather than an arbitrary constraint. Pilot error vs
mechanical failure gives us the acquittal verdict for free. The export JSON is genuinely a
flight recorder: a complete, timestamped record of the flight, sometimes including the
cockpit voice channel (thinking blocks). The persona is load-bearing, not costume, and it
sits on the orchestrator's own existing frameworks (The Airline, The Flight Recorder
pipeline), so it is his, which the community reads as authenticity.

## Why the causal origin / failure surface split is the core mechanic

A symptom inventory lists where things look wrong. A diagnosis finds where the fault entered,
which is almost never where it surfaced. The origin/surface split plus the propagation trace
is what makes the output structurally incapable of being an audit checklist: the trace is a
path, not a list. The counterfactual (but-for) test is the cause/symptom separator made
visible: "had msg N specified X, the drift at msg M does not occur" is reasoning a judge can
check, not a conclusion they must trust.

## Why the value ceiling is self-recognition

The most valuable possible output quotes the orchestrator's own sentence back and names the
mechanism: "You wrote 'make it work like before'. 'Before' had two referents in this
transcript, msg 14 and msg 31. The model bound it to the wrong one silently. Drift begins in
the next reply." Nobody argues with their own words. This is why the fabrication check
matters beyond honesty: the entire persuasive force of a report rests on the quotes being
real, so a fabricated quote is not a small defect, it is the whole product failing.

## Why the verdict space must acquit

A diagnostician whose every verdict indicts the person asking is a blame machine and would
also be wrong: sometimes the model hallucinated, sometimes the environment broke, sometimes
the record cannot say. Undetermined-with-what-would-resolve-it is a real investigative
outcome and shipping it as a legitimate path is an honesty feature the field will not have.
The acquittal run (mechanical verdict) is mandatory evidence, not optional.

## Why this entry has REAL evidence and #9 could not

#9's named weakness: no genuine user existed, every run was constructed. Here the genuine
user is the builder, the failure corpus is his real export, and the flagship incident has an
independent answer key: the #9 build journal, which named the jargon stall, its cause, and
its lesson before this entry was conceived. That is the strongest evidence shape available:
a real incident, a real record, and a ground truth written by a different process at a
different time. The comparison note must be honest in both directions, including where the
diagnostician misses or diverges from the journal; a perfect match would be suspicious and a
divergence honestly logged is evidence the run was blind.

## Why the recursion is worth surfacing

The diagnostician's first case is the session that built its predecessor, and the
training-layer's first orchestrator profile corresponds to a profile the journal already
drafted by hand. The methodology examining itself, with receipts, is precisely what this
community's judges built the competition to teach. Surface it in writeup.md, not in the
diagnostician itself (the tool must work for a stranger with no knowledge of #9).

## Why we skipped a diagnostic pass on the #9 repo

The journal's handover section already names what to lift (machinery) and what not to
(domain layers). Re-deriving known information is itself one of our failure modes
(missing-context's inverse: context existed, was written down, and re-derivation would have
ignored it). The decision is also a demonstration of the lesson.

## Why parse.py is honest about thinking content

Exports do not reliably carry assistant reasoning. Where present, the trace may use it
("the reasoning at msg 40 shows the model resolving the ambiguity silently instead of
asking"). Where absent, the report says the reasoning channel was not on the recorder.
Claiming insight into reasoning that is not in the record would be fabrication with extra
steps; stating the channel's absence is what a real investigator does with a missing
recorder.

## Why the deliverable is a subfolder

#9 lesson, learned late there and inherited early here: the drop-in folder must be
unmistakable and self-contained, so a judge's Claude project becomes the investigator rather
than a reader of build plans. Enforcement, runs, and the build record are evidence about the
deliverable, not part of it.

## The internal challenge

This build is itself an orchestration benchmark: minimum messages and prompts, maximum
quality, five manifests, two human gates. The build record (handover files) doubles as the
methodology demonstration the community scores. If this build fails somewhere, its own
export becomes a future test case, which is the correct relationship between a diagnostician
and its maker.
