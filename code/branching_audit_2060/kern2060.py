"""kern2060 --- the audit kernel for mg-2060.

Written from definitions for this audit.  It imports nothing from
`code/branching_locate_db09` (the audited instrument) or from any other
directory in this repo.  Where it recomputes an object the audited
instrument also builds --- Temperley-Lieb diagrams, cell modules, the
radical, F(P), AC(P) --- the construction here is written independently
and the agreement (or disagreement) is the measurement.

Conventions, stated because they are where this subject goes wrong:

* `TL_n(beta)` has the DIAGRAM basis: planar perfect matchings of 2n
  boundary points.  Multiplication is stacking; each closed loop
  contributes a factor `beta`.  `beta` is an integer here, so all the
  linear algebra is exact over Q.
* A LINK STATE on n points is a non-crossing partial matching in which no
  arc covers an unmatched point.  Unmatched points are DEFECTS.  A link
  state with `p` arcs has `n - 2p` defects.  `V(n,p)` is the standard
  (cell) module spanned by the link states with p arcs.  This indexing ---
  p = number of ARCS --- is the audited document's, kept so the tables can
  be compared row for row.
* The TL bilinear form on `V(n,p)`: glue u to v; the value is
  `beta^(#closed loops)` when every open path runs from a defect of u to a
  defect of v, and 0 when some path joins two defects of the same side.
* `L(n,p) := V(n,p) / rad<,>` (Graham-Lehrer).  The NON-ZERO `L(n,p)` are
  the simple modules; they are the VERTICES of the branching graph of the
  tower.  This is the definition the audit uses, and it is not the same
  object as the set of cell modules.
* `F(P)` is the set of ordered set partitions of [n] compatible with P,
  under the Tits product.  `AC(P)` is the set of underlying (unordered)
  set partitions.
"""

from fractions import Fraction
from itertools import combinations, permutations

# --------------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------------


def rref(rows, ncols):
    """Reduced row echelon form over Q.  Returns (rows, pivot_columns)."""
    M = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        sel = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        inv = Fraction(1, 1) / M[r][c]
        M[r] = [x * inv for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[0])


def rank_bounded(rows, ncols, expect=None):
    """Rank by elimination that stops as soon as the rest of the matrix is
    zero.  Cost is O(rank * size), not O(ncols * size), which is what makes
    the 541 x 541 trace form of kF(antichain_5) reachable."""
    M = [list(r) for r in rows]
    nrows = len(M)
    r = 0
    for c in range(ncols):
        if r == nrows:
            break
        sel = None
        for i in range(r, nrows):
            if M[i][c] != 0:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        pr = M[r]
        inv = Fraction(1, 1) / pr[c]
        pr = [x * inv for x in pr]
        M[r] = pr
        for i in range(nrows):
            if i != r:
                f = M[i][c]
                if f:
                    Mi = M[i]
                    M[i] = [a - f * b for a, b in zip(Mi, pr)]
        r += 1
    return r


def nullspace(rows, ncols):
    """A basis of the right nullspace of the matrix with the given rows."""
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    out = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        out.append(v)
    return out


def mat_mul(A, B):
    n, m, p = len(A), len(B), len(B[0])
    Bt = list(zip(*B))
    return [[sum(A[i][k] * Bt[j][k] for k in range(m)) for j in range(p)]
            for i in range(n)]


def mat_inv(A):
    n = len(A)
    M = [list(A[i]) + [Fraction(1) if i == j else Fraction(0)
                       for j in range(n)] for i in range(n)]
    R, piv = rref(M, n)
    assert piv == list(range(n)), "singular matrix"
    return [row[n:] for row in R]


def solve_exact(cols, target):
    """Solve sum_j x_j * cols[j] = target over Q.  Returns the (unique)
    solution and a flag saying whether it is unique."""
    m = len(target)
    k = len(cols)
    aug = [[cols[j][i] for j in range(k)] + [target[i]] for i in range(m)]
    R, piv = rref(aug, k + 1)
    if k in piv:
        return None, False           # inconsistent
    x = [Fraction(0)] * k
    for i, c in enumerate(piv):
        x[c] = R[i][k]
    unique = len(piv) == k
    return x, unique


