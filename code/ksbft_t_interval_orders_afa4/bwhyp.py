"""bwhyp.py (mg-afa4): which hypotheses does Claim K need?  Count interval orders having a Brightwell-bad L when
(a) dominance constraint dropped, (b) only 'l(x)<=l(y) & r(x)<=r(y)' pairs with l strictly smaller, etc.,
(c) decomposable / twins allowed (dominance kept)."""
import sys
from iolib import *
from brightwell import covers, seps, linexts
def dom_ok(iv, L, mode):
    pos = {v: i for i, v in enumerate(L)}; n = len(iv)
    for x in range(n):
        for y in range(n):
            if not inc(iv, x, y) or iv[x] == iv[y] or pos[x] < pos[y]: continue
            lx, rx = iv[x]; ly, ry = iv[y]
            if mode == 'full' and lx <= ly and rx <= ry: return False
            if mode == 'sameL' and lx == ly and rx < ry: return False       # only down-twin classes
            if mode == 'sameLR' and ((lx == ly and rx < ry) or (rx == ry and lx < ly)): return False
    return True
def has_bad(iv, mode):
    C = covers(iv)
    for L in linexts(iv):
        if mode != 'none' and not dom_ok(iv, L, mode): continue
        if all(len(seps(iv, C, L[i], L[i + 1])) >= 2 for i in range(len(L) - 1) if inc(iv, L[i], L[i + 1])):
            return L
    return None
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
for n in range(3, NMAX + 1):
    res = {}
    for mode in ['none', 'sameL', 'sameLR', 'full']:
        cnt = 0; ex = None
        for iv in gen(n):
            if decomposable(iv) or len(set(iv)) < n: continue
            L = has_bad(iv, mode)
            if L: cnt += 1; ex = ex or (iv, L)
        res[mode] = (cnt, ex)
    cnt = 0; ex = None; chains = 0
    for iv in gen(n):            # all interval orders incl. decomposable and with twins, full dominance
        if all(not inc(iv, a, b) for a in range(n) for b in range(n)): continue
        L = has_bad(iv, 'full')
        if L: cnt += 1; ex = ex or (iv, L)
    res['full, all non-chain (decomp+twins)'] = (cnt, ex)
    print(f"n={n}: " + "; ".join(f"{k}: {v[0]}" + (f" e.g. {v[1][0]} L={v[1][1]}" if v[1] else "") for k, v in res.items()))
    sys.stdout.flush()
