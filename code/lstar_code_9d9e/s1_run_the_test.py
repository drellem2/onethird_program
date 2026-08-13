"""s1 — THE TICKET'S TEST, RUN.

    "Does the code's expected length beat ceil(log2 n!) -- the code that indexes L into all of
     S_n and ignores P entirely -- AT THE n YOU CLAIM IT?"                        (mg-99f4 §3)

Seven codes, six families, `n = 6..12`.  Nothing here is asymptotic and nothing here is a proof:
a code answers the question by being run, which is the predecessor's own point and is why this
arm is four seconds rather than a theorem.

WHAT TO READ FIRST.  `s1.1` is the answer for `compression2`'s own construction and it does not
need a table: the tape is a BIJECTION, so indexing its words exactly is the free code written in
another coordinate system.  Everything after that is about codes that read `P` for real.
"""

import math

import lib9d9e as L

R = L.Report()
NS = list(range(6, 13))

# --------------------------------------------------------------------------------------------
R.banner("s1.1  compression2's OWN TAPE, READ AS A CODE — the two P-blind readings, at n = 6..12")

R.line("   n | ceil(log2 n!) | MERGE-IDX exact-index | MERGE-TAPE fixed-width | verdict")
R.line("  ---+---------------+-----------------------+------------------------+---------------")
bad = 0
for n in NS:
    free = math.ceil(L.log2_factorial(n))
    t = L.merge_tree(tuple(range(n)))
    prod = 1
    for _, l, r in L.tree_nodes(t):
        prod *= math.comb(len(l[0]) + len(r[0]), len(l[0]))
    idx = math.log2(prod)
    tape = L.tape_width(n)
    ties = abs(idx - L.log2_factorial(n)) < 1e-9
    loses = tape > free
    if not (ties and loses):
        bad += 1
    R.line("  %2d |          %4d |   %8.4f  %-7s|   %4d  %-13s| %s"
           % (n, free, idx, "= log2 n!" if ties else "!!", tape,
              "LOSES by %d" % (tape - free) if loses else "!!",
              "NEITHER READING BEATS THE FREE BOUND"))
R.verdict(bad == 0, "P1 and P2 hold at every n = 6..12",
          "exact-index TIES log2 n! exactly; fixed-width LOSES at every n")
R.note("THIS IS THE ANSWER FOR THE CONSTRUCTION THE TICKET NAMED, AND IT IS NOT A MEASUREMENT")
R.note("OF A CONSTANT.  The tape is a bijection S_n -> (merge words) -- s0.3, 0 collisions at")
R.note("n = 4..8 -- and the binomials telescope to n! -- s0.4, every n <= 16.  So the exact-index")
R.note("reading IS the free code, re-coordinatised, at every poset and every n.  mg-0fc6's own")
R.note("sentence says as much from the other side: `compression2's encoding forgets NOTHING --")
R.note("it is a re-coordinatisation`.  A re-coordinatisation of the free code is the free code.")
R.note("s0's D5 makes the same point from the plant side: the telescoping holds for ANY binary")
R.note("tree, so no repair to the TREE can rescue this reading.")
R.line()
R.note("What compression2 actually bounds is therefore not this code's length.  It is the")
R.note("ENTROPY of the merge words under Unif(L(P)) -- a statement about the MEASURE, bounded")
R.note("node by node.  s1.6 measures those per-node entropies where they can be instantiated.")

# --------------------------------------------------------------------------------------------
R.banner("s1.2  THE FULL TEST — every code, every family, n = 6..12  (bits, expected under "
         "Unif(L(P)))")

