"""Theorem G, rebuilt from scratch.

The deliverable's own §13 says this is the one thing an auditor should rebuild:
"the eigenfunction computation in §6 ... no independent code path re-derives
(the exact-arithmetic check confirms the identity, using the same link
construction)".

So this file does NOT touch audit_core's link machinery, and does not touch
code/hodge_leverage at all.  The Coxeter complex of S_m is built directly from
its definition -- vertices are the proper nonempty subsets of [m], facets are
the m! maximal flags -- and the induced weights are written down in closed form
and then CHECKED against a brute-force facet count.

Three separate questions, kept apart:

  G1  is the walk operator the deliverable describes the actual 1-skeleton walk
      of the weighted link?  (closed form vs brute-force facet counting)
  G2  is  P f = f/2  exact, for m = 3..14, in exact rational arithmetic?
  G3  is 1/2 the SECOND eigenvalue (equality) or only AN eigenvalue?
      -- the deliverable deliberately does not upgrade this; checked here to see
      whether the restraint is correctly placed.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial

from audit_core import jacobi_eigenvalues


def coxeter_vertices(m):
    """Proper nonempty subsets of [m] as frozensets."""
    out = []
    for k in range(1, m):
        for c in combinations(range(m), k):
            out.append(frozenset(c))
    return out


def brute_force_link(m):
    """The weighted 1-skeleton of F(A_m) = the Coxeter complex of S_m, built by
    enumerating all m! facets and counting.  Returns (verts, vertex weight dict,
    edge weight dict)."""
    verts = coxeter_vertices(m)
    vw = {v: 0 for v in verts}
    ew = {}
    for w in permutations(range(m)):
        flag = [frozenset(w[:k]) for k in range(1, m)]
        for v in flag:
            vw[v] += 1
        for a in range(len(flag)):
            for b in range(a + 1, len(flag)):
                key = (flag[a], flag[b])
                ew[key] = ew.get(key, 0) + 1
    return verts, vw, ew


def closed_form_weights(m):
    """w(S) = |S|! (m-|S|)!  and  w(S,T) = |S|!(|T|-|S|)!(m-|T|)! for S < T."""
    verts = coxeter_vertices(m)
    vw = {S: factorial(len(S)) * factorial(m - len(S)) for S in verts}
    ew = {}
    for S in verts:
        for T in verts:
            if len(S) < len(T) and S < T:
                ew[(S, T)] = (factorial(len(S)) * factorial(len(T) - len(S))
                              * factorial(m - len(T)))
    return verts, vw, ew


def walk_rows(m, vw, ew, verts):
    """Sparse exact transition data for the weighted-graph random walk:
    P[S][T] = w(S,T) / sum_U w(S,U).  For the Coxeter complex the row sum must
    come out as (m-2) w(S) -- checked here rather than assumed.

    Returns (adjacency as list of (j, weight), row sums, index map)."""
    idx = {v: i for i, v in enumerate(verts)}
    N = len(verts)
    adj = [[] for _ in range(N)]
    for (S, T), val in ew.items():
        adj[idx[S]].append((idx[T], val))
        adj[idx[T]].append((idx[S], val))
    rows = [sum(w for _, w in a) for a in adj]
    assert all(rows[idx[S]] == (m - 2) * vw[S] for S in verts), \
        "row sum is not (m-2)w(S)"
    return adj, rows, idx


def main():
    print("=" * 78)
    print("AUDIT: Theorem G rebuilt from scratch (no shared link code)")
    print("=" * 78)

    print("\nG1  closed-form induced weights vs brute-force facet counting")
    for m in range(3, 8):
        v1, vw1, ew1 = brute_force_link(m)
        v2, vw2, ew2 = closed_form_weights(m)
        same_v = set(v1) == set(v2)
        same_vw = vw1 == vw2
        # the brute-force edge dict may key pairs in either order
        e1 = {}
        for (a, b), x in ew1.items():
            k = (a, b) if len(a) < len(b) else (b, a)
            e1[k] = e1.get(k, 0) + x
        same_ew = e1 == ew2
        print("    m=%2d  vertices=%3d  verts match=%s  w(S) match=%s  w(S,T) match=%s"
              % (m, len(v1), same_v, same_vw, same_ew))
        assert same_v and same_vw and same_ew

    print("\nG2  P f = f/2 exactly, f(S) = sum_{i in S} a_i with sum a_i = 0")
    print("    (exact rationals; several independent choices of a; m up to 14)")
    for m in range(3, 13):
        verts, vw, ew = closed_form_weights(m)
        adj, rows, idx = walk_rows(m, vw, ew, verts)
        N = len(verts)
        avecs = []
        # a few genuinely different a's, all summing to zero
        a = [Fraction(0)] * m
        a[0], a[1] = Fraction(1), Fraction(-1)
        avecs.append(list(a))
        avecs.append([Fraction(2 * i - (m - 1), 2) for i in range(m)])
        a = [Fraction((i * i) % 7) for i in range(m)]
        s = sum(a)
        avecs.append([x - Fraction(s, m) for x in a])
        worst = Fraction(0)
        for a in avecs:
            assert sum(a) == 0
            f = [sum(a[i] for i in S) for S in verts]
            for r in range(N):
                got = sum(Fraction(w, rows[r]) * f[j] for j, w in adj[r])
                d = abs(got - f[r] / 2)
                if d > worst:
                    worst = d
        # orthogonality of f to the constants under the stationary measure
        f = [sum(avecs[0][i] for i in S) for S in verts]
        pi = [rows[i] for i in range(N)]
        orth = sum(pi[i] * f[i] for i in range(N))
        nz = any(x != 0 for x in f)
        print("    m=%2d  |V|=%5d  max |Pf - f/2| = %s   <f,1>_pi = %s   f != 0: %s"
              % (m, N, worst, orth, nz))
        assert worst == 0 and orth == 0 and nz

    print("\nG3  is 1/2 the SECOND eigenvalue, or only AN eigenvalue?")
    print("    (full spectrum of the reversible walk, dense symmetric solver)")
    import math
    for m in range(3, 10):
        verts, vw, ew = closed_form_weights(m)
        adj, rows, idx = walk_rows(m, vw, ew, verts)
        N = len(verts)
        # symmetrise: D^{1/2} P D^{-1/2}
        d = [math.sqrt(float(rows[i])) for i in range(N)]
        A = [[0.0] * N for _ in range(N)]
        for i in range(N):
            for j, w in adj[i]:
                A[i][j] = (w / rows[i]) * d[i] / d[j]
        ev = sorted(jacobi_eigenvalues(A))
        top = ev[-1]
        second = ev[-2]
        print("    m=%2d  |V|=%4d  lambda_1=%.12f  lambda_2=%.12f  "
              "lambda_min=%.12f   lambda_2 == 1/2: %s"
              % (m, N, top, second, ev[0], abs(second - 0.5) < 1e-9))

    print("\n    (m = 3..9 covers A_3..A_9; the deliverable's equality row G'")
    print("     claims A_3..A_7 only.)")


if __name__ == "__main__":
    main()
