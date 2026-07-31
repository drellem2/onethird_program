"""V1 -- OPEN 1.  THE FIFTH RUNG, AND THE POPULATION THAT COULD NOT SEE IT.

mg-6ef4's F3: `set -e` sits at the top of each of the three species runners,
53, 60 and 43 lines above the cross-section call.  It is the statement that
turns e2's exit code into the runner's exit code.  Deleted alone, 3 of 3
runners exit 0 WHILE PRINTING e2's FINDING IN FULL -- and it is in no deletion
population this arc has used: mg-821e's p3_wiring.py, mg-4700's q2_wiring.py
and mg-5040's r2_wiring.py each enumerate THE BLOCK.

    A mutation population that excludes a line makes that line invisible to
    the control that the population certifies -- and the exclusion looks like
    nothing, because the certificate still reads 100%.

TWO THINGS ARE REPAIRED AND BOTH ARE MEASURED HERE.

THE RUNG.  The gate is moved to the END of each runner.  A POSIX shell
script's exit status is its last command's, so the statement that carries e2's
status out of the file is now the CALL, which is inside the block and inside
every population that has ever enumerated it.  No guard was added beside
`set -e`: mg-4700's F2 measured what that produces -- a line whose deletion
changes no verdict because the other one catches it -- and mg-5040 removed it.

THE POPULATION.  It is EVERY LINE OF THE RUNNER FILE.  Not the block, not the
statements, not the non-comment lines: every line, deleted one at a time, with
the runner executed each time.  THERE IS NO EXCLUSION LIST, so there is no
exclusion to justify -- which is the only answer to F3 that does not depend on
somebody having predicted correctly which lines matter.  "Obviously fatal" and
"obviously inert" are both predictions, and F3 is what one of them cost.

  V1a  the population, stated, and its size
  V1b  the attribution control -- e2 red, runners unmodified
  V1c  EVERY LINE OF EVERY RUNNER, DELETED ALONE, with e2 red
  V1d  declared load-bearing lines against measured ones, and the source rule
       that keeps the gate last
  V1e  what `set -e` still carries, named by forcing each step red without it
  V1f  the same deletion at the pin -- mg-6ef4's F3, reproduced and closed

    python3 code/species_rung_repair_4adb/v1_population.py
"""

import os
import sys

from kern4adb import (hdr, REPO, RUNNERS, CALL, HEADING, SETE, E2_SAYS,
                      STRIKE_DOC, STRIKE_TEXT, Probe, prove, drop_index,
                      without, force_step, steps, read_runner, run_runner,
                      runner_path, show, PRE, disposition)

bad = 0
missed = 0


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    for ln in detail.splitlines():
        if ln:
            print("        %s" % ln)


def note(label, value):
    print("  %-64s %s" % (label[:64], value))


def score(pid, predicted, got):
    global missed
    hit = predicted == got
    missed += (not hit)
    print("  %-6s predicted %-26s got %-26s %s"
          % (pid, str(predicted), str(got), "" if hit else "*** MISSED ***"))
    return hit


SRC = {rn: read_runner(rn) for rn in RUNNERS}


# ---------------------------------------------------------------------------
# V1a  THE POPULATION
# ---------------------------------------------------------------------------
hdr("V1a  THE DELETION POPULATION, STATED -- WHAT IS IN IT AND WHAT IS OUT")

print("  IN:   every line of the file, 1..N, deleted one at a time.")
print("  OUT:  nothing.")
print()
print("  That is the whole statement, and it is written this way because the")
print("  ticket asks for each exclusion to be justified individually and the")
print("  honest way to meet that is to have none.  Comment lines are in.")
print("  Blank lines are in.  The shebang is in.  `set -e` is in, which is")
print("  the line mg-6ef4 found outside all three previous populations.")
print()
for rn in RUNNERS:
    n = len(SRC[rn].splitlines())
    comments = len([l for l in SRC[rn].splitlines()
                    if l.strip().startswith("#")])
    blanks = len([l for l in SRC[rn].splitlines() if not l.strip()])
    note("code/%s/run_all.sh" % rn,
         "%d line(s): %d comment, %d blank, %d other"
         % (n, comments, blanks, n - comments - blanks))
TOTAL = sum(len(SRC[rn].splitlines()) for rn in RUNNERS)
print()
note("TOTAL RUNNER EXECUTIONS IN V1c", TOTAL)
print()
print("  The three earlier populations, for comparison, from mg-6ef4's T2f:")
print("  mg-821e p3_wiring.py, mg-4700 q2_wiring.py and mg-5040 r2_wiring.py")
print("  each enumerate THE WIRING BLOCK -- 2 lines after mg-5040, 20 before.")
print("  None of them contains `%s`.  This one contains every line that" % SETE)
print("  exists, so the question 'is the load-bearing line in the set' cannot")
print("  be answered wrongly by a judgement call.")
print()


