#!/usr/bin/env python3
"""mg-b447 (KSBFT-F): exact checks behind docs/KSBFT-F-L4-step6-under-bounded-range.md.

Every figure is exact (fractions.Fraction) and deterministic: no clock, no randomness.
Sections:
  W   the witnesses' ranges (W*, W*_t, W, the N-poset/2+2, the fence = Fibonacci, the chain family)
  X   exhaustive over every naturally labelled poset on n <= NMAX elements (so every pair (P, e)):
        X1  tau(cut) <= 2*pi(P) - 1           (Prop 2.2: interface cover under range)
        X2  max_sigma K(sigma) <= tau(cut)    (mg-3af9 Theorem A, re-checked)
        X3  max_sigma K(sigma) <= pi(P)       (Lemma 2.1)
        X4  P[b before a] >= c(D) for x||y    (Lemma 2.3, the self-contained flip bound)
        X5  (EQ) identity h(x)-e(x) = sum_{later inc} P(y<x) - sum_{earlier inc} P(x<y)
  T   one-point transport on W*: which deletions v keep some balanced pair of P-v balanced in P
  C   firing controls: each check above is run against a claim known to be false and must FIRE
"""
import itertools
import sys
from fractions import Fraction as Fr

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6


def closure(n, rel):
    lt = [[False] * n for _ in range(n)]
    for i, j in rel:
        lt[i][j] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]:
                        lt[i][j] = True
    return lt


def les(n, lt):
    out = []

    def go(rem, seq):
        if not rem:
            out.append(tuple(seq))
            return
        for x in sorted(rem):
            if not any(lt[y][x] for y in rem if y != x):
                seq.append(x)
                go(rem - {x}, seq)
                seq.pop()

    go(frozenset(range(n)), [])
    return out


def inc(n, lt, x):
    return [y for y in range(n) if y != x and not lt[x][y] and not lt[y][x]]


def rng(n, lt):
    return max((len(inc(n, lt, x)) for x in range(n)), default=0)


def before(L, x, y):
    return Fr(sum(1 for s in L if s.index(x) < s.index(y)), len(L))


def delta(n, lt, L):
    best = Fr(0)
    for x in range(n):
        for y in range(x + 1, n):
            if not lt[x][y] and not lt[y][x]:
                p = before(L, x, y)
                best = max(best, min(p, 1 - p))
    return best


def tau(A, B, lt):
    """vertex cover number of the cross-incomparability bipartite graph (brute force)."""
    edges = [(a, b) for a in A for b in B if not lt[a][b] and not lt[b][a]]
    if not edges:
        return 0
    verts = sorted({v for e in edges for v in e})
    for r in range(1, len(verts) + 1):
        for S in itertools.combinations(verts, r):
            s = set(S)
            if all(a in s or b in s for a, b in edges):
                return r
    return len(verts)


def cD(D):
    """Lemma 2.3: P[b before a] >= 1/(1+f(D)),
    f(D) = sum_{j=1..D} sum_{r=0..2D-1-j} C(j-1+r, r)  (fibre bound of the block move)."""
    from math import comb
    f = sum(comb(j - 1 + r, r) for j in range(1, D + 1) for r in range(0, 2 * D - j))
    return Fr(1, 1 + f)


def wstar(a, b, t):
    """W*_t: c_1<..<c_{a-2} < {x,y}; B chain b_1<..<b_b; all A<B except x<b_1..x<b_t deleted."""
    c = list(range(a - 2))
    x, y = a - 2, a - 1
    B = list(range(a, a + b))
    rel = [(c[i], c[i + 1]) for i in range(len(c) - 1)]
    rel += [(c[-1], x), (c[-1], y)] if c else []
    rel += [(B[i], B[i + 1]) for i in range(b - 1)]
    rel += [(y, B[0])]
    rel += [(x, B[t])]  # x below b_{t+1}; x || b_1..b_t
    if c:
        rel += [(c[-1], B[0])]
    n = a + b
    return n, closure(n, rel), list(range(a)), B, x, y


