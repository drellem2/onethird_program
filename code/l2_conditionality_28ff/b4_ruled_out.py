"""b4_ruled_out — THE CANDIDATES I RULED OUT, enumerated.

The ticket: "If you answer in the negative on any branch, ENUMERATE THE CANDIDATES YOU
RULED OUT.  A bare negative reads as honesty and goes unchecked."  My answer on branch (C)
is affirmative but CONDITIONAL, which owes the same debt: these are the L2-free routes I
tried and what happened to each, with an explicit witness wherever one exists.

R1  "the prefix is the minimum cut at its own size"      -> FALSE, smallest witness given
R2  "Phi*_pref = Phi*"                                    -> FALSE, counted
R3  "the position vector is a dominant standard eigenvector" -> FALSE, counted
R4  "the monotone rearrangement of a dominant eigenvector is near-optimal enough"
                                                          -> measured, see b3
R5  "(M) with the parent's un-sharpened 2*Delta*R form"   -> FAILS from n = 5, see b2
R6  "the footrule route without restricting to primitive" -> FAILS, and the reason was
                                                             filed in advance (P10)
R7  a RED DRILL on the instrument itself: a synthetic weighted graph where the target is
    genuinely FALSE, to show the whole verdict pipeline can print FAIL.
"""

from fractions import Fraction as F
from itertools import combinations

from lib28ff import (all_posets, pencil, from_coeffs, is_monotone, rayleigh,
                     gap_at_least, pencil_eigs, psd_exact, sweep_bound_sq)


def synth_verdict(n, W):
    """Everything the poset pipeline does, but for an arbitrary symmetric weight matrix W
    with zero diagonal.  Returns (Phi*_pref, Phi*, target-holds?).  EXACT."""
    d = [sum(W[i][j] for j in range(n) if j != i) for i in range(n)]
    L = [[(d[i] if i == j else -W[i][j]) for j in range(n)] for i in range(n)]

    def cut(A):
        A = set(A)
        return sum(W[i][j] for i in A for j in range(n) if j not in A)

    def phi(A):
        A = set(A)
        return F(cut(A), 1) / min(len(A), n - len(A))

    pref = min(phi(range(k)) for k in range(1, n))
    star = min(phi(A) for m in range(1, n) for A in combinations(range(n), m))

    def gap_ge(r):
        B = [[L[i][j] - r * ((F(1) if i == j else F(0)) - F(1, n)) for j in range(n)]
             for i in range(n)]
        return psd_exact(B)

    return pref, star, gap_ge(pref * pref / 2), max(d)


if __name__ == "__main__":
    print("=== b4: candidates ruled out ===\n")

    # ---------------------------------------------------------------- R1, R2, R3
    r1_wit = r2_cnt = r3_cnt = 0
    r1_first = None
    tot = 0
    for n in range(2, 7):
        for P in all_posets(n):
            tot += 1
            # R1: is the prefix a minimum-leak set of its own size?
            for m in range(1, n):
                lo, arg = P.leak_min_at_size(m)
                if lo < P.leak(range(m)):
                    r1_wit += 1
                    if r1_first is None:
                        r1_first = (P, m, arg, lo, P.leak(range(m)))
                    break
            # R2: does the prefix family contain a global minimiser of Phi?
            if P.phi_star_prefix()[0] > P.phi_star()[0]:
                r2_cnt += 1
            # R3: is the position vector a dominant standard eigenvector?
            g = [F(2 * i - (n - 1)) for i in range(n)]
            if P.is_primitive():
                Q, N = pencil(P)
                mu = pencil_eigs(Q, N)[0][0]
                if float(rayleigh(P, g)) > mu + 1e-9:
                    r3_cnt += 1

    print("R1  'the prefix minimises leak among sets of its own size'  -> FALSE "
          "[PREDICTIONS.md P14, FORMALITY: mg-76b2 already reports 468/5230 for R2]")
    P, m, arg, lo, pv = r1_first
    print(f"    failing at {r1_wit} of {tot} posets, n = 2..6.  Smallest witness:")
    print(f"      n = {P.n}, relations {sorted(P.rel)}")
    print(f"      size {m}: prefix {{0..{m-1}}} leaks {pv} = {float(pv):.6f}, "
          f"but {sorted(arg)} leaks {lo} = {float(lo):.6f}")
    print("    CONSEQUENCE: the prefix family is NOT closed under the min-cut argument, so "
          "plain\n    Cheeger over all cuts cannot be transported to prefixes for free.  "
          "This is exactly\n    the gap L2 exists to bridge, and it is real.\n")

    print(f"R2  'Phi*_pref = Phi*'  -> FALSE at {r2_cnt} of {tot} posets, n = 2..6.")
    print("    The prefix restriction genuinely costs something at a positive fraction of "
          "the\n    population, so no route may assume it is free.\n")

    print(f"R3  'the position vector is a dominant standard eigenvector'  -> FALSE at "
          f"{r3_cnt} primitive posets.")
    print("    If it were true L2's first disjunct would be automatic.  It is not, which is "
          "why\n    b3's g_pos route is a genuine test and not a restatement.\n")

    print("R4  'the monotone rearrangement of a dominant eigenvector is near-optimal' — "
          "MEASURED in b3, not ruled out.\n")
    print("R5  '(M) with the parent's un-sharpened 2*Delta_P*R(g)' — FAILS from n = 5 "
          "(b2: c > 1 at 6 of 275\n    primitive posets).  The Cauchy-Schwarz factor "
          "mg-76b2 discarded is load-bearing.\n")
    print("R6  'the footrule route on all posets' — FAILS on every decomposable non-chain, "
          "for the\n    reason filed in PREDICTIONS.md P10 BEFORE the run: 1-lambda_std = 0 "
          "there.  b1 confirms it.\n")

    # ---------------------------------------------------------------- R7 RED DRILL
    print("R7  RED DRILL — can this pipeline ever print FAIL?")
    print("    A synthetic weighted graph on 6 vertices whose only thin cut is NOT a prefix:")
    print("    two clusters {0,3} and {1,2,4,5}, joined weakly.  If the verdict machinery")
    print("    were vacuous it would certify this too.\n")
    fired = 0
    for eps_den in (10, 40, 200, 1000):
        n = 6
        e = F(1, eps_den)
        W = [[F(0)] * n for _ in range(n)]

        def put(i, j, w):
            W[i][j] = W[j][i] = w

        put(0, 3, F(1, 2))                                  # inside cluster A = {0,3}
        for (i, j) in [(1, 2), (1, 4), (1, 5), (2, 4), (2, 5), (4, 5)]:
            put(i, j, F(1, 4))                              # inside cluster B
        for i in (0, 3):                                    # weak bridge A -- B
            for j in (1, 2, 4, 5):
                put(i, j, e)
        pref, star, target, dmax = synth_verdict(n, W)
        print(f"    bridge weight 1/{eps_den:<5}:  Phi*_pref = {float(pref):.6f}  "
              f"Phi* = {float(star):.6f}  "
              f"target Phi*_pref^2 <= 2(1-lam):  {'HOLDS' if target else 'FAILS'}")
        if not target:
            fired += 1
    print(f"\n    the pipeline printed FAIL at {fired} of 4 synthetic graphs.  "
          "The verdict is not vacuous.")
    assert fired > 0, "R7: the red drill never fired -- the verdict machinery is vacuous"
