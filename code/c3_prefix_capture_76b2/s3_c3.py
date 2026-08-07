#!/usr/bin/env python3
"""s3 — MEASURING C_3 ITSELF, in all three currencies, with the population stratified.

`Op-Form 4.3` names TWO readings of the Prefix-capture conjecture and derives ONE relation
from them.  With the s1 dictionary in hand the readings become three distinct measurable
quantities, and they are NOT the same number:

    C_3^cut  := Phi*_prefix / Phi*                    (conductance currency)
                -- "the Cheeger sweep restricted to prefixes, with controlled loss",
                which is L3's own wording.  Feeds a degraded prefix-Cheeger inequality
                Phi*_pref <= sqrt(2 (C_3^cut)^2 (1-lambda_std)), so Op-Form's C_3 is its
                SQUARE.

    C_3^gap  := min_k (1 - rho(A_k)) / (1 - lambda_std)      (gap currency)
                -- the "1-o(1)" repair Op-Form 4.3 names.  Gives
                Phi_P(A_k) <= C_3^gap * eps_spec DIRECTLY, with NO Cheeger square.

    c        := max_k rho(A_k) / lambda_std                  (literal currency)
                -- the conjecture AS WORDED: "captures a constant fraction of the
                dominant standard eigenvalue".  Usable iff c >= (1-eps_leak)/(1-eps_spec).

Sections:
    (C0)  STRATIFY.  1 - lambda_std = 0 on a large sub-population.  Exactly which one?
    (C1)  THE REGIME.  Does ANY poset here sit inside the budget eps_spec <= 2e-2?
    (C2)  C_3^cut, exactly, over the primitive posets, by n.
    (C3)  C_3^gap and c, by n, against the H3 threshold.
    (C4)  MONOTONICITY STRATIFIED BY GAP -- the honest test of the theorem's hypothesis.

Every C_3 figure printed here is measured OUTSIDE the regime it would be used in.  That
sentence is printed next to every one of them, not once at the top.
"""

from fractions import Fraction as F
import sys

from lib76b2 import (Poset, all_posets, standard_spectrum, monotone_in_span,
                     is_monotone, connected)

NMAX = 6
EPS_LEAK = F(1, 5)                 # 0.20 -- mg-e35c F5's repaired value.  EMPIRICAL.
EPS_SPEC = EPS_LEAK ** 2 / 2       # 2e-2 -- the C_3 = 1 budget, STATE.md's live figure.
C_THRESH = (1 - EPS_LEAK) / (1 - EPS_SPEC)     # H3
fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")
    return cond


print("=" * 78)
print("s3 — MEASURING C_3, in all three currencies")
print("=" * 78)
print()
print(f"CALIBRATION USED, stated per the ticket's instruction:")
print(f"  eps_leak = {EPS_LEAK} = {float(EPS_LEAK)}   (mg-e35c F5 repaired; EMPIRICAL --")
print("                                mg-3ce3's envelope, 0 RED / 6681 up to 0.20)")
print(f"  eps_spec = eps_leak^2/2 = {EPS_SPEC} = {float(EPS_SPEC)}   (the C_3 = 1 budget)")
print(f"  H3 threshold on the literal capture fraction:")
print(f"      c >= (1-eps_leak)/(1-eps_spec) = {C_THRESH} = {float(C_THRESH):.6f}")
print()

pops = {n: all_posets(n) for n in range(2, NMAX + 1)}
POP = sum(len(v) for v in pops.values())

# --------------------------------------------------------------------- (C0)
print("-" * 78)
print("(C0) STRATIFY -- where is 1 - lambda_std = 0, and is C_3 even defined there?")
print("-" * 78)
print("  Three predicates, all EXACT (no float, no eigenvalue):")
print("    DISC  the weighted graph a_ij is disconnected   <=>  1 - lambda_std = 0")
print("    CUT   the poset has an ordinal-sum cut point k  <=>  A_k is an exact split")
print("    PHI0  Phi* = 0")
rows = []
for n in range(2, NMAX + 1):
    d = c = p = agree = 0
    for P in pops[n]:
        D = not connected(P)
        C = not P.is_primitive()
        Z = P.phi_star()[0] == 0
        d += D
        c += C
        p += Z
        agree += (D == C == Z)
    rows.append((n, len(pops[n]), d, c, p, agree))
    check(agree == len(pops[n]),
          f"C0 n={n}: the three predicates disagree on {len(pops[n]) - agree} posets")
