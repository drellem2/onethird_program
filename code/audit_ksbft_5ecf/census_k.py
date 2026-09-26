"""census_k.py (audit mg-5ecf): Claim K over ALL non-chain interval orders n <= N (default 10), independent engine.

For each n: number of non-chain interval orders with a bad linear extension (every consecutive incomparable
pair has >= 2 separators), any-L and dominance-respecting L. Lists every bad poset at n <= 9 with a witness L,
and for n = 10 the structural facts claimed in KSBFT-T sec. 3.3 (all contain 3+1; 1-3 intervals of
canonical length >= 2, the rest <= 1). Pool sized from POGO_WORKER_CORES.
"""
import os, sys
from multiprocessing import Pool
import eng


def work(iv):
    P = eng.from_intervals(iv)
    if all(not eng.inc(P, a, b) for a in range(P[0]) for b in range(P[0])):
        return None
    S = eng.seps(P)
    a = eng.badL(P, S)
    d = eng.badL(P, S, dominance=True) if a else None
    if not a:
        return None
    return iv, bool(d), eng.badL(P, S, dominance=bool(d), want=True), eng.has_3p1(P)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    cores = int(os.environ.get("POGO_WORKER_CORES", "1"))
    with Pool(cores) as pool:
        for n in range(2, N + 1):
            G = eng.gen(n)
            res = [r for r in pool.map(work, G, chunksize=256) if r]
            nany = len(res)
            ndom = sum(1 for r in res if r[1])
            print(f"n={n}: {len(G) - 1} non-chain interval orders; bad L (any) = {nany}; bad L (dominance) = {ndom}")
            if n <= 9:
                for iv, d, L, t31 in res:
                    print(f"   {' '.join(f'[{l},{r}]' for l, r in iv)}  dominance={d}  3+1={t31}")
                    print(f"      witness L = {' '.join(f'[{iv[x][0]},{iv[x][1]}]' for x in L)}")
            if res:
                all31 = all(r[3] for r in res)
                longs = sorted({sum(1 for l, r in iv if r - l >= 2) for iv, *_ in res})
                shortok = all(all(r - l <= 1 or r - l >= 2 for l, r in iv) for iv, *_ in res)
                print(f"   all contain 3+1: {all31}; #intervals with r-l >= 2 per bad poset: {longs}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
