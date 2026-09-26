"""mg-af00 remark (§5.5(b)): a pi(x)=2 sub-family where the Stanley deficit is a function of a
quantised probability. x; I(x)={a<b}; up(x) = {d} ⊔ chain c_1<...<c_k with b<c_1, d free of a,b,c.
Predicted: deficit at the interior index = q^2/(1+2q), q = P[d first in up(x)] = 1/(k+1).
Also finite witnesses re-decoded with THIS audit's own closure (not ranges2.py's)."""
import io, contextlib, sys
from fractions import Fraction as Fr
with contextlib.redirect_stdout(io.StringIO()):
    sys.argv = ['x', '0']; import check_af00 as C
for k in range(1, 7):
    n = 4 + k  # 0=x, 1=a, 2=b, 3=d, 4..=c_i
    cs = list(range(4, 4 + k))
    rel = [(0, 3), (0, cs[0]), (1, 2), (2, cs[0])] + [(cs[i], cs[i+1]) for i in range(k-1)]
    lt = C.close(n, rel); N, e = C.pos_counts(n, lt)
    q = Fr(1, k+1); r = N[0]
    got = Fr(r[2]**2, r[1]*r[3]) - 1
    print(f"k={k}: range={C.rng(n, lt)} N(x)={r[1:4]} deficit={got} predicted q^2/(1+2q)={q*q/(1+2*q)} {'OK' if got == q*q/(1+2*q) else 'MISMATCH'}")
def from_dn(dn):
    n = len(dn); lt = C.close(n, [(j, i) for i in range(n) for j in range(n) if (dn[i] >> j) & 1])
    assert all(sum(1 << j for j in range(n) if lt[j][i]) == dn[i] for i in range(n)); return n, lt
W = {"(L*) n=9 #1": (0,1,0,4,0,0,32,96,239), "(L*) n=9 #2": (0,0,0,0,0,16,48,16,247),
     "(L*) n=10": (0,1,3,0,9,0,32,96,255,239), "(L*) n=11": (0,1,3,7,0,1,1,113,1,257,257),
     "(F)&(M#) n=10 a": (0,0,0,7,15,31,15,6,135,135), "(F)&(M#) n=10 b": (0,0,3,0,8,0,56,127,127,123),
     "(F)&(M#) n=11": (0,0,0,7,15,15,63,6,135,135,647), "(F)&(M#) n=12 a": (0,0,3,7,15,7,63,2,135,391,7,1159),
     "(F)&(M#) n=12 b": (0,0,0,7,15,31,63,6,135,135,647,135)}
for name, dn in W.items():
    n, lt = from_dn(dn); print(f"{name}: range={C.rng(n, lt)}")
