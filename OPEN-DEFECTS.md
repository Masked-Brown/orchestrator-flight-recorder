# Open defects

What is weak, unproven, or out of scope. Written so a reader can decide what to trust before
trusting it, and so nothing here has to be discovered by someone who was relying on it.

Nothing on this list is hypothetical. Every item is either a hole in the machinery, a bound on
the evidence, or a boundary of the domain.

---

## In the machinery

### 1. Prescription detection is heuristic, and always will be

`check.py` blocks advice by matching phrasings — *next time*, *you should*, *the fix is*, *I
recommend*, and about forty more, plus a softer set (*should have*, *would have been better*)
that is only allowed when the sentence carries a message anchor, because that is what makes it a
counterfactual rather than a recommendation.

This is a word list. It catches the shapes advice actually takes and it will not catch a
prescription written in words nobody thought to list. A report that ends *the ambiguity would not
have survived a second pair of eyes* is advice, and no pattern here fires on it.

The word list is also deliberately narrower than it could be. The bare tokens `try`, `say`,
`state`, `write` and `claim` were tried and removed: they have ordinary non-prescriptive senses
that appear constantly in honest investigative prose, and a gate that fails good reports gets
worked around, after which it is enforcing nothing. The trade is stated rather than hidden. The
structural defences — the report must end at section 7, there is no recommendations section in
the schema, and a heading after the counterfactual is a blocking failure — do more work here than
the word list does.

### 2. The gate checks form, never correctness

Everything `check.py` enforces is mechanical: that quotations are verbatim, that there is exactly
one primary cause, that the verdict is one of five, that every factor points at a message, that
the counterfactual exists and nothing follows it, that a named failure mode has a file.

**A report can satisfy every one of those and still name the wrong cause.** The gate makes
fabrication and prescription impossible; it cannot make an investigation correct. That is what
the comparison notes in `runs/` are for, and they are graded by a human against a withheld
document, not by a script.

### 3. Quotation in italics escapes the checker

The report schema makes block quotes the only quoting device precisely so that every quotation
gets checked. `check.py` verifies block quotes and does not look inside running prose.

A report can therefore quote the record in *italics* inside a sentence and the passage is never
verified. Run 3's report does this in three places — the reasoning at message 6 and two phrases
in its contributing factors. They were checked by hand and are accurate, but they were not
checked by the machinery, and the machinery is the point.

Found while writing that run's notes; recorded rather than patched, because closing it properly
means deciding what a report may do with a three-word phrase, and that is a schema decision
rather than a regex.

### 4. A gate that could be made to exit 0 without reading anything — found and fixed

`--list-checks` prints the catalogue of checks and examines nothing. Handed a report as well, it
short-circuited, printed the catalogue, and exited **0** — the identical exit code a clean report
produces, and the only thing a CI step or a shell script reads. Any wrapper that ran
`check.py report.md --list-checks` would have reported a pass over a report the gate never
opened.

Fixed in M5: that combination is now refused with exit 2, and eight invocations that cannot check
anything are asserted in `tests/verify.py` to exit 2 and never print `PASS`.

**A correction to how this was first described**, because the repo does not get to round its own
history up. The human's final read flagged it as *check.py exits 0 when invoked without
`--manifest`*. That specific path was never broken: the missing-manifest guard has been in
`check.py` since it was written in M3 and exits 2, which `git log` shows. The flag was right that
a silent-pass route existed and wrong about which one, and the route it turned out to be is the
worse of the two — a missing manifest at least produces an error a person would read, whereas
`--list-checks` produces plausible-looking output and success. The real defect was that **no test
covered the command line at all**, so either could have regressed unnoticed. That gap is what the
human's instruction actually closed.

### 5. The parser can lose evidence to its own truncation cap

`--tool-io-limit` keeps the first N characters of tool arguments, tool output and attachment
text. It keeps a true prefix rather than a summary, so a quotation inside what was kept still
verifies and one outside it fails honestly instead of half-matching, and every capped segment
records how much was withheld.

But material past the cap is not in the record the investigator reads. Run 1 was built with a
2,000-character cap and 15,745 characters were withheld from a single tool result; the report
says so and states that nothing in its finding rests on that text. That is the right handling and
it is not the same as having the text. An investigation whose decisive evidence sits past the cap
will reach `undetermined` — correctly, but avoidably.

### 6. Schema drift

