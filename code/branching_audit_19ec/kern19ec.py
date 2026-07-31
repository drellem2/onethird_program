"""kern19ec -- mg-19ec's own kernel.  Imports nothing from any other
instrument in this repository.

Everything the audit measures is built here from definitions, and every
structure that has two possible constructions is built from the one that does
NOT presuppose the thing being tested:

  * meets and joins are computed as greatest lower bounds and least upper
    bounds IN THE ORDER, by search, on BOTH sides of every comparison.  The
    left side is not allowed to use "intersection of ideals" and the right side
    is not allowed to use "componentwise min of partitions", because those are
    the identifications under test.

  * two lattices are compared by an explicit isomorphism search on the ORDER
    RELATION.  Join-irreducibles are never used to decide whether two lattices
    are isomorphic.  That is what makes the converse of X1 measurable WITHOUT
    Birkhoff, and losing it is the thing mg-19ec was told to protect.

  * `canon` is the plain minimum over all n! relabellings.  mg-5800 recorded a
    control firing on a cheaper canonical form that still reproduced A000112
    exactly, so a counting sequence is not accepted here as a control on a
    canonical form.

A poset is `(n, less)` with `less` a frozenset of ordered pairs `(i, j)`
meaning `i < j` strictly.  It is required to be transitively closed and
irreflexive; `check_poset` enforces both.
"""

import itertools

# --------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------


def poset(n, less):
    return (n, frozenset(less))


def check_poset(P):
    n, less = P
    for (i, j) in less:
        if i == j or not (0 <= i < n and 0 <= j < n):
            return False
        if (j, i) in less:
            return False
    for (i, j) in less:
        for (k, l) in less:
            if j == k and (i, l) not in less:
                return False
    return True


def from_relations(n, pairs):
    """Transitive closure of `pairs` read as strict relations."""
    less = set(pairs)
    changed = True
    while changed:
        changed = False
        for (i, j) in list(less):
            for (k, l) in list(less):
                if j == k and (i, l) not in less:
                    less.add((i, l))
                    changed = True
    return poset(n, less)


def relabel(P, perm):
    n, less = P
    return poset(n, {(perm[i], perm[j]) for (i, j) in less})


def key(P):
    n, less = P
    return (n, tuple(sorted(less)))


def canon(P):
    """Plain minimum over all n! relabellings.  No refinement, no ordering
    heuristic.  Exponential and correct."""
    n, _ = P
    best = None
    for perm in itertools.permutations(range(n)):
        k = key(relabel(P, perm))
        if best is None or k < best:
            best = k
    return best


def down_set(P, x):
    n, less = P
    return frozenset([x] + [i for i in range(n) if (i, x) in less])


def up_set(P, x):
    n, less = P
    return frozenset([x] + [j for j in range(n) if (x, j) in less])


_COVERS = {}


def covers(P):
    """Cover pairs of P."""
    if P in _COVERS:
        return _COVERS[P]
    n, less = P
    out = set()
    for (i, j) in less:
        if not any((i, k) in less and (k, j) in less for k in range(n)):
            out.add((i, j))
    _COVERS[P] = out
    return out


def height(P):
    """Number of elements of a longest chain, minus one."""
    n, less = P
    best = {}

    def h(x):
        if x in best:
            return best[x]
        r = 0
        for i in range(n):
            if (i, x) in less:
                r = max(r, h(i) + 1)
        best[x] = r
        return r

    return max([h(x) for x in range(n)] + [0])


def ideals(P):
    """Order ideals (down-sets) of P, as frozensets."""
    n, less = P
    out = []
    for mask in range(1 << n):
        S = frozenset(i for i in range(n) if mask >> i & 1)
        if all(all(j in S for j in range(n) if (j, i) in less) for i in S):
            out.append(S)
    return out


def poset_of_sets(sets):
    """Poset on a list of sets, ordered by strict inclusion."""
    m = len(sets)
    less = set()
    for a in range(m):
        for b in range(m):
            if a != b and sets[a] < sets[b]:
                less.add((a, b))
    return poset(m, less)


# --------------------------------------------------------------------------
# lattice operations, computed FROM THE ORDER by search
# --------------------------------------------------------------------------


def leq(P, a, b):
    return a == b or (a, b) in P[1]


def _masks(P):
    """(down-set mask, up-set mask) per element.  Cached on the poset."""
    if P in _MASKS:
        return _MASKS[P]
    n, less = P
    dn = [1 << i for i in range(n)]
    up = [1 << i for i in range(n)]
    for (i, j) in less:
        dn[j] |= 1 << i
        up[i] |= 1 << j
    _MASKS[P] = (dn, up, {m: i for i, m in enumerate(dn)},
                 {m: i for i, m in enumerate(up)})
    return _MASKS[P]


_MASKS = {}


