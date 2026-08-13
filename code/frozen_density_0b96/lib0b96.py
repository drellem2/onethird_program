#!/usr/bin/env python3
"""mg-0b96 — shared machinery for THE NO-HUNT ON A FROZEN-CLASS UPPER BOUND FOR THE
INCOMPARABILITY DENSITY `d(P) = m/C(n,2)`.

THE QUESTION.  `STATE.md` row 8's supply bound is `ε_sup = d·n/(n+1)` (`mg-0e8c`), so the wall is
already down at `d ≲ ε_dem ≈ 2×10⁻²` and the open region is the DENSE one.  Three arcs — `mg-8b32`
(fiber tightness), `mg-6ff4` (boundary density), `mg-c776` (image geometry) — have each concluded
that `d` UNDER THE FROZEN HYPOTHESIS is the only remaining lever, and none asked whether the lever
can exist.  This directory asks.

WHAT IS IMPORTED AND WHY, said here rather than left to a reader of the import line.  Poset
enumeration, `δ`, exact pair biases and `width` come from `code/boundary_epsilon_6ff4/lib6ff4.py`.
That is a REUSE OF A CONTROLLED PRIMITIVE, not a re-measurement: `mg-6ff4`'s `c0` already checks
that enumerator against OEIS A000112 and its pair-bias identity against brute-force enumeration of
`L(P)`.  `d0` re-checks BOTH here anyway — the class counts against A000112 and `δ` against a
brute-force count over every linear extension — because an import whose controls live in another
directory is an unchecked dependency from this directory's point of view, and this arm's whole
subject is a claim nobody re-checked.

WHAT IS NOT IMPORTED.  Every predicate below (`thinness`, `height`, `is_N_free`, `is_semiorder`,
`cover_graph_is_forest`, `is_rigid`) is written here, because none of them exists anywhere in this
repository and each one is a LITERATURE CLASS whose definition is the thing that could be wrong.
`d0` plants a defect in each and checks it is caught.

REPRESENTATION.  `lib6ff4`'s: a poset on `n` elements is `(n, down)` with `down[i]` a bitmask of
the elements strictly below `i`, transitively closed.
"""

import os
import sys
from fractions import Fraction
from itertools import permutations

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "code", "boundary_epsilon_6ff4"))
import lib6ff4 as L                                                        # noqa: E402

THIRD = Fraction(1, 3)

# `ε_dem ≈ 2×10⁻²` — STATE.md row 8 and mg-33f5 §3's repaired calibration.  Carried as an exact
# rational because every verdict path here is exact; the SOURCE of the number is a calibration in
# another document and this file does not re-derive it.
EPS_DEM = Fraction(2, 100)


# ------------------------------------------------------------------------------------------------
# density, and the two quantities row 8 reads it through
# ------------------------------------------------------------------------------------------------


