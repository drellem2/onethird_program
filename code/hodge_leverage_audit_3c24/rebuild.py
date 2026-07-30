"""An INDEPENDENT rebuild of the machinery mg-a2bd's strike rests on.

This module shares NO code with `code/hodge_leverage/` or `code/face_geometry/`
and imports nothing from them.  Everything below is written from the
definitions:

  * posets on n elements up to isomorphism, by brute-force canonicalisation
    over all n! relabellings (the deliverable's route is a canonical key from
    `face_complex.Poset.canonical_key`);
  * faces of F(P) as P-COMPATIBLE ORDERED PARTITIONS, enumerated by peeling
    ideals off the front (the deliverable's route is chains of proper ideals);
  * the weighted 1-skeleton of link(sigma) built from REFINEMENTS of sigma,
    with weights computed as PRODUCTS OF LINEAR-EXTENSION COUNTS of the
    induced subposets (the deliverable's route counts facets containing the
    face, by brute force over the facet list);
  * lambda_2 decided EXACTLY, in rational arithmetic, by the INERTIA of
    W - t*D (the deliverable's route is a floating-point cyclic Jacobi sweep
    of D^{-1/2} W D^{-1/2});
  * full spectra by Householder tridiagonalisation + implicit-shift QL (again
    a different algorithm from cyclic Jacobi).

Pure Python 3, no third-party packages (the repository convention).
"""

import math
from fractions import Fraction
from itertools import combinations, permutations


# ==========================================================================
# posets
# ==========================================================================

class P0:
    """A poset on {0..n-1}: `less` is the transitively closed strict order."""

    __slots__ = ("n", "less", "up", "dn", "tag")

    def __init__(self, n, rel, tag=None):
        less = set()
        frontier = set(rel)
        while frontier:
            less |= frontier
            nxt = set()
            for (a, b) in less:
                for (c, d) in less:
                    if b == c and (a, d) not in less:
                        nxt.add((a, d))
            frontier = nxt
        self.n = n
        self.less = frozenset(less)
        self.up = [set() for _ in range(n)]
        self.dn = [set() for _ in range(n)]
        for (a, b) in less:
            self.up[a].add(b)
            self.dn[b].add(a)
        self.tag = tag

    def key(self):
        """Canonical form: the lexicographically least relation set over all
        n! relabellings.  Deliberately brute force -- a different route from
        the deliverable's `canonical_key`, and cheap at n <= 6."""
        best = None
        for p in permutations(range(self.n)):
            r = tuple(sorted((p[a], p[b]) for (a, b) in self.less))
            if best is None or r < best:
                best = r
        return (self.n, best)


def all_posets_indep(n):
    """Every poset on n elements up to isomorphism.

    Every poset admits a linear extension, so it is isomorphic to one whose
    relation sits inside {(i,j) : i < j}; range over those and deduplicate by
    the brute-force canonical key.
    """
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    seen = {}
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            rel = set(sub)
            # transitively closed?
            ok = True
            for (a, b) in rel:
                for (c, d) in rel:
                    if b == c and (a, d) not in rel:
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                continue
            Q = P0(n, rel)
            kk = Q.key()
            if kk not in seen:
                seen[kk] = Q
    return [seen[k] for k in sorted(seen)]


def induced(P, mask):
    """P restricted to `mask`, relabelled 0..k-1."""
    elts = [x for x in range(P.n) if (mask >> x) & 1]
    pos = {x: i for i, x in enumerate(elts)}
    rel = [(pos[a], pos[b]) for (a, b) in P.less if a in pos and b in pos]
    return P0(len(elts), rel)


def is_antichain(P):
    return not P.less


def ideals(P):
    """All order ideals (downward-closed subsets) of P, as bitmasks."""
    out = []
    for m in range(1 << P.n):
        ok = True
        for x in range(P.n):
            if (m >> x) & 1:
                for a in P.dn[x]:
                    if not ((m >> a) & 1):
                        ok = False
                        break
            if not ok:
                break
        if ok:
            out.append(m)
    return out


_NLE = {}


def n_linext(P):
    """The number of linear extensions of P, by dynamic programming over
    ideals.  (The deliverable enumerates the words themselves.)"""
    k = P.key()
    if k in _NLE:
        return _NLE[k]
    full = (1 << P.n) - 1
    f = {0: 1}
    for m in sorted(ideals(P)):
        if m == 0:
            continue
        tot = 0
        for x in range(P.n):
            if not ((m >> x) & 1):
                continue
            # x may be removed iff it is maximal in m
            if any(((m >> y) & 1) for y in P.up[x]):
                continue
            tot += f[m & ~(1 << x)]
        f[m] = tot
    _NLE[k] = f[full]
    return f[full]


def nle_mask(P, mask, cache):
    if mask not in cache:
        cache[mask] = n_linext(induced(P, mask))
    return cache[mask]


# ==========================================================================
# faces = P-compatible ordered partitions
# ==========================================================================

