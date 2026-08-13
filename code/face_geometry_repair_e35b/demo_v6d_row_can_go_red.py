#!/usr/bin/env python3
"""V6d, watched firing (mg-843d).  A row nobody has seen go red is not evidence.

V6d was added because V6b -- the census -- fired on `de86fee` and could not say
WHICH KIND of value had moved.  A row added for that reason has to answer two
questions before it is worth its runtime, and neither is answered by asserting
it:

  (1) CAN IT GO RED AT ALL, on an input nobody built it around?
  (2) DOES IT SEE ANYTHING V6b AND V6c DO NOT?  A row that can only fail
      alongside a scored row is REDUNDANT, not unfalsifiable -- de86fee's own
      commit message says so about two conjuncts it kept for that reason -- but
      redundancy has to be NAMED and not discovered later.

Four constructions, each a mutation of a THROWAWAY COPY of code/face_geometry/,
each scored by exactly the functions `verify_e35b.py` scores with:

  D0  the copy, unmutated                      all three GREEN
  D1  a PRINTED value moved into a branch the run never takes, and the
      artifact REGENERATED so the missing line is "committed"
                                               V6b GREEN, V6c GREEN, V6d RED
  D2  a new `%d` added in a branch nobody runs V6b RED,   V6c GREEN, V6d RED
  D3  a new `%d` added to what the run PRINTS, artifact regenerated
                                               V6b RED,   V6c GREEN, V6d RED
  D4  the artifact hand-edited                 V6b GREEN, V6c RED,   V6d RED

D1 IS THE LOAD-BEARING ONE and it is the answer to (2): a value stops being
printed and the record is regenerated to agree.  V6b is lexical and sees
nothing; V6c compares a fresh run to the committed file and both moved
together, so it sees nothing; V6a covers only the twelve counts in `TABLE`.
V6d is the only row in this instrument that goes red.

D2 AND D3 ARE THE ANSWER TO WHY THE SPLIT IS WORTH PRINTING: they move V6b by
the SAME amount -- one specifier -- and they are opposite events.  V6b reports
one number for both.  V6d says `unreached +1` for one and `printed +1` for the
other, which is the sentence somebody had to reconstruct by hand when V6b fired
for real.

The mutations are STRUCTURAL, not textual: the module is parsed, the AST is
edited, and `ast.unparse` writes the copy back.  A `sed` on a quoted phrase
would rot the first time controls.py is reworded -- which is precisely the
event this whole instrument exists for.  The round trip is checked: D0 must
reproduce the committed artifact byte for byte, or the technique is measuring
its own reformatting and every row below is void.

Exit 0 iff every cell comes out as tabulated above.
"""

import ast
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
sys.path.insert(0, HERE)

from verify_e35b import (                                        # noqa: E402
    CENSUS_DECLARED, CENSUS_REACH_DECLARED, census, census_reach, regenerate,
)

FN = "negative_control_incidence"
ROWS = ["V6b CENSUS", "V6c REGENERATED", "V6d REACH"]

EXPECTED = {
    "D0 the copy, unmutated":
        {"V6b CENSUS": True, "V6c REGENERATED": True, "V6d REACH": True},
    "D1 a PRINTED value moved into an unreachable branch, artifact regenerated":
        {"V6b CENSUS": True, "V6c REGENERATED": True, "V6d REACH": False},
    "D2 a new %d in a branch nobody runs":
        {"V6b CENSUS": False, "V6c REGENERATED": True, "V6d REACH": False},
    "D3 a new %d in what the run PRINTS, artifact regenerated":
        {"V6b CENSUS": False, "V6c REGENERATED": True, "V6d REACH": False},
    "D4 the artifact hand-edited":
        {"V6b CENSUS": True, "V6c REGENERATED": False, "V6d REACH": False},
}


# ---------------------------------------------------------------------------
# Scoring, through the shipped functions and not through a copy of them.
# ---------------------------------------------------------------------------
def score(probe_dir):
    """V6b / V6c / V6d, exactly as `verify_e35b.py` scores them."""
    src = open(os.path.join(probe_dir, "controls.py")).read()
    art = open(os.path.join(probe_dir, "controls_output.txt")).read()
    reach, _, probed = census_reach(probe_dir)
    return {
        "V6b CENSUS": census(src) == CENSUS_DECLARED,
        "V6c REGENERATED": regenerate(probe_dir) == art,
        "V6d REACH": (reach == CENSUS_REACH_DECLARED
                      and sum(reach.values()) == CENSUS_DECLARED["specifiers"]
                      and probed == art),
    }, {"specifiers": census(src)["specifiers"], "reach": reach}


# ---------------------------------------------------------------------------
# The mutations.  Each takes the module tree and returns it edited in place.
# ---------------------------------------------------------------------------
def _fn(tree):
    return next(f for f in ast.walk(tree)
                if isinstance(f, ast.FunctionDef) and f.name == FN)


def _guarded(body):
    """`if False: <body>` -- a statement that stays lexically present."""
    return ast.If(test=ast.Constant(value=False), body=body, orelse=[])


def _new_print(text):
    """A bare `print("<text> %d" % 1)` statement."""
    return ast.Expr(value=ast.Call(
        func=ast.Name(id="print", ctx=ast.Load()),
        args=[ast.BinOp(left=ast.Constant(value=text + " %d"),
                        op=ast.Mod(), right=ast.Constant(value=1))],
        keywords=[]))


