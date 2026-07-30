"""Posets, exhaustively up to isomorphism, and the two balance statistics.

Written for mg-dea5.  Imports nothing from code/counterexample_probe_24a3/ or
code/counterexample_audit_a7b4/ and shares no code with either.  Exact integer /
Fraction arithmetic throughout; no floats anywhere a comparison depends on one.

A poset on n elements is stored as `Poset(n, up, down)` with `up[i]` / `down[i]`
bitmasks of the STRICT up-set / down-set, transitively closed.

Route notes (deliberately different from both prior instruments):

  * e(P|_S) for EVERY subset S at once, by the bottom-up subset recursion
    e(S) = sum over minimal x of S of e(S - x).  One O(2^n n) pass per poset
    yields every induced-subposet count, which is what the level multiplicities
    need (see levels.py).
  * p(x,y) as e(P + {x<y}) / e(P) on the transitively closed augmentation, by the
    same subset recursion run on the augmented relation.
  * isomorph rejection by an explicit canonical labelling: colour refinement to
    an isomorphism-invariant vertex ordering, then a branch-and-bound minimum
    over the colour-compatible relabellings of an incrementally-comparable
    encoding.
"""

from fractions import Fraction
from itertools import combinations


# --------------------------------------------------------------------------
# construction
# --------------------------------------------------------------------------

class Poset:
    __slots__ = ("n", "up", "down", "_e", "_key")

    def __init__(self, n, up, down):
        self.n = n
        self.up = up
        self.down = down
        self._e = None
        self._key = None

    # -- basic predicates -------------------------------------------------

    def leq(self, i, j):
        return i == j or bool(self.up[i] >> j & 1)

    def comparable(self, i, j):
        return i == j or bool(self.up[i] >> j & 1) or bool(self.down[i] >> j & 1)

    def incomparable_pairs(self):
        return [(i, j) for i in range(self.n) for j in range(i + 1, self.n)
                if not self.comparable(i, j)]

    def is_chain(self):
        return not self.incomparable_pairs()

    def cover_string(self):
        """The cover relations, as a stable text label."""
        out = []
        for i in range(self.n):
            for j in range(self.n):
                if self.up[i] >> j & 1:
                    mid = self.up[i] & self.down[j]
                    if mid == 0:
                        out.append("%d<%d" % (i, j))
        return " ".join(out)


def transitive_closure(n, rel):
    """rel: list of bitmasks of DIRECT strict relations.  Returns closed up-sets."""
    up = list(rel)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            m = up[i]
            new = m
            r = m
            while r:
                b = r & -r
                r ^= b
                new |= up[b.bit_length() - 1]
            if new != m:
                up[i] = new
                changed = True
    return up


def make(n, up):
    """Build a Poset from (already transitively closed) strict up-sets."""
    down = [0] * n
    for i in range(n):
        r = up[i]
        while r:
            b = r & -r
            r ^= b
            down[b.bit_length() - 1] |= 1 << i
    # antisymmetry / irreflexivity, asserted rather than assumed
    for i in range(n):
        assert not (up[i] >> i & 1), "irreflexivity"
        assert up[i] & down[i] == 0, "antisymmetry"
    return Poset(n, tuple(up), tuple(down))


def from_covers(n, covers):
    """covers: iterable of (i, j) meaning i < j.  Transitively closed here."""
    rel = [0] * n
    for i, j in covers:
        rel[i] |= 1 << j
    return make(n, transitive_closure(n, rel))


def induced(P, mask):
    """P restricted to the elements of `mask`, relabelled 0.. in bit order."""
    idx = []
    r = mask
    while r:
        b = r & -r
        r ^= b
        idx.append(b.bit_length() - 1)
    k = len(idx)
    pos = {v: t for t, v in enumerate(idx)}
    up = [0] * k
    for t, v in enumerate(idx):
        r = P.up[v] & mask
        while r:
            b = r & -r
            r ^= b
            up[t] |= 1 << pos[b.bit_length() - 1]
    return make(k, up)


# --------------------------------------------------------------------------
# canonical form
# --------------------------------------------------------------------------

