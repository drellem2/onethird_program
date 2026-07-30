"""B2 --- THE CLAIM NO PRE-FILED LIST NAMES.

mg-db09's brief names six places to attack the document.  None of them is
the sentence that opens its own T1a output:

    "A basis indexed by pairs of paths with a common endpoint exists iff
     dim A = sum over the top-level vertices of (number of paths)^2."

and none of them is the consequence the document draws from it, in the
section-0 2x2 table and again in T1d:

    "Path-pair *basis* survives, direct sum does not."
    "What survives without semisimplicity is the BASIS, not the
     DECOMPOSITION: dim TL_n = sum_p (dim V(n,p))^2 holds at every beta
     (T1a), so the pairs-of-paths basis exists throughout."

I chose this one because it is the only load-bearing sentence in the
document that is stated as an IFF, is not a quotation, is not in the
pre-filed list, and is checkable by construction.  A dimension count is
being read as the existence of a structure.

B2a  the 'only if' direction, which is fine
B2b  the 'if' direction, refuted by construction at the document's own
     parameters
B2c  what the surviving statement actually is
"""

from fractions import Fraction
import kern2060 as K

BAD = 0


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


hr("B2a  WHAT 'A PATH-PAIR BASIS' MEANS, and the direction that holds")
print("""In Vershik-Okounkov section 1 the pairs-of-paths basis is not a
counting statement.  It is the set of MATRIX UNITS: for a tower of
semisimple algebras, A_n = sum_lambda End(V_lambda), the increasing
paths to lambda index a basis of V_lambda, and the pairs (s,t) of paths
with the same endpoint index the matrix units E_{s,t}, which satisfy
E_{s,t} E_{u,v} = delta_{t,u} E_{s,v}.

If such a basis exists then dim A = sum_lambda (#paths to lambda)^2 ---
the 'only if' direction, and it is immediate.

The document's T1a asserts the converse as an IFF.  A dimension count
cannot produce matrix units, and here is the construction that shows it
does not.
""")

hr("B2b  THE 'IF' DIRECTION, REFUTED BY CONSTRUCTION")
print("""The smallest witness is TL_2(0), which the document itself puts on
the record (T1c row 4, 'TL_2(0) has a 1-dimensional radical') and then
counts as satisfying its iff.
""")
print("  %-12s %-8s %-8s %-16s %-12s %-9s %s"
      % ("algebra", "dim A", "sum V^2", "# simple modules",
         "sum (dim L)^2", "dim rad", "matrix units possible?"))
for n in range(2, 7):
    for beta in (3, 2, 1, 0):
        A = K.tl_algebra(n, beta)
        cells = [len(K.link_states(n, p)) for p in range(0, n // 2 + 1)]
        pathpair = sum(c * c for c in cells)
        sims = [(p, d) for (p, d, c) in K.tl_simples(n, beta) if d > 0]
        ssq = sum(d * d for (p, d) in sims)
        rad = A.radical_dim()
        ok = (rad == 0)
        if pathpair != A.dim:
            print("  UNEXPECTED: path-pair count != dim A")
            BAD += 1
        if n == 6 or (n <= 4):
            print("  %-12s %-8d %-8d %-16d %-12d %-9d %s"
                  % ("TL_%d(%d)" % (n, beta), A.dim, pathpair, len(sims),
                     ssq, rad, "yes" if ok else "NO"))

print("""
  Read the TL_2(0) row.  dim A = 2 and the path-pair count is
  1^2 + 1^2 = 2, so the document's iff is satisfied.  But TL_2(0) is
  k[e]/(e^2): it is LOCAL, it has ONE simple module, and there is no
  set of matrix units in it at all --- the only idempotents are 0 and 1.
  The counting identity holds and the structure it is claimed to be
  equivalent to does not exist.

  Read the TL_6(1) row.  dim A = 132 = the path-pair count, and the
  document reports A/rad of dimension 99.  A basis of matrix units would
  make A semisimple of dimension 99, not 132.
""")

# make the refutation explicit rather than rhetorical
A = K.tl_algebra(2, 0)
idem = []
for i in range(A.dim):
    for a in (Fraction(-2), Fraction(-1), Fraction(0), Fraction(1),
              Fraction(2), Fraction(1, 2)):
        pass
# exhaustively: every element x = a*1 + b*e with e^2 = 0 has
# x^2 = a^2*1 + 2ab*e, so x^2 = x forces a in {0,1} and b = 0.
print("  Exhaustive check in TL_2(0) = k[e]/(e^2):  x = a + b e  =>")
print("  x^2 - x = (a^2 - a) + (2ab - b) e = 0  =>  a in {0,1} and")
print("  b(2a - 1) = 0  =>  b = 0.  The only idempotents are 0 and 1, so")
print("  no family of >= 2 orthogonal idempotents exists and there is no")
print("  path-pair basis of matrix units.")
one = tuple(sorted(tuple(sorted((i, i + 2))) for i in range(2)))
e = ((0, 1), (2, 3))
assert A.table[A.index[e]][A.index[e]] == (Fraction(0), A.index[e]), \
    "e^2 = 0 at beta = 0"
print("  (e^2 = 0 verified in the constructed algebra.)")

nsimple = len([1 for (p, d, c) in K.tl_simples(2, 0) if d > 0])
if nsimple != 1:
    print("  UNEXPECTED: TL_2(0) has %d simples" % nsimple)
    BAD += 1

hr("B2c  WHAT THE SURVIVING STATEMENT IS")
print("""dim TL_n(beta) = sum_p (dim V(n,p))^2 at every beta is TRUE, and it
is a statement about CELL modules.  It is the Catalan identity
    sum_p (C(n,p) - C(n,p-1))^2 = Catalan(n)
and it holds for every beta because neither side mentions beta.  It is
not evidence that a path-pair basis of the tower exists at non-generic
parameters; it is evidence that the CELL module dimensions are
parameter-independent, which is Graham-Lehrer's cellular structure and
was never in doubt.

The correct non-semisimple statement, and the document does not make it:
a cellular algebra has a CELLULAR basis indexed by pairs of paths, and
that basis multiplies according to
    C^lambda_{s,t} C^mu_{u,v} = <t,u> delta_{lambda,mu} C^lambda_{s,v}
                                 + (lower cell terms),
which degenerates to matrix units exactly when every form <,> is
non-degenerate --- that is, exactly when the algebra is semisimple.
The lower-cell terms are what 'the basis survives' elides.
""")

print("  The consequence for the document:")
print("   * section 0's 2x2 table cell 'Path-pair *basis* survives' is")
print("     a dimension coincidence read as a structure.")
print("   * T1a's 'iff' is FALSE in the 'if' direction.")
print("   * NOTHING ELSE in the document depends on it: the load-bearing")
print("     verdict rests on T1c/T1d and on Wedderburn, not on this.")
print()
print("TOTAL BAD: %d" % BAD)
