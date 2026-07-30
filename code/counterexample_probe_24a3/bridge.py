"""The bridge object of the mg-24a3 addendum: the majority tournament, the
distinguished linear extension L*, and the concentration quantity.

Definitions (all exact, all rational):

  p(x,y)        Pr[x before y] under the UNIFORM measure on L(P).
  Inc(P)        the incomparable pairs.
  delta(P)      max over Inc(P) of min(p, 1-p).      <- the conjecture's statistic
  M(P)          the majority digraph: x -> y iff p(x,y) > 1/2.  Comparable pairs
                have p = 1 and orient with P, so M contains P.
  tie           an incomparable pair with p = 1/2 exactly.  A counterexample has
                none (p outside [1/3,2/3] excludes 1/2), so on the counterexample
                population M is a TOTAL orientation -- a tournament.
  L*            when M is acyclic, any linear order extending it.  Unique iff P
                is tie-free.  L* extends P, so L* is a linear extension of P.
  inv(L,L*)     #pairs on which L and L* disagree.

The identity this module is built on (proved in the deliverable, checked in
selftest-style below):

  E_{L ~ uniform on L(P)} [ inv(L, L*) ]  =  sum over Inc(P) of min(p, 1-p)

-- because L disagrees with L* on a pair exactly when it takes the minority side,
and comparable pairs never disagree.  Note the right-hand side does not mention
the tie-break, so E[inv] is the same for every choice of L*.

  R(P) := E[inv(L,L*)] / (|Inc(P)|/3) = 3 * mean over Inc(P) of min(p,1-p)

The addendum's concentration statement is that a counterexample has R(P) < 1.
Since R is 3x the MEAN and 3*delta is 3x the MAX of the same per-pair numbers,

  R(P) <= 3 * delta(P)                                        (mean <= max)

so R < 1 is a strictly weaker condition than the counterexample condition
3*delta < 1.  How much weaker is measured, not asserted.
"""

from fractions import Fraction

from core import (Poset, linear_extensions, restriction_counts,
                  pair_before_counts, delta_of, order_ideals)


class Bridge:
    """The bridge data of one poset."""

    __slots__ = ("P", "n", "e", "per_pair", "p", "delta", "ties", "succ",
                 "acyclic", "Lstar", "Einv", "ninc", "R", "cyc_best", "tie_free")

    def __init__(self, P, e=None, before=None):
        n = P.n
        self.P = P
        self.n = n
        if e is None:
            e = restriction_counts(P)
        if before is None:
            before = pair_before_counts(P, e)
        tot = e[(1 << n) - 1]
        self.e = tot
        self.p = {}
        for x in range(n):
            for y in range(n):
                if x != y:
                    self.p[(x, y)] = Fraction(before[(x, y)], tot)
        self.delta, _, self.per_pair = delta_of(P, e, before)
        self.ninc = len(self.per_pair)
        self.ties = [pr for pr, v in self.per_pair.items() if v == Fraction(1, 2)]
        self.tie_free = not self.ties
        # the strict majority digraph
        succ = [0] * n
        for x in range(n):
            for y in range(n):
                if x != y and self.p[(x, y)] > Fraction(1, 2):
                    succ[x] |= 1 << y
        self.succ = succ
        self.Lstar = _topo_lex_least(n, succ)
        self.acyclic = self.Lstar is not None
        # E[inv(L,L*)] and the concentration ratio
        self.Einv = sum(self.per_pair.values()) if self.per_pair else Fraction(0)
        self.R = (Fraction(3) * self.Einv / self.ninc) if self.ninc else None
        # the cyclic branch: the strongest majority cycle available
        self.cyc_best = _best_cycle_strength(n, succ, self.p)

    # -- the concentration geometry ---------------------------------------

    def inv_distribution(self):
        """The exact law of inv(L, L*) over the uniform measure on L(P)."""
        if self.Lstar is None:
            return None
        rank = {x: k for k, x in enumerate(self.Lstar)}
        dist = {}
        for w in linear_extensions(self.P):
            pos = {x: k for k, x in enumerate(w)}
            d = 0
            for (a, b) in self.per_pair:
                if (pos[a] < pos[b]) != (rank[a] < rank[b]):
                    d += 1
            dist[d] = dist.get(d, 0) + 1
        return dist

    def ball_mass(self, radius):
        """Pr[inv(L,L*) < radius] exactly."""
        dist = self.inv_distribution()
        if dist is None:
            return None
        num = sum(c for d, c in dist.items() if d < radius)
        return Fraction(num, self.e)


