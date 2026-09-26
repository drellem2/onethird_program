"""swapladder.py (mg-ce69): census check of the Swap Ladder Theorem (docs/KSBFT-Q2-both-ends.md, Thm 1.4) and
its coverage compared with Local Linial.

For every connected poset in the files and every ordered pair x || b with down(x) SUBSET down(b)   (H1):
  b_0 = b < b_1 < .. < b_m = the chain bottom of Up(b) - Up(x) (Up = closed up-set; b_{i+1} the unique minimal
  element of what is left; stop when not unique or empty);  full = (Up(b) - Up(x) is exactly {b_0..b_m}).
  steps t_0 = P[x<b_0], t_i = P[x<b_i] - P[x<b_{i-1}], and t_{m+1} = P[b_m<x] when full.
  PROVEN claim 1: t_0 >= t_1 >= ... >= t_m (>= t_{m+1} if full).                         -> STEP_VIOLATION
  PROVEN claim 2: if P[x<b_0] <= 2/3 and P[x<b_m] >= 1/3 (automatic when full), some (x,b_i) is balanced.
                                                                                          -> SL_VIOLATION
Controls (must FIRE):
  CTRL_H1: the same step test on pairs violating H1 (down(x) not a subset of down(b)) -> some step increase.
  CTRL_WIN: 'balanced' narrowed to [0.34,0.66] in claim 2's conclusion -> a violation (sharp at 2+1).
Coverage: SL fires = some pair meets claim 2's hypotheses (so P has a balanced pair by the theorem, or its dual);
  LL fires = Local Linial (Thm 2.1 of KSBFT-Q) at either end.
Usage: python3 swapladder.py FILE...
"""
import sys
from fractions import Fraction
from lib import analyse, upmasks, inc, connected, chain_bottom, THIRD, TWOTHIRD

LO34, HI66 = Fraction(34, 100), Fraction(66, 100)


def ladders(dn, up, e, B, h1=True):
    """yield (x, chain, full, steps) for ordered pairs x||b; h1=False yields only pairs VIOLATING H1"""
    n = len(dn)
    for x in range(n):
        for b in range(n):
            if not inc(dn, up, x, b):
                continue
            sub = (dn[x] & ~dn[b]) == 0
            if sub != h1:
                continue
            W = [b] + [w for w in range(n) if up[b] >> w & 1 and not up[x] >> w & 1 and w != x]
            ch = chain_bottom(dn, W)
            full = len(ch) == len(W)
            r = [Fraction(B[x][c], e) for c in ch]
            steps = [r[0]] + [r[i] - r[i - 1] for i in range(1, len(r))]
            if full:
                steps.append(1 - r[-1])
            yield x, ch, full, r, steps


def ll_fires(dn, up, e, pos):
    n = len(dn)
    for x in range(n):
        if dn[x]:
            continue
        Z = [y for y in range(n) if inc(dn, up, x, y)]
        C = chain_bottom(dn, Z)
        k = len(C)
        if k and Fraction(pos[x][0], e) <= TWOTHIRD and Fraction(sum(pos[x][:k]), e) >= THIRD:
            return True
    return False


def run(files):
    c = dict(posets=0, pairs=0, STEP_VIOLATION=0, SL_VIOLATION=0, CTRL_H1=0, CTRL_WIN=0,
             SL_fires=0, LL_fires=0, SL_not_LL=0, LL_not_SL=0, neither=0, full_pairs=0)
    for f in files:
        for line in open(f):
            a = line.split()
            n = int(a[0])
            if n < 2:
                continue
            dn = [int(t, 16) for t in a[1:]]
            if not connected(dn):
                continue
            c["posets"] += 1
            up = upmasks(dn)
            e, B, pos = analyse(dn)
            sl = False
            for side in (0, 1):
                d, u = (dn, up) if side == 0 else (up, dn)
                Bs = B if side == 0 else [[B[j][i] for j in range(n)] for i in range(n)]
                for x, ch, full, r, steps in ladders(d, u, e, Bs):
                    c["pairs"] += 1
                    c["full_pairs"] += full
                    if any(steps[i + 1] > steps[i] for i in range(len(steps) - 1)):
                        c["STEP_VIOLATION"] += 1
                    if r[0] <= TWOTHIRD and r[-1] >= THIRD:
                        sl = True
                        if not any(THIRD <= p <= TWOTHIRD for p in r):
                            c["SL_VIOLATION"] += 1
                        if not any(LO34 <= p <= HI66 for p in r):
                            c["CTRL_WIN"] += 1
                for x, ch, full, r, steps in ladders(d, u, e, Bs, h1=False):
                    if any(steps[i + 1] > steps[i] for i in range(len(steps) - 1)):
                        c["CTRL_H1"] += 1
            posd = [[pos[x][n - 1 - j] for j in range(n)] for x in range(n)]
            ll = ll_fires(dn, up, e, pos) or ll_fires(up, dn, e, posd)
            c["SL_fires"] += sl
            c["LL_fires"] += ll
            c["SL_not_LL"] += sl and not ll
            c["LL_not_SL"] += ll and not sl
            c["neither"] += not sl and not ll
        print("file", f.split("/")[-1], " ".join(f"{k}={v}" for k, v in c.items()))
        sys.stdout.flush()
    return c


if __name__ == "__main__":
    c = run(sys.argv[1:])
    ok = c["STEP_VIOLATION"] == 0 and c["SL_VIOLATION"] == 0
    fire = c["CTRL_H1"] > 0 and c["CTRL_WIN"] > 0
    print("RESULT", "violations=0" if ok else "VIOLATION", "controls_fire" if fire else "CONTROL_DID_NOT_FIRE")
    sys.exit(0 if ok and fire else 1)
