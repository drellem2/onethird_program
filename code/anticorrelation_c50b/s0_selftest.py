"""s0 -- FORCED ARMS.  Every arm asserts; the file exits non-zero on any failure.

Positive arms A*, negative controls C*.  A control that CANNOT fire is worthless, so
every C* is checked to actually fire.
"""
import sys
from fractions import Fraction
from libc50b import *

fails = []


def arm(name, ok, detail=""):
    print("  %-58s %s  %s" % (name, "PASS" if ok else "**FAIL**", detail))
    if not ok:
        fails.append(name)


def mk(n, rels):
    dn = [0] * n
    for a, b in rels:
        dn[b] |= 1 << a
    for _ in range(n):
        for i in range(n):
            m, add = dn[i], 0
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                add |= dn[j]
            dn[i] |= add
    return tuple(dn)


print("=" * 78)
print("s0.  SELFTEST -- mg-c50b")
print("=" * 78)

# ---------------------------------------------------------------- A1 population
counts = [sum(1 for _ in gen_posets(n)) for n in range(1, 8)]
arm("A1  population 1,2,7,40,357,4824,96428", counts == [1, 2, 7, 40, 357, 4824, 96428],
    str(counts))

# ---------------------------------------------------------------- A2 transitivity
bad = sum(1 for n in (5, 6) for dn in gen_posets(n) if not transitive_ok(dn, n))
arm("A2  every generated poset natural + transitive", bad == 0, "%d bad" % bad)

