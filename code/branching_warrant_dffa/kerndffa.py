"""kerndffa -- the kernel for mg-dffa, the warrant repair of mg-5800's F1-F4.

mg-dffa rewrites four CLAIM STATEMENTS in
`docs/OneThird-Branching-Graphs-Where-This-Lives.md`.  A repair whose entire
content is rewriting claim statements is exactly where a wrong new statement is
likeliest, so every sentence this repair writes that carries a number or an
identification is measured here first.

INDEPENDENCE.  This file imports nothing from `branching_af28/`,
`branching_audit_6ad0/`, `branching_repair_41aa/` or `branching_audit_5800/`.
Where a probe cites one of those instruments it says so and reads the committed
OUTPUT file; it never imports their code.

CANONICAL FORM.  mg-5800 recorded a control firing on its own canonical form: a
form that chose a colour class by dict-insertion order was not canonical, and
A000112 came out exactly while the bug was live.  This file does not refine at
all -- `canon` is the plain minimum over ALL n! relabellings.  That is provably
canonical and it is affordable because nothing here exceeds n = 7.  The price is
speed, and it is the right price to pay in a file whose job is warrant.

Pure Python 3, no dependencies.
"""

from itertools import permutations

# ---------------------------------------------------------------- partitions


def partitions(n, maxpart=None):
    """All partitions of `n` as weakly decreasing tuples."""
    if maxpart is None:
        maxpart = n
    if n == 0:
        return [()]
    out = []
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - first, first):
            out.append((first,) + rest)
    return out


def partitions_upto(n):
    """All partitions of 0, 1, ..., n."""
    out = []
    for m in range(n + 1):
        out.extend(partitions(m))
    return out


def partitions_in_box(rows, cols):
    """All partitions with at most `rows` parts, each part at most `cols`."""
    out = []

    def rec(prefix, remaining_rows, cap):
        out.append(tuple(prefix))
        if remaining_rows == 0:
            return
        for part in range(cap, 0, -1):
            prefix.append(part)
            rec(prefix, remaining_rows - 1, part)
            prefix.pop()

    rec([], rows, cols)
    return sorted(set(out))


def sub_partitions(lam, size=None):
    """All partitions mu with mu contained in lam (row by row).

    `size`, when given, keeps only the mu with that many cells, and prunes the
    recursion on both sides rather than filtering at the end.  Without the
    prune the box control in `w2_family.py` enumerates about twelve million
    pairs at k = 6 and takes minutes; with it, seconds.
    """
    out = []
    n = len(lam)
    # suffix[i] = the most cells rows i.. can still contribute
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + lam[i]

    def rec(i, prefix, cap, acc):
        if size is not None:
            if acc > size or acc + suffix[i] < size:
                return
        if i == n:
            if size is None or acc == size:
                while prefix and prefix[-1] == 0:
                    prefix = prefix[:-1]
                out.append(tuple(prefix))
            return
        for v in range(min(cap, lam[i]), -1, -1):
            rec(i + 1, prefix + [v], v, acc + v)

    rec(0, [], max(lam) if lam else 0, 0)
    return sorted(set(out))


# --------------------------------------------------------------- cell posets


def skew_cells(lam, mu):
    """The cells of the skew diagram lam/mu, as (row, column) pairs, 1-based.

    Returns None if mu is not contained in lam.
    """
    mu = tuple(mu) + (0,) * (len(lam) - len(mu))
    if len(mu) > len(lam):
        return None
    for i in range(len(lam)):
        if mu[i] > lam[i]:
            return None
    return [(i + 1, j + 1) for i in range(len(lam))
            for j in range(mu[i], lam[i])]


def poset_from_cells(cells):
    """The cell poset of a set of (row, col) cells: (i,j) <= (i',j') iff
    i <= i' and j <= j'.  Returns `up`, a tuple of bitmasks, up[a] holding the
    bit of every b with a <= b (a included)."""
    n = len(cells)
    up = []
    for a in range(n):
        m = 0
        for b in range(n):
            if cells[a][0] <= cells[b][0] and cells[a][1] <= cells[b][1]:
                m |= 1 << b
        up.append(m)
    return tuple(up)


def cell_poset(lam):
    """The straight cell poset D_lam."""
    return poset_from_cells(skew_cells(lam, ()))


def trim_skew(lam, mu):
    """Delete every row and every column of lam/mu that carries no cell.

    The cell poset is unchanged by this: deleting an empty row (or column)
    preserves the relative order of the rows (columns) that remain, so the
    induced order on the cells is the same.  Trimming is what bounds the search
    box in `skew_classes` -- after it, lam has at most |lam/mu| rows and at most
    |lam/mu| columns.
    """
    mu = tuple(mu) + (0,) * (len(lam) - len(mu))
    rows = [(lam[i], mu[i]) for i in range(len(lam)) if lam[i] > mu[i]]
    lam2 = tuple(r[0] for r in rows)
    mu2 = tuple(r[1] for r in rows)
    if not lam2:
        return (), ()
    # transpose, trim rows again, transpose back
    lamT = conjugate(lam2)
    muT = conjugate(mu2)
    muT = tuple(muT) + (0,) * (len(lamT) - len(muT))
    rows = [(lamT[i], muT[i]) for i in range(len(lamT)) if lamT[i] > muT[i]]
    lam3 = conjugate(tuple(r[0] for r in rows))
    mu3 = conjugate(tuple(r[1] for r in rows))
    return lam3, mu3


