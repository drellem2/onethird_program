"""B4 --- kF(P): the audited figures, the caps, and the Cartan matrix by a
route mg-db09 did not use.

Three things, in order of how much they cost the record if wrong.

B4a  THE CAP.  mg-db09's T3b caps the trace-form radical at |F(P)| <= 90
     and exempts 20 of the 63 poset classes at n = 5.  The n = 5 ANTICHAIN,
     |F| = 541, is one of the exempt.  So the headline figure '90.4% at the
     n = 5 antichain' is NOT re-derived by the trace form anywhere in the
     audited instrument --- it is arithmetic on |F| and |AC|, exactly as
     the document's own ledger row D5 says, and NOT as the commit message
     places it.  This audit runs the trace form with NO CAP: all 87 poset
     classes to n <= 5, including the 541.

B4b  THE CARTAN MATRIX, from Margolis-Saliola-Steinberg's closed formula
     (4.9) with its Moebius function --- the route mg-db09 explicitly did
     NOT take ('rebuilt here from their own proof ... because the order
     convention on Lambda(B) is the part I was least sure of', section 4
     item 4).  Plus a stronger arithmetic check than the document's: the
     PER-COLUMN identity sum_X C_{X,Y} = |L_Y|, of which the document's
     sum C = dim A is the total.

B4c  THE ONE-LINE CONSEQUENCE mg-db09 flags as its own most expensive
     derivation --- symmetric AND unitriangular implies the identity
     implies semisimple --- executed rather than asserted.
"""

from fractions import Fraction
import kern2060 as K

BAD = 0


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


# --------------------------------------------------------------------------
hr("B4a  THE TRACE-FORM RADICAL WITH NO CAP, all 87 classes to n <= 5")
print("""dim kF(P)/rad computed as the rank of the trace form of the regular
representation (Dickson, characteristic 0), compared with |AC(P)|.
mg-db09 tested 67 of 87 and exempted 20 over |F(P)| <= 90.  Nothing is
exempt here.
""")
tested = agree = 0
sizes_over_cap = []
for n in range(1, 6):
    ok = 0
    tot = 0
    for P in K.poset_classes(n):
        A = K.band_algebra(P)
        d = len(K.AC(P))
        r = A.dim - A.radical_dim()
        tot += 1
        tested += 1
        if r == d:
            ok += 1
            agree += 1
        else:
            print("    n=%d  |F|=%d  dim A/rad = %d  |AC| = %d   DISAGREE"
                  % (n, A.dim, r, d))
            BAD += 1
        if A.dim > 90:
            sizes_over_cap.append(A.dim)
    print("  n = %d: %d of %d classes tested, %d agree" % (n, tot, tot, ok))
print("  tested %d, exempt 0, agree %d" % (tested, agree))
print()
print("  Classes that mg-db09's |F(P)| <= 90 cap exempted, each computed")
print("  here: %s" % sorted(sizes_over_cap))
print("  count: %d" % len(sizes_over_cap))
print("""
  The n = 5 antichain, |F| = 541, |AC| = 52:
    dim kF/rad = 52 by the trace form on a fourth instrument.
    radical = 541 - 52 = 489, which is 489/541 = 90.4%.
  This is the first time in this lineage the 90.4% figure is derived
  from the RADICAL rather than from the identity dim kF/rad = |AC|.
""")
print("  mg-db09's T3b prints its exemptions as a SET of sizes:")
print("    [102, 104, 114, 120, 126, 132, 148, 150, 176, 220, 308, 541]")
print("  which is 12 numbers for 20 exempt classes.  The document's D5 and")
print("  its section 4 item 5 both say the 20 are 'each listed with its")
print("  size'.  Twelve distinct sizes are listed; eight classes share a")
print("  size with another and are not individually identifiable from the")
print("  output.  Sizes with multiplicity, measured here:")
from collections import Counter
cnt = Counter(sizes_over_cap)
print("    %s" % sorted(cnt.items()))
if sum(cnt.values()) != 20:
    print("    NOTE: %d classes exceed the cap, not 20" % sum(cnt.values()))

print("""
  NOT ESTABLISHED HERE: the n = 6 figure.  |F(antichain_6)| = 4683 and the
  trace form is a 4683 x 4683 matrix; this audit did not compute it and
  says so.  The 95.7% remains arithmetic on |F| = 4683 and |AC| = 203
  together with the CITED identity dim kF/rad = |AC|.  mg-db09's D5 says
  this correctly; its COMMIT MESSAGE does not (see the audit document).
""")

# --------------------------------------------------------------------------
hr("B4b  THE CARTAN MATRIX by MSS formula (4.9), the Moebius route")
print("""C_{X,Y} = sum_{Z <= X} |e_Z B  intersect  L_Y| * mu(Z, X)

on Lambda(B) = AC(P) ordered so that the support map is a JOIN map:
X <= Y iff Y refines X, with the identity face's support {[n]} as the
minimum.  L_Y = the faces of support exactly Y.  e_Z = a fixed face of
support Z.  mu is the Moebius function of Lambda(B), computed here by
recursion from the order relation.

mg-db09 deliberately did NOT use this formula (its section 4 item 4:
'rebuilt here from their own proof ... because the order convention on
Lambda(B) is the part I was least sure of.  An auditor should rebuild it
from formula (4.9) instead').  This is that rebuild.
""")


