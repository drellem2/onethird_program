#!/usr/bin/env python3
"""mg-d3f3 a1 -- REINTRODUCE F1 AND SEE WHAT GOES RED.  (PREDICTIONS.md P1)

THE TICKET'S FRAMING, AND WHY I THINK IT IS WRONG.  The addendum says:

    "V6a is the row that must catch an F1-shaped defect.  CONSTRUCT ONE and
     confirm V6a goes red."

mg-fcb2's F1 was `"... corrupted on %d/%d posets" % (N, N, ...)` -- the same
expression twice.  mg-8af0 replaced the first operand with a measurement.  By
mg-8af0's own **E1**, which it predicted before writing any code and which came
out HIT, the repaired expression prints THE SAME DIGITS: 86/86 before, 86/86
after.  So the defect and its repair are byte-identical in the artifact -- and
therefore so are the defect's RETURN and the repair.

V6a is `anchor in artifact` over 12 literal strings.  V6c is
`fresh_run == committed_artifact`.  V6d compares a probed run to the same bytes.
None of the three can respond to an input that moves no byte of the artifact.
That is not a defect in them; it is what "F1-shaped" means.

SO THE CONSTRUCTION IS THE OTHER WAY ROUND.  Rather than trying to make V6a go
red on an F1-shaped input, this file puts F1 BACK and enumerates the whole
candidate space of things that could notice.  A negative claim needs its
candidate space built, not asserted, so every scored artefact of the repair is
run:

    X1  THE EXACT REVERT.  `% (site_rows[3][1], N, ...)` -> `% (N, N, ...)`.
        The sentence is a tautology again.  Predicted: artifact byte-identical,
        nothing red.

    X2  THE WRONG-DIRECTION CONTROL.  `% (N - 1, N, ...)` -- still a tautology
        (both operands are the population size, one of them off by one; the
        number cannot respond to `le_to_facet_offbyone` any more than X1's can)
        but it prints 85/86 instead of 86/86.  Predicted: V6a red.

X2 is the half that makes X1 mean something.  If X1 and X2 both came out green
the harness would be broken; if both came out red the claim would be false.  The
prediction is that they SPLIT, and where they split is the finding: detectability
tracks WHETHER THE DIGITS MOVED, not whether the sentence is a tautology.

Exit 0 iff the enumeration comes out as scored below.  Cells are compared to
PREDICTIONS.md P1a-P1d, and a cell coming out other than predicted is recorded
as a MISS, not smoothed over.
"""

import sys

import lib_d3f3 as L

SITE = "% (site_rows[3][1], N,"
TAUT = "% (N, N,"
TAUT_MOVED = "% (N - 1, N,"


def construct(replacement):
    """Substitute one operand tuple at the F1 site and rebuild the world."""
    sb = L.Sandbox()
    src = sb.read("face_geometry/controls.py")
    assert src.count(SITE) == 1, "the F1 site is not unique in controls.py"
    sb.write("face_geometry/controls.py", src.replace(SITE, replacement))
    art, art_rc = sb.regenerate()
    return sb, art, art_rc


