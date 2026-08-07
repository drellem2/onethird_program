#!/usr/bin/env python3
"""mg-345e P3 — exact-rational check of MY OWN algebra.

Nothing here re-derives an already-proven corpus result. It checks the arithmetic this
ticket's document performs on top of them, because that arithmetic is mine and is the
thing most likely to be wrong. Everything is Fraction; there is no floating point in the
identity checks.
"""
import sys
from fractions import Fraction as F
from itertools import permutations


def unif_footrule_bruteforce(n):
    tot = F(0)
    cnt = 0
    for p in permutations(range(1, n + 1)):
        tot += sum(abs(p[i] - (i + 1)) for i in range(n))
        cnt += 1
    return tot / cnt


def eps_from_pairbias(n, m):
    """Smallest eps with  m/3 <= (eps/6)(n^2-1).   (LIB-const), Op-Form 6.2."""
    return F(2 * m, n * n - 1)


def main():
    fail = 0
    print("=" * 78)
    print("mg-345e P3 — EXACT-RATIONAL CHECK OF THIS TICKET'S OWN ALGEBRA")
    print("=" * 78)
    print()

    # ---------------------------------------------------------------- check 1
    print("-- C1: E_unif[footrule] = (n^2-1)/3 ------------------------------------------")
    bad = 0
    for n in range(2, 8):
        bf = unif_footrule_bruteforce(n)
        cf = F(n * n - 1, 3)
        ok = bf == cf
        bad += (not ok)
        print(f"   n={n}: brute {bf}   closed {cf}   {'OK' if ok else 'MISMATCH'}")
    for n in range(8, 60):
        # the closed form re-derived from  (1/n)*2*sum_d d(n-d)
        s = sum(F(d * (n - d)) for d in range(1, n))
        if F(2, n) * s != F(n * n - 1, 3):
            bad += 1
    print(f"   n=8..59 by re-derived sum: {'0 mismatches' if not bad else f'{bad} MISMATCH'}")
    if bad:
        fail = 1
    print()

    # ---------------------------------------------------------------- check 2
    print("-- C2: pair bias alone -> eps_spec = d*n/(n+1) --------------------------------")
    print("   inputs: Claim 6.1  E[inv_e] < m/3   (PROVEN, Op-Form 6.3)")
    print("           (LIB-const) E[inv_e] <= (eps/6)(n^2-1)   (Op-Form 6.2)")
    print("           d = m / C(n,2)")
    bad = 0
    for n in range(3, 40):
        C2 = F(n * (n - 1), 2)
        for num in (1, 2, 3, n - 1, n, C2 // 2 or 1, C2):
            m = int(num)
            if m > C2 or m < 1:
                continue
            d = F(m) / C2
            lhs = eps_from_pairbias(n, m)
            rhs = d * F(n, n + 1)
            if lhs != rhs:
                bad += 1
                print(f"   MISMATCH n={n} m={m}: {lhs} vs {rhs}")
    print(f"   {'0 mismatches' if not bad else f'{bad} MISMATCHES'} over the (n,m) grid")
    if bad:
        fail = 1
    print()

    # ---------------------------------------------------------------- check 3
    print("-- C3: the constant is uniform in n, and its supremum is exactly 1 ------------")
    worst = max(F(n, n + 1) for n in range(2, 5000))
    print(f"   max over n<5000 of d*n/(n+1) at d=1 : {worst} = {float(worst):.6f}")
    print(f"   strictly < 1 at every finite n      : {worst < 1}")
    print("   sup over n                          : 1  (limit, not attained)")
    if not (worst < 1):
        fail = 1
    print("   => pair bias alone DELIVERS (LIB-const) with an n-free constant.")
    print("      The constant it delivers is 1.")
    print()

    # ---------------------------------------------------------------- check 4
    print("-- C4: cross-check against mg-210d's recorded degenerate bound ----------------")
    print("   Op-Form 6.3 records: master bound + Claim 6.1 reproduces 1-lambda_std")
    print("   < d*n/(n+1). Feeding m/3 through 6E[I]/(n^2-1):")
    bad = 0
    for n in range(3, 40):
        C2 = F(n * (n - 1), 2)
        for m in (1, n, int(C2)):
            if m > C2:
                continue
            d = F(m) / C2
            via_master = F(6) * F(m, 3) / F(n * n - 1)
            if via_master != d * F(n, n + 1):
                bad += 1
    print(f"   {'0 mismatches' if not bad else f'{bad} MISMATCHES'} — the two agree exactly")
    if bad:
        fail = 1
    print()

    # ---------------------------------------------------------------- check 5
    print("-- C5: the DEMAND budget, and where C_3 went ---------------------------------")
    eps_leak = F(1, 5)                      # 0.20, mg-3ce3 repaired calibration
    print(f"   eps_leak (mg-3ce3, 0 RED / 6681)          : {eps_leak} = {float(eps_leak)}")
    for C3 in (F(1), F(2), F(10)):
        v = eps_leak ** 2 / (2 * C3)
        print(f"   eps_spec <= eps_leak^2/(2*C_3), C_3={C3}   : {v} = {float(v):.2e}")
    printed = eps_leak ** 2 / 2
    print(f"   STATE.md:15 carries eps_spec <~ 2e-2       : {float(printed):.2e}")
    print("   => the live headline is the C_3 = 1 value. C_3 is a LOSS factor (>= 1),")
    print("      so dropping it yields the LARGEST budget: the omission runs in the")
    print("      OPTIMISTIC direction. Op-Form sec 8.1 records C_3 as UNQUANTIFIED and its")
    print("      source conjecture as open AND too weak as worded.")
    if printed != F(1, 50):
        print("   !! 0.2^2/2 is not 1/50")
        fail = 1
    print()

    # ---------------------------------------------------------------- check 6
    print("-- C6: the 'factor ~50' figure is exactly supply/demand -----------------------")
    supply = F(1)                            # C3 above
    gap = supply / printed
    print(f"   supply (pair bias alone)  : {supply}")
    print(f"   demand (L4-set, C_3 = 1)  : {printed} = {float(printed):.2e}")
    print(f"   ratio                     : {gap}")
    print("   d101026 / mg-c4f5 landed 'the repaired gap factor is ~50, not ~5e3'.")
    print(f"   This reproduces it EXACTLY at {gap}, and identifies its two ends:")
    print("   the numerator is the PAIR-BIAS supply constant and the denominator is the")
    print("   L4-CALIBRATED demand. The published gap figure is the ratio of an")
    print("   L4-independent quantity to an L4-dependent one.")
    if gap != 50:
        print("   !! ratio is not 50")
        fail = 1
    print()

    print("=" * 78)
    print(f"P3 exit {fail}")
    return fail


if __name__ == "__main__":
    sys.exit(main())
