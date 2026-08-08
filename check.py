#!/usr/bin/env python3
"""
check.py — the blocking gate.

Reads an investigation report and the message manifest it claims to be about, and
refuses the report if it breaks any of the rules the entry guarantees. Exit 0 means
every rule held. Exit 1 means at least one did not, and the report is not shippable.
Exit 2 means the gate could not run at all.

Why this exists
---------------
A "must" in markdown is a request. A "must" in code is a constraint. Everything this
file checks is mechanical — counting, matching, locating — so none of it rests on the
investigator remembering to be careful. The load-bearing one is the quote check: the
persuasive force of a report is that it hands people their own words back, so a
fabricated quotation is not a small defect, it is the whole product failing.

    python check.py report.md --manifest manifest.json

Build the manifest with parse.py --json. Python 3.8+, stdlib only.
"""

import argparse
import json
import os
import re
import sys

# The five verdicts, spelled as spec.md locks them.
VERDICTS = ("pilot-error", "mechanical", "environment", "mixed", "undetermined")

# The channel labels parse.py emits. An anchor naming anything else is malformed.
CHANNELS = ("SAID", "REASONING", "REASONING-SUMMARY", "ACTION", "RESULT", "ATTACHMENT")

# Channels whose text parse.py leaves out of the manifest unless asked for it. A quote
# against one of these that finds an empty segment is probably a manifest built without
# the right flag, not a fabrication, and the message has to say so.
NOT_INLINED_BY_DEFAULT = ("ACTION", "RESULT", "ATTACHMENT")

# The reasoning channels. Nobody but the model could see these.
REASONING_CHANNELS = ("REASONING", "REASONING-SUMMARY")

SECTION_TITLES = {
    1: "Incident statement",
    2: "Failure surface",
    3: "Causal origin",
    4: "Propagation trace",
    5: "Verdict class",
    6: "Primary cause",
    7: "Counterfactual test",
}

# Speech verbs. The model did not say anything in its private reasoning; it was working
# out, weighing, settling on. Writing it the other way merges the channels back together
# in prose, which is the error the parser exists to prevent.
#
# Deliberately only the unambiguous ones. The bare forms `say`, `state`, `write`, `tell`
# and `claim` were tried and removed: they carry ordinary non-speech senses that turn up
# constantly in honest investigative prose — the state of the work, a claim as a noun,
# somewhere a finding could be confirmed. A gate that fails good reports gets worked
# around, and then it is enforcing nothing at all.
SPEECH_VERBS = (
    "said", "says", "told", "tells", "stated", "states", "claimed", "claims",
    "wrote", "writes", "announced", "announces", "replied", "replies",
    "mentioned", "mentions", "asserted", "asserts", "declared", "declares",
)

# Prescription patterns. spec.md names the shapes; these are the phrasings, because the
# bare tokens it lists ("try") fire on ordinary investigative prose. Anything here is
# advice about a future or another session, which is a different document.
PRESCRIPTION_HARD = (
    "next time", "in future", "in the future", "going forward", "from now on",
    "you should", "you could", "you might want", "you may want", "you need to",
    "try this", "try instead", "you could try", "instead you should", "instead, you",
    "i recommend", "we recommend", "it is recommended", "my recommendation",
    "recommendation:", "recommendations:",
    "i suggest", "we suggest", "suggested fix", "suggestion:",
    "the fix is", "to fix this", "to prevent this", "to avoid this", "the remedy",
    "make sure to", "be sure to", "ensure that you", "consider using", "consider adding",
    "lesson learned", "lessons learned", "takeaway", "key takeaway",
    "rewritten as", "improved version", "better prompt", "a better message would",
)

# Softer constructions. These are legitimate inside a but-for test, which is about this
# session in the past and is anchored to a message. Unanchored, the same words are
# advice. M2's decision 29 is the specification; this is the implementation of it.
PRESCRIPTION_SOFT = (
    "should have", "ought to have", "would have been better", "should be", "should have been",
)

ANCHOR_RE = re.compile(r"msg\s+(\d+)\s*\(\s*([A-Za-z]+)\s*,\s*([A-Z][A-Z-]*)\s*\)")
WHITESPACE_RE = re.compile(r"\s+")
ELLIPSIS_RE = re.compile(r"\[\s*\.\s*\.\s*\.\s*\]")


# --------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------

