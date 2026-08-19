#!/usr/bin/env python3
"""lib872c — THE CODE-SIDE READING OF A STRUCTURE RESULT THAT IS ALREADY PUBLISHED.

`mg-872c`.  The ticket names one open object: *a bound on a code's expected length PROVED FROM
hypothesis (1)*, and instructs that `mg-9b6b` and `mg-0b96` be checked BEFORE anything is built,
because *"the same dial may already have a number on it."*

IT HAS.  `mg-6ff4` `c1` `m4` publishes, exhaustively to `n = 9` and width-restricted to `n = 12`:

    a boundary poset (delta(P) = 1/3) on n elements is  k >= 1  copies of V  ordinally summed
    with  n - 3k  singletons.

Every quantity this directory prints is arithmetic on that sentence.  `e(P) = 3^k`, `w(P) = 2`
(which is `docs/FACTS.md` F19, already banked), and therefore the expected length of EVERY code on
the class is a closed-form function of `P`.  This library is the arithmetic, and the two
conversions it needs.

WHAT IT IMPORTS AND WHY IT IMPORTS RATHER THAN RE-SPELLS (`mg-d2c2`, `mg-1344`'s P5):

  * `lib6ff4`  — enumeration, `count_ext`, `width`, `delta_at_most`.  The population this arm
    reports on IS `mg-6ff4`'s boundary class; a second spelling of `delta` could make the two
    documents disagree about which 31 posets are in question while both printed `1/3`.
  * `lib9d9e`  — `q_minimals` and `q_merge_p` VERBATIM.  The ticket is about `mg-9d9e`'s codes.
    A re-spelling here would make `P2` and `P3` statements about this file's arithmetic rather
    than about the codes `mg-9d9e` measured.

An import whose controls live elsewhere is unchecked from here, so `k0` re-checks both against
brute force before any arm uses either (`mg-9b6b`'s discipline).

THE ONE THING THAT IS NOT IMPORTED, DELIBERATELY.  `ordinal_cut_blocks` below is written here and
does NOT call `lib6ff4.ordinal_summands`.  `P1` — `e(P) = 3^k` — is the identity every downstream
figure is arithmetic on, and re-deriving it through the same decomposition that `mg-6ff4` used
would test nothing.  `k0` `C4` asserts the two spellings AGREE, which is the check that is worth
having; the answer is computed with this one.

EMPTY IS NOT ZERO.  `delta < 1/3` is the counterexample condition and its class is empty at every
`n` reachable.  `fmt_empty` exists so that no arm here can print `0` for it (`mg-9b6b`'s
carry-forward; `mg-3c92` measured that this estate already keeps them apart at 9 sites in 10).
"""

import math
import os
import sys
from fractions import Fraction

