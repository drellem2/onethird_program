"""probe.py (mg-afa4): candidate lemmas on interval orders, n<=NMAX (instrument, not a census extension).
Population: all unlabelled interval orders (canonical multisets), ordinal-indecomposable, twin-free
(twins = equal intervals, give P=1/2 trivially).  For each, which natural pair families contain a balanced pair."""
import sys, os
from fractions import Fraction as F
from multiprocessing import Pool
from iolib import *
T3 = F(1, 3)

def chain_bottom(iv, S, start):
    """start, then successive unique minimal elements of S (a set of indices)."""
    out = [start]; rest = set(S) - {start}
    while rest:
        mins = [z for z in rest if not any(lt(iv, w, z) for w in rest)]
        if len(mins) != 1: return out, False
        out.append(mins[0]); rest.discard(mins[0])
    return out, True

def ladder_fires(iv, P, x, b, dual=False):
    """Swap Ladder Thm 1.4 at (x;b): primal needs down(x)<=down(b), i.e. l(x)<=l(b)."""
    n = len(iv)
    if not dual:
        W = {z for z in range(n) if z == b or lt(iv, b, z)} - {z for z in range(n) if z == x or lt(iv, x, z)}
        L, full = chain_bottom(iv, W, b)
        ps = [P[(x, c)] for c in L]
    else:  # reverse the order
        W = {z for z in range(n) if z == b or lt(iv, z, b)} - {z for z in range(n) if z == x or lt(iv, z, x)}
        rev = [(-r, -l) for l, r in iv]
        L, full = chain_bottom(rev, W, b)
        ps = [P[(c, x)] for c in L]
    if ps[0] > 2 * T3: return False
    return ps[-1] >= T3 or (full and ps[0] < T3)

def analyse(iv):
    n = len(iv)
    if decomposable(iv) or len(set(iv)) < n: return None
    P, e = prob(iv)
    d = delta(P)
    if d is None: return None
    B = [k for k, p in P.items() if bal(p) and k[0] < k[1]]
    l = [a for a, _ in iv]; r = [b for _, b in iv]; h = max(r)
    mins = [i for i in range(n) if l[i] == 1]; maxs = [i for i in range(n) if r[i] == h]
    res = {}
    res['C1_min_or_max_pair'] = any((a in mins and b in mins) or (a in maxs and b in maxs) for a, b in B)
    res['C2_same_l_or_same_r'] = any(l[a] == l[b] or r[a] == r[b] for a, b in B)
    res['C8_dominance_pair'] = any((l[a] - l[b]) * (r[a] - r[b]) >= 0 for a, b in B)
    res['C8c_containment_pair'] = any((l[a] - l[b]) * (r[a] - r[b]) < 0 for a, b in B)
    lex = sorted(range(n), key=lambda i: (l[i], r[i])); rl = sorted(range(n), key=lambda i: (r[i], l[i]))
    cons = lambda o: any(inc(iv, o[i], o[i + 1]) and bal(P[(o[i], o[i + 1])]) for i in range(n - 1))
    res['C7_consecutive_lr_or_rl'] = cons(lex) or cons(rl)
    # ladders
    def fires(pivots):
        for x in range(n):
            for b in range(n):
                if x == b or not inc(iv, x, b): continue
                if l[x] <= l[b] and pivots(x, b, False) and ladder_fires(iv, P, x, b): return True
                if r[x] >= r[b] and pivots(x, b, True) and ladder_fires(iv, P, x, b, True): return True
        return False
    res['L1_ladder_from_min/max_pivot_pair'] = fires(lambda x, b, d: (r[x] == h and r[b] == h) if d else (l[x] == 1 and l[b] == 1))
    res['L2_ladder_from_same_l/same_r_pair'] = fires(lambda x, b, d: r[x] == r[b] if d else l[x] == l[b])
    res['L3_ladder_from_containment_or_twinclass'] = fires(lambda x, b, d: True)
    semi = not any(l[a] < l[b] and r[b] < r[a] for a in range(n) for b in range(n))
    return (n, d, semi, res, iv, e)

if __name__ == '__main__':
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    cores = int(os.environ.get('POGO_WORKER_CORES', '3'))
    for n in range(3, NMAX + 1):
        with Pool(cores) as pool:
            R = [x for x in pool.imap_unordered(analyse, gen_fast(n), chunksize=64) if x]
        keys = list(R[0][3]) if R else []
        dmin = min(x[1] for x in R); wmin = [x for x in R if x[1] == dmin]
        io_ns = [x for x in R if not x[2]]
        dmin_ns = min(x[1] for x in io_ns) if io_ns else None
        print(f"n={n}: {len(R)} indecomposable twin-free interval orders ({len(io_ns)} not semiorders); "
              f"min delta = {dmin} = {float(dmin):.5f} on {len(wmin)} (e.g. {wmin[0][4]}); "
              f"min delta non-semiorder = {dmin_ns}" + (f" = {float(dmin_ns):.5f}" if dmin_ns else ""))
        for k in keys:
            miss = [x for x in R if not x[3][k]]
            print(f"   {k:42s} fails on {len(miss):6d}" + (f"   e.g. {miss[0][4]} delta={float(miss[0][1]):.4f}" if miss else ""))
        sys.stdout.flush()