def use_utf8_streams():
    """Real reports contain arrows and dashes; a legacy Windows codepage cannot."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def die(message):
    sys.stderr.write("check.py: %s\n" % message)
    raise SystemExit(2)


def normalise(text):
    """
    Flatten a passage so that only its words and their order matter.

    Line endings and line wrapping are presentation, not content: a report that rewraps
    a long quotation to fit the page has not altered it, and failing it would train
    people to fight the gate rather than use it. Everything else is left alone, so a
    changed word, a fixed typo or a dropped clause still fails.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return WHITESPACE_RE.sub(" ", text).strip()


def parse_anchor(line):
    """First `msg N (role, CHANNEL)` in the line, as (number, role, channel)."""
    match = ANCHOR_RE.search(line)
    if not match:
        return None
    return int(match.group(1)), match.group(2).lower(), match.group(3)


def parse_last_anchor(text):
    """The anchor nearest the end — the one introducing whatever follows."""
    matches = list(ANCHOR_RE.finditer(text))
    if not matches:
        return None
    match = matches[-1]
    return int(match.group(1)), match.group(2).lower(), match.group(3)


def all_anchors(line):
    return [(int(m.group(1)), m.group(2).lower(), m.group(3))
            for m in ANCHOR_RE.finditer(line)]


# --------------------------------------------------------------------------
# the report, taken apart
# --------------------------------------------------------------------------

class Report(object):
    """A parsed report: its lines, which of them are quotes or code, and its sections."""

    def __init__(self, text, path):
        self.path = path
        self.lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        self.fenced, self.quoted = self._scan_masks()
        self.sections = self._find_sections()
        self.paragraphs = self._find_paragraphs()
        self.quote_blocks = self._find_quote_blocks()

    def _find_paragraphs(self):
        """
        Runs of consecutive prose lines, joined.

        Reports are written in wrapped prose, so an anchor is frequently split across a
        line break: `... settled it at msg 6` on one line and `(assistant, REASONING):`
        on the next. Anything that reasons about whether a claim is anchored has to look
        at the paragraph, not the line, or it fails reports for where their margin fell.
        """
        found = []
        index = 0
        while index < len(self.lines):
            if not self.is_prose(index) or not self.lines[index].strip():
                index += 1
                continue
            start = index
            buffer = []
            while (index < len(self.lines) and self.is_prose(index)
                   and self.lines[index].strip()):
                buffer.append(self.lines[index].strip())
                index += 1
            found.append({"start": start, "end": index - 1, "text": " ".join(buffer)})
        by_line = {}
        for paragraph in found:
            for i in range(paragraph["start"], paragraph["end"] + 1):
                by_line[i] = paragraph
        self.paragraph_of = by_line
        return found

    def _scan_masks(self):
        """Mark which lines sit inside a code fence and which are block quotes."""
        fenced = [False] * len(self.lines)
        quoted = [False] * len(self.lines)
        in_fence = False
        marker = None
        for i, line in enumerate(self.lines):
            opener = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
            if opener:
                char = opener.group(1)[0]
                if not in_fence:
                    in_fence, marker = True, char
                    fenced[i] = True
                    continue
                if char == marker:
                    in_fence, marker = False, None
                    fenced[i] = True
                    continue
            fenced[i] = in_fence
            if not in_fence and re.match(r"^\s{0,3}>", line):
                quoted[i] = True
        return fenced, quoted

    def is_prose(self, i):
        """A line that is the investigator's own writing, not code and not a quotation."""
        return not self.fenced[i] and not self.quoted[i]

    def _find_sections(self):
        """Map section number -> {title, start, end}. Only real headings count."""
        found = []
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            match = re.match(r"^##\s+(\d+)\.\s+(.+?)\s*$", line)
            if match:
                found.append((int(match.group(1)), match.group(2), i))
        sections = {}
        for position, (number, title, start) in enumerate(found):
            end = found[position + 1][2] if position + 1 < len(found) else len(self.lines)
            sections[number] = {"title": title, "start": start, "end": end,
                                "order": position}
        self.section_order = [n for n, _t, _s in found]
        return sections

    def _find_quote_blocks(self):
        """
        Every run of block-quote lines, with the prose line that introduces it.

        A quotation is a syntactic object here, not a judgement call: block quotes are
        the only quoting device the report format allows, which is what makes the
        fabrication check implementable at all.
        """
        blocks = []
        i = 0
        while i < len(self.lines):
            if not self.quoted[i]:
                i += 1
                continue
            start = i
            body = []
            while i < len(self.lines) and self.quoted[i]:
                stripped = re.sub(r"^\s{0,3}>\s?", "", self.lines[i])
                body.append(stripped)
                i += 1
            blocks.append({
                "start": start,
                "end": i - 1,
                "text": "\n".join(body),
                "lead_in": self._lead_in(start),
            })
        return blocks

    def _lead_in(self, start):
        """
        The paragraph immediately above a quote block, skipping blank lines.

        The whole paragraph rather than its last line, because the anchor routinely
        wraps. Where a paragraph carries more than one anchor, the last one wins: it is
        the one nearest the quotation, and it is the one a reader would take as
        introducing it.
        """
        j = start - 1
        while j >= 0 and not self.lines[j].strip():
            j -= 1
        if j < 0 or not self.is_prose(j):
            return None
        paragraph = self.paragraph_of.get(j)
        if paragraph is None:
            return {"index": j, "text": self.lines[j]}
        return {"index": j, "text": paragraph["text"]}

    def section_lines(self, number):
        """(line_index, text) for each line inside a section, heading excluded."""
        section = self.sections.get(number)
        if not section:
            return []
        return [(i, self.lines[i]) for i in range(section["start"] + 1, section["end"])]

    def fixed_lines(self, label):
        """
        Every prose line beginning with a fixed label such as `Verdict:`.

        Quotes and code are skipped deliberately: a transcript message that happens to
        contain the word `Verdict:` is evidence, not an instruction to the gate.
        """
        hits = []
        for i, line in enumerate(self.lines):
            if not self.is_prose(i):
                continue
            stripped = line.strip()
            if stripped.lower().startswith(label.lower()):
                hits.append((i, stripped[len(label):].strip()))
        return hits


