"""P3 -- `RETURNED 0` AND `EXAMINED NOTHING` MUST NOT BE THE SAME STATE.

mg-d53d's finding 2.  `e2_crosssection.py:52` was `FILES += _f`.  Deleted
alone, the checker READ NO DOCUMENT, PRINTED NO ROW, SAID NOTHING AND RETURNED
0 -- and the three runners whose last command it is returned 0 with it.  That
is the same vacuous-pass shape this arc kept finding on the same evening:
mg-9a59's exit 0 over ZERO gate runs, mg-0120's four verdicts pinned to the
literal `False`, mg-8af0's row scoring a string literal.  A control that cannot
fail is not a control.

THIS SECTION IS THE FLOOR, AND IT IS MEASURED IN BOTH DIRECTIONS.  Every row
here has a known right answer, and the rows that must say NO are here for the
same reason as the rows that must say YES.

  P3a  the three states, given three exit codes and three sentences
  P3b  the empty-population floor, called directly, with `bad` 0 and non-zero
  P3c  the dead man's switch, armed and delivered / armed and abandoned
  P3d  the population size is printed ON A PASSING RUN, which is the only run
       where a vacuous pass could hide
  P3e  the same four questions asked of the PRE-REPAIR checker, so that the
       difference is measured and not asserted

    python3 code/verdict_path_repair_1d26/p3_vacuous.py
"""

import os
import shutil
import subprocess
import sys

from kern1d26 import (hdr, Rows, REPO, E2, KERN, PRE_E2, PRE_KERN, clone,
                      cleanup, neutralise, run_e2, sh, Deletion, locate,
                      SIX_PRE, SIX_POST, pre_pair)

R = Rows()
D633 = os.path.join("code", "species_extent_d633")


def py(root, source, timeout=120):
    """Run a one-off program in the checker's own directory, so that its
    `import kernd633` is the one under test."""
    d = os.path.join(root, D633)
    p = os.path.join(d, "_p3_probe.py")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(source)
    try:
        return sh([sys.executable, "-B", "_p3_probe.py"], cwd=d,
                  timeout=timeout)
    finally:
        os.remove(p)


base = clone()
neutralise(base)


# ---------------------------------------------------------------------------
hdr("P3a  THREE STATES, THREE EXIT CODES, THREE SENTENCES")
# ---------------------------------------------------------------------------

R.note("A reader with an `&&` sees an exit code and nothing else.  Until this")
R.note("ticket, `checked 264 documents and found nothing wrong`, `read no")
R.note("document at all` and `never reached its own verdict` were all 0.")
print()

STATES = [
    ("checked, and found nothing wrong",
     "import kernd633 as k\nk.arm_verdict()\n"
     "k.deliver('P3', 0, 264, 'a population that exists')\n",
     0, "CHECKED 264"),
    ("found nothing to check",
     "import kernd633 as k\nk.arm_verdict()\n"
     "k.deliver('P3', 0, 0, 'an empty population')\n",
     2, "FOUND NOTHING TO CHECK"),
    ("never delivered a verdict at all",
     "import kernd633 as k\nk.arm_verdict()\n"
     "print('P3: this program ends without delivering anything')\n",
     9, "NO VERDICT WAS DELIVERED"),
]
seen = []
for label, src, want_rc, want_says in STATES:
    rc, out = py(base, src)
    seen.append((label, rc, want_says in out))
    R.note("    %-38s exit %-4s says %-28s %s"
           % (label, rc, "`%s`" % want_says,
              "yes" if want_says in out else "NO"))
print()
R.row("each of the three has its own exit code",
      len(set(rc for _l, rc, _s in seen)) == 3,
      "measured: %s" % ", ".join(str(rc) for _l, rc, _s in seen))
R.row("each of the three names itself in the output",
      all(s for _l, _rc, s in seen))
R.predicted(
    "P3c.1", "the three states are distinguishable by exit code AND by a "
             "printed sentence",
    "exit codes %s; %d of 3 print their own sentence"
    % ("/".join(str(rc) for _l, rc, _s in seen),
       sum(1 for _l, _rc, s in seen if s)),
    len(set(rc for _l, rc, _s in seen)) == 3
    and all(s for _l, _rc, s in seen))


# ---------------------------------------------------------------------------
hdr("P3b  THE EMPTY-POPULATION FLOOR, CALLED DIRECTLY, BOTH WAYS ROUND")
# ---------------------------------------------------------------------------

R.note("`deliver` must refuse to exit 0 over an empty population WHATEVER the")
R.note("finding count is -- including the case where nothing was found,")
R.note("because that is precisely the case an empty population produces.  And")
R.note("it must still exit 0 when a real population found nothing, or the")
R.note("floor has replaced one control that cannot fail with another.")
print()

