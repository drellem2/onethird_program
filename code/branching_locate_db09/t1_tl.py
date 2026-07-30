"""T1 --- the Temperley-Lieb tower, and a WITHDRAWN separating example.

The ticket asks which of the two hypotheses in

    "a suitable category with a rank function and a multiplicity-free
     branching rule  =>  the Bratteli/path algebra is canonically an
     endomorphism algebra"

is load-bearing.  This script set out to build the object that a
"semisimplicity is not needed" reading would forbid: a tower whose branching
graph is multiplicity-free and IDENTICAL at every parameter, and whose
algebras are endomorphism algebras at some parameters and not at others.  The
tower is Temperley-Lieb, TL_1 subset TL_2 subset ... , at beta = 3 (generic),
2, 1 and 0.

IT IS NOT THAT OBJECT, and the claim that it is has been WITHDRAWN (mg-e8b8,
on the finding of the independent audit mg-2060).  The original T1b measured
the branching of the CELL modules at beta = 3, and at the other parameters
only the dimension identity dim V(n,p) = dim V(n-1,p) + dim V(n-1,p-1), which
mentions no beta and cannot separate parameters.  Vershik-Okounkov's branching
graph -- the definition this instrument itself quotes -- has the IRREDUCIBLES
as its vertices.  T1b2, added by the repair, measures that graph at every
parameter: the vertex set DIFFERS at beta = 0 and multiplicities reach 2 at
beta = 1 and beta = 0, so multiplicity-freeness varies down the column in
exact step with semisimplicity.  Both hypotheses moved together and the tower
separates nothing.

What the tower still does is inhabit one corner and reproduce six published
control facts; the verdict itself rests on Wedderburn, in T1d.

Everything is computed from the diagram definition in exact arithmetic.
"""

import sys
from fractions import Fraction

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from kerndb09 import (tl_diagrams, tl_algebra, link_states, tl_gram,
                      tl_cell_matrices, restrict_cell, hom_dim, rank,
                      tl_simples, tl_embed_diagram, solve_exact)

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
print("CORRECTED HEADING (mg-13b2, on mg-2060's X2).  This block used to say")
print("that a basis indexed by pairs of paths with a common endpoint exists")
print("IFF dim A = sum over the top-level vertices of (number of paths)^2.")
print("The 'only if' direction is right.  THE 'if' DIRECTION IS FALSE, and the")
print("counterexample is on this script's own T1c table.  What is measured")
print("here is the count identity and nothing more; T1c2 refutes the converse")
print("at every parameter where it can be refuted.")
print()
print("A basis of MATRIX UNITS indexed by pairs of paths with a common")
print("endpoint exists ONLY IF dim A = sum over the top-level vertices of")
print("(number of paths)^2.")
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
print("T1b  the CELL-module branching data, measured")
print("=" * 74)
print("dim Hom_{TL_{n-1}}(V_{n-1,q}, V_{n,p} restricted), at beta = 3 (generic,")
print("hence semisimple: see T1c), which in the semisimple case IS the")
print("restriction multiplicity.")
print()
print("CORRECTED HEADING (mg-e8b8).  This block used to be titled 'the")
print("BRANCHING GRAPH, measured (not cited)'.  What it measures is the")
print("branching of the CELL modules V_{n,p} at beta = 3, plus the")
print("parameter-free dimension identity below.  Vershik-Okounkov's branching")
print("graph has the IRREDUCIBLES as its vertices, and the two are not the")
print("same object away from semisimplicity.  T1b2 measures the actual one.")
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
print("  Every CELL multiplicity is 0 or 1, at beta = 3.  Because TL_6(3) is")
print("  semisimple (T1c) the cell modules ARE the irreducibles there, so at")
print("  beta = 3 this is also the branching graph.  At the other three")
print("  parameters it is NOT: see T1b2.")

print()
print("  The same rule, in dimensions, at EVERY beta.  NOTE WHAT THIS IS AND")
print("  IS NOT (mg-e8b8): neither side of the identity mentions beta, so it")
print("  cannot separate parameters and it is NOT a measurement of the")
print("  branching graph at beta != 3.  It is the Catalan triangle.")
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
print("T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT  (mg-e8b8)")
print("=" * 74)
print("The repair of T1b.  Vershik-Okounkov, quoted in the delivered document:")
print("the vertices at level n are the IRREDUCIBLE modules of the n-th algebra")
print("and the edges are the RESTRICTION MULTIPLICITIES; multiplicity-freeness")
print("is 'the multiplicities of all restrictions are equal 0 or 1'.  So the")
print("hypothesis is a statement about SIMPLE modules, and it is measured here")
print("at EVERY parameter, which is what the withdrawn claim asserted and did")
print("not do.")
print()
print("Graham-Lehrer: the irreducibles are the non-zero L(n,p) = V_{n,p}/rad<,>.")
print()

