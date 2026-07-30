"""mg-c6bc -- the audit kernel.  Built from the DEFINITIONS in the documents,
not from any instrument under audit.

Imports nothing from code/counterexample_probe_24a3/ (the target),
code/counterexample_repair_dea5/ (the repair) or code/counterexample_audit_0a11/
(the previous audit).  Pure Python 3, exact integer and rational arithmetic.

Definitions used, and where they are stated:

  poset, linear extension, e(P)          target document section 1
  p(x,y), Inc(P), delta(P) = max min     target document section 1
  delta-extremal                          delta(P) = 1/3, the value the
                                          conjecture is tight at (target
                                          document section 3: "min 3delta = 1
                                          says the conjecture is tight")
  move / P-compatible ordered partition   Semigroup-Walk-Family-Note section 1
  level, Q(P), m_X                        target document section 1
  qfrac, qmass                            target document section 4
  L*                                      target document section 2 (majority)
  cut element, cut extension, core        Repair document section 3.4

Everything below is rebuilt from those sentences.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations


# --------------------------------------------------------------- the object

class Poset(object):
    """A poset on {0..n-1}, held as transitively closed up/down bitmasks."""

    __slots__ = ("n", "up", "down")

    def __init__(self, n, up, down):
        self.n = n
        self.up = tuple(up)
        self.down = tuple(down)

    @staticmethod
    def from_relations(n, rels):
        """rels: iterable of (a, b) meaning a < b.  Transitively closed here."""
        up = [0] * n
        for a, b in rels:
            up[a] |= 1 << b
        changed = True
        while changed:
            changed = False
            for i in range(n):
                new = up[i]
                m = up[i]
                while m:
                    j = (m & -m).bit_length() - 1
                    m &= m - 1
                    new |= up[j]
                if new != up[i]:
                    up[i] = new
                    changed = True
        down = [0] * n
        for i in range(n):
            m = up[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                down[j] |= 1 << i
        return Poset(n, up, down)

    def key(self):
        return (self.n, self.up)

    def dual(self):
        return Poset(self.n, self.down, self.up)

    def induced(self, mask):
        """The subposet on the elements of `mask`, relabelled 0..k-1."""
        elems = bits(mask)
        idx = {e: i for i, e in enumerate(elems)}
        k = len(elems)
        up = [0] * k
        for e in elems:
            m = self.up[e] & mask
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                up[idx[e]] |= 1 << idx[j]
        down = [0] * k
        for i in range(k):
            m = up[i]
            while m:
                j = (m & -m).bit_length() - 1
                m &= m - 1
                down[j] |= 1 << i
        return Poset(k, up, down)

    def covers(self):
        """Cover relations, for printing."""
        out = []
        for a in range(self.n):
            m = self.up[a]
            while m:
                b = (m & -m).bit_length() - 1
                m &= m - 1
                if not (self.up[a] & self.down[b]):
                    out.append((a, b))
        return sorted(out)

    def cover_string(self):
        return " ".join("%d<%d" % (a, b) for a, b in self.covers())


def bits(m):
    out = []
    while m:
        b = (m & -m).bit_length() - 1
        out.append(b)
        m &= m - 1
    return out


def popcount(m):
    return bin(m).count("1")


# ------------------------------------------------------- canonical labelling

def canonical(P):
    """A canonical form: the lexicographically least up-mask tuple over all
    relabellings that respect the colour refinement.  Colour is an isomorphism
    invariant, so restricting to colour-respecting relabellings is sound."""
    n = P.n
    sig0 = [(popcount(P.up[i]), popcount(P.down[i])) for i in range(n)]
    base = sorted(set(sig0))
    colour = [base.index(s) for s in sig0]
    while True:
        sig = [(colour[i],
                tuple(sorted(colour[j] for j in bits(P.up[i]))),
                tuple(sorted(colour[j] for j in bits(P.down[i]))))
               for i in range(n)]
        order = sorted(set(sig))
        new = [order.index(s) for s in sig]
        if _same_partition(new, colour):
            colour = new
            break
        colour = new
    classes = {}
    for i in range(n):
        classes.setdefault(colour[i], []).append(i)
    ordered = [classes[c] for c in sorted(classes)]
    best = None
    for perm in _class_perms(ordered):
        pos = [0] * n
        for slot, v in enumerate(perm):
            pos[v] = slot
        up = [0] * n
        for v in range(n):
            m = P.up[v]
            while m:
                w = (m & -m).bit_length() - 1
                m &= m - 1
                up[pos[v]] |= 1 << pos[w]
        t = tuple(up)
        if best is None or t < best:
            best = t
    return (n, best)


def _same_partition(a, b):
    ma, mb = {}, {}
    for i, (x, y) in enumerate(zip(a, b)):
        ma.setdefault(x, []).append(i)
        mb.setdefault(y, []).append(i)
    return sorted(map(tuple, ma.values())) == sorted(map(tuple, mb.values()))


def _class_perms(ordered):
    if not ordered:
        yield []
        return
    head, rest = ordered[0], ordered[1:]
    for p in permutations(head):
        for tail in _class_perms(rest):
            yield list(p) + tail


# ------------------------------------------------------ linear extension data

def le_data(P):
    """Returns (e, cnt) with cnt[x][y] = #linear extensions listing x before y."""
    n = P.n
    full = (1 << n) - 1
    down = P.down
    f = [0] * (1 << n)
    f[0] = 1
    for S in range(1 << n):
        if not f[S]:
            continue
        for i in range(n):
            if S >> i & 1:
                continue
            if down[i] & ~S:
                continue
            f[S | (1 << i)] += f[S]
    g = [0] * (1 << n)
    g[full] = 1
    for S in range(full, -1, -1):
        if S == full:
            continue
        tot = 0
        for i in range(n):
            if S >> i & 1:
                continue
            if down[i] & ~S:
                continue
            tot += g[S | (1 << i)]
        g[S] = tot
    e = f[full]
    cnt = [[0] * n for _ in range(n)]
    for S in range(1 << n):
        fS = f[S]
        if not fS:
            continue
        xs = bits(S)
        for y in range(n):
            if S >> y & 1:
                continue
            if down[y] & ~S:
                continue
            w = fS * g[S | (1 << y)]
            if not w:
                continue
            row = cnt
            for x in xs:
                row[x][y] += w
    return e, cnt


