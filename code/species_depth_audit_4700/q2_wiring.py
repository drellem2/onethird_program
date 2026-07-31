"""Q2 -- PRESENCE OF A CALL IS NOT EVIDENCE OF EXECUTION.  RUN ALL THREE.

mg-6cb9's F2: `e2_crosssection.py` is the check that closes mg-7dd3's B1 -- a
claim struck in one section of a document standing un-struck in another, which
no per-section checker can see by construction.  It existed, it was correct, it
was named in every reader-facing artifact, and it was called by **0 of the 3**
species `run_all.sh`.  mg-821e wired it into all three.

The brief for this audit is explicit: *presence of a call in a script is not
evidence that it executes -- a guarded branch, an early exit, or a swallowed
error all leave the call in place.*  So nothing here greps a runner.  Every row
is a `sh run_all.sh` and its OWN STDOUT, and the observed output is reported per
script for all three.

  Q2a  the three runners, RUN.  Exit code and the check's own output, quoted.
  Q2b  B1 ITSELF restored on disk -- and the control that makes the result mean
       something: the same document state with the wiring REMOVED must be
       GREEN, or a red run proves only that something failed somewhere.
  Q2c  DELETION AT THE FINEST UNIT THAT HAS A RETURN.  mg-821e deletion-tested
       the block as ONE 20-line unit.  It has at least three separable parts --
       the call, the `||` guard, and the two `echo`s that PRINT the result --
       and each is deleted alone here.
  Q2d  WHAT A CRASH LOOKS LIKE.  The guard's message names a specific finding.
       Any non-zero exit reaches it.
  Q2e  ONE THING NO LIST NAMES: `| tee` in front of `set -e`.  `41ac5d4` fixed
       exactly this in mg-821e's OWN runner and recorded that every other
       runner in the arc still has it.  Two of those are runners this repair
       edited.  Measured, not taken on the commit message's word.

    python3 code/species_depth_audit_4700/q2_wiring.py
"""

import os
import re
import sys

from kern4700 import (hdr, REPO, sh, Probe, run_runner, predict, PRE_REPAIR,
                      WIRE_MARK, CALL_AND_GUARD, CALL_ONLY, PRINTING, unwire)

bad = 0
miss = 0

TREES = ["species_repair_a4ef", "species_remainder_f8fa", "species_repair_6f61"]
RUNNERS = {t: "code/%s/run_all.sh" % t for t in TREES}
DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
E2 = "code/species_extent_d633/e2_crosssection.py"

# The three separable parts of the wiring block, and `unwire`, live in
# kern4700 so that selftest4700.py can test them without importing this file --
# which runs twenty-one `run_all.sh` at module level.  mg-821e's OUTCOMES.md
# records paying for that lesson once already.
# B1, and the substitution that puts it back.  COPIED from
# `e2_crosssection.py`'s own control (a) rather than imported: importing it
# would run the checker at module level, and -- more to the point -- an
# expectation that moves when the subject moves cannot disagree with the
# subject.  That is mg-6cb9's F1 in a different costume and this instrument is
# not going to wear it.
B1 = ('Aguiar–Mahajan §17.5, quoting their own §17.4: '
      '*"`K̄(Π)` is the algebra of\nsymmetric functions in '
      'noncommuting variables and `K(Π)` is the familiar Hopf algebra '
      'of\nsymmetric functions."*')
CORRECTION = re.compile(r"(?s)Aguiar–Mahajan §17\.5, quoting their own "
                        r"§17\.4, records both values.*?"
                        r"rest of its own document\.\n")

SELFTESTS = {
    "species_repair_a4ef": "code/species_repair_a4ef/selftesta4ef.py",
    "species_remainder_f8fa": "code/species_remainder_f8fa/selftestf8fa.py",
    "species_repair_6f61": "code/species_repair_6f61/selftest6f61.py",
}
RED_STUB = ('print("*** FAILED *** self-test forced red by the mg-4700 audit")\n'
            'raise SystemExit(1)\n')


def e2_lines(out):
    """The cross-section check's own output as the runner printed it."""
    keep = []
    grab = False
    for l in out.splitlines():
        if l.startswith("cross-section check (mg-821e)"):
            grab = True
            keep.append(l)
            continue
        if grab:
            if re.match(r"^(E2 TOTAL BAD:|\s+\d+ file\(s\) carry a strike)", l):
                keep.append(l.rstrip())
                continue
            break
    return keep


# ---------------------------------------------------------------------------
# Q2a  the three runners, RUN
# ---------------------------------------------------------------------------
hdr("Q2a  ALL THREE `run_all.sh`, EXECUTED -- exit code and the check's own"
    " output")

