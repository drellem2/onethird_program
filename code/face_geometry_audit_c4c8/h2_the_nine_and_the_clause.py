"""mg-c4c8 H2 -- THE NINE, RE-DERIVED AT THEIR OWN UNIT, AND THE LEVEL BELOW A
RETURN.

TWO QUESTIONS, and the second is the one this audit was pre-filed to ask.

1.  THE NINE.  "The deletion test bites 9 of 9" is the sentence mg-04a8 shipped,
    mg-e7bc re-measured and mg-9220 quotes.  The nine are mg-d0e2's
    `e1_deletion.py`, and that file no longer applies to this tree: its first
    mutation's anchor was deleted by mg-9220, so it aborts before running any of
    them.  So the nine are RE-DERIVED here from the live source by the syntax
    tree, run on the live tree, and -- the point -- each is reported with THE
    UNIT IT ACTUALLY REMOVES, measured from the two trees rather than declared.

    Four of the nine delete a `return`.  One deletes a statement that is not a
    return.  Two neutralise a CONDITION and delete nothing.  Two are not
    deletions at all.  "Per return on all nine" is therefore a question with an
    answer of five parts, and the answer is printed as five parts.

2.  THE LEVEL BELOW A RETURN.  mg-e7bc found a gate with two `return`s, deleted
    together, read as a statement about each.  mg-9220 MERGED them: one `return`,
    guarded by a condition with TWO CLAUSES.  The unit went from a pair of
    returns to a pair of clauses inside one return -- so the question the ticket
    asks, whether the granularity error recurs at a third level, is a question
    about clauses, and it is answered by deleting them.

    Population: every top-level `or`/`and` clause of every boolean condition
    that decides a `return` in face_complex.py -- read from the tree, not
    chosen.  Each is removed ALONE, the rest of the condition kept, and the whole
    battery is run.

3.  AND WHAT THE INERT CLAUSE DOES, asked on the LIVE tree.  The subject answers
    "remove it or show what it does" by loading the PINNED two-return
    implementation with its first RETURN cut and measuring that.  That is a
    measurement about the pinned tree.  The live tree's clause is never cut
    anywhere, so this file cuts it and measures the live function against its own
    unmutated self, over a population of SHAPES built here.

PREDICTIONS ARE REGISTERED BEFORE THE RUNS.  Where a prediction is informed by
H1's already-completed sweep this is said in the row rather than presented as
foresight.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernc4c8 import (BAR, FC, TWO_RETURN_REF, _splice, _walk,        # noqa: E402
                      claim, count_returns, delete_clause, delete_return,
                      finding, footer, guard_clauses, head, load_source, read,
                      returns, run_battery, run_with_source, tree_from_ref,
                      tree_from_worktree)


# --------------------------------------------------------------------- units
def _fn(tree, name):
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef,)) and node.name == name:
            return node
    raise SystemExit("no function %s" % name)


def stmt_census(src):
    """(statements, returns) counted from the tree.  The measurement that says
    what a patch removed, independent of anything the patch declares."""
    t = ast.parse(src)
    return (sum(1 for n in ast.walk(t)
                if isinstance(n, ast.stmt) and not isinstance(n, ast.Pass)),
            count_returns(src))


def unit_delta(before, after):
    """What one mutation actually did, in units: (returns removed, statements
    removed, boolean clauses removed)."""
    sb, rb = stmt_census(before)
    sa, ra = stmt_census(after)

    def clauses(src):
        return sum(len(n.values) - 1 for n in ast.walk(ast.parse(src))
                   if isinstance(n, ast.BoolOp))
    return rb - ra, sb - sa, clauses(before) - clauses(after)


# ------------------------------------------------- the nine, on the live tree
def m_return(src, index):
    pop = returns(src)
    return delete_return(src, pop[index - 1][4])


def m_del_stmt(src, needle):
    """Delete the one statement whose source segment is `needle`."""
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, ast.stmt):
            continue
        seg = ast.get_source_segment(src, node)
        if seg == needle:
            return _splice(src, node.lineno, node.col_offset, node.end_lineno,
                           node.end_col_offset, "pass")
    raise SystemExit("no statement %r" % needle)


def m_replace_test(src, funcname, k, new_text):
    """Replace the test of the k-th `if` inside `funcname`."""
    t = ast.parse(src)
    fn = _fn(t, funcname)
    ifs = [n for n in ast.walk(fn) if isinstance(n, ast.If)]
    node = ifs[k].test
    return _splice(src, node.lineno, node.col_offset, node.end_lineno,
                   node.end_col_offset, new_text, allow_prefix=True)


def m_invert_return(src, funcname, which=-1):
    """Wrap one return of `funcname` in `not (...)`, indexed IN SOURCE ORDER.

    THE SORT IS NOT COSMETIC AND THIS INSTRUMENT LEARNED IT THE HARD WAY.  The
    first run of this file took `[n for n in ast.walk(fn) if isinstance(n,
    ast.Return)][-1]`, and `ast.walk` is breadth-first: `diagonal_moves`'s
    routing return is a direct child of the function and its shape guard's
    `return False` is a grandchild, so the walk yields the routing one FIRST and
    `[-1]` selected the shape guard.  The mutation then declared "invert the
    routing quantity" and inverted something else -- which is the defect this
    audit exists to look for, committed by the audit, and caught by the
    registered prediction (N9 was predicted CHANGES/1 and observed
    IDENTICAL/0).  The miss is kept below as N9x, which is that accidental
    mutation promoted to a measurement of its own.
    """
    t = ast.parse(src)
    fn = _fn(t, funcname)
    rets = sorted((n for n in ast.walk(fn) if isinstance(n, ast.Return)),
                  key=lambda n: (n.lineno, n.col_offset))
    node = rets[which].value
    seg = ast.get_source_segment(src, node)
    return _splice(src, node.lineno, node.col_offset, node.end_lineno,
                   node.end_col_offset, "not (%s)" % seg, allow_prefix=True)


def m_swap_forced_gates(src):
    """The two forced gates in absorb_trace's row loop, in the other order."""
    t = ast.parse(src)
    fn = _fn(t, "absorb_trace")
    loop = next(n for n in fn.body if isinstance(n, ast.For))
    a, b = loop.body[0], loop.body[1]
    lines = src.split("\n")
    blk_a = lines[a.lineno - 1:a.end_lineno]
    blk_b = lines[b.lineno - 1:b.end_lineno]
    return "\n".join(lines[:a.lineno - 1] + blk_b + blk_a
                     + lines[b.end_lineno:])


