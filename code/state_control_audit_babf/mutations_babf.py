#!/usr/bin/env python3
"""mg-babf — MY OWN mutation battery against the DIGEST-based delta_control.py.

NONE OF THESE IS ONE OF mg-2216's FOURTEEN, and that is the point of the exercise.
mg-2216's list is now the repair's known-answer set: mg-7870 built against it and re-ran it
as evidence, so a control tuned to those fourteen and a control that works are the same
thing from inside.  I read the fourteen in order to AVOID them, exactly as mg-2216 read
NC3 in order to avoid it.  Their five B2 members are re-run separately, as the regression
they are, in regression_2216_b2.py.

WHERE I AIMED, and why.  A SHA-256 over a region cannot be fooled by a length-preserving
edit — that is why it was chosen, and mg-2216's five die on it (verified separately).  So
everything that is left lives in what the implementation decides is INSIGNIFICANT BEFORE
HASHING.  There are two such decisions and mg-7870 states only one of them:

  (i)  THE NORMALISATION `N`, which is stated in full: strip ASCII space/tab/CR/LF from the
       two ends of the region, nothing else.  This is a genuinely small surface and B09-B12
       probe it in both directions.

  (ii) THE LOCATOR, which is upstream of `N` and is NOT presented as a discard at all.  It
       decides WHICH BYTES ARE THE REGION.  A region is "the maximal run of blockquote lines
       containing this marker", so the digest is a function of the block's CONTENT and of
       NOTHING ELSE — not its position in the file, not the heading it sits under, not
       whether it is inside a fence or an HTML comment, not what the line above it says.
       B04-B07 are the consequence and they are where this battery's findings are.

  A third area is the SCOPE of the region within the certified row: the cell is the row's
  widest field, so the row's other two fields are outside every digest.  B01-B03.

EXPECTATIONS ARE DECLARED BEFORE THE RUN, in the table at the bottom, and "tolerate" is
used only where COVERAGE.md says in words that the thing is out of scope.  Where I expect
"catch" and get SILENT, that is a finding; where I expect "tolerate" and get a fire, that
is noise and is also a finding.
"""
import sys

from harness import (Harness, STATE, README, certified_row, edit_cell, quote_span,
                     para_span, M_F1, M_F2, M_A1_7870, M_INDEX)


# =========================================================================================
# GROUP A — the certified ROW, outside the certified CELL.
# COVERAGE.md's exclusion list reads "every row but :135", which says :135 is covered.
# The digest covers the row's WIDEST field only.  These three test the difference.
# =========================================================================================
def a_verdict(text):
    """B01.  The row's own verdict, in field 1, inverted."""
    n, spans = certified_row(text)
    lines = text.split("\n")
    s, e = spans[0]
    old = lines[n][s:e]
    assert "**GREEN · PROVEN, all finite posets" in old, "verdict text moved"
    new = old.replace("**GREEN · PROVEN, all finite posets",
                      "**RED · REFUTED, no finite poset", 1)
    lines[n] = lines[n][:s] + new + lines[n][e:]
    return "\n".join(lines)


def a_pointer(text):
    """B02.  Field 2 — the row's claim about what it supplies, and its doc pointer."""
    n, spans = certified_row(text)
    lines = text.split("\n")
    s, e = spans[1]
    old = lines[n][s:e]
    assert "foundation claims (1)–(3) supply" in old, "field-2 text moved"
    new = old.replace("foundation claims (1)–(3) supply",
                      "FABRICATED claims (1)–(9) supply", 1)
    lines[n] = lines[n][:s] + new + lines[n][e:]
    return "\n".join(lines)


def a_after_pipe(text):
    """B03.  Text appended to the certified row AFTER its closing pipe.

    Outside every field the parser returns, so outside the digest, outside the three-column
    check and outside the whole-file '**'-parity tally, which are all taken over
    between-pipe fragments only.  GFM drops cells past the header's arity, so this is the
    weakest of the three as a rendering attack and it is reported as such — it is here to
    map the parser's boundary, not to claim damage.
    """
    n, _ = certified_row(text)
    lines = text.split("\n")
    lines[n] = lines[n] + " RETRACTED — the proof in this row does not close."
    return "\n".join(lines)


# =========================================================================================
# GROUP B — the LOCATOR.  Every one of these leaves the certified bytes EXACTLY as
# certified and changes only where they sit or what surrounds them.
# =========================================================================================
def b_relocate(text):
    """B04.  A certified block moved VERBATIM to a superseded-drafts appendix."""
    lines = text.split("\n")
    s, e = quote_span(text, M_A1_7870)
    block = lines[s:e]
    rest = lines[:s] + lines[e:]
    return "\n".join(rest + ["", "## Appendix Z — superseded drafts, retained for the "
                             "record only; nothing below is in force", ""] + block)


def b_fence(text):
    """B05.  A certified block wrapped in a code fence — renders as a code sample."""
    lines = text.split("\n")
    s, e = quote_span(text, M_F1)
    return "\n".join(lines[:s] + ["```text"] + lines[s:e] + ["```"] + lines[e:])


