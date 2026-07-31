"""S2 -- READ THE STATUS THE PIPELINES THREW AWAY, over the corrected population.

mg-c2b3 settled its retroactive question by running all 34 tee'd targets
directly and reading the number the pipeline discarded: 34 of 34 exit 0.  That
is the right method and it is used again here, unchanged, on the members of the
property-defined population the sweep's filename never reached:

  * 8 `| tee` pipelines in `code/face_geometry_audit_f1b2/run_audit.sh` and
    `code/face_geometry_audit_fcf1/run_audit.sh` -- outside the NAME rule;
  * 3 `git diff ... | wc -c | tr -d ' '` SOURCE LINES in two `run_all.sh` --
    inside the name rule and outside the SHAPE rule -- which sit inside `for`
    loops and are 8 EXECUTIONS between them.

THE GRAIN, WHICH IS mg-dee4's F1.  This probe once said `11 of 11 read
directly`, and 11 was the number of SOURCE LINES.  A source line inside a loop
is N executions, not one; three hand-written argv covered four of the eight
runs; two of the three were the same command; and one row was labelled with a
line whose `':!*.md'` pathspec its argv did not have, so that form was never
executed in any shape.  The `git diff` rows are now DERIVED from the runners'
own bytes at the execution grain, exactly as the `| tee` rows always were, and
every count below says whether it is counting SITES or RUNS.

S2a reads 8 tee executions and 8 `git diff` executions.  S2a2 computes the byte
counts `OUTCOMES.md` said were `verified`, on both mechanisms, because until
mg-70c7 no probe in this tree computed one.  S2b and S2c are the positive
control in BOTH directions on
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

# The `git diff | wc -c` pipelines: the discarded stage is the `git diff`
# itself, so that is what gets run and read.
#
# mg-70c7, ON THE GRAIN.  This used to be a HAND-LIST of three argv, one per
# SOURCE LINE, and mg-dee4's F1 is what a hand-list costs.  The three lines sit
# inside `for pair in …` loops and execute EIGHT `git diff`s between them, so
# three argv covered four of eight runs; two of the three argv were the same
# command; and the row labelled `state_delegation_audit_16eb/run_all.sh:39`
# carried an argv WITHOUT the `':!*.md'` pathspec that line 39 has, so that
# form was never executed in any shape and a row was labelled with a line it
# did not run.  The list is now DERIVED from the runners' own bytes at the pin:
# the loop header expands to its literal items, the body's `base=${pair%% *}`
# assignments are followed, and the argv is built by `lib7522.argv_of`, which
# returns None rather than leaving an unresolved `$` in a command it is about
# to run.  A row set that cannot drift from the source is the same property the
# `| tee` half already had.
GITROWS = []
NOT_DERIVABLE = []
for _runner in ("code/state_delegation_audit_16eb/run_all.sh",
                "code/state_delegation_repair_0049/run_all.sh"):
    _pre = L.read(_runner, L.PINNED)
    _rows = []
    for _line, _it, _bind, _text in L.pipeline_executions(_pre):
        _stage = L.discarded_stages(_text)[0]
        _argv = L.argv_of(_stage, _bind) if _bind is not None else None
        if _argv is None:
            NOT_DERIVABLE.append((_runner, _line, _stage.strip()))
            continue
        _rows.append((_runner, _line, _it, _argv))
    # IN RUNTIME ORDER -- iteration first, then line within the iteration.
    # `pipeline_executions` returns rows grouped by SOURCE LINE, which is the
    # right grain and the wrong sequence: the loop runs line 38 and line 39 of
    # pair 1 before line 38 of pair 2.  Printing the grouped order under a
    # sentence about what the runner did would be a third version of the same
    # defect -- a true set of rows in an order nothing executed.
    GITROWS.extend(sorted(_rows, key=lambda r: (r[2], r[1])))

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

for runner, n, it, cmd in GITROWS:
    t0 = time.time()
    code, out = L.run_argv(cmd, L.REPO, timeout=TIMEOUT)
    dt = time.time() - t0
    verdict = ("nothing was being swallowed" if code == 0
               else "*** NON-ZERO -- a status the pipeline hid ***")
    if code != 0:
        nonzero.append((runner, n, cmd[0], code))
    print("  %-42s %-24s %6s %7.1f  %s"
          % (runner.replace("code/", "") + ":%d#%d" % (n, it),
             "git diff " + cmd[2].split("..")[0],
             "-" if code is None else code, dt, verdict))

print()
if NOT_DERIVABLE:
    BAD += len(NOT_DERIVABLE)
    print("  *** %d pipeline execution(s) could not be derived from the source"
          % len(NOT_DERIVABLE))
    for r, n, s in NOT_DERIVABLE:
        print("      %s:%d  %s" % (r, n, s))
    print("      A row that cannot be derived must not be hand-written; that")
    print("      is mg-dee4's F1 and this is where it would come back. ***")
    print()

# THE GRAIN IS IN THE SENTENCE.  mg-dee4's F1: `11 of 11 read directly` was a
# count of SOURCE LINES presented as a count of RUNS, and the two are
# indistinguishable in a report that does not say which it is at.
_lines = len({(r, n) for r, n, _i, _c in GITROWS})
print("  GRAIN.  These are EXECUTIONS, not source lines, and the difference is")
print("  the whole of mg-dee4's F1:")
print()
print("      `| tee` pipeline SITES, derived from the runners' bytes  %3d"
      % len(ROWS))
print("      `| tee` EXECUTIONS (none of them is inside a loop)       %3d"
      % len(ROWS))
print("      `git diff` pipeline SOURCE LINES                         %3d"
      % _lines)
print("      `git diff` EXECUTIONS (those lines sit in `for` loops)   %3d"
      % len(GITROWS))
print("      ---------------------------------------------------------")
print("      DISCARDED STATUSES READ DIRECTLY HERE                    %3d"
      % (len(ROWS) + len(GITROWS)))
print()
print("  So the corrected population is mg-c2b3's 34 -- INHERITED from its")
print("  transcript at the SITE grain and not re-run here -- plus the %d"
      % (len(ROWS) + len(GITROWS)))
print("  executions above, which ARE run here.  `%d of %d` is a statement about"
      % (len(ROWS) + len(GITROWS), len(ROWS) + len(GITROWS)))
print("  RUNS; `34 of 34` is a statement about SITES; and the two are not")
print("  added into one number, because a source line inside a loop is N")
print("  executions and an enumeration of sites cannot support a claim about")
print("  runs.")
print()
if nonzero:
    BAD += len(nonzero)
    print("  *** %d discarded status is non-zero TODAY ***" % len(nonzero))
    for r, n, s, c in nonzero:
        print("      %s:%d  %s -> %d" % (r, n, s, c))
else:
    print("  %d of %d EXECUTIONS exit 0.  THE RETROACTIVE CLEARANCE NOW COVERS"
          % (len(ROWS) + len(GITROWS), len(ROWS) + len(GITROWS)))
    print("  THE CORRECTED POPULATION AT THE GRAIN IT RUNS AT, not only the")
    print("  filename-defined one and not only its source lines.")
    print()
    print("  WHAT THIS DOES NOT ESTABLISH, stated rather than omitted: the")
    print("  same fact at every intermediate commit.  It is read at HEAD, on")
    print("  this machine, and the rows say so.  And mg-c2b3's own 34 are")
    print("  CITED, not re-measured, so the covered set is `%d run by me +"
          % (len(ROWS) + len(GITROWS)))
    print("  34 inherited from a transcript I did not re-run`.")

# ---------------------------------------------------------------------------
L.hdr("S2a2  THE WORD `verified` -- THE BYTE COUNTS, COMPUTED ON BOTH ARMS")

print("  `OUTCOMES.md` says the repaired `wc -c < FILE` counts the same bytes")
print("  the pipeline did, `verified against the pre-repair output")
print("  (0 / 0 / 0 / 0 / 2111 / 0, unchanged)`.  `verified` is one of the")
print("  markers this tree's own general form names, and until mg-70c7 NO")
print("  probe here computed a byte count: the figure stood on the word.")
print("  Both arms are computed below, on the same derived executions.")
print()
print("  TWO MECHANISMS, ONE INPUT.  The PIPELINE arm is the byte length of")
print("  the command's stdout STREAM, which is what `| wc -c` reported.  The")
print("  REDIRECT arm writes that stdout to a real file and reads the file's")
print("  size, which is what `wc -c < FILE` reports.  Same derived argv, two")
print("  different paths to the number, and the claim is that they agree.")
print()
print("  %-46s %9s %9s  %s"
      % ("execution", "pipeline", "redirect", "verdict"))
by_runner = {}
disagree = 0
_scratch = os.path.join(INJECT, "_bytes.tmp")
for runner, n, it, cmd in GITROWS:
    _c, out = L.run_argv(cmd, L.REPO, timeout=TIMEOUT)
    pipe_n = len(out.encode("utf-8"))
    with open(_scratch, "wb") as fh:
        p = subprocess.run(cmd, cwd=L.REPO, stdout=fh,
                           stderr=subprocess.DEVNULL, timeout=TIMEOUT)
    redir_n = os.path.getsize(_scratch)
    ok = pipe_n == redir_n and p.returncode == 0
    disagree += 0 if ok else 1
    by_runner.setdefault(runner, []).append(redir_n)
    print("  %-46s %9d %9d  %s"
          % (runner.replace("code/", "") + ":%d#%d" % (n, it), pipe_n, redir_n,
             "AGREE" if ok else "*** DISAGREE ***"))
try:
    os.unlink(_scratch)
except OSError:
    pass
print()
for runner, vals in sorted(by_runner.items()):
    print("      %-46s %s" % (runner.replace("code/", ""),
                              " / ".join(str(v) for v in vals)))
print()
print("  THOSE EIGHT VALUES ARE THIS TRANSCRIPT'S, not a figure in prose.")
print("  They move if any of the three predecessor directories is ever")
print("  edited, so `OUTCOMES.md` points here instead of quoting them --")
print("  a number that moves belongs in a transcript, which is this tree's")
print("  own rule and mg-dee4's F2 is where it was not applied.")
print()
print("  OUTCOMES.md's parenthesis listed the SIX values of")
print("  state_delegation_audit_16eb and not the two of")
print("  state_delegation_repair_0049.  Both runners are printed above,")
print("  because a figure covering 6 of 8 under the words `the byte counts`")
print("  is the same shape as `11 of 11` covering 4 of 8.")
print()
print("  EXTENT.  Both arms are computed HERE, in Python, from the same")
print("  derived argv -- so what is checked is that a stream count and a file")
print("  count of the same output agree, and NOT that the `wc` binary in the")
print("  runner produces either of them.  That limit is stated because a")
print("  stated limit is checkable and an absence is not.")
if disagree:
    BAD += disagree
    print("  *** %d byte count disagreed between the two arms ***" % disagree)

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
