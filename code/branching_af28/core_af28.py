"""Core objects for mg-af28, built from the definitions in
`docs/OneThird-Semigroup-Walk-Family-Note.md` §1-§2 and from the published
definitions of the branching-graph objects.

Shares no code with `code/landscape_ebd8/`, `code/landscape_repair_1953/`,
`code/landscape_audit_d673/`, `code/semigroup_note/` or any other instrument in
this repo: posets are carried as tuples of up-set bitmasks, moves as tuples of
block bitmasks, and every object is rebuilt from its definition.

Pure Python 3, no dependencies, exact integer / Fraction arithmetic only.
"""

from itertools import permutations
from fractions import Fraction

# ---------------------------------------------------------------- posets ----
# A poset on n elements is a tuple `up` of length n; up[i] is the bitmask of the
# elements STRICTLY above i.  Reflexivity is never stored.


def is_poset(up):
    n = len(up)
    for i in range(n):
        if up[i] >> i & 1:
            return False
        for j in range(n):
            if up[i] >> j & 1:
                if up[j] >> i & 1:
                    return False
                if up[i] | up[j] != up[i]:      # transitivity
                    return False
    return True


def canon(up):
    """Canonical form of a poset under relabelling: min over all n! relabellings."""
    n = len(up)
    best = None
    for p in permutations(range(n)):
        rows = [0] * n
        for i in range(n):
            m = up[i]
            r = 0
            while m:
                b = m & -m
                r |= 1 << p[b.bit_length() - 1]
                m ^= b
            rows[p[i]] = r
        t = tuple(rows)
        if best is None or t < best:
            best = t
    return best


def poset_classes(n):
    """All isomorphism classes of posets on n elements.

    Built by one-point extension: every poset on n elements arises from one on
    n-1 by adjoining a new maximal element above an order ideal.  Deduplicated
    by `canon`.  This is an enumeration route independent of anything in the
    repo; the counts are certified against A000112 in selftest.py.
    """
    if n == 0:
        return [()]
    if n == 1:
        return [(0,)]
    out = {}
    for q in poset_classes(n - 1):
        m = n - 1
        for I in ideals_of(q):                 # elements strictly below the new top
            newup = []
            for i in range(m):
                r = q[i]
                if I >> i & 1:
                    r |= 1 << m                # i is below the new element
                newup.append(r)
            newup.append(0)
            t = tuple(newup)
            assert is_poset(t)
            out[canon(t)] = t
    return sorted(out.values())


def ideals_of(up):
    """All order ideals (down-closed sets) of `up`, as bitmasks, sorted by size."""
    n = len(up)
    down = [0] * n
    for i in range(n):
        m = up[i]
        while m:
            b = m & -m
            down[b.bit_length() - 1] |= 1 << i
            m ^= b
    out = []
    for S in range(1 << n):
        ok = True
        m = S
        while m:
            b = m & -m
            if down[b.bit_length() - 1] & ~S:
                ok = False
                break
            m ^= b
        if ok:
            out.append(S)
    return sorted(out, key=lambda S: (bin(S).count("1"), S))


def linear_extensions(up):
    """All linear extensions of `up`, as tuples of element indices."""
    n = len(up)
    down = [0] * n
    for i in range(n):
        m = up[i]
        while m:
            b = m & -m
            down[b.bit_length() - 1] |= 1 << i
            m ^= b
    out = []

    def rec(placed, seq):
        if placed == (1 << n) - 1:
            out.append(tuple(seq))
            return
        for i in range(n):
            if placed >> i & 1:
                continue
            if down[i] & ~placed:
                continue
            seq.append(i)
            rec(placed | 1 << i, seq)
            seq.pop()

    rec(0, [])
    return out


# ----------------------------------------------------------------- moves ----
# A move is a tuple of nonzero, disjoint bitmasks covering [n], in block order,
# subject to P-compatibility: i < j in P implies block(i) index <= block(j).


def moves_bruteforce(up):
    """All P-compatible ordered set partitions, by direct filtering of ALL
    ordered set partitions of [n].  Deliberately naive: this is the definition
    in the note, not the chains-in-J(P) route."""
    n = len(up)
    out = []

    def rec(remaining, blocks):
        if remaining == 0:
            out.append(tuple(blocks))
            return
        # the next block is ANY nonempty subset of `remaining`.  (Blocks are
        # ordered, so the usual "force the lowest remaining element into this
        # block" trick -- which is correct for unordered partitions -- would
        # lose every ordered partition whose first block omits it.)
        sub = remaining
        while sub:
            blocks.append(sub)
            rec(remaining ^ sub, blocks)
            blocks.pop()
            sub = (sub - 1) & remaining
    rec((1 << n) - 1, [])
    return [x for x in out if compatible(up, x)]


def compatible(up, blocks):
    idx = {}
    for t, B in enumerate(blocks):
        m = B
        while m:
            b = m & -m
            idx[b.bit_length() - 1] = t
            m ^= b
    n = len(up)
    for i in range(n):
        m = up[i]
        while m:
            b = m & -m
            j = b.bit_length() - 1
            if idx[i] > idx[j]:
                return False
            m ^= b
    return True


def moves_from_chains(up):
    """The same set, built as chains 0 = I_0 < I_1 < ... < I_k = 1 in J(P):
    block t is I_t \\ I_{t-1}.  This is Brown 2000 §4.3's description."""
    ids = ideals_of(up)
    idset = set(ids)
    full = (1 << len(up)) - 1
    out = []

    def rec(cur, blocks):
        if cur == full:
            out.append(tuple(blocks))
            return
        for I in ids:
            if I & cur == cur and I != cur:
                blocks.append(I ^ cur)
                rec(I, blocks)
                blocks.pop()
    assert 0 in idset and full in idset
    rec(0, [])
    return out


