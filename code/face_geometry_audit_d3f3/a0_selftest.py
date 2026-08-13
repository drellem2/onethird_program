#!/usr/bin/env python3
"""mg-d3f3 a0 -- the harness, on a population where the answer is NOT the one it wants.

THIS AUDIT'S HEADLINE IS A NEGATIVE: "reintroduce F1 and no row goes red."  A
negative is worth nothing from an instrument that has never been shown reporting
a red, because "no row went red" and "the harness cannot see red" print the same
way.  So before any construction of the audit proper:

  a0.1  BASELINE.  The unmutated sandbox reproduces the committed transcript
        byte for byte and exits 0.  If the sandbox has perturbed the tree, every
        later cell is about a different repository.
  a0.2  THE HARNESS SEES RED.  A construction whose answer is already known --
        mg-8af0's own C3, a classified count reworded in the artifact by hand --
        is run, and the harness must report V6a and V6c RED and exit 1.  This is
        deliberately a case where the repair WORKS: the point is the instrument,
        not the verdict.
  a0.3  THE TAG LOOKUP CANNOT MATCH NOTHING.  `row()` raises when a tag matches
        zero or several rows.  A tag that silently missed would report the
        absence of a row as its passing, and this audit's whole method is reading
        verdicts by name.
  a0.4  NO WRITE ESCAPES THE SANDBOX.  Every file under code/face_geometry/,
        code/face_geometry_repair_e35b/ and code/face_geometry_repair_8af0/ is
        hashed before and after every construction above.

Exit 0 iff all four hold.
"""

import sys

import lib_d3f3 as L


def main():
    R = L.Report("mg-d3f3 a0 -- audit harness self-test (controls before the audit)")
    before = L.tree_digest(L.real_tree_paths())

    committed = open(L.REPAIR + "/out_verify_e35b.txt").read()

    # -- a0.1 baseline ---------------------------------------------------
    sb = L.Sandbox()
    try:
        code, rows, out = sb.verify()
        R.check("a0.1 BASELINE -- the unmutated sandbox exits 0 with %d rows, "
                "all green, and reproduces out_verify_e35b.txt byte for byte"
                % len(rows),
                code == 0 and not L.reds(rows) and out == committed,
                "exit %d, %d rows, %d red, transcript %s"
                % (code, len(rows), len(L.reds(rows)),
                   "identical" if out == committed else
                   "DIFFERS (%d bytes against %d)" % (len(out), len(committed))))
        R.count("rows scored by the verifier", len(rows), "COULD MOVE",
                "a row added or deleted in verify_e35b.py moves it; it is 29 "
                "today and was 28 before mg-843d added V6d")
    finally:
        sb.close()

    # -- a0.2 the harness sees red ---------------------------------------
    sb = L.Sandbox()
    try:
        art = sb.artifact()
        assert "coverage at `le_to_facet` is 61/86" in art
        sb.write("face_geometry/controls_output.txt",
                 art.replace("coverage at `le_to_facet` is 61/86",
                             "coverage at `le_to_facet` is 61/87"))
        code, rows, _ = sb.verify()
        got = L.reds(rows)
        R.check("a0.2 THE HARNESS SEES RED -- mg-8af0's C3 (a classified count "
                "reworded in the artifact by hand) turns V6a and V6c red and "
                "exits 1",
                code == 1 and not L.row(rows, "V6a") and not L.row(rows, "V6c")
                and L.row(rows, "V6b") and L.row(rows, "V7"),
                "exit %d, %d red: %s" % (code, len(got),
                                         [g[:40] for g in got]))
        R.count("rows red under C3", len(got), "COULD MOVE",
                "V6d also reads the artifact, so the 3 here is V6a + V6c + V6d "
                "and it would be 2 on the pre-mg-843d tree")
    finally:
        sb.close()

    # -- a0.3 the tag lookup cannot match nothing ------------------------
    try:
        L.row({"some other row": True}, "V6a")
        ok = False
        why = "row() returned instead of raising on a tag that matches nothing"
    except KeyError as e:
        ok = True
        why = "raised: %s" % e
    R.check("a0.3 THE TAG LOOKUP CANNOT MATCH NOTHING -- row() raises rather "
            "than reporting an absent row as green", ok, why)

    # -- a0.4 nothing under code/ was written ----------------------------
    after = L.tree_digest(L.real_tree_paths())
    moved = sorted(k for k in before if before[k] != after.get(k))
    R.check("a0.4 NO WRITE ESCAPES THE SANDBOX -- all %d tracked files under "
            "face_geometry/, _repair_e35b/ and _repair_8af0/ are byte-identical "
            "before and after" % len(before),
            not moved and set(before) == set(after),
            "moved: %s" % (moved or "none"))
    R.count("tracked files hashed", len(before), "COULD MOVE",
            "a file added to any of the three directories moves it")

    return R.finish()


if __name__ == "__main__":
    sys.exit(main())
