"""a0 -- the instrument checks itself before it is allowed to check the note.

Nothing here is about compression.tex.  These are the facts lib8bc7 must get right for any
later arm's PASS to mean anything: linear-extension counts against closed forms, the two
position groupings against the note's own prose, the exact PSD test against matrices whose
definiteness is known by hand, the span test against a vector known to be in and one known
to be out, and the BK Dirichlet form against a case small enough to do on paper.
"""

from fractions import Fraction
import math
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, linear_extensions, groups_o,
                     groups_e, swap_positions, incomparable_pairs, linear_stat, variance,
                     expected_cond_variance, bk_energy, psd_exact, in_span,
                     jacobi_eigenvalues, random_poset, transitive_closure, fibers)

ok = True

banner("a0.1  linear-extension counts against closed forms")
for n in range(1, 8):
    anti = frozenset()
    chain = frozenset((i, j) for i in range(n) for j in range(n) if i < j)
    la = len(linear_extensions(n, anti))
    lc = len(linear_extensions(n, chain))
    ok &= verdict(la == math.factorial(n), f"antichain n={n}: |L(P)| = {la} = {n}!")
    ok &= verdict(lc == 1, f"chain    n={n}: |L(P)| = {lc} = 1")

# the "N" poset on 4 elements: a<c, b<c, b<d.  Its linear extensions are enumerable by hand:
# 5 of them (abcd, abdc, badc, bacd, bdac).
N = frozenset(transitive_closure(4, [(0, 2), (1, 2), (1, 3)]))
LN = linear_extensions(4, N)
ok &= verdict(len(LN) == 5, f"N-poset: |L(P)| = {len(LN)} = 5 (hand count)")

banner("a0.2  the two position groupings, against the note's own prose")
# compression.tex:14  C_o(L) = (I_2, I_4, I_6, ...)   -> blocks {x1,x2},{x3,x4},...
# compression.tex:42  edges are tau_1, tau_3, tau_5, ...          (1-indexed positions)
# compression.tex:47  C_e(L) = (I_1, I_3, I_5, ...)   -> {x1},{x2,x3},{x4,x5},...
# compression.tex:51  edges are tau_2, tau_4, tau_6, ...
for n in range(2, 9):
    go, ge = groups_o(n), groups_e(n)
    so = [p + 1 for p in swap_positions(go)]   # back to the note's 1-indexing
    se = [p + 1 for p in swap_positions(ge)]
    flat_o = [p for g in go for p in g]
    flat_e = [p for g in ge for p in g]
    ok &= verdict(flat_o == list(range(n)) and flat_e == list(range(n)),
                  f"n={n}: both groupings partition all {n} positions")
    ok &= verdict(all(i % 2 == 1 for i in so) and all(i % 2 == 0 for i in se),
                  f"n={n}: odd swaps {so}, even swaps {se}")
    ok &= verdict(sorted(so + se) == list(range(1, n)),
                  f"n={n}: the two swap sets are disjoint and cover 1..{n-1}")

banner("a0.3  exact PSD test on matrices whose definiteness is known by hand")
cases = [
    ([[2, 1], [1, 2]], True, "2x2 diagonally dominant"),
    ([[1, 1], [1, 1]], True, "rank-1 PSD"),
    ([[1, 2], [2, 1]], False, "det = -3"),
    ([[0, 1], [1, 0]], False, "zero pivot with nonzero row"),
    ([[0, 0], [0, 1]], True, "zero pivot with zero row"),
    ([[1, 0, 0], [0, 0, 0], [0, 0, -1]], False, "negative last pivot"),
    ([[4, 2, 0], [2, 2, 0], [0, 0, 0]], True, "PSD with a null direction"),
]
for A, want, why in cases:
    got = psd_exact([[Fraction(x) for x in r] for r in A])
    ok &= verdict(got == want, f"psd_exact({why}) = {got}, want {want}")

banner("a0.4  exact span test")
b1 = [Fraction(1), Fraction(1), Fraction(1)]
b2 = [Fraction(1), Fraction(0), Fraction(0)]
ok &= verdict(in_span([b1, b2], [Fraction(3), Fraction(2), Fraction(2)]), "in-span case")
ok &= verdict(not in_span([b1, b2], [Fraction(0), Fraction(1), Fraction(0)]), "out-of-span case")

banner("a0.5  Jacobi eigenvalues against a hand-computable matrix")
ev = jacobi_eigenvalues([[2.0, 1.0], [1.0, 2.0]])
ok &= verdict(abs(ev[0] - 1) < 1e-12 and abs(ev[1] - 3) < 1e-12, f"eigs = {ev}, want [1, 3]")

banner("a0.6  BK Dirichlet form on a case small enough to do on paper")
# n = 2 antichain.  L(P) = {(0,1), (1,0)}, one adjacent position, always legal.
# f = 1{0 <_L 1} takes values 1 and 0.  P_BK is the swap, so (I-P)f = f - (1-f) = 2f - 1,
# and <f, (I-P)f> = E[f(2f-1)] = (1*1 + 0*(-1))/2 = 1/2.  Var(f) = 1/4, so R = 2 = 2/(n-1).
LEs = linear_extensions(2, frozenset())
vals = linear_stat(2, frozenset(), Fraction(0), {(0, 1): Fraction(1)}, LEs)
E = bk_energy(vals, LEs, 2, frozenset())
ok &= verdict(E == Fraction(1, 2), f"E_BK = {E}, want 1/2")
ok &= verdict(variance(vals) == Fraction(1, 4), f"Var = {variance(vals)}, want 1/4")

banner("a0.7  law of total variance: E Var(f|C) <= Var(f), on every poset to n = 4")
bad = 0
rng = random.Random(20260812)
cnt = 0
for n in range(2, 5):
    for lt in gen_posets_exhaustive(n):
        LEs = linear_extensions(n, lt)
        I = incomparable_pairs(n, lt)
        if not I:
            continue
        c = {p: Fraction(rng.randint(-5, 5)) for p in I}
        vals = linear_stat(n, lt, Fraction(0), c, LEs)
        V = variance(vals)
        for g in (groups_o(n), groups_e(n)):
            if expected_cond_variance(vals, LEs, g) > V:
                bad += 1
        cnt += 1
ok &= verdict(bad == 0, f"0 violations over {cnt} posets x 2 compressions")

banner("a0.8  fibers partition L(P)")
bad = 0
for n in range(2, 6):
    for lt in ([random_poset(n, 0.3, rng) for _ in range(40)] if n == 5
               else list(gen_posets_exhaustive(n))):
        LEs = linear_extensions(n, lt)
        for g in (groups_o(n), groups_e(n)):
            fb = fibers(LEs, g)
            if sum(len(v) for v in fb.values()) != len(LEs):
                bad += 1
            if len(set(L for v in fb.values() for L in v)) != len(LEs):
                bad += 1
ok &= verdict(bad == 0, "every fiber decomposition is a partition")

print()
print("a0 SELFTEST:", "ALL PASS" if ok else "FAILURES PRESENT")
sys.exit(0 if ok else 1)
