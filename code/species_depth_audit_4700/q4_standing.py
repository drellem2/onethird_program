"""Q4 -- DO NOT DISTURB WHAT IS CONFIRMED.

mg-6cb9 confirmed two things about mg-d633 and this audit's brief says to flag
any weakening of either:

  * all four extents MEASURED BOTH WAYS at the auditor's own sites;
  * the cross-section check DEMONSTRABLY FIRES, three ways in two documents.

Both were measured by mg-6cb9's own battery, so the honest test is to run THAT
battery, unmodified, against the tree as it now stands -- not to re-implement
its questions in this instrument's words, which would let a weakening hide in
the rewording.  `a1_bothways.py` and `a2_crosssection.py` are executed from
their own tree with no edit of any kind, and the byte-level agreement with the
transcripts mg-821e committed is checked as well.

  Q4a  `a1_bothways.py`, unmodified.  Its own totals, its own WIDE rows.
  Q4b  `a2_crosssection.py`, unmodified.  The three ways, in two documents.
  Q4c  THE COMMITTED TRANSCRIPTS vs THE LIVE RUN.  mg-821e published
       out_a1_6cb9_after.txt and out_a2_6cb9_after.txt as evidence.  A
       transcript is a claim about a run; this compares it with the run.

    python3 code/species_depth_audit_4700/q4_standing.py
"""

import difflib
import os
import re
import sys

from kern4700 import hdr, HERE, REPO, sh, run_checker, predict

bad = 0
miss = 0

A1 = "code/species_extent_audit_6cb9/a1_bothways.py"
A2 = "code/species_extent_audit_6cb9/a2_crosssection.py"
T_A1 = "code/species_sites_821e/out_a1_6cb9_after.txt"
T_A2 = "code/species_sites_821e/out_a2_6cb9_after.txt"


def total(out, key):
    m = re.search(r"^%s (\d+)" % re.escape(key), out, re.M)
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Q4a  a1_bothways.py, unmodified
# ---------------------------------------------------------------------------
hdr("Q4a  mg-6cb9's `a1_bothways.py`, RUN UNMODIFIED")

rc1, out1 = run_checker(A1)
t1 = total(out1, "A1 TOTAL BAD:")
miss += predict("D5a", "A1 TOTAL BAD 0, exit 0",
                "A1 TOTAL BAD %s, exit %d" % (t1, rc1), t1 == 0 and rc1 == 0)
bad += (t1 != 0)
print()
print("  THE FOUR EXTENTS, MEASURED BOTH WAYS, at mg-6cb9's own sites.  These")
print("  rows are that audit's, printed by that audit's file:")
keep = False
both = 0
for line in out1.splitlines():
    if re.match(r"^\s*A1[bcd]\s", line) or "BOTH DIRECTIONS" in line.upper():
        keep = True
    if keep and re.search(r"\bIN\s+both\b|both direction|measured both ways",
                          line, re.I):
        print("      %s" % line.rstrip()[:96])
        both += 1
for line in out1.splitlines():
    if "extent TRUE here" in line or "EXTENT WIDER" in line:
        print("      %s" % line.rstrip()[:96])
        both += 1
print()
print("  Q17e prints RED in that battery BY DESIGN and it is not a defect:")
print("  it runs e1_extents.py, whose exit 1 means AN EXTENT LINE IS FALSE,")
print("  and mg-6cb9 scores a WIDE row good only at exit 1.  mg-821e said so")
print("  in the run rather than leaving it to be found; this row is here so")
print("  that a reader of THIS transcript is told the same thing.")
for line in out1.splitlines():
    if "Q17e" in line:
        print("      %s" % line.rstrip()[:96])
print()


# ---------------------------------------------------------------------------
# Q4b  a2_crosssection.py, unmodified
# ---------------------------------------------------------------------------
hdr("Q4b  mg-6cb9's `a2_crosssection.py`, RUN UNMODIFIED")

rc2, out2 = run_checker(A2)
t2 = total(out2, "A2 TOTAL BAD:")
miss += predict("D5b", "A2 TOTAL BAD 1 (R29), exit 1",
                "A2 TOTAL BAD %s, exit %d" % (t2, rc2), t2 == 1 and rc2 == 1)
print()
print("  THE CROSS-SECTION CHECK FIRES, THREE WAYS IN TWO DOCUMENTS -- again,")
print("  mg-6cb9's own rows:")
for line in out2.splitlines():
    if re.search(r"reach it|three ways|fires|F4", line) and \
            not line.strip().startswith("#"):
        s = line.rstrip()
        if s.strip():
            print("      %s" % s[:96])
print()
print("  and the TWO F4 ROWS -- the ones b534db7 exists to have turned green:")
F4ROWS = ("the COMMITTED run's extent line is true at HEAD",
          "the committed CENSUS is right for the shipped tree")
