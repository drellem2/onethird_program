"""r4 -- DOES W2's REPAIR RESTORE THE OBJECT SECTION 5 REDUCES TO?  The mayor's first task.

Section 5 asks for the inequality "for the relevant f" -- under section 4's assumption at
:217, the linear ones.  W2's repair (fa29801) is a FULL-SPACE operator inequality: it gives
gap_BK >= (2/(n-1)) * lam_min(M|1perp) with the minimum over ALL f perp 1, and needs no
assumption about which f attains the BK gap.

So the repair delivers the SAME OPERATOR M and the SAME DIRECTION, but at a DIFFERENT
QUANTIFIER.  Write

    alpha_full(P) = min over all f perp 1        of R_M(f)     <- what the repair consumes
    alpha_lin(P)  = min over linear f perp 1     of R_M(f)     <- what section 5 states

Then alpha_full <= alpha_lin always, so section 5's target as WRITTEN is strictly weaker than
what the repaired section 4 can use.  This arm measures the gap: how often, and by how much.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

ok = True


def alpha_linear(n, lt, LEs):
    """min R_M over the span of the pair-orientation indicators, centred.

    Basis: {f_xy - mean : (x,y) incomparable}, reduced to a linearly independent subset by
    exact rational elimination, then the generalized eigenproblem <f,Mf> vs <f,f>.
    """
    inc = L.incomparable(n, lt)
    if not inc:
        return None
    raw = [L.center(L.pair_indicator(n, lt, LEs, x, y)) for (x, y) in inc]
    basis = []
    rows = []
    for v in raw:
        # exact Gram-Schmidt-by-elimination for independence only
        w = list(v)
        for b in rows:
            piv = next((i for i, t in enumerate(b) if t != 0), None)
            if piv is None:
                continue
            if w[piv] != 0:
                f = w[piv] / b[piv]
                w = [a - f * c for a, c in zip(w, b)]
        if any(t != 0 for t in w):
            rows.append(w)
            basis.append(v)
    if not basis:
        return None
    A = [[sum(a * b for a, b in zip(u, L.apply_M(v, LEs, n))) for v in basis] for u in basis]
    B = L.gram(basis)
    return L.min_gen_eig(A, B)


L.banner("r4.1  alpha_full vs alpha_lin -- the quantifier the repair moves")

print("   n |  posets |  alpha_full < alpha_lin |  worst ratio alpha_full/alpha_lin")
rows = []
for n, label, posets in ((3, "exhaustive", list(L.all_posets(3))),
                         (4, "exhaustive", list(L.all_posets(4))),
                         (5, "sampled(45,seed=5409)", L.sample_posets(5, 45, 5409))):
    strictly = 0
    cnt = 0
    worst = 1.0
    worst_lt = None
    for lt in posets:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        af = L.alpha_measured(LEs, n)
        al = alpha_linear(n, lt, LEs)
        if al is None:
            continue
        cnt += 1
        if af < al - 1e-9:
            strictly += 1
        r = af / al if al > 1e-12 else 1.0
        if r < worst:
            worst, worst_lt = r, sorted(lt)
    rows.append((n, cnt, strictly, worst))
    print("  %3d |  %6d |  %22d |  %s" % (n, cnt, strictly, L.frac(worst, 6)))
    ok &= L.verdict(worst <= 1.0 + 1e-9, f"  n={n}: alpha_full <= alpha_lin everywhere")
print()
print("  worst case seen:", worst_lt)

L.banner("r4.2  what that costs, stated as the answer to the mayor's first question")
print("  1. THE OPERATOR IS THE SAME.  W2's repair bounds gap_BK below by (2/(n-1)) times")
print("     the SAME 2I - Pi_o - Pi_e that section 5 reduces to.  Section 4's object is")
print("     delivered, and unconditionally -- :217 is not needed for that direction.")
print("  2. THE QUANTIFIER MOVES, AND AGAINST YOU.  The repair consumes alpha_full; section")
print("     5 states alpha_lin.  A proof of section 5 exactly as written does NOT feed the")
print("     repair whenever the two differ, and the table above says they differ often.")
print("  3. NEITHER IS THE WALL'S OBJECT.  Both bound lambda_2^BK.  STATE.md:78 records that")
print("     lambda_std and lambda_2^BK are INCOMPARABLE -- no universal inequality in either")
print("     direction (mg-d1be, exact rationals) -- so nothing here reaches lambda_std, and")
print("     the repair does not change that.  See README S1.")

sys.exit(0 if ok else 1)
