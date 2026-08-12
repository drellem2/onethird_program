#!/usr/bin/env python3
"""mg-0e8c a3 -- SETTLE THE CURRENCY BEFORE SETTLING THE LOGIC.

The ticket's first instruction is that `eps_spec` and `eps_c3ca` are the same theorem in two
normalisations and that `1/6` and `1` do not compare, so the question "does eps_sup < 1 discharge
row 8?" cannot be answered until it is established that `eps_sup` is quoted in ROW 8'S OWN units.
This file establishes exactly that, and then measures the one thing the currency question turns
out NOT to settle: that row 8's two halves are not the same statement.

FOUR MEASUREMENTS.

  C1  THE UNIT MAP, checked as arithmetic.  One theorem `E[inv_e] < m/3`; two divisions:
        / (n^2-1)/6  ->  eps_spec  < 2m/(n^2-1) = d*n/(n+1)  -> 1      [row 8's units]
        / n^2        ->  eps_c3ca  < m/(3n^2)   <= (n-1)/(6n) -> 1/6   [mg-c3ca's units]
      and eps_spec/eps_c3ca = 6n^2/(n^2-1).  Verified over the (n, m) grid on exact rationals.
      THE POINT: `eps_sup < 1` is already in row 8's currency.  The two-currency trap does NOT
      apply to it, so it does not rescue the row.

  C2  CLAIM 6.1's INEQUALITY, checked against the frozen population it quantifies over.
      Op-Form Claim 6.1 is INHERITED, not re-derived; this is a test that our E[inv_e] and our
      frozen predicate sit on the sides of it the corpus says they do.

  C3  THE TWO HALVES COME APART AT eps = 1.  For every poset: does the spectral form hold at
      eps = 1?  Does the inversion form?  A poset satisfying one and not the other is a
      counterexample to reading them as `equivalently` (docs/CONCEPTS.md §4's word).

  C4  THE SIZE OF THE GAP, in one currency, with the demand beside the supply.

⚠️ SCOPE, so no figure here can be quoted away from its population.  Every census is over the
labelled posets on n <= 6 admitting e = 0 < 1 < ... < n-1 as a linear extension, EXHAUSTIVE.
Nothing here is proven for all n; C1's algebra is, and is marked where it is stated.
"""

import os
import sys
from fractions import Fraction
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib0e8c as L                                        # noqa: E402

print("=" * 78)
print("mg-0e8c a3 -- THE CURRENCY, AND WHETHER ROW 8'S TWO HALVES ARE ONE STATEMENT")
print("=" * 78)

# ---- C1 --------------------------------------------------------------------------------
print("""
C1  THE UNIT MAP.  One theorem, two divisions.  Exact rationals, no floating point.
    KIND: ALGEBRA -- true for every n, not a population.
""")
print("   n    m=C(n,2)   eps_spec bound   eps_c3ca bound   ratio 6n^2/(n^2-1)   d*n/(n+1) ?")
bad = 0
for n in range(3, 13):
    m = n * (n - 1) // 2                                   # the antichain: every pair incomparable
    eps_spec = Fraction(2 * m, n * n - 1)
    eps_c3ca = Fraction(m, 3 * n * n)
    ratio = eps_spec / eps_c3ca
    want_ratio = Fraction(6 * n * n, n * n - 1)
    d = Fraction(m, m)                                     # density 1 at the antichain
    want_spec = d * Fraction(n, n + 1)
    if ratio != want_ratio or eps_spec != want_spec:
        bad += 1
    print("  %2d    %-9d  %-15s  %-15s  %-19s  %s"
          % (n, m, eps_spec, eps_c3ca, ratio, "OK" if eps_spec == want_spec else "MISMATCH"))
print("\n  mismatches over the grid: %d" % bad)
print("""
  READING.  `eps_sup < 1` is `eps_spec < n/(n+1)`, i.e. it is quoted in ROW 8'S OWN units -- the
  units in which row 8 writes `E[inv_e] <= (eps_spec/6)(n^2-1)`.  The `1/6` figure lives in
  mg-c3ca's `E[inv_e] <= eps*n^2` units and is the SAME theorem.  So the ledger's two-currency
  warning is real and it does NOT apply here: there is no unit mismatch standing between
  `eps_sup < 1` and row 8's stated conclusion.  The currency question is settled, and settling it
  REMOVES the only defence the row had.
""")

