"""xyzlp.py (mg-785e): the LP of proven linear facts (mg-561a lpcheck.build, imported read-only) EXTENDED by
  (TRI) exact triple-order variables: for chosen triples {x,y,z}, one variable per ordering consistent with P,
        summing to 1, with every pair marginal equal to the pair law of the base LP (this contains every
        3-cycle row and every Bonferroni/Frechet bound on a triple);
  (JT)  the base LP's joint variable J(a,a') of a two-separator pair of type AA or BB tied to the triple law
        (AA: J = P[s<a', t<a'];  BB: J = P[a<w1, a<w2]);
  (XYZ) Shepp's XYZ inequality P[x<y, x<z] >= P[x<y] P[x<z] and its dual P[y<x, z<x] >= P[y<x] P[z<x]
        (x incomparable to y and to z), relaxed EXACTLY by McCormick under-estimators of the product on a
        box of the two pair laws: uv >= lu*v + lv*u - lu*lv and uv >= hu*v + hv*u - hu*hv.
        Every row is implied by the true law, so max eps <= 0 (or infeasible) is a proof that no counterexample
        has this (P, L).  A positive value is NOT evidence of feasibility of the nonlinear system (relaxation).
Boxes: each pair law P[y before z] lies in [0, 1/3] or [2/3, 1] according to L; `boxes` may refine that.
"""
import sys, os
from itertools import permutations, combinations
from fractions import Fraction as F
from t3lib import *
sys.path.insert(0, os.path.join(HERE, '..', 'ksbft_t2_two_separator_561a'))
import lpcheck, xlp
from lpcheck import lin_add


def build(iv, L, tools=('T1', 'T2', 'T3'), triples='xyz', xyz=True, boxes=None, split=None):
    n = len(iv); pos = {v: i for i, v in enumerate(L)}
    M, eps = lpcheck.build(iv, L, tools)
    name2 = {nm: k for k, nm in enumerate(M.names)}
    X = {}
    for u in range(n):
        for v in range(n):
            if inc(iv, u, v) and pos[u] < pos[v]:
                X[(u, v)] = name2[f'x{iv[u]}{iv[v]}']
    def before(y, z):
        if lt(iv, y, z): return {None: 1}
        if lt(iv, z, y): return {None: 0}
        return {X[(z, y)]: 1} if pos[z] < pos[y] else {None: 1, X[(y, z)]: -1}
    def box(y, z):          # bounds on P[y before z]
        if boxes and (y, z) in boxes: return boxes[(y, z)]
        if boxes and (z, y) in boxes: lo, hi = boxes[(z, y)]; return (1 - hi, 1 - lo)
        if lt(iv, y, z): return (F(1), F(1))
        if lt(iv, z, y): return (F(0), F(0))
        return (F(0), F(1, 3)) if pos[z] < pos[y] else (F(2, 3), F(1))
    # --- triples
    T = {}
    def tri(trip):
        trip = tuple(sorted(trip))
        if trip in T: return T[trip]
        ords = [o for o in permutations(trip) if all(not lt(iv, o[j], o[i]) for i in range(3) for j in range(i + 1, 3))]
        vs = {o: M.var('t' + ''.join(str(iv[k]) for k in o)) for o in ords}
        M.add({v: 1 for v in vs.values()}, '=', 1)
        for y, z in combinations(trip, 2):
            if inc(iv, y, z):
                lhs = {vs[o]: 1 for o in ords if o.index(y) < o.index(z)}
                M.add(lin_add((1, lhs), (-1, before(y, z))), '=', 0)
        T[trip] = (ords, vs); return T[trip]
    def joint(trip, pred):   # linear form: P[pred(order)]
        ords, vs = tri(trip)
        return {vs[o]: 1 for o in ords if pred(o)}
    C = covers(iv)
    # JT: tie J(a,a') of AA / BB two-separator pairs to the triple law
    for a in range(n):
        for a2 in range(n):
            if not inc(iv, a, a2): continue
            A, B = seps_typed(iv, C, a, a2)
            if len(A) + len(B) != 2 or f'J{iv[a]}{iv[a2]}' not in name2: continue
            j = name2[f'J{iv[a]}{iv[a2]}']
            if len(A) == 2:
                s, t = A
                M.add(lin_add((1, {j: 1}), (-1, joint((s, t, a2), lambda o: o.index(s) < o.index(a2) and o.index(t) < o.index(a2)))), '=', 0)
            elif len(B) == 2:
                w1, w2 = B
                M.add(lin_add((1, {j: 1}), (-1, joint((w1, w2, a), lambda o: o.index(a) < o.index(w1) and o.index(a) < o.index(w2)))), '=', 0)
    nx = 0
    if xyz:
        for x in range(n):
            I = [y for y in range(n) if inc(iv, x, y)]
            for y, z in combinations(I, 2):
                if split is not None and not split(x, y, z): continue
                for dual in (False, True):
                    if not dual:
                        pj = joint((x, y, z), lambda o: o.index(x) < o.index(y) and o.index(x) < o.index(z))
                        u, v = before(x, y), before(x, z); bu, bv = box(x, y), box(x, z)
                    else:
                        pj = joint((x, y, z), lambda o: o.index(x) > o.index(y) and o.index(x) > o.index(z))
                        u, v = before(y, x), before(z, x); bu, bv = box(y, x), box(z, x)
                    for (lu, lv) in ((bu[0], bv[0]), (bu[1], bv[1])):
                        # pj >= lu*v + lv*u - lu*lv
                        M.add(lin_add((1, pj), (-lu, v), (-lv, u)), '>=', -lu * lv); nx += 1
    elif triples == 'all':
        pass
    return M, eps, T, nx


def solve(M, eps):
    st, val, x = xlp.solve(M.nv, M.rows, {eps: 1})
    return (None if st == 'infeasible' else val), x


def mk(ivl, Ll):
    used = set(); L = []
    for t in Ll:
        i = next(j for j in range(len(ivl)) if ivl[j] == t and j not in used); used.add(i); L.append(i)
    return L

Q12 = [(1, 1), (1, 2), (2, 3), (2, 5), (3, 4), (4, 5), (5, 6), (5, 8), (6, 7), (7, 8), (8, 9), (9, 9)]
LQ12 = [(1, 1), (1, 2), (2, 3), (3, 4), (2, 5), (4, 5), (5, 6), (5, 8), (6, 7), (7, 8), (8, 9), (9, 9)]

if __name__ == '__main__':
    import time
    L = mk(Q12, LQ12)
    for xyz in (False, True):
        t0 = time.time()
        M, eps, T, nx = build(Q12, L, xyz=xyz)
        if not xyz:   # triples only for the JT ties
            pass
        v, x = solve(M, eps)
        print(f"Q12 T1+T2+T3 +TRI/JT {'+XYZ(McCormick on L-boxes)' if xyz else ''}: eps* = {v}  [{M.nv} vars, {len(M.rows)} rows, {len(T)} triples, {nx} XYZ rows, {time.time()-t0:.1f}s]")
        sys.stdout.flush()
