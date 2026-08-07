"""libA832 — mg-832f's own library for the INDEPENDENT AUDIT of mg-6bc2.

Written from STATE.md's statements of the definitions and from first principles.
It shares no line with code/pairbias_sharpening_6bc2/, code/perslot_symmetry_200d/,
code/dual_certificate_131e/ or code/pairbias_repair_ba78/ -- none of those files was
opened before this one was written.

Exact rationals everywhere (fractions.Fraction). There is no numpy on this machine, so
the simplex below is hand-written; that is a constraint, not a virtue, and it is why
Bland's rule is used unconditionally rather than a faster pivot rule.

Conventions, fixed here once so no script can drift:

  * A permutation sigma of {0..n-1} is a TUPLE giving the WORD: sigma[i] is the element
    occupying position i.  pos_sigma(x) = sigma.index(x).
  * The reference order e is ALWAYS the identity word (0,1,...,n-1) after relabelling.
    STATE.md:42 says the relabelling is load-bearing; every caller here relabels first
    and asserts it did.
  * A pair {x,y} with x < y is FLIPPED by sigma iff y appears before x.
  * inv_e(sigma) counts flipped INCOMPARABLE pairs.  For an abstract measure on S_n
    there is no poset, so every pair is incomparable and inv_e is the Kendall distance.
  * footrule(sigma) = sum_x |pos_sigma(x) - x|.
"""

from fractions import Fraction as F
from itertools import permutations, combinations

# ---------------------------------------------------------------- permutations


def all_perms(n):
    return list(permutations(range(n)))


def flipped_pairs(sigma):
    """Set of pairs (x, y), x < y, that sigma flips against the identity."""
    pos = {x: i for i, x in enumerate(sigma)}
    return {(x, y) for x, y in combinations(range(len(sigma)), 2) if pos[y] < pos[x]}


def kendall(sigma, incomparable=None):
    """inv_e(sigma).  If `incomparable` is given, only those pairs are counted."""
    fl = flipped_pairs(sigma)
    return len(fl) if incomparable is None else len(fl & set(incomparable))


def footrule(sigma):
    return sum(abs(sigma.index(x) - x) for x in range(len(sigma)))


# ---------------------------------------------------------------- posets
# A poset on {0..n-1} is stored as `less`: a frozenset of pairs (i, j) meaning i < j.
# We enumerate NATURALLY LABELLED posets: less subset of {(i,j) : i < j}.  Every
# isomorphism class has at least one naturally labelled representative, so a maximum
# taken over this family is the maximum over all posets on n elements.


def is_transitive(less, n):
    for i, j in less:
        for k in range(n):
            if (j, k) in less and (i, k) not in less:
                return False
    return True


def naturally_labelled_posets(n):
    """All transitively closed subsets of the strict upper triangle on {0..n-1}."""
    upper = list(combinations(range(n), 2))
    out = []
    for mask in range(1 << len(upper)):
        less = frozenset(upper[b] for b in range(len(upper)) if mask >> b & 1)
        if is_transitive(less, n):
            out.append(less)
    return out


def incomparable_pairs(less, n):
    return [(i, j) for i, j in combinations(range(n), 2)
            if (i, j) not in less and (j, i) not in less]


def linear_extensions(less, n):
    """All words that respect `less`.  Direct filter -- correct, and n <= 7 here."""
    out = []
    for sigma in permutations(range(n)):
        pos = {x: i for i, x in enumerate(sigma)}
        if all(pos[i] < pos[j] for i, j in less):
            out.append(sigma)
    return out


def count_extensions(less_set, n):
    """#linear extensions, by downset DP.  O(2^n) rather than O(n!)."""
    below = [0] * n
    for i, j in less_set:
        below[j] |= 1 << i
    f = [0] * (1 << n)
    f[0] = 1
    for D in range(1, 1 << n):
        tot = 0
        for x in range(n):
            bx = 1 << x
            if D & bx and (below[x] & ~(D ^ bx)) == 0:
                tot += f[D ^ bx]
        f[D] = tot
    return f[(1 << n) - 1]


