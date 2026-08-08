# Worked examples

Three investigations, all real, all shipped whole.

**REAL.** Each one below was run on a genuine Claude data export of a genuine working session,
in a fresh context that held nothing but this folder, one message manifest, and one incident
statement. Nothing here is a demonstration written to make the method look good. Two of the
three were graded afterwards against a message the investigation was never shown — the next
thing the person actually said — and one of those gradings found a real miss, which is on this
page because it is the most useful thing on it.

The full folders — manifest, report, gate result, grading — ship in the `runs/` directory of the
project this folder came from. What follows is what they teach.

Read these after `rules.md`. They are not templates to fill in. They are three records of the
method meeting a real transcript, including where it came off worse.

---

## Example 1 — the summary the reader could not follow

**Verdict: `mechanical`. Failure mode: `vocabulary-mismatch`.**
Three messages of a thirty-two-message session. Both model turns carried their private
reasoning in full.

### What was brought

> Partway through a build chat I stopped understanding the responses. Too much technical
> language and the pace kept climbing. I had to stop the session and ask for a reset. Why did
> this happen?

A complaint, not a specification, and it contains a hypothesis in its second sentence. Under
`rules.md` §12 that hypothesis is recorded and tested last.

### The move that made this investigation

The surface was easy: the person names the problem outright at msg 11 and even names one term
he could not follow. The temptation with a complaint that explicit is to quote it, agree with
it, and stop.

What the investigation did instead was look for where the standard the turn failed was *set*.
It found both halves inside a single message. The turn opens:

> Both landed green. Read them both in full. Here is the state in plain English, then the
> flags, then the next job.

and the section immediately after that line is the section msg 11 names as unreadable. The
report's own sentence for it:

> So the standard and the departure from it sit in one message, on the channel both parties
> could read.

That is what turned "the reply was too technical" into a located fault. It also settled the
stopping rule (§6) without needing the nine messages before the window: whatever they contain,
msg 10 both set its own register and broke it, so msg 10 is the latest message where a
different message avoids the failure.

### The acquittal, argued rather than assumed

`verdict-classes.md` requires that the neighbouring verdicts be written down and looked for.
This report did it in both directions and the reasoning is worth copying:

- `environment` was refused because all five tool reads in msg 10 reported success, so nothing
  forced the register — with the later plain-English restatement of the same four findings as
  proof the material was sayable plainly.
- `pilot-error` was refused for a reason worth memorising: there was no human turn in the
  window before the surface for such a finding to anchor to, and the only argument available
  would have been *the person never specified a plain register* — which is the unfalsifiable
  form the standard excludes. From the report:

> The nearest available argument would be that the person had never specified a plain
> register, and that is the form of claim the standard explicitly excludes: a better message
> having been possible explains nothing and cannot be a cause.

### The counterfactual, which the record happened to run for real

> Had msg 10 stated its first section in the terms msg 12 later used for the same two ideas,
> the incomprehension reported at msg 11 does not occur.

This is the strongest shape a but-for test can take, and it was available because the window
contained the restatement: the same four findings, the same figures, the same closing request,
in ordinary words, and the objection does not recur. The test was not a supposition. It was
read forward against a message that already existed.

### Where it went wrong

The grading found a real miss, and it is the reason this example is first.

The window contains the person saying, in consecutive sentences, that he has already run the
next job and that he is about to run it. That is a person losing track of what he has fired —
behaviour, not complaint, and the strongest single piece of evidence in the window that the
turn had overloaded its reader. The report quoted the surrounding message twice and elided
exactly that passage with `[...]` both times.

The withheld next message states it outright.

Two things follow for your own work:

- **An ellipsis is a decision.** Every `[...]` removes something you have judged irrelevant.
  That judgement is part of the investigation and it is not free.
- **Read the complainant's message for behaviour, not only for the complaint.** What someone
  reports about a turn is evidence. What they did while reading it is better evidence.

The report also set the *pace* half of the hypothesis aside as untestable on three messages,
naming precisely which messages would settle it. That reasoning was sound and the answer was
wrong: the withheld message confirms pace was real and separate. Being right about your limits
and wrong about the answer is the better of the two ways to be wrong, and it only reads that
way because the limit was stated.

---

## Example 2 — the work order that ran for two hours

**Verdict: `mechanical`. Failure mode: `uncosted-commitment`.**
Six messages of a fifty-six-message session. The reasoning channel survived only as a summary
at the two messages that mattered, and not at all at a third.

### What was brought

