"""Self-test for the mg-4adb instrument.

Every helper this instrument uses to DELETE, SUBSTITUTE or CLASSIFY is
asserted here, and each is asserted IN BOTH DIRECTIONS -- it must fire when it
should and stay silent when it should not.  mg-6ef4's P1f is why: a predicate
that matched a marker in a legend and a filename on a different line reported
three catches that had not happened, and the instrument's own transcript
carried them as facts.

The restore proof is asserted in the direction that must FAIL as well: a probe
that deliberately leaves a file behind must report `restored=False`.  A
restore proof only ever seen to succeed is worth nothing (mg-5040's own
self-test caught its `--untracked-files=all` gap exactly this way).

    python3 code/species_rung_repair_4adb/selftest4adb.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern4adb import (REPO, RUNNERS, CALL, HEADING, SETE, PRE, Probe,
                      drop_index, without, force_step, steps, disposition,
                      read_runner, runner_path, show)

n = 0
fails = 0


def ok(label, cond, detail=""):
    global n, fails
    n += 1
    fails += (not cond)
    print("  %-66s %s" % (label[:66], "ok" if cond else "*** FAILED ***"))
    if not cond and detail:
        print("        %s" % detail)


def raises(fn, *a, **kw):
    try:
        fn(*a, **kw)
    except Exception:                              # noqa: BLE001
        return True
    return False


print("=" * 78)
print("selftest4adb -- the helpers, in both directions")
print("=" * 78)
print()

# --- without ---------------------------------------------------------------
ok("without() removes the one matching line",
   without("a\nset -e\nb\n", "set -e") == "a\nb\n")
ok("without() RAISES when the line is not there",
   raises(without, "a\nb\n", "set -e"),
   "a deletion test that silently deletes nothing is a green run that means "
   "nothing")
ok("without() RAISES when the line is there twice",
   raises(without, "set -e\nset -e\n", "set -e"))
ok("without() matches on the STRIPPED line, not on a substring",
   without("a\n  set -e  \nb\n", "set -e") == "a\nb\n")
ok("without() does NOT match a line that merely contains the needle",
   raises(without, "a\n# set -e is discussed here\nb\n", "set -e"))

# --- drop_index ------------------------------------------------------------
ok("drop_index() removes exactly one line",
   drop_index("a\nb\nc\n", 1) == "a\nc\n")
ok("drop_index() removes the LAST line when asked",
   drop_index("a\nb\nc\n", 2) == "a\nb\n")
ok("drop_index() RAISES past the end",
   raises(drop_index, "a\nb\n", 5))
ok("drop_index() over every index of a file gives files one line shorter",
   all(len(drop_index("a\nb\nc\n", i).splitlines()) == 2 for i in range(3)))

# --- steps -----------------------------------------------------------------
SAMPLE = ("#!/bin/sh\n"
          "set -e\n"
          "python3 a.py > out_a.txt || {\n"
          "    cat out_a.txt; echo FAILED; exit 1; }\n"
          "cat out_a.txt\n"
          "python3 -B b.py > out_b.txt || RC=1\n"
          "# python3 c.py is only mentioned in this comment\n"
          "exit $RC\n")
ok("steps() finds the two invocations and nothing else",
   [i for i, _l in steps(SAMPLE)] == [2, 5])
ok("steps() does not take a `cat` of a transcript for a step",
   not any("cat " in l for _i, l in steps(SAMPLE)))
ok("steps() does not take a COMMENTED invocation for a step",
   not any(l.strip().startswith("#") for _i, l in steps(SAMPLE)))

# --- force_step ------------------------------------------------------------
FORCED = force_step(SAMPLE, 2)
ok("force_step() keeps the redirect", "> out_a.txt" in FORCED.splitlines()[2])
ok("force_step() keeps the `|| {` guard opener",
   FORCED.splitlines()[2].rstrip().endswith("|| {"))
ok("force_step() changes only the one line it was given",
   [l for i, l in enumerate(FORCED.splitlines()) if i != 2]
   == [l for i, l in enumerate(SAMPLE.splitlines()) if i != 2])
ok("force_step() leaves a file with the same number of lines",
   len(FORCED.splitlines()) == len(SAMPLE.splitlines()))

# --- disposition -----------------------------------------------------------
ok("disposition(): exit 0 is GATE LOST whatever was printed",
   disposition(0, True) == "GATE LOST" and disposition(0, False) == "GATE LOST",
   "exit 0 WITH the finding printed is the whole class this ticket is about")
ok("disposition(): non-zero with the finding printed is `gate fired`",
   disposition(1, True) == "gate fired")
ok("disposition(): non-zero WITHOUT the finding is BROKE EARLY",
   disposition(1, False) == "BROKE EARLY" and
   disposition(2, False) == "BROKE EARLY",
   "a red that e2 never spoke for is not a working gate")

# --- the subjects, as they must be for the probes to mean anything ---------
for rn in RUNNERS:
    src = read_runner(rn)
    # The rule is about the last COMMAND.  A trailing comment cannot carry an
    # exit status, and mg-d633's e3_bothways.py appends one to one of these
    # files as a probe.
    lines = [l for l in src.splitlines()
             if l.strip() and not l.lstrip().startswith("#")]
    ok("%s: the call is the LAST command" % rn, lines[-1].strip() == CALL,
       "last: %s" % lines[-1].strip()[:60])
    ok("%s: the call appears exactly once" % rn,
       len([l for l in src.splitlines() if l.strip() == CALL]) == 1)
    ok("%s: the heading is immediately above it" % rn,
       src.splitlines()[[i for i, l in enumerate(src.splitlines())
                         if l.strip() == CALL][0] - 1].strip() == HEADING)
    ok("%s: `%s` appears exactly once" % (rn, SETE),
       len([l for l in src.splitlines() if l.strip() == SETE]) == 1,
       "mg-6ef4's selftest asserts the same thing; the repair did not remove "
       "the line, it removed the gate's dependence on it")

# --- the PIN is the state mg-6ef4 described -------------------------------
for rn in RUNNERS:
    pre = show(PRE, runner_path(rn))
    lines = [l for l in pre.splitlines()
             if l.strip() and not l.lstrip().startswith("#")]
    ok("%s at %s: the call is NOT the last command" % (rn, PRE),
       lines[-1].strip() != CALL,
       "if it already were, there would be nothing for V1f to compare")
    ok("%s at %s: `%s` is there exactly once" % (rn, PRE, SETE),
       len([l for l in pre.splitlines() if l.strip() == SETE]) == 1)

# --- the restore proof, in the direction that must fail --------------------
SCRATCH = "code/species_rung_repair_4adb/selftest_scratch_4adb.txt"
with Probe("selftest-restores") as pr:
    pr.write(SCRATCH, "planted\n")
    planted = os.path.exists(pr.path(SCRATCH))
ok("a probe that plants a file and cleans up reports restored=True",
   planted and pr.restored is True)
ok("and the file is gone afterwards", not os.path.exists(pr.path(SCRATCH)))

leaked = os.path.join(REPO, SCRATCH)
with Probe("selftest-does-not-restore") as pr2:
    with open(leaked, "w", encoding="utf-8") as f:
        f.write("left behind on purpose\n")
ok("a probe that LEAVES a file behind reports restored=False",
   pr2.restored is False,
   "a restore proof only ever seen to succeed is worth nothing")
os.unlink(leaked)

# --- the mode the restore proof cannot see (mg-6ef4 F5), stated ------------
MODED = "code/species_rung_repair_4adb/selftest_mode_4adb.txt"
with Probe("selftest-mode") as pr3:
    pr3.write(MODED, "x\n", mode=0o400)
    mode_during = os.stat(pr3.path(MODED)).st_mode & 0o777
ok("a probe can plant a file at mode 400 and remove it",
   mode_during == 0o400 and not os.path.exists(pr3.path(MODED))
   and pr3.restored is True)

print()
print("=" * 78)
print("selftest4adb: %d assertions, %d failed" % (n, fails))
print("=" * 78)
sys.exit(1 if fails else 0)
