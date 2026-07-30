"""W3 -- THE CHECKER THAT MG-6F61 DID NOT BUILD: the INSTRUMENT, not the
document.

mg-6f61 built `code/species_repair_6f61/check_doc.py`, which requires every
false sentence to survive only inside the strike that replaces it -- IN
`docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md`.  It reads one file.
That is why three of mg-a61f's findings were repaired in the prose and left
standing in `code/species_7d75/`, where a successor re-runs them:

  X4  `t3_bidigare.py` headed T3d "four candidate identifications, three are
      controls" and its vacuity branch read "the three controls did not fire".
  X5  `code/species_7d75/README.md` presented control (ii)'s 1 442 / 252 /
      11 020 under "Conventions that have bitten this repo before" as
      measuring "how differently" the two products behave -- the near-miss
      reading the audit refuted.
  S4  `t4_one_operation.py` printed "Sol(S_n) / rad = k^{Pi_n / S_n} = the
      character ring of S_n" and `t6_fock_and_record.py` printed "K(Pi) =
      symmetric functions, whose degree-n component is the character ring of
      S_n", both unmarked, both inside a run that ends TOTAL BAD: 0.  The
      second equality in each is ledger S4 / S5: cited to Solomon and to
      Garsia-Reutenauer/Atkinson, neither read here or by the audit.  A
      reader is given no way to tell the measured half from the cited one.

THIS FILE IS THE DETECTOR FOR ALL THREE, AND IT WAS RUN AGAINST THE
PRE-REPAIR TREE FIRST: it reported 12 problems there.  A checker written after
the fix and never seen to fail is not a checker.  `out_w3_scope_before.txt`
is the failing run, committed beside the passing one.

(That number read "6" until mg-a4ef, on mg-73df's Y5, against its own
evidence file's `FAIL (12 problems)` and against sections 14.3 and S14, which
both say 12.  A checker's own account of the run that falsified it told a
successor the falsification was half the size it was.)

ITS EXTENT, STATED, WHICH IS mg-73df's MAJOR (see section 14.4).  This file
enforces TWO of the eleven corrections -- X4 and X5 -- over ONE tree, plus the
character-ring rule.  `check_doc.py` enforces ten of them over ONE file.  So
between them every file was covered and every statement was covered, and NO
STATEMENT WAS COVERED IN EVERY FILE -- which is how X3 stayed in force in
`t6_fock_and_record.py` inside a run ending `T6 TOTAL BAD: 0`.  The union of
the two lists over all trees is `code/species_repair_a4ef/s1_extent.py`.
A PASS HERE IS NOT COVERAGE OF THAT EXTENT.

    python3 code/species_remainder_f8fa/w3_scope.py
"""

import os
import re
import sys

from kernf8fa import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
# The directory under test defaults to the source instrument.  It is
# overridable so the SAME checker can be pointed at the pre-repair tree --
# which is how `out_w3_scope_before.txt` is produced, and the reason that
# file is evidence rather than decoration:
#
#     git worktree list                      # from this repo
#     mkdir -p /tmp/pre && git archive 83ac472 code/species_7d75 \
#         | tar -x -C /tmp/pre
#     python3 w3_scope.py /tmp/pre/code/species_7d75
#
SRC = (os.path.abspath(sys.argv[1]) if len(sys.argv) > 1
       else os.path.normpath(os.path.join(HERE, "..", "species_7d75")))
print("# target: %s" % os.path.join(*SRC.split(os.sep)[-2:]))
print()

# mg-d633, on mg-7dd3's A1: this listing filtered on `.py/.txt/.md`, so
# "over ONE tree" in the extent below covered every file in the tree EXCEPT
# `run_all.sh`, which is in it.  Same defect as `s1_extent.py`'s, one tree
# narrower, and repaired the same way: THE CODE IS WIDENED, not the claim
# narrowed.  Every regular file is read; anything undecodable is NAMED in the
# output rather than dropped by a rule no sentence carries.
#
# mg-821e, on mg-6cb9's F1: and it now RECURSES.  `os.listdir` plus a
# `continue` past anything that is not a file dropped every SUBDIRECTORY --
# again by a rule no sentence carried, and again invisible, because
# `code/species_7d75` has never had one.  "Every regular file in it" was a
# true sentence resting on an unstated condition; X4 planted in
# `code/species_7d75/sub/leak.md` left this checker silent (mg-6cb9 Q10).  The
# walk is now `os.walk`, so the sentence is true BY CONSTRUCTION.  ONE
# directory rule remains and it is PRINTED: `__pycache__` is not descended
# into, because it holds bytecode these runs write themselves.
PYCACHE = "__pycache__"
FILES, UNDECODABLE = [], []
for _dp, _dns, _fns in os.walk(SRC):
    _dns[:] = sorted(_d for _d in _dns if _d != PYCACHE)
    for _f in sorted(_fns):
        _p = os.path.join(_dp, _f)
        _rel = os.path.relpath(_p, SRC)
        if not os.path.isfile(_p):
            continue
        try:
            open(_p, encoding="utf-8").read()
        except (UnicodeDecodeError, OSError):
            UNDECODABLE.append(_rel)
            continue
        FILES.append(_rel)
