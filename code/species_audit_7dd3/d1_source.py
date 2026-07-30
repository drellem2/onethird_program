"""D1 -- EVERY CORRECTION mg-a4ef CLAIMS, CHECKED AT SOURCE, THROUGH NO CHECKER.

The brief: *"Do not accept a green run as evidence.  For each correction the
parent claims, go to the source and check the corrected state is there,
independent of any checker."*

So this file opens the named file, reads the named bytes, and asserts on them.
It imports nothing from `species_repair_a4ef`, `species_repair_6f61` or
`species_remainder_f8fa`.  Where a claim is "X is no longer asserted", the test
is not "the string is absent" -- the repair's convention, which this audit
accepts, is that a withdrawn sentence may be QUOTED where it is being withdrawn.
The test is that every occurrence is inside such a passage, and D1 prints the
REASONS, from `kern7dd3.reasons`, so a reader can see what is holding it.

    python3 code/species_audit_7dd3/d1_source.py
"""

import os
import re
import sys

from kern7dd3 import hdr, find, reasons
from statements7dd3 import STATEMENTS, DOC

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
OWN = {sid: own for sid, _l, _p, own in STATEMENTS}
PATS = {sid: p for sid, _l, p, _o in STATEMENTS}


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def check(label, cond):
    global bad
    bad += (not cond)
    print("  %-68s %s" % (label[:68], "ok" if cond else "*** FAILS ***"))
    return cond


def not_asserted(rel, sid):
    """Every occurrence of statement `sid` in file `rel` is exonerated.
    Prints line and the SET of reasons for each."""
    global bad
    text = read(rel)
    hits = find(text, PATS[sid])
    live = []
    for ln in hits:
        rs = reasons(text, ln, OWN[sid])
        print("      %-46s line %-5d %s"
              % (rel.split("/")[-1], ln,
                 "held by {%s}" % ", ".join(sorted(rs)) if rs
                 else "*** STILL ASSERTED ***"))
        if not rs:
            live.append(ln)
    ok = not live
    bad += (not ok)
    print("  %-68s %s"
          % ("%s: %s occurs %d time(s), 0 asserted" % (rel.split("/")[-1], sid,
                                                       len(hits)),
             "ok" if ok else "*** %d STILL ASSERTED ***" % len(live)))
    return ok


# ---------------------------------------------------------------------------
hdr("D1a  Y1 -- THE MAJOR.  X3 AND THE AM 17.5 QUOTATION, AT SOURCE")
print("  mg-73df found X3 at t6_fock_and_record.py:149 and at")
print("  out_t6_fock_and_record.txt:66, unmarked, inside a run ending")
print("  T6 TOTAL BAD: 0.  Both files are opened here directly.")
print()

not_asserted("code/species_7d75/t6_fock_and_record.py", "X3")
not_asserted("code/species_7d75/out_t6_fock_and_record.txt", "X3")
not_asserted("code/species_7d75/t6_fock_and_record.py", "X7")
not_asserted("code/species_7d75/out_t6_fock_and_record.txt", "X7")
print()

t6 = read("code/species_7d75/t6_fock_and_record.py")
o6 = read("code/species_7d75/out_t6_fock_and_record.txt")
check("t6 source states the corrected reading: CLOSURE, AND ONLY CLOSURE",
      "WHAT 4399 BASIS ELEMENTS MEASURE IS CLOSURE, AND ONLY" in t6)
check("t6 source names the repair at the correction",
      "CORRECTED AT SOURCE (mg-a4ef" in t6)
check("the committed OUTPUT carries the same correction",
      "WHAT 4399 BASIS ELEMENTS MEASURE IS CLOSURE, AND ONLY" in o6)
check("the live prose no longer claims the axiom count",
      "T5 measures it on 4399 basis elements." in t6
      and "T5 measured it against every Hopf monoid axiom with 0 failures"
      not in t6.split("CORRECTED AT SOURCE")[0])
check("the AM 17.5 quotation at source now reads Pi* in BOTH slots",
      t6.count("K(Pi*)") >= 2 and "K-bar(Pi) is the algebra" not in t6)
check("and says why the difference is harmless (17.4.1), as section 4 does",
      "Since Pi and Pi* are isomorphic" in t6)
check("the run that contains it still ends T6 TOTAL BAD: 0",
      re.search(r"T6 TOTAL BAD: 0", o6) is not None)
print()

# ---------------------------------------------------------------------------
hdr("D1b  Y2 -- THE DESCENT ALGEBRA, IN THE DOCUMENT AND AT SOURCE")

doc = read("docs/" + DOC)
t4 = read("code/species_7d75/t4_one_operation.py")

not_asserted("code/species_7d75/t4_one_operation.py", "Y2")
check("t4 line 22 region states the ANTI-isomorphism",
      "the left side is ANTI-isomorphic to" in t4)
check("t4 names the repair and the measurement that decides it",
      "CORRECTED AT SOURCE (mg-a4ef, on mg-73df's Y2)" in t4
      and "0/0/4/54/472" in t4)
check("section 0's headline box reads anti-isomorphic",
      "the left side is **anti-isomorphic to Solomon's" in doc)
check("and the old reading is gone from the document entirely",
      "the left side is **Solomon's descent algebra**" not in doc)
