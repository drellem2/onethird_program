"""lpprobe.py (audit mg-6c30): scope probe of mg-561a sec.4 ('13 survivors stay LP-feasible; no linear
combination of the listed lemmas refutes Q12').  Uses the AUTHOR's LP builder read-only (lpcheck.build,
exact simplex xlp) -- this is NOT an independent re-derivation of eps*; it re-runs Q12 and the second n=12
survivor, then ADDS the distribution-free 3-cycle inequalities 1 <= P[u<v]+P[v<w]+P[w<u] <= 2 for every
triple (true for any probability measure on linear extensions), and reports whether eps* moves.
Also re-reads each survivor with this audit's own engine: dominance-respecting, K-bad, no TS/2.1*/3.1* kill."""
import sys, os, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ksbft_t2_two_separator_561a'))
import lpcheck, xlp
from lpcheck import lin_add
from t2lib import lt, inc
sys.path.insert(0, HERE)
from eng import Poset
from badl import kills, need_masks, kvec

SURV = [
 ('Q12', [(1,1),(1,2),(2,3),(2,5),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)],
         [(1,1),(1,2),(2,3),(3,4),(2,5),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)]),
 ('S12b', [(1,1),(1,2),(1,5),(2,3),(2,7),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,8)],
          [(1,1),(1,2),(2,3),(3,4),(1,5),(2,7),(4,5),(5,6),(5,8),(6,7),(7,8),(8,8)]),
 ('S12a', [(1,1),(1,2),(1,4),(2,3),(2,7),(3,4),(4,5),(4,8),(5,6),(6,7),(7,8),(8,8)],
          [(1,1),(1,2),(2,3),(1,4),(3,4),(4,5),(2,7),(4,8),(5,6),(6,7),(7,8),(8,8)]),
]

def idx(iv, Lint):
    used = set(); L = []
    for t in Lint:
        i = next(j for j in range(len(iv)) if iv[j] == t and j not in used); used.add(i); L.append(i)
    return L

def own_check(iv, L):
    P = Poset.from_iv(tuple(iv)); n = P.n; pos = {v: i for i, v in enumerate(L)}
    need = need_masks(P)
    dom_ok = all((need[v] >> w) & 1 == 0 or pos[w] < pos[v] for v in range(n) for w in range(n))
    kbad = all(not P.inc[L[i]][L[i+1]] or len(P.S(L[i], L[i+1])) >= 2 for i in range(n - 1))
    steps = []
    for i in range(n - 1):
        a, b = L[i], L[i+1]
        if P.inc[a][b]:
            (la, ra), (lb, rb) = iv[a], iv[b]
            sh = 'CONT' if (lb < la and ra < rb) or (la < lb and rb < ra) else 'DOM'
            steps.append((iv[a], iv[b], sh, len(P.A(a, b)), len(P.B(a, b))))
    ks = [(iv[L[i+1]], len(kvec(P, L[i], L[i+1], L[i+2]))) for i in range(n - 2)
          if P.inc[L[i]][L[i+1]] and P.inc[L[i+1]][L[i+2]]]
    lemmaC = [s for s in steps if s[2] == 'CONT' and s[3] + s[4] == 2]
    return dom_ok, kbad, sorted(kills(P, L)), steps, ks, lemmaC

if __name__ == '__main__':
    which = sys.argv[1:] or ['Q12']
    for name, iv, Lint in SURV:
        if name not in which: continue
        L = idx(iv, Lint)
        dom_ok, kbad, kl, steps, ks, lemmaC = own_check(iv, L)
        print(f"{name}: dominance-respecting={dom_ok} K-bad={kbad} own-engine kills={kl}")
        print(f"   steps (a, a', shape, |A|, |B|): {steps}")
        print(f"   consecutive-triple k (centre, k): {ks}")
        print(f"   Lemma C targets (containment step, |S|=2): {lemmaC}")
        n = len(iv); pos = {v: i for i, v in enumerate(L)}
        for tools in (('T1',), ('T1', 'T2', 'T3')):
            M, eps = lpcheck.build(iv, L, tools)
            st, v0, _ = xlp.solve(M.nv, M.rows, {eps: 1})
            # add 3-cycle rows
            before = lambda y, z: ({None: 1} if lt(iv, y, z) else {None: 0} if lt(iv, z, y) else
                                   next(({M.names.index(f'x{iv[z]}{iv[y]}'): 1} if pos[z] < pos[y] else
                                         {None: 1, M.names.index(f'x{iv[y]}{iv[z]}'): -1}) for _ in [0]))
            added = 0
            for u, v, w in itertools.permutations(range(n), 3):
                if u > v or u > w: continue
                s = lin_add((1, before(u, v)), (1, before(v, w)), (1, before(w, u)))
                c = s.get(None, 0)
                if all(k is None for k in s): continue
                M.add(dict(s), '<=', 2); M.add(dict(s), '>=', 1); added += 2
            st1, v1, _ = xlp.solve(M.nv, M.rows, {eps: 1})
            print(f"   tools {'+'.join(tools):9s}: eps* = {v0}  | +{added} 3-cycle rows: eps* = {v1}", flush=True)
