#!/usr/bin/env python3
"""a2 — mg-39bf re-solves the four chains from their own Phi bounds.

E6, filed in advance: I must not accept mg-9461's `s1` as confirmation of
mg-9461's chain arithmetic — it is the parent's own route and the ticket
forbids exactly that.  So nothing here reads `code/chain_selection_9461/`.
Each chain is re-derived from the inequality it is defined by, in exact
rationals, and only then compared against the parent's published rows.

The chains, as the corpus defines them:

  (I)  monotone sweep       Phi_pref <= sqrt(2 eps_spec)
  (III) same with a loss    Phi_pref <= sqrt(2 C3 eps_spec)     [Op-Form 4.3 displayed]
  (II) gap form             1 - rho_pref <= C3 (1 - lambda_std) [Op-Form 4.3 gap repair]
  (IV) literal capture      rho_pref >= c * lambda_std          [Prefix-capture, :360-364]

Every chain has to deliver the SAME hypothesis, Step 5's conclusion:

      Delta_1(A_k, A_k^c) = Phi_P(A_k) <= eps_leak

and `eps_dem` is the largest eps_spec for which that is guaranteed.  The
derivations, done here rather than quoted:

  (III):  sqrt(2 C3 eps_spec) <= eps_leak   <=>  eps_spec <= eps_leak^2/(2 C3)
  (II):   dictionary Phi <= 1-rho, so Phi_pref <= C3 (1-lambda_std) <= C3 eps_spec;
          C3 eps_spec <= eps_leak            <=>  eps_spec <= eps_leak/C3
  (IV):   Phi_pref <= 1 - rho_pref <= 1 - c*lambda_std <= 1 - c(1 - eps_spec)
          = (1-c) + c*eps_spec;
          (1-c) + c*eps_spec <= eps_leak     <=>  eps_spec <= (eps_leak - (1-c))/c

`E2` guard, live rather than asserted: a `Spec` handed where a `Leak` belongs
raises.  `E7` guard: every printed figure carries its unit.
"""

from fractions import Fraction as F
import sys

FAILURES = []


def fail(m):
    FAILURES.append(m)
    print("  *** FAIL: %s" % m)


class Leak(F):
    """eps_leak — a Delta_1 budget.  Distinct type from Spec on purpose."""
    unit = "eps_leak"


class Spec(F):
    """eps_spec — a spectral budget.  Reaches eps_leak through a SQUARE."""
    unit = "eps_spec"


def _need_leak(x, where):
    if not isinstance(x, Leak):
        raise TypeError("%s: expected a Leak (eps_leak), got %r — this is the "
                        "normalisation trap mg-d3c7 named; the two differ by a "
                        "Cheeger SQUARE" % (where, type(x).__name__))


def dem_III(eps_leak, C3):
    """eps_dem for chain (III) (= chain (I) at C3 = 1)."""
    _need_leak(eps_leak, "dem_III")
    return Spec(F(eps_leak) ** 2 / (2 * F(C3)))


def dem_II(eps_leak, C3):
    """eps_dem for chain (II), the gap form.  Never pays the Cheeger square."""
    _need_leak(eps_leak, "dem_II")
    return Spec(F(eps_leak) / F(C3))


def dem_IV(eps_leak, c):
    """eps_dem for chain (IV), literal prefix capture.  May be <= 0."""
    _need_leak(eps_leak, "dem_IV")
    return Spec((F(eps_leak) - (1 - F(c))) / F(c))


def close_threshold_IV(eps_leak):
    """Smallest c at which chain (IV) closes AT ALL (eps_dem > 0)."""
    return 1 - F(eps_leak)


def parity_threshold_IV(eps_leak, C3=1):
    """Smallest c at which chain (IV) delivers the budget chain (III) publishes.

    Fix eps_spec at chain (III)'s own demand and ask what c chain (IV) needs to
    reach the SAME eps_leak there.  This is a DIFFERENT question from 'does it
    close at all', and the two answers are different numbers.
    """
    es = dem_III(eps_leak, C3)
    # (1-c) + c*es <= eps_leak  <=>  c >= (1 - eps_leak)/(1 - es)
    return (1 - F(eps_leak)) / (1 - F(es))


