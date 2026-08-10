"""a3_currency -- THE ADVERSARIAL SECTION.  Which C_3 is `C_3 = 1` about?

mg-76b2's title says `C_3 ... IS 1`.  Its own section 7 measures a C_3 that
RISES with n.  Both can be true only if they are different numbers, and the
whole question this audit turns on is whether the deliverable EXHIBITS that
rather than leaving a reader to reconcile it.

Three currencies, all present in Op-Form sec.4.3 or its consumers:

    C_3^cut  = Phi*_pref / Phi*                     (L3's own wording)
    C_3^gap  = min_k (1-rho(A_k)) / (1-lambda_std)  (sec.4.3's gap-form repair)
    c        = max_k rho(A_k) / lambda_std          (the conjecture AS WORDED)

and a fourth, which is the one the TICKET'S RELATION uses:

    C_3^(III): the constant for which  Phi_pref <= sqrt(2 C_3 (1-lambda_std)).

Scores P4 (the adversarial one) and P5.

By hand, before running any of this (PREDICTIONS H7): C_3^gap >= 1 IDENTICALLY,
because 1-lambda_std is the MINIMUM of 1-rho(f) over all centred f and a centred
prefix indicator is one such f.  So the question is never "is it >= 1" -- it is
"is it > 1, and is it > 1 even where L2's FIRST DISJUNCT holds".

SCOPE ADDED AT THE CLAIM, mg-be0b, on mg-3329's finding (which is on mg-fa70's).
NOTHING HERE WAS FALSE AND NO NUMBER MOVES.  This section's population is built by
`p["mono"] == "YES"`, i.e. the 1032 primitive posets exhibiting L2's FIRST disjunct,
so every figure it prints was TRUE AS MEASURED.  What was missing is that the site
said so: EIGHT labels in this file read "under L2" / "where L2 holds" / "CONDITIONAL
on L2" / "under L2's hypothesis" -- the ticket named THREE of them, and re-running the
sweep rather than inheriting its list found the other five.  `L2` is a DISJUNCTION
("... monotone in the distinguished order, OR AT LEAST YIELDS A LOW-CONDUCTANCE
PREFIX"), so an unqualified "under L2" reads as "under EITHER disjunct" -- a claim
about a population this instrument never measured.  This is UNDER-SCOPING, NOT
FALSITY: nothing is marked false, no measurement is restated, and the C4 finding
(C_3^gap > 1 even on the branch where mg-76b2's theorem holds) stands exactly as
it was.  The second disjunct is UNQUANTIFIED -- weaker than and different from
refuted -- and is not struck anywhere here.
"""

from fractions import Fraction as F
from itertools import combinations
import math
from libA94 import (all_posets, linear_extensions, T_matrix, is_primitive,
                    spectral_gap, monotone_dominant, banner)

NS = [3, 4, 5, 6]
EPS_LEAK = F(1, 5)
EPS_SPEC = EPS_LEAK ** 2 / 2                       # 1/50, the C_3 = 1 budget
C_THRESH = (1 - EPS_LEAK) / (1 - EPS_SPEC)         # 40/49 = 0.816327
rc = 0


def leak_m(n, T, A):
    s = F(0)
    for x in A:
        row = T[x]
        for a in A:
            s += row[a]
    return len(A) - s


