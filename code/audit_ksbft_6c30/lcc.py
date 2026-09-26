"""lcc.py (audit mg-6c30): independent recount of mg-561a sec.2.1 (locally counterexample-compatible
two-separator configurations), from the doc's definition, with this audit's generator and laws.
Types by separator kind (AA / AB / BB) and shape (DOM: a dominates a'; CONT: strict nesting; OTHER).
Columns: total, P[a<a']>2/3, LCC on X0 = {a,a'} u S, on X0 u Y, on X0 u Y u Inc(S), on all of P.
usage: python3 lcc.py NMAX"""
import sys, os
from fractions import Fraction as Fr
from multiprocessing import Pool
from eng import gen, Poset

def work(iv):
    P = Poset.from_iv(iv); n = P.n; M, e = P.before_counts()
    big = lambda x, y: 3 * M[x][y] > 2 * e             # P[x<y] > 2/3
    bal = lambda x, y: 3 * M[x][y] >= e and 3 * M[x][y] <= 2 * e
    prec = lambda x, y: P.lt[x][y] or (P.inc[x][y] and big(x, y))
    out = []
    for a in range(n):
        for a2 in range(n):
            if not P.inc[a][a2]: continue
            A, B = P.A(a, a2), P.B(a, a2)
            if len(A) + len(B) != 2: continue
            (la, ra), (lb, rb) = iv[a], iv[a2]
            shape = 'DOM' if P.dominates(a, a2) else ('CONT' if (la < lb and rb < ra) or (lb < la and ra < rb) else 'OTHER')
            typ = 'A' * len(A) + 'B' * len(B)
            X0 = {a, a2} | A | B
            Y = {y for y in range(n) if P.inc[y][a] and P.inc[y][a2]}
            XN = X0 | Y | {y for y in range(n) for z in A | B if P.inc[y][z]}
            def lcc(X):
                if not big(a, a2): return False
                if any(P.inc[i][j] and bal(i, j) for i in X for j in X if i < j): return False
                return not any(prec(a, x) and prec(x, a2) for x in X if x not in (a, a2))
            out.append((typ, shape, big(a, a2), lcc(X0), lcc(X0 | Y), lcc(XN), lcc(set(range(n)))))
    return out

if __name__ == '__main__':
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in range(4, int(sys.argv[1]) + 1):
            agg = {}
            for rs in pool.imap_unordered(work, gen(n), chunksize=64):
                for r in rs:
                    c = agg.setdefault(r[:2], [0] * 6); c[0] += 1
                    for k in range(5): c[k + 1] += r[k + 2]
            print(f"n={n}: (type, shape): total / P>2/3 / LCC X0 / X0+Y / X0+Y+Inc(S) / all P")
            for k in sorted(agg): print(f"   {k}: {agg[k]}")
            sys.stdout.flush()
