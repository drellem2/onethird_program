"""prop21.py (audit mg-f4f0): exact re-check of mg-785e Prop 2.1's witness point, and the same local system
evaluated at the REAL laws of X12 (an actual interval order, so every true inequality holds there)."""
from fractions import Fraction as F
from eng import *
from xfail import X12
def system(q, g, us, ut, b):
    return {'swap identity u_s+u_t-beta = 1-2q+gamma': us + ut - b == 1 - 2*q + g,
            'Prop 2.2: beta <= q-gamma': b <= q - g, 'Prop 2.2: u_s+u_t-2beta <= q-gamma': us + ut - 2*b <= q - g,
            'q,u_s,u_t < 1/3': max(q, us, ut) < F(1, 3), '0 <= beta <= min(u_s,u_t)': 0 <= b <= min(us, ut),
            'XYZ (dual): beta >= u_s u_t': b >= us * ut}
r = system(F(3,10), F(0), F(3,10), F(3,10), F(1,5)); print('Prop 2.1 point (3/10,0,3/10,3/10,1/5):', all(r.values()), r)
# X12 real values (Z = S there? report)
R = rel_from_iv(X12); C = covers_rel(R); a, a2 = X12.index((3,4)), X12.index((2,6)); s, t = seps_rel(R, C, a, a2)[0]
n = len(X12); Z = [z for z in range(n) if X12[a][1] < X12[z][0] <= X12[a2][1]]
law = auto_count(R, (), lambda st, v: st + (v,) if v in (a, a2, s, t) else st); e = sum(law.values())
P = lambda f: F(sum(c for o, c in law.items() if f(o)), e)
q = P(lambda o: o.index(a2) < o.index(a)); us = P(lambda o: o.index(s) < o.index(a2)); ut = P(lambda o: o.index(t) < o.index(a2))
b = P(lambda o: o.index(s) < o.index(a2) and o.index(t) < o.index(a2))
Sr = sum(seps_rel(R, C, a2, a), [])   # gamma computed DIRECTLY (not from the identity): a' before a, a reverse separator between
E = extensions(R); g = F(sum(1 for sg in E if (lambda p: p[a2] < p[a] and any(p[a2] < p[z] < p[a] for z in Sr))({v: i for i, v in enumerate(sg)})), len(E))
assert len(E) == e
print(f'X12: Z = S? {sorted(Z) == sorted([s, t])}; q={q}, u_s={us}, u_t={ut}, beta={b}, gamma={g}; beta/(u_s u_t) = {float(b/(us*ut)):.4f}')
print('X12 satisfies the Prop 2.1 local system:', {k: v for k, v in system(q, g, us, ut, b).items()})
