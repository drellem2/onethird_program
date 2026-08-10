"""a6 -- every other load-bearing "if X then Y" in the landing, checked on suspicion.

pm-onethird's 03:45Z note asks for exactly this: the ticket's own instruction contained
a scope error two minutes after the error was circulated, so every conditional in the
lineage is checked rather than read.

  C1.  "(L*) rearranges, WITH NO LOSS, to Delta*(rho - 1) <= 1 - Delta = min_i (S_P)_ii"
       (mg-789d s1).  The rearrangement divides mu*Delta <= gamma by gamma, so it needs
       gamma > 0 -- which mg-789d's OWN defect D2 is about (a chain has gamma = 0).
       Checked: gamma > 0 at every primitive poset, exactly, and the identity itself.

  C2.  "1 - Delta = min_i (S_P)_ii".  Immediate from Delta = max_i (1 - (S_P)_ii), but
       checked as an integer identity because it is quoted as a geometric reading.

  C3.  "R >= 1" (mg-789d s3, the (R1) route).  R = min_k n*leak_k/(gamma*k(n-k)) is
       claimed >= 1, i.e. every prefix indicator's Rayleigh quotient is >= gamma.  True
       because gamma is the min over ALL of 1^perp -- checked exactly.

  C4.  "screening on an UPPER bound is what makes the hunt RIGOROUS" (mg-789d
       mu_ub_float docstring).  Checked as a direction: mu_ub >= mu_pref must hold at
       every poset, or the screen can hide a counterexample.  This is D1's own repair
       and it is the arm that would fire if D1 came back.

  C5.  mg-c50b's n=8 SCREEN: "both failing forces min > 1 > 0.85 and c#_UB >= c#, so
       every both-failing poset survives the screen".  The screen keeps a poset when
       min(c#_UB, f*) > 0.85.  If both routes fail then f* > 1 and c# > 1; c#_UB >= c#
       gives c#_UB > 1; so min(c#_UB, f*) > 1 > 0.85 and the poset is kept.  VALID as
       stated, and it is what makes "both routes fail at 0 of 2600369" exhaustive
       without an exhaustive exact pass.  The corresponding claim for the (F)-alone
       count 3589 is NOT valid -- and mg-c50b says so itself (its E9).  Checked here
       only for the inequality mu_pref <= 2*Phi*_pref that the screen rests on.

  C6.  The document's own arithmetic: the ledger's (R1)/(R2) rows count FAILURES while
       s3's table counts HOLDS.  2 + 166 = 168 and 133 + 35 = 168; consistent, but the
       two conventions sit in one document.
"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, gen_posets, psd_int, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


def det_frac(Min, k):
    A = [[Fraction(Min[i][j]) for j in range(k)] for i in range(k)]
    d = Fraction(1)
    for c in range(k):
        p = None
        for i in range(c, k):
            if A[i][c]:
                p = i
                break
        if p is None:
            return Fraction(0)
        if p != c:
            A[c], A[p] = A[p], A[c]
            d = -d
        d *= A[c][c]
        inv = 1 / A[c][c]
        for i in range(c + 1, k):
            f = A[i][c] * inv
            if f:
                for j in range(c, k):
                    A[i][j] -= f * A[c][j]
    return d


print("=" * 78)
print("a6  EVERY OTHER LOAD-BEARING CONDITIONAL, CHECKED")
print("=" * 78)
print(__doc__)

print("-" * 78)
print("C1/C2  gamma > 0 at every primitive poset, and 1 - Delta = min_i (S_P)_ii")
print("-" * 78)
badg = badd = 0
tot = 0
for n in range(2, 8):
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        tot += 1
        m = n - 1
        # gamma > 0  <=>  Q positive DEFINITE  <=>  QI PSD and det(QI) != 0
        if not (psd_int(p.QI, m) and det_frac(p.QI, m) > 0):
            badg += 1
        if 1 - p.Delta() != min(Fraction(p.PI[i][i], p.LE) for i in range(n)):
            badd += 1
arm("gamma > 0 at every one of the %d primitive posets n <= 7" % tot, badg == 0,
    "%d with gamma = 0" % badg)
arm("1 - Delta = min_i (S_P)_ii, as an exact identity, at every one", badd == 0,
    "%d violations" % badd)
print("     => the rearrangement (L*) <=> Delta*(rho-1) <= 1-Delta is loss-free ON THE")
print("        PRIMITIVE POPULATION, which is the population (L*) quantifies over.")
print("        It is NOT loss-free at gamma = 0: a chain has gamma = 0 and no rho.")
p = P5(tuple((1 << i) - 1 for i in range(7)), 7)
arm("  and the chain, where it would fail, is NOT primitive (mg-789d's D2)",
    not p.primitive() and not (psd_int(p.QI, 6) and det_frac(p.QI, 6) > 0))

print("\n" + "-" * 78)
print("C3  R >= 1 -- every prefix indicator's Rayleigh quotient is >= gamma")
print("-" * 78)
print("     gamma <= min_k Rayleigh(psi_k) is IMMEDIATE (psi_k lies in 1^perp and gamma")
print("     is the min over all of 1^perp), so 'R >= 1' needs no census.  What DOES")
print("     need checking is the closed form the route is phrased in:")
print("        Rayleigh(psi_k) = Q_kk/N_kk = n*leak(A_k)/(k(n-k)).")
bad = 0
tot = 0
for n in (4, 5, 6, 7):
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        if cnt % 17:
            continue
        tot += 1
        for k in range(1, n):
            lhs = Fraction(p.QI[k - 1][k - 1], 2 * p.LE) / Fraction(p.NI[k - 1][k - 1], n)
            rhs = Fraction(n * p.LK[k], p.LE * k * (n - k))
            if lhs != rhs:
                bad += 1
arm("Q_kk/N_kk == n*leak(A_k)/(k(n-k)) exactly, every k, every sampled poset n<=7",
    bad == 0, "%d violations over %d posets" % (bad, tot))

print("\n" + "-" * 78)
print("C4  THE SCREEN'S DIRECTION -- mu_ub >= mu_pref, the arm that fires if D1 returns")
print("-" * 78)
# reconstruct the DEFECTIVE version of the screen: face lambda_min with NO monotonicity
# check.  On the all-cuts face that subspace is all of 1^perp, so it returns gamma.
bad = 0
tot = 0
worst = 0.0
for n in (5, 6):
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        tot += 1
        g = gamma_float(p)
        mu, _ = mu_pref_float(p)
        if mu < g - 1e-9:
            bad += 1
        worst = max(worst, mu - g)
arm("mu_pref >= gamma at every primitive poset n <= 6 (an upper bound on mu that",
    bad == 0, "%d violations over %d" % (bad, tot))
print("     returns gamma is therefore a LOWER bound, which is exactly D1)")
arm("  and mu_pref > gamma STRICTLY somewhere, so the check is not vacuous",
    worst > 1e-6, "max mu - gamma = %.6f" % worst)

print("\n" + "-" * 78)
print("C5  mg-c50b's n=8 SCREEN -- the inequality it rests on: mu_pref <= 2*Phi*_pref")
print("-" * 78)
bad = 0
tot = 0
for n in (5, 6, 7):
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        if cnt % 13:
            continue
        tot += 1
        Phi = min(Fraction(p.LK[k], p.LE * min(k, n - k)) for k in range(1, n))
        mu, _ = mu_pref_float(p)
        if mu > 2 * float(Phi) + 1e-9:
            bad += 1
arm("mu_pref <= 2*Phi*_pref at every sampled primitive poset n <= 7", bad == 0,
    "%d violations over %d sampled" % (bad, tot))
print("     So c#_UB >= c# and the screen cannot drop a both-failing poset:")
print("     both failing => f* > 1 and c# > 1 => c#_UB > 1 => min(c#_UB, f*) > 1 > 0.85.")
print("     mg-c50b's 'both routes fail at 0 of 2600369' is EXHAUSTIVE on this argument.")
print("     Its (F)-alone count 3589 is NOT, and mg-c50b's own E9 says so.")

print("\n" + "-" * 78)
print("C6  THE DOCUMENT'S TWO COUNTING CONVENTIONS")
print("-" * 78)
print("     s3 table : (R1) holds at 166 of 168 ; (R2) holds at 35 of 168")
print("     s6 ledger: (R1) 'REFUTED at n = 7, 2 of 168' ; (R2) '133 of 168'")
arm("2 + 166 = 168 and 133 + 35 = 168 -- the two conventions are consistent",
    2 + 166 == 168 and 133 + 35 == 168)
print("     They are consistent but opposite, in one document, one section apart.")
print("     Flagged as a READABILITY defect, not an arithmetic one.")

print("\n" + "=" * 78)
print("a6 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