def _topo_lex_least(n, succ):
    """The lexicographically least topological order of the digraph, or None if
    it has a directed cycle."""
    indeg = [0] * n
    for i in range(n):
        m = succ[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] += 1
    out = []
    avail = [i for i in range(n) if indeg[i] == 0]
    while avail:
        avail.sort()
        i = avail.pop(0)
        out.append(i)
        m = succ[i]
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            indeg[j] -= 1
            if indeg[j] == 0:
                avail.append(j)
    return tuple(out) if len(out) == n else None


def _best_cycle_strength(n, succ, p):
    """max over directed cycles of M of the MINIMUM edge strength max(p,1-p).

    A counterexample whose majority tournament is cyclic needs a cycle every edge
    of which is decided by a margin > 2/3, so this number would have to exceed
    2/3.  Returns None if M is acyclic (no cycle exists)."""
    best = None
    # only need to look at cycles; enumerate simple cycles by DFS (n <= 7 here)
    def dfs(start, cur, visited, weakest):
        nonlocal best
        m = succ[cur]
        while m:
            nxt = (m & -m).bit_length() - 1
            m &= m - 1
            w = min(weakest, max(p[(cur, nxt)], 1 - p[(cur, nxt)]))
            if nxt == start:
                if best is None or w > best:
                    best = w
            elif not ((visited >> nxt) & 1):
                dfs(start, nxt, visited | (1 << nxt), w)
    for s in range(n):
        dfs(s, s, 1 << s, Fraction(1))
    return best


# --------------------------------------------------------------------------
# the quotient side: L*'s own chain inside Q(P)
# --------------------------------------------------------------------------

def lstar_interval_levels(n, Lstar):
    """The partitions whose blocks are contiguous intervals of L*, as canonical
    partition keys.  There are 2^(n-1) of them (one per composition of n), and
    every one is a level: ordering the blocks along L* is P-compatible because L*
    extends P."""
    out = []
    for cut in range(1 << (n - 1)):
        blocks = []
        cur = 1 << Lstar[0]
        for i in range(1, n):
            if (cut >> (i - 1)) & 1:
                blocks.append(cur)
                cur = 0
            cur |= 1 << Lstar[i]
        blocks.append(cur)
        out.append(tuple(sorted(blocks, key=lambda B: B & -B)))
    return out


def quotient_concentration(rec, br, lat):
    """How much of Q(P) and of the spectrum sits on L*'s own chain.

    Returns (frac_levels, mult_mass, n_interval_levels) with
      frac_levels = 2^(n-1) / |Q(P)|                 -- share of the levels
      mult_mass   = (sum of m_X over those) / e(P)   -- share of the SPECTRUM
    Both are 1 for a chain, and small when Q(P) is much bigger than L*'s chain.
    """
    if br.Lstar is None:
        return None
    keys = lstar_interval_levels(br.n, br.Lstar)
    idxs = [lat.index[k] for k in keys]
    isl = set(rec.levels)
    assert all(i in isl for i in idxs), "an L*-interval partition was not a level"
    mass = sum(rec.mult[i] for i in idxs)
    return (Fraction(len(idxs), rec.nlev), Fraction(mass, rec.e), len(idxs))


# --------------------------------------------------------------------------
# named families, extended past the exhaustive range
# --------------------------------------------------------------------------

def chain_sum_family(a, b):
    """C_a disjoint-union C_b -- two incomparable chains."""
    rel = [(i, i + 1) for i in range(a - 1)]
    rel += [(a + j, a + j + 1) for j in range(b - 1)]
    return Poset(a + b, rel)


def one_plus_two(n):
    """The tight 3-element poset 1+2 (a 2-chain and an isolated point) sitting at
    the bottom of a chain of the remaining n-3 elements: an ordinal sum, so
    delta = 1/3 for every n >= 3, and NOT primitive for n > 3."""
    rel = [(0, 1)]
    prev = None
    for k in range(3, n):
        rel += [(0, k), (1, k), (2, k)]
        if prev is not None:
            rel.append((prev, k))
        prev = k
    return Poset(n, rel)


def fence(n):
    """The zigzag / fence on n elements: 0 < 1 > 2 < 3 > ... (a primitive poset)."""
    rel = []
    for i in range(n - 1):
        rel.append((i, i + 1) if i % 2 == 0 else (i + 1, i))
    return Poset(n, rel)
