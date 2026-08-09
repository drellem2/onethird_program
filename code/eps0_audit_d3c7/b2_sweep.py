"""B2 — my own exhaustive sweep for U_either / U_smaller violators.

Purpose (brief item 4): the parent asserts a CEILING, and a ceiling of this shape
is the claim 'no violator thinner than 17/78 exists in the population'.  That is
a negative.  This script tries to CONSTRUCT the thing the negative says does not
exist, by re-running the search from my own definitions over the same population.

Definitions used (parent's doc Sec 6, restated here in my own terms so the reading
is auditable):

  U_either(eps): for every poset P, every prefix cut (A,B) with Delta_1(A,B) <= eps
                 and NEITHER side a chain, SOME pair that is balanced in P[A] or in
                 P[B] is still in [1/3,2/3] in P.
  U_smaller(eps): same, but the surviving pair must come from the SMALLER side.

A cut VIOLATES U_either iff both sides are non-chain, at least one balanced-in-side
pair exists, and EVERY such pair leaves [1/3,2/3] in P.  The ceiling is then
    eps_0(U_either) <= min{ Delta_1(cut) : cut violates }.

Usage:  python3 b2_sweep.py [max_n]
"""

import sys
from fractions import Fraction

from lib_d3c7 import (naturally_labelled_posets, le_dp, delta1, pair_probs,
                      incomparable_pairs, induced, is_chain, balanced)

MAX_N = int(sys.argv[1]) if len(sys.argv) > 1 else 6

# Prune threshold: we only need the full pair analysis on cuts that could
# LOWER the ceiling, plus (for reporting) everything at n<=6 so the failure
# counts are comparable with the parent's.  PRUNE=None means analyse everything.
PRUNE = Fraction(17, 78) if MAX_N >= 7 else None


def analyse(rel, n, k, dp):
    """Return (violates_either, violates_smaller, n_bal, n_survive_either,
    n_survive_smaller) or None if the cut is out of scope (a side is a chain)."""
    amask = (1 << k) - 1
    bmask = ((1 << n) - 1) ^ amask
    subA, kA, elemsA = induced(rel, n, amask)
    if is_chain(subA, kA):
        return None
    subB, kB, elemsB = induced(rel, n, bmask)
    if is_chain(subB, kB):
        return None

    beforeP, totP = pair_probs(rel, n, dp)
    n_bal = 0
    surv_e = 0
    surv_s = 0
    smaller = "A" if kA < kB else ("B" if kB < kA else "tie")
    for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)), ("B", (subB, kB, elemsB))):
        sdp = le_dp(sub, ks)
        sbefore, stot = pair_probs(sub, ks, sdp)
        for (x, y) in incomparable_pairs(sub, ks):
            p_side = Fraction(sbefore[x][y], stot)
            if not balanced(p_side):
                continue
            n_bal += 1
            gx, gy = elems[x], elems[y]
            if balanced(Fraction(beforeP[gx][gy], totP)):
                surv_e += 1
                if smaller == "tie" or nm == smaller:
                    surv_s += 1
    if n_bal == 0:
        # No pair to transfer at all -- U_* is vacuously satisfied here, but
        # record it: the parent's Remark 5.0 says this needs both sides to be
        # chains, which we have already excluded, so it should never happen.
        return ("NOBAL", None, 0, 0, 0)
    return (surv_e == 0, surv_s == 0, n_bal, surv_e, surv_s)


best_either = None      # (Delta_1, n, k, rel)
best_smaller = None
nobal = []

for n in range(2, MAX_N + 1):
    n_posets = 0
    n_nonchain = 0
    n_cuts_nonchain_poset = 0
    n_cuts_all = 0
    n_inscope = 0
    fail_e = 0
    fail_s = 0
    for rel in naturally_labelled_posets(n):
        n_posets += 1
        n_cuts_all += (n - 1)
        chain = is_chain(rel, n)
        if not chain:
            n_nonchain += 1
            n_cuts_nonchain_poset += (n - 1)
        dp = le_dp(rel, n)
        for k in range(1, n):
            d1 = delta1(rel, n, k, dp)
            if PRUNE is not None and d1 >= PRUNE:
                # cannot lower either ceiling; skip the expensive part
                continue
            res = analyse(rel, n, k, dp)
            if res is None:
                continue
            n_inscope += 1
            if res[0] == "NOBAL":
                nobal.append((n, k, rel))
                continue
            ve, vs, nb, se, ss = res
            if ve:
                fail_e += 1
                if best_either is None or d1 < best_either[0]:
                    best_either = (d1, n, k, rel)
            if vs:
                fail_s += 1
                if best_smaller is None or d1 < best_smaller[0]:
                    best_smaller = (d1, n, k, rel)
    print(f"n={n}: posets={n_posets} non-chain={n_nonchain} "
          f"cuts(all posets)={n_cuts_all} cuts(non-chain posets)={n_cuts_nonchain_poset} "
          f"both-sides-non-chain analysed={n_inscope} "
          f"U_either failures={fail_e} U_smaller failures={fail_s}"
          + ("  [PRUNED to Delta_1 < 17/78]" if PRUNE is not None else ""))
    sys.stdout.flush()

print()
if PRUNE is not None:
    print(f"NOTE: pruned at Delta_1 < {PRUNE}; failure counts above are NOT totals,")
    print("      they are counts of failures that would LOWER the ceiling.")
print()
for nm, best in (("U_either", best_either), ("U_smaller", best_smaller)):
    if best is None:
        print(f"{nm}: NO violator found below the prune threshold")
        continue
    d1, n, k, rel = best
    print(f"{nm}: thinnest violator  Delta_1 = {d1} = {float(d1):.6f}  "
          f"at n={n}, k={k}, rel={list(rel)}")
    print(f"   => eps_0({nm}) <= {d1}")

print()
print(f"cuts with both sides non-chain but NO balanced-in-side pair: {len(nobal)}")
if nobal:
    print(f"   first few: {nobal[:5]}")
