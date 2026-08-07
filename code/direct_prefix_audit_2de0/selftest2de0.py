"""mg-2de0 SELFTEST — every verdict in this audit is shown GOING RED on a constructed input.

An audit that only ever prints OK is indistinguishable from an audit that checks nothing.
This file drills each check in both directions: a positive control that must pass and a
constructed negative that must FAIL. If any drill fails to fire, this script exits 1 and the
audit's OKs are not to be trusted.

Two-sided closure is the point. A check that cannot go red has no evidential value, and this
arc has repeatedly found instruments whose negative was unreachable.
"""

import sys
from fractions import Fraction as F
from itertools import permutations, combinations

from lib2de0 import (Poset, K_k, footrule, inversions, sum_K, k_range,
                     denom_exact, denom_claimed, named_posets, all_posets)

FAILS = []
N = 0


def drill(label, got, want):
    global N
    N += 1
    if got != want:
        FAILS.append(f"{label}: got {got!r}, want {want!r}")
        print(f"  RED-DRILL-FAILED {label}: got {got!r}, want {want!r}")
    else:
        print(f"  ok  {label}  ({got!r})")


print("=" * 78)
print("SELFTEST — two-sided closure on every verdict of the mg-2de0 audit")
print("=" * 78)

# ---------------------------------------------------------------- K_k, footrule
print()
print("S1  K_k and footrule on HAND-COMPUTED values (positive controls)")
# n=3, sigma = (1,0,2) i.e. element 1 at position 0
p = (1, 0, 2)
drill("K_1((1,0,2)) == 1  [A_1={0}, first position holds 1]", K_k(p, 1), 1)
drill("K_2((1,0,2)) == 0  [A_2={0,1}, first two positions hold {1,0}]", K_k(p, 2), 0)
drill("footrule((1,0,2)) == 2", footrule(p), 2)
drill("inversions((1,0,2)) == 1", inversions(p), 1)
drill("sum_K((1,0,2)) == 1 == footrule/2", sum_K(p), 1)
# identity
drill("K_k(identity) all zero", [K_k((0, 1, 2, 3), k) for k in (1, 2, 3)], [0, 0, 0])
drill("footrule(identity) == 0", footrule((0, 1, 2, 3)), 0)
# full reversal n=4: (3,2,1,0)
r = (3, 2, 1, 0)
drill("footrule(reversal n=4) == 8", footrule(r), 8)
drill("sum_K(reversal n=4) == 4 == 8/2", sum_K(r), 4)
drill("inversions(reversal n=4) == 6", inversions(r), 6)

print()
print("S2  LEMMA A GOING RED — the identity is checked against the WRONG constant, and")
print("    the check must fire. This is the drill for A1.1.")
red = sum(1 for q in permutations(range(5)) if F(sum_K(q)) != F(footrule(q)))   # no /2
drill("Lemma A vs footrule (NOT /2) fires on n=5", red > 0, True)
drill("  ... and fires on 119 of 120 (identity is the only fixed point, D=0)", red, 119)
green = sum(1 for q in permutations(range(5)) if F(sum_K(q)) != F(footrule(q), 2))
drill("Lemma A vs footrule/2 fires on NOTHING", green, 0)

print()
print("S3  the FACTOR-2 finding of A1.6 GOING RED both ways")
q = (2, 0, 1)
one = sum_K(q)
drill("one-sided sum == D/2 (true reading)", F(one) == F(footrule(q), 2), True)
drill("one-sided sum == D   (STATE.md:28's other reading) is FALSE here",
      F(one) == F(footrule(q)), False)
drill("2 * one-sided == D  (symmetric-difference reading) is TRUE",
      2 * one == footrule(q), True)