def _refine(n, up, down):
    """Isomorphism-invariant vertex colours, by iterated neighbourhood refinement."""
    col = []
    for i in range(n):
        col.append((bin(up[i]).count("1"), bin(down[i]).count("1")))
    col = _renumber(col)
    for _ in range(n):
        nxt = []
        for i in range(n):
            a = sorted(col[j] for j in _bits(up[i]))
            b = sorted(col[j] for j in _bits(down[i]))
            nxt.append((col[i], tuple(a), tuple(b)))
        nxt = _renumber(nxt)
        if nxt == col:
            break
        col = nxt
    return col


def _renumber(vals):
    order = {v: k for k, v in enumerate(sorted(set(vals)))}
    return [order[v] for v in vals]


def _bits(m):
    out = []
    while m:
        b = m & -m
        m ^= b
        out.append(b.bit_length() - 1)
    return out


def canonical(P):
    """A canonical encoding: equal iff isomorphic.

    The encoding is read off pair by pair in the order
    (0,1),(1,0),(0,2),(2,0),(1,2),(2,1),(0,3),... so that a partial labelling
    already determines a prefix and the search can be pruned.  Only labellings
    that place the vertices in non-decreasing refined-colour order are
    considered; the colour sequence is isomorphism-invariant, so restricting to
    those is harmless, and it is prepended to the encoding.
    """
    if P._key is not None:
        return P._key
    n, up, down = P.n, P.up, P.down
    col = _refine(n, up, down)
    csig = tuple(sorted(col))
    buckets = {}
    for i, c in enumerate(col):
        buckets.setdefault(c, []).append(i)
    order = [c for c in sorted(buckets)]
    # counts of each colour, in the order they must be placed
    plan = []
    for c in order:
        plan.extend([c] * len(buckets[c]))

    best = [None]
    placed = []
    used = [False] * n

    def word(v):
        """the 2k bits added by placing v as the k-th vertex"""
        w = 0
        for t, u in enumerate(placed):
            w = (w << 2) | ((up[u] >> v & 1) << 1) | (up[v] >> u & 1)
        return w

    def rec(prefix):
        k = len(placed)
        if k == n:
            t = tuple(prefix)
            if best[0] is None or t < best[0]:
                best[0] = t
            return
        want = plan[k]
        seen = set()
        cands = []
        for v in buckets[want]:
            if used[v]:
                continue
            w = word(v)
            cands.append((w, v))
        if not cands:
            return
        cands.sort()
        for w, v in cands:
            nxt = prefix + [w]
            if best[0] is not None:
                b = best[0][:len(nxt)]
                if tuple(nxt) > b:
                    continue
            if w in seen and len(cands) > 6:
                # same prefix contribution; explored already at this node.  Only
                # applied when the colour class is large enough that the full
                # search would be wasteful -- see controls.py, which checks the
                # canonical form against brute force over all n! relabellings.
                continue
            seen.add(w)
            used[v] = True
            placed.append(v)
            rec(nxt)
            placed.pop()
            used[v] = False

    rec([])
    P._key = (n, csig, best[0])
    return P._key


def canonical_bruteforce(P):
    """Minimum relation encoding over ALL n! relabellings.  Controls only."""
    from itertools import permutations
    n, up = P.n, P.up
    best = None
    for perm in permutations(range(n)):
        rows = []
        for i in range(n):
            r = 0
            for j in range(n):
                if up[perm[i]] >> perm[j] & 1:
                    r |= 1 << j
            rows.append(r)
        t = tuple(rows)
        if best is None or t < best:
            best = t
    return (n, best)


# --------------------------------------------------------------------------
# exhaustive enumeration up to isomorphism
# --------------------------------------------------------------------------

