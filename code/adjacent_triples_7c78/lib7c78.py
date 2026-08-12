#!/usr/bin/env python3
"""mg-7c78 — shared machinery: poset enumeration up to isomorphism, linear extensions, and
the configuration statistics Daniel's observation is about.

IMPORTS NOTHING FROM THIS REPOSITORY.  Standard library only, exact integers/Fractions on
every verdict path.  That is deliberate: the statements being checked here are compared against
`FACTS.md` F1/F2 and against `mg-92e6`, and a check that reuses those arcs' code cannot
distinguish "the fact is true" from "the two implementations share a bug".

REPRESENTATION.  A poset on `n` elements is `(n, down)` where `down[i]` is a bitmask of the
elements strictly below `i`, transitively closed.  `up[i]` is derived.  Elements are
`0 .. n-1`; `i` and `j` are incomparable iff neither bit is set in the other's mask.

WHY ISOMORPHISM CLASSES.  Every quantity measured here is an isomorphism invariant (all of them
are functionals of the uniform measure on `L(P)` under a relabelling-equivariant definition), so
classes are the correct population and are ~3000x cheaper than labeled posets at `n = 7`.  The
risk this buys is that a BROKEN canonical form silently MERGES classes, shrinking the population
while every failure count stays 0 -- so `a0` checks the class counts against OEIS A000112
(1, 2, 5, 16, 63, 318, 2045, 16999) before any arm is allowed to trust them.
"""

from fractions import Fraction
from itertools import permutations

# ---------------------------------------------------------------------------------------------
# posets
# ---------------------------------------------------------------------------------------------


def ups(n, down):
    """up[i] = bitmask of elements strictly above i."""
    u = [0] * n
    for i in range(n):
        for j in range(n):
            if down[j] >> i & 1:
                u[i] |= 1 << j
    return tuple(u)


def incomparable_pairs(n, down):
    out = []
    for i in range(n):
        for j in range(i + 1, n):
            if not (down[i] >> j & 1) and not (down[j] >> i & 1):
                out.append((i, j))
    return out


def is_below(down, i, j):
    """True iff i <_P j."""
    return bool(down[j] >> i & 1)


def comparable(down, i, j):
    return bool(down[j] >> i & 1) or bool(down[i] >> j & 1)


def _refine_colors(n, down, up):
    """Iterated Weisfeiler-Leman-style refinement, used only to SHRINK the permutation search
    for the canonical form.  Correctness of `canon` does not depend on the refinement being
    strong -- only on it being ISOMORPHISM-INVARIANT, which it is, because every ingredient is
    a multiset over neighbours."""
    col = [(bin(down[i]).count("1"), bin(up[i]).count("1")) for i in range(n)]
    full = (1 << n) - 1
    for _ in range(n):
        new = []
        for i in range(n):
            inc = full & ~down[i] & ~up[i] & ~(1 << i)
            new.append((
                col[i],
                tuple(sorted(col[j] for j in range(n) if down[i] >> j & 1)),
                tuple(sorted(col[j] for j in range(n) if up[i] >> j & 1)),
                tuple(sorted(col[j] for j in range(n) if inc >> j & 1)),
            ))
        # compress to small ints so the tuples do not grow without bound
        order = {c: k for k, c in enumerate(sorted(set(new)))}
        nxt = [order[c] for c in new]
        if nxt == col:
            break
        col = nxt
    return col


def canon(n, down):
    """Canonical form: the lexicographically least `down` tuple over all relabellings.

    The search is restricted to permutations that respect the refined colouring, which is sound
    because the colouring is an isomorphism invariant: any isomorphism maps a vertex to one of
    the same colour, so the least encoding is attained inside that restricted set."""
    up = ups(n, down)
    col = _refine_colors(n, down, up)
    blocks = {}
    for i in range(n):
        blocks.setdefault(col[i], []).append(i)
    keys = sorted(blocks)
    # positions in the canonical labelling are handed out block by block, in colour order
    slots = []
    for k in keys:
        slots.extend(blocks[k])

    best = None
    # iterate over the product of within-block permutations
    def gen(bi, mapping):
        nonlocal best
        if bi == len(keys):
            nd = [0] * n
            for old in range(n):
                m = down[old]
                acc = 0
                while m:
                    b = m & -m
                    acc |= 1 << mapping[b.bit_length() - 1]
                    m ^= b
                nd[mapping[old]] = acc
            t = tuple(nd)
            if best is None or t < best:
                best = t
            return
        blk = blocks[keys[bi]]
        base = sum(len(blocks[k]) for k in keys[:bi])
        for perm in permutations(range(len(blk))):
            for a, b in zip(blk, perm):
                mapping[a] = base + b
            gen(bi + 1, mapping)

    gen(0, [0] * n)
    return best