def profile(n, rel, exts):
    T = T_matrix(n, exts)
    phi_star = None
    for k in range(1, n // 2 + 1):
        for A in combinations(range(n), k):
            v = leak_m(n, T, A) / k
            phi_star = v if phi_star is None else min(phi_star, v)
    phi_pref = None
    omr_min = None
    rho_max = None
    for k in range(1, n):
        E = leak_m(n, T, list(range(k)))
        v = E / min(k, n - k)
        phi_pref = v if phi_pref is None else min(phi_pref, v)
        omr = F(n) * E / (k * (n - k))
        omr_min = omr if omr_min is None else min(omr_min, omr)
        rho = 1 - omr
        rho_max = rho if rho_max is None else max(rho_max, rho)
    gap, v, vals, vecs = spectral_gap(n, T)
    return dict(T=T, phi_star=phi_star, phi_pref=phi_pref, omr_min=omr_min,
                rho_max=rho_max, gap=gap, prim=is_primitive(n, rel),
                mono=monotone_dominant(n, T))


DATA = {}
for n in NS:
    DATA[n] = []
    for rel in all_posets(n):
        exts = linear_extensions(n, rel)
        DATA[n].append(profile(n, rel, exts))

# --------------------------------------------------------------------------
banner("C0. STRATIFY -- where is 1 - lambda_std = 0?  (mg-76b2 claim 18, re-derived)")
print("""  Three predicates, computed independently of each other:
    (a) 1 - lambda_std = 0            (Jacobi, FLOAT, tol 1e-12)
    (b) P is ordinal-sum decomposable (combinatorial, EXACT)
    (c) Phi* = 0                      (EXACT rational over all cuts)
""")
print(f"{'n':>3} {'posets':>8} {'gap=0':>7} {'decomp':>7} {'Phi*=0':>7} {'disagree':>9}")
dis = 0
for n in NS:
    a = [p["gap"] < 1e-12 for p in DATA[n]]
    b = [not p["prim"] for p in DATA[n]]
    c = [p["phi_star"] == 0 for p in DATA[n]]
    d = sum(1 for i in range(len(a)) if not (a[i] == b[i] == c[i]))
    dis += d
    print(f"{n:>3} {len(DATA[n]):>8} {sum(a):>7} {sum(b):>7} {sum(c):>7} {d:>9}")
print(f"\n  {dis} disagreements over {sum(len(DATA[n]) for n in NS)} posets.")
print("  CLAIM 18 REPRODUCED on three predicates that share no code.  Note what")
print("  this costs the population: every C_3 ratio below is 0/0 on the")
print("  decomposable posets and is therefore measured only on the primitive ones.")
if dis:
    rc = 1

# --------------------------------------------------------------------------
banner("C1. IS ANY POSET HERE INSIDE THE BUDGET?  (mg-76b2 claim 19, re-derived)")
print(f"  Budget: 1 - lambda_std <= eps_spec = {EPS_SPEC} = {float(EPS_SPEC)}\n")
print(f"{'n':>3} {'primitive':>10} {'inside budget':>14} {'smallest gap':>14}")
inside = 0
for n in NS:
    ps = [p for p in DATA[n] if p["prim"]]
    ins = sum(1 for p in ps if p["gap"] <= float(EPS_SPEC))
    inside += ins
    print(f"{n:>3} {len(ps):>10} {ins:>14} {min(p['gap'] for p in ps):>14.4f}")
print(f"\n  {inside} of {sum(1 for n in NS for p in DATA[n] if p['prim'])} primitive")
print("  posets are inside the budget.  EVERY C_3 FIGURE BELOW IS THEREFORE")
print("  MEASURED OUTSIDE THE REGIME IT WOULD BE USED IN -- exactly as mg-76b2")
print("  says of its own, and the same caveat binds this audit's numbers.")

# --------------------------------------------------------------------------
banner("C2/C3. THE THREE CURRENCIES OVER THE PRIMITIVE POPULATION -- P5")
print(f"  c threshold (Op-Form/mg-76b2 H3) = (1-eps_leak)/(1-eps_spec) = "
      f"{C_THRESH} = {float(C_THRESH):.6f}\n")
print(f"{'n':>3} {'max C_3^cut':>12} {'max C_3^gap':>12} {'min c':>9} "
      f"{'c below thresh':>16}")
mine = {}
for n in NS:
    ps = [p for p in DATA[n] if p["prim"]]
    cut = max(p["phi_pref"] / p["phi_star"] for p in ps)
    gapc = max(p["omr_min"] / p["gap"] for p in ps)
    # c = max_k rho(A_k)/lambda_std is 0/0 wherever lambda_std = 0 -- which is
    # exactly the antichain, whose S_P|_H is the zero matrix.  A DEFECT OF MINE,
    # KEPT: the first version of this line divided anyway and printed min c =
    # 0.000 at every n, which is not a small capture fraction, it is an
    # undefined ratio wearing one.  mg-76b2's population is smaller than mine by
    # exactly 1 at every n and this is why -- ITS exclusion is the correct one.
    csrc = [p for p in ps if 1 - p["gap"] > 1e-12]
    cs = [float(p["rho_max"]) / (1 - p["gap"]) for p in csrc]
    below = sum(1 for x in cs if x < float(C_THRESH))
    mine[n] = (cut, gapc, min(cs), below, len(csrc))
    print(f"{n:>3} {str(cut):>12} {gapc:>12.3f} {min(cs):>9.3f} "
          f"{str(below) + '/' + str(len(csrc)):>16}"
          f"   [{len(ps)} primitive, {len(ps) - len(csrc)} dropped as 0/0]")
print("""
  mg-76b2 sec.7 reports, on the same population:
      max C_3^cut  1, 3/2, 6/5, 15/8
      max C_3^gap  1.500, 1.473, 1.990, 2.386
      min c        0.750, 0.618, 0.536, 0.453
      c below      1/3, 5/26, 39/274, 523/4069""")
REF_CUT = {3: F(1), 4: F(3, 2), 5: F(6, 5), 6: F(15, 8)}
REF_GAP = {3: 1.500, 4: 1.473, 5: 1.990, 6: 2.386}
REF_C = {3: 0.750, 4: 0.618, 5: 0.536, 6: 0.453}
REF_BELOW = {3: (1, 3), 4: (5, 26), 5: (39, 274), 6: (523, 4069)}
mismatch = 0
for n in NS:
    cut, gapc, minc, below, npop = mine[n]
    ok_cut = cut == REF_CUT[n]
    ok_gap = abs(gapc - REF_GAP[n]) < 5e-4
    ok_c = abs(minc - REF_C[n]) < 5e-4
    ok_b = (below, npop) == REF_BELOW[n]
    mismatch += sum(1 for x in (ok_cut, ok_gap, ok_c, ok_b) if not x)
    print(f"  n = {n}: cut {ok_cut}   gap {ok_gap}   c {ok_c}   below {ok_b}")
print(f"\n  {16 - mismatch}/16 of mg-76b2's sec.7 figures reproduce on independent code.")
print(f"  P5 (I predicted at least one would NOT reproduce): "
      f"{'MISSED' if mismatch == 0 else 'HELD'}")
print("""
  DIRECTION.  max C_3^cut and max C_3^gap RISE with n; min c FALLS.  A finite
  population can refute a uniform-in-n bound and can never establish one, so
  this is a direction and not a bound -- which is how mg-76b2 reports it too.""")

# --------------------------------------------------------------------------
banner("C4. P4 -- THE ADVERSARIAL PROBE.  Restrict to L2's FIRST DISJUNCT.")
print("""  mg-76b2's theorem is CONDITIONAL on L2's FIRST DISJUNCT.  The honest
  question is not 'is C_3^gap > 1 somewhere', it is 'is C_3^gap > 1 WHERE that
  disjunct holds'.  Restrict to primitive posets with a NON-DEGENERATE top
  standard eigenspace whose eigenvector IS monotone along e -- i.e. posets that
  exhibit L2's first disjunct -- and re-measure.
""")
print(f"{'n':>3} {'prim & L2':>10} {'max C_3^cut':>12} {'max C_3^gap':>12} "
      f"{'C_3^cut>1':>10} {'C_3^gap>1':>10}")
tot_cut_gt = tot_gap_gt = tot_l2 = 0
worst_gap = 0.0
worst_cut = F(1)
for n in NS:
    ps = [p for p in DATA[n] if p["prim"] and p["mono"] == "YES" and p["gap"] > 1e-12]
    if not ps:
        print(f"{n:>3} {0:>10}")
        continue
    cut = max(p["phi_pref"] / p["phi_star"] for p in ps)
    gapc = max(p["omr_min"] / p["gap"] for p in ps)
    ncut = sum(1 for p in ps if p["phi_pref"] > p["phi_star"])
    ngap = sum(1 for p in ps if p["omr_min"] / p["gap"] > 1 + 1e-9)
    tot_l2 += len(ps)
    tot_cut_gt += ncut
    tot_gap_gt += ngap
    worst_gap = max(worst_gap, gapc)
    worst_cut = max(worst_cut, cut)
    print(f"{n:>3} {len(ps):>10} {str(cut):>12} {gapc:>12.3f} {ncut:>10} {ngap:>10}")
print(f"""
  Over {tot_l2} primitive posets that EXHIBIT L2's first disjunct:
      C_3^cut > 1 at {tot_cut_gt} of them, worst {worst_cut}
      C_3^gap > 1 at {tot_gap_gt} of them, worst {worst_gap:.3f}

  P4: {'HELD' if tot_gap_gt else 'MISSED'}.""")
print("""
  WHAT THIS DOES AND DOES NOT SHOW -- and this is exactly the distinction I
  filed against myself as P9 before running anything.

  It does NOT refute mg-76b2's theorem.  The theorem does not say the best
  prefix is the best cut, and it does not say the gap-form C_3 is 1.  It says
  the CHEEGER SWEEP BOUND is delivered AT a prefix, which is a statement about
  sqrt(2(1-lambda_std)) and not about Phi* or about 1-rho.  C_3^cut > 1 and
  C_3^gap > 1 on L2's FIRST DISJUNCT are both COMPATIBLE with it.

  It DOES show that 'C_3 = 1' is true only in the chain-(III) currency, and that
  in the two currencies Op-Form sec.4.3 actually uses to DEFINE the prefix-capture
  readings, the constant is > 1 and rising even on L2's FIRST DISJUNCT.""")

# --------------------------------------------------------------------------
banner("C5. THE THEOREM, MEASURED -- chain (III) at C_3 = 1, on L2's FIRST DISJUNCT")
print("""  For every primitive poset exhibiting L2's first disjunct: is there a
  PREFIX A_k with Phi_P(A_k) <= sqrt(2(1-lambda_std))?  That -- and only that --
  is what 'C_3 = 1' means in the currency the ticket's relation uses.
""")
ok = bad = 0
worst_ratio = 0.0
for n in NS:
    for p in DATA[n]:
        if not (p["prim"] and p["mono"] == "YES" and p["gap"] > 1e-12):
            continue
        lhs = float(p["phi_pref"])
        rhs = math.sqrt(2 * p["gap"])
        if lhs <= rhs + 1e-9:
            ok += 1
            worst_ratio = max(worst_ratio, lhs * lhs / (2 * p["gap"]))
        else:
            bad += 1
print(f"  posets checked                   : {ok + bad}")
print(f"  Phi*_pref <= sqrt(2(1-lambda_std)): {ok}")
print(f"  violations                       : {bad}")
print(f"  worst Phi*_pref^2/(2(1-lambda_std)): {worst_ratio:.4f}")
print(f"""
  P8: mg-76b2's constant in the chain-(III) currency comes out at
  {'1 -- CONFIRMED' if bad == 0 else 'NOT 1 -- REFUTED'} on this population, under L2's FIRST DISJUNCT's hypothesis.

  AND THE SAME CHECK WITHOUT L2, as a red drill -- if it passes there too, the
  hypothesis is not doing work and the theorem is weaker than it looks:""")
ok2 = bad2 = 0
for n in NS:
    for p in DATA[n]:
        if not (p["prim"] and p["mono"] == "NO" and p["gap"] > 1e-12):
            continue
        if float(p["phi_pref"]) <= math.sqrt(2 * p["gap"]) + 1e-9:
            ok2 += 1
        else:
            bad2 += 1
print(f"  non-monotone primitive posets    : {ok2 + bad2}")
print(f"  satisfying the same inequality   : {ok2}")
print(f"  violating it                     : {bad2}")
print("""
  READ THIS CAREFULLY.  The inequality holds on the non-monotone posets too, on
  THIS population.  That does NOT make the hypothesis idle: sqrt(2 eps) is a
  weak bound at eps ~ 0.3, which is where this whole population lives, and no
  poset here is inside the budget (C1).  It DOES mean the population supplies
  no separating evidence for the theorem, and mg-76b2 should not be read as
  having any -- its support is the PROOF, and the proof is what this audit
  re-derived in a2 sections C-F.  A reader who took sec.7's monotonicity
  correlation as evidence FOR the theorem would be reading it wrongly, and
  mg-76b2 labels that table HEURISTIC for this reason.""")

banner("EXIT")
print(f"rc = {rc}")
raise SystemExit(rc)