rng = L.LCG()
RESULTS = {}
for fam, fn in L.FAMILIES:
    R.line()
    R.line("  FAMILY: %s" % fam)
    R.line("     n |  e(P) | log2 e |  FREE | M-TAPE | M-IDX | MERGE-P | MINIMALS | LEHMER | how")
    R.line("    ---+-------+--------+-------+--------+-------+---------+----------+--------+-----")
    for n in NS:
        rel = fn(n)
        ctx, rows, how = L.measure(rel, n, rng=rng)
        e = ctx["e"]
        get = lambda tag: next(v for k, v in rows.items() if k.startswith(tag))  # noqa: E731
        vals = {t: get(t)[0] for t in ["FREE", "MERGE-TAPE", "MERGE-IDX", "MERGE-P",
                                       "MINIMALS", "LEHMER"]}
        RESULTS[(fam, n)] = (e, vals, ctx)
        fmt = lambda v: "  n/a " if v is None else "%6.2f" % v  # noqa: E731
        R.line("    %2d |%6d | %6.3f |%6.2f | %6.2f |%6.2f | %7.2f | %8.2f | %s | %s"
               % (n, e, math.log2(e), vals["FREE"], vals["MERGE-TAPE"], vals["MERGE-IDX"],
                  vals["MERGE-P"], vals["MINIMALS"], fmt(vals["LEHMER"]), how))

R.line()
R.note("`how = exact` enumerates L(P); `sampled(N)` draws N uniform extensions with the LCG.")
R.note("Which one produced a row is PRINTED and not inferred -- they are different kinds of")
R.note("number.  Note where the sampling happens: only at the ANTICHAIN, which is exactly the")
R.note("family where every code is CONSTANT and the sample cannot be wrong.")

# --------------------------------------------------------------------------------------------
R.banner("s1.3  THE TEST'S VERDICT — AND THE TEST AS LITERALLY WORDED IS PASSED BY THE CODE IT "
         "COMPARES AGAINST")

R.line("   `beat ceil(log2 n!)` is not the same test as `beat log2 n!`, and the gap between")
R.line("   them is the rounding.  The FREE code -- the one the test names as the thing to beat")
R.line("   -- has ideal length log2 n!, so it beats its OWN ceiling at every n where n! is not")
R.line("   a power of two:")
R.line()
R.line("     n |  log2 n! | ceil | FREE beats its own ceiling by")
R.line("    ---+----------+------+------------------------------")
for n in NS:
    lf = L.log2_factorial(n)
    R.line("    %2d | %8.4f |  %3d | %.4f bits"
           % (n, lf, math.ceil(lf), math.ceil(lf) - lf))
R.verdict(all(math.ceil(L.log2_factorial(n)) - L.log2_factorial(n) > 0 for n in NS),
          "the reference code passes the test that names it, at every n = 6..12",
          "so the literal wording cannot be the screen; the margin is what carries")
R.line()
R.line("   Read against log2 n! instead.  YES = beats it; ROUND = beats only ceil(log2 n!), on")
R.line("   the rounding alone, by under one bit; NO = does not beat even that.")
R.line()
R.line("   family                          | MERGE-P at n = 6..12          | margin at n = 12")
R.line("  --------------------------------+-------------------------------+-----------------")
for fam, _ in L.FAMILIES:
    marks = []
    for n in NS:
        e, vals, ctx = RESULTS[(fam, n)]
        lf = L.log2_factorial(n)
        m = vals["MERGE-P"]
        marks.append("YES  " if m < lf - 1e-6 else
                     "ROUND" if m < math.ceil(lf) - 1e-9 else "NO   ")
    m12 = L.log2_factorial(12) - RESULTS[(fam, 12)][1]["MERGE-P"]
    R.line("   %-31s | %s | %+8.3f bits" % (fam, " ".join(marks), m12))
R.verdict(all(RESULTS[(f, n)][1]["MERGE-P"] < L.log2_factorial(n) - 1e-6
              for f, _ in L.FAMILIES if "antichain (" not in f for n in NS),
          "P3: MERGE-P beats log2 n! at every non-antichain family, every n = 6..12")
R.verdict(all(abs(RESULTS[("antichain (delta = 1/2)", n)][1]["MERGE-P"]
                  - L.log2_factorial(n)) < 1e-6 for n in NS),
          "P3: MERGE-P TIES log2 n! EXACTLY at the antichain, every n = 6..12",
          "so its ROUND row passes the literal test on the rounding and on nothing else")
