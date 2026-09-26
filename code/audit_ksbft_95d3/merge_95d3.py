"""merge_95d3.py (mg-95d3): sum the AGG lines of the stride-parts of one scan (exact Fractions for margins)."""
import sys, re
from fractions import Fraction as Fr
tot={}; wm=None; wmP=''; wc=None; canon_neg=0; dp1=0.0; dpw=''; fails=[]
for fn in sys.argv[1:]:
    for line in open(fn):
        if line.startswith('FAIL'): fails.append(line.strip()); continue
        if line.startswith('AGG '):
            for k,v in re.findall(r'(\w+)=(\S+)',line):
                if k in ('file','part','indec','lo','worst_margin'): continue
                tot[k]=tot.get(k,0)+int(v)
            m=re.search(r'worst_margin=(\d+)/(\d+) at (.*)$',line); f=Fr(int(m.group(1)),int(m.group(2)))
            if m.group(3).strip() and (wm is None or f<wm): wm=f; wmP=m.group(3).strip()
            head=re.search(r'indec=(\d) lo=(\S+)',line).groups()
        if line.startswith('AGGC'):
            m=re.search(r'margin=(\d+)/(\d+).*fails=(\d+)',line); f=Fr(int(m.group(1)),int(m.group(2))); canon_neg+=int(m.group(3))
            if wc is None or f<wc: wc=f
        if line.startswith('AGGR maxdp_pi1'):
            m=re.search(r'maxdp_pi1=(\S+) witness (.*)$',line)
            if float(m.group(1))>dp1: dp1=float(m.group(1)); dpw=m.group(2)
print(f"  indec_only={head[0]} interval_lo={head[1]}")
print("  "+"  ".join(f"{k}={v}" for k,v in tot.items()))
print(f"  worst margin (min over P of max over v,pair) = {wm} = {float(wm):.6f} at {wmP}" if wm is not None else "  worst margin: none")
print(f"  worst canonical margin (every min-range v works) = {wc} = {float(wc):.6f}; posets where some min-range v fails = {canon_neg}")
print(f"  Lemma R: max |p-p'| at pi(v)=1: {dp1:.10f}  witness {dpw}")
for l in fails[:12]: print("  "+l)
if len(fails)>12: print(f"  ... {len(fails)-12} more FAIL lines")
