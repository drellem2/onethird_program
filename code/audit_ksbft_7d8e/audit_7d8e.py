#!/usr/bin/env python3
"""Independent referee checks for notes/lemma-W-polynomial-range-bound.tex (mg-7d8e).
Written from the note and the cited sources only; imports nothing from the author's code."""
import itertools, math, random
from fractions import Fraction as Fr

def lin_exts(n, less):
    out = []
    for perm in itertools.permutations(range(n)):
        pos = [0]*n
        for i, e in enumerate(perm): pos[e] = i + 1
        if all(pos[a] < pos[b] for (a, b) in less): out.append(pos)
    return out

def labeled_posets(n):
    pairs = [(a, b) for a in range(n) for b in range(n) if a != b]
    seen = set()
    # generate strict orders as transitive, antisymmetric subsets; filter by order a<b consistent w/ some perm (DAG)
    for mask in range(1 << len(pairs)):
        rel = {pairs[i] for i in range(len(pairs)) if mask >> i & 1}
        if any((b, a) in rel for (a, b) in rel): continue
        if any((a, c) not in rel for (a, b) in rel for (b2, c) in rel if b == b2 and a != c): continue
        yield rel

def pi_of(n, rel):
    return [sum(1 for v in range(n) if v != u and (u, v) not in rel and (v, u) not in rel) for u in range(n)]

def census(nmax):
    stats = dict(pairs=0, viol_E1=0, viol_ge2=0, viol_middle=0, viol_propB=0, posets=0, middle_example=None)
    for n in range(2, nmax + 1):
        for rel in labeled_posets(n):
            stats['posets'] += 1
            L = lin_exts(n, rel); e = len(L); pi = pi_of(n, rel)
            D = max(pi)
            for x in range(n):
                for y in range(n):
                    if x == y or (x, y) in rel or (y, x) in rel: continue
                    N = [w for w in range(n) if w not in (x, y) and (w, y) not in rel and (x, w) not in rel]
                    if not N: continue
                    stats['pairs'] += 1
                    piN = max(pi[w] for w in N)
                    E1 = sum(1 for g in L if g[x] == g[y] + 1)
                    E2 = sum(1 for g in L if g[x] == g[y] + 2)
                    ge2 = sum(1 for g in L if g[x] - g[y] >= 2)
                    p = sum(1 for g in L if g[y] < g[x])
                    if E1 > piN * E2: stats['viol_E1'] += 1
                    if Fr(ge2) < Fr(p, piN + 1): stats['viol_ge2'] += 1
                    if Fr(E2) < Fr(p, piN + 1):
                        stats['viol_middle'] += 1
                        if stats['middle_example'] is None: stats['middle_example'] = (n, sorted(rel), x, y, piN, Fr(E2, e), Fr(p, e))
            # Prop B: connected incomparability graph, d1 >= 1/(D+1)
            adj = {u: [v for v in range(n) if v != u and (u, v) not in rel and (v, u) not in rel] for u in range(n)}
            seen = {0}; st = [0]
            while st:
                u = st.pop()
                for v in adj[u]:
                    if v not in seen: seen.add(v); st.append(v)
            if len(seen) == n:
                h = [Fr(sum(g[u] for g in L), e) for u in range(n)]
                if min(h) - 1 < Fr(1, D + 1): stats['viol_propB'] += 1
    return stats

def ratio(n, rel, x, y):
    L = lin_exts(n, rel)
    p = sum(1 for g in L if g[y] < g[x]); ge2 = sum(1 for g in L if g[x] - g[y] >= 2)
    E2 = sum(1 for g in L if g[x] == g[y] + 2)
    return Fr(ge2, p), Fr(E2, p), L

def closure(n, rel):
    rel = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel: rel.add((a, d)); changed = True
    return rel

