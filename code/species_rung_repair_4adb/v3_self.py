"""V3 -- THIS INSTRUMENT, HELD TO THE RULE IT SHIPS.

    This deliverable is of the same kind as the defect it repairs -- it
    defines populations for controls and writes runners that exit on
    conditions.  Check that your own deletion population contains every line
    your gate depends on, and that every runner you touch can go red.

So the two questions V1 asks of the three species runners are asked of
`code/species_rung_repair_4adb/run_all.sh`.

WHAT IS EXECUTED, AND WHY IT IS NOT THIS FILE'S OWN RUNNER VERBATIM.  V1 can
execute its subjects because they are not V1.  This runner calls V3, so
executing it here does not terminate.  What is executed instead is a STAND-IN:
the runner's own bytes with every `python3 ...` COMMAND -- and only the command
-- replaced by one whose exit code this probe chooses.  The redirects, the
`||` guards, the `RC` assignments, the `exit`, the comments and the blank lines
are the file's own, byte for byte.

That is a real limitation and it is stated rather than glossed: V3 measures
THE WIRING of this runner and not its checkers.  The checkers are measured by
being run -- V1, V2 and V4 are what this runner executes, and their transcripts
are committed beside it.  A stand-in that reported on the checkers would be the
defect mg-6cb9's F2 is about, a call present in a script taken as evidence of
execution.

THE ONE THING THAT IS NOT BYTE-IDENTICAL, AND WHY.  Every TRANSCRIPT PATH in
an executable line is rebound to a scratch directory -- the redirect targets
and the `cat` arguments together, because rebinding only the first would leave
each `cat` reading a file its own step no longer wrote and every mutant would
be red for that reason instead of the one being asked about.

The rebinding is not tidiness.  `out_v3_self.txt` is one of those paths, and
it is the file THIS PROBE'S OWN STDOUT is being written to by the runner that
called it: a stand-in using the file's own target would truncate the
transcript under its author mid-run.  `out_v4_neighbours.txt` is another, and
it does not exist yet when v3 runs.

The redirect OPERATORS, the `||` guards, the `RC` assignments, the `exit`, the
comments and the blank lines are the file's own.  A side effect worth having:
a mutant with `cd "$(dirname "$0")"` deleted now writes nothing at the
repository root either.

  V3a  the population of this runner: every line, deleted alone
  V3b  every step forced red, one at a time -- can this runner go red?
  V3c  does this runner's exit status depend on `set -e`?

    python3 code/species_rung_repair_4adb/v3_self.py
"""

import os
import re
import shutil
import sys
import tempfile

from kern4adb import (hdr, REPO, Probe, prove, sh, drop_index, without,
                      steps, SETE, disposition)

bad = 0
missed = 0

SELF = os.path.join("code", "species_rung_repair_4adb", "run_all.sh")
STANDIN = os.path.join("code", "species_rung_repair_4adb", "run_all_v3.sh")
MARK = "V3 STAND-IN STEP"

with open(os.path.join(REPO, SELF), encoding="utf-8") as _f:
    SRC = _f.read()


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
    print("  %-6s predicted %-24s got %-24s %s"
          % (pid, str(predicted), str(got), "" if hit else "*** MISSED ***"))
    return hit


SCRATCH = tempfile.mkdtemp(prefix="mg4adb-v3-")


def standin(text, red_line=None):
    """`text` with every step's COMMAND replaced by a stand-in.

    `red_line` is the STRIPPED CONTENT of the step that must exit 1, never its
    index (mg-7522's S3): every mutant here is a file with a line taken out,
    so an index computed against one version of the file names a different
    line in the next.
    """
    lines = text.splitlines(True)
    for i, ln in steps(text):
        stripped = ln.lstrip()
        indent = ln[:len(ln) - len(stripped)]
        m = re.match(r"python3\s+(?:-B\s+)?\S+\s*(.*)$", stripped.rstrip("\n"))
        rest = m.group(1) if m else ""
        rc = 1 if (red_line is not None and ln.strip() == red_line) else 0
        cmd = ("python3 -c \"print('%s'); import sys; sys.exit(%d)\""
               % (MARK, rc))
        lines[i] = "%s%s %s\n" % (indent, cmd, rest)
    # Every transcript path in an EXECUTABLE line is rebound to the scratch
    # directory; comments are left alone so the file still reads as itself.
    # See the module docstring for the two files that make this necessary.
    for i, ln in enumerate(lines):
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        lines[i] = re.sub(r"(?<![/\w])(out_[\w*]*\.txt)",
                          lambda mm: os.path.join(SCRATCH, mm.group(1)), ln)
    return "".join(lines)


def run_standin(text):
    """Write `text` as the stand-in runner and execute it FROM THE REPOSITORY
    ROOT -- the same working directory V1 uses, so that a mutant which has
    lost its `cd` is measured and not accommodated."""
    p = os.path.join(REPO, STANDIN)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    try:
        return sh(["sh", STANDIN], cwd=REPO)
    finally:
        os.unlink(p)


STEPS = [ln.strip() for _i, ln in steps(SRC)]
LAST_STEP = STEPS[-1]


# ---------------------------------------------------------------------------
# V3a  THE POPULATION
# ---------------------------------------------------------------------------
hdr("V3a  EVERY LINE OF THIS INSTRUMENT'S RUNNER, DELETED ALONE")

