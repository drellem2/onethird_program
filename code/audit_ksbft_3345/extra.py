"""extra.py (audit mg-3345): further independent checks for docs/KSBFT-Q-local-width2.md."""
import itertools
from fractions import Fraction as F
from indep import info, parse

# (1) P_9: self-duality by brute force over 9! relabellings; P[2<3]; ends' windows; where balanced pairs sit.
s = "9 0 0 2 2 3 b 2b 2f 7f"
d = info(s); n, less = d['n'], d['less']
dual = [[less[j][i] for j in range(n)] for i in range(n)]
iso = next((g for g in itertools.permutations(range(n))
            if all(less[i][j] == dual[g[i]][g[j]] for i in range(n) for j in range(n))), None)
print("P_9 self-dual:", iso is not None, "map", iso)
print("P_9 P[2<3] =", d['p'](2, 3))
wins = {("bot", x): {x, *d['I'][x]} for x in d['mins']} | {("top", x): {x, *d['I'][x]} for x in d['maxs']}
for a, b, v in d['bal']:
    print("P_9 balanced (%d,%d)=%s  inside a window: %s  touching windows: %s" % (a, b, v,
          [k for k, W in wins.items() if a in W and b in W], [k for k, W in wins.items() if a in W or b in W]))
cov = sorted((i, j) for i in range(n) for j in range(n) if less[i][j] and not any(less[i][k] and less[k][j] for k in range(n)))
print("P_9 covers:", cov)

# (2) the n=11 range-6 record
s11 = "11 0 0 2 2 3 b 2b 2f af bf 1ff"
d = info(s11)
print("R11: e", d['e'], "range", d['rng'], "width", d['wid'], "delta", d['delta'], "closed", d['closed'])
print("R11 balanced:", [(a, b, str(v)) for a, b, v in d['bal']])
wins = {("bot", x): {x, *d['I'][x]} for x in d['mins']} | {("top", x): {x, *d['I'][x]} for x in d['maxs']}
print("R11 windows:", {k: sorted(W) for k, W in wins.items()})
for a, b, v in d['bal']:
    print("R11 balanced (%d,%d) inside a window: %s touching: %s" % (a, b, [k for k, W in wins.items() if a in W and b in W],
          [k for k, W in wins.items() if a in W or b in W]))

# (3) 8-element min3 witness: isolated element?
d8 = info("8 0 0 0 4 4 6 16 2f")
print("W8 isolated elements:", [x for x in range(8) if len(d8['I'][x]) == 7])

# (4) section 3.2 inclusion claim "{f(x)<=j+1} subset of intersection over U of {x before u}" for j>k:
#     Y-gadget c<u, c<v plus isolated x.  k=1, U={u,v}; test j=k and j=k+1.
d = info("4 0 1 1 0")   # 0=c, 1=u, 2=v, 3=x
x, U = 3, [1, 2]
for j in (1, 2):
    A = [dd for dd in d['pos'] if dd[x] <= j]                 # f(x) <= j+1  (0-based position <= j)
    B = [dd for dd in d['pos'] if all(dd[x] < dd[u] for u in U)]
    sub = all(all(dd[x] < dd[u] for u in U) for dd in A)
    sup = all(dd[x] <= j for dd in B)
    print("3.2 check j=%d: {f(x)<=j+1} subset of cap_U {x<u}: %s ; superset: %s ; P=%s vs %s" % (
        j, sub, sup, F(len(A), d['e']), F(len(B), d['e'])))

# (5) Remark 2.6 as stated vs KSBFT-A: is x necessarily v_2 (second-lowest mean height)?  Search small posets.
def height(d, v): return F(sum(dd[v] + 1 for dd in d['pos']), d['e'])