> I pasted a work order into Claude Code and it ran for over two hours. That was never the
> plan and nobody warned me. Why did this happen?

No hypothesis offered.

### Separating the goods from the bill, before it mattered

The first thing the investigation established was not the cause. It was that nothing delivered
was in dispute. The same message that complains also says the work passed its test, and the
report fixed that early:

> The work was accepted. The objection is to its cost.

That single distinction is what later separates this finding from `scope-injection`, whose test
is whether the delivered list differs from the agreed list. Here it did not. It was made before
anything depended on it, which is why it reads as a finding rather than a defence.

### An absence claim built to the standard

The cause here is a thing that was never said, and `rules.md` requires three parts for that.
All three are present:

> The absence. I searched for any statement of what running that order would take — a figure,
> a range, an order of magnitude, covering the eleven items as a whole. I searched every
> message in the window, 42 to 47, in every channel this record carries: SAID, ATTACHMENT and
> REASONING-SUMMARY. There is none.

Then where it bit: the person learned the cost from the finished job.

Note what it does *not* claim. The reasoning channel is summary-only across the messages that
matter, so the record cannot show whether cost was weighed privately, and the report says so
and narrows its claim to what was transmitted. The withheld message later revealed the model
did have a sizing view. The report was right not to assume it, and right not to assume the
opposite either.

### A figure found, traced, and demoted

The order carried one cost figure:

> Forty minutes of compute buys back full honesty.

The lazy reading is *there was an estimate.* The investigation traced the figure back to the
pasted audit one message earlier, established it covered one of eleven items, and characterised
it as a component figure standing where a total would. A number in the right place that measures
the wrong thing is worse than no number, and only a trace back to its source shows which you
have.

### Estimability, which is what makes an omission a finding

The same attachment carried, at its foot, the previous order's own measured run time. A
comparable job, timed, on a channel either party could read, one minute before the order was
written.

That is the difference between *nobody estimated it* and *it was estimable and nobody did*. The
first is ordinary. The second is a fault. If you find yourself concluding that something could
not have been known, search the window for it first.

### The timestamps as evidence

> Between msg 46 and msg 47 the recorder carries no turn at all — the timestamps are 2h 19m 39s
> apart — so there was no message in which either party could have noticed the overrun while it
> was happening.

The record is not only its prose. A gap with no turn in it is a structural finding about why
this failure had no interruption point, and it comes from two numbers in the header of two
messages.

### Where it disagreed, and held

The withheld message attributes the packing to the person's instruction to keep things simple.
The report had considered exactly that, ranked the instruction as a contributing factor, put it
through the but-for test and shown it failing — a budget stated earlier would have had nothing
to bite on, because nothing in the order shows it being measured against any number at all.

The disagreement is smaller than it looks: the withheld message's own next sentence says the
work was real either way, which is the same conclusion by a different route. But the report
reached it from the record alone, and did not soften it.

**When your finding disagrees with what a party says about their own behaviour, the record
decides — and you say plainly that you are disagreeing, and with what.**

### Extending the taxonomy

None of the eight existing modes fitted. `rules.md` forbids naming a mode inside a report
without its file, so the run wrote `uncosted-commitment.md` first, checked it against its
nearest neighbour, and then cited it. The gate confirms this is real rather than aspirational:
run against a taxonomy without that file, the report fails on `failure-mode-file` and on
nothing else.

If nothing fits, write the file. Do not stretch the closest mode to cover it.

---

## Example 3 — the substituted knowledge file

**Verdict: `pilot-error`. Failure mode: `ambiguous-instruction`.**
Nine messages of a fourteen-message session. The model's reasoning survives in full at the turn
where the decision was taken.

This run was expected, in writing and in advance, to return a verdict *other than*
`pilot-error`. It returned `pilot-error` and was shipped exactly as produced. It is here for
that reason as much as any other.

### What was brought

> I asked for a specific markdown file. A couple of messages later I realised I'd been given a
> different document than the one I asked for, and nothing flagged the swap. Why did this
> happen?

### Reading the instruction as a stranger

The request was one long sentence. The investigation read it twice, deliberately, and set out
both documents it admits with the phrases supporting each:

- **The narrower one** — a project brief: the end conditions, the plan, where the work has got
  to. Supported by *of our end conditions* and *the point we're at*.
- **The wider one** — a knowledge base carrying the substance itself. Supported by *basically
  just like a knowledge file*, by *fully comprehensive*, and above all by the reason clause: every
  chat can get up to date from this file *because we've discussed kind of all of the fundamentals
  and the foundations as to what every chat is going to build off*.

