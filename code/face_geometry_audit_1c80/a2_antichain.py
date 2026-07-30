"""mg-1c80 part 2 -- THE ANTICHAIN FAMILY, rebuilt SPARSELY and pushed to n = 8.

The three posets row I4 keeps absorbability scored for are the antichains at
n = 3, 4, 5 (part 1 identifies them).  mg-f1b2 measured them and the n = 6
antichain; mg-da45 asserts, in `controls.py`'s section docstring, that the
answer is

    "forced at every n and not merely measured to n = 5: ... exactly one
     neighbour of every vertex changes: 2|L(P)| mismatched entries at every
     n >= 3."

That sentence contains FOUR separable claims, and this file scores each one
separately rather than checking only the arithmetic they add up to:

  (i)   `le_to_facet_offbyone(w) == le_to_facet(rot(w))`, rot the LEFT CYCLIC
        ROTATION OF POSITIONS.
  (ii)  conjugation by rot carries n-2 of the n-1 adjacent transpositions to
        adjacent transpositions and exactly one out of the set.
  (iii) exactly one neighbour of every vertex changes, so 2 entries per row.
  (iv)  the diagonal is preserved, so the answer is reached at the ABSOLUTE-
        VALUE gate and not the diagonal one.

Nothing here is dense: at n = 8 the matrices are 40320 x 40320, so the boundary,
the relative Laplacian and the target are all carried as dictionaries.  That is
also why this file can go two sizes past the audited claim.
"""

import sys
from itertools import permutations

sys.path.insert(0, "../face_geometry")

from kern1c80 import facets_offbyone, facets_true, my_sign, rot          # noqa: E402

BAR = "=" * 78
NMAX = 8


def sparse_L_rel(words, facet_rule):
    """Twisted relative top Laplacian E.L^rel.E as {(i,j): v}, built from the
    boundary with no dense matrix anywhere."""
    facets = [facet_rule(w) for w in words]
    rows = {}
    for j, f in enumerate(facets):
        for i in range(len(f)):
            r = f[:i] + f[i + 1:]
            rows.setdefault(r, {})
            rows[r][j] = rows[r].get(j, 0) + (-1) ** i
    s = [my_sign(w) for w in words]
    L = {}
    for r, row in rows.items():
        if len(row) != 2:                      # only interior ridges survive
            continue
        items = list(row.items())
        for (j1, c1) in items:
            for (j2, c2) in items:
                v = s[j1] * c1 * c2 * s[j2]
                if v:
                    L[(j1, j2)] = L.get((j1, j2), 0) + v
    return {k: v for k, v in L.items() if v}


def sparse_target(words):
    """D - A on the adjacent-transposition graph of S_n, as {(i,j): v}."""
    idx = {w: i for i, w in enumerate(words)}
    n = len(words[0])
    T = {}
    for w in words:
        i = idx[w]
        d = 0
        for t in range(n - 1):
            v = list(w)
            v[t], v[t + 1] = v[t + 1], v[t]
            T[(i, idx[tuple(v)])] = -1
            d += 1
        T[(i, i)] = d
    return T


print(BAR)
print("mg-1c80 part 2 -- the antichain family, from a sparse rebuild, to n = %d"
      % NMAX)
print(BAR)
print()

# ---------------------------------------------------------------------------
print("(i) le_to_facet_offbyone(w) == le_to_facet(rot(w)) ?")
ok = bad = 0
for n in range(2, NMAX + 1):
    for w in permutations(range(n)):
        if facets_offbyone(w) == facets_true(rot(w)):
            ok += 1
        else:
            bad += 1
print("    %d words checked (n = 2..%d): %d hold, %d FAIL" % (ok + bad, NMAX, ok, bad))
print()

# ---------------------------------------------------------------------------
print("(ii) conjugating the generators by rot: how many stay adjacent?")
print("     s_t swaps POSITIONS t, t+1.  rot(w) = w[1:] + w[:1].  The claim is")
print("     n-2 of the n-1 generators map to generators and exactly one leaves.")
for n in range(3, NMAX + 1):
    stay = leave = 0
    ident = tuple(range(n))
    for t in range(n - 1):
        v = list(ident)
        v[t], v[t + 1] = v[t + 1], v[t]
        # rot(w . s_t) = rot(w) . s_t'  -- find s_t' by acting on one word
        a, b = rot(tuple(v)), rot(ident)
        moved = [p for p in range(n) if a[p] != b[p]]
        adjacent = (len(moved) == 2 and moved[1] == moved[0] + 1)
        stay += adjacent
        leave += not adjacent
    print("     n=%d: %d of %d generators stay adjacent, %d leave%s"
          % (n, stay, n - 1, leave, "  [as claimed]" if (stay, leave) == (n - 2, 1)
             else "  [*** NOT AS CLAIMED ***]"))
print()

# ---------------------------------------------------------------------------
print(BAR)
print("(iii)+(iv) THE MISMATCH CENSUS ON THE ANTICHAIN, n = 3..%d" % NMAX)
print(BAR)
print()
print("   %3s %8s %10s %10s %8s %10s %10s %8s"
      % ("n", "|L(P)|", "mag mism", "predicted", "per row", "sign-only",
         "diag pres", "gate"))
for n in range(3, NMAX + 1):
    words = sorted(permutations(range(n)))
    m = len(words)
    L = sparse_L_rel(words, facets_offbyone)
    T = sparse_target(words)
    keys = set(L) | set(T)
    mag = sgn = 0
    per_row = {}
    diag_ok = True
    for (i, j) in keys:
        a, b = L.get((i, j), 0), T.get((i, j), 0)
        if i == j:
            if a != b:
                diag_ok = False
            continue
        if abs(a) != abs(b):
            mag += 1
            per_row[i] = per_row.get(i, 0) + 1
        elif a != b:
            sgn += 1
    counts = sorted(set(per_row.get(i, 0) for i in range(m)))
    # which gate does the predicate reach?  diagonal first, then magnitudes.
    gate = "diagonal" if not diag_ok else ("magnitude" if mag else
                                           ("parity" if sgn else "equal"))
    print("   %3d %8d %10d %10d %8s %10d %10s %8s"
          % (n, m, mag, 2 * m,
             ",".join(str(c) for c in counts), sgn, diag_ok, gate))
print()
print("   'predicted' is 2|L(P)| = 2.n!, the closed form the repair's docstring")
print("   asserts.  'per row' is the set of per-row off-diagonal magnitude")
print("   mismatch counts over all %s rows -- a single value 2 is the claim" % "n!")
print("   'exactly one neighbour of every vertex changes'.")
print()