def section_W():
    print("== W: witness ranges (range pi(P) = max_x #incomparables of x)")
    for (a, b, t) in [(3, 3, 2), (4, 4, 2), (4, 28, 2), (5, 9, 2), (4, 8, 3), (4, 9, 6), (4, 10, 7)]:
        n, lt, A, B, x, y = wstar(a, b, t)
        L = les(n, lt)
        EK = Fr(sum(len(set(A) - set(s[: len(A)])) for s in L), len(L))
        d1 = EK / min(len(A), len(B))
        pA = Fr(1, 2)  # P[A] = C_{a-2} (+) AC_2, two extensions
        print(
            f"W*_t a={a} b={b} t={t}: n={n} #LE={len(L)} range={rng(n, lt)} pi(x)={len(inc(n, lt, x))}"
            f" p_xy^P={before(L, x, y)} p_xy^P[A]={pA} EK={EK} Delta1={d1} Delta1*n={d1 * n}"
            f" tau={tau(A, B, lt)} delta(P)={delta(n, lt, L)}"
        )
    # 2+2 and the n=4 N-poset
    for name, n, rel in [
        ("2+2 {0<1,2<3}", 4, [(0, 1), (2, 3)]),
        ("N-poset {0<2,0<3,1<3}", 4, [(0, 2), (0, 3), (1, 3)]),
    ]:
        lt = closure(n, rel)
        L = les(n, lt)
        print(f"{name}: range={rng(n, lt)} delta={delta(n, lt, L)}")
    # the fence argmax of mg-f5be at n=8, and its identification with the Fibonacci poset
    rel8 = [(0, 2), (0, 3), (1, 3), (1, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (4, 7), (5, 7)]
    lt = closure(8, rel8)
    fib = all(lt[i][j] == (j - i >= 2) for i in range(8) for j in range(8) if i != j)
    print(f"fence n=8 (mg-f5be argmax): range={rng(8, lt)} equals Fibonacci Z_8 (i<j iff j-i>=2): {fib}")
    for m in range(4, 13):
        ltm = closure(m, [(i, j) for i in range(m) for j in range(i + 2, m)])
        print(f"  Z_{m}: range={rng(m, ltm)}", end="")
    print()
    for a, t in [(4, 1), (4, 2), (5, 3)]:
        n = 2 * a
        rel = [(i, i + 1) for i in range(a - 1)] + [(a + i, a + i + 1) for i in range(a - 1)]
        rel += [(a - 2, a)] + [(a - 1, a + t)]  # c_{a-1}<b_1 keeps c<b; c_a < b_{t+1}; c_a || b_1..b_t
        lt = closure(n, rel)
        print(f"C_a+C_a minus t crosses a={a} t={t}: range={rng(n, lt)} (expect t)")


def posets(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for mask in range(1 << len(pairs)):
        lt = [[False] * n for _ in range(n)]
        for k, (i, j) in enumerate(pairs):
            if mask >> k & 1:
                lt[i][j] = True
        ok = True
        for i, j in pairs:
            if lt[i][j]:
                for k in range(j + 1, n):
                    if lt[j][k] and not lt[i][k]:
                        ok = False
                        break
            if not ok:
                break
        if ok:
            yield lt


def section_X(claims):
    """claims: dict name -> callable used as the bound; the firing controls swap in false bounds."""
    print(f"== X: exhaustive over naturally labelled posets, n <= {NMAX}; e = identity, every prefix cut")
    stats = {k: [0, 0] for k in claims}  # [checked, violations]
    extra = {"max tau/(2D-1)": Fr(0), "posets": 0, "cuts": 0}
    for n in range(2, NMAX + 1):
        for lt in posets(n):
            D = rng(n, lt)
            if D == 0:
                continue
            extra["posets"] += 1
            L = les(n, lt)
            c = cD(D)
            # X4 and X5
            for x in range(n):
                for y in range(n):
                    if x != y and not lt[x][y] and not lt[y][x]:
                        stats["X4"][0] += 1
                        if before(L, y, x) < claims["X4"](D, c):
                            stats["X4"][1] += 1
                h = Fr(sum(s.index(x) for s in L), len(L))
                rhs = sum((before(L, y, x) for y in inc(n, lt, x) if y > x), Fr(0)) - sum(
                    (before(L, x, y) for y in inc(n, lt, x) if y < x), Fr(0)
                )
                stats["X5"][0] += 1
                if h - x != rhs:
                    stats["X5"][1] += 1
            for k in range(1, n):
                A, B = list(range(k)), list(range(k, n))
                extra["cuts"] += 1
                t = tau(A, B, lt)
                Ks = [len(set(A) - set(s[:k])) for s in L]
                mK = max(Ks)
                stats["X1"][0] += 1
                if t > claims["X1"](D):
                    stats["X1"][1] += 1
                extra["max tau/(2D-1)"] = max(extra["max tau/(2D-1)"], Fr(t, 2 * D - 1))
                stats["X2"][0] += 1
                if mK > claims["X2"](t):
                    stats["X2"][1] += 1
                stats["X3"][0] += 1
                if mK > claims["X3"](D):
                    stats["X3"][1] += 1
    return stats, extra


def section_T():
    print("== T: one-point transport on W*(a=4,b=4,t=2): delete v; does SOME balanced pair of P-v stay balanced in P?")
    n, lt, A, B, x, y = wstar(4, 4, 2)
    L = les(n, lt)

    def bal(nn, ltt, LL, pairs):
        out = []
        for (u, w) in pairs:
            p = before(LL, u, w)
            if Fr(1, 3) <= p <= Fr(2, 3):
                out.append((u, w))
        return out

    names = {0: "c1", 1: "c2", 2: "x", 3: "y", 4: "b1", 5: "b2", 6: "b3", 7: "b4"}
    for v in range(n):
        keep = [u for u in range(n) if u != v]
        idx = {u: i for i, u in enumerate(keep)}
        lts = [[lt[u][w] for w in keep] for u in keep]
        Ls = les(n - 1, lts)
        pairs = [(u, w) for u in keep for w in keep if u < w and not lt[u][w] and not lt[w][u]]
        bs = bal(n - 1, lts, Ls, [(idx[u], idx[w]) for u, w in pairs])
        bs = [(keep[i], keep[j]) for i, j in bs]
        surv = [pr for pr in bs if Fr(1, 3) <= before(L, *pr) <= Fr(2, 3)]
        print(
            f"  v={names[v]}: balanced pairs of P-v: {[(names[a], names[b]) for a, b in bs]}"
            f" -> balanced in P: {[(names[a], names[b]) for a, b in surv]}"
        )


def section_S():
    """One-point persistence: for every non-chain P (n>=3) is there a pair balanced in P AND in some
    P-v (v outside the pair)?  This is the one-point form of Step 6's transfer read in the only
    direction a minimal counterexample can use (a pair of some P-v that stays balanced in P)."""
    print(f"== S: one-point persistence, exhaustive over naturally labelled posets, 3 <= n <= {NMAX}")
    tot = fail = 0
    worst = None
    for n in range(3, NMAX + 1):
        for lt in posets(n):
            if rng(n, lt) == 0:
                continue
            L = les(n, lt)
            bal = [(x, y) for x in range(n) for y in range(x + 1, n)
                   if not lt[x][y] and not lt[y][x] and Fr(1, 3) <= before(L, x, y) <= Fr(2, 3)]
            tot += 1
            ok = False
            for v in range(n):
                keep = [u for u in range(n) if u != v]
                idx = {u: i for i, u in enumerate(keep)}
                lts = [[lt[u][w] for w in keep] for u in keep]
                Ls = None
                for (x, y) in bal:
                    if v in (x, y):
                        continue
                    if Ls is None:
                        Ls = les(n - 1, lts)
                    p = before(Ls, idx[x], idx[y])
                    if Fr(1, 3) <= p <= Fr(2, 3):
                        ok = True
                        break
                if ok:
                    break
            if not ok:
                fail += 1
                if worst is None:
                    worst = (n, [(i, j) for i in range(n) for j in range(n) if lt[i][j]])
    print(f"  non-chains checked (labelled): {tot}   with NO persistent pair: {fail}")
    if worst:
        print(f"  first failure: n={worst[0]} relations={worst[1]}")


def section_c():
    print("== c(D): the Lemma 2.3 flip constant, against 2^(1-2D) and KSBFT's q2 = (D+1)^(-2(D+1))")
    bad = 0
    for D in range(1, 21):
        c = cD(D)
        if c < Fr(1, 2 ** (2 * D - 1)):
            bad += 1
        if D <= 6:
            print(f"  D={D}: c(D)=1/{1 / c}  2^(1-2D)=1/{2 ** (2 * D - 1)}  q2=1/{(D + 1) ** (2 * (D + 1))}")
    print(f"  D=1..20: c(D) >= 2^(1-2D) violations: {bad}")


def main():
    section_c()
    section_W()
    true_claims = {
        "X1": lambda D: 2 * D - 1,
        "X2": lambda t: t,
        "X3": lambda D: D,
        "X4": lambda D, c: c,
        "X5": None,
    }
    stats, extra = section_X(true_claims)
    print(f"  posets with pi>=1 (labelled, natural): {extra['posets']}   prefix cuts: {extra['cuts']}")
    for k in ["X1", "X2", "X3", "X4", "X5"]:
        print(f"  {k}: checked {stats[k][0]}, violations {stats[k][1]}")
    print(f"  max tau/(2D-1) observed: {extra['max tau/(2D-1)']}")
    section_T()
    section_S()
    print("== C: firing controls (each swaps in a bound that is FALSE; each must report violations > 0)")
    false_claims = {
        "X1": lambda D: D - 1,        # tau <= D-1 : false (W*-type cuts have tau = 1 at D = 1? see count)
        "X2": lambda t: t - 1,        # K <= tau-1 : false wherever tau > 0 is attained by K
        "X3": lambda D: D - 1,        # K <= D-1   : false (2-antichain, D=1, K=1)
        "X4": lambda D, c: Fr(1, 2),  # P[b<a] >= 1/2 : false (chain-with-a-float)
        "X5": None,
    }
    stats, _ = section_X(false_claims)
    for k in ["X1", "X2", "X3", "X4"]:
        v = stats[k][1]
        print(f"  control {k}: violations {v} -> {'FIRES' if v > 0 else 'DOES NOT FIRE (instrument broken)'}")


if __name__ == "__main__":
    main()
