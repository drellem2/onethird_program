"""libf5be -- mg-f5be's instrument for DANIEL'S PRIMITIVITY OBJECTION.

THE QUESTION.  mg-409a proved alpha(P) <= 1 at every poset and exhibited attainment at Z_n,
the ordinal sum of 2-element antichains.  Z_n is DECOMPOSABLE; counterexamples to
(1/3)-(2/3) are PRIMITIVE.  Does the ceiling survive restriction to the primitive class,
and is pm-onethird right that it gets TIGHTER there?

INDEPENDENCE, STATED FIRST BECAUSE IT IS THE THING A READER MUST PRICE.
Posets, linear extensions, the two compressions, the fibers, Pi_o / Pi_e, M, and the BK
Dirichlet form are all IMPORTED from `lib409a` -- deliberately.  This ticket's job is to
audit a claim ABOUT mg-409a's object, so re-implementing that object would make a
disagreement uninterpretable (is it the claim or is it my constructions?).  What is new
here and built from scratch is:

  * enumeration of posets UP TO ISOMORPHISM by augmentation, with the count sequence
    1, 2, 5, 16, 63, 318 as a positive control (p0.1);
  * modular decomposition / primitivity, ordinal decomposition, connectivity;
  * the pair statistics p_xy and P(adjacent), and pm-onethird's chain;
  * an EXACT test for `alpha == 1` that needs no eigenvalue at all;
  * a float power iteration for alpha, cross-checked against lib409a's Jacobi (p0.4).

EXACTNESS.  Fractions on every verdict path.  Two floats exist -- `alpha_power` here and
`lib409a.jacobi_eigenvalues` -- and both are MEASUREMENT.  Every PASS in this directory is
an exact rational comparison, an exhibited rational witness, or a combinatorial count.
"""

import os
import sys
from fractions import Fraction
from itertools import combinations, permutations

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "compression_rate_409a"))
import lib409a as L  # noqa: E402


# --------------------------------------------------------------------------------------
# enumeration of posets UP TO ISOMORPHISM, by augmentation with a maximal element
# --------------------------------------------------------------------------------------


def canonical(n, lt):
    """Lexicographically least relabelling.  Brute force over n! -- honest to n = 6."""
    best = None
    for perm in permutations(range(n)):
        img = tuple(sorted((perm[a], perm[b]) for (a, b) in lt))
        if best is None or img < best:
            best = img
    return best


def down_sets(n, lt):
    """Every down-closed subset of P (including empty and full)."""
    preds = [set() for _ in range(n)]
    for (i, j) in lt:
        preds[j].add(i)
    out = []
    for mask in range(1 << n):
        S = {v for v in range(n) if mask >> v & 1}
        if all(preds[v] <= S for v in S):
            out.append(S)
    return out


def posets_up_to_iso(n, cache={}):
    """All iso classes of posets on n elements, as frozensets of strict relations on 0..n-1.

    EVERY poset has a maximal element; deleting it leaves a poset on n-1 elements.  So
    augmenting each (n-1)-class by a new top element sitting above each down-set of it
    generates every n-class at least once.  Dedup by `canonical`.
    """
    if n in cache:
        return cache[n]
    if n == 0:
        cache[0] = [frozenset()]
        return cache[0]
    smaller = posets_up_to_iso(n - 1)
    seen, out = set(), []
    for lt in smaller:
        for S in down_sets(n - 1, lt):
            rel = set(lt) | {(v, n - 1) for v in S}
            key = canonical(n, rel)
            if key in seen:
                continue
            seen.add(key)
            out.append(frozenset(rel))
    cache[n] = out
    return out


# --------------------------------------------------------------------------------------
# structure: modules (primitivity), ordinal decomposition, connectivity
# --------------------------------------------------------------------------------------


def relation_kind(lt, x, m):
    if (x, m) in lt:
        return -1          # x below m
    if (m, x) in lt:
        return +1          # x above m
    return 0               # incomparable


def is_module(n, lt, M):
    """M is a module (autonomous set): every x outside M relates identically to all of M."""
    for x in range(n):
        if x in M:
            continue
        kinds = {relation_kind(lt, x, m) for m in M}
        if len(kinds) > 1:
            return False
    return True


def modules(n, lt, nontrivial_only=True):
    out = []
    for size in range(1, n + 1):
        for M in combinations(range(n), size):
            if nontrivial_only and (size == 1 or size == n):
                continue
            if is_module(n, lt, set(M)):
                out.append(frozenset(M))
    return out


def is_prime(n, lt):
    """PRIMITIVE in the modular-decomposition sense: no module of size 2..n-1.

    Note the convention: n <= 2 is VACUOUSLY prime -- there is no size in the range at all,
    so the quantifier is empty.  That degeneracy is not a curiosity here: it is the ONLY
    way `alpha = 1` survives into the prime class (p2.2), and the poset it lets in is the
    2-element antichain, which is exactly the BLOCK Z_n is the ordinal sum OF.  Use
    `is_primitive_proper` for the class Daniel's objection is about.
    """
    return not modules(n, lt, nontrivial_only=True)