f4ok = 0
for line in out2.splitlines():
    for r in F4ROWS:
        if r in line:
            print("      %s" % line.rstrip()[:96])
            f4ok += (line.rstrip().endswith("ok"))
print("  reading ok: %d of 2" % f4ok)
print()
for line in out2.splitlines():
    if "R29" in line and "OUT" in line:
        print("  R29, mg-6cb9's own kept prediction miss, still present and")
        print("  still not a regression:")
        print("      %s" % line.rstrip()[:96])
        break
print()


# ---------------------------------------------------------------------------
# Q4b2  the bottom line, against the commit message that reports it
# ---------------------------------------------------------------------------
hdr("Q4b2  A2 TOTAL BAD, AGAINST WHAT THE REPAIR'S OWN COMMIT SAYS IT IS")

print("  `41ac5d4`: \"Its a2_crosssection.py: A2 TOTAL BAD 1, the one row being")
print("  R29 ... both F4 rows still read ok against HEAD.\"  `b534db7`, whose")
print("  entire subject is PUBLISH THE POST-COMMIT MEASUREMENT: \"A2 TOTAL BAD")
print("  stays 1.\"  Live, at HEAD, in a clean worktree:")
print()
print("      A2 TOTAL BAD  claimed 1   measured %s" % t2)
print("      F4 rows       claimed ok, ok   measured %d of 2 ok" % f4ok)
print()
if t2 != 1 or f4ok != 2:
    bad += 1
    print("  *** FINDING.  The claim is not true of the tree it is committed")
    print("      into.  It was true where it was measured, which is the whole")
    print("      of the matter and is developed in Q4d. ***")
print()


# ---------------------------------------------------------------------------
# Q4c  the committed transcripts against the live run
# ---------------------------------------------------------------------------
hdr("Q4c  THE PUBLISHED TRANSCRIPTS AGAINST THE RUN THEY CLAIM TO BE")

print("  mg-821e committed both of these as its evidence that the instrument")
print("  which raised the findings now reports them closed.  A transcript is")
print("  a claim about a run.  These two rows compare it with the run.")
print()
_mine = [f for f in os.listdir(HERE) if f.endswith(".md")]
print("  DECLARED FIRST: this instrument's own %d markdown file(s) -- %s --"
      % (len(_mine), ", ".join(sorted(_mine))))
print("  are under code/, and e2 reads every *.md under code/.  So the LIVE")
print("  file count below is %d higher than the shipped tree's, by me."
      % len(_mine))
print("  None of them carries a `~~strike~~`, so the strike census is not")
print("  perturbed -- and Q4d below counts from `git` alone and is immune to")
print("  this instrument entirely: it counts *.md from `git` at four named")
print("  commits and never looks at the worktree.  The two F4 rows and the")
print("  A2 TOTAL BAD below are decided by `git ls-tree` against a committed")
print("  transcript, so no file of mine can reach them either.")
print()
for label, rel, live in (("out_a1_6cb9_after.txt", T_A1, out1),
                         ("out_a2_6cb9_after.txt", T_A2, out2)):
    p = os.path.join(REPO, rel)
    if not os.path.exists(p):
        print("  %-28s *** not committed ***" % label)
        bad += 1
        continue
    stored = open(p, encoding="utf-8").read()
    a = stored.splitlines()
    b = live.splitlines()
    diff = [d for d in difflib.unified_diff(a, b, lineterm="", n=0)
            if d[:1] in "+-" and d[:3] not in ("---", "+++")]
    same = not diff
    bad += (not same)
    print("  %-28s %d line(s) stored, %d live, %s"
          % (label, len(a), len(b),
             "IDENTICAL" if same else "*** %d line(s) differ ***" % len(diff)))
    for d in diff[:12]:
        print("        %s" % d[:92])
    if len(diff) > 12:
        print("        ... and %d more" % (len(diff) - 12))
print()
print("  A published transcript that no longer reproduces is the same defect")
print("  as an extent that is true only today, in a different medium: both")
print("  are claims resting on a condition nobody re-checks.  These two are")
print("  re-checked here.")
print()


# ---------------------------------------------------------------------------
# Q4d  WHY.  The condition was `HEAD as it stood when I ran it`.
# ---------------------------------------------------------------------------
hdr("Q4d  THE CENSUS IS 8 SHORT, AND THE CONDITION THAT BROKE IS UNNAMED")

print("  This is not a re-run that drifted.  `out_e2_crosssection.txt` is a")
print("  committed artifact, af432ee REGENERATED it, and its extent line is")
print("  the thing mg-6cb9's F4 measures.  Counting *.md under docs/ and")
print("  code/ at each commit, from git, so none of it is my worktree:")
print()
CT = "code/species_extent_d633/out_e2_crosssection.txt"


