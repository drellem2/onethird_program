"""lib0fc6 — machinery for SCOPING docs/imports/compression2.tex (mg-0fc6).

WRITTEN INDEPENDENTLY of lib409a/lib8bc7/lib8d66 for the parts those also compute, so that
agreement is evidence rather than a shared bug.  The one place a prior library is imported is
`a4_operators.py`, and it is imported there ON PURPOSE as a second implementation and is
labelled as such.

Everything here is exact where exactness is available: linear extensions are enumerated,
probabilities are `fractions.Fraction`, and the only floating point is entropy (where a
logarithm is unavoidable) and the maximum-entropy solver (where the answer is irrational).
"""

from fractions import Fraction
from itertools import combinations, permutations
import math

# ---------------------------------------------------------------- posets


def tclose(n, pairs):
    """Transitive closure of `pairs` as a strict-less-than matrix."""
    lt = [[False] * n for _ in range(n)]
    for a, b in pairs:
        lt[a][b] = True
    for k in range(n):
        for i in range(n):
            if lt[i][k]:
                for j in range(n):
                    if lt[k][j]:
                        lt[i][j] = True
    return lt


def is_poset(lt):
    n = len(lt)
    for i in range(n):
        if lt[i][i]:
            return False
        for j in range(n):
            if lt[i][j] and lt[j][i]:
                return False
    return True


_POSET_CACHE = {}


def all_posets(n):
    """Every strict order on {0..n-1} as a labelled relation (not up to iso).

    Built by ADDING ELEMENT n-1 to each poset on {0..n-2}: a poset on [n] is determined by its
    restriction to [n-1] together with the new element's down-set `D` and up-set `U`, and the
    admissible `(D, U)` are exactly those with `D` a down-set of `Q`, `U` an up-set of `Q`,
    `D ∩ U = ∅`, and no `u ∈ U` below any `d ∈ D`.  That is a bijection, so the enumeration is
    exhaustive without a dedup pass — checked against OEIS A001035 in `a0`.
    """
    if n in _POSET_CACHE:
        return _POSET_CACHE[n]
    if n == 0:
        out = [[]]
    elif n == 1:
        out = [[[False]]]
    else:
        out = []
        for q in all_posets(n - 1):
            m = n - 1
            downs = []
            ups = []
            for mask in range(1 << m):
                S = [i for i in range(m) if mask >> i & 1]
                # down-set: x in S and y < x  =>  y in S
                if all((y in S) for x in S for y in range(m) if q[y][x]):
                    downs.append(S)
                # up-set: x in S and y > x  =>  y in S
                if all((y in S) for x in S for y in range(m) if q[x][y]):
                    ups.append(S)
            for D in downs:
                Dset = set(D)
                for U in ups:
                    if Dset & set(U):
                        continue
                    # d < m < u forces d < u, so every (d, u) must ALREADY be related in q.
                    # D3 KEPT: my first version tested only `not q[u][d]`, which admits
                    # INCOMPARABLE (d, u) and builds an intransitive relation — it returned
                    # 21 posets at n = 3 against the published 19, and a0.1 caught it.
                    if any(not q[d][u] for u in U for d in D):
                        continue
                    lt = [[False] * n for _ in range(n)]
                    for i in range(m):
                        for j in range(m):
                            lt[i][j] = q[i][j]
                    for d in D:
                        lt[d][m] = True
                    for u in U:
                        lt[m][u] = True
                    for d in D:
                        for u in U:
                            lt[d][u] = True
                    out.append(lt)
    _POSET_CACHE[n] = out
    return out


def chain(n):
    return tclose(n, [(i, i + 1) for i in range(n - 1)])


def antichain(n):
    return tclose(n, [])


def linear_extensions(n, lt):
    """All linear extensions, each as a tuple of elements in order (position 0 = smallest)."""
    out = []
    cur = []
    used = [False] * n

    def rec():
        if len(cur) == n:
            out.append(tuple(cur))
            return
        for x in range(n):
            if used[x]:
                continue
            if any((not used[y]) and lt[y][x] for y in range(n)):
                continue
            used[x] = True
            cur.append(x)
            rec()
            cur.pop()
            used[x] = False

    rec()
    return out