# --------------------------------------------------------------------------
# the manifest, indexed
# --------------------------------------------------------------------------

class Recorder(object):
    """The message manifest, indexed for lookup by message number and channel."""

    def __init__(self, data, path):
        self.path = path
        self.data = data
        self.by_message = {}
        for entry in data.get("messages") or []:
            self.by_message[entry.get("index")] = entry
        window = data.get("window") or {}
        self.first = window.get("first")
        self.last = window.get("last")
        self.sha256 = data.get("source_sha256") or ""

    def segments(self, number, channel):
        entry = self.by_message.get(number)
        if entry is None:
            return None
        return [s for s in entry.get("segments") or [] if s.get("channel") == channel]

    def role(self, number):
        entry = self.by_message.get(number)
        return None if entry is None else (entry.get("role") or "")


# --------------------------------------------------------------------------
# failures
# --------------------------------------------------------------------------

def failure(check, line, message):
    """line is a 0-based index into the report, or None."""
    return {"check": check, "line": None if line is None else line + 1,
            "message": message}


# --------------------------------------------------------------------------
# the checks
# --------------------------------------------------------------------------

def check_heading_block(report, recorder, modes_dir):
    """The three provenance lines above section 1, which pair report to record."""
    end = report.sections[1]["start"] if 1 in report.sections else len(report.lines)
    head = "\n".join(report.lines[:end])
    problems = []
    for label in ("record", "source-sha256", "window"):
        if not re.search(r"^\s+%s\s+\S" % re.escape(label), head, re.M):
            problems.append(label)
    if problems:
        return [failure("heading-block", None,
                        "the heading block above section 1 is missing its %s line. "
                        "A report and the record it reads are checked as a pair, and "
                        "without these lines there is nothing tying them together."
                        % " and ".join(problems))]
    return []


def check_section_order(report, recorder, modes_dir):
    """Sections 1 to 6 present, in order, titled as the schema fixes them."""
    out = []
    for number in range(1, 7):
        if number not in report.sections:
            out.append(failure("section-order", None,
                               "section %d (%s) is missing."
                               % (number, SECTION_TITLES[number])))
    present = [n for n in report.section_order if n in SECTION_TITLES]
    if present != sorted(present):
        out.append(failure("section-order", None,
                           "the sections are out of order: found %s, expected them "
                           "ascending." % ", ".join(str(n) for n in present)))
    for number, section in sorted(report.sections.items()):
        expected = SECTION_TITLES.get(number)
        if expected and section["title"].strip().lower() != expected.lower():
            out.append(failure("section-order", section["start"],
                               "section %d is titled %r; the schema fixes it as %r."
                               % (number, section["title"], expected)))
    return out