# --------------------------------------------------------------------------
# a finite-dimensional algebra with a basis in which products are
# scalar * basis element (Temperley-Lieb, group algebras, band algebras)
# --------------------------------------------------------------------------


class ScalarBasisAlgebra:
    """basis b_0..b_{d-1}; b_i b_j = coef * b_k."""

    def __init__(self, basis, mult, name=""):
        self.basis = list(basis)
        self.index = {b: i for i, b in enumerate(self.basis)}
        self.name = name
        d = len(self.basis)
        self.dim = d
        self.table = [[None] * d for _ in range(d)]
        for i, x in enumerate(self.basis):
            for j, y in enumerate(self.basis):
                c, z = mult(x, y)
                self.table[i][j] = (c, self.index[z])

    def left_mult_trace(self, i):
        """trace of left multiplication by b_i on the regular module."""
        t = Fraction(0)
        for j in range(self.dim):
            c, k = self.table[i][j]
            if k == j:
                t += c
        return t

    def trace_form(self):
        """T[i][j] = tr(L_{b_i b_j}).  Dickson: over a field of
        characteristic 0 the radical of this form IS rad(A)."""
        tr = [self.left_mult_trace(i) for i in range(self.dim)]
        T = [[None] * self.dim for _ in range(self.dim)]
        for i in range(self.dim):
            row = T[i]
            ti = self.table[i]
            for j in range(self.dim):
                c, k = ti[j]
                row[j] = c * tr[k]
        return T

    def radical_dim(self):
        return self.dim - rank_bounded(self.trace_form(), self.dim)

    def radical_basis(self):
        return nullspace(self.trace_form(), self.dim)

    def is_two_sided_nilpotent_ideal(self, vecs, max_power=40):
        """Verify, without using Dickson, that the span of `vecs` is a
        two-sided ideal and is nilpotent."""
        d = self.dim
        if not vecs:
            return True, True
        R, piv = rref(vecs, d)

        def in_span(v):
            w = list(v)
            for i, c in enumerate(piv):
                if w[c] != 0:
                    f = w[c]
                    w = [a - f * b for a, b in zip(w, R[i])]
            return all(x == 0 for x in w)

        def act(v, i, side):
            out = [Fraction(0)] * d
            for j, a in enumerate(v):
                if a == 0:
                    continue
                c, k = (self.table[i][j] if side == 'L' else self.table[j][i])
                out[k] += a * c
            return out

        ideal = True
        for v in R:
            for i in range(d):
                if not in_span(act(v, i, 'L')) or not in_span(act(v, i, 'R')):
                    ideal = False
                    break
            if not ideal:
                break

        cur = [list(v) for v in R]
        nilpotent = False
        for _ in range(max_power):
            nxt = []
            for v in cur:
                for w in R:
                    p = [Fraction(0)] * d
                    for j, a in enumerate(v):
                        if a == 0:
                            continue
                        for l, b in enumerate(w):
                            if b == 0:
                                continue
                            c, k = self.table[j][l]
                            p[k] += a * b * c
                    nxt.append(p)
            NR, _ = rref(nxt, d)
            if not NR:
                nilpotent = True
                break
            cur = NR
        return ideal, nilpotent


# --------------------------------------------------------------------------
# Temperley-Lieb: diagrams, link states, cell modules, the bilinear form
# --------------------------------------------------------------------------


def _noncrossing_matchings(points):
    """All non-crossing perfect matchings of an ordered list of points."""
    if not points:
        return [()]
    out = []
    a = points[0]
    for i in range(1, len(points), 2):
        b = points[i]
        for L in _noncrossing_matchings(points[1:i]):
            for Rm in _noncrossing_matchings(points[i + 1:]):
                out.append(((a, b),) + L + Rm)
    return out


