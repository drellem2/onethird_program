"""a0 -- self-test of lib5cba BEFORE any verdict is taken from it.

Every arm is FORCED: it asserts against a value this file's author could not choose
(a published corpus figure, a closed-form, or an identity between two independent
paths inside this file).  Arms that could not fail are not arms.
"""
import sys
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import (P5, gen_posets, is_natural_transitive, height, transport,
                     psd_int, copositive_int, gamma_float, mu_pref_float)

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-58s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


print("=" * 78)
print("a0  SELF-TEST -- lib5cba, mg-5cba's independent audit instrument")
print("=" * 78)

print("\nS0. Provenance")
import subprocess
h = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True).stdout.strip()
print("      HEAD: %s" % h)
print("      lib789d.py was NOT opened before this file and lib5cba.py were written;")
print("      definitions were re-derived from libc50b.py sections 1-3 and the docs.")

print("\nS1. Population counts -- naturally labelled posets  1,2,7,40,357,4824,96428")
exp = [1, 1, 2, 7, 40, 357, 4824, 96428]
for n in range(0, 8):
    c = sum(1 for _ in gen_posets(n))
    arm("n=%d count = %d" % (n, exp[n]), c == exp[n], str(c))
    if n <= 6:
        arm("  all naturally labelled + transitive",
            all(is_natural_transitive(dn, n) for dn in gen_posets(n)))

print("\nS2. Primitive counts -- corpus publishes 4/27/275/4070/86278 at n=3..7")
expp = {3: 4, 4: 27, 5: 275, 6: 4070, 7: 86278}
prim = {}
for n in range(3, 8):
    c = sum(1 for dn in gen_posets(n) if P5(dn, n).primitive())
    prim[n] = c
    arm("n=%d primitive = %d" % (n, expp[n]), c == expp[n], str(c))

print("\nS3. Transport sanity -- S_P doubly stochastic, chain and antichain closed forms")
for n in (4, 5, 6):
    bad = 0
    for dn in gen_posets(n):
        LE, PI = transport(dn, n)
        for i in range(n):
            if sum(PI[i]) != LE:
                bad += 1
            if sum(PI[j][i] for j in range(n)) != LE:
                bad += 1
    arm("n=%d: every row and column of PI sums to LE" % n, bad == 0, "%d bad" % bad)
# chain: LE = 1, S_P = I, gamma = 0, NOT primitive  (mg-789d's own defect D2)
for n in (5, 9):
    dn = tuple((1 << i) - 1 for i in range(n))
    p = P5(dn, n)
    arm("chain n=%d: LE = 1" % n, p.LE == 1, str(p.LE))
    arm("chain n=%d: Delta = 0 (S_P = I)" % n, p.Delta() == 0, str(p.Delta()))
    arm("chain n=%d: gamma = 0 exactly" % n, p.gamma_ge(0) and not p.gamma_ge(Fraction(1, 10**9)))
    arm("chain n=%d: NOT primitive" % n, not p.primitive())
# antichain: LE = n!, S_P = J/n, A = J/n, gamma = 1, Delta = 1 - 1/n
import math
for n in (4, 6):
    dn = tuple(0 for _ in range(n))
    p = P5(dn, n)
    arm("antichain n=%d: LE = n!" % n, p.LE == math.factorial(n), str(p.LE))
    arm("antichain n=%d: Delta = 1 - 1/n" % n, p.Delta() == Fraction(n - 1, n), str(p.Delta()))
    arm("antichain n=%d: gamma = 1 exactly" % n,
        p.gamma_ge(1) and not p.gamma_ge(Fraction(1000001, 1000000)))