def sub_le_counts(P):
    """e(P|_B) for every subset B, by one DP."""
    n = P.n
    up = P.up
    eB = [0] * (1 << n)
    eB[0] = 1
    for B in range(1, 1 << n):
        tot = 0
        for i in bits(B):
            if not (up[i] & B):            # i maximal in P|_B
                tot += eB[B & ~(1 << i)]
        eB[B] = tot
    return eB


# ---------------------------------------------------------- the record of P

class Record(object):
    __slots__ = ("e", "delta", "qmass", "qfrac", "tiefree", "acyclic",
                 "lstar", "nlevels")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)


def analyse(P, want_q=True):
    """Full record, or None if P is a chain / tied / majority-cyclic."""
    n = P.n
    e, cnt = le_data(P)
    inc = []
    for x in range(n):
        for y in range(x + 1, n):
            if not (P.up[x] >> y & 1) and not (P.down[x] >> y & 1):
                inc.append((x, y))
    if not inc:
        return None                                    # chain
    for x, y in inc:
        if cnt[x][y] == cnt[y][x]:
            return None                                # tied
    delta = max(Fraction(min(cnt[x][y], cnt[y][x]), e) for x, y in inc)
    # majority relation: x -> y iff more extensions put x before y
    adj = [0] * n
    for x in range(n):
        for y in range(n):
            if x != y and cnt[x][y] > cnt[y][x]:
                adj[x] |= 1 << y
    lstar = _topo_total(n, adj)
    if lstar is None:
        return None                                    # majority cycle
    if not want_q:
        return Record(e=e, delta=delta, qmass=None, qfrac=None,
                      tiefree=True, acyclic=True, lstar=lstar, nlevels=None)
    qm, qf, nlev = _q_stats(P, e, lstar)
    return Record(e=e, delta=delta, qmass=qm, qfrac=qf, tiefree=True,
                  acyclic=True, lstar=lstar, nlevels=nlev)


def _topo_total(n, adj):
    """The majority relation is a tournament; return the linear order if it is
    acyclic (i.e. transitive/total), else None."""
    order = sorted(range(n), key=lambda v: -popcount(adj[v]))
    for i in range(n):
        for j in range(i + 1, n):
            if not (adj[order[i]] >> order[j] & 1):
                return None
    return order


# ------------------------------------------------------------ levels, m_X, q

def _partitions(elems):
    """All set partitions of a list of elements, as tuples of bitmasks."""
    if not elems:
        yield ()
        return
    first, rest = elems[0], elems[1:]
    for sub in _partitions(rest):
        for i in range(len(sub)):
            yield sub[:i] + (sub[i] | (1 << first),) + sub[i + 1:]
        yield sub + ((1 << first),)


def _is_level(P, blocks):
    """A partition is a level iff some ordering of its blocks is P-compatible,
    iff the block digraph (i<j across distinct blocks) is acyclic."""
    k = len(blocks)
    idx = {}
    for bi, B in enumerate(blocks):
        for x in bits(B):
            idx[x] = bi
    adj = [0] * k
    for x in range(P.n):
        m = P.up[x]
        while m:
            y = (m & -m).bit_length() - 1
            m &= m - 1
            if idx[x] != idx[y]:
                adj[idx[x]] |= 1 << idx[y]
    # Kahn
    indeg = [0] * k
    for a in range(k):
        for b in bits(adj[a]):
            indeg[b] += 1
    stack = [a for a in range(k) if indeg[a] == 0]
    seen = 0
    while stack:
        a = stack.pop()
        seen += 1
        for b in bits(adj[a]):
            indeg[b] -= 1
            if indeg[b] == 0:
                stack.append(b)
    return seen == k


