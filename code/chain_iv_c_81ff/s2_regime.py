#!/usr/bin/env python3
"""s2 — THE SCOPE.  s1's refutation is measured OUTSIDE the regime chain (IV) is used in.

`c` is not a number attached to the poset population at large.  It is invoked at ONE
place in the architecture: after Step 2 has supplied `lambda_std >= 1 - eps`, i.e. on
posets whose spectral gap is at most `eps_spec`.  Every poset in s1's refuting family
has gap >= 0.46, which is 23x to 33x outside that.  So s1 settles a question chain (IV)
does not ask, and this script asks the one it does:

  (R1) DOES `c` FALL BECAUSE `n` GROWS, OR BECAUSE THE GAP IS LARGE?  Stratify.
  (R2) THE ARCHITECTURE'S ACTUAL REQUIREMENT, written without `c` at all, and the
       envelope of it over {gap <= eps}.
  (R3) IS THE REGIME EVEN REACHABLE?  mg-76b2 (C1) reports `0 of 4377 inside the
       budget` — a statement about n <= 6, not an emptiness theorem.  An explicit
       primitive family INSIDE `eps_spec = 2e-2` is exhibited here, exactly.
  (R4) WHAT IS STILL NOT SETTLED, said in the terms the ticket asks for: how many
       INFORMATIVE points, and in which direction they run.
"""

from fractions import Fraction as F

from lib81ff import (all_posets, poset_from_relations, C_THRESH_SELF, C_THRESH_EXIST,
                     EPS_LEAK, EPS_SPEC)

print("=" * 78)
print("s2 — THE SCOPE: `c` IN THE REGIME THE ARCHITECTURE ACTUALLY SUPPLIES")
print("=" * 78)
print()
print(f"  Step 2 supplies   1 - lambda_std <= eps_spec = eps_leak^2/2 = {EPS_SPEC} = {float(EPS_SPEC)}")
print(f"  Step 5 requires   Phi_P(A_k)     <= eps_leak            = {EPS_LEAK} = {float(EPS_LEAK)}")
print("  s1's refuting family D_k has gap 0.46 .. 0.66.  It is not in the class.")
print()

# collect (gap, c, minQ) once
data = {}
for n in range(3, 8):
    rows = []
    for P in all_posets(n):
        if not P.is_primitive():
            continue
        c = P.float_c()
        if c is None:
            continue
        lam2, _ = P.fiedler()
        mq, _k = P.min_prefix_Q()
        rows.append((lam2, c, float(mq), P))
    data[n] = rows

# --------------------------------------------------------------------- (R1)
print("-" * 78)
print("(R1) `min c` STRATIFIED BY GAP — is the fall about n, or about the gap?")
print("-" * 78)
print()
BANDS = [(0.0, 0.06), (0.06, 0.10), (0.10, 0.20), (0.20, 0.30),
         (0.30, 0.50), (0.50, 0.70), (0.70, 1.01)]
print("  n=6                                    n=7")
print("  gap band          posets   min c       posets   min c")
for b in BANDS:
    line = f"  [{b[0]:.2f}, {b[1]:.2f})   "
    for n in (6, 7):
        sub = [r for r in data[n] if b[0] <= r[0] < b[1]]
        line += (f"  {len(sub):6d}  {min(sub, key=lambda t: t[1])[1]:.6f}   "
                 if sub else "       0      --      ")
    print(line)