def main():
    print("== 1. census, all labeled posets n<=5 ==")
    s = census(5)
    for k, v in s.items(): print(f"  {k}: {v}")
    print("  NEG CONTROL (the note's displayed middle inequality, which is false): viol_middle =", s['viol_middle'], "FIRES" if s['viol_middle'] > 0 else "DOES NOT FIRE")
    print("  poset count n=2..5 =", s['posets'], "(A001035: 3+19+219+4231 = 4472)", "OK" if s['posets'] == 4472 else "MISMATCH")
    assert s['viol_E1'] == 0 and s['viol_ge2'] == 0 and s['viol_propB'] == 0 and s['posets'] == 4472

    print("== 2. explicit counterexample to the displayed middle inequality P[f(x)=f(y)+2] >= P[y<x]/(pi_N+1) ==")
    # chain c1<c2<x (0,1,2), y=3 isolated
    for k in range(1, 5):
        n = k + 2; x = k; y = k + 1
        rel = closure(n, [(i, i + 1) for i in range(k)])  # 0<1<..<k=x
        pi = pi_of(n, rel)
        N = [w for w in range(n) if w not in (x, y) and (w, y) not in rel and (x, w) not in rel]
        piN = max(pi[w] for w in N)
        rge2, rE2, L = ratio(n, rel, x, y)
        print(f"  chain of {k} below x, y isolated: pi_N={piN}, P[>=2]/p={rge2}, P[E2]/p={rE2}, claimed >= {Fr(1, piN+1)} -> middle {'FAILS' if rE2 < Fr(1, piN+1) else 'holds'}, (b) main {'holds' if rge2 >= Fr(1,piN+1) else 'FAILS'}")

    print("== 3. sharpness families ==")
    for D in range(2, 8):
        # generic: x=c1<...<c_{D-1}, y, w isolated
        m = D - 1; n = m + 2; x = 0; y = m; w = m + 1
        rel = closure(n, [(i, i + 1) for i in range(m - 1)])
        pi = pi_of(n, rel)
        N = [u for u in range(n) if u not in (x, y) and (u, y) not in rel and (x, u) not in rel]
        rge2, rE2, _ = ratio(n, rel, x, y)
        print(f"  generic D={D}: pi(P)={max(pi)}, N={N}, pi_N={max(pi[u] for u in N)}, ratio={rge2} (1/(D+1)={Fr(1,D+1)})")
    for k in range(0, 5):
        # Q_k: x=0<z=2, y=1, chain c_1..c_k above all; w isolated
        n = 4 + k; x, y, z, w = 0, 1, 2, 3; cs = list(range(4, 4 + k))
        base = [(x, z)]
        if cs:
            base += [(u, cs[0]) for u in (x, y, z)] + [(cs[i], cs[i + 1]) for i in range(k - 1)]
        rel = closure(n, base)
        pi = pi_of(n, rel); D = k + 3
        rge2, rE2, L = ratio(n, rel, x, y)
        h = [Fr(sum(g[u] for g in L), len(L)) for u in range(n)]
        N = [u for u in range(n) if u not in (x, y) and (u, y) not in rel and (x, u) not in rel]
        bft = h[x] <= h[y] <= h[z] <= h[x] + 2
        print(f"  CaseD P_k k={k}: D={D}, pi(P)={max(pi)}, N={N}, h=({h[x]},{h[y]},{h[z]}), BFT={bft}, ratio={rge2} (1/(D+1)={Fr(1,D+1)})")
    # pi_N = 1 sharpness (abstract says 'every value of pi_N'): y<w, x isolated
    rel = {(1, 2)}; rge2, _, _ = ratio(3, rel, 0, 1)
    print(f"  pi_N=1 example (y<w, x isolated): pi(w)={pi_of(3,rel)[2]}, ratio={rge2} (1/2)")

    print("== 4. Lemma 2.4(a): 7b1+3b2+3b3 <= F(s) and chord, random sampling ==")
    random.seed(7)
    worst = -1e9
    c = (7 * math.sqrt(5) - 1) / 4
    for _ in range(200000):
        b1 = random.random() * 0.5; b2 = random.random() * (1 - 2 * b1)
        s = 2 * b1 + b2
        b3max = min(0.5 - b2, b2 * b2 / (4 * b1) if b1 > 0 else 0.5 - b2)
        if b3max < 0: continue
        b3 = random.random() * b3max
        F = max(3.5 * s, 3.5 * math.sqrt(s * s + 0.25) - 0.25)
        worst = max(worst, 7 * b1 + 3 * b2 + 3 * b3 - F, F - (c - (c - 1.5) * (1 - s)))
    print(f"  max violation (should be <= ~1e-12): {worst:.3e}")
    C = (5 - math.sqrt(5)) / 10
    print(f"  7/(2(9+c))={7/(2*(9+c)):.12f} C_BFT={C:.12f}; (c-1.5)/(2(9+c))={(c-1.5)/(2*(9+c)):.12f} 1/(5+3sqrt5)={1/(5+3*math.sqrt(5)):.12f}")

    print("== 5. Prop C: sample (r,s,alpha*,beta*) in the admissible region, check M <= (20+2sqrt5) eps ==")
    worst = 0; cnt = 0; rho = (math.sqrt(5) - 1) / 2
    for _ in range(400000):
        r = random.random(); s_ = random.random()
        if random.random() < 0.5:  # concentrate near (rho,rho)
            r = min(1, max(0, rho + random.gauss(0, 0.05))); s_ = min(1, max(0, rho + random.gauss(0, 0.05)))
        v = r + s_; Z = 1 + v; g = v + 2 * r * s_ - 2
        if g < 0: continue
        cnt += 1
        tot = random.random() * g / Z; a_ = random.random() * tot; b_ = tot - a_
        eps = max(r, s_) / Z - C
        dm = (r - (1 + s_) * (1 - r)) / Z - a_
        dm2 = ((1 + r) * (1 - s_) - s_) / Z + b_
        M = max(abs(dm), abs(dm2))
        if eps <= 0:
            worst = max(worst, 1e9 if M > 1e-12 else 0); continue
        worst = max(worst, M / eps)
    print(f"  samples={cnt}, max M/eps = {worst:.4f}  vs 20+2sqrt5 = {20+2*math.sqrt(5):.4f}")

    print("== 6. constants ==")
    th0 = 0.2764 - C
    thW = lambda D: C / ((5 + 3 * math.sqrt(5)) * (D + 1) + 1)
    D0 = max(D for D in range(1, 10000) if thW(D) > th0)
    print(f"  theta0={th0:.9e}; thW(3471)={thW(3471):.9e}; thW(3472)={thW(3472):.9e}; D0={D0}")
    print(f"  gain D=1e4: {thW(10**4):.4e}; D=1e6: {thW(10**6):.4e}; C/(5+3sqrt5)={C/(5+3*math.sqrt(5)):.6f}; 1/(20+2sqrt5)={1/(20+2*math.sqrt(5)):.6f}")
    D17 = max(D for D in range(1, 1000) if 1 / (441 * (D + 1) ** 2) > th0)
    print(f"  M^2/441 with M>=1/(D+1) beats theta0 up to D={D17}")
    T = Fr(67, 242); th0p = 67 / 242 - C
    D49 = max(D for D in range(1, 1000) if thW(D) >= th0p)
    print(f"  67/242={float(T):.7f}; theta0'={th0p:.4e}; thW>=theta0' up to D={D49}; 67/242<1-1/sqrt2={float(T) < 1-1/math.sqrt(2)}; <e^-1={float(T)<math.exp(-1)}")
    print(f"  final-line threshold: 5-11T+1/22 = {float(5 - 11*T + Fr(1,22))} (=2 exactly at T=67/242); first-branch 37/132={37/132:.5f}; 32/9={32/9:.4f} < 1/T={float(1/T):.4f}; 29/9 < 1/T: {Fr(29,9) < 1/T}")
    vq = lambda q: (-3 + math.sqrt(9 + 8 * (1 / q - 1))) / 4
    print(f"  v_q: q=0.3 -> {vq(0.3):.4f}; q=0.2764 -> {vq(0.2764):.4f}; q=6/11-0.2764 -> {vq(6/11-0.2764):.4f}; q=65/242 -> {vq(65/242):.4f}; q=67/242 -> {vq(67/242):.4f}")
    print(f"  5-11*0.2764+1/22 = {5-11*0.2764+1/22:.5f}")

if __name__ == '__main__':
    main()
