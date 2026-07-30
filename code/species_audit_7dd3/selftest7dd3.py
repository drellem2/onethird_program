"""SELF-TEST for mg-7dd3.  About half of these assert the detector does NOT
fire on something that looks like the defect.

A detector only ever seen to fire is a detector that fires.  The sections
below are in the order the failures actually happened while this audit was
built; four of them exist because a first version of one of the d-files got it
wrong, and each says which.

    python3 code/species_audit_7dd3/selftest7dd3.py
"""

import os
import re
import sys

from kern7dd3 import tokens, stream, find, reasons
from statements7dd3 import STATEMENTS

n = fails = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
PATS = {s[0]: s[2] for s in STATEMENTS}
OWN = {s[0]: s[3] for s in STATEMENTS}


def ok(label, cond):
    global n, fails
    n += 1
    if not cond:
        fails += 1
        print("  *** FAIL  %s" % label)


def hdr(t):
    print(t)


# ---------------------------------------------------------------------------
hdr("1  the tokeniser")
ok("alphanumeric runs survive", [t for t, _ in tokens("abc def")]
   == ["abc", "def"])
ok("case is folded", [t for t, _ in tokens("ABC")] == ["abc"])
ok("punctuation is its own token", [t for t, _ in tokens("y(i)")]
   == ["y", "(", "i", ")"])
ok("Greek is alphanumeric and survives", "π" in
   [t for t, _ in tokens("K(Π)")])
ok("a star is a token, so Pi and Pi* differ",
   [t for t, _ in tokens("K(Π*)")] != [t for t, _ in tokens("K(Π)")])
ok("line numbers are 1-based", tokens("a\nb")[1][1] == 2)
ok("a blank first line still counts", tokens("\nb")[0][1] == 2)
ok("combining marks are kept as tokens",
   len([t for t, _ in tokens("K̄(Π)")]) > len([t for t, _ in tokens("K(Π)")]))

hdr("2  the token stream crosses Python scaffolding without a mask")
SCAFFOLD = ('print("  ... axiom with 0 failures on")\n'
            'print("  4399 basis elements")\n')
s, _ = stream(SCAFFOLD)
ok("the sentence is one run in the stream",
   "axiom with 0 failures on" in s)
ok("and the scaffolding is present as tokens, not deleted", '"' in s)
ok("a pattern spanning two print() calls matches",
   bool(find(SCAFFOLD, [r"0 failures on \" \) print \( \" 4399"])))
ok("kerna4ef's masking approach and this one agree that X3 is there",
   bool(find(SCAFFOLD, [r"axiom with 0 failures"])))

hdr("3  the statement patterns FIRE on the withdrawn form")
ok("X3 fires on the struck sentence",
   bool(find("it passes every Hopf-monoid axiom with 0 failures on 4399",
             PATS["X3"])))
ok("X4 fires", bool(find("four candidates, three are controls",
                         PATS["X4"])))
ok("X5 fires", bool(find("control (ii) fires hard on 1442", PATS["X5"])))
ok("X7 fires on the source rendering",
   bool(find("Recall from Section 17.4 that K-bar(Pi) is the algebra of "
             "symmetric functions", PATS["X7"])))
ok("X8 fires", bool(find("stated in three independent agreements about the "
                         "term", PATS["X8"])))
ok("Y2 fires", bool(find("the left side is Solomon's descent algebra",
                         PATS["Y2"])))
ok("X6b fires on <= and on the glyph",
   bool(find("y(i) <= y(j)", PATS["X6b"]))
   and bool(find("y(i) ≤ y(j)", PATS["X6b"])))

hdr("4  and DO NOT fire on the corrected form -- the load-bearing half")
ok("X7 does NOT fire on Pi* in both slots",
   not find("Recall from Section 17.4 that K(Pi*) is the algebra of "
            "symmetric functions", PATS["X7"]))
ok("X6b does NOT fire on the corrected direction",
   not find("y(i) >= y(j)", PATS["X6b"]))
ok("Y2 does NOT fire on the anti-isomorphism",
   not find("the left side is ANTI-isomorphic to Solomon's descent algebra",
            PATS["Y2"]))
ok("X3 does NOT fire on the per-column reading",
   not find("what 4399 basis elements measure is CLOSURE, and only closure",
            PATS["X3"]))
