#!/usr/bin/env python3
"""Independent re-computation for the audit of mg-b447 (KSBFT-F), mg-de37.
Written without reading code/ksbft_f_b447/check.py.  Exact Fractions, no randomness.
usage: python3 indep_de37.py NMAX
"""
import sys, itertools
from fractions import Fraction as Fr
from math import comb

def posets(n):
    """all naturally labelled posets on 0..n-1 as sets of (i,j), i<j meaning i<_P j (transitive)."""
    pairs = [(i, j) for j in range(n) for i in range(j)]
    out = []
    def rec(idx, rel):
        if idx == len(pairs):
            out.append(frozenset(rel)); return
        i, j = pairs[idx]
        # decide whether i<j; pairs ordered by j then i, so all (a,b) with b<j are decided
        # transitivity check done at the end of each column j
        for choice in (False, True):
            if choice: rel.add((i, j))
            ok = True
            if i == j - 1:  # column j complete: check closure for column j
                for a in range(j):
                    for b in range(a + 1, j):
                        if (a, b) in rel and (b, j) in rel and (a, j) not in rel: ok = False
                        if (a, b) in rel and (a, j) not in rel and False: pass
                # downward closure: if a<j then every c<a must be <j
                for a in range(j):
                    if (a, j) in rel:
                        for c in range(a):
                            if (c, a) in rel and (c, j) not in rel: ok = False
            if ok: rec(idx + 1, rel)
            if choice: rel.discard((i, j))
    rec(0, set())
    return out

def lt(rel, a, b): return (a, b) in rel
def inc(rel, a, b): return a != b and (a, b) not in rel and (b, a) not in rel

def linexts(n, rel):
    preds = [[a for a in range(n) if (a, b) in rel] for b in range(n)]
    res = []
    def rec(seq, used):
        if len(seq) == n: res.append(tuple(seq)); return
        for v in range(n):
            if not used[v] and all(used[p] for p in preds[v]):
                used[v] = True; seq.append(v); rec(seq, used); seq.pop(); used[v] = False
    rec([], [False]*n)
    return res

def rng(n, rel): return max([sum(inc(rel, x, y) for y in range(n)) for x in range(n)] + [0])

def f(D): return sum(comb(j - 1 + r, r) for j in range(1, D + 1) for r in range(0, 2*D - j))
def c(D): return Fr(1, 1 + f(D))

def mincover(A, B, edges):
    if not edges: return 0
    V = sorted(set([a for a, _ in edges] + [b for _, b in edges]))
    for s in range(1, len(V) + 1):
        for S in itertools.combinations(V, s):
            S = set(S)
            if all(a in S or b in S for a, b in edges): return s

