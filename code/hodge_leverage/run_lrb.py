"""Verification of the face-semigroup (Brown/LRB) route, and of its scope.

Committed output: `lrb_output.txt`.

Checks, in order:
  1. F(P) is a left regular band under successive refinement: closure, x^2 = x,
     xyx = xy, associativity, two-sided identity.  Exhaustive, n <= 5.
  2. The set of supports equals the set of acyclic partitions of P (the source's
     description), and is closed under join = common refinement.  Exhaustive.
  3. Brown multiplicities m_X are nonnegative integers summing to |L(P)|.
  4. The predicted spectrum is the actual spectrum: for every distinct predicted
     eigenvalue, dim ker(M - Lambda I) equals the summed multiplicity, and the
     dimensions add up to |L(P)| -- which also certifies diagonalisability.
     Three weight families, so the check is not only on a generic w.
  5. SCOPE: the adjacent-transposition walk is NOT a Brown walk.  A face x can
     appear in a Brown walk all of whose steps stay inside {c} u N_AT(c) only if
     x.c in {c} u N_AT(c) for EVERY chamber c; we compute the set of faces with
     that property.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import Poset, rank_exact, rank_mod_p, linear_extensions
from posets import all_posets, cover_string
from lrb import (all_faces, lrb_product, support, support_lattice, refines,
                 is_acyclic_partition, all_set_partitions, brown_multiplicities,
                 brown_eigenvalues, brown_walk, weights_all_faces,
                 weights_two_block, weights_singleton_first)


def chamber_word(x):
    """The linear-extension word of a chamber (all blocks singletons)."""
    return tuple(b.bit_length() - 1 for b in x)


# --------------------------------------------------------------------------
# 1. the band axioms
# --------------------------------------------------------------------------

def check_band(P):
    faces = all_faces(P)
    fset = set(faces)
    idf = tuple([(1 << P.n) - 1])
    assert idf in fset, "identity face missing"
    bad = 0
    for x in faces:
        if lrb_product(x, x) != x:
            bad += 1
        if lrb_product(idf, x) != x or lrb_product(x, idf) != x:
            bad += 1
        for y in faces:
            xy = lrb_product(x, y)
            if xy not in fset:
                bad += 1
            if lrb_product(xy, x) != xy:
                bad += 1
    return len(faces), bad


def check_associativity(P):
    faces = all_faces(P)
    bad = 0
    for x in faces:
        for y in faces:
            xy = lrb_product(x, y)
            for z in faces:
                if lrb_product(xy, z) != lrb_product(x, lrb_product(y, z)):
                    bad += 1
    return bad


# --------------------------------------------------------------------------
# 2. the support lattice
# --------------------------------------------------------------------------

def check_supports(P):
    faces = all_faces(P)
    L = set(support_lattice(P, faces))
    acyc = {pi for pi in all_set_partitions(P.n) if is_acyclic_partition(P, pi)}
    joins_ok = True
    for X in L:
        for Y in L:
            # join = common refinement
            J = frozenset(a & b for a in X for b in Y if a & b)
            if J not in L:
                joins_ok = False
    return len(L), (L == acyc), joins_ok


# --------------------------------------------------------------------------
# 3./4. the spectrum
# --------------------------------------------------------------------------

def kernel_dim(M, lam, mod=None):
    m = len(M)
    D = {}
    for i in range(m):
        row = {}
        for j in range(m):
            v = M[i][j] - (lam if i == j else 0)
            if v:
                row[j] = v
        if row:
            D[i] = row
    if mod is None:
        r = rank_exact(D, m, m)
    else:
        r = rank_mod_p(D, m, m, p=mod)
    return m - r


def check_spectrum(P, wfun, exact=True, mod=None, label=""):
    faces = all_faces(P)
    w = wfun(faces)
    if not w:
        return None
    L = support_lattice(P, faces)
    mult = brown_multiplicities(P, L)
    lam = brown_eigenvalues(P, w, L, faces)
    chambers, M, total = brown_walk(P, w, faces)
    nL = len(chambers)

    negm = [X for X in L if mult[X] < 0]
    summ = sum(mult.values())

    # group predicted eigenvalues (integers, since M = total * Q)
    grouped = {}
    for X in L:
        grouped[lam[X]] = grouped.get(lam[X], 0) + mult[X]
    grouped = {v: c for v, c in grouped.items() if c > 0}

    got = {}
    for v in sorted(grouped):
        got[v] = kernel_dim(M, v, mod=None if exact else mod)
    ok = all(got[v] == grouped[v] for v in grouped)
    diagonalisable = sum(got.values()) == nL
    return {
        "label": label, "nL": nL, "nlat": len(L),
        "neg_mult": len(negm), "sum_mult": summ, "sum_ok": summ == nL,
        "n_distinct": len(grouped), "spectrum_ok": ok,
        "diagonalisable": diagonalisable,
    }


# --------------------------------------------------------------------------
# 5. scope: which faces could ever appear in an AT-supported walk
# --------------------------------------------------------------------------

def at_compatible_faces(P):
    """Two things, for the scope claim.

    `good` -- the faces x with x.c in {c} u N_AT(c) for every chamber c.  Any
    Brown walk whose steps all stay inside the adjacent-transposition graph must
    put ALL its weight on these (a face outside `good` has, at some chamber, a
    step that leaves the graph, and weights are nonnegative).

    `unreachable` -- the edges (c,d) of the adjacent-transposition graph for
    which no x in `good` has x.c = d.  The lazy AT walk gives every such edge
    probability 1/(2(n-1)) > 0, so if `unreachable` is nonempty the lazy AT walk
    is provably NOT a Brown walk: the linear system has no nonnegative solution,
    and no LP is needed to see it.
    """
    faces = all_faces(P)
    chambers = [x for x in faces if len(x) == P.n]
    words = {c: chamber_word(c) for c in chambers}
    wset = {words[c]: c for c in chambers}
    nbr = {}
    edges = []
    for c in chambers:
        wd = words[c]
        s = {wd}
        for t in range(P.n - 1):
            v = list(wd)
            v[t], v[t + 1] = v[t + 1], v[t]
            v = tuple(v)
            if v in wset:
                s.add(v)
                edges.append((c, wset[v]))
        nbr[c] = s
    good = []
    for x in faces:
        if all(words[lrb_product(x, c)] in nbr[c] for c in chambers):
            good.append(x)
    reach = set()
    for x in good:
        for c in chambers:
            reach.add((c, lrb_product(x, c)))
    unreachable = [(c, d) for (c, d) in edges if (c, d) not in reach]
    return len(chambers), good, unreachable, len(edges)


# --------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("1-2. F(P) IS A LEFT REGULAR BAND, AND ITS SUPPORTS ARE THE ACYCLIC")
    print("     PARTITIONS.  Exhaustive over all posets up to isomorphism.")
    print("=" * 78)
    for n in range(1, 6):
        tot_bad = tot_assoc = 0
        lat_ok = sup_ok = 0
        cnt = 0
        for P in all_posets(n):
            cnt += 1
            _, bad = check_band(P)
            tot_bad += bad
            if n <= 4:
                tot_assoc += check_associativity(P)
            _, eq, jok = check_supports(P)
            sup_ok += 1 if eq else 0
            lat_ok += 1 if jok else 0
        print("n=%d  posets=%3d   band-axiom violations=%d   associativity"
              " violations=%s   supports == acyclic partitions: %d/%d"
              "   join-closed: %d/%d"
              % (n, cnt, tot_bad, tot_assoc if n <= 4 else "(skipped)",
                 sup_ok, cnt, lat_ok, cnt))

    print()
    print("=" * 78)
    print("3. BROWN MULTIPLICITIES: nonnegative integers summing to |L(P)|")
    print("=" * 78)
    for n in range(1, 7):
        neg = 0
        bad = 0
        cnt = 0
        for P in all_posets(n):
            cnt += 1
            L = support_lattice(P)
            m = brown_multiplicities(P, L)
            if any(v < 0 for v in m.values()):
                neg += 1
            if sum(m.values()) != len(linear_extensions(P)):
                bad += 1
        print("n=%d  posets=%3d   posets with a negative m_X: %d"
              "   posets where sum m_X != |L(P)|: %d" % (n, cnt, neg, bad))

    print()
    print("=" * 78)
    print("4. THE PREDICTED SPECTRUM IS THE ACTUAL SPECTRUM")
    print("   exact rational rank computations; three weight families")
    print("=" * 78)
    fams = [("generic w on all faces", lambda f, P: weights_all_faces(f)),
            ("w on two-block faces only", lambda f, P: weights_two_block(f, P)),
            ("w on ({i},rest) faces (move-to-front)",
             lambda f, P: weights_singleton_first(f, P))]
    for name, fn in fams:
        for n in range(2, 5):
            oks = 0
            diags = 0
            cnt = 0
            skipped = 0
            for P in all_posets(n):
                r = check_spectrum(P, lambda f, P=P: fn(f, P), exact=True,
                                   label=name)
                if r is None:
                    skipped += 1
                    continue
                cnt += 1
                oks += 1 if (r["spectrum_ok"] and r["sum_ok"]
                             and r["neg_mult"] == 0) else 0
                diags += 1 if r["diagonalisable"] else 0
            print("  %-38s n=%d  posets checked=%2d (skipped %d, no such face)"
                  "  spectrum correct=%2d  diagonalisable=%2d"
                  % (name, n, cnt, skipped, oks, diags))

    print()
    print("  named larger instances (mod-p ranks, p = 2^31-1):")
    named = [("antichain A_5", Poset(5, [])),
             ("chain C_5", Poset(5, [(i, j) for i in range(5)
                                    for j in range(i + 1, 5)])),
             ("fence n=5", Poset(5, [(0, 1), (2, 1), (2, 3), (4, 3)])),
             ("C_2+C_3", Poset(5, [(0, 1), (2, 3), (3, 4), (2, 4)])),
             ("V+A_2 n=5", Poset(5, [(0, 1), (0, 2)])),
             ("A_6", Poset(6, []))]
    P_PRIME = (1 << 31) - 1
    for nm, P in named:
        if len(linear_extensions(P)) > 130:
            print("    %-14s |L(P)|=%d -- skipped (matrix too large for the"
                  " exact-rank budget)" % (nm, len(linear_extensions(P))))
            continue
        r = check_spectrum(P, lambda f, P=P: weights_all_faces(f), exact=False,
                           mod=P_PRIME, label=nm)
        print("    %-14s |L(P)|=%3d  |support lattice|=%3d  distinct eigenvalues"
              "=%3d  spectrum correct=%s  diagonalisable=%s"
              % (nm, r["nL"], r["nlat"], r["n_distinct"], r["spectrum_ok"],
                 r["diagonalisable"]))

    print()
    print("=" * 78)
    print("5. SCOPE: the lazy adjacent-transposition walk is NOT a Brown walk.")
    print("   A face x can carry weight in a Brown walk supported on the")
    print("   adjacent-transposition graph only if x.c in {c} u N_AT(c) for EVERY")
    print("   chamber c.  If some AT edge (c,d) is then unreachable -- no such x")
    print("   has x.c = d -- the lazy AT walk, which gives (c,d) probability")
    print("   1/(2(n-1)) > 0, cannot be written as sum_x w(x) T_x with w >= 0.")
    print("   ")
    print("   READ THE 'undecided by this test' ROWS WITH THIS (mg-a806, from the")
    print("   mg-86a3 audit, F1): the test below is SUFFICIENT only, and every")
    print("   case it leaves open is in fact DECIDED, and decided POSITIVELY --")
    print("   the lazy AT walk IS a Brown walk there, by exact rational LP with")
    print("   witnesses (code/hodge_leverage_audit_86a3/exact_lp.py).  The")
    print("   |L(P)| <= 4 boundary is an artifact of stopping at n = 5: at n = 6")
    print("   there is a positive with |L(P)| = 8, and the family V_k (ordinal sum")
    print("   of k 2-antichains, |L(P)| = 2^k) is positive for every k tested, so")
    print("   ledger row B6 is FALSIFIED as a universal rather than coverage-")
    print("   gapped.  The scope statement that STANDS is stronger: on V_k the AT")
    print("   graph is the hypercube Q_k, so Delta_AT is already diagonal -- THE")
    print("   SEMIGROUP TECHNIQUE REACHES Delta_AT ONLY WHERE Delta_AT IS ALREADY")
    print("   FREE.  Nothing printed below changes; what changes is what it means.")
    print("=" * 78)
    for n in range(2, 6):
        cnt = decisive = vacuous = undecided = 0
        undec = []
        for P in all_posets(n):
            cnt += 1
            nch, good, unreach, nedges = at_compatible_faces(P)
            if nedges == 0:
                vacuous += 1               # |L(P)| = 1: no AT edge at all
            elif unreach:
                decisive += 1
            else:
                undecided += 1
                undec.append((cover_string(P), nch, len(good), nedges))
        print("n=%d  posets=%3d   NOT a Brown walk (an AT edge is unreachable):"
              " %3d   vacuous (|L(P)|=1, no edge): %2d   undecided by this test:"
              " %2d" % (n, cnt, decisive, vacuous, undecided))
        for (cs, nch, ng, ne) in undec:
            print("      undecided: %-24s |L(P)|=%2d  AT edges=%2d  candidate"
                  " faces=%d" % (cs, nch, ne, ng))


if __name__ == "__main__":
    main()
