"""kern_a218.py -- Temperley-Lieb from definitions, for the mg-a218 audit.

Shares no code with code/branching_locate_db09/ (the target, mg-db09/mg-e8b8)
or with code/branching_audit_2060/ (the first audit).  Everything here is
rebuilt from the definitions in the papers the target quotes:

  * TL_n(beta) as the algebra of planar perfect matchings of 2n points, with
    beta per closed loop.
  * link states / half-diagrams: non-crossing partial matchings of n points
    with p arcs, no defect nested inside an arc.
  * the cell (standard) module V(n,p): span of the link states with p arcs,
    with the diagram action truncated to zero whenever the number of defects
    drops (Graham-Lehrer).
  * the cellular bilinear form <,> on V(n,p).
  * L(n,p) := V(n,p)/rad<,>  -- the irreducibles (Graham-Lehrer).
  * the trace form of the regular representation, whose radical is rad(A) in
    characteristic 0.

Everything is exact: beta is an integer, all linear algebra is over Fraction.

NOTHING IN THIS FILE PRINTS.  It raises on internal inconsistency.
"""

from fractions import Fraction
from itertools import combinations

# ---------------------------------------------------------------------------
# 0.  small combinatorics
# ---------------------------------------------------------------------------


def binom(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(k):
        r = r * (n - i) // (i + 1)
    return r


def catalan(n):
    return binom(2 * n, n) // (n + 1)


def ballot(n, p):
    """dim V(n,p): number of link states on n points with p arcs."""
    return binom(n, p) - binom(n, p - 1)


# ---------------------------------------------------------------------------
# 1.  link states (half-diagrams)
# ---------------------------------------------------------------------------
#
# A link state on n points is a set of arcs (i,j), i<j, pairwise disjoint,
# non-crossing, such that every point strictly inside an arc is itself
# matched.  Unmatched points are "defects".  Represented as a sorted tuple of
# (i,j) pairs, points 0-indexed.


def _noncrossing(arcs):
    for (a, b), (c, d) in combinations(arcs, 2):
        if a < c < b < d or c < a < d < b:
            return False
    return True


def _no_defect_under_arc(arcs, n):
    matched = set()
    for a, b in arcs:
        matched.add(a)
        matched.add(b)
    for a, b in arcs:
        for k in range(a + 1, b):
            if k not in matched:
                return False
    return True


def link_states(n, p):
    """All link states on n points with exactly p arcs, canonically ordered."""
    out = []
    pts = list(range(n))
    for chosen in combinations(pts, 2 * p):
        # all perfect matchings of `chosen`
        for arcs in _perfect_matchings(list(chosen)):
            if not _noncrossing(arcs):
                continue
            if not _no_defect_under_arc(arcs, n):
                continue
            out.append(tuple(sorted(arcs)))
    out.sort()
    return out


def _perfect_matchings(pts):
    if not pts:
        yield ()
        return
    a = pts[0]
    for i in range(1, len(pts)):
        b = pts[i]
        rest = pts[1:i] + pts[i + 1:]
        for m in _perfect_matchings(rest):
            yield ((a, b),) + m


def defects(arcs, n):
    matched = set()
    for a, b in arcs:
        matched.add(a)
        matched.add(b)
    return tuple(i for i in range(n) if i not in matched)


# ---------------------------------------------------------------------------
# 2.  TL diagrams
# ---------------------------------------------------------------------------
#
# A diagram on n strands is a perfect matching of the 2n nodes
#   ('t',0..n-1)  (top)   and   ('b',0..n-1)  (bottom)
# that is non-crossing when the nodes are placed on a circle in the cyclic
# order  t0, t1, ..., t(n-1), b(n-1), ..., b0.
# Represented as a tuple `pair` of length 2n: the partner index of each node
# under the circular indexing above.


def _circle_order(n):
    """node list in cyclic order; index i of this list is the circle position."""
    return [('t', i) for i in range(n)] + [('b', i) for i in range(n - 1, -1, -1)]


def diagrams(n):
    """All Catalan(n) planar diagrams, as frozensets of node-pairs."""
    order = _circle_order(n)
    out = []
    for m in _noncrossing_perfect_matchings(list(range(2 * n))):
        out.append(frozenset(frozenset((order[a], order[b])) for a, b in m))
    # canonical order for reproducibility
    out.sort(key=lambda d: sorted(tuple(sorted(e)) for e in d))
    return out


def _noncrossing_perfect_matchings(positions):
    """Non-crossing perfect matchings of a linearly ordered position list,
    where 'non-crossing' is with respect to that order read as a circle."""
    if not positions:
        yield []
        return
    a = positions[0]
    for i in range(1, len(positions), 2):
        b = positions[i]
        inside = positions[1:i]
        outside = positions[i + 1:]
        for mi in _noncrossing_perfect_matchings(inside):
            for mo in _noncrossing_perfect_matchings(outside):
                yield [(a, b)] + mi + mo


def identity_diagram(n):
    return frozenset(frozenset((('t', i), ('b', i))) for i in range(n))


def generator_diagram(n, i):
    """e_i : cup joining bottom i,i+1 and cap joining top i,i+1 (0-indexed)."""
    edges = [frozenset((('t', i), ('t', i + 1))), frozenset((('b', i), ('b', i + 1)))]
    for k in range(n):
        if k in (i, i + 1):
            continue
        edges.append(frozenset((('t', k), ('b', k))))
    return frozenset(edges)


def _partner_map(d):
    m = {}
    for e in d:
        a, b = tuple(e)
        m[a] = b
        m[b] = a
    return m


def multiply(d1, d2, n):
    """d1 * d2  (d1 stacked ON TOP of d2).  Returns (loops, diagram)."""
    p1 = _partner_map(d1)
    p2 = _partner_map(d2)
    # nodes: ('T',i) = d1 top, ('M',i) = d1 bottom = d2 top, ('B',i) = d2 bottom
    adj = {}

    def link(x, y):
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)

    for i in range(n):
        adj.setdefault(('T', i), [])
        adj.setdefault(('M', i), [])
        adj.setdefault(('B', i), [])
    for e in d1:
        a, b = tuple(e)
        link(('T', a[1]) if a[0] == 't' else ('M', a[1]),
             ('T', b[1]) if b[0] == 't' else ('M', b[1]))
    for e in d2:
        a, b = tuple(e)
        link(('M', a[1]) if a[0] == 't' else ('B', a[1]),
             ('M', b[1]) if b[0] == 't' else ('B', b[1]))

    seen = set()
    loops = 0
    edges = []
    for start in list(adj):
        if start in seen:
            continue
        if start[0] == 'M':
            continue  # start from endpoints (T/B) first
        # walk the path
        seen.add(start)
        cur, prev = start, None
        while True:
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                break
            # a node has degree 1 (T/B) or 2 (M)
            nxt = nxt[0]
            if nxt in seen and nxt[0] != 'M':
                prev, cur = cur, nxt
                seen.add(nxt)
                break
            prev, cur = cur, nxt
            seen.add(cur)
            if cur[0] != 'M':
                break
        edges.append((start, cur))
    # remaining unseen nodes are all 'M' and form closed loops
    for start in list(adj):
        if start in seen:
            continue
        loops += 1
        cur, prev = start, None
        seen.add(start)
        while True:
            nxt = [x for x in adj[cur] if x != prev]
            nxt = [x for x in nxt if x not in seen]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)

    res = []
    for a, b in edges:
        na = ('t', a[1]) if a[0] == 'T' else ('b', a[1])
        nb = ('t', b[1]) if b[0] == 'T' else ('b', b[1])
        res.append(frozenset((na, nb)))
    d = frozenset(res)
    if len(d) != n:
        raise AssertionError("diagram multiply produced %d edges, want %d" % (len(d), n))
    return loops, d


