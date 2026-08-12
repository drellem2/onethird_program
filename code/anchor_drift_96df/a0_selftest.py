"""mg-96df a0 -- SELF-TEST OF THE MATCH LADDER, on planted text.

The whole finding of this ticket is that a matcher's PREDICATE decides what it
reports as unrepairable.  An instrument making that claim has to show its own
matcher answers correctly on cases whose answers are known by construction --
including, first and loudest, the case that produced the wrong report: a line
that gained a strike and a warning suffix.

Every case below is synthetic.  Nothing here reads the corpus.
"""
import sys

import lib96df as L

FAIL = 0
CHECKS = 0


def check(name, got, want):
    global FAIL, CHECKS
    CHECKS += 1
    ok = got == want
    if not ok:
        FAIL += 1
    print("  %-4s %-46s got %-18s want %s"
          % ("ok" if ok else "FAIL", name, got, want))


def banner(t):
    print("\n" + t)
    print("-" * 78)


def exact_only(old_lines, old_n, new_lines):
    """mg-688c's POP-D predicate, reimplemented in one line so this file can
    DEMONSTRATE the difference rather than assert it: is the old line present
    verbatim at the new revision?"""
    old = L.line_at(old_lines, old_n)
    hits = [i + 1 for i, ln in enumerate(new_lines) if ln == old]
    return hits[0] if len(hits) == 1 else None


OLD = [
    "# A document",
    "",
    "## Kill-shot 2 - Standard dominance - **GREEN**",
    "",
    "| standard dominance | **holds** |",
    "| standard-dominance failures (n<=6 exhaustive + n=7 top-lambda spot) | 0 / 132 |",
    "a short line",
    "a short line",
    "**Every one of the 166 refuters has delta(P) in {0.473, 0.474, 0.500}** -- i.e. it",
    "this sentence is deleted outright and has no successor anywhere at all",
]

# The new revision, built by APPLYING THIS CORPUS'S REPAIR IDIOM: a banner is
# inserted at the top (pushing everything down 3), two lines gain a strike plus
# a warning suffix, one line is unchanged, one is deleted.
NEW = [
    "# A document",
    "",
    "> **BANNER: a scope correction was inserted here.**",
    "> second banner line",
    "",
    "## Kill-shot 2 - Standard dominance - ~~**GREEN**~~ **GREEN-IN-FRAME ONLY**",
    "",
    "| standard dominance | **holds** |",
    "| standard-dominance failures (n<=6 exhaustive + n=7 top-lambda spot) | 0 / 132 -- "
    "**SAMPLING ARTIFACT, NEVER QUOTABLE BARE.** |",
    "a short line",
    "a short line",
    "**Every one of the 166 refuters has delta(P) in {0.473, 0.474, 0.500}** -- i.e. it",
]


