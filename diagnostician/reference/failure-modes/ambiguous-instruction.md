# Ambiguous instruction

**In one line.** An instruction that could reasonably be read more than one way; the model
picked one reading and carried on without ever saying that it had picked.

## What it is

Two or more readings of the same words were genuinely available. A careful stranger could have
gone either way. The model chose, and the choice never surfaced.

The ambiguity is not the failure. Ambiguous instructions are ordinary and mostly harmless,
because most of the time the reading is obvious from context or the model asks. **The failure is
the silent binding** — the moment a choice with real consequences gets made and left off the
transmitted record, so the only person who could have corrected it never learns there was
anything to correct.

That is also why it takes so long to surface. From the person's side, nothing looks wrong. They
said a thing, they got a reply that fits what they said, and the divergence only becomes visible
several turns later when the work has already been built on the wrong reading.

## What it looks like in the record

- **A referring expression with more than one candidate.** "The other one", "like before", "the
  same as last time", "that file", "the usual format", "it". Then look backwards: if two or more
  things in the window fit, the instruction was ambiguous at that point.
- **In the reasoning channel, where you have it:** the model weighing candidates and settling on
  one, with nothing corresponding in what it actually sent. A decision present in one channel and
  absent from the other is the strongest evidence this mode produces, and it is the single most
  valuable thing a full record can show you.
- **Without the reasoning channel:** the model's output commits consistently to one reading from
  a specific message onwards, and the earlier record contains at least two candidates it could
  have meant.
- **No reaction for several turns.** The person carries on normally, because on their reading
  everything is fine.
- **A late, disproportionate correction.** When it finally lands, the correction is much bigger
  than the message that caused it.

## Telling it apart

| Easily confused with | The question that separates them |
|---|---|
| `missing-context` | Count the candidates in the record. Two or more → ambiguous. **None** → the model had nothing to choose between and had to invent, which is missing context. |
| `scope-injection` | Was the disagreement about **which thing** or about **how much**? Which → ambiguous. How much → scope injection. |
| `stale-constraint` | Was the reading the model took one that used to be correct? If the record shows the world changing underneath a still-clear instruction, it is stale, not ambiguous. |
| `vocabulary-mismatch` | Who could not read whom? The model could not read the person → ambiguous. The person could not evaluate the model → vocabulary mismatch. |

## What rules it out

- **The model asked.** If it surfaced the ambiguity and the person chose, the binding was not
  silent. Whatever went wrong afterwards, look at the answer that was given.
- **Only one reading is actually available.** Read the instruction as a stranger who does not
  know what was wanted. If the model's reading is not available to that stranger, the instruction
  was determinate and the model went outside it — a different mode, and probably a different
  verdict.
- **The model bound it correctly.** An ambiguity resolved the right way is not the cause of a
  later failure, however conspicuous it looks once you know what happened.

## A note on the verdict

This mode usually sits under `pilot-error`, but not always, and the record can tell you which.
If the reasoning channel shows the model noticing the ambiguity, weighing it, and choosing not
to raise it, the failure is at least partly the model's — `mechanical` or `mixed`. If the model
never registered a second reading at all, the instruction did the work, and the verdict is the
person's.

---

*Example: REAL. A request for "a comprehensive Markdown file" admitted two documents: a narrow
project brief, supported by the words of the ask itself, and a wide knowledge base, supported by
the reason clause attached to it — that every future chat could get up to date from this file
because the fundamentals had all been discussed. A file that brings a new chat up to date on the
fundamentals has to contain the fundamentals, so the reason clause specified a larger document
than the ask did. The model bound the wider reading in the first line of its private reasoning,
without weighing the narrower one and without asking; the mismatch surfaced three messages later.
Verdict: `pilot-error`, because that reading was available to a stranger. Worked through in full
in `../../examples.md`, example 3.*
