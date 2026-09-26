"""EMPIRICAL probe: is N_C(x) = #{c in C : c before x} log-concave for every chain C?
Positive control: f(x) (Stanley) must never fail.  Negative control: the same statistic
for an ANTICHAIN A in place of C (not expected log-concave) should fail sometimes."""
import random, sys, itertools
from lib import *

def rand_poset(n, p, rng):
    rel = set()
    perm = list(range(n)); rng.shuffle(perm)
    for a in range(n):
        for b in range(a+1, n):
            if rng.random() < p: rel.add((perm[a], perm[b]))
    return Poset(n, closure(n, rel))

def chains_of(P, maxlen=None):
    n = P.n
    out = []
    for mask in range(1, 1 << n):
        el = [i for i in range(n) if (mask >> i) & 1]
        if len(el) < 2: continue
        if all(P.comparable(a, b) for a, b in itertools.combinations(el, 2)):
            out.append(mask)
    return out

def antichains_of(P):
    n = P.n; out = []
    for mask in range(1, 1 << n):
        el = [i for i in range(n) if (mask >> i) & 1]
        if len(el) < 2: continue
        if not any(P.comparable(a, b) for a, b in itertools.combinations(el, 2)):
            out.append(mask)
    return out

def is_unimodal(seq):
    i = 0
    while i + 1 < len(seq) and seq[i + 1] >= seq[i]: i += 1
    while i + 1 < len(seq) and seq[i + 1] <= seq[i]: i += 1
    return i == len(seq) - 1

def dist(P, x, M):
    pl = P.placements(x)
    k = popcount(M)
    d = [0]*(k+1)
    for S, w in pl: d[popcount(S & M)] += w
    return d

if __name__ == "__main__":
    rng = random.Random(5371)
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 400
    stats = dict(posets=0, chainpairs=0, chainfail=0, chainunimodalfail=0, fxfail=0, antipairs=0, antifail=0)
    example = None
    for t in range(trials):
        n = rng.randint(4, 9)
        P = rand_poset(n, rng.choice([0.15, 0.25, 0.35, 0.5]), rng)
        stats['posets'] += 1
        ch = chains_of(P); an = antichains_of(P)
        for x in range(n):
            fx = [0]*n
            for S, w in P.placements(x): fx[popcount(S)] += w
            if not is_logconcave(fx): stats['fxfail'] += 1
            for M in ch:
                if (M >> x) & 1: continue
                stats['chainpairs'] += 1
                if not is_logconcave(dist(P, x, M)):
                    stats['chainfail'] += 1
                    if not is_unimodal(dist(P, x, M)): stats['chainunimodalfail'] += 1
                    if example is None: example = (n, P.below, x, M, dist(P, x, M))
            for M in an:
                if (M >> x) & 1: continue
                stats['antipairs'] += 1
                if not is_logconcave(dist(P, x, M)): stats['antifail'] += 1
    print(stats)
    print("first chain failure:", example)
    print("positive control f(x) (Stanley):", "PASS" if stats['fxfail'] == 0 else "FAIL")
    print("negative control antichain count:", "FIRES" if stats['antifail'] > 0 else "DOES NOT FIRE")
    print("chain statistic N_C(x) log-concave:", "0 failures" if stats['chainfail'] == 0 else "FAILS")
    print("chain statistic N_C(x) unimodal:", "0 failures" if stats['chainunimodalfail'] == 0 else "FAILS")
