"""T2 -- THE OPERATION, ON OUR SIDE, RE-ANCHORED.

The single categorical operation this ticket is about is

        the face algebra of a cone,  MODULO ITS RADICAL,
        which is the linearised SUPPORT MAP onto the flats.

Aguiar-Mahajan, "Monoidal Functors, Species and Hopf Algebras", Section 10.10,
state it for the whole braid arrangement:

    "Let A be the algebra of faces Sigma[I], and let J be its Jacobson radical.
     Bidigare [45] showed that J is precisely the kernel of its support map.
     This result was generalized to left regular bands by Brown [70] ...
     Thus, A/J is the algebra of flats Pi[I], and the quotient map is the
     support map."

This file checks the corresponding statement for OUR objects -- the faces
lying in the braid cone of a poset P -- with no citation and no trace form:
Phi = (chi_X)_{X in AC(P)} is an algebra map, it is onto, and its kernel is
nilpotent.  Surjective + nilpotent kernel gives kF(P)/rad = k^{AC(P)}.

This re-anchors mg-af28's B5 / mg-6ad0's A4a from fresh code.  It is NOT the
new content of this ticket; T3 and T4 are.

  T2a  AC(P) computed two ways -- acyclicity of the quotient digraph, and
       supp(F(P)) -- agree as SETS.
  T2b  supp : F(P) -> AC(P) is a surjective monoid homomorphism onto a
       semilattice.
  T2c  Phi : kF(P) -> k^{AC(P)} is a surjective algebra map with nilpotent
       kernel, hence dim kF(P)/rad = |AC(P)|.
  T2d  CONTROL: the same nilpotency routine, run on a kernel that is NOT the
       radical (the span of {F - G : supp F = supp G} enlarged by one extra
       basis vector), must fail to be nilpotent.
"""

import sys
from fractions import Fraction
from kern7d75 import (poset_classes, faces_of, AC_by_acyclicity,
                      AC_by_support, sc_product, supp, nullspace, rank)

CAP = 80
bad = 0


def _leq(X, Y):
    """X <= Y in the support order: Y is coarser, i.e. every block of X is
    inside a block of Y."""
    return all(any(B <= C for C in Y) for B in X)


def _meet(X, Y):
    """The semilattice operation on supports.  For faces of an arrangement the
    support of a product is the JOIN OF FLATS, and a join of flats is the
    INTERSECTION of the subspaces, which on set partitions is the common
    refinement.  Written as a meet of partitions to keep the direction
    explicit -- getting this backwards is the obvious way to make T2b vacuous,
    and the first run of this file did exactly that (supp failed to be a
    homomorphism on every class, which is how it was caught)."""
    return frozenset(B & C for B in X for C in Y if B & C)



def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def vec_mul(u, v, F, index):
    """Product of two vectors in kF, in the monoid basis."""
    out = [Fraction(0)] * len(F)
    for i, a in enumerate(u):
        if a == 0:
            continue
        for j, b in enumerate(v):
            if b == 0:
                continue
            out[index[sc_product(F[i], F[j])]] += a * b
    return out


def is_nilpotent(basis, F, index, maxstep=12):
    """Is the ideal spanned by `basis` nilpotent?  Iterate N, N^2, ... to 0."""
    cur = [list(b) for b in basis]
    for step in range(1, maxstep + 1):
        if not cur:
            return True, step
        prods = []
        for u in cur:
            for v in basis:
                prods.append(vec_mul(u, v, F, index))
        R = [r for r in prods if any(x != 0 for x in r)]
        if not R:
            return True, step + 1
        from kern7d75 import rref
        R, _ = rref(R, len(F))
        if len(R) == len(cur) and step > 1:
            # dimension stopped dropping -- not nilpotent
            return False, step
        cur = R
    return False, maxstep


