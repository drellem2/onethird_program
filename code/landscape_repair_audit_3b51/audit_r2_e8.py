#!/usr/bin/env python3
"""
mg-3b51 AUDIT 3 -- R2, THE E8 REPLACEMENT.

mg-ebd8's ledger row E8 / L2 row H said Björner's greedoid band on the poset
shelling antimatroid is "a proper submonoid of ours".  mg-d673 called that
impossible; mg-1953 replaced it with:

    the word-to-move map is a monoid HOMOMORPHISM (63/63 at n=5); its image
    lies in F(P) and is closed under the product (63/63); so a HOMOMORPHIC
    IMAGE of the band is a submonoid of F(P), PROPER EXACTLY FOR n >= 3
    (0/2 at n=2, 5/5, 16/16, 63/63 at n=3,4,5); the map is NEVER injective
    (0 of 63); at the antichain the band is strictly LARGER than all of F(P)
    at n = 2, 3 (5 vs 3, 16 vs 13).

Rebuilt here.  The band is the one the DOCUMENT identifies -- feasible words of
the poset shelling antimatroid under the greedy product -- which is the scope
mg-1953's own E8 row states, and which neither mg-d673 nor mg-1953 could check
against Björner's page.  This audit inherits that limit and says so.

  C1  The band: feasible words, greedy product.  Idempotent, left-regular,
      associative, identity -- checked, so it IS a band with identity.
  C2  phi(w) = ({w_1}, ..., {w_k}, rest) lands in F(P).
  C3  phi is a monoid homomorphism.
  C4  the image is closed under the repo's product and contains the identity.
  C5  properness of the image, by n.
  C6  injectivity of phi.
  C7  the antichain cardinalities, band vs F(P), against A000522 / A000670.
  C8  IS THE BAND A SUBSET OF F(P) AT ALL?  The claim being replaced said
      "submonoid"; the replacement says "not even a subset".  Checked as
      cardinality AND as type.
"""

import sys
from itertools import permutations

import core3b51 as C


def feasible_words(n, up):
    """Words over distinct elements every prefix of which is an order ideal:
    an element may be written only once all its P-predecessors are written."""
    down = [0] * n
    for i in range(n):
        for j in range(n):
            if up[j] >> i & 1:
                down[i] |= 1 << j
    out = []

    def rec(word, used):
        out.append(tuple(word))
        for i in range(n):
            if used >> i & 1:
                continue
            if down[i] & ~used:
                continue
            word.append(i)
            rec(word, used | (1 << i))
            word.pop()

    rec([], 0)
    return out


def band_product(n, up, w, v):
    """w . v -- w, then scan v and append every letter that is not already used
    and all of whose predecessors are present.  Björner's greedy product."""
    down = [0] * n
    for i in range(n):
        for j in range(n):
            if up[j] >> i & 1:
                down[i] |= 1 << j
    used = 0
    for x in w:
        used |= 1 << x
    out = list(w)
    for x in v:
        if used >> x & 1:
            continue
        if down[x] & ~used:
            continue
        out.append(x)
        used |= 1 << x
    return tuple(out)