def b_comment(text):
    """B06.  A certified block wrapped in an HTML comment — GONE from the rendered page."""
    lines = text.split("\n")
    s, e = quote_span(text, M_F1)
    return "\n".join(lines[:s] + ["<!--"] + lines[s:e] + ["-->"] + lines[e:])


def b_retract_above(text):
    """B07.  A retraction inserted immediately above a certified block, block untouched."""
    lines = text.split("\n")
    s, _ = quote_span(text, M_A1_7870)
    ins = ["**RETRACTED 2026-08-01. The correction block below was filed in error, is void, "
           "and is retained only so the retraction has something to point at.**", ""]
    return "\n".join(lines[:s] + ins + lines[s:])


# =========================================================================================
# GROUP C — the NORMALISATION, probed in both directions.
# =========================================================================================
def c_nbsp_at_edge(text):
    """B09.  U+00A0 appended at a certified block's OUTER edge.

    COVERAGE.md says U+00A0 is not whitespace to `N`.  If that is right, padding the outer
    edge with U+00A0 must FIRE even though padding it with ASCII space does not.  This is
    the claim's own test, at the one place the tolerance lives.
    """
    lines = text.split("\n")
    _, e = quote_span(text, M_F2)
    lines[e - 1] = lines[e - 1] + " "
    return "\n".join(lines)


def c_ascii_at_edge(text):
    """B10.  ASCII spaces appended at the same edge — the stated tolerance, on a README
    block rather than on the ledger cell mg-2216 tested it on."""
    lines = text.split("\n")
    _, e = quote_span(text, M_F2)
    lines[e - 1] = lines[e - 1] + "    "
    return "\n".join(lines)


def c_interior_edge(text):
    """B11.  A single trailing space on an INTERIOR line of a certified block.

    Invisible in the rendered page, invisible in most diffs, one character.  `N` strips
    only the region's two ends, so it must fire.  The contrast with B10 is the whole
    content of the normalisation rule, measured.
    """
    lines = text.split("\n")
    s, e = quote_span(text, M_F2)
    assert e - s > 2
    lines[s + 1] = lines[s + 1] + " "
    return "\n".join(lines)


def c_lookalike(text):
    """B12.  One ASCII hyphen-minus -> U+2010 HYPHEN inside a certified block.

    Visually identical in most fonts.  `N` does no Unicode normalisation, so it must fire;
    an implementation that had reached for NFKC here would fold it and go green.
    """
    lines = text.split("\n")
    s, e = quote_span(text, M_A1_7870)
    for k in range(s, e):
        if "-" in lines[k]:
            lines[k] = lines[k].replace("-", "‐", 1)
            return "\n".join(lines)
    raise AssertionError("no ASCII hyphen in the block")


def c_cell_zwsp(text):
    """B13.  A zero-width space inserted mid-word in the certified cell.

    Zero visible change, +1 character, and it breaks the word for search.  The digest must
    fire; nothing else in the instrument could.
    """
    def fn(cell):
        i = cell.find("pseudomanifold")
        assert i >= 0
        return cell[:i + 6] + "​" + cell[i + 6:]
    return edit_cell(text, fn)


# =========================================================================================
# GROUP D — the stated boundary, tested so the statement is checked and not assumed.
# =========================================================================================
def d_index_table(text):
    """B14.  The per-row index table's own numeric column falsified.

    COVERAGE.md names this as deliberately uncovered.  Expect tolerate; this is here to
    confirm the statement is TRUE, which is a different job from finding a miss.
    """
    lines = text.split("\n")
    s, e = para_span(text, M_INDEX)
    for k in range(0, s):
        if lines[k].startswith("|") and "7,705" in lines[k]:
            lines[k] = lines[k].replace("7,705", "9,705", 1)
            return "\n".join(lines)
    raise AssertionError("index-table figure 7,705 not found above the note")


def d_appendix_a(text_state):
    """B15.  STATE.md's Appendix A — the convention this whole cluster establishes.

    run_all.sh says "THE CONVENTION THIS ESTABLISHES lives in STATE.md's Appendix A".
    It is not in CERTIFIED and COVERAGE.md's exclusion list covers it under "every row but
    :135" only by implication.  Expect tolerate; reported as a boundary, not a defect.
    """
    old = ("**Re-running a REVISION-PINNED instrument certifies the revision it is pinned "
           "to, never the commit that re-ran it")
    assert text_state.count(old) == 1, "Appendix A convention sentence not found"
    return text_state.replace(
        old, "**Re-running a REVISION-PINNED instrument certifies the commit that re-ran "
             "it, exactly as `b68db5d` said it did", 1)


def d_row_indent(text):
    """B16.  The certified row indented by one space.

    The parser requires the line to START with '|'.  One leading space and the row is not
    a table row at all.  Expect catch — and specifically FAIL, since the row becomes
    unlocatable rather than merely changed.
    """
    n, _ = certified_row(text)
    lines = text.split("\n")
    lines[n] = " " + lines[n]
    return "\n".join(lines)


