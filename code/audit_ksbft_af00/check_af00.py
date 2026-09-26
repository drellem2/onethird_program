#!/usr/bin/env python3
"""mg-af00: independent audit instrument for KSBFT-P1 (mg-0b78). Shares NO code with
code/ksbft_p1_walled_0b78. Exact integers/Fractions. Instrument only: checks the specific
PROVEN claims of KSBFT-P1 §3.1/§5 on explicit posets; proves nothing beyond what it prints."""
import itertools, random, sys
from fractions import Fraction as Fr
from functools import lru_cache

def close(n, rel):
    lt = [[False]*n for _ in range(n)]
    for a, b in rel: lt[a][b] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]: lt[i][j] = True
    assert all(not lt[i][i] for i in range(n))
    return lt

def pos_counts(n, lt):
    """N[x][i] = #linear extensions with x at position i (1-based), by forward/backward ideal DP."""
    below = [sum(1 << j for j in range(n) if lt[j][i]) for i in range(n)]
    full = (1 << n) - 1
    @lru_cache(None)
    def fwd(I):  # number of extensions of ideal I
        if I == 0: return 1
        return sum(fwd(I & ~(1 << z)) for z in range(n) if (I >> z) & 1
                   and not any((I >> w) & 1 and lt[z][w] for w in range(n)))
    @lru_cache(None)
    def bwd(I):  # completions from ideal I
        if I == full: return 1
        return sum(bwd(I | (1 << z)) for z in range(n) if not (I >> z) & 1 and below[z] & I == below[z])
    N = [[0]*(n+2) for _ in range(n)]
    # enumerate ideals
    ideals = [0]; seen = {0}; k = 0
    while k < len(ideals):
        I = ideals[k]; k += 1
        for z in range(n):
            if not (I >> z) & 1 and below[z] & I == below[z]:
                J = I | (1 << z)
                N[z][bin(J).count("1")] += fwd(I) * bwd(J)
                if J not in seen: seen.add(J); ideals.append(J)
    return N, fwd(full)

def inc(n, lt, x): return [y for y in range(n) if y != x and not lt[x][y] and not lt[y][x]]
def rng(n, lt): return max((len(inc(n, lt, x)) for x in range(n)), default=0)

def pbefore(n, lt, x, y):
    return Fr(pos_counts(n, lt + [])[1], 1) and None

def delta(n, lt):
    # P[x before y] via extensions of P + (x<y)
    e = pos_counts(n, lt)[1]; best = None
    for x in range(n):
        for y in range(x+1, n):
            if not lt[x][y] and not lt[y][x]:
                lt2 = close(n, [(a, b) for a in range(n) for b in range(n) if lt[a][b]] + [(x, y)])
                p = Fr(pos_counts(n, lt2)[1], e); v = min(p, 1-p)
                best = v if best is None or v > best else best
    return best

out = []
def say(s): print(s); out.append(s)

# ---- 1. Prop 5.5 closed form, brute force: C_2 ⊔ C_D, x = bottom of C_2, i = 2 ----
say("[Prop 5.5] C_m ⊔ C_n, x=u1: brute-force Stanley ratio vs closed form 1+(m-1)/((t+1)(t-m+1))")
bad = 0
for m in range(2, 5):
    for n in range(2, 8):
        N_ = m + n
        rel = [(i, i+1) for i in range(m-1)] + [(m+i, m+i+1) for i in range(n-1)]
        lt = close(N_, rel); N, e = pos_counts(N_, lt); row = N[0]
        for j in range(1, n):  # interior i = 1+j, need j-1>=0 and j+1<=n
            i = 1 + j; t = n + m - 1 - j
            got = Fr(row[i]**2, row[i-1]*row[i+1]); want = 1 + Fr(m-1, (t+1)*(t-m+1))
            if got != want: bad += 1
say(f"  mismatches: {bad}")
for D in range(2, 9):
    N_ = 2 + D; lt = close(N_, [(0, 1)] + [(2+i, 3+i) for i in range(D-1)])
    N, e = pos_counts(N_, lt); r = N[0]
    say(f"  D={D}: range={rng(N_, lt)} deficit at i=2: {Fr(r[2]**2, r[1]*r[3]) - 1}  1/(D^2-1)={Fr(1, D*D-1)}")

# ---- 2. the exhibited range-4 poset with deficit 1/18 ----
say("[§5.3 exhibit] covers 0<1,1<3,1<5,1<6,2<5,2<6,3<4,3<7,6<7, x=5")
lt = close(8, [(0,1),(1,3),(1,5),(1,6),(2,5),(2,6),(3,4),(3,7),(6,7)])
N, e = pos_counts(8, lt)
say(f"  range={rng(8, lt)}  N(x=5)[1..8]={N[5][1:9]}  deficit at i=6: {Fr(N[5][6]**2, N[5][5]*N[5][7]) - 1}")

# ---- 3. Example 5.7 arithmetic ----
L = {'0': 1, 'a': 1, 'b': 1, 'ab': 3}; R = {'0': 3, 'a': 1, 'b': 1, 'ab': 1}
N0, N1, N2 = L['0']*R['0'], L['a']*R['a'] + L['b']*R['b'], L['ab']*R['ab']
say(f"[Ex 5.7] (N0,N1,N2)=({N0},{N1},{N2}), N1^2={N1*N1} < N0*N2={N0*N2}: {N1*N1 < N0*N2}")

