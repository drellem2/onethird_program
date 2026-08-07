from fractions import Fraction as F
from itertools import combinations
# 3-atom fence on the consecutive-pairs branch: verify (n-1)/3 for n=3..20 from scratch
for n in range(3,21):
    I={(i,i+1) for i in range(n-1)}
    ident=tuple(range(n))
    def matching(par):
        s=list(range(n))
        for k in range(par,n-1,2): s[k],s[k+1]=s[k+1],s[k]
        return tuple(s)
    atoms=[ident,matching(0),matching(1)]; m=F(1,3)
    flip={p:F(0) for p in combinations(range(n),2)}; E=F(0)
    for s in atoms:
        P={v:i for i,v in enumerate(s)}; k=0
        for (a,b) in combinations(range(n),2):
            if P[a]>P[b]:
                flip[(a,b)]+=m
                if (a,b) in I: k+=1
        E+=m*k
    bad_comp=[p for p in flip if p not in I and flip[p]>0]
    maxflip=max(flip.values())
    viol=0
    for (x,y) in I:
        for k in range(n-1):
            if sum(m for s in atoms if s[k]==x and s[k+1]==y)!=sum(m for s in atoms if s[k]==y and s[k+1]==x): viol+=1
    ok = (E==F(n-1,3)) and maxflip<=F(1,3) and not bad_comp and viol==0
    if n in (3,6,12,20) or not ok:
        print(f"n={n:2d} E[inv]={E}  (n-1)/3={F(n-1,3)}  maxflip={maxflip}  comparable-flipped={len(bad_comp)}  perslot-viol={viol}  OK={ok}")
    assert ok, n
print("ALL n=3..20: fence attains (n-1)/3, feasible, per-slot symmetric, no comparable pair flipped")
