#!/usr/bin/env python3
"""indep_f889.py (mg-f889) -- INDEPENDENT re-implementation for the audit of mg-6b81 (KSBFT-M).
Shares no code with pcert.c / onept.c. Written from the statements in docs/KSBFT-M-margin-induction.md.

Poset on 0..t-1, naturally labelled (a <_Q b => a < b); dn[b] = bitmask of elements strictly below b
(transitively closed).  Canonical form = lexicographically least tuple of down-rows over ALL natural
labellings (linear extensions), computed level by level (exact; an isomorphism invariant, and it
determines the poset).  Counts: DP over order ideals, exact integers; margins: fractions.Fraction.

Modes:
  gen D TMAX                 pruned generator: non-CUT classes of range<=D, sizes 1..TMAX (my own);
                             prints counts per size; writes lists to $OUT/cD_t.txt if OUT set
  cert D T [s]               certificate over every class of cD_T.txt: #fail, worst max_s rm, per-s
  base D NMAX                delta-1/3 over indecomposable non-chains of range<=D, n<=NMAX (from lists)
  e2e D T N SEEDS            random indecomposable P in Pi_D of size N, every size-T prefix ideal Q:
                             Theorem 2.4 checked against directly counted p_P; OFF control s=T-D+1
  sample D T FILE K SEED     certify a random sample of K classes from a pcert list FILE (hex rows)
"""
import sys, os, random
from fractions import Fraction as F

THIRD = F(os.environ.get('AUDIT_LO','1/3'))   # firing control: AUDIT_LO=2/5 narrows the interval
TWOTHIRD = 1-THIRD
BROKEN_CANON = os.environ.get('AUDIT_BROKEN_CANON')=='1'  # firing control: canon from ONE labelling only
def dist(p): return min(p-THIRD, TWOTHIRD-p)

def popc(x): return bin(x).count('1')

def ideals(dn, U):
    """all order ideals of the induced poset on U (bitmask)"""
    seen={0}; out=[0]; i=0
    while i<len(out):
        I=out[i]; i+=1
        av=U&~I
        while av:
            b=av&-av; x=b.bit_length()-1; av^=b
            if dn[x]&U&~I==0:
                J=I|b
                if J not in seen: seen.add(J); out.append(J)
    return out

def ups(dn,t):
    up=[0]*t
    for b in range(t):
        m=dn[b]
        while m:
            l=m&-m; a=l.bit_length()-1; m^=l; up[a]|=1<<b
    return up

def incomp(dn,t):
    up=ups(dn,t); full=(1<<t)-1
    return [full&~dn[i]&~up[i]&~(1<<i) for i in range(t)]

def rng(dn,t): return max((popc(m) for m in incomp(dn,t)), default=0)

def count_dp(dn, t, idl, x=None, y=None):
    """f[I] = # linear extensions of the induced poset on I (I an ideal), optionally with x before y"""
    up=ups(dn,t)
    f={}
    for I in sorted(idl, key=popc):
        if I==0: f[I]=1; continue
        if x is not None and (I>>y&1) and not (I>>x&1): f[I]=0; continue
        s=0; m=I
        while m:
            l=m&-m; a=l.bit_length()-1; m^=l
            if up[a]&I==0: s+=f[I^l]
        f[I]=s
    return f

def canon(dn,t):
    """lexicographically least down-row tuple over all natural labellings"""
    if BROKEN_CANON:   # NOT an invariant: the input labelling's own rows
        return tuple(dn)
    front=[(0, {})]   # (placed mask, pos map old->new)
    code=[]
    for k in range(t):
        best=None; nxt=[]
        for placed,pos in front:
            av=((1<<t)-1)&~placed
            while av:
                l=av&-av; c=l.bit_length()-1; av^=l
                if dn[c]&~placed: continue
                row=0; m=dn[c]
                while m:
                    b=m&-m; a=b.bit_length()-1; m^=b; row|=1<<pos[a]
                if best is None or row<best: best=row; nxt=[(placed,pos,c)]
                elif row==best: nxt.append((placed,pos,c))
        code.append(best)
        front=[]
        for placed,pos,c in nxt:
            p2=dict(pos); p2[c]=k; front.append((placed|1<<c,p2))
        # dedup frontier states that are identical as (placed,pos)
        if len(front)>1:
            u={}
            for pl,ps in front: u[(pl,tuple(sorted(ps.items())))]=(pl,ps)
            front=list(u.values())
    return tuple(code)