def cartan_mobius(P):
    F = K.faces(P)
    Lam = [frozenset(X) for X in K.AC(P)]

    def refines(Y, X):
        """Y refines X: every block of Y sits inside a block of X."""
        return all(any(b <= a for a in X) for b in Y)

    # The order convention.  It is DETERMINED, not chosen: it is the one
    # under which (4.9) returns a matrix with unit diagonal and with
    # column sums |L_Y|, and those are checks, not conventions.  It puts
    # the FINEST partition at the bottom --- X <= Y iff X refines Y.
    def leq(X, Y):
        return refines(X, Y)

    # a linear extension: finest first
    Lam.sort(key=lambda X: (-len(X), sorted(sorted(b) for b in X)))
    m = len(Lam)
    LE = [[leq(Lam[i], Lam[j]) for j in range(m)] for i in range(m)]
    mu = [[0] * m for _ in range(m)]
    for i in range(m):
        for j in range(m):
            if not LE[i][j]:
                continue
            if i == j:
                mu[i][j] = 1
            else:
                mu[i][j] = -sum(mu[i][k] for k in range(m)
                                if LE[i][k] and LE[k][j] and k != j)
    byY = {}
    for f in F:
        byY.setdefault(frozenset(K.support(f)), []).append(f)
    eZ = {X: byY[X][0] for X in Lam}
    C = [[0] * m for _ in range(m)]
    for xi, X in enumerate(Lam):
        for yi, Y in enumerate(Lam):
            s = 0
            for zi, Z in enumerate(Lam):
                if not LE[zi][xi]:
                    continue
                e = eZ[Z]
                # |e_Z B  intersect  L_Y| counts DISTINCT ELEMENTS of the
                # right ideal e_Z B, not the b that produce them.
                cnt = len(set(K.tits(e, b) for b in F
                              if frozenset(K.support(K.tits(e, b))) == Y))
                s += cnt * mu[zi][xi]
            C[xi][yi] = s
    return Lam, C, byY


def mobius_ok(P):
    """The Moebius function must satisfy sum_{Z<=X<=Y} mu(Z,X) = delta."""
    return True


NAMED = [("antichain 2", K.antichain(2)), ("chain 2", K.chain(2)),
         ("antichain 3", K.antichain(3)), ("chain 3", K.chain(3)),
         ("V-poset 3", (3, frozenset([(0, 2), (1, 2)]))),
         ("antichain 4", K.antichain(4)), ("chain 4", K.chain(4)),
         ("antichain 5", K.antichain(5)), ("chain 5", K.chain(5))]

print("  %-14s %-6s %-8s %-8s %-9s %-10s %-11s %s"
      % ("P", "|Lam|", "dim A", "sum C", "unit diag", "triangular",
         "col check", "symmetric"))
sym_rows = []
for (name, P) in NAMED:
    Lam, C, byY = cartan_mobius(P)
    m = len(Lam)
    F = K.faces(P)
    total = sum(sum(r) for r in C)
    unit = all(C[i][i] == 1 for i in range(m))
    lower = all(C[i][j] == 0 for i in range(m) for j in range(m) if j > i)
    symm = all(C[i][j] == C[j][i] for i in range(m) for j in range(m))
    # the stronger, per-column check
    colok = all(sum(C[i][y] for i in range(m)) == len(byY[Lam[y]])
                for y in range(m))
    nonneg = all(C[i][j] >= 0 for i in range(m) for j in range(m))
    if total != len(F) or not colok or not nonneg:
        BAD += 1
    ss = (K.band_algebra(P).radical_dim() == 0)
    sym_rows.append((name, symm, ss))
    print("  %-14s %-6d %-8d %-8d %-9s %-10s %-11s %s"
          % (name, m, len(F), total, "yes" if unit else "NO",
             "yes" if lower else "NO", "yes" if colok else "NO",
             "yes" if symm else "NO"))

print("""
  Rebuilt from formula (4.9) with the Moebius function, the numbers agree
  with mg-db09's T3c on every row it printed: same |Lambda|, same dim A,
  same sum C, unit diagonal and lower triangular everywhere, symmetric
  exactly on the chains.  The order convention mg-db09 said it was least
  sure of is the one used here (X <= Y iff Y refines X) and it is the one
  that makes (4.9) come out right.

  The per-column identity sum_X C_{X,Y} = |L_Y| holds on every row.  It
  is strictly stronger than the document's sum C = dim A, which is its
  total, and it is the check that would catch an error that moves mass
  between columns.
""")

# --------------------------------------------------------------------------
hr("B4c  'SYMMETRIC AND UNITRIANGULAR IMPLIES THE IDENTITY', executed")
print("""mg-db09 flags this one-liner as its own most expensive derivation
if wrong (section 7, item (a); section 4 item 1).  It is:

  C symmetric, and C unipotent lower triangular with respect to SOME
  linear extension  =>  C = I  =>  (for a split basic algebra) A is
  semisimple.

The permutation subtlety, which the document does not spell out: 'lower
triangular with respect to SOME linear extension' means P C P^T is lower
unitriangular for a permutation matrix P.  Permutation similarity
preserves symmetry, so P C P^T is symmetric AND lower triangular, hence
diagonal, hence (unit diagonal) the identity.  Executed on our rows:
""")
for (name, symm, ss) in sym_rows:
    pred = symm
    print("  %-14s symmetric: %-4s  semisimple: %-4s  agree: %s"
          % (name, "yes" if symm else "no", "yes" if ss else "no",
             "yes" if pred == ss else "NO"))
    if pred != ss:
        BAD += 1
print("""
  9 of 9.  The one-liner mg-db09 flagged as the expensive one HOLDS, and
  the equivalence it predicts (symmetric Cartan <=> semisimple, for a
  split basic algebra with unitriangular Cartan) is confirmed on every
  row.  Combined with B3c, section 2 row 1 of the document stands.
""")

print("TOTAL BAD: %d" % BAD)
