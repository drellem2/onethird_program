"""kern5800 -- independent kernel for the mg-5800 audit of mg-41aa / 504ab6c.

Shares no code with code/branching_af28/, code/branching_audit_6ad0/ or
code/branching_repair_41aa/.  Written from the definitions:

  * a poset on {0..n-1} is a tuple `up` of bitmasks, up[i] = {j : i < j},
    required irreflexive and transitively closed;
  * canonical form is individualisation-refinement min over labellings,
    with orbit pruning by explicit swap-automorphisms;
  * unlabelled posets are enumerated by ADDING A MAXIMAL ELEMENT over an
    order ideal of a poset one size smaller (every poset has a maximal
    element, so this is exhaustive) -- no induction on shape, no table;
  * skew shapes are (a_i, b_i] row intervals with both bounds weakly
    decreasing; the interval [mu, lambda] of Young's lattice is built
    DIRECTLY as the set of partitions nu with mu <= nu <= lambda ordered by
    containment -- never as J(anything) -- which is what makes the converse
    test independent of Birkhoff.
"""

from itertools import combinations

# ----------------------------------------------------------------- bit utils

def bits(m):
    out = []
    while m:
        b = m & -m
        out.append(b.bit_length() - 1)
        m ^= b
    return out


def popcount(m):
    return bin(m).count("1")


# ------------------------------------------------------------------- posets

def check_poset(n, up):
    """Irreflexive, transitively closed, antisymmetric.  Raises on failure."""
    assert len(up) == n
    for i in range(n):
        assert not (up[i] >> i) & 1, "reflexive"
        for j in bits(up[i]):
            assert not (up[j] >> i) & 1, "antisymmetric"
            assert up[i] & up[j] == up[j], "not transitively closed"
    return True


def down_of(n, up):
    dn = [0] * n
    for i in range(n):
        for j in bits(up[i]):
            dn[j] |= 1 << i
    return tuple(dn)


def _refine(n, up, dn, colors):
    while True:
        sig = []
        for i in range(n):
            sig.append((colors[i],
                        tuple(sorted(colors[j] for j in bits(up[i]))),
                        tuple(sorted(colors[j] for j in bits(dn[i])))))
        order = {s: k for k, s in enumerate(sorted(set(sig)))}
        new = tuple(order[s] for s in sig)
        if new == colors:
            return colors
        colors = new


def _encode(n, up, perm):
    """perm[pos] = element.  Bit (pos_i*n + pos_j) set iff perm[pos_i] < perm[pos_j]."""
    code = 0
    for pi in range(n):
        row = up[perm[pi]]
        for pj in range(n):
            if (row >> perm[pj]) & 1:
                code |= 1 << (pi * n + pj)
    return code


def canon(n, up):
    """Canonical code: min over all labellings, via individualisation-refinement.

    Orbit pruning: inside the class being individualised, two elements with
    identical up-mask and identical down-mask are swapped by an automorphism,
    so only one representative is branched on.  That is what keeps antichains
    (and disjoint unions of equal blocks) cheap.
    """
    if n == 0:
        return 0
    dn = down_of(n, up)
    best = [None]

    def rec(colors):
        colors = _refine(n, up, dn, colors)
        cls = {}
        for i in range(n):
            cls.setdefault(colors[i], []).append(i)
        big = [c for c in cls.values() if len(c) > 1]
        if not big:
            perm = [0] * n
            for i in range(n):
                perm[colors[i]] = i
            code = _encode(n, up, perm)
            if best[0] is None or code < best[0]:
                best[0] = code
            return
        # The target class must be chosen by an INVARIANT of the colouring.
        # Choosing it by dict-insertion order (i.e. by element index) makes the
        # search tree label-dependent, and then the min over leaves is not a
        # canonical form: two isomorphic 20-element distributive lattices came
        # out with different codes.  Smallest class, then smallest colour.
        target = min(big, key=lambda c: (len(c), colors[c[0]]))
        seen = set()
        reps = []
        for v in target:
            key = (up[v], dn[v])
            if key in seen:
                continue
            seen.add(key)
            reps.append(v)
        base = colors[target[0]]
        for v in reps:
            nc = list(colors)
            for i in range(n):
                nc[i] = 2 * colors[i]
            nc[v] = 2 * base - 1
            rec(tuple(nc))

    rec(tuple([0] * n))
    return best[0]


def canon_key(n, up):
    return (n, canon(n, up))


def decode(n, code):
    """Inverse of _encode: rebuild `up` from a canonical code."""
    up = [0] * n
    for i in range(n):
        for j in range(n):
            if (code >> (i * n + j)) & 1:
                up[i] |= 1 << j
    return tuple(up)


# --------------------------------------------------- unlabelled enumeration

