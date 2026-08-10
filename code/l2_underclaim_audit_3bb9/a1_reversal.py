"""a1 — the UNDER-CLAIM reversal, re-measured on an instrument that shares no code with
mg-28ff's, mg-29fe's or mg-51f4's.

What mg-b58d landed (docs/OneThird-L2-Conditionality-mg-28ff.md §2, repair 6):

    V00 = rho EXACTLY, so dropping both added steps certifies IFF L2's first disjunct
    holds; the V00 failure counts 0/0/10/166/3164 EQUAL the L2-failure counts and sum
    to 3340; and the first failure moves from n = 5 to n = 4.

This script measures, from the definitions and NOT from anyone's closed form:

  (A) the population (5230 / 4377) and the per-n primitive counts,
  (B) the identity `sum_k c_k psi_k is nondecreasing  iff  c >= 0` (the cone IS the
      monotone cone -- if this fails, mu_pref is a minimum over the wrong set),
  (C) rho >= 1 at EVERY primitive poset, which is what makes "V00 fails iff L2 fails" an
      identity rather than a coincidence,
  (D) the four variant constants computed TWICE -- once from the raw bound forms
      (2R, 2*Delta*R, R(2-R), R(2Delta-R)) divided by 2(1-lambda_std), and once from the
      closed forms in rho -- and the two must agree,
  (E) the per-n L2 census and the per-n failure counts of all four variants,
  (F) the per-n maxima of all four variants.
"""
import sys
import time
from fractions import Fraction as F
from lib3bb9 import (all_natural_posets, P3bb9, pencil, psi, from_coeffs,
                     gap_float, mu_pref_float, l2_first_disjunct)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
TOL = 1e-9

print("=" * 92)
print("a1  mg-3bb9 — the V00 = rho reversal, re-measured from the definitions")
print("=" * 92)

# ---------------------------------------------------------------- (B) the cone identity
print()
print("(B) CONE IDENTITY — `sum_k c_k psi_k` nondecreasing along e iff c >= 0")
bad = 0
checked = 0
for n in range(2, 7):
    import itertools
    for c in itertools.product([F(-1), F(0), F(1), F(3)], repeat=n - 1):
        v = from_coeffs(n, list(c))
        mono = all(v[i] <= v[i + 1] for i in range(n - 1))
        nonneg = all(x >= 0 for x in c)
        checked += 1
        if mono != nonneg:
            bad += 1
print(f"    {checked} coefficient vectors, mismatches: {bad}   -> {'IDENTITY HOLDS' if bad == 0 else 'BROKEN'}")

# ---------------------------------------------------------------- the sweep
tot_posets = 0
tot_prim = 0
rows = {}
rho_min_seen = None
disagree_closed_vs_raw = 0
for n in range(2, NMAX + 1):
    t0 = time.time()
    posets = all_natural_posets(n)
    tot_posets += len(posets)
    cnt = {"V11": 0, "V10": 0, "V01": 0, "V00": 0}
    mx = {"V11": None, "V10": None, "V01": None, "V00": None}
    l2_fail = 0
    l2_fail_eig = 0
    degen = 0
    disagree_l2 = 0
    prim = 0
    n4_fail_rels = []
    for rel in posets:
        P = P3bb9(n, rel)
        if P.decomposable():
            continue
        prim += 1
        Q, N = pencil(P)
        g = gap_float(Q, N)                       # 1 - lambda_std
        mu, cvec = mu_pref_float(Q, N)            # min over the monotone cone
        rho = mu / g
        if rho_min_seen is None or rho < rho_min_seen:
            rho_min_seen = rho
        D = float(P.Delta)
        # (D) raw bound forms -> constants, and the closed forms in rho
        raw = {"V00": 2 * mu, "V10": 2 * D * mu,
               "V01": mu * (2 - mu), "V11": mu * (2 * D - mu)}
        craw = {k: raw[k] / (2 * g) for k in raw}
        cclosed = {"V00": rho, "V10": rho * D,
                   "V01": rho - rho * rho * g / 2, "V11": rho * D - rho * rho * g / 2}
        for k in craw:
            if abs(craw[k] - cclosed[k]) > 1e-9 * max(1.0, abs(craw[k])):
                disagree_closed_vs_raw += 1
        # L2's first disjunct: the top standard eigenspace meets the monotone cone,
        # i.e. mu_pref == 1 - lambda_std.  Decided independently of any variant.
        holds_eig, dim = l2_first_disjunct(Q, N)
        if dim > 1:
            degen += 1
        if not holds_eig:
            l2_fail_eig += 1
        if mu > g * (1 + TOL):
            l2_fail += 1
            if n == 4:
                n4_fail_rels.append(sorted(rel))
            if holds_eig:
                disagree_l2 += 1
        else:
            if not holds_eig:
                disagree_l2 += 1
        for k in cnt:
            if cclosed[k] > 1 + TOL:
                cnt[k] += 1
            if mx[k] is None or cclosed[k] > mx[k]:
                mx[k] = cclosed[k]
    tot_prim += prim
    rows[n] = (len(posets), prim, cnt, mx, l2_fail, l2_fail_eig, degen, disagree_l2)
    print(f"    n={n}: {len(posets)} posets, {prim} primitive, {time.time()-t0:.1f}s")
    if n == 4:
        print("      the 10 that V00 kills at n = 4 (relations):")
        for r in n4_fail_rels:
            print(f"        {r}")

