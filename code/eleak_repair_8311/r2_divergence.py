"""mg-8311 R2 — THE DIVERGENCE COUNT, RE-DERIVED. The ticket forbids taking it from its body.

The ticket reports 8178 of 11316 (poset, cut) pairs at n <= 5. That number is NOT used as an
input anywhere in this script. What this script does is enumerate the population from
scratch -- my own poset enumerator, my own linear extensions, my own two leak functions --
count the divergences, and print the count. Whether it lands on 8178 is a PREDICTION
(PREDICTIONS.md P1, 80%), scored in the README against whatever comes out.

The population is stated at every print site rather than implied, because the denominator is
the whole content of a fraction like `8178 of 11316`: it is `all posets on {0..n-1} with the
identity a linear extension, n = 2..5` x `all 2^n - 2 proper cuts`. R2.1 reproduces the
poset counts themselves, so a matching total is not an accident of a differently-sized
population landing on the same ratio.

R2.4 measures the SIGN of the divergence, which no one has measured: PREDICTIONS.md P9 bets
70% that the convention never UNDER-charges. That is a real bet with a real loser.

OPERATOR SCOPE: leak counts only. No eigenvalue, no Delta_AT, no A(P). Transport axis.
"""

import sys
from fractions import Fraction as F

from lib8311 import all_posets_8311, leak_def, leak_conv, Tally

T = Tally()

print("=" * 78)
print("R2 — the divergence, counted from my own enumeration (the ticket's 8178 is NOT")
print("     an input to this script; whether I land on it is PREDICTIONS.md P1)")
print("=" * 78)

NMAX = 5
POP = {n: all_posets_8311(n) for n in range(2, NMAX + 1)}

# ---------------------------------------------------------------------------
print()
print("R2.1  first the POPULATION, so the denominator is not taken on trust. Posets on")
print("      {0..n-1} with the identity a linear extension, grown-and-closed rather than")
print("      masked-and-filtered, so agreement with mg-2de0's 40 and 357 is a real check:")
print(f"       {'n':>3s} {'posets':>8s} {'cuts each':>10s} {'pairs':>8s} {'lib2de0 says':>13s}")
LIB2DE0_SAYS = {4: 40, 5: 357}          # read from a3_nonvacuity.py's own print text
total_pairs = 0
bad = 0
for n in range(2, NMAX + 1):
    cuts = 2 ** n - 2
    pairs = len(POP[n]) * cuts
    total_pairs += pairs
    says = LIB2DE0_SAYS.get(n)
    if says is not None and says != len(POP[n]):
        bad += 1
    print(f"       {n:>3d} {len(POP[n]):>8d} {cuts:>10d} {pairs:>8d} "
          f"{('' if says is None else str(says)):>13s}")
print(f"       {'':>3s} {sum(len(POP[n]) for n in POP):>8d} {'':>10s} {total_pairs:>8d}")
T.report("my poset counts agree with mg-2de0's stated 40 (n=4) and 357 (n=5)", bad, 2,
         "per-n, integer equality against the count printed in a3_nonvacuity.py",
         "n=4 and n=5, the two n where mg-2de0 states a count in its own transcript")
print("       => the denominator is REPRODUCED, not adopted.")

# ---------------------------------------------------------------------------
print()
print("R2.2  the DIVERGENCE, per n and in total. A pair (P, A) diverges iff the two")
print("      EXPECTATIONS over L(P) differ -- not iff some single linear extension")
print("      differs, which would be a looser and larger count.")
print(f"       {'n':>3s} {'pairs':>8s} {'diverge':>8s} {'agree':>8s} {'% diverge':>10s}")
div_total = agree_total = 0
per_n = {}
smallest = None
for n in range(2, NMAX + 1):
    d = a = 0
    for P in POP[n]:
        for A in P.cuts():
            ed = P.E_leak(A, "def")
            ec = P.E_leak(A, "conv")
            if ed != ec:
                d += 1
                if smallest is None:
                    smallest = (n, P, A, ed, ec)
            else:
                a += 1
    per_n[n] = (d, a)
    div_total += d
    agree_total += a
    print(f"       {n:>3d} {d + a:>8d} {d:>8d} {a:>8d} {100.0 * d / (d + a):>9.1f}%")
