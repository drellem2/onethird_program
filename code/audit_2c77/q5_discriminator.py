"""q5_discriminator.py -- THE CHECK THAT DECIDES WHETHER A SENTENCE IS LIVE.

FLOOR, NOT SCOPE.  No list in this ticket names this.  It is chosen because it
is the single check the whole of mg-69d1's OPEN 1 and OPEN 2 rests on: `p1 (i)`
and `p3 (i)` each end with a gate of the form *the old sentence is asserted at 0
live sites*, and `live` is decided entirely by a proximity test.  If that test
cannot go red in a given file, then the gate is green in that file for a reason
that has nothing to do with what the file says.

mg-69d1's own `PREDICTIONS.md` records `miss #2`: the discriminator began life
as a PATH LIST which exempted `d2_deletion.py`, `face_complex.py` and
`run_all.sh` -- the three files the wide sentence was live in -- and was
replaced because that made it vacuous by construction. The replacement is

    a correcting MARKER within N lines, in the same file

with the markers including the ticket ids `mg-69d1` and `mg-eaef`.

EVERY FILE mg-69d1 WROTE SAYS `mg-69d1`, OFTEN.  So the question this script
asks is whether the marker set is a path list again, spelled differently.

HOW IT IS ASKED WITHOUT WRITING ANYTHING.  The markers and the window are PARSED
OUT OF `p1_bound.py` and `p3_reason.py` rather than copied here, so this probe
moves when they move. The rule is then applied to file contents held in memory:
each subject file's real text with one fresh assertion of the old sentence
spliced in at a chosen line. Nothing is written to disk.

A `refuted` verdict on a line that was just planted as a live assertion means
the rule cannot see a live assertion there.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib2c77 as L                                              # noqa: E402

R = L.Report(
    selfpop="the parse of CORRECTION_MARKERS, CORRECTION_WINDOW, MARKERS and "
            "WINDOW out of p1_bound.py and p3_reason.py, and the requirement "
            "that each subject file be readable and each splice really insert "
            "the sentence it names",
    findpop="the two shipped discriminators applied to a planted live "
            "assertion at every insertion point tried, over the 4 files "
            "mg-69d1's own gates run against, plus the same rule applied to "
            "the file where the defect was live before the repair")

L.banner("Q5", "THE PROXIMITY TEST THAT DECIDES `LIVE ASSERTION`")

P1_REL = L.R69D1_DIR + "/p1_bound.py"
P3_REL = L.R69D1_DIR + "/p3_reason.py"
p1_src = L.read_worktree(P1_REL)
p3_src = L.read_worktree(P3_REL)


def literal(src, name, rel):
    try:
        return L.read_literal(src, name)
    except KeyError:
        R.selferr("%s could not be parsed out of %s; the probes that use it "
                  "are DROPPED rather than counted as passing" % (name, rel))
        return None


P1_MARKERS = literal(p1_src, "CORRECTION_MARKERS", P1_REL)
P1_WINDOW = literal(p1_src, "CORRECTION_WINDOW", P1_REL)
P3_MARKERS = literal(p3_src, "MARKERS", P3_REL)
P3_WINDOW = literal(p3_src, "WINDOW", P3_REL)
WIDE = literal(p1_src, "WIDE", P1_REL)
OLD_REASON = literal(p3_src, "OLD", P3_REL)

L.rule("(i) THE RULE, READ OUT OF THE SUBJECT RATHER THAN COPIED")
print("   %-14s %-8s %s" % ("gate", "window", "markers"))
print("   %-14s %-8s %s" % ("p1 (i)", P1_WINDOW, P1_MARKERS))
print("   %-14s %-8s %s" % ("p3 (i)", P3_WINDOW, P3_MARKERS))
print()
print("   the sentence p1 hunts : %r" % (WIDE[:64] if WIDE else None))
print("   the sentence p3 hunts : %r" % (OLD_REASON,))
print()


def corrected_near(text, lineno, markers, window):
    """The shipped rule, applied to text held in memory."""
    lines = text.splitlines()
    i = int(lineno) - 1
    return any(m in "\n".join(lines[max(0, i - window):i + window + 1])
               for m in markers)


# ---------------------------------------------------------------------------
L.rule("(ii) A LIVE ASSERTION, PLANTED, AND THE RULE ASKED ABOUT IT")
print("""   Into each subject file's real text, at three insertion points --
   the first line, the middle, and the last -- one fresh line that
   ASSERTS the sentence with nothing correcting it. The rule is then
   asked whether that line is a live assertion.

   `refuted` on a planted assertion means the rule cannot go red in
   that file at that point, whatever the file says.""")
print()

SUBJECTS = [
    ("p1 (i)", WIDE, P1_MARKERS, P1_WINDOW,
     [L.R69D1_DIR + "/README.md",
      L.R69D1_DIR + "/p1_bound.py",
      "docs/repair-mg-69d1-bound-and-reason.md",
      L.INSTR_DIR + "/d2_deletion.py",
      L.FG_DIR + "/face_complex.py"]),
    ("p3 (i)", OLD_REASON, P3_MARKERS, P3_WINDOW,
     [L.R69D1_DIR + "/p3_reason.py",
      L.S58DA_DIR + "/g1_provenance.py",
      L.R76CC_DIR + "/lib76cc.py" if hasattr(L, "R76CC_DIR")
      else "code/branching_repair_76cc/lib76cc.py",
      L.FG_DIR + "/face_complex.py"]),
]

print("   %-10s %-52s %-10s %s"
      % ("gate", "file the assertion is planted in", "points", "verdict"))
blind, seeing = [], []
RATE = {"repair": [0, 0], "elsewhere": [0, 0]}
for gate, sentence, markers, window, files in SUBJECTS:
    if sentence is None or markers is None or window is None:
        continue
    for rel in files:
        try:
            text = L.read_worktree(rel)
        except (IOError, OSError):
            R.selferr("%s could not be read; its row is DROPPED rather than "
                      "counted" % rel)
            continue
        lines = text.splitlines()
        points = [1, max(1, len(lines) // 2), max(1, len(lines))]
        verdicts = []
        for pt in points:
            planted = lines[:pt] + [sentence] + lines[pt:]
            body = "\n".join(planted)
            if body.count(sentence) < 1:
                R.selferr("the splice into %s at line %d did not insert the "
                          "sentence; that point is DROPPED" % (rel, pt))
                continue
            verdicts.append(corrected_near(body, pt + 1, markers, window))
        if not verdicts:
            continue
        n_ref = sum(1 for v in verdicts if v)
        bucket = "repair" if rel.startswith(L.R69D1_DIR) else "elsewhere"
        RATE[bucket][0] += n_ref
        RATE[bucket][1] += len(verdicts)
        label = ("REFUTED at %d of %d -- rule is BLIND here" % (n_ref,
                                                                len(verdicts))
                 if n_ref == len(verdicts) else
                 "blind at %d of %d, live at %d"
                 % (n_ref, len(verdicts), len(verdicts) - n_ref))
        print("   %-10s %-52s %-10d %s" % (gate, rel, len(verdicts), label))
        (blind if n_ref == len(verdicts) else seeing).append((gate, rel))
print()
print("   %d file(s) where the rule reported REFUTED at EVERY point tried; "
      "%d where it\n   reported at least one live assertion."
      % (len(blind), len(seeing)))
print()
print("""   MISS #4, KEPT.  I predicted the rule would be blind at every point
   in every file under code/repair_69d1/.  It is not: the markers are
   dense but not uniform, and a 25-line window can fall between them.
   The all-or-nothing gate below therefore fires on ONE file.  The rate
   is the more informative number and it is printed rather than the
   gate's number alone:""")
