"""kerna61f -- the audit kernel for mg-a61f.

Independent of code/species_7d75/ (kern7d75.py, hopf7d75.py) and of
core_af28.py / kern6ad0.py / core1953.py.  Nothing is imported from any of
them.  Where an object is also built there, it is built here by a DIFFERENT
route so that agreement is evidence and disagreement is a finding:

  * posets are enumerated by a THREE-WAY CHOICE PER UNORDERED PAIR
    (incomparable / a<b / b<a) followed by a transitivity test, not by
    iterating over subsets of the ordered pairs;
  * the radical is computed from the TRACE FORM (Dickson: over a field of
    characteristic 0 the Jacobson radical of a finite-dimensional
    associative algebra is the radical of the bilinear form
    B(x,y) = tr(L_{xy})).  mg-7d75 states explicitly that it used "no trace
    form"; using one is the point of this file.  Ranks are taken modulo two
    different large primes and must agree.
  * set partitions and set compositions are built by recursive insertion,
    not by iterating over ordered set partitions.

Conventions, all fixed here so that every a*.py script shares them:

  poset            frozenset of ordered pairs (a,b) meaning a < b; strict,
                   transitively closed, irreflexive, antisymmetric.
  set composition  tuple of disjoint nonempty frozensets covering the ground
                   set.  This is a FACE of the braid arrangement.
  face of P        set composition whose block-index map is weakly increasing
                   along every relation of P; equivalently a face of the
                   braid arrangement lying in the cone
                   C(P) = { x : x_a <= x_b whenever a < b in P }.
  Tits product     F.G = the nonempty blocks F_i & G_j ordered by (i, j).
  AC(P)            { supp(F) : F a face of P } = the set partitions of the
                   ground set whose quotient digraph is acyclic.
"""

from itertools import product as _iproduct, permutations, combinations

# ---------------------------------------------------------------------------
# posets
# ---------------------------------------------------------------------------


