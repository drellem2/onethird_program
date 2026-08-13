"""s0 — CONTROLS ON lib99f4, BEFORE ANY ARM THAT PRODUCES A FINDING.

Five external or independent anchors and four planted defects.  The planted defects are the
half that matters: a library that agrees with A001035 can still be wrong about the object this
directory is actually about, which is the extension SET rather than its size.

ONE PLANT CAME BACK INERT AND IS PRINTED RATHER THAN SWAPPED OUT — see s0.9.
"""

import math
import sys
from fractions import Fraction
from itertools import combinations, permutations

import lib99f4 as L

R = L.Report()

A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}
NMAX = 5

R.banner("s0.1  THE EXTERNAL ANCHOR — labelled poset counts against OEIS A001035")
POSETS = {}
for n in range(1, NMAX + 1):
    POSETS[n] = L.all_posets(n)
    R.verdict(len(POSETS[n]) == A001035[n],
              "n = %d: %d labelled posets" % (n, len(POSETS[n])),
              "A001035 says %d" % A001035[n])
R.note("The enumerator is brute force over 3^C(n,2) orientations plus a transitivity filter.")
R.note("It shares no idea with the minimal-element recursions used elsewhere in code/, so this")
R.note("is a SECOND ROUTE to A001035 rather than the estate's route run again.")

R.banner("s0.2  A SECOND ROUTE TO e(P) — enumeration against a down-set DP that never enumerates")
bad = 0
for n in range(1, NMAX + 1):
    for rel in POSETS[n]:
        if len(L.linear_extensions(rel, n)) != L.count_extensions_dp(rel, n):
            bad += 1
R.verdict(bad == 0, "e(P) agrees on all %d posets, n = 1..%d"
          % (sum(len(POSETS[n]) for n in POSETS), NMAX), "%d disagreements" % bad)

R.banner("s0.3  THE SET AND THE POSET ARE INVERSE — P = intersection of L(P), on every poset")
bad = 0
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        if L.relation_from(L.linear_extensions(rel, n), n) != rel:
            bad += 1
R.verdict(bad == 0, "relation_from(linear_extensions(P)) == P at n = 2..%d" % NMAX,
          "%d failures" % bad)
R.note("This is the control that makes s1.1's BIJECTION a measurement rather than a definition:")
R.note("without it, `LL_n -> posets` would not be well defined and the census would be counting")
R.note("something else.")

R.banner("s0.4  L* IS A LINEAR EXTENSION WHEN IT EXISTS — the defining property, checked")
bad = has = 0
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        LE = L.linear_extensions(rel, n)
        star = L.lstar(L.pair_marginals(LE, n), n)
        if star is None:
            continue
        has += 1
        if star not in set(LE):
            bad += 1
R.verdict(bad == 0, "L* in L(P) at all %d posets where L* exists, n = 2..%d" % (has, NMAX),
          "%d failures" % bad)
R.note("ALSO THE PROOF, in one line, and it is why s1.4's T2a row reads res = 1: if x < y in P")
R.note("then pi_xy = 1 > 1/2, so x beats y in the majority tournament and precedes y in L*.")
R.note("So L* extends P whenever it is a total order at all.  The run is the vacuity guard.")

R.banner("s0.5  delta AGAINST HAND VALUES")
n = 3
chain = frozenset({(0, 1), (1, 2), (0, 2)})
anti = frozenset()
vee = frozenset({(0, 1), (0, 2)})
for rel, want, name in [(chain, Fraction(0), "the 3-chain (max over the EMPTY set)"),
                        (anti, Fraction(1, 2), "the 3-antichain"),
                        (vee, Fraction(1, 2), "0 < 1, 0 < 2")]:
    got = L.delta(rel, L.linear_extensions(rel, n), n)
    R.verdict(got == want, "delta = %s at %s" % (got, name), "expected %s" % want)

R.banner("s0.6  THE CROSSOVER BINARY SEARCH REPRODUCES compression2's OWN MEASURED NUMBER")
NOTE_CONST = 1.0 - 1.0 / (24.0 * math.log(2.0))     # compression2.tex (6), exactly
got = L.crossover(NOTE_CONST)
R.verdict(got == 16777063,
          "crossover(c = 1 - 1/(24 ln 2) = %.7f) = %s" % (NOTE_CONST, got),
          "mg-0fc6 a1.6 measured 16,777,063 by its own binary search")
R.note("THE EXTERNAL ANCHOR FOR s2.  mg-0fc6's figure was produced by different code in a")
R.note("different directory against the same definition; reproducing it to the UNIT is what")
R.note("licenses s2 to quote crossover numbers for constants nobody has measured yet.")
R.line()
R.note("AND THE ANCHOR WENT RED ON ITS FIRST RUN, WHICH IS REPORTED RATHER THAN QUIETLY FIXED.")
R.note("This control was first written against `0.9399`, the constant as it is PRINTED in")
R.note("mg-0fc6's own table header (`OneThird-Compression2-Scope-mg-0fc6.md:113`).  The arm")
R.note("computes `NOTE_CONST = 1 - 1/(24 ln 2)` = 0.9398877, and the header is that rounded to")
R.note("four places.  The two do not give the same crossover:")
rounded = L.crossover(0.9399)
R.verdict(rounded == 16834249,
          "the PRINTED constant 0.9399 gives n* = %s" % rounded,
          "%+d against the published 16,777,063 — %.2f%%"
          % (rounded - 16777063, 100.0 * (rounded - 16777063) / 16777063))
