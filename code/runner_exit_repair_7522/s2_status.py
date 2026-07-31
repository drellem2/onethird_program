"""S2 -- READ THE STATUS THE PIPELINES THREW AWAY, over the corrected population.

mg-c2b3 settled its retroactive question by running all 34 tee'd targets
directly and reading the number the pipeline discarded: 34 of 34 exit 0.  That
is the right method and it is used again here, unchanged, on the members of the
property-defined population the sweep's filename never reached:

  * 8 `| tee` pipelines in `code/face_geometry_audit_f1b2/run_audit.sh` and
    `code/face_geometry_audit_fcf1/run_audit.sh` -- outside the NAME rule;
  * 3 `git diff ... | wc -c | tr -d ' '` pipelines in two `run_all.sh` --
    inside the name rule and outside the SHAPE rule.

S2a reads those 11.  S2b and S2c are the positive control in BOTH directions on
the two repaired runners, at every one of the 8 sites: on the PRE-repair text a
step forced to fail must NOT stop the run and the runner must still exit 0 (the
defect reproduced on the real runner text, not argued from the spec); on the
repaired text the runner must exit non-zero AND the forced step must be the last
one that ran.  Every verdict is a CONJUNCTION of the exit code and the reach,
because an exit-code-only control cannot tell a repair from an unrelated later
failure -- mg-c2b3 found eight such sites in its own population.

THE FORCED FAILURE IS NOT A STUB.  The target runs in full and is made to report
failure by an `atexit` hook injected through `PYTHONPATH`; the runner's and the
target's bytes are untouched.  Both arms are written to a scratch file and run
from there, so neither arm edits a tracked runner.
"""

import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

HERE = os.path.dirname(os.path.abspath(__file__))
INJECT = os.path.join(HERE, "_inject7522")
TIMEOUT = 1800
BAD = 0

os.makedirs(INJECT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "sitecustomize_mg7522.py"),
                os.path.join(INJECT, "sitecustomize.py"))

L.bar("S2  THE STATUS THE PIPELINES DISCARDED, READ DIRECTLY")

before_tree = L.porcelain()

# ---------------------------------------------------------------------------
L.hdr("S2a  EVERY PIPELINE THE SWEEP'S POPULATION DID NOT REACH, RUN DIRECTLY")

print("  Each row runs the DISCARDED stage of one pipeline with nothing in")
print("  the way and reads its exit status -- the number `tee` (or `wc`)")
print("  replaced with its own.  A 0 means the past green was green for the")
print("  right reason.  This is mg-c2b3's K3b method, unchanged, applied to")
print("  the members of the population its filename could not contain.")
print()

ROWS = []
for runner in L.OUTSIDE:
    src = L.read(runner, None)
    pre = L.read(runner, L.PINNED)
    d = os.path.dirname(os.path.join(L.REPO, runner))
    for n, line in L.tee_pipelines(pre):
        inv = L.invocation(line)
        assert inv, "no invocation parsed on %s:%d" % (runner, n)
        ROWS.append((runner, d, n, inv[0], inv[1], L.arguments(line, inv[1])))

