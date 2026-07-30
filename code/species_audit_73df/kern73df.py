"""kern73df -- the independent kernel for the mg-73df audit.

WHAT THIS IS.  A from-scratch rebuild of every object the audited documents
measure: posets on a finite set, the faces of a poset's braid cone, the
support map, set compositions, the Hopf-monoid operations of Aguiar-Mahajan
13.1.1 / 13.4.2 / 8.13 on the Hadamard products P x Sigma and P x Pi, the
S_n-invariant subalgebra of the face algebra, and Solomon's descent algebra.

WHAT IT SHARES WITH THE THINGS IT AUDITS.  Nothing.  It imports nothing from
`code/species_7d75`, `code/species_repair_6f61`, `code/species_audit_a61f` or
`code/species_remainder_f8fa`, and no routine here was copied from any of
them.  Blocks are integer bitmasks in all four, which is the obvious
representation for subsets of a small ground set and is not a shared routine;
the enumerations differ:

  * posets are enumerated here by EXTENDING a strict order one comparable
    pair at a time and rejecting anything that is not already transitive,
    not as fixed points of a Warshall closure (6f61) and not from a
    cover-relation generator (7d75);
  * faces are enumerated here from ORDERED SET PARTITIONS built by an
    explicit block-by-block recursion and then filtered against the cone,
    not from block-index functions;
  * acyclicity of a quotient is decided here by a depth-first cycle search
    on the quotient digraph, not by Kahn's algorithm.

The self-test anchors the counts to OEIS A001035 (labelled posets), A000670
(ordered set partitions), A000110 (Bell), A000112 (unlabelled posets),
A000041 (partitions) and A000142 (factorials).  If any of those disagree the
whole audit is void, which is the point of anchoring them.
"""

from functools import lru_cache
from itertools import combinations, permutations

# ---------------------------------------------------------------------------
# subsets, as bitmasks
# ---------------------------------------------------------------------------


def bits(m):
    """The elements of a mask, ascending."""
    out = []
    i = 0
    while m:
        if m & 1:
            out.append(i)
        m >>= 1
        i += 1
    return out


def submasks(m):
    """Every submask of m, including 0 and m itself."""
    out = [0]
    for i in bits(m):
        out += [s | (1 << i) for s in out]
    return sorted(set(out))


def popcount(m):
    return bin(m).count("1")


# ---------------------------------------------------------------------------
# posets.  A poset on the mask `g` is a STRICT order, stored as a tuple of
# n masks: down[j] is the set of elements strictly below j.
# ---------------------------------------------------------------------------


def _is_transitive(down, n):
    for j in range(n):
        for i in bits(down[j]):
            if down[i] & ~down[j]:
                return False
    return True


@lru_cache(maxsize=None)
def posets_on(g, n):
    """Every strict partial order on the ground set `g`, as tuples of n masks.

    Built by extending: run over the comparable pairs in a fixed order and
    either add the pair or not, keeping only the assignments that are already
    transitive and antisymmetric.  Deliberately not a closure algorithm --
    a closure would silently repair a non-transitive candidate, and the point
    of enumerating this way is that nothing is repaired.
    """
    el = bits(g)
    pairs = [(a, b) for a in el for b in el if a != b]
    out = []

    def rec(k, down):
        if k == len(pairs):
            if _is_transitive(down, n):
                out.append(tuple(down))
            return
        a, b = pairs[k]
        rec(k + 1, down)
        if not (down[a] >> b) & 1:            # antisymmetry
            nd = list(down)
            nd[b] |= 1 << a
            rec(k + 1, nd)

    rec(0, [0] * n)
    return tuple(sorted(set(out)))


def poset_restrict(down, s, n):
    return tuple((down[j] & s) if (s >> j) & 1 else 0 for j in range(n))


def poset_disjoint_union(d1, d2, n):
    return tuple(d1[j] | d2[j] for j in range(n))


def poset_opposite(down, n):
    up = [0] * n
    for j in range(n):
        for i in bits(down[j]):
            up[i] |= 1 << j
    return tuple(up)


def is_lower_set(down, s, n):
    """s is a lower set (down-closed) of the order `down`."""
    for j in bits(s):
        if down[j] & ~s:
            return False
    return True


def is_upper_set(down, s, n):
    for j in bits(s):
        pass
    for j in range(n):
        if (s >> j) & 1:
            continue
        if down[j] & s:
            return False
    return True


# ---------------------------------------------------------------------------
# faces = set compositions.  A face is a tuple of non-empty disjoint masks
# whose union is the ground set.  Block order matters.
# ---------------------------------------------------------------------------


@lru_cache(maxsize=None)
def compositions_on(g):
    """Every ordered set partition of `g`, built block by block."""
    if g == 0:
        return ((),)
    out = []
    for first in submasks(g):
        if first == 0:
            continue
        for rest in compositions_on(g & ~first):
            out.append((first,) + rest)
    return tuple(out)


def block_index(face):
    """element -> index of the block containing it."""
    idx = {}
    for k, B in enumerate(face):
        for e in bits(B):
            idx[e] = k
    return idx