# ---------------------------------------------------------------- pair marginals


def pair_probs(LEs, n):
    """`p[(x,y)] = Pr[x before y]` under the UNIFORM measure on `LEs`, exact."""
    N = len(LEs)
    # every ORDERED pair is present, including the ones that never occur (a comparable pair
    # occurs in one direction only, and `p[(x,y)] = 0` is the value the note's (1) needs).
    cnt = {(x, y): 0 for x in range(n) for y in range(n) if x != y}
    for L in LEs:
        pos = [0] * n
        for i, x in enumerate(L):
            pos[x] = i
        for x in range(n):
            for y in range(n):
                if x != y and pos[x] < pos[y]:
                    cnt[(x, y)] = cnt.get((x, y), 0) + 1
    return {k: Fraction(v, N) for k, v in cnt.items()}


def pair_probs_measure(mu, n):
    """Same, for an arbitrary measure `mu: order -> weight` (weights sum to 1)."""
    out = {}
    for L, w in mu.items():
        pos = [0] * n
        for i, x in enumerate(L):
            pos[x] = i
        for x in range(n):
            for y in range(n):
                if x != y and pos[x] < pos[y]:
                    out[(x, y)] = out.get((x, y), 0) + w
    return out


def delta(LEs, n, lt):
    """min over INCOMPARABLE pairs of min(p, 1-p); `None` if there are none (a chain)."""
    p = pair_probs(LEs, n)
    best = None
    for x, y in combinations(range(n), 2):
        if lt[x][y] or lt[y][x]:
            continue
        v = min(p[(x, y)], 1 - p[(x, y)])
        best = v if best is None else min(best, v)
    return best


def coherent_order(LEs, n):
    """The majority ("distinguished") order `L*`, or `None` if the majority tournament cycles.

    `L*` is the note's `(v_1,...,v_n)`.  Returned as a tuple of elements in `L*`-order.
    """
    p = pair_probs(LEs, n)
    wins = [0] * n
    for x, y in combinations(range(n), 2):
        if p[(x, y)] > Fraction(1, 2):
            wins[x] += 1
        elif p[(x, y)] < Fraction(1, 2):
            wins[y] += 1
        else:
            return None  # a tie has no orientation; treat as incoherent for our purpose
    order = sorted(range(n), key=lambda x: -wins[x])
    # verify it really is the majority order (i.e. the tournament is transitive)
    for i in range(n):
        for j in range(i + 1, n):
            if p[(order[i], order[j])] <= Fraction(1, 2):
                return None
    return tuple(order)


def max_flip_against(mu_pairs, star):
    """max over i<j of Pr[v_j before v_i] — the left-hand side of the note's (1)."""
    n = len(star)
    worst = Fraction(0)
    for i in range(n):
        for j in range(i + 1, n):
            v = mu_pairs.get((star[j], star[i]), 0)
            if v > worst:
                worst = v
    return worst


# ---------------------------------------------------------------- the dyadic merge encoding


def dyadic_nodes(n):
    """Internal nodes of the balanced binary tree over positions [0,n), as (lo, mid, hi).

    The note takes `n = 2^r` "for clarity" and says balanced non-dyadic trees give the same
    asymptotic statement; this builds the balanced tree for any `n`, which is a superset.
    """
    out = []

    def rec(lo, hi):
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        out.append((lo, mid, hi))
        rec(lo, mid)
        rec(mid, hi)

    rec(0, n)
    return out


