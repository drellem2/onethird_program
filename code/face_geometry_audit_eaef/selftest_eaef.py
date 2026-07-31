"""mg-eaef selftest -- this audit's own primitives, on inputs counted by hand.

Every finding in e1-e5 rests on four functions written here: an enumerator that
walks for boolean operators instead of asking whether a condition is one, a
splicer that removes a single operand, a differ that computes what a patch
removed, and a direction function that says which way a declaration misses.
A finding produced by a miscounting enumerator is not a finding, so each is run
on a source small enough to count by eye, with the expected answer written down
beside it.

THE DIRECTION FUNCTION IS TESTED ON A CASE THE SUBJECT'S CANNOT PRODUCE.
mg-0b07's A2 is that a verdict column of the form `"exact" if got == reading
else "UNDERSTATES"` names a direction it never measures.  This one is asked
about an OVERSTATING pair and a MIXED pair, which are the two answers that
binary cannot give.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, boolean_operands, claim, declared_row, deciding_conditions,
    drop_operand, expr_nodes, head, report, unit_removed, direction,
)

TOY = '''
def a(x, y):
    if x > 0 and y > 0:
        return 1
    return 0


def b(items):
    return [i for i in items if i != 0 and i != 9]


def c(x):
    if x:
        print(x)
    return all(v > 0 and v < 9 for v in x)


def d(x):
    print(x)
'''


def main():
    print(BAR)
    print("mg-eaef selftest -- primitives on hand-counted inputs")
    print(BAR)

    head("1.  DECIDING CONDITIONS")
    print("The toy source has, by hand: `a` -- one guard (`x > 0 and y > 0`) "
          "and two return\nvalues (`1`, `0`); `b` -- one return value; `c` -- "
          "one return value, and its `if`\nis NOT a deciding condition because "
          "nothing under it returns; `d` -- none.\nThat is 1 guard + 4 return "
          "values = 5.\n")
    conds = deciding_conditions(TOY)
    for f, k, node in conds:
        print("   %-4s %-6s %s" % (f, k, ast.dump(node)[:56]))
    claim("5 deciding conditions, 1 of them a guard: got %d and %d"
          % (len(conds), sum(1 for c in conds if c[1] == "guard")),
          len(conds) == 5 and sum(1 for c in conds if c[1] == "guard") == 1,
          "the walk counting an `if` with no `return` under it, which would "
          "make `c`'s print-guard a deciding condition and every census "
          "number above it too large")

    head("2.  BOOLEAN OPERANDS, NESTED AND TOP-LEVEL")
    print("By hand: `a`'s guard is a top-level `and` with 2 operands.  `b`'s "
          "return value is a\nlist comprehension whose `if` holds an `and` "
          "with 2 operands -- NESTED.  `c`'s\nreturn value is `all(...)` whose "
          "generator holds an `and` with 2 -- NESTED.\nSo 6 operands in all, "
          "2 top-level and 4 nested.\n")
    ops = boolean_operands(TOY)
    for o in ops:
        print("   %-4s %-6s c%d/%d %-9s %s"
              % (o.func, o.kind, o.index + 1, o.total,
                 "nested" if o.nested else "TOP", o.source))
    top = [o for o in ops if not o.nested]
    claim("6 operands, 2 top-level and 4 nested: got %d, %d and %d"
          % (len(ops), len(top), len(ops) - len(top)),
          len(ops) == 6 and len(top) == 2,
          "the enumerator asking whether the CONDITION is a `BoolOp` instead "
          "of walking for them -- which is exactly the difference this audit "
          "measures, so it is scored here on a source where the answer is "
          "countable by eye")
    claim("AND THE TOP-LEVEL-ONLY MODE MATCHES THE SUBJECT'S SHAPE: asking for "
          "top-level operands alone returns the same %d" % len(top),
          len(boolean_operands(TOY, nested_too=False)) == len(top),
          "the two modes diverging, which would mean the 11-vs-15 comparison "
          "in e1 and e2 is between two different questions")

    head("3.  THE SPLICER")
    nested_op = [o for o in ops if o.nested][0]
    out = drop_operand(TOY, nested_op)
    line = [ln for ln in out.splitlines() if "for i in items" in ln][0]
    print("   before: %s"
          % [ln for ln in TOY.splitlines() if "for i in items" in ln][0].strip())
    print("   after : %s" % line.strip())
    claim("REMOVING ONE OPERAND LEAVES THE OTHER STANDING AND THE STATEMENT "
          "INTACT: the patched source parses, and `b`'s comprehension keeps "
          "its filter with one comparison instead of two",
          "i != 9" in line and "i != 0" not in line
          and len(boolean_operands(out)) == len(ops) - 2
          and ast.parse(out) is not None,
          "a splicer that removes the whole condition, which would make every "
          "CHANGES row in e1 a statement about a larger patch than the one it "
          "names")

    head("4.  THE DIFFER")
    before = "def f(x):\n    if x > 1 and x < 9:\n        return 1\n    return 0\n"
    cases = [
        ("delete the `return 1` and put `pass` in its place",
         before.replace("        return 1\n", "        pass\n"), (1, 0, 0)),
        ("delete the `if` and the `return` together",
         "def f(x):\n    return 0\n", (1, 1, 2)),
        ("delete one operand of the guard",
         before.replace("if x > 1 and x < 9:", "if x < 9:"), (0, 0, 1)),
        ("reorder nothing -- an identical file",
         before, (0, 0, 0)),
    ]
    for why, after, want in cases:
        got = unit_removed(before, after)[:3]
        print("   %-52s want %-10s got %s" % (why, want, got))
    claim("THE DIFFER AGREES WITH FOUR HAND-COUNTED PATCHES on (returns, other "
          "statements, boolean operands)",
          all(unit_removed(before, a)[:3] == w for _w, a, w in cases),
          "a `pass` inserted where a statement was removed cancelling the "
          "removal, or an operand left standing as a bare condition being "
          "counted as removed.  Both are ways of understating a patch, which "
          "is the defect the whole 8-of-11 measurement is about")

    head("5.  THE DIRECTION FUNCTION, ON THE TWO ANSWERS A BINARY CANNOT GIVE")
    rows = [((1, 0, 0), (1, 0, 0), "AGREES"),
            ((1, 0, 0), (1, 1, 0), "UNDERSTATES"),
            ((1, 1, 0), (1, 0, 0), "OVERSTATES"),
            ((1, 1, 0), (0, 2, 0), "MIXED")]
    for declared, measured, want in rows:
        got = direction(declared, measured)
        print("   declared %-10s measured %-10s -> %-12s (want %s)"
              % (declared, measured, got, want))
    claim("ALL FOUR DIRECTIONS ARE DISTINGUISHED, including OVERSTATES and "
          "MIXED -- the two a `exact / not exact` column reports as the same "
          "thing (mg-0b07's A2)",
          all(direction(d, m) == w for d, m, w in rows),
          "the function reducing to inequality, at which point the word "
          "`understate` in e4 would be a label rather than a measurement")

    head("6.  THE TRANSCRIPT ROW PARSER, AND THE NODE TOTAL")
    sample = ("   AFTER-4   0    1    0    4      0 `return`, 1 other "
              "statement(s), 0 boolean clause(s), 4 syntax node(s) in all, "
              "from `absorb_trace`")
    row = declared_row(sample, "AFTER-4")
    print("   parsed: %s" % (row[:4],))
    claim("THE DECLARATION ROW IS READ BY TAG, not by line number: (0, 1, 0, "
          "4) out of a line taken verbatim from the subject's own transcript",
          row is not None and row[:4] == (0, 1, 0, 4),
          "the subject changing the column order, at which point e3 would read "
          "the wrong numbers.  It is parsed by the tag it prints so a line "
          "moving does not silently change what is read")
    claim("AND `expr_nodes` COUNTS ONLY INSIDE DECIDING CONDITIONS: the toy "
          "source's %d node(s) exclude `d`, which has no deciding condition at "
          "all" % expr_nodes(TOY),
          expr_nodes(TOY) == sum(len(list(ast.walk(c)))
                                 for _f, _k, c in conds),
          "the total being widened to the whole module, which is the very "
          "widening e1's rung-7 finding says has NOT happened in the subject")
    return report()


if __name__ == "__main__":
    sys.exit(main())
