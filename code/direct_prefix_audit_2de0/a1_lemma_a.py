"""mg-2de0 A1 — AUDIT OF LEMMA A, derived from the definitions, not from mg-00b9's derivation.

LEMMA A (mg-00b9, as restated in mg-2de0's body):
    sum_{k=1}^{n-1} K_k(sigma) = D(sigma)/2,   D = footrule.

MY DERIVATION (independent; the author's reasoning was not consulted for correctness):
    Fix x. K_k counts x exactly when rank_e(x) <= k < pos_sigma(x) (1-indexed), i.e. when
    k lies in the integer interval [rank_e(x), pos_sigma(x) - 1]. That interval has
    (pos - 1) - rank + 1 = pos - rank integers when pos > rank, and none otherwise, and it
    is automatically inside [1, n-1]. Summing over x and exchanging the order of summation:
        sum_k K_k(sigma) = sum_x (pos_sigma(x) - rank_e(x))^+ .
    Both pos_sigma and rank_e are bijections onto the same n positions, so
        sum_x (pos - rank) = 0  =>  sum_x (pos-rank)^+ = sum_x (pos-rank)^- ,
    and the two halves add to sum_x |pos - rank| = D(sigma). Hence each is D(sigma)/2.  QED

TWO STRUCTURAL CONSEQUENCES OF THAT DERIVATION, which the statement alone does not show:
    (i)  it is a PER-SIGMA identity, not an identity in expectation;
    (ii) it is POSET-FREE. P appears nowhere. The poset enters only when sigma is restricted
         to L(P) to take an expectation. So the strongest population for the check is ALL
         permutations, and the poset population is a redundant sub-check kept as a control.

This script checks the identity, and separately checks the INTERMEDIATE step
sum_k K_k = sum_x (pos-rank)^+, so a failure can be localised.

OPERATOR SCOPE: footrule / K_k. Transport axis. Not Delta_AT, not A(P), not Hodge.
"""

import sys
from fractions import Fraction as F
from itertools import permutations

from lib2de0 import K_k, footrule, sum_K, named_posets, all_posets

BAD = 0


def report(label, bad, total, grain, population):
    global BAD
    BAD += bad
    flag = "OK  " if bad == 0 else "BAD "
    print(f"  {flag} {label}: {bad} bad / {total} checked")
    print(f"       population: {population}")
    print(f"       grain:      {grain}")


print("=" * 78)
print("A1 — LEMMA A:  sum_{k=1}^{n-1} K_k(sigma) = D(sigma)/2")
print("     derived independently from the definitions (see module docstring)")
print("=" * 78)

# ---------------------------------------------------------------------------
print()
print("A1.1  the identity, over ALL permutations (the widest population it has)")
bad = tot = 0
per_n = []
for n in range(2, 8):
    nbad = ntot = 0
    for p in permutations(range(n)):
        ntot += 1
        if F(sum_K(p)) != F(footrule(p), 2):
            nbad += 1
    per_n.append((n, ntot, nbad))
    bad += nbad
    tot += ntot
for (n, ntot, nbad) in per_n:
    print(f"       n={n}: {ntot:5d} permutations, {nbad} exceptions")
report("Lemma A over all permutations", bad, tot,
       "per-permutation, exact Fraction equality",
       f"all n! permutations for n=2..7 ({tot} permutations)")

# ---------------------------------------------------------------------------
print()
print("A1.2  the INTERMEDIATE step:  sum_k K_k = sum_x (pos - rank)^+")
print("      (localises a failure: this is the counting exchange, not the cancellation)")
bad = tot = 0
for n in range(2, 8):
    for p in permutations(range(n)):
        tot += 1
        pos = {x: i for i, x in enumerate(p)}
        pos_part = sum(max(0, pos[x] - x) for x in range(n))
        if sum_K(p) != pos_part:
            bad += 1
report("counting exchange", bad, tot,
       "per-permutation, integer equality",
       f"all n! permutations for n=2..7 ({tot} permutations)")

print()
print("A1.3  the CANCELLATION step:  sum_x (pos - rank) = 0")
bad = tot = 0
for n in range(2, 8):
    for p in permutations(range(n)):
        tot += 1
        pos = {x: i for i, x in enumerate(p)}
        if sum(pos[x] - x for x in range(n)) != 0:
            bad += 1
report("cancellation", bad, tot,
       "per-permutation, integer equality",
       f"all n! permutations for n=2..7 ({tot} permutations)")

# ---------------------------------------------------------------------------
print()
print("A1.4  CONTROL — the same identity over linear extensions of real posets.")
print("      Redundant given A1.1 (Lemma A is poset-free); kept because the arc's")
print("      statement of it is about L(P) and a reader will want to see L(P).")
bad = tot = 0
pops = named_posets(7) + all_posets(4) + all_posets(5)
for P in pops:
    for p in P.linear_extensions():
        tot += 1
        if F(sum_K(p)) != F(footrule(p), 2):
            bad += 1
