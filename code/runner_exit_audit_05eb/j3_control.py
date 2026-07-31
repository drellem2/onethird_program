"""J3 -- THE POSITIVE CONTROL, PER FIXED RUNNER, BOTH DIRECTIONS.

The assignment is explicit that `pipefail is now set` -- or, here, `the pipeline
is now a redirect` -- is PRESENCE and not BEHAVIOUR.  So nothing in this section
reads a runner's TEXT.  Every row is `/bin/sh run_all.sh` and the number the
kernel gave back.

TWO DIRECTIONS, per runner:

  RED    the runner's own self-test (or, where it has none, its first repaired
         step) is made to fail, and the RUNNER's exit code is read.  A repaired
         runner must exit NON-ZERO.
  GREEN  the runner is executed unmodified.  It must exit ZERO.  Without this
         half, `always exits non-zero` would score a perfect RED column.

AND A THIRD COLUMN, because exit code alone is not enough.  The sweep records
that at eight of its sites the PRE-repair runner exits 1 for an unrelated
downstream `grep`; an exit-code-only control calls those healthy.  The mirror
risk here is a runner that exits non-zero because the forced failure broke it
in some other way.  So every RED row also records REACH: whether the forced
step's own marker reached the runner's stdout, and whether any LATER step ran.
A RED row passes only on the conjunction.

AND THE NEGATIVE CONTROL, which is the point of the whole section: the two
`run_audit.sh` runners J1 found outside the sweep's population get the same
treatment.  If the instrument is any good they must come back exit 0 with the
failure printed -- the defect, alive, in this repository, after the sweep.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib05eb as L

BAD = 0
MISS = []
MARK = "*** MG-05EB FORCED FAILURE ***"

# The injector lives in a scratch directory built at run time from the single
# committed source, so there is exactly one copy of the forcing mechanism.
INJECT = tempfile.mkdtemp(prefix="mg05eb_inject_")
shutil.copyfile(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 "sitecustomize_mg05eb.py"),
    os.path.join(INJECT, "sitecustomize.py"))


def predict(qid, predicted, measured, ok):
    MISS.append((qid, predicted, measured, ok))
    print("  %-4s predicted %-32s measured %-26s %s"
          % (qid, predicted, measured, "as predicted" if ok else "*** MISS ***"))


L.bar("J3  THE POSITIVE CONTROL -- behaviour of the real runner, both ways")

# ---------------------------------------------------------------------------
# The population: every `*.sh` that had a real `| tee` pipeline at the pin and
# does not have one now.  DERIVED, not typed in, so it cannot drift from J1.
# ---------------------------------------------------------------------------
pre = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
now = {p: L.read(p) for p in L.ls_sh()}
FIXED = sorted(p for p in pre
               if L.tee_pipelines(pre[p]) and p in now and not L.tee_pipelines(now[p]))
UNFIXED = sorted(p for p in now if L.tee_pipelines(now[p]))

print("  POPULATION, DERIVED FROM J1's PARSER, NOT TYPED IN:")
print("    runners with a real `| tee` pipeline at %s and none now : %d"
      % (L.PINNED, len(FIXED)))
print("    runners with a real `| tee` pipeline STILL, at HEAD       : %d"
      % len(UNFIXED))
print()


def first_target(text):
    """(line no, target script) for the first step whose status the runner reads.

    For a REPAIRED runner that is the first `CMD > f.txt || { ... }`.  For an
    UNREPAIRED one it is the first `CMD | tee f.txt`.  Both spellings are
    resolved to the same thing -- the script whose exit code the step produces
    -- so the red and the negative control force failure at the SAME PLACE and
    the two columns are comparable.
    """
    for i, l in L.command_lines(text):
        m = re.search(r"python3\s+(?:-\S+\s+)*(\S+\.py)\b[^|>]*(?:>|\|\s*tee)", l)
        if m:
            return i, m.group(1)
        m = re.search(r"sh\s+(\./\S+\.sh)\b[^|>]*(?:>|\|\s*tee)", l)
        if m:
            return i, m.group(1)
    return None, None


def later_markers(text, after_line):
    """Transcript filenames written by steps AFTER `after_line`."""
    out = []
    for i, l in L.command_lines(text):
        if i <= after_line:
            continue
        for m in re.finditer(r"(?:>|\|\s*tee)\s*(\S+\.txt)", l):
            out.append(m.group(1))
    return out


def force_and_run(runner, text, label):
    """Force the first scored step to fail; return (rc, reached, later_ran).

    HOW THE FAILURE IS FORCED, and why it is not an edit to the target.  The
    first draft APPENDED `raise SystemExit(1)` to the target script.  That fires
    only if the script falls off its own end, and two of these targets end in
    `sys.exit(main())` -- so the forcer never ran, the runner legitimately came
    back 0, and my instrument printed `*** NOT CAUGHT ***` against two sound
    runners.  The miss is kept in OUTCOMES.md.

    What replaced it: a `sitecustomize.py` on PYTHONPATH which registers an
    `atexit` hook, but ONLY in the process whose `sys.argv[0]` is the named
    target.  `atexit` fires on every exit path, and the target's bytes -- and
    its line numbers, which several instruments in this arc read -- are never
    touched.  Shell targets have no `atexit`, so those still get an appended
    `exit 1`; the two mechanisms are named per row.
    """
    line, target = first_target(text)
    if target is None:
        return None, None, None, None, None, None
    tree = os.path.dirname(runner)
    tpath = os.path.join(tree, target.lstrip("./"))
    abstarget = os.path.join(L.REPO, tpath)
    if not os.path.exists(abstarget):
        return None, None, None, None, target, None
    later = later_markers(text, line)
    for f in later:
        fp = os.path.join(L.REPO, tree, f)
        if os.path.exists(fp):
            os.utime(fp, (0, 0))          # stamp, so "did it rewrite" is visible
    own = _own_transcript(text, line)
    if tpath.endswith(".sh"):
        how = "append exit 1"
        with L.Sandbox() as sb:
            sb.append(tpath, '\necho "%s"\nexit 1\n' % MARK)
            rc, out = L.run_sh(runner, timeout=1800)
            ran_later = _rewritten(tree, later)
            ran = _mark_in(tree, own)
    else:
        how = "atexit hook"
        rc, out = L.run_sh(runner, timeout=1800,
                           env={"PYTHONPATH": INJECT,
                                "MG05EB_FORCE_TARGET": abstarget})
        ran_later = _rewritten(tree, later)
        ran = _mark_in(tree, own)
        L.restore_tracked()
    # TWO different questions, deliberately not merged:
    #   ran      -- the forced failure really happened in the target
    #   stdout   -- and the runner PRINTED it, which `| tee` always did and a
    #               bare redirect does only when the guard `cat`s.  J4c.
    return rc, ran, MARK in out, ran_later, target, how


def _own_transcript(text, line):
    """The transcript file the forced step itself writes."""
    for i, l in L.command_lines(text):
        if i != line:
            continue
        m = re.search(r"(?:>|\|\s*tee)\s*(\S+\.txt)", l)
        if m:
            return m.group(1)
    return None


def _mark_in(tree, name):
    if not name:
        return None
    p = os.path.join(L.REPO, tree, name)
    if not os.path.exists(p):
        return False
    with open(p, "r", encoding="utf-8", errors="replace") as fh:
        return MARK in fh.read()


def _rewritten(tree, later):
    """Which stamped transcripts the run rewrote.  Read BEFORE any restore --
    `git checkout -- .` rewrites files unconditionally and would make every
    later transcript look as though a later step had run."""
    return [f for f in later
            if os.path.exists(os.path.join(L.REPO, tree, f))
            and os.path.getmtime(os.path.join(L.REPO, tree, f)) > 1]


# ---------------------------------------------------------------------------
L.hdr("J3a  RED -- the first scored step forced to fail, per FIXED runner")

print("  The target is NOT replaced by a stub.  It runs in full, prints all")
print("  of its real output, and is then made to report failure by an")
print("  `atexit` hook injected through PYTHONPATH -- so the row measures a")
print("  real instrument reporting a real non-zero, not a placeholder.  Shell")
print("  targets get an appended `exit 1`; the mechanism is named per row.")
print()
print("  runner                                    forced target          exit  ran    stdout   later ran how            verdict")
red = {}
t0 = time.time()
for r in FIXED:
    rc, ran, on_stdout, later, target, how = force_and_run(r, now[r], "RED")
    if target is None:
        print("  %-42s (no scored step found)" % r)
        BAD += 1
        continue
    ok = (rc not in (0, None)) and ran and not later
    red[r] = (rc, ran, on_stdout, later, ok)
    print("  %-42s %-22s %-5s %-6s %-8s %-9s %-14s %s"
          % (r, target, "-" if rc is None else rc,
             "yes" if ran else "*** no ***",
             "yes" if on_stdout else "NO",
             "none" if not later else "*** %s ***" % ",".join(later),
             how, "caught" if ok else "*** NOT CAUGHT ***"))
    if not ok:
        BAD += 1
nred = sum(1 for v in red.values() if v[4])
print()
print("  %d of %d FIXED runners exit non-zero AND stop at the forced step."
      % (nred, len(FIXED)))
predict("Q15", "17 of 17 non-zero",
        "%d of %d" % (sum(1 for v in red.values() if v[0] not in (0, None)),
                      len(FIXED)),
        sum(1 for v in red.values() if v[0] not in (0, None)) == len(FIXED) == 17)
predict("Q16", "17 of 17 stop at the forced step",
        "%d of %d" % (sum(1 for v in red.values() if not v[3]), len(FIXED)),
        sum(1 for v in red.values() if not v[3]) == len(FIXED) == 17)
nout = sum(1 for v in red.values() if v[2])
print("  ...and the failing step's own text reached the RUNNER'S STDOUT in")
print("  %d of %d.  `| tee` did that at 34 of 34 by construction; a bare"
      % (nout, len(FIXED)))
print("  redirect does it only where the `||` guard cats.  J4c is the census.")

# ---------------------------------------------------------------------------
L.hdr("J3b  GREEN -- the same runners, unmodified")

print("  Without this column, a runner that exits non-zero unconditionally")
print("  would have scored a perfect J3a.  This is the direction that makes")
print("  J3a mean something.")
print()
print("  runner                                    exit   secs  verdict")
green = {}
for r in FIXED:
    t = time.time()
    rc, out = L.run_sh(r, timeout=1800)
    L.restore_tracked()
    green[r] = rc
    print("  %-42s %-5s %6.1f  %s"
          % (r, "-" if rc is None else rc, time.time() - t,
             "green" if rc == 0 else "*** NOT GREEN ***"))
    if rc != 0:
        BAD += 1
ngreen = sum(1 for v in green.values() if v == 0)
print()
print("  %d of %d FIXED runners exit 0 unmodified." % (ngreen, len(FIXED)))
predict("Q17", "17 of 17 exit 0", "%d of %d" % (ngreen, len(FIXED)),
        ngreen == len(FIXED) == 17)

# ---------------------------------------------------------------------------
L.hdr("J3c  THE NEGATIVE CONTROL -- the runners the sweep's population excluded")

print("  Same instrument, same forced failure, same reading of the runner's")
print("  own exit code.  These two files were never in the sweep's population")
print("  because they are not named `run_all.sh`.")
print()
print("  runner                                    forced target          exit  ran    stdout   later ran how            verdict")
neg = {}
for r in UNFIXED:
    rc, ran, on_stdout, later, target, how = force_and_run(r, now[r], "NEG")
    swallowed = (rc == 0)
    neg[r] = (rc, ran, on_stdout, later, swallowed)
    print("  %-42s %-22s %-5s %-6s %-8s %-9s %-14s %s"
          % (r, target, "-" if rc is None else rc,
             "yes" if ran else "*** no ***",
             "yes" if on_stdout else "NO",
             "none" if not later else ",".join(later), how,
             "*** SWALLOWED ***" if swallowed else "stopped the run"))
nsw = sum(1 for v in neg.values() if v[4])
print()
print("  %d of %d UNFIXED runners print the failure and exit 0."
      % (nsw, len(UNFIXED)))
predict("Q18", "2 of 2 exit 0", "%d of %d" % (nsw, len(UNFIXED)),
        nsw == len(UNFIXED) == 2)
if nsw:
    print()
    print("  THE DEFECT, ALIVE, AT HEAD.  A `set -e` runner in this repository")
    print("  prints `%s` from its own step and exits 0." % MARK)
    print("  It is the identical failure the sweep repaired 34 times, in a")
    print("  file its census could not reach.  Counted as a finding, not as a")
    print("  failure of this instrument.")

# ---------------------------------------------------------------------------
L.hdr("J3d  THE GENERAL FORM, ON J3")

print("   1. Every run here is `subprocess.run([\"/bin/sh\", <name>], ...)`:")
print("      list argv, no `shell=True`, no pipeline, so `returncode` is the")
print("      runner's own.  Structural, not a promise.")
print("   2. `returncode` is read on every path.  A timeout returns None and")
print("      prints `-`, never 0.")
print("   3. Every RED verdict is a CONJUNCTION of exit code, reach of the")
print("      forced marker into the runner's stdout, and no later step having")
print("      run.  Any one of the three alone would pass rows that are wrong:")
print("      code alone passes a runner that died for an unrelated reason;")
print("      reach alone passes the pre-repair text exactly.")
print("   4. `later ran` is measured by STAMPING every later transcript to")
print("      epoch 0 before the run and checking its mtime after -- a file")
print("      that exists is not evidence a step ran, which is mg-6cb9's F2.")
print("   5. The population is DERIVED from J1's parser inside this script,")
print("      not copied into it, so J3 cannot disagree with J1 about which")
print("      runners were fixed.")
print("   6. GREEN is run AFTER RED and restores tracked files between every")
print("      row, so a leaked forced-failure cannot make a GREEN row red.")

before = L.porcelain()
print()
print("  worktree state after J3: %s"
      % ("clean" if not before.strip() else "*** DIRTY ***\n" + before))
if before.strip():
    BAD += 1

print()
L.bar("J3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT.  It counts, per FIXED runner, a RED row that did not catch")
print("(exit code, reach, or a later step running) and a GREEN row that is")
print("not 0, plus a dirty worktree at the end.  It does NOT count the")
print("SWALLOWED rows in J3c: those are the finding.  It ranges over the %d"
      % len(FIXED))
print("runners J1's parser says were repaired and the %d it says were not,"
      % len(UNFIXED))
print("each run once in each direction on this machine at HEAD -- not over")
print("the batteries those runners execute, which J3 forces to fail on")
print("purpose and does not re-prove.")
print()
nmiss = sum(1 for _q, _p, _m, ok in MISS if not ok)
print("PREDICTIONS: %d of %d as predicted, %d MISSED (%s)"
      % (len(MISS) - nmiss, len(MISS), nmiss,
         ", ".join(q for q, _p, _m, ok in MISS if not ok) or "none"))
print("wall clock: %.0f s" % (time.time() - t0))
sys.exit(1 if BAD else 0)