FILES.sort()
UNDECODABLE.sort()
NESTED = [f for f in FILES if os.sep in f]
TEXT = {f: open(os.path.join(SRC, f), encoding="utf-8").read() for f in FILES}
print("# files read: %d, %d of them below the tree root   (skipped as not"
      % (len(FILES), len(NESTED)))
print("# UTF-8 text: %s; skipped as %s: the whole directory rule)"
      % (", ".join(UNDECODABLE) if UNDECODABLE else "none", PYCACHE))
if NESTED:
    for _f in NESTED:
        print("#   below the root: %s" % _f)
print()
LINES = {f: TEXT[f].splitlines() for f in FILES}


# ---------------------------------------------------------------------------
# A.  The corrected statements must not still be ASSERTED at source.
# ---------------------------------------------------------------------------
FORBIDDEN = [
    ("X4  T3d's control count",
     [r"three\s+are\s+controls", r"the\s+three\s+controls",
      r"three\s+of\s+the\s+four\s+(?:columns\s+)?are\s+the\s+control"]),
    ("X5  control (ii) read as a near miss",
     [r"measures\s+how\s+differently"]),
]

# Deliberately NARROW.  An earlier version of this file accepted a bare
# "REPAIRED" or "CORRECTED" nearby, and the pre-repair README disarmed it by
# accident: an unrelated "the error mg-1953 repaired" four lines above the
# near-miss bullet made the bullet read as already corrected.  A marker has to
# name THIS repair, or say in so many words that the sentence no longer holds.
QUOTED_AS_CORRECTED = re.compile(r"mg-f8fa|used\s+to|no\s+longer", re.I)
QWINDOW = 4

hdr("W3a  the corrected statements are not still ASSERTED in the instrument")
print()
print("  This is the negative half, and it is the load-bearing one -- the")
print("  same shape as check_doc.py's strike test, moved from the document to")
print("  the code.  A corrected statement may survive ONLY where it is being")
print("  quoted as corrected: within %d lines of a marker saying so.  Anywhere"
      % QWINDOW)
print("  else it is still in force, whatever the prose elsewhere says.")
print()
for label, pats in FORBIDDEN:
    asserted, quoted = [], []
    for f in FILES:
        for i, ln in enumerate(LINES[f]):
            if not any(re.search(p, ln, re.I) for p in pats):
                continue
            lo, hi = max(0, i - QWINDOW), min(len(LINES[f]), i + QWINDOW + 1)
            near = "\n".join(LINES[f][lo:hi])
            (quoted if QUOTED_AS_CORRECTED.search(near)
             else asserted).append("%s:%d" % (f, i + 1))
    ok = not asserted
    bad += (not ok)
    print("  %-46s %s" % (label, "ok" if ok else "*** STILL ASSERTED ***"))
    for h in asserted:
        print("        STILL ASSERTED AT  %s" % h)
    for h in quoted:
        print("        quoted as corrected at %s" % h)
print()


# ---------------------------------------------------------------------------
# B.  EVERY occurrence of the cited identification carries its ledger row.
# ---------------------------------------------------------------------------
CITED = re.compile(r"character\s+ring", re.I)
MARKER = re.compile(r"ledger\s+S[45]|CITED,?\s+NOT\s+(?:DERIVED|VERIFIED)"
                    r"|NOT\s+VERIFIED\s+HERE", re.I)
WINDOW = 8

hdr("W3b  EVERY occurrence of the CITED identification is marked, not only"
    " the ledger")