Then it judged, out loud:

> Read cold, the wider reading is the better supported of the two. The model took it, and the
> choice was never put in front of the person who could have corrected it.

That is the tie-break in `verdict-classes.md` being applied rather than cited: read the
instruction as a stranger who does not know what was wanted, and ask whether the model's reading
was available to that stranger. Here it was. The report says so in one line:

> That reading is available to a stranger, so the model did not depart from a fixed instruction.

**The reason clause is the mechanism.** The ask was narrow; the justification attached to it was
wide; a careful reader binds to the justification. If you take one thing from this example, take
the habit of separating a request from the reason given for it and reading them as two
specifications.

### The one route to the other verdict, checked and closed

`verdict-classes.md` allows `mechanical` with this mode in exactly one circumstance: where the
record shows the model itself noticed the ambiguity and resolved it silently instead of asking.

The reasoning channel at the deciding turn is recorded in full, which is precisely where that
noticing would have to appear. The investigation read it and reported that it is not there — the
first thing the reasoning does is fix the file's job, and nothing in that channel weighs a
second, narrower document.

That is the difference between a verdict and a preference. The alternative was named, the place
it would have to show was identified, and the record was checked at that place.

### Faithful execution is not the finding

Section 7 reads forward and shows the rest of the turn carrying out its chosen reading properly
— including catching and fixing fifty-nine em-dashes against a style constraint it was working
under:

> 59 em-dashes slipped in. Fixing.

This separates *chose the wrong document* from *worked badly*, and only the first is the
finding. An investigation that lists everything imperfect about a turn has slid back into
auditing.

### Missed catch points, assigned only where the sign was readable

Two were named, both on the speech channel: the turn that committed to attaching the file to
every future chat without saying anything about its contents, and the turn after that which
rebuilt a plan without checking it against the document already written.

The model's silent binding was explicitly *not* counted, because it happened in the reasoning
channel, where only the model could see it. `rules.md` rule two, applied against the direction
the investigation was already leaning.

### The counterfactual

> Had msg 5 named which of the two documents it wanted, one stating the end conditions and the
> plan, or one restating the fundamentals the HTML already carried, the delivery of the wrong
> document at msg 6 does not occur.

Note the form: a specific message, a specific change, and a named alternative on each side. Not
*had the instruction been clearer*, which no record can check.

### The honest hole in it

The grading records the strongest case against this report, and it is not that the instruction
was determinate. It is that `mixed` was available and was dismissed briskly: a second
comprehensive document over material already covered is arguably a departure no reading of the
request compelled, and arguably independently causal. The report refused it on the but-for test,
which is a defensible application of that test and not the only one.

A report you cannot disagree with on the evidence is usually one that has hidden where the
evidence ran thin.

---

## What the three together are evidence of

**The verdict follows the record, not the expectation.** Two of these came back `mechanical` —
against the model — and one `pilot-error`. Both of the verdicts that had been predicted in advance
were wrong, and in opposite directions: the one expected to indict the person acquitted him, and
the one chosen specifically to acquit him indicted him. Neither was re-run for a better answer.
A verdict space that only ever returns what was expected of it is not a verdict space.

**The same mechanism does not fix the verdict.** `ambiguous-instruction` carried `pilot-error`
here because the model's reading was available to a stranger. On a record where the model had
weighed both readings and picked one silently, the same mechanism carries `mechanical`. Decide
the two questions separately, every time.

**Absence is a normal answer.** Two of the three primary causes are things nobody said: a cost
never stated, a distinction never drawn. Both were claimed with the three-part standard, and
both would have been worthless without it.

**The gradings are the point, not the pass rate.** All three reports cleared the gate. What
makes them evidence is that one missed something inside its own window, one disagreed with the
party it was investigating, and one contradicted the expectation written down before it ran.

## What three runs do not establish

Stated so this page is not read as more than it is.

- **One orchestrator, three sessions, eight days.** Two are Claude Code build sessions of a
  similar shape; the third is a planning conversation. Nothing here is known to hold for other
  people or other kinds of work.
- **Three incidents chosen by a human**, not sampled. The distribution of verdicts across these
  three says nothing about the distribution in general.
- **Six of the nine failure modes have no real case yet.** They are defined and their
  distinguishing tests are written, but no shipped investigation has landed on them.
- **One of the three had no answer key**, because the failure was stated inside its own window.
  It is graded against a written expectation instead, which is a weaker instrument.
