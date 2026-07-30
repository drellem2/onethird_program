"""kern6f61 -- the repair kernel for mg-6f61.

Independent of code/species_7d75/ (kern7d75.py, hopf7d75.py) and of
code/species_audit_a61f/ (kerna61f.py).  Nothing is imported from either.
Where an object is also built there, it is built here by a THIRD route, so
that agreement is evidence rather than a shared bug:

  * a poset on a ground set is a TUPLE OF INT BITMASKS, up[i] = the set of j
    with i < j.  7d75 and a61f both carry posets as frozensets of ordered
    pairs.
  * posets are enumerated as the FIXED POINTS OF THE TRANSITIVE CLOSURE:
    every subset of the ordered pairs is closed by Warshall and kept only if
    the closure returns the subset unchanged and is irreflexive.  7d75
    iterates subsets with an incremental closure; a61f makes a three-way
    choice per unordered pair and then tests transitivity.
  * a face is a tuple of int bitmasks, enumerated as a BLOCK-INDEX FUNCTION
    f : ground -> {0,1,...} whose image is an initial segment.  Both
    predecessors build set compositions by recursive block choice.  The
    face condition is then literally "f is weakly increasing along <".

Conventions:

  ground       an int bitmask over range(N).
  poset        tuple of N ints; up[i] has bit j set iff i < j.  Strict,
               transitively closed, irreflexive, antisymmetric, and
               supported inside its ground set.
  face         tuple of nonzero disjoint int masks covering the ground set,
               in block order.  A face of P is one whose block-index map is
               weakly increasing along every relation of P.
  partition    frozenset of nonzero disjoint int masks covering the ground.
  AC(P)        { supp(F) : F a face of P }, equivalently the partitions
               whose quotient digraph is acyclic.

Nothing here makes a claim.  The claims are in r1_smallest.py, r2_columns.py
and r3_quotes.py.
"""

from itertools import combinations, product as _iproduct

# ---------------------------------------------------------------------------
# bitmask helpers
# ---------------------------------------------------------------------------


def bits(m):
    """The elements of the mask m, ascending."""
    out = []
    i = 0
    while m:
        if m & 1:
            out.append(i)
        m >>= 1
        i += 1
    return out


def popcount(m):
    c = 0
    while m:
        m &= m - 1
        c += 1
    return c


def submasks(m):
    """Every submask of m, including 0 and m."""
    out = [0]
    for e in bits(m):
        out += [s | (1 << e) for s in out]
    return sorted(set(out))


# ---------------------------------------------------------------------------
# posets as tuples of up-masks
# ---------------------------------------------------------------------------


def _closure(up, n):
    """Warshall transitive closure of the relation given by up-masks."""
    up = list(up)
    for k in range(n):
        bk = 1 << k
        for i in range(n):
            if up[i] & bk:
                up[i] |= up[k]
    return tuple(up)


def _irreflexive(up, n):
    return all(not (up[i] >> i) & 1 for i in range(n))


def posets_on(ground, n):
    """Every partial order supported on `ground`, as the FIXED POINTS of the
    transitive closure.  Returns a sorted list of up-mask tuples of length n.
    """
    els = bits(ground)
    pairs = [(a, b) for a in els for b in els if a != b]
    out = []
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            up = [0] * n
            for (a, b) in sub:
                up[a] |= 1 << b
            up = tuple(up)
            cl = _closure(up, n)
            if cl == up and _irreflexive(up, n):
                out.append(up)
    return sorted(set(out))


def restrict_poset(up, mask, n):
    return tuple((up[i] & mask) if (mask >> i) & 1 else 0 for i in range(n))


def is_lower_set(up, S, n):
    """S is a lower set of the poset: nothing outside S is below anything in
    S."""
    for i in range(n):
        if not (S >> i) & 1:
            if up[i] & S:
                return False
    return True


def is_antichain(up, S, n):
    return all(not (up[i] & S) for i in bits(S))


def union_poset(a, b, n):
    return tuple(a[i] | b[i] for i in range(n))


def aut_group(up, ground, n):
    """The automorphisms of the poset, as tuples giving the image of each
    element of `ground`."""
    els = bits(ground)
    out = []
    for perm in _perms(els):
        f = dict(zip(els, perm))
        ok = True
        for i in els:
            for j in bits(up[i]):
                if not (up[f[i]] >> f[j]) & 1:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(tuple(perm))
    return out


def _perms(seq):
    from itertools import permutations
    return list(permutations(seq))


def relabel(up, perm, els, n):
    """perm maps els[k] -> perm[k]."""
    f = dict(zip(els, perm))
    out = [0] * n
    for i in els:
        for j in bits(up[i]):
            out[f[i]] |= 1 << f[j]
    return tuple(out)


def canonical(up, ground, n):
    els = bits(ground)
    return min(relabel(up, p, els, n) for p in _perms(els))


# ---------------------------------------------------------------------------
# faces, via block-index functions
# ---------------------------------------------------------------------------