print("  Nothing below is a grep of a script.  Each row is `sh run_all.sh`")
print("  from inside its own tree, and the quoted lines are that runner's")
print("  stdout.  The distinction is the whole of mg-6cb9's F2.")
print()

base = {}
for t in TREES:
    rc, out = run_runner(t)
    base[t] = (rc, out)
    got = e2_lines(out)
    print("  code/%-24s exit %d" % (t, rc))
    if got:
        for l in got:
            print("        | %s" % l)
    else:
        print("        | *** the check printed NOTHING in this runner ***")
    ok = (rc == 0 and len(got) >= 2)
    bad += (not ok)

allrun = all(base[t][0] == 0 and len(e2_lines(base[t][1])) >= 2 for t in TREES)
miss += predict("D3a-c", "3 of 3 exit 0 + output",
                "%d of 3" % sum(1 for t in TREES
                                if base[t][0] == 0 and e2_lines(base[t][1])),
                allrun)
print()
print("  For comparison, the state mg-6cb9 measured: the same check reached by")
print("  0 of these 3 runners.  The difference is visible in stdout, which is")
print("  the only place it was ever going to be visible.")
print()


# ---------------------------------------------------------------------------
# Q2b  B1 restored, AND the control that makes it mean something
# ---------------------------------------------------------------------------
hdr("Q2b  B1 ITSELF PUT BACK ON DISK -- with the control a red run needs")

print("  A red runner proves the wiring works only if the SAME document state")
print("  with the wiring REMOVED is green.  Without that control, `exit 1`")
print("  could be `check_doc.py` failing forty lines earlier and the")
print("  cross-section check never being reached at all.  Both halves are run.")
print()

doc0 = open(os.path.join(REPO, DOC), encoding="utf-8").read()
if not CORRECTION.search(doc0):
    print("  *** §0's corrected paragraph is not where this instrument expects")
    print("      it: Q2b cannot run, and this line is the record that it did")
    print("      not.  ***")
    bad += 1
    restored_doc = None
else:
    restored_doc = CORRECTION.sub(lambda _m: B1 + "\n", doc0, count=1)

if restored_doc:
    wired_rc, unwired_rc = {}, {}
    for t in TREES:
        with Probe("D3d B1 restored, wiring in place",
                   restores=["code/" + t]) as pr:
            pr.write(DOC, restored_doc)
            rc, out = run_runner(t)
        wired_rc[t] = rc
        named = "STANDING UN-STRUCK" in out
        msg = "E2 CROSS-SECTION FAILED" in out
        print("  code/%-24s WIRED    exit %d   names STANDING UN-STRUCK: %s"
              % (t, rc, "yes" if named else "*** no ***"))
        for l in out.splitlines():
            if "STANDING UN-STRUCK" in l:
                print("        | %s" % l.strip()[:90])
                break
        bad += (rc == 0) + (not named) + (not msg)

        with Probe("D3d-ctl B1 restored, wiring REMOVED",
                   restores=["code/" + t]) as pr2:
            pr2.write(DOC, restored_doc)
            pr2.write(RUNNERS[t], unwire(pr2.read(RUNNERS[t])))
            rc2, _out2 = run_runner(t)
        unwired_rc[t] = rc2
        print("  code/%-24s UNWIRED  exit %d   %s"
              % (t, rc2,
                 "green -- so the red above IS the wiring"
                 if rc2 == 0 else
                 "*** ALSO RED: the red above is not attributable ***"))
        bad += (rc2 != 0)
    nc = sum(1 for t in TREES if wired_rc[t] != 0)
    ng = sum(1 for t in TREES if unwired_rc[t] == 0)
    miss += predict("D3d", "3 of 3 caught", "%d of 3 caught" % nc, nc == 3)
    print()
    print("  CAUGHT wired %d of 3, GREEN unwired %d of 3.  The second number is"
          % (nc, ng))
    print("  what makes the first one mean anything.")
print()

# And the unwiring is checked against the pre-repair file byte for byte, so
# `a pure addition` is measured rather than asserted -- and against a PINNED
# ref, not `HEAD`, which is the error `41ac5d4` had to come back and fix.
print("  `unwire()` above against %s, byte for byte:" % PRE_REPAIR)
for t in TREES:
    rc, old, _ = sh(["git", "show", "%s:%s" % (PRE_REPAIR, RUNNERS[t])])
    cur = open(os.path.join(REPO, RUNNERS[t]), encoding="utf-8").read()
    same = (unwire(cur) == old)
    bad += (not same)
    print("      code/%-24s %s" % (t, "identical" if same
                                   else "*** DIFFERS ***"))
