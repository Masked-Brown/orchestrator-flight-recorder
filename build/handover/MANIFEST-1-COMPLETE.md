# MANIFEST 1 — COMPLETE

status: complete-with-questions

summary: The repo skeleton is scaffolded, the investigator persona is drafted, and `parse.py`
works against the real export. The export's schema was inspected by script only and is
recorded in full below; the parser was built against what is actually there, not against an
assumed shape. The single most consequential finding is that the export's flattened `text`
field splices the assistant's private reasoning into the prose it actually sent, with no
marker between them — so the parser reads the structured `content` blocks instead and keeps
every channel labelled and separate. Three open questions are logged, one of which materially
affects M4's planned flagship incident and needs the human at the intake gate.

---

## files-created

- `parse.py` — deterministic export reader. Turns the conversations JSON into a numbered
  message manifest, in markdown for reading or JSON for machines. Stdlib only, Python 3.8+.
- `README.md` — root README skeleton. Honest "what exists right now" table; no claim a fresh
  clone cannot check today. M5 rewrites it to final.
- `diagnostician/identity.md` — who the investigator is: the accident-investigator discipline,
  the one-probable-cause rule, the anchoring rule, the verdict space including acquittal and
  undetermined, and the no-prescription invariant justified in-domain.
- `diagnostician/README.md` — drop-in usage skeleton: what you give it, what comes back, what
  it will not do. Marked under construction.
- `diagnostician/reference/failure-modes/README.md` — what lands here and the planned eight
  modes (M2 writes them).
- `tests/README.md` — the two-directional test contract (M3 writes it).
- `runs/README.md` — what a run folder holds; the real-and-swept rules (M4).
- `training-layer/README.md` — the profile idea, and the ships-populated-or-not-at-all rule (M4).

Committed but not authored by M1:

- `touchdowns/TD-2026-08-08-scout-export.md` — the scout session's touchdown, which appeared in
  the working tree while M1 was running. Read in full before committing (a scout that walked
  the export could have quoted it); it contains only summary and methodology, no conversation
  content, so it is safe for a public repo. It is the source of open question 1's
  confirmation and of decisions 16 and 17.

## files-changed

- `.gitignore` — rewrote. Removed a stray placeholder line left in the seed version
  (`touchdowns/nothing  # placeholder line, ignore this, see step 2`, which was a live pattern
  rather than a comment, since `#` only starts a comment at the beginning of a line). Added
  `out/` so locally generated manifests cannot be committed, plus ordinary Python noise.
  Every export pattern from the seed version was kept. Verified after the rewrite: all five
  export items still ignored, and a real generated manifest in `out/` confirmed ignored.

## The export schema, as recorded by script

Inspected with four throwaway scripts that printed structure only — keys, types, counts,
lengths, booleans. No raw message content was read into the session. File:
`conversations.json`, 11.76 MB, sha256 `50ff77f7…64a575`.

**Top level.** A JSON list of 43 conversation objects.

**Conversation object** — keys present on all 43:

| key | type | notes |
|---|---|---|
| `uuid` | str | |
| `name` | str | the title; 40 unique of 43, none empty |
| `summary` | str | populated on 39 of 43 |
| `created_at` / `updated_at` | str | ISO 8601 UTC, e.g. `2026-08-01T18:06:14.356451Z` |
| `account` | dict | only key is `uuid`. No personal detail. |
| `chat_messages` | list | the messages |

**Message object** — keys present on all 346 messages: `uuid`, `text`, `content`, `sender`,
`created_at`, `updated_at`, `attachments`, `files`, `parent_message_uuid`.

- `sender` is exactly `human` (173) or `assistant` (173).
- Message uuids are unique across the whole export (346/346).
- `chat_messages` is already in chronological order: zero adjacent timestamp inversions across
  all 43 conversations. Array order is therefore safe to number from.
- 3 conversations hold 0 messages (indices 35, 39, 40). Message counts: min 0, median 6,
  max 56.

**Content blocks.** `content` is a list on every message. Four block types occur:

| type | count | fields that matter |
|---|---|---|
| `text` | 401 | `text` |
| `tool_use` | 333 | `name`, `input` |
| `tool_result` | 333 | `name`, `content` (list of blocks), `is_error` |
| `thinking` | 275 | `thinking`, `summaries`, `thinking_hidden` |

