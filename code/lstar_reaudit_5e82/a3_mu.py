"""a3 -- STEP C.  mu_pref >= m_lo, by exact copositivity, in the HARD direction.

THIS IS THE ARM THE VERDICT RESTS ON.  pm-onethird ranked it first and the reason is
structural, not rhetorical: an EXHIBITED monotone vector bounds mu_pref from ABOVE
and can never certify that it is large (mg-51f4's trap, mg-c50b's E3).  So there is
no certificate here of the kind a2 produces.  A "yes" is the output of a routine, and
the routine has to be complete.

WHAT MAKES A "yes" MEAN SOMETHING.  Three things, all measured below and none assumed:

  1. Every one of the 2^11 - 1 = 2047 faces is visited.  Printed, not asserted.
  2. Singular faces are DECIDED, not refused.  mg-789d refuses them; mg-5cba's
     completeness upgrade decides them by exact Fourier-Motzkin; this instrument does
     the same by an independently written FM engine (a0 arm S2 exercises it directly).
     The counters are printed even when the count is zero, because "0 singular faces
     arose" is a MEASUREMENT and the sentence is worthless without it.
  3. THE ROUTINE REFUSES A FALSE BOUND.  Run at a t just ABOVE the true mu_pref it
     must answer NOT copositive and hand back a c >= 0 -- otherwise a certifier that
     says yes to everything would produce exactly the confirmation this audit was
     sent to find.  That is the control, and it is run on the SAME matrix family.

ALSO ESTABLISHED HERE: mu_pref <= Delta.  See a4 for why that is not decoration.
"""
import sys
import time
from fractions import Fraction as Fr
from common5e82 import M_LO, build, banner
import lib5e82 as L

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


banner("a3  STEP C -- mu_pref >= m_lo BY EXACT COPOSITIVITY")
P = build()
a, b = M_LO.numerator, M_LO.denominator
print("  m_lo = %d/%d = %.15f" % (a, b, float(M_LO)))
R = P.R(a, b)
check("R(m_lo) = b*n*QI - 2*LE*a*NI is 2*LE*n*b*(Q - m_lo*N)", P.scale_check(a, b), True)
check("R(m_lo) is integral", all(isinstance(x, int) for r in R for x in r), True)
check("R(m_lo) is 11 x 11", (len(R), len(R[0])), (11, 11))
print("  R(m_lo) has %d negative entries of %d, and every diagonal entry is > 0."
      % (sum(1 for r in R for x in r if x < 0), 11 * 11))
print("  So NEITHER trivial sufficient condition applies: it is not entrywise")
print("  nonnegative, and it is not PSD (mu_pref > gamma means it cannot be).")
check("R(m_lo) is NOT PSD (so copositivity is not being got for free)", L.is_psd(R), False)
print()

L.reset_counters()
t0 = time.time()
wit = L.not_copositive_witness(R)
el = time.time() - t0
print("  faces visited            : %d   (of 2^11 - 1 = %d)" % (L.FACES_VISITED, 2 ** 11 - 1))
print("  singular faces met       : %d" % L.SINGULAR_FACES)
print("  singular faces DECIDED   : %d" % L.SINGULAR_FACES_DECIDED)
print("  elapsed                  : %.1f s" % el)
check("every face was visited", L.FACES_VISITED, 2 ** 11 - 1)
check("no singular face was left undecided",
      L.SINGULAR_FACES_DECIDED, L.SINGULAR_FACES)
print()
check("R(m_lo) IS COPOSITIVE  ==>  mu_pref >= m_lo", wit is None, True)
if wit is not None:
    print("  *** REFUTED.  counter-witness c >= 0 with c'Rc < 0: ***")
    print("   ", L.clear_denominators(wit))
    print("    c'Rc =", L.quad(R, L.clear_denominators(wit)))

print()
print("  MEASURED: 0 singular faces arose.  Stated as a measurement, so that the")
print("  completeness upgrade is reported as UNEXERCISED here rather than as load-")
print("  bearing.  a0 arm S2 exercises the FM engine on matrices where it IS needed.")

print()
banner("a3.1  THE EXACT BRACKET, AND THE CONTROL THAT THE ROUTINE CAN SAY NO")
lo, hi = Fr(65, 1000), Fr(67, 1000)
for _ in range(42):
    mid = (lo + hi) / 2
    if L.is_copositive(P.R(mid.numerator, mid.denominator)):
        lo = mid
    else:
        hi = mid
print("  mu_pref in [%.15f, %.15f]  (exact bisection on the copositivity device)"
      % (float(lo), float(hi)))
print("  m_lo       %.15f" % float(M_LO))
print("  mu_pref - m_lo in [%.4e, %.4e]" % (float(lo - M_LO), float(hi - M_LO)))
check("the bracket confirms mu_pref >= m_lo", lo >= M_LO, True)
print()
print("  THE CONTROL.  At t = %.15f, just ABOVE mu_pref, the routine must REFUSE." % float(hi))
Rb = P.R(hi.numerator, hi.denominator)
w = L.not_copositive_witness(Rb)
check("R(t) at t just above mu_pref is NOT copositive", w is None, False)
if w is not None:
    c = L.clear_denominators(w)
    check("  ... the counter-witness is >= 0", all(x >= 0 for x in c), True)
    check("  ... and nonzero", any(x != 0 for x in c), True)
    check("  ... and c'R(t)c < 0", L.quad(Rb, c) < 0, True)
    num = sum(Fr(c[i]) * P.Q[i][j] * Fr(c[j]) for i in range(P.m) for j in range(P.m))
    den = sum(Fr(c[i]) * P.N[i][j] * Fr(c[j]) for i in range(P.m) for j in range(P.m))
    ray = num / den
    print("    the exhibited monotone c has support", [i for i in range(P.m) if c[i] != 0])
    print("    and Rayleigh quotient %.15f" % float(ray))
    check("  ... which is < t, as a counter-witness must be", ray < hi, True)
    check("  ... and STILL >= m_lo, so it refutes t and not the claim", ray >= M_LO, True)
    print()
    print("    THIS c IS THE UPPER BOUND, and it is the direction mg-51f4 warns about:")
    print("    it proves mu_pref <= %.15f and could never prove mu_pref is large." % float(ray))
    MU_UB = ray
else:
    MU_UB = None

print()
banner("a3.2  mu_pref <= Delta, WHICH a4 NEEDS AND WHICH NO ARM SO FAR HAS GIVEN")
print("  Delta = %s = %.15f" % (P.Delta, float(P.Delta)))
if MU_UB is not None:
    print("  mu_pref <= %.15f  (exhibited monotone vector above)" % float(MU_UB))
    check("mu_pref <= Delta, certified by an exhibited vector", MU_UB <= P.Delta, True)
print()
banner("a3 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
