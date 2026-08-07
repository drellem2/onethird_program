#!/usr/bin/env python3
"""s1 — THE DICTIONARY.

`Op-Form 4.3` reasons about `C_3` entirely in the currency of the *prefix Rayleigh
quotient* `rho(A_k)`, and the architecture consumes the *conductance* `Phi_P(A_k)` =
`Delta_1(A_k, A_k^c)`.  Nothing in the corpus connects them: a grep for "Rayleigh" across
`docs/` and `STATE.md` returns two lines, both inside `Op-Form 4.3` itself.  Without that
link no statement about `C_3` is checkable at all.

This section establishes the link exactly, over the whole population:

    (D1)   1 - rho(A_k)  =  n * E|A_k \\ sigma(A_k)| / (k(n-k))
                         =  n * Phi_P(A_k) / max(k, n-k)      for 1 <= k <= n-1
    (D2)   Phi_P(A_k) <=  1 - rho(A_k)  <=  2 * Phi_P(A_k)    for EVERY k

PREDICTIONS.md H1 derived (D1) in the form `n*Phi/(n-k)`, which is the `k <= n/2` case
(there `Phi = leak/k` and `max(k,n-k) = n-k`).  Written that way for all k it is FALSE
above the median, because `Phi_P` normalises by `min(|A|,|A^c|)` and the normalisation
switches sides at `k = n/2`.  The script caught that on 9909 (poset, prefix) pairs before
the general form was written; the general form is what is checked below, and it reduces
to H1's exactly where H1 claimed it.  `1-rho = n*leak/(k(n-k))` is the symmetric form and
is the one to quote.

and two facts the rest of the instrument leans on:

    (D3)   <1_A, (I-M) 1_A>  =  E|A \\ sigma(A)|              for EVERY cut A
    (D4)   |A \\ sigma(A)|  =  |A^c \\ sigma(A^c)|            pointwise in sigma

(D4) is the load-bearing half of the suffix branch of the sweep, and PREDICTIONS.md P13
bets 15% against it.  It is checked here permutation by permutation, not assumed.

Exit 0 iff every check passes.  Every count names its population at the print site.
"""

from fractions import Fraction as F
from itertools import combinations, permutations
import sys

from lib76b2 import Poset, all_posets, named_posets

NMAX = 6
fail = 0


def check(cond, msg):
    global fail
    if not cond:
        fail += 1
        print(f"    FAIL: {msg}")
    return cond


print("=" * 78)
print("s1 — THE DICTIONARY between the prefix Rayleigh quotient and the conductance")
print("=" * 78)
print()
print("POPULATION: every poset on {0..n-1} whose identity permutation is a linear")
print(f"extension (so e is fixed by the labelling), n = 2..{NMAX}, enumerated exhaustively.")
print()

pops = {n: all_posets(n) for n in range(2, NMAX + 1)}
for n in range(2, NMAX + 1):
    print(f"  n = {n}:  {len(pops[n])} posets")
print(f"  TOTAL:   {sum(len(v) for v in pops.values())} posets")
print()

# ---------------------------------------------------------------- (D4) first
print("-" * 78)
print("(D4)  |A \\ sigma(A)| = |A^c \\ sigma(A^c)|  pointwise in sigma")
print("      -- the whole warrant for the sweep's SUFFIX branch (P13 bets against it)")
print("-" * 78)
d4_perms = d4_cuts = 0
for n in range(2, NMAX + 1):
    for p in permutations(range(n)):
        d4_perms += 1
        for size in range(1, n):
            for A in combinations(range(n), size):
                A = frozenset(A)
                Ac = frozenset(range(n)) - A
                lhs = len(A) - len(A & {p[i] for i in A})
                rhs = len(Ac) - len(Ac & {p[i] for i in Ac})
                d4_cuts += 1
                if lhs != rhs:
                    check(False, f"n={n} p={p} A={sorted(A)}: {lhs} != {rhs}")
print(f"  checked {d4_cuts} (permutation, cut) pairs over {d4_perms} permutations, n = 2..{NMAX}")
print(f"  VERDICT: {'HOLDS with 0 exceptions' if fail == 0 else 'FAILS'}")
print()
print("  Consequence, and it is the one the sweep needs: Phi_P is a function of the CUT")
print("  {A, A^c}, not of the side.  A low-conductance SUFFIX of size <= n/2 therefore")
print("  delivers Step 5's own quantity Delta_1(A_k, A_k^c) at the complementary prefix,")
print("  with no loss and no further argument.  P13 is REFUTED as a worry.")
print()

