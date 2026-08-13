"""mg-7ae5 — machinery for pricing THE ABSENT STEP.

Exact `Fraction` arithmetic everywhere.  No float on any decision path; floats
appear only inside `%.4f` on report lines.

WRITTEN INDEPENDENTLY OF `code/eps0_threshold_3969/lib3969.py`, on purpose:
this instrument's whole job is to price a step by re-measuring the population
mg-3969 measured, stratified in a way it did not.  Sharing its code would make
agreement with its published numbers uninformative.  The plug-back controls in
`a0` §C therefore test THIS code against TEN numbers published by mg-3969,
mg-d3c7, Op-Form and mg-0e8c, and a transcription slip fails them.

Definitions, quoted at the source line as the corpus quotes them
(`spectral_near_ordinal_sum_program.tex`, read through the documents that read
it — this repository does not contain the .tex):

    Delta_1(A,B) = E_sigma |A \\ sigma(A)| / min(|A|,|B|)          (:270-278)
    Phi_P(A)     = E_sigma |A \\ sigma(A)| / |A|,  0 < |A| <= n/2  (:229-237)
    p_xy         = Pr_{sigma in L(P)}[x precedes y]                (:59-62)
    delta(P)     = max_{x || y} min(p_xy, 1-p_xy)                  (:63-66)

and one quantity the .tex does not have, taken from `mg-0e8c` §4:

    d(P)         = m / C(n,2),  m = # incomparable pairs   (incomparability density)

`sigma` is ONE-LINE: `sigma[a]` is the element at position `a`.  So
`sigma(A_k)` for `A_k = {0..k-1}` is the set of elements in the first k
positions, and `A_k \\ sigma(A_k)` counts prefix elements sitting after
position k.

POSET ENCODING.  A poset on [n] for which 0 < 1 < ... < n-1 is a linear
extension == a transitively closed set of pairs (i,j) with i<j.  Enumerating
those enumerates every isomorphism class with multiplicity, and the
multiplicity is exactly the number of linear extensions, i.e. the number of
DISTINGUISHED ORDERS the architecture could be handed.  That is the right
population here: Step 4 hands the argument one prefix chain, and a poset with
many linear extensions offers many.  Every count below says which of the two
it is over.
"""

from fractions import Fraction
from itertools import combinations


# ----------------------------------------------------------------- posets ---

def poset_iter(n):
    """Yield every poset on [n] admitting 0<1<...<n-1 as a linear extension,
    as a frozenset of strict relations (i,j) with i<j, transitively closed."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    m = len(pairs)
    idx = {p: b for b, p in enumerate(pairs)}
    for mask in range(1 << m):
        rel = frozenset(p for p in pairs if mask >> idx[p] & 1)
        ok = True
        for (a, b) in rel:
            for (c, dd) in rel:
                if b == c and (a, dd) not in rel:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            yield rel


def linear_extensions(n, rel):
    """Every linear extension as a tuple in ONE-LINE notation."""
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
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


def density(n, rel):
    """d(P) = m / C(n,2), the incomparability density — mg-0e8c §4."""
    return Fraction(len(incomparable(n, rel)), n * (n - 1) // 2)


# ------------------------------------------------------- pair quantities ----

def p_matrix(n, rel, exts):
    """p_xy for every incomparable {x,y}, exact."""
    inc = incomparable(n, rel)
    if not inc:
        return {}
    N = len(exts)
    cnt = {pair: 0 for pair in inc}
    for sigma in exts:
        pos = [0] * n
        for a, e in enumerate(sigma):
            pos[e] = a
        for pair in inc:
            if pos[pair[0]] < pos[pair[1]]:
                cnt[pair] += 1
    return {pair: Fraction(c, N) for pair, c in cnt.items()}


def delta(n, rel, exts):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  None for a chain."""
    P = p_matrix(n, rel, exts)
    if not P:
        return None
    return max(min(p, 1 - p) for p in P.values())


LO, HI = Fraction(1, 3), Fraction(2, 3)


def balanced_pairs(n, rel, exts):
    """Pairs with p_xy in [1/3,2/3] — L4 disjunct (i)'s object."""
    return {pair: p for pair, p in p_matrix(n, rel, exts).items()
            if LO <= p <= HI}


# -------------------------------------------------------- cut quantities ----

def delta1(n, rel, exts, k):
    """Delta_1(A_k, A_k^c), A_k = {0..k-1}.  Exact."""
    A = set(range(k))
    tot = 0
    for sigma in exts:
        tot += len(A - set(sigma[:k]))
    return Fraction(tot, len(exts)) / min(k, n - k)