simples = {}
for b in BETAS:
    for n in range(1, NMAX + 1):
        simples[(n, b)] = tl_simples(n, b)

vtx = {}
for b in BETAS:
    for n in range(1, NMAX + 1):
        vtx[(n, b)] = [(p, d) for (p, d, c) in simples[(n, b)] if d > 0]


def vset(pairs):
    return "[" + ",".join("%d:%d" % (p, d) for (p, d) in pairs) + "]"


def vdims(pairs):
    return "[" + ",".join("%d" % d for (p, d) in pairs) + "]"


count_eq_set_ne = []
for i, b1 in enumerate(BETAS):
    for b2 in BETAS[i + 1:]:
        for n in range(1, NMAX + 1):
            s1, s2 = vtx[(n, b1)], vtx[(n, b2)]
            if len(s1) == len(s2) and s1 != s2:
                count_eq_set_ne.append((b1, b2, n, s1, s2))
CELLS = len(BETAS) * (len(BETAS) - 1) // 2 * NMAX

print("  (i) THE VERTEX SET --- the vertices, and NOT their number")
print()
print("  REPORTED AS A SET (mg-13b2, on mg-a218's X1).  A vertex of this graph")
print("  is an IRREDUCIBLE MODULE, so the datum the hypothesis is about is the")
print("  SET of them.  The break this whole block repairs was that equality of")
print("  ONE STATISTIC was taken for identity of the structure -- and a count")
print("  is one statistic.  A count column is therefore NOT printed beside")
print("  this one: two different vertex sets can carry the same cardinality,")
print("  and they do, at %d of the %d cells compared below."
      % (len(count_eq_set_ne), CELLS))
print()
print("  Canonical form of a vertex: the pair (p, dim L(n,p)).  Two vertex sets")
print("  are EQUAL iff these lists are equal.")
print()
for b in BETAS:
    print("  beta = %s" % b)
    for n in range(1, NMAX + 1):
        print("     n=%d  %s" % (n, vset(vtx[(n, b)])))
