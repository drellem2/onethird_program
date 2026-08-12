"""r1 -- THE CEILING.  How large can alpha_n possibly be?

The note (:234) asks for  E Var(f|C_o) + E Var(f|C_e) >= alpha_n Var(f)  and never says what
alpha_n has to be.  Before asking whether that is provable, this arm asks what the largest
TRUE value is, because no proof can exceed it.

Two facts, both proved in the README (S2) and both re-derived here by exhibited rational
witnesses rather than by an eigensolver:

  (C0)  alpha(P) > 0 for every P            -- so the inequality is TRUE for free
  (C1)  alpha(P) <= 1 for every P with |L(P)| >= 2, ATTAINED

alpha(P) := lam_min of M = 2I - Pi_o - Pi_e restricted to 1-perp, i.e. the largest constant
the note's inequality can carry at this P.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True


def connected_by_fibers(LEs, n):
    """Is the graph on L(P) with edges {same odd fiber} u {same even fiber} connected?

    alpha(P) > 0  <=>  the only f with Pi_o f = Pi_e f = f is constant  <=>  this graph is
    connected.  A pure combinatorial check: no eigenvalue, no float.
    """
    parent = list(range(len(LEs)))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for groups in (L.blocks_o(n), L.blocks_e(n)):
        for _, idxs in L.fiber_map(LEs, groups).items():
            for k in idxs[1:]:
                union(idxs[0], k)
    return len({find(k) for k in range(len(LEs))}) == 1


def ceiling_witness(LEs, n):
    """An EXHIBITED rational f, orthogonal to constants, with R_M(f) <= 1 -- or the exact
    degenerate case.

    Returns (kind, value) where value is an exact Fraction upper bound on alpha(P).
      'odd-fiber'  : f = 1_{one odd fiber}, which satisfies Pi_o f = f, so
                     R_M(f) = 1 - ||Pi_e f||^2/||f||^2 <= 1.
      'C_o-trivial': C_o is constant on L(P); then C_e separates L(P) completely, Pi_e = I,
                     Pi_o = projection onto constants, and M|_{1perp} = I exactly.
    """
    N = len(LEs)
    fo = L.fiber_map(LEs, L.blocks_o(n))
    for _, idxs in fo.items():
        if 0 < len(idxs) < N:
            f = [Fraction(0)] * N
            for k in idxs:
                f[k] = Fraction(1)
            return "odd-fiber", L.rayleigh_M(f, LEs, n)
    # C_o is constant.  Then every even fiber must be a singleton; check it, do not assume it.
    fe = L.fiber_map(LEs, L.blocks_e(n))
    if all(len(v) == 1 for v in fe.values()):
        return "C_o-trivial", Fraction(1)
    return "UNCOVERED", None


# --------------------------------------------------------------------------------------
L.banner("r1.1  (C0)  alpha(P) > 0 for every poset  --  exact, combinatorial")

pops = []
for n in (2, 3, 4, 5):
    pops.append((n, "exhaustive", list(L.all_posets(n))))
pops.append((6, "sampled(150,seed=409)", L.sample_posets(6, 150, 409)))

tot = disc = 0
for n, label, posets in pops:
    bad = 0
    cnt = 0
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            disc += 1
            continue
        cnt += 1
        if not connected_by_fibers(LEs, n):
            bad += 1
    tot += cnt
    ok &= L.verdict(bad == 0, f"n={n} {label}: fiber graph connected at all {cnt} posets")
print(f"  ({tot} posets with |L(P)| >= 2; {disc} chains skipped -- Var(f) = 0 there)")

# --------------------------------------------------------------------------------------
L.banner("r1.2  (C1)  alpha(P) <= 1 for every poset  --  exhibited rational witness")

worst = Fraction(0)
worst_at = None
kinds = {}
uncovered = 0
for n, label, posets in pops:
    mx = Fraction(0)
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        kind, val = ceiling_witness(LEs, n)
        kinds[kind] = kinds.get(kind, 0) + 1
        if val is None:
            uncovered += 1
            continue
        if val > mx:
            mx = val
        if val > worst:
            worst, worst_at = val, (n, sorted(lt))
    ok &= L.verdict(mx <= 1, f"n={n} {label}: max exhibited R_M = {mx} <= 1")
ok &= L.verdict(uncovered == 0, "every poset is covered by one of the two witness kinds")
print(f"  witness kinds: {kinds}")
print(f"  largest exhibited bound anywhere: {worst}  at n={worst_at[0]}")

# --------------------------------------------------------------------------------------
L.banner("r1.3  the ceiling is ATTAINED, and not only at small n")

for n in (4, 6, 8, 10, 12):
    Z = L.two_block_ordinal_sum(n)
    LEs = L.linear_extensions(n, Z)
    fo = L.fiber_map(LEs, L.blocks_o(n))
    fe = L.fiber_map(LEs, L.blocks_e(n))
    c_o_trivial = (len(fo) == 1)
    c_e_separates = all(len(v) == 1 for v in fe.values())
    # M|_{1perp} = 2I - P_const - I = I  =>  alpha = 1 exactly, no eigensolver needed
    ok &= L.verdict(c_o_trivial and c_e_separates,
                    f"Z_{n}: C_o constant AND C_e separates  =>  alpha(Z_{n}) = 1 EXACTLY",
                    f"|L|={len(LEs)}, odd fibers={len(fo)}, even fibers={len(fe)}")

for n in (4, 6, 8):
    Z = L.two_block_ordinal_sum(n)
    LEs = L.linear_extensions(n, Z)
    a = L.alpha_measured(LEs, n)
    ok &= L.verdict(abs(a - 1.0) < 1e-10, f"  ... and Jacobi agrees at Z_{n}", L.frac(a))

# --------------------------------------------------------------------------------------
L.banner("r1.4  the measured alpha never exceeds the exhibited witness")

bad = 0
checked = 0
for n in (3, 4):
    for lt in L.all_posets(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        _, w = ceiling_witness(LEs, n)
        a = L.alpha_measured(LEs, n)
        checked += 1
        if a > float(w) + 1e-9:
            bad += 1
ok &= L.verdict(bad == 0, f"measured alpha <= exhibited bound at all {checked} posets (n<=4)")

L.banner("r1 VERDICT")
print("  alpha(P) is in (0, 1] for EVERY poset, and 1 is attained at every even n tested.")
print("  THE NOTE'S alpha_n CAN NEVER EXCEED 1.  Remember that number.")
sys.exit(0 if ok else 1)
