"""localcc.py (mg-561a): is there a purely LOCAL two-separator lemma?

For every interval order with n <= N and every ordered incomparable pair (a,a') with EXACTLY two
separators S = {s,t}, let X = {a,a'} u S.  Call the configuration LOCALLY COUNTEREXAMPLE-COMPATIBLE (LCC) if
  (i)   every incomparable pair inside X has law outside [1/3,2/3];
  (ii)  P[a<a'] > 2/3;
  (iii) no element of X lies strictly between a and a' in the 2/3-order (the order is automatically
        transitive on X, Thm 2.1(a) argument).
These are exactly the constraints a counterexample's L imposes on X.  If an LCC configuration occurs in
a real poset, NO inequality among the pair laws of X (nor the Lambda-counts, which are computed too) can
turn an L-consecutive two-separator pair into a contradiction: the lemma must look outside X.
Types: AA (two above-separators), AB (one each), BB.  Also reports the Brightwell margin
P(L2) - (2P[a<a'] - 1) >= 0 (Thm 2.1(b)) as a control: it must never be negative.
usage: python3 localcc.py N"""
import sys, os
from multiprocessing import Pool
from t2lib import *

def typ(A, B): return 'A' * len(A) + 'B' * len(B)

def work(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    Pr = lambda x, y: F(N[x][y], e)
    res = []
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2): continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2: continue
            X = [a, a2] + A + B
            p = Pr(a, a2)
            rec = {'type': typ(A, B), 'p': p}
            ok = p > F(2, 3)
            if ok:
                for i in X:
                    for j in X:
                        if i < j and inc(iv, i, j) and bal(Pr(i, j)): ok = False
            if ok:
                for x in X:
                    if x in (a, a2): continue
                    ax = 1 if lt(iv, a, x) else (Pr(a, x) > F(2, 3) if inc(iv, a, x) else 0)
                    xa2 = 1 if lt(iv, x, a2) else (Pr(x, a2) > F(2, 3) if inc(iv, x, a2) else 0)
                    if ax and xa2: ok = False
            rec['lcc'] = ok
            if ok:
                l1, l2, l3 = lambdas(dn, a, a2, A + B)
                rec.update(iv=iv, a=iv[a], a2=iv[a2], A=[iv[z] for z in A], B=[iv[z] for z in B],
                           L=(l1, l2, l3, e), marg={(iv[i], iv[j]): Pr(i, j) for i in X for j in X if inc(iv, i, j)})
            res.append(rec)
    return res

if __name__ == '__main__':
    NN = int(sys.argv[1])
    for n in range(4, NN + 1):
        with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
            out = pool.map(work, list(gen_fast(n)), chunksize=64)
        tot = {}; lcc = {}; ex = {}
        for rs in out:
            for r in rs:
                tot[r['type']] = tot.get(r['type'], 0) + 1
                if r['lcc']:
                    lcc[r['type']] = lcc.get(r['type'], 0) + 1
                    ex.setdefault(r['type'], []).append(r)
        print(f"n={n}: two-separator ordered pairs by type {dict(sorted(tot.items()))}; LCC {dict(sorted(lcc.items()))}")
        for t, rs in sorted(ex.items()):
            posets = {tuple(r['iv']) for r in rs}
            print(f"   LCC type {t}: {len(rs)} configurations in {len(posets)} posets")
            rs.sort(key=lambda r: -min(min(v, 1 - v) for v in r['marg'].values()))
            for r in rs[:3]:
                l1, l2, l3, e = r['L']
                print(f"     P={r['iv']}  a={r['a']} a'={r['a2']} above={r['A']} below={r['B']}  P[a<a']={float(r['p']):.4f}"
                      f"  L1/L2/L3 = {l1}/{l2}/{l3} of {e}")
                print("        laws in X:", {k: round(float(v), 4) for k, v in r['marg'].items() if k[0] <= k[1]})
        sys.stdout.flush()
