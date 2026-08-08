#!/usr/bin/env python3
"""
verify.py — run the gate in both directions and assert the contract.

    python tests/verify.py

Two directions, because only one of them is evidence:

- Every report in `cases/` must pass. A gate that rejects everything is useless and
  would satisfy any test that only fed it broken input.
- Every report in `negative/` must fail, **on the check it was built to break, and on
  nothing else**. Merely failing proves nothing: a gate that rejected all input would
  do that too. Each negative fixture differs from a passing report by exactly one
  mutation, so the check that fires is the one that reacted to the mutation.

And one completeness assertion: every check `check.py` can report must have at least one
negative fixture behind it. Without that, a check could be added, never be exercised, and
quietly do nothing.

Then the command line itself, which is the same argument one level down. Every one of the
checks above is worth nothing if the gate can be invoked in a way that examines nothing and
still exits 0, because 0 is the only thing a CI step or a shell script reads. So every
invocation that cannot actually check a report has to exit 2 and must never print PASS.

The manifests are built by running parse.py over a committed synthetic export, so the
tests exercise the real parser-to-gate path and cannot drift from what parse.py actually
emits. Nothing here touches a real conversation export; CI has none.

Stdlib only. Python 3.8+. Exit 0 if the contract holds, 1 if it does not.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPORT = os.path.join(HERE, "fixtures", "synthetic-export.json")
PARSE = os.path.join(ROOT, "parse.py")
CHECK = os.path.join(ROOT, "check.py")

# Which manifest each report is checked against. A report and a record are a pair.
MANIFESTS = {
    "conv0": ["--index", "0"],
    "conv1": ["--index", "1"],
    "conv0-window": ["--index", "0", "--messages", "6-10"],
}

CLEAN = [
    ("grid-mismatch-pilot-error.md", "conv0"),
    ("thin-record-undetermined.md", "conv1"),
    ("windowed-origin-outside.md", "conv0-window"),
]

# (fixture, manifest, the one check it must fail on)
NEGATIVE = [
    ("fabricated-quote.md", "conv0", "quote-verbatim"),
    ("quote-welded-across-channels.md", "conv0", "quote-verbatim"),
    ("quote-stitched-segments.md", "conv0", "quote-verbatim"),
    ("wrong-role-anchor.md", "conv0", "quote-verbatim"),
    ("two-primary-causes.md", "conv0", "primary-cause-count"),
    ("no-primary-cause.md", "conv0", "primary-cause-count"),
    ("invented-failure-mode.md", "conv0", "failure-mode-file"),
    ("prescription-in-factor.md", "conv0", "prescription"),
    ("prescription-future-advice.md", "conv0", "prescription"),
    ("missing-counterfactual.md", "conv0", "counterfactual-missing"),
    ("continues-past-counterfactual.md", "conv0", "report-continues"),
    ("unanchored-factor.md", "conv0", "factor-anchor"),
    ("unanchored-quote.md", "conv0", "quote-anchor"),
    ("reasoning-as-speech.md", "conv0", "reasoning-attribution"),
    ("verdict-out-of-enum.md", "conv0", "verdict-enum"),
    ("wrong-record.md", "conv0", "record-pairing"),
    ("missed-catch-points-omitted.md", "conv0", "missed-catch-points"),
    ("sections-out-of-order.md", "conv0", "section-order"),
    ("no-heading-block.md", "conv0", "heading-block"),
    ("origin-not-quoted.md", "conv0", "section-quote-required"),
    ("undetermined-no-resolution.md", "conv1", "undetermined-resolution"),
]

# Invocations that cannot check anything. Each must exit 2 — "the gate could not run" —
# and none may print PASS. The dangerous one is `--list-checks` alongside a report: it
# reads neither file, so before it was refused it exited 0, which is the same 0 a clean
# report produces. A gate that can be made to say yes without looking is not a gate.
#
# (description, argv builder taking (report, manifest, workdir))
CLI_REFUSALS = [
    ("a report with no --manifest",
     lambda report, manifest, work: [report]),
    ("no arguments at all",
     lambda report, manifest, work: []),
    ("--manifest with no report",
     lambda report, manifest, work: ["--manifest", manifest]),
    ("--list-checks alongside a report",
     lambda report, manifest, work: [report, "--list-checks"]),
    ("--list-checks alongside a manifest",
     lambda report, manifest, work: ["--list-checks", "--manifest", manifest]),
    ("a --manifest that does not exist",
     lambda report, manifest, work: [report, "--manifest",
                                     os.path.join(work, "no-such-manifest.json")]),
    ("a --manifest that is valid JSON but not a manifest",
     lambda report, manifest, work: [report, "--manifest",
                                     os.path.join(HERE, "fixtures",
                                                  "test-sweep-rules.json")]),
    ("a report that does not exist",
     lambda report, manifest, work: [os.path.join(work, "no-such-report.md"),
                                     "--manifest", manifest]),
]


def use_utf8_streams():
    """This output contains dashes a legacy Windows console codepage cannot encode."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def run(argv):
    """Run a command and return (exit code, stdout, stderr)."""
    process = subprocess.Popen([sys.executable] + argv, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=ROOT)
    out, err = process.communicate()
    return (process.returncode,
            out.decode("utf-8", "replace"),
            err.decode("utf-8", "replace"))


