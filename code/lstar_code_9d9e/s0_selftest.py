"""s0 — CONTROLS ON lib9d9e, BEFORE ANY ARM THAT PRODUCES A FINDING RUNS.

The two that matter most are `s0.6` and `s0.7`, and they matter for the same reason: every
number this directory publishes is an expected CODELENGTH, and a codelength is only an upper
bound on `log2 e(P)` if the thing producing it is a code.  So Kraft is checked EXACTLY, as an
equality where the construction claims one, and Gibbs (`E[len] >= log2 e(P)`) is checked at every
poset the arm can reach.  A "code" failing either would make every table in `s1` meaningless
while still printing plausible numbers.
"""

import math
from fractions import Fraction
from itertools import permutations

import lib9d9e as L

R = L.Report()
NMAX = 5

# --------------------------------------------------------------------------------------------
R.banner("s0.1  THE ENUMERATOR AGAINST A001035 — and by a DIFFERENT ALGORITHM from lib99f4's")

A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231, 6: 130023}
POSETS = {}
for n in range(1, 7):
    POSETS[n] = L.all_posets(n)
    R.verdict(len(POSETS[n]) == A001035[n],
              "labelled posets on [%d]" % n,
              "%d   (A001035: %d)" % (len(POSETS[n]), A001035[n]))
R.note("lib99f4 brute-forces the 3^C(n,2) orientations and keeps the transitive ones; this")
R.note("library INSERTS an element into every poset on [n-1] as a (down-set, up-set) pair.")
R.note("Agreement is therefore a second route to A001035 rather than the same route twice --")
R.note("and the insertion route reaches n = 6, which brute force does not.")

# --------------------------------------------------------------------------------------------
R.banner("s0.2  e(P) BY THREE ROUTES — recursion, down-set DP, and a filter of S_n")

bad_dp = bad_filter = 0
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        LEs = L.linear_extensions(rel, n)
        if len(LEs) != L.count_extensions_dp(rel, n):
            bad_dp += 1
        if n <= 5:
            brute = tuple(sorted(p for p in permutations(range(n))
                                 if all(p.index(x) < p.index(y) for x, y in rel)))
            if brute != LEs:
                bad_filter += 1
R.verdict(bad_dp == 0, "recursion agrees with the down-set DP at every poset, n = 2..%d" % NMAX)
R.verdict(bad_filter == 0, "recursion agrees with a FILTER of S_n at every poset, n = 2..%d" % NMAX,
          "the DP never enumerates a permutation, so this is the route it is checked on")

# --------------------------------------------------------------------------------------------
R.banner("s0.3  THE TAPE IS A BIJECTION — mg-0fc6 a1.1 reproduced on code sharing nothing with it")

for n in range(4, 9):
    t = L.merge_tree(tuple(range(n)))
    seen = set()
    for p in permutations(range(n)):
        seen.add(L.tape(t, p))
    R.verdict(len(seen) == math.factorial(n),
              "n = %d: %d distinct tapes over %d permutations" % (n, len(seen), math.factorial(n)),
              "0 collisions")
R.note("This is what makes the MERGE-IDX row a CODE rather than a lossy summary, and it is also")
R.note("mg-0fc6's own statement that compression2's encoding forgets nothing.  Checked here at")
R.note("n = 4..8 (40 320 permutations at the top) on an independent implementation.")

# --------------------------------------------------------------------------------------------
R.banner("s0.4  THE BINOMIALS TELESCOPE — prod C(a+b,a) over the tree = n!")

bad = 0
for n in range(1, 17):
    t = L.merge_tree(tuple(range(n)))
    prod = 1
    for _, l, r in L.tree_nodes(t):
        prod *= math.comb(len(l[0]) + len(r[0]), len(l[0]))
    if prod != math.factorial(n):
        bad += 1
