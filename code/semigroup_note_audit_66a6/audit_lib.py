"""Independent rebuild of the objects in docs/OneThird-Semigroup-Walk-Family-Note.md.

Written for the mg-66a6 audit.  Shares NO code with code/semigroup_note/ (the
artefact under audit), nor with code/face_geometry/ or code/hodge_leverage/.
Everything is rebuilt from the definitions as they are stated in the note, in
exact arithmetic (int / Fraction).  Pure Python 3, no dependencies.

Conventions used throughout:
  * elements are 0..n-1
  * a poset is (n, frozenset of strict pairs (i,j) meaning i < j), transitively
    closed and irreflexive
  * an ORDERING (= linear extension = chamber) is a tuple w with w[position] =
    element, in which every element precedes everything above it
  * a MOVE (= face) is a tuple of frozensets (B_1,...,B_k) partitioning the
    elements, such that i<j in P implies index(B containing i) <= index(B
    containing j)
  * the LEVEL (= support) of a move is the frozenset of its blocks
"""

from fractions import Fraction
from itertools import permutations, combinations


# --------------------------------------------------------------------------
# posets
# --------------------------------------------------------------------------

def poset(n, rels):
    """Transitive closure of `rels`; asserts it is a strict partial order."""
    R = set(rels)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(R):
            for (c, d) in list(R):
                if b == c and (a, d) not in R:
                    R.add((a, d))
                    changed = True
    for (a, b) in R:
        assert a != b, "not irreflexive"
        assert (b, a) not in R, "not antisymmetric"
    return (n, frozenset(R))


def induced(P, S):
    """Induced subposet on the set S, relabelled to 0..|S|-1 by sorted order."""
    n, R = P
    els = sorted(S)
    pos = {e: i for i, e in enumerate(els)}
    return (len(els), frozenset((pos[a], pos[b]) for (a, b) in R
                                if a in pos and b in pos))


def orderings(P):
    """All linear extensions, sorted."""
    n, R = P
    out = []
    for w in permutations(range(n)):
        at = {e: i for i, e in enumerate(w)}
        if all(at[a] < at[b] for (a, b) in R):
            out.append(w)
    return out


def n_orderings(P):
    return len(orderings(P))


# --------------------------------------------------------------------------
# moves
# --------------------------------------------------------------------------

def ordered_set_partitions(els):
    """All ordered set partitions of the iterable `els` (as tuples of
    frozensets): choose the first block as any non-empty subset, recurse on the
    rest."""
    allels = tuple(sorted(els))
    if not allels:
        yield ()
        return
    for size in range(1, len(allels) + 1):
        for B in combinations(allels, size):
            Bs = set(B)
            remaining = [e for e in allels if e not in Bs]
            for tail in ordered_set_partitions(remaining):
                yield (frozenset(B),) + tail


def is_compatible(P, x):
    """P-compatibility: i<j in P => block-index(i) <= block-index(j)."""
    n, R = P
    where = {}
    for i, B in enumerate(x):
        for e in B:
            where[e] = i
    return all(where[a] <= where[b] for (a, b) in R)


def moves(P):
    n, R = P
    return [x for x in ordered_set_partitions(range(n)) if is_compatible(P, x)]


def act(x, c):
    """x . c : elements of B_1 first (in their c-order), then B_2, ..."""
    pos = {e: i for i, e in enumerate(c)}
    out = []
    for B in x:
        out.extend(sorted(B, key=lambda e: pos[e]))
    return tuple(out)


def product(x, y):
    """x . y : blocks are the non-empty B_i & C_j, ordered lexicographically by
    (i, j).  The single move that does y first, then x."""
    out = []
    for B in x:
        for C in y:
            Z = B & C
            if Z:
                out.append(Z)
    return tuple(out)


def level(x):
    return frozenset(x)


def levels(P):
    return sorted({level(x) for x in moves(P)}, key=_lkey)


def _lkey(X):
    return (len(X), sorted(tuple(sorted(B)) for B in X))


def lstr(X):
    """'ac|bd' style rendering with a,b,c,... for 0,1,2,..., blocks sorted."""
    names = "abcdefgh"
    blocks = sorted(("".join(names[e] for e in sorted(B)) for B in X))
    return "|".join(blocks)


def mstr(x):
    names = "abcdefgh"
    return "(" + "|".join("".join(names[e] for e in sorted(B)) for B in x) + ")"


# --------------------------------------------------------------------------
# partitions and the acyclic-quotient description
# --------------------------------------------------------------------------

def set_partitions(els):
    els = tuple(sorted(els))
    if not els:
        yield frozenset()
        return
    first, rest = els[0], els[1:]
    for p in set_partitions(rest):
        pl = list(p)
        for i in range(len(pl)):
            q = pl[:i] + [pl[i] | {first}] + pl[i + 1:]
            yield frozenset(q)
        yield frozenset(pl + [frozenset({first})])


def quotient_acyclic(P, X):
    """Contract each block of X to a point, keep induced arrows between
    DISTINCT blocks, demand no directed cycle."""
    n, R = P
    blocks = list(X)
    idx = {}
    for i, B in enumerate(blocks):
        for e in B:
            idx[e] = i
    adj = {i: set() for i in range(len(blocks))}
    for (a, b) in R:
        if idx[a] != idx[b]:
            adj[idx[a]].add(idx[b])
    # cycle detection by DFS colouring
    colour = {}

    def dfs(u):
        colour[u] = 1
        for v in adj[u]:
            if colour.get(v) == 1:
                return False
            if colour.get(v, 0) == 0 and not dfs(v):
                return False
        colour[u] = 2
        return True

    return all(colour.get(u, 0) != 0 or dfs(u) for u in adj)


