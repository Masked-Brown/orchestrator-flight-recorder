# Stale constraint

**In one line.** A rule that was right for an earlier situation, carried forward after the
situation changed, without anyone stopping to re-decide it.

## What it is

The constraint is not missing and it is not unclear. It is **obsolete**. Someone set it for good
reasons, the ground it stood on moved, and it went on being obeyed.

Stale constraints are hard to see precisely because they were correct when written. Both parties
remember agreeing to them. Neither has any reason to look at them again, and the record shows a
model behaving perfectly consistently with an instruction you can find and quote — which reads,
on a quick pass, like everything working.

They arrive most often through carried material: a pasted specification, a handover from an
earlier session, a standing set of instructions, a plan written before the work started.

## What it looks like in the record

- **An early message sets a rule with reasons attached to a state of affairs** — a file layout, a
  tool being used, a limit, an approach, an environment.
- **The record then shows that state of affairs changing.** A tool result revealing different
  file state. A decision to switch approach. A new plan superseding an old one. A capability
  turning out to be available or unavailable.
- **After the change, the old rule is still being applied**, often by both parties, and nobody
  re-opens it. There is no message anywhere saying "does that still hold?"
- **The behaviour traces cleanly to an instruction that no longer matches the world.** If you can
  quote the rule, and quote the change, and show the rule still operating after the change, you
  have this mode.
- Frequently the rule sits in an attachment rather than in anyone's typed message.

## Telling it apart

| Easily confused with | The question that separates them |
|---|---|
| `missing-context` | Search for the constraint. If you find it in the window, it is stale, not missing. Missing context is about something that was never there; this is about something that is there and out of date. |
| `ambiguous-instruction` | Is the rule unclear, or clear-but-wrong-now? One reading applied to a changed world → stale. |
| `scope-injection` | Did the **job** change size, or did the **ground under the job** change? Job → scope injection. Ground → stale constraint. |
| `premature-parallelism` | Was the problem an old rule still in force, or new work started on unfinished foundations? |

## What rules it out

- **The constraint was re-examined and deliberately kept.** If the record shows anyone looking at
  it again after the change and choosing to keep it, it is not stale. If keeping it was wrong,
  the origin is that re-decision, and you should be quoting the message where it was made.
- **The situation never actually changed inside the window.** Then the constraint is current,
  whatever anyone now thinks of it, and applying it is not the fault. You need the change on the
  recorder, not in hindsight.

## A note on the verdict

Stale constraints often sit under `environment` rather than `pilot-error`, because what changed
was usually the world rather than anyone's judgment — a tool, a file, a limit. Check the tool
result channel for the moment the ground moved before assuming anyone made a mistake.

---

*Example: none yet. No shipped investigation has landed on this mode, so there is no real
case to show and none is invented here. The three modes that do have one are worked through
in `../../examples.md`.*
