"""selftest28ff — the instrument checks itself before it is allowed to publish.

Every arm is FORCED: it asserts, and a failure aborts the run rather than printing a
warning.  Arms C* are NEGATIVE controls / mutation tests (PREDICTIONS.md E4): each one
deliberately breaks something and asserts that the check NOTICES.  A control that cannot
fail is not a control.
"""

from fractions import Fraction as F
from itertools import combinations
import sys

from lib28ff import (Poset, all_posets, named_posets, psi, pencil, from_coeffs,
                     is_monotone, rayleigh, psd_exact, charpoly_coeffs, gap_at_least,
                     gap_exact_bounds, pencil_eigs, cone_min, rationalise, sweep_bound_sq)

ok = 0


def arm(label, cond, detail=""):
    global ok
    assert cond, f"FAIL {label}: {detail}"
    ok += 1
    print(f"  ok  {label}" + (f"  [{detail}]" if detail else ""))


print("== selftest28ff ==")

POP6 = []
for n in range(2, 7):
    POP6 += all_posets(n)
print(f"population: {len(POP6)} posets over n = 2..6 "
      f"(every poset with the identity a linear extension)")

# ---- A1. T is doubly stochastic, S_P symmetric, I-S_P is the graph Laplacian
bad = []
for P in POP6:
    T, S, L = P.T(), P.S(), P.laplacian()
    n = P.n
    for i in range(n):
        if sum(T[i]) != 1 or sum(T[r][i] for r in range(n)) != 1:
            bad.append((P, "T not doubly stochastic"))
            break
    for i in range(n):
        d = sum(S[i][j] for j in range(n) if j != i)
        if L[i][i] != d:
            bad.append((P, f"L_ii != d_i at {i}"))
            break
arm("A1  T doubly stochastic and (I-S_P) is the combinatorial Laplacian of a_ij",
    not bad, f"{len(POP6)} posets, 0 exceptions")

# ---- A2. energy(1_A) == leak(A) -- matrix side vs definition side
pairs = 0
bad = []
for P in POP6:
    n = P.n
    for m in range(1, n):
        for A in combinations(range(n), m):
            f = [F(1) if i in A else F(0) for i in range(n)]
            pairs += 1
            if P.energy(f) != P.leak(A):
                bad.append((P, A))
arm("A2  <1_A,(I-S_P)1_A> == E|A \\ sigma(A)|  (matrix vs definition)",
    not bad, f"{pairs} (poset, cut) pairs, 0 exceptions")

# ---- A3. leak(A) == leak(A^c)  (Phi is a function of the cut)
bad = []
for P in POP6:
    n = P.n
    for m in range(1, n):
        for A in combinations(range(n), m):
            Ac = [i for i in range(n) if i not in A]
            if P.leak(A) != P.leak(Ac):
                bad.append((P, A))
arm("A3  leak(A) == leak(A^c)", not bad, f"{pairs} pairs, 0 exceptions")

# ---- A4. THE PENCIL (PREDICTIONS.md P2 -- a HARD control, not a prediction)
bad = []
for P in POP6:
    n = P.n
    Q, N = pencil(P)
    for k in range(1, n):
        for l in range(1, n):
            pk, pl = psi(n, k), psi(n, l)
            # bilinear energy from the definition
            e = F(0)
            S = P.S()
            for i in range(n):
                for j in range(i + 1, n):
                    e += S[i][j] * (pk[i] - pk[j]) * (pl[i] - pl[j])
            if Q[k - 1][l - 1] != e:
                bad.append((P, k, l, "Q"))
            ip = sum(pk[i] * pl[i] for i in range(n))
            if N[k - 1][l - 1] != ip:
                bad.append((P, k, l, "N"))
    for k in range(1, n):
        if Q[k - 1][k - 1] != P.leak(range(k)):
            bad.append((P, k, "Qkk != leak(A_k)"))
arm("A4  pencil closed forms == definitions, and Q_kk == leak(A_k)",
    not bad, f"{len(POP6)} posets, 0 exceptions")

# ---- A5. psi is a basis of 1^perp and the monotone cone is exactly c >= 0
bad = []
for P in POP6[:400]:
    n = P.n
    for c in [[F(1)] * (n - 1), [F(k + 1) for k in range(n - 1)],
              [F(0)] * (n - 2) + [F(1)]]:
        f = from_coeffs(n, c)
        if sum(f) != 0 or not is_monotone(f):
            bad.append((P, c))
    if n >= 3:                                   # a c with a negative entry breaks it
        c = [F(1)] + [F(-1)] + [F(0)] * (n - 3)
        f = from_coeffs(n, c)
        if is_monotone(f):
            bad.append((P, "negative c stayed monotone"))
arm("A5  sum c_k psi_k is centred and monotone iff c >= 0", not bad)

