# Touchdown: scout-export

date: 2026-08-08
window: scout

prompt-received:
```
You are the Scout for a project called orchestrator-flight-recorder. Your job is to find
candidate failure incidents in my Claude conversation export that would make strong public
test runs for a diagnostician that traces AI-session failures back to orchestrator
(human) behaviour.

INPUT
The export zip is at:
C:\Users\alexa\Downloads\data-ad34491b-3694-4872-9284-1e46d1313908-1786205438-c37d0405-batch-0000.zip

SETUP
1. Create a working folder at C:\Users\alexa\Downloads\ofr-scout\ and extract the zip there.
2. Locate conversations.json. Do NOT read the raw JSON into your context. Write a Python
   script to parse it and inspect the schema first (top-level keys, message structure,
   whether assistant thinking/reasoning content is present or only final text). Record the
   schema in your report, because the project parser will be built against it.

WHAT TO SCAN FOR
Write Python that walks every conversation and scores it for failure signals. Signals, in
rough priority order:
- Explicit orchestrator frustration or correction: "that's not what I meant", "you ignored",
  "I said", "wrong", "no.", "start again", "why did you", profanity aimed at output.
- Repeated re-instruction: the human restating the same requirement 2+ times in one chat.
- Overload or consolidation signals: "slow down", "lagging behind", "too many threads",
  "consolidate".
- Abandonment: long build chats that stop abruptly after a correction.
- The human accepting a confident claim that is later shown wrong in the same chat.
For each signal hit, capture the conversation name, date, message index, and a verbatim
excerpt of the surrounding 2-3 messages (trimmed to what is needed to see the pattern).

SPECIFIC KNOWN INCIDENTS
Also search directly for two incidents I already know about, from a build in late July 2026
(a competition entry called hod-review, Head of Department lesson editor):
- A stall where a review report used untranslated internal jargon. Search terms: "no-anchor",
  "hard blocks", "not got a fucking clue", "lagging behind", "explain those in English".
- An incident where a confident explanation for a discrepancy between two test counts was
  offered and later found wrong by checking the code. Search terms: "test count",
  "discrepancy", "verify", "check the code".
Flag these two separately if found, with conversation name and message indices.

OUTPUT
Write C:\Users\alexa\Downloads\ofr-scout\scout-report.md containing:
1. The export schema summary (including whether thinking content exists).
2. The two known incidents, if located, with excerpts.
3. A ranked shortlist of the top 8 other candidate incidents. For each: conversation name,
   date, size, the signal excerpts with message indices, a one-line hypothesis of the
   failure mode (e.g. ambiguous instruction, stale constraint, thread overload, unverified
   claim accepted), and a sensitivity flag (does the excerpt window contain names, client
   detail, credentials, or anything a public repo should not carry).
4. A short verdict: which 2 incidents you would pick as test runs and why, considering
   diagnostic clarity, excerpt self-containedness, and sensitivity.

CONSTRAINTS
- Parse with Python, never by loading the JSON into context.
- Excerpts in the report are working material, not yet cleared for the public repo. The
  report stays in ofr-scout and must not be committed to any git repo.
- Do not modify the export. Read only.
```

what-happened:
Extracted the export to `ofr-scout` and profiled `conversations.json` with 14 throwaway Python
scripts, never loading the JSON into context. Established the schema, then scored all 43
conversations against a 17-signal lexicon and wrote per-conversation excerpt dumps to disk so only
compact summaries entered context. Both known incidents were located, but not where expected: they
live inside `tool_result[view].content` in the 2026-08-08 genesis chat, as retrospective journal
prose from `hod-review-comp9-journal.md`, not as live turns — this export batch only covers
2026-08-01→08, so the late-July hod-review transcripts are absent entirely. Verified that claim by
reading the earlier Aug-5 zip read-only from the scratchpad (6 conversations, Aug 5 only), which
confirmed the exports are incremental rather than cumulative. Shortlisted and hand-verified 8
candidates, discarded roughly as many false positives, ran a 12-pattern sensitivity scan over both
whole conversations and the specific excerpt windows I recommend, and delivered a 37 KB report.