def main():
    L = Leak(1, 5)
    print("SETTING:  eps_leak = %s = %s  [unit: eps_leak, a Delta_1 budget]"
          % (L, float(L)))

    print("\nE2 GUARD, FIRED LIVE — a Spec where a Leak belongs must RAISE")
    try:
        dem_III(Spec(1, 50), 1)
        fail("E2 guard did NOT fire: a Spec was accepted as a Leak")
    except TypeError as e:
        print("  raised as required: %s" % str(e)[:70] + "...")

    print("\nA — chain (III)/(I): eps_dem = eps_leak^2/(2 C3)   [unit: eps_spec]")
    for C3 in (1, 2, F(3, 2), 3):
        print("  C3 = %-4s  eps_dem = %-12s = %.6g"
              % (C3, dem_III(L, C3), float(dem_III(L, C3))))
    if dem_III(L, 1) != F(1, 50):
        fail("chain (III) at C3=1 is %s, parent publishes 1/50" % dem_III(L, 1))
    else:
        print("  -> C3 = 1 gives 1/50 = 2e-02.  Parent's headline REPRODUCES.")

    print("\nB — chain (II) gap form: eps_dem = eps_leak/C3   [unit: eps_spec]")
    for C3, tag in ((1, "C3=1"), (F(3, 2), "measured n=3"),
                    (F(1193, 500), "measured n=6, 2.386")):
        print("  %-16s C3 = %-8s eps_dem = %-10s = %.6g"
              % (tag, C3, dem_II(L, C3), float(dem_II(L, C3))))

    print("\nC — THE 10x, RE-DERIVED AS AN IDENTITY (does C3 really cancel?)")
    print("    ratio (II)/(III) = (eps_leak/C3) / (eps_leak^2/(2 C3)) = 2/eps_leak")
    ok = True
    for C3 in (1, F(3, 2), F(7, 3), 10, F(1193, 500), 99):
        r = dem_II(L, C3) / dem_III(L, C3)
        if r != 2 / F(L):
            ok = False
            fail("ratio at C3=%s is %s, not 2/eps_leak = %s" % (C3, r, 2 / F(L)))
    if ok:
        print("    ratio = %s = %s at every C3 tested (6 values incl. 1193/500)."
              % (2 / F(L), float(2 / F(L))))
        print("    C3 CANCELS — the identity holds.  (mg-94c3's figure, cited")
        print("    not re-derived per the ticket; what is re-derived is that it")
        print("    is C3-INDEPENDENT, which is the load-bearing part.)")

    print("\nD — chain (IV), literal capture: eps_dem = (eps_leak-(1-c))/c")
    print("    [unit: eps_spec]")
    for c, tag in ((1, "c = 1, most permissive"),
                   (F(9, 10), "c = 9/10"),
                   (F(40, 49), "c = 40/49"),
                   (F(4, 5), "c = 4/5 — the close threshold"),
                   (F(3, 4), "c = 3/4 — the MEASURED min c at n=3")):
        d = dem_IV(L, c)
        print("  %-30s eps_dem = %-10s = %-10.6g %s"
              % (tag, d, float(d), "" if d > 0 else "<-- DOES NOT CLOSE"))
    for c, expect in ((1, F(1, 5)), (F(9, 10), F(1, 9)), (F(40, 49), F(1, 50))):
        if dem_IV(L, c) != expect:
            fail("chain (IV) at c=%s is %s, parent publishes %s"
                 % (c, dem_IV(L, c), expect))
    print("  -> all three of the parent's chain (IV) rows REPRODUCE exactly.")

    print("\nE — THE TWO DIFFERENT THRESHOLDS ON c, WHICH THE PARENT CONFLATES")
    print("    The ticket asks: does chain (IV) fail to CLOSE unless c >= 40/49?")
    print()
    print("  %-10s %-24s %-24s" % ("eps_leak", "closes at all if c >", "matches (III)'s budget if c >="))
    for lk in (F(1, 5), F(1, 7), F(17, 78), F(1, 50)):
        print("  %-10s %-24s %-24s"
              % (lk, close_threshold_IV(lk), parity_threshold_IV(Leak(lk))))
    ct = close_threshold_IV(L)
    pt = parity_threshold_IV(L)
    print()
    print("  At eps_leak = 1/5 the two numbers are %s = %.6g and %s = %.6g."
          % (ct, float(ct), pt, float(pt)))
    print("  They are NOT the same number, and 40/49 is the SECOND one.")
    d_at_close = dem_IV(L, ct + F(1, 1000))
    print("  Proof that 40/49 is not the closure threshold: at c = 4/5 + 1/1000,")
    print("  strictly below 40/49, chain (IV) gives eps_dem = %s = %.3g > 0."
          % (d_at_close, float(d_at_close)))
    if d_at_close <= 0:
        fail("chain (IV) does not close just above 4/5 — my derivation is wrong")
    else:
        print("  So chain (IV) DOES close there.  It closes worse than chain")
        print("  (III) — %.3g against 1/50 = 0.02 — but 'does not close AT ALL'"
              % float(d_at_close))
        print("  is false of it.  The parent's own 5.3 states this correctly.")

    print("\nF — THE PARENT'S 5.4 DISTANCE TABLE, RE-COMPUTED  (eps_sup = 1)")
    sup = F(1)
    rows = [("(I)=(III) C3=1", dem_III(L, 1), F(50)),
            ("(III) C3=2", dem_III(L, 2), F(100)),
            ("(II) C3=3/2", dem_II(L, F(3, 2)), F(15, 2)),
            ("(II) C3=2.386", dem_II(L, F(1193, 500)), None),
            ("(IV) c=40/49", dem_IV(L, F(40, 49)), F(50)),
            ("(IV) c=9/10", dem_IV(L, F(9, 10)), F(9)),
            ("(IV) c=1", dem_IV(L, 1), F(5))]
    for tag, dem, expect in rows:
        r = sup / F(dem)
        mark = ""
        if expect is not None:
            mark = "OK" if r == expect else "MISMATCH (parent: %s)" % expect
            if r != expect:
                fail("%s ratio %s != parent's %s" % (tag, r, expect))
        else:
            mark = "%.4g (parent: ~11.9)" % float(r)
        print("  %-18s eps_dem = %-10s  eps_sup/eps_dem = %-10s %s"
              % (tag, dem, r, mark))

    print("\nG — THE THRESHOLD n >= 4 C3/eps_leak^2 - 1")
    n = 4 * F(1) / F(L) ** 2 - 1
    print("  at C3 = 1, eps_leak = 1/5:  n >= %s   (parent/corpus: 99)" % n)
    if n != 99:
        fail("threshold is %s, corpus says 99" % n)

    print("\nH — THE OPTIMISM ARITHMETIC OF 4.3, DIRECTION CHECKED ROW BY ROW")
    print("  All values below are in the eps_leak unit; none is an eps_spec.")
    ceilings = [("uniform surrogate, REQUIRED scope, uniform in n", F(0),
                 "mg-d3c7 infinite family"),
                ("uniform surrogate, REQUIRED scope, n <= 7", F(1, 7),
                 "mg-d3c7 sweep"),
                ("uniform surrogate, RESTRICTED scope (both sides non-chain), "
                 "n <= 7", F(17, 78), "mg-3969, scope-limited")]
    for name, val, prov in ceilings:
        if val == 0:
            rel = "above by everything (0.20 > 0)"
            direction = "OPTIMISTIC"
        else:
            excess = (F(L) - val) / val
            rel = "%.4g%% %s" % (abs(float(excess)) * 100,
                                 "above" if excess > 0 else "BELOW")
            direction = "OPTIMISTIC" if excess > 0 else "CONSERVATIVE"
        print("  %-62s ceiling %-8s  0.20 is %-16s -> %s"
              % (name[:62], val, rel, direction))
    excess7 = (F(L) - F(1, 7)) / F(1, 7)
    print()
    print("  The headline: 0.20 vs 1/7 -> excess = %s = %.4g -> %s%% above."
          % (excess7, float(excess7), float(excess7) * 100))
    if excess7 != F(2, 5):
        fail("the 40%% is %s, not 2/5" % excess7)
    else:
        print("  EXACTLY 40%. The parent's headline arithmetic is CORRECT.")
    print()
    print("  BUT the third row runs the OTHER WAY: 0.20 < 17/78, so against")
    print("  that ceiling 0.20 is CONSERVATIVE, not optimistic.  The parent's")
    print("  TABLE says so inline; the parent's COMMIT SUBJECT says it 'ERRS")
    print("  OPTIMISTIC IN EVERY READING WHERE A COMPARISON EXISTS' and simply")
    print("  omits this row.  17/78's scope: both-sides-non-chain cuts only,")
    print("  which is NOT the scope Step 6 must survive — so the row is not a")
    print("  safety margin, and that is exactly why it must stay visible.")

    print("\n" + "=" * 72)
    if FAILURES:
        print("RESULT: %d FAILURE(S)" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        return 1
    print("RESULT: every published chain figure re-derived from its own Phi")
    print("bound and REPRODUCED.  One conflation found and localised (E).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
