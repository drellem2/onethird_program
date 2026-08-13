"""mg-8b32 — WHICH FUNCTIONS FACTOR THROUGH THE PAIR MARGINALS.  Independent of `lib0fc6`.

Nothing in this directory imports `code/compression2_scope_0fc6/`.  That is deliberate and it is
the same discipline `mg-8748`'s `c4.1` applied to `mg-0fc6`'s `a2.3`: the witness this ticket
CITES rather than re-runs is `a2.3`'s, and every object around it here — the linear-extension
enumerator, the marginal map, the realizability oracle, the majority order — is re-derived from
the definitions so that a shared bug in one library cannot produce agreement in two.

EXACT ARITHMETIC THROUGHOUT.  Every marginal, every kernel direction and every fiber point is a
`Fraction`.  The only floats in this directory are the entropies printed for reading, and they
are printed beside the exact statement they illustrate, never used to decide a verdict.
"""

from fractions import Fraction
from itertools import combinations, permutations, product
import math
import sys

# ------------------------------------------------------------------ posets


def is_strict_order(n, lt):
    """`lt[x][y]` is a strict partial order: irreflexive, asymmetric, transitive."""
    for x in range(n):
        if lt[x][x]:
            return False
        for y in range(n):
            if lt[x][y] and lt[y][x]:
                return False
            if not lt[x][y]:
                continue
            for z in range(n):
                if lt[y][z] and not lt[x][z]:
                    return False
    return True


def all_posets(n):
    """Every LABELLED strict partial order on `{0..n-1}`, as a tuple-of-tuples `lt`.

    Enumerated by assigning each unordered pair one of three states and testing transitivity.
    `3^C(n,2)`: 27 at n=3, 729 at n=4, 59049 at n=5.  n=6 is 14.3M and is NOT enumerated here —
    every n=6 statement in this directory names its population explicitly instead.
    """
    prs = list(combinations(range(n), 2))
    out = []
    for state in product((0, 1, 2), repeat=len(prs)):
        lt = [[False] * n for _ in range(n)]
        for (x, y), s in zip(prs, state):
            if s == 1:
                lt[x][y] = True
            elif s == 2:
                lt[y][x] = True
        if is_strict_order(n, lt):
            out.append(tuple(tuple(r) for r in lt))
    return out


def antichain(n):
    return tuple(tuple(False for _ in range(n)) for _ in range(n))


def linexts(n, lt):
    """`L(P)`, as a sorted tuple of permutations (each a tuple of elements, first-to-last)."""
    out = []
    order = []
    used = [False] * n

    def rec():
        if len(order) == n:
            out.append(tuple(order))
            return
        for x in range(n):
            if used[x]:
                continue
            if any(lt[y][x] and not used[y] for y in range(n)):
                continue
            used[x] = True
            order.append(x)
            rec()
            order.pop()
            used[x] = False

    rec()
    return tuple(sorted(out))


# ------------------------------------------------------------------ the marginal map


def ordered_pairs(n):
    return [(x, y) for x in range(n) for y in range(n) if x != y]


def marg(mu, n):
    """`pi[(x,y)] = Pr_mu[x before y]`, EVERY ordered pair present, exact.

    Absent pairs would make two marginal vectors compare unequal for a reason that is not a
    difference in the measure, which is exactly the comparison this whole ticket turns on.
    """
    pi = {k: Fraction(0) for k in ordered_pairs(n)}
    for sig, w in mu.items():
        if w == 0:
            continue
        pos = [0] * n
        for t, x in enumerate(sig):
            pos[x] = t
        for x, y in pi:
            if pos[x] < pos[y]:
                pi[(x, y)] += w
    return pi


def unif(S):
    """The uniform measure on a non-empty collection of orders."""
    S = list(S)
    return {sig: Fraction(1, len(S)) for sig in S}


def marg_set(S, n):
    return marg(unif(S), n)


def forced_poset(pi, n):
    """`P(pi) := {(x,y) : pi_xy = 1}` — THE POSET A MARGINAL VECTOR ALREADY CARRIES.

    This function is the whole content of b1: its input is the marginal vector and NOTHING else,
    so anything computed from its output factors through the pair marginals by construction.
    """
    lt = [[False] * n for _ in range(n)]
    for (x, y), v in pi.items():
        if v == 1:
            lt[x][y] = True
    return tuple(tuple(r) for r in lt)


def support(mu):
    return tuple(sorted(sig for sig, w in mu.items() if w != 0))


# ------------------------------------------------------------------ realizability


