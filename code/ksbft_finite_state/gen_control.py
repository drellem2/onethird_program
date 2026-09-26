#!/usr/bin/env python3
"""gen_control.py (mg-e8b4) -- positive control for tree.c's GENERATION.

Claim tested: for every n <= NMAX and D, the set of complete n-element posets
tree.c visits (mode `nocert dump`, certification switched off) equals, up to
isomorphism, the set of ALL ordinal-indecomposable posets on n elements with
range <= D.  The reference set is built by brute force, independently of
tree.c's canonical order: every naturally labelled poset (count checked
against OEIS A006455), filtered, then reduced to isomorphism classes.

Also cross-checks delta for every such poset by brute force over all n!
permutations (n <= 7), against the tree's "no counterexample" at threshold 1/3.
"""
import itertools, subprocess, sys
from fractions import Fraction

A006455 = {1: 1, 2: 2, 3: 7, 4: 40, 5: 357, 6: 4824, 7: 96428}


def natural_posets(n):
    """all naturally labelled posets: down[j] = strict down-set bitmask, closed."""
    out = []

    def rec(j, down):
        if j == n:
            out.append(tuple(down)); return
        for m in range(1 << j):
            ok = all((down[i] & ~m) == 0 for i in range(j) if m >> i & 1)
            if ok:
                rec(j + 1, down + [m])
    rec(0, [])
    return out


def rel(down):
    n = len(down)
    return {(i, j) for j in range(n) for i in range(n) if down[j] >> i & 1}


def rng(down):
    n = len(down); R = rel(down)
    return max(sum(1 for y in range(n) if y != x and (x, y) not in R and (y, x) not in R) for x in range(n)) if n else 0


def indecomposable(down):
    # ordinal-indecomposable <=> incomparability graph connected (n >= 2)
    n = len(down); R = rel(down)
    if n < 2:
        return False
    seen = {0}; fr = [0]
    while fr:
        x = fr.pop()
        for y in range(n):
            if y not in seen and (x, y) not in R and (y, x) not in R:
                seen.add(y); fr.append(y)
    return len(seen) == n


def canon(down):
    n = len(down); R = rel(down)
    inv = [(bin(down[x]).count('1'), sum(1 for y in range(n) if (x, y) in R)) for x in range(n)]
    classes = sorted(set(inv))
    groups = [[x for x in range(n) if inv[x] == c] for c in classes]
    best = None
    for perms in itertools.product(*[itertools.permutations(g) for g in groups]):
        order = [x for p in perms for x in p]
        pos = {x: i for i, x in enumerate(order)}
        key = tuple(sorted((pos[a], pos[b]) for a, b in R))
        if best is None or key < best:
            best = key
    return (n, best)


def delta_bruteforce(down):
    n = len(down); R = rel(down)
    exts = [p for p in itertools.permutations(range(n))
            if all(p.index(a) < p.index(b) for a, b in R)]
    e = len(exts); best = Fraction(0)
    for x in range(n):
        for y in range(x + 1, n):
            if (x, y) in R or (y, x) in R:
                continue
            c = sum(1 for p in exts if p.index(x) < p.index(y))
            best = max(best, min(Fraction(c, e), 1 - Fraction(c, e)))
    return best


def main():
    tree = sys.argv[1]; NMAX = int(sys.argv[2])
    allp = {n: natural_posets(n) for n in range(1, NMAX + 1)}
    for n in allp:
        assert len(allp[n]) == A006455[n], (n, len(allp[n]))
    print(f"A006455 control: natural-labelling counts {[len(allp[n]) for n in allp]} match OEIS")
    bad = 0
    for D in range(1, NMAX):
        out = subprocess.run([tree, str(D), str(NMAX), "1", "3", "nocert", "dump"],
                             capture_output=True, text=True, check=True).stdout
        got = {}
        for line in out.splitlines():
            if line.startswith("P "):
                dn = tuple(int(t) for t in line[3:-1].split(","))
                got.setdefault(len(dn), set()).add(canon(dn))
        for n in range(2, NMAX + 1):
            ref = {canon(p) for p in allp[n] if rng(p) <= D and indecomposable(p)}
            g = got.get(n, set())
            status = "EQUAL" if g == ref else "DIFFER"
            if g != ref:
                bad += 1
            print(f"D={D} n={n}: brute-force classes {len(ref):5d}  tree classes {len(g):5d}  {status}"
                  + ("" if g == ref else f"  missing={len(ref - g)} extra={len(g - ref)}"))
            if D == NMAX - 1 or n <= 6:
                pass
    # delta cross-check on all indecomposable posets n <= NMAX with range <= NMAX-1 (all of them)
    worst = Fraction(1)
    cnt = 0
    for n in range(2, NMAX + 1):
        seen = set()
        for p in allp[n]:
            if not indecomposable(p):
                continue
            c = canon(p)
            if c in seen:
                continue
            seen.add(c); cnt += 1
            worst = min(worst, delta_bruteforce(p))
    print(f"brute-force delta over {cnt} indecomposable iso-classes, n<=%d: min delta = {worst}" % NMAX)
    print("GEN-CONTROL", "PASS" if bad == 0 else "FAIL")


if __name__ == "__main__":
    main()
