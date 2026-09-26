"""verify3.py (mg-561a): exact check of the UNCONDITIONAL inequality behind Thm 3.1 (any poset, any a,c,b
with a||c, c||b, a != b):
  (P[a<c]-P[c<a]) + (P[c<b]-P[b<c])
     <= sum_{z in A(a,c)-A(b,c)} P[z<c] + sum_{w in B(a,c)} P[a<w] + sum_{w in B(c,b)-B(c,a)} P[c<w] + sum_{z in A(c,b)} P[z<b]
(Thm 3.1 is this inequality plus 'each counted event is an L-inversion, of probability < 1/3').
Also the one-pair form (Thm 2.1(b) via the Swap Identity): 2P[a<a']-1 <= sum over S(a,a') of the events.
CONTROL (must fail somewhere): over-cancel, i.e. drop the whole A(a,c) sum (as if every above-separator
of (a,c) were absorbed by Lambda_2(b,c)).
Populations: all interval orders n <= N; 2000 random general posets n = 5..8.
usage: python3 verify3.py N"""
import sys, os, random
from multiprocessing import Pool
from fractions import Fraction as F
from t2lib import *

def check(n, LT):
    dn = [sum(1 << w for w in range(n) if LT[w][v]) for v in range(n)]
    e, N = laws(dn)
    P = lambda x, y: F(1) if LT[x][y] else (F(0) if LT[y][x] else F(N[x][y], e))
    inc_ = lambda x, y: x != y and not LT[x][y] and not LT[y][x]
    cov = lambda x, y: LT[x][y] and not any(LT[x][c] and LT[c][y] for c in range(n))
    A = lambda x, y: {z for z in range(n) if cov(x, z) and inc_(z, y)}
    B = lambda x, y: {w for w in range(n) if cov(w, y) and inc_(w, x)}
    bad = ctrl = tested = 0; worst = None
    for a in range(n):
        for c in range(n):
            if not inc_(a, c): continue
            for b in range(n):
                if b == a or not inc_(c, b): continue
                lhs = (2 * P(a, c) - 1) + (2 * P(c, b) - 1)
                rhs = sum(P(z, c) for z in A(a, c) - A(b, c)) + sum(P(a, w) for w in B(a, c)) + \
                      sum(P(c, w) for w in B(c, b) - B(c, a)) + sum(P(z, b) for z in A(c, b))
                rc = sum(P(a, w) for w in B(a, c)) + sum(P(c, w) for w in B(c, b) - B(c, a)) + sum(P(z, b) for z in A(c, b))
                tested += 1; bad += lhs > rhs; ctrl += lhs > rc
                if worst is None or rhs - lhs < worst: worst = rhs - lhs
    return tested, bad, ctrl, worst

def job_iv(iv):
    n = len(iv); return check(n, [[lt(iv, x, y) for y in range(n)] for x in range(n)])

def job_rand(seed):
    rnd = random.Random(seed); n = 5 + seed % 4; p = rnd.choice((0.2, 0.3, 0.45))
    LT = [[x < y and rnd.random() < p for y in range(n)] for x in range(n)]
    for k in range(n):
        for x in range(n):
            if LT[x][k]:
                for y in range(n):
                    if LT[k][y]: LT[x][y] = True
    return check(n, LT)

def summ(name, out):
    t = sum(o[0] for o in out); b = sum(o[1] for o in out); c = sum(o[2] for o in out)
    w = min((o[3] for o in out if o[3] is not None), default=None)
    print(f"{name}: triples {t}; Thm 3.1 inequality violations {b}; CONTROL (over-cancellation) violations {c}; "
          f"min slack {w}"); sys.stdout.flush()

if __name__ == '__main__':
    NN = int(sys.argv[1])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in range(3, NN + 1):
            summ(f"interval orders n={n}", pool.map(job_iv, list(gen_fast(n)), chunksize=64))
        summ("random general posets n=5..8 (2000)", pool.map(job_rand, range(2000), chunksize=16))
