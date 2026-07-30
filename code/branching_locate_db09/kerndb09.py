"""kerndb09 --- the kernel for mg-db09.

Everything here is built from a published definition and nothing is imported
from another directory in this repo.  Exact arithmetic throughout
(`fractions.Fraction`); no floating point anywhere.

Contents
  * exact linear algebra over Q  (rref / rank / nullspace / solve)
  * "monomial algebras": a finite basis in which the product of two basis
    elements is a SCALAR times a basis element.  Temperley-Lieb diagram
    algebras, group algebras and band algebras are all of this shape, so one
    radical routine serves all three.
  * the radical of a finite-dimensional algebra over Q via the trace form
    (Dickson's theorem, valid in characteristic 0), WITH an independent
    nilpotency verification so the answer never rests on the theorem alone.
  * Temperley-Lieb: planar diagrams, the diagram product, cell (standard)
    modules, the Gram form, and Hom-spaces between restricted modules.
  * symmetric group algebras, centres, and the Gelfand-Tsetlin subalgebra.
  * posets, the faces F(P) of the braid cone of P, and the support
    semilattice AC(P).
"""

from fractions import Fraction
from itertools import permutations, combinations

# --------------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------------


def rref(rows, ncols):
    """Row-reduce a list of lists of Fractions.  Returns (rows, pivots)."""
    M = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                p = i
                break
        if p is None:
            continue
        M[r], M[p] = M[p], M[r]
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


def nullspace(rows, ncols):
    """Basis of {x : M x = 0} for M with `ncols` columns."""
    R, piv = rref(rows, ncols)
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncols
        v[f] = Fraction(1)
        for i, c in enumerate(piv):
            v[c] = -R[i][f]
        basis.append(v)
    return basis


def span_closure(vectors, ncols, products):
    """Smallest subspace containing `vectors` and closed under `products`.

    `products(u, v)` returns the coordinate vector of u*v.  Returns a
    row-reduced basis.
    """
    B, _ = rref([list(v) for v in vectors], ncols)
    changed = True
    while changed:
        changed = False
        new = []
        for u in B:
            for v in B:
                new.append(products(u, v))
        C, _ = rref([list(b) for b in B] + new, ncols)
        if len(C) > len(B):
            B = C
            changed = True
        else:
            B = C
    return B


# --------------------------------------------------------------------------
# monomial algebras
# --------------------------------------------------------------------------


