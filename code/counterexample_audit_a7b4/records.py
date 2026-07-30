"""Per-poset record builder for the mg-a7b4 audit.  Independent of the target's
`probe.py`: in particular the directional move masses q(x<y) are obtained by
counting topological sorts of the quotient with one extra edge, rather than by
enumerating every P-compatible ordered partition.  That makes delta_walk
computable at n = 7, where the target's own instrument stops at n = 6.
"""

import pickle
import sys
from fractions import Fraction

from kernel import (Lattice, Poset, count_topological_sorts, level_move_counts,
                    levels_of, majority_relation, multiplicities, pair_data,
                    posets_up_to_iso, quotient_adj, restriction_counts)


class Rec(object):
    __slots__ = ("cover", "n", "e", "delta", "R", "ps", "primitive", "chain",
                 "tie_free", "maj_acyclic", "Lstar", "levels", "mult", "mc",
                 "nmoves", "lam", "lam2", "s_max", "delta_walk", "pi",
                 "qfrac", "qmass", "nlev", "levprof", "multprof", "inv4",
                 "spec", "width", "einv")


def _width(P):
    """Largest antichain, by brute force over subsets (n <= 7)."""
    best = 0
    for S in range(1 << P.n):
        ok = True
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if P.up[x] & S:
                ok = False
                break
        if ok:
            best = max(best, bin(S).count("1"))
    return best


def build(P, lat):
    r = Rec()
    n = P.n
    r.n = n
    r.cover = P.covers_string()
    e = restriction_counts(P)
    full = (1 << n) - 1
    r.e = e[full]
    _, _, ps = pair_data(P)
    r.ps = ps
    r.chain = not ps
    r.primitive = P.incomparability_connected()
    mins = [min(p, 1 - p) for p in ps.values()]
    r.delta = max(mins) if mins else None
    r.R = 3 * sum(mins) / len(mins) if mins else None
    r.einv = sum(mins) if mins else Fraction(0)      # E[inv(L,L*)] by Prop 2
    edges, tf, ac, L = majority_relation(P, ps)
    r.tie_free, r.maj_acyclic, r.Lstar = tf, ac, L
    r.levels = levels_of(P, lat)
    r.mult = multiplicities(P, lat, r.levels, e)
    r.mc = level_move_counts(P, lat, r.levels)
    r.nmoves = sum(r.mc.values())
    r.nlev = len(r.levels)
    lp = [0] * (n + 1)
    mp = [0] * (n + 1)
    for X in r.levels:
        lp[lat.nblocks[X]] += 1
        mp[lat.nblocks[X]] += r.mult[X]
    r.levprof = tuple(lp[1:])
    r.multprof = tuple(mp[1:])
    # eigenvalues: lambda_X = mass of moves whose level is COARSER than or equal to X
    lam = {}
    for X in r.levels:
        tot = 0
        for Y in r.levels:
            if X in lat.refiners[Y]:
                tot += r.mc[Y]
        lam[X] = Fraction(tot, r.nmoves)
    r.lam = lam
    cands = [lam[X] for X in r.levels if r.mult[X] > 0 and X != lat.bottom]
    r.lam2 = max(cands) if cands else Fraction(0)
    r.spec = tuple(sorted((lam[X], r.mult[X]) for X in r.levels if r.mult[X] > 0))
    # per-pair move masses: s (same block), q(x<y), q(y<x)
    r.pi = {}
    smax = Fraction(0)
    dwalk = None
    for (x, y) in ps:
        same = qxy = qyx = 0
        for X in r.levels:
            blocks = lat.parts[X]
            bof = lat.blockof[X]
            if bof[x] == bof[y]:
                same += r.mc[X]
                continue
            adj = quotient_adj(P, blocks, bof)
            k = len(blocks)
            a1 = list(adj)
            a1[bof[x]] |= 1 << bof[y]
            fwd = count_topological_sorts(k, a1)
            qxy += fwd
            qyx += r.mc[X] - fwd
        s = Fraction(same, r.nmoves)
        smax = max(smax, s)
        pi = Fraction(qxy, qxy + qyx) if qxy + qyx else None
        r.pi[(x, y)] = (s, Fraction(qxy, r.nmoves), Fraction(qyx, r.nmoves), pi)
        if pi is not None:
            v = min(pi, 1 - pi)
            dwalk = v if dwalk is None else max(dwalk, v)
    r.s_max = smax if ps else None
    r.delta_walk = dwalk
    # quotient concentration around L*'s chain of contiguous intervals
    r.qfrac = r.qmass = None
    if tf and ac and ps:
        cut_sets = []
        for mask in range(1 << (n - 1)):
            blocks, cur = [], 1 << L[0]
            for i in range(1, n):
                if (mask >> (i - 1)) & 1:
                    blocks.append(cur)
                    cur = 0
                cur |= 1 << L[i]
            blocks.append(cur)
            cut_sets.append(tuple(sorted(blocks, key=lambda B: B & -B)))
        idxs = []
        for key in cut_sets:
            j = lat.index[key]
            assert j in r.mult, "interval partition of L* is NOT a level"
            idxs.append(j)
        r.qfrac = Fraction(len(idxs), r.nlev)
        r.qmass = Fraction(sum(r.mult[j] for j in idxs), r.e)
    fp = []
    for X in r.levels:
        prof = tuple(sorted((bin(B).count("1"), e[B]) for B in lat.parts[X]))
        fp.append((prof, r.mult[X], r.mc[X]))
    r.inv4 = (r.nlev, tuple(sorted(fp)))
    r.width = _width(P)
    return r


def build_all(n, cache=True):
    path = "records_n%d.pkl" % n
    if cache:
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except IOError:
            pass
    pops = posets_up_to_iso(1)
    for k in range(2, n + 1):
        pops = posets_up_to_iso(k, pops)
    lat = Lattice(n)
    recs = [build(P, lat) for P in pops]
    if cache:
        with open(path, "wb") as f:
            pickle.dump(recs, f)
    return recs


if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]]:
        recs = build_all(n)
        print("n=%d: %d posets, %d non-chains, %d primitive non-chains"
              % (n, len(recs), sum(1 for r in recs if not r.chain),
                 sum(1 for r in recs if not r.chain and r.primitive)))
