"""wincount.py (audit mg-3345): independent recount (own DP from rec44.py, own WIN/BR/minpair
definitions written from the doc's prose) of KSBFT-Q's census columns on one census file."""
import sys
from fractions import Fraction as F
from rec44 import analyse

def run(path):
    agg = dict(indec=0, win_fail=0, br_fail=0, min3_nobal=0, rng=0)
    wit = []
    for line in open(path):
        a = line.split(); n = int(a[0]); down = [int(t, 16) for t in a[1:]]
        if n < 2: continue
        inc = lambda x, y: x != y and not down[x] >> y & 1 and not down[y] >> x & 1
        seen = 1; st = [0]
        while st:
            v = st.pop()
            for w in range(n):
                if not seen >> w & 1 and inc(v, w): seen |= 1 << w; st.append(w)
        if seen != (1 << n) - 1: continue
        agg['indec'] += 1
        _, e, up, posc, before = analyse(down)
        bal = lambda x, y: inc(x, y) and F(1, 3) <= F(before[x][y], e) <= F(2, 3)
        def ends(dn, first):
            ext = [v for v in range(n) if dn[v] == 0]
            win = any(bal(p, q) for x in ext for W in [[x] + [y for y in range(n) if inc(x, y)]] for p in W for q in W if p < q)
            x = min(ext, key=first)
            I = [y for y in range(n) if inc(x, y)]
            rest = set(I); C = []
            while rest:
                mn = [v for v in rest if not any(dn[v] >> u & 1 for u in rest)]
                if len(mn) != 1: break
                C.append(mn[0]); rest.remove(mn[0])
            U = [v for v in rest if not any(dn[v] >> u & 1 for u in rest)]
            T = [x] + C + U
            br = any(bal(p, q) for p in T for q in T if p < q)
            return win, br, ext
        wb, bb, mins = ends(down, lambda v: posc[v][0])
        wt, bt, _ = ends(up, lambda v: posc[v][n - 1])
        if not (wb or wt): agg['win_fail'] += 1; wit.append(" ".join(a))
        if not (bb or bt): agg['br_fail'] += 1
        if len(mins) >= 3 and not any(bal(p, q) for p in mins for q in mins if p < q): agg['min3_nobal'] += 1
    print(path.split("/")[-1], agg, "WIN-fail witnesses:", wit[:5])

for p in sys.argv[1:]: run(p)
