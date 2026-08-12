#!/usr/bin/env python3
"""mg-7c78 arm a4 — THE READING IN WHICH THE `> 2/3` HYPOTHESIS DOES WORK, AND ITS SIGN.

Daniel's phrasing is `"> 2/3 property YIELDS adjacent triples"`.  a1 showed the existential
reading is hypothesis-free.  This arm measures the only statement in the neighbourhood that the
hypothesis DOES constrain -- and its sign is the OPPOSITE one: `> 2/3` makes reversible
configurations RARE, it does not produce them.

  m1  THE S_3 SYMMETRY (P6).  Conditioned on a pairwise-incomparable triple {x,y,z} occupying
      three CONSECUTIVE positions, all 6 orders have EXACTLY equal probability.
      Hand proof: the two adjacent transpositions inside the block generate S_3, and each is a
      swap of an INCOMPARABLE ADJACENT pair -- i.e. exactly `mg-92e6`'s involution.  SO THIS IS
      IMPLIED BY mg-92e6 AND IS NOT INDEPENDENT OF IT.
  m2  THE TRIPLE BUDGET (P8).  Sum over unordered triples of Pr[consecutive] = n-2 EXACTLY --
      the triple analogue of FACTS.md F2's n-1.  And over PAIRWISE-INCOMPARABLE triples only it
      is <= n-2, with the gap taken by triples containing a comparable pair.
  m3  THE JOINT THREE-PAIR CONSTRAINT (P7).  min(p_ab, 1-p_ab) >= (1/2)Pr[{x,y,z} consecutive]
      for ALL THREE pairs of the triple at once.
  m4  THE SHARPEST MEMBER OF THE FAMILY (P9), and the one this arm exists to find:
          min(p_xy, 1-p_xy) >= (1/2) Pr[E_xy],   E_xy = { sigma : sigma o (x y) in L(P) }
      F1 is its k=2 slice (adjacent ==> E_xy) and Daniel's triple is its k=3 slice (free
      consecutive triple containing x,y ==> E_xy).  Measured against both slices to see whether
      it is STRICTLY stronger, i.e. whether there is anything in the family above F1.
  m5  THE STRONG `"ALL ALIGNED WITH e"` READING, REFUTED, AND BY WHAT.  For every incomparable
      pair and every reference order, the e-aligned and e-inverted adjacent occurrences are
      EQUINUMEROUS, and so are the e-aligned and e-inverted members of E_xy.  No hypothesis on
      p_xy can tilt that -- mg-92e6 is what forbids it.

Exits 0 if m1-m5 return the stated counts, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction
from itertools import permutations

import lib7c78 as L

NMAX = 7
SAMPLE_N, SAMPLE_K, SEED = 8, 800, 20260812


def main():
    print("=" * 92)
    print("mg-7c78  a4  the bound family: S_3 symmetry, the triple budget, and E_xy")
    print("=" * 92)
    print()

    classes = L.all_classes(SAMPLE_N)
    import random
    rng = random.Random(SEED)
    pop = [(n, d, True) for n in range(2, NMAX + 1) for d in classes[n]]
    pop += [(SAMPLE_N, d, False) for d in rng.sample(classes[SAMPLE_N], SAMPLE_K)]

    m1_inst = m1_fail = m1_positive = 0
    m2_fail = m2_strict = m2_posets = 0
    m3_inst = m3_fail = 0
    m4_pairs = m4_fail = 0
    m4_strict_over_f1 = m4_strict_over_triple = m4_strict_over_both = 0
    m4_max_prob = Fraction(0)
    m5_pairs = m5_adj_asym = m5_e_asym = 0
    posets = 0

    for (n, down, _exh) in pop:
        inc = L.incomparable_pairs(n, down)
        if not inc:
            continue
        posets += 1
        exts = L.linear_extensions(n, down)
        N = len(exts)
        p = L.pair_probs(n, down, exts)

        # ---- consecutive-triple order counts, keyed by the triple as a frozenset -------------
        tri_order = {}          # frozenset -> {order tuple: count}
        tri_total = {}          # frozenset -> count of consecutive occurrences
        for e in exts:
            for _k, blk in L.consecutive_triples(n, e):
                key = frozenset(blk)
                tri_total[key] = tri_total.get(key, 0) + 1
                if L.free_set(down, blk):
                    tri_order.setdefault(key, {})
                    tri_order[key][blk] = tri_order[key].get(blk, 0) + 1

        # m1: the six orders of a free consecutive triple are equinumerous
        for key, counts in tri_order.items():
            m1_inst += 1
            tot = sum(counts.values())
            if tot > 0:
                m1_positive += 1
                elts = tuple(sorted(key))
                want = Fraction(tot, 6)
                for perm in permutations(elts):
                    if Fraction(counts.get(perm, 0)) != want:
                        m1_fail += 1
                        break

        # m2: the triple budget
        m2_posets += 1
        if n >= 3:
            tot_all = sum(Fraction(v, N) for v in tri_total.values())
            if tot_all != n - 2:
                m2_fail += 1
            tot_free = sum(Fraction(v, N) for k, v in tri_total.items()
                           if L.free_set(down, tuple(k)))
            if tot_free < n - 2:
                m2_strict += 1

        # m3: the joint three-pair constraint
        for key, cnt in tri_total.items():
            elts = sorted(key)
            if not L.free_set(down, tuple(elts)):
                continue
            pr = Fraction(cnt, N)
            m3_inst += 1
            for a in range(3):
                for b in range(a + 1, 3):
                    u, v = elts[a], elts[b]
                    bias = min(p[(u, v)], 1 - p[(u, v)])
                    if bias < pr / 2:
                        m3_fail += 1

        # m4/m5: E_xy, and the two slices it contains
        for (x, y) in inc:
            m4_pairs += 1
            e_cnt = adj_cnt = tri_cnt = 0
            e_fwd = e_rev = adj_fwd = adj_rev = 0
            for e in exts:
                pos = {v: k for k, v in enumerate(e)}
                fwd = pos[x] < pos[y]
                if L.value_transposition_legal(n, down, e, x, y):
                    e_cnt += 1
                    if fwd:
                        e_fwd += 1
                    else:
                        e_rev += 1
                if abs(pos[x] - pos[y]) == 1:
                    adj_cnt += 1
                    if fwd:
                        adj_fwd += 1
                    else:
                        adj_rev += 1
                # x,y inside a FREE consecutive triple
                for _k, blk in L.consecutive_triples(n, e):
                    if x in blk and y in blk and L.free_set(down, blk):
                        tri_cnt += 1
                        break
            bias = min(p[(x, y)], 1 - p[(x, y)])
            pe = Fraction(e_cnt, N)
            pa = Fraction(adj_cnt, N)
            pt = Fraction(tri_cnt, N)
            if bias < pe / 2:
                m4_fail += 1
            if pe > m4_max_prob:
                m4_max_prob = pe
            if pe > pa:
                m4_strict_over_f1 += 1
            if pe > pt:
                m4_strict_over_triple += 1
            if pe > max(pa, pt):
                m4_strict_over_both += 1
            m5_pairs += 1
            if adj_fwd != adj_rev:
                m5_adj_asym += 1
            if e_fwd != e_rev:
                m5_e_asym += 1

    ok = (m1_fail == 0 and m2_fail == 0 and m3_fail == 0 and m4_fail == 0
          and m5_adj_asym == 0 and m5_e_asym == 0
          and m1_positive > 0 and m2_strict > 0 and m4_strict_over_both > 0)

    print("POPULATION.  n = 2..%d EXHAUSTIVE over isomorphism classes, plus n = %d SAMPLED %d of"
          % (NMAX, SAMPLE_N, SAMPLE_K))
    print("  %d (seed %d).  %d posets · %d incomparable pairs.  EXACT RATIONALS THROUGHOUT."
          % (len(classes[SAMPLE_N]), SEED, posets, m4_pairs))
    print()

    print("m1  the 6 orders of a FREE CONSECUTIVE TRIPLE are equinumerous (exactly)")
    print("-" * 92)
    print("    %d free triples examined, %d with POSITIVE consecutive probability, %d failures  [%s]"
          % (m1_inst, m1_positive, m1_fail, "PASS" if m1_fail == 0 else "FAIL"))
    print("    IMPLIED BY mg-92e6: the two adjacent swaps inside the block generate S_3 and each")
    print("    is a swap of an incomparable adjacent pair.  NOT an independent fact.")
    print()

    print("m2  THE TRIPLE BUDGET -- sum over ALL triples of Pr[consecutive] = n-2 exactly")
    print("-" * 92)
    print("    %d posets, %d violations of the identity   [%s]"
          % (m2_posets, m2_fail, "PASS" if m2_fail == 0 else "FAIL"))
    print("    over PAIRWISE-INCOMPARABLE triples only it is <= n-2, STRICT at %d of %d posets"
          % (m2_strict, m2_posets))
    print("    -- so quoting `= n-2` with the population dropped is the F2 error class again.")
    print()

    print("m3  THE JOINT THREE-PAIR CONSTRAINT  min(p,1-p) >= (1/2)Pr[triple consecutive]")
    print("-" * 92)
    print("    %d (triple, pair) instances, %d failures   [%s]"
          % (m3_inst * 3, m3_fail, "PASS" if m3_fail == 0 else "FAIL"))
    print()

    print("m4  THE SHARPEST MEMBER  min(p_xy,1-p_xy) >= (1/2)Pr[E_xy]")
    print("-" * 92)
    print("    %d pairs, %d failures   [%s]   max Pr[E_xy] observed = %s"
          % (m4_pairs, m4_fail, "PASS" if m4_fail == 0 else "FAIL", m4_max_prob))
    print("    STRICTLY STRONGER THAN ITS SLICES, measured:")
    print("      Pr[E_xy] > Pr[adjacent]        (i.e. beats F1's event)        at %d of %d pairs"
          % (m4_strict_over_f1, m4_pairs))
    print("      Pr[E_xy] > Pr[in a free triple] (i.e. beats Daniel's event)   at %d of %d pairs"
          % (m4_strict_over_triple, m4_pairs))
    print("      Pr[E_xy] > BOTH at once                                       at %d of %d pairs"
          % (m4_strict_over_both, m4_pairs))
    print("    So the triple is one rung of a ladder, not the top of it: the k=2 rung is F1, the")
    print("    k=3 rung is Daniel's, and E_xy is the union of every rung.")
    print()

    print("m5  THE STRONG `\"ALL ALIGNED WITH e\"` READING IS REFUTED, AND mg-92e6 IS THE REFUTER")
    print("-" * 92)
    print("    pairs whose ADJACENT occurrences split unevenly between the two orders: %d of %d"
          % (m5_adj_asym, m5_pairs))
    print("    pairs whose E_xy occurrences split unevenly between the two orders:     %d of %d"
          % (m5_e_asym, m5_pairs))
    print("    BOTH ZERO, at every poset in the population -- INCLUDING every biased pair.")
    print("    A configuration on which the x/y order can be reversed carries NO bias at all, so")
    print("    no hypothesis on p_xy, `> 2/3` or otherwise, can make these configurations prefer")
    print("    e.  THE HYPOTHESIS ACTS WITH THE OPPOSITE SIGN: it CAPS Pr[E_xy] at 2*delta, it")
    print("    does not produce e-aligned occurrences.")
    print()
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
