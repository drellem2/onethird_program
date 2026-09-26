"""lpcheck.py (mg-561a): can the PROVEN LINEAR calculus kill a Brightwell-bad L?

Given an interval order P and a candidate 2/3-order L, variables are
  x_{uv} = P[v before u] for every incomparable pair with u before v in L (so a counterexample needs x < 1/3),
  B(a,a') = P(Lambda_2(a,a')) for every ordered incomparable pair, beta = joint laws for two-separator pairs.
Tool sets (each is a theorem that holds in EVERY poset, so a real counterexample satisfies all of them):
  T1  Swap Identity (Thm 1.1): B(a,a') - B(a',a) = P[a<a'] - P[a'<a]; 0 <= B(a,a') <= P[a<a'];
      B(a,a') >= P[a<z<a'] for each separator z; B(a,a') <= sum_z P[a<z<a'] (union bound), exact
      inclusion-exclusion with a joint variable when |S| = 2; B(a,a') = 0 when S(a,a') is empty.
      (For above-separators z, {a<z<a'} = {z<a'}; for below-separators w, {a<w<a'} = {a<w}.)
  T2  Swap Ladder Thm 1.4 (mg-ce69, audited) in P and in the dual, with Doubling Lemma 1.5 equalities.
  T3  Prop 2.2 (containment, Z = S): P(one separator between) <= P(Lambda_1), P(both between) <= P(Lambda_1).
Maximise eps subject to x <= 1/3 - eps.  eps* <= 0 (or infeasible) means the tools refute L.
CONTROL: any L with a consecutive incomparable step with |S| <= 1 must be refuted by T1 alone (Thm 2.1).
usage: python3 lpcheck.py"""
import sys
from fractions import Fraction as F
from t2lib import *
from shape import shape
import xlp

class Model:
    def __init__(s): s.nv = 0; s.rows = []; s.names = []
    def var(s, name): s.names.append(name); s.nv += 1; return s.nv - 1
    def add(s, lin, sense, rhs):
        """lin: dict var->coef plus optional key None for a constant on the LHS."""
        c = lin.pop(None, 0); s.rows.append((lin, sense, F(rhs) - c))

def lin_add(*ts):
    out = {}
    for coef, d in ts:
        for k, v in d.items(): out[k] = out.get(k, 0) + coef * v
    return out

