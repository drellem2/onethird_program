"""goodpair.py (mg-ce69): how often do posets have a Zaguia good pair (Order 2019, Def. 1: in P or its dual,
D(a) SUBSET D(b), U(b)-U(a) a chain, P(a<b) <= 1/2), versus the chain-bottom Swap Ladder of the doc (Thm 1.4,
quantitative hypotheses P[a<b_0] <= 2/3, P[a<b_m] >= 1/3)?  EMPIRICAL coverage only; prints posets with no
good pair (first 5 per file) with their range.  Usage: python3 goodpair.py FILE...  (census files)
       python3 goodpair.py --records   (mg-2912's records)"""
import glob
import json
import os
import sys
from fractions import Fraction
from lib import analyse, upmasks, inc, connected, fmt, rng, THIRD, TWOTHIRD
from swapladder import ladders

HALF = Fraction(1, 2)


def classify(dn):
    n = len(dn)
    up = upmasks(dn)
    e, B, _ = analyse(dn)
    good = sl = False
    for side in (0, 1):
        d, u = (dn, up) if side == 0 else (up, dn)
        Bs = B if side == 0 else [[B[j][i] for j in range(n)] for i in range(n)]
        for x, ch, full, r, steps in ladders(d, u, e, Bs):
            if full and r[0] <= HALF:
                good = True
            if r[0] <= TWOTHIRD and r[-1] >= THIRD:
                sl = True
    return good, sl


def main(args):
    if args == ["--records"]:
        here = os.path.dirname(os.path.abspath(__file__))
        seen = {}
        for f in sorted(glob.glob(os.path.join(here, "../ksbft_range_probe/out/*.jsonl"))):
            for line in open(f):
                rec = json.loads(line)["rec"]
                if len(rec["down"]) >= 3:
                    seen[tuple(rec["down"])] = 1
        sources = [("records", [list(k) for k in seen])]
    else:
        sources = []
        for f in args:
            L = []
            for line in open(f):
                a = line.split()
                if int(a[0]) >= 2:
                    L.append([int(t, 16) for t in a[1:]])
            sources.append((f.split("/")[-1], L))
    for name, L in sources:
        c = dict(posets=0, good=0, sl=0, sl_not_good=0)
        shown = 0
        for dn in L:
            if not connected(dn):
                continue
            c["posets"] += 1
            g, s = classify(dn)
            c["good"] += g
            c["sl"] += s
            c["sl_not_good"] += s and not g
            if not g and shown < 5:
                shown += 1
                print("NO_GOOD_PAIR range", rng(dn), "|", fmt(dn), "| SL fires" if s else "| SL silent")
        print("file", name, " ".join(f"{k}={v}" for k, v in c.items()))
        sys.stdout.flush()


if __name__ == "__main__":
    main(sys.argv[1:])
