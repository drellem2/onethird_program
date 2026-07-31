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

from collections import namedtuple
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


def le_to_facet_offbyone(w):
    """A DELIBERATELY MIS-INDEXED facet enumeration.

    Exists only so that NEGATIVE CONTROL 4 (mg-2789) can corrupt the map
    L(P) -> facets of F(P); the probe never calls it.

    The correct rule (`le_to_facet`) takes the prefixes w[:1], ..., w[:n-1].
    This one takes the prefixes of w[1:] instead:
        {w[1]}, {w[1],w[2]}, ..., {w[1],...,w[n-1]},
    the classic off-by-one on the same loop.  It is still injective on words
    and still returns a strictly increasing chain of n-1 sets, so nothing
    downstream complains -- but the sets are in general NOT order ideals of P,
    and the pattern of which facets share a ridge changes.  The resulting
    complex is therefore a DIFFERENT incidence structure, not a relabelled
    copy of the right one.
    """
    chain = []
    mask = 0
    for t in range(1, len(w)):
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

def boundary_matrix(faces_d, faces_dm1, sign_mode="true"):
    """Standard simplicial boundary  d_d : C_d -> C_{d-1}.

    Faces are tuples of vertices in a fixed increasing order (here: increasing
    by inclusion, which is a total order on any chain).  The boundary of
    (v_0,...,v_d) is sum_i (-1)^i (v_0,...,^v_i,...,v_d).

    Returns a dict-of-dicts M[row][col] = coefficient, with rows indexed by
    faces_dm1 and columns by faces_d, plus the two index maps.

    `sign_mode` exists ONLY so that a negative control can corrupt the
    *construction* of the boundary matrix (mg-e0ce F2; NEGATIVE CONTROL 3 in
    controls.py).  The probe itself always runs with "true".

      "true"     the standard alternating sign (-1)^i.
      "allplus"  every incidence +1.  Kept because it is the corruption that
                 CANNOT fire on the top Laplacians -- see NEGATIVE CONTROL 3.
      "parity"   (-1)^i times a global sign per column (facet), flipped on the
                 odd-indexed columns.  This is the corruption that does fire.
    """
    row_idx = {f: i for i, f in enumerate(faces_dm1)}
    M = {}
    for j, f in enumerate(faces_d):
        if sign_mode == "true":
            col_sign = 1
        elif sign_mode == "allplus":
            col_sign = 1
        elif sign_mode == "parity":
            col_sign = 1 if j % 2 == 0 else -1
        else:
            raise ValueError("unknown sign_mode %r" % (sign_mode,))
        for i in range(len(f)):
            g = f[:i] + f[i + 1:]
            r = row_idx[g]
            s = 1 if sign_mode == "allplus" else (-1) ** i * col_sign
            M.setdefault(r, {})
            M[r][j] = M[r].get(j, 0) + s
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

INCIDENCE_MODES = ("true", "facet_offbyone", "ridge_facets",
                   "split_free_as_interior", "ridge_drop", "facet_swap01")


