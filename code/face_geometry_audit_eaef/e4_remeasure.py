"""mg-eaef e4 -- THE 8 OF 11, RE-DERIVED, AND THE POPULATION NAMED.

The figure mg-c4c8 raised, mg-64b6 printed and mg-0b07 re-measured is `8 of 11
declarations understate their own patches`, and mg-f7e1 carries it forward as
untouched.  A figure carried forward three times is a quotation unless somebody
computes it again, and the thing that would break it silently is a change to
what the eleven patches apply to -- which is what mg-f7e1's rewrite of
`absorb_trace` is.

SO IT IS RE-DERIVED HERE FROM THE SOURCE OF THE COMMIT THAT WROTE IT.

  * the eleven declarations are executed out of `b6bc2ef`'s own `d2_deletion.py`
    rather than read from any later copy of them;
  * each patch is applied to the tree that commit applied it to, read from git;
  * the unit each patch removes is computed by THIS audit's differ;
  * this auditor's reading of each English sentence is written above, before any
    measurement, and is what `UNDERSTATES` is measured against;
  * the DIRECTION is computed rather than inferred from inequality, because
    understating makes the evidence look FINER than it is -- which is the defect
    -- and overstating makes it look coarser, which is harmless.

NO BARE TOTAL.  The population is the eleven rows of `UNITS` at `b6bc2ef`,
enumerated below with the tree each was applied to.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, claim, direction, finding, head, report, show, source_at,
    unit_removed,
)

MG9220 = "b6bc2ef"          # the commit that WROTE the eleven declarations
PRE_REPAIR = "5cae82c^"     # the tree BEFORE-* run against
TWO_RETURN = "c7f9673"      # the tree R* run against

REF_OF = {"BEFORE-1": PRE_REPAIR, "BEFORE-2": PRE_REPAIR,
          "AFTER-1": MG9220, "AFTER-2": MG9220, "AFTER-3": MG9220,
          "AFTER-4": MG9220, "AFTER-5": MG9220, "AFTER-6": MG9220,
          "R1": TWO_RETURN, "R2": TWO_RETURN, "R3": TWO_RETURN}

# THIS AUDITOR'S READING of each of mg-9220's eleven sentences: what the
# sentence would have to remove for it to be exact, as (returns, other
# statements, boolean operands).  Written from the sentences alone.
MY_READING = {
    "BEFORE-1": (0, 0, 1),   # "one CLAUSE ...; the `return` it guards stays"
    "BEFORE-2": (1, 0, 0),   # "one `return` statement -- the magnitude gate"
    "AFTER-1": (1, 0, 0),
    "AFTER-2": (1, 0, 0),
    "AFTER-3": (0, 0, 0),    # "NO statement: the ORDER of two gates"
    "AFTER-4": (0, 1, 0),    # "one statement, and not a `return`"
    "AFTER-5": (1, 0, 0),
    "AFTER-6": (1, 0, 0),
    "R1": (1, 0, 0),
    "R2": (1, 0, 0),
    "R3": (2, 0, 0),         # "TWO `return` statements -- the PAIR"
}


def units_of_mg9220():
    """mg-9220's `UNITS` table, executed out of its own committed source."""
    src = show(MG9220, "code/face_geometry_instr_5f9a/d2_deletion.py")
    ns = {}
    for node in ast.parse(src).body:
        if not isinstance(node, ast.Assign):
            continue
        try:
            exec(compile(ast.Module([node], []), "<b6bc2ef>", "exec"), ns)
        except Exception:                                       # noqa: BLE001
            continue
    if "UNITS" not in ns:
        raise SystemExit("could not reconstruct mg-9220's UNITS")
    return ns["UNITS"]


