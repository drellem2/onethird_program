"""T4 --- every quotation in the document, checked against the extraction.

`sources_db09.txt` holds the pdftotext windows the quotations were taken from,
captured by `fetch_sources.sh` (the only script here that uses the network;
`run_all.sh` does not call it).  This script checks that each quoted string
occurs VERBATIM in its window after whitespace normalisation, and it also
runs a set of NEGATIVE controls --- strings that are almost the quotation ---
so that the check is known to be able to fail.

mg-af28 and mg-7d75 both had quotation defects found by their audits, both
caused by a Flate-decode-and-scrape extractor.  pdftotext is a renderer-grade
extractor, so the characters below are the ones on the page; what it still
does is break lines mid-sentence, which is why every comparison here is
whitespace-normalised.
"""

import re
import sys

HERE = __file__.rsplit('/', 1)[0]
BAD = 0


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def load():
    txt = open(HERE + '/sources_db09.txt', encoding='utf-8').read()
    blocks = {}
    cur = None
    for line in txt.split('\n'):
        if line.startswith('### '):
            cur = line[4:].split()[0]
            blocks[cur] = []
        elif cur:
            blocks[cur].append(line)
    return {k: norm(' '.join(v)) for k, v in blocks.items()}


BLOCKS = load()

QUOTES = [
    ("OV-branching",
     "The same definition of the branching graph applies to any chain"),
    ("OV-branching",
     "of finite-dimensional semisimple algebras"),
    ("OV-branching",
     "If the multiplicities of all restrictions are equal 0 or 1, then this "
     "diagram is a graph (and not multigraph); in this case one says that the "
     "multiplicities are simple or the branching is simple."),
    ("OV-canonical",
     "If the branching is simple, the decomposition"),
    ("OV-canonical",
     "into the sum of irreducible G(n − 1)-modules is canonical."),
    ("OV-canonical",
     "Such chains are increasing paths from"),
    ("OV-wedderburn",
     "Recall the following fundamental isomorphism:"),
    ("OV-wedderburn",
     "Proposition 1.1. The algebra GZ(n) is the algebra of all operators "
     "diagonal in the Gelfand–Tsetlin basis. In particular, it is a "
     "maximal commutative subalgebra of C[G(n)]."),
    ("OV-prop14",
     "Remark 1.3. For an arbitrary inductive family of semisimple algebras, "
     "the GZsubalgebra is a maximal commutative subalgebra if and only if the "
     "branching graph has no multiple edges."),
    ("OV-prop14",
     "(1) The restriction of any finite-dimensional irreducible complex "
     "representation of the algebra M to N has simple multiplicities."),
    ("OV-prop14",
     "(2) The centralizer Z(M, N ) is commutative."),
    ("TL-prop41",
     "Then, we have an exact sequence of TLn−1 -modules,"),
    ("TL-cor46",
     "Corollary 4.6. When q is not a root of unity, TLn is a semisimple "
     "algebra"),
    ("TL-wedderburn",
     "Theorem B.1 (Wedderburn). Let A be a complex, finite-dimensional, "
     "semisimple, associative algebra."),
    ("TL-wedderburn",
     "Wedderburn’s theorem does not hold when semisimplicity is relaxed."),
    ("MSS-thm418",
     "Theorem 4.18. Let B be a connected left regular band with support "
     "semilattice"),
    ("MSS-thm418",
     "is unipotent lower triangular with respect to any linear extension of "
     "the partial order on"),
    ("MS-quasihereditary",
     "The algebras of finite (von Neumann) regular monoids provide natural "
     "and diverse examples of quasi-hereditary algebras. This was first "
     "proved by Putcha"),
    ("MS-quasihereditary",
     "Recall that a k-algebra is split basic if all its irreducible "
     "representations are one-dimensional"),
]

# strings that are ALMOST a quotation: the check must reject all of them.
CONTROLS = [
    ("OV-prop14",
     "Remark 1.3. For an arbitrary inductive family of algebras, the "
     "GZsubalgebra is a maximal commutative subalgebra if and only if the "
     "branching graph has no multiple edges."),
    ("OV-branching",
     "If the multiplicities of all restrictions are equal 0 or 1, then this "
     "diagram is a multigraph"),
    ("MSS-thm418",
     "is unipotent upper triangular with respect to any linear extension of "
     "the partial order on"),
    ("OV-canonical",
     "into the sum of irreducible G(n − 1)-modules is unique."),
    ("TL-cor46",
     "Corollary 4.6. When q is a root of unity, TLn is a semisimple algebra"),
]

print("=" * 74)
print("T4  QUOTATIONS, checked verbatim against the pdftotext extraction")
print("=" * 74)
print()
for tag, q in QUOTES:
    hay = BLOCKS.get(tag, "")
    ok = norm(q) in hay
    print("  %-22s %-6s %s" % (tag, "OK" if ok else "MISS", q[:64].replace("\n", " ")))
    if not ok:
        BAD += 1
        print("      NOT FOUND in window %s" % tag)

print()
print("  NEGATIVE CONTROLS --- each is one word away from a quotation above")
print("  and each must be rejected:")
for tag, q in CONTROLS:
    hay = BLOCKS.get(tag, "")
    found = norm(q) in hay
    print("  %-22s %-10s %s" % (tag, "REJECTED" if not found else "ACCEPTED",
                                q[:60]))
    if found:
        BAD += 1
        print("      a control was accepted: the check cannot fail")

print()
print("  Windows loaded: %d.  Sizes (characters): %s" %
      (len(BLOCKS), {k: len(v) for k, v in sorted(BLOCKS.items())}))
print()
print("  NOT CHECKED HERE, and flagged in the document instead:")
print("   * Graham-Lehrer, Cellular algebras, Invent. Math. 123 (1996) --- the")
print("     statement that a cellular algebra has a SYMMETRIC Cartan matrix is")
print("     taken from a SECONDARY source (the Wikipedia article on cellular")
print("     algebras, which states it without proof) and the original was NOT")
print("     read.  It is the one load-bearing citation here that is not from a")
print("     PDF I have on disk.")
print("   * Goodman-de la Harpe-Jones, Coxeter Graphs and Towers of Algebras")
print("     (MSRI 14, 1989), Chapter 2 --- located, NOT read; it is not")
print("     openly available and nothing here depends on it.")
print("   * Putcha, J. Algebra 205 (1998) 53-76 --- located, NOT read.  It is")
print("     quoted at second hand THROUGH Margolis-Steinberg, whose sentence")
print("     naming it is checked above.")

print()
print("TOTAL BAD: %d" % BAD)
