"""csearch.py (mg-561a): targeted counterexample search for the LOCAL form of Lemma C.

Local Lemma C (candidate): if a' strictly contains a and S(a,a') = {s,t}, then NOT all of
  P[a<a'] > 2/3,  P[s<a'] < 1/3,  P[t<a'] < 1/3,  P[s<t] outside [1/3,2/3].
It holds on every interval order with n <= 9 (contprobe.py) with slack -> 0.  This is a hill-climb over
interval orders with n <= NMAX maximising slack = min(1/3-P[s<a'], 1/3-P[t<a'], |P[s<t]-1/2|-1/6,
P[a<a']-2/3) over containment 2-separator pairs; slack > 0 is a local counterexample.  Moves: perturb one
endpoint, add an interval, delete an interval (then canonicalise).  Seeds: the n=9 slack leaders.
usage: python3 csearch.py NMAX ITERS SEED"""
import sys, os, random
from t2lib import *
from shape import shape
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ksbft_t_interval_orders_afa4'))
from iolib import canon

def best_slack(iv):
    n = len(iv); dn = downmasks(iv); e, N = laws(dn); C = covers(iv)
    Pr = lambda x, y: F(N[x][y], e)
    best = None
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2) or shape(iv[a], iv[a2]) != 'CONT_IN': continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2: continue
            s, t = A
            sl = min(F(1, 3) - Pr(s, a2), F(1, 3) - Pr(t, a2), abs(Pr(s, t) - F(1, 2)) - F(1, 6), Pr(a, a2) - F(2, 3))
            if best is None or sl > best[0]: best = (sl, iv[a], iv[a2], iv[s], iv[t])
    return best

def move(iv, nmax):
    iv = list(iv); h = max(r for _, r in iv); k = random.random()
    if k < 0.5:
        i = random.randrange(len(iv)); l, r = iv[i]
        if random.random() < 0.5: l = max(1, min(r, l + random.choice((-1, 1))))
        else: r = max(l, min(h + 1, r + random.choice((-1, 1))))
        iv[i] = (l, r)
    elif k < 0.8 and len(iv) < nmax:
        l = random.randint(1, h + 1); r = random.randint(l, h + 1); iv.append((l, r))
    elif len(iv) > 5:
        iv.pop(random.randrange(len(iv)))
    return canon(iv)

if __name__ == '__main__':
    NMAX, ITERS, SEED = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    random.seed(SEED)
    seeds = [[(1, 1), (1, 1), (1, 2), (2, 4), (3, 3), (3, 5), (4, 4), (4, 5), (5, 5)],
             [(1, 1), (1, 1), (1, 2), (2, 5), (3, 3), (3, 4), (4, 5), (5, 5)],
             [(1, 1), (1, 4), (2, 2), (2, 3), (3, 3), (3, 4), (4, 4)]]
    seeds.append([(1, 1), (1, 1), (1, 2), (2, 4), (3, 3), (3, 5), (3, 5), (4, 4), (4, 5), (5, 5), (5, 5)])  # slack 0 found at seed 3
    cur = seeds[-1] if SEED >= 10 else random.choice(seeds); cb = best_slack(cur); glob = (cb, cur)
    T = 0.02
    for it in range(ITERS):
        nx = move(cur, NMAX)
        b = best_slack(nx)
        if b is None: continue
        if b[0] >= cb[0] or random.random() < pow(2.718, float(b[0] - cb[0]) / T):
            cur, cb = nx, b
            if cb[0] > glob[0][0]:
                glob = (cb, cur)
                print(f"it {it}: slack {float(cb[0]):+.5f} n={len(cur)} P={cur} a={cb[1]} a'={cb[2]} s={cb[3]} t={cb[4]}"); sys.stdout.flush()
        if it % 500 == 0: T = max(0.002, T * 0.9)
    print("BEST", float(glob[0][0]), glob[1], glob[0][1:])