report("Lemma A over linear extensions", bad, tot,
       "per-(poset, linear extension), exact Fraction equality",
       f"{len(pops)} posets = 34 named (n=2..7) + all 40 LABELLED posets on n=4 + all "
       f"357 LABELLED posets on n=5 (labelled-with-e-as-identity, NOT the 16 and 63 "
       f"UNLABELLED posets on 4 and 5 elements -- a different grain), "
       f"{tot} (poset, linear extension) pairs")

# ---------------------------------------------------------------------------
print()
print("A1.5  the EXPECTATION form actually used by Lemma B:  sum_k E[K_k] = E[D]/2")
bad = tot = 0
for P in pops:
    tot += 1
    lhs = sum(P.E_K(k) for k in range(1, P.n))
    if lhs != P.E_footrule() / 2:
        bad += 1
        print(f"       BAD {P.name}: {lhs} != {P.E_footrule()/2}")
report("Lemma A in expectation", bad, tot,
       "per-poset, exact Fraction equality over L(P)",
       f"{len(pops)} posets as in A1.4")

# ---------------------------------------------------------------------------
print()
print("A1.6  THE FACTOR OF 2 — which normalisation is 'Sigma prefix-violations'?")
print("      STATE.md:28 records `Sigma prefix-violations = footrule`. Lemma A says the")
print("      sum of K_k is footrule/2. The two are reconciled only by a normalisation")
print("      STATE.md:28 does not state. Both candidate readings, measured:")
bad = tot = 0
for n in range(2, 7):
    for p in permutations(range(n)):
        tot += 1
        one_sided = sum_K(p)                       # sum_k |A_k \ sigma(A_k)|
        sym_diff = 2 * one_sided                   # sum_k |A_k symmetric-difference sigma(A_k)|
        D = footrule(p)
        # reading 1: prefix-violations at k = |A_k \ sigma(A_k)|  -> claims = D, is D/2
        # reading 2: prefix-violations at k = |A_k D sigma(A_k)|  -> claims = D, is D
        if not (F(one_sided) == F(D, 2) and sym_diff == D):
            bad += 1
report("both readings simultaneously", bad, tot,
       "per-permutation; reading 1 = D/2 AND reading 2 = D, both exact",
       f"all n! permutations for n=2..6 ({tot} permutations)")
print("       => STATE.md:28 is TRUE under the symmetric-difference reading and FALSE")
print("          by a factor of 2 under the one-sided reading K_k = |A_k \\ sigma(A_k)|,")
print("          which is the reading the corpus pins at")
print("          docs/OneThird-lambda-std-Operative-Form.md:84 and its audit :227.")
print("       => also verified here: |A_k \\ sigma(A_k)| = |sigma(A_k) \\ A_k| always,")
print("          which is WHY the two readings differ by exactly 2 and not by something")
print("          sigma-dependent:")
bad = tot = 0
for n in range(2, 7):
    for p in permutations(range(n)):
        for k in range(1, n):
            tot += 1
            A = set(range(k))
            S = set(p[:k])
            if len(A - S) != len(S - A):
                bad += 1
report("|A_k \\ sigma(A_k)| = |sigma(A_k) \\ A_k|", bad, tot,
       "per-(permutation, k), integer equality",
       f"all (permutation, k) pairs for n=2..6 ({tot} pairs)")

# ---------------------------------------------------------------------------
print()
print("A1.7  mg-00b9's OWN hand-check, reproduced (its n=4 antichain), plus the")
print("      DIFFERENT cases mg-2de0 asked for. Antichain closed forms re-derived by")
print("      hand independently: E[K_k] = k(n-k)/n, Delta_1(A_k) = max(k,n-k)/n.")
hdr = f"       {'poset':26s} {'sum_k E[K_k]':>14s} {'E[D]/2':>14s} {'equal':>6s}"
print(hdr)
bad = tot = 0
for P in named_posets(7):
    tot += 1
    lhs = sum(P.E_K(k) for k in range(1, P.n))
    rhs = P.E_footrule() / 2
    ok = lhs == rhs
    if not ok:
        bad += 1
    if P.n <= 5 or "antichain" in P.name:
        print(f"       {P.name:26s} {str(lhs):>14s} {str(rhs):>14s} {str(ok):>6s}")
report("named families, expectation form", bad, tot,
       "per-poset, exact Fraction equality",
       f"{tot} named posets, n=2..7 (antichain, chain, chain+pt, ordinal sum, two "
       f"chains, N-poset; the N-poset family starts at n=4, which is why the count is "
       f"{tot} and not 6*6)")
print("       mg-00b9's own check was n=4 antichain: 3/4 + 1 + 3/4 = 5/2 = E_unif[D]/2.")
print("       Reproduced above and EXTENDED to 33 further named posets and 5912 permutations.")
print("       The n=4 antichain is one cell of a 5912-cell population; on its own it could")
print("       not have distinguished Lemma A from the factor-2 variant of A1.6, because")
print("       it is a single value and both readings are consistent with a single value")
print("       only if you already know which normalisation you meant.")

# ---------------------------------------------------------------------------
print()
print("=" * 78)
print(f"A1 TOTAL BAD: {BAD}")
print("=" * 78)
sys.exit(0 if BAD == 0 else 1)
