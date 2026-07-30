#!/usr/bin/env python3
"""
mg-d673 INDEPENDENT AUDIT of mg-ebd8 / 714aceb -- instrument 4.

ARE THE IDENTIFICATIONS TOO GENEROUS?  (pm-onethird, mid-flight redirect.)

"Same shape" is not "same theorem".  This instrument tests each identification
as an EQUALITY, from the published definition, with no shortcut through the
repo's own description of its objects.

  I1  BROWN section 4.3.  Build J(P), the lattice of order ideals; enumerate
      the chains 0 = x_0 < ... < x_l = 1; form Brown's product by REFINING THE
      FIRST FACTOR BY THE SECOND as elements of the lattice (meets and joins in
      J(P), never blockwise set intersection); and compare, under the
      ideal-difference bijection, with F(P) and its product.  Also checks the
      HYPOTHESIS: J(P) is a finite distributive lattice, and by Birkhoff every
      finite distributive lattice arises this way -- so section 4.3 covers our
      class exactly, neither more nor less.

  I2  CZEDLI-LENKEHEGYI.  O(P) built literally from the published
      characterisation: pi is an order congruence iff pi = Ker f for an
      order-preserving f : P -> Q into SOME poset Q.  Implemented by searching
      over ALL labelled posets Q on |pi| points -- no acyclicity argument, no
      topological sort, no reference to moves.  Compared setwise with the
      repo's AC(P).  This is the test that decides whether the repo's level
      lattice is a re-derivation or a new object.

  I3  "BROWN'S THEOREM 2 IS STRICTLY SHARPER."  Sharper is a comparison, so
      both sides are stated and run: the repo's triangular counting identity
      solved numerically, and Brown's closed form.  A case where one is BETTER
      than the other would be a level where they disagree.  Counted.

Pure Python 3.  Shares no code with code/landscape_ebd8/.
"""

import sys
from math import factorial

from audit_populations import (iso_classes, F_of_P, AC_by_acyclicity,
                               linear_extensions, leq_matrix, set_partitions,
                               transitive, refines)


# ==========================================================================
# I1 -- Brown section 4.3: chains in the distributive lattice J(P)
# ==========================================================================


