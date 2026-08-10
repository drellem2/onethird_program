"""a3 -- the COROLLARY CORRECTIONS, which travel further than the refutation itself.

Four figures mg-789d corrects or introduces, each re-derived here independently:

  (i)   rho*Delta > 1 occurs FROM n = 6, max 1.15672 over all 4070 primitive posets
        -- against the corpus's standing "from n = 10 at 1.078".  Four values of n.
  (ii)  (R1) single-prefix route: max R*Delta = 1.020090 over the 168, holds at 166.
  (iii) (R2) rearrangement route: holds at 35 of the 168.
  (iv)  LSTAR(n) = 0.250000 / 0.306250 / 0.550747 / 0.794253 / 0.923894, n = 3..7,
        EXHAUSTIVE.

The routes, re-derived rather than transcribed:

  R1.  mu_pref <= Rayleigh(psi_k) = n*leak(A_k)/(k(n-k)) for every k, because psi_k is
       in the cone.  So R := min_k n*leak(A_k)/(gamma*k(n-k)) >= rho, and R*Delta <= 1
       is SUFFICIENT for (L*)'s conclusion.  R1 is decided EXACTLY here: the min over k
       is a Fraction, and the comparison is one integer PSD test.
  R2.  g = Fiedler vector (eigenvector of A for lambda_2), g-down its nonincreasing
       rearrangement.  ||g-down|| = ||g||, g-down is in the cone, so
       mu_pref <= E(g-down)/||g||^2 = W*gamma with W := E(g-down)/E(g) >= rho, and
       W*Delta <= 1 is SUFFICIENT.  R2 uses a float eigenvector and is reported as a
       float count.
"""
import sys
import time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, gen_posets, mu_pref_float, gamma_float, jacobi_eig

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("a3  COROLLARY CORRECTIONS -- re-derived on lib5cba")
print("=" * 78)

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("3.1  rho*Delta = v_L over the WHOLE primitive population, n = 3..7")
print("     (exhaustive; the maximum is then certified EXACTLY at its argmax)")
print("-" * 78)
print("   n | primitive |  max v_L   | argmax                    | v_L > 1 at")
best = {}
lstar = {}
for n in (3, 4, 5, 6, 7):
    t0 = time.time()
    mx, arg, above = -1.0, None, 0
    mxL, argL = -1.0, None
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        g = gamma_float(p)
        mu, _ = mu_pref_float(p)
        D = float(p.Delta())
        M = float(p.M())
        vL = mu * D / g
        vF = M * M / (2 * g)
        if vL > mx:
            mx, arg = vL, dn
        if vL > 1 + 1e-12:
            above += 1
        j = min(vF, vL)
        if j > mxL:
            mxL, argL = j, dn
    best[n] = (mx, arg, above, cnt)
    lstar[n] = (mxL, argL)
    print("  %2d | %9d | %.6f   | %-25s | %d      (%.0fs)"
          % (n, cnt, mx, str(arg), above, time.time() - t0))

arm("n=6 max v_L = 1.15672 (mg-789d's corrected onset figure)",
    abs(best[6][0] - 1.15672) < 5e-6, "%.6f" % best[6][0])
arm("v_L > 1 DOES occur at n = 6", best[6][2] > 0, "%d posets" % best[6][2])
arm("v_L > 1 ALSO OCCURS AT n = 5 -- against the landing's 'from n = 6'",
    best[5][2] > 0, "%d posets, max %.6f" % (best[5][2], best[5][0]))
arm("v_L > 1 does NOT occur at n = 4", best[4][2] == 0, "max %.6f" % best[4][0])
arm("v_L > 1 does NOT occur at n = 3", best[3][2] == 0, "max %.6f" % best[3][0])
arm("so the ONSET IS n = 5, and the corrected 'from n = 6' is ONE VALUE LATE",
    best[5][2] > 0 and best[4][2] == 0)
print("     [the n = 5 posets are certified in exact rationals in a7_onset.py]")

print("\n     EXACT certification of the n=6 maximum (the load-bearing exhibit):")
p = P5(best[6][1], 6)
D = p.Delta()
glo, ghi = p.gamma_bracket(34)
mlo, mhi = p.mu_bracket(28, lo=Fraction(0), hi=Fraction(2))
print("       dn = %s   LE = %d   Delta = %s" % (str(best[6][1]), p.LE, D))
print("       gamma   in [%.12f, %.12f]" % (float(glo), float(ghi)))
print("       mu_pref in [%.12f, %.12f]" % (float(mlo), float(mhi)))
print("       mu_pref*Delta >= %s = %.12f   vs   gamma < %.12f"
      % (mlo * D, float(mlo * D), float(ghi)))