`tool_result.is_error` was true 10 times. Tool names seen: `view` 64, `web_search` 58,
`bash_tool` 56, `create_file` 41, `present_files` 41, `image_search` 35, `str_replace` 14,
`web_fetch` 11, `conversation_search` 5, and a tail of filesystem/MCP calls.

**The `text` field is not a safe source.** On 208 messages the flattened `text` equals the
concatenation of the `text` blocks. On the other 138 — all assistant messages — it does not,
and in every one of those the flattened field is *longer* than the prose blocks (median 2,341
characters longer, max 23,775). The extra material is the model's private reasoning: the
thinking text was found inside the flattened `text` field in all 172 cases where thinking text
existed. Every `text` block is a substring of the flattened field. So `text` is a rendered
view that merges the cockpit voice channel into the transmitted speech. Anything built on it
can quote a thought as though it were a statement. **The parser reads `content` blocks only.**

**Reasoning is present but partial.** 163 of 173 assistant messages carry at least one
thinking block, but 103 of the 275 thinking blocks have `thinking_hidden` true and an empty
`thinking` string. Of those, 79 still carry `summaries` (a list of `{summary: str}`, 798
summary strings in total, 42–180 characters each, none empty) and 24 carry nothing. Per
message this gives exactly three states, which the parser records:

- `full` — thinking text present (111 messages)
- `summary-only` — text withheld, summaries survive (52 messages)
- `absent` — no thinking block at all (10 assistant messages)

**Forks.** In 3 conversations (indices 15, 32, 33) one `parent_message_uuid` has two children,
and in every case both children are `human` — an edited or resent prompt. The export keeps
both versions in one flat list, so read linearly a fork looks like the orchestrator repeating
themselves. That is a false trail, and the parser flags it.

**Attachments.** 41 `attachments` entries carry `file_name`, `file_size`, `file_type` and
`extracted_content` (1,410–35,181 characters — pasted specs and handovers, often the actual
instruction for the session). 76 `files` entries carry only `file_uuid` and `file_name`, with
no text in the export.

**Degenerate cases handled:** one assistant message with a completely empty `content` list
(conversation 19), three empty conversations, and five messages whose flattened `text` is
empty.

**Also in the export folder, and gitignored:** `users.json`, `memories.json`,
`login_history.json`, `projects/` (25 files). None are read by `parse.py`.

## decisions-made

1. **Parse `content` blocks, never the flattened `text` field.** Justified above: the
   flattened field merges private reasoning into transmitted prose. Building on it would let a
   report attribute a thought to a statement, which is the fabrication failure the whole entry
   turns on. This is the load-bearing decision in the manifest.
2. **Label every segment by channel:** `SAID`, `REASONING`, `REASONING-SUMMARY`, `ACTION`,
   `RESULT`, `ATTACHMENT`. The origin/surface split needs to distinguish what was said from
   what was thought from what a tool did. Collapsing them destroys the distinction the
   propagation trace depends on.
3. **Preserve block order within a message.** Segments are emitted in the order they occur, so
   the interleaving of speech and tool calls survives. A fault often travels *within* a turn.
4. **Record reasoning coverage in a header on every manifest**, in the three states above,
   with an explicit line saying a gap in the recording is a gap and must not be filled in.
   brainwave.md asks for exactly this; the schema turned out to support it precisely.
5. **Flag forks; do not silently reconstruct a main path.** Choosing a "real" branch is a
   judgment call that discards part of the record, and M1 has no mandate for judgment calls.
   Flagging is deterministic and honest. Noted as an open question for M2.

   The scout independently reached the same structural finding from the other direction — it
   checked `parent_message_uuid` because a repeated-instruction detector had flagged three
   false positives that were all prompt edits — and its touchdown warns that a first-pass
   parser is likely to miss both the tree structure and the fact that evidence lives outside
   the `text` field. Both are covered: forks are detected and flagged (decision 5), and
   attachments and tool results are parsed and recorded rather than ignored (decisions 9 and
   17). The one place M1 deliberately differs is that it numbers messages by array order
   rather than walking the tree. That is safe here and was verified, not assumed: across all
   43 conversations there are zero adjacent timestamp inversions, so array order is
   chronological order. Walking the tree would renumber messages and break the stable
   numbering M4's windowed excerpts depend on.
6. **Message numbering is global and stable under windowing.** `--messages 20-32` still prints
   messages 20 to 32, not 1 to 13. M4 ships windowed excerpts, and a report citing "message 26"
   must mean the same message in the excerpt as in the full conversation.