# ---- A6. exact PSD test on hand cases
arm("A6  psd_exact on hand cases",
    psd_exact([[F(1), F(0)], [F(0), F(1)]]) and
    psd_exact([[F(1), F(1)], [F(1), F(1)]]) and
    not psd_exact([[F(1), F(2)], [F(2), F(1)]]) and
    not psd_exact([[F(-1, 3)]]) and
    psd_exact([[F(0)]]))

# ---- A7. gap_at_least agrees with a float eigenvalue of the pencil (cross-check)
SUB = POP6[::17]
outside, widest = [], 0.0
for P in SUB:
    lo, hi = gap_exact_bounds(P, iters=30)
    Q, N = pencil(P)
    mu = pencil_eigs(Q, N)[0][0]
    widest = max(widest, float(hi - lo))
    if not (float(lo) - 1e-9 <= mu <= float(hi) + 1e-9):
        outside.append((P, float(lo), mu, float(hi)))
arm("A7  the FLOAT pencil eigenvalue lies inside the EXACT bisection bracket on 1-lambda_std",
    not outside,
    f"{len(SUB)} posets, 0 outside; widest bracket {widest:.3e}  [FLOAT is the checked side]")

# ---- A8. 1-lambda_std == 0 exactly iff the poset is decomposable
bad = [P for P in POP6 if gap_at_least(P, F(1, 10 ** 6)) == (not P.is_primitive())]
arm("A8  1-lambda_std > 0 iff ordinal-sum-indecomposable", not bad,
    f"{len(POP6)} posets, 0 exceptions")

# ---- A9. R(g) >= 1-lambda_std for EVERY g (PREDICTIONS.md E2 guard)
bad = []
EPS = F(1, 10 ** 6)
for P in POP6[::5]:
    n = P.n
    for c in [[F(1)] * (n - 1), [F(k + 1) for k in range(n - 1)],
              [F(0)] * (n - 2) + [F(1)], [F(1)] + [F(0)] * (n - 2)]:
        f = from_coeffs(n, c)
        r = rayleigh(P, f)
        # 1-lambda_std is a MINIMUM over 1^perp, so 1-lambda_std <= R(g) for every g.
        # Exactly: the gap cannot be >= R(g) + eps.  A violation means `rayleigh` and
        # `gap_at_least` disagree, and every certificate in this instrument is void.
        if gap_at_least(P, r + EPS):
            bad.append((P, c, float(r)))
arm("A9  1-lambda_std <= R(g) for every test vector built, exactly (E2 guard)",
    not bad, f"{len(POP6[::5])} posets x 4 vectors")

# ---- A10. the footrule identity, INDEPENDENTLY of the claim it supports
bad = []
for P in POP6:
    lhs = sum(P.leak(range(k)) for k in range(1, P.n))
    if lhs != P.E_footrule() / 2:
        bad.append(P)
arm("A10 sum_k leak(A_k) == E[footrule]/2", not bad,
    f"{len(POP6)} posets, 0 exceptions")

# ---- A12. THE THEOREM AGAINST BRUTE FORCE.  For every monotone rational g I build,
#           Phi*_pref^2 <= sweep_bound_sq(Delta_P, R(g)).  This is the single most
#           important control in the file: it tests the L2-FREE sweep theorem itself
#           against an exhaustive minimisation over prefixes.  EXACT.
bad, checks = [], 0
for P in POP6[::3]:
    n = P.n
    dmax = P.delta_max()
    ps, _ = P.phi_star_prefix()
    cands = [[F(1)] * (n - 1), [F(k + 1) for k in range(n - 1)],
             [F(n - k) for k in range(n - 1)], [F(0)] * (n - 2) + [F(1)],
             [F(1)] + [F(0)] * (n - 2), [F(1, k + 1) for k in range(n - 1)]]
    for c in cands:
        g = from_coeffs(n, c)
        assert is_monotone(g)
        r = rayleigh(P, g)
        checks += 1
        if ps * ps > sweep_bound_sq(dmax, r):
            bad.append((P, c, float(ps), float(r)))
arm("A12 THE L2-FREE SWEEP THEOREM vs BRUTE FORCE: Phi*_pref^2 <= R(g)(2Delta_P - R(g)) "
    "for every monotone g", not bad, f"{checks} (poset, monotone vector) pairs, 0 exceptions")

# ---- A13. the sharp bound really is sharper than the parent's 2R, and both are valid
bad = []
for P in POP6[::3]:
    dmax = P.delta_max()
    for r in [F(1, 10), F(1, 3), F(1, 2), F(9, 10)]:
        if sweep_bound_sq(dmax, r) > 2 * dmax * r + F(1, 10 ** 12):
            bad.append((P, r))
arm("A13 the sharp sweep bound never exceeds the parent's 2*Delta_P*R form", not bad)