# (tag, what mg-d0e2 called it, builder, predicted change, predicted exit, note)
NINE = [
    ("N1", "delete gate 'shape'", lambda s: m_return(s, 46), True, 1,
     "H1 #46 ran this exact edit"),
    ("N2", "delete gate 'diagonal'", lambda s: m_return(s, 47), True, 0,
     "H1 #47"),
    ("N3", "delete gate 'magnitude'", lambda s: m_return(s, 48), True, 1,
     "H1 #48"),
    ("N4", "delete gate 'parity'", lambda s: m_return(s, 50), True, 1,
     "H1 #50"),
    ("N5", "stop counting signs_read",
     lambda s: m_del_stmt(s, "signs_read += 1"), True, 0,
     "blind: the artifact prints signs-read totals"),
    ("N6", "swap the two forced gates' order", m_swap_forced_gates, True, 0,
     "blind: same answers, different trace label"),
    ("N7", "delete 'diagonal' from gate_violations",
     lambda s: m_replace_test(s, "gate_violations", 1, "False"), True, 0,
     "blind: the both-gates-violated counts are printed"),
    ("N8", "delete 'magnitude' from gate_violations",
     lambda s: m_replace_test(s, "gate_violations", 2, "False"), True, 0,
     "blind: row I4's 'the ONLY one violated' sentence is computed here"),
    ("N9", "invert diagonal_moves (the routing)",
     lambda s: m_invert_return(s, "diagonal_moves", -1), True, 1,
     "blind: the routing row scores the split"),
    ("N9x", "invert diagonal_moves's SHAPE return (this audit's own slip)",
     lambda s: m_invert_return(s, "diagonal_moves", 0), False, 0,
     "registered AFTER the slip and said so: H1 #54 is inert whole, so "
     "inverting it should be invisible too"),
]

