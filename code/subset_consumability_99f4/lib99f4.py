"""lib99f4 — posets, their extension SETS, and the on-record subset-separators.

mg-99f4.  THE QUESTION IS CONSUMABILITY, NOT SEPARATION, so this library is built around one
object the estate's other libraries do not name: the **realizable subset family**

    LL_n  =  { L(P) : P a poset on [n] }   as a subset of  2^{S_n}.

Every construction in this ticket's live class is a map  Phi : 2^{S_n} -> (anything).  `LL_n`
is where such a map can be CONSUMED, because it is where an `e(P)` exists at all.  Everything
else in `2^{S_n}` is where it can SEPARATE.  The library therefore exposes `LL_n` explicitly
rather than only `L(P)` one poset at a time.

IMPORTS NOTHING FROM `code/`.  Not `lib8b32`, not `lib0fc6`, not `lib_c776`, not `lib6ff4` —
this directory's finding is that a construction on subsets splits into two independent halves,
and a shared enumerator would move both halves together.  What is shared with the estate is
OEIS A001035 and the definitions; `s0_selftest.py` checks this library against A001035, against
an independent extension count, and against planted defects before any arm that produces a
finding runs.

EXACT ARITHMETIC.  Pair marginals are `Fraction`s.  `delta(P)` and `L*` are compared against
1/2 and 1/3, and a float comparison would turn `at the boundary` into `near the boundary`,
which is the one distinction the boundary population cannot afford.
"""

from fractions import Fraction
from itertools import combinations, permutations

# --------------------------------------------------------------------------- posets

# A poset on [n] is a frozenset of STRICT relations (x, y) meaning x < y.  Reflexivity is
# implicit and never stored; antisymmetry is implicit in "at most one of (x,y), (y,x)".


def is_transitive(rel, n):
    for x, y in rel:
        for z in range(n):
            if (y, z) in rel and (x, z) not in rel:
                return False
    return True


def all_posets(n):
    """Every LABELLED poset on [n], as a frozenset of strict pairs.

    Brute force over the 3^C(n,2) orientations of the pairs (x<y / y<x / incomparable), keeping
    the transitive ones.  Deliberately the dumbest correct algorithm: it shares no idea with the
    minimal-element recursions used elsewhere in the estate, so an agreement with A001035 is a
    second route rather than the same route run twice.
    """
    pairs = list(combinations(range(n), 2))
    out = []

    def rec(i, rel):
        if i == len(pairs):
            if is_transitive(rel, n):
                out.append(frozenset(rel))
            return
        x, y = pairs[i]
        rec(i + 1, rel)
        rec(i + 1, rel | {(x, y)})
        rec(i + 1, rel | {(y, x)})

    rec(0, set())
    return out


def linear_extensions(rel, n):
    """`L(P)` as a SORTED TUPLE of permutations (each a tuple giving the order of elements).

    Sorted so that `L(P)` is a canonical object and `LL_n` can be a set of them — which is the
    whole point of this library.
    """
    return tuple(sorted(
        p for p in permutations(range(n))
        if all(p.index(x) < p.index(y) for x, y in rel)
    ))


def count_extensions_dp(rel, n):
    """`e(P)` by a down-set DP that NEVER enumerates a permutation — the independent route
    `s0` checks `len(linear_extensions(...))` against."""
    below = [{x for x, y in rel if y == e} for e in range(n)]
    memo = {}

    def f(placed):
        if placed == (1 << n) - 1:
            return 1
        if placed in memo:
            return memo[placed]
        t = 0
        for e in range(n):
            if not (placed >> e) & 1 and all((placed >> b) & 1 for b in below[e]):
                t += f(placed | (1 << e))
        memo[placed] = t
        return t

    return f(0)


def relation_from(LEs, n):
    """`P = intersection of L(P)` — the pairs on which EVERY member of the set agrees.

    This is the map that makes `LL_n -> posets` well defined, and `s1.1` measures that it is
    inverse to `linear_extensions`.
    """
    rel = set()
    for x, y in permutations(range(n), 2):
        if all(p.index(x) < p.index(y) for p in LEs):
            rel.add((x, y))
    return frozenset(rel)


# --------------------------------------------------------------------------- marginals


def pair_marginals(S, n):
    """`pi_xy = Pr[x before y]` under the UNIFORM measure on the subset `S`.

    Defined for ANY non-empty `S <= S_n`, not only for an `L(P)` — that is the whole live class.
    """
    m = len(S)
    out = {}
    for x, y in permutations(range(n), 2):
        out[(x, y)] = Fraction(sum(1 for p in S if p.index(x) < p.index(y)), m)
    return out


def delta(rel, LEs, n):
    """`delta(P) = max over INCOMPARABLE pairs of min(pi_xy, pi_yx)`; `0` for a chain, where the
    max is over the empty set (mg-c776's own reading, kept)."""
    pi = pair_marginals(LEs, n)
    best = Fraction(0)
    for x, y in combinations(range(n), 2):
        if (x, y) in rel or (y, x) in rel:
            continue
        best = max(best, min(pi[(x, y)], pi[(y, x)]))
    return best