def merge_words(L, star, nodes):
    """The note's `(W_B)`: for each internal node, the A/C merge word.

    `star` is `L*`; `rank[x]` is x's index in `L*`.  A node `(lo,mid,hi)` owns the elements of
    `L*`-rank in `[lo,hi)`; `A` = ranks `[lo,mid)`, `C` = ranks `[mid,hi)`.  `W_B` records, in
    `L`-order restricted to the node, which half each successive element came from.
    """
    rank = [0] * len(star)
    for i, x in enumerate(star):
        rank[x] = i
    words = []
    for (lo, mid, hi) in nodes:
        w = []
        for x in L:
            r = rank[x]
            if lo <= r < hi:
                w.append("A" if r < mid else "C")
        words.append("".join(w))
    return tuple(words)


def decode_merge_words(words, star, nodes):
    """Inverse of `merge_words` — the losslessness claim boxed at compression2.tex:32."""
    idx = {nd: i for i, nd in enumerate(nodes)}

    def rec(lo, hi):
        if hi - lo == 1:
            return [star[lo]]
        mid = (lo + hi) // 2
        left = rec(lo, mid)
        right = rec(mid, hi)
        w = words[idx[(lo, mid, hi)]]
        out = []
        a = c = 0
        for ch in w:
            if ch == "A":
                out.append(left[a])
                a += 1
            else:
                out.append(right[c])
                c += 1
        return out

    return tuple(rec(0, len(star)))


def word_inv(w):
    """inv(W) = #{(a,c) : a is an A, c is a C, c occurs before a}."""
    seen_c = 0
    inv = 0
    for ch in w:
        if ch == "C":
            seen_c += 1
        else:
            inv += seen_c
    return inv


def word_prefix_area(w):
    """Σ_{t=1}^{|w|-1} d_t(W) with d_t = (#A's in the canonical prefix) − (#A's in W's prefix).

    This is compression2.tex (3).  The canonical word is `A^m C^m`, so the canonical prefix of
    length t holds `min(t, m)` A's.
    """
    m = w.count("A")
    a = 0
    tot = 0
    for t, ch in enumerate(w, start=1):
        if ch == "A":
            a += 1
        if t <= len(w) - 1:
            tot += min(t, m) - a
    return tot


def inv_against(L, star):
    """inv_{L*}(L) — the number of pairs whose `L`-order disagrees with `L*`."""
    rank = [0] * len(star)
    for i, x in enumerate(star):
        rank[x] = i
    r = [rank[x] for x in L]
    inv = 0
    for i in range(len(r)):
        for j in range(i + 1, len(r)):
            if r[i] > r[j]:
                inv += 1
    return inv


# ---------------------------------------------------------------- entropy


def entropy_bits(weights):
    h = 0.0
    for w in weights:
        w = float(w)
        if w > 0:
            h -= w * math.log2(w)
    return h


def h2(p):
    if p <= 0.0 or p >= 1.0:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def note_word_bound(m):
    """compression2.tex (5), first form: 2m − m³/(3 ln2 (4m²−1))."""
    return 2 * m - (m ** 3) / (3 * math.log(2) * (4 * m * m - 1))


NOTE_CONST = 1 - 1 / (24 * math.log(2))  # 0.93989...


def note_headline_bound(n):
    """compression2.tex (6): (1 − 1/(24 ln 2)) · n log2 n."""
    return NOTE_CONST * n * math.log2(n)


def log2_factorial(n):
    return math.lgamma(n + 1) / math.log(2)


# ---------------------------------------------------------------- the pair-bias information set


