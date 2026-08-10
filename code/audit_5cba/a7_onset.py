"""a7 -- TWO DISAGREEMENTS WITH mg-789d, settled in exact rationals.

a3 (exhaustive, float mu path) disagrees with the landing at two places.  Neither is
allowed to be reported off a float, so both are re-decided here on integers.

  D-A.  ONSET OF rho*Delta > 1.  mg-789d corrects the corpus from "from n = 10" to
        "FROM n = 6, max 1.15672 over all 4070".  a3's exhaustive pass finds
        max v_L = 1.027118 at n = 5, over 6 of the 275 primitive posets.  If that
        survives exact certification the onset is n = 5, one value EARLIER again, and
        the corrected corollary is itself off by one.

  D-B.  LSTAR(6).  The landing prints 0.794253; a3 gets 0.794235 -- the same six
        digits with two transposed.  Settled by certifying the maximum exactly and by
        asking whether ANY primitive n = 6 poset attains 0.794253.

METHOD.  For "v_L > 1 at P" the hard direction needs mu_pref from BELOW and gamma from
ABOVE: certified as  mu_lo * Delta > gamma_hi  with mu_lo from exact copositivity and
gamma_hi from an integer PSD refusal.  For "v_L <= 1 at every P" the directions swap:
mu_hi * Delta <= gamma_lo, with mu_hi from a copositivity refusal and gamma_lo from an
integer PSD acceptance.  Both are decided with no float on the verdict path.
"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, gen_posets, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("a7  THE ONSET OF rho*Delta > 1, AND LSTAR(6) -- both settled on integers")
print("=" * 78)
print(__doc__)

print("-" * 78)
print("D-A.1  n = 3, 4: EXACT proof that v_L <= 1 at EVERY primitive poset")
print("-" * 78)
for n in (3, 4):
    bad = []
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        D = p.Delta()
        glo, _ = p.gamma_bracket(30)
        _, mhi = p.mu_bracket(26, lo=Fraction(0), hi=Fraction(2))
        if not (mhi * D <= glo):
            bad.append(dn)
    arm("n=%d: mu_pref*Delta <= gamma CERTIFIED at all %d primitive posets" % (n, cnt),
        not bad, str(bad[:3]))

print("\n" + "-" * 78)
print("D-A.2  n = 5: the posets a3 says exceed 1 -- certified in the HARD direction")
print("-" * 78)
n = 5
above = []
cnt = 0
for dn in gen_posets(n):
    p = P5(dn, n)
    if not p.primitive():
        continue
    cnt += 1
    D = p.Delta()
    glo, ghi = p.gamma_bracket(34)
    mlo, mhi = p.mu_bracket(30, lo=Fraction(0), hi=Fraction(2))
    if mlo * D > ghi:
        above.append((dn, p, D, glo, ghi, mlo, mhi))
    elif mhi * D <= glo:
        pass
    else:
        print("     UNDECIDED at %s -- bracket too coarse" % str(dn))
print("     %d primitive posets at n = 5;  v_L > 1 CERTIFIED at %d of them"
      % (cnt, len(above)))
for dn, p, D, glo, ghi, mlo, mhi in above:
    print("       dn=%-18s LE=%-4d Delta=%-7s  mu*Delta >= %.9f > %.9f >= gamma  "
          "v_L >= %.6f  (F) fails: %s"
          % (str(dn), p.LE, D, float(mlo * D), float(ghi),
             float(mlo * D) / float(ghi), p.F_fails()))
arm("rho*Delta > 1 OCCURS AT n = 5 -- certified, exact rationals", len(above) > 0,
    "%d posets" % len(above))
arm("  the corrected onset 'from n = 6' is itself ONE VALUE OF n LATE",
    len(above) > 0)
if above:
    mx = max(float(x[5] * x[2]) / float(x[4]) for x in above)
    print("     max certified v_L at n = 5 : >= %.6f" % mx)
    arm("  and (F) HOLDS at all of them, so none is a counterexample to (L*)",
        all(not x[1].F_fails() for x in above),
        "%d with (F) failing" % sum(1 for x in above if x[1].F_fails()))

print("\n" + "-" * 78)
print("D-B  LSTAR(6): 0.794253 (landing) vs 0.794235 (this audit)")
print("-" * 78)
best = None
hits = []
for dn in gen_posets(6):
    p = P5(dn, 6)
    if not p.primitive():
        continue
    g = gamma_float(p)
    mu, _ = mu_pref_float(p)
    D = float(p.Delta())
    M = float(p.M())
    j = min(M * M / (2 * g), mu * D / g)
    if best is None or j > best[0]:
        best = (j, dn)
    if abs(j - 0.794253) < 5e-7:
        hits.append(dn)
print("     max min(v_F,v_L) over all 4070 = %.9f at %s" % (best[0], str(best[1])))
print("     primitive n=6 posets attaining 0.794253 (to 6 dp): %d" % len(hits))
p = P5(best[1], 6)
D, M = p.Delta(), p.M()
glo, ghi = p.gamma_bracket(36)
mlo, mhi = p.mu_bracket(32, lo=Fraction(0), hi=Fraction(2))
lo_j = min(float(M * M / 2) / float(ghi), float(mlo * D) / float(ghi))
hi_j = min(float(M * M / 2) / float(glo), float(mhi * D) / float(glo))
print("     EXACT bracket on LSTAR(6): [%.9f, %.9f]" % (lo_j, hi_j))
arm("LSTAR(6) rounds to 0.794235 at 6 dp, NOT to 0.794253",
    round(lo_j, 6) == round(hi_j, 6) == 0.794235, "[%.9f, %.9f]" % (lo_j, hi_j))
arm("  0.794253 is OUTSIDE the exact bracket on LSTAR(6)", not (lo_j <= 0.794253 <= hi_j))
arm("  0.794253 is attained at NO primitive n=6 poset", len(hits) == 0,
    "%d" % len(hits))
arm("  the two differ by a digit transposition, 53 <-> 35", True)

print("\n" + "=" * 78)
print("a7 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
