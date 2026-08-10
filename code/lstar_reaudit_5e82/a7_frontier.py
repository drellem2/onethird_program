"""a7 -- BEYOND THE TICKET: the frontier rows cb417 landed while this audit was running.

WHY THIS ARM EXISTS.  mg-5e82 was filed against ONE claim -- both routes failing at
mg-5cba's C5, n = 12.  cb417's landing (main 5e31a13) is larger than the claim the
ticket describes: it certifies 26 posets at n = 10..14 and moves the ONSET from 12 to
10.  Its marker says 'Every verdict in this tree is CERTIFIED-PENDING-AUDIT', so a
verdict that re-certified only C5 would license removing a marker over work it never
looked at.

THE n = 10 ROW IS ALSO THE MOST EXPOSED THING IN THE TREE, and by a wide margin:

    n = 10   min(c#, f*) = 1.000546      margin over 1:  5.5e-4
    n = 12   min(c#, f*) = 1.022616      margin over 1:  2.3e-2      (the ticket's)

-- a factor of 42 tighter, carrying the more consequential claim (the onset), on the
same instrument.  So it is re-certified here on this instrument too.

NOTHING IS QUOTED FROM cb417 EXCEPT THE POSETS.  The bounds are this audit's own:
gamma's upper bound is the smallest bisection point at which the PSD device REFUSES,
mu_pref's lower bound the largest at which the copositivity device ACCEPTS -- so each
is certified in its hard direction by the same devices a2 and a3 use, and cb417's
rationals are never read.

AND THE n = 9 ROW IS A NEGATIVE CONTROL.  cb417's own table says its best n = 9
champion does NOT refute the disjunction.  An instrument that manufactured route
failures would refute it here.
"""
import sys
import time
from fractions import Fraction as Fr
from common5e82 import banner, isqrt_frac
import lib5e82 as L

ok = True


def check(label, got, want):
    global ok
    good = got == want
    ok = ok and good
    print("  [%s] %-58s got=%s want=%s" % ("ok " if good else "FAIL", label, got, want))


# (n, dn, does cb417's out_b4_certify.txt say it refutes the disjunction?)
ROWS = [
    (9, (0, 1, 0, 0, 8, 8, 56, 125, 127), False),
    (10, (0, 0, 0, 7, 15, 31, 15, 6, 135, 135), True),
    (11, (0, 0, 0, 7, 15, 15, 63, 6, 135, 135, 647), True),
]

banner("a7  THE FRONTIER ROWS, RE-CERTIFIED ON THIS INSTRUMENT")
for n, dn, expect in ROWS:
    t0 = time.time()
    P = L.Poset(dn, n)
    print()
    print("-" * 78)
    print("  n = %d   dn = %s" % (n, dn))
    print("  LE = %d   Delta = %s   M = %s   primitive = %s   naturally labelled = %s"
          % (P.LE, P.Delta, P.M, P.primitive, P.natural))
    check("  transitively closed", P.transitive, True)
    check("  primitive", P.primitive, True)

    # gamma: bisect the PSD device.  `ghi` is a point where R REFUSES PSD, so
    # gamma < ghi is CERTIFIED by an exhibited vector, exactly as in a2.
    glo, ghi = Fr(0), Fr(1)
    for _ in range(46):
        mid = (glo + ghi) / 2
        if L.is_psd(P.R(mid.numerator, mid.denominator)):
            glo = mid
        else:
            ghi = mid
    # mu_pref: bisect the copositivity device.  `mlo` is a point where R IS
    # copositive, so mu_pref >= mlo is CERTIFIED, exactly as in a3.
    mlo, mhi = glo, Fr(1)
    for _ in range(40):
        mid = (mlo + mhi) / 2
        if L.is_copositive(P.R(mid.numerator, mid.denominator)):
            mlo = mid
        else:
            mhi = mid
    print("  gamma   < %.12f   [PSD device REFUSES here]" % float(ghi))
    print("  mu_pref >= %.12f   [copositivity device ACCEPTS here]" % float(mlo))
    check("  the two brackets are consistent (gamma <= mu_pref)", glo <= mhi, True)

    D, M = P.Delta, P.M
    f_fails = ghi <= M * M / 2                      # gamma < M^2/2
    sweep = 2 * D * mlo - mlo * mlo
    m_fails = (mlo <= D) and (sweep > 2 * ghi)      # and mu_pref <= Delta, below
    mu_ub = min(P.Q[k][k] / P.N[k][k] for k in range(P.m))
    print("  M^2/2 = %.12f     f* > %.9f" % (float(M * M / 2), float((M * M / 2) / ghi)))
    print("  sweep(m_lo,Delta) - 2*gamma_ub = %+.12f    c# > %.9f"
          % (float(sweep - 2 * ghi), float(sweep / (2 * ghi))))
    print("  mu_pref <= %.9f (exhibited c = e_k) <= Delta = %.9f : %s"
          % (float(mu_ub), float(D), mu_ub <= D))
    check("  mu_pref <= Delta, so the sweep is monotone across the bracket", mu_ub <= D, True)
    print("  (F) FAILS : %s      (M#) FAILS : %s      refutes the disjunction : %s"
          % (f_fails, m_fails, f_fails and m_fails))
    check("  agrees with cb417's out_b4_certify.txt on this row",
          f_fails and m_fails, expect)
    print("  [%.1fs]" % (time.time() - t0))

print()
print("""
  WHAT THIS ARM DOES AND DOES NOT SETTLE.

  SETTLED: the ONSET row.  Both routes fail at a primitive, naturally labelled,
  transitively closed poset on TEN elements, re-derived here with no rational read
  from cb417 -- so 'the disjunction is false' does not depend on n = 12 and does not
  depend on lib5cba.  The n = 9 row comes back NOT refuting, on the same devices, so
  the instrument is not answering YES by habit.

  NOT SETTLED: the other 23 certified posets, the W(n) rows at n = 13 and n = 14, the
  0-of-36 refusal count, the 93.8%/6.2% decomposition, and the u_M = v_L*D identity.
  None of those was re-run here.  A marker on cb417's tree can be narrowed to them;
  it cannot simply be deleted on the strength of this audit.""")
print()
banner("a7 VERDICT: %s" % ("ALL ARMS SATISFACTORY" if ok else "*** AN ARM FAILED ***"))
sys.exit(0 if ok else 1)