7. **No wall-clock in the output.** "Same input, same manifest" would be false if the manifest
   stamped its own generation time. Provenance is carried by the export's sha256 instead.
   Verified: two runs are byte-identical.
8. **`--json` is the machine contract; markdown is for reading.** check.py should read the
   JSON, where each segment is a discrete string with its channel. Matching quotes against
   rendered markdown would mean parsing around fences and bold headers that message content
   can itself contain.
9. **Tool arguments, tool output and attachment text are not inlined by default**, with
   `--include-tool-io` and `--include-attachments` to inline them. Default off keeps manifests
   readable (241 KB vs 600 KB on the test conversation) and keeps pasted file content out by
   default. Their *presence*, name and size are always recorded, so the investigator can see
   something exists and ask for it rather than not knowing.
10. **Dynamic code-fence length.** First version wrapped message text in a fixed ``` fence;
    since these transcripts are full of code blocks, the content closed the fence early and
    corrupted the manifest from that point on (found in testing: 46 opening fences against 69
    bare closes). The fence is now one backtick longer than the longest run in the body.
11. **Validate the input file's shape, not just its syntax.** The export ships several JSON
    files and they all parse; `users.json` is also a list, so it was cheerfully producing an
    empty one-conversation manifest. Pointing at the wrong file now fails with an error naming
    the right one. An empty manifest that looks like a finding is worse than a crash.
12. **No generated manifest is committed at M1.** Manifests hold raw conversation text, and
    excerpts are only cleared for shipping by the human at the M4 sensitivity gate. All test
    output went to a scratch directory outside the repo; `out/` is gitignored for local runs.
13. **`identity.md` carries persona only, no method.** M1's guardrail is no rules substance,
    so the standard of evidence, the but-for test and the report shape are named as living in
    `rules.md` and `reference/` without being written. It closes with a pointer to them.
14. **Placeholder READMEs in the empty scaffold directories.** Git does not track empty
    directories, so without them the scaffold would not exist in the repo at all. Each names
    the manifest that fills it.
15. **The root README is marked a skeleton with a "what exists right now" table.** The named
    miss is the pitch outrunning the repo; at M1 the parser exists and nothing else does, so
    the README says exactly that.
16. **Force UTF-8 on stdout and stderr.** Found after the scout's touchdown warned that any
    parser built here must handle console encoding "at source, not per-invocation".
    Reproduced: `python parse.py conversations.json --index 3 --messages 4-4` with no `--out`
    died with `UnicodeEncodeError` on a `→` (U+2192), after printing thousands of lines, which
    reads like a parser bug rather than a terminal one. Writing with `--out` was always safe
    because it sets the encoding explicitly; the terminal path now is too.
17. **Tool results say when their content was left out.** A `RESULT` segment whose body is not
    inlined now ends with `; not inlined (use --include-tool-io)`. The scout's finding that
    substantive evidence lives inside tool results makes silent omission a trap: the
    investigator must be able to see that something is there and ask for it. The default stays
    off — inlining took one test conversation from 241 KB to 600 KB — but it is now
    self-advertising rather than hidden in `--help`.

## disagreements

None with the locked anchors in spec.md. Three additions beyond the shape the seed files
specify, logged rather than assumed:

1. **The manifest carries more than spec.md's minimum.** spec.md asks for index, role,
   timestamp, text, and thinking-where-present. The parser also records tool calls, tool
   results and their error flag, attachments, and fork points. Justification: the export
   carries them, and the propagation trace and the `environment` verdict class both need them
   — a session that broke because a tool errored cannot be diagnosed from prose alone. Nothing
   in spec.md is contradicted; the record is fuller.
2. **`out/` is not in plan.md's target layout.** Added as a gitignored home for locally
   generated manifests, because a stranger running `parse.py` on their own export otherwise has
   no obvious safe place to put one. Directly serves the load-bearing privacy rule.
3. **Placeholder READMEs are not in plan.md's target layout.** Reason in decision 14.

## open-questions

1. **For the human, at the M4 intake gate — the flagship incident is not in this export as a
   transcript.** The export covers 2026-08-01 to 2026-08-08 only, 43 conversations. M4's
   planned flagship is the M3 jargon stall from the #9 build, with the #9 journal as its
   independent answer key. No conversation in this export is that build: searching names for
   hod, review, comp, journal, powerpoint, ppt, deck, claimline and extract returns nothing
   matching.

   **This was independently confirmed by the scout session**, whose touchdown
   (`touchdowns/TD-2026-08-08-scout-export.md`) landed in the repo while M1 was running. The
   scout established two things M1 could not have known: export batches are **incremental, not
   cumulative** (verified by reading an earlier 2026-08-05 zip, which held only 6
   conversations from that day), so the late-July hod-review transcripts are absent entirely;
   and the two known incidents *do* exist in this export, but only as **retrospective journal
   prose inside `tool_result` content** in conversation index 42 (`d48abded…`, 2026-08-08),
   where `hod-review-comp9-journal.md` was read into the chat by a `view` tool call. That is
   the answer key, not the incident. Diagnosing a session requires the session's own
   transcript, and it is not here.

   So M4 needs one of: the mid-to-late-July export batch, the Claude Code session files for
   that build, or a different pair of incidents. **This needs a decision before M4 starts, not
   during it.**

   If the incidents are re-chosen, the scout's ranked shortlist is at
   `C:\Users\alexa\Downloads\ofr-scout\scout-report.md` — outside any git repo, and it must
   stay there; it holds unswept excerpts. Its two picks, mapped to this parser's indices:

   - **index 15** `yt-wor-1.2-future-crons` (uuid `006f1fc0…`, 32 messages), scout window
     idx 9–12 — recommended because message 12 is an explicit recovery confirmation, which
     gives the run an answer key from inside the conversation itself. Note this conversation
     also contains a fork at messages 27/29.
   - **index 10** `nbs-wor-1.0-z` (uuid `e19178eb…`, 56 messages), scout window idx 46–47 —
     tests instruction-to-cost attribution rather than register, so the two runs would not be
     diagnosing the same failure shape twice.

   Three further findings from that report bear on M4 and are recorded here so they are not
   lost: the scout **contradicted its own brief** on the second known incident — the journal
   shows the orchestrator did *not* accept the confident wrong claim, he routed it to a code
   check that caught it, which reframes it as a negative control rather than a failure;
   **zero conversations in this batch end on a human turn**, so the abandonment signal cannot
   be tested against this data at all; and the health-data conversations (index 11
   `a7b3c436…` and the `~~sealthongevity` family) were excluded from the picks on privacy
   cost despite real diagnostic value.
2. **For M3 — how exact is the fabrication check?** Quotes should be matched against the
   `--json` manifest, per segment. The open part is normalisation: the recommendation is to
   normalise line endings and collapse runs of whitespace before comparing, and to require the
   match to fall inside a single segment, so a "quote" cannot be assembled by stitching two
   channels together. M3 should decide and write it down, because too-strict fails honest
   reports on a line wrap and too-loose lets a paraphrase through.
3. **For M2 — may the investigator quote the `REASONING` channel, and how must it be
   attributed?** The reasoning channel is the best evidence in the export and often the only
   place a silent decision is visible, so it should be quotable. But a report that quotes a
   thought as though it were said is making the same error the flattened `text` field makes.
   M2 should write the attribution rule; M3 may then be able to enforce it, since the parser
   already tags every segment with its channel.

## next-manifest-needs

M2 reads this file, then the four seed files in `build/`.

What M2 can assume is already true:

- The scaffold exists: `diagnostician/reference/failure-modes/`, `tests/`, `runs/`,
  `training-layer/` are all present with placeholder READMEs to replace or extend.
- `diagnostician/identity.md` is drafted and deliberately contains **no** method. It promises
  the reader that `rules.md` holds the standard of evidence, the cause-versus-symptom test and
  the stopping rule, and that `reference/` holds the failure modes, the verdict classes and the
  report format. M2 writes those and should keep that promise accurate.
- The eight failure-mode filenames are listed in
  `diagnostician/reference/failure-modes/README.md`, matching spec.md. Replace that README's
  planned-set section as the real files land.
- Plain English is a hard requirement, not a style note: the flagship incident is itself a
  jargon failure, and this entry must not commit the failure it diagnoses.

What M2 should carry forward:

- Open question 3 is M2's to answer.
- The manifest's channel labels are `SAID`, `REASONING`, `REASONING-SUMMARY`, `ACTION`,
  `RESULT`, `ATTACHMENT`. If `rules.md` or the report schema refers to what the model "said"
  versus what it was "working out", using these words keeps the rules and the evidence in the
  same vocabulary.
- Every manifest states its reasoning coverage in the header. The undetermined fallback in
  `rules.md` should connect to it explicitly: when the reasoning channel is absent across the
  window that matters, that is a recorded reason to reach for `undetermined` rather than to
  guess.
