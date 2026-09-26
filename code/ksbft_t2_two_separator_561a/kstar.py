"""kstar.py (mg-561a): the NON-LOCAL forms of Thm 2.1 and Thm 3.1 (both PROVEN; the proofs never use
consecutiveness except to make the counted events L-inversions).

  (2.1*) a <_L a' incomparable, and every separator z of (a,a') is L-OUTSIDE (above-separator after a',
         below-separator before a)  =>  |S(a,a')| >= 2.
  (3.1*) a <_L c <_L b with a||c, c||b, and every REST event of Thm 3.1 an L-inversion
         (z in A(a,c)-A(b,c): z after c;  w in B(a,c): w before a;  w in B(c,b)-B(c,a): w before c;
          z in A(c,b): z after b)  =>  #rest >= 3.
Procedure: enumerate ALL dominance-respecting K-bad L of each poset in the population (every
L-consecutive incomparable step has |S| >= 2), and classify each L as killed by TS (consecutive
Thm 3.1), by 2.1*, by 3.1*, or surviving everything.
Populations: every poset with a K-bad L in the census n <= 10 (found by kprime.py) and the staircase family.
usage: python3 kstar.py N"""
import sys, os
from multiprocessing import Pool
from t2lib import *
import kprime

def tables(iv):
    n = len(iv); C = covers(iv)
    A = {}; B = {}
    for x in range(n):
        for y in range(n):
            if inc(iv, x, y):
                A[(x, y)] = frozenset(z for z in range(n) if (x, z) in C and inc(iv, z, y))
                B[(x, y)] = frozenset(w for w in range(n) if (w, y) in C and inc(iv, w, x))
    need = [0] * n
    for y in range(n):
        for x in range(n):
            if lt(iv, x, y) or (inc(iv, x, y) and iv[x] != iv[y] and iv[x][0] <= iv[y][0] and iv[x][1] <= iv[y][1]):
                need[y] |= 1 << x
    return A, B, need

def all_bad(iv, A, B, need, cap=20000):
    n = len(iv); out = []
    def rec(I, pre):
        if len(out) >= cap: return
        if len(pre) == n: out.append(list(pre)); return
        for v in range(n):
            if I >> v & 1 or need[v] & ~I: continue
            if pre and inc(iv, pre[-1], v) and len(A[(pre[-1], v)]) + len(B[(pre[-1], v)]) <= 1: continue
            pre.append(v); rec(I | 1 << v, pre); pre.pop()
    rec(0, [])
    return out

def classify(iv, L, A, B):
    n = len(iv); pos = {v: i for i, v in enumerate(L)}
    I = [(x, y) for x in range(n) for y in range(n) if inc(iv, x, y) and pos[x] < pos[y]]
    Iset = set(I)
    def ts(a, c, b):
        return (len(A[(a, c)] - A[(b, c)]) + len(B[(a, c)]) + len(B[(c, b)] - B[(c, a)]) + len(A[(c, b)])) <= 2
    for i in range(n - 2):
        a, c, b = L[i], L[i + 1], L[i + 2]
        if inc(iv, a, c) and inc(iv, c, b) and ts(a, c, b): return 'TS'
    for a, a2 in I:
        if all(pos[z] > pos[a2] for z in A[(a, a2)]) and all(pos[w] < pos[a] for w in B[(a, a2)]) \
                and len(A[(a, a2)]) + len(B[(a, a2)]) <= 1: return '2.1*'
    for (a, c) in I:
        for b in range(n):
            if (c, b) not in Iset: continue
            rest = [(z, 'after', c) for z in A[(a, c)] - A[(b, c)]] + [(w, 'before', a) for w in B[(a, c)]] + \
                   [(w, 'before', c) for w in B[(c, b)] - B[(c, a)]] + [(z, 'after', b) for z in A[(c, b)]]
            if len(rest) <= 2 and all((pos[z] > pos[r]) if d == 'after' else (pos[z] < pos[r]) for z, d, r in rest):
                return '3.1*'
    return 'SURVIVES'

def job(iv):
    A, B, need = tables(iv)
    Ls = all_bad(iv, A, B, need)
    cnt = {}; surv = []
    for L in Ls:
        c = classify(iv, L, A, B); cnt[c] = cnt.get(c, 0) + 1
        if c == 'SURVIVES': surv.append([iv[v] for v in L])
    return iv, len(Ls), cnt, surv[:2]

if __name__ == '__main__':
    NN = int(sys.argv[1])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        pops = []
        for n in range(9, NN + 1):
            R = pool.map(kprime.job, list(gen_fast(n)), chunksize=64)
            pops.append((f"census n={n} (posets with a K-bad dominance L)",
                         [iv for iv, o in zip(gen_fast(n), R) if o and o['K']]))
        fam = list(kprime.staircase_family())
        R = pool.map(kprime.job, fam, chunksize=64)
        pops.append(("staircase + 1..3 long, n=10..13 (posets with a K-bad L)", [iv for iv, o in zip(fam, R) if o and o['K']]))
        for name, pop in pops:
            out = pool.map(job, pop, chunksize=1)
            tot = {}; nL = 0; sp = []
            for iv, k, cnt, surv in out:
                nL += k
                for c, v in cnt.items(): tot[c] = tot.get(c, 0) + v
                if surv: sp.append((iv, surv))
            print(f"{name}: {len(pop)} posets, {nL} K-bad dominance L; killed by {dict(sorted(tot.items()))}; "
                  f"posets with a surviving L: {len(sp)}")
            for iv, surv in sp[:4]: print(f"   SURVIVOR P={iv}\n            L={surv[0]}")
            sys.stdout.flush()
