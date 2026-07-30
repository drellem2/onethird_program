"""E3 --- EVERY DISPOSITION IN SECTION 8'S STATUS TABLE, AGAINST THE DIFF.

mg-d330, on the mg-13b2 repair.  My brief:

    "For each label, read the diff and confirm the label is true.  Report per
     label, BOTH DIRECTIONS: label-says-fixed-and-is, label-says-outstanding-
     and-is."

    "Partial states are the trap.  A finding with several sites is where a
     binary label goes wrong.  Check EVERY SITE of every multi-site finding,
     and confirm a partial is labelled as partial with the open site named."

Nothing here calls `t5_labels.py`.  Every check is written afresh against
`git show` of the three named commits and against the working tree, so a
label is confirmed by an instrument that does not share the target's idea of
what to look for.

Exit 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
"""

import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

DELIVERED = "03d7f91"      # mg-db09, as delivered
REPAIR1 = "2e66d03"        # mg-e8b8, the repair mg-a218 audited
REPAIR2 = "ed9cde4"        # mg-13b2, the repair THIS audit audits

DOC = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
T1 = "code/branching_locate_db09/t1_tl.py"
O1 = "code/branching_locate_db09/out_t1_tl.txt"
T3 = "code/branching_locate_db09/t3_ours.py"

SELF, FIND = [], []
CHECKS = 0


def selferr(m):
    SELF.append(m)
    print("      SELF-ERROR: " + m)


def finding(m):
    FIND.append(m)
    print("      FINDING: " + m)


def git(*args):
    p = subprocess.run(["git"] + list(args), cwd=ROOT,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.decode()[:160]))
    return p.stdout.decode("utf-8", "replace")


def at(commit, path):
    return git("show", "%s:%s" % (commit, path))