def check_counterfactual_present(report, recorder, modes_dir):
    """Section 7 has to exist. It is the section that proves the cause."""
    if 7 not in report.sections:
        return [failure("counterfactual-missing", None,
                        "section 7 (Counterfactual test) is missing. Without the "
                        "but-for reasoning there is nothing separating the cause from "
                        "a symptom, so the report has not made its case.")]
    body = "\n".join(t for _i, t in report.section_lines(7)).strip()
    if not body:
        return [failure("counterfactual-missing", report.sections[7]["start"],
                        "section 7 (Counterfactual test) is present but empty.")]
    return []


def check_section_quotes(report, recorder, modes_dir):
    """
    Sections 2 and 3 each carry at least one quotation.

    The surface and the origin are the two places the report makes a claim about a
    specific message, and a claim about a message that does not quote it is an assertion.
    Section 3 is covered even when the origin is an absence, because an absence claim has
    to name the message where a party had to proceed without the missing thing.
    """
    out = []
    for number in (2, 3):
        section = report.sections.get(number)
        if not section:
            continue
        has_quote = any(section["start"] < block["start"] < section["end"]
                        for block in report.quote_blocks)
        if not has_quote:
            out.append(failure("section-quote-required", section["start"],
                               "section %d (%s) carries no quotation. This section makes "
                               "a claim about a specific message, and a claim about a "
                               "message that does not quote it is an assertion."
                               % (number, SECTION_TITLES[number])))
    return out


def check_report_stops(report, recorder, modes_dir):
    """Nothing after section 7. Stopping is where the discipline usually fails."""
    if 7 not in report.sections:
        return []
    start = report.sections[7]["start"]
    out = []
    for i in range(start + 1, len(report.lines)):
        if not report.is_prose(i):
            continue
        line = report.lines[i]
        if re.match(r"^#{1,6}\s+\S", line):
            out.append(failure("report-continues", i,
                               "the report continues past the counterfactual test with "
                               "a new heading: %s. Section 7 is the last thing in the "
                               "file — no summary, no lessons, no closing note."
                               % line.strip()))
            break
    return out


def check_record_pairing(report, recorder, modes_dir):
    """The report's fingerprint must be the record's, or say it had none."""
    match = re.search(r"^\s+source-sha256\s+(\S+)", "\n".join(report.lines), re.M)
    if not match:
        return []
    claimed = match.group(1).strip()
    if claimed.lower() in ("not", "not-recorded", "none"):
        return []
    if claimed.lower().startswith("not recorded"):
        return []
    if not recorder.sha256:
        return []
    if claimed != recorder.sha256:
        return [failure("record-pairing", None,
                        "the report says it read a record with fingerprint %s, but the "
                        "manifest supplied has fingerprint %s. These are different "
                        "records, so every message number in the report is checked "
                        "against the wrong transcript."
                        % (claimed[:16] + "...", recorder.sha256[:16] + "..."))]
    return []


def check_verdict(report, recorder, modes_dir):
    """Exactly one Verdict line, and its value one of the five."""
    hits = report.fixed_lines("Verdict:")
    if not hits:
        return [failure("verdict-enum", None,
                        "no `Verdict:` line. Section 5 has to say whose failure it was, "
                        "as one of: %s." % ", ".join(VERDICTS))]
    if len(hits) > 1:
        return [failure("verdict-enum", hits[1][0],
                        "%d `Verdict:` lines; there must be exactly one." % len(hits))]
    line_index, value = hits[0]
    value = value.strip().rstrip(".")
    if value not in VERDICTS:
        return [failure("verdict-enum", line_index,
                        "verdict %r is not one of the five: %s."
                        % (value, ", ".join(VERDICTS)))]
    return []


def verdict_value(report):
    hits = report.fixed_lines("Verdict:")
    if len(hits) != 1:
        return None
    return hits[0][1].strip().rstrip(".")


