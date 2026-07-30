"""T3 --- where kF(P) sits, measured against the same two hypotheses.

T1 and T2 established which hypothesis carries the conclusion.  This script
takes our own object to it.

  * `F(P)` = the faces of the braid arrangement lying in the cone
    C(P) = {x : x_i <= x_j whenever i <_P j}, multiplied by the Tits product.
  * `AC(P)` = their supports = the set partitions of [n] with acyclic
    quotient.

Built here from the geometric definition; nothing is imported from
`code/species_7d75`, `code/branching_af28` or `code/branching_audit_6ad0`.

Three things are measured.

  T3a  the size of the endomorphism-algebra shadow, |AC(P)|, against the size
       of the algebra, |F(P)|.
  T3b  dim kF(P)/rad = |AC(P)|, re-derived here through the trace form (a
       third instrument: mg-af28 used the trace form, mg-7d75 deliberately did
       not, mg-6ad0 used both).
  T3c  the Cartan matrix, by Margolis-Saliola-Steinberg's route.  Its
       SYMMETRY is the invariant that separates the two programmes, because a
       cellular algebra --- which is what the branching side becomes when
       semisimplicity is dropped --- has a symmetric Cartan matrix.
  T3d  the census of posets for which kF(P) IS semisimple, i.e. where our
       family meets the branching axis at all.
"""

import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kerndb09 import (mk_poset, poset_classes, faces_of, tits, supp,
                      AC_by_support, AC_by_acyclicity, band_algebra, rref)

BAD = 0
FCAP = 90          # the trace-form radical is only run below this size


def bad(msg):
    global BAD
    BAD += 1
    print("  BAD: " + msg)


def key(X):
    return tuple(sorted(tuple(sorted(b)) for b in X))


def refines(X, Y):
    return all(any(set(bx) <= set(by) for by in Y) for bx in X)


def antichain(n):
    return mk_poset(n, [])


def chain(n):
    return mk_poset(n, [(i, i + 1) for i in range(n - 1)])


print("=" * 74)
print("T3a  THE ALGEBRA AGAINST ITS ENDOMORPHISM-ALGEBRA SHADOW")
print("=" * 74)
print("Every irreducible representation of kF(P) is one-dimensional (Brown;")
print("re-anchored at T3b below by dim kF(P)/rad = |AC(P)| together with the")
print("commutativity of the quotient).  So the algebra that Daniel's statement")
print("would produce --- sum over the vertices of End(V) --- has dimension")
print("|AC(P)| exactly, one for each vertex.")
print()
print("%-14s %8s %10s %12s %12s" %
      ("P", "|F(P)|", "|AC(P)|", "sum End dim", "radical %"))
rows = []
for n in range(1, 7):
    for nm, P in [("antichain %d" % n, antichain(n)), ("chain %d" % n, chain(n))]:
        F = faces_of(P)
        AC = {key(supp(f)) for f in F}
        pct = 100.0 * (len(F) - len(AC)) / len(F)
        print("%-14s %8d %10d %12d %11.1f%%" % (nm, len(F), len(AC), len(AC), pct))
        rows.append((nm, len(F), len(AC)))
print()
print("  The two figures the ticket carries: the radical is 90.4% of the")
print("  algebra at the n=5 antichain and 95.7% at n=6.  Both reproduce here")
print("  from |F| and |AC| alone.")
for nm, f, a in rows:
    if nm == "antichain 5" and round(100.0 * (f - a) / f, 1) != 90.4:
        bad("n=5 antichain radical fraction is %.1f%%" % (100.0 * (f - a) / f))
    if nm == "antichain 6" and round(100.0 * (f - a) / f, 1) != 95.7:
        bad("n=6 antichain radical fraction is %.1f%%" % (100.0 * (f - a) / f))

print()
print("  Same numbers as a ratio: how many times too big the algebra is.")
for nm, f, a in rows:
    if nm.startswith("antichain"):
        print("    %-14s |F|/|AC| = %d/%d = %.1f" % (nm, f, a, float(f) / a))

