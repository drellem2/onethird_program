"""contprobe.py (mg-561a): the CONTAINMENT two-separator pairs.  a' strictly contains a, a before a',
S(a,a') = {s,t} = the two minimal elements of Z = {z : r(a) < l(z) <= r(a')} (Prop 3.1; no below-separators).
Which counterexample constraint breaks?  For each such pair with P[a<a'] > 2/3 record
  q = P[a'<a], u_s = P[s<a'], u_t = P[t<a'], w = P[t<s] (s = the 2/3-earlier of the two), L2 = P(Lambda_2),
and the 'slack' min(1/3-u_s, 1/3-u_t, |w-1/2|-1/6): LCC <=> slack > 0.  Prints the configurations with the
largest slack, and tests candidate inequalities over ALL containment two-separator pairs (no p>2/3 filter):
  C1: max(u_s,u_t) >= q          C2: u_s + u_t >= 1 - 2q + ... (i.e. union bound; always true, control)
  C3: max(u_s,u_t) >= 1/3 whenever q < 1/3       C4: max(u_s, u_t) >= 2q
usage: python3 contprobe.py N"""
import sys, os
from multiprocessing import Pool
from t2lib import *
from shape import shape

def work(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    Pr = lambda x, y: F(N[x][y], e)
    res = []
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2) or shape(iv[a], iv[a2]) != 'CONT_IN': continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2: continue
            assert not B
            s, t = A
            if Pr(s, t) < F(1, 2): s, t = t, s
            q = Pr(a2, a); us = Pr(s, a2); ut = Pr(t, a2); w = Pr(t, s)
            l1, l2, l3 = lambdas(dn, a, a2, A)
            res.append(dict(iv=iv, a=iv[a], a2=iv[a2], s=iv[s], t=iv[t], q=q, us=us, ut=ut, w=w, L2=F(l2, e),
                            slack=min(F(1, 3) - us, F(1, 3) - ut, abs(w - F(1, 2)) - F(1, 6)), p=1 - q))
    return res

if __name__ == '__main__':
    NN = int(sys.argv[1])
    for n in range(5, NN + 1):
        with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
            out = [r for rs in pool.map(work, list(gen_fast(n)), chunksize=64) for r in rs]
        big = [r for r in out if r['p'] > F(2, 3)]
        c1 = sum(max(r['us'], r['ut']) < r['q'] for r in out)
        c4 = sum(max(r['us'], r['ut']) < 2 * r['q'] for r in out)
        c3 = sum(r['q'] < F(1, 3) and max(r['us'], r['ut']) < F(1, 3) for r in out)
        c5 = sum(r['q'] < F(1, 3) and max(r['us'], r['ut']) < F(1, 3) and not bal(r['w']) for r in out)
        print(f"n={n}: containment 2-sep pairs {len(out)}, with P[a<a']>2/3: {len(big)}; "
              f"fail C1 {c1}, C4 {c4}, C3 {c3}, C3+(s,t unbalanced) {c5}")
        big.sort(key=lambda r: -r['slack'])
        for r in big[:4]:
            print(f"   slack {float(r['slack']):+.4f}  P={r['iv']} a={r['a']} a'={r['a2']} s={r['s']} t={r['t']}  "
                  f"q={float(r['q']):.4f} u_s={float(r['us']):.4f} u_t={float(r['ut']):.4f} P[t<s]={float(r['w']):.4f} L2={float(r['L2']):.4f}")
        sys.stdout.flush()