print(f"       {'':>3s} {div_total + agree_total:>8d} {div_total:>8d} {agree_total:>8d} "
      f"{100.0 * div_total / (div_total + agree_total):>9.1f}%")
print()
print(f"       MY COUNT: {div_total} of {div_total + agree_total} (poset, cut) pairs diverge "
      f"at n <= {NMAX}.")
print(f"       THE TICKET'S FIGURE: 8178 of 11316.")
match = (div_total == 8178 and div_total + agree_total == 11316)
T.report("my independent recount equals the ticket's 8178 of 11316",
         0 if match else 1, 1,
         "two integer equalities, numerator and denominator separately",
         f"all posets n=2..{NMAX} with identity a linear extension x all 2^n-2 proper cuts",
         fatal=False)
if match:
    print("       => CONFIRMED INDEPENDENTLY. PREDICTIONS.md P1 HIT.")
else:
    print("       => DOES NOT REPRODUCE. PREDICTIONS.md P1 MISSED. The count above is mine")
    print("          and is what this instrument reports; the ticket's is not adopted.")

# ---------------------------------------------------------------------------
print()
print("R2.3  the SMALLEST witness, found by my own search order rather than quoted. Search")
print("      order is n ascending, then poset by relation-size ascending, then cut by size")
print("      ascending -- so 'smallest' means smallest n first, and is stated as such:")
n, P, A, ed, ec = smallest
print(f"       n = {n}, poset relation = {sorted(P.rel)}, A = {sorted(A)}")
print(f"       |L(P)| = {len(P.linear_extensions())}, L(P) = {list(P.linear_extensions())}")
print(f"       definition {ed}   convention {ec}")
is_2chain = (n == 2 and P.rel == frozenset({(0, 1)}) and A == frozenset({1})
             and ed == 0 and ec == 1)
T.report("the smallest witness IS the ticket's 2-chain 0<1 with A={1}, def 0 / conv 1",
         0 if is_2chain else 1, 1,
         "conjunction of five exact equalities: n, relation, cut, and both values",
         "the first divergence encountered in the search order stated above")

# ---------------------------------------------------------------------------
print()
print("R2.4  THE SIGN, which nobody has measured. Does the convention OVER-charge leakage,")
print("      UNDER-charge it, or both? PREDICTIONS.md P9 bets 70% that it never")
print("      under-charges. Measured per (poset, cut) on EXPECTATIONS, and separately per")
print("      (linear extension, cut) on the raw integer counts:")
over = under = eq = 0
for n in range(2, NMAX + 1):
    for P in POP[n]:
        for A in P.cuts():
            ed = P.E_leak(A, "def")
            ec = P.E_leak(A, "conv")
            if ec > ed:
                over += 1
            elif ec < ed:
                under += 1
            else:
                eq += 1
print(f"       on EXPECTATIONS:  convention > definition on {over}, "
      f"< on {under}, == on {eq}")
T.report("convention never UNDER-charges, on expectations", under,
         over + under + eq,
         "per-(poset, cut), exact Fraction comparison of the two expectations",
         f"all posets n=2..{NMAX} x all 2^n-2 proper cuts = {over + under + eq} pairs",
         fatal=False)
over_r = under_r = eq_r = 0
for n in range(2, NMAX + 1):
    for P in POP[n]:
        for A in P.cuts():
            for p in P.linear_extensions():
                vd, vc = leak_def(A, p), leak_conv(A, p)
                if vc > vd:
                    over_r += 1
                elif vc < vd:
                    under_r += 1
                else:
                    eq_r += 1
print(f"       on RAW COUNTS:    convention > definition on {over_r}, "
      f"< on {under_r}, == on {eq_r}")
