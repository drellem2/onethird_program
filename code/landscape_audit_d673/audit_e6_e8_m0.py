#!/usr/bin/env python3
"""
mg-d673 INDEPENDENT AUDIT of mg-ebd8 / 714aceb -- instrument 3 of 3.

THE THREE THINGS THE TARGET'S OWN PRE-FILED AUDIT RANKS 1, 2 AND 3 AS
UNMEASURED.  It named them; nobody measured them; here they are measured.

  E6  (its pre-filed item 2) "the sign-condition-to-block-order translation is
      asserted in prose and never measured on its own".  Measured here from a
      NUMERIC realisation of the braid arrangement: each ordered set partition
      is realised as a point, sign vectors are read off the coordinates, and
      Brown's G = { F : sigma_i(F) >= 0 for i in J } is compared setwise with
      the repo's F(P), with the Tits product compared against the repo's
      blockwise-intersection product.

  M_0 (its pre-filed item 3) "a wrong derivation that happens to produce the
      right set is possible".  The DOCUMENT states the closed form as
      "m_X = prod (|B|-1)! if every block of X is an antichain of P, and 0
      otherwise", over the flats X -- dropping the acyclicity condition that
      the instrument's OWN docstring carries.  Tested here as Brown states it,
      over ALL flats, against Brown's own total-multiplicity identity.

  E8  (its pre-filed item 1, "the weakest link ... An auditor should build both
      and compare") Bjorner's greedoid band on the poset shelling antimatroid,
      claimed to be "a proper submonoid of ours".  Built and compared.

Pure Python 3.  Shares no code with code/landscape_ebd8/.
"""

import sys
from itertools import permutations
from math import factorial

from audit_populations import (iso_classes, F_of_P, AC_by_acyclicity,
                               linear_extensions, leq_matrix, set_partitions,
                               ordered_set_partitions, refines)


# ==========================================================================
# E6 -- the braid arrangement, realised numerically
# ==========================================================================


def realise(osp, n):
    """A point of R^n in the relatively open face named by the ordered set
    partition osp: give every element of block p the coordinate p."""
    x = [0] * n
    for p, B in enumerate(osp):
        for i in B:
            x[i] = p
    return x


def sign_vector(x, n):
    """sigma_{ij}(x) = sign(x_j - x_i) for i < j, over the C(n,2) hyperplanes
    x_i = x_j of the braid arrangement.  Read off the coordinates -- no
    combinatorics."""
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            d = x[j] - x[i]
            out.append(0 if d == 0 else (1 if d > 0 else -1))
    return tuple(out)


def tits(u, v):
    """the Tits product on sign vectors: keep u where it is nonzero, else v"""
    return tuple(a if a != 0 else b for a, b in zip(u, v))


def osp_product(x, y):
    """the repo's product: non-empty B_p n C_q in lexicographic (p,q) order"""
    out = []
    for B in x:
        for C in y:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


def hyperplane_index(n):
    idx = {}
    k = 0
    for i in range(n):
        for j in range(i + 1, n):
            idx[(i, j)] = k
            k += 1
    return idx


def check_E6(n):
    """Is Brown's sign-condition subsemigroup G literally F(P)?  And is the
    Tits product on sign vectors the repo's product?"""
    all_osp = list(ordered_set_partitions(n))
    hidx = hyperplane_index(n)
    sv = {}
    for osp in all_osp:
        sv[osp] = sign_vector(realise(osp, n), n)
    # faithfulness of the encoding: distinct faces <-> distinct sign vectors
    faithful = len(set(sv.values())) == len(all_osp)

    bad_set = bad_prod = bad_cham = 0
    for rel in iso_classes(n):
        # Brown's J and the U-side sign: for (i,j) in rel with i<j as labels,
        # U is x_i < x_j, so the U-side of hyperplane (i,j) is sigma = +1.
        # (Every poset here is naturally labelled, so i < j numerically.)
        J = []
        for (i, j) in rel:
            a, b = (i, j) if i < j else (j, i)
            want = 1 if (i, j) == (a, b) else -1
            J.append((hidx[(a, b)], want))
        G = set()
        for osp in all_osp:
            s = sv[osp]
            if all(s[k] == 0 or s[k] == want for (k, want) in J):
                G.add(osp)
        FP = set(F_of_P(rel, n))
        if G != FP:
            bad_set += 1
        # chambers of G (no zero coordinate) vs linear extensions
        cham = [o for o in G if all(len(B) == 1 for B in o)]
        if len(cham) != len(linear_extensions(rel, n)):
            bad_cham += 1
        # Tits product on sign vectors == repo product, on all pairs from G
        Gl = sorted(G)
        for x in Gl:
            for y in Gl:
                if sv[osp_product(x, y)] != tits(sv[x], sv[y]):
                    bad_prod += 1
                    break
            else:
                continue
            break
    return faithful, len(all_osp), bad_set, bad_prod, bad_cham