def glb(P, a, b):
    """Greatest lower bound, or None.

    In any poset the meet of a and b, when it exists, is the unique element
    whose DOWN-SET is exactly the intersection of their down-sets: it lies in
    that intersection, and every element of the intersection lies below it.
    So the search over the order is a lookup, and it is still a search over the
    order -- nothing here knows what an ideal or a partition is."""
    dn, _, dnix, _ = _masks(P)
    return dnix.get(dn[a] & dn[b])


def lub(P, a, b):
    _, up, _, upix = _masks(P)
    return upix.get(up[a] & up[b])


def is_lattice(P):
    n, _ = P
    if n == 0:
        return False
    for a in range(n):
        for b in range(a, n):
            if glb(P, a, b) is None or lub(P, a, b) is None:
                return False
    return True


def meet_table(P):
    n, _ = P
    return [[glb(P, a, b) for b in range(n)] for a in range(n)]


def join_table(P):
    n, _ = P
    return [[lub(P, a, b) for b in range(n)] for a in range(n)]


def is_distributive(P):
    """a & (b | c) == (a & b) | (a & c) for every triple.  Requires a lattice."""
    n, _ = P
    if not is_lattice(P):
        return False
    M, J = meet_table(P), join_table(P)
    for a in range(n):
        Ma = M[a]
        for b in range(n):
            Mab = Ma[b]
            for c in range(n):
                if Ma[J[b][c]] != J[Mab][Ma[c]]:
                    return False
    return True


def join_irreducibles(P):
    """Elements with exactly one lower cover.  Used only for REPORTING which
    P arise; never for deciding lattice isomorphism."""
    n, _ = P
    cov = covers(P)
    return [x for x in range(n) if len([1 for (i, j) in cov if j == x]) == 1]


def induced(P, elts):
    n, less = P
    idx = {x: i for i, x in enumerate(sorted(elts))}
    return poset(len(idx), {(idx[i], idx[j]) for (i, j) in less
                            if i in idx and j in idx})


# --------------------------------------------------------------------------
# poset isomorphism by backtracking on the ORDER (no Birkhoff)
# --------------------------------------------------------------------------


def _invariant(P, x):
    n, less = P
    return (len(down_set(P, x)), len(up_set(P, x)),
            len([1 for (i, j) in covers(P) if j == x]),
            len([1 for (i, j) in covers(P) if i == x]))


def iso(P, Q):
    """True iff P and Q are isomorphic as posets.  Backtracking on the strict
    order relation, pruned by a degree/ideal-size invariant.  Nothing here
    knows what a join-irreducible is."""
    if P[0] != Q[0]:
        return False
    n = P[0]
    if n == 0:
        return True
    if len(P[1]) != len(Q[1]):
        return False
    invP = [_invariant(P, x) for x in range(n)]
    invQ = [_invariant(Q, y) for y in range(n)]
    if sorted(invP) != sorted(invQ):
        return False
    order = sorted(range(n), key=lambda x: -len(down_set(P, x)))
    used = [False] * n
    phi = {}

    def bt(k):
        if k == n:
            return True
        x = order[k]
        for y in range(n):
            if used[y] or invQ[y] != invP[x]:
                continue
            ok = True
            for x2, y2 in phi.items():
                if ((x2, x) in P[1]) != ((y2, y) in Q[1]):
                    ok = False
                    break
                if ((x, x2) in P[1]) != ((y, y2) in Q[1]):
                    ok = False
                    break
            if ok:
                used[y] = True
                phi[x] = y
                if bt(k + 1):
                    return True
                del phi[x]
                used[y] = False
        return False

    return bt(0)


# --------------------------------------------------------------------------
# partitions, Young's lattice, skew shapes
# --------------------------------------------------------------------------


def partitions(n):
    """Partitions of n as weakly decreasing tuples."""
    if n == 0:
        return [()]
    out = []

    def rec(rest, cap, acc):
        if rest == 0:
            out.append(tuple(acc))
            return
        for p in range(min(rest, cap), 0, -1):
            rec(rest - p, p, acc + [p])

    rec(n, n, [])
    return out


def partitions_upto(n):
    out = []
    for k in range(n + 1):
        out.extend(partitions(k))
    return out


def trim(lam):
    """Drop trailing zero rows.  A partition and the same partition padded
    with empty rows are the same Young diagram, and `skew_shapes` emits padded
    ones -- treating them as different silently deleted the bottom element of
    every interval whose mu ended in a zero."""
    lam = tuple(lam)
    while lam and lam[-1] == 0:
        lam = lam[:-1]
    return lam


def contains(lam, mu):
    """mu is contained in lam, as Young diagrams."""
    lam, mu = trim(lam), trim(mu)
    if len(mu) > len(lam):
        return False
    return all(mu[i] <= lam[i] for i in range(len(mu)))


