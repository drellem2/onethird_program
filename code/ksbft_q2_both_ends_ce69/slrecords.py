"""slrecords.py (mg-ce69): Swap Ladder (Thm 1.4) coverage on mg-2912's kept records
(code/ksbft_range_probe/out/*.jsonl, n up to 24, deduplicated by down-mask list, n >= 3, not a chain), plus the
witnesses of this ticket.  'fires' = some ordered pair (x,b), in P or its dual, meets H1 and the quantitative
hypotheses P[x<b_0] <= 2/3, P[x<b_m] >= 1/3.  Every firing is checked to produce a balanced rung (0 expected).
Prints every record on which SL does not fire."""
import glob
import json
import os
import sys
from fractions import Fraction
from lib import analyse, upmasks, inc, THIRD, TWOTHIRD, fmt, parse, rng
from swapladder import ladders


def sl(dn):
    n = len(dn)
    up = upmasks(dn)
    e, B, _ = analyse(dn)
    fires = viol = 0
    for side in (0, 1):
        d, u = (dn, up) if side == 0 else (up, dn)
        Bs = B if side == 0 else [[B[j][i] for j in range(n)] for i in range(n)]
        for x, ch, full, r, steps in ladders(d, u, e, Bs):
            if r[0] <= TWOTHIRD and r[-1] >= THIRD:
                fires += 1
                viol += not any(THIRD <= p <= TWOTHIRD for p in r)
    return fires, viol


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    seen = {}
    for f in sorted(glob.glob(os.path.join(here, "../ksbft_range_probe/out/*.jsonl"))):
        for line in open(f):
            rec = json.loads(line)["rec"]
            if len(rec["down"]) >= 3:
                seen[tuple(rec["down"])] = rec["width"]
    tot = nf = nv = 0
    for dn, w in sorted(seen.items(), key=lambda t: len(t[0])):
        dn = list(dn)
        up = upmasks(dn)
        if not any(inc(dn, up, a, b) for a in range(len(dn)) for b in range(len(dn))):
            continue
        tot += 1
        fires, viol = sl(dn)
        nv += viol
        if fires:
            nf += 1
        else:
            print("NOFIRE width", w, "range", rng(dn), "|", fmt(dn))
            sys.stdout.flush()
    print(f"records (non-chain, n>=3): {tot}; SL fires on {nf}; SL conclusion violations {nv}")
    for name, s in (("P9", "9 0 0 2 2 3 b 2b 2f 7f"), ("rec11", "11 0 0 2 2 3 b 2b 2f af bf 1ff"),
                    ("W8", "8 0 0 0 4 4 6 16 2f"), ("W6", "6 0 0 2 2 3 f")):
        print(name, "SL firing pairs, violations:", sl(parse(s)))


if __name__ == "__main__":
    main()
