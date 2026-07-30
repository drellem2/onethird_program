"""Intrinsic face geometry of a finite poset: core objects.

Pure Python, no external dependencies, exact integer arithmetic throughout.
Nothing here uses floating point.

Objects built (all from the definitions in
`~/files/intrinsic_face_geometry_program.tex`, not from any prior calculation):

  * a poset P on ground set [n] = {0,...,n-1}, given by its strict order relation;
  * the order ideals J(P)  (down-sets), encoded as bitmasks;
  * the face complex  F(P) = \\coprod_k Sur_iso(P,[k])  -- surjective isotone maps
    P -> [k], equivalently ordered set partitions of P compatible with P;
  * the boundary maps of F(P) with the standard simplicial signs;
  * the top absolute and top relative Hodge Laplacians;
  * the adjacent-transposition graph on L(P) and its graph Laplacian.

KEY STRUCTURAL IDENTIFICATION (derived here, used everywhere below).
A map f : P -> [k] is surjective and isotone iff the sets
    S_i = f^{-1}({1,...,i}),  i = 1..k-1
are a strictly increasing chain of *proper nonempty order ideals* of P.
So
    Sur_iso(P,[k])  <->  chains of length k-1 in  J(P) \\ {empty, P}.
Hence F(P) is exactly the order complex of the proper part of the distributive
lattice J(P): a simplicial complex whose vertices are the proper nonempty
ideals, whose faces are chains of them, and whose facets (k = n) are the
maximal chains, i.e. the linear extensions of P.  dim F(P) = n-2.

We do NOT assume this identification: `sur_iso` below enumerates surjective
isotone maps directly by brute force, and `chains_of_ideals` builds the chain
complex; `selftest.py` checks the two agree for every poset tested.
"""

from fractions import Fraction
from itertools import combinations, permutations


# --------------------------------------------------------------------------
# Posets
# --------------------------------------------------------------------------

class Poset:
    """A finite poset on ground set {0,...,n-1}.

    `less` is the set of strict relations (i,j) meaning i <_P j.  It is stored
    transitively closed and irreflexive.  Nothing assumes compatibility with
    the natural order of the labels.
    """

    __slots__ = ("n", "less", "name")

    def __init__(self, n, relations, name=None):
        self.n = n
        less = set()
        for (a, b) in relations:
            if a == b:
                raise ValueError("irreflexive relation required")
            less.add((a, b))
        # transitive closure
        changed = True
        while changed:
            changed = False
            for (a, b) in list(less):
                for (c, d) in list(less):
                    if b == c and (a, d) not in less:
                        if a == d:
                            raise ValueError("relation has a cycle: not a poset")
                        less.add((a, d))
                        changed = True
        for (a, b) in less:
            if (b, a) in less:
                raise ValueError("relation is not antisymmetric: not a poset")
        self.less = frozenset(less)
        self.name = name

    def __repr__(self):
        return "Poset(n=%d, less=%s)" % (self.n, sorted(self.less))

    def leq(self, a, b):
        return a == b or (a, b) in self.less

    def comparable(self, a, b):
        return a == b or (a, b) in self.less or (b, a) in self.less

    # -- invariants used for reporting failure modes ------------------------

    def automorphisms(self):
        """All order-automorphisms, as tuples g with g[i] = image of i."""
        out = []
        for g in permutations(range(self.n)):
            ok = all(((g[a], g[b]) in self.less) for (a, b) in self.less)
            if ok:
                out.append(g)
        return out

    def is_connected(self):
        """Connectivity of the comparability graph (Hasse-connectedness)."""
        if self.n == 0:
            return True
        adj = {i: set() for i in range(self.n)}
        for (a, b) in self.less:
            adj[a].add(b)
            adj[b].add(a)
        seen = {0}
        stack = [0]
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        return len(seen) == self.n

    def is_antichain(self):
        return len(self.less) == 0

    def is_chain(self):
        return len(self.less) == self.n * (self.n - 1) // 2

    def canonical_key(self):
        """Isomorphism invariant: lexicographically minimal relation set."""
        best = None
        for g in permutations(range(self.n)):
            rel = tuple(sorted((g[a], g[b]) for (a, b) in self.less))
            if best is None or rel < best:
                best = rel
        return (self.n, best)


# --------------------------------------------------------------------------
# Order ideals and the face complex
# --------------------------------------------------------------------------

def order_ideals(P):
    """All order ideals (down-sets) of P as bitmasks, sorted by (popcount, mask).

    S is an ideal iff  (j in S and i <_P j)  =>  i in S.
    """
    out = []
    for mask in range(1 << P.n):
        ok = True
        for (a, b) in P.less:
            if (mask >> b) & 1 and not ((mask >> a) & 1):
                ok = False
                break
        if ok:
            out.append(mask)
    out.sort(key=lambda m: (bin(m).count("1"), m))
    return out