# ------------------------------------------------- A3 the hard control Q_kk = 2 leak
bad = 0
tested = 0
for n in (3, 4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        for k in range(1, n):
            tested += 1
            if P.QI[k - 1][k - 1] != 2 * P.LK[k]:
                bad += 1
arm("A3  Q_kk = leak(A_k) at every (poset,prefix)  [mg-28ff's control]", bad == 0,
    "%d pairs, %d bad" % (tested, bad))

# ------------------------------------------------------- A4 the footrule identity
bad = 0
tested = 0
for n in (3, 4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        # sum_k leak(A_k)  ==  (1/2) E sum_i |i - pos(i)|
        lhs = Fraction(P.sumLK, P.LE)
        foot = sum(P.PI[i][j] * abs(i - j) for i in range(n) for j in range(n))
        rhs = Fraction(foot, 2 * P.LE)
        tested += 1
        if lhs != rhs:
            bad += 1
arm("A4  footrule identity sum_k leak = (1/2)E[D_F]  [mg-28ff §3]", bad == 0,
    "%d posets, %d bad" % (tested, bad))

# ------------------------------------------- A5 Lemma 2.1 sandwich  Phi <= R(psi) <= 2Phi
bad = 0
tested = 0
for n in (4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        for k in range(1, n):
            R = Fraction(n * P.LK[k], P.LE * k * (n - k))
            phi = P.phi(k)
            tested += 1
            if not (phi <= R <= 2 * phi):
                bad += 1
arm("A5  Lemma 2.1  Phi_P(A_k) <= 1-rho(A_k) <= 2 Phi_P(A_k)", bad == 0,
    "%d pairs, %d bad" % (tested, bad))

# ------------------------------------------ A6 two independent PSD devices agree
import random
random.seed(20260810)
disagree = 0
trials = 0
for _ in range(400):
    m = random.randint(1, 4)
    B = [[random.randint(-4, 4) for _ in range(m)] for _ in range(m)]
    R = [[sum(B[k][i] * B[k][j] for k in range(m)) for j in range(m)] for i in range(m)]
    if random.random() < 0.5:                      # perturb off PSD half the time
        i = random.randrange(m)
        R[i][i] -= random.randint(1, 6)
    trials += 1
    if psd_int(R, m) != psd_minors(R, m):
        disagree += 1
arm("A6  psd_int == psd_minors (two independent devices)", disagree == 0,
    "%d matrices, %d disagreements" % (trials, disagree))

# ----------------------------------------- A7 gamma = 0 exactly on the decomposables
badp = badd = 0
for n in (4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        pos = P.gap_ge(Fraction(1, 10 ** 9))
        if P.primitive() and not pos:
            badp += 1
        if not P.primitive() and pos:
            badd += 1
arm("A7  gamma > 0 iff primitive  [mg-76b2: 1-lambda_std = 0 on the decomposables]",
    badp == 0 and badd == 0, "%d/%d bad" % (badp, badd))

# ------------------------------- A8 the floor theorem  gamma <= mu_pref, 0 exceptions
bad = 0
tested = 0
for n in (4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive():
            continue
        tested += 1
        mu, _ = mu_exhaustive(P)
        if mu < P.gamma_float() - 1e-11:
            bad += 1
arm("A8  THE FLOOR: gamma <= mu_pref at every primitive poset  [mg-51f4 §2]",
    bad == 0, "%d posets, %d exceptions" % (tested, bad))

# ------------------------- A9 mg-51f4's TWO n=7 WITNESSES, to every printed digit
r = [(0, 1), (0, 2), (0, 3), (0, 5), (0, 6), (1, 2), (1, 3), (1, 5), (1, 6),
     (2, 3), (2, 6), (4, 5), (4, 6), (5, 6)]
P = Poset(mk(7, r), 7)
ub = P.mu_upper()
okA = (P.LE == 19 and P.Delta() == Fraction(18, 19) and P.Phi_star() == Fraction(5, 19)
       and [str(P.phi(k)) for k in range(1, 7)] ==
       ["5/19", "5/19", "5/19", "8/19", "7/19", "7/19"]
       and abs(P.gamma_float() - 0.185485078) < 5e-9
       and abs(float(ub[0]) - 0.226537524) < 5e-8
       and abs(P.c_sharp_float(ub[0]) - 1.018707) < 5e-7)
arm("A9a (M#) n=7 witness reproduces  [PREDICTIONS.md E6's guard]", okA,
    "LE=%d Delta=%s Phi*=%s c#=%.6f" % (P.LE, P.Delta(), P.Phi_star(),
                                        P.c_sharp_float(ub[0])))
r2 = [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6)]
P2 = Poset(mk(7, r2), 7)
okB = (P2.LE == 156 and P2.Phi_star() == Fraction(1, 39) and P2.M() == Fraction(157, 468)
       and P2.M() * P2.M() / 2 == Fraction(24649, 438048)
       and abs(P2.f_star_float() - 1.297074) < 5e-7
       and abs(P2.c_true_float() - 0.007578) < 5e-7 and P2.F_fails())
arm("A9b (F)  n=7 witness reproduces", okB,
    "LE=%d Phi*=%s M=%s f*=%.6f" % (P2.LE, P2.Phi_star(), P2.M(), P2.f_star_float()))

# ------------------------- A10 the L2-free THEOREM itself, against brute force
bad = 0
tested = 0
for n in (4, 5):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive():
            continue
        D = P.Delta()
        for trial in range(6):
            c = [random.randint(0, 5) for _ in range(n - 1)]
            if not any(c):
                continue
            num = sum(c[i] * c[j] * P.QI[i][j] for i in range(n - 1) for j in range(n - 1))
            den = sum(c[i] * c[j] * P.NI[i][j] for i in range(n - 1) for j in range(n - 1))
            if den <= 0:
                continue
            R = Fraction(n * num, 2 * P.LE * den)
            tested += 1
            if P.Phi_star() ** 2 > P.sweep(R):
                bad += 1
arm("A10 THEOREM  Phi*^2 <= sweep(R(g), Delta) at (poset, monotone g) pairs",
    bad == 0, "%d pairs, %d exceptions" % (tested, bad))

# ------------------------- A11 my pre-run inequalities (PREDICTIONS.md H4)
bad1 = bad2 = 0
tested = 0
for n in (4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive():
            continue
        tested += 1
        if P.M() > P.Delta():
            bad1 += 1
        mu, _ = mu_exhaustive(P)
        if mu > 2 * float(P.Phi_star()) + 1e-11:
            bad2 += 1
arm("A11a M <= Delta_P  [derived pre-run, H4]", bad1 == 0, "%d posets" % tested)
arm("A11b mu_pref <= 2 Phi*_pref  [derived pre-run, H4]", bad2 == 0, "%d posets" % tested)

# ================================ NEGATIVE CONTROLS ==========================
print("\n  -- negative controls (each must FIRE) --")

# C1 the mutated floor Delta + gamma/2 must be violated essentially everywhere
fired = 0
tot = 0
for dn in gen_posets(6):
    P = Poset(dn, 6)
    if not P.primitive():
        continue
    tot += 1
    if P.c_sharp_float(P.mu_upper()[0]) < float(P.Delta()) + P.gamma_float() / 2 - 1e-12:
        fired += 1
arm("C1  mutated floor  c# >= Delta + gamma/2  is VIOLATED", fired == tot,
    "%d of %d violate  [mg-51f4's own control]" % (fired, tot))

# C2 psd_int must reject an indefinite matrix
arm("C2  psd_int rejects [[1,2],[2,1]]", not psd_int([[1, 2], [2, 1]], 2))

# C3 dropping the second branch of the sweep must change a number somewhere
diff = 0
for n in (2, 3, 4, 5, 6):
    for dn in gen_posets(n):
        P = Poset(dn, n)
        if not P.primitive():
            continue
        mu, _ = mu_exhaustive(P)
        muF = Fraction(int(mu * 10 ** 9), 10 ** 9)
        one_case = muF * (2 * P.Delta() - muF)
        if one_case != P.sweep(muF):
            diff += 1
arm("C3  the one-case (M#) differs from the THEOREM's two-case form",
    diff > 0, "%d posets differ  [mg-28ff repair 7 -- the ANTICHAINS]" % diff)

# C4 a broken transitive closure must break A3's control
dnbad = (0, 1, 2)          # 2 covers 1 covers 0 but dn[2] omits 0 -> not transitive
arm("C4  the Q_kk control CATCHES a non-transitive dn", not transitive_ok(dnbad, 3))

# C5 an exhibited vector can never certify FAILS -- assert the direction
P3 = Poset(mk(7, r), 7)
mu_true, bv = mu_exhaustive(P3)
ub_exact = exact_ub_from(P3, bv[0], bv[1])
arm("C5  exhibited-vector bound is an UPPER bound on mu_pref  [E3's direction]",
    float(ub_exact) >= mu_true - 1e-12,
    "ub=%.9f >= mu=%.9f" % (float(ub_exact), mu_true))

print()
if fails:
    print("  *** %d ARM(S) FAILED: %s" % (len(fails), fails))
    sys.exit(1)
print("  ALL ARMS PASS")
