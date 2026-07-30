"""Self-contained core for the counterexample-detection probe (mg-24a3).

Nothing here imports from `code/face_geometry/`, `code/hodge_leverage/` or
`code/semigroup_note/`.  Every object is rebuilt from its definition so that the
numbers this probe reports are independent of the pipeline they are about.
Exact arithmetic throughout (Python ints and `fractions.Fraction`).

The objects, and the definitions used:

  Poset P on {0..n-1}                strict relation, transitively closed.
  L(P)                               linear extensions, as words.
  e(P|_S)                            #linear extensions of the induced subposet on S.
  p(x,y)                             |{w in L(P) : x before y}| / e(P).
  delta(P)                           max over incomparable pairs of min(p, 1-p).
                                     "frozen" = delta < 1/3 = counterexample condition.
  move                               a P-compatible ordered set partition (a face of
                                     the order cone): whenever i <_P j, block(i) is
                                     not strictly after block(j).
  level (commitment level)           the unordered partition underlying a move.
  Q(P)                               the set of levels, ordered by refinement.
  m_X                                multiplicity, from  sum_{Y level, Y refines X} m_Y
                                     = prod_{B in X} e(P|_B).
  lambda_X(w)                        total w-probability of moves whose level is
                                     coarser than or equal to X.
"""

from fractions import Fraction
from itertools import combinations, permutations


# --------------------------------------------------------------------------
# 1.  Posets
# --------------------------------------------------------------------------

class Poset:
    """A finite poset on {0..n-1}; `less` is the transitively closed strict relation."""

    __slots__ = ("n", "less", "up", "dn", "_key")

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
        # bitmask up-sets and down-sets (strict)
        self.up = [0] * n
        self.dn = [0] * n
        for (a, b) in less:
            self.up[a] |= 1 << b
            self.dn[b] |= 1 << a
        self._key = None

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

    # ---- canonical form (isomorphism invariant) --------------------------

    def _vertex_classes(self):
        """Iteratively refined vertex invariant; returns a list of index lists,
        the classes in a canonical (sorted-by-invariant) order."""
        n = self.n
        inv = [(bin(self.dn[i]).count("1"), bin(self.up[i]).count("1")) for i in range(n)]
        for _ in range(n):
            new = []
            for i in range(n):
                dnb = sorted(inv[j] for j in range(n) if (self.dn[i] >> j) & 1)
                upb = sorted(inv[j] for j in range(n) if (self.up[i] >> j) & 1)
                new.append((inv[i], tuple(dnb), tuple(upb)))
            # compress to small ranks so the tuples do not grow
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
        """Lexicographically minimal relation tuple over all isomorphic relabellings.

        Only relabellings that respect the refined vertex invariant are tried;
        every isomorphism does, so the minimum is the same as over all of S_n.
        `selftest.py` checks this against the brute-force minimum over all n!.
        """
        if self._key is not None:
            return self._key
        n = self.n
        classes = self._vertex_classes()
        slots = []
        pos = 0
        for cls in classes:
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

    def canonical_key_bruteforce(self):
        best = None
        for g in permutations(range(self.n)):
            rel = tuple(sorted((g[a], g[b]) for (a, b) in self.less))
            if best is None or rel < best:
                best = rel
        return (self.n, best)

    def cover_string(self):
        covers = []
        for (a, b) in sorted(self.less):
            if not any((a, c) in self.less and (c, b) in self.less for c in range(self.n)):
                covers.append("%d<%d" % (a, b))
        return " ".join(covers) if covers else "(antichain)"

    def incomparability_connected(self):
        """Connectivity of the INcomparability graph.  Connected == primitive ==
        not an ordinal sum (ledger row 2).  A one-element poset counts as
        connected by convention; chains on n >= 2 are disconnected."""
        n = self.n
        if n <= 1:
            return True
        adj = [0] * n
        for a in range(n):
            for b in range(n):
                if a != b and not self.comparable(a, b):
                    adj[a] |= 1 << b
        seen = 1
        stack = [0]
        while stack:
            x = stack.pop()
            m = adj[x] & ~seen
            while m:
                y = (m & -m).bit_length() - 1
                m &= m - 1
                seen |= 1 << y
                stack.append(y)
        return seen == (1 << n) - 1


def all_posets_bruteforce(n):
    """All posets on n elements up to isomorphism, by sweeping transitively
    closed subsets of {(i,j) : i<j} and deduplicating on the canonical key.
    Exponential in n(n-1)/2; used directly for n <= 6 and as the control for the
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
            P = Poset(n, rel)
            seen.setdefault(P.canonical_key(), P)
    return [seen[k] for k in sorted(seen)]


def order_ideals(P):
    """Down-sets of P, as bitmasks."""
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
    ideal of the smaller poset.  Complete because every finite poset has a
    maximal element, and deleting it leaves an (n-1)-element poset with the
    deleted element's down-set an ideal."""
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


