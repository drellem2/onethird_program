#!/usr/bin/env python3
"""
mg-8fd1, L2: is the lattice of acyclic partitions (= poset quotients) of P
preserved by the symmetric group for any poset other than antichains and chains?

Everything here is built from scratch -- no import from code/hodge_leverage/.
A partition pi of [n] is ACYCLIC for P iff the induced digraph on the blocks
(an arrow B -> B' whenever some a in B is <_P some b in B') has no directed
cycle among distinct blocks; equivalently iff the quotient P/pi is a poset.

We compute, for every isomorphism class of poset at n = 1..6:

  AC(P)   the set of acyclic partitions
  G(P)    = { sigma in S_n : sigma . AC(P) = AC(P) }, a subgroup of S_n
  D(P)    = { sigma in S_n : sigma.P = P or sigma.P = P^op }, the "obvious"
            subgroup contained in G(P) (acyclicity is arrow-reversal invariant)

and report the population with G(P) = S_n.
"""

import sys
from itertools import permutations, combinations

# --------------------------------------------------------------------------
# posets, as frozensets of strict pairs (a,b) meaning a <_P b
# --------------------------------------------------------------------------


def is_transitive(rel):
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def naturally_labelled_posets(n):
    """All strict orders on [n] for which 0<1<...<n-1 is a linear extension.
    Every poset is isomorphic to at least one of these."""
    pairs = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(pairs)):
        rel = frozenset(p for i, p in enumerate(pairs) if (mask >> i) & 1)
        if is_transitive(rel):
            out.append(rel)
    return out


def relabel_poset(rel, sigma):
    return frozenset((sigma[a], sigma[b]) for (a, b) in rel)


def dual(rel):
    return frozenset((b, a) for (a, b) in rel)


def canonical(rel, n, perms):
    return min(tuple(sorted(relabel_poset(rel, s))) for s in perms)


def iso_classes(n):
    perms = list(permutations(range(n)))
    seen = {}
    for rel in naturally_labelled_posets(n):
        c = canonical(rel, n, perms)
        if c not in seen:
            seen[c] = frozenset(rel)
    return [seen[c] for c in sorted(seen)]


# --------------------------------------------------------------------------
# set partitions of [n], as frozensets of bitmasks
# --------------------------------------------------------------------------


def set_partitions(n):
    out = []

    def rec(i, blocks):
        if i == n:
            out.append(frozenset(blocks))
            return
        for j in range(len(blocks)):
            b = list(blocks)
            b[j] |= (1 << i)
            rec(i + 1, b)
        rec(i + 1, list(blocks) + [1 << i])

    rec(0, [])
    return out


def acyclic(rel, part):
    """No directed cycle among distinct blocks. Independent of lrb.py:
    we close the block digraph transitively and look for a self-loop."""
    blocks = sorted(part)
    idx = {}
    for i, B in enumerate(blocks):
        for x in range(64):
            if (B >> x) & 1:
                idx[x] = i
    k = len(blocks)
    reach = [0] * k
    for (a, b) in rel:
        if idx[a] != idx[b]:
            reach[idx[a]] |= (1 << idx[b])
    # Floyd-Warshall style transitive closure on the bitmask adjacency
    for m in range(k):
        bit = 1 << m
        for i in range(k):
            if reach[i] & bit:
                reach[i] |= reach[m]
    return all(not (reach[i] >> i) & 1 for i in range(k))


# --------------------------------------------------------------------------
# the partition-lattice join, used only as a sanity check on "lattice"
# --------------------------------------------------------------------------


def join(p, q, n):
    """Finest partition coarser than both p and q (union-find on [n])."""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for part in (p, q):
        for B in part:
            members = [x for x in range(n) if (B >> x) & 1]
            for y in members[1:]:
                rx, ry = find(members[0]), find(y)
                if rx != ry:
                    parent[rx] = ry
    groups = {}
    for x in range(n):
        groups.setdefault(find(x), 0)
        groups[find(x)] |= (1 << x)
    return frozenset(groups.values())


# --------------------------------------------------------------------------
# main sweep
# --------------------------------------------------------------------------


def poset_name(rel, n):
    if not rel:
        return "antichain A_%d" % n
    if len(rel) == n * (n - 1) // 2:
        return "chain C_%d" % n
    bots = {a for (a, b) in rel}
    tops = {b for (a, b) in rel}
    if len(bots) == 1:
        return "down-star (1 below %d)%s" % (
            len(tops), isolated_suffix(rel, n))
    if len(tops) == 1:
        return "up-star (%d below 1)%s" % (len(bots), isolated_suffix(rel, n))
    return "relations=%s" % sorted(rel)


def isolated_suffix(rel, n):
    used = {x for p in rel for x in p}
    k = n - len(used)
    return " + %d isolated" % k if k else ""


