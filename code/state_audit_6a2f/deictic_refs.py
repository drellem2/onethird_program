#!/usr/bin/env python3
"""
mg-6a2f part 5 — DEICTIC REFERENCES BROKEN BY RELOCATION.

A restructure cannot lose a word and still change what the words mean, if the words
include "see below", "the paragraph above", "the same commit", "that row".  Moving a
passage from a table cell into a separate file silently re-points every such phrase.
Token-level completeness is blind to this by construction: the tokens are all there.

For every relocated passage (i.e. every passage now in a history file) and for every
rewritten cell, list the intra-document deictic phrases and say where their referent
now lives.  Adjudication is by hand; this only finds the sites.
"""
import re, subprocess
def show(rev,p): return subprocess.run(["git","show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout
def ls(rev,p):
    return [l for l in subprocess.run(["git","ls-tree","-r","--name-only",rev,p],
            capture_output=True,text=True,check=True).stdout.split("\n") if l.strip()]
a=show("57f962f","STATE.md"); b=show("97cb533","STATE.md")
hist={p:show("57f962f",p) for p in ls("57f962f","docs/state-history")}
al=a.split("\n"); bl=b.split("\n")
changed=[i for i in range(len(bl)) if bl[i]!=al[i]]
CS=re.compile(r'(?<!\\)\|')
def cells(l):
    p=CS.split(l)
    if p and p[0].strip()=="":p=p[1:]
    if p and p[-1].strip()=="":p=p[:-1]
    return [x.strip() for x in p]

DEICTIC = re.compile(
    r'\b(see below|see above|below[,.)]|above[,.)]|the paragraph (above|below)|'
    r'the (row|cell|clause|sentence|line) (above|below)|'
    r'immediately (above|below)|earlier in this (row|cell|document)|'
    r'later in this (row|cell|document)|as (noted|stated|said) (above|below)|'
    r'this row|this cell|that row|the next row|the row below|the row above|'
    r'the same (row|cell)|first item|last item|the previous (row|item))\b', re.I)

def scan(name, txt):
    out=[]
    for m in DEICTIC.finditer(txt):
        s=max(0,m.start()-130); e=min(len(txt),m.end()+130)
        out.append((m.group(0), txt[s:e].replace("\n"," ")))
    if out:
        print(f"\n### {name}   ({len(out)} site(s))")
        for g,c in out: print(f"   [{g}]  ...{c}...")

print("="*78); print("A. deictic phrases in the REWRITTEN cells")
print("="*78)
for i in changed:
    ac=cells(al[i]); bc=cells(bl[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    scan(f"STATE.md:{i+1} (AFTER)", ac[dc])
print("\n"+"="*78); print("B. deictic phrases in the RELOCATED text (history files)")
print("="*78)
for p,t in sorted(hist.items()):
    if p.endswith("README.md"): continue
    scan(p, t)
print("\n"+"="*78)
print("C. for comparison: the same phrases in the BASELINE cells")
print("="*78)
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    n=len(DEICTIC.findall(bc[dc]))
    m=len(DEICTIC.findall(ac[dc]))
    fs=sorted(set(re.findall(r'docs/state-history/([A-Za-z0-9._-]+\.md)', ac[dc])))
    h=sum(len(DEICTIC.findall(hist["docs/state-history/"+f])) for f in fs)
    print(f"  :{i+1:3d}  baseline {n:2d}  ->  row {m:2d} + history {h:2d} = {m+h:2d}")
