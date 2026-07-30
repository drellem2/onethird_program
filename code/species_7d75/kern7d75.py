"""Kernel for mg-7d75 -- species / Hopf monoids as the framework behind BOTH
`S_n` representation theory and the poset-quotient story.

Written fresh for this ticket.  It shares no code with `core_af28.py`,
`kern6ad0.py`, `core1953.py`; where it recomputes an object those files also
build (`F(P)`, `AC(P)`), it does so from the geometric definition and the two
routes are cross-checked against each other in `selftest.py`.

CONVENTIONS, stated once because two of them are places this repo has slipped.

  * A poset on `[n]` is `(n, rel)` with `rel` a frozenset of STRICT pairs
    `(i, j)` meaning `i < j` in `P`, transitively closed.
  * The braid cone (Aguiar-Ardila's term) of `P` is
        C(P) = { x in R^n : x_i <= x_j whenever i < j in P }.
    A face of the braid arrangement is a set composition `F = (B_1,...,B_k)`,
    read as `x` constant on each block with value strictly increasing in `r`.
    `F` lies in `C(P)` iff  i < j in P  implies  block(i) <= block(j).
    That set is `F(P)`, and it is exactly the repo's `P`-compatible ordered set
    partitions.
  * The support of a face is its underlying UNORDERED set partition.
    `AC(P) := supp(F(P))` -- and, separately computed, the set partitions of
    `[n]` whose quotient digraph is acyclic.  These two are the same set; that
    equality is a TEST here, not an assumption.
    NOTE: `AC(P)` is NOT the set of flats meeting the OPEN cone.  That smaller
    set additionally requires every block to be an antichain, and conflating
    the two is the error mg-1953 repaired (R1).  Nothing here uses it.

Pure Python 3, exact integer / Fraction arithmetic, no dependencies.
"""

from fractions import Fraction
from itertools import combinations, permutations

# ------------------------------------------------------------------ posets --


def mk_poset(n, pairs):
    """Transitive closure of `pairs`; antisymmetry asserted."""
    rel = set(pairs)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel and a != d:
                    rel.add((a, d))
                    changed = True
    for (a, b) in rel:
        assert a != b and (b, a) not in rel, "not a poset"
    return (n, frozenset(rel))


def all_posets(n):
    """Every LABELLED poset on [n], by closing every antisymmetric digraph.
    Slow and obvious on purpose; n <= 5 only."""
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    seen = {}
    for k in range(len(pairs) + 1):
        for sub in combinations(pairs, k):
            s = set(sub)
            if any((b, a) in s for (a, b) in s):
                continue
            # transitive closure, rejecting cycles
            ok = True
            rel = set(s)
            changed = True
            while changed and ok:
                changed = False
                for (a, b) in list(rel):
                    for (c, d) in list(rel):
                        if b == c and a != d and (a, d) not in rel:
                            rel.add((a, d))
                            changed = True
                        if b == c and a == d:
                            ok = False
                if any((b, a) in rel for (a, b) in rel):
                    ok = False
            if ok:
                seen[frozenset(rel)] = True
    return [(n, r) for r in sorted(seen, key=lambda r: (len(r), sorted(r)))]


def relabel(P, perm):
    n, rel = P
    return (n, frozenset((perm[a], perm[b]) for (a, b) in rel))


def canon(P):
    """Canonical form of the isomorphism class: lexicographically least
    relabelling.  n <= 5, so n! relabellings is affordable."""
    n, _ = P
    best = None
    for perm in permutations(range(n)):
        r = tuple(sorted(relabel(P, perm)[1]))
        if best is None or r < best:
            best = r
    return (n, best)


def poset_classes(n):
    """One representative per isomorphism class."""
    out = {}
    for P in all_posets(n):
        out.setdefault(canon(P), P)
    return [out[k] for k in sorted(out)]


def aut(P):
    """The automorphism group of P, as a list of permutations (tuples)."""
    n, rel = P
    return [perm for perm in permutations(range(n))
            if relabel(P, perm)[1] == rel]


def linear_extensions(P):
    n, rel = P
    out = []
    for perm in permutations(range(n)):
        pos = {v: i for i, v in enumerate(perm)}
        if all(pos[a] < pos[b] for (a, b) in rel):
            out.append(perm)
    return out


# ------------------------------------- set partitions and set compositions --


def set_partitions(n):
    """All set partitions of [n] via restricted growth strings."""
    out = []

    def rec(i, rgs, mx):
        if i == n:
            blocks = {}
            for v, b in enumerate(rgs):
                blocks.setdefault(b, []).append(v)
            out.append(frozenset(frozenset(v) for v in blocks.values()))
            return
        for b in range(mx + 2):
            rec(i + 1, rgs + [b], max(mx, b))
    rec(0, [], -1)
    return out


def set_compositions(n):
    """All set compositions (= faces of the braid arrangement) of [n]."""
    out = []
    for X in set_partitions(n):
        for order in permutations(sorted(X, key=lambda b: (min(b), sorted(b)))):
            out.append(tuple(order))
    return out


