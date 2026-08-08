# Judge guide

Two paths. The first needs nothing installed and takes about a minute. The second is the full
battery and takes about ten.

Both are designed so you check a claim rather than take one. Where something cannot be verified
from a cold clone, this file says so rather than glossing it.

---

## Sixty seconds, nothing installed

**Open three files, in this order.**

**1.** [`runs/01-too-complex-too-fast/report.md`](runs/01-too-complex-too-fast/report.md)

An investigation of a real incident: partway through a build session the person steering stopped
understanding the replies and halted the work. Read section 3 and section 7 if you read nothing
else. Section 3 locates the fault inside a single message — a turn that opens by promising plain
English and then breaks that promise in the section immediately after. Section 7 is the but-for
test, and it is unusual: the record happened to run the counterfactual for real two messages
later, so the test is checked forward against a message that already exists rather than
supposed.

Note what is not there. No rewritten prompt. No "next time". No list of everything imperfect
about the session. The file ends at section 7.

**2.** [`runs/01-too-complex-too-fast/answer-key.md`](runs/01-too-complex-too-fast/answer-key.md)

The next message the person actually sent — message 13 — which the investigation was never
shown. It did not exist on disk anywhere when the run happened; it was written into the repo
afterwards. It is the orchestrator saying, in the session, unprompted, whether the problem was
fixed and what fixed it.

**3.** [`runs/01-too-complex-too-fast/comparison-note.md`](runs/01-too-complex-too-fast/comparison-note.md)

The grading, both directions.

**The thing to look for is the miss.** The key contains *I already ran 2B before I read through
your whole response* — the person fired the next job without finishing the message explaining it.
That is the strongest evidence in the window that the turn had overloaded its reader, it was
sitting on the plain-speech channel inside the investigation's own window, and the report elided
it with `[...]` twice without reading it.

That miss is the point. A perfect match against a withheld document is a reason to suspect a
run, not to trust it. A run that got the cause right, argued its verdict against the neighbouring
verdicts, and still failed to see a contradiction in its own window is a run that was reading the
record rather than the answer.

If you have another minute, [`runs/03-the-wrong-file/comparison-note.md`](runs/03-the-wrong-file/comparison-note.md)
opens by recording that this run returned the opposite verdict to the one written down for it in
advance, and that it was shipped as produced rather than re-run.

---

## The full battery

### 1. The gate discriminates

```bash
python tests/verify.py
```

Python 3.9 or newer, standard library only, no packages, no export. Expect exit 0 and four
blocks:

- **3 clean reports pass.** A gate that rejects everything would satisfy any test that only fed
  it broken input.
- **21 broken reports are each rejected on the one check they were built to break, and on
  nothing else.** This is the block that matters. Each negative fixture differs from a clean one
  by exactly one mutation, and the assertion is that the set of checks it trips is exactly the
  one that mutation should trip. Merely failing would prove nothing.
- **16/16 checks have a negative fixture behind them.** `verify.py` asks `check.py` what checks
  it can report and fails if any has nothing exercising it, so a check cannot be added, never
  run, and quietly do nothing while looking like enforcement.
- **8 invocations that examine nothing are refused.** A gate that can be made to exit 0 without
  reading a report is not a gate. See `OPEN-DEFECTS.md` — one of these eight is a real defect
  found in this repo, and it is recorded there rather than quietly patched.

```bash
python tests/parser-check.py
```

Expect exit 0. Asserts the four properties the gate's own tests cannot see: that a fork in the
export is marked rather than flattened into a false repetition, that every text-bearing channel
is read, that the redaction sweep's replacements are counted including a rule that matched
nothing, and that the same export produces the same manifest byte for byte with the reader's own
filesystem path nowhere in it.

Both suites run on every push, on Linux and Windows, at Python 3.9 and 3.13 —
[`.github/workflows/verify.yml`](.github/workflows/verify.yml). A separate CI job fails the
build if any raw export file is ever tracked in git.

### 2. The three shipped reports still pass, against the records they read

The manifests ship, so this works from a cold clone with no export:

```bash
python check.py runs/01-too-complex-too-fast/report.md --manifest runs/01-too-complex-too-fast/message-manifest.json
python check.py runs/02-the-two-hour-job/report.md    --manifest runs/02-the-two-hour-job/message-manifest.json
python check.py runs/03-the-wrong-file/report.md      --manifest runs/03-the-wrong-file/message-manifest.json
```

