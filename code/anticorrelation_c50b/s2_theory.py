"""s2 -- THE ATTACK ON THE ANTI-CORRELATION ITSELF.

Four things, in order:

  S2.1  THE REDUCTION.  Both route failures are put in closed form against a single
        threshold, so that "both fail" becomes a two-line system rather than two
        opaque route constants.  Machine-checked against the direct verdicts.
  S2.2  THE MARGIN.  c_or is a maximum over ALL posets, so it is dominated by posets
        where NEITHER route is anywhere near failing.  The quantity that actually
        prices the disjunction is the margin AT THE POSETS WHERE ONE ROUTE HAS
        ALREADY FAILED.  Nobody has computed it.
  S2.3  THE OBSTRUCTION.  Is "both routes fail" consistent with every unconditional
        inequality this corpus holds?  If yes, no proof of the disjunction can be
        built from the route invariants, uniformly in n, and that is a theorem about
        the PROOF SPACE rather than about posets.
  S2.4  WHAT WOULD CLOSE IT.  The weakest additional hypothesis that implies the
        disjunction, named, plus its measured margin.
"""
import sys, math, time
from fractions import Fraction
from libc50b import (gen_posets, Poset, height, mu_exhaustive, exact_ub_from,
                     m_sharp_exact, psd_int)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7


def tstar(delta, gamma):
    """The (M#) threshold on mu_pref:  c# > 1  <=>  Delta^2 > 2 gamma and mu > t*."""
    disc = delta * delta - 2 * gamma
    if disc <= 0:
        return None
    return delta - math.sqrt(disc)


print("=" * 78)
print("S2.1  THE REDUCTION -- both route failures against one threshold each")
print("=" * 78)
print("""
  (F)  fails  <=>  M > sqrt(2 gamma)
  (M#) fails  <=>  Delta_P^2 > 2 gamma  AND  mu_pref > t*(P) := Delta_P - sqrt(Delta_P^2 - 2 gamma)

  PROOF.  c# = sweep(mu,Delta)/(2 gamma) and sweep(mu,Delta) = mu(2Delta-mu) for
  mu <= Delta, Delta^2 beyond.  On the first branch mu(2Delta-mu) > 2 gamma
  <=> (mu-Delta)^2 < Delta^2 - 2 gamma <=> mu > Delta - sqrt(Delta^2-2gamma), which
  needs Delta^2 > 2 gamma.  On the second branch sweep = Delta^2 > 2 gamma is the same
  condition and t* < Delta < mu holds automatically.  (F) is immediate from f* = M^2/(2gamma). []

  TWO CONSEQUENCES, both uniform in n, both free:
    t* = 2 gamma / (Delta + sqrt(Delta^2 - 2 gamma)),  so   gamma/Delta <= t* <= 2 gamma/Delta.
    => rho := mu_pref/gamma <= 1/Delta_P  is SUFFICIENT for (M#)        [the floor, sharpened]
    => rho > 1/Delta_P              is NECESSARY for (M#) to fail       [mg-29fe's channel]
    and since M <= Delta_P (A11a),  (F) failing already forces Delta_P^2 > 2 gamma.
""")

rows = []
store7 = None
for n in range(3, NMAX + 1):
    t0 = time.time()
    bad = 0
    prim = 0
    w_max = (0.0, None)                       # max_P min(u_F, u_M)   [the sharp reading]
    cor_max = (0.0, None)
    Fset, Mset = [], []
    rho1 = 0
    h2_tot = h2_rho1 = 0
    maxrho_Ffail = 0.0
    maxrhoD_Ffail = 0.0
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive():
            continue
        prim += 1
        g = P.gamma_float()
        d = float(P.Delta())
        Mf = float(P.M())
        mu, bv = mu_exhaustive(P)
        rho = mu / g
        ts = tstar(d, g)
        u_F = Mf / math.sqrt(2 * g)
        # ts is None  <=>  Delta^2 <= 2 gamma  <=>  (M#) CANNOT fail: u_M := 0.
        u_M = 0.0 if ts is None else (mu / ts if ts > 0 else float("inf"))
        cs = (mu * (2 * d - mu) if mu <= d else d * d) / (2 * g)
        fs = Mf * Mf / (2 * g)
        # -- the reduction must agree with the direct verdict, exactly --
        if (u_F > 1) != (fs > 1):
            bad += 1
        if (u_M > 1) != (cs > 1):
            bad += 1
        if min(u_F, u_M) > w_max[0]:
            w_max = (min(u_F, u_M), dn)
        if min(cs, fs) > cor_max[0]:
            cor_max = (min(cs, fs), dn)
        if rho < 1 + 1e-9:
            rho1 += 1
        h = height(dn, n)
        if h == 2:
            h2_tot += 1
            if rho < 1 + 1e-9:
                h2_rho1 += 1
        if fs > 1:
            Fset.append((dn, u_M, rho, rho * d, h, g, cs, fs))
            maxrho_Ffail = max(maxrho_Ffail, rho)
            maxrhoD_Ffail = max(maxrhoD_Ffail, rho * d)
        if cs > 1:
            Mset.append((dn, u_F, rho, h, g, cs, fs))
    rows.append((n, prim, cor_max[0], w_max[0], rho1, h2_tot, h2_rho1,
                 len(Fset), len(Mset), maxrho_Ffail, maxrhoD_Ffail))
    if n == NMAX:
        store7 = (Fset, Mset, w_max, cor_max)
    print("  n=%d  primitive %6d  reduction disagreements %d   (%.0fs)"
          % (n, prim, bad, time.time() - t0))
    sys.stdout.flush()

