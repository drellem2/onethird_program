"""G2 -- CAN EACH RUNNER GO RED?

A runner that cannot be made to fail is not a control, and this arc has
produced several: `w3_scope.py` ended in an unconditional `sys.exit(0)` and
says so in its own comment; three species runners printed e2's finding in full
and exited 0 (mg-6ef4 F3).  So every claim of the form "the runner catches it"
is asked here as a construction, not as a reading.

  G2a  every step of every runner forced red, one at a time
  G2b  a NATURAL input per runner -- not a substituted command
  G2c  `set -e` deleted alone, at HEAD and at the pin, with the finding
       printed in full both times

G2c is the re-test the ticket asks for by name: at the pin the exit status and
the printed content DISAGREE, which is the whole of mg-6ef4's F3, and at HEAD
they must agree.  A control demonstrated only against the tree that already
passes it has not been demonstrated.

    python3 code/species_gate_audit_d53d/g2_red.py
"""

import os
import re
import stat
import sys

from kern_d53d import (hdr, Rows, RUNNERS, PIN, SETE, E2_SAYS, FORCED,
                       clone, run_runner, plant_strike, read_lines,
                       write_lines, source_lines, force_step, steps_of,
                       cleanup)

R = Rows()
base = clone()


# ---------------------------------------------------------------------------
hdr("G2a  EVERY STEP OF EVERY RUNNER, FORCED RED ONE AT A TIME")
# ---------------------------------------------------------------------------

R.note("The step's COMMAND is replaced by one that exits 1 on stderr.  Its")
R.note("redirect and any `||` guard around it are left exactly as they were,")
R.note("so what is measured is the runner's wiring and not a runner this")
R.note("audit rewrote into one it liked better.")
print()

rows = []
for rn in RUNNERS:
    steps = steps_of(base, rn)
    print("  %s -- %d step(s)" % (rn, len(steps)))
    for k, (lineno, text) in enumerate(steps):
        rel, i, was = force_step(base, rn, k)
        try:
            rc, out = run_runner(base, rn)
        finally:
            lines = read_lines(base, rel)
            lines[i] = was
            write_lines(base, rel, lines)
        saw = "FORCED RED by mg-d53d" in out
        rows.append((rn, lineno, rc, saw))
        print("      step %d  line %-4d exit %-4s runner reported it: %-4s %s"
              % (k + 1, lineno, rc, "yes" if saw else "no", text[:34]))
    print()

nonzero = [r for r in rows if r[2] not in (0, None)]
R.predicted(
    "Q8", "15 of 15 leave the runner non-zero",
    "%d of %d non-zero (%d step(s): %s)"
    % (len(nonzero), len(rows), len(rows),
       " + ".join(str(len(steps_of(base, rn))) for rn in RUNNERS)),
    len(rows) == 15 and len(nonzero) == 15)

silent = [r for r in rows if r[2] not in (0, None) and not r[3]]
R.note("")
R.note("  of the %d red runs, %d did not carry the forced step's own words"
       % (len(nonzero), len(silent)))
for rn, lineno, rc, _saw in silent:
    R.note("      %s line %d (exit %s) -- red, but the reason is not in the"
           % (rn, lineno, rc))
    R.note("      output.  A reader gets a verdict and no finding.")
R.row("every step that CAN be made red IS made red", len(nonzero) == len(rows))


# ---------------------------------------------------------------------------
hdr("G2b  A NATURAL INPUT PER RUNNER")
# ---------------------------------------------------------------------------

R.note("G2a substitutes a command.  This does not: each runner is given an")
R.note("input of the kind its own checkers exist to find, and nothing in any")
R.note("runner or checker is modified.")
print()

nat = {}

# (i) a4ef -- a planted strike, which is e2's business and is the gate.
root = clone()
plant_strike(root)
rc, out = run_runner(root, "species_repair_a4ef")
nat["species_repair_a4ef"] = (rc, "a struck claim standing un-struck", out)

# (ii) f8fa -- an unreadable REGULAR FILE in the tree w3_scope.py walks.
root2 = clone()
victim = os.path.join(root2, "code", "species_7d75", "t1_grading.py")
os.chmod(victim, 0)
try:
    rc2, out2 = run_runner(root2, "species_remainder_f8fa")
