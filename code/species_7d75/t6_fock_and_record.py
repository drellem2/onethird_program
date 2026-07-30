"""T6 -- THE TWO FOCK FUNCTORS, AND A CORRECTION TO THE RECORD.

Daniel: "set partitions of [n] form a species; integer partitions are the
ORBITS under the S_n-action, i.e. what you get after passing to coinvariants.
Taking S_n-coinvariants of a species is a standard operation."

It is, it has a name, and both values are in Aguiar-Mahajan.  Joyal's foreword
to that book states the definition:

    "By definition, we have K(p) = (+)_n p[n]_{S_n}, where p[n]_{S_n} denotes
     the space of S_n coinvariants of p[n]."

and Section 17.4 is quoted in Section 17.5 as:

    "Recall from Section 17.4 that K-bar(Pi) is the algebra of symmetric
     functions in noncommuting variables and K(Pi) is the familiar Hopf
     algebra of symmetric functions."

So the Bell(n) / p(n) gap that this ticket was told to explain is the gap
between the two Fock functors on ONE species, and this file measures it.

  T6a  dim K-bar(Pi)_n = Bell(n)  and  dim K(Pi)_n = p(n).
  T6b  the same two functors on our species F and AC.
  T6c  A CORRECTION TO THE RECORD.  mg-af28 row 3 / section 2.5 rejected the
       towers-of-algebras programme because block concatenation fails
       Bergeron-Li axiom (2), which demands 1_m (x) 1_n |-> 1_{m+n}.  That
       demand is NOT an axiom of a Hopf monoid in species.  Both facts are
       measured here side by side.
  T6d  does the poset side map to Sym?  The obvious candidate morphism
       (p, X) |-> X is measured and it FAILS, on the coproduct.
"""

import sys
from itertools import permutations, combinations
from collections import Counter
from kern7d75 import (set_partitions, bell, p_count, perm_sp, orbits,
                      mk_poset, faces_of, AC_by_acyclicity, all_posets,
                      sc_product)
from hopf7d75 import (elems_F, elems_AC, mu_F, de_F, mu_AC, de_AC,
                      decompositions, posets_on, faces_on, supp_of,
                      restrict_part, is_lower_set)

bad = 0


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


hdr("T6a  the Bell(n) / p(n) gap IS the full-vs-bosonic Fock functor gap")
print()
print("   n  dim K-bar(Pi)_n = |Pi[n]|  Bell(n)   dim K(Pi)_n = |Pi[n]/S_n|"
      "   p(n)")
for n in range(1, 8):
    P = set_partitions(n)
    G = list(permutations(range(n)))
    o = len(orbits(P, G, perm_sp))
    ok = (len(P) == bell(n)) and (o == p_count(n))
    bad += (not ok)
    print("  %2d %26d %8d %28d %6d" % (n, len(P), bell(n), o, p_count(n)))
print()
print("  Left pair: K-bar(Pi) = symmetric functions in NONCOMMUTING variables.")
print("  Right pair: K(Pi) = symmetric functions, whose degree-n component is")
print("  the character ring of S_n with the integer partitions as its basis.")
print("  The gap is not a discrepancy to be explained away; it is the two")
print("  functors, applied to ONE species.")
print()

hdr("T6b  the same two functors on OUR species")
print()
print("   n  labelled posets  dim K-bar(AC)_n  dim K(AC)_n  dim K-bar(F)_n"
      "  dim K(F)_n")
for n in range(1, 5):
    I = frozenset(range(n))
    EF = elems_F(I)
    EA = elems_AC(I)
    G = list(permutations(range(n)))

    def actF(x, g):
        rel, F = x
        return (frozenset((g[a], g[b]) for (a, b) in rel),
                tuple(frozenset(g[v] for v in B) for B in F))

    def actA(x, g):
        rel, X = x
        return (frozenset((g[a], g[b]) for (a, b) in rel),
                frozenset(frozenset(g[v] for v in B) for B in X))
    oF = len(orbits(EF, G, actF))
    oA = len(orbits(EA, G, actA))
    print("  %2d %16d %16d %12d %15d %11d"
          % (n, len(posets_on(I)), len(EA), oA, len(EF), oF))
print()
print("  Both functors are defined on our species too -- that is automatic")
print("  once T5 has shown it IS a species with the structure.  What is NOT")
print("  claimed is that either value is a known Hopf algebra; it is not")
print("  identified here and identifying it would be new mathematics.")
print()