def check_undetermined_resolution(report, recorder, modes_dir):
    """An undetermined finding must name evidence that would settle it."""
    if verdict_value(report) != "undetermined":
        return []
    if not report.fixed_lines("Would resolve it:"):
        return [failure("undetermined-resolution", None,
                        "the verdict is `undetermined` but there is no `Would resolve "
                        "it:` line. Undetermined is a finding, not a shrug: it has to "
                        "name obtainable evidence that would settle the question.")]
    return []


def check_primary_cause_count(report, recorder, modes_dir):
    """Exactly one `Failure mode:` line — the mechanical form of one primary cause."""
    hits = report.fixed_lines("Failure mode:")
    if len(hits) == 1:
        return []
    if not hits:
        return [failure("primary-cause-count", None,
                        "no `Failure mode:` line, so the report names no primary cause. "
                        "A symptom inventory with no ranked primary cause is not a "
                        "diagnosis.")]
    return [failure("primary-cause-count", hits[1][0],
                    "%d `Failure mode:` lines, so the report names %d primary causes. "
                    "There is exactly one primary cause; everything else is a "
                    "contributing factor, ranked beneath it."
                    % (len(hits), len(hits)))]


def check_failure_mode_file(report, recorder, modes_dir):
    """A named mode must be a file that exists. Modes are not invented in reports."""
    out = []
    for line_index, value in report.fixed_lines("Failure mode:"):
        name = value.strip().rstrip(".")
        if not name:
            out.append(failure("failure-mode-file", line_index,
                               "the `Failure mode:` line names nothing."))
            continue
        path = os.path.join(modes_dir, name + ".md")
        if not os.path.isfile(path):
            available = sorted(f[:-3] for f in os.listdir(modes_dir)
                               if f.endswith(".md") and f != "README.md") \
                if os.path.isdir(modes_dir) else []
            out.append(failure("failure-mode-file", line_index,
                               "failure mode %r has no file in %s. A mode may not be "
                               "invented inside a report; if the session failed in a "
                               "way nothing covers, the file is written first. "
                               "Available: %s."
                               % (name, modes_dir, ", ".join(available) or "none")))
    return out


def _numbered_items(lines, start_offset):
    """Group a numbered list into items, each carrying its continuation lines."""
    items = []
    for offset, text in lines[start_offset:]:
        if re.match(r"^\s*\d+\.\s+\S", text):
            items.append({"line": offset, "text": text})
        elif items and text.strip() and not re.match(r"^\s*[-*]\s", text) \
                and not text.startswith("#"):
            items[-1]["text"] += " " + text.strip()
        elif not text.strip() and items:
            break
    return items


def check_factor_anchors(report, recorder, modes_dir):
    """Every contributing factor points at a message. An unanchored factor is opinion."""
    hits = report.fixed_lines("Contributing factors:")
    if not hits:
        return [failure("factor-anchor", None,
                        "no `Contributing factors:` line. If there are none, the report "
                        "has to say so: `Contributing factors: none.` An omission and a "
                        "finding of none look identical otherwise, and only one of them "
                        "is a statement.")]
    line_index, tail = hits[0]
    if tail.strip().rstrip(".").lower() == "none":
        return []
    section = report.section_lines(6)
    start_offset = next((k for k, (i, _t) in enumerate(section) if i > line_index), None)
    if start_offset is None:
        return [failure("factor-anchor", line_index,
                        "`Contributing factors:` is followed by nothing. Write the "
                        "ranked list, or `Contributing factors: none.`")]
    items = _numbered_items(section, start_offset)
    if not items:
        return [failure("factor-anchor", line_index,
                        "`Contributing factors:` is followed by no numbered items. "
                        "Write the ranked list, or `Contributing factors: none.`")]
    out = []
    for item in items:
        if not ANCHOR_RE.search(item["text"]):
            out.append(failure("factor-anchor", item["line"],
                               "this contributing factor carries no anchor. Every "
                               "factor points at a message, as msg N (role, CHANNEL); "
                               "a factor with no anchor is an opinion."))
    return out


