# Investigation: the substituted knowledge file

    record         message-manifest.md
    source-sha256  50ff77f77041ee062e46a72909d9139fee6f0a9b4f092f1dfae4a83e9264a575
    window         messages 1-9 of "AI voice training and qualitative reinforcement framework"

## 1. Incident statement

A comprehensive markdown file was asked for at msg 5; the file delivered at msg 6 was a
7,322-word canonical knowledge base restating the material already carried by the HTML
reference built one message earlier, and the mismatch is stated for the first time at msg 9.

Reporter's hypothesis: none offered.

## 2. Failure surface

The document that was delivered, written into the file's own opening lines, msg 6 (assistant,
ACTION):

> **Companion artifact:** `voice-layer-reference.html` (Project Reference 01, same content, presentation format)

The file's statement of its own job, in the same write call, msg 6 (assistant, ACTION):

> This is the shared context layer for the whole project. It exists so that eleven parallel conversations do not each rediscover the same fundamentals, contradict each other, or drift.

The validation run in the same message reports the finished file at 7,322 words, msg 6
(assistant, RESULT).

It did not become visible as a mismatch for two further turns. Where it surfaced, msg 9
(human, SAID):

> I realize you haven't really produced the Markdown file that I wanted a couple of messages ago. I just want you to push a Markdown file of my end conditions, what my initial message was aiming at, because you produced the voicelayer knowledge.md. I'm looking for a project knowledge document.

A note on this recorder before going further. The manifest carries channel labels and the
model's private reasoning is recorded in full at msg 6, the message where the decision was
taken. It is summary-only at msgs 4 and 8. Tool calls and tool output are inlined only to
their first 2,000 characters, so the delivered file is read here through its opening text, the
section sets named in the write calls, and the validation output, not in full.

## 3. Causal origin

The fault enters at the request itself. One message earlier the same material had already been
delivered as a long HTML document, asked for at msg 3 (human, SAID):

> I want you to produce an HTML distillation and summary of this full process, everything that I mentioned in the bit above the divider.

The request for the markdown file then arrived without saying how the two documents were to
differ, msg 5 (human, SAID):

> I also want you to produce a comprehensive Markdown file initially of our end conditions, everything that I've mentioned that we want to discuss, basically just like a knowledge file. Every chat can go up to date in terms of the point we're at, because we've discussed kind of all of the fundamentals and the foundations as to what every chat is going to build off in this conversation. Just a fully comprehensive Markdown file around everything that we've mentioned - all the specific points, involvements, and conditions, almost just taking all of our current messages in this chat and building that into a proper file.

Two documents fit that sentence, and a reader who did not already know which was wanted could
have built either.

The narrower one is a project brief: the end conditions, the plan, and where the work has got
to. That reading is supported by *of our end conditions* and by *the point we're at*. It is the
document msg 9 turns out to have wanted.

The wider one is a knowledge base that carries the substance itself. That reading is supported
by *basically just like a knowledge file*, by *fully comprehensive [...] around everything that
we've mentioned*, and most of all by the reason clause: every chat can get up to date from this
file *because we've discussed kind of all of the fundamentals and the foundations as to what
every chat is going to build off*. A file that lets a new chat get up to date on the
fundamentals has to contain the fundamentals. The closing phrase, *almost just taking all of our
current messages in this chat and building that into a proper file*, points the same way, since
the messages of this chat include the two long substantive replies at msgs 2 and 4.

Read cold, the wider reading is the better supported of the two. The model took it, and the
choice was never put in front of the person who could have corrected it.

## 4. Propagation trace

- **msg 5 (human, SAID)** — the fault enters: one request, two documents available, and no statement of how the markdown file was to differ from the HTML delivered at msg 4.
- **msg 6 (assistant, REASONING)** — the choice is made silently. The first thing the recorded reasoning does is fix the file's job for itself: *The user needs a comprehensive Markdown knowledge file that serves as a canonical reference for all future chats, capturing the end conditions, foundational concepts, and key discussion points.* Nothing else in that channel weighs a second, narrower document; the only size question it settles is how long to make the one it has chosen.
- **msg 6 (assistant, REASONING)** — the choice compounds. The eleven spawn prompts are folded into the same file rather than sent in the reply, on the reasoning that one canonical document is better, which widens the file again.
- **msg 6 (assistant, ACTION)** — the reading is written into the artefact. The file declares itself the shared context layer for the project and names itself the same content as the HTML in another format.
- **msg 6 (assistant, SAID)** — the fault becomes harder to see. The delivery is announced by the file's structural properties, not by its contents.
- **msg 7 (human, SAID)** — carried forward. The delivered file is accepted as the thing that will be attached to every spawned chat, and the turn's attention goes to the HTML.
- **msg 8 (assistant, SAID)** — carried forward. The chat list is rebuilt as K1 to K9, superseding the register inside the delivered file, with no reference to that file at all.
- **msg 9 (human, SAID)** — the mismatch surfaces.

