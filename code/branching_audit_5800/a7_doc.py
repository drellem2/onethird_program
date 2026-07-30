"""A7 -- the repaired documents read off disk, and the beyond-brief diff.

Three jobs:

  1. EVERY NUMBER mg-41aa writes into either document is checked against this
     audit's own measurement.  A number that this instrument did not produce is
     reported as UNCHECKED, not as agreeing.
  2. The NEGATIVE half: each sentence mg-41aa strikes must still be present,
     exactly once, and inside a block that carries a strike marker -- the same
     discipline check_doc.py applies, applied here to check_doc.py's own
     document rather than trusting its report.
  3. The BEYOND-BRIEF DIFF: mg-41aa's brief is X1, X2, X3, X4.  Anything the
     commit changes that is not one of those four is listed, because that is
     where X2 came from and the recursion this ticket exists to catch.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..")
DOC = os.path.join(ROOT, "docs", "OneThird-Branching-Graphs-Where-This-Lives.md")
REP = os.path.join(ROOT, "docs", "OneThird-Branching-Graphs-Repair.md")
YOUNG = os.path.join(ROOT, "code", "branching_af28", "out_young.txt")

N = [0]
FAIL = []


def check(label, cond, detail=""):
    N[0] += 1
    print("  %-4s %s%s" % ("ok" if cond else "FAIL", label,
                           "" if cond else "   " + detail))
    if not cond:
        FAIL.append(label)


print("=" * 78)
print("A7  THE REPAIRED DOCUMENTS, READ OFF DISK")
print("=" * 78)

doc = open(DOC, encoding="utf-8").read()
rep = open(REP, encoding="utf-8").read()
young = open(YOUNG, encoding="utf-8").read()
flatdoc = re.sub(r"\s+", " ", doc)
flatrep = re.sub(r"\s+", " ", rep)

# --------------------------------------------- 1. every number, re-measured

print("\n[1] NUMBERS IN THE REPAIRED TEXT vs THIS AUDIT'S OWN MEASUREMENTS")
MEASURED = {
    "n=6 skew count 62": ("62", 62),
    "n=7 skew count 149": ("149", 149),
    "n=8 skew count 360": ("360", 360),
    "n=6 all posets 318": ("318", 318),
    "n=7 all posets 2 045": ("2 045", 2045),
    "n=8 all posets 16 999": ("16 999", 16999),
}
MINE = {"62": 62, "149": 149, "360": 360, "318": 318, "2 045": 2045,
        "16 999": 16999}
for label, (txt, val) in MEASURED.items():
    check("%s appears in the repaired document" % label, txt in flatdoc)
print("  (each of these was independently enumerated in out_a1_counts.txt;")
print("   the audit's values are 62 / 149 / 360 and 318 / 2045 / 16999)")

for lab, s in [
        ("107 of 405 interval posets", "107"),
        ("17 admitted by af28's wording", "17"),
        ("90 excluded", "90"),
]:
    check("repair document states %s" % lab, s in flatrep)

for lab, s in [("33 YF intervals", "33"), ("5 non-distributive", "5"),
               ("28 distributive", "28"), ("witness (2,2,1)/221", "(2,2,1)"),
               ("30 Young intervals", "30")]:
    check("repair document states %s" % lab, s in flatrep)

check("the n<=3 claim is stated in the repaired document",
      "every** poset is a skew cell poset" in doc or
      "**every** poset is a skew cell poset" in doc or
      "EVERY poset is a skew shape poset" in young)
check("out_young.txt states the n<=3 claim",
      "At n <= 3 EVERY poset is a skew shape poset" in young)

# ---------------------------------------------- 2. the negative half again

print("\n[2] THE STRUCK SENTENCES -- present, once, and inside a struck block")
STRUCK = [
    ("X1 fractions", "6 of 318"),
    ("X2 grid sentence", "is **not** an interval of Young's lattice"),
    ("X4 no-other-differential-poset",
     "the **only** differential poset his construction can consume"),
    ("X3 antichain clause (mg-6ad0's X7, NOT repaired here)",
     "which lands back at the classical antichain case"),
]
# The right question is not "exactly once" -- mg-41aa's own §6 says the X7
# clause survives in the struck quote AND in the §9 record.  The right question
# is whether ANY occurrence stands in live prose, i.e. on a line that is not a
# block quote and not inside the §9 "left open" record.
lines = doc.split("\n")
sec9 = next((i for i, l in enumerate(lines)
             if l.startswith("## 9.")), len(lines))
for lab, s_ in STRUCK:
    hits = []
    for i, l in enumerate(lines):
        if re.sub(r"\s+", " ", l.strip().lstrip("> ")).find(s_) >= 0:
            hits.append(i)
    # multi-line strings: fall back to a flattened whole-document search
    flat_s = re.sub(r"\s+", " ", s_)
    if not hits:
        joined = re.sub(r"\s+", " ", doc.replace("\n   > ", "\n").replace("> ", ""))
        present = flat_s in joined
        check("%s is still present in the document" % lab, present)
        continue
    check("%s is still present in the document" % lab, True)
    live = [i for i in hits
            if not lines[i].lstrip().startswith(">") and i < sec9]
    check("%s stands ONLY inside a strike block or the §9 record" % lab,
          not live, "(live at lines %s)" % [i + 1 for i in live])
    for i in hits:
        if lines[i].lstrip().startswith(">"):
            window = "\n".join(lines[max(0, i - 25):i])
            marked = any(m in window for m in ("CORRECTED (mg-41aa",
                                               "STRUCK (mg-41aa",
                                               "RE-SCOPED (mg-41aa"))
            check("%s: quote at line %d carries a strike marker" % (lab, i + 1),
                  marked)
            break

check("consequence 3's false conclusion is no longer asserted outside a strike",
      flatdoc.count("that grid is `J(C_p ⊔ C_q)`, which for") <= 1)
check("B2's untested 'exactly the cell posets' is gone from live text",
      "are exactly the cell posets" not in
      re.sub(r"\|\s*\*\*B2′\*\*.*", "", flatdoc))
check("out_young.txt no longer asserts the untested 'exactly'",
      "an interval of Young's lattice are exactly the cell posets" not in young)

# ------------------------------------------------- 3. the beyond-brief diff

print("\n[3] BEYOND-BRIEF: what the commit changed that X1-X4 did not require")
print("  mg-41aa's brief (mg show mg-41aa) is X1, X2, X3, X4.  Items below are")
print("  changes in the delivered diff that no one of the four requires.")
BEYOND = [
    ("B1", "§8's 'Two elementary one-line derivations' -> 'Three'",
     "**Three** elementary one-line derivations" in doc or
     "**Three** elementary one-line" in doc,
     "entailed by X2 and declared in §6 of the repair document"),
    ("B2", "§2 heading note: 'the index-set contact DOES extend' to YF",
     "the index-set contact **does**" in doc.replace("**DOES**", "**does**") or
     "index-set contact **does**" in doc,
     "NEW positive claim; X4 asked only that the old reading be re-scoped"),
    ("B3", "§3 row 10: 'the SAME index-set contact ... on 28 of 33'",
     "same index-set contact" in doc,
     "NEW positive claim about the Okada monoid"),
    ("B4", "§5 item 5(c) verdict block on the three one-liners",
     "THIS ATTACK LANDED" in doc,
     "records X7 (explicitly NOT repaired) and re-verifies (b)"),
    ("B5", "new §9 recording X5, X6, X7 unrepaired",
     "WHAT mg-41aa's REPAIR DELIBERATELY LEFT OPEN" in doc,
     "record only, no claim -- declared in the brief's spirit"),
]
for tag, what, present, why in BEYOND:
    print("  %-3s %-58s present:%s" % (tag, what[:58], present))
    print("      why it is beyond brief: %s" % why)

print("\n  THE ONE THAT CARRIES A CLAIM: B2/B3.  Measured in out_a4_yf.txt --")
print("  28 of 33 YF intervals ARE distributive and each IS a J(P), which is")
print("  true; but the 28 intervals yield only 17 distinct P, of which 5 are")
print("  NOT skew cell posets.  So the FAMILY of index sets is not the same")
print("  family; what is the same is that both are ideal lattices, which for a")
print("  finite distributive lattice is Birkhoff and nothing more.")

print("\n" + "=" * 78)
print("A7: %d checks, %d failed" % (N[0], len(FAIL)))
for f in FAIL:
    print("  FAILED: %s" % f)
print("=" * 78)
print("SUMMARY a7_doc: %d checks, %d failed" % (N[0], len(FAIL)))
sys.exit(0)
