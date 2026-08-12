"""r0 -- self-test and cross-check.  Gates the whole run.

Nothing below is a finding.  It exists so that r1..r5 are entitled to be read: it checks this
file's independently-written constructions against (a) hand-known values, (b) the second
implementation in code/compression_audit_8bc7/lib8bc7.py (mg-8bc7, W2), and (c) two controls
that are shown to GO RED on a planted defect.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib409a as L  # noqa: E402

SIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "compression_audit_8bc7")
sys.path.insert(0, SIB)
import lib8bc7 as W2  # noqa: E402

ok = True


def rng_stream(seed):
    st = seed & 0x7FFFFFFF

    def nxt(lo, hi):
        nonlocal st
        st = (1103515245 * st + 12345) & 0x7FFFFFFF
        return lo + st % (hi - lo + 1)
    return nxt


# --------------------------------------------------------------------------------------
L.banner("r0.1  hand-known linear-extension counts")

for n in range(2, 7):
    got = len(L.linear_extensions(n, L.antichain(n)))
    want = 1
    for k in range(2, n + 1):
        want *= k
    ok &= L.verdict(got == want, f"|L(A_{n})| = n!", f"{got} == {want}")

chain5 = L.close_rel(5, {(0, 1), (1, 2), (2, 3), (3, 4)})
ok &= L.verdict(len(L.linear_extensions(5, chain5)) == 1, "|L(chain_5)| = 1")

for n in (4, 6):
    Z = L.two_block_ordinal_sum(n)
    got = len(L.linear_extensions(n, Z))
    ok &= L.verdict(got == 2 ** (n // 2), f"|L(Z_{n})| = 2^(n/2)", f"{got}")

# --------------------------------------------------------------------------------------
L.banner("r0.2  the two compressions agree with W2's independently-written groups")

for n in range(2, 8):
    ok &= L.verdict(L.blocks_o(n) == W2.groups_o(n), f"blocks_o({n}) == lib8bc7.groups_o")
    ok &= L.verdict(L.blocks_e(n) == W2.groups_e(n), f"blocks_e({n}) == lib8bc7.groups_e")

# --------------------------------------------------------------------------------------
L.banner("r0.3  E Var(f|C), Var(f), E_BK(f) agree with W2's implementations")

nxt = rng_stream(20260812)
agree = 0
for n in (3, 4, 5):
    for lt in list(L.all_posets(n))[:40]:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        vals = [Fraction(nxt(-9, 9)) for _ in LEs]
        for gs_mine, gs_w2 in ((L.blocks_o(n), W2.groups_o(n)), (L.blocks_e(n), W2.groups_e(n))):
            a = L.e_cond_var(vals, LEs, gs_mine)
            b = W2.expected_cond_variance(vals, LEs, gs_w2)
            if a != b:
                ok &= L.verdict(False, "E Var(f|C) disagrees", f"n={n} {a} vs {b}")
            else:
                agree += 1
        if L.variance(vals) != W2.variance(vals):
            ok &= L.verdict(False, "Var disagrees")
        if L.bk_energy(vals, LEs, n, lt) != W2.bk_energy(vals, LEs, n, lt):
            ok &= L.verdict(False, "E_BK disagrees", f"n={n}")
print(f"  ({agree} exact agreements on conditional variances, 0 disagreements)")
ok &= L.verdict(agree > 100, "cross-check population is not empty", f"{agree} comparisons")

# --------------------------------------------------------------------------------------
L.banner("r0.4  M = 2I - Pi_o - Pi_e is what the note says it is")

bad_psd = bad_ker = bad_form = 0
for n in (3, 4, 5):
    for lt in list(L.all_posets(n))[:25]:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        A = L.M_matrix(LEs, n)
        if not W2.psd_exact([[Fraction(x) for x in row] for row in A]):
            bad_psd += 1
        one = [Fraction(1)] * len(LEs)
        if any(v != 0 for v in L.apply_M(one, LEs, n)):
            bad_ker += 1
        vals = [Fraction(nxt(-9, 9)) for _ in LEs]
        lhs = sum(a * b for a, b in zip(vals, L.apply_M(vals, LEs, n)))
        rhs = len(LEs) * (L.e_cond_var(vals, LEs, L.blocks_o(n))
                          + L.e_cond_var(vals, LEs, L.blocks_e(n)))
        if lhs != rhs:
            bad_form += 1
ok &= L.verdict(bad_psd == 0, "M is PSD (exact Schur reduction)")
ok &= L.verdict(bad_ker == 0, "M kills the constants")
ok &= L.verdict(bad_form == 0, "<f,Mf> = N * (E Var(f|C_o) + E Var(f|C_e))  -- the note's :234")

# --------------------------------------------------------------------------------------
L.banner("r0.5  the note's (*) at :149 and W2's repair, re-derived on this instrument")

star_lin = star_gen = viol_lin = viol_gen = 0
for n in (3, 4, 5):
    for lt in list(L.all_posets(n))[:30]:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        inc = L.incomparable(n, lt)
        if inc:
            c = {p: Fraction(nxt(-6, 6)) for p in inc}
            f = L.linear_stat(n, lt, LEs, c)
            if L.variance(f) != 0:
                lhs = L.bk_energy(f, LEs, n, lt)
                rhs = Fraction(2, n - 1) * (L.e_cond_var(f, LEs, L.blocks_o(n))
                                            + L.e_cond_var(f, LEs, L.blocks_e(n)))
                star_lin += 1
                if lhs != rhs:
                    viol_lin += 1
        g = [Fraction(nxt(-9, 9)) for _ in LEs]
        if L.variance(g) != 0:
            lhs = L.bk_energy(g, LEs, n, lt)
            rhs = Fraction(2, n - 1) * (L.e_cond_var(g, LEs, L.blocks_o(n))
                                        + L.e_cond_var(g, LEs, L.blocks_e(n)))
            star_gen += 1
            if lhs < rhs:
                viol_gen += 1
ok &= L.verdict(viol_lin == 0, "(*) is an EQUALITY on linear statistics",
                f"{star_lin} tested")
ok &= L.verdict(viol_gen == 0, "W2's repair: E_BK(f) >= (2/(n-1))<f,Mf> for ARBITRARY f",
                f"{star_gen} tested")

# --------------------------------------------------------------------------------------
L.banner("r0.6  hand-known alpha, and the float eigensolver against an exact witness")

Z4 = L.two_block_ordinal_sum(4)
LEs = L.linear_extensions(4, Z4)
a = L.alpha_measured(LEs, 4)
ok &= L.verdict(abs(a - 1.0) < 1e-12, "alpha(Z_4) = 1 (Jacobi)", L.frac(a))

A3 = L.antichain(3)
LEs3 = L.linear_extensions(3, A3)
a3 = L.alpha_measured(LEs3, 3)
ok &= L.verdict(abs(a3 - 0.5) < 1e-12, "alpha(A_3) = 1/2 (Jacobi)", L.frac(a3))
# and the same number from an exhibited rational test vector, no eigensolver
w = {0: Fraction(-1), 1: Fraction(0), 2: Fraction(1)}
f = L.position_stat(LEs3, w)
r = L.rayleigh_M(f, LEs3, 3)
ok &= L.verdict(r == Fraction(1, 2), "R_M at the exhibited vector = 1/2 EXACTLY", str(r))

# --------------------------------------------------------------------------------------
L.banner("r0.7  two controls that MUST go red on a planted defect")

def star_gap(n, lt):
    """(E_BK(f) , (2/(n-1))<f,Mf>) at the all-ones linear statistic."""
    LEs = L.linear_extensions(n, lt)
    c = {p: Fraction(1) for p in L.incomparable(n, lt)}
    f = L.linear_stat(n, lt, LEs, c)
    lhs = L.bk_energy(f, LEs, n, lt)
    rhs = Fraction(2, n - 1) * (L.e_cond_var(f, LEs, L.blocks_o(n))
                                + L.e_cond_var(f, LEs, L.blocks_e(n)))
    return lhs, rhs


orig_o = L.blocks_o
try:
    L.blocks_o = L.blocks_e          # the two foliations collapse into one
    lhs, rhs = star_gap(4, L.antichain(4))
    ok &= L.verdict(lhs != rhs, "C1: blocks_o := blocks_e BREAKS (*)  [control fires]",
                    f"{lhs} vs {rhs}")
finally:
    L.blocks_o = orig_o

orig_legal = L.legal
try:
    L.legal = lambda Lx, i, lt: False   # no swap is legal: the BK graph loses every edge
    lhs, rhs = star_gap(4, L.close_rel(4, {(0, 1)}))
    ok &= L.verdict(lhs != rhs, "C2: `legal` := False BREAKS (*)  [control fires]",
                    f"{lhs} vs {rhs}")
finally:
    L.legal = orig_legal

# D1, KEPT.  My FIRST C1 dropped the trailing singleton from blocks_e for even n and did NOT
# fire: (*) still held exactly.  That corruption is INVISIBLE because the last position of a
# linear extension is determined by the other n-1, so the coarser group list induces the SAME
# partition of L(P).  A control that cannot fail is not a control -- see README D1.  It is
# also a small true fact about the note's C_e, and it is re-derived here rather than asserted:
orig_e = L.blocks_e
try:
    L.blocks_e = lambda n: [(0,)] + [(2 * j + 1, 2 * j + 2) for j in range((n - 1) // 2)]
    same = 0
    for n in (4, 6):
        LEs = L.linear_extensions(n, L.antichain(n))
        a = {L.fiber_of(x, L.blocks_e(n)) for x in LEs}
        b = {L.fiber_of(x, orig_e(n)) for x in LEs}
        if len(a) == len(b):
            same += 1
    ok &= L.verdict(same == 2,
                    "D1: dropping C_e's trailing singleton induces the SAME partition",
                    "(that is why my first control could not fire)")
finally:
    L.blocks_e = orig_e

L.banner("r0 GATE")
print("  ALL PASS" if ok else "  SOMETHING FAILED -- r1..r5 must not be read")
sys.exit(0 if ok else 1)
