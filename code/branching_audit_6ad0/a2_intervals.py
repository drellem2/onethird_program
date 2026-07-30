"""A2 -- REFUTATION BY CONSTRUCTION of mg-af28's ledger row B2, and of the
sentence in its section 0 consequence 3 that depends on the same conflation.

WHAT mg-af28 CLAIMS

  B2 (ledger, marked MEASURED + CITED):
      "the posets P for which J(P) is an interval of Young's lattice are
       exactly the cell posets, and they are a vanishing fraction:
       6/318 (n=6), 8/2 045 (n=7), 12/16 999 (n=8)"

  t_young.py T2 header, and out_young.txt lines 68-70, say the same:
      "The posets P for which J(P) is an interval of Young's lattice are
       exactly the cell posets D_lambda."

  section 0 consequence 3:
      "that grid is J(C_p + C_q), which for p, q >= 1 is NOT an interval of
       Young's lattice -- D_lambda has a minimum and C_p + C_q does not."

WHAT IS ACTUALLY TRUE

  An interval [mu, lambda] of Young's lattice is the set of partitions nu with
  mu <= nu <= lambda.  Under "nu -> the cells of nu/mu", it is the ideal lattice
  of the SKEW cell poset lambda/mu.  So

      {P : J(P) is an interval of Young's lattice} = {skew cell posets}

  which STRICTLY contains the straight cell posets.  af28's own measurement (T2)
  only ever counts straight cell posets D_lambda -- it never tests the "exactly"
  at all.  The reason offered in consequence 3 ("D_lambda has a minimum") only
  rules out intervals of the special form [0, lambda]; a general interval's
  poset need not have a minimum, and the grid's does not.

WHAT THIS FILE DOES

  A2a  Exhibits the smallest witness explicitly: the 2-element ANTICHAIN is not
       a cell poset, yet J(2-antichain) = the diamond = the interval
       [(1), (2,1)] of Young's lattice.  Both sides printed.

  A2b  Exhibits, for every p, q >= 1 in range, an EXPLICIT interval of Young's
       lattice isomorphic to Brown section 4.3's own example lattice
       {0..p} x {0..q} = J(C_p + C_q) -- refuting consequence 3's sentence by
       construction rather than by argument.

  A2c  Recomputes the "vanishing fraction" over the CORRECT class (skew cell
       posets) and prints both columns side by side, so the reader can see
       which part of consequence 1 survives and which does not.
"""

import sys
from kern6ad0 import (partitions, contains, straight_poset, skew_poset, canon,
                      ideals, all_posets, mk_poset, poset_of_ideals, leq,
                      is_lattice_and_distributive, linear_extensions)

OUT = sys.stdout


def young_interval(mu, lam):
    """[mu, lambda] as a list of partitions, by containment on both sides."""
    n = sum(lam)
    out = []
    for m in range(sum(mu), n + 1):
        for nu in (partitions(m) if m else [()]):
            if contains(mu, nu) and contains(nu, lam):
                out.append(nu)
    return out


def chain(k):
    return mk_poset(k, [(i, i + 1) for i in range(k - 1)])


def disjoint(P, Q):
    n, dn = P
    m, dm = Q
    pairs = []
    for i in range(n):
        for j in dn[i]:
            pairs.append((j, i))
    for i in range(m):
        for j in dm[i]:
            pairs.append((j + n, i + n))
    return mk_poset(n + m, pairs)


def trimmed_skew_shapes(n, box=None):
    """Every skew cell poset with n cells, up to isomorphism.

    Any skew diagram with n cells has, after deleting its empty rows and empty
    columns (both operations produce another skew diagram with the same cell
    poset), at most n rows and at most n columns.  So enumerating lambda inside
    the n x n box, with mu contained in lambda and |lambda| - |mu| = n, reaches
    every isomorphism class.
    """
    b = box if box is not None else n
    lams = [l for m in range(0, b * b + 1) for l in (partitions(m) if m else [()])
            if len(l) <= b and (not l or l[0] <= b)]
    seen = {}
    for lam in lams:
        target = sum(lam) - n
        if target < 0:
            continue
        for mu in (partitions(target) if target else [()]):
            if not contains(mu, lam):
                continue
            P, cs = skew_poset(lam, mu)
            if P[0] != n:
                continue
            seen.setdefault(canon(P), (lam, mu, P))
    return seen