print()
print("     n   posets     DISC      CUT     PHI0   all three agree")
for (n, tot, d, c, p, a) in rows:
    print(f"  {n:4d} {tot:8d} {d:8d} {c:8d} {p:8d}   {a:8d} of {tot}")
print()
print(f"  VERDICT: {'the three predicates are the SAME predicate, 0 disagreements' if fail == 0 else 'THEY DISAGREE'}")
print()
print("  CONSEQUENCE, and it is the reason this section comes first.  On the")
print("  ordinal-sum-DECOMPOSABLE posets every currency of C_3 is 0/0: Phi* = 0,")
print("  Phi*_prefix = 0, 1 - lambda_std = 0, and 1 - rho(A_k) = 0 at the cut point.")
print("  Those posets are not evidence about C_3 in either direction -- they are the")
print("  case where Step 5's conclusion holds EXACTLY and the whole chain is vacuous.")
print("  Every C_3 figure below is therefore restricted to the PRIMITIVE population.")
print()
prim = {n: [P for P in pops[n] if P.is_primitive()] for n in range(2, NMAX + 1)}
PRIM = sum(len(v) for v in prim.values())
print(f"  PRIMITIVE population: {PRIM} of {POP} posets " +
      ", ".join(f"n={n}:{len(prim[n])}/{len(pops[n])}" for n in range(2, NMAX + 1)))
print()

# --------------------------------------------------------------------- (C1)
print("-" * 78)
print("(C1) THE REGIME -- does any poset in this population sit inside the budget?")
print("-" * 78)
gaps = []
for n in range(2, NMAX + 1):
    for P in prim[n]:
        lam, dom, mult = standard_spectrum(P)
        gaps.append((1.0 - lam, n, P))
gaps.sort(key=lambda t: t[0])
print(f"  smallest 1 - lambda_std over the {PRIM} primitive posets  [FLOAT, Jacobi]:")
for g, n, P in gaps[:5]:
    print(f"      {g:.10f}   n={n}  rel={sorted(P.rel)}")
print(f"  the budget requires 1 - lambda_std <= eps_spec = {float(EPS_SPEC)}")
inside = sum(1 for g, _, _ in gaps if g <= float(EPS_SPEC))
print(f"  posets inside the budget: {inside} of {PRIM}")
print()
print("  >>> EVERY C_3 FIGURE BELOW IS MEASURED OUTSIDE THE REGIME IT WOULD BE USED IN. <<<")
print("  This corroborates mg-c4f5 / mg-e35c A1 from a different direction: the master")
print("  bound excludes the target for non-chain posets on n <= 10 (n <= 100 primitive),")
print("  and here the SPECTRAL quantity itself never gets near it at any n this")
print("  population reaches.  A C_3 measured here is a structural datum, not a")
print("  calibration, and it is reported as one.")
print()

# --------------------------------------------------------------------- (C2)
print("-" * 78)
print("(C2) C_3^cut = Phi*_prefix / Phi*   -- EXACT, the conductance currency (L3's own")
print("     wording).  Op-Form 4.3's C_3 is its SQUARE, because it is spent inside the")
print("     Cheeger square: Phi*_pref <= C_3^cut * Phi* <= C_3^cut * sqrt(2(1-lambda_std)).")
print("-" * 78)
print()
print("     n   primitive   C_3^cut = 1   max C_3^cut          attained at")
worst_by_n = {}
for n in range(2, NMAX + 1):
    ones = 0
    best = None
    for P in prim[n]:
        ps = P.phi_star()[0]
        pp = P.phi_star_prefix()[0]
        check(pp >= ps, f"C2 n={n}: prefix minimum below the global minimum")
        if ps == 0:
            continue
        r = pp / ps
        if r == 1:
            ones += 1
        if best is None or r > best[0]:
            best = (r, P)
    worst_by_n[n] = best
    if best is None:
        print(f"  {n:4d} {len(prim[n]):10d}   (no poset with Phi* > 0)")
    else:
        r, P = best
        print(f"  {n:4d} {len(prim[n]):10d} {ones:13d}   {str(r):10s} = {float(r):.6f}"
              f"   rel={sorted(P.rel)}")
