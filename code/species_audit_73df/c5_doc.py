"""C5 -- THE SEAM: do mg-6f61's edits and mg-f8fa's edits agree with each
other, and do the document's numbers agree with the committed outputs?

Two workers edited one document.  Each ticket's brief covers its own edits.
Nobody's brief covers the SEAM, and this file is aimed at it.

  C5a  DUPLICATE PASSAGES.  A general detector, not a hard-coded one: every
       block quote in the document is compared with every other, and any pair
       above a similarity threshold is reported.  Two independent passes over
       one file is the classic way to end up saying the same thing twice in
       two versions that do not agree.
  C5b  the stale cross-reference the second pass created.
  C5c  the survivals BOTH ways: what the repair had to keep, and what it had
       to not soften.  A repair is a defect in either direction.
  C5d  the document's load-bearing numbers against the committed outputs
       they are cited to -- every one located in the file that produced it.
"""

import difflib
import os
import re
import sys

from kern73df import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
DOC = os.path.join(REPO, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
TEXT = open(DOC, encoding="utf-8").read()
LINES = TEXT.splitlines()


def norm(s):
    s = re.sub(r"[*`~>|#]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


# ---------------------------------------------------------------------------
hdr("C5a  DUPLICATE PASSAGES -- every block quote against every other")

blocks, cur, start = [], [], None
for i, ln in enumerate(LINES):
    if ln.startswith(">"):
        if start is None:
            start = i + 1
        cur.append(ln)
    else:
        if cur:
            blocks.append((start, i, "\n".join(cur)))
        cur, start = [], None
if cur:
    blocks.append((start, len(LINES), "\n".join(cur)))

big = [(a, b, t) for (a, b, t) in blocks if len(norm(t)) > 300]
print("  %d block quotes in the document, %d of them longer than 300"
      % (len(blocks), len(big)))
print("  characters and therefore comparable.")
print()
dups = []
for i in range(len(big)):
    for j in range(i + 1, len(big)):
        r = difflib.SequenceMatcher(None, norm(big[i][2]),
                                    norm(big[j][2])).ratio()
        if r > 0.55:
            dups.append((r, big[i], big[j]))
for r, x, y in sorted(dups, reverse=True):
    print("  *** NEAR-DUPLICATE  %.0f%% similar" % (100 * r))
    print("      lines %d-%d and lines %d-%d" % (x[0], x[1], y[0], y[1]))
    print()
    sm = difflib.SequenceMatcher(None, norm(x[2]).split(), norm(y[2]).split())
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        a = " ".join(norm(x[2]).split()[i1:i2])
        b = " ".join(norm(y[2]).split()[j1:j2])
        if a.strip():
            print("      first  only: %s" % a[:160])
        if b.strip():
            print("      second only: %s" % b[:160])
    print()
bad += len(dups)
if not dups:
    print("  no near-duplicate block quotes.")
    print()

# ---------------------------------------------------------------------------
hdr("C5b  cross-references that the SECOND pass left stale")

checks = []

# The banner's own item count, and how a later section refers back to it.
banner_n = re.search(r"(Eight|Seven|Six|Five) things changed", TEXT)
back_ref = re.findall(r"the (five|six|seven|eight) items in the banner", TEXT)
checks.append(("the banner announces its own item count",
               bool(banner_n),
               "'%s things changed'" % (banner_n.group(1) if banner_n
                                        else "-")))
for w in back_ref:
    checks.append(("14's back-reference to that banner agrees with it",
                   banner_n is not None and w.lower() == banner_n.group(1).lower(),
                   "back-reference says '%s', banner says '%s'"
                   % (w, banner_n.group(1) if banner_n else "-")))

# "a second, shelved filing" vs 14.3, which is that filing's own record.
shelved = "shelved filing" in TEXT
has143 = "14.3 The eighth defect was found" in TEXT
checks.append(("the second filing is not described as SHELVED while 14.3"
               " records it as executed", not (shelved and has143),
               "both present" if (shelved and has143) else "consistent"))

# "an eighth defect, IF there is one" after 14.3 says it was found.
iffy = re.findall(r"an eighth defect, if (?:there is one|one exists)",
                  TEXT, re.I)
checks.append(("no passage still says 'an eighth defect, IF there is one'"
               " after 14.3 reports it found", not iffy,
               "%d such passage(s)" % len(iffy)))

# An instrument's docstring is part of what a successor reads.  Two of them
# disagree with the runs they describe.
_r2 = open(os.path.join(REPO, "code", "species_repair_6f61",
                        "r2_columns.py"), encoding="utf-8").read()
_r2o = open(os.path.join(REPO, "code", "species_repair_6f61",
                         "out_r2_columns.txt"), encoding="utf-8").read()
_d = re.search(r"predicted-vs-actual for all (\d+) cells", _r2)
_o = re.search(r"(\d+) cells, every one of them predicted", _r2o)
checks.append(("r2_columns.py's docstring cell count matches its own output",
               bool(_d) and bool(_o) and _d.group(1) == _o.group(1),
               "docstring says %s cells, the run prints %s"
               % (_d.group(1) if _d else "?", _o.group(1) if _o else "?")))

for label, ok, detail in checks:
    bad += (not ok)
    print("  %-64s %s" % (label, "ok" if ok else "*** NO ***"))
    print("      %s" % detail)
print()

# ---------------------------------------------------------------------------
hdr("C5c  WHAT HAD TO SURVIVE, AND WHAT HAD TO NOT BE SOFTENED")

MUST_SURVIVE = [
    ("control (ii)'s conclusion is explicitly NOT withdrawn",
     r"NOT withdrawn|is not withdrawn|SURVIVES THE"),
    ("the band product is still invisible to the Hopf structure",
     r"band product is invisible to the Hopf structure"),
    ("the headline is still a THEOREM, not a measurement",
     r"IT IS A THEOREM, NOT ONLY A MEASUREMENT"),
    ("2.3 has no n dependence", r"no `n` dependence"),
    ("the poset half is 87 of 87 with NO cap", r"87 of 87 classes"),
    ("and 179 of 179 out of sample", r"179 of 179"),
    ("the S_n half is NOT independently verified",
     r"NOT INDEPENDENTLY VERIFIED|NOT VERIFIED HERE"),
    ("Solomon is named as unread", r"Solomon"),
    ("Garsia-Reutenauer / Atkinson is named as unread",
     r"Garsia.Reutenauer"),
    ("the Fock statement is LOCATED, not re-derived",
     r"[Ll]ocated, not verified|LOCATED, not re-derived|quoted,\s*\n?\s*not"
     r" re-derived"),
    ("being located is stated to be a REAL result",
     r"[Bb]eing located is a real result"),
    ("the successor literature search is cancelled",
     r"DO NOT FILE THE SUCCESSOR LITERATURE SEARCH"),
    ("and its errand withdrawn where it was written",
     r"THIS ITEM IS CLOSED AND ITS ERRAND IS WITHDRAWN"),
    ("T3d is reported as TWO statements, not four",
     r"TWO STATEMENTS, EACH COMPUTED\s*\n?>?\s*TWICE|two statements each"
     r" computed twice|TWO statements each computed"),
    ("control (ii)'s 1 442 are the 1 442 disjoint-ground-set pairs",
     r"1 442 of 11 301|1 442 disjoint-ground-set"),
]

# A withdrawn sentence is allowed to survive INSIDE the strike that replaces
# it -- that is check_doc.py's rule and this document keeps it.  So the test
# is not "the string is absent" but "every occurrence of it lies inside a
# ~~...~~ span".  Testing absence instead reports the repair's own strikes as
# defects, which is what a first version of this file did.
STRIKES = [(m.start(), m.end())
           for m in re.finditer(r"~~.+?~~", TEXT, re.S)]


REPAIR_ID = re.compile(r"mg-6f61|mg-f8fa|mg-a61f", re.I)


def struck(pos):
    """Inside a strike, OR inside a passage that names the repair.

    The document's convention is that a corrected sentence may be QUOTED
    where the correction is being described -- section 0's banner does
    exactly that for five of the eight.  Testing only for the strike marks
    the banner as a defect, which is the second false positive this file
    produced against itself.
    """
    if any(a <= pos < b for a, b in STRIKES):
        return True
    ln = TEXT.count("\n", 0, pos)
    lo = hi = ln
    while lo > 0 and LINES[lo - 1].strip():
        lo -= 1
    while hi + 1 < len(LINES) and LINES[hi + 1].strip():
        hi += 1
    return bool(REPAIR_ID.search("\n".join(LINES[lo:hi + 1])))


MUST_ONLY_SURVIVE_STRUCK = [
    ("2.3 re-hedged as 'measured, not proved'", r"measured, not proved"),
    ("2.3 re-described as not located in that generality",
     r"not located.{0,60}in that generality"),
    ("'three of the four columns are the control'",
     r"[Tt]hree of the four columns are the control"),
    ("'fires hard' as the reading of control (ii)", r"fires hard"),
    ("the smallest witness given as \\{a<c, b<d\\}",
     r"Smallest witness with"),
]

for label, pat in MUST_SURVIVE:
    ok = bool(re.search(pat, TEXT))
    bad += (not ok)
    print("  survives  %-60s %s" % (label, "ok" if ok else "*** MISSING ***"))
print()
for label, pat in MUST_ONLY_SURVIVE_STRUCK:
    hits = [m.start() for m in re.finditer(pat, TEXT)]
    loose = [h for h in hits if not struck(h)]
    ok = bool(hits) and not loose
    bad += (not ok)
    print("  struck    %-60s %s"
          % (label, "ok (%d, all inside a strike)" % len(hits) if ok
             else ("*** %d OCCURRENCE(S) NOT INSIDE A STRIKE ***" % len(loose)
                   if loose else "*** NOT PRESENT AT ALL ***")))
print()
print("  Both directions are checked, because after a BROKEN finding the")
print("  comfortable error is retreating too far: a hedge reinstated by the")
print("  second pass over a claim the first pass strengthened would be a")
print("  defect, and it would look like caution.")
print()

# ---------------------------------------------------------------------------
hdr("C5d  the document's numbers against the outputs they are cited to")

CITES = [
    ("4 399", "code/species_7d75/out_t5_hopf_monoid.txt", "4399"),
    ("2 685", "code/species_7d75/out_t5_hopf_monoid.txt", "2685"),
    ("216", "code/species_repair_6f61/out_r2_columns.txt", "216"),
    ("6 988", "code/species_repair_6f61/out_r2_columns.txt", "6988"),
    ("396", "code/species_repair_6f61/out_r2_columns.txt", "396"),
    ("12 186", "code/species_repair_6f61/out_r2_columns.txt", "12186"),
    ("12 192", "code/species_repair_6f61/out_r2_columns.txt", "12192"),
    ("266 459", "code/species_repair_6f61/out_r2_columns.txt", "266459"),
    ("3 408", "code/species_repair_6f61/out_r2_columns.txt", "3408"),
    ("16 425", "code/species_repair_6f61/out_r2_columns.txt", "16425"),
    ("75 512", "code/species_7d75/out_t5_hopf_monoid.txt", "75512"),
    ("22 614", "code/species_7d75/out_t6_fock_and_record.txt", "22614"),
    ("529", "code/species_7d75/out_t6_fock_and_record.txt", "529"),
    ("1 442", "code/species_remainder_f8fa/out_w2_typemismatch.txt", "1442"),
    ("11 301", "code/species_remainder_f8fa/out_w2_typemismatch.txt", "11301"),
    ("11 300", "code/species_remainder_f8fa/out_w2_typemismatch.txt", "11300"),
    ("472", "code/species_7d75/out_t3_bidigare.txt", "472"),
    ("170", "code/species_7d75/out_t3_bidigare.txt", "170"),
    ("174", "code/species_repair_6f61/out_r1_smallest.txt", "174"),
    ("12 problems", "code/species_remainder_f8fa/out_w3_scope_before.txt",
     "12 problem"),
    ("eight of them", "code/species_remainder_f8fa/out_w3_scope.txt",
     "8 occurrence"),
    ("759 assertions", "code/species_7d75/out_selftest.txt", "759"),
    ("2 114 assertions", "code/species_remainder_f8fa/out_selftest.txt",
     "2114"),
    ("45 predicted cells", "code/species_repair_6f61/out_r2_columns.txt",
     "of 45"),
]

miss = 0
for shown, path, token in CITES:
    full = os.path.join(REPO, path)
    body = open(full, encoding="utf-8").read() if os.path.exists(full) else ""
    in_doc = (shown in TEXT) or (shown.replace(" ", "") in TEXT) \
        or (shown.replace(" ", " ") in TEXT)
    in_out = token in body
    ok = in_doc and in_out
    miss += (not ok)
    print("  %-18s doc %-3s  %-52s %s"
          % (shown, "yes" if in_doc else "NO", path,
             "ok" if ok else "*** NOT IN THAT OUTPUT ***"))
bad += miss
print()
print("  %d of %d cited figures located in the output they are cited to."
      % (len(CITES) - miss, len(CITES)))
print()

print("=" * 78)
print("C5 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
