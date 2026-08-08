# orchestrator-flight-recorder

**You tell it what went wrong. You give it the session's export. It reads the black box and
tells you why, anchored to your own words, and stops.**

When a long working session with an AI model goes wrong, the usual post-mortem is a list of
everything that looks bad. That is an audit, not a diagnosis. This is a diagnosis: one
probable cause, the exact message where the fault entered, the path it travelled to reach the
point where you noticed it, and nothing after that. No fixes, no rewrites, no "next time."

The investigator is an air accident investigator, and the discipline is borrowed intact:
determine probable cause, rank the contributing factors beneath it, anchor every claim to the
recorder, and end the report at cause. Recommendations are a different document.

> **Build status: in progress.** This README is a skeleton written at the first build stage
> and will be rewritten when the repo is finished. Right now the parser (`parse.py`) is built
> and working. The investigator folder, the enforcement gate and the worked examples are not
> finished yet — see *What exists right now* below. Nothing in this file claims a capability
> the repo does not currently have.

## What exists right now

| Piece | State |
|---|---|
| `parse.py` — turns a Claude data export into a numbered message manifest | **working** |
| `diagnostician/identity.md` — who the investigator is | **drafted** |
| `diagnostician/rules.md` — how the investigator works | not yet written |
| `diagnostician/reference/` — failure patterns, verdict classes, report format | not yet written |
| `check.py` + `tests/` — the gate that blocks fabricated quotes and prescriptions | not yet written |
| `runs/` — real worked investigations | not yet run |

## The parser

`parse.py` reads the conversations file from a Claude data export and produces a **message
manifest**: every message numbered, in order, with who said it, when, and what channel it
came through. Standard library only, Python 3.8 or newer. No install step.

```bash
# see what conversations are in your export
python parse.py conversations.json --list

# read one of them
python parse.py conversations.json --name "my-session" --out out/manifest.md

# just the stretch you care about (numbering stays the same as the full conversation)
python parse.py conversations.json --index 15 --messages 20-32 --out out/manifest.md
```

`python parse.py --help` lists every option.

### Why a parser instead of pasting the transcript

Message numbering, quote matching and counting are mechanical work. Mechanical work belongs
in a script, where it is the same every time, rather than resting on a model's diligence.
Running the same command over the same export twice gives you two byte-identical manifests.

The parser also does three things a pasted transcript cannot:

**It keeps the channels apart.** Each message in the export carries both a flattened `text`
field and a structured list of content blocks. They are not the same thing — the flattened
field splices the model's private reasoning together with the prose it actually sent, with no
marker between them. Anything built on that field can quote a thought as though it were a
statement. The parser reads the structured blocks and labels every segment: `SAID`,
`REASONING`, `ACTION` (a tool call), `RESULT`, `ATTACHMENT`.

**It tells you how much of the recording survived.** Exports do not reliably carry the
model's reasoning. Each manifest opens with a count: how many assistant messages have their
reasoning recorded in full, how many kept only a summary, and how many have none at all. A
gap in the recording is stated as a gap, never filled in by guesswork.

**It flags forks.** If a message was edited or a reply regenerated, the export keeps every
version in one flat list. Read linearly, a fork looks like someone repeating themselves —
which is a false trail an investigator would otherwise follow. The parser detects shared
parents and marks them.

### Getting your export

In Claude, open Settings → Privacy → Export data. You will be emailed a zip. Unzip it and use
the `conversations.json` file inside.

## Privacy

**Your export never belongs in version control.** It is the most sensitive file you own —
every conversation you have had, in full. This repo's `.gitignore` covers the export files
from the first commit, and `out/` is ignored too, so manifests you generate locally stay
local.

If you run this on your own export, keep that arrangement. Check `git status` before you
commit anything.

## Layout

```
diagnostician/     the deliverable: drop this folder into a Claude project
parse.py           export  ->  message manifest
check.py           the gate (not yet written)
tests/             proves the gate works (not yet written)
runs/              real investigations, shipped whole (not yet run)
build/             how this repo was built, and why
```

## Licence

Not yet chosen.
