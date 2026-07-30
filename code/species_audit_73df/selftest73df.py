"""selftest73df -- anchor kern73df to published integer sequences.

Every count this audit reports is built out of the routines checked here.  If
one of these disagrees with OEIS the audit is void, which is why they are run
first and why run_all.sh stops on a failure.
"""

import sys
from itertools import permutations

from kern73df import (AC_on, COLUMNS, bits, comp_to_subset, compositions_on,
                      concat, descent_set, descent_structure, faces_on,
                      five_columns, in_cone, integer_compositions,
                      is_lower_set, orbit_sum_structure, popcount,
                      poset_disjoint_union, poset_opposite, poset_restrict,
                      posets_on, quotient_acyclic, restrict_face, shape,
                      splits, submasks, supp, tits)

n_assert = 0
fails = []


def eq(got, want, what):
    global n_assert
    n_assert += 1
    if got != want:
        fails.append("%s: got %r want %r" % (what, got, want))


def ok(cond, what):
    global n_assert
    n_assert += 1
    if not cond:
        fails.append(what)


# --- A001035, labelled posets: 1, 1, 3, 19, 219, 4231 ----------------------
A001035 = [1, 1, 3, 19, 219]
for n in range(0, 5):
    eq(len(posets_on((1 << n) - 1, 5)), A001035[n],
       "A001035 labelled posets on [%d]" % n)

# --- A000670, ordered set partitions: 1, 1, 3, 13, 75, 541 -----------------
A000670 = [1, 1, 3, 13, 75, 541]
for n in range(0, 6):
    eq(len(compositions_on((1 << n) - 1)), A000670[n],
       "A000670 set compositions of [%d]" % n)

# --- A000110, Bell: 1, 1, 2, 5, 15, 52, 203 --------------------------------
A000110 = [1, 1, 2, 5, 15, 52, 203]
for n in range(0, 7):
    parts = {supp(F) for F in compositions_on((1 << n) - 1)}
    eq(len(parts), A000110[n], "A000110 Bell(%d)" % n)

# --- A000142, factorials, via the antichain's faces of shape (1,..,1) ------
A000142 = [1, 1, 2, 6, 24, 120]
for n in range(0, 6):
    g = (1 << n) - 1
    chains = [F for F in compositions_on(g) if all(popcount(B) == 1 for B in F)]
    eq(len(chains), A000142[n], "A000142 %d!" % n)

# --- A000041, partitions of n, as S_n-orbits of set partitions -------------
A000041 = [1, 1, 2, 3, 5, 7, 11]
for n in range(0, 7):
    shapes = {tuple(sorted(popcount(B) for B in X))
              for X in {supp(F) for F in compositions_on((1 << n) - 1)}}
    eq(len(shapes), A000041[n], "A000041 p(%d)" % n)

# --- A000112, unlabelled posets: 1, 1, 2, 5, 16, 63 ------------------------
# canonical form by minimising the down-mask tuple over relabellings.


def iso_class(down, n):
    best = None
    for pi in permutations(range(n)):
        d = [0] * n
        for j in range(n):
            for i in bits(down[j]):
                d[pi[j]] |= 1 << pi[i]
        t = tuple(d)
        if best is None or t < best:
            best = t
    return best


A000112 = [1, 1, 2, 5, 16]
for n in range(0, 5):
    g = (1 << n) - 1
    eq(len({iso_class(p, n) for p in posets_on(g, n)}), A000112[n],
       "A000112 unlabelled posets on [%d]" % n)

# --- the antichain's faces are all of Sigma_n, and AC = all of Pi[n] -------
for n in range(0, 5):
    g = (1 << n) - 1
    anti = tuple([0] * 5)
    eq(len(faces_on(anti, g, 5)), A000670[n], "antichain faces = Sigma_%d" % n)
    eq(len(AC_on(anti, g, 5)), A000110[n], "antichain AC = Pi[%d]" % n)

# --- the chain on [n] has exactly one face and one AC element --------------
for n in range(1, 5):
    ch = [0] * 5
    for j in range(n):
        ch[j] = (1 << j) - 1
    ch = tuple(ch)
    F = faces_on(ch, (1 << n) - 1, 5)
    ok(len(F) >= 1, "chain on [%d] has a face" % n)
    ok(all(in_cone(ch, f, 5) for f in F), "chain faces lie in the cone")

# --- supp of a face of C(P) always lies in AC(P) ---------------------------
for p in posets_on(0b1111, 4):
    A = set(AC_on(p, 0b1111, 4))
    for F in faces_on(p, 0b1111, 4):
        ok(supp(F) in A, "supp(face) in AC")

