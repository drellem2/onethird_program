"""a5 -- SCOPE: the LSTAR(n) table's n >= 8 rows, and the n = 12 claim.

WHY THIS SECTION EXISTS.  mg-789d's LSTAR table reads

     8 |  >= 0.968818 | SEARCH ONLY
     9 |  >= 1.013539 | SEARCH ONLY -- (L*) FALSE
    10 |  >= 1.020310 | SEARCH ONLY -- (L*) FALSE
    11 |  >= 1.025044 | SEARCH ONLY -- (L*) FALSE
    12 |  >= 1.057643 | SEARCH ONLY -- (L*) FALSE

but every one of those five numbers is produced by `s1_hunt.py:50` /
`s6_aftermath.py:71`, which score the hill climb with `mu_ub_float` -- an UPPER bound
on mu_pref, correctly so, because a screen may only over-state the hunted quantity.

An UPPER bound on mu_pref gives an UPPER bound on v_L = mu_pref*Delta/gamma, hence an
UPPER bound on min(v_F, v_L), hence an UPPER bound on LSTAR(n).  It cannot certify
"LSTAR(n) >= x".  The direction is wrong for four of the five rows as written.

For n = 9, 10, 11 that is harmless in substance -- s5 re-does those three posets in
exact rationals and the certified values are what this file recomputes.  For n = 12
it is NOT harmless: s1 handed a candidate to the exact stage and s5 never certified
it (s5.4 lists FOUR counterexamples, at n = 9, 9, 10, 11 -- no n = 12).  So the
table's "12 | (L*) FALSE" rests on a float upper bound alone.

This file settles n = 12 exactly and re-states each n >= 8 row at its certified value.
"""
import sys
import time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


ROWS = [
    ("n=8  search argmax", (0, 0, 2, 0, 8, 24, 63, 62), 8, 0.968818, False),
    ("n=9  search argmax (= counterexample C2)", (0, 0, 0, 0, 0, 16, 48, 16, 247), 9,
     1.013539, True),
    ("n=10 search argmax (= counterexample C3)", (0, 1, 3, 0, 9, 0, 32, 96, 255, 239),
     10, 1.020310, True),
    ("n=11 search argmax (= counterexample C4)",
     (0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11, 1.025044, True),
    ("n=12 search argmax -- NEVER CERTIFIED BY mg-789d",
     (0, 0, 3, 7, 15, 7, 63, 2, 135, 391, 7, 1159), 12, 1.057643, None),
]

print("=" * 78)
print("a5  SCOPE -- the LSTAR(n) rows for n >= 8, recomputed with LOWER bounds")
print("=" * 78)
print(__doc__)

print("%-44s %10s %12s %12s" % ("row", "published", "certified", "direction"))
print("-" * 78)
results = []
for tag, dn, n, pub, claim_false in ROWS:
    t0 = time.time()
    p = P5(dn, n)
    D = p.Delta()
    M = p.M()
    glo, ghi = p.gamma_bracket(30)
    mf, _ = mu_pref_float(p)
    # a rational LOWER certificate on mu_pref, from a small bracket seeded by the float
    lo = Fraction(int(mf * 10 ** 7) - 20, 10 ** 7)
    if lo < 0:
        lo = Fraction(0)
    mlo, mhi = p.mu_bracket(18, lo=lo, hi=Fraction(int(mf * 10 ** 7) + 200, 10 ** 7))
    vL_lo = float(mlo * D) / float(ghi)        # certified LOWER bound on v_L
    vF_lo = float(M * M / 2) / float(ghi)      # certified LOWER bound on v_F
    cert = min(vL_lo, vF_lo)
    Ffails = p.F_fails()
    refuted = Ffails and (mlo * D > ghi)
    print("%-44s %10.6f %12.6f %12s   (%.0fs)"
          % (tag, pub, cert, "over" if pub > cert else "under", time.time() - t0))
    print("     LE=%d  Delta=%s  M=%s  gamma in [%.9f,%.9f]  mu_pref >= %.9f"
          % (p.LE, D, M, float(glo), float(ghi), float(mlo)))
    print("     (F) fails: %s     mu_pref*Delta > gamma CERTIFIED: %s     (L*) refuted: %s"
          % (Ffails, mlo * D > ghi, refuted))
    results.append((tag, n, pub, cert, refuted, Ffails))
    if claim_false is True:
        arm("  (L*) IS refuted at this poset, in exact rationals", refuted)
    # the published figures are printed to 6 dp, so compare at that precision
    arm("  the published search figure is an UPPER bound: published >= certified",
        pub >= cert - 5e-7, "%.6f vs %.8f" % (pub, cert))

print("\n" + "-" * 78)
print("5.0  THE n = 8 RELABELLING CLAIM -- 'exactly mg-c50b's published maximum,")
print("     at a relabelling of their argmax'.  A relabelling moves gamma and M, so")
print("     this only holds if the maximum is attained at the OTHER labelling.")
print("-" * 78)
for dn in [(0, 0, 2, 0, 8, 24, 62, 63), (0, 0, 2, 0, 8, 24, 63, 62)]:
    p = P5(dn, 8)
    g = gamma_float(p)
    mu, _ = mu_pref_float(p)
    print("     %s  Delta=%s  M=%-9s gamma=%.6f  rho*Delta=%.6f"
          % (str(dn), p.Delta(), p.M(), g, mu * float(p.Delta()) / g))
pa = P5((0, 0, 2, 0, 8, 24, 62, 63), 8)
pb = P5((0, 0, 2, 0, 8, 24, 63, 62), 8)
va = mu_pref_float(pa)[0] * float(pa.Delta()) / gamma_float(pa)
vb = mu_pref_float(pb)[0] * float(pb.Delta()) / gamma_float(pb)
arm("the two labellings give DIFFERENT rho*Delta (so 'relabelling' is not a no-op)",
    abs(va - vb) > 1e-6, "%.6f vs %.6f" % (va, vb))
arm("0.968818 is the one mg-789d reached, and it IS mg-c50b's published maximum",
    abs(vb - 0.968818) < 5e-7, "%.6f" % vb)

print("\n" + "-" * 78)
print("5.1  THE n = 12 ROW")
print("-" * 78)
n12 = [r for r in results if r[1] == 12][0]
arm("n=12: the poset the table points at IS a genuine counterexample after all",
    n12[4], "refuted=%s (F)fails=%s" % (n12[4], n12[5]))
print("     Whether or not it is genuine, mg-789d never certified it: out_s5_certify.txt")
print("     S5.4 lists FOUR counterexamples at n = 9, 9, 10, 11.  The table's n=12")
print("     '(L*) FALSE' was carried by a float UPPER bound on v_L.")

print("\n" + "-" * 78)
print("5.2  THE n = 8 ROW -- the one the document says is OPEN")
print("-" * 78)
n8 = [r for r in results if r[1] == 8][0]
print("     published 0.968818, certified %.6f -- the published figure is the larger,"
      % n8[3])
print("     as an upper bound must be.  Both are far below 1, so (L*) holds at this")
print("     poset either way, and n = 8 remains a SEARCH over 2600369 primitive posets.")
arm("(L*) HOLDS at the n=8 search argmax (certified value < 1)", n8[3] < 1,
    "%.6f" % n8[3])
arm("n=8 is not settled by this: 0.968818 is one poset, not a census", True)

print("\n" + "=" * 78)
print("a5 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