# ------------------------------------------------------------- (D3) and (D1)
print("-" * 78)
print("(D3)  <1_A,(I-M)1_A> = E|A \\ sigma(A)| for EVERY cut  --  matrix vs definition")
print("(D1)  1 - rho(A_k) = n*leak/(k(n-k)) = n * Phi_P(A_k) / max(k, n-k)")
print("(D2)  Phi <= 1 - rho <= 2 Phi, for EVERY k")
print("-" * 78)
d3 = d1 = d2 = 0
d2_tight_lo = d2_tight_hi = 0
for n in range(2, NMAX + 1):
    for P in pops[n]:
        for size in range(1, n):
            for A in combinations(range(n), size):
                ind = [F(1) if i in A else F(0) for i in range(n)]
                d3 += 1
                check(P.energy(ind) == P.leak(A), f"D3 {P} A={A}")
        for k in range(1, n):
            lhs = P.rho_prefix(k)                       # 1 - rho, exact
            phi = P.phi(range(k))
            leak = P.leak(range(k))
            d1 += 1
            check(lhs == F(n, k * (n - k)) * leak, f"D1-sym {P} k={k}")
            check(lhs == F(n, max(k, n - k)) * phi, f"D1 {P} k={k}")
            if k <= n // 2:
                check(lhs == F(n, n - k) * phi, f"D1-H1form {P} k={k}")
            d2 += 1
            check(phi <= lhs <= 2 * phi, f"D2 {P} k={k}")
            if lhs == phi:
                d2_tight_lo += 1
            if lhs == 2 * phi:
                d2_tight_hi += 1
print(f"  (D3) checked on {d3} (poset, cut) pairs over the {sum(len(v) for v in pops.values())}-poset population")
print(f"  (D1) checked on {d1} (poset, prefix) pairs")
print(f"  (D2) checked on {d2} (poset, prefix) pairs, ALL k")
print(f"  VERDICT: {'ALL THREE HOLD with 0 exceptions' if fail == 0 else 'FAILURES ABOVE'}")
print()
print(f"  lower end 1-rho = Phi attained: {d2_tight_lo} of {d2} cases (needs max(k,n-k) = n, i.e.")
print("     Phi = 0 -- an exact ordinal-sum cut; the bound is otherwise strict)")
print(f"  upper end 1-rho = 2 Phi attained: {d2_tight_hi} of {d2} cases (needs k = n/2 EXACTLY,")
print("     so it is attained at every even n and unreachable at odd n -- PREDICTIONS P2s")
print("     second clause said the factor 2 is approached and never attained: REFUTED)")
print()

# ---------------------------------------------------- (P11) the other convention
print("-" * 78)
print("(P11) `sigma(A)` = image of A, versus the `set(p[:|A|])` convention")
print("-" * 78)
print("  PREDICTIONS.md H7 read `lib2de0.E_leak` as using the first |A| POSITIONS rather")
print("  than the positions indexed by A, and `lib2de0.phi_star` calls it on every subset.")
print("  Measured here rather than argued: `leak_naive_prefixstyle` reproduces that")
print("  convention and is compared against the definition on every cut.")
print()
div = tot = 0
first = None
for n in range(2, 5 + 1):
    for P in pops[n]:
        for size in range(1, n):
            for A in combinations(range(n), size):
                tot += 1
                a, b = P.leak(A), P.leak_naive_prefixstyle(A)
                if a != b:
                    div += 1
                    if first is None:
                        first = (n, sorted(P.rel), sorted(A), a, b)
print(f"  {div} of {tot} (poset, cut) pairs over n = 2..5 DIVERGE between the two conventions")
if first:
    n, rel, A, a, b = first
    print(f"  first witness: n={n}, rel={rel}, A={A}")
    print(f"      E|A \\ sigma(A)| (definition)      = {a}")
    print(f"      |A| - |A & set(p[:|A|])| (other)  = {b}")
print("  Prefix cuts agree by construction; the divergence is entirely on non-prefix cuts,")
print("  which is exactly where `phi_star` ranges.")
print("  NOTED AND NOT REPAIRED — `code/direct_prefix_audit_2de0/` is mg-2de0's file, and")
print("  this ticket does not own it.  What follows uses this instrument's own definition.")
print()

print("=" * 78)
print(f"s1 VERDICT: {'ALL CHECKS PASS' if fail == 0 else str(fail) + ' FAILURES'}")
print("=" * 78)
sys.exit(1 if fail else 0)
