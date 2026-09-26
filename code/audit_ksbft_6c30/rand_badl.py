"""rand_badl.py (audit mg-6c30): the Cor 3.2 certificate pipeline (all dominance-respecting K-bad L, then
Thm 3.1 / 2.1* / 3.1* kills) on (i) uniformly random interval multisets n = 11..14 and (ii) this audit's own
staircase construction (path [1,1],[1,2],...,[h-1,h],[h,h] plus 1..3 random long intervals of length >= 3),
built independently of kprime.staircase_family().  A counterexample SEARCH for the scope of Thm 3.1, not a census.
usage: python3 rand_badl.py SEED NRAND NSTAIR"""
import sys, os, random
from multiprocessing import Pool
from eng import Poset
from badl import all_bad, kills, fmt

def rand_iv(rnd):
    n = rnd.randint(11, 14); h = rnd.randint(5, 10); iv = []
    for _ in range(n):
        l = rnd.randint(1, h); iv.append((l, min(h, l + int(rnd.expovariate(0.7)))))
    return tuple(sorted(iv))

def stair_iv(rnd):
    h = rnd.randint(6, 10)
    iv = [(1, 1)] + [(i, i + 1) for i in range(1, h)] + [(h, h)]
    for _ in range(rnd.randint(1, 3)):
        l = rnd.randint(1, h - 3); r = rnd.randint(l + 3, h); iv.append((l, r))
    return tuple(sorted(iv))

def job(arg):
    kind, seed = arg; rnd = random.Random(seed)
    iv = rand_iv(rnd) if kind == 'rand' else stair_iv(rnd)
    P = Poset.from_iv(iv)
    Ls = all_bad(P, cap=5000)
    res = []
    for L in Ls:
        ks = kills(P, L)
        res.append(next((k for k in ('TS', '2.1*', '3.1*') if k in ks), 'SURVIVES'))
    surv = [L for L, r in zip(Ls, res) if r == 'SURVIVES']
    return kind, iv, res, (surv[0] if surv else None)

if __name__ == '__main__':
    seed, nr, ns = map(int, sys.argv[1:4])
    jobs = [('rand', seed * 10**6 + i) for i in range(nr)] + [('stair', seed * 10**6 + 500000 + i) for i in range(ns)]
    agg = {}; seen = set(); ex = []
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for kind, iv, res, s in pool.imap_unordered(job, jobs, chunksize=4):
            key = (kind, iv)
            if key in seen: continue
            seen.add(key)
            d = agg.setdefault(kind, {'posets': 0, 'with_bad': 0, 'badL': 0, 'kill': {}, 'surv_posets': 0})
            d['posets'] += 1; d['with_bad'] += bool(res); d['badL'] += len(res)
            for r in res: d['kill'][r] = d['kill'].get(r, 0) + 1
            if s is not None:
                d['surv_posets'] += 1
                if len(ex) < 6: ex.append((kind, iv, s))
    for k, d in sorted(agg.items()): print(k, d)
    for kind, iv, L in sorted(ex, key=lambda t: len(t[1])):
        print(f"  {kind} SURVIVOR n={len(iv)} P = {fmt(iv)}\n{'':20s}L = {fmt(iv, L)}")