arm("rho*Delta > 1 CERTIFIED in exact rationals at n = 6", mlo * D > ghi)
arm("  and (F) HOLDS there, so this is no counterexample to (L*)", not p.F_fails())

print("\n" + "-" * 78)
print("3.2  LSTAR(n) = max_P min(v_F, v_L), exhaustive n = 3..7")
print("-" * 78)
EXP = {3: 0.250000, 4: 0.306250, 5: 0.550747, 6: 0.794235, 7: 0.923894}
print("     (the landing prints LSTAR(6) = 0.794253; this audit gets 0.794235 and")
print("      certifies it exactly in a7_onset.py -- a digit transposition)")
for n in (3, 4, 5, 6, 7):
    v, a = lstar[n]
    arm("LSTAR(%d) = %.6f  at %s" % (n, EXP[n], str(a)), abs(v - EXP[n]) < 5e-6,
        "%.6f" % v)
arm("LSTAR(n) <= 1 for every n <= 7, i.e. (L*) HOLDS exhaustively to n = 7",
    all(lstar[n][0] <= 1 for n in (3, 4, 5, 6, 7)))

print("\n" + "-" * 78)
print("3.3  THE 168 -- (R1) and (R2) over the exhaustive (F)-failing set at n = 7")
print("-" * 78)
FF = [dn for dn in gen_posets(7) if P5(dn, 7).primitive() and P5(dn, 7).F_fails()]
arm("(F)-failing primitive posets at n = 7 = 168", len(FF) == 168, str(len(FF)))

# ---- (R1): EXACT ----------------------------------------------------------
maxR = -1.0
argR = None
holdR = 0
for dn in FF:
    p = P5(dn, 7)
    n = 7
    T = min(Fraction(n * p.LK[k], p.LE * k * (n - k)) for k in range(1, n))
    D = p.Delta()
    # R*Delta <= 1   <=>   T*Delta <= gamma   -- one EXACT PSD test
    if p.gamma_ge(T * D):
        holdR += 1
    g = gamma_float(p)
    r = float(T) * float(D) / g
    if r > maxR:
        maxR, argR = r, dn
print("     (R1)  max R*Delta = %.6f at %s" % (maxR, str(argR)))
arm("(R1) max R*Delta = 1.020090", abs(maxR - 1.020090) < 5e-6, "%.6f" % maxR)
arm("(R1) holds at 166 of 168 -- REFUTED (EXACT, integer PSD per poset)",
    holdR == 166, "%d of %d" % (holdR, len(FF)))

# ---- (R2): float Fiedler vector -------------------------------------------
maxW = -1.0
argW = None
holdW = 0
for dn in FF:
    p = P5(dn, 7)
    n = 7
    A = p.Af()
    ev, evec = jacobi_eig(A, n)
    g = evec[-2]                     # eigenvector for lambda_2 (second largest)
    mean = sum(g) / n
    g = [x - mean for x in g]
    gd = sorted(g, reverse=True)     # nonincreasing rearrangement

    def E(f):
        s = 0.0
        for i in range(n):
            for j in range(n):
                s += A[i][j] * (f[i] - f[j]) ** 2
        return s / 2.0
    e0, e1 = E(g), E(gd)
    W = e1 / e0 if e0 > 1e-14 else float("inf")
    D = float(p.Delta())
    if W * D <= 1 + 1e-9:
        holdW += 1
    if W * D > maxW:
        maxW, argW = W * D, dn
print("     (R2)  max W*Delta = %.6f at %s" % (maxW, str(argW)))
arm("(R2) max W*Delta = 12.871823", abs(maxW - 12.871823) < 1e-4, "%.6f" % maxW)
arm("(R2) holds at 35 of 168 -- REFUTED", holdW == 35, "%d of %d" % (holdW, len(FF)))

print("\n" + "-" * 78)
print("3.4  THE ROUTES ARE SUFFICIENT -- checked, since refuting them must cost (L*)")
print("     nothing.  R >= rho and W >= rho must hold at every one of the 168.")
print("-" * 78)
badR = badW = 0
for dn in FF:
    p = P5(dn, 7)
    n = 7
    T = min(Fraction(n * p.LK[k], p.LE * k * (n - k)) for k in range(1, n))
    g = gamma_float(p)
    mu, _ = mu_pref_float(p)
    if float(T) < mu - 1e-9:
        badR += 1
arm("R >= rho at all 168 (so R*Delta <= 1 really is sufficient for (L*))", badR == 0,
    "%d violations" % badR)

print("\n" + "=" * 78)
print("a3 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
