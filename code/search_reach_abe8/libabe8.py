"""Self-contained core for the search-reach cost model (mg-abe8).

Nothing here imports from `code/counterexample_probe_24a3/`, `code/face_geometry/`
or anywhere else in this repo.  Every object is rebuilt from its definition so
that the numbers this instrument reports are independent of the pipeline they are
about.  Exact arithmetic throughout (Python ints and `fractions.Fraction`); the
only floats are logarithms and wall-clock times, and those are labelled at the
call site.

Definitions used, all of them written out so a reader need not chase them:

  Poset P on {0..n-1}         strict relation, transitively closed.
  delta(P)                    max over incomparable pairs of min(p, 1-p),
                              p = p(x,y) = Pr[x before y in a uniform linear
                              extension].  `frozen` = delta < 1/3 (STATE.md:46).
  primitive                   incomparability graph connected  <=>  P is not an
                              ordinal sum (STATE.md:47, ledger row 2).
  rigid                       |Aut(P)| = 1.  THE LITERATURE'S SENSE (Peczarski
                              2017 via mg-5998), NOT STATE.md:169's
                              "extremal rigidity", which is a statement about the
                              value set of delta and is a different property with
                              the same name.
  width(P)                    largest antichain (Dilworth / Mirsky not needed:
                              computed by brute force at these n).
  thinness                    max over x of |{y : y incomparable to x, y != x}|.
                              `not 6-thin` = thinness >= 7 (Peczarski 2008 via
                              mg-5998).

  PRUNING, IN BITS            -log2(surviving / total).   <-- P14 binds this file
                              to this formula and to no other.  A constraint whose
                              EXCLUDED set is a vanishing fraction prunes ~0 bits,
                              not many; writing it the other way round is the
                              error P14 was filed to catch.
"""

import math
from fractions import Fraction
from itertools import combinations, permutations


# ---------------------------------------------------------------------------
# 1.  Posets
# ---------------------------------------------------------------------------

class Poset:
    """A finite poset on {0..n-1}; `less` is the transitively closed strict relation."""

    __slots__ = ("n", "less", "up", "dn", "inc", "_key")

    def __init__(self, n, relations):
        less = set()
        for (a, b) in relations:
            if a == b:
                raise ValueError("irreflexive relation required")
            less.add((a, b))
        changed = True
        while changed:
            changed = False
            for (a, b) in list(less):
                for (c, d) in list(less):
                    if b == c and (a, d) not in less:
                        if a == d:
                            raise ValueError("cycle: not a poset")
                        less.add((a, d))
                        changed = True
        for (a, b) in less:
            if (b, a) in less:
                raise ValueError("not antisymmetric: not a poset")
        self.n = n
        self.less = frozenset(less)
        self.up = [0] * n
        self.dn = [0] * n
        for (a, b) in less:
            self.up[a] |= 1 << b
            self.dn[b] |= 1 << a
        full = (1 << n) - 1
        # incomparability neighbourhoods, x excluded from its own
        self.inc = [full & ~self.up[i] & ~self.dn[i] & ~(1 << i) for i in range(n)]
        self._key = None

    def __repr__(self):
        return "Poset(%d, %s)" % (self.n, sorted(self.less))

    def comparable(self, a, b):
        return a == b or (a, b) in self.less or (b, a) in self.less

    def incomparable_pairs(self):
        return [(a, b) for a in range(self.n) for b in range(a + 1, self.n)
                if not self.comparable(a, b)]

    # ---- canonical form (isomorphism invariant) --------------------------

    def _vertex_classes(self):
        n = self.n
        inv = [(bin(self.dn[i]).count("1"), bin(self.up[i]).count("1")) for i in range(n)]
        for _ in range(n):
            new = []
            for i in range(n):
                dnb = sorted(inv[j] for j in range(n) if (self.dn[i] >> j) & 1)
                upb = sorted(inv[j] for j in range(n) if (self.up[i] >> j) & 1)
                new.append((inv[i], tuple(dnb), tuple(upb)))
            order = sorted(set(new))
            rank = {v: k for k, v in enumerate(order)}
            nxt = [rank[v] for v in new]
            if nxt == inv:
                break
            inv = nxt
        classes = {}
        for i in range(n):
            classes.setdefault(inv[i], []).append(i)
        return [classes[k] for k in sorted(classes)]

    def canonical_key(self):
        """Lexicographically minimal relation tuple over the relabellings that
        RESPECT THE REFINED VERTEX INVARIANT -- a strict subset of S_n.

        It is therefore NOT in general the global lexicographic minimum over all
        of S_n, and `selftestabe8.py` measures how often it differs (often: 58 of
        63 at n = 5).  What has to be true, and what the selftest checks, is that
        it is a COMPLETE ISOMORPHISM INVARIANT -- constant on isomorphism classes
        (every isomorphism respects the refined invariant, so the admissible sets
        of relabellings correspond) and distinct on distinct ones.  That is what
        the enumeration needs, and the A000112 agreement to n = 9 is the
        end-to-end check of it.
        """
        if self._key is not None:
            return self._key
        n = self.n
        slots = []
        pos = 0
        for cls in self._vertex_classes():
            slots.append((cls, list(range(pos, pos + len(cls)))))
            pos += len(cls)
        best = None

        def rec(k, g):
            nonlocal best
            if k == len(slots):
                rel = tuple(sorted((g[a], g[b]) for (a, b) in self.less))
                if best is None or rel < best:
                    best = rel
                return
            cls, targets = slots[k]
            for perm in permutations(targets):
                g2 = dict(g)
                for i, t in zip(cls, perm):
                    g2[i] = t
                rec(k + 1, g2)

        rec(0, {})
        self._key = (n, best)
        return self._key