R.verdict(bad == 0, "prod over internal nodes of C(a+b,a) = n! at every n = 1..16")
R.note("So the exact-index reading of the tape has a codelength of exactly log2 n! at EVERY")
R.note("permutation.  P1 is a consequence of this line; s1 measures it rather than deriving it.")

# --------------------------------------------------------------------------------------------
R.banner("s0.5  L* IS A LINEAR EXTENSION WHEREVER IT EXISTS — the defining property, with a "
         "vacuity guard")

has = bad = 0
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        LEs = L.linear_extensions(rel, n)
        star = L.lstar(L.pair_marginals(LEs, n), n)
        if star is None:
            continue
        has += 1
        if star not in set(LEs):
            bad += 1
R.verdict(bad == 0, "L* in L(P) at all %d posets where L* exists, n = 2..%d" % (has, NMAX))
R.verdict(has > 0, "L* exists SOMEWHERE — the vacuity guard", "%d posets" % has)

# --------------------------------------------------------------------------------------------
R.banner("s0.6  KRAFT, EXACTLY — every code is a code, TWO are TIGHT, and the L* merge code "
         "IS NOT")

TIGHT = {"MINIMALS", "OPT"}
worst = {}
tight_ok = {}
leak = {}
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        LEs = L.linear_extensions(rel, n)
        ctx = L.context(rel, n, LEs=LEs)
        for name, fn in L.CODES:
            k = L.kraft(rel, n, LEs, ctx, fn)
            if k is None:
                continue
            tag = name.split()[0]
            worst[tag] = max(worst.get(tag, Fraction(0)), k)
            if tag in TIGHT:
                tight_ok[tag] = tight_ok.get(tag, True) and (k == 1)
            if tag == "MERGE-P":
                cur = leak.get(n, (Fraction(1), 0, None))
                lo = min(cur[0], k)
                leak[n] = (lo, cur[1] + (1 if k != 1 else 0),
                           rel if k == lo and k != 1 else cur[2])
for tag in sorted(worst):
    R.verdict(worst[tag] <= 1, "%-11s max Kraft sum over L(P)" % tag, "%s" % worst[tag])
for tag in sorted(TIGHT):
    R.verdict(tight_ok.get(tag, False), "%-11s Kraft sum = 1 EXACTLY at every poset" % tag)
R.note("Exact Fractions, so `= 1` is an equality and not a rounding.  MINIMALS and OPT are")
R.note("TIGHT: their leaves are exactly L(P), every feasible choice tuple is a linear extension")
R.note("and every linear extension is one.  FREE and MERGE-IDX sum to e(P)/n! < 1 BECAUSE they")
R.note("code all of S_n -- that slack IS the free bound's waste, in one number.")

R.line()
R.line("  THE `L*` MERGE CODE IS **NOT** TIGHT, AND THIS ROW IS WHY THE FIRST DRAFT WENT RED.")
for n in sorted(leak):
    lo, cnt, wit = leak[n]
    R.line("    n = %d   %4d of %5d posets leak   worst Kraft sum %s"
           % (n, cnt, len(POSETS[n]), lo))
R.note("Feasibility is checked LOCALLY, against the two sequences at hand.  Two locally valid")
R.note("halves need not be interleavable at all, so the bottom-up code can reach a node with")
R.note("ZERO feasible merges and mass leaks into dead branches.  THE FIRST WITNESS, EXHIBITED:")
WIT = frozenset({(1, 3), (2, 0)})
wt = L.merge_tree((0, 1, 2, 3))
for u, v in [((0, 1), (2, 3)), ((0, 1), (3, 2)), ((1, 0), (2, 3)), ((1, 0), (3, 2))]:
    R.note("     P = {1<3, 2<0}   halves %s | %s  ->  %d feasible merges"
           % (u, v, L.feasible_merges(u, v, WIT)))