def tl_diagrams(n):
    """Planar perfect matchings of 2n points.  Top points are 0..n-1 read
    left to right; bottom points are n..2n-1 read left to right.  The
    circular order that makes 'planar' mean 'non-crossing' is the top row
    left to right followed by the bottom row RIGHT to left."""
    circle = list(range(n)) + list(range(2 * n - 1, n - 1, -1))
    out = []
    for m in _noncrossing_matchings(circle):
        out.append(tuple(sorted(tuple(sorted(p)) for p in m)))
    return sorted(set(out))


def _uf_find(par, x):
    while par[x] != x:
        par[x] = par[par[x]]
        x = par[x]
    return x


def tl_mult(n):
    """Return a multiplication function on tl_diagrams(n): stacking, with
    beta^loops.  The factor is returned as an exponent so the caller can
    substitute any beta."""
    def mult(a, b):
        # points: 0..n-1  top of a ; n..2n-1  middle (a's bottom = b's top) ;
        # 2n..3n-1  bottom of b.
        par = list(range(3 * n))
        for (x, y) in a:                          # a's labels are already
            ra, rb = _uf_find(par, x), _uf_find(par, y)   # 0..2n-1
            if ra != rb:
                par[ra] = rb
        for (x, y) in b:                          # b's labels shift by n
            ra, rb = _uf_find(par, x + n), _uf_find(par, y + n)
            if ra != rb:
                par[ra] = rb
        ends = list(range(n)) + list(range(2 * n, 3 * n))
        seen = {}
        pairs = []
        for e in ends:
            r = _uf_find(par, e)
            if r in seen:
                pairs.append((seen[r], e))
                del seen[r]
            else:
                seen[r] = e
        assert not seen, "dangling endpoint"
        touched = set(_uf_find(par, e) for e in ends)
        comps = set(_uf_find(par, i) for i in range(n, 2 * n))
        loops = len(comps - touched)
        res = tuple(sorted(tuple(sorted((x if x < n else x - n,
                                         y if y < n else y - n)))
                           for (x, y) in pairs))
        return loops, res
    return mult


def tl_algebra(n, beta):
    """TL_n(beta) as a ScalarBasisAlgebra over Q."""
    D = tl_diagrams(n)
    raw = tl_mult(n)
    beta = Fraction(beta)

    def mult(a, b):
        loops, res = raw(a, b)
        return beta ** loops, res
    return ScalarBasisAlgebra(D, mult, name="TL_%d(%s)" % (n, beta))


def link_states(n, p):
    """Link states on n points with p arcs, as sorted tuples of arcs.

    Generated as bracket words: a word over {'(', ')', '|'} of length n in
    which the brackets are balanced and every '|' (a DEFECT) sits at
    nesting depth 0.  'Depth 0' is exactly the condition that no arc covers
    a defect, and it is what makes the count the Catalan-triangle number
    C(n,p) - C(n,p-1)."""
    out = []

    def rec(i, depth, opened, stack, arcs):
        if i == n:
            if depth == 0 and opened == p:
                out.append(tuple(sorted(arcs)))
            return
        # a defect, only at depth 0
        if depth == 0:
            rec(i + 1, 0, opened, stack, arcs)
        # open an arc
        if opened < p:
            rec(i + 1, depth + 1, opened + 1, stack + [i], arcs)
        # close an arc
        if depth > 0:
            rec(i + 1, depth - 1, opened, stack[:-1],
                arcs + [(stack[-1], i)])

    rec(0, 0, 0, [], [])
    return sorted(set(tuple(sorted(tuple(sorted(a)) for a in s))
                      for s in out))