def sur_iso(P, k):
    """Brute-force enumeration of Sur_iso(P,[k]).

    Returns tuples f of length n with f[i] in {1..k}, surjective, and isotone:
    i <_P j  =>  f[i] <= f[j].  Used only as an independent cross-check of the
    chain description; exponential, so only called for small n.
    """
    out = []
    n = P.n
    def rec(i, assign):
        if i == n:
            if len(set(assign)) == k:
                out.append(tuple(assign))
            return
        for v in range(1, k + 1):
            ok = True
            for j in range(i):
                if (j, i) in P.less and assign[j] > v:
                    ok = False
                    break
                if (i, j) in P.less and v > assign[j]:
                    ok = False
                    break
            if ok:
                rec(i + 1, assign + [v])
    rec(0, [])
    return out


def face_from_sur_iso(P, f):
    """The chain of proper nonempty ideals corresponding to an f in Sur_iso(P,[k])."""
    k = max(f)
    chain = []
    for i in range(1, k):
        mask = 0
        for x in range(P.n):
            if f[x] <= i:
                mask |= 1 << x
        chain.append(mask)
    return tuple(chain)


def proper_ideals(P):
    full = (1 << P.n) - 1
    return [m for m in order_ideals(P) if m != 0 and m != full]


def chains_of_ideals(P):
    """All chains (by strict inclusion) of proper nonempty ideals of P.

    Returns dict: dimension d -> sorted list of faces, where a face is a tuple
    of d+1 ideals in strictly increasing order.  dim -1 is the empty face.
    A face with d+1 vertices corresponds to an ordered partition with d+2
    blocks, i.e. to an element of Sur_iso(P,[d+2]).
    """
    verts = proper_ideals(P)
    idx = {v: i for i, v in enumerate(verts)}
    # covering relation of inclusion among proper ideals is not needed; we
    # enumerate chains directly.
    below = {v: [w for w in verts if w != v and (w & v) == w] for v in verts}
    faces = {-1: [()]}
    cur = [(v,) for v in verts]
    d = 0
    while cur:
        faces[d] = sorted(cur, key=lambda c: tuple(idx[x] for x in c))
        nxt = []
        for c in cur:
            top = c[-1]
            for w in verts:
                if w != top and (top & w) == top:  # top strictly contained in w
                    nxt.append(c + (w,))
        cur = nxt
        d += 1
    return faces


def linear_extensions(P):
    """Linear extensions of P as words: w[t] = element in position t (0-indexed).

    Enumerated directly from the definition (repeated minimal-element choice),
    not via ideals.
    """
    out = []
    n = P.n
    def rec(placed_mask, word):
        if len(word) == n:
            out.append(tuple(word))
            return
        for x in range(n):
            if (placed_mask >> x) & 1:
                continue
            # x must have all its P-predecessors already placed
            ok = all(((placed_mask >> a) & 1) for a in range(n) if (a, x) in P.less)
            if ok:
                rec(placed_mask | (1 << x), word + [x])
    rec(0, [])
    out.sort()
    return out


def le_to_facet(w):
    """The maximal chain of proper ideals determined by a linear extension word."""
    chain = []
    mask = 0
    for t in range(len(w) - 1):
        mask |= 1 << w[t]
        chain.append(mask)
    return tuple(chain)


def facet_to_le(facet, n):
    """Inverse of le_to_facet."""
    w = []
    prev = 0
    for m in list(facet) + [(1 << n) - 1]:
        diff = m & ~prev
        assert bin(diff).count("1") == 1, "not a maximal chain"
        w.append(diff.bit_length() - 1)
        prev = m
    return tuple(w)


# --------------------------------------------------------------------------
# Simplicial chain complex with standard signs
# --------------------------------------------------------------------------

def boundary_matrix(faces_d, faces_dm1):
    """Standard simplicial boundary  d_d : C_d -> C_{d-1}.

    Faces are tuples of vertices in a fixed increasing order (here: increasing
    by inclusion, which is a total order on any chain).  The boundary of
    (v_0,...,v_d) is sum_i (-1)^i (v_0,...,^v_i,...,v_d).

    Returns a dict-of-dicts M[row][col] = coefficient, with rows indexed by
    faces_dm1 and columns by faces_d, plus the two index maps.
    """
    row_idx = {f: i for i, f in enumerate(faces_dm1)}
    M = {}
    for j, f in enumerate(faces_d):
        for i in range(len(f)):
            g = f[:i] + f[i + 1:]
            r = row_idx[g]
            M.setdefault(r, {})
            M[r][j] = M[r].get(j, 0) + (-1) ** i
    return M, len(faces_dm1), len(faces_d)


