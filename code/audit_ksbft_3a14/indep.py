"""indep.py (mg-3a14) -- INDEPENDENT exact re-computation of the EMPIRICAL
claims of docs/KSBFT-B-case-c-attack.md (mg-d707).  Shares no code with
code/ksbft_case_c_d707/census.c: exact integer/Fraction arithmetic, a
different poset generator (upward closure check on relations), and a
forward/backward ideal DP written from scratch.

Usage: python3 indep.py all N      -- exhaustive over naturally labelled posets
       python3 indep.py witness    -- the specific posets the doc names
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations
from functools import lru_cache

def stats(n, down):
    """down[j] = bitmask of strict down-set of j.  Returns dict of exact stats."""
    full = (1 << n) - 1
    up = [0]*n
    for j in range(n):
        for i in range(n):
            if down[j] >> i & 1: up[i] |= 1 << j
    inc = [full & ~(down[i] | up[i] | (1 << i)) for i in range(n)]
    # forward counts N over ideals
    N = {0: 1}
    order = [0]
    k = 0
    while k < len(order):
        I = order[k]; k += 1
        for x in range(n):
            if not I >> x & 1 and (down[x] & ~I) == 0:
                J = I | 1 << x
                if J not in N: N[J] = 0; order.append(J)
                N[J] += N[I]
    B = {}
    for I in reversed(order):
        if I == full: B[I] = 1; continue
        B[I] = sum(B[I | 1 << x] for x in range(n)
                   if not I >> x & 1 and (down[x] & ~I) == 0)
    e = N[full]
    hs = [0]*n                       # sum of positions * count
    before = [[0]*n for _ in range(n)]   # before[x][y] = #ext with x before y
    for I in order:
        if I == full: continue
        pos = bin(I).count("1") + 1
        for x in range(n):
            if not I >> x & 1 and (down[x] & ~I) == 0:
                w = N[I] * B[I | 1 << x]
                hs[x] += w * pos
                for y in range(n):
                    if y != x and not I >> y & 1: before[x][y] += w
    h = [Fr(hs[x], e) for x in range(n)]
    return e, h, before, inc

def connected(n, inc):
    seen = 1; fr = 1
    while fr:
        nf = 0
        for i in range(n):
            if fr >> i & 1: nf |= inc[i]
        nf &= ~seen; seen |= nf; fr = nf
    return seen == (1 << n) - 1

def analyse(n, down):
    e, h, before, inc = stats(n, down)
    pi = max(bin(m).count("1") for m in inc)
    ordr = sorted(range(n), key=lambda x: (h[x], x))
    d = [h[ordr[i]] - (i + 1) for i in range(n)]
    M = max(abs(t) for t in d)
    delta = Fr(0)
    for x in range(n):
        for y in range(x+1, n):
            if inc[x] >> y & 1:
                p = Fr(before[x][y], e); delta = max(delta, min(p, 1-p))
    def BK(K):
        b = Fr(0); K = min(K, n)
        for seg in (ordr[:K], ordr[n-K:]):
            for x, y in combinations(seg, 2):
                if inc[x] >> y & 1:
                    p = Fr(before[x][y], e); b = max(b, min(p, 1-p))
        return b
    minpair = min((Fr(before[x][y], e) for x in range(n) for y in range(n)
                   if x != y and inc[x] >> y & 1), default=None)
    return dict(e=e, pi=pi, M=M, d=d, d1=d[0], delta=delta,
                B3=BK(3), B4=BK(4), minpair=minpair, conn=connected(n, inc))

def gen(n):
    down = [0]*n
    def rec(j):
        if j == n:
            yield list(down); return
        for S in range(1 << j):
            cl = S
            for i in range(j):
                if S >> i & 1: cl |= down[i]
            if cl != S: continue
            down[j] = S
            yield from rec(j+1)
    yield from rec(0)

def run_all(n):
    total = conn = 0
    rows = {}
    for dn in gen(n):
        total += 1
        r = analyse(n, dn)
        if not r["conn"] or n < 2: continue
        conn += 1
        row = rows.setdefault(r["pi"], dict(cnt=0, minM=None, wM=None, minratio=None, minB4=None, minB3=None, mindelta=None))
        row["cnt"] += 1
        ratio = r["d1"] * (r["pi"] + 1)
        for key, val, w in (("minM", r["M"], dn), ("minratio", ratio, None), ("minB4", r["B4"], None),
                            ("minB3", r["B3"], None), ("mindelta", r["delta"], None)):
            if row[key] is None or val < row[key]:
                row[key] = val
                if key == "minM": row["wM"] = (list(dn), r["delta"])
    print(f"n={n} posets={total} connected={conn}")
    for pi in sorted(rows):
        rw = rows[pi]
        print(f"  pi={pi} count={rw['cnt']} minM={rw['minM']} ({float(rw['minM']):.6f}) wM={rw['wM'][0]} delta(wM)={rw['wM'][1]}"
              f" min d1*(pi+1)={rw['minratio']} minB3={float(rw['minB3']):.6f} minB4={rw['minB4']} mindelta={rw['mindelta']}")

def chain_closure(n, rel):
    down = [0]*n
    for (i, j) in rel: down[j] |= 1 << i
    for j in range(n):
        s = down[j]
        for i in range(j-1, -1, -1):
            if s >> i & 1: s |= down[i]
        down[j] = s
    return down

def witness():
    F = [0, 1]
    for _ in range(60): F.append(F[-1] + F[-2])
    for name, n, dn in (("doc n=6 minimiser", 6, [0,0,1,3,5,23]),
                        ("doc n=7 minimiser", 7, [0,0,1,1,7,7,31]),
                        ("doc n=8 minimiser", 8, [0,0,1,1,3,7,13,63])):
        # sanity: given masks must already be down-closed
        assert chain_closure(n, [(i, j) for j in range(n) for i in range(n) if dn[j] >> i & 1]) == dn, name
        r = analyse(n, dn)
        print(f"{name} {dn}: conn={r['conn']} pi={r['pi']} e={r['e']} M={r['M']} delta={r['delta']} d={[str(t) for t in r['d']]}")
    for m in range(1, 7):
        n = 2*m + 1
        dn = chain_closure(n, [(i, j) for j in range(n) for i in range(n) if j - i >= 2])
        r = analyse(n, dn)
        print(f"Fibonacci F_m m={m}: M={r['M']} == F2m/F2m+2={Fr(F[2*m], F[2*m+2])} ? {r['M'] == Fr(F[2*m], F[2*m+2])}; "
              f"d={[str(t) for t in r['d']]}")
    for k in range(2, 6):
        n = 2*k
        rel = [(i, i+1) for i in range(k-1)] + [(k+i, k+i+1) for i in range(k-1)]
        dn = chain_closure(n, rel)
        r = analyse(n, dn)
        print(f"two parallel {k}-chains: pi={r['pi']} min P[u<v]={r['minpair']} 1/C(2k,k)={Fr(1, __import__('math').comb(2*k, k))}")
    for D in range(1, 7):
        n = D + 1
        dn = chain_closure(n, [(i, i+1) for i in range(D-1)])   # chain 0..D-1, point D
        r = analyse(n, dn)
        print(f"D-chain + point D={D}: pi={r['pi']} d1={r['d1']} 1/(D+1)={Fr(1, D+1)}")

if __name__ == "__main__":
    if sys.argv[1] == "all": run_all(int(sys.argv[2]))
    else: witness()
