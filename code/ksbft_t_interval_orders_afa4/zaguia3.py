"""zaguia3.py (mg-afa4): does every indecomposable twin-free interval order contain a configuration of Zaguia's
Thm 3 (arXiv:1610.00809), which certifies a balanced pair with NO probability input?  (Brightwell 1989 gives one
in every semiorder: condition (i).)  Autonomy of {x,y} in P-Z: every v outside {x,y}uZ relates to x and y alike."""
import sys
from iolib import *
def auton(iv, x, y, Z):
    return all((lt(iv, v, x) == lt(iv, v, y)) and (lt(iv, x, v) == lt(iv, y, v)) for v in range(len(iv)) if v not in Z and v not in (x, y))
def z3(iv):
    n = len(iv); R = range(n)
    for dual in (False, True):
        LT = (lambda a, b: lt(iv, b, a)) if dual else (lambda a, b: lt(iv, a, b))
        I = lambda a, b: a != b and not LT(a, b) and not LT(b, a)
        for x in R:
            for y in R:
                if not I(x, y): continue
                for z in R:
                    if LT(x, z) and I(y, z) and auton(iv, x, y, {z}): return 'i'
                for z in R:
                    for t in R:
                        if z == t: continue
                        if LT(x, z) and LT(y, t) and I(y, z) and I(x, t) and auton(iv, x, y, {z, t}): return 'ii'
                        if LT(t, x) and LT(x, z) and I(y, z) and I(y, t) and auton(iv, x, y, {z, t}): return 'iii'
    return None
for n in range(4, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
    tot = miss = semimiss = 0; ex = None
    for iv in gen_fast(n):
        if decomposable(iv) or len(set(iv)) < n: continue
        tot += 1
        if z3(iv) is None:
            miss += 1; ex = ex or iv
            if not any(iv[a][0] < iv[b][0] and iv[b][1] < iv[a][1] for a in range(n) for b in range(n)): semimiss += 1
    print(f"n={n}: {tot} indecomposable twin-free interval orders; NO Zaguia-Thm-3 configuration: {miss} (semiorders among them: {semimiss} -- must be 0)" + (f"  e.g. {ex}" if ex else ""))
