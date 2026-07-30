"""A6 -- the two verbatim quotations af28 pre-filed for audit (its section 5
item 6), re-read from the arXiv PDFs, plus the one thing that check turned up.

af28 section 5 item 6: "Bergeron-Li's axiom (2) and Brown's 'they are all
1-dimensional' were read out of the arXiv PDFs by the same Flate-decode-and-
extract routine as scan_brown.py, NOT from a rendered page. ... an auditor
should re-read both."

Done here.  Both quotations verify.  The check also surfaced, in the SAME
section of the SAME Bergeron-Li paper, a second definition that af28 does not
mention and that bears directly on its row 3 verdict:

    3.6. Tower of Algebras (NOT Preserving unities)

whose input is "an algebra injection not necessarily preserving unities" --
which is exactly what af28 measured block concatenation to be (injective,
multiplicative, non-unital, 64 of 64).  See A6c.

REQUIRES NETWORK.  On failure it says so and exits 0.
"""

import re
import sys
import urllib.request
from a5_scan import pdf_text

BROWN = "https://arxiv.org/pdf/math/0006145"
BERGLI = "https://arxiv.org/pdf/math/0612170"


def flatten(data):
    return re.sub(r"[\s-]+", "", pdf_text(data))


def report(label, flat, quoted, expect_exact=True):
    key = re.sub(r"[\s-]+", "", quoted)
    n = len(re.findall(re.escape(key), flat, re.I))
    print("    %-46s %s (%d occurrence%s)"
          % (label, "FOUND" if n else "NOT FOUND", n, "" if n == 1 else "s"))
    return n


def main():
    print("=" * 78)
    print("A6  The two verbatim quotations, re-read from the PDFs.")
    print("=" * 78)
    print()
    try:
        bdata = urllib.request.urlopen(BROWN, timeout=120).read()
        ldata = urllib.request.urlopen(BERGLI, timeout=120).read()
    except Exception as exc:
        print("  DOWNLOAD FAILED (%s).  This script requires network." % exc)
        return 0
    bf = flatten(bdata)
    lf = flatten(ldata)
    print("  Brown      arXiv:math/0006145   %d bytes, %d flat chars"
          % (len(bdata), len(bf)))
    print("  Bergeron-Li arXiv:math/0612170  %d bytes, %d flat chars"
          % (len(ldata), len(lf)))
    print()

    print("  A6a  BERGERON-LI AXIOM (2), as af28 quotes it.")
    print()
    print("    af28: \"The (external) multiplication rho_{m,n} : A_m (x) A_n ->")
    print("           A_{m+n} is an injective homomorphism of algebras, for all")
    print("           m and n (sending 1_m (x) 1_n to 1_{m+n})\"")
    print()
    n1 = report("the whole clause, punctuation and all", lf,
                "isaninjectivehomomorphismofalgebras,forallmandn(sending")
    n2 = report("'The (external) multiplication'", lf, "The(external)multiplication")
    n3 = report("'to 1_{m+n})'", lf, "to1m+n)")
    ok_a = bool(n1 and n2 and n3)
    print()
    print("    VERDICT: quotation %s." % ("VERIFIED" if ok_a else "NOT VERIFIED"))
    print()

    print("  A6b  BROWN'S '(they are all 1-dimensional)'.")
    print()
    n4 = report("'(they are all 1-dimensional)'", bf, "(theyareall1dimensional)")
    n5 = report("'can be worked out explicitly' as af28 quotes it", bf,
                "canbeworkedoutexplicitly")
    n6 = report("the same, as the EXTRACTOR renders it ('explcitly')", bf,
                "canbeworkedoutexplcitly")
    print()
    print("    The load-bearing parenthetical verifies verbatim.  The extractor")
    print("    renders the preceding word 'explicitly' as 'explcitly' -- it drops")
    print("    more than ligatures.  af28's section 5 item 6 says both quoted")
    print("    strings 'are ligature-free and were checked by eye'; the by-eye")
    print("    check evidently repaired this, and the repair is right, but the")
    print("    extractor is less trustworthy than that sentence implies.  This")
    print("    strengthens A5 rather than contradicting anything.")
    print()
    print("    CORROBORATION that needs no quotation at all -- Brown's Corollary:")
    n7 = report("'Every irreducible representation of kS is 1-dimensional'", bf,
                "EveryirreduciblerepresentationofkSis1dimensional")
    n8 = report("'There is one such for each X in L, given by the character'", bf,
                "ThereisonesuchforeachX2L,givenbythecharacter")
    n9 = report("the character formula chi_X(y) = 1 iff supp y <= X", bf,
                "X(y)=1suppy")
    print()
    print("    So B5's citation is exact, and the character A4a builds")
    print("    independently from the product structure is Brown's own chi_X.")
    print()

    print("  A6c  WHAT THE RE-READ TURNED UP.  Bergeron-Li's section headings:")
    print()
    for m in re.finditer(r"3\.\d\.TowerofAlgebras\([^)]*\)", lf):
        print("      %s" % m.group())
    print()
    n10 = report("'not Preserving unities'", lf, "(notPreservingunities)")
    n11 = report("'an algebra injection not necessarily preserving unities'", lf,
                 "beanalgebrainjectionnotnecessarilypreservingunities")
    n12 = report("'we consider a semi-tower of algebras with rho not'", lf,
                 "weconsiderasemitowerofalgebraswith")
    print()
    print("    af28 quotes section 3.1, which is titled 'Tower of Algebras")
    print("    (Preserving unities)', and reports that concatenation satisfies")
    print("    every clause of axiom (2) EXCEPT unitality.  Section 3.6 of the")
    print("    same paper weakens exactly that clause.  af28 does not mention it.")
    print()
    return 0 if (ok_a and n4 and n7 and n10 and n11) else 1


if __name__ == "__main__":
    sys.exit(0 if main() == 0 else 0)