ok("X4 does NOT fire on 'two statements, each computed twice'",
   not find("the four columns are TWO STATEMENTS, EACH COMPUTED TWICE",
            PATS["X4"]))
ok("X1 does NOT fire on the 3-element chain",
   not find("the smallest is the 3-ELEMENT CHAIN", PATS["X1"]))

hdr("5  the exoneration clauses, each on its own")
BODY = "it passes every Hopf-monoid axiom with 0 failures on 4399\n"
ok("a bare assertion is NOT exonerated", not reasons(BODY, 1, OWN["X3"]))
ok("naming a repair exonerates",
   "names-a-repair" in reasons(BODY + "corrected by mg-a4ef.\n", 1,
                               OWN["X3"]))
ok("an explicit negation exonerates",
   "negates" in reasons(BODY + "this is STRICKEN.\n", 1, OWN["X3"]))
ok("the per-statement negation exonerates",
   "own-negation" in reasons(BODY + "it measures CLOSURE only.\n", 1,
                             OWN["X3"]))
ok("a declared table exonerates",
   "declared-table" in reasons("STRICKEN = [\n    " + BODY + "]\n", 2,
                               OWN["X3"]))
ok("an UNRELATED ticket id does not count as an explicit negation",
   "negates" not in reasons(BODY + "the error mg-1953 repaired.\n", 1,
                            OWN["X3"]))
ok("a bare REPAIRED does not exonerate -- w3_scope.py's own false negative",
   not reasons(BODY + "this REPAIRED thing is elsewhere.\n", 1, OWN["X3"]))
ok("'is not the framework this ticket is about' does not exonerate -- "
   "c4_scope.py's",
   not reasons(BODY + "and it is not the framework this ticket is about.\n",
               1, OWN["X3"]))
ok("a bare PROVED inside 'not proved' does not exonerate its own sentence",
   not reasons("The identity is measured, not proved.\n", 1, OWN["X2a"]))
ok("a bare located inside 'not located' does not exonerate its own sentence",
   not reasons("The Aut(P) form was not located in that generality.\n", 1,
               OWN["X2c"]))

hdr("6  the reasons are a SET, so over-determination is visible")
r = reasons(BODY + "corrected by mg-a4ef: it measures CLOSURE only, and "
            "the old form is STRICKEN.\n", 1, OWN["X3"])
ok("three clauses fire at once on a triply-marked hit", len(r) >= 3)
ok("and one clause fires alone on a singly-marked hit",
   len(reasons(BODY + "corrected by mg-a4ef.\n", 1, OWN["X3"])) == 1)

hdr("7  the four defects this audit committed in itself, as regressions")
# (a) d1: a wrapped sentence matched against RAW bytes fails
doc = open(os.path.join(REPO, "docs",
                        "OneThird-Species-Hopf-Monoids-Where-This-Lives.md"),
           encoding="utf-8").read()
q = "two readers of one audit produced two different lists"
ok("(a) the sentence is NOT in the raw document -- it wraps", q not in doc)
ok("(a) and IS in the flattened one",
   q in re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", doc)))
# (b) d2: [a-z0-9]+ destroys the Pi/Pi* distinction
naive = re.findall(r"[0-9a-z]+", "K̄(Π) and K(Π*)".lower())
ok("(b) a bare [a-z0-9]+ collapses both renderings to 'k'",
   naive.count("k") == 2 and "π" not in naive)
ok("(b) the tokeniser keeps them apart",
   [t for t, _ in tokens("K̄(Π)")] != [t for t, _ in tokens("K(Π*)")])
# (c) d2: shutil.copytree opens files in BINARY -- not a read for scanning
ok("(c) binary mode is distinguishable from text mode", "b" in "rb")
# (d) d4: a 4-token line can never contain a 6-token run
ok("(d) min(6, len) is the right bar for a short line", min(6, 4) == 4)

hdr("8  the document's own strikes are 11 and the one list has 11 rows")
ok("11 strikes", len(re.findall(r"~~(.+?)~~", doc, re.S)) == 11)
ok("12 statements here -- the 11 plus Y2", len(STATEMENTS) == 12)
ok("X8 is on this list", "X8" in {s[0] for s in STATEMENTS})

print()
print("selftest7dd3: %d assertion(s), %d failure(s)" % (n, fails))
sys.exit(1 if fails else 0)
