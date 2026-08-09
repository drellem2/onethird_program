"""mg-d3c7 — INDEPENDENT re-derivation library for the audit of mg-3969.

Written from the SOURCE definitions, read at
`~/Library/Mobile Documents/com~apple~CloudDocs/spectral_near_ordinal_sum_program.tex`:

  * `p_xy`      `:59-66`   — `p_xy = Pr_{sigma in LE(P)}[x before y]`,
                             `delta(P) = max_{x || y} min(p_xy, 1-p_xy)`.
  * `sigma(A)`  `:239-250` — `K_k(sigma) = |A_k \\ sigma(A_k)|` is described in the
                             source as "the number of prefix elements lying after
                             position k", which FIXES the reading: `sigma(A)` is the
                             set of elements occupying the positions in `A`, i.e. for
                             `A = A_k` it is the set of the first `k` elements of the
                             linear extension.
  * `Delta_1`   `:270-278` — `Delta_1(A,B) = E|A \\ sigma(A)| / min(|A|,|B|)`.

NOTHING here is derived from `code/eps0_threshold_3969/`. The poset enumeration,
the linear-extension counting and the pair probabilities are all built here from
the definitions above. Exact `Fraction` throughout; no float on any decision path.

Population. A "prefix cut" presupposes a linear extension to take a prefix OF, so
the natural population of (poset, cut) pairs is NATURALLY LABELLED posets on [n]
-- posets on the ground set {0..n-1} for which the identity order is a linear
extension -- together with `A_k = {0..k-1}` for `k = 1..n-1`. Every (poset,
linear extension, prefix cut) triple appears exactly once this way.
"""

from fractions import Fraction
from functools import lru_cache


# --------------------------------------------------------------------------
# Posets as bitmask "down" relations on {0..n-1}, naturally labelled.
# rel[j] = bitmask of elements strictly BELOW j.  Transitively closed.
# Natural labelling => rel[j] only ever has bits < j.
# --------------------------------------------------------------------------

def naturally_labelled_posets(n):
    """Yield every naturally labelled poset on [n] as a tuple rel[0..n-1].

    Built incrementally: a naturally labelled poset on [n] is a naturally
    labelled poset Q on [n-1] plus a choice of DOWN-SET D of Q to serve as the
    strict-predecessor set of the new top element n-1.  (D must be a down-set,
    or transitivity fails; conversely any down-set works and the natural
    labelling is preserved because n-1 is above nothing.)
    """
    if n == 0:
        yield ()
        return
    for q in naturally_labelled_posets(n - 1):
        for d in down_sets(q, n - 1):
            yield q + (d,)


def down_sets(rel, n):
    """All down-sets (order ideals) of the poset `rel` on [n], as bitmasks."""
    out = [0]
    for j in range(n):
        below = rel[j]
        nxt = []
        for s in out:
            nxt.append(s)
            # j may join iff everything strictly below j is already in s
            if below & ~s == 0:
                nxt.append(s | (1 << j))
        out = nxt
    # `out` may contain duplicates? No: each subset appears at most once,
    # because membership of each j is decided exactly once.
    return out


def is_chain(rel, n):
    """True iff the poset is a total order (every pair comparable)."""
    for j in range(n):
        # in a naturally labelled chain, everything below j is exactly {0..j-1}
        if rel[j] != (1 << j) - 1:
            return False
    return True


def induced(rel, n, mask):
    """Induced subposet on the elements of `mask`, relabelled 0..k-1 in
    increasing order of original label (so it stays naturally labelled)."""
    elems = [i for i in range(n) if mask >> i & 1]
    idx = {e: t for t, e in enumerate(elems)}
    sub = []
    for e in elems:
        b = 0
        below = rel[e] & mask
        for f in elems:
            if below >> f & 1:
                b |= 1 << idx[f]
        sub.append(b)
    return tuple(sub), len(elems), elems


# --------------------------------------------------------------------------
# Linear extension counting by down-set DP.
# --------------------------------------------------------------------------