def order_ideals(n, down):
    """All down-sets (order ideals) of the poset, as bitmasks."""
    out = []
    for m in range(1 << n):
        ok = True
        mm = m
        while mm:
            b = mm & -mm
            i = b.bit_length() - 1
            if down[i] & ~m:
                ok = False
                break
            mm ^= b
        if ok:
            out.append(m)
    return out


def all_classes(nmax):
    """{n: [down-tuples]} -- every isomorphism class of poset on n elements, n = 1..nmax.

    Generated by adding a MAXIMAL element whose strict down-set is an order ideal of the
    (n-1)-poset.  Complete because every finite poset has a maximal element, and deleting one
    leaves a poset in which that element's strict down-set was an ideal."""
    classes = {1: [(0,)]}
    for n in range(2, nmax + 1):
        seen = set()
        for down in classes[n - 1]:
            for ideal in order_ideals(n - 1, down):
                nd = list(down) + [ideal]
                seen.add(canon(n, tuple(nd)))
        classes[n] = sorted(seen)
    return classes


# ---------------------------------------------------------------------------------------------
# linear extensions and the configuration statistics
# ---------------------------------------------------------------------------------------------


def linear_extensions(n, down):
    """Every linear extension, as a tuple of elements in position order 0 .. n-1."""
    out = []
    stack = [(0, ())]
    while stack:
        placed, seq = stack.pop()
        if len(seq) == n:
            out.append(seq)
            continue
        for i in range(n):
            if not (placed >> i & 1) and (down[i] & ~placed) == 0:
                stack.append((placed | (1 << i), seq + (i,)))
    return out


def pair_probs(n, down, exts):
    """p[(i,j)] = Pr[i before j] for i < j, as exact Fractions.  Comparable pairs included."""
    N = len(exts)
    cnt = {}
    for i in range(n):
        for j in range(i + 1, n):
            cnt[(i, j)] = 0
    for e in exts:
        pos = [0] * n
        for k, x in enumerate(e):
            pos[x] = k
        for i in range(n):
            for j in range(i + 1, n):
                if pos[i] < pos[j]:
                    cnt[(i, j)] += 1
    return {k: Fraction(v, N) for k, v in cnt.items()}


def delta(n, down, p):
    """delta(P) = max over INCOMPARABLE pairs of min(p, 1-p).  None if no incomparable pair."""
    inc = incomparable_pairs(n, down)
    if not inc:
        return None
    return max(min(p[(i, j)], 1 - p[(i, j)]) for (i, j) in inc)


def value_transposition_legal(n, down, ext, x, y):
    """Is the permutation obtained from `ext` by exchanging the VALUES x and y still a linear
    extension?  Requires x || y.  True iff every element strictly BETWEEN them in `ext` is
    incomparable to both.

    This is the event `E_xy` of P9.  Its k=2 slice is `x, y adjacent` (F1 / mg-92e6); its k=3
    slice is `x, y inside a free consecutive triple` (Daniel's reading R1-as-a-bound)."""
    pos = {v: k for k, v in enumerate(ext)}
    a, b = sorted((pos[x], pos[y]))
    for k in range(a + 1, b):
        z = ext[k]
        if comparable(down, z, x) or comparable(down, z, y):
            return False
    return True


def consecutive_triples(n, ext):
    """[(k, (a,b,c))] -- the n-2 blocks of three consecutive positions, in position order."""
    return [(k, (ext[k], ext[k + 1], ext[k + 2])) for k in range(n - 2)]


def free_set(down, elts):
    """Are these elements pairwise incomparable?"""
    for a in range(len(elts)):
        for b in range(a + 1, len(elts)):
            if comparable(down, elts[a], elts[b]):
                return False
    return True


def aligned_with(reference_rank, elts):
    """Are `elts` (in the order given) in the same relative order as the reference order?"""
    r = [reference_rank[x] for x in elts]
    return all(r[i] < r[i + 1] for i in range(len(r) - 1))


def population(nmax_exhaustive, sample_n=None, sample_k=0, seed=0):
    """Yield (n, down, exhaustive_flag) over the declared population.

    Exhaustive over every isomorphism class up to `nmax_exhaustive`; then, if `sample_n` is
    given, `sample_k` classes drawn without replacement at that n with the stated seed."""
    classes = all_classes(sample_n if sample_n else nmax_exhaustive)
    for n in range(1, nmax_exhaustive + 1):
        for down in classes[n]:
            yield n, down, True
    if sample_n and sample_n > nmax_exhaustive:
        import random
        rng = random.Random(seed)
        pool = classes[sample_n]
        k = min(sample_k, len(pool))
        for down in rng.sample(pool, k):
            yield sample_n, down, False


A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}