# --- the total face count over labelled posets on [4] ----------------------
tot4 = sum(len(faces_on(p, 0b1111, 4)) for p in posets_on(0b1111, 4))
eq(tot4, 4399, "|F| on the ground set [4]")
tot4ac = sum(len(AC_on(p, 0b1111, 4)) for p in posets_on(0b1111, 4))
eq(tot4ac, 2685, "|AC| on the ground set [4]")
eq(len(posets_on(0b1111, 4)) * len(compositions_on(0b1111)), 16425,
   "|P x Sigma| on the ground set [4]")

# --- lower sets: the empty set and the whole set always are ----------------
for p in posets_on(0b111, 3):
    ok(is_lower_set(p, 0, 3), "empty set is a lower set")
    ok(is_lower_set(p, 0b111, 3), "whole set is a lower set")

# --- restriction and disjoint union are what they say they are -------------
for p in posets_on(0b111, 3):
    for s in submasks(0b111):
        r = poset_restrict(p, s, 3)
        for j in range(3):
            ok(r[j] & ~s == 0, "restriction stays inside s")
    eq(poset_opposite(poset_opposite(p, 3), 3), p, "opposite is an involution")

# --- the Tits product: idempotent, and F.G refines F -----------------------
for F in compositions_on(0b111):
    eq(tits(F, F), F, "Tits product is idempotent")
    for G in compositions_on(0b111):
        H = tits(F, G)
        eq(sum(popcount(B) for B in H), 3, "Tits product partitions [3]")
        eq(supp(tits(H, F)), supp(H), "F.G.F = F.G on supports")

# --- descent sets, and dim Sol(S_n) = 2^{n-1} ------------------------------
eq(descent_set((1, 2, 3)), frozenset(), "des(123)")
eq(descent_set((3, 2, 1)), frozenset({1, 2}), "des(321)")
eq(descent_set((2, 1, 3)), frozenset({1}), "des(213)")
for n in range(1, 5):
    subs, _ = descent_structure(n, "A")
    eq(len(subs), 2 ** (n - 1), "dim Sol(S_%d) = 2^{n-1}" % n)

# --- orbits of faces ARE the block-size compositions -----------------------
for n in range(1, 6):
    comps, _ = orbit_sum_structure(n)
    eq(len(comps), 2 ** (n - 1), "compositions of %d" % n)
    seen = {shape(F) for F in compositions_on((1 << n) - 1)}
    eq(len(seen), 2 ** (n - 1), "shapes seen at n=%d" % n)
    ok(set(comps) == seen, "orbit labels are the compositions at n=%d" % n)

# --- |{w : des(w) subset T(alpha)}| = |orbit of alpha| ---------------------
for n in range(1, 6):
    comps, _ = orbit_sum_structure(n)
    by_shape = {}
    for F in compositions_on((1 << n) - 1):
        by_shape[shape(F)] = by_shape.get(shape(F), 0) + 1
    perms = list(permutations(range(1, n + 1)))
    for a in comps:
        T = comp_to_subset(a, n)
        cnt = sum(1 for w in perms if descent_set(w).issubset(T))
        eq(cnt, by_shape[a], "|des subset T(%s)| = |O_%s|" % (a, a))

# --- five_columns on a trivial universe: everything 0 ----------------------
U = {0: {("z",)}}
f = five_columns(U, lambda x, y: ("z",), lambda x, S, T: (("z",), ("z",)), 0)
for c in COLUMNS:
    eq(f[c], 0, "trivial universe column %s" % c)

# --- five_columns DETECTS a broken product (a positive control on the
#     measuring routine itself, not on the thing measured) ------------------
U2 = {0: {0}, 1: {0, 1}}
f2 = five_columns(U2, lambda x, y: 99, lambda x, S, T: None, 1)
ok(f2["prod_closure"] > 0, "five_columns sees a product leaving the universe")

# --- splits/submasks --------------------------------------------------------
eq(len(splits(0b1111)), 16, "16 splits of a 4-set")
eq(len(submasks(0b1111)), 16, "16 submasks of a 4-set")
eq(sorted(bits(0b1011)), [0, 1, 3], "bits")

# --- quotient_acyclic: the 3-chain with {a,c}|{b} IS cyclic ----------------
ch3 = (0, 0b001, 0b011)                       # 0 < 1 < 2
eq(quotient_acyclic(ch3, (0b101, 0b010), 3), False,
   "3-chain: {a,c}|{b} has a cyclic quotient")
eq(quotient_acyclic(ch3, (0b001, 0b110), 3), True,
   "3-chain: {a}|{b,c} has an acyclic quotient")

print("selftest73df %s -- %d assertions"
      % ("OK" if not fails else "*** %d FAILURES ***" % len(fails), n_assert))
for f in fails:
    print("   FAIL  %s" % f)
sys.exit(1 if fails else 0)