print("  So the wiring really is an addition and nothing else moved -- and the")
print("  ref is PINNED.  Anchored on HEAD this row would have stopped")
print("  comparing on the day the repair landed (mg-821e's own 41ac5d4).")
print()


# ---------------------------------------------------------------------------
# Q2c  deletion at the finest unit that has a return
# ---------------------------------------------------------------------------
hdr("Q2c  THE BLOCK IS NOT ONE UNIT -- each part deleted ALONE")

print("  mg-821e's deletion test removes the block as ONE unit, 20 lines, and")
print("  reports the output disappearing.  `Delete at the finest unit that has")
print("  a return`: the block has three separable parts, and two of them turn")
print("  out to have no return at all.")
print()

if restored_doc:
    print("  D3e  the `|| { ... exit 1; }` GUARD deleted alone, call kept, with")
    print("       B1 restored on disk -- does the runner still go red?")
    guard_rc = {}
    for t in TREES:
        with Probe("D3e guard removed", restores=["code/" + t]) as pr:
            pr.write(DOC, restored_doc)
            pr.edit(RUNNERS[t], CALL_AND_GUARD, CALL_ONLY)
            rc, out = run_runner(t)
        guard_rc[t] = rc
        named = "E2 CROSS-SECTION FAILED" in out
        print("       code/%-24s exit %d   guard's message printed: %s"
              % (t, rc, "yes" if named else "no"))
    nred = sum(1 for t in TREES if guard_rc[t] != 0)
    miss += predict("D3e", "3 of 3 still red", "%d of 3 red" % nred, nred == 3)
    if nred == 3:
        bad += 1
        print()
        print("  *** FINDING.  Deleting the guard moves the MESSAGE and not the")
        print("      VERDICT.  `set -e` already aborts on a failed command")
        print("      substitution in an assignment, so five of the block's")
        print("      twenty lines have no return under the deletion test that")
        print("      was run on the block as a whole.  The 20-line unit")
        print("      OVERSTATES what is load-bearing; the guard's only")
        print("      contribution is the diagnosis a reader gets, which is")
        print("      what Q2d is about. ***")
    print()

print("  D3f  the two `echo`s that PRINT the check's output, deleted alone,")
print("       against the CLEAN tree.  The wiring comment says `The OUTPUT is")
print("       printed, not just the call made`.  What guards that sentence?")
print()
quiet_rc = {}
for t in TREES:
    with Probe("D3f printing removed", restores=["code/" + t]) as pr:
        pr.edit(RUNNERS[t], PRINTING, "")
        rc, out = run_runner(t)
    quiet_rc[t] = (rc, bool(e2_lines(out)))
    print("       code/%-24s exit %d   any sign the check ran: %s"
          % (t, rc, "yes" if e2_lines(out) else "NONE"))
ngreen = sum(1 for t in TREES if quiet_rc[t][0] == 0 and not quiet_rc[t][1])
miss += predict("D3f", "3 of 3 green and silent", "%d of 3" % ngreen,
                ngreen == 3)
if ngreen == 3:
    bad += 1
    print()
    print("  *** FINDING.  The claim that distinguishes this repair from the")
    print("      state mg-6cb9 found -- `a call present in a script is not")
    print("      evidence of execution, so the OUTPUT is printed` -- is itself")
    print("      unguarded.  Delete the two `echo`s and all three runners exit")
    print("      0 with no trace that the check ran, which is exactly the")
    print("      reader-facing state F2 was about.  Nothing in any self-test")
    print("      or checker asserts those lines exist. ***")
print()


# ---------------------------------------------------------------------------
# Q2d  what a crash looks like from the runner's stdout
# ---------------------------------------------------------------------------
hdr("Q2d  ANY NON-ZERO EXIT REACHES A MESSAGE THAT NAMES ONE SPECIFIC FINDING")

print("  The guard prints `a struck claim stands un-struck elsewhere`.  That")
print("  is the ONE thing e2 exits 1 for -- but the `||` reaches it for a")
print("  crash, an import error, a missing file or a syntax error just as")
print("  readily, and stderr is not captured into $E2OUT, so the traceback")
print("  goes to the terminal while the summary line asserts a finding.")
print()
for t in TREES:
    with Probe("D3g e2 crashes", restores=["code/" + t, E2]) as pr:
        pr.edit(E2, "import os\n", "import os\nraise RuntimeError('mg-4700')\n")
        rc, out = run_runner(t)
    claims = "a struck claim stands un-struck elsewhere" in out
    names = "STANDING UN-STRUCK" in out
    trace = "RuntimeError" in out
    print("  code/%-24s exit %d   claims a finding: %-3s  names one: %-3s"
          % (t, rc, "yes" if claims else "no", "yes" if names else "no"))
    bad += 0        # reported, not scored: see the extent note below
