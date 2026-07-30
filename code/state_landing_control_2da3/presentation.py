#!/usr/bin/env python3
"""mg-4acd — THE PRESENTATION RESOLVER.  What a reader SEES, not which bytes exist.

WHY THIS FILE EXISTS.  mg-7870 replaced the certifying mechanism with a SHA-256 per
certified region, and it worked: mg-babf re-implemented mg-2216's five surviving mutations
from their published prose and all five now fire, and five independent probes of the
normalisation all landed correctly.  What mg-babf found instead is that the blind spot had
moved ONE LAYER UP, into the LOCATOR:

    B04  a certified block MOVED VERBATIM under "Appendix Z — superseded drafts ...
         nothing below is in force"                                            exit 0
    B05  a certified block wrapped in a ```text FENCE, so it renders as a code sample
                                                                               exit 0
    B06  a certified block wrapped in an HTML COMMENT, absent from every rendered view
                                                                               exit 0
    B07  a "RETRACTED ... is void" paragraph inserted immediately ABOVE a certified block
                                                                               exit 0

Not one of those changes a single certified byte.  A digest answers *"are these the
certified bytes?"* and answers it correctly.  The locator answers *"which bytes are the
certified ones?"* — and, silently, *"and is anybody shown them?"* — and that second
question was never controlled.

THE PROPERTY THIS FILE CERTIFIES, STATED TO ITS BOUND (mg-bee1, repairing mg-218d's B1).

    A mutation that changes HOW A CERTIFIED REGION IS PRESENTED — the container it renders
    in, the heading path in force over it, or its ordinal among the blocks OF ITS OWN
    SECTION — must change a digest.

    CROSS-SECTION CONTEXT IS NOT COVERED.  A block a reader passes immediately before a
    certified region, but on the other side of a heading, is not a field of any record
    here, and a mutation that adds one exits 0.

WHAT THAT SENTENCE REPLACES, AND WHY THE REPLACEMENT IS THE REPAIR.  This file, COVERAGE.md
and e4426c9's commit message all published the property in capitals as

    A MUTATION THAT CHANGES WHAT A READER SEES MUST CHANGE A DIGEST

— universally quantified over mutations.  The mechanism is quantified over A REGION'S OWN
SECTION: `heading` is the ATX path and `position` is an ordinal among the blocks of that
section.  Nothing outside the section is a field.  mg-218d demonstrated the gap with a pair
of mutations differing by ONE LINE:

    P1  mg-babf's B07 restated — the retraction as the first block INSIDE the certified
        section                                                              exit 2
    P2  THE SAME PARAGRAPH ONE LINE EARLIER — the last block of the section before
                                                                             exit 0

A reader is shown the same page in both.  So B07, one of the four mutations e4426c9 leads
with, is caught by where its author happened to put the paragraph and not by a property.
Three more at this layer exit 0: a retraction in an unrelated section of the README; a new
"READ THIS FIRST — this document is superseded" section near the top; the same in STATE.md.
The positive control — the README's H1 retitled — DOES fire, because `heading` carries
path[0].  The layer is not inert; it is bounded, and the bound is the section.

THE DEFECT WAS IN THE STATEMENT, and the statement is what the next reader relies on, so
the statement is what is repaired.  The mechanism is unchanged: mg-bee1 measured what a
document-global `position` would buy and what it would cost, and did not take the trade —
see COVERAGE.md, "The document-global ordinal, costed and NOT taken", and
code/state_delegation_repair_bee1/ for the measurement.

THE CLOSURE ARGUMENT — why this is a small job and not "implement a renderer".
------------------------------------------------------------------------------
The content digest of mg-7870 already fires on EVERY edit inside a certified region.  So
the presentation layer only has to answer for edits OUTSIDE the region.  That bounds the
job sharply, because an edit outside a region can only change how the region is presented
by changing the BLOCK CONTEXT the region sits in, and in CommonMark + GFM there are exactly
three ways to do that:

    (a) put the region inside a container that suppresses or re-frames it — a fenced code
        block, an HTML comment, or a raw HTML block.  (Indented code cannot do it from
        outside: making a region indented code requires indenting the region's own lines,
        which changes its bytes and fires the content digest.)
    (b) change the HEADING the region sits under — by moving the region, or by moving,
        adding or deleting a heading around it.
    (c) change the region's POSITION among the blocks OF ITS OWN SECTION — which is how
        B07 works: nothing inside the block moves, but a retraction now stands immediately
        above it, under the same heading.

(a) is a state, (b) is a path, (c) is an ordinal.  All three are block-level facts, and
block-level structure is a much smaller thing to model than markdown rendering.  That is
what this file models, and it models nothing else.

WHERE THE CLOSURE ARGUMENT IS TOO STRONG, said here rather than left to be found again.
(c) is stated above as a fact about the region's own section, and that is the whole of it:
a block inserted in ANOTHER section is an outside edit that changes what a reader passes
and moves no field of any record.  So "an edit outside a region can only change how the
region is presented in three ways" is true of the three ways THIS FILE MODELS, and is not
an exhaustive account of what an outside edit can do to a reader.  mg-218d's P2/P3/P4/P6
are the counterexamples, and they are named in the property above rather than absorbed.

WHAT THIS FILE IS NOT.  It is NOT a markdown renderer, it does not emit HTML, and it does
not resolve any inline construct — emphasis, links, code spans (except when masking them
for the raw-HTML scan) and entities are all left exactly as written.  It never needs to:
inline markup lives INSIDE a region, and inside a region the content digest already
certifies every byte.

THE DECLARED SUBSET, and the default-deny that bounds it.
---------------------------------------------------------
MODELLED block constructs: ATX headings, thematic breaks, blank lines, fenced code blocks
(``` and ~~~, with the CommonMark closing rule), block quotes (including nesting and
bullet-indented quotes), GFM tables (header + delimiter row + body), and paragraphs.

Everything else is DEFAULT-DENY.  `anomalies()` reports every line carrying a block
construct outside the modelled subset — setext underlines, indented code blocks, tab
indentation, CR line endings — and `html_tokens()` reports every raw-HTML-looking token in
text a reader is shown as prose.  Both are ZERO in the two certified files as they stand,
and `delta_control.py` treats a non-zero count as a non-zero exit.  So a mutation that
reaches for a suppression mechanism this resolver does not model does not slip past it;
it trips the guard instead.  An open-ended "does it model construct X?" is thereby closed
the same way mg-7870 closed "does it catch mutation X?" — by refusing to answer it with a
list.

THE COST, STATED HERE AND IN COVERAGE.md BECAUSE IT IS REAL.
------------------------------------------------------------
mg-babf's brief proposed digesting the RENDERED TEXT of each region and named the cost: a
dependency on a renderer, under which a renderer upgrade becomes a false positive.  That
direction is taken here; that MECHANISM is not, for three reasons, and the reasons are
worth arguing with:

  1. NO RENDERER IS AVAILABLE.  This box has no `markdown`, `markdown_it`, `mistune`,
     `commonmark` or `cmarkgfm` module and no `pandoc`, `cmark` or `cmark-gfm` binary
     (checked).  A control that cannot run is not a control.
  2. EVERY INSTRUMENT IN THIS CLUSTER IMPORTS NOTHING.  A certification whose verdict
     depends on a third-party version is a certification about that version too.
  3. THE COST NAMED IN THE BRIEF IS REAL.  A renderer upgrade re-baselines every region at
     once, and a control that is re-baselined wholesale stops being read.

THE COST TAKEN INSTEAD, which is not smaller, only different, and is the new uncontrolled
layer: THIS RESOLVER IS A MODEL OF A RENDERER, NOT A RENDERER.  Where the model and the
renderer disagree, the control is wrong.  The model is argued from the CommonMark 0.31
block-structure rules and the GFM table extension; it is NOT measured against a renderer,
because there is none here to measure against.  What bounds the damage is the default-deny
above: the model is allowed to be ignorant, and where it is ignorant it must say so rather
than pass.  What is NOT bounded, and is named here so the next auditor tests it, is the
model being CONFIDENT AND WRONG — a construct it classifies as `rendered` that a real
renderer suppresses, or the reverse.  That is where the blind spot has moved to now.
"""
import hashlib
import re

