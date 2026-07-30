#!/usr/bin/env python3
"""mg-16eb — EIGHT NEW MUTATIONS mg-0049's AUTHOR NEVER SAW, each with its exit code
PREDICTED BEFORE THE RUN, plus a ninth construction that is not a row (the documented
RECOVERY PATH, run to the letter on C1; see battery16eb.py section 2).

WHY NEW ONES AT ALL.  mg-0049 was fitted to nine rows it wrote itself, and a fix fitted to
known rows is a fix fitted to its test set.  mg-5644's Q1-Q6 and mg-0049's R1-R9 are re-run
here unmodified, on their own harnesses — mg-5644's whole audit in `out_5644_rerun.txt`, and
mg-0049's nine in `out_reproduce.txt`, which regenerates its committed output and diffs the
bytes.  That is the control on the control.  These eight are the rows nobody has run.

WHERE THEY POINT.  mg-0049's commit message and `COVERAGE.md` both name where it thinks it
might have failed: the target's page outside its cited sections (`R3`/`R4`), the derivation
of the delegation surface, and `L2`.  This lineage established at mg-a61f that a pre-filed
list of one's own weak points DIRECTS ATTENTION, and that the broken row is the one the list
omits.  So all eight are aimed at what the list does NOT name:

    A1 A2 A3 A5   the SECOND PINNED TABLE the repair added, and the precise claim it
                  published about how the two tables are kept in step
    B1 B2         a reader shown the cited sections in a DIFFERENT ORDER, in the one field
                  the repair declared inert on this surface
    B3            the blank page the repair classifies as DRIFT rather than damage
    C1            a cited section that gains an ordinary CODE EXAMPLE — every byte of it
                  shown to a reader on both renderers — on the new whole-section span

`R3`/`R4` are not re-litigated here: mg-0049 re-measured them rather than inheriting them,
and this audit confirms that re-measurement rather than repeating it.

EVERY MUTATION IS COMPUTED FROM AN UNMUTATED SNAPSHOT and every anchor is checked to match
exactly once, so a row that has rotted is a LookupError and never a silent no-op.
"""
import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True, check=True).stdout.strip()

ATTEMPT = "docs/state-history/attempt-mg-276d.md"
CONTROL = "code/state_landing_control_2da3/delta_control.py"

PASS, FAIL, MOVED = 0, 1, 2

ZERO = "0" * 64

# --- anchors, all checked to match exactly once before use --------------------------------
_H3_HEAD = "### H3 — the all-+1 invariance theorem, and the repair of its citation"
_H4_HEAD = ("### H4 — the relocated coverage gap, the gauge-conjugation mechanism, "
            "and the positive control on the control")
_H5_HEAD = "### H5 — the recommended next probe, and the answer that discharged it"

_DP_OPEN = "DELEGATED_PRESENTATION = {\n"
_DP_H3 = ('        "H3": "2fae29f7da64900f5ec7bd10ffd2199666feb11b65a50279c9adaef5e908747e",\n')
_DP_H5 = ('        "H5": "f6ae6325c5307d5a6c088990ad5f49b7b2f9f8347e73458b55c66f072fcbe406",\n')
_D_H3 = ('        "H3": (544, "cea7a8207b7dedb11eae2d3b7ea9bc75a22e4cd07e9536eb90e35de1d432fc60"),\n')


def _once(text, needle):
    n = text.count(needle)
    if n != 1:
        raise LookupError(f"anchor matched {n} times, need exactly 1: {needle[:70]!r}")
    return text


def _section(text, head):
    """(start index, end index) of the ATX section opened by `head`, heading line included,
    running to the next heading of the same or a shallower level.  The instrument's own
    rule (`named_section`), re-implemented here rather than imported, so a mutation cannot
    be silently reshaped by a change to the thing under test."""
    _once(text, head)
    lines = text.split("\n")
    i = lines.index(head)
    level = len(re.match(r"^(#{1,6})\s", head).group(1))
    deeper = re.compile(r"^#{1,%d}\s" % level)
    j = i + 1
    while j < len(lines) and not deeper.match(lines[j]):
        j += 1
    return lines, i, j


# =========================================================================================
# A — THE TABLE THE REPAIR ADDED.  delta_control.py's own comment over DELEGATED_PRESENTATION
# says, in these words: "A cited section present in DELEGATED and absent here has no
# certified record, so its comparison fails and exits non-zero: THE TWO TABLES CANNOT DRIFT
# APART QUIETLY IN EITHER DIRECTION."  That is a claim about the instrument, so it is tested
# by mutating the instrument.  A3 is the direction the sentence describes; A1 and A2 are the
# other one; A5 is the same shape on the table mg-bee1 added, for comparison.
# =========================================================================================
def a1_extra_section_in_presentation(t):
    """A certified presentation record for a section that is not delegated and not cited.

    Predicted exit 0: nothing iterates DELEGATED_PRESENTATION, so an entry that is in it and
    in nothing else is never visited.  If this is 0 the published sentence is false in one
    of the two directions it names."""
    _once(t, _DP_H5)
    return t.replace(_DP_H5, _DP_H5 + f'        "H9": "{ZERO}",\n', 1)


def a2_extra_target_in_presentation(t):
    """A whole TARGET FILE with a certified presentation record, delegated by nobody."""
    _once(t, _DP_OPEN)
    return t.replace(
        _DP_OPEN,
        _DP_OPEN + f'    "docs/state-history/README.md": {{"H1": "{ZERO}"}},\n', 1)


