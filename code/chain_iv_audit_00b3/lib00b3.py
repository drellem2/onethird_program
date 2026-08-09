"""lib00b3 — the ADVERSARIAL instrument for mg-00b3, the independent audit of mg-81ff.

WHAT IS BEING AUDITED.  mg-81ff's finding is not its refutation of `c > 0.80` (that is
mg-76b2's row, extended).  Its finding is the REVERSAL: that the refuting posets are all
far outside the regime Step 2 supplies, and that stratifying the SAME population by gap
sends `min c` the other way.  This library exists to re-derive that reversal on a path
that shares nothing with `lib81ff`, and to ask the one question a self-caught correction
never gets asked: DOES THE REVERSAL SURVIVE A DIFFERENT CHOICE OF BINS?

NO SHARED CODE, and the differences are structural rather than cosmetic:

  * ENUMERATION.  `lib81ff` builds a poset on [n] by extending one on [n-1] with a
    down-closed set as the new top element's strict down-set.  This file enumerates the
    2^C(n,2) subsets of the natural order relation and KEEPS the transitively closed
    ones.  The two routes agree on a count or they do not; that agreement is a1 (P1).
  * TRANSPORT.  `lib81ff` runs two DPs, a forward `e[S]` (pull, peeling maximal elements)
    and a backward `g[S]`.  This file runs ONE routine, a PUSH DP over the down-set
    lattice, and gets the up-side by applying that same routine to the DUAL poset.  So a
    defect in the peel would have to be a defect that survives dualisation.
  * THE QUADRATIC FORM.  `lib81ff` evaluates <f_k, L f_k> as a sum over weighted edges of
    a centred vector.  Here the centred prefix indicator is observed to be piecewise
    constant with a jump of exactly `n` across the cut and NOWHERE else, so

        Q_k = <f_k,L f_k>/||f_k||^2 = n * CUT_k / (2 N k (n-k)),
        CUT_k = sum_{i<k<=j} ( Tint[i][j] + Tint[j][i] )      [INTEGERS]

    which is exact in `int` with a single `Fraction` at the end.  It is also a different
    object to check: a2 (C2) asserts it against the edge-sum form.
  * THE EIGENROUTINE.  `lib81ff` decides `lambda_2 > q` by Sylvester on the pencil
    (B^T L B) - q (B^T B) for the rational basis B = (e_i - e_{n-1}).  Here there is NO
    pencil and NO basis: since L*1 = 0 and P_H := I - J/n is the projector onto H,

        K(q) := L - q*P_H + J/n     has spectrum { 1 } u { lambda_i - q : i >= 2 },

    so `lambda_2 > q  <==>  K(q) is positive definite`, tested by exact rational LDL^T.
    One n x n matrix, no metric, no change of basis.  a0 (E) cross-checks the two
    directions against a float route and against a deliberately wrong `q`.

CONVENTIONS, all taken from Op-Form / mg-76b2 and NOT from mg-81ff's prose:

    T[x][a] = Pr[ x occupies position a ]  over uniform linear extensions   (doubly stoch.)
    M       = (T + T^T)/2                                       (symmetric, doubly stoch.)
    L       = I - M                                             (a graph Laplacian)
    gap     = lambda_2(L) = 1 - lambda_std        [so `gap` and `1 - lambda_std` are ONE
                                                   number; this file uses `gap` only]
    rho(A_k)= 1 - Q_k,     A_k = {0..k-1},   f_k = 1_{A_k} - (k/n) 1
    c(P)    = max_k rho(A_k) / lambda_std = (1 - min_k Q_k) / (1 - gap)
    C3gap(P)= min_k Q_k / gap

`c` is undefined at gap = 1 (lambda_std = 0); those posets are `INFORMATIVE = False`.
Because min_k Q_k >= lambda_2 = gap for every k (a Rayleigh quotient of a vector in H),
C3gap >= 1 and c <= 1 identically — a0 (F) asserts both rather than assuming them.
"""

from fractions import Fraction as F
from itertools import combinations, permutations

# ---------------------------------------------------------------- posets


def pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def down_from_mask(n, mask, prs):
    """down[y] = bitmask of strict predecessors of y under the chosen relation subset."""
    down = [0] * n
    for b, (i, j) in enumerate(prs):
        if mask >> b & 1:
            down[j] |= 1 << i
    return down


def is_transitive(n, down):
    """down is transitively closed: x < y  ==>  down[x] subset of down[y]."""
    for y in range(n):
        dy = down[y]
        x = dy
        while x:
            b = x & -x
            i = b.bit_length() - 1
            if down[i] & ~dy:
                return False
            x ^= b
    return True