def compositions_on(ground):
    """Every set composition of `ground`, as a tuple of block masks.

    Enumerated as block-index functions whose image is an initial segment.
    """
    els = bits(ground)
    k = len(els)
    if k == 0:
        return [()]
    out = []
    for f in _iproduct(range(k), repeat=k):
        m = max(f) + 1
        if set(f) != set(range(m)):
            continue
        blocks = [0] * m
        for e, t in zip(els, f):
            blocks[t] |= 1 << e
        out.append(tuple(blocks))
    return sorted(set(out))


def faces_on(up, ground):
    """The faces of the braid arrangement lying in the cone C(P)."""
    out = []
    for F in compositions_on(ground):
        idx = {}
        for t, B in enumerate(F):
            for e in bits(B):
                idx[e] = t
        ok = True
        for i in bits(ground):
            for j in bits(up[i]):
                if idx[i] > idx[j]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(F)
    return out


def supp(F):
    return frozenset(F)


def concat(F, G):
    return tuple(F) + tuple(G)


def restrict_face(F, S):
    return tuple(B & S for B in F if B & S)


def restrict_part(X, S):
    return frozenset(B & S for B in X if B & S)


def part_union(X, Y):
    return frozenset(X) | frozenset(Y)


def quotient_acyclic(up, X, ground):
    """Kahn's algorithm on the quotient digraph -- a different route from the
    DFS colouring in 7d75 and from a61f's."""
    blocks = sorted(X)
    where = {}
    for t, B in enumerate(blocks):
        for e in bits(B):
            where[e] = t
    m = len(blocks)
    succ = [set() for _ in range(m)]
    indeg = [0] * m
    for i in bits(ground):
        for j in bits(up[i]):
            a, b = where[i], where[j]
            if a != b and b not in succ[a]:
                succ[a].add(b)
                indeg[b] += 1
    q = [v for v in range(m) if indeg[v] == 0]
    seen = 0
    while q:
        v = q.pop()
        seen += 1
        for w in succ[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                q.append(w)
    return seen == m


def partitions_on(ground):
    return sorted({supp(F) for F in compositions_on(ground)}, key=_pkey)


def _pkey(X):
    return (len(X), sorted(X))


def AC_by_support(up, ground):
    return {supp(F) for F in faces_on(up, ground)}


def AC_by_acyclicity(up, ground):
    return {X for X in partitions_on(ground) if quotient_acyclic(up, X, ground)}


# ---------------------------------------------------------------------------
# the bimonoid battery, generic in the collection AND in the operations
# ---------------------------------------------------------------------------

COLUMNS = ("prod_closure", "coprod_closure", "assoc", "coassoc", "compat")


def decompositions(I):
    """Every ordered pair (S, T) with S disjoint-union T = I."""
    return [(S, I & ~S) for S in submasks(I)]


def axioms(universe, mu, de, ground):
    """Failure counts in each of the five columns.

    `universe` maps a ground-set mask to the set of basis elements on it.
    `mu(x, y)` is the product; `de(x, S, T)` the coproduct component, or None
    where the coproduct is zero.  No assumption is made about either.
    """
    f = dict.fromkeys(COLUMNS, 0)
    f["pairs_tested"] = 0
    for I, els in universe.items():
        for (S, T) in decompositions(I):
            for x in universe[S]:
                for y in universe[T]:
                    f["pairs_tested"] += 1
                    if mu(x, y) not in els:
                        f["prod_closure"] += 1
            for x in els:
                d = de(x, S, T)
                if d is None:
                    continue
                if d[0] not in universe[S] or d[1] not in universe[T]:
                    f["coprod_closure"] += 1
    I = ground
    for (S, R) in decompositions(I):
        for (S1, S2) in decompositions(S):
            for x in universe[S1]:
                for y in universe[S2]:
                    for z in universe[R]:
                        if mu(mu(x, y), z) != mu(x, mu(y, z)):
                            f["assoc"] += 1
    for (A, rest) in decompositions(I):
        for (B, C) in decompositions(rest):
            for x in universe[I]:
                d1 = de(x, A, B | C)
                lo = None if d1 is None else de(d1[1], B, C)
                d2 = de(x, A | B, C)
                ro = None if d2 is None else de(d2[0], A, B)
                lv = None if lo is None else (d1[0], lo[0], lo[1])
                rv = None if ro is None else (ro[0], ro[1], d2[1])
                if lv != rv:
                    f["coassoc"] += 1
    for (S1, T1) in decompositions(I):
        for (S2, T2) in decompositions(I):
            A, B = S1 & S2, S1 & T2
            C, D = T1 & S2, T1 & T2
            for x in universe[S1]:
                for y in universe[T1]:
                    lhs = de(mu(x, y), S2, T2)
                    dx = de(x, A, B)
                    dy = de(y, C, D)
                    if dx is None or dy is None:
                        rhs = None
                    else:
                        rhs = (mu(dx[0], dy[0]), mu(dx[1], dy[1]))
                    if lhs != rhs:
                        f["compat"] += 1
    return f