`parse.py` was rewritten against the actual structure of a Claude data export as it existed in
August 2026: messages as a tree linked by `parent_message_uuid`, text in content blocks rather
than the flattened `text` field, `thinking` blocks that may be replaced by summaries,
`attachments[].extracted_content`, `tool_result[].content`.

None of that is a published, stable interface. If the export format changes, the parser will
either fail loudly or — worse — read part of the record and silently drop the rest. There is no
version marker in the export to check against and no test that can detect drift, because the
fixtures are synthetic exports written to the schema the parser expects. `tests/parser-check.py`
proves the parser reads *this* schema correctly. It cannot prove the schema is still the schema.

If your manifest comes out thinner than your session felt, suspect this first.

### 7. The training layer does not learn by itself

`training-layer/AB.md` is populated from three real investigations, and every entry names the
runs it came from. But it is written by a person after the grading, not accumulated by a
mechanism. Nothing in this repo updates it when a new run happens; there is no code path from a
report to a profile.

It is a real accretion layer with real rows and a manual write step. Ship it as that.

---

## In the evidence

### 8. The evidence base is one orchestrator, three sessions, eight days

Every real run here comes from one person's own export, covering 2026-08-01 to 08. Two of the
three sessions are Claude Code build sessions of a similar shape; the third is a planning
conversation.

That is enough to show the method works on real transcripts and produces findings that survive
grading against withheld evidence. It is nowhere near enough to claim it generalises — to other
people, other kinds of work, other models, or longer horizons. The three incidents were chosen by
a human from a scout report, not sampled, so even the distribution of verdicts across them says
nothing about the distribution in general.

`training-layer/AB.md` carries the same warning about itself, and lists which of its six patterns
rest on one run rather than three.

### 9. Reasoning is only partly observable, which bounds every claim about it

The export does not reliably carry what the model was working out privately. In the batch this
repo was built from, a scout pass measured **37% of assistant reasoning surviving only as a
summary** rather than as the model's own words, with more absent entirely. (That figure is from
the raw export, which is gitignored — you cannot check it here, which is exactly why it is on
this list.)

The consequences are structural, not cosmetic:

- A finding that rests on the reasoning channel can only be made where the channel survived. Run
  2 hit this directly: the reasoning is summary-only at the two messages that matter, so its
  absence claim is explicitly narrowed to *what was transmitted*, and it says so. The withheld
  answer key later revealed the model did have a private view on the question. The report was
  right not to assume it — and right not to assume the opposite.
- `parse.py` labels every assistant turn `full`, `summary_only` or `absent` and prints the counts
  in the manifest header, and `rules.md` forbids quoting a summary as though it were the model's
  words or reasoning from a withheld block at all. That converts the problem into a stated bound
  rather than solving it.
- **Absence of visible reasoning is not evidence of absent reasoning.** Anything built on this
  tool inherits that.

### 10. The branch problem: a correction delivered as a prompt edit destroys its own signal

This one is a hole in the artefact, and every transcript diagnostician inherits it.

When someone corrects a model by *editing their earlier message and re-sending* rather than by
writing a new turn, the export keeps both versions as siblings under a shared parent. The
correction is real, it happened, and it leaves no message in the conversation saying so. The
signal that most reliably marks a failure — a person restating a requirement — is the signal
this workflow deletes.

`parse.py` walks the tree, marks abandoned branches and flags forks in the header, and `rules.md`
carries an explicit warning that a fork is *not* evidence of repetition or frustration. That
handles the false positive. It does not recover the missing evidence: an investigator reading a
session corrected entirely by prompt-editing sees a conversation that went smoothly.

The scout pass over this export hit the same thing from the other side — three "repeated
requirement" detections that all turned out to be branch points.

**If you work by editing prompts rather than by replying, this tool will systematically
under-read your failures.** No amount of parser work fixes that; the information is not in the
record.

### 11. Run 1's shipped record diverges from the one its investigator read

Run 2's redaction sweep ran *before* its investigation: `parse.py --redact` applies the rules on
the way into the manifest, so the record the investigator read, the record the gate matched
against, and the record in the repo are one record. That is the property worth having.

Run 1 does not have it. Its window was cleared as clean by an intake whose category list did not
include personal names or platform identifiers, and it carried both — a real name as the default
value of a configuration constant, and a real channel identifier twice inside a file path, on a
repository that is public under a pseudonymous account. The M4 recovery session caught it in the
pre-commit sweep and applied two rules, three replacements, regenerating the manifest
deterministically.