def main():
    print(BAR)
    print("mg-eaef e4 -- the eleven written declarations, measured again")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md e4):")
    print("   e4.1  the population is still 11")
    print("   e4.2  8 UNDERSTATE / 3 AGREE / 0 OVERSTATE / 0 MIXED")
    print("   e4.3  the three that AGREE are BEFORE-1, AFTER-3 and AFTER-4\n")

    units = units_of_mg9220()
    head("1.  THE POPULATION, AND THE TREE EACH ROW WAS APPLIED TO")
    print("   %-9s %-11s %s" % ("tag", "tree", "the sentence mg-9220 wrote"))
    for tag, _edit, sentence in units:
        print("   %-9s %-11s %s" % (tag, REF_OF[tag], sentence[:58]))
    claim("THE POPULATION IS THE ELEVEN ROWS OF `UNITS` AT %s, read by "
          "executing that commit's own assignments: %d row(s), and this audit "
          "has a reading registered for %d of them"
          % (MG9220, len(units), len(MY_READING)),
          len(units) == 11 and set(MY_READING) == {t for t, _e, _s in units},
          "mg-9220's table changing size, or a tag appearing with no reading "
          "beside it -- which is BROKEN here rather than skipped, because a "
          "row nobody read is a row nobody measured")

    head("2.  EACH SENTENCE AGAINST ITS OWN PATCH")
    print("`nodes` is the net syntax-node difference and has no grain; the "
          "three named units\nare the three the sentences use.  DIRECTION is "
          "computed: UNDERSTATES means the\npatch removed MORE than the "
          "sentence claims, which makes the deletion evidence\nlook finer than "
          "it is.\n")
    print("   %-9s %-12s %-12s %-6s %s"
          % ("tag", "declared", "measured", "nodes", "direction"))
    tally = {}
    rows = []
    for tag, edit, _sentence in units:
        fname, old, new = edit
        base = source_at(REF_OF[tag], fname)
        if base.count(old) != 1:
            raise SystemExit("mg-9220's %s anchor occurs %d times at %s"
                             % (tag, base.count(old), REF_OF[tag]))
        ret, stmt, cls, nodes = unit_removed(base, base.replace(old, new))
        got = (ret, stmt, cls)
        d = direction(MY_READING[tag], got)
        tally[d] = tally.get(d, 0) + 1
        rows.append((tag, got, d))
        print("   %-9s %-12s %-12s %-6d %s"
              % (tag, MY_READING[tag], got, nodes, d))
    agree = [t for t, _g, d in rows if d == "AGREES"]
    under = [t for t, _g, d in rows if d == "UNDERSTATES"]
    over = [t for t, _g, d in rows if d == "OVERSTATES"]
    claim("THE RE-DERIVED FIGURE IS %d UNDERSTATE / %d AGREE / %d OVERSTATE "
          "OVER A POPULATION OF %d, which is the figure mg-c4c8 raised, "
          "mg-64b6 printed, mg-0b07 re-measured and mg-f7e1 carried forward"
          % (len(under), len(agree), len(over), len(rows)),
          len(under) == 8 and len(agree) == 3 and len(over) == 0
          and len(rows) == 11,
          "any of the eleven patches or sentences changing, or this audit's "
          "differ disagreeing with the subject's.  Three instruments now agree "
          "on eleven patches from three sets of code, which is what makes the "
          "figure a measurement and not a quotation",
          "understate: %s | agree: %s | overstate: %s"
          % (", ".join(under), ", ".join(agree), ", ".join(over) or "none"))
    claim("AND THE THREE THAT AGREE ARE NAMED, not counted: %s"
          % ", ".join(agree),
          set(agree) == {"BEFORE-1", "AFTER-3", "AFTER-4"},
          "a different three agreeing, which would mean the total is stable "
          "and its composition is not -- and the total is what gets quoted")
    finding("E7", "NOT A FINDING AGAINST THE SUBJECT -- BOOKED AS CONFIRMED. "
            "The 8 / 3 / 0 re-derives exactly, over a population that is still "
            "11, from mg-9220's own committed table and this audit's own "
            "differ.  mg-f7e1's rewrite of `absorb_trace` did not move it, "
            "which is what carrying a figure forward is supposed to mean.")
    return report()


if __name__ == "__main__":
    sys.exit(main())