class MonAlg:
    """A finite-dimensional algebra with a basis b_0..b_{m-1} such that
    b_i b_j = c(i,j) * b_{k(i,j)}  (or 0).

    `table[i][j]` is either None (product 0) or a pair (coeff, k).
    """

    def __init__(self, basis, table, name=""):
        self.basis = basis
        self.table = table
        self.dim = len(basis)
        self.name = name

    @staticmethod
    def from_monoid(elements, mult, coeff=None, name=""):
        """`mult(x, y)` returns an element (or None); `coeff(x, y)` a Fraction."""
        idx = {x: i for i, x in enumerate(elements)}
        m = len(elements)
        table = [[None] * m for _ in range(m)]
        for i, x in enumerate(elements):
            for j, y in enumerate(elements):
                z = mult(x, y)
                if z is None:
                    continue
                c = Fraction(1) if coeff is None else coeff(x, y)
                if c != 0:
                    table[i][j] = (c, idx[z])
        return MonAlg(list(elements), table, name)

    def mul_vec(self, u, v):
        out = [Fraction(0)] * self.dim
        for i, a in enumerate(u):
            if a == 0:
                continue
            row = self.table[i]
            for j, b in enumerate(v):
                if b == 0 or row[j] is None:
                    continue
                c, k = row[j]
                out[k] += a * b * c
        return out

    def left_trace(self, k):
        """trace of left multiplication by the basis element b_k."""
        t = Fraction(0)
        for l in range(self.dim):
            e = self.table[k][l]
            if e is not None and e[1] == l:
                t += e[0]
        return t

    def trace_form(self):
        """T[i][j] = tr(L_{b_i b_j}).  Symmetric bilinear form on the algebra."""
        lt = [self.left_trace(k) for k in range(self.dim)]
        T = [[Fraction(0)] * self.dim for _ in range(self.dim)]
        for i in range(self.dim):
            row = self.table[i]
            for j in range(self.dim):
                e = row[j]
                if e is not None:
                    T[i][j] = e[0] * lt[e[1]]
        return T

    def radical(self):
        """rad(A) as a row-reduced basis, via the trace form.

        Dickson: over a field of characteristic 0, rad(A) is the radical of the
        trace form of the regular representation.  We do not take that on
        trust: `verify_radical` below checks the answer is a two-sided ideal
        and is nilpotent, which is the definition.
        """
        T = self.trace_form()
        return nullspace(T, self.dim)

    def verify_radical(self, R, maxpow=40):
        """Return (is_ideal, is_nilpotent, nilpotency_index).

        This is the check that keeps the answer from resting on Dickson's
        theorem: `R` is confirmed to be a two-sided ideal and to be nilpotent,
        which is the definition of a nilpotent ideal, and rad(A) is the largest
        one.
        """
        if not R:
            return True, True, 0
        Rb, piv = rref([list(r) for r in R], self.dim)
        pivset = list(piv)

        def in_span(v):
            w = list(v)
            for i, c in enumerate(pivset):
                if w[c] != 0:
                    f = w[c]
                    row = Rb[i]
                    for j in range(self.dim):
                        if row[j] != 0:
                            w[j] -= f * row[j]
            return all(x == 0 for x in w)

        is_ideal = True
        for r in Rb:
            for i in range(self.dim):
                e = [Fraction(0)] * self.dim
                e[i] = Fraction(1)
                if not in_span(self.mul_vec(e, r)) or not in_span(self.mul_vec(r, e)):
                    is_ideal = False
                    break
            if not is_ideal:
                break
        cur = [list(r) for r in Rb]
        for k in range(1, maxpow + 1):
            nxt = []
            for u in cur:
                for v in Rb:
                    nxt.append(self.mul_vec(u, v))
            C, _ = rref(nxt, self.dim)
            if not C:
                return is_ideal, True, k + 1
            cur = C
        return is_ideal, False, -1

    def semisimple_quotient_dim(self):
        return self.dim - len(self.radical())


# --------------------------------------------------------------------------
# Temperley-Lieb: planar diagrams
# --------------------------------------------------------------------------
#
# A TL_n diagram is a non-crossing perfect matching of 2n points: the top row
# is 0..n-1 (left to right) and the bottom row is n..2n-1 (left to right).
# Around the boundary of the rectangle the cyclic order is
#     0, 1, ..., n-1, 2n-1, 2n-2, ..., n
# so "planar" means "non-crossing in that cyclic order".


def _circle_order(n):
    return list(range(n)) + list(range(2 * n - 1, n - 1, -1))


def tl_diagrams(n):
    """All planar perfect matchings of the 2n points, as tuples m with
    m[i] = partner of i.  Planar means non-crossing in the boundary cyclic
    order 0, 1, ..., n-1, 2n-1, 2n-2, ..., n."""
    res = []
    for pairs in _noncrossing_perfect(_circle_order(n)):
        m = [None] * (2 * n)
        for a, b in pairs:
            m[a] = b
            m[b] = a
        res.append(tuple(m))
    return sorted(set(res))


def _components(adj, nodes):
    """Connected components of an undirected graph, as a list of node sets."""
    seen = set()
    comps = []
    for s in nodes:
        if s in seen:
            continue
        stack = [s]
        comp = set()
        seen.add(s)
        while stack:
            x = stack.pop()
            comp.add(x)
            for y in adj.get(x, []):
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        comps.append(comp)
    return comps


