"""Kernel for mg-41aa -- the repair of mg-af28 under mg-6ad0's audit.

WHY A THIRD KERNEL.  mg-af28 carries posets as tuples of UP-set bitmasks and
enumerates them by adjoining a new MAXIMAL element above an order ideal.
mg-6ad0 carries posets as tuples of frozensets of strict predecessors and
enumerates them by NATURAL LABELLING.  This file carries posets as tuples of
DOWN-set bitmasks and enumerates them by DECIDING EACH PAIR -- for every pair
i < j, one of {i below j, j below i, incomparable} -- with transitivity pruned
at each step and no induction on n at all.  Nothing here is imported from
either directory; the enumeration is certified against A000112 and the tableau
counts against the hook length formula in `selftest41aa.py`.

The canonical form is necessarily the same IDEA in all three (minimise an
encoding over relabellings) -- that is what a canonical form is.  What differs
is the encoding (down-masks here, up-masks in af28, an adjacency string in
6ad0) and the fact that this one refines colours first, which it must, because
this repair has to canonicalise posets that the other two never touch.

CONVENTIONS
  A poset is a pair (n, down) with down a tuple of n ints; bit j of down[i] is
  set iff j < i strictly.  A partition is a weakly decreasing tuple of positive
  ints.  `sub(mu, lam)` means the diagram of mu is contained in that of lam.
"""

from itertools import permutations

# ------------------------------------------------------------------ posets --


def mk(n, pairs):
    """Poset from strict pairs (a, b) meaning a < b.  Transitive closure taken
    here; irreflexivity and antisymmetry asserted."""
    down = [0] * n
    for a, b in pairs:
        down[b] |= 1 << a
    changed = True
    while changed:
        changed = False
        for i in range(n):
            m = down[i]
            new = m
            r = m
            while r:
                b = r & -r
                new |= down[b.bit_length() - 1]
                r ^= b
            if new != m:
                down[i] = new
                changed = True
    P = (n, tuple(down))
    assert is_poset(P), "mk: not a poset"
    return P


def is_poset(P):
    n, down = P
    for i in range(n):
        if down[i] >> i & 1:
            return False
        m = down[i]
        while m:
            b = m & -m
            j = b.bit_length() - 1
            if down[j] >> i & 1:
                return False
            if down[i] | down[j] != down[i]:
                return False
            m ^= b
    return True


def ups(P):
    n, down = P
    u = [0] * n
    for i in range(n):
        m = down[i]
        while m:
            b = m & -m
            u[b.bit_length() - 1] |= 1 << i
            m ^= b
    return tuple(u)


def _colours(P):
    """Iterated refinement.  Start from (|down|, |up|); refine by the multiset
    of neighbour colours below and above until stable.  Returns a tuple of
    hashable colours, one per element."""
    n, down = P
    u = ups(P)
    col = [(bin(down[i]).count("1"), bin(u[i]).count("1")) for i in range(n)]
    while True:
        new = []
        for i in range(n):
            lo, hi = [], []
            m = down[i]
            while m:
                b = m & -m
                lo.append(col[b.bit_length() - 1])
                m ^= b
            m = u[i]
            while m:
                b = m & -m
                hi.append(col[b.bit_length() - 1])
                m ^= b
            new.append((col[i], tuple(sorted(lo)), tuple(sorted(hi))))
        # compress to small ints, keeping the order induced by the colour value
        order = {c: k for k, c in enumerate(sorted(set(new)))}
        new = [order[c] for c in new]
        if len(set(new)) == len(set(col)) and all(
                (col[i] == col[j]) == (new[i] == new[j])
                for i in range(n) for j in range(n)):
            return tuple(new)
        col = new


def canon(P):
    """Canonical form: the lexicographically least tuple of down-set bitmasks
    over all relabellings that respect the refined colouring."""
    n, down = P
    col = _colours(P)
    groups = {}
    for i in range(n):
        groups.setdefault(col[i], []).append(i)
    keys = sorted(groups)
    best = [None]

    def emit(inv):
        # inv[new] = old
        pos = [0] * n
        for new, old in enumerate(inv):
            pos[old] = new
        rows = [0] * n
        for old in range(n):
            m = down[old]
            r = 0
            while m:
                b = m & -m
                r |= 1 << pos[b.bit_length() - 1]
                m ^= b
            rows[pos[old]] = r
        t = tuple(rows)
        if best[0] is None or t < best[0]:
            best[0] = t

    def rec(k, inv):
        if k == len(keys):
            emit(inv)
            return
        for p in permutations(groups[keys[k]]):
            rec(k + 1, inv + list(p))

    rec(0, [])
    return (n, best[0])