check("AM Thm 10.13 is still quoted in section 0, as mg-73df relied on",
      "The descent algebra is isomorphic to" in doc)
print()

# ---------------------------------------------------------------------------
hdr("D1c  Y3 / Y4 -- THE SEAM, AT SOURCE IN THE DOCUMENT")

h142 = doc.find("### 14.2")
h143 = doc.find("### 14.3")
h144 = doc.find("### 14.4")
# FLATTENED, and this line is a near-miss kept on the record.  The first
# version of the next check matched the raw bytes and FAILED, because the
# sentence wraps across a `> `-prefixed line -- which is exactly the defect
# this audit predicted (D4) in s2_seam.py's dead `quoted` variable, committed
# by the instrument that predicted it.  See OUTCOMES.md.
flat142 = re.sub(r"\s+", " ", re.sub(r"(?m)^\s*>\s?", "", doc[h142:h143]))
n_box = doc.count("THE SAME LIMITATION APPLIES TO")
check("the limitation box occurs exactly ONCE (found %d)" % n_box, n_box == 1)
check("the surviving copy is section 14.2's",
      "THE SAME LIMITATION APPLIES TO §14 ITSELF" in doc)
check("the surviving copy traces the list to TWO sources",
      "two readers of one audit produced two different lists" in flat142)
check("the five-versus-eight miscount is gone",
      "the five items in the banner" not in doc)
check("the banner it miscounted still says eight",
      "Eight things changed" in doc)
check("'a second, shelved filing' is gone", "shelved filing" not in doc)
check("and the correction is stated in place, not silently",
      "Corrected mg-a4ef, on mg-73df's Y4" in doc)
check("a note records that the duplicate was resolved, not just deleted",
      "Resolved to one copy by mg-a4ef, on mg-73df's Y3" in doc)
print()
print("  AND THE BY-NAME REFERENCE §14.3 MAKES OF §14.2 -- the thing a")
print("  resolved duplicate most easily breaks:")
quoted = "outside every beam currently pointed at this document"
check("§14.2 and §14.3 both exist and are in order",
      -1 < h142 < h143 < h144)
check("§14.3 answers §14.2 BY NAME", "§14.2 predicted" in doc[h143:h144])
check("and the sentence §14.3 quotes back IS in §14.2", quoted in flat142)
print()

# ---------------------------------------------------------------------------
hdr("D1d  Y5 -- THE TWO DOCSTRINGS, AGAINST THEIR OWN COMMITTED RUNS")

w3 = read("code/species_remainder_f8fa/w3_scope.py")
r2 = read("code/species_repair_6f61/r2_columns.py")
before = read("code/species_remainder_f8fa/out_w3_scope_before.txt")
r2o = read("code/species_repair_6f61/out_r2_columns.txt")

check("w3_scope.py's docstring says 12 problems",
      "it reported 12 problems there" in w3)
check("and its own evidence file says FAIL (12 problems)",
      "FAIL   (12 problem(s))" in before or "12 problem" in before)
check("the '6' is gone from the docstring's claim",
      "reported 6 problems" not in w3)
check("r2_columns.py's docstring says 45 cells",
      "predicted-vs-actual for all 45 cells" in r2)
check("and its own run prints 45 cells and MISSED: 2 of 45",
      "45 cells" in r2o and "MISSED: 2 of 45" in r2o)
check("the '40' is gone", "all 40 cells" not in r2)
print()
print("  BEYOND mg-73df's FIVE, claimed by mg-a4ef: w3_scope.py exited 0")
print("  unconditionally.  The source is read here; d5 RUNS it.")
check("w3_scope.py's last line is a conditional exit",
      "sys.exit(1 if bad else 0)" in w3)
check("and the unconditional exit(0) is gone",
      not re.search(r"(?m)^sys\.exit\(0\)\s*$", w3))
print()

# ---------------------------------------------------------------------------
hdr("D1e  THE EXTENT LINES EXIST AT SOURCE (their TRUTH is d2's job)")

cd = read("code/species_repair_6f61/check_doc.py")
s1 = read("code/species_repair_a4ef/s1_extent.py")
s2 = read("code/species_repair_a4ef/s2_seam.py")
check("check_doc.py prints an extent after its verdict",
      "EXTENT OF THAT VERDICT (added mg-a4ef)" in cd)
check("w3_scope.py prints an extent after its verdict",
      "EXTENT OF THAT VERDICT (added mg-a4ef)" in w3)
check("s1_extent.py prints an extent after TOTAL BAD",
      "EXTENT OF THIS NUMBER" in s1)
check("s2_seam.py prints an extent after TOTAL BAD", '\nprint("EXTENT.' in s2)
check("the document states the extents too (§14.4)",
      "WHICH EXTENTS EACH CHECKER COVERS" in doc)
print()

print("=" * 78)
print("D1 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  D1 checks the SEVEN corrections mg-a4ef claims,")
print("in the SIX files it names plus the document, by reading those files.")
print("It says nothing about any other file, about whether the corrections are")
print("COMPLETE (d2), about the seam beyond the one pair (d3), or about")
print("anything mg-a4ef did not claim.  A pass here means the claims are true")
print("where they were made -- not that they are all the claims that were due.")
sys.exit(1 if bad else 0)
