"""selftest29fe — arms that would catch THIS instrument being wrong.

Every arm is FORCED (raises on failure).  Negative controls are marked NC: they assert
that a deliberately broken object gives the WRONG answer, so an arm cannot rot into a
tautology.
"""
import sys
from fractions import Fraction as F
from itertools import permutations, combinations
from lib29fe import (all_natural_posets, linear_extensions, is_decomposable, Poset,
                     is_psd, det_frac, gap_at_least, bracket_gap, cone_QN,
                     cone_QN_closedform, psi_basis, quad, monotone)

ok = fail = 0


def arm(name, cond, detail=""):
    global ok, fail
    if cond:
        ok += 1
        print(f"  PASS  {name}  {detail}")
    else:
        fail += 1
        print(f"  FAIL  {name}  {detail}")


print("=" * 78)
print("A1  population counts — naturally labelled posets on [n]")
print("=" * 78)
pops = {}
for n in range(2, 7):
    ps = all_natural_posets(n)
    prim = [r for r in ps if not is_decomposable(n, r)]
    pops[n] = (ps, prim)
    print(f"  n={n}  total={len(ps):5d}  primitive={len(prim):5d}  "
          f"decomposable={len(ps)-len(prim):4d}")
tot = sum(len(pops[n][0]) for n in range(2, 7))
prm = sum(len(pops[n][1]) for n in range(2, 7))
arm("A1a total n<=6 == 5230", tot == 5230, f"got {tot}")
arm("A1b primitive n<=6 == 4377", prm == 4377, f"got {prm}")
arm("A1c per-n primitive == 1,4,27,275,4070",
    [len(pops[n][1]) for n in range(2, 7)] == [1, 4, 27, 275, 4070],
    str([len(pops[n][1]) for n in range(2, 7)]))

print()
print("=" * 78)
print("A2  linear extensions — recursive enumeration vs brute-force over n!")
print("=" * 78)
bad = 0
for n in (4, 5):
    for rel in pops[n][0]:
        rec = set(linear_extensions(n, rel))
        brute = set(p for p in permutations(range(n))
                    if all(p.index(i) < p.index(j) for (i, j) in rel))
        if rec != brute:
            bad += 1
arm("A2 recursive LE == n! filter, all posets n=4,5", bad == 0, f"{bad} mismatches")

print()
print("=" * 78)
print("A3  PSD test — hand cases (the arm mg-28ff's E3 fired on)")
print("=" * 78)
I3 = [[F(1) if i == j else F(0) for j in range(3)] for i in range(3)]
arm("A3a identity is PSD", is_psd(I3))
arm("A3b -identity is NOT PSD", not is_psd([[-x for x in r] for r in I3]))
arm("A3c zero is PSD", is_psd([[F(0)] * 3 for _ in range(3)]))
arm("A3d diag(1,-1) is NOT PSD", not is_psd([[F(1), F(0)], [F(0), F(-1)]]))
arm("A3e [[1,2],[2,1]] is NOT PSD (eigs 3,-1)",
    not is_psd([[F(1), F(2)], [F(2), F(1)]]))
arm("A3f [[2,1],[1,2]] is PSD (eigs 3,1)", is_psd([[F(2), F(1)], [F(1), F(2)]]))
arm("A3g rank-1 vv^T is PSD", is_psd([[F(i * j) for j in (1, 2, 3)] for i in (1, 2, 3)]))
# NC1: a matrix PSD-except-one-negative-principal-minor that leading minors miss
NC = [[F(1), F(0), F(0)], [F(0), F(0), F(0)], [F(0), F(0), F(-1)]]
arm("A3h NC leading-minors-blind case correctly rejected", not is_psd(NC),
    "all leading principal minors are >=0 here; full principal minors catch it")
arm("A3i det_frac agrees with 2x2 formula",
    det_frac([[F(3), F(1)], [F(1), F(4)]]) == F(11))

print()
print("=" * 78)
print("A4  Lemma 2.1 at source:  <1_A,(I-S)1_A> == E|A \\ sigma(A)|  (exact)")
print("=" * 78)
bad = 0
tested = 0
for n in (4, 5):
    for rel in pops[n][0]:
        P = Poset(n, rel)
        L = P.L()
        les = linear_extensions(n, rel)
        for size in range(1, n):
            for A in combinations(range(n), size):
                Aset = set(A)
                ind = [F(1) if i in Aset else F(0) for i in range(n)]
                lhs = quad(L, ind)
                s = 0
                for perm in les:
                    pos = {el: t for t, el in enumerate(perm)}
                    s += sum(1 for i in A if pos[i] not in Aset)
                rhs = F(s, len(les))
                tested += 1
                if lhs != rhs:
                    bad += 1
arm("A4 Lemma 2.1 holds exactly", bad == 0, f"{bad} of {tested} (poset,cut) pairs bad")

print()
print("=" * 78)
print("A5  leak(A_k) == E #{i<k : pos(i)>=k}  and  Phi normalisation")
print("=" * 78)
bad = 0
for n in (4, 5, 6):
    for rel in pops[n][0][:400]:
        P = Poset(n, rel)
        L = P.L()
        for k in range(1, n):
            ind = [F(1) if i < k else F(0) for i in range(n)]
            if quad(L, ind) != P.leak[k]:
                bad += 1
arm("A5 leak from LE-count == quadratic form", bad == 0, f"{bad} bad")

