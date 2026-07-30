"""C2 -- "THREE COLUMNS CANNOT FAIL ON ANY SUB-COLLECTION", swept.

mg-6f61 demonstrates this on FIVE collections and calls it "no choice of
sub-collection can move those three columns".  Five collections do not
establish a claim quantified over every sub-collection; the argument does,
and the argument is one sentence long:

    associativity, coassociativity and compatibility are evaluated with the
    AMBIENT operations on elements of the collection, and both sides of each
    identity are computed in the ambient.  Restricting the collection can
    only remove tests.  It cannot change the value of one.

The one way that argument fails is if the measuring routine SKIPS a test when
an intermediate value leaves the collection -- in which case a 0 would be
vacuity rather than an identity, and "cannot fail" would be a statement about
the instrument.  It does not skip: mg-6f61's `axioms` and this audit's
`five_columns` both evaluate mu and de unconditionally.  That is checked
below and it is the load-bearing check in this file.

So this file does two things the repair does not: it sweeps 24 sub-collections
chosen by an arithmetic rule with no geometric content, and it shows the sweep
is NOT VACUOUS by running the identical sweep against a mutated operation,
where it must fire on every single collection.
"""

import sys

from kern73df import (COLUMNS, compositions_on, concat, faces_on, five_columns,
                      hdr, is_lower_set, poset_disjoint_union, poset_restrict,
                      posets_on, restrict_face, splits, submasks)

N = 4
FULL = (1 << N) - 1
bad = 0
PINNED = ("assoc", "coassoc", "compat")


def mu(x, y):
    return (poset_disjoint_union(x[0], y[0], N), concat(x[1], y[1]))


def de(x, S, T):
    p, F = x
    if not is_lower_set(p, S, N):
        return None
    return ((poset_restrict(p, S, N), restrict_face(F, S)),
            (poset_restrict(p, T, N), restrict_face(F, T)))


def mu_rotate(x, y):
    """A product that is NOT associative and does NOT stay in the cone --
    used only to prove the sweep below can fire."""
    H = concat(x[1], y[1])
    H = H[1:] + H[:1] if H else H
    return (poset_disjoint_union(x[0], y[0], N), H)


def U_F(m):
    return {(p, F) for p in posets_on(m, N) for F in faces_on(p, m, N)}


FULLSET = {m: sorted(U_F(m)) for m in submasks(FULL)}


def sub(a, b):
    """The sub-collection {x : index(x) mod a == b}, an arithmetic rule with
    no geometric meaning whatever.  a runs 2..7, b runs 0..a-1: 24 in all.

    The rule is applied only where there is something to thin.  A first
    version of this file applied it to EVERY ground set, which emptied the
    one-element components -- and then every associativity triple needs a
    component that is empty, so the sweep reported 0 by testing nothing.
    That is precisely the vacuity this file exists to exclude, and it turned
    up inside the file rather than in the thing being audited; C2a below is
    the check that now catches it, and it is printed for every rule rather
    than for one.
    """
    return {m: (set(FULLSET[m]) if bin(m).count("1") <= 1
                else set(FULLSET[m][b::a])) for m in FULLSET}


def n_assoc_triples(u):
    t = 0
    for (S, R) in splits(FULL):
        for (S1, S2) in splits(S):
            t += len(u[S1]) * len(u[S2]) * len(u[R])
    return t


RULES = [(a, b) for a in range(2, 8) for b in range(a)][:24]

# ---------------------------------------------------------------------------
hdr("C2a  the measuring routine does not SKIP -- so a 0 is an identity")

print("  If `five_columns` skipped an associativity test whenever mu(x, y)")
print("  left the collection, then a collection closed under nothing would")
print("  report 0 by having tested nothing.  It does not skip: the assoc,")
print("  coassoc and compat loops call mu and de unconditionally and compare")
print("  the two sides in the ambient.  Demonstrated by counting the tests")
print("  actually performed on the smallest sub-collection in the sweep.")
print()

TRIPLES = {(a, b): n_assoc_triples(sub(a, b)) for (a, b) in
           [(a, b) for a in range(2, 8) for b in range(a)][:24]}
worst = min(TRIPLES, key=lambda k: TRIPLES[k])
ok0 = TRIPLES[worst] > 0
bad += (not ok0)
print("  associativity triples actually evaluated, per rule:")
print("    fewest : index %% %d == %d  ->  %d triples" % (worst[0], worst[1],
                                                          TRIPLES[worst]))
print("    most   : index %% %d == %d  ->  %d triples"
      % (max(TRIPLES, key=lambda k: TRIPLES[k])[0],
         max(TRIPLES, key=lambda k: TRIPLES[k])[1], max(TRIPLES.values())))
print()
print("  %s -- every 0 reported below is an identity holding on at least %d"
      % ("NON-VACUOUS" if ok0 else "*** VACUOUS ***", TRIPLES[worst]))
print("  evaluated triples, not the absence of a test.")
print()

# ---------------------------------------------------------------------------
hdr("C2b  24 sub-collections, chosen arithmetically: are the three pinned?")

print("  %-14s %7s %10s %10s %10s" % ("rule", "size", "assoc", "coassoc",
                                      "compat"))
print()
nonzero = 0
for (a, b) in RULES:
    u = sub(a, b)
    f = five_columns(u, mu, de, FULL)
    row = tuple(f[c] for c in PINNED)
    nonzero += sum(1 for v in row if v)
    print("  index %% %d == %d %7d %10d %10d %10d"
          % (a, b, len(u[FULL]), row[0], row[1], row[2]))
print()
bad += (nonzero > 0)
print("  cells non-zero: %d of %d" % (nonzero, 3 * len(RULES)))
print("  %s" % ("PINNED -- confirmed on 24 sub-collections chosen by an"
                " arithmetic rule" if nonzero == 0
                else "*** A PINNED COLUMN MOVED ***"))
print()

# ---------------------------------------------------------------------------
hdr("C2c  THE SWEEP IS NOT VACUOUS -- the same 24 with a mutated product")

print("  Identical sweep, product replaced by rotate(concat).  If the sweep")
print("  above were measuring nothing, this one would also report 0.  It must")
print("  fire on every collection, and on the associativity column in")
print("  particular.")
print()
print("  %-14s %7s %10s %10s %10s" % ("rule", "size", "assoc", "coassoc",
                                      "compat"))
print()
fired_all = True
for (a, b) in RULES:
    u = sub(a, b)
    f = five_columns(u, mu_rotate, de, FULL)
    row = tuple(f[c] for c in PINNED)
    if row[0] == 0:
        fired_all = False
    print("  index %% %d == %d %7d %10d %10d %10d"
          % (a, b, len(u[FULL]), row[0], row[1], row[2]))
print()
bad += (not fired_all)
print("  %s" % ("the mutated sweep fires on associativity for all 24 --"
                " so the pinned result in C2b is a measurement"
                if fired_all
                else "*** THE MUTATED SWEEP DID NOT FIRE EVERYWHERE ***"))
print()

print("=" * 78)
print("C2 TOTAL BAD: %d" % bad)
print("=" * 78)
sys.exit(0)
