"""records.py (mg-5f14): run the LL / BR tests on mg-2912's kept low-delta and low-M records and
annealing witnesses (code/ksbft_range_probe/out/*.jsonl, n up to 24).  For each record: width,
delta, whether LL fires at the bottom / top, and whether the LL pair (x, c_j) is a delta-attaining
pair.  Records are deduplicated by down-mask list across all files and tags."""
import glob
import json
import sys
from fractions import Fraction
from probe import analyse, dual, inc, chain_bottom, window_tests, balanced


def ll_pairs(n, dn, up, e, B, pos):
    out = []
    for x in [v for v in range(n) if dn[v] == 0]:
        q = pos[x]
        I = [y for y in range(n) if inc(dn, up, x, y)]
        cb = chain_bottom(dn, I)
        k = len(cb)
        if Fraction(q[0], e) <= Fraction(2, 3) and k >= 1 and Fraction(sum(q[:k]), e) >= Fraction(1, 3):
            S = 0
            for j in range(k):
                S += q[j]
                if Fraction(S, e) >= Fraction(1, 3):
                    out.append((x, cb[j], j))
                    break
    return out


def main(files):
    seen = {}
    for f in files:
        for line in open(f):
            rec = json.loads(line)["rec"]
            if len(rec["down"]) >= 3:
                seen[tuple(rec["down"])] = rec["width"]
    byw = {}
    low = [0, 0, 0, 0]  # records with delta<0.35; LL fires (either end); ... with j*=0 and the pair attaining delta; ... at the bottom
    for dn, w in seen.items():
        dn = list(dn)
        n = len(dn)
        up = dual(dn)
        e, B, pos, _ = analyse(dn)
        delta = max(Fraction(min(B[x][y], B[y][x]), e) for x in range(n) for y in range(n) if inc(dn, up, x, y))
        Bd = [[B[y][x] for y in range(n)] for x in range(n)]
        posd = [[pos[x][n - 1 - j] for j in range(n)] for x in range(n)]
        lb = ll_pairs(n, dn, up, e, B, pos)
        lt = ll_pairs(n, up, dn, e, Bd, posd)
        a = byw.setdefault(w, [0, 0])
        a[0] += 1
        a[1] += bool(lb or lt)
        if delta < Fraction(35, 100):
            att = lambda L: any(j == 0 and Fraction(min(B[x][c], B[c][x]), e) == delta for x, c, j in L)
            low[0] += 1
            low[1] += bool(lb or lt)
            low[2] += att(lb) or att(lt)
            low[3] += att(lb)
    print("distinct records (n>=3) in", len(files), "files:", len(seen))
    print("AGG delta<0.35: records %d, LL fires %d, LL crossing j*=0 with the pair attaining delta %d, of which at the bottom end %d" % tuple(low))
    for w in sorted(byw):
        print("AGG width %d: records %d, LL fires at some end %d" % (w, *byw[w]))


if __name__ == "__main__":
    main(sys.argv[1:] or sorted(glob.glob("../ksbft_range_probe/out/*.jsonl")))
