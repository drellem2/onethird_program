#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument -- shared core.

Written from scratch for the repair of mg-ebd8 / 714aceb.  Shares no code with
code/landscape_ebd8/ (the target), code/landscape_audit_d673/ (the audit),
code/semigroup_note/, code/face_geometry/, code/unified_gate_8fd1/ or
code/hodge_leverage/.  Pure Python 3, exact integer arithmetic, no third-party
imports.

Posets are carried as a frozenset of STRICT pairs (i, j) meaning i < j in P,
transitively closed, on the ground set {0, ..., n-1}.  Every finite poset has a
linear extension, so every isomorphism class has a NATURALLY LABELLED
representative (i < j in P implies i < j as integers); the enumeration below
walks the transitively closed subsets of {(i, j) : i < j} and then reduces to
isomorphism classes with a canonical form that is a minimum over the FULL S_n
ORBIT -- not min() over a frozenset, the shape that silently returns labelled
counts.  The class counts are certified against A000112 (1, 2, 5, 16, 63, 318)
by the caller.
"""

from itertools import combinations, permutations


# ----------------------------------------------------------------- posets ---

def transitive_closure(n, pairs):
    """Warshall on a strict relation given as a set of pairs."""
    reach = [[False] * n for _ in range(n)]
    for (i, j) in pairs:
        reach[i][j] = True
    for k in range(n):
        rk = reach[k]
        for i in range(n):
            if reach[i][k]:
                ri = reach[i]
                for j in range(n):
                    if rk[j]:
                        ri[j] = True
    return frozenset((i, j) for i in range(n) for j in range(n) if reach[i][j])


def naturally_labelled_posets(n):
    """Every transitively closed subset of {(i,j) : i < j}."""
    ups = list(combinations(range(n), 2))
    seen = set()
    for mask in range(1 << len(ups)):
        pairs = [ups[k] for k in range(len(ups)) if mask >> k & 1]
        rel = transitive_closure(n, pairs)
        if len(rel) == len(pairs):          # already transitively closed
            seen.add(rel)
    return seen


def canonical(n, rel):
    """Minimum over the FULL S_n orbit of the sorted pair list."""
    best = None
    for sigma in permutations(range(n)):
        img = tuple(sorted((sigma[i], sigma[j]) for (i, j) in rel))
        if best is None or img < best:
            best = img
    return best


def iso_classes(n):
    """One naturally labelled representative per isomorphism class."""
    reps = {}
    for rel in naturally_labelled_posets(n):
        c = canonical(n, rel)
        if c not in reps:
            reps[c] = rel
    return [reps[c] for c in sorted(reps)]


def is_connected(n, rel):
    """Connected as an undirected comparability graph."""
    if n == 0:
        return True
    adj = [set() for _ in range(n)]
    for (i, j) in rel:
        adj[i].add(j)
        adj[j].add(i)
    seen = {0}
    stack = [0]
    while stack:
        x = stack.pop()
        for y in adj[x]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == n


def linear_extensions(n, rel):
    """All permutations of [n] (as tuples, position = rank) compatible with P."""
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for p, x in enumerate(perm):
            pos[x] = p
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(perm)
    return out


# ------------------------------------------------------------- partitions ---

def set_partitions(n):
    """All set partitions of [n], each a tuple of frozensets sorted by min."""
    if n == 0:
        return [()]
    out = []

    def rec(i, blocks):
        if i == n:
            out.append(tuple(sorted((frozenset(b) for b in blocks),
                                    key=lambda s: min(s))))
            return
        for k in range(len(blocks)):
            blocks[k].append(i)
            rec(i + 1, blocks)
            blocks[k].pop()
        blocks.append([i])
        rec(i + 1, blocks)
        blocks.pop()

    rec(0, [])
    return out


def ordered_set_partitions(n):
    """All ordered set partitions of [n], as tuples of frozensets."""
    out = []
    for part in set_partitions(n):
        for perm in permutations(part):
            out.append(tuple(perm))
    return out


def blocks_are_antichains(rel, X):
    """Every block of the set partition X is an antichain of P."""
    for B in X:
        for (i, j) in rel:
            if i in B and j in B:
                return False
    return True


def quotient_is_acyclic(rel, X):
    """The quotient digraph on the blocks of X -- edge B -> C when some i in B
    is below some j in C -- has no directed cycle.  Depth-first, no reference
    to Brown, to M_0 or to any block ordering."""
    m = len(X)
    where = {}
    for b, B in enumerate(X):
        for i in B:
            where[i] = b
    succ = [set() for _ in range(m)]
    for (i, j) in rel:
        a, b = where[i], where[j]
        if a != b:
            succ[a].add(b)
    colour = [0] * m                        # 0 white, 1 grey, 2 black

    def dfs(v):
        colour[v] = 1
        for w in succ[v]:
            if colour[w] == 1:
                return False
            if colour[w] == 0 and not dfs(w):
                return False
        colour[v] = 2
        return True

    for v in range(m):
        if colour[v] == 0 and not dfs(v):
            return False
    return True


def meets_the_open_order_cone(rel, X):
    """DOES THE FLAT X MEET THE OPEN CONE U = {x : x_i < x_j for i < j in P}?

    Answered by CONSTRUCTION, with no acyclicity test and no topological sort.
    The flat X is the subspace { x : x_i = x_j whenever i and j share a block },
    so a point of X in U is an assignment of a real value to each block, TIES
    ALLOWED, with value(block i) < value(block j) for every i < j in P.  Any
    such assignment restricts to a weak order on the blocks; refining a weak
    order to a strict total order compatible with it keeps every strict
    inequality, and conversely a strict total order is a special case of a weak
    one.  So X meets U iff SOME TOTAL ORDERING OF THE BLOCKS sends every
    relation of P strictly forwards -- searched exhaustively over all |X|!
    orderings here.  This is the derivation the document asserted, exercised
    directly rather than through its consequence.
    """
    blocks = list(X)
    for order in permutations(range(len(blocks))):
        pos = {}
        for slot, b in enumerate(order):
            for i in blocks[b]:
                pos[i] = slot
        if all(pos[i] < pos[j] for (i, j) in rel):
            return True
    return False


def refines(Y, X):
    """Y refines X: every block of Y sits inside a block of X."""
    for B in Y:
        if not any(B <= C for C in X):
            return False
    return True


def factorial(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def label(X, n=None):
    """ac|bd style label for a set partition."""
    return "|".join("".join(chr(97 + x) for x in sorted(B))
                    for B in sorted(X, key=lambda s: min(s)))


def poset_name(rel):
    cov = sorted(rel)
    return "{" + ", ".join("%s<%s" % (chr(97 + i), chr(97 + j))
                           for (i, j) in cov) + "}" if cov else "{antichain}"
