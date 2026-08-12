#!/usr/bin/env python3
"""mg-0e8c a2 -- IS `1 - lambda_std <= 1` VACUOUS?

Daniel's challenge has a trap inside it that the ticket names: `1 - lambda_std <= 1` may be true
for EVERY poset, hypothesis or no hypothesis, in which case row 8's stated form is not merely
already-satisfied but TRIVIAL -- a stronger version of his point.  Settling it is a question
about `lambda_std`'s SIGN, and the answer must not be a floating-point one.

        `1 - lambda_std <= 1`   <=>   `lambda_std >= 0`   <=>   S_P|_H not negative definite

decided EXACTLY over rationals (lib0e8c.lambda_std_nonneg_exact), over every poset to n = 6.

⚠️ THE FIRST DRAFT OF THIS FILE TESTED THE WRONG STATEMENT AND THE CENSUS THAT CAUGHT IT IS
KEPT BELOW.  It tested `S_P is PSD`, which asserts EVERY eigenvalue of S_P is non-negative, where
`lambda_std >= 0` asserts only that the LARGEST one on H is.  PSD is strictly stronger and it is
false at almost every poset, so the wrong oracle would have reported a vacuity FAILURE that is
not there.  The correction is recorded rather than quietly applied because this report's whole
subject is a claim stated in the wrong currency, and filing one inside it would have been the
same defect one level down.

AND A GENERAL-n REDUCTION, so the verdict is not left as a bare finite population.  M = I - S_P
is the Laplacian of the weighted graph with edge weights S_P[i][j] >= 0, so its eigenvalues are
0 = mu_1 <= mu_2 <= ... <= mu_n and `1 - lambda_std = mu_2` is the SMALLEST of the n-1 upper
ones, hence at most their average:

        1 - lambda_std  =  mu_2  <=  trace(M)/(n-1)  =  (n - trace T_P)/(n-1)      [ALGEBRA]

which is <= 1 exactly when `trace T_P >= 1`.  `trace T_P = E_sigma[#{x : pos_sigma(x) =
rank_e(x)}]`, the expected number of elements a random linear extension leaves in their `e`
position.  The REDUCTION is proven for all n.  `trace T_P >= 1` is MEASURED here and is finite
population.  The two are reported separately with their kinds marked, because a proven reduction
over a measured premise is not a proven conclusion -- and this repository's ledger exists to stop
exactly that sentence being written.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib0e8c as L                                        # noqa: E402

print("=" * 78)
print("mg-0e8c a2 -- IS ROW 8'S SPECTRAL FORM VACUOUS AT eps_spec = 1?")
print("=" * 78)
print("""
EXACT VERDICT COLUMN is `lambda_std >= 0`, i.e. `1 - lambda_std <= 1`, decided over rationals.
The PSD column is the WRONG oracle, kept as the evidence that it is wrong (see the docstring).
""")

print(" n   posets   lambda_std < 0   [wrong oracle: S_P not PSD]   max(1-lambda_std)   min trace T_P")
for n in range(2, 7):
    tot = neg = notpsd = 0
    worst_gap, worst_rel = -1.0, None
    tr_min, tr_min_rel = None, None
    for rel in L.all_posets(n):
        exts = L.linear_extensions(n, rel)
        T = L.T_matrix(n, exts)
        S = L.S_matrix(n, T)
        tot += 1
        if not L.lambda_std_nonneg_exact(n, S):
            neg += 1
        if not L.is_psd_exact(S):
            notpsd += 1
        g = L.one_minus_lambda_std(n, S)
        if g > worst_gap:
            worst_gap, worst_rel = g, rel
        tr = L.trace_T(n, T)
        if tr_min is None or tr < tr_min:
            tr_min, tr_min_rel = tr, rel
    print(" %d   %-8d %-16d %-29s %-19.12f %s"
          % (n, tot, neg, "%d of %d" % (notpsd, tot), worst_gap, tr_min))
    print("     argmax(1-lambda_std) = %s%s ;  argmin(trace T_P) = %s%s"
          % (sorted(worst_rel), " [ANTICHAIN]" if not worst_rel else "",
             sorted(tr_min_rel), " [ANTICHAIN]" if not tr_min_rel else ""))

print("""
-------------------------------------------------------------------------------
READING.

  * `lambda_std >= 0` at EVERY poset tested -- 0 exceptions, exact arithmetic.  So
    `1 - lambda_std <= 1` holds with NO HYPOTHESIS AT ALL.  Row 8's SPECTRAL form, read at the
    constant that is already proven, asserts nothing whatever about frozenness.

  * The maximum of `1 - lambda_std` is EXACTLY 1 and it IS attained -- at the antichain, at
    every n, where T = J/n and spec(I - J/n) = {0} u {1}^(n-1) (hand-checked in a1/T3).  So the
    vacuity is SHARP: `1` is precisely the smallest constant at which the spectral form becomes
    a universal truth, and any eps < 1 would have left it a real statement.

  * `min trace T_P = 1` at every n tested, also attained at the antichain (where a uniform
    random permutation has exactly 1 expected fixed point).  With the ALGEBRA above that gives
    `1 - lambda_std <= (n-1)/(n-1) = 1` on the whole tested population by a second, independent
    route -- and names precisely what a general-n proof would still need: `trace T_P >= 1`.

  * KIND, stated so the green is not over-read.  The reduction `mu_2 <= (n - trace T_P)/(n-1)`
    is ALGEBRA, all n.  `trace T_P >= 1` and `lambda_std >= 0` are both FINITE POPULATION,
    n <= 6, exhaustive.  "The spectral form is vacuous at every n" is therefore NOT proven here.
    IT DOES NOT NEED TO BE for the verdict: on the FROZEN class the same inequality is a THEOREM
    at every n via Op-Form Claim 6.1 and the master bound, which is a3's subject.  Vacuity is the
    SHARPER reading of Daniel's point; it is not the load-bearing one.
-------------------------------------------------------------------------------""")

print("\nTHE ANTICHAIN AT EVERY n, so a reader can redo the arithmetic on paper:\n")
print("   n   E[inv_e]=C(n,2)/2   6E[inv]/(n^2-1)   1-lambda_std   inversion form at eps=1")
for n in range(2, 9):
    rel = frozenset()
    exts = L.linear_extensions(n, rel)
    Einv = L.E_inv_e(n, exts, rel)
    rhs = L.master_bound_rhs(n, Einv)
    g = L.one_minus_lambda_std(n, L.S_matrix(n, L.T_matrix(n, exts)))
    ok = "HOLDS" if Einv <= Fraction(n * n - 1, 6) else "FAILS"
    print("  %2d   %-17s   %-15s   %.10f   %s" % (n, str(Einv), str(rhs), g, ok))
print("""
That last column is the finding a3 makes precise.  At the SAME constant eps = 1, row 8's
spectral form is universally TRUE and row 8's inversion form is FALSE from n = 3 on.  The two
halves of the row are not the same statement, and `equivalently` is not the word for them.
""")