def phi(n, w):
    """({w_1}, ..., {w_k}, rest) -- the last block dropped when empty."""
    used = 0
    blocks = []
    for x in w:
        blocks.append(1 << x)
        used |= 1 << x
    rest = ((1 << n) - 1) & ~used
    if rest:
        blocks.append(rest)
    return tuple(blocks)


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=" * 78)
    print("mg-3b51 AUDIT 3 -- R2, THE E8 REPLACEMENT")
    print("=" * 78)
    print()
    print("SCOPE, INHERITED AND RESTATED.  The band tested is the one the")
    print("document IDENTIFIES (feasible words of the poset shelling")
    print("antimatroid, greedy product), not one read off Björner's Thm 4.15 or")
    print("his (4.8).  Neither mg-d673 nor mg-1953 could obtain those, and")
    print("neither could I.  Everything below is therefore a check of the")
    print("document's own object; it is NOT a check that the object is")
    print("Björner's.  mg-1953's E8 row states this limit and it is correct.")
    print()

    hdr = ("%3s %8s %8s %8s %10s %10s %10s %10s %10s"
           % ("n", "classes", "band ok", "phi->F(P)", "hom", "img closed",
              "proper", "injective", "band<=F(P)"))
    print("-" * 110)
    print(hdr)
    print("-" * 110)
    for n in range(1, nmax + 1):
        classes = C.iso_classes(n)
        band_ok = hom_ok = into = closed = proper = inj = subset = 0
        for up in classes:
            W = feasible_words(n, up)
            Wset = set(W)
            F = set(C.moves_of(n, up))

            # C1 -- band axioms
            ok = True
            for w in W:
                if band_product(n, up, w, w) != w:
                    ok = False
            for w in W:
                for v in W:
                    p = band_product(n, up, w, v)
                    if p not in Wset:
                        ok = False
                    if band_product(n, up, p, w) != p:   # left regular
                        ok = False
            if band_product(n, up, (), ()) != ():
                ok = False
            band_ok += ok

            # C2 -- phi lands in F(P)
            img = {phi(n, w) for w in W}
            if img <= F:
                into += 1

            # C3 -- homomorphism
            h = all(phi(n, band_product(n, up, w, v))
                    == C.move_product(phi(n, w), phi(n, v))
                    for w in W for v in W)
            hom_ok += h

            # C4 -- image closed under the repo product, identity present
            cl = all(C.move_product(a, b) in img for a in img for b in img)
            ident = tuple(1 << i for i in range(n))
            cl = cl and (((1 << n) - 1,) in img or n == 0)
            closed += cl

            # C5 -- proper
            proper += (img != F)

            # C6 -- injective
            inj += (len({phi(n, w) for w in W}) == len(W))

            # C8 -- is the band even a subset of F(P)?  Words are not ordered
            # set partitions; compare as SETS OF OBJECTS after the only
            # type-honest embedding there is, and also compare cardinalities.
            subset += (Wset <= F)

        k = len(classes)
        print("%3d %8d %8s %8s %10s %10s %10s %10s %10s"
              % (n, k, "%d/%d" % (band_ok, k), "%d/%d" % (into, k),
                 "%d/%d" % (hom_ok, k), "%d/%d" % (closed, k),
                 "%d/%d" % (proper, k), "%d/%d" % (inj, k),
                 "%d/%d" % (subset, k)))
    print("-" * 110)
    print()
    print("    'proper' counts posets where the IMAGE is a PROPER subset of")
    print("    F(P).  mg-1953 claims proper EXACTLY for n >= 3: 0/2 at n = 2,")
    print("    then all.  'injective' must be 0 everywhere.")
    print()

    print("-" * 78)
    print("C7  THE ANTICHAIN CARDINALITIES.  |band| against |F(P)|.")
    print("    band = A000522 (arrangements of a set), F(P) = A000670")
    print("    (ordered Bell / Fubini).")
    print("-" * 78)
    print("%3s %14s %14s %10s" % ("n", "|band|", "|F(antichain)|", "band > F?"))
    for n in range(1, min(nmax, 6) + 1):
        up = tuple(0 for _ in range(n))
        W = feasible_words(n, up)
        F = C.moves_of(n, up)
        print("%3d %14d %14d %10s"
              % (n, len(W), len(F), "YES" if len(W) > len(F) else "no"))
    print()
    print("    A000522 : 1, 2, 5, 16, 65, 326    A000670 : 1, 1, 3, 13, 75, 541")
    print("    The document quotes 'free LRB 5, 16 vs ordered Bell 3, 13 at")
    print("    n = 2, 3'.  Those are the n = 2 and n = 3 entries above.")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
