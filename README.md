# orchestrator-flight-recorder

**You tell it what went wrong. You give it your Claude export, and it reads the black box:
the exact message where the fault entered, the path it travelled to the point you noticed,
and one probable cause, quoting your own conversation back at you. Then it stops — it never
rewrites your prompts and never hands you a fix.**

When a long working session with an AI goes wrong, the usual post-mortem is a list of
everything that looks bad. That is an audit, not a diagnosis. This is a diagnosis, borrowed
intact from air accident investigation: determine probable cause, rank the contributing
factors beneath it, anchor every claim to the recorder, and end the report at cause.
Recommendations are a different document, written later, by different people.

So it is not three things it would be easy to mistake it for. It is **not an audit** — you get
one cause, not a checklist. It is **not an editor** — it will not produce an improved version
of anything you wrote. It is **not a consultant** — there is no "next time, try this" in it
anywhere, and a script blocks one from being written.

---

## What you get back

A report in seven fixed sections, in this order, and nothing after the seventh.

1. **Incident statement** — your complaint restated in one line that names something findable
   in the record, so the scope of the investigation is fixed before it starts.
2. **Failure surface** — the message where the problem actually became visible, quoted.
3. **Causal origin** — the message where the fault entered, quoted. Usually not the same
   place, and sometimes it is an absence: a thing nobody ever said.
4. **Propagation trace** — the turn-by-turn path from origin to surface, plus the points where
   either side could have caught it and did not.
5. **Verdict class** — whose failure it was: yours, the model's, the environment's, a mix, or
   the record genuinely cannot say.
6. **Primary cause** — one sentence naming one mechanism, with contributing factors ranked
   beneath it, each pointing at a message.
7. **Counterfactual test** — the but-for check: *had message N said X, the failure at message M
   does not occur*, read forward against the record. This is what separates a cause from a
   symptom.

Every quotation carries the message number, who it belongs to, and which channel it came
from — what was said out loud, what the model was working out privately, what a tool did. That
last distinction matters more than it sounds: a report that quotes private reasoning as though
it had been spoken is describing a conversation that did not happen.

Three complete reports are in [`runs/`](runs/). Read one before deciding whether this is
useful to you.

---

## How to use it

### The no-code path

Nothing to install. Nothing to run.

1. Drop the [`diagnostician/`](diagnostician/) folder into a Claude project. That folder is the
   whole tool and it is self-contained — nothing inside it points anywhere outside it.
2. Paste your incident statement. A line or two, the way you would say it to a colleague:
   *"It rewrote a file I told it to leave alone."* *"Four hours in it was confidently building
   the wrong thing."* You do not need to know the cause — finding it is the job.
3. Attach the record. Your export's `conversations.json`, or just the single conversation that
   went wrong, or a plain copy-pasted transcript. Numbered messages in order is the only real
   requirement, because the report cites message numbers and without them nothing can be
   checked.

Optionally tell it where you think it went wrong. That gets recorded as your hypothesis and
tested last, like any other hypothesis, and you will be told plainly if the record does not
support it.

### The full path

Three steps, and the third is the one that makes the difference.

```bash
# 1. Turn the export into a numbered message manifest, windowed to the incident
python parse.py conversations.json --list                    # what is in the export
python parse.py conversations.json --uuid <uuid> --messages 42-47 \
       --include-tool-io --include-attachments \
       --out manifest.md
python parse.py conversations.json --uuid <uuid> --messages 42-47 \
       --include-tool-io --include-attachments \
       --json --out manifest.json

# 2. Run the diagnostician on that manifest, in a project holding diagnostician/
#    Give it the manifest and your incident statement. It produces report.md.

# 3. Check the report against the record it claims to have read
python check.py report.md --manifest manifest.json
```

Python 3.9 or newer — the oldest version CI tests — standard library only, nothing to install.
`python parse.py --help` and `python check.py --help` list every option.

**Why bother with the parser.** Message numbering, quote matching and counting are mechanical
work, and mechanical work belongs in a script rather than resting on a model's diligence. The
parser also does three things a pasted transcript cannot: it keeps the channels apart, so
private reasoning can never be quoted as speech; it counts how much of the reasoning channel
actually survived into the export and prints that at the top, so a gap is stated as a gap; and
it detects forks — messages you edited, replies you regenerated — which read as someone
repeating themselves if you take the export's flat list at face value.

**Why bother with the gate.** `check.py` refuses a report that breaks the guarantee: a quotation
that is not verbatim in the manifest, more than one primary cause or none, a verdict outside the
five, a contributing factor with no message anchor, a missing counterfactual, anything written
after it, a failure mode that has no file, or a prescription. It exits 1 and names the rule. A
*must* in markdown is a request; a *must* in code is a constraint.

---

## Getting your export

