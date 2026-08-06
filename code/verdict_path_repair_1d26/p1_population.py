"""P1 -- THE POPULATION THE GATE IS ACTUALLY CERTIFIED OVER, DERIVED.

mg-d53d's finding is that mg-4adb's certified population was NARROWER THAN THE
VERDICT PATH: 255 lines certified, 806 lines able to change the verdict.  The
whole defect is an inherited boundary, so a repair that re-uses mg-d53d's own
five-file list and certifies THAT reproduces the error one level up.

This section derives the population from a RULE, walking outward from the
runner, and prints the closure it walked file by file with the grain of every
number beside it:

    the runner file
      -> the script its LAST COMMAND invokes
        -> the transitive closure of that script's repository-local imports

  P1a  the rule, applied to each of the three runners, and the closure printed
  P1b  what the closure resolved and what it could not
  P1c  mg-4adb's certified population, parsed out of its own transcript, and
       the arithmetic of what it does not cover
  P1d  the source rule that makes the last command the verdict-carrier

    python3 code/verdict_path_repair_1d26/p1_population.py
"""

import os
import re
import sys

from kern1d26 import (hdr, Rows, REPO, RUNNERS, E2, KERN, V1_TRANSCRIPT,
                      clone, cleanup, source_lines, verdict_path,
                      last_command, local_imports)

R = Rows()
base = clone()


# ---------------------------------------------------------------------------
hdr("P1a  THE VERDICT PATH, DERIVED FROM THE RUNNER OUTWARD")
# ---------------------------------------------------------------------------

R.note("The rule is stated once and applied three times.  Nothing below is")
R.note("read from mg-d53d's list of five files; the list is COMPARED against")
R.note("what the rule returns, in P1a's last row, and if the rule returns more")
R.note("then the hole is wider than mg-d53d's number too.")
print()

PATHS = {}
for rn in RUNNERS:
    rel, cmd, files, unres = verdict_path(base, rn)
    PATHS[rn] = (rel, cmd, files, unres)
    R.note("  %s" % rn)
    R.note("      last command: %s" % cmd)
    for f in files:
        R.note("      %-52s %3d line(s)" % (f, len(source_lines(base, f))))
    if unres:
        R.note("      UNRESOLVED: %s" % ", ".join(unres))
print()

UNION = []
for rn in RUNNERS:
    for f in PATHS[rn][2]:
        if f not in UNION:
            UNION.append(f)
LINES = {f: len(source_lines(base, f)) for f in UNION}
TOTAL = sum(LINES.values())

R.note("THE UNION OVER THE THREE RUNNERS -- the population of this repair:")
for f in UNION:
    R.note("    %-56s %3d line(s)" % (f, LINES[f]))
R.note("    %-56s %3d line(s)" % ("TOTAL", TOTAL))
R.note("")
R.note("GRAIN.  %d is the LINE grain over %d FILES.  The file grain is %d and"
       % (TOTAL, len(UNION), len(UNION)))
R.note("they are not interchangeable: mg-d53d's 806 is the line grain over the")
R.note("same five files at the commit it ran, and this repair has since added")
R.note("lines to two of them, so the two numbers are over the same POPULATION")
R.note("and different TREES.")
print()

D53D_FIVE = sorted([os.path.join("code", r, "run_all.sh") for r in RUNNERS]
                   + [E2, KERN])
same = sorted(UNION) == D53D_FIVE
R.predicted(
    "P1a", "exactly five files -- the same five mg-d53d names",
    "%d file(s): %s" % (len(UNION), ", ".join(sorted(UNION))),
    same,
    "mg-d53d's five are named here ONLY as the object of this comparison.\n"
    "Every line count above was taken from the source in the sandbox.")

extra = [f for f in UNION if f not in D53D_FIVE]
missing = [f for f in D53D_FIVE if f not in UNION]
R.row("the derived closure contains no file mg-d53d's list omits", not extra,
      "\n".join(extra) or "(none)")
R.note("  files in mg-d53d's list that the rule does NOT reach: %s"
       % (", ".join(missing) or "(none)"))


# ---------------------------------------------------------------------------
hdr("P1b  WHAT THE CLOSURE RESOLVED, AND WHAT IT COULD NOT")
# ---------------------------------------------------------------------------

R.note("An import this rule cannot resolve is a piece of the verdict path it")
R.note("cannot certify, so it is RETURNED and printed rather than dropped.")
print()

res_e2, unres_e2 = local_imports(base, E2)
res_kern, unres_kern = local_imports(base, KERN)
R.note("  %s imports, repository-local: %s"
       % (E2, ", ".join(res_e2) or "(none)"))
R.note("      unresolved: %s" % (", ".join(unres_e2) or "(none)"))
R.note("  %s imports, repository-local: %s"
       % (KERN, ", ".join(res_kern) or "(none)"))
R.note("      unresolved: %s" % (", ".join(unres_kern) or "(none)"))
print()

SIBLINGS = ["trace_open.py", "e1_extents.py", "e3_bothways.py",
            "selftestd633.py"]
d = os.path.dirname(E2)
off_path = [s for s in SIBLINGS
            if os.path.join(d, s) not in UNION]