def posets_labelled(n):
    """Every partial order on range(n), by a three-way choice per pair."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    for choice in _iproduct((0, 1, 2), repeat=len(pairs)):
        rel = set()
        for c, (i, j) in zip(choice, pairs):
            if c == 1:
                rel.add((i, j))
            elif c == 2:
                rel.add((j, i))
        if _transitive(rel):
            out.append(frozenset(rel))
    return out


def _transitive(rel):
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c:
                if a == d or (a, d) not in rel:
                    return False
    return True


def relabel(rel, perm):
    """perm is a dict or a sequence: element -> element."""
    return frozenset((perm[a], perm[b]) for (a, b) in rel)


def canonical(rel, n):
    """Lexicographically least relabelling; the isomorphism-class key."""
    best = None
    for p in permutations(range(n)):
        r = tuple(sorted(relabel(rel, p)))
        if best is None or r < best:
            best = r
    return best


def iso_classes(n):
    """One representative per isomorphism class of poset on range(n)."""
    seen = {}
    for rel in posets_labelled(n):
        k = canonical(rel, n)
        if k not in seen:
            seen[k] = frozenset(k)
    return [seen[k] for k in sorted(seen)]


def iso_classes_6_from_5():
    """Isomorphism classes on 6 points, built by adjoining a MAXIMAL element.

    Every poset on 6 points has a maximal element x; deleting it leaves a
    poset on 5 points, and x sits above exactly a down-set of that poset.  So
    ranging over (5-point class, down-set) covers every 6-point class.  This
    route never enumerates the 130023 labelled posets on [6].
    """
    seen = {}
    base = iso_classes(5)
    for rel in base:
        for D in _down_sets(rel, 5):
            new = set(rel)
            for d in D:
                new.add((d, 5))
            new = frozenset(new)
            k = canonical(new, 6)
            if k not in seen:
                seen[k] = frozenset(k)
    return [seen[k] for k in sorted(seen)]


def _down_sets(rel, n):
    out = []
    for m in range(1 << n):
        S = frozenset(i for i in range(n) if m >> i & 1)
        if all(a in S for (a, b) in rel if b in S):
            out.append(S)
    return out


def aut(rel, n):
    """The automorphism group of the poset, as a list of tuples."""
    return [p for p in permutations(range(n)) if relabel(rel, p) == rel]


# ---------------------------------------------------------------------------
# set partitions and set compositions
# ---------------------------------------------------------------------------


def set_partitions(S):
    S = sorted(S)
    if not S:
        return [frozenset()]
    x, rest = S[0], S[1:]
    out = []
    for p in set_partitions(rest):
        blocks = list(p)
        out.append(frozenset(blocks + [frozenset([x])]))
        for i in range(len(blocks)):
            q = list(blocks)
            q[i] = q[i] | frozenset([x])
            out.append(frozenset(q))
    return out


def set_compositions(S):
    """Ordered set partitions, by recursive insertion of the least element."""
    S = sorted(S)
    if not S:
        return [()]
    x, rest = S[0], S[1:]
    out = []
    for c in set_compositions(rest):
        for i in range(len(c)):
            q = list(c)
            q[i] = q[i] | frozenset([x])
            out.append(tuple(q))
        for i in range(len(c) + 1):
            out.append(c[:i] + (frozenset([x]),) + c[i:])
    return out


def supp(F):
    return frozenset(F)


def tits(F, G):
    """Refine F by G: blocks F_i & G_j in the order (i, j)."""
    out = []
    for B in F:
        for C in G:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


def concat(F, G):
    return tuple(F) + tuple(G)


def restrict_comp(F, S):
    return tuple(B & S for B in F if B & S)


def restrict_part(X, S):
    return frozenset(B & S for B in X if B & S)


def restrict_poset(rel, S):
    return frozenset((a, b) for (a, b) in rel if a in S and b in S)


def is_lower_set(rel, S):
    return all(a in S for (a, b) in rel if b in S)


# ---------------------------------------------------------------------------
# faces of a braid cone, and AC(P)
# ---------------------------------------------------------------------------


def faces(rel, ground):
    """Set compositions of `ground` lying in the braid cone of `rel`."""
    out = []
    for F in set_compositions(ground):
        idx = {}
        for t, B in enumerate(F):
            for v in B:
                idx[v] = t
        if all(idx[a] <= idx[b] for (a, b) in rel):
            out.append(F)
    return out


def quotient_acyclic(rel, X):
    """Is the quotient digraph of `rel` by the partition X acyclic?"""
    blocks = sorted(X, key=lambda b: sorted(b))
    idx = {}
    for t, B in enumerate(blocks):
        for v in B:
            idx[v] = t
    m = len(blocks)
    adj = [set() for _ in range(m)]
    for (a, b) in rel:
        if idx[a] != idx[b]:
            adj[idx[a]].add(idx[b])
    indeg = [0] * m
    for u in range(m):
        for v in adj[u]:
            indeg[v] += 1
    stack = [u for u in range(m) if indeg[u] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    return seen == m


def AC_by_support(rel, ground):
    return {supp(F) for F in faces(rel, ground)}


def AC_by_acyclicity(rel, ground):
    return {X for X in set_partitions(ground) if quotient_acyclic(rel, X)}


# ---------------------------------------------------------------------------
# orbits
# ---------------------------------------------------------------------------


def act_comp(F, perm):
    return tuple(frozenset(perm[v] for v in B) for B in F)


def act_part(X, perm):
    return frozenset(frozenset(perm[v] for v in B) for B in X)


def orbits(objs, group, action):
    objs = list(objs)
    index = {o: i for i, o in enumerate(objs)}
    seen = [False] * len(objs)
    out = []
    for i, o in enumerate(objs):
        if seen[i]:
            continue
        orb = set()
        for g in group:
            x = action(o, g)
            if x not in index:
                return None            # the group does not preserve the set
            orb.add(x)
        for x in orb:
            seen[index[x]] = True
        out.append(frozenset(orb))
    return out


# ---------------------------------------------------------------------------
# exact linear algebra: rank over F_p, and null spaces over Q
# ---------------------------------------------------------------------------

P1 = (1 << 31) - 1          # 2147483647, prime
P2 = 1000003                # prime


def rank_mod(rows, ncols, p):
    """Rank of an integer matrix modulo the prime p.  rows is a list of lists."""
    m = [[x % p for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c]:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = pow(m[r][c], p - 2, p)
        m[r] = [(x * inv) % p for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                f = m[i][c]
                m[i] = [(a - f * b) % p for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


def rank_two_primes(rows, ncols):
    """(rank mod P1, rank mod P2).  Equal ranks are the evidence of exactness."""
    return rank_mod(rows, ncols, P1), rank_mod(rows, ncols, P2)


def nullspace_q(rows, ncols):
    """Exact null space over Q of an integer matrix, as a list of Fraction rows."""
    from fractions import Fraction
    m = [[Fraction(x) for x in r] for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c]:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        f = m[r][c]
        m[r] = [x / f for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                g = m[i][c]
                m[i] = [a - g * b for a, b in zip(m[i], m[r])]
        pivots.append(c)
        r += 1
        if r == len(m):
            break
    free = [c for c in range(ncols) if c not in pivots]
    basis = []
    for fc in free:
        v = [Fraction(0)] * ncols
        v[fc] = Fraction(1)
        for i, pc in enumerate(pivots):
            v[pc] = -m[i][fc]
        basis.append(v)
    return basis


def rank_q(rows, ncols):
    from fractions import Fraction
    m = [[Fraction(x) for x in r] for r in rows]
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(m)):
            if m[i][c]:
                piv = i
                break
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        f = m[r][c]
        m[r] = [x / f for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c]:
                g = m[i][c]
                m[i] = [a - g * b for a, b in zip(m[i], m[r])]
        r += 1
        if r == len(m):
            break
    return r


# ---------------------------------------------------------------------------
# the face algebra kF(P), its invariants, and the trace-form radical
# ---------------------------------------------------------------------------


def face_algebra(rel, ground):
    """Returns (basis, index, product table as a list of lists of indices)."""
    B = faces(rel, ground)
    idx = {F: i for i, F in enumerate(B)}
    tab = [[idx[tits(F, G)] for G in B] for F in B]
    return B, idx, tab


def trace_vector(tab):
    """t[c] = tr(L_{e_c}) = #{ h : c.h = h }."""
    n = len(tab)
    return [sum(1 for h in range(n) if tab[c][h] == h) for c in range(n)]


