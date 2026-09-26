"""enlarge.py (mg-561a): how far outside X = {a,a'} u S must a two-separator lemma look?

For each two-separator ordered pair (a,a'), test local counterexample-compatibility (LCC, see localcc.py)
on nested enlargements of X:
  X0 = {a,a'} u S
  XY = X0 u Y,   Y = {y : y || a and y || a'}  (the only elements that can sit between a and a' in Lambda_1)
  XN = X0 u Y u {elements incomparable to some separator}
  XALL = all elements
LCC on XALL would be a counterexample to 1/3-2/3 (known false for n <= 14), so the XALL column must be 0:
that is the sanity control; X0 > 0 is the positive control (localcc.py).
Also records, for LCC-on-X0 configurations, whether |Lambda_1| = |Lambda_3| (swap is a bijection).
usage: python3 enlarge.py N"""
import sys, os
from multiprocessing import Pool
from t2lib import *

def lcc(iv, Pr, a, a2, X):
    if not Pr(a, a2) > F(2, 3): return False
    for i in X:
        for j in X:
            if i < j and inc(iv, i, j) and bal(Pr(i, j)): return False
    for x in X:
        if x in (a, a2): continue
        ax = lt(iv, a, x) or (inc(iv, a, x) and Pr(a, x) > F(2, 3))
        xa2 = lt(iv, x, a2) or (inc(iv, x, a2) and Pr(x, a2) > F(2, 3))
        if ax and xa2: return False
    return True

def work(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    Pr = lambda x, y: F(N[x][y], e)
    res = []
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2): continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2: continue
            t = 'A' * len(A) + 'B' * len(B)
            X0 = set([a, a2] + A + B)
            Y = {y for y in range(n) if inc(iv, y, a) and inc(iv, y, a2)}
            XY = X0 | Y
            XN = XY | {y for y in range(n) for z in A + B if inc(iv, y, z)}
            XALL = set(range(n))
            row = [t] + [lcc(iv, Pr, a, a2, X) for X in (X0, XY, XN, XALL)]
            if row[1]:
                l1, l2, l3 = lambdas(dn, a, a2, A + B)
                row.append(l1 == l3)
                row.append((iv, iv[a], iv[a2], [iv[z] for z in A], [iv[z] for z in B], [iv[y] for y in Y]) if row[2] else None)
            res.append(row)
    return res

if __name__ == '__main__':
    NN = int(sys.argv[1])
    for n in range(4, NN + 1):
        with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
            out = pool.map(work, list(gen_fast(n)), chunksize=64)
        cnt = {}; bij = {}; ex = {}
        for rs in out:
            for r in rs:
                c = cnt.setdefault(r[0], [0, 0, 0, 0, 0])
                c[0] += 1
                for k in range(4): c[k + 1] += r[k + 1]
                if r[1]:
                    bij.setdefault(r[0], [0, 0])[0] += 1; bij[r[0]][1] += r[5]
                    if r[6]: ex.setdefault(r[0], []).append(r[6])
        print(f"n={n}: type: total / LCC on X0 / XY / XN / XALL ;  |L1|=|L3| among LCC-X0")
        for t in sorted(cnt):
            print(f"   {t}: {cnt[t]}   bijective {bij.get(t, [0, 0])[1]}/{bij.get(t, [0, 0])[0]}")
        for t in sorted(ex):
            for x in ex[t][:2]:
                print(f"   XY-survivor {t}: P={x[0]} a={x[1]} a'={x[2]} above={x[3]} below={x[4]} Y={x[5]}")
        sys.stdout.flush()
