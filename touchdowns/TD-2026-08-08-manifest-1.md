# Touchdown: manifest-1

date: 2026-08-08

window: Manifest 1 (Scaffold and parser)

prompt-received:
```
You are Manifest 1 of the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

FIRST, before anything else: confirm .gitignore exists at repo root and covers the raw
conversation export (the unzipped export files/folders and any *.zip). Run `git status` and
confirm no export file appears as tracked or untracked-to-be-added. If the export is exposed,
stop and fix .gitignore before proceeding. This repo will become public; the export must
never be committed.

Then read, in order:
  build/communitycompetitions.md
  build/spec.md
  build/plan.md
  build/brainwave.md

Execute Manifest M1 exactly as specified in build/plan.md (Scaffold and parser). The real
export is already unzipped inside this repo folder; locate it, inspect its schema by script
only (never load the raw JSON into your context), and build parse.py against what is actually
there.

Finish by writing build/handover/MANIFEST-1-COMPLETE.md in the format plan.md defines.
Commit and push your work (verify git status shows no export files first).
```

what-happened:
Ran the safety check first: `.gitignore` already covered all five export items and `git status`
was clean, with nothing export-shaped tracked or staged. Read the four seed files, then
inspected the export's schema with four throwaway scripts kept in the scratchpad, each
printing structure only — keys, types, counts, lengths, booleans — so no raw conversation text
entered the session. The inspection turned up the finding that shaped the parser: the export's
flattened `text` field splices the assistant's private reasoning into the prose it actually
sent, with no marker between them, so `parse.py` reads the structured `content` blocks instead
and labels every segment by channel. Built and tested the parser against all 43 conversations,
scaffolded the repo layout, drafted the investigator persona and two README skeletons, and
wrote the handover.

files-touched:
- created `parse.py` — deterministic export reader, stdlib only
- created `README.md` — root skeleton with an honest "what exists right now" table
- created `diagnostician/identity.md` — the investigator persona, no method (M2 owns that)
- created `diagnostician/README.md` — drop-in usage skeleton
- created `diagnostician/reference/failure-modes/README.md`, `tests/README.md`,
  `runs/README.md`, `training-layer/README.md` — scaffold placeholders naming their owning manifest
- created `build/handover/MANIFEST-1-COMPLETE.md` — the handover, including the full schema record
- created `touchdowns/TD-2026-08-08-manifest-1.md` — this file
- changed `.gitignore` — removed a stray placeholder line, added `out/` and Python noise

decisions:
- Parse `content` blocks, never the flattened `text` field — the flattened field merges
  reasoning into speech, so a report built on it could quote a thought as a statement.
- Label segments SAID / REASONING / REASONING-SUMMARY / ACTION / RESULT / ATTACHMENT — the
  origin/surface split needs those kept apart.
- Flag forks rather than reconstructing a main path — picking a branch is a judgment call and
  M1 has no mandate for judgment calls.
- Global message numbering under windowing — M4 ships windowed excerpts and "message 26" must
  mean the same message in both.
- No wall-clock in the output; provenance by export sha256 — otherwise "same input, same
  manifest" is false.
- `--json` is the machine contract for check.py; markdown is for reading.
- Tool IO and attachment text not inlined by default, presence always recorded.
- No generated manifest committed — excerpts are the human's call at the M4 gate.
- `identity.md` gets persona only — M1's guardrail is no rules substance.

friction:
- Two real bugs, both found by testing rather than by reading. First, message text was wrapped
  in a fixed ``` fence; these transcripts are full of code blocks, so content closed the fence
  early and corrupted the manifest from that point on — 46 opening fences against 69 bare
  closes. Fixed by sizing the fence to one backtick longer than the longest run in the body.
  Second, `parse.py users.json --list` succeeded and reported "1 conversation" instead of
  failing, because `users.json` is also a JSON list; the input is now shape-checked, not just
  syntax-checked. An empty manifest that looks like a finding is worse than a crash.
- A missing input file dumped a raw traceback rather than an error message. Fixed.
- Console output on this machine is not UTF-8, so an em dash came back mojibaked in an early
  inspection run. Worked around by writing all parser output to files with an explicit
  encoding rather than reading it off stdout.
- The seed `.gitignore` had `touchdowns/nothing        # placeholder line, ignore this, see
  step 2` on its last line. `#` only starts a comment at the start of a line, so that was a
  live pattern with a comment glued to it, not a comment. Harmless in effect; removed.
- A third bug, found only because a scout session's touchdown appeared in the working tree
  mid-session and warned that console encoding needed handling "at source, not
  per-invocation". Reproduced it: printing a manifest without `--out` dies with
  UnicodeEncodeError on a `→` after several thousand lines, which reads like a parser bug
  rather than a terminal one. Fixed by forcing UTF-8 on stdout and stderr. Worth noting that
  this was the one defect testing did not find on its own — every earlier test wrote to a
  file, which set the encoding explicitly and hid the problem.
- Unresolved, and the one worth carrying: the export covers 2026-08-01 to 2026-08-08 only, and
  no conversation in it matches the #9 build session that M4's flagship incident and its
  independent answer key depend on. The scout confirmed this independently and established
  that export batches are incremental rather than cumulative, so the late-July transcripts are
  not merely unfound but absent. The #9 journal *is* in the export, as prose read into a chat
  by a tool call — that is the answer key, not the incident. Logged as open question 1 for the
  human at the M4 intake gate. It needs deciding before M4 starts, not during it.

state-left:
M1 is complete and pushed to `main`. `parse.py` runs clean against the real export: all 346
messages across all 40 non-empty conversations render without a crash, byte-identically across
repeated runs, with balanced code fences and every error path returning a usable message. The
scaffold is in place with placeholder READMEs; `diagnostician/identity.md` is drafted and
promises that `rules.md` and `reference/` hold the method, which M2 must now make true. The
raw export remains untracked and ignored, and no generated manifest was committed — all test
output went to the scratch directory. M2 can start immediately: it reads
`build/handover/MANIFEST-1-COMPLETE.md`, then the four seed files. Open question 3 (whether and
how the investigator may quote the reasoning channel) is M2's to answer; open question 1 (the
missing flagship session) is the human's.
