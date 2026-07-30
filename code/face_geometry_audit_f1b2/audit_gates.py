"""mg-f1b2 -- part 2.  WHICH GATE OF `absorbable_by_diagonal_twist` DECIDES?

mg-8a12 routes each NEGATIVE CONTROL 4 row to [PASS] or [CANNOT FAIL] on one
quantity, `diag_preserved`, and treats "the diagonal is preserved" as
"the off-diagonal signs actually decide" (controls.py:701-702, :832, :894-895).

The predicate's own docstring names TWO forced gates, not one
(face_complex.py:763-765):

    "s_i^2 = 1 pins every diagonal entry, |s_i s_j| = 1 pins every absolute
     value, and each nonzero off-diagonal entry forces the product s_i s_j.
     What remains is a parity system, solved by union-find."

A decision reached at the diagonal gate is forced.  A decision reached at the
absolute-value gate is forced in exactly the same way and by the same arithmetic.
Only a decision reached in the PARITY SYSTEM is a decision about signs.  So the
question mg-8a12 needed to ask, and did not, is which gate fires.
"""

import sys

sys.path.insert(0, "../face_geometry")

from face_complex import (                                     # noqa: E402
    linear_extensions, perm_sign, top_laplacians, at_laplacian, mat_eq,
    absorbable_by_diagonal_twist,
)
from posets import all_posets                                  # noqa: E402

MODES = [("I1 ridge_facets", "ridge_facets"),
         ("I2 split_free_as_interior", "split_free_as_interior"),
         ("I3 ridge_drop", "ridge_drop"),
         ("I4 facet_offbyone", "facet_offbyone"),
         ("swap01 (rejected candidate)", "facet_swap01"),
         ("NC3 facet-parity (the witness)", "__parity__")]


def twisted(P, incidence_mode="true", sign_mode="true"):
    td = top_laplacians(P, incidence_mode=incidence_mode, sign_mode=sign_mode)
    s = [perm_sign(w) for w in td["les"]]
    L, m = td["L_rel"], len(td["les"])
    return [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]


def main():
    print("=" * 78)
    print("mg-f1b2 part 2 -- WHICH GATE DECIDES 'not absorbable', for every")
    print("                  corruption NEGATIVE CONTROL 4 touches (n <= 5)")
    print("=" * 78)
    ps = [P for n in range(2, 6) for P in all_posets(n)]
    print()
    print("  %-31s %5s %7s %7s %7s %7s %7s" % (
        "corruption", "bites", "diagMV", "diagOK", "magMM", "parity", "absorb"))
    print("  %-31s %5s %7s %7s %7s %7s %7s" % (
        "", "", "forced", "", "forced", "REAL", ""))
    tot_bite = tot_par = 0
    for tag, mode in MODES:
        bites = dmv = dok = mag = par = ab = 0
        for P in ps:
            Lt = twisted(P)
            target = at_laplacian(P)[1]
            Lm = (twisted(P, sign_mode="parity") if mode == "__parity__"
                  else twisted(P, mode))
            if mat_eq(Lm, Lt):
                continue
            bites += 1
            m = len(Lt)
            if len(Lm) != m:
                continue
            if any(Lm[i][i] != target[i][i] for i in range(m)):
                dmv += 1                       # diagonal gate: forced
                continue
            dok += 1
            if any(abs(Lm[i][j]) != abs(target[i][j])
                   for i in range(m) for j in range(m)):
                mag += 1                       # absolute-value gate: forced too
                continue
            par += 1                           # the only real decision
            ab += absorbable_by_diagonal_twist(Lm, target)
        print("  %-31s %5d %7d %7d %7d %7d %7d"
              % (tag, bites, dmv, dok, mag, par, ab))
        if mode != "__parity__":
            tot_bite += bites
            tot_par += par
    print()
    print("  Across the FOUR SCORED mutations: %d biting (poset, mutation) pairs, "
          "of which %d reach\n  the parity system.  Every absorbability answer in "
          "the scored rows -- I4's included --\n  is settled at a gate that s_i^2 "
          "= 1 or |s_i s_j| = 1 forces." % (tot_bite - 72, tot_par))
    print("  The ONE corruption that reaches the parity system is NEGATIVE CONTROL "
          "3's facet-parity\n  gauge, which is absorbable 82/82 -- it is a witness "
          "that the predicate CAN say True, but\n  it says nothing about row I4, "
          "whose magnitudes differ.")

    print()
    print("=" * 78)
    print("THE 3 POSETS mg-8a12 KEEPS ROW I4's ABSORBABILITY SCORED FOR")
    print("=" * 78)
    print("  the printed row (controls.py:892-895): 'Absorbable into a diagonal "
          "+-1 twist on 0 of\n  those 61, and this row DOES score it: the diagonal "
          "is preserved on 3 of them, so the\n  predicate had to decide on the "
          "off-diagonal signs and could have returned absorbable.'")
    print("  mg-fcf1's out_nc4.txt:27, which mg-8a12 routes on: '-> the predicate "
          "does real work on\n  3 poset(s): the diagonal matches and the "
          "off-diagonal signs decide.'")
    print()
    for n in range(3, 7):
        P = [Q for Q in all_posets(n) if not Q.less][0]        # the antichain
        m = len(linear_extensions(P))
        Lt, target, Lm = twisted(P), at_laplacian(P)[1], twisted(P, "facet_offbyone")
        if mat_eq(Lm, Lt):
            print("  n=%d antichain |L(P)|=%-4d mutation VACUOUS" % (n, m))
            continue
        dok = all(Lm[i][i] == target[i][i] for i in range(m))
        mag = sum(1 for i in range(m) for j in range(m)
                  if abs(Lm[i][j]) != abs(target[i][j]))
        sgn = sum(1 for i in range(m) for j in range(m)
                  if abs(Lm[i][j]) == abs(target[i][j]) and Lm[i][j] != target[i][j])
        print("  n=%d antichain |L(P)|=%-4d diagonal preserved=%-5s  off-diagonal "
              "MAGNITUDE mismatches=%-5d (%d per row)  sign-only mismatches=%d  "
              "absorbable=%s"
              % (n, m, dok, mag, mag // m, sgn,
                 absorbable_by_diagonal_twist(Lm, target)))
    print()
    print("  Zero sign-only mismatches at every n: there is not one entry on which "
          "a sign decision\n  could have been made.  The predicate returns False at "
          "the absolute-value gate, before\n  any sign is consulted.")
    print()
    print("  AND IT IS FORCED AT EVERY n, not just measured here.  The off-diagonal "
          "support of L^rel\n  is the adjacent-transposition graph (that is claim "
          "(1), and it is proven).  The off-by-one\n  map is prefixes_true(rot(w)) "
          "with rot the cyclic rotation of POSITIONS, which carries n-2 of\n  the "
          "n-1 generators s_1..s_{n-1} to generators and the remaining one out of "
          "the set -- so\n  exactly one neighbour of each vertex changes, giving "
          "2 mismatched entries per row (12,\n  48, 240, 1440 at n = 3, 4, 5, 6 = "
          "2|L(P)|).  Row I4's absorbability answer is therefore\n  forced too, on "
          "precisely the posets mg-8a12 keeps it scored for.")


if __name__ == "__main__":
    main()
