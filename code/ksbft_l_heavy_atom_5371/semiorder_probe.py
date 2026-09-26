"""EMPIRICAL: semiorders S(n,k): x_i < x_j iff j - i >= k (width k).  Globally unbalanced?
For the middle element x, D/U from delta_x, and compare the Thm 2.6 atom P(A<x<B)
with q(x) = max_k P(f(x)=k) and with P(f(x)=|D|+1)."""
import sys
from fractions import Fraction
from lib import *

def semiorder(n, k):
    rel = {(i, j) for i in range(n) for j in range(n) if j - i >= k}
    return Poset(n, closure(n, rel))

def pair_probs(P):
    # P(i before j) for all incomparable pairs via placements-free DP: count ext with i before j
    tot = P.total()
    n = P.n
    out = {}
    for i in range(n):
        pl = P.placements(i)
        for j in range(n):
            if j == i or P.comparable(i, j): continue
            c = sum(w for S, w in pl if (S >> j) & 1)  # j before i
            out[(j, i)] = Fraction(c, tot)
    return out

for (n, k) in [(int(a), int(b)) for a, b in (s.split(',') for s in sys.argv[1:])]:
    P = semiorder(n, k)
    tot = P.total()
    pp = pair_probs(P)
    delta = min(min(v, 1 - v) for v in pp.values())
    x = n // 2
    pl = P.placements(x)
    dx = min(min(pp[(y, x)], 1 - pp[(y, x)]) for y in range(n) if y != x and not P.comparable(x, y))
    D = [y for y in range(n) if y != x and (y in [i for i in range(n) if (P.below[x] >> i) & 1] or (not P.comparable(x, y) and pp[(y, x)] > Fraction(1, 2)))]
    Dm = sum(1 << y for y in D)
    fx = [0]*(n+1)
    for S, w in pl: fx[popcount(S)] += w
    q = Fraction(max(fx), tot)
    atom = Fraction(sum(w for S, w in pl if S == Dm), tot)
    fD = Fraction(fx[len(D)], tot)
    print(f"n={n} k={k} width={k} delta(P)={float(delta):.4f} delta_x={float(dx):.4f} |D|={len(D)} "
          f"P(A<x<B)={float(atom):.3e} P(f(x)=|D|+1)={float(fD):.4f} q(x)={float(q):.4f}")
