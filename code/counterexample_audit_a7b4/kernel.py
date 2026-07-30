"""Independent kernel for the mg-a7b4 audit of mg-24a3 / f5d3485.

Written from the definitions, sharing NO code with `code/counterexample_probe_24a3/`
(nor with `code/face_geometry/`, `code/hodge_leverage/`, `code/semigroup_note/`).
Where a route was available I deliberately took a DIFFERENT one from the target's,
so that a shared bug cannot cancel:

  target                                   here
  ------                                   ----
  enumerate by adjoining a MAXIMAL elt     adjoin a MINIMAL elt (dual sweep)
  canonical form certified vs A000112      ALSO certified vs A001035 (labelled
                                           posets) via the orbit-counting identity
                                           sum_classes n!/|Aut| = #labelled, which
                                           detects over- AND under-merging
  p(x,y) by splitting L at x's placement   p(x,y) = e(P + {x<y}) / e(P), a separate
                                           ideal DP on the AUGMENTED poset
  acyclicity of a quotient by Kahn         by DFS three-colouring
  #moves at a level by recursive count     by subset DP over the block set

Everything is exact (ints and Fraction).  No third-party dependencies.
"""

from fractions import Fraction
from itertools import permutations

# ---------------------------------------------------------------------------
# posets, as bitmask up/down sets over {0..n-1}
# ---------------------------------------------------------------------------


class Poset:
    __slots__ = ("n", "up", "dn", "pairs")

    def __init__(self, n, up, dn):
        self.n = n
        self.up = up            # up[x] = bitmask of y with x < y   (strict, closed)
        self.dn = dn            # dn[x] = bitmask of y with y < x
        self.pairs = None

    @staticmethod
    def from_relations(n, rels):
        """rels: iterable of (a,b) meaning a < b.  Transitively closed here."""
        up = [0] * n
        for (a, b) in rels:
            up[a] |= 1 << b
        changed = True
        while changed:
            changed = False
            for x in range(n):
                m, add = up[x], 0
                while m:
                    y = (m & -m).bit_length() - 1
                    m &= m - 1
                    add |= up[y]
                if add & ~up[x]:
                    up[x] |= add
                    changed = True
        for x in range(n):
            if (up[x] >> x) & 1:
                raise ValueError("cycle")
        dn = [0] * n
        for x in range(n):
            m = up[x]
            while m:
                y = (m & -m).bit_length() - 1
                m &= m - 1
                if (up[y] >> x) & 1:
                    raise ValueError("not antisymmetric")
                dn[y] |= 1 << x
        return Poset(n, up, dn)

    def rel_tuple(self):
        return tuple(sorted((a, b) for a in range(self.n)
                            for b in range(self.n) if (self.up[a] >> b) & 1))

    def incomparable(self):
        if self.pairs is None:
            out = []
            for a in range(self.n):
                for b in range(a + 1, self.n):
                    if not ((self.up[a] >> b) & 1 or (self.dn[a] >> b) & 1):
                        out.append((a, b))
            self.pairs = out
        return self.pairs

    def is_chain(self):
        return not self.incomparable()

    def covers_string(self):
        cov = []
        for a in range(self.n):
            m = self.up[a]
            while m:
                b = (m & -m).bit_length() - 1
                m &= m - 1
                mid = self.up[a] & self.dn[b]
                if not mid:
                    cov.append("%d<%d" % (a, b))
        return " ".join(sorted(cov)) if cov else "(antichain)"

    def incomparability_connected(self):
        """primitive == incomparability graph connected == not an ordinal sum."""
        n = self.n
        if n <= 1:
            return True
        full = (1 << n) - 1
        adj = [full & ~(self.up[x] | self.dn[x] | (1 << x)) for x in range(n)]
        seen, stack = 1, [0]
        while stack:
            x = stack.pop()
            m = adj[x] & ~seen
            while m:
                y = (m & -m).bit_length() - 1
                m &= m - 1
                seen |= 1 << y
                stack.append(y)
        return seen == full


# ---------------------------------------------------------------------------
# isomorphism: canonical key and |Aut|
# ---------------------------------------------------------------------------


def _refined_invariant(P):
    n = P.n
    inv = [(bin(P.dn[i]).count("1"), bin(P.up[i]).count("1")) for i in range(n)]
    inv = _compress(inv)
    for _ in range(n + 1):
        nxt = []
        for i in range(n):
            below = tuple(sorted(inv[j] for j in range(n) if (P.dn[i] >> j) & 1))
            above = tuple(sorted(inv[j] for j in range(n) if (P.up[i] >> j) & 1))
            nxt.append((inv[i], below, above))
        nxt = _compress(nxt)
        if nxt == inv:
            break
        inv = nxt
    return inv


