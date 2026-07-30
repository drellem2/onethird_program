"""B6 --- THE 'DO NOT DEVELOP' INSTRUCTION, MEASURED, and mg-db09's own
claim ledger re-scored.

mg-db09's brief: 'This is a locating exercise.  Do not develop new
mathematics.'  mg-db09's delivery: 'Scope, and it is the whole of the
scope ... It develops no mathematics' (opening), and 'It does not develop
mathematics.  Two objects are CONSTRUCTED (T1, T2) because the brief
asked for exactly those two objects ... Four elementary one-line
derivations were needed and each is flagged in place' (section 7).

The instruction and the compliance claim are both assertions to test.
This script does two things:

  B6a  A DERIVATION CENSUS.  Every mathematical step in the delivered
       document, classified LOCATED-AND-CITED / CONSTRUCTED-AS-COMMISSIONED
       / DEVELOPED-HERE, with whether mg-db09 flagged it.  The measurement
       is the count of DEVELOPED-HERE steps that mg-db09 did NOT flag.
  B6b  THE LEDGER, re-scored: every numeric claim in D1..D13 that this
       audit can check, checked.
"""

from fractions import Fraction
from itertools import permutations

import kern2060 as K

BAD = 0


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


# --------------------------------------------------------------------------
hr("B6a  DERIVATION CENSUS")
print("""Legend
  CITED     located in a source, and this audit found the source text
  ASKED     an object CONSTRUCTED because the brief asked for it by name
  MINE      a derivation performed in mg-db09 and not taken from a source
  flag      did mg-db09 flag it as its own?
""")

CENSUS = [
    # (where, what, class, flagged by mg-db09?, this audit's finding)
    ("sec 0 bullets 1-4",
     "Daniel's sentence = VO section 1, hypotheses separated",
     "CITED", "n/a", "4 passages verbatim (B3b); 1 of 22 doc quotations "
     "deviates by an inserted comma"),
    ("sec 0 bullet 3",
     "C[G(n)] = sum End(V^lambda) is Wedderburn, needs semisimplicity alone",
     "CITED", "n/a", "quoted; and the CONVERSE is elementary -- see below"),
    ("sec 0 / T1",
     "TL_n(beta) at beta = 3,2,1,0 built and measured",
     "ASKED", "yes (sec 4 item 6)",
     "reproduces; but see the branching-graph finding in B1"),
    ("sec 0 / T2",
     "C S_4 on skipped chains and C inside M_2(C) built",
     "ASKED", "yes (sec 4 item 6)", "reproduces"),
    ("sec 0 / T1d",
     "'a path-pair BASIS survives without semisimplicity', from "
     "dim A = sum (dim V)^2",
     "MINE", "NO", "REFUTED in the 'if' direction -- B2"),
    ("sec 0 / T1b",
     "'the branching graph is the same multiplicity-free graph at each beta'",
     "MINE", "partly (sec 4 item 3, as a 'dimension shadow')",
     "FALSE under VO's definition: different vertex sets AND "
     "multiplicities >= 2 -- B1"),
    ("sec 1 table row 3",
     "'multiplicities in {0,1}, equivalently (VO Prop 1.4) Z(M,N) "
     "commutative' -- stated with no semisimplicity qualifier",
     "MINE", "NO",
     "the equivalence FAILS off semisimplicity, measured on mg-db09's own "
     "example: Z commutative at beta = 1 and 0 while multiplicities are 2 "
     "-- B1c"),
    ("sec 0 2x2 table / D4",
     "the synthesis: semisimplicity load-bearing, multiplicity-freeness not",
     "MINE", "yes (D4, sec 4 item 6)",
     "the VERDICT stands but is FORCED, not measured -- see B6a note"),
    ("sec 7 item (a) / D9",
     "symmetric AND unitriangular implies the identity",
     "MINE", "yes", "executed and holds, 9 of 9 -- B4c"),
    ("sec 7 item (b) / D10",
     "a band is a von Neumann regular monoid",
     "MINE", "yes", "not checked by this audit"),
    ("sec 7 item (c) / D6",
     "all kF(P) irreducibles 1-dim, so all branching is multiplicity-free",
     "MINE", "yes, and NOT booked as evidence", "consistent"),
    ("sec 7 item (d) / D8",
     "kF(P) semisimple iff |F(P)| = |AC(P)|",
     "MINE", "yes", "verified on all 87 classes to n <= 5 -- B4a, B6b"),
    ("T3c / sec 2 row 1",
     "'an algebra with identity Cartan matrix and one-dimensional simples "
     "is semisimple', and hence LRB-cellular = semisimple IN GENERAL",
     "MINE", "NO -- section 7's list of four does not contain it",
     "TRUE (dim A = sum C = #simples = dim A/rad), but it is a fifth "
     "one-liner and a claim about two whole classes of algebra, not "
     "about kF(P)"),
    ("sec 0 / D9",
     "a cellular algebra has a symmetric Cartan matrix",
     "CITED (secondary)", "yes -- flagged as the weakest citation",
     "UPGRADED: stated and attributed in a refereed source -- B3c"),
    ("sec 0 / D10",
     "regular monoid algebras are quasi-hereditary (Putcha, via "
     "Margolis-Steinberg)",
     "CITED", "yes -- primary not read", "quotation verbatim (B3b); the "
     "APPLICATION to kF(P) is NOT verified by this audit either"),
    ("sec 0 / T3c",
     "the Cartan matrix of kF(P) is unipotent lower triangular",
     "CITED (MSS Thm 4.18) + rebuilt", "yes (sec 4 item 4)",
     "rebuilt from formula (4.9), agrees on all 9 rows -- B4b"),
    ("sec 3",
     "TL semisimplicity controls (Ridout-Saint-Aubin)",
     "CITED", "n/a", "all six reproduced independently -- selftest2060"),
]