def iso(P, Q):
    """An explicit isomorphism P -> Q as a list phi with phi[i] the image of i,
    or None.  Backtracking over colour classes; the map is checked in full
    before it is returned, so a returned map is verified, not inferred."""
    n, dP = P
    m, dQ = Q
    if n != m:
        return None
    cP, cQ = _colours(P), _colours(Q)
    # colours are small ints assigned in sorted order of the refined signature,
    # so equal colour values mean the same class only if the class SIZES match.
    if sorted(cP) != sorted(cQ):
        return None
    cand = [[j for j in range(n) if cQ[j] == cP[i]] for i in range(n)]
    order = sorted(range(n), key=lambda i: len(cand[i]))
    phi = [-1] * n
    used = 0

    def ok(i, j):
        for k in range(n):
            if phi[k] < 0:
                continue
            if bool(dP[i] >> k & 1) != bool(dQ[j] >> phi[k] & 1):
                return False
            if bool(dP[k] >> i & 1) != bool(dQ[phi[k]] >> j & 1):
                return False
        return True

    def rec(t):
        nonlocal used
        if t == n:
            return True
        i = order[t]
        for j in cand[i]:
            if used >> j & 1:
                continue
            if not ok(i, j):
                continue
            phi[i] = j
            used |= 1 << j
            if rec(t + 1):
                return True
            used ^= 1 << j
            phi[i] = -1
        return False

    if not rec(0):
        return None
    # full re-check of the returned map, both directions
    for a in range(n):
        for b in range(n):
            if bool(dP[b] >> a & 1) != bool(dQ[phi[b]] >> phi[a] & 1):
                return None
    return list(phi)


def all_posets(n):
    """Every isomorphism class of poset on n elements, by DECIDING EACH PAIR.

    For the pairs (i, j) with i < j in lexicographic order, choose one of
    "i below j", "j below i", "incomparable"; after each choice the partial
    relation is closed transitively and rejected if that creates a cycle or
    contradicts an earlier "incomparable" decision.  No induction on n, and no
    reference to posets on fewer elements.  Deduplicated by `canon`.
    """
    if n == 0:
        return [(0, ())]
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    out = {}

    def close(down):
        d = list(down)
        changed = True
        while changed:
            changed = False
            for i in range(n):
                m, new = d[i], d[i]
                r = m
                while r:
                    b = r & -r
                    new |= d[b.bit_length() - 1]
                    r ^= b
                if new != m:
                    d[i] = new
                    changed = True
        for i in range(n):
            if d[i] >> i & 1:
                return None
        return d

    def rec(t, down, forbidden):
        # `forbidden` is a list of masks: bit j of forbidden[i] set means i and
        # j were decided incomparable, so neither may become comparable later.
        if t == len(pairs):
            P = (n, tuple(down))
            out.setdefault(canon(P), P)
            return
        i, j = pairs[t]
        if down[j] >> i & 1 or down[i] >> j & 1:
            rec(t + 1, down, forbidden)          # already forced by transitivity
            return
        for choice in (0, 1, 2):
            if choice == 2:
                f2 = list(forbidden)
                f2[i] |= 1 << j
                f2[j] |= 1 << i
                rec(t + 1, down, f2)
                continue
            d = list(down)
            if choice == 0:
                d[j] |= 1 << i
            else:
                d[i] |= 1 << j
            d = close(d)
            if d is None:
                continue
            if any(d[a] & forbidden[a] for a in range(n)):
                continue
            rec(t + 1, d, forbidden)

    rec(0, [0] * n, [0] * n)
    return sorted(out.values())


def ideals(P):
    """All order ideals as bitmasks, by closing every subset downwards."""
    n, down = P
    out = set()
    for S in range(1 << n):
        cl = S
        m = S
        while m:
            b = m & -m
            cl |= down[b.bit_length() - 1]
            m ^= b
        out.add(cl)
    return sorted(out, key=lambda S: (bin(S).count("1"), S))


