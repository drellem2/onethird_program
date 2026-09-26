"""reduction.py (audit mg-6e7c): mg-ce69 Lemma 1.1 reading 'the Y-gadget is O1 in R = P - C, so items 1 and 3 are
one question'.  The reduction is exact for x-pairs (window shifted).  For the twin pair (u,v) the law in P is a
MIXTURE of P_R and P_{P - (C_i u x)} laws, so balance of (u,v) in R need not be balance in P.  Count gadgets
(n <= 8, connected) where the balanced status of some pair of U differs between P and R."""
import sys
from fractions import Fraction as F
from aud import close, conn, ups, incp, probs, chainbot, T1, T2
from census import restrict
diff = gad = 0; ex = None
for f in sys.argv[1:]:
    for line in open(f):
        a = line.split(); n = int(a[0])
        if n < 3: continue
        dn = close([int(t, 16) for t in a[1:1 + n]])
        if not conn(dn): continue
        up = ups(dn); e, B = probs(dn)
        for x in range(n):
            if dn[x]: continue
            Z = [z for z in range(n) if incp(dn, up, x, z)]
            C, full = chainbot(dn, Z)
            if not C or full: continue
            rest = [z for z in Z if z not in C]
            U = [v for v in rest if not any(dn[v] >> w & 1 for w in rest if w != v)]
            if len(U) < 2: continue
            gad += 1
            keep = [v for v in range(n) if v not in C]
            R = restrict(dn, keep); eR, BR = probs(R)
            for i in range(len(U)):
                for j in range(i + 1, len(U)):
                    u, v = U[i], U[j]
                    bp = T1 <= F(B[u][v], e) <= T2
                    br = T1 <= F(BR[keep.index(u)][keep.index(v)], eR) <= T2
                    if bp != br:
                        diff += 1
                        if ex is None: ex = (line.strip(), x, u, v, F(B[u][v], e), F(BR[keep.index(u)][keep.index(v)], eR))
print(f"gadgets={gad} twin pairs whose balanced status differs between P and R: {diff}; first example {ex}")
