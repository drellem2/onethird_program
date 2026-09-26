"""mg-244e instrument: does (T∃^any) of KSBFT-R Prop 5.1 (IDEALS only) fail on prime posets?
(T∃^any)(P): some proper ideal A with P[A] a non-chain has a pair balanced in P[A] AND in P.
Also the filter-closed variant (ideal OR filter). Random small posets; instrument only, not a census."""
import random
from fractions import Fraction as Fr
from itertools import combinations
from indep import Poset, fibrel
third = Fr(1, 3); bal = lambda p: third <= p <= 2 * third

def sub(P, S):
    S = sorted(S); ix = {v: i for i, v in enumerate(S)}
    return Poset(len(S), [(ix[a], ix[b]) for a in S for b in S if P.lt(a, b)]), ix

def texists(P, filters=False):
    full = (1 << P.n) - 1
    pairs = [(a, b) for a, b in combinations(range(P.n), 2) if not P.comp(a, b)]
    balP = {pr for pr in pairs if bal(P.before(*pr))}
    lev = P.ideals_by_size()
    sets = [I for L in lev[2:P.n] for I in L]
    if filters:
        sets += [full & ~I for L in lev[1:P.n - 1] for I in L]
    for S in sets:
        mem = [v for v in range(P.n) if (S >> v) & 1]
        cand = [(a, b) for (a, b) in balP if a in mem and b in mem]
        if not cand:
            continue
        Q, ix = sub(P, mem)
        for a, b in cand:
            if bal(Q.before(ix[a], ix[b])):
                return True
    return False

def main():
    # positive control for the detector: the doc's own W*_2(4,4) and F_8 must satisfy it; a hand-made failure must fail
    print("control F_8:", texists(Poset(8, fibrel(8))))
    random.seed(7)
    stats = {}
    ex = None
    for trial in range(3000):
        n = random.choice((5, 6, 7, 8)); pr = random.choice((0.25, 0.35, 0.45))
        perm = list(range(n)); random.shuffle(perm)
        P = Poset(n, [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if random.random() < pr])
        if P.proper_nonchain_module() is not None or not P.g_conn() or not P.g_conn(True):
            continue   # keep only prime, both-connected (the K_min shape minus range)
        ti, tf = texists(P), texists(P, True)
        stats[(ti, tf)] = stats.get((ti, tf), 0) + 1
        if not ti and ex is None:
            ex = (n, sorted((a, b) for a in range(n) for b in P.above[a]), P.rng(), float(P.delta()))
    print("prime both-connected hosts: (ideal-only holds, ideal-or-filter holds) -> count:", stats)
    print("first ideal-only failure:", ex)
    # POSITIVE CONTROL: the detector must return False somewhere (any non-chain, n<=6)
    random.seed(11); found = None; cnt = 0
    for t in range(20000):
        n = random.choice((3, 4, 5, 6)); pr = random.random()
        perm = list(range(n)); random.shuffle(perm)
        P = Poset(n, [(perm[i], perm[j]) for i in range(n) for j in range(i + 1, n) if random.random() < pr])
        if all(P.comp(a, b) for a in range(n) for b in range(a + 1, n)):
            continue
        cnt += 1
        if not texists(P):
            found = (n, sorted((a, b) for a in range(n) for b in P.above[a]), P.proper_nonchain_module()); break
    print("POSITIVE CONTROL: detector returns False on", found, "after", cnt, "non-chains -> FIRES" if found else "-> DID NOT FIRE")


if __name__ == "__main__":
    main()
