"""T1, T2, T6 -- the ONE place where this construction and the branching-graph
programme share an object, tested as an equality rather than a resemblance.

T1  For every partition lambda, J(D_lambda) is the interval [0, lambda] of
    Young's lattice, and the maximal chains of J(D_lambda) are the standard
    Young tableaux of shape lambda.  Both sides are built independently: the
    left from order ideals of the cell poset, the right from containment of
    Young diagrams and from column/row-increasing fillings, with the count
    checked against the hook length formula.

T2  How large is the overlap?  Two classes, not one: the posets P with
    J(P) = [0, lambda] are exactly the STRAIGHT cell posets D_lambda, and the
    posets P with J(P) = [mu, lambda] for a general interval are exactly the
    SKEW cell posets lambda/mu.  Both counted against all posets.  CORRECTED
    by mg-41aa under X1 of mg-6ad0's audit: this test used to assert the two
    classes were equal -- they are not, the 2-element antichain separates
    them -- and measured only the first.

T6  Does the monoid act on SYT(lambda) the way S_n acts on the Gelfand-Tsetlin
    basis of the irreducible S^lambda?  Measured: no move other than the
    identity map acts invertibly.
"""

import sys
from core_af28 import (partitions, conj, cell_poset, sub_shapes, contained,
                       hook_length_formula, ideals_of, linear_extensions,
                       moves_bruteforce, moves_from_chains, canon,
                       poset_classes, act, support, skew_cell_poset,
                       skew_shape_classes)

OUT = sys.stdout


def shape_of_ideal(I, cells, nrows):
    rows = [0] * nrows
    for a, (i, j) in enumerate(cells):
        if I >> a & 1:
            rows[i] += 1
    while rows and rows[-1] == 0:
        rows.pop()
    return tuple(rows)


def syt_of_shape(lam):
    """Standard Young tableaux of shape lambda, built directly: fillings of the
    diagram by 1..n increasing along rows and down columns.  Returned as tuples
    giving, for each value 1..n, the cell it occupies."""
    cells = [(i, j) for i, p in enumerate(lam) for j in range(p)]
    n = len(cells)
    out = []

    def rec(filled, seq):
        if len(seq) == n:
            out.append(tuple(seq))
            return
        for c in cells:
            if c in filled:
                continue
            i, j = c
            if i > 0 and (i - 1, j) not in filled:
                continue
            if j > 0 and (i, j - 1) not in filled:
                continue
            filled.add(c)
            seq.append(c)
            rec(filled, seq)
            seq.pop()
            filled.discard(c)
    rec(set(), [])
    return out