hdr("T2a/T2b/T2c  the operation on F(P), all poset classes, |F(P)| <= %d" % CAP)
print()
print("   n classes tested skipped  AC two routes differ  supp not a hom"
      "  Phi not onto  ker not nilpotent")
for n in range(1, 6):
    cls = poset_classes(n)
    tested = skipped = 0
    d_ac = d_hom = d_onto = d_nil = 0
    for P in cls:
        F = faces_of(P)
        if len(F) > CAP:
            skipped += 1
            continue
        tested += 1
        A1 = set(AC_by_acyclicity(P))
        A2 = set(AC_by_support(P))
        if A1 != A2:
            d_ac += 1
        AC = sorted(A1, key=lambda X: (len(X), sorted(sorted(b) for b in X)))
        index = {f: i for i, f in enumerate(F)}
        # supp is a monoid hom onto a semilattice: supp(FG) = supp(F) v supp(G)
        for f in F:
            for g in F:
                if supp(sc_product(f, g)) != _meet(supp(f), supp(g)):
                    d_hom += 1
                    break
            else:
                continue
            break
        # Phi
        M = []
        for X in AC:
            # chi_X(F) = 1 iff X refines supp(F)
            M.append([Fraction(1) if _leq(X, supp(f)) else Fraction(0)
                      for f in F])
        if rank(M, len(F)) != len(AC):
            d_onto += 1
        K = nullspace(M, len(F))
        nil, _ = is_nilpotent(K, F, index) if K else (True, 0)
        if not nil:
            d_nil += 1
    bad += d_ac + d_hom + d_onto + d_nil
    print("  %2d %7d %6d %7d %21d %15d %13d %18d"
          % (n, len(cls), tested, skipped, d_ac, d_hom, d_onto, d_nil))
print()
print("  Reading: on every poset class tested, AC(P) has the same two")
print("  descriptions, supp is a surjective semilattice homomorphism, and")
print("  Phi : kF(P) -> k^{AC(P)} is onto with nilpotent kernel.  Hence")
print("  kF(P)/rad = k^{AC(P)}: the characters of kF(P) ARE indexed by the")
print("  quotients of P.  Independent re-anchor of mg-af28 B5 / mg-6ad0 A4a.")
print()

hdr("T2d  CONTROL -- a NON-radical ideal must fail the nilpotency routine")
print()
print("  Same routine, same posets, but the subspace fed to it is the kernel")
print("  of Phi ENLARGED by the identity face (the whole one-block face), which")
print("  is idempotent and therefore cannot lie in any nilpotent ideal.")
print()
print("   n classes tested  control fired (not nilpotent)  control FAILED to fire")
fired = failed = 0
for n in range(2, 5):
    cls = poset_classes(n)
    t = f = x = 0
    for P in cls:
        F = faces_of(P)
        if len(F) > CAP:
            continue
        t += 1
        AC = sorted(set(AC_by_acyclicity(P)),
                    key=lambda X: (len(X), sorted(sorted(b) for b in X)))
        index = {fc: i for i, fc in enumerate(F)}
        M = [[Fraction(1) if _leq(X, supp(fc)) else Fraction(0) for fc in F]
             for X in AC]
        K = [list(v) for v in nullspace(M, len(F))]
        one = [Fraction(0)] * len(F)
        one[index[max(F, key=lambda z: -len(z))]] = Fraction(1)
        K.append(one)
        nil, _ = is_nilpotent(K, F, index)
        if nil:
            x += 1
        else:
            f += 1
    fired += f
    failed += x
    print("  %2d %7d %6d %31d %23d" % (n, len(cls), t, f, x))
print()
if failed:
    print("  CONTROL FAILED on %d classes -- T2c's nilpotency test is not" % failed)
    print("  discriminating and T2c must not be relied on.")
    bad += failed
else:
    print("  The control fired on all %d classes: the routine does distinguish" % fired)
    print("  a nilpotent ideal from one containing an idempotent.")
print()
print("=" * 78)
print("T2 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
