#!/usr/bin/env python3
"""indep_tree.py (mg-e8b4) -- an independent re-implementation of tree.c's
search rules (single-pair certification only; no LP), for small D.

Design deliberately different from tree.c: no incremental layers, no
integer overflow guards, no pair tracking/hopeless dropping.  At every node
the down-sets of size k of the known poset are enumerated from scratch, and
P_J[a<b] is computed by brute-force DP with Fractions for EVERY incomparable
pair.  The complete-poset check computes delta exactly from scratch.

Output: per-depth node / certified / cut-pruned counts, to be compared with
`tree D MAXDEPTH 1 3 nolp` (identical counts are expected, since the rules
are identical; a mismatch means one of the two implementations is wrong).
"""
import sys
from fractions import Fraction
from functools import lru_cache

LO = Fraction(1, 3); HI = Fraction(2, 3)


def popcount(x):
    return bin(x).count("1")


def downsets_of_size(down, n, k):
    """all down-sets of size k of the poset on 0..n-1 (down[i] strict down-set)."""
    layer = {0}
    for _ in range(k):
        nxt = set()
        for I in layer:
            for z in range(n):
                if not I >> z & 1 and (down[z] & ~I) == 0:
                    nxt.add(I | 1 << z)
        layer = nxt
    return layer


def count_ext(down, J, a=None, b=None):
    """(#linear extensions of the subposet J, #those with a before b)."""
    elems = [i for i in range(64) if J >> i & 1]

    @lru_cache(maxsize=None)
    def f(I):   # number of ways to finish from down-set I (within J) ; returns (total, with a<b)
        if I == J:
            return (1, 1)
        tot = 0; good = 0
        for z in elems:
            if not I >> z & 1 and (down[z] & ~I & J) == 0 and (down[z] & J) == down[z]:
                if a is not None and z == b and not I >> a & 1:
                    t, _ = f(I | 1 << z); tot += t   # b placed before a: contributes 0 to good
                    continue
                t, g = f(I | 1 << z)
                tot += t
                if a is not None and z == a and not I >> b & 1:
                    good += t   # a before b in every continuation
                else:
                    good += g
        return (tot, good)
    return f(0)


def incomparable(down, n):
    return [(a, b) for b in range(n) for a in range(b) if not down[b] >> a & 1]


def cut_of(down, n, D):
    if n == 0:
        return 0
    k = max(n - D, popcount(down[n - 1]))
    return max(k, 0)


def certified(down, n, D):
    k = cut_of(down, n, D)
    Js = downsets_of_size(down, n, k)
    for (a, b) in incomparable(down, n):
        ok = True
        for J in Js:
            ai, bi = J >> a & 1, J >> b & 1
            if ai and bi:
                e, g = count_ext(down, J, a, b); r = Fraction(g, e)
            elif ai:
                r = Fraction(1)
            elif bi:
                r = Fraction(0)
            else:
                ok = False; break
            if not (LO <= r <= HI):
                ok = False; break
        if ok:
            return True
    return False


def decomposable(down, n):
    for c in range(1, n):
        low = (1 << c) - 1
        if all(down[i] & low == low for i in range(c, n)):
            return True
    return False


def delta_ok(down, n):
    full = (1 << n) - 1
    for (a, b) in incomparable(down, n):
        e, g = count_ext(down, full, a, b)
        if LO <= Fraction(g, e) <= HI:
            return True
    return False


def main():
    D = int(sys.argv[1]); MAXD = int(sys.argv[2])
    nodes = {}; cert = {}; cutp = {}; viol = []
    down = []; pic = []

    def visit(n):
        nodes[n] = nodes.get(n, 0) + 1
        if certified(down, n, D):
            cert[n] = cert.get(n, 0) + 1; return
        if n >= 2 and not decomposable(down, n) and not delta_ok(down, n):
            viol.append(list(down))
        if n >= MAXD:
            return
        lo = max(0, n - 2 * D + 1)
        window = list(range(lo, n))
        succ = [0] * n
        for i in range(n):
            for j in range(i + 1, n):
                if down[j] >> i & 1:
                    succ[i] |= 1 << j
        # every subset U of the window that is an up-set of size <= D
        for m in range(1 << len(window)):
            U = 0
            for t, pos in enumerate(window):
                if m >> t & 1:
                    U |= 1 << pos
            sz = popcount(U)
            if sz > D:
                continue
            if any(U >> j & 1 and (succ[j] & ~U) for j in window):
                continue
            if any(U >> j & 1 and pic[j] >= D for j in window):
                continue
            Dn = ((1 << n) - 1) & ~U
            if n > 0:
                dp = popcount(down[n - 1])
                if n - sz < dp or (n - sz == dp and Dn < down[n - 1]):
                    continue
            Nc = n + 1
            if sz == 0 and n >= 1:
                cutp[Nc] = cutp.get(Nc, 0) + 1; continue
            down.append(Dn); pic.append(sz)
            for j in range(n):
                if U >> j & 1:
                    pic[j] += 1
            c = Nc - 2 * D + 1; pruned = False
            if c >= 1:
                low = (1 << c) - 1
                if all(down[i] & low == low for i in range(c, Nc)):
                    pruned = True; cutp[Nc] = cutp.get(Nc, 0) + 1
            if not pruned:
                visit(Nc)
            for j in range(n):
                if U >> j & 1:
                    pic[j] -= 1
            down.pop(); pic.pop()

    visit(0)
    for d in sorted(set(nodes) | set(cutp)):
        print(f"depth {d:2d}  nodes {nodes.get(d,0):10d}  certified {cert.get(d,0):10d}  cutpruned {cutp.get(d,0):8d}")
    print(f"violations {len(viol)}")


if __name__ == "__main__":
    main()