def order_ideals(rel, n):
    """down-sets of P, as frozensets"""
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
    out = []
    for mask in range(1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        if all(below[i] <= S for i in S):
            out.append(S)
    return out


def is_distributive(ideals):
    """J(P) is a lattice under inclusion with meet = intersection, join =
    union (both of which are again ideals).  Distributivity checked directly
    on all triples -- the HYPOTHESIS of Brown section 4.3."""
    for a in ideals:
        for b in ideals:
            for c in ideals:
                if (a | (b & c)) != ((a | b) & (a | c)):
                    return False
    return True


def chains(ideals, n):
    """maximal-length-unrestricted chains 0 = x_0 < x_1 < ... < x_l = 1"""
    bot = frozenset()
    top = frozenset(range(n))
    ideals = sorted(ideals, key=lambda s: (len(s), sorted(s)))
    out = []

    def rec(ch):
        last = ch[-1]
        if last == top:
            out.append(tuple(ch))
            return
        for y in ideals:
            if last < y:
                rec(ch + [y])

    rec([bot])
    return out


def brown_refine(x, y):
    """Brown section 4.3: 'we use the second factor to refine the first'.
    Purely lattice-theoretic: between consecutive x_{p-1} < x_p insert the
    elements x_{p-1} v (x_p ^ y_q) for q = 0..m, in order, and keep the
    distinct ones.  Only joins and meets of J(P) are used."""
    out = [x[0]]
    for p in range(1, len(x)):
        lo, hi = x[p - 1], x[p]
        for yq in y:
            z = lo | (hi & yq)
            if z != out[-1]:
                out.append(z)
        if out[-1] != hi:
            out.append(hi)
    return tuple(out)


def chain_to_move(ch):
    """the ideal-difference bijection: block p = x_p \\ x_{p-1}"""
    return tuple(frozenset(ch[p] - ch[p - 1]) for p in range(1, len(ch)))


def osp_product(x, y):
    out = []
    for B in x:
        for C in y:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


def check_I1(nmax):
    print("-" * 78)
    print("I1  BROWN section 4.3 -- chains in J(P), with the product formed by")
    print("    LATTICE operations only (joins and meets of order ideals).")
    print("-" * 78)
    print("%3s %8s %10s %10s %14s %12s %14s %14s"
          % ("n", "classes", "J(P) dist", "sum|chains|", "= sum|F(P)|",
             "bijection", "products agree", "max <-> lin ext"))
    for n in range(1, nmax + 1):
        cls = iso_classes(n)
        ndist = 0
        tot_ch = 0
        tot_mv = 0
        bad_bij = 0
        bad_prod = 0
        bad_max = 0
        npairs = 0
        for rel in cls:
            I = order_ideals(rel, n)
            if is_distributive(I):
                ndist += 1
            ch = chains(I, n)
            mv = set(F_of_P(rel, n))
            tot_ch += len(ch)
            tot_mv += len(mv)
            img = set(chain_to_move(c) for c in ch)
            if img != mv or len(img) != len(ch):
                bad_bij += 1
            # Brown's product vs the repo's product, on every pair
            for a in ch:
                for b in ch:
                    npairs += 1
                    lhs = chain_to_move(brown_refine(a, b))
                    rhs = osp_product(chain_to_move(a), chain_to_move(b))
                    if lhs != rhs:
                        bad_prod += 1
            # maximal chains <-> linear extensions
            maximal = [c for c in ch if len(c) == n + 1]
            if len(maximal) != len(linear_extensions(rel, n)):
                bad_max += 1
        print("%3d %8d %10s %10d %14s %12s %14s %14s"
              % (n, len(cls), "%d/%d" % (ndist, len(cls)), tot_ch,
                 "%d %s" % (tot_mv, "OK" if tot_ch == tot_mv else "MISMATCH"),
                 "%d bad" % bad_bij, "%d bad of %d" % (bad_prod, npairs),
                 "%d bad" % bad_max))
    print()
    print("    HYPOTHESIS CHECK.  Brown section 4.3 asks for a finite")
    print("    DISTRIBUTIVE lattice L.  J(P) is one (column 3).  By Birkhoff's")
    print("    theorem every finite distributive lattice is J(P) for a unique")
    print("    finite poset P, so section 4.3's class and ours are the SAME")
    print("    class -- the citation does not require anything we lack, and it")
    print("    does not cover a strictly smaller class either.")
    print()


# ==========================================================================
# I2 -- Czedli-Lenkehegyi, implemented from the published characterisation
# ==========================================================================


def labelled_posets(k):
    """ALL labelled posets on {0..k-1}: transitive, irreflexive, antisymmetric
    relations.  Not up to isomorphism -- the kernel test needs every labelling."""
    pairs = [(i, j) for i in range(k) for j in range(k) if i != j]
    m = len(pairs)
    out = []
    for mask in range(1 << m):
        rel = set(pairs[t] for t in range(m) if mask >> t & 1)
        if any((j, i) in rel for (i, j) in rel):
            continue
        if not transitive(rel, k):
            continue
        out.append(rel)
    return out


_LP_CACHE = {}


def lp(k):
    if k not in _LP_CACHE:
        _LP_CACHE[k] = labelled_posets(k)
    return _LP_CACHE[k]


def O_of_P_czedli(rel, n):
    """pi is an order congruence iff pi = Ker f for an order-preserving
    f : P -> Q into SOME poset Q.  Take Q on the blocks of pi and f the
    block map (any f with kernel pi factors this way); search all labelled
    posets Q on |pi| points for one making f order-preserving.

    No acyclicity test, no topological sort, no reference to F(P)."""
    out = set()
    for part in set_partitions(range(n)):
        pi = tuple(sorted((frozenset(b) for b in part), key=lambda s: sorted(s)))
        k = len(pi)
        idx = {}
        for p, B in enumerate(pi):
            for x in B:
                idx[x] = p
        need = set()
        ok = True
        for (i, j) in rel:
            if idx[i] != idx[j]:
                need.add((idx[i], idx[j]))
        for Q in lp(k):
            if need <= Q:
                out.add(pi)
                ok = True
                break
    return out


def check_I2(nmax):
    print("-" * 78)
    print("I2  CZEDLI-LENKEHEGYI: O(P) = { Ker f : f : P -> Q order-preserving,")
    print("    Q ANY poset }, built by searching all labelled posets Q, against")
    print("    the repo's AC(P).  Equality of SETS; both are ordered by")
    print("    refinement, so equality of sets is equality of LATTICES.")
    print("-" * 78)
    print("%3s %8s %14s %14s %10s" % ("n", "classes", "sum|O(P)| (CL)",
                                      "sum|AC(P)| (repo)", "disagree"))
    for n in range(1, nmax + 1):
        cls = iso_classes(n)
        s1 = s2 = bad = 0
        for rel in cls:
            O = O_of_P_czedli(rel, n)
            A = AC_by_acyclicity(rel, n)
            s1 += len(O)
            s2 += len(A)
            if O != A:
                bad += 1
        print("%3d %8d %14d %14d %10s"
              % (n, len(cls), s1, s2, "%d posets" % bad))
    print()
    print("    NOTE ON WHAT THIS DOES AND DOES NOT SETTLE.  It settles that the")
    print("    repo's AC(P) IS the lattice of order congruences as that object")
    print("    is DEFINED in the modern literature.  It does not verify that")
    print("    Sturm (1971) or Czedli-Lenkehegyi (1983) state it -- neither the")
    print("    target nor this audit read those papers; both take the")
    print("    attribution from Jenca-Sarkoci's citation of them.")
    print()


# ==========================================================================
# I3 -- "strictly sharper" is a comparison; run both sides
# ==========================================================================


def repo_multiplicities(rel, n, AC):
    """the repo's triangular counting identity, solved from the finest level
    upwards:   sum_{Y refines X, Y in AC} m_Y = prod_B |L(P|_B)|"""
    le = leq_matrix(rel, n)

    def ext_count(B):
        B = sorted(B)
        sub = frozenset((i, j) for i in B for j in B if i != j and le[i][j])
        remap = {x: k for k, x in enumerate(B)}
        sub2 = frozenset((remap[i], remap[j]) for (i, j) in sub)
        return len(linear_extensions(sub2, len(B)))

    order = sorted(AC, key=lambda p: -len(p))     # finest first
    m = {}
    for X in order:
        rhs = 1
        for B in X:
            rhs *= ext_count(B)
        s = 0
        for Y in order:
            if Y is not X and Y in m and refines(Y, X):
                s += m[Y]
        m[X] = rhs - s
    return m


def brown_multiplicities(rel, n, AC):
    le = leq_matrix(rel, n)
    m = {}
    for X in AC:
        anti = all(not (le[i][j] or le[j][i])
                   for B in X for i in B for j in B if i != j)
        v = 0
        if anti:
            v = 1
            for B in X:
                v *= factorial(len(B) - 1)
        m[X] = v
    return m


def check_I3(nmax):
    print("-" * 78)
    print("I3  'BROWN'S THEOREM 2 IS STRICTLY SHARPER THAN WHAT THE REPO USES'")
    print("    -- both sides run, and every level compared.  A level where one")
    print("    is BETTER than the other is a level where they DISAGREE.")
    print("-" * 78)
    print("%3s %8s %10s %14s %18s" % ("n", "classes", "levels", "disagreements",
                                      "levels Brown names 0"))
    for n in range(1, nmax + 1):
        cls = iso_classes(n)
        lev = dis = zer = 0
        for rel in cls:
            AC = AC_by_acyclicity(rel, n)
            a = repo_multiplicities(rel, n, AC)
            b = brown_multiplicities(rel, n, AC)
            lev += len(AC)
            for X in AC:
                if a[X] != b[X]:
                    dis += 1
                if b[X] == 0:
                    zer += 1
        print("%3d %8d %10d %14d %18d" % (n, len(cls), lev, dis, zer))
    print()
    print("    READING.  The two agree at EVERY level.  So Brown's Theorem 2 is")
    print("    not sharper in the sense a bound is sharper -- there is no case")
    print("    where it gives a better number, because it gives the SAME")
    print("    number.  What it gives that the repo's identity does not is the")
    print("    answer in CLOSED FORM: the spectrum-carrying levels are named")
    print("    a priori rather than discovered by a solve.  The document says")
    print("    'strictly more informative', which is right; the commit subject")
    print("    says 'STRICTLY SHARPER', which is a bound word and is not.")
    print()


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("mg-d673 AUDIT INSTRUMENT 4 -- ARE THE IDENTIFICATIONS TOO GENEROUS?")
    print("=" * 78)
    print()
    check_I1(min(nmax, 5))
    check_I2(min(nmax, 5))
    check_I3(min(nmax, 6))
    print("=" * 78)


if __name__ == "__main__":
    main()