def check_missed_catch_points(report, recorder, modes_dir):
    """The line has to be there, in one of its two forms, and its items anchored."""
    hits = report.fixed_lines("Missed catch points:")
    if not hits:
        return [failure("missed-catch-points", None,
                        "no `Missed catch points:` line in section 4. If there were "
                        "none, say so: `Missed catch points: none.`")]
    line_index, tail = hits[0]
    if tail.strip().rstrip(".").lower() == "none":
        return []
    section = report.section_lines(4)
    out = []
    seen_any = False
    for i, text in section:
        if i <= line_index:
            continue
        if re.match(r"^\s*[-*]\s+\S", text):
            seen_any = True
            if not ANCHOR_RE.search(text):
                out.append(failure("missed-catch-points", i,
                                   "this missed catch point carries no anchor."))
        elif seen_any and not text.strip():
            break
    if not seen_any:
        out.append(failure("missed-catch-points", line_index,
                           "`Missed catch points:` is followed by no items. Write the "
                           "list, or `Missed catch points: none.`"))
    return out


def check_quote_anchors(report, recorder, modes_dir):
    """Every quotation is introduced by an anchor naming message, role and channel."""
    out = []
    for block in report.quote_blocks:
        lead_in = block["lead_in"]
        if lead_in is None:
            out.append(failure("quote-anchor", block["start"],
                               "this quotation has no line above it. Every quote block "
                               "is preceded immediately by its anchor."))
            continue
        anchor = parse_last_anchor(lead_in["text"])
        if anchor is None:
            out.append(failure("quote-anchor", lead_in["index"],
                               "the line introducing this quotation carries no anchor. "
                               "The form is: <lead-in>, msg N (role, CHANNEL): — an "
                               "unattributed quotation is how a report starts telling "
                               "people they said things they only thought."))
            continue
        _number, role, channel = anchor
        if channel not in CHANNELS:
            out.append(failure("quote-anchor", lead_in["index"],
                               "channel %r is not one the record uses. The labels are: "
                               "%s." % (channel, ", ".join(CHANNELS))))
        if role not in ("human", "assistant"):
            out.append(failure("quote-anchor", lead_in["index"],
                               "role %r is not one the record uses; it is `human` or "
                               "`assistant`." % role))
    return out


def check_reasoning_attribution(report, recorder, modes_dir):
    """
    No speech verb may introduce the reasoning channel.

    The model did not say, tell, claim or state anything there. It was working out.
    A report that quotes a thought as though it were a statement commits, in miniature,
    the same merge the export's flattened text field makes.
    """
    out = []
    seen = set()

    def scrutinise(line_index, text, channel):
        if line_index in seen:
            return
        lowered = text.lower()
        for verb in SPEECH_VERBS:
            if re.search(r"\b%s\b" % re.escape(verb), lowered):
                seen.add(line_index)
                out.append(failure("reasoning-attribution", line_index,
                                   "this anchors to the %s channel but uses the speech "
                                   "verb %r. Nothing was said on that channel — the "
                                   "model was working out, weighing, settling on. Write "
                                   "it that way." % (channel, verb)))
                return

    # The paragraph introducing a quotation, which is where a thought gets dressed as
    # speech most often and most damagingly.
    for block in report.quote_blocks:
        lead_in = block["lead_in"]
        if lead_in is None:
            continue
        anchor = parse_last_anchor(lead_in["text"])
        if anchor and anchor[2] in REASONING_CHANNELS:
            scrutinise(lead_in["index"], lead_in["text"], anchor[2])

    # Any other line that anchors to a reasoning channel — trace steps, factors.
    for i, line in enumerate(report.lines):
        if not report.is_prose(i):
            continue
        channels = [c for _n, _r, c in all_anchors(line) if c in REASONING_CHANNELS]
        if channels:
            scrutinise(i, line, channels[0])
    return out


