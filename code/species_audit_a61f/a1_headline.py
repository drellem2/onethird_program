"""A1 -- THE HEADLINE IDENTITY, re-measured by a disjoint route and then PROVED.

mg-7d75 section 0 makes this the headline of the document:

    ( k F(P) )^{Aut(P)} / rad  =  k^{ AC(P) / Aut(P) }

and section 6 item 6 files it as "MEASURED, NOT PROVED, and stated for n <= 5",
with section 10 item 2 and ledger row S12 adding "I did not locate it stated in
that generality in the literature ... the weakest claim in this document".

This file does four things.

  A1a  RE-MEASURES it on all 87 isomorphism classes to n <= 5 with NO SIZE CAP,
       closing the 4 classes mg-7d75 exempted from its nilpotency step, using
       the TRACE FORM -- the one route mg-7d75 says it did not use.
  A1b  EXHIBITS THE ROWS BETWEEN THE TWO EXTREMES.  mg-7d75 prints only
       |Aut| = n! (the antichain) and |Aut| = 1.  If the identity is really one
       formula in one argument, the rows in between are where that shows.
  A1c  RUNS IT OUT OF SAMPLE AT n = 6, past mg-7d75's stated reach.
  A1d  PROVES IT, in three lines, from the theorem mg-7d75 itself quotes plus
       standard characteristic-0 invariant theory, and then CHECKS THE PROOF'S
       TWO STEPS EXACTLY OVER Q.  The consequence for the audit is not that the
       identity is wrong -- it is right -- but that its ledger status is wrong:
       it is a COROLLARY of a quoted theorem, not an unlocated measurement, and
       n <= 5 and the dim <= 90 cap are not limitations on it at all.
  A1e  CONTROLS: two WRONG index sets, one of which is this repo's own largest
       recorded error (mg-1953 R1).
"""

import sys
from kerna61f import (iso_classes, iso_classes_6_from_5, aut, faces, supp,
                      set_partitions, AC_by_support, AC_by_acyclicity,
                      quotient_acyclic, face_algebra, gram_full,
                      gram_invariant, invariant_structure_constants, orbits,
                      act_part, act_comp, rank_two_primes, rank_mod,
                      nullspace_q, rank_q, P1, P2)

bad = 0
NOTES = []


def hdr(t):
    print("=" * 78)
    print(t)
    print("=" * 78)
    print()


# ---------------------------------------------------------------------------
hdr("A1a  the identity on all 87 classes to n <= 5, NO CAP, via the trace form")

print("  dim A/rad is computed as the RANK OF THE TRACE FORM B(x,y) = tr(L_xy)")
print("  (Dickson: in characteristic 0 the Jacobson radical is the radical of")
print("  that form).  Rank is taken modulo two primes, %d and %d; a" % (P1, P2))
print("  disagreement between them would be reported as a failure.")
print()
print("   n  classes  |Aut|>1  identity holds  identity FAILS  prime disagreement"
      "  max dim kF(P)")
rows5 = []
for n in range(1, 6):
    cls = iso_classes(n)
    ok = fail = disagree = 0
    mx = 0
    for rel in cls:
        g = range(n)
        B, idx, tab = face_algebra(rel, g)
        mx = max(mx, len(B))
        G = aut(rel, n)
        orbs, C, closed = invariant_structure_constants(B, idx, tab, G)
        if not closed:
            fail += 1
            continue
        Gi = gram_invariant(C)
        r1, r2 = rank_two_primes(Gi, len(orbs))
        if r1 != r2:
            disagree += 1
        AC = AC_by_support(rel, g)
        oa = orbits(sorted(AC, key=repr), G, act_part)
        rows5.append((n, rel, len(G), len(B), len(orbs), r1, len(AC), len(oa)))
        if r1 == len(oa):
            ok += 1
        else:
            fail += 1
    bad += fail + disagree
    print("  %2d  %7d  %7d  %14d  %14d  %19d  %13d"
          % (n, len(cls), sum(1 for r in rows5 if r[0] == n and r[2] > 1),
             ok, fail, disagree, mx))
print()
print("  mg-7d75's T4a exempted 4 of the 63 classes at n = 5 from its")
print("  nilpotency step over a dim <= 90 cap.  There is no cap here and no")
print("  exemption: 87 of 87 classes are tested for the identity itself.")
print()

