#!/usr/bin/env python3
"""s0 — CONTROLS.  Nothing in s1/s2/s3 is worth reading until this passes.

This ticket's whole job is to CHECK a number somebody else measured, so the controls
that matter are the ones that would fire if this instrument silently agreed with
`mg-76b2` for the wrong reason, or disagreed with it for a reason of its own.

  (A) POPULATION.  The extension enumeration against the 2^C(n,2) transitive-closure
      enumeration, as SETS of posets, n <= 5 — and the counts against mg-76b2's
      published 2, 7, 40, 357, 4824.
  (B) TRANSPORT.  The down-set DP against the n! path, EVERY poset n <= 6.
  (C) MUTATION on (B).  The peeling predicate this file got wrong on its first run is
      re-installed and must FAIL — so (B) cannot rot into a tautology.
  (D) MUTATION on the Rayleigh reading.  An UNCENTRED prefix indicator must give
      different numbers, so `c` is pinned to the centred reading and not merely
      described as it.
  (E) THE IDENTITY.  rho(A_k) computed from M directly, against 1 - Q_k computed from
      the Laplacian.  This is the control for the class of slip this file's own
      docstring made (`c = (1-minQ)/lambda_2` for `(1-minQ)/(1-lambda_2)`).
  (F) EXACT vs FLOAT.  The Sylvester bracket must contain the Jacobi value, every
      poset n <= 6; and a deliberately wrong q must be REJECTED by `lambda2_gt`.
  (G) THE STRATIFICATION.  mg-76b2 s3 (C0)'s DISC <=> CUT <=> (Phi* = 0), re-verified
      here at n <= 6 on this instrument's own predicates, and EXTENDED to n = 7.
  (H) THE HEADLINE ROW.  mg-76b2's `min c` at n = 3..6 reproduced EXACTLY.  This is
      the ticket's sequencing directive and it is a control, not a result: if it fails,
      nothing downstream is about mg-76b2's object.
"""

from fractions import Fraction as F
import sys

from lib81ff import (Poset, all_posets, all_posets_bymask, poset_from_relations,
                     h_basis, jacobi)

fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")
    else:
        print(f"    ok:   {msg}")
    return cond


print("=" * 78)
print("s0 — CONTROLS")
print("=" * 78)

# ------------------------------------------------------------------ (A)
print()
print("-" * 78)
print("(A) POPULATION — extension enumeration vs the 2^C(n,2) route")
print("-" * 78)
PUBLISHED = {2: 2, 3: 7, 4: 40, 5: 357, 6: 4824}     # mg-76b2 s3 (C0)
for n in range(2, 6):
    a = {P.down for P in all_posets(n)}
    b = {P.down for P in all_posets_bymask(n)}
    check(a == b, f"n={n}: the two enumerations give the SAME set ({len(a)} posets)")
for n in range(2, 7):
    check(len(all_posets(n)) == PUBLISHED[n],
          f"n={n}: population {len(all_posets(n))} == mg-76b2's {PUBLISHED[n]}")

# ------------------------------------------------------------------ (B)
print()
print("-" * 78)
print("(B) TRANSPORT — down-set DP vs the n! path, EVERY poset n <= 6")
print("-" * 78)
tot = bad = 0
for n in range(2, 7):
    for P in all_posets(n):
        tot += 1
        if P.transport() != P.transport_factorial():
            bad += 1
check(bad == 0, f"{tot} posets, {bad} mismatches between the DP and the n! path")

# ------------------------------------------------------------------ (C)
print()
print("-" * 78)
print("(C) MUTATION on (B) — the peeling predicate this file got wrong, re-installed")
print("-" * 78)
print("    The mutant peels i from the down-set S whenever `down[i] <= S\\{i}`.  That is")
print("    TRUE OF EVERY i IN S, minimal elements included, because S is already")
print("    down-closed — so the mutant offers subsets that are not down-sets at all.")
print()
print("    THIS CONTROL WAS BUILT WRONG FIRST AND THE FIRST RUN SAID SO.  I wrote it to")
print("    assert the mutant gives WRONG NUMBERS.  It does not: guarded with `.get(...,0)`")
print("    the bogus states contribute nothing and the mutant is NUMERICALLY CORRECT at")
print("    every poset here — which is exactly the defect mg-9461's own s0 (C) records,")
print("    arrived at independently.  So the control asserts BOTH halves, as that one")
print("    does: the numbers agree AND the state count exceeds the down-set lattice.")
print("    A numbers-only check at any n could not have seen this.")


