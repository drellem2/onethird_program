"""kts.py (mg-561a): the TWO-STEP lemma (Thm 3.1 of the doc) as a combinatorial rule on L.

Thm 3.1 (PROVEN, any poset).  In a counterexample with 2/3-order L, let a < c < b be L-consecutive with
a || c and c || b.  With A(x,y) = {z : x covered by z, z || y}, B(x,y) = {w : w covered by y, w || x},
    k(a,c,b) = |A(a,c) - A(b,c)| + |B(a,c)| + |B(c,b) - B(c,a)| + |A(c,b)|  >=  3.
(Each counted separator is an L-inversion event of probability < 1/3; the cancelled ones are absorbed by the
reverse terms Lambda_2(b,c), Lambda_2(c,a) of the Swap Identity; the two identities sum to 2-2q1-2q2 > 2/3.)
Rules (forbidden patterns in a putative counterexample's L; L must respect dominance):
  K  : consecutive incomparable step with |S| <= 1                      (Thm 2.1)
  TS : K + consecutive incomparable triple with k <= 2                  (Thm 3.1)
Populations: interval orders n <= N (census), the audit's staircase family (n = 10..13), and random
general posets n = 7..11 (does the interval-order reduction extend?).  Every TS-bad L is printed.
CONTROL: TS must not forbid anything K allows on semiorders' canonical L... (not needed: TS is a theorem);
the positive control is that K alone reproduces 0/2/24 at n = 8/9/10.
usage: python3 kts.py N NRANDOM"""
import sys, os, random
from multiprocessing import Pool
from t2lib import *

def rel_tables(n, LT, dom_pred):
    INC = [[x != y and not LT[x][y] and not LT[y][x] for y in range(n)] for x in range(n)]
    COV = [[LT[x][y] and not any(LT[x][c] and LT[c][y] for c in range(n)) for y in range(n)] for x in range(n)]
    A = lambda x, y: frozenset(z for z in range(n) if COV[x][z] and INC[z][y])
    B = lambda x, y: frozenset(w for w in range(n) if COV[w][y] and INC[w][x])
    NS = {(x, y): len(A(x, y)) + len(B(x, y)) for x in range(n) for y in range(n) if INC[x][y]}
    def k(a, c, b):
        return len(A(a, c) - A(b, c)) + len(B(a, c)) + len(B(c, b) - B(c, a)) + len(A(c, b))
    need = [sum(1 << w for w in range(n) if LT[w][v] or dom_pred(w, v)) for v in range(n)]
    return INC, NS, k, need

def search(n, LT, INC, NS, k, need, rule):
    """DFS with memo over (ideal, last, second-last) for an L avoiding the rule's forbidden patterns."""
    seen = set(); kc = {}
    def K(a, c, b):
        key = (a, c, b)
        if key not in kc: kc[key] = k(a, c, b)
        return kc[key]
    def rec(I, p2, p1, pre):
        if len(pre) == n: return pre
        key = (I, p2, p1)
        if key in seen: return None
        for v in range(n):
            if I >> v & 1 or need[v] & ~I: continue
            if p1 >= 0 and INC[p1][v] and NS[(p1, v)] <= 1: continue
            if rule == 'TS' and p2 >= 0 and INC[p2][p1] and INC[p1][v] and K(p2, p1, v) <= 2: continue
            r = rec(I | 1 << v, p1, v, pre + [v])
            if r: return r
        seen.add(key); return None
    return rec(0, -1, -1, [])

def job_iv(iv):
    n = len(iv)
    if all(not inc(iv, a, b) for a in range(n) for b in range(n)): return None
    LT = [[lt(iv, x, y) for y in range(n)] for x in range(n)]
    dom = lambda w, v: inc(iv, w, v) and iv[w] != iv[v] and iv[w][0] <= iv[v][0] and iv[w][1] <= iv[v][1]
    INC, NS, k, need = rel_tables(n, LT, dom)
    rK = search(n, LT, INC, NS, k, need, 'K')
    if rK is None: return (iv, None, None)
    rT = search(n, LT, INC, NS, k, need, 'TS')
    return (iv, rK, None if rT is None else [iv[v] for v in rT])

def job_gen(seed):
    rnd = random.Random(seed); n = 7 + seed % 5; p = rnd.choice((0.15, 0.25, 0.35))
    LT = [[x < y and rnd.random() < p for y in range(n)] for x in range(n)]
    for c in range(n):
        for x in range(n):
            if LT[x][c]:
                for y in range(n):
                    if LT[c][y]: LT[x][y] = True
    if all(LT[x][y] or LT[y][x] for x in range(n) for y in range(n) if x != y): return None
    dn = [frozenset(w for w in range(n) if LT[w][v]) for v in range(n)]
    up = [frozenset(w for w in range(n) if LT[v][w]) for v in range(n)]
    INCt = lambda x, y: x != y and not LT[x][y] and not LT[y][x]
    dom = lambda w, v: INCt(w, v) and dn[w] <= dn[v] and up[w] >= up[v] and not (dn[w] == dn[v] and up[w] == up[v])
    INC, NS, k, need = rel_tables(n, LT, dom)
    rK = search(n, LT, INC, NS, k, need, 'K')
    if rK is None: return (seed, None, None)
    rT = search(n, LT, INC, NS, k, need, 'TS')
    return (seed, rK, rT, n, [(x, y) for x in range(n) for y in range(n) if LT[x][y]])

if __name__ == '__main__':
    import kprime
    NN = int(sys.argv[1]); NR = int(sys.argv[2])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        pops = [(f"census n={n}", list(gen_fast(n))) for n in range(4, NN + 1)]
        pops.append(("staircase + 1..3 long, n=10..13", list(kprime.staircase_family())))
        for name, pop in pops:
            R = [r for r in pool.map(job_iv, pop, chunksize=64) if r]
            nk = sum(1 for r in R if r[1]); nt = [r for r in R if r[2]]
            print(f"{name}: {len(R)} non-chain; K-bad {nk}; TS-bad {len(nt)}")
            for iv, _, L in nt[:5]: print(f"   TS-bad P={iv} L={L}")
            sys.stdout.flush()
        R = [r for r in pool.map(job_gen, range(NR), chunksize=32) if r]
        nk = sum(1 for r in R if r[1]); nt = [r for r in R if r[2]]
        print(f"random general posets n=7..11: {len(R)} non-chain; K-bad {nk}; TS-bad {len(nt)}")
        for r in nt[:3]: print(f"   TS-bad n={r[3]} rel={r[4]} L={r[2]}")
