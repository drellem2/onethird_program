"""Q1 -- A CONTINGENT EXTENT LOOKS IDENTICAL TO A SOUND ONE.  ADD A
SUBDIRECTORY AND SEE.

mg-6cb9's F1: `EVERY REGULAR FILE in each tree is read` was true, and true for
exactly one reason -- **no tree under `code/species_*` had a subdirectory**.
Both scans were a single `os.listdir` and a `continue` past anything that is
not `os.path.isfile`.  mg-821e says it removed the condition rather than
stating it: all three walks are `os.walk` now, so the sentence is true by
construction.

THIS FILE DOES NOT READ THE WALK AND CONCLUDE THAT.  `os.walk` in the source is
a fact about the source.  The claim is about behaviour, and the only instrument
that separates a contingent extent from a sound one is a subdirectory with a
file in it.  So:

  Q1a  DEPTH, MEASURED.  A forbidden statement is planted below the root, at
       depth 1, at depth 3, and in a tree mg-6cb9 never planted in, and each
       checker is RUN.  Silence is the finding; exit 1 is the repair working.
  Q1b  THE ONE STATED DIRECTORY RULE, measured in the other direction --
       `__pycache__` must still be skipped, because that rule is printed and
       therefore arguable.  A repair that widened until nothing was excluded
       would have kept a promise nobody made.
  Q1c  THE GUARD THAT DID NOT EXIST.  Put each walk back to `os.listdir`, one
       at a time, with a subdirectory planted, and `e1_extents.py` must fire.
       A repair with no guard is one careless edit from where it started.
  Q1d  A SECOND ONE, HUNTED.  `os.walk` does not descend into a SYMLINKED
       directory unless `followlinks=True`, and none of the three walks passes
       it.  The symlink is classified into `dirnames`, so it is never a
       candidate file either.  That is a second directory rule carried by no
       sentence -- the extent lines name exactly one -- and it is invisible
       today for precisely the reason F1 was invisible: no tree has one.

    python3 code/species_depth_audit_4700/q1_depth.py
"""

import os
import shutil
import sys
import tempfile

from kern4700 import hdr, REPO, Probe, run_checker, predict

bad = 0
miss = 0

W3 = "code/species_remainder_f8fa/w3_scope.py"
S1 = "code/species_repair_a4ef/s1_extent.py"
E1 = "code/species_extent_d633/e1_extents.py"

# X4 -- "§2.2, the control count" -- asserted plainly.  It is on BOTH lists:
# `w3_scope.py`'s two-row FORBIDDEN and `stricken_a4ef.py`'s CORRECTIONS, so
# one planted file is a probe of both checkers at once.
#
# Nothing in these three lines may exonerate it.  `kerna4ef` exonerates on
# `mg-(6f61|f8fa|a61f|73df|a4ef)` within six lines, on the NEGATES vocabulary
# ("refut", "STRICKEN", "no longer holds", "used to say"), and inside a
# declared table; `w3_scope` exonerates on `mg-f8fa|used to|no longer` within
# four.  `mg-4700` matches none of them, which is the point of using it.
LEAK = ("# planted by the mg-4700 audit, and removed again\n"
        "\n"
        "Three of the four columns are the control, and they fire.\n")

INNOCENT = ("# planted by the mg-4700 audit, and removed again\n"
            "\n"
            "This file asserts nothing at all.  It exists to have a depth.\n")


def fired(rc):
    return "exit %d (%s)" % (rc, "FIRES" if rc else "silent")


# ---------------------------------------------------------------------------
# Q1a  depth, measured
# ---------------------------------------------------------------------------
hdr("Q1a  A FORBIDDEN STATEMENT BELOW THE ROOT -- planted, and the checkers RUN")

print("  The planted file, verbatim, so a reader can see it carries no")
print("  exoneration:")
for ln in LEAK.rstrip("\n").split("\n"):
    print("      | %s" % ln)
print()

# D1a / D1b -- depth 1, in the tree w3_scope.py covers.
with Probe("D1ab depth 1 in species_7d75") as pr:
    pr.plant("code/species_7d75/sub/leak.md", LEAK)
    rc_w3, out_w3 = run_checker(W3)
    rc_s1, out_s1 = run_checker(S1)
miss += predict("D1a", "exit 1", fired(rc_w3), rc_w3 == 1)
miss += predict("D1b", "exit 1", fired(rc_s1), rc_s1 == 1)
named_w3 = "sub/leak.md" in out_w3
named_s1 = "sub/leak.md" in out_s1
bad += (rc_w3 != 1) + (rc_s1 != 1) + (not named_w3) + (not named_s1)
print("        w3_scope.py names the path below the root: %s"
      % ("yes" if named_w3 else "*** NO ***"))
print("        s1_extent.py names it:                     %s"
      % ("yes" if named_s1 else "*** NO ***"))
