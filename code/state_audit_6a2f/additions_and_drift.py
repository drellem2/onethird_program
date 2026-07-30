#!/usr/bin/env python3
"""
mg-6a2f part 2 — what CHANGED in meaning, and what was ADDED beyond the brief.

Completeness (part 1) proves nothing left. It proves nothing about what arrived.
This script asks the two remaining questions:

  D. ADDITIONS.  Every sentence in the after-corpus (changed cells + history files)
     that does NOT occur verbatim in the baseline STATE.md.  Each one is either
     (i) a pointer/structural sentence the ticket asked for, or (ii) something
     beyond the brief.  Printed in full for hand adjudication -- there is no
     mechanical test for "beyond brief".

  E. RETRACTION ADJACENCY.  Every table cell in the after file scanned for
     retraction / strike / supersession / correction markers, so the claim
     "no row contains a claim and its own retraction" can be checked against
     ALL 58 rows and not only the ten that moved.

  F. CITATIONS.  Every doc name, mg-id, commit sha and section reference in the
     baseline changed cells must still appear in the row or a file it links to.
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
    if not line.startswith("|"): return None
    p=CS.split(line)
    if p and p[0].strip()=="":p=p[1:]
    if p and p[-1].strip()=="":p=p[:-1]
    return [x.strip() for x in p]

def norm(s): return " ".join(s.split())

# sentence-ish splitter: on '. ' / '! ' / '? ' outside inline code, plus newlines
def sentences(txt):
    txt=txt.replace("\n"," \n ")
    out=[]; cur=[]
    toks=txt.split(" ")
    for t in toks:
        if t=="\n":
            if cur: out.append(" ".join(cur)); cur=[]
            continue
        cur.append(t)
        if re.search(r'[.!?](\*\*|\*|`|\)|")*$', t) and not re.search(r'§|mg-|no\.$|vs\.$|etc\.$|e\.g\.$|i\.e\.$|cf\.$|Thm\.$|approx\.$', t):
            out.append(" ".join(cur)); cur=[]
    if cur: out.append(" ".join(cur))
    return [norm(s) for s in out if norm(s)]

baseline_norm = norm(before)

print("="*78); print("D. ADDITIONS — after-corpus sentences absent verbatim from the baseline")
print("="*78)
added=[]
for i in changed:
    ac=cells(al[i]); bc=cells(bl[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    for s in sentences(ac[dc]):
        if s not in baseline_norm: added.append((f"STATE.md:{i+1}", s))
for p,txt in hist.items():
    for s in sentences(txt):
        if s not in baseline_norm: added.append((p, s))
print(f"{len(added)} added sentence-units\n")
groups=collections.OrderedDict()
for p,s in added: groups.setdefault(p,[]).append(s)
for p,ss in groups.items():
    print(f"### {p}  ({len(ss)})")
    for s in ss: print("   + "+s)
    print()

print("="*78); print("E. RETRACTION ADJACENCY — all table cells in the after file")
print("="*78)
MARK=[r'\bSTRUCK\b',r'\bstruck\b',r'\bRETRACT',r'\bretract',r'\bRETIRED\b',r'\bretired\b',
      r'used to (say|read|state)',r'\bREFUTED\b',r'\brefuted\b',r'\bCORRECTION\b',
      r'\bsupersed',r'\bSUPERSED',r'\bno longer\b',r'\bwithdrawn\b',r'previously (said|stated|read)',
      r'\bfalse as stated\b',r'\bwas wrong\b',r'\bnow (struck|withdrawn|retired)\b',
      r'\bREPLACED\b',r'\bcorrected\b',r'\bCORRECTED\b',r'\bstrike\b',r'\bSTRIKE\b',
      r'\breopen',r'\bREOPEN']
MRE=re.compile("|".join(MARK))
nrows=0
for i,l in enumerate(al,1):
    c=cells(l)
    if c is None: continue
    if all(set(x)<=set("-: ") for x in c): continue
    nrows+=1
    hits=[]
    for k,x in enumerate(c):
        for m in MRE.finditer(x):
            s=max(0,m.start()-90); e=min(len(x),m.end()+90)
            hits.append((k,m.group(0),"..."+x[s:e]+"..."))
    if hits:
        print(f"--- row at line {i} :: {c[0][:70]!r}")
        for k,g,ctx in hits: print(f"    col{k} [{g}] {ctx}")
print(f"\nscanned {nrows} table rows (incl. header rows)")

print("="*78); print("F. CITATIONS — every reference in a baseline changed cell must survive")
print("="*78)
CITE=re.compile(r'(mg-[0-9a-f]{4})|([A-Za-z0-9][A-Za-z0-9._-]*\.(md|tex|py|sh|txt|html))|(\b[0-9a-f]{7}\b)|(§[0-9]+(\.[0-9]+)*)|(\b[0-9]{4}\.[0-9]{4,5}\b)')
LINKRE=re.compile(r'docs/state-history/([A-Za-z0-9._-]+\.md)')
lost_cites=[]
allb=collections.Counter(); alla=collections.Counter()
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    reach=norm(ac[dc])
    for f in sorted(set(LINKRE.findall(ac[dc]))):
        reach += " " + norm(hist["docs/state-history/"+f])
    bcites=collections.Counter(m.group(0) for m in CITE.finditer(bc[dc]))
    acites=collections.Counter(m.group(0) for m in CITE.finditer(reach))
    allb.update(bcites); alla.update(acites)
    for cit,n in bcites.items():
        if acites.get(cit,0) < n:
            lost_cites.append((i+1,cit,n,acites.get(cit,0)))
print(f"distinct references in baseline changed cells: {len(allb)} ({sum(allb.values())} occurrences)")
if not lost_cites:
    print("RESULT: every reference survives at >= its baseline multiplicity. PASS.")
else:
    print("RESULT: references short:")
    for ln,cit,n,h in lost_cites: print(f"   line {ln}: {cit}  need {n} have {h}")
