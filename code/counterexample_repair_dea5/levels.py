"""Commitment levels, their multiplicities, and the two quotient statistics.

A LEVEL of P is a partition X of the ground set whose quotient digraph is
acyclic (equivalently, some ordering of its blocks is a P-compatible move).
Multiplicities are defined, as in the target document, by

    sum over levels Y refining X of m_Y  =  prod over blocks B of X of e(P|_B).     (*)

THE ROUTE HERE IS NOT THE TARGET'S.  Both prior instruments build the whole
level lattice, sort it by refinement, and invert (*) by downward recursion over
that lattice.  This one uses a factorisation instead, which is what makes n = 8
reachable:

  LEMMA (multiplicativity).  For every level Y of P,
      m_Y  =  product over blocks B of Y of  M(P|_B),      where  M(R) := m_{top(R)}
  with top(R) the one-block partition of R.

  Proof.  Fix a level Y with blocks B_1..B_k.  If Z refines Y then any directed
  cycle of P/Z projects to a directed cycle or a loop of P/Y; P/Y is acyclic, so
  every cycle of P/Z stays inside one block B_i.  The relations of P inside B_i
  are exactly those of P|_{B_i}, so Z is a level of P iff each Z|_{B_i} is a
  level of P|_{B_i}:  the levels refining Y are the product of the level sets of
  the B_i.  Now put g(Z) = prod_i m^{P|_{B_i}}_{Z|_{B_i}} for Z refining Y.  Then
  sum_{Z refines Y'} g(Z) = prod_i prod over blocks of Y'|_{B_i} of e(P|_block)
  for every Y' refining Y, which is the right-hand side of (*) at Y'.  So g and m
  satisfy the same triangular system on the interval below Y, and (*) determines
  m uniquely by induction on refinement, whence g = m there; at Z = Y this is the
  claim.  QED

  Two corollaries used below.  M(single point) = 1, and M(R) = 0 whenever R is a
  chain with at least 2 elements (for a chain e(R) = 1 and the finest partition
  already contributes 1) -- so the target's supporting fact "every all-chain
  level other than the finest has m = 0" is structural here, not a measurement.

  Consequence for the enumeration: only partitions all of whose blocks have
  M != 0 can carry positive multiplicity, and that prunes the recursion for
  M(R) = e(R) - sum over non-top levels Y of prod_B M(P|_B) very hard.

  And because every m_X is a multiplicity, hence >= 0, qmass = 1 holds iff EVERY
  level with positive multiplicity is an interval partition of L*.  That is the
  exact combinatorial content of the statistic, and section 4 of the repair uses
  it.

The two statistics of the target's section 4, for a poset with a majority linear
order L*:

    qfrac = 2^(n-1) / |Q(P)|                          share of the LEVELS
    qmass = (sum of m_X over L*-interval levels) / e(P)  share of the SPECTRUM

qmass is computed from the lemma by a composition DP along L*: with A(0) = 1 and
A(j) = sum_{i<j} A(i) * M(P|_{L*[i..j)}), the numerator is A(n).
"""

from fractions import Fraction

from poset import Poset, induced, canonical, e_all_subsets, find_cycle, _bits


# --------------------------------------------------------------------------
# levels
# --------------------------------------------------------------------------

def block_digraph(P, blocks):
    k = len(blocks)
    adj = [0] * k
    for a in range(k):
        reach = 0
        for v in _bits(blocks[a]):
            reach |= P.up[v]
        for b in range(k):
            if b != a and reach & blocks[b]:
                adj[a] |= 1 << b
    return adj


def is_level(P, blocks):
    return find_cycle(len(blocks), block_digraph(P, blocks)) is None


def all_partitions(mask):
    """Every partition of `mask` into blocks, as tuples of bitmasks."""
    if mask == 0:
        yield ()
        return
    low = mask & -mask
    rest = mask ^ low
    subs = _subsets(rest)
    for extra in subs:
        block = low | extra
        for tail in all_partitions(mask ^ block):
            yield (block,) + tail


def _subsets(mask):
    out = [0]
    r = mask
    while r:
        b = r & -r
        r ^= b
        out += [s | b for s in out]
    return out


def all_levels(P, mask=None):
    """Every level of P|_mask (as a partition of `mask`)."""
    if mask is None:
        mask = (1 << P.n) - 1
    return [X for X in all_partitions(mask) if is_level(P, X)]


def is_convex(P, B):
    """No element outside B lies strictly between two elements of B."""
    for a in _bits(B):
        ua = P.up[a]
        for b in _bits(B):
            if ua & P.down[b] & ~B:
                return False
    return True