R.note("The antichain row is not a limitation of this code.  e(antichain) = n!, so log2 e(P) is")
R.note("log2 n! there and Gibbs forbids ANY code from doing better.  s2 turns that into the")
R.note("statement it is: a shape-B constant c < 1 valid at every P does not exist, for any code")
R.note("that will ever be written.")

# --------------------------------------------------------------------------------------------
R.banner("s1.4  THE ONE POPULATION THE BOUND IS ABOUT — the boundary family, priced in both "
         "shapes")

R.line("   The class hypothesis (1) names is FROZEN, delta < 1/3, and it is EMPTY at every n")
R.line("   below 15 (s0.9 here; the corpus has it empty to n = 8 and the conjecture verified")
R.line("   to n = 14).  The closest INSTANTIABLE population is the boundary, delta = 1/3.")
R.line()
R.line("     n | log2 n! | log2 e(P) | MERGE-P | shape-A c = E/(n log2 n) | shape-B c = E/log2 n!")
R.line("    ---+---------+-----------+---------+--------------------------+----------------------")
fam = "boundary  (V-sum, delta = 1/3)"
for n in NS:
    e, vals, ctx = RESULTS[(fam, n)]
    lf = L.log2_factorial(n)
    nlogn = n * math.log2(n)
    R.line("    %2d | %7.3f |   %7.3f | %7.3f |                   %6.4f |                %6.4f"
           % (n, lf, math.log2(e), vals["MERGE-P"], vals["MERGE-P"] / nlogn,
              vals["MERGE-P"] / lf))
R.line()
R.note("BOTH CONSTANTS FALL WITH n AND KEEP FALLING.  That is not the code being good; it is")
R.note("the population having log2 e(P) = Theta(n) against a free bound of Theta(n log n).")
R.note("On this population EVERY code that reads P at all wins by a margin that GROWS, so")
R.note("PASSING THE TEST HERE CARRIES NO INFORMATION ABOUT THE CODE.  compression2's own")
R.note("0.9399 is 30x above what a four-line code delivers at n = 12.")

# --------------------------------------------------------------------------------------------
R.banner("s1.5  IS `L*` DOING THE WORK?  — the L*-free code, side by side")

R.line("   family                          |  n | MERGE-P (uses L*) | MINIMALS (does not) | who wins")
R.line("  --------------------------------+----+-------------------+---------------------+---------")
wins = {"MERGE-P": 0, "MINIMALS": 0, "tie": 0}
for fam, _ in L.FAMILIES:
    for n in NS:
        e, vals, ctx = RESULTS[(fam, n)]
        a, b = vals["MERGE-P"], vals["MINIMALS"]
        w = "tie" if abs(a - b) < 1e-9 else ("MERGE-P" if a < b else "MINIMALS")
        wins[w] += 1
        if n in (6, 12):
            R.line("   %-31s | %2d |          %8.3f |            %8.3f | %s"
                   % (fam, n, a, b, w))
R.line()
R.line("   over all %d (family, n) cells:  MERGE-P %d   MINIMALS %d   tie %d"
       % (sum(wins.values()), wins["MERGE-P"], wins["MINIMALS"], wins["tie"]))
R.note("MINIMALS reads P and NEVER reads L*.  It is four lines long.  Whatever the split, the")
R.note("conclusion is the same one: the win over the free bound is bought by reading P, not by")
R.note("reading L*, and L* is the half mg-0fc6 measured the poset-dependence washing out at.")

# --------------------------------------------------------------------------------------------
R.banner("s1.6  compression2's REAL OBJECT — the PER-NODE conditional entropies, on the "
         "boundary family")

R.note("The note bounds `H(W_v | earlier words) <= (1-c)(a+b)` at each node and sums over the")
R.note("n log2 n total word length.  The chain rule makes the sum EXACTLY log2 e(P), which is")
R.note("this table's own control -- if the entropies did not sum to log2 e(P) the decomposition")
R.note("would not be the note's.")
R.line()


