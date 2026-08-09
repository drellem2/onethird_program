"""B0 — controls for mg-d3c7's own instrument, run BEFORE any verdict.

Every number this audit publishes comes out of `lib_d3c7.py`, so the library is
checked against a brute-force enumerator that shares no code with it, plus two
counting identities that a systematically-missing poset class cannot survive.

A negative control is included: a deliberately WRONG reading of `sigma(A)` must
produce a DIFFERENT `Delta_1`, otherwise the test is not sensitive to the very
reading the audit turns on.
"""

import sys
from fractions import Fraction
from itertools import permutations

from lib_d3c7 import (
    naturally_labelled_posets, le_dp, delta1, pair_probs,
    incomparable_pairs, is_chain, down_sets,
)

fails = []


def check(name, got, want):
    ok = got == want
    print(f"  [{'ok ' if ok else 'FAIL'}] {name}: got {got}" + ("" if ok else f" want {want}"))
    if not ok:
        fails.append(name)


# ---------------------------------------------------------------- brute force
def brute_les(rel, n):
    """All linear extensions, by filtering all n! permutations. Shares no code
    with the down-set DP."""
    out = []
    for perm in permutations(range(n)):
        pos = {e: i for i, e in enumerate(perm)}
        ok = True
        for j in range(n):
            b = rel[j]
            for i in range(n):
                if b >> i & 1 and pos[i] > pos[j]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(perm)
    return out


def brute_delta1(rel, n, k):
    les = brute_les(rel, n)
    A = set(range(k))
    tot = 0
    for perm in les:
        first_k = set(perm[:k])          # sigma(A_k): elements in positions 0..k-1
        tot += len(A - first_k)          # |A_k \ sigma(A_k)|
    return Fraction(tot, len(les) * min(k, n - k))


def brute_delta1_OTHER_SIGMA(rel, n, k):
    """The OTHER reading of sigma(A) -- 'the set of POSITIONS of the elements of
    A' instead of 'the elements at the positions in A'.

    FINDING (C7): on PREFIX cuts these two readings are provably the same
    number, because A_k = {0..k-1} is simultaneously a set of labels and the set
    of positions 0..k-1, so
        |A \\ {positions of A}| = k - |{a in A : pos(a) < k}| = |A \\ sigma(A)|.
    The control is kept, and now ASSERTS the agreement, because 'the sigma(A)
    reading is ambiguous' is a live objection to the whole measurement and this
    is the fact that retires it.  It is NOT a sensitivity control -- C7b is."""
    les = brute_les(rel, n)
    A = set(range(k))
    tot = 0
    for perm in les:
        pos_of_A = {perm.index(a) for a in A}
        tot += len(A - pos_of_A)
    return Fraction(tot, len(les) * min(k, n - k))


def brute_delta1_MUTANT(rel, n, k):
    """SENSITIVITY CONTROL: Phi_P(A_k) -- the source's TRANSPORT CONDUCTANCE
    (`:229-237`), which divides by |A| rather than min(|A|,|B|).  It must differ
    from Delta_1 exactly on the cuts with k > n/2, and nowhere else.  If this
    agreed everywhere, the pipeline would be blind to the normalisation and the
    headline would rest on nothing."""
    les = brute_les(rel, n)
    A = set(range(k))
    tot = 0
    for perm in les:
        tot += len(A - set(perm[:k]))
    return Fraction(tot, len(les) * k)


def brute_pxy(rel, n, x, y):
    les = brute_les(rel, n)
    c = sum(1 for p in les if p.index(x) < p.index(y))
    return Fraction(c, len(les))


# ---------------------------------------------------------------- C1: counts
print("C1 — naturally labelled poset counts (OEIS A006455: 1,1,2,7,40,357,4824,96428)")
want = [1, 1, 2, 7, 40, 357, 4824, 96428]
for n in range(0, 8):
    got = sum(1 for _ in naturally_labelled_posets(n))
    check(f"|NLP({n})|", got, want[n])

print()
print("C2 — non-chain counts and prefix-cut counts (the population this audit sweeps)")
for n in range(2, 8):
    ps = list(naturally_labelled_posets(n))
    nonchain = sum(1 for r in ps if not is_chain(r, n))
    print(f"  n={n}: posets={len(ps)}  non-chain={nonchain}  "
          f"cuts(non-chain, k=1..n-1)={nonchain * (n - 1)}  "
          f"cuts(all posets)={len(ps) * (n - 1)}")