def _q_stats(P, e, lstar):
    n = P.n
    eB = sub_le_counts(P)
    levels = {}
    for blocks in _partitions(list(range(n))):
        key = tuple(sorted(blocks))
        if key in levels:
            continue
        if _is_level(P, key):
            levels[key] = None
    # Mobius over refinement, restricted to levels
    order = sorted(levels, key=lambda k: -len(k))       # finest first
    order = sorted(levels, key=lambda k: len(k), reverse=True)
    m = {}
    for X in order:
        prod = 1
        for B in X:
            prod *= eB[B]
        s = 0
        for Y in _refinements(X):
            if Y == X:
                continue
            if Y in levels:
                s += m[Y]
        m[X] = prod - s
    # L*-interval partitions: blocks are contiguous runs of lstar
    tot = 0
    ncomp = 0
    for cut in range(1 << (n - 1)):
        blocks = []
        cur = 1 << lstar[0]
        for i in range(1, n):
            if cut >> (i - 1) & 1:
                blocks.append(cur)
                cur = 0
            cur |= 1 << lstar[i]
        blocks.append(cur)
        key = tuple(sorted(blocks))
        ncomp += 1
        if key not in levels:
            raise AssertionError("L*-interval partition is not a level")
        tot += m[key]
    assert ncomp == 1 << (n - 1)
    return Fraction(tot, e), Fraction(1 << (n - 1), len(levels)), len(levels)


def _refinements(X):
    """All partitions refining the partition X (as tuples of bitmasks)."""
    if not X:
        yield ()
        return
    head, rest = X[0], X[1:]
    heads = list(_partitions(bits(head)))
    for tail in _refinements(rest):
        for h in heads:
            yield tuple(sorted(h + tail))


# ------------------------------------------------------- cut elements, cores

def cut_elements(P):
    full = (1 << P.n) - 1
    return [x for x in range(P.n)
            if (P.up[x] | P.down[x]) == (full & ~(1 << x))]


def core(P):
    Q = P
    while True:
        cs = cut_elements(Q)
        if not cs or Q.n == 0:
            return Q
        Q = Q.induced(((1 << Q.n) - 1) & ~(1 << cs[0]))


def cut_extensions(P):
    """Every Q on n+1 elements having a cut element x with Q - x = P, up to iso.
    x sits above a down-set D and below its complement; for x to be a cut
    element D must be a down-set whose complement is an up-set -- i.e. any
    down-set at all -- AND every element of D must be below every element of
    the complement already.  Those D are exactly the 'cut points' of P."""
    out = {}
    n = P.n
    full = (1 << n) - 1
    for D in range(1 << n):
        # D must be a down-set
        ok = True
        for i in bits(D):
            if P.down[i] & ~D:
                ok = False
                break
        if not ok:
            continue
        U = full & ~D
        # every element of D strictly below every element of U
        good = True
        for i in bits(D):
            if (P.up[i] & U) != U:
                good = False
                break
        if not good:
            continue
        rels = []
        for a in range(n):
            for b in bits(P.up[a]):
                rels.append((a, b))
        for a in bits(D):
            rels.append((a, n))
        for b in bits(U):
            rels.append((n, b))
        Q = Poset.from_relations(n + 1, rels)
        out[canonical(Q)] = Q
    return out


# --------------------------------------------------------------- generation

def all_posets(n):
    """Every poset on n elements up to isomorphism, by adjoining a maximal
    element above an arbitrary down-set of a poset on n-1 elements."""
    if n == 0:
        return {canonical(Poset(0, [], [])): Poset(0, [], [])}
    if n == 1:
        P = Poset(1, [0], [0])
        return {canonical(P): P}
    prev = all_posets(n - 1)
    out = {}
    for P in prev.values():
        for D in _down_sets(P):
            rels = []
            for a in range(P.n):
                for b in bits(P.up[a]):
                    rels.append((a, b))
            for a in bits(D):
                rels.append((a, P.n))
            Q = Poset.from_relations(n, rels)
            out.setdefault(canonical(Q), Q)
    return out


def all_posets_bounded(n, emax):
    """Every poset on n elements up to isomorphism with e(P) <= emax.
    Sound because deleting a maximal element cannot increase e: the restriction
    map L(Q) -> L(Q-x) is surjective, so e(Q-x) <= e(Q).  Hence the family
    {e <= emax} is closed under deletion of a maximal element and incremental
    generation with pruning is complete."""
    cur = {}
    P = Poset(1, [0], [0])
    cur[canonical(P)] = P
    for k in range(2, n + 1):
        nxt = {}
        for P in cur.values():
            for D in _down_sets(P):
                rels = []
                for a in range(P.n):
                    for b in bits(P.up[a]):
                        rels.append((a, b))
                for a in bits(D):
                    rels.append((a, P.n))
                Q = Poset.from_relations(k, rels)
                key = canonical(Q)
                if key in nxt:
                    continue
                e, _ = le_data(Q)
                if e <= emax:
                    nxt[key] = Q
        cur = nxt
    return cur


def _down_sets(P):
    out = []
    for D in range(1 << P.n):
        ok = True
        for i in bits(D):
            if P.down[i] & ~D:
                ok = False
                break
        if ok:
            out.append(D)
    return out
