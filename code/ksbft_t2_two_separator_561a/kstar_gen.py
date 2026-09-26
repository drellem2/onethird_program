"""kstar_gen.py (mg-561a): Q3 -- the same classification as kstar.py (Thm 2.1, TS, 2.1*, 3.1*, all PROVEN
for every poset) on random GENERAL posets n = 7..11 (random DAG + closure, chains excluded).
A counterexample's L respects dominance (down(x) <= down(y), up(x) >= up(y) => x before y; Zaguia Lemma 7).
Also splits the surviving L by whether P contains an induced 2+2 (interval orders cannot).
usage: python3 kstar_gen.py COUNT"""
import sys, os, random
from multiprocessing import Pool
import kstar

class G:
    """adapter: a general poset with the lt/inc interface kstar expects."""
    def __init__(s, n, LT): s.n = n; s.LT = LT

def run(seed):
    rnd = random.Random(seed); n = 7 + seed % 5; p = rnd.choice((0.15, 0.25, 0.35))
    LT = [[x < y and rnd.random() < p for y in range(n)] for x in range(n)]
    for c in range(n):
        for x in range(n):
            if LT[x][c]:
                for y in range(n):
                    if LT[c][y]: LT[x][y] = True
    if all(LT[x][y] or LT[y][x] for x in range(n) for y in range(n) if x != y): return None
    inc = lambda x, y: x != y and not LT[x][y] and not LT[y][x]
    cov = lambda x, y: LT[x][y] and not any(LT[x][c] and LT[c][y] for c in range(n))
    A = {}; B = {}
    for x in range(n):
        for y in range(n):
            if inc(x, y):
                A[(x, y)] = frozenset(z for z in range(n) if cov(x, z) and inc(z, y))
                B[(x, y)] = frozenset(w for w in range(n) if cov(w, y) and inc(w, x))
    dn = [frozenset(w for w in range(n) if LT[w][v]) for v in range(n)]
    up = [frozenset(w for w in range(n) if LT[v][w]) for v in range(n)]
    need = [sum(1 << w for w in range(n) if LT[w][v] or (inc(w, v) and dn[w] <= dn[v] and up[w] >= up[v]
                and not (dn[w] == dn[v] and up[w] == up[v]))) for v in range(n)]
    # monkeypatch kstar's lt/inc for this poset
    kstar.inc = lambda iv, x, y: inc(x, y); kstar.lt = lambda iv, x, y: LT[x][y]
    iv = list(range(n))
    Ls = kstar.all_bad(iv, A, B, need, cap=5000)
    cnt = {}; ex = None
    for L in Ls:
        c = kstar.classify(iv, L, A, B); cnt[c] = cnt.get(c, 0) + 1
        if c == 'SURVIVES' and ex is None: ex = (n, [(x, y) for x in range(n) for y in range(n) if LT[x][y] and cov(x, y)], L)
    two2 = any(LT[a][b] and LT[c][d] and inc(a, c) and inc(a, d) and inc(b, c) and inc(b, d)
               for a in range(n) for b in range(n) for c in range(n) for d in range(n) if len({a, b, c, d}) == 4)
    return cnt, two2, ex

if __name__ == '__main__':
    COUNT = int(sys.argv[1])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        out = [o for o in pool.map(run, range(COUNT), chunksize=32) if o]
    tot = {}; ps = 0; ps22 = 0; pk = 0
    exs = []
    for cnt, two2, ex in out:
        if ex: exs.append(ex)
        for c, v in cnt.items(): tot[c] = tot.get(c, 0) + v
        if cnt: pk += 1
        if cnt.get('SURVIVES'): ps += 1; ps22 += two2
    print(f"{len(out)} random non-chain general posets n=7..11; {pk} have a K-bad dominance L; "
          f"all K-bad L killed by {dict(sorted(tot.items()))}; posets with a surviving L: {ps} (containing 2+2: {ps22})")
    exs.sort(key=lambda e: e[0])
    for n, cov, L in exs[:3]: print(f"   survivor n={n} covers={cov} L={L}")
