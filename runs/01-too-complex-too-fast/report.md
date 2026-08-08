# Investigation: the summary the reader could not follow

    record         message-manifest.md
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575
    window         messages 10-12 of "yt-wor-1.2-future-crons"

## 1. Incident statement

At msg 11 the person steering stopped the work and asked for the previous turn to be restated in simple English, naming the first section of msg 10 as the part he could not follow and naming one term in it that he did not know; the one decision msg 10 had asked him to make -- the settle lag -- was not made.

Reporter's hypothesis: Too much technical language and the pace kept climbing.

What was on the recorder: this is a full message manifest with channel labels, so what was sent, what the model worked out privately, what tools were called and what they returned are held apart. Both assistant turns in the window, msgs 10 and 12, carry their reasoning in full. The window is three messages -- 10, 11 and 12 of a conversation of 32 -- so nothing before msg 10 is on this recorder. The forks the header records sit outside the window, and none of these three messages is a branch. Five tool results inside msg 10 are shortened by the manifest rather than by the session; one of them had 15,745 characters withheld, so I do not have the full text of the two documents the model read. Nothing in this finding rests on that text.

## 2. Failure surface

Where the failure became visible, msg 11 (human, SAID):

> okay, overall, especially in the first section of your response, there is just too much language that I don't understand. I don't know what the byte identical guarantee outright is. [...] In general, simplify what are the four things that I need to know in simple English. Let's just consolidate where we're at. Simple English: you've moved too fast and too complex for me, so treat this as a kind of learning experience for you and the speed that I want to follow going forwards. This is talking about the settle lag, and in general, I need this simplified.

The passage he is pointing at is in the first section of the previous turn, and it is the only place in the record where that phrase occurs, msg 10 (assistant, SAID):

> The consolidator asked four questions where the schema reads two ways and answered all four under stated readings rather than stopping. I've reviewed all four and I'm confirming them. The important one: the schema specified a timestamp two incompatible ways, one of which would have broken the byte-identical guarantee outright. It chose the reading that preserves idempotence. That was the right tiebreak, because idempotence is the property the entire design rests on.

The same section carries the same idea twice more without a gloss, msg 10 (assistant, SAID):

> - **It is genuinely a projection, not a store.** Two consecutive runs byte-identical; the whole output deleted and rebuilt byte-identical. And it holds structurally rather than by care, because the script never reads its own previous output in any code path.

## 3. Causal origin

The fault entered at msg 10, in the same message that announced the standard it then missed. Its opening line fixes the register for the section that follows, msg 10 (assistant, SAID):

> Both landed green. Read them both in full. Here is the state in plain English, then the flags, then the next job.

The section immediately after that line is the one quoted in section 2, and it is the section msg 11 names. So the standard and the departure from it sit in one message, on the channel both parties could read.

What the register blocked is stated in the last line of the same turn, msg 10 (assistant, SAID):

> **The one open item for you:** confirm the settle lag ruling from four to five. Everything in that order downstream of step 3 depends on it, and it is a canon change, so it is yours rather than mine. If you would rather hold at four, say so and I will strip the change out and run the live pull alone.

The turn therefore asked for a judgment while writing the case for it in words the person judging had no definition for. The private working-out behind that turn is on the recorder in full and is entirely about which findings mattered and how to sequence the next jobs, msg 10 (assistant, REASONING):

> Both approaches landed well. Now I'm summarizing the key findings and flagging what needs decisions. The main issue is whether to increase SETTLE_LAG_DAYS from 4 to 5 days.

Searching the whole of msgs 10 and 12 on every channel for any weighing of whether the wording could be followed by its reader: the only mentions of the reader in msg 10's reasoning concern which findings to put in front of him, not how they would be phrased. The question of register does not appear there at all. It appears for the first time at msg 12, after the surface.

Why the origin is here rather than upstream: the window opens at msg 10, so I cannot see messages 1 to 9, and I checked whether that matters. It does not for this question. The stopping rule puts the origin at the latest message where a different message would have avoided the failure, and msg 10 is that message whatever messages 1 to 9 contain -- it both set its own register and departed from it inside itself, with no instruction needed from anyone to explain either half.

## 4. Propagation trace

- **msg 10 (assistant, RESULT)** -- five tool reads return the two source documents, none reporting an error; the material the summary was built from arrived intact, so nothing upstream forced the register that followed.
- **msg 10 (assistant, REASONING)** -- the working-out settles which findings to report, whether the settle-lag change should be its own job, and how to order the jobs after it; the question of whether the reader could follow the wording never enters it, so the choice of terms is never made as a choice.
- **msg 10 (assistant, SAID)** -- the fault enters: the turn promises plain English, then states the first section's findings in terms it does not define, and closes by asking for a ruling that depends on those findings being understood.
- **msg 11 (human, SAID)** -- the fault surfaces: the first section is named, one term is named, the work is halted for a consolidation in simple English, and the settle-lag ruling is not given.
- **msg 12 (assistant, REASONING)** -- the need is re-read as a straightforward answer plus the four points explained simply and the decision laid out so he can make the call himself.
- **msg 12 (assistant, SAID)** -- the same four findings are restated in ordinary words with the two terms defined, and the same ruling is asked for a second time; the decision is still outstanding where the window ends.