# --------------------------------------------------------------------------
# 2.  Linear extensions, restriction counts, and the balance constant delta
# --------------------------------------------------------------------------

def linear_extensions(P):
    """L(P) as words: w[t] = element in position t.  From the definition."""
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
    out.sort()
    return out


def restriction_counts(P):
    """e[S] = e(P|_S) for EVERY subset S of {0..n-1}, as a list indexed by bitmask.

    DP on the definition: a linear extension of P|_S ends in an element maximal
    in P|_S, so e[S] = sum over x maximal in P|_S of e[S \\ {x}]."""
    n = P.n
    e = [0] * (1 << n)
    e[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if not (P.up[x] & S):          # x is maximal inside S
                tot += e[S & ~(1 << x)]
        e[S] = tot
    return e


def pair_before_counts(P, e):
    """before[(x,y)] = |{w in L(P) : x before y}| for every ordered pair x != y.

    Derivation used: split a linear extension at the moment x is placed.  If the
    prefix set at that moment is S then S is a down-set of P, x is maximal in S,
    and y not in S; the prefix can be completed in e(P|_{S\\{x}}) ways and the
    suffix in e(P|_{S^c}) ways, and every extension with x before y is counted
    exactly once (the prefix S is determined by the extension and x).
    """
    n = P.n
    full = (1 << n) - 1
    ideals = order_ideals(P)
    before = {}
    for (x, y) in [(a, b) for a in range(n) for b in range(n) if a != b]:
        tot = 0
        bx, by = 1 << x, 1 << y
        for S in ideals:
            if not (S & bx) or (S & by):
                continue
            if P.up[x] & S:                # x not maximal in S: cannot be last
                continue
            tot += e[S & ~bx] * e[full & ~S]
        before[(x, y)] = tot
    return before


def delta_of(P, e, before):
    """The balance constant: max over incomparable pairs of min(p, 1-p).

    Returns (delta, worst_pair_balance, per_pair) with delta = None for a chain
    (no incomparable pairs, so the conjecture says nothing).  `per_pair` maps the
    unordered pair to Fraction min(p, 1-p)."""
    tot = e[(1 << P.n) - 1]
    per = {}
    for (a, b) in P.incomparable_pairs():
        p = Fraction(before[(a, b)], tot)
        per[(a, b)] = min(p, 1 - p)
    if not per:
        return None, None, per
    return max(per.values()), min(per.values()), per


# --------------------------------------------------------------------------
# 3.  Set partitions, refinement, and the level structure Q(P)
# --------------------------------------------------------------------------

def part_key(blocks):
    """The canonical key of a partition given as any iterable of bitmasks:
    the blocks in increasing order of their minimum element.  `set_partitions`
    produces its tuples in exactly this order, so this is the key into
    `PartitionLattice.index`."""
    return tuple(sorted(blocks, key=lambda B: B & -B))


def set_partitions(n):
    """All set partitions of {0..n-1}, each as a tuple of bitmasks ordered by
    minimum element."""
    if n == 0:
        return [()]
    out = []
    def rec(i, blocks):
        if i == n:
            out.append(tuple(blocks))
            return
        for k in range(len(blocks)):
            blocks[k] |= 1 << i
            rec(i + 1, blocks)
            blocks[k] &= ~(1 << i)
        blocks.append(1 << i)
        rec(i + 1, blocks)
        blocks.pop()
    rec(0, [])
    return out


class PartitionLattice:
    """The partition lattice Pi_n, precomputed once per n and shared by every
    poset: the partitions, the refinement relation, and the block lists."""

    def __init__(self, n):
        self.n = n
        self.parts = set_partitions(n)
        self.index = {p: i for i, p in enumerate(self.parts)}
        self.nblocks = [len(p) for p in self.parts]
        # refiners[i] = indices j with parts[j] refining parts[i] (j <= i in the
        # refinement order), including i itself.
        self.refiners = []
        for i, X in enumerate(self.parts):
            lst = []
            for j, Y in enumerate(self.parts):
                if len(Y) < len(X):
                    continue
                if all(any(B & ~A == 0 for A in X) for B in Y):
                    lst.append(j)
            self.refiners.append(lst)
        self.bottom = self.index[tuple(1 << i for i in range(n))]
        self.top = self.index[((1 << n) - 1,)]

    def block_id_vector(self, i):
        v = [0] * self.n
        for k, B in enumerate(self.parts[i]):
            m = B
            while m:
                x = (m & -m).bit_length() - 1
                m &= m - 1
                v[x] = k
        return v


def quotient_is_acyclic(P, blocks):
    """Contract each block to a point, keep induced arrows between DISTINCT
    blocks, and ask for no directed cycle.  This is the level condition."""
    k = len(blocks)
    of = [0] * P.n
    for idx, B in enumerate(blocks):
        m = B
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            of[x] = idx
    adj = [0] * k
    for (a, b) in P.less:
        ia, ib = of[a], of[b]
        if ia != ib:
            adj[ia] |= 1 << ib
    # Kahn: repeatedly remove a source
    indeg = [0] * k
    for i in range(k):
        m = adj[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] += 1
    stack = [i for i in range(k) if indeg[i] == 0]
    removed = 0
    while stack:
        i = stack.pop()
        removed += 1
        m = adj[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] -= 1
            if indeg[j] == 0:
                stack.append(j)
    return removed == k


def levels_of(P, lat):
    """Indices (into lat.parts) of the commitment levels of P."""
    return [i for i, blocks in enumerate(lat.parts) if quotient_is_acyclic(P, blocks)]


def multiplicities(P, lat, level_idx, e):
    """m_X for every level X, from  sum_{Y level, Y refines X} m_Y = prod_B e(P|_B).

    Solved from the finest level upwards (finest first: more blocks first)."""
    isl = set(level_idx)
    m = {}
    for i in sorted(level_idx, key=lambda i: -lat.nblocks[i]):
        prod = 1
        for B in lat.parts[i]:
            prod *= e[B]
        s = 0
        for j in lat.refiners[i]:
            if j != i and j in isl:
                s += m[j]
        m[i] = prod - s
    return m


# --------------------------------------------------------------------------
# 4.  Moves, weights, and the spectrum
# --------------------------------------------------------------------------

def moves_of(P):
    """All P-compatible ordered set partitions, as tuples of bitmasks in block
    order.  Enumerated from the definition: for each set partition, keep every
    ordering of the blocks in which no relation i <_P j points strictly
    backwards."""
    out = []
    n = P.n
    for blocks in set_partitions(n):
        k = len(blocks)
        for order in permutations(range(k)):
            seq = [blocks[t] for t in order]
            of = [0] * n
            for idx, B in enumerate(seq):
                m = B
                while m:
                    x = (m & -m).bit_length() - 1
                    m &= m - 1
                    of[x] = idx
            if all(of[a] <= of[b] for (a, b) in P.less):
                out.append(tuple(seq))
    return out


def act(move, word):
    """The action: elements of block 1 first, then block 2, ..., and inside each
    block in the order they already stand in `word`."""
    out = []
    for B in move:
        out.extend(x for x in word if (B >> x) & 1)
    return tuple(out)


def support_index(move, lat):
    """The commitment level of a move: forget the block order, keep the blocks."""
    return lat.index[part_key(move)]


def uniform_move_spectrum(P, lat, level_idx, mult):
    """The spectrum of the walk under the weight that is UNIFORM on all
    P-compatible moves.  Exact rationals.

    lambda_X = (#moves whose level is coarser than or equal to X) / #moves, and
    "level(y) coarser than or equal to X" means X refines level(y).
    Returns (lambda per level, lambda_2, n_moves).
    """
    moves = moves_of(P)
    cnt = {}
    for mv in moves:
        i = support_index(mv, lat)
        cnt[i] = cnt.get(i, 0) + 1
    nm = len(moves)
    lam = {}
    for X in level_idx:
        # levels coarser than or equal to X = levels Y with X in refiners[Y]
        tot = 0
        for Y, c in cnt.items():
            if X in lat.refiners[Y]:
                tot += c
        lam[X] = Fraction(tot, nm)
    # lambda_2: largest lambda over levels with m > 0 other than the finest
    cands = [lam[X] for X in level_idx if mult[X] > 0 and X != lat.bottom]
    lam2 = max(cands) if cands else Fraction(0)
    return lam, lam2, nm, cnt


def move_pair_stats(P, moves):
    """For each unordered incomparable pair, the uniform-move probabilities
      s   = both in the same block  (the move inherits the pair's order),
      qxy = x's block strictly before y's,
      qyx = y's block strictly before x's,
    and the walk's stationary pair marginal, which satisfies
      pi(x<y) = qxy + s * pi(x<y)   =>   pi(x<y) = qxy / (qxy + qyx).
    """
    nm = len(moves)
    out = {}
    for (x, y) in P.incomparable_pairs():
        same = bx = by = 0
        for mv in moves:
            for idx, B in enumerate(mv):
                if (B >> x) & 1:
                    ix = idx
                if (B >> y) & 1:
                    iy = idx
            if ix == iy:
                same += 1
            elif ix < iy:
                bx += 1
            else:
                by += 1
        out[(x, y)] = (Fraction(same, nm), Fraction(bx, nm), Fraction(by, nm),
                       Fraction(bx, bx + by) if bx + by else None)
    return out