def main():
    banner("1. THE CASE THAT PRODUCED THE WRONG REPORT -- a line that gained a "
           "strike\n   and a warning suffix.  Exact matching calls this GONE.")
    m = L.relocate(OLD, 3, NEW)
    check("heading :3 tier", m.tier, "PREFIX")
    check("heading :3 lands at", m.line, 6)
    check("exact-only reports no target for :3", exact_only(OLD, 3, NEW), None)

    m = L.relocate(OLD, 6, NEW)
    check("data row :6 tier", m.tier, "PREFIX")
    check("data row :6 lands at", m.line, 9)
    check("exact-only reports no target for :6", exact_only(OLD, 6, NEW), None)
    # ...and it is RIGHT about its own predicate and WRONG as a conclusion.
    check("exact-only agrees where nothing was appended", exact_only(OLD, 5, NEW), 8)

    banner("2. AN UNCHANGED LINE PUSHED DOWN BY THE BANNER -- exact and unique.")
    m = L.relocate(OLD, 5, NEW)
    check("unchanged :5 tier", m.tier, "EXACT")
    check("unchanged :5 lands at", m.line, 8)

    m = L.relocate(OLD, 9, NEW)
    check("unchanged :9 tier", m.tier, "EXACT")
    check("unchanged :9 lands at", m.line, 12)

    banner("3. AMBIGUITY IS NOT A GUESS.  Two identical short lines exist at\n"
           "   both revisions; the ladder must refuse rather than pick one.")
    m = L.relocate(OLD, 7, NEW)
    check("duplicated line tier", m.tier, "AMBIGUOUS")
    check("duplicated line has no answer", m.line, None)

    banner("4. GENUINE ABSENCE IS DISTINCT FROM AMBIGUITY AND FROM DRIFT.")
    m = L.relocate(OLD, 10, NEW)
    check("deleted line tier", m.tier, "GONE")
    check("deleted line has no answer", m.line, None)

    banner("5. EDITED IN PLACE -- the number still resolves.  This is the\n"
           "   ComparisonRoute:104 shape, and calling it a BROKEN ANCHOR is wrong.")
    a = ["x", "| **SD-Cayley** | lambda2 = lambda_std | Empirically supported, 0/132. |"]
    b = ["x", "| **SD-Cayley** | lambda2 = lambda_std | Empirically supported, 0/132. "
              "~~withdrawn~~ **THE BARE FIGURE IS WITHDRAWN.** |"]
    m = L.relocate(a, 2, b)
    check("edited-in-place tier", m.tier, "SAME-LINE-AMENDED")
    check("edited-in-place lands at", m.line, 2)
    check("edited-in-place RESOLVES", m.resolves, True)
    check("edited-in-place is determinate", m.determinate, True)

    m = L.relocate(a, 1, a)
    check("untouched line tier", m.tier, "SAME-LINE-EXACT")
    check("untouched line RESOLVES", m.resolves, True)

    banner("6. THE >= 25-CHAR EVIDENCE FLOOR.  A prefix shorter than the floor\n"
           "   must not be allowed to relocate anything (mg-cdd5's rule).")
    short_o = ["| a | b |"]
    short_n = ["zzz", "| a | b | and much more text appended here to make it longer |"]
    m = L.relocate(short_o, 1, short_n)
    check("9-char prefix refused", m.tier, "GONE")
    long_o = ["| a very much longer table row indeed | b |"]
    long_n = ["zzz", "| a very much longer table row indeed | b | appended |"]
    m = L.relocate(long_o, 1, long_n)
    check("42-char prefix accepted", m.tier, "PREFIX")

    banner("6b. THE TRAILING-DELIMITER CONCESSION, and its guard.  Dropping a\n"
           "    table row's closing `|` is the whole concession -- it must not\n"
           "    let a key below the floor through.")
    check("key drops a closing pipe", L.prefix_key("| a | b |"), "| a | b")
    check("key leaves prose alone", L.prefix_key("a sentence."), "a sentence.")
    tiny_o = ["| ab |"]
    tiny_n = ["zzz", "| ab | plus a great deal of appended warning text here |"]
    m = L.relocate(tiny_o, 1, tiny_n)
    check("short key still refused after strip", m.tier, "GONE")

    banner("7. RANGES.  Consensus first, then verify the WHOLE range -- because\n"
           "   a quoted paragraph contains blank and one-word lines that match\n"
           "   everywhere or nowhere, and those must not veto it.")
    m = L.relocate_block(OLD, 5, 6, NEW)
    check("contiguous range tier", m.tier, "BLOCK-PREFIX")
    check("contiguous range lands at", m.line, 8)

    # OLD 5..8 spans the two duplicated short lines, which cannot be placed
    # alone.  The two placeable lines still carry the range.
    m = L.relocate_block(OLD, 5, 8, NEW)
    check("blank/duplicate lines do not veto", m.tier, "BLOCK-PREFIX")
    check("range with unplaceable lines lands at", m.line, 8)

    # ...but a range that only lands in PART is still refused, and says so.
    # Here the range's two voters agree on +3 and its LAST line was rewritten
    # rather than appended to, so the block does not carry whole.
    partial = list(NEW)
    partial[11] = "**Every one of the 166 refuters** -- REWRITTEN, and not an append"
    m = L.relocate_block(OLD, 5, 9, partial)
    check("partially-landing range refused", m.tier, "BLOCK-PREFIX-PARTIAL")
    check("a PARTIAL block is not determinate", m.determinate, False)
    # A genuine split: the second line of the range survives, but ABOVE the
    # first rather than below it, so the two land at different offsets.
    ragged_new = ["this sentence is deleted outright and has no successor anywhere at all"] + NEW
    m = L.relocate_block(OLD, 9, 10, ragged_new)
    check("split range refused", m.tier, "BLOCK-SPLIT")
    m = L.relocate_block(OLD, 9, 10, NEW)
    check("range whose tail was deleted refused", m.tier, "BLOCK-EXACT-PARTIAL")
    check("...and is not determinate", m.determinate, False)
    m = L.relocate_block(["only this line, deleted outright and gone"], 1, 1, NEW)
    check("range with no placeable line at all", m.tier, "BLOCK-BROKEN")

    banner("8. SECTION ANCHORS -- the durable form, and its own failure mode.")
    h = L.enclosing_heading(NEW, 9)
    check("enclosing heading level", h[0], 2)
    check("enclosing heading found at", h[2], 6)
    check("unique heading is unique", L.heading_is_unique(NEW, h[1]), True)
    dup = ["## S", "a", "## S"]
    check("repeated heading is NOT durable", L.heading_is_unique(dup, "S"), False)

    banner("9. NORMALISATION MUST NOT ERASE CONTENT -- only markup.")
    check("markup stripped", L.norm("**a**  `b` ~~c~~"), "a b c")
    check("strike detected", L.strike_added("a", "~~a~~ b"), True)
    check("strike not invented", L.strike_added("~~a~~", "~~a~~ b"), False)

    banner("10. MISSING IS NOT EMPTY.")
    check("line_at on MISSING", L.line_at(L.MISSING, 1), None)
    check("MISSING is not ''", L.MISSING == "", False)

    print("\n%s" % ("=" * 78))
    print("a0 SELFTEST: %d checks, %d FAIL" % (CHECKS, FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
