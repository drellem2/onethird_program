"""lemmac_census.py (audit mg-6c30): Lemma C as a rule (forbid an L-consecutive strict-containment step with
exactly 2 separators) on every dominance-respecting K-bad L of every interval order with n = 9, 10."""
import os
from multiprocessing import Pool
from eng import gen, Poset
from badl import all_bad
from lemmac import lemmaC_fires

def job(iv):
    P = Poset.from_iv(iv)
    if not any(P.inc[x][y] for x in range(P.n) for y in range(P.n)): return None   # chains: vacuous
    Ls = all_bad(P)
    if not Ls: return None
    return iv, len(Ls), sum(lemmaC_fires(P, iv, L) for L in Ls)

if __name__ == '__main__':
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in (9, 10):
            R = [r for r in pool.imap_unordered(job, gen(n), chunksize=256) if r]
            print(f"n={n}: K-bad posets {len(R)}, K-bad L {sum(r[1] for r in R)}, Lemma C fires on {sum(r[2] for r in R)}; "
                  f"posets with an L Lemma C misses: {sum(1 for r in R if r[2] < r[1])}", flush=True)