def close_with(less_set, n, x, y):
    """Transitive closure of `less_set` plus the relation x < y.  Returns None if that
    would create a cycle (i.e. if y < x already)."""
    rel = set(less_set)
    if (y, x) in rel:
        return None
    down_x = {x} | {a for a in range(n) if (a, x) in rel}
    up_y = {y} | {b for b in range(n) if (y, b) in rel}
    for a in down_x:
        for b in up_y:
            if a == b:
                return None
            rel.add((a, b))
    return frozenset(rel)


def pair_probabilities(less, n):
    """{(x, y): Pr[x before y]} for every incomparable pair x < y, exact Fractions.

    Pr[x before y] = e(P + (x<y)) / e(P): the linear extensions putting x first are
    exactly the linear extensions of the poset with that relation added.  Derived here,
    not read from anywhere.
    """
    e_total = count_extensions(less, n)
    out = {}
    for x, y in incomparable_pairs(less, n):
        q = close_with(less, n, x, y)
        out[(x, y)] = F(count_extensions(q, n), e_total)
    return out


def delta(less, n):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  0 if P is a chain."""
    ps = pair_probabilities(less, n)
    if not ps:
        return F(0)
    return max(min(p, 1 - p) for p in ps.values())


def majority_order(less, n, threshold=F(2, 3)):
    """The distinguished order e: the >=`threshold`-majority tournament, IF it is a
    complete transitive tournament.  Returns the word, or None.

    P15's guard, bound in the library rather than in a script so no script can bypass
    it: this returns None rather than falling back to the natural labelling.  `e` is
    the >2/3-majority order (STATE.md:45); a poset for which that tournament is
    incomplete or intransitive has no `e`, and inv_e is then undefined, not zero.
    """
    ps = pair_probabilities(less, n)
    beats = {}                                    # beats[(a,b)] = a before b in e
    for i, j in combinations(range(n), 2):
        if (i, j) in less:
            p = F(1)
        elif (j, i) in less:
            p = F(0)
        else:
            p = ps[(i, j)]
        if p >= threshold:
            beats[(i, j)] = True
        elif 1 - p >= threshold:
            beats[(i, j)] = False
        else:
            return None                           # incomplete: no distinguished order
    wins = [0] * n
    for (i, j), ij in beats.items():
        if ij:
            wins[i] += 1
        else:
            wins[j] += 1
    # A tournament is transitive iff its out-degrees are all distinct, i.e. iff the
    # sorted out-degree vector is 0,1,...,n-1.  That is the whole test; there is no
    # separate 3-cycle scan to write.
    if sorted(wins) != list(range(n)):
        return None                               # intransitive: a strong 3-cycle
    return tuple(sorted(range(n), key=lambda x: -wins[x]))


def relabel(less, n, order):
    """Relabel so that `order` becomes the identity.  Returns the new `less`."""
    rank = {x: r for r, x in enumerate(order)}
    return frozenset((rank[i], rank[j]) for i, j in less)


def expected_inv(less, n):
    """E[inv_e] under uniform sigma on L(P), with e the >=2/3-majority order.

    Returns None if e does not exist.  Computed from the pair probabilities, so it is
    linearity of expectation applied directly -- the same three ingredients as the
    hand derivation, run on a real poset instead of on the relaxation.
    """
    order = majority_order(less, n)
    if order is None:
        return None
    r = relabel(less, n, order)
    ps = pair_probabilities(r, n)
    # after relabelling, e is the identity, so a pair (x, y) with x < y is flipped with
    # probability 1 - Pr[x before y].
    return sum(1 - p for p in ps.values())


# ---------------------------------------------------------------- exact simplex
# Two-phase, Bland's rule, Fractions.  Solves
#     max c.x   s.t.  A_le x <= b_le,  A_eq x = b_eq,  x >= 0
# and returns (value, x) or (None, None) if infeasible.


def _pivot(T, basis, r, c):
    piv = T[r][c]
    T[r] = [v / piv for v in T[r]]
    for i in range(len(T)):
        if i != r and T[i][c] != 0:
            f = T[i][c]
            T[i] = [a - f * b for a, b in zip(T[i], T[r])]
    basis[r] = c


def _run(T, basis, ncols):
    while True:
        col = -1
        for j in range(ncols):
            if T[-1][j] < 0:
                col = j                                   # Bland: lowest index
                break
        if col < 0:
            return
        row, best = -1, None
        for i in range(len(T) - 1):
            if T[i][col] > 0:
                ratio = T[i][-1] / T[i][col]
                if best is None or ratio < best or (ratio == best and basis[i] < basis[row]):
                    row, best = i, ratio
        if row < 0:
            raise RuntimeError("unbounded")
        _pivot(T, basis, row, col)


def lp_max(c, A_le, b_le, A_eq=None, b_eq=None):
    A_eq = A_eq or []
    b_eq = b_eq or []
    n = len(c)
    rows = []
    for a, b in zip(A_le, b_le):
        rows.append((list(a), F(b), "le"))
    for a, b in zip(A_eq, b_eq):
        rows.append((list(a), F(b), "eq"))
    for k, (a, b, kind) in enumerate(rows):
        if b < 0:
            rows[k] = ([-v for v in a], -b, kind)
    m = len(rows)
    nslack = sum(1 for _, _, k in rows if k == "le")
    total = n + nslack + m
    T, basis, s = [], [], 0
    for a, b, kind in rows:
        row = [F(v) for v in a] + [F(0)] * (nslack + m) + [F(b)]
        if kind == "le":
            row[n + s] = F(1)
            s += 1
        row[n + nslack + len(T)] = F(1)
        basis.append(n + nslack + len(T))
        T.append(row)
    obj = [F(0)] * (total + 1)
    for i in range(m):
        obj[n + nslack + i] = F(1)
    T.append([F(0)] * (total + 1))
    for i in range(m):
        T[-1] = [a - b for a, b in zip(T[-1], T[i])]
    for i in range(m):
        T[-1][n + nslack + i] = F(0)
    _run(T, basis, n + nslack)
    if -T[-1][-1] != 0:
        return None, None                                  # phase 1 optimum > 0
    for i in range(m):
        for r in range(len(T)):
            T[r][n + nslack + i] = F(0)
    T[-1] = [F(0)] * (total + 1)
    for j in range(n):
        T[-1][j] = -F(c[j])
    for i in range(m):
        if basis[i] < n and T[-1][basis[i]] != 0:
            f = T[-1][basis[i]]
            T[-1] = [a - f * b for a, b in zip(T[-1], T[i])]
    _run(T, basis, n + nslack)
    x = [F(0)] * n
    for i in range(m):
        if basis[i] < n:
            x[basis[i]] = T[i][-1]
    return T[-1][-1], x


# ---------------------------------------------------------------- poset generation
# A naturally labelled poset on [n] is a naturally labelled poset on [n-1] plus an
# order ideal of it, taken as the down-set of the new element n-1.  That is a
# bijection, so this generates each one exactly once and rejects nothing.


def order_ideals(less, k):
    below = [set() for _ in range(k)]
    for i, j in less:
        below[j].add(i)
    out = []
    for mask in range(1 << k):
        S = {x for x in range(k) if mask >> x & 1}
        if all(below[x] <= S for x in S):
            out.append(S)
    return out


def gen(n):
    cur = [frozenset()]
    for k in range(1, n):
        nxt = []
        for less in cur:
            for D in order_ideals(less, k):
                nxt.append(less | frozenset((d, k) for d in D))
        cur = nxt
    return cur


def delta_le(less, n, thresh):
    """(delta(P) <= thresh, delta) with EARLY ABORT at the first pair over thresh."""
    inc = incomparable_pairs(less, n)
    if not inc:
        return True, F(0)
    tot = count_extensions(less, n)
    worst = F(0)
    for x, y in inc:
        p = F(count_extensions(close_with(less, n, x, y), n), tot)
        b = min(p, 1 - p)
        if b > thresh:
            return False, b
        worst = max(worst, b)
    return True, worst


def primitive(less, n):
    """Incomparability graph connected  <=>  not an ordinal sum  <=>  lambda_std < 1."""
    if n == 1:
        return False
    adj = {x: set() for x in range(n)}
    for x, y in incomparable_pairs(less, n):
        adj[x].add(y)
        adj[y].add(x)
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in adj[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == n