print()
print("  Across the six bands below 0.70, `min c` RISES as the band tightens, at BOTH n,")
print("  and the band nearest the regime is the band where c is LARGEST.  s1's minimisers")
print("  live in [0.50, 0.70).")
print()
print("  *** ERRATUM (mg-b3ab, after mg-00b3's audit).  THIS LINE USED TO READ `rises")
print("  MONOTONICALLY as the band tightens`, and `THE FALL IS THE GAP, NOT n`.  Both are")
print("  over-stated and both are repaired here.")
print("    (a) THE DIRECTION IS ROBUST; THE MONOTONICITY IS A PROPERTY OF THIS PARTITION.")
print("        Re-bin the SAME population at uniform width 0.01 and 32 of 63 adjacent")
print("        pairs violate at n = 6, 32 of 73 at n = 7 — and not only in the")
print("        near-antichain tail printed below: 10 (n=6) and 7 (n=7) have BOTH bands")
print("        under gap 0.30.  Largest such rise: n = 6, [0.130,0.140) 0.824256 ->")
print("        [0.140,0.150) 0.874508.  (mg-00b3 sec 0.2, independent instrument.)")
print("    (b) `NOT BECAUSE n IS` is contradicted by (R4) BELOW, on this instrument: at a")
print("        FIXED gap cap, min c falls as n grows.  The gap carries the direction; it")
print("        does not clear n.  Both effects are live. ***")
print()
print("  THE TOP BAND [0.70, 1.01) RUNS THE OTHER WAY AND IS PRINTED, NOT DROPPED:")
print("  min c there is 0.673 (n=6) and 0.556 (n=7), ABOVE the band below it.  It holds")
print("  14 and 38 posets — the near-antichain end, where lambda_std is nearly 0 and c is")
print("  a ratio of two small numbers.  It is the farthest band from the regime and it")
print("  does not disturb the reading, but a table that omitted it would be choosing its")
print("  rows to fit the sentence.")
print()

# --------------------------------------------------------------------- (R2)
print("-" * 78)
print("(R2) THE REQUIREMENT WITHOUT `c`, AND ITS ENVELOPE OVER {gap <= eps}")
print("-" * 78)
print()
print("  Chain (IV) delivers Phi_P(A_k) <= 1 - rho(A_k) = min_k Q_k (mg-76b2 Lemma 2.1),")
print("  and Step 5 needs that <= eps_leak.  So, stripped of every constant:")
print()
print("      CHAIN (IV) CLOSES ON A POSET  <=>  min_k Q_k <= eps_leak = 1/5.")
print()
print("  `c >= 40/49` is exactly this condition re-parametrised at gap = eps_spec:")
print("      c >= (1-eps_leak)/(1-eps_spec)  <=>  1 - min_k Q_k >= 1 - eps_leak")
print("                                      <=>  min_k Q_k <= eps_leak.   [ALGEBRA]")
print()
EPS_CAPS = [1.0, 0.30, 0.20, 0.10, 0.08, 0.06, 0.04]
print("  max min_k Q_k over {gap <= eps}   [chain (IV) closes iff this stays <= 0.2]")
print("   eps    " + "".join(f"    n={n}  " for n in range(4, 8)))
for e in EPS_CAPS:
    line = f"  {e:<5.2f} "
    for n in range(4, 8):
        sub = [r[2] for r in data[n] if r[0] <= e]
        line += f"  {max(sub):.5f}" if sub else "     --   "
    print(line)
print()
print("  and the same table as `min c`, which is the ticket's own currency:")
print("   eps    " + "".join(f"    n={n}  " for n in range(4, 8)))
for e in EPS_CAPS:
    line = f"  {e:<5.2f} "
    for n in range(4, 8):
        sub = [r[1] for r in data[n] if r[0] <= e]
        line += f"  {min(sub):.5f}" if sub else "     --   "
    print(line)
print()
smallest = {n: min(r[0] for r in data[n]) for n in data}
print("  smallest gap reached, by n: " +
      ", ".join(f"n={n}: {smallest[n]:.6f}" for n in sorted(smallest)))
print(f"  the budget is {float(EPS_SPEC)}.  NO poset at n <= 7 reaches it — mg-76b2 (C1)'s")
print("  `0 of 4377` at n <= 6, reproduced and extended: 0 of 86 277 at n = 7 too.")
print()

# --------------------------------------------------------------------- (R3)
print("-" * 78)
print("(R3) THE REGIME IS REACHABLE — AND HERE IT IS, EXACTLY")
print("-" * 78)
print()
print("  `0 of 4377 inside the budget` is a statement ABOUT n <= 6.  It has been read in")
print("  this corpus as though the regime were structurally empty; it is not, it is only")
print("  out of enumeration range.  The family below is primitive, is inside the budget")
print("  from n = 10, and every figure is an exact rational bracket.")
print()
print("      N_a(n):  antichain {0..a-1}  <  antichain {a..n-1},  a = n/2,")
print("               MINUS the single relation (a-1, a).")
print()
print("   n   primitive   gap (exact)      gap <= 1/50?   min_k Q_k    c (exact bracket)")
minQ_N = {}
for n in range(6, 17, 2):
    a = n // 2
    rel = [(x, y) for x in range(a) for y in range(a, n) if (x, y) != (a - 1, a)]
    P = poset_from_relations(n, rel)
    lo, hi = P.lambda2_bracket(F(1, 10 ** 12))
    clo, chi = P.c_bracket(F(1, 10 ** 12))
    mq, _k = P.min_prefix_Q()
    minQ_N[n] = mq
    inside = not P.lambda2_gt(EPS_SPEC)
    print(f"  {n:3d}   {str(P.is_primitive()):5s}    {float(lo):.9f}    "
          f"{'YES' if inside else 'no ':>3s}         {str(mq):>7s}   "
          f"[{float(clo):.7f}, {float(chi):.7f}]")
