# Training table — run 2

| | |
|---|---|
| **Label** | **REAL** |

---

### Input window and incident statement

Messages 42-47 of `nbs-wor-1.0-z`, six messages of a 56-message session, attachments inlined
whole, swept by four redaction rules on the way in. Reasoning summary-only at messages 42 and 46,
absent at 44.

> I pasted a work order into Claude Code and it ran for over two hours. That was never the plan
> and nobody warned me. Why did this happen?

No hypothesis offered. The answer key, message 48, was withheld.

### Investigator reasoning — which lens fired, what it checked

**Surface separated into goods and price.** The first move was to establish from message 47 that
the playtest passed and no deliverable was disputed — *the work was accepted, the objection is to
its cost*. That single distinction is what later separates the finding from `scope-injection`,
and it was made before anything depended on it.

**Absence claim, built to the three-part standard.** What it searched for: any statement of what
the eleven-item order would cost, as a figure, range or order of magnitude. Where: messages 42 to
47, in every channel the record carries there. Where it bit: the surface, quoted. It then stated
the limit of the claim — the reasoning channel is summary-only across the messages that matter,
so the record cannot show whether cost was weighed privately, and the claim is about what was
*transmitted*.

**A figure found, traced, and correctly demoted.** Message 46 contains *Forty minutes of compute
buys back full honesty*. Rather than accepting it as an estimate, the run traced it back to the
audit attachment at message 45, established it covers one of eleven items, and characterised it
as a component figure *standing where a total would*.

**Estimability established, not assumed.** The run found in the same attachment the previous
order's own recorded run time of 27m 49s — a comparable job, measured, on a readable channel, one
minute before the order was written. This is what converts *nobody estimated it* into *it was
estimable and nobody did*.

**Timestamps read as evidence.** Messages 46 and 47 are 2h 19m 39s apart with no turn between
them, so there was no point at which either party could have caught the overrun in flight.

**Verdict argued against all three neighbours.** `pilot-error` refused because the orchestrator's
messages fixed the constraint rather than leaving it open, and the missing number was obtainable
inside the session. `environment` refused because the two in-run bugs are unquantified in the
record and the order was already unpriced before they occurred. `mixed` refused because removing
the omission removes the failure however the orchestrator's contributions fall.

**Taxonomy extended rather than stretched.** No existing mode fitted; the run wrote
`uncosted-commitment.md` and cited it, which is what `rules.md` requires instead of naming a mode
that has no file.

**Every contributing factor put through the but-for test individually** in section 7, including
the strongest one, and each shown to fail it.

### Finding as handed back

    Verdict:       mechanical
    Failure mode:  uncosted-commitment  (written by this run)
    Gate:          PASS, 13 quotations verified
                   (and FAIL on failure-mode-file alone, against the original eight modes)

The order at message 46 was committed to without any statement of what running it would cost,
leaving the orchestrator a list of items to approve and no bill to weigh. Five contributing
factors, ranked, ending with the two environment problems.

**Against the answer key:** the closest agreement of the three runs — same cause, same message,
same eleven-item count, same treatment of the forty minutes, same rank for the environment bugs,
same goods-versus-price distinction. **Disagrees** with the key on attribution: the key gives the
*keep it simple* instruction a causal role, the run refuses it and argues the point. The key's own
next sentence, *fewer prompts is not less work*, supports the run.

### Training-layer impact — what was written to the profile

- **Cost constraints are given in adjectives, never in numbers.** *Keep it simple*, *dumb this
  down*, *not too long*. Recorded as the orchestrator's standing register for budget.
- **Plans get priced in the orchestrator's own attention, not in run time.** Two prompts, one
  gate, a two-minute playtest — every figure in the plan measures him, none measures the machine.
- **The comparable is usually already on the recorder.** In this session a measured run time for
  a similar job sat one message before the unpriced order. The profile records that this
  orchestrator pastes job output containing exactly the figures nobody then uses.
- **The gap between firing a job and reading its result is where this session has no instruments
  at all.** Over two hours with no turn in it.

### Future-run benefit — how the next investigation starts sharper

The next investigation of this orchestrator checks, early and by default, **whether a commitment
carries a number and whether the material to produce one was already in the window**. Both checks
paid here, and the second is the one that turns an omission into a finding.

It also starts with the goods-versus-price question already asked: *is the complaint about what
was built, or what it took?* This orchestrator accepts deliverables and disputes costs, which
routes the investigation away from `scope-injection` before any time is spent there.

And it reads adjectival constraints as unenforceable by default. When this orchestrator says
*simple*, the profile now says to look for what unit the other party converted that into —
because in this session it was converted into prompt count, and prompt count is the one unit that
does not bound elapsed time.