def top_laplacians(P, sign_mode="true", incidence_mode="true"):
    """Top absolute and top relative Hodge Laplacians of F(P), plus bookkeeping.

    The top faces of F(P) are the facets = linear extensions (n-1 vertices,
    dimension n-2).  There is nothing above them, so the top Hodge Laplacian is
    purely the down-Laplacian  d^T d.

    The boundary subcomplex dF(P) is generated by the *free ridges*: the
    (n-3)-faces contained in exactly one facet.  The relative complex
    C_*(F, dF) kills those ridges, so the relative top Laplacian is
    d_rel^T d_rel with the free rows dropped.

    `sign_mode` is passed straight to boundary_matrix and exists only for
    NEGATIVE CONTROL 3 (the construction-side control, mg-e0ce F2).  The probe
    always runs with the default "true".

    `incidence_mode` exists only for NEGATIVE CONTROL 4 (mg-2789).  It corrupts
    the INCIDENCE STRUCTURE rather than the signs -- the sites are named in
    controls.py -- and the probe always runs with the default "true".

      "true"                   the construction as defined.
      "facet_offbyone"         facets built by `le_to_facet_offbyone`: the map
                               L(P) -> facets is mis-indexed, so the ridge
                               sharing pattern is a different complex.
      "ridge_facets"           one interior ridge's facet list is mis-recorded:
                               its second incidence is re-targeted onto a facet
                               it does not meet.  Row weight and signs are
                               untouched, so the free/interior split below is
                               untouched: the only thing wrong is WHICH facets
                               that ridge joins.
      "split_free_as_interior" the boundary matrix is exactly right, but one
                               FREE ridge is counted as interior, i.e. the
                               boundary subcomplex dF(P) is taken one ridge too
                               small when forming the relative complex.
      "ridge_drop"             one interior ridge is missing from the complex
                               altogether (an incomplete ridge enumeration).
      "facet_swap01"           facets 0 and 1 exchanged.  A REJECTED CANDIDATE,
                               kept because the reason it was rejected is the
                               point: exchanging two columns conjugates L^rel
                               by a (signed) permutation matrix, so it is
                               isospectral -- a relabelling of the facet set,
                               i.e. a gauge.  NEGATIVE CONTROL 4 measures that
                               and does not score it as one of its rows.

    Returns a dict.
    """
    n = P.n
    les = linear_extensions(P)
    if incidence_mode == "facet_offbyone":
        facets = [le_to_facet_offbyone(w) for w in les]
    elif incidence_mode in INCIDENCE_MODES:
        facets = [le_to_facet(w) for w in les]
    else:
        raise ValueError("unknown incidence_mode %r" % (incidence_mode,))
    if incidence_mode == "facet_swap01" and len(facets) >= 2:
        facets[0], facets[1] = facets[1], facets[0]
    fidx = {f: i for i, f in enumerate(facets)}

    # ridges = (n-3)-faces that lie in some facet == all (n-2)-subsets of facets
    ridge_set = set()
    for f in facets:
        for i in range(len(f)):
            ridge_set.add(f[:i] + f[i + 1:])
    ridges = sorted(ridge_set)

    M, nr, nc = boundary_matrix(facets, ridges, sign_mode=sign_mode)
    # which facets contain each ridge
    ridge_facets = {r: [] for r in range(nr)}
    for r, row in M.items():
        ridge_facets[r] = sorted(row.keys())

    mutated_ridge = None
    if incidence_mode == "ridge_facets":
        for r in range(nr):
            if len(ridge_facets[r]) != 2:
                continue
            j1, j2 = ridge_facets[r]
            j3 = next((j for j in range(nc) if j not in (j1, j2)), None)
            if j3 is None:          # fewer than 3 facets: mutation undefined
                break
            M[r][j3] = M[r].pop(j2)
            ridge_facets[r] = sorted(M[r].keys())
            mutated_ridge = r
            break
    elif incidence_mode == "ridge_drop":
        for r in range(nr):
            if len(ridge_facets[r]) == 2:
                del M[r]
                ridge_facets[r] = []
                mutated_ridge = r
                break

    interior_rows = {r for r in range(nr) if len(ridge_facets[r]) == 2}
    free_rows = {r for r in range(nr) if len(ridge_facets[r]) == 1}
    multi_rows = {r for r in range(nr) if len(ridge_facets[r]) >= 3}
    if incidence_mode == "true":
        assert interior_rows | free_rows == set(range(nr)), \
            "a ridge lies in 0 or >=3 facets"
    if incidence_mode == "split_free_as_interior" and free_rows:
        mutated_ridge = min(free_rows)
        interior_rows = interior_rows | {mutated_ridge}

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
        "incidence_mode": incidence_mode,
        "n_multi_ridges": len(multi_rows),
        "mutated_ridge": mutated_ridge,
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


