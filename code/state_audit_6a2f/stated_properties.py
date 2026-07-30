#!/usr/bin/env python3
"""
mg-6a2f part 4 — verify every NUMBER mg-34bf states about itself, from scratch.
Nothing here is taken from the commit message or the README; those are printed
beside my measurement for comparison only.
"""
import re, subprocess, collections
B="97cb533"; A="57f962f"
def show(rev,p): return subprocess.run(["git","show",f"{rev}:{p}"],capture_output=True,text=True,check=True).stdout
def ls(rev,p):
    return [l for l in subprocess.run(["git","ls-tree","-r","--name-only",rev,p],
            capture_output=True,text=True,check=True).stdout.split("\n") if l.strip()]
before=show(B,"STATE.md"); after=show(A,"STATE.md")
hist={p:show(A,p) for p in ls(A,"docs/state-history")}
bl=before.split("\n"); al=after.split("\n")
changed=[i for i in range(len(bl)) if bl[i]!=al[i]]
CS=re.compile(r'(?<!\\)\|')
def cells(line):
    p=CS.split(line)
    if p and p[0].strip()=="":p=p[1:]
    if p and p[-1].strip()=="":p=p[:-1]
    return [x.strip() for x in p]

def hdr(t): print("\n"+"="*78+f"\n{t}\n"+"="*78)

hdr("1. FILE-LEVEL")
print(f"lines: before {len(bl)-1}  after {len(al)-1}   (claim: same 367, no line inserted/deleted)")
print(f"lines differing: {len(changed)} -> {[i+1 for i in changed]}   (claim: ten ledger cells)")
print(f"STATE.md size: before {len(before):,} chars / {len(before.encode()):,} bytes")
print(f"               after  {len(after):,} chars / {len(after.encode()):,} bytes")
print(f"  delta: {len(before)-len(after):,} chars / {len(before.encode())-len(after.encode()):,} bytes")
print(f"  README claims: 188,870 -> 161,269 'bytes'  (delta 27,601)")

hdr("2. PER-ROW CELL SIZES vs THE README INDEX TABLE")
README_INDEX = {89:(1556,1585),114:(725,555),124:(1467,1621),130:(2597,2052),131:(4918,3651),
                132:(8630,4804),133:(12696,6876),134:(9974,6247),135:(13190,7705),136:(15386,8442)}
ok=True
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    mb,ma=len(bc[dc]),len(ac[dc])
    rb,ra=README_INDEX[i+1]
    flag = "" if (mb,ma)==(rb,ra) else "  <-- MISMATCH"
    if flag: ok=False
    print(f"  :{i+1:3d} col{dc}  measured chars {mb:6,d} -> {ma:6,d} | README {rb:6,d} -> {ra:6,d}"
          f" | measured BYTES {len(bc[dc].encode()):6,d} -> {len(ac[dc].encode()):6,d}{flag}")
print(f"  index table matches CHARACTER counts exactly: {ok}   (it is labelled 'bytes')")

hdr("3. THE 'FIVE CONSECUTIVE GIANTS' FIGURES")
rows=[132,133,134,135,136]
mine=[len(cells(bl[i-1])[2]) for i in rows]
print("  rows 132-136 measured, cell characters:", ", ".join(f"{v:,}" for v in mine))
print("  rows 132-136 measured, KB (chars/1000): ", " / ".join(f"{v/1000:.1f}" for v in mine))
print("  commit message states:  5.4 / 8.6 / 12.7 / 10.0 / 15.4 KB")
print("  README states:          5.4 / 9.2 / 13.5 / 10.8 / 15.4 KB")
print("  ticket (pm-onethird, stale rev) stated: 5,351 / 9,228 / 13,487 / 10,824 / 11,727 bytes = 5.4/9.2/13.5/10.8/11.7")
print("  -> row 135 (13.2 KB, the SECOND-largest cell in the file) appears in NEITHER list.")

hdr("4. LARGEST CELL ANYWHERE")
def allcells(txt):
    out=[]
    for n,l in enumerate(txt.split("\n"),1):
        if not l.startswith("|"): continue
        c=cells(l)
        if all(set(x)<=set("-: ") for x in c): continue
        for k,x in enumerate(c): out.append((n,k,x))
    return out
for nm,txt in (("before",before),("after",after)):
    cs=sorted(allcells(txt),key=lambda t:-len(t[2]))
    n,k,x=cs[0]
    print(f"  {nm}: line {n} col {k}: {len(x):,} chars / {len(x.encode()):,} bytes")
print("  claim: largest cell 15,386 -> 8,442 'bytes'")

hdr("5. ROW COUNT / RENUMBERING / COLUMNS 1-2")
def rowkeys(txt):
    out=[]
    for n,l in enumerate(txt.split("\n"),1):
        if not l.startswith("|"): continue
        c=cells(l)
        if all(set(x)<=set("-: ") for x in c): continue
        out.append((n,tuple(c[:2])))
    return out
rb=rowkeys(before); ra=rowkeys(after)
print(f"  rows: before {len(rb)}  after {len(ra)}")
print(f"  (line, col0, col1) identical for every row: {rb==ra}")
# full-ledger '#' column
nums_b=[cells(bl[i])[0] for i in range(77,89)]
nums_a=[cells(al[i])[0] for i in range(77,89)]
print(f"  Full-ledger '#' column unchanged: {nums_b==nums_a}  -> {nums_b}")