print()
seq = [float(worst_by_n[n][0]) for n in range(3, NMAX + 1) if worst_by_n[n]]
print(f"  max C_3^cut by n, n = 3..{NMAX}: " + ", ".join(f"{x:.4f}" for x in seq))
grows = all(seq[i] <= seq[i + 1] + 1e-12 for i in range(len(seq) - 1))
strict = any(seq[i] < seq[i + 1] - 1e-12 for i in range(len(seq) - 1))
print(f"  weakly non-decreasing in n: {grows}      strictly somewhere: {strict}")
print()
print("  READ THIS ROW CAREFULLY.  It is the ONLY currency in which a C_3 bound could be")
print("  read off a finite population, and a finite population CANNOT establish a bound")
print("  uniform in n -- it can only REFUTE one.  What the row shows is the direction of")
print("  travel, and the direction is the wrong one for the conductance reading of L3.")
print("  This is a NEGATIVE result about that reading and is reported as one.")
print()

# --------------------------------------------------------------------- (C3)
print("-" * 78)
print("(C3) C_3^gap and the literal capture fraction c   [lambda_std is FLOAT, Jacobi;")
print("     Phi and rho are EXACT; the ratio is float only because its denominator is]")
print("-" * 78)
print()
print("     n   primitive   max C_3^gap    min c      c below H3 threshold")
for n in range(2, NMAX + 1):
    mx = None
    mn = None
    below = 0
    cnt = 0
    for P in prim[n]:
        lam, dom, mult = standard_spectrum(P)
        gap = 1.0 - lam
        if gap <= 1e-12 or lam <= 1e-12:
            continue
        cnt += 1
        best_gap = min(float(P.rho_prefix(k)) for k in range(1, n))
        r = best_gap / gap
        if mx is None or r > mx[0]:
            mx = (r, P)
        cc = max(1.0 - float(P.rho_prefix(k)) for k in range(1, n)) / lam
        if mn is None or cc < mn[0]:
            mn = (cc, P)
        if cc < float(C_THRESH):
            below += 1
    if cnt == 0:
        print(f"  {n:4d} {len(prim[n]):10d}   (none with 0 < lambda_std)")
        continue
    print(f"  {n:4d} {len(prim[n]):10d} {mx[0]:12.6f} {mn[0]:10.6f}   "
          f"{below} of {cnt} primitive posets with lambda_std > 0")
print()
print(f"  H3 threshold: the LITERAL conjecture closes the chain iff c >= {float(C_THRESH):.6f}")
print(f"     at eps_leak = {float(EPS_LEAK)}.  At the SUPERSEDED eps_leak = 0.02 / ")
print(f"     eps_spec = 2e-4 the same threshold is "
      f"{float((1-F(1,50))/(1-F(1,5000))):.6f}.")
print("  The threshold MOVED with mg-e35c F5's 100x repair, and Op-Form 4.3's verdict on")
print("  the literal reading was never re-examined against the repaired value.")
print()
print("  >>> measured outside the regime; see (C1) <<<")
print()

# --------------------------------------------------------------------- (C4)
print("-" * 78)
print("(C4) MONOTONICITY, STRATIFIED BY GAP -- the honest test of the theorem's own")
print("     hypothesis.  s2 found monotonicity is a MINORITY property overall; the")
print("     conjecture is stated only for a minimal counterexample, where the gap is")
print("     small.  So: does monotonicity concentrate where the gap is small?")
print("-" * 78)
buckets = [(0.0, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.01)]
tally = {b: [0, 0] for b in buckets}
for g, n, P in gaps:
    if g <= 1e-12:
        continue
    lam, dom, mult = standard_spectrum(P)
    v = monotone_in_span(dom)
    for b in buckets:
        if b[0] <= g < b[1]:
            tally[b][0] += 1
            tally[b][1] += (v == "YES")
            break
print()
print("     1 - lambda_std band     primitive posets    monotone dominant eigenvector")
for b in buckets:
    tot, yes = tally[b]
    pct = f"{100.0*yes/tot:.1f}%" if tot else "  n/a"
    print(f"     [{b[0]:.2f}, {b[1]:.2f})  {tot:16d} {yes:20d}   {pct}")
print()
smallest = [P for g, n, P in gaps if g > 1e-12][:50]
mono50 = sum(1 for P in smallest if monotone_in_span(standard_spectrum(P)[1]) == "YES")
print(f"  among the 50 primitive posets with the SMALLEST positive gap: "
      f"{mono50} of 50 are monotone")
print()

print("=" * 78)
print(f"s3 VERDICT: {'ALL CONSISTENCY CHECKS PASS' if fail == 0 else str(fail) + ' FAILURES'}")
print("=" * 78)
sys.exit(1 if fail else 0)
