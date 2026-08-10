"""s5 -- EXACT CERTIFICATION OF THE COUNTEREXAMPLES TO (L*).

WHAT HAS TO BE CERTIFIED, AND WHY THE EASY DIRECTION IS THE WRONG ONE.

  (L*) says   M^2 > 2 gamma  ==>  mu_pref * Delta <= gamma.
  To REFUTE it at a poset P we must establish BOTH

      (i)   M^2 > 2 gamma          -- an UPPER bound on gamma
      (ii)  mu_pref * Delta > gamma -- a LOWER bound on mu_pref, and an upper on gamma.

  (ii) is the hard direction and it is exactly the trap mg-51f4 names and mg-c50b's E3
  records: an exhibited monotone vector gives an UPPER bound on mu_pref and can NEVER
  certify that mu_pref is large.  s1's hunt scores with such an upper bound, which is
  correct for SCREENING (it cannot hide a counterexample) and worthless as proof.

  So mu_pref >= s is certified here by EXACT COPOSITIVITY.  In the psi basis
  mu_pref = min over c >= 0 of c'Qc / c'Nc, so

      mu_pref >= s = a/b     <==>     R := Q - s N   is copositive
                             <==>     R_int := b*n*QI - 2*LE*a*NI  is copositive,

  an INTEGER matrix.  Copositivity is decided exactly: the minimum of c'R c over the
  standard simplex is attained at a point whose support S has all coordinates positive,
  and there the first-order condition is R_S c_S = t*1 with value exactly t.  Enumerating
  every support S and taking the least feasible t decides the sign with no floating point
  anywhere.  A singular R_S is REFUSED rather than guessed at.

  gamma < g is certified by the same integer PSD device the corpus already uses: gamma >= g
  iff b*n*(2*LE*I - AI) - 2*LE*a*(n*I - J) is PSD, so its FAILURE certifies gamma < g.

  Then  mu_pref * Delta  >=  s * Delta  >  g  >  gamma  closes (ii) in exact rationals.
"""

import sys, time
from itertools import combinations
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import P789, height, fam_chain_plus_points


def psi_QI(P):
    n, m = P.n, P.n - 1
    QI = [[0] * m for _ in range(m)]
    for a in range(m):
        k = a + 1
        for b in range(a, m):
            l = b + 1
            lo, hi = min(k, l), max(k, l)
            s = 0
            for i in range(lo):
                for j in range(hi, n):
                    s += P.AI[i][j]
            QI[a][b] = QI[b][a] = s
    NI = [[n * min(a + 1, b + 1) - (a + 1) * (b + 1) for b in range(m)] for a in range(m)]
    return QI, NI


def solve_exact(Ain, bin_, k):
    """Solve A x = b exactly.  Returns x, or None if A is singular."""
    A = [[Fraction(Ain[i][j]) for j in range(k)] + [Fraction(bin_[i])] for i in range(k)]
    for c in range(k):
        p = None
        for r in range(c, k):
            if A[r][c] != 0:
                p = r
                break
        if p is None:
            return None
        A[c], A[p] = A[p], A[c]
        pv = A[c][c]
        A[c] = [x / pv for x in A[c]]
        for r in range(k):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [A[r][j] - f * A[c][j] for j in range(k + 1)]
    return [A[i][k] for i in range(k)]


def copositive_exact(R, m):
    """EXACT.  Returns (verdict, min_simplex_value) with verdict in
    {'COPOSITIVE', 'NOT', 'REFUSE'}.  REFUSE only on a singular face."""
    best = None
    for r in range(1, m + 1):
        for S in combinations(range(m), r):
            RS = [[R[i][j] for j in S] for i in S]
            x = solve_exact(RS, [1] * r, r)
            if x is None:
                return "REFUSE", None
            sx = sum(x)
            if sx == 0:
                continue
            t = Fraction(1, 1) / sx
            c = [t * xi for xi in x]
            if any(ci < 0 for ci in c):
                continue
            if best is None or t < best:
                best = t
    if best is None:
        return "REFUSE", None
    return ("COPOSITIVE" if best >= 0 else "NOT"), best