def young_interval(mu, lam):
    """The set {nu : mu <= nu <= lam} and its containment order.

    Built from PARTITIONS and containment only.  No cell poset, no order
    ideal, no join-irreducible."""
    assert contains(lam, mu)
    lam, mu = trim(lam), trim(mu)
    elts = []
    for k in range(sum(mu), sum(lam) + 1):
        for nu in partitions(k):
            if contains(lam, nu) and contains(nu, mu):
                elts.append(nu)
    idx = {nu: i for i, nu in enumerate(elts)}
    less = set()
    for a in elts:
        for b in elts:
            if a != b and contains(b, a):
                less.add((idx[a], idx[b]))
    return elts, poset(len(elts), less)


def skew_cells(lam, mu):
    """Cells of lam/mu as (row, col) pairs, 0-indexed."""
    mu = tuple(mu) + (0,) * (len(lam) - len(mu))
    return [(i, j) for i in range(len(lam)) for j in range(mu[i], lam[i])]


def cell_poset(cells):
    """(i,j) <= (i',j') iff i <= i' and j <= j'."""
    cells = sorted(cells)
    idx = {c: i for i, c in enumerate(cells)}
    less = set()
    for a in cells:
        for b in cells:
            if a != b and a[0] <= b[0] and a[1] <= b[1]:
                less.add((idx[a], idx[b]))
    return poset(len(cells), less)


def shape_of_ideal(cells, S):
    """The partition filled by the cells in the ideal S (indices into the
    sorted cell list), added to mu.  Returned as row counts."""
    cells = sorted(cells)
    rows = {}
    for i in S:
        r, c = cells[i]
        rows[r] = max(rows.get(r, -1), c)
    return rows


def skew_shapes(k, box=None):
    """Every skew shape lam/mu with exactly k cells and no empty row, up to
    a shift of the columns.

    A skew shape with no empty row is a list of rows, row i occupying columns
    [mu_i, lam_i) with lam_i = mu_i + l_i and l_i >= 1.  Being a skew shape of
    two PARTITIONS is exactly: mu weakly decreasing and lam weakly decreasing.
    The cell poset is unchanged by subtracting a constant from every mu_i and
    lam_i, so the smallest start is normalised to 0.  `box` bounds the largest
    start; growing it is the control that the search was wide enough.

    Yielded as (lam, mu) with lam, mu weakly decreasing tuples."""
    if box is None:
        box = k
    for rows in range(1, k + 1):
        for lens in itertools.product(range(1, k + 1), repeat=rows):
            if sum(lens) != k:
                continue
            for starts in itertools.product(range(box + 1), repeat=rows):
                if any(starts[i] < starts[i + 1] for i in range(rows - 1)):
                    continue
                if min(starts) != 0:
                    continue
                lam = tuple(starts[i] + lens[i] for i in range(rows))
                if any(lam[i] < lam[i + 1] for i in range(rows - 1)):
                    continue
                yield lam, starts


def skew_shape_classes(k, box=None):
    """Canonical forms of every cell poset of a skew shape with exactly k
    cells.  Key -> one witnessing (lam, mu)."""
    if k == 0:
        return {(0, ()): ((), ())}
    seen = {}
    for lam, mu in skew_shapes(k, box):
        c = canon(cell_poset(skew_cells(lam, mu)))
        if c not in seen:
            seen[c] = (lam, mu)
    return seen


# --------------------------------------------------------------------------
# Young-Fibonacci
# --------------------------------------------------------------------------


def yf_up_covers(w):
    """Up-covers of a Fibonacci word w (a tuple of 1s and 2s).

    a = number of leading 2s, rest = w[a:].
      * insert a 1 anywhere inside the leading 2-block: 2^b 1 2^(a-b) rest
      * if rest starts with a 1, promote it: 2^(a+1) rest[1:]
    """
    a = 0
    while a < len(w) and w[a] == 2:
        a += 1
    rest = w[a:]
    out = set()
    for b in range(a + 1):
        out.add((2,) * b + (1,) + (2,) * (a - b) + rest)
    if rest and rest[0] == 1:
        out.add((2,) * (a + 1) + rest[1:])
    return out


def yf_words(max_rank):
    """All Fibonacci words of rank <= max_rank, by rank."""
    ranks = [[()]]
    for r in range(1, max_rank + 1):
        cur = set()
        for w in ranks[r - 1]:
            for v in yf_up_covers(w):
                if sum(v) == r:
                    cur.add(v)
        ranks.append(sorted(cur))
    return ranks


def yf_poset(max_rank):
    """The Young-Fibonacci order truncated at max_rank: elements, and the
    strict order got by transitive closure of the cover graph."""
    ranks = yf_words(max_rank)
    elts = [w for r in ranks for w in r]
    idx = {w: i for i, w in enumerate(elts)}
    edges = set()
    for w in elts:
        for v in yf_up_covers(w):
            if v in idx:
                edges.add((idx[w], idx[v]))
    return elts, from_relations(len(elts), edges)


def yf_down_covers(w):
    """Down-covers, derived by inverting the up-cover rule over the words of
    rank(w)-1.  Kept separate so the two can be checked against each other."""
    r = sum(w)
    if r == 0:
        return set()
    below = yf_words(r)[r - 1]
    return {u for u in below if w in yf_up_covers(u)}
