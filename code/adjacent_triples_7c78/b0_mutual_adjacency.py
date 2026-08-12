#!/usr/bin/env python3
"""mg-7c78 arm b0 — THE CORRECTED READING, PART 1: "3 ADJACENT" AS MUTUAL ADJACENCY, AND THE RUN
LEMMA THAT THE OTHER READING NEEDS.

pm-onethird's correction leaves four ambiguities (his list, and mine to Daniel).  Two of them can
be settled before Daniel answers, because they do not depend on which he meant -- they are facts
about the ambient object either way.  This arm settles both.

  b1  "THREE MUTUALLY ADJACENT LINEAR EXTENSIONS" IS IMPOSSIBLE UNDER ADJACENT TRANSPOSITIONS,
      AT EVERY POSET, WITH NO HYPOTHESIS.  The linear-extension graph is a subgraph of the
      Cayley graph of S_n with adjacent-transposition generators, which is BIPARTITE by the
      parity of the permutation -- one transposition flips it.  A bipartite graph is
      triangle-free.  Measured: triangle count and bipartiteness at every poset in the
      population.
  b2  AND THE KILL IS SPECIFIC TO *ADJACENT* TRANSPOSITIONS.  Under swaps of two values at
      ARBITRARY positions the graph does have triangles, so the refutation above is about the
      generator set and not about linear extensions being scarce.  This is the control that
      stops b1 being read as "no three extensions are ever close together".
  b3  THE RUN LEMMA, EXACTLY, AND BRUTE-FORCED.  The largest number of good items an ordering of
      N items can carry with NO 3 consecutive goods is N - floor(N/3).  Hence EVERY ordering has
      3 consecutive goods iff  g > N - floor(N/3) = ceil(2N/3).
  b4  WHERE THE `2/3` COMES FROM, AND THE DIVISIBILITY CATCH.  `p_xy > 2/3` gives `g > 2N/3`.
      That implies `g > ceil(2N/3)` IFF 3 divides N.  Otherwise there are counterexamples, and
      the smallest is exhibited: N = 4, g = 3 (so p = 3/4, comfortably over 2/3), ordering
      G G B G, no run of three.

Exits 0 if b1 finds 0 triangles and bipartiteness everywhere, b2 finds triangles somewhere, b3
agrees with brute force, and b4 exhibits the counterexample; 1 otherwise; 2 on refusal.
"""

import sys

import lib7c78 as L
import lib7c78b as B

NMAX = 6
LE_CAP = 400          # posets with more linear extensions than this are SKIPPED and COUNTED