def gram_full(tab):
    """B(e_f, e_g) = tr(L_{e_f . e_g}) = t[ f.g ]."""
    t = trace_vector(tab)
    return [[t[tab[f][g]] for g in range(len(tab))] for f in range(len(tab))]


def invariant_structure_constants(B, idx, tab, group):
    """Orbit sums of the G-action on the faces, and their structure constants.

    Returns (orbs, C, closed) where orbs is the list of orbits (as frozensets
    of basis indices), C[a][b] is a dict {c: coefficient} and `closed` is True
    iff every product of orbit sums really is constant on orbits (so that the
    orbit sums span a subalgebra).
    """
    orbs = orbits(B, group, act_comp)
    if orbs is None:
        return None, None, False
    orbs = [frozenset(idx[F] for F in o) for o in orbs]
    where = {}
    for a, o in enumerate(orbs):
        for i in o:
            where[i] = a
    C = []
    closed = True
    for a, oa in enumerate(orbs):
        row = []
        for b, ob in enumerate(orbs):
            counts = {}
            for i in oa:
                for j in ob:
                    k = tab[i][j]
                    counts[k] = counts.get(k, 0) + 1
            # must be constant on orbits
            agg = {}
            for k, v in counts.items():
                c = where[k]
                agg.setdefault(c, {})[k] = v
            coef = {}
            for c, d in agg.items():
                vals = set(d.values())
                if len(vals) != 1 or len(d) != len(orbs[c]):
                    closed = False
                coef[c] = next(iter(vals))
            row.append(coef)
        C.append(row)
    return orbs, C, closed


def gram_invariant(C):
    """Trace form of the invariant algebra in the orbit-sum basis."""
    m = len(C)
    t = [0] * m
    for c in range(m):
        # tr(L_{O_c}) = sum_a coefficient of O_a in O_c . O_a
        t[c] = sum(C[c][a].get(a, 0) for a in range(m))
    G = [[0] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            G[a][b] = sum(v * t[c] for c, v in C[a][b].items())
    return G
