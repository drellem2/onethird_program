"""sharp_95d3.py (mg-95d3): Lemma R sharpness at pi(v)=1 by an explicit family (PROVEN in AUDIT-mg-eedd.md s.2;
this script is the arithmetic check).  Q(a,b) = chain A (a elements, top x) + chain B (b elements, top z), disjoint.
P(a,b) = Q(a,b) plus v with v > every element except z (so v || z only, pi(v)=1).
Claim: p' = P_Q[x before z] = b/(a+b), p = P_P[x before z] = 2p'/(1+p'), |p-p'| = p'(1-p')/(1+p').
Exact check by an independent ideal DP with Fractions; control: making v > z too (v on top of everything)
must give p = p' (difference 0), i.e. the effect disappears."""
from fractions import Fraction as Fr
from functools import lru_cache
import math
def pr(n, less, x, y):
    """exact P[x before y] under uniform linear extensions; less = set of (a,b) with a<b (transitively closed)"""
    down=[frozenset(a for a in range(n) if (a,b) in less) for b in range(n)]
    full=(1<<n)-1
    @lru_cache(None)
    def cnt(I):          # number of ways to complete from ideal I
        if I==full: return 1
        return sum(cnt(I|1<<e) for e in range(n) if not I>>e&1 and all(I>>d&1 for d in down[e]))
    @lru_cache(None)
    def cntxy(I):        # completions from I in which x comes before y (x,y not in I)
        if I==full: return 0
        s=0
        for e in range(n):
            if I>>e&1 or not all(I>>d&1 for d in down[e]): continue
            if e==x: s+=cnt(I|1<<e)
            elif e==y: pass
            else: s+=cntxy(I|1<<e)
        return s
    return Fr(cntxy(0),cnt(0))
def build(a,b,ctrl=False):
    A=list(range(a)); B=list(range(a,a+b)); v=a+b; less=set()
    for ch in (A,B):
        for i in range(len(ch)):
            for j in range(i+1,len(ch)): less.add((ch[i],ch[j]))
    z=B[-1]
    for e in A+B:
        if e!=z or ctrl: less.add((e,v))
    return a+b+1, less, A[-1], z, v
best=0; bad=0
target=3-2*math.sqrt(2)
for (a,b) in [(1,1),(2,1),(3,2),(4,3),(5,3),(7,5),(10,7),(12,8),(12,9),(17,12)]:
    n,less,x,z,v=build(a,b)
    lessQ={(s,t) for (s,t) in less if v not in (s,t)}
    pq=pr(n-1,lessQ,x,z); pp=pr(n,less,x,z)
    pred_q=Fr(b,a+b); pred_p=2*pred_q/(1+pred_q); d=abs(pp-pq)
    ok = (pq==pred_q and pp==pred_p and d==pred_q*(1-pred_q)/(1+pred_q))
    bad+= not ok
    n2,less2,_,_,_=build(a,b,ctrl=True); pc=pr(n2,less2,x,z)
    print(f"a={a:2d} b={b:2d} n={n:2d}: p'={pq} p={pp} |p-p'|={d} = {float(d):.9f}  formula {'OK' if ok else 'MISMATCH'};"
          f"  control (v above z too): |p-p'|={abs(pc-pq)} {'(0: control behaves)' if pc==pq else '(!!)'}")
print(f"formula mismatches: {bad}; bound 3-2sqrt2 = {target:.9f}; with b/(a+b) -> sqrt2-1 the gap -> bound (PROVEN in the audit)")
# how close along Pell convergents (closed form only, no DP): b/(a+b)=P_k/(P_k+P_{k+1})... use b/(a+b) -> sqrt2-1
for k in range(1,8):
    # sqrt2-1 convergents: 1/2, 2/5, 5/12, 12/29, 29/70 ...
    pell=[0,1]; 
    while len(pell)<k+3: pell.append(2*pell[-1]+pell[-2])
    p1=Fr(pell[k],pell[k+1]); d=p1*(1-p1)/(1+p1)
    print(f"  p'={p1} (a={pell[k+1]-pell[k]}, b={pell[k]}): |p-p'|={d} = {float(d):.12f}, bound-gap={target-float(d):.2e}")
