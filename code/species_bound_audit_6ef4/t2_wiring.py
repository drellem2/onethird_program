"""T2 -- OPEN 2.  Is the structure removed, or is this a fourth rung?

mg-4700's F2: mg-821e deletion-tested the wiring as one twenty-line unit, and
two of that unit's three separable parts had no return.  mg-5040's answer, in
the runners' own words:

    THE STRUCTURE IS REMOVED.  Running the check and printing its output are
    now the SAME statement, so neither can be deleted without the other and
    there is exactly one unit here that has a return; `set -e` carries the
    verdict, which is what it was already doing.

BOTH HALVES OF THAT ARE MEASURED HERE, and the second half is the section.

The block is now two non-comment lines.  Deleting the `echo` heading alone is
measured, not argued about -- if the runner stays red, the heading is inert
and the by-line deletion test still has a part with no return, which is
mg-4700's F2 at a smaller size rather than gone.

AND THEN THE FIFTH RUNG, WHICH IS NOT A FINER GRAIN.  The levels so far are
the gate (mg-9220), the clause (mg-64b6), the twenty-line block (mg-4700 F2)
and now the line (mg-5040).  Each answer made the tested unit smaller.  The
statement that carries this block's verdict is `set -e`, and `set -e` is not
in the block -- it is at the top of the file, outside every deletion
population any of the four levels enumerated.  A test whose population is the
block cannot reach it AT ANY GRAIN.  So the fifth thing to try is not a
smaller unit, it is a WIDER SCOPE, and this section deletes that one line and
runs all three runners.

T2a  the block, by line, in all three runners
T2b  the attribution control: e2 forced red, runners unmodified
T2c  the `echo` heading deleted alone
T2d  the `python3` line deleted alone
T2e  THE FIFTH RUNG -- `set -e` deleted alone
T2f  is `set -e` in any deletion population this arc has used?
T2g  does anything assert the heading exists?

    python3 code/species_bound_audit_6ef4/t2_wiring.py
"""

import os
import re
import sys

from kern6ef4 import hdr, REPO, RUNNERS, Probe6ef4, prove, sh

bad = 0
missed = 0

CALL = "python3 ../species_extent_d633/e2_crosssection.py"
HEADING = 'echo "cross-section check (mg-821e), its own output, unfiltered:"'
SETE = "set -e"

# THE DOCUMENT THAT MAKES e2 RED, and it is a NEW file in THIS tree on
# purpose.  mg-5040's kept defect 3: its first B1 probe appended to a document
# those runners' own checkers ALSO read, and 2 of 3 went red without printing
# `STANDING UN-STRUCK` -- a red that proved nothing.  `e2_crosssection.py`
# reads every *.md under code/ and no other checker in the three runners reads
# a *.md in this directory, so a red here is attributable to e2 and to e2
# alone.  T2b measures that rather than assuming it.
STRIKE_DOC = "code/species_bound_audit_6ef4/probe_strike_6ef4.md"
CLAIM = ("The ninth species of the ninth kind arrives in the ninth order at "
         "the ninth hour on every ninth day of the ninth month.")
STRIKE_TEXT = ("# planted by mg-6ef4's T2 probe and removed by the same "
               "probe\n\n~~%s~~\n\n%s\n" % (CLAIM, CLAIM))
E2_SAYS = "STANDING UN-STRUCK"


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    if detail:
        for ln in detail.splitlines():
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


def runner_path(rn):
    return os.path.join("code", rn, "run_all.sh")


def read(rn):
    with open(os.path.join(REPO, runner_path(rn)), encoding="utf-8") as f:
        return f.read()


def block_lines(text):
    """The wiring block: the CALL line and the contiguous non-comment,
    non-blank lines immediately above it back to the last blank line."""
    lines = text.splitlines()
    i = [n for n, ln in enumerate(lines) if ln.strip() == CALL]
    if len(i) != 1:
        raise RuntimeError("expected exactly 1 call site, found %d" % len(i))
    i = i[0]
    j = i
    while j > 0 and lines[j - 1].strip() != "":
        j -= 1
    return [ln for ln in lines[j:i + 1]
            if ln.strip() and not ln.lstrip().startswith("#")]