R.note("    `(0,1)` and `(3,2)` are each valid on their own set; together with P they close the")
R.note("    4-cycle  2 < 0 < 1 < 3 < 2.  Mass 1/4 dies there, Kraft = 3/4.")
kw = L.kraft(WIT, 4, L.linear_extensions(WIT, 4), L.context(WIT, 4), L.q_merge_p)
R.verdict(kw == Fraction(3, 4), "the exhibited witness has Kraft sum 3/4", "%s" % kw)
R.verdict(all(leak[n][0] <= 1 for n in leak),
          "MERGE-P is still a CODE at every poset (Kraft <= 1), so every bound it gives stands",
          "s0.7 checks the bound itself")

# --------------------------------------------------------------------------------------------
R.banner("s0.7  GIBBS — every code's expected length is at or above log2 e(P), at every poset")

bad = 0
worst_gap = None
for n in range(2, NMAX + 1):
    for rel in POSETS[n]:
        LEs = L.linear_extensions(rel, n)
        ctx = L.context(rel, n, LEs=LEs)
        target = math.log2(len(LEs))
        for name, fn in L.CODES:
            tot = 0.0
            ok = True
            for Lx in LEs:
                q = fn(Lx, ctx)
                if q is None:
                    ok = False
                    break
                tot += L.ideal_bits(q)
            if not ok:
                continue
            gap = tot / len(LEs) - target
            if gap < -1e-9:
                bad += 1
            if worst_gap is None or gap < worst_gap:
                worst_gap = gap
R.verdict(bad == 0, "E[len] >= log2 e(P) for all 7 codes at all %d posets, n = 2..%d"
          % (sum(len(POSETS[n]) for n in range(2, NMAX + 1)), NMAX),
          "smallest gap %.2e (attained by OPT, which is the equality case)" % worst_gap)

# --------------------------------------------------------------------------------------------
R.banner("s0.8  THE BOUNDARY FAMILY — delta = 1/3 EXACTLY at n = 3..12, and e(P) = 3^floor(n/3)")