def ideal_lattice(P):
    """J(P) as a poset, plus the list of ideals in element order."""
    ids = ideals(P)
    m = len(ids)
    down = [0] * m
    for a in range(m):
        for b in range(m):
            if a != b and ids[a] & ids[b] == ids[a]:
                down[b] |= 1 << a
    return (m, tuple(down)), ids


def linear_extensions(P):
    n, down = P
    res = []

    def rec(used, seq):
        if used == (1 << n) - 1:
            res.append(tuple(seq))
            return
        for i in range(n):
            if used >> i & 1:
                continue
            if down[i] & ~used:
                continue
            seq.append(i)
            rec(used | 1 << i, seq)
            seq.pop()
    rec(0, [])
    return res


# -------------------------------------------------------------- partitions --


def partitions(n):
    if n == 0:
        return [()]
    out = []

    def rec(left, cap, cur):
        if left == 0:
            out.append(tuple(cur))
            return
        for v in range(min(left, cap), 0, -1):
            cur.append(v)
            rec(left - v, v, cur)
            cur.pop()
    rec(n, n, [])
    return out


def sub(mu, lam):
    """Diagram containment mu subset lam."""
    if len(mu) > len(lam):
        return False
    return all(mu[i] <= lam[i] for i in range(len(mu)))


def cells(lam, mu=()):
    """Cells of the skew diagram lam/mu, row-major."""
    assert sub(mu, lam), (mu, lam)
    out = []
    for i, p in enumerate(lam):
        lo = mu[i] if i < len(mu) else 0
        for j in range(lo, p):
            out.append((i, j))
    return out


def skew_poset(lam, mu=()):
    """The cell poset of lam/mu: cells ordered componentwise (row and column
    both weakly increasing).  Returns (P, cells)."""
    cs = cells(lam, mu)
    n = len(cs)
    down = [0] * n
    for a, (ia, ja) in enumerate(cs):
        for b, (ib, jb) in enumerate(cs):
            if (ia, ja) != (ib, jb) and ia <= ib and ja <= jb:
                down[b] |= 1 << a
    return (n, tuple(down)), cs


def young_interval(mu, lam):
    """[mu, lam] as the sorted list of partitions nu with mu subset nu subset
    lam -- built from CONTAINMENT of diagrams, with no reference to any cell
    poset."""
    assert sub(mu, lam)
    out = []
    for k in range(sum(mu), sum(lam) + 1):
        for nu in partitions(k):
            if sub(mu, nu) and sub(nu, lam):
                out.append(nu)
    return sorted(out, key=lambda x: (sum(x), x))


def interval_poset(mu, lam):
    """[mu, lam] as a poset, ordered by containment.  Returns (P, elements)."""
    iv = young_interval(mu, lam)
    m = len(iv)
    down = [0] * m
    for a in range(m):
        for b in range(m):
            if a != b and sub(iv[a], iv[b]):
                down[b] |= 1 << a
    return (m, tuple(down)), iv


def conj(lam):
    if not lam:
        return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))


def hook_length_formula(lam):
    n = sum(lam)
    lc = conj(lam)
    num = 1
    for k in range(2, n + 1):
        num *= k
    den = 1
    for i, p in enumerate(lam):
        for j in range(p):
            den *= (p - j) + (lc[j] - i) - 1
    assert num % den == 0
    return num // den


def chain(k):
    """The k-element chain 0 < 1 < ... < k-1."""
    return mk(k, [(i, i + 1) for i in range(k - 1)])


def grid(p, q):
    """The lattice {0..p} x {0..q} ordered componentwise, built DIRECTLY as a
    product of two integer intervals -- not as J(anything)."""
    pts = [(a, b) for a in range(p + 1) for b in range(q + 1)]
    n = len(pts)
    down = [0] * n
    for x, (a, b) in enumerate(pts):
        for y, (c, d) in enumerate(pts):
            if (a, b) != (c, d) and a <= c and b <= d:
                down[y] |= 1 << x
    return (n, tuple(down)), pts


def disjoint_union(P, Q):
    n, dp = P
    m, dq = Q
    down = list(dp) + [x << n for x in dq]
    return (n + m, tuple(down))


# ----------------------------------------------------------------- lattices --