CASES = [(0, 0, 2, "empty population, no findings"),
         (3, 0, 2, "empty population, three findings"),
         (0, 1, 0, "one document, no findings"),
         (0, 264, 0, "a real population, no findings"),
         (1, 264, 1, "a real population, one finding")]
floor = []
for bad, examined, want, label in CASES:
    rc, out = py(base, "import kernd633 as k\nk.arm_verdict()\n"
                       "k.deliver('P3', %d, %d, 'P3b')\n" % (bad, examined))
    floor.append((label, rc, want))
    R.note("    %-34s bad=%-3d examined=%-4d exit %-4s expected %d  %s"
           % (label, bad, examined, rc, want,
              "ok" if rc == want else "*** WRONG ***"))
print()
R.row("5 of 5 floor cases return the exit code they must",
      all(rc == want for _l, rc, want in floor),
      "The last two are the rows that must say NO: a floor that reddened a\n"
      "real clean run would have made the gate unable to be green, which is\n"
      "not a repair -- it is the same defect with the sign flipped.")


# ---------------------------------------------------------------------------
hdr("P3c  THE DEAD MAN'S SWITCH")
# ---------------------------------------------------------------------------

R.note("`sys.exit(1 if bad else 0)` as the last line of a checker is a line")
R.note("whose DELETION exits 0: CPython gives status 0 to a process that runs")
R.note("off the end of its own module, so losing the verdict WAS a pass.  The")
R.note("switch is armed at the top of the checker and fires at interpreter")
R.note("shutdown if nothing was ever delivered.")
print()

SWITCH = [
    ("armed, and a verdict delivered (clean)",
     "import kernd633 as k\nk.arm_verdict()\nk.deliver('P3', 0, 9, 'x')\n", 0),
    ("armed, and a verdict delivered (red)",
     "import kernd633 as k\nk.arm_verdict()\nk.deliver('P3', 2, 9, 'x')\n", 1),
    ("armed, and abandoned",
     "import kernd633 as k\nk.arm_verdict()\n", 9),
    ("armed, and abandoned after a sys.exit(0)",
     "import sys\nimport kernd633 as k\nk.arm_verdict()\nsys.exit(0)\n", 9),
    ("NOT armed, and abandoned -- must stay 0",
     "import kernd633 as k\nprint(k.RUN_MIN)\n", 0),
    # THE DEFECT THIS INSTRUMENT FOUND IN ITS OWN REPAIR, closed and then
    # measured.  The first version of the switch recorded the FACT of a
    # verdict; deleting the `sys.exit` INSIDE `deliver` then recorded it,
    # returned normally and exited 0.  P2's first run reported that as its one
    # GATE LOST and `out_p2_FIRSTRUN_one_lost.txt` is the transcript.  The
    # switch now records the CODE and returns it, so the verdict is carried by
    # two lines and either one alone delivers it.  Here `sys.exit` is replaced
    # by a no-op, which is that deletion's effect without the deletion.
    ("delivered with `sys.exit` neutralised -- the switch carries the code",
     "import sys\nimport kernd633 as k\nk.arm_verdict()\n"
     "sys.exit = lambda *a: None\nk.deliver('P3', 2, 5, 'x')\n"
     "print('deliver returned instead of exiting')\n", 1),
    ("the same, with nothing wrong to report -- must be 0 and not 9",
     "import sys\nimport kernd633 as k\nk.arm_verdict()\n"
     "sys.exit = lambda *a: None\nk.deliver('P3', 0, 5, 'x')\n", 0),
]
sw = []
for label, src, want in SWITCH:
    rc, _out = py(base, src)
    sw.append((label, rc, want))
    R.note("    %-46s exit %-4s expected %-4s %s"
           % (label, rc, want, "ok" if rc == want else "*** WRONG ***"))
print()
R.row("%d of %d switch cases return the exit code they must" % (len(sw),
                                                                len(sw)),
      all(rc == want for _l, rc, want in sw),
      "The fourth is the one that matters most: a deletion that leaves a\n"
      "`sys.exit(0)` reachable ahead of the verdict is still caught.\n"
      "The fifth is the row that must say NO -- `e1_extents.py`,\n"
      "`e3_bothways.py` and `selftestd633.py` import this kernel and do not\n"
      "deliver through it, and arming them would redden three runs that are\n"
      "not lying about anything.")


# ---------------------------------------------------------------------------
hdr("P3d  THE POPULATION SIZE IS PRINTED ON A RUN THAT PASSES")
# ---------------------------------------------------------------------------

