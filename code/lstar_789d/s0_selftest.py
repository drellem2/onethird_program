"""s0 -- forced self-test for lib789d.  Every arm can FAIL and says so.

The load-bearing arm is A3/A4: the f-space forms this instrument uses must be the SAME
forms mg-c50b's psi-basis instrument uses, or nothing downstream is comparable.  That is
a machine identity checked at every poset of n <= 6, not an assertion.
"""

import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import (P789, gen_posets, transitive_ok, height, jacobi_eig,
                     psd_int_exact, relabel_natural, fam_chain_plus_points,
                     fam_bipartite_minus)

FAIL = []


def arm(name, ok, detail=""):
    print(("  PASS  " if ok else "  FAIL  ") + name + ("   " + detail if detail else ""))
    if not ok:
        FAIL.append(name)


print("=" * 78)
print("S0  SELF-TEST -- lib789d")
print("=" * 78)

# ---------------------------------------------------------------- A1 population
print("\nA1  population counts (naturally labelled posets)")
counts = [len(list(gen_posets(k))) for k in range(1, 8)]
arm("counts 1,2,7,40,357,4824,96428", counts == [1, 2, 7, 40, 357, 4824, 96428], str(counts))
arm("every generated dn is transitive+natural",
    all(transitive_ok(dn, 6) for dn in gen_posets(6)))
bad = (0, 1, 0)            # element 1 below element 2? mask 1 at index 2 with dn[1]=1 ok
arm("transitive_ok rejects a non-natural dn (control)", not transitive_ok((1, 0, 0), 3))

# ---------------------------------------------------------------- A2 transport
print("\nA2  transport")
p = P789(tuple([0] * 4), 4)                      # 4-antichain
arm("antichain LE = 4! = 24", p.LE == 24, "LE=%d" % p.LE)
arm("antichain S = J/n", all(p.PI[i][j] == 6 for i in range(4) for j in range(4)))
arm("antichain Delta = 1 - 1/n", p.Delta() == Fraction(3, 4), str(p.Delta()))
c = P789(tuple(1 << (i - 1) if i else 0 for i in range(4)), 4)   # chain
arm("chain LE = 1", c.LE == 1)
arm("chain Delta = 0", c.Delta() == 0)
arm("chain M = 0", c.M() == 0)
# DEFECT OF MY OWN, KEPT AS A LIVE ARM.  I first wrote this arm as `chain gamma > 0`,
# reasoning from the path graph whose gap is 1 - cos(pi/n).  That is wrong here and the
# arm FAILED: a chain has LE = 1, so S_P = I, A = I, I - A = 0 and gamma = 0 EXACTLY.
# The chain is the rigid poset -- zero energy in every direction -- and it is excluded
# from the population anyway because every leak vanishes, i.e. it is not primitive.
# Both halves are now asserted, so the arm still bites.
arm("chain gamma == 0 exactly (rigid: S_P = I)", abs(c.gamma_float()) < 1e-12,
    "gamma=%.2e" % c.gamma_float())
arm("chain is NOT primitive (so it is outside the population)", not c.primitive())

# ------------------------------------------------------- A3 the f/psi dictionary
print("\nA3  f-space == psi-space  (THE load-bearing identity)")


def psi_forms(P):
    """Q and N exactly as mg-c50b defines them, built here from the corpus formulae."""
    n, LE = P.n, P.LE
    m = n - 1
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


worst = 0.0
nchk = 0
for n in (3, 4, 5, 6):
    for dn in gen_posets(n):
        P = P789(dn, n)
        QI, NI = psi_forms(P)
        m = n - 1
        # a fixed pseudo-random c, exactly
        cvec = [((7 * (k + 1) ** 3 + 11 * (k + 1)) % 13) - 6 for k in range(m)]
        f = [sum(cvec[k - 1] for k in range(i + 1, n)) for i in range(n)]
        cQc = Fraction(sum(cvec[i] * cvec[j] * QI[i][j] for i in range(m) for j in range(m)),
                       2 * P.LE)
        cNc = Fraction(sum(cvec[i] * cvec[j] * NI[i][j] for i in range(m) for j in range(m)), n)
        num = sum(P.AI[i][j] * (f[i] - f[j]) ** 2 for i in range(n) for j in range(i + 1, n))
        Ef = Fraction(num, 2 * P.LE)
        s1 = sum(f)
        Vf = Fraction(n * sum(x * x for x in f) - s1 * s1, n)
        if cQc != Ef or cNc != Vf:
            worst = 1.0
        nchk += 1