# ---------------------------------------------------------------------------
# V1b  THE ATTRIBUTION CONTROL
# ---------------------------------------------------------------------------
hdr("V1b  THE ATTRIBUTION CONTROL -- e2 FORCED RED, RUNNERS UNMODIFIED")

print("  Nothing below means anything if this is not red, and it means the")
print("  wrong thing if it is red without e2 saying so.  Both are checked,")
print("  and the clean baseline is measured first: a repair that reddens a")
print("  correct tree has moved the problem rather than removed it.")
print()

CLEAN = {}
for rn in RUNNERS:
    rc, out = run_runner(rn)
    CLEAN[rn] = (rc, E2_SAYS in out)
    print("      CLEAN  %-26s exit %d   prints %s: %s"
          % (rn, rc, E2_SAYS, "yes" if CLEAN[rn][1] else "no"))
row("3 of 3 runners are GREEN on a clean tree, and e2 is silent",
    all(v == (0, False) for v in CLEAN.values()))
print()

BASE = {}
with Probe("v1b") as pr:
    pr.write(STRIKE_DOC, STRIKE_TEXT)
    for rn in RUNNERS:
        rc, out = run_runner(rn)
        BASE[rn] = (rc, E2_SAYS in out)
        print("      RED    %-26s exit %d   prints %s: %s"
              % (rn, rc, E2_SAYS, "yes" if BASE[rn][1] else "NO"))
prove(pr)
print()
row("3 of 3 runners are RED, and red BECAUSE of e2",
    all(v == (1, True) for v in BASE.values()),
    "If this row is a finding, every row below it is uninterpretable\n"
    "and should be read as such.")
print()


# ---------------------------------------------------------------------------
# V1c  THE SWEEP
# ---------------------------------------------------------------------------
hdr("V1c  EVERY LINE OF EVERY RUNNER, DELETED ALONE, WITH e2 RED")

print("  One row per line of each file.  `gate fired` means the runner was")
print("  red AND e2's sentence was in its output, so the deletion cost")
print("  nothing.  `GATE LOST` means the runner exited 0 -- the class this")
print("  ticket is about, and the column after it says whether the finding")
print("  was printed anyway.  `BROKE EARLY` means the runner was red without")
print("  e2 ever speaking: the deletion broke it before the gate.")
print()

SWEEP = {}
with Probe("v1c") as pr:
    pr.write(STRIKE_DOC, STRIKE_TEXT)
    for rn in RUNNERS:
        lines = SRC[rn].splitlines()
        SWEEP[rn] = []
        print("  code/%s/run_all.sh" % rn)
        for i, ln in enumerate(lines):
            pr.write(runner_path(rn), drop_index(SRC[rn], i))
            rc, out = run_runner(rn)
            names = E2_SAYS in out
            d = disposition(rc, names)
            SWEEP[rn].append((i, ln, rc, names, d))
            # EVERY row is printed, not only the interesting ones.  A census
            # that prints its exceptions and summarises the rest is a census a
            # reader has to take on trust for the part that was summarised,
            # and this arc has spent four tickets on exactly that.
            print("      line %3d  exit %d  %-11s  finding printed: %-3s  %s"
                  % (i + 1, rc, d, "yes" if names else "no",
                     ln.strip()[:40]))
        pr.write(runner_path(rn), SRC[rn])
        kinds = {}
        for _i, _ln, _rc, _n, d in SWEEP[rn]:
            kinds[d] = kinds.get(d, 0) + 1
        print("      %d line(s): %s" % (len(lines), ", ".join(
            "%s %d" % (k, kinds[k]) for k in sorted(kinds))))
        print()
prove(pr)
print()

LOST = {rn: [ln.strip() for _i, ln, _rc, _n, d in SWEEP[rn]
             if d == "GATE LOST"] for rn in RUNNERS}
EARLY = {rn: [ln.strip() for _i, ln, _rc, _n, d in SWEEP[rn]
              if d == "BROKE EARLY"] for rn in RUNNERS}
LOST_LOUD = {rn: [ln.strip() for _i, ln, _rc, n, d in SWEEP[rn]
                  if d == "GATE LOST" and n] for rn in RUNNERS}

for rn in RUNNERS:
    note("%s: lines whose deletion loses the gate" % rn,
         "%d -- %s" % (len(LOST[rn]), LOST[rn] or "none"))
for rn in RUNNERS:
    note("%s: of those, printing e2's finding anyway" % rn, len(LOST_LOUD[rn]))
for rn in RUNNERS:
    note("%s: lines whose deletion breaks it before the gate" % rn,
         len(EARLY[rn]))