def tl_product(n, a, b):
    """Product a*b, with `a` stacked ON TOP of `b`.  Returns (loops, diagram).

    The bottom row of `a` is glued to the top row of `b`; closed cycles in the
    glued picture are the loops, each contributing a factor of beta.
    """
    adj = {}

    def link(x, y):
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)

    for i in range(2 * n):
        if i < a[i]:
            link(('a', i), ('a', a[i]))
        if i < b[i]:
            link(('b', i), ('b', b[i]))
    for k in range(n):
        link(('a', n + k), ('b', k))
    label = {}
    for i in range(n):
        label[('a', i)] = i
    for k in range(n):
        label[('b', n + k)] = n + k
    nodes = [('a', i) for i in range(2 * n)] + [('b', i) for i in range(2 * n)]
    m = [None] * (2 * n)
    loops = 0
    for comp in _components(adj, nodes):
        ends = sorted(label[x] for x in comp if x in label)
        if not ends:
            loops += 1
            continue
        assert len(ends) == 2, (a, b, comp)
        m[ends[0]] = ends[1]
        m[ends[1]] = ends[0]
    return loops, tuple(m)


def tl_algebra(n, beta):
    """TL_n(beta) as a MonAlg over Q.  beta must be a Fraction/int."""
    beta = Fraction(beta)
    diags = tl_diagrams(n)
    idx = {d: i for i, d in enumerate(diags)}
    m = len(diags)
    table = [[None] * m for _ in range(m)]
    for i, a in enumerate(diags):
        for j, b in enumerate(diags):
            loops, d = tl_product(n, a, b)
            c = beta ** loops
            if c != 0:
                table[i][j] = (c, idx[d])
    return MonAlg(diags, table, name="TL_%d(%s)" % (n, beta))


# ---- cell (standard) modules of TL --------------------------------------
#
# A link state on n points with p arcs (and d = n - 2p defects) is a
# non-crossing partial matching in which no arc encloses a defect.


def _noncrossing_perfect(free):
    """All non-crossing perfect matchings of the ordered list `free`."""
    if not free:
        return [[]]
    acc = []
    a = free[0]
    for k in range(1, len(free), 2):
        b = free[k]
        for L in _noncrossing_perfect(free[1:k]):
            for R in _noncrossing_perfect(free[k + 1:]):
                acc.append([(a, b)] + L + R)
    return acc


def link_states(n, p):
    """All (n, p) link states: non-crossing partial matchings of 0..n-1 with
    exactly p arcs, no arc enclosing a defect.  Returned as tuples t with
    t[i] = partner of i, or -1 if i is a defect."""
    out = []

    def rec(pts, arcs):
        if len(arcs) > p:
            return
        if not pts:
            if len(arcs) == p:
                t = [-1] * n
                for a, b in arcs:
                    t[a] = b
                    t[b] = a
                out.append(tuple(t))
            return
        # pts[0] is a defect ...
        rec(pts[1:], arcs)
        # ... or opens an arc, with everything strictly inside matched inside
        a = pts[0]
        for k in range(1, len(pts)):
            b = pts[k]
            inner = pts[1:k]
            if len(inner) % 2 != 0:
                continue
            if len(arcs) + 1 + len(inner) // 2 > p:
                continue
            for im in _noncrossing_perfect(inner):
                rec(pts[k + 1:], arcs + [(a, b)] + im)

    rec(list(range(n)), [])
    return sorted(set(out))


def tl_gen_action(n, p, beta, i, state):
    """u_i acting on a link state (0-based: u_i joins i and i+1).

    Returns (coeff, state) or None for 0 (a drop in the number of defects).
    """
    beta = Fraction(beta)
    t = list(state)
    a, b = t[i], t[i + 1]
    if a == i + 1:
        return (beta, tuple(t))
    if a == -1 and b == -1:
        return None  # defect count would drop
    t[i] = i + 1
    t[i + 1] = i
    if a != -1 and b != -1:
        t[a] = b
        t[b] = a
    elif a != -1:
        t[a] = -1
    else:
        t[b] = -1
    return (Fraction(1), tuple(t))


