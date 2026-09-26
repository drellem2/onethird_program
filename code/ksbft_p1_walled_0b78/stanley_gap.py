#!/usr/bin/env python3
"""mg-0b78 (KSBFT-P1) §5 instrument: is the k=1 Stanley deficit QUANTISED on Pi_D?

For x in P, N_i(x) = #{linear extensions with x at position i}. Stanley: N_i^2 >= N_{i-1}N_{i+1}.
Question (the deep-dive's key lemma, 'QD_D'): is there kappa(D) > 0 with
    N_i^2 > N_{i-1}N_{i+1}  ==>  N_i^2 >= (1 + kappa(D)) N_{i-1}N_{i+1}   for every P in Pi_D ?
We record, per (D, n), the minimum over (P, x, i) of  N_i^2/(N_{i-1}N_{i+1}) - 1  among the
STRICT indices (N_{i-1}, N_{i+1} > 0 and the ratio > 1). If this minimum drifts to 0 as n grows at
fixed D, QD_D is false. Exact integers throughout. Deterministic (seeded).

Families: (a) exhaustive-by-construction C_p ⊔ C_q (mg-dcae refuter; range max(p,q));
(b) Fibonacci Z_m; (c) seeded random banded posets filtered to range <= D.
CONTROL: C_n ⊔ C_n at x = u_1, i = 2 must reproduce mg-dcae's exact deficit 1 + 1/(2n-1)."""
import random, sys
from fractions import Fraction as Fr
from lib import closure, rng, chain, disjoint_union


def slot_counts(n, lt, x):
    """exact N_i(x), i = 1..n, by DP over ideals (bitmasks)."""
    dm = [sum(1 << y for y in range(n) if lt[y][x2]) for x2 in range(n)]
    full = (1 << n) - 1
    fwd = {0: 1}  # number of ways to build ideal I from bottom
    layers = [dict() for _ in range(n + 1)]
    layers[0][0] = 1
    for s in range(n):
        for I, c in layers[s].items():
            for z in range(n):
                if not (I >> z) & 1 and (dm[z] & I) == dm[z]:
                    J = I | (1 << z)
                    layers[s + 1][J] = layers[s + 1].get(J, 0) + c
    # backward counts: number of ways to complete from ideal I to full
    bwd = {full: 1}
    for s in range(n - 1, -1, -1):
        for I in layers[s]:
            t = 0
            for z in range(n):
                if not (I >> z) & 1 and (dm[z] & I) == dm[z]:
                    t += bwd[I | (1 << z)]
            bwd[I] = t
    N = [0] * (n + 1)
    for s in range(n):
        for I, c in layers[s].items():
            if not (I >> x) & 1 and (dm[x] & I) == dm[x]:
                N[s + 1] += c * bwd[I | (1 << x)]
    return N[1:]


EQ = {"equal": 0, "equal_not_flat": 0}


def min_strict_deficit(n, lt):
    best = None
    for x in range(n):
        N = slot_counts(n, lt, x)
        for i in range(1, n - 1):
            a, b, c = N[i - 1], N[i], N[i + 1]
            if a > 0 and c > 0 and b * b == a * c:
                # Ma-Shenfeld k=1 as quoted by mg-48ab: interior equality forces a FLAT triple
                EQ["equal"] += 1
                if not (a == b == c):
                    EQ["equal_not_flat"] += 1
            assert b * b >= a * c, ("Stanley violated: instrument broken", N)
            if a > 0 and c > 0 and b * b > a * c:
                d = Fr(b * b, a * c) - 1
                if best is None or d < best[0]:
                    best = (d, x, i + 1)
    return best


def banded_random(n, w, p, rnd):
    rel = []
    for i in range(n):
        for j in range(i + 1, n):
            if j - i >= w or rnd.random() < p:
                rel.append((i, j))
    return n, closure(n, rel)


if __name__ == "__main__":
    # CONTROL (mg-dcae): C_n ⊔ C_n, x = u_1 (label 0), i = 2
    for m in (2, 3, 4, 5):
        n, lt = disjoint_union(chain(m), chain(m))
        N = slot_counts(n, lt, 0)
        got = Fr(N[1] ** 2, N[0] * N[2])
        assert got == 1 + Fr(1, 2 * m - 1), (m, N, got)
    print("control: C_m ⊔ C_m at x=u_1, i=2 gives 1 + 1/(2m-1) exactly for m=2..5 — OK")

    print("(a) C_p ⊔ C_q, range max(p,q): min strict deficit")
    for D in (2, 3, 4, 5, 6):
        vals = []
        for p in range(1, D + 1):
            n, lt = disjoint_union(chain(p), chain(D))
            b = min_strict_deficit(n, lt)
            if b: vals.append((b[0], p))
        v = min(vals)
        print(f"  D={D}: min over p<=D of min deficit = {v[0]} = {float(v[0]):.5f} (p={v[1]})")

    print("(b) Fibonacci Z_m (range 2)")
    for m in (4, 6, 8, 10, 12, 14):
        n, lt = m, closure(m, [(i, j) for i in range(m) for j in range(i + 2, m)])
        b = min_strict_deficit(n, lt)
        print(f"  m={m}: {b[0]} = {float(b[0]):.6f} at x={b[1]}, i={b[2]}")

    print("(c) seeded random banded posets, range <= D, per n: min strict deficit")
    rnd = random.Random(20260926)
    MINS = {}
    SAMPLES = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    for D in (2, 3, 4):
        for n in (8, 10, 12, 14, 16):
            best = None; kept = 0; tries = 0
            while kept < SAMPLES and tries < 200 * SAMPLES:
                tries += 1
                P = banded_random(n, D + 1, rnd.choice((0.2, 0.35, 0.5, 0.65)), rnd)
                if rng(*P) > D or rng(*P) == 0:
                    continue
                kept += 1
                b = min_strict_deficit(*P)
                if b and (best is None or b[0] < best[0]):
                    best = b
            print(f"  D={D} n={n:2d} kept={kept:4d}: min deficit = "
                  + (f"{best[0]} = {float(best[0]):.6f}" if best else "none"))
            MINS[(D, n)] = best[0]
    print(f"interior equalities seen: {EQ['equal']}, of which NOT flat: {EQ['equal_not_flat']}"
          " (Ma-Shenfeld k=1 as quoted by mg-48ab predicts 0)")
    # NEGATIVE CONTROL: a planted false floor must be caught by the same data
    planted = {2: Fr(1, 2), 3: Fr(1, 7), 4: Fr(1, 14)}
    caught = sum(1 for (D, n), v in MINS.items() if v < planted[D])
    print(f"negative control: planted floors kappa(2)>=1/2, kappa(3)>=1/7, kappa(4)>=1/14 violated "
          f"in {caught} of {len(MINS)} (D,n) cells -> {'CAUGHT' if caught else 'CONTROL DID NOT FIRE'}")
    assert caught
