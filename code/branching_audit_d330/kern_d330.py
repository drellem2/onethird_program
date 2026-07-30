"""kern_d330 --- the fourth instrument to measure this object, written fresh.

mg-d330, the independent audit of the mg-13b2 repair.

SHARES NO CODE with `code/branching_locate_db09/kerndb09.py` (mg-db09, the
first instrument), with `code/branching_audit_2060/kern2060.py` (mg-2060, the
second) or with `code/branching_audit_a218/kern_a218.py` (mg-a218, the third).
It is built from the combinatorial definition and nothing else.

WHAT IS DEFINED HERE, and it is the whole of it.

A half-diagram on `n` points with `p` arcs is a non-crossing partial matching
of {0, ..., n-1} using `p` arcs; the `n - 2p` unmatched points are DEFECTS,
and no arc may enclose a defect.  These index a basis of the Temperley-Lieb
cell module V(n,p); their number is C(n,p) - C(n,p-1).

The cellular bilinear form: glue the reflection of `u` onto `v`.  Every arc
endpoint then has degree 2 and every defect degree 1, so each connected
component is a closed loop or a path between two defects.  <u,v> is
beta^(#loops) when every path runs from a u-defect to a v-defect, and 0 when
any path joins two defects on the same side --- that is exactly the condition
"the number of through-lines is not reduced".

The irreducible L(n,p) = V(n,p)/rad<,> and dim L(n,p) = rank of the Gram
matrix over Q.  A vertex of Vershik-Okounkov's branching graph at level n is
an irreducible module, so the VERTEX SET at (n, beta) is

    { (p, dim L(n,p)) : dim L(n,p) > 0 }

and its CARDINALITY is one statistic about it.  This distinction is the whole
subject of this audit, so the two are given different names here and the
rendering that abbreviates the first to a list of dimensions is a third thing
again --- `dims_render` --- never called "the set".

Exact arithmetic only: Fraction, and beta is an integer.
"""

from fractions import Fraction
from itertools import combinations


def binom(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def half_diagrams(n, p):
    """Non-crossing partial matchings of {0..n-1} with p arcs and no arc
    enclosing a defect.  Returned as (tuple of sorted arcs, tuple of defects),
    in a deterministic order."""
    out = []
    for pts in combinations(range(n), 2 * p):
        rest = [i for i in range(n) if i not in set(pts)]
        # the 2p chosen points must match up as a balanced non-crossing
        # matching among THEMSELVES, and no arc may enclose a leftover point.
        arcs = _noncrossing_matchings(list(pts))
        for a in arcs:
            if any(any(i < d < j for (i, j) in a) for d in rest):
                continue
            out.append((tuple(sorted(a)), tuple(rest)))
    return sorted(set(out))


def _noncrossing_matchings(pts):
    """All non-crossing perfect matchings of the list `pts` (already sorted)."""
    if not pts:
        return [[]]
    out = []
    first = pts[0]
    for k in range(1, len(pts), 2):
        partner = pts[k]
        inside = pts[1:k]
        outside = pts[k + 1:]
        for a in _noncrossing_matchings(inside):
            for b in _noncrossing_matchings(outside):
                out.append([(first, partner)] + a + b)
    return out


def pairing(u, v, n, beta):
    """<u, v> in the cellular form.  Returns a Fraction (0 or beta^loops)."""
    # nodes 0..n-1 are the u side, n..2n-1 the v side; gluing edge i -- n+i.
    adj = {i: [] for i in range(2 * n)}

    def link(a, b):
        adj[a].append(b)
        adj[b].append(a)

    for (i, j) in u[0]:
        link(i, j)
    for (i, j) in v[0]:
        link(n + i, n + j)
    for i in range(n):
        link(i, n + i)
    seen = [False] * (2 * n)
    loops = 0
    for start in range(2 * n):
        if seen[start]:
            continue
        comp = []
        stack = [start]
        seen[start] = True
        while stack:
            x = stack.pop()
            comp.append(x)
            for y in adj[x]:
                if not seen[y]:
                    seen[y] = True
                    stack.append(y)
        ends = [x for x in comp if len(adj[x]) == 1]
        if not ends:
            loops += 1
        else:
            assert len(ends) == 2, "a component has %d endpoints" % len(ends)
            a, b = ends
            if (a < n) == (b < n):        # both defects on the same side
                return Fraction(0)
    return Fraction(beta) ** loops


def gram(n, p, beta):
    hd = half_diagrams(n, p)
    return [[pairing(u, v, n, beta) for v in hd] for u in hd]


def rank(mat):
    """Exact rank over Q by fraction-free-enough Gaussian elimination."""
    m = [row[:] for row in mat]
    rows, cols = len(m), (len(m[0]) if m else 0)
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if m[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = Fraction(1) / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for (a, b) in zip(m[i], m[r])]
        r += 1
        if r == rows:
            break
    return r


_cache = {}


def vertex_set(n, beta):
    """THE VERTEX SET at (n, beta): the pairs (p, dim L(n,p)) with dim > 0.

    A set of labelled vertices.  NOT a count, and NOT the rendering below."""
    key = (n, beta)
    if key not in _cache:
        out = []
        for p in range(n // 2 + 1):
            d = rank(gram(n, p, beta))
            if d > 0:
                out.append((p, d))
        _cache[key] = tuple(out)
    return _cache[key]


def dims_render(vset):
    """THE RENDERING the delivered document's section-0 column uses: the
    dimensions alone, p ascending.  This is a function OF the set; whether it
    is injective is the question e1 asks, and it is not assumed here."""
    return "[" + ",".join(str(d) for (p, d) in vset) + "]"


def pairs_render(vset):
    """The full labelled form: (p, dim) for every vertex."""
    return "[" + ",".join("%d:%d" % (p, d) for (p, d) in vset) + "]"


def cell_dims(n):
    """dim V(n,p) for p = 0.., independent of beta --- the Catalan triangle."""
    return [binom(n, p) - binom(n, p - 1) for p in range(n // 2 + 1)]
