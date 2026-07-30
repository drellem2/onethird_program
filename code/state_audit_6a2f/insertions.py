#!/usr/bin/env python3
"""
mg-6a2f part 3 — INSERTIONS, computed the other way round.

Part 1 decomposed BASELINE -> after-corpus and found 0 lost.  This decomposes
AFTER-CORPUS -> baseline: every token run in the after corpus that does NOT occur
anywhere in the baseline STATE.md is NEW TEXT.  Contiguous new tokens are grouped
into inserted spans and printed in full, per file / per cell.

This is the only mechanical way to enumerate "what did it add beyond its brief",
and it also surfaces paraphrase: if a relocated passage had been reworded, the
reworded words would appear here as an insertion sitting inside otherwise-verbatim
material.
"""
import re, subprocess, collections
BEFORE_REV="97cb533"; AFTER_REV="57f962f"
def show(rev,p): return subprocess.run(["git","show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout
def ls(rev,p):
    return [l for l in subprocess.run(["git","ls-tree","-r","--name-only",rev,p],
            capture_output=True,text=True,check=True).stdout.split("\n") if l.strip()]
before=show(BEFORE_REV,"STATE.md"); after=show(AFTER_REV,"STATE.md")
hist={p:show(AFTER_REV,p) for p in ls(AFTER_REV,"docs/state-history")}
bl=before.split("\n"); al=after.split("\n")
changed=[i for i in range(len(bl)) if bl[i]!=al[i]]
CS=re.compile(r'(?<!\\)\|')
def cells(line):
    p=CS.split(line)
    if p and p[0].strip()=="":p=p[1:]
    if p and p[-1].strip()=="":p=p[:-1]
    return [x.strip() for x in p]

btok=before.split()
pos=collections.defaultdict(list)
for i,t in enumerate(btok): pos[t].append(i)
def longest(seq,i):
    st=pos.get(seq[i])
    if not st: return 0
    best=0
    for s in st:
        L=1
        while i+L<len(seq) and s+L<len(btok) and btok[s+L]==seq[i+L]: L+=1
        best=max(best,L)
        if i+best>=len(seq): break
    return best

def insertions(text):
    seq=text.split(); out=[]; i=0; cur=[]
    while i<len(seq):
        L=longest(seq,i)
        if L==0:
            cur.append(seq[i]); i+=1
        else:
            if cur: out.append(" ".join(cur)); cur=[]
            i+=L
    if cur: out.append(" ".join(cur))
    return out

total=0
print("="*78); print("INSERTED SPANS IN THE REWRITTEN STATE.md CELLS")
print("="*78)
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    ins=insertions(ac[dc])
    print(f"\n--- STATE.md:{i+1} col{dc}   {len(ins)} inserted span(s)")
    for s in ins: print("   + "+s); total+=len(s.split())
print("\n"+"="*78); print("INSERTED SPANS IN THE HISTORY FILES")
print("="*78)
for p,txt in sorted(hist.items()):
    ins=insertions(txt)
    print(f"\n--- {p}   {len(ins)} inserted span(s)")
    for s in ins: print("   + "+s); total+=len(s.split())
print(f"\nTOTAL inserted tokens across the whole change: {total}")
