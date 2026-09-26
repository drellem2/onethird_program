"""classify_pi2_95d3.py (mg-95d3): check Lemma 4.2 of KSBFT-J on the independent generator's output.
For every indecomposable class of range <= 2 with 3 <= n <= NMAX, test whether it is A3, 2+2 or F_n
(x_i < x_j iff j - i >= 2) by an explicit isomorphism search.  Prints per-n counts and any poset that
is none of the three (Lemma 4.2 predicts: none).  Control: the same test on range <= 3 must report
posets that are none of the three (it FIRES)."""
import sys, itertools
def read(fn):
    for line in open(fn):
        t=line.split(); n=int(t[0]); yield n,[int(x,16) for x in t[1:]]
def rel(n,dn):
    return {(j,i) for i in range(n) for j in range(n) if dn[i]>>j&1}   # (j,i): j < i
def inc_graph(n,R):
    return {i:{j for j in range(n) if j!=i and (i,j) not in R and (j,i) not in R} for i in range(n)}
def connected(n,G):
    seen={0}; st=[0]
    while st:
        v=st.pop()
        for u in G[v]:
            if u not in seen: seen.add(u); st.append(u)
    return len(seen)==n
def fib(n): return {(i,j) for i in range(n) for j in range(n) if j-i>=2}
A3={}; TWO2={(0,1),(2,3)}
def iso_to(n,R,T):
    if len(R)!=len(T): return False
    # small n: use degree-guided search over permutations of the incomparability path
    for p in itertools.permutations(range(n)) if n<=8 else []:
        if all(((p[a],p[b]) in R) for (a,b) in T): return True
    return False
def is_fib(n,R,G):
    # G must be a path; walk it from an endpoint and test both orientations
    ends=[v for v in G if len(G[v])==1]
    if n>=3 and (len(ends)!=2 or any(len(G[v])>2 for v in G)): return False
    order=[ends[0]]; prev=None
    while len(order)<n:
        nxt=[u for u in G[order[-1]] if u!=prev]
        if not nxt: return False
        prev=order[-1]; order.append(nxt[0])
    F=fib(n)
    for o in (order, order[::-1]):
        if {(o[a],o[b]) for (a,b) in F}==R: return True
    return False
def run(prefix,nmax,label):
    tot_other=0
    for n in range(3,nmax+1):
        cnt={'A3':0,'2+2':0,'F_n':0,'other':0}
        for m,dn in read(f"{prefix}{n}.txt"):
            R=rel(m,dn); G=inc_graph(m,R)
            if not any(G[v] for v in G) or not connected(m,G): continue
            if m==3 and len(R)==0: cnt['A3']+=1
            elif m==4 and iso_to(4,R,TWO2): cnt['2+2']+=1
            elif is_fib(m,R,G): cnt['F_n']+=1
            else: cnt['other']+=1
        tot_other+=cnt['other']
        print(f"{label} n={n}: indecomposable classes by type {cnt}")
    return tot_other
o2=run(sys.argv[1],int(sys.argv[2]),"range<=2")
print(f"range<=2: posets that are none of A3, 2+2, F_n: {o2} (Lemma 4.2 predicts 0)")
o3=run(sys.argv[3],int(sys.argv[4]),"CONTROL range<=3")
print(f"CONTROL range<=3: 'other' count {o3} -> {'FIRES' if o3>0 else 'DOES NOT FIRE (instrument broken)'}")
