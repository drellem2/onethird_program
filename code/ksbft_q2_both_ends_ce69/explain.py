"""explain.py (mg-ce69): for each witness, every Swap Ladder (Thm 1.4) whose quantitative hypotheses hold,
with its rungs and the balanced rung it certifies ('P' = in P, 'D' = in the dual; a dual ladder (x; b_0..) certifies
P[b_i < x]).  Exact Fractions."""
from fractions import Fraction
from lib import parse, analyse, upmasks, THIRD, TWOTHIRD, fmt
from swapladder import ladders
from longtail import grow, dual, glue

P9 = parse("9 0 0 2 2 3 b 2b 2f 7f")
W = [("W6", parse("6 0 0 2 2 3 f")), ("P9", P9), ("B7", parse("7 0 0 2 2 3 b 2b")),
     ("rec11", parse("11 0 0 2 2 3 b 2b 2f af bf 1ff")), ("W8", parse("8 0 0 0 4 4 6 16 2f")),
     ("Y8_nostruct", parse("8 0 0 2 2 3 b 1b 2f")),
     ("Q_4", glue(grow(P9, 4, 1), dual(grow(P9, 4, 1)), 1))]
for name, dn in W:
    n = len(dn)
    up = upmasks(dn)
    e, B, _ = analyse(dn)
    print(f"== {name}: {fmt(dn)}  e={e}")
    for side in (0, 1):
        d, u = (dn, up) if side == 0 else (up, dn)
        Bs = B if side == 0 else [[B[j][i] for j in range(n)] for i in range(n)]
        for x, ch, full, r, steps in ladders(d, u, e, Bs):
            if r[0] <= TWOTHIRD and r[-1] >= THIRD:
                i = next(i for i, p in enumerate(r) if THIRD <= p <= TWOTHIRD)
                print(f"   {'PD'[side]} pivot {x}; chain {ch}{' (full)' if full else ''}; rungs {[str(p) for p in r]}; "
                      f"steps {[str(s) for s in steps]}; balanced rung ({x},{ch[i]}) = {r[i]}")
