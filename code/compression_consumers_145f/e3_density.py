"""e3 -- residual (R), the density ceiling.  The one target in the programme whose
deliverable is a CRUDE CONSTANT rather than a rate, which is the shape the ticket says this
machinery gives away cheaply.

    (R)  is there a constant D < 1 with d(P) = m / C(n,2) <= D on every FROZEN poset?
         (mg-210d; reopened quantitatively by mg-88bd as D <= eps_spec, STATE.md:183-185)

If (R) held, mg-210d's chain gives  1 - lambda_std < D  immediately -- and STATE.md:17 says a
constant is exactly what the architecture consumes.  So (R) passes the ticket's tests 2 and 3
outright.  This arm asks test 1: can the identity bound d(P) from above?

THE ONLY DENSITY-FACING RELATION THE IDENTITY SUPPLIES, and it is saturated at d = 1.

    sum over ALL pairs {x,y} of A_xy = n - 1      EXACTLY, at every poset
    hence  sum over INCOMPARABLE pairs of A_xy <= n - 1

and on the antichain -- where d = 1 -- the incomparable sum IS n - 1.  A relation that a
density-1 poset satisfies with equality cannot certify d <= D < 1.

The relation also needs no foliation: each of the n-1 adjacent position slots holds exactly
one pair, so the adjacency probabilities of all pairs sum to n-1 by counting.  Checked here
against the fiber machinery so the claim is not merely asserted.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib145f as L  # noqa: E402

ok = True

POP = ([(3, p) for p in L.all_posets(3)]
       + [(4, p) for p in L.all_posets(4)]
       + [(5, p) for p in L.sample_posets(5, 60, 31)]
       + [(6, p) for p in L.sample_posets(6, 30, 37)])

# ---------------------------------------------------------------------------------------
L.banner("e3.1  sum of A_xy over ALL pairs is exactly n - 1, at every poset")
bad = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    A = L.all_pair_adjacency(n, LEs)
    if sum(A.values()) != Fraction(n - 1):
        bad += 1
ok &= L.verdict(bad == 0, "sum_{all pairs} A_xy = n - 1", f"{bad} failures / {len(POP)}")

# ---------------------------------------------------------------------------------------
L.banner("e3.2  and A^o + A^e reproduces it on the incomparable pairs")
print("  The identity emits A^o and A^e separately; their sum over incomparable pairs is the")
print("  incomparable share of the n-1 budget.  Checked against a direct adjacency count.")
bad = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    A = L.all_pair_adjacency(n, LEs)
    inc = set(L.incomparable_pairs(n, lt))
    lhs = sum(A_o[p] + A_e[p] for p in inc)
    rhs = sum(A[p] for p in inc)
    if lhs != rhs or lhs > Fraction(n - 1):
        bad += 1
ok &= L.verdict(bad == 0, "A^o + A^e = Pr[adjacent] on incomparable pairs, and sums to <= n-1",
                f"{bad} failures / {len(POP)}")

# ---------------------------------------------------------------------------------------
L.banner("e3.3  THE SATURATION: the antichain has d = 1 and sits ON the bound")
print(f"  {'n':>3} {'d(P)':>8} {'sum_{x||y} A_xy':>18} {'n-1':>6} {'slack':>8}")
tight = True
for n in (3, 4, 5, 6, 7):
    lt = L.antichain(n)
    LEs = L.linear_extensions(n, lt)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    s = sum(A_o[p] + A_e[p] for p in A_o)
    d = L.density(n, lt)
    tight &= (s == Fraction(n - 1) and d == 1)
    print(f"  {n:>3} {str(d):>8} {str(s):>18} {n - 1:>6} {str(Fraction(n - 1) - s):>8}")
ok &= L.verdict(tight, "at d = 1 the identity's density-facing relation holds with EQUALITY",
                "so no D < 1 follows from it")

# ---------------------------------------------------------------------------------------
L.banner("e3.4  and the relation is FOLIATION-FREE -- pure slot counting")
print("  Each linear extension has exactly n-1 adjacent position slots and each slot holds")
print("  exactly one pair, so sum_{all pairs} A_xy = n-1 by counting alone.  Confirmed by")
print("  computing the same number without touching a fiber, a projection or a block system.")
bad = 0
for (n, lt) in POP[:80]:
    LEs = L.linear_extensions(n, lt)
    # SECOND ROUTE: iterate over PAIRS and test |pos(x) - pos(y)| == 1.  The primary route
    # in lib145f iterates over SLOTS.  Neither touches odd_blocks / even_blocks / fibers.
    by_pair = Fraction(0)
    for x in range(n):
        for y in range(x + 1, n):
            hits = sum(1 for Lx in LEs if abs(Lx.index(x) - Lx.index(y)) == 1)
            by_pair += Fraction(hits, len(LEs))
    A = L.all_pair_adjacency(n, LEs)
    if by_pair != sum(A.values()) or by_pair != Fraction(n - 1):
        bad += 1
ok &= L.verdict(bad == 0, "a pair-indexed second route reproduces n-1 with no foliation "
                          "anywhere in either path", f"{bad} failures / 80")

# a control on the control: the pair-indexed route must NOTICE a corrupted slot count
n0, lt0 = 4, next(iter(L.all_posets(4)))
LEs0 = L.linear_extensions(n0, lt0)
corrupt = sum(Fraction(sum(1 for Lx in LEs0 if abs(Lx.index(x) - Lx.index(y)) == 2),
                       len(LEs0))
              for x in range(n0) for y in range(x + 1, n0))
ok &= L.verdict(corrupt != Fraction(n0 - 1),
                "C  distance-2 in place of distance-1 does NOT give n-1",
                f"{L.fr(corrupt)} vs {n0 - 1}")

# ---------------------------------------------------------------------------------------
L.banner("e3.5  WHAT THE RELATION DOES SAY -- and it is step8.tex Step 1, re-derived")
print("  inv_e is itself a pair-orientation linear statistic (all c = 1), so the identity")
print("  DOES compute E_BK(inv_e) = (1/(2(n-1))) sum_{x||y} A_xy <= 1/2.  That is exactly")
print("  mg-409a's L3 / step8.tex Step 1, 'sum_{x||y} E_BK(f_xy) <= 1/2', reached here by a")
print("  different route on an implementation that has never seen it.")
bad = 0
mx = Fraction(0)
tot = 0
for (n, lt) in POP:
    LEs = L.linear_extensions(n, lt)
    inc = L.incomparable_pairs(n, lt)
    if not inc:
        continue
    f = L.pair_orientation_stat(LEs, {p: Fraction(1) for p in inc})
    e_inv = L.bk_energy(f, LEs, n, lt)
    s = sum(L.bk_energy(L.pair_orientation_stat(LEs, {p: Fraction(1)}), LEs, n, lt)
            for p in inc)
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    pred = sum(A_o[p] + A_e[p] for p in A_o) / (2 * (n - 1))
    bad += (e_inv != s) + (e_inv != pred)
    mx = max(mx, e_inv)
    tot += 1
ok &= L.verdict(bad == 0, "E_BK(inv_e) = sum_{x||y} E_BK(f_xy) = (1/(2(n-1))) sum A_xy",
                f"{bad} failures / {tot} posets")
ok &= L.verdict(mx == Fraction(1, 2), "and its maximum is exactly 1/2 -- mg-409a's L3 value",
                f"max = {mx}")
print("""
  AND THAT IS THE POINT.  The identity computes E_BK(inv_e) exactly and the number it gets
  is bounded by 1/2 at EVERY poset -- the same 1/2 whatever E[inv_e] is.  So the quantity
  the identity CAN compute about inv_e carries ZERO information about the quantity row 8
  needs, which is E[inv_e] itself.  A Dirichlet form is not a mean.""")

# ---------------------------------------------------------------------------------------
L.banner("e3.6  SCOPE, stated because it limits every arm in this directory")
print("""  (R) is a FROZEN-conditional statement and the frozen class is EMPTY at every n this
  corpus can enumerate -- the 1/3-2/3 conjecture is verified to n = 14 (mg-33f5), and the
  literature lower bound on a minimal counterexample is n >= 12 refereed / n >= 15 preprint
  (STATE.md:213).  So no measurement here, or anywhere in this repository, samples the class
  (R) quantifies over.  mg-345e and mg-6bc2 declared and refused the same sweep for the same
  reason and that refusal is kept here.

  What this arm therefore establishes is NOT "d is large on frozen posets".  It is that the
  identity's ONLY relation touching d is an equality at d = 1, so the identity cannot be the
  source of an upper bound on d at any poset, frozen or not.  That is a statement about the
  relation, and it does not need the class to be nonempty.""")

L.banner("e3  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