hdr("6. APPENDIX A BYTE-IDENTICAL")
# Appendix A runs from its heading to EOF-ish; find bounds
start=[i for i,l in enumerate(bl) if l.startswith("## Appendix A")][0]
print(f"  Appendix A heading at line {start+1}")
print(f"  byte-identical from line {start+1} to EOF: "
      f"{'\n'.join(bl[start:])=='\n'.join(al[start:])}")
print(f"  no changed line is >= {start+1}: {max(changed)+1 < start+1}")

hdr("7. HISTORY FILE TOTALS AND 'BYTES MOVED'")
tot=sum(len(v.encode()) for k,v in hist.items() if not k.endswith('README.md'))
totc=sum(len(v) for k,v in hist.items() if not k.endswith('README.md'))
print(f"  ten row-history files: {totc:,} chars / {tot:,} bytes   (README claims 52,126 'bytes')")
print(f"  README.md itself: {len(hist['docs/state-history/README.md']):,} chars / "
      f"{len(hist['docs/state-history/README.md'].encode()):,} bytes")
# bytes moved = chars of history-file text that occurs verbatim in the baseline cell of its row
btok=before.split(); pos=collections.defaultdict(list)
for i,t in enumerate(btok): pos[t].append(i)
def matched_chars(text):
    seq=text.split(); i=0; kept=0; newc=0
    while i<len(seq):
        st=pos.get(seq[i]); best=0
        if st:
            for s in st:
                L=1
                while i+L<len(seq) and s+L<len(btok) and btok[s+L]==seq[i+L]: L+=1
                best=max(best,L)
                if i+best>=len(seq): break
        if best==0:
            newc+=len(seq[i])+1; i+=1
        else:
            kept+=sum(len(t)+1 for t in seq[i:i+best]); i+=best
    return kept,newc
mk=mn=0
for k,v in hist.items():
    if k.endswith("README.md"): continue
    a_,b_=matched_chars(v); mk+=a_; mn+=b_
print(f"  of the ten files, text matching the baseline verbatim: ~{mk:,} chars; new header/scaffold: ~{mn:,} chars")
print(f"  README claims '36,188 bytes of ledger text moved'")
# pointer text added into rows
addrows=0
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    _,n_=matched_chars(ac[dc]); addrows+=n_
print(f"  new (non-baseline) text added into the ten rows: ~{addrows:,} chars   (README: 'about 5 KB')")

hdr("8. 'BYTES MOVED' and 'NEW POINTER TEXT', measured by partitioning each baseline cell")
# For each row: decompose the baseline cell into maximal runs against (after cell) alone,
# and against (after cell U history file).  A run findable in the after cell STAYED; a run
# findable only in the history file MOVED.
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
stay=move=newp=0; per=[]
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    fs=sorted(set(LINK.findall(ac[dc])))
    acell=corpus(ac[dc].split())
    both=corpus(ac[dc].split()+sum((hist["docs/state-history/"+f].split() for f in fs),[]))
    seq=bc[dc].split(); i2=0; s_=m_=0
    while i2<len(seq):
        L=run_at(seq,i2,both)
        assert L>0
        txt=" ".join(seq[i2:i2+L]); n=len(txt)+1
        # did this exact run survive in the after cell itself?
        if run_at(seq,i2,acell)>=L: s_+=n
        else: m_+=n
        i2+=L
    # new pointer text = after cell chars minus baseline chars that stayed
    np_=len(ac[dc])-s_
    stay+=s_; move+=m_; newp+=np_
    per.append((i+1,len(bc[dc]),s_,m_,len(ac[dc]),np_))
print("  row |  before |  stayed |   MOVED |   after | new-in-row")
for r in per: print(f"  :{r[0]:3d} | {r[1]:7,d} | {r[2]:7,d} | {r[3]:7,d} | {r[4]:7,d} | {r[5]:+8,d}")
print(f"  TOT |         | {stay:7,d} | {move:7,d} |         | {newp:+8,d}")
print(f"  README claims: 36,188 'bytes' of ledger text moved; 'about 5 KB' of new pointer text in rows")

hdr("9. COLUMNS OTHER THAN THE RESTRUCTURED ONE")
for i in changed:
    bc=cells(bl[i]); ac=cells(al[i])
    dc=[c for c in range(len(ac)) if ac[c]!=bc[c]][0]
    others=[c for c in range(len(bc)) if c!=dc]
    same=all(bc[c]==ac[c] for c in others)
    print(f"  :{i+1:3d}  restructured col {dc} of {len(bc)}; all other columns identical: {same}")

hdr("10. MECHANISM SENTENCES THE TICKET NAMED BY NAME")
targets=["joins suppress","the pipeline survived the control it was missing",
         "coverage went from ZERO to ONE ABSORBABLE SIGN GAUGE",
         "SUPPRESS","absorbable sign gauge"]
corpus_all = after + "\n" + "\n".join(hist.values())
for t in targets:
    nb=before.count(t); na=after.count(t); nh=sum(v.count(t) for v in hist.values())
    print(f"  {t!r}: baseline {nb}  after-STATE {na}  history {nh}  total-after {na+nh}")
