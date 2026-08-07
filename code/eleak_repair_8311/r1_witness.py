"""mg-8311 R1 — THE WITNESS, BY HAND, BEFORE ANYTHING IS REPAIRED.

The ticket's instruction is explicit: reproduce the 2-chain witness first, and if it does
not reproduce, STOP and report, because then the finding is wrong and that is the result.

It reproduces. This script is that reproduction, written out at full grain -- every linear
extension printed, every set printed, so a reader can check it without running anything.

It then establishes the two facts that make the ruling a two-way choice rather than a
three-way one, and that make the convention's Phi a non-conductance:

  R1.2  |A \\ sigma(A)| = |A \\ sigma^{-1}(A)| for every (A, sigma) -- so the two natural
        readings of sigma(A) are ONE number, and set(p[:|A|]) is neither of them.
  R1.3  |A \\ sigma(A)| = |A^c \\ sigma(A^c)| for every (A, sigma) -- mg-76b2's Lemma 3.2,
        re-derived here on my own permutation enumeration -- and the SAME test against the
        convention, which FAILS.

R1.3 is the substance of the ruling. Conductance is a property of a CUT. A quantity that
gives different answers on the two sides of the same cut is not a conductance, whatever it
is called.

OPERATOR SCOPE: leak counts and one matrix quadratic form. No eigenvalue. Transport axis.
"""

import sys
from fractions import Fraction as F
from itertools import permutations, combinations

from lib8311 import (P8311, leak_def, leak_inv, leak_conv, Tally,
                     all_posets_8311)

T = Tally()

print("=" * 78)
print("R1 — the 2-chain witness, reproduced BEFORE any repair, and the two symmetries")
print("=" * 78)

# ---------------------------------------------------------------------------
print()
print("R1.1  THE WITNESS. 2-chain 0 < 1, cut A = {1}. Every linear extension printed.")
C2 = P8311(2, [(0, 1)], "chain n=2")
les = C2.linear_extensions()
print(f"       L(P) = {list(les)}   (|L(P)| = {len(les)})")
A = frozenset({1})
print(f"       A = {set(A)}, |A| = {len(A)}")
print()
print(f"       {'sigma':>10s} {'sigma(A)':>12s} {'|A\\sig(A)|':>11s} "
      f"{'first |A| pos':>14s} {'lib2de0 gives':>14s}")
for p in les:
    img = set(p[i] for i in A)
    pref = set(p[:len(A)])
    print(f"       {str(p):>10s} {str(img):>12s} {leak_def(A, p):>11d} "
          f"{str(pref):>14s} {leak_conv(A, p):>14d}")

e_def = C2.E_leak(A, "def")
e_conv = C2.E_leak(A, "conv")
print()
print(f"       E|A\\sigma(A)|  by the DEFINITION  = {e_def}")
print(f"       E  as lib2de0.E_leak COMPUTES it  = {e_conv}")
T.report("the witness reproduces: definition gives 0", 0 if e_def == 0 else 1, 1,
         "exact Fraction equality against 0",
         "the 2-chain 0<1, its single linear extension, the single cut A={1}")
T.report("the witness reproduces: convention gives 1", 0 if e_conv == 1 else 1, 1,
         "exact Fraction equality against 1",
         "same")
T.report("and they DIFFER, so the ticket's finding is REAL",
         0 if e_def != e_conv else 1, 1,
         "exact Fraction inequality",
         "same")
print("       => the ticket said to STOP and report if this did not reproduce.")
print("          It reproduced. The finding is real and the audit proceeds.")
print()
print("       and the SAME cut read from the other side, which is R1.3's point in one line:")
Ac = frozenset({0})
print(f"       A  = {set(A)}:  definition {C2.E_leak(A, 'def')}   convention {C2.E_leak(A, 'conv')}")
print(f"       A^c= {set(Ac)}: definition {C2.E_leak(Ac, 'def')}   convention {C2.E_leak(Ac, 'conv')}")
print("       => the DEFINITION agrees across the cut (0 = 0). The CONVENTION does not")
print("          (1 != 0). Held over to R1.3 and measured at population scale there.")

# ---------------------------------------------------------------------------
print()
print("R1.2  THE RULING IS A TWO-WAY CHOICE, NOT A THREE-WAY ONE.")
print("      sigma(A) has two natural readings -- image of a POSITION set {p[i] : i in A},")
print("      and image of an ELEMENT set, i.e. sigma^{-1} in this indexing. They give the")
print("      SAME COUNT for every (A, sigma), because |A n sigma(A)| = |sigma^{-1}(A) n A|")
print("      (apply the bijection sigma^{-1} to both members of the intersection).")
print("      So set(p[:|A|]) is not 'the other reading' -- it is neither reading.")
bad = tot = 0
for n in range(1, 8):
    for p in permutations(range(n)):
        for size in range(0, n + 1):
            for S in combinations(range(n), size):
                A = frozenset(S)
                tot += 1
                if leak_def(A, p) != leak_inv(A, p):
                    bad += 1