def realizable(mu, n):
    """Is `mu` the UNIFORM measure on `L(Q)` for some poset `Q` on n elements?  (exact, no search)

    If `supp(mu) = L(Q)` then `Q` is forced — it is the intersection of the orders in the support
    — so the test is: uniform on its support, and the support is closed under being that
    intersection's linear extensions.  Cross-checked against brute force over ALL posets in b0.
    """
    S = support(mu)
    if not S:
        return False, "empty support"
    w0 = mu[S[0]]
    if any(mu[s] != w0 for s in S):
        return False, "not uniform on its support"
    lt = [[True] * n for _ in range(n)]
    for i in range(n):
        lt[i][i] = False
    for sig in S:
        pos = [0] * n
        for t, x in enumerate(sig):
            pos[x] = t
        for x in range(n):
            for y in range(n):
                if x != y and pos[x] > pos[y]:
                    lt[x][y] = False
    got = linexts(n, lt)
    if got != S:
        return False, f"support is not L(P): |L(P)|={len(got)} vs |supp|={len(S)}"
    return True, "uniform on L(P)"


def realizable_bruteforce(mu, n, posets_n):
    """The same question answered by trying EVERY poset.  Slow, and that is the point: it shares
    no reasoning with `realizable`, so agreement between the two is evidence and not a tautology.
    """
    S = set(support(mu))
    w0 = mu[support(mu)[0]] if S else None
    if not S or any(mu[s] != w0 for s in S):
        return False
    for lt in posets_n:
        if set(linexts(n, lt)) == S:
            return True
    return False


# ------------------------------------------------------------------ the majority order L*


def lstar(pi, n):
    """The distinguished / majority order `L*`, or `None` if the majority tournament is not a
    total order.  READS THE MARGINAL VECTOR AND NOTHING ELSE — that is the point of the signature.
    """
    half = Fraction(1, 2)
    wins = [0] * n
    for x, y in combinations(range(n), 2):
        if pi[(x, y)] > half:
            wins[x] += 1
        elif pi[(x, y)] < half:
            wins[y] += 1
        else:
            return None
    order = sorted(range(n), key=lambda x: -wins[x])
    for i in range(n):
        for j in range(i + 1, n):
            if pi[(order[i], order[j])] <= half:
                return None
    return tuple(order)


def max_flip(pi, star):
    """`max_{i<j} Pr[v_j before v_i]` — compression2's hypothesis (1), a function of `pi` alone."""
    n = len(star)
    worst = Fraction(0)
    for i in range(n):
        for j in range(i + 1, n):
            v = pi[(star[j], star[i])]
            if v > worst:
                worst = v
    return worst


# ------------------------------------------------------------------ the fiber over a marginal vector


def _rref(rows, ncols):
    """Exact reduced row echelon form over Q.  Returns (rows, pivot column per row)."""
    rows = [list(r) for r in rows]
    pivots = []
    r = 0
    for c in range(ncols):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = Fraction(1) / rows[r][c]
        rows[r] = [v * inv for v in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], pivots


def kernel_basis(S, n):
    """Basis of `{v in Q^S : sum v = 0 and the pair-marginal map sends v to 0}`.

    A vector in this kernel is exactly a direction along which a measure supported on `S` can be
    moved WITHOUT MOVING ANY PAIR MARGINAL.  `a2.3`'s witness is one such direction, found by a
    different route (a commuting square of adjacent swaps); this one is the whole space.
    """
    S = list(S)
    rows = [[Fraction(1)] * len(S)]
    for x, y in combinations(range(n), 2):
        row = []
        for sig in S:
            pos = [0] * n
            for t, e in enumerate(sig):
                pos[e] = t
            row.append(Fraction(1) if pos[x] < pos[y] else Fraction(0))
        rows.append(row)
    red, pivots = _rref(rows, len(S))
    free = [c for c in range(len(S)) if c not in pivots]
    basis = []
    for f in free:
        v = [Fraction(0)] * len(S)
        v[f] = Fraction(1)
        for i, p in enumerate(pivots):
            v[p] = -red[i][f]
        basis.append(v)
    return S, basis


# ------------------------------------------------------------------ entropy


def entropy_bits(mu):
    """`H(mu)` in bits.  A float, and used only for printing — no verdict in this directory is
    decided on it (see b4, where the tightness statement is decided on EXACT support containment).
    """
    h = 0.0
    for w in mu.values():
        if w > 0:
            p = float(w)
            h -= p * math.log2(p)
    return h


# ------------------------------------------------------------------ transcript helpers

_FAILED = []


def banner(t):
    print()
    print("=" * 78)
    print(t)
    print("=" * 78)


def verdict(ok, label, extra=""):
    print(f"  [{'GREEN' if ok else 'RED  '}] {label}" + (f"   {extra}" if extra else ""))
    if not ok:
        _FAILED.append(label)
    return ok


def note(s):
    print(f"       {s}")


def finish():
    print()
    if _FAILED:
        print(f"RESULT: RED — {len(_FAILED)} check(s) failed")
        for f in _FAILED:
            print(f"  - {f}")
        sys.exit(1)
    print("RESULT: GREEN — all checks passed")
    sys.exit(0)
