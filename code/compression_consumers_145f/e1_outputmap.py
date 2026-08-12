"""e1 -- THE OUTPUT MAP.  What the cube-foliation energy identity actually emits.

The ticket's test 1 is "REACHABLE BY THE MACHINERY", and that is a matter of taste until the
machinery's output is pinned.  This arm pins it, exactly.

    THEOREM (e1.1, verified here on exact rationals).  For every finite poset P and every
    pair-orientation linear statistic f(L) = a + sum_{x||y} c_xy 1{x <_L y},

        E Var(f | C_o) = (1/4) sum_{x||y} c_xy^2 * A^o_xy
        E Var(f | C_e) = (1/4) sum_{x||y} c_xy^2 * A^e_xy
        E_BK(f)        = (1/(2(n-1))) sum_{x||y} c_xy^2 * (A^o_xy + A^e_xy)

    where A^o_xy = Pr[{x,y} is a 2-block of C_o] and A^e_xy = Pr[{x,y} is a 2-block of C_e],
    so A^o_xy + A^e_xy = Pr[x and y occupy adjacent positions].

    COROLLARY.  The identity's ENTIRE measure-dependent output is the pair-adjacency
    probability vector (A^o, A^e).  Nothing else about the linear-extension measure enters.

Two blindnesses follow immediately and are measured here rather than asserted:

    (e1.2) SIGN-BLIND.  The output depends on c only through c^2.  Flip the sign of any
           coefficient and the identity returns the same numbers while Var(f) moves.
    (e1.3) LEVEL-BLIND.  The output is unchanged by f -> f + a.  No first moment of any
           statistic is emitted.

Those two are the filter the enumeration in the README runs every candidate target through.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib145f as L  # noqa: E402

ok = True

POP = ([(3, p) for p in L.all_posets(3)]
       + [(4, p) for p in L.all_posets(4)]
       + [(5, p) for p in L.sample_posets(5, 60, 7)]
       + [(6, p) for p in L.sample_posets(6, 30, 13)])


def coefficient_vectors(inc, seed):
    """Five structurally different coefficient vectors per poset, including negatives."""
    if not inc:
        return []
    out = [{inc[0]: Fraction(1)},                              # a pair indicator
           {p: Fraction(1) for p in inc},                      # inv_e-shaped (all ones)
           {p: Fraction(1 + ((i * seed) % 5)) for i, p in enumerate(inc)},
           {p: Fraction((-1) ** i * (1 + (i % 3))) for i, p in enumerate(inc)},
           {p: Fraction((i * seed) % 7 - 3, 2) for i, p in enumerate(inc)}]
    return out


# ---------------------------------------------------------------------------------------
L.banner("e1.1  THE OUTPUT MAP: E Var(f|C_o) = (1/4) sum c^2 A^o,  and E_BK from it")
tot = 0
fails_o = fails_e = fails_bk = 0
per_n = {}
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    inc = L.incomparable_pairs(n, lt)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    for c in coefficient_vectors(inc, n + 3):
        f = L.pair_orientation_stat(LEs, c)
        pred_o = sum(Fraction(c.get(p, 0)) ** 2 * A_o[p] for p in A_o) / 4
        pred_e = sum(Fraction(c.get(p, 0)) ** 2 * A_e[p] for p in A_e) / 4
        got_o = L.e_cond_var(f, LEs, L.odd_blocks(n))
        got_e = L.e_cond_var(f, LEs, L.even_blocks(n))
        got_bk = L.bk_energy(f, LEs, n, lt)
        pred_bk = Fraction(2, n - 1) * (pred_o + pred_e)
        fails_o += (pred_o != got_o)
        fails_e += (pred_e != got_e)
        fails_bk += (pred_bk != got_bk)
        tot += 1
        per_n[n] = per_n.get(n, 0) + 1
print(f"  population: {len(POP)} posets, {tot} (poset, coefficient-vector) instances")
print("  by n: " + ", ".join(f"n={k}: {v}" for k, v in sorted(per_n.items())))
ok &= L.verdict(fails_o == 0, "E Var(f|C_o) = (1/4) sum c^2 A^o", f"{fails_o} failures / {tot}")
ok &= L.verdict(fails_e == 0, "E Var(f|C_e) = (1/4) sum c^2 A^e", f"{fails_e} failures / {tot}")
ok &= L.verdict(fails_bk == 0, "E_BK(f) = (2/(n-1)) (EVar|C_o + EVar|C_e)  -- (*) at :145",
                f"{fails_bk} failures / {tot}")

# ---------------------------------------------------------------------------------------
L.banner("e1.2  SIGN-BLINDNESS: the identity cannot see the signs of c")
print("  For each poset, flip the sign of ONE coefficient.  The identity's output is")
print("  unchanged BY CONSTRUCTION (c^2); the question is whether Var(f) moves -- if it")
print("  never did, sign-blindness would cost nothing.")
moved = same = 0
worst = Fraction(0)
for (n, lt) in POP:
    inc = L.incomparable_pairs(n, lt)
    if len(inc) < 2:
        continue
    LEs = L.linear_extensions(n, lt)
    c = {p: Fraction(1) for p in inc}
    d = dict(c)
    d[inc[0]] = Fraction(-1)
    f, g = L.pair_orientation_stat(LEs, c), L.pair_orientation_stat(LEs, d)
    mo_f = L.machinery_output(n, lt, LEs, c)
    mo_g = L.machinery_output(n, lt, LEs, d)
    assert mo_f == mo_g, "sign flip changed the identity's output -- impossible"
    vf, vg = L.variance(f), L.variance(g)
    if vf != vg:
        moved += 1
        if vf != 0:
            worst = max(worst, abs(vf - vg) / vf)
    else:
        same += 1
ok &= L.verdict(moved > 0, "a one-coefficient sign flip leaves the identity's output EXACTLY "
                           "fixed while Var(f) moves",
                f"{moved} posets move, {same} do not; worst relative move {L.fr(worst)}")

# ---------------------------------------------------------------------------------------
L.banner("e1.3  LEVEL-BLINDNESS: the identity emits no first moment")
print("  f -> f + a leaves every conditional variance and the Dirichlet form fixed, so no")
print("  quantity of the form E[f] is recoverable from the identity's output.  Checked")
print("  against the programme's own first-moment targets: E[inv_e] (row 8 / LIB) and")
print("  E[pos_x] (the (EQ) residual and lambda_std's position matrix).")
shifted = 0
for (n, lt) in POP[:80]:
    LEs = L.linear_extensions(n, lt)
    inc = L.incomparable_pairs(n, lt)
    if not inc:
        continue
    c = {p: Fraction(1) for p in inc}
    f = L.pair_orientation_stat(LEs, c)
    g = [v + Fraction(17, 3) for v in f]
    a = (L.e_cond_var(f, LEs, L.odd_blocks(n)), L.e_cond_var(f, LEs, L.even_blocks(n)),
         L.bk_energy(f, LEs, n, lt))
    b = (L.e_cond_var(g, LEs, L.odd_blocks(n)), L.e_cond_var(g, LEs, L.even_blocks(n)),
         L.bk_energy(g, LEs, n, lt))
    assert a == b
    if L.mean(f) != L.mean(g):
        shifted += 1
ok &= L.verdict(shifted > 0, "the identity is invariant under f -> f + a while E[f] is not",
                f"{shifted} posets checked, 0 output changes, {shifted} mean changes")

# ---------------------------------------------------------------------------------------
L.banner("e1.4  THE FILTER, stated as it is used in the README")
print("""  A target Q is REACHABLE BY THE MACHINERY (ticket test 1) only if the way Q depends on
  the linear-extension measure factors through the pair-adjacency probabilities (A^o, A^e).
  By e1.2 and e1.3 that excludes, at minimum:

    * every FIRST MOMENT of a pair-orientation statistic -- E[inv_e], E[pos_x], p_xy,
      the position matrix T[x,i], delta(P), Delta_1;
    * every quantity sensitive to the SIGNS of pair coefficients -- covariances between
      pair indicators, i.e. the (B-cov) residual;
    * every DEGREE-TWO statistic -- E[sum disp^2], i.e. (B).

  It admits: the BK Dirichlet form of a degree-one statistic, and functionals of the
  adjacency probabilities themselves.""")

L.banner("e1  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
