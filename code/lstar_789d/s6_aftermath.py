"""s6 -- WHAT THE REFUTATION OF (L*) DOES AND DOES NOT COST.

(L*) is a SUFFICIENT condition for the disjunction, not an equivalent one.  Refuting it
removes the only uniform-in-n route currently standing; it does NOT refute the
disjunction, and the first thing to do is check whether the disjunction survives at the
very posets that kill (L*).  If it did not, this would be a much larger result and would
have to be reported as one.  It does survive, and that is measured here, not assumed.

Also here: how hard the n = 8 boundary was pushed, since mg-c50b's n = 8 statement about
(L*) is over the SURVIVORS of a 0.85 screen (their own s5 scoping note), not over a
census -- so "first failure at n = 9" is a statement about what has been EXHIBITED, and
the n = 8 question is left open rather than closed by assertion.
"""

import sys, time, math, random
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import P789, gen_posets, height, relabel_natural

random.seed(4242)

CE = [((0, 1, 0, 4, 0, 0, 32, 96, 239), 9),
      ((0, 1, 3, 0, 9, 0, 32, 96, 255, 239), 10),
      ((0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11)]

print("=" * 78)
print("S6.1  DOES THE DISJUNCTION SURVIVE AT THE COUNTEREXAMPLES?")
print("=" * 78)
print("""  mg-c50b's reduction, inherited exactly:
     (F)  fails  <=>  M > sqrt(2 gamma)
     (M#) fails  <=>  Delta^2 > 2 gamma  AND  mu_pref > t* = Delta - sqrt(Delta^2 - 2 gamma)
  The disjunction holds at P iff at least one of the two routes holds.
""")
print("   n | v_F     | v_L     |  t*      | mu_pref  | u_M=mu/t* | (M#)   | disjunction")
for dn, n in CE:
    P = P789(dn, n)
    g = P.gamma_float()
    D = float(P.Delta())
    M = float(P.M())
    mu = P.mu_faces()[0]
    vF = M * M / (2 * g)
    vL = mu * D / g
    disc = D * D - 2 * g
    tstar = D - math.sqrt(disc) if disc > 0 else float("inf")
    uM = mu / tstar
    mfails = disc > 0 and mu > tstar
    print("  %2d | %.5f | %.5f | %.6f | %.6f | %9.5f | %s | %s"
          % (n, vF, vL, tstar, mu, uM, "FAILS" if mfails else "HOLDS",
             "SURVIVES" if (vF <= 1 or not mfails) else "*** BOTH ROUTES FAIL ***"))
print()
print("""  READING.  (M#) HOLDS at every one, with u_M = mu_pref/t* well below 1, so the
  disjunction is untouched.  What died is the ROUTE: (L*) was the one-line sufficient
  condition that delivered the disjunction uniformly in n, and it is false from n = 9.
  The disjunction itself now has no uniform-in-n proof again -- it has the n <= 8
  enumerations and nothing else.""")
sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S6.2  HOW MANY, AND HOW BAD, AT n = 9 -- is the n=9 counterexample a fluke?")
print("=" * 78)


def score(P):
    g = P.gamma_float()
    if g <= 1e-13:
        return None
    M = float(P.M())
    D = float(P.Delta())
    mu = P.mu_ub_float()[0]
    if mu == float("inf"):
        return None
    return (M * M / (2.0 * g), mu * D / g)


def neighbours(dn, n):
    out = []
    for i in range(n):
        m = dn[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            rel = list(dn)
            rel[i] = dn[i] & ~(1 << j)
            d2 = relabel_natural(rel, n)
            if d2 is not None:
                out.append(d2)
    for i in range(n):
        for j in range(i):
            if dn[i] >> j & 1:
                continue
            rel = list(dn)
            rel[i] = dn[i] | (1 << j)
            d2 = relabel_natural(rel, n)
            if d2 is not None:
                out.append(d2)
    for k in range(n - 1):
        if dn[k + 1] >> k & 1:
            continue
        perm = list(range(n))
        perm[k], perm[k + 1] = perm[k + 1], perm[k]
        rel = [0] * n
        for i in range(n):
            m, mask = dn[i], 0
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= 1 << perm.index(j)
            rel[perm.index(i)] = mask
        d2 = tuple(rel)
        if all(d2[i] >> i == 0 for i in range(n)):
            out.append(d2)
    return out


def random_start(n):
    while True:
        dn = []
        for i in range(n):
            mask = 0
            for j in range(i):
                if random.random() < 0.35:
                    mask |= 1 << j
            m = mask
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                mask |= dn[j]
            dn.append(mask)
        dn = tuple(dn)
        P = P789(dn, n)
        if P.primitive() and P.gamma_float() > 1e-12:
            return dn


for n, restarts in ((8, 60), (9, 40)):
    t0 = time.time()
    found = set()
    bestJ, bestdn = -1.0, None
    for r in range(restarts):
        dn = random_start(n)
        s = score(P789(dn, n))
        cur = min(s) if s else -1.0
        for _ in range(80):
            improved = False
            for d2 in neighbours(dn, n):
                P2 = P789(d2, n)
                if not P2.primitive():
                    continue
                s2 = score(P2)
                if s2 is None:
                    continue
                if min(s2) > cur + 1e-12:
                    cur, dn, s = min(s2), d2, s2
                    improved = True
            if not improved:
                break
        if cur > 1.0:
            found.add(dn)
        if cur > bestJ:
            bestJ, bestdn = cur, dn
    print("  n = %d : %d restarts, %d distinct local optima above 1, best min(v_F,v_L) = %.6f"
          % (n, restarts, len(found), bestJ))
    print("           best at %s   (%.0fs)" % (str(bestdn), time.time() - t0))
    if n == 8 and bestJ <= 1.0:
        print("           n = 8: the search did NOT reach 1.  That is a SEARCH RESULT, not a")
        print("           census -- n = 8 has 2600369 primitive posets and this examined a")
        print("           vanishing fraction.  Whether (L*) already fails at n = 8 is OPEN.")
    sys.stdout.flush()

print()
print("=" * 78)
print("S6.3  THE STRUCTURE OF THE n = 9 COUNTEREXAMPLE")
print("=" * 78)
dn, n = CE[0]
P = P789(dn, n)
print("  dn = %s      LE = %d   height = %d" % (str(dn), P.LE, height(dn, n)))
print("  covers (j < i):")
for i in range(n):
    pred = [j for j in range(n) if dn[i] >> j & 1]
    print("     %d  >  %s" % (i, pred if pred else "-"))
print()
print("  d_i = 1 - (S_P)_ii  (Delta is the max):")
print("     " + "  ".join("%d:%.4f" % (i, P.dI[i] / P.LE) for i in range(n)))
print("  leak(A_k)/min(k,n-k) = phi_k:")
print("     " + "  ".join("%d:%.4f" % (k, P.LK[k] / P.LE / min(k, n - k)) for k in range(1, n)))
print()
print("""  READING.  Delta = 62/63: element 5 sits at position 5 with probability 1/63, i.e.
  the poset carries a nearly-free element -- the rho > 1 mechanism -- while the rest of
  it carries a thin cut, the (F)-failing mechanism.  mg-c50b's two families each ran ONE
  of these; the counterexample runs BOTH, which is why neither family found it.""")