print()
print("  Rule: any line in code/species_7d75 that identifies the semisimple")
print("  quotient with the CHARACTER RING of S_n must have the scope marker")
print("  within %d lines of it, in the same file.  The step from k^{Pi_n/S_n}"
      % WINDOW)
print("  to the character ring is ledger S4; the Fock-functor statement is")
print("  S5.  Neither Solomon nor Garsia-Reutenauer/Atkinson was read, here")
print("  or by mg-a61f.")
print()
found = 0
for f in FILES:
    for i, ln in enumerate(LINES[f]):
        if not CITED.search(ln):
            continue
        found += 1
        lo, hi = max(0, i - WINDOW), min(len(LINES[f]), i + WINDOW + 1)
        near = "\n".join(LINES[f][lo:hi])
        ok = bool(MARKER.search(near))
        bad += (not ok)
        print("  %-38s line %-5d %s"
              % (f, i + 1, "marked" if ok else "*** UNMARKED ***"))
if not found:
    bad += 1
    print("  *** NO OCCURRENCE FOUND -- the detector is looking at the wrong")
    print("      tree, or the identification was deleted rather than scoped ***")
else:
    print()
    print("  %d occurrence(s) checked." % found)
print()


# ---------------------------------------------------------------------------
# C.  The positive half: the corrected readings are present at source.
# ---------------------------------------------------------------------------
REQUIRED = [
    ("t3_bidigare.py", "X4  two statements, each computed twice",
     r"two\s+statements,?\s+each\s+computed\s+twice"),
    ("t3_bidigare.py", "X4  and the count is COMPUTED, not asserted",
     r"T3e"),
    ("t5_hopf_monoid.py", "X5  control (ii) reads as a type mismatch",
     r"type\s+mismatch"),
    ("t5_hopf_monoid.py", "X5  and its conclusion is stated to survive",
     r"NOT\s+withdrawn|is\s+not\s+withdrawn"),
    ("README.md", "X5  the conventions bullet is repaired",
     r"type\s+mismatch"),
    ("README.md", "S4  the S_n half is named as unverified",
     r"ledger\s+S4"),
]

hdr("W3c  the corrected readings are present at source")
print()
for f, label, pat in REQUIRED:
    ok = f in TEXT and bool(re.search(pat, TEXT[f], re.I))
    bad += (not ok)
    print("  %-14s %-46s %s" % (f, label, "ok" if ok else "*** MISSING ***"))
print()

print("=" * 78)
print("W3 SCOPE: %s   (%d problem(s))" % ("PASS" if bad == 0 else "FAIL", bad))
print("=" * 78)
print()
print("EXTENT OF THAT VERDICT (added mg-a4ef).  MEASURED mg-d633.  DEEPENED")
print("mg-821e.  This enforces TWO corrected statements -- X4 and X5 -- plus")
print("the character-ring rule, over ONE tree of %d file(s)." % len(FILES))
# The next line is ONE line on purpose.  mg-6cb9's A1g asks whether the
# committed output SAYS that the repair widened the code, and it looks for the
# phrases `every regular file in it` and `no extension rule`.  Wrapping this
# sentence across two prints splits both, and A1g went *** SILENT *** against
# a file that says so more loudly than before.  A label check that reads the
# artifact is worth keeping; the artifact is what moves to suit it.
print("It reads every regular file in it, AT ANY DEPTH: no extension rule")
print("and no depth rule.  The extension rule existed until mg-d633 and")
print("dropped run_all.sh while this line said 'over ONE tree'; the depth")
print("rule existed until mg-821e and dropped every subdirectory while this")
print("line made the same claim -- true, and true only because the tree had")
print("no subdirectory (mg-6cb9 F1).  The one directory rule left is %s/,"
      % PYCACHE)
print("and it is named here rather than left to be inferred from the code.")
print("mg-6f61 enumerated ten stricken sentences; eight of")
print("them are NOT on this list, and X3 and the AM 17.5 quotation were in")
print("force in code/species_7d75 for the whole time this file reported")
print("PASS.  A PASS HERE IS NOT COVERAGE OF THE OTHER NINE STATEMENTS.")
print("The union of both lists over all trees is:")
print("    python3 code/species_repair_a4ef/s1_extent.py")
# mg-a4ef: this was `sys.exit(0)` unconditionally, so a run reporting
# `FAIL (12 problems)` still exited 0 -- the same shape as the finding this
# file exists to carry.  Beyond mg-73df's five; recorded in the repair doc.
sys.exit(1 if bad else 0)
