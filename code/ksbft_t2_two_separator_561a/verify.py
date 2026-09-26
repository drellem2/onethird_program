"""verify.py (mg-561a): exact checks of the PROVEN statements of docs/KSBFT-T2-two-separator.md, with controls.

(V1) Swap Identity (Thm 1.1), ANY poset, any incomparable a,a':  |Lambda_1(a,a')| = |Lambda_1(a',a)|,
     hence P(Lambda_2(a,a')) - P(Lambda_2(a',a)) = P[a<a'] - P[a'<a].
     Populations: all interval orders n <= N; 3000 random general posets n = 5..8.
     CONTROL: with only the above-separators, the identity must fail.
(V2) Cor 1.2: if a dominates a' (interval sense; in general: down(a) <= down(a'), up(a) >= up(a')),
     S(a',a) is empty, so P(Lambda_2(a,a')) = 2P[a<a'] - 1 exactly.
(V3) Prop 2.2 (containment, Z = S): a' strictly contains a, S(a,a') = {s,t} = Z.  Then
     |Lambda_2^(1)| <= |Lambda_1| and |Lambda_2^(2)| <= |Lambda_1| (one / both separators between a and a').
     Also reports how often these fail when Z != S (not claimed).
usage: python3 verify.py N"""
import sys, os, random
from multiprocessing import Pool
from t2lib import *
from shape import shape

def gen_lambdas(dn, a, a2, S, count_between=False):
    """returns counts keyed by ('L3',) or ('L', k) = a before a' with k elements of S between."""
    S = frozenset(S)
    def step(s, v):
        if isinstance(s, tuple) and s[0] in ('L', 'L3'): return s
        if v == a: return 0
        if v == a2: return ('L3',) if s == 'pre' else ('L', s)
        if v in S and s != 'pre': return s + 1
        return s
    return auto_count(dn, 'pre', step)

def seps_general(n, LT, a, a2):
    COV = lambda x, y: LT[x][y] and not any(LT[x][c] and LT[c][y] for c in range(n))
    INC = lambda x, y: x != y and not LT[x][y] and not LT[y][x]
    A = [z for z in range(n) if COV(a, z) and INC(z, a2)]
    B = [z for z in range(n) if COV(z, a2) and INC(z, a)]
    return A, B

def check_poset(n, LT, iv=None):
    dn = [sum(1 << w for w in range(n) if LT[w][v]) for v in range(n)]
    out = dict(v1=0, v1bad=0, v1ctrl=0, v2=0, v2bad=0, v3=0, v3bad=0, v3z=0, v3zbad=0)
    INC = lambda x, y: x != y and not LT[x][y] and not LT[y][x]
    for a in range(n):
        for a2 in range(n):
            if not INC(a, a2): continue
            A, B = seps_general(n, LT, a, a2)
            A2, B2 = seps_general(n, LT, a2, a)
            c = gen_lambdas(dn, a, a2, A + B); c2 = gen_lambdas(dn, a2, a, A2 + B2)
            L1 = c.get(('L', 0), 0); L1r = c2.get(('L', 0), 0)
            out['v1'] += 1; out['v1bad'] += L1 != L1r
            cc = gen_lambdas(dn, a, a2, A); cc2 = gen_lambdas(dn, a2, a, A2)
            out['v1ctrl'] += cc.get(('L', 0), 0) != cc2.get(('L', 0), 0)
            if not A2 and not B2:
                e = sum(c.values()); L2 = e - c.get(('L3',), 0) - L1
                out['v2'] += 1; out['v2bad'] += L2 != sum(c.values()) - 2 * c.get(('L3',), 0)
            if iv is not None and shape(iv[a], iv[a2]) == 'CONT_IN' and len(A) == 2 and not B:
                Z = [z for z in range(n) if iv[a][1] < iv[z][0] <= iv[a2][1]]
                ok = c.get(('L', 1), 0) <= L1 and c.get(('L', 2), 0) <= L1
                if sorted(Z) == sorted(A): out['v3'] += 1; out['v3bad'] += not ok
                else: out['v3z'] += 1; out['v3zbad'] += not ok
    return out

def job_iv(iv):
    n = len(iv); LT = [[lt(iv, x, y) for y in range(n)] for x in range(n)]
    return check_poset(n, LT, iv)

def job_rand(args):
    n, seed = args; rnd = random.Random(seed)
    p = rnd.choice((0.2, 0.3, 0.45))
    LT = [[x < y and rnd.random() < p for y in range(n)] for x in range(n)]
    for k in range(n):
        for x in range(n):
            for y in range(n):
                if LT[x][k] and LT[k][y]: LT[x][y] = True
    return check_poset(n, LT)

def add(tot, o):
    for k, v in o.items(): tot[k] = tot.get(k, 0) + v

if __name__ == '__main__':
    NN = int(sys.argv[1])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in range(3, NN + 1):
            tot = {}
            for o in pool.map(job_iv, list(gen_fast(n)), chunksize=64): add(tot, o)
            print(f"interval orders n={n}: {tot}"); sys.stdout.flush()
        tot = {}
        for o in pool.map(job_rand, [(5 + i % 4, i) for i in range(3000)], chunksize=16): add(tot, o)
        print(f"random general posets n=5..8 (3000): {tot}")