def ideals(n, up):
    """All order ideals (down-sets) of the poset, as bitmasks."""
    dn = down_of(n, up)
    out = []
    for S in range(1 << n):
        ok = True
        for i in bits(S):
            if dn[i] & ~S:
                ok = False
                break
        if ok:
            out.append(S)
    return out


def add_maximal(n, up, D):
    """New element n, sitting strictly above exactly the ideal D."""
    nu = list(up)
    for i in bits(D):
        nu[i] |= 1 << n
    nu.append(0)
    return tuple(nu)


def enumerate_posets(nmax):
    """{n: [canonical codes]} for n = 1..nmax, by adding a maximal element."""
    out = {1: [canon(1, (0,))]}
    for n in range(2, nmax + 1):
        seen = set()
        for code in out[n - 1]:
            up = decode(n - 1, code)
            for D in ideals(n - 1, up):
                nu = add_maximal(n - 1, up, D)
                seen.add(canon(n, nu))
        out[n] = sorted(seen)
    return out


# ------------------------------------------------------- lattice operations

def ideal_lattice(n, up):
    """J(P) as a poset: elements are the ideals, ordered by inclusion."""
    ids = ideals(n, up)
    m = len(ids)
    idx = {s: k for k, s in enumerate(ids)}
    jup = [0] * m
    for a in range(m):
        for b in range(m):
            if a != b and ids[a] & ids[b] == ids[a]:
                jup[a] |= 1 << b
    return m, tuple(jup), ids


def join_irreducibles(m, up):
    """Elements covering exactly one element -- the join-irreducibles of a
    finite lattice.  Returned as an induced subposet."""
    dn = down_of(m, up)
    ji = []
    for x in range(m):
        # covers of x = elements y < x with no z strictly between y and x
        ncov = 0
        for y in bits(dn[x]):
            if not (dn[x] & up[y]):
                ncov += 1
        if ncov == 1:
            ji.append(x)
    return induced(m, up, ji)


def induced(m, up, elts):
    k = len(elts)
    pos = {e: i for i, e in enumerate(elts)}
    nu = [0] * k
    for i, e in enumerate(elts):
        for f in elts:
            if (up[e] >> f) & 1:
                nu[i] |= 1 << pos[f]
    return k, tuple(nu)


def is_lattice(m, up):
    dn = down_of(m, up)
    for a in range(m):
        for b in range(m):
            ua = (up[a] | (1 << a)) & (up[b] | (1 << b))
            if ua == 0:
                return False
            # least element of ua
            cand = [x for x in bits(ua) if all((up[x] >> y) & 1 or x == y for y in bits(ua))]
            if len(cand) != 1:
                return False
            da = (dn[a] | (1 << a)) & (dn[b] | (1 << b))
            if da == 0:
                return False
            cand = [x for x in bits(da) if all((dn[x] >> y) & 1 or x == y for y in bits(da))]
            if len(cand) != 1:
                return False
    return True