def build_manifests(workdir):
    """Turn the committed synthetic export into the manifests the reports cite."""
    paths = {}
    for key, selector in MANIFESTS.items():
        target = os.path.join(workdir, key + ".json")
        code, _out, err = run([PARSE, EXPORT] + selector + ["--json", "--out", target])
        if code != 0:
            raise SystemExit("verify.py: parse.py failed building %s:\n%s" % (key, err))
        paths[key] = target
    return paths


def gate(report_path, manifest_path):
    """Run check.py and return (exit code, set of failing check names)."""
    code, out, err = run([CHECK, report_path, "--manifest", manifest_path, "--json"])
    if code not in (0, 1):
        raise SystemExit("verify.py: check.py could not run on %s:\n%s"
                         % (report_path, err or out))
    try:
        payload = json.loads(out)
    except json.JSONDecodeError:
        raise SystemExit("verify.py: check.py did not emit JSON for %s:\n%s"
                         % (report_path, out))
    return code, [f["check"] for f in payload["failures"]], payload["failures"]


def known_checks():
    code, out, err = run([CHECK, "--list-checks"])
    if code != 0:
        raise SystemExit("verify.py: could not list checks:\n%s" % (err or out))
    return [line.strip() for line in out.splitlines() if line.strip()]


def main():
    use_utf8_streams()
    workdir = tempfile.mkdtemp(prefix="ofr-verify-")
    failures = []
    try:
        manifests = build_manifests(workdir)

        print("Clean reports — every one must pass")
        clean_ok = 0
        for name, manifest_key in CLEAN:
            path = os.path.join(HERE, "cases", name)
            code, names, detail = gate(path, manifests[manifest_key])
            if code == 0:
                clean_ok += 1
                print("  pass  %s" % name)
            else:
                print("  FAIL  %s — rejected on: %s" % (name, ", ".join(names)))
                for item in detail:
                    print("          [%s] line %s: %s"
                          % (item["check"], item["line"], item["message"]))
                failures.append("clean report %s was rejected" % name)
        print("  %d/%d clean reports passed\n" % (clean_ok, len(CLEAN)))

        print("Broken reports — every one must fail, on its own check and no other")
        negative_ok = 0
        for name, manifest_key, expected in NEGATIVE:
            path = os.path.join(HERE, "negative", name)
            code, names, _detail = gate(path, manifests[manifest_key])
            distinct = sorted(set(names))
            if code == 0:
                print("  FAIL  %-38s expected %s, but the gate passed it"
                      % (name, expected))
                failures.append("%s slipped through the gate" % name)
            elif distinct == [expected]:
                negative_ok += 1
                print("  pass  %-38s rejected on %s" % (name, expected))
            elif expected in distinct:
                print("  FAIL  %-38s rejected on %s, but also tripped %s"
                      % (name, expected, ", ".join(n for n in distinct if n != expected)))
                failures.append("%s trips checks beyond the one it tests" % name)
            else:
                print("  FAIL  %-38s expected %s, got %s"
                      % (name, expected, ", ".join(distinct) or "nothing"))
                failures.append("%s failed on the wrong check" % name)
        print("  %d/%d broken reports rejected on their named check\n"
              % (negative_ok, len(NEGATIVE)))

        print("Coverage — every check the gate can report must have a fixture")
        declared = known_checks()
        exercised = set(expected for _n, _m, expected in NEGATIVE)
        uncovered = [c for c in declared if c not in exercised]
        stray = sorted(exercised - set(declared))
        if uncovered:
            print("  FAIL  no negative fixture for: %s" % ", ".join(uncovered))
            failures.append("checks with no fixture behind them: %s"
                            % ", ".join(uncovered))
        if stray:
            print("  FAIL  fixtures expect checks the gate does not report: %s"
                  % ", ".join(stray))
            failures.append("fixtures name unknown checks: %s" % ", ".join(stray))
        if not uncovered and not stray:
            print("  pass  %d/%d checks have a negative fixture"
                  % (len(declared), len(declared)))

        print("\nThe command line — an invocation that checks nothing must not exit 0")
        cli_ok = 0
        report = os.path.join(HERE, "cases", CLEAN[0][0])
        manifest = manifests[CLEAN[0][1]]
        for description, build_argv in CLI_REFUSALS:
            argv = build_argv(report, manifest, workdir)
            code, out, err = run([CHECK] + argv)
            said_pass = "PASS" in out
            if code == 2 and not said_pass:
                cli_ok += 1
                print("  pass  %-46s refused, exit 2" % description)
            elif said_pass:
                print("  FAIL  %-46s printed PASS having checked nothing"
                      % description)
                failures.append("check.py passes on: %s" % description)
            else:
                print("  FAIL  %-46s exit %d, expected 2 — %s"
                      % (description, code, (err or out).strip().splitlines()[0]
                         if (err or out).strip() else "no message"))
                failures.append("check.py does not refuse: %s" % description)
        print("  %d/%d invocations that check nothing were refused\n"
              % (cli_ok, len(CLI_REFUSALS)))
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print("")
    if failures:
        print("CONTRACT BROKEN")
        for line in failures:
            print("  - %s" % line)
        return 1
    print("CONTRACT HOLDS  %d clean reports pass, %d broken reports rejected on their "
          "named check, %d checks covered, %d invocations that check nothing refused."
          % (len(CLEAN), len(NEGATIVE), len(known_checks()), len(CLI_REFUSALS)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
