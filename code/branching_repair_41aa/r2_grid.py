"""R2 -- the repair of X2: section 0 consequence 3's sentence about Brown's own
example lattice.

WHAT WAS WRONG.  mg-af28 section 0 consequence 3 said:

    "His worked section 4.3 example is the p x q grid of lattice paths ...
     that grid is J(C_p + C_q), which for p, q >= 1 is NOT an interval of
     Young's lattice -- D_lambda has a minimum and C_p + C_q does not."

The reason is TRUE and the conclusion is FALSE, and the gap between them is
exactly the gap X1 opens: "D_lambda has a minimum" rules out intervals of the
form [empty, lambda] and says nothing about a general interval [mu, lambda],
whose poset is a skew shape and need not have a minimum.  This is one of the
three elementary derivations mg-af28 flagged as its own and pre-filed for
audit at its section 5 item 5(c).

WHAT THIS FILE DOES, AND WHAT A FALSIFIER WOULD HAVE LOOKED LIKE.

  R2a  Is the first half right?  Build the grid {0..p} x {0..q} DIRECTLY as a
       product of two integer intervals -- not as J of anything -- and check it
       is J(C_p + C_q).  FALSIFIER: a p, q where the two differ.  (af28 gets
       this half right; it is checked because the sentence's second half is
       what fails, and the two must not be confused.)

  R2b  Is the reason right?  Check that C_p + C_q is not isomorphic to any
       straight cell poset D_lambda with p + q cells.  FALSIFIER: one that is.
       This is what the sentence's stated reason actually establishes, and it
       is all it establishes.

  R2c  Is the conclusion right?  Construct the interval [(q), (q+p, q)] from
       CONTAINMENT of partitions, construct the map from the grid to it, and
       verify it is a bijection and an order isomorphism pair by pair, for
       every p, q <= 5.  FALSIFIER: any pair where no such map exists, or
       where the constructed map fails a check.

  R2d  What the correction does to the document.  Consequence 3's real claim --
       that Brown does not make the identification -- rests on the keyword
       census (ledger B8), which mg-6ad0 re-ran ligature-aware and confirmed.
       That claim is untouched.  What changes is that Brown's own worked
       example turns out to BE a Young-lattice interval, which makes the
       contact closer than mg-af28 said, not further.
"""

import sys
from kern41aa import (grid, chain, disjoint_union, ideal_lattice, ideals, iso,
                      canon, partitions, skew_poset, interval_poset,
                      young_interval, sub, cells)

OUT = sys.stdout
TOP = 5


