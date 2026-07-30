"""mg-5f9a part 1 -- THE REASON IS NOW EMITTED BY THE CODE PATH.

Three things are checked, in the order a sceptic would ask them.

  A. The refactor decided nothing differently.  `absorbable_by_diagonal_twist`
     is now a wrapper over `absorb_trace`; the decision is re-decided here by
     2-colouring and (m <= 8) by brute force over all 2^m sign vectors, and by
     `main`'s own copy of the predicate run in a temporary tree.

  B. The trace cannot disagree with the predicate, structurally: there is one
     implementation.  Checked as a fact about the source (the public predicate's
     body is a single `return absorb_trace(...)`), not only as a fact about this
     population -- an agreeing population is what mg-da45 had.

  C. mg-1c80's 57-of-297 disagreement is re-measured here, against the trace, so
     the size of what was corrected is this instrument's own number.  And the
     artifact is checked to print the TRACE's split and not the priority one.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern5f9a import (                                              # noqa: E402
    BAR, FG, MODES, ROW, absorbable_2colour, absorbable_bruteforce, eq, head,
    pair, priority_gate, PRE_REPAIR_REF, write_ref_tree,
)
from face_complex import (                                          # noqa: E402
    absorb_trace, absorbable_by_diagonal_twist, gate_violations, diagonal_moves,
)
from posets import all_posets                                       # noqa: E402

import d2_deletion as d2                                            # noqa: E402
"""Imported for its MUTATION TABLE only -- `UNITS`, the (tag, patch, unit)
list -- so the source-level census below can ask whether every rejecting
`return` in `absorb_trace` has a mutation of its own (mg-9220).  No battery is
run from here and no result of d2's is read; this is the deletion table checked
against the source it deletes from, which is the one place the bundling mg-e7bc
found could have been caught without running anything."""

SCORE = []


def claim(text, ok, detail="", differs_under=None):
    """`differs_under` is optional here and required in d2/d4.

    mg-e7bc's F3 is that this script carries none of them; it is not closed by
    mg-9220, which added the two that do carry one.  Two statements written to
    the standard is not the standard applied to sixteen, and saying so is
    cheaper than a sentence implying otherwise.
    """
    SCORE.append(ok)
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    if differs_under:
        print("        WOULD DIFFER UNDER: %s" % differs_under)


def main(nmax=5):
    # exactly NEGATIVE CONTROL 4's population: every poset on 2..nmax
    # elements up to isomorphism (controls.py:908).
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    print(BAR)
    print("mg-5f9a part 1 -- the gate label is returned BY the predicate")
    print(BAR)
    print("posets n <= %d: %d" % (nmax, len(ps)))

    # ------------------------------------------------------------------- A
    head("A. THE REFACTOR DECIDED NOTHING DIFFERENTLY")
    agree_2c = dis_2c = agree_bf = dis_bf = 0
    for P in ps:
        for mode in MODES + ["true", "facet_swap01"]:
            A, B = pair(P, incidence_mode=mode) if mode != "true" else pair(P)
            got = absorbable_by_diagonal_twist(A, B)
            if got == absorbable_2colour(A, B):
                agree_2c += 1
            else:
                dis_2c += 1
            if len(A) <= 8:
                if got == absorbable_bruteforce(A, B):
                    agree_bf += 1
                else:
                    dis_bf += 1
    claim("union-find (the shipped predicate) vs BFS 2-colouring: %d agree, %d "
          "disagree" % (agree_2c, dis_2c), dis_2c == 0)
    claim("union-find vs brute force over all 2^m sign vectors (m <= 8): %d "
          "agree, %d disagree" % (agree_bf, dis_bf), dis_bf == 0)

    # The PRE-REPAIR predicate, read from a pinned commit and not from `main`
    # (mg-04a8).  This claim is "the refactor decided nothing differently"; once
    # mg-5f9a merged, `main` WAS the refactor and the claim became "this tree
    # agrees with itself", which no defect can falsify.  ITS ANSWER WOULD DIFFER
    # UNDER: any edit to `absorb_trace` that changes a decision on the 516 pairs
    # below -- and, before the pin, under nothing at all.
    tmp, pre_sha = write_ref_tree(["face_complex.py", "posets.py"])
    sys.path.insert(0, tmp)
    for m in ("face_complex", "posets"):
        sys.modules.pop(m, None)
    import importlib
    old_fc = importlib.import_module("face_complex")
    old_pred = old_fc.absorbable_by_diagonal_twist
    sys.path.remove(tmp)
    for m in ("face_complex", "posets"):
        sys.modules.pop(m, None)
    importlib.import_module("face_complex")     # restore the working tree's
    importlib.import_module("posets")
    same = diff = 0
    for P in ps:
        for mode in MODES + ["true", "facet_swap01"]:
            A, B = pair(P, incidence_mode=mode) if mode != "true" else pair(P)
            if absorbable_by_diagonal_twist(A, B) == old_pred(A, B):
                same += 1
            else:
                diff += 1
    claim("this tree's predicate vs the PRE-REPAIR one at %s (%s), on the same "
          "%d pairs: %d identical, %d differ"
          % (PRE_REPAIR_REF, pre_sha[:7], same + diff, same, diff), diff == 0)

    # ------------------------------------------------------------------- B
    head("B. ONE IMPLEMENTATION -- checked in the SOURCE, not only in the counts")
    src = open(os.path.join(FG, "face_complex.py")).read()
    tree = ast.parse(src)
    fns = {n.name: n for n in ast.walk(tree)
           if isinstance(n, ast.FunctionDef)}
    body = [s for s in fns["absorbable_by_diagonal_twist"].body
            if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    delegates = (len(body) == 1 and isinstance(body[0], ast.Return)
                 and isinstance(body[0].value, ast.Attribute)
                 and isinstance(body[0].value.value, ast.Call)
                 and getattr(body[0].value.value.func, "id", "") == "absorb_trace"
                 and body[0].value.attr == "absorbable")
    claim("`absorbable_by_diagonal_twist` is a single `return absorb_trace(...)"
          ".absorbable` -- so the gate label and the answer come from ONE "
          "execution and cannot be produced by different orders",
          delegates,
          "AST body after the docstring: %d statement(s)" % len(body))
    returns = [n for n in ast.walk(fns["absorb_trace"])
               if isinstance(n, ast.Return) and isinstance(n.value, ast.Call)
               and getattr(n.value.func, "id", "") == "Trace"]
    labels = sorted({n.value.args[1].value for n in returns})
    literal = all(isinstance(n.value.args[1], ast.Constant) for n in returns)
    census = {}
    for n in returns:
        census[n.value.args[1].value] = census.get(n.value.args[1].value, 0) + 1
    claim("every `return` in `absorb_trace` carries its gate label as a LITERAL "
          "at the return site, and the four gates are all of them: %d returns, "
          "labels %s, per gate %s"
          % (len(returns), labels,
             ", ".join("%s %d" % (g, census[g]) for g in sorted(census))),
          literal and labels == ["diagonal", "magnitude", "parity", "shape"],
          differs_under=
          "a gate label computed instead of written at the return site, or a "
          "fifth label appearing.  The count was FROZEN AT 6 until mg-9220, "
          "which merged the `shape` gate's two returns into one; a literal "
          "here would only have had to be edited to 5, and it said nothing "
          "about what the returns are")
    # AND EVERY REJECTING RETURN IS DELETED BY EXACTLY ONE MUTATION (mg-9220).
    # mg-e7bc's finding was that the deletion test removed the `shape` gate's
    # two returns TOGETHER and its result was read as a statement about each.
    # Counting mutations against the SOURCE is what makes that impossible to
    # repeat silently: a return with no mutation of its own is a return nothing
    # has deleted, and a return in two mutations is a bundle.
    rejecting = [n for n in returns if isinstance(n.value.args[0], ast.Constant)
                 and n.value.args[0].value is False]
    src_lines = src.split("\n")
    after = [(t, e) for t, e, _u in d2.UNITS if t.startswith("AFTER")]
    cover, uncovered = [], []
    for n in rejecting:
        line = src_lines[n.lineno - 1].strip()
        hits = [t for t, e in after if line in e[1] and line not in e[2]]
        cover.append((line[:46], hits))
        if len(hits) != 1:
            uncovered.append((line, hits))
    accepting = [n for n in returns if n not in rejecting]
    claim("and each of the %d REJECTING returns is deleted by EXACTLY ONE "
          "mutation of d2_deletion.py's AFTER table -- %s.  The remaining %d "
          "return(s) accept, and deleting one of those leaves the function "
          "returning None rather than answering differently"
          % (len(rejecting),
             "; ".join("%s <- %s" % (ln, ",".join(h) or "NOTHING")
                       for ln, h in cover),
             len(accepting)),
          not uncovered and len(rejecting) > 0,
          "%d return(s) not covered by exactly one mutation: %s"
          % (len(uncovered),
             "; ".join("%s -> %s" % (ln.strip()[:40], h)
                       for ln, h in uncovered) or "none"),
          differs_under=
          "a return added to `absorb_trace` without a mutation of its own, or "
          "two returns bundled into one mutation again.  The second is what "
          "mg-e7bc found: `shape`'s two returns went together, the pair moved "
          "the artifact, and the first one alone moved nothing")
    ctl = open(os.path.join(FG, "controls.py")).read()
    ctl_fns = {n.name for n in ast.walk(ast.parse(ctl))
               if isinstance(n, ast.FunctionDef)}
    claim("controls.py defines NO gate procedure of its own -- `deciding_gate` "
          "is gone and nothing replaced it; the rows call `absorb_trace`",
          not any("gate" in f for f in ctl_fns) and "absorb_trace(" in ctl,
          "functions in controls.py with 'gate' in the name: %s"
          % (sorted(f for f in ctl_fns if "gate" in f) or "none"))

    # ------------------------------------------------------------------- C
    head("C. WHAT WAS CORRECTED, re-measured here (mg-1c80's 57 of 297)")
    print("   row  corruption                bites |  trace: diag mag par |"
          "  mg-da45 priority   | differ | both | signs")
    tot = {"app": 0, "differ": 0, "both": 0, "signs": 0,
           "d": 0, "m": 0, "p": 0, "pd": 0, "pm": 0, "pp": 0}
    for mode in MODES:
        app = differ = both = signs = 0
        tr_c = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
        pr_c = {"diagonal": 0, "magnitude": 0, "parity": 0, "shape": 0}
        for P in ps:
            L_true, target = pair(P)
            L_mut, _ = pair(P, incidence_mode=mode)
            if eq(L_mut, L_true):
                continue
            app += 1
            t = absorb_trace(L_mut, target)
            p = priority_gate(L_mut, target)
            tr_c[t.gate] += 1
            pr_c[p] += 1
            differ += t.gate != p
            signs += t.signs_read
            both += len(gate_violations(L_mut, target)
                        & {"diagonal", "magnitude"}) == 2
        print("   %-4s %-24s %5d | %13d %4d %3d | %8d %4d %3d | %6d | %4d | %5d"
              % (ROW[mode], mode, app,
                 tr_c["diagonal"], tr_c["magnitude"], tr_c["parity"],
                 pr_c["diagonal"], pr_c["magnitude"], pr_c["parity"],
                 differ, both, signs))
        for k, v in (("app", app), ("differ", differ), ("both", both),
                     ("signs", signs), ("d", tr_c["diagonal"]),
                     ("m", tr_c["magnitude"]), ("p", tr_c["parity"]),
                     ("pd", pr_c["diagonal"]), ("pm", pr_c["magnitude"]),
                     ("pp", pr_c["parity"])):
            tot[k] += v
    print("   %-4s %-24s %5d | %13d %4d %3d | %8d %4d %3d | %6d | %4d | %5d"
          % ("ALL", "", tot["app"], tot["d"], tot["m"], tot["p"],
             tot["pd"], tot["pm"], tot["pp"], tot["differ"], tot["both"],
             tot["signs"]))
    claim("the two orders disagree on %d of the %d biting pairs -- mg-1c80 "
          "measured 57 of 297 and that is what the artifact was printing"
          % (tot["differ"], tot["app"]),
          (tot["differ"], tot["app"]) == (57, 297))
    claim("BOTH forced gates are violated on %d of the %d, so on those the gate "
          "a trace names is a fact about the order and nothing more"
          % (tot["both"], tot["app"]), tot["both"] == 294)
    claim("the predicate read %d off-diagonal SIGNS in total over the %d pairs "
          "-- the one quantity in this table no ordering can move"
          % (tot["signs"], tot["app"]), tot["signs"] == 0)

    art = open(os.path.join(FG, "controls_output.txt")).read()
    tr_split = "I1 %d biting = %d diagonal + %d magnitude" % (72, 15, 57)
    pr_split = "I1 %d biting = %d diagonal + %d magnitude" % (72, 72, 0)
    claim("the artifact prints the TRACE's split for I1 (%r)" % tr_split,
          tr_split in art)
    claim("the artifact no longer prints the priority order's split (%r)"
          % pr_split, pr_split not in art)
    claim("the artifact warns, where it prints a gate, that the gates are not "
          "exclusive and the label is the first one REACHED",
          "the first one REACHED" in art and "not exclusive" in art)

    # routing is a different question, asked directly
    head("D. THE ROUTING QUESTION IS ASKED DIRECTLY (`diagonal_moves`)")
    for mode in MODES:
        app = moved = trace_diag = 0
        for P in ps:
            L_true, target = pair(P)
            L_mut, _ = pair(P, incidence_mode=mode)
            if eq(L_mut, L_true):
                continue
            app += 1
            moved += diagonal_moves(L_mut, target)
            trace_diag += absorb_trace(L_mut, target).gate == "diagonal"
        claim("%s: the diagonal MOVES on %d/%d; the trace happens to return at "
              "the diagonal gate on %d/%d.  Routing uses the first"
              % (ROW[mode], moved, app, trace_diag, app),
              moved == app or ROW[mode] == "I4")

    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN." % (len(SCORE), SCORE.count(False)))
    print(BAR)
    return 1 if not all(SCORE) else 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 5))
