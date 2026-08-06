"""mg-2de0 — shared machinery for the independent audit of the mg-00b9 direct-prefix route.

OPERATOR SCOPE: everything here is on the TRANSPORT axis — footrule / inv_e / K_k / Delta_1 /
Phi_P / lambda_std(S_P). Nothing here is Delta_AT, A(P), or the Hodge axis. There is no
eigenvalue computation in this file at all: lambda_std is never computed, only the corpus's
master BOUND on 1-lambda_std is evaluated, and that is named as a bound everywhere it is used.

Everything is exact: Fraction throughout, no floats in any decision. Floats appear only in
printed display columns, never in a comparison that produces a verdict.

Definitions, all taken from the corpus and cited at the call site:
  A_k        = {0,...,k-1}     the first k elements of the reference order e (0-indexed here)
  K_k(sigma) = |A_k \\ sigma(A_k)|   where sigma(A_k) = the elements in the first k POSITIONS
  D(sigma)   = sum_x |pos_sigma(x) - rank_e(x)|          (footrule)
  inv_e      = # pairs {x,y} whose e-order and sigma-order disagree (Kendall tau to e)
  Delta_1(A) = E|A \\ sigma(A)| / min(|A|,|A^c|)
  Phi_P(A)   = same quantity, read as a conductance, minimised over ALL cuts A
"""

from fractions import Fraction as F
from itertools import permutations, combinations


# ---------------------------------------------------------------- permutations

def K_k(perm, k):
    """K_k = |A_k \\ sigma(A_k)|, A_k = {0..k-1}. perm[p] = element at position p.

    An element x is in A_k \\ sigma(A_k) iff rank_e(x) < k <= pos_sigma(x). We take the
    reference order e to be the identity, so rank_e(x) = x.
    """
    first_k_positions = set(perm[:k])
    return sum(1 for x in range(k) if x not in first_k_positions)


def footrule(perm):
    """D(sigma) = sum_x |pos_sigma(x) - rank_e(x)|, e = identity."""
    pos = {x: p for p, x in enumerate(perm)}
    return sum(abs(pos[x] - x) for x in range(len(perm)))


def inversions(perm):
    """inv_e(sigma) = # pairs disagreeing with e. For sigma in L(P) only incomparable pairs
    can disagree, so this equals inv_e as the corpus defines it (comparable pairs never flip
    in a linear extension) -- that equality is asserted here and CHECKED in a2_lemma_b.py."""
    n = len(perm)
    return sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])


def sum_K(perm):
    """sum_{k=1}^{n-1} K_k(sigma) -- the left side of Lemma A."""
    n = len(perm)
    return sum(K_k(perm, k) for k in range(1, n))


# ---------------------------------------------------------------------- posets

class Poset:
    """A poset on {0,...,n-1}. `rel` is the strict order as a set of (x,y) meaning x < y.
    The identity permutation is required to be a linear extension (the reference order e)."""

    def __init__(self, n, rel, name):
        self.n = n
        self.name = name
        self.rel = set()
        # transitive closure
        rel = set(rel)
        changed = True
        while changed:
            changed = False
            for (a, b) in list(rel):
                for (c, d) in list(rel):
                    if b == c and (a, d) not in rel:
                        rel.add((a, d))
                        changed = True
        self.rel = rel
        for (x, y) in self.rel:
            assert x < y, f"{name}: identity is not a linear extension ({x},{y})"
        self._le = None
        self._cache = {}

    def leq(self, x, y):
        return x == y or (x, y) in self.rel

    def incomparable_pairs(self):
        if "ip" not in self._cache:
            self._cache["ip"] = self._incomparable_pairs()
        return self._cache["ip"]

    def _incomparable_pairs(self):
        return [(x, y) for x, y in combinations(range(self.n), 2)
                if not self.leq(x, y) and not self.leq(y, x)]

    def linear_extensions(self):
        if self._le is None:
            self._le = [p for p in permutations(range(self.n))
                        if all(p.index(x) < p.index(y) for (x, y) in self.rel)]
        return self._le

    def width(self):
        """Largest antichain, by brute force over subsets (n <= 8 here)."""
        best = 0
        for size in range(self.n, 0, -1):
            if size <= best:
                break
            for S in combinations(range(self.n), size):
                if all(not self.leq(x, y) and not self.leq(y, x)
                       for x, y in combinations(S, 2)):
                    best = max(best, size)
                    break
        return best

    # ---- expectations over L(P), exact

    def E_K(self, k):
        key = ("K", k)
        if key not in self._cache:
            les = self.linear_extensions()
            self._cache[key] = F(sum(K_k(p, k) for p in les), len(les))
        return self._cache[key]

    def E_footrule(self):
        if "D" not in self._cache:
            les = self.linear_extensions()
            self._cache["D"] = F(sum(footrule(p) for p in les), len(les))
        return self._cache["D"]

    def E_inv(self):
        if "I" not in self._cache:
            les = self.linear_extensions()
            self._cache["I"] = F(sum(inversions(p) for p in les), len(les))
        return self._cache["I"]

    def delta_1_prefix(self, k):
        """Delta_1(A_k) = E[K_k]/min(k, n-k)  (STATE.md:39 with A = A_k)."""
        return self.E_K(k) / min(k, self.n - k)

    def E_leak(self, A):
        """E|A \\ sigma(A)| for an arbitrary cut A (a frozenset of elements)."""
        if ("L", A) in self._cache:
            return self._cache[("L", A)]
        les = self.linear_extensions()
        a = len(A)
        tot = 0
        for p in les:
            tot += a - len(A & set(p[:a]))
        self._cache[("L", A)] = F(tot, len(les))
        return self._cache[("L", A)]

    def phi(self, A):
        """Phi_P(A) = E|A \\ sigma(A)| / min(|A|,|A^c|)."""
        a = len(A)
        return self.E_leak(A) / min(a, self.n - a)

    def phi_star(self):
        """min over ALL cuts A with 0 < |A| < n."""
        best = None
        elts = list(range(self.n))
        for size in range(1, self.n):
            for S in combinations(elts, size):
                v = self.phi(frozenset(S))
                if best is None or v < best:
                    best = v
        return best

    def delta(self):
        """The balance constant: max over incomparable pairs {x,y} of
        min(pr(x before y), pr(y before x)). delta >= 1/3 is the conjecture.
        Returns None if there is no incomparable pair (a chain has no delta)."""
        ips = self.incomparable_pairs()
        if not ips:
            return None
        les = self.linear_extensions()
        N = len(les)
        best = F(0)
        for (x, y) in ips:
            before = sum(1 for p in les if p.index(x) < p.index(y))
            v = min(F(before, N), F(N - before, N))
            if v > best:
                best = v
        return best


