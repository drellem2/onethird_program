"""The e(P)-controlled comparison of section 4, done on EVERY e-group that contains
an extremal poset -- which is where the document's universal sentence lives.
"""

from fractions import Fraction

from records import build_all

for n in (5, 6, 7):
    recs = build_all(n)
    pop = [r for r in recs if not r.chain and r.tie_free and r.qmass is not None]
    dmin = min(r.delta for r in pop)
    ext = [r for r in pop if r.delta == dmin]
    print("=" * 78)
    print("n = %d : tie-free non-chains = %d, extremal = %d (delta = %s)"
          % (n, len(pop), len(ext), dmin))
    for E in sorted(set(r.e for r in ext)):
        grp = [r for r in pop if r.e == E]
        ge = [r for r in grp if r.delta == dmin]
        sat = [r for r in grp if r.qmass == 1]
        print("  e(P) = %-3d : group size %-3d, extremal in it %-2d, qmass = 1 in it %-2d"
              % (E, len(grp), len(ge), len(sat)))
        print("      qmass values in the group: %s"
              % sorted(set(str(r.qmass) for r in grp)))
        if len(sat) == len(ge) and len(sat) < len(grp):
            # exact separation inside the control group
            from math import comb
            print("      *** WITHIN THIS e-GROUP qmass = 1 PICKS OUT EXACTLY THE"
                  " EXTREMAL POSETS: %d of %d." % (len(ge), len(grp)))
            print("      *** under a null that puts %d marks at random on %d posets the"
                  " chance is 1/%d = %.4f"
                  % (len(sat), len(grp), comb(len(grp), len(sat)),
                     1.0 / comb(len(grp), len(sat))))
        elif len(sat) > len(ge):
            print("      (qmass = 1 also holds for %d non-extremal member(s): no"
                  " separation here)" % (len(sat) - len(ge)))
    print()
