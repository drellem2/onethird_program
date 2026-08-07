#!/usr/bin/env python3
"""mg-9f91 / step 1 -- RE-DERIVE THE UNIT MAP.

Exact rational arithmetic.  No floats in any assertion.

The one theorem (mg-6bc2, cited not re-derived):   E[inv_e] <= n(n-1)/6

Two normalisations of that same bound:
    eps_c3ca := E[inv_e] / n^2                (OneThird-LIBweak-mg-c3ca.md:172)
    eps_spec := 6*E[inv_e] / (n^2 - 1)        (STATE.md row 8's (LIB-const) form)

Claims under test:
    C1  eps_c3ca = (n-1)/(6n)          -> 1/6, strictly BELOW at every finite n
    C2  eps_spec = n/(n+1)             -> 1,   strictly BELOW at every finite n
    C3  eps_spec/eps_c3ca = 6n^2/(n^2-1) -> 6, strictly ABOVE at every finite n
    C4  C2's value is EXACTLY the closure value mg-6bc2 reports attained over M_n.
    C5  the entire difference between the two normalisations is the explicit /6
        in eps_spec's DEFINITION -- i.e. dropping it makes the ratio -> 1.
"""
from fractions import Fraction as F

NS = [3, 4, 5, 6, 7, 8, 10, 12, 100, 1000, 10**6]

def main():
    ok = 0
    tot = 0
    print(f"{'n':>8} {'eps_c3ca':>14} {'eps_spec':>12} {'ratio':>18} {'ratio-6':>12}")
    for n in NS:
        E = F(n * (n - 1), 6)
        c3ca = E / F(n * n)
        spec = 6 * E / F(n * n - 1)
        ratio = spec / c3ca
        # C1
        tot += 1; ok += (c3ca == F(n - 1, 6 * n))
        # C2
        tot += 1; ok += (spec == F(n, n + 1))
        # C3
        tot += 1; ok += (ratio == F(6 * n * n, n * n - 1))
        # strictness: limits are NOT attained
        tot += 1; ok += (c3ca < F(1, 6))
        tot += 1; ok += (spec < 1)
        tot += 1; ok += (ratio > 6)
        # C5: strip the /6 from eps_spec's definition -> E/(n^2-1); ratio to eps_c3ca -> 1
        spec_no6 = E / F(n * n - 1)
        tot += 1; ok += ((spec_no6 / c3ca) == F(n * n, n * n - 1))
        print(f"{n:>8} {str(c3ca):>14} {str(spec):>12} {str(ratio):>18} {float(ratio-6):>12.3e}")

    print()
    print(f"C1..C3 + strictness + C5 : {ok}/{tot} exact-rational checks pass")

    # C4 -- the closure value, stated as mg-6bc2 reports it, is the SAME expression.
    # max over M_n of 6E[inv_e]/(n^2-1) = n/(n+1).  We do not re-derive the LP;
    # we check that eps_spec evaluated at the theorem's bound IS that value.
    same = all((6 * F(n * (n - 1), 6) / F(n * n - 1)) == F(n, n + 1) for n in NS)
    print(f"C4  eps_spec at the bound == n/(n+1) (the attained closure value): {same}")

    # direction of approach, the P12 trap
    print()
    print("DIRECTION OF APPROACH (what a flat factor of 6 gets wrong at small n):")
    for n in (3, 4, 5, 6, 8):
        c3ca = F(n - 1, 6 * n)
        print(f"  n={n:<3} eps_c3ca={c3ca}  x6 -> {c3ca*6}   TRUE eps_spec={F(n,n+1)}"
              f"   error={float(F(n,n+1) - c3ca*6):+.4f}")

    # the finite population mg-6bc2 reports attainment over
    print()
    print("ATTAINMENT POPULATION per mg-6bc2 (cited, NOT re-derived here): n in {3,4,5,6,8}")
    print("  the <= directions are theorems for ALL n.  This script checks the ALGEBRA")
    print("  of the map only; it makes no claim about the LP or the extremal construction.")

if __name__ == "__main__":
    main()