# ---- 4. exhaustive n<=6 (+ random n=7,8): Prop 3.1(6) support, Lemma 5.1, Lemma 5.2 bounds,
#         Ma-Shenfeld k=1 consistency, and mg-48ab Thm 5.2 (full-support flat => delta>=1/3) ----
def ideals_of(n, lt, S):
    """down-sets of the induced subposet on S (list), as frozensets"""
    res = []
    for r in range(len(S)+1):
        for J in itertools.combinations(S, r):
            Js = set(J)
            if all(w in Js for z in J for w in S if lt[w][z]): res.append(frozenset(J))
    return res

def e_of(n, lt, S):
    S = list(S); m = len(S)
    if m == 0: return 1
    idx = {v: i for i, v in enumerate(S)}
    rel = [(idx[a], idx[b]) for a in S for b in S if lt[a][b]]
    return pos_counts(m, close(m, rel))[1]

stats = dict(posets=0, support_bad=0, l51_bad=0, l52_bad=0, ms_bad=0, eq=0, flat_full=0, thm52_bad=0, stanley_bad=0)
def check(n, lt, do_delta=True):
    stats['posets'] += 1
    N, e = pos_counts(n, lt)
    for x in range(n):
        I = inc(n, lt, x); d = sum(lt[y][x] for y in range(n)); p = len(I)
        sup = [i for i in range(1, n+1) if N[x][i] > 0]
        if sup != list(range(d+1, d+2+p)): stats['support_bad'] += 1
        Dn = [y for y in range(n) if lt[y][x]]
        dsets = ideals_of(n, lt, I)
        for j in range(p+1):
            s = 0
            for J in dsets:
                if len(J) == j:
                    K = set(Dn) | J
                    s += e_of(n, lt, K) * e_of(n, lt, set(range(n)) - K - {x})
            if s != N[x][d+1+j]: stats['l51_bad'] += 1
        for J in dsets:
            K = set(Dn) | J
            for z in I:
                if z not in J and (J | {z}) in dsets:
                    rL = Fr(e_of(n, lt, K | {z}), e_of(n, lt, K))
                    rR = Fr(e_of(n, lt, set(range(n)) - K - {x, z}), e_of(n, lt, set(range(n)) - K - {x}))
                    pz = len(inc(n, lt, z))
                    if not (1 <= rL <= pz+1 and Fr(1, pz+1) <= rR <= 1): stats['l52_bad'] += 1
        for i in range(d+2, d+1+p):
            a, b, c = N[x][i-1], N[x][i], N[x][i+1]
            if b*b < a*c: stats['stanley_bad'] += 1
            if b*b == a*c:
                stats['eq'] += 1
                if not (a == b == c): stats['ms_bad'] += 1
        if p >= 1 and len(set(N[x][i] for i in sup)) == 1:
            stats['flat_full'] += 1
            if do_delta and delta(n, lt) < Fr(1, 3): stats['thm52_bad'] += 1

seen = set()
for n in range(2, 7):
    pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
    for mask in range(1 << len(pairs)):
        rel = [pairs[k] for k in range(len(pairs)) if (mask >> k) & 1]
        lt = close(n, rel)
        key = (n, tuple(tuple(r) for r in lt))
        if key in seen: continue
        seen.add(key); check(n, lt)
say(f"[exhaustive labelled n<=6] {stats}")
random.seed(20260926)
for _ in range(int(sys.argv[1]) if len(sys.argv) > 1 else 300):
    n = random.choice([7, 8]); pr = random.choice([0.15, 0.25, 0.35])
    rel = [(i, j) for i in range(n) for j in range(i+1, n) if random.random() < pr]
    check(n, close(n, rel))
say(f"[+ random n=7,8] {stats}")

# ---- 5. CONTROLS ----
# positive control for the support check: a planted non-contiguous vector must be flagged
sup = [i for i, v in enumerate([0, 1, 0, 0, 1]) if v]
say(f"[control] non-contiguous support detected: {sup != list(range(sup[0], sup[-1]+1))}")
# (1,0,0,1) satisfies b^2 >= ac at every interior index yet has internal zeros:
v = [1, 0, 0, 1]
say(f"[control] (1,0,0,1) satisfies N_i^2>=N_(i-1)N_(i+1): {all(v[i]**2 >= v[i-1]*v[i+1] for i in (1, 2))}  -> 'log-concave => no internal zeros' needs the extra hypothesis")
# negative control for Thm 5.2 test: (2+1) is flat at the isolated point and has delta exactly 1/3 (tight, not < 1/3)
lt = close(3, [(0, 1)]); N, e = pos_counts(3, lt)
say(f"[control] (2+1): N(isolated)={N[2][1:4]} delta={delta(3, lt)}")
# the delta routine must see a sub-1/3... none exists; instead check it reports 1/2 on the 2-antichain and 2/5 on N
say(f"[control] delta(A_2)={delta(2, close(2, []))}  delta(N)={delta(4, close(4, [(0,2),(0,3),(1,3)]))}")

# ---- 6. Z_m (i<j iff j-i>=2): least strict deficit ----
for m in (6, 9, 12, 14):
    lt = close(m, [(i, j) for i in range(m) for j in range(i+2, m)]); N, e = pos_counts(m, lt)
    best = min((Fr(N[x][i]**2, N[x][i-1]*N[x][i+1]) - 1 for x in range(m) for i in range(2, m)
                if N[x][i-1] and N[x][i+1] and N[x][i]**2 != N[x][i-1]*N[x][i+1]), default=None)
    say(f"[Z_{m}] least strict deficit = {float(best):.6f}" if best is not None else f"[Z_{m}] none")