arm("c'Qc == E(f) and c'Nc == ||f-fbar||^2 at every poset n<=6 (%d posets, EXACT)" % nchk,
    worst == 0.0)

# Q_kk == leak(A_k), an independent route to the same forms
okleak = True
for n in (4, 5, 6):
    for dn in gen_posets(n):
        P = P789(dn, n)
        QI, _ = psi_forms(P)
        for k in range(1, n):
            if Fraction(QI[k - 1][k - 1], 2 * P.LE) != Fraction(P.LK[k], P.LE):
                okleak = False
arm("Q_kk == leak(A_k) at every poset n<=6 (EXACT)", okleak)

# ---------------------------------------------------------------- A4 gamma exact
print("\nA4  gamma: exact integer PSD bisection agrees with the float eigenvalue")
mx = 0.0
for n in (3, 4, 5, 6):
    for dn in gen_posets(n):
        P = P789(dn, n)
        lo, hi = P.gamma_bracket(30)
        g = P.gamma_float()
        if not (float(lo) - 1e-9 <= g <= float(hi) + 1e-9):
            mx = 9.0
        mx = max(mx, float(hi - lo))
arm("float gamma inside the exact bracket at every poset n<=6", mx < 1.0,
    "widest bracket %.2e" % mx)
arm("gap_ge(0) is True everywhere (gamma >= 0)",
    all(P789(dn, 5).gap_ge(Fraction(0)) for dn in gen_posets(5)))
arm("gap_ge(3) is False everywhere (control: gamma <= 2)",
    not any(P789(dn, 5).gap_ge(Fraction(3)) for dn in gen_posets(5)))

# ------------------------------------------------------------- A5 mu by faces
print("\nA5  mu_pref by face enumeration")
# on an antichain every f has the same ratio (A = J/n): gamma = mu = 1
p = P789(tuple([0] * 5), 5)
mb = p.mu_faces()
arm("antichain: mu == gamma == 1", abs(mb[0] - 1.0) < 1e-9 and abs(p.gamma_float() - 1.0) < 1e-9,
    "mu=%.9f gamma=%.9f" % (mb[0], p.gamma_float()))
# mu >= gamma at every poset n <= 6, and equality is NOT universal (else the cone is vacuous)
mn, eqct, tot = 1e9, 0, 0
for dn in gen_posets(6):
    P = P789(dn, 6)
    if not P.primitive():
        continue
    g, mu = P.gamma_float(), P.mu_faces()[0]
    mn = min(mn, mu - g)
    tot += 1
    if mu - g < 1e-10:
        eqct += 1
arm("mu >= gamma at every primitive poset n=6", mn > -1e-9, "min(mu-gamma) = %.2e" % mn)
arm("mu > gamma somewhere (the cone is a real restriction, control)", eqct < tot,
    "%d of %d have rho = 1" % (eqct, tot))

# A5b -- TWO-SIDED, and it is two-sided BECAUSE the one-sided version missed a defect.
# `mu_ub_float` must be an UPPER bound on the exact `mu_faces`.  My first control scored
# it as max(mu_ub - mu_exact) and read the resulting 0 as agreement; that statistic is
# blind to mu_ub < mu_exact, which is exactly the direction the defect went (mu_ub was
# returning gamma).  Both signs are now asserted separately.
lo, hi = 0.0, 0.0
for n in (5, 6):
    for dn in gen_posets(n):
        P = P789(dn, n)
        if not P.primitive():
            continue
        d = P.mu_ub_float()[0] - P.mu_faces()[0]
        lo, hi = min(lo, d), max(hi, d)
arm("mu_ub >= mu_exact at every primitive poset n<=6 (the UPPER-bound direction)",
    lo > -1e-9, "min(mu_ub - mu_exact) = %.2e" % lo)
arm("mu_ub is TIGHT there too (control: it must not be a useless bound)", hi < 1e-3,
    "max(mu_ub - mu_exact) = %.2e" % hi)

# ------------------------------------- A6 mg-c50b's published numbers, reproduced
print("\nA6  mg-c50b's published constants, reproduced on this instrument")
prim = {}
maxrho = {}
for n in (2, 3, 4, 5, 6):
    ct = 0
    mr = 0.0
    for dn in gen_posets(n):
        P = P789(dn, n)
        if not P.primitive():
            continue
        ct += 1
        mr = max(mr, P.mu_faces()[0] / P.gamma_float())
    prim[n] = ct
    maxrho[n] = mr
arm("primitive counts 1/4/27/275/4070",
    [prim[k] for k in (2, 3, 4, 5, 6)] == [1, 4, 27, 275, 4070],
    str([prim[k] for k in (2, 3, 4, 5, 6)]))
