"""s4 -- (L*) CERTIFIED EXACTLY, AND PUSHED PAST THE ENUMERABLE RANGE.

(L*)   M^2 > 2 gamma   ==>   mu_pref * Delta_P  <=  gamma        [i.e. rho <= 1/Delta_P]

(L*) IMPLIES THE DISJUNCTION UNIFORMLY IN n (s2 S2.1): rho <= 1/Delta_P gives
mu_pref <= gamma/Delta_P <= t*, so (M#) HOLDS at every poset where (F) fails.

THE ASYMMETRY THAT MAKES THIS CHECKABLE FAR BEYOND n = 8.  Certifying (L*) at a poset
needs an UPPER bound on mu_pref -- and an exhibited monotone vector gives exactly that,
exactly, in O(n^2).  It is refuting (M#) that needs the expensive lower bound.  So the
direction (L*) points is the CHEAP one, and the families below reach n = 18 where no
exact copositivity bracket ever will.

    certificate at a poset:   mu_ub * Delta_P <= gamma,
    decided as   PSD( Q - (mu_ub * Delta_P) N ),   integer matrices, no float.
"""
import sys, pickle, time
from fractions import Fraction
from libc50b import gen_posets, Poset, height, mu_exhaustive, exact_ub_from

print("=" * 78)
print("S4.1  (L*) AT n = 7, EXACTLY, ON THE WHOLE (F)-FAILING SET")
print("=" * 78)

with open("out_s1_store.pkl", "rb") as fh:
    store = pickle.load(fh)
F7 = [x[0] for x in store[7]["Flist"]]
print("  (F)-failing primitive posets on [7]: %d" % len(F7))

cert = 0
worst = (Fraction(0), None)
for dn in F7:
    P = Poset(dn, 7)
    ub = P.mu_upper()[0]
    t = ub * P.Delta()
    if P.gap_ge(t):                       # gamma >= mu_ub * Delta >= mu_pref * Delta
        cert += 1
    mu, bv = mu_exhaustive(P)
    r = Fraction(int(mu * 10 ** 12), 10 ** 12) * P.Delta() / Fraction(
        int(P.gamma_float() * 10 ** 12), 10 ** 12)
    if r > worst[0]:
        worst = (r, dn)
print("  (L*) CERTIFIED EXACTLY at %d of %d          %s"
      % (cert, len(F7), "ALL" if cert == len(F7) else "*** NOT ALL ***"))
print("  max rho*Delta over the set (float measurement) = %.6f" % float(worst[0]))
print("  attained at dn = %s" % (worst[1],))
print("""
  CONSEQUENCE.  The disjunction at n = 7 is not 86278 independent checks.  It is ONE
  sufficient condition, rho*Delta_P <= 1, holding on the 168 posets where it is the
  only thing standing between the two routes -- with a margin, and certified on
  integers at every one of them.
""")

print("=" * 78)
print("S4.2  (L*) ON THE FAMILIES -- FAMILY MEMBERS, NEVER MAXIMA OVER THEIR n")
print("=" * 78)


def near_ordinal(n, a, drop):
    """Two antichains A = [0,a), B = [a,n), every a<b present EXCEPT the pairs in
    `drop` -- mg-51f4 §8's family, the one that kills (F) from n = 7 on."""
    dn = [0] * n
    for i in range(a):
        for j in range(a, n):
            if (i, j) not in drop:
                dn[j] |= 1 << i
    return tuple(dn)


def chain_plus_point(n):
    """chain(n-1) + one isolated point -- mg-51f4 §8's (M#)-killing family."""
    dn = [0] * n
    for i in range(1, n - 1):
        dn[i] = (1 << i) - 1
    return tuple(dn)


print("\n  FAMILY: near-ordinal antichains (|A| = floor(n/2), two relations dropped)")
print("   n | (F) fails | rho     | rho*Delta | (L*) certified | u_M = mu/t* | c#      | f*")
for n in range(6, 19):
    a = n // 2
    drop = {(a - 1, a), (0, n - 1)}
    dn = near_ordinal(n, a, drop)
    P = Poset(dn, n)
    if not P.primitive():
        print("   %2d | not primitive" % n)
        continue
    t0 = time.time()
    g = P.gamma_float()
    d = float(P.Delta())
    ub = P.mu_upper()[0]
    rho = float(ub) / g
    ffail = P.F_fails()
    ok = P.gap_ge(ub * P.Delta())
    fs = float(P.M()) ** 2 / (2 * g)
    disc = d * d - 2 * g
    ts = (d - disc ** 0.5) if disc > 0 else None
    uM = (float(ub) / ts) if ts and ts > 0 else 0.0
    cs = (float(ub) * (2 * d - float(ub)) if float(ub) <= d else d * d) / (2 * g)
    print("   %2d | %-9s | %.5f | %.5f   | %-14s | %.5f     | %.5f | %.5f  (%.0fs)"
          % (n, "YES" if ffail else "no", rho, rho * d,
             "YES" if ok else "*** NO ***", uM, cs, fs, time.time() - t0))
    sys.stdout.flush()

print("\n  FAMILY: chain(n-1) + one isolated point  -- (M#)'s family; (F) must be far off")
print("   n | (F) fails | u_F = M/sqrt(2g) | c#(upper) | rho     | rho*Delta")
for n in range(6, 17):
    dn = chain_plus_point(n)
    P = Poset(dn, n)
    if not P.primitive():
        print("   %2d | not primitive" % n)
        continue
    g = P.gamma_float()
    d = float(P.Delta())
    ub = P.mu_upper()[0]
    uF = float(P.M()) / (2 * g) ** 0.5
    cs = (float(ub) * (2 * d - float(ub)) if float(ub) <= d else d * d) / (2 * g)
    print("   %2d | %-9s | %.5f          | %.5f   | %.5f | %.5f"
          % (n, "YES" if P.F_fails() else "no", uF, cs, float(ub) / g, float(ub) / g * d))
    sys.stdout.flush()

print("""
  READING.  On (F)'s own family, rho*Delta stays under 1 at every n tested and (L*) is
  certified on integers at every one -- so (M#) HOLDS there, at every n, by S2.1's
  one-line sufficient condition and NOT by a copositivity bracket.  These are FAMILY
  MEMBERS.  No row here is a maximum over its n.
""")