print()
print("=" * 78)
print("A6  the psi pencil — closed forms vs definition (mg-28ff's own A4 claim)")
print("=" * 78)
bad = 0
for n in range(2, 7):
    for rel in pops[n][0][:600]:
        P = Poset(n, rel)
        Q1, N1 = cone_QN(P)
        Q2, N2 = cone_QN_closedform(P)
        if Q1 != Q2 or N1 != N2:
            bad += 1
arm("A6a Q,N closed forms == definition", bad == 0, f"{bad} bad")
bad = 0
for n in range(2, 7):
    for rel in pops[n][0][:600]:
        P = Poset(n, rel)
        Q, _ = cone_QN(P)
        for k in range(1, n):
            if Q[k - 1][k - 1] != P.leak[k]:
                bad += 1
arm("A6b Q_kk == leak(A_k)  (the hard control)", bad == 0, f"{bad} bad")
# NC2 (REBUILT — the first version was a control that could never fire; see README §D1).
# Adding a CONSTANT to psi cannot change Q at all, because the energy form is
# shift-invariant.  The mutation must perturb a SINGLE coordinate to be discriminating.
P = Poset(4, [r for r in pops[4][0] if not is_decomposable(4, r)][3])
psi = psi_basis(4)
L = P.L()
shifted = [x + F(1, 7) for x in psi[0]]
arm("A6c0 NC-DEAD a constant shift of psi leaves Q_kk UNCHANGED "
    "(this is why the first form of this control could not fire)",
    quad(L, shifted) == P.leak[1], f"shifted {quad(L, shifted)} == leak {P.leak[1]}")
perturbed = psi[0][:]
perturbed[0] = perturbed[0] + F(1, 7)
arm("A6c NC a single-coordinate perturbation of psi BREAKS Q_kk == leak",
    quad(L, perturbed) != P.leak[1],
    f"perturbed {quad(L, perturbed)} vs leak {P.leak[1]}")

print()
print("=" * 78)
print("A7  monotone cone == nonneg span of psi")
print("=" * 78)
n = 5
psi = psi_basis(n)
bad = 0
for trial in range(200):
    c = [F((trial * 7 + 3 * k) % 11) for k in range(n - 1)]
    g = [sum(c[k] * psi[k][i] for k in range(n - 1)) for i in range(n)]
    if not monotone(g) or sum(g, F(0)) != 0:
        bad += 1
arm("A7a nonneg combos are monotone and perp 1", bad == 0, f"{bad} bad")
neg = [sum((F(-1) if k == 0 else F(1)) * psi[k][i] for k in range(n - 1))
       for i in range(n)]
arm("A7b NC a negative coefficient breaks monotonicity", not monotone(neg), str(neg))

print()
print("=" * 78)
print("A3j  fast PSD path vs brute-force principal minors — on the sweep's own matrices")
print("=" * 78)
from lib29fe import is_psd_fast
bad = tested = npsd = 0
for n in (4, 5):
    for rel in pops[n][0][:120]:
        P = Poset(n, rel)
        L = P.L()
        for num in range(0, 17):
            t = F(num, 16)
            M = [[L[i][j] - t * ((F(1) if i == j else F(0)) - F(1, n))
                  for j in range(n)] for i in range(n)]
            a, b = is_psd_fast(M), is_psd(M)
            tested += 1
            npsd += 1 if a else 0
            if a != b:
                bad += 1
arm("A3j fast == brute force on every swept matrix", bad == 0,
    f"{bad} of {tested} disagree; {npsd} were PSD, {tested-npsd} were not "
    f"(so the arm is not vacuous in either direction)")

print()
print("=" * 78)
print("A8  gap bracket — exact PSD bisection vs float eigenvalue")
print("=" * 78)
import numpy as np
bad = 0
tested = 0
for n in (4, 5):
    for rel in pops[n][1][:60]:
        P = Poset(n, rel)
        lo, hi = bracket_gap(P, iters=30)
        Lf = np.array([[float(x) for x in row] for row in P.L()])
        w = sorted(np.linalg.eigvalsh(Lf))
        g = w[1]                       # smallest eigenvalue on 1^perp
        tested += 1
        if not (float(lo) - 1e-6 <= g <= float(hi) + 1e-6):
            bad += 1
arm("A8 float eigenvalue lies inside the exact bracket", bad == 0,
    f"{bad} of {tested} outside")

print()
print("=" * 78)
print("A9  decomposable <=> zero gap <=> some prefix leaks 0")
print("=" * 78)
bad = 0
for n in range(2, 7):
    for rel in pops[n][0][:800]:
        P = Poset(n, rel)
        zero_pref = any(P.leak[k] == 0 for k in range(1, n))
        if zero_pref != P.decomposable:
            bad += 1
arm("A9 ordinal-sum cut point <=> a prefix with zero leak", bad == 0, f"{bad} bad")

print()
print("=" * 78)
print("A10 NC — the verdict pipeline is not vacuous")
print("=" * 78)
# The target Phi*_pref^2 <= 2K(1-lambda) must FAIL for small K and HOLD for K=1.
fails_small = holds_one = 0
for rel in pops[5][1]:
    P = Poset(5, rel)
    lo, hi = bracket_gap(P, iters=24)
    ph = P.Phi_star_pref()
    if ph ** 2 > 2 * F(1, 20) * hi:
        fails_small += 1
    if ph ** 2 <= 2 * F(1) * lo:
        holds_one += 1
arm("A10a K=1/20 fails somewhere", fails_small > 0, f"{fails_small} of 275 fail")
arm("A10b K=1 holds everywhere at n=5", holds_one == 275, f"{holds_one} of 275")

print()
print("=" * 78)
print(f"RESULT  {ok} passed, {fail} failed")
print("=" * 78)
sys.exit(1 if fail else 0)
