"""T2 --- the SEMISIMPLE, NON-MULTIPLICITY-FREE object, BUILT.

The other half of the load-bearing question.  T1 held the branching fixed and
switched semisimplicity off.  This script holds semisimplicity fixed and
switches multiplicity-freeness off, and measures what breaks.

The statement being tested against our objects is Okounkov-Vershik's, quoted
verbatim in t4_quotes.py:

  * "the fundamental isomorphism  C[G(n)] = sum_lambda End(V^lambda)"   (1.4)
  * "If the branching is simple, the decomposition ... is canonical"
  * Remark 1.3: "For an arbitrary inductive family of semisimple algebras, the
    GZ-subalgebra is a maximal commutative subalgebra if and only if the
    branching graph has no multiple edges."
  * Prop. 1.4: restriction has simple multiplicities <=> the centralizer
    Z(M, N) is commutative.

Everything below is computed inside C[S_n] over Q from permutations, and
inside an explicitly built matrix algebra.  No character table is used.
"""

import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kerndb09 import (MonAlg, group_algebra, class_sums, sym_group, embed,
                      algebra_generated, centralizer, is_commutative_subspace,
                      rank)

BAD = 0


def bad(msg):
    global BAD
    BAD += 1
    print("  BAD: " + msg)


def involutions(n):
    a = [1, 1]
    for k in range(2, n + 1):
        a.append(a[k - 1] + (k - 1) * a[k - 2])
    return a[n]


def gz(n, chain):
    A = group_algebra(n)
    idx = {g: i for i, g in enumerate(A.basis)}
    gens = []
    for k in chain:
        gens.extend(class_sums(k, n, idx))
    return A, algebra_generated(A, gens)


print("=" * 74)
print("T2a  POSITIVE CONTROL --- the full symmetric group tower")
print("=" * 74)
print("The number of paths from the root to level n in the branching graph is")
print("sum_lambda f^lambda = the number of involutions in S_n.  Okounkov-")
print("Vershik Prop. 1.1: GZ(n) is the algebra of operators diagonal in the")
print("Gelfand-Tsetlin basis, hence has that dimension and is MAXIMAL")
print("commutative.")
print()
print("%3s %10s %14s %18s %10s" %
      ("n", "dim GZ(n)", "# involutions", "dim centralizer", "maximal?"))
for n in range(1, 6):
    A, B = gz(n, list(range(1, n + 1)))
    C = centralizer(A, B)
    comm = is_commutative_subspace(A, B)
    inv = involutions(n)
    print("%3s %10d %14d %18d %10s" %
          (n, len(B), inv, len(C), "yes" if len(C) == len(B) else "NO"))
    if len(B) != inv:
        bad("dim GZ(%d) = %d, expected %d" % (n, len(B), inv))
    if not comm:
        bad("GZ(%d) is not commutative" % n)
    if len(C) != len(B):
        bad("GZ(%d) is not maximal commutative" % n)

print()
print("=" * 74)
print("T2b  MULTIPLICITY-FREENESS SWITCHED OFF, SEMISIMPLICITY KEPT")
print("=" * 74)
print("Same algebra C[S_4] --- still semisimple, still a sum of endomorphism")
print("algebras --- but the chain has a level removed, so the branching is no")
print("longer multiplicity-free.  Okounkov-Vershik Remark 1.3 predicts the GZ")
print("algebra stops being maximal commutative, and that is what is measured.")
print()
print("%-22s %10s %12s %16s %12s" %
      ("chain", "dim GZ", "# paths", "dim centralizer", "maximal?"))
for n, chain in [(4, [1, 2, 3, 4]), (4, [1, 2, 4]), (4, [1, 3, 4]), (4, [1, 4]),
                 (5, [1, 2, 3, 4, 5]), (5, [1, 2, 3, 5])]:
    A, B = gz(n, chain)
    C = centralizer(A, B)
    npaths = involutions(n)
    print("%-22s %10d %12d %16d %12s" %
          ("S_" + " < S_".join(str(k) for k in chain), len(B), npaths, len(C),
           "yes" if len(C) == len(B) else "NO"))
    full = (chain == list(range(1, n + 1)))
    if full and len(B) != npaths:
        bad("full chain at n=%d lost paths" % n)
    if (not full) and len(B) >= npaths:
        bad("skipped chain at n=%d, chain %s: dim GZ = %d not < %d"
            % (n, chain, len(B), npaths))