def meet_join_tables(m, up):
    dn = down_of(m, up)
    meet = [[None] * m for _ in range(m)]
    join = [[None] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            ua = (up[a] | (1 << a)) & (up[b] | (1 << b))
            c = [x for x in bits(ua) if all((up[x] >> y) & 1 or x == y for y in bits(ua))]
            if len(c) != 1:
                return None, None
            join[a][b] = c[0]
            da = (dn[a] | (1 << a)) & (dn[b] | (1 << b))
            c = [x for x in bits(da) if all((dn[x] >> y) & 1 or x == y for y in bits(da))]
            if len(c) != 1:
                return None, None
            meet[a][b] = c[0]
    return meet, join


def is_distributive(m, up):
    meet, join = meet_join_tables(m, up)
    if meet is None:
        return False
    for a in range(m):
        for b in range(m):
            for c in range(m):
                if meet[a][join[b][c]] != join[meet[a][b]][meet[a][c]]:
                    return False
    return True


# -------------------------------------------------------------- skew shapes

def skew_shapes(n, box):
    """All (a, b) row-interval skew shapes with n cells, no empty row, left
    edge normalised to 0, right edge bounded by `box`.

    a = (a_1 >= ... >= a_r = 0), b = (b_1 >= ... >= b_r), a_i < b_i,
    sum(b_i - a_i) = n.  These are exactly the pairs mu = a subset of
    lambda = b of partitions with |lambda/mu| = n after trimming empty rows
    and empty columns on the left.
    """
    out = []

    def rec(rows, cells):
        if cells == n:
            if rows and rows[-1][0] == 0:
                out.append(tuple(rows))
            return
        if cells > n:
            return
        maxa = rows[-1][0] if rows else box - 1
        maxb = rows[-1][1] if rows else box
        for b in range(1, maxb + 1):
            for a in range(0, min(b, maxa + 1)):
                if cells + (b - a) > n:
                    continue
                rows.append((a, b))
                rec(rows, cells + (b - a))
                rows.pop()

    rec([], 0)
    return out


def skew_cell_poset(shape):
    """Cells (i, j) with a_i <= j < b_i, ordered componentwise."""
    cells = []
    for i, (a, b) in enumerate(shape):
        for j in range(a, b):
            cells.append((i, j))
    n = len(cells)
    pos = {c: k for k, c in enumerate(cells)}
    up = [0] * n
    for c in cells:
        for d in cells:
            if c != d and c[0] <= d[0] and c[1] <= d[1]:
                up[pos[c]] |= 1 << pos[d]
    return n, tuple(up)


def straight_shapes(n):
    """Partitions of n, as skew shapes with a_i = 0."""
    out = []

    def rec(rows, rem, cap):
        if rem == 0:
            out.append(tuple((0, r) for r in rows))
            return
        for r in range(min(cap, rem), 0, -1):
            rows.append(r)
            rec(rows, rem - r, r)
            rows.pop()

    rec([], n, n)
    return out


# ------------------------------------- Young's lattice intervals, DIRECTLY

def partitions_between(mu, lam):
    """All partitions nu with mu subset nu subset lam, as tuples padded to
    len(lam).  Built from the partition definition -- no cell posets."""
    lam = tuple(lam)
    mu = tuple(mu) + (0,) * (len(lam) - len(mu))
    out = []

    def rec(i, prev, acc):
        if i == len(lam):
            out.append(tuple(acc))
            return
        lo, hi = mu[i], min(lam[i], prev)
        for v in range(lo, hi + 1):
            acc.append(v)
            rec(i + 1, v, acc)
            acc.pop()

    rec(0, 10 ** 9, [])
    return out


def interval_poset(mu, lam):
    """[mu, lam] in Young's lattice, ordered by containment of diagrams."""
    els = partitions_between(mu, lam)
    m = len(els)
    up = [0] * m
    for a in range(m):
        for b in range(m):
            if a != b and all(x <= y for x, y in zip(els[a], els[b])):
                up[a] |= 1 << b
    return m, tuple(up), els


def shape_to_mu_lam(shape):
    mu = tuple(a for a, b in shape)
    lam = tuple(b for a, b in shape)
    return mu, lam


# -------------------------------------------------- Young-Fibonacci lattice

def yf_words(maxrank):
    """Words in {1,2} by rank (digit sum)."""
    by = {0: [()]}
    for r in range(1, maxrank + 1):
        cur = []
        for d in (1, 2):
            for w in by.get(r - d, []):
                cur.append((d,) + w)
        by[r] = sorted(set(cur))
    return by


def yf_down_covers(w):
    """Words COVERED BY w, by the published neighbour rule for the Fibonacci
    differential poset Z(1): u is covered by w iff u is obtained from w by

      (a) deleting the leftmost 1, or
      (b) replacing by 1 a 2 that lies strictly to the LEFT of the leftmost 1
          (all 2's qualify when w contains no 1).

    The rank sizes alone do NOT pin this rule down -- several wrong rules give
    Fibonacci ranks.  What pins it down is DU - UD = I, which the self-test
    checks as an operator identity, and which is why that control is here.
    """
    out = []
    first1 = next((i for i, d in enumerate(w) if d == 1), len(w))
    if first1 < len(w):
        out.append(w[:first1] + w[first1 + 1:])
    for i in range(first1):
        if w[i] == 2:
            out.append(w[:i] + (1,) + w[i + 1:])
    return out


def yf_covers(w):
    """Words COVERING w -- the inverse of yf_down_covers, computed by search
    over the next rank rather than by a second rule."""
    cand = set()
    n = sum(w)
    for v in _yf_rank(n + 1):
        if w in yf_down_covers(v):
            cand.add(v)
    return sorted(cand)


_YF_RANK_CACHE = {0: [()]}

def _yf_rank(r):
    if r not in _YF_RANK_CACHE:
        out = [(1,) + w for w in _yf_rank(r - 1)]
        if r >= 2:
            out += [(2,) + w for w in _yf_rank(r - 2)]
        _YF_RANK_CACHE[r] = sorted(set(out))
    return _YF_RANK_CACHE[r]


def yf_poset(maxrank):
    by = yf_words(maxrank)
    els = [w for r in range(maxrank + 1) for w in by[r]]
    idx = {w: i for i, w in enumerate(els)}
    m = len(els)
    cov = [[] for _ in range(m)]
    for w in els:
        for u in yf_down_covers(w):
            assert u in idx, "down-cover left the poset: %s -> %s" % (w, u)
            cov[idx[u]].append(idx[w])
    up = [0] * m
    for w in reversed(els):
        i = idx[w]
        for j in cov[i]:
            up[i] |= (1 << j) | up[j]
    return m, tuple(up), els, idx, cov
