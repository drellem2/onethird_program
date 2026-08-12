#!/usr/bin/env python3
"""mg-7c78 arm a3 — READING R4: bias away from 1/2 FORCES a distinguishing third element.

R4 is the only reading in which the `> 2/3` hypothesis does real work, so it is the one that has
to be checked hardest.

  m1  THE FORWARD DIRECTION.  For every poset and every incomparable pair {x,y} with
      p_xy != 1/2, is there a z (z != x, y) comparable to exactly ONE of x, y?
      Hand proof: if no such z exists then every z is comparable to BOTH or NEITHER; a z
      comparable to both must lie on the same side of both (a z with y < z < x would force
      y < x, contradicting x || y), so exchanging x and y is an automorphism of P, hence a
      measure-preserving involution of L(P), hence p_xy = 1/2.
  m2  THE AUTOMORPHISM ITSELF, checked directly rather than inferred: at every pair with NO
      distinguishing z, the value-transposition (x y) is verified to map L(P) onto L(P).
  m3  THE CONVERSE, which must FAIL for R4 to be a one-way implication rather than a
      characterisation: pairs that HAVE a distinguishing z and still sit at p = 1/2 exactly.
  m4  THE NO-3-CYCLE ANCHOR, re-derived here and not read: over pairwise-incomparable triples,
      at most two of the three cyclic events can exceed 2/3, and the sum of the three
      "before" probabilities around a cycle is <= 2.

Exits 0 if m1 has 0 failures, m2 has 0 failures and m3 is NON-EMPTY (a converse that never
fails would mean m3 is measuring nothing); 1 otherwise; 2 on refusal.
"""

import sys
from fractions import Fraction

import lib7c78 as L

NMAX = 7
SAMPLE_N, SAMPLE_K, SEED = 8, 800, 20260812
HALF = Fraction(1, 2)


def distinguishers(n, down, x, y):
    """The z != x, y comparable to exactly one of x, y."""
    return [z for z in range(n) if z not in (x, y)
            and (L.comparable(down, z, x) != L.comparable(down, z, y))]


def main():
    print("=" * 92)
    print("mg-7c78  a3  READING R4 -- bias != 1/2 forces a distinguishing third element")
    print("=" * 92)
    print()

    classes = L.all_classes(SAMPLE_N)
    import random
    rng = random.Random(SEED)
    pop = [(n, d, True) for n in range(2, NMAX + 1) for d in classes[n]]
    pop += [(SAMPLE_N, d, False) for d in rng.sample(classes[SAMPLE_N], SAMPLE_K)]

    pairs = biased = 0
    m1_fail = 0
    m2_checked = m2_fail = 0
    m3_hits = m3_total_with_z = 0
    m3_witness = None
    triples = m4_fail = 0
    m4_over23 = {0: 0, 1: 0, 2: 0, 3: 0}
    posets = 0

    for (n, down, _exh) in pop:
        inc = L.incomparable_pairs(n, down)
        if not inc:
            continue
        posets += 1
        exts = L.linear_extensions(n, down)
        eset = set(exts)
        p = L.pair_probs(n, down, exts)

        for (x, y) in inc:
            pairs += 1
            pz = distinguishers(n, down, x, y)
            pxy = p[(x, y)]
            if pxy != HALF:
                biased += 1
                if not pz:
                    m1_fail += 1
            else:
                if pz:
                    m3_total_with_z += 1
                    m3_hits += 1
                    if m3_witness is None:
                        m3_witness = (n, list(down), x, y, pz)
            if not pz:
                # m2: the transposition must be an automorphism, so it must permute L(P)
                m2_checked += 1
                for e in exts:
                    sw = tuple(y if v == x else (x if v == y else v) for v in e)
                    if sw not in eset:
                        m2_fail += 1
                        break

        # m4: the no-3-cycle anchor
        for a in range(n):
            for b in range(a + 1, n):
                for c in range(b + 1, n):
                    if not L.free_set(down, (a, b, c)):
                        continue
                    triples += 1
                    # the cyclic orientation a<b, b<c, c<a
                    cyc = [p[(a, b)], p[(b, c)], 1 - p[(a, c)]]
                    if sum(cyc) > 2:
                        m4_fail += 1
                    k = sum(1 for v in cyc if v > Fraction(2, 3))
                    m4_over23[k] = m4_over23.get(k, 0) + 1

    ok = (m1_fail == 0 and m2_fail == 0 and m3_hits > 0 and m4_fail == 0
          and m4_over23.get(3, 0) == 0)

    print("POPULATION.  n = 2..%d EXHAUSTIVE over isomorphism classes, plus n = %d SAMPLED %d of"
          % (NMAX, SAMPLE_N, SAMPLE_K))
    print("  %d (seed %d).  %d posets · %d incomparable pairs · %d pairwise-incomparable triples."
          % (len(classes[SAMPLE_N]), SEED, posets, pairs, triples))
    print()

    print("m1  p_xy != 1/2  ==>  a distinguishing z EXISTS")
    print("-" * 92)
    print("    biased pairs %d of %d   failures %d   [%s]"
          % (biased, pairs, m1_fail, "PASS" if m1_fail == 0 else "FAIL"))
    print("    NON-VACUITY: %d of the %d pairs are biased, so the hypothesis is not empty."
          % (biased, pairs))
    print()

    print("m2  where NO distinguishing z exists, (x y) is verified to be an automorphism of L(P)")
    print("-" * 92)
    print("    pairs with no distinguisher %d   L(P) not preserved at %d   [%s]"
          % (m2_checked, m2_fail, "PASS" if m2_fail == 0 else "FAIL"))
    print()

    print("m3  THE CONVERSE FAILS -- a distinguishing z does NOT force bias")
    print("-" * 92)
    print("    pairs at p = 1/2 EXACTLY that nevertheless HAVE a distinguishing z: %d   [%s]"
          % (m3_hits, "PASS (converse refuted)" if m3_hits else "FAIL -- m3 measures nothing"))
    if m3_witness:
        n, dn, x, y, pz = m3_witness
        print("    smallest witness: n=%d down-masks %s, pair (%d,%d), distinguishers %s, p = 1/2"
              % (n, dn, x, y, pz))
        print("    So R4 is a ONE-WAY implication: the third element is FORCED by bias, but its")
        print("    presence does NOT produce bias -- a larger symmetry can cancel it.")
    print()

    print("m4  THE NO-3-CYCLE ANCHOR, re-derived on this instrument")
    print("-" * 92)
    print("    triples with cyclic sum > 2: %d of %d   [%s]"
          % (m4_fail, triples, "PASS" if m4_fail == 0 else "FAIL"))
    print("    how many of the three cyclic events exceed 2/3:")
    for k in sorted(m4_over23):
        print("       %d of 3 : %8d triples%s" % (k, m4_over23[k],
              "   <-- MUST BE 0" if k == 3 else ""))
    print()
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