print()
print(f"(A) POPULATION over n = 2..{NMAX}:  {tot_posets} posets, {tot_prim} primitive")
print(f"(C) min rho over every primitive poset measured: {rho_min_seen:.12f}"
      f"   (must be >= 1: {'YES' if rho_min_seen >= 1 - 1e-9 else 'NO'})")
print(f"(D) closed-form-vs-raw-bound disagreements: {disagree_closed_vs_raw}")

print()
print("-" * 92)
print("(E) FAILURE COUNTS — posets where each variant's constant exceeds 1")
print("-" * 92)
print("NOTE: the `L2 by mu` column is the SAME predicate as V00 > 1, so its agreement with")
print("V00 is a TAUTOLOGY.  The `L2 by eigenspace` column is the independent one: it asks")
print("whether the top standard eigenspace meets the monotone cone, with mu_pref never used.")
print(f"{'n':>3} {'primitive':>10} | {'V11':>6} {'V10':>6} {'V01':>6} {'V00':>6} |"
      f" {'L2 by mu':>9} {'L2 by eigsp':>12} {'degen':>6} {'disagree':>9}")
s00 = s_l2 = s_l2e = s_deg = 0
for n in range(2, NMAX + 1):
    _, prim, cnt, mx, l2f, l2fe, deg, dis = rows[n]
    s00 += cnt["V00"]
    s_l2 += l2f
    s_l2e += l2fe
    s_deg += deg
    print(f"{n:>3} {prim:>10} | {cnt['V11']:>6} {cnt['V10']:>6} {cnt['V01']:>6} "
          f"{cnt['V00']:>6} | {l2f:>9} {l2fe:>12} {deg:>6} {dis:>9}")
print(f"{'sum':>3} {tot_prim:>10} | {'':>6} {'':>6} {'':>6} {s00:>6} | {s_l2:>9} {s_l2e:>12} {s_deg:>6}")

print()
print("-" * 92)
print("(F) MAXIMA")
print("-" * 92)
print(f"{'n':>3} | {'V11':>10} {'V10':>10} {'V01':>10} {'V00':>10}")
for n in range(2, NMAX + 1):
    _, prim, cnt, mx, l2f = rows[n][:5]
    print(f"{n:>3} | {mx['V11']:>10.6f} {mx['V10']:>10.6f} {mx['V01']:>10.6f} {mx['V00']:>10.6f}")

print()
print("VERDICT:")
first = {k: min([n for n in range(2, NMAX + 1) if rows[n][2][k] > 0], default=None)
         for k in ("V11", "V10", "V01", "V00")}
print(f"  first n at which each variant exceeds 1: {first}")
print(f"  V00 failure counts sum to {s00}; L2-by-mu sum {s_l2}; L2-by-eigenspace sum {s_l2e}; degenerate eigenspaces {s_deg}")
print("=" * 92)
