"""mg-2198 -- independent audit of mg-5371 (docs/KSBFT-L-heavy-atom.md).
Written from scratch; imports nothing from code/ksbft_l_heavy_atom_5371 or code/ksbft_g_constants_b852.
  [A] F(m,k) by brute-force downset DP (own implementation): AK25b Thm 2.6 hypotheses, (4) at 1/(k+1),
      P(A<x<B) closed form, the (pi k/2)^(-m/2) sqrt(2/mk) bound, AK25b's own D,U at eps_delta.
  [B] exponent coefficient log(1/P)/(m log(1/eps4)) for large m (exact big-int closed form).
  [C] the ceiling: delta_x, q(x) of F(m,k) for k even AND odd.
  [D] the explicit non-unimodal Dilworth instance of sec 3.3, by the same DP.
  [E] the q0 -> L chain re-implemented from mg-b852's DOC formulas (sec 3.2-3.4), log-space.
Controls: each check prints PASS/FAIL; negative controls print FIRES / DOES NOT FIRE."""
from fractions import Fraction as Fr
from math import comb, log, pi, sqrt, e, ceil
import sys

# ---------------------------------------------------------------- [A] poset machinery
def closure(n, pred):
    pred = [set(p) for p in pred]
    changed = True
    while changed:
        changed = False
        for i in range(n):
            new = set(pred[i])
            for j in pred[i]: new |= pred[j]
            if new != pred[i]: pred[i] = new; changed = True
    return [sum(1 << j for j in p) for p in pred]

def down_counts(n, pm):
    """N[S] = # linear extensions of the downset S (0 if S not a downset); forward DP."""
    N = {0: 1}
    frontier = [0]
    for _ in range(n):
        nxt = {}
        for S in frontier:
            c = N[S]
            for v in range(n):
                if not (S >> v) & 1 and (pm[v] & S) == pm[v]:
                    T = S | (1 << v); nxt[T] = nxt.get(T, 0) + c
        N.update(nxt); frontier = list(nxt)
    return N

def up_counts(n, pm):
    """M[S] = # extensions of P - S (S a downset) = # ways to finish from S."""
    full = (1 << n) - 1
    N = down_counts(n, pm)
    M = {full: 1}
    for S in sorted(N, key=lambda s: -bin(s).count('1')):
        if S == full: continue
        tot = 0
        for v in range(n):
            if not (S >> v) & 1 and (pm[v] & S) == pm[v]:
                tot += M[S | (1 << v)]
        M[S] = tot
    return N, M

def placements(n, pm, x):
    """list of (S, weight): S = set placed before x; weight = # extensions with that prefix-set."""
    N, M = up_counts(n, pm)
    out = []
    for S, c in N.items():
        if not (S >> x) & 1 and (pm[x] & S) == pm[x]:
            out.append((S, c * M[S | (1 << x)]))
    return out, N[(1 << n) - 1]

def F(m, k):
    n = m * k + 1
    pred = [[] for _ in range(n)]
    for i in range(m):
        for l in range(1, k): pred[i * k + l] = [i * k + l - 1]
    return n, closure(n, pred), m * k   # x = last index, isolated

def P_before(pl, tot, cond): return Fr(sum(w for S, w in pl if cond(S)), tot)

allok = True
def check(name, ok):
    global allok
    allok &= ok
    print("  %-72s %s" % (name, "PASS" if ok else "FAIL"))