def main():
    R = L.Report("mg-d3f3 a1 -- F1 put back at the source, and the whole "
                 "candidate space asked whether it noticed")
    before = L.tree_digest(L.real_tree_paths())
    baseline_art = open(L.PROBE + "/controls_output.txt").read()

    print("  the F1 site, verbatim, at controls.py:2282:")
    print("      %s ...)" % SITE)
    print("  X1 puts back mg-fcb2's F1:  %s ...)" % TAUT)
    print("  X2 is the wrong-direction control: %s ...)  -- still unable to "
          "respond to the" % TAUT_MOVED)
    print("      corruption, but it prints different digits")
    print()

    # ---------------- X1: the exact revert -----------------------------
    sb, art, art_rc = construct(TAUT)
    try:
        R.check("a1.1 X1 -- with F1 put back, the artifact is BYTE-IDENTICAL to "
                "the committed one (P1a)",
                art == baseline_art,
                "regenerated %d bytes against the committed %d; controls.py "
                "exit %d" % (len(art), len(baseline_art), art_rc))
        R.count("bytes differing in the artifact", 0
                if art == baseline_art else abs(len(art) - len(baseline_art)),
                "FORCED",
                "mg-8af0's E1 measured the repair as digit-neutral, so its "
                "reversal is digit-neutral too; this 0 could not have come out "
                "otherwise once E1 held and is printed, not offered as evidence")

        code, rows, _ = sb.verify()
        red = L.reds(rows)
        R.check("a1.2 X1 -- verify_e35b.py exits 0 with all %d rows green: V6a, "
                "V6b, V6c, V6d and V7 ALL PASS with F1 present (P1b)"
                % len(rows),
                code == 0 and not red
                and all(L.row(rows, t) for t in ("V6a", "V6b", "V6c", "V6d", "V7")),
                "exit %d, red rows: %s" % (code, [r[:40] for r in red] or "none"))

        others = [
            ("face_geometry_repair_8af0/demo_f2_row_can_go_red.py", 0),
            ("face_geometry_repair_8af0/probe_f1_count_moves.py", 0),
            ("face_geometry_repair_8af0/probe_f3_ridge_multiplicity.py", 0),
            ("face_geometry_repair_8af0/probe_f3_tightness.py", 0),
            ("face_geometry_repair_e35b/demo_v6d_row_can_go_red.py", 0),
        ]
        got = []
        for rel, want in others:
            rc, _ = sb.run_script(rel)
            got.append((rel.split("/")[-1], rc, want))
        R.check("a1.3 X1 -- every other scored artefact of the repair also exits "
                "0 with F1 present: the two demonstrations and the three probes "
                "(P1c)",
                all(rc == want for _, rc, want in got),
                ", ".join("%s exit %d" % (n, rc) for n, rc, _ in got))
        R.note("probe_f1_count_moves.py is the artefact whose whole subject is "
               "this count, and it exits 0 because it never opens controls.py: "
               "it rebuilds the measured numerator from top_laplacians and "
               "TRANSCRIBES the tautology as `len(ps)`.  It is a statement about "
               "two definitions, not about the file that uses one of them.")

        space = 1 + len(rows) + len(others)
        R.count("artefacts in the candidate space", space, "COULD MOVE",
                "1 artifact-byte comparison + %d verifier rows + %d scripts; a "
                "row or script added to the repair moves it" % (len(rows), len(others)))
        R.count("of them that go red when F1 returns", 0, "FORCED",
                "FORCED by a1.1: an artifact-scored row cannot move on "
                "byte-identical bytes, and no artefact reads the F1 site's "
                "SOURCE.  Naming the forcing is the point -- this 0 is not "
                "evidence that the repair is weak, it is a restatement of E1")
    finally:
        sb.close()

    # ---------------- X2: the wrong-direction control -------------------
    sb, art2, _ = construct(TAUT_MOVED)
    try:
        R.check("a1.4 X2 (WRONG DIRECTION) -- a tautology that prints DIFFERENT "
                "digits does move the artifact",
                art2 != baseline_art and "corrupted on 85/86 posets" in art2,
                "regenerated %d bytes against %d; the sentence now reads "
                "%r" % (len(art2), len(baseline_art),
                        "corrupted on 85/86 posets"
                        if "corrupted on 85/86 posets" in art2 else "??"))
        code2, rows2, _ = sb.verify()
        red2 = L.reds(rows2)
        R.check("a1.5 X2 -- and THEN the rows fire: V6a red, V7 red, exit 1",
                code2 == 1 and not L.row(rows2, "V6a") and not L.row(rows2, "V7"),
                "exit %d, %d red: %s" % (code2, len(red2),
                                         [r[:40] for r in red2]))
        R.count("rows red under X2", len(red2), "COULD MOVE",
                "which rows fire depends on which anchors the moved digits sit "
                "in; V6b stays green in both constructions because no specifier "
                "moved in either")
    finally:
        sb.close()

    # ---------------- the finding, stated as a dividing line ------------
    print()
    R.note("THE DIVIDING LINE, MEASURED: X1 and X2 are the same defect class -- "
           "an operand at the F1 site that cannot respond to the corruption the "
           "sentence is about.  X1 is invisible to all %d artefacts and X2 is "
           "caught by two rows.  What separates them is not the defect; it is "
           "whether the digits happened to move.  So the repair's guard is a "
           "guard on the OUTPUT and F1 was a defect in the EXPRESSION, and the "
           "two only coincide when a reader is lucky." % space)
    R.note("WHAT THIS IS NOT.  It is not a claim that the F1 repair failed: the "
           "printed number IS now a measurement, and probe_f1_count_moves.py "
           "shows it taking three values.  It is a claim about the SCOPE of the "
           "declared limit -- see a3.")

    after = L.tree_digest(L.real_tree_paths())
    moved = sorted(k for k in before if before[k] != after.get(k))
    R.check("a1.6 nothing under code/ was written", not moved,
            "moved: %s" % (moved or "none"))

    return R.finish()


if __name__ == "__main__":
    sys.exit(main())
