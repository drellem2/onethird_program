"""mg-eaef e1 -- THE MOVE THE REPAIR TOOK, RUN AGAIN HERE, AND THE NEXT TWO RUNGS.

mg-f7e1 took mg-0b07's option 1: `absorb_trace`'s `shape` guard, which mg-64b6
had merged into one list comparison, is spelled with an `or` again so that both
halves are operands the clause sweep deletes individually.  The point of that
move is that a deletion test which can name a unit can also SHOW that unit
mattering.  So the first question this file asks is the plain one:

    DELETE EACH SIDE ALONE.  DOES THE ARTIFACT CHANGE FOR EACH?

It does not, and the subject says so on the row -- that half of the finding is
booked as honest below and not as a defect.  The question this file then asks is
the one the subject's own bound invites: the operator bought a HANDLE on two
sub-decisions of one comparison, and the comparison still contains others.  How
far down does the handle go, and where does it stop?

  RUNG 6, MEASURED HERE: an operand of `or`/`and` that is NOT the top level of
  its condition.  It is spelled with the operator -- the exact thing the subject
  names as the floor of its coverage -- and the subject's enumerator does not
  see it, because that enumerator asks whether the CONDITION is a `BoolOp`
  rather than walking for them.

  RUNG 7, NAMED AND DEMONSTRATED HERE: a decision that is not in a condition at
  all.  `shape_A` and `shape_B` are computed one and two lines above the guard,
  and every number the subject prints -- including the one it says has no grain
  -- counts nodes inside DECIDING CONDITIONS.  Perturb the comprehension and the
  guard means something else, with nothing removed from any condition.

Everything here is run against the live worktree tree and against a baseline
regenerated in this run.  No committed artifact is read as the baseline.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, SHAPE_GUARD, SHAPE_GUARD_ORDER_ONLY, SHAPE_GUARD_WIDTH_ONLY,
    boolean_operands, build_tree, claim, deciding_conditions, drop_operand,
    expr_nodes, finding, head, report, run_battery, source_at,
)

# The seventh rung, as a patch: the guard compares `shape_A` with `shape_B`, and
# `shape_B` is built one line above it.  Truncating B to A's row count makes the
# ORDER half unable to fire -- the same defect mg-0b07 found, reintroduced from
# a STATEMENT rather than from the condition.
ASSIGN_OLD = "    shape_B = [len(row) for row in B]\n"
ASSIGN_NEW = "    shape_B = [len(row) for row in B[:len(A)]]\n"

SEP_A = [[0, 1], [1, 0]]
SEP_B = [[0, 1], [1, 0], [0, 0]]


def load(tree, module):
    import importlib.util
    path = os.path.join(tree, "%s.py" % module)
    spec = importlib.util.spec_from_file_location("eaef_%s_%d"
                                                  % (module, id(tree)), path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, tree)
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path.remove(tree)
    return mod


def main():
    print(BAR)
    print("mg-eaef e1 -- each side of the respelled `or`, then rungs 6 and 7")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md e1):")
    print("   e1.1  delete the ORDER half alone -> BYTE-IDENTICAL, exit 0")
    print("   e1.2  delete the WIDTH half alone -> CHANGES, exit 1")
    print("   e1.3  every NESTED boolean operand deleted alone -> "
          "BYTE-IDENTICAL, exit 0")
    print("   e1.4  the rung-7 assignment patch -> BYTE-IDENTICAL, exit 0, and "
          "the\n         predicate's answer on the separator pair FLIPS\n")

    live = source_at(None)
    base_dir = build_tree()
    base, base_code = run_battery(base_dir)
    claim("THE BASELINE IS REGENERATED IN THIS RUN, not read from "
          "controls_output.txt: %d bytes, exit %d"
          % (len(base), base_code),
          base_code == 0 and len(base) > 0,
          "the battery ceasing to be reproducible from its own sources.  Every "
          "IDENTICAL/CHANGES below is against THIS text, so a committed "
          "artifact that had drifted from its own code could not make a row "
          "here read green",
          "%d bytes" % len(base))

    # ----------------------------------------------------------------- rung 5
    head("1.  THE MOVE: each half of the respelled guard, deleted alone")
    print("The live guard, read out of the tree:\n")
    print("      " + "\n      ".join(SHAPE_GUARD.strip().splitlines()))
    print("\nmg-0b07 asked for this and mg-f7e1 did it.  The two halves are now "
          "operands, so\nthe deletion test HAS A HANDLE on each.  What it "
          "reports when it pulls each one\nis the question -- a handle is not "
          "coverage.\n")
    rows = []
    for label, text, want in (
            ("ORDER half `len(shape_A) != len(shape_B)`",
             SHAPE_GUARD_WIDTH_ONLY, False),
            ("WIDTH half `any(a != b for a, b in zip(...))`",
             SHAPE_GUARD_ORDER_ONLY, True)):
        out, code = run_battery(build_tree(
            [("face_complex.py", SHAPE_GUARD, text)]))
        changed = out != base
        rows.append((label, changed, code))
        print("   delete %-44s %-10s exit %d  %s"
              % (label, "CHANGES" if changed else "IDENTICAL", code,
                 "the battery covers it"
                 if changed else "NOT COVERED by any pair in the battery"))
    claim("THE OPERATOR IS REALLY THERE AND EACH HALF IS REALLY DELETABLE: 2 "
          "of 2 patches applied to a single anchor occurring exactly once, and "
          "the two results DIFFER from each other, so the sweep is reading the "
          "code and not a constant",
          len({(c, x) for _l, c, x in rows}) == 2,
          "the two halves producing the same result, which would mean this "
          "section cannot tell them apart and neither could the subject's",
          "; ".join("%s %s exit %d" % (l.split("`")[0].strip(),
                                       "CHANGES" if c else "IDENTICAL", x)
                    for l, c, x in rows))
    covered = [l for l, c, _x in rows if c]
    finding("E1", "THE MOVE BOUGHT A HANDLE AND NOT A SECOND COVERED HALF: of "
            "the 2 operands the respelling created, 1 changes the artifact and "
            "1 does not.  The subject states this on the row that carries it "
            "(`NOT COVERED -- deletion establishes nothing about it`) and this "
            "run reproduces it independently, so it is booked here as a "
            "DISCLOSED limit rather than a hidden one -- the finding is the "
            "shape of what option 1 can buy, not a false claim.",
            "covered by deletion: %s; not covered: %s"
            % (", ".join(c.split("`")[0].strip() for c in covered) or "none",
               ", ".join(l.split("`")[0].strip()
                         for l, c, _x in rows if not c) or "none"))

    # ----------------------------------------------------------------- rung 6
    head("2.  RUNG SIX -- an explicit boolean operand the sweep does not reach")
    print("The subject's bound is a sentence AND a count: `DELETION "
          "ESTABLISHES COVERAGE DOWN\nTO EXPLICIT BOOLEAN OPERANDS AND NO "
          "FURTHER`, with `the sweep above reaches the\noperands of `or` and "
          "`and` and nothing else`.  Both sentences describe a population.\n"
          "This section enumerates that population from the tree and compares "
          "it with the\none the sweep actually visits.\n")
    all_ops = boolean_operands(live)
    top = [o for o in all_ops if not o.nested]
    nested = [o for o in all_ops if o.nested]
    print("   every operand of every `or`/`and` inside a deciding condition of "
          "face_complex.py:\n")
    for o in all_ops:
        print("      %-22s %-6s c%d/%-2d %-10s %s"
              % (o.func, o.kind, o.index + 1, o.total,
                 "nested" if o.nested else "TOP LEVEL",
                 " ".join((o.source or "").split())[:44]))
    print("\n   %d in all: %d at the top level of their condition -- which is "
          "the sweep's\n   population, and the subject's `operands` column -- "
          "and %d NESTED, under a\n   comprehension or a quantifier."
          % (len(all_ops), len(top), len(nested)))
    claim("THE TOP-LEVEL COUNT THIS AUDIT READS AND THE ONE THE SUBJECT PRINTS "
          "AGREE: %d, so the disagreement below is about which operands are "
          "IN the population and not about how to count one" % len(top),
          len(top) == 11,
          "either enumerator changing, or the predicate layer gaining or "
          "losing a top-level clause.  The subject prints 11 in its `operands` "
          "column and sweeps 11 rows; this audit walks the tree with different "
          "code and gets the same 11",
          "top-level operands here: %d; rows in the subject's PER CLAUSE "
          "table: 11" % len(top))

    print("\nSO THE NESTED ONES ARE DELETED HERE, one at a time, exactly as "
          "the sweep deletes\nits eleven.  If they came back IDENTICAL the gap "
          "would be a bookkeeping one.\n")
    print("   %-22s %-6s %-4s %-10s %-5s %s"
          % ("function", "kind", "op", "artifact", "exit", "operand"))
    nested_rows = []
    for o in nested:
        out, code = run_battery(build_tree(
            extra={"face_complex.py": drop_operand(live, o)}))
        changed = out != base
        nested_rows.append((o, changed, code))
        print("   %-22s %-6s c%d/%-2d %-10s %-5d %s"
              % (o.func, o.kind, o.index + 1, o.total,
                 "CHANGES" if changed else "IDENTICAL", code,
                 " ".join((o.source or "").split())[:36]))
    load_bearing = [o for o, c, _x in nested_rows if c]
    claim("EVERY NESTED OPERAND WAS ACTUALLY REMOVED AND THE BATTERY ACTUALLY "
          "RAN ON THE RESULT: %d patch(es), each parsed back and each battery "
          "exiting 0 or 1 rather than crashing"
          % len(nested_rows),
          all(x in (0, 1) for _o, _c, x in nested_rows) and nested_rows,
          "a mutated source that does not parse or a battery that dies, either "
          "of which would make an IDENTICAL row mean 'the run failed the same "
          "way' instead of 'the deletion moved nothing'",
          "; ".join("%s c%d exit %d" % (o.func, o.index + 1, x)
                    for o, _c, x in nested_rows))
    finding("E2", "RUNG SIX IS REAL AND IT IS LOAD-BEARING: %d explicit "
            "boolean operands in face_complex.py's deciding conditions are "
            "NESTED, so the sweep never deletes one, and %d of %d CHANGE the "
            "artifact when deleted here.  The bound sentence names `explicit "
            "boolean operands` as the level deletion reaches; deletion reaches "
            "%d of the %d there are, and the %d it misses are the ones whose "
            "deletion the battery would have SEEN."
            % (len(nested), len(load_bearing), len(nested), len(top),
               len(all_ops), len(nested)),
            "nested and load-bearing: "
            + "; ".join("%s c%d (%s)"
                        % (o.func, o.index + 1,
                           " ".join((o.source or "").split())[:30])
                        for o in load_bearing))

    # ----------------------------------------------------------------- rung 7
    head("3.  RUNG SEVEN -- the decision that is not in a condition at all")
    print("Naming a rung is cheap.  This one is named AND run, because the "
          "point of the\nexercise is that the chasing does not terminate and "
          "an unrun seventh rung is\njust a sentence.\n")
    print("The guard compares `shape_A` with `shape_B`.  Neither is computed "
          "in the guard:\n")
    print("      shape_A = [len(row) for row in A]")
    print("      shape_B = [len(row) for row in B]")
    print("      if len(shape_A) != len(shape_B) or any(...):")
    print("\nThe subject's five census columns all range over DECIDING "
          "CONDITIONS -- the test\nof an `if` that returns, and the value of a "
          "`return`.  Two assignments are not\neither, so the comprehensions "
          "that build the two things being compared are\noutside every column, "
          "including the one whose whole purpose is to have no grain.\n")
    import ast as _ast
    conds = deciding_conditions(live)
    nodes = expr_nodes(live)
    patched = live.replace(ASSIGN_OLD, ASSIGN_NEW)
    added = (len(list(_ast.walk(_ast.parse(patched))))
             - len(list(_ast.walk(_ast.parse(live)))))
    census_delta = expr_nodes(patched) - nodes
    claim("THE PATCH IS OUTSIDE THE GRAIN-FREE TOTAL, MEASURED RATHER THAN "
          "ARGUED: face_complex.py has %d deciding conditions carrying %d "
          "expression nodes, and the rung-7 patch moves the module's syntax "
          "node count by %+d while moving that total by %+d"
          % (len(conds), nodes, added, census_delta),
          nodes == 1002 and added != 0 and census_delta == 0,
          "the census being widened to statements, at which point this claim "
          "would need rewriting rather than being quietly true.  The number "
          "1002 is the subject's own and is re-derived here by different code",
          "%d deciding condition(s) in `absorb_trace`; the patch touches none "
          "of them"
          % len([c for c in conds if c[0] == "absorb_trace"]))

    out, code = run_battery(build_tree(
        [("face_complex.py", ASSIGN_OLD, ASSIGN_NEW)]))
    changed = out != base
    print("\n   the rung-7 patch, which removes NO return, NO statement and NO "
          "boolean operand:")
    print("      -%s      +%s" % (ASSIGN_OLD.rstrip("\n") + "\n",
                                  ASSIGN_NEW.rstrip("\n")))
    print("\n   artifact: %-10s exit %d"
          % ("CHANGES" if changed else "BYTE-IDENTICAL", code))
    mut_dir = build_tree([("face_complex.py", ASSIGN_OLD, ASSIGN_NEW)])
    live_fc = load(build_tree(), "face_complex")
    mut_fc = load(mut_dir, "face_complex")
    ctl = load(build_tree(), "controls")
    live_tr = live_fc.absorb_trace(SEP_A, SEP_B)
    mut_tr = mut_fc.absorb_trace(SEP_A, SEP_B)
    truth = ctl.absorbable_bruteforce(SEP_A, SEP_B)
    print("\n   and the predicate, asked about the pair the ORDER half exists "
          "for:")
    print("      A = %s   B = %s" % (SEP_A, SEP_B))
    print("      live tree     : absorbable=%s at gate %r"
          % (live_tr.absorbable, live_tr.gate))
    print("      rung-7 mutant : absorbable=%s at gate %r"
          % (mut_tr.absorbable, mut_tr.gate))
    print("      brute force over all 2^m sign vectors: %s" % truth)
    claim("THE RUNG-7 PATCH REALLY CHANGES THE DECISION, so its byte-identical "
          "artifact is a statement about the battery and not about the patch: "
          "the live predicate answers %s at gate %r and the mutant answers %s "
          "at gate %r on the separator pair, against a brute force that says %s"
          % (live_tr.absorbable, live_tr.gate, mut_tr.absorbable, mut_tr.gate,
             truth),
          live_tr.absorbable != mut_tr.absorbable
          and live_tr.absorbable == truth,
          "the separator pair ceasing to separate -- which would need `zip` to "
          "stop truncating.  The expected value is the enumerated definition "
          "and shares no line with `absorb_trace`")
    finding("E3", "RUNG SEVEN: A DECISION HOISTED OUT OF THE CONDITION IS "
            "OUTSIDE EVERY NUMBER THE SUBJECT PRINTS.  A one-token change to "
            "`shape_B = [len(row) for row in B]` reinstates exactly mg-0b07's "
            "defect -- the order half stops rejecting -- and leaves the "
            "artifact %s at exit %d while removing 0 returns, 0 statements and "
            "0 boolean operands.  The `%d expression nodes` column is offered "
            "as the total that depends on no classification; it depends on the "
            "classification `deciding condition`, and this patch is outside it."
            % ("BYTE-IDENTICAL" if not changed else "CHANGED", code, nodes),
            "the subject's own SELF_DEFECT_BRANCHES entry 9 says the "
            "expression-node total 'bounds how much is there and does not name "
            "what'; this is a case where it does not bound how much is there "
            "either")
    return report()


if __name__ == "__main__":
    sys.exit(main())