def all_posets(n):
    """EVERY naturally labelled poset on [n], as a tuple `down` of strict down-set masks.

    Enumerated by masking the C(n,2) natural-order pairs and keeping the transitively
    closed subsets.  This is deliberately NOT mg-81ff's extension recursion: the two
    populations must agree by count and by content, and a1 (P1) asserts it.
    """
    prs = pairs(n)
    for mask in range(1 << len(prs)):
        down = down_from_mask(n, mask, prs)
        if is_transitive(n, down):
            yield tuple(down)


def relations(n, down):
    return sorted((x, y) for y in range(n) for x in range(n) if down[y] >> x & 1)


def dual(n, down):
    """The order-dual, relabelled x -> n-1-x so it is again naturally labelled."""
    up = [0] * n
    for y in range(n):
        d = down[y]
        while d:
            b = d & -d
            x = b.bit_length() - 1
            up[x] |= 1 << y
            d ^= b
    return tuple(reverse_mask(n, up[n - 1 - y]) for y in range(n))


def reverse_mask(n, m):
    r = 0
    for i in range(n):
        if m >> i & 1:
            r |= 1 << (n - 1 - i)
    return r


def cut_points(n, down):
    """k in 1..n-1 with {0..k-1} an ordinal-sum split (every y>=k above every x<k)."""
    lo_all = [(1 << k) - 1 for k in range(n + 1)]
    out = []
    for k in range(1, n):
        lo = lo_all[k]
        if all(down[y] & lo == lo for y in range(k, n)):
            out.append(k)
    return out


def is_primitive(n, down):
    return not cut_points(n, down)


# ---------------------------------------------------------- linear extensions


def downsets_scan(n, down):
    """All down-closed masks by scanning all 2^n subsets.  O(2^n); exact and obviously
    right, which is why it is the one the exhaustive sweep uses and the one a0 (A)
    cross-checks the lattice walk against."""
    out = []
    for S in range(1 << n):
        ok = True
        x = S
        while x:
            b = x & -x
            i = b.bit_length() - 1
            if down[i] & ~S:
                ok = False
                break
            x ^= b
        if ok:
            out.append(S)
    out.sort(key=lambda S: S.bit_count())
    return out


def downsets_walk(n, down):
    """All down-closed masks by BFS over the down-set LATTICE, never touching a subset
    that is not one.  O(#down-sets * n), which is what makes the named families reachable
    at n = 20-24 where 2^n is not.  a0 (A) asserts it equals `downsets_scan` at every
    poset n <= 6 and at every family member where both are affordable."""
    seen = {0}
    frontier = [0]
    out = [0]
    while frontier:
        nxt = []
        for S in frontier:
            for i in range(n):
                if S >> i & 1:
                    continue
                if down[i] & ~S:
                    continue
                U = S | (1 << i)
                if U not in seen:
                    seen.add(U)
                    nxt.append(U)
                    out.append(U)
        frontier = nxt
    out.sort(key=lambda S: S.bit_count())
    return out


def downsets(n, down):
    """The scan below n = 18, the lattice walk above it."""
    return downsets_scan(n, down) if n < 18 else downsets_walk(n, down)


def ext_counts(n, down, ds=None):
    """e[S] = # linear extensions of the induced order on the down-set S, by a PUSH DP.

    Increasing popcount; from each down-set S push into S|{i} for every i not in S whose
    strict down-set is already inside S.  (mg-81ff's DP PULLS, peeling maximal elements,
    and needs `S\\{i} still down-closed` to do it; the push form needs `down[i] <= S`,
    which is the same condition read forwards.  The two must agree — a0 (B).)
    """
    if ds is None:
        ds = downsets(n, down)
    e = dict.fromkeys(ds, 0)
    e[0] = 1
    for S in ds:
        v = e[S]
        if not v:
            continue
        for i in range(n):
            if S >> i & 1:
                continue
            if down[i] & ~S:
                continue
            e[S | (1 << i)] += v
    return e


def transport_int(n, down):
    """(Tint, N):  Tint[x][a] = # linear extensions placing x at position a;  N = e(P).

    The up-side counts come from `ext_counts` applied to the DUAL poset, not from a
    second, separately written backward DP.
    """
    ds = downsets(n, down)
    e = ext_counts(n, down, ds)
    dn = dual(n, down)
    edual = ext_counts(n, dn)
    full = (1 << n) - 1
    # g[S] = # extensions of the induced order on the complement of S.
    #   complement of a down-set of P is an up-set of P, i.e. maps to a down-set of the
    #   dual under the relabel x -> n-1-x.
    T = [[0] * n for _ in range(n)]
    for S in ds:
        a = S.bit_count()
        eS = e[S]
        if not eS:
            continue
        for i in range(n):
            if S >> i & 1:
                continue
            if down[i] & ~S:
                continue
            comp = full ^ (S | (1 << i))
            T[i][a] += eS * edual[reverse_mask(n, comp)]
    return T, e[full]