def density(n, down):
    """`d(P) = m/C(n,2)`, the incomparability density.  Exact.

    `n ≤ 1` has no pairs at all and `0/0` is not a density; it returns `0` rather than raising,
    and every arm here starts its populations at `n = 2` so the convention is never load-bearing."""
    if n < 2:
        return Fraction(0)
    return Fraction(len(L.incomparable_pairs(n, down)), n * (n - 1) // 2)


def eps_sup(n, d):
    """`ε_sup = d·n/(n+1)` — mg-0e8c's supply bound, STATE.md:123.  Exact."""
    return Fraction(d) * Fraction(n, n + 1)


def d_needed(n, eps=EPS_DEM):
    """The density ceiling that would put `ε_sup` at or below `eps`: `d ≤ eps·(n+1)/n`."""
    return Fraction(eps) * Fraction(n + 1, n)


# ------------------------------------------------------------------------------------------------
# the structural predicates — one per literature class exclusion (mg-33f5 §2's table)
# ------------------------------------------------------------------------------------------------


def inc_degrees(n, down):
    """Per-element incomparability degree: how many elements each one is incomparable with."""
    up = L.ups(n, down)
    full = (1 << n) - 1
    return [bin(full & ~down[i] & ~up[i] & ~(1 << i)).count("1") for i in range(n)]


def thinness(n, down):
    """`k` such that `P` is `k`-thin and no smaller: the MAXIMUM incomparability degree.

    Peczarski, Order 25 (2008): the conjecture holds for posets in which "every element is
    incomparable with at most six others", i.e. `thinness(P) ≤ 6`."""
    return max(inc_degrees(n, down)) if n else 0


def height(n, down):
    """Longest chain, counted in ELEMENTS (a single element has height 1)."""
    h = [0] * n
    for i in sorted(range(n), key=lambda i: bin(down[i]).count("1")):
        best = 0
        for j in range(n):
            if down[i] >> j & 1:
                best = max(best, h[j])
        h[i] = best + 1
    return max(h) if n else 0


def covers(n, down):
    """The covering relation as a set of `(a, b)` with `a < b` and nothing strictly between."""
    out = set()
    for b in range(n):
        for a in range(n):
            if down[b] >> a & 1:
                mid = down[b] & ~down[a] & ~(1 << a)
                if not any((mid >> c & 1) and (down[c] >> a & 1) for c in range(n)):
                    out.add((a, b))
    return out


def cover_graph_is_forest(n, down):
    """Is the Hasse diagram, read as an UNDIRECTED graph, acyclic?

    Zaguia (arXiv:1610.00809): the conjecture holds when the cover graph is a forest."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (a, b) in covers(n, down):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


def is_N_free(n, down):
    """No `N` in the HASSE DIAGRAM: no covers `a ≺ c`, `b ≺ c`, `b ≺ d` with `a ≠ b`, `c ≠ d`.

    Zaguia, Electron. J. Combin. 19(2) #P29 (2012): the conjecture holds for `N`-free ordered sets.
    ⚠️ The `N` is read on COVERS, which is the standard reading for "N-free ordered set"; read on
    the order relation instead, the class would be different and smaller."""
    cv = covers(n, down)
    up_cov = {}
    for (a, c) in cv:
        up_cov.setdefault(a, set()).add(c)
    down_cov = {}
    for (a, c) in cv:
        down_cov.setdefault(c, set()).add(a)
    for c in down_cov:
        for b in down_cov[c]:
            for a in down_cov[c]:
                if a == b:
                    continue
                if any(d != c for d in up_cov.get(b, ())):
                    return False
    return True


def is_semiorder(n, down):
    """No induced `2+2` and no induced `3+1`.  (Scott–Suppes; the conjecture holds for semiorders,
    Brightwell — listed in mg-33f5 §2.)"""
    def lt(a, b):
        return bool(down[b] >> a & 1)

    def cmpb(a, b):
        return lt(a, b) or lt(b, a)

    for a in range(n):
        for b in range(n):
            if not lt(a, b):
                continue
            for c in range(n):
                if c in (a, b):
                    continue
                for d in range(n):
                    if d in (a, b, c) or not lt(c, d):
                        continue
                    if not cmpb(a, c) and not cmpb(a, d) and not cmpb(b, c) and not cmpb(b, d):
                        return False                                        # 2+2
    for a in range(n):
        for b in range(n):
            if not lt(a, b):
                continue
            for c in range(n):
                if not lt(b, c):
                    continue
                for d in range(n):
                    if d in (a, b, c):
                        continue
                    if not cmpb(d, a) and not cmpb(d, b) and not cmpb(d, c):
                        return False                                        # 3+1
    return True


def automorphisms(n, down, cap=None):
    """Every order automorphism, as permutations.  `cap` stops the search early.

    The search is restricted to permutations respecting `lib6ff4._colors`, which is an isomorphism
    INVARIANT refinement — so no automorphism can be missed by the restriction, only work."""
    col = L._colors(n, down, L.ups(n, down))
    blocks = {}
    for i in range(n):
        blocks.setdefault(col[i], []).append(i)
    keys = sorted(blocks)
    mapping = [0] * n
    out = []

    def rec(bi):
        if cap is not None and len(out) >= cap:
            return
        if bi == len(keys):
            for old in range(n):
                m, acc = down[old], 0
                while m:
                    b = m & -m
                    acc |= 1 << mapping[b.bit_length() - 1]
                    m ^= b
                if acc != down[mapping[old]]:
                    return
            out.append(tuple(mapping))
            return
        blk = blocks[keys[bi]]
        for perm in permutations(blk):
            for a, b in zip(blk, perm):
                mapping[a] = b
            rec(bi + 1)

    rec(0)
    return out


def is_rigid(n, down):
    """Trivial automorphism group.

    Peczarski (2017): the conjecture holds for posets with a non-trivial automorphism, so a
    counterexample must be RIGID.  Two elements with the same strict up-set and down-set are
    swapped by an automorphism, which is the cheap special case `d4` uses."""
    if all(len(v) == 1 for v in _blocks(n, down).values()):
        return True                       # discrete refinement ⟹ every automorphism fixes every
    return len(automorphisms(n, down, cap=2)) <= 1     # element, so the group is trivial


def _blocks(n, down):
    col = L._colors(n, down, L.ups(n, down))
    b = {}
    for i in range(n):
        b.setdefault(col[i], []).append(i)
    return b


# ------------------------------------------------------------------------------------------------
# the class-exclusion table, and what it does to a poset
# ------------------------------------------------------------------------------------------------

#: name -> (predicate, citation).  Every row is a class for which the (1/3)–(2/3) conjecture (or
#: Peczarski's GPC, which implies it) is PROVED, taken from mg-33f5 §2's table verbatim.  A poset
#: in ANY of these classes is decided by the literature at every `n`, without a census.
LIT_CLASSES = [
    ("width ≤ 2",           lambda n, d: L.width(n, d) <= 2,          "Linial 1984"),
    ("semiorder",           lambda n, d: is_semiorder(n, d),          "Brightwell"),
    ("height ≤ 2",          lambda n, d: height(n, d) <= 2,           "mg-33f5 §2 lists NO source"),
    ("N-free",              lambda n, d: is_N_free(n, d),             "Zaguia, EJC 19(2) #P29"),
    ("cover graph a forest", lambda n, d: cover_graph_is_forest(n, d), "Zaguia, arXiv:1610.00809"),
    ("6-thin",              lambda n, d: thinness(n, d) <= 6,         "Peczarski, Order 25 (2008)"),
    ("has a non-trivial automorphism", lambda n, d: not is_rigid(n, d), "Peczarski 2017"),
]


def covering_classes(n, down):
    """Which literature classes contain `P`.  Empty list ⟹ the STRUCTURAL literature does not
    decide `P` — it may still be inside a CENSUS range, which is a different kind of warrant and
    is kept separate everywhere in this directory."""
    return [name for (name, pred, _cite) in LIT_CLASSES if pred(n, down)]


def is_immune(n, down):
    """Outside EVERY class in `LIT_CLASSES`."""
    return not covering_classes(n, down)


# ------------------------------------------------------------------------------------------------
# the explicit family: literature-immune at density 1 − Θ(1/n)
# ------------------------------------------------------------------------------------------------


def close(n, rel):
    """Transitive closure of `rel` as a `down` tuple."""
    down = [0] * n
    for (a, b) in rel:
        down[b] |= 1 << a
    for _ in range(n):
        for b in range(n):
            m, add = down[b], 0
            while m:
                x = m & -m
                add |= down[x.bit_length() - 1]
                m ^= x
            down[b] |= add
    return tuple(down)


def unicyclic_asymmetric(p):
    """An asymmetric unicyclic graph on `p ≥ 7` vertices, as an edge list.

    A triangle `0,1,2` with two pendant paths of DIFFERENT lengths hung off two of its vertices:
    a path of 1 vertex at `0` and a path of `p − 4` vertices at `1`.  The three triangle vertices
    then have pairwise different branch structures, so no graph automorphism moves any of them,
    and each pendant path is rigid once its foot is fixed."""
    if p < 7:
        raise ValueError("p ≥ 7")
    edges = [(0, 1), (1, 2), (0, 2), (0, 3)]
    prev = 1
    for v in range(4, p):
        edges.append((prev, v))
        prev = v
    return edges


def family(n):
    """`F(n)` for `n ≥ 15`: the INCIDENCE POSET of an asymmetric unicyclic graph — vertices at the
    bottom, one element per edge above its two endpoints — plus one element above one edge-element
    (to leave height 2), plus one isolated element when the parity needs it.

    Comparable pairs are `2p + 3 (+ 0)` on `n = 2p + 1 (+ 1)` elements, i.e. `Θ(n)`, so
    `d(F(n)) = 1 − Θ(1/n)`.  `d3` verifies membership of the seven classes rather than asserting
    it, at every `n` it reaches; `at most one` isolated element is deliberate — two would be
    interchangeable and `F(n)` would stop being rigid, which is `d4`'s lemma acting as a
    constraint on this construction rather than as a result about it."""
    pad = (n % 2 == 0)
    p = (n - 1 - (1 if pad else 0)) // 2
    edges = unicyclic_asymmetric(p)
    rel = []
    for k, (a, b) in enumerate(edges):
        e = p + k
        rel.append((a, e))
        rel.append((b, e))
    top = p + len(edges)
    rel.append((p, top))                    # above the edge-element of edge 0 = (0,1)
    return close(n, rel)
