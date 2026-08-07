#!/usr/bin/env python3
"""s2 — THE SWEEP, and the theorem `C_3 = 1 given L2`.

The claim this section exists to check is:

    THEOREM.  If a dominant standard eigenvector of S_P is monotone along the
    distinguished order e (this is L2's first disjunct, and Step 3 of the architecture),
    then the Cheeger sweep produces a PREFIX cut directly, with NO loss.  There is a
    prefix A_k with

        Delta_1(A_k, A_k^c)  =  Phi_P(A_k)  <=  sqrt( 2 (1 - lambda_std) ),

    i.e. L3's "quantitatively controlled loss" is a factor of exactly 1, uniformly in n,
    and C_3 = 1.

It rests on three legs, checked here separately:

    (S1)  THE SWEEP LEMMA.  For any non-constant f, some threshold set S of f with
          |S| <= n/2 has Phi_P(S)^2 <= 2 R(f).  Checked EXACTLY on rational f -- no
          verdict passes through math.sqrt; the comparison is squared.
    (S2)  MONOTONE => PREFIX.  If f is non-decreasing along e then EVERY threshold set
          of f is a suffix, and its complement is a prefix.  Checked exhaustively.
    (S3)  THE INSTANTIATION.  At every poset whose dominant standard eigenspace contains
          a monotone vector, sweeping that vector yields a prefix cut meeting the bound.
          The eigenvector is FLOAT (labelled); the conductance and the comparison are
          exact.

    (S4)  RED DRILL.  The hypothesis is doing work: there are posets where the sweep of a
          NON-monotone dominant eigenvector lands on a set that is neither prefix nor
          suffix, and posets where the best prefix is strictly worse than the best cut.
          Without L2 the conclusion genuinely fails; the theorem is not vacuous.

Exit 0 iff every check passes.
"""

from fractions import Fraction as F
from itertools import combinations
import sys

from lib76b2 import (Poset, all_posets, named_posets, standard_spectrum,
                     monotone_in_span, is_monotone, sweep_sets, sweep_best,
                     is_prefix_or_suffix, rayleigh)

NMAX = 6
fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")
    return cond


print("=" * 78)
print("s2 — THE SWEEP, and the theorem  C_3 = 1  given L2")
print("=" * 78)
print()

pops = {n: all_posets(n) for n in range(2, NMAX + 1)}
POP = sum(len(v) for v in pops.values())
print(f"POPULATION: {POP} posets -- every poset on {{0..n-1}} with the identity a linear")
print(f"extension, n = 2..{NMAX}.  Counts by n: " +
      ", ".join(f"n={n}:{len(pops[n])}" for n in range(2, NMAX + 1)))
print()

# --------------------------------------------------------------------- (S1)
print("-" * 78)
print("(S1) THE SWEEP LEMMA -- Phi(S)^2 <= 2 R(f) at some threshold set S, |S| <= n/2")
print("     EXACT: Fractions throughout, the Cheeger comparison is SQUARED not rooted")
print("-" * 78)
# Deterministic rational test functions: all f in {0,1,2}^n modulo constants, plus the
# centred prefix indicators.  No RNG -- a seedless random sweep is not reproducible and a
# seeded one is not more informative than an enumeration this small.
def test_functions(n):
    out = []
    for vec in range(3 ** n):
        f, v = [], vec
        for _ in range(n):
            f.append(F(v % 3))
            v //= 3
        if len(set(f)) > 1:
            out.append(f)
    return out


s1_cases = 0
s1_slack_min = None
for n in range(2, 5 + 1):
    for P in pops[n]:
        for f in test_functions(n):
            R = rayleigh(P, f)
            S, phi = sweep_best(P, f)
            s1_cases += 1
            ok = check(S is not None and phi ** 2 <= 2 * R,
                       f"S1 n={n} rel={sorted(P.rel)} f={f}: Phi={phi} R={R}")
            if ok and R > 0:
                slack = phi ** 2 / (2 * R)
                if s1_slack_min is None or slack > s1_slack_min:
                    s1_slack_min = slack