def main():
    a000112 = {1: 1, 2: 2, 3: 5, 4: 16, 5: 63, 6: 318, 7: 2045, 8: 16999}

    print("=" * 78, file=OUT)
    print("A2a  THE SMALLEST WITNESS.  B2 says the posets P with J(P) an interval", file=OUT)
    print("     of Young's lattice are EXACTLY the cell posets.  Here is one that", file=OUT)
    print("     is not a cell poset.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    A2 = mk_poset(2, [])                      # the 2-element antichain
    JA = ideals(A2)
    print("  P = the 2-element ANTICHAIN.", file=OUT)
    print("    J(P) has %d elements: %s"
          % (len(JA), [sorted(x) for x in JA]), file=OUT)
    cellcanons = {canon(straight_poset(l)[0]): l for l in partitions(2)}
    print("    2-cell straight shapes: %s -- their posets are %s"
          % ([str(l) for l in partitions(2)],
             "both the 2-CHAIN" if len(cellcanons) == 1 else "distinct"), file=OUT)
    print("    is P a cell poset D_lambda?  %s"
          % ("YES" if canon(A2) in cellcanons else "NO"), file=OUT)
    iv = young_interval((1,), (2, 1))
    print("    the Young-lattice interval [(1), (2,1)] = %s   (%d elements)"
          % ([str(x) for x in iv], len(iv)), file=OUT)
    Q, cs = skew_poset((2, 1), (1,))
    same = canon(Q) == canon(A2)
    print("    the skew cell poset (2,1)/(1) has cells %s and is isomorphic to"
          % cs, file=OUT)
    print("    the 2-element antichain: %s" % ("YES" if same else "NO"), file=OUT)
    # and J of it really is that interval, as a poset
    JQ, _ = poset_of_ideals(Q)
    ivp = mk_poset(len(iv), [(i, j) for i in range(len(iv)) for j in range(len(iv))
                             if iv[i] != iv[j] and contains(iv[i], iv[j])])
    print("    J((2,1)/(1)) is isomorphic to the interval as a poset: %s"
          % ("YES" if canon(JQ) == canon(ivp) else "NO"), file=OUT)
    print(file=OUT)
    print("  CONCLUSION A2a: B2's word \"exactly\" is FALSE.  The 2-element", file=OUT)
    print("  antichain is not a cell poset and J(antichain_2) IS an interval of", file=OUT)
    print("  Young's lattice.  The correct class is the SKEW cell posets.", file=OUT)
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("A2b  BROWN'S OWN EXAMPLE.  section 0 consequence 3 says the p x q grid,", file=OUT)
    print("     = J(C_p + C_q), is NOT an interval of Young's lattice for", file=OUT)
    print("     p,q >= 1.  Here is the interval, for each p,q.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   p  q   witness lambda / mu           |[mu,lam]|  (p+1)(q+1)  poset iso", file=OUT)
    bad = 0
    for p in range(1, 5):
        for q in range(1, 5):
            # lambda = (q + p, q), mu = (q,) : row 0 keeps columns q..q+p-1,
            # row 1 keeps columns 0..q-1; the two blocks are incomparable.
            lam = (q + p, q)
            mu = (q,)
            P, cs = skew_poset(lam, mu)
            target = disjoint(chain(p), chain(q))
            iso = (canon(P) == canon(target))
            iv = young_interval(mu, lam)
            szok = (len(iv) == (p + 1) * (q + 1))
            if not (iso and szok):
                bad += 1
            print("  %2d %2d   %-24s %10d  %10d  %s"
                  % (p, q, "%s / %s" % (str(lam), str(mu)), len(iv),
                     (p + 1) * (q + 1), "." if (iso and szok) else "BAD"), file=OUT)
    print(file=OUT)
    print("  CONCLUSION A2b: %s" % (
        "REFUTED BY CONSTRUCTION -- for every p,q tested, C_p + C_q IS the cell\n"
        "  poset of the skew shape (q+p, q)/(q), so the grid J(C_p + C_q) IS the\n"
        "  Young-lattice interval [(q), (q+p, q)].  The reason offered in\n"
        "  consequence 3 (\"D_lambda has a minimum\") rules out only intervals of\n"
        "  the form [0, lambda], which is not what the sentence claims."
        if bad == 0 else "witness construction FAILED in %d cases" % bad), file=OUT)
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("A2c  THE CORRECTED COUNT.  Consequence 1 says the overlap is a", file=OUT)
    print("     vanishing fraction 6/318, 8/2045, 12/16999.  Those are counts of", file=OUT)
    print("     STRAIGHT cell posets.  Here is the count over the class B2", file=OUT)
    print("     actually names.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    import os
    top = 8 if os.environ.get("SKEW8") else 7
    print("   n   straight D_lam   skew (= interval posets)   all posets   af28  corrected",
          file=OUT)
    for n in range(1, top + 1):
        straight = {canon(straight_poset(l)[0]) for l in partitions(n)}
        skew = trimmed_skew_shapes(n)
        tot = a000112[n]
        assert straight <= set(skew), "straight shapes must be skew shapes"
        print("  %2d   %14d   %23d   %10d   %6.4f  %8.4f"
              % (n, len(straight), len(skew), tot,
                 len(straight) / tot, len(skew) / tot), file=OUT)
    print(file=OUT)
    if top < 8:
        print("   8 is behind a flag because it takes ~4 minutes: run with SKEW8=1.", file=OUT)
        print("   Its value, computed by this same function: straight 12 (af28's", file=OUT)
        print("   number, reproduced), skew 360, of 16 999 -- 0.0007 against 0.0212.", file=OUT)
        print(file=OUT)
    print("  Both columns vanish, so consequence 1's DIRECTION (\"ours contains", file=OUT)
    print("  theirs, as a vanishing fraction\") survives.  What does not survive", file=OUT)
    print("  is B2's identification of the class, and the three numbers, which", file=OUT)
    print("  are the counts of a strictly smaller family than the one named.", file=OUT)
    print(file=OUT)

    print("=" * 78, file=OUT)
    print("A2d  IS THE CORRECTION MATERIAL?  Skew shapes are not a technicality", file=OUT)
    print("     of the branching-graph programme -- intervals [mu, lambda] index", file=OUT)
    print("     the SKEW standard tableaux, which are the paths of the same", file=OUT)
    print("     branching graph starting at mu instead of at the empty shape.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   lambda/mu       cells   e(skew poset)   #paths mu->lambda in Young", file=OUT)
    bad2 = 0
    for (lam, mu) in [((2, 1), (1,)), ((3, 1), (1,)), ((2, 2), (1,)),
                      ((3, 2), (2,)), ((3, 2, 1), (2, 1)), ((4, 2), (2, 1)),
                      ((3, 3), (1, 1))]:
        P, cs = skew_poset(lam, mu)
        e = len(linear_extensions(P))
        iv = young_interval(mu, lam)
        # count saturated chains mu -> lambda inside the interval
        cnt = {mu: 1}
        for nu in sorted(iv, key=lambda x: sum(x)):
            if nu == mu:
                continue
            cnt[nu] = sum(cnt.get(rho, 0) for rho in iv
                          if sum(rho) == sum(nu) - 1 and contains(rho, nu))
        if e != cnt[lam]:
            bad2 += 1
        print("   %-14s %5d   %13d   %24d"
              % ("%s/%s" % (str(lam), str(mu)), P[0], e, cnt[lam]), file=OUT)
    print(file=OUT)
    print("  linear extensions of the skew cell poset = paths mu -> lambda: %d bad"
          % bad2, file=OUT)
    print(file=OUT)
    return bad, bad2


if __name__ == "__main__":
    b, b2 = main()
    print("=" * 78, file=OUT)
    print("SUMMARY a2_intervals: witness constructions bad %d; skew-path check bad %d"
          % (b, b2), file=OUT)
    print("=" * 78, file=OUT)
