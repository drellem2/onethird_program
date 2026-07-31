"""A5 -- THE FLOOR: ONE THING NO LIST IN THE TICKET NAMES.

The ticket names four targets.  This is the fifth, chosen because it is the
one consequence of mg-7522 that nothing in the ticket, in mg-7522's README or
in its OUTCOMES.md asks about:

    mg-7522 EDITED THE INSTRUMENT THAT mg-05eb CITES, AND DELIBERATELY DID NOT
    RE-RUN IT.

`libc2b3.PIPEFAIL_RE` was changed, `k1_census.py`'s docstring was rewritten,
`k2_consume.py`'s caller scan was rewritten, `selftestc2b3.py` gained three
rows, and both `run_audit.sh` runners were rewritten -- 63 changed lines of
shell between them.  The committed transcripts were left as they were, with a
stated and correct reason: a transcript is the record of a run at a time.

The consequence nobody checked is that those files are now UNVERIFIED CODE.
Their transcripts no longer describe them, so a break in them is silent.  This
probe runs them.

  A5a  mg-c2b3's own probes, run at HEAD against the repaired library.
  A5b  the `pipefail` figure, re-derived by the SUBJECT's own instrument --
       does `k1_census.py` now print AGREES where its committed transcript
       prints DIFFERS?
  A5c  the two rewritten runners, run at HEAD, exit code read.
  A5d  the repaired runners under the SAME positive control mg-7522 used:
       does the repair still stop the run?  Checked on one site rather than
       eight, and the narrowing is stated.

Every exit code below was predicted in PREDICTIONS.md before this file ran.
"""

import os
import re
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
FINDINGS = []
HERE = os.path.dirname(os.path.abspath(__file__))
C2B3 = os.path.join(L.REPO, "code/runner_exit_c2b3")
TIMEOUT = 1500

L.bar("A5  THE INSTRUMENT MG-7522 EDITED UNDER MG-05EB'S CITATIONS")

before = L.porcelain()

# ---------------------------------------------------------------------------
L.hdr("A5a  MG-C2B3'S OWN PROBES, RUN AT HEAD AGAINST THE REPAIRED LIBRARY")

print("  POPULATION, named: every `*.py` in `code/runner_exit_c2b3/` that")
print("  mg-7522's commit touched, plus that tree's self-test.  Derived from")
print("  `git show --name-only %s`, not hand-listed." % L.REPAIR)
print()
touched = [p for p in L.git("show", "--name-only", "--format=", L.REPAIR).split()
           if p.startswith("code/runner_exit_c2b3/") and p.endswith(".py")]
targets = sorted(set(touched) | {"code/runner_exit_c2b3/selftestc2b3.py"})
for p in targets:
    print("      %s" % p)
print()
print("    %-32s %-6s %-8s %s" % ("probe", "exit", "secs", "verdict"))
results = {}
for p in targets:
    if not L.exists(p, None):
        continue
    t0 = time.time()
    code, out = L.run_argv([sys.executable, "-B", os.path.basename(p)], C2B3,
                           timeout=TIMEOUT)
    dt = time.time() - t0
    results[p] = (code, out)
    ok = code == 0
    if not ok:
        BAD += 1
        FINDINGS.append("A5a %s exits %s at HEAD after mg-7522's edits"
                        % (p, L.code_str(code)))
    print("    %-32s %-6s %-8.1f %s"
          % (os.path.basename(p), L.code_str(code), dt,
             "runs clean" if ok else "*** does not exit 0 ***"))
    if not ok:
        for l in out.strip().split("\n")[-6:]:
            print("          %s" % l[:70])
print()
print("  WHY THIS IS WORTH A SECTION.  mg-7522 changed these files and left")
print("  their transcripts alone, correctly.  The side effect is that the")
print("  code has no current record: a break in it would show up nowhere")
print("  until someone ran it.  Someone has now run it.")

# ---------------------------------------------------------------------------
L.hdr("A5b  THE `pipefail` FIGURE, RE-DERIVED BY THE SUBJECT'S OWN INSTRUMENT")

