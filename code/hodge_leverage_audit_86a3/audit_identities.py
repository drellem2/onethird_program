"""Independent rebuild of Theorem D (down-up walk) and Theorem N1 (twisted
relative top Laplacian = signed incidence Gram matrix).

Route notes.  The relative top Laplacian is built here as  d^T d  where d is the
(interior ridge) x (facet) matrix with entries (-1)^t at the ridge obtained by
deleting the t-th ideal of the chain.  An "interior" ridge is one lying in
exactly two facets -- computed by counting, not by the free-ridge/forbidden-
generator bijection of mg-276d Lemma 3(b).  E = diag(sgn w) uses the sign of the
linear extension read as a permutation, computed by inversion count.

Reported separately, because the audit has to distinguish them:
  N1a   E L^rel E == Delta_AT                (this IS mg-276d's bridge)
  N1b   Delta_AT == N^T N                    (the incidence factorisation)
  N1c   d_rel E == N up to a sign per row    (the actual new clause of N1)
"""

import sys
from fractions import Fraction

from audit_core import (posets_upto_iso, linexts, proper_ideals_of, facet_of,
                        at_graph, at_laplacian)


def sgn(w):
    inv = 0
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if w[i] > w[j]:
                inv += 1
    return -1 if inv % 2 else 1


def ridge_data(P):
    """facets (as chains of ideals), and ridge -> list of facet indices."""
    les = linexts(P)
    facets = [facet_of(P, w) for w in les]
    rf = {}
    for i, f in enumerate(facets):
        for t in range(len(f)):
            r = f[:t] + f[t + 1:]
            rf.setdefault(r, []).append((i, t))
    return les, facets, rf


def down_up(P):
    """The standard down-up walk on facets, from ridge incidence only."""
    les, facets, rf = ridge_data(P)
    m = len(facets)
    nr = P.n - 1
    M = [[Fraction(0)] * m for _ in range(m)]
    for i, f in enumerate(facets):
        for t in range(len(f)):
            r = f[:t] + f[t + 1:]
            cof = rf[r]
            for (j, _) in cof:
                M[i][j] += Fraction(1, nr * len(cof))
    return les, M


def rel_top_laplacian(P):
    """d^T d over interior ridges only, with the standard simplicial signs."""
    les, facets, rf = ridge_data(P)
    m = len(facets)
    L = [[0] * m for _ in range(m)]
    for r, cof in rf.items():
        if len(cof) != 2:
            continue                      # boundary ridge: killed in the quotient
        (i, ti), (j, tj) = cof
        si = -1 if ti % 2 else 1
        sj = -1 if tj % 2 else 1
        L[i][i] += 1
        L[j][j] += 1
        L[i][j] += si * sj
        L[j][i] += si * sj
    return les, facets, rf, L


def check(n, verbose=False):
    res = dict(D=0, N1a=0, N1b=0, N1c=0, tot=0, nondeg=0,
               interior_eq_deg=0)
    for P in posets_upto_iso(n):
        res["tot"] += 1
        les, Ldu = down_up(P)
        _, Delta = at_laplacian(P)
        m = len(les)
        nr = P.n - 1 if P.n > 1 else 1
        okD = all(
            (Fraction(1) if i == j else Fraction(0)) - Ldu[i][j]
            == Delta[i][j] / (2 * nr)
            for i in range(m) for j in range(m)) if P.n > 1 else True
        res["D"] += bool(okD)

        les2, facets, rf, Lrel = rel_top_laplacian(P)
        E = [sgn(w) for w in les2]
        okA = all(E[i] * Lrel[i][j] * E[j] == Delta[i][j]
                  for i in range(m) for j in range(m))
        res["N1a"] += bool(okA)

        # N^T N from the AT graph alone
        _, adj = at_graph(P)
        edges = sorted({(min(i, j), max(i, j)) for i in range(m) for j in adj[i]})
        NtN = [[0] * m for _ in range(m)]
        for (a, b) in edges:
            NtN[a][a] += 1
            NtN[b][b] += 1
            NtN[a][b] -= 1
            NtN[b][a] -= 1
        okB = all(NtN[i][j] == Delta[i][j] for i in range(m) for j in range(m))
        res["N1b"] += bool(okB)

        # N1c: rows of d_rel E, one row per interior ridge, must be
        # +-(e_a - e_b) for the AT edge {a,b} that ridge carries.
        eset = set(edges)
        okC = True
        seen = set()
        for r, cof in rf.items():
            if len(cof) != 2:
                continue
            (i, ti), (j, tj) = cof
            si = (-1 if ti % 2 else 1) * E[i]
            sj = (-1 if tj % 2 else 1) * E[j]
            if si * sj != -1:
                okC = False
                break
            key = (min(i, j), max(i, j))
            if key not in eset:
                okC = False
                break
            seen.add(key)
        if seen != eset:
            okC = False
        res["N1c"] += bool(okC)

        # is #interior ridges at a facet == its AT degree?
        deg_ok = True
        for i in range(m):
            cnt = 0
            for t in range(len(facets[i])):
                if len(rf[facets[i][:t] + facets[i][t + 1:]]) == 2:
                    cnt += 1
            if cnt != len(adj[i]):
                deg_ok = False
        res["interior_eq_deg"] += bool(deg_ok)
        if m >= 2:
            res["nondeg"] += 1
        if verbose and not (okD and okA and okB and okC):
            print("   FAIL", P.tag(), okD, okA, okB, okC)
    return res


if __name__ == "__main__":
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("AUDIT: Theorem D and Theorem N1, independent rebuild")
    print("=" * 78)
    print("  N1a  E L^rel E == Delta_AT     (mg-276d's bridge, re-derived here)")
    print("  N1b  Delta_AT  == N^T N        (the incidence factorisation)")
    print("  N1c  d_rel E   == N up to a sign per row  (N1's own new clause)")
    print()
    tot = dict(D=0, N1a=0, N1b=0, N1c=0, tot=0, nondeg=0, interior_eq_deg=0)
    for n in range(1, hi + 1):
        r = check(n)
        for k in tot:
            tot[k] += r[k]
        print("n=%d posets=%3d  D=%3d/%3d  N1a=%3d  N1b=%3d  N1c=%3d  "
              "#interior==deg on %3d  (|L|>=2: %3d)"
              % (n, r["tot"], r["D"], r["tot"], r["N1a"], r["N1b"], r["N1c"],
                 r["interior_eq_deg"], r["nondeg"]))
    print()
    print("TOTAL over %d posets: D=%d  N1a=%d  N1b=%d  N1c=%d"
          % (tot["tot"], tot["D"], tot["N1a"], tot["N1b"], tot["N1c"]))
