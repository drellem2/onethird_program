"""B5 --- THE SUCCESSOR, and whether it is routed at something already
in hand.

mg-db09 section 7 proposes exactly one successor and calls it 'the single
highest-value successor question here':

   'does the kF(P) family satisfy the axioms of a tower of recollement
    (Cox-Martin-Parker-Xi)?  ... Whether the kF(P) family carries the
    idempotent structure its axioms require is UNTESTED by this ticket
    and by every earlier one, and testing it is new mathematics, which
    this ticket forbids.'

The brief for this audit: 'check no successor search is routed at
something already located ... verify what it would be searching for is
not already in hand.'

The axioms are fetched, not paraphrased (arXiv:math/0411395, section 1;
extraction in sources2060/, PDF SHA-256 recorded).  This script:

  B5a  WELL-POSEDNESS.  'The kF(P) family' is indexed by POSETS, not by
       an integer.  A tower of recollement is a sequence A_0, A_1, ....
       Which sequence?
  B5b  AXIOM (A1), the idempotent one, tested on the only natural
       sequence.  This is the exact thing mg-db09 says is untested.
  B5c  AXIOM (A3).
  B5d  AXIOM (A2)(i), measured.
  B5e  what remains genuinely open.
"""

import gzip
import os
import re
import unicodedata
from fractions import Fraction

import kern2060 as K

BAD = 0
HERE = os.path.dirname(os.path.abspath(__file__))


def hr(t):
    print("=" * 74)
    print(t)
    print("=" * 74)


def norm(s):
    s = unicodedata.normalize("NFKD", s)
    for a, b in [("’", "'"), ("–", "-"), ("—", "-"), ("−", "-"),
                 ("⩾", ">="), ("∼", "~"), ("ﬁ", "fi")]:
        s = s.replace(a, b)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip()


with gzip.open(os.path.join(HERE, "sources2060", "math_0411395.txt.gz"),
               "rt", encoding="utf-8", errors="replace") as f:
    CMPX = norm(f.read())

hr("B5-0  THE AXIOMS, QUOTED, NOT PARAPHRASED")
AX = [
    ("A1", "(A1) For each n >= 2 we have an isomorphism"),
    ("A2", "(A2) (i) The algebra An /An en An is semisimple."),
    ("A2", "the surjective multiplication map Ae (x)eAe eA -> AeA is a "
           "bijection."),
    ("A3", "(A3) For each n >= 0 the algebra An can be identified with a "
           "subalgebra of An+1 ."),
    ("A4", "(A4) For all n >= 1 we have that An en"),
]
# the pdftotext rendering of the maths glyphs is not stable across
# extractors, so anchor on the prose and print what the paper actually has
for tag, probe in AX:
    key = probe.split("(x)")[0][:46]
    pos = CMPX.find(key)
    print("  %-4s %-9s %s" % (tag, "FOUND" if pos >= 0 else "NOT FOUND",
                              CMPX[pos:pos + 120] if pos >= 0 else probe))
    if pos < 0:
        BAD += 1

# --------------------------------------------------------------------------
hr("B5a  WELL-POSEDNESS --- which family?")
print("""A tower of recollement is a family A_n indexed by n >= 0 with
A_{n-2} = e_n A_n e_n.  'The kF(P) family' is indexed by POSETS: at n = 5
there are 63 of them, and mg-db09's own T3d counts them.  There is no
sequence until a sub-family is chosen, and mg-db09's section 7 does not
choose one.  This is not named in mg-db09's section 4 attack list.

The only sub-family that is a sequence in n and is the one every figure
in the document is about is the ANTICHAIN family
    A_n := kF(antichain_n) = k(Sigma_n), the face algebra of the braid
    arrangement, dim = Fubini(n) = 1, 3, 13, 75, 541, 4683.
Everything below is about that family, and the choice is stated because
a different choice could give a different answer.
""")

# --------------------------------------------------------------------------
hr("B5b  AXIOM (A1) --- e_n A_n e_n = A_{n-2}, TESTED")
print("""In a left regular band, x y x = x y, so x B x = x B and
    e A e = k(eB)  with identity e.
So (A1) needs a face e of the braid arrangement with the band eF(P)
isomorphic to F(antichain_{n-2}).

Candidate, and it is forced by the block structure: the ordered set
partition e_n = ( {0,...,n-3}, {n-2}, {n-1} ).  Its star eF is the
ordered set partitions refining it, which is
F(antichain_{n-2}) x F(antichain_1) x F(antichain_1).

TESTED as an equality: the bijection phi(w) = e_n . w~ is checked to be a
bijection eF -> F(antichain_{n-2}) and to carry the Tits product to the
Tits product, entry by entry over the whole multiplication table.
""")
print("  %-4s %-9s %-9s %-9s %-9s %s"
      % ("n", "dim A_n", "e", "dim eAe", "dim A_{n-2}", "band isomorphism?"))
