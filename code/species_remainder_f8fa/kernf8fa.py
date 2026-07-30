"""kernf8fa -- primitives for the mg-f8fa remainder repair.

Written fresh.  It shares NO code with `kern7d75.py`, `hopf7d75.py`,
`kern6f61.py` or `kerna61f.py`: posets are sets of strict pairs closed under
transitivity, faces are ordered set compositions tested against the cone
inequality directly, and the Tits product is built from block intersections.
Nothing here is imported from the instrument it is checking.

The two objects this file exists to build:

  * Solomon's descent algebra inside `kS_n`, under BOTH composition
    conventions, so that "convention B is the opposite algebra of convention
    A" is a measurement rather than an assertion (w1).
  * faces lying in the braid cone of a poset, with the Tits product and with
    the Hopf-monoid product mu_{S,T}, so that "control (ii) fires on a type
    mismatch" is a measurement rather than an assertion (w2).
"""

from itertools import permutations, combinations


# ---------------------------------------------------------------------------
# permutations, descents, and the two composition conventions
# ---------------------------------------------------------------------------

def descent_set(w):
    """w is a tuple of 1..n.  Descents as a frozenset of positions 0..n-2."""
    return frozenset(i for i in range(len(w) - 1) if w[i] > w[i + 1])


def subsets(n):
    """All subsets of {0..n-2}, as frozensets, in a fixed order."""
    base = list(range(n - 1))
    out = []
    for k in range(len(base) + 1):
        for c in combinations(base, k):
            out.append(frozenset(c))
    return out


def d_basis(n):
    """d_T = sum over { w : des(w) subset T }.  Returned as {T: [w, ...]}."""
    W = list(permutations(range(1, n + 1)))
    return {T: [w for w in W if descent_set(w) <= T] for T in subsets(n)}


def compose_A(u, v):
    """Convention A: (u.v)(i) = u(v(i))."""
    return tuple(u[v[i] - 1] for i in range(len(v)))


def compose_B(u, v):
    """Convention B: (u.v)(i) = v(u(i)) -- the opposite convention."""
    return tuple(v[u[i] - 1] for i in range(len(u)))


def product_multiset(members, S, T, compose):
    """The product d_S . d_T as a multiset of permutations (a dict w -> mult).

    Comparing multisets rather than structure constants keeps this file free
    of any basis-expansion step, so nothing about the d_T basis is assumed.
    """
    out = {}
    for u in members[S]:
        for v in members[T]:
            w = compose(u, v)
            out[w] = out.get(w, 0) + 1
    return out


def descent_table(n, compose):
    """{(S, T): multiset of d_S . d_T} for every pair of subsets."""
    members = d_basis(n)
    subs = subsets(n)
    return {(S, T): product_multiset(members, S, T, compose)
            for S in subs for T in subs}


# ---------------------------------------------------------------------------
# posets, faces, cones
# ---------------------------------------------------------------------------

def posets_on(I):
    """Every partial order on the finite set I, as a frozenset of strict
    pairs (i, j) meaning i < j.  Brute force over all irreflexive relations,
    kept and returned when transitive and antisymmetric."""
    I = sorted(I)
    pairs = [(i, j) for i in I for j in I if i != j]
    out = []
    for m in range(1 << len(pairs)):
        rel = frozenset(pairs[k] for k in range(len(pairs)) if m >> k & 1)
        if any((j, i) in rel for (i, j) in rel):
            continue
        if any((i, k) not in rel
               for (i, j) in rel for (j2, k) in rel if j == j2 and i != k):
            continue
        out.append(rel)
    return out


def set_compositions(I):
    """Ordered set compositions of I: tuples of non-empty disjoint blocks
    (as frozensets) whose union is I.  The empty set has exactly one, ()."""
    I = sorted(I)
    if not I:
        return [()]
    out = []
    for k in range(1, len(I) + 1):
        for assign in _surjections(len(I), k):
            blocks = [frozenset(I[p] for p in range(len(I))
                                if assign[p] == b) for b in range(k)]
            out.append(tuple(blocks))
    return out


def _surjections(n, k):
    """All surjective maps {0..n-1} -> {0..k-1}, as tuples."""
    if k > n:
        return []
    out = []
    for m in range(k ** n):
        f = []
        x = m
        for _ in range(n):
            f.append(x % k)
            x //= k
        if len(set(f)) == k:
            out.append(tuple(f))
    return out


def in_cone(rel, F):
    """Does the face F lie in the braid cone C(rel) = {x : x_i <= x_j when
    i < j}?  A face is the locus constant on each block with values strictly
    increasing in the block index, so the test is: block(i) <= block(j)."""
    where = {}
    for b, B in enumerate(F):
        for i in B:
            where[i] = b
    return all(where[i] <= where[j] for (i, j) in rel)


def faces_in_cone(rel, I):
    return [F for F in set_compositions(I) if in_cone(rel, F)]


def tits_product(F, G):
    """Refine F by G: blocks B_a & C_b in lexicographic (a, b) order, empties
    dropped.  On disjoint ground sets every intersection is empty and the
    result is the EMPTY composition -- which is the whole of w2."""
    out = []
    for B in F:
        for C in G:
            X = B & C
            if X:
                out.append(X)
    return tuple(out)


def concat(F, G):
    """The Hopf-monoid product of set compositions: concatenation."""
    return tuple(F) + tuple(G)


def restrict_poset(rel, S):
    return frozenset((i, j) for (i, j) in rel if i in S and j in S)


def poset_union(r1, r2):
    return frozenset(r1) | frozenset(r2)


def decompositions(I):
    """Every ordered pair (S, T) with S disjoint union T = I."""
    I = sorted(I)
    out = []
    for m in range(1 << len(I)):
        S = frozenset(I[k] for k in range(len(I)) if m >> k & 1)
        out.append((S, frozenset(I) - S))
    return out


def elems_F(I):
    """The basis of F[I]: pairs (poset on I, face of I lying in its cone)."""
    out = []
    for rel in posets_on(I):
        for F in faces_in_cone(rel, I):
            out.append((rel, F))
    return out


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