def embed(d, n):
    """TL_{n-1} -> TL_n by adjoining a through-strand at the last position."""
    return frozenset(list(d) + [frozenset((('t', n - 1), ('b', n - 1)))])


# ---------------------------------------------------------------------------
# 3.  the cell module V(n,p) and the diagram action
# ---------------------------------------------------------------------------


def act(d, state, n, p, beta):
    """Diagram d acting on link state `state` (state sits BELOW d).

    Returns (coefficient, new_state) or (0, None) if the number of defects
    drops -- which is zero in the cell module V(n,p).
    """
    adj = {}

    def link(x, y):
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)

    for i in range(n):
        adj.setdefault(('t', i), [])
        adj.setdefault(('b', i), [])
    for e in d:
        a, b = tuple(e)
        link(a, b)
    for a, b in state:
        link(('b', a), ('b', b))

    seen = set()
    loops = 0
    endpoints = []
    # path endpoints are: every 't' node, and every 'b' node that is a defect
    # of `state` (degree 1 in the glued graph)
    starts = [x for x in adj if len(adj[x]) == 1]
    for start in starts:
        if start in seen:
            continue
        seen.add(start)
        cur, prev = start, None
        while True:
            nxt = [x for x in adj[cur] if x != prev]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            seen.add(cur)
            if len(adj[cur]) == 1:
                break
        endpoints.append((start, cur))
    for x in adj:
        if x not in seen:
            loops += 1
            cur, prev = x, None
            seen.add(x)
            while True:
                nxt = [y for y in adj[cur] if y != prev and y not in seen]
                if not nxt:
                    break
                prev, cur = cur, nxt[0]
                seen.add(cur)

    arcs = []
    ndef = 0
    for a, b in endpoints:
        if a[0] == 't' and b[0] == 't':
            arcs.append(tuple(sorted((a[1], b[1]))))
        elif a[0] == 't' or b[0] == 't':
            ndef += 1
        else:
            # a defect of `state` joined to another defect of `state`:
            # the defect count drops.  Zero in the cell module.
            return 0, None
    if ndef != n - 2 * p:
        return 0, None
    new = tuple(sorted(arcs))
    return beta ** loops, new