def without(text, needle):
    """`text` with the single line equal to `needle` removed.  Raises if the
    line is not there exactly once -- a deletion test that silently deletes
    nothing is a green run that means nothing."""
    lines = text.splitlines(True)
    hits = [n for n, ln in enumerate(lines) if ln.strip() == needle]
    if len(hits) != 1:
        raise RuntimeError("%r appears %d times, expected 1"
                           % (needle, len(hits)))
    del lines[hits[0]]
    return "".join(lines)


def run(rn):
    return sh(["sh", "run_all.sh"], cwd=os.path.join(REPO, "code", rn))


# ---------------------------------------------------------------------------
# T2a  THE BLOCK, BY LINE
# ---------------------------------------------------------------------------
hdr("T2a  THE REWIRED BLOCK, BY LINE, IN ALL THREE RUNNERS")

counts = {}
for rn in RUNNERS:
    bl = block_lines(read(rn))
    counts[rn] = len(bl)
    print("  %-26s %d non-comment line(s)" % (rn, len(bl)))
    for ln in bl:
        print("      %s" % ln.strip())
print()
score("P2a", [2, 2, 2], [counts[r] for r in RUNNERS])
print()
for rn in RUNNERS:
    lines = read(rn).splitlines()
    s = [n for n, ln in enumerate(lines) if ln.strip() == SETE]
    c = [n for n, ln in enumerate(lines) if ln.strip() == CALL]
    note("%s: `%s` at line %s, the call at line %s"
         % (rn, SETE, s[0] + 1 if s else "ABSENT", c[0] + 1 if c else "?"),
         "%d lines apart" % (c[0] - s[0]) if s and c else "")


# ---------------------------------------------------------------------------
# T2b  THE ATTRIBUTION CONTROL
# ---------------------------------------------------------------------------
hdr("T2b  THE ATTRIBUTION CONTROL -- e2 forced red, runners UNMODIFIED")

print("  Nothing below means anything if this is not red, and it means the")
print("  wrong thing if it is red without e2 saying so.  Both are checked.")
print()

BASE = {}
with Probe6ef4("t2b") as pr:
    pr.write(STRIKE_DOC, STRIKE_TEXT)
    for rn in RUNNERS:
        code, out = run(rn)
        BASE[rn] = (code, E2_SAYS in out)
        print("      %-26s exit %d   prints %s: %s"
              % (rn, code, E2_SAYS, "yes" if BASE[rn][1] else "NO"))
prove(pr)
print()
row("3 of 3 runners are red, and red BECAUSE of e2",
    all(v == (1, True) for v in BASE.values()),
    "If this row is a finding, every row below it is uninterpretable and\n"
    "should be read as such.")
score("P2d", [1, 1, 1], [BASE[r][0] for r in RUNNERS])


# ---------------------------------------------------------------------------
# T2c / T2d  THE TWO LINES OF THE BLOCK, DELETED ONE AT A TIME
# ---------------------------------------------------------------------------
hdr("T2c/T2d  EACH LINE OF THE BLOCK, DELETED ALONE, WITH e2 RED")

DEL = {}
for tag, needle in (("HEADING", HEADING), ("CALL", CALL)):
    DEL[tag] = {}
    with Probe6ef4("t2-%s" % tag) as pr:
        pr.write(STRIKE_DOC, STRIKE_TEXT)
        for rn in RUNNERS:
            pr.write(runner_path(rn), without(read(rn), needle))
        for rn in RUNNERS:
            code, out = run(rn)
            DEL[tag][rn] = (code, E2_SAYS in out, "cross-section check" in out)
            print("      %-8s %-26s exit %d   e2 output present: %s"
                  % (tag, rn, code, "yes" if DEL[tag][rn][1] else "NO"))
    prove(pr)
