"""a4 -- mg-8bc7's question (A): the parity / boundary asymmetry.

pm-onethird's statement of it: C_o gives blocks {x1,x2},{x3,x4},... with swaps at positions
1,3,5,...; C_e gives a leftover singleton x1 and blocks {x2,x3},{x4,x5},... with swaps at
2,4,6,....  For n even there are n/2 odd positions and n/2 - 1 even ones, so the two
foliations are not symmetric and do not cover the same number of edges -- and the symmetric
expression 2I - Pi_o - Pi_e "quietly presumes a symmetry the construction does not have".
Does the asymmetry perturb (*), (**) or (***), and does it differ for n odd vs even?

Four things are separated here, because the question runs them together:

  4.1  the asymmetry is REAL and is worse than the position count suggests -- measured, with
       the degenerate case where one of the two terms of (*) is identically zero exhibited.
  4.2  it perturbs NONE of (*), (**), (***) -- verified separately at each parity, because
       "holds for all n" and "holds at both parities" are different measurements and only the
       second answers the question that was asked.
  4.3  n odd vs n even: order reversal (which carries L(P) to L(P^op)) maps the 0-indexed
       position p to n-1-p, so it PRESERVES position parity iff n is even and REVERSES it
       iff n is odd.  Hence for n odd the pair (C_o, C_e) on P is carried to (C_e, C_o) on
       P^op -- a genuine symmetry, up to duality -- while for n even each foliation is
       carried to ITSELF and no such exchange exists.  Verified as fiber-size multisets.
  4.4  what the asymmetry does cost: the two projections have different ranks, so no
       argument may treat them as interchangeable at n even.
"""

from fractions import Fraction
from collections import Counter
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, random_poset, linear_extensions,
                     groups_o, groups_e, swap_positions, fibers, incomparable_pairs,
                     linear_stat, variance, expected_cond_variance, bk_energy, random_c,
                     cond_expectation, bk_apply, legal_at, swap_at, dual)

rng = random.Random(77713)