def is_primitive_proper(n, lt):
    """PRIME and n >= 4 -- the class in which primitivity is a real hypothesis.

    There is no prime poset on exactly 3 elements (p0.3 checks this rather than assuming
    it), and n <= 2 is prime only because the definition's range is empty there.  So
    `n >= 4` excludes exactly the degenerate cases and nothing else.
    """
    return n >= 4 and is_prime(n, lt)


def ordinal_split(n, lt):
    """A proper nonempty down-set D with D entirely below P\\D: P = P|D (+) P|(P-D).

    Returns such a D or None.  This is the ORDINAL-SUM decomposition -- strictly weaker
    than modular decomposability, and the one Z_n exhibits.
    """
    for D in down_sets(n, lt):
        if not D or len(D) == n:
            continue
        rest = set(range(n)) - D
        if all((d, r) in lt for d in D for r in rest):
            return frozenset(D)
    return None


def is_connected(n, lt):
    """Connectivity of the comparability graph."""
    if n == 0:
        return True
    adj = {v: set() for v in range(n)}
    for (a, b) in lt:
        adj[a].add(b)
        adj[b].add(a)
    seen, stack = {0}, [0]
    while stack:
        v = stack.pop()
        for w in adj[v] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == n


def classify(n, lt):
    """The three structure flags, computed once per poset."""
    return {
        "prime": is_prime(n, lt),
        "ordinal_indecomposable": ordinal_split(n, lt) is None,
        "connected": is_connected(n, lt),
    }


# --------------------------------------------------------------------------------------
# pair statistics: p_xy, P(adjacent), delta, mu
# --------------------------------------------------------------------------------------


def pair_stats(n, lt, LEs, x, y):
    """Exact (p, P_adj) for the incomparable pair {x,y}.

    p     = P(x before y)             -- the (1/3)-(2/3) quantity
    P_adj = P(x and y occupy adjacent positions), either order
    """
    N = len(LEs)
    before = 0
    adj = 0
    for Lx in LEs:
        i = Lx.index(x)
        j = Lx.index(y)
        if i < j:
            before += 1
        if abs(i - j) == 1:
            adj += 1
    return Fraction(before, N), Fraction(adj, N)


def all_pair_stats(n, lt, LEs):
    return {(x, y): pair_stats(n, lt, LEs, x, y) for (x, y) in L.incomparable(n, lt)}


def delta_of(stats):
    """delta(P) = max over incomparable pairs of min(p, 1-p).  The BEST-balanced pair.

    (1/3)-(2/3) says delta >= 1/3.  A counterexample ('frozen') has delta < 1/3.
    Raises on a poset with no incomparable pair -- a chain has no delta, and returning a
    number there is E6.
    """
    if not stats:
        raise ValueError("no incomparable pair: delta is a max over the empty set")
    return max(min(p, 1 - p) for (p, _a) in stats.values())


def mu_of(stats):
    """mu(P) = min over incomparable pairs of min(p, 1-p).  The WORST-balanced pair.

    This is the one pm-onethird's chain gets to choose, because L2 holds at EVERY pair.
    mu <= delta always; frozen (delta < 1/3) therefore forces mu < 1/3 too.
    """
    if not stats:
        raise ValueError("no incomparable pair: mu is a min over the empty set")
    return min(min(p, 1 - p) for (p, _a) in stats.values())


def is_frozen(stats):
    """delta(P) < 1/3: every incomparable pair outside [1/3, 2/3].  THE COUNTEREXAMPLE CLASS."""
    return delta_of(stats) < Fraction(1, 3)


# --------------------------------------------------------------------------------------
# pm-onethird's chain, link by link
# --------------------------------------------------------------------------------------


def chain_term1(p, p_adj):
    """P(adjacent) / (4 p (1-p)) -- pm-onethird's first term.  EXACT."""
    return p_adj / (4 * p * (1 - p))


def chain_term2(p):
    """1 / (2 max(p, 1-p)) -- pm-onethird's second term.  EXACT."""
    return 1 / (2 * max(p, 1 - p))


def chain_bound(stats):
    """min over incomparable pairs of the tightest term available.  EXACT.

    Returns (best_term1, best_term2) -- both valid upper bounds on alpha(P) if the chain
    holds, the first being the tighter.
    """
    t1 = min(chain_term1(p, a) for (p, a) in stats.values())
    t2 = min(chain_term2(p) for (p, _a) in stats.values())
    return t1, t2


# --------------------------------------------------------------------------------------
# alpha: an EXACT `== 1` test, and a float measurement
# --------------------------------------------------------------------------------------