def transport_mutant(P):
    """(B)'s DP with the wrong maximality test.

    Returns (linear-extension count, peel attempts, peels onto a genuine down-set).
    """
    n, ds = P.n, P.downsets()
    full = (1 << n) - 1
    e = {}
    tried = real = 0
    for S in ds:
        if S == 0:
            e[S] = 1
            continue
        tot_ = 0
        x = S
        while x:
            b = x & -x
            i = b.bit_length() - 1
            if not (P.down[i] & ~(S ^ b)):        # the WRONG test — always True
                tried += 1
                if P.is_downset(S ^ b):
                    real += 1
                tot_ += e.get(S ^ b, 0)           # bogus states contribute 0
            x ^= b
        e[S] = tot_
    return e[full], tried, real


numeric_diff = 0
seen = tried_tot = real_tot = 0
for n in range(2, 6):
    for P in all_posets(n):
        seen += 1
        val, tried, real = transport_mutant(P)
        tried_tot += tried
        real_tot += real
        if val != P.n_linear_extensions():
            numeric_diff += 1
check(numeric_diff == 0,
      f"the mutant is NUMERICALLY CORRECT on all {seen} posets n<=5 — so (B) alone "
      f"cannot catch it")
check(tried_tot > real_tot,
      f"the mutant offers {tried_tot} peels where only {real_tot} land on a down-set "
      f"— {tried_tot - real_tot} bogus states ({100*(tried_tot-real_tot)/tried_tot:.1f}%), "
      f"which is what catches it")

# ------------------------------------------------------------------ (D)
print()
print("-" * 78)
print("(D) MUTATION on the Rayleigh reading — UNCENTRED prefix indicator")
print("-" * 78)
print("    `rho(A_k)` is the Rayleigh quotient of the CENTRED indicator f = 1_A - (k/n)1,")
print("    which is the only reading that lands in H = 1^perp.  An uncentred 1_A gives a")
print("    different number and this control exhibits the difference rather than")
print("    asserting the convention in prose.")
diff = 0
seenD = 0
for n in range(3, 6):
    for P in all_posets(n):
        for k in range(1, n):
            seenD += 1
            f_un = [F(1) if i < k else F(0) for i in range(n)]
            q_un = P.energy(f_un) / sum(x * x for x in f_un)
            if q_un != P.prefix_Q(k):
                diff += 1
check(diff > 0,
      f"centred and uncentred disagree on {diff} of {seenD} (poset, k) pairs n<=5")

# ------------------------------------------------------------------ (E)
print()
print("-" * 78)
print("(E) THE IDENTITY — rho(A_k) from M directly vs 1 - Q_k from the Laplacian")
print("-" * 78)
print("    This is the control for the class of slip this file's own module docstring")
print("    made: `c = (1-minQ)/lambda_2` where the truth is `(1-minQ)/(1-lambda_2)`.")
badE = totE = 0
for n in range(3, 7):
    for P in all_posets(n):
        M = P.M()
        for k in range(1, n):
            totE += 1
            f = [F(n - k, n) if i < k else F(-k, n) for i in range(n)]
            num = sum(f[i] * M[i][j] * f[j] for i in range(n) for j in range(n))
            rho_direct = num / F(k * (n - k), n)
            if rho_direct != 1 - P.prefix_Q(k):
                badE += 1
check(badE == 0, f"{totE} (poset, k) pairs: rho from M == 1 - Q_k from L, {badE} mismatches")

