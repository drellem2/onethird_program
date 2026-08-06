"""mg-03d1 -- self-test of THIS audit's own predicates.

Every predicate this tree relies on, put to inputs whose answer is known by
construction.  The point is not coverage.  It is that a probe which cannot go
RED over its own subject is not evidence -- so several cases below are the
DEFECT the predicate was written to catch, asserted to be caught.

Exit code = failing cases.
"""

import sys

import lib03d1 as B

BAD = 0
CASES = []


def case(name, got, want):
    global BAD
    ok = got == want
    if not ok:
        BAD += 1
    CASES.append((name, got, want, ok))


# --- label_grain: the predicate my own first run got wrong (AS1) ------------
case("label_grain: CAPITALISED noun wins over a later lowercase one",
     B.label_grain("...ROWS outside it, across 10 distinct basenames")[0],
     {"row"})
case("label_grain: ...and reports the stage it used",
     B.label_grain("...ROWS outside it, across 10 distinct basenames")[1],
     "caps")
case("label_grain: THE FIRST-DRAFT ANSWER IS NOT PRODUCED any more",
     B.label_grain("...ROWS outside it, across 10 distinct basenames")[0]
     == {"basename"}, False)
case("label_grain: a noun claimed by an embedded count is skipped, and with"
     " no lines above the answer is `-` rather than that noun",
     B.label_grain("...outside it, across 6 distinct basenames")[1], "-")
case("label_grain: header fallback offers the header's nouns",
     B.label_grain("...outside it, across 6 distinct basenames",
                   ["  target basename   sites  consuming"])[0],
     {"basename", "site"})
case("label_grain: no noun anywhere is `-`, not a guess",
     B.label_grain("...things of interest")[1], "-")
case("label_grain: lowercase head noun when nothing is capitalised",
     B.label_grain("source lines naming more than one script")[0], {"site"})

# --- embedded_counts: the floor item's population (AF) ----------------------
case("embedded_counts: finds the count inside a label",
     B.embedded_counts("...ROWS outside it, across 10 distinct basenames"),
     [(10, "basenames")])
case("embedded_counts: a bare label has none",
     B.embedded_counts("...distinct SITES outside it"), [])
case("embedded_counts: a line reference `:214` is not a count",
     B.embedded_counts("s3_figure.py:214 rows"), [])
case("embedded_counts: two counts inside one label are both found",
     len(B.embedded_counts("of 3 trees and 4 runners")), 2)

# --- top_alts: the by-name rule diff (A3d) ----------------------------------
case("top_alts: splits at depth 0 only", B.top_alts(r"a|(b|c)|d"),
     ["a", "(b|c)", "d"])
case("top_alts: an escaped pipe is not a separator",
     B.top_alts(r"a\|b|c"), [r"a\|b", "c"])
case("top_alts: a pipe in a character class is not a separator",
     B.top_alts(r"[a|b]|c"), ["[a|b]", "c"])
case("top_alts: `proven` is one of lib7522.MARK's alternatives",
     any("proven" in a for a in B.top_alts(B.L.MARK.pattern)), True)

# --- singular / grain_nouns: A1d's extractor -------------------------------
case("singular: rows -> row", B.singular("rows"), "row")
# RECORDED AS THE WRONG ANSWER, ASSERTED SO IT STAYS VISIBLE.  `species` ends
# in `ies`, so the crude rule makes it `specy`.  The case asserts `specy`
# rather than being deleted, because a de-pluraliser this rough is a fact about
# A1d's 400 and a reader should be able to see it without reading the source.
case("singular: `species` -> `specy` -- THE CRUDE RULE, KEPT VISIBLE",
     B.singular("species"), "specy")
case("grain_nouns: takes the last content word",
     "basenames" in B.grain_nouns("...across 10 distinct basenames"), True)
case("grain_nouns: drops stop words",
     "the" in B.grain_nouns("the total of the rows"), False)

# --- my_rows: the second enumerator (A3a) ----------------------------------
rows = B.my_rows(None)
case("my_rows: returns (file, line, basename) triples",
     all(len(r) == 3 for r in rows), True)
case("my_rows: SITES are never more than ROWS",
     len(B.my_sites(rows)) <= len(rows), True)
case("my_rows: at least one site names two different scripts",
     len(rows) > len(B.my_sites(rows)), True)

# --- THE KNOWN-FALSE CLAIM, ASSERTED AS FALSE ------------------------------
# `figures()`'s deleted comment claimed to exclude `a git revision`.  It does
# not.  Asserting the exclusion AS FALSE means a later real fix turns this row
# red and NAMES ITSELF, instead of the claim quietly becoming true and nobody
# learning that it had been false for the whole arc.  This is the parent's own
# idiom and it is adopted rather than re-invented.
case("figures() STILL reads an all-decimal short revision as a figure",
     1234567 in B.L.figures("at `1234567` the census gives 9 sites"), True)

# --- CAN THIS TREE GO RED?  A probe that cannot is not evidence. ------------
case("a label with a wrong grain IS caught by label_grain",
     B.label_grain("distinct executing SITES behind those rows")[0], {"site"})
case("...and the pre-repair label is NOT reported as stating a grain",
     B.label_grain("...outside it, across 6 distinct basenames")[1] != "caps",
     True)

print("mg-03d1 -- SELF-TEST")
print()
print("  population: the %d CASES below, each an input whose answer is known"
      % len(CASES))
print("  by construction")
print()
for name, got, want, ok in CASES:
    print("      %-64s %s" % (name[:64], "ok" if ok else "*** FAIL"))
    if not ok:
        print("          got  %r" % (got,))
        print("          want %r" % (want,))
print()
B.plain("...CASES that pass, one CHECK each", sum(1 for c in CASES if c[3]))
print("      ^ one unit of that number is one self-test case")
B.plain("...CASES that fail, one CHECK each", BAD)
print("      ^ one unit of that number is one self-test case")
print()
print("  RECORDED, NOT REPAIRED: `singular('species') == 'specy'`.  The")
print("  de-pluraliser is crude and this case proves it, which is why the case")
print("  asserts the WRONG answer rather than being deleted.  A1d prints the")
print("  full extracted vocabulary so a reader can see every merge it made;")
print("  trimming the list would make its collapse ratio a fact about my")
print("  trimming.  See `a6_self.py`/AS5.")
print()
print("selftest03d1 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