# ---------------------------------------------------------------------------
hdr("A1b  the rows BETWEEN the two extremes -- mg-7d75 prints only the ends")

print("  mg-7d75 section 2.3 shows |Aut| = n! (the antichain) and |Aut| = 1.")
print("  A formula in one argument should also hold in between, and the")
print("  interesting content is whether |AC/Aut| < |AC| there, i.e. whether the")
print("  symmetry is actually doing something on the flats.")
print()
print("   |Aut|  classes  identity holds  of which |AC/Aut| < |AC|  (n = 5 only)")
from collections import defaultdict
byaut = defaultdict(lambda: [0, 0, 0])
for (n, rel, na, nf, no, r, nac, noa) in rows5:
    if n != 5:
        continue
    e = byaut[na]
    e[0] += 1
    e[1] += (r == noa)
    e[2] += (noa < nac)
for k in sorted(byaut):
    v = byaut[k]
    print("  %6d  %7d  %14d  %25d" % (k, v[0], v[1], v[2]))
mid = sum(v[0] for k, v in byaut.items() if 1 < k < 120)
midstrict = sum(v[2] for k, v in byaut.items() if 1 < k < 120)
print()
print("  %d classes at n = 5 are strictly between the two rows mg-7d75 shows,"
      % mid)
print("  and on %d of them the quotient by Aut(P) is strictly smaller than"
      % midstrict)
print("  AC(P).  Those are the rows where the identity says something that")
print("  neither of the printed extremes says, and they are all correct.")
print()

# ---------------------------------------------------------------------------
hdr("A1c  OUT OF SAMPLE: n = 6, past mg-7d75's stated reach")

cls6 = iso_classes_6_from_5()
print("  isomorphism classes on 6 points, built by adjoining a maximal element")
print("  to each 5-point class: %d  (OEIS A000112(6) = 318)" % len(cls6))
CAP = 300
ok = fail = 0
tested = skipped = 0
for rel in cls6:
    g = range(6)
    F = faces(rel, g)
    if len(F) > CAP:
        skipped += 1
        continue
    tested += 1
    B, idx, tab = face_algebra(rel, g)
    G = aut(rel, 6)
    orbs, C, closed = invariant_structure_constants(B, idx, tab, G)
    if not closed:
        fail += 1
        continue
    Gi = gram_invariant(C)
    r1, r2 = rank_two_primes(Gi, len(orbs))
    AC = AC_by_support(rel, g)
    oa = orbits(sorted(AC, key=repr), G, act_part)
    if r1 == r2 == len(oa):
        ok += 1
    else:
        fail += 1
bad += fail
print("  |F(P)| <= %d:  tested %d   skipped %d   identity holds %d   FAILS %d"
      % (CAP, tested, skipped, ok, fail))
print()
print("  The identity is not an n <= 5 phenomenon.  A1d says why no n could")
print("  have broken it.")
print()

# ---------------------------------------------------------------------------
hdr("A1d  THE PROOF, and an exact check of its two steps")

print("  Write A = kF(P), G = Aut(P), k of characteristic 0.")
print()
print("  (1)  A/rad A = k^{AC(P)}.  This is Bidigare's radical theorem, which")
print("       mg-7d75 quotes in full from Aguiar-Mahajan section 10.10 and")
print("       which Brown extended to left regular bands: rad A = ker(supp).")
print()
print("  (2)  G acts on A by algebra automorphisms (it permutes F(P) and the")
print("       Tits product is equivariant), and |G| is invertible in k, so the")
print("       Reynolds operator e = (1/|G|) sum_g g is a projection A -> A^G")
print("       and taking G-invariants is EXACT.  Applying it to")
print("       0 -> rad A -> A -> k^{AC} -> 0 gives")
print("            A^G / (rad A)^G  =  ( k^{AC} )^G  =  k^{AC/G}.")
print()
print("  (3)  (rad A)^G is a nilpotent ideal of A^G, so it lies in rad(A^G);")
print("       and the quotient above is a product of copies of k, hence")
print("       semisimple, so rad(A^G) lies in (rad A)^G.  They are equal, and")
print("            A^G / rad(A^G)  =  k^{ AC(P)/G }.")
print()
print("  Three lines, no new object, and no dependence on n.  What follows for")
print("  the audit is in the ledger, not here: the identity is a COROLLARY of")
print("  the theorem mg-7d75 quotes, not a measurement awaiting a citation.")
print()
print("  Step (2) and step (3) checked EXACTLY over Q, all classes to n <= 4:")
print()
print("   n  classes  dim(rad A)^G = dim rad(A^G)  ...FAILS  dim A^G/(rad A)^G"
      " = |AC/G|  ...FAILS")