print()
print("  The number of CELL modules at level n is %s --- parameter-free."
      % [n // 2 + 1 for n in range(1, NMAX + 1)])
print()
# the labels live at p = 0,1,...,k with no gaps, which is what lets the
# delivered document abbreviate a vertex set to its dimensions alone.
for b in BETAS:
    for n in range(1, NMAX + 1):
        labels = [p for (p, d) in vtx[(n, b)]]
        if labels != list(range(len(labels))):
            bad("the live labels at (n,beta)=(%d,%s) are %s, not an unbroken "
                "run from 0 -- the dimensions-only abbreviation used in the "
                "delivered document is then ambiguous and must be widened"
                % (n, b, labels))
# and the abbreviation is checked, not argued: it must separate exactly the
# pairs the full canonical form separates, on every cell compared below.
for i, b1 in enumerate(BETAS):
    for b2 in BETAS[i + 1:]:
        for n in range(1, NMAX + 1):
            if ((vdims(vtx[(n, b1)]) == vdims(vtx[(n, b2)]))
                    != (vtx[(n, b1)] == vtx[(n, b2)])):
                bad("the dimensions-only abbreviation collides at "
                    "(n,beta1,beta2)=(%d,%s,%s)" % (n, b1, b2))
print("  THE VERTEX SETS, COMPARED PAIRWISE.  Population: the %d cells --- %d"
      % (CELLS, len(BETAS) * (len(BETAS) - 1) // 2))
print("  ordered pairs of the %d parameters x %d levels." % (len(BETAS), NMAX))
print()
print("    cells where the COUNT agrees and the SET does not: %d of %d"
      % (len(count_eq_set_ne), CELLS))
for (b1, b2, n, s1, s2) in count_eq_set_ne:
    print("      beta=%s vs beta=%s at n=%d: both have %d vertices, %s vs %s"
          % (b1, b2, n, len(s1), vset(s1), vset(s2)))
if not count_eq_set_ne:
    bad("no cell has an equal count and an unequal vertex set -- mg-a218 "
        "measured 10 of 36, and this instrument now disagrees with it")
print()
same_vertices = all(vtx[(n, b)] == vtx[(n, 3)]
                    for b in BETAS for n in range(1, NMAX + 1))
if same_vertices:
    bad("the vertex sets agree at every parameter -- mg-2060 measured them "
        "to differ at beta = 0, and this instrument now agrees with it")
else:
    print("  THE VERTEX SETS DIFFER, and at TWO parameters, not one:")
    for b in BETAS:
        levels = [n for n in range(1, NMAX + 1) if vtx[(n, b)] != vtx[(n, 3)]]
        if not levels:
            continue
        fewer = [n for n in levels if len(vtx[(n, b)]) < len(vtx[(n, 3)])]
        print("    beta = %s differs from beta = 3 at %d of the %d levels "
              "(n = %s); the COUNT differs at %d of them"
              % (b, len(levels), NMAX, ", ".join(str(n) for n in levels),
                 len(fewer)))
        for n in levels:
            print("      n=%d  %s   vs beta=3: %s"
                  % (n, vset(vtx[(n, b)]), vset(vtx[(n, 3)])))
    print("    -- so at beta = 1 a COUNT column would have printed the beta = 3")
    print("       row unchanged at every level while the graph was different at")
    print("       four of them.  That is the failure mode of the withdrawn")
    print("       claim, in the column that reports it.")
print()
print("  cross-check tying this to T1c: sum over the vertices of (dim L)^2")
print("  must be the dimension of the semisimple quotient, computed there by")
print("  two other routes.")
print()
print("  THE COLUMN AS SECTION 0 OF THE DELIVERED DOCUMENT PRINTS IT, dimensions")
print("  only (the labels are an unbroken run from 0, checked above):")
for b in BETAS:
    print("    beta = %s :  %s"
          % (b, " ".join(vdims(vtx[(n, b)]) for n in range(1, NMAX + 1))))

print()
print("  (ii) THE EDGES --- [L(n,p) restricted to TL_{n-1} : L(n-1,q)]")
print()
print("  Composition-factor multiplicities from characters: in characteristic")
print("  0 the characters of pairwise non-isomorphic simples are linearly")
print("  independent, so the multiplicities are the unique solution of")
print("  chi_{L(n,p)} restricted = sum_q m_q chi_{L(n-1,q)} on the diagram")
print("  basis of TL_{n-1}.  UNIQUENESS, INTEGRALITY, NON-NEGATIVITY and")
print("  sum_q m_q dim L(n-1,q) = dim L(n,p) are all checked, not assumed.")
print()
emb = {n: tl_embed_diagram(n) for n in range(2, NMAX + 1)}
mfree = {}
for b in BETAS:
    print("  ---- beta = %s ----" % b)
    mfree[b] = True
    for n in range(2, NMAX + 1):
        small = tl_diagrams(n - 1)
        low = [(q, d, c) for (q, d, c) in simples[(n - 1, b)] if d > 0]
        cols = [[c[d] for d in small] for (q, d, c) in low]
        for (p, dim, chi) in simples[(n, b)]:
            if dim == 0:
                continue
            target = [chi[emb[n][d]] for d in small]
            x, uniq = solve_exact(cols, target)
            if x is None:
                bad("no solution for L(%d,%d) at beta=%s" % (n, p, b))
                continue
            if not uniq:
                bad("solution not unique for L(%d,%d) at beta=%s" % (n, p, b))
            for v in x:
                if v.denominator != 1 or v < 0:
                    bad("multiplicity %s is not a non-negative integer for "
                        "L(%d,%d) at beta=%s" % (v, n, p, b))
            tot = sum(x[i] * low[i][1] for i in range(len(low)))
            if tot != dim:
                bad("dimension check: %s != %d for L(%d,%d) at beta=%s"
                    % (tot, dim, n, p, b))
            flag = ""
            if any(v > 1 for v in x):
                flag = "   <-- MULTIPLICITY 2"
                mfree[b] = False
            print("    L(%d,%d) dim %-2d ->  %s%s"
                  % (n, p, dim,
                     "  ".join("[L(%d,%d)]=%s" % (n - 1, low[i][0], x[i])
                               for i in range(len(low))), flag))
    ssq = sum(d * d for (p, d, c) in simples[(NMAX, b)])
    print("    multiplicity-free at beta = %s ?  %s     "
          "(sum (dim L)^2 at n = %d: %d)"
          % (b, "YES" if mfree[b] else "NO", NMAX, ssq))
    print()

print("  (iii) THE HYPOTHESIS, DOWN THE COLUMN")
print()
print("  %-6s %-24s" % ("beta", "branching multiplicity-free?"))
for b in BETAS:
    print("  %-6s %-24s" % (b, "YES" if mfree[b] else "NO"))
print()
expect = {3: True, 2: True, 1: False, 0: False}
for b in BETAS:
    if mfree[b] != expect[b]:
        bad("multiplicity-freeness at beta=%s is %s, expected %s"
            % (b, mfree[b], expect[b]))
if not all(mfree.values()):
    print("  MULTIPLICITY-FREENESS IS NOT HELD FIXED DOWN THIS COLUMN.  It")
    print("  varies in exact step with semisimplicity (T1c), which is what the")
    print("  experiment needed it not to do.  The separating example is")
    print("  WITHDRAWN in T1d.")

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
print("T1c2  THE 'iff' OF T1a IS FALSE, MEASURED  (mg-13b2, on mg-2060's X2)")
print("=" * 74)
print("mg-2060's X2: T1a asserted that the path-pair basis exists IFF the")
print("count identity holds.  The converse is refuted here rather than in")
print("prose, and it is refuted at every (n, beta) where it can be.")
print()
print("A basis of matrix units indexed by pairs of paths is exactly an")
print("isomorphism A = sum_lambda End(V_lambda), and by Wedderburn -- quoted")
print("in the delivered document, in both directions -- that holds iff A is")
print("SEMISIMPLE.  No new derivation is introduced here; the criterion is the")
print("theorem the document already quotes.  So wherever the count identity")
print("holds and rad(A) is non-zero, the 'if' direction is false at that pair.")
print()
print("%3s %6s %8s %14s %10s %20s" %
      ("n", "beta", "dim A", "sum (#paths)^2", "dim rad", "count identity?"))
refutations = []
for n in range(2, NMAX + 1):
    for b in BETAS:
        d, r, ss, ranks = table[(n, b)]
        paths = sum(len(link_states(n, p)) ** 2 for p in range(n // 2 + 1))
        holds = (paths == d)
        if not holds:
            bad("the path-pair count identity fails at (n,beta)=(%d,%s): "
                "%d vs %d" % (n, b, paths, d))
        print("%3d %6s %8d %14d %10d %20s"
              % (n, b, d, paths, r, "yes" if holds else "NO"))
        if holds and r > 0:
            refutations.append((n, b, d, paths, r))
print()
print("  THE COUNT IDENTITY HOLDS AT ALL %d (n, beta) PAIRS.  It is"
      % (4 * (NMAX - 1)))
print("  parameter-free: the link states are defined without reference to")
print("  beta, so it CANNOT distinguish the semisimple parameters from the")
print("  others, and an 'iff' resting on it is false wherever the two part.")
print("  They part at %d of the %d pairs:"
      % (len(refutations), 4 * (NMAX - 1)))
for (n, b, d, paths, r) in refutations:
    print("    TL_%d(%s): dim %d = sum (#paths)^2 = %d, and rad has dimension "
          "%d -- so it is NOT semisimple and has NO such basis"
          % (n, b, d, paths, r))
if not refutations:
    bad("no (n,beta) refutes the 'if' direction -- mg-2060 exhibited "
        "TL_2(0), and this instrument now disagrees with it")
else:
    sm = min(refutations, key=lambda t: t[2])
    print()
    print("  THE SMALLEST IS TL_%d(%s) = k[e]/(e^2), which is mg-2060's own"
          % (sm[0], sm[1]))
    print("  counterexample: dim %d, path-pair count 1^2 + 1^2 = %d, radical of"
          % (sm[2], sm[3]))
    print("  dimension %d.  It is on T1c's table above and always was." % sm[4])
    if not (sm[0] == 2 and sm[1] == 0 and sm[2] == 2 and sm[4] == 1):
        bad("the smallest refutation is not TL_2(0) with a 1-dimensional "
            "radical, which is what mg-2060 named")
print()
print("  What is TRUE, and is the statement the document did not make: a")
print("  CELLULAR algebra has a cellular basis indexed by pairs of paths,")
print("  multiplying with lower-cell terms, and it degenerates to matrix units")
print("  exactly when every cell form is non-degenerate -- exactly when the")
print("  algebra is semisimple.  The lower-cell terms are what 'the basis")
print("  survives' elided.  Nothing else in this instrument depended on the")
print("  'iff': T1a's own numbers are the count identity, unchanged.")

print()
print("=" * 74)
print("T1d  THE VERDICT --- WITHDRAWN AND REPLACED  (mg-e8b8, from mg-2060)")
print("=" * 74)
print("WHAT THIS BLOCK USED TO SAY, and it was wrong:")
print()
print("    'At n = 6 the branching graph is the same multiplicity-free graph")
print("     for every beta ... Multiplicity-freeness is held FIXED across")
print("     those four rows and the conclusion changes.  So multiplicity-")
print("     freeness is not what carries it.'")
print()
print("The invariant was never measured at beta != 3 under the definition this")
print("instrument quotes; the path-pair count was, and equality of that one")
print("statistic was taken for identity of the structure.  T1b2 measures the")
print("branching graph itself, at every parameter.  It is not the same graph:")
print("the vertex SET differs at beta = 1 and at beta = 0 -- and at beta = 1")
print("it differs while the NUMBER of vertices agrees with beta = 3 at every")
print("level, which is why T1b2 (i) reports the set and no count column sits")
print("beside it (mg-13b2, on mg-a218) -- and multiplicities reach 2 at")
print("beta = 1 and beta = 0.  THE SEPARATING EXAMPLE IS WITHDRAWN.")
print()
print("What is still true, and is measured here:")
print()
print("%6s %10s %26s %14s %22s"
      % ("beta", "dim TL_6", "dim of sum_lambda End(L_lambda)",
         "endomorphism algebra?", "branching mult-free?"))
for b in BETAS:
    d, r, ss, ranks = table[(6, b)]
    print("%6s %10d %26d %14s %22s"
          % (b, d, ss, "YES" if ss == d else "no",
             "YES" if mfree[b] else "NO"))
print()
print("  The last two columns move TOGETHER.  This tower does not separate the")
print("  two hypotheses in either direction, so it cannot decide which of them")
print("  carries the conclusion, and no claim that it does is made here.")
print()
print("  WHAT THE VERDICT NOW RESTS ON, and it is not a construction.  A")
print("  finite direct sum sum_lambda End(V_lambda) IS semisimple, so for")
print("  EVERY finite-dimensional algebra")
print()
print("      A  =  sum_lambda End(V_lambda)     <=>     A is semisimple,")
print()
print("  with no rank function, no branching graph and no multiplicity")
print("  hypothesis anywhere in it.  That is Wedderburn in both directions and")
print("  it settles the 'is' before any object is built.  Multiplicity-")
print("  freeness buys the word 'canonically' and nothing else, by Vershik-")
print("  Okounkov's Remark 1.3, quoted in T4.")
print()
print("  WHAT THE BUILDS DO ESTABLISH, which is real and is less than was")
print("  claimed: both off-diagonal cells of the 2x2 table are INHABITED.")
print("  Multiplicity-free and not semisimple is inhabited by kF(P) (T3: all")
print("  its irreducibles are one-dimensional, so its branching really is")
print("  multiplicity-free, and it is 90.4% radical at n = 5) -- NOT by")
print("  TL_6(1) or TL_6(0), which do not belong in that cell.  Semisimple")
print("  and not multiplicity-free is inhabited by C[S_4] on a skipped chain")
print("  and by C inside M_2(C) (T2).")
print()
print("  What survives without semisimplicity is the COUNT, not the")
print("  DECOMPOSITION: dim TL_n = sum_p (dim V_{n,p})^2 holds at every beta")
print("  (T1a); the direct sum of endomorphism algebras does not.")
print()
print("  MARKED IN PLACE (mg-13b2).  These two sentences used to read '(T1a),")
print("  so the pairs-of-paths BASIS exists throughout; the direct sum does")
print("  not.'  That was mg-2060's X2 and mg-e8b8 corrected it HERE while")
print("  booking X2 as untouched -- the correction was right and the")
print("  disclosure was not.  X2's remaining sites -- T1a's 'iff', corrected")
print("  above and refuted in T1c2, and a FOURTH site in section 1 of the")
print("  delivered document that no list named -- are closed here, so X2 is")
print("  closed at all four: two at 2e66d03 unmarked, two at mg-13b2.")

print()
print("TOTAL BAD: %d" % BAD)
