"""witnesses.py (audit mg-6c30): the named witnesses of mg-561a recomputed with this audit's engine."""
from fractions import Fraction as Fr
from eng import Poset, lambdas
from badl import kills, need_masks, kvec

def I(iv): return Poset.from_iv(tuple(iv))
def ix(iv, t, k=0): return [i for i, x in enumerate(iv) if x == t][k]
def law(P, M, e, x, y): return Fr(M[x][y], e)

print("== P5 no-go (sec 2.1) ==")
iv = [(1,1),(1,2),(2,2),(2,3),(3,3)]; P = I(iv); M, e = P.before_counts()
a, a2, w, s = ix(iv,(1,2)), ix(iv,(2,3)), ix(iv,(1,1)), ix(iv,(3,3))
print(" e =", e, " A =", [iv[z] for z in P.A(a,a2)], " B =", [iv[z] for z in P.B(a,a2)],
      " dominance:", P.dominates(a, a2))
X = [w, a, a2, s]
for x in X:
    for y in X:
        if P.inc[x][y] and M[x][y] * 2 > e: print(f"  P[{iv[x]}<{iv[y]}] = {law(P,M,e,x,y)}")
print("  comparable in X:", [(iv[x], iv[y]) for x in X for y in X if P.lt[x][y]])
print("  (L1, L2, L3)(a,a') =", lambdas(P, a, a2), " (L1,L2,L3)(a',a) =", lambdas(P, a2, a))
print("  2/3-order restricted to X is w < a < a' < s, a,a' adjacent in it:",
      all(M[X[i]][X[j]] * 3 > 2 * e for i in range(4) for j in range(i+1, 4)))

print("== AA dominance LCC witness at n=7 (out_localcc.txt, first AA row) ==")
iv = [(1,1),(1,2),(1,3),(1,4),(2,3),(3,4),(4,4)]; P = I(iv); M, e = P.before_counts()
a, a2 = ix(iv,(1,2)), ix(iv,(1,4)); S = sorted(P.S(a, a2)); X = [a, a2] + S
print(" A =", [iv[z] for z in P.A(a,a2)], "B =", [iv[z] for z in P.B(a,a2)], "dominance a->a':", P.dominates(a, a2))
for x in X:
    for y in X:
        if P.inc[x][y] and M[x][y] * 2 > e: print(f"  P[{iv[x]}<{iv[y]}] = {law(P,M,e,x,y)} ({float(law(P,M,e,x,y)):.4f})")
print("  every law in X outside [1/3,2/3]:", all(not (Fr(1,3) <= law(P,M,e,x,y) <= Fr(2,3)) for x in X for y in X if P.inc[x][y]))
print("  no X element between a and a' in the 2/3-order:",
      not any(M[a][z]*3 > 2*e and M[z][a2]*3 > 2*e for z in X if z not in (a, a2) and P.inc[a][z] and P.inc[z][a2]) and
      not any((P.lt[a][z] and M[z][a2]*3 > 2*e) or (P.lt[z][a2] and M[a][z]*3 > 2*e) for z in S))

print("== T11 (sec 2.3) ==")
iv = [(1,1),(1,1),(1,2),(2,4),(3,3),(3,5),(3,5),(4,4),(4,5),(5,5),(5,5)]; P = I(iv); M, e = P.before_counts()
a, a2, s, t = ix(iv,(3,3)), ix(iv,(2,4)), ix(iv,(4,4)), ix(iv,(4,5))
print("  A(a,a') =", sorted(iv[z] for z in P.A(a,a2)), " Z =", sorted(iv[z] for z in range(P.n) if iv[a][1] < iv[z][0] <= iv[a2][1]))
print(f"  P[a<a']={law(P,M,e,a,a2)} P[s<a']={law(P,M,e,s,a2)} P[t<a']={law(P,M,e,t,a2)} P[s<t]={law(P,M,e,s,t)}")
Ds = [z for z in range(P.n) if iv[a2][0] <= iv[z][1] < iv[s][0]]
print("  D_s =", [iv[z] for z in Ds], "; Prop 2.4 equality P[a<a'] = 2P[s<a']:", law(P,M,e,a,a2) == 2*law(P,M,e,s,a2))

print("== O9a certificate triple (sec 3.1) ==")
iv = [(1,1),(1,2),(1,5),(2,3),(2,6),(3,4),(4,5),(5,6),(6,6)]; P = I(iv)
a, c, b = ix(iv,(3,4)), ix(iv,(2,6)), ix(iv,(4,5))
f = lambda S: sorted(iv[z] for z in S)
print("  A(a,c) =", f(P.A(a,c)), " B(a,c) =", f(P.B(a,c)), " A(b,c) =", f(P.A(b,c)), " B(c,a) =", f(P.B(c,a)))
print("  B(c,b) =", f(P.B(c,b)), " A(c,b) =", f(P.A(c,b)), " counted k-events:", [(iv[z], d, iv[r]) for z, d, r in kvec(P, a, c, b)])

print("== sec 5 general n=9 survivor ==")
cov = [(0,2),(1,3),(1,4),(2,6),(3,5),(3,6),(4,7),(5,8),(6,7)]
n = 9; lt = [[False]*n for _ in range(n)]
for x, y in cov: lt[x][y] = True
for c_ in range(n):
    for x in range(n):
        if lt[x][c_]:
            for y in range(n):
                if lt[c_][y]: lt[x][y] = True
P = Poset(n, lt); L = [1,0,3,2,4,5,6,8,7]; pos = {v: i for i, v in enumerate(L)}
need = need_masks(P)
print("  dominance-respecting:", all(not (need[v] >> w) & 1 or pos[w] < pos[v] for v in range(n) for w in range(n)),
      " linear ext:", all(not lt[x][y] or pos[x] < pos[y] for x in range(n) for y in range(n)),
      " K-bad:", all(not P.inc[L[i]][L[i+1]] or len(P.S(L[i], L[i+1])) >= 2 for i in range(n-1)),
      " kills:", sorted(kills(P, L)))
print("  steps (|A|,|B|, dominance either way):", [(len(P.A(L[i],L[i+1])), len(P.B(L[i],L[i+1])), P.dominates(L[i],L[i+1]) or P.dominates(L[i+1],L[i])) for i in range(n-1) if P.inc[L[i]][L[i+1]]])
M, e = P.before_counts()
print("  delta(P) =", min(min(Fr(M[x][y], e), Fr(M[y][x], e)) for x in range(n) for y in range(n) if P.inc[x][y]))