def tl_cell_matrices(n, p, beta):
    """Matrices of u_0..u_{n-2} on the cell module V_{n,p}.  Row-vector free:
    M[i] is a dim x dim matrix acting on coordinate column vectors."""
    states = link_states(n, p)
    idx = {s: i for i, s in enumerate(states)}
    d = len(states)
    mats = []
    for i in range(n - 1):
        M = [[Fraction(0)] * d for _ in range(d)]
        for s, j in idx.items():
            r = tl_gen_action(n, p, beta, i, s)
            if r is None:
                continue
            c, s2 = r
            M[idx[s2]][j] += c
        mats.append(M)
    return states, mats


def tl_gram(n, p, beta):
    """Gram matrix of the canonical bilinear form on V_{n,p}."""
    beta = Fraction(beta)
    states = link_states(n, p)
    d = len(states)
    G = [[Fraction(0)] * d for _ in range(d)]
    for i, u in enumerate(states):
        for j, v in enumerate(states):
            G[i][j] = _glue(n, u, v, beta)
    return states, G


def _glue(n, u, v, beta):
    """<u, v>: reflect u and glue it on top of v.

    The value is beta^(number of closed loops) if every defect of u is joined
    to a defect of v, and 0 otherwise (a drop in the number of through-lines).
    """
    adj = {}

    def link(x, y):
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(x)

    for i in range(n):
        if u[i] != -1 and i < u[i]:
            link(('u', i), ('u', u[i]))
        if v[i] != -1 and i < v[i]:
            link(('v', i), ('v', v[i]))
        link(('u', i), ('v', i))
    nodes = [('u', i) for i in range(n)] + [('v', i) for i in range(n)]
    defects = set(('u', i) for i in range(n) if u[i] == -1) | \
              set(('v', i) for i in range(n) if v[i] == -1)
    loops = 0
    for comp in _components(adj, nodes):
        ends = sorted(x for x in comp if x in defects)
        if not ends:
            loops += 1
            continue
        if len(ends) != 2 or ends[0][0] == ends[1][0]:
            return Fraction(0)
    return Fraction(beta) ** loops


def hom_dim(matsA, matsB, dA, dB):
    """dim Hom(M_A, M_B) for modules given by the SAME list of generators.

    Solves phi * A_i = B_i * phi for phi a dB x dA matrix.
    """
    nvar = dA * dB
    rows = []
    for A, B in zip(matsA, matsB):
        for r in range(dB):
            for c in range(dA):
                row = [Fraction(0)] * nvar
                # (phi A)_{r,c} = sum_k phi[r][k] A[k][c]
                for k in range(dA):
                    if A[k][c] != 0:
                        row[r * dA + k] += A[k][c]
                # (B phi)_{r,c} = sum_k B[r][k] phi[k][c]
                for k in range(dB):
                    if B[r][k] != 0:
                        row[k * dA + c] -= B[r][k]
                if any(x != 0 for x in row):
                    rows.append(row)
    return nvar - rank(rows, nvar)


def restrict_cell(n, p, beta):
    """V_{n,p} restricted to TL_{n-1}: the same space, generators u_0..u_{n-3}."""
    states, mats = tl_cell_matrices(n, p, beta)
    return states, mats[:n - 2]


# --------------------------------------------------------------------------
# symmetric groups, centres, Gelfand-Tsetlin algebras
# --------------------------------------------------------------------------


def sym_group(n):
    return [tuple(p) for p in permutations(range(n))]


def perm_mul(a, b):
    """(a*b)(i) = a(b(i))."""
    return tuple(a[b[i]] for i in range(len(a)))


def group_algebra(n):
    els = sym_group(n)
    return MonAlg.from_monoid(els, lambda x, y: perm_mul(x, y), name="CS_%d" % n)


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    ct = []
    for i in range(n):
        if seen[i]:
            continue
        l = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = p[j]
            l += 1
        ct.append(l)
    return tuple(sorted(ct, reverse=True))