BATTERY = [
    # id     class                 expect       fn            path      description
    ("B01", "certified-row", "catch", a_verdict, STATE,
     "row :135 FIELD 1 (the row's own verdict): '**GREEN · PROVEN, all finite posets' -> "
     "'**RED · REFUTED, no finite poset'"),
    ("B02", "certified-row", "catch", a_pointer, STATE,
     "row :135 FIELD 2: 'foundation claims (1)–(3) supply' -> "
     "'FABRICATED claims (1)–(9) supply'"),
    ("B03", "certified-row", "tolerate", a_after_pipe, STATE,
     "row :135: 'RETRACTED — the proof in this row does not close.' appended AFTER the "
     "closing pipe (outside every field the parser returns; GFM drops it too)"),
    ("B04", "locator-position", "catch", b_relocate, README,
     "the mg-7870 correction block MOVED VERBATIM under a new heading "
     "'Appendix Z — superseded drafts ... nothing below is in force'"),
    ("B05", "locator-context", "catch", b_fence, README,
     "the certified F1 correction block wrapped in a ```text fence — bytes identical, "
     "renders as a code sample instead of a correction"),
    ("B06", "locator-context", "catch", b_comment, README,
     "the certified F1 correction block wrapped in an HTML comment — bytes identical, "
     "ABSENT from the rendered page"),
    ("B07", "locator-context", "catch", b_retract_above, README,
     "a 'RETRACTED 2026-08-01 ... is void' paragraph inserted immediately ABOVE the "
     "mg-7870 correction block; the block itself untouched"),
    ("B09", "normalisation", "catch", c_nbsp_at_edge, README,
     "U+00A0 appended at the F2 block's OUTER edge (COVERAGE.md: U+00A0 is not "
     "whitespace to N, so the tolerance must not extend to it)"),
    ("B10", "normalisation", "tolerate", c_ascii_at_edge, README,
     "four ASCII spaces appended at the F2 block's OUTER edge (the stated tolerance, "
     "tested on a README block rather than on the ledger cell)"),
    ("B11", "normalisation", "catch", c_interior_edge, README,
     "one trailing space on an INTERIOR line of the F2 block (invisible rendered, "
     "invisible in most diffs, one character)"),
    ("B12", "normalisation", "catch", c_lookalike, README,
     "one ASCII '-' -> U+2010 HYPHEN inside the mg-7870 correction block "
     "(visually identical; NFKC would have folded it)"),
    ("B13", "normalisation", "catch", c_cell_zwsp, STATE,
     "U+200B ZERO WIDTH SPACE inserted mid-word in 'pseudomanifold' in the certified cell "
     "(zero visible change, +1 character)"),
    ("B14", "stated-boundary", "tolerate", d_index_table, README,
     "the per-row index table's '7,705' falsified to '9,705' "
     "(COVERAGE.md names this uncovered — confirming the statement, not hunting a miss)"),
    ("B15", "stated-boundary", "tolerate", d_appendix_a, STATE,
     "STATE.md Appendix A: 'Re-running a revision-pinned instrument' -> "
     "'Re-running a working-tree instrument' — the convention this cluster establishes, "
     "inverted"),
    ("B16", "parser", "catch", d_row_indent, STATE,
     "the certified row indented by ONE SPACE (the parser requires the line to start "
     "with '|')"),
]


def main():
    h = Harness()
    print("mg-babf — INDEPENDENT mutation battery against mg-7870's digest-based control")
    print("=" * 86)
    print("None of these is one of mg-2216's fourteen.  Those are the repair's known-answer")
    print("set; they are re-run as a regression in regression_2216_b2.py, not reused here.")
    print()
    st, rm = h.text(STATE), h.text(README)
    print(f"STATE.md  at rest : {len(st.encode('utf-8'))} bytes, {len(st)} characters")
    print(f"README.md at rest : {len(rm.encode('utf-8'))} bytes, {len(rm)} characters")
    n, spans = certified_row(st)
    line = st.split("\n")[n]
    widths = [e - s for s, e in spans]
    print(f"certified row     : line :{n + 1}, {len(line)} characters, "
          f"{len(spans)} fields of widths {widths}")
    print(f"                    the digest covers the WIDEST field only "
          f"({max(widths)} of {len(line)} raw characters, "
          f"{100.0 * max(widths) / len(line):.1f}% of the line)")
    print(f"mutations         : {len(BATTERY)}, each applied to the snapshot, never stacked")
    print()

    if h.positive_control() != 0:
        print("ABORT — the clean tree does not pass; nothing below would mean anything.")
        return 3

    for mid, kind, expect, fn, path, desc in BATTERY:
        h.mutate(mid, kind, expect, desc, {path: fn})

    miss = h.summary("mg-babf's own battery against the repaired instrument")
    print()
    print("READ THE 'tolerate' ROWS AS BOUNDARY CONFIRMATIONS, NOT AS PASSES: B03, B10, B14")
    print("and B15 exit 0 because COVERAGE.md says they are outside the boundary, and the")
    print("point of running them is that the statement is now TESTED rather than trusted.")
    return 0 if miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
