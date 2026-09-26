"""mech.py (audit mg-f4f0): mg-785e sec 4.1 'reason' check on all 29 non-twin region configurations at n=10:
is (s,t) a dominance pair whose only separator lies below both (so Cor 1.2 of mg-561a forces balance)?
Also Q12 / T11 exact values."""
from fractions import Fraction as F
from eng import *
from xlocal import run
_, _, _, _, _, nt = run(10)
kinds = {}
for w, iv, A, A2, S, T, q, us, ut in nt:
    R = rel_from_iv(iv); C = covers_rel(R); ix = {}
    s = next(i for i, x in enumerate(iv) if x == S); t = next(i for i, x in enumerate(iv) if x == T)
    cnt, e = pair_counts(R)
    if cnt[t][s] > cnt[s][t]: s, t = t, s
    dom = iv[s][0] <= iv[t][0] and iv[s][1] <= iv[t][1]
    Ast, Bst = seps_rel(R, C, s, t); Ats, Bts = seps_rel(R, C, t, s)
    # Cor 1.2 identity: P(Lambda_2(s,t)) = 2P[s<t]-1 when S(t,s) empty
    k = (dom, len(Ast), len(Bst), len(Ats) + len(Bts))
    kinds[k] = kinds.get(k, 0) + 1
print('non-twin region configs at n=10 by (s dominates t, |A(s,t)|, |B(s,t)|, |S(t,s)|):', kinds)
# Q12 and T11
Q12 = [(1,1),(1,2),(2,3),(2,5),(3,4),(4,5),(5,6),(5,8),(6,7),(7,8),(8,9),(9,9)]
R = rel_from_iv(Q12); cnt, e = pair_counts(R); ix = {x: i for i, x in enumerate(Q12)}
p = F(cnt[ix[(2,5)]][ix[(3,4)]], e)
print(f'Q12: e = {e}; P[[2,5]<[3,4]] = {p} = {float(p):.5f}; 1/3 - that = {float(F(1,3)-p):.5f}')
L = Q12[:3] + [(3,4), (2,5)] + Q12[5:]
Li = [ix[x] for x in L]; pos = {v: i for i, v in enumerate(Li)}
inv = [(float(F(cnt[v][u], e)), Q12[u], Q12[v]) for u in range(12) for v in range(12) if inc(Q12, u, v) and pos[u] < pos[v]]
print('Q12 staircase L: max L-inversion probability =', max(inv))
T11 = [(1,1),(1,1),(1,2),(2,4),(3,3),(3,5),(3,5),(4,4),(4,5),(5,5),(5,5)]
R = rel_from_iv(T11); cnt, e = pair_counts(R)
a, a2, s, t = 4, 3, 7, 8
print('T11: P[a<a\'] =', F(cnt[a][a2], e), ' P[s<a\'] =', F(cnt[s][a2], e), ' P[t<a\'] =', F(cnt[t][a2], e), ' P[s<t] =', F(cnt[s][t], e),
      ' seps(a,a\') =', [T11[z] for z in sum(seps_rel(R, covers_rel(R), a, a2), [])])
