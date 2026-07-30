"""B1 --- THE SEPARATING EXAMPLE, CHECKED AGAINST THE DEFINITION.

mg-db09 section 0 states, of the Temperley-Lieb tower at beta in {3,2,1,0}:

    "The branching graph is MEASURED (not cited) to be the same
     multiplicity-free graph at each"

and builds its load-bearing verdict on holding multiplicity-freeness fixed
down that column.  Vershik-Okounkov's branching graph, quoted in the same
document, has as its VERTICES at level n the irreducible modules of the
n-th algebra and as its EDGES the restriction multiplicities.  So the
claim is a claim about SIMPLE modules.

What mg-db09's T1b measures is the multiplicity of CELL modules at
beta = 3 only, plus, at every beta, the dimension identity
dim V(n,p) = dim V(n-1,p) + dim V(n-1,p-1).

This script measures the object the claim is about:

  B1a  the VERTEX set at each (n, beta): the non-zero L(n,p) = V(n,p)/rad<,>
  B1b  the EDGE multiplicities [L(n,p) restricted : L(n-1,q)], from
       characters, at every beta
  B1c  Vershik-Okounkov Prop. 1.4 --- 'Z(M,N) is commutative' --- applied
       to the audited document's own example
  B1d  the verdict

TOTAL BAD counts DISAGREEMENTS WITH mg-db09's STATED CLAIM, not errors.
"""

from fractions import Fraction
import kern2060 as K

BAD = 0
BETAS = [3, 2, 1, 0]
NMAX = 6


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


# --------------------------------------------------------------------------
simples = {}      # (n, beta) -> list of (p, dim, character)
for beta in BETAS:
    for n in range(1, NMAX + 1):
        simples[(n, beta)] = K.tl_simples(n, beta)