print()
print("     %-34s %-10s %-10s %s"
      % ("insertion points in", "blind", "tried", "rate"))
for bucket, label in (("repair", "code/repair_69d1/ -- the fix"),
                      ("elsewhere", "everywhere else tried")):
    b, t = RATE[bucket]
    print("     %-34s %-10d %-10d %s"
          % (label, b, t, "%d%%" % (100 * b // t) if t else "n/a"))
print()
R.check(bool(seeing),
        "the rule reported REFUTED everywhere, including in files that carry "
        "no ticket id; the probe is not distinguishing and says nothing")
R.gate(not [b for b in blind if b[1].startswith(L.R69D1_DIR)],
       "THE PROXIMITY TEST IS BLIND IN THE DIRECTORY THE REPAIR WROTE.  A "
       "fresh, uncorrected assertion of the sentence each gate hunts is "
       "reported as `refuted within %s lines` at every insertion point tried "
       "in %s -- because every file there says `mg-69d1`, which is a "
       "correction marker.  mg-69d1's own miss #2 records that this check "
       "began as a PATH LIST exempting the three files the sentence was live "
       "in, and was replaced for being vacuous by construction; the marker "
       "set exempts, by construction, the directory where a repair writes its "
       "NEW prose, which is where a newly-wrong sentence would be written.  "
       "Across every insertion point tried, the rule was blind at %d of %d in "
       "code/repair_69d1/ and at %d of %d everywhere else"
       % (P1_WINDOW,
          ", ".join(sorted({b[1] for b in blind
                            if b[1].startswith(L.R69D1_DIR)})),
          RATE["repair"][0], RATE["repair"][1],
          RATE["elsewhere"][0], RATE["elsewhere"][1]))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) WHAT THIS DOES AND DOES NOT IMPLY")
print("""   IT DOES NOT IMPLY THE GATES ARE WRONG NOW.  p1 (i) reports 8 copies
   of the wide sentence and 0 live; q3's own site walk agrees that none
   of them is a live assertion of the BOUND. The defect is in what the
   check could have caught, not in what it reported.

   IT DOES IMPLY THE GATE CANNOT PROTECT THE REPAIR'S OWN OUTPUT.  p3
   (i-b) demonstrates non-vacuity by running the rule against HEAD and
   getting live assertions there -- in mg-eaef's files, which is where
   the OLD defect lived.  Non-vacuity in the directory the defect came
   from is not non-vacuity in the directory the fix goes to, and those
   are different directories.""")
print()
print("   the four insertion points the repair's own miss #2 was about, as a")
print("   control -- the rule IS able to go red where the marker is absent:")
for gate, rel in sorted(seeing):
    print("     %-10s %s" % (gate, rel))
print()

L.finish(R)
