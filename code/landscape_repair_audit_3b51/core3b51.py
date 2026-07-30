#!/usr/bin/env python3
"""
mg-3b51 INDEPENDENT AUDIT of mg-1953 / 6b1eacf -- shared core.

Written from scratch.  Shares no code with code/landscape_ebd8/ (the original),
code/landscape_audit_d673/ (the first audit), code/landscape_repair_1953/ (the
target of THIS audit), code/semigroup_note/, code/face_geometry/,
code/unified_gate_8fd1/ or code/hodge_leverage/.  Pure Python 3, exact integer
arithmetic, no third-party imports.

DELIBERATELY DIFFERENT ROUTES.  Where mg-1953's core1953.py makes a choice, this
file makes the other one, so that agreement is evidence and not a shared bug:

  * POSETS are carried as an n x n BOOLEAN REACHABILITY MATRIX packed into a
    tuple of row bitmasks, not as a frozenset of pairs.  They are ENUMERATED BY
    MAXIMAL-ELEMENT EXTENSION -- every n-poset is an (n-1)-poset plus a new
    maximal element sitting over a down-set -- not by filtering the 2^C(n,2)
    transitively closed subsets of the upper triangle.  Class counts are
    certified against A000112 by the caller.

  * "DOES THE FLAT X MEET THE OPEN ORDER CONE U?" is decided by NUMERIC
    CONSTRUCTION WITH A CERTIFICATE BOTH WAYS, not by an exhaustive search over
    |X|! block orderings.  On the YES side a rational point of X is BUILT by
    longest-path potentials and then VERIFIED to satisfy every defining
    inequality of U and every defining equation of X.  On the NO side a
    DIRECTED CYCLE of blocks is EXHIBITED; summing the strict inequalities
    around it yields 0 < 0, so no point can exist.  Neither side consults the
    word "acyclic" as a criterion -- the cycle is the certificate, not the test.

  * LINEAR EXTENSIONS are counted by dynamic programming over order ideals, not
    by filtering all n! permutations.

  * The MULTIPLICITY SOLVE is the repo's own triangular identity
    sum_{Y refines X} m_Y = prod_B |L(P|_B)| , rebuilt here from the identity
    rather than copied.

Nothing in this file reads any output committed by mg-1953.
"""

from itertools import permutations


# ------------------------------------------------------------------ posets ---
# A poset on [n] is a tuple `up` of n ints; bit j of up[i] is set iff i < j in P
# (STRICT, transitively closed).

