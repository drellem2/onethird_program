"""V4 -- EVERY RUNNER AND PROBE THIS REPAIR TOUCHES, ENUMERATED AND EXECUTED.

    Check that your own deletion population contains every line your gate
    depends on, and that every runner you touch can go red.  Enumerate what
    you checked.

V1 and V2 execute the three species runners and the four checkers.  This file
is the rest of the enumeration: the instruments that READ or MUTATE the files
this ticket changed, and would therefore be the ones a repair like this breaks
without anybody noticing until much later.

EXIT CODE IS NOT THE ASSERTION FOR ALL OF THEM, AND SAYING SO IS THE POINT.
Two of these are AUDITS, and an audit with a standing finding exits 1 BY
DESIGN -- mg-6ef4's `t2_wiring.py` has four, one of which (T2f: `set -e` is in
the deletion population of none of the three earlier instruments) is a true
statement about those instruments that this repair does not and should not
change.  Asserting `exit 0` on it would be asking an audit to stop reporting.
So each row below carries the assertion that BELONGS to it, named, and the
exit code is printed beside it as information.

WHY THE PROBE AND NOT ALWAYS THE WHOLE RUNNER.  Two of these runners take tens
of minutes because their own probes execute the species runners twenty times
over.  Where the whole runner is cheap it is run.  Where it is not, THE FILE
THAT CARRIES THE DEPENDENCY is run, and which one that is, is named.

WHAT WOULD MAKE THIS SECTION WORTHLESS: a table of green rows with nothing
that could have been red.  V4b takes one of them and makes it red on purpose.

  V4a  the neighbours, run, each with the assertion that belongs to it
  V4b  one of them, forced red, so the rows above mean something

    python3 code/species_rung_repair_4adb/v4_neighbours.py
"""

import os
import sys

from kern4adb import (hdr, REPO, PRE, Probe, prove, run_checker, run_runner,
                      SETE, without, read_runner, runner_path, show)

bad = 0


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    for ln in detail.splitlines():
        if ln:
            print("        %s" % ln)


def note(label, value):
    print("  %-64s %s" % (label[:64], value))


def find_row(out, needle):
    """The one output line carrying `needle`, or ''."""
    hits = [l for l in out.splitlines() if needle in l]
    return hits[0] if hits else ""


hdr("V4a  THE NEIGHBOURS -- WHAT THIS REPAIR TOUCHES, AND WHAT IT DID TO THEM")

RESULTS = {}

# --- 1.  code/species_7d75 -------------------------------------------------
print("  1. code/species_7d75/run_all.sh -- the tree w3_scope.py and")
print("     s1_extent.py quantify over, and the tree V2 plants in.")
rc, out = run_runner("species_7d75")
RESULTS["species_7d75"] = rc
note("exit", rc)
row("species_7d75 is green", rc == 0)
print()

# --- 2.  code/species_extent_d633 ------------------------------------------
print("  2. code/species_extent_d633/run_all.sh -- ships trace_open.py and")
print("     e1_extents.py, both changed by this ticket.")
rc, out = run_runner("species_extent_d633")
RESULTS["species_extent_d633"] = rc
note("exit", rc)
row("species_extent_d633 is green", rc == 0)
# The runner redirects each step to its own transcript, so E1's output is not
# on the runner's stdout.  The transcript the runner just regenerated is what
# carries it, and reading that is the difference between measuring the run and
# measuring the runner's summary of it.
with open(os.path.join(REPO, "code", "species_extent_d633",
                       "out_e1_extents.txt"), encoding="utf-8") as _f:
    e1out = _f.read()
row("its E1 transcript carries the new ATTEMPTED AND FAILED column",
    "ATTEMPTED AND FAILED" in e1out,
    "If the column is absent, the runner is green on a version of E1 that\n"
    "still counts a failed open as a read.")
print()