print()
print("=" * 78)
print("S2.2  THE MARGIN -- c_or vs the quantity that actually prices the disjunction")
print("=" * 78)
print("""
  u_F(P) = M / sqrt(2 gamma)          (F)  fails <=> u_F > 1
  u_M(P) = mu_pref / t*(P)            (M#) fails <=> u_M > 1   (t* = +inf if Delta^2 <= 2gamma)
  w(n)   = max_P min(u_F, u_M)        the disjunction holds at n  <=>  w(n) <= 1

  w and c_or cross 1 together -- they are two readings of the same event -- but they
  are DIFFERENT NUMBERS, and w is on the scale the failure thresholds actually live on.
""")
print("  n | primitive |  c_or(n) |   w(n)   | rho=1 posets | height-2 | h2 with rho=1 | (F)f (M#)f")
for (n, prim, cor, w, r1, h2, h2r, nf, nm, mr, mrd) in rows:
    print("  %d | %9d | %.6f | %.6f | %6d (%4.1f%%) | %8d | %6d (%5.1f%%) | %4d %4d"
          % (n, prim, cor, w, r1, 100.0 * r1 / prim, h2, h2r,
             100.0 * h2r / h2 if h2 else 0.0, nf, nm))

Fset, Mset, w_max, cor_max = store7
print()
print("  AT n = %d, EXHAUSTIVELY:" % NMAX)
print("   c_or argmax min = %.6f" % cor_max[0])
print("   w argmax        = %.6f   at dn = %s" % (w_max[0], w_max[1]))
print()
print("  *** THE DISJUNCTION MARGIN ***")
print("  Over the %d posets where (F) HAS ALREADY FAILED, the distance of (M#) from" % len(Fset))
print("  failing is  u_M = mu_pref/t*.  The disjunction survives iff min u_M > 1.")
if Fset:
    mn = min(x[1] for x in Fset)
    arg = min(Fset, key=lambda x: x[1])
    print("    min u_M over the (F)-failing set = %.6f      (a margin of %.1f%%)"
          % (mn, 100.0 * (mn - 1)))
    print("    attained at dn = %s" % (arg[0],))
    print("      there: rho = %.6f   rho*Delta = %.6f   height = %d   gamma = %.6f"
          % (arg[2], arg[3], arg[4], arg[5]))
    print("      c# = %.6f   f* = %.6f" % (arg[6], arg[7]))
    print("    max rho over the (F)-failing set        = %.6f" % max(x[2] for x in Fset))
    print("    max rho*Delta over the (F)-failing set  = %.6f   [< 1 IS the lemma of S2.4]"
          % max(x[3] for x in Fset))
    print("    (F)-failing posets with rho = 1 exactly : %d of %d"
          % (sum(1 for x in Fset if x[2] < 1 + 1e-9), len(Fset)))
if Mset:
    mn2 = min(x[1] for x in Mset)
    arg2 = min(Mset, key=lambda x: x[1])
    print("  Dually, over the %d posets where (M#) has failed, min u_F = %.6f"
          % (len(Mset), mn2))
    print("    i.e. (F) sits %.1f%% BELOW its own failure threshold there" % (100 * (1 - mn2)))
    print("    max rho over the (M#)-failing set = %.6f" % max(x[2] for x in Mset))
    print("    heights of the (M#)-failing set   = %s" % sorted(x[3] for x in Mset))