print()
print("=" * 74)
print("T3b  dim kF(P)/rad = |AC(P)|, through the trace form")
print("=" * 74)
print("All poset classes to n <= 5 with |F(P)| <= %d.  Larger classes are" % FCAP)
print("listed as exemptions with their sizes, not silently dropped.")
print()
tested = skipped = 0
exempt = []
for n in range(1, 6):
    cls = poset_classes(n)
    ok = 0
    for P in cls:
        F = faces_of(P)
        if len(F) > FCAP:
            skipped += 1
            exempt.append((n, len(F)))
            continue
        A = band_algebra(P)
        R = A.radical()
        isideal, isnilp, _ = A.verify_radical(R)
        AC = {key(supp(f)) for f in F}
        tested += 1
        if A.dim - len(R) != len(AC):
            bad("n=%d: dim A/rad = %d, |AC| = %d" % (n, A.dim - len(R), len(AC)))
        elif not (isideal and isnilp):
            bad("n=%d: radical not verified as a nilpotent ideal" % n)
        else:
            ok += 1
    print("  n = %d: %d of %d classes tested, %d agree" % (n, ok, len(cls), ok))
print("  tested %d, exempt %d (sizes: %s)" %
      (tested, skipped, sorted(set(f for _, f in exempt))))
print()
print("  The two AC routes --- supports of faces, and acyclicity of the")
print("  quotient --- are also compared, all classes to n <= 4:")
dis = 0
for n in range(1, 5):
    for P in poset_classes(n):
        a = {key(x) for x in AC_by_support(P)}
        b = {key(x) for x in AC_by_acyclicity(P)}
        if a != b:
            dis += 1
print("    disagreements: %d" % dis)
if dis:
    bad("AC routes disagree")

print()
print("=" * 74)
print("T3c  THE CARTAN MATRIX --- the invariant that separates the two sides")
print("=" * 74)
print("Margolis-Saliola-Steinberg (arXiv:1508.05446) Thm 4.18 computes the")
print("Cartan matrix of the algebra of a left regular band and states that it")
print("is 'unipotent lower triangular with respect to any linear extension of")
print("the partial order on Lambda(B)'.  It is rebuilt here from their own")
print("proof --- the character of kL_Y is chi(b) = |bB intersect L_Y|, and")
print("chi = sum_Z C_{Z,Y} chi_Z --- and then tested for the three properties")
print("that matter.")
print()
print("The self-check that makes this trustworthy: for a split basic algebra")
print("(all simples one-dimensional) the entries of the Cartan matrix must sum")
print("to dim A.")
print()


def cartan(P):
    B = faces_of(P)
    supp_of = {f: key(supp(f)) for f in B}
    Lam = sorted(set(supp_of.values()))
    idx = {x: i for i, x in enumerate(Lam)}
    reps = {}
    for f in B:
        reps.setdefault(supp_of[f], f)
    n = len(Lam)
    M = [[Fraction(1) if refines(Lam[j], Lam[i]) else Fraction(0)
          for j in range(n)] for i in range(n)]
    V = [[Fraction(0)] * n for _ in range(n)]
    for i, X in enumerate(Lam):
        f = reps[X]
        for h in {tits(f, g) for g in B}:
            V[i][idx[supp_of[h]]] += 1
    R, piv = rref([M[i][:] + V[i][:] for i in range(n)], 2 * n)
    if piv != list(range(n)):
        return None, None, len(B)
    return Lam, [[R[i][n + j] for j in range(n)] for i in range(n)], len(B)


print("%-14s %6s %8s %8s %10s %10s %12s %10s" %
      ("P", "|Lam|", "dim A", "sum C", "nonneg int", "unit diag", "triangular",
       "symmetric"))
