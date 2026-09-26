"""shape.py (mg-561a): split two-separator ordered pairs (a,a') by the SHAPE of the pair:
  DOM  : a dominates a' (l(a)<=l(a'), r(a)<=r(a'), not twins)   -- the orientation a counterexample's L uses;
  RDOM : a' dominates a (reverse; impossible in a counterexample's L by Zaguia Lemma 7);
  CONT_OUT : a strictly contains a';   CONT_IN : a' strictly contains a;   TWIN: equal intervals.
and report LCC-on-X0 counts per (type, shape), plus whether |L1|=|L3| holds.
usage: python3 shape.py N"""
import sys, os
from multiprocessing import Pool
from t2lib import *
from enlarge import lcc

def shape(x, y):
    (lx, rx), (ly, ry) = x, y
    if x == y: return 'TWIN'
    if lx <= ly and rx <= ry: return 'DOM'
    if ly <= lx and ry <= rx: return 'RDOM'
    if lx < ly: return 'CONT_OUT'
    return 'CONT_IN'

def work(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    Pr = lambda x, y: F(N[x][y], e)
    res = []
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2): continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2: continue
            X0 = set([a, a2] + A + B)
            ok = lcc(iv, Pr, a, a2, X0)
            eq = None
            if ok:
                l1, l2, l3 = lambdas(dn, a, a2, A + B); eq = (l1 == l3)
            res.append(('A' * len(A) + 'B' * len(B), shape(iv[a], iv[a2]), ok, eq, Pr(a, a2) > F(2, 3)))
    return res

if __name__ == '__main__':
    NN = int(sys.argv[1])
    for n in range(4, NN + 1):
        with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
            out = pool.map(work, list(gen_fast(n)), chunksize=64)
        cnt = {}
        for rs in out:
            for t, sh, ok, eq, big in rs:
                c = cnt.setdefault((t, sh), [0, 0, 0, 0])
                c[0] += 1; c[1] += big; c[2] += ok; c[3] += bool(eq)
        print(f"n={n}: (type, shape): total / P[a<a']>2/3 / LCC-X0 / LCC with |L1|=|L3|")
        for k in sorted(cnt): print(f"   {k}: {cnt[k]}")
        sys.stdout.flush()
