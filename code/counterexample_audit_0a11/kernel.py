"""Independent kernel for the mg-0a11 audit of mg-dea5 / 522c1f3.

Written from the DEFINITIONS in
    docs/OneThird-Counterexample-Under-The-Action.md            (sections 1, 2, 4)
    docs/OneThird-Counterexample-Under-The-Action-Repair.md     (sections 1, 2, 3)
and from nothing else.  It imports nothing from

    code/counterexample_probe_24a3/    (the target, mg-24a3)
    code/counterexample_audit_a7b4/    (the first audit, mg-a7b4)
    code/counterexample_repair_dea5/   (the repair under audit, mg-dea5)

and shares no code with any of them.  Deliberately different routes:

  * posets are carried as up-set / down-set bitmasks, and every poset on n
    elements is generated from a poset on n-1 by adjoining a NEW MAXIMAL
    element above an order ideal;
  * isomorph rejection is by an exact canonical code -- the lexicographic
    minimum, over the permutations compatible with a Weisfeiler-Leman colour
    refinement, of the pair-symbol sequence -- with |Aut(P)| read off as the
    number of permutations attaining that minimum;
  * e(P|_S) for every subset S comes from one O(2^n n) pass;
  * p(x,y) is counted by SPLITTING linear extensions at the position of x,
    p(x,y) = sum over order ideals S with x maximal in S, y not in S, of
    e(P|_{S-x}) * e(P|_{V-S}), which never builds an augmented poset;
  * multiplicities m_X come from the DEFINING triangular system
    sum_{Y level, Y refines X} m_Y = prod_{B in X} e(P|_B)
    solved downward over the actual refinements of X -- NOT from the repair's
    multiplicativity Lemma, which is one of the things being audited.

Exact integer / rational arithmetic throughout; no floats anywhere a
comparison depends on one.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations

# --------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------


class Poset:
    """A poset on {0,...,n-1}, carried as transitively closed strict order."""

    __slots__ = ("n", "up", "down", "_e_sub", "_p", "_key")

    def __init__(self, n, up):
        self.n = n
        self.up = tuple(up)
        self.down = tuple(
            sum(1 << j for j in range(n) if up[j] >> i & 1) for i in range(n)
        )
        self._e_sub = None
        self._p = None
        self._key = None

    # -- basic predicates ---------------------------------------------------

    def less(self, x, y):
        return (self.up[x] >> y) & 1 == 1

    def incomparable_pairs(self):
        out = []
        for x in range(self.n):
            for y in range(x + 1, self.n):
                if not self.less(x, y) and not self.less(y, x):
                    out.append((x, y))
        return out

    def is_chain(self):
        return not self.incomparable_pairs()

    def covers(self):
        """Cover relations, for printing a witness."""
        out = []
        for x in range(self.n):
            for y in range(self.n):
                if self.less(x, y):
                    mid = self.up[x] & self.down[y]
                    if mid == 0:
                        out.append((x, y))
        return sorted(out)

    # -- linear extension counts -------------------------------------------

    def e_sub(self):
        """e(P|_S) for EVERY subset S, in one pass over the 2^n subsets.

        e_sub[S] = sum over x minimal in P|_S of e_sub[S - x].
        """
        if self._e_sub is not None:
            return self._e_sub
        n, down = self.n, self.down
        full = 1 << n
        f = [0] * full
        f[0] = 1
        for S in range(1, full):
            t = 0
            rest = S
            while rest:
                b = rest & -rest
                x = b.bit_length() - 1
                rest ^= b
                if down[x] & S == 0:  # x is minimal in P|_S
                    t += f[S ^ b]
            f[S] = t
        self._e_sub = f
        return f

    def e(self):
        return self.e_sub()[(1 << self.n) - 1]

    def is_ideal(self, S):
        """S is an order ideal (down-set) of P."""
        rest = S
        while rest:
            b = rest & -rest
            x = b.bit_length() - 1
            rest ^= b
            if self.down[x] & ~S:
                return False
        return True

    def ideals(self):
        return [S for S in range(1 << self.n) if self.is_ideal(S)]

    def pmat(self):
        """pmat[x][y] = # linear extensions of P placing x before y (integer).

        Split each linear extension at the position of x: the prefix is an
        order ideal S with x maximal in S, and the extension factors as
        (a linear extension of P|_{S-x}) . x . (a linear extension of P|_{V-S}).
        """
        if self._p is not None:
            return self._p
        n = self.n
        f = self.e_sub()
        full = (1 << n) - 1
        N = [[0] * n for _ in range(n)]
        for S in self.ideals():
            comp = full ^ S
            if comp == 0:
                continue
            tail = f[comp]
            rest = S
            while rest:
                b = rest & -rest
                x = b.bit_length() - 1
                rest ^= b
                if self.up[x] & S:  # x not maximal in P|_S
                    continue
                val = f[S ^ b] * tail
                if val == 0:
                    continue
                r = comp
                Nx = N[x]
                while r:
                    c = r & -r
                    y = c.bit_length() - 1
                    r ^= c
                    Nx[y] += val
        self._p = N
        return N

    def p(self, x, y):
        return Fraction(self.pmat()[x][y], self.e())

    def delta(self):
        """max over incomparable pairs of min(p, 1-p); None for a chain."""
        inc = self.incomparable_pairs()
        if not inc:
            return None
        N = self.pmat()
        tot = self.e()
        best = None
        for x, y in inc:
            a = N[x][y]
            m = min(a, tot - a)
            if best is None or m > best:
                best = m
        return Fraction(best, tot)

    def tie_free(self):
        """No incomparable pair has p(x,y) = 1/2."""
        N = self.pmat()
        tot = self.e()
        for x, y in self.incomparable_pairs():
            if 2 * N[x][y] == tot:
                return False
        return True

    def majority_edges(self):
        """x -> y iff p(x,y) > 1/2.  Comparable pairs have p = 1, so orient
        with P.  Tied pairs contribute no edge."""
        n = self.n
        N = self.pmat()
        tot = self.e()
        adj = [0] * n
        for x in range(n):
            for y in range(n):
                if x != y and 2 * N[x][y] > tot:
                    adj[x] |= 1 << y
        return adj

    def majority_cycle(self):
        """A directed cycle of the majority relation, or None."""
        adj = self.majority_edges()
        n = self.n
        colour = [0] * n
        stack = []

        def dfs(u):
            colour[u] = 1
            stack.append(u)
            r = adj[u]
            while r:
                b = r & -r
                v = b.bit_length() - 1
                r ^= b
                if colour[v] == 1:
                    return stack[stack.index(v):] + [v]
                if colour[v] == 0:
                    got = dfs(v)
                    if got:
                        return got
            colour[u] = 2
            stack.pop()
            return None

        for u in range(n):
            if colour[u] == 0:
                got = dfs(u)
                if got:
                    return got
        return None

    def Lstar(self):
        """The majority order as a list of elements in increasing order, or
        None if it is not a linear order (a tie or a cycle)."""
        if not self.tie_free():
            return None
        if self.majority_cycle() is not None:
            return None
        adj = self.majority_edges()
        order = sorted(range(self.n), key=lambda x: -bin(adj[x]).count("1"))
        # verify it really is a strict linear order extending P
        for i, x in enumerate(order):
            for y in order[i + 1:]:
                if not (adj[x] >> y) & 1:
                    return None
        for x in range(self.n):
            for y in range(self.n):
                if self.less(x, y) and order.index(x) > order.index(y):
                    return None
        return order

    # -- canonical form -----------------------------------------------------

    def _colours(self):
        """Weisfeiler-Leman style refinement on (down, up) neighbourhoods."""
        n = self.n
        col = [(bin(self.down[i]).count("1"), bin(self.up[i]).count("1"))
               for i in range(n)]
        while True:
            new = []
            for i in range(n):
                d = sorted(col[j] for j in range(n) if (self.down[i] >> j) & 1)
                u = sorted(col[j] for j in range(n) if (self.up[i] >> j) & 1)
                new.append((col[i], tuple(d), tuple(u)))
            # compress
            order = {c: k for k, c in enumerate(sorted(set(new)))}
            new = [order[c] for c in new]
            if len(set(new)) == len(set(col)):
                return new
            col = new

    def _sym(self, x, y):
        if self.less(x, y):
            return 1
        if self.less(y, x):
            return 2
        return 0

    def canon(self):
        """(canonical code, |Aut(P)|).

        The code is the lexicographic minimum, over permutations that list the
        elements in non-decreasing colour order, of the sequence

            sym(p[0],p[1]) sym(p[0],p[2]) sym(p[1],p[2]) sym(p[0],p[3]) ...

        Colour is an isomorphism invariant, so restricting to colour-sorted
        permutations is legitimate; within a colour class every order is tried.
        """
        if self._key is not None:
            return self._key
        n = self.n
        col = self._colours()
        classes = {}
        for i, c in enumerate(col):
            classes.setdefault(c, []).append(i)
        blocks = [classes[c] for c in sorted(classes)]

        best = [None]
        count = [0]

        def rec2(idx, perm, cur):
            if idx == n:
                code = tuple(cur)
                if best[0] is None or code < best[0]:
                    best[0] = code
                    count[0] = 1
                elif code == best[0]:
                    count[0] += 1
                return
            # which colour class must position idx come from?
            b = pos_block[idx]
            for x in blocks[b]:
                if x in perm:
                    continue
                row = [self._sym(q, x) for q in perm]
                cand = cur + row
                if best[0] is not None and tuple(cand) > best[0][:len(cand)]:
                    continue
                rec2(idx + 1, perm + [x], cand)

        pos_block = []
        for b, blk in enumerate(blocks):
            pos_block.extend([b] * len(blk))
        rec2(0, [], [])
        self._key = (best[0], count[0])
        return self._key

    def code(self):
        return self.canon()[0]

    def aut(self):
        return self.canon()[1]

    def __repr__(self):
        return "Poset(n=%d, covers=%s)" % (self.n, self.covers())


def from_covers(n, covers):
    """Transitive closure of a cover / relation list."""
    up = [0] * n
    for x, y in covers:
        up[x] |= 1 << y
    changed = True
    while changed:
        changed = False
        for x in range(n):
            new = up[x]
            r = up[x]
            while r:
                b = r & -r
                y = b.bit_length() - 1
                r ^= b
                new |= up[y]
            if new != up[x]:
                up[x] = new
                changed = True
    return Poset(n, up)


def restrict(P, mask):
    """P restricted to the elements of `mask`, relabelled 0..k-1."""
    elts = [i for i in range(P.n) if (mask >> i) & 1]
    idx = {x: i for i, x in enumerate(elts)}
    up = [0] * len(elts)
    for x in elts:
        for y in elts:
            if P.less(x, y):
                up[idx[x]] |= 1 << idx[y]
    return Poset(len(elts), up)


# --------------------------------------------------------------------------
# exhaustive enumeration up to isomorphism
# --------------------------------------------------------------------------


def extend(P):
    """Every poset on n+1 elements got from P by adjoining a new MAXIMAL
    element (labelled n) above an order ideal of P."""
    n = P.n
    out = []
    for S in P.ideals():
        up = list(P.up) + [0]
        for x in range(n):
            if (S >> x) & 1:
                up[x] |= 1 << n
        out.append(Poset(n + 1, up))
    return out


def enumerate_posets(nmax, keep=None, verbose=False):
    """All posets on 1..nmax elements up to isomorphism.

    `keep(P) -> bool` optionally prunes; it MUST be closed under deleting a
    maximal element for the enumeration to stay exhaustive.
    """
    levels = {1: [Poset(1, [0])]}
    for n in range(2, nmax + 1):
        seen = {}
        for P in levels[n - 1]:
            for Q in extend(P):
                if keep is not None and not keep(Q):
                    continue
                k = Q.code()
                if k not in seen:
                    seen[k] = Q
        levels[n] = list(seen.values())
        if verbose:
            print("    [enumerate n=%d: %d classes]" % (n, len(levels[n])))
    return levels


# --------------------------------------------------------------------------
# levels, multiplicities, qmass, qfrac
# --------------------------------------------------------------------------


@lru_cache(maxsize=None)
def set_partitions(elts):
    """All set partitions of a tuple of elements, each as a sorted tuple of
    sorted tuples."""
    elts = tuple(elts)
    if not elts:
        return ((),)
    if len(elts) == 1:
        return (((elts[0],),),)
    head, rest = elts[0], elts[1:]
    out = []
    for part in set_partitions(rest):
        for i in range(len(part)):
            new = list(part)
            new[i] = tuple(sorted(new[i] + (head,)))
            out.append(tuple(sorted(new)))
        out.append(tuple(sorted(part + ((head,),))))
    return tuple(sorted(set(out)))


def is_level(P, part):
    """A partition is a LEVEL iff the quotient digraph is acyclic -- i.e. iff
    the blocks admit an order making the ordered partition P-compatible."""
    k = len(part)
    where = {}
    for i, B in enumerate(part):
        for x in B:
            where[x] = i
    adj = [0] * k
    for x in range(P.n):
        r = P.up[x]
        while r:
            b = r & -r
            y = b.bit_length() - 1
            r ^= b
            if where[x] != where[y]:
                adj[where[x]] |= 1 << where[y]
    colour = [0] * k

    def dfs(u):
        colour[u] = 1
        r = adj[u]
        while r:
            b = r & -r
            v = b.bit_length() - 1
            r ^= b
            if colour[v] == 1:
                return False
            if colour[v] == 0 and not dfs(v):
                return False
        colour[u] = 2
        return True

    for u in range(k):
        if colour[u] == 0 and not dfs(u):
            return False
    return True


def refinements(part):
    """All partitions refining `part` (including itself)."""
    per_block = [set_partitions(B) for B in part]
    out = [()]
    for choices in per_block:
        out = [acc + ch for acc in out for ch in choices]
    return [tuple(sorted(p)) for p in out]


def level_data(P):
    """(levels, m) with m the multiplicity from the DEFINING system

        sum_{Y level, Y refines X} m_Y = prod_{B in X} e(P|_B) ,

    solved downward.  No use of the repair's multiplicativity Lemma.
    """
    V = tuple(range(P.n))
    f = P.e_sub()

    def F(part):
        t = 1
        for B in part:
            t *= f[sum(1 << x for x in B)]
        return t

    all_parts = set_partitions(V)
    levels = set(p for p in all_parts if is_level(P, p))
    m = {}
    for X in sorted(levels, key=len, reverse=True):  # finest (most blocks) first
        s = 0
        for Y in refinements(X):
            if Y != X and Y in levels:
                s += m[Y]
        m[X] = F(X) - s
    return levels, m


def interval_partitions(order):
    """The 2^(n-1) partitions of `order` into contiguous intervals."""
    n = len(order)
    out = []
    for mask in range(1 << (n - 1)):
        part = []
        cur = [order[0]]
        for i in range(1, n):
            if (mask >> (i - 1)) & 1:
                part.append(tuple(sorted(cur)))
                cur = [order[i]]
            else:
                cur.append(order[i])
        part.append(tuple(sorted(cur)))
        out.append(tuple(sorted(part)))
    return out


def qstats(P):
    """(qfrac, qmass, #levels, #interval partitions that are levels).

    qfrac = 2^(n-1) / |Q(P)| ,
    qmass = ( sum of m_X over the L*-interval partitions ) / e(P) .
    """
    order = P.Lstar()
    if order is None:
        return None
    levels, m = level_data(P)
    iv = interval_partitions(order)
    ivset = set(iv)
    good = sum(1 for X in ivset if X in levels)
    mass = sum(m[X] for X in ivset if X in levels)
    qfrac = Fraction(1 << (P.n - 1), len(levels))
    qmass = Fraction(mass, P.e())
    return qfrac, qmass, len(levels), good