print("== [A] F(m,k) brute force (own DP)")
for (m, k, j) in [(1, 2, 1), (2, 2, 1), (3, 2, 1), (4, 2, 1), (5, 2, 1), (2, 4, 2), (3, 4, 2), (2, 6, 3), (2, 3, 1), (2, 5, 2)]:
    n, pm, x = F(m, k)
    pl, tot = placements(n, pm, x)
    el = lambda i, l: i * k + (l - 1)   # c_{i,l}, l 1-based
    D = [el(i, l) for i in range(m) for l in range(1, j + 1)]
    U = [el(i, l) for i in range(m) for l in range(j + 1, k + 1)]
    Dmask = sum(1 << d for d in D)
    # Thm 2.6 structural hypotheses: D ideal, U filter, A=max(D), B=min(U)
    ideal = all((pm[d] & ~Dmask) == 0 for d in D)
    filt = all(not ((pm[v] >> u) & 1) for u in U for v in D)   # nothing in D above something in U
    A = [el(i, j) for i in range(m)]; B = [el(i, j + 1) for i in range(m)]
    maxD = [d for d in D if not any((pm[e2] >> d) & 1 for e2 in D)]
    minU = [u for u in U if not any((pm[u] >> e2) & 1 for e2 in U)]
    struct = ideal and filt and sorted(maxD) == sorted(A) and sorted(minU) == sorted(B)
    # (4)
    p4 = [P_before(pl, tot, lambda S, a=a, b=b: (S >> a) & 1 and not (S >> b) & 1) for a in A for b in B]
    min4 = min(p4)
    atom = P_before(pl, tot, lambda S: S == Dmask)
    closed = Fr(comb(k, j) ** m, comb(m * k, m * j) * (m * k + 1))
    # q(x)
    dist = [0] * n
    for S, w in pl: dist[bin(S).count('1')] += w
    q = Fr(max(dist), tot); unif = len(set(dist)) == 1
    print(f" m={m} k={k} j={j}: struct={struct} min(4)={min4} (1/(k+1)={Fr(1,k+1)}) atom={atom} closed={closed} q={q} uniform={unif}")
    check(f"F({m},{k}) j={j}: hypotheses of Thm 2.6 + (4)>=1/(k+1) + closed form + q=1/(mk+1)",
          struct and min4 >= Fr(1, k + 1) and atom == closed and q == Fr(1, m * k + 1) and unif)
    if k % 2 == 0 and j == k // 2 and m >= 1:
        bound = (pi * k / 2) ** (-m / 2) * sqrt(2 / (m * k))
        check(f"F({m},{k}): atom <= (pi k/2)^(-m/2) sqrt(2/mk) = {bound:.4g}", float(atom) <= bound)
        # AK25b's own D,U at eps_delta = 1/(2(k+1)), using 2eps in (4): same sets?
        ed = Fr(1, 2 * (k + 1))
        hx = [P_before(pl, tot, lambda S, y=y: (S >> y) & 1) for y in range(n - 1)]
        Dak = sorted(y for y in range(n - 1) if hx[y] >= Fr(1, 2) + ed)
        Uak = sorted(y for y in range(n - 1) if 1 - hx[y] >= Fr(1, 2) + ed)
        dx = max(min(h, 1 - h) for h in hx)
        check(f"F({m},{k}): delta_x = 1/2 - 1/(2(k+1)) and AK25b's D,U (p.5) = this D,U",
              dx == Fr(1, 2) - ed and Dak == sorted(D) and Uak == sorted(U))
# negative control: the instrument must see a WRONG closed form (drop (mk+1)) as wrong
n, pm, x = F(3, 2); pl, tot = placements(n, pm, x)
atom = P_before(pl, tot, lambda S: S == 0b010101)
wrong = Fr(comb(2, 1) ** 3, comb(6, 3))
print("  negative control, closed form without (mk+1):", "FIRES" if atom != wrong else "DOES NOT FIRE")
# negative control on (4): a cross pair with j and j+1 swapped must violate
print("  negative control, (4) with b=c_{l,j} (not j+1) gives P=%s < 1/3:" % P_before(pl, tot, lambda S: (S >> 0) & 1 and not (S >> 2) & 1),
      "FIRES" if P_before(pl, tot, lambda S: (S >> 0) & 1 and not (S >> 2) & 1) < Fr(1, 3) else "DOES NOT FIRE")

print("\n== [A''] (F3) cross-chain values P(c_{1,j}<x<c_{2,j+1}) in F(2,k)")
for k in [2, 4, 6, 8]:
    j = k // 2; n, pm, x = F(2, k); pl, tot = placements(n, pm, x)
    v = P_before(pl, tot, lambda S: (S >> (j - 1)) & 1 and not (S >> (k + j)) & 1)
    print("   k=%d: %s (doc: 11/30, 17/70, 1129/6006, 6841/43758) >= 1/(k+1): %s" % (k, v, v >= Fr(1, k + 1)))
