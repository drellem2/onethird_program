"""p4 -- THE PRIMITIVE CENSUS EXTENDED TO n = 8.

p2 reaches n = 7 with brute-force canonical forms (7! = 5040 relabellings per candidate).
n = 8 needs 40320 and that is where brute force stops being honest about its own cost.
This arm adds a COLOUR-REFINED canonical form -- permutations are restricted to those
respecting an isomorphism-invariant vertex colouring -- and validates it against the brute
force one at n <= 6 before using it (p4.0).  That validation is the whole warrant for the
n = 8 numbers, so it runs first and the arm exits if it fails.

The point of going to n = 8 is P4/P5's trend claim: the primitive maximum measured at
n = 4..7 is 0.3876 / 0.3596 / 0.3343 / 0.3219, i.e. DECREASING.  One more term is worth
having before that is written down as a trend rather than four numbers.
"""

import os
import sys
from itertools import permutations, product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libf5be as F  # noqa: E402
import lib409a as L  # noqa: E402

ok = True


def colours(n, lt):
    """An isomorphism-invariant vertex colouring, refined to a fixed point.

    Start from (down-degree, up-degree); repeatedly replace each vertex's colour by
    (own colour, sorted colours of strict predecessors, sorted colours of strict
    successors).  Any isomorphism preserves the result, which is what makes restricting
    permutations to colour classes sound.
    """
    down = [frozenset(a for (a, b) in lt if b == v) for v in range(n)]
    up = [frozenset(b for (a, b) in lt if a == v) for v in range(n)]
    col = [(len(down[v]), len(up[v])) for v in range(n)]
    for _ in range(n):
        new = [(col[v],
                tuple(sorted(col[u] for u in down[v])),
                tuple(sorted(col[w] for w in up[v]))) for v in range(n)]
        # compress to small ints, preserving the induced order (so it stays invariant)
        order = {c: i for i, c in enumerate(sorted(set(new)))}
        nxt = [order[c] for c in new]
        if nxt == col:
            break
        col = nxt
    return col


def canonical_refined(n, lt):
    """Least relabelling over COLOUR-RESPECTING permutations only.

    Vertices are first bucketed by colour and the buckets ordered by colour value; a
    relabelling is then any product of within-bucket permutations composed with that fixed
    bucket order.  Sound because every isomorphism maps colour classes to colour classes.
    """
    col = colours(n, lt)
    buckets = {}
    for v in range(n):
        buckets.setdefault(col[v], []).append(v)
    keys = sorted(buckets)
    slots, at = [], 0
    for k in keys:
        slots.append(list(range(at, at + len(buckets[k]))))
        at += len(buckets[k])
    best = None
    for choice in product(*[permutations(buckets[k]) for k in keys]):
        perm = [0] * n
        for sl, grp in zip(slots, choice):
            for pos, v in zip(sl, grp):
                perm[v] = pos
        img = tuple(sorted((perm[a], perm[b]) for (a, b) in lt))
        if best is None or img < best:
            best = img
    return best


# --------------------------------------------------------------------------------------
F.banner("p4.0  VALIDATE the refined canonical form against brute force -- n <= 6")

for n in (3, 4, 5, 6):
    P = F.posets_up_to_iso(n)
    # (a) it must separate the same classes: distinct classes -> distinct keys
    keys = {canonical_refined(n, lt) for lt in P}
    ok &= F.verdict(len(keys) == len(P),
                    f"n={n}: refined form gives {len(keys)} keys for {len(P)} iso classes",
                    "(no class collision)")
    # (b) it must MERGE relabellings: a random relabelling must get the same key
    bad = 0
    for lt in P:
        for perm in list(permutations(range(n)))[:24]:
            rel = frozenset((perm[a], perm[b]) for (a, b) in lt)
            if canonical_refined(n, rel) != canonical_refined(n, lt):
                bad += 1
    ok &= F.verdict(bad == 0, f"n={n}: invariant under 24 relabellings of every class",
                    f"{bad} failures")

if not ok:
    print("\n  refined canonical form FAILED validation -- n = 8 numbers withheld")
    sys.exit(1)

# --------------------------------------------------------------------------------------
F.banner("p4.1  ENUMERATE every PRIMITIVE iso class at n = 7 and n = 8")