def faces_by_dim(P):
    """dict i -> list of faces of dimension i, a face being a tuple of block
    bitmasks (B_1,...,B_{i+2}) whose prefix unions are order ideals.

    Enumerated by peeling a nonempty ideal off the front of what is left --
    not by building chains of ideals.
    """
    full = (1 << P.n) - 1
    out = {}

    def rec(rest, blocks):
        if rest == 0:
            out.setdefault(len(blocks) - 2, []).append(tuple(blocks))
            return
        Q_elts = [x for x in range(P.n) if (rest >> x) & 1]
        # nonempty ideals of P restricted to `rest`
        k = len(Q_elts)
        for sub in range(1, 1 << k):
            m = 0
            for t in range(k):
                if (sub >> t) & 1:
                    m |= 1 << Q_elts[t]
            ok = True
            for x in Q_elts:
                if (m >> x) & 1:
                    for a in P.dn[x]:
                        if ((rest >> a) & 1) and not ((m >> a) & 1):
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                rec(rest & ~m, blocks + [m])

    rec(full, [])
    return out


def link_graph(P, sigma, cache):
    """The weighted 1-skeleton of link_{F(P)}(sigma).

    Vertices: the refinements of sigma that split ONE block B_s into an ideal
    C of P|_{B_s} and its complement, C proper and nonempty.
    Edge weight between two compatible splits = the number of facets of F(P)
    containing the doubly-refined face = the PRODUCT of the linear-extension
    counts of the induced subposets on its blocks.

    Returns (verts, edges) with edges = [(i, j, integer weight)].
    """
    # base product over the blocks of sigma that are never split
    splits = []          # (block index s, ideal C)
    for s, B in enumerate(sigma):
        elts = [x for x in range(P.n) if (B >> x) & 1]
        k = len(elts)
        if k < 2:
            continue
        for sub in range(1, (1 << k) - 1):
            m = 0
            for t in range(k):
                if (sub >> t) & 1:
                    m |= 1 << elts[t]
            ok = True
            for x in elts:
                if (m >> x) & 1:
                    for a in P.dn[x]:
                        if ((B >> a) & 1) and not ((m >> a) & 1):
                            ok = False
                            break
                if not ok:
                    break
            if ok:
                splits.append((s, m))
    nv = len(splits)
    edges = []
    for i in range(nv):
        si, Ci = splits[i]
        for j in range(i + 1, nv):
            sj, Cj = splits[j]
            if si == sj:
                if (Ci & Cj) == Ci and Ci != Cj:
                    parts = [Ci, Cj & ~Ci, sigma[si] & ~Cj]
                elif (Ci & Cj) == Cj and Ci != Cj:
                    parts = [Cj, Ci & ~Cj, sigma[si] & ~Ci]
                else:
                    continue
                blocks = []
                for s, B in enumerate(sigma):
                    if s == si:
                        blocks.extend(parts)
                    else:
                        blocks.append(B)
            else:
                blocks = []
                for s, B in enumerate(sigma):
                    if s == si:
                        blocks.extend([Ci, B & ~Ci])
                    elif s == sj:
                        blocks.extend([Cj, B & ~Cj])
                    else:
                        blocks.append(B)
            w = 1
            for b in blocks:
                w *= nle_mask(P, b, cache)
            if w:
                edges.append((i, j, w))
    return splits, edges


# ==========================================================================
# exact spectral decisions
# ==========================================================================

def inertia(M):
    """(pos, zero, neg) of a symmetric matrix of Fractions, exactly.

    Symmetric Gaussian elimination; when every remaining diagonal entry is 0
    a congruence v_i -> v_i + v_j manufactures a nonzero one.
    """
    N = len(M)
    if N == 0:
        return (0, 0, 0)
    A = [[Fraction(x) for x in row] for row in M]
    active = list(range(N))
    pos = neg = zero = 0
    while active:
        piv = None
        for i in active:
            if A[i][i] != 0:
                piv = i
                break
        if piv is None:
            found = None
            for a in range(len(active)):
                for b in range(a + 1, len(active)):
                    i, j = active[a], active[b]
                    if A[i][j] != 0:
                        found = (i, j)
                        break
                if found:
                    break
            if found is None:
                zero += len(active)
                break
            i, j = found
            for k in range(N):
                A[i][k] = A[i][k] + A[j][k]
            for k in range(N):
                A[k][i] = A[k][i] + A[k][j]
            piv = i
        p = A[piv][piv]
        if p > 0:
            pos += 1
        else:
            neg += 1
        active = [i for i in active if i != piv]
        for i in active:
            f = A[i][piv] / p
            if f:
                rp = A[piv]
                ri = A[i]
                for k in active:
                    ri[k] = ri[k] - f * rp[k]
    return (pos, zero, neg)


def spectral_inertia_at(nv, edges, t):
    """Inertia of W - t*D, i.e. (#{lambda_i > t}, #{= t}, #{< t}) for the
    eigenvalues of the walk P = D^{-1}W.  `t` a Fraction.

    Valid because P is self-adjoint for <f,g>_D, so f^T(W - tD)f is the
    D-quadratic form of P - tI.
    """
    d = [0] * nv
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    M = [[Fraction(0)] * nv for _ in range(nv)]
    for (u, v, w) in edges:
        M[u][v] += w
        M[v][u] += w
    for u in range(nv):
        M[u][u] -= t * d[u]
    return inertia(M)