EDGE = " \t\r\n"

# --- the presentation states a line can be in -------------------------------------------
RENDERED = "rendered"            # shown to a reader as prose / table / heading
FENCED_CODE = "fenced-code"      # shown, but as a code sample: not in force as prose
HTML_COMMENT = "html-comment"    # not shown at all
HTML_BLOCK = "html-block"        # raw HTML: shown at the renderer's discretion, not ours

SUPPRESSED = (FENCED_CODE, HTML_COMMENT, HTML_BLOCK)

_QUOTE = re.compile(r"^ {0,3}> ?")
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_ATX = re.compile(r"^ {0,3}(#{1,6})(?: +(.*?))? *$")
_SETEXT = re.compile(r"^ {0,3}(?:=+|-+) *$")
_HTML_COMMENT_OPEN = re.compile(r"^ {0,3}<!--")
_HTML_TAG_OPEN = re.compile(r"^ {0,3}</?[A-Za-z]")
_INDENT4 = re.compile(r"^(?: {4}|\t)")
_CODESPAN = re.compile(r"`+[^`]*`+")
_HTMLISH = re.compile(r"<[A-Za-z!/?]")
# A GFM delimiter row: pipes, colons, dashes and spaces, with at least one dash.
_DELIM = re.compile(r"^ {0,3}\|?[ :\-|]*-[ :\-|]*$")