def primitives(n, base):
    """All primitive iso classes on n elements, from the (n-1) classes by augmentation.

    Augmenting each (n-1)-class by a new maximal element over each of its down-sets
    generates EVERY n-class (delete a maximal element to invert), so filtering the result
    to primitive ones is exhaustive over the primitive sub-population.
    """
    seen, out = set(), []
    for lt in base:
        for S in F.down_sets(n - 1, lt):
            rel = frozenset(set(lt) | {(v, n - 1) for v in S})
            if not F.is_prime(n, rel):
                continue
            k = canonical_refined(n, rel)
            if k in seen:
                continue
            seen.add(k)
            out.append(rel)
    return out


# the FULL n=7 population is needed as the base for n=8 primitives: a primitive 8-poset
# need NOT have a primitive 7-element restriction, so filtering early would be unsound.
p6 = F.posets_up_to_iso(6)
seen7, p7 = set(), []
for lt in p6:
    for S in F.down_sets(6, lt):
        rel = frozenset(set(lt) | {(v, 6) for v in S})
        k = canonical_refined(7, rel)
        if k in seen7:
            continue
        seen7.add(k)
        p7.append(rel)
ok &= F.verdict(len(p7) == 2045, f"n=7: {len(p7)} iso classes (OEIS A000112 says 2045)")

prim7 = [lt for lt in p7 if F.is_prime(7, lt)]
prim8 = primitives(8, p7)
print(f"      n=7: {len(prim7)} primitive iso classes")
print(f"      n=8: {len(prim8)} primitive iso classes")
print("""
      NOTE ON SOUNDNESS: the n=8 base is the FULL n=7 population, not the primitive one.
      A primitive poset can have a decomposable restriction (deleting a maximal element
      can create a module), so seeding from primitives only would silently miss classes.
      That is the n=8 analogue of PREDICTIONS E5 and it is the reason this arm costs what
      it costs.""")

# --------------------------------------------------------------------------------------
F.banner("p4.2  alpha OVER THE PRIMITIVE CLASS AT n = 8")

results = {}
for n, pop in ((7, prim7), (8, prim8)):
    best = None
    ones = 0
    for lt in pop:
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        one, _w = F.alpha_is_one_exact(LEs, n)
        if one:
            ones += 1
        a = F.alpha_power(LEs, n)
        if best is None or a > best[0]:
            best = (a, lt, len(LEs))
    results[n] = (best, ones, len(pop))
    print(f"  n = {n}: {len(pop):>5} primitive classes,  max alpha = {best[0]:.9f},  "
          f"attaining alpha=1: {ones}")

for n in (7, 8):
    ok &= F.verdict(results[n][1] == 0, f"n={n}: NO primitive poset attains alpha = 1 (EXACT test)",
                    f"({results[n][1]} found)")

# --------------------------------------------------------------------------------------
F.banner("p4.3  THE TREND, n = 4..8")

KNOWN = {4: 0.387627564304, 5: 0.359611797000, 6: 0.334349276000}
print(f"  {'n':>2}  {'max alpha over PRIMITIVE posets':>32}")
seq = []
for n in (4, 5, 6):
    print(f"  {n:>2}  {KNOWN[n]:>32.9f}     (from p2)")
    seq.append(KNOWN[n])
for n in (7, 8):
    print(f"  {n:>2}  {results[n][0][0]:>32.9f}")
    seq.append(results[n][0][0])
mono = all(seq[i] > seq[i + 1] for i in range(len(seq) - 1))
ok &= F.verdict(mono, "strictly DECREASING over n = 4..8",
                "measured on an exhaustive primitive population at every n")

b8 = results[8][0]
def cover(n, lt):
    cov = [(a, b) for (a, b) in lt
           if not any((a, c) in lt and (c, b) in lt for c in range(n))]
    return "{" + ", ".join(f"{a}<{b}" for (a, b) in sorted(cov)) + "}"
print(f"\n      n=8 argmax: {cover(8, b8[1])}   |L| = {b8[2]}")

print()
print("=" * 88)
print("p4 OVERALL: " + ("PASS" if ok else "FAIL"))
print("=" * 88)
sys.exit(0 if ok else 1)