print(f"  checked {s1_cases} (poset, test function) pairs over the "
      f"{sum(len(pops[n]) for n in range(2,6))}-poset population at n = 2..5")
print(f"  worst ratio Phi(S)^2 / (2 R(f)) attained: {s1_slack_min} "
      f"= {float(s1_slack_min):.6f}  (must be <= 1)")
print(f"  VERDICT: {'HOLDS with 0 exceptions' if fail == 0 else 'FAILS'}")
print()

# --------------------------------------------------------------------- (S2)
print("-" * 78)
print("(S2) MONOTONE => PREFIX.  If f is non-decreasing along e, every threshold set of f")
print("     is a SUFFIX and its complement is a PREFIX.  Exhaustive over monotone f.")
print("-" * 78)
s2_f = s2_sets = 0
for n in range(2, 7 + 1):
    for vec in range(4 ** n):
        f, v = [], vec
        for _ in range(n):
            f.append(F(v % 4))
            v //= 4
        f = f[::-1]
        if not all(f[i] <= f[i + 1] for i in range(n - 1)) or len(set(f)) < 2:
            continue
        s2_f += 1
        for S in sweep_sets(f):
            s2_sets += 1
            check(is_prefix_or_suffix(S, n), f"S2 n={n} f={f} S={sorted(S)}")
print(f"  checked {s2_sets} threshold sets over {s2_f} monotone functions, n = 2..7,")
print("  f ranging over every non-decreasing vector in {0,1,2,3}^n")
print(f"  VERDICT: {'HOLDS with 0 exceptions' if fail == 0 else 'FAILS'}")
print()
print("  This is the whole content of the source's own remark at `:328-332`:")
print('    "Cheeger theory does not by itself imply that the cut is a prefix.  That')
print('     requires monotonicity of the dominant standard eigenvector in the')
print('     distinguished order, or a direct prefix theorem."')
print("  The source attaches NO loss to that conversion, and there is none to attach: the")
print("  sweep of a monotone vector never visits a non-prefix cut in the first place.")
print()

# --------------------------------------------------------------------- (S3)
print("-" * 78)
print("(S3) THE INSTANTIATION -- at every poset with a monotone dominant standard")
print("     eigenvector, the sweep lands on a prefix cut meeting the Cheeger bound.")
print("     Eigenvector: FLOAT (Jacobi).  Conductance and comparison: EXACT.")
print("-" * 78)
buckets = {"YES": 0, "NO": 0, "UNDECIDED": 0}
degenerate = 0
s3_checked = s3_prefix = 0
worst = None
for n in range(2, NMAX + 1):
    for P in pops[n]:
        lam, dom, mult = standard_spectrum(P)
        gap = 1.0 - lam
        verdict = monotone_in_span(dom)
        buckets[verdict] += 1
        if mult > 1:
            degenerate += 1
        if verdict != "YES" or gap <= 1e-12:
            continue                       # gap 0 => every cut already exact; see s3
        v = None
        for w in dom:
            if is_monotone(w):
                v = w
                break
        if v is None:                       # the YES came from the projected observable
            continue
        S, phi = sweep_best(P, v, tol=1e-9)
        if S is None:
            continue
        s3_checked += 1
        if is_prefix_or_suffix(S, n):
            s3_prefix += 1
        else:
            check(False, f"S3 sweep of a monotone vector left the prefix/suffix family: "
                         f"n={n} rel={sorted(P.rel)} S={sorted(S)}")
        # Cheeger, with the FLOAT gap and a tolerance stated at the site
        check(float(phi) ** 2 <= 2 * gap + 1e-9,
              f"S3 Cheeger n={n} rel={sorted(P.rel)} Phi={phi} gap={gap}")
        r = float(phi) ** 2 / (2 * gap) if gap > 0 else 0.0
        if worst is None or r > worst[0]:
            worst = (r, n, sorted(P.rel), phi, gap)
