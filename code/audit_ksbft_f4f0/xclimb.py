"""xclimb.py (audit mg-f4f0): counterexample SEARCH (hill-climb, a probe not a census) for the X-local form of
Lemma C (mg-785e sec 4.1) at n = 11..20: maximise over strict-containment 2-separator pairs
   slack = min(1/3 - q, 1/3 - u_s, 1/3 - u_t, 1/3 - w),  w = min(P[s<t], P[t<s]).
slack > 0 would be an interval order where the step looks locally like a counterexample step with s,t
unbalanced, i.e. the X-local form fails. Also tracks slack0 = min(1/3-q, 1/3-u_s, 1/3-u_t) (region only).
Seeds: the 29 tight n=10 configurations' shape, Q12, T11, random staircases."""
import sys, random, time
from fractions import Fraction as F
from eng import *

TH = F(1, 3)
def score(iv):
    iv = canonical(iv)   # geometric containment is meaningful only in the canonical representation
    R = rel_from_iv(iv); C = covers_rel(R)
    try: cp = list(cont_twosep(iv, R, C))
    except AssertionError: return None
    if not cp: return None
    cnt, e = pair_counts(R); best = None
    for a, a2, s, t in cp:
        q = F(cnt[a2][a], e); us = F(cnt[s][a2], e); ut = F(cnt[t][a2], e); w = min(F(cnt[s][t], e), F(cnt[t][s], e))
        sl0 = min(TH - q, TH - us, TH - ut); sl = min(sl0, TH - w)
        cand = (sl, sl0, (iv[a], iv[a2], iv[s], iv[t]))
        if best is None or cand[:2] > best[:2]: best = cand
    return best

def mutate(iv, rng, nmin, nmax):
    iv = list(iv); r = rng.random(); m = max(x[1] for x in iv)
    if r < 0.45:
        i = rng.randrange(len(iv)); l, rr = iv[i]
        if rng.random() < 0.5: l = max(1, min(rr, l + rng.choice([-1, 1])))
        else: rr = max(l, min(m + 1, rr + rng.choice([-1, 1])))
        iv[i] = (l, rr)
    elif r < 0.7 and len(iv) < nmax: iv.append(iv[rng.randrange(len(iv))])
    elif r < 0.85 and len(iv) < nmax:
        l = rng.randint(1, m); iv.append((l, min(m, l + rng.randint(0, 4))))
    elif len(iv) > nmin: iv.pop(rng.randrange(len(iv)))
    return sorted(iv)

SEEDS = [
    [(1,1),(1,1),(1,1),(1,2),(1,3),(2,6),(3,4),(4,5),(5,6),(6,6),(6,6)],
    [(1,1),(1,2),(2,3),(2,5),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)],
    [(1,1),(1,1),(1,2),(2,4),(3,3),(3,5),(3,5),(4,4),(4,5),(5,5),(5,5)],
    [(1,1),(1,2),(2,6),(3,3),(3,4),(3,4),(4,7),(5,5),(6,6),(7,7),(7,7)],
]
if __name__ == '__main__':
    T = float(sys.argv[1]); rng = random.Random(int(sys.argv[2])); nmin, nmax = (int(sys.argv[3]), int(sys.argv[4])) if len(sys.argv) > 4 else (11, 20)
    t0 = time.time(); glob = None; evals = 0; restarts = 0; pos_found = []
    while time.time() - t0 < T:
        restarts += 1
        cur = list(rng.choice(SEEDS)) if rng.random() < 0.6 else sorted([(i, i+1) for i in range(1, 8)] + [(1,1),(8,8)] + [(lambda l: (l, l + rng.randint(2, 4)))(rng.randint(1, 5)) for _ in range(rng.randint(2, 4))])
        while len(cur) < nmin: cur = mutate(cur, rng, nmin, nmax)
        while len(cur) > nmax: cur.pop(rng.randrange(len(cur)))
        cs = score(cur); stall = 0
        while stall < 300 and time.time() - t0 < T:
            nxt = mutate(cur, rng, nmin, nmax)
            if len(max(nxt, key=lambda x: 0)) and len(nxt) < nmin: continue
            ns = score(nxt); evals += 1
            if ns is None: stall += 1; continue
            if cs is None or ns[:2] >= cs[:2]:
                if cs is None or ns[:2] > cs[:2]: stall = 0
                else: stall += 1
                cur, cs = nxt, ns
                if glob is None or cs[:2] > glob[0][:2]: glob = (cs, list(cur))
                if cs[0] > 0: pos_found.append((cs, list(cur)))
            else: stall += 1
    (sl, sl0, cfg), iv = glob
    print(f'seed {sys.argv[2]}, {T:.0f}s, {evals} evaluations, {restarts} restarts, n in [{nmin},{nmax}]')
    print(f'best slack (X-local; >0 = X-local form FAILS) = {sl} = {float(sl):.5f}; its region slack0 = {float(sl0):.5f}')
    print(f'   n={len(iv)} P={iv}\n   (a, a\', s, t) = {cfg}')
    print(f'configurations with slack > 0: {len(pos_found)}')
    seen = {}
    for c, v in pos_found:
        k = tuple(canonical(v)); seen[k] = max(seen.get(k, c[0]), c[0])
    print(f'distinct canonical failing posets: {len(seen)}; by n: ' + str(sorted({len(k): 0 for k in seen})))
    for k, v in sorted(seen.items(), key=lambda kv: (len(kv[0]), -kv[1]))[:4]: print('   FAIL n=%d slack=%.6f' % (len(k), float(v)), list(k))