print("\n== [A'] k=2 bound atom < 2^-m, exact, m=1..200")
check("2^m/(C(2m,m)(2m+1)) < 2^-m for m=1..200",
      all(Fr(2 ** m, comb(2 * m, m) * (2 * m + 1)) < Fr(1, 2 ** m) for m in range(1, 201)))
check("identity 2^m m!^2/(2m+1)! == 2^m/(C(2m,m)(2m+1)), m=1..50",
      all(Fr(2 ** m * __import__('math').factorial(m) ** 2, __import__('math').factorial(2 * m + 1)) == Fr(2 ** m, comb(2 * m, m) * (2 * m + 1)) for m in range(1, 51)))
check("(pi k/2)^(-m/2)sqrt(2/mk) bound, k even 2..20, m 1..60 (log-space)",
      all(log(comb(k, k // 2)) * m - log(comb(m * k, m * k // 2)) - log(m * k + 1)
          <= -(m / 2) * log(pi * k / 2) + 0.5 * log(2 / (m * k)) + 1e-12
          for k in range(2, 21, 2) for m in range(1, 61)))

print("\n== [B] exponent coefficient c(k) = lim log(1/atom)/(m log(1/eps4)), eps4 = 1/(k+1), at m=2000")
for k in [2, 4, 6, 8, 10, 20, 50, 100]:
    m = 2000; j = k // 2
    la = m * log(comb(k, j)) - log(comb(m * k, m * j)) - log(m * k + 1)
    print("   k=%3d eps4=1/%d: log(1/atom)/(m log(k+1)) = %.4f   (m->inf limit (k log2 - log C(k,k/2))/log(k+1) = %.4f)"
          % (k, k + 1, -la / (m * log(k + 1)), (k * log(2) - log(comb(k, j))) / log(k + 1)))

print("\n== [C] the ceiling: delta_x and q(x) of F(m,k), k even and odd (exact DP)")
for (m, k) in [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 3)]:
    n, pm, x = F(m, k); pl, tot = placements(n, pm, x)
    hx = [P_before(pl, tot, lambda S, y=y: (S >> y) & 1) for y in range(n - 1)]
    dx = max(min(h, 1 - h) for h in hx)
    dist = [0] * n
    for S, w in pl: dist[bin(S).count('1')] += w
    epsd = Fr(1, 2) - dx
    formula = (Fr(1, (m * k + 1)))
    ce = None if epsd == 0 else 1 / (m * (1 / (2 * epsd) - 1) + 1)
    print(f"   F({m},{k}) width {m+1}: delta_x={dx} eps={epsd} q(x)={Fr(max(dist), tot)} ceiling formula 1/((w-1)(1/(2eps)-1)+1)={ce}")
    if k % 2 == 0: check(f"F({m},{k}) ceiling formula == q(x)", ce == Fr(max(dist), tot))
    else: check(f"F({m},{k}) k odd: delta_x = 1/2 (odd k gives NO ceiling point)", dx == Fr(1, 2))
for eps in [Fr(1, 6)]:
    for w in [3, 10, 10 ** 6]:
        c = 1 / ((w - 1) * (1 / (2 * eps) - 1) + 1)
        print(f"   eps=1/6 w={w}: ceiling={float(c):.4g}, 2eps/w={float(2*eps/w):.4g}, ratio ceiling/(2eps/w)={float(c/(2*eps/w)):.4f}")

print("\n== [D] sec 3.3 explicit non-unimodal instance")
masks = [112, 113, 272, 115, 0, 0, 0, 115, 0]
n = 9
pm = closure(n, [[j for j in range(n) if (mk >> j) & 1] for mk in masks])
print("   transitively closed as given:", pm == masks)
x = 2; C = [1, 3, 5]
isChain = all(((pm[b] >> a) & 1) or ((pm[a] >> b) & 1) for a in C for b in C if a != b)
comp = lambda a, b: ((pm[a] >> b) & 1) or ((pm[b] >> a) & 1)
Pi = [y for y in range(n) if y != x and not comp(x, y)]
def width(S):
    best = 0
    for r in range(1 << len(S)):
        sub = [S[i] for i in range(len(S)) if (r >> i) & 1]
        if all(not comp(a, b) for a in sub for b in sub if a < b): best = max(best, len(sub))
    return best
wPi = width(Pi); wRest = width([y for y in Pi if y not in C])
pl, tot = placements(n, pm, x)
dist = [0] * 4
for S, w in pl: dist[sum((S >> c) & 1 for c in C)] += w
g = __import__('math').gcd(*dist)
print(f"   C chain={isChain} C in Pi(x)={all(c in Pi for c in C)} Pi(x)={Pi} w(Pi)={wPi} w(Pi-C)={wRest} e(P)={tot}")
print(f"   N_C(x) distribution (counts) = {dist}, /gcd = {[d//g for d in dist]}")
check("instance: C Dilworth-type chain, N_C distribution proportional to [20,120,114,138], non-unimodal",
      isChain and all(c in Pi for c in C) and wRest == wPi - 1 and [d * 20 for d in dist] == [dd * dist[0] for dd in [20, 120, 114, 138]]
      and dist[1] > dist[2] < dist[3])
# Stanley positive control: f(x) itself log-concave here
fd = [0] * n
for S, w in pl: fd[bin(S).count('1')] += w
check("control: Stanley f(x) log-concave on the same instance", all(fd[i] ** 2 >= fd[i - 1] * fd[i + 1] for i in range(1, n - 1)))
# trivial chain example
n2 = 6; pm2 = closure(n2, [[], [0], [1], [2], [3], []])   # v<c1<c2<u<c3, x=5 isolated
pl2, tot2 = placements(n2, pm2, 5)
d2 = [0] * 4
for S, w in pl2: d2[sum((S >> c) & 1 for c in [1, 2, 4])] += w
check("trivial example v<c1<c2<u<c3 + isolated x gives [2,1,2,1]", d2 == [2, 1, 2, 1])

print("\n== [E] q0 -> L chain, re-implemented from mg-b852 DOC sec 3.2-3.4 formulas (log10 space)")
LN10 = log(10)
def log10L(l10q0):
    """log10 L for log10 q0.  eta = 1/(16 sqrt(300/q0^2+1)); B=ceil(2e/eta); K44=(3B+1)(B+1);
    TD=4K44+1; D=3 sqrt300/eta^1.5; gam=3mu^3/160 (mu=1/4); C=2 TD D/gam; t=2+2 TD ln(6/(gam eta));
    K32=80 C t/(eta mu^2); K31=2K32+2; L=K31^2."""
    mu = 0.25; gam = 3 * mu ** 3 / 160
    # log10 eta: eta = q0/(16 sqrt(300 + q0^2))
    if l10q0 > -300:
        q0 = 10 ** l10q0
        le = log(q0 / (16 * sqrt(300 + q0 * q0)), 10)
    else:
        le = l10q0 - log(16 * sqrt(300), 10)
    lx = -le                                        # log10(1/eta)
    if lx < 25:   # direct float evaluation only where nothing overflows
        eta = 10 ** le
        B = ceil(2 * e / eta); K44 = (3 * B + 1) * (B + 1); TD = 4 * K44 + 1
        D = 3 * sqrt(300) / eta ** 1.5
        C = 2 * TD * D / gam; t = 2 + 2 * TD * log(6 / (gam * eta))
        K32 = 80 * C * t / (eta * mu * mu)
        return 2 * log(2 * K32 + 2, 10)
    lB = log(2 * e, 10) + lx
    lTD = log(12, 10) + 2 * lB                      # 4(3B+1)(B+1) ~ 12 B^2
    lD = log(3 * sqrt(300), 10) + 1.5 * lx
    lC = log(2, 10) + lTD + lD - log(gam, 10)
    lt = log(2, 10) + lTD + log(log(6 / gam) + lx * LN10, 10)
    lK32 = log(80, 10) + lC + lt + lx - 2 * log(mu, 10)
    return 2 * (log(2, 10) + lK32)

def width_bound(eps):   # KSBFT p.25 via mg-c929's form, as quoted in mg-b852 sec 1
    G1 = 10 * e * (1 + sqrt(3)) / eps ** 3
    A = 18432 * sqrt(3) / eps ** 3
    return 2 * sqrt(3) * max(G1, 4 * A * log(A) ** 2) / eps
K0 = float(int(width_bound(1 / e - 1 / 3)))
CB = (5 - sqrt(5)) / 10
K12 = float(round(width_bound(1 / e - CB)))
print("   K0 = %.4e (mg-b852: 1.301e14)  K12 = %.4e (mg-b852: 1.944e12)" % (K0, K12))
sixth = 1 / 6; eT = 0.5 - CB
shapes = [("(2e)^(w^2)", lambda w, ep: w * w * log(2 * ep, 10), 1.050e29, 119.1, -1.717e25),
          ("(2e)^(0.6309w)", lambda w, ep: 0.6309 * w * log(2 * ep, 10), 5.09e14, None, -5.6e12),
          ("(2e)^w", lambda w, ep: w * log(2 * ep, 10), 8.07e14, 81.6, -8.83e12),
          ("(2e/w)^w", lambda w, ep: w * log(2 * ep / w, 10), 2.47e16, 100.4, -3.19e14),
          ("(2e/w)^3", lambda w, ep: 3 * log(2 * ep / w, 10), 633.7, 100.4, -559.0),
          ("2e/w", lambda w, ep: log(2 * ep / w, 10), 253.5, 75.4, -229.7)]
for name, f, dLs, dL4, dE in shapes:
    Ls = log10L(f(K0, sixth)); L4 = log10L(f(3, sixth)); L12 = log10L(f(K12, eT))
    le = min(log(6.8e-6, 10), log(0.0236, 10) - L12)
    ok = abs(Ls / dLs - 1) < 2e-3 and (dL4 is None or abs(L4 - dL4) < 0.15) and abs(le / dE - 1) < 2e-3 * (1 if name != "(2e)^(0.6309w)" else 10)
    print("   %-16s log10 L* = %-11.5g (doc %-9.4g) log10 L(4,1/6) = %-8.4g (doc %s) log10 eps12 = %-11.5g (doc %.4g)"
          % (name, Ls, dLs, L4, dL4, le, dE))
    check(f"row {name} reproduced", ok)
# negative control: a planted error (degree: D ~ eta^-1 instead of eta^-1.5) must change L*
wrong = log10L(K0 * K0 * log(1 / 3, 10)) * 12 / 13
print("   negative control: 12/13 of the w^2 row = %.4g vs doc 1.050e29 ->" % wrong, "FIRES" if abs(wrong / 1.050e29 - 1) > 2e-3 else "DOES NOT FIRE")
# the true ceiling value at eps=1/6 (not 2eps/w)
for w, lab in [(K0, "L*"), (3, "L(4,1/6)")]:
    c = 1 / ((w - 1) * (1 / (2 * sixth) - 1) + 1)
    print("   exact ceiling 1/((w-1)(1/(2eps)-1)+1) at eps=1/6, w=%s: log10 L = %.4f (row '2e/w' gives %.4f)"
          % (lab, log10L(log(c, 10)), log10L(log(2 * sixth / w, 10))))
print("   degree check: d log10 L / d log10(1/q0) near ceiling row = %.3f"
      % ((log10L(-20) - log10L(-19)) / 1))
print("\nALL:", "PASS" if allok else "FAIL")

print("\n== [F] sec 3.1 Attempt 2: P(A<x<B) vs P(A<x)P(x<B) on F(m,2), exact DP")
prev = None
rs = []
for m in range(1, 7):
    n, pm, x = F(m, 2); pl, tot = placements(n, pm, x)
    A = [2 * i for i in range(m)]; B = [2 * i + 1 for i in range(m)]
    pA = P_before(pl, tot, lambda S: all((S >> a) & 1 for a in A))
    pB = P_before(pl, tot, lambda S: not any((S >> b) & 1 for b in B))
    pj = P_before(pl, tot, lambda S: S == sum(1 << a for a in A))
    r = pj / (pA * pB); rs.append(r)
    print("   m=%d P(A<x)=%.4f P(x<B)=%.4f  sqrt(pi)/(2sqrt m)=%.4f  joint=%.3e  joint/(product)=%.4f"
          % (m, pA, pB, sqrt(pi) / (2 * sqrt(m)), float(pj), float(r)))
check("joint/product strictly decreasing in m=1..6 (consistent with exponential decay)", all(rs[i + 1] < rs[i] for i in range(5)))
print("\nALL (after [F]):", "PASS" if allok else "FAIL")