def a3_drop_presentation_row(t):
    """H3's presentation record deleted: the direction the published sentence describes."""
    _once(t, _DP_H3)
    return t.replace(_DP_H3, "", 1)


def a5_drop_delegated_row(t):
    """H3's CONTENT digest deleted from mg-bee1's table — the same shape one table over.
    That table's keys are cross-checked against the sections the certified text actually
    cites, so this one is expected to be caught; it is here as the comparison that makes
    A1's result mean something."""
    _once(t, _D_H3)
    return t.replace(_D_H3, "", 1)


# =========================================================================================
# B — WHAT A READER IS SHOWN ON THE TARGET, inside the cited sections, with no cited byte
# changed.  The repair's bound is "a reader who follows a certified region's citation IS
# SHOWN the section it names, as prose, under the heading path that was certified".
# =========================================================================================
def b1_swap_two_cited_sections(t):
    """H3 and H4 exchanged in the source.  Not one byte of either section changes, both
    keep their heading path, both are prose, and a reader is shown them in the other
    order.  `position` is the field that would carry this and the repair declared it inert
    on this surface."""
    lines, i3, j3 = _section(t, _H3_HEAD)
    _lines, i4, j4 = _section(t, _H4_HEAD)
    if not j3 == i4:
        raise LookupError(f"H3 and H4 are not adjacent ({j3} vs {i4}) — the row has rotted")
    out = lines[:i3] + lines[i4:j4] + lines[i3:j3] + lines[j4:]
    return "\n".join(out)


def b2_move_cited_section_to_the_end(t):
    """H5 relocated verbatim under a different `##` parent.  Its bytes do not change; its
    heading path does.  The control on B1: it shows the record is not inert to everything,
    so B1's result is about `position` and not about the record being unread."""
    lines, i5, j5 = _section(t, _H5_HEAD)
    block = lines[i5:j5]
    rest = lines[:i5] + lines[j5:]
    while block and not block[-1].strip():
        block.pop()
    return "\n".join(rest + [""] + block + [""])


def b3_details_with_summary(t):
    """mg-0049's R5 with a `<summary>`, so what a reader sees is a labelled CLOSED
    disclosure widget rather than the browser's default one.  Both renderers put every
    cited section inside the `<details>` element and neither closes it (render16eb.py
    measures this), so per the HTML standard a reader is shown the summary and nothing
    else until they click.  The exit code is not the finding; the CLASSIFICATION is."""
    return ("<details>\n<summary>Superseded drafts — click to expand</summary>\n\n" + t)


# =========================================================================================
# C — THE WHOLE-SECTION SPAN.  region_record's `state` is the SET of states over the span,
# and is_presented() accepts only the singleton "rendered".  A certified region is a
# paragraph or a quote block and cannot contain a fence; a DELEGATED SECTION is a heading
# and everything under it, in a history document about a computation.
# =========================================================================================
def c1_code_example_inside_a_cited_section(t):
    """An ordinary, closed, fully visible fenced code block added to cited section H3.

    Every line of the section is shown to a reader on both renderers — render16eb.py
    measures it — and the fence renders as a code sample, which is what a code sample is
    for.  Predicted exit 1: `state` becomes `fenced-code+rendered`, which is not the
    singleton is_presented() accepts, so the control reports the section as one THE READER
    IS SHOWN NOTHING OF.  Predicted, and the prediction is that the control is WRONG about
    what a reader sees while being right that something changed."""
    _once(t, _H4_HEAD)
    example = ("An example of that rescaling, so a reader can check it:\n"
               "\n"
               "```python\n"
               "d_true = np.diag(row_signs) @ d_allplus\n"
               "```\n"
               "\n")
    return t.replace(_H4_HEAD, example + _H4_HEAD, 1)


# (id, surface, description, PREDICTED exit code, file it mutates, fn)
ROWS = [
    ("A1", "the table mg-0049 ADDED",
     "a presentation record for a section nothing delegates or cites", PASS, CONTROL,
     a1_extra_section_in_presentation),
    ("A2", "the table mg-0049 ADDED",
     "a whole TARGET FILE certified here and delegated by nobody", PASS, CONTROL,
     a2_extra_target_in_presentation),
    ("A3", "the table mg-0049 ADDED",
     "a delegated section's presentation record DELETED", MOVED, CONTROL,
     a3_drop_presentation_row),
    ("A5", "mg-bee1's table (control)",
     "a delegated section's CONTENT digest deleted (the same shape)", MOVED, CONTROL,
     a5_drop_delegated_row),
    ("B1", "reader order, cited",
     "two cited sections EXCHANGED; no byte of either changes", PASS, ATTEMPT,
     b1_swap_two_cited_sections),
    ("B2", "heading path (control)",
     "one cited section moved verbatim under a different parent", MOVED, ATTEMPT,
     b2_move_cited_section_to_the_end),
    ("B3", "blank page, classified",
     "<details><summary> at the top: a CLOSED widget over the whole page", MOVED, ATTEMPT,
     b3_details_with_summary),
    ("C1", "the whole-section span",
     "an ordinary CODE EXAMPLE inside a cited section, fully shown", FAIL, ATTEMPT,
     c1_code_example_inside_a_cited_section),
]
