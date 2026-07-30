"""The measurement: what does a link-based (local-to-global) bound give for
lambda_2(Delta_AT), and how does it compare with the truth?

The technique under test is the one Hodge-side technique whose *hypothesis* has
no graph-side statement: it is quantified over the LINKS of faces of F(P), and
links of faces below the top two dimensions have no counterpart in the
adjacent-transposition graph.

Statement used (CITED -- Alev-Lau 2020, refining Kaufman-Oppenheim and
Dinur-Kaufman; the matroid case is Anari-Liu-Oveis Gharan-Vinzant).  For a pure
d-dimensional weighted simplicial complex X, writing

    gamma_i = max { lambda_2(1-skeleton of link(sigma)) : dim sigma = i }

for -1 <= i <= d-2, the down-up walk on the facets satisfies

    gap(P_du)  >=  (1 / (d+1)) * prod_{i=-1}^{d-2} (1 - gamma_i).

Here d = n-2 and (Theorem D of the deliverable) I - P_du = Delta_AT / (2(n-1)),
so the bound reads

    lambda_2(Delta_AT)  >=  2 * prod_{i=-1}^{n-4} (1 - gamma_i).            (LG)

The inequality itself is CITED, not proved here -- so this module also *checks*
it on every poset in the population.  A violation would mean either the cited
form is misremembered or the weighting convention is wrong; either way the
measurement would be void, so the check is reported alongside the numbers.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from linalg import lambda2_weighted_graph, smallest_nonzero, sparse_matvec
from links import (faces_of, facets_of, join_type, link_skeleton, at_gap_matrix,
                   blocks_of_face, induced_subposet)

_LINK_MEMO = {}


def link_lambda2(P, sigma, facets, memo=None, use_memo=True):
    """lambda_2 of the weighted 1-skeleton of link(sigma).

    Memoised on the localisation key `join_type(P, sigma)`.  `controls.py`
    verifies (exhaustively, n <= 5) that the key really does determine the value,
    which is the spectral content of the localisation theorem.
    """
    memo = _LINK_MEMO if memo is None else memo
    key = join_type(P, sigma) if use_memo else None
    if use_memo and key in memo:
        return memo[key]
    verts, edges = link_skeleton(P, sigma, facets)
    lam, conn = lambda2_weighted_graph(len(verts), edges)
    if use_memo:
        memo[key] = (lam, conn)
    return (lam, conn)


def gammas(P, facets=None, faces=None):
    """gamma_i for -1 <= i <= d-2, d = n-2.  Returns a dict i -> (gamma, argmax
    key, connected_flag).  Faces of dimension i have i+2 blocks, so only faces
    with at most n-2 blocks are touched."""
    n = P.n
    d = n - 2
    if facets is None:
        facets = facets_of(P)
    if faces is None:
        faces = faces_of(P)
    out = {}
    for i in range(-1, d - 1):
        best = None
        for sigma in faces.get(i, []):
            lam, conn = link_lambda2(P, sigma, facets)
            if lam is None:
                continue
            if best is None or lam > best[0]:
                best = (lam, join_type(P, sigma), conn)
        if best is not None:
            out[i] = best
    return out


def lg_bound(P, facets=None, faces=None):
    """The (LG) lower bound on lambda_2(Delta_AT), plus its ingredients."""
    g = gammas(P, facets, faces)
    prod = 1.0
    for i in sorted(g):
        prod *= (1.0 - g[i][0])
    return 2.0 * prod, g


def at_lambda2(P, m_lanczos=None):
    """lambda_2(Delta_AT) = smallest nonzero eigenvalue of D - A on L(P).

    Rank-one shift rather than deflation: with c > lambda_max(Delta_AT) the
    operator  M = Delta_AT + c * (1 1^T)/|L|  has the same spectrum except that
    the kernel eigenvalue 0 (the constants, since the adjacent-transposition
    graph is connected) is moved to c.  So lambda_min(M) = lambda_2(Delta_AT),
    and Lanczos converges to it as an extreme eigenvalue with no projection to
    maintain.  Returns None if |L(P)| = 1.
    """
    les, rows = at_gap_matrix(P)
    m = len(les)
    if m < 2:
        return None
    c = 4.0 * (P.n - 1) + 4.0            # > lambda_max(D - A) <= 2 max deg
    base = sparse_matvec(rows, m)

    def mv(v):
        s = sum(v) * c / m
        out = base(v)
        return [x + s for x in out]

    return smallest_nonzero(mv, m, [], m=m_lanczos)
