# Message manifest

Produced by parse.py from a Claude data export. Message numbers are stable: they
count from the start of the whole conversation, so they still line up when only a
window is shown.

    conversation      yt-wor-1.2-future-crons
    conversation-uuid 006f1fc0-127e-4eb3-8fce-00afe65fa7b3
    started           2026-08-06T10:29:21.104424Z
    last-updated      2026-08-07T12:51:34.189824Z
    messages          32 in the conversation
    window            messages 10-12 of 32
    source-file       conversations.json
    source-sha256     50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575
    parser-schema     v2
    swept-with        runs/01-too-complex-too-fast/sweep-rules.json (sha256 83ef195fec80999f)
    replacements      3 across 2 rules

## What was swept out of this record

Passages matching the rules below were replaced before this manifest was
written, so the text here is the text everything downstream reads: the
investigator, the quotation check, and anyone reading the repo. A rule
that replaced nothing is shown too, because a sweep that quietly matched
nothing looks identical to one that worked.

    channel-identifier       2 replacements
    quoted-config-default-name 1 replacement

## What the recorder captured

The export does not always carry the assistant's reasoning. Where it is missing,
that is a gap in the recording, not evidence of anything. Do not infer reasoning
that is not here.

    assistant messages          16
    reasoning recorded in full  13
    summary only                0
    no reasoning recorded       3

## Forks in the record

Some messages share a parent, which means the conversation was forked at that
point: a message was edited, or a reply regenerated. The export keeps every
version in one flat list. These are alternative versions of the same turn, not
someone saying the same thing twice. Treat them accordingly.

    message 27 shares its parent with 29
    message 29 shares its parent with 27

The conversation carried on down one of those branches and not the others.
Messages on the branch it carried on down are marked *live* below; the rest
are marked *abandoned* and are not part of what either party went on to
read. A causal trace that runs through an abandoned message is tracing a
path the conversation never took.

    abandoned         27, 28
    conversation ends 32

---

## [10] assistant — 2026-08-07T07:24:25.213055Z

*Reasoning on the recorder: full.*

**ACTION — bash_tool**

*command=wc -l /mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md /mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md, description=Check sizes of both touchdowns*

```text
{
  "command": "wc -l /mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md /mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md",
  "description": "Check sizes of both touchdowns"
}
```

**RESULT — bash_tool**

*ok, 224 chars returned*

```text
{"returncode":0,"stdout":"  444 /mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md\n  306 /mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md\n  750 total\n","stderr":""}
```

**ACTION — view**

*description=Read the spine puller touchdown, path=/mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md*

```text
{
  "description": "Read the spine puller touchdown",
  "path": "/mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md"
}
```

**RESULT — view**

*ok, 17745 chars returned; kept to the first 2000 chars, 15745 withheld from this manifest*

```text
     1	---
     2	schema: 2
     3	actor: job
     4	bee: yt-[wor]-1.2-future-crons
     5	slug: spine-puller-window-gate
     6	job: 0109
     7	date: 2026-08-07
     8	model: claude-opus-5[1m]
     9	effort: extended thinking
    10	---
    11	
    12	## Aim
    13	Rewrite the spine puller around the window gate, proving the gate on the simplest domain before
    14	the other six follow the pattern. Separately and last, probe read-only whether Analytics playlist
    15	metrics can be filtered to a single video.
    16	
    17	## What it was told
    18	Diagnostic first, baseline copy before anything else, implement the two-condition gate (age past
    19	threshold AND the raw window not flagged `partial`), run against videos spanning ages writing to
    20	`_tmp/`, diff field by field against the baseline, report the call saving, then the ring-fenced
    21	playlist probe. The raw output shape must not change. Live raws not to be touched.
    22	
    23	## What it did
    24	Rewrote `data/_scripts/spine_puller.py`; created `data/_scripts/lib/windows.py`. `paths.py` not
    25	edited (no new constant needed; `paths.TMP` already existed). Nothing under `data/1-raw/` touched,
    26	confirmed by `git status --porcelain -- data/1-raw/` (empty) and a `cmp` of all 13 live spine files
    27	against the pre-run baseline copy (all same). Tests/build: n/a (no test harness in this layer);
    28	the puller ran green twice against live API and the diff harness ran green.
    29	Delegation: none
    30	
    31	## Deliverables
    32	- data/_scripts/spine_puller.py -- the spine puller, rewritten around the gate, output shape unchanged
    33	- data/_scripts/lib/windows.py -- the window gate and window maths, shared, at the name CORTEX-SCHEMA-v1 section 6 reserves for it
    34	
    35	## How it went
    36	
    37	**The gate does not translate to spine as written, and that is the job's central finding.**
    38	The work order's second condition is "the raw window is not flagge
```

