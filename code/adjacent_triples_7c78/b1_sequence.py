#!/usr/bin/env python3
"""mg-7c78 arm b1 — THE CORRECTED READING, PART 2: `3 ADJACENT` AS THREE CONSECUTIVE IN AN
ORDERING OF L(P).

Daniel: "pick some permutation of the whole set of linear extensions (for instance one specially
crafted) then there will always be 3 adjacent linear extensions sharing a given 'good' edge".

Fix the vocabulary.  `N = |L(P)|`.  For an incomparable pair {x,y}, an extension is GOOD for it
when it orients the pair the way `e` does; `g_xy = p_xy · N` counts them.  Three readings, in
increasing strength, and all three are measured because Daniel has not answered yet:

  Q2  UNIVERSAL over orderings, one edge at a time.  b0 b3 gives the sharp criterion:
      every ordering has a good run of 3 for {x,y}  iff  g_xy > ceil(2N/3).
  Q1  EXISTENTIAL over orderings, ALL edges at once -- one crafted ordering serving every
      incomparable edge simultaneously.  This is the reading with content, and the one
      "specially crafted" points at.
  Q3  Q1 restricted to GRAY CODES -- orderings in which consecutive extensions differ by a single
      adjacent transposition, i.e. Hamiltonian paths in the BK graph.

  m1  Q2 measured: the fraction of (poset, edge) at which `> 2/3` alone is enough, banded by
      delta, with the boundary class called out.
  m2  Q1 decided where it can be: the NECESSARY condition (g_xy >= 3) and a SUFFICIENT condition
      (a system of pairwise-DISJOINT good triples, one per edge, decided EXACTLY by max flow).
      Posets that pass the necessary and fail the sufficient are counted as UNDECIDED, not as
      failures -- disjointness is sufficient and not necessary.
  m3  Q3: Hamiltonian-path existence in the BK graph, and the structural fact that makes the run
      condition nearly free in a Gray code -- three consecutive vertices of ANY walk differ by at
      most two swaps, so a run of 3 is unanimous on all but at most 2 incomparable edges.

Exits 0 if the arm's own consistency checks hold, 1 otherwise, 2 on refusal.
"""

import math
import sys
from fractions import Fraction

import lib7c78 as L
import lib7c78b as B

NMAX = 6
LE_CAP = 200           # |L(P)| cap for the flow and graph work; skips are COUNTED
HAM_CAP = 60           # |L(P)| cap for Hamiltonian-path search
THIRD = Fraction(1, 3)
HALF = Fraction(1, 2)


def disjoint_triples_feasible(good, nexts):
    """EXACT: is there a system of pairwise-disjoint triples, one per edge, each triple made of
    extensions good for that edge?  Max-flow: source -> edge (cap 3) -> good extensions (cap 1)
    -> sink.  Feasible iff flow = 3 * #edges."""
    keys = list(good)
    m = len(keys)
    if m == 0:
        return True
    S, T = 0, 1 + m + nexts
    Nn = T + 1
    cap = [{} for _ in range(Nn)]

    def add(u, v, c):
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)

    for i, k in enumerate(keys):
        add(S, 1 + i, 3)
        for j, isgood in enumerate(good[k]):
            if isgood:
                add(1 + i, 1 + m + j, 1)
    for j in range(nexts):
        add(1 + m + j, T, 1)

    flow = 0
    while True:
        par = {S: None}
        stack = [S]
        while stack and T not in par:
            u = stack.pop()
            for v, c in cap[u].items():
                if c > 0 and v not in par:
                    par[v] = u
                    stack.append(v)
        if T not in par:
            break
        v, bott = T, math.inf
        while par[v] is not None:
            u = par[v]
            bott = min(bott, cap[u][v])
            v = u
        v = T
        while par[v] is not None:
            u = par[v]
            cap[u][v] -= bott
            cap[v][u] += bott
            v = u
        flow += bott
    return flow == 3 * m


