"""remark26.py (audit mg-3345): Remark 2.6 value vs its (v_1,v_2) labelling.  Poset y<a<b<c plus an
isolated x: Inc(y)={x}, P[x before y] = h(y)-1 (the value claim), but x is not v_2 in mean-height order."""
from fractions import Fraction as F
from indep import info
d = info("5 0 1 3 0 7")   # 0=y, 1=a, 2=b, 3=x (isolated), 4=c
H = {v: F(sum(dd[v] + 1 for dd in d['pos']), d['e']) for v in range(5)}
print("Inc(y)=", d['I'][0], " P[x before y]=", d['p'](3, 0), " h(y)-1=", H[0] - 1)
print("mean heights:", {v: str(h) for v, h in H.items()}, " order:", sorted(H, key=H.get))