print("\nS4. psd_int -- forced positive AND negative arms")
arm("I_3 PSD", psd_int([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3))
arm("diag(1,0,1) PSD (semidefinite, not definite)", psd_int([[1, 0, 0], [0, 0, 0], [0, 0, 1]], 3))
arm("[[0,1],[1,0]] NOT PSD (zero diag, nonzero off-diag)", not psd_int([[0, 1], [1, 0]], 2))
arm("[[1,2],[2,1]] NOT PSD (det < 0)", not psd_int([[1, 2], [2, 1]], 2))
arm("[[1,1],[1,1]] PSD (rank 1)", psd_int([[1, 1], [1, 1]], 2))
arm("diag(1,1,-1) NOT PSD", not psd_int([[1, 0, 0], [0, 1, 0], [0, 0, -1]], 3))
# a matrix that is PSD but whose LEADING minors alone would not decide it
arm("[[0,0],[0,-1]] NOT PSD (leading minors are 0,0)", not psd_int([[0, 0], [0, -1]], 2))

print("\nS5. copositive_int -- forced arms, including the classic separators")
arm("I_3 copositive", copositive_int([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 3)[0])
arm("all-ones copositive", copositive_int([[1, 1], [1, 1]], 2)[0])
arm("[[1,-3],[-3,1]] NOT copositive", not copositive_int([[1, -3], [-3, 1]], 2)[0])
arm("[[1,-1],[-1,1]] copositive (PSD)", copositive_int([[1, -1], [-1, 1]], 2)[0])
# Horn matrix: copositive but NOT (PSD + nonnegative) -- the standard separator
horn = [[1, -1, 1, 1, -1], [-1, 1, -1, 1, 1], [1, -1, 1, -1, 1],
        [1, 1, -1, 1, -1], [-1, 1, 1, -1, 1]]
arm("Horn matrix IS copositive", copositive_int(horn, 5)[0])
arm("Horn matrix is NOT PSD", not psd_int(horn, 5))
hm = [[-1 if i == j == 0 else horn[i][j] for j in range(5)] for i in range(5)]
arm("Horn with H[0][0] -> -1 is NOT copositive", not copositive_int(hm, 5)[0])
# a SINGULAR face, to prove the singular branch is exercised and decided
sing = [[1, 1, -1], [1, 1, -1], [-1, -1, 1]]     # = vv' with v=(1,1,-1): PSD, copositive
arm("rank-1 singular vv' IS copositive (and PSD)",
    copositive_int(sing, 3)[0] and psd_int(sing, 3))
sing2 = [[0, 0, -1], [0, 0, -1], [-1, -1, 0]]    # singular, c=(1,0,1): -2 < 0
ok2, w2 = copositive_int(sing2, 3)
arm("singular [[0,0,-1],[0,0,-1],[-1,-1,0]] NOT copositive", not ok2)
# witness check when returned
if w2 is not None:
    v = sum(w2[i] * sing2[i][j] * w2[j] for i in range(3) for j in range(3))
    arm("  returned witness really has c'Rc < 0", v < 0, str(v))

print("\nS6. copositive => the copositivity/PSD ordering, on real posets")
bad = 0
for n in (4, 5):
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        g_lo, g_hi = p.gamma_bracket(24)
        # mu_pref >= gamma always: PSD at t implies copositive at t
        if p.gamma_ge(g_lo) and not p.mu_ge(g_lo):
            bad += 1
arm("PSD at t => copositive at t, on every primitive n<=5 poset", bad == 0, "%d bad" % bad)

print("\nS7. TWO INDEPENDENT mu_pref PATHS AGREE (the D1 cross-check)")
worst = 0.0
worstp = None
nbelow = 0
for n in (4, 5, 6):
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        if cnt % 7:          # sample: the exact path is expensive
            continue
        mf, _ = mu_pref_float(p)
        lo, hi = p.mu_bracket(22)
        d = abs(mf - float(lo))
        if not (float(lo) - 1e-7 <= mf <= float(hi) + 1e-7):
            nbelow += 1
        if d > worst:
            worst, worstp = d, (n, dn)
arm("f-space face path lies inside the psi-basis copositivity bracket, BOTH SIDES",
    nbelow == 0, "%d outside; worst |gap| = %.2e at %s" % (nbelow, worst, worstp))

print("\nS8. gamma: two independent paths (Jacobi on A vs integer PSD bisection)")
worst = 0.0
for n in (4, 5, 6):
    cnt = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        if cnt % 11:
            continue
        gf = gamma_float(p)
        lo, hi = p.gamma_bracket(26)
        if not (float(lo) - 1e-7 <= gf <= float(hi) + 1e-7):
            worst = 9e9
arm("1 - lambda_2(A) lies inside the integer-PSD bracket", worst < 1e9)

print("\nS9. NEGATIVE CONTROL -- the D1 defect, reproduced and then caught")
# mu without the monotonicity check == gamma at the all-cuts face, i.e. rho == 1.
n = 6
hits = 0
tot = 0
for dn in gen_posets(n):
    p = P5(dn, n)
    if not p.primitive():
        continue
    tot += 1
    if tot % 37:
        continue
    gf = gamma_float(p)
    mf, _ = mu_pref_float(p)
    if mf > gf + 1e-9:
        hits += 1
arm("mu_pref > gamma STRICTLY at some poset (a check-free method cannot do this)",
    hits > 0, "%d of the sampled" % hits)

print("\n" + "=" * 78)
print("a0 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
