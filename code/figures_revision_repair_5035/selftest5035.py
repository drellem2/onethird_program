"""mg-5035 -- SELF-TEST.  Inputs whose answer is known by construction.

A repair whose subject is *a rule that did not do what its label said* has to
be able to go red.  Every case below is an input where the right answer is
fixed in advance, and roughly half of them assert that the repair does NOT
fire -- because a rule that excluded everything would pass a one-sided suite.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5035 as B                                              # noqa: E402

CASES = []


def case(name, got, want):
    CASES.append((name, got, want, got == want))


D = B.L._is_declared_revision

# --- the SHAPE half, alone, decides nothing ---------------------------------
case("shape alone is not enough: no cue -> not a revision",
     D("3738079", "the census gives "), False)
case("cue alone is not enough: too short -> not a revision",
     D("373807", "at "), False)
case("41 digits is past a sha and is not revision-shaped",
     D("1" * 41, "at "), False)
case("40 digits is exactly a full sha and IS revision-shaped",
     D("1" * 40, "at "), True)
case("7 digits is the shortest shape accepted", D("1234567", "at "), True)

# --- the DECLARATION half ---------------------------------------------------
case("`at ` declares", D("1234567", "measured at "), True)
case("backtick after the cue does not break it",
     D("1234567", "landed at `"), True)
case("`carried by ` declares through one filler",
     D("8490669", "carried by `"), True)
case("`HEAD is ` declares through a copula (the F1a defect)",
     D("3738079", "HEAD is "), True)
case("a sibling revision between cue and token is skipped",
     D("3942319", "`git rev-parse` on `ec98300`, `645b5a4`, `"), True)
case("a GRAIN NOUN between cue and token BREAKS the declaration",
     D("3738079", "at the census of "), False)
case("`rows` is not a filler, so it breaks it",
     D("3738079", "carried rows "), False)
case("nothing at all to the left is NOT a declaration (the table-column gap)",
     D("37380799", ""), False)
case("a bare filename to the left is not a declaration",
     D("3738079", "UNBACKED README.md "), False)

# --- end to end, through the shipped entry point ----------------------------
case("a declared all-decimal revision is not a figure",
     B.L.figures("at `1234567` the census gives 9 sites"), [9])
case("...and the OTHER number on that line survives",
     9 in B.L.figures("at `1234567` the census gives 9 sites"), True)
case("INT_MAX in prose is still a figure",
     B.L.figures("`2147483647`, an INT_MAX in a fixture"), [2147483647])
case("a big measurement with a grain noun is still a figure",
     431723379 in B.L.figures("(16999 classes, 431723379 labelled posets)"),
     True)
case("the three OLD exclusions still hold: `:`-prefix",
     B.L.figures("s3_figure.py:154"), [])
case("...`on line 89`", B.L.figures("on line 89"), [])
case("...and `2` is still not a figure", B.L.figures("2"), [])
case("`3` is a figure, as mg-bf79 settled",
     B.L.figures("the census gives 3 rows"), [3])

# --- the multiset grain of `dropped` ---------------------------------------
case("a line naming the same revision twice loses it twice",
     B.dropped("at 1234567 and at 1234567"), [1234567, 1234567])
case("dropped() is empty when nothing is declared",
     B.dropped("the census gives 33554432 relations"), [])

# --- THE POSITIVE CONTROL MUST STILL BE ABLE TO FIRE ------------------------
# If mg-56dc's copy ever acquires the exclusion, every A/B row this tree
# prints becomes a comparison of a rule with itself.
case("the UNREPAIRED control still reads the declared revision as a figure",
     1234567 in B.A.figures("at `1234567` the census gives 9 sites", small=2),
     True)
case("...and the forwarder does NOT, because it delegates",
     1234567 in B.C.figures("at `1234567` the census gives 9 sites"), False)

# --- CAN THIS SUITE GO RED?  A probe that cannot is not evidence. -----------
case("a deliberately wrong expectation is caught",
     B.L.figures("at `1234567` the census") == [1234567], False)

print("mg-5035 -- SELF-TEST")
print()
print("  population: the %d CASES below, each an input whose answer is known"
      % len(CASES))
print("  by construction")
print()
for name, got, want, ok in CASES:
    print("      %-68s %s" % (name[:68], "ok" if ok else "*** FAIL"))
    if not ok:
        print("          got  %r" % (got,))
        print("          want %r" % (want,))
print()
B.plain("...CASES that pass, one CHECK each", sum(1 for c in CASES if c[3]))
print("      ^ one unit of that number is one case")
bad = sum(1 for c in CASES if not c[3])
print()
print("selftest5035 TOTAL BAD: %d" % bad)
sys.exit(min(bad, 120))
