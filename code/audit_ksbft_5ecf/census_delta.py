"""census_delta.py (audit mg-5ecf): KSBFT-T sec. 0 item 6 and sec. 5 (C1, C2, C7), independent engine.

Population per n: ordinal-indecomposable, twin-free interval orders (the author's population; counts must
be 160 / 866 / 5198 at n = 7 / 8 / 9). Reports: min delta and its posets; every poset with delta = 1/3;
min delta among non-semiorders; failure counts of
  C1 some pair of minimal elements, or of maximal elements, is balanced;
  C2 some balanced pair has equal l or equal r;
  C7 some pair consecutive in the (l,r)- or (r,l)-lexicographic order is balanced.
Also min delta over ALL interval orders (no restriction) per n, as context.
"""
import os, sys
from fractions import Fraction as F
from multiprocessing import Pool
import eng

THIRD = F(1, 3)


def bal(p):
    return THIRD <= p <= 2 * THIRD


def work(iv):
    P = eng.from_intervals(iv)
    n = P[0]
    e, N = eng.laws(P)
    d = eng.delta(P, (e, N))
    pop = eng.twin_free(P) and eng.ordinal_indecomposable(P)
    if not pop:
        return (False, d, None)
    semi = not eng.has_3p1(P)
    dn = eng.downs(P)
    up = P[1]
    B = lambda x, y: eng.inc(P, x, y) and bal(F(N[x][y], e))
    mins = [x for x in range(n) if dn[x] == 0]
    maxs = [x for x in range(n) if up[x] == 0]
    c1 = any(B(x, y) for S_ in (mins, maxs) for x in S_ for y in S_ if x < y)
    c2 = any(B(x, y) for x in range(n) for y in range(x + 1, n) if iv[x][0] == iv[y][0] or iv[x][1] == iv[y][1])
    o1 = sorted(range(n), key=lambda x: iv[x])
    o2 = sorted(range(n), key=lambda x: (iv[x][1], iv[x][0]))
    c7 = any(B(a, b) for o in (o1, o2) for a, b in zip(o, o[1:]))
    return (True, d, (semi, c1, c2, c7))


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    cores = int(os.environ.get("POGO_WORKER_CORES", "1"))
    fmt = lambda iv: "".join(f"[{l},{r}]" for l, r in iv)
    with Pool(cores) as pool:
        for n in range(3, N + 1):
            G = eng.gen(n)
            R = pool.map(work, G, chunksize=128)
            allmin = min(r[1] for r in R if r[1] > 0)
            popR = [(iv, r) for iv, r in zip(G, R) if r[0]]
            ds = [r[1] for _, r in popR]
            if not popR:
                continue
            m = min(ds)
            arg = [fmt(iv) for iv, r in popR if r[1] == m]
            third = [fmt(iv) for iv, r in popR if r[1] == THIRD]
            ns = [r[1] for _, r in popR if not r[2][0]]
            nsm = min(ns) if ns else None
            nsarg = [fmt(iv) for iv, r in popR if not r[2][0] and r[1] == nsm][:3]
            f1 = sum(1 for _, r in popR if not r[2][1])
            f2 = sum(1 for _, r in popR if not r[2][2])
            f7 = sum(1 for _, r in popR if not r[2][3])
            sub = [(iv, r) for iv, r in popR if r[1] != THIRD]
            m2 = min(r[1] for _, r in sub) if sub else None
            print(f"n={n}: population {len(popR)} (non-semiorders {len(ns)}); min delta (non-chain, all IO) = {allmin}")
            print(f"   min delta in population = {m} ({float(m):.5f}) at {arg[:3]}")
            print(f"   delta = 1/3 in population: {third}")
            if nsm is not None:
                print(f"   min delta among non-semiorders = {nsm} ({float(nsm):.5f}) at {nsarg}")
            print(f"   failures: C1 = {f1}, C2 = {f2}, C7 = {f7}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