The result: the investigator read the unswept text and the repo ships the swept text. The
divergence is three strings wide, none of them quoted in the report or named in its reasoning,
and the gate re-run against the swept record still verifies all eleven quotations — so nothing in
the finding rests on what was removed. The property is still weaker for run 1 than for run 2, and
it is recorded in that run's notes and its comparison note rather than smoothed over.

The wider point, which is not fixed: **the sweep's category list was derived per-incident rather
than being a standing part of the pre-commit check.** The blind spot was structural, not a slip,
and the same shape of miss is available to the next person who ships an excerpt.

### 12. The ninth failure mode rests on one run

`uncosted-commitment` was written by run 2 under the taxonomy's extension rule, after checking all
eight existing modes and finding none fitted. It was reviewed against the failure-modes README's
four requirements and against its nearest neighbour before promotion, and the gate enforces the
rule that produced it: run against the original eight, that report fails on `failure-mode-file`
and on nothing else.

But it has exactly one supporting case. A mode with one instance is a hypothesis with a file. The
distinguishing test it gives against `scope-injection` — is the complaint about the goods or about
the bill — has been applied once, successfully, on the transcript that generated it. That is the
weakest form of evidence a taxonomy entry can have while still being real.

### 13. Six of the nine failure modes have no real case at all

Three modes carry a worked example from a shipped investigation. The other six —
`missing-context`, `stale-constraint`, `thread-overload`, `premature-parallelism`,
`scope-injection`, `unverified-claim-accepted` — are defined, with transcript signatures and
distinguishing tests written, and no investigation has landed on any of them.

Their files say so instead of carrying an invented example. They are untested, and an untested
mode is a mode that may turn out to be unusable, or to overlap one of its neighbours in ways only
a real transcript reveals.

### 14. The blind runs were isolated by protocol, not by mechanism

Each investigation ran in a fresh context whose entire world was a copy of `diagnostician/`, one
manifest, and one incident statement, with an instruction that the repository, the raw export and
every build document were off limits, and an inspection afterwards.

For runs 1 and 2 there is one piece of isolation that does not rest on instructions being obeyed:
**the answer keys did not exist on disk anywhere at the time the runs happened.** Everything else
does rest on it. The raw export was present and readable on the same machine, and nothing
mechanically prevented an investigator from going and finding the source conversation.

What can be said, and is said in each `run-notes.md`, is that the reports are wrong in ways a
contaminated run would not have been: run 1 missed a contradiction the key states outright, run 2
argues *against* the key's attribution and does not share its framing, and run 3 contradicted the
expectation written down for it in advance.

---

## Out of scope

The domain is locked and narrow on purpose: **why one AI-orchestrated working session failed,
traced to a specific behaviour in that conversation, from that session's own export. One session,
one stated incident, one investigation.**

These adjacent uses are not supported, and using it for them would produce confident, well-cited,
wrong output:

- **Security auditing.** It does not look for leaked credentials, injection, unsafe tool use or
  anything else in that family. It looks for one causal chain behind one stated complaint, and
  `rules.md` explicitly forbids widening scope to the most interesting thing found. A report here
  is not evidence that a session was safe.
- **General chat review.** Not a quality rater, not a satisfaction analyser, not a summariser. It
  needs a stated incident to fix its scope; without one it has nothing to investigate and will
  either invent a scope or find nothing.
- **Prompt improvement.** The opposite of what it does, structurally and by enforcement. If you
  want the fix, that is a different conversation — a better-informed one, which is the argument
  for the separation, but a different one.
- **Multi-session or cross-project analysis.** One session, one window. It has no mechanism for
  reasoning across conversations and no way to establish that two sessions are related beyond a
  person saying so.
- **Anything about a person beyond the record.** State of mind, skill, workload, intent. The
  stopping rule makes the recorder the boundary of the investigation, and a report that speculates
  past it stops being checkable.

---

## Housekeeping

- **No licence has been chosen.** The `README` says so. Until one is, the default applies and you
  should not assume permission to reuse.
- **Message numbering.** `parse.py` numbers from 1; the export's own message array is 0-based, and
  the build's intake used array indices. Everything public in this repo uses the manifest's
  1-based numbering, and each run's notes state its own mapping. If you compare a report against
  raw export JSON, expect the off-by-one and check the run notes first.
- **The build's own record is in `build/`**, including the handover files and the session
  touchdowns, and it contains a session that crashed mid-manifest and a recovery that found what
  it had left undone. That is on purpose. A diagnostician whose own build record is tidier than
  its subject matter is hiding something.