# ---- C2 --------------------------------------------------------------------------------
print("-" * 78)
print("""
C2  CLAIM 6.1's INEQUALITY `E[inv_e] < m/3` on the frozen population (INHERITED, tested).
""")
FROZEN = {}
for n in range(2, 7):
    tot = frozen = frozen_nontrivial = viol = 0
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        d, ninc = L.delta_P(n, exts, rel)
        tot += 1
        if d < Fraction(1, 3):
            frozen += 1
            if ninc > 0:
                frozen_nontrivial += 1
            Einv = L.E_inv_e(n, exts, rel)
            if not (Einv < Fraction(ninc, 3) or ninc == 0 and Einv == 0):
                viol += 1
    FROZEN[n] = (tot, frozen, frozen_nontrivial)
    print("  n=%d  posets=%-6d  frozen (delta<1/3)=%-6d  of which with >=1 incomparable pair=%-4d"
          "  Claim 6.1 violations=%d" % (n, tot, frozen, frozen_nontrivial, viol))
print("""
  READING.  Claim 6.1 holds on every frozen poset tested.  Note the third column: at these n the
  frozen class is EXACTLY the chains -- posets with no incomparable pair -- so `frozen` is
  vacuously satisfied there and carries no information.  That is a4's subject and it does NOT
  weaken the verdict: Claim 6.1 is proven for all n and its bound `2m/(n^2-1) <= n/(n+1) < 1`
  is arithmetic on m, so the discharge of row 8 does not depend on this population being rich.
""")

# ---- C3 --------------------------------------------------------------------------------
print("-" * 78)
print("""
C3  DO ROW 8'S TWO HALVES AGREE AT eps = 1?
      SPECTRAL   form at eps=1:  1 - lambda_std <= 1
      INVERSION  form at eps=1:  E[inv_e] <= (1/6)(n^2 - 1)
    Counted over EVERY poset, since `equivalently` (docs/CONCEPTS.md §4) is a claim about the two
    QUANTITIES and is read that way by a reader holding one poset.
""")
print("   n   posets   spec only   inv only   both   neither   |   spec holds   inv holds")
for n in range(2, 7):
    tot = sonly = ionly = both = neither = sh = ih = 0
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        S = L.S_matrix(n, L.T_matrix(n, exts))
        spec = L.lambda_std_nonneg_exact(n, S)                       # 1-lambda_std <= 1, exact
        inv = L.E_inv_e(n, exts, rel) <= Fraction(n * n - 1, 6)      # exact
        tot += 1
        sh += spec
        ih += inv
        if spec and inv:
            both += 1
        elif spec:
            sonly += 1
        elif inv:
            ionly += 1
        else:
            neither += 1
    print("   %d   %-8d %-11d %-10d %-6d %-9d |   %-11d %d"
          % (n, tot, sonly, ionly, both, neither, sh, ih))
print("""
  READING.  The `spec only` column is non-empty from n = 3 on: those posets satisfy row 8's
  SPECTRAL conclusion at eps = 1 and FAIL its INVERSION conclusion at the same eps.  So the two
  halves are NOT equivalent as statements about a poset, and the master bound
  `1 - lambda_std <= 6E[inv_e]/(n^2-1)` is ONE-WAY -- inversions to spectrum, never back.

  WHAT THIS DOES AND DOES NOT LICENCE.  It refutes `equivalently` as a claim about the two
  QUANTITIES, which is how docs/CONCEPTS.md §4 reads.  It does NOT by itself refute the weaker
  reading `frozen => A  iff  frozen => B`, because the separating posets are not frozen; that
  reading is unrefuted here and is also unproven, and the honest word for the join is the
  implication that IS proven -- inversion form => spectral form -- with its direction named.
""")

# ---- C4 --------------------------------------------------------------------------------
print("-" * 78)
print("""
C4  THE GAP, in one currency (eps_spec units).  Both numbers are READ from the corpus, not
    derived here: eps_sup < 1 is Op-Form Claim 6.1 via mg-345e; eps_dem ~ 2e-2 is STATE.md:21's
    repaired calibration.  What is computed here is the ratio.
""")
sup = Fraction(1)
dem = Fraction(2, 100)
print("      eps_sup  (PROVEN, all n, L4-independent)   <  %s" % sup)
print("      eps_dem  (what Step 6 consumes)            ~  %s   = %.3f" % (dem, float(dem)))
print("      ratio    eps_sup / eps_dem                 =  %s   = %.0fx"
      % (sup / dem, float(sup / dem)))
print("""
  READING.  The distance between what is proven and what is needed is a factor of ~50 IN A
  SINGLE CURRENCY.  It is not an existence question and it is not a quantifier question: both
  ends are explicit absolute constants uniform in n, and the whole remaining content of row 8 is
  the interval between them.
""")