def strip_quotes(line):
    """(blockquote depth, the line's content inside those quotes).

    CommonMark's block-quote marker is up to three leading spaces, '>', and one optional
    space.  Applied repeatedly, so nesting and bullet-indented quotes are handled by the
    same rule.
    """
    depth, rest = 0, line
    while True:
        m = _QUOTE.match(rest)
        if not m:
            return depth, rest
        rest = rest[m.end():]
        depth += 1


class Doc:
    """A resolved document: per-line presentation state, heading path and block index.

    Nothing here is line-number-pinned from the outside: callers hand in a marker, get a
    line span from the existing locator, and ask this object what a reader sees there.
    """

    def __init__(self, text):
        self.text = text
        self.lines = text.split("\n")
        n = len(self.lines)
        self.state = [RENDERED] * n
        self.heading = [()] * n
        self.depth = [0] * n
        self._anomalies = []
        self._resolve()
        self._segment()

    # -- the scan ------------------------------------------------------------------------
    def _resolve(self):
        fence = None            # (fence char, run length, blockquote depth)
        html = None             # ("comment" | "block", blockquote depth)
        path = []
        prev_blank = True
        if "\r" in self.text:
            self._anomalies.append((0, "cr-line-ending",
                                    "the file contains CR; every rule here assumes LF"))
        for i, line in enumerate(self.lines):
            d, content = strip_quotes(line)
            self.depth[i] = d
            blank = not content.strip()
            if "\t" in line:
                self._anomalies.append((i + 1, "tab", line.strip()[:60]))

            # A container opened at blockquote depth k ends when a line sits shallower.
            if fence is not None and d < fence[2]:
                fence = None
            if html is not None and (d < html[1] or (html[0] == "block" and blank)):
                html = None

            if fence is not None:
                self.state[i] = FENCED_CODE
                m = _FENCE.match(content)
                if (m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]
                        and not m.group(2).strip()):
                    fence = None
                self.heading[i] = tuple(path)
                prev_blank = blank
                continue

            if html is not None:
                self.state[i] = HTML_COMMENT if html[0] == "comment" else HTML_BLOCK
                if html[0] == "comment" and "-->" in content:
                    html = None
                self.heading[i] = tuple(path)
                prev_blank = blank
                continue

            m = _FENCE.match(content)
            if m:
                self.state[i] = FENCED_CODE
                fence = (m.group(1)[0], len(m.group(1)), d)
            elif _HTML_COMMENT_OPEN.match(content):
                self.state[i] = HTML_COMMENT
                if "-->" not in content.split("<!--", 1)[1]:
                    html = ("comment", d)
            elif _HTML_TAG_OPEN.match(content):
                self.state[i] = HTML_BLOCK
                html = ("block", d)
            else:
                atx = _ATX.match(content)
                if atx:
                    level = len(atx.group(1))
                    title = (atx.group(2) or "").strip().rstrip("#").strip()
                    path = path[:level - 1] + [title]
                elif not blank and _INDENT4.match(content) and prev_blank and d == 0:
                    self._anomalies.append((i + 1, "indented-code", content.strip()[:60]))
                elif not blank and not prev_blank and _SETEXT.match(content):
                    # `---` is a thematic break after a blank line and a SETEXT H2 after a
                    # paragraph line: the two are textually identical and only context
                    # separates them, so `prev_blank` is the whole of the rule.  Do NOT add
                    # a _TBREAK exclusion here — it matches `---` too, and it silently
                    # swallowed every setext case when it was tried.
                    self._anomalies.append((i + 1, "setext-underline", content.strip()[:60]))
                self.state[i] = RENDERED
            self.heading[i] = tuple(path)
            prev_blank = blank

    # -- blocks --------------------------------------------------------------------------
    def _segment(self):
        """Split the document into the BLOCKS a reader passes, section by section.

        A block is a maximal run of consecutive lines that are not blank-in-prose; a blank
        line inside a fence or an HTML block does not split anything, because a reader sees
        one code sample and not two.  ATX heading lines are section delimiters and are not
        themselves blocks: they are the thing a block's position is measured against.
        """
        self.blocks = []           # (first, last, heading path, ordinal, kind)
        self._block_of = {}
        run = None
        ordinal = 0
        section = ()
        for i, line in enumerate(self.lines):
            st = self.state[i]
            d, content = strip_quotes(line)
            is_heading = (st == RENDERED and d == 0
                          and _ATX.match(content) is not None)
            breaks = (st == RENDERED and not line.strip()) or is_heading
            if breaks:
                if run is not None:
                    self._close(run, section, ordinal)
                    ordinal += 1
                    run = None
                if is_heading:
                    section = self.heading[i]
                    ordinal = 0
                continue
            if run is None:
                run = [i, i, st]
            else:
                run[1] = i
        if run is not None:
            self._close(run, section, ordinal)
        siblings = {}
        for b in self.blocks:
            siblings[b[2]] = siblings.get(b[2], 0) + 1
        self.siblings = siblings

    def _close(self, run, section, ordinal):
        first, last, kind = run
        idx = len(self.blocks)
        self.blocks.append((first, last, section, ordinal, kind))
        for i in range(first, last + 1):
            self._block_of[i] = idx

    def block_at(self, line_index):
        """The block a given 0-based line belongs to, or None for a blank separator."""
        idx = self._block_of.get(line_index)
        return None if idx is None else self.blocks[idx]

    # -- the guards ----------------------------------------------------------------------
    def anomalies(self):
        """Block constructs outside the declared subset.  Default-deny: non-empty is a
        non-zero exit, because a construct this resolver does not model is a construct it
        cannot certify the presentation of."""
        return list(self._anomalies)

    def html_tokens(self):
        """Raw-HTML-looking tokens anywhere OUTSIDE a fenced code block.

        Fenced code and inline code spans are masked first, so the `mermaid` diagram in
        `STATE.md` and prose like `x<b_1` are correctly not HTML; everything else is,
        INCLUDING the lines this resolver has already classified as `html-comment` or
        `html-block`, so that the guard fires on a wrapper that suppresses nothing but
        still changes what a reader sees — `<details>`, `<span style="display:none">`,
        `<div hidden>`.  This one guard subsumes the whole
        family of HTML suppression and disclosure mechanisms — `<!-- -->`, `<div hidden>`,
        `<details>`, `<span style="display:none">` — without enumerating it, which is the
        point: an enumeration is a list somebody chose.
        """
        out = []
        for i, line in enumerate(self.lines):
            if self.state[i] == FENCED_CODE:
                continue
            masked = _CODESPAN.sub(lambda m: " " * len(m.group(0)), line)
            for m in _HTMLISH.finditer(masked):
                out.append((i + 1, m.group(0), line.strip()[:70]))
        return out


