"""indep.py (audit mg-3345 of mg-5f14): independent re-check of the exact witnesses in
docs/KSBFT-Q-local-width2.md.  Shares no code with code/ksbft_q_local_width2_5f14: linear
extensions are ENUMERATED explicitly (no ideal DP), relations built from the down-masks by
transitive closure (the input masks are not trusted to be closed)."""
import sys, itertools
from fractions import Fraction as F

def parse(s):
    a = s.split(); n = int(a[0]); m = [int(t, 16) for t in a[1:]]
    assert len(m) == n
    less = [[bool(m[j] >> i & 1) for j in range(n)] for i in range(n)]  # less[i][j]: i<j
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if less[i][k] and less[k][j]: less[i][j] = True
    assert not any(less[i][i] for i in range(n))
    closed = all((m[j] >> i & 1) == less[i][j] for i in range(n) for j in range(n))
    return n, less, closed

def exts(n, less):
    out = []
    def rec(pre, used):
        if len(pre) == n: out.append(tuple(pre)); return
        for v in range(n):
            if not used >> v & 1 and all(used >> u & 1 for u in range(n) if less[u][v]):
                pre.append(v); rec(pre, used | 1 << v); pre.pop()
    rec([], 0); return out

def info(s):
    n, less, closed = parse(s)
    inc = lambda a, b: a != b and not less[a][b] and not less[b][a]
    L = exts(n, less); e = len(L)
    pos = [dict((v, i) for i, v in enumerate(l)) for l in L]
    p = lambda a, b: F(sum(1 for d in pos if d[a] < d[b]), e)
    I = {x: [y for y in range(n) if inc(x, y)] for x in range(n)}
    rng = max(len(v) for v in I.values())
    # width by brute force
    wid = max(r for r in range(1, n + 1) for S in itertools.combinations(range(n), r)
              if all(inc(a, b) for a, b in itertools.combinations(S, 2))) if n <= 11 else None
    mins = [x for x in range(n) if not any(less[y][x] for y in range(n))]
    maxs = [x for x in range(n) if not any(less[x][y] for y in range(n))]
    bal = sorted((a, b, p(a, b)) for a in range(n) for b in range(a + 1, n)
                 if inc(a, b) and F(1, 3) <= p(a, b) <= F(2, 3))
    delta = max(min(p(a, b), 1 - p(a, b)) for a in range(n) for b in range(n) if inc(a, b)) if rng else None
    return dict(n=n, less=less, closed=closed, e=e, L=L, pos=pos, p=p, I=I, rng=rng, wid=wid,
                mins=mins, maxs=maxs, bal=bal, delta=delta, inc=inc)

def chain_bottom(less, S):
    rest = set(S); out = []
    while rest:
        mn = [v for v in rest if not any(less[u][v] for u in rest)]
        if len(mn) != 1: break
        out.append(mn[0]); rest.remove(mn[0])
    return out, rest

def endinfo(d, x, top=False):
    n, less, pos, e = d['n'], d['less'], d['pos'], d['e']
    lt = (lambda a, b: less[b][a]) if top else (lambda a, b: less[a][b])
    Lr = [[None]*0]
    Z = d['I'][x]
    # chain bottom in the order lt
    rest = set(Z); C = []
    while rest:
        mn = [v for v in rest if not any(lt(u, v) for u in rest)]
        if len(mn) != 1: break
        C.append(mn[0]); rest.remove(mn[0])
    U = [v for v in rest if not any(lt(u, v) for u in rest)]
    # position law: #elements before x (after x if top)
    q = [0]*(n)
    for dd in pos:
        k = dd[x] if not top else n - 1 - dd[x]
        q[k] += 1
    q = [F(c, e) for c in q]
    S = list(itertools.accumulate(q))
    return dict(C=C, U=U, q=q, S=S, m=len(Z))

if __name__ == "__main__":
    for s in sys.argv[1:]:
        d = info(s)
        print("== poset", s, "| closed-input", d['closed'], "| n", d['n'], "e", d['e'], "range", d['rng'], "width", d['wid'])
        print("   minimal", d['mins'], "maximal", d['maxs'], "delta", d['delta'])
        print("   balanced pairs:", [(a, b, str(v)) for a, b, v in d['bal']])
        for top, ends in ((False, d['mins']), (True, d['maxs'])):
            for x in ends:
                E = endinfo(d, x, top)
                print("   %s x=%d Inc=%s m=%d C=%s U=%s q0=%s S=%s" % ("TOP" if top else "BOT", x, d['I'][x], E['m'], E['C'], E['U'],
                      E['q'][0], [str(t) for t in E['S'][:E['m']+1]]))
                for c in d['I'][x]:
                    pr = d['p'](x, c) if not top else d['p'](c, x)
                    print("      P[x before c=%d]%s = %s" % (c, " (top: c before x)" if top else "", pr))
