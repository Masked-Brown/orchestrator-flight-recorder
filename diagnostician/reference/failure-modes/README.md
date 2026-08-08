# Failure modes

One file per named way an AI working session goes wrong. Each file defines the mode, describes
what it looks like in a transcript, and gives the test that separates it from the modes it is
easily confused with.

The investigator names exactly one of these as the primary cause. A mode may not be invented
mid-report: if a session fails in a way none of these files covers, the file gets written
first.

Planned set (written in build stage M2):

- `ambiguous-instruction.md` — an instruction with more than one valid reading; the model
  picked one silently instead of asking.
- `missing-context.md` — a decision the model needed was never put in front of it.
- `stale-constraint.md` — a rule set for an older situation, carried forward after the
  situation changed, without anyone re-deciding it.
- `vocabulary-mismatch.md` — an answer written in words the reader cannot evaluate.
- `thread-overload.md` — turns that are each fine but together open more questions than they
  close.
- `premature-parallelism.md` — new work started faster than existing work is finished.
- `scope-injection.md` — the job quietly got bigger or smaller without anyone deciding it
  should.
- `unverified-claim-accepted.md` — a confident explanation taken at face value when checking
  it would have been cheap.
