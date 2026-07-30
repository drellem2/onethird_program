import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_core import posets_upto_iso, linexts, at_graph
from audit_brown import decide_brown, unreachable_edge_test
pos=[];neg=0;vac=0;skip=0
for P in posets_upto_iso(6):
    m=len(linexts(P))
    if m>14:
        skip+=1; continue
    v,wit=decide_brown(P)
    t=unreachable_edge_test(P)
    if v=='vacuous': vac+=1
    elif v=='NOT a Brown walk': neg+=1
    else: pos.append((P.tag(),m,t))
print("n=6, restricted to |L(P)| <= 14:  NOT=%d  IS=%d  vacuous=%d  (skipped %d larger)"%(neg,len(pos),vac,skip))
for tag,m,t in pos:
    print("   IS a Brown walk: |L(P)|=%2d   §9.4 test: %-26s  %s"%(m,t,tag))