print(f"  monotone dominant standard eigenvector, over the {POP}-poset population:")
print(f"      YES       {buckets['YES']:6d}   a monotone dominant eigenvector was EXHIBITED")
print(f"      NO        {buckets['NO']:6d}   multiplicity 1 and neither +v nor -v is monotone")
print(f"      UNDECIDED {buckets['UNDECIDED']:6d}   multiplicity > 1 and this instrument did not")
print("                         solve the feasibility problem -- silence, not a miss")
print(f"  degenerate top standard eigenvalue (multiplicity > 1): {degenerate} of {POP} posets")
print()
print(f"  swept the exhibited monotone eigenvector at {s3_checked} posets with gap > 0:")
print(f"      {s3_prefix} of {s3_checked} sweeps landed on a PREFIX-OR-SUFFIX cut")
if worst:
    r, n, rel, phi, gap = worst
    print(f"  worst Phi^2 / (2(1-lambda_std)) over those: {r:.6f}  (must be <= 1)")
    print(f"      at n={n}, rel={rel}, Phi={phi}, 1-lambda_std={gap:.10f}  [gap is FLOAT]")
print(f"  VERDICT: {'HOLDS with 0 exceptions' if fail == 0 else 'FAILS'}")
print()

# --------------------------------------------------------------------- (S4)
print("-" * 78)
print("(S4) RED DRILL -- is the hypothesis doing any work?")
print("-" * 78)
print("  An instrument that can only print OK is indistinguishable from one that checks")
print("  nothing.  Two constructed negatives:")
print()
# (a) a non-monotone vector whose sweep leaves the prefix/suffix family
n = 4
Pn = Poset(4, [(0, 2), (1, 2), (1, 3)], "N-poset")
fbad = [F(0), F(3), F(1), F(2)]              # non-monotone along e
bad_sets = [S for S in sweep_sets(fbad) if not is_prefix_or_suffix(S, n)]
print(f"  (a) f = {fbad} on the N-poset is NOT monotone along e.  Of its "
      f"{len(sweep_sets(fbad))} threshold")
print(f"      sets, {len(bad_sets)} are neither prefix nor suffix: "
      f"{[sorted(S) for S in bad_sets]}")
check(len(bad_sets) > 0, "S4a: red drill found no non-prefix threshold set")
print("      So (S2) is not a triviality about threshold sets -- it is about MONOTONE f.")
print()
# (b) a poset where the best prefix is strictly worse than the best cut
gapfound = []
for n2 in range(3, NMAX + 1):
    for P in pops[n2]:
        ps, _ = P.phi_star()
        pp, _ = P.phi_star_prefix()
        if pp > ps:
            gapfound.append((n2, sorted(P.rel), ps, pp))
print(f"  (b) posets where min-over-prefixes STRICTLY exceeds min-over-all-cuts: "
      f"{len(gapfound)} of {POP}")
if gapfound:
    n2, rel, ps, pp = gapfound[0]
    print(f"      first witness: n={n2}, rel={rel}, Phi* = {ps}, Phi*_prefix = {pp}, "
          f"ratio = {pp/ps} = {float(pp/ps):.6f}")
    print("      At such a poset the prefix restriction DOES cost something, and the")
    print("      theorem's conclusion C_3 = 1 is not available from the sweep alone.")
    print("      What rescues it is that the sweep of a MONOTONE eigenvector never")
    print("      proposes the offending cut -- so the loss is never incurred.  Whether")
    print("      the two coexist is measured in s3, not assumed here.")
check(len(gapfound) > 0, "S4b: red drill found no prefix/global conductance gap")
print()

print("=" * 78)
print(f"s2 VERDICT: {'ALL CHECKS PASS' if fail == 0 else str(fail) + ' FAILURES'}")
print("=" * 78)
sys.exit(1 if fail else 0)