R.note("A vacuous pass hides in a PASSING run, so the population size has to")
R.note("be in the output of the runs that exit 0 -- not only in the runs that")
R.note("fire.  The sandbox here is neutralised (see kern1d26) and carries no")
R.note("plant, so this is a genuinely green run of the repaired checker.")
print()

rc_green, out_green = run_e2(base)
has_pop = "E2 POPULATION EXAMINED:" in out_green
n_pop = 0
for ln in out_green.splitlines():
    if ln.startswith("E2 POPULATION EXAMINED:"):
        n_pop = int(ln.split(":")[1].split()[0])
R.note("    the repaired checker on a clean tree: exit %s, population line "
       "present: %s, population %d" % (rc_green, "yes" if has_pop else "NO",
                                       n_pop))
R.row("a GREEN run prints the size of the population it examined",
      rc_green == 0 and has_pop and n_pop > 0)
R.predicted(
    "P3d", "the repaired checker prints its population size on every run, "
           "passes included",
    "green run: exit %s, population line %s, %d document(s)"
    % (rc_green, "present" if has_pop else "ABSENT", n_pop),
    rc_green == 0 and has_pop and n_pop > 0,
    "This row is also the clean-tree control mg-4adb's V1b and mg-d53d's G1b\n"
    "each assert.  It is true here ONLY because the sandbox was neutralised:\n"
    "on the untouched tree the repaired checker exits 1 over a live finding\n"
    "in %s, which is P2's first row." % os.path.join(
        "code", "face_geometry_repair_e35b", "README.md"))


# ---------------------------------------------------------------------------
hdr("P3e  THE SAME QUESTIONS, ASKED OF THE PRE-REPAIR CHECKER")
# ---------------------------------------------------------------------------

R.note("The difference is measured, not asserted.  The pre-repair content of")
R.note("both files is written into a second sandbox from the byte-identical")
R.note("copies committed in this directory -- content, never a revision, since")
R.note("the refinery rebases and a recorded SHA is displaced on main.")
print()

pre = clone()
neutralise(pre)
pre_pair(pre)

rc_pre_clean, out_pre_clean = run_e2(pre)
R.note("    pre-repair, clean neutralised tree:      exit %s" % rc_pre_clean)

i = locate(pre, E2, SIX_PRE[0][1], SIX_PRE[0][2])
with Deletion(pre, E2, i):
    rc_pre_empty, out_pre_empty = run_e2(pre)
j = locate(base, E2, SIX_POST[0][1], SIX_POST[0][2])
with Deletion(base, E2, j):
    rc_post_empty, out_post_empty = run_e2(base)

R.note("    pre-repair, `FILES += _f` deleted:       exit %s, %d line(s) of "
       "output, says nothing about a population"
       % (rc_pre_empty, len(out_pre_empty.splitlines())))
R.note("    repaired,   `FILES += _f` deleted:       exit %s, says `%s`: %s"
       % (rc_post_empty, "FOUND NOTHING TO CHECK",
          "yes" if "FOUND NOTHING TO CHECK" in out_post_empty else "NO"))
print()
R.predicted(
    "P3c.2", "the repaired checker exits non-zero over an empty population "
             "and the pre-repair one exits 0 on the same tree",
    "pre-repair exit %s; repaired exit %s"
    % (rc_pre_empty, rc_post_empty),
    rc_pre_empty == 0 and rc_post_empty not in (0, None),
    "This is mg-d53d's finding 2, reproduced by an instrument that shares no\n"
    "code with mg-d53d, and then closed -- in the same section, against the\n"
    "same tree, one paragraph apart.")

R.row("the pre-repair checker was silent about it, and the repaired one is not",
      "FOUND NOTHING TO CHECK" not in out_pre_empty
      and "FOUND NOTHING TO CHECK" in out_post_empty,
      "mg-1d26's third instruction: a deletion that changes the verdict must\n"
      "not be able to do so WITHOUT PRINTING.  Loud before impossible.")

R.tail("P3")
print()
print("EXTENT OF THESE NUMBERS.  %d one-off programs run against the repaired"
      % (len(STATES) + len(CASES) + len(SWITCH)))
print("kernel, plus 2 whole runs of `e2_crosssection.py` and 2 deletions, in")
print("two `git clone --shared` sandboxes.  IT SAYS NOTHING about any other")
print("checker in this repository, about any exit code other than the ones")
print("printed above, or about a deletion of more than one line at a time.")
print("The floor `deliver` enforces is `examined > 0` and NOT `examined is")
print("right`: it distinguishes CHECKED NOTHING from FOUND NOTHING, and a")
print("population that is merely too SMALL is caught by the second")
print("enumeration in E2a, which is P2's subject and not this section's.")

cleanup()
sys.exit(1 if R.bad else 0)
