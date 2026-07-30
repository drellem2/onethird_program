"""The face semigroup of F(P): left-regular band, support lattice, Brown walks.

mg-276d used F(P) purely as a simplicial complex and recorded (its 8.3(6)) that
the left-regular-band product the source equips F(P) with is UNUSED.  This module
uses it.

A face is stored as a tuple of bitmask blocks (B_1,...,B_k) -- the ordered
partition of P read off a chain of ideals.  k = 1 is the identity face.

  * `lrb_product(x,y)`  -- successive refinement: blocks B_i & C_j ordered
    lexicographically by (i,j), empties dropped.
  * `support(x)`        -- the underlying set partition, as a frozenset of masks.
  * `support_lattice(P)`-- all supports, i.e. all partitions pi with P/pi acyclic
    (the two descriptions are checked against each other in `controls.py`).
    Order: X <= Y iff Y refines X (coarser = smaller).  This is the order in
    which supp(xy) = supp(x) v supp(y).
  * `brown_walk(P,w)`   -- the walk c -> x.c on chambers, x ~ w.
  * `brown_spectrum(P,w)` -- the predicted eigenvalues and multiplicities:

        lambda_X = sum_{y : supp(y) <= X} w(y)
        multiplicities m_X determined by
            sum_{Y >= X} m_Y  =  prod_{B in X} |L(P|_B)|
        (the number of chambers refining X).

    This is Brown's theorem for random walks on left regular bands (Brown 2000;
    Bidigare-Hanlon-Rockmore for the braid arrangement).  The theorem is CITED;
    every consequence is checked against the actual matrix in `run_lrb.py`.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import Poset, linear_extensions
from links import faces_of, blocks_of_face, induced_subposet


# --------------------------------------------------------------------------
# faces as ordered partitions, and the band product
# --------------------------------------------------------------------------

def all_faces(P):
    """Every face of F(P) as an ordered partition (tuple of bitmask blocks),
    including the identity face (k = 1).  Sorted for determinism."""
    out = []
    fs = faces_of(P)
    for d in sorted(fs):
        for sigma in fs[d]:
            out.append(tuple(blocks_of_face(P, sigma)))
    return out


def lrb_product(x, y):
    """Successive refinement: the LRB product of two ordered partitions."""
    out = []
    for B in x:
        for C in y:
            m = B & C
            if m:
                out.append(m)
    return tuple(out)


def support(x):
    return frozenset(x)


def is_chamber(x, n):
    return len(x) == n


# --------------------------------------------------------------------------
# the support lattice: acyclic partitions
# --------------------------------------------------------------------------

def is_acyclic_partition(P, part):
    """Does P/part have no directed cycle among distinct blocks?"""
    blocks = list(part)
    bi = {}
    for i, B in enumerate(blocks):
        for x in range(P.n):
            if (B >> x) & 1:
                bi[x] = i
    adj = {i: set() for i in range(len(blocks))}
    for (a, b) in P.less:
        if bi[a] != bi[b]:
            adj[bi[a]].add(bi[b])
    # cycle detection
    colour = {}

    def dfs(u):
        colour[u] = 1
        for v in adj[u]:
            if colour.get(v, 0) == 1:
                return True
            if colour.get(v, 0) == 0 and dfs(v):
                return True
        colour[u] = 2
        return False

    return not any(colour.get(u, 0) == 0 and dfs(u) for u in adj)


def all_set_partitions(n):
    """Every set partition of {0..n-1} as a frozenset of bitmasks."""
    out = []

    def rec(i, blocks):
        if i == n:
            out.append(frozenset(blocks))
            return
        for j in range(len(blocks)):
            nb = list(blocks)
            nb[j] |= (1 << i)
            rec(i + 1, nb)
        rec(i + 1, blocks + [1 << i])

    rec(0, [])
    return out


def support_lattice(P, faces=None):
    """All supports of faces of F(P), as a sorted list of frozensets of masks."""
    if faces is None:
        faces = all_faces(P)
    S = {support(x) for x in faces}
    return sorted(S, key=lambda X: (len(X), sorted(X)))


def refines(Y, X):
    """True if Y refines X (every block of Y is inside a block of X), i.e. X <= Y
    in the LRB support order."""
    for b in Y:
        if not any((b & a) == b for a in X):
            return False
    return True


def chambers_refining(P, X):
    """prod_{B in X} |L(P|_B)| -- the number of chambers refining X."""
    tot = 1
    for B in X:
        tot *= len(linear_extensions(induced_subposet(P, B)))
    return tot


def brown_multiplicities(P, L=None):
    """m_X for every X in the support lattice, by descending solution of
    sum_{Y >= X} m_Y = chambers_refining(X).  Returns dict X -> m_X."""
    if L is None:
        L = support_lattice(P)
    # process from finest (largest, |X| = n) to coarsest
    order = sorted(L, key=lambda X: -len(X))
    m = {}
    for X in order:
        tot = chambers_refining(P, X)
        s = 0
        for Y in L:
            if Y != X and refines(Y, X):
                s += m.get(Y, 0)
        m[X] = tot - s
    return m


def brown_eigenvalues(P, w, L=None, faces=None):
    """lambda_X = sum_{y : supp(y) <= X} w(y), as exact Fractions.

    `w` is a dict face -> weight (Fraction or int); it need not be normalised,
    in which case the returned eigenvalues are scaled by sum(w) too.
    """
    if faces is None:
        faces = all_faces(P)
    if L is None:
        L = support_lattice(P, faces)
    out = {}
    for X in L:
        s = 0
        for y in faces:
            if w.get(y, 0) and refines(X, support(y)):
                s += w[y]
        out[X] = s
    return out


def brown_walk(P, w, faces=None):
    """The walk c -> x.c on the chambers of F(P).

    Returns (chambers, M, total) with M an integer matrix and `total` = sum of
    the (integer) weights, so that M/total is the stochastic transition matrix.
    """
    if faces is None:
        faces = all_faces(P)
    chambers = [x for x in faces if len(x) == P.n]
    cidx = {c: i for i, c in enumerate(chambers)}
    m = len(chambers)
    M = [[0] * m for _ in range(m)]
    total = 0
    for x in faces:
        wt = w.get(x, 0)
        if not wt:
            continue
        total += wt
        for c in chambers:
            d = lrb_product(x, c)
            M[cidx[c]][cidx[d]] += wt
    return chambers, M, total


# --------------------------------------------------------------------------
# deterministic integer weight vectors
# --------------------------------------------------------------------------

def weights_all_faces(faces, seed=7):
    """A deterministic positive integer weight on every face."""
    st = seed
    w = {}
    for x in faces:
        st = (1103515245 * st + 12345) % 100003
        w[x] = 1 + (st % 97)
    return w


def weights_two_block(faces, P, seed=11):
    """Positive weights on the faces with exactly two blocks, zero elsewhere.

    These are the 'block moves': x.c cuts the linear extension into the two
    blocks of x and reorders inside each by c.  A named, non-generic support, so
    that the check is not only on generic w.
    """
    st = seed
    w = {}
    for x in faces:
        if len(x) == 2:
            st = (1103515245 * st + 12345) % 100003
            w[x] = 1 + (st % 61)
    return w


def weights_singleton_first(faces, P, seed=13):
    """Positive weights on the faces ({i}, rest) -- the 'move i to the front'
    faces.  For an antichain this is exactly the Tsetlin library / move-to-front
    walk, whose spectrum is classical, so it doubles as a positive control."""
    st = seed
    w = {}
    full = (1 << P.n) - 1
    for x in faces:
        if len(x) == 2 and bin(x[0]).count("1") == 1:
            st = (1103515245 * st + 12345) % 100003
            w[x] = 1 + (st % 53)
    return w
