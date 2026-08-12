#!/usr/bin/env python3
"""mg-6ff4 — shared machinery for MEASURING `ε_spec = 6·E[inv_e]/(n²−1)` ON THE BOUNDARY CLASS
`δ(P) = 1/3` EXACTLY.

IMPORTS NOTHING FROM THIS REPOSITORY.  Standard library only, exact `Fraction` on every verdict
path, no float anywhere a number is compared.  That is deliberate and it is the same reason
`lib7c78.py` gives: this arm re-measures a census `mg-7c78`'s `a5` already published, and a
re-measurement that reuses that arm's code cannot distinguish "the census is right" from "the two
runs share a bug".  `c0` cross-checks the census against `a5`'s printed table AND against
OEIS A000112, so a silent merge in the canonical form has two independent ways to be caught.

REPRESENTATION.  A poset on `n` elements is `(n, down)` where `down[i]` is a bitmask of the
elements strictly below `i`, transitively closed.  `i ∥ j` iff neither bit is set in the other's
mask.

THE ONE IDENTITY THIS FILE IS BUILT AROUND, and the reason no arm has to enumerate `L(P)` to get
`E[inv_e]`:

    e orients every incomparable pair toward its ≥ 2/3 side, so
        Pr[σ disagrees with e on {x,y}]  =  1 − max(p_xy, 1−p_xy)  =  min(p_xy, 1−p_xy),
    and by linearity
        E[inv_e]  =  Σ_{x ∥ y} min(p_xy, 1−p_xy)  =  m · q̄.

`c0` checks it against a brute-force enumeration of `L(P)` rather than trusting it, because the
step "e orients toward the majority side" is exactly the step that fails if `e` is not the
weak-majority order — which is `mg-6ff4`'s item 4 and the thing that would silently dominate every
number here.
"""

from fractions import Fraction
from itertools import combinations, permutations

THIRD = Fraction(1, 3)
TWO_THIRDS = Fraction(2, 3)

A000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999, 9: 183231}

# ------------------------------------------------------------------------------------------------
# poset basics
# ------------------------------------------------------------------------------------------------


def ups(n, down):
    u = [0] * n
    for i in range(n):
        for j in range(n):
            if down[j] >> i & 1:
                u[i] |= 1 << j
    return tuple(u)


def incomparable_pairs(n, down):
    return [(i, j) for i in range(n) for j in range(i + 1, n)
            if not (down[i] >> j & 1) and not (down[j] >> i & 1)]


def comparable(down, i, j):
    return bool(down[j] >> i & 1) or bool(down[i] >> j & 1)


def is_below(down, i, j):
    return bool(down[j] >> i & 1)


# ------------------------------------------------------------------------------------------------
# canonical form and generation
# ------------------------------------------------------------------------------------------------


def _colors(n, down, up):
    """Isomorphism-invariant refinement, used ONLY to shrink the permutation search.  Correctness
    of `canon` needs the colouring to be invariant, not strong."""
    full = (1 << n) - 1
    col = [(bin(down[i]).count("1"), bin(up[i]).count("1")) for i in range(n)]
    for _ in range(n):
        nxt = []
        for i in range(n):
            inc = full & ~down[i] & ~up[i] & ~(1 << i)
            nxt.append((col[i],
                        tuple(sorted(col[j] for j in range(n) if down[i] >> j & 1)),
                        tuple(sorted(col[j] for j in range(n) if up[i] >> j & 1)),
                        tuple(sorted(col[j] for j in range(n) if inc >> j & 1))))
        rank = {c: k for k, c in enumerate(sorted(set(nxt)))}
        new = [rank[c] for c in nxt]
        if new == col:
            break
        col = new
    return col


def canon(n, down):
    """Lexicographically least `down` tuple over all relabellings that respect the refinement."""
    up = ups(n, down)
    col = _colors(n, down, up)
    blocks = {}
    for i in range(n):
        blocks.setdefault(col[i], []).append(i)
    keys = sorted(blocks)
    best = [None]
    mapping = [0] * n

    def rec(bi):
        if bi == len(keys):
            nd = [0] * n
            for old in range(n):
                m, acc = down[old], 0
                while m:
                    b = m & -m
                    acc |= 1 << mapping[b.bit_length() - 1]
                    m ^= b
                nd[mapping[old]] = acc
            t = tuple(nd)
            if best[0] is None or t < best[0]:
                best[0] = t
            return
        blk = blocks[keys[bi]]
        base = sum(len(blocks[k]) for k in keys[:bi])
        for perm in permutations(range(len(blk))):
            for a, b in zip(blk, perm):
                mapping[a] = base + b
            rec(bi + 1)

    rec(0)
    return best[0]


def order_ideals(n, down):
    out = []
    for m in range(1 << n):
        ok = True
        mm = m
        while mm:
            b = mm & -mm
            if down[b.bit_length() - 1] & ~m:
                ok = False
                break
            mm ^= b
        if ok:
            out.append(m)
    return out