# =========================================================================================
# THE PRESENTED TEXT of a span, and the PRESENTATION RECORD of a region.
# =========================================================================================
def presented_text(doc, first, last):
    """R(span): the span's lines with their block-quote markers removed, joined, edge-
    stripped.  Container prefixes are what a renderer consumes and a reader never sees;
    everything else is left exactly as written, because inside a region the content digest
    certifies every byte and R would only be a second, weaker opinion about the same bytes.
    """
    return "\n".join(strip_quotes(doc.lines[i])[1]
                     for i in range(first, last + 1)).strip(EDGE)


def _sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def region_record(doc, first, last):
    """The presentation record of the line span [first, last], as ordered (key, value).

    Printed in full by the control so a reader can recompute the digest by hand, exactly
    as the content digests are.
    """
    states = sorted({doc.state[i] for i in range(first, last + 1)})
    block = doc.block_at(first)
    if block is None:
        position = "no block (the region's first line is a blank separator)"
        heading = " > ".join(doc.heading[first]) or "(no heading)"
    else:
        _f, _l, section, ordinal, _kind = block
        heading = " > ".join(section) or "(no heading)"
        position = f"block {ordinal + 1} of {doc.siblings[section]} in its section"
    return [
        ("state", "+".join(states)),
        ("heading", heading),
        ("position", position),
        ("presented", _sha(presented_text(doc, first, last))),
    ]