def lstar(pi, n):
    """The distinguished / majority order `L*`, or `None` if the majority tournament is not a
    total order.  Same definition as `lib8b32.lstar` and `lib0fc6.coherent_order` — RE-WRITTEN
    here rather than imported, and `s0` checks it agrees with the two properties that define it.
    """
    half = Fraction(1, 2)
    wins = [0] * n
    for x, y in combinations(range(n), 2):
        if pi[(x, y)] > half:
            wins[x] += 1
        elif pi[(x, y)] < half:
            wins[y] += 1
        else:
            return None
    order = sorted(range(n), key=lambda x: -wins[x])
    for i in range(n):
        for j in range(i + 1, n):
            if pi[(order[i], order[j])] <= half:
                return None
    return tuple(order)


# --------------------------------------------------------------------------- the separators

# The FOUR constructions `mg-8b32`'s b2.3 put in TIER 2 — "reads supp(mu), DOES NOT FACTOR".
# Each is a map from a SUBSET of S_n to a value.  Written with the subset as the only argument,
# because that signature is this ticket's entire subject.


def bk_edges(S):
    """The BK graph on an arbitrary subset: an edge for each ADJACENT transposition inside `S`.
    Returns the edge count."""
    Sset = set(S)
    e = 0
    for p in S:
        for i in range(len(p) - 1):
            q = list(p)
            q[i], q[i + 1] = q[i + 1], q[i]
            q = tuple(q)
            if q in Sset and q > p:
                e += 1
    return e


def inversions_against(p, star):
    """Number of pairs inverted in `p` relative to the order `star`."""
    pos = {v: i for i, v in enumerate(p)}
    n = len(star)
    return sum(1 for i in range(n) for j in range(i + 1, n)
               if pos[star[i]] > pos[star[j]])


def weak_ideal(S, star):
    """`S` is a lower ideal of the weak order rooted at `star`: for every `p` in `S` with an
    inversion against `star`, some single adjacent transposition of `p` that REMOVES one
    inversion also lands in `S`.  The `mg-8b32` b2 row, restated on an arbitrary subset."""
    Sset = set(S)
    for p in S:
        k = inversions_against(p, star)
        if k == 0:
            continue
        ok = False
        for i in range(len(p) - 1):
            q = list(p)
            q[i], q[i + 1] = q[i + 1], q[i]
            q = tuple(q)
            if inversions_against(q, star) == k - 1 and q in Sset:
                ok = True
                break
        if not ok:
            return False
    return True


def separators(n):
    """The four TIER-2 constructions, each as `(name, Phi)` with `Phi(S, star)`.

    `star` is passed separately because `L*` is a function of the MARGINALS of the input set,
    and two of the four read it.  That is faithful to `mg-8b32` b2.3, where `star` is computed
    once from the common `pi` and both witnesses are read against it.
    """
    return [
        # `star is None` is UNDEFINED, not False — the same treatment T2c gets, and for the same
        # reason: mg-8b32 b2.3 reads both rows against a single `L*` computed from the common
        # `pi`, so where the majority tournament cycles there is no row to read.  Written out
        # because the first draft returned `False` there and the s1.4 census came back `res = 2`
        # for a construction whose one-line proof says `res = 1` — the census caught it.
        ("T2a  L* is a member of the set",
         lambda S, star: (star in set(S)) if star is not None else None),
        ("T2b  |S| equals e(P(pi(S)))",
         lambda S, star: len(S) == count_extensions_dp(relation_from(S, n), n)),
        ("T2c  S is a weak-order ideal under L*",
         lambda S, star: weak_ideal(S, star) if star is not None else None),
        ("T2d  the BK graph of S  [edge count]", lambda S, star: bk_edges(S)),
    ]


# --------------------------------------------------------------------------- the crossover law


def log2_factorial(n):
    """`log2 n!` in floating point, by summation — no Stirling approximation, because the
    crossover this file computes is a DIFFERENCE of two nearly equal quantities and Stirling's
    error is the same size as the answer at small `n`."""
    import math
    return math.lgamma(n + 1) / math.log(2.0)


def crossover(c, hi=1 << 70):
    """The first `n >= 3` at which a bound of shape `c * n log2 n` beats `log2 n!`.

    Returns `None` if no such `n` below `hi`.  Binary search on the monotone predicate
    `(1-c) log2 n > log2 n! ... ` — stated as the raw comparison rather than the closed form, so
    the closed form `2^(log2(e)/(1-c))` can be CHECKED against it in `s2` instead of assumed.
    """
    import math

    def bites(n):
        return c * n * math.log2(n) < log2_factorial(n)

    if c >= 1.0:
        return None
    lo = 3
    if bites(lo):
        return lo
    if not bites(hi):
        return None
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if bites(mid):
            hi = mid
        else:
            lo = mid
    return hi


# --------------------------------------------------------------------------- transcript

class Report:
    """Minimal transcript writer.  `bad` counts the RED rows and becomes the arm's exit code,
    so a red row cannot be printed and then walked past."""

    def __init__(self):
        self.bad = 0

    def banner(self, s):
        print("=" * 78)
        print(s)
        print("=" * 78)

    def note(self, s):
        print("       " + s)

    def line(self, s=""):
        print(s)

    def verdict(self, ok, label, detail=""):
        if not ok:
            self.bad += 1
        print("  [%s] %s%s" % ("GREEN" if ok else "RED  ", label,
                               ("   " + detail) if detail else ""))

    def done(self):
        print()
        print("arm exit: %d   (0 green, %d red row(s))" % (1 if self.bad else 0, self.bad))
        return 1 if self.bad else 0