def gram_entry(u, v, n, p, beta):
    """<u,v> : glue u (reflected) on top of v."""
    adj = {i: [] for i in range(n)}
    for a, b in u:
        adj[a].append(('u', b))
        adj[b].append(('u', a))
    for a, b in v:
        adj[a].append(('v', b))
        adj[b].append(('v', a))
    udef = set(defects(u, n))
    vdef = set(defects(v, n))
    seen = set()
    loops = 0
    for start in range(n):
        if start in seen:
            continue
        if len(adj[start]) == 2:
            continue  # interior of a path or on a cycle; handled below
    # walk paths from every degree<2 node
    for start in range(n):
        if start in seen or len(adj[start]) >= 2:
            continue
        seen.add(start)
        cur, prevlab = start, None
        while True:
            nxt = [(lab, w) for (lab, w) in adj[cur] if lab != prevlab]
            if not nxt:
                break
            lab, w = nxt[0]
            prevlab, cur = lab, w
            seen.add(cur)
            if len(adj[cur]) < 2:
                break
        a, b = start, cur
        # one endpoint must be a u-defect and the other a v-defect
        if not ((a in udef and b in vdef) or (a in vdef and b in udef)):
            return 0
    for start in range(n):
        if start in seen:
            continue
        loops += 1
        cur, prevlab = start, None
        seen.add(start)
        while True:
            nxt = [(lab, w) for (lab, w) in adj[cur] if lab != prevlab and w not in seen]
            if not nxt:
                break
            lab, w = nxt[0]
            prevlab, cur = lab, w
            seen.add(cur)
    return beta ** loops


# ---------------------------------------------------------------------------
# 4.  exact linear algebra over Q
# ---------------------------------------------------------------------------


def rref(mat):
    """Reduced row echelon form.  Returns (R, pivots).  mat is list of lists."""
    m = [[Fraction(x) for x in row] for row in mat]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    piv = []
    r = 0
    for c in range(cols):
        sel = None
        for i in range(r, rows):
            if m[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        m[r], m[sel] = m[sel], m[r]
        pv = m[r][c]
        m[r] = [x / pv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != 0:
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv.append(c)
        r += 1
        if r == rows:
            break
    return m, piv


def rank(mat):
    if not mat or not mat[0]:
        return 0
    return len(rref(mat)[1])


def nullspace(mat, ncols):
    """Basis of {x : mat x = 0}, as a list of column vectors."""
    if not mat:
        return [[Fraction(1) if i == j else Fraction(0) for i in range(ncols)]
                for j in range(ncols)]
    R, piv = rref(mat)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        basis.append(v)
    return basis


def solve_exact(A, b):
    """Solve A x = b exactly.  Returns (solution, unique) or (None, False)."""
    rows = len(A)
    cols = len(A[0]) if rows else 0
    aug = [[Fraction(A[i][j]) for j in range(cols)] + [Fraction(b[i])] for i in range(rows)]
    R, piv = rref(aug)
    if cols in piv:
        return None, False  # inconsistent
    x = [Fraction(0)] * cols
    for i, c in enumerate(piv):
        x[c] = R[i][cols]
    # check
    for i in range(rows):
        s = sum(Fraction(A[i][j]) * x[j] for j in range(cols))
        if s != Fraction(b[i]):
            return None, False
    unique = len(piv) == cols
    return x, unique


def matmul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)] for i in range(n)]