files-touched:
- created `C:\Users\alexa\Downloads\ofr-scout\scout-report.md` (the deliverable, 37,402 B)
- created `ofr-scout/scripts/01_schema.py` … `14_window_sens.py` (14 scan scripts, reusable)
- created `ofr-scout/excerpts/*.txt` (14 per-conversation signal + window dumps)
- created `ofr-scout/known/*.txt` (5 documents extracted from d48abded tool results, incl. the comp9 journal)
- created `touchdowns/TD-2026-08-08-scout-export.md` (this file)
- extracted the export into `ofr-scout/` (conversations.json, projects/, memories.json, users.json, login_history.json) — source zip unmodified

decisions:
- Wrote excerpt windows to files and read back only signal-hit summary lines — kept a 11.7 MB corpus out of context while still allowing verbatim quoting.
- Searched every text-bearing field, not just `text` and `thinking`, after the first pass returned zero hits for the known incidents — the evidence was in attachments and tool results, and a text-only parser would miss most of the corpus.
- Checked `parent_message_uuid` for branching rather than trusting array order, because a shingle detector had flagged three "repeated instructions" that turned out to be prompt edits.
- Read the earlier Aug-5 export read-only to test whether batches are cumulative — small scope excursion, but it decided whether the July incidents were findable at all.
- Ran the sensitivity scan twice, once per conversation and once scoped to the exact recommended windows, so the verdict could claim "clean" about a specific publishable unit rather than a whole chat.
- Recommended `006f1fc0` idx 9–12 and `e19178eb` idx 46–47: the first because idx 12 is an explicit recovery confirmation and therefore an answer key, the second because it tests instruction-to-cost attribution rather than register.
- Excluded the health-data conversations (`a7b3c436`, `~~sealthongevity` family) from the picks — real diagnostic value, but the privacy cost is not worth it when #1–#6 cover the same failure modes.
- Contradicted the brief on known incident B: the journal shows the orchestrator did *not* accept the confident claim, he routed it to a code check that caught it. Reframed it as a negative control rather than dropping it.

friction:
- `python` printing crashed with `UnicodeEncodeError` on cp1252 the first time a journal line containing an emoji was printed; fixed by prefixing `PYTHONIOENCODING=utf-8` on every subsequent run. Any parser built here needs this handled at source, not per-invocation.
- First term search returned zero hits for all five incident-A search terms and I nearly concluded the incidents were absent from the export. They were present 4× each — the search was only covering `text` and `thinking` blocks. Cost one wrong intermediate conclusion, stated to the user before it was corrected.
- The 7-gram repeated-requirement detector produced three false positives that all turned out to be branch points (edit-and-resend), and one more that was a pasted PowerShell error message appearing twice. Saturated at the cap of 8 on 8 conversations, so the raw count was useless as a ranking signal.
- The `wrong` signal is poisoned by the orchestrator's own standing prompt preamble ("Push back with logic if I am wrong"), which scored two clean chats as frustration. Noted in the report as a parser requirement.
- `Bash` tool resets cwd to the repo root after every call, so every script invocation needed an explicit `cd` — minor, but it makes chained commands fragile.

state-left:
The deliverable is `C:\Users\alexa\Downloads\ofr-scout\scout-report.md`. `ofr-scout` is confirmed
outside any git repository (`git rev-parse` fails there), so the do-not-commit constraint holds by
location, not by `.gitignore` — if that folder is ever moved inside the repo, the constraint breaks.
The 14 scan scripts are the raw material for the real parser; `01_schema.py`, `07_tree.py` and
`10_allfields.py` encode the three schema facts that matter most (thinking is 37% redacted to
summaries, the message list is a tree with branch points, and the evidence lives in attachments and
tool results).

Next session should know two things. First, the two canonical hod-review incidents exist only as
journal prose in this batch; if a public test run must show the diagnostician working on that build,
the mid-to-late-July export batch or the Claude Code session files for it need to be sourced. Second,
the abandonment signal from the brief cannot be tested against this data at all — zero conversations
in the batch end on a human turn.

Unrelated: the repo working tree now shows untracked `README.md`, `parse.py`, `diagnostician/` and
`__pycache__/` that were not present in this session's opening `git status` and that I did not
create. I left them alone. `__pycache__/` should probably be gitignored before anyone commits, and
whoever wrote `parse.py` should check it against the schema section of the scout report — in
particular the tree-walking and all-fields findings, which a first-pass parser is likely to have
missed.