R.note("NOT AN ERROR IN mg-0fc6's MEASUREMENT — its number is correct for the constant its code")
R.note("uses, and the row header is a rounding in prose.  It is recorded because 0.34% of an")
R.note("order-10^7 crossover is 57,186 and because THE SENSITIVITY IS THE POINT s2 makes: the")
R.note("elasticity `d(ln n*)/dc = 1/(1-c)^2` is 277 at this constant, so four printed digits of")
R.note("`c` do not pin `n*` to four digits.  A ticket that asks 'does it bite below 10^7?' is")
R.note("asking a question whose answer moves under rounding, and that is a fact about the")
R.note("FAMILY rather than about any one paper.")
R.verdict(L.crossover(1.0) is None, "crossover(c = 1.0) is None", "no c >= 1 ever bites")
R.verdict(L.crossover(0.0) == 3, "crossover(c = 0.0) = 3", "a free bound bites at the first n")

R.banner("s0.7  PLANT 1 — an enumerator that drops the antisymmetry of the strict order")
saved = L.is_transitive
try:
    L.is_transitive = lambda rel, n: True          # keep every orientation
    got = len(L.all_posets(3))
    R.verdict(got != A001035[3], "planted: transitivity filter removed -> %d at n = 3" % got,
              "A001035 says 19; the control CATCHES it")
finally:
    L.is_transitive = saved
R.verdict(len(L.all_posets(3)) == 19, "and the library is restored", "19 again")

R.banner("s0.8  PLANT 2 — a BK graph that counts every pair, not the adjacent transpositions")
S = L.linear_extensions(frozenset(), 3)            # the antichain: all 6 permutations
true_edges = L.bk_edges(S)
all_pairs = len(S) * (len(S) - 1) // 2
R.verdict(true_edges == 6 and all_pairs == 15,
          "BK(S_3) has %d edges, not %d" % (true_edges, all_pairs),
          "the Cayley graph of S_3 on adjacent transpositions is a 6-cycle")
R.note("The plant a wrong BK graph would produce is the COMPLETE graph, and 6 != 15 separates")
R.note("them at the smallest n where the two differ at all.")

R.banner("s0.9  PLANT 3 — CAME BACK INERT, AND IS PRINTED RATHER THAN SWAPPED OUT")
R.note("The plant was: make `weak_ideal` accept ANY adjacent transposition that lands in S,")
R.note("rather than one that REMOVES an inversion.  It changes NOTHING on this population:")
same = 0
tot = 0
for n in range(2, 5):
    for rel in POSETS[n]:
        LE = L.linear_extensions(rel, n)
        star = L.lstar(L.pair_marginals(LE, n), n)
        if star is None:
            continue
        tot += 1
        Sset = set(LE)
        loose = all(
            any(tuple(q) in Sset
                for q in ([list(p)[:i] + [p[i + 1], p[i]] + list(p)[i + 2:]
                           for i in range(n - 1)]))
            for p in LE if L.inversions_against(p, star) > 0)
        if loose == L.weak_ideal(LE, star):
            same += 1
R.verdict(same == tot, "the loosened predicate agrees at %d of %d posets" % (same, tot),
          "0 discrimination — the plant is INERT here")
R.note("WHY IT IS INERT, and it is a fact about the domain rather than about the plant: on an")
R.note("L(P) every member is connected to L* through L(P) itself, so the two readings coincide.")
R.note("A plant has to be a defect the domain can EXPRESS.  Reported, not replaced — a green")
R.note("from an inert plant says nothing about the control's power and pretending otherwise is")
R.note("the failure mode this section exists to avoid.")

R.banner("s0.10  PLANT 4 — a crossover that compares against n log2 n instead of log2 n!")
def wrong_crossover(c):
    for n in range(3, 100000):
        if c * n * math.log2(n) < n * math.log2(n):
            return n
    return None
R.verdict(wrong_crossover(0.9399) == 3,
          "planted: comparing c*n log2 n against n log2 n -> n* = %s" % wrong_crossover(0.9399),
          "says every c < 1 bites at n = 3; the real answer is 16,777,063")
R.note("THIS IS THE PLANT THAT MATTERS, because the whole of s2 is the claim that the REFERENCE")
R.note("SCALE is what decides vacuity.  A library that silently compared against the wrong scale")
R.note("would make s2's finding true by construction.  s0.6's agreement with mg-0fc6 to the unit")
R.note("is what rules it out.")

sys.exit(R.done())