print()
print("  IN THE REGIME, `c` GOES TO 1, NOT TO 0.  At n = 16 the gap is 3.7e-3 — five")
print("  times inside the budget — and c = 0.99990, against a threshold of 0.8163.")
print("  min_k Q_k there is 1/260, against a requirement of 1/5: a factor of 52 of slack.")
print()
print("  *** ERRATUM (mg-b3ab, after mg-00b3's audit).  THE TABLE BELOW USED TO BE HEADED")
print("  `A SECOND FAMILY, so the answer is not one construction's artefact`.  IT IS NOT A")
print("  SECOND FAMILY.  N and N' are the SAME poset under two labellings: both are")
print("  K_{a,a} minus ONE relation, and Aut(K_{a,a}) is transitive on its a^2 relations,")
print("  so ANY two single-relation deletions are isomorphic.  An explicit isomorphism at")
print("  every n is exhibited and CHECKED below, not asserted.  N' IS NOT INDEPENDENT")
print("  EVIDENCE: the class exhibited in the regime is ONE poset shape. ***")
print()
print("  *** AND THE STRUCTURAL POINT, which is why this was not visible on its face:")
print("  sec 1.2 establishes that chain (IV) closes IFF min_k Q_k <= eps_leak, and THIS")
print("  TABLE USED TO OMIT THAT COLUMN, printing gap and c alone.  Had it been here, a")
print("  reader would have seen the SAME 1/15 .. 1/260 twice over and asked why two")
print("  `different` families agree exactly in the one number that decides closing.  The")
print("  column is restored, and the equality is now ASSERTED rather than left to the eye.")
print("  The n = 6 row is also restored: the old table started at n = 8, so the two could")
print("  not be read side by side even where both were printed. ***")
print()
print("      N'_a(n): the same, MINUS the relation (0, n-1) instead.")
print("   n   primitive   gap (exact)      gap <= 1/50?   min_k Q_k    c (exact bracket)"
      "   min_k Q_k == N's?   sigma(N) == N'?")
for n in range(6, 17, 2):
    a = n // 2
    rel_N = [(x, y) for x in range(a) for y in range(a, n) if (x, y) != (a - 1, a)]
    rel = [(x, y) for x in range(a) for y in range(a, n) if (x, y) != (0, n - 1)]
    P = poset_from_relations(n, rel)
    lo, _hi = P.lambda2_bracket(F(1, 10 ** 12))
    clo, chi = P.c_bracket(F(1, 10 ** 12))
    mq, _k = P.min_prefix_Q()
    inside = not P.lambda2_gt(EPS_SPEC)
    # Explicit isomorphism N -> N', valid at every n: swap (a-1, 0) inside the lower
    # block and (a, n-1) inside the upper block.  Both blocks are preserved setwise, so
    # sigma is an automorphism of K_{a,a}; it carries the deleted relation (a-1, a) to
    # the deleted relation (0, n-1).  This is Aut(K_{a,a})-transitivity made concrete.
    sigma = list(range(n))
    sigma[a - 1], sigma[0] = 0, a - 1
    sigma[a], sigma[n - 1] = n - 1, a
    iso = sorted((sigma[x], sigma[y]) for x, y in rel_N) == sorted(rel)
    assert iso, f"the exhibited sigma is not an isomorphism at n = {n}"
    assert mq == minQ_N[n], f"min_k Q_k differs at n = {n}: {mq} vs {minQ_N[n]}"
    print(f"  {n:3d}   {str(P.is_primitive()):5s}    {float(lo):.9f}    "
          f"{'YES' if inside else 'no ':>3s}         {str(mq):>7s}   "
          f"[{float(clo):.7f}, {float(chi):.7f}]"
          f"      {str(mq == minQ_N[n]):5s}            {str(iso):5s}")