print()
print("C3 — double-count identity: sum over LABELLED posets of e(P) == n! * |NLP(n)|")
# Every (labelled poset P on [n], linear extension L) pair corresponds to exactly
# one (naturally labelled poset, relabelling) pair, so summing e(P) over all
# labelled posets must equal n! * |NLP(n)|.  The left side is computed from an
# independent enumeration (all 3^C(n,2)-style orientation filtering).
def all_labelled_posets(n):
    """Every partial order on [n], by filtering all reflexive-free relations
    for antisymmetry+transitivity. Independent of the incremental builder."""
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    from itertools import product
    for bits in product([0, 1], repeat=len(pairs)):
        rel = [0] * n
        for (i, j), b in zip(pairs, bits):
            if b:
                rel[j] |= 1 << i          # i < j
        # antisymmetry
        bad = False
        for j in range(n):
            for i in range(n):
                if rel[j] >> i & 1 and rel[i] >> j & 1:
                    bad = True
                    break
            if bad:
                break
        if bad:
            continue
        # transitivity
        for j in range(n):
            for i in range(n):
                if rel[j] >> i & 1 and rel[i] & ~rel[j]:
                    bad = True
                    break
            if bad:
                break
        if bad:
            continue
        yield tuple(rel)


import math
for n in range(1, 5):
    tot = 0
    cnt = 0
    for rel in all_labelled_posets(n):
        cnt += 1
        tot += len(brute_les(rel, n))
    check(f"n={n}: sum_P e(P) (over {cnt} labelled posets)",
          tot, math.factorial(n) * want[n])

print()
print("C4 — DP e(P) == brute-force e(P), every naturally labelled poset, n<=5")
bad = 0
for n in range(1, 6):
    for rel in naturally_labelled_posets(n):
        if le_dp(rel, n)[3] != len(brute_les(rel, n)):
            bad += 1
check("mismatching posets", bad, 0)

print()
print("C5 — DP Delta_1 == brute-force Delta_1, every poset and cut, n<=5")
bad = 0
for n in range(2, 6):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            if delta1(rel, n, k, dp) != brute_delta1(rel, n, k):
                bad += 1
check("mismatching (poset, cut)", bad, 0)

print()
print("C6 — DP p_xy == brute-force p_xy, every poset and incomparable pair, n<=5")
bad = 0
for n in range(2, 6):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        before, total = pair_probs(rel, n, dp)
        for (x, y) in incomparable_pairs(rel, n):
            if Fraction(before[x][y], total) != brute_pxy(rel, n, x, y):
                bad += 1
            if before[x][y] + before[y][x] != total:
                bad += 1
check("mismatching (poset, pair)", bad, 0)

print()
print("C7 — the two readings of sigma(A) AGREE on every prefix cut (finding, not a bug)")
disagree = 0
same = 0
for n in range(3, 6):
    for rel in naturally_labelled_posets(n):
        for k in range(1, n):
            if brute_delta1(rel, n, k) != brute_delta1_OTHER_SIGMA(rel, n, k):
                disagree += 1
            else:
                same += 1
print(f"  cuts where the two readings differ: {disagree}; agree: {same}")
check("sigma(A) ambiguity is immaterial on prefix cuts (0 disagreements)", disagree, 0)

print()
print("C7b — SENSITIVITY CONTROL: the pipeline must SEE a normalisation change")
# Phi (divide by |A|) vs Delta_1 (divide by min(|A|,|B|)) must differ exactly on
# the cuts with k > n/2 -- an exact predicted disagreement set, not just 'some'.
wrong_where = 0
mispredicted = 0
for n in range(3, 6):
    for rel in naturally_labelled_posets(n):
        for k in range(1, n):
            differs = brute_delta1(rel, n, k) != brute_delta1_MUTANT(rel, n, k)
            predicted = (k > n - k) and brute_delta1(rel, n, k) != 0
            if differs:
                wrong_where += 1
            if differs != predicted:
                mispredicted += 1
print(f"  cuts where Phi != Delta_1: {wrong_where}")
check("disagreement set is exactly {k > n/2, nonzero} (0 mispredictions)", mispredicted, 0)
check("the mutant IS visible (disagreements > 0)", wrong_where > 0, True)

print()
print("C8 — source sanity: Delta_1 <= 1 always, attained by the antichain at (n-1)/n")
bad = 0
for n in range(2, 7):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            if delta1(rel, n, k, dp) > 1:
                bad += 1
check("cuts with Delta_1 > 1", bad, 0)
for n in range(3, 8):
    anti = tuple([0] * n)
    dp = le_dp(anti, n)
    mx = max(delta1(anti, n, k, dp) for k in range(1, n))
    check(f"max_k Delta_1(antichain, n={n})", mx, Fraction(n - 1, n))

print()
if fails:
    print(f"SELFTEST FAILED: {len(fails)} check(s): {fails}")
    sys.exit(1)
print("SELFTEST PASSED — all controls green")