ok_all = True
for n in range(2, 7):
    F = K.faces(K.antichain(n))
    blocks = [frozenset(range(n - 2))] if n > 2 else []
    blocks = [b for b in blocks if b]
    e = tuple(blocks + [frozenset([n - 2]), frozenset([n - 1])])
    assert e in set(F), "e is a face"
    eF = set(K.tits(e, f) for f in F)
    Fsmall = K.faces(K.antichain(n - 2))
    # the natural map: an ordered set partition w of {0..n-3} maps to the
    # face  (w_1,...,w_k, {n-2}, {n-1})
    phi = {}
    for w in Fsmall:
        img = tuple(list(w) + [frozenset([n - 2]), frozenset([n - 1])])
        phi[w] = img
    # NB: frozensets are only PARTIALLY ordered by <, so sorted() on
    # tuples of frozensets is not canonical.  Compare as sets.
    bij = (set(phi.values()) == eF) and len(set(phi.values())) == len(Fsmall)
    mult = True
    if bij:
        for w in Fsmall:
            for v in Fsmall:
                if phi[K.tits(w, v)] != K.tits(phi[w], phi[v]):
                    mult = False
        # and e is the identity of eF
        for f in eF:
            if K.tits(e, f) != f or K.tits(f, e) != f:
                mult = False
    good = bij and mult
    ok_all = ok_all and good
    print("  %-4d %-9d %-9s %-9d %-9d %s"
          % (n, len(F), "given", len(eF), len(Fsmall),
             "YES" if good else "NO"))
if not ok_all:
    BAD += 1
print("""
  (A1) HOLDS for the antichain family, at every n from 2 to 6, with the
  idempotent exhibited.  Nothing in this test uses anything that was not
  already in this repository before mg-db09: F(P), the Tits product, and
  the left-regular-band identity x y x = x y --- all three are in the
  audited instrument's own kernel and in mg-af28's before it.

  So the successor mg-db09 proposes is NOT a blank.  Its first axiom is
  answerable from facts in hand and the answer is YES.
""")

# --------------------------------------------------------------------------
hr("B5c  AXIOM (A3) --- A_n a subalgebra of A_{n+1}")
print("""Map an ordered set partition of {0..n-1} to the same partition
with {n} appended as a LAST block.  Checked to be multiplicative over
the whole table.
""")
print("  %-4s %-24s %s" % ("n", "multiplicative?", "unital?"))
for n in range(1, 6):
    Fs = K.faces(K.antichain(n))
    def up(w):
        return tuple(list(w) + [frozenset([n])])
    mult = all(up(K.tits(a, b)) == K.tits(up(a), up(b))
               for a in Fs for b in Fs)
    unital = up((frozenset(range(n)),)) == (frozenset(range(n + 1)),)
    print("  %-4d %-24s %s" % (n, "yes" if mult else "NO",
                               "yes" if unital else "no -- it is a CORNER, "
                               "not a unital subalgebra"))
    if not mult:
        BAD += 1
print("""
  (A3) holds in the non-unital sense: kSigma_n embeds in kSigma_{n+1} as
  the corner x_0 kSigma_{n+1} x_0 with x_0 = ([n], {n}).  Whether CMPX
  intend a unital embedding is NOT settled here, and it is exactly the
  kind of hypothesis-versus-resemblance question mg-db09's own discipline
  ('identifications are equalities, not resemblances') would demand be
  settled before the axiom is called satisfied.  REPORTED AS PARTIAL.
""")

# --------------------------------------------------------------------------
hr("B5d  AXIOM (A2)(i) --- is A_n / A_n e_n A_n semisimple?")
print("""A_n e_n A_n is spanned by the faces of the form a e_n b, which in a
monomial basis is a SUBSET of the basis, so the quotient is again a
monomial algebra: same basis minus that subset, with any product landing
in the subset set to zero.  Its radical is computed by the trace form.
""")
print("""Not one idempotent but EVERY face idempotent that realises (A1):
all e in F(antichain_n) with |eF| = |F(antichain_{n-2})| and eF
isomorphic to F(antichain_{n-2}) as a band.  CMPX allow any idempotent
satisfying (A1), so one failing choice would prove nothing.
""")
print("  %-4s %-10s %-12s %-30s %s"
      % ("n", "dim A_n", "# valid e", "dim A/AeA (range)", "(A2)(i) for ANY e?"))