print("  mg-05eb's OPEN 2: `out_k1_census.txt` prints")
print("      setting pipefail   ticket 1   re-derived 0   DIFFERS")
print("  while four artifacts said `1, confirmed exactly`.  mg-7522 repaired")
print("  `libc2b3.PIPEFAIL_RE` and did not regenerate the transcript.  So the")
print("  row is read out of the LIVE run above and set beside the committed")
print("  one.")
print()
K1 = "code/runner_exit_c2b3/k1_census.py"
live = results.get(K1, (None, ""))[1]
committed = L.read("code/runner_exit_c2b3/out_k1_census.txt", None)


def pipefail_row(text):
    for l in text.split("\n"):
        if "pipefail" in l and ("DIFFERS" in l or "AGREES" in l):
            return l.strip()
    return None


lr, cr = pipefail_row(live), pipefail_row(committed)
print("      committed transcript : %s" % (cr or "(row not found)"))
print("      live run at HEAD     : %s" % (lr or "(row not found)"))
print()
if lr and "AGREES" in lr and cr and "DIFFERS" in cr:
    print("  THE REPAIR IS REAL AND IT IS VISIBLE IN THE SUBJECT'S OWN")
    print("  INSTRUMENT.  The regex now matches `set -euo pipefail`, the")
    print("  re-derived figure is 1, and the row that mg-05eb found DIFFERS")
    print("  reads AGREES on a run that nobody committed.  This is the")
    print("  strongest confirmation available for OPEN 2 and it is positive.")
elif lr is None:
    BAD += 1
    FINDINGS.append("A5b the `pipefail` row is absent from a live k1_census run")
    print("  *** the row is not in the live output ***")
else:
    BAD += 1
    FINDINGS.append("A5b the live `pipefail` row reads `%s`; the committed one "
                    "reads `%s`" % (lr, cr))
    print("  *** the two do not stand in the expected relation ***")

# ---------------------------------------------------------------------------
L.hdr("A5c  THE TWO REWRITTEN RUNNERS, RUN AT HEAD")

print("  mg-7522 rewrote 63 lines of shell across these two files to remove")
print("  8 `| tee` pipelines.  A rewrite that removes a pipeline can also")
print("  remove a step.  Both are run whole and their exit codes read.")
print()
RUNNERS = ("code/face_geometry_audit_f1b2/run_audit.sh",
           "code/face_geometry_audit_fcf1/run_audit.sh")
def steps_of(runner_rel):
    """[(target script, redirect file)] for each python step of a runner.

    REACH IS MEASURED FROM THE REDIRECT TARGET, not from the run's stdout.
    The repair's whole shape is `python3 x.py > out_x.txt || { ...; exit 1; }`,
    so the target's name never appears on the runner's stdout and a rule that
    looked for it would score every step as unreached -- and then a forced
    failure would look like a stopped run for the wrong reason.  The first
    draft of this probe did exactly that; it is recorded in OUTCOMES.md.
    """
    out = []
    for _i, s in L.command_lines(L.read(runner_rel, None)):
        inv = L.invocation(s)
        if not inv or not inv[0].startswith("python"):
            continue
        m = re.search(r">\s*([\w.-]+)", L.unquoted(s))
        out.append((inv[1], m.group(1) if m else None))
    return out


def mtimes(d, files):
    return {f: (os.path.getmtime(os.path.join(d, f))
                if f and os.path.exists(os.path.join(d, f)) else None)
            for f in files}


print("    %-46s %-6s %-8s %s" % ("runner", "exit", "secs", "steps reached"))
for r in RUNNERS:
    d = os.path.dirname(os.path.join(L.REPO, r))
    steps = steps_of(r)
    before_m = mtimes(d, [f for _s, f in steps])
    t0 = time.time()
    code, out = L.run_argv(["/bin/sh", os.path.basename(r)], d,
                           timeout=TIMEOUT)
    dt = time.time() - t0
    after_m = mtimes(d, [f for _s, f in steps])
    reached = len([1 for f in before_m if after_m[f] != before_m[f]])
    ok = code == 0 and reached == len(steps)
    if not ok:
        BAD += 1
        FINDINGS.append("A5c %s exits %s at HEAD with %d of %d steps reached"
                        % (r, L.code_str(code), reached, len(steps)))
    print("    %-46s %-6s %-8.1f %d of %d"
          % (r, L.code_str(code), dt, reached, len(steps)))
    if not ok:
        for l in out.strip().split("\n")[-8:]:
            print("          %s" % l[:70])
