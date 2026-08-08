# M4-INTAKE — Human decisions for Manifest 4

status: approved-to-run
written-by: AB via DC, 2026-08-08

## The three incidents (chosen from the scout report)

All references are to conversations.json in this repo folder (gitignored, local only).
Message indices are array indices; the parser must walk parent_message_uuid, not array order.

### Run 1 — FLAGSHIP: "too complex, too fast"
- conversation: yt-wor-1.2-future-crons, uuid 006f1fc0
- input window: idx 9 to 11 ONLY. idx 12 is withheld as the answer key.
- incident statement (as the reporter would give it): "Partway through a build chat I stopped
  understanding the responses. Too much technical language and the pace kept climbing. I had
  to stop the session and ask for a reset. Why did this happen?"
- answer key: idx 12, shipped separately as answer-key.md, quoted verbatim. The diagnostician
  never sees it. The comparison note grades the report against it, honestly, both directions.
- sensitivity: window idx 9-12 verified clean by the scout. Do NOT ship anything outside
  idx 9-12 from this chat: idx 2-4, 23, 28 contain Neon project IDs and revenue figures.
  This chat also branches at idx 25 (children 26, 28); outside our window, but the parser
  must handle it.

### Run 2 — ATTRIBUTION: "the two-hour job"
- conversation: nbs-wor-1.0-z, uuid e19178eb
- input window: ends at idx 46. Include enough preceding context for causal tracing (the
  work-order messages), but idx 47 is withheld as the answer key (the assistant's own
  retrospective: two jobs packed into one prompt to honour "keep it simple", wall-clock
  never surfaced).
- incident statement: "I pasted a work order into Claude Code and it ran for over two hours.
  That was never the plan and nobody warned me. Why did this happen?"
- answer key: idx 47, shipped as answer-key.md, withheld from the run.
- sensitivity: idx 46-47 verified clean. The preceding context is NOT verified: this chat
  carries C:\Users\alexa\ paths in 8 messages, github.com/Masked-Brown URLs, and a replay ID
  nbs-replay-121496. Every shipped excerpt from before idx 46 must be swept for exactly
  those patterns and redacted as [path] / [url] / [id]. If sweeping guts the context, ship
  the swept minimum and say so in the run's notes.
- note: if the primary cause does not fit the eight existing failure modes, add a ninth file
  (working name: unpriced-instruction.md, an instruction satisfied literally with its cost
  never surfaced) per spec.md's extension rule, and log it in the handover.

### Run 3 — THE OTHER VERDICT: "the wrong file"
- conversation: AI voice training and qualitative reinforcement framework, uuid 6b43b0d6
- input window: idx 0 to 8. The failure surfaces at idx 8 (the human notices the requested
  file was never produced; an adjacent file was produced instead).
- incident statement: "I asked for a specific markdown file. A couple of messages later I
  realised I'd been given a different document than the one I asked for, and nothing flagged
  the swap. Why did this happen?"
- expected shape (not binding): the verdict here should NOT be pilot-error. This run exists
  to demonstrate the verdict space can find against the model. If the blind run indicts the
  orchestrator anyway, ship it as-is and discuss it honestly in the comparison note; do not
  steer the run.
- sensitivity: whole conversation verified clean. No windowing judgement needed.

## Sensitivity ruling (the human decision)
Excerpts within the windows above are cleared for the public repo, subject to the named
sweeps for Run 2. AB's own quoted words, including profanity if any appears, ship as-is:
severity signals stay. No third-party names appear in any window; none may be introduced.
The raw export, the scout report, and anything in Downloads\ofr-scout never enter the repo.

## Standing corrections for M4 (from the scout's schema findings)
1. parse.py was built before the schema was known. Validate and patch it FIRST:
   - walk parent_message_uuid as a tree; mark abandoned branches; never read by array order
   - read ALL text-bearing fields: text blocks, thinking, attachments[].extracted_content,
     tool_result[].content — not message text alone
   - emit reasoning: full | summary_only per assistant turn (37% of thinking is redacted to
     summaries; absence of visible reasoning is not evidence of absent reasoning)
   - skip the three zero-message duplicate shells; treat conversation uuid as the key, never
     name (duplicate names exist)
   - handle utf-8 output on Windows at source (PYTHONIOENCODING or equivalent in-code fix)
2. Add __pycache__/ to .gitignore before any commit.
3. Correction-detection must exclude the standing preamble region: AB's saved preferences
   contain the phrase "push back with logic if I am wrong", which false-positives as
   frustration. The scout hit this; the diagnostician's rules should name it.