def check_quotes_verbatim(report, recorder, modes_dir):
    """
    The one that matters: every quoted passage appears verbatim in the record.

    A quotation must sit inside a single segment of a single message on a single
    channel. The single-segment rule is the important half — without it a report could
    weld a thought onto a statement and still pass, which is exactly the fabrication
    the whole design exists to prevent.
    """
    out = []
    for block in report.quote_blocks:
        lead_in = block["lead_in"]
        if lead_in is None:
            continue
        anchor = parse_last_anchor(lead_in["text"])
        if anchor is None:
            continue
        number, role, channel = anchor
        if channel not in CHANNELS or role not in ("human", "assistant"):
            continue

        quoted = normalise(block["text"])
        if not quoted:
            out.append(failure("quote-verbatim", block["start"],
                               "this quote block is empty."))
            continue
        fragments = [f for f in (p.strip() for p in ELLIPSIS_RE.split(quoted)) if f]
        if not fragments:
            out.append(failure("quote-verbatim", block["start"],
                               "this quote block is only an ellipsis."))
            continue

        actual_role = recorder.role(number)
        if actual_role is None:
            out.append(failure("quote-verbatim", block["start"],
                               "the record has no message %d. This manifest covers "
                               "messages %s-%s." % (number, recorder.first, recorder.last)))
            continue
        if actual_role != role:
            out.append(failure("quote-verbatim", lead_in["index"],
                               "the anchor says message %d belongs to %s, but in the "
                               "record it is %s." % (number, role, actual_role)))
            continue

        segments = recorder.segments(number, channel)
        if not segments:
            out.append(failure("quote-verbatim", block["start"],
                               "message %d has nothing on the %s channel in this record."
                               % (number, channel)))
            continue

        if all(not normalise(s.get("text") or "") for s in segments):
            hint = ""
            if channel in NOT_INLINED_BY_DEFAULT:
                hint = (" parse.py records that this %s exists but leaves its text out "
                        "unless asked; rebuild the manifest with --include-tool-io or "
                        "--include-attachments if the text really is there."
                        % channel.lower())
            out.append(failure("quote-verbatim", block["start"],
                               "message %d has a %s segment but no text for it in this "
                               "record, so this quotation cannot be verified.%s"
                               % (number, channel, hint)))
            continue

        if any(_fragments_in_order(normalise(s.get("text") or ""), fragments)
               for s in segments):
            continue

        stitched = _fragments_in_order(
            normalise(" ".join(s.get("text") or "" for s in segments)), fragments)
        if stitched:
            out.append(failure("quote-verbatim", block["start"],
                               "this quotation only matches message %d if two separate "
                               "%s segments are run together. One block is one message, "
                               "one channel, one continuous stretch — a quotation "
                               "assembled from two places is not a quotation."
                               % (number, channel)))
            continue

        out.append(failure("quote-verbatim", block["start"],
                           "this quotation does not appear in message %d on the %s "
                           "channel. Nothing was found matching: %s"
                           % (number, channel, _excerpt(fragments[0]))))
    return out


def _fragments_in_order(haystack, fragments):
    """Each fragment present, in order, without overlapping."""
    position = 0
    for fragment in fragments:
        found = haystack.find(fragment, position)
        if found < 0:
            return False
        position = found + len(fragment)
    return True


def _excerpt(text, limit=70):
    return text if len(text) <= limit else text[:limit] + "..."


def check_prescription(report, recorder, modes_dir):
    """
    No advice. The report ends at cause.

    Two things are deliberately not scanned: block quotes, because those are the
    record's own words and an orchestrator who wrote "next time, use v2" is evidence
    rather than a rule breach; and the reporter's hypothesis, which is recorded as they
    put it. Everything else is the investigator writing, and the investigator does not
    prescribe.
    """
    out = []
    for i, line in enumerate(report.lines):
        if report.quoted[i]:
            continue
        stripped = line.strip()
        if stripped.lower().startswith("reporter's hypothesis:"):
            continue
        lowered = stripped.lower()
        for pattern in PRESCRIPTION_HARD:
            if pattern in lowered:
                out.append(failure("prescription", i,
                                   "prescription: %r. The report determines cause and "
                                   "stops; recommendations are a different document, "
                                   "written by different people at a different time."
                                   % pattern))
                break
        else:
            paragraph = report.paragraph_of.get(i)
            context = paragraph["text"] if paragraph else stripped
            if ANCHOR_RE.search(context):
                continue
            for pattern in PRESCRIPTION_SOFT:
                if pattern in lowered:
                    out.append(failure("prescription", i,
                                       "prescription: %r with no message anchor. Past "
                                       "and this session is a counterfactual and is "
                                       "required; unanchored, the same words are advice "
                                       "about a session nothing in the record can check."
                                       % pattern))
                    break
    return out


CHECKS = (
    check_heading_block,
    check_section_order,
    check_counterfactual_present,
    check_section_quotes,
    check_report_stops,
    check_record_pairing,
    check_verdict,
    check_undetermined_resolution,
    check_primary_cause_count,
    check_failure_mode_file,
    check_factor_anchors,
    check_missed_catch_points,
    check_quote_anchors,
    check_reasoning_attribution,
    check_quotes_verbatim,
    check_prescription,
)