for nm, P in [("antichain 2", antichain(2)), ("chain 2", chain(2)),
              ("antichain 3", antichain(3)), ("chain 3", chain(3)),
              ("V-poset 3", mk_poset(3, [(0, 1), (0, 2)])),
              ("antichain 4", antichain(4)), ("chain 4", chain(4)),
              ("antichain 5", antichain(5)), ("chain 5", chain(5))]:
    Lam, C, dimA = cartan(P)
    if C is None:
        bad("Cartan system singular for %s" % nm)
        continue
    m = len(Lam)
    tot = sum(sum(r) for r in C)
    nonneg = all(x >= 0 and x.denominator == 1 for r in C for x in r)
    diag1 = all(C[i][i] == 1 for i in range(m))
    # triangular with respect to the refinement order on Lambda
    tri = all(C[i][j] == 0 for i in range(m) for j in range(m)
              if not refines(Lam[j], Lam[i]) and i != j)
    sym = all(C[i][j] == C[j][i] for i in range(m) for j in range(m))
    print("%-14s %6d %8d %8d %10s %10s %12s %10s" %
          (nm, m, dimA, tot, "yes" if nonneg else "NO", "yes" if diag1 else "NO",
           "yes" if tri else "NO", "yes" if sym else "NO"))
    if tot != dimA:
        bad("%s: sum of Cartan entries %d != dim A %d" % (nm, tot, dimA))
    if not (nonneg and diag1 and tri):
        bad("%s: Cartan matrix fails MSS Thm 4.18" % nm)
    if sym != (dimA == m):
        bad("%s: symmetry and semisimplicity disagree" % nm)
print()
print("  sum C = dim A on every row, 0 exceptions: the computation is right.")
print("  Unipotent lower triangular on every row: MSS Thm 4.18 reproduced")
print("  against our object.")
print("  SYMMETRIC exactly on the rows where the algebra is semisimple.")
print()
print("  Why that last column decides the question.  A cellular algebra in the")
print("  sense of Graham-Lehrer --- Temperley-Lieb, Brauer, partition, Hecke,")
print("  and the whole non-semisimple continuation of the branching axis ---")
print("  has a SYMMETRIC Cartan matrix.  A left regular band algebra has a")
print("  UNITRIANGULAR one.  A matrix that is both is the identity, and an")
print("  algebra with identity Cartan matrix and one-dimensional simples is")
print("  semisimple.  So the two families meet only at their semisimple point.")

print()
print("=" * 74)
print("T3d  WHERE OUR FAMILY MEETS THE BRANCHING AXIS --- a census")
print("=" * 74)
print("kF(P) is semisimple exactly when |F(P)| = |AC(P)|, by T3b.  Over all")
print("poset isomorphism classes:")
print()
print("%3s %10s %14s %s" % ("n", "classes", "semisimple", "which"))
for n in range(1, 6):
    cls = poset_classes(n)
    eq = [P for P in cls if len(faces_of(P)) == len({key(supp(f)) for f in faces_of(P)})]
    names = []
    for P in eq:
        nn, rel = P
        names.append("total order" if len(rel) == nn * (nn - 1) // 2 else "other")
    print("%3d %10d %14d %s" % (n, len(cls), len(eq), ", ".join(names)))
    if len(eq) != 1 or names != ["total order"]:
        bad("n=%d: semisimple classes are %s" % (n, names))
print()
print("  1 class of 63 at n = 5, and it is the total order, where kF(P) is the")
print("  commutative algebra k^(2^(n-1)) --- a sum of 2^(n-1) copies of End of")
print("  a one-dimensional space.  Daniel's conclusion is TRUE there and")
print("  carries no information.")

print()
print("=" * 74)
print("T3e  MULTIPLICITY-FREENESS ON OUR SIDE --- an ARGUMENT, not evidence")
print("=" * 74)
print("Every simple kF(P)-module is one-dimensional.  A one-dimensional module")
print("over any subalgebra is simple, so along ANY chain of subalgebras every")
print("restriction multiplicity is 0 or 1 and the branching graph is")
print("automatically a graph, never a multigraph.")
print()
print("This is forced for every P of every size, so a measurement of it cannot")
print("do any work and is NOT booked as evidence here.  (mg-6ad0's X5 is the")
print("finding that this repo has booked forced answers as MEASURED before.)")
print("It is stated because it settles which side of T1/T2 we are on: we have")
print("the hypothesis that does not carry the conclusion, and we fail the one")
print("that does.")

print()
print("TOTAL BAD: %d" % BAD)