def down_laplacian_from_boundary(M, nrows, ncols, allowed_rows=None):
    """L = d^T d  as a dense list-of-lists of integers, ncols x ncols.

    If `allowed_rows` is given (a set of row indices), rows outside it are
    dropped first -- this is exactly the relative boundary map
    C_d(K) -> C_{d-1}(K)/C_{d-1}(A) for a subcomplex A whose (d-1)-faces are
    the dropped rows.
    """
    L = [[0] * ncols for _ in range(ncols)]
    for r, row in M.items():
        if allowed_rows is not None and r not in allowed_rows:
            continue
        items = list(row.items())
        for (j1, c1) in items:
            for (j2, c2) in items:
                L[j1][j2] += c1 * c2
    return L


# --------------------------------------------------------------------------
# The three objects the sketch's claims compare
# --------------------------------------------------------------------------

def top_laplacians(P):
    """Top absolute and top relative Hodge Laplacians of F(P), plus bookkeeping.

    The top faces of F(P) are the facets = linear extensions (n-1 vertices,
    dimension n-2).  There is nothing above them, so the top Hodge Laplacian is
    purely the down-Laplacian  d^T d.

    The boundary subcomplex dF(P) is generated by the *free ridges*: the
    (n-3)-faces contained in exactly one facet.  The relative complex
    C_*(F, dF) kills those ridges, so the relative top Laplacian is
    d_rel^T d_rel with the free rows dropped.

    Returns a dict.
    """
    n = P.n
    les = linear_extensions(P)
    facets = [le_to_facet(w) for w in les]
    fidx = {f: i for i, f in enumerate(facets)}

    # ridges = (n-3)-faces that lie in some facet == all (n-2)-subsets of facets
    ridge_set = set()
    for f in facets:
        for i in range(len(f)):
            ridge_set.add(f[:i] + f[i + 1:])
    ridges = sorted(ridge_set)

    M, nr, nc = boundary_matrix(facets, ridges)
    # which facets contain each ridge
    ridge_facets = {r: [] for r in range(nr)}
    for r, row in M.items():
        ridge_facets[r] = sorted(row.keys())

    interior_rows = {r for r in range(nr) if len(ridge_facets[r]) == 2}
    free_rows = {r for r in range(nr) if len(ridge_facets[r]) == 1}
    assert interior_rows | free_rows == set(range(nr)), \
        "a ridge lies in 0 or >=3 facets"

    L_abs = down_laplacian_from_boundary(M, nr, nc)
    L_rel = down_laplacian_from_boundary(M, nr, nc, allowed_rows=interior_rows)

    return {
        "P": P,
        "n": n,
        "les": les,
        "facets": facets,
        "fidx": fidx,
        "ridges": ridges,
        "n_ridges": nr,
        "n_free_ridges": len(free_rows),
        "L_abs": L_abs,
        "L_rel": L_rel,
        "ridge_facets": ridge_facets,
    }


def adjacent_transposition_graph(P):
    """The adjacent-transposition graph on L(P): the induced subgraph of the
    Cayley graph of S_n on the generators s_1,...,s_{n-1} (acting on positions).

    Built directly from the words -- no reference to the face complex.
    Returns (les, A, deg) with A the 0/1 adjacency matrix and deg the degrees.
    """
    les = linear_extensions(P)
    idx = {w: i for i, w in enumerate(les)}
    m = len(les)
    A = [[0] * m for _ in range(m)]
    for w in les:
        i = idx[w]
        for t in range(P.n - 1):
            v = list(w)
            v[t], v[t + 1] = v[t + 1], v[t]
            v = tuple(v)
            if v in idx:
                A[i][idx[v]] = 1
    deg = [sum(row) for row in A]
    return les, A, deg


def at_laplacian(P):
    """The ordinary adjacent-transposition Laplacian on L(P):
    the generator  sum_{i=1}^{n-1} (1 - tau_i)  where tau_i swaps positions
    i,i+1 if the result is a linear extension and acts as the identity
    otherwise.  Equal to  D - A , the unnormalised graph Laplacian of the
    adjacent-transposition graph.
    """
    les, A, deg = adjacent_transposition_graph(P)
    m = len(les)
    return les, [[(deg[i] if i == j else 0) - A[i][j] for j in range(m)]
                 for i in range(m)]


_AMBIENT_CACHE = {}