print()
print("  `steps reached` is a CONJUNCTION with the exit code, for the same")
print("  reason mg-7522 gives: an exit-code-only check cannot tell a repair")
print("  from a run that stopped early for an unrelated reason.  Reach is")
print("  read from the mtime of each step's REDIRECT TARGET, because the")
print("  repaired shape sends every step's output to a file and the target's")
print("  name never reaches the runner's stdout.")

# ---------------------------------------------------------------------------
L.hdr("A5d  DOES THE REPAIR STILL STOP THE RUN?  ONE SITE, AND SAID SO")

print("  mg-7522's S2c drives all 8 sites in both directions.  This is ONE")
print("  site on ONE runner -- a spot check, not a re-run of that control,")
print("  and the narrowing is stated here rather than left for a reader to")
print("  infer from a bare `PASS`.  The forced failure is an `atexit` hook")
print("  injected through `PYTHONPATH`; no tracked byte is edited.")
print()
INJECT = os.path.join(HERE, "_inject_dee4")
os.makedirs(INJECT, exist_ok=True)
with open(os.path.join(INJECT, "sitecustomize.py"), "w") as fh:
    fh.write(
        "import atexit, os, sys\n"
        "T = os.environ.get('DEE4_FORCE', '')\n"
        "def _f():\n"
        "    if T and T in ' '.join(sys.argv):\n"
        "        os._exit(3)\n"
        "atexit.register(_f)\n")
R = "code/face_geometry_audit_f1b2/run_audit.sh"
d = os.path.dirname(os.path.join(L.REPO, R))
steps = steps_of(R)
first = steps[0][0]
print("      runner            %s" % R)
print("      forced target     %s  (the FIRST python step, so a repair that" % first)
print("                        stops the run leaves every later step unrun)")
before_m = mtimes(d, [f for _s, f in steps])
env = {"PYTHONPATH": INJECT, "DEE4_FORCE": first}
code, out = L.run_argv(["/bin/sh", os.path.basename(R)], d, timeout=TIMEOUT,
                       env=env)
after_m = mtimes(d, [f for _s, f in steps])
later = [f for _s, f in steps[1:] if after_m[f] != before_m[f]]
print("      exit code         %s" % L.code_str(code))
print("      later steps that still ran   %d of %d" % (len(later), len(steps) - 1))
ok = code not in (0, None) and not later
if ok:
    print("      -> NON-ZERO AND STOPPED.  The repair holds on this site.")
else:
    BAD += 1
    FINDINGS.append(
        "A5d %s: forcing %s to fail gives exit %s with %d later step(s) still "
        "run -- the repair does not stop the run at this site"
        % (R, first, L.code_str(code), len(later)))
    print("      *** exit %s with %d later step(s) still run ***"
          % (L.code_str(code), len(later)))
shutil.rmtree(INJECT, ignore_errors=True)

# ---------------------------------------------------------------------------
L.hdr("A5e  THE WORKTREE IS AS IT WAS")

after = L.porcelain()
same = before == after
print("      `git status --porcelain` identical before and after: %s" % same)
print()
print("  AND THAT IS A RESULT, not only a hygiene check: A5c re-ran both")
print("  runners whole and A5d re-ran one of them under a forced failure, so")
print("  every `out_*.txt` those runners write was rewritten.  The worktree")
print("  being identical afterwards means all 8 of those transcripts")
print("  regenerate byte for byte on this machine.")
if not same:
    BAD += 1
    FINDINGS.append("A5e this probe changed the worktree")
    for l in set(after.split("\n")) - set(before.split("\n")):
        if l.strip():
            print("          *** %s" % l)

print()
L.bar("A5 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a probe of mg-c2b3's that no longer")
print("runs, a `pipefail` row that does not stand in the expected relation to")
print("its committed transcript, a rewritten runner that does not exit 0, one")
print("forced-failure site that is not caught, and a worktree this probe")
print("changed.  It ranges over the %d `*.py` of `code/runner_exit_c2b3/`" % len(targets))
print("that %s touched and the 2 rewritten runners.  It does NOT re-run" % L.REPAIR)
print("mg-7522's 8-site control -- A5d is 1 site of the 8, and says so.")
print()
for f in FINDINGS:
    print("FINDING: %s" % f)
sys.exit(1 if BAD else 0)
