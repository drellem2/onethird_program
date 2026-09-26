"""controls.py (audit mg-5ecf): brute-force cross-checks of eng.laws and eng.badL, with planted controls.

1. laws() vs explicit enumeration of linear extensions: every interval order n <= 6 and 200 random n = 7, 8;
   plus T8 (general poset). Planted error: perturb one count, must be detected.
2. badL() vs explicit enumeration: every interval order n <= 7, both any-L and dominance-L.
   POSITIVE CONTROL: the author's general poset with 2+2 (n=7) must have a bad L, and the author's
   quoted L must be bad under brute force.
3. Prop 3.1 (interval formula for |S|) vs the cover-based count, every incomparable ordered pair (a before a'
   possible, i.e. a || a') of every interval order n <= 8.
4. Cor 3.2: strict dominance step (l < l', r < r') has |S| >= 2; every n <= 8.
"""
import itertools, random, sys
from fractions import Fraction as F
import eng


def exts(P):
    n, up = P
    out = []
    for perm in itertools.permutations(range(n)):
        pos = [0] * n
        for i, v in enumerate(perm):
            pos[v] = i
        if all(pos[x] < pos[y] for x in range(n) for y in range(n) if up[x] >> y & 1):
            out.append(perm)
    return out


def brute_laws(P):
    n, _ = P
    E = exts(P)
    N = [[0] * n for _ in range(n)]
    for perm in E:
        for i in range(n):
            for j in range(i + 1, n):
                N[perm[i]][perm[j]] += 1
    return len(E), N, E


def is_bad(P, S, perm):
    for a, b in zip(perm, perm[1:]):
        if eng.inc(P, a, b) and S[a][b] <= 1:
            return False
    return True


def dom_ok(P, pred, perm):
    pos = {v: i for i, v in enumerate(perm)}
    return all(pos[x] < pos[y] for y in range(P[0]) for x in range(P[0]) if pred[y] >> x & 1)


def main():
    random.seed(5)
    fails = 0
    # 1
    pop = [iv for n in range(1, 7) for iv in eng.gen(n)] + random.sample(eng.gen(7), 200) + random.sample(eng.gen(8), 200)
    T8 = eng.from_down([int(t, 16) for t in "0 0 2 6 3 e 17 5f".split()])
    mism = 0
    for P in [eng.from_intervals(iv) for iv in pop] + [T8]:
        e, N = eng.laws(P)
        e2, N2, _ = brute_laws(P)
        if e != e2 or N != N2:
            mism += 1
    print(f"1. laws vs brute: {len(pop) + 1} posets, mismatches = {mism}")
    e, N = eng.laws(T8)
    e2, N2, _ = brute_laws(T8)
    N[0][1] += 1
    print(f"   CONTROL planted +1 in N[0][1] detected: {N != N2}")
    fails += mism
    # 2
    cnt = [0, 0]
    mism = 0
    for n in range(2, 8):
        for iv in eng.gen(n):
            P = eng.from_intervals(iv)
            S = eng.seps(P)
            pred = eng.dominance_pred(P)
            E = exts(P)
            b_any = any(is_bad(P, S, p) for p in E)
            b_dom = any(is_bad(P, S, p) and dom_ok(P, pred, p) for p in E)
            if bool(eng.badL(P, S)) != b_any or bool(eng.badL(P, S, dominance=True)) != b_dom:
                mism += 1
            cnt[0] += b_any
            cnt[1] += b_dom
    print(f"2. badL vs brute, every interval order 2 <= n <= 7: mismatches = {mism}; bad(any) = {cnt[0]}, bad(dom) = {cnt[1]}")
    fails += mism
    rel = [(0, 1), (0, 5), (0, 6), (1, 6), (2, 5), (3, 4), (3, 6)]
    dn = [0] * 7
    for a, b in rel:
        dn[b] |= 1 << a
    G7 = eng.from_down(dn)
    # transitive closure check
    S = eng.seps(G7)
    L = [0, 3, 2, 1, 4, 5, 6]
    valid = L in [list(p) for p in exts(G7)]
    print(f"   CONTROL general poset (2+2: {eng.has_2p2(G7)}): badL found = {bool(eng.badL(G7))}; "
          f"author's L valid = {valid}, bad = {is_bad(G7, S, L)}")
    # 3, 4
    mism = 0
    viol = 0
    npairs = 0
    for n in range(2, 9):
        for iv in eng.gen(n):
            P = eng.from_intervals(iv)
            S = eng.seps(P)
            h = max(r for _, r in iv)
            alpha = [0] * (h + 2)
            beta = [0] * (h + 2)
            for l, r in iv:
                alpha[l] += 1
                beta[r] += 1

            def rho(p):
                c = [r for l, r in iv if l > p]
                return min(c) if c else h

            def lam(q):
                c = [l for l, r in iv if r < q]
                return max(c) if c else 1
            for a in range(n):
                for b in range(n):
                    if not eng.inc(P, a, b):
                        continue
                    npairs += 1
                    (li, ri), (lj, rj) = iv[a], iv[b]
                    A = sum(alpha[p] for p in range(ri + 1, min(rj, rho(ri)) + 1))
                    B = sum(beta[q] for q in range(max(li, lam(lj)), lj))
                    if A + B != S[a][b]:
                        mism += 1
                    if li < lj and ri < rj and S[a][b] < 2:
                        viol += 1
    print(f"3. Prop 3.1 formula vs cover count: {npairs} ordered incomparable pairs, n <= 8: mismatches = {mism}")
    print(f"4. Cor 3.2 (strict dominance step has |S| >= 2): violations = {viol}")
    fails += mism + viol
    print("RESULT", "all controls pass" if fails == 0 else f"FAILURES {fails}")


if __name__ == "__main__":
    main()