def in_cone(down, face, n):
    """The face lies in C(P) = {x : x_i <= x_j whenever i < j in P}."""
    idx = block_index(face)
    for j in range(n):
        if j not in idx:
            continue
        for i in bits(down[j]):
            if idx[i] > idx[j]:
                return False
    return True


def faces_on(down, g, n):
    return tuple(F for F in compositions_on(g) if in_cone(down, F, n))


def supp(face):
    """Forget the order of the blocks: a set partition, as a sorted tuple."""
    return tuple(sorted(face))


def concat(F, G):
    return F + G


def restrict_face(F, s):
    return tuple(B & s for B in F if B & s)


def restrict_part(X, s):
    return tuple(sorted(B & s for B in X if B & s))


def part_disjoint_union(X, Y):
    return tuple(sorted(X + Y))


# ---------------------------------------------------------------------------
# AC(P): the partitions of P with ACYCLIC quotient, decided by a depth-first
# cycle search on the quotient digraph.
# ---------------------------------------------------------------------------


def quotient_acyclic(down, X, n):
    """X is a tuple of blocks.  Edge B -> C when some b in B is below some
    c in C (b != c).  Acyclic?  Depth-first, colouring."""
    k = len(X)
    where = {}
    for bi, B in enumerate(X):
        for e in bits(B):
            where[e] = bi
    adj = [set() for _ in range(k)]
    for j in range(n):
        if j not in where:
            continue
        for i in bits(down[j]):
            if where[i] != where[j]:
                adj[where[i]].add(where[j])
    colour = [0] * k                      # 0 white, 1 grey, 2 black

    def dfs(v):
        colour[v] = 1
        for w in adj[v]:
            if colour[w] == 1:
                return False
            if colour[w] == 0 and not dfs(w):
                return False
        colour[v] = 2
        return True

    for v in range(k):
        if colour[v] == 0 and not dfs(v):
            return False
    return True


def AC_on(down, g, n):
    """The support semilattice, computed the SLOW honest way: every set
    partition of g, kept when its quotient digraph is acyclic."""
    out = set()
    for F in compositions_on(g):
        out.add(supp(F))
    return tuple(sorted(X for X in out if quotient_acyclic(down, X, n)))


# ---------------------------------------------------------------------------
# the Tits product of two faces on the SAME ground set
# ---------------------------------------------------------------------------


def tits(F, G):
    out = []
    for B in F:
        for C in G:
            if B & C:
                out.append(B & C)
    return tuple(out)


# ---------------------------------------------------------------------------
# the S_n-invariant subalgebra of the face algebra, and Solomon's descent
# algebra, both on [n].
# ---------------------------------------------------------------------------


def integer_compositions(n):
    """Compositions of n, as tuples."""
    if n == 0:
        return [()]
    out = []
    for k in range(1, n + 1):
        for rest in integer_compositions(n - k):
            out.append((k,) + rest)
    return out


def shape(F):
    return tuple(popcount(B) for B in F)


def orbit_sum_structure(n):
    """c^gamma_{alpha,beta} for the orbit-sum basis of (k Sigma_n)^{S_n}.

    The orbit of a face under S_n is exactly its BLOCK-SIZE COMPOSITION --
    checked, not assumed, in the self-test.

    O_a . O_b = sum over ALL pairs (F, G) of shapes (a, b) of the Tits
    product F.G, and the number of pairs landing on a given face H depends
    only on shape(H).  So the structure constant is that count at one fixed
    H per shape.  It is NOT "fix one F of shape a and sum over G": that
    counts each product once per G rather than once per target, and it gets
    the unit wrong -- O_(n) is the identity of the face algebra, so
    O_(n) . O_b must be O_b with coefficient 1, and the one-representative
    recipe returns |orbit of b| instead.  That error is what the n = 2 row
    of C3a caught before this routine was corrected.
    """
    g = (1 << n) - 1
    allF = compositions_on(g)
    by_shape = {}
    for F in allF:
        by_shape.setdefault(shape(F), []).append(F)
    comps = integer_compositions(n)
    rep = {a: by_shape[a][0] for a in comps}
    tally = {}
    for F in allF:
        sF = shape(F)
        for G in allF:
            H = tits(F, G)
            if H == rep[shape(H)]:
                k = (sF, shape(G), shape(H))
                tally[k] = tally.get(k, 0) + 1
    return comps, tally


def descent_set(w):
    """w a tuple (one-line notation).  des(w) = {i : w[i-1] > w[i]}, 1-based."""
    return frozenset(i for i in range(1, len(w)) if w[i - 1] > w[i])