R.predicted(
    "P1b", "the closure adds nothing beyond kernd633.py, nothing is "
           "unresolved, and trace_open/e1_extents/e3_bothways are NOT on it",
    "closure beyond e2: %s; unresolved: %s; of the four siblings, %d are off "
    "the path"
    % (", ".join(res_e2) or "(none)",
       ", ".join(unres_e2 + unres_kern) or "(none)", len(off_path)),
    res_e2 == [os.path.join("code", "species_extent_d633", "kernd633.py")]
    and not unres_e2 and not unres_kern and len(off_path) == len(SIBLINGS),
    "Those three run in `code/species_extent_d633/run_all.sh` and not in any\n"
    "of the three species runners, and none of them is imported by e2.  A\n"
    "line of theirs cannot change the verdict this gate carries.")


# ---------------------------------------------------------------------------
hdr("P1c  THE CERTIFIED POPULATION, AND WHAT IT DOES NOT COVER")
# ---------------------------------------------------------------------------

R.note("mg-4adb's `out_v1_population.txt` is read HERE and only here, as the")
R.note("OBJECT of a measurement: how many lines of which files its certificate")
R.note("ranges over.  No figure this instrument reports as its own comes from")
R.note("it.")
print()

CERT = {}
cur = None
with open(V1_TRANSCRIPT, encoding="utf-8") as fh:
    for ln in fh:
        m = re.match(r"^  (code/\S+/run_all\.sh)\s*$", ln)
        if m:
            cur = m.group(1).replace("/", os.sep)
            continue
        m = re.match(r"^      line\s+(\d+)\s+exit (\d+)\s+"
                     r"(gate fired|GATE LOST|BROKE EARLY)", ln)
        if m and cur:
            CERT[(cur, int(m.group(1)))] = m.group(3)

cert_files = sorted(set(k[0] for k in CERT))
R.note("  rows parsed out of mg-4adb's transcript: %d" % len(CERT))
for f in cert_files:
    R.note("      %-52s %3d row(s)" % (f, len([1 for k in CERT if k[0] == f])))
uncovered = [f for f in UNION if f not in cert_files]
uncovered_lines = sum(LINES[f] for f in uncovered)
R.note("")
R.note("  files of the verdict path with NO row in that certificate:")
for f in uncovered:
    R.note("      %-52s %3d line(s)" % (f, LINES[f]))
R.note("")
R.note("  verdict path, LINE grain, at this tree            %4d" % TOTAL)
R.note("  covered by the certified population               %4d" % len(CERT))
R.note("  NOT covered                                       %4d"
       % (TOTAL - len(CERT)))
R.note("  and the certificate over the covered %d reads 100%% -- correctly."
       % len(CERT))

R.predicted(
    "P1c", "255 rows over 3 files, so 551 lines of the verdict path have no "
           "certificate",
    "%d rows over %d file(s); %d lines uncovered AT THIS TREE"
    % (len(CERT), len(cert_files), TOTAL - len(CERT)),
    len(CERT) == 255 and len(cert_files) == 3,
    "The uncovered figure is scored on the ROW COUNT and the FILE COUNT only.\n"
    "551 was the line grain at mg-d53d's tree; this repair adds lines to two\n"
    "of the five files, so the uncovered LINE count moves with the repair and\n"
    "a prediction pinned to it would be scoring the size of the patch.")


# ---------------------------------------------------------------------------
hdr("P1d  THE SOURCE RULE THAT MAKES THE LAST COMMAND THE VERDICT-CARRIER")
# ---------------------------------------------------------------------------

R.note("The derivation above rests on one fact about POSIX sh -- a script's")
R.note("exit status is its last command's -- and on one fact about these three")
R.note("files, which is asserted against their source rather than against the")
R.note("comment in them that says it.")
print()

CALL = "python3 ../species_extent_d633/e2_crosssection.py"
lasts = []
for rn in RUNNERS:
    rel, cmd = last_command(base, rn)
    lasts.append(cmd)
    R.note("    %-30s %s" % (rn, cmd))
R.predicted(
    "P1d", "the last command of all three runners is `%s`" % CALL,
    "%d of 3 are" % sum(1 for c in lasts if c == CALL),
    all(c == CALL for c in lasts),
    "A comment in each of these files says the same thing.  A comment is not\n"
    "a measurement, and mg-4adb's V1d already reads the source for it; this\n"
    "row exists because the DERIVATION above would be wrong if it stopped\n"
    "being true, not to re-audit mg-4adb.")

R.tail("P1")
print()
print("EXTENT OF THESE NUMBERS.  They are read from the SOURCE of %d files in"
      % len(UNION))
print("a `git clone --shared` sandbox at this worktree's HEAD, with the two")
print("repaired files written in from the worktree.  NOTHING WAS EXECUTED IN")
print("THIS SECTION: P1 measures what the population IS, and P2 measures what")
print("deleting each member of it does.  The certified-population figures are")
print("parsed out of mg-4adb's committed transcript and are ITS measurements,")
print("re-counted here but not re-run.")

cleanup()
sys.exit(1 if R.bad else 0)
