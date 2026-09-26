"""tiefam.py (mg-561a): the local Lemma C boundary.  csearch.py finds slack exactly 0 at n = 11:
  T11 = [1,1]^2 [1,2] [2,4] [3,3] [3,5]^2 [4,4] [4,5] [5,5]^2, a=[3,3], a'=[2,4], s=[4,4], t=[4,5],
  P[a<a'] = 2/3, P[s<a'] = 1/3, P[t<a'] = 1/5, P[s<t] = 43/60 (exact).
Probe: vary the multiplicities (1..3) of every interval type of T11 except s and t (duplicating s or t
changes |S|), n <= NMAX, and report the best slack of the containment pair (a',a) (first copy of each).
slack > 0 would be an exact local counterexample to Lemma C.
usage: python3 tiefam.py NMAX"""
import sys, os, itertools
from multiprocessing import Pool
from t2lib import *

TYPES = [(1, 1), (1, 2), (2, 4), (3, 3), (3, 5), (5, 5)]

def job(mult):
    iv = sorted([t for t, m in zip(TYPES, mult) for _ in range(m)] + [(4, 4), (4, 5)])
    n = len(iv); dn = downmasks(iv); e, N = laws(dn)
    Pr = lambda x, y: F(N[x][y], e)
    a, a2, s, t = iv.index((3, 3)), iv.index((2, 4)), iv.index((4, 4)), iv.index((4, 5))
    sl = min(F(1, 3) - Pr(s, a2), F(1, 3) - Pr(t, a2), abs(Pr(s, t) - F(1, 2)) - F(1, 6), Pr(a, a2) - F(2, 3))
    return sl, mult, (Pr(a, a2), Pr(s, a2), Pr(t, a2), Pr(s, t))

if __name__ == '__main__':
    NMAX = int(sys.argv[1])
    pop = [m for m in itertools.product((1, 2, 3), repeat=len(TYPES)) if sum(m) + 2 <= NMAX]
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        out = pool.map(job, pop, chunksize=4)
    out.sort(key=lambda r: -r[0])
    print(f"{len(pop)} multiplicity vectors, n <= {NMAX}; slack > 0: {sum(r[0] > 0 for r in out)}; slack = 0: {sum(r[0] == 0 for r in out)}")
    for sl, m, v in out[:8]:
        print(f"  slack {float(sl):+.5f}  mult {dict(zip(TYPES, m))}  P[a<a'],P[s<a'],P[t<a'],P[s<t] = {[str(x) for x in v]}")