# The clause sweep.  Predicted by (function, kind, k) so the table cannot be
# silently re-ordered under the predictions.
CLAUSE_PRED = {
    ("absorb_trace", "guard", 0): (False, 0,
                                   "THE THIRD LEVEL: the battery's two shape "
                                   "pairs are both caught by clause 1"),
    ("absorb_trace", "guard", 1): (True, 1, "the ragged pair needs this clause"),
    ("gate_violations", "guard", 0): (False, 0, "H1 #52 is inert whole"),
    ("gate_violations", "guard", 1): (False, 0, "H1 #52 is inert whole"),
    ("diagonal_moves", "guard", 0): (False, 0, "H1 #54 is inert whole"),
    ("diagonal_moves", "guard", 1): (False, 0, "H1 #54 is inert whole"),
    ("Poset.leq", "value", 0): (False, 0, "H1 #2: no call site"),
    ("Poset.leq", "value", 1): (False, 0, "H1 #2: no call site"),
    ("Poset.comparable", "value", 0): (False, 0, "H1 #3 is inert whole"),
    ("Poset.comparable", "value", 1): (False, 0, "H1 #3 is inert whole"),
    ("Poset.comparable", "value", 2): (False, 0, "H1 #3 is inert whole"),
}


# ------------------------------------------------------- the shape population
def shape_population():
    """Matrices enumerated by SHAPE PROFILE, which is what the clause under test
    is about.

    Every row-width tuple of length 0..3 with widths in 0..3 -- 85 shapes --
    filled two ways by a fixed rule.  Deliberately NOT the subject's population
    (every square matrix over {0,1,-1} of order <= 2 plus four hand-added ragged
    ones): a clause that reads `len(A)` against `len(B)` and row widths against
    row widths is separated by SHAPES, and a population indexed by entries can
    only reach the shapes someone remembered to append.
    """
    shapes = [()]
    for a in range(4):
        shapes.append((a,))
        for b in range(4):
            shapes.append((a, b))
            for c in range(4):
                shapes.append((a, b, c))
    mats = []
    for sh in shapes:
        for rule in (0, 1):
            m = [[((i + j + rule) % 3) - 1 for j in range(w)]
                 for i, w in enumerate(sh)]
            mats.append((sh, rule, m))
    return mats


def ask(fn, A, B):
    try:
        tr = fn(A, B)
        return (tr.absorbable, tr.gate)
    except Exception as exc:                                    # noqa: BLE001
        return ("raised", type(exc).__name__)