def _compress(vals):
    order = {v: k for k, v in enumerate(sorted(set(vals)))}
    return [order[v] for v in vals]


def canonical_key(P):
    """Lexicographically least relation tuple over relabellings that respect the
    refined vertex invariant.  Every isomorphism respects it, so this is the same
    minimum as over all of S_n (checked against brute force in selfcheck)."""
    n = P.n
    inv = _refined_invariant(P)
    buckets = {}
    for i in range(n):
        buckets.setdefault(inv[i], []).append(i)
    slots, pos = [], 0
    for k in sorted(buckets):
        cls = buckets[k]
        slots.append((cls, tuple(range(pos, pos + len(cls)))))
        pos += len(cls)
    best = [None]
    rel = [(a, b) for a in range(n) for b in range(n) if (P.up[a] >> b) & 1]

    def rec(k, g):
        if k == len(slots):
            t = tuple(sorted((g[a], g[b]) for (a, b) in rel))
            if best[0] is None or t < best[0]:
                best[0] = t
            return
        cls, targets = slots[k]
        for perm in permutations(targets):
            g2 = dict(g)
            for i, t in zip(cls, perm):
                g2[i] = t
            rec(k + 1, g2)

    rec(0, {})
    return (n, best[0])


def canonical_key_allperms(P):
    n = P.n
    rel = [(a, b) for a in range(n) for b in range(n) if (P.up[a] >> b) & 1]
    best = None
    for g in permutations(range(n)):
        t = tuple(sorted((g[a], g[b]) for (a, b) in rel))
        if best is None or t < best:
            best = t
    return (n, best)


def aut_size(P):
    """|Aut(P)|, by brute force over permutations respecting the refined invariant."""
    n = P.n
    inv = _refined_invariant(P)
    buckets = {}
    for i in range(n):
        buckets.setdefault(inv[i], []).append(i)
    cls_list = [buckets[k] for k in sorted(buckets)]
    count = [0]
    rel = set((a, b) for a in range(n) for b in range(n) if (P.up[a] >> b) & 1)

    def rec(k, g):
        if k == len(cls_list):
            if all((g[a], g[b]) in rel for (a, b) in rel):
                count[0] += 1
            return
        cls = cls_list[k]
        for perm in permutations(cls):
            g2 = dict(g)
            for i, t in zip(cls, perm):
                g2[i] = t
            rec(k + 1, g2)

    rec(0, {})
    return count[0]


# ---------------------------------------------------------------------------
# enumeration up to isomorphism: adjoin a new MINIMAL element
# ---------------------------------------------------------------------------


def order_filters(P):
    """Up-sets of P as bitmasks (complement route to ideals)."""
    out = []
    for mask in range(1 << P.n):
        ok = True
        m = mask
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if P.up[x] & ~mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def order_ideals(P, universe=None):
    n = P.n
    if universe is None:
        universe = (1 << n) - 1
    out = []
    # iterate over subsets of `universe`
    masks = []
    m = universe
    while True:
        masks.append(m)
        if m == 0:
            break
        m = (m - 1) & universe
    for mask in masks:
        ok = True
        mm = mask
        while mm:
            x = (mm & -mm).bit_length() - 1
            mm &= mm - 1
            if P.dn[x] & universe & ~mask:
                ok = False
                break
        if ok:
            out.append(mask)
    return out


def posets_up_to_iso(n, smaller=None):
    """All posets on n elements up to isomorphism.

    Route: every finite poset has a MINIMAL element; deleting it leaves an
    (n-1)-element poset in which the deleted element's strict up-set is an order
    FILTER.  New element is labelled n-1 to keep labels compact.
    """
    if n == 0:
        return [Poset(0, [], [])]
    if n == 1:
        return [Poset(1, [0], [0])]
    if smaller is None:
        smaller = posets_up_to_iso(n - 1)
    seen = {}
    for Q in smaller:
        for filt in order_filters(Q):
            rels = [(a, b) for a in range(Q.n) for b in range(Q.n)
                    if (Q.up[a] >> b) & 1]
            for i in range(Q.n):
                if (filt >> i) & 1:
                    rels.append((n - 1, i))
            P = Poset.from_relations(n, rels)
            seen.setdefault(canonical_key(P), P)
    return [seen[k] for k in sorted(seen)]