def transport_factorial(n, down):
    """Tint by brute force over n! permutations.  CONTROL ONLY."""
    rel = relations(n, down)
    T = [[0] * n for _ in range(n)]
    N = 0
    for p in permutations(range(n)):
        pos = [0] * n
        for a, x in enumerate(p):
            pos[x] = a
        if all(pos[x] < pos[y] for (x, y) in rel):
            N += 1
            for a, x in enumerate(p):
                T[x][a] += 1
    return T, N


# ------------------------------------------------------------- the constants


def prefix_Q_all(n, Tint, N):
    """[Q_1..Q_{n-1}] exactly.  Q_k = n*CUT_k / (2 N k (n-k)) with CUT_k an integer.

    Derivation, in one line, because this is the step that replaces an edge sum:
    f_k is (n-k)/n on {0..k-1} and -k/n above, so (f_i - f_j)^2 is 1 across the cut and
    0 elsewhere; <f_k,Lf_k> = sum_{i<k<=j} M_ij and ||f_k||^2 = k(n-k)/n.
    """
    A = [[Tint[i][j] + Tint[j][i] for j in range(n)] for i in range(n)]
    out = []
    for k in range(1, n):
        cut = 0
        for i in range(k):
            row = A[i]
            for j in range(k, n):
                cut += row[j]
        out.append(F(n * cut, 2 * N * k * (n - k)))
    return out


def energy_edgesum(n, Tint, N, f):
    """<f, L f> = sum_{i<j} M_ij (f_i - f_j)^2 — the form lib81ff uses.  CONTROL ONLY."""
    tot = F(0)
    for i in range(n):
        for j in range(i + 1, n):
            a = F(Tint[i][j] + Tint[j][i], 2 * N)
            if a:
                d = f[i] - f[j]
                tot += a * d * d
    return tot


def L_fractions(n, Tint, N):
    return [[(F(1) if i == j else F(0)) - F(Tint[i][j] + Tint[j][i], 2 * N)
             for j in range(n)] for i in range(n)]


def L_floats(n, Tint, N):
    inv = 1.0 / (2.0 * N)
    return [[(1.0 if i == j else 0.0) - (Tint[i][j] + Tint[j][i]) * inv
             for j in range(n)] for i in range(n)]


# ---------------------------------------------------------------- lambda_2

def _pd_exact(n, K):
    """Is the exact symmetric rational matrix K positive definite?  LDL^T, no pivoting:
    K is PD iff every pivot of the elimination is > 0 (and then no pivot can vanish)."""
    A = [row[:] for row in K]
    for p in range(n):
        piv = A[p][p]
        if piv <= 0:
            return False
        for i in range(p + 1, n):
            f = A[i][p] / piv
            if f:
                Ai, Ap = A[i], A[p]
                for j in range(p, n):
                    Ai[j] -= f * Ap[j]
    return True


def _pd_float(n, K):
    A = [row[:] for row in K]
    for p in range(n):
        piv = A[p][p]
        if piv <= 0.0:
            return False
        for i in range(p + 1, n):
            f = A[i][p] / piv
            if f:
                Ai, Ap = A[i], A[p]
                for j in range(p, n):
                    Ai[j] -= f * Ap[j]
    return True


def lambda2_gt_exact(n, L, q):
    """lambda_2(L) > q, EXACTLY.  K(q) = L - q*(I - J/n) + J/n is PD iff it is.

    Spectrum of K(q): 1 on span(1) (since L*1 = 0, P_H*1 = 0, (J/n)*1 = 1) and
    lambda_i - q on H.  So PD <=> every nonzero eigenvalue of L exceeds q.  There is no
    pencil and no change of basis here; that is the whole point of writing it this way.
    """
    q = F(q)
    inv_n = F(1, n)
    K = [[L[i][j] - q * ((F(1) if i == j else F(0)) - inv_n) + inv_n
          for j in range(n)] for i in range(n)]
    return _pd_exact(n, K)


def lambda2_gt_float(n, Lf, q):
    inv_n = 1.0 / n
    K = [[Lf[i][j] - q * ((1.0 if i == j else 0.0) - inv_n) + inv_n
          for j in range(n)] for i in range(n)]
    return _pd_float(n, K)