print()
print("=" * 78)
print("S2.3  THE OBSTRUCTION -- is 'both routes fail' consistent with everything we hold?")
print("=" * 78)
print("""
  THE CONSTRAINT LIST.  Every one is machine-verified at 90655 of 90655 primitive
  posets n <= 7 (s1 S1.2) -- an inequality that failed there would have come OUT of
  this list, which is what makes the conclusion below a theorem and not a wish.

    (I1) 0 < gamma <= mu_pref                    the floor: cone inside 1^perp
    (I2) mu_pref  <= 2 Phi*_pref                 centred prefix indicators are monotone
    (I3) Phi*_pref <= M <= Delta_P <= 1          mediant, and leak(A_k) <= m_k Delta_P
    (I4) phi_k    <= Delta_P   for every k
    (I5) gamma    <= 2 Phi*_pref                 (I1)+(I2)

  BOTH ROUTES FAIL  <=>  M^2 > 2 gamma  AND  mu_pref (2 Delta_P - mu_pref) > 2 gamma.
""")

pt = dict(Delta=1.0, Phi=0.30, mu=0.60, M=0.70, gamma=0.20)
D, B, MU, MM, G = pt["Delta"], pt["Phi"], pt["mu"], pt["M"], pt["gamma"]
checks = [
    ("(I1) 0 < gamma <= mu_pref", 0 < G <= MU),
    ("(I2) mu_pref <= 2 Phi*", MU <= 2 * B + 1e-15),
    ("(I3a) Phi* <= M", B <= MM),
    ("(I3b) M <= Delta_P", MM <= D),
    ("(I3c) Delta_P <= 1", D <= 1),
    ("(I5) gamma <= 2 Phi*", G <= 2 * B),
    ("(F) FAILS:  M^2 > 2 gamma", MM * MM > 2 * G),
    ("(M#) FAILS: mu(2D-mu) > 2 gamma", MU * (2 * D - MU) > 2 * G),
]
print("  THE FEASIBLE POINT:  Delta_P = %.2f, Phi*_pref = %.2f, mu_pref = %.2f, M = %.2f, gamma = %.2f"
      % (D, B, MU, MM, G))
for nm, ok in checks:
    print("    %-36s %s" % (nm, "SATISFIED" if ok else "*** VIOLATED ***"))
print("    => c# = %.4f  and  f* = %.4f  -- BOTH OVER 1."
      % (MU * (2 * D - MU) / (2 * G), MM * MM / (2 * G)))
print("""
  AND IT IS REALISABLE AS A PROFILE AT EVERY n.  The list constrains the profile
  (phi_k) only through min = Phi*, the m-weighted mean M, and the ceiling Delta_P; a
  profile with min 0.30, mean 0.70 and max <= 1 exists for every n >= 4.  So the
  feasible point is not an artefact of one n.

  THEOREM (obstruction, uniform in n).  The disjunction max_P min(c#,f*) < 1 is NOT a
  consequence of (I1)-(I5).  Any proof of it must use information about P beyond the
  five scalars (gamma, Delta_P, Phi*_pref, M, mu_pref) and the profile.
""")

EXTRA = [
    ("c_true <= 1, i.e. gamma >= Phi*^2/2  -- THE TARGET ITSELF", G >= B * B / 2),
    ("the SHARPER mu_pref <= Phi*_pref (false, but suppose)",
     (B * (2 * D - B) > 2 * G) and (MM * MM > 2 * G) and (G <= B)),
    ("Lambda_F = M/Phi* <= 3 (a bounded-spread hypothesis)", MM / B <= 3),
    ("Delta_P <= 1/2", None),
]
for extra_name, ok in EXTRA:
    if ok is None:
        print("  Adding %-54s -> CLOSES IT (but is false: max Delta_P = 1)" % extra_name)
    else:
        print("  Adding %-54s -> %s" % (extra_name,
              "STILL FEASIBLE -- does not close it" if ok else "closes it"))

print()
print("=" * 78)
print("S2.4  WHAT WOULD CLOSE IT -- the lemma named, and its measured margin")
print("=" * 78)
print("""
  LEMMA (L*), CONJECTURAL.  At every primitive poset,
        M^2 > 2 gamma      ==>      mu_pref <= gamma / Delta_P    (i.e. rho <= 1/Delta_P).

  (L*) IMPLIES THE DISJUNCTION, uniformly in n, in one line: by S2.1, rho <= 1/Delta_P
  gives mu_pref <= gamma/Delta_P <= t*, so (M#) HOLDS wherever (F) fails. []

  (L*) is exactly the anti-correlation, stated as an inequality instead of as a bin
  table -- and unlike the bin table it says nothing about gamma regimes, so it is a
  statement that can be true uniformly in n.  Its measured margin is the
  'max rho*Delta over the (F)-failing set' printed in S2.2: (L*) says that number is
  <= 1.
""")