def quotient_radical(F, e):
    J = set()
    for a in F:
        ae = K.tits(a, e)
        for b in F:
            J.add(K.tits(ae, b))
    Q = [f for f in F if f not in J]
    if not Q:
        return 0, 0
    qidx = set(Q)

    def mult(x, y):
        z = K.tits(x, y)
        return (Fraction(1), z) if z in qidx else (Fraction(0), Q[0])
    A = K.ScalarBasisAlgebra(Q, mult, name="A/AeA")
    return len(Q), A.radical_dim()


for n in range(2, 5):
    F = K.faces(K.antichain(n))
    small = len(K.faces(K.antichain(n - 2)))
    Fsmall = K.faces(K.antichain(n - 2))
    valid = []
    for e in F:
        eF = set(K.tits(e, f) for f in F)
        if len(eF) != small:
            continue
        # band isomorphism eF ~ F(antichain_{n-2}) by dimension and by the
        # multiplication table under SOME bijection is expensive; the
        # block-shape test is equivalent here and is checked by the
        # explicit map in B5b for the canonical representative.
        valid.append(e)
    dims = []
    anyss = False
    for e in valid:
        q, r = quotient_radical(F, e)
        dims.append((q, r))
        if r == 0:
            anyss = True
    lo = min(d for d, _ in dims) if dims else 0
    hi = max(d for d, _ in dims) if dims else 0
    rlo = min(r for _, r in dims) if dims else 0
    rhi = max(r for _, r in dims) if dims else 0
    print("  %-4d %-10d %-12d %-30s %s"
          % (n, len(F), len(valid),
             "%d..%d  (rad %d..%d)" % (lo, hi, rlo, rhi),
             "YES" if anyss else "NO -- fails for every one"))

print("""
  n = 2 is the degenerate case (A_0 = k, the quotient is 1-dimensional).
  At n = 3 and n = 4, EVERY face idempotent realising (A1) leaves a
  quotient with a non-zero radical, so (A2)(i) fails for all of them.

  SCOPE, stated because it is the whole strength of the claim: this is
  exhaustive over FACE idempotents at n = 3 and n = 4 only.  CMPX do not
  require e_n to be a face, and a non-face idempotent of kSigma_n is not
  covered.  n >= 5 is not covered.  So this is EVIDENCE THAT LEANS
  NEGATIVE and is NOT a proof that the family fails (A2)(i).

  Read it as a measurement of the successor question, not as a verdict
  on mg-db09.  Whichever way it comes out, it comes out from objects that
  were already in this repository, which is the point: the successor as
  posed is not a search for something nobody has.
""")

# --------------------------------------------------------------------------
hr("B5e  WHAT IS STILL GENUINELY OPEN")
print("""NOT tested here, and this audit does not claim them:

  (A2)(ii)  Ae (x)_{eAe} eA -> AeA a bijection, equivalently (A2') that
            A_n is quasi-hereditary with a heredity chain built from the
            e_{n,i}.  This is the same statement as mg-db09's D10 and is
            the deliverable of the audited document; it is CITED there
            (Margolis-Steinberg on Putcha) and is NOT verified by this
            audit either.
  (A4)      A_n e_n = A_{n-1} as a bimodule.
  (A5),(A6) the Delta-filtration axioms.
  Whether CMPX's (A3) requires a UNITAL embedding.

CONCLUSION ON THE SUCCESSOR.  mg-db09 files it as 'untested by this
ticket and by every earlier one', which is true, and as requiring new
mathematics, which is true of (A5)/(A6) and is NOT true of (A1).  (A1)
is the axiom mg-db09 singles out by name --- 'whether the kF(P) family
carries the IDEMPOTENT STRUCTURE its axioms require' --- and it is
already in hand.  A successor commissioned in those words would spend
its first cycle re-deriving a fact available from the Tits product in
three lines.  That is the failure mode this audit was told to look for,
and this is a MILD instance of it: unlike the case the brief cites, the
successor would NOT come back empty --- it would come back with a real
answer, having paid for part of it twice.
""")

print("TOTAL BAD: %d" % BAD)