# ---- A11. sum_k min(k,n-k) == floor(n^2/4)
bad = [n for n in range(2, 10)
       if sum(min(k, n - k) for k in range(1, n)) != (n * n) // 4]
arm("A11 sum_{k=1}^{n-1} min(k,n-k) == floor(n^2/4)", not bad)

# ================= NEGATIVE CONTROLS / MUTATION TESTS (E4) =================

print("-- negative controls: each one BREAKS something and asserts the check notices --")

# ---- C1. mutate a weight: A2 must fail
P = POP6[len(POP6) // 2]
n = P.n
S = [row[:] for row in P.S()]
S[0][n - 1] += F(1, 7)
S[n - 1][0] += F(1, 7)


class _Mut(Poset):
    def S(self):
        return S


Pm = _Mut(P.n, P.rel, "mutant")
caught = any(Pm.energy([F(1) if i in A else F(0) for i in range(n)]) != Pm.leak(A)
             for m in range(1, n) for A in combinations(range(n), m))
arm("C1  a perturbed weight matrix IS caught by the energy/leak cross-check", caught)

# ---- C2. the footrule identity is not vacuous: a wrong constant fails
bad = [P for P in POP6 if sum(P.leak(range(k)) for k in range(1, P.n))
       == P.E_footrule() / 3 and P.E_footrule() != 0]
arm("C2  the footrule identity fails with the constant 1/3 in place of 1/2",
    not bad, "0 posets satisfy the mutated identity with a nonzero footrule")

# ---- C3. gap_at_least is not vacuously true: it must reject r above the gap
bad = []
for P in POP6[::11]:
    lo, hi = gap_exact_bounds(P, iters=20)
    if gap_at_least(P, hi + F(1, 100)):
        bad.append(P)
arm("C3  gap_at_least REJECTS an r above the bracket", not bad)

# ---- C4. gap_at_least is not vacuously false: it must accept r = 0
arm("C4  gap_at_least ACCEPTS r = 0 everywhere",
    all(gap_at_least(P, F(0)) for P in POP6))

# ---- C5. cone_min never returns below the unconstrained minimum, and its returned
#          vector really is in the cone
bad = []
for P in POP6[::9]:
    Q, N = pencil(P)
    mu2 = pencil_eigs(Q, N)[0][0]
    val, c = cone_min(Q, N)
    if c is None or val < mu2 - 1e-9 or any(x < -1e-12 for x in c):
        bad.append((P, val, mu2))
    else:
        f = from_coeffs(P.n, rationalise(c))
        if not is_monotone(f):
            bad.append((P, "rationalised vector is not monotone"))
arm("C5  cone_min >= unconstrained min, and its vector is monotone after rationalising",
    not bad, f"{len(POP6[::9])} posets  [FLOAT search, exact monotonicity assert]")

# ---- C6. THE TARGET IS NOT VACUOUS -- and the ladder that shows it is a measurement
#          in its own right: the SMALLEST constant K for which Phi*_pref^2 <= K(1-lam)
#          holds on this population is the TRUE C_3^(III) here, route-independent.
print("     C6 ladder: Phi*_pref^2 <= K*(1-lambda_std), failures out of 5230 posets")
ladder = [F(1, 10), F(1, 5), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1), F(2)]
res = {}
for K in ladder:
    res[K] = sum(1 for P in POP6 if not gap_at_least(P, P.phi_star_prefix()[0] ** 2 / K))
    print(f"       K = {str(K):>5}:  {res[K]:5d} failures")
arm("C6  the target is NOT vacuous: it FAILS at small K and HOLDS at K = 2",
    res[F(1, 10)] > 0 and res[F(2)] == 0,
    f"K=1/10 fails at {res[F(1,10)]} posets, K=2 fails at 0 -- so the check discriminates")

# ---- C7. the route-independent worst case: max Phi*_pref^2 / (2(1-lambda_std)) over
#          PRIMITIVE posets, bracketed EXACTLY by bisection on gap_at_least.
prim = [P for P in POP6 if P.is_primitive()]
lo, hi = F(0), F(2)
for _ in range(22):
    mid = (lo + hi) / 2
    if all(gap_at_least(P, P.phi_star_prefix()[0] ** 2 / (2 * mid)) for P in prim):
        hi = mid
    else:
        lo = mid
print(f"     C7 [EXACT bracket] the smallest c with Phi*_pref^2 <= 2c(1-lambda_std) at ALL")
print(f"        {len(prim)} PRIMITIVE posets n<=6 lies in [{float(lo):.6f}, {float(hi):.6f}]")
arm("C7  the TRUE C_3^(III) on this population is strictly below 1", hi < 1,
    f"c_true <= {float(hi):.6f} over {len(prim)} primitive posets n <= 6  [EXACT]")

print(f"\n{ok}/{ok} arms pass.")
