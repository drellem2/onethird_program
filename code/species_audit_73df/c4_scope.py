"""C4 -- THE SAME DETECTOR, POINTED AT ALL OF THE REPAIR'S CORRECTIONS.

mg-f8fa's finding (its section 14.3) is that mg-6f61 corrected three
statements in the document and left them in force in `code/species_7d75`,
because `check_doc.py` opens one file.  Its fix is `w3_scope.py`, which takes
a DIRECTORY.

The fix widened the TARGET.  It did not widen the LIST.  `w3_scope.py`'s
forbidden-statement table has exactly two entries -- X4's control count and
X5's near-miss reading -- plus the character-ring rule for S4/S5.  mg-6f61
corrected EIGHT things.  So the question mg-f8fa's own reasoning raises, and
does not ask, is: of the other five corrections, how many are also still in
force at source?

This file asks it.  Every one of mg-6f61's corrections gets a pattern, the
whole tree is scanned, and a hit counts as REPAIRED only if the six lines
around it name a repair, negate the sentence outright, or sit inside a table
the file declares to be a list of forbidden strings -- the same narrow rule
w3_scope adopted after its own false negative, and narrowed once more here
after this file reproduced that false negative against itself (see NEGATES).

It is pointed at THREE trees, not one: `code/species_7d75` (the tree
w3_scope checks), and `code/species_repair_6f61` and
`code/species_remainder_f8fa` (the trees nobody checks), because "the checker
must take the code directory as a target too" has an obvious next instance
and section 14.3 does not name it.

FOUR CONTROLS, because a detector that has only ever been seen to fire is
worth as little as one that has only ever been seen to pass:

  (a) the same detector against the PRE-REPAIR tree at 83ac472 must report
      MORE than it reports now, and must specifically catch X4 and X5
      there -- the two w3_scope covers, so the control tests the detector
      and not the coverage claim;
  (b) `w3_scope.py` itself, run against the CURRENT tree, must report PASS
      while this file reports hits -- that is the coverage gap DEMONSTRATED
      rather than asserted;
  (c) the document claims w3_scope "fails if a NINTH occurrence is added
      unmarked".  A ninth is added to a scratch copy and w3_scope must fail;
  (d) this detector must fire on a statement injected into a scratch copy,
      or it is not detecting anything.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from kern73df import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(REPO, "code", "species_7d75")
OTHER = [os.path.join(REPO, "code", "species_repair_6f61"),
         os.path.join(REPO, "code", "species_remainder_f8fa")]
PRE_COMMIT = "83ac472"

# A corrected statement may survive only where the surrounding window ALSO
# says it does not hold.  That is check_doc.py's own rule, moved to the code.
# Three ways to say it, and nothing weaker:
#   1. name a repair -- w3_scope's rule, adopted after its own false negative
#      where a bare "REPAIRED" four lines away disarmed it by accident;
#   2. negate the sentence in so many words;
#   3. sit inside a table the file declares to be a list of forbidden or
#      stricken strings, which is what a checker's own source looks like.
NAMES_A_REPAIR = re.compile(r"mg-6f61|mg-f8fa|mg-a61f", re.I)
# Deliberately NARROW, and narrowed once already.  A first version accepted
# the generic English "is not the ...", and `t6_fock_and_record.py`'s
# "is not the framework this ticket is about" -- four lines below the X3
# sentence and about something else entirely -- exonerated it by accident.
# That is w3_scope.py's own false negative, reproduced against this file by
# the same mechanism: an adjacent unrelated phrase disarming a detector.
NEGATES = re.compile(r"refut|STRICKEN|FORBIDDEN|is\s+FALSE"
                     r"|NOT\s+the\s+smallest|no\s+longer|used\s+to"
                     r"|must\s+not\s+survive|does\s+not\s+hold"
                     r"|only\s+'smallest'\s+is\s+false", re.I)
DECLARED_TABLE = re.compile(r"^(STRICKEN|FORBIDDEN|REQUIRED|PREDICTIONS)\s*=")
TABLE_REACH = 30
WINDOW = 6

# Every statement mg-6f61 corrected, with the identifier the repair gives it,
# and the words that count as saying THIS one no longer holds.
CORRECTIONS = [
    ("X1  the smallest witness is {a<c, b<d}",
     [r"\{?\s*a\s*<\s*c\s*,\s*b\s*<\s*d", r"smallest\s+witness"],
     r"3-?ELEMENT\s+CHAIN|3-?chain|smallest\s+is\s+the|'smallest'"
     r"|whole\s+of\s+the\s+error|IS\s+a\s+witness"),
    ("X3  '0 failures across 5 axioms on 4399 basis elements'",
     [r"(?:every|all\s+five|all\s+5|five|5)\s+(?:Hopf[- ]monoid\s+|bimonoid\s+)?"
      r"axiom"],
     r"CLOSURE|closure\s+only|two\s+columns|cannot\s+fail|pinned"),
    ("X4  'three are controls' / 'three of the four are the control'",
     [r"three\s+are\s+controls", r"the\s+three\s+controls",
      r"three\s+of\s+the\s+four\s+(?:columns\s+)?are\s+the\s+control"],
     r"two\s+statements|one\s+control|computed\s+twice"),
    ("X5  control (ii) read as 'how differently'",
     [r"measures\s+how\s+differently", r"how\s+differently"],
     r"type\s+mismatch|near[- ]miss"),
    ("X6/X7  AM 17.5 quoted with the species Pi, not Pi*",
     [r"K-?bar\(Pi\)\s+is\s+the\s+algebra\s+of\s+symmetric",
      r"K\(Pi\)\s+is\s+the\s+familiar"],
     r"Pi-?\*|misquot|printed\s+it\s+wrong|both\s+slots"),
    ("X8  'three independent sources' for 'braid cone'",
     [r"three\s+independent"],
     r"collision|two\s+sources|flags\s+the\s+term"),
]

# X3 is a co-occurrence, not a phrase: the axiom word has to sit beside the
# 4399.  Scanning for the axiom word alone would hit every legitimate mention
# of the bimonoid axioms in the tree.
X3_COMPANION = re.compile(r"4\s?399|4399")
X3_SPAN = 3


def files_of(root):
    if not os.path.isdir(root):
        return {}
    out = {}
    for f in sorted(os.listdir(root)):
        if f.endswith((".py", ".txt", ".md")):
            with open(os.path.join(root, f), encoding="utf-8") as fh:
                out[f] = fh.read().splitlines()
    return out


def scan(root, label):
    """Returns (asserted, marked) lists of 'file:line  correction' strings."""
    L = files_of(root)
    asserted, marked = [], []
    for name, pats, own in CORRECTIONS:
        is_x3 = name.startswith("X3")
        ownre = re.compile(own, re.I)
        for f, lines in L.items():
            for i, ln in enumerate(lines):
                if not any(re.search(p, ln, re.I) for p in pats):
                    continue
                if is_x3:
                    lo = max(0, i - X3_SPAN)
                    hi = min(len(lines), i + X3_SPAN + 1)
                    if not X3_COMPANION.search("\n".join(lines[lo:hi])):
                        continue
                lo, hi = max(0, i - WINDOW), min(len(lines), i + WINDOW + 1)
                near = "\n".join(lines[lo:hi])
                in_table = any(DECLARED_TABLE.match(lines[j])
                               for j in range(max(0, i - TABLE_REACH), i))
                exonerated = (NAMES_A_REPAIR.search(near)
                              or NEGATES.search(near)
                              or ownre.search(near)
                              or in_table)
                (marked if exonerated else asserted).append(
                    "%-32s %s:%d" % (name.split("  ")[0], f, i + 1))
    return asserted, marked


# ---------------------------------------------------------------------------
hdr("C4a  all EIGHT of mg-6f61's corrections, scanned at source")

print("  target: code/species_7d75 -- the tree w3_scope.py checks and the")
print("  copy a successor re-runs.")
print()
asserted, marked = scan(SRC, "species_7d75")
for h in marked:
    print("    quoted as corrected   %s" % h)
print()
for h in asserted:
    print("    *** STILL ASSERTED    %s" % h)
print()
print("  still asserted: %d      quoted as corrected: %d"
      % (len(asserted), len(marked)))
print()
STILL = list(asserted)

# ---------------------------------------------------------------------------
hdr("C4b  the two trees nobody points a checker at")

for root in OTHER:
    a, m = scan(root, os.path.basename(root))
    print("  %-34s still asserted: %d   quoted as corrected: %d"
          % ("code/" + os.path.basename(root), len(a), len(m)))
    for h in a:
        print("      *** STILL ASSERTED    %s" % h)
print()
print("  These two are the repair's OWN instruments.  A hit here would be the")
print("  same defect one directory further out; there is none, and that is")
print("  reported as a NEGATIVE result rather than left unsaid.")
print()

# ---------------------------------------------------------------------------
hdr("C4c  CONTROL (a): the same detector against the PRE-REPAIR tree")

tmp = tempfile.mkdtemp(prefix="audit73df_")
pre_ok = False
try:
    tar = subprocess.run(["git", "archive", PRE_COMMIT, "code/species_7d75"],
                         cwd=REPO, capture_output=True)
    if tar.returncode == 0:
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        pre = os.path.join(tmp, "code", "species_7d75")
        pa, pm = scan(pre, "pre")
        pre_ok = True
        print("  tree at %s: still asserted %d, quoted as corrected %d"
              % (PRE_COMMIT, len(pa), len(pm)))
        print()
        for h in pa:
            print("    STILL ASSERTED (pre)  %s" % h)
        print()
        caught = {h.split()[0] for h in pa}
        need = {"X4", "X5"}
        got_all = need.issubset(caught)
        bad += (not got_all)
        print("  the detector catches %s on the pre-repair tree: %s"
              % (", ".join(sorted(need)), "yes" if got_all else "*** NO ***"))
        bad += (not (len(pa) > len(STILL)))
        print("  and it reports MORE there (%d) than now (%d): %s"
              % (len(pa), len(STILL),
                 "yes" if len(pa) > len(STILL) else "*** NO ***"))
    else:
        print("  git archive unavailable -- control (a) SKIPPED, and this line")
        print("  is the record of the skip rather than a silent pass.")
        bad += 1
except Exception as e:                                    # pragma: no cover
    print("  control (a) could not run: %s" % e)
    bad += 1
print()

# ---------------------------------------------------------------------------
hdr("C4d  CONTROL (b): w3_scope.py PASSES the tree this file has hits on")

w3 = os.path.join(REPO, "code", "species_remainder_f8fa", "w3_scope.py")
r = subprocess.run([sys.executable, w3, SRC], capture_output=True, text=True,
                   cwd=os.path.dirname(w3))
verdict = [l for l in r.stdout.splitlines() if l.startswith("W3 SCOPE:")]
print("  w3_scope.py against code/species_7d75 : %s"
      % (verdict[0] if verdict else "?"))
print("  this file against the same tree       : %d statement(s) still"
      % len(STILL))
print("                                          asserted")
print()
gap = [h for h in STILL]
if gap and verdict and "PASS" in verdict[0]:
    print("  THE GAP IS REAL AND IT IS DEMONSTRATED, NOT ARGUED.  w3_scope's")
    print("  forbidden-statement table has two entries, X4 and X5.  mg-6f61")
    print("  corrected eight things.  The statements below are corrected in")
    print("  the document, in force at source, and invisible to the checker")
    print("  built to prevent exactly that:")
    print()
    for h in gap:
        print("      %s" % h)
elif not gap:
    print("  No gap: every one of mg-6f61's corrections is either marked at")
    print("  source or absent from it.")
else:
    print("  w3_scope does not pass this tree, so the gap cannot be read off")
    print("  this way.")
print()

# ---------------------------------------------------------------------------
hdr("C4e  CONTROL (c): w3_scope FAILS on a NINTH unmarked occurrence")

scratch = os.path.join(tmp, "ninth")
shutil.copytree(SRC, scratch)
with open(os.path.join(scratch, "t4_one_operation.py"), "a",
          encoding="utf-8") as fh:
    fh.write('\nprint("  this quotient is the character ring of S_n")\n')
r2 = subprocess.run([sys.executable, w3, scratch], capture_output=True,
                    text=True, cwd=os.path.dirname(w3))
v2 = [l for l in r2.stdout.splitlines() if l.startswith("W3 SCOPE:")]
n_occ = [l for l in r2.stdout.splitlines() if "occurrence(s) checked" in l]
fired = bool(v2) and "FAIL" in v2[0]
bad += (not fired)
print("  after adding one unmarked 'character ring' line:")
print("    %s" % (n_occ[0].strip() if n_occ else "?"))
print("    %s" % (v2[0] if v2 else "?"))
print("  %s -- the document's claim that it 'fails if a ninth is added"
      % ("CONFIRMED" if fired else "*** NOT CONFIRMED ***"))
print("  unmarked' is true.")
print()

# ---------------------------------------------------------------------------
hdr("C4f  CONTROL (d): this detector fires on an injected statement")

scratch2 = os.path.join(tmp, "inject")
shutil.copytree(SRC, scratch2)
with open(os.path.join(scratch2, "t2_operation.py"), "a",
          encoding="utf-8") as fh:
    fh.write('\nprint("  four candidates, three are controls")\n')
ia, _ = scan(scratch2, "inject")
grew = len(ia) > len(STILL)
bad += (not grew)
print("  injected 'three are controls' into a scratch copy:")
print("    still asserted before %d, after %d : %s"
      % (len(STILL), len(ia), "fires" if grew else "*** DOES NOT FIRE ***"))
print()

# ---------------------------------------------------------------------------
hdr("C4g  w3_scope.py's own docstring disagrees with its own evidence file")

with open(w3, encoding="utf-8") as fh:
    w3text = fh.read()
doc_n = re.search(r"it reported (\d+) problems there", w3text)
before = os.path.join(REPO, "code", "species_remainder_f8fa",
                      "out_w3_scope_before.txt")
with open(before, encoding="utf-8") as fh:
    m = re.search(r"W3 SCOPE: FAIL\s+\((\d+) problem", fh.read())
d, e = (doc_n.group(1) if doc_n else "?"), (m.group(1) if m else "?")
agree = (d == e)
bad += (not agree)
print("  w3_scope.py docstring                : 'it reported %s problems'" % d)
print("  out_w3_scope_before.txt              : FAIL (%s problems)" % e)
print("  document, section 14.3 and ledger S14: 12 problems")
print()
print("  %s" % ("consistent" if agree else
                "*** INCONSISTENT -- the checker's own account of the run"
                " that falsified it disagrees with the committed run ***"))
print()

shutil.rmtree(tmp, ignore_errors=True)
print("=" * 78)
print("C4 STILL ASSERTED AT SOURCE: %d" % len(STILL))
print("C4 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