def certify(dn, n, label):
    P = P789(dn, n)
    print("-" * 78)
    print("  %s   dn = %s" % (label, str(dn)))
    print("    n = %d   height = %d   primitive = %s   LE = %d"
          % (n, height(dn, n), P.primitive(), P.LE))
    D = P.Delta()
    M = P.M()
    print("    Delta = %s   M = %s" % (D, M))

    # ---- (i) (F) fails, exactly -------------------------------------------
    thr = M * M / 2
    Ffails = not P.gap_ge(thr)
    print("    (i)  (F): gamma >= M^2/2 = %s ?  %s   =>  (F) %s"
          % (thr, "yes" if not Ffails else "NO", "FAILS" if Ffails else "holds"))

    # ---- exact upper bound on gamma ---------------------------------------
    g = P.gamma_float()
    ghi = None
    for den in (10 ** 6, 10 ** 7, 10 ** 8):
        cand = Fraction(int(g * den) + 2, den)
        if not P.gap_ge(cand):
            ghi = cand
            break
    print("    exact upper bound   gamma < %s = %.9f   (certified: the PSD test FAILS there)"
          % (ghi, float(ghi)))

    # ---- exact lower bound on mu_pref via copositivity --------------------
    QI, NI = psi_QI(P)
    m = n - 1
    mu = P.mu_faces()[0]
    slo = None
    verdict = None
    for den in (10 ** 5, 10 ** 6, 10 ** 7):
        cand = Fraction(int(mu * den) - 1, den)
        a, b = cand.numerator, cand.denominator
        R = [[b * n * QI[i][j] - 2 * P.LE * a * NI[i][j] for j in range(m)] for i in range(m)]
        v, val = copositive_exact(R, m)
        if v == "COPOSITIVE":
            slo, verdict = cand, v
            break
        if v == "NOT":
            verdict = v
            break
    if slo is None:
        print("    exact lower bound   mu_pref: COULD NOT CERTIFY (%s)" % verdict)
        return False
    print("    exact lower bound   mu_pref >= %s = %.9f   (certified: Q - sN COPOSITIVE)"
          % (slo, float(slo)))

    # ---- the conclusion ----------------------------------------------------
    lhs = slo * D
    print("    (ii) mu_pref * Delta >= %s = %.9f   vs   gamma < %s = %.9f"
          % (lhs, float(lhs), ghi, float(ghi)))
    ok = lhs > ghi
    print("    => mu_pref * Delta %s gamma       %s"
          % (">" if ok else "NOT >", "*** (L*) REFUTED AT THIS POSET ***" if (ok and Ffails)
             else "not a counterexample"))
    return ok and Ffails


print("=" * 78)
print("S5.1  NEGATIVE CONTROLS -- the certifier must REFUSE where (L*) holds")
print("=" * 78)
print("""  Run first, and on posets whose answer the corpus already publishes.  A certifier
  that says 'refuted' everywhere proves nothing; these two must come back NOT refuted.
""")
certify((0, 0, 0, 4, 4, 31, 29), 7, "mg-c50b S4.1 argmax, rho*Delta = 0.923894 -- (L*) HOLDS here")
certify((0, 0, 0, 0, 15, 11, 15), 7, "mg-c50b S2.2 witness, rho = 1 -- (L*) HOLDS here")

print()
print("=" * 78)
print("S5.2  POSITIVE CONTROL -- a poset where mu_pref*Delta > gamma is ALREADY PUBLISHED")
print("=" * 78)
print("""  chain(9) + one isolated point: mg-c50b S4.2 prints rho*Delta = 1.00636 there.  (F)
  HOLDS at it, so it is no counterexample to (L*) -- but the copositivity machinery must
  be able to certify the inequality it does satisfy, or it cannot certify anything.
""")
dn, n = fam_chain_plus_points(9, 1)
certify(dn, n, "chain(9)+point -- mu_pref*Delta > gamma expected, (F) holds so (L*) untouched")

print()
print("=" * 78)
print("S5.3  THE CANDIDATES")
print("=" * 78)
CAND = [((0, 1, 0, 4, 0, 0, 32, 96, 239), 9),
        ((0, 0, 0, 0, 0, 16, 48, 16, 247), 9),
        ((0, 1, 3, 0, 9, 0, 32, 96, 255, 239), 10),
        ((0, 1, 3, 7, 0, 1, 1, 113, 1, 257, 257), 11)]
res = []
for dn, n in CAND:
    t0 = time.time()
    ok = certify(dn, n, "hunt candidate n=%d" % n)
    res.append((n, dn, ok))
    print("    (%.0fs)" % (time.time() - t0))
    sys.stdout.flush()

print()
print("=" * 78)
print("S5.4  VERDICT")
print("=" * 78)
good = [r for r in res if r[2]]
if good:
    print("  (L*) IS FALSE.  Certified counterexamples, exactly, on integers:")
    for n, dn, _ in good:
        print("     n = %2d   dn = %s" % (n, str(dn)))
    print()
    print("  The smallest is n = %d." % min(n for n, _, _ in good))
    print("  (L*) was certified at 168/168 (n=7) and 3589/3589 (n=8); it first fails at n = %d,"
          % min(n for n, _, _ in good))
    print("  which is exactly the first n the corpus had never enumerated.")
else:
    print("  No candidate survived exact treatment.  (L*) stands.")