def build(iv, L, tools):
    n = len(iv); pos = {v: i for i, v in enumerate(L)}; C = covers(iv); M = Model()
    eps = M.var('eps'); X = {}
    for u in range(n):
        for v in range(n):
            if inc(iv, u, v) and pos[u] < pos[v]:
                X[(u, v)] = M.var(f'x{iv[u]}{iv[v]}')
                M.add({X[(u, v)]: 1, eps: 1}, '<=', F(1, 3))
    def before(y, z):                      # linear form for P[y before z]
        if lt(iv, y, z): return {None: 1}
        if lt(iv, z, y): return {None: 0}
        return {X[(z, y)]: 1} if pos[z] < pos[y] else {None: 1, X[(y, z)]: -1}
    def ev_between(a, a2, z, above):       # linear form for P[a < z < a'] for a separator z
        return before(z, a2) if above else before(a, z)
    Bv = {}
    if 'T1' in tools:
        for a in range(n):
            for a2 in range(n):
                if inc(iv, a, a2): Bv[(a, a2)] = M.var(f'B{iv[a]}{iv[a2]}')
        for (a, a2), b in Bv.items():
            A, Bs = seps_typed(iv, C, a, a2)
            M.add(lin_add((1, {b: 1}), (-1, before(a, a2))), '<=', 0)
            if not A and not Bs: M.add({b: 1}, '=', 0); continue
            evs = [ev_between(a, a2, z, True) for z in A] + [ev_between(a, a2, z, False) for z in Bs]
            for e in evs: M.add(lin_add((1, {b: 1}), (-1, e)), '>=', 0)
            if len(evs) == 2:
                j = M.var(f'J{iv[a]}{iv[a2]}')
                M.add(lin_add((1, {b: 1}), (-1, evs[0]), (-1, evs[1]), (1, {j: 1})), '=', 0)
                M.add(lin_add((1, {j: 1}), (-1, evs[0])), '<=', 0)
                M.add(lin_add((1, {j: 1}), (-1, evs[1])), '<=', 0)
                if 'T3' in tools and shape(iv[a], iv[a2]) == 'CONT_IN' and len(A) == 2:
                    Z = [z for z in range(n) if iv[a][1] < iv[z][0] <= iv[a2][1]]
                    if sorted(Z) == sorted(A):
                        lam1 = lin_add((1, before(a, a2)), (-1, {b: 1}))
                        M.add(lin_add((1, {j: 1}), (-1, lam1)), '<=', 0)                   # both between <= L1
                        M.add(lin_add((1, {b: 1}), (-1, {j: 1}), (-1, lam1)), '<=', 0)     # exactly one <= L1
            else:
                M.add(lin_add((1, {b: 1}), *[(-1, e) for e in evs]), '<=', 0)
        done = set()
        for (a, a2) in Bv:
            if (a2, a) in done: continue
            done.add((a, a2))
            M.add(lin_add((1, {Bv[(a, a2)]: 1}), (-1, {Bv[(a2, a)]: 1}), (-1, before(a, a2)), (1, before(a2, a))), '=', 0)
    if 'T2' in tools:
        dn = [frozenset(w for w in range(n) if lt(iv, w, v)) for v in range(n)]
        up = [frozenset(w for w in range(n) if lt(iv, v, w)) for v in range(n)]
        for dual in (False, True):
            D = up if dual else dn; U = dn if dual else up
            bef = (lambda y, z: before(z, y)) if dual else before
            for x in range(n):
                for b in range(n):
                    if not inc(iv, x, b) or not D[x] <= D[b]: continue
                    W = ({b} | U[b]) - U[x] - {x}
                    chain = [b]; rest = set(W) - {b}
                    while rest:
                        mins = [w for w in rest if not any((w in U[v]) for v in rest if v != w)]
                        if len(mins) != 1: break
                        chain.append(mins[0]); rest.discard(mins[0])
                    full = not rest
                    cum = [bef(x, bi) for bi in chain]
                    steps = [cum[0]] + [lin_add((1, cum[i]), (-1, cum[i - 1])) for i in range(1, len(cum))]
                    if full: steps.append(lin_add((1, {None: 1}), (-1, cum[-1])))
                    for i in range(1, len(steps)):
                        M.add(lin_add((1, steps[i]), (-1, steps[i - 1])), '<=', 0)
                    if len(steps) >= 2 and D[x] == D[b] and U[x] <= U[b]:
                        M.add(lin_add((1, steps[1]), (-1, steps[0])), '=', 0)
    return M, eps

def check(iv, L, tools):
    M, eps = build(iv, L, tools)
    st, val, x = xlp.solve(M.nv, M.rows, {eps: 1})
    return (None if st == 'infeasible' else val), M

def bad_L_for(iv, rule='K'):
    import kprime
    return kprime.bad_L(iv, kprime.step_table(iv), rule)

if __name__ == '__main__':
    O9a = [(1, 1), (1, 2), (1, 5), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 6)]
    L9a = [(1, 1), (1, 2), (2, 3), (1, 5), (3, 4), (2, 6), (4, 5), (5, 6), (6, 6)]
    O9b = [(1, 1), (1, 2), (2, 3), (2, 6), (3, 4), (4, 5), (5, 6), (6, 7), (7, 7)]
    L9b = [(1, 1), (1, 2), (2, 3), (3, 4), (2, 6), (4, 5), (5, 6), (6, 7), (7, 7)]
    P5 = [(1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]
    cases = [('O9a', O9a, L9a), ('O9b', O9b, L9b)]
    # CONTROL: the canonical (l,r) order of O9a / P5 is K-good (has a step with |S|<=1): T1 must refute it
    cases += [('control O9a lex', O9a, sorted(O9a)), ('control P5 lex', P5, sorted(P5))]
    for name, iv, Lint in cases:
        used = set(); L = []
        for t in Lint:
            i = next(j for j in range(len(iv)) if iv[j] == t and j not in used); used.add(j := i); L.append(i)
        for tools in (('T1',), ('T1', 'T3'), ('T1', 'T2'), ('T1', 'T2', 'T3')):
            v, M = check(iv, L, tools)
            print(f"{name:18s} tools {'+'.join(tools):10s}: " +
                  ("INFEASIBLE (L refuted)" if v is None else f"max eps = {v} ({float(v):+.5f}) -> {'refuted' if v <= 0 else 'NOT refuted'}")
                  + f"   [{M.nv} vars, {len(M.rows)} rows]")
            sys.stdout.flush()