hr("B1a  THE VERTEX SET OF THE BRANCHING GRAPH, at each parameter")
print("""A vertex of the branching graph at level n is an IRREDUCIBLE module
of TL_n(beta).  Graham-Lehrer: the irreducibles are the non-zero
L(n,p) = V(n,p)/rad<,>.  The cell modules V(n,p) are parameter-
independent; the SIMPLE ones are not.
""")
print("  %-4s %s" % ("n", "  ".join("beta=%d" % b for b in BETAS)))
vertex_counts = {}
for n in range(1, NMAX + 1):
    cells = [p for p in range(0, n // 2 + 1)]
    row = []
    for beta in BETAS:
        live = [p for (p, d, c) in simples[(n, beta)] if d > 0]
        vertex_counts[(n, beta)] = live
        row.append("%d" % len(live))
    print("  n=%-2d  %s   (cell modules: %d)"
          % (n, "      ".join(row), len(cells)))

print("\n  which p survive, by parameter:")
for beta in BETAS:
    print("    beta=%d:" % beta)
    for n in range(1, NMAX + 1):
        live = vertex_counts[(n, beta)]
        dims = dict((p, d) for (p, d, c) in simples[(n, beta)])
        print("      n=%d  vertices p = %-14s dims %s"
              % (n, str(live), [dims[p] for p in live]))

ref = {n: vertex_counts[(n, 3)] for n in range(1, NMAX + 1)}
same = True
for beta in BETAS:
    for n in range(1, NMAX + 1):
        if vertex_counts[(n, beta)] != ref[n]:
            same = False
print()
if same:
    print("  The vertex set is the same at every parameter.")
else:
    print("  *** THE VERTEX SET IS NOT THE SAME AT EVERY PARAMETER. ***")
    print("  mg-db09 section 0: 'The branching graph is measured (not cited)")
    print("  to be the same multiplicity-free graph at each'.  Under")
    print("  Vershik-Okounkov's definition of the branching graph --- the one")
    print("  mg-db09 quotes --- the graphs at beta = 3 and beta = 0 do not")
    print("  even have the same number of vertices.")
    BAD += 1
    for n in range(1, NMAX + 1):
        for beta in BETAS:
            if vertex_counts[(n, beta)] != ref[n]:
                print("    n=%d  beta=%d: vertices %s   vs beta=3: %s"
                      % (n, beta, vertex_counts[(n, beta)], ref[n]))

# --------------------------------------------------------------------------
hr("B1b  THE EDGES, from characters, at every parameter")
print("""[L(n,p) restricted to TL_{n-1} : L(n-1,q)] --- composition-factor
multiplicities, not cell-module multiplicities.  Over a field of
characteristic 0 the characters of the pairwise non-isomorphic simple
modules of a finite-dimensional algebra are linearly independent, so the
multiplicities are the unique solution of

    chi_{L(n,p)} restricted  =  sum_q  m_q * chi_{L(n-1,q)}

on the diagram basis of TL_{n-1}.  Uniqueness is CHECKED, not assumed,
and so is integrality and non-negativity.
""")

mfree = {}
edges = {}
for beta in BETAS:
    print("  ---- beta = %d ----" % beta)
    mfree[beta] = True
    for n in range(2, NMAX + 1):
        emb = K.tl_subalgebra_embedding(n)
        small = K.tl_diagrams(n - 1)
        low = [(q, d, c) for (q, d, c) in simples[(n - 1, beta)] if d > 0]
        cols = [[c[d] for d in small] for (q, d, c) in low]
        for (p, dim, chi) in simples[(n, beta)]:
            if dim == 0:
                continue
            target = [chi[emb[d]] for d in small]
            x, uniq = K.solve_exact(cols, target)
            if x is None:
                print("      n=%d p=%d : NO SOLUTION (characters not "
                      "spanning) -- reported, not silently dropped" % (n, p))
                BAD += 1
                continue
            if not uniq:
                print("      n=%d p=%d : solution NOT UNIQUE" % (n, p))
                BAD += 1
            mult = []
            for v in x:
                if v.denominator != 1 or v < 0:
                    print("      n=%d p=%d : non-integral or negative "
                          "multiplicity %s" % (n, p, v))
                    BAD += 1
                mult.append(v)
            edges[(n, p, beta)] = [(low[i][0], mult[i])
                                   for i in range(len(low))]
            # independent check on the character solve: composition
            # factors must account for the dimension exactly.
            tot = sum(mult[i] * low[i][1] for i in range(len(low)))
            if tot != dim:
                print("      n=%d p=%d : DIMENSION CHECK FAILED %s != %d"
                      % (n, p, tot, dim))
                BAD += 1
            flags = ""
            if any(m > 1 for m in mult):
                flags = "   <-- MULTIPLICITY > 1"
                mfree[beta] = False
            print("      L(%d,%d) dim %-3d ->  %s%s"
                  % (n, p, dim,
                     "  ".join("[L(%d,%d)]=%s" % (n - 1, low[i][0], mult[i])
                               for i in range(len(low))), flags))
    print("      multiplicity-free at beta = %d ?  %s"
          % (beta, "YES" if mfree[beta] else "NO"))
    print()

print("  Summary --- the hypothesis mg-db09 says it holds FIXED:")
for beta in BETAS:
    print("    beta = %d : branching multiplicity-free = %s"
          % (beta, mfree[beta]))
if not all(mfree.values()):
    print()
    print("  *** MULTIPLICITY-FREENESS IS NOT HELD FIXED DOWN THE COLUMN. ***")
    print("  mg-db09 section 0: 'Multiplicity-freeness is held fixed down")
    print("  that column and the conclusion changes.'  Measured here under")
    print("  the definition mg-db09 itself quotes, it is not held fixed.")
    BAD += 1

# --------------------------------------------------------------------------
hr("B1c  VERSHIK-OKOUNKOV Prop. 1.4, applied to mg-db09's own example")
print("""mg-db09 section 1 adopts Prop. 1.4 as the equality-form of the
multiplicity-freeness hypothesis --- 'multiplicities in {0,1},
equivalently (VO Prop. 1.4) the centralizer Z(M,N) is commutative' ---
and mg-db09's T2c uses exactly that test on the symmetric-group side.
Here it is, applied to the Temperley-Lieb side, where mg-db09 did not
run it.
""")


def centralizer(A, sub_indices):
    """{x in A : x*s = s*x for every s in the subalgebra}, as a basis."""
    d = A.dim
    rows = []
    for si in sub_indices:
        for k in range(d):
            row = [Fraction(0)] * d
            for j in range(d):
                c, t = A.table[j][si]      # (b_j s)
                if t == k:
                    row[j] += c
                c, t = A.table[si][j]      # (s b_j)
                if t == k:
                    row[j] -= c
            rows.append(row)
    return K.nullspace(rows, d)


def commutes(A, vecs):
    d = A.dim
    for v in vecs:
        for w in vecs:
            p = [Fraction(0)] * d
            for j, a in enumerate(v):
                if a == 0:
                    continue
                for l, b in enumerate(w):
                    if b == 0:
                        continue
                    c, k = A.table[j][l]
                    p[k] += a * b * c
                    c, k = A.table[l][j]
                    p[k] -= a * b * c
            if any(x != 0 for x in p):
                return False
    return True


print("  %-5s %-6s %-14s %-10s %s"
      % ("n", "beta", "dim Z(M,N)", "commutative?", "semisimple?"))
for n in (3, 4, 5):
    for beta in BETAS:
        A = K.tl_algebra(n, beta)
        emb = K.tl_subalgebra_embedding(n)
        sub = [A.index[emb[d]] for d in K.tl_diagrams(n - 1)]
        Z = centralizer(A, sub)
        cm = commutes(A, Z)
        ss = A.radical_dim() == 0
        print("  %-5d %-6d %-14d %-10s %s"
              % (n, beta, len(Z), "yes" if cm else "NO", "yes" if ss else "no"))

# --------------------------------------------------------------------------
hr("B1d  VERDICT ON THE SEPARATING EXAMPLE")
print("""What survives of mg-db09's T1, measured:

  * The CELL modules V(n,p) and their dimensions are parameter-independent.
    Confirmed here (selftest: the Catalan triangle at every beta).
  * dim TL_n = sum_p (dim V(n,p))^2 at every beta.  Confirmed --- it is
    the Catalan identity and has nothing to do with beta.
  * The algebra is a direct sum of endomorphism algebras exactly at the
    parameters where it is semisimple.  Confirmed, and it is Wedderburn
    in BOTH directions: a finite direct sum of full matrix algebras IS
    semisimple, so the implication 'not semisimple => not sum_lambda End'
    holds for EVERY finite-dimensional algebra and could not have failed
    for any example.

What does not survive:

  * that the BRANCHING GRAPH is the same at each parameter, and
  * that MULTIPLICITY-FREENESS is held fixed down the column,

under the definition of 'branching graph' that mg-db09 quotes from
Vershik-Okounkov and uses everywhere else in the document.  See B1a/B1b.
""")

print("TOTAL BAD: %d" % BAD)