# ---------------------------------------------------------------------------
# 5.  the objects the audit needs
# ---------------------------------------------------------------------------


class TL:
    """Everything about TL_n(beta) that this audit measures."""

    def __init__(self, n, beta):
        self.n = n
        self.beta = beta
        self.parts = list(range(n // 2 + 1))
        self.states = {p: link_states(n, p) for p in self.parts}
        self._gram = {}
        self._null = {}

    def gram(self, p):
        if p not in self._gram:
            S = self.states[p]
            self._gram[p] = [[gram_entry(u, v, self.n, p, self.beta) for v in S] for u in S]
        return self._gram[p]

    def dim_V(self, p):
        return len(self.states[p])

    def dim_L(self, p):
        return rank(self.gram(p)) if self.dim_V(p) else 0

    def vertices(self):
        """The vertex set at level n: [(p, dim L(n,p))] for the non-zero ones."""
        return [(p, self.dim_L(p)) for p in self.parts if self.dim_L(p) > 0]

    def radical_basis(self, p):
        if p not in self._null:
            G = self.gram(p)
            self._null[p] = nullspace(G, self.dim_V(p))
        return self._null[p]

    def action_matrix(self, d, p):
        """Matrix of diagram d (a diagram on n strands) on V(n,p),
        columns indexed by link states."""
        S = self.states[p]
        idx = {s: i for i, s in enumerate(S)}
        M = [[Fraction(0)] * len(S) for _ in S]
        for j, s in enumerate(S):
            c, t = act(d, s, self.n, p, self.beta)
            if c == 0:
                continue
            M[idx[t]][j] = Fraction(c)
        return M

    def trace_on_L(self, d, p):
        """Trace of d acting on L(n,p) = V(n,p)/rad<,>."""
        A = self.action_matrix(d, p)
        N = self.radical_basis(p)
        trV = sum(A[i][i] for i in range(len(A)))
        if not N:
            return trV
        # A * N = N * M  -> solve column by column, N has full column rank
        Ncols = [[N[j][i] for j in range(len(N))] for i in range(self.dim_V(p))]
        # Ncols is dim_V x r
        AN = matmul(A, Ncols)
        M = []
        for j in range(len(N)):
            col = [AN[i][j] for i in range(self.dim_V(p))]
            x, unique = solve_exact(Ncols, col)
            if x is None:
                raise AssertionError(
                    "rad of the Gram form is not invariant under the diagram "
                    "action at n=%d beta=%d p=%d" % (self.n, self.beta, p))
            if not unique:
                raise AssertionError("radical basis is not independent")
            M.append(x)
        trRad = sum(M[j][j] for j in range(len(N)))
        return trV - trRad

    # ---- the regular representation and its trace form -------------------

    def trace_form_rank(self):
        n, beta = self.n, self.beta
        D = diagrams(n)
        idx = {d: i for i, d in enumerate(D)}
        prod = {}
        for a in D:
            for b in D:
                prod[(a, b)] = multiply(a, b, n)
        # tau(x) = trace of left multiplication by x on A
        tau = {}
        for x in D:
            t = 0
            for c in D:
                loops, res = prod[(x, c)]
                if res == c:
                    t += beta ** loops
            tau[x] = t
        M = []
        for a in D:
            row = []
            for b in D:
                loops, res = prod[(a, b)]
                row.append(beta ** loops * tau[res])
            M.append(row)
        return rank(M), len(D)