finally:
    os.chmod(victim, stat.S_IRUSR | stat.S_IWUSR)
nat["species_remainder_f8fa"] = (rc2, "a regular file that cannot be read",
                                 out2)

# (iii) 6f61 -- a sentence check_doc.py stores as false, asserted un-struck.
#       The string is the VERBATIM entry from check_doc.py's own STRICKEN
#       table (§2.2, the control count).  An earlier version of this probe
#       used a PARAPHRASE of a different entry, and check_doc.py did not fire
#       on it -- e2 did, further down the same runner.  The runner still went
#       red, so Q9 still held, and the prose beside it saying which checker
#       caught it was WRONG.  Kept in OUTCOMES.md as a defect of this
#       instrument: the column below is now DERIVED from the run.
root3 = clone()
DOC = os.path.join(root3, "docs",
                   "OneThird-Species-Hopf-Monoids-Where-This-Lives.md")
STRICKEN_VERBATIM = "Three of the four columns are the control, and they fire."
with open(DOC, encoding="utf-8") as fh:
    doc = fh.read()
with open(DOC, "w", encoding="utf-8") as fh:
    fh.write(doc + "\n\n%s\n" % STRICKEN_VERBATIM)
rc3, out3 = run_runner(root3, "species_repair_6f61")
nat["species_repair_6f61"] = (rc3, "a stricken sentence asserted un-struck",
                              out3)


def caught_by(out):
    """Which checker made the finding, READ OUT OF THE RUN.

    A runner's exit code says it went red.  It does not say what caught it,
    and this audit has already once written down the wrong answer for that.

    The pattern is `^<anything> FAILED` and NOT `^<name>.py FAILED`: 6f61's
    guard prints `CHECK_DOC FAILED`, not `check_doc.py FAILED`, and the
    narrower pattern reported `(cannot be told from the output)` for a run
    whose very next line said which checker it was.  Second time in this
    section that a written-down answer lost to a read one."""
    m = re.search(r"^(\S+) FAILED", out, re.M)
    if m:
        return m.group(1)
    tots = re.findall(r"^([A-Z0-9_]+) TOTAL BAD: ([1-9]\d*)", out, re.M)
    if tots:
        return "%s (TOTAL BAD %s)" % (tots[-1][0], tots[-1][1])
    return "(cannot be told from the output)"


for rn in RUNNERS:
    rc, why, out = nat[rn]
    tot = re.findall(r"^[A-Z0-9_]+ TOTAL BAD: [1-9]\d*", out, re.M)
    nat[rn] = (rc, why, out, caught_by(out))
    R.note("    %-26s exit %-4s  %s" % (rn, rc, why))
    R.note("        caught by, read out of the run:  %s" % caught_by(out))
    R.note("        non-zero totals in that run:     %s"
           % (", ".join(t.strip() for t in tot) or "(none printed)"))

catchers = [nat[rn][3] for rn in RUNNERS]
named = [c for c in catchers if "cannot" not in c]
R.predicted(
    "Q9", "exit 1, 1, 1",
    ", ".join(str(nat[rn][0]) for rn in RUNNERS),
    all(nat[rn][0] == 1 for rn in RUNNERS),
    "Three different KINDS of input.  The checker each one reaches is read\n"
    "out of the run and not asserted: %s.\n"
    "A runner shown red by one substituted command has been shown to\n"
    "propagate an exit code; this is the other half." % ", ".join(catchers))
R.row("each of the three names a catcher, and the three are distinct",
      len(named) == 3 and len(set(named)) == 3,
      "A row that passes because `(cannot be told from the output)` is a\n"
      "distinct string from the other two would be this audit's own subject:\n"
      "an instrument reporting something other than what happened.  So both\n"
      "conditions are required and the names are printed above either way.")


# ---------------------------------------------------------------------------
hdr("G2c  `set -e` DELETED ALONE, AT HEAD AND AT THE PIN (%s)" % PIN)
# ---------------------------------------------------------------------------