def embed(p, k, n):
    """S_k -> S_n fixing k..n-1."""
    return tuple(list(p) + list(range(k, n)))


def class_sums(k, n, els_index):
    """Coordinate vectors (in CS_n) of the conjugacy class sums of S_k."""
    by = {}
    for p in sym_group(k):
        by.setdefault(cycle_type(p), []).append(embed(p, k, n))
    out = []
    for ct in sorted(by):
        v = [Fraction(0)] * len(els_index)
        for g in by[ct]:
            v[els_index[g]] += 1
        out.append(v)
    return out


def gz_algebra(chain, n):
    """The GZ subalgebra of CS_n generated by the centres of CS_k, k in chain."""
    A = group_algebra(n)
    idx = {g: i for i, g in enumerate(A.basis)}
    gens = []
    for k in chain:
        gens.extend(class_sums(k, n, idx))
    B = span_closure(gens, A.dim, A.mul_vec)
    return A, B


def centralizer(A, subspace):
    """{x in A : x s = s x for all s in `subspace`}, as a basis."""
    rows = []
    for s in subspace:
        cols = []
        for c in range(A.dim):
            e = [Fraction(0)] * A.dim
            e[c] = Fraction(1)
            u = A.mul_vec(e, s)
            v = A.mul_vec(s, e)
            cols.append([a - b for a, b in zip(u, v)])
        for r in range(A.dim):
            row = [cols[c][r] for c in range(A.dim)]
            if any(x != 0 for x in row):
                rows.append(row)
    return nullspace(rows, A.dim)


def is_commutative_subspace(A, basis):
    for u in basis:
        for v in basis:
            if A.mul_vec(u, v) != A.mul_vec(v, u):
                return False
    return True


# --------------------------------------------------------------------------
# posets, faces of the braid cone, support semilattice
# --------------------------------------------------------------------------


def mk_poset(n, pairs):
    """Reflexive-transitive closure as a frozenset of strict pairs."""
    rel = set(pairs)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel and a != d:
                    rel.add((a, d))
                    changed = True
    return (n, frozenset(rel))


def all_posets(n):
    """All labelled posets on [n], as (n, frozenset) pairs."""
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    seen = set()
    out = []
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            rel = set(sub)
            # transitively closed and antisymmetric and irreflexive?
            ok = True
            for (a, b) in rel:
                if (b, a) in rel:
                    ok = False
                    break
            if not ok:
                continue
            cl = True
            for (a, b) in rel:
                for (c, d) in rel:
                    if b == c and a != d and (a, d) not in rel:
                        cl = False
                        break
                if not cl:
                    break
            if not cl:
                continue
            f = frozenset(rel)
            if f in seen:
                continue
            seen.add(f)
            out.append((n, f))
    return out


def poset_classes(n):
    """One representative per isomorphism class."""
    reps = {}
    for P in all_posets(n):
        best = None
        for s in permutations(range(n)):
            img = frozenset((s[a], s[b]) for (a, b) in P[1])
            key = tuple(sorted(img))
            if best is None or key < best:
                best = key
        if best not in reps:
            reps[best] = P
    return list(reps.values())


def faces_of(P):
    """F(P): ordered set partitions (B_1,...,B_k) of [n] with i <_P j implying
    block(i) <= block(j).  These are the faces of the braid arrangement lying
    in the cone C(P) = {x : x_i <= x_j whenever i <_P j}."""
    n, rel = P
    out = []

    def rec(remaining, blocks):
        if not remaining:
            out.append(tuple(blocks))
            return
        rem = sorted(remaining)
        for r in range(1, len(rem) + 1):
            for B in combinations(rem, r):
                Bs = set(B)
                rest = remaining - Bs
                # no element of `rest` may be strictly below an element of B
                ok = True
                for b in B:
                    for c in rest:
                        if (c, b) in rel:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    rec(rest, blocks + [frozenset(B)])

    rec(frozenset(range(n)), [])
    return sorted(out, key=lambda F: (len(F), [sorted(b) for b in F]))