def _ambient_coxeter_laplacian(n):
    """The matrix of sum_{i=1}^{n-1} (1 - s_i) on C[S_n], s_i acting on the
    right (= swapping positions i,i+1 of the word).  Cached per n."""
    if n in _AMBIENT_CACHE:
        return _AMBIENT_CACHE[n]
    allperm = sorted(permutations(range(n)))
    aidx = {w: i for i, w in enumerate(allperm)}
    N = len(allperm)
    amb = [[0] * N for _ in range(N)]
    for w in allperm:
        i = aidx[w]
        amb[i][i] += n - 1
        for t in range(n - 1):
            v = list(w)
            v[t], v[t + 1] = v[t + 1], v[t]
            amb[i][aidx[tuple(v)]] -= 1
    _AMBIENT_CACHE[n] = (amb, aidx)
    return amb, aidx


def coxeter_compression(P):
    """Compression to C[L(P)] of the ambient Coxeter Laplacian sum_i (1 - s_i)
    acting on C[S_n] by right multiplication (= adjacent transposition of
    positions).

      sum_i (1 - s_i) = (n-1) I - sum_i R_{s_i}
      compression     = (n-1) I - A_ind      (A_ind = induced adjacency on L(P))

    Built here by literally forming the ambient S_n matrix and cutting it down,
    so that the "compression" is not assumed to equal (n-1)I - A.
    """
    n = P.n
    amb, aidx = _ambient_coxeter_laplacian(n)
    les = linear_extensions(P)
    keep = [aidx[w] for w in les]
    return les, [[amb[a][b] for b in keep] for a in keep]


# --------------------------------------------------------------------------
# The orientation / sign twist
# --------------------------------------------------------------------------

def perm_sign(w):
    """Sign of the permutation given by the word w (as a bijection position ->
    element).  Computed by inversion count."""
    inv = 0
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if w[i] > w[j]:
                inv += 1
    return -1 if inv % 2 else 1


def twist(L, les):
    """Conjugate L by E = diag(sgn(w)).  E is an involution, so E L E = E L E^{-1}."""
    s = [perm_sign(w) for w in les]
    m = len(les)
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]


# --------------------------------------------------------------------------
# Exact linear algebra (rank over Q, and mod p) -- only used for homology
# --------------------------------------------------------------------------

def rank_mod_p(M, nrows, ncols, p=(1 << 31) - 1):
    """Rank of a sparse dict-of-dicts matrix mod a prime p."""
    rows = []
    for r in range(nrows):
        d = M.get(r)
        if d:
            rows.append({c: v % p for c, v in d.items() if v % p})
    rank = 0
    pivots = {}
    for row in rows:
        row = dict(row)
        while row:
            c = min(row)
            if c in pivots:
                prow = pivots[c]
                factor = row[c] * pow(prow[c], p - 2, p) % p
                for cc, vv in prow.items():
                    nv = (row.get(cc, 0) - factor * vv) % p
                    if nv:
                        row[cc] = nv
                    else:
                        row.pop(cc, None)
            else:
                pivots[c] = row
                rank += 1
                break
    return rank


def rank_exact(M, nrows, ncols):
    """Rank over Q by fraction-free-ish Gaussian elimination (Fractions)."""
    rows = []
    for r in range(nrows):
        d = M.get(r)
        if d:
            rows.append({c: Fraction(v) for c, v in d.items() if v})
    rank = 0
    pivots = {}
    for row in rows:
        row = dict(row)
        while row:
            c = min(row)
            if c in pivots:
                prow = pivots[c]
                factor = row[c] / prow[c]
                for cc, vv in prow.items():
                    nv = row.get(cc, Fraction(0)) - factor * vv
                    if nv:
                        row[cc] = nv
                    else:
                        row.pop(cc, None)
            else:
                pivots[c] = row
                rank += 1
                break
    return rank


def reduced_betti(faces, use_exact=False):
    """Reduced Betti numbers over Q of the simplicial complex given by
    `faces` (dict d -> list of d-faces, including d = -1 for the empty face).

    Uses the augmented chain complex, so this returns *reduced* homology.
    """
    dims = sorted(d for d in faces if d >= -1)
    top = max(dims)
    rk = {}
    for d in range(0, top + 1):
        M, nr, nc = boundary_matrix(faces[d], faces[d - 1])
        rk[d] = rank_exact(M, nr, nc) if use_exact else rank_mod_p(M, nr, nc)
    rk[top + 1] = 0
    betti = {}
    for d in range(0, top + 1):
        betti[d] = len(faces[d]) - rk[d] - rk[d + 1]
    return betti


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def mat_eq(A, B):
    if len(A) != len(B):
        return False
    return all(len(a) == len(b) and all(x == y for x, y in zip(a, b))
               for a, b in zip(A, B))


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[i]))] for i in range(len(A))]


def is_diagonal(A):
    return all(A[i][j] == 0 for i in range(len(A)) for j in range(len(A)) if i != j)