On the silence itself, an absence claim. I searched for any statement, by either party, naming
which of the two documents the markdown file was to be, or any question asking which. I
searched messages 5 to 8 in every channel the manifest carries for them: SAID, REASONING (full
at msg 6), REASONING-SUMMARY (msg 8), ACTION and RESULT. There is none. Where it bit, msg 7
(human, SAID):

> What I'm going to do is I'm going to attach the main full Markdown file that you produce so far, just everything that I'm doing in this project, and an initial prompt which you need to design for each and every chat once we finalize them.

Missed catch points:

- **msg 7 (human, SAID)** — the file had been presented at msg 6 and is named here as the thing to attach to every chat. The sign was on a channel that could be read: the file itself. This turn states instead that the HTML has been read, *I've just read through the HTML, and I've got loads to add*, and commits to the markdown file without saying anything about its contents.
- **msg 8 (assistant, SAID)** — msg 7 had just named the file's intended use, as an attachment carried into every spawned chat alongside a short per-chat prompt. That use was on the SAID channel and readable. The reply rebuilds the chat list without checking it against the 7,322-word document already written.

The model's silent binding at msg 6 is not a missed catch point for the person. It happened in
the reasoning channel, which only the model could see.

## 5. Verdict class

Verdict: pilot-error

Both halves are on the record. Msg 5 (human, SAID) did not determine which of two documents was
wanted, and its own reason clause points at the wider one. Msg 6 (assistant, REASONING) is where
that under-determination bit: the model had to fix the file's job before it could write
anything, and it fixed it in the first line of its reasoning.

I checked the two neighbouring verdicts before settling on this one.

`mechanical` would need msg 5 to have been determinate, one reasonable reading, with the model
then going outside it. It fails on that first half. The request names the artefact *a knowledge
file*, asks for it to be *fully comprehensive*, and grounds it in the fundamentals every chat
will build off. The delivered file is titled a knowledge file and contains those things. That
reading is available to a stranger, so the model did not depart from a fixed instruction.

`environment` would need a tool error, a file not in the state either party believed, a stated
limit, or material demonstrably out of view. Every RESULT in messages 1 to 9 reports ok, and
every bash call returns returncode 0. The one capability question in the window is at msg 6,
where a check of the skills directory finds no markdown skill and the model proceeds without
one; the failure does not follow from that, since what went wrong was the document's contents,
not its formatting. There is no environment trace here.

`mixed` would need two independent causes, each necessary. The other things that went wrong in
this window, the opaque delivery line and the two turns before anyone looked, do not survive the
removal of msg 5's under-determination as causes of this failure. They shaped how long it stood,
not that it happened.

## 6. Primary cause

Failure mode: ambiguous-instruction

The request at msg 5 left it open whether the markdown file was to state the project's end
conditions and plan or to restate the fundamentals the HTML already carried, a choice the model
then made silently at msg 6.

Contributing factors:

1. The delivery was announced by the file's structural properties rather than by what was in it, so nothing on a channel the person could read named the document — msg 6 (assistant, SAID), where the finished file is reported as *11 sections, canonical, versioned, with a change log so it survives contact with eleven chats*.
2. A comprehensive document over the same material had been delivered one message earlier, which is what made the wider reading of msg 5 produce a duplicate rather than new work — msg 4 (assistant, ACTION), whose write calls cover mechanism, elicitation, representation, pipeline, evaluation, product and research, the same set the msg 6 write calls cover again.

## 7. Counterfactual test

Had msg 5 named which of the two documents it wanted, one stating the end conditions and the
plan, or one restating the fundamentals the HTML already carried, the delivery of the wrong
document at msg 6 does not occur.

Read forward from msg 5. The first thing msg 6 (assistant, REASONING) does is fix the file's
job, and with that fixed by msg 5 there is nothing left for it to fix. Everything after that
point in msg 6 is faithful execution of the reading it took: it wrote the end conditions as
section 1.2, aimed the file at the per-chat context role, validated the structure, and found and
corrected 59 em-dashes against a style constraint it was operating under, msg 6 (assistant,
SAID):

> 59 em-dashes slipped in. Fixing.

The window contains no instance of this model declining or departing from a brief that was
stated: at msg 4 it executed the HTML brief from msg 3, and msg 7 raises no objection to that
document. With the kind of document fixed at msg 5, msg 6 delivers the brief that msg 9 asks
for, and msg 9's complaint has nothing to attach to.

This sits upstream of both contributing factors. Remove the under-determination and factor 1
stops mattering: an announcement written in structural terms conceals nothing when the document
underneath it is the one that was wanted. Factor 2 stops mattering too: a second document scoped
as a brief is not a duplicate of the HTML however much ground the HTML covered. Remove either
factor on its own and the failure still arrives. Had msg 6 described the file's contents
plainly, the file delivered would still have been the wider document, and msg 9 still asks for
the one it did not get, only sooner. Had the HTML at msg 4 never been written, msg 5 still
admits both readings, and the model still binds one of them in the first line of its reasoning
at msg 6.
