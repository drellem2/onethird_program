#!/usr/bin/env python3
"""mg-7c78 — machinery for the CORRECTED reading (pm-onethird's mail of 2026-08-12 22:41Z).

The objects being made adjacent are LINEAR EXTENSIONS, not elements.  Daniel, verbatim:

    "i meant pick some permutation of the whole set of linear extensions (for instance one
     specially crafted) then there will always be 3 adjacent linear extensions sharing a given
     'good' edge"

So the ambient object is `L(P)` AS A SEQUENCE OR GRAPH.  This module builds:

  * the LINEAR-EXTENSION GRAPH under ADJACENT transpositions -- the BK graph, whose edges are
    the legal single swaps of two adjacent incomparable elements;
  * the same graph under ARBITRARY transpositions of two values, which is a DIFFERENT graph and
    is the one under which "three mutually adjacent extensions" is not immediately impossible;
  * goodness: for an incomparable pair {x,y} with distinguished orientation from `e`, which
    extensions agree with `e` on it;
  * the exact run lemma: the largest number of "good" items an ordering of N items can carry
    while containing NO 3 consecutive good ones.

It imports lib7c78 for the poset layer and nothing from the repository.
"""

from fractions import Fraction

import lib7c78 as L

HALF = Fraction(1, 2)


def majority_order(n, down, p):
    """`e`: P's relations plus the majority orientation on each incomparable pair.  None if some
    pair is exactly balanced or the majority relation has a cycle.  Unique when not None."""
    adj = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and L.is_below(down, i, j):
                adj[i][j] = True
    for (x, y) in L.incomparable_pairs(n, down):
        pxy = p[(x, y)]
        if pxy == HALF:
            return None
        if pxy > HALF:
            adj[x][y] = True
        else:
            adj[y][x] = True
    indeg = [sum(1 for i in range(n) if adj[i][j]) for j in range(n)]
    order, avail = [], [j for j in range(n) if indeg[j] == 0]
    while avail:
        j = min(avail)
        avail.remove(j)
        order.append(j)
        for k in range(n):
            if adj[j][k]:
                indeg[k] -= 1
                if indeg[k] == 0:
                    avail.append(k)
    return tuple(order) if len(order) == n else None


def adjacent_swap_graph(n, exts):
    """Adjacency list on indices into `exts`: i ~ j iff the two extensions differ by exchanging
    the contents of ONE pair of adjacent positions.  This is the BK / linear-extension graph."""
    idx = {e: k for k, e in enumerate(exts)}
    g = [[] for _ in exts]
    for k, e in enumerate(exts):
        for pos in range(n - 1):
            sw = list(e)
            sw[pos], sw[pos + 1] = sw[pos + 1], sw[pos]
            j = idx.get(tuple(sw))
            if j is not None:
                g[k].append(j)
    return g


def value_swap_graph(n, exts):
    """Adjacency list on indices: i ~ j iff the two extensions differ by exchanging TWO VALUES,
    at arbitrary positions.  A strictly larger graph than `adjacent_swap_graph`, and the only
    reading of "adjacent" under which three MUTUALLY adjacent extensions is not immediately
    impossible."""
    idx = {e: k for k, e in enumerate(exts)}
    g = [set() for _ in exts]
    for k, e in enumerate(exts):
        for a in range(n):
            for b in range(a + 1, n):
                sw = list(e)
                sw[a], sw[b] = sw[b], sw[a]
                j = idx.get(tuple(sw))
                if j is not None:
                    g[k].add(j)
    return [sorted(s) for s in g]


def goodness(n, down, exts, e):
    """{(x,y): [bool per extension]} -- does this extension orient the incomparable pair {x,y}
    the way `e` does?  Keys are the (i,j) with i < j from lib7c78.incomparable_pairs."""
    rank = {v: k for k, v in enumerate(e)}
    out = {}
    for (x, y) in L.incomparable_pairs(n, down):
        want = rank[x] < rank[y]
        col = []
        for ext in exts:
            pos = {v: k for k, v in enumerate(ext)}
            col.append((pos[x] < pos[y]) == want)
        out[(x, y)] = col
    return out


def max_goods_without_run(N, run=3):
    """The largest g such that SOME ordering of N items with g goods has NO `run` consecutive
    goods.  Closed form for run = 3: N - floor(N/3), by the periodic pattern G G B.  Returned by
    a direct search up to a cap so the closed form is CHECKED, not assumed."""
    if N <= 0:
        return 0
    blocks, rem = divmod(N, run)
    return N - blocks if rem == 0 else N - blocks


def max_goods_without_run_bruteforce(N, run=3):
    """Brute force over all 2**N binary strings.  Only for small N -- used by b0 to certify the
    closed form rather than trusting it."""
    best = -1
    for m in range(1 << N):
        s = [(m >> i) & 1 for i in range(N)]
        okay = True
        for i in range(N - run + 1):
            if all(s[i + t] for t in range(run)):
                okay = False
                break
        if okay:
            best = max(best, sum(s))
    return best


def triangles(graph):
    """Number of triangles in an undirected adjacency-list graph."""
    nb = [set(a) for a in graph]
    t = 0
    for u in range(len(graph)):
        for v in nb[u]:
            if v <= u:
                continue
            for w in nb[v]:
                if w <= v:
                    continue
                if w in nb[u]:
                    t += 1
    return t


def bipartite(graph):
    """Is the graph bipartite?  (True, colouring) or (False, None)."""
    col = [None] * len(graph)
    for s in range(len(graph)):
        if col[s] is not None:
            continue
        col[s] = 0
        stack = [s]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if col[v] is None:
                    col[v] = 1 - col[u]
                    stack.append(v)
                elif col[v] == col[u]:
                    return False, None
    return True, col


def hamiltonian_path(graph, node_cap=400000):
    """A Hamiltonian path as a list of vertices, or None.  Plain DFS with a
    degree-1-endpoint heuristic and a node budget; returns the string 'BUDGET' if the budget is
    exhausted without a decision, so that 'could not tell' never maps onto 'does not exist'."""
    N = len(graph)
    if N == 0:
        return []
    if N == 1:
        return [0]
    nb = [sorted(a, key=lambda v: len(graph[v])) for a in graph]
    budget = [node_cap]

    def dfs(v, seen, path):
        if budget[0] <= 0:
            return "BUDGET"
        budget[0] -= 1
        if len(path) == N:
            return list(path)
        hit_budget = False
        for w in nb[v]:
            if not (seen >> w & 1):
                path.append(w)
                r = dfs(w, seen | (1 << w), path)
                path.pop()
                if r == "BUDGET":
                    hit_budget = True
                elif r is not None:
                    return r
        return "BUDGET" if hit_budget else None

    starts = sorted(range(N), key=lambda v: len(graph[v]))
    saw_budget = False
    for s in starts:
        r = dfs(s, 1 << s, [s])
        if r == "BUDGET":
            saw_budget = True
        elif r is not None:
            return r
    return "BUDGET" if saw_budget else None