T.report("|A\\sigma(A)| == |A\\sigma^{-1}(A)|", bad, tot,
         "per-(permutation, subset), integer equality",
         f"ALL permutations of {{0..n-1}} for n=1..7 (5913 permutations) x ALL 2^n subsets "
         f"INCLUDING the empty set and the full set = {tot} (permutation, subset) pairs")
print("       => the two readings are ONE number. Nothing below has to choose between them.")

# ---------------------------------------------------------------------------
print()
print("R1.3  THE RULING. Lemma 3.2: |A\\sigma(A)| = |A^c\\sigma(A^c)|, so Phi_P is a")
print("      function of the CUT and not of the SIDE. Re-derived here on my own")
print("      enumeration -- and then the IDENTICAL test run against the convention.")
for which in ("def", "conv"):
    bad = tot = 0
    first = None
    for n in range(2, 8):
        for p in permutations(range(n)):
            for size in range(1, n):
                for S in combinations(range(n), size):
                    A = frozenset(S)
                    Ac = frozenset(range(n)) - A
                    tot += 1
                    f = {"def": leak_def, "conv": leak_conv}[which]
                    if f(A, p) != f(Ac, p):
                        bad += 1
                        if first is None:
                            first = (n, p, set(A), f(A, p), set(Ac), f(Ac, p))
    label = ("DEFINITION: |A\\sig(A)| == |A^c\\sig(A^c)|" if which == "def"
             else "CONVENTION: same test, EXPECTED TO FAIL")
    T.report(label, bad, tot,
             "per-(permutation, proper cut), integer equality across the cut",
             f"ALL permutations for n=2..7 x ALL 2^n-2 proper cuts = {tot} pairs",
             fatal=(which == "def"))
    if first is not None:
        n, p, a, va, ac, vac = first
        print(f"       first failure: n={n}, sigma={p}, A={a} -> {va}, "
              f"A^c={ac} -> {vac}")
print()
print("       => THE RULING. The convention is not a function of the cut. Conductance IS a")
print("          function of the cut -- lib2de0.py's own docstring line 17 calls Phi_P 'the")
print("          same quantity, read as a CONDUCTANCE, minimised over ALL cuts A'. A")
print("          quantity that disagrees with itself across a cut cannot be minimised over")
print("          cuts in the sense a Cheeger argument needs, because 'the cut' does not")
print("          determine its value. THE DEFINITION WINS, and it wins on this, not on")
print("          being the definition.")

# ---------------------------------------------------------------------------
print()
print("R1.4  WHERE THE CONVENTION IS *NOT* WRONG, stated at the same grain, because a")
print("      repair that cannot say what it preserves is not assessable. A_k = {0..k-1} IS")
print("      the set of the first k positions, so the two agree on PREFIXES OF e:")
bad = tot = 0
for n in range(2, 8):
    for p in permutations(range(n)):
        for k in range(1, n):
            A = frozenset(range(k))
            tot += 1
            if leak_def(A, p) != leak_conv(A, p):
                bad += 1
T.report("def == conv on every PREFIX A_k = {0..k-1}", bad, tot,
         "per-(permutation, prefix), integer equality",
         f"ALL permutations for n=2..7 x prefixes k=1..n-1 = {tot} pairs")
print("       => so lib2de0's K_k, E_K and delta_1_prefix are UNAFFECTED, and every")
print("          Delta_1(A_k) figure mg-2de0 published stands untouched. This is NARROW:")
print("          prefixes of e ONLY. It does NOT extend to suffixes, to general intervals,")
print("          or to prefixes of sigma -- and the very next line shows it failing on the")
print("          suffix of the same size:")
bad = tot = 0
for n in range(2, 8):
    for p in permutations(range(n)):
        for k in range(1, n):
            A = frozenset(range(n - k, n))
            tot += 1
            if leak_def(A, p) != leak_conv(A, p):
                bad += 1
T.report("def == conv on SUFFIXES -- EXPECTED TO FAIL, this is the guard on R1.4",
         bad, tot, "per-(permutation, suffix), integer equality",
         f"ALL permutations for n=2..7 x suffixes of size k=1..n-1 = {tot} pairs",
         fatal=False)
print(f"       => {bad} of {tot}. The agreement is exactly as wide as 'prefix of e' and no")
print("          wider. Filed in advance as PREDICTIONS.md P14, the slip I bet 35% on.")

print()
print("=" * 78)
print(f"R1 TOTAL BAD: {T.bad}")
print("=" * 78)
sys.exit(0 if T.bad == 0 else 1)