print()
score("P1a", [1, 1, 1], [len(LOST[r]) for r in RUNNERS])
score("P1e", 0, sum(1 for rn in RUNNERS
                    for _i, ln, _rc, _n, d in SWEEP[rn]
                    if d == "GATE LOST"
                    and (not ln.strip() or ln.strip().startswith("#"))))
score("P1f", True, all(len(EARLY[r]) > 0 for r in RUNNERS))
# P1c is a row of the sweep above and is read back out of it here rather than
# measured a second time: a prediction scored against a separate measurement
# of the same thing is two chances to be right.
HEADING_RC = [[rc for _i, ln, rc, _n, _d in SWEEP[rn] if ln.strip() == HEADING]
              for rn in RUNNERS]
score("P1c", [[1], [1], [1]], HEADING_RC)
print()


# ---------------------------------------------------------------------------
# V1d  DECLARED AGAINST MEASURED, AND THE RULE THAT KEEPS THE GATE LAST
# ---------------------------------------------------------------------------
hdr("V1d  THE DECLARED LOAD-BEARING SET AGAINST THE MEASURED ONE")

print("  DECLARED, by content and never by line number (mg-7522 S3): the one")
print("  line whose deletion may lose the verdict is the call itself.")
print("      %s" % CALL)
print()
DECLARED = {CALL}
for rn in RUNNERS:
    got = set(LOST[rn])
    ok = got == DECLARED
    row("%s: measured == declared" % rn, ok,
        "declared %s\nmeasured %s" % (sorted(DECLARED), sorted(got)))
score("P1d", True, all(set(LOST[r]) == DECLARED for r in RUNNERS))
print()

print("  AND THE SOURCE RULE.  The gate carries the verdict BECAUSE it is the")
print("  last command, so 'nothing may be appended below it' is not a")
print("  convention -- it is the rung, and it is asserted here against the")
print("  file rather than left in a comment for a reader to honour.")
print()
print("  A COMMENT after the call is not a violation and the rule says so:")
print("  what carries the status is the last COMMAND, and a comment is not")
print("  one.  mg-d633's e3_bothways.py appends a commented statement to one")
print("  of these files as a probe, and a rule that could not tell that from")
print("  an appended `echo` would be wrong in the direction of noise.")
print()
for rn in RUNNERS:
    lines = [l for l in SRC[rn].splitlines()
             if l.strip() and not l.lstrip().startswith("#")]
    last = lines[-1].strip() if lines else ""
    row("%s: the LAST command in the file is the call" % rn, last == CALL,
        "last non-blank, non-comment line: %s" % last[:60])
    idx = [i for i, l in enumerate(SRC[rn].splitlines())
           if l.strip() == CALL]
    above = SRC[rn].splitlines()[idx[0] - 1].strip() if idx else ""
    row("%s: the heading is the line immediately above it" % rn,
        above == HEADING, "found: %s" % above[:60])
    row("%s: `%s` appears exactly once" % (rn, SETE),
        len([l for l in SRC[rn].splitlines() if l.strip() == SETE]) == 1)
print()


# ---------------------------------------------------------------------------
# V1e  WHAT `set -e` STILL CARRIES
# ---------------------------------------------------------------------------
hdr("V1e  WITH `set -e` GONE, WHICH STEPS GO UNREPORTED?")

print("  The gate no longer needs `set -e`.  Other steps may.  A line that is")
print("  load-bearing is not a defect -- mg-6ef4's finding was a line that")
print("  was load-bearing AND OUTSIDE THE POPULATION.  So the remaining load")
print("  is measured and NAMED here instead of being left to a reader to")
print("  infer from the absence of a `||`.")
print()
print("  Each step is forced red by replacing its command with one that exits")
print("  1, leaving its redirect and any guard exactly as they are.  Two")
print("  worlds: `set -e` present, and `set -e` deleted.")
print()

CARRIES = {}
with Probe("v1e") as pr:
    for rn in RUNNERS:
        CARRIES[rn] = []
        print("  code/%s/run_all.sh" % rn)
        for i, ln in steps(SRC[rn]):
            forced = force_step(SRC[rn], i)
            pr.write(runner_path(rn), forced)
            rc_with, _o = run_runner(rn)
            pr.write(runner_path(rn), without(forced, SETE))
            rc_without, _o = run_runner(rn)
            carried = (rc_with != 0 and rc_without == 0)
            CARRIES[rn].append((ln.strip(), rc_with, rc_without, carried))
            print("      %-46s with %d  without %d  %s"
                  % (ln.strip()[:46], rc_with, rc_without,
                     "<- `set -e` IS THE ONLY RUNG" if carried else ""))
        pr.write(runner_path(rn), SRC[rn])
        print()
prove(pr)
print()
for rn in RUNNERS:
    n = len([1 for _l, _a, _b, c in CARRIES[rn] if c])
    note("%s: steps `set -e` alone reports" % rn, n)
