"""T1 --- the MULTIPLICITY-FREE, NON-SEMISIMPLE object, BUILT.

The ticket asks which of the two hypotheses in

    "a suitable category with a rank function and a multiplicity-free
     branching rule  =>  the Bratteli/path algebra is canonically an
     endomorphism algebra"

is load-bearing.  This script builds the object that a "semisimplicity is not
needed" reading would forbid: a tower whose branching graph is multiplicity-
free and IDENTICAL at every parameter, and whose algebras are endomorphism
algebras at some parameters and not at others.

The tower is Temperley-Lieb, TL_1 subset TL_2 subset ... , at the parameters
beta = 3 (generic), 2, 1 and 0.  Nothing here is specific to TL: it is simply
the smallest tower in which the branching data can be held fixed while
semisimplicity is switched off.

Everything is computed from the diagram definition in exact arithmetic.
"""

import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kerndb09 import (tl_diagrams, tl_algebra, link_states, tl_gram,
                      tl_cell_matrices, restrict_cell, hom_dim, rank)

BAD = 0
NMAX = 6
BETAS = [3, 2, 1, 0]


def catalan(n):
    c = 1
    for k in range(n):
        c = c * 2 * (2 * k + 1) // (k + 2)
    return c


def bad(msg):
    global BAD
    BAD += 1
    print("  BAD: " + msg)