def sc_product(F, G):
    """The Tits / left-regular-band product: refine F by G, drop empties."""
    out = []
    for A in F:
        for B in G:
            C = A & B
            if C:
                out.append(C)
    return tuple(out)


def supp(F):
    return frozenset(F)


def sc_restrict(F, S):
    """Restriction of a set composition to a subset S (AM's coproduct)."""
    out = []
    for A in F:
        C = A & S
        if C:
            out.append(C)
    return tuple(out)


def sp_restrict(X, S):
    out = set()
    for A in X:
        C = A & S
        if C:
            out.add(C)
    return frozenset(out)


def sc_concat(F, G):
    """AM's product on set compositions: concatenation."""
    return tuple(F) + tuple(G)


# --------------------------------------------------- the braid cone objects --


def faces_of(P):
    """F(P): the faces of the braid arrangement lying in the braid cone of P."""
    n, rel = P
    out = []
    for F in set_compositions(n):
        idx = {}
        for t, B in enumerate(F):
            for v in B:
                idx[v] = t
        if all(idx[a] <= idx[b] for (a, b) in rel):
            out.append(F)
    return out


def quotient_is_acyclic(rel, X):
    """Does contracting each block of X leave an acyclic digraph on blocks?"""
    blocks = sorted(X, key=lambda b: (min(b), sorted(b)))
    where = {}
    for t, B in enumerate(blocks):
        for v in B:
            where[v] = t
    m = len(blocks)
    succ = [set() for _ in range(m)]
    for (a, b) in rel:
        u, v = where[a], where[b]
        if u != v:
            succ[u].add(v)
    colour = [0] * m

    def dfs(v):
        colour[v] = 1
        for w in succ[v]:
            if colour[w] == 1:
                return False
            if colour[w] == 0 and not dfs(w):
                return False
        colour[v] = 2
        return True

    return all(colour[v] != 0 or dfs(v) for v in range(m))


def AC_by_acyclicity(P):
    """AC(P) as {set partitions whose quotient digraph is acyclic}."""
    n, rel = P
    return sorted((X for X in set_partitions(n) if quotient_is_acyclic(rel, X)),
                  key=_spkey)


def AC_by_support(P):
    """AC(P) as supp(F(P)) -- the support semilattice of the band F(P)."""
    return sorted({supp(F) for F in faces_of(P)}, key=_spkey)


def _spkey(X):
    return (len(X), sorted(sorted(b) for b in X))


# ------------------------------------------------------------------ orbits --


def perm_sp(X, perm):
    return frozenset(frozenset(perm[v] for v in B) for B in X)


def perm_sc(F, perm):
    return tuple(frozenset(perm[v] for v in B) for B in F)


def orbits(items, group, act):
    """Orbits of `group` on `items` under `act`; returns list of frozensets."""
    remaining = set(items)
    out = []
    while remaining:
        x = next(iter(remaining))
        orb = frozenset(act(x, g) for g in group)
        out.append(orb)
        remaining -= orb
    return sorted(out, key=lambda o: (len(o), sorted(map(repr, o))[0]))


# ------------------------------------------------------- integer partitions --


def integer_partitions(n):
    """All partitions of n as weakly decreasing tuples."""
    def rec(m, cap):
        if m == 0:
            yield ()
            return
        for k in range(min(m, cap), 0, -1):
            for rest in rec(m - k, k):
                yield (k,) + rest
    return list(rec(n, n))


def bell(n):
    """Bell numbers by the triangle recursion -- independent of any enumeration."""
    row = [1]
    for _ in range(n):
        nxt = [row[-1]]
        for v in row:
            nxt.append(nxt[-1] + v)
        row = nxt
    return row[0]


def p_count(n):
    """p(n) by the standard partition-counting DP -- independent of the
    `integer_partitions` enumerator above."""
    dp = [0] * (n + 1)
    dp[0] = 1
    for k in range(1, n + 1):
        for m in range(k, n + 1):
            dp[m] += dp[m - k]
    return dp[n]


def compositions(n):
    """All compositions of n as tuples."""
    out = []
    for k in range(1, n + 1):
        for cut in combinations(range(1, n), k - 1):
            pts = (0,) + cut + (n,)
            out.append(tuple(pts[i + 1] - pts[i] for i in range(k)))
    return sorted(out)


# ------------------------------------------------------- exact linear algebra --


def rref(rows, ncols):
    """Reduced row echelon form over Q.  Returns (rows, pivot columns)."""
    M = [list(map(Fraction, r)) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        s = None
        for i in range(r, len(M)):
            if M[i][c] != 0:
                s = i
                break
        if s is None:
            continue
        M[r], M[s] = M[s], M[r]
        inv = M[r][c]
        M[r] = [v / inv for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return [row for row in M[:r]], piv


def rank(rows, ncols):
    return len(rref(rows, ncols)[0])


def nullspace(rows, ncols):
    """Basis of the null space of the matrix with the given rows."""
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
