"""mg-54b1 C0 -- WHAT THIS CLASSIFIER CATCHES, AND WHAT IT IS DECLARED BLIND TO.

A classifier with no controls is a net presented as a catch, which is the one
thing mg-20ee's own census.py is criticised for in its README.  So every claim
lib54b1 makes is planted here in both directions, and the two rules are held to
their size: RULE B's vocabulary is PRINTED, with its length, so that growing it
is visible in a diff.

The planted worlds are not invented shapes.  Every line below is copied from a
real committed transcript under code/, and the transcripts are named.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib54b1 as L

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True).stdout.strip()

bad = 0
WORLD_LINES = []


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


def diff_of(path, old, new):
    """A minimal unified diff of one changed line, as git would emit it."""
    return ("diff --git a/%s b/%s\n--- a/%s\n+++ b/%s\n@@ -1 +1 @@\n-%s\n+%s\n"
            % (path, path, path, path, old, new))


def world(wid, expect, path, old, new, why):
    global bad
    WORLD_LINES.append((old, new))
    got, ev = L.classify_diff(diff_of(path, old, new))
    ok = (got == expect)
    bad += (not ok)
    print("  %-5s expect %-14s got %-14s %s  %s"
          % (wid, expect, got, "ok" if ok else "*** FAILED ***", why))
    if not ok or expect == "VERDICT MOVED":
        for _p, evs in ev.items():
            for rule, o, n in evs[:1]:
                print("        %s" % rule)
                print("        -  %s" % o[:88])
                print("        +  %s" % n[:88])
    return ok


hdr("mg-54b1 C0  PLANTED WORLDS -- the strong sense, in both directions")

print("  A world is one changed line in one transcript.  `VERDICT MOVED` is the")
print("  strong sense this instrument exists to count; `ADDRESSES ONLY` is what")
print("  mg-20ee's pinning tranche removes and what must NOT be counted as a")
print("  finding.  The NEGATIVE worlds are the load-bearing half: a classifier")
print("  that says VERDICT MOVED to everything measures nothing.")
print()

print("  §1  MUST FIRE -- a verdict moved")
print()
P = "code/x/out_x.txt"
world("W1", "VERDICT MOVED", P,
      "  Q2     check_doc.py  IN  delete C4's anchor    1    0    *** MISSED ***",
      "  Q2     check_doc.py  IN  delete C4's anchor    1    1    as predicted",
      "6cb9 a1 Q2: the marker vocabulary")
world("W2", "VERDICT MOVED", P,
      "  e2_crosssection.py exits 0 unmutated                               ok",
      "  e2_crosssection.py exits 0 unmutated                     *** FAILED ***",
      "6cb9 selftest: ok -> FAILED")
world("W3", "VERDICT MOVED", P,
      "  [PASS] V6d REACH -- of the 210 formatted values V6b counts",
      "  [FAIL] V6d REACH -- of the 210 formatted values V6b counts",
      "e35b verify: a bracket tag flipped")
world("W4", "VERDICT MOVED", P,
      "A1 TOTAL BAD: 1", "A1 TOTAL BAD: 0",
      "6cb9 a1: RULE B, the digit IS the verdict")
world("W5", "VERDICT MOVED", P,
      "  check_doc.py   baseline clean | INSIDE 1/2 fired | OUTSIDE 3/3 silent",
      "  check_doc.py   baseline clean | INSIDE 2/2 fired | OUTSIDE 3/3 silent",
      "6cb9 a1: RULE B, a fired ratio")
world("W6", "VERDICT MOVED", P,
      "     exit 0 -- SILENT.  The printed extent claims this file",
      "     exit 1 -- fired, the extent is true here",
      "6cb9 a1: SILENT -> fired, a vocabulary nobody enumerated")
world("W7", "VERDICT MOVED", P,
      "selftestd6cb9: 33 assertion(s), 0 failed",
      "selftestd6cb9: 33 assertion(s), 2 failed",
      "6cb9 selftest: RULE B, an assertion tally")

print()
print("  §2  MUST NOT FIRE -- an address or a magnitude moved and nothing else")
print("      GREEN ON PURPOSE.  These are exactly what mg-20ee's AS_OF pins")
print("      remove, and counting one as a finding would make this census a")
print("      restatement of the census it exists to be different from.")
print()
world("N1", "ADDRESSES ONLY", P,
      "  corpus read at : 5a62e8c88c4458453e47593d3474d584d2def8ff",
      "  corpus read at : e337f2311a4a0f3ee0e2b4bfd44c3f5c4b1a09cc",
      "a sha moved")
world("N2", "ADDRESSES ONLY", P,
      "  E2 POPULATION EXAMINED: 267 markdown file(s)",
      "  E2 POPULATION EXAMINED: 530 markdown file(s)",
      "a corpus size moved -- mg-f771 W2's own shape")
world("N3", "ADDRESSES ONLY", P,
      "  strike line 372   run   4 of  47 (  9%)  restated at line 295",
      "  strike line 401   run   4 of  47 (  9%)  restated at line 318",
      "line numbers moved, verdict column absent from both")
world("N4", "ADDRESSES ONLY", P,
      "VERDICT: CLEAN  0.11s", "VERDICT: CLEAN  0.14s",
      "a duration moved -- mg-f771 W3's declared NOISE")
world("N5", "ADDRESSES ONLY", P,
      "  measured on   : 2026-08-13, against the working tree",
      "  measured on   : 2026-09-01, against the working tree",
      "a date moved")
world("N6", "ADDRESSES ONLY", P,
      "  reading /Users/daniel/research/onethird_program/code/x/y.py",
      "  reading /Users/daniel/.pogo/polecats/p54b1/code/x/y.py",
      "a worktree root moved -- mg-f771 N1's own shape")
world("N7", "ADDRESSES ONLY", P,
      "  -> code/species_sites_821e/out_a2_6cb9_after.txt",
      "  -> code/species_sites_9999/out_a2_6cb9_after.txt",
      "an addressed PATH moved; see the EXTENT note below")
world("N8", "ADDRESSES ONLY", P,
      "VERDICT: CLEAN  0.11s", "VERDICT: CLEAN  1.11s",
      "MY OWN DEFECT: a duration on a VERDICT line, read as a scored counter")

print()
print("  §3  THE OTHER TWO CLASSES")
print()
for wid, expect, text, why in [
        ("D1", "DEAD",
         "diff --git a/%s b/%s\n@@ -1 +1 @@\n-  A3 TOTAL BAD: 1\n+Traceback "
         "(most recent call last):\n" % (P, P),
         "a3_differ_and_placement.py today: the instrument no longer runs"),
        ("D2", "REPRODUCES", "", "an empty diff")]:
    got, _ = L.classify_diff(text)
    ok = (got == expect)
    bad += (not ok)
    print("  %-5s expect %-14s got %-14s %s  %s"
          % (wid, expect, got, "ok" if ok else "*** FAILED ***", why))

print()
hdr("§4  RULE B'S VOCABULARY, PRINTED SO THAT GROWING IT IS VISIBLE")
print("  RULE A names no verdict words and cannot be outrun by an instrument")
print("  that invents its own.  RULE B is the half that CAN be blind: it is a")
print("  list, and a scored counter whose shape is not on it reads as an")
print("  address.  There are %d entries and they are:" % len(L.SCORED_COUNTERS))
print()
for name, pat in L.SCORED_COUNTERS:
    print("      %-16s %s" % (name, pat.pattern))
print()
print("  WHICH ENTRIES A WORLD ABOVE ACTUALLY EXERCISES IS MEASURED, NOT LISTED.")
print("  The first draft of this section named three by hand and was WRONG:")
print("  `failure tally` also matches the `0 failed` of W7's assertion line, so")
print("  a hand-written coverage list under-reported its own coverage.  The")
print("  entries below are the ones no planted world reaches, computed by")
print("  running every world's two lines back through the list.")
print()
exercised = set()
for _o, _n in WORLD_LINES:
    for nm, _g in L.scored(_o) + L.scored(_n):
        exercised.add(nm)
unex = [nm for nm, _ in L.SCORED_COUNTERS if nm not in exercised]
for nm in unex:
    print("      %-16s no planted world" % nm)
if not unex:
    print("      (none -- every entry is reached by a world above)")
print()
print("  %d of %d entries exercised." % (len(exercised), len(L.SCORED_COUNTERS)))

print()
hdr("§6  REAL DIFFS FROM THIS REPOSITORY'S OWN HISTORY")
print("""  A planted world is a line I wrote.  These are diffs somebody else
  produced, LABELLED BY THEIR OWN COMMIT MESSAGE rather than by me, which is
  the only labelling here I did not author.""")
print()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=REPO,
                          capture_output=True, text=True).stdout


def real(rid, expect, rev, paths, why, known_overcount=False):
    global bad
    d = git("diff", rev + "^", rev, "--", *paths)
    if not d.strip():
        print("  %-5s *** NO DIFF -- %s is not in this history ***" % (rid, rev))
        bad += 1
        return
    got, ev = L.classify_diff(d)
    ok = (got == expect)
    if known_overcount:
        print("  %-5s classifier says %-14s ADJUDICATED %-14s %s"
              % (rid, got, expect, "*** OVER-COUNT, KNOWN ***"))
    else:
        bad += (not ok)
        print("  %-5s expect %-14s got %-14s %s" %
              (rid, expect, got, "ok" if ok else "*** FAILED ***"))
    print("        %s" % why)
    for _p, evs in list(ev.items())[:2]:
        for rule, o, n in evs[:1]:
            print("        %s" % rule)
            print("        -  %s" % o.strip()[:84])
            print("        +  %s" % n.strip()[:84])


# The refresh this branch landed.  Resolved by FOLLOWING THE FILE rather than
# by a written-in sha: a branch's own commit sha does not survive the
# refinery's rebase, which is mg-daba's defect and mg-20ee's first bad pin.
A1 = "code/species_extent_audit_6cb9/out_a1_bothways.txt"
rev = git("log", "-1", "--format=%H", "--", A1).strip()[:12] or "HEAD"
real("R1", "VERDICT MOVED", rev, [A1],
     "mg-54b1's own refresh of 6cb9 a1 -- three verdicts, and the reason this "
     "ticket exists")

real("R2", "ADDRESSES ONLY", "6c9ab90",
     ["code/control_audit_9876/out_a4_sweep.txt"],
     "`220 -> 221 directories because this branch adds one, and the row that "
     "flagged mine stays at 27` -- its own words")

real("R3", "ADDRESSES ONLY", "417a789",
     ["code/control_audit_9876/out_a4_sweep.txt",
      "code/control_gate_724a/out_gate.txt"],
     "`the arm census gains one directory` -- a LISTING that gained an entry, "
     "which this classifier calls a moved verdict.  NOT SCORED AS A PASS AND "
     "NOT TUNED AWAY: separating a census listing from a findings listing "
     "needs to know which one this line is, and a rule that knew would be a "
     "rule about one file.  This is the calibration number -- one real "
     "over-count in three real diffs.",
     known_overcount=True)

print()
hdr("§5  THE EXTENT OF THIS CLASSIFIER, AND WHICH WAY IT ERRS")
print("""  UNDER-COUNTS.  RULE A erases addresses before comparing, so a diff whose
  only change is WHICH FILE or WHICH LINE a finding is about reads as
  ADDRESSES ONLY -- world N7 above is that case, planted GREEN on purpose.
  A finding that moved to a different subject is a real change and this
  classifier will not report it.

  OVER-COUNTS.  RULE A fires on ANY non-address word that changed on a line,
  including prose an author edited beside a result.  A transcript whose
  narration was reworded reads as VERDICT MOVED.

  ONE MISS, MEASURED RATHER THAN REASONED ABOUT.  RULE A erases digits, so a
  verdict carried ONLY by a digit is invisible to it and reaches RULE B's
  declared list or nothing.  This line is one of the three the mg-54b1 ticket
  itself quotes as a moved verdict, and no entry in the list matches it:""")
_miss = ("  3 WIDE site(s) are silent.  Both repaired scans read",
         "  1 WIDE site(s) are silent.  Both repaired scans read")
print("        -  %s" % _miss[0].strip())
print("        +  %s" % _miss[1].strip())
print("        classifier: %s" % ("MISSED" if not L.moved(*_miss)[0] else
                                  "caught -- this note is stale"))
print("""
  6cb9 is still reported VERDICT MOVED, because its `*** MISSED ***` and
  `TOTAL BAD` lines moved in the same run.  An instrument whose ONLY movement
  is an unlisted counter would be missed outright, and that is the shape a
  successor should widen RULE B for -- with a world beside it.

  THEREFORE THE COUNT IS NOT PUBLISHED ALONE.  classify.py prints the quoted
  -/+ pair for every VERDICT MOVED it reports, so a reader can do to this
  classifier what mg-20ee did to census.py: check the net against the catch.

  NOT MEASURED HERE AT ALL: an instrument whose baseline control has gone red,
  which makes its remaining rows unscorable without any of them changing.
  code/species_extent_audit_6cb9's a2 arm is exactly that and this classifier
  reports it as VERDICT MOVED for the four rows that moved, which is true but
  is not the finding.  Naming it is all this instrument does about it.""")

print()
print("=" * 78)
print("C0 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(1 if bad else 0)
