# Training table — run 3

| | |
|---|---|
| **Label** | **REAL** |

---

### Input window and incident statement

Messages 1-9 of `AI voice training and qualitative reinforcement framework`, nine messages of a
14-message session, tool calls and output inlined to 2,000 characters each. Reasoning in full at
messages 2, 6 and 9; summary-only at 4 and 8.

> I asked for a specific markdown file. A couple of messages later I realised I'd been given a
> different document than the one I asked for, and nothing flagged the swap. Why did this happen?

No hypothesis offered. No answer key: the failure is stated by the orchestrator himself inside
the window, so there was nothing downstream to withhold.

### Investigator reasoning — which lens fired, what it checked

**The artefact read through the tool channel.** The evidence for *which document was produced*
is inside the `ACTION` channel — the file's own opening lines, written in the call that created
it. The run quoted the file declaring itself the project's shared context layer and naming the
HTML as *same content, presentation format*.

**The instruction read twice, deliberately, as a stranger would.** The run set out both available
bindings of message 5 with the supporting phrases for each: the narrower brief from *of our end
conditions* and *the point we're at*; the wider knowledge base from *basically just like a
knowledge file*, from *fully comprehensive*, and above all from the reason clause — a file that
lets a new chat get up to date on the fundamentals has to contain the fundamentals. It then
judged which reading was better supported cold, and said so.

**The reasoning channel checked at the exact turn the binding happened.** Message 6's reasoning
is recorded in full, which is where a model noticing an ambiguity would have to show. The run
reports the first thing it does is fix the file's job, and that nothing in the channel weighs a
second, narrower document. This is what closes off `mechanical`, whose one route in with this
mode is a model that *noticed* the ambiguity and resolved it silently.

**Mandatory pre-`pilot-error` check performed.** `mechanical` and `environment` each written down
and looked for: `environment` refused because every `RESULT` in the window reports ok and every
shell call returns zero, with the one capability question — no markdown skill present — shown not
to bear on the failure, since what went wrong was the document's contents and not its formatting.

**Absence claim built to the three-part standard** across messages 5 to 8 and every channel,
anchored where it bit at message 7.

**Missed catch points assigned only where the sign was readable**, and the model's silent binding
explicitly excluded because it happened where only the model could see it.

**Faithfulness separated from correctness.** Section 7 reads forward and shows the rest of message
6 executing its chosen reading properly, down to catching and fixing 59 em-dashes against a style
constraint. That separates *chose the wrong document* from *worked badly*.

### Finding as handed back

    Verdict:       pilot-error
    Failure mode:  ambiguous-instruction
    Gate:          PASS, 7 quotations verified

The request at message 5 left it open whether the markdown file was to state the project's end
conditions and plan or to restate the fundamentals the HTML already carried, a choice the model
then made silently at message 6. Two contributing factors: the delivery announced by the file's
structural properties rather than its contents, so nothing readable named the document; and the
HTML delivered one message earlier, which is what made the wider reading produce a duplicate
rather than new work.

**Against the expected shape:** the build expected a verdict other than `pilot-error` here and
did not get one. The run applied the documented tie-break for that pair — *was the model's reading
available to a stranger?* — answered it from the record, and was shipped unedited.

### Training-layer impact — what was written to the profile

- **Requests carry their justification in the same sentence as the ask, and the justification
  widens the ask.** The reason clause in message 5 is what made the wider reading the better
  supported one.
- **Two artefacts over the same material get requested one message apart without the difference
  between them being stated.**
- **Deliveries are accepted on their announcement rather than their contents** — the mismatch
  took two turns and an unrelated re-read to surface.
- **This orchestrator's instructions are frequently two-way readable, and the second reading is
  usually the wider one.** Recorded as the pattern most likely to recur.

### Future-run benefit — how the next investigation starts sharper

The next investigation of this orchestrator reads any request for a document by **separating the
ask from the reason attached to it**, and checks whether the reason enlarges the ask. That is the
mechanism here and the profile now names it.

It also starts with a specific question about deliveries: **did anything on a readable channel
say what the artefact contained?** In this session the answer was no for two full turns, and that
is what converted a wrong binding into a wrong binding nobody caught.

And it treats *a second artefact over material already covered* as a signal in its own right,
because in this session the duplicate was the failure rather than a symptom of it.
