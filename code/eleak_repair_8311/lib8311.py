"""mg-8311 — INDEPENDENT machinery for the E_leak ruling.

This file imports NOTHING from `lib2de0` and NOTHING from `lib76b2`. That is deliberate and
it is the point: the ticket asks me to confirm a divergence between two functions, and a
confirmation that calls one of the functions under audit shares its defects. The poset
enumerator, the linear-extension enumerator and BOTH leak conventions are written fresh
here. Where a count of mine agrees with mg-2de0's or mg-76b2's, that agreement is evidence;
where it disagrees, the disagreement is real and not a shared bug.

Exact throughout: Fraction, no floats in any comparison that produces a verdict.

THE TWO CONVENTIONS, both implemented, both named, neither privileged by the code:

  leak_def(A, p)   = |A \\ sigma(A)|,  sigma(A) = {p[i] : i in A}
                     the positions INDEXED BY A.  This is `sigma(A)` read as function
                     application, which is how STATE.md:41 writes it.

  leak_conv(A, p)  = |A| - |A & set(p[:|A|])|
                     the first |A| POSITIONS.  This is what lib2de0.E_leak computes.

  leak_inv(A, p)   = |A \\ sigma^{-1}(A)|,  the OTHER natural reading of sigma(A).
                     Equal in CARDINALITY to leak_def for every (A, p) -- asserted here,
                     CHECKED in r1_witness.py.  It exists in this file only so that the
                     ruling is demonstrably a two-way choice and not a three-way one.

`p` is a tuple with p[position] = element, matching lib2de0's convention so that the
comparison is like-for-like.
"""

from fractions import Fraction as F
from itertools import permutations, combinations


# --------------------------------------------------------------- the two conventions

def leak_def(A, p):
    """|A \\ sigma(A)| with sigma(A) = {p[i] : i in A} -- the positions INDEXED BY A."""
    img = frozenset(p[i] for i in A)
    return len(A - img)


def leak_inv(A, p):
    """|A \\ sigma^{-1}(A)| -- the other reading. Same cardinality as leak_def."""
    inv = {x: i for i, x in enumerate(p)}
    img = frozenset(inv[x] for x in A)
    return len(A - img)


def leak_conv(A, p):
    """lib2de0's convention: the first |A| POSITIONS, whatever A's members are."""
    return len(A) - len(A & frozenset(p[:len(A)]))


LEAKS = {"def": leak_def, "conv": leak_conv, "inv": leak_inv}


# ------------------------------------------------------------------------- posets

class P8311:
    """A poset on {0..n-1} with the identity permutation required to be a linear extension.

    `rel` is the strict order as a set of (x, y) pairs meaning x < y, given already
    transitively closed (the enumerator only ever hands closed sets in).
    """

    def __init__(self, n, rel, name):
        self.n = n
        self.rel = frozenset(rel)
        self.name = name
        for (x, y) in self.rel:
            assert x < y, f"{name}: identity is not a linear extension ({x},{y})"
        self._les = None

    def leq(self, x, y):
        return x == y or (x, y) in self.rel

    def linear_extensions(self):
        if self._les is None:
            self._les = tuple(p for p in permutations(range(self.n))
                              if self._is_le(p))
        return self._les

    def _is_le(self, p):
        """Independent of lib2de0's `p.index(x) < p.index(y)`: build the position map once.

        Same predicate, different code path -- so a defect in one is not a defect in both.
        """
        pos = [0] * self.n
        for i, x in enumerate(p):
            pos[x] = i
        return all(pos[x] < pos[y] for (x, y) in self.rel)

    def cuts(self):
        """Every proper cut A, 0 < |A| < n, as a frozenset. 2^n - 2 of them."""
        for size in range(1, self.n):
            for S in combinations(range(self.n), size):
                yield frozenset(S)

    # ---- expectations, exact

    def E_leak(self, A, which):
        f = LEAKS[which]
        les = self.linear_extensions()
        return F(sum(f(A, p) for p in les), len(les))

    def phi(self, A, which):
        return self.E_leak(A, which) / min(len(A), self.n - len(A))

    def phi_star(self, which):
        return min(self.phi(A, which) for A in self.cuts())

    def K_k(self, p, k):
        """|A_k \\ sigma(A_k)| for the PREFIX A_k = {0..k-1}, computed via leak_def.

        Deliberately routed through leak_def rather than through a prefix special case:
        that both conventions reproduce this is r3's business, not something assumed here.
        """
        return leak_def(frozenset(range(k)), p)

    def delta_1_prefix(self, k):
        les = self.linear_extensions()
        return F(sum(self.K_k(p, k) for p in les), len(les)) / min(k, self.n - k)

    def prefix_min(self):
        return min(self.delta_1_prefix(k) for k in range(1, self.n))


