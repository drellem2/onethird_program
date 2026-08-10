"""a2 -- STEP B.  gamma < g_ub, by the PSD device REFUSING, in the hard direction.

pm-onethird ranked this exposure MUCH WEAKER than the copositivity side, and the
reason is that refusing PSD needs only ONE exhibited vector: if c'R(g_ub)c < 0 for a
single rational c then R(g_ub) is not PSD, hence gamma < g_ub, and no eigensolver,
no elimination and no algorithm of mine has to be trusted -- one dot product settles
it.  So this arm's job is to produce a SMALL c and print it in full.

The search for c is done in whatever way is convenient (exact symmetric congruence,
then rounding to short denominators).  The VERDICT is the exact evaluation of c'Rc
in Fractions.  A search cannot manufacture a certificate here: it can only fail to
find one.
"""
import sys
from fractions import Fraction as Fr
from common5e82 import G_UB, build, banner
import lib5e82 as L

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


banner("a2  STEP B -- gamma < g_ub BY PSD REFUSAL, WITH AN EXHIBITED VECTOR")
P = build()
a, b = G_UB.numerator, G_UB.denominator
print("  g_ub = %d/%d = %.13f" % (a, b, float(G_UB)))
R = P.R(a, b)
check("R(g_ub) = b*n*QI - 2*LE*a*NI is 2*LE*n*b*(Q - g_ub*N)", P.scale_check(a, b), True)
check("R(g_ub) is integral", all(isinstance(x, int) for r in R for x in r), True)
print()

npos, nneg, nzero, wit = L.inertia_with_witness(R)
print("  exact inertia of R(g_ub) by symmetric congruence: +%d  -%d  0%d" % (npos, nneg, nzero))
check("R(g_ub) is NOT PSD", wit is None, False)

# Shorten the witness: the congruence produces an exact but enormous vector.  Round it
# to short denominators and keep the first that still evaluates strictly negative.
best = None
scale = max(abs(Fr(x)) for x in wit)
for k in range(3, 16):
    D = 10 ** k
    c = [int(round(float(Fr(x) / scale) * D)) for x in wit]
    g = 0
    from math import gcd

    for x in c:
        g = gcd(g, abs(x))
    if g:
        c = [x // g for x in c]
    if L.quad(R, c) < 0:
        best = c
        break
if best is None:
    best = L.clear_denominators(wit)
    print("  (no short rounding survived; falling back to the exact congruence vector)")

q = L.quad(R, best)
print()
print("  THE CERTIFICATE.  c =")
print("    ", best)
print("  c' R(g_ub) c =")
print("    ", q)
check("c' R(g_ub) c < 0", q < 0, True)

num = sum(Fr(best[i]) * P.Q[i][j] * Fr(best[j]) for i in range(P.m) for j in range(P.m))
den = sum(Fr(best[i]) * P.N[i][j] * Fr(best[j]) for i in range(P.m) for j in range(P.m))
print()
print("  the same vector, read as a Rayleigh quotient:")
print("    c'Qc / c'Nc = %.15f" % float(num / den))
print("    g_ub        = %.15f" % float(G_UB))
check("c'Qc/c'Nc < g_ub, so gamma < g_ub", num / den < G_UB, True)
check("c'Nc > 0 (N is PD, so the quotient is well posed)", den > 0, True)

print()
print("  HOW MUCH ROOM THERE IS, which is the thing a small margin hides.")
lo, hi = Fr(61, 1000), Fr(62, 1000)
for _ in range(50):
    mid = (lo + hi) / 2
    if L.is_psd(P.R(mid.numerator, mid.denominator)):
        lo = mid
    else:
        hi = mid
print("    gamma  in  [%.15f, %.15f]   (exact bisection on the PSD device)" % (float(lo), float(hi)))
print("    g_ub       %.15f" % float(G_UB))
print("    g_ub - gamma  in  [%.4e, %.4e]" % (float(G_UB - hi), float(G_UB - lo)))
check("the bracket confirms gamma < g_ub", hi < G_UB, True)
print()
print("    NOTE.  g_ub sits 4.1e-11 above gamma -- cb417 bisected it hard.  That is in")
print("    the SAFE direction for everything downstream: (F) needs gamma < M^2/2 and")
print("    (M#) needs sweep > 2*gamma, and BOTH get harder as g_ub is raised, so an")
print("    upper bound on gamma that is loose can only weaken the claim, never inflate it.")

print()
banner("a2 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