def lambda2_float(n, Lf, iters=52):
    """lambda_2(L) as a float, by bisection on the PD test.  0 <= lambda_2 <= 1 always
    (L = I - M with M doubly stochastic symmetric, so spec(L) is in [0,2]; and
    lambda_2 <= 1 here because R(f) <= 1 for the centred prefix indicator... which is not
    assumed: the upper end of the bracket is grown until the test fails)."""
    hi = 1.0
    while lambda2_gt_float(n, Lf, hi):
        hi *= 2.0
        if hi > 4.0:
            break
    lo = 0.0
    for _ in range(iters):
        mid = (lo + hi) / 2.0
        if mid <= lo or mid >= hi:
            break
        if lambda2_gt_float(n, Lf, mid):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def lambda2_bracket(n, L, prec=F(1, 10 ** 9), hi=None):
    """An EXACT rational bracket (lo, hi] with lo < lambda_2(L) <= hi, hi - lo <= prec."""
    if hi is None:
        hi = F(1)
        while lambda2_gt_exact(n, L, hi):
            hi *= 2
    lo = F(0)
    while hi - lo > prec:
        mid = (lo + hi) / 2
        if lambda2_gt_exact(n, L, mid):
            lo = mid
        else:
            hi = mid
    return lo, hi


# ------------------------------------------------------------ poset summary


class Report:
    __slots__ = ("n", "down", "N", "T", "Q", "minQ", "argmin", "gap", "informative")

    def __repr__(self):
        return f"Report(n={self.n}, rel={relations(self.n, self.down)})"

    def c(self):
        """c = (1 - min_k Q_k)/(1 - gap), as a float.  Undefined at gap = 1."""
        return (1.0 - float(self.minQ)) / (1.0 - self.gap)

    def C3gap(self):
        return float(self.minQ) / self.gap

    def c_bracket(self, prec=F(1, 10 ** 12)):
        """An exact rational bracket on c.  Lower end refutes an upper threshold."""
        L = L_fractions(self.n, self.T, self.N)
        lo, hi = lambda2_bracket(self.n, L, prec)
        num = 1 - self.minQ
        # c = num/(1-gap), gap in (lo, hi]  =>  c in [num/(1-lo), num/(1-hi))  reversed:
        # 1-gap in [1-hi, 1-lo), so c = num/(1-gap) in (num/(1-lo), num/(1-hi)]
        return num / (1 - lo), num / (1 - hi)


def analyse(n, down, want_gap=True):
    r = Report()
    r.n, r.down = n, tuple(down)
    T, N = transport_int(n, down)
    r.T, r.N = T, N
    Q = prefix_Q_all(n, T, N)
    r.Q = Q
    m = min(Q)
    r.minQ = m
    r.argmin = Q.index(m) + 1
    if want_gap:
        r.gap = lambda2_float(n, L_floats(n, T, N))
        r.informative = r.gap < 1.0 - 1e-12
    else:
        r.gap = None
        r.informative = None
    return r


# ------------------------------------------------------------ named families


def D_k(k):
    """k disjoint 2-chains on {0..2k-1}: 2i < 2i+1.  mg-81ff's minimiser family."""
    n = 2 * k
    down = [0] * n
    for i in range(k):
        down[2 * i + 1] = 1 << (2 * i)
    return n, tuple(down)


def S_n(n):
    """THE STAIRCASE:  i < j  iff  j >= i + 2.   down[y] = {0 .. y-2}.

    NOT constructed to fit anything: it is what the EXHAUSTIVE sweep returns when asked
    for the poset maximising C3gap = min_k Q_k / gap, at n = 5, 6 and 7 alike.  a3 exhibits
    that derivation before using the family, because a family that arrives by construction
    and a family that arrives by search are different kinds of evidence.
    """
    return n, tuple((1 << max(0, y - 1)) - 1 for y in range(n))


def N_family(n, drop="mid"):
    """antichain {0..a-1} < antichain {a..n-1}, a = n//2, minus ONE relation.

    drop='mid'  removes (a-1, a)      -- mg-81ff's N(n)
    drop='ends' removes (0, n-1)      -- mg-81ff's N'(n)
    """
    a = n // 2
    down = [0] * n
    for y in range(a, n):
        down[y] = (1 << a) - 1
    if drop == "mid":
        down[a] &= ~(1 << (a - 1))
    elif drop == "ends":
        down[n - 1] &= ~(1 << 0)
    else:
        raise ValueError(drop)
    return n, tuple(down)