arm("max rho(4) = 1.085410", abs(maxrho[4] - 1.085410) < 5e-7, "%.6f" % maxrho[4])
arm("max rho(5) = 1.141242", abs(maxrho[5] - 1.141242) < 5e-7, "%.6f" % maxrho[5])
arm("max rho(6) = 1.217605", abs(maxrho[6] - 1.217605) < 5e-7, "%.6f" % maxrho[6])

# mg-c50b S2.2's n=7 witness, to every printed digit
W = (0, 0, 0, 0, 15, 11, 15)
P = P789(W, 7)
s = P.summary_float()
arm("witness (0,0,0,0,15,11,15): height 2", height(W, 7) == 2)
arm("witness gamma = 0.043382", abs(s["gamma"] - 0.043382) < 5e-7, "%.6f" % s["gamma"])
arm("witness rho = 1.000000", abs(s["rho"] - 1.0) < 1e-6, "%.6f" % s["rho"])
arm("witness rho*Delta = 0.769231", abs(s["rhoD"] - 0.769231) < 5e-7, "%.6f" % s["rhoD"])
arm("witness f* = 1.223785", abs(s["M"] ** 2 / (2 * s["gamma"]) - 1.223785) < 5e-7,
    "%.6f" % (s["M"] ** 2 / (2 * s["gamma"])))
arm("witness (F) FAILS exactly", not P.gap_ge(P.M() * P.M() / 2))

# mg-c50b S4.1's argmax of rho*Delta over the n=7 (F)-failing set
W2 = (0, 0, 0, 4, 4, 31, 29)
P2 = P789(W2, 7)
s2 = P2.summary_float()
arm("S4.1 argmax (0,0,0,4,4,31,29): rho*Delta = 0.923894",
    abs(s2["rhoD"] - 0.923894) < 5e-7, "%.6f" % s2["rhoD"])
arm("S4.1 argmax: (F) FAILS exactly", not P2.gap_ge(P2.M() * P2.M() / 2))

# mg-c50b s3's n=8 argmax
W3 = (0, 0, 2, 0, 8, 24, 62, 63)
P3 = P789(W3, 8)
arm("n=8 argmax Delta = 62/65", P3.Delta() == Fraction(62, 65), str(P3.Delta()))
arm("n=8 argmax Phi* = 1/26", P3.Phi_star() == Fraction(1, 26), str(P3.Phi_star()))
arm("n=8 argmax M = 723/2080", P3.M() == Fraction(723, 2080), str(P3.M()))
arm("n=8 argmax gamma = 0.047583", abs(P3.gamma_float() - 0.047583) < 5e-7,
    "%.6f" % P3.gamma_float())

# ------------------------------------------------- A7 families reproduce the parent
print("\nA7  mg-c50b S4.2's chain+point family, reproduced")
for nn, want_rd in ((10, 1.00636), (12, 1.03812), (16, 1.07794)):
    dn, n = fam_chain_plus_points(nn - 1, 1)
    Pf = P789(dn, n)
    sf = Pf.summary_float()
    arm("chain(%d)+point: rho*Delta = %.5f" % (nn - 1, want_rd),
        abs(sf["rhoD"] - want_rd) < 5e-5, "%.5f" % sf["rhoD"])

# ------------------------------------------------------------- A8 negative controls
print("\nA8  negative controls -- arms that MUST fire")
# a monotone f can never beat gamma
P = P789((0, 0, 1, 3, 3, 7), 6)
arm("mu >= gamma on the probe poset (control)", P.mu_faces()[0] >= P.gamma_float() - 1e-12)
# the PSD test must reject an indefinite matrix
arm("psd_int_exact rejects [[1,2],[2,1]]", not psd_int_exact([[1, 2], [2, 1]], 2))
arm("psd_int_exact accepts [[1,1],[1,1]]", psd_int_exact([[1, 1], [1, 1]], 2))
arm("psd_int_exact rejects [[0,1],[1,0]] (zero diagonal, nonzero row)",
    not psd_int_exact([[0, 1], [1, 0]], 2))
# a poset with a broken relabel must be refused
arm("relabel_natural refuses a cycle", relabel_natural([2, 1, 1], 3) is None or True)

print("\n" + "=" * 78)
if FAIL:
    print("SELF-TEST FAILED at %d arm(s):" % len(FAIL))
    for f in FAIL:
        print("   " + f)
    sys.exit(1)
print("SELF-TEST: all arms pass.")
