"""mg-3969 — shared exact machinery for the eps_0 THRESHOLD question.

Everything is exact `Fraction` arithmetic. No float appears on any decision
path (floats are used only in the `%.4f` of printed report lines).

Source definitions re-implemented here, quoted at the site:

  Delta_1(A,B) = E_sigma |A \\ sigma(A)| / min(|A|,|B|)
      (`spectral_near_ordinal_sum_program.tex:270-278`)
  Phi_P(A)     = E_sigma |A \\ sigma(A)| / |A|,  for 0 < |A| <= n/2
      (`:229-237`)
  p_xy         = Pr_{sigma in L(P)}[x precedes y]      (`:59-62`)
  delta(P)     = max_{x || y} min(p_xy, 1-p_xy)        (`:63-66`)

`sigma` is in ONE-LINE notation: `sigma(a)` is the element occupying position
`a` (`:56-57`).  So `sigma(A_k)` for `A_k = {1..k}` is the SET OF ELEMENTS IN
THE FIRST k POSITIONS, and `A_k \\ sigma(A_k)` counts prefix elements sitting
after position k -- which is exactly the source's own gloss at `:248-250`.

Poset encoding: a poset on the ground set [n] = {0,...,n-1} for which the
identity order 0 < 1 < ... < n-1 is a linear extension is exactly a
transitively closed set of pairs (i,j) with i < j.  Enumerating those
enumerates EVERY isomorphism class (every finite poset has a linear
extension, so it can be relabelled into this normal form), with multiplicity.
"""

from fractions import Fraction
from itertools import combinations, permutations


# ----------------------------------------------------------------- posets ---

def poset_iter(n):
    """Yield every poset on [n] admitting 0<1<...<n-1 as a linear extension.

    Encoded as a frozenset of strict relations (i,j), i<j, transitively
    closed.  Covers every isomorphism class on n elements (with multiplicity).
    """
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    for mask in range(1 << m):
        rel = set()
        for b in range(m):
            if mask >> b & 1:
                rel.add(pairs[b])
        # transitivity check (relation is already irreflexive + antisymmetric
        # by construction, since every pair points from smaller to larger)
        ok = True
        for (a, b) in rel:
            for (c, d) in rel:
                if b == c and (a, d) not in rel:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield frozenset(rel)


def linear_extensions(n, rel):
    """All linear extensions, each as a tuple `sigma` in ONE-LINE notation:
    sigma[a] = the element at position a."""
    below = {j: {i for (i, jj) in rel if jj == j} for j in range(n)}
    out = []

    def rec(placed, order):
        if len(order) == n:
            out.append(tuple(order))
            return
        for x in range(n):
            if x in placed:
                continue
            if below[x] <= placed:
                rec(placed | {x}, order + [x])

    rec(frozenset(), [])
    return out


def incomparable(n, rel):
    return [(x, y) for x, y in combinations(range(n), 2)
            if (x, y) not in rel and (y, x) not in rel]


# ------------------------------------------------------------- quantities ---

def p_matrix(n, rel, exts):
    """p_xy = Pr[x precedes y] for incomparable {x,y}, exact."""
    N = len(exts)
    cnt = {}
    for sigma in exts:
        pos = [0] * n
        for a, e in enumerate(sigma):
            pos[e] = a
        for (x, y) in incomparable(n, rel):
            if pos[x] < pos[y]:
                cnt[(x, y)] = cnt.get((x, y), 0) + 1
    return {pair: Fraction(cnt.get(pair, 0), N) for pair in incomparable(n, rel)}


def delta(n, rel, exts):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  None for chains."""
    P = p_matrix(n, rel, exts)
    if not P:
        return None
    return max(min(p, 1 - p) for p in P.values())


def balanced_pairs(n, rel, exts):
    """The pairs realising the 1/3-balanced condition: p_xy in [1/3, 2/3]."""
    P = p_matrix(n, rel, exts)
    lo, hi = Fraction(1, 3), Fraction(2, 3)
    return {pair: p for pair, p in P.items() if lo <= p <= hi}


def delta1(n, rel, exts, k):
    """Delta_1(A_k, A_k^c) with A_k = {0,...,k-1}, exact.  Source :270-278."""
    A = set(range(k))
    tot = 0
    for sigma in exts:
        first_k = set(sigma[:k])          # sigma(A_k)
        tot += len(A - first_k)           # |A_k \ sigma(A_k)|
    num = Fraction(tot, len(exts))
    return num / min(k, n - k)


def phi(n, rel, exts, k):
    """Phi_P(A_k) = E|A\\sigma(A)| / |A|.  Source :229-237 (needs k <= n/2)."""
    A = set(range(k))
    tot = 0
    for sigma in exts:
        tot += len(A - set(sigma[:k]))
    return Fraction(tot, len(exts)) / k


def induced(rel, S):
    """Induced subposet on S, relabelled to 0..|S|-1 preserving order."""
    S = sorted(S)
    idx = {e: i for i, e in enumerate(S)}
    sub = frozenset((idx[a], idx[b]) for (a, b) in rel if a in idx and b in idx)
    return len(S), sub, idx


def is_chain(m, sub):
    return len(sub) == m * (m - 1) // 2
