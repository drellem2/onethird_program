"""B3 — chase the one place my sweep DISAGREES with mg-3969.

B2 finds the thinnest U_smaller violator at n<=6 to be Delta_1 = 13/74 = 0.17568.
The parent (doc Sec 6, Claim 6.2 and the Sec 6.0 table) reports 1/7 = 0.142857,
"unique smaller-side pair 1/2 -> 5/7".  1/7 < 13/74, so one of us is wrong.

This script (a) lists every n<=6 cut with Delta_1 = 1/7 and reports its status
under several readings of "smaller side", and (b) lists the thinnest U_smaller
violators under each reading, so the disagreement is localised to a DEFINITION
rather than left as a bare numeric mismatch.

Readings of "the pair must come from the smaller side" when |A| == |B|:
  TIE_EITHER  -- a tie means either side counts (what B2 used)
  TIE_NEITHER -- a tie means the cut is out of scope for U_smaller
  TIE_A       -- on a tie, "smaller" means the prefix A
Also tested: whether the LARGER side is allowed to be a chain.
"""

from fractions import Fraction

from lib_d3c7 import (naturally_labelled_posets, le_dp, delta1, pair_probs,
                      incomparable_pairs, induced, is_chain, balanced)

TARGET = Fraction(1, 7)


def sides(rel, n, k):
    amask = (1 << k) - 1
    bmask = ((1 << n) - 1) ^ amask
    return induced(rel, n, amask), induced(rel, n, bmask)


def side_report(rel, n, k, dp):
    (subA, kA, elemsA), (subB, kB, elemsB) = sides(rel, n, k)
    beforeP, totP = pair_probs(rel, n, dp)
    out = {}
    for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)), ("B", (subB, kB, elemsB))):
        sdp = le_dp(sub, ks)
        sbefore, stot = pair_probs(sub, ks, sdp)
        pairs = []
        for (x, y) in incomparable_pairs(sub, ks):
            p_side = Fraction(sbefore[x][y], stot)
            if balanced(p_side):
                gx, gy = elems[x], elems[y]
                p_P = Fraction(beforeP[gx][gy], totP)
                pairs.append(((gx, gy), p_side, p_P, balanced(p_P)))
        out[nm] = dict(size=ks, chain=is_chain(sub, ks), pairs=pairs)
    return out


print("=" * 78)
print("PART A — every n<=6 prefix cut with Delta_1 exactly 1/7")
print("=" * 78)
hits = 0
for n in range(2, 7):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            if delta1(rel, n, k, dp) != TARGET:
                continue
            hits += 1
            r = side_report(rel, n, k, dp)
            kA, kB = r["A"]["size"], r["B"]["size"]
            smaller = "A" if kA < kB else ("B" if kB < kA else "TIE")
            # is it a U_smaller violator under any reading?
            def viol(nm):
                ps = r[nm]["pairs"]
                return len(ps) > 0 and not any(p[3] for p in ps)
            note = []
            if r["A"]["chain"] or r["B"]["chain"]:
                note.append(f"side chain: A={r['A']['chain']} B={r['B']['chain']}")
            if hits <= 40:
                print(f"\nn={n} k={k} rel={list(rel)} e={dp[3]} smaller={smaller} "
                      f"|A|={kA} |B|={kB} {' '.join(note)}")
                for nm in ("A", "B"):
                    print(f"   side {nm} (size {r[nm]['size']}, chain={r[nm]['chain']}): "
                          f"balanced pairs = {[(p[0], str(p[1]), str(p[2]), p[3]) for p in r[nm]['pairs']]}")
                print(f"   violates-if-smaller-is-A: {viol('A')}   "
                      f"violates-if-smaller-is-B: {viol('B')}")
print(f"\ntotal n<=6 cuts with Delta_1 == 1/7: {hits}")

print()
print("=" * 78)
print("PART B — thinnest U_smaller violator under each reading, n<=6")
print("=" * 78)

READINGS = ["TIE_EITHER", "TIE_NEITHER", "TIE_A"]
for allow_large_chain in (False, True):
    best = {r: None for r in READINGS}
    for n in range(2, 7):
        for rel in naturally_labelled_posets(n):
            dp = le_dp(rel, n)
            for k in range(1, n):
                d1 = delta1(rel, n, k, dp)
                (subA, kA, _), (subB, kB, _) = sides(rel, n, k)
                cA, cB = is_chain(subA, kA), is_chain(subB, kB)
                small_nm = "A" if kA < kB else ("B" if kB < kA else "TIE")
                if not allow_large_chain and (cA or cB):
                    continue
                if allow_large_chain:
                    # the SMALLER side must still be non-chain, else no pair
                    if small_nm == "A" and cA:
                        continue
                    if small_nm == "B" and cB:
                        continue
                    if small_nm == "TIE" and cA and cB:
                        continue
                r = side_report(rel, n, k, dp)

                def viol(nm):
                    ps = r[nm]["pairs"]
                    return len(ps) > 0 and not any(p[3] for p in ps)

                for reading in READINGS:
                    if small_nm == "TIE":
                        if reading == "TIE_NEITHER":
                            continue
                        v = (viol("A") and viol("B")) if reading == "TIE_EITHER" else viol("A")
                        # TIE_EITHER: survivor may come from either -> violated
                        # only if neither side supplies a survivor
                    else:
                        v = viol(small_nm)
                    if v and (best[reading] is None or d1 < best[reading][0]):
                        best[reading] = (d1, n, k, list(rel))
    tag = "larger side MAY be a chain" if allow_large_chain else "BOTH sides non-chain"
    print(f"\n[{tag}]")
    for reading in READINGS:
        b = best[reading]
        if b is None:
            print(f"  {reading:12s}: none")
        else:
            print(f"  {reading:12s}: Delta_1 = {b[0]} = {float(b[0]):.6f}  "
                  f"n={b[1]} k={b[2]} rel={b[3]}")