def is_cut(dn,t,D,idl=None):
    if idl is None: idl=ideals(dn,(1<<t)-1)
    full=(1<<t)-1
    for I in idl:
        k=popc(I)
        if k<1 or k>t-2*D+1: continue
        rest=full&~I; ok=True
        while rest:
            l=rest&-rest; b=l.bit_length()-1; rest^=l
            if dn[b]&I!=I: ok=False; break
        if ok: return True
    return False

def gen(D,TMAX,out=None,prune=True):
    lists={0:[()]}
    for t in range(1,TMAX+1):
        seen=set(); res=[]
        for q in lists[t-1]:
            dn=list(q); m=t-1
            for I in ideals(dn,(1<<m)-1):
                d2=dn+[I]
                if rng(d2,t)>D: continue
                if prune and is_cut(d2,t,D): continue
                c=canon(d2,t)
                if c not in seen: seen.add(c); res.append(c)
        lists[t]=res
        if prune: print(f"gen D={D} t={t} nonCUT-classes={len(res)}", flush=True)
        else: print(f"full D={D} t={t} classes={len(res)} nonCUT={sum(1 for c in res if not is_cut(list(c),t,D))}", flush=True)
        if out and prune:
            with open(os.path.join(out,f"c{D}_{t}.txt"),'w') as fo:
                for c in res: fo.write(f"{t} "+" ".join('%x'%r for r in c)+"\n")
    return lists

def cert_one(dn,t,D,only_s=None):
    """returns (best rm over s, {s: rm(Q,s)})"""
    full=(1<<t)-1; idl=ideals(dn,full); inc=incomp(dn,t)
    per={}
    for s in range(t-D,1,-1):
        if only_s is not None and s!=only_s: continue
        Js=[I for I in idl if popc(I)==s]
        if not Js: continue
        K=full
        for J in Js: K&=J
        pairs=[(x,y) for x in range(t) if K>>x&1 for y in range(x+1,t) if (K>>y&1) and (inc[x]>>y&1)]
        if not pairs: continue
        f=count_dp(dn,t,idl)
        best=None
        for x,y in pairs:
            g=count_dp(dn,t,idl,x,y)
            mn=min(dist(F(g[J],f[J])) for J in Js)
            if best is None or mn>best: best=mn
        per[s]=best
    b=max(per.values()) if per else None
    return b,per

def read_list(path):
    L=[]
    with open(path) as fi:
        for line in fi:
            a=line.split(); t=int(a[0]); L.append(tuple(int(h,16) for h in a[1:1+t]))
    return L

def indecomposable(dn,t):
    inc=incomp(dn,t); seen=1; st=[0]
    while st:
        a=st.pop(); m=inc[a]&~seen; seen|=m
        while m:
            l=m&-m; st.append(l.bit_length()-1); m^=l
    return seen==(1<<t)-1

def delta_margin(dn,t):
    full=(1<<t)-1; idl=ideals(dn,full); inc=incomp(dn,t); f=count_dp(dn,t,idl); e=f[full]
    b=None
    for x in range(t):
        for y in range(x+1,t):
            if inc[x]>>y&1:
                d=dist(F(count_dp(dn,t,idl,x,y)[full],e))
                if b is None or d>b: b=d
    return b