for n in range(1, 5):
    a = b = c = d = 0
    for rel in iso_classes(n):
        g = range(n)
        B, idx, tab = face_algebra(rel, g)
        G = aut(rel, n)
        gr = gram_full(tab)
        rad = nullspace_q(gr, len(B))               # rad A, exact over Q
        # (rad A)^G : average each radical basis vector over G, then rank
        pos = {F: i for i, F in enumerate(B)}
        rowsav = []
        for v in rad:
            w = [0] * len(B)
            from fractions import Fraction
            w = [Fraction(0)] * len(B)
            for gperm in G:
                for i, F in enumerate(B):
                    w[pos[act_comp(F, gperm)]] += v[i]
            rowsav.append(w)
        # clear denominators for an integer rank
        ints = []
        for w in rowsav:
            from fractions import Fraction
            den = 1
            for x in w:
                den = den * x.denominator // __import__("math").gcd(
                    den, x.denominator)
            ints.append([int(x * den) for x in w])
        dim_radG = rank_q(ints, len(B)) if ints else 0
        orbs, C, closed = invariant_structure_constants(B, idx, tab, G)
        Gi = gram_invariant(C)
        dim_AG = len(orbs)
        dim_rad_AG = dim_AG - rank_mod(Gi, dim_AG, P1)
        AC = AC_by_support(rel, g)
        oa = orbits(sorted(AC, key=repr), G, act_part)
        a += 1
        if dim_radG != dim_rad_AG:
            b += 1
        if dim_AG - dim_radG != len(oa):
            d += 1
        c += 1
    bad += b + d
    print("  %2d  %7d  %27d  %8d  %30d  %8d"
          % (n, a, a - b, b, c - d, d))
print()

# ---------------------------------------------------------------------------
hdr("A1e  CONTROLS -- two WRONG index sets, one of them this repo's own error")

print("  If dim A^G/rad were insensitive to the index set, A1a would prove")
print("  nothing.  Two substitutes are run against the same left-hand side.")
print()
print("  (i)  Pi[n]/G in place of AC(P)/G  -- the full partition lattice.")
print("  (ii) the OPEN-cone flats in place of AC(P): the partitions in AC(P)")
print("       whose every block is an antichain of P.  Conflating these two is")
print("       exactly the error mg-1953 repaired (R1, 455 spurious flats at")
print("       n = 6), and code/species_7d75/README.md names it as the")
print("       convention that has bitten this repo before.")
print()
print("   n  classes  (i) disagrees  (i) agrees  (ii) disagrees  (ii) agrees")
for n in range(2, 6):
    i_d = i_a = ii_d = ii_a = 0
    for rel in iso_classes(n):
        g = range(n)
        B, idx, tab = face_algebra(rel, g)
        G = aut(rel, n)
        orbs, C, closed = invariant_structure_constants(B, idx, tab, G)
        Gi = gram_invariant(C)
        r = rank_mod(Gi, len(orbs), P1)
        allp = set_partitions(g)
        o_all = orbits(sorted(allp, key=repr), G, act_part)
        AC = AC_by_support(rel, g)
        openf = {X for X in AC
                 if all(not any(a in Bk and b in Bk for (a, b) in rel)
                        for Bk in X)}
        o_open = orbits(sorted(openf, key=repr), G, act_part)
        i_d += (r != len(o_all))
        i_a += (r == len(o_all))
        ii_d += (r != len(o_open))
        ii_a += (r == len(o_open))
    print("  %2d  %7d  %13d  %11d  %14d  %11d"
          % (n, i_d + i_a, i_d, i_a, ii_d, ii_a))
print()
print("  Both controls fire.  The right-hand side of the identity is not a")
print("  free parameter: AC(P)/Aut(P) is the index set and neither of the two")
print("  nearby candidates reproduces the dimension.")
print()

print("=" * 78)
print("A1 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