# ---------------------------------------------------------------------------
# linear extensions, restriction counts, pair probabilities
# ---------------------------------------------------------------------------


def restriction_counts(P):
    """e[S] = number of linear extensions of P restricted to S, all S."""
    n = P.n
    e = [0] * (1 << n)
    e[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        m = S
        while m:
            x = (m & -m).bit_length() - 1
            m &= m - 1
            if not (P.dn[x] & S):          # x minimal inside S -> can go first
                tot += e[S & ~(1 << x)]
        e[S] = tot
    return e


def count_extensions_augmented(P, x, y):
    """e(P + {x<y}), by an ideal DP on the augmented poset.

    Different route from the target's, which splits L(P) at the moment x is placed.
    """
    n = P.n
    up = list(P.up)
    dn = list(P.dn)
    # add x < y and close: everything <= x gets everything >= y above it
    below_x = dn[x] | (1 << x)
    above_y = up[y] | (1 << y)
    for a in range(n):
        if (below_x >> a) & 1:
            up[a] |= above_y
    for b in range(n):
        if (above_y >> b) & 1:
            dn[b] |= below_x
    f = [0] * (1 << n)
    f[0] = 1
    for S in range(1, 1 << n):
        tot = 0
        m = S
        while m:
            a = (m & -m).bit_length() - 1
            m &= m - 1
            if not (dn[a] & S):
                tot += f[S & ~(1 << a)]
        f[S] = tot
    return f[(1 << n) - 1]


def linear_extensions(P):
    n = P.n
    out = []

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


def pair_data(P):
    """For each incomparable pair {x<y as labels}, p = Pr[x before y] as Fraction."""
    e = restriction_counts(P)
    tot = e[(1 << P.n) - 1]
    out = {}
    for (x, y) in P.incomparable():
        out[(x, y)] = Fraction(count_extensions_augmented(P, x, y), tot)
    return e, tot, out


def delta_R(P):
    """(delta, R, e, per-pair p).  delta = max min(p,1-p); R = 3*mean min(p,1-p)."""
    e, tot, ps = pair_data(P)
    if not ps:
        return None, None, tot, ps
    mins = [min(p, 1 - p) for p in ps.values()]
    delta = max(mins)
    R = 3 * sum(mins) / len(mins)
    return delta, R, tot, ps


# ---------------------------------------------------------------------------
# the bridge object: majority relation
# ---------------------------------------------------------------------------


def majority_relation(P, ps):
    """Orient each pair by its majority.  Returns (edges, tie_free, acyclic, Lstar).

    edges: set of (a,b) meaning a -> b (a majority-before b), over ALL pairs
    (comparable pairs orient with P).  Ties (p == 1/2) are left unoriented and
    flagged.
    """
    n = P.n
    edges = set()
    tie_free = True
    for a in range(n):
        for b in range(n):
            if a != b and (P.up[a] >> b) & 1:
                edges.add((a, b))
    for (x, y) in P.incomparable():
        p = ps[(x, y)]
        if p > Fraction(1, 2):
            edges.add((x, y))
        elif p < Fraction(1, 2):
            edges.add((y, x))
        else:
            tie_free = False
    adj = [0] * n
    for (a, b) in edges:
        adj[a] |= 1 << b
    order = topological_order(n, adj)
    return edges, tie_free, (order is not None), order


def topological_order(n, adj):
    """DFS three-colouring; returns a topological order or None if cyclic."""
    colour = [0] * n
    out = []

    def visit(x):
        colour[x] = 1
        m = adj[x]
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            if colour[y] == 1:
                return False
            if colour[y] == 0 and not visit(y):
                return False
        colour[x] = 2
        out.append(x)
        return True

    for x in range(n):
        if colour[x] == 0 and not visit(x):
            return None
    return out[::-1]


def find_cycle(n, adj):
    """Return a directed cycle (list of vertices) or None."""
    colour = [0] * n
    stack = []

    def visit(x):
        colour[x] = 1
        stack.append(x)
        m = adj[x]
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            if colour[y] == 1:
                return stack[stack.index(y):] + [y]
            if colour[y] == 0:
                r = visit(y)
                if r:
                    return r
        colour[x] = 2
        stack.pop()
        return None

    for x in range(n):
        if colour[x] == 0:
            r = visit(x)
            if r:
                return r
    return None


# ---------------------------------------------------------------------------
# partitions, levels, multiplicities
# ---------------------------------------------------------------------------


def set_partitions(n):
    """All set partitions of {0..n-1} as tuples of bitmasks, blocks sorted by
    least element.  Built by restricted-growth strings (a different generator
    from the target's insert-recursion)."""
    out = []
    a = [0] * n
    m = [0] * n          # m[i] = max of a[0..i-1]

    def rec(i):
        if i == n:
            k = max(a[:n]) + 1 if n else 0
            blocks = [0] * k
            for j in range(n):
                blocks[a[j]] |= 1 << j
            out.append(tuple(blocks))
            return
        top = m[i]
        for v in range(top + 1):
            a[i] = v
            if i + 1 < n:
                m[i + 1] = max(top, v + 1)
            rec(i + 1)

    if n == 0:
        return [()]
    m[0] = 0
    rec(0)
    return out


class Lattice:
    """Pi_n: partitions, refinement lists, block data.  Built once per n."""

    def __init__(self, n):
        self.n = n
        self.parts = set_partitions(n)
        self.index = {p: i for i, p in enumerate(self.parts)}
        self.nblocks = [len(p) for p in self.parts]
        self.refiners = []
        for X in self.parts:
            lst = []
            for j, Y in enumerate(self.parts):
                if len(Y) < len(X):
                    continue
                if all(any(B & ~A == 0 for A in X) for B in Y):
                    lst.append(j)
            self.refiners.append(lst)
        self.bottom = self.index[tuple(1 << i for i in range(n))]
        self.top = self.index[((1 << n) - 1,)]
        self.blockof = []
        for p in self.parts:
            v = [0] * n
            for k, B in enumerate(p):
                m = B
                while m:
                    x = (m & -m).bit_length() - 1
                    m &= m - 1
                    v[x] = k
            self.blockof.append(v)


def quotient_adj(P, blocks, blockof):
    k = len(blocks)
    adj = [0] * k
    for a in range(P.n):
        m = P.up[a]
        ia = blockof[a]
        while m:
            b = (m & -m).bit_length() - 1
            m &= m - 1
            ib = blockof[b]
            if ia != ib:
                adj[ia] |= 1 << ib
    return adj


def is_level(P, blocks, blockof):
    """A partition is a commitment level iff its quotient digraph is acyclic."""
    return topological_order(len(blocks), quotient_adj(P, blocks, blockof)) is not None


def levels_of(P, lat):
    return [i for i, blocks in enumerate(lat.parts)
            if is_level(P, blocks, lat.blockof[i])]


def multiplicities(P, lat, levels, e):
    isl = set(levels)
    m = {}
    for i in sorted(levels, key=lambda i: -lat.nblocks[i]):
        prod = 1
        for B in lat.parts[i]:
            prod *= e[B]
        s = 0
        for j in lat.refiners[i]:
            if j != i and j in isl:
                s += m[j]
        m[i] = prod - s
    return m


def count_topological_sorts(k, adj):
    """#linear orders of the k blocks compatible with the quotient DAG, by a
    subset DP (the target uses a recursive count; this is the DP route)."""
    need = [0] * k                     # need[j] = predecessors of j
    for i in range(k):
        m = adj[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            need[j] |= 1 << i
    f = [0] * (1 << k)
    f[0] = 1
    for S in range(1, 1 << k):
        tot = 0
        m = S
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            # j can be FIRST among S iff it has no predecessor inside S
            if need[j] & S & ~(1 << j):
                continue
            tot += f[S & ~(1 << j)]
        f[S] = tot
    return f[(1 << k) - 1]


def level_move_counts(P, lat, levels):
    """#moves with each level (= #topological sorts of the quotient)."""
    out = {}
    for X in levels:
        blocks = lat.parts[X]
        out[X] = count_topological_sorts(len(blocks),
                                         quotient_adj(P, blocks, lat.blockof[X]))
    return out


def moves_of(P, lat):
    """All P-compatible ordered set partitions, explicitly."""
    out = []
    for i, blocks in enumerate(lat.parts):
        k = len(blocks)
        bof = lat.blockof[i]
        adj = quotient_adj(P, blocks, bof)
        for order in permutations(range(k)):
            posn = [0] * k
            for t, bi in enumerate(order):
                posn[bi] = t
            ok = True
            for a in range(k):
                m = adj[a]
                while m:
                    b = (m & -m).bit_length() - 1
                    m &= m - 1
                    if posn[a] > posn[b]:
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                out.append(tuple(blocks[t] for t in order))
    return out


def act(move, word):
    out = []
    for B in move:
        out.extend(x for x in word if (B >> x) & 1)
    return tuple(out)
