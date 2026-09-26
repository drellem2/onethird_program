"""xfail.py (audit mg-f4f0): exact verification of an X-LOCAL FAILURE of Lemma C found by xclimb.py.
X14 (canonical) = [1,1]^2 [1,2] [2,6] [3,3] [3,4]^2 [3,5] [4,7] [5,5] [6,6] [7,7]^3, containment step
a = [3,3] inside a' = [2,6], S(a,a') = {s=[4,7], t=[5,5]}.
Three independent computations of the same four pair laws:
 (A) ideal-lattice forward/backward DP (eng.pair_counts);
 (B) order law of the 4-tuple (a,a',s,t) by an automaton DP over (ideal, order-so-far);
 (C) brute-force enumeration of all linear extensions (only if e(P) <= 3e6).
Separators recomputed from covers, and checked against the interval rule min Z, Z = {z: r(a) < l(z) <= r(a')}."""
import sys
from fractions import Fraction as F
from eng import *
X14 = [(1,1),(1,1),(1,2),(2,6),(3,3),(3,4),(3,4),(3,5),(4,7),(5,5),(6,6),(7,7),(7,7),(7,7)]

def check(iv, a, a2, brute=True):
    assert canonical(iv) == sorted(iv), 'not canonical'
    R = rel_from_iv(iv); C = covers_rel(R); n = len(iv)
    A, B = seps_rel(R, C, a, a2)
    Z = [z for z in range(n) if iv[a][1] < iv[z][0] <= iv[a2][1]]
    minZ = [z for z in Z if not any(R[y][z] for y in Z)]
    assert not B and sorted(A) == sorted(minZ), (A, B, minZ)
    s, t = A
    print(f"P = {iv}\n a = {iv[a]}, a' = {iv[a2]}, S = A(a,a') = {[iv[s], iv[t]]} (= min Z, B empty); strict containment: {iv[a2][0] < iv[a][0] and iv[a][1] < iv[a2][1]}")
    cnt, e = pair_counts(R)
    q, us, ut, pst = F(cnt[a2][a], e), F(cnt[s][a2], e), F(cnt[t][a2], e), F(cnt[s][t], e)
    law = auto_count(R, (), lambda st, v: st + (v,) if v in (a, a2, s, t) else st)
    tot = sum(law.values())
    def pr(x, y): return F(sum(c for o, c in law.items() if o.index(x) < o.index(y)), tot)
    assert tot == e and (pr(a2, a), pr(s, a2), pr(t, a2), pr(s, t)) == (q, us, ut, pst), 'DP methods disagree'
    print(f" e(P) = {e}; (A) and (B) agree exactly")
    if brute and e <= 3_000_000:
        E = extensions(R); assert len(E) == e
        c = [0, 0, 0, 0]
        for sg in E:
            p = {v: i for i, v in enumerate(sg)}
            c[0] += p[a2] < p[a]; c[1] += p[s] < p[a2]; c[2] += p[t] < p[a2]; c[3] += p[s] < p[t]
        assert [F(x, e) for x in c] == [q, us, ut, pst], 'enumeration disagrees'
        print(' (C) brute-force enumeration agrees exactly')
    w = min(pst, 1 - pst)
    print(f" q = P[a'<a] = {q} = {float(q):.5f}\n u_s = P[s<a'] = {us} = {float(us):.5f}\n u_t = P[t<a'] = {ut} = {float(ut):.5f}\n"
          f" P[s<t] = {pst} = {float(pst):.5f}  ->  min(P[s<t],P[t<s]) = {float(w):.5f}")
    fail = q < F(1,3) and us < F(1,3) and ut < F(1,3) and w < F(1,3)
    print(f" q, u_s, u_t < 1/3 and (s,t) UNBALANCED: {fail}  -> X-local form of Lemma C {'FAILS' if fail else 'holds'} here; slack = {float(min(F(1,3)-q, F(1,3)-us, F(1,3)-ut, F(1,3)-w)):.6f}")
    return fail

X12 = [(1,1),(1,1),(1,1),(1,1),(1,2),(1,3),(2,6),(3,4),(3,5),(4,5),(5,6),(6,6)]

if __name__ == '__main__':
    for P in (X12, X14):
        R = rel_from_iv(P); hits = 0
        for a, a2, s, t in cont_twosep(P, R, covers_rel(R)):
            print('-' * 70); hits += check(P, a, a2)
        print(f'==> {len(P)} elements: X-local failures {hits}')
    # control: the n=10 tight configuration of mg-785e sec 4.1 must NOT fail (w = 49/125)
    P = [(1,1),(1,1),(1,1),(1,2),(1,3),(2,6),(3,4),(4,5),(5,6),(6,6)]
    print('-' * 70, '\ncontrol (n=10, doc sec 4.1 tightest case; must hold):')
    print('control', 'CAUGHT' if not check(P, P.index((3,4)), P.index((2,6))) else 'NOT CAUGHT')