def tits(F, G):
    """The Tits product: refine F by G, dropping empty intersections."""
    out = []
    for B in F:
        for C in G:
            I = B & C
            if I:
                out.append(I)
    return tuple(out)


def supp(F):
    """The underlying (unordered) set partition."""
    return frozenset(F)


def quotient_acyclic(P, X):
    """Is the quotient of P by the set partition X acyclic?"""
    n, rel = P
    blocks = list(X)
    where = {}
    for i, B in enumerate(blocks):
        for x in B:
            where[x] = i
    m = len(blocks)
    adj = [[False] * m for _ in range(m)]
    for (a, b) in rel:
        if where[a] != where[b]:
            adj[where[a]][where[b]] = True
    # transitive closure, look for a loop
    for k in range(m):
        for i in range(m):
            if adj[i][k]:
                for j in range(m):
                    if adj[k][j]:
                        adj[i][j] = True
    return not any(adj[i][i] for i in range(m))


def set_partitions(n):
    out = []

    def rec(i, blocks):
        if i == n:
            out.append(frozenset(frozenset(b) for b in blocks))
            return
        for b in blocks:
            b.append(i)
            rec(i + 1, blocks)
            b.pop()
        blocks.append([i])
        rec(i + 1, blocks)
        blocks.pop()

    rec(0, [])
    return out


def AC_by_acyclicity(P):
    n, rel = P
    return sorted((sorted(sorted(b) for b in X) for X in set_partitions(n)
                   if quotient_acyclic(P, X)))


def AC_by_support(P):
    return sorted(sorted(sorted(b) for b in supp(F)) for F in faces_of(P))


def band_algebra(P):
    F = faces_of(P)
    return MonAlg.from_monoid(F, lambda x, y: tits(x, y), name="kF(P)")


# --------------------------------------------------------------------------
# Mobius function of a finite poset given by a <= relation
# --------------------------------------------------------------------------


def mobius(elements, leq):
    """mu(x, y) for a finite poset, as a dict."""
    els = list(elements)
    order = sorted(range(len(els)),
                   key=lambda i: sum(1 for j in range(len(els))
                                     if leq(els[j], els[i])))
    mu = {}
    for xi in order:
        for yi in order:
            x, y = els[xi], els[yi]
            if not leq(x, y):
                continue
            if x == y:
                mu[(xi, yi)] = 1
            else:
                s = 0
                for zi in order:
                    z = els[zi]
                    if leq(x, z) and leq(z, y) and z != y:
                        s += mu.get((xi, zi), 0)
                mu[(xi, yi)] = -s
    return mu


def algebra_generated(A, gens, include_unit=True):
    """The unital subalgebra of A generated by `gens` (coordinate vectors).

    Closes the span under RIGHT multiplication by the generators, which is
    enough: the subalgebra is the span of all words in the generators.
    """
    start = []
    if include_unit:
        u = unit_vector(A)
        if u is not None:
            start.append(u)
    start.extend([list(g) for g in gens])
    B, _ = rref(start, A.dim)
    while True:
        new = [A.mul_vec(b, g) for b in B for g in gens]
        C, _ = rref([list(b) for b in B] + new, A.dim)
        if len(C) == len(B):
            return C
        B = C


def unit_vector(A):
    """The identity of A as a coordinate vector, if one basis element is it."""
    for k in range(A.dim):
        ok = True
        for l in range(A.dim):
            e = A.table[k][l]
            f = A.table[l][k]
            if e is None or e != (Fraction(1), l) or f is None or f != (Fraction(1), l):
                ok = False
                break
        if ok:
            v = [Fraction(0)] * A.dim
            v[k] = Fraction(1)
            return v
    return None