def table_record(doc, line_index, cells_raw):
    """The presentation record of a GFM table row.

    A reader sees a table row only if the row is inside a table — header line, delimiter
    row, body — and sees only the first `arity` cells of it, because GFM drops every cell
    past the header's column count.  Both facts are certified here: `state` says whether
    the row renders as a table row at all, and `presented` digests the cells a reader is
    actually shown.  The row's INDEX within the table is deliberately not certified, so
    that deleting an unrelated ledger row stays outside coverage, as it is today.
    """
    block = doc.block_at(line_index)
    heading = " > ".join(doc.heading[line_index]) or "(no heading)"
    if block is None or doc.state[line_index] != RENDERED:
        return [("state", doc.state[line_index] + " (not presented as a table row)"),
                ("heading", heading), ("position", "n/a"), ("columns", "n/a"),
                ("presented", _sha(""))]
    first, _last, section, ordinal, _kind = block
    position = f"block {ordinal + 1} of {doc.siblings[section]} in its section"
    arity = None
    if line_index >= first + 2 and _DELIM.match(strip_quotes(doc.lines[first + 1])[1]):
        header = _split_row(strip_quotes(doc.lines[first])[1])
        if header is not None:
            arity = len(header)
    if arity is None:
        return [("state", "pipes-in-a-paragraph (no header + delimiter row above it)"),
                ("heading", heading), ("position", position), ("columns", "n/a"),
                ("presented", _sha(""))]
    shown = [c.strip(EDGE) for c in cells_raw[:arity]]
    return [
        ("state", "gfm-table-row"),
        ("heading", heading),
        ("position", position),
        ("columns", f"{arity} presented"),
        ("presented", _sha("\x1f".join(shown))),
    ]


def _split_row(line):
    """The raw fragments between unescaped pipes, or None if not a table row.

    Same escaped-pipe rule as delta_control.py's, restated rather than imported so this
    module stands alone.
    """
    bounds = [i for i, ch in enumerate(line)
              if ch == "|" and (i == 0 or line[i - 1] != "\\")]
    if len(bounds) < 2 or bounds[0] != 0:
        return None
    return [line[bounds[i] + 1:bounds[i + 1]] for i in range(len(bounds) - 1)]


def record_digest(record):
    """sha256 of the record's canonical serialisation.  One line per field, `key=value`."""
    return hashlib.sha256(
        "\n".join(f"{k}={v}" for k, v in record).encode("utf-8")).hexdigest()


# =========================================================================================
# SELF-TEST.  The model's own declared claims, checked against the model.
#
# This does NOT establish that the model matches a renderer — nothing here can, and
# COVERAGE.md says so in as many words.  What it does is stop the DECLARED SUBSET from
# being a paragraph of prose that nothing reads: every claim the header makes about which
# constructs are modelled and which are default-denied has a case below, and a case that
# stops holding is a non-zero exit rather than a stale sentence.  It is the cheapest
# available check on the layer this repair leaves uncontrolled, and it is deliberately not
# described as more than that.
#
#     python3 code/state_landing_control_2da3/presentation.py
# =========================================================================================
_CASES = [
    ("a plain paragraph is rendered",
     "# H\n\nhello\n", 2, RENDERED, ("H",), 0, 0),
    ("a blockquote is rendered",
     "# H\n\n> quoted\n", 2, RENDERED, ("H",), 0, 0),
    ("a fenced block is not prose",
     "# H\n\n```\ncode\n```\n", 3, FENCED_CODE, ("H",), 0, 0),
    ("a fence SWALLOWS what follows until it closes",
     "# H\n\n```\n\n> quoted\n\n```\n", 4, FENCED_CODE, ("H",), 0, 0),
    ("an UNCLOSED fence swallows the rest of the document",
     "# H\n\n```\n\n> quoted\n", 4, FENCED_CODE, ("H",), 0, 0),
    ("a tilde fence is a fence too",
     "# H\n\n~~~\n> quoted\n~~~\n", 3, FENCED_CODE, ("H",), 0, 0),
    ("a fence is closed only by its OWN character at its OWN length",
     "# H\n\n````\n```\n> quoted\n````\n", 4, FENCED_CODE, ("H",), 0, 0),
    ("an HTML comment hides what it wraps",
     "# H\n\n<!--\n> quoted\n-->\n", 3, HTML_COMMENT, ("H",), 0, 1),
    ("a raw HTML block is not prose",
     "# H\n\n<div>\n> quoted\n", 3, HTML_BLOCK, ("H",), 0, 1),
    ("a <details> wrapper suppresses NOTHING and is caught by the html guard alone",
     "# H\n\n<details>\n\n> quoted\n\n</details>\n", 4, RENDERED, ("H",), 0, 2),
    ("an HTML comment is caught by the html guard as well as by `state`",
     "# H\n\n<!-- hidden -->\n", 2, HTML_COMMENT, ("H",), 0, 1),
    ("the heading path is the ATX chain in force",
     "# A\n\n## B\n\n### C\n\ntext\n", 6, RENDERED, ("A", "B", "C"), 0, 0),
    ("a deeper heading pops back on a shallower one",
     "# A\n\n## B\n\n### C\n\n## D\n\ntext\n", 8, RENDERED, ("A", "D"), 0, 0),
    ("a thematic break is NOT a setext underline",
     "# H\n\n---\n\ntext\n", 4, RENDERED, ("H",), 0, 0),
    ("a setext underline IS default-denied",
     "# H\n\nTitle\n---\n\ntext\n", 5, RENDERED, ("H",), 1, 0),
    ("an indented code block is default-denied",
     "# H\n\n    code\n", 2, RENDERED, ("H",), 1, 0),
    ("a tab is default-denied",
     "# H\n\nte\txt\n", 2, RENDERED, ("H",), 1, 0),
    ("a code span is not raw HTML",
     "# H\n\nprose `x<b_1` prose\n", 2, RENDERED, ("H",), 0, 0),
    ("HTML inside a fence is not raw HTML",
     "# H\n\n```mermaid\nA[\"x<br/>y\"]\n```\n", 3, FENCED_CODE, ("H",), 0, 0),
]