miss += predict("D3g", "claims a finding, names none",
                "claims %s / names %s" % ("yes" if claims else "no",
                                          "yes" if names else "no"),
                claims and not names)
print()
print("  A crash is reported as `a struck claim stands un-struck elsewhere`")
print("  with no such claim named.  This is MINOR -- the run does go red, and")
print("  the traceback is on stderr for anyone watching -- but it is the one")
print("  line a reader of the transcript is given, and it is false.")
print()


# ---------------------------------------------------------------------------
# Q2e  the thing no list names: `| tee` in front of `set -e`
# ---------------------------------------------------------------------------
hdr("Q2e  A RED SELF-TEST, SWALLOWED -- in two of the three runners repaired")

print("  `41ac5d4` fixed this in mg-821e's OWN runner: under `set -e` a")
print("  pipeline's status is the LAST command's, and `tee` always exits 0, so")
print("  a failing self-test does not stop the run.  Its message says `Every")
print("  other run_all.sh in this arc still uses | tee; noted, not touched.`")
print("  Two of those are the runners THIS repair edited -- it added twenty")
print("  lines to each -- so the swallow is measured here rather than taken on")
print("  the commit message's word.")
print()
for t in TREES:
    with Probe("D6 red self-test", restores=["code/" + t]) as pr:
        pr.write(SELFTESTS[t], RED_STUB)
        rc, out = run_runner(t)
    swallowed = (rc == 0)
    saw = "*** FAILED ***" in out
    print("  code/%-24s exit %d   printed *** FAILED ***: %-3s  %s"
          % (t, rc, "yes" if saw else "no",
             "SWALLOWED" if swallowed else "stopped the run"))
    bad += swallowed
    if t == "species_repair_a4ef":
        a4ef_sw = swallowed
    if t == "species_remainder_f8fa":
        f8fa_sw = swallowed
    if t == "species_repair_6f61":
        f61_sw = swallowed
miss += predict("D6a-c", "a4ef+f8fa swallow, 6f61 not",
                "a4ef %s / f8fa %s / 6f61 %s"
                % (a4ef_sw, f8fa_sw, f61_sw),
                a4ef_sw and f8fa_sw and not f61_sw)
print()

# D6d -- and the class, counted, so the two above are placed rather than
# reported as if they were the whole of it.
rc, out, _ = sh(["git", "grep", "-l", "| tee", "--", "*/run_all.sh"])
teed = [l for l in out.splitlines() if l]
rc, out2, _ = sh(["git", "grep", "-c", "selftest.*| tee", "--", "*/run_all.sh"])
selftee = [l.split(":")[0] for l in out2.splitlines() if l]
print("  THE CLASS, COUNTED so these two are placed and not mistaken for all")
print("  of it: %d run_all.sh in this repository pipe a SELF-TEST through"
      % len(selftee))
print("  `tee` (%d use `| tee` anywhere).  Two of them are above.  This is a" % len(teed))
print("  repo-wide shape and mg-821e said so; what is measured here is that")
print("  two of the three files this repair opened still carry it.")
for f in sorted(selftee):
    print("      %s%s" % (f, "   <-- edited by this repair"
                          if f in RUNNERS.values() else ""))
print()


print("=" * 78)
print("Q2 TOTAL BAD: %d" % bad)
print("Q2 PREDICTIONS MISSED: %d" % miss)
print("=" * 78)
print()
print("EXTENT OF THOSE NUMBERS.  Q2 executed `run_all.sh` %d times across the"
      % (3 * 7))
print("three species trees and read each runner's own stdout.  It greps no")
print("script for a call.  It covers the WIRING of e2_crosssection.py into")
print("those three runners and nothing else: not e2's own correctness (mg-d633")
print("and mg-6cb9 measured that, and Q4 re-runs mg-6cb9's battery unmodified),")
print("not the other two OPEN items, and not the fourth runner")
print("code/species_extent_d633/run_all.sh, which is where e2 already lived.")
print("Q2d is REPORTED and not scored: the run does go red, so it is a wrong")
print("message and not a missing verdict, and scoring it would put a")
print("cosmetic row beside two structural ones.")
sys.exit(1 if bad else 0)