# ------------------------------------------------------------------- k_range
print()
print("S4  k_range clamping. At beta=0 the literal range [0, n] contains k=0 and k=n,")
print("    where min(k,n-k)=0 and Delta_1 does not exist. The clamp must exclude them.")
drill("k_range(6, 0) == [1..5]", k_range(6, F(0)), [1, 2, 3, 4, 5])
drill("k_range(8, 1/4) == [2..6]", k_range(8, F(1, 4)), [2, 3, 4, 5, 6])
drill("k_range(5, 1/3) == [2,3]", k_range(5, F(1, 3)), [2, 3])
drill("0 never in any k_range",
      any(0 in k_range(n, b) for n in range(2, 12)
          for b in (F(0), F(1, 4), F(1, 3))), False)
drill("n never in any k_range",
      any(n in k_range(n, b) for n in range(2, 12)
          for b in (F(0), F(1, 4), F(1, 3))), False)

# ------------------------------------------------------- denom, the I2 finding
print()
print("S5  the I2 FINDING GOING RED — A2.2 claims denom_exact < denom_claimed sometimes.")
print("    Drilled at the hand-computed cells, and drilled to NOT fire where it must not.")
drill("denom_exact(3,0) == 2 (hand: min(1,2)+min(2,1) = 1+1)", denom_exact(3, F(0)), 2)
drill("denom_claimed(3,0) == 9/4", denom_claimed(3, F(0)), F(9, 4))
drill("I2 FAILS at (3,0)", denom_exact(3, F(0)) < denom_claimed(3, F(0)), True)
drill("denom_exact(4,0) == 4 (hand: 1+2+1)", denom_exact(4, F(0)), 4)
drill("I2 HOLDS at (4,0) with equality", denom_exact(4, F(0)) == denom_claimed(4, F(0)), True)
drill("floor(n^2/4) identity at n=2..20",
      all(denom_exact(n, F(0)) == n * n // 4 for n in range(2, 21)), True)
odd_all = all(denom_exact(n, F(0)) < denom_claimed(n, F(0))
              for n in range(3, 30, 2))
even_none = any(denom_exact(n, F(0)) < denom_claimed(n, F(0))
                for n in range(2, 30, 2))
drill("at beta=0 I2 fails on EVERY odd n (3..29)", odd_all, True)
drill("at beta=0 I2 fails on NO even n (2..28)", even_none, False)

# --------------------------------------------------- the falsifier, both ways
print()
print("S6  THE FALSIFIER GOING RED AND GREEN. The witness of A2.4 is rebuilt from")
print("    scratch here (chain 0<2 plus a free point 1) and its every number is a")
print("    hand-computed positive control.")
W = Poset(3, [(0, 2)], "witness")
drill("witness has 3 linear extensions", len(W.linear_extensions()), 3)
drill("witness E[D] == 4/3", W.E_footrule(), F(4, 3))
drill("witness E[inv] == 2/3", W.E_inv(), F(2, 3))
drill("witness E[K_1] == 1/3", W.E_K(1), F(1, 3))
drill("witness E[K_2] == 1/3", W.E_K(2), F(1, 3))
drill("Lemma A holds on the witness", W.E_K(1) + W.E_K(2), W.E_footrule() / 2)
truth = min(W.delta_1_prefix(k) for k in (1, 2))
drill("witness truth min_k Delta_1 == 1/3", truth, F(1, 3))
drill("mg-00b9 OUTER bound 4E[inv]/n^2 == 8/27", 4 * W.E_inv() / 9, F(8, 27))
drill("OUTER BOUND IS FALSIFIED on the witness (1/3 > 8/27)",
      truth > 4 * W.E_inv() / 9, True)
drill("DG has ZERO slack on the witness (2E[inv] - E[D] == 0)",
      2 * W.E_inv() - W.E_footrule(), F(0))
drill("the REPAIRED bound is NOT falsified, and is TIGHT (== 1/3)",
      (W.E_footrule() / 2) / (9 // 4), F(1, 3))
print("    and the same detector must NOT fire on a poset where the bound holds:")
A4 = Poset(4, [], "antichain n=4")
t4 = min(A4.delta_1_prefix(k) for k in (1, 2, 3))
drill("antichain n=4 truth == 1/2", t4, F(1, 2))
drill("outer bound NOT falsified at antichain n=4",
      t4 > 4 * A4.E_inv() / 16, False)

# ------------------------------------------------------------ Phi, both ways
print()
print("S7  Phi_P and Phi* GOING RED. A3.2 claims Phi <= 1 for every cut; drilled with a")
print("    constructed value above 1 to show the comparison is live.")
drill("Phi(antichain n=4, A={0}) == 3/4", A4.phi(frozenset({0})), F(3, 4))
drill("Phi <= 1 does not fire on any real cut of antichain n=4",
      any(A4.phi(frozenset(S)) > 1 for size in (1, 2, 3)
          for S in combinations(range(4), size)), False)
drill("the SAME comparison fires on a constructed 5/4", F(5, 4) > 1, True)
drill("Phi* (antichain n=4) == 1/2", A4.phi_star(), F(1, 2))
drill("Phi* == min over prefixes at antichain n=4", A4.phi_star(), t4)
print("    and a poset where Phi* is STRICTLY below the prefix minimum must exist, or")
print("    A3.4's 'strictly smaller on 16 of 431' is unreachable:")
strict = [P for P in all_posets(4) if P.phi_star() < min(P.delta_1_prefix(k)
                                                        for k in range(1, 4))]
drill("at least one n=4 poset has Phi* < prefix minimum", len(strict) > 0, True)

# --------------------------------------------------- S7b: the mg-8311 E_leak repair
print()
print("S7b E_leak GOING RED ON THE mg-8311 DEFECT. E_leak must read the positions INDEXED")
print("    BY A, not the first |A| positions. The two agree on every prefix of e, so a")
print("    drill that only ever tests prefixes cannot see the difference -- which is")
print("    exactly why the defect survived this file for a whole audit. Every drill below")
print("    is on a NON-prefix cut.")
C2 = Poset(2, [(0, 1)], "chain n=2")
drill("the mg-8311 witness: E_leak(2-chain, A={1}) == 0, NOT 1",
      C2.E_leak(frozenset({1})), F(0))
print("    and the SAME cut read from the other side must agree, because conductance is a")
print("    property of the CUT and not of the SIDE (mg-76b2 Lemma 3.2). The old convention")
print("    gave 1 on one side and 0 on the other; that asymmetry is the defect's signature:")
drill("E_leak(2-chain, A={1}) == E_leak(2-chain, A^c={0})",
      C2.E_leak(frozenset({1})), C2.E_leak(frozenset({0})))
print("    the same symmetry across EVERY cut of EVERY poset to n=5, which is the property")
print("    the old convention violated on 457132 of 683656 (permutation, cut) pairs:")
asym = 0
pairs = 0
for P in named_posets(5) + all_posets(4):
    full = frozenset(range(P.n))
    for size in range(1, P.n):
        for S in combinations(range(P.n), size):
            A = frozenset(S)
            pairs += 1
            if P.E_leak(A) != P.E_leak(full - A):
                asym += 1
drill(f"E_leak is a function of the CUT on all {pairs} (poset, cut) pairs", asym, 0)
print("    and a CONSTRUCTED asymmetry must be detected, or the check above is vacuous:")
drill("the same comparison fires on a constructed 1 != 0", F(1) != F(0), True)
print("    the chain is the sharpest positive control: sigma = identity is the ONLY linear")
print("    extension, so sigma(A) = A and EVERY cut leaks exactly 0. Under the old")
print("    convention every non-prefix cut of a chain leaked a positive amount:")
C4 = Poset(4, [(0, 1), (1, 2), (2, 3)], "chain n=4")
drill("every cut of chain n=4 has E_leak == 0",
      [C4.E_leak(frozenset(S)) for size in (1, 2, 3)
       for S in combinations(range(4), size)], [F(0)] * 14)
drill("so Phi*(chain n=4) == 0", C4.phi_star(), F(0))
print("    [that last drill is a POSITIVE CONTROL ONLY and is NOT a detector: it passes")
print("     under the old convention too, because the chain's PREFIX cuts leak 0 either way")
print("     and Phi* is a minimum. Verified by running it against the old code. Recorded")
print("     here so no reader counts it as evidence the repair landed -- the detectors are")
print("     the four drills above it, all of which go red on the old E_leak.]")
print("    and the repair must NOT have disturbed the prefix agreement, which is what")
print("    K_k / E_K / delta_1_prefix and every Lemma A/B figure of this audit depend on:")
bad = 0
for P in named_posets(5) + all_posets(4):
    for k in range(1, P.n):
        if P.E_leak(frozenset(range(k))) != P.E_K(k):
            bad += 1
drill("E_leak(A_k) == E_K(k) on every prefix of every poset tested", bad, 0)

# ----------------------------------------------------------- delta, both ways
print()
print("S8  delta GOING RED. A5.2 claims delta >= 1/3 on width<=2; drilled against a")
print("    constructed sub-1/3 value, and drilled that chains give None.")
drill("delta(chain n=3) is None", Poset(3, [(0, 1), (1, 2)], "c3").delta(), None)
V = Poset(3, [(0, 1), (0, 2)], "V")
drill("delta(V) == 1/2 (hand: 2 LEs, the pair {1,2} splits 1/1 -> min = 1/2)",
      V.delta(), F(1, 2))
drill("delta >= 1/3 does not fire on V", V.delta() < F(1, 3), False)
# the TIGHT 3-element case: a 2-chain plus a free point. 3 LEs; BOTH incomparable
# pairs split 1/2, so delta = 1/3 exactly -- this is A5.2's tightest cell.
T = Poset(3, [(0, 1)], "2-chain+pt")
drill("2-chain+pt has 3 linear extensions", len(T.linear_extensions()), 3)
drill("delta(2-chain+pt) == 1/3 EXACTLY (A5.2's tightest cell)", T.delta(), F(1, 3))
drill("delta >= 1/3 does not fire on it (equality is not a violation)",
      T.delta() < F(1, 3), False)
drill("the SAME comparison fires on a constructed 1/4", F(1, 4) < F(1, 3), True)
drill("width(V) == 2", V.width(), 2)
drill("width(antichain n=4) == 4", A4.width(), 4)
drill("width(chain n=4) == 1", Poset(4, [(0, 1), (1, 2), (2, 3)], "c4").width(), 1)

# ------------------------------------------------- population sanity, measured
print()
print("S9  POPULATION SIZES, measured not recalled. Every count printed by the audit")
print("    scripts must match these, or a label is describing a different population")
print("    than the loop that produced it.")
drill("named_posets(7) == 34", len(named_posets(7)), 34)
drill("all_posets(4) == 40 LABELLED (not the 16 UNLABELLED)", len(all_posets(4)), 40)
drill("all_posets(5) == 357 LABELLED (not the 63 UNLABELLED)", len(all_posets(5)), 357)
drill("audit poset population == 431", 34 + 40 + 357, 431)
drill("sum of n! for n=2..7 == 5912 (NOT 5913)",
      sum(len(list(permutations(range(n)))) for n in range(2, 8)), 5912)
drill("every named poset has e=identity as a linear extension",
      all((0, 1, 2, 3, 4, 5, 6)[:P.n] in P.linear_extensions()
          for P in named_posets(7)), True)

print()
print("=" * 78)
print(f"SELFTEST: {N} drills, {len(FAILS)} failed")
for f in FAILS:
    print(f"  FAILED {f}")
print("=" * 78)
sys.exit(0 if not FAILS else 1)
