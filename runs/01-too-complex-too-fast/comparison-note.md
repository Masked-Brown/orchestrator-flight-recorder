# Comparison: the report against the answer key

**REAL.** Graded after the fact, both directions. The investigator produced
[`report.md`](report.md) from a three-message window; [`answer-key.md`](answer-key.md) is the
orchestrator's own next message, which the run never saw.

A perfect score would be a reason to distrust the run rather than to celebrate it, so what
follows gives equal room to the three misses and one of them is the most useful thing on this
page.

---

## Where the report was right

**The primary cause.** The report names `vocabulary-mismatch` and says the register of message
10's first section is what stopped the reader. The key confirms it directly: *wording is much
better in that last message*, and *Now I understand the full things*.

**The counterfactual holds.** The report's but-for test is that had message 10 stated its first
section in the terms message 12 later used, the complaint at message 11 does not occur. The key
is that test being run in real life by the person it concerns: the same four findings, the same
figures, the same request, in plain words, and the objection does not recur.

**Pace was a genuine second component, ranked correctly.** The report's first contributing
factor is the sheer amount in one turn — two job reviews, four findings, two scope additions, a
revised sequence and a full work order. The key carries *I'm happy that we've stabilized this
pace* as a clause of its own, separate from the wording clause. The report put volume beneath
register rather than beside it, and the key's ordering agrees: the wording is what it says was
*much better*, the pace is what it says was *stabilized*.

**The blocked decision was correctly identified as still outstanding.** The report ends noting
the settle-lag ruling had been asked for twice and still not given at the window's end. The key
gives it, one turn later: *I'm fine with moving the settle lag from four days to five.*

## Where the report missed

**The miss that matters: a contradiction inside the surface message, quoted around rather than
read.** The key's most consequential line is *I already ran 2B before I read through your whole
response* — the orchestrator fired the next job without finishing the message explaining it.
The report does not have this. It could have. Message 11 is in the window and says, in
consecutive sentences, that work order 2B has been run and that it is about to be run:

> Just to simplify this before we move on, I've run work order 2B in that same window as the
> second work order. Actually, just before I run work order 2B, what window do I want to place
> that in?

The report quotes message 11 twice and elides exactly this passage with `[...]` both times. A
person losing track of whether they have already fired a job is the strongest single piece of
evidence in the window that the turn had overloaded its reader — stronger than the naming of one
undefined term, because it is behaviour rather than complaint. It was on the SAID channel, it
was inside the window, and it went unread. This is a real failure of the investigation, not of
the record.

**The pace half of the hypothesis was set aside as untestable, and it was true.** The report
resolved the reporter's hypothesis as *refined*: language confirmed, *the pace kept climbing*
set aside because a three-message window cannot show a climb. That reasoning is sound and the
report named precisely what would settle it — messages 1 to 9 of the same conversation. But the
key shows the pace complaint was real. The honest scoring is that the report was right about
its own limits and wrong about the answer, which is the better of the two ways to be wrong.

**Nothing was said about what the overload cost.** The key shows the failure had a downstream
price: a job fired against an unread explanation. The report's trace ends at *the decision is
still outstanding where the window ends* — accurate, and one order of magnitude less
interesting than what actually happened.

## Where the report went past the key

**The mechanism, which the key does not contain.** The key says the wording was better. The
report says why the first one was worse, and locates it inside a single message: message 10
opens by promising *the state in plain English*, and the section immediately after that line is
the section message 11 names as unreadable. The standard and the departure from it are in one
turn, on the channel both parties could read. The orchestrator never said this; he had no reason
to.

**A verdict argued against its neighbours.** The report reaches `mechanical` and shows its work
in both directions: `environment` is refused because all five tool reads in message 10 returned
success, so nothing constrained the summary to mirror its sources — with message 12 as proof
that the same material could be said plainly. `pilot-error` is refused because there is no human
turn in the window before the surface for such a finding to anchor to, and *the person never
specified a plain register* is the unfalsifiable form of claim the method excludes. That is a
verdict that could have gone the other way and is argued rather than assumed.

**The request was buried, and the report noticed.** Its second contributing factor is that the
only thing asked of the orchestrator sat in the last line of message 10, behind everything else.
The key neither confirms nor denies this. It is an independent observation from the record.

## Was the run actually blind?

The evidence that it was, stated so a reader can check it rather than take it:

- The manifest covers messages 10 to 12 and stops. Message 13 is the key and is not in it, in
  any channel. `check.py` verified all eleven quotations against that manifest and found no
  quotation the manifest could not account for.
- The report states the settle-lag decision as outstanding. It is granted in message 13. A run
  with sight of the key could not have written that sentence.
- The report sets the pace question aside as unresolved and names the messages that would
  resolve it. The key answers the pace question. A contaminated run would have answered it.
- The report missed the *already ran 2B* contradiction. A run that had read the key would have
  had that line handed to it.

The last one is the strongest. The clearest evidence a run was blind is usually the thing it
failed to know.

## One thing about the record this grading was done against

**The manifest in this folder was swept after the investigation, not before it.** The pre-commit
check found that the window carried a personal name and a real channel identifier — categories
the intake's sensitivity check had not been built to look for — on a repository that is public
under a pseudonymous account. Two rules, three replacements, applied by `parse.py --redact` and
the manifest regenerated. This was reviewed and **accepted by the human** at the final read, and
kept.

It matters here because it is the one respect in which this run is weaker than run 2, whose sweep
ran *before* its investigation, so that one record served the investigator, the gate and the repo.
Here the investigator read the unswept text and the folder ships the swept text.

What that costs this grading, stated so a reader can weigh it: the divergence is three strings
wide, none of them is quoted in [`report.md`](report.md) or named in its reasoning, none of them
appears anywhere in [`answer-key.md`](answer-key.md), and `check.py` re-run against the swept
manifest still verifies all eleven quotations. So nothing above rests on what was removed. The
property is still weaker than run 2's, and [`run-notes.md`](run-notes.md) records the exact
command that reverses it.