for line in out_s1.splitlines():
    if "STILL ASSERTED" in line and "sub/leak.md" in line:
        print("        %s" % line.strip())
for line in out_w3.splitlines():
    if "sub/leak.md" in line and "below the root" not in line:
        print("        %s" % line.strip())
print()

# D1c -- depth 3.  `os.walk` has no depth limit, but nothing in the extent line
# says the walk is unbounded either, so it is measured rather than assumed.
with Probe("D1c depth 3 in species_7d75") as pr:
    pr.plant("code/species_7d75/a/b/c/leak.md", LEAK)
    rc_w3d, out_w3d = run_checker(W3)
    rc_s1d, _ = run_checker(S1)
ok = rc_w3d == 1 and rc_s1d == 1
miss += predict("D1c", "exit 1 from both",
                "w3 %d / s1 %d" % (rc_w3d, rc_s1d), ok)
bad += (not ok)
print("        the path as w3_scope.py prints it: %s"
      % next((l.strip() for l in out_w3d.splitlines()
              if "a/b/c/leak.md" in l), "*** NOT NAMED ***"))
print()

# D1d -- a tree mg-6cb9 never planted in.  Its Q10/Q17 planted only in
# `code/species_7d75`; a repair that fixed the walk it was shown is a different
# repair from one that fixed the walk.
with Probe("D1d depth 1 in species_repair_a4ef") as pr:
    pr.plant("code/species_repair_a4ef/sub/leak.md", LEAK)
    rc_s1a, out_s1a = run_checker(S1)
    rc_w3a, _ = run_checker(W3)
miss += predict("D1d", "s1 exit 1, w3 exit 0",
                "s1 %d / w3 %d" % (rc_s1a, rc_w3a),
                rc_s1a == 1 and rc_w3a == 0)
bad += (rc_s1a != 1) + (rc_w3a != 0)
print("        s1_extent.py:  %s"
      % next((l.strip() for l in out_s1a.splitlines()
              if "STILL ASSERTED" in l and "sub/leak.md" in l),
             "*** NOT NAMED ***"))
print("        w3_scope.py is silent and that is CORRECT: its extent is ONE")
print("        tree and it says so.  A checker that fired here would be")
print("        reporting outside its own stated extent.")
print()


# ---------------------------------------------------------------------------
# Q1b  the one stated directory rule, in the other direction
# ---------------------------------------------------------------------------
hdr("Q1b  `__pycache__` -- the ONE rule that is printed, measured as still real")

print("  A repair that widened the walk until NOTHING was excluded would pass")
print("  every probe above and would have quietly dropped the one rule its")
print("  own extent line promises.  So the rule is measured in the direction")
print("  that can only fail: the same planted statement, under __pycache__.")
print()
with Probe("D1e __pycache__ is not descended into") as pr:
    pr.plant("code/species_7d75/__pycache__/leak.md", LEAK)
    rc_w3p, out_w3p = run_checker(W3)
    rc_s1p, out_s1p = run_checker(S1)
miss += predict("D1e", "exit 0 from both",
                "w3 %d / s1 %d" % (rc_w3p, rc_s1p),
                rc_w3p == 0 and rc_s1p == 0)
bad += (rc_w3p != 0) + (rc_s1p != 0)
print("        and the rule is NAMED in both printed extents:")
print("            w3_scope.py   %s"
      % ("__pycache__ named" if "__pycache__" in out_w3p else "*** NOT NAMED ***"))
print("            s1_extent.py  %s"
      % ("__pycache__ named" if "__pycache__" in out_s1p else "*** NOT NAMED ***"))
bad += ("__pycache__" not in out_w3p) + ("__pycache__" not in out_s1p)
print()

# The nested file must also be PRINTED when it is innocent -- an extent that
# only mentions depth when something goes wrong is not an extent.
with Probe("D1f an innocent file below the root is PRINTED") as pr:
    pr.plant("code/species_7d75/sub/note.md", INNOCENT)
    rc_e1n, out_e1n = run_checker(E1)
    rc_s1n, out_s1n = run_checker(S1)
printed = "sub/note.md" in out_s1n
miss += predict("D1f", "e1 exit 0, path printed",
                "e1 %d, printed %s" % (rc_e1n, "yes" if printed else "no"),
                rc_e1n == 0 and printed)
bad += (rc_e1n != 0) + (not printed)
for line in out_s1n.splitlines():
    if "below the tree root" in line and "species_7d75" in line:
        print("        %s" % line.strip())
for line in out_e1n.splitlines():
    if "file(s) sit below a tree root today" in line:
        print("        %s" % line.strip())
print()


# ---------------------------------------------------------------------------
# Q1c  the guard that did not exist
# ---------------------------------------------------------------------------
hdr("Q1c  PUT EACH WALK BACK TO `os.listdir` -- E1 must FIRE")