nmine = nunflagged = 0
for (where, what, cls, flag, finding) in CENSUS:
    if cls == "MINE":
        nmine += 1
        if flag.startswith("NO"):
            nunflagged += 1
    print("  [%-4s] %-22s %s" % (cls[:4], where, what))
    print("           mg-db09 flags it: %s" % flag)
    print("           this audit      : %s" % finding)
    print()

print("  DERIVATIONS PERFORMED IN mg-db09 RATHER THAN LOCATED : %d" % nmine)
print("  OF THOSE, NOT FLAGGED BY mg-db09                     : %d"
      % nunflagged)
print("""
  mg-db09's section 7 says 'Four elementary one-line derivations were
  needed and each is flagged in place'.  The count of derivations that
  are mg-db09's own is larger than four, and %d of them are not in that
  list.  Two of the three unflagged ones are WRONG or OVERSTATED (the
  path-pair basis, the parameter-independent branching graph); the third
  is true.
""" % nunflagged)

print("""  A NOTE ON WHAT T1 AND T2 CAN ESTABLISH, which no list names.
  The conclusion under test is 'A is a direct sum of endomorphism
  algebras'.  A finite direct sum of full matrix algebras over a field IS
  semisimple.  So

      A = sum_lambda End(V_lambda)   =>   A semisimple

  for EVERY finite-dimensional algebra, with no hypothesis at all.  The
  half of the verdict that says 'failure of semisimplicity BREAKS the
  conclusion' is therefore not something an example could have refuted:
  it is the contrapositive of Wedderburn's easy direction, which mg-db09
  quotes.  Likewise 'semisimple => the conclusion survives' is Wedderburn
  itself and needs no branching hypothesis, which mg-db09 also says.

  What T1 and T2 DO establish is the EXISTENCE of towers in the two
  off-diagonal cells --- that both hypothesis-combinations are inhabited.
  That is real and it is worth having.  But mg-db09's section 0 says
  'Both halves are settled here by BUILDING the object each would
  forbid', which credits the builds with settling the verdict.  The
  verdict was settled by the quoted theorem; the builds settled that the
  cells are non-empty.

  This is the SAME critique mg-db09 applies to itself at D6 ('forced for
  every P of every size, so a measurement of it could not do any work')
  and does NOT apply to the conclusion columns of D2 and D3, where it
  also applies.
""")

# --------------------------------------------------------------------------
hr("B6b  THE LEDGER, re-scored on the numbers this audit can check")


