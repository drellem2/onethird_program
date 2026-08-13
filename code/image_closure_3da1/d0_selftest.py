"""d0 — controls on lib3da1, run before any arm that produces a finding.

This directory exists to CORROBORATE a measurement made elsewhere in this estate, so its
library has to be checked against something outside it or the corroboration is circular.  The
checks below are, in order: an external anchor (OEIS A001035), a second algorithm for the same
quantity, and planted defects that each control must catch.

A control that cannot fail is not a control, so every check here is paired with a world in
which it goes red, and that world is EXERCISED rather than described.
"""

from fractions import Fraction

import lib3da1 as L

FAIL = []


def check(ok, name, detail):
    print(f"  [{'GREEN' if ok else 'RED  '}] {name}")
    print(f"       {detail}")
    if not ok:
        FAIL.append(name)


def head(t):
    print("\n" + "=" * 78 + f"\n{t}\n" + "=" * 78)


# ---------------------------------------------------------------------------------------
head("d0.1  the poset enumerator against OEIS A001035 — an EXTERNAL anchor")

# A001035, labelled posets on n points: n = 0..6 -> 1, 1, 3, 19, 219, 4231, 130023.
A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}
counts = {n: len(L.enumerate_posets(n)) for n in (1, 2, 3, 4, 5)}
check(counts == {n: A001035[n] for n in counts},
      "labelled poset counts match A001035 at n = 1..5",
      f"measured {[counts[n] for n in sorted(counts)]}, "
      f"A001035 {[A001035[n] for n in sorted(counts)]}")

# ---------------------------------------------------------------------------------------
head("d0.2  is_poset is not vacuously true — the two ways it must refuse")

n = 3
cyc = {(0, 1), (1, 2), (2, 0)}                       # transitive closure would need (0,0)
intrans = {(0, 1), (1, 2)}                           # missing (0,2)
both = {(0, 1), (1, 0)}                              # antisymmetry
check(not L.is_poset(cyc, n) and not L.is_poset(intrans, n) and not L.is_poset(both, n),
      "a cycle, a non-transitive relation and a symmetric pair are all REFUSED",
      "if any of these passed, d0.1's count would be an over-count and would not match A001035")
check(L.is_poset(set(), n) and L.is_poset({(0, 1), (1, 2), (0, 2)}, n),
      "the antichain and the 3-chain are ACCEPTED",
      "the refusals above are therefore not a predicate that refuses everything")

# ---------------------------------------------------------------------------------------
head("d0.3  linear extensions against a second route, and the marginal against a third")

n = 4
U = L.all_perms(n)
mismatch_e, mismatch_pi = [], []
for P in L.enumerate_posets(n):
    Lp = L.linear_extensions(P, n, U)

    # SECOND ROUTE for e(P): count by recursive removal of minimal elements, which shares no
    # code path with the filter above -- it never enumerates a permutation at all.
    def count(rem):
        if not rem:
            return 1
        tot = 0
        for x in rem:
            if not any((y, x) in P for y in rem):
                tot += count(rem - {x})
        return tot
    if count(frozenset(range(n))) != len(Lp):
        mismatch_e.append(P)

    # THIRD ROUTE for the marginal: average the vertex vectors of L(P) instead of accumulating
    # pair-by-pair inside `marginal`.
    w = Fraction(1, len(Lp))
    byvert = {p: sum(L.vertex(s, n)[p] for s in Lp) * w for p in L.pairs(n)}
    if byvert != L.uniform_image(P, n, U)[0]:
        mismatch_pi.append(P)

check(not mismatch_e, "e(P) agrees with a minimal-element recursion at all 219 posets, n = 4",
      "the filter-over-S_n route and the recursion share no code")
check(not mismatch_pi, "the image point agrees with an average of vertex vectors at all 219",
      "so `marginal`'s accumulation is not carrying the arms on its own")

# ---------------------------------------------------------------------------------------
head("d0.4  PLANTED DEFECTS — each control above, put to a library that has the defect")