print("  mg-6cb9's F1 was invisible because E1, whose job is deciding whether")
print("  a printed extent is TRUE, listed the tree the same way the subjects")
print("  did: `want <= got` held over a file none of the three could see.  An")
print("  instrument that computes its expectation the way the subject computes")
print("  its answer cannot disagree with the subject.  These three rows are")
print("  the guard, and each is ONE LINE reverted -- the line that tells the")
print("  walk to descend.")
print()

REVERTS = [
    ("D1g", W3, "os.walk(SRC)", "[(SRC, [], os.listdir(SRC))]",
     "w3_scope.py"),
    ("D1h", S1, "os.walk(root)", "[(root, [], os.listdir(root))]",
     "s1_extent.py"),
    ("D1i", E1, "os.walk(root)", "[(root, [], os.listdir(root))]",
     "e1_extents.py (E1's OWN expectation)"),
]
for pid, rel, old, new, name in REVERTS:
    with Probe("%s revert %s" % (pid, name)) as pr:
        pr.plant("code/species_7d75/sub/note.md", INNOCENT)
        pr.edit(rel, old, new)
        rc, out = run_checker(E1)
    want = 1
    ok = rc == want
    miss += predict(pid, "exit %d" % want, fired(rc), ok)
    print("        reverted: %-24s %s -> %s" % (name, old, new))
    for line in out.splitlines():
        if "*** FALSE ***" in line:
            print("        %s" % line.rstrip())
    # D1i is the one predicted wrong on purpose; see OUTCOMES.md.  Only the
    # two SUBJECT walks are scored, because only they are what the guard is
    # for.  E1's own walk shrinking is a different failure and Q1d is where it
    # is measured.
    if pid != "D1i":
        bad += (not ok)
print()


# ---------------------------------------------------------------------------
# Q1d  A SECOND ONE.  What does the repaired extent still silently assume?
# ---------------------------------------------------------------------------
hdr("Q1d  THE SYMLINKED DIRECTORY -- a second rule carried by no sentence")

print("  The brief: a claim true by accident of the current tree is invisible")
print("  by inspection, so ASK OF EVERY EXTENT WHAT STATE OF THE WORLD IT")
print("  SILENTLY ASSUMES.  `os.walk` does not descend into a symlinked")
print("  directory unless `followlinks=True`, and none of the three walks")
print("  passes it.  The link is classified into `dirnames`, so it is never a")
print("  candidate file either.  The extent lines name ONE directory rule.")
print("  This is a second, and it is invisible today for exactly the reason F1")
print("  was invisible: no tree has one.")
print()