def sym_group_algebra(n):
    G = list(permutations(range(n)))

    def mult(a, b):
        return (Fraction(1), tuple(a[b[i]] for i in range(n)))
    return K.ScalarBasisAlgebra(G, mult, name="CS_%d" % n)


rows = []

# D5 / D8 : |F|, |AC|, radical, and the semisimplicity census
census = {}
for n in range(1, 6):
    ss = []
    for P in K.poset_classes(n):
        F = K.faces(P)
        A = K.AC(P)
        if len(F) == len(A):
            ss.append(P)
    census[n] = (len(K.poset_classes(n)), len(ss), ss)

A5 = K.band_algebra(K.antichain(5))
r5 = A5.dim - A5.radical_dim()
pct5 = 100.0 * (A5.dim - r5) / A5.dim
f6 = len(K.faces(K.antichain(6)))
a6 = len(K.AC(K.antichain(6)))
pct6 = 100.0 * (f6 - a6) / f6

rows.append(("D5", "dim kF/rad = |AC| on all classes to n <= 5",
             "87 of 87, 0 bad, NO CAP (mg-db09: 67 of 87)", "CONFIRMED+"))
rows.append(("D5", "radical 90.4%% at the n = 5 antichain",
             "541 - %d = %d, %.1f%%, from the TRACE FORM" % (r5, A5.dim - r5,
                                                             pct5),
             "CONFIRMED, and derived from the radical for the first time"))
rows.append(("D5", "radical 95.7% at n = 6",
             "4683 vs 203 -> %.1f%%, arithmetic on counts only" % pct6,
             "ARITHMETIC CONFIRMED; the identity at n = 6 NOT re-derived "
             "by this audit either"))
rows.append(("D8", "kF(P) semisimple for exactly 1 class at each n <= 5",
             "; ".join("n=%d: %d of %d" % (n, census[n][1], census[n][0])
                       for n in range(1, 6)),
             "CONFIRMED"))

CS5 = sym_group_algebra(5)
rows.append(("D11", "dim C S_5 = 120, semisimple",
             "dim %d, dim rad %d" % (CS5.dim, CS5.radical_dim()),
             "CONFIRMED"))
rows.append(("D11", "dim k Sigma_5 = 541, 90.4% radical",
             "dim %d, dim rad %d" % (A5.dim, A5.dim - r5), "CONFIRMED"))
rows.append(("D7", "Cartan unipotent lower triangular; symmetric iff "
             "semisimple",
             "9 of 9 rows by MSS formula (4.9), the route mg-db09 did not "
             "take", "CONFIRMED"))
rows.append(("D2", "TL branching graph parameter-independent and "
                   "multiplicity-free at every beta",
             "vertex sets differ at beta = 0; multiplicities reach 2 at "
             "beta = 1 and 0", "REFUTED as stated"))
rows.append(("D2", "TL path-pair count 132 at n = 6 at every beta; "
                   "sum End = 132/132/99/42",
             "reproduced exactly, all four parameters", "CONFIRMED"))
rows.append(("D3", "C S_4 semisimple on every chain; GZ not maximal "
                   "commutative on skipped chains",
             "every T2a/T2b/T2c/T2d number reproduced on a disjoint "
             "instrument (B7)", "CONFIRMED"))
rows.append(("D9", "cellular => symmetric Cartan",
             "Ehrig-Tubbenhauer Remark 2.19, attributing Koenig-Xi 1999",
             "UPGRADED from 'secondary source' to 'refereed, attributed'"))
rows.append(("D10", "kF(P) is quasi-hereditary",
             "not tested here", "NOT ESTABLISHED BY THIS AUDIT"))
rows.append(("D12", "the candidate space is the eight rows of section 2",
             "row 3 (towers of recollement) partially evaluated here: "
             "(A1) holds, (A2)(i) fails for every face idempotent at "
             "n = 3, 4", "row 3 is no longer 'not evaluated'"))

print("  %-5s %-46s %s" % ("row", "claim", "verdict"))
for (d, claim, measured, verdict) in rows:
    print("  %-5s %-46s %s" % (d, claim[:46], verdict))
    print("        measured: %s" % measured)
print()

if census[5][1] != 1 or r5 != 52 or CS5.radical_dim() != 0:
    BAD += 1

print("TOTAL BAD: %d" % BAD)