def node_entropies(rel, n, LEs):
    """`H(W_v | words at earlier nodes)` for each node in post-order, under Unif(L(P))."""
    star = L.lstar(L.pair_marginals(LEs, n), n) or tuple(range(n))
    tree = L.merge_tree(star)
    nodes = L.tree_nodes(tree)
    words = {}
    for Lx in LEs:
        pos = {v: i for i, v in enumerate(Lx)}
        seqs = L.node_sequences(tree, pos)
        words[Lx] = tuple(L.merge_word(*seqs[nd[0]], perm_pos=pos) for nd in nodes)
    out = []
    for i, nd in enumerate(nodes):
        groups = {}
        for Lx in LEs:
            groups.setdefault(words[Lx][:i], []).append(words[Lx][i])
        h = 0.0
        for pre, ws in groups.items():
            p_pre = len(ws) / len(LEs)
            cnt = {}
            for w in ws:
                cnt[w] = cnt.get(w, 0) + 1
            h += p_pre * sum(-(c / len(ws)) * math.log2(c / len(ws)) for c in cnt.values())
        out.append((len(nd[0]), h))
    return out


R.line("     n | node size a+b | H(word | earlier) | note's ceiling 0.9399(a+b) | overpay")
R.line("    ---+---------------+-------------------+----------------------------+---------")
bad = 0
for n in (6, 9, 12):
    rel = L.vsum(n)
    LEs = L.linear_extensions(rel, n)
    ents = node_entropies(rel, n, LEs)
    tot = sum(h for _, h in ents)
    if abs(tot - math.log2(len(LEs))) > 1e-9:
        bad += 1
    agg = {}
    for size, h in ents:
        cur = agg.get(size, [0.0, 0])
        agg[size] = [cur[0] + h, cur[1] + 1]
    for size in sorted(agg):
        h, k = agg[size]
        ceil_ = 0.9399 * size * k
        R.line("    %2d | %13d | %17.4f | %26.4f | %s"
               % (n, size, h, ceil_,
                  "%.0fx" % (ceil_ / h) if h > 1e-9 else "INFINITE (H = 0)"))
    R.line("       |   %d nodes    | sum = %8.4f    | log2 e(P) = %8.4f       | %s"
           % (len(ents), tot, math.log2(len(LEs)),
              "chain rule EXACT" if abs(tot - math.log2(len(LEs))) < 1e-9 else "!!"))
    R.line()
R.verdict(bad == 0, "the per-node entropies sum to log2 e(P) EXACTLY at n = 6, 9, 12",
          "so this IS the note's decomposition and not a different one")
R.note("A NODE WHOSE SPLIT FALLS ON A BLOCK BOUNDARY CARRIES ZERO CONDITIONAL ENTROPY, because")
R.note("the boundary family is an ordinal sum and a block's elements are consecutive in L*: the")
R.note("merge word there is FORCED.  The note's ceiling pays 0.9399(a+b) bits for a word that")
R.note("carries none, so the overpayment at those nodes is not a factor -- it is infinite.")
R.note("P10 holds AS WRITTEN, and the run adds the clause the prediction did not have:")
R.note("⚠️ WHICH NODES THOSE ARE DEPENDS ON n, AND AT n = 9 THE ROOT IS NOT ONE OF THEM.  Nine")
R.note("elements bisect 4|5 while the blocks are 3|3|3, so the root straddles a block and")
R.note("carries 0.6667 bits.  At n = 6 and n = 12 the bisection lands on block boundaries and")
R.note("the top TWO levels are free.  THE TREE IS BUILT FROM L* AND L* KNOWS NOTHING ABOUT THE")
R.note("BLOCK STRUCTURE -- so whether the expensive nodes are free is an ARITHMETIC ACCIDENT of")
R.note("n against the block size, which is the sharpest form of mg-0fc6's wash-out this arm")
R.note("reaches: the one place the poset could have entered the construction, it did not.")
R.note("⚠️ This prices the note's PER-NODE LEMMA on one family; it is not a refutation of the")
R.note("note's theorem, which is a worst-case statement and is allowed to be loose anywhere in")
R.note("particular.  What it shows is where the slack is, and it is at the top of the tree.")

raise SystemExit(R.done())