def all_posets_8311(n):
    """EVERY poset on {0..n-1} with the identity a linear extension.

    Independent construction: rather than masking over 2^C(n,2) candidate relation sets and
    filtering for transitive closure (lib2de0's route, which spends 2^15 = 32768 masks at
    n=6 and 2^21 at n=7), this GROWS the closed sets by adding one covering pair at a time
    and closing, keeping a `seen` set. Different algorithm, same object -- so the counts
    agreeing with lib2de0's 40 and 357 is a real cross-check.
    """
    pairs = [(x, y) for x, y in combinations(range(n), 2)]
    start = frozenset()
    seen = {start}
    frontier = [start]
    while frontier:
        nxt = []
        for rel in frontier:
            for pr in pairs:
                if pr in rel:
                    continue
                grown = _close(rel | {pr})
                if grown is None or grown in seen:
                    continue
                seen.add(grown)
                nxt.append(grown)
        frontier = nxt
    out = []
    for rel in sorted(seen, key=lambda r: (len(r), sorted(r))):
        out.append(P8311(n, rel, f"Q{len(out)} n={n}"))
    return out


def _close(rel):
    """Transitive closure. Returns None if closure would need a non-upward pair (x >= y),
    which cannot happen when every seed pair is upward -- asserted by returning None so a
    silent violation becomes a missing poset rather than a bad one."""
    rel = set(rel)
    changed = True
    while changed:
        changed = False
        for (a, b) in list(rel):
            for (c, d) in list(rel):
                if b == c and (a, d) not in rel:
                    if a >= d:
                        return None
                    rel.add((a, d))
                    changed = True
    return frozenset(rel)


def antichain(n):
    return P8311(n, [], f"antichain n={n}")


# --------------------------------------------------- the transport matrix and its form

def S_P(P):
    """The SYMMETRISED transport operator, built here from its definition and from nothing
    else. T[x][i] = Pr[pos_sigma(x) = i] over uniform sigma in L(P), relative to the
    reference order e = identity (so element x has rank x and the matrix is square on
    {0..n-1}). S_P = (T + T^t)/2.

    Named as a matrix, not an eigenvalue: no eigenvalue is taken anywhere in this
    instrument. The only thing asked of S_P is its QUADRATIC FORM on indicator vectors.
    """
    n = P.n
    les = P.linear_extensions()
    N = len(les)
    T = [[F(0) for _ in range(n)] for _ in range(n)]
    for p in les:
        for i, x in enumerate(p):
            T[x][i] += F(1, N)
    return [[(T[x][y] + T[y][x]) / 2 for y in range(n)] for x in range(n)]


def quad_form_I_minus_S(P, A, S=None):
    """<1_A, (I - S_P) 1_A>, exact."""
    if S is None:
        S = S_P(P)
    n = P.n
    tot = F(0)
    for x in A:
        tot += F(1)                      # (I 1_A)_x = 1
        for y in A:
            tot -= S[x][y]
    return tot


# ------------------------------------------------------------------------ reporting

class Tally:
    def __init__(self):
        self.bad = 0

    def report(self, label, bad, total, grain, population, fatal=True):
        if fatal:
            self.bad += bad
        flag = "OK  " if bad == 0 else ("BAD " if fatal else "MEAS")
        print(f"  {flag} {label}: {bad} / {total}")
        print(f"       population: {population}")
        print(f"       grain:      {grain}")