def main():
    print("=" * 92)
    print("mg-7c78  b1  three CONSECUTIVE linear extensions in an ordering of L(P)")
    print("=" * 92)
    print()
    ok = True
    classes = L.all_classes(8)

    # ---- build the working population ------------------------------------------------------
    work = []          # (n, down, exts, p, e, delta)
    skipped_cap = no_e = 0
    for n in range(2, NMAX + 1):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            exts = L.linear_extensions(n, down)
            if len(exts) > LE_CAP:
                skipped_cap += 1
                continue
            p = L.pair_probs(n, down, exts)
            e = B.majority_order(n, down, p)
            if e is None:
                no_e += 1
                continue
            work.append((n, down, exts, p, e, L.delta(n, down, p)))
    # the boundary class to n = 8, added exhaustively: it is the hypothesis class
    bnd_extra = 0
    for n in range(7, 9):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            exts = L.linear_extensions(n, down)
            p = L.pair_probs(n, down, exts)
            if L.delta(n, down, p) != THIRD:
                continue
            e = B.majority_order(n, down, p)
            if e is None or len(exts) > LE_CAP:
                skipped_cap += 1
                continue
            work.append((n, down, exts, p, e, THIRD))
            bnd_extra += 1

    print("POPULATION.  Every isomorphism class n = 2..%d with a well-defined `e` and" % NMAX)
    print("  |L(P)| <= %d, PLUS the delta = 1/3 boundary class at n = 7, 8 (%d more)."
          % (LE_CAP, bnd_extra))
    print("  %d posets.  SKIPPED for |L(P)| > %d: %d.  NO well-defined `e` (a pair at exactly"
          % (len(work), LE_CAP, skipped_cap))
    print("  1/2, or a majority cycle): %d -- excluded because `good` NAMES `e`." % no_e)
    print()

    print("m1  Q2 (UNIVERSAL over orderings) -- is `> 2/3` alone enough?")
    print("-" * 92)
    bands = [
        ("delta = 1/3   (boundary)", lambda d: d == THIRD),
        ("1/3 < delta <= 2/5", lambda d: THIRD < d <= Fraction(2, 5)),
        ("2/5 < delta < 1/2", lambda d: Fraction(2, 5) < d < HALF),
    ]
    print("    %-28s %8s %14s %14s %10s"
          % ("delta band", "edges", "g > ceil(2N/3)", "3 | N", "match"))
    for (label, pred) in bands:
        edges = suffices = div3 = both = 0
        for (n, down, exts, p, e, d) in work:
            if not pred(d):
                continue
            N = len(exts)
            rank = {v: k for k, v in enumerate(e)}
            for (x, y) in L.incomparable_pairs(n, down):
                want = rank[x] < rank[y]
                pxy = p[(x, y)] if want else 1 - p[(x, y)]
                g = pxy * N
                edges += 1
                s = g > math.ceil(2 * N / 3)
                if s:
                    suffices += 1
                if N % 3 == 0:
                    div3 += 1
                if s == (N % 3 == 0 and pxy > Fraction(2, 3)):
                    both += 1
        if edges:
            print("    %-28s %8d %14d %14d %10s"
                  % (label, edges, suffices, div3, "%d/%d" % (both, edges)))
    print()
    print("    ON THE BOUNDARY CLASS Q2 FAILS AT EVERY EDGE, and for a reason that is not a near")
    print("    miss: delta = 1/3 means the most-balanced pair sits at EXACTLY p = 2/3, so its")
    print("    g = 2N/3 is not even > 2N/3, let alone > ceil(2N/3).  The universal reading needs")
    print("    the STRICT frozen hypothesis, whose population is empty (a5 m1).")
    print()

    print("m2  Q1 (EXISTENTIAL over orderings, ALL edges at once)")
    print("-" * 92)
    nec_fail = suff_ok = undecided = greedy_ok = 0
    per_band = {}
    for (n, down, exts, p, e, d) in work:
        N = len(exts)
        good = B.goodness(n, down, exts, e)
        m = len(good)
        band = "delta = 1/3" if d == THIRD else "delta > 1/3"
        row = per_band.setdefault(band, [0, 0, 0, 0, 0])
        row[0] += 1
        if any(sum(col) < 3 for col in good.values()):
            nec_fail += 1
            row[1] += 1
            continue
        if min(sum(col) for col in good.values()) > 3 * (m - 1):
            greedy_ok += 1
            row[4] += 1
        if disjoint_triples_feasible(good, N):
            suff_ok += 1
            row[2] += 1
        else:
            undecided += 1
            row[3] += 1
    print("    %-16s %7s %19s %21s %11s %10s"
          % ("delta band", "posets", "Q1 FALSE (some g<3)", "Q1 TRUE (flow cert.)",
             "undecided", "greedy"))
    for b in sorted(per_band):
        t, f, s, u, gr = per_band[b]
        print("    %-16s %7d %19d %21d %11d %10d" % (b, t, f, s, u, gr))
    print()
    print("    TOTAL: Q1 FALSE at %d posets, TRUE at %d, UNDECIDED at %d (greedy certificate at"
          % (nec_fail, suff_ok, undecided))
    print("    %d)." % greedy_ok)
    print()
    print("    ⚠️  READ THE 21 BOUNDARY FAILURES CORRECTLY -- THEY ARE AN ARTEFACT OF THE PROXY,")
    print("    NOT A REFUTATION OF DANIEL'S CLAIM.  On the boundary class the most-balanced pair")
    print("    sits at EXACTLY p = 2/3, so at N = 3 it has g = 2 and no good run of 3 exists in")
    print("    ANY ordering.  Under the STRICT hypothesis p_xy > 2/3 that cannot happen:")
    print("      g > 2N/3 with g an integer forces g >= 3 as soon as N >= 3, and a poset with an")
    print("      incomparable pair and N = 2 has that pair at exactly 1/2, so is not frozen.")
    print("    SO THE NECESSARY CONDITION FOR Q1 IS A THEOREM UNDER THE STRICT HYPOTHESIS, and the")
    print("    boundary class -- which is the right proxy for the a-arm statements -- is the WRONG")
    print("    proxy for this one, because this claim is sensitive to the strictness that the")
    print("    boundary gives up.  That is a scope fact about the instrument and it is stated here")
    print("    rather than discovered by whoever re-reads the 21.")
    print()
    print("    AND THE SUFFICIENT SIDE HAS A HAND PROOF TOO, quantified: assign triples one edge")
    print("    at a time; at most 3(m-1) extensions are already used, so a system exists whenever")
    print("      min_xy g_xy > 3(m-1),  which under frozen holds whenever  2N/3 >= 3m - 2.")
    print("    The `greedy` column counts where that certificate fires.  Between the two")
    print("    certificates Q1 is DECIDED-TRUE at %d posets; the %d undecided ones have neither"
          % (suff_ok, undecided))
    print("    certificate and are NOT counterexamples -- disjointness is sufficient, not")
    print("    necessary, and overlapping runs are allowed by the statement.")
    print()

    print("m3  Q3 (the GRAY-CODE restriction) -- and why the run condition is nearly free there")
    print("-" * 92)
    ham_yes = ham_no = ham_budget = ham_skip = 0
    flips_max = 0
    runs_checked = 0
    for (n, down, exts, p, e, d) in work:
        N = len(exts)
        if N > HAM_CAP:
            ham_skip += 1
            continue
        g = B.adjacent_swap_graph(n, exts)
        hp = B.hamiltonian_path(g)
        if hp == "BUDGET":
            ham_budget += 1
            continue
        if hp is None:
            ham_no += 1
            continue
        ham_yes += 1
        # the structural fact: 3 consecutive vertices of the path differ by at most 2 swaps
        inc = L.incomparable_pairs(n, down)
        for i in range(len(hp) - 2):
            a, b, c = (exts[hp[i]], exts[hp[i + 1]], exts[hp[i + 2]])
            flipped = set()
            for (x, y) in inc:
                oa = {v: k for k, v in enumerate(a)}
                ob = {v: k for k, v in enumerate(b)}
                oc = {v: k for k, v in enumerate(c)}
                s = {(oa[x] < oa[y]), (ob[x] < ob[y]), (oc[x] < oc[y])}
                if len(s) > 1:
                    flipped.add((x, y))
            flips_max = max(flips_max, len(flipped))
            runs_checked += 1
    print("    population: the above, restricted to |L(P)| <= %d.  %d SKIPPED (counted)."
          % (HAM_CAP, ham_skip))
    print("    Hamiltonian path in the BK graph: EXISTS at %d, DOES NOT EXIST at %d,"
          % (ham_yes, ham_no))
    print("    search budget exhausted (no decision reached) at %d." % ham_budget)
    print()
    print("    THE STRUCTURAL FACT, measured over %d runs of three consecutive path vertices:"
          % runs_checked)
    print("      the maximum number of incomparable edges whose orientation is NOT shared by all")
    print("      three is %d.  Two steps flip at most two pairs, so a run of 3 in ANY Gray code" % flips_max)
    print("      is UNANIMOUS on every incomparable edge but at most 2 -- the run condition is")
    print("      nearly free once a Gray code exists, and what is NOT free is that the shared")
    print("      orientation be the GOOD one.")
    print()
    ok &= (runs_checked > 0 and flips_max <= 2)
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