def t1(maxn=7):
    print("=" * 78, file=OUT)
    print("T1  J(D_lambda) = [0, lambda] in Young's lattice, and the maximal", file=OUT)
    print("    chains of J(D_lambda) = SYT(lambda).  Tested as equalities.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("  n  lam            |J(D_lam)|  |[0,lam]|  bad  e(D_lam)  |SYT|   HLF  bad", file=OUT)
    bad_iso = bad_syt = 0
    total = 0
    for n in range(1, maxn + 1):
        for lam in partitions(n):
            total += 1
            up, cells = cell_poset(lam)
            ids = ideals_of(up)
            shapes = sub_shapes(lam)
            # the map ideal -> shape
            img = [shape_of_ideal(I, cells, len(lam)) for I in ids]
            bijective = (len(set(img)) == len(ids) and set(img) == set(shapes))
            # order isomorphism, both directions, checked on every pair
            order_ok = True
            for a in range(len(ids)):
                for b in range(len(ids)):
                    sub_ideal = (ids[a] & ids[b] == ids[a])
                    sa, sb = img[a], img[b]
                    sub_shape = (len(sa) <= len(sb)
                                 and all(sa[k] <= sb[k] for k in range(len(sa))))
                    if sub_ideal != sub_shape:
                        order_ok = False
            ok_iso = bijective and order_ok
            if not ok_iso:
                bad_iso += 1
            le = linear_extensions(up)
            syt = syt_of_shape(lam)
            hlf = hook_length_formula(lam)
            # the maximal chains of J(D_lam) are the linear extensions of D_lam;
            # match them to SYT elementwise via the cell order
            le_as_cells = {tuple(cells[e] for e in c) for c in le}
            ok_syt = (le_as_cells == set(syt) and len(le) == hlf)
            if not ok_syt:
                bad_syt += 1
            print("%3d  %-14s %9d  %9d  %3s  %8d  %6d %5d  %3s"
                  % (n, str(lam), len(ids), len(shapes), "." if ok_iso else "BAD",
                     len(le), len(syt), hlf, "." if ok_syt else "BAD"), file=OUT)
    print(file=OUT)
    print("  partitions tested: %d   lattice-iso bad: %d   SYT/chain bad: %d"
          % (total, bad_iso, bad_syt), file=OUT)
    print(file=OUT)
    return total, bad_iso, bad_syt


def t2(maxn_full=6, maxn_shapes=8, maxn_skew=6):
    """CORRECTED by mg-41aa under X1 of mg-6ad0's audit.

    What this printed before: "the posets P for which J(P) is an interval of
    Young's lattice are EXACTLY the cell posets D_lambda", with the straight
    count as its measurement.  The word "exactly" was never tested by any line
    of this directory, and it is FALSE: an interval [mu, lambda] is J of the
    SKEW cell poset lambda/mu, and the 2-element ANTICHAIN -- which is no
    D_lambda -- has J(P) = [(1), (2,1)].  Both columns are now printed.
    """
    print("=" * 78, file=OUT)
    print("T2  How much of the family is Young?  Two questions, not one:", file=OUT)
    print("      which P have J(P) = [0, lambda]?   exactly the STRAIGHT cell", file=OUT)
    print("        posets D_lambda (T1).", file=OUT)
    print("      which P have J(P) = [mu, lambda], any interval?  exactly the", file=OUT)
    print("        SKEW cell posets lambda/mu.", file=OUT)
    print("    Counted against all posets.  CORRECTED by mg-41aa: the earlier", file=OUT)
    print("    version of this test asserted the second class equalled the", file=OUT)
    print("    first and measured only the first.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    a000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}
    # n = 7, 8 are not enumerated here: this file's canonical form is a
    # min over all n! relabellings, which costs ~5 min at n = 7 and hours at
    # n = 8 on the skew enumeration.  Stated with provenance, never silently.
    cited_skew = {7: 149, 8: 360}
    print("   n   straight D_lam   skew = interval posets   all posets"
          "   straight  interval", file=OUT)
    res = {}
    for n in range(1, maxn_shapes + 1):
        cls = {canon(cell_poset(lam)[0]) for lam in partitions(n)}
        k = len(cls)
        if n <= maxn_full:
            mine = len(poset_classes(n))
            assert mine == a000112[n], (n, mine)
            tot = mine
        else:
            tot = a000112[n]
        if n <= maxn_skew:
            sk = len(skew_shape_classes(n))
            mark = " "
        else:
            sk = cited_skew[n]
            mark = "*"
        res[n] = (k, sk, tot)
        print("  %2d   %14d   %21d%s   %10d   %8.4f  %8.4f"
              % (n, k, sk, mark, tot, k / tot, sk / tot), file=OUT)
    print(file=OUT)
    print("  * n = 7 and n = 8 skew counts are NOT enumerated in this file --", file=OUT)
    print("    this file's canonical form is a min over all n! relabellings and", file=OUT)
    print("    the skew enumeration costs minutes at n = 7 and hours at n = 8.", file=OUT)
    print("    Both were computed twice on other instruments, agreeing:", file=OUT)
    print("    code/branching_repair_41aa (r1_exactly.py, r1b_skew8.py) and", file=OUT)
    print("    code/branching_audit_6ad0/a2_intervals.py (n=8 behind SKEW8=1).", file=OUT)
    print("    The all-posets column is A000112, cited, for n = 7, 8 and", file=OUT)
    print("    enumerated here for n <= 6.", file=OUT)
    print(file=OUT)
    print("  THE WITNESS, so the correction is not taken on trust:", file=OUT)
    A2 = (0, 0)                               # the 2-element antichain
    straight2 = {canon(cell_poset(lam)[0]) for lam in partitions(2)}
    Q, qcells = skew_cell_poset((2, 1), (1,))
    print("    both 2-cell straight shapes (2) and (1,1) give the 2-CHAIN, so", file=OUT)
    print("    the 2-element ANTICHAIN is not any D_lambda: %s"
          % ("confirmed" if canon(A2) not in straight2 else "REFUTED"), file=OUT)
    print("    the skew shape (2,1)/(1) has cells %s and is the 2-element" % qcells,
          file=OUT)
    print("    antichain: %s"
          % ("confirmed" if canon(Q) == canon(A2) else "REFUTED"), file=OUT)
    interval = [nu for nu in sub_shapes((2, 1)) if contained((1,), nu)]
    print("    |J(2-antichain)| = %d = |[(1), (2,1)]| = %d, the interval being %s"
          % (len(ideals_of(A2)), len(interval),
             [str(x) for x in interval]), file=OUT)
    print(file=OUT)
    print("  Note: D_lambda and D_(lambda') are isomorphic posets (transpose),", file=OUT)
    print("  so the straight count is at most the number of partitions and is", file=OUT)
    print("  smaller; it is computed here by canonical form, not by that rule.", file=OUT)
    print("  The same holds for skew shapes under transposition of lambda/mu.", file=OUT)
    print(file=OUT)
    print("  READING.  The direction of section 0 consequence 1 -- ours contains", file=OUT)
    print("  theirs, as a vanishing fraction -- survives on BOTH columns.  The", file=OUT)
    print("  three numbers quoted in ledger B2 are the straight column and are", file=OUT)
    print("  reproduced here unchanged; they are not counts of the class B2", file=OUT)
    print("  named.  At n <= 3 EVERY poset is a skew shape poset.", file=OUT)
    print(file=OUT)
    return res


def t6(maxn=5):
    print("=" * 78, file=OUT)
    print("T6  Is the action of the monoid on the states the action of a group?", file=OUT)
    print("    For every poset: how many moves act on L(P) as a bijection, and", file=OUT)
    print("    how many of those act as something other than the identity map?", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes  moves   act bijectively   bijective & not identity map", file=OUT)
    grand = 0
    for n in range(1, maxn + 1):
        cls = poset_classes(n)
        tot_moves = tot_bij = tot_bad = 0
        for up in cls:
            le = linear_extensions(up)
            mv = moves_from_chains(up)
            tot_moves += len(mv)
            for x in mv:
                img = {act(x, c) for c in le}
                if len(img) == len(le):
                    tot_bij += 1
                    if any(act(x, c) != c for c in le):
                        tot_bad += 1
        grand += tot_bad
        print("  %2d  %7d  %5d   %15d   %28d"
              % (n, len(cls), tot_moves, tot_bij, tot_bad), file=OUT)
    print(file=OUT)
    print("  Every move is idempotent, so a move acting bijectively acts as the", file=OUT)
    print("  identity map.  Measured non-identity invertible elements: %d." % grand, file=OUT)
    print("  The image of F(P) in the transformation monoid of L(P) therefore", file=OUT)
    print("  contains no non-trivial invertible element: it is not a group, and", file=OUT)
    print("  for P = D_lambda it is not the S_n-action on the GT basis of S^lambda.", file=OUT)
    print(file=OUT)
    return grand


def t0_anchor(maxn=5):
    """Consistency anchor, independent of mg-ebd8: the moves defined by
    P-compatibility (the note's definition) and the chains in J(P) (Brown
    2000 §4.3's definition) are the same set, and the chain products agree."""
    print("=" * 78, file=OUT)
    print("T0  Anchor: P-compatible ordered set partitions = chains in J(P).", file=OUT)
    print("    (Re-derived here so that everything below rests on this file,", file=OUT)
    print("     not on mg-ebd8's instruments.)", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   n  classes  moves   set-equality bad", file=OUT)
    bad = 0
    for n in range(1, maxn + 1):
        cls = poset_classes(n)
        tot = 0
        b = 0
        for up in cls:
            a = set(moves_bruteforce(up))
            c = set(moves_from_chains(up))
            tot += len(a)
            if a != c:
                b += 1
        bad += b
        print("  %2d  %7d  %5d   %16d" % (n, len(cls), tot, b), file=OUT)
    print(file=OUT)
    return bad


if __name__ == "__main__":
    b0 = t0_anchor()
    t1res = t1()
    t2res = t2()
    t6res = t6()
    print("=" * 78, file=OUT)
    print("SUMMARY t_young: anchor bad %d; T1 iso bad %d, SYT bad %d; T6 bad %d"
          % (b0, t1res[1], t1res[2], t6res), file=OUT)
    print("=" * 78, file=OUT)
