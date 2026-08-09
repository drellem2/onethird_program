"""B1 — re-derive mg-3969's Claim 6.1 witness from scratch, and certify it.

The parent states (doc §6, Claim 6.1):
    n = 6, A = {0,1,2}, B = {3,4,5},
    strict relations {(0,2),(0,3),(0,4),(0,5),(1,4),(1,5),(2,4),(3,4)},
    |L(P)| = 26, Delta_1 = 17/78,
    all four balanced-in-side pairs leave [1/3,2/3] in P:
    2/3 -> 9/13, 2/3 -> 19/26, 2/3 -> 19/26, 1/3 -> 4/13.

Everything below is recomputed here from the source definitions.  The relation
list is the ONLY thing taken from the parent -- it is a witness, and a witness
is a claim about a specific object, so quoting the object is not replication;
recomputing its properties is the check.  B2 additionally re-FINDS it by an
exhaustive search that does not use the parent's coordinates at all.
"""

from fractions import Fraction

from lib_d3c7 import (le_dp, delta1, pair_probs, incomparable_pairs,
                      induced, is_chain, balanced, THIRD, TWOTHIRD)

N = 6
RELS = [(0, 2), (0, 3), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (3, 4)]
K = 3

# ---- build the poset, and CHECK the given relation set is transitively closed
rel = [0] * N
for (a, b) in RELS:
    rel[b] |= 1 << a
closed = True
for j in range(N):
    for i in range(N):
        if rel[j] >> i & 1 and rel[i] & ~rel[j]:
            closed = False
print(f"relation set transitively closed as given: {closed}")
if not closed:
    # take the transitive closure and report what was added
    import itertools
    changed = True
    while changed:
        changed = False
        for j in range(N):
            m = rel[j]
            for i in range(N):
                if m >> i & 1 and rel[i] & ~rel[j]:
                    rel[j] |= rel[i]
                    changed = True
    added = [(i, j) for j in range(N) for i in range(N)
             if rel[j] >> i & 1 and (i, j) not in RELS]
    print(f"  transitive closure ADDED: {added}")

print(f"rel (bitmask of strict predecessors): {rel}")
print(f"naturally labelled (no i>j below j): "
      f"{all(rel[j] < (1 << j) for j in range(N))}")

dp = le_dp(rel, N)
ids, up, down, total = dp
print(f"\ne(P) = |L(P)| = {total}     [parent says 26]")

d1 = delta1(rel, N, K, dp)
print(f"Delta_1(A_3, B) = {d1} = {float(d1):.6f}     [parent says 17/78 = 0.217949]")
print(f"  as a check, 17/78 = {Fraction(17,78)}; equal: {d1 == Fraction(17,78)}")

# Delta_1 at every cut, so the reader can see 17/78 is the k=3 one
print("\nDelta_1 at every prefix cut of this poset:")
for k in range(1, N):
    print(f"  k={k}: {delta1(rel, N, k, dp)}  ({float(delta1(rel, N, k, dp)):.6f})")

# ---- the two sides
Amask = (1 << K) - 1
Bmask = ((1 << N) - 1) ^ Amask
for nm, mask in (("P[A]", Amask), ("P[B]", Bmask)):
    sub, k, elems = induced(rel, N, mask)
    print(f"\n{nm}: elements {elems}, rel={sub}, chain={is_chain(sub, k)}, "
          f"e={le_dp(sub, k)[3]}")

# ---- every pair balanced in its side, and where it lands in P
beforeP, totP = pair_probs(rel, N, dp)
print("\nEvery pair balanced in its own side, and its probability in P:")
rows = []
for nm, mask in (("A", Amask), ("B", Bmask)):
    sub, k, elems = induced(rel, N, mask)
    sdp = le_dp(sub, k)
    sbefore, stot = pair_probs(sub, k, sdp)
    for (x, y) in incomparable_pairs(sub, k):
        p_side = Fraction(sbefore[x][y], stot)
        if not balanced(p_side):
            continue
        gx, gy = elems[x], elems[y]
        p_P = Fraction(beforeP[gx][gy], totP)
        rows.append((nm, (gx, gy), p_side, p_P, balanced(p_P)))
        print(f"  side {nm}  pair ({gx},{gy}):  p_side = {p_side} "
              f"-> p_P = {p_P} = {float(p_P):.6f}   in [1/3,2/3] in P? "
              f"{balanced(p_P)}")

n_bal = len(rows)
n_survive = sum(1 for r in rows if r[4])
print(f"\nbalanced-in-side pairs: {n_bal}   surviving in P: {n_survive}")
print(f"U_either VIOLATED at this cut: {n_bal > 0 and n_survive == 0}")

parent_claim = {Fraction(9, 13), Fraction(19, 26), Fraction(4, 13)}
got = {r[3] for r in rows}
print(f"\nparent's stated landing values {{9/13, 19/26, 19/26, 4/13}}")
print(f"  distinct values I compute: {sorted(got)}")
print(f"  set match: {got == parent_claim}")
print(f"  multiset I compute: {sorted(r[3] for r in rows)}")
print(f"  side p-values I compute: {sorted(r[2] for r in rows)}  "
      f"[parent says 2/3, 2/3, 2/3, 1/3]")

# ---- delta of each side, to confirm 'zero interior slack' (parent's Sec 6.1)
print("\nInterior slack of each side's balanced pairs "
      "(min distance from p_side to an endpoint of [1/3,2/3]):")
for nm, mask in (("A", Amask), ("B", Bmask)):
    sub, k, elems = induced(rel, N, mask)
    sdp = le_dp(sub, k)
    sbefore, stot = pair_probs(sub, k, sdp)
    for (x, y) in incomparable_pairs(sub, k):
        p_side = Fraction(sbefore[x][y], stot)
        if balanced(p_side):
            slack = min(p_side - THIRD, TWOTHIRD - p_side)
            print(f"  side {nm} pair ({elems[x]},{elems[y]}): p={p_side} slack={slack}")