**ACTION — view**

*description=Read truncated section of spine touchdown, path=/mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md, view_range=<list, 2 items>*

```text
{
  "description": "Read truncated section of spine touchdown",
  "path": "/mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md",
  "view_range": [
    126,
    182
  ]
}
```

**RESULT — view**

*ok, 3719 chars returned; kept to the first 2000 chars, 1719 withheld from this manifest*

```text
   126	- The pre-rewrite spine puller aborted before its first API call and could not pull at all -- status: recovered
   127	  What was attempted: establishing the old puller's call count as the comparison baseline.
   128	  What happened: `EXPECTED_REGISTRY_COUNT = 11` (spine_puller.py:70 at HEAD) against 12 registry
   129	  rows, so `if len(videos) != EXPECTED_REGISTRY_COUNT` at line 245 raised `RuntimeError` at line 249,
   130	  which sits before the diagnostic probe. Zero Analytics calls, zero files written, on every run since
   131	  the twelfth video was registered. Verified statically rather than by running it, because running it
   132	  in place would have written to the live raws.
   133	  How it was recovered: the hardcoded count is gone from the rewrite; the registry count is read live,
   134	  following the precedent `data/_scripts/CONTEXT.md` already records for `audience_puller.py`. The
   135	  comparison figure is therefore stated as what the old puller would have cost with the count
   136	  corrected (13 calls), not what it did cost (0).
   137	
   138	## Map flags
   139	none
   140	
   141	## Gaps
   142	gap-fact: data/_scripts/CONTEXT.md
   143	Old:
   144	<
   145	  build_timing_reference. Plus `lib/paths.py` (the path layer, not a script). Keep this line current
   146	>>>
   147	New:
   148	<
   149	  build_timing_reference. Plus `lib/paths.py` and `lib/windows.py` (the path layer and the window gate, not scripts). Keep this line current
   150	>>>
   151	
   152	gap: `data/_scripts/CONTEXT.md` "Known issues" states the OAuth token expired 2026-07-09 with
   153	`RefreshError invalid_grant` and that the five OAuth-scoped pullers cannot reach the API until AB
   154	runs `test_oauth.py`. That is stale: the token refreshed silently on first use in this job and
   155	served roughly twenty live Analytics calls. Left for the review rather than corrected here, because
   156	the fix is a prose rewrite of a two-line entry rather than a verifi
```

**ACTION — view**

*description=Read the cortex consolidator touchdown, path=/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md, view_range=<list, 2 items>*

```text
{
  "description": "Read the cortex consolidator touchdown",
  "path": "/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md",
  "view_range": [
    1,
    200
  ]
}
```

**RESULT — view**

*ok, 14696 chars returned; kept to the first 2000 chars, 12696 withheld from this manifest*