def main(NMAX):
    print("== c(D) and f(D) recomputed")
    for D in range(1, 7): print(f"  D={D} f={f(D)} c={c(D)} 2^(1-2D)={Fr(1,2**(2*D-1))} ok={c(D) >= Fr(1,2**(2*D-1))}")
    print("  D<=30 c(D)>=2^(1-2D):", all(c(D) >= Fr(1, 2**(2*D-1)) for D in range(1, 31)))
    counts = {}
    worst = {}          # D -> max tau
    tau_gt_D = {}       # D -> #cuts with tau > D
    viol = dict(K=0, flip=0, thm31=0, uid=0, bw=0, onept=0)
    ctrl = dict(Kminus=0, flip_half=0, tau_D=0, onept_every=0)
    for n in range(1, NMAX + 1):
        Ps = posets(n); counts[n] = len(Ps)
        for rel in Ps:
            D = rng(n, rel)
            if D == 0: continue
            L = linexts(n, rel); N = len(L)
            pos = [{v: i for i, v in enumerate(s)} for s in L]
            # flip probabilities
            P = {}
            for a in range(n):
                for b in range(n):
                    if inc(rel, a, b):
                        P[(a, b)] = Fr(sum(1 for p in pos if p[a] < p[b]), N)
                        if P[(b, a)] if (b, a) in P else False: pass
            for (a, b), p in P.items():
                if 1 - p < c(D): viol['flip'] += 1      # P[b before a] >= c(D)
                if 1 - p < Fr(1, 2): ctrl['flip_half'] += 1
                # bandwidth in every LE
                for q in pos:
                    if abs(q[a] - q[b]) > 2*D - 1: viol['bw'] += 1
            # e = identity (natural labelling), every prefix cut
            for k in range(1, n):
                A = set(range(k)); B = set(range(k, n))
                edges = [(a, b) for a in A for b in B if inc(rel, a, b)]
                tau = mincover(A, B, edges)
                worst[D] = max(worst.get(D, 0), tau)
                if tau > D: tau_gt_D[D] = tau_gt_D.get(D, 0) + 1
                if tau > D - 1: ctrl['tau_D'] += 1
                Ks = [len(A - set(s[:k])) for s in L]
                if max(Ks) > D: viol['K'] += 1
                if max(Ks) > D - 1: ctrl['Kminus'] += 1
                EK = Fr(sum(Ks), N); d1 = EK / min(k, n - k)
                if edges:
                    FD = Fr(2*D - 1) * d1 / (2 * c(D))   # E2 reading: eps = Delta1
                    if FD * n < tau: viol['thm31'] += 1
            # U-identity
            for x in range(n):
                h = Fr(sum(p[x] for p in pos), N)  # 0-based position
                rhs = sum((P[(y, x)] for y in range(n) if inc(rel, x, y) and y > x), Fr(0)) \
                    - sum((P[(x, y)] for y in range(n) if inc(rel, x, y) and y < x), Fr(0))
                if h - x != rhs: viol['uid'] += 1
            # one-point transport, exists-v form
            if n >= 3:
                bal = lambda p: Fr(1, 3) <= p <= Fr(2, 3)
                balP = {(a, b) for (a, b), p in P.items() if a < b and bal(p)}
                ok_exists = False; ok_every = True
                for v in range(n):
                    keep = [u for u in range(n) if u != v]
                    idx = {u: i for i, u in enumerate(keep)}
                    rel2 = frozenset((idx[a], idx[b]) for (a, b) in rel if a != v and b != v)
                    if rng(n - 1, rel2) == 0: continue
                    L2 = linexts(n - 1, rel2)
                    surv = False
                    for (a, b) in balP:
                        if v in (a, b): continue
                        p2 = Fr(sum(1 for s in L2 if s.index(idx[a]) < s.index(idx[b])), len(L2))
                        if bal(p2): surv = True; break
                    ok_exists |= surv; ok_every &= surv
                if not ok_exists: viol['onept'] += 1
                if not ok_every: ctrl['onept_every'] += 1
    print("== naturally labelled poset counts (A006455: 1,1,2,7,40,357,4824,96428):", counts)
    print("  non-chains with n>=3:", sum(counts[n] - 1 for n in counts if n >= 3))
    print("== violations (each must be 0):", viol)
    print("== firing controls (each must be > 0):", {k: (v, 'FIRES' if v else 'SILENT') for k, v in ctrl.items()})
    print("== max tau per range D (against 2D-1):", {D: (worst[D], 2*D - 1) for D in sorted(worst)})
    print("== #cuts with tau > D, per D:", tau_gt_D)

def wstar(a, b, t):
    """W*_t(a,b): c1<..<c_{a-2} < {x,y} < b1<..<b_b, minus x<b1..x<bt. returns names, rel."""
    names = [f"c{i}" for i in range(1, a - 1)] + ["x", "y"] + [f"b{i}" for i in range(1, b + 1)]
    ix = {s: i for i, s in enumerate(names)}
    rel = set()
    lowA = [f"c{i}" for i in range(1, a - 1)]
    for i, u in enumerate(lowA):
        for w in lowA[i+1:] + ["x", "y"] + [f"b{j}" for j in range(1, b + 1)]: rel.add((ix[u], ix[w]))
    for j in range(1, b + 1):
        rel.add((ix["y"], ix[f"b{j}"]))
        if j > t: rel.add((ix["x"], ix[f"b{j}"]))
        for jj in range(j + 1, b + 1): rel.add((ix[f"b{j}"], ix[f"b{jj}"]))
    # check transitivity
    for (p, q) in list(rel):
        for (r, s) in list(rel):
            assert not (q == r and (p, s) not in rel), "not transitive"
    return names, ix, frozenset(rel)