R.note("The line is found by reading the source and matching it exactly, not")
R.note("by a line number: at the pin it sits 53, 60 and 43 lines above the")
R.note("cross-section call and at HEAD it does not.  Its line number is")
R.note("printed so a reader can see which line was removed.")
print()


def sete_probe(root, label):
    out_rows = []
    for rn in RUNNERS:
        rel = os.path.join("code", rn, "run_all.sh")
        lines = source_lines(root, rel)
        hits = [i for i, ln in enumerate(lines) if ln.strip() == SETE]
        if len(hits) != 1:
            R.row("%s: %s has %d `%s` line(s), expected 1"
                  % (label, rn, len(hits), SETE), False)
            continue
        i = hits[0]
        keep = list(lines)
        del lines[i]
        write_lines(root, rel, lines + [""])
        try:
            rc, out = run_runner(root, rn)
        finally:
            write_lines(root, rel, keep + [""])
        says = E2_SAYS in out
        n_standing = out.count("*** %s ***" % E2_SAYS)
        out_rows.append((rn, i + 1, rc, says, n_standing))
        R.note("    %-6s %-26s `%s` at line %-4d exit %-4s prints the "
               "finding: %-4s (%d occurrence(s))"
               % (label, rn, SETE, i + 1, rc, "yes" if says else "no",
                  n_standing))
    return out_rows


head_root = clone()
plant_strike(head_root)
head_rows = sete_probe(head_root, "HEAD")
print()
pin_root = clone(PIN)
plant_strike(pin_root)
pin_rows = sete_probe(pin_root, PIN)
print()

head_codes = [r[2] for r in head_rows]
head_says = [r[3] for r in head_rows]
pin_codes = [r[2] for r in pin_rows]
pin_says = [r[3] for r in pin_rows]

R.predicted(
    "Q10",
    "HEAD 1, 1, 1 with the finding printed 3 of 3 -- status and printed "
    "content AGREE; pin %s 0, 0, 0 with the finding printed 3 of 3 -- they "
    "DISAGREE" % PIN,
    "HEAD %s, finding printed %d of 3; pin %s, finding printed %d of 3"
    % (", ".join(str(c) for c in head_codes), sum(head_says),
       ", ".join(str(c) for c in pin_codes), sum(pin_says)),
    head_codes == [1, 1, 1] and all(head_says)
    and pin_codes == [0, 0, 0] and all(pin_says))

R.row("at HEAD, exit status and printed content agree",
      head_codes == [1, 1, 1] and all(head_says))
R.row("at the pin they disagree -- mg-6ef4's F3, reproduced by this "
      "instrument", pin_codes == [0, 0, 0] and all(pin_says),
      "This row is a FINDING if it does NOT reproduce: a repair whose\n"
      "before-state cannot be constructed is a repair to nothing, and every\n"
      "after-figure in mg-4adb would then prove less than it appears to.")

R.note("")
R.note("  THE DIFFERENCE, in one sentence.  At the pin `%s` is the statement"
       % SETE)
R.note("  that carries e2's exit code out of the file and it sits tens of")
R.note("  lines away from the call; at HEAD the CALL IS THE LAST COMMAND and a")
R.note("  POSIX script's status is its last command's, so deleting `%s`" % SETE)
R.note("  moves the message and not the verdict.  G1c measured that from the")
R.note("  other side: at HEAD the only runner line whose deletion loses the")
R.note("  gate is the call itself.")

R.tail("G2")
print()
print("EXTENT OF THAT NUMBER.  %d step substitutions in G2a, 3 natural inputs"
      % len(rows))
print("in G2b and %d `%s` deletions in G2c -- %d at HEAD and %d at %s."
      % (len(head_rows) + len(pin_rows), SETE, len(head_rows), len(pin_rows),
         PIN))
print("Every run is a whole runner executed in a git clone of this worktree.")
print("IT RANGES OVER NOTHING ELSE: G2a forces the steps a runner CALLS, so a")
print("checker that is never called cannot appear here, and G2b's three")
print("inputs are three, not a sample of a space.  `can this runner go red`")
print("is answered YES or NO for each; `does it go red for every finding its")
print("own battery can make` is a different question and is G5's.")

cleanup()
sys.exit(1 if R.bad else 0)