def lambda2_ge_exact(nv, edges, t=Fraction(1, 2)):
    """Exactly: is lambda_2 >= t?  (lambda_1 = 1 on a connected graph.)

    lambda_2 < t  iff  exactly one eigenvalue exceeds t and none equals it.
    An isolated vertex or a disconnected graph therefore reports True, which
    matches the deliverable's convention (lambda_2 = 1 there).
    """
    if nv < 2:
        return None
    pos, zero, neg = spectral_inertia_at(nv, edges, t)
    return not (pos == 1 and zero == 0)


# ==========================================================================
# floating-point full spectra (Householder + implicit-shift QL)
# ==========================================================================

def _tred2(a):
    n = len(a)
    d = [0.0] * n
    e = [0.0] * n
    for i in range(n - 1, 0, -1):
        l = i - 1
        h = scale = 0.0
        if l > 0:
            for k in range(l + 1):
                scale += abs(a[i][k])
            if scale == 0.0:
                e[i] = a[i][l]
            else:
                for k in range(l + 1):
                    a[i][k] /= scale
                    h += a[i][k] * a[i][k]
                f = a[i][l]
                g = -math.sqrt(h) if f >= 0.0 else math.sqrt(h)
                e[i] = scale * g
                h -= f * g
                a[i][l] = f - g
                f = 0.0
                for j in range(l + 1):
                    g = 0.0
                    for k in range(j + 1):
                        g += a[j][k] * a[i][k]
                    for k in range(j + 1, l + 1):
                        g += a[k][j] * a[i][k]
                    e[j] = g / h
                    f += e[j] * a[i][j]
                hh = f / (h + h)
                for j in range(l + 1):
                    f = a[i][j]
                    e[j] = g = e[j] - hh * f
                    for k in range(j + 1):
                        a[j][k] -= (f * e[k] + g * a[i][k])
        else:
            e[i] = a[i][l]
        d[i] = h
    e[0] = 0.0
    for i in range(n):
        d[i] = a[i][i]
    return d, e


def _tqli(d, e):
    n = len(d)
    for i in range(1, n):
        e[i - 1] = e[i]
    e[n - 1] = 0.0
    for l in range(n):
        it = 0
        while True:
            m = l
            while m < n - 1:
                dd = abs(d[m]) + abs(d[m + 1])
                if abs(e[m]) <= 1e-16 * dd:
                    break
                m += 1
            if m == l:
                break
            it += 1
            if it > 60:
                break
            g = (d[l + 1] - d[l]) / (2.0 * e[l])
            r = math.hypot(g, 1.0)
            g = d[m] - d[l] + e[l] / (g + (r if g >= 0 else -r))
            s = c = 1.0
            p = 0.0
            for i in range(m - 1, l - 1, -1):
                f = s * e[i]
                b = c * e[i]
                r = math.hypot(f, g)
                e[i + 1] = r
                if r == 0.0:
                    d[i + 1] -= p
                    e[m] = 0.0
                    break
                s = f / r
                c = g / r
                g = d[i + 1] - p
                r = (d[i] - g) * s + 2.0 * c * b
                p = s * r
                d[i + 1] = g + p
                g = c * r - b
            else:
                d[l] -= p
                e[l] = g
                e[m] = 0.0
                continue
    return sorted(d)


def walk_spectrum_float(nv, edges):
    """All eigenvalues of P = D^{-1}W (ascending), or None if some vertex is
    isolated.  Householder + QL on S = D^{-1/2} W D^{-1/2}."""
    if nv < 1:
        return []
    d = [0.0] * nv
    for (u, v, w) in edges:
        d[u] += w
        d[v] += w
    if any(x <= 0.0 for x in d):
        return None
    S = [[0.0] * nv for _ in range(nv)]
    sq = [math.sqrt(x) for x in d]
    for (u, v, w) in edges:
        val = w / (sq[u] * sq[v])
        S[u][v] += val
        S[v][u] += val
    dd, ee = _tred2(S)
    return _tqli(dd, ee)


# ==========================================================================
# the Coxeter complex F(A_m), from the closed-form weights
# ==========================================================================

def coxeter_graph(m):
    """The weighted 1-skeleton of F(A_m): vertices the proper nonempty subsets
    S of [m]; edge {S,T} for S subset T with weight |S|!(|T|-|S|)!(m-|T|)!."""
    verts = list(range(1, (1 << m) - 1))
    idx = {S: i for i, S in enumerate(verts)}
    fac = [math.factorial(k) for k in range(m + 1)]
    edges = []
    for S in verts:
        sS = bin(S).count("1")
        for T in verts:
            if T == S or (S & T) != S:
                continue
            sT = bin(T).count("1")
            if sT <= sS:
                continue
            edges.append((idx[S], idx[T], fac[sS] * fac[sT - sS] * fac[m - sT]))
    return len(verts), edges
