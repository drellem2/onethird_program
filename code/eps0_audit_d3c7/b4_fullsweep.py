"""B4 — unpruned sweep, and CLOSING the coverage gap mg-3969 disclosed in its Sec 9.

mg-3969 Sec 9 says, in its own words:

  "My sweeps skip every cut at which *either* side is a chain -- a coverage gap I
   did not close. Only the *both*-sides-chain case is genuinely outside the
   statement (Remark 5.0). When exactly ONE side is a chain the architecture still
   works -- the other side supplies the pair -- and a violator could live there.
   Excluding those cuts makes the population smaller, so it can only make my
   ceiling TOO HIGH: the bounds stand, and a sweep that includes them may lower both."

That is an honest disclosure of an open hole, and it is cheap to close, so this
script closes it.  Three scope regimes, exhaustive to n = 7, no pruning:

  BOTH   -- both sides non-chain          (mg-3969's scope; reproduces its counts)
  ONE+   -- at least one side non-chain   (the gap CLOSED: a chain side simply
                                           contributes no balanced pair)
  Also reported: total failure counts, so a population mismatch with mg-3969
  would show up as a count mismatch rather than passing silently.

Usage:  python3 b4_fullsweep.py [max_n]
"""

import sys
from fractions import Fraction

from lib_d3c7 import (naturally_labelled_posets, le_dp, delta1, pair_probs,
                      incomparable_pairs, induced, is_chain, balanced)

MAX_N = int(sys.argv[1]) if len(sys.argv) > 1 else 7


def cut_facts(rel, n, k, dp):
    """Return (kA, kB, chainA, chainB, pairs) where pairs is a list of
    (side, (x,y), p_side, p_P, survives) over pairs balanced in their own side."""
    amask = (1 << k) - 1
    bmask = ((1 << n) - 1) ^ amask
    subA, kA, elemsA = induced(rel, n, amask)
    subB, kB, elemsB = induced(rel, n, bmask)
    cA, cB = is_chain(subA, kA), is_chain(subB, kB)
    if cA and cB:
        return kA, kB, cA, cB, None       # genuinely outside the statement
    beforeP, totP = pair_probs(rel, n, dp)
    pairs = []
    for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)), ("B", (subB, kB, elemsB))):
        if is_chain(sub, ks):
            continue
        sdp = le_dp(sub, ks)
        sbefore, stot = pair_probs(sub, ks, sdp)
        for (x, y) in incomparable_pairs(sub, ks):
            p_side = Fraction(sbefore[x][y], stot)
            if not balanced(p_side):
                continue
            gx, gy = elems[x], elems[y]
            p_P = Fraction(beforeP[gx][gy], totP)
            pairs.append((nm, (gx, gy), p_side, p_P, balanced(p_P)))
    return kA, kB, cA, cB, pairs


stats = {}
for scope in ("BOTH", "ONE+"):
    stats[scope] = dict(inscope=0, fail_e=0, best_e=None,
                        fail_s=0, best_s=None, nobal=0)

for n in range(2, MAX_N + 1):
    per_n = {s: dict(inscope=0, fail_e=0, fail_s=0) for s in stats}
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            kA, kB, cA, cB, pairs = cut_facts(rel, n, k, dp)
            if pairs is None:
                continue                       # both sides chains
            d1 = delta1(rel, n, k, dp)
            both = (not cA) and (not cB)
            for scope in ("BOTH", "ONE+"):
                if scope == "BOTH" and not both:
                    continue
                st, pn = stats[scope], per_n[scope]
                st["inscope"] += 1
                pn["inscope"] += 1
                if not pairs:
                    st["nobal"] += 1
                    continue
                # U_either
                if not any(p[4] for p in pairs):
                    st["fail_e"] += 1
                    pn["fail_e"] += 1
                    if st["best_e"] is None or d1 < st["best_e"][0]:
                        st["best_e"] = (d1, n, k, list(rel))
                # U_smaller: only defined when the sides differ in size, and the
                # smaller side must actually offer a pair.
                if kA != kB:
                    sm = "A" if kA < kB else "B"
                    sp = [p for p in pairs if p[0] == sm]
                    if sp and not any(p[4] for p in sp):
                        st["fail_s"] += 1
                        pn["fail_s"] += 1
                        if st["best_s"] is None or d1 < st["best_s"][0]:
                            st["best_s"] = (d1, n, k, list(rel))
    line = f"n={n}: "
    for scope in ("BOTH", "ONE+"):
        pn = per_n[scope]
        line += (f"[{scope}] cuts={pn['inscope']} U_either_fail={pn['fail_e']} "
                 f"U_smaller_fail={pn['fail_s']}   ")
    print(line)
    sys.stdout.flush()

print()
for scope in ("BOTH", "ONE+"):
    st = stats[scope]
    print(f"=== scope {scope} (cumulative to n={MAX_N}) ===")
    print(f"  cuts in scope: {st['inscope']}")
    print(f"  cuts with no balanced-in-side pair at all: {st['nobal']}")
    for nm, key in (("U_either", "best_e"), ("U_smaller", "best_s")):
        fk = "fail_e" if key == "best_e" else "fail_s"
        b = st[key]
        if b is None:
            print(f"  {nm}: 0 violators")
        else:
            print(f"  {nm}: {st[fk]} violators; thinnest Delta_1 = {b[0]} "
                  f"= {float(b[0]):.6f} at n={b[1]} k={b[2]} rel={b[3]}")
    print()

print("CEILING COMPARISON vs mg-3969")
be_both = stats["BOTH"]["best_e"]
be_one = stats["ONE+"]["best_e"]
bs_both = stats["BOTH"]["best_s"]
bs_one = stats["ONE+"]["best_s"]
print(f"  U_either  mg-3969 (BOTH scope): 17/78 = 0.217949")
print(f"  U_either  mine    (BOTH scope): {be_both[0]} = {float(be_both[0]):.6f}  "
      f"MATCH={be_both[0] == Fraction(17,78)}")
print(f"  U_either  mine    (ONE+ scope): {be_one[0]} = {float(be_one[0]):.6f}  "
      f"GAP LOWERS THE CEILING={be_one[0] < Fraction(17,78)}")
print(f"  U_smaller mg-3969 (BOTH scope): 13/111 = 0.117117")
print(f"  U_smaller mine    (BOTH scope): {bs_both[0]} = {float(bs_both[0]):.6f}  "
      f"MATCH={bs_both[0] == Fraction(13,111)}")
print(f"  U_smaller mine    (ONE+ scope): {bs_one[0]} = {float(bs_one[0]):.6f}  "
      f"GAP LOWERS THE CEILING={bs_one[0] < Fraction(13,111)}")