# Every check this gate can report, so tooling can enumerate them without running one.
CHECK_NAMES = (
    "heading-block", "section-order", "counterfactual-missing", "section-quote-required",
    "report-continues", "record-pairing", "verdict-enum", "undetermined-resolution",
    "primary-cause-count", "failure-mode-file", "factor-anchor", "missed-catch-points",
    "quote-anchor", "reasoning-attribution", "quote-verbatim", "prescription",
)


# --------------------------------------------------------------------------
# running
# --------------------------------------------------------------------------

def run_checks(report_text, report_path, manifest_data, manifest_path, modes_dir):
    report = Report(report_text, report_path)
    recorder = Recorder(manifest_data, manifest_path)
    failures = []
    for check in CHECKS:
        failures.extend(check(report, recorder, modes_dir))
    failures.sort(key=lambda f: (f["line"] is None and -1 or f["line"]))
    return failures


def default_modes_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "diagnostician", "reference", "failure-modes")


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check.py",
        description="Check an investigation report against the record it claims to read.",
        epilog="Exit 0 if every rule held, 1 if any did not, 2 if the gate could not run.")
    parser.add_argument("report", nargs="?", help="path to the report markdown file")
    parser.add_argument("--manifest",
                        help="path to the message manifest from parse.py --json")
    parser.add_argument("--modes-dir", default=None,
                        help="directory of failure-mode files "
                             "(default: diagnostician/reference/failure-modes)")
    parser.add_argument("--json", action="store_true",
                        help="emit the result as JSON instead of prose")
    parser.add_argument("--list-checks", action="store_true",
                        help="print every check this gate can report, and exit")
    args = parser.parse_args(argv)
    use_utf8_streams()

    if args.list_checks:
        for name in CHECK_NAMES:
            sys.stdout.write(name + "\n")
        return 0

    if not args.report:
        die("which report should I check? Usage:\n"
            "  python check.py report.md --manifest manifest.json")
    if not args.manifest:
        die("a report is checked against the record it claims to be about, so I need "
            "the manifest too:\n"
            "  python parse.py <export> --json --out manifest.json\n"
            "  python check.py %s --manifest manifest.json" % args.report)

    modes_dir = args.modes_dir or default_modes_dir()

    try:
        with open(args.report, "r", encoding="utf-8") as fh:
            report_text = fh.read()
    except OSError as exc:
        die("could not open the report %s: %s" % (args.report, exc.strerror or exc))

    try:
        with open(args.manifest, "r", encoding="utf-8") as fh:
            manifest_data = json.load(fh)
    except OSError as exc:
        die("could not open the manifest %s: %s" % (args.manifest, exc.strerror or exc))
    except json.JSONDecodeError as exc:
        die("could not read %s as JSON: %s\nBuild it with: python parse.py <export> "
            "--json --out manifest.json" % (args.manifest, exc))

    if not isinstance(manifest_data, dict) or "messages" not in manifest_data:
        die("%s does not look like a message manifest. Build one with:\n"
            "  python parse.py <export> --json --out manifest.json" % args.manifest)

    failures = run_checks(report_text, args.report, manifest_data, args.manifest,
                          modes_dir)

    if args.json:
        sys.stdout.write(json.dumps(
            {"ok": not failures, "report": args.report, "manifest": args.manifest,
             "failures": failures}, indent=2) + "\n")
        return 1 if failures else 0

    if not failures:
        sys.stdout.write("PASS  %s\n" % args.report)
        sys.stdout.write("      %d quotations checked against %s\n"
                         % (len(Report(report_text, args.report).quote_blocks),
                            args.manifest))
        return 0

    sys.stdout.write("FAIL  %s\n" % args.report)
    sys.stdout.write("      %d problem%s against %s\n\n"
                     % (len(failures), "" if len(failures) == 1 else "s", args.manifest))
    for item in failures:
        where = "line %d" % item["line"] if item["line"] else "report"
        sys.stdout.write("  [%s] %s\n" % (item["check"], where))
        for chunk in _wrap(item["message"], 74):
            sys.stdout.write("      %s\n" % chunk)
        sys.stdout.write("\n")
    return 1


def _wrap(text, width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = word if not current else current + " " + word
    if current:
        lines.append(current)
    return lines


if __name__ == "__main__":
    raise SystemExit(main())