def main():
    ok = True

    banner("a4.1  the asymmetry, measured")
    print(f"  {'n':>3}{'odd swap posns':>16}{'even swap posns':>17}{'C_o blocks':>12}"
          f"{'C_e blocks':>12}{'C_o singletons':>16}{'C_e singletons':>16}")
    for n in range(2, 11):
        go, ge = groups_o(n), groups_e(n)
        so, se = swap_positions(go), swap_positions(ge)
        print(f"  {n:>3}{len(so):>16}{len(se):>17}"
              f"{sum(1 for g in go if len(g) == 2):>12}{sum(1 for g in ge if len(g) == 2):>12}"
              f"{sum(1 for g in go if len(g) == 1):>16}{sum(1 for g in ge if len(g) == 1):>16}")
    ok &= verdict(all(len(swap_positions(groups_o(n))) - len(swap_positions(groups_e(n)))
                      == (1 if n % 2 == 0 else 0) for n in range(2, 40)),
                  "position counts differ by exactly 1 at n even and by 0 at n odd")
    print("  pm-onethird's count is confirmed: n/2 vs n/2-1 at n even.  The note never uses it.")

    # The asymmetry in EDGES -- which is what actually enters (*) -- is a property of P too.
    print()
    print("  edge counts are not determined by the position counts; measured over posets:")
    ratios = []
    zero_e = zero_o = 0
    for n in range(2, 7):
        pool = (list(gen_posets_exhaustive(n)) if n <= 5
                else [random_poset(6, 0.3, rng) for _ in range(60)])
        for lt in pool:
            LEs = linear_extensions(n, lt)
            eo = sum(1 for L in LEs for p in swap_positions(groups_o(n)) if legal_at(L, p, lt))
            ee = sum(1 for L in LEs for p in swap_positions(groups_e(n)) if legal_at(L, p, lt))
            if eo + ee == 0:
                continue
            if ee == 0:
                zero_e += 1
            if eo == 0:
                zero_o += 1
            if ee > 0:
                ratios.append(eo / ee)
    print(f"    odd-edges / even-edges over {len(ratios)} posets: min {min(ratios):.4f}, "
          f"max {max(ratios):.4f}, and {zero_e} posets have ZERO even edges "
          f"({zero_o} have zero odd edges)")

    # The extreme case, exhibited: at n = 2, C_e = (I_1) determines L completely, so Pi_e = I
    # and E Var(f|C_e) is identically zero.  One of the two terms of (*) VANISHES and (*)
    # still holds exactly.  This is stronger than "not symmetric".
    LEs = linear_extensions(2, frozenset())
    vals = linear_stat(2, frozenset(), Fraction(0), {(0, 1): Fraction(1)}, LEs)
    Vo = expected_cond_variance(vals, LEs, groups_o(2))
    Ve = expected_cond_variance(vals, LEs, groups_e(2))
    E = bk_energy(vals, LEs, 2, frozenset())
    print()
    print(f"  n=2 antichain, f = 1{{0<1}}:  E Var(f|C_o) = {Vo},  E Var(f|C_e) = {Ve},"
          f"  E_BK = {E},  (2/(n-1))(Vo+Ve) = {Fraction(2, 1) * (Vo + Ve)}")
    ok &= verdict(Ve == 0 and E == Fraction(2, 1) * (Vo + Ve),
                  "one term of (*) is IDENTICALLY ZERO and (*) is still exact")

    banner("a4.2  does the asymmetry perturb (*), (**), (***)?  -- split by parity of n")
    res = {}
    for n in range(2, 8):
        pool = (list(gen_posets_exhaustive(n)) if n <= 5
                else [random_poset(n, rng.choice([0.15, 0.3]), rng) for _ in range(50)])
        bad_star = bad_starstar = bad_3 = tested = 0
        for lt in pool:
            LEs = linear_extensions(n, lt)
            pairs = incomparable_pairs(n, lt)
            if not pairs:
                continue
            c = random_c(pairs, rng)
            vals = linear_stat(n, lt, Fraction(rng.randint(-2, 2)), c, LEs)
            tested += 1
            go, ge = groups_o(n), groups_e(n)
            k = Fraction(2, n - 1)
            Vo = expected_cond_variance(vals, LEs, go)
            Ve = expected_cond_variance(vals, LEs, ge)
            E = bk_energy(vals, LEs, n, lt)
            if E != k * (Vo + Ve):
                bad_star += 1
            V = variance(vals)
            if V != 0 and E / V != k * (Vo + Ve) / V:
                bad_starstar += 1
            lhs = bk_apply(vals, LEs, n, lt)
            po, pe = cond_expectation(vals, LEs, go), cond_expectation(vals, LEs, ge)
            if lhs != [k * (2 * f - a - b) for f, a, b in zip(vals, po, pe)]:
                bad_3 += 1
        res[n] = (tested, bad_star, bad_starstar, bad_3)
    print(f"  {'n':>3}{'parity':>8}{'tested':>9}{'(*) bad':>10}{'(**) bad':>10}{'(***) bad':>11}")
    for n, (t, b1, b2, b3) in sorted(res.items()):
        print(f"  {n:>3}{('even' if n % 2 == 0 else 'odd'):>8}{t:>9}{b1:>10}{b2:>10}{b3:>11}")
    ok &= verdict(all(b1 == b2 == b3 == 0 for _, b1, b2, b3 in res.values()),
                  "(*), (**) and (***) are unperturbed at BOTH parities",
                  f"{sum(r[0] for r in res.values())} statistics")
    print("  reason: the derivation is a per-position sum and 2/(n-1) is the CHAIN's")
    print("  normalization (compression.tex:106), not a count of odd vs even positions.")
    print("  The two sides of (*) are free to be lopsided; the identity never compares them.")

    banner("a4.3  n odd vs n even: reversal maps position p to n-1-p")
    print("  prediction: reversal (L(P) -> L(P^op)) preserves position parity iff n is even.")
    print("    n odd  -> fiber-size multiset of C_e on P equals that of C_o on P^op")
    print("    n even -> fiber-size multiset of C_o on P equals that of C_o on P^op")
    bad_odd = bad_even = seen_odd = seen_even = 0
    for n in range(2, 8):
        pool = (list(gen_posets_exhaustive(n))[:400] if n <= 5
                else [random_poset(n, rng.choice([0.15, 0.3]), rng) for _ in range(60)])
        for lt in pool:
            ltd = dual(n, lt)
            LEs, LEd = linear_extensions(n, lt), linear_extensions(n, ltd)
            so = Counter(len(v) for v in fibers(LEs, groups_o(n)).values())
            se = Counter(len(v) for v in fibers(LEs, groups_e(n)).values())
            do = Counter(len(v) for v in fibers(LEd, groups_o(n)).values())
            de = Counter(len(v) for v in fibers(LEd, groups_e(n)).values())
            if n % 2 == 1:
                seen_odd += 1
                if se != do or so != de:
                    bad_odd += 1
            else:
                seen_even += 1
                if so != do or se != de:
                    bad_even += 1
    ok &= verdict(bad_odd == 0, "n ODD: reversal+duality EXCHANGES the two foliations",
                  f"{bad_odd}/{seen_odd} violations")
    ok &= verdict(bad_even == 0, "n EVEN: reversal+duality preserves EACH foliation",
                  f"{bad_even}/{seen_even} violations")
    # and the exchange must NOT hold at n even -- otherwise the distinction is vacuous
    cross_even = 0
    seen = 0
    for n in (4, 6):
        pool = (list(gen_posets_exhaustive(4)) if n == 4
                else [random_poset(6, 0.3, rng) for _ in range(60)])
        for lt in pool:
            ltd = dual(n, lt)
            se = Counter(len(v) for v in fibers(linear_extensions(n, lt), groups_e(n)).values())
            do = Counter(len(v) for v in fibers(linear_extensions(n, ltd), groups_o(n)).values())
            seen += 1
            if se != do:
                cross_even += 1
    ok &= verdict(cross_even > 0,
                  "n EVEN: the exchange FAILS -- the parity distinction is not vacuous",
                  f"{cross_even}/{seen} posets where C_e(P) and C_o(P^op) differ")

    banner("a4.4  what the asymmetry costs: rank Pi_o vs rank Pi_e")
    print("  rank Pi = number of fibers.  2I - Pi_o - Pi_e is symmetric in FORM; the two")
    print("  projections it subtracts are not interchangeable objects.")
    print(f"  {'n':>3}{'posets':>9}{'rank Pi_o > rank Pi_e':>24}{'equal':>8}{'<':>6}")
    for n in range(2, 7):
        pool = (list(gen_posets_exhaustive(n)) if n <= 5
                else [random_poset(6, 0.3, rng) for _ in range(80)])
        gt = eq = lt_ = 0
        for lt in pool:
            LEs = linear_extensions(n, lt)
            a = len(fibers(LEs, groups_o(n)))
            b = len(fibers(LEs, groups_e(n)))
            gt += a > b
            eq += a == b
            lt_ += a < b
        print(f"  {n:>3}{len(pool):>9}{gt:>24}{eq:>8}{lt_:>6}")
    print("  (rank Pi_o <= rank Pi_e is the typical direction at n even: C_o has more blocks,")
    print("   so its fibers are bigger and there are fewer of them.)")

    print()
    print("a4 VERDICT:", "(A) answered" if ok else "INSTRUMENT BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
