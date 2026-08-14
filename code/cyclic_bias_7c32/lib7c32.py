"""THE CYCLIC-ORIENTATION BIAS `db`, AND EVERYTHING THE THREE CHECKS SHARE (mg-7c32).

The subject is one identity and one telescope.  For a finite poset `P` on `n`
elements with `L(P)` its linear extensions under the uniform measure:

    p(x,y) = Pr[x <_L y]          b(x,y) = p(x,y) - 1/2          (the PAIR BIAS)
    (db)(x,y,z) = b(x,y) + b(y,z) + b(z,x)                       (its COBOUNDARY)

Step 1 of the research line says `db` is the CYCLIC-ORIENTATION BIAS:

    (db)(x,y,z) = Pr[ the order L induces on {x,y,z} is a rotation of (x,y,z) ] - 1/2

and step 3 says the pair bias telescopes along any chain with `db` as the defect.

EVERYTHING IS EXACT.  Counts are Python integers; probabilities are `Fraction`.
No floating point enters any decision in this directory -- the quantities under
test are compared against `1/6` and `1/2`, and a rounded `1/6` is a different
number from `1/6`.

TWO INDEPENDENT ROUTES TO THE SAME TRIPLE, ON PURPOSE.  `triple_class_counts`
enumerates `L(P)` and reads the induced order off each word; `db_from_marginals`
never builds a linear extension and computes `db` from the three pair marginals
alone.  Step 1 is precisely the claim that these agree, so a directory that
computed the second and called it a measurement of the first would be asserting
its own subject.  `c1_identity.py` runs both and compares as integers.

WHAT IS DELIBERATELY NOT IMPORTED.  `code/counterexample_probe_24a3/core.py`
carries a poset enumerator and a marginal routine, and this file re-derives both
rather than importing them.  The reason is mg-d2c2's: a finding computed through
another directory's library is partly a statement about that library.  The price
is paid back as a control -- `c1` checks this enumerator's population against
OEIS A000112 and its marginals against brute-force enumeration of `L(P)`.
"""

from fractions import Fraction
from itertools import combinations, permutations

# ---------------------------------------------------------------------------
# 1.  Posets
# ---------------------------------------------------------------------------


class Poset:
    """A poset on {0..n-1}.  `less` is the transitively closed STRICT relation."""

    __slots__ = ("n", "less", "up", "dn", "_key", "_ideals", "_ecounts")

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
        self._key = None
        self._ideals = None
        self._ecounts = None

    def __repr__(self):
        return "Poset(%d, %s)" % (self.n, sorted(self.less))

    def comparable(self, a, b):
        return a == b or (a, b) in self.less or (b, a) in self.less

    def incomparable_pairs(self):
        return [(a, b) for a in range(self.n) for b in range(a + 1, self.n)
                if not self.comparable(a, b)]

    def is_chain(self):
        return len(self.less) == self.n * (self.n - 1) // 2

    def is_antichain(self):
        return len(self.less) == 0

    def canonical_key(self):
        """Lexicographically least relabelled relation set: the isomorphism class.

        Only relabellings that PRESERVE the up-set/down-set size profile are
        tried, because an isomorphism must.  THIS DOES CHANGE THE KEY'S VALUE --
        it is not the unrestricted lex-least, and `c1` §0 measures 82 posets at
        `n <= 5` where the two strings differ.  What it does not change is the
        CLASSIFICATION, which is the only thing anything here reads: the
        restricted relabelling set is itself determined by the isomorphism class,
        so the key is constant on classes and separates them.  §0 checks exactly
        that -- the two keys induce the SAME partition -- rather than checking a
        string equality that was never the claim.  A first draft of that control
        asserted the strings and went red on its own arm."""
        if self._key is None:
            inv = [(bin(self.up[i]).count("1"), bin(self.dn[i]).count("1"))
                   for i in range(self.n)]
            groups = {}
            for i, v in enumerate(inv):
                groups.setdefault(v, []).append(i)
            keys = sorted(groups)
            best = None
            targets = []
            pos = 0
            for k in keys:
                targets.append(list(range(pos, pos + len(groups[k]))))
                pos += len(groups[k])
            def rec(gi, perm):
                nonlocal best
                if gi == len(keys):
                    rel = tuple(sorted((perm[a], perm[b]) for (a, b) in self.less))
                    if best is None or rel < best:
                        best = rel
                    return
                src = groups[keys[gi]]
                for images in permutations(targets[gi]):
                    for s, t in zip(src, images):
                        perm[s] = t
                    rec(gi + 1, perm)
            rec(0, [0] * self.n)
            self._key = (self.n, best)
        return self._key

    def canonical_key_unrestricted(self):
        """The same key with NO invariant cut -- the control for `canonical_key`."""
        best = None
        for perm in permutations(range(self.n)):
            rel = tuple(sorted((perm[a], perm[b]) for (a, b) in self.less))
            if best is None or rel < best:
                best = rel
        return (self.n, best)

    def with_relation(self, a, b):
        return Poset(self.n, set(self.less) | {(a, b)})


def order_ideals(P):
    """Down-sets of `P` as bitmasks, cached on the poset."""
    if P._ideals is None:
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
        P._ideals = out
    return P._ideals