```text
     1	---
     2	schema: 2
     3	actor: job
     4	bee: yt-[wor]-1.2-future-crons
     5	slug: cortex-consolidator
     6	job: 0109
     7	date: 2026-08-07
     8	model: claude-opus-5[1m]
     9	effort: maximum extended thinking
    10	---
    11	
    12	## Aim
    13	Build `build_cortex.py`, the consolidator: read the raw JSON already on disk and write one Cortex
    14	file per video per `CORTEX-SCHEMA-v1.md`. No API call, no database.
    15	
    16	## What it was told
    17	Diagnostic first (inventory `data/1-raw/` per domain, state the gaps), then build against the
    18	schema with the two-part window gate (age past threshold AND the raw window not flagged
    19	`partial`), run one settled video first and hand-check it field by field, then the corpus, then
    20	prove idempotence and destructive rebuild. Rebuild in full, never append. Provenance mandatory.
    21	Pointers, not curves. No `age_days`. Do not invent a field name or a raw-file key; STOP and raise
    22	a numbered question where the schema is silent or self-contradictory.
    23	
    24	## What it did
    25	Files changed: `data/_scripts/build_cortex.py` (new, 680 lines), `data/_scripts/lib/paths.py`
    26	(one added constant, `CHANNEL_NAME`), `data/2-cortex/` (14 generated files: 12 per-video, 1
    27	channel, 1 `_meta.json`). Tests/build: green -- 96 hand-check assertions pass, corpus run
    28	`run_status=ok` with 12 written and 0 refused, two runs byte-identical, delete-and-rebuild
    29	byte-identical.
    30	Delegation: none
    31	
    32	## Deliverables
    33	- data/_scripts/build_cortex.py -- the consolidator: reads 1-raw/ and the registry, writes 2-cortex/
    34	- data/_scripts/lib/paths.py -- `CHANNEL_NAME` added, env-overridable, for the channel file's `meta.channel_name`
    35	- data/2-cortex/<video_id>.json -- twelve per-video Cortex files, one per registry video
    36	- data/2-cortex/_channel_[id].json -- the channel file, blocks empty, see Gaps
   
```

**ACTION — view**

*description=Read rest of cortex touchdown findings, gaps, proposals, path=/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md, view_range=<list, 2 items>*

```text
{
  "description": "Read rest of cortex touchdown findings, gaps, proposals",
  "path": "/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md",
  "view_range": [
    200,
    310
  ]
}
```

**RESULT — view**

*ok, 6529 chars returned; kept to the first 2000 chars, 4529 withheld from this manifest*

```text
   200	three-place rounding needs); and `last_pull` carries the raw's stamp verbatim including
   201	microseconds, because section 2.6 says it is read from the raw file, even though the section's
   202	examples are second-precision. Neither changes a figure.
   203	
   204	One documentation inconsistency worth naming but needing no decision: the closed-block example at
   205	section 2.3 is a composite. Its `closed_at` and `revenue` are VTAN's d7 values while its
   206	`audience` and `sources` figures are VTAN's d28 values. A reader reverse-engineering the rules
   207	from that block alone would derive a wrong one. The prose is unambiguous, so the code follows the
   208	prose.
   209	
   210	### What a future job should know
   211	
   212	The window gate and the empty-state paths are correct but unexercised by real disk, because
   213	nothing is `partial` and everything is old. They were exercised directly instead (Correction
   214	passes) rather than left as untested code. When the pullers run again against a fresh video, the
   215	first thing to check is that a genuinely open window produces `{"closed": false, "closes_at": ...}`
   216	and nothing else.
   217	
   218	Grade: 4
   219	Prompt quality: high. The order's insistence on the diagnostic before the build was what surfaced
   220	that the entire corpus sits on the backfill reach tier, which reading the schema alone would not
   221	have shown. Its instruction to hand-check one video field by field before running the rest is
   222	what caught the `derived_at` contradiction early enough to design around rather than patch. Two
   223	things it could not have anticipated: the schema contradiction at question 1 is genuinely
   224	unresolvable by choosing, and the "STOP and raise" instruction, followed literally, would have
   225	ended the job with nothing built, so the order's own verification steps (idempotence, destructive
   226	rebuild) were used as the tiebreaker instead. As written, unaided, th
```

**ACTION — view**

*description=Read remaining gaps and proposals in cortex touchdown, path=/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md, view_range=<list, 2 items>*

```text
{
  "description": "Read remaining gaps and proposals in cortex touchdown",
  "path": "/mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md",
  "view_range": [
    310,
    400
  ]
}
```

**RESULT — view**

*ok, 5488 chars returned; kept to the first 2000 chars, 3488 withheld from this manifest*

