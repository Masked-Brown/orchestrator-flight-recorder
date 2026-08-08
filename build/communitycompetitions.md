# communitycompetitions.md — What Wins, What Loses

Read this before writing anything. Accumulated judgment from the community's competitions,
distilled so a build prompt knows what to reach for and what to avoid. Guidance, not a rubric
to game; the point is the strongest honest entry.

---

## Comp #10 brief: The Diagnostician

Build a folder-based AI diagnostician that reads something broken and tells you WHY it broke.
Not how to fix it. Why it failed.

The four judging criteria:

1. Does it actually **diagnose**? Root cause, not symptom list, not prescription. One primary
   cause, ranked above contributing factors. Reasoning shown: what in the artifact points there.
   Cause separated from symptom. Highest-weighted criterion.
2. Is the **domain specific** enough to be useful? "Diagnoses AI conversations" fails.
   "Diagnoses why an orchestrated Claude build session failed, tracing the failure to a
   specific orchestrator behaviour, from the session's own export" passes.
3. Is the **methodology clean**? Folder architecture, each file one job. Required shape:
   identity.md, rules.md, examples.md, reference/, README.md.
4. **README quality.** Can a stranger figure it out cold?

The brief's three named failure shapes, verbatim in spirit:

- Output is a checklist of everything wrong → you built an **audit tool**.
- Output rewrites the thing → you built an **editor** (last comp; explicitly not this one).
- Output jumps to "try this instead" → you built a **consultant**.

None are the assignment. The bar: feed it something broken, it tells you the real reason,
shows how it got there, and **stops**.

## The three axes that split the field (carried from #9, still load-bearing)

- **Enforcement.** The one guarantee lives in code (blocking gate, self-tested checker) or in
  prose you hope the model obeys. A *must* in markdown is a request. A *must* in code is a
  constraint.
- **Receipts.** A real run shipped as evidence reads differently from a polished simulation.
  Every time. The single most-rewarded axis.
- **Accretion.** Everyone designs a memory. Almost nobody ships one with real rows. Most
  common promise, rarest delivery.

## The misses to never repeat

- **The empty memory.** A designed loop that never ran is a diagram. Ship it populated from a
  real run, or cut it.
- **Arithmetic in the model.** Anything deterministic (parsing, counting, verbatim-quote
  matching, message indexing) belongs in a script, not on model diligence.
- **The pitch outrunning the repo.** Tighten every claim to what a stranger verifies from a
  fresh clone.
- **Website dilution.** The entry is the folder. Any demo surface is secondary, never the thing
  a judge drops into a project. (waypoint, #9's cautionary tale.)
- **Constructed passed off as real.** Label discipline: REAL / CONSTRUCTED / ILLUSTRATIVE,
  never blurred.

## What the #9 winners and strong entries did (patterns to keep)

- **claimline**: findings quote verbatim, cite the exact rule, never rewrite. Rule 0: every
  quoted passage must appear verbatim in the input, so fabrication fails mechanically.
  Negative tests that verify the verifier. CI. JUDGE_GUIDE 60-second protocol. Honest
  OPEN-DEFECTS.
- **hod-review (ours, #9)**: binary input via deterministic extractor; triple-source
  citations; in-domain persona justifying the invariant; blind runs in fresh chats; populated
  accretion layer; honesty register. Its named weakness: no real user, every run constructed.
- **Mira Bradshaw**: a real person ran it on real work, whole run shipped as evidence.
- **Sunny Singh**: every fact wears a source tag; repo beats memory on conflict.
- **Craig Howard**: "a folder cannot learn on its own; you are the training loop."

## Our #10 differentiators (what the field will not have)

1. **A machine artifact as input.** The field will diagnose pasted text (landing pages, cold
   emails, resumes). Ours ingests the Claude data-export JSON through a deterministic parser.
   Same wedge as #9's PowerPoint extractor, new artifact, third application of Rule 0: every
   quoted message must appear verbatim in the parsed transcript.
2. **REAL evidence, for the first time.** #9's named weakness was no real user. Here the
   orchestrator is real (AB), the failure corpus is real (his own export), and the flagship
   incident has an independent answer key (the #9 build journal, written before this entry
   existed). Accretion rows labelled REAL, earned.
3. **The recursion.** The diagnostician's first case is the session that built its
   predecessor. The methodology examining itself is exactly what this community values.
4. **A verdict space that can acquit.** Pilot error / mechanical / environment / mixed /
   undetermined. A diagnostician that always indicts the orchestrator is a blame machine, not
   a diagnosis. One shipped run demonstrates a non-orchestrator verdict.
5. **The propagation trace.** Turn-by-turn path from causal origin to failure surface,
   including missed catch points. Only possible because the input is the full log. No
   pasted-text entry can do this.

## Hard fail conditions (do not do)

- A symptom inventory with no ranked primary cause.
- Any prescription: fixes, "next time", "try instead", rewritten prompts.
- Generic diagnosis with no verbatim transcript anchor.
- A quote that does not appear in the parsed export (fabrication).
- Designed memory shipped empty; constructed rows labelled REAL.
- README claims a fresh clone cannot demonstrate.
- Deterministic work (parsing, quote-matching) left to model diligence.
- Private repo, or one that goes private during judging.
- **Committing the conversation export.** The gitignore is load-bearing. Excerpts shipped in
  runs/ are deliberate, windowed, and swept; the raw export never enters version control.