_HERE = os.path.dirname(os.path.abspath(__file__))
_CODE = os.path.dirname(_HERE)
for _d in ("boundary_epsilon_6ff4", "lstar_code_9d9e"):
    _p = os.path.join(_CODE, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import lib6ff4                                    # noqa: E402
import lib9d9e                                    # noqa: E402

THIRD = lib6ff4.THIRD
TWO_FIFTHS = Fraction(2, 5)

# `mg-6ff4` c1/c2's published boundary counts, CITED for cross-instrument agreement and not
# re-derived above n = 8.  Source: code/boundary_epsilon_6ff4/out_c1_census.txt (exhaustive,
# n <= 9) and out_c2_reach.txt (width <= 3 to n = 10, width <= 2 to n = 12).
MG6FF4_BOUNDARY_COUNTS = {3: 1, 4: 2, 5: 3, 6: 5, 7: 8, 8: 12, 9: 18}


def fmt_empty(count, of_what="member"):
    """`EMPTY` and `0` are different answers and are printed differently."""
    return "EMPTY (no %s exists)" % of_what if count == 0 else str(count)


# ------------------------------------------------------------------------------------------------
# the two representations, and the conversion between them
# ------------------------------------------------------------------------------------------------


def down_to_rel(n, down):
    """`lib6ff4`'s bitmask form -> `lib9d9e`'s set-of-pairs form (transitively closed, strict)."""
    return frozenset((x, y) for y in range(n) for x in range(n) if down[y] >> x & 1)


def rel_to_down(n, rel):
    """`lib9d9e`'s form -> `lib6ff4`'s.  The inverse of `down_to_rel` on transitive relations."""
    d = [0] * n
    for (x, y) in rel:
        d[y] |= 1 << x
    return tuple(d)


# ------------------------------------------------------------------------------------------------
# the decomposition — written here, NOT imported (see the module docstring)
# ------------------------------------------------------------------------------------------------


def ordinal_cut_blocks(n, down):
    """The finest ordinal-sum decomposition of `(n, down)`, as a list of element tuples.

    `S` is an ORDINAL CUT iff every element of `S` is strictly below every element of its
    complement.  The cuts are totally ordered by inclusion (if `S`, `T` are cuts and `x` is in
    `S \\ T` then everything in `T` is above `x`, hence `T` is a subset of `S`), so the finest
    blocks are the differences of consecutive cuts.  Exhaustive over subsets: `n <= 9` here."""
    full = (1 << n) - 1
    cuts = {0, full}
    for m in range(1, full):
        below = [x for x in range(n) if m >> x & 1]
        above = [y for y in range(n) if not (m >> y & 1)]
        if all(down[y] >> x & 1 for x in below for y in above):
            cuts.add(m)
    cuts = sorted(cuts)
    blocks = []
    for a, b in zip(cuts, cuts[1:]):
        blk = b & ~a
        blocks.append(tuple(i for i in range(n) if blk >> i & 1))
    return blocks


def block_kind(n, down, blk):
    """`'singleton'`, `'V'`, or a description of whatever else it is.

    `V` is the 3-element poset with exactly one strict relation — a 2-chain beside an isolated
    point.  That is the summand `mg-6ff4` c1 m4 names."""
    if len(blk) == 1:
        return "singleton"
    if len(blk) == 3:
        rel = [(x, y) for x in blk for y in blk if down[y] >> x & 1]
        if len(rel) == 1:
            return "V"
    return "other(size=%d)" % len(blk)


def v_count(n, down):
    """`(k, kinds)` — the number of `V` summands, and every block's kind.

    `k` is `None` when some block is neither a singleton nor a `V`, which is the shape the
    structure result forbids on the boundary class."""
    blocks = ordinal_cut_blocks(n, down)
    kinds = [block_kind(n, down, b) for b in blocks]
    if all(k in ("singleton", "V") for k in kinds):
        return kinds.count("V"), kinds
    return None, kinds


# ------------------------------------------------------------------------------------------------
# the population
# ------------------------------------------------------------------------------------------------


def hypothesis_class(classes, n, bound=THIRD):
    """[(down, delta, table)] over every non-chain isomorphism class at `n` with `delta <= bound`."""
    out = []
    for down in classes[n]:
        ok, d, tbl = lib6ff4.delta_at_most(n, down, bound)
        if ok:
            out.append((down, d, tbl))
    return out


# ------------------------------------------------------------------------------------------------
# codelengths
# ------------------------------------------------------------------------------------------------


def elen(n, down, qfn, ctx=None, les=None):
    """`(E[len] as an exact Fraction or None, E[len] as a float)` under `Unif(L(P))`.

    Exact whenever every codeword length is an integer — which is what happens on the whole
    hypothesis class, because `|minimals|` there is never more than 2.  Off the class the lengths
    are irrational and only the float is returned, which is why both are always reported."""
    rel = down_to_rel(n, down)
    if les is None:
        les = lib9d9e.linear_extensions(rel, n)
    if ctx is None:
        ctx = lib9d9e.context(rel, n, LEs=les)
    tot_f = 0.0
    exact = Fraction(0)
    all_int = True
    for L in les:
        q = qfn(L, ctx)
        bits = lib9d9e.ideal_bits(q)
        tot_f += bits
        d = q.denominator
        if q.numerator == 1 and d & (d - 1) == 0:
            exact += Fraction(d.bit_length() - 1)
        else:
            all_int = False
    m = len(les)
    return (exact / m if all_int else None), tot_f / m


def opt_prefix_elen(m):
    """Expected length of an OPTIMAL prefix code on `m` equiprobable words, exact.

    `L = floor(log2 m)`, `a = 2^(L+1) - m` words of length `L` and `m - a` of length `L + 1`;
    `E = L + 1 - a/m`.  Needs `m` and nothing else — which is why `P10` is a statement about
    `Q2'`: on this class `m = e(P) = 3^k` is read off the decomposition."""
    if m == 1:
        return Fraction(0)
    L = m.bit_length() - 1
    if 1 << L == m:
        return Fraction(L)
    a = (1 << (L + 1)) - m
    return Fraction(L + 1) - Fraction(a, m)


def benchmark_bits(n, down):
    """`mg-9d9e` §5.3's benchmark `n log2 w(P)`, exact when `w` is a power of two."""
    w = lib6ff4.width(n, down)
    return w, (Fraction(n * (w.bit_length() - 1)) if w & (w - 1) == 0 else None), n * math.log2(w)


LOG2_3 = math.log2(3)


def log2_e_exact(k):
    """`log2 e(P)` on the class, as `k * log2 3`."""
    return k * LOG2_3