_POSITION_CASES = [
    ("a paragraph inserted ABOVE moves the ordinal",
     "# H\n\nfirst\n\n> target\n", "# H\n\nfirst\n\nRETRACTED\n\n> target\n"),
    ("a paragraph inserted BELOW moves the sibling count",
     "# H\n\n> target\n", "# H\n\n> target\n\nafterword\n"),
    ("moving the block under a new heading moves the path",
     "# H\n\n> target\n", "# H\n\n## Appendix Z\n\n> target\n"),
    ("editing a NEIGHBOURING block moves neither",
     "# H\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n> target\n",
     "# H\n\n| a | b |\n|---|---|\n| 1 | 9 |\n\n> target\n"),
]


def _self_test():
    bad = 0
    print("presentation.py — SELF-TEST of the DECLARED SUBSET")
    print("=" * 86)
    print("Each case asserts what the module header CLAIMS about one construct.  This checks")
    print("the model against its own statement; it does NOT check the model against a")
    print("renderer, and no case below should ever be read as if it did.")
    print()
    print(f"{'#':>3}  {'state':<13} {'heading':<14} {'anom':>4} {'html':>4}  claim")
    for n, (name, text, line, want_state, want_head, want_anom, want_html) in \
            enumerate(_CASES, start=1):
        doc = Doc(text)
        got = (doc.state[line], doc.heading[line], len(doc.anomalies()),
               len(doc.html_tokens()))
        want = (want_state, want_head, want_anom, want_html)
        ok = got == want
        bad += not ok
        print(f"{n:>3}  {got[0]:<13} {'>'.join(got[1]):<14} {got[2]:>4} {got[3]:>4}  "
              f"{'ok  ' if ok else 'WRONG'} {name}")
        if not ok:
            print(f"     expected {want}")
    print()
    print("POSITION — what moves a region's presentation record, and what does not")
    for name, before, after in _POSITION_CASES:
        d0, d1 = Doc(before), Doc(after)
        i0 = next(i for i, l in enumerate(d0.lines) if "target" in l)
        i1 = next(i for i, l in enumerate(d1.lines) if "target" in l)
        r0 = region_record(d0, i0, i0)
        r1 = region_record(d1, i1, i1)
        moved = record_digest(r0) != record_digest(r1)
        want_moved = not name.startswith("editing a NEIGHBOURING")
        ok = moved == want_moved
        bad += not ok
        print(f"     {'ok  ' if ok else 'WRONG'} record {'MOVES ' if moved else 'holds '}"
              f"— {name}")
        if not ok:
            print(f"       {dict(r0)}\n       {dict(r1)}")
    print()
    print("=" * 86)
    print(f"{len(_CASES) + len(_POSITION_CASES)} cases, {bad} wrong")
    return 1 if bad else 0


if __name__ == "__main__":
    import sys as _sys
    _sys.exit(_self_test())