def det_shift_mod_p(A, shift, p=(1 << 31) - 1):
    """det(A - shift.I) mod p, by Gaussian elimination over F_p."""
    m = len(A)
    B = [[(A[i][j] - (shift if i == j else 0)) % p for j in range(m)]
         for i in range(m)]
    det = 1
    for c in range(m):
        piv = next((r for r in range(c, m) if B[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            B[c], B[piv] = B[piv], B[c]
            det = -det
        det = det * B[c][c] % p
        inv = pow(B[c][c], p - 2, p)
        for r in range(c + 1, m):
            f = B[r][c] * inv % p
            if f:
                Bc, Br = B[c], B[r]
                for k in range(c, m):
                    Br[k] = (Br[k] - f * Bc[k]) % p
    return det % p


def not_isospectral(A, B, shifts=(3, 5, 7, 11, 13)):
    """True iff A and B are PROVABLY not isospectral.  ONE-SIDED: False means
    "no invariant checked here separated them", never "they are isospectral".

    Both matrices must be symmetric integer matrices (L^rel and its twist are).
    Checked, cheapest first: the trace (sum of the eigenvalues), the sum of the
    squares of the entries (= trace of the square = sum of the squared
    eigenvalues), and finally det(. - k.I) mod a prime for a few k, which are
    values of the characteristic polynomial.  Any of these differing over Z
    forces the characteristic polynomials to differ; differing residues force
    differing integers, so a difference found mod p is a proof.

    Used by NEGATIVE CONTROL 4: a corruption whose spectrum provably moves is
    not a similarity transform of the true matrix at all -- not a diagonal sign
    conjugation, not a relabelling of the facets, not anything.
    """
    if trace(A) != trace(B):
        return True
    if frobenius2(A) != frobenius2(B):
        return True
    for k in shifts:
        if det_shift_mod_p(A, k) != det_shift_mod_p(B, k):
            return True
    return False


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


def trace(A):
    return sum(A[i][i] for i in range(len(A)))


def frobenius2(A):
    """sum of squares of the entries = trace(A^2) for symmetric A = sum of the
    squares of the eigenvalues."""
    return sum(x * x for row in A for x in row)


Trace = namedtuple("Trace", "absorbable gate signs_read")

ABSORB_GATES = ("shape", "diagonal", "magnitude", "parity")


def absorb_trace(A, B):
    """`absorbable_by_diagonal_twist`, INSTRUMENTED: the decision, together with
    the gate the code actually returned at and how many signs it actually read.

    Returns Trace(absorbable, gate, signs_read):

      gate       -- "shape", "diagonal", "magnitude" or "parity": the label
                    written at the `return` statement that fired.  It is
                    EMITTED BY THE CODE PATH, not recomputed from A and B
                    afterwards, and it is the only thing in this file entitled
                    to be called the gate that settled a pair.
      signs_read -- how many off-diagonal constraints s_i s_j the union-find
                    loop actually consumed.  0 means no sign entered the
                    decision, whatever the gate says.

    WHY THIS EXISTS, and it is the third attempt at one sentence (mg-8a12 ->
    mg-da45 -> mg-5f9a).  Two previous versions of "which gate decided" were
    written ALONGSIDE the predicate and both were wrong about it: mg-8a12 read
    only `diag_preserved` and mg-da45's `deciding_gate` tested all diagonals and
    then all magnitudes, which is not this function's order -- it interleaves
    the two BY ROW.  On 57 of the 297 biting pairs in NEGATIVE CONTROL 4 the two
    orders name different gates (mg-1c80 F1).  A reason asserted next to a
    procedure can disagree with it; a reason returned by the procedure cannot.
    So the label is produced here and `controls.py` has NO gate procedure at all
    -- `deciding_gate` was deleted outright and nothing, not even an alias,
    replaced it (checked in the AST by
    code/face_geometry_instr_5f9a/d1_trace.py).  An earlier draft of this
    docstring said the name survived as a call to this function; it does not, and
    describing a design that was not shipped is what mg-d0e2's F4 caught.

    THE LABEL IS A TRACE AND NOT A CAUSE, and this is the limitation to read
    before quoting a gate count.  The gates are NOT exclusive: a pair can
    violate several and this reports the FIRST ONE REACHED.  In particular the
    magnitude test runs over j == i as well, so on matrices with non-negative
    diagonals every "diagonal" here is also a magnitude violation, and deleting
    the diagonal gate would change these labels while changing no decision.
    `gate_violations` below measures that exhaustively rather than arguing it.

    THIS IS THE QUESTION A NEGATIVE CONTROL MUST ANSWER ABOUT ITSELF (mg-5630):
    the orientation twist E = diag(sgn w) is a member of this family, so is
    NEGATIVE CONTROL 2's M3 twist ("-1 on one facet, +1 elsewhere"), and so is
    the diag((-1)^j) that NEGATIVE CONTROL 3's facet-parity corruption turns
    out to equal.  If this returns True for a corruption, the corruption is a
    re-orientation the battery already varies -- a sign gauge, not a
    construction error.

    THE `shape` GATE HAS ONE `return` AND ITS CONDITION HAS ONE CLAUSE, and it
    reached that state one rung at a time (mg-e7bc -> mg-9220 -> mg-c4c8 ->
    mg-64b6).  THE UNIT A DELETION TEST REMOVES IS THE UNIT IT LICENSES A CLAIM
    ABOUT, and this gate has now been rewritten twice for that one sentence, at
    two different sizes.

    RUNG ONE -- TWO RETURNS (mg-e7bc).  The test that guards this function
    deleted both `shape` returns TOGETHER, the artifact changed, and the gate
    was booked as covered.  Deleting the FIRST one ALONE -- `if m != len(B)` --
    left the artifact BYTE-IDENTICAL, every row green, exit 0: the
    2x2-against-3x3 pair built for the gate falls into the loop, where
    `len(A[0]) != len(B[0])` fires the SECOND return and answers False at gate
    "shape" identically.  So the deletion proved the PAIR was load-bearing and
    proved nothing about either return.  mg-9220 MERGED the two rather than
    cutting the first, and measured the difference rather than arguing it: cut
    `if m != len(B)` and put nothing in its place and this function answers
    ABSORBABLE for ([], [[1]]), raises IndexError for ([[1]], []), and answers
    ABSORBABLE for a 2x2 against a three-row B whose first two rows are 2 wide
    -- against a brute force that enumerates every s and finds none.

    RUNG TWO -- TWO CLAUSES (mg-c4c8).  The merged condition was `m != len(B)
    or any(len(A[i]) != len(B[i]) for i in range(m))`, and deleting its FIRST
    CLAUSE alone left the artifact BYTE-IDENTICAL, exit 0, every row green.
    That is rung one's sentence with `return` replaced by `clause`: the unit
    moved from a pair of returns to a pair of clauses and the pair was still
    what the test bit on.

    SO THE CONDITION BELOW HAS NO CLAUSE TO BE THE THIRD RUNG.  The two clauses
    were saying one thing -- A and B do not have the same row-shape profile --
    and it is written here as one comparison of two lists.  There is no boolean
    operator in it, so the smallest deletable unit inside this gate IS the
    `return`, and the deletion test that removes it (d2_deletion.py, AFTER-5)
    is a claim about the whole of it.  The move is the merge's, made once more
    instead of at the level below: REMOVE WHAT GENERATES THE FINDING RATHER
    THAN MEASURE ITS OUTPUT.  `gate_violations` and `diagonal_moves` below
    still carry the two-clause form; their `return`s are inert whole (mg-c4c8
    F3) and this commit did not touch them.

    IT IS THE SAME PREDICATE, MEASURED AND NOT ARGUED.  The condition below is
    true exactly when the orders differ or some row width does, so nothing this
    function returns can move.  d2_deletion.py's
    section PER CLAUSE runs this form, the merged two-clause form and the
    pinned two-return form side by side over a population indexed by SHAPE
    PROFILE -- which is what the condition reads -- and reports decision, gate
    label and raised exception for each.

    ONE LABEL MOVED WITH THE MERGE, on pairs no population here contains: the
    old order tested row 0's diagonal before row 1's width, so a pair RAGGED at
    row 1 and diagonal-different at row 0 was traced "diagonal".  Hoisting the
    width test labels it "shape" -- which is what `gate_violations` and
    `priority_gate` always said about it, so the merge removed a disagreement
    rather than creating one.  The artifact did not move for it, and does not
    move for this rewrite either.  AND THE MERGE MADE THIS GATE TOTAL: the
    two-return form indexed `A[i][i]` before it had checked row i's width and
    raised IndexError on 2,064 of mg-c4c8's 28,900 pairs where this form
    decides (its F5, undisclosed by mg-9220 and disclosed here).

    Method: s_i^2 = 1 pins every diagonal entry, |s_i s_j| = 1 pins every
    absolute value, and each nonzero off-diagonal entry forces the product
    s_i s_j.  What remains is a parity system, solved by union-find.
    """
    m = len(A)
    if [len(row) for row in A] != [len(row) for row in B]:
        return Trace(False, "shape", 0)
    for i in range(m):
        if A[i][i] != B[i][i]:
            return Trace(False, "diagonal", 0)
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return Trace(False, "magnitude", 0)
    parent = list(range(m))
    rel = [0] * m               # rel[x] = parity of s_x against parent[x]
    signs_read = 0

    def find(x):
        p = 0
        while parent[x] != x:
            p ^= rel[x]
            x = parent[x]
        return x, p

    for i in range(m):
        for j in range(i + 1, m):
            if A[i][j] == 0:
                continue
            signs_read += 1
            need = 0 if B[i][j] == A[i][j] else 1        # s_i s_j = (-1)^need
            ri, pi = find(i)
            rj, pj = find(j)
            if ri == rj:
                if pi ^ pj != need:
                    return Trace(False, "parity", signs_read)
            else:
                parent[ri] = rj
                rel[ri] = pi ^ pj ^ need
    return Trace(True, "parity", signs_read)


def gate_violations(A, B):
    """The SET of gates the pair (A, B) violates, computed EXHAUSTIVELY -- no
    short-circuit, so no dependence on the order the gates are tested in.

    This is the companion `absorb_trace` needs to be quotable.  A trace reports
    the first gate reached; whether that gate is the reason for the answer is a
    different question, and the only honest way to ask it is to test the others
    too.  A pair whose set is {"diagonal", "magnitude"} would have been rejected
    with either gate removed, so neither of them is load-bearing on it; a pair
    whose set is {"magnitude"} alone is one the magnitude gate really does
    settle.

    "parity" is never in the returned set: reaching the parity system is not a
    violation.  A pair with an empty set cleared both forced gates.
    """
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return frozenset(["shape"])
    bad = set()
    if any(A[i][i] != B[i][i] for i in range(m)):
        bad.add("diagonal")
    if any(abs(A[i][j]) != abs(B[i][j])
           for i in range(m) for j in range(m)):
        bad.add("magnitude")
    return frozenset(bad)


def diagonal_moves(A, B):
    """Does A differ from B on the DIAGONAL?  A property of the two matrices,
    asked directly.

    NOT a statement about `absorb_trace`'s execution, and kept apart from it on
    purpose (mg-5f9a).  This is the hypothesis of the theorem NEGATIVE CONTROL
    4 routes its forced rows to -- S.A.S = B with s_i^2 = 1 pins every diagonal
    entry, so a corruption that moves one is not absorbable for ANY sign vector
    -- and that implication holds at every n independently of what the code
    tests first.  mg-da45's `deciding_gate` served both purposes at once, which
    is how a routing quantity came to be printed as a trace of the predicate.
    """
    if len(A) != len(B) or any(len(A[i]) != len(B[i]) for i in range(len(A))):
        return False                    # shapes differ: no diagonal to compare
    return any(A[i][i] != B[i][i] for i in range(len(A)))


def absorbable_by_diagonal_twist(A, B):
    """Is there a diagonal sign matrix S = diag(s), s_i in {+1,-1}, with
    S.A.S == B ?  An exact decision procedure over the whole family, not a
    search over a few candidates.

    The decision half of `absorb_trace` (above), which is where the method and
    the caveats are documented.  One implementation, so a caller that wants the
    gate as well as the answer cannot get a gate from a different procedure.
    """
    return absorb_trace(A, B).absorbable
