"""Proposition 5, verified against the ACTUAL stationary vector of the transition
matrix under the uniform-move weight -- solved exactly over Q, not assumed.

  Prop 5:  pi(x<y) = q(x<y) / (q(x<y) + q(y<x)),
where q is the mass of moves that separate the pair in each direction.
"""

from fractions import Fraction

from kernel import Lattice, act, linear_extensions, moves_of, posets_up_to_iso

TOT = BAD = 0
POSETS = 0
prev = None
for n in range(1, 6):
    prev = posets_up_to_iso(n, prev)
    if n < 3:
        continue
    lat = Lattice(n)
    for P in prev:
        les = linear_extensions(P)
        N = len(les)
        if N > 24 or not P.incomparable():
            continue
        idx = {w: i for i, w in enumerate(les)}
        mvs = moves_of(P, lat)
        M = [[Fraction(0)] * N for _ in range(N)]
        for mv in mvs:
            for w in les:
                M[idx[w]][idx[act(mv, w)]] += Fraction(1, len(mvs))
        # solve pi M = pi, sum pi = 1, exactly
        A = [[M[i][j] - (1 if i == j else 0) for i in range(N)] for j in range(N)]
        A.append([Fraction(1)] * N)
        b = [Fraction(0)] * N + [Fraction(1)]
        rows = [A[i] + [b[i]] for i in range(N + 1)]
        piv = 0
        where = []
        for c in range(N):
            p = None
            for r in range(piv, len(rows)):
                if rows[r][c] != 0:
                    p = r
                    break
            if p is None:
                continue
            rows[piv], rows[p] = rows[p], rows[piv]
            inv = rows[piv][c]
            rows[piv] = [v / inv for v in rows[piv]]
            for r in range(len(rows)):
                if r != piv and rows[r][c] != 0:
                    f = rows[r][c]
                    rows[r] = [a - f * bb for a, bb in zip(rows[r], rows[piv])]
            where.append(c)
            piv += 1
        pi = [Fraction(0)] * N
        for i, c in enumerate(where):
            pi[c] = rows[i][N]
        assert sum(pi) == 1, "stationary vector does not sum to 1"
        assert all(sum(pi[i] * M[i][j] for i in range(N)) == pi[j] for j in range(N)), \
            "not stationary"
        POSETS += 1
        for (x, y) in P.incomparable():
            qxy = qyx = Fraction(0)
            for mv in mvs:
                ix = iy = -1
                for k, B in enumerate(mv):
                    if (B >> x) & 1:
                        ix = k
                    if (B >> y) & 1:
                        iy = k
                if ix < iy:
                    qxy += Fraction(1, len(mvs))
                elif iy < ix:
                    qyx += Fraction(1, len(mvs))
            pred = qxy / (qxy + qyx)
            actual = sum(pi[idx[w]] for w in les if w.index(x) < w.index(y))
            TOT += 1
            if pred != actual:
                BAD += 1
                print("  MISMATCH %s pair (%d,%d): predicted %s, actual %s"
                      % (P.covers_string(), x, y, pred, actual))
print("Proposition 5 against the exact stationary vector: %d posets, %d incomparable"
      " pairs, %d mismatches" % (POSETS, TOT, BAD))
print("(the document reports control C8 as '0 bad of 52 pairs'; the pair COUNT differs")
print(" only because I ran every poset with e(P) <= 24 at n <= 5)")