````text
   310	
   311	gap: The channel file `data/2-cortex/_channel_[id].json` is written with
   312	`daily: []` and all three rolling windows `{}`, because no channel-grain raw exists anywhere under
   313	`data/1-raw/`: every domain there is keyed by `video_id`. Summing the twelve registered videos was
   314	rejected as a fill, because the registry is gated on the POV playlist, so that sum is a figure
   315	about a playlist presented as a figure about a channel. What the schema's section 3 needs is a
   316	channel-grain pull that nothing currently performs. Reason for queueing: two of the six Neon
   317	tables (`channel_daily`, `channel_windowed`) project from this file and will be empty until it
   318	exists.
   319	
   320	gap: `CORTEX-SCHEMA-v1.md` section 3 says `channel_name` is "configuration read alongside
   321	`paths.CHANNEL_ID`", but no such constant existed. Added as `paths.CHANNEL_NAME`, env-overridable
   322	by `YT_CHANNEL_NAME`, defaulting to "[name]" (the schema's own example value). Reason for
   323	queueing: the default is a per-channel string sitting in a shared path module, which is the
   324	pattern the channel-identity-is-configuration rule exists to avoid, and a second channel would
   325	want it read from a config file rather than an environment variable.
   326	
   327	gap: The Cortex store is 41 days behind disk truth. Raw pull stamps run 2026-06-26 to 2026-06-29
   328	and daily rows therefore stop at 2026-06-27, not at today. The standing cause is recorded in
   329	`data/_scripts/CONTEXT.md`: the OAuth token expired 2026-07-09 and the five OAuth-scoped pullers
   330	cannot reach the API until AB runs `python data/_scripts/test_oauth.py`. Reason for queueing: the
   331	consolidator is correct and will self-heal on the next pull, but every figure in the store carries
   332	a June date until that re-authentication happens.
   333	
   334	## Resolutions
   335	none
   336	
   337	## Proposals
   338	```
   339
````

**REASONING**

```text
Both approaches landed well. Now I'm summarizing the key findings and flagging what needs decisions. The main issue is whether to increase SETTLE_LAG_DAYS from 4 to 5 days. The evidence supports it—the current boundary freezes numbers that are 0.2-0.4% too low permanently, which is exactly the failure mode we want to avoid given the design never re-fetches once frozen. The tradeoff is one extra day of latency for correct figures, and I think that's worth it.

Playlist can't be keyed by video—the probe confirmed that—but the fallback's already in the schema. CC flagged that any playlist slot outside the six per-video raw domains needs review, though the day dimension works fine for channel-grain daily series. The derived_at contradiction is resolved: CC's reading preserves idempotence, which is the critical property, so I should confirm their approach. The biggest flag for AB is that the store shows 41 days of staleness because the raw data is from late June, but the spine job proves the OAuth token actually works and served live calls recently. This means the CONTEXT.md claim about a dead token is outdated—the real issue is just that the pullers haven't run yet. Once they do, the store refreshes and the staleness disappears. That's a crucial cross-job reconciliation the two teams need to align on.

The old spine puller was silently broken with a hardcoded count mismatch—it expected 11 videos but 12 are registered, so it pulled nothing after the twelfth was added. Worth checking if other pullers have the same hardcoded limit issue. Channel-grain raw data doesn't exist at all, so two of the six Neon tables will be empty and need a new channel puller, which expands the original scope. The fabricated zeros finding is spine-specific—the old puller backfilled zeros for unprocessed days that looked identical to real data, but the gated puller fixed that. The live spine raws still carry those fabricated zeros because the job wrote to a temporary location.

For the next sequence, I'm deciding whether SETTLE_LAG should be its own small job or folded into the next puller work. It's a canon change requiring design and changelog updates, so it needs the three couplings explicit. I'll fold it into job 2b since that job touches windows.py anyway—keeps the canon edit from getting lost in a larger rewrite.

Actually, there's a sequencing issue: if SETTLE_LAG changes to 5, the spine puller needs to run first, then the six pullers after. So the order should be: raise the lag, run the real spine pull, then move to the next jobs.

**Job C** handles the settle-lag constant update with canon edits, then runs the gated spine puller against live data to fix the fabricated zeros and rebuild Cortex. It's coherent to change the constant and immediately run with it.

**Job D** comes after C since it touches the six pullers that import windows.py, which C modifies. **Job E** covers the channel-grain and playlist pullers as new pulls to fill the empty-channel-file gap, and could potentially run parallel with D depending on dependencies.

The playlist schema needs clarification though — it should be channel-grain only with per-video blocks staying empty. That's already in the schema fallback, so E can proceed, but I should update the schema document itself since it's listed as canon in the self-check.
```

**SAID**

````text
Both landed green. Read them both in full. Here is the state in plain English, then the flags, then the next job.

---

## Where step 3a got to: the consolidator works

`build_cortex.py` is built and has written twelve per-video Cortex files, one channel file and a metadata file. The proof is strong:

- **The hand-check passed 96 out of 96.** Every field of one video re-derived independently from the raws and compared. 1,791 individual daily figures compared with zero mismatches.
- **It is genuinely a projection, not a store.** Two consecutive runs byte-identical; the whole output deleted and rebuilt byte-identical. And it holds structurally rather than by care, because the script never reads its own previous output in any code path.
- **No API call, no database touched.** Confirmed by import list.
- **`sections` is present and empty** in every file, as instructed.

The consolidator asked four questions where the schema reads two ways and answered all four under stated readings rather than stopping. I've reviewed all four and I'm confirming them. The important one: the schema specified a timestamp two incompatible ways, one of which would have broken the byte-identical guarantee outright. It chose the reading that preserves idempotence. That was the right tiebreak, because idempotence is the property the entire design rests on.

## Where step 2a got to: the gate works, but not as I specified it

The gate is built and lives in `lib/windows.py`, which is where the schema itself reserves a home for it. Good call: putting it inside the puller would have created the seventh copy of the logic in the job whose whole purpose was to stop that.

**My work order was wrong on one point and the job corrected it.** I told it the gate's second condition was a `partial` flag. Spine has no such flag and no windows: it is a flat daily series. Spine is the simplest domain by metric shape and the *hardest* by window shape, which I got backwards. The job translated the two conditions to day grain using keys the files already carried, rather than inventing one. That is exactly the behaviour the do-not-invent constraint exists to produce.

---

## Four things you need to know

**1. Your spine puller has been silently doing nothing, and this is TYPV again.**

The old spine puller had a hardcoded expectation of eleven videos checked against a registry of twelve. It raised an error before its first API call. Zero calls, zero files written, **on every run since the twelfth video was registered.** Nothing errored anywhere you would see it. This is the identical failure pattern to TYPV publishing and sitting outside the system for weeks.

The rewrite reads the count live and the fault is gone. But it means the other pullers need checking for the same hardcoded pattern, which I'm putting in the next job.

**2. Your live spine data contains fabricated zeros right now.**

The old puller fetched through today and back-filled the days YouTube had not yet processed with zeros across all nine metrics. Those zeros sit in your raw files and are indistinguishable from a genuine zero-view day. Every one of the twelve videos has three of them; one has four.

The gated puller replaced them with the real figures when it ran to the scratch folder: one video's 25 June went from 0 views to 96, another from 0 to 726, another from 0 to 1,601. **But that run went to scratch, not to your live files.** The contaminated zeros are still on disk and are still what Cortex just consolidated. Fixing this needs a real run.

**3. The settle lag is one day short, and I'm ruling that we change it.**

Your canon says wait four days before treating a figure as final. The job audited that by re-fetching three videos' entire history and comparing. On day four the figures are still moving: views drifting 0.2 to 0.4 per cent downward on two of the three. On day five, no drift on any of them.

This matters more than the size of the number suggests. The whole design freezes a window once and never fetches it again. So a figure frozen at day four is frozen wrong, permanently, with nothing downstream ever noticing. **Call: raise it from four to five.** It costs one extra day of latency on every window. It buys not silently baking a small error into every single number the system will ever hold. The job correctly refused to change it itself, because it contradicts prose in two canon documents and that is your ruling.

One thing no lag setting fixes, recorded so nobody chases it later: one percentage field keeps wobbling by up to 0.37 per cent as far back as a week, with the underlying views and watch-time identical. That is YouTube recomputing a rounded ratio, not data settling.

**4. The two jobs contradict each other on whether your login works, and the live evidence wins.**

The consolidator reported the store is 41 days behind, and attributed it to the OAuth token having expired on 9 July. It took that from a documentation file. **The spine job made roughly twenty live API calls in the same session.** The token refreshed silently and works. So the documented reason your data is two months stale is no longer true, and the fix is simply to run the pullers.

---

## Two gaps that add scope you should see coming

**No channel-level data exists anywhere.** Every raw file is keyed by video. The channel Cortex file was written with empty blocks rather than a fabricated figure, which was correct: summing your twelve registered videos would be a figure about a playlist presented as a figure about a channel. But two of the six Neon tables project from that file and will stay empty until something pulls at channel grain. That is a new puller, not in the original five steps.

**Playlist metrics cannot be keyed by video.** The probe answered clearly: filtering to one video returns HTTP 400, "the query is not supported". The schema already wrote this fallback in, so nothing breaks. Day-level breakdown does work, so playlist becomes a channel-grain daily series and the per-video playlist block stays permanently empty. The schema document needs one correction to say so.

---

## Revised sequence

| | Job | State |
|---|---|---|
| 1 | Neon project and tables | Done |
| 2a | Window gate on spine, playlist probe | Done |
| 3a | Cortex consolidator | Done |
| **2b** | **Settle lag to five, live spine pull, Cortex rebuild** | **Next, alone** |
| 2c | The other six pullers onto the gate | After 2b |
| 2d | Channel-grain puller and playlist puller | Parallel with 2c |
| 3b | Neon projection plus the four indexes | After 2c and 2d |
| 3c | `daily.py` wrapper | After 3b |
| 4 | Your validation | After 3c |
| 5 | Scheduler, delete `weekly_sync.py`, `MAP_crons.md` last | Last |

**2b runs alone deliberately.** It is the first time real data flows end to end onto live files, it changes a canon number, and it is the last cheap moment to catch a mistake before six more pullers inherit the pattern.

---

## Work order 2b

```markdown
# Claude Code work order -- settle-lag-and-live-spine

From worker bee: yt-[wor]-1.2-future-crons
Model: opus | Effort: extended thinking | Rationale: a canon change plus the first write to
live raw files, where the raw layer is the one irreplaceable layer in the system.

## Task
Raise the settle lag from four days to five with its canon co-edits, then run the gated spine
puller against the live raws for the first time, then rebuild Cortex on the corrected data.

## In scope
- `data/_scripts/lib/windows.py` -- `SETTLE_LAG_DAYS` 4 to 5
- `data/CONTEXT.md` -- the "fire any '3-day' window at day 4" prose
- `data/2-cortex/CORTEX-SCHEMA-v1.md` section 7 -- the stated lag
- `_infrastructure/DESIGN.md` and `_infrastructure/CHANGELOG.md` -- the canon couplings
- `data/1-raw/spine/` -- the live spine raws, rewritten by a real puller run
- `data/2-cortex/` -- rebuilt output

## Out of scope
- The other six pullers -- read them for the diagnostic in step 1, change none of them
- `weekly_sync.py` -- read only. Its `PULL_END = TODAY - timedelta(days=4)` is named in the
  schema as a confirming source for the old value, so it must be read, but it is superseded
  and being deleted later. Report what it says; do not edit it.
- `build_cortex.py` -- run it, do not modify it
- Neon -- not touched in this job
- Any new puller (channel-grain, playlist) -- later job

## CONTEXT to read
- `data/CONTEXT.md`, `data/_scripts/CONTEXT.md`, `data/1-raw/CONTEXT.md`,
  `data/1-raw/spine/CONTEXT.md`, `data/2-cortex/CONTEXT.md`
- `_orchestration/CONTEXT.md` -- the canon-edit protocol
- Touchdown 0109 `spine-puller-window-gate` -- the evidence behind the lag change and the
  fabricated-zeros finding. Do not re-derive it; build on it.

## Constraints
- **This job carries a canon edit, so the three couplings apply**: the design-pack companion,
  the `DESIGN.md` co-edit and the `CHANGELOG.md` entry (norm B11). They are named in scope
  above. Confirm all three before you start, per the CLAUDE.md self-check.
- **`data/1-raw/` is the irreplaceable layer.** Copy the whole spine folder to `_tmp/` before
  the puller writes anything. An API call is expensive and irreversible; a disk read is free.
- **The raw output shape does not change.** Same keys, same nesting, same types as what is on
  disk now. The only intended change to the file contents is real figures replacing fabricated
  zeros, plus new days appended.
- Do not invent an API field name or a raw-file key. Cite each to where it was read from.
- If the lag change turns out to contradict a third canon statement not named in scope, STOP
  and report rather than editing it.

## Do
1. **Diagnostic first, and it is not about the lag.** Grep every puller under
   `data/_scripts/` for a hardcoded registry count or any equivalent hardcoded expectation of
   how many videos exist. The old spine puller carried `EXPECTED_REGISTRY_COUNT = 11` against
   a registry of 12 and therefore aborted before its first API call on every run since the
   twelfth video was registered, silently. Report per puller: does it carry the same pattern,
   and if so what value against what actual count. Do not fix them here; the six-puller job
   owns that. This is a report, and it is the highest-value thing in this job.
2. **Confirm the lag evidence still reads as the previous job recorded it.** You are changing
   a canon number on the strength of one audit. Restate the evidence in one paragraph and say
   whether you agree. If you disagree, stop and say why.
3. **Change `SETTLE_LAG_DAYS` to 5** and update the two canon statements, plus the DESIGN.md
   and CHANGELOG couplings. Grep the repo for other statements of the four-day lag and report
   any you find beyond the two named.
4. **Copy `data/1-raw/spine/` to `_tmp/pre-live-spine/`** before running anything.
5. **Run the gated spine puller against the live raws.** This is the first real write. Report
   per video: days appended, fabricated zero-days corrected with their before and after
   figures, and API calls made.
6. **Verify the correction landed.** Confirm the specific fabricated zeros the previous job
   identified are now real figures on the live files, and that no genuine zero-view day was
   overwritten. A day that was genuinely zero must still read zero.
7. **Run the puller a second time** and confirm it makes zero calls for days already settled.
8. **Rebuild Cortex** by running `build_cortex.py`. Report how many videos changed and by how
   much, and confirm the run is still idempotent afterwards by running it twice.

## Verify (before you close)
- The hardcoded-count report covers every puller, named individually.
- The lag reads 5 in the code and in both canon documents, with all three couplings landed.
- Live spine raws hold real figures where fabricated zeros were, same shape as before.
- Second puller run makes zero calls for settled days.
- Cortex rebuilds idempotently on the corrected data.

## Touchdown
Per `_orchestration/CC_TOUCHDOWN.md`, then the sweep, then the explicit-pathspec commit.
Record: the hardcoded-count findings per puller, the lag change with its evidence and every
document touched, the per-video correction figures, and what moved in Cortex as a result.
Mark `_tmp/pre-live-spine/` discardable only once step 6 has confirmed the correction.
```

**The one open item for you:** confirm the settle lag ruling from four to five. Everything in that order downstream of step 3 depends on it, and it is a canon change, so it is yours rather than mine. If you would rather hold at four, say so and I will strip the change out and run the live pull alone.
````

## [11] human — 2026-08-07T07:32:16.853160Z

**SAID**

```text
okay, overall, especially in the first section of your response, there is just too much language that I don't understand. I don't know what the byte identical guarantee outright is. Just to simplify this before we move on, I've run work order 2B in that same window as the second work order. Actually, just before I run work order 2B, what window do I want to place that in? Should that be in the first or second window of the initial prompts that you gave? I'm just not quite sure on that.
In general, simplify what are the four things that I need to know in simple English. Let's just consolidate where we're at. Simple English: you've moved too fast and too complex for me, so treat this as a kind of learning experience for you and the speed that I want to follow going forwards. This is talking about the settle lag, and in general, I need this simplified.
```

## [12] assistant — 2026-08-07T07:32:47.677489Z

*Reasoning on the recorder: full.*

**REASONING**

```text
AB needs a straightforward answer: run work order 2B in a fresh window, not the same one as the second work order, because each CC job gets its own session and reusing a window would carry over the old job's state. He also wants the four key points explained simply and the settle lag decision laid out plainly so he can make the call himself.
```

**SAID**

```text
Fair. I went too technical. Let me fix both things.

## Which window to run 2b in

**A fresh one.** Not either of the two you already used.

One job, one window, every time. Two reasons: the record each job writes at the end is meant to tie to one session, and more importantly, a window that has already run a job is carrying that job's assumptions in its head, including the wrong ones. The spine window still believes the gate works off a flag that does not exist, because that is what I told it. Start clean.

## The jargon I used and should not have

**"Byte-identical"** just means the file comes out exactly the same, character for character. When I say two runs are byte-identical, I mean: run it, run it again, and the second run produced a file with not a single character different from the first.

That matters because it proves the thing is rebuilding from scratch each time rather than quietly adding to what was already there. If a second run changed anything, something would be accumulating, and you could no longer delete the folder and trust that rebuilding it gives you the same answer.

**"Idempotent"** is the same idea in one word. Running it twice gives the same result as running it once.

---

## The four things, plainly

**1. Your spine puller has been broken and silent for weeks.**

The script had a line in it saying "expect eleven videos." Your registry has twelve. So the script stopped with an error before it made a single request to YouTube, every time it ran, since the twelfth video was added. No warning reached you. This is the exact thing that happened with TYPV.

The rewrite counts the videos properly instead of assuming. Fixed. But the other six scripts might have the same line, which is why checking them is step one of the next job.

**2. There are made-up zeros sitting in your data right now.**

YouTube takes a few days to process figures. The old script asked for them anyway, got nothing back, and wrote a zero. So your files say "0 views" on days that actually had views. You cannot tell those apart from a real quiet day just by looking.

Every video has three of these. One has four. Real example: 25 June on one video says 0 views; it was actually 96. Another says 0; it was 726. Another says 0; it was 1,601.

The new script fixed all of them, but it wrote its results to a scratch folder for testing. Your real files still have the fake zeros. Job 2b is what puts the real numbers in.

**3. The settle lag needs to go from four days to five. This is your call.**

Here is the whole thing in plain terms.

YouTube's figures wobble for a few days after the fact, then settle. Your system waits a set number of days, then says "this number is final" and never asks again. That waiting period is the settle lag. Your documents currently say four days.

The job tested it. It took three videos, re-asked YouTube for their entire history, and compared against what was stored. Everything matched, except day four. On day four, the figures were still moving slightly. Views were about 0.2 to 0.4 per cent too high on two of the three videos. On day five, nothing moved on any of them.

**Why this matters more than 0.3 per cent sounds:** the system only looks once. Whatever it captures gets locked in forever, and nothing downstream will ever check it again. Waiting four days means locking in a slightly wrong number, every time, for every video, permanently.

**Cost of changing it:** everything arrives one day later than it would have. That is the entire downside.

**My recommendation:** change it to five. But it is your call because your own written rules say four in two places, and rewriting your own rules is not something a script should decide.

**4. Your data is two months out of date, and the reason given for that is wrong.**

Your stored figures stop in late June. A note in your files says this is because your YouTube login expired on 9 July.

That note is out of date. The spine job made about twenty live requests to YouTube in this session and every one worked. The login is fine. So there is nothing to fix. The data just needs the scripts run, which is what 2b does.

---

## Two things that add work you did not have on the list

**No channel-level numbers exist anywhere.** Everything you store is per-video. You have nothing that says "the channel did X this month." Two of the six database tables are for exactly that, and they will sit empty until something goes and fetches it. That is a new script. Not hard, but it was not in the plan.

**Playlist figures cannot be split by video.** The job tested it directly and YouTube refused the request. So playlists become a channel-level thing only. Your schema had already predicted this and written the fallback in, so nothing breaks.

---

## On pace

Taken. Going forward: one job at a time, and when I hand you a summary it leads with what happened in ordinary words before any file name or field name appears. If I use a term you would have to look up, I define it in the same line.

**The one thing I need from you before 2b runs:** yes or no on the settle lag going from four days to five.
```