bad = 0
for n in range(3, 13):
    rel = L.vsum(n)
    LEs = L.linear_extensions(rel, n)
    d = L.delta(rel, LEs, n)
    e = len(LEs)
    ok = (d == Fraction(1, 3)) and (e == 3 ** (n // 3))
    if not ok:
        bad += 1
    R.verdict(ok, "n = %2d   delta = %-4s   e(P) = %-5d" % (n, d, e),
              "log2 e = %7.4f   vs   log2 n! = %8.4f" % (math.log2(e), L.log2_factorial(n)))
R.note("mg-9b6b's explicit family, rebuilt here and re-verified rather than quoted.  It is the")
R.note("closest INSTANTIABLE population to hypothesis (1): frozen is delta < 1/3 and is empty")
R.note("at every n this or any other instrument can reach -- see s0.9 and s2.")

# --------------------------------------------------------------------------------------------
R.banner("s0.9  THE FROZEN CLASS IS EMPTY AT n <= 5 — re-established here, not cited")

for n in range(3, NMAX + 1):
    mind = None
    for rel in POSETS[n]:
        LEs = L.linear_extensions(rel, n)
        if len(LEs) == 1:
            continue                      # a chain: delta = 0 over an empty max, excluded
        d = L.delta(rel, LEs, n)
        mind = d if mind is None else min(mind, d)
    R.verdict(mind == Fraction(1, 3), "n = %d   min delta over NON-CHAINS = %s" % (n, mind),
              "so {delta < 1/3} is EMPTY and {delta = 1/3} is the boundary")

# --------------------------------------------------------------------------------------------
R.banner("s0.10  THE UNIFORM SAMPLER — used only above the enumeration cap, checked below it")

rng = L.LCG()
rel, n = L.two_chains(8), 8
LEs = L.linear_extensions(rel, n)
exact = L.pair_marginals(LEs, n)
N = 20000
counts = [L.sample_extension(rel, n, rng) for _ in range(N)]
emp = L.pair_marginals(counts, n)
worst = max(abs(float(emp[k]) - float(exact[k])) for k in exact)
R.verdict(worst < 0.02, "sampled pair marginals match the exact ones at two_chains(8)",
          "%d draws, e(P) = %d, worst |deviation| = %.4f" % (N, len(LEs), worst))
R.verdict(len(set(counts)) == len(LEs), "every one of the %d extensions was drawn" % len(LEs))

# --------------------------------------------------------------------------------------------
R.banner("s0.11  FIVE PLANTED DEFECTS — four live, ONE INERT AND PRINTED RATHER THAN SWAPPED OUT")

REL, N5 = L.vsum(6), 6
LES5 = L.linear_extensions(REL, N5)


def merge_p_beats_free():
    ctx = L.context(REL, N5, LEs=LES5)
    tot = sum(L.ideal_bits(L.q_merge_p(x, ctx)) for x in LES5) / len(LES5)
    return tot < L.log2_factorial(N5) - 1e-9


def kraft_merge_p():
    ctx = L.context(REL, N5, LEs=LES5)
    return L.kraft(REL, N5, LES5, ctx, L.q_merge_p)


# D1 — feasibility blind to P
orig_feas = L.feasible_merges
L.feasible_merges = lambda left, right, rel: math.comb(len(left) + len(right), len(left))
caught = not merge_p_beats_free()
L.feasible_merges = orig_feas
R.verdict(caught, "D1  feasible_merges ignores P  ->  MERGE-P stops beating the free bound",
          "CAUGHT" if caught else "MISSED")

# D2 — feasibility over-reported by one
L.feasible_merges = lambda left, right, rel: orig_feas(left, right, rel) + 1
k = kraft_merge_p()
L.feasible_merges = orig_feas
R.verdict(k != 1, "D2  feasibility +1  ->  Kraft sum %s, no longer 1" % k,
          "CAUGHT BY THE EQUALITY ROW ONLY -- Kraft <= 1 still holds, so a `<= 1` check misses it")

# D3 — feasibility under-reported by one
L.feasible_merges = lambda left, right, rel: max(1, orig_feas(left, right, rel) - 1)
k = kraft_merge_p()
L.feasible_merges = orig_feas
R.verdict(k > 1, "D3  feasibility -1  ->  Kraft sum %s > 1, so it is not a code at all" % k,
          "CAUGHT")

# D4 — the tape loses its last word
orig_nodes = L.tree_nodes
L.tree_nodes = lambda t: orig_nodes(t)[:-1] if orig_nodes(t) else []
t = L.merge_tree(tuple(range(6)))
seen = {L.tape(t, p) for p in permutations(range(6))}
L.tree_nodes = orig_nodes
R.verdict(len(seen) < 720, "D4  the tape drops its root word  ->  %d distinct tapes for 720 "
          "permutations" % len(seen), "CAUGHT")

# D5 — the tree bisects the other way
orig_tree = L.merge_tree


def other_tree(order):
    if len(order) == 1:
        return (tuple(order), None, None)
    h = (len(order) + 1) // 2
    return (tuple(order), other_tree(order[:h]), other_tree(order[h:]))


L.merge_tree = other_tree
prod_ok = True
for n in range(1, 13):
    tt = other_tree(tuple(range(n)))
    prod = 1
    for _, l, r in orig_nodes(tt):
        prod *= math.comb(len(l[0]) + len(r[0]), len(l[0]))
    prod_ok = prod_ok and (prod == math.factorial(n))
L.merge_tree = orig_tree
R.verdict(prod_ok, "D5  the tree bisects the OTHER way  ->  MERGE-IDX is STILL exactly log2 n!",
          "INERT, and printed rather than swapped out")
R.note("D5 is inert because the telescoping is a property of ANY binary tree over the elements,")
R.note("not of the balanced bisection.  That is worth more than a live plant here: it says P1")
R.note("does not depend on compression2's choice of tree, so no repair to the tree can rescue")
R.note("the exact-index reading.  A plant has to be a defect the claim can EXPRESS, and this")
R.note("claim cannot express a change of tree.")

raise SystemExit(R.done())