def acyclic_partitions(P):
    n, R = P
    return sorted((X for X in set_partitions(range(n)) if quotient_acyclic(P, X)),
                  key=_lkey)


# --------------------------------------------------------------------------
# refinement, multiplicities, eigenvalues
# --------------------------------------------------------------------------

def refines(Y, X):
    """Y refines X: every block of Y sits inside some block of X.
    (Y finer or equal; X coarser or equal.)"""
    return all(any(B <= C for C in X) for B in Y)


def multiplicities(P, lv=None):
    """m_X solved from  sum_{Y refines X} m_Y = prod_{B in X} |L(P|_B)| ,
    finest level first."""
    if lv is None:
        lv = levels(P)
    lv = sorted(lv, key=lambda X: -len(X))          # finest (most blocks) first
    m = {}
    for X in lv:
        rhs = 1
        for B in X:
            rhs *= n_orderings(induced(P, B))
        s = sum(m[Y] for Y in m if refines(Y, X))
        m[X] = rhs - s
    return m


def eigenvalue(P, w, X, mv=None):
    """lambda_X = total weight of moves whose level is COARSER THAN OR EQUAL to
    X, i.e. of moves y with  X refines level(y)."""
    if mv is None:
        mv = moves(P)
    tot = Fraction(0)
    for y in mv:
        if w.get(y, 0) and refines(X, level(y)):
            tot += w[y]
    return tot


def transition_matrix(P, w, ords=None, mv=None):
    """M[i][j] = P(j -> i) = sum of w(x) over x with x . ord_j = ord_i."""
    if ords is None:
        ords = orderings(P)
    if mv is None:
        mv = moves(P)
    idx = {c: i for i, c in enumerate(ords)}
    m = len(ords)
    M = [[Fraction(0)] * m for _ in range(m)]
    for x in mv:
        wx = w.get(x, 0)
        if not wx:
            continue
        for j, c in enumerate(ords):
            M[idx[act(x, c)]][j] += wx
    return M


# --------------------------------------------------------------------------
# exact linear algebra over Q
# --------------------------------------------------------------------------

def rank_Q(rows):
    """Rank of a list of lists of Fractions, by fraction-free-ish elimination."""
    rows = [list(map(Fraction, r)) for r in rows]
    if not rows:
        return 0
    ncols = len(rows[0])
    r = 0
    for col in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][col]
        for i in range(r + 1, len(rows)):
            if rows[i][col] != 0:
                f = rows[i][col] / pv
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def nullity(M):
    return len(M[0]) - rank_Q(M)


def sub_scalar(M, lam):
    return [[M[i][j] - (lam if i == j else 0) for j in range(len(M))]
            for i in range(len(M))]


def mat_vec(M, v):
    return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]


# --------------------------------------------------------------------------
# the adjacent-transposition graph, signs
# --------------------------------------------------------------------------

def at_graph(P, ords=None):
    """Adjacency of the adjacent-transposition graph on L(P): swap two adjacent
    POSITIONS, keep the edge iff the result is again a linear extension."""
    if ords is None:
        ords = orderings(P)
    idx = {c: i for i, c in enumerate(ords)}
    m = len(ords)
    A = [[0] * m for _ in range(m)]
    for c in ords:
        i = idx[c]
        for t in range(len(c) - 1):
            v = list(c)
            v[t], v[t + 1] = v[t + 1], v[t]
            v = tuple(v)
            if v in idx:
                A[i][idx[v]] = 1
    return A


def at_laplacian(P, ords=None):
    A = at_graph(P, ords)
    m = len(A)
    return [[(sum(A[i]) if i == j else 0) - A[i][j] for j in range(m)]
            for i in range(m)]


def inversions(w):
    return sum(1 for i in range(len(w)) for j in range(i + 1, len(w))
               if w[i] > w[j])


def sgn(w):
    return -1 if inversions(w) % 2 else 1


def connected(A):
    m = len(A)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in range(m):
            if A[u][v] and v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == m


# --------------------------------------------------------------------------
# labelled posets and isomorphism classes
# --------------------------------------------------------------------------

def all_labelled_posets(n):
    """Every strict partial order on {0..n-1}, by brute force over the
    3^C(n,2) antisymmetric relations (each unordered pair is unrelated, i<j, or
    j<i), keeping the transitive ones."""
    up = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = []
    total = 3 ** len(up)
    for code in range(total):
        c = code
        R = set()
        for (i, j) in up:
            d = c % 3
            c //= 3
            if d == 1:
                R.add((i, j))
            elif d == 2:
                R.add((j, i))
        ok = True
        for (a, b) in R:
            for (x, y) in R:
                if b == x and (a, y) not in R:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append((n, frozenset(R)))
    return out


def canon(P):
    """Canonical form under relabelling: min over all permutations of the
    SORTED TUPLE of relation pairs (a tuple order, i.e. total -- not the
    frozenset subset order, which is only partial)."""
    n, R = P
    best = None
    for p in permutations(range(n)):
        key = tuple(sorted((p[a], p[b]) for (a, b) in R))
        if best is None or key < best:
            best = key
    return (n, best)


def iso_classes(n):
    seen = {}
    for P in all_labelled_posets(n):
        c = canon(P)
        if c not in seen:
            seen[c] = P
    return [seen[c] for c in sorted(seen)]