def all_posets_bruteforce(n):
    """Every poset on `n` elements up to isomorphism, by sweeping transitively
    closed subsets of {(i,j) : i < j}.  Exponential; the CONTROL for the
    extension enumerator below, run only at n <= 5."""
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
            seen.setdefault(Poset(n, rel).canonical_key(), Poset(n, rel))
    return [seen[k] for k in sorted(seen)]


def all_posets(n, smaller=None):
    """Every poset on `n` elements up to isomorphism, built from the (n-1)-element
    classes by adjoining a MAXIMAL element whose strict down-set is any order
    ideal.  Complete because every finite poset has a maximal element."""
    if n == 0:
        return [Poset(0, [])]
    if n == 1:
        return [Poset(1, [])]
    if smaller is None:
        smaller = all_posets(n - 1)
    seen = {}
    for Q in smaller:
        for ideal in order_ideals(Q):
            rel = set(Q.less)
            for i in range(Q.n):
                if (ideal >> i) & 1:
                    rel.add((i, n - 1))
            P = Poset(n, rel)
            seen.setdefault(P.canonical_key(), P)
    return [seen[k] for k in sorted(seen)]


def posets_upto(nmax):
    """{n: [posets]} for n = 1..nmax, each level built from the one below."""
    out = {}
    prev = None
    for n in range(1, nmax + 1):
        prev = all_posets(n, prev)
        out[n] = prev
    return out


# ---------------------------------------------------------------------------
# 2.  Linear extensions and pair marginals
# ---------------------------------------------------------------------------


def linear_extensions(P):
    """`L(P)` as words: `w[t]` is the element in position `t`.  From the definition."""
    out = []
    n = P.n

    def rec(placed, word):
        if len(word) == n:
            out.append(tuple(word))
            return
        for x in range(n):
            if (placed >> x) & 1:
                continue
            if P.dn[x] & ~placed:
                continue
            rec(placed | (1 << x), word + [x])

    rec(0, [])
    return out


def restriction_counts(P):
    """`e[S] = e(P|_S)` for every subset `S`, indexed by bitmask.  Cached.

    DP on the definition: a linear extension of `P|_S` ends in an element maximal
    in `S`, and deleting it leaves one of `P|_{S \\ {x}}`."""
    if P._ecounts is None:
        n = P.n
        e = [0] * (1 << n)
        e[0] = 1
        for S in range(1, 1 << n):
            tot = 0
            m = S
            while m:
                x = (m & -m).bit_length() - 1
                m &= m - 1
                if not (P.up[x] & S):            # x is maximal in S
                    tot += e[S & ~(1 << x)]
            e[S] = tot
        P._ecounts = e
    return P._ecounts


def before_counts(P):
    """`before[(x,y)] = |{w in L(P) : x before y}|` for every ordered pair.

    Split a linear extension at the moment `x` is placed.  If the prefix set is
    `S` then `S` is a down-set, `x` is maximal in `S` and `y` is not in `S`; the
    prefix completes in `e(P|_{S\\{x}})` ways and the suffix in `e(P|_{S^c})`
    ways, and each extension with `x` before `y` is counted exactly once."""
    n = P.n
    full = (1 << n) - 1
    e = restriction_counts(P)
    ideals = order_ideals(P)
    before = {}
    for x in range(n):
        bx = 1 << x
        for y in range(n):
            if x == y:
                continue
            by = 1 << y
            tot = 0
            for S in ideals:
                if not (S & bx) or (S & by):
                    continue
                if P.up[x] & S:
                    continue
                tot += e[S & ~bx] * e[full & ~S]
            before[(x, y)] = tot
    return before


def marginals(P):
    """`(e_total, p)` with `p[(x,y)] = Pr[x <_L y]` as an exact `Fraction`."""
    e = restriction_counts(P)
    tot = e[(1 << P.n) - 1]
    before = before_counts(P)
    return tot, {k: Fraction(v, tot) for k, v in before.items()}


def bias(p):
    """`b(x,y) = p(x,y) - 1/2` for every ordered pair."""
    return {k: v - Fraction(1, 2) for k, v in p.items()}


def delta_of(P, p):
    """The balance constant `delta(P) = max over incomparable pairs of min(p, 1-p)`.

    The conjecture is `delta(P) >= 1/3`; the counterexample hypothesis is
    `delta(P) < 1/3`, i.e. EVERY incomparable pair has `|b| > 1/6`.  `None` for a
    chain, which has no incomparable pair and about which the conjecture says
    nothing."""
    per = {(a, b): min(p[(a, b)], 1 - p[(a, b)]) for (a, b) in P.incomparable_pairs()}
    if not per:
        return None, per
    return max(per.values()), per


# ---------------------------------------------------------------------------
# 3.  The coboundary, by two routes that share no line
# ---------------------------------------------------------------------------


