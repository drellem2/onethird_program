"""mg-9461 — poset primitives, written from scratch for this ticket.

Deliberately shares no line with `code/eps0_audit_d3c7/lib_d3c7.py` or
`code/eps0_threshold_3969/lib3969.py`: the one fact this ticket leans on from
`mg-d3c7` (that the uniform surrogate's threshold is `0` in the architecturally
required scope) is re-verified here on an independent path, because it is
load-bearing for the `ε_leak` half of the deliverable.

Everything on a decision path is `Fraction`. No float anywhere in this file.
"""

from fractions import Fraction
from itertools import permutations, combinations


class Poset:
    """Strict partial order on `range(n)`, stored as a transitively closed
    relation `lt` (a frozenset of `(x, y)` meaning `x < y`)."""

    def __init__(self, n, covers):
        self.n = n
        # transitive closure by reachability DFS from each node — O(n·(n+|E|)).
        # (The Floyd-Warshall-shaped loop this replaces was quadratically too
        # slow at the n ≈ 40 members of mg-d3c7's family.)
        succ = [[] for _ in range(n)]
        for a, b in covers:
            succ[a].append(b)
        lt = set()
        for a in range(n):
            stack, seen = list(succ[a]), set()
            while stack:
                b = stack.pop()
                if b in seen:
                    continue
                seen.add(b)
                lt.add((a, b))
                stack.extend(succ[b])
        for x in range(n):
            assert (x, x) not in lt, "not a strict order"
        self.lt = frozenset(lt)

    def comparable(self, x, y):
        return (x, y) in self.lt or (y, x) in self.lt

    def incomparable_pairs(self):
        return [(x, y) for x, y in combinations(range(self.n), 2)
                if not self.comparable(x, y)]

    def linear_extensions(self):
        """All linear extensions, by filtering permutations. O(n!) — honest and
        slow, which is the point: this is the independent path."""
        out = []
        for p in permutations(range(self.n)):
            pos = {v: i for i, v in enumerate(p)}
            if all(pos[a] < pos[b] for a, b in self.lt):
                out.append(p)
        return out

    def is_chain(self):
        return len(self.incomparable_pairs()) == 0

    def induced(self, S):
        """`P[S]`, relabelled to `range(|S|)` in increasing order of the
        original label. Returns `(poset, relabel_map)`."""
        S = sorted(S)
        idx = {v: i for i, v in enumerate(S)}
        covers = [(idx[a], idx[b]) for a, b in self.lt if a in idx and b in idx]
        return Poset(len(S), covers), idx


def count_extensions(P):
    """`e(P)` by a down-set DP — the SECOND path, used where `n!` is out of
    reach. `dp[S]` = number of linear orders of the down-set `S`."""
    n = P.n
    above = _above_lists(P)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(S):
        if not S:
            return 1
        # peel a MAXIMAL element: `S - {x}` must still be a down-set. The first
        # version of this tested `below[x] <= S - {x}`, which is true of every
        # minimal element too — the answers came out right (dead branches
        # return 0) but the state space was all 2^n subsets instead of the
        # down-set lattice, and it could not reach n = 17.
        return sum(dp(S - {x}) for x in S if not (above[x] & S))

    return dp(frozenset(range(n)))


def pair_probabilities_dp(P):
    """`p[(x, y)] = Pr[x before y]` via `e(P ∪ {x<y}) / e(P)` — no permutation
    enumeration. Agrees with `pair_probabilities` wherever both are runnable."""
    e = count_extensions(P)
    out = {}
    for x, y in P.incomparable_pairs():
        Q = Poset(P.n, list(P.lt) + [(x, y)])
        out[(x, y)] = Fraction(count_extensions(Q), e)
    return out


def _below_lists(P):
    below = [set() for _ in range(P.n)]
    for a, b in P.lt:
        below[b].add(a)
    return [frozenset(b) for b in below]


def _above_lists(P):
    above = [set() for _ in range(P.n)]
    for a, b in P.lt:
        above[a].add(b)
    return [frozenset(a) for a in above]


def head_leak_dp(P, A):
    """`E|A ∖ σ(A)|`, exactly, by summing over the possible HEADS.

    `σ`'s first `k = |A|` positions always form a down-set `S` of size `k`, and
    `Pr[head = S] = e(P[S]) · e(P ∖ S) / e(P)`. So
    `E|A ∖ σ(A)| = Σ_S Pr[head = S] · |A ∖ S|`, a sum over the size-`k` level of
    the down-set lattice — not over `C(n, k)` subsets, which is what the first
    version of this function did and why it could not reach `n = 41`.
    """
    n, k = P.n, len(A)
    A = frozenset(A)
    e = count_extensions(P)
    below = _below_lists(P)
    above = _above_lists(P)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(S):
        if not S:
            return 1
        return sum(dp(S - {x}) for x in S if not (above[x] & S))

    total = Fraction(0)
    checked = Fraction(0)
    for S in all_down_sets(P, below):
        if len(S) != k:
            continue
        rest, _ = P.induced(frozenset(range(n)) - S)
        w = Fraction(dp(S) * count_extensions(rest), e)
        checked += w
        total += w * len(A - S)
    assert checked == 1, f"head distribution must sum to 1, got {checked}"
    return total


def is_down_set(P, A):
    """`A` is a down-set: nothing below a member is outside it."""
    A = set(A)
    return all(a in A for a, b in P.lt if b in A)


