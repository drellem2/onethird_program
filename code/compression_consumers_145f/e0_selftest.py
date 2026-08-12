"""e0 -- selftest and cross-check against mg-409a's independent implementation.

This is the ONLY arm that imports `lib409a`.  Its job is to make the rest of the directory
worth reading: if my fibers, my conditional variances or my BK Dirichlet form disagreed with
mg-409a's, every downstream number would be mine alone.

Four positive controls are included and all four MUST fire.  A control that cannot fail is
not a control -- mg-409a's own D1 and mg-8bc7's D2 are both that shape, and both were caught
only by someone re-reading the control rather than the result.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "compression_rate_409a"))

import lib145f as L
import lib409a as R  # noqa: E402  -- cross-check ONLY, no verdict below routes through it

ok = True

# ---------------------------------------------------------------------------------------
L.banner("e0.1  poset enumeration agrees with lib409a")
for n in (3, 4):
    mine = sorted(map(sorted, L.all_posets(n)))
    theirs = sorted(map(sorted, R.all_posets(n)))
    ok &= L.verdict(mine == theirs, f"n = {n}: labelled posets", f"{len(mine)}")

# ---------------------------------------------------------------------------------------
L.banner("e0.2  block systems, fibers, E Var(f|C) and E_BK agree with lib409a")
pop = [(4, p) for p in L.all_posets(4)] + [(5, p) for p in L.sample_posets(5, 40, 11)]
worst = 0
checked = 0
for (n, lt) in pop:
    LEs = L.linear_extensions(n, lt)
    LEs_r = R.linear_extensions(n, lt)
    if sorted(LEs) != sorted(LEs_r):
        ok &= L.verdict(False, "linear extensions disagree")
        break
    if L.odd_blocks(n) != R.blocks_o(n) or L.even_blocks(n) != R.blocks_e(n):
        ok &= L.verdict(False, "block systems disagree")
        break
    inc = L.incomparable_pairs(n, lt)
    if not inc:
        continue
    # three generators: a pair indicator, an all-ones linear statistic, a position statistic
    for c in ({inc[0]: Fraction(1)},
              {p: Fraction(1) for p in inc},
              {p: Fraction(1 + (i % 3)) for i, p in enumerate(inc)}):
        f = L.pair_orientation_stat(LEs, c)
        f_r = R.linear_stat(n, lt, LEs, c)
        assert f == f_r
        for (g_mine, g_theirs) in ((L.odd_blocks(n), R.blocks_o(n)),
                                   (L.even_blocks(n), R.blocks_e(n))):
            a = L.e_cond_var(f, LEs, g_mine)
            b = R.e_cond_var(f, LEs, g_theirs)
            worst = max(worst, abs(a - b))
        a = L.bk_energy(f, LEs, n, lt)
        b = R.bk_energy(f, LEs, n, lt)
        worst = max(worst, abs(a - b))
        checked += 1
ok &= L.verdict(worst == 0, f"E Var(f|C_o), E Var(f|C_e), E_BK over {checked} (poset, f) pairs",
                f"max |difference| = {worst} (exact)")

# ---------------------------------------------------------------------------------------
L.banner("e0.3  POSITIVE CONTROLS -- all four must FIRE")

n, lt = 4, frozenset()
LEs = L.linear_extensions(n, lt)
inc = L.incomparable_pairs(n, lt)
c = {p: Fraction(1) for p in inc}
f = L.pair_orientation_stat(LEs, c)
A_o, A_e = L.adjacency_probs(n, lt, LEs)

# C1: corrupt one adjacency probability -> the identity must break.
bad = dict(A_o)
bad[inc[0]] = bad[inc[0]] + Fraction(1, 7)
lhs = L.e_cond_var(f, LEs, L.odd_blocks(n))
rhs_bad = sum(Fraction(c.get(p, 0)) ** 2 * bad[p] for p in bad) / 4
ok &= L.verdict(lhs != rhs_bad, "C1  perturbed A_o breaks the identity",
                f"{L.fr(lhs)} vs {L.fr(rhs_bad)}")

# C2: swap the two block systems -> E Var(f|C_o) must stop matching A_o.
rhs_swapped = sum(Fraction(c.get(p, 0)) ** 2 * A_e[p] for p in A_e) / 4
ok &= L.verdict(lhs != rhs_swapped, "C2  A_e in A_o's slot breaks the identity",
                f"{L.fr(lhs)} vs {L.fr(rhs_swapped)}")

# C3: a DEGREE-TWO statistic must violate the identity (the identity is degree-one only).
pos = L.positions(LEs)
f2 = [Fraction(p[0]) ** 2 for p in pos]          # pos(x_0)^2 -- not degree one on fibers
lhs2 = L.e_cond_var(f2, LEs, L.odd_blocks(n))
# the identity's prediction for the closest degree-one surrogate is c = 0 off pairs of x_0
c2 = {q: (Fraction(1) if 0 in q else Fraction(0)) for q in inc}
rhs2 = sum(Fraction(c2[p]) ** 2 * A_o[p] for p in A_o) / 4
ok &= L.verdict(lhs2 != rhs2, "C3  a degree-two statistic is NOT computed by the identity",
                f"{L.fr(lhs2)} vs {L.fr(rhs2)}")

# C4: drop the trailing singleton of blocks_e for even n -- mg-409a's D1 defect.  Here the
# control is that this arm NOTICES, which mg-409a's first attempt did not: check the block
# LIST, not the induced partition (the partition is genuinely unchanged, which is why the
# original control could not fire).
full = L.even_blocks(n)
assert len(full[-1]) == 1, full          # n even: the trailing group IS a singleton
mutilated = full[:-1]
def _part(groups):
    return sorted(sorted(v) for v in L.fibers(LEs, groups).values())


same_partition = (_part(mutilated) == _part(full))
ok &= L.verdict(same_partition and mutilated != full,
                "C4  mg-409a's D1 reproduced: dropping the trailing singleton leaves the "
                "PARTITION identical", "so the block LIST is what must be compared")

# ---------------------------------------------------------------------------------------
L.banner("e0  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