def _bound(a, b, rel):
    """The extremum of the common `rel`-bounds of a and b, or None.

    With rel = ups(P) this is the JOIN: the common upper bounds are
    (up[a] + a) & (up[b] + b), and the join is the one of them that lies below
    all of them.  With rel = down it is the MEET, by the same words upside
    down.  In both cases the test is `common subset rel[c] + c`."""
    common = (rel[a] | 1 << a) & (rel[b] | 1 << b)
    m = common
    while m:
        bb = m & -m
        c = bb.bit_length() - 1
        if common & ~(rel[c] | 1 << c) == 0:
            return c
        m ^= bb
    return None


def is_lattice(P):
    """True iff every pair has both a join and a meet."""
    n, down = P
    u = ups(P)
    for a in range(n):
        for b in range(n):
            if _bound(a, b, u) is None or _bound(a, b, down) is None:
                return False
    return True


def is_distributive(P):
    """x /\\ (y \\/ z) = (x /\\ y) \\/ (x /\\ z) on every triple.  Assumes a
    lattice; call `is_lattice` first.  Returns (verdict, failing triple)."""
    n, down = P
    u = ups(P)
    join = [[_bound(a, b, u) for b in range(n)] for a in range(n)]
    meet = [[_bound(a, b, down) for b in range(n)] for a in range(n)]
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if meet[x][join[y][z]] != join[meet[x][y]][meet[x][z]]:
                    return False, (x, y, z)
    return True, None


def join_irreducibles(P):
    """The subposet of elements covering exactly one element."""
    n, down = P
    ji = []
    for i in range(n):
        lower = down[i]
        # x is join-irreducible iff it has exactly one lower cover
        covers = []
        m = lower
        while m:
            b = m & -m
            c = b.bit_length() - 1
            if lower & ~(down[c] | 1 << c) == 0:
                covers.append(c)
            m ^= b
        if len(covers) == 1:
            ji.append(i)
    idx = {v: k for k, v in enumerate(ji)}
    d2 = [0] * len(ji)
    for a in ji:
        for b in ji:
            if a != b and down[b] >> a & 1:
                d2[idx[b]] |= 1 << idx[a]
    return (len(ji), tuple(d2)), ji


# ------------------------------------------------------- Young-Fibonacci ----


def young_fibonacci(maxrank):
    """Ranks and covers of the Young-Fibonacci lattice to `maxrank`.

    Third coding of the same published neighbour rule (Stanley 1988, as stated
    on the Young-Fibonacci lattice page): from a word w with k leading 2s,
    the upper covers are the k+1 words obtained by inserting a 1 at or before
    the leftmost 1, together with the word obtained by promoting that leftmost
    1 to a 2 (when w contains a 1).  Certified in selftest41aa.py by Fibonacci
    rank sizes and by DU - UD = I below the top rank.
    """
    ranks = {0: [()]}
    for r in range(1, maxrank + 1):
        cur = []

        def gen(left, w):
            if left == 0:
                cur.append(tuple(w))
                return
            for d in (1, 2):
                if d <= left:
                    w.append(d)
                    gen(left - d, w)
                    w.pop()
        gen(r, [])
        ranks[r] = sorted(set(cur))
    covers = {}
    for r in range(maxrank + 1):
        for w in ranks[r]:
            if r == maxrank:
                covers[w] = []
                continue
            k = 0
            while k < len(w) and w[k] == 2:
                k += 1
            up = set()
            for pos in range(k + 1):
                up.add(w[:pos] + (1,) + w[pos:])
            if k < len(w):
                up.add(w[:k] + (2,) + w[k + 1:])
            covers[w] = sorted(x for x in up if sum(x) == r + 1)
    return ranks, covers


def yf_interval_poset(w, ranks, covers):
    """The interval [empty, w] of the Young-Fibonacci lattice, as a poset."""
    below = {w}
    frontier = {w}
    dn = {}
    for v, us in covers.items():
        for x in us:
            dn.setdefault(x, set()).add(v)
    while frontier:
        nxt = set()
        for x in frontier:
            for y in dn.get(x, ()):
                if y not in below:
                    below.add(y)
                    nxt.add(y)
        frontier = nxt
    elems = sorted(below, key=lambda x: (sum(x), x))
    idx = {v: k for k, v in enumerate(elems)}
    pairs = []
    for v in elems:
        for x in covers.get(v, ()):
            if x in idx:
                pairs.append((idx[v], idx[x]))
    return mk(len(elems), pairs), elems