def has_antichain(n, down, k):
    """Is there an antichain of size `k`?  DFS over the incomparability graph's cliques."""
    if k <= 1:
        return n >= k
    full = (1 << n) - 1
    up = ups(n, down)
    inc = [full & ~down[i] & ~up[i] & ~(1 << i) for i in range(n)]

    def rec(cand, need, start):
        if need == 0:
            return True
        m = cand & ~((1 << start) - 1)
        while m:
            b = m & -m
            i = b.bit_length() - 1
            m ^= b
            if bin(cand & inc[i] & ~((1 << (i + 1)) - 1)).count("1") >= need - 1:
                if rec(cand & inc[i], need - 1, i + 1):
                    return True
        return False

    return rec(full, k, 0)


def width(n, down):
    w = 1
    while w < n and has_antichain(n, down, w + 1):
        w += 1
    return w


def all_classes(nmax, maxwidth=None):
    """{n: [down-tuples]} — every isomorphism class on `n` elements, `n = 1..nmax`.

    Generated by adding a MAXIMAL element whose strict down-set is an order ideal of the
    `(n−1)`-poset.  Complete: every finite poset has a maximal element, and deleting one leaves a
    poset in which that element's strict down-set was an ideal.

    `maxwidth` prunes to posets of width `≤ maxwidth`.  THE PRUNE IS SOUND AND COMPLETE FOR THAT
    CLASS, because width is monotone under induced subposets: deleting a maximal element cannot
    raise the width, so every width-`≤ W` poset on `n` elements arises from a width-`≤ W` poset on
    `n − 1`.  It is a RESTRICTED population and every arm that uses it says so at the table."""
    classes = {1: [(0,)]}
    for n in range(2, nmax + 1):
        seen = set()
        for down in classes[n - 1]:
            for ideal in order_ideals(n - 1, down):
                nd = tuple(list(down) + [ideal])
                if maxwidth is not None and has_antichain(n, nd, maxwidth + 1):
                    continue
                seen.add(canon(n, nd))
        classes[n] = sorted(seen)
    return classes


# ------------------------------------------------------------------------------------------------
# linear extensions: counting (DP over ideals) and enumeration (controls only)
# ------------------------------------------------------------------------------------------------


def count_ext(n, down):
    """|L(P)| by DP over order ideals.  Exact integer."""
    full = (1 << n) - 1
    memo = {0: 1}

    def f(m):
        v = memo.get(m)
        if v is not None:
            return v
        tot = 0
        mm = m
        while mm:
            b = mm & -mm
            i = b.bit_length() - 1
            mm ^= b
            rest = m ^ b
            if not (down[i] & ~rest):        # i is maximal inside m
                tot += f(rest)
        memo[m] = tot
        return tot

    return f(full)


def _closure_with(n, down, x, y):
    """`down` of the poset P + (x < y), transitively closed.  Requires x ∥ y."""
    up = ups(n, down)
    lo = down[x] | (1 << x)               # everything ≤ x
    hi = up[y] | (1 << y)                 # everything ≥ y
    nd = list(down)
    for j in range(n):
        if hi >> j & 1:
            nd[j] |= lo
    return tuple(nd)


def p_before(n, down, x, y, total=None):
    """Pr[x precedes y] as an exact Fraction, for x ∥ y."""
    if total is None:
        total = count_ext(n, down)
    return Fraction(count_ext(n, _closure_with(n, down, x, y)), total)


def linear_extensions(n, down):
    """Every linear extension as a tuple in position order.  Used by controls only."""
    out = []
    stack = [(0, ())]
    while stack:
        placed, seq = stack.pop()
        if len(seq) == n:
            out.append(seq)
            continue
        for i in range(n):
            if not (placed >> i & 1) and not (down[i] & ~placed):
                stack.append((placed | (1 << i), seq + (i,)))
    return out


# ------------------------------------------------------------------------------------------------
# delta, the boundary test, and the measurement
# ------------------------------------------------------------------------------------------------


def pair_bias_table(n, down, inc=None, total=None):
    """{(i,j): p_ij} over incomparable pairs, exact."""
    if inc is None:
        inc = incomparable_pairs(n, down)
    if total is None:
        total = count_ext(n, down)
    return {(i, j): p_before(n, down, i, j, total) for (i, j) in inc}


def delta_at_most(n, down, bound=THIRD):
    """(is_delta_le_bound, delta_or_None, p_table_or_None).

    Early-exits the moment ONE incomparable pair is more balanced than `bound`, which is what makes
    an exhaustive `n = 9` sweep affordable: `δ(P) ≤ 1/3` is rare, so almost every poset is rejected
    after one or two pair evaluations.  Returns the full table only when the poset survives."""
    inc = incomparable_pairs(n, down)
    if not inc:
        return False, None, None                      # a chain: no incomparable pair, δ undefined
    total = count_ext(n, down)
    best = Fraction(0)
    tbl = {}
    for (i, j) in inc:
        p = p_before(n, down, i, j, total)
        tbl[(i, j)] = p
        b = min(p, 1 - p)
        if b > bound:
            return False, None, None
        if b > best:
            best = b
    return True, best, tbl


