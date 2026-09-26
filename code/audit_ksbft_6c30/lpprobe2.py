"""lpprobe2.py (audit mg-6c30): is Thm 3.1 (as a LINEAR inequality, unconditional form, every triple
a||c||b, no L needed) implied by the author's LP rows?  The LP bounds B(a,c) by the SUM of its separator
events and bounds each shared event separately by B(b,c); Thm 3.1's proof needs P(union of shared events)
<= B(b,c), which is not a sum of the LP rows when two or more events are shared.  Adds, for every such
triple, the proven row
  sum_{A(a,c)-A(b,c)} P[z<c] + sum_{B(a,c)} P[a<w] + sum_{B(c,b)-B(c,a)} P[c<w] + sum_{A(c,b)} P[z<b]
      >= (P[a<c]-P[c<a]) + (P[c<b]-P[b<c])
and re-solves Q12 (author's builder and exact simplex, read-only)."""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'ksbft_t2_two_separator_561a'))
import lpcheck, xlp
from lpcheck import lin_add
from t2lib import lt
sys.path.insert(0, HERE)
from eng import Poset
from lpprobe import SURV, idx

which = sys.argv[1:] or ['Q12']
for name, iv, Lint in SURV:
    if name not in which: continue
    L = idx(iv, Lint); n = len(iv); pos = {v: i for i, v in enumerate(L)}; P = Poset.from_iv(tuple(iv))
    for tools in (('T1',), ('T1', 'T2', 'T3')):
        M, eps = lpcheck.build(iv, L, tools)
        def before(y, z):
            if lt(iv, y, z): return {None: 1}
            if lt(iv, z, y): return {None: 0}
            return {M.names.index(f'x{iv[z]}{iv[y]}'): 1} if pos[z] < pos[y] else {None: 1, M.names.index(f'x{iv[y]}{iv[z]}'): -1}
        added = 0; shared2 = 0
        for a in range(n):
            for c in range(n):
                if not P.inc[a][c]: continue
                for b in range(n):
                    if b == a or not P.inc[c][b]: continue
                    shared2 += (len(P.A(a, c) & P.A(b, c)) >= 2 or len(P.B(c, b) & P.B(c, a)) >= 2)
                    lhs = lin_add(*[(1, before(z, c)) for z in P.A(a, c) - P.A(b, c)],
                                  *[(1, before(a, w)) for w in P.B(a, c)],
                                  *[(1, before(c, w)) for w in P.B(c, b) - P.B(c, a)],
                                  *[(1, before(z, b)) for z in P.A(c, b)])
                    rhs = lin_add((1, before(a, c)), (-1, before(c, a)), (1, before(c, b)), (-1, before(b, c)))
                    row = lin_add((1, lhs), (-1, rhs))
                    if all(k is None for k in row): continue
                    M.add(row, '>=', 0); added += 1
        st, v, _ = xlp.solve(M.nv, M.rows, {eps: 1})
        print(f"{name} tools {'+'.join(tools):9s} + {added} Thm-3.1 rows ({shared2} triples share >=2 events): eps* = {v}", flush=True)