# ==========================================================================
# M_0 -- the closed form AS THE DOCUMENT STATES IT, over all flats
# ==========================================================================


def check_M0(n):
    """Brown's (10) at the discrete flat: the multiplicities must sum to
    |D| = |L(P)|.  Run the sum with the DOCUMENT's rule (antichain blocks
    only) and with the INSTRUMENT's rule (antichain blocks AND acyclic)."""
    allparts = [tuple(sorted((frozenset(b) for b in part),
                             key=lambda s: sorted(s)))
                for part in set_partitions(range(n))]
    doc_bad = 0
    code_bad = 0
    extra_total = 0
    witness = None
    for rel in iso_classes(n):
        le = leq_matrix(rel, n)
        ac = AC_by_acyclicity(rel, n)
        e = len(linear_extensions(rel, n))
        doc_sum = 0
        code_sum = 0
        extra = []
        for X in allparts:
            anti = all(not (le[i][j] or le[j][i])
                       for B in X for i in B for j in B if i != j)
            if not anti:
                continue
            m = 1
            for B in X:
                m *= factorial(len(B) - 1)
            doc_sum += m
            if X in ac:
                code_sum += m
            else:
                extra.append((X, m))
        extra_total += len(extra)
        if doc_sum != e:
            doc_bad += 1
            if witness is None:
                witness = (rel, e, doc_sum, code_sum, extra)
        if code_sum != e:
            code_bad += 1
    return doc_bad, code_bad, extra_total, witness, len(list(iso_classes(n)))


# ==========================================================================
# E8 -- Bjorner's greedoid band on the poset shelling antimatroid
# ==========================================================================


def feasible_words(rel, n):
    """the poset shelling antimatroid: words of distinct elements each of whose
    prefixes is an order ideal (down-set) of P.  All lengths 0..n."""
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
    out = []

    def rec(w, used):
        out.append(tuple(w))
        for x in range(n):
            if x in used:
                continue
            if below[x] <= used:
                rec(w + [x], used | {x})

    rec([], frozenset())
    return out


def greedoid_product(u, v):
    """Bjorner's greedy product for an antimatroid: u followed by the letters
    of v that are still addable.  For a shelling antimatroid a letter is
    addable exactly when everything below it is already present, and the
    result is again feasible."""
    return u + tuple(x for x in v if x not in u)


def phi(w, n):
    """the natural map from a feasible word to a move of F(P):
    ({w_1}, ..., {w_k}, rest)   -- the last block dropped when empty"""
    rest = frozenset(set(range(n)) - set(w))
    blocks = [frozenset([x]) for x in w]
    if rest:
        blocks.append(rest)
    return tuple(blocks)


def support(part):
    return tuple(sorted(part, key=lambda s: sorted(s)))


def check_E8(n):
    rows = []
    for rel in iso_classes(n):
        FW = feasible_words(rel, n)
        FP = set(F_of_P(rel, n))
        img = set(phi(w, n) for w in FW)

        subset = img <= FP
        proper = img < FP
        injective = len(img) == len(FW)
        # is the greedoid band's element set literally inside F(P)?
        band_bigger = len(FW) > len(FP)
        # is the image closed under the repo's product?
        closed = all(osp_product(x, y) in img for x in img for y in img)
        # does phi intertwine the two products?
        hom = all(phi(greedoid_product(u, v), n) == osp_product(phi(u, n), phi(v, n))
                  for u in FW for v in FW)
        supp_img = set(support(m) for m in img)
        supp_band = set(frozenset(w) for w in FW)
        rows.append(dict(rel=rel, nFW=len(FW), nFP=len(FP), nimg=len(img),
                         subset=subset, proper=proper, injective=injective,
                         band_bigger=band_bigger, closed=closed, hom=hom,
                         nsupp_img=len(supp_img), nsupp_band=len(supp_band),
                         nAC=len(AC_by_acyclicity(rel, n))))
    return rows


