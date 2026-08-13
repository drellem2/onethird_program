"""mg-3da1 — the marginal body, its vertices, and the realizable points inside it.

WRITTEN FROM SCRATCH AND IMPORTING NOTHING FROM THIS ESTATE, ON PURPOSE.  The subject of this
directory is a claim that `code/image_geometry_c776/` measured, and a library shared with the
instrument under test cannot corroborate it: a defect in the poset enumerator or the
linear-extension routine would move BOTH readings the same way and the agreement would be an
artifact of the shared code rather than evidence.  `lib_c776.py` is therefore not imported here
and neither is `lib8b32`.  What the two directories share is OEIS A001035 and the definitions
below, and `d0` checks this library against A001035 and against brute force before any arm
that produces a finding runs.

EXACT ARITHMETIC THROUGHOUT.  Every marginal is a `Fraction`.  The claims in this directory are
equalities between rationals (`2/3`, `d = m/C(n,2)`, `max = m/3`) and a float comparison would
turn an exact statement into a tolerance, which is the one thing the subject of this ticket
cannot afford: the whole question is whether a bound is ATTAINED or merely approached.

CONVENTIONS
-----------
Ground set is `{0, ..., n-1}`.  The coordinates of the marginal body `M_n` are indexed by the
UNORDERED pairs `(i, j)` with `i < j`, and `pi[(i,j)] = P(i appears before j)`.  The reverse
coordinate is not stored: `P(j before i) = 1 - pi[(i,j)]`.

A poset is a `frozenset` of ORDERED pairs `(x, y)` read as `x < y in P`.  It is irreflexive,
antisymmetric and transitive; `d0` checks all three on every member of every population it
builds, rather than trusting the constructor.

`M_n = conv{ delta_sigma : sigma in S_n }` is the linear ordering polytope.  `delta_sigma` has
`pi[(i,j)] = 1` when `i` precedes `j` in `sigma` and `0` otherwise, so it is a 0/1 point and the
`n!` of them are exactly the vertices of `M_n`.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


# --------------------------------------------------------------------------------------
# pairs, permutations, vertices
# --------------------------------------------------------------------------------------

def pairs(n):
    """The coordinate index of M_n, in a FIXED order so transcripts are reproducible."""
    return list(combinations(range(n), 2))


def all_perms(n):
    """Every linear order on {0..n-1}, as a tuple read left-to-right (first = smallest)."""
    return list(permutations(range(n)))


def vertex(sigma, n):
    """delta_sigma — the marginal vector of the point mass at `sigma`.

    This is the function the whole ticket turns on: it is the marginal vector of a MEASURE
    (a point mass), so every vertex of M_n is a realizable point, and no restriction phrased
    as "pi must be realizable" can exclude one.
    """
    pos = {x: k for k, x in enumerate(sigma)}
    return {(i, j): Fraction(1) if pos[i] < pos[j] else Fraction(0) for (i, j) in pairs(n)}


def vertices(n):
    return [vertex(s, n) for s in all_perms(n)]


# --------------------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------------------

def is_poset(rel, n):
    """Irreflexive + antisymmetric + transitive, checked rather than assumed."""
    for (x, y) in rel:
        if x == y or (y, x) in rel:
            return False
    for (x, y) in rel:
        for (u, v) in rel:
            if y == u and (x, v) not in rel:
                return False
    return True


def enumerate_posets(n):
    """Every labelled poset on {0..n-1}, by assigning each unordered pair one of three states.

    3^C(n,2) candidates, transitivity-filtered.  This is a DIFFERENT algorithm from a
    closure-of-DAGs enumeration and from an isomorphism-class census; `d0` checks the counts
    against OEIS A001035, which is the external anchor.
    """
    ps = pairs(n)
    out = []
    for choice in product((0, 1, 2), repeat=len(ps)):
        rel = set()
        for c, (i, j) in zip(choice, ps):
            if c == 1:
                rel.add((i, j))
            elif c == 2:
                rel.add((j, i))
        if is_poset(rel, n):
            out.append(frozenset(rel))
    return out


def enumerate_chain_subposets(n):
    """Every poset whose comparable pairs all run i < j — the transitive subrelations of the
    n-chain.  2^C(n,2) candidates instead of 3^C(n,2), which is what makes n = 6 reachable.

    THIS IS A RESTRICTION AND `d3` DERIVES ITS EXACTNESS RATHER THAN ASSUMING IT: an image
    point with any pair comparable the other way has a coordinate at 0 where the cell demands
    at least 2/3, so it is outside the cell and cannot be the maximiser.  `d3` re-checks that
    derivation against the FULL population at n <= 5, where both routes are affordable.
    """
    ps = pairs(n)
    out = []
    for choice in product((0, 1), repeat=len(ps)):
        rel = set()
        for c, (i, j) in zip(choice, ps):
            if c:
                rel.add((i, j))
        if is_poset(rel, n):
            out.append(frozenset(rel))
    return out


def poset_of(pi, n):
    """P(pi) = {(x,y) : pi says x is before y with probability 1}.

    Both orientations are read, because the stored coordinate is only the i < j one.
    """
    rel = set()
    for (i, j) in pairs(n):
        if pi[(i, j)] == 1:
            rel.add((i, j))
        elif pi[(i, j)] == 0:
            rel.add((j, i))
    return frozenset(rel)


def incomparable_pairs(P, n):
    return [(i, j) for (i, j) in pairs(n) if (i, j) not in P and (j, i) not in P]


def density(P, n):
    """d(P) = m / C(n,2), the incomparability density."""
    m = len(incomparable_pairs(P, n))
    return Fraction(m, len(pairs(n))), m


# --------------------------------------------------------------------------------------
# linear extensions and marginals
# --------------------------------------------------------------------------------------

def linear_extensions(P, n, universe=None):
    """L(P) — every linear order extending P.  Brute force over S_n, which is the slow route
    and the one that cannot be wrong for a subtle reason."""
    out = []
    for sigma in (universe if universe is not None else all_perms(n)):
        pos = {x: k for k, x in enumerate(sigma)}
        if all(pos[x] < pos[y] for (x, y) in P):
            out.append(sigma)
    return out


def marginal(weighted, n):
    """Marginal vector of a measure given as [(sigma, weight)] with weights summing to 1."""
    ps = pairs(n)
    acc = {p: Fraction(0) for p in ps}
    for sigma, w in weighted:
        pos = {x: k for k, x in enumerate(sigma)}
        for (i, j) in ps:
            if pos[i] < pos[j]:
                acc[(i, j)] += w
    return acc


def uniform_image(P, n, universe=None):
    """pi(Unif(L(P))) — the image point of the poset P.  This is `r`'s value on P's whole cell."""
    L = linear_extensions(P, n, universe)
    w = Fraction(1, len(L))
    return marginal([(s, w) for s in L], n), L


def retract(pi, n, universe=None):
    """r(pi) = pi(Unif(L(P(pi)))) — the retraction whose fixed set is the image R_n."""
    return uniform_image(poset_of(pi, n), n, universe)[0]


# --------------------------------------------------------------------------------------
# linear functionals
# --------------------------------------------------------------------------------------

def dot(c, pi, n):
    return sum(c[p] * pi[p] for p in pairs(n))


def maximise(c, points, n):
    return max(dot(c, pi, n) for pi in points)


def inv_e(pi, n):
    """E[inv_e] with the reference order the identity: the expected number of pairs that appear
    in the order (j, i) with i < j.  Linear in pi, which is the property the whole argument
    turns on -- `sum_{i<j} (1 - pi[(i,j)])`."""
    return sum(1 - pi[(i, j)] for (i, j) in pairs(n))


def fmt(x):
    """A Fraction as `a/b`, or as `a` when the denominator is 1."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# --------------------------------------------------------------------------------------
# a tiny deterministic PRNG, so the direction sweeps reproduce byte-for-byte
# --------------------------------------------------------------------------------------

class Lcg:
    """A linear congruential generator written out here rather than `random.seed(...)`.

    The reason is transcript reproducibility across Python versions: `random`'s stream is
    documented as stable but its CONSUMPTION by helpers like `randrange` is not something this
    directory should have to depend on, and a sweep whose directions changed between hosts
    would make a byte-identical re-run impossible to distinguish from a real movement.
    """

    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFFFFFFFFFF

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        return self.s >> 11

    def below(self, k):
        return self.next() % k

    def direction(self, n, lo=-9, hi=9):
        span = hi - lo + 1
        return {p: lo + self.below(span) for p in pairs(n)}
