"""K4 -- THE POSITIVE CONTROL, PER FIXED RUNNER, IN BOTH DIRECTIONS.

The ticket: *"Positive control per fixed runner: make its self-test fail on
purpose and confirm the RUNNER exits non-zero.  Printing failures and exiting
non-zero are trivially separated by a pipe, which is the whole defect."*

WHAT IS MEASURED, AND WHAT IS DELIBERATELY NOT.  The property under test is the
runner's PLUMBING -- whether a non-zero from a step reaches the runner's own
exit status -- and nothing about the batteries themselves.  So each runner is
copied into a temp directory with every script it launches replaced by a
three-line stub that prints a marker and exits with a chosen code.  Two facts
come out of each run:

    exit code       the runner's own status
    reach           WHICH STUBS EXECUTED, IN ORDER -- each stub appends its
                    own name to a file at an absolute path, because every
                    runner here redirects its steps into a transcript and a
                    marker on stdout would measure "survived the redirect"
                    instead of "ran"

and the control is scored on BOTH, because either alone is forgeable.  A runner
that exits non-zero for an unrelated reason (a downstream `grep` finding
nothing in a stubbed transcript) would pass an exit-code-only check; a runner
that stops early but exits 0 would pass a reach-only check.  The pair does not.

FOUR RUNS PER PIPELINE, and the two-by-two is the whole point:

    text        target      expected exit   expected reach
    pre-repair  exits 0     0               reaches the end      (baseline)
    pre-repair  exits 1     0  <-- DEFECT   reaches the end      (the bug)
    post-repair exits 0     0               reaches the end      (not broken)
    post-repair exits 1     NON-ZERO        THE TARGET IS THE LAST STEP THAT
                                            RAN                  (the fix)

Row 2 is the one that matters: it is the defect reproduced on the real runner
text, at every site, rather than argued from the POSIX spec.  A control that
only ran rows 3 and 4 would show a working runner and would not show that it
was ever broken.

WHY STUBS AND NOT THE REAL BATTERIES.  Running the real thing 4 x 34 times is
about forty hours (branching_audit_2060 alone is ~20 minutes a pass) and would
measure the batteries, which are not what changed.  The cost is stated: K4
proves the runners propagate status, and does NOT re-prove that the batteries
pass.  K3b does that, directly, once per target.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libc2b3 as L

BAD = 0
REF = L.TICKET_REF
MARK = "C2B3-STUB-RAN"

# THE STUB RECORDS ITSELF IN A FILE, NOT ON STDOUT, and the first draft did it
# the other way.  Every runner here redirects its steps into a transcript, so a
# marker printed on stdout is captured by the redirect and only reappears if
# something `cat`s the file -- which made `reach` measure "markers that survived
# the redirect" instead of "steps that executed", and scored 15 working runners
# BAD.  An absolute path is immune to redirection, to `2>&1`, and to `cd`.
STUB = """#!/usr/bin/env python3
import sys
open(%r, "a").write("%s\\n")
print("stub output for %s")
sys.exit(%d)
"""
SH_STUB = """#!/bin/sh
echo "%s" >> %s
echo "stub output for %s"
exit %d
"""


def hdr(t):
    print()
    L.bar(t)
    print()


def plant(tmp, tree, runner_src, fail_script):
    """Write `runner_src` plus a stub for every script it launches."""
    d = os.path.join(tmp, "code", tree)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "run_all.sh"), "w") as fh:
        fh.write(runner_src)
    log = os.path.join(tmp, "reach.log")
    planted = []
    for _, text in L.logical_lines(runner_src):
        if text.strip().startswith("#"):
            continue
        for interp, script in L.invocations(text):
            p = os.path.normpath(os.path.join(d, script))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            code = 1 if script == fail_script else 0
            base = os.path.basename(script)
            body = (SH_STUB % (base, log, base, code)
                    if script.endswith(".sh")
                    else STUB % (log, base, base, code))
            with open(p, "w") as fh:
                fh.write(body)
            os.chmod(p, 0o755)
            planted.append(script)
    return d, log, planted


def run(d, log):
    p = subprocess.run(["/bin/sh", os.path.join(d, "run_all.sh")],
                       capture_output=True, text=True, timeout=120)
    try:
        with open(log) as fh:
            reached = [l for l in fh.read().split("\n") if l]
    except FileNotFoundError:
        reached = []
    return p.returncode, reached


L.bar("K4  POSITIVE CONTROL -- the runner's own exit code, both directions")

old = {r: L.read(r, REF) for r in L.runners(REF)}
new = {r: L.read(r) for r in L.runners()}
affected = [r for r in old if L.tee_pipelines(old[r])]

hdr("K4a  THE TWO-BY-TWO, PER PIPELINE")

print("  For each `| tee` site: the target stub is made to exit 1 and the")
print("  RUNNER's exit code is read, on the pre-repair text and on the")
print("  post-repair text.  `reach` is the number of stubs that printed.")
print()
print("  %-42s %-9s %-16s %-16s %s"
      % ("runner / target", "baseline", "PRE-REPAIR fail",
         "POST-REPAIR fail", ""))

rows = []
for r in sorted(affected):
    tree = r.split("/")[1]
    for n, t in L.tee_pipelines(old[r]):
        script = L.invocations(t)[0][1]
        res = {}
        for label, src, failing in (("base", new[r], None),
                                    ("pre", old[r], script),
                                    ("post", new[r], script)):
            tmp = tempfile.mkdtemp(prefix="c2b3-")
            try:
                d, log, planted = plant(tmp, tree, src, failing)
                res[label] = run(d, log)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        b_code, b_reach = res["base"]
        p_code, p_reach = res["pre"]
        q_code, q_reach = res["post"]

        # the two-by-two, scored.
        #   pre  : the DEFECT must be visible -- the failing step does not
        #          stop the run, so it gets as far as the baseline did.
        #   post : the FIX must bite -- the runner exits non-zero AND THE
        #          TARGET IS THE LAST STEP THAT RAN.  Not `reach < baseline`:
        #          when the target IS the last step, a working runner reaches
        #          exactly as far as the baseline and would score BAD.  Ten of
        #          the thirty-four sites are last steps.
        base = os.path.basename(script)
        defect = (p_reach == b_reach)
        fixed = (q_code != 0 and q_reach and q_reach[-1] == base
                 and q_reach == b_reach[:len(q_reach)])
        ok = defect and fixed
        BAD += (not ok)
        rows.append((r, script, b_code, len(b_reach), p_code, len(p_reach),
                     q_code, len(q_reach), defect, fixed))
        print("  %-42s %-9s %-16s %-16s %s"
              % ("%s / %s" % (tree, os.path.basename(script)),
                 "exit %d/%d" % (b_code, len(b_reach)),
                 "exit %d/%d %s" % (p_code, len(p_reach),
                                    "SWALLOWED" if defect else "***"),
                 "exit %d/%d %s" % (q_code, len(q_reach),
                                    "stops here" if fixed else "***"),
                 "ok" if ok else "*** BAD ***"))

print()
print("  columns read `exit <code>/<stubs that printed>`.")
print()
n = len(rows)
print("  %d of %d sites show the DEFECT on the pre-repair text: the runner"
      % (sum(1 for x in rows if x[8]), n))
print("  ran to the end with a step exiting 1.")
print("  %d of %d sites show the FIX on the post-repair text: the runner"
      % (sum(1 for x in rows if x[9]), n))
print("  exits non-zero AND stops before the steps that follow.")

# ---------------------------------------------------------------------------
hdr("K4b  THE PRE-REPAIR EXIT CODES, LOOKED AT DIRECTLY")

print("  `SWALLOWED` above is scored on REACH, not on the exit code, and this")
print("  section says why in numbers.  On the pre-repair text a failing step")
print("  does not stop the run, so the runner's status is whatever its LAST")
print("  command happened to return -- usually 0, but some of these runners")
print("  end in a `grep` that finds nothing in a stubbed transcript and")
print("  returns 1 for a reason that has nothing to do with the failure.")
print("  Scoring the defect on the exit code alone would have counted those")
print("  as working.")
print()
zero = [x for x in rows if x[4] == 0]
nonzero = [x for x in rows if x[4] != 0]
print("  pre-repair, step exits 1:")
print("    runner exited 0        %2d of %d   <- the defect, unambiguously"
      % (len(zero), n))
print("    runner exited non-zero %2d of %d   <- for an unrelated downstream"
      % (len(nonzero), n))
print("                                       reason; REACH shows the run did")
print("                                       not stop at the failure")
for x in nonzero:
    print("      %-40s exit %d, reach %d of %d"
          % ("%s / %s" % (x[0].split("/")[1], os.path.basename(x[1])),
             x[4], x[5], x[3]))

# ---------------------------------------------------------------------------
hdr("K4c  THE STUBS ARE NOT DOING THE WORK -- a control on the control")

print("  A stub harness can pass for a reason that has nothing to do with the")
print("  runner: if the stubs never ran at all, `reach` would be empty")
print("  everywhere, `q_reach[-1]` would not exist and every row would score")
print("  BAD -- which is the safe direction, but a baseline that silently")
print("  reached nothing would make every row unscoreable while still")
print("  printing a full table.  So:")
print()
empty = [x for x in rows if x[3] == 0]
print("    sites whose BASELINE reached zero stubs: %d" % len(empty))
BAD += len(empty)
print("    sites whose baseline exited non-zero:    %d"
      % sum(1 for x in rows if x[2] != 0))
print("      (allowed, and named: several runners end with a `grep` over")
print("       out_*.txt that stubs do not populate.  The scoring does not use")
print("       the baseline's exit code for anything -- only its reach.)")
print()
print("  And the second direction, which is the one a stub harness usually")
print("  gets wrong: with NO stub failing, does the post-repair runner still")
print("  reach the end?  If the repair had broken a runner outright, every")
print("  `fixed` row would still be green while the runner was useless.")
broken = [x for x in rows if x[7] >= x[3] or x[3] == 0]
print()
for r in sorted(affected):
    tree = r.split("/")[1]
    tmp = tempfile.mkdtemp(prefix="c2b3-")
    try:
        d, log, planted = plant(tmp, tree, new[r], None)
        code, reach = run(d, log)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    tmp = tempfile.mkdtemp(prefix="c2b3-")
    try:
        d2, log2, planted2 = plant(tmp, tree, old[r], None)
        ocode, oreach = run(d2, log2)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    same = (len(reach) == len(oreach) and reach == oreach)
    BAD += (not same)
    print("    %-42s pre reach %2d, post reach %2d  %s"
          % (tree, len(oreach), len(reach), "identical" if same
             else "*** THE REPAIR CHANGED WHAT RUNS ***"))
print()
print("  Identical reach with nothing failing means the repair changed the")
print("  runner's behaviour in exactly one circumstance: when a step fails.")

# ---------------------------------------------------------------------------
hdr("K4d  THE GENERAL FORM, ON THIS SECTION")

print("  K4 is a script that runs scripts and reads their exit codes, so it")
print("  is the most exposed part of this instrument.  Enumerated:")
print()
print("   1. `run()` uses subprocess.run with a LIST argv, no `shell=True`,")
print("      no pipe.  `returncode` is the runner's own status.  This is the")
print("      branch that cannot exhibit the defect and the reason is that")
print("      there is no pipeline for a status to be taken from.")
print("   2. Every verdict here is a CONJUNCTION of the exit code and the")
print("      reach.  That is not belt-and-braces: the defect under repair is")
print("      precisely the separation of `printed a failure` from `exited")
print("      non-zero`, so an instrument that scored only one of them would")
print("      be reproducing the defect while testing for it.")
print("   3. The pre-repair arm is run from `git show %s:...`, a pinned" % REF)
print("      revision, not from HEAD.  Against HEAD both arms would be the")
print("      repaired text and every row would pass trivially -- mg-821e's")
print("      finding (41ac5d4), applied to this file.")
print("   4. K4c is the control on the control: it checks the baseline")
print("      actually reached the stubs and that the repair did not change")
print("      what runs when nothing fails.  Without it, `fixed` could be true")
print("      because the runner was broken rather than because it was fixed.")
print("   5. What K4 does NOT establish, stated: that the batteries pass.")
print("      The stubs replace them.  K3b is where the real targets run.")

print()
L.bar("K4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It ranges over the %d `| tee` pipelines of the"
      % n)
print("%d affected runners -- three runs per site plus two per runner, %d"
      % (len(affected), n * 3 + len(affected) * 2))
print("runner executions in all -- plus the %d pre/post reach comparisons"
      % len(affected))
print("in K4c.  It counts a site bad when the defect is")
print("NOT reproducible on the pre-repair text, when the fix does NOT stop the")
print("run, when a baseline reached no stubs, or when the repair changed what")
print("runs in the no-failure case.  It does NOT range over the batteries")
print("themselves -- those are stubbed here on purpose and run for real in K3b.")
sys.exit(1 if BAD else 0)