def main():
    mode=sys.argv[1]; out=os.environ.get('OUT')
    if mode=='gen':
        gen(int(sys.argv[2]),int(sys.argv[3]),out)
    elif mode=='full':   # UNPRUNED census of range<=D (hereditary under deleting a maximal element), CUT counted after
        gen(int(sys.argv[2]),int(sys.argv[3]),None,prune=False)
    elif mode=='cert':
        D,T=int(sys.argv[2]),int(sys.argv[3]); only=int(sys.argv[4]) if len(sys.argv)>4 else None
        L=read_list(os.path.join(out,f"c{D}_{T}.txt"))
        fail=0; worst=None; wq=None; ats={}
        for q in L:
            b,per=cert_one(list(q),T,D,only)
            if b is None or b<0: fail+=1
            if worst is None or (b is not None and b<worst): worst=b; wq=q
            for s,v in per.items():
                ok=v>=0; ats.setdefault(s,[0,None]); ats[s][0]+=ok
                if ats[s][1] is None or v<ats[s][1]: ats[s][1]=v
        print(f"cert D={D} t={T}{' s='+str(only) if only else ''}: classes={len(L)} uncertified={fail} worst(max_s rm)={worst} Q={' '.join('%x'%r for r in wq)}")
        for s in sorted(ats): print(f"   s={s}: certified-at-s={ats[s][0]} worst rm(Q,s)={ats[s][1]}")
    elif mode=='base':
        D,NMAX=int(sys.argv[2]),int(sys.argv[3]); tot=0; allmin=None
        for t in range(2,NMAX+1):
            L=read_list(os.path.join(out,f"c{D}_{t}.txt"))
            byp={}
            for q in L:
                dn=list(q)
                if not indecomposable(dn,t): continue
                p=rng(dn,t); m=delta_margin(dn,t); byp.setdefault(p,[0,None,None])
                byp[p][0]+=1
                if byp[p][1] is None or m<byp[p][1]: byp[p][1]=m; byp[p][2]=q
                if m<0: print("  NEGATIVE", t, q)
                if m==0: print(f"  ZERO margin: n={t} P={' '.join('%x'%r for r in q)}")
            n_ind=sum(v[0] for v in byp.values()); tot+=n_ind
            print(f"base D={D} n={t} indec={n_ind} " + "  ".join(f"pi={p}:{v[0]} min={v[1]}" for p,v in sorted(byp.items())), flush=True)
        print(f"base D={D} total indecomposable n=2..{NMAX}: {tot}")
    elif mode=='e2e':
        D,T,N,SEEDS,OFF=int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
        viol=bad=nP=nQ=cert=0; minslack=None
        for seed in range(SEEDS):
            rnd=random.Random(seed)
            while True:  # random indecomposable P in Pi_D, grown by maximal elements
                dn=[]
                for t in range(1,N+1):
                    opts=[I for I in ideals(dn,(1<<(t-1))-1) if rng(dn+[I],t)<=D]
                    # bias toward large down-sets so P stays long, not an antichain-like blob
                    opts.sort(key=popc); dn=dn+[rnd.choice(opts[-8:])]
                if indecomposable(dn,N) and rng(dn,N)<=D: break
            nP+=1; full=(1<<N)-1; idlP=ideals(dn,full); fP=count_dp(dn,N,idlP); eP=fP[full]
            for Q in [I for I in idlP if popc(I)==T]:
                nQ+=1
                # relabel Q as a naturally labelled poset on 0..T-1
                el=[i for i in range(N) if Q>>i&1]; ix={e:k for k,e in enumerate(el)}
                dq=[sum(1<<ix[a] for a in range(N) if dn[e]>>a&1) for e in el]
                s=T-D+OFF
                idq=ideals(dq,(1<<T)-1); Js=[I for I in idq if popc(I)==s]
                # the size-s ideals of P, for the bracket check
                JsP=[I for I in idlP if popc(I)==s]
                K=(1<<T)-1
                for J in Js: K&=J
                incq=incomp(dq,T); f=count_dp(dq,T,idq)
                for x in range(T):
                    for y in range(x+1,T):
                        if not((K>>x&1) and (K>>y&1) and (incq[x]>>y&1)): continue
                        g=count_dp(dq,T,idq,x,y); ps=[F(g[J],f[J]) for J in Js]
                        pP=F(count_dp(dn,N,idlP,el[x],el[y])[full],eP)
                        if not(min(ps)<=pP<=max(ps)): viol+=1
                        rm=min(dist(p) for p in ps)
                        if rm>=0:
                            cert+=1
                            if dist(pP)<rm: bad+=1
                            sl=dist(pP)-rm
                            if minslack is None or sl<minslack: minslack=sl
                if OFF==0 and len(JsP)!=len(Js): print("  LEMMA 2.2 COUNT MISMATCH", len(JsP), len(Js))
        print(f"e2e D={D} t={T} N={N} OFF={OFF}: P={nP} Q={nQ} bracket-violations={viol} certified-pairs={cert} certified-but-dist(pP)<rm={bad} min(dist(pP)-rm)={minslack}")
    elif mode=='sample':
        D,T,path,K,SEED=int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],int(sys.argv[5]),int(sys.argv[6])
        L=read_list(path); rnd=random.Random(SEED); S=rnd.sample(range(len(L)),min(K,len(L)))
        fail=0; worst=None; ncut=0; mism=0; nind=0; dmin=None; canons=set()
        for i in S:
            dn=list(L[i]); canons.add(canon(dn,T))
            if indecomposable(dn,T):
                nind+=1; m=delta_margin(dn,T)
                if dmin is None or m<dmin: dmin=m
            if rng(dn,T)>D: mism+=1
            if is_cut(dn,T,D): ncut+=1
            b,_=cert_one(dn,T,D)
            if b is None or b<0: fail+=1
            if worst is None or (b is not None and b<worst): worst=b
        print(f"sample D={D} t={T} from {len(L)} classes: sampled={len(S)} range>D={mism} CUT={ncut} uncertified={fail} worst(max_s rm)={worst} distinct-canon={len(canons)} indecomposable={nind} min(delta-1/3)={dmin}")
main()