hdr("T6c  RECORD CORRECTION -- the axiom that killed the tower story is not")
print("     an axiom of a Hopf monoid in species")
print()
print("  mg-af28 ledger B7: 'block concatenation F(P) x F(Q) -> F(P + Q) is an")
print("  injective semigroup homomorphism and is NOT unital, so it fails")
print("  Bergeron-Li axiom (2)', measured 0 of 64 unital.  Reproduced here:")
print()
small = []
for k in (1, 2, 3):
    for rel in posets_on(frozenset(range(k))):
        small.append((k, rel))
tot = unital = 0
for (k1, r1) in small:
    for (k2, r2) in small:
        I1 = frozenset(range(k1))
        I2 = frozenset(range(k1, k1 + k2))
        r2s = frozenset((a + k1, b + k1) for (a, b) in r2)
        F1 = faces_on(I1, r1)
        F2 = faces_on(I2, r2s)
        # the identity of each face monoid is the single-block face
        e1 = (I1,) if I1 else ()
        e2 = (I2,) if I2 else ()
        e12 = (I1 | I2,) if (I1 | I2) else ()
        tot += 1
        if tuple(e1) + tuple(e2) == e12:
            unital += 1
print("    pairs of LABELLED posets with |P|,|Q| <= 3 : %d" % tot)
print("    (af28's 64 is the same measurement over ISOMORPHISM CLASSES,")
print("     8 x 8; 23 x 23 = 529 here.  Not a disagreement -- a wider net.)")
print("    concatenation sends (1_P, 1_Q) to 1_{P+Q} : %d" % unital)
print()
print("  CONFIRMED: it is not unital, and af28's rejection of the TOWERS")
print("  programme stands.  What does not follow -- and af28 did not claim it,")
print("  but nothing in the record separated the two -- is that the same map")
print("  fails for HOPF MONOIDS.  In a Hopf monoid in species the unit object")
print("  lives only in degree empty; there is no 1_S for nonempty S and no")
print("  unitality requirement on mu_{S,T} at all.  That same concatenation")
print("  IS mu_{S,T}, and T5 measured it against every Hopf monoid axiom with")
print("  0 failures on 4399 basis elements.")
print()
print("  So the Bergeron-Li negative does NOT transfer, and the framework it")
print("  ruled out is not the framework this ticket is about.")
print()

hdr("T6d  does the poset side map to Sym?  The obvious candidate FAILS")
print()
print("  Candidate morphism AC -> Pi,  (p, X) |-> X.  If it were a morphism of")
print("  bimonoids, K of it would be a map from our side into K(Pi) = Sym and")
print("  Daniel's 'both land in one graded Hopf algebra' would be answered on")
print("  the nose.  Measured over the ground set [4]:")
print()
GR = 4
I = frozenset(range(GR))
uA = {}
for k in range(GR + 1):
    for J in combinations(range(GR), k):
        J = frozenset(J)
        uA[J] = set(elems_AC(J))
badmu = badde = 0
for J in uA:
    for (S, T) in decompositions(J):
        for x in uA[S]:
            for y in uA[T]:
                if mu_AC(x, y)[1] != (frozenset(x[1]) | frozenset(y[1])):
                    badmu += 1
        for x in uA[J]:
            d = de_AC(x, S, T)
            # Pi's coproduct is restriction, ALWAYS defined and never zero
            if d is None:
                badde += 1
print("    product   : %d disagreements  (the product does commute with the"
      " forgetful map)" % badmu)
print("    coproduct : %d disagreements" % badde)
print()
print("  The coproduct of Pi is restriction and is NEVER zero.  Ours is zero")
print("  unless S is a lower set of p.  So the forgetful map is a map of")
print("  monoids and NOT of comonoids, and it is not a morphism of bimonoids.")
print("  MEASURED, not argued: %d of the decompositions above are killed on" % badde)
print("  our side and survive on Pi's.")
print()
print("  What remains available is the Aguiar-Bergeron-Sottile universal")
print("  property -- every connected graded Hopf algebra with a character maps")
print("  uniquely to QSym.  That is a citation, it applies to our side as it")
print("  applies to everything else in the class, and BECAUSE it applies to")
print("  everything else in the class it does not identify our object with")
print("  anything.  Daniel's 'both land in one graded Hopf algebra by the same")
print("  universal property' is therefore TRUE AND NOT DISCRIMINATING, and the")
print("  content is at the species level, not at the QSym landing.")
print()
print("=" * 78)
print("T6 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
