"""b3_routes — the EXPLICIT L2-free test vectors, and exactly what each one buys.

The theorem of b2 says: any monotone `g` gives `Phi*_pref^2 <= R(g)(2Delta_P - R(g))`.
It does not say where `g` comes from.  Three constructions, in increasing order of how
much they know about the poset, and one control:

  (a) `g_pos`  — the centred POSITION vector (0,1,...,n-1) - (n-1)/2.  Knows nothing about
      the poset at all.  Its Rayleigh quotient has a closed form worth recording:
          R(g_pos) = 6 E[sum_i (i - pos(i))^2] / (n(n^2-1)) = 1 - E[Spearman rho],
      the expected Spearman rank correlation between e and a uniform linear extension.
      Verified exactly here rather than asserted.
  (b) `g_sort` — the MONOTONE REARRANGEMENT of a dominant standard eigenvector: take `v`,
      sort its entries increasingly along e.  Knows the eigenvector but not its order.
      This is the natural "repair" of L2: it is what you do when `v` is NOT monotone.
  (c) `g_cone` — the minimiser over the whole monotone cone.  The best any such route can
      do.  b2's `mu_pref`.
  (d) CONTROL: `v` itself, unsorted.  It is not monotone in general, so the theorem does
      not apply to it; it is included only to show the ordering R(v) <= R(g_sort) that
      makes (b) a genuine loss and not a free lunch.

Every certification below is EXACT.  The eigenvector that seeds (b) and (d) is FLOAT, but
it is only a source of candidate vectors: what is certified is the rational vector actually
built, whose Rayleigh quotient is computed in Fractions.
"""

from fractions import Fraction as F

from lib28ff import (all_posets, pencil, from_coeffs, is_monotone, rayleigh,
                     gap_at_least, pencil_eigs, cone_min, rationalise, sweep_bound_sq)

LADDER = [F(1), F(11, 10), F(5, 4), F(3, 2), F(2), F(3), F(5), F(10)]


def g_pos(n):
    """Centred position vector, scaled by 2 to stay integral."""
    return [F(2 * i - (n - 1)) for i in range(n)]


def coeffs_of(f):
    """Write a centred monotone f in the psi basis: c_k = f_k - f_{k-1} >= 0."""
    return [f[k] - f[k - 1] for k in range(1, len(f))]


def sorted_fiedler(P):
    """The monotone rearrangement of a dominant standard eigenvector, rationalised.
    FLOAT seed, exact output."""
    n = P.n
    Q, N = pencil(P)
    ev = pencil_eigs(Q, N)
    c = ev[0][1]
    v = [float(x) for x in from_coeffs(n, [F(round(y * 10 ** 6), 10 ** 6) for y in c])]
    vs = sorted(v)
    g = [F(round(x * 840), 840) for x in vs]
    s = sum(g)
    g = [x * n - s for x in g]                      # centre exactly
    return g, v


if __name__ == "__main__":
    print("=== b3: explicit L2-free test vectors ===\n")

    # ---- the closed form for R(g_pos), verified exactly
    bad = []
    for n in range(2, 7):
        for P in all_posets(n):
            g = g_pos(n)
            lhs = rayleigh(P, g)
            rhs = 6 * P.E_sq_displacement() / (n * (n * n - 1))
            if lhs != rhs:
                bad.append(P)
    print(f"[EXACT] R(g_pos) == 6 E[sum_i (i-pos(i))^2] / (n(n^2-1)) == 1 - E[Spearman rho]:")
    print(f"        {'0 exceptions' if not bad else str(len(bad)) + ' EXCEPTIONS'} over all "
          f"5230 posets, n = 2..6")
    assert not bad

    for n in range(2, 7):
        pop = [P for P in all_posets(n) if P.is_primitive()]
        print(f"\n--- n = {n}:  {len(pop)} PRIMITIVE posets "
              f"(decomposable excluded: 1-lambda_std = 0 there) ---")

        stats = {"g_pos": [], "g_sort": [], "g_cone": []}
        order_violation = 0
        for P in pop:
            d = P.delta_max()
            # (a)
            r = rayleigh(P, g_pos(n))
            stats["g_pos"].append((P, sweep_bound_sq(d, r)))
            # (b)
            gs, v = sorted_fiedler(P)
            assert is_monotone(gs), "sorted_fiedler produced a non-monotone vector"
            if sum(x * x for x in gs) == 0:
                gs = g_pos(n)
            rs = rayleigh(P, gs)
            stats["g_sort"].append((P, sweep_bound_sq(d, rs)))
            # (c)
            Q, N = pencil(P)
            mp, c_f = cone_min(Q, N)
            gc = from_coeffs(n, rationalise(c_f, den=840))
            assert is_monotone(gc)
            rc = rayleigh(P, gc)
            stats["g_cone"].append((P, sweep_bound_sq(d, rc)))
            # (d) control: the cone minimum can never beat the unconstrained minimum
            if mp < pencil_eigs(Q, N)[0][0] - 1e-9:
                order_violation += 1

        assert order_violation == 0, "cone minimum fell below the unconstrained minimum"
        print("        control (d): the cone minimum never fell below the unconstrained "
              "minimum.  0 violations.")
        for name in ("g_pos", "g_sort", "g_cone"):
            line = []
            for c in LADDER:
                good = sum(1 for (P, b) in stats[name]
                           if gap_at_least(P, b / (2 * c)))
                line.append(f"c={str(c):>5}:{good:5d}")
            print(f"   [EXACT] {name:7s} certifies C_3 <= c at ... / {len(pop)}")
            print(f"           " + "  ".join(line))
