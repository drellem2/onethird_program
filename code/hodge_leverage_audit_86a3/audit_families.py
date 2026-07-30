"""§5.3's two width-2 families, reproduced independently (claim M3)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_core import P0, linexts, facet_of, at_graph
from audit_sweep import gammas, lg_bound, lambda2_at
def chains2(a):  # C_a + C_a : two disjoint chains of length a
    lt=set()
    for i in range(a):
        for j in range(i+1,a): lt.add((i,j)); lt.add((a+i,a+j))
    return P0(2*a,lt)
def fence(n):  # 0<1>2<3>4...
    lt=set()
    for i in range(n-1):
        if i%2==0: lt.add((i,i+1))
        else: lt.add((i+1,i))
    return P0(n,lt)
memo={}
print("C_a + C_a")
for a in (1,2,3,4):
    P=chains2(a); les=linexts(P); f=[facet_of(P,w) for w in les]
    g=gammas(P,f,memo); b=lg_bound(g); t=lambda2_at(P)
    gv=[g[i] for i in sorted(g) if g[i] is not None]
    print("  n=%d |L|=%3d gamma=%s bound=%.6f truth=%.6f ratio=%.2f"%(P.n,len(les),",".join("%.3f"%x for x in gv),b,t,t/b))
print("fences")
for n in (3,4,5,6,7):
    P=fence(n); les=linexts(P); f=[facet_of(P,w) for w in les]
    g=gammas(P,f,memo); b=lg_bound(g); t=lambda2_at(P)
    gv=[g[i] for i in sorted(g) if g[i] is not None]
    print("  n=%d |L|=%3d gamma=%s bound=%.6f truth=%.6f ratio=%.2f"%(n,len(les),",".join("%.3f"%x for x in gv),b,t,t/b))