# ------------------------------------------------------------------ (F)
print()
print("-" * 78)
print("(F) EXACT vs FLOAT — Sylvester bracket vs Jacobi, and a NEGATIVE control")
print("-" * 78)
badF = totF = 0
for n in range(3, 7):
    for P in all_posets(n):
        totF += 1
        lo, hi = P.lambda2_bracket(F(1, 10 ** 9))
        lam2, _ = P.fiedler()
        if not (float(lo) - 1e-6 <= lam2 <= float(hi) + 1e-6):
            badF += 1
check(badF == 0, f"{totF} posets: the exact bracket contains the Jacobi value, {badF} failures")

print()
print("    NEGATIVE CONTROL — `lambda2_gt` must REJECT a q above lambda_2 and ACCEPT one")
print("    below it, on a poset whose lambda_2 is known independently.")
Pn = poset_from_relations(4, [(0, 1), (2, 3)])
lo, hi = Pn.lambda2_bracket(F(1, 10 ** 9))
check(Pn.lambda2_gt(lo - F(1, 100)),
      f"lambda2_gt(lo - 1/100) is True  [lambda_2 ~ {float(lo):.6f}]")
check(not Pn.lambda2_gt(hi + F(1, 100)),
      f"lambda2_gt(hi + 1/100) is False [lambda_2 ~ {float(hi):.6f}]")
check(not Pn.lambda2_gt(F(1)), "lambda2_gt(1) is False — lambda_2 <= 1 on this population")

# ------------------------------------------------------------------ (G)
print()
print("-" * 78)
print("(G) THE STRATIFICATION — mg-76b2 s3 (C0)'s DISC <=> CUT, re-verified and EXTENDED")
print("-" * 78)
print("    `lambda_std = 0` iff the weighted graph a_ij is disconnected iff the poset has")
print("    an ordinal-sum cut point.  mg-76b2 verified this at n <= 6; n = 7 is new here.")
print()
print("     n   posets     DISC      CUT   agree")
for n in range(2, 8):
    d = c_ = agree = 0
    for P in all_posets(n):
        dd = not P.connected()
        cc = bool(P.cut_points())
        d += dd
        c_ += cc
        agree += (dd == cc)
    print(f"  {n:4d} {len(all_posets(n)):8d} {d:8d} {c_:8d} {agree:7d}")
    check(agree == len(all_posets(n)), f"n={n}: DISC == CUT on all {agree} posets")

# ------------------------------------------------------------------ (H)
print()
print("-" * 78)
print("(H) THE HEADLINE ROW — mg-76b2 s3 (C3)'s `min c` at n = 3..6, reproduced")
print("-" * 78)
print("    THIS IS THE TICKET'S SEQUENCING DIRECTIVE, RUN AS A CONTROL.  If these four")
print("    figures do not come back exactly, nothing downstream is about mg-76b2's object.")
MG76B2_MIN_C = {3: 0.750000, 4: 0.618034, 5: 0.536219, 6: 0.452934}
MG76B2_PRIM = {3: 4, 4: 27, 5: 275, 6: 4070}
print()
print("     n   primitive   with lam_std>0    min c        mg-76b2   ")
for n in range(3, 7):
    prim = [P for P in all_posets(n) if P.is_primitive()]
    vals = [(P.float_c(), P) for P in prim]
    vals = [(c, P) for c, P in vals if c is not None]
    mn = min(vals, key=lambda t: t[0])
    print(f"  {n:4d} {len(prim):10d} {len(vals):15d}   {mn[0]:.6f}     {MG76B2_MIN_C[n]:.6f}")
    check(len(prim) == MG76B2_PRIM[n],
          f"n={n}: primitive count {len(prim)} == mg-76b2's {MG76B2_PRIM[n]}")
    check(abs(mn[0] - MG76B2_MIN_C[n]) < 5e-7,
          f"n={n}: min c {mn[0]:.6f} == mg-76b2's {MG76B2_MIN_C[n]:.6f}")

print()
print("=" * 78)
print(f"s0 VERDICT: {'ALL CONTROLS PASS' if fail == 0 else str(fail) + ' FAILURES'}")
print("=" * 78)
sys.exit(1 if fail else 0)