def descent_structure(n, convention):
    """c^gamma_{S,T} for Solomon's basis d_T = sum_{des(w) subset T} w.

    `convention` is "A" (product of permutations as (uv)(i) = u(v(i))) or
    "B" (the other order).  Indices are subsets of {1..n-1} keyed by the
    composition they correspond to, so both algebras are indexed by the SAME
    set and the comparison of structure constants is meaningful.
    """
    perms = list(permutations(range(1, n + 1)))
    subsets = []
    for k in range(n):
        for S in combinations(range(1, n), k):
            subsets.append(frozenset(S))
    d = {}
    for S in subsets:
        d[S] = [w for w in perms if descent_set(w).issubset(S)]

    def mult(u, v):
        if convention == "A":
            return tuple(u[v[i] - 1] for i in range(n))
        return tuple(v[u[i] - 1] for i in range(n))

    # expand d_S * d_T in the permutation basis, then re-express in the d
    # basis by inclusion-exclusion over subsets (the d_S are a basis and
    # the expansion is constant on descent classes -- verified in selftest).
    by_class = {}
    for w in perms:
        by_class.setdefault(descent_set(w), []).append(w)

    c = {}
    for S in subsets:
        for T in subsets:
            acc = {}
            for u in d[S]:
                for v in d[T]:
                    w = mult(u, v)
                    acc[w] = acc.get(w, 0) + 1
            # The product is a combination of the d_U, so its coefficient in
            # the permutation basis is CONSTANT on each exact descent class.
            # Every class is read, including the ones with coefficient 0 --
            # an earlier version of this routine read only the classes that
            # appear in `acc`, which silently gave a partially-covered class
            # the multiplicity of its non-zero members.
            cls = {}
            for U, ws in by_class.items():
                vals = {acc.get(w, 0) for w in ws}
                if len(vals) != 1:
                    raise AssertionError(
                        "d_%s . d_%s is not constant on the descent class %s"
                        % (sorted(S), sorted(T), sorted(U)))
                cls[U] = vals.pop()
            # d_U = sum of the exact classes V SUBSET of U, so writing the
            # product as sum_U lambda_U d_U gives cls[V] = sum_{U superset V}
            # lambda_U, and the inversion runs over SUPERSETS:
            #     lambda_U = sum_{V superset U} (-1)^{|V|-|U|} cls[V].
            # Inverting over subsets instead is a different invertible change
            # of basis -- it leaves the opposite-algebra test of C3b intact,
            # which is why that test passed while C3a did not.
            for U in subsets:
                tot = 0
                for V in subsets:
                    if U.issubset(V):
                        tot += (-1) ** (len(V) - len(U)) * cls[V]
                if tot:
                    c[(S, T, U)] = tot
    return subsets, c


def comp_to_subset(alpha, n):
    """The composition alpha of n, as its set of partial sums in {1..n-1}."""
    out, s = [], 0
    for a in alpha[:-1]:
        s += a
        out.append(s)
    return frozenset(out)


# ---------------------------------------------------------------------------
# the five bimonoid columns, on an arbitrary collection with arbitrary maps
# ---------------------------------------------------------------------------

COLUMNS = ("prod_closure", "coprod_closure", "assoc", "coassoc", "compat")


def splits(m):
    """Ordered pairs (S, T) with S | T = m and S & T = 0."""
    return [(s, m & ~s) for s in submasks(m)]


def five_columns(universe, mu, de, ground):
    """Failure counts, one per column.

    `universe[mask]` is the collection's basis on that ground set.  `mu` and
    `de` are evaluated in the AMBIENT -- nothing is skipped for landing
    outside the collection -- so a 0 in the associativity column is a real
    identity and not a vacuous count.  That distinction is the whole content
    of the section-5 repair and it is re-implemented here rather than
    inherited.
    """
    f = dict.fromkeys(COLUMNS, 0)
    f["pairs"] = 0
    for I, els in universe.items():
        for (S, T) in splits(I):
            for x in universe[S]:
                for y in universe[T]:
                    f["pairs"] += 1
                    if mu(x, y) not in els:
                        f["prod_closure"] += 1
            for x in els:
                d = de(x, S, T)
                if d is None:
                    continue
                if d[0] not in universe[S] or d[1] not in universe[T]:
                    f["coprod_closure"] += 1
    I = ground
    for (S, R) in splits(I):
        for (S1, S2) in splits(S):
            for x in universe[S1]:
                for y in universe[S2]:
                    for z in universe[R]:
                        if mu(mu(x, y), z) != mu(x, mu(y, z)):
                            f["assoc"] += 1
    for (A, rest) in splits(I):
        for (B, C) in splits(rest):
            for x in universe[I]:
                d1 = de(x, A, B | C)
                lo = None if d1 is None else de(d1[1], B, C)
                d2 = de(x, A | B, C)
                ro = None if d2 is None else de(d2[0], A, B)
                lv = None if lo is None else (d1[0], lo[0], lo[1])
                rv = None if ro is None else (ro[0], ro[1], d2[1])
                if lv != rv:
                    f["coassoc"] += 1
    for (S1, T1) in splits(I):
        for (S2, T2) in splits(I):
            A, B = S1 & S2, S1 & T2
            C, D = T1 & S2, T1 & T2
            for x in universe[S1]:
                for y in universe[T1]:
                    lhs = de(mu(x, y), S2, T2)
                    dx = de(x, A, B)
                    dy = de(y, C, D)
                    rhs = (None if (dx is None or dy is None)
                           else (mu(dx[0], dy[0]), mu(dx[1], dy[1])))
                    if lhs != rhs:
                        f["compat"] += 1
    return f


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()