def conjugate(lam):
    if not lam:
        return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))


# ------------------------------------------------------------ canonical form


def canon(up):
    """The minimum of `up` over ALL n! relabellings.  No refinement, no
    heuristic ordering: this is the definition, computed."""
    n = len(up)
    best = None
    for p in permutations(range(n)):
        new = [0] * n
        for a in range(n):
            m = up[a]
            t = 0
            b = 0
            while m:
                if m & 1:
                    t |= 1 << p[b]
                m >>= 1
                b += 1
            new[p[a]] = t
        t = tuple(new)
        if best is None or t < best:
            best = t
    return best


def relabel(up, p):
    """Apply the permutation p (old index -> new index) without minimising."""
    n = len(up)
    new = [0] * n
    for a in range(n):
        t = 0
        for b in range(n):
            if up[a] >> b & 1:
                t |= 1 << p[b]
        new[p[a]] = t
    return tuple(new)


# ----------------------------------------------------------- ideals, lattices


def ideals(up):
    """Every down-set of the poset, as a bitmask.  Returned sorted."""
    n = len(up)
    down = [0] * n
    for a in range(n):
        for b in range(n):
            if up[b] >> a & 1:
                down[a] |= 1 << b
    out = []
    for mask in range(1 << n):
        ok = True
        for a in range(n):
            if mask >> a & 1 and (down[a] & ~mask):
                ok = False
                break
        if ok:
            out.append(mask)
    return sorted(out)


class Lattice(object):
    """A finite lattice given by its element list and its order relation.

    `leq[i][j]` is True iff element i <= element j.  Meets and joins are
    COMPUTED from the order and verified to exist and be unique -- nothing here
    assumes lattice-ness, because two of the four sentences this repair narrows
    turn on the difference between an order statement and a lattice statement.
    """

    def __init__(self, elements, leq):
        self.elements = list(elements)
        self.n = len(self.elements)
        self.leq = leq
        self.meet = [[None] * self.n for _ in range(self.n)]
        self.join = [[None] * self.n for _ in range(self.n)]
        self.is_lattice = True
        for a in range(self.n):
            for b in range(self.n):
                lo = [c for c in range(self.n) if leq[c][a] and leq[c][b]]
                hi = [c for c in range(self.n) if leq[a][c] and leq[b][c]]
                m = [c for c in lo if all(leq[d][c] for d in lo)]
                j = [c for c in hi if all(leq[c][d] for d in hi)]
                if len(m) != 1 or len(j) != 1:
                    self.is_lattice = False
                else:
                    self.meet[a][b] = m[0]
                    self.join[a][b] = j[0]

    def distributive(self):
        """a & (b | c) == (a & b) | (a & c) on every triple."""
        if not self.is_lattice:
            return False
        for a in range(self.n):
            for b in range(self.n):
                for c in range(self.n):
                    if (self.meet[a][self.join[b][c]]
                            != self.join[self.meet[a][b]][self.meet[a][c]]):
                        return False
        return True

    def bottom(self):
        for a in range(self.n):
            if all(self.leq[a][b] for b in range(self.n)):
                return a
        return None

    def join_irreducibles(self):
        """Elements with exactly one lower cover, bottom excluded.  For a
        finite lattice these are the elements that are not the join of the
        strictly smaller elements, which is Birkhoff's index set."""
        bot = self.bottom()
        out = []
        for a in range(self.n):
            if a == bot:
                continue
            below = [b for b in range(self.n) if self.leq[b][a] and b != a]
            if not below:
                out.append(a)
                continue
            j = below[0]
            for b in below[1:]:
                j = self.join[j][b]
            if j != a:
                out.append(a)
        return out

    def induced_poset(self, subset):
        """`up` bitmasks for the order induced on `subset`."""
        k = len(subset)
        up = []
        for i in range(k):
            m = 0
            for j in range(k):
                if self.leq[subset[i]][subset[j]]:
                    m |= 1 << j
            up.append(m)
        return tuple(up)


def lattice_of_ideals(up):
    """J(P), as a Lattice, ordered by inclusion of down-sets."""
    ids = ideals(up)
    leq = [[(ids[a] & ids[b]) == ids[a] for b in range(len(ids))]
           for a in range(len(ids))]
    return Lattice(ids, leq)


# ------------------------------------------------------------ Young's lattice


def contains(lam, mu):
    """mu subset lam, as Young diagrams."""
    if len(mu) > len(lam):
        return False
    return all(mu[i] <= lam[i] for i in range(len(mu)))


def young_interval(mu, lam):
    """The interval [mu, lam] of Young's lattice, as a Lattice whose elements
    are the PARTITIONS nu with mu subset nu subset lam.

    Built from containment of partitions only.  No cell poset, no order ideal,
    no join-irreducible, no Birkhoff -- that separation is the point of the
    probe that uses it.
    """
    els = [nu for nu in partitions_upto(sum(lam))
           if contains(lam, nu) and contains(nu, mu)]
    leq = [[contains(els[b], els[a]) for b in range(len(els))]
           for a in range(len(els))]
    return Lattice(els, leq)