Missed catch points:

- **msg 10 (assistant, SAID)** -- the opening line of the turn set the register and the next section broke it. Both halves are in one message on the channel either party could read, so this was visible without any private information.

There is no human turn between the origin and the surface in this window: msg 10 is the first message on the recorder and msg 11 is the surface. So there is no missed catch point for the person steering. The one place where the fault could be seen forming before it was sent -- the absence of any register question in msg 10's working-out -- was on a channel only the model could read, and is not a missed catch point for him.

## 5. Verdict class

Verdict: mechanical

Before settling on this I looked for what the two neighbouring verdicts would need.

`environment` would need a tool error, a file not in the state either party believed, or a limit reached. The record shows the opposite: all five tool results in msg 10 report success, the first of them, msg 10 (assistant, RESULT):

> {"returncode":0,"stdout":"  444 /mnt/user-data/uploads/1786087335481_0109_cortex-consolidator_2026-08-07.md\n  306 /mnt/user-data/uploads/1786087339088_0109_spine-puller-window-gate_2026-08-07.md\n  750 total\n","stderr":""}

The other four carry the same success flag. The two documents read were dense technical records, but nothing constrained the summary to mirror them, and msg 12 is the proof: the same source material, the same four findings, in ordinary words.

`pilot-error` would need a message from the person that admitted the reading taken, or left out something the model needed and could not obtain -- anchored both at the instruction and at the point downstream where it bit. There is no human turn in this window before the surface, so there is nothing to anchor it to. The nearest available argument would be that the person had never specified a plain register, and that is the form of claim the standard explicitly excludes: a better message having been possible explains nothing and cannot be a cause.

What puts it in `mechanical` is that the determining standard in this window was one the model set for itself and then missed within the same message -- plain English announced in msg 10's opening line, and the section that immediately follows it named at msg 11 as the part that could not be followed -- and that nothing outside the model is needed to account for either half. The model's own account of the turn agrees on the substance, msg 12 (assistant, SAID):

> Fair. I went too technical. Let me fix both things.

The limit worth stating once: messages 1 to 9 are not on this recorder. This verdict rests on what messages 10 to 12 contain.

## 6. Primary cause

Failure mode: vocabulary-mismatch

Msg 10 stated the findings supporting a decision it was asking the person to make in terms it never defined, so he could not judge the decision and stopped the work at msg 11 to ask for the same material in ordinary words.

Contributing factors:

1. The turn carried two job reviews, four findings, two scope additions, a nine-row revised sequence and a complete work order for the next job in one message, so the undefined terms arrived inside a turn that already took a long time to get through -- msg 10 (assistant, SAID)
2. The only thing asked of the person sits in the last line of that turn, behind all of it -- msg 10 (assistant, SAID)

The reporter's hypothesis resolves as refined. Its first half is confirmed and is the finding: the language is what he names at msg 11, and he names the section and the term. Its second half, that the pace kept climbing, I could not test on this recorder and have set aside. A pace finding would point at `thread-overload` or `premature-parallelism`, and neither can be evidenced here. Thread overload requires a count of unresolved items rising across turns; the only open item in this window, the settle-lag ruling, is raised at msg 10 and raised again at msg 12 rather than dropped. Premature parallelism requires new work starting before existing work is confirmed; msg 10 does the reverse, marking the next job as running alone and placing every other job after it. What I can say about volume is a statement about one message, factor 1 above, not about a climb across a session. Messages 1 to 9 of this same conversation would settle the pace half.

## 7. Counterfactual test

Had msg 10 stated its first section in the terms msg 12 later used for the same two ideas, the incomprehension reported at msg 11 does not occur.

The check, read forward from msg 10. The complaint at msg 11 has exactly one object: the first section, and one phrase in it, which occurs in the record only in the msg 10 paragraph quoted in section 2. With that phrase carrying its meaning where it was used, the sentence at msg 11 has nothing to point at.

That the same content survives the change is not a supposition; the record contains it. Msg 12 (assistant, SAID):

> **"Byte-identical"** just means the file comes out exactly the same, character for character. When I say two runs are byte-identical, I mean: run it, run it again, and the second run produced a file with not a single character different from the first.

And msg 12 (assistant, SAID):

> **"Idempotent"** is the same idea in one word. Running it twice gives the same result as running it once.

Msg 12 carries the same four findings, the same evidence figures and the same closing request, msg 12 (assistant, SAID):

> **The one thing I need from you before 2b runs:** yes or no on the settle lag going from four days to five.

So nothing the person needed depended on the register of msg 10, and the objection he raised at msg 11 has no target in msg 12.

This sits upstream of both contributing factors. Remove the primary cause and they stop mattering: msg 12 is a long turn that still ends on the same request placed last, and the objection of msg 11 does not apply to it. Remove either factor and the failure still arrives: a shorter msg 10, or one that opened with the request instead of closing on it, still puts the undefined terms of the first section between the person and the ruling -- and it is that section, specifically, that msg 11 names.