def bb(p, x, y):
    """`b(x,y)`, with the diagonal `b(x,x) = 0` supplied.

    The diagonal is not a marginal and `marginals` does not return it, but the
    coboundary of a 1-cochain is defined on DEGENERATE triples too and the star
    telescope walks straight through two of them whenever its base point is an
    interior point of the chain.  Supplying it here is what lets `star` be one
    formula instead of a formula and a case analysis."""
    if x == y:
        return Fraction(0)
    return p[(x, y)] - Fraction(1, 2)


def db_from_marginals(p, x, y, z):
    """`(db)(x,y,z) = b(x,y) + b(y,z) + b(z,x)`, from the pair marginals alone.

    Never builds a linear extension.  On non-degenerate triples this equals
    `p(x,y) + p(y,z) + p(z,x) - 3/2`; it is `0` whenever two arguments coincide."""
    return bb(p, x, y) + bb(p, y, z) + bb(p, z, x)


def triple_class_counts(P, exts, x, y, z):
    """`(cyc, acyc, nvals)` over an explicit list of linear extensions.

    `cyc` counts the words whose induced order on {x,y,z} is a ROTATION of
    (x,y,z) -- that is `x<y<z`, `y<z<x` or `z<x<y`.  `acyc` counts the other
    three.  `nvals` is the multiset of `N = #{x<y, y<z, z<x}` actually seen,
    which step 1 says is always a subset of {1,2}."""
    cyc = 0
    acyc = 0
    nvals = set()
    for w in exts:
        pos = [0] * P.n
        for t, v in enumerate(w):
            pos[v] = t
        n = ((pos[x] < pos[y]) + (pos[y] < pos[z]) + (pos[z] < pos[x]))
        nvals.add(n)
        if n == 2:
            cyc += 1
        else:
            acyc += 1
    return cyc, acyc, nvals


# ---------------------------------------------------------------------------
# 4.  The majority order and the telescope
# ---------------------------------------------------------------------------


def majority_edges(p, n, threshold):
    """Oriented pairs `(x,y)` with `p(x,y) > threshold`.  At `threshold = 1/2`
    this is the WEAK majority tournament (undecided only on exact ties); at
    `threshold = 2/3` it is the relation of BASIC-FACTS fact 2, which is total
    exactly when the counterexample hypothesis holds."""
    return [(x, y) for x in range(n) for y in range(n)
            if x != y and p[(x, y)] > threshold]


def is_acyclic(edges, n):
    """Kahn's algorithm on the oriented edge set."""
    indeg = [0] * n
    adj = [[] for _ in range(n)]
    for (x, y) in edges:
        adj[x].append(y)
        indeg[y] += 1
    q = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while q:
        v = q.pop()
        seen += 1
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return seen == n


def majority_order(p, n):
    """A total order sorting by the weak-majority relation, ties broken by index.

    Under the counterexample hypothesis the `2/3`-relation is total and
    transitive (BASIC-FACTS fact 2), and this order IS it.  Off that hypothesis
    the `2/3`-relation is partial, so a total order needs the weak relation --
    which may itself be cyclic, and `c3` checks that rather than assuming it.
    Sorting is by `sum_y [p(x,y) > 1/2]` (the Copeland score), which agrees with
    the majority order whenever the majority tournament is transitive."""
    score = [sum(1 for y in range(n) if y != x and p[(x, y)] > Fraction(1, 2))
             for x in range(n)]
    return sorted(range(n), key=lambda x: (-score[x], x))


def consecutive_sum(p, chain):
    """`SUM_i b(chain[i], chain[i+1])` -- the first sum of step 3.

    Under the counterexample hypothesis every term exceeds `1/6` when `chain` is
    the majority order, so this exceeds `(n-1)/6`."""
    return sum((bb(p, chain[i], chain[i + 1]) for i in range(len(chain) - 1)),
               Fraction(0))


def star(p, chain, base):
    """The step-3 star telescope along `chain`, based at element `base`.

    Returns `(D, terms, live, identity_rhs)` where

        D = SUM_{k=1}^{n-1} (db)(base, chain[k-1], chain[k])

    and `identity_rhs = consecutive_sum - b(base, chain[-1]) + b(base, chain[0])`.
    The two are EQUAL as an algebraic identity, at every base point and for every
    chain, because the star sum telescopes the potential `g_k = b(base, chain[k])`:

        (db)(base, c_{k-1}, c_k) = g_{k-1} + b(c_{k-1}, c_k) - g_k

    `terms` is the list of `db` values and `live` counts the NON-DEGENERATE ones.
    With `base = chain[0]` the degenerate term is the single `k = 1`, `live` is
    `n - 2` and the identity reduces to the ticket's

        b(x_1, x_n) = SUM b(x_i, x_{i+1}) - D

    since `b(base, chain[0]) = 0`.  With `base` interior TWO terms are degenerate
    and `live` is `n - 3`; the base point is the ticket's own unspent resource
    and is a parameter here rather than a hard-coded first element.
    """
    terms = [db_from_marginals(p, base, chain[k - 1], chain[k])
             for k in range(1, len(chain))]
    live = sum(1 for k in range(1, len(chain))
               if base != chain[k - 1] and base != chain[k])
    rhs = consecutive_sum(p, chain) - bb(p, base, chain[-1]) + bb(p, base, chain[0])
    return sum(terms, Fraction(0)), terms, live, rhs
