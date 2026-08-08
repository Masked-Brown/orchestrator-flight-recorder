# Tests

Written in build stage M3, alongside `check.py`.

The gate is only worth having if it demonstrably catches things, so the tests run in both
directions:

- `cases/` — well-formed reports that must pass the gate.
- `negative/` — deliberately broken reports, each one breaking a *different* rule: a quote
  that never appeared in the transcript, two primary causes, a fix smuggled into a
  contributing factor, a missing counterfactual, a factor with no message cited, a failure
  mode with no file behind it.
- `verify.py` — runs both sets and asserts the contract: every clean report passes, and every
  broken report is rejected *on the rule it was built to break*, not merely rejected.

That last distinction is the point. A gate that rejects everything also rejects all the
negative cases, and proves nothing.