def fiber_partitions(LEs, n):
    """(odd fibers, even fibers) as lists of index lists."""
    fo = list(L.fiber_map(LEs, L.blocks_o(n)).values())
    fe = list(L.fiber_map(LEs, L.blocks_e(n)).values())
    return fo, fe


def alpha_is_one_exact(LEs, n):
    """EXACT: alpha(P) == 1 iff Ran Q_o _|_ Ran Q_e, where Q = Pi - P_1.

    Two-projection theory (mg-409a section 5): alpha = 1 - cos(theta_min) between Ran Q_o
    and Ran Q_e, so alpha = 1 exactly when the two ranges are orthogonal, i.e. Q_o Q_e = 0.
    Ran Q_e is spanned by v_F = 1_F/|F| - 1/N over even fibers F, and each v_F is already
    perpendicular to 1, so Q_o v_F = Pi_o v_F.  Hence the test is:

            Pi_o v_F = 0   for every even fiber F.

    O(N * #fibers) exact rational work and NO eigenvalue.  Returns (bool, witness) where
    the witness on a False is (fiber, odd-fiber, nonzero average) -- an exhibited reason.
    """
    N = len(LEs)
    fo, fe = fiber_partitions(LEs, n)
    for F in fe:
        # v_F on index k is 1/|F| - 1/N if k in F else -1/N
        inF = set(F)
        c_in = Fraction(1, len(F)) - Fraction(1, N)
        c_out = -Fraction(1, N)
        for G in fo:
            s = sum(c_in if k in inF else c_out for k in G)
            if s != 0:
                return False, (tuple(sorted(inF)), tuple(sorted(G)), s / len(G))
    return True, None


def alpha_power(LEs, n, iters=4000, tol=1e-15):
    """alpha = 2 - lambda_max( (Pi_o + Pi_e) restricted to 1-perp ).  FLOAT.  MEASUREMENT.

    Power iteration on A = Pi_o + Pi_e, which is PSD with eigenvalues in [0,2] and top
    eigenvalue 2 carried by the constants; deflating the constants leaves lambda_2.
    O(N) per iteration versus Jacobi's O(N^3) per sweep, which is what makes n = 6
    exhaustive reachable at all.  Cross-checked against lib409a.alpha_measured in p0.4.
    """
    N = len(LEs)
    if N < 2:
        return None
    fo, fe = fiber_partitions(LEs, n)

    def apply_A(v):
        out = [0.0] * N
        for part in (fo, fe):
            for G in part:
                m = sum(v[k] for k in G) / len(G)
                for k in G:
                    out[k] += m
        return out

    def deflate(v):
        m = sum(v) / N
        return [x - m for x in v]

    import math
    v = deflate([math.sin(1.0 + 2.7 * k) for k in range(N)])
    nrm = math.sqrt(sum(x * x for x in v))
    if nrm == 0.0:
        v = deflate([1.0] + [0.0] * (N - 1))
        nrm = math.sqrt(sum(x * x for x in v))
    v = [x / nrm for x in v]
    lam = 0.0
    for _ in range(iters):
        w = deflate(apply_A(v))
        nw = math.sqrt(sum(x * x for x in w))
        if nw < 1e-300:
            return 2.0
        w = [x / nw for x in w]
        new = sum(a * b for a, b in zip(w, deflate(apply_A(w))))
        if abs(new - lam) < tol:
            lam = new
            v = w
            break
        lam, v = new, w
    return 2.0 - lam


def alpha_exact_upper(LEs, n, stats):
    """An EXACT rational upper bound on alpha, from exhibited test vectors only.

    Two families, both Rayleigh quotients at a named f, so both are valid without any
    eigenvalue computation:
      * the pair indicators f_xy, one per incomparable pair (mg-409a L2);
      * the odd-fiber indicators 1_G - |G|/N (mg-409a section 3, Case 1).
    Returns (bound, which).
    """
    best, which = None, None
    for (x, y) in stats:
        f = L.pair_indicator(n, None, LEs, x, y)
        r = L.rayleigh_M(f, LEs, n)
        if r is not None and (best is None or r < best):
            best, which = r, ("pair", x, y)
    N = len(LEs)
    fo, _fe = fiber_partitions(LEs, n)
    for G in fo:
        if len(G) == N:
            continue
        inG = set(G)
        f = [Fraction(1) if k in inG else Fraction(0) for k in range(N)]
        r = L.rayleigh_M(f, LEs, n)
        if r is not None and (best is None or r < best):
            best, which = r, ("oddfiber", tuple(sorted(inG)))
    return best, which


# --------------------------------------------------------------------------------------
# reporting
# --------------------------------------------------------------------------------------

banner = L.banner
verdict = L.verdict
frac = L.frac
