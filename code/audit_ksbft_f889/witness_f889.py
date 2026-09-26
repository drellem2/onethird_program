#!/usr/bin/env python3
"""witness_f889.py (mg-f889): recompute, with indep_f889.py's own counter, the mg-2912 (KSBFT-A)
annealing witness n=21 (code/ksbft_range_probe/out/*.jsonl, search_delta D=4) and compare its
delta-margin with KSBFT-M's claimed mu_4 = 5/318."""
import sys
sys.argv=['x']
exec(open(__file__.replace('witness_f889.py','indep_f889.py')).read().split('def main')[0])
down=[0,0,1,3,5,15,63,31,255,159,767,511,1791,4095,8191,12287,65535,32767,196607,524287,131071]
t=len(down)
# transitive closure check (the record must already be closed)
clo=list(down); ch=True
while ch:
    ch=False
    for b in range(t):
        m=clo[b]; x=m
        while x:
            l=x&-x; a=l.bit_length()-1; x^=l
            if clo[a]&~clo[b]: clo[b]|=clo[a]; ch=True
print("closed:", clo==down, " acyclic:", all(not(clo[b]>>b&1) for b in range(t)))
m=delta_margin(clo,t); inc=incomp(clo,t)
print(f"n={t} range={rng(clo,t)} indecomposable={indecomposable(clo,t)} delta-1/3={m} = {float(m):.6f}  delta={m+F(1,3)}")
print(f"5/318 = {float(F(5,318)):.6f};  witness below 5/318: {m < F(5,318)};  below 1/150 (Cor 2.6 D=4): {m < F(1,150)}")