print("=" * 74)
print("T1a  dim TL_n = sum_p (dim V_{n,p})^2  --- the PATH-PAIR count")
print("=" * 74)
print("A basis indexed by pairs of paths with a common endpoint exists iff")
print("dim A = sum over the top-level vertices of (number of paths)^2.")
print()
print("%3s %8s %10s %s" % ("n", "dim TL_n", "Catalan", "cell-module dims (dim V_{n,p})"))
for n in range(1, NMAX + 1):
    dims = [len(link_states(n, p)) for p in range(n // 2 + 1)]
    d = len(tl_diagrams(n))
    s = sum(x * x for x in dims)
    print("%3d %8d %10d  %s   sum of squares = %d" % (n, d, catalan(n), dims, s))
    if d != catalan(n):
        bad("dim TL_%d = %d, Catalan = %d" % (n, d, catalan(n)))
    if s != d:
        bad("n=%d: sum of squares %d != dim %d" % (n, s, d))
print()
print("The cell-module dimensions do not depend on beta: the diagram basis and")
print("the link states are defined without reference to it.  So the path-pair")
print("count is the SAME at every parameter.")

print()
print("=" * 74)
print("T1b  the BRANCHING GRAPH, measured (not cited)")
print("=" * 74)
print("dim Hom_{TL_{n-1}}(V_{n-1,q}, V_{n,p} restricted), at beta = 3 (generic,")
print("hence semisimple: see T1c), which in the semisimple case IS the")
print("restriction multiplicity.")
print()
mults = {}
for n in range(2, NMAX + 1):
    for p in range(n // 2 + 1):
        st, rm = restrict_cell(n, p, 3)
        row = []
        for q in range((n - 1) // 2 + 1):
            st2, m2 = tl_cell_matrices(n - 1, q, 3)
            m = hom_dim(m2, rm, len(st2), len(st))
            row.append(m)
            mults[(n, p, q)] = m
        print("  V_{%d,%d} (dim %d) -> multiplicities over q=0.. : %s" %
              (n, p, len(st), row))
        if any(m not in (0, 1) for m in row):
            bad("multiplicity not in {0,1} at (n,p)=(%d,%d): %s" % (n, p, row))
        # the multiplicity-free rule: exactly V_{n-1,p} and V_{n-1,p-1}
        want = []
        for q in range((n - 1) // 2 + 1):
            want.append(1 if (q == p or q == p - 1) else 0)
        if row != want:
            bad("branching at (n,p)=(%d,%d) is %s, expected %s" % (n, p, row, want))
print()
print("  Every multiplicity is 0 or 1: the branching graph is a GRAPH, not a")
print("  multigraph.  This is the hypothesis 'multiplicity-free branching'.")

print()
print("  The same rule, in dimensions, at EVERY beta (the dimensions do not")
print("  depend on beta, so this is one check that covers all of them):")
for n in range(2, NMAX + 1):
    for p in range(n // 2 + 1):
        d = len(link_states(n, p))
        a = len(link_states(n - 1, p)) if p <= (n - 1) // 2 else 0
        b = len(link_states(n - 1, p - 1)) if p >= 1 else 0
        ok = (d == a + b)
        print("   dim V_{%d,%d} = %d = %d + %d  %s" % (n, p, d, a, b, "" if ok else "<-- BAD"))
        if not ok:
            bad("Pascal rule fails at (%d,%d)" % (n, p))

print()
print("=" * 74)
print("T1c  SEMISIMPLICITY, by two disjoint routes")
print("=" * 74)
print("route 1: rad(A) = radical of the trace form of the regular")
print("         representation (char 0), CHECKED to be a two-sided ideal and")
print("         to be nilpotent.")
print("route 2: Graham-Lehrer's criterion for a cellular algebra --- the")
print("         semisimple quotient has dimension sum_p (rank of the Gram")
print("         matrix of V_{n,p})^2.  Built from the bilinear form on link")
print("         states; shares no code with route 1.")
print()
print("%3s %6s %8s %8s %10s %10s %8s" %
      ("n", "beta", "dim A", "dim rad", "A/rad (1)", "A/rad (2)", "ss?"))
table = {}
for n in range(2, NMAX + 1):
    for b in BETAS:
        A = tl_algebra(n, b)
        R = A.radical()
        isideal, isnilp, idx = A.verify_radical(R)
        if not isideal:
            bad("rad(TL_%d(%s)) is not an ideal" % (n, b))
        if not isnilp:
            bad("rad(TL_%d(%s)) is not nilpotent" % (n, b))
        ss1 = A.dim - len(R)
        ranks = []
        for p in range(n // 2 + 1):
            st, G = tl_gram(n, p, b)
            ranks.append(rank(G, len(st)))
        ss2 = sum(r * r for r in ranks)
        table[(n, b)] = (A.dim, len(R), ss1, ranks)
        print("%3d %6s %8d %8d %10d %10d %8s" %
              (n, b, A.dim, len(R), ss1, ss2, "yes" if len(R) == 0 else "NO"))
        if ss1 != ss2:
            bad("two routes disagree at (n,beta)=(%d,%s): %d vs %d" % (n, b, ss1, ss2))
print()
print("  0 disagreements between the two routes is the check that matters:")
print("  the trace form never sees a cell module and the Gram matrices never")
print("  see the regular representation.")

print()
print("  Published facts this reproduces, as controls (Ridout-Saint-Aubin,")
print("  arXiv:1204.4505, Cor. 4.6 and the remark after Cor. 4.8):")
ctrl = [
    ("TL_n(2) is semisimple for every n", all(table[(n, 2)][1] == 0 for n in range(2, NMAX + 1))),
    ("TL_n(0) is semisimple for n odd", all(table[(n, 0)][1] == 0 for n in range(3, NMAX + 1, 2))),
    ("TL_n(0) is NOT semisimple for n even", all(table[(n, 0)][1] > 0 for n in range(2, NMAX + 1, 2))),
    ("TL_2(0) has a 1-dimensional radical", table[(2, 0)][1] == 1),
    ("TL_n(1) is NOT semisimple for n >= 3", all(table[(n, 1)][1] > 0 for n in range(3, NMAX + 1))),
    ("TL_n(3) is semisimple for every n", all(table[(n, 3)][1] == 0 for n in range(2, NMAX + 1))),
]
for msg, ok in ctrl:
    print("   %-45s %s" % (msg, "reproduced" if ok else "FAILED"))
    if not ok:
        bad("control failed: " + msg)

print()
print("=" * 74)
print("T1d  THE VERDICT --- which hypothesis is load-bearing")
print("=" * 74)
print("At n = 6 the branching graph is the same multiplicity-free graph for")
print("every beta, and the path-pair count is 132 for every beta.  What")
print("changes is only whether the algebra is an endomorphism algebra:")
print()
print("%6s %10s %26s %14s" % ("beta", "dim TL_6", "dim of sum_lambda End(L_lambda)",
                              "endomorphism algebra?"))
for b in BETAS:
    d, r, ss, ranks = table[(6, b)]
    print("%6s %10d %26d %14s" % (b, d, ss, "YES" if ss == d else "no"))
print()
print("  Multiplicity-freeness is held FIXED across those four rows and the")
print("  conclusion changes.  So multiplicity-freeness is not what carries it.")
print("  Semisimplicity varies across those four rows exactly in step with the")
print("  conclusion.")
print()
print("  What survives without semisimplicity is the BASIS, not the")
print("  DECOMPOSITION: dim TL_n = sum_p (dim V_{n,p})^2 holds at every beta")
print("  (T1a), so the pairs-of-paths basis exists throughout; the direct sum")
print("  of endomorphism algebras does not.")

print()
print("TOTAL BAD: %d" % BAD)
