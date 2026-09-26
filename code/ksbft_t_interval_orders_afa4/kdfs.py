"""kdfs.py (mg-afa4): exact search for a Brightwell-bad linear extension (every L-consecutive incomparable
pair has >=2 separators), by DFS with prefix pruning (separator sets depend only on P).
mode 'all': any linear extension; mode 'dom': L must respect interval dominance (the counterexample case).
Populations: full census n<=NCEN; random interval orders; named witnesses.  CONTROL: general posets with 2+2."""
import sys, random, os
from multiprocessing import Pool
from iolib import *
from brightwell import covers

def prep(iv):
    n = len(iv)
    LT = [[lt(iv, a, b) for b in range(n)] for a in range(n)]
    return prep_rel(n, LT, iv)

def prep_rel(n, LT, iv=None):
    INC = [[a != b and not LT[a][b] and not LT[b][a] for b in range(n)] for a in range(n)]
    COV = [[LT[a][b] and not any(LT[a][c] and LT[c][b] for c in range(n)) for b in range(n)] for a in range(n)]
    NS = [[sum(1 for z in range(n) if (COV[a][z] and INC[z][b]) or (COV[z][b] and INC[z][a])) for b in range(n)] for a in range(n)]
    DOM = [[False] * n for _ in range(n)]      # DOM[x][y]: x must precede y
    if iv is not None:
        for x in range(n):
            for y in range(n):
                if INC[x][y] and iv[x] != iv[y] and iv[x][0] <= iv[y][0] and iv[x][1] <= iv[y][1]: DOM[x][y] = True
    down = [sum(1 << w for w in range(n) if LT[w][v]) for v in range(n)]
    return n, INC, NS, DOM, down

def bad_ext(P, mode):
    n, INC, NS, DOM, down = P
    need = [down[v] | (sum(1 << w for w in range(n) if DOM[w][v]) if mode == 'dom' else 0) for v in range(n)]
    seen = set()
    def rec(used, last, depth, pre):
        if depth == n: return pre
        key = (used, last)
        if key in seen: return None
        for v in range(n):
            if used >> v & 1 or need[v] & ~used: continue
            if last >= 0 and INC[last][v] and NS[last][v] < 2: continue
            r = rec(used | 1 << v, v, depth + 1, pre + [v])
            if r: return r
        seen.add(key); return None
    return rec(0, -1, 0, [])

def job(iv):
    if all(not inc(iv, a, b) for a in range(len(iv)) for b in range(len(iv))): return None
    P = prep(iv)
    return (iv, bad_ext(P, 'all'), bad_ext(P, 'dom'))

def rand_io(n, h):
    iv = []
    for _ in range(n):
        a, b = sorted((random.randint(1, h), random.randint(1, h))); iv.append((a, b))
    return canon(iv)

if __name__ == '__main__':
    cores = int(os.environ.get('POGO_WORKER_CORES', '3'))
    NCEN = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    with Pool(cores) as pool:
        for n in range(3, NCEN + 1):
            R = [x for x in pool.imap_unordered(job, gen_fast(n), chunksize=256) if x]
            ba = [x for x in R if x[1]]; bd = [x for x in R if x[2]]
            print(f"census n={n}: {len(R)} non-chain interval orders; bad L (any L): {len(ba)}; bad L (dominance L): {len(bd)}"
                  + (f"  e.g. {ba[0][0]} L={ba[0][1]}" if ba else "")); sys.stdout.flush()
        random.seed(2026)
        for n in (10, 12, 14, 16, 20, 25, 30):
            pop = [rand_io(n, random.choice([n // 3 + 1, n // 2, n, 2 * n])) for _ in range(300 if n <= 16 else 120)]
            R = [x for x in pool.imap_unordered(job, pop, chunksize=4) if x]
            ba = [x for x in R if x[1]]; bd = [x for x in R if x[2]]
            print(f"random n={n}: {len(R)} non-chain interval orders; bad L (any): {len(ba)}; bad L (dom): {len(bd)}"
                  + (f"  e.g. {ba[0][0]} L={ba[0][1]}" if ba else "")); sys.stdout.flush()