def move_product(x, y):
    """x . y : blocks are the nonempty B & C, ordered lexicographically by
    (index of B in x, index of C in y)."""
    out = []
    for B in x:
        for C in y:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


def support(x):
    """The commitment level: the blocks as an unordered partition."""
    return tuple(sorted(x))


def AC(up, mv=None):
    """The support lattice AC(P) = O(P): the set of levels of moves."""
    if mv is None:
        mv = moves_from_chains(up)
    return sorted({support(x) for x in mv})


def act(x, c):
    """A move acting on an ordering: block by block, in the order the elements
    already appear in c."""
    out = []
    for B in x:
        for e in c:
            if B >> e & 1:
                out.append(e)
    return tuple(out)


# ------------------------------------------------------ Young-side objects ----


def partitions(n):
    """Partitions of n, as weakly decreasing tuples."""
    out = []

    def rec(left, cap, cur):
        if left == 0:
            out.append(tuple(cur))
            return
        for p in range(min(cap, left), 0, -1):
            cur.append(p)
            rec(left - p, p, cur)
            cur.pop()
    rec(n, n, [])
    return out


def conj(lam):
    if not lam:
        return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))


def cell_poset(lam):
    """D_lambda: the cells of the Young diagram of lambda, ordered componentwise.
    Returned as (up, cells) with cells the list of (row, col) in the index order."""
    cells = [(i, j) for i, p in enumerate(lam) for j in range(p)]
    n = len(cells)
    up = []
    for a in range(n):
        r = 0
        ia, ja = cells[a]
        for b in range(n):
            ib, jb = cells[b]
            if (ia, ja) != (ib, jb) and ia <= ib and ja <= jb:
                r |= 1 << b
        up.append(r)
    return tuple(up), cells


def sub_shapes(lam):
    """All partitions mu with mu contained in lambda (the interval [0, lambda]
    of Young's lattice), built directly from containment of diagrams."""
    out = []

    def rec(i, cap, cur):
        if i == len(lam):
            t = list(cur)
            while t and t[-1] == 0:
                t.pop()
            out.append(tuple(t))
            return
        for v in range(min(lam[i], cap), -1, -1):
            cur.append(v)
            rec(i + 1, v, cur)
            cur.pop()
    rec(0, lam[0] if lam else 0, [])
    return sorted(set(out))


def hook_length_formula(lam):
    n = sum(lam)
    lc = conj(lam)
    num = 1
    for k in range(1, n + 1):
        num *= k
    den = 1
    for i, p in enumerate(lam):
        for j in range(p):
            den *= (p - j) + (lc[j] - i) - 1
    assert num % den == 0
    return num // den


def young_fibonacci(maxrank):
    """The Young-Fibonacci lattice up to rank `maxrank`.

    Vertices at rank n are the words in {1,2} with digit sum n.  The neighbour
    operations are Stanley's, as stated on the Young-Fibonacci lattice page and
    in Goodman-Kerov (the Martin boundary paper), in this form:

      up:   insert a "1" anywhere at or before the position of the leftmost "1"
            (equivalently, anywhere inside the leading block of 2s), giving
            k+1 words where k is the number of leading 2s; and, if the word
            contains a "1", change that leftmost "1" into a "2".
      down: delete the leftmost "1"; and change any "2" that has no "1" to its
            left into a "1".

    So a word with at least one 1 and k leading 2s has k+2 up-neighbours and
    k+1 down-neighbours, and an all-2s word of length k has k+1 and k -- which
    is the count stated in the literature, and the differential condition is
    used as a positive control on this implementation in t_branching.py.
    """
    ranks = {0: [()]}
    for r in range(1, maxrank + 1):
        cur = set()

        def gen(left, cur_word):
            if left == 0:
                cur.add(tuple(cur_word))
                return
            for d in (1, 2):
                if d <= left:
                    cur_word.append(d)
                    gen(left - d, cur_word)
                    cur_word.pop()
        gen(r, [])
        ranks[r] = sorted(cur)
    covers = {}
    for r in range(0, maxrank):
        for v in ranks[r]:
            k = 0
            while k < len(v) and v[k] == 2:
                k += 1
            ups = set()
            for pos in range(k + 1):               # insert a 1 at or before the leftmost 1
                ups.add(v[:pos] + (1,) + v[pos:])
            if k < len(v):                         # change the leftmost 1 into a 2
                ups.add(v[:k] + (2,) + v[k + 1:])
            covers[v] = sorted(u for u in ups if sum(u) == r + 1)
    for v in ranks[maxrank]:
        covers[v] = []
    return ranks, covers


# --------------------------------------------------------- linear algebra ----


def rank_exact(M):
    """Exact rank over Q of an integer matrix, by fraction-free elimination."""
    A = [[Fraction(x) for x in row] for row in M]
    rows, cols = len(A), (len(A[0]) if A else 0)
    r = 0
    for c in range(cols):
        piv = None
        for i in range(r, rows):
            if A[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][c]
        for i in range(r + 1, rows):
            if A[i][c] != 0:
                f = A[i][c] / pv
                Ai, Ar = A[i], A[r]
                for j in range(c, cols):
                    Ai[j] -= f * Ar[j]
        r += 1
        if r == rows:
            break
    return r
