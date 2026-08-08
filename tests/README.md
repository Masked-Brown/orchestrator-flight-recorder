# Tests

The gate is only worth having if it demonstrably catches things. Run them:

    python tests/verify.py

Exit 0 means the contract holds. Exit 1 means it does not, and the output says where.
No packages to install, and nothing here touches a real conversation export.

## What is in here

- **`fixtures/synthetic-export.json`** — a small CONSTRUCTED export in the same shape as
  a real Claude data export: two conversations, both channels of assistant output, a
  message carrying two separate stretches of speech either side of a tool call, a
  reasoning block withheld with only a summary surviving, two withheld with nothing
  surviving, and a tool call that returned an error. Invented for these tests. It is not
  a record of anything that happened.
- **`cases/`** — well-formed reports. Every one must pass.
- **`negative/`** — deliberately broken reports. Every one must fail, on the check it was
  built to break.
- **`verify.py`** — runs both directions and asserts the contract.

## The contract

Three things are asserted, and the second is the one that matters.

**One — every clean report passes.** Three of them: a `pilot-error` finding with ranked
contributing factors, an `undetermined` finding on a record too thin to settle, and an
`undetermined` finding where the origin sits outside the window supplied. Between them
they exercise quotation from the speech and reasoning channels, shortening with `[...]`,
the explicit `none.` forms, and message numbering that stays global when only a window is
given.

**Two — every broken report fails on its own check, and on nothing else.** Merely failing
proves nothing: a gate that rejected all input would do that too, and would also reject
every clean report above. So each negative fixture is derived from a clean one by exactly
one mutation, and the assertion is that the set of checks it trips is exactly the one
check that mutation should trip. That is what makes this evidence rather than decoration.

**Three — every check has a fixture behind it.** `verify.py` asks `check.py` what checks it
can report and fails if any of them has no negative fixture. Without this a check could be
added, never exercised, and quietly do nothing while looking like enforcement.

## The manifests are built, not stored

`verify.py` runs `parse.py` over the synthetic export to produce the manifests the reports
are checked against, rather than committing manifests alongside them. Two reasons: the
tests then exercise the real parser-to-gate path instead of a stored approximation of it,
and a stored manifest could drift from what `parse.py` actually emits without anything
noticing.

One consequence worth knowing: the reports carry the export's `source-sha256` in their
heading block, and the gate fails a report whose fingerprint does not match the record it
is handed. So **editing `fixtures/synthetic-export.json` by even one byte will fail every
test** on `record-pairing` until the new fingerprint is written into each report. That is
the check doing its job. `.gitattributes` keeps the file's bytes identical across
platforms, which is why the suite also runs on Windows in CI.