def all_down_sets(P, below=None):
    """Every down-set of `P`, by BFS up the down-set lattice.

    Enumerating `C(n, k)` subsets and filtering (as `down_sets` does at the
    `n ≤ 7` sizes where it is affordable) is hopeless at `n = 41`; the lattice
    itself is small for the posets this file cares about."""
    below = below if below is not None else _below_lists(P)
    frontier = {frozenset()}
    seen = {frozenset()}
    while frontier:
        nxt = set()
        for S in frontier:
            for x in range(P.n):
                if x in S or not (below[x] <= S):
                    continue
                T = S | {x}
                if T not in seen:
                    seen.add(T)
                    nxt.add(T)
        frontier = nxt
    return seen


def down_sets_of_size(P, k):
    for S in all_down_sets(P):
        if len(S) == k:
            yield S


def delta_1_dp(P, A):
    """`Δ₁(A, Aᶜ)` on the DP path."""
    return head_leak_dp(P, set(A)) / min(len(A), P.n - len(A))


def pair_probabilities(P, exts=None):
    """`p[(x, y)] = Pr[x before y]` over the uniform linear extension, for every
    incomparable pair `x < y` (as labels)."""
    exts = exts if exts is not None else P.linear_extensions()
    e = len(exts)
    assert e > 0
    out = {}
    for x, y in P.incomparable_pairs():
        c = sum(1 for p in exts if p.index(x) < p.index(y))
        out[(x, y)] = Fraction(c, e)
    return out


def delta(P, exts=None):
    """`δ(P)` — the balance constant: max over incomparable pairs of
    `min(p, 1−p)`. `< 1/3` is frozen. Returns `0` if `P` is a chain."""
    pr = pair_probabilities(P, exts)
    if not pr:
        return Fraction(0)
    return max(min(p, 1 - p) for p in pr.values())


def delta_1(P, A, exts=None):
    """`Δ₁(A, Aᶜ) = E|A ∖ σ(A)| / min(|A|, |Aᶜ|)`, where `σ(A)` is the set of
    elements occupying the first `|A|` positions of `σ`."""
    exts = exts if exts is not None else P.linear_extensions()
    A = set(A)
    k, n = len(A), P.n
    assert 0 < k < n
    total = 0
    for p in exts:
        head = set(p[:k])
        total += len(A - head)
    return Fraction(total, len(exts) * min(k, n - k))


def down_sets(P):
    """All proper non-empty down-sets of `P` — i.e. all legitimate prefix cuts."""
    out = []
    for r in range(1, P.n):
        for A in combinations(range(P.n), r):
            S = set(A)
            if all(not (a in S and (b, a) in P.lt and b not in S)
                   for a in S for b in range(P.n)):
                out.append(frozenset(A))
    return out


BAL_LO, BAL_HI = Fraction(1, 3), Fraction(2, 3)


def balanced(p):
    return BAL_LO <= p <= BAL_HI


def transfer_survives(P, A, side_labels, exts=None):
    """The `F`-free repaired transfer, on ONE named side.

    *Does some pair that is balanced inside `P[side]` remain balanced in `P`?*
    This is `mg-3969`'s (i)-free surrogate, restricted to the given side.
    Returns `(survives, n_balanced_in_side, witness_or_None)`.
    """
    exts = exts if exts is not None else P.linear_extensions()
    pr_full = pair_probabilities(P, exts)
    S = sorted(side_labels)
    if len(S) < 2:
        return False, 0, None
    Q, idx = P.induced(S)
    inv = {i: v for v, i in idx.items()}
    pr_side = pair_probabilities(Q)
    nbal = 0
    for (i, j), p_side in pr_side.items():
        if not balanced(p_side):
            continue
        nbal += 1
        x, y = inv[i], inv[j]
        key = (x, y) if (x, y) in pr_full else (y, x)
        if key not in pr_full:
            continue  # became comparable in P — cannot survive as a pair
        p_full = pr_full[key] if key == (x, y) else 1 - pr_full[key]
        if balanced(p_full):
            return True, nbal, ((x, y), p_side, p_full)
    return False, nbal, None


def delta_dp(P):
    pr = pair_probabilities_dp(P)
    if not pr:
        return Fraction(0)
    return max(min(p, 1 - p) for p in pr.values())


def transfer_survives_dp(P, side_labels):
    """`transfer_survives` on the DP path — same predicate, no `n!`."""
    S = sorted(side_labels)
    if len(S) < 2:
        return False, 0, None
    pr_full = pair_probabilities_dp(P)
    Q, idx = P.induced(S)
    inv = {i: v for v, i in idx.items()}
    pr_side = pair_probabilities_dp(Q)
    nbal = 0
    for (i, j), p_side in pr_side.items():
        if not balanced(p_side):
            continue
        nbal += 1
        x, y = inv[i], inv[j]
        key = (x, y) if (x, y) in pr_full else (y, x)
        if key not in pr_full:
            continue
        p_full = pr_full[key] if key == (x, y) else 1 - pr_full[key]
        if balanced(p_full):
            return True, nbal, ((x, y), p_side, p_full)
    return False, nbal, None


def chain_plus_isolated(n):
    """`mg-d3c7`'s family carrier: the chain `1 < 2 < … < n−1` plus one isolated
    element `0`. Labels match `mg-d3c7` §4.2 exactly."""
    return Poset(n, [(i, i + 1) for i in range(1, n - 1)])