# ==========================================================================


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("mg-d673 AUDIT INSTRUMENT 3 -- E6, M_0 AND E8: the three things the")
    print("target's own pre-filed audit ranks 1-3 as UNMEASURED.")
    print("=" * 78)
    print()

    print("-" * 78)
    print("E6  Brown's G = { F : sigma_i(F) >= 0, i in J } vs the repo's F(P),")
    print("    with sign vectors READ OFF A NUMERIC REALISATION of the braid")
    print("    arrangement (not defined combinatorially from the block order).")
    print("-" * 78)
    print("%3s %10s %10s %14s %14s %14s"
          % ("n", "faces", "encoding", "G == F(P)", "Tits == repo", "chambers==e(P)"))
    for n in range(2, min(nmax, 5) + 1):
        faithful, nf, bs, bp, bc = check_E6(n)
        print("%3d %10d %10s %14s %14s %14s"
              % (n, nf, "faithful" if faithful else "*** NOT ***",
                 "%d bad" % bs, "%d bad" % bp, "%d bad" % bc))
    print()

    print("-" * 78)
    print("M_0  Brown's total-multiplicity identity, run with the DOCUMENT's")
    print("     stated rule (blocks are antichains) and with the INSTRUMENT's")
    print("     docstring rule (blocks are antichains AND the quotient is")
    print("     acyclic).  They differ; only one of them satisfies Brown.")
    print("-" * 78)
    print("%3s %8s %26s %26s %10s"
          % ("n", "classes", "doc rule: sum m != |L(P)|",
             "code rule: sum m != |L(P)|", "extra flats"))
    for n in range(2, min(nmax, 6) + 1):
        db, cb, ex, wit, nc = check_M0(n)
        print("%3d %8d %26s %26s %10d"
              % (n, nc, "%d of %d posets" % (db, nc),
                 "%d of %d posets" % (cb, nc), ex))
        if wit and n == 4:
            rel, e, ds, cs, extra = wit
            names = ",".join("%s<%s" % (chr(97 + i), chr(97 + j))
                             for i, j in sorted(rel))
            print("      first witness at n=4: P = [%s], |L(P)| = %d" % (names, e))
            print("        document's rule gives sum m = %d  (Brown's (10) says %d)"
                  % (ds, e))
            print("        instrument's rule gives sum m = %d  OK" % cs)
            for X, m in extra:
                print("        spurious level: %s with m = %d "
                      "(all blocks antichains, quotient NOT acyclic)"
                      % ("|".join("".join(chr(97 + x) for x in sorted(B))
                                  for B in X), m))
    print()

    print("-" * 78)
    print("E8  Bjorner's greedoid band on the poset shelling antimatroid vs")
    print("    F(P).  The document says: 'A proper submonoid of ours'.")
    print("-" * 78)
    for n in range(2, min(nmax, 5) + 1):
        rows = check_E8(n)
        nsub = sum(r['subset'] for r in rows)
        nprop = sum(r['proper'] for r in rows)
        ninj = sum(r['injective'] for r in rows)
        nbig = sum(r['band_bigger'] for r in rows)
        ncl = sum(r['closed'] for r in rows)
        nhom = sum(r['hom'] for r in rows)
        print("  n=%d, %d classes:" % (n, len(rows)))
        print("     the band's IMAGE under w -> ({w_1}..{w_k},rest) is in F(P): %d of %d"
              % (nsub, len(rows)))
        print("     the BAND ITSELF is strictly LARGER than all of F(P): %d of %d"
              % (nbig, len(rows)))
        print("     word -> move map is INJECTIVE              : %d of %d"
              % (ninj, len(rows)))
        print("     its IMAGE is closed under the repo product : %d of %d"
              % (ncl, len(rows)))
        print("     the map is a monoid HOMOMORPHISM           : %d of %d"
              % (nhom, len(rows)))
        print("     its IMAGE is a PROPER submonoid of F(P)    : %d of %d"
              % (nprop, len(rows)))
    print()
    print("  The antichain, in detail (the case the document names):")
    print("%3s %10s %10s %10s %10s %14s %12s"
          % ("n", "|band|", "|F(P)|", "|image|", "2^n", "band supports",
             "image supports"))
    for n in range(2, min(nmax, 5) + 1):
        anti = frozenset()
        FW = feasible_words(anti, n)
        FP = set(F_of_P(anti, n))
        img = set(phi(w, n) for w in FW)
        supp_band = set(frozenset(w) for w in FW)
        supp_img = set(support(m) for m in img)
        print("%3d %10d %10d %10d %10d %14d %12d"
              % (n, len(FW), len(FP), len(img), 2 ** n, len(supp_band),
                 len(supp_img)))
    print()
    print("  |F(antichain)| is the ordered Bell number; |band| at the antichain")
    print("  is sum_k n!/(n-k)! = the free left regular band on n generators.")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
