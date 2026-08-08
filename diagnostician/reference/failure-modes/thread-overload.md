# Thread overload

**In one line.** Turns that are each perfectly reasonable, but which together open more questions
than they close, until things start falling on the floor.

## What it is

A failure of the **sequence**, not of any message in it. Every individual turn passes review.
Read one at a time, there is nothing to object to — which is exactly why this survives, and why
it cannot be found by looking harder at any single message.

What goes wrong is arithmetic. Questions get asked and not answered. Decisions get raised and not
taken. Tasks get named and not finished. Each one is small and each one is fine, and the number
of them in flight keeps climbing until something that mattered drops out unnoticed.

The surface is usually an **omission**, not an error. Nothing was done wrong; something simply
never got done, and nobody spotted the gap because there was too much in the air to notice one
thing missing from it.

## What it looks like in the record

- **A rising count of open items.** This is the actual evidence. Walk the window and track every
  question asked, decision raised and task named, marking where each one is answered, taken or
  finished. In this mode the count rises and does not come back down.
- **Turns carrying several distinct asks at once**, repeatedly, from either party — three
  questions in one message, four topics in one reply.
- **Items disappearing without resolution.** Not decided against, not dropped on purpose. Just
  never mentioned again.
- **Later turns treating unsettled things as settled**, because so much has gone past that
  nobody can remember which of them was actually agreed.
- **The complaint that brought you here is often "it forgot" or "it never did X."**

## The count is the claim

If you name this mode, you should be able to list the open items and the message each one entered
at. That list is what makes the finding checkable, and without it "there was too much going on"
is an impression rather than a diagnosis. Put the items in the propagation trace with their
anchors.

## Telling it apart

| Easily confused with | The question that separates them |
|---|---|
| `premature-parallelism` | **Count** or **order**? Overload is about how many things are unresolved at once — it happens on a single thread that keeps spawning questions. Parallelism is about starting new work before finishing existing work, and can happen with a low open count if each strand closes promptly. |
| `scope-injection` | Did the **job get bigger** — a change of scope, however unstated — or did unfinished business simply pile up inside an unchanged job? Bigger job → scope injection. |
| `missing-context` | An item **nobody answered** is overload. A fact **nobody supplied** is missing context. |
| `vocabulary-mismatch` | Too much, or wrong words? A reader who cannot keep up is overload; a reader who cannot evaluate is vocabulary. |

## What rules it out

- **The open count falls as well as rises.** Things are being closed. A busy session is not an
  overloaded one, and volume alone is not this mode.
- **You can pin the failure on a single message.** If one turn is genuinely responsible, this is
  not a sequence-level failure. Find the turn and name what it did.
- **The dropped item was dropped deliberately.** If the record shows anyone deciding to let it
  go, it did not fall on the floor; it was put down.

---

*Example: none yet. Worked examples are added from real investigations.*
