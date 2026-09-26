"""rec44.py (audit mg-3345): independent re-check (own ideal DP, own code) of KSBFT-Q §2.6 on
mg-2912's records with delta < 0.35: LL fires, crossing j*=0, the LL pair attains delta, bottom/top
split; and Remark 2.6's reading (extreme y with Inc(y)={x}; is x = v_2 in mean-height order?)."""
import glob, json
from fractions import Fraction as F
from functools import lru_cache

def analyse(down):
    n = len(down); full = (1 << n) - 1
    up = [sum(1 << j for j in range(n) if down[j] >> i & 1) for i in range(n)]
    @lru_cache(None)
    def fwd(I):   # linear extensions of the ideal I
        if not I: return 1
        return sum(fwd(I & ~(1 << v)) for v in range(n) if I >> v & 1 and not up[v] & I)
    @lru_cache(None)
    def bwd(I):   # linear extensions of P \ I (I ideal)
        if I == full: return 1
        return sum(bwd(I | 1 << v) for v in range(n) if not I >> v & 1 and (down[v] & ~I) == 0)
    e = fwd(full)
    # enumerate ideals
    ideals = set(); st = [0]
    while st:
        I = st.pop()
        if I in ideals: continue
        ideals.add(I)
        for v in range(n):
            if not I >> v & 1 and (down[v] & ~I) == 0: st.append(I | 1 << v)
    posc = [[0] * n for _ in range(n)]   # posc[v][k]: #ext with v at 0-based position k
    before = [[0] * n for _ in range(n)]  # before[a][b]: #ext with a before b
    for I in ideals:
        k = bin(I).count("1")
        for v in range(n):
            if not I >> v & 1 and (down[v] & ~I) == 0:
                c = fwd(I) * bwd(I | 1 << v)
                posc[v][k] += c
                for b in range(n):
                    if not (I | 1 << v) >> b & 1: before[v][b] += c
    return n, e, up, posc, before

def run():
    seen = {}
    for f in sorted(glob.glob("../ksbft_range_probe/out/*.jsonl")):
        for line in open(f):
            r = json.loads(line)["rec"]
            if len(r["down"]) >= 3: seen[tuple(r["down"])] = r["width"]
    print("distinct records n>=3:", len(seen))
    low = 0; stats = dict(fires=0, j0_att=0, bottom=0, top=0, width2=0, one_inc=0, x_is_v2=0, maxn=0)
    for down, w in seen.items():
        down = list(down); n = len(down)
        # cheap filter first: only analyse if claimed delta small (we recompute delta ourselves anyway for all with n<=24)
        n, e, up, posc, before = analyse(down)
        inc = lambda a, b: a != b and not down[a] >> b & 1 and not down[b] >> a & 1
        delta = max(F(min(before[a][b], before[b][a]), e) for a in range(n) for b in range(n) if inc(a, b))
        if delta >= F(35, 100): continue
        low += 1; stats['maxn'] = max(stats['maxn'], n); stats['width2'] += (w == 2)
        H = [F(sum((k + 1) * posc[v][k] for k in range(n)), e) for v in range(n)]
        hits = []
        for top in (False, True):
            dn = up if top else down
            ext = [v for v in range(n) if dn[v] == 0]
            for x in ext:
                I = [y for y in range(n) if inc(x, y)]
                rest = set(I); C = []
                while rest:
                    mn = [v for v in rest if not any(dn[v] >> u & 1 for u in rest)]
                    if len(mn) != 1: break
                    C.append(mn[0]); rest.remove(mn[0])
                q = [F(posc[x][n - 1 - j] if top else posc[x][j], e) for j in range(n)]
                k = len(C)
                if q[0] <= F(2, 3) and k >= 1 and sum(q[:k]) >= F(1, 3):
                    S = F(0)
                    for j in range(k):
                        S += q[j]
                        if S >= F(1, 3): break
                    c = C[j]
                    pv = F(before[c][x] if top else before[x][c], e)
                    hits.append((top, x, c, j, min(pv, 1 - pv) == delta))
        if hits: stats['fires'] += 1
        good = [h for h in hits if h[3] == 0 and h[4]]
        if good:
            stats['j0_att'] += 1
            if any(not h[0] for h in good): stats['bottom'] += 1
            else: stats['top'] += 1
        # Remark 2.6 structure: v_1 = min mean height; one incomparable?  is it v_2?
        order = sorted(range(n), key=lambda v: H[v]); v1, v2 = order[0], order[1]
        Iv1 = [y for y in range(n) if inc(v1, y)]
        orderT = sorted(range(n), key=lambda v: -H[v]); t1, t2 = orderT[0], orderT[1]
        It1 = [y for y in range(n) if inc(t1, y)]
        d1 = H[v1] - 1; dn_ = n - H[t1]
        end = (len(Iv1) == 1 and min(d1, 1 - d1) == delta) or (len(It1) == 1 and min(dn_, 1 - dn_) == delta)
        stats['one_inc'] += end
        stats['x_is_v2'] += (len(Iv1) == 1 and Iv1[0] == v2 and min(d1,1-d1) == delta) or (len(It1) == 1 and It1[0] == t2 and min(dn_,1-dn_) == delta)
    print("delta<0.35 records:", low, stats)

if __name__ == "__main__":
    run()