def main():
    print(BAR)
    print("mg-c4c8 H2 -- the nine at their own unit, and the level below a "
          "return")
    print(BAR)

    src = read(FC)
    base_dir = tree_from_worktree()
    base_out, base_code = run_battery(base_dir)
    claim(base_code == 0 and len(base_out) > 0,
          "baseline: the unmutated tree exits 0 and writes %d bytes"
          % len(base_out),
          "the worktree being dirty, which would make every comparison below "
          "against a tree nobody committed",
          "exit %d" % base_code)

    # ------------------------------------------------------------- the nine
    head("1. THE NINE, RE-DERIVED FROM THE LIVE SOURCE AND RUN ON THE LIVE TREE")
    print("mg-d0e2's e1_deletion.py cannot run here -- mg-9220 deleted the text "
          "its first\nmutation anchors on.  These are the same nine intents, "
          "located in the syntax tree\ninstead of by string anchor, so they "
          "apply to whatever the tree currently says.\n")
    print("PREDICTIONS, registered before the runs:")
    for tag, what, _b, pc, pe, note in NINE:
        print("   %-4s %-42s %-10s exit %d   (%s)"
              % (tag, what, "CHANGES" if pc else "IDENTICAL", pe, note))
    print()
    print("   %-4s %-42s %-10s %-5s %-24s %s"
          % ("tag", "mutation", "artifact", "exit", "UNIT ACTUALLY REMOVED",
             "match"))
    nine_rows = []
    for tag, what, build, pc, pe, _note in NINE:
        mut = build(src)
        dr, ds, dc = unit_delta(src, mut)
        out, code = run_with_source(base_dir, "face_complex.py", mut)
        changed = out != base_out
        ok = (changed == pc) and (code == pe)
        unit = "%d return, %d stmt, %d clause" % (dr, ds, dc)
        nine_rows.append((tag, what, changed, code, dr, ds, dc, ok))
        print("   %-4s %-42s %-10s %-5d %-24s %s"
              % (tag, what[:42], "CHANGES" if changed else "IDENTICAL", code,
                 unit, "match" if ok else "*** MISS ***"))

    misses = [r for r in nine_rows if not r[7]]
    print("\n  %d of %d matched." % (len(nine_rows) - len(misses),
                                     len(nine_rows)))
    print("  (N9x is this audit's own slip, promoted to a measurement; see "
          "`m_invert_return`.)")
    for tag, what, changed, code, _dr, _ds, _dc, _ok in misses:
        pred = [p for p in NINE if p[0] == tag][0]
        print("   MISS %-4s predicted %s/%d, observed %s/%d"
              % (tag, "C" if pred[3] else "I", pred[4],
                 "C" if changed else "I", code))

    core = [r for r in nine_rows if r[0] != "N9x"]
    per_return = [r for r in core if r[4] == 1]
    no_return = [r for r in core if r[4] == 0]
    claim(len(per_return) == 4 and len(no_return) == 5,
          "OF THE NINE, %d REMOVE EXACTLY ONE `return` AND %d REMOVE NONE.  "
          "'Per return on all nine' is not a property nine mutations can have: "
          "five of them are not deletions of a return at all -- one deletes a "
          "non-return statement, two neutralise a CONDITION, two are a "
          "reordering and an inversion"
          % (len(per_return), len(no_return)),
          "one of the nine changing what it removes.  The counts here are "
          "measured by parsing both trees, not read off any declaration -- "
          "which is the check pm-onethird asked for, applied to mg-d0e2's list "
          "as well as to mg-9220's",
          "; ".join("%s: %d return(s), %d stmt, %d clause"
                    % (t, dr, ds, dc)
                    for t, _w, _ch, _c, dr, ds, dc, _o in core))
    bite = [r for r in core if r[2]]
    claim(len(bite) == 9,
          "AND ALL NINE STILL BITE ON THE LIVE TREE: %d of 9 move the artifact "
          "-- mg-04a8's '9 of 9', re-measured after mg-9220 restructured the "
          "gate the first of them deletes" % len(bite),
          "the two UNREACHED_GATE_PAIRS rows leaving controls.py (N1 and N4 go "
          "byte-identical, which is the state mg-d0e2 found), or the merged "
          "`shape` condition losing its second clause (N1 stops being visible "
          "to the 2x2-against-ragged pair)",
          "; ".join("%s %s exit %d" % (t, "CHANGES" if ch else "IDENTICAL", c)
                    for t, _w, ch, c, _dr, _ds, _dc, _o in core))

    live_touch = [t for t, w, *_ in core
                  if "gate_violations" in w or "diagonal_moves" in w]
    finding(len(live_touch) == 3,
            "THREE OF THE NINE ARE RUN BY NOTHING IN THE TREE.  %s target "
            "`gate_violations` and `diagonal_moves`; d2_deletion.py's eleven "
            "mutations touch neither function, and mg-d0e2's e1_deletion.py -- "
            "the only instrument that ever ran them -- aborts on this tree at "
            "its first mutation because mg-9220 deleted the text it anchors "
            "on.  d4_auditor_rerun.py preserves them by re-running e1 against "
            "the PINNED commit, which is a measurement about c7f9673.  On the "
            "live tree the standing evidence for those three is this file"
            % ", ".join(live_touch))

    # ------------------------------------------------------- the clause level
    head("2. THE LEVEL BELOW A RETURN -- every clause of every deciding "
         "condition")
    pop = guard_clauses(src)
    print("  population, read from the tree: %d clause(s) in %d condition(s)"
          % (len(pop), len({(q, k2) for q, k2, _k, _n, _t, _v, _w in
                            [(a, b, c, d, e, f, g) for a, b, c, d, e, f, g
                             in pop]})))
    for qual, kind, k, n, text, _val, _whole in pop:
        print("      %-30s %-6s clause %d of %d   %s"
              % (qual, kind, k + 1, n, text))
    print()
    print("PREDICTIONS, registered before the runs:")
    for qual, kind, k, _n, _t, _v, _w in pop:
        pc, pe, why = CLAUSE_PRED[(qual, kind, k)]
        print("   %-30s %-6s c%d  %-10s exit %d   (%s)"
              % (qual, kind, k + 1, "CHANGES" if pc else "IDENTICAL", pe, why))
    print()
    print("   %-30s %-6s %-4s %-10s %-5s %s"
          % ("function", "kind", "cls", "artifact", "exit", "match"))
    clause_rows = []
    for qual, kind, k, n, text, _val, whole in pop:
        mut = delete_clause(src, whole, k)
        out, code = run_with_source(base_dir, "face_complex.py", mut)
        changed = out != base_out
        pc, pe, _why = CLAUSE_PRED[(qual, kind, k)]
        ok = (changed == pc) and (code == pe)
        clause_rows.append((qual, kind, k, n, text, changed, code, ok))
        print("   %-30s %-6s %-4d %-10s %-5d %s"
              % (qual, kind, k + 1, "CHANGES" if changed else "IDENTICAL",
                 code, "match" if ok else "*** MISS ***"))
    cmiss = [r for r in clause_rows if not r[7]]
    print("\n  %d of %d matched." % (len(clause_rows) - len(cmiss),
                                     len(clause_rows)))
    for qual, kind, k, _n, _t, changed, code, _ok in cmiss:
        pc, pe, _why = CLAUSE_PRED[(qual, kind, k)]
        print("   MISS %-30s %s c%d predicted %s/%d, observed %s/%d"
              % (qual, kind, k + 1, "C" if pc else "I", pe,
                 "C" if changed else "I", code))

    shape_c0 = [r for r in clause_rows
                if r[0] == "absorb_trace" and r[2] == 0][0]
    finding(not shape_c0[5],
            "THE GRANULARITY ERROR RECURS AT THE THIRD LEVEL, IN THE STATEMENT "
            "THE REPAIR WROTE.  mg-9220 merged two `return`s into one guarded "
            "by `m != len(B) or any(len(A[i]) != len(B[i]) for i in "
            "range(m))`.  Deleting the RETURN moves the artifact (H1 #46, "
            "AFTER-5) -- and deleting the FIRST CLAUSE of its condition ALONE "
            "leaves the artifact BYTE-IDENTICAL, exit 0, every row green.  "
            "That is mg-e7bc's sentence with `return` replaced by `clause`: "
            "the deletion proves the CONDITION is load-bearing and proves "
            "nothing about either clause.  The unit moved from a pair of "
            "returns to a pair of clauses; the pair is still what the test "
            "bites on")

    # -------------------------------------- what the inert clause actually does
    head("3. WHAT THE INERT CLAUSE DOES -- asked of the LIVE function")
    print("The subject answers this by loading the PINNED two-return "
          "implementation with its\nfirst RETURN cut.  That is a measurement "
          "about c7f9673.  Here the LIVE merged\ncondition has its first "
          "CLAUSE cut, and the live function is compared with itself\nover a "
          "population indexed by SHAPE, which is what the clause reads.\n")
    two_dir, two_sha = tree_from_ref(TWO_RETURN_REF)
    two_fc = load_source(read(os.path.join(two_dir, "face_complex.py")),
                         "fc_two_c4c8")
    live_fc = load_source(src, "fc_live_c4c8")
    cut_src = delete_clause(src, [w for q, k2, k, n, t, v, w in pop
                                  if q == "absorb_trace" and k == 0][0], 0)
    cut_fc = load_source(cut_src, "fc_cut_c4c8")

    mats = shape_population()
    print("  population: %d matrices over %d distinct shape profiles, %d pairs"
          % (len(mats), len({sh for sh, _r, _m in mats}), len(mats) ** 2))
    # THREE OUTCOME CLASSES, kept apart on purpose.  "Same decision" is only a
    # meaningful comparison between two calls that both TERMINATE; lumping a
    # raised exception in with False is the equality-of-one-statistic error
    # this lineage keeps finding one level down.
    pairs = both_ok = same_dec = same_gate = 0
    old_raised_new_decided = new_raised_old_decided = both_raised = 0
    dec_moved_both_ok = 0
    raise_examples, dec_examples, cut_examples = [], [], []
    cut_dec = cut_gate = 0
    for _sa, _ra, A in mats:
        for _sb, _rb, B in mats:
            pairs += 1
            o = ask(two_fc.absorb_trace, A, B)
            n = ask(live_fc.absorb_trace, A, B)
            c = ask(cut_fc.absorb_trace, A, B)
            o_raised, n_raised = o[0] == "raised", n[0] == "raised"
            if o_raised and n_raised:
                both_raised += 1
            elif o_raised:
                old_raised_new_decided += 1
                if len(raise_examples) < 4:
                    raise_examples.append((A, B, o, n))
            elif n_raised:
                new_raised_old_decided += 1
            else:
                both_ok += 1
                same_dec += (o[0] == n[0])
                same_gate += (o == n)
                if o[0] != n[0] and len(dec_examples) < 4:
                    dec_examples.append((A, B, o, n))
                dec_moved_both_ok += (o[0] != n[0])
            cut_dec += (n[0] == c[0])
            cut_gate += (n == c)
            if n[0] != c[0] and len(cut_examples) < 4:
                cut_examples.append((A, B, n, c))
    print("  outcome classes: %d pairs -- %d where both implementations "
          "terminate, %d where BOTH raise, %d where the PINNED two-return form "
          "raises and the merged one decides, %d the other way round"
          % (pairs, both_ok, both_raised, old_raised_new_decided,
             new_raised_old_decided))
    claim(same_dec == both_ok and dec_moved_both_ok == 0,
          "WHERE BOTH FORMS TERMINATE THE MERGE IS DECISION-PRESERVING ON A "
          "POPULATION THE SUBJECT DID NOT CHOOSE: %d of %d such pairs, of "
          "which %d also agree on the gate label"
          % (same_dec, both_ok, same_gate),
          "the merged condition losing either clause, or the hoist changing an "
          "answer rather than a label.  The population here is 85 shape "
          "profiles rather than the subject's 89 mostly-square matrices, so "
          "this is not a re-run of their 7,921",
          "%d of the %d terminating pairs differ in the gate LABEL, which is "
          "the relabelling mg-9220 discloses"
          % (both_ok - same_gate, both_ok))
    finding(old_raised_new_decided > 0,
            "THE MERGE IS NOT OUTCOME-PRESERVING, AND THE POPULATION THAT "
            "SHOWS IT IS ONE THE SUBJECT'S CANNOT REACH.  On %d of %d pairs "
            "the pinned two-return `absorb_trace` RAISES IndexError and the "
            "merged one returns (False, 'shape') -- every one of them a matrix "
            "with a row SHORTER than the matrix's own order, where the old "
            "form indexed `A[i][i]` before it had checked row i's width.  "
            "mg-9220's docstring and landing say the merged gate gives 'the "
            "SAME DECISION on 7,921 of 7,921'; that is true of its population, "
            "every ragged member of which has rows at least as long as its "
            "order, and the sentence is read as a statement about the merge.  "
            "The change is an IMPROVEMENT -- a total function replacing a "
            "partial one -- and it is undisclosed: the only behaviour change "
            "mg-9220 discloses is the 126 gate relabellings.  Examples: %s"
            % (old_raised_new_decided, pairs,
               "; ".join("A widths %s vs B widths %s: pinned %s, merged %s"
                         % ([len(r) for r in A], [len(r) for r in B], o, n)
                         for A, B, o, n in raise_examples))
            if old_raised_new_decided else "")
    claim(cut_dec < pairs,
          "AND THE CLAUSE IS NOT INERT AS A PREDICATE, only as a battery "
          "input: cutting it from the LIVE condition moves the DECISION on %d "
          "of %d pairs and the (decision, gate) on %d"
          % (pairs - cut_dec, pairs, pairs - cut_gate),
          "the clause becoming genuinely redundant -- which is what a reader "
          "of the byte-identical row above would otherwise have to assume.  "
          "This is the measurement that makes the third-level finding a "
          "GRANULARITY finding and not a demand to delete the clause",
          "; ".join("A shape %s vs B shape %s: live %s, cut %s"
                    % ([len(r) for r in A], [len(r) for r in B], n, c)
                    for A, B, n, c in cut_examples))

    print("\n  So the answer to 'remove it, or show what it does' is SHOWN for "
          "the clause,\n  on the live tree, by this file.  What the subject "
          "shows is the same question\n  asked of the pinned tree's cut "
          "RETURN; the live clause is cut nowhere in the\n  repository, and "
          "the deletion test that reports per return does not report\n  per "
          "clause.")

    print("\n  pinned tree: %s (%s)" % (TWO_RETURN_REF, two_sha[:12]))
    return footer()


if __name__ == "__main__":
    sys.exit(main())
