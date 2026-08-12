#!/usr/bin/env python3
"""mg-7c78 arm a0 — THE INSTRUMENT IS SHOWN ABLE TO FAIL BEFORE ANY ARM IS BELIEVED.

Four checks, each of which is a way this instrument could return `0 failures` while measuring
nothing:

  c1  THE POPULATION IS THE RIGHT SIZE.  Every arm below counts failures over isomorphism
      classes.  A broken canonical form MERGES classes -- the population shrinks and every
      failure count stays 0.  So the class counts are checked against OEIS A000112
      (1, 2, 5, 16, 63, 318, 2045, 16999), which was computed by someone else.
  c2  E4 FROM PREDICTIONS.md -- "free block" is not assumed to mean "pairwise incomparable".
      For a block of CONSECUTIVE positions in a linear extension, all k! reorderings are linear
      extensions iff the block is pairwise incomparable.  Checked, both directions, k = 2, 3.
  c3  `value_transposition_legal` is checked against BRUTE FORCE -- build the swapped sequence
      and test membership in L(P) -- rather than trusted as a characterisation.
  c4  WRONG-DIRECTION WORLDS.  Three planted defects, each of which must be caught.

Exits 0 if the instrument is sound, 1 if a check fails, 2 if it could not run at all.
"""

import sys
from itertools import permutations

import lib7c78 as L

NMAX_POP = 8
NMAX_LEMMA = 5


def main():
    print("=" * 92)
    print("mg-7c78  a0  the instrument is shown able to fail")
    print("=" * 92)
    print()
    ok = True

    print("c1  POPULATION SIZE -- isomorphism classes against OEIS A000112")
    print("-" * 92)
    classes = L.all_classes(NMAX_POP)
    for n in range(1, NMAX_POP + 1):
        got, want = len(classes[n]), L.A000112[n]
        good = got == want
        ok &= good
        print("    n=%d  classes %6d   A000112 %6d   [%s]"
              % (n, got, want, "PASS" if good else "FAIL"))
    print()

    print("c2  E4 -- a CONSECUTIVE block is fully reorderable iff pairwise incomparable")
    print("-" * 92)
    inst = {2: 0, 3: 0}
    bad = 0
    for n in range(2, NMAX_LEMMA + 1):
        for down in classes[n]:
            exts = set(L.linear_extensions(n, down))
            for e in exts:
                for k in (2, 3):
                    for s in range(n - k + 1):
                        blk = e[s:s + k]
                        allperm = all(e[:s] + p + e[s + k:] in exts
                                      for p in permutations(blk))
                        free = L.free_set(down, blk)
                        inst[k] += 1
                        if allperm != free:
                            bad += 1
    ok &= bad == 0
    print("    k=2 blocks %d · k=3 blocks %d   disagreements %d   [%s]"
          % (inst[2], inst[3], bad, "PASS" if bad == 0 else "FAIL"))
    print("    (n = 2..%d exhaustive over isomorphism classes)" % NMAX_LEMMA)
    print()

    print("c3  `value_transposition_legal` against BRUTE FORCE membership in L(P)")
    print("-" * 92)
    checked = disagree = legal_true = 0
    for n in range(2, NMAX_LEMMA + 1):
        for down in classes[n]:
            exts = L.linear_extensions(n, down)
            eset = set(exts)
            for (x, y) in L.incomparable_pairs(n, down):
                for e in exts:
                    swapped = tuple(y if v == x else (x if v == y else v) for v in e)
                    brute = swapped in eset
                    mine = L.value_transposition_legal(n, down, e, x, y)
                    checked += 1
                    legal_true += 1 if brute else 0
                    if brute != mine:
                        disagree += 1
    ok &= disagree == 0
    print("    %d (poset, pair, extension) instances · %d legal · %d disagreements   [%s]"
          % (checked, legal_true, disagree, "PASS" if disagree == 0 else "FAIL"))
    print("    NON-VACUITY: the event is neither always nor never legal (%d of %d)"
          % (legal_true, checked))
    print()

    print("c4  WRONG-DIRECTION WORLDS -- each planted defect must be CAUGHT")
    print("-" * 92)

    # w1: a canonical form built from a WEAKER invariant (the down-degree multiset alone, which
    # is isomorphism-invariant but far from complete) merges classes -- and c1 is what notices.
    merged = len({tuple(sorted(bin(m).count("1") for m in d)) for d in classes[5]})
    caught1 = merged < len(classes[5])
    ok &= caught1
    print("    w1  a down-degree-only canonical form at n=5 collapses %d classes to %d  [%s]"
          % (len(classes[5]), merged, "CAUGHT by c1" if caught1 else "MISSED"))

    # w2: "pairwise incomparable" replaced by "adjacent pair incomparable" -- must disagree on
    # some 3-block, else c2 would be checking nothing at k = 3.
    n, dn = 3, (0, 1, 0)          # 0 < 1, 2 isolated
    exts = set(L.linear_extensions(n, dn))
    w2 = False
    for e in exts:
        blk = e[0:3]
        weak = not L.comparable(dn, blk[0], blk[1]) and not L.comparable(dn, blk[1], blk[2])
        if weak != L.free_set(dn, blk):
            w2 = True
    ok &= w2
    print("    w2  chain-only incomparability vs pairwise, on a 3-block               [%s]"
          % ("CAUGHT" if w2 else "MISSED"))

    # w3: the adjacency event is a STRICT subset of the value-transposition event -- if it were
    # not, P9 would be F1 rewritten and this instrument would be measuring one thing twice.
    w3 = False
    for n in range(4, 6):
        for down in classes[n]:
            for (x, y) in L.incomparable_pairs(n, down):
                for e in L.linear_extensions(n, down):
                    pos = {v: k for k, v in enumerate(e)}
                    adj = abs(pos[x] - pos[y]) == 1
                    if L.value_transposition_legal(n, down, e, x, y) and not adj:
                        w3 = True
    ok &= w3
    print("    w3  E_xy strictly contains the adjacency event somewhere at n=4,5      [%s]"
          % ("CAUGHT" if w3 else "MISSED -- P9 would be F1 in new notation"))
    print()

    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
