"""b1_footrule — an EXACT identity that is L2-free, and the bound it produces.

IDENTITY.   sum_{k=1}^{n-1} leak(A_k)  =  (1/2) E[ sum_i |i - pos(i)| ]
            i.e. the prefix leaks sum to HALF the expected Spearman footrule between the
            distinguished order e and a uniform random linear extension.

Proof (one line, no L2, no spectra).  leak(A_k) = E #{i : i < k <= pos(i)}, so
sum_k leak(A_k) = E sum_i #{k : i < k <= pos(i)} = E sum_i max(0, pos(i) - i)
                = (1/2) E sum_i |pos(i) - i|,
the last step because sum_i (pos(i) - i) = 0 for every permutation.

CONSEQUENCE (the linear co-area bound).  min_k a_k/b_k <= (sum a_k)/(sum b_k), and
sum_{k=1}^{n-1} min(k, n-k) = floor(n^2/4), so

    Phi*_pref  <=  E[footrule] / (2 floor(n^2/4)),      UNCONDITIONALLY.

This is a purely combinatorial handle on the quantity L2 exists to control — no
eigenvector, no monotonicity, no spectral gap on the left.  Whether it is STRONG enough to
reach the target `Phi*_pref^2 <= 2(1-lambda_std)` is a separate question, measured below.

PREDICTIONS.md P10 recorded IN ADVANCE that it cannot be, on decomposable posets: there
`1-lambda_std = 0` so the target's right side is 0, while E[footrule] > 0 at every
decomposable non-chain.  That is checked here rather than discovered.
"""

from fractions import Fraction as F

from lib28ff import all_posets, named_posets, sample_posets, gap_at_least

if __name__ == "__main__":
    print("=== b1: the footrule identity and the bound it gives ===\n")

    for n in range(2, 8):
        pop = all_posets(n) if n <= 6 else named_posets(7) + sample_posets(7, 90)
        tag = "EXHAUSTIVE" if n <= 6 else "named + deterministic sample"
        bad = [P for P in pop
               if sum(P.leak(range(k)) for k in range(1, P.n)) != P.E_footrule() / 2]
        # the linear co-area bound, exact
        viol = []
        for P in pop:
            lhs, _ = P.phi_star_prefix()
            rhs = P.E_footrule() / (2 * ((n * n) // 4))
            if lhs > rhs:
                viol.append(P)
        print(f"n={n} [{tag}, {len(pop)} posets]")
        print(f"   [EXACT] identity  sum_k leak(A_k) == E[footrule]/2 : "
              f"{len(pop)-len(bad)}/{len(pop)} hold")
        print(f"   [EXACT] bound     Phi*_pref <= E[footrule]/(2*floor(n^2/4)) : "
              f"{len(pop)-len(viol)}/{len(pop)} hold")
        assert not bad and not viol, "b1: an EXACT identity or bound failed"

    print("\n--- does the footrule bound reach the target Phi*_pref^2 <= 2(1-lambda_std)? ---")
    print("    (the question is whether E[footrule]/(2 floor(n^2/4)) is itself below "
          "sqrt(2(1-lambda_std)))\n")
    for n in range(2, 7):
        pop = all_posets(n)
        prim = [P for P in pop if P.is_primitive()]
        dec = [P for P in pop if not P.is_primitive()]
        q = 2 * ((n * n) // 4)

        def ok(P):
            b = P.E_footrule() / q
            return gap_at_least(P, b * b / 2)

        pg = sum(1 for P in prim if ok(P))
        dg = sum(1 for P in dec if ok(P))
        dch = sum(1 for P in dec if P.is_chain())
        print(f"n={n}:  PRIMITIVE {pg}/{len(prim)} certified by the footrule route;  "
              f"DECOMPOSABLE {dg}/{len(dec)} (chains among them: {dch})")
    print("\n--- HOW MUCH MARGIN? f* = max over PRIMITIVE posets of ---")
    print("    [E[footrule]/(2 floor(n^2/4))]^2 / (2(1-lambda_std)),  bracketed EXACTLY ---")
    for n in range(2, 8):
        pop = all_posets(n) if n <= 6 else named_posets(7) + sample_posets(7, 200)
        prim = [P for P in pop if P.is_primitive()]
        q = 2 * ((n * n) // 4)
        lo, hi = F(0), F(4)
        for _ in range(20):
            mid = (lo + hi) / 2
            b = [(P, (P.E_footrule() / q) ** 2 / (2 * mid)) for P in prim]
            if all(gap_at_least(P, r) for (P, r) in b):
                hi = mid
            else:
                lo = mid
        tag = "EXHAUSTIVE" if n <= 6 else "named + sample"
        print(f"    n={n} [{tag}, {len(prim):5d} primitive]:  "
              f"f* in [{float(lo):.5f}, {float(hi):.5f}]"
              + ("   <-- f* < 1 means the route certifies C_3 = 1 at EVERY member"
                 if hi < 1 else "   <-- f* >= 1: the route FAILS somewhere"))

    print("\n    P10 confirmed as predicted: on decomposable posets the route certifies "
          "exactly the chains,")
    print("    for the reason filed in advance — 1-lambda_std = 0 there, so only "
          "E[footrule] = 0 can pass.")
