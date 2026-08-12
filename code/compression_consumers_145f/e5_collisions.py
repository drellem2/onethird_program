"""e5 -- does the identity's output DETERMINE the programme's targets?

e1 proved the identity's whole measure-dependent output is the adjacency vector (A^o, A^e).
That is a statement about what the identity computes.  It is not yet a statement that the
targets are out of reach: a target could still be a function of (A^o, A^e) by some route
nobody has found.

This arm attacks that.  It buckets posets by the ISOMORPHISM-INVARIANT multiset

    { (A^o_xy, A^e_xy) : {x,y} incomparable }

and asks whether the programme's own targets are constant inside a bucket.  A bucket carrying
two different values of a target is a HARD witness that the identity's output does not
determine it -- no future argument can extract from (A^o, A^e) something that (A^o, A^e) does
not distinguish.

THE KEY IS AN ISOMORPHISM INVARIANT AND THAT IS LOAD-BEARING.  My first version of e4.3 keyed
a pair-indexed question on ORDERED pairs and duly reported [(2,3)] against [(3,2)] -- one
poset relabelled -- as a finding.  That is mg-409a's own D2 recurring in this directory, and
it is kept as D1 in the README.  Every key below is over UNORDERED pairs and is checked for
invariance under a relabelling before it is used.

VACUITY CONTROL.  A bucket that only ever contains one isomorphism class proves nothing:
"isomorphic posets agree" is a tautology.  The third column below is the number of buckets
that genuinely merge distinct isomorphism classes, and it must be positive for any negative
finding here to mean anything.  Same control mg-409a section 6(b) used, for the same reason.
"""

import os
import sys
from fractions import Fraction
from itertools import permutations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib145f as L  # noqa: E402

ok = True


def relabel(n, lt, perm):
    return frozenset((perm[a], perm[b]) for (a, b) in lt)


def iso_key(n, lt):
    """Canonical form under relabelling -- the lexicographically least image."""
    best = None
    for perm in permutations(range(n)):
        img = tuple(sorted(relabel(n, lt, perm)))
        if best is None or img < best:
            best = img
    return best


def adjacency_multiset(n, lt, LEs):
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    return tuple(sorted((A_o[p], A_e[p]) for p in A_o))


# ---------------------------------------------------------------------------------------
L.banner("e5.0  the key is an isomorphism invariant -- checked, not assumed")
bad = 0
for lt in list(L.all_posets(4))[:60]:
    LEs = L.linear_extensions(4, lt)
    base = adjacency_multiset(4, lt, LEs)
    for perm in list(permutations(range(4)))[:8]:
        lt2 = relabel(4, lt, perm)
        LEs2 = L.linear_extensions(4, lt2)
        if adjacency_multiset(4, lt2, LEs2) != base:
            bad += 1
ok &= L.verdict(bad == 0, "the (A^o, A^e) multiset is invariant under relabelling",
                f"{bad} violations")

# a control on that: an ORDERED-pair key must NOT be invariant (this is D1's defect, armed)
def ordered_key(n, lt, LEs):
    A_o, A_e = L.adjacency_probs(n, lt, LEs)
    return tuple(sorted((p, A_o[p], A_e[p]) for p in A_o))


moved = 0
for lt in list(L.all_posets(4))[:60]:
    LEs = L.linear_extensions(4, lt)
    base = ordered_key(4, lt, LEs)
    for perm in list(permutations(range(4)))[:8]:
        lt2 = relabel(4, lt, perm)
        if ordered_key(4, lt2, L.linear_extensions(4, lt2)) != base:
            moved += 1
ok &= L.verdict(moved > 0, "C  and the ORDERED-pair key my D1 used is NOT invariant",
                f"{moved} relabellings move it")

# ---------------------------------------------------------------------------------------
L.banner("e5.1  do the programme's targets vary inside an (A^o, A^e) bucket?")

TARGETS = [
    ("delta(P)            (Axis 2, the counterexample condition)",
     lambda n, lt, LEs: L.delta(n, lt, LEs)),
    ("E[inv_e]            (row 8 / LIB / LIB-const)",
     lambda n, lt, LEs: L.expected_inv(n, lt, LEs)),
    ("max_x Var(pos_x)    (the (B) variance diagonal)",
     lambda n, lt, LEs: max(L.variance([Fraction(Lx.index(x)) for Lx in LEs])
                            for x in range(n))),
    ("max_x |E pos_x - rank_e x|   (the (EQ) residual)",
     lambda n, lt, LEs: max(
         abs(L.mean([Fraction(Lx.index(x)) for Lx in LEs])
             - Fraction(L.majority_order(n, lt, LEs).index(x)))
         for x in range(n))),
    ("max_{x||y} p_xy     (the pair-bias marginals)",
     lambda n, lt, LEs: (max(L.pair_up_prob(n, lt, LEs).values())
                         if L.incomparable_pairs(n, lt) else Fraction(0))),
]

for n, popname, pop in ((4, "exhaustive", list(L.all_posets(4))),
                        (5, "exhaustive", list(L.all_posets(5)))):
    buckets = {}
    for lt in pop:
        LEs = L.linear_extensions(n, lt)
        if not L.incomparable_pairs(n, lt):
            continue
        key = adjacency_multiset(n, lt, LEs)
        buckets.setdefault(key, []).append(lt)
    merging = 0
    power = 0            # number of DISTINCT-CLASS pairs the test actually compares
    for key, members in buckets.items():
        classes = {iso_key(n, m) for m in members}
        if len(classes) > 1:
            merging += 1
            power += len(classes) * (len(classes) - 1) // 2
    print(f"\n  n = {n} ({popname}, {len(pop)} labelled posets): "
          f"{len(buckets)} buckets, {merging} merging >1 isomorphism class")
    print(f"    POWER: the test compares {power} distinct-class pairs in total.  A "
          f"'constant' row below\n           is a null over THOSE pairs and nothing wider.")
    if merging == 0:
        print("    VACUOUS at this n -- no bucket merges distinct classes, so nothing below")
        print("    is evidence.  Reported rather than dropped.")
    for label, fn in TARGETS:
        split = 0
        witness = None
        for key, members in buckets.items():
            if len({iso_key(n, m) for m in members}) <= 1:
                continue
            vals = set()
            for m in members:
                vals.add(fn(n, m, L.linear_extensions(n, m)))
            if len(vals) > 1:
                split += 1
                if witness is None:
                    witness = (members, sorted(vals))
        tag = "SPLITS" if split else "constant"
        print(f"    {label:<56} {tag:>9}  ({split} buckets)")
        if witness is not None and label.startswith("E[inv_e]"):
            ms, vals = witness
            print(f"        witness values {[L.fr(v) for v in vals]}")

print("""
  READING.  A "SPLITS" row is a HARD negative for that target: two posets the identity cannot
  tell apart carry different values of it, so no argument whatever can compute it from the
  identity's output.  A "constant" row is NOT a positive -- it is an n <= 5 observation and
  says only that this population did not separate them.""")

L.banner("e5  RESULT")
print("  ok" if ok else "  NOT ok")
sys.exit(0 if ok else 1)