def tl_cell_module(n, p, beta):
    """Matrices for the action of every diagram of TL_n on V(n,p), in the
    link-state basis.  A diagram acts by stacking below the link state;
    the result is 0 if the number of defects drops."""
    beta = Fraction(beta)
    S = link_states(n, p)
    idx = {s: i for i, s in enumerate(S)}
    D = tl_diagrams(n)
    m = len(S)
    mats = {}
    for d in D:
        M = [[Fraction(0)] * m for _ in range(m)]
        for j, s in enumerate(S):
            # points 0..n-1 : diagram top ; n..2n-1 : diagram bottom = link
            # state points.  Result lives on the diagram's TOP row.
            par = list(range(2 * n))
            for (x, y) in d:
                ra, rb = _uf_find(par, x), _uf_find(par, y)
                if ra != rb:
                    par[ra] = rb
            for (x, y) in s:
                ra, rb = _uf_find(par, x + n), _uf_find(par, y + n)
                if ra != rb:
                    par[ra] = rb
            top = list(range(n))
            seen = {}
            arcs = []
            defects = []
            for e in top:
                r = _uf_find(par, e)
                if r in seen:
                    arcs.append(tuple(sorted((seen[r], e))))
                    del seen[r]
                else:
                    seen[r] = e
            # remaining tops are connected to defect points of s (or to
            # each other through the middle, already handled)
            sdef = [q for q in range(n) if all(q not in a for a in s)]
            defroots = set(_uf_find(par, q + n) for q in sdef)
            for r, e in list(seen.items()):
                if r in defroots:
                    defects.append(e)
                    del seen[r]
            assert not seen, "dangling top point"
            if len(defects) != n - 2 * p:
                continue                    # defects annihilated -> 0
            touched = set(_uf_find(par, e) for e in top)
            comps = set(_uf_find(par, i) for i in range(n, 2 * n))
            loops = len(comps - touched)
            res = tuple(sorted(arcs))
            if res not in idx:
                continue
            M[idx[res]][j] += beta ** loops
        mats[d] = M
    return S, mats


def tl_gram(n, p, beta):
    """The TL bilinear form on V(n,p), in the link-state basis."""
    beta = Fraction(beta)
    S = link_states(n, p)
    m = len(S)
    G = [[Fraction(0)] * m for _ in range(m)]
    for i, u in enumerate(S):
        udef = set(q for q in range(n) if all(q not in a for a in u))
        for j, v in enumerate(S):
            vdef = set(q for q in range(n) if all(q not in a for a in v))
            par = list(range(n))
            deg = [0] * n
            for (x, y) in u:
                deg[x] += 1
                deg[y] += 1
                ra, rb = _uf_find(par, x), _uf_find(par, y)
                if ra != rb:
                    par[ra] = rb
            for (x, y) in v:
                deg[x] += 1
                deg[y] += 1
                ra, rb = _uf_find(par, x), _uf_find(par, y)
                if ra != rb:
                    par[ra] = rb
            comp = {}
            for q in range(n):
                comp.setdefault(_uf_find(par, q), []).append(q)
            ok = True
            loops = 0
            for r, pts in comp.items():
                ends = [q for q in pts if deg[q] <= 1]
                if not ends:
                    loops += 1
                    continue
                if len(ends) == 1:
                    # an isolated point: a defect of u AND of v; a
                    # through-line of length zero.
                    a = b = ends[0]
                else:
                    assert len(ends) == 2, "not a path"
                    a, b = ends
                # each open path must run from a u-defect to a v-defect
                if not ((a in udef and b in vdef) or (a in vdef and b in udef)):
                    ok = False
                    break
            if ok:
                G[i][j] = beta ** loops
    return S, G


# --------------------------------------------------------------------------
# simple modules of TL_n(beta) and their characters
# --------------------------------------------------------------------------