def all_pairs_share_an_end(rel):
    """No two strict relations (x<y),(u<v) with x!=u and y!=v."""
    R = sorted(rel)
    for i in range(len(R)):
        for j in range(len(R)):
            (x, y), (u, v) = R[i], R[j]
            if x != u and y != v:
                return False
    return True


def sweep(n, verbose_stable=True):
    perms = list(permutations(range(n)))
    parts = set_partitions(n)
    pidx = {p: i for i, p in enumerate(parts)}
    nP = len(parts)

    # precompute the S_n action on partition indices
    act = []
    for s in perms:
        row = [0] * nP
        for p in parts:
            q = frozenset(
                sum(1 << s[x] for x in range(n) if (B >> x) & 1) for B in p)
            row[pidx[p]] = pidx[q]
        act.append(row)

    classes = iso_classes(n)
    stable = []
    order_hist = {}
    bigger_than_D = []
    lattice_ok = True
    min_ac = (10 ** 9, None)

    for rel in classes:
        ac = frozenset(pidx[p] for p in parts if acyclic(rel, p))
        # sanity: join-closed, contains bottom and top
        acp = [parts[i] for i in sorted(ac)]
        for a in acp:
            for b in acp:
                if pidx[join(a, b, n)] not in ac:
                    lattice_ok = False
        G = [s for k, s in enumerate(perms)
             if frozenset(act[k][i] for i in ac) == ac]
        D = [s for s in perms
             if relabel_poset(rel, s) == rel or relabel_poset(rel, s) == dual(rel)]
        order_hist.setdefault(len(G), 0)
        order_hist[len(G)] += 1
        if len(G) > len(D):
            bigger_than_D.append((rel, len(G), len(D)))
        if len(ac) < min_ac[0]:
            min_ac = (len(ac), rel)
        if len(G) == len(perms):
            stable.append((rel, len(ac)))

    print("=" * 74)
    print("n = %d   isomorphism classes of poset: %d   partitions of [n]: %d"
          % (n, len(classes), nP))
    print("=" * 74)
    print("AC(P) is a join-closed subset of Pi_n on every class: %s"
          % ("YES" if lattice_ok else "NO"))
    print("smallest |AC(P)|: %d, attained by %s"
          % (min_ac[0], poset_name(min_ac[1], n)))
    print()
    print("POSETS WITH G(P) = S_%d  (the full relabelling group preserves the"
          " quotient lattice):  %d of %d" % (n, len(stable), len(classes)))
    if verbose_stable:
        for rel, sz in stable:
            print("    |AC|=%3d of %3d  full-lattice=%-5s  share-an-end=%-5s  %s"
                  % (sz, nP, sz == nP, all_pairs_share_an_end(rel),
                     poset_name(rel, n)))
    print()
    print("distribution of |G(P)| over the %d classes (|S_%d| = %d):"
          % (len(classes), n, len(perms)))
    for k in sorted(order_hist):
        print("    |G| = %-4d : %d classes" % (k, order_hist[k]))
    print("classes where G(P) is STRICTLY LARGER than "
          "{sigma : sigma.P in {P, P^op}}: %d" % len(bigger_than_D))
    for rel, g, d in bigger_than_D:
        print("    |G|=%d > |D|=%d   %s" % (g, d, poset_name(rel, n)))
    print()

    # the chain, explicitly -- the ticket calls it a known degenerate end
    chain = frozenset((i, j) for i in range(n) for j in range(n) if i < j)
    if n >= 1:
        acc = [p for p in parts if acyclic(chain, p)]
        Gc = [s for k, s in enumerate(perms)
              if frozenset(act[k][pidx[p]] for p in acc)
              == frozenset(pidx[p] for p in acc)]
        print("CHAIN C_%d:  |AC| = %d (= 2^(n-1) = %d),  |G(C_%d)| = %d,"
              "  S_n-stable: %s"
              % (n, len(acc), 2 ** (n - 1) if n else 1, n, len(Gc),
                 len(Gc) == len(perms)))
        anti = frozenset()
        aca = [p for p in parts if acyclic(anti, p)]
        print("ANTICHAIN A_%d: |AC| = %d (= all partitions: %s),"
              "  S_n-stable: True"
              % (n, len(aca), len(aca) == nP))
    print()
    return classes, stable


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    summary = []
    for n in range(1, nmax + 1):
        classes, stable = sweep(n)
        summary.append((n, len(classes), len(stable)))
    print("=" * 74)
    print("SUMMARY")
    print("=" * 74)
    print("  n   iso classes   G(P) = S_n   fraction")
    for n, c, s in summary:
        print("  %d   %11d   %10d   %s" % (n, c, s, "%.4f" % (s / c)))
