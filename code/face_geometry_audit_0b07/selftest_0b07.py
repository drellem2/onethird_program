"""mg-0b07 selftest -- this audit's own primitives, on inputs whose answers are
known without running anything.

Every number in this audit comes out of `kern0b07`.  An instrument that measures
a grain and has never been checked at a grain it can be checked at is asking to
be believed, which is what the whole lineage is about.  So each primitive is
exercised on a case small enough to count by hand, INCLUDING the cases that
would make this audit wrong in the subject's own way:

  * counting a `pass` as a statement (a substituted statement would look retained);
  * counting `a or b or c` as one clause (one rung coarser than the tree);
  * taking `[-1]` of an `ast.walk` for "the last return" -- mg-c4c8's own slip;
  * a patch anchor that matches twice, which silently mutates two sites.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern0b07 import (                                          # noqa: E402
    BAR, apply_edits, census, delta, deciding_boolops, all_boolops, claim,
    report, returns_of, scored_rows, splice, strings_removed,
)

SRC = '''\
def f(a, b):
    """doc"""
    if a or b or a:
        return 1
    x = 2
    if a and b:
        pass
    return "gate"


def g():
    while a:
        return 3
    return 4
'''


def main():
    print(BAR)
    print("mg-0b07 selftest -- the audit's own primitives")
    print(BAR + "\n")

    c = census(SRC)
    # By hand: returns are `return 1`, `return "gate"`, `return 3`, `return 4`
    # = 4.  Other statements: 2 FunctionDefs, the docstring Expr, 2 Ifs in f,
    # 1 Assign, 1 While = 7; the `pass` is NOT one.  Clauses: `a or b or a` = 2,
    # `a and b` = 1, total 3.
    claim("census counts 4 returns, 7 other statements, 3 clauses on a source "
          "counted by hand -- got %d/%d/%d"
          % (c.returns, c.statements, c.clauses),
          (c.returns, c.statements, c.clauses) == (4, 7, 3),
          "`pass` being counted as a statement (8 instead of 7), or clauses "
          "being counted per BoolOp instead of per droppable operand (2 "
          "instead of 3).  Both are the ways this audit could be one rung "
          "coarser than the tree it reads")

    mut = SRC.replace("        return 1\n", "        pass\n")
    d = delta(SRC, mut)
    claim("a `return` substituted by `pass` reads as 1 return and 0 statements "
          "removed -- got %d/%d/%d" % (d.returns, d.statements, d.clauses),
          (d.returns, d.statements, d.clauses) == (1, 0, 0),
          "`pass` being counted, which would report -1 statements and make "
          "every narrowed patch in the subject look like it removed nothing")

    labs = strings_removed(SRC, SRC.replace('return "gate"', "return None"))
    claim("the label of a removed `return` is read from the string constant "
          "that left the tree -- got %s" % labs, labs == ["gate"],
          "a docstring or a comment being counted, or a string that occurs "
          "twice being reported as removed when one copy remains")

    rets = returns_of(SRC, "f")
    walk_last = [n for n in ast.walk(
        next(x for x in ast.walk(ast.parse(SRC))
             if isinstance(x, ast.FunctionDef) and x.name == "f"))
        if isinstance(n, ast.Return)][-1]
    claim("`returns_of` is in SOURCE order: the last return of `f` is line %d, "
          "and `[-1]` of an ast.walk gives line %d -- mg-c4c8's own slip, "
          "reproduced here to show this audit does not repeat it"
          % (rets[-1].line, walk_last.lineno),
          rets[-1].line > rets[0].line and len(rets) == 2,
          "`ast.walk` order being taken for source order.  It is "
          "breadth-first, so `[-1]` is not the last statement -- which is how "
          "mg-c4c8 inverted a different return than the one it declared")

    spliced = splice(SRC, rets[0].node, "pass")
    claim("`splice` replaces exactly one node's span and leaves the file "
          "parseable and one statement shorter",
          "        pass\n" in spliced and ast.parse(spliced) is not None
          and spliced.count("return") == SRC.count("return") - 1,
          "an off-by-one in the line-start table, which would corrupt the "
          "neighbouring statement instead of the target -- a mutation whose "
          "declaration and whose patch name different things, which is the "
          "defect this audit exists to look for")

    twice = False
    try:
        apply_edits("x = 1\nx = 1\n", [("f.py", "x = 1\n", "")])
    except SystemExit:
        twice = True
    claim("an anchor that matches twice is an ERROR, not a silent double "
          "mutation", twice,
          "`str.replace` being used without a count check.  A patch applied "
          "twice, or not at all, looks exactly like a patch the battery did "
          "not notice")

    dec = deciding_boolops(SRC)
    allb = all_boolops(SRC)
    # `a or b or a` decides a return; `a and b` guards a `pass`, and `while a`
    # has no BoolOp.  So 1 deciding, 2 in all.
    claim("`deciding_boolops` finds %d of the %d BoolOps -- the one that "
          "guards a return, and not the one that guards a `pass`"
          % (len(dec), len(allb)),
          len(dec) == 1 and len(allb) == 2,
          "the two populations being confused, which is how a claim about "
          "'every boolean condition' comes to be read as a claim about the "
          "file")

    rows = scored_rows("  [PASS] a\n  [FAIL] b\n  a bullet quoting [PASS] x\n"
                       "[CANNOT FAIL] c\n")
    claim("`scored_rows` reads the marker as the row's FIRST token: %d rows, "
          "not 4 -- the prose bullet quoting a marker is not a row"
          % len(rows),
          len(rows) == 3 and [m for m, _t in rows] == ["[PASS]", "[FAIL]",
                                                       "[CANNOT FAIL]"],
          "a substring scan, which is half of the defect mg-d0e2 found in the "
          "shipped check and which this audit would inherit by copying it")
    return report()


if __name__ == "__main__":
    sys.exit(main())
