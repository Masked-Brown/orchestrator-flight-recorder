# The report

Seven sections, in this order, and nothing after the seventh.

The shape is fixed for two reasons. It forces the investigation to answer the questions in the
order that keeps it honest — where it showed up, where it started, how it travelled, whose it
was, what it was, and how you know. And it is regular enough that a report can be checked
mechanically: quotes matched against the record, verdicts checked against the list, the ending
checked for an ending.

Some lines below are written in a fixed form for exactly that reason. They are marked
**fixed line** and the wording of the label matters.

---

## The heading block

Before section 1, three lines saying which recorder this report read. Copy the last two
straight from the top of the record you were given.

```
# Investigation: <short name for the incident>

    record         <name or path of the record you read>
    source-sha256  <the fingerprint from the record's header>
    window         messages <N>-<M> of "<conversation name>"
```

A report and a record are checked as a pair. If you were given a plain transcript with no
fingerprint, write `source-sha256  not recorded` and say so again in section 1.

---

## 1. Incident statement

The complaint restated in one line that names something findable in the record. This fixes what
you are investigating and, just as importantly, what you are not.

Then the reporter's hunch, if they gave one, recorded as given:

**Fixed line:** `Reporter's hypothesis: <as they put it>` — or `Reporter's hypothesis: none
offered.`

It gets tested like anything else, last, and it must be resolved somewhere in section 6 or 7:
confirmed, refined, or set aside with the reason. It is never the starting point.

## 2. Failure surface

Where the failure actually became visible. One message, or a small number, quoted.

This is the easy part and it is not the answer. Naming the surface is not a diagnosis; it is
the fixed point everything else is measured from.

At least one anchored quotation is required here.

## 3. Causal origin

The message where the fault entered the conversation. Quoted, anchored.

It may belong to either party. It may sit a long way upstream of the surface — that is the
normal case, and the distance is the point.

**It may also be an absence.** If nothing was ever said, the origin is the gap, and the claim
needs all three parts: what you searched for, the exact message range and channels you searched,
and the message where a party had to proceed without it. That last one is quoted, so this
section always carries at least one quotation even when the origin is a gap.

## 4. Propagation trace

The path from origin to surface, turn by turn. Not everything that happened in between — the
messages the fault actually travelled through, and what each one did to it: carried it
forward, compounded it, made it harder to see.

One line per step, each anchored:

```
- **msg <N> (<role>, <CHANNEL>)** — <what this turn did to the fault>
```

Then the places where it could have been stopped and was not:

**Fixed line:** `Missed catch points:` followed by a list in the same form — or `Missed catch
points: none.`

A missed catch point requires that the party could actually have seen the sign. If the only
indication at that moment was in the model's private reasoning, the person could not have
seen it, and it is not a missed catch point for them. Say instead that the sign existed but
was not on any channel they could read.

This section is what makes the report a path rather than a list. A trace with no direction of
travel is an inventory, and an inventory is not a diagnosis.

## 5. Verdict class

Whose failure it was.

**Fixed line:** `Verdict: <one of>` — `pilot-error`, `mechanical`, `environment`, `mixed`,
`undetermined`. Exactly one, spelled exactly as listed. What each one requires is in
`verdict-classes.md`.

Then a short justification, anchored, saying what in the record puts it in that class rather
than a neighbouring one.

When the verdict is `undetermined`, two more things are required: the live candidates the
record does admit, each anchored, and

**Fixed line:** `Would resolve it: <the obtainable evidence that would settle it>`

## 6. Primary cause

**Fixed line:** `Failure mode: <name of one file in failure-modes/, without the .md>`

Exactly one, and the file must exist. A mode may not be invented inside a report; if the
session failed in a way nothing covers, the file is written first.

Then one sentence naming the cause. One. If it needs an "and", you have two causes and one of
them belongs below.

Then, ranked by how much the outcome depended on each:

**Fixed line:** `Contributing factors:` followed by a numbered list, **every item carrying at
least one anchor** — or `Contributing factors: none.`