def measure(n, down, tbl):
    """The ticket's quantities, exact.  `tbl` is the pair-bias table over incomparable pairs.

        m       = # incomparable pairs
        d       = m / C(n,2)                       incomparability density
        qbar    = mean over incomparable pairs of min(p, 1−p)
        Einv    = Σ min(p, 1−p)  =  m·q̄           = E[inv_e]  (see module docstring)
        eps     = 6·Einv/(n²−1)                    = ε_spec
    """
    m = len(tbl)
    Einv = sum(min(p, 1 - p) for p in tbl.values())
    qbar = Einv / m if m else None
    d = Fraction(m, n * (n - 1) // 2)
    eps = Fraction(6, 1) * Einv / (n * n - 1)
    return {"m": m, "d": d, "qbar": qbar, "Einv": Einv, "eps": eps}


# ------------------------------------------------------------------------------------------------
# the distinguished order e
# ------------------------------------------------------------------------------------------------


def majority_order(n, down, tbl, strict=False):
    """The weak-majority (`≥ 2/3`) order `e`, or None if the tournament has a cycle.

    Returns (e, unique, oriented_pairs, unoriented_pairs).  With `strict=True` only pairs at
    `> 2/3` are oriented — that is the version the no-3-cycle argument actually proves acyclic, and
    at `δ = 1/3` EXACTLY it is NOT total, which is `mg-6ff4`'s item 4.

    `unique` is True iff the topological order is forced at every step (in-degree-0 set of size 1
    throughout), i.e. iff `e` is canonical rather than one of several tie-breaks."""
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and is_below(down, i, j):
                adj[i][j] = True
    oriented = unoriented = 0
    for (x, y), p in tbl.items():
        hi = p if p >= 1 - p else 1 - p
        if (hi > TWO_THIRDS) if strict else (hi >= TWO_THIRDS):
            oriented += 1
            if p >= 1 - p:
                adj[x][y] = True
            else:
                adj[y][x] = True
        else:
            unoriented += 1
    indeg = [sum(1 for i in range(n) if adj[i][j]) for j in range(n)]
    order, unique = [], True
    avail = [j for j in range(n) if indeg[j] == 0]
    while avail:
        if len(avail) > 1:
            unique = False
        j = min(avail)
        avail.remove(j)
        order.append(j)
        for k in range(n):
            if adj[j][k]:
                indeg[k] -= 1
                if indeg[k] == 0:
                    avail.append(k)
    if len(order) != n:
        return None, False, oriented, unoriented
    return tuple(order), unique, oriented, unoriented


def inv_against(n, down, ext, rank, incomparable_only=True):
    """Inversions of `ext` against the reference order given by `rank`."""
    pos = {v: k for k, v in enumerate(ext)}
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            if incomparable_only and comparable(down, i, j):
                continue
            if (pos[i] < pos[j]) != (rank[i] < rank[j]):
                c += 1
    return c


# ------------------------------------------------------------------------------------------------
# ordinal-sum structure
# ------------------------------------------------------------------------------------------------


def ordinal_cuts(n, down):
    """Sizes `s` (1 ≤ s ≤ n−1) of proper down-sets `D` with every element of `D` below every
    element outside.  Such a `D` is determined by its size, so the search is over `s` alone."""
    up = ups(n, down)
    out = []
    for s in range(1, n):
        D = [x for x in range(n) if bin(up[x]).count("1") >= n - s]
        if len(D) != s:
            continue
        Dm = 0
        for x in D:
            Dm |= 1 << x
        if all((up[x] | Dm | (1 << x)) == (1 << n) - 1 for x in D):
            out.append(s)
    return out


def is_primitive(n, down):
    """No non-trivial ordinal-sum cut.  Equivalently (n ≥ 2) the incomparability graph is
    connected, which is `STATE.md` row 2's word for the same property."""
    return n >= 2 and not ordinal_cuts(n, down)


def ordinal_summands(n, down):
    """Decompose into ordinally-indecomposable (primitive) summands, in order, as
    `[(size, canonical down-tuple), ...]`.

    Every cut `D` is determined by its SIZE (an element of `D` is below every element outside, so
    `D` is exactly the set of `x` with `|up(x)| ≥ n − |D|`), so the filtration `∅ = D_0 ⊂ D_{s_1} ⊂
    … ⊂ D_n` given by the cut sizes is well defined and its consecutive differences are the
    summands."""
    up = ups(n, down)

    def Dset(s):
        return set() if s == 0 else set(x for x in range(n) if bin(up[x]).count("1") >= n - s)

    cuts = [0] + ordinal_cuts(n, down) + [n]
    out = []
    for a, b in zip(cuts, cuts[1:]):
        elts = sorted(Dset(b) - Dset(a))
        idx = {x: k for k, x in enumerate(elts)}
        nd = tuple(sum(1 << idx[y] for y in elts if is_below(down, y, x)) for x in elts)
        out.append((len(elts), canon(len(elts), nd)))
    return out