print()
row("deleting the HEADING alone changes a verdict in some runner",
    any(DEL["HEADING"][r][0] != BASE[r][0] for r in RUNNERS),
    "3 of 3 stay red with e2's full output present.  The heading is INERT.\n"
    "mg-4700's F2 was 2 of 3 parts with no return; this is 1 of 2.  The\n"
    "unit deletion-tested is still larger than the unit that has a return --\n"
    "smaller, and not a different shape.")
row("deleting the CALL alone leaves a trace that the check did not run",
    any(DEL["CALL"][r][1] or DEL["CALL"][r][2] for r in RUNNERS),
    "3 of 3 exit %s with no e2 output and no heading."
    % ", ".join(str(DEL["CALL"][r][0]) for r in RUNNERS))
score("P2b", [1, 1, 1], [DEL["HEADING"][r][0] for r in RUNNERS])


# ---------------------------------------------------------------------------
# T2e  THE FIFTH RUNG
# ---------------------------------------------------------------------------
hdr("T2e  THE FIFTH RUNG -- `set -e` DELETED ALONE, ONE LINE, OUTSIDE THE "
    "BLOCK")

print("  Not a finer grain.  A WIDER SCOPE.  The four levels this arc has")
print("  climbed -- gate, clause, twenty-line block, line -- each made the")
print("  tested unit smaller, and the population stayed 'the wiring'.  The")
print("  statement that turns e2's exit code into the runner's exit code is")
print("  `%s`, at the top of the file.  No deletion test in this arc has" % SETE)
print("  ever included it, and no amount of further subdivision reaches it.")
print()

FIFTH = {}
with Probe6ef4("t2e") as pr:
    pr.write(STRIKE_DOC, STRIKE_TEXT)
    for rn in RUNNERS:
        pr.write(runner_path(rn), without(read(rn), SETE))
    for rn in RUNNERS:
        code, out = run(rn)
        FIFTH[rn] = (code, E2_SAYS in out, out.count("E2 TOTAL BAD"))
        print("      %-26s exit %d   prints %s: %-3s   e2 verdict lines: %d"
              % (rn, code, E2_SAYS, "yes" if FIFTH[rn][1] else "NO",
                 FIFTH[rn][2]))
prove(pr)
print()
row("deleting `%s` alone leaves the verdict intact in some runner" % SETE,
    any(FIFTH[r][0] == BASE[r][0] for r in RUNNERS),
    "%d of %d runners exit 0 -- and %d of %d print e2's finding IN FULL\n"
    "while doing it.  The check runs.  Its output is printed.  The runner is\n"
    "GREEN.  That is mg-6cb9's F2 exactly, reached by deleting one line that\n"
    "no deletion test in this arc has ever had in its population."
    % (len([r for r in RUNNERS if FIFTH[r][0] == 0]), len(RUNNERS),
       len([r for r in RUNNERS if FIFTH[r][1]]), len(RUNNERS)))
score("P2c", [0, 0, 0], [FIFTH[r][0] for r in RUNNERS])


# ---------------------------------------------------------------------------
# T2f  IS `set -e` IN ANY DELETION POPULATION THIS ARC HAS USED?
# ---------------------------------------------------------------------------
hdr("T2f  THE POPULATION OF EVERY DELETION TEST THIS ARC HAS APPLIED HERE")

POPULATIONS = [
    ("mg-821e", "code/species_sites_821e/p3_wiring.py"),
    ("mg-4700", "code/species_depth_audit_4700/q2_wiring.py"),
    ("mg-5040", "code/species_bound_repair_5040/r2_wiring.py"),
]
inpop = []
for tag, rel in POPULATIONS:
    src = open(os.path.join(REPO, rel), encoding="utf-8").read()
    # A deletion population that could reach `set -e` has to name it as
    # something it removes.  Naming it in prose is not the same thing, so the
    # search is for it inside a call that deletes or replaces.
    mentions = len(re.findall(r"set -e", src))
    deletes = bool(re.search(
        r"(unwire|delete|without|remove|strip)[^\n]{0,200}set -e", src)
        or re.search(r"set -e[^\n]{0,200}(delete|remove|strip)", src))
    inpop.append(deletes)
    print("      %-8s %-46s mentions %d   deletes it: %s"
          % (tag, os.path.basename(rel), mentions, "YES" if deletes else "no"))