def _closure(n, up):
    up = list(up)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            acc = up[i]
            m = up[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                acc |= up[j]
            if acc != up[i]:
                up[i] = acc
                changed = True
    return tuple(up)


def down_sets(n, up):
    """All order ideals of P, as bitmasks (D closed downwards)."""
    down = [0] * n
    for i in range(n):
        for j in range(n):
            if up[j] >> i & 1:
                down[i] |= 1 << j
    out = []
    for D in range(1 << n):
        ok = True
        for i in range(n):
            if D >> i & 1 and (down[i] & ~D):
                ok = False
                break
        if ok:
            out.append(D)
    return out


def _relabel(n, up, sigma):
    new = [0] * n
    for i in range(n):
        m = up[i]
        v = 0
        while m:
            j = (m & -m).bit_length() - 1
            m &= m - 1
            v |= 1 << sigma[j]
        new[sigma[i]] = v
    return tuple(new)


def canonical(n, up):
    """Minimum over the FULL S_n orbit."""
    best = None
    for sigma in permutations(range(n)):
        img = _relabel(n, up, sigma)
        if best is None or img < best:
            best = img
    return best


def iso_classes(n):
    """One representative per isomorphism class, built by MAXIMAL-ELEMENT
    EXTENSION: every poset on [n] is a poset on [n-1] with a new element n-1
    placed above an order ideal of it.  (Delete any maximal element.)"""
    if n == 0:
        return [()]
    if n == 1:
        return [(0,)]
    seen = {}
    for up in iso_classes(n - 1):
        for D in down_sets(n - 1, up):
            new = list(up) + [0]
            for i in range(n - 1):
                if D >> i & 1:
                    new[i] |= 1 << (n - 1)
            cand = _closure(n, tuple(new))
            c = canonical(n, cand)
            if c not in seen:
                seen[c] = cand
    return [seen[c] for c in sorted(seen)]


def relations(n, up):
    """The strict pairs (i, j) with i < j in P."""
    return [(i, j) for i in range(n) for j in range(n) if up[i] >> j & 1]


def is_connected(n, up):
    if n <= 1:
        return True
    adj = [0] * n
    for (i, j) in relations(n, up):
        adj[i] |= 1 << j
        adj[j] |= 1 << i
    seen, stack = 1, [0]
    while stack:
        x = stack.pop()
        m = adj[x] & ~seen
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            seen |= 1 << y
            stack.append(y)
    return seen == (1 << n) - 1


def count_linear_extensions(n, up):
    """DP over order ideals -- no permutation enumeration."""
    down = [0] * n
    for i in range(n):
        for j in range(n):
            if up[j] >> i & 1:
                down[i] |= 1 << j
    memo = {0: 1}

    def f(D):
        if D in memo:
            return memo[D]
        tot = 0
        m = D
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if down[i] & ~(D & ~(1 << i)) == 0:      # i maximal in D
                tot += f(D & ~(1 << i))
        memo[D] = tot
        return tot

    return f((1 << n) - 1)


def linear_extensions(n, up):
    """The actual list, for the small-n places that need it."""
    rel = relations(n, up)
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for p, x in enumerate(perm):
            pos[x] = p
        if all(pos[i] < pos[j] for (i, j) in rel):
            out.append(perm)
    return out


def induced(n, up, mask):
    """The subposet on the elements of `mask`, relabelled to 0..k-1."""
    elts = [i for i in range(n) if mask >> i & 1]
    idx = {e: t for t, e in enumerate(elts)}
    new = [0] * len(elts)
    for a, e in enumerate(elts):
        for f in elts:
            if up[e] >> f & 1:
                new[a] |= 1 << idx[f]
    return len(elts), tuple(new)


# -------------------------------------------------------------- partitions ---

def set_partitions(n):
    """All set partitions of [n], each a tuple of block BITMASKS sorted by low
    bit.  Built by restricted-growth strings, not by recursive block append."""
    out = []
    rgs = [0] * n

    def rec(i, mx):
        if i == n:
            blocks = {}
            for e in range(n):
                blocks[rgs[e]] = blocks.get(rgs[e], 0) | (1 << e)
            out.append(tuple(blocks[k] for k in sorted(blocks)))
            return
        for v in range(mx + 2):
            rgs[i] = v
            rec(i + 1, max(mx, v))

    rec(0, -1)
    return out


def block_of(X, n):
    w = [0] * n
    for b, B in enumerate(X):
        m = B
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            w[i] = b
    return w


def all_blocks_antichain(up, X):
    """No block contains a comparable pair."""
    for B in X:
        m = B
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if up[i] & B:
                return False
    return True


def quotient_digraph(n, up, X):
    """succ[b] = set of blocks strictly above block b (edges between DISTINCT
    blocks only), plus the list of blocks carrying an internal relation."""
    w = block_of(X, n)
    k = len(X)
    succ = [set() for _ in range(k)]
    internal = set()
    for (i, j) in relations(n, up):
        a, b = w[i], w[j]
        if a == b:
            internal.add(a)
        else:
            succ[a].add(b)
    return succ, internal


def find_cycle(succ):
    """Return a directed cycle (list of vertices) or None.  Iterative DFS."""
    k = len(succ)
    colour = [0] * k
    parent = [-1] * k
    for s in range(k):
        if colour[s]:
            continue
        stack = [(s, iter(sorted(succ[s])))]
        colour[s] = 1
        while stack:
            v, it = stack[-1]
            advanced = False
            for w in it:
                if colour[w] == 1:
                    cyc = [w]
                    x = v
                    while x != w:
                        cyc.append(x)
                        x = parent[x]
                    cyc.reverse()
                    return cyc
                if colour[w] == 0:
                    colour[w] = 1
                    parent[w] = v
                    stack.append((w, iter(sorted(succ[w]))))
                    advanced = True
                    break
            if not advanced:
                colour[v] = 2
                stack.pop()
    return None


def meets_open_cone(n, up, X, want_certificate=False):
    """DOES THE FLAT X MEET THE OPEN ORDER CONE U = {x : x_i < x_j for i <_P j}?

    Decided by CONSTRUCTION with a certificate on BOTH sides, and with no use of
    'acyclic' as a criterion:

      YES -- build the potential  v(b) = length of the longest directed path in
             the quotient digraph ending at block b, assign x_i = v(block(i)),
             and VERIFY every defining equation of the flat (x_i = x_j inside a
             block) and every defining inequality of U (x_i < x_j for i <_P j).
             The returned point is the witness.

      NO  -- exhibit either a block carrying an internal relation i <_P j (then
             x_i = x_j and x_i < x_j are contradictory), or a directed cycle
             B_0 -> B_1 -> ... -> B_0 of blocks.  Summing the strict
             inequalities around the cycle gives t < t, so no point exists.

    Returns a bool, or (bool, certificate) when want_certificate is set.
    """
    succ, internal = quotient_digraph(n, up, X)
    if internal:
        cert = ("internal relation in block %d" % sorted(internal)[0])
        return (False, cert) if want_certificate else False
    cyc = find_cycle(succ)
    if cyc is not None:
        cert = "block cycle " + " -> ".join(str(b) for b in cyc + [cyc[0]])
        return (False, cert) if want_certificate else False

    # longest-path potentials by relaxation (the digraph has no cycle, so this
    # terminates in at most k rounds); no topological sort is performed.
    k = len(X)
    v = [0] * k
    for _ in range(k):
        for b in range(k):
            for c in succ[b]:
                if v[c] < v[b] + 1:
                    v[c] = v[b] + 1
    w = block_of(X, n)
    x = [v[w[i]] for i in range(n)]
    # VERIFY, from the definitions, that x lies in X and in U.
    for B in X:
        m, first = B, None
        while m:
            i = (m & -m).bit_length() - 1
            m &= m - 1
            if first is None:
                first = x[i]
            elif x[i] != first:
                raise AssertionError("constructed point leaves the flat")
    for (i, j) in relations(n, up):
        if not x[i] < x[j]:
            raise AssertionError("constructed point leaves the open cone")
    return (True, x) if want_certificate else True


def meets_open_cone_bruteforce(n, up, X):
    """Independent cross-check of meets_open_cone: is there a total ordering of
    the blocks sending every relation strictly forwards?  Exponential; used only
    to cross-validate the constructive route at small n."""
    rel = relations(n, up)
    w = block_of(X, n)
    k = len(X)
    for order in permutations(range(k)):
        slot = [0] * k
        for s, b in enumerate(order):
            slot[b] = s
        if all(slot[w[i]] < slot[w[j]] for (i, j) in rel):
            return True
    return False


def refines(Y, X):
    """Every block of Y sits inside a block of X."""
    return all(any(B & ~C == 0 for C in X) for B in Y)


def factorial(k):
    r = 1
    for i in range(2, k + 1):
        r *= i
    return r


def closed_form(X):
    p = 1
    for B in X:
        p *= factorial(bin(B).count("1") - 1)
    return p


def support_lattice(n, up, flats=None):
    """AC(P): the flats whose quotient digraph on DISTINCT blocks is acyclic.
    Blocks MAY contain comparable pairs -- this is the repo's commitment-level
    set, not M_0."""
    fl = flats if flats is not None else set_partitions(n)
    out = []
    for X in fl:
        succ, _ = quotient_digraph(n, up, X)
        if find_cycle(succ) is None:
            out.append(X)
    return out


def commitment_levels_from_moves(n, up):
    """AC(P) computed the OTHER way: the supports of the P-compatible ordered
    set partitions, enumerated directly.  Used as a cross-check on
    support_lattice()."""
    rel = relations(n, up)
    lev = set()
    for X in set_partitions(n):
        k = len(X)
        w = block_of(X, n)
        for order in permutations(range(k)):
            slot = [0] * k
            for s, b in enumerate(order):
                slot[b] = s
            if all(slot[w[i]] <= slot[w[j]] for (i, j) in rel):
                lev.add(X)
                break
    return sorted(lev)


def moves_of(n, up):
    """P-compatible ORDERED set partitions: i <_P j implies i's block is not
    strictly after j's."""
    rel = relations(n, up)
    out = []
    for X in set_partitions(n):
        k = len(X)
        w = block_of(X, n)
        for order in permutations(range(k)):
            slot = [0] * k
            for s, b in enumerate(order):
                slot[b] = s
            if all(slot[w[i]] <= slot[w[j]] for (i, j) in rel):
                out.append(tuple(X[b] for b in order))
    return out


def move_product(x, y):
    """Blocks B_i & C_j, ordered lexicographically by (i, j), empties dropped."""
    return tuple(B & C for B in x for C in y if B & C)


def multiplicities(n, up, levels=None):
    """Solve the repo's triangular identity from scratch:
           sum_{Y refines X} m_Y = prod_{B in X} |L(P|_B)| ,
    finest first.  Returns (m, target)."""
    lev = levels if levels is not None else support_lattice(n, up)
    target = {}
    for X in lev:
        p = 1
        for B in X:
            k, sub = induced(n, up, B)
            p *= count_linear_extensions(k, sub)
        target[X] = p
    order = sorted(lev, key=lambda X: -len(X))
    m = {}
    for X in order:
        s = 0
        for Y in m:
            if Y != X and refines(Y, X):
                s += m[Y]
        m[X] = target[X] - s
    return m, target


def label(X, n):
    return "|".join("".join(chr(97 + i) for i in range(n) if B >> i & 1)
                    for B in X)


def poset_name(n, up):
    rel = relations(n, up)
    if not rel:
        return "{antichain on %d}" % n
    # print the cover relations only
    cov = []
    for (i, j) in rel:
        if not any(up[i] >> k & 1 and up[k] >> j & 1 for k in range(n)):
            cov.append((i, j))
    return "{" + ", ".join("%s<%s" % (chr(97 + i), chr(97 + j))
                           for (i, j) in sorted(cov)) + "}"