tmp = tempfile.mkdtemp(prefix="mg4700_")
try:
    hidden = os.path.join(tmp, "hidden")
    os.makedirs(hidden)
    with open(os.path.join(hidden, "leak.md"), "w", encoding="utf-8") as fh:
        fh.write(LEAK)

    with Probe("D2abc symlinked directory in species_7d75") as pr:
        pr.symlink("code/species_7d75/slink", hidden)
        rc_w3s, out_w3s = run_checker(W3)
        rc_s1s, out_s1s = run_checker(S1)
        rc_e1s, out_e1s = run_checker(E1)
    miss += predict("D2a", "exit 0 (silent)", fired(rc_w3s), rc_w3s == 0)
    miss += predict("D2b", "exit 0 (silent)", fired(rc_s1s), rc_s1s == 0)
    miss += predict("D2c", "exit 0 (extent TRUE)", fired(rc_e1s), rc_e1s == 0)
    print()
    print("        the same statement, in the same tree, one symlink away:")
    print("            w3_scope.py   %s" % fired(rc_w3s))
    print("            s1_extent.py  %s" % fired(rc_s1s))
    print("            e1_extents.py %s -- it CERTIFIES the extent as true"
          % fired(rc_e1s))
    print("        and neither printed extent mentions the file:")
    print("            named by w3_scope.py:  %s"
          % ("yes" if "slink" in out_w3s else "no"))
    print("            named by s1_extent.py: %s"
          % ("yes" if "slink" in out_s1s else "no"))
    print()

    # D2b MISSED, and the miss is the sharper result.  `s1_extent.py` exits 1
    # -- but NOT because it read the planted file.  Its SCAN is as blind as the
    # other two; what broke is control (c), which `shutil.copytree`s the tree
    # into a scratch dir and injects one statement.  `copytree` defaults to
    # `symlinks=False`, so it FOLLOWS the link and materialises `slink/leak.md`
    # as a real file in the copy -- where the same scan, now walking a real
    # directory, finds it.  The control expected `now + 1` and got `now + 2`.
    #
    # So the exit code is right for a reason that has nothing to do with the
    # extent, and the DIAGNOSIS a reader is handed is wrong: the run says the
    # injection control failed, not that a forbidden statement is live in the
    # tree.  These three numbers are what separate the two readings.
    asserted = next((l.strip() for l in out_s1s.splitlines()
                     if "still asserted at source" in l), "?")
    extent = next((l.strip() for l in out_s1s.splitlines()
                   if "code/species_7d75 " in l and "file(s) read" in l), "?")
    ctlc = next((l.strip() for l in out_s1s.splitlines()
                 if "injected into a scratch copy" in l), "?")
    print("        WHY s1_extent.py exits 1, which is NOT what D2b predicted")
    print("        and NOT the extent working:")
    print("            its own S1b verdict:   %s" % asserted)
    print("            its own extent line:   %s" % extent)
    print("            the row that failed:   %s" % ctlc)
    print("        The scan is blind.  Control (c) copytree()s the tree with")
    print("        `symlinks=False`, which FOLLOWS the link and materialises")
    print("        the planted file as a real one in the scratch copy, so the")
    print("        injection count came out one high.  A reader of that run is")
    print("        told the injection control is broken.  Nothing tells them a")
    print("        forbidden statement is live in `code/species_7d75`.")

    scan_blind = ("0 statement-occurrence(s) still asserted" in out_s1s
                  and "0 of them below the tree root" in out_s1s)
    if rc_w3s == 0 and rc_e1s == 0 and scan_blind:
        bad += 1
        print()
        print("  *** FINDING.  The F1 SHAPE SURVIVES THE REPAIR one rule to the")
        print("      side.  `EVERY REGULAR FILE ... AT ANY DEPTH` is still true")
        print("      only because no tree contains a symlinked directory.  All")
        print("      three walks are blind to it, E1 -- which walks the same")
        print("      way -- cannot disagree and certifies the extent TRUE, and")
        print("      the one non-zero exit comes from a control breaking for an")
        print("      unrelated reason and naming the wrong thing.  This is the")
        print("      sentence mg-821e wrote about `os.listdir`, with")
        print("      `followlinks` in place of recursion. ***")

    # D2d -- and the boundary of the finding, measured rather than asserted.
    # A symlink to a FILE is read, because `os.path.isfile` follows it.  So the
    # rule is precisely "symlinked DIRECTORY", which is what makes it a
    # directory rule and puts it beside `__pycache__` in the sentence that
    # names only `__pycache__`.
    leakfile = os.path.join(hidden, "leak.md")
    with Probe("D2d symlink to a FILE is followed") as pr:
        pr.symlink("code/species_7d75/slink.md", leakfile)
        rc_w3f, out_w3f = run_checker(W3)
    miss += predict("D2d", "exit 1 (followed)", fired(rc_w3f), rc_w3f == 1)
    print("        so the unstated rule is exactly `symlinked DIRECTORY`, not")
    print("        `symlink`: a linked FILE is read.  That is what makes it a")
    print("        DIRECTORY rule, and the extent line names one of those.")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
print()

# D2e -- does any printed extent mention it?
rc, out_w3c = run_checker(W3)
rc, out_s1c = run_checker(S1)
rc, out_e1c = run_checker(E1)
mentions = [n for n, o in (("w3_scope.py", out_w3c), ("s1_extent.py", out_s1c),
                           ("e1_extents.py", out_e1c))
            if "symlink" in o.lower() or "followlinks" in o.lower()]
miss += predict("D2e", "no extent mentions it",
                "%d of 3 mention it" % len(mentions), not mentions)
bad += bool(mentions)
print("        Three extents printed the word `__pycache__` and the phrase")
print("        `at any depth`.  None of the three printed `symlink`.  That is")
print("        the whole of the finding: the sentence is complete about the")
print("        rule somebody thought of.")
print()


print("=" * 78)
print("Q1 TOTAL BAD: %d" % bad)
print("Q1 PREDICTIONS MISSED: %d" % miss)
print("=" * 78)
print()
print("EXTENT OF THOSE NUMBERS.  Q1 measures the DEPTH claim of exactly three")
print("walks -- w3_scope.py's, s1_extent.py's and e1_extents.py's `regular()`")
print("-- by planting real files in the real worktree and RUNNING each")
print("checker.  It reads no walk and infers nothing from `os.walk` appearing")
print("in a source file.  It says nothing about the CONTENT of any extent")
print("beyond depth, nothing about the other two OPEN items, and nothing")
print("about any tree outside `code/species_7d75` and")
print("`code/species_repair_a4ef`, the two it plants in.  Q1 TOTAL BAD counts")
print("probes whose OUTCOME was wrong, not predictions that were wrong; the")
print("second number is separate on purpose, and D1i's miss is scored there")
print("and nowhere else.")
sys.exit(1 if bad else 0)