def le_dp(rel, n):
    """Return (ideals, up, down, total).

    `ideals` : list of every down-set bitmask.
    `up[S]`  : number of linear orderings of S that are valid prefixes
               (= number of maximal chains from 0 to S in the ideal lattice).
    `down[S]`: number of ways to order [n]\\S as a valid suffix.
    `total`  : e(P) = number of linear extensions.
    """
    ids = down_sets(rel, n)
    idset = set(ids)
    full = (1 << n) - 1

    up = {0: 1}
    for s in sorted(ids, key=lambda m: bin(m).count("1")):
        if s == 0:
            continue
        tot = 0
        m = s
        while m:
            b = m & -m
            m ^= b
            prev = s ^ b
            if prev in idset:
                # b may be last iff s\{b} is a down-set (i.e. b maximal in s)
                tot += up[prev]
        up[s] = tot

    down = {full: 1}
    for s in sorted(ids, key=lambda m: -bin(m).count("1")):
        if s == full:
            continue
        tot = 0
        rest = full ^ s
        m = rest
        while m:
            b = m & -m
            m ^= b
            nxt = s | b
            if nxt in idset:
                tot += down[nxt]
        down[s] = tot

    return ids, up, down, up[full]


def delta1(rel, n, k, dp=None):
    """Delta_1(A_k, B) with A_k = {0..k-1}, as an exact Fraction.

    E|A_k \\ sigma(A_k)| = k - E|A_k ∩ (first k elements)|, and the set of
    "first k elements" ranges over the SIZE-k DOWN-SETS S with weight
    up[S]*down[S].
    """
    if dp is None:
        dp = le_dp(rel, n)
    ids, up, down, total = dp
    amask = (1 << k) - 1
    acc = 0
    for s in ids:
        if bin(s).count("1") != k:
            continue
        w = up[s] * down[s]
        if w:
            acc += w * bin(s & amask).count("1")
    # E|A ∩ first-k| = acc/total ; E|A \ sigma(A)| = k - that
    num = k * total - acc
    return Fraction(num, total * min(k, n - k))


def pair_probs(rel, n, dp=None):
    """p_xy for every incomparable ordered pair (x,y), exact Fractions.

    p_xy = (# linear extensions with x before y) / e(P).
    Counted by summing, over every down-set S that contains x but not y and
    from which y is immediately placeable, the completions -- equivalently and
    more simply: a linear extension has x before y iff the down-set formed by
    the elements up to and including x excludes y.  We use the direct
    formulation: for each down-set S, up[S]*down[S] counts the extensions whose
    first |S| elements are exactly S; x is before y iff there is a prefix
    containing x but not y.  Summing over the UNIQUE such prefix (the one of
    size = position of y, minus...) is fiddly, so instead we count extensions
    in which y sits at each position and x is already placed.
    """
    ids, up, down, total = dp if dp else le_dp(rel, n)
    idset = set(ids)
    # before[x][y] = # LEs with x before y, for x != y
    before = [[0] * n for _ in range(n)]
    # For each down-set S and each y placeable at S (i.e. S|{y} is a down-set),
    # the extensions whose first |S| elements are S and whose (|S|+1)-th is y
    # number up[S] * down[S | {y}].  In all of them, exactly the members of S
    # precede y.
    for s in ids:
        u = up[s]
        if not u:
            continue
        for y in range(n):
            if s >> y & 1:
                continue
            nxt = s | (1 << y)
            if nxt not in idset:
                continue
            w = u * down[nxt]
            if not w:
                continue
            m = s
            while m:
                b = m & -m
                m ^= b
                before[b.bit_length() - 1][y] += w
    return before, total


def incomparable_pairs(rel, n):
    out = []
    for x in range(n):
        for y in range(x + 1, n):
            if not (rel[y] >> x & 1) and not (rel[x] >> y & 1):
                out.append((x, y))
    return out


THIRD = Fraction(1, 3)
TWOTHIRD = Fraction(2, 3)


def balanced(p):
    return THIRD <= p <= TWOTHIRD