# --- 3.  mg-6cb9's a1_bothways.py ------------------------------------------
print("  3. code/species_extent_audit_6cb9/a1_bothways.py -- its Q18 plants a")
print("     non-UTF-8 file in species_7d75 and asserts s1_extent EXITS 0.")
print("     That assertion is the reason the ENCODING bucket is a STATED")
print("     decline here and is not counted: making it a finding would redden")
print("     a landed audit's control, and the control is right.")
rc, out = run_checker("species_extent_audit_6cb9", "a1_bothways.py")
RESULTS["a1_bothways.py"] = rc
q18 = find_row(out, "Q18")
note("exit", rc)
note("its Q18 row", q18.strip()[:70] or "(not found)")
row("Q18 is present and does not report a mismatch",
    bool(q18) and "***" not in q18,
    "Q18 row: %s" % q18.strip()[:100])
print()

# --- 4.  mg-5040's r2_wiring.py --------------------------------------------
print("  4. code/species_bound_repair_5040/r2_wiring.py -- deletes lines from")
print("     the wiring block of all three runners.  This repair MOVED that")
print("     block to the end of each file, so if anything was going to break")
print("     from the move it is this.")
rc, out = run_checker("species_bound_repair_5040", "r2_wiring.py")
RESULTS["r2_wiring.py"] = rc
note("exit", rc)
note("its R2 TOTAL BAD", find_row(out, "R2 TOTAL BAD").strip()[:50])
row("mg-5040's wiring probe is still green after the move", rc == 0,
    "It is a REPAIR probe, not an audit: green is its landed state, and a\n"
    "red here would mean this repair broke the one it builds on.")
print()

# --- 5.  mg-6ef4's selftest6ef4.py -----------------------------------------
print("  5. code/species_bound_audit_6ef4/selftest6ef4.py -- asserts `%s`"
      % SETE)
print("     appears exactly once in each of the three runners.  This repair")
print("     deliberately did NOT delete that line, and this row is where that")
print("     decision is checked rather than asserted in a commit message.")
rc, out = run_checker("species_bound_audit_6ef4", "selftest6ef4.py")
RESULTS["selftest6ef4.py"] = rc
note("exit", rc)
note("its headline", find_row(out, "selftest6ef4:").strip()[:60])
row("mg-6ef4's self-test still passes", rc == 0)
print()

# --- 6.  mg-6ef4's t2_wiring.py --------------------------------------------
print("  6. code/species_bound_audit_6ef4/t2_wiring.py -- the probe that FOUND")
print("     this ticket's OPEN 1.  Its T2e row is written so that it reads")
print("     `ok` when the verdict SURVIVES the deletion of `%s`; before" % SETE)
print("     this repair it read *** FINDING ***.  Its exit code is 1 either")
print("     way, because T2f -- `%s` is in the deletion population of none" % SETE)
print("     of the three earlier instruments -- is a true statement about")
print("     those instruments that this repair does not touch.")
rc, out = run_checker("species_bound_audit_6ef4", "t2_wiring.py")
RESULTS["t2_wiring.py"] = rc
t2e = find_row(out, "leaves the verdict intact in some runner")
t2f = find_row(out, "is in the deletion population of some instrument here")
note("exit", rc)
note("its T2e row", t2e.strip()[:74] or "(not found)")
note("its T2f row", t2f.strip()[:74] or "(not found)")
row("mg-6ef4's T2e row now reads ok -- the finding this ticket repairs",
    bool(t2e) and "***" not in t2e,
    "This is the audit's own instrument agreeing that OPEN 1 is closed,\n"
    "measured by the file that raised it and not by the file repairing it.")
row("and its T2f row is UNCHANGED -- still a finding about the three earlier"
    " populations", bool(t2f) and "***" in t2f,
    "T2f is closed by mg-4adb's own population containing every line that\n"
    "exists, not by adding a fourth name to an audit's table after the fact.\n"
    "An audit is a record of what was true when it ran.")
print()

