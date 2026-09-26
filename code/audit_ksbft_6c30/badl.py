"""badl.py (audit mg-6c30): every dominance-respecting K-bad L (every L-consecutive incomparable step has
|S| >= 2) of every interval order with n <= N, and which of the doc's rules kill it, re-implemented from the
doc's TEXT (Thm 3.1 consecutive 'TS', Thm 2.1*, Thm 3.1*), not from kstar.py.
usage: python3 badl.py NMIN NMAX"""
import sys, os
from multiprocessing import Pool
from eng import gen, Poset


def need_masks(P):
    n = P.n
    return [sum(1 << w for w in range(n) if P.lt[w][v] or P.dominates(w, v)) for v in range(n)]


def all_bad(P, cap=10 ** 6):
    n = P.n; need = need_masks(P); dead = set(); out = []
    def ok(u, v):
        return not P.inc[u][v] or len(P.S(u, v)) >= 2
    def rec(I, last, pre):
        if len(pre) == n:
            out.append(tuple(pre)); return True
        if (I, last) in dead: return False
        found = False
        for v in range(n):
            if (I >> v) & 1 or need[v] & ~I: continue
            if last >= 0 and not ok(last, v): continue
            pre.append(v)
            if rec(I | (1 << v), v, pre): found = True
            pre.pop()
            if len(out) >= cap: return True
        if not found: dead.add((I, last))
        return found
    rec(0, -1, [])
    return out


def kvec(P, a, c, b):
    """the counted separator events of Thm 3.1, as (element, 'after'|'before', reference)."""
    ev = [(z, 'after', c) for z in P.A(a, c) - P.A(b, c)]
    ev += [(w, 'before', a) for w in P.B(a, c)]
    ev += [(w, 'before', c) for w in P.B(c, b) - P.B(c, a)]
    ev += [(z, 'after', b) for z in P.A(c, b)]
    return ev


def kills(P, L):
    """set of rule names that refute L as the 2/3-order of a counterexample."""
    n = P.n; pos = {v: i for i, v in enumerate(L)}; res = set()
    for i in range(n - 2):
        a, c, b = L[i], L[i + 1], L[i + 2]
        if P.inc[a][c] and P.inc[c][b] and len(kvec(P, a, c, b)) <= 2: res.add('TS')
    def outside(e):
        z, d, r = e
        return pos[z] > pos[r] if d == 'after' else pos[z] < pos[r]
    for a in range(n):
        for a2 in range(n):
            if P.inc[a][a2] and pos[a] < pos[a2]:
                S = [(z, 'after', a2) for z in P.A(a, a2)] + [(w, 'before', a) for w in P.B(a, a2)]
                if len(S) <= 1 and all(outside(e) for e in S): res.add('2.1*')
    for a in range(n):
        for c in range(n):
            if not (P.inc[a][c] and pos[a] < pos[c]): continue
            for b in range(n):
                if not (P.inc[c][b] and pos[c] < pos[b]): continue
                ev = kvec(P, a, c, b)
                if len(ev) <= 2 and all(outside(e) for e in ev): res.add('3.1*')
    return res


def job(iv):
    P = Poset.from_iv(iv)
    if not any(P.inc[x][y] for x in range(P.n) for y in range(P.n)): return None
    Ls = all_bad(P)
    if not Ls: return (iv, [])
    return (iv, [(L, sorted(kills(P, L))) for L in Ls])


def fmt(iv, L=None):
    return ' '.join(f"[{l},{r}]" for l, r in ([iv[v] for v in L] if L is not None else iv))


if __name__ == '__main__':
    n0, n1 = int(sys.argv[1]), int(sys.argv[2])
    with Pool(int(os.environ.get('POGO_WORKER_CORES', '3'))) as pool:
        for n in range(n0, n1 + 1):
            R = [r for r in pool.imap_unordered(job, gen(n), chunksize=256) if r]
            bad = [(iv, Ls) for iv, Ls in R if Ls]
            nL = sum(len(Ls) for _, Ls in bad)
            prio = {}; anyk = {}
            surv = []
            for iv, Ls in bad:
                for L, ks in Ls:
                    p = next((k for k in ('TS', '2.1*', '3.1*') if k in ks), 'SURVIVES')
                    prio[p] = prio.get(p, 0) + 1
                    anyk[tuple(ks)] = anyk.get(tuple(ks), 0) + 1
                    if not ks: surv.append((iv, L))
            print(f"n={n}: non-chain {len(R)}; posets with a K-bad dominance L: {len(bad)}; K-bad L: {nL}; "
                  f"first-match kill {dict(sorted(prio.items()))}; kill-sets {dict(sorted(anyk.items()))}; survivors {len(surv)}",
                  flush=True)
            if n <= 9:
                for iv, Ls in sorted(bad):
                    for L, ks in Ls:
                        print(f"   P = {fmt(iv)}\n   L = {fmt(iv, L)}  kills={ks}")
            if n == 10:
                for iv, Ls in sorted(bad):
                    for L, ks in Ls:
                        if 'TS' not in ks:
                            print(f"   non-TS: P = {fmt(iv)}\n           L = {fmt(iv, L)}  kills={ks}")
            for iv, L in surv[:5]:
                print(f"   SURVIVOR P = {fmt(iv)}\n            L = {fmt(iv, L)}")
