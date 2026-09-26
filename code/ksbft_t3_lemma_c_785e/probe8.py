"""probe8.py (mg-785e): the joint law of X = (a, a', s, t) at containment two-separator pairs.
For every such pair of every interval order with n <= N: record q = P[a'<a], u_s, u_t, w = P[t<s] (s = the
more-likely-first of the two), and the 8 ordering probabilities of X.  Prints the pairs with q, u_s, u_t < 1/3
(the region a counterexample needs), with their w.  usage: python3 probe8.py N"""
import sys, os
from multiprocessing import Pool
from t3lib import *

def work(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    out = []
    for a, a2, s, t, Z in cont_pairs(iv, C):
        if N[s][t] < N[t][s]: s, t = t, s
        law = order_law(dn, (a, a2, s, t))
        P = lambda f: F(sum(c for o, c in law.items() if f(o)), e)
        ix = lambda o, x: o.index(x)
        q = P(lambda o: ix(o, a2) < ix(o, a)); us = P(lambda o: ix(o, s) < ix(o, a2)); ut = P(lambda o: ix(o, t) < ix(o, a2))
        w = P(lambda o: ix(o, t) < ix(o, s))
        if q < F(1, 3) and us < F(1, 3) and ut < F(1, 3):
            out.append((iv, iv[a], iv[a2], iv[s], iv[t], len(Z), q, us, ut, w))
    return out

if __name__ == '__main__':
    NN = int(sys.argv[1])
    for n in range(5, NN + 1):
        with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
            out = [r for rs in pool.map(work, list(gen_fast(n)), chunksize=64) for r in rs]
        print(f"n={n}: containment 2-sep pairs with q,u_s,u_t < 1/3: {len(out)}; max w = P[t<s] among them: "
              f"{max((r[-1] for r in out), default=None)}")
        nt = [r for r in out if r[3] != r[4]]
        print(f"   twins s=t: {len(out)-len(nt)}; non-twin: {len(nt)}; min w over non-twin: {min((r[-1] for r in nt), default=None)}")
        for r in sorted(nt, key=lambda r: r[-1])[:12]:
            print("   ", r[0], "a", r[1], "a'", r[2], "s", r[3], "t", r[4], "|Z|", r[5], "q,us,ut,w =", *[f"{float(x):.4f}" for x in r[6:]])
        sys.stdout.flush()
