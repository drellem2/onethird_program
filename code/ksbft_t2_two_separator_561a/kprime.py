"""kprime.py (mg-561a): which two-separator lemma would kill every known Brightwell obstruction?

A candidate lemma is encoded as a STEP RULE: the set of L-consecutive incomparable steps (v_i, v_{i+1}) that
it forbids in a counterexample's 2/3-order L.  Thm 2.1 (PROVEN) forbids |S| <= 1.  A rule R 'kills' (P, L)
if L has a forbidden step.  An R-bad L is a dominance-respecting linear extension with no forbidden step.
If R were a theorem and P had no R-bad L, P would satisfy 1/3-2/3 (as Cor 2.2 of mg-afa4).
  K    : forbid |S| <= 1                                   (Claim K; baseline, must reproduce 2 @ n=9, 24 @ n=10)
  KC   : K + forbid CONTAINMENT steps with |S| = 2         (Lemma C)
  KD   : K + forbid DOMINANCE steps with |S| = 2           (control: the dominance half)
  KDab : K + forbid dominance steps of type AB with |S| = 2
  KDaa : K + forbid dominance steps of type AA or BB with |S| = 2
Populations: every interval order with n <= N (census; the populations of mg-afa4) and the audit mg-5ecf
targeted family 'unit staircase + 1..3 long intervals', n = 10..13.
usage: python3 kprime.py N"""
import sys, os, itertools
from multiprocessing import Pool
from t2lib import *
from shape import shape

RULES = ['K', 'KC', 'KD', 'KDab', 'KDaa']

def step_table(iv):
    n = len(iv); C = covers(iv)
    T = {}
    for a in range(n):
        for b in range(n):
            if not inc(iv, a, b): continue
            A, B = seps_typed(iv, C, a, b)
            k = len(A) + len(B); sh = shape(iv[a], iv[b]); t = 'A' * len(A) + 'B' * len(B)
            cont = sh in ('CONT_IN', 'CONT_OUT'); dom = not cont
            T[(a, b)] = {'K': k <= 1,
                         'KC': k <= 1 or (cont and k == 2),
                         'KD': k <= 1 or (dom and k == 2),
                         'KDab': k <= 1 or (dom and k == 2 and t == 'AB'),
                         'KDaa': k <= 1 or (dom and k == 2 and t in ('AA', 'BB'))}
    return T

def bad_L(iv, T, rule):
    n = len(iv)
    need = [0] * n
    for y in range(n):
        for x in range(n):
            if lt(iv, x, y): need[y] |= 1 << x
            elif inc(iv, x, y) and iv[x] != iv[y] and iv[x][0] <= iv[y][0] and iv[x][1] <= iv[y][1]: need[y] |= 1 << x
    layer = {1 << x: {x: None} for x in range(n) if need[x] == 0}
    back = [layer]
    for _ in range(n - 1):
        nxt = {}
        for I, lasts in layer.items():
            for x in range(n):
                if I >> x & 1 or need[x] & ~I: continue
                for a in lasts:
                    if lt(iv, a, x) or not T[(a, x)][rule]:
                        nxt.setdefault(I | 1 << x, {})[x] = (I, a); break
        layer = nxt; back.append(layer)
    full = (1 << n) - 1
    if full not in layer: return None
    x = next(iter(layer[full])); I = full; seq = []
    for k in range(n - 1, -1, -1):
        seq.append(x); par = back[k][I][x]
        if par is None: break
        I, x = par
    return [iv[v] for v in reversed(seq)]

def job(iv):
    n = len(iv)
    if all(not inc(iv, a, b) for a in range(n) for b in range(n)): return None
    T = step_table(iv)
    out = {}
    L = bad_L(iv, T, 'K')
    if L is None: return {r: None for r in RULES}
    out['K'] = L
    for r in RULES[1:]: out[r] = bad_L(iv, T, r)
    return out

def staircase_family():
    for k in range(4, 12):
        stair = [(1, 1)] + [(i, i + 1) for i in range(1, k)] + [(k, k)]
        pts = range(1, k + 1)
        longs = [(a, b) for a in pts for b in pts if b - a >= 2]
        for t in (1, 2, 3):
            if not 10 <= len(stair) + t <= 13: continue
            for extra in itertools.combinations(longs, t):
                yield sorted(stair + list(extra))

def report(name, pop, pool):
    R = [(iv, o) for iv, o in zip(pop, pool.map(job, pop, chunksize=64)) if o]
    cnt = {r: sum(1 for _, o in R if o[r]) for r in RULES}
    print(f"{name}: {len(R)} non-chain posets; posets with an R-bad dominance L: " +
          ", ".join(f"{r} {cnt[r]}" for r in RULES))
    for r in ('KC', 'KDab', 'KDaa'):
        ex = [(iv, o[r]) for iv, o in R if o[r]]
        for iv, L in ex[:2]:
            print(f"   {r}-bad: P={iv}  L={L}")
    sys.stdout.flush()
    return R

if __name__ == '__main__':
    NN = int(sys.argv[1])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in range(4, NN + 1):
            report(f"census n={n}", list(gen_fast(n)), pool)
        report("staircase+1..3 long, n=10..13", list(staircase_family()), pool)