print()
print("  Every skipped chain has dim GZ strictly below the number of paths,")
print("  and is not maximal commutative.  The GELFAND-TSETLIN BASIS is what")
print("  multiplicity-freeness buys, and it is what is lost.")

print()
print("=" * 74)
print("T2c  Okounkov-Vershik Prop. 1.4, tested as an equality")
print("=" * 74)
print("'restriction from M to N has simple multiplicities  <=>  Z(M,N) is")
print("commutative'.  Adjacent steps of the symmetric group tower are the")
print("multiplicity-free case; skipping a level is not.")
print()
print("%-20s %10s %16s" % ("pair", "dim Z(M,N)", "commutative?"))
for n, k in [(3, 2), (4, 3), (5, 4), (4, 2), (5, 3), (5, 2)]:
    A = group_algebra(n)
    idx = {g: i for i, g in enumerate(A.basis)}
    sub = []
    for p in sym_group(k):
        v = [Fraction(0)] * A.dim
        v[idx[embed(p, k, n)]] = Fraction(1)
        sub.append(v)
    Z = centralizer(A, sub)
    c = is_commutative_subspace(A, Z)
    adj = (k == n - 1)
    print("%-20s %10d %16s   %s" %
          ("Z(CS_%d, CS_%d)" % (n, k), len(Z), "yes" if c else "NO",
           "adjacent" if adj else "level(s) skipped"))
    if adj and not c:
        bad("adjacent pair (%d,%d) gave a non-commutative centralizer" % (n, k))
    if (not adj) and c:
        bad("skipped pair (%d,%d) gave a commutative centralizer" % (n, k))

print()
print("=" * 74)
print("T2d  THE CONCLUSION SURVIVES ANYWAY --- sum_lambda End(V_lambda) holds")
print("=" * 74)
print("C[S_4] is semisimple whatever chain is drawn through it, so Wedderburn")
print("still gives C[S_4] = sum_lambda End(V^lambda).  Measured: the radical")
print("is zero, and the dimension is a sum of squares of the irreducible")
print("dimensions 1,1,2,3,3.")
A = group_algebra(4)
R = A.radical()
isideal, isnilp, _ = A.verify_radical(R)
print("  dim C[S_4] = %d, dim rad = %d, 1+1+4+9+9 = %d"
      % (A.dim, len(R), 1 + 1 + 4 + 9 + 9))
if len(R) != 0:
    bad("C[S_4] has a radical")
if A.dim != 24:
    bad("dim C[S_4] != 24")

print()
print("  And the minimal witness, with no group in sight: C inside M_2(C).")
print("  The unique simple of M_2 restricts to 2 copies of the simple of C, so")
print("  the Bratteli diagram has a DOUBLE EDGE.")
els = [(i, j) for i in range(2) for j in range(2)]
M2 = MonAlg.from_monoid(els, lambda x, y: (x[0], y[1]) if x[1] == y[0] else None,
                        name="M_2")
one = [Fraction(1), Fraction(0), Fraction(0), Fraction(1)]
centre_bottom = [one]          # Z(C . 1) = span(1)
centre_top = [one]             # Z(M_2)   = span(1)
GZ = algebra_generated(M2, centre_bottom + centre_top)
Cz = centralizer(M2, GZ)
R2 = M2.radical()
print("  dim M_2 = %d, dim rad = %d  ->  M_2 = End(V), V of dimension 2"
      % (M2.dim, len(R2)))
print("  # paths from the root to the top vertex = 2")
print("  dim GZ = %d  (< 2), dim centralizer of GZ = %d  -> NOT maximal commutative"
      % (len(GZ), len(Cz)))
if len(R2) != 0:
    bad("M_2 has a radical")
if len(GZ) != 1:
    bad("dim GZ(M_2 tower) = %d, expected 1" % len(GZ))
if len(Cz) == len(GZ):
    bad("GZ of the M_2 tower came out maximal commutative")

print()
print("=" * 74)
print("T2e  THE VERDICT")
print("=" * 74)
print("Dropping multiplicity-freeness costs the CANONICAL BASIS and nothing")
print("else: the algebra is still a direct sum of endomorphism algebras, and")
print("paths still index a basis of each irreducible --- but the path basis is")
print("no longer determined, because GZ is no longer maximal commutative and")
print("the decomposition into irreducibles of the smaller algebra involves a")
print("choice of splitting of a multiplicity space.")
print()
print("Dropping semisimplicity costs the CONCLUSION (T1).  The two hypotheses")
print("are not on a par.")

print()
print("TOTAL BAD: %d" % BAD)