```
1. <the factor, in one line> — msg <N> (<role>, <CHANNEL>)
```

A factor with no anchor is an opinion. If the primary cause rests only on a summarised
reasoning channel with nothing else corroborating it, say so here, in one sentence.

## 7. Counterfactual test

The but-for reasoning, stated as a sentence you could check against the record:

```
Had msg <N> <specific change>, <the failure at msg M> does not occur.
```

Then the check itself: read forward from N and show what does not happen, anchored. And show
why this is upstream of every contributing factor — remove the primary cause and they stop
mattering; remove any of them and the failure still arrives.

Past tense, this session, always. A sentence that would still make sense in someone else's
transcript is a recommendation, and recommendations are a different document.

**The file ends here.** No summary, no lessons, no closing note, no offer of help.

---

## How quotations are written

Every quotation from the record follows one form:

```
<lead-in>, msg <N> (<role>, <CHANNEL>):

> <the exact words>
```

- `<N>` is the message number as it appears in the record. Numbers are global: message 26 is
  message 26 whether you were given the whole conversation or a slice of it.
- `<role>` is the record's own word — `human` or `assistant`.
- `<CHANNEL>` is the record's own label — `SAID`, `REASONING`, `REASONING-SUMMARY`, `ACTION`,
  `RESULT`, `ATTACHMENT`. If your record has no channel labels, everything in it is `SAID`,
  and section 1 should say that is the kind of record you had.

Five rules:

1. **Quote blocks are only ever quotations.** Nothing else in the report is written as an
   indented quote. Every one of them is checkable against the record, and every one gets
   checked.
2. **Every quote block is preceded by its anchor line**, immediately, with only a blank line
   between.
3. **Never use quotation marks to quote the record.** Speech marks around words invite the
   reader to treat them as verbatim without any of the machinery that makes them checkable. If
   a phrase is worth pointing at, point at it with a message number and quote it properly.
4. **One block, one message, one channel, one continuous stretch.** You may not assemble a
   quotation from two places, and you may not run two channels together — that is precisely
   the error that turns a thought into a statement.
5. **Shortening is allowed, with `[...]`.** Everything either side of it must still be exact
   and still be in the original order. Do not use it to bridge two different messages.

Rewrapping lines is fine; changing words is not. Nothing else about a quotation may be
adjusted — not capitalisation, not punctuation, not a typo. Fixing someone's typo inside a
quote is a small, well-meant fabrication, and the report's entire force rests on quotes being
exactly what was there.

---

## Skeleton

> **ILLUSTRATIVE.** Structure only. The angle-bracket placeholders are not findings, and the
> two short quotations below are invented to show the citation form — they are not from any
> real record.

```markdown
# Investigation: <short name>

    record         <name of the record>
    source-sha256  <fingerprint from its header>
    window         messages <N>-<M> of "<conversation name>"

## 1. Incident statement

<one line naming something findable in the record>

Reporter's hypothesis: <as given, or "none offered.">

## 2. Failure surface

<where it showed up>, msg <M> (assistant, SAID):

> <verbatim>

## 3. Causal origin

<where it entered, and why here>, msg <N> (human, SAID):

> <verbatim>

## 4. Propagation trace

- **msg <N> (human, SAID)** — <the fault enters>
- **msg <N+1> (assistant, REASONING)** — <it is resolved silently, one way>
- **msg <M> (assistant, SAID)** — <it surfaces>

Missed catch points:

- **msg <K> (human, SAID)** — <what was visible, on a channel they could read>

## 5. Verdict class

Verdict: <pilot-error | mechanical | environment | mixed | undetermined>

<why this class and not the neighbouring one, anchored>

## 6. Primary cause

Failure mode: <one file name from failure-modes/>

<one sentence.>

Contributing factors:

1. <factor> — msg <N> (<role>, <CHANNEL>)
2. <factor> — msg <N> (<role>, <CHANNEL>)

## 7. Counterfactual test

Had msg <N> <specific change>, <the failure at msg M> does not occur.

<the check, read forward from N, anchored — and why this sits upstream of every factor above>
```