def shape_of_ideal(mask, cells):
    """The partition shape filled by the cells in `mask` (straight shapes)."""
    rows = {}
    for a, (i, j) in enumerate(cells):
        if mask >> a & 1:
            rows[i] = max(rows.get(i, 0), j)
    if not rows:
        return ()
    return tuple(rows.get(i, 0) for i in range(1, max(rows) + 1))


# ------------------------------------------------------- Young-Fibonacci


def yf_words(maxrank):
    """Every word in {1,2} with digit sum at most `maxrank`, the empty word
    included."""
    out = [()]
    frontier = [()]
    while frontier:
        nxt = []
        for w in frontier:
            for d in (1, 2):
                v = (d,) + w
                if sum(v) <= maxrank:
                    nxt.append(v)
        out.extend(nxt)
        frontier = nxt
    return sorted(set(out), key=lambda w: (sum(w), w))


def yf_up_covers(s):
    """The words covering `s` in the Young-Fibonacci lattice.

    Write `s = 2^a t` with `t` empty or beginning with a 1.  Then s is covered
    by:

      * `2^i 1 2^(a-i) t` for each `i = 0 .. a` -- a 1 inserted at any of the
        `a+1` positions of the leading 2-run; and
      * `2^(a+1) t[1:]` when `t` is non-empty -- the leftmost 1 promoted to a 2.

    This is the UP direction and it is the one stated; `yf_down_covers` is
    checked against it word by word in `selftestdffa.py`.
    """
    a = 0
    while a < len(s) and s[a] == 2:
        a += 1
    t = s[a:]
    out = set()
    for i in range(a + 1):
        out.add((2,) * i + (1,) + (2,) * (a - i) + t)
    if t:
        out.add((2,) * (a + 1) + t[1:])
    return out


def yf_down_covers(w):
    """The words covered by `w` in the Young-Fibonacci lattice.

    Inverting `yf_up_covers`:

      * delete the LEFTMOST 1 of `w`, if it has one; and
      * replace by a 1 ANY 2 of `w`'s leading 2-run -- every position, not just
        the first and not just the last.  `(2,2)` covers both `(1,2)` and
        `(2,1)`, and that is where the count comes from.

    THIS RULE WAS WRONG TWICE BEFORE IT WAS RIGHT, AND THE FIBONACCI RANK SIZES
    NEVER NOTICED.  mg-5800 recorded the same failure on its own instrument.
    Two wrong rules were written here; both returned rank sizes
    1, 1, 2, 3, 5, 8, 13 and both failed `DU - UD = I` -- the first on 10 words
    checked to rank 6, the second on 22 words checked to rank 7.  (Two different
    bounds, because that is what each was run at; they are not a comparison.)
    The rank sizes are NOT a control on the cover rule.
    `w2_family.py` prints the operator identity, which is; the self-test also
    checks this function against `yf_up_covers` word by word.
    """
    out = set()
    for i, d in enumerate(w):
        if d == 1:
            out.add(w[:i] + w[i + 1:])
            break
    for i, d in enumerate(w):
        if d != 2:
            break
        out.add(w[:i] + (1,) + w[i + 1:])
    return out


def yf_leq(maxrank):
    """The order relation of the Young-Fibonacci lattice truncated at
    `maxrank`, as a dict word -> set of words below or equal to it."""
    words = yf_words(maxrank)
    below = {}
    for w in words:
        acc = {w}
        for u in yf_down_covers(w):
            acc |= below[u]
        below[w] = acc
    return words, below


def yf_interval(w, below):
    """The interval [empty word, w] as a Lattice."""
    els = sorted(below[w], key=lambda u: (sum(u), u))
    leq = [[els[a] in below[els[b]] for b in range(len(els))]
           for a in range(len(els))]
    return Lattice(els, leq)


# ------------------------------------------------------- skew-poset classes


def skew_classes(k, box=None):
    """`canon` of the cell poset of every skew shape with exactly k cells.

    `box` bounds the number of rows and columns of lam.  The default is k,
    which is enough: `trim_skew` deletes every cell-free row and column, and
    after trimming every row and every column carries a cell, so lam has at
    most k of each.  `w2_family.py` re-runs this at box = k+1 as a control on
    the bound.
    """
    if box is None:
        box = k
    if k == 0:
        return {()}
    out = set()
    seen = set()
    for lam in partitions_in_box(box, box):
        if sum(lam) < k:
            continue
        for mu in sub_partitions(lam, size=sum(lam) - k):
            # Trim first and canonicalise once per trimmed shape: many
            # (lam, mu) pairs trim to the same skew diagram, and `canon` is the
            # cost here.
            t = trim_skew(lam, mu)
            if t in seen:
                continue
            seen.add(t)
            cells = skew_cells(t[0], t[1])
            if cells is None or len(cells) != k:
                continue
            out.add(canon(poset_from_cells(cells)))
    return out