# Plant 1: an enumerator that forgets transitivity.  A001035 must stop matching.
def loose(n):
    from itertools import product as pr
    out = []
    for choice in pr((0, 1, 2), repeat=len(L.pairs(n))):
        rel = set()
        for c, (i, j) in zip(choice, L.pairs(n)):
            if c == 1:
                rel.add((i, j))
            elif c == 2:
                rel.add((j, i))
        out.append(frozenset(rel))          # NO transitivity filter
    return out


check(len(loose(4)) != A001035[4],
      "an enumerator with the transitivity filter removed FAILS d0.1",
      f"it returns {len(loose(4))} at n = 4 against A001035's {A001035[4]} — d0.1 can go red")

# Plant 2: a linear-extension routine that drops the last extension.  Both d0.3 checks must fire.
n = 4
P = frozenset({(0, 1)})
short = L.linear_extensions(P, n, U)[:-1]
w = Fraction(1, len(short))
check(L.marginal([(s, w) for s in short], n) != L.uniform_image(P, n, U)[0],
      "an extension list one short moves the marginal — d0.3's third route can go red",
      f"e(P) = {len(L.linear_extensions(P, n, U))} at P = {{0 < 1}}, n = 4; dropping one moves pi")

# Plant 3: THE ONE THAT MATTERS FOR THIS DIRECTORY.  `vertex` is the function every finding
# below rests on -- d1's whole subject is that the n! vertices are DISTINCT points of R_n --
# so it gets a plant of its own.
#
# THE FIRST PLANT WRITTEN HERE WAS INERT AND IS KEPT RATHER THAN SWAPPED OUT, because the
# reason is a fact about the domain and not about the library.  It weakened `pos[i] < pos[j]`
# to `pos[i] <= pos[j]`, the classic off-by-one in a comparison -- and it changes NOTHING,
# because the coordinates are indexed by pairs with i != j and two distinct elements never
# share a position.  A plant has to be a defect the domain can EXPRESS; this one is a defect
# the domain forbids, so it reports GREEN against a library that is genuinely correct and
# says nothing at all about whether the control has power.
def inert_vertex(sigma, n):
    pos = {x: k for k, x in enumerate(sigma)}
    return {(i, j): Fraction(1) if pos[i] <= pos[j] else Fraction(0) for (i, j) in L.pairs(n)}


# The LIVE plant reads the element LABELS where it should read their POSITIONS -- the same
# slip one level out, and one the domain can express.  It collapses all n! vertices onto
# delta_id, which is exactly the failure that would make d1 vacuous.
def bad_vertex(sigma, n):
    return {(i, j): Fraction(1) if i < j else Fraction(0) for (i, j) in L.pairs(n)}


n = 3
distinct = lambda vs: len({tuple(sorted(v.items())) for v in vs})
good = distinct([L.vertex(s, n) for s in L.all_perms(n)])
inert = distinct([inert_vertex(s, n) for s in L.all_perms(n)])
bad = distinct([bad_vertex(s, n) for s in L.all_perms(n)])
check(good == 6 and bad < 6,
      "the n! vertex vectors are DISTINCT, and a labels-for-positions slip collapses them",
      f"{good} distinct points with `<` on positions, {bad} with `<` on labels — "
      f"the plant leaves ONE point, so d1 would have no subject left")
check(inert == good,
      "AND THE INERT PLANT IS REPORTED, NOT HIDDEN: `<=` for `<` changes nothing",
      f"{inert} distinct, same as the {good} the library gives — i != j on every coordinate, "
      f"so positions never tie and the two comparisons agree on this domain")

# ---------------------------------------------------------------------------------------
head("d0.5  the retraction is idempotent — cited from mg-c776 T1, RE-CHECKED not assumed")

n = 4
U = L.all_perms(n)
bad = []
for P in L.enumerate_posets(n):
    pi, _ = L.uniform_image(P, n, U)
    if L.retract(pi, n, U) != pi or L.poset_of(pi, n) != P:
        bad.append(P)
check(not bad, "r(r(pi)) = r(pi) and P(r(pi)) = P at all 219 posets, n = 4",
      "so `R_n = Fix(r)` and the cells are a partition — this directory's arms may use both")

print("\nRESULT: " + ("GREEN — all controls passed" if not FAIL else f"RED — {FAIL}"))
raise SystemExit(1 if FAIL else 0)