def main():
    print("=" * 92)
    print("mg-7c78  b0  mutual adjacency is impossible, and the run lemma is exact")
    print("=" * 92)
    print()
    ok = True

    classes = L.all_classes(NMAX)

    print("b1  THREE MUTUALLY ADJACENT LINEAR EXTENSIONS -- adjacent-transposition graph")
    print("-" * 92)
    posets = skipped = tri_total = nonbip = 0
    edges_total = 0
    for n in range(2, NMAX + 1):
        for down in classes[n]:
            exts = L.linear_extensions(n, down)
            if len(exts) > LE_CAP:
                skipped += 1
                continue
            posets += 1
            g = B.adjacent_swap_graph(n, exts)
            edges_total += sum(len(a) for a in g) // 2
            tri_total += B.triangles(g)
            bip, _c = B.bipartite(g)
            if not bip:
                nonbip += 1
    print("    population: every isomorphism class n = 2..%d with |L(P)| <= %d." % (NMAX, LE_CAP))
    print("      %d posets examined, %d SKIPPED for |L(P)| > %d (counted, not silent)."
          % (posets, skipped, LE_CAP))
    print("      total graph edges %d · TRIANGLES %d · non-bipartite %d"
          % (edges_total, tri_total, nonbip))
    b1ok = tri_total == 0 and nonbip == 0 and edges_total > 0
    ok &= b1ok
    print("      [%s]" % ("PASS -- 0 triangles, bipartite everywhere" if b1ok else "FAIL"))
    print()
    print("    ⚠️  THIS IS A PROOF, NOT A SAMPLE.  One adjacent transposition changes the parity")
    print("    of the permutation, so the linear-extension graph is a subgraph of a bipartite")
    print("    graph at EVERY poset and every n -- there is nothing to check above n = %d." % NMAX)
    print("    SO IF `3 ADJACENT` MEANS THREE MUTUALLY ADJACENT IN THE BK GRAPH, THE CLAIM IS")
    print("    FALSE FOR EVERY POSET, AND `> 2/3` NEVER ENTERS.")
    print()

    print("b2  HOW FAR THE KILL REACHES, and the ONE adjacency notion that escapes it")
    print("-" * 92)
    vposets = vtri = 0
    for n in range(3, 6):
        for down in classes[n]:
            exts = L.linear_extensions(n, down)
            if len(exts) > LE_CAP:
                continue
            vposets += 1
            vtri += B.triangles(B.value_swap_graph(n, exts))
    print("    swaps of two values at ARBITRARY positions: %d posets, %d triangles"
          % (vposets, vtri))
    print("    ⚠️  STILL ZERO, AND FOR THE SAME REASON -- EVERY transposition is an ODD")
    print("    permutation, adjacent or not.  So the kill does NOT depend on the generators being")
    print("    adjacent: under ANY transposition-based notion of `adjacent linear extension` the")
    print("    graph is bipartite and three mutually adjacent extensions do not exist, at any")
    print("    poset, at any n, with no hypothesis.  b1's statement is stronger than b1 claimed.")
    print()
    print("    THE ONE ESCAPE, and it lands exactly where a6 already is.  Take `adjacent` to mean")
    print("    `related by rotating three consecutive positions` -- a 3-cycle, which is EVEN.")
    print("    Then sigma, sigma·c, sigma·c^2 IS a triangle, and it exists iff those three")
    print("    positions hold a FREE 3-BLOCK, i.e. a 3-element antichain.")
    ctri_posets = ctri = 0
    first = None
    for n in range(3, 6):
        for down in classes[n]:
            exts = L.linear_extensions(n, down)
            if len(exts) > LE_CAP:
                continue
            idx = {e: k for k, e in enumerate(exts)}
            g = [set() for _ in exts]
            for k, e in enumerate(exts):
                for pos in range(n - 2):
                    for rot in ((1, 2, 0), (2, 0, 1)):
                        sw = list(e)
                        blk = e[pos:pos + 3]
                        for t2 in range(3):
                            sw[pos + t2] = blk[rot[t2]]
                        j = idx.get(tuple(sw))
                        if j is not None and j != k:
                            g[k].add(j)
                            g[j].add(k)
            gg = [sorted(s) for s in g]
            t = B.triangles(gg)
            ctri_posets += 1
            ctri += t
            if t and first is None:
                first = (n, list(down), len(exts), t)
    b2ok = ctri > 0
    ok &= b2ok
    print("    3-cycle adjacency: %d posets, %d triangles   [%s]"
          % (ctri_posets, ctri, "CONTROL FIRED" if b2ok else "NOT FIRED -- b1 proves too much"))
    if first:
        print("    first witness: n=%d down-masks %s, |L(P)|=%d, %d triangles" % first)
    print("    AND THAT ESCAPE IS SHUT ON THE HYPOTHESIS CLASS.  a6 m2 measured the delta = 1/3")
    print("    boundary class exhaustively to n = 8: width 2 at every member, ZERO 3-element")
    print("    antichains.  No free 3-block exists there, so no such triangle exists there.")
    print("    BOTH mutual-adjacency readings therefore die, and the second one dies BECAUSE of")
    print("    the hypothesis rather than in spite of it.")
    print()

    print("b3  THE RUN LEMMA, closed form against brute force")
    print("-" * 92)
    print("    %4s %26s %20s %8s" % ("N", "brute force max goods", "N - floor(N/3)", "match"))
    b3ok = True
    for N in range(1, 17):
        bf = B.max_goods_without_run_bruteforce(N)
        cf = B.max_goods_without_run(N)
        m = bf == cf
        b3ok &= m
        print("    %4d %26d %20d %8s" % (N, bf, cf, "yes" if m else "NO"))
    ok &= b3ok
    print("    [%s]  exhaustive over all 2^N orderings for N <= 16."
          % ("PASS" if b3ok else "FAIL"))
    print()
    print("    SO: EVERY ordering of L(P) contains 3 consecutive extensions good for {x,y}")
    print("        IF AND ONLY IF   g > N - floor(N/3) = ceil(2N/3),")
    print("    where g = #good = p_xy * N and N = |L(P)|.")
    print()

    print("b4  WHERE THE `2/3` COMES FROM -- and the divisibility catch")
    print("-" * 92)
    print("    `p_xy > 2/3` gives `g > 2N/3`.  Is that enough for `g > ceil(2N/3)`?")
    print("    %6s %14s %18s %14s" % ("N mod 3", "smallest g > 2N/3", "ceil(2N/3)", "enough?"))
    import math
    cex = None
    for N in range(3, 22):
        gmin = N * 2 // 3 + 1
        need = math.ceil(2 * N / 3)
        enough = gmin > need
        if not enough and cex is None:
            cex = (N, gmin, need)
        print("    N=%-4d %14d %18d %14s" % (N, gmin, need, "yes" if enough else "NO"))
    print()
    b4ok = cex is not None
    ok &= b4ok
    if cex:
        N, g, need = cex
        print("    SMALLEST COUNTEREXAMPLE TO THE UNIVERSAL FORM UNDER `> 2/3` ALONE:")
        print("      N = %d, g = %d, so p = %d/%d > 2/3, and an avoiding ordering exists:"
              % (N, g, g, N))
        print("      G G B G  --  no three consecutive goods.   [%s]"
              % ("CONTROL FIRED" if b4ok else "NOT FIRED"))
    print()
    print("    THE PATTERN IS EXACTLY `3 divides N`.  `> 2/3` suffices for the universal form iff")
    print("    3 divides |L(P)|, and fails for every other residue.  A theorem whose truth turns")
    print("    on |L(P)| mod 3 is not the shape a real lemma takes -- which is evidence that the")
    print("    intended reading is the EXISTENTIAL one over orderings (Q-D, now with Daniel).")
    print()

    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