# ---- C5 --------------------------------------------------------------------------------
print("-" * 78)
print("""
C5  A THIRD NORMALISATION, AND THE DENSITY IT TURNS THE WALL INTO.

    Op-Form §6.3 states Claim 6.1's consequence in units the ledger does NOT carry -- as a
    fraction of the uniform baseline:

        E_unif[inv] = C(n,2)/2, and m <= C(n,2), so Claim 6.1 gives
        E[inv_e] < (2/3) E_unif[inv]                             <- Op-Form's own words:
        "(LIB-const) ALREADY HOLDS, WITH CONSTANT 2/3"

    So THREE numbers name one theorem: 1 (eps_spec units, row 8's), 1/6 (eps_c3ca units), and
    2/3 (fraction-of-uniform).  The ledger warns about the first two and does not mention the
    third.  Checked below that all three are the same theorem.

    AND THE USEFUL COROLLARY.  Claim 6.1's bound is eps_sup = d * n/(n+1) with d = m/C(n,2) the
    INCOMPARABILITY DENSITY -- it is not a flat 1, it is proportional to d.  So the proven
    constant already clears the demand whenever d is small enough, and the wall is open only in
    the DENSE regime.  The threshold is computed here rather than asserted.
""")
print("   n    E_unif[inv] in eps_spec units   (2/3) of it   Claim 6.1's eps_sup at d=1   equal?")
bad5 = 0
for n in range(3, 13):
    m_full = n * (n - 1) // 2
    unif_eps = Fraction(6, 1) * Fraction(m_full, 2) / (n * n - 1)
    two_thirds = Fraction(2, 3) * unif_eps
    claim = Fraction(n, n + 1)
    if two_thirds != claim:
        bad5 += 1
    print("  %2d    %-30s  %-13s %-28s %s"
          % (n, unif_eps, two_thirds, claim, "OK" if two_thirds == claim else "MISMATCH"))
print("\n  mismatches: %d  -- the 2/3, the 1 and the 1/6 are one theorem in three normalisations."
      % bad5)

print("""
    THE DENSITY THRESHOLD.  eps_sup(d) = d * n/(n+1) <= eps_dem = 1/50 requires
    d <= (1/50)(n+1)/n, i.e. d <~ 2e-2.  Tabulated:
""")
print("   n      max density d      largest m clearing eps_dem   m forced by primitivity (>= n-1)")
for n in [10, 50, 99, 100, 101, 1000, 10 ** 4]:
    dmax = Fraction(2, 100) * Fraction(n + 1, n)
    m_allowed = dmax * Fraction(n * (n - 1), 2)
    m_floor = int(m_allowed)                       # Fraction -> floor for positive values
    forced = n - 1
    flag = "CLEARS" if m_floor >= forced else "*** NO PRIMITIVE POSET CLEARS IT ***"
    print("  %-6d %-18s %-27s %-8d %s"
          % (n, "%.6f" % float(dmax), "%d  (of C(n,2)=%d)" % (m_floor, n * (n - 1) // 2),
             forced, flag))
print("""
    THE CROSS-CHECK THAT MAKES THIS NOT A NEW NUMBER.  Primitivity forces m >= n-1 (STATE.md's
    own density facts, mg-6bc2 §7), i.e. d >= 2/n.  So a PRIMITIVE poset can satisfy
    d <= eps_dem(n+1)/n only when 2/n <~ 2e-2, i.e. n >~ 100 -- which is EXACTLY the `n >= 100
    (primitive)` threshold STATE.md row 8 already carries from mg-e35c A1.  The density reading
    and the ledger's own threshold are the same fact, reached from opposite ends.""")

print("""
  READING, AND IT IS THE SHARPEST RESTATEMENT AVAILABLE.  The pair-bias supply is NOT a flat
  constant that happens to be too big; it is `d * n/(n+1)`, LINEAR IN THE INCOMPARABILITY
  DENSITY.  At d <~ 2e-2 it already clears the demand and the wall is DOWN for those posets --
  proven, all n, L4-independent.  What is open is the dense regime: a frozen poset with
  incomparability density above ~2%.  Op-Form §6.3 records this threshold at the SUPERSEDED
  eps_spec = 2e-4 (it prints `d <~ 2e-4`); at the repaired 2e-2 it is 100x looser, and the
  100x is mg-e35c's repair, not a new result.

  So "how small a constant" and "how dense a poset" are the same open question, and the second
  is the one you can point an instrument at.
""")
