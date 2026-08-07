from fractions import Fraction as F
from itertools import combinations
n=6
I={(0,1),(1,2),(2,3),(3,4),(4,5),(1,4)}
COMP=[p for p in combinations(range(n),2) if p not in I]
# transitivity of the comparable relation
cs=set(COMP)
trans=all(((a,c) in cs) for a,b in cs for b2,c in cs if b==b2)
print("comparable set transitive:", trans, "| #comparable:", len(cs))
atoms=[(0,1,2,3,5,4),(0,1,3,2,5,4),(0,2,1,4,3,5),(0,2,4,1,3,5),(1,0,2,3,4,5),(1,0,3,2,4,5)]
m=F(1,6)
print("total mass:", sum([m]*6))
def pos(s): return {v:i for i,v in enumerate(s)}
inv_tot=F(0); flip={p:F(0) for p in combinations(range(n),2)}
for s in atoms:
    P=pos(s); k=0
    for (a,b) in combinations(range(n),2):
        if P[a]>P[b]:
            flip[(a,b)]+=m
            if (a,b) in I: k+=1
    inv_tot+=m*k
print("E[inv] =",inv_tot," (n-1)/3 =",F(n-1,3)," eps_spec =",6*inv_tot/(n*n-1)," 2/(n+1) =",F(2,n+1))
print("max flip over I:",max(flip[p] for p in I),"| per-pair:",{p:str(flip[p]) for p in sorted(I)})
print("any comparable pair flipped?:",[p for p in COMP if flip[p]>0])
# per-slot symmetry J_k(x,y)=J_k(y,x): x in slot k, y in slot k+1 vs reversed
viol=0
for (x,y) in combinations(range(n),2):
    if (x,y) not in I: continue
    for k in range(n-1):
        a=sum(m for s in atoms if s[k]==x and s[k+1]==y)
        b=sum(m for s in atoms if s[k]==y and s[k+1]==x)
        if a!=b: viol+=1
print("per-slot adjacency-symmetry violations on incomparable pairs:",viol)