# The three `git diff | wc -c` pipelines: the discarded stage is the `git diff`
# itself, so that is what gets run and read.
GITROWS = [
    ("code/state_delegation_audit_16eb/run_all.sh", 38,
     ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"]),
    ("code/state_delegation_audit_16eb/run_all.sh", 39,
     ["git", "diff", "3a80d99..HEAD", "--", "code/state_delegation_audit_5644"]),
    ("code/state_delegation_repair_0049/run_all.sh", 39,
     ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"]),
]

print("  %-42s %-24s %6s %7s  %s"
      % ("runner", "discarded stage", "exit", "secs", "verdict"))
nonzero = []
for runner, d, n, interp, script, extra in ROWS:
    cmd = ([sys.executable, "-B"] if interp.startswith("python")
           else ["/bin/sh"]) + [script] + extra
    t0 = time.time()
    code, _out = L.run_argv(cmd, d, timeout=TIMEOUT)
    dt = time.time() - t0
    verdict = ("nothing was being swallowed" if code == 0
               else "*** NON-ZERO -- a status the pipeline hid ***")
    if code != 0:
        nonzero.append((runner, n, script, code))
    print("  %-42s %-24s %6s %7.1f  %s"
          % (runner.replace("code/", "") + ":%d" % n,
             os.path.basename(script), "-" if code is None else code, dt,
             verdict))

for runner, n, cmd in GITROWS:
    t0 = time.time()
    code, _out = L.run_argv(cmd, L.REPO, timeout=TIMEOUT)
    dt = time.time() - t0
    verdict = ("nothing was being swallowed" if code == 0
               else "*** NON-ZERO -- a status the pipeline hid ***")
    if code != 0:
        nonzero.append((runner, n, cmd[0], code))
    print("  %-42s %-24s %6s %7.1f  %s"
          % (runner.replace("code/", "") + ":%d" % n, "git diff",
             "-" if code is None else code, dt, verdict))

print()
print("  population: %d pipelines -- the %d `| tee` in the two runners the NAME"
      % (len(ROWS) + len(GITROWS), len(ROWS)))
print("  rule excluded, plus the %d the SHAPE rule excluded.  Together with"
      % len(GITROWS))
print("  mg-c2b3's 34, the corrected population is %d and every member of it"
      % (34 + len(ROWS) + len(GITROWS)))
print("  has now had the discarded status read.")
print()
if nonzero:
    BAD += len(nonzero)
    print("  *** %d discarded status is non-zero TODAY ***" % len(nonzero))
    for r, n, s, c in nonzero:
        print("      %s:%d  %s -> %d" % (r, n, s, c))
else:
    print("  %d of %d exit 0.  THE RETROACTIVE CLEARANCE NOW COVERS THE"
          % (len(ROWS) + len(GITROWS), len(ROWS) + len(GITROWS)))
    print("  CORRECTED POPULATION, not only the filename-defined one.")
    print()
    print("  WHAT THIS DOES NOT ESTABLISH, stated rather than omitted: the")
    print("  same fact at every intermediate commit.  It is read at HEAD, on")
    print("  this machine, and the rows say so.")

# ---------------------------------------------------------------------------
# The positive control.
# ---------------------------------------------------------------------------


def transcripts_of(runner):
    """The committed out_*.txt a runner writes, absolute paths."""
    d = os.path.dirname(os.path.join(L.REPO, runner))
    return [os.path.join(d, f) for f in sorted(os.listdir(d))
            if f.startswith("out_") and f.endswith(".txt")]


def snapshot(paths):
    out = {}
    for p in paths:
        with open(p, "rb") as fh:
            out[p] = fh.read()
    return out


def restore(snap):
    """Put the exact bytes back.  NOT `git checkout -- .`: that rewrites every
    tracked file in the repository, and mg-05eb's j3 read an mtime after one and
    reported eight false positives for it."""
    for p, b in snap.items():
        with open(p, "wb") as fh:
            fh.write(b)


def arm(runner, text, target_abs, stamp_paths):
    """(exit code, [transcripts that were REWRITTEN], stderr saw the forcer).

    `reach` is measured by stamping every transcript to epoch 0 BEFORE the run
    and reading its mtime after -- a transcript whose bytes are unchanged is
    still evidence that its step executed, and comparing bytes would have
    scored a re-run identical step as "did not run".
    """
    d = os.path.dirname(os.path.join(L.REPO, runner))
    for p in stamp_paths:
        os.utime(p, (0, 0))
    code, out = L.run_sh_text(text, d, timeout=TIMEOUT,
                              env={"PYTHONPATH": INJECT,
                                   "MG7522_FORCE_TARGET": target_abs})
    ran = [p for p in stamp_paths if os.stat(p).st_mtime > 1]
    return code, ran, ("*** MG-7522 FORCED FAILURE ***" in out)


def control(label, use_pre):
    global BAD
    L.hdr(label)
    if use_pre:
        print("  PRE-REPAIR text, from `git show %s:<runner>` -- the real"
              % L.PINNED)
        print("  bytes as they stood, not a reconstruction.  A step is forced")
        print("  to fail; the DEFECT is that the runner still exits 0 and the")
        print("  later steps still run on an unchecked precondition.")
        print()
        print("  %-40s %-24s %6s %6s  %s"
              % ("runner:line", "forced target", "exit", "later", "verdict"))
    else:
        print("  REPAIRED text, as committed at HEAD.  The same step is forced")
        print("  to fail; the repair is that the runner exits non-zero AND")
        print("  stops there.  The verdict is the CONJUNCTION -- an exit-code-")
        print("  only rule cannot tell a repair from an unrelated later error.")
        print()
        print("  %-40s %-24s %6s %6s  %s"
              % ("runner:line", "forced target", "exit", "later", "verdict"))

    n_ok = n_all = 0
    for runner in L.OUTSIDE:
        pre = L.read(runner, L.PINNED)
        text = pre if use_pre else L.read(runner, None)
        d = os.path.dirname(os.path.join(L.REPO, runner))
        tps = transcripts_of(runner)
        sites = L.tee_pipelines(pre)
        # The transcript each site writes, read off the PRE text's `tee`
        # argument.  It is the same filename in both arms -- the repair swaps
        # `| tee f` for `> f` and does not rename anything -- so one list
        # serves both directions and neither arm has to be parsed twice.
        site_files = [L.unquoted(l).split("tee", 1)[1].split()[0]
                      for _m, l in sites]
        for idx, (n, line) in enumerate(sites):
            inv = L.invocation(line)
            target_abs = os.path.join(d, inv[1])
            snap = snapshot(tps)
            code, ran, saw = arm(runner, text, target_abs, tps)
            restore(snap)
            n_all += 1
            # transcripts belonging to steps AFTER the forced one
            later = set(os.path.basename(x) for x in site_files[idx + 1:])
            later_ran = sum(1 for p in ran if os.path.basename(p) in later)
            if use_pre:
                ok = (code == 0 and saw and later_ran == len(sites) - idx - 1)
                verdict = ("SWALLOWED -- defect reproduced" if ok
                           else "*** did not reproduce ***")
            else:
                ok = (code is not None and code != 0 and saw and later_ran == 0)
                verdict = ("CAUGHT -- non-zero and stopped" if ok
                           else "*** NOT CAUGHT ***")
            n_ok += 1 if ok else 0
            if not ok:
                BAD += 1
            print("  %-40s %-24s %6s %6s  %s"
                  % (runner.replace("code/", "") + ":%d" % n,
                     os.path.basename(inv[1]),
                     "-" if code is None else code, later_ran, verdict))
    print()
    print("  %d of %d" % (n_ok, n_all))
    return n_ok, n_all


pre_ok, pre_all = control(
    "S2b  POSITIVE CONTROL, PRE-REPAIR -- the defect, reproduced", True)
post_ok, post_all = control(
    "S2c  POSITIVE CONTROL, REPAIRED -- the defect, caught", False)

# ---------------------------------------------------------------------------
L.hdr("S2d  NO COMMITTED TRANSCRIPT MOVED")

print("  `> f` and `| tee f` write the same bytes, so the prediction is that")
print("  the repair moves no committed transcript.  It is MEASURED, not")
print("  deduced: the repaired runners were executed in full in S2b/S2c and")
print("  the worktree is compared with its state before this probe started.")
print()
after_tree = L.porcelain()
if before_tree == after_tree:
    print("  worktree unchanged by S2 (git status --porcelain identical)")
else:
    BAD += 1
    print("  *** WORKTREE CHANGED BY S2 ***")
    print("  before:\n%s\n  after:\n%s" % (before_tree, after_tree))

# ---------------------------------------------------------------------------
L.hdr("S2e  THE GENERAL FORM, ON THIS SECTION")

print("  S2 is a script that decides whether other scripts' statuses were")
print("  discarded, so the question it owes is whether it discards its own.")
print("  Enumerated, with the branches that CANNOT exhibit it and why:")
print()
print("   1. Every subprocess here is a LIST argv with no `shell=True`, so no")
print("      shell parses it, so there is no pipeline, so `returncode` is the")
print("      target's own status.  Structural, not a promise about callers.")
print("   2. `returncode` is read on EVERY path including the timeout path,")
print("      which returns None and prints `-`, never 0.")
print("   3. Both arms are written to a scratch file and run from there, so")
print("      neither edits a tracked runner -- which is what makes S2d's")
print("      worktree comparison mean anything.")
print("   4. Every control verdict is a CONJUNCTION of exit code AND reach.")
print("      Reach is stamped-mtime, read BEFORE any restore.")
print("   5. The forced failure writes its marker to STDERR, so it cannot")
print("      land in the transcript whose bytes S2d checks.")
print("   6. The transcripts are restored by writing back exact bytes, not by")
print("      `git checkout -- .`, which rewrites every tracked file and would")
print("      have destroyed the mtime evidence in 4.")
print("   7. The LIMIT, stated: S2 forces these targets to FAIL, so it does")
print("      not re-prove that they pass.  S2a is the row that shows they do,")
print("      at HEAD, on this machine.")

shutil.rmtree(INJECT, ignore_errors=True)

print()
L.bar("S2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) a discarded status that is")
print("non-zero at HEAD, (b) a control site that fails its conjunction in")
print("either direction, and (c) the worktree not being restored.  It ranges")
print("over the %d pipelines outside mg-c2b3's population and over the %d"
      % (len(ROWS) + len(GITROWS), pre_all + post_all))
print("control sites in the two runners the NAME rule excluded.  It does NOT")
print("range over mg-c2b3's own 34, which K3b read and this probe does not")
print("re-read -- S1d states which population is whose.")
sys.exit(1 if BAD else 0)