def phi(n, rel, exts, k):
    """Phi_P(A_k) = E|A \\ sigma(A)| / |A| — needs k <= n/2 to be Op-Form's Phi."""
    A = set(range(k))
    tot = 0
    for sigma in exts:
        tot += len(A - set(sigma[:k]))
    return Fraction(tot, len(exts)) / k


def is_ordinal_sum_at(n, rel, k):
    """True iff P = P[A_k] (+) P[A_k^c]: every a<k is below every b>=k."""
    for a in range(k):
        for b in range(k, n):
            if (a, b) not in rel:
                return False
    return True


def induced(rel, S):
    """Induced subposet on S, relabelled 0..|S|-1 preserving order."""
    S = sorted(S)
    idx = {e: i for i, e in enumerate(S)}
    sub = frozenset((idx[a], idx[b]) for (a, b) in rel if a in idx and b in idx)
    return len(S), sub, idx


def is_chain(m, sub):
    return len(sub) == m * (m - 1) // 2


# ----------------------------------------------- the transfer surrogates ----
#
# U_either(eps): Delta_1(A,B) <= eps  ==>  a pair balanced in P[A] OR in P[B]
#                is still in [1/3,2/3] in P.
# The POPULATION matters and is the thing mg-5214/mg-d3c7 repaired:
#   BOTH   — cuts at which both sides are non-chain (mg-3969 §6's scope)
#   EITHER — cuts at which AT LEAST ONE side is non-chain (the architecturally
#            required scope; mg-d3c7 §4, where the uniform threshold is 0)

def side_report(n, rel, exts, S, pP):
    """(supplies_a_pair, some_such_pair_survives) for the induced poset on S.

    Returns (None, None) when S is a chain: a chain supplies no balanced pair,
    so the cut is outside the BOTH population.
    """
    m, sub, idx = induced(rel, S)
    if is_chain(m, sub):
        return None, None
    bal = balanced_pairs(m, sub, linear_extensions(m, sub))
    if not bal:
        return False, False
    inv = {i: e for e, i in idx.items()}
    for (a, b) in bal:
        x, y = inv[a], inv[b]
        if (x, y) in pP:
            p = pP[(x, y)]
        else:
            p = 1 - pP[(y, x)]
        if LO <= p <= HI:
            return True, True
    return True, False


def cut_verdict(n, rel, exts, k, pP=None):
    """One prefix cut, everything the sweeps need.

    dict with: k, eps (=Delta_1), sizes, scope ('BOTH'/'EITHER'/'NEITHER'),
    fails_either (U_either violated at this cut), ordsum (Delta_1 == 0 test's
    structural twin).
    """
    if pP is None:
        pP = p_matrix(n, rel, exts)
    A, B = set(range(k)), set(range(k, n))
    hasA, survA = side_report(n, rel, exts, A, pP)
    hasB, survB = side_report(n, rel, exts, B, pP)
    if hasA is None and hasB is None:
        scope = 'NEITHER'
    elif hasA is None or hasB is None:
        scope = 'EITHER'
    else:
        scope = 'BOTH'
    supplies = bool(hasA) or bool(hasB)
    survives = bool(survA) or bool(survB)
    return {
        'k': k,
        'eps': delta1(n, rel, exts, k),
        'scope': scope,
        'supplies': supplies,
        'fails_either': supplies and not survives,
        'ordsum': is_ordinal_sum_at(n, rel, k),
    }


# ------------------------------------------------------ closure arithmetic --
#
# mg-ac0c, re-derived here rather than imported, and stated with the density
# mg-0e8c's restatement puts on the supply.

def eps_sup(n, d):
    """The PROVED pair-bias supply, mg-0e8c §4: eps_sup = d * n/(n+1)."""
    return d * Fraction(n, n + 1)


def eps_dem_chain13(eps0, C3=Fraction(1)):
    """Chain (I)=(III): eps_dem = eps0^2 / (2 C3)  — mg-9461 §5.1."""
    return eps0 * eps0 / (2 * C3)


def eps0_required_cap(n, d):
    """mg-7564 §4's chain-free cap eps_dem <= 2 eps0 turned into a requirement:
    closure at density d needs eps0 >= eps_sup(n,d)/2 = d*n/(2(n+1)).

    At d = 1 this is mg-ac0c §4's n/(2(n+1)) -> 1/2, which is the d=1 reading.
    """
    return eps_sup(n, d) / 2


def eps0_required_chain13(n, d, C3=Fraction(1)):
    """Closure of chain (I)=(III) at density d needs eps0^2/(2 C3) >= eps_sup,
    i.e. eps0 >= sqrt(2 C3 d n/(n+1)).  Returned as the exact SQUARE, so no
    float enters a decision: caller compares eps0^2 against it."""
    return 2 * C3 * eps_sup(n, d)