print("  The population is every line of %s," % SELF)
print("  with nothing excluded, for the reason V1a gives.  Each mutant runs")
print("  with ONE step forced red -- the last one, so that every guard above")
print("  it has already had to carry a passing step -- and a mutant that")
print("  exits 0 has lost the verdict.")
print()
note("the step forced red in every row below", LAST_STEP[:52])
print()

with Probe("v3a") as pr:
    BASE_RC, BASE_OUT = run_standin(standin(SRC, LAST_STEP))
    GREEN_RC, _g = run_standin(standin(SRC, None))
    print("      stand-in, no step red      exit %d" % GREEN_RC)
    print("      stand-in, last step red    exit %d" % BASE_RC)
    print()
    SWEEP = []
    for i, ln in enumerate(SRC.splitlines()):
        mutant = standin(drop_index(SRC, i), LAST_STEP)
        rc, out = run_standin(mutant)
        d = disposition(rc, MARK in out)
        SWEEP.append((i, ln, rc, d))
        print("      line %3d  exit %d  %-11s  %s"
              % (i + 1, rc, d, ln.strip()[:44]))
prove(pr)
print()

row("with no step red the runner is GREEN", GREEN_RC == 0)
row("with the last step red the runner is RED", BASE_RC == 1)
LOST = [ln.strip() for _i, ln, rc, _d in SWEEP if rc == 0]
note("lines whose deletion loses the verdict", len(LOST))
for l in LOST:
    print("        %s" % l[:70])
print()

# DECLARED, by content.  Deleting the forced step itself removes the failure,
# so that mutant is correctly green: it is a different question being asked,
# not a lost verdict.  `exit $RC` is the statement that carries the verdict out
# of this file, and deleting it must lose it -- that is what makes it the rung
# rather than a decoration.  Anything else that turns this runner green is a
# finding.
DECLARED = set(STEPS) | {"exit $RC"}
UNDECLARED = [l for l in LOST if l not in DECLARED]
row("no line outside the declared set turns this runner green",
    not UNDECLARED, "undeclared: %s" % UNDECLARED)
row("`exit $RC` IS in the measured set -- this runner's own fifth rung",
    "exit $RC" in LOST,
    "If deleting it changed nothing, the verdict would be resting on\n"
    "something else again, and that something would be the next F3.")
score("P4a", True, not UNDECLARED)
print()


# ---------------------------------------------------------------------------
# V3b  EVERY STEP, FORCED RED ONE AT A TIME
# ---------------------------------------------------------------------------
hdr("V3b  EVERY STEP OF THIS RUNNER, FORCED RED ONE AT A TIME")

print("  `every runner you touch can go red` is a claim about EVERY step, not")
print("  about the runner as a whole.  A runner that reddens for its first")
print("  step and swallows its fourth is a green run away from mg-6cb9's F2.")
print()

PER_STEP = []
with Probe("v3b") as pr:
    for line in STEPS:
        rc, out = run_standin(standin(SRC, line))
        PER_STEP.append((line, rc))
        print("      %-52s exit %d  %s"
              % (line[:52], rc, "" if rc else "*** SWALLOWED ***"))
prove(pr)
print()
row("every step of this runner reddens it when it fails",
    all(rc != 0 for _l, rc in PER_STEP))
score("P4b", True, all(rc != 0 for _l, rc in PER_STEP))
print()


# ---------------------------------------------------------------------------
# V3c  DOES THIS RUNNER DEPEND ON `set -e`?
# ---------------------------------------------------------------------------
hdr("V3c  THE QUESTION mg-6ef4 ASKED OF THE THREE SUBJECTS, ASKED HERE")

has_sete = len([l for l in SRC.splitlines() if l.strip() == SETE])
note("`%s` appears in this runner" % SETE, "%d time(s)" % has_sete)
print()

WITHOUT = []
with Probe("v3c") as pr:
    base = without(SRC, SETE) if has_sete == 1 else SRC
    for line in STEPS:
        rc, out = run_standin(standin(base, line))
        WITHOUT.append((line, rc))
        print("      %-46s without `%s`: exit %d  %s"
              % (line[:46], SETE, rc, "" if rc else "*** SWALLOWED ***"))
prove(pr)
print()
row("deleting `%s` from this runner changes no verdict" % SETE,
    [rc for _l, rc in WITHOUT] == [rc for _l, rc in PER_STEP],
    "with:    %s\nwithout: %s" % ([rc for _l, rc in PER_STEP],
                                  [rc for _l, rc in WITHOUT]))
last = [l for l in SRC.splitlines() if l.strip()][-1].strip()
row("the last statement of this runner is an explicit `exit`",
    last.startswith("exit "), "last non-blank line: %s" % last)
score("P4c", True, [rc for _l, rc in WITHOUT] == [rc for _l, rc in PER_STEP])
print()


print("=" * 78)
print("V3 TOTAL BAD: %d" % bad)
print("V3 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THAT NUMBER.  %d line deletions and %d step substitutions"
      % (len(SWEEP), len(STEPS) * 2))
print("over ONE file, %s," % SELF)
print("executed as a STAND-IN whose commands are replaced and whose control")
print("flow is the file's own.  It says NOTHING about whether the checkers")
print("this runner calls are correct -- that is what V1, V2 and V4 are, and")
print("this runner executes them.")
shutil.rmtree(SCRATCH, ignore_errors=True)
sys.exit(1 if bad else 0)
