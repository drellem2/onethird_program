"""mg-c4c8 H1 -- THE PRIMARY MEASUREMENT: delete EVERY `return` INDIVIDUALLY and
report the artifact per return.

mg-9220 says the deletion test is now per RETURN.  The measurement that settles
that is not a table of the mutations its author chose; it is deleting every
return statement the file HAS, one at a time, and printing what happened to each.
So the population here is read out of the syntax tree:

    every `return` statement in code/face_geometry/face_complex.py

and each one is replaced -- ALONE -- by `pass` at its own indentation, the whole
control battery is run on the resulting tree, and the artifact is compared byte
for byte with the unmutated one.

WHY `pass` AND NOT DELETION OF THE LINES.  Many of these returns are the only
statement of their block.  Removing the lines would remove the enclosing `if` as
well, which is a LARGER unit -- and running a mutation larger than the one the
result is read as being about is precisely the defect this audit is auditing.

WHAT A BYTE-IDENTICAL ROW MEANS, and it is not "the return is wrong".  It means
the battery cannot see that return.  mg-e7bc's rule, which this audit adopts: a
return that is byte-identical under INDIVIDUAL deletion must have been removed,
or the document must say what it does.  A comment saying it is there for safety
is not a reason; a measurement against something outside the battery is.

THE POPULATION IS NAMED AND NOT TOTALLED.  56 returns in one file, of which 6 are
in `absorb_trace` (the function mg-9220 edited), 2 in `gate_violations`, 2 in
`diagonal_moves` and 1 in `absorbable_by_diagonal_twist` -- the four functions
mg-d0e2's nine mutations touch.  The other 45 are the rest of the file and they
are reported too, because "the deletion test bites" is a sentence about a
population and the population has to be visible for the sentence to mean
anything.

PREDICTIONS FOR ALL 56 ARE REGISTERED BELOW, WRITTEN BEFORE THE RUNS, and the
misses are kept as written.  A prediction table edited after its run is not a
prediction.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kernc4c8 import (BAR, FC, FINDINGS, SCORE, claim, delete_return,  # noqa: E402
                      finding, footer, head, read, returns, run_battery,
                      run_with_source, scored_rows, tree_from_worktree)

# The four functions mg-d0e2's nine mutations touch.  Named, so that the
# focused verdict below is about a stated set and not about "the interesting
# ones".
PREDICATE_LAYER = ("absorb_trace", "absorb_trace.find", "gate_violations",
                   "diagonal_moves", "absorbable_by_diagonal_twist")

# ---------------------------------------------------------------- PREDICTIONS
# (index, qualname, predicted artifact, predicted exit code, one-line reason).
# "C" = CHANGED, "I" = BYTE-IDENTICAL.  Written before any mutant was run, from
# reading the source and grepping for call sites -- not from a coverage trace.
PREDICTIONS = [
    (1, "Poset.__repr__", "I", 0, "no call site: nothing reprs a Poset"),
    (2, "Poset.leq", "I", 0, "no call site: `.leq(` occurs nowhere"),
    (3, "Poset.comparable", "C", 1, "controls.py:487 uses it"),
    (4, "Poset.automorphisms", "C", 1, "posets.py len(P.automorphisms())"),
    (5, "Poset.is_connected", "I", 0, "the n == 0 early exit; no empty poset"),
    (6, "Poset.is_connected", "C", 1, "posets.py branches on it"),
    (7, "Poset.is_antichain", "C", 1, "controls.py:388 and posets.py"),
    (8, "Poset.is_chain", "C", 1, "posets.py describes with it"),
    (9, "Poset.canonical_key", "C", 1, "posets.py keys a dict with it"),
    (10, "order_ideals", "C", 1, "the whole complex is built from it"),
    (11, "sur_iso.rec", "C", 1, "bare return: without it the recursion diverges"),
    (12, "sur_iso", "C", 1, "controls cross-checks the chain description"),
    (13, "face_from_sur_iso", "C", 1, "same cross-check"),
    (14, "proper_ideals", "C", 1, "vertices of the complex"),
    (15, "chains_of_ideals", "C", 1, "the complex itself"),
    (16, "linear_extensions.rec", "I", 0,
     "bare return at the base case; with all n placed the loop below skips "
     "every x, so control leaves the frame anyway"),
    (17, "linear_extensions", "C", 1, "facets are linear extensions"),
    (18, "le_to_facet", "C", 1, "every facet is built by it"),
    (19, "le_to_facet_offbyone", "C", 1, "NEGATIVE CONTROL 4's I4 mode"),
    (20, "facet_to_le", "C", 1, "controls.py uses it twice"),
    (21, "boundary_matrix", "C", 1, "every Laplacian"),
    (22, "down_laplacian_from_boundary", "C", 1, "every Laplacian"),
    (23, "top_laplacians", "C", 1, "the central object"),
    (24, "adjacent_transposition_graph", "C", 1, "claim (1)'s right side"),
    (25, "at_laplacian", "C", 1, "claim (1)'s right side"),
    (26, "_ambient_coxeter_laplacian", "C", 1,
     "the cache-hit return; two posets share an n, so it is taken"),
    (27, "_ambient_coxeter_laplacian", "C", 1, "the cache-miss return"),
    (28, "coxeter_compression", "C", 1, "controls.py uses it twice"),
    (29, "perm_sign", "C", 1, "the twist E = diag(sgn w)"),
    (30, "twist", "C", 1, "claim (1)'s left side"),
    (31, "rank_mod_p", "C", 1, "reduced_betti's default path"),
    (32, "rank_exact", "C", 1, "controls.py asks for exact ranks"),
    (33, "det_shift_mod_p", "I", 0,
     "the singular early exit; k in (3,5,7,11,13) is unlikely to be an "
     "eigenvalue of any matrix compared"),
    (34, "det_shift_mod_p", "I", 0,
     "returning None makes both sides None, the comparison False, and "
     "`not_isospectral` answers False -- which is the answer on the only "
     "pairs that reach the det test at all"),
    (35, "not_isospectral", "C", 1,
     "the trace early exit; without it a separated pair falls to frobenius2, "
     "which I expect NOT to separate at least one of them"),
    (36, "not_isospectral", "I", 0,
     "the frobenius early exit; the trace above catches the same pairs"),
    (37, "not_isospectral", "I", 0,
     "the det early exit; trace or frobenius catch the separated pairs first"),
    (38, "not_isospectral", "I", 0, "None is falsy exactly where False was"),
    (39, "reduced_betti", "C", 1, "controls.py checks Betti numbers"),
    (40, "mat_eq", "I", 0,
     "the length guard; every mat_eq call in controls.py is shape-guarded "
     "before it"),
    (41, "mat_eq", "C", 1, "None is falsy: every equality becomes False"),
    (42, "mat_sub", "C", 1, "residuals are printed"),
    (43, "is_diagonal", "C", 1, "controls.py tests diagonality"),
    (44, "trace", "C", 1, "controls.py prints traces"),
    (45, "frobenius2", "I", 0,
     "only `not_isospectral` calls it, and only after the trace test; None != "
     "None is False, so the answer does not move"),
    (46, "absorb_trace", "C", 1, "gate `shape` -- mg-9220's AFTER-5"),
    (47, "absorb_trace", "C", 0, "gate `diagonal` -- AFTER-1, trace only"),
    (48, "absorb_trace", "C", 1, "gate `magnitude` -- AFTER-2"),
    (49, "absorb_trace.find", "C", 1, "the union-find root; None unpacks badly"),
    (50, "absorb_trace", "C", 1, "the `parity` contradiction -- AFTER-6"),
    (51, "absorb_trace", "C", 1, "the accepting return; None has no .absorbable"),
    (52, "gate_violations", "I", 0,
     "the shape return.  controls.py calls gate_violations only after its own "
     "shape guard has `continue`d, so nothing reaches it"),
    (53, "gate_violations", "C", 1, "the violation set itself"),
    (54, "diagonal_moves", "I", 0,
     "the shape return, same reason as 52"),
    (55, "diagonal_moves", "C", 1, "the routing quantity itself"),
    (56, "absorbable_by_diagonal_twist", "C", 1,
     "the wrapper; None is falsy and rows quote it"),
]


def main():
    print(BAR)
    print("mg-c4c8 H1 -- every `return` in face_complex.py, deleted alone")
    print(BAR)

    src = read(FC)
    pop = returns(src)
    head("THE POPULATION -- enumerated from the syntax tree, not from a list")
    print("  file: code/face_geometry/face_complex.py (%d bytes)" % len(src))
    print("  %d `return` statements, in %d function(s)"
          % (len(pop), len({q for _i, q, _l, _t, _n in pop})))
    byfun = {}
    for _i, q, _l, _t, _n in pop:
        byfun[q] = byfun.get(q, 0) + 1
    layer = [q for q in PREDICATE_LAYER if q in byfun]
    print("  of these, %d are in the four functions mg-d0e2's nine mutations "
          "touch:" % sum(byfun[q] for q in layer))
    for q in layer:
        print("      %-32s %d" % (q, byfun[q]))
    print("  the remaining %d are the rest of the file"
          % (len(pop) - sum(byfun[q] for q in layer)))
    claim(len(pop) == len(PREDICTIONS),
          "every return in the file has a registered prediction -- %d returns, "
          "%d predictions" % (len(pop), len(PREDICTIONS)),
          "a return being added to or removed from face_complex.py without a "
          "prediction being written for it.  A population that grows while the "
          "prediction table does not is how a deletion test comes to cover "
          "less than it says",
          "predictions were written before any mutant ran")

    print("\nPREDICTIONS, registered before the runs "
          "(C = artifact CHANGES, I = BYTE-IDENTICAL):")
    print("   %-4s %-32s %-4s %-5s %s" % ("#", "function", "art", "exit", "why"))
    for i, q, a, c, why in PREDICTIONS:
        print("   %-4d %-32s %-4s %-5d %s" % (i, q, a, c, why[:60]))

    head("THE BASELINE")
    base_dir = tree_from_worktree()
    base_out, base_code = run_battery(base_dir)
    committed = read(os.path.join(os.path.dirname(FC), "controls_output.txt"))
    claim(base_out == committed and base_code == 0,
          "the unmutated tree regenerates the committed controls_output.txt "
          "byte-identically and exits 0 -- %d bytes" % len(base_out),
          "any edit to controls.py, face_complex.py or posets.py not followed "
          "by regenerating the artifact.  Every row below is a comparison "
          "against THIS run, not against the committed file, so a stale "
          "committed artifact would show up here and not silently downstream",
          "%d bytes regenerated, %d committed, exit %d"
          % (len(base_out), len(committed), base_code))

    head("EVERY RETURN, DELETED ALONE")
    print("   %-4s %-32s %-6s %-9s %-6s %-6s %s"
          % ("#", "function", "line", "artifact", "exit", "pred", "match"))
    results = []
    for (i, qual, lineno, _text, node) in pop:
        mut = delete_return(src, node)
        out, code = run_with_source(base_dir, "face_complex.py", mut)
        changed = out != base_out
        pred = [p for p in PREDICTIONS if p[0] == i][0]
        want_changed = (pred[2] == "C")
        ok = (changed == want_changed) and (code == pred[3])
        results.append((i, qual, lineno, changed, code, len(out), ok))
        print("   %-4d %-32s L%-5d %-9s %-6d %-6s %s"
              % (i, qual, lineno, "CHANGES" if changed else "IDENTICAL", code,
                 "%s/%d" % (pred[2], pred[3]),
                 "match" if ok else "*** MISS ***"))

    head("PREDICTION SCORE -- misses kept as written")
    misses = [r for r in results if not r[6]]
    print("  %d of %d matched." % (len(results) - len(misses), len(results)))
    for i, qual, lineno, changed, code, _n, _ok in misses:
        pred = [p for p in PREDICTIONS if p[0] == i][0]
        print("   MISS #%-3d %-32s predicted %s/%d, observed %s/%d"
              % (i, qual, pred[2], pred[3],
                 "C" if changed else "I", code))
    if not misses:
        print("   none")

    head("THE FOCUSED VERDICT -- the four functions the nine mutations touch")
    layer_rows = [r for r in results if r[1] in PREDICATE_LAYER]
    layer_ident = [r for r in layer_rows if not r[3]]
    print("  %d returns; %d CHANGE the artifact under individual deletion, "
          "%d leave it BYTE-IDENTICAL"
          % (len(layer_rows), len(layer_rows) - len(layer_ident),
             len(layer_ident)))
    for i, qual, lineno, changed, code, n, _ok in layer_rows:
        print("      #%-3d %-32s L%-5d %-9s exit %d, %d bytes"
              % (i, qual, lineno, "CHANGES" if changed else "IDENTICAL", code,
                 n))

    at = [r for r in results if r[1] in ("absorb_trace", "absorb_trace.find")]
    at_ident = [r for r in at if not r[3]]
    claim(not at_ident,
          "ABSORB_TRACE IS COVERED AT THE GRANULARITY OF A RETURN: all %d of "
          "its `return` statements, each deleted ALONE, move the artifact.  "
          "mg-e7bc's finding does not survive on this function" % len(at),
          "a `return` being added to `absorb_trace` that no constructed pair "
          "reaches -- which is the state its `shape` gate's first return was "
          "in until mg-9220, and the state 52 and 54 below are in now.  Also "
          "under `controls.py` losing the two UNREACHED_GATE_PAIRS rows: "
          "without them AFTER-5 and AFTER-6 go byte-identical again",
          "; ".join("%s L%d %s" % (q, ln, "CHANGES" if ch else "IDENTICAL")
                    for _i, q, ln, ch, _c, _n, _o in at))

    other_ident = [r for r in layer_ident if r[1] not in
                   ("absorb_trace", "absorb_trace.find")]
    finding(bool(other_ident),
            "%d MORE INERT RETURN(S) AT THE SAME GRANULARITY, IN THE SAME "
            "REPAIR'S BLAST RADIUS: %s.  Each is a `return` whose individual "
            "deletion moves NOT ONE BYTE of the artifact -- the exact "
            "condition mg-e7bc named for `absorb_trace`'s first `shape` "
            "return.  They are the shape guards of `gate_violations` and "
            "`diagonal_moves`, the two companion procedures the same "
            "docstrings cite; mg-9220 fixed the one return its ticket named "
            "and did not sweep the other two, and no mutation in "
            "d2_deletion.py deletes either of them"
            % (len(other_ident),
               "; ".join("%s L%d" % (q, ln)
                         for _i, q, ln, _ch, _c, _n, _o in other_ident))
            if other_ident else "")

    head("AND THE REST OF THE FILE -- the returns the battery cannot see")
    rest_ident = [r for r in results
                  if r[1] not in PREDICATE_LAYER and not r[3]]
    print("  %d of the %d returns outside the four functions are BYTE-IDENTICAL "
          "under individual deletion:"
          % (len(rest_ident), len(results) - len(layer_rows)))
    for i, qual, lineno, _ch, code, n, _ok in rest_ident:
        print("      #%-3d %-32s L%-5d exit %d, %d bytes" % (i, qual, lineno,
                                                             code, n))
    print("\n  This is CONTEXT, not a finding against mg-9220: its ticket is "
          "the `shape`\n  gate, and no claim in the repair says the whole file "
          "is deletion-covered.  It\n  is printed because '9 of 9' and '43 "
          "rows' are sentences about populations,\n  and the population of "
          "returns in this file is %d." % len(results))
    claim(True,
          "the file-wide census is reported rather than summarised: %d "
          "returns, %d byte-identical under individual deletion, %d of those "
          "inside the four functions the nine mutations touch"
          % (len(results), len(rest_ident) + len(layer_ident),
             len(layer_ident)),
          "nothing -- this claim is a report of the rows above and is scored "
          "TRUE by construction.  It is here so the number that a summary "
          "would carry is written beside the rows that produce it, which is "
          "mg-8aae's finding applied to this file",
          "byte-identical set: %s"
          % ", ".join("#%d %s" % (i, q) for i, q, _l, ch, _c, _n, _o in results
                      if not ch))

    return footer()


if __name__ == "__main__":
    sys.exit(main())