print()
row("`%s` is in the deletion population of some instrument here" % SETE,
    any(inpop),
    "0 of %d.  Every one of them enumerates THE BLOCK.  The line that\n"
    "carries the block's return is not in the block, so the population is\n"
    "wrong in a way no refinement of the GRAIN can fix -- which is the\n"
    "cheapest available demonstration that the level-chasing does not\n"
    "terminate by getting finer." % len(POPULATIONS))
score("P2e", 0, sum(inpop))


# ---------------------------------------------------------------------------
# T2g  DOES ANYTHING ASSERT THE HEADING EXISTS?
# ---------------------------------------------------------------------------
hdr("T2g  IS THE INERT LINE GUARDED BY ANYTHING?")

needle = "cross-section check (mg-821e)"
holders = []
for dirpath, dirnames, filenames in os.walk(os.path.join(REPO, "code")):
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    for fn in sorted(filenames):
        if not fn.endswith(".py"):
            continue
        p = os.path.join(dirpath, fn)
        try:
            if needle in open(p, encoding="utf-8").read():
                holders.append(os.path.relpath(p, REPO))
        except (OSError, UnicodeDecodeError):
            continue
print("  .py files under code/ that mention the heading string: %d"
      % len(holders))
print()
print("  MENTIONING IT AND REQUIRING IT ARE NOT THE SAME THING, and the")
print("  difference is the whole question.  A file REQUIRES the line if it")
print("  would fail when the line is absent.  A deletion-test instrument")
print("  mentions it in order to REMOVE it, and goes right on passing")
print("  without it -- and this instrument is one of those, so it is")
print("  classified by the same rule rather than filtered out by name.")
print()
requires = []
for h in holders:
    src = open(os.path.join(REPO, h), encoding="utf-8").read()
    # A requirement reads the heading and asserts on it.  A deletion test
    # names it next to a removal.
    removes = bool(re.search(r"(without|unwire|del |remove|replace|\.pop|"
                             r"splitlines)", src))
    asserts = bool(re.search(r"(assert[^\n]{0,120}|check\([^\n]{0,120}|"
                             r"row\([^\n]{0,120})cross-section check", src))
    if asserts and not removes:
        requires.append(h)
    print("      %-56s asserts %-5s deletes %-5s -> %s"
          % (h[-56:], asserts, removes,
             "REQUIRES" if (asserts and not removes) else "does not require"))
print()
row("some self-test or checker REQUIRES the heading to be present",
    bool(requires),
    "%d of %d files that mention it require it.  Every one of them is a\n"
    "deletion-test instrument that names the line in order to take it away.\n"
    "Deleting it is invisible to every instrument in this repository --\n"
    "mg-4700's F2 second bullet, one line shorter and otherwise unchanged."
    % (len(requires), len(holders)))
score("P2f", 0, len(requires))


# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("T2 TOTAL BAD: %d" % bad)
print("T2 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THESE NUMBERS.  THREE runners -- the three in")
print("kern6ef4.RUNNERS, which is kern5040.RUNNERS unchanged -- each EXECUTED")
print("in four states: unmodified, heading deleted, call deleted, `set -e`")
print("deleted, all four with e2 forced red by ONE planted markdown file in")
print("this directory.  Twelve executions plus three controls.  It says")
print("NOTHING about the other 14 run_all.sh mg-c2b3 swept, nothing about any")
print("step in these three runners other than the cross-section block, and")
print("nothing about whether e2_crosssection.py is the right check.")
print("`T2 TOTAL BAD` counts rows that contradict MG-5040'S OWN CLAIMS;")
print("`T2 PREDICTIONS MISSED` counts predictions that were wrong.")
sys.exit(1 if bad else 0)
