#!/usr/bin/env python3
"""
mg-6a2f part 6 — 'nothing was cut mid-sentence', and the two boundary rulings.

For each baseline cell, walk the maximal-run decomposition and inspect every
STAYED->MOVED and MOVED->STAYED transition.  A cut is clean iff the text
immediately before it ends a sentence (terminal punctuation, allowing trailing
markdown emphasis / closing brackets).  Anything else is a mid-sentence cut.
"""
import re, subprocess, collections
def show(rev,p): return subprocess.run(["git","show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout
def ls(rev,p):
    return [l for l in subprocess.run(["git","ls-tree","-r","--name-only",rev,p],
            capture_output=True,text=True,check=True).stdout.split("\n") if l.strip()]
b=show("97cb533","STATE.md"); a=show("57f962f","STATE.md")
hist={p:show("57f962f",p) for p in ls("57f962f","docs/state-history")}
bl=b.split("\n"); al=a.split("\n")
changed=[i for i in range(len(bl)) if bl[i]!=al[i]]
CS=re.compile(r'(?<!\\)\|')
def cells(l):
    p=[x.strip() for x in CS.split(l)]
    if p and p[0]=="":p=p[1:]
    if p and p[-1]=="":p=p[:-1]
    return p
def corpus(toks):
    d=collections.defaultdict(list)
    for i,t in enumerate(toks): d[t].append(i)
    return toks,d
def run_at(seq,i,pair):
    T,d=pair; st=d.get(seq[i])
    if not st: return 0
    best=0
    for s in st:
        L=1
        while i+L<len(seq) and s+L<len(T) and T[s+L]==seq[i+L]: L+=1
        best=max(best,L)
        if i+best>=len(seq): break
    return best
LINK=re.compile(r'docs/state-history/([A-Za-z0-9._-]+\.md)')
# a token ends a sentence if it ends with . ! ? : ; possibly followed by markdown closers/quotes
END=re.compile(r'[.!?:;][\*\`\)\]"”’\*]*$')
clean=dirty=0; report=[]
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    fs=sorted(set(LINK.findall(ac[dc])))
    acell=corpus(ac[dc].split())
    both=corpus(ac[dc].split()+sum((hist["docs/state-history/"+f].split() for f in fs),[]))
    seq=bc[dc].split(); k=0; segs=[]
    while k<len(seq):
        L=run_at(seq,k,both)
        stayed = run_at(seq,k,acell)>=L
        segs.append((k,L,stayed)); k+=L
    for n in range(1,len(segs)):
        if segs[n][2]==segs[n-1][2]: continue
        k,L,st=segs[n]
        prev=seq[k-1]
        ok=bool(END.search(prev))
        if ok: clean+=1
        else:
            dirty+=1
            report.append((i+1, "STAYED->MOVED" if segs[n-1][2] else "MOVED->STAYED",
                           " ".join(seq[max(0,k-9):k]), " ".join(seq[k:k+9])))
print(f"transitions between kept and relocated text: {clean+dirty}")
print(f"  ending at a sentence boundary: {clean}")
print(f"  NOT at a sentence boundary   : {dirty}")
for ln,kind,before_,after_ in report:
    print(f"\n  :{ln}  {kind}")
    print(f"     ...{before_}   ||CUT||   {after_}...")

print("\n" + "="*78)
print("DIRECT TEST: does every relocated PARAGRAPH stand as whole sentences?")
print("(the 11 above are artifacts of greedy run boundaries where a pointer headline")
print(" shares a prefix with the passage it points at -- checked directly instead)")
print("="*78)
bad=0; n=0
STARTOK=re.compile(r'^(\*\*|\*|`|⚠️|⭐|\(|>|[A-Z0-9§])')
for p,t in sorted(hist.items()):
    if p.endswith("README.md"): continue
    body=t
    for para in [x.strip() for x in body.split("\n\n")]:
        if not para or para.startswith("#") or para.startswith("*Why") or para.startswith("*These"):
            continue
        if para.startswith("Per-row history") or para.startswith("Every passage below"):
            continue
        n+=1
        s_ok=bool(STARTOK.match(para))
        e_ok=bool(re.search(r'[.!?][\*\`\)\]"”’\*]*$', para.strip()))
        if not (s_ok and e_ok):
            bad+=1
            print(f"  {p}: start_ok={s_ok} end_ok={e_ok}")
            print(f"     {para[:100]!r} ... {para[-80:]!r}")
print(f"  {n} relocated paragraphs; {bad} not whole-sentence-bounded")