def convex_partitions(P, mask):
    """Partitions of `mask` all of whose blocks are convex in P.

    Every block of a level is convex: if z is outside B with a < z < b for
    a, b in B then the quotient carries B -> {z} and {z} -> B, a 2-cycle.  So
    restricting the enumeration to convex blocks drops no level, and controls.py
    checks the pruned and unpruned level counts agree at n <= 6.
    """
    ok = {}

    def rec(m):
        if m == 0:
            yield ()
            return
        low = m & -m
        rest = m ^ low
        for extra in _subsets(rest):
            block = low | extra
            good = ok.get(block)
            if good is None:
                good = is_convex(P, block)
                ok[block] = good
            if not good:
                continue
            for tail in rec(m ^ block):
                yield (block,) + tail

    return rec(mask)


def count_levels(P, mask=None, prune=True):
    if mask is None:
        mask = (1 << P.n) - 1
    src = convex_partitions(P, mask) if prune else all_partitions(mask)
    return sum(1 for X in src if is_level(P, X))


# --------------------------------------------------------------------------
# multiplicities
# --------------------------------------------------------------------------

def m_table(P, cache=None, e=None):
    """M(P|_S) for every subset S, using the lemma above.

    `cache` maps a canonical form to its M value and may be shared across
    posets -- M depends only on the isomorphism class of the induced subposet.
    """
    if cache is None:
        cache = {}
    if e is None:
        e = e_all_subsets(P)
    n = P.n
    Mm = [0] * (1 << n)
    Mm[0] = 1                              # empty product convention
    order = sorted(range(1, 1 << n), key=lambda S: bin(S).count("1"))
    for S in order:
        key = canonical(induced(P, S))
        hit = cache.get(key)
        if hit is not None:
            Mm[S] = hit
            continue
        if bin(S).count("1") == 1:
            val = 1
        else:
            val = e[S] - _nontop_mass(P, S, Mm)
        cache[key] = val
        Mm[S] = val
    return Mm, cache


def _nontop_mass(P, S, Mm):
    """sum of prod_B M(B) over levels of P|_S with at least two blocks."""
    total = 0
    for blocks in _pruned_partitions(P, S, Mm):
        if len(blocks) < 2:
            continue
        if not is_level(P, blocks):
            continue
        prod = 1
        for B in blocks:
            prod *= Mm[B]
        total += prod
    return total


def _pruned_partitions(P, mask, Mm):
    """Partitions of `mask` all of whose blocks have M != 0."""
    if mask == 0:
        yield ()
        return
    low = mask & -mask
    rest = mask ^ low
    for extra in _subsets(rest):
        block = low | extra
        if Mm[block] == 0:
            continue
        for tail in _pruned_partitions(P, mask ^ block, Mm):
            yield (block,) + tail


def positive_levels(P, Mm):
    """(blocks, m) for every level of P with m > 0."""
    full = (1 << P.n) - 1
    out = []
    for blocks in _pruned_partitions(P, full, Mm):
        if not is_level(P, blocks):
            continue
        prod = 1
        for B in blocks:
            prod *= Mm[B]
        if prod:
            out.append((blocks, prod))
    return out


def m_by_inversion(P):
    """m_X for every level, by inverting (*) directly over the level lattice.

    The target's route, kept here only as a control on the lemma.
    """
    e = e_all_subsets(P)
    levels = all_levels(P)
    levels = sorted(levels, key=lambda X: (len(X), sorted(X)), reverse=True)
    # refinement order: X refines Y iff every block of X sits inside a block of Y
    def refines(X, Y):
        return all(any(B & C == B for C in Y) for B in X)
    m = {}
    for X in sorted(levels, key=lambda X: -len(X)):     # finest first
        f = 1
        for B in X:
            f *= e[B]
        s = 0
        for Y, mv in m.items():
            if Y != X and refines(Y, X):
                s += mv
        m[X] = f - s
    return m


# --------------------------------------------------------------------------
# the two statistics
# --------------------------------------------------------------------------

def interval_masks(order):
    """{(i,j): mask of order[i:j]} for 0 <= i < j <= n."""
    n = len(order)
    out = {}
    for i in range(n):
        mask = 0
        for j in range(i, n):
            mask |= 1 << order[j]
            out[(i, j + 1)] = mask
    return out


def qmass(P, order, Mm, e_full):
    """(sum of m over L*-interval levels) / e(P), exactly."""
    n = len(order)
    iv = interval_masks(order)
    A = [0] * (n + 1)
    A[0] = 1
    for j in range(1, n + 1):
        tot = 0
        for i in range(j):
            if A[i]:
                tot += A[i] * Mm[iv[(i, j)]]
        A[j] = tot
    return Fraction(A[n], e_full)


def qfrac(P, order):
    return Fraction(1 << (P.n - 1), count_levels(P))


def interval_partitions_are_levels(P, order):
    """All 2^(n-1) interval partitions of L* are levels -- asserted, not assumed."""
    n = len(order)
    iv = interval_masks(order)
    for cut in range(1 << (n - 1)):
        blocks = []
        start = 0
        for k in range(n - 1):
            if cut >> k & 1:
                blocks.append(iv[(start, k + 1)])
                start = k + 1
        blocks.append(iv[(start, n)])
        if not is_level(P, tuple(blocks)):
            return False
    return True