def tl_simples(n, beta):
    """For each p, the character of L(n,p) = V(n,p)/rad<,> as a function on
    the diagram basis of TL_n.  Returns a list of (p, dim, character dict).
    L(n,p) is dropped when the form is identically zero (dim 0)."""
    D = tl_diagrams(n)
    out = []
    for p in range(0, n // 2 + 1):
        S = link_states(n, p)
        if not S:
            continue
        _, G = tl_gram(n, p, beta)
        m = len(S)
        R = nullspace(G, m)                 # radical of the form
        r = len(R)
        if m - r == 0:
            out.append((p, 0, None))
            continue
        _, mats = tl_cell_module(n, p, beta)
        # basis: radical first, then standard vectors completing it
        RR, piv = rref(R, m) if R else ([], [])
        cols = [list(v) for v in RR]
        free = [c for c in range(m) if c not in piv]
        for c in free:
            e = [Fraction(0)] * m
            e[c] = Fraction(1)
            cols.append(e)
        B = [[cols[j][i] for j in range(m)] for i in range(m)]
        Binv = mat_inv(B)
        chi = {}
        for d in D:
            M = mats[d]
            Mp = mat_mul(Binv, mat_mul(M, B))
            chi[d] = sum(Mp[i][i] for i in range(r, m))
        out.append((p, m - r, chi))
    return out


def tl_subalgebra_embedding(n):
    """TL_{n-1} -> TL_n: add a through strand at the last position."""
    emb = {}
    for d in tl_diagrams(n - 1):
        pairs = []
        for (x, y) in d:
            xx = x if x < n - 1 else x + 1
            yy = y if y < n - 1 else y + 1
            pairs.append(tuple(sorted((xx, yy))))
        pairs.append((n - 1, 2 * n - 1))
        emb[d] = tuple(sorted(tuple(sorted(p)) for p in pairs))
    return emb


# --------------------------------------------------------------------------
# posets, F(P), AC(P)
# --------------------------------------------------------------------------


def all_posets(n):
    """All partial orders on [n] as (n, frozenset of strict pairs)."""
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    out = []
    seen = set()
    for mask in range(1 << len(pairs)):
        rel = set(pairs[k] for k in range(len(pairs)) if mask >> k & 1)
        bad = False
        for (a, b) in rel:
            if (b, a) in rel:
                bad = True
                break
        if bad:
            continue
        # transitivity
        ok = True
        for (a, b) in rel:
            for (c, d) in rel:
                if b == c and a != d and (a, d) not in rel:
                    ok = False
                    break
            if not ok:
                break
        if not ok:
            continue
        f = frozenset(rel)
        if f in seen:
            continue
        seen.add(f)
        out.append((n, f))
    return out


def poset_classes(n):
    reps = {}
    for P in all_posets(n):
        best = None
        for s in permutations(range(n)):
            key = tuple(sorted((s[a], s[b]) for (a, b) in P[1]))
            if best is None or key < best:
                best = key
        reps.setdefault(best, P)
    return list(reps.values())


def faces(P):
    """Ordered set partitions (B_1,...,B_k) of [n] such that no element of a
    later block is strictly below an element of an earlier one."""
    n, rel = P
    out = []

    def rec(remaining, blocks):
        if not remaining:
            out.append(tuple(blocks))
            return
        rem = sorted(remaining)
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                Bs = frozenset(B)
                rest = remaining - Bs
                if any((c, b) in rel for b in B for c in rest):
                    continue
                rec(rest, blocks + [Bs])

    rec(frozenset(range(n)), [])
    return sorted(out, key=lambda F: (len(F), [sorted(b) for b in F]))


def tits(F, G):
    out = []
    for B in F:
        for C in G:
            I = B & C
            if I:
                out.append(I)
    return tuple(out)


def support(F):
    return frozenset(F)


def AC(P):
    return sorted(set(support(F) for F in faces(P)),
                  key=lambda X: sorted(sorted(b) for b in X))


def band_algebra(P):
    F = faces(P)
    return ScalarBasisAlgebra(F, lambda x, y: (Fraction(1), tits(x, y)),
                              name="kF(P)")


def antichain(n):
    return (n, frozenset())


def chain(n):
    return (n, frozenset((i, j) for i in range(n) for j in range(n) if i < j))