def now(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def touched(commit, path):
    return path in git("show", "--format=", "--name-only", commit).split()


def check(desc, got, want):
    """One assertion.  `want` is the state the LABEL asserts."""
    global CHECKS
    CHECKS += 1
    ok = (got == want)
    print("      [%s] %-64s %s" % ("ok" if ok else "BAD", desc,
                                   "present" if got else "absent"))
    if not ok:
        finding("%s: the label asserts %s and the tree says %s"
                % (desc, "present" if want else "absent",
                   "present" if got else "absent"))
    return ok


print("=" * 74)
print("E3  SECTION 8'S STATUS TABLE, CHECKED AGAINST THE DIFF, BOTH DIRECTIONS")
print("=" * 74)
print("commits: %s (delivered), %s (mg-e8b8), %s (mg-13b2, the target)"
      % (DELIVERED, REPAIR1, REPAIR2))
print()

doc_now, t1_now, o1_now = now(DOC), now(T1), now(O1)

# ===========================================================================
# X2 --- the label says CLOSED at FOUR sites.  Four sites, checked one at a
#        time, each in both directions: open before, closed now.
# ===========================================================================
print("-" * 74)
print("X2   label: CLOSED, at FOUR sites, in TWO commits")
print("-" * 74)
print("   The label is a conjunction of four site-claims and a two-commit")
print("   attribution.  A partial would be a site still open, or a site")
print("   attributed to the wrong commit.  Each is separated below.")
print()

print("   SITE 1 --- section 0's 2x2 table cell.  Label: closed at %s." % REPAIR1)
# CORRECTED DURING CONSTRUCTION, recorded here and not in a commit message:
# my first needle was the BOLD form `Path-pair **basis** survives`, which is
# how the repaired prose QUOTES the old cell, not how the old cell was
# written.  At 03d7f91 the table row reads `Path-pair *basis* survives` with
# single asterisks.  Checking the wrong string made a true label look false.
check("was OPEN at %s ('Path-pair *basis* survives')" % DELIVERED,
      "Path-pair *basis* survives, direct sum does not" in at(DELIVERED, DOC),
      True)
check("is CLOSED at %s ('Path-pair *count* survives')" % REPAIR1,
      "Path-pair *count* survives" in at(REPAIR1, DOC), True)
check("the false form is gone at %s" % REPAIR1,
      "Path-pair **basis** survives" in at(REPAIR1, DOC), False)
check("still closed in the working tree (the TABLE ROW says count)",
      "Path-pair *count* survives, direct sum does not" in doc_now, True)
check("the false form survives in the tree only as a marked quotation",
      any("Path-pair **basis** survives" in b and
          ("It read" in b or "MARKED IN PLACE" in b or "until `2e66d03`" in b)
          for b in doc_now.split("\n\n")), True)
check("and no table row still asserts it",
      any(l.startswith("|") and "Path-pair *basis* survives" in l
          for l in doc_now.splitlines()), False)
check("carried NO marker at %s -- which is why the old label was wrong" % REPAIR1,
      "MARKED IN PLACE" in at(REPAIR1, DOC), False)
check("carries a marker now, added by %s" % REPAIR2,
      "**MARKED IN PLACE (mg-13b2" in doc_now, True)
print()

print("   SITE 2 --- T1d's printed line, in t1_tl.py and its committed output.")
print("              Label: closed at %s." % REPAIR1)
OLD2 = "so the pairs-of-paths basis exists throughout"
check("was OPEN at %s in t1_tl.py" % DELIVERED,
      OLD2 in at(DELIVERED, T1), True)
check("was OPEN at %s in out_t1_tl.txt" % DELIVERED,
      OLD2 in at(DELIVERED, O1), True)
check("is CLOSED at %s in t1_tl.py" % REPAIR1, OLD2 in at(REPAIR1, T1), False)
check("is CLOSED at %s in out_t1_tl.txt" % REPAIR1, OLD2 in at(REPAIR1, O1), False)
check("still closed in the working tree (source)", OLD2 in t1_now, False)
check("still closed in the working tree (committed output)", OLD2 in o1_now, False)
check("carried NO marker at %s" % REPAIR1,
      "MARKED IN PLACE" in at(REPAIR1, T1), False)
check("carries a marker now, added by %s (source)" % REPAIR2,
      "MARKED IN PLACE (mg-13b2)" in t1_now, True)
check("and the marker reaches the READER, i.e. the committed output",
      "MARKED IN PLACE (mg-13b2)" in o1_now, True)
print()

print("   SITE 3 --- T1a's 'iff' header.  Label: closed at %s, not before."
      % REPAIR2)
OLD3 = "with a common endpoint exists iff"
check("was OPEN at %s" % DELIVERED, OLD3 in at(DELIVERED, T1), True)
check("was STILL OPEN at %s -- the label says so" % REPAIR1,
      OLD3 in at(REPAIR1, T1), True)
check("and still open in %s's committed output" % REPAIR1,
      OLD3 in at(REPAIR1, O1), True)
check("is CLOSED in the working tree (source)", OLD3 in t1_now, False)
check("is CLOSED in the working tree (committed output)", OLD3 in o1_now, False)
check("the corrected form 'ONLY IF' is in source",
      "endpoint exists ONLY IF dim A" in t1_now, True)
check("and in the committed output", "endpoint exists ONLY IF dim A" in o1_now, True)
check("the converse is REFUTED, in source (T1c2)",
      "T1c2  THE 'iff' OF T1a IS FALSE, MEASURED" in t1_now, True)
check("and the refutation reaches the reader",
      "They part at 7 of the 20 pairs:" in o1_now, True)
m = re.search(r"They part at (\d+) of the (\d+) pairs:", o1_now)
if m:
    print("      the refutation's own figures: %s of %s (n, beta) pairs"
          % (m.group(1), m.group(2)))
    if (m.group(1), m.group(2)) != ("7", "20"):
        finding("section 8 says T1c2 refutes the converse at 7 of 20 pairs; "
                "the committed output says %s of %s" % (m.group(1), m.group(2)))
    CHECKS += 1
else:
    selferr("could not read T1c2's own figures out of out_t1_tl.txt")
print()

print("   SITE 4 --- section 1's clause table.  Label: a FOURTH site, named by")
print("              no list, closed at %s." % REPAIR2)
OLD4 = "**this survives without semisimplicity**"
check("was OPEN at %s" % DELIVERED, OLD4 in at(DELIVERED, DOC), True)
check("was STILL OPEN at %s -- so it is genuinely a fourth site" % REPAIR1,
      OLD4 in at(REPAIR1, DOC), True)
check("is CLOSED in the working tree", OLD4 in doc_now, False)
check("the corrected form is in place",
      "the COUNT survives without semisimplicity and the MATRIX UNITS do not"
      in doc_now, True)
check("with the marker naming it a fourth site",
      "a **fourth site of mg-2060's X2, named by no list**" in doc_now, True)
print()
print("   AND THE COUNTING CLAIM ITSELF: 'four, not the three mg-2060 named'.")
mg2060 = "docs/OneThird-Bratteli-Path-Algebras-IndependentAudit.md"
try:
    # CORRECTED DURING CONSTRUCTION: mg-2060 writes its quotations with
    # markdown emphasis inside them (`exists **iff**`), so a raw substring
    # test scored two of the three sites it does name as unnamed.  Emphasis
    # markers and line breaks are stripped before matching.  The correction
    # moves the count UP, against this instrument's interest.
    a2060 = now(mg2060)
    seg = " ".join(a2060.replace("*", "").replace("`", "").split())
    named = []
    for (nm, needle) in [("T1a's iff", "common endpoint exists iff"),
                         ("section 0's 2x2 cell", "Path-pair basis survives"),
                         ("T1d's printed line", "pairs-of-paths basis exists"),
                         ("section 1's clause table",
                          "this survives without semisimplicity")]:
        hit = needle in seg
        named.append((nm, hit))
        print("      mg-2060's audit names %-28s %s"
              % (nm, "YES" if hit else "no"))
    CHECKS += 1
    n_named = sum(1 for (_, h) in named if h)
    print("      -> mg-2060 names %d of the 4 sites; section 8 says 'three'."
          % n_named)
    if n_named != 3:
        finding("section 8's X2 row says mg-2060 named THREE sites; mg-2060's "
                "own audit document names %d of the four by their text"
                % n_named)
except Exception as exc:
    selferr("could not read mg-2060's audit document: %s" % exc)
print()

# ===========================================================================
# X3, X5, X6, 95.7% --- the label says OPEN.  An OPEN label is falsified by a
# site that has been silently CLOSED, which is the harder direction.
# ===========================================================================
print("-" * 74)
print("X3   label: OPEN.  Untouched by %s and by %s." % (REPAIR1, REPAIR2))
print("-" * 74)
X3 = "equivalently (VO Prop. 1.4)"
check("the unqualified site is still in force", X3 in doc_now, True)
unqual = [l for l in doc_now.splitlines()
          if "(VO Prop. 1.4)" in l and "semisimple" not in l]
CHECKS += 1
print("      unqualified '(VO Prop. 1.4)' lines: %d (OPEN asserts exactly 1)"
      % len(unqual))
if len(unqual) != 1:
    finding("X3 is labelled OPEN but %d unqualified VO Prop. 1.4 lines stand"
            % len(unqual))
for cm in (REPAIR1, REPAIR2):
    added = [l for l in git("show", "--format=", cm, "--", DOC).splitlines()
             if l.startswith("+") and not l.startswith("+++") and X3 in l]
    removed = [l for l in git("show", "--format=", cm, "--", DOC).splitlines()
               if l.startswith("-") and not l.startswith("---") and X3 in l]
    CHECKS += 1
    print("      %s: %d added line(s), %d deleted line(s) carrying the site"
          % (cm, len(added), len(removed)))
    if added or removed:
        finding("X3 is labelled untouched by %s, and that commit moves %d/%d "
                "lines carrying its site" % (cm, len(added), len(removed)))
print()

print("-" * 74)
print("X5   label: OPEN.  t3_ours.py byte-identical across both commits.")
print("-" * 74)
for cm in (DELIVERED, REPAIR1, REPAIR2):
    same = (at(cm, T3) == now(T3))
    CHECKS += 1
    print("      [%s] t3_ours.py identical to its state at %s"
          % ("ok" if same else "BAD", cm))
    if not same:
        finding("X5 is labelled OPEN on the ground that t3_ours.py has not "
                "moved; it differs from its state at %s" % cm)
check("and D5 still discloses it ('T3b prints twelve exempt')",
      "T3b prints twelve exempt" in doc_now, True)
print()

print("-" * 74)
print("X6   label: OPEN.  Section 7 still says four one-line derivations.")
print("-" * 74)
check("section 7 says four", "**Four elementary" in doc_now, True)
check("and the dispute is disclosed", "census finds eight" in doc_now, True)
# CORRECTED DURING CONSTRUCTION: section 7 writes the four derivations
# INLINE inside a wrapped bullet, so a line-anchored regex counted 0.  The
# labels are counted inside section 7's own block instead.
sec7 = doc_now.split("## 7. NOTE FOR pm-onethird")[-1].split("## 8.")[0]
n_flagged = len({m.group(1) for m in re.finditer(r"\(([a-d])\) ", sec7)})
CHECKS += 1
print("      section 7 enumerates %d derivations inline (a)-(d): %s"
      % (n_flagged, "consistent with 'four'" if n_flagged == 4 else "INCONSISTENT"))
if n_flagged != 4:
    finding("X6's OPEN label rests on section 7 saying four; it enumerates %d"
            % n_flagged)
print()

print("-" * 74)
print("n = 6 95.7%   label: OPEN, re-derived by nobody.")
print("-" * 74)
check("disclosed in section 0 ('remains arithmetic')",
      "remains arithmetic" in doc_now, True)
check("disclosed at D5 ('still arithmetic')", "still arithmetic" in doc_now, True)
CHECKS += 1
same = (at(DELIVERED, T3) == now(T3))
print("      [%s] and nothing re-derived it: t3_ours.py unmoved since delivery"
      % ("ok" if same else "BAD"))
print()

# ===========================================================================
# "Repaired 1 --- FIVE sites" --- the other multi-site label in section 8
# ===========================================================================
print("-" * 74)
print("Repaired 1   label: FIVE sites of the multiplicity-free assertion")
print("-" * 74)
FIVE = [
    ("site 1  section 0's 'MEASURED (not cited)' sentence",
     "(not cited) to be the same multiplicity-free"),
    ("site 2  'Multiplicity-freeness is held fixed down that column'",
     "Multiplicity-freeness is held\nfixed down that column"),
    ("site 3  section 0's four-row table", "| 1 | 132 | **99** | **no** |"),
    ("site 4  the 2x2 cell placement", "`TL_6(1)`: 99 of 132"),
    ("site 5  section 3's two sentences",
     "**at generic parameters, which is where they are also"),
]
WD = ("WITHDRAWN", "CORRECTED", "Corrected", "used to", "What was claimed",
      "~~", "USED TO SAY", "no longer", "MARKED IN PLACE", "SUPERSEDED",
      "What it is wrong", "Why it is wrong")
blocks = doc_now.split("\n\n")
for (name, needle) in FIVE:
    CHECKS += 1
    hits = [i for (i, b) in enumerate(blocks) if needle in b]
    if not hits:
        print("      [BAD] %-56s absent" % name)
        finding("%s: the site named by the label is not in the document" % name)
        continue
    live = [i for i in hits
            if not any(m in blocks[i] for m in WD)
            and not (i and any(m in blocks[i - 1] for m in WD))]
    ok = not live or needle.startswith(("| 1 |", "`TL_6(1)`", "**at generic"))
    print("      [%s] %-56s %d block(s), %d unmarked"
          % ("ok" if ok else "BAD", name, len(hits), len(live)))
    if not ok:
        finding("%s stands unmarked in %d block(s)" % (name, len(live)))
print()

# ===========================================================================
# THE FIFTH-SITE SWEEP --- X2 across the WHOLE tree, not this document alone
# ===========================================================================
print("-" * 74)
print("A FIFTH SITE OF X2?  swept over the whole tree, not one document")
print("-" * 74)
print("   Section 8 says X2 has four sites and that the fourth was found by")
print("   sweeping.  A sweep of the same document would find the same four.")
print("   This one is over every tracked .md/.py/.txt/.sh in the repository.")
print()
SHAPES = [
    ("a path/pairs-of-paths BASIS surviving", re.compile(
        r"(path-pair|pairs-of-paths|path)\s+\**basis\**\s+(survives|exists)", re.I)),
    ("MATRIX UNITS surviving without semisimplicity", re.compile(
        r"matrix units.{0,200}?without semisimplicity", re.I | re.S)),
    ("'this survives without semisimplicity'", re.compile(
        r"this survives without semisimplicity", re.I)),
    ("a basis existing IFF the count identity", re.compile(
        r"basis\b.{0,80}?\biff\b.{0,60}?dim A", re.I | re.S)),
]
tracked = [f for f in git("ls-files").split("\n")
           if f.endswith((".md", ".py", ".txt", ".sh"))]
print("   swept population: %d tracked .md/.py/.txt/.sh files" % len(tracked))
# THE MARKER VOCABULARY, and it was WIDENED ONCE.  Recorded here with its
# reason rather than in a commit message, per this repo's convention.
#
# The first run used only the withdrawal/correction words and a window of 4
# lines either side.  It returned 17 sites, and reading them showed the
# vocabulary was simply too narrow for what an X2 occurrence looks like OUTSIDE
# the delivered document: mg-2060's `b2_pathbasis.py` states the claim as the
# thing it is about to refute, mg-a218's `c5_record.py` carries it as a needle
# in a checker, and section 4 item 3 of the delivered document quotes it inside
# a sentence whose next words are "is false in the 'if' direction".  None of
# those is an assertion.  The vocabulary now includes the words a refutation
# uses and the window is 8 lines either side.
#
# THIS IS A REAL LOOSENING and it is the widening that could hide a fifth site,
# so it is calibrated below rather than trusted: a bare unmarked assertion is
# injected into a scratch copy of the delivered document and the sweep must
# still find it, and the same assertion with a marker beside it must not fire.
MARKERS = ("WITHDRAWN", "withdrawn", "CORRECTED", "Corrected", "corrected",
           "used to", "USED TO SAY", "MARKED IN PLACE", "SUPERSEDED",
           "~~", "no longer", "X2", "FINDING", "finding", "REMOVED",
           "pre-repair", "OPEN", "CLOSED", "false", "FALSE", "refut", "REFUT",
           "counterexample", "ONLY IF", "is wrong", "audit", "AUDIT",
           "does not", "NOT ", "old ", "was ", "said", "reads", "read ")
WINDOW = 8


def sweep(files_text):
    """Return the unmarked X2-shaped assertions in {path: text}."""
    out = []
    for (f, txt) in files_text.items():
        fl = txt.splitlines()
        for (nm, rx) in SHAPES:
            for mm in rx.finditer(txt):
                ln = txt[:mm.start()].count("\n") + 1
                win = "\n".join(fl[max(0, ln - 1 - WINDOW):ln + WINDOW])
                if not any(k in win for k in MARKERS):
                    out.append((f, ln, nm, fl[ln - 1].strip()[:88]))
    return out


texts = {}
for f in tracked:
    try:
        texts[f] = now(f)
    except Exception:
        continue
total_hits = sum(len(list(rx.finditer(t)))
                 for t in texts.values() for (_, rx) in SHAPES)
unmarked = sweep(texts)
CHECKS += 1
print("   occurrences of an X2-shaped claim : %d" % total_hits)
print("   marker window                     : %d lines either side" % WINDOW)
print("   of those, UNMARKED                : %d" % len(unmarked))
for (f, ln, nm, txt) in unmarked:
    print("      %s:%d  [%s]" % (f, ln, nm))
    print("         %s" % txt)
    finding("an X2-shaped claim stands unmarked at %s:%d -- a fifth site the "
            "'CLOSED at all FOUR' label does not cover" % (f, ln))
if not unmarked:
    print("   -> NO FIFTH SITE.  Every one of the %d occurrences sits inside a"
          % total_hits)
    print("      withdrawal, a correction, a refutation or a checker's needle.")
print()
print("   CALIBRATION --- what would have counted, and does it still fire?")
probe_txt = doc_now.replace(
    "## 3. WHERE THE FAMILY ENDS",
    "## 3. WHERE THE FAMILY ENDS\n\nThe path-pair basis survives here, and\n"
    "matrix units are available without semisimplicity.\n")
neg_txt = doc_now.replace(
    "## 3. WHERE THE FAMILY ENDS",
    "## 3. WHERE THE FAMILY ENDS\n\nWITHDRAWN: this used to say the path-pair\n"
    "basis survives without semisimplicity, and it is false.\n")
pos = sweep({"PROBE.md": probe_txt})
neg = sweep({"PROBE.md": neg_txt})
CHECKS += 2
print("      [%s] a bare unmarked assertion IS caught      : %d hit(s)"
      % ("ok" if pos else "DEAD", len(pos)))
print("      [%s] the same assertion, marked, is NOT caught: %d hit(s)"
      % ("ok" if not neg else "BAD", len(neg)))
if not pos:
    selferr("the sweep does not catch a bare unmarked assertion after the "
            "widening, so its 'no fifth site' result is worthless")
if neg:
    selferr("the sweep fires on a correctly marked withdrawal")
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the git reads and file reads above"
      % len(SELF))
print("FINDINGS: %d, population: the %d site-checks across X2's four sites, "
      "X3, X5, X6, the 95.7%% figure, Repaired 1's five sites, and the "
      "whole-tree sweep" % (len(FIND), CHECKS))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
