"""Shared machinery for the (LIB-weak) probe of mg-c3ca.

POPULATION and GRAIN, stated once and repeated at every printed count:

  * `naturally_labelled_posets(n)` enumerates every subset of the C(n,2) pairs
    (i,j) with i<j that is transitively closed.  GRAIN = one **naturally
    labelled poset** (a poset together with one compatible labelling), NOT one
    isomorphism class: an isomorphism class with k compatible labellings that
    are distinct as relation sets appears k times.  This is deliberate — every
    readout below is a max/min over the population, and duplication does not
    move a max.

  * All probabilities are over `sigma` uniform on L(P), computed EXACTLY in
    integer arithmetic (Fraction-free: counts, then one division at the end).

Definitions, matching STATE.md's glossary (`STATE.md:34-48`):

  p(x,y)  = Pr[y precedes x in sigma]  for x||y   (x <_e y at the caller's choice)
  delta(P)= max over incomparable pairs of min(p, 1-p).  delta < 1/3 = "frozen".
  E_maj   = sum over incomparable pairs of min(p, 1-p).

E_maj is the quantity this probe reports instead of E[inv_e], and the reason is
stated in the README: for any reference linear order r,
E[inv_r] = sum over incomparable pairs of (p or 1-p), so
E_maj <= E[inv_r] for EVERY r, with EQUALITY exactly when r orders every
incomparable pair the majority way.  For a frozen poset the majority order is
a linear order (the distinguished order e; elementary proof re-derived in the
README), so on the class the ticket is about, E_maj IS E[inv_e].  Off that
class E_maj is a labelling-free lower bound, which is the conservative
direction for a probe looking for LARGE E[inv_e].
"""

from itertools import combinations


def transitively_closed(n, pairs):
    """True iff `pairs` (a set of (i,j), i<j) is transitively closed."""
    for i, j in pairs:
        for k in range(j + 1, n):
            if (j, k) in pairs and (i, k) not in pairs:
                return False
    return True


def down_masks(n, pairs):
    """down[x] = bitmask of strict predecessors of x."""
    down = [0] * n
    for i, j in pairs:
        down[j] |= 1 << i
    return down


def count_extensions(n, down):
    """|L(P)| by the standard down-set DP.  Exact integer count."""
    full = (1 << n) - 1
    f = [0] * (1 << n)
    f[0] = 1
    for mask in range(1 << n):
        if not f[mask]:
            continue
        rest = full & ~mask
        m = rest
        while m:
            b = m & -m
            x = b.bit_length() - 1
            if down[x] & ~mask == 0:
                f[mask | b] += f[mask]
            m ^= b
    return f[full]


def _closure_with(n, down, lo, hi):
    """down-masks of the poset P + (lo < hi), transitively closed.

    Assumes lo || hi in P.  Returns None if the addition is inconsistent
    (cannot happen for an incomparable pair, but checked).
    """
    d = list(down)
    d[hi] |= (1 << lo) | d[lo]
    changed = True
    while changed:
        changed = False
        for z in range(n):
            if d[z] & (1 << hi):
                new = d[z] | d[hi]
                if new != d[z]:
                    d[z] = new
                    changed = True
    for z in range(n):
        if d[z] & (1 << z):
            return None
    return d


def pair_stats(n, pairs):
    """Exact per-incomparable-pair probabilities.

    Returns (total_extensions, [(x, y, p_xy_num, denom), ...]) where
    p_xy_num/denom = Pr[y precedes x] for the incomparable pair x<y (numeric
    labels), i.e. the probability the pair appears in the order OPPOSITE to the
    natural labelling.
    """
    down = down_masks(n, pairs)
    total = count_extensions(n, down)
    out = []
    for x, y in combinations(range(n), 2):
        if (x, y) in pairs:
            continue
        d = _closure_with(n, down, y, x)          # force y before x
        cnt = count_extensions(n, d) if d is not None else 0
        out.append((x, y, cnt, total))
    return total, out


def delta_and_emaj(n, pairs):
    """(delta, E_maj, n_incomparable_pairs) for one naturally labelled poset.

    delta is None when P is a chain (no incomparable pair): delta is undefined
    there and the 1/3-2/3 conjecture says nothing about chains.
    """
    total, stats = pair_stats(n, pairs)
    if not stats:
        return None, 0.0, 0
    delta = 0.0
    emaj = 0.0
    for _x, _y, cnt, tot in stats:
        p = cnt / tot
        mn = min(p, 1.0 - p)
        emaj += mn
        if mn > delta:
            delta = mn
    return delta, emaj, len(stats)


def naturally_labelled_posets(n):
    """Yield every transitively closed subset of {(i,j) : i<j}, as a frozenset.

    GRAIN: one naturally labelled poset.  See module docstring.
    """
    allpairs = list(combinations(range(n), 2))
    m = len(allpairs)
    for bits in range(1 << m):
        pairs = frozenset(allpairs[k] for k in range(m) if bits >> k & 1)
        if transitively_closed(n, pairs):
            yield pairs