def claimed_at(ref):
    rc, t, _ = sh(["git", "show", "%s:%s" % (ref, CT)])
    if rc != 0:
        return None
    m = re.search(r"(\d+) markdown file\(s\)", t)
    return int(m.group(1)) if m else None


def md_count(ref):
    rc, t, _ = sh(["git", "ls-tree", "-r", "--name-only", ref])
    return sum(1 for f in t.splitlines() if f.endswith(".md")
               and (f.startswith("docs/") or f.startswith("code/")))


print("      %-9s %-34s %8s %8s %6s"
      % ("commit", "what it is", "claimed", "actual", "short"))
for ref, what in (("e8fbd4f", "mg-d633 wrote the transcript"),
                  ("ef38841", "af432ee's parent"),
                  ("af432ee", "mg-821e REGENERATED it"),
                  ("HEAD", "the tree it ships in")):
    c, a = claimed_at(ref), md_count(ref)
    print("      %-9s %-34s %8s %8d %6s"
          % (ref, what, c if c is not None else "-", a,
             (a - c) if c is not None else "-"))
print()
print("  THE LOAD-BEARING ROW IS `af432ee`, NOT `HEAD`.  That row is a")
print("  statement about a commit that is fixed in git: the transcript it")
print("  contains claims 123 and the tree it contains holds 131, and no")
print("  later commit can move either number.  The HEAD row WILL move --")
print("  this audit's own commit adds markdown files under docs/ and code/")
print("  and will make the same extent line staler still.  That is the")
print("  mechanism, not a fix, and it is why the finding is anchored on a")
print("  pinned commit.  Anchored on HEAD it would have been a number that")
print("  changes every time anybody writes a document, which is exactly the")
print("  error 41ac5d4 came back to correct.")
print()
print("  mg-6cb9 raised this against mg-d633's transcript, which claimed 100")
print("  where its tree held 105.  af432ee regenerated the file and it now")
print("  claims 123 where its tree holds 131.  THE GAP DID NOT CLOSE, IT")
print("  WIDENED -- and mg-821e's own published transcript records the run")
print("  that produced 123 as having seen `git ls-tree HEAD -- 123`, a tree")
print("  no commit in this history has.")
print()
print("  WHAT ACTUALLY HAPPENED, and it is worth naming precisely because the")
print("  repair did the right thing by the rule it was given.  b534db7 exists")
print("  solely to obey this arc's Appendix A --")
print()
print("      A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST PUBLISH")
print("      THE POST-COMMIT MEASUREMENT")
print()
print("  -- and it did: it re-ran a2 with the repair landed and both F4 rows")
print("  turned ok.  Then the work was REBASED onto a main that had grown by")
print("  eight markdown files while the ticket was open, and the artifact")
print("  regenerated against the pre-rebase HEAD shipped inside a different")
print("  tree.  POST-COMMIT IS NOT POST-MERGE.  The rule as written names a")
print("  condition -- `the commit` -- that a merge queue is free to change")
print("  underneath it, and nothing re-checks it afterwards.")
print()
print("  That is this repair's OWN OPEN 1, one level out and in its evidence")
print("  rather than its code: a measurement true because of a state of the")
print("  world nobody had stated -- there `no tree has a subdirectory`, here")
print("  `main has not moved since I ran this`.  mg-821e removed the first")
print("  condition by construction.  The second is still stated nowhere, and")
print("  it has now gone false twice in the same file.")
print()
print("  WHAT IS NOT AFFECTED, stated so the finding is not read as wider")
print("  than it is: e2's VERDICT.  A live run at HEAD reports 0 standing,")
print("  Q2a printed that from inside all three runners, and none of the 8")
print("  unread files carries a strike that could change it.  What is false")
print("  is the EXTENT LINE on a committed transcript -- which is exactly the")
print("  kind of claim this arc exists to take seriously.")
print()


print("=" * 78)
print("Q4 TOTAL BAD: %d" % bad)
print("Q4 PREDICTIONS MISSED: %d" % miss)
print("=" * 78)
print()
print("EXTENT OF THOSE NUMBERS.  Q4 runs exactly two files -- mg-6cb9's")
print("a1_bothways.py and a2_crosssection.py -- with NO modification of any")
print("kind, and compares their live output with the two transcripts mg-821e")
print("committed.  It re-implements none of their questions, on purpose: a")
print("re-implementation can agree with a weakened subject by being weakened")
print("in the same place.  It says nothing about mg-6cb9's third file")
print("a3_differ_and_placement.py, which neither of the confirmed findings")
print("this section is protecting depends on.  Q4d counts markdown files")
print("from `git` at four named commits and touches no worktree state.")
sys.exit(1 if bad else 0)