print()
print("  BOTH COLUMNS ARE True AT EVERY n.  The two labellings differ ONLY in the gap,")
print("  and hence only in c, because M mixes the element index with the POSITION index")
print("  and so is not relabelling-invariant.  min_k Q_k — the quantity sec 1.2 shows")
print("  decides closing — is IDENTICAL, which is what `one poset` means here.")
print()
print("  NEGATIVE CONTROL, so the isomorphism check above is not vacuous: the same test")
print("  run against a deletion that is NOT a single relation of K_{a,a} must FAIL.")
for n in (6, 8, 10):
    a = n // 2
    rel_N = [(x, y) for x in range(a) for y in range(a, n) if (x, y) != (a - 1, a)]
    # delete TWO relations: not in the Aut-orbit of a single deletion
    rel_bad = [(x, y) for x in range(a) for y in range(a, n)
               if (x, y) not in ((0, n - 1), (0, a))]
    sigma = list(range(n))
    sigma[a - 1], sigma[0] = 0, a - 1
    sigma[a], sigma[n - 1] = n - 1, a
    bad_iso = sorted((sigma[x], sigma[y]) for x, y in rel_N) == sorted(rel_bad)
    P_bad = poset_from_relations(n, rel_bad)
    mq_bad, _k = P_bad.min_prefix_Q()
    assert not bad_iso, f"negative control did not fire at n = {n}"
    print(f"    n = {n:2d}   sigma(N) == K_{{a,a}} minus TWO: {str(bad_iso):5s}   "
          f"min_k Q_k {str(mq_bad):>7s} vs N's {str(minQ_N[n]):>7s}   "
          f"equal: {str(mq_bad == minQ_N[n]):5s}")
print("  The control FIRES at every n: both tests are False, so True above is a result.")
print()

# --------------------------------------------------------------------- (R4)
print("-" * 78)
print("(R4) WHAT IS NOT SETTLED, AND HOW MANY INFORMATIVE POINTS THERE ARE")
print("-" * 78)
print()
print("  NOT SETTLED: whether `c >= 40/49` holds for EVERY poset in the regime.  The")
print("  regime is empty at every n this or any enumeration reaches (0 of 86 277 at")
print("  n = 7), so the class cannot be swept; the evidence for it is two constructed")
print("  families, which is 2 points and not a population.")
print()
print("  THE ONE READING THAT RUNS AGAINST IT, stated because it is the one a reader")
print("  would otherwise find later: at a FIXED gap cap, `min c` falls as n grows —")
print("  0.974 -> 0.869 -> 0.859 at eps = 0.10 for n = 5, 6, 7, and 0.989 -> 0.881 at")
print("  eps = 0.06 for n = 6, 7.  That is TWO and THREE informative points respectively,")
print("  it is confounded with population size (a min over more posets falls for free),")
print("  and every value is still above both thresholds.  IT IS NOT EVIDENCE THAT c")
print("  DROPS BELOW THE THRESHOLD IN THE REGIME, AND IT IS NOT EVIDENCE THAT IT DOES")
print("  NOT.  Four points killed 2/(n+1); three points decide nothing here either.")
print()
print("=" * 78)
print("s2 VERDICT: s1's REFUTATION DOES NOT TRANSFER.  `min c` rises as the gap tightens,")
print("at both n, across the six bands below 0.70; the ONE poset shape exhibited here in")
print("the architecture's own regime — N and N' are two labellings of it, NOT two")
print("families — has c = 0.999+, five times inside the budget.  `c > 0.80` is REFUTED on")
print("the full population and UNMEASURED — not unmeasurable — in the regime.")
print("(ERRATUM mg-b3ab: this line used to read `falls because the GAP is large, not")
print("because n is` and `the two families`.  The gap carries the direction and does not")
print("clear n — (R4) above measures min c falling with n at a FIXED gap cap — and the")
print("monotonicity across the six bands is a property of THIS partition; see (R1).)")
print("=" * 78)
