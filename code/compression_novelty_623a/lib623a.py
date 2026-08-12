"""Independent implementation of the objects in docs/imports/compression.tex.

Deliberately imports NOTHING from this repository's other libraries.  The point of
this instrument is to decide whether the note's claims are true and whether they are
new; a shared poset/eigen library would make "it agrees" a statement about one
derivation read twice.

Everything on a verdict path is exact rational arithmetic (Fraction).  The only
floats are in `gap_bk` / `gap_linear`, which are eigenvalue computations and are
labelled [FLOAT] wherever they are printed.

Conventions, fixed here once so that no downstream file re-chooses them:

  * A poset on `n` elements is a frozenset of ordered pairs (i, j) meaning i < j,
    irreflexive, antisymmetric, transitive.
  * A linear extension L is a tuple (x_1, ..., x_n) with x_a < x_b in P implying
    a < b.  I_k(L) = {x_1, ..., x_k}.
  * tau_i swaps positions i, i+1 (1-indexed) when those two elements are
    incomparable in P.  So tau_i is defined on L iff L[i-1], L[i] are incomparable.
  * BK chain: from L, pick i uniformly from {1, ..., n-1}; move to tau_i L if the
    swap is legal, else stay.  Stationary distribution uniform on L(P).
    Dirichlet form  E(f) = (1/2) sum_L pi(L) sum_M P(L,M) (f(M)-f(L))^2.
  * C_o(L) = (I_2, I_4, I_6, ...)   -- the "odd" compression of the note's section 1,
    named for the tau_odd edges it leaves free, NOT for the prefixes it keeps.
  * C_e(L) = (I_1, I_3, I_5, ...).
"""

from fractions import Fraction
from itertools import combinations, permutations, product


# ---------------------------------------------------------------- posets

def is_transitive(rel, n):
    for (a, b) in rel:
        for (c, d) in rel:
            if b == c and (a, d) not in rel:
                return False
    return True


def all_posets(n):
    """Every labelled poset on {0..n-1}, by brute force over the 3^C(n,2) choices
    per unordered pair (i<j, j<i, incomparable), filtered by transitivity."""
    pairs = list(combinations(range(n), 2))
    for choice in product((0, 1, 2), repeat=len(pairs)):
        rel = set()
        for (i, j), c in zip(pairs, choice):
            if c == 1:
                rel.add((i, j))
            elif c == 2:
                rel.add((j, i))
        if is_transitive(rel, n):
            yield frozenset(rel)


def incomparable_pairs(rel, n):
    """Unordered pairs {x,y} of P that are incomparable -- the index set I(P) of
    the note's section 2."""
    return [(i, j) for (i, j) in combinations(range(n), 2)
            if (i, j) not in rel and (j, i) not in rel]


def linear_extensions(rel, n):
    out = []
    for perm in permutations(range(n)):
        pos = {x: k for k, x in enumerate(perm)}
        if all(pos[a] < pos[b] for (a, b) in rel):
            out.append(perm)
    return out


def v_family(k):
    """V_k: the ordinal sum of k two-element antichains, n = 2k.  This is the family
    docs/OneThird-Hodge-Side-Leverage.md names as the one where the AT graph IS the
    hypercube Q_k.  Included as a named control: the note's odd compression must
    collapse to a single fiber there."""
    n = 2 * k
    rel = set()
    for a in range(n):
        for b in range(n):
            if a // 2 < b // 2:
                rel.add((a, b))
    return frozenset(rel), n


# ---------------------------------------------------- compressions and fibers

def C_odd(L):
    """(I_2, I_4, I_6, ...)"""
    n = len(L)
    return tuple(frozenset(L[:k]) for k in range(2, n + 1, 2))


def C_even(L):
    """(I_1, I_3, I_5, ...)"""
    n = len(L)
    return tuple(frozenset(L[:k]) for k in range(1, n + 1, 2))


def fibers(les, C):
    out = {}
    for L in les:
        out.setdefault(C(L), []).append(L)
    return out


def free_blocks(L, rel, parity):
    """The note's blocks B_j together with whether each is free.

    parity == 'odd':  blocks are positions (1,2), (3,4), ...  -- free under C_odd,
                      and their swaps are tau_1, tau_3, ...
    parity == 'even': blocks are positions (2,3), (4,5), ...  -- free under C_even,
                      and their swaps are tau_2, tau_4, ...

    Returns a list of (i, x, y) with i the 1-indexed tau that moves the block and
    {x, y} incomparable in P (i.e. the block is free).
    """
    n = len(L)
    start = 1 if parity == 'odd' else 2
    out = []
    for i in range(start, n, 2):
        x, y = L[i - 1], L[i]
        if (x, y) not in rel and (y, x) not in rel:
            out.append((i, x, y))
    return out


# ------------------------------------------------------- linear statistics

def pair_orientation(L, coeffs, a=Fraction(0)):
    """f(L) = a + sum_{{x,y} in I(P)} c_xy 1{x <_L y}, with the pair written (x,y),
    x < y as integers, and the indicator 1 when x precedes y in L."""
    pos = {x: k for k, x in enumerate(L)}
    tot = a
    for (x, y), c in coeffs.items():
        if pos[x] < pos[y]:
            tot += c
    return tot


def variance(vals):
    m = sum(vals) / len(vals)
    return sum((v - m) ** 2 for v in vals) / len(vals)


# ------------------------------------------------------------ the BK chain

def bk_neighbours(L, rel):
    """[(i, tau_i L)] over legal i."""
    n = len(L)
    out = []
    for i in range(1, n):
        x, y = L[i - 1], L[i]
        if (x, y) not in rel and (y, x) not in rel:
            M = list(L)
            M[i - 1], M[i] = M[i], M[i - 1]
            out.append((i, tuple(M)))
    return out


def bk_energy(les, rel, f):
    """E(f) = (1/2) * (1/|L|) * sum_L (1/(n-1)) sum_{legal i} (f(tau_i L) - f(L))^2"""
    n = len(les[0])
    tot = Fraction(0)
    for L in les:
        for (_i, M) in bk_neighbours(L, rel):
            tot += (f[M] - f[L]) ** 2
    return tot / (2 * len(les) * (n - 1))


def bk_apply(les, rel, f):
    """(P_BK f)(L)."""
    n = len(les[0])
    out = {}
    for L in les:
        nb = bk_neighbours(L, rel)
        s = f[L] * Fraction(n - 1 - len(nb), n - 1)
        for (_i, M) in nb:
            s += f[M] / (n - 1)
        out[L] = s
    return out


def conditional_expectation(les, C, f):
    fib = fibers(les, C)
    out = {}
    for _key, members in fib.items():
        m = sum(f[L] for L in members) / len(members)
        for L in members:
            out[L] = m
    return out


def mean_conditional_variance(les, C, f):
    """E[ Var(f | C) ] -- the fiber-size-weighted mean of within-fiber variance."""
    fib = fibers(les, C)
    tot = Fraction(0)
    for _key, members in fib.items():
        tot += len(members) * variance([f[L] for L in members])
    return tot / len(les)
