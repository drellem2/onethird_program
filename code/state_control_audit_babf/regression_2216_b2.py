#!/usr/bin/env python3
"""mg-babf — THE REGRESSION: mg-2216's five B2 mutations, re-implemented from scratch.

mg-2216's B2 was the finding that FIVE independent mutations of the certified ledger cell
exited 0 against the pre-repair `delta_control.py`.  mg-7870's repair is only a repair if
all five now fail.  A repair that does not close its own stated findings is not a repair.

WHY RE-IMPLEMENTED RATHER THAN RE-RUN.  mg-7870's evidence is mg-2216's own battery re-run
unmodified, and that is the right evidence for mg-7870 to offer.  It is not evidence I can
offer, because a battery re-run by the author of the repair tests exactly the mutations the
repair was built against.  These five are written here from mg-2216's PROSE DESCRIPTIONS of
them — quoted verbatim below each — with my own cell locator, my own sentence splitter and
my own filler construction.  Where the exit code agrees with mg-7870's re-run, the two
independent implementations agree; where a description admits more than one implementation,
that is stated in the mutation's own note.

The five, as mg-2216 published them (docs/OneThird-STATE-Landing-Control-mg2da3-
IndependentAudit.md, table under B2):

    M01  single-character   "every ridge in 1 or 2 facets" -> "1 or 3"
    M02  length-preserving  "the proof is sound" -> "the proof is bogus"
    M03  whitespace-only    the spaces in "**The mathematics.**" -> U+00A0
    M05  reordering         two adjacent sentences swapped, length and token multiset kept
    M06  bulk-but-quiet     the last 3,000 characters replaced by 'x', ** markers preserved

All five must be CAUGHT.  Anything else is the finding not closing.
"""
import sys

from harness import Harness, STATE, content_field, edit_cell


def one_character(cell):
    """M01.  A false statement about the pseudomanifold the row's mathematics rests on."""
    old = "every ridge in 1 or 2 facets"
    assert cell.count(old) == 1, f"target appears {cell.count(old)} times"
    return cell.replace(old, "every ridge in 1 or 3 facets", 1)


def verdict_inverted(cell):
    """M02.  The row's verdict on its own proof, inverted in five characters."""
    old = "the proof is sound"
    assert cell.count(old) == 1
    return cell.replace(old, "the proof is bogus", 1)


def spaces_to_nbsp(cell):
    """M03.  No visible character changes at all; the heading stops rendering."""
    old = "**The mathematics.**"
    assert cell.count(old) == 1
    return cell.replace(old, old.replace(" ", " "), 1)


def swap_adjacent_sentences(cell):
    """M05.  Two adjacent sentences swapped.

    My own sentence splitter and my own choice of pair, so this is not mg-2216's exact
    edit — the description admits many.  The invariant the description names is what is
    asserted: total length preserved, and the whitespace-separated token MULTISET
    preserved.  Both are checked here, and the check is part of the mutation.
    """
    marker = "**The mathematics.**"
    i = cell.find(marker)
    assert i >= 0
    tail = cell[i:]
    # split on ". " boundaries in the tail; take the first two whole sentences after the
    # heading sentence and exchange them in place.
    parts, start, found = [], 0, 0
    k = 0
    while k < len(tail) - 1 and found < 3:
        if tail[k] == "." and tail[k + 1] == " ":
            parts.append((start, k + 2))
            start = k + 2
            found += 1
        k += 1
    assert len(parts) >= 3, f"only {len(parts)} sentence boundaries found"
    (a0, a1), (b0, b1) = parts[1], parts[2]
    assert a1 == b0
    swapped = tail[:a0] + tail[b0:b1] + tail[a0:a1] + tail[b1:]
    assert len(swapped) == len(tail)
    assert sorted(swapped.split()) == sorted(tail.split()), "token multiset not preserved"
    return cell[:i] + swapped


def bulk_quiet(cell):
    """M06.  The last 3,000 characters replaced by 'x', ** markers preserved so parity holds.

    38% of the certified cell.  The filler carries the same number of '**' occurrences as
    the slice it replaces, so the whole-file '**'-parity invariant in the control's section
    6 cannot be what fires — the region digest is the only thing that can.
    """
    n = 3000
    assert len(cell) > n
    head, slug = cell[:-n], cell[-n:]
    stars = slug.count("**")
    filler = "**" * stars + "x" * (n - 2 * stars)
    assert len(filler) == n
    assert filler.count("**") % 2 == slug.count("**") % 2
    out = head + filler
    assert len(out) == len(cell)
    return out


MUTATIONS = [
    ("M01", "single-character", one_character,
     "row :135 cell: 'every ridge in 1 or 2 facets' -> '1 or 3' (one character, "
     "a false statement about the pseudomanifold)"),
    ("M02", "length-preserving", verdict_inverted,
     "row :135 cell: 'the proof is sound' -> 'the proof is bogus' "
     "(five characters, the row's verdict on its own proof)"),
    ("M03", "whitespace-only", spaces_to_nbsp,
     "row :135 cell: the ASCII spaces in '**The mathematics.**' -> U+00A0 "
     "(no visible character changes; the heading stops rendering)"),
    ("M05", "reordering", swap_adjacent_sentences,
     "row :135 cell: two adjacent sentences swapped "
     "(length AND whitespace-separated token multiset both preserved, asserted in code)"),
    ("M06", "bulk-but-quiet", bulk_quiet,
     "row :135 cell: the last 3,000 of 7,876 characters replaced by 'x', "
     "'**' count preserved (38% of the certified cell)"),
]


def main():
    h = Harness()
    print("mg-babf — mg-2216's five B2 mutations, RE-IMPLEMENTED and re-run")
    print("=" * 86)
    print("Every one of these exited 0 against the PRE-repair delta_control.py.")
    print("mg-7870 claims the repair closes all five.  This is the independent check.")
    print()
    state = h.text(STATE)
    n, s, e = content_field(state)
    cell = state.split("\n")[n][s:e].strip(" \t\r\n")
    print(f"certified row : line :{n + 1} (1-indexed), located by attempt id, not line number")
    print(f"content cell  : {len(cell)} characters stripped, "
          f"{e - s} raw, {len(cell.encode('utf-8'))} bytes stripped")
    print()

    if h.positive_control() != 0:
        print("ABORT — the clean tree does not pass; nothing below would mean anything.")
        return 3

    for mid, kind, fn, desc in MUTATIONS:
        h.mutate(mid, kind, "catch", desc,
                 {STATE: lambda t, fn=fn: edit_cell(t, fn)})

    miss = h.summary("mg-2216's five B2 mutations against the REPAIRED instrument")
    print()
    if miss == 0:
        print("VERDICT: B2 CLOSES.  All five mutations that exited 0 against the pre-repair")
        print("         instrument are now non-zero, reproduced by an implementation that")
        print("         shares no code with mg-2216's battery or mg-7870's repair.")
    else:
        print(f"VERDICT: B2 DOES NOT CLOSE — {miss} of 5 still exit 0.")
    return 0 if miss == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