In Claude: **Settings → Privacy → Export data**. You will be emailed a link to a zip; unzip it
and use the `conversations.json` file inside. It holds your conversations as structured data —
every message, in order, with timestamps, and, where Claude recorded it, the model's own
reasoning.

One thing worth checking before you assume the session you want is in there: **exports arrive as
batches of recent history, not as your whole account.** The export used to build this repo
covered an eight-day window, and sessions from a few weeks earlier were simply absent from it. A
later request produced a different range. Look at the date span of what you get first.

---

## The three shipped runs

Three real investigations, run blind on a genuine export of genuine working sessions, shipped
whole — report, the record it read, the gate result, and an honest grading against something the
run could not see.

| Run | The complaint | Verdict | Mechanism | Gate |
|---|---|---|---|---|
| [1 — too complex, too fast](runs/01-too-complex-too-fast/) | a summary the reader could not follow, so the work stopped | `mechanical` | `vocabulary-mismatch` | PASS, 11 quotations |
| [2 — the two-hour job](runs/02-the-two-hour-job/) | a work order that ran 2h 14m against a plan that never priced it | `mechanical` | `uncosted-commitment` | PASS, 13 quotations |
| [3 — the wrong file](runs/03-the-wrong-file/) | a document delivered that was not the one asked for, and nothing flagged it | `pilot-error` | `ambiguous-instruction` | PASS, 7 quotations |

Runs 1 and 2 were graded against a message the investigation was never shown — the next thing
that was actually said in the session — which did not exist on disk anywhere when the run
happened. Run 3 has no such key, because the failure is stated inside its own window.

---

## On the verdicts

**The finding can go against you, against the model, against your tooling, or come back
undetermined. All four are real outcomes and all four ship as findings.** A diagnostician whose
verdict is the same every time is not diagnosing, it is a blame machine with a template.
"Undetermined" in particular is a result, not a shrug: it comes with the candidate causes the
record does admit and with what obtainable evidence would settle it.

The evidence that this is true here is not that the folder says so. It is that **both verdicts
predicted before the runs were wrong, in opposite directions.** The run expected to find against
the person cleared him. The run chosen specifically to demonstrate a finding against the model
indicted the person instead — and was shipped exactly as produced, not re-prompted and not run
again for a better answer. Across three blind runs the verdicts split two against the model, one
against the orchestrator, and neither split was the one planned. A verdict space that follows the
transcript rather than the plan is the only kind worth having, and this is what that looks like
when it costs you the demonstration you wanted.

Where each report came off worse is written down in its comparison note. Run 1 missed a
contradiction sitting inside its own window that the withheld message states outright; that miss
is the best evidence in this repo that the run was genuinely blind, and it is the reason one
entry exists in the accumulated profile.

---

## Checking it yourself

[`JUDGE_GUIDE.md`](JUDGE_GUIDE.md) has a sixty-second path with nothing installed, and then the
full battery. The short version:

```bash
python tests/verify.py        # the gate discriminates: clean reports pass, broken ones fail
python tests/parser-check.py  # the parser reads the record correctly and repeats itself
```

`verify.py` asserts three clean reports pass, twenty-one deliberately broken ones are each
rejected on the one check they were built to break and on nothing else, every check the gate can
report has a fixture behind it, and eight invocations that would examine nothing refuse to exit
0. Both suites run on every push, on Linux and Windows. Neither touches a real export; CI has
none.

[`OPEN-DEFECTS.md`](OPEN-DEFECTS.md) lists what is weak, unproven or out of scope. Read it
before you trust anything here.

---

## Privacy

**Your export never belongs in version control.** It is the most sensitive file you own — every
conversation you have had, in full. This repo's `.gitignore` has covered the export files since
the first commit, `out/` is ignored so manifests you generate locally stay local, and CI fails
the build if any raw export file is ever tracked.

Only windowed, swept excerpts ship in `runs/`. The redaction is done by rule rather than by
reading — `parse.py --redact` applies a rules file on the way *into* the manifest, and the
manifest header prints what each rule replaced, including rules that matched nothing. Each run's
notes record exactly what was swept and why.

If you run this on your own export, keep that arrangement, and check `git status` before you
commit anything.

## Layout

```
diagnostician/     the deliverable: drop this folder into a Claude project
  identity.md        who the investigator is
  rules.md           how it works: evidence, cause vs symptom, when to stop
  examples.md        three real investigations, including where they went wrong
  reference/         nine failure modes, the report schema, the five verdicts
parse.py           export  ->  numbered message manifest
check.py           the gate: exit 1 on any broken guarantee
tests/             proves the gate discriminates and the parser repeats itself
runs/              the three real investigations, shipped whole
training-layer/    what three investigations of one orchestrator accumulated
build/             how this repo was built, and why — including its own failures
JUDGE_GUIDE.md     verify the headline claims from a cold clone
OPEN-DEFECTS.md    what is weak, unproven, or out of scope
writeup.md         the build story
```

## Licence

Not yet chosen.
