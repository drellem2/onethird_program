"""family_e60e.py (mg-e60e) -- exact check of the audit's sharpness family.
P_k = ({x<z} + {y}) (+) chain c_1<...<c_k above x,y,z, plus one element w
incomparable to everything.  Claim (proved in docs/AUDIT-mg-f218.md sec 3):
(x,y,z) is a Case-D BFT triple, pi(P_k)=pi(w)=k+3=:D, N(x,y)={w}, and
P[f(x)-f(y)>=2] / P[f(y)<f(x)] = 1/(D+1) exactly.
Also the generic (non-BFT) family: chain of k + two isolated points.
Exact Fractions from a down-set DP; no randomness."""
from fractions import Fraction as Fr
import sys
def stats(n, less):   # less: set of (a,b) with a<b, transitively closed
    pred=[0]*n
    for a,b in less: pred[b]|=1<<a
    full=(1<<n)-1; fwd={0:1}; order=sorted(range(full+1),key=lambda s:bin(s).count('1'))
    for S in order:
        if S not in fwd: continue
        for v in range(n):
            if not S>>v&1 and pred[v]&~S==0: fwd[S|1<<v]=fwd.get(S|1<<v,0)+fwd[S]
    bwd={full:1}
    for S in reversed(order):
        if S==full or S not in fwd: continue
        bwd[S]=sum(bwd[S|1<<v] for v in range(n) if not S>>v&1 and pred[v]&~S==0)
    e=fwd[full]
    def H(v): return Fr(sum(fwd[S]*bwd[S|1<<v]*(bin(S).count('1')+1) for S in fwd if not S>>v&1 and pred[v]&~S==0),e)
    def before(a,b): return sum(fwd[S]*bwd[S|1<<a] for S in fwd if not S>>a&1 and not S>>b&1 and pred[a]&~S==0)
    def adj(a,b):
        t=0
        for S in fwd:
            if S>>a&1 or S>>b&1 or pred[a]&~S: continue
            S1=S|1<<a
            if pred[b]&~S1==0: t+=fwd[S]*bwd[S1|1<<b]
        return t
    return e,H,before,adj,pred
def closure(n,rel):
    R=set(rel)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if (i,k) in R and (k,j) in R: R.add((i,j))
    return R
def pi(n,R): return [sum(1 for u in range(n) if u!=v and (u,v) not in R and (v,u) not in R) for v in range(n)]
ok=True
print("BFT family P_k: x=0,z=1,y=2, chain 3..k+2, w=k+3")
for k in range(0,int(sys.argv[1]) if len(sys.argv)>1 else 9):
    n=k+4; x,z,y,w=0,1,2,n-1; ch=list(range(3,3+k))
    rel=[(x,z)]+[(a,c) for c in ch for a in (x,y,z)]+[(ch[i],ch[i+1]) for i in range(k-1)]
    R=closure(n,rel); p_=pi(n,R); D=max(p_)
    e,H,before,adj,_=stats(n,R)
    caseD=(x,z) in R and all((a,b) not in R and (b,a) not in R for a,b in ((x,y),(y,z)))
    bft=H(x)<=H(y)<=H(z)<=H(x)+2
    N=[u for u in range(n) if u not in (x,y) and (u,y) not in R and (x,u) not in R]
    p=Fr(before(y,x),e); gap=p-Fr(adj(y,x),e); r=gap/p
    good=caseD and bft and N==[w] and D==p_[w]==k+3 and r==Fr(1,D+1)
    ok&=good
    print(f" k={k} n={n} D=pi(P)={D} pi(w)={p_[w]} N={N} caseD={caseD} BFT={bft} h=({H(x)},{H(y)},{H(z)}) p={p} ratio={r} 1/(D+1)={Fr(1,D+1)} {'OK' if good else 'FAIL'}")
print("generic family: chain c_0<..<c_{k-1} (x=c_0) + isolated y, w")
for k in range(1,int(sys.argv[1]) if len(sys.argv)>1 else 9):
    n=k+2; x=0; y=k; w=k+1
    R=closure(n,[(i,i+1) for i in range(k-1)]); p_=pi(n,R); D=max(p_)
    e,H,before,adj,_=stats(n,R)
    p=Fr(before(y,x),e); r=(p-Fr(adj(y,x),e))/p
    good = r==Fr(1,D+1); ok&=good
    print(f" k={k} D={D} ratio={r} {'OK' if good else 'FAIL'}")
# negative control: the same checker on P_k WITHOUT w (N(x,y) empty, ratio 0)
# must report failure on every row, else the checker cannot fail.
neg=0
for k in range(0,6):
    n=k+3; x,z,y=0,1,2; ch=list(range(3,3+k))
    rel=[(x,z)]+[(a,c) for c in ch for a in (x,y,z)]+[(ch[i],ch[i+1]) for i in range(k-1)]
    R=closure(n,rel); p_=pi(n,R); D=max(p_)
    e,H,before,adj,_=stats(n,R)
    p=Fr(before(y,x),e); r=(p-Fr(adj(y,x),e))/p
    if r!=Fr(1,D+1): neg+=1
print(f"negative control (w removed): {neg}/6 rows fail the 1/(D+1) check ->", "FIRES" if neg==6 else "SILENT")
ok &= neg==6
print("ALL OK" if ok else "FAILURE"); sys.exit(0 if ok else 1)