# --- 7.  one that was ALREADY red, and was not made so here ----------------
print("  7. code/runner_exit_c2b3/k3_retro.py looks for `E2OUT=$(` in two of")
print("     these runners and reports the cross-section block GONE when it is")
print("     absent.  It IS absent -- and it was absent before this ticket.")
print("     mg-5040 removed that block.  Measured from git rather than by")
print("     running c2b3's whole runner, because the question is whether THIS")
print("     repair caused it and git answers that exactly:")
pre_hits = sum(show(PRE, runner_path(t)).count("E2OUT=$(")
               for t in ("species_repair_a4ef", "species_remainder_f8fa"))
now_hits = sum(read_runner(t).count("E2OUT=$(")
               for t in ("species_repair_a4ef", "species_remainder_f8fa"))
note("occurrences of `E2OUT=$(` at %s" % PRE, pre_hits)
note("occurrences of `E2OUT=$(` on disk", now_hits)
row("k3_retro's condition is PRE-EXISTING, not caused here",
    pre_hits == now_hits == 0,
    "NOTED, NOT FIXED.  It is mg-5040's subtraction seen from an instrument\n"
    "that still expects the structure mg-5040 removed, and repairing it is\n"
    "a different ticket's judgement about which of the two is right.")
print()

print("  NOT RUN AS WHOLE RUNNERS, and named so the omission is not silent:")
print("      code/species_bound_repair_5040/run_all.sh   (~25 min; the file")
print("          that carries the dependency, r2_wiring.py, IS run above)")
print("      code/species_bound_audit_6ef4/run_all.sh    (~12 min; its two")
print("          dependent files ARE run above)")
print("      code/species_extent_audit_6cb9/run_all.sh   (its dependent file,")
print("          a1_bothways.py, IS run above)")
print("      code/species_depth_audit_4700/q2_wiring.py  and")
print("      code/species_sites_821e/p3_wiring.py        -- the other two")
print("          deletion populations mg-6ef4's T2f names.  They are AUDITS")
print("          of states this repair is two and three tickets downstream")
print("          of, and their committed transcripts are the record of what")
print("          was true when they ran.  Re-running an audit against a tree")
print("          it did not audit does not test this repair; it replaces a")
print("          record with a measurement of something else.")
print("      code/runner_exit_c2b3/run_all.sh            -- row 7 answers the")
print("          only question about it that this repair can be responsible")
print("          for, and answers it from git.")
print("  That is a judgement about what this repair touches.  It is written")
print("  here so a reader can disagree with it, which is the difference")
print("  between a stated bound and a silent one.")
print()
for k in sorted(RESULTS):
    note("exit code, %s" % k, RESULTS[k])
print()


hdr("V4b  ONE OF THEM, FORCED RED -- A TABLE THAT COULD NOT HAVE BEEN RED IS "
    "NOT EVIDENCE")

print("  `selftest6ef4.py` is the one chosen, because its green row above is")
print("  a claim about a line THIS REPAIR could have deleted and did not.  So")
print("  the line is deleted here, and it must say so.")
print()

target = "species_repair_a4ef"
with Probe("v4b") as pr:
    pr.write(runner_path(target), without(read_runner(target), SETE))
    rc, out = run_checker("species_bound_audit_6ef4", "selftest6ef4.py")
    failing = find_row(out, "`%s` appears exactly once" % SETE)
    print("      selftest6ef4.py with `%s` deleted from %s: exit %d"
          % (SETE, target, rc))
    print("          %s" % failing.strip()[:100])
prove(pr)
print()
row("it goes red, and on the assertion that names the deleted line",
    rc != 0 and "***" in failing,
    "If this is a finding, row 5 above says nothing.")
print()


print("=" * 78)
print("V4 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THAT NUMBER.  Seven rows, named above with the reason")
print("each could have been broken, plus one forced-red control.  It says")
print("NOTHING about instruments that read these files and are not on that")
print("list.  The list is a judgement about what this repair touches, and a")
print("judgement about what to leave out of a population is exactly what")
print("mg-6ef4's F3 was -- so it is written where a reader can disagree.")
sys.exit(1 if bad else 0)
