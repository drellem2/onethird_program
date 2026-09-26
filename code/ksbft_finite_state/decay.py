#!/usr/bin/env python3
"""decay.py (mg-e8b4) -- EMPIRICAL: how fast does the certification hull of a
bottom pair shrink with the cut k?  (Q3 of the ticket.)

For a pair (a,b) and cut k, hull_k = [min_J P_J[a<b], max_J P_J[a<b]] over
the down-sets J of size k (Lemma 3).  Its width w_k is the quantity whose
decay makes the finite check terminate.  Lemma 6 (Dobrushin) proves
w_{k+2D} <= tau_D * w_k with tau_D = 1 - (D+1)^(-2D); this script measures
the actual per-2D-block ratio on (i) the Fibonacci poset (range 2) and
(ii) random range-<=D posets built in canonical order.
"""
import random, math, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from indep_tree import downsets_of_size, count_ext
from fractions import Fraction


def hull(down, n, a, b, k):
    vals = []
    for J in downsets_of_size(down, n, k):
        ai, bi = J >> a & 1, J >> b & 1
        if ai and bi:
            e, g = count_ext(down, J, a, b); vals.append(Fraction(g, e))
        elif ai:
            vals.append(Fraction(1))
        elif bi:
            vals.append(Fraction(0))
        else:
            return None
    return min(vals), max(vals)


def fib(n):
    return [sum(1 << i for i in range(j - 1)) for j in range(n)]   # x_i < x_j iff j-i >= 2


def rand_poset(n, D, rng):
    """random canonical range-<=D poset (a random walk in tree.c's generation rules)."""
    down, pic = [], []
    for m in range(n):
        lo = max(0, m - 2 * D + 1)
        for _ in range(200):
            U = 0; sz = 0
            for pos in range(m - 1, lo - 1, -1):
                succ = sum(1 << j for j in range(pos + 1, m) if down[j] >> pos & 1)
                if sz < D and pic[pos] < D and (succ & ~U) == 0 and rng.random() < 0.55:
                    U |= 1 << pos; sz += 1
            Dn = ((1 << m) - 1) & ~U
            if m == 0 or sz > 0:
                dp = bin(down[m - 1]).count("1") if m else 0
                if m == 0 or m - sz > dp or (m - sz == dp and Dn >= down[m - 1]):
                    break
        else:
            return None
        down.append(Dn); pic.append(sz)
        for j in range(m):
            if U >> j & 1:
                pic[j] += 1
    return down


def report(name, down, n, a, b, D):
    print(f"== {name}: pair ({a},{b}), n={n}, range<= {D}")
    prev = None
    for k in range(1, n - D + 1):
        h = hull(down, n, a, b, k)
        if h is None:
            continue
        w = h[1] - h[0]
        line = f"  k={k:2d} hull=[{float(h[0]):.6f}, {float(h[1]):.6f}] width={float(w):.3e}"
        if prev is not None and prev > 0 and w > 0:
            line += f"  ratio/step={float(w/prev):.4f}"
        print(line); prev = w


def main():
    report("Fibonacci F (x_i<x_j iff j-i>=2)", fib(22), 22, 0, 1, 2)
    rng = random.Random(20260926)
    for D in (3, 4, 5):
        got = 0
        while got < 2:
            n = 18 if D < 5 else 16
            down = rand_poset(n, D, rng)
            if down is None:
                continue
            pairs = [(a, b) for b in range(4) for a in range(b) if not down[b] >> a & 1]
            if not pairs:
                continue
            report(f"random canonical poset, D={D}, seed-walk #{got}", down, n, pairs[0][0], pairs[0][1], D)
            got += 1
    for D in (2, 3, 4, 5, 7):
        print(f"Lemma 6 bound: D={D}: tau_D = 1 - (D+1)^(-2D) = 1 - {(D + 1) ** (-2 * D):.3e} per block of 2D cuts")


if __name__ == "__main__":
    main()