def r2a():
    print("=" * 78, file=OUT)
    print("R2a  The FIRST half of the sentence: the grid is J(C_p + C_q).", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   p  q   |grid|   |J(C_p + C_q)|   isomorphic", file=OUT)
    bad = 0
    for p in range(1, TOP + 1):
        for q in range(1, TOP + 1):
            G, pts = grid(p, q)
            P = disjoint_union(chain(p), chain(q))
            J, _ = ideal_lattice(P)
            ok = iso(G, J) is not None
            if not ok:
                bad += 1
            if p <= 3 and q <= 3:
                print("  %2d %2d   %6d   %14d   %s"
                      % (p, q, G[0], J[0], "." if ok else "BAD"), file=OUT)
    print("   ... all %d pairs p, q <= %d tested." % (TOP * TOP, TOP), file=OUT)
    print(file=OUT)
    print("  grid = J(C_p + C_q): %d bad.  af28's first half is RIGHT." % bad, file=OUT)
    print(file=OUT)
    return bad


def r2b():
    print("=" * 78, file=OUT)
    print("R2b  The REASON: C_p + C_q has no minimum, D_lambda does.  What that", file=OUT)
    print("     establishes, and all it establishes.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   p  q   C_p+C_q = some D_lambda with p+q cells?", file=OUT)
    bad = 0
    for p in range(1, TOP + 1):
        for q in range(1, TOP + 1):
            P = disjoint_union(chain(p), chain(q))
            straight = {canon(skew_poset(l)[0]) for l in partitions(p + q)}
            hit = canon(P) in straight
            if hit:
                bad += 1
            if p <= 3 and q <= 3:
                print("  %2d %2d   %s" % (p, q, "YES -- reason FAILS" if hit else "no"),
                      file=OUT)
    print("   ... all %d pairs tested." % (TOP * TOP), file=OUT)
    print(file=OUT)
    print("  C_p + C_q is a straight cell poset in %d of %d cases.  So the"
          % (bad, TOP * TOP), file=OUT)
    print("  stated reason is TRUE: the grid is not [empty, lambda] for any", file=OUT)
    print("  lambda.  It says nothing about [mu, lambda] with mu nonempty --", file=OUT)
    print("  and that is the whole of the defect.", file=OUT)
    print(file=OUT)
    return bad


def r2c():
    print("=" * 78, file=OUT)
    print("R2c  The CONCLUSION: is the grid an interval of Young's lattice?", file=OUT)
    print("     lambda = (q+p, q), mu = (q).  Row 0 keeps columns q..q+p-1 and", file=OUT)
    print("     row 1 keeps columns 0..q-1, so the two blocks are incomparable.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    print("   p  q   lambda / mu        |[mu,lam]|  (p+1)(q+1)  map built  map verified",
          file=OUT)
    bad = 0
    for p in range(1, TOP + 1):
        for q in range(1, TOP + 1):
            lam, mu = (q + p, q), (q,)
            G, pts = grid(p, q)
            IP, iv = interval_poset(mu, lam)
            phi = iso(G, IP)
            built = phi is not None
            ok = False
            if built:
                # verify the constructed map on every pair, both directions
                ok = True
                n, dG = G
                m, dI = IP
                for a in range(n):
                    for b in range(n):
                        if bool(dG[b] >> a & 1) != bool(dI[phi[b]] >> phi[a] & 1):
                            ok = False
                if len(set(phi)) != n or n != m:
                    ok = False
                if len(iv) != (p + 1) * (q + 1):
                    ok = False
            if not (built and ok):
                bad += 1
            if p <= 4 and q <= 4:
                print("  %2d %2d   %-16s  %9d  %10d  %9s  %12s"
                      % (p, q, "%s / %s" % (str(lam), str(mu)), len(iv),
                         (p + 1) * (q + 1), "yes" if built else "NO",
                         "yes" if ok else "NO"), file=OUT)
    print("   ... all %d pairs p, q <= %d tested." % (TOP * TOP, TOP), file=OUT)
    print(file=OUT)
    print("  REFUTED BY CONSTRUCTION, %d bad of %d: Brown's own section 4.3"
          % (bad, TOP * TOP), file=OUT)
    print("  example lattice IS the interval [(q), (q+p, q)] of Young's", file=OUT)
    print("  lattice.  Reproduces mg-6ad0's A2b (16 pairs) on a third", file=OUT)
    print("  instrument, over 25, with the grid built as a product of chains", file=OUT)
    print("  rather than as J(C_p + C_q).", file=OUT)
    print(file=OUT)
    return bad


def r2d():
    print("=" * 78, file=OUT)
    print("R2d  A worked instance, printed in full, so the correction is legible", file=OUT)
    print("     rather than tabular: p = 2, q = 3.", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)
    p, q = 2, 3
    lam, mu = (q + p, q), (q,)
    print("  lambda = %s, mu = %s.  The skew diagram lambda/mu (X = a cell):"
          % (str(lam), str(mu)), file=OUT)
    cs = cells(lam, mu)
    for i in range(len(lam)):
        row = ""
        for j in range(lam[0]):
            row += "X" if (i, j) in cs else ("." if j < (mu[i] if i < len(mu) else 0)
                                             else " ")
        print("      %s" % row, file=OUT)
    print(file=OUT)
    print("  the interval [%s, %s], %d partitions:" % (str(mu), str(lam),
                                                       len(young_interval(mu, lam))),
          file=OUT)
    for nu in young_interval(mu, lam):
        print("      %s" % (str(nu),), file=OUT)
    print(file=OUT)
    print("  |[mu, lambda]| = %d = (p+1)(q+1) = %d, which is the size of the"
          % (len(young_interval(mu, lam)), (p + 1) * (q + 1)), file=OUT)
    print("  %d x %d grid of lattice paths in Brown's section 4.3." % (p, q), file=OUT)
    print(file=OUT)
    print("  WHAT IS NOT TOUCHED.  Consequence 3's claim is that BROWN DOES NOT", file=OUT)
    print("  MAKE THE IDENTIFICATION.  That rests on the keyword census (ledger", file=OUT)
    print("  B8), which mg-6ad0 re-ran ligature-aware and confirmed: all twelve", file=OUT)
    print("  keywords absent in both spellings.  The claim stands; the sentence", file=OUT)
    print("  offered in support of it does not.  And the correction runs TOWARD", file=OUT)
    print("  the headline, not away from it: Brown's own worked example lattice", file=OUT)
    print("  is an interval of Young's lattice, so the contact is closer than", file=OUT)
    print("  mg-af28 said, on a point mg-af28 used to argue it was further.", file=OUT)
    print(file=OUT)


def main():
    a = r2a()
    b = r2b()
    c = r2c()
    r2d()
    print("=" * 78, file=OUT)
    print("SUMMARY r2_grid: grid = J(C_p+C_q) bad %d; C_p+C_q a straight cell"
          % a, file=OUT)
    print("  poset %d of %d; interval constructions bad %d of %d"
          % (b, TOP * TOP, c, TOP * TOP), file=OUT)
    print("=" * 78, file=OUT)


if __name__ == "__main__":
    main()
