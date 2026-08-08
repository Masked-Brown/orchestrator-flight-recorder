# The investigator — how to use this folder

Drop this folder into a Claude project. Claude becomes an air accident investigator for AI
working sessions: you show it a session that went wrong, and it tells you **why**, anchored to
what was actually said, and then stops.

This folder is complete and self-contained. Nothing in it depends on a file outside it, so
dropping it into a project is the whole installation. Where it mentions the wider project — the
parser, the gate, the shipped runs — those are useful, not required.

## What you give it

**1. What went wrong, in a line or two.** Plain words, the way you would say it to a
colleague. "It rewrote a file I told it to leave alone." "Four hours in it was confidently
building the wrong thing." You do not need to know the cause — finding it is the job.

**2. The session's record.** Best is a *message manifest*: the session's messages, numbered,
in order, with who said what and when. The `parse.py` script in the project this folder came
from produces one from a Claude data export. If you do not have a manifest, a plain
transcript works, as long as the messages are in order and numbered — the report cites
message numbers, so without them a finding cannot be checked.

**3. Optional: where you think it went wrong.** Say so if you have a hunch. It gets tested
like any other hypothesis, and it does not get special treatment. If the record does not
support it, you will be told.

## What you get back

A report in seven fixed sections:

1. **Incident statement** — your complaint restated in one line, fixing the scope.
2. **Failure surface** — where the failure actually showed up, quoted.
3. **Causal origin** — the message where the fault entered. Rarely the same place.
4. **Propagation trace** — how it travelled from origin to surface, turn by turn, including
   the points where either side could have caught it and did not.
5. **Verdict class** — was this the person, the model, the environment, a mix, or does the
   record genuinely not say.
6. **Primary cause** — one sentence, plus contributing factors ranked beneath it.
7. **Counterfactual test** — the but-for check: had message N said X, the failure does not
   happen. This is what separates a cause from a symptom.

The report ends there. That is deliberate.

**Everything in it points at a message.** Quotes are exact and carry the message number, who it
belongs to, and which channel it came from — what was sent, what the model was working out
privately, what a tool did. That last part matters more than it sounds: a report that quotes the
model's private reasoning as though it had been said out loud is telling you about a
conversation that did not happen.

## What it will not do

**It will not fix anything.** No rewritten prompts, no improved instructions, no "next time,
try." In accident investigation, cause and recommendation are two different documents written
at two different times, and mixing them is how you end up committed to a cause you never
proved. If you want the fix, that is a separate conversation — and you will be in a much
better position to have it.

**It will not blame you by default.** Sometimes the model failed. Sometimes the tooling did.
Clearing you is a legitimate finding and it will say so when it is true.

**It will not invent evidence.** Every quote comes from the record you supplied. If the record
cannot support a finding, the verdict is "undetermined", along with what evidence would have
settled it.

## What is in this folder

| File | What it is |
|---|---|
| `identity.md` | Who the investigator is and the discipline it works to |
| `rules.md` | How it works: standard of evidence, cause vs symptom, when to stop |
| `reference/failure-modes/` | The nine named ways these sessions fail, one file each |
| `reference/report-schema.md` | The seven sections, the citation format, and a template |
| `reference/verdict-classes.md` | The five verdicts and what the record must show for each |
| `examples.md` | Three real investigations, worked through — including where they went wrong |

## A note on the recording

Exports do not always carry the model's private reasoning. Where it survives, it is the best
evidence available, because it often shows a decision being made silently. Where it does not,
the investigator says so and works from what remains. It will not guess at reasoning that was
never recorded, and neither should you.