print()
row("every step is reported when `set -e` is present",
    all(a != 0 for rn in RUNNERS for _l, a, _b, _c in CARRIES[rn]),
    "A step that fails and is reported by NOTHING is a silent green with no\n"
    "mutation needed at all, and would be a finding against the runner as\n"
    "it ships.")
print()
print("  THE THREE LINES `set -e` CARRIES ARE NAMED, WHICH IS THE POINT:")
for rn in RUNNERS:
    for lab, _a, _b, c in CARRIES[rn]:
        if c:
            print("      %-26s %s" % (rn, lab[:48]))
if not any(c for rn in RUNNERS for _l, _a, _b, c in CARRIES[rn]):
    print("      (none)")
print()
score("P2a", 0, len([1 for _l, _a, _b, c in CARRIES["species_repair_a4ef"]
                     if c]))
score("P2b", 0, len([1 for _l, _a, _b, c in CARRIES["species_remainder_f8fa"]
                     if c]))
score("P2c", 3, len([1 for _l, _a, _b, c in CARRIES["species_repair_6f61"]
                     if c]))
print()


# ---------------------------------------------------------------------------
# V1f  THE SAME DELETION AT THE PIN
# ---------------------------------------------------------------------------
hdr("V1f  `set -e` DELETED ALONE AT THE PIN (%s) AND AT HEAD" % PRE)

print("  mg-6ef4 measured 0/0/0 with the finding printed in full.  The")
print("  before-figure is re-derived here rather than quoted: the runners as")
print("  they were at the pin are written into this worktree, `set -e` is")
print("  deleted from each, and they are executed against the SAME planted")
print("  strike the rows above used.  Everything else in the tree is at HEAD,")
print("  which is stated because it is the one thing this comparison cannot")
print("  hold fixed -- the checkers are the repaired ones.  What is being")
print("  compared is the SHELL WIRING, and that is what is swapped.")
print()

PIN_SRC = {rn: show(PRE, runner_path(rn)) for rn in RUNNERS}
PINNED = {}
with Probe("v1f") as pr:
    pr.write(STRIKE_DOC, STRIKE_TEXT)
    for rn in RUNNERS:
        pr.write(runner_path(rn), PIN_SRC[rn])
        rc_a, out_a = run_runner(rn)
        pr.write(runner_path(rn), without(PIN_SRC[rn], SETE))
        rc_b, out_b = run_runner(rn)
        pr.write(runner_path(rn), without(SRC[rn], SETE))
        rc_c, out_c = run_runner(rn)
        PINNED[rn] = (rc_a, rc_b, E2_SAYS in out_b, rc_c, E2_SAYS in out_c)
        print("      %-26s pin: exit %d   pin less `%s`: exit %d (finding "
              "printed: %s)" % (rn, rc_a, SETE, rc_b,
                                "YES" if PINNED[rn][2] else "no"))
        print("      %-26s HEAD less `%s`: exit %d (finding printed: %s)"
              % ("", SETE, rc_c, "yes" if PINNED[rn][4] else "NO"))
        pr.write(runner_path(rn), SRC[rn])
prove(pr)
print()
row("at the PIN, deleting `%s` alone turns 3 of 3 runners GREEN" % SETE,
    all(PINNED[r][1] == 0 for r in RUNNERS),
    "This row being `ok` is mg-6ef4's F3 reproduced independently.  If it\n"
    "is a FINDING the before-state was not what F3 described and the\n"
    "after-state below proves less than it appears to.")
row("and 3 of 3 print e2's finding while doing it",
    all(PINNED[r][2] for r in RUNNERS))
row("at HEAD, deleting `%s` alone leaves 3 of 3 RED" % SETE,
    all(PINNED[r][3] == 1 for r in RUNNERS),
    "THIS IS THE REPAIR.  The gate's return is the call's, the call is the\n"
    "last command, and `set -e` is no longer between e2 and the reader.")
row("and 3 of 3 still print e2's finding",
    all(PINNED[r][4] for r in RUNNERS))
score("P1b", [1, 1, 1], [PINNED[r][3] for r in RUNNERS])
print()


print("=" * 78)
print("V1 TOTAL BAD: %d" % bad)
print("V1 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THAT NUMBER.  It ranges over %d runner executions in V1c --"
      % TOTAL)
print("every line of %d files, deleted one at a time, with nothing excluded"
      % len(RUNNERS))
print("-- plus %d step substitutions in V1e and %d pinned runs in V1f.  It"
      % (sum(len(CARRIES[r]) for r in RUNNERS) * 2, len(RUNNERS) * 3))
print("says NOTHING about any runner outside those three, about deletions of")
print("MORE than one line at a time, or about any failure mode of e2 other")
print("than the planted B1.  A population is a claim about what was tried,")
print("and two lines deleted together were not tried.")
sys.exit(1 if bad else 0)