def _ideals(P):
    """All down-closed subsets of P, as bitmasks."""
    n = P.n
    out = []
    for mask in range(1 << n):
        ok = True
        r = mask
        while r:
            b = r & -r
            r ^= b
            if P.down[b.bit_length() - 1] & ~mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def all_posets(n):
    """Every poset on n elements up to isomorphism.

    Built by adjoining a new MAXIMAL element whose strict down-set is an
    arbitrary order ideal of a poset on n-1 elements, then rejecting isomorphs.
    """
    if n == 0:
        return [make(0, [])]
    cur = [make(1, [0])]
    for k in range(2, n + 1):
        seen = {}
        for P in cur:
            for D in _ideals(P):
                up = [P.up[i] | ((1 << (k - 1)) if (D >> i & 1) else 0)
                      for i in range(k - 1)] + [0]
                Q = make(k, up)
                key = canonical(Q)
                if key not in seen:
                    seen[key] = Q
        cur = list(seen.values())
    return cur


# --------------------------------------------------------------------------
# linear extension counts, pair probabilities, delta, L*
# --------------------------------------------------------------------------

def e_all_subsets(P):
    """e[S] = number of linear extensions of P|_S, for every subset S."""
    n = P.n
    down = P.down
    e = [0] * (1 << n)
    e[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        r = S
        while r:
            b = r & -r
            r ^= b
            i = b.bit_length() - 1
            if down[i] & S == 0:          # i minimal in P|_S
                tot += e[S ^ b]
        e[S] = tot
    return e


def e_of(P):
    if P._e is None:
        P._e = e_all_subsets(P)[(1 << P.n) - 1]
    return P._e


def _e_full_augmented(P, x, y):
    """e(P + {x<y}), transitively closed."""
    n = P.n
    up = list(P.up)
    lower_x = P.down[x] | (1 << x)
    upper_y = P.up[y] | (1 << y)
    for i in _bits(lower_x):
        up[i] |= upper_y
    Q = make(n, transitive_closure(n, up))
    full = (1 << n) - 1
    down = Q.down
    e = [0] * (1 << n)
    e[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        r = S
        while r:
            b = r & -r
            r ^= b
            i = b.bit_length() - 1
            if down[i] & S == 0:
                tot += e[S ^ b]
        e[S] = tot
    return e[full]


def pair_probs(P):
    """{(i,j): p(i,j)} over incomparable pairs i<j, as exact Fractions."""
    tot = e_of(P)
    out = {}
    for (i, j) in P.incomparable_pairs():
        out[(i, j)] = Fraction(_e_full_augmented(P, i, j), tot)
    return out


def delta_of(probs):
    if not probs:
        return None
    return max(min(p, 1 - p) for p in probs.values())


def tie_free(probs):
    return all(p != Fraction(1, 2) for p in probs.values())


def majority_edges(P, probs):
    """Strict-majority orientation: x -> y iff p(x,y) > 1/2.  Ties unoriented."""
    adj = [0] * P.n
    for i in range(P.n):
        for j in range(P.n):
            if i != j and (P.up[i] >> j & 1):
                adj[i] |= 1 << j
    for (i, j), p in probs.items():
        if p > Fraction(1, 2):
            adj[i] |= 1 << j
        elif p < Fraction(1, 2):
            adj[j] |= 1 << i
    return adj


def find_cycle(n, adj):
    """A directed cycle in `adj`, as a vertex list, or None.  DFS 3-colouring."""
    colour = [0] * n
    stack = []

    def dfs(v):
        colour[v] = 1
        stack.append(v)
        for w in _bits(adj[v]):
            if colour[w] == 1:
                return stack[stack.index(w):] + [w]
            if colour[w] == 0:
                got = dfs(w)
                if got:
                    return got
        colour[v] = 2
        stack.pop()
        return None

    for v in range(n):
        if colour[v] == 0:
            got = dfs(v)
            if got:
                return got
    return None


def lstar(P, probs):
    """The majority linear order, as a list of elements in increasing order.

    Returns None if the majority relation has a tie or a cycle (in which case it
    is not a linear order and neither statistic of section 4 is defined).
    """
    if not tie_free(probs):
        return None
    adj = majority_edges(P, probs)
    if find_cycle(P.n, adj) is not None:
        return None
    n = P.n
    order = sorted(range(n), key=lambda v: -bin(adj[v]).count("1"))
    # a tournament with no cycle is a linear order; out-degree gives the rank
    for a in range(n):
        for b in range(a + 1, n):
            assert (adj[order[a]] >> order[b] & 1), "majority order inconsistent"
    return order