# ------------------------------------------------------------ poset population

def named_posets(nmax=7):
    """The NAMED families. Population is stated at every print site that uses it."""
    out = []
    for n in range(2, nmax + 1):
        out.append(Poset(n, [], f"antichain n={n}"))
        out.append(Poset(n, [(i, i + 1) for i in range(n - 1)], f"chain n={n}"))
        # W_n = C_{n-1} + one free point (the corpus's own W_m, attempt-mg-88bd.md:64)
        out.append(Poset(n, [(i, i + 1) for i in range(n - 2)], f"chain_{n-1}+pt n={n}"))
        # ordinal sum of two antichains, split as evenly as possible
        h = n // 2
        out.append(Poset(n, [(i, j) for i in range(h) for j in range(h, n)],
                         f"ordsum A{h}<A{n-h} n={n}"))
        # union of two chains (interleaved) -- the "both sides chains" case of item (e)
        evens = [i for i in range(n) if i % 2 == 0]
        odds = [i for i in range(n) if i % 2 == 1]
        rel = [(evens[i], evens[i + 1]) for i in range(len(evens) - 1)] + \
              [(odds[i], odds[i + 1]) for i in range(len(odds) - 1)]
        out.append(Poset(n, rel, f"two_chains(interleaved) n={n}"))
        if n >= 4:
            # N-poset padded with an antichain -- L4's named adversary
            out.append(Poset(n, [(0, 2), (1, 2), (1, 3)], f"N-poset+{n-4}pts n={n}"))
    return out


def all_posets(n):
    """EVERY poset on {0..n-1} for which the identity is a linear extension, up to the
    labelling that fixes e = identity. Enumerated by brute force over the 2^C(n,2) candidate
    relation sets, keeping the transitively closed ones. Only used for small n."""
    pairs = list(combinations(range(n), 2))
    seen = set()
    out = []
    for mask in range(1 << len(pairs)):
        rel = frozenset(pairs[i] for i in range(len(pairs)) if mask >> i & 1)
        # keep only transitively closed relation sets, so each poset appears once
        closed = all((a, d) in rel for (a, b) in rel for (c, d) in rel if b == c)
        if not closed or rel in seen:
            continue
        seen.add(rel)
        out.append(Poset(n, rel, f"P{len(out)} n={n}"))
    return out


# ------------------------------------------------------- Lemma B, as three parts

def k_range(n, beta):
    """The integers k with beta*n <= k <= (1-beta)*n, and 1 <= k <= n-1.

    beta is a Fraction. The clamp to [1, n-1] is forced: Delta_1(A_k) is undefined at
    k = 0 and k = n (min(k,n-k) = 0), and at beta = 0 the range as literally written
    ([0, n]) contains both. mg-00b9 writes the range as [beta n, (1-beta) n]; this is the
    only reading under which the quantity it bounds exists.
    """
    lo = max(1, -((-beta * n) // 1))          # ceil(beta*n), exact on Fractions
    hi = min(n - 1, ((1 - beta) * n) // 1)    # floor((1-beta)*n)
    return [int(k) for k in range(int(lo), int(hi) + 1)]


def denom_exact(n, beta):
    """sum_{k in K_beta} min(k, n-k) -- the mediant denominator, exact."""
    return sum(min(k, n - k) for k in k_range(n, beta))


def denom_claimed(n, beta):
    """(1 - 4 beta^2) n^2 / 4 -- what mg-00b9's Lemma B substitutes for denom_exact."""
    return (1 - 4 * beta * beta) * F(n * n, 4)


BETAS = [F(0), F(1, 16), F(1, 8), F(1, 6), F(1, 5), F(1, 4), F(1, 3), F(2, 5)]