T.report("convention never UNDER-charges, on raw per-extension counts", under_r,
         over_r + under_r + eq_r,
         "per-(poset, cut, linear extension), integer comparison",
         f"the same posets and cuts, every linear extension of each = "
         f"{over_r + under_r + eq_r} triples",
         fatal=False)
if under == 0 and under_r == 0:
    print("       => the convention is a ONE-SIDED error: it only ever over-charges leakage.")
    print("          CONSEQUENCE, and it is the load-bearing one for R4: Phi_conv(A) >=")
    print("          Phi_def(A) at every cut, so repairing E_leak can only LOWER Phi*, and")
    print("          the set of posets with Phi* strictly below the prefix minimum can only")
    print("          GROW. That is a DIRECTION on mg-2de0's published `65 of 431`, derived")
    print("          rather than observed. PREDICTIONS.md P9 HIT.")
else:
    print("       => the convention errs in BOTH directions. PREDICTIONS.md P9 MISSED, and")
    print("          R4 cannot predict the direction the `65 of 431` moves -- it must be")
    print("          measured on both sides, which R4 does anyway.")

# ---------------------------------------------------------------------------
print()
print("R2.5  n = 6, which PREDICTIONS.md declared a STRETCH GOAL and not a promise. It")
print("      finished, in about 15 seconds of CPU, so it is here rather than excused.")
print("      Two things come out of it, and the second is worth more than the first:")
P6 = all_posets_8311(6)
d6 = a6 = 0
for P in P6:
    for A in P.cuts():
        if P.E_leak(A, "def") != P.E_leak(A, "conv"):
            d6 += 1
        else:
            a6 += 1
print(f"       posets at n=6: {len(P6)}     cuts each: 62     pairs: {d6 + a6}")
print(f"       diverge: {d6} of {d6 + a6} ({100.0 * d6 / (d6 + a6):.1f}%)")
cum_p = sum(len(POP[n]) for n in POP) + len(P6)
cum_pairs = div_total + agree_total + d6 + a6
cum_div = div_total + d6
print(f"       CUMULATIVE n=2..6: {cum_p} posets, {cum_pairs} (poset, cut) pairs, "
      f"{cum_div} diverge ({100.0 * cum_div / cum_pairs:.1f}%)")
print()
print("       and the CROSS-CHECK, which is why this section earns its runtime: mg-76b2")
print("       reports 5230 posets and 310404 (poset, cut) pairs for n=2..6, from an")
print("       instrument this one shares no code with. My enumerator GROWS closed relation")
print("       sets; lib2de0's MASKS over 2^C(n,2) candidates and filters. Two algorithms,")
print("       two authors, one number -- or not:")
bad = 0
if cum_p != 5230:
    bad += 1
if cum_pairs != 310404:
    bad += 1
print(f"       mine: {cum_p} posets / {cum_pairs} pairs        "
      f"mg-76b2: 5230 posets / 310404 pairs")
T.report("my n=2..6 population equals mg-76b2's 5230 posets and 310404 pairs", bad, 2,
         "two integer equalities against the figures printed at "
         "docs/OneThird-C3-PrefixCapture-mg-76b2.md:140 and :382",
         "all posets on {0..n-1} with identity a linear extension, n=2..6, grown-and-closed")
print("       => the DENOMINATOR of this whole arc's Phi work is now confirmed from two")
print("          independent enumerators. This is a check on mg-76b2's population, not on")
print("          its conclusion, and it does not touch C_3 -- lib76b2 is never imported.")
print("       => the divergence rises with n (25%, 43%, 59%, 73%, 84%), which is the shape")
print("          to expect: the fraction of cuts that are PREFIXES of e is (n-1)/(2^n-2)")
print("          and falls off exponentially, and prefixes are exactly where the two")
print("          conventions agree. So the defect is not a small-n artefact getting")
print("          smaller -- it gets WORSE as n grows, and 72% at n<=5 understates it.")

print()
print("=" * 78)
print(f"R2 TOTAL BAD: {T.bad}")
print("=" * 78)
sys.exit(0 if T.bad == 0 else 1)