def max_entropy_in_Mn(n, cap=Fraction(1, 3), iters=20000, lr=0.5, tol=1e-12):
    """max { H(mu) : mu on S_n, Pr[v_j before v_i] <= cap for all i<j }, with v = identity.

    Solved in the dual.  The maximiser is the exponential family
    `mu(L) ∝ exp(−Σ_{i<j} θ_ij · 1{v_j before v_i})` with `θ ≥ 0`, and the dual objective
    `g(θ) = log Z(θ) + cap · Σ θ_ij` is convex; projected gradient with `∂g/∂θ_ij =
    cap − Pr_θ[v_j before v_i]`.  Returns `(H_bits, mu, worst_violation)`.
    """
    perms = list(permutations(range(n)))
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    # inv_flags[p][k] = 1 if in perm p, element j precedes element i for pairs[k]=(i,j)
    # `flags[k]` is the LIST OF PAIR INDICES flipped by perm k — sparse, so the inner loops
    # cost `#inversions` rather than `C(n,2)` per permutation.
    flags = []
    for L in perms:
        pos = [0] * n
        for t, x in enumerate(L):
            pos[x] = t
        flags.append([t for t, (i, j) in enumerate(pairs) if pos[j] < pos[i]])
    theta = [0.0] * len(pairs)
    capf = float(cap)
    mu = None
    exp = math.exp
    for it in range(iters):
        ws = []
        mx = -1e300
        for fk in flags:
            s = 0.0
            for t in fk:
                s -= theta[t]
            ws.append(s)
            if s > mx:
                mx = s
        tot = 0.0
        for k in range(len(ws)):
            ws[k] = exp(ws[k] - mx)
            tot += ws[k]
        mu = [w / tot for w in ws]
        grad = [capf] * len(pairs)
        for k, fk in enumerate(flags):
            mk = mu[k]
            if mk == 0.0:
                continue
            for t in fk:
                grad[t] -= mk
        step = lr / (1.0 + it / 500.0)
        moved = 0.0
        for t in range(len(pairs)):
            new = theta[t] - step * grad[t]
            if new < 0.0:
                new = 0.0
            dd = abs(new - theta[t])
            if dd > moved:
                moved = dd
            theta[t] = new
        if moved < tol:
            break
    worst = 0.0
    marg = [0.0] * len(pairs)
    for k, fk in enumerate(flags):
        for t in fk:
            marg[t] += mu[k]
    for t in range(len(pairs)):
        worst = max(worst, marg[t] - capf)
    return entropy_bits(mu), dict(zip(perms, mu)), worst


def mixture_witness(n, lam=Fraction(2, 3)):
    """`lam · Unif(S_n) + (1−lam) · δ_{L*}` with `L* = identity`.

    Every pair is flipped against `L*` with probability `lam/2`, so the measure sits in
    `M_n(0)` exactly when `lam ≤ 2/3`.  Returned as a dict order -> weight (Fractions).
    """
    perms = list(permutations(range(n)))
    N = len(perms)
    star = tuple(range(n))
    mu = {L: Fraction(lam, N) for L in perms}
    mu[star] = mu[star] + (1 - lam)
    return mu


# ---------------------------------------------------------------- BK moves


def bk_edges(L, n, lt):
    """Positions p such that swapping L[p], L[p+1] gives another linear extension."""
    out = []
    for p in range(n - 1):
        x, y = L[p], L[p + 1]
        if not lt[x][y] and not lt[y][x]:
            out.append(p)
    return out


def swap(L, p):
    Lst = list(L)
    Lst[p], Lst[p + 1] = Lst[p + 1], Lst[p]
    return tuple(Lst)


def lca_node(x, y, star, nodes):
    """The unique internal node whose two children separate `x` and `y`."""
    rank = [0] * len(star)
    for i, v in enumerate(star):
        rank[v] = i
    rx, ry = rank[x], rank[y]
    for (lo, mid, hi) in nodes:
        if lo <= rx < hi and lo <= ry < hi and ((rx < mid) != (ry < mid)):
            return (lo, mid, hi)
    return None


# ---------------------------------------------------------------- reporting


def banner(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


FAILURES = []


def verdict(ok, label, extra=""):
    tag = "GREEN" if ok else "RED  "
    print(f"  [{tag}] {label}" + (f"   {extra}" if extra else ""))
    if not ok:
        FAILURES.append(label)
    return ok


def finish():
    print()
    if FAILURES:
        print(f"RESULT: RED — {len(FAILURES)} check(s) failed:")
        for f in FAILURES:
            print(f"   - {f}")
        return 1
    print("RESULT: GREEN — all checks passed")
    return 0
