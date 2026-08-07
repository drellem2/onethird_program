#!/usr/bin/env python3
"""
mg-1df8 / checks 2, 4, 6 + standing target "bound words / figures" —
MACHINE-CHECK EVERY NUMBER STATE.md PRINTS AT THE ORDERING SITES.

Target: STATE.md at 491d42c79f7628c18cb7a5d197faa9f4600cd6c1
Sites:  lines 15 (L1b blockquote), 23 (Axis 1), 64 (mermaid), 115 (ledger row 8),
        209 (Literature status).

Every figure below is TYPED IN BY HAND from the quoted text and then re-derived
from the definitions.  Exact integers / Fractions throughout; the only floats are
in the log10 renderings, and those are cross-checked against exact integer digit
counts so no decision rests on one.
"""

from fractions import Fraction as F
import math
import sys

sys.set_int_max_str_digits(200000)   # 2^30000 has 9031 decimal digits


def rule(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


PASS, FAIL = [], []


def check(label, got, want, note=""):
    ok = (got == want)
    (PASS if ok else FAIL).append(label)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print(f"         STATE.md says : {want}")
    print(f"         re-derived    : {got}")
    if note:
        print(f"         {note}")
    return ok


def main():
    # ================================================================== C1
    rule("C1  THE UNIT MAP (lines 15 and 115).  One theorem, two divisions.")
    print("""
  STATE.md: "the ONE theorem is E[inv_e] < m/3 <= n(n-1)/6, and the two
  constants are two divisions of it -- / n^2 -> eps_c3ca < (n-1)/(6n) -> 1/6,
  and / ((n^2-1)/6) -> eps_spec < n/(n+1) -> 1.  eps_spec/eps_c3ca =
  6n^2/(n^2-1) -> 6."
""")
    print(f"    {'n':>4} {'n(n-1)/6':>12} {'/n^2':>14} {'/((n^2-1)/6)':>14} "
          f"{'ratio':>14}")
    for n in (3, 4, 5, 6, 40):
        T = F(n * (n - 1), 6)
        a = T / F(n * n)                      # eps_c3ca form
        b = T / (F(n * n - 1, 6))             # eps_spec form
        print(f"    {n:>4} {str(T):>12} {str(a):>14} {str(b):>14} "
              f"{str(b / a):>14}")
        assert a == F(n - 1, 6 * n), "eps_c3ca form must equal (n-1)/(6n)"
        assert b == F(n, n + 1), "eps_spec form must equal n/(n+1)"
        assert b / a == F(6 * n * n, n * n - 1), "ratio must be 6n^2/(n^2-1)"
    check("C1a  eps_c3ca closed form = (n-1)/(6n), limit 1/6",
          "(n-1)/(6n) -> 1/6", "(n-1)/(6n) -> 1/6",
          "verified as an IDENTITY at n = 3,4,5,6,40, not a fit")
    check("C1b  eps_spec closed form = n/(n+1), limit 1",
          "n/(n+1) -> 1", "n/(n+1) -> 1")
    check("C1c  ratio = 6n^2/(n^2-1), limit 6",
          "6n^2/(n^2-1) -> 6", "6n^2/(n^2-1) -> 6")

    # ================================================================== C2
    rule("C2  mg-5ce3's WITNESS (lines 15, 115).  g = n^2 below N0, "
         "n^2/log2 n at and above.")
    print("""
  STATE.md: "for any candidate N0, g(n) = n^2 below N0 and n^2/log2 n at and
  above is o(n^2) and violates E[inv_e] <= (eps_spec/6)(n^2-1) throughout
  [1, N0)."  Commit 4ef64d7 claims 13/13, 98/98, 898/898 violations at
  N0 = 15, 100, 900.  Re-derived here from the definition, eps_spec = 2e-2:
""")
    eps = F(2, 100)
    for N0, claimed in ((15, 13), (100, 98), (900, 898)):
        viol = 0
        tested = 0
        for n in range(2, N0):
            tested += 1
            if F(n * n) > eps / 6 * F(n * n - 1):
                viol += 1
        print(f"    N0={N0:<5} tested n=2..{N0-1}: {tested:>4} "
              f"violations {viol:>4}  (commit claims {claimed})")
        check(f"C2-N0={N0}  violation count on [2, N0)", viol, claimed)
    print("""
  NOTE ON THE PREFIX: STATE.md writes the interval as [1, N0) while the counts
  are over n = 2..N0-1.  At n = 1 the bound is (eps/6)(1-1) = 0 and g(1) = 1 > 0,
  so n = 1 IS a violation too and the claim '[1, N0)' is correct; the counts
  simply start at n = 2, which is where inv_e is defined.  NOT A DISCREPANCY.""")

    # ================================================================== C3
    rule("C3  THE TAME MEMBER'S OWN THRESHOLD (line 115).  "
         "n >= 2^300 ~ 10^90, and 10^9031.")
    print("""
  STATE.md: "the tame member n^2/log2 n on its own first satisfies (LIB-const)
  at log2 n >= 6/eps_spec = 300, i.e. n >= 2^300 ~ 10^90 at the repaired
  eps_spec = 2e-2 (10^9031 at the superseded 2e-4)."

  DERIVATION (mine).  n^2/log2 n <= (eps/6)(n^2-1) is, dropping the -1 (which
  only helps),  1/log2 n <= eps/6,  i.e.  log2 n >= 6/eps.
""")
    for eps_str, eps_v in (("2e-2", F(2, 100)), ("2e-4", F(2, 10000))):
        thresh = F(6) / eps_v
        n_exp = int(thresh)
        # exact integer 2^n_exp, then its exact decimal digit count
        val = 1 << n_exp
        digits = len(str(val))
        log10_float = n_exp * math.log10(2)
        print(f"    eps_spec = {eps_str:<6} 6/eps = {thresh}  "
              f"-> n >= 2^{n_exp}")
        print(f"        exact decimal digits of 2^{n_exp} = {digits}"
              f"   => floor(log10) = {digits-1}")
        print(f"        float log10 cross-check           = {log10_float:.4f}"
              f"   round-to-nearest = {round(log10_float)}")
        assert digits - 1 == int(log10_float), "digit count must match log10"
    check("C3a  6/eps_spec at 2e-2", int(F(6) / F(2, 100)), 300)
    check("C3b  2^300 rendered as 10^90", round(300 * math.log10(2)), 90,
          "log10(2^300) = 90.309; STATE.md prints 10^90")
    check("C3c  6/eps_spec at the superseded 2e-4",
          int(F(6) / F(2, 10000)), 30000)
    check("C3d  2^30000 rendered as 10^9031",
          round(30000 * math.log10(2)), 9031,
          "log10(2^30000) = 9030.9; STATE.md prints 10^9031")
    print("""
    CONVENTION CHECK -- the two figures must use the SAME rounding, or one of
    them is wrong.  floor would give (90, 9030); round-to-nearest gives
    (90, 9031).  STATE.md prints (90, 9031), so it is round-to-nearest at BOTH
    sites.  CONSISTENT.  (Had it printed (90, 9030) or (91, 9031) that would be
    a mixed convention and a finding.)""")
    check("C3e  rounding convention is the same at both sites",
          (round(300 * math.log10(2)), round(30000 * math.log10(2))),
          (90, 9031))

    # ================================================================== C4
    rule("C4  THE CROSSOVER (lines 15, 115, 209).  n ~ 900C = 18C/eps_spec "
         "-- AND IT PINS gamma.")
    print("""
  STATE.md:209  "the n ~ 900C (LIB)/(LIB-const) crossover ... (18C/eps_spec at
  eps_spec = 2e-2 -- this row's own n ~ 900 is that value at C = 1, and C >= 1)."

  ARITHMETIC CHECK of 18C/eps_spec:""")
    for C in (1, 2, 10):
        v = F(18 * C) / F(2, 100)
        print(f"        C={C:<3}  18C/eps_spec = {v}")
    check("C4a  18C/eps_spec at C=1, eps=2e-2", F(18) / F(2, 100), F(900))
    print("""
  NOW THE PART THAT IS NOT BOOKKEEPING.  The crossover is where (LIB)'s bound
  meets (LIB-const)'s.  (LIB) is E[inv_e] = O(n/gamma), so the crossover solves

        (eps/6)(n^2 - 1)  =  C*n/gamma      ==>   n ~ 6C/(gamma*eps).

  STATE.md's own figure is 18C/eps.  Equating the two closed forms:

        6C/(gamma*eps) = 18C/eps   <==>   gamma = 6/18 = 1/3.

  SO STATE.md's 900C IS CONSISTENT WITH EXACTLY ONE VALUE OF gamma, AND IT IS
  1/3.  Verified numerically:""")
    print(f"    {'gamma':>10} {'6C/(gamma*eps), C=1':>24} {'matches 900?':>14}")
    for g in (F(1), F(1, 2), F(1, 3), F(1, 6)):
        v = F(6) / (g * F(2, 100))
        print(f"    {str(g):>10} {str(v):>24} {str(v == 900):>14}")
    check("C4b  gamma implied by the 900C figure", F(6) / (F(1, 3) * F(2, 100)),
          F(900), "gamma = 1/3 is the UNIQUE value making 6C/(gamma*eps) = 900C")
    print("""
  CONSEQUENCE FOR CHECK 1.  (LIB) ==> (LIB-weak) needs gamma = omega(1/n)
  (m1_ordering.py R1).  gamma = 1/3 is a CONSTANT, so the implication holds and
  the chain's first link is sound.  BUT STATE.md NEVER STATES gamma = 1/3, AND
  NEVER DEFINES gamma AT ALL -- I recovered it by inverting a figure in a
  different section.  See the verdict.""")

    # ================================================================== C5
    rule("C5  THE LITERATURE SHORTFALLS (line 209).")
    print("""
  STATE.md: "n >= 15 falls short of n >= 100 ... by 85, short of the n ~ 900C
  crossover by >= 885 ... Gain: 6 of the 91 orders in the master-bound dead
  zone, 6.6% -- 0.67% against the crossover at the most favourable C = 1."
""")
    check("C5a  100 - 15", 100 - 15, 85)
    check("C5b  900 - 15 (floor, since C >= 1)", 900 - 15, 885)
    print("\n    Dead zone: this arc's own census covers n <= 8, the master-bound")
    print("    route needs n >= 100, so the dead zone is n = 9..99:")
    dead = list(range(9, 100))
    print(f"        |{{9,...,99}}| = {len(dead)}")
    check("C5c  size of the master-bound dead zone", len(dead), 91)
    gained = list(range(9, 15))     # literature pushes coverage to n >= 15
    print(f"        literature covers n <= 14, so it removes "
          f"{{9,...,14}} = {len(gained)} orders")
    check("C5d  orders gained", len(gained), 6)
    pct = F(6, 91) * 100
    print(f"        6/91 = {pct} = {float(pct):.4f}%")
    check("C5e  gain as a percentage of the dead zone",
          round(float(pct), 1), 6.6)
    pct2 = F(6, 900) * 100
    print(f"        6/900 = {pct2} = {float(pct2):.4f}%")
    check("C5f  gain against the crossover at C=1",
          round(float(pct2), 2), 0.67)

    # ================================================================== C6
    rule("C6  mg-c4f5's BEST CONSTANTS (line 15) -- CHECK 4's "
         "'manufactured optimism' TEST.")
    print("""
  STATE.md: "the document names the linear form min(p,1-p) >= (1/3)(1-TV),
  which has 0 counterexamples over 1,168,036 pairs at n <= 7 and best constant
  c*(n) = 1/2, 1/2, 5/12, 2/5, 7/20 -- above 1/3 and falling."
""")
    cs = [F(1, 2), F(1, 2), F(5, 12), F(2, 5), F(7, 20)]
    third = F(1, 3)
    print(f"    {'c*(n)':>10} {'decimal':>12} {'> 1/3?':>8} {'margin':>14}")
    for c in cs:
        print(f"    {str(c):>10} {float(c):>12.5f} {str(c > third):>8} "
              f"{str(c - third):>14}")
    check("C6a  every c* is strictly above 1/3", all(c > third for c in cs), True)
    non_increasing = all(cs[i] >= cs[i + 1] for i in range(len(cs) - 1))
    strictly_falling = all(cs[i] > cs[i + 1] for i in range(len(cs) - 1))
    check("C6b  the sequence is non-increasing", non_increasing, True)
    print(f"\n    STRICTLY falling?  {strictly_falling}  "
          f"-- the first two entries are EQUAL (1/2, 1/2), so 'falling' is")
    print("    non-strict.  Reported as a wording note, NOT a finding: the")
    print("    substantive content ('above 1/3', and the margin SHRINKING from")
    print(f"    {cs[0]-third} to {cs[-1]-third}) is exactly right, and the margin at n=7 is")
    print(f"    {float(cs[-1]-third):.5f} -- a factor "
          f"{float((cs[0]-third)/(cs[-1]-third)):.2f} smaller than at n=3.")
    print("    THIS IS THE OPPOSITE OF MANUFACTURED OPTIMISM: the row prints the")
    print("    number that is closing on the threshold that would kill it.")

    # ================================================================== C7
    rule("C7  IS mg-131e's REFUTED 2/(n+1) IN CONFLICT WITH n/(n+1)?  NO.")
    print("""
  Dispatch note: mg-131e REFUTED eps_spec = 2/(n+1) at n=6.  STATE.md prints
  max{6E[inv_e]/(n^2-1) : mu in M_n} = n/(n+1).  These are DIFFERENT QUANTITIES
  in the same units: 2/(n+1) was mg-200d's PER-SLOT value, n/(n+1) is the MAX
  over the pair-bias information set.  A max must DOMINATE a particular value:
""")
    print(f"    {'n':>4} {'2/(n+1)':>10} {'n/(n+1)':>10} {'2/(n+1) <= n/(n+1)?':>22}")
    ok_all = True
    for n in (2, 3, 4, 5, 6, 7):
        a, b = F(2, n + 1), F(n, n + 1)
        ok_all &= (a <= b)
        print(f"    {n:>4} {str(a):>10} {str(b):>10} {str(a <= b):>22}")
    check("C7a  2/(n+1) <= n/(n+1) for all n >= 2", ok_all, True,
          "so the refuted per-slot value and the live max do NOT contradict; "
          "they coincide only at n = 2")
    print("\n    GREP RESULT: 0 occurrences of '2/(n+1)' anywhere in STATE.md at")
    print("    491d42c.  So the known in-flight correction (mg-372e) has nothing")
    print("    left to do IN THIS FILE.  Location report only, per the dispatch.")

    # ================================================================== SUM
    rule("SUMMARY")
    print(f"  PASS: {len(PASS)}    FAIL: {len(FAIL)}")
    for f in FAIL:
        print(f"    FAILED: {f}")
    if not FAIL:
        print("  Every figure STATE.md prints at the ordering sites re-derives.")


if __name__ == "__main__":
    main()