def mutate_d1(tree, printed_lines):
    """Move the first PRINTED site's whole statement under `if False:`.

    Only a bare-expression statement is eligible: guarding an assignment would
    break the run instead of silencing a line, and this construction is about
    silencing a line.  The `%`-expression stays lexically where it was, which
    is the entire point -- the census cannot tell.
    """
    fn = _fn(tree)
    for i, stmt in enumerate(fn.body):
        if not isinstance(stmt, ast.Expr):
            continue
        if any(stmt.lineno <= ln <= (stmt.end_lineno or stmt.lineno)
               for ln in printed_lines):
            fn.body[i] = _guarded([stmt])
            return "guarded the statement at controls.py line %d" % stmt.lineno
    raise AssertionError("no bare-expression statement carries a printed site")


def mutate_d2(tree, _printed):
    fn = _fn(tree)
    fn.body.append(_guarded([_new_print("D2 never runs")]))
    return "appended `if False: print('... %d' % 1)` to the section"


def mutate_d3(tree, _printed):
    fn = _fn(tree)
    fn.body.append(_new_print("D3 does run"))
    return "appended `print('... %d' % 1)` to the section"


def build(mutation, printed_lines, regen, hand_edit=False):
    """A throwaway copy of the probe dir, mutated and scored.

    Returns (row, note, measured) -- the three verdicts, what was mutated, and
    the NUMBERS behind the verdicts, because "V6b reports the same number for
    D2 and D3" is the claim this file makes and a verdict column does not
    show it.
    """
    tmp = tempfile.mkdtemp(prefix="v6d_")
    try:
        dst = os.path.join(tmp, "face_geometry")
        shutil.copytree(PROBE, dst,
                        ignore=shutil.ignore_patterns("__pycache__"))
        path = os.path.join(dst, "controls.py")
        tree = ast.parse(open(path).read())
        note = mutation(tree, printed_lines) if mutation else "none"
        ast.fix_missing_locations(tree)
        open(path, "w").write(ast.unparse(tree))
        if regen:
            open(os.path.join(dst, "controls_output.txt"), "w").write(
                regenerate(dst))
        if hand_edit:
            with open(os.path.join(dst, "controls_output.txt"), "a") as fh:
                fh.write("a line added by hand, 99 of 99\n")
        verdicts, measured = score(dst)
        return verdicts, note, measured
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    print("V6d, watched firing.  Four mutations of a throwaway copy of "
          "code/face_geometry/, scored by verify_e35b.py's own functions.\n")

    reach, where, _ = census_reach(PROBE)
    print("baseline split on the real tree: %s" % reach)
    print("printed sites: %d, unreached at line(s) %s, discarded at line(s) %s\n"
          % (len(where["printed"]), where["unreached"], where["discarded"]))

    results, notes, measured = {}, {}, {}
    plan = [
        ("D0 the copy, unmutated", None, False, False),
        ("D1 a PRINTED value moved into an unreachable branch, artifact regenerated",
         mutate_d1, True, False),
        ("D2 a new %d in a branch nobody runs", mutate_d2, False, False),
        ("D3 a new %d in what the run PRINTS, artifact regenerated",
         mutate_d3, True, False),
        ("D4 the artifact hand-edited", None, False, True),
    ]
    for name, mutation, regen, hand_edit in plan:
        results[name], notes[name], measured[name] = build(
            mutation, where["printed"], regen=regen, hand_edit=hand_edit)

    width = max(len(k) for k in EXPECTED)
    print("  %-*s  %s" % (width, "construction",
                          "".join("%-18s" % r for r in ROWS)))
    for name in EXPECTED:
        print("  %-*s  %s" % (width, name,
                              "".join("%-18s" % ("GREEN" if results[name][r]
                                                 else "RED") for r in ROWS)))
    print()
    print("  the numbers behind the verdicts -- V6b is ONE total, V6d is the "
          "split of it:")
    for name in EXPECTED:
        m = measured[name]
        print("  %-3s census %d  reach %s%s"
              % (name.split(" ")[0], m["specifiers"], m["reach"],
                 ("   [%s]" % notes[name]) if notes[name] != "none" else ""))
    print("  D2 and D3 BOTH move the census by 1, in opposite directions of "
          "meaning: D2 lands in `unreached`, D3 in `printed`.  That sentence "
          "is the whole reason V6d exists.")

    print("\nD0 IS THE CONTROL ON THE TECHNIQUE: the AST round trip reproduces "
          "the committed artifact byte for byte (V6c GREEN above), so the RED "
          "cells below it are the mutations and not the reformatting.")
    print("NOT SHOWN: that V6d catches every way a value can stop being "
          "printed.  It is scored on ONE number per fate, so two changes that "
          "cancel are invisible to it -- the same limit V6b carries and states.")

    wrong = [(n, r) for n in EXPECTED for r in ROWS
             if results[n][r] != EXPECTED[n][r]]
    if wrong:
        print("\n%d cell(s) came out other than tabulated:" % len(wrong))
        for n, r in wrong:
            print("  - %s / %s: expected %s, got %s"
                  % (n, r, "GREEN" if EXPECTED[n][r] else "RED",
                     "GREEN" if results[n][r] else "RED"))
        return 1
    print("\n%d/%d cells as tabulated in this file's docstring.  V6d is the "
          "ONLY row that goes red on D1, and V6b reports the same number for "
          "D2 and D3 while V6d separates them."
          % (len(EXPECTED) * len(ROWS), len(EXPECTED) * len(ROWS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