```
PASS  runs/01-too-complex-too-fast/report.md
      11 quotations checked against runs/01-too-complex-too-fast/message-manifest.json
PASS  runs/02-the-two-hour-job/report.md
      13 quotations checked against runs/02-the-two-hour-job/message-manifest.json
PASS  runs/03-the-wrong-file/report.md
      7 quotations checked against runs/03-the-wrong-file/message-manifest.json
```

Thirty-one quotations, each matched verbatim against the record the investigator actually read.

### 3. Break one yourself

This is the fastest way to establish the quote check is real rather than decorative.

Open any shipped report, find a quote block, and change one word inside it — a plausible word, a
tidier word, a fixed typo. Re-run the command above. The gate names the file, the line and the
rule, and exits 1. Put the word back and it passes again.

Then try the mutations the fixtures already encode, in [`tests/negative/`](tests/negative/).
Twenty-one files, one mutation each. The three worth reading are:

- `quote-welded-across-channels.md` — a quotation assembled from the model's speech and its
  private reasoning run together. It reads perfectly. Without the single-segment rule it would
  pass, and it would be a fabricated statement.
- `prescription-in-factor.md` — a fix smuggled into a contributing factor, which is where advice
  actually creeps into reports rather than into a headed "recommendations" section.
- `reasoning-as-speech.md` — a thought introduced with a speech verb. One word wrong, and the
  report is describing a conversation that did not happen.

### 4. Read the accretion layer, and check it against its sources

[`training-layer/AB.md`](training-layer/AB.md) is the accumulated profile of one orchestrator,
built from the three runs. Six recurring patterns, each naming the runs it came from, each
written as a check to run early rather than a conclusion to apply.

The one to check is **pattern 5**, which exists because an investigation *missed* something its
answer key contained. The profile is written after the grading rather than after the report, so
what the investigation failed to see is what the next one is told to look for. That is the loop
closing on real evidence rather than on a diagram of one.

Its final section states what three sessions of one person over eight days do not establish.

### 5. Re-run a blind investigation, on your own material

This is the only part that needs something you supply.

1. Export your own Claude data: Settings → Privacy → Export data.
2. `python parse.py conversations.json --list` to find the session, then window it:
   `python parse.py conversations.json --uuid <uuid> --messages <N>-<M> --include-tool-io
   --include-attachments --out manifest.md`, and again with `--json`.
3. Start a fresh chat or project whose entire contents are a copy of
   [`diagnostician/`](diagnostician/), that manifest, and one or two lines saying what went
   wrong. Nothing else — no build documents, no expectations.
4. Run `python check.py report.md --manifest manifest.json` over whatever comes back.

The protocol each shipped run used, and what it does *not* guarantee, is in each run's
`run-notes.md`. The honest limit is stated there: the raw export was present and readable on the
machine, so nothing mechanically prevented an investigator from going and finding the source
conversation. What can be said is that it was told not to, that it wrote no file suggesting it
did, and that the reports are wrong in ways a contaminated run would not have been.

---

## What a cold clone cannot verify

Stated plainly, because the alternative is you finding out.

- **The manifests cannot be regenerated here.** They came from a real personal export which is
  gitignored and stays that way. Each `run-notes.md` records the exact `parse.py` command and the
  export's SHA-256, so the person holding that export can rebuild them byte for byte — and
  nobody else can. What ships is the record the investigator read, and the gate re-runs against
  it.
- **The isolation of the three blind runs rests on protocol plus evidence, not on a mechanism.**
  See step 5 above. The strongest evidence is what the runs got wrong.
- **Run 1's shipped manifest is not quite the text its investigator read.** A redaction sweep was
  applied after the investigation, replacing three strings — a personal name and a channel
  identifier — that an earlier check had missed. Neither is quoted in the report or named in its
  reasoning, and the gate passes against the swept record. Run 2's sweep ran *before* its
  investigation, which is the stronger property. Both are recorded in
  [`OPEN-DEFECTS.md`](OPEN-DEFECTS.md) and in the runs' own notes.
- **Three investigations of one person over eight days** is the entire evidence base. Nothing
  here is known to generalise.

[`OPEN-DEFECTS.md`](OPEN-DEFECTS.md) is the full list, and it is longer than this one.
