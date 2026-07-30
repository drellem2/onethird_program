"""Links of faces of F(P), the localisation theorem, and the down-up walk.

Everything is built on `code/face_geometry/face_complex.py` (the audited
machinery of mg-276d / mg-e0ce); nothing here re-derives the bridge.

Objects added here:

  * `faces_of(P)`            -- all faces of F(P) as chains of proper ideals
                                (dimension d = number of ideals - 1).
  * `blocks_of_face`         -- the ordered partition of P a face encodes.
  * `link_skeleton(P, sigma)`-- the weighted 1-skeleton of link_{F(P)}(sigma),
                                with weights induced from the uniform measure on
                                facets: w(tau) = #{facets containing tau}.
                                Built by brute force from the facets, NOT from
                                the localisation theorem.
  * `join_type(P, sigma)`    -- the multiset of isomorphism types of the induced
                                subposets on the blocks of sigma.  By the
                                localisation theorem (Theorem L, docs) this
                                determines link(sigma) up to isomorphism of
                                weighted complexes -- which `controls.py` checks
                                rather than assumes.
  * `down_up_walk(P)`        -- the standard HDX down-up walk on the facets of
                                F(P), built from ridge incidences only.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import (Poset, proper_ideals, linear_extensions, le_to_facet,
                          adjacent_transposition_graph)


# --------------------------------------------------------------------------
# faces of F(P)
# --------------------------------------------------------------------------

def faces_of(P):
    """dict d -> list of faces of dimension d, a face being a tuple of proper
    nonempty ideals in strictly increasing order.  d = -1 is the empty face."""
    verts = proper_ideals(P)
    out = {-1: [()]}
    cur = [(v,) for v in verts]
    d = 0
    while cur:
        out[d] = cur
        nxt = []
        for c in cur:
            top = c[-1]
            for w in verts:
                if w != top and (top & w) == top:
                    nxt.append(c + (w,))
        cur = nxt
        d += 1
    return out


def facets_of(P):
    return [le_to_facet(w) for w in linear_extensions(P)]


def blocks_of_face(P, sigma):
    """The ordered partition of P encoded by the face sigma (a chain of ideals).

    Returns the list of blocks as bitmasks: I_1, I_2\\I_1, ..., P\\I_j.
    """
    full = (1 << P.n) - 1
    prev = 0
    blocks = []
    for I in sigma:
        blocks.append(I & ~prev)
        prev = I
    blocks.append(full & ~prev)
    return blocks


def induced_subposet(P, mask):
    """P restricted to the elements of `mask`, relabelled 0..k-1 in increasing
    order of the original label."""
    elts = [x for x in range(P.n) if (mask >> x) & 1]
    pos = {x: i for i, x in enumerate(elts)}
    rel = [(pos[a], pos[b]) for (a, b) in P.less if a in pos and b in pos]
    return Poset(len(elts), rel)


_CANON = {}


def canon_key(P):
    k = (P.n, tuple(sorted(P.less)))
    if k not in _CANON:
        _CANON[k] = P.canonical_key()
    return _CANON[k]


def join_type(P, sigma):
    """Isomorphism types of the induced subposets on the blocks of sigma,
    as a sorted tuple (blocks of size 1 contribute nothing to the link and are
    recorded as such, so they are kept in the key only via their count)."""
    keys = []
    for b in blocks_of_face(P, sigma):
        Q = induced_subposet(P, b)
        keys.append(canon_key(Q))
    return tuple(sorted(keys))


# --------------------------------------------------------------------------
# links, weighted by the induced measure
# --------------------------------------------------------------------------

def link_skeleton(P, sigma, facets=None):
    """The weighted 1-skeleton of link_{F(P)}(sigma).

    Vertices: proper nonempty ideals K not in sigma with sigma + {K} a chain.
    Edge {u,v} with weight #{facets of F(P)} containing sigma + {u,v}.
    Vertices with no incident edge are kept (they matter for connectivity).

    Built directly from the facet list: no use of the localisation theorem.
    Returns (vertices, edges) with edges a list of (i, j, weight) into
    `vertices`.
    """
    if facets is None:
        facets = facets_of(P)
    sset = set(sigma)
    # facets containing sigma
    cont = [set(f) for f in facets if sset <= set(f)]
    verts = set()
    for f in cont:
        verts |= (f - sset)
    verts = sorted(verts)
    idx = {v: i for i, v in enumerate(verts)}
    ew = {}
    for f in cont:
        rest = sorted(f - sset)
        for a in range(len(rest)):
            for b in range(a + 1, len(rest)):
                key = (idx[rest[a]], idx[rest[b]])
                ew[key] = ew.get(key, 0) + 1
    edges = [(i, j, float(w)) for (i, j), w in sorted(ew.items())]
    return verts, edges


# --------------------------------------------------------------------------
# the down-up walk on facets, built from ridge incidence only
# --------------------------------------------------------------------------

def down_up_walk(P):
    """The standard HDX down-up walk on the facets of F(P).

    From a facet sigma: pick one of its n-1 ridges uniformly, then pick
    uniformly among the facets containing that ridge (1 or 2 of them, by
    Lemma 3(a) of mg-276d).  Returns (facets, Pmat) with Pmat a dense
    row-stochastic matrix of Fractions-as-floats.

    Built ONLY from the simplicial incidence data -- no reference to linear
    extensions as words, no adjacent transpositions.
    """
    facets = facets_of(P)
    fidx = {f: i for i, f in enumerate(facets)}
    m = len(facets)
    nr = P.n - 1                          # ridges per facet
    ridge_facets = {}
    for f in facets:
        for i in range(len(f)):
            r = f[:i] + f[i + 1:]
            ridge_facets.setdefault(r, []).append(f)
    Pm = [[0.0] * m for _ in range(m)]
    for f in facets:
        i = fidx[f]
        for k in range(len(f)):
            r = f[:k] + f[k + 1:]
            cof = ridge_facets[r]
            for g in cof:
                Pm[i][fidx[g]] += 1.0 / (nr * len(cof))
    return facets, Pm


def at_gap_matrix(P):
    """Delta_AT = D - A on L(P) as a sparse row list [(j, value), ...]."""
    les, A, deg = adjacent_transposition_graph(P)
    rows = []
    for i in range(len(les)):
        row = [(i, float(deg[i]))]
        for j in range(len(les)):
            if A[i][j]:
                row.append((j, -1.0))
        rows.append(row)
    return les, rows