def witnesses():
    print("== W*_t witnesses, independent construction (a, b, t)")
    for (a, b, t) in [(3,3,2),(4,4,2),(4,28,2),(5,9,2),(4,8,3),(4,9,6),(4,10,7),(4,12,9),(6,20,12)]:
        names, ix, rel = wstar(a, b, t); n = len(names)
        L = linexts(n, rel); N = len(L)
        x, y = ix["x"], ix["y"]
        pxy = Fr(sum(1 for s in L if s.index(x) < s.index(y)), N)
        A = set(range(a))
        EK = Fr(sum(len(A - set(s[:a])) for s in L), N)
        edges = [(u, w) for u in A for w in range(a, n) if inc(rel, u, w)]
        tau = mincover(A, set(range(a, n)), edges)
        pis = [sum(inc(rel, u, w) for w in range(n)) for u in range(n)]
        # sides: P[A] incomparable pairs, P[B] incomparable pairs
        sideA = [(names[u], names[w]) for u in A for w in A if u < w and inc(rel, u, w)]
        sideB = [(names[u], names[w]) for u in range(a, n) for w in range(a, n) if u < w and inc(rel, u, w)]
        print(f"  a={a} b={b} t={t}: n={n} #LE={N} range={max(pis)} pi(x)={pis[x]} others<=1:{max(p for i,p in enumerate(pis) if i!=x)<=1}"
              f" p_xy={pxy} (1/(t+2)={Fr(1,t+2)}) EK={EK} (t/(t+2)={Fr(t,t+2)}) Delta1={EK/min(a,b)} tau={tau} sideA={sideA} sideB={sideB}")
    print("== W*(4,4,2) delete b1")
    names, ix, rel = wstar(4, 4, 2); n = len(names)
    def probs(keep):
        idx = {u: i for i, u in enumerate(keep)}
        rel2 = frozenset((idx[p], idx[q]) for (p, q) in rel if p in idx and q in idx)
        L = linexts(len(keep), rel2)
        out = {}
        for u in keep:
            for w in keep:
                if u < w and inc(rel2, idx[u], idx[w]):
                    out[(names[u], names[w])] = Fr(sum(1 for s in L if s.index(idx[u]) < s.index(idx[w])), len(L))
        return out
    full = probs(list(range(n)))
    print("  P:", full)
    for v in names:
        sub = probs([u for u in range(n) if names[u] != v])
        balsub = [k for k, p in sub.items() if Fr(1,3) <= p <= Fr(2,3)]
        surv = [k for k in balsub if Fr(1,3) <= full[k] <= Fr(2,3)]
        print(f"  delete {v}: balanced in P-v {balsub} -> survive in P {surv}")
    print("== other witness ranges")
    Z = lambda m: frozenset((i, j) for i in range(m) for j in range(m) if j - i >= 2)
    print("  Z_m ranges m=3..14:", [rng(m, Z(m)) for m in range(3, 15)])
    print("  2+2:", rng(4, frozenset({(0,1),(2,3)})), " N-poset:", rng(4, frozenset({(0,2),(0,3),(1,3)})))

def staircase():
    """tau = D is attained for every D: u_1<..<u_m, v_1<..<v_m, u_i < v_j iff j > i, no v below a u.
    Cut A = {u}.  Matching u_i - v_i, so tau = m; pi(u_m) = pi(v_1) = m, so D = m."""
    print("== staircase S_m: tau = D attained for every D (refutes nothing; shows the audit's tau <= D is sharp)")
    for m in range(1, 7):
        n = 2*m
        rel = set()
        for i in range(m):
            for j in range(i + 1, m): rel.add((i, j)); rel.add((m + i, m + j))
            for j in range(m):
                if j > i: rel.add((i, m + j))
        rel = frozenset(rel)
        for (p, q) in rel:
            for (r, s2) in rel: assert not (q == r and (p, s2) not in rel)
        edges = [(a, b) for a in range(m) for b in range(m, n) if inc(rel, a, b)]
        tau = mincover(None, None, edges); D = rng(n, rel)
        print(f"  m={m}: range D={D} tau={tau} 2D-1={2*D-1} tau==D:{tau == D}")

if __name__ == "__main__":
    witnesses()
    staircase()
    main(int(sys.argv[1]))