def all_posets_bruteforce(n):
    """All posets on n elements up to isomorphism, by sweeping transitively closed
    subsets of {(i,j) : i<j}.  Used for n <= 5 and as the control for the
    extension-based enumeration."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            rel = set(sub)
            ok = True
            for (a, b) in rel:
                for (c, d) in rel:
                    if b == c and (a, d) not in rel:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            seen.setdefault(Poset(n, rel).canonical_key(), None)
    return [Poset(n, set(k[1])) for k in sorted(seen)]


def order_ideal_masks(P):
    """Down-sets of P, as bitmasks.  Cost Theta(2^n * n) -- this routine is the
    reason the exhaustive arm stops where it does, and s4 measures it."""
    out = []
    for mask in range(1 << P.n):
        ok = True
        m = mask
        while m:
            b = (m & -m).bit_length() - 1
            m &= m - 1
            if P.dn[b] & ~mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def all_posets_by_extension(n, smaller):
    """All posets on n elements up to isomorphism, built from the (n-1)-element
    classes by adjoining a new MAXIMAL element whose strict down-set is any order
    ideal of the smaller poset.

    Complete because every finite poset has a maximal element, and deleting one
    leaves an (n-1)-element poset in which the deleted element's down-set is an
    ideal.  THIS ROUTINE IS THE SEARCH TREE H4/P-H4 IS ABOUT: pruning a search
    means discarding elements of `smaller`, and a minimal counterexample's parent
    is by definition NOT frozen, so frozen-ness discards none of them.
    """
    seen = {}
    for Q in smaller:
        for ideal in order_ideal_masks(Q):
            rel = set(Q.less)
            for i in range(Q.n):
                if (ideal >> i) & 1:
                    rel.add((i, n - 1))
            seen.setdefault(Poset(n, rel).canonical_key(), None)
    return [Poset(n, set(k[1])) for k in sorted(seen)]


# ---------------------------------------------------------------------------
# 2.  delta, from the definition
# ---------------------------------------------------------------------------

def restriction_counts(P):
    """e[S] = #linear extensions of P restricted to S, for every subset S.

    DP on the definition: a linear extension of P|_S ends in an element maximal in
    P|_S, so e[S] = sum over such x of e[S \\ {x}]."""
    n = P.n
    e = [0] * (1 << n)
    e[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if not (P.up[x] & S):
                tot += e[S & ~(1 << x)]
        e[S] = tot
    return e


def pair_before_counts(P, e):
    """before[(x,y)] = #{linear extensions with x before y}, all ordered pairs.

    Split an extension at the moment x is placed: the prefix set S is a down-set,
    x is maximal in S, y not in S; the prefix completes in e(P|_{S-x}) ways and the
    suffix in e(P|_{S^c}) ways, each extension counted once."""
    n = P.n
    full = (1 << n) - 1
    ideals = order_ideal_masks(P)
    before = {}
    for x in range(n):
        for y in range(n):
            if x == y:
                continue
            tot = 0
            for S in ideals:
                if not ((S >> x) & 1):
                    continue
                if (S >> y) & 1:
                    continue
                if P.up[x] & S:
                    continue
                tot += e[S & ~(1 << x)] * e[full & ~S]
            before[(x, y)] = tot
    return before


def delta(P):
    """max over incomparable pairs of min(p, 1-p), as an exact Fraction.
    Returns None for a chain (no incomparable pair)."""
    pairs = P.incomparable_pairs()
    if not pairs:
        return None
    e = restriction_counts(P)
    total = e[(1 << P.n) - 1]
    before = pair_before_counts(P, e)
    best = Fraction(0)
    for (x, y) in pairs:
        p = Fraction(before[(x, y)], total)
        best = max(best, min(p, 1 - p))
    return best


def is_frozen(P):
    d = delta(P)
    return d is not None and d < Fraction(1, 3)


# --- the same thing at Theta(#ideals * n) instead of Theta(2^n * n) ---------
#
# `restriction_counts` fills every one of the 2^n subsets and is why the exact
# test looks like a 2^n algorithm.  It is not.  The marginals need e(S) only for
# S an IDEAL minus a maximal point (still an ideal) and for S a FILTER (the
# complement of an ideal); both families are closed under deleting a maximal
# element, so a memoised recursion touches exactly 2 * #ideals subsets.  THIS is
# the per-candidate cost a real search pays, and it is the cost s2/C and s4 use.

def order_ideal_masks_lazy(P):
    """Down-sets of P without the 2^n sweep: DFS in a linear-extension order,
    including an element only once its whole strict down-set is present.  Cost
    O(n * #ideals), which is what makes n = 28 reachable at all."""
    n = P.n
    order = []
    placed = 0
    while len(order) < n:
        for x in range(n):
            if not ((placed >> x) & 1) and not (P.dn[x] & ~placed):
                order.append(x)
                placed |= 1 << x
                break
    out = []

    def rec(i, mask):
        if i == n:
            out.append(mask)
            return
        x = order[i]
        rec(i + 1, mask)                      # x excluded
        if not (P.dn[x] & ~mask):             # x includable
            rec(i + 1, mask | (1 << x))

    rec(0, 0)
    return out


def delta_lazy_stats(P, ideals=None):
    """(delta_or_certificate, #incomparable pairs examined).

    Exact delta when the poset is frozen; otherwise it stops at the first
    balanced pair and returns a value >= 1/3, which is all a search needs.  The
    pair count is the figure s3 reports: it is how much work one REJECTION
    costs, and it is not the same quantity as how many candidates must be
    visited."""
    n = P.n
    full = (1 << n) - 1
    pairs = P.incomparable_pairs()
    if not pairs:
        return (None, 0)
    if ideals is None:
        ideals = order_ideal_masks_lazy(P)
    memo = {0: 1}

    def e_of(S):
        v = memo.get(S)
        if v is not None:
            return v
        tot = 0
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if not (P.up[x] & S):
                tot += e_of(S & ~(1 << x))
        memo[S] = tot
        return tot

    total = e_of(full)
    best = Fraction(0)
    third = Fraction(1, 3)
    tried = 0
    for (x, y) in pairs:
        tried += 1
        c = 0
        for S in ideals:
            if not ((S >> x) & 1) or ((S >> y) & 1):
                continue
            if P.up[x] & S:
                continue
            c += e_of(S & ~(1 << x)) * e_of(full & ~S)
        p = Fraction(c, total)
        best = max(best, min(p, 1 - p))
        if best >= third:
            return (best, tried)      # certified non-frozen; stop
    return (best, tried)


def delta_lazy(P, ideals=None):
    return delta_lazy_stats(P, ideals)[0]


def is_frozen_lazy(P, ideals=None):
    d = delta_lazy(P, ideals)
    return d is not None and d < Fraction(1, 3)


# ---------------------------------------------------------------------------
# 3.  The four literature constraints
# ---------------------------------------------------------------------------

def automorphism_count(P):
    """|Aut(P)|, by brute force over relabellings respecting the refined vertex
    invariant (every automorphism does)."""
    n = P.n
    slots = [cls for cls in P._vertex_classes()]
    count = 0

    def rec(k, g):
        nonlocal count
        if k == len(slots):
            for (a, b) in P.less:
                if (g[a], g[b]) not in P.less:
                    return
            count += 1
            return
        cls = slots[k]
        for perm in permutations(cls):
            g2 = dict(g)
            for i, t in zip(cls, perm):
                g2[i] = t
            rec(k + 1, g2)

    rec(0, {})
    return count


def is_rigid(P):
    """|Aut(P)| = 1.  THE LITERATURE'S SENSE, not STATE.md:169's."""
    return automorphism_count(P) == 1


def width(P):
    """Largest antichain, by brute force over subsets (n <= 9 here)."""
    n = P.n
    best = 0
    for mask in range(1 << n):
        ok = True
        m = mask
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if (P.up[x] | P.dn[x]) & mask:
                ok = False
                break
        if ok:
            best = max(best, bin(mask).count("1"))
    return best


def thinness(P):
    """max over x of the number of elements incomparable to x.
    `not 6-thin` (Peczarski 2008 via mg-5998) is thinness >= 7."""
    return max(bin(m).count("1") for m in P.inc) if P.n else 0


def is_primitive(P):
    """Incomparability graph connected == not an ordinal sum (STATE.md:47)."""
    n = P.n
    if n <= 1:
        return True
    seen = 1
    stack = [0]
    while stack:
        x = stack.pop()
        m = P.inc[x] & ~seen
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            seen |= 1 << y
            stack.append(y)
    return seen == (1 << n) - 1


CONSTRAINTS = [
    ("rigid",       "Aut(P)=1 (Peczarski 2017 via mg-5998, UNVERIFIED)", is_rigid),
    ("width>=3",    "width(P)>=3 (Linial 1984 via mg-5998, UNVERIFIED)", lambda P: width(P) >= 3),
    ("not-6-thin",  "some x incomparable to >=7 (Peczarski 2008 via mg-5998, UNVERIFIED)",
     lambda P: thinness(P) >= 7),
    ("primitive",   "incomparability graph connected (STATE.md:47, row 2)", is_primitive),
]


# ---------------------------------------------------------------------------
# 4.  Pruning, in bits -- ONE formula, and P14 binds this file to it
# ---------------------------------------------------------------------------

def prune_bits(surviving, total):
    """-log2(surviving/total).  0 bits when nothing is excluded; +inf when the
    class is emptied.  NOT -log2(excluded/total): that is the P14 error."""
    if total == 0:
        raise ValueError("empty population")
    if surviving == 0:
        return float("inf")
    return -math.log2(surviving / total)


def reach_from_bits(bits, n, g):
    """Extra elements of reach bought by a pruning of `bits` bits at size n.
    g(n) bits are needed per element, so the answer is bits / g(n)."""
    return bits / g(n)


# ---------------------------------------------------------------------------
# 5.  The population model  (A000112 exact to n=16, extrapolated above)
# ---------------------------------------------------------------------------

# A000112: posets on n unlabelled elements.  n <= 9 is re-derived by this
# instrument's own enumerator (s1) and agrees; n = 10..16 is QUOTED from OEIS and
# is NOT verified here (PREDICTIONS H2).
A000112 = [1, 1, 2, 5, 16, 63, 318, 2045, 16999, 183231, 2567284, 46749427,
           1104891746, 33823827452, 1338193159771, 68275077901156,
           4483130665195087]

_EXACT_MAX = len(A000112) - 1          # 16


def g_exact(n):
    """log2(N(n)/N(n-1)) from the exact table.  Bits paid for element n."""
    return math.log2(A000112[n]) - math.log2(A000112[n - 1])


# Two growth models above n = 16, reported side by side and never mixed:
#
#   LOW  -- linear extrapolation of g with the slope observed at n = 13..16
#           (0.365 bits per element per element).  This UNDERSTATES N(n) at every
#           n > 16, because the true asymptotic slope is 1/2 (Kleitman-Rothschild).
#           It is the model most favourable to a search succeeding and it is the
#           one every headline figure in this instrument uses.
#   KR   -- the asymptotic slope 1/2, anchored at the exact g(16).  Larger, and
#           the one the mathematics actually says.
#
G16 = None          # filled at import
SLOPE_LOW = 0.365
SLOPE_KR = 0.5


def _init():
    global G16
    G16 = g_exact(_EXACT_MAX)


_init()


def g_model(n, model="LOW"):
    """Bits paid for element n, under the named model."""
    if n <= _EXACT_MAX:
        return g_exact(n)
    slope = SLOPE_LOW if model == "LOW" else SLOPE_KR
    return G16 + slope * (n - _EXACT_MAX)


def log2_N(n, model="LOW"):
    """log2 of the number of posets on n unlabelled elements."""
    if n <= _EXACT_MAX:
        return math.log2(A000112[n])
    tot = math.log2(A000112[_EXACT_MAX])
    for k in range(_EXACT_MAX + 1, n + 1):
        tot += g_model(k, model)
    return tot


# ---------------------------------------------------------------------------
# 6.  Per-candidate cost:  the KR three-layer model
# ---------------------------------------------------------------------------
#
# Kleitman-Rothschild: almost every finite poset has three levels L1, L2, L3 with
# |L1| ~ |L3| ~ n/4 and |L2| ~ n/2, every element of L1 below every element of L3,
# and each L2 element's down-set in L1 / up-set in L3 otherwise unconstrained.
# The model is used here ONLY to say what a TYPICAL candidate costs and how the
# four constraints behave on one; it is a MODEL, it is not the uniform
# distribution on posets, and every figure derived from it is labelled KR-model.

def kr_layer_sizes(n):
    """(|L1|, |L2|, |L3|) for the KR three-layer model at size n."""
    l1 = n // 4
    l3 = n // 4
    l2 = n - l1 - l3
    return (l1, l2, l3)


def kr_sample(n, rng):
    """One KR-model poset on n elements: L1 = [0,l1), L2 = [l1,l1+l2),
    L3 = the rest.  L1 < L3 entirely; each L2 element gets a uniform random
    down-set in L1 and up-set in L3."""
    l1, l2, l3 = kr_layer_sizes(n)
    A = list(range(l1))
    B = list(range(l1, l1 + l2))
    C = list(range(l1 + l2, n))
    rel = set()
    for a in A:
        for c in C:
            rel.add((a, c))
    for b in B:
        for a in A:
            if rng.getrandbits(1):
                rel.add((a, b))
        for c in C:
            if rng.getrandbits(1):
                rel.add((b, c))
    return Poset(n, rel)


def kr_ideal_count(P, l1, l2, l3):
    """#order ideals of a three-layer KR poset, counted in 2^l2 + 2^l3 work
    rather than 2^n (which is what `order_ideal_masks` costs and what makes the
    exact delta computation die).

    Split on whether the ideal S meets the top layer L3.

      S n L3 = {} :  S = A u B with A <= L1, B <= L2 and dn(B) n L1 <= A.
                     Count = sum over B <= L2 of 2^(l1 - |dn(B) n L1|).
      S n L3 != {}:  some c in L3 is in S, and L1 < L3 entirely, so L1 <= S.
                     For each nonempty T <= L3 the B-part must contain
                     dn(T) n L2 and is otherwise free.
                     Count = sum over nonempty T <= L3 of 2^(l2 - |dn(T) n L2|).

    `selftestabe8.py` checks this against `order_ideal_masks` at small n.
    """
    n = P.n
    A = list(range(l1))
    B = list(range(l1, l1 + l2))
    C = list(range(l1 + l2, n))
    maskA = (1 << l1) - 1
    maskB = ((1 << l2) - 1) << l1
    dnB_in_A = [P.dn[b] & maskA for b in B]
    dnC_in_B = [P.dn[c] & maskB for c in C]
    total = 0
    for bmask in range(1 << l2):
        need = 0
        m = bmask
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            need |= dnB_in_A[j]
        total += 1 << (l1 - bin(need).count("1"))
    bsel = ((1 << l2) - 1) << l1
    for tmask in range(1, 1 << l3):
        need = 0
        m = tmask
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            need |= dnC_in_B[j]
        total += 1 << (l2 - bin(need).count("1"))
    return total
