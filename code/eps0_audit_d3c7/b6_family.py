"""B6 — the n=7 gap witness is the first member of an INFINITE family, and the
family drives the uniform ceiling to ZERO.

B5 certified a U_either violator at Delta_1 = 1/7 in the architecturally required
scope (at least one side non-chain -- mg-3969's own Sec 9 says the both-sides-chain
case is the only one genuinely outside the statement).  Inspecting it shows a
mechanism that does not depend on n:

    P(n, k) :=  a chain  c_1 < c_2 < ... < c_{n-1}   PLUS one isolated element z.
    A       :=  {z, c_1, ..., c_{k-1}}      (a down-set, so a legitimate prefix cut)
    B       :=  {c_k, ..., c_{n-1}}         (a chain: contributes no pair)

Hand derivation (verified below in exact rationals for every case computed):

  * e(P) = n           -- z may occupy any of the n slots, the chain is forced.
  * p^P(z < c_j) = j/n -- z precedes c_j iff z's slot index is <= j-1.
  * side A is z plus the chain c_1<...<c_{k-1}, so by the same argument
    p^A(z < c_j) = j/k.
  * |A \\ sigma(A)| = 1 iff z lands at slot >= k, which happens in n-k of the n
    extensions, so  E|A \\ sigma(A)| = (n-k)/n  and
        Delta_1(A,B) = (n-k) / (n * min(k, n-k)).
  * A pair (z,c_j) is balanced IN THE SIDE iff  k/3 <= j <= 2k/3,
    and it is EVICTED in P iff j/n < 1/3 (it cannot exceed 2/3, since j/n < j/k).
  * So EVERY balanced-in-side pair is evicted as soon as  2k/3 < n/3, i.e. n > 2k.

Taking n = 2k+1 gives min(k,n-k) = k and

        Delta_1 = (k+1) / ((2k+1) k)   ->   0   as k -> infinity,

with every balanced-in-side pair evicted at every k >= 3.  Hence

        eps_0(U_either) = eps_0(U_smaller) = 0

in the architecturally required scope: NOT bounded by 17/78, but zero.

This script verifies the family member by member with the library (exact
Fractions), and cross-checks the small ones against the n!-filtering path.
"""

from fractions import Fraction
from itertools import permutations

from lib_d3c7 import (le_dp, delta1, pair_probs, incomparable_pairs,
                      induced, is_chain, balanced)


def build(n):
    """chain c_1<...<c_{n-1} on labels 1..n-1, plus isolated z = label 0."""
    rel = [0] * n
    for j in range(2, n):
        rel[j] = ((1 << j) - 1) & ~1        # all of 1..j-1, not 0
    return tuple(rel)


def bf_les(rel, n):
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for i, e in enumerate(perm):
            pos[e] = i
        if all(not (rel[j] >> i & 1) or pos[i] < pos[j]
               for j in range(n) for i in range(n)):
            out.append(perm)
    return out


def examine(n, k, brute=False):
    rel = build(n)
    dp = le_dp(rel, n)
    e = dp[3]
    d1 = delta1(rel, n, k, dp)

    amask = (1 << k) - 1
    bmask = ((1 << n) - 1) ^ amask
    subA, kA, elemsA = induced(rel, n, amask)
    subB, kB, elemsB = induced(rel, n, bmask)
    beforeP, totP = pair_probs(rel, n, dp)

    bal, surv, detail = 0, 0, []
    for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)), ("B", (subB, kB, elemsB))):
        if is_chain(sub, ks):
            continue
        sdp = le_dp(sub, ks)
        sbefore, stot = pair_probs(sub, ks, sdp)
        for (x, y) in incomparable_pairs(sub, ks):
            p_side = Fraction(sbefore[x][y], stot)
            if not balanced(p_side):
                continue
            bal += 1
            gx, gy = elems[x], elems[y]
            p_P = Fraction(beforeP[gx][gy], totP)
            s = balanced(p_P)
            surv += s
            detail.append((nm, (gx, gy), p_side, p_P, s))

    # hand formulas
    hand_e = n
    hand_d1 = Fraction(n - k, n * min(k, n - k))
    ok_e = (e == hand_e)
    ok_d1 = (d1 == hand_d1)

    res = dict(n=n, k=k, e=e, d1=d1, bal=bal, surv=surv,
               viol=(bal > 0 and surv == 0), detail=detail,
               chainA=is_chain(subA, kA), chainB=is_chain(subB, kB),
               ok_e=ok_e, ok_d1=ok_d1)

    if brute:
        les = bf_les(rel, n)
        A = set(range(k))
        tot = sum(len(A - set(p[:k])) for p in les)
        bd1 = Fraction(tot, len(les) * min(k, n - k))
        res["brute_e"] = len(les)
        res["brute_d1"] = bd1
        res["brute_ok"] = (len(les) == e and bd1 == d1)
    return res


print("=" * 78)
print("PART A — the family at n = 2k+1 (so n > 2k, every balanced pair evicted)")
print("=" * 78)
print(f"{'k':>4} {'n':>5} {'e(P)':>6} {'Delta_1':>14} {'float':>10} "
      f"{'bal':>4} {'surv':>5} {'VIOLATES':>9} {'hand e':>7} {'hand d1':>8} {'brute':>6}")
allviol = True
for k in range(3, 21):
    n = 2 * k + 1
    r = examine(n, k, brute=(n <= 9))
    allviol &= r["viol"]
    print(f"{k:>4} {n:>5} {r['e']:>6} {str(r['d1']):>14} {float(r['d1']):>10.6f} "
          f"{r['bal']:>4} {r['surv']:>5} {str(r['viol']):>9} {str(r['ok_e']):>7} "
          f"{str(r['ok_d1']):>8} {str(r.get('brute_ok','-')):>6}")
print(f"\nall members violate U_either: {allviol}")

print()
print("PART A2 — pushing k further (hand formula + library agreement only)")
for k in (30, 50, 100, 200):
    n = 2 * k + 1
    r = examine(n, k)
    print(f"  k={k:<4} n={n:<4} Delta_1 = {r['d1']} = {float(r['d1']):.8f}  "
          f"balanced-in-side={r['bal']} surviving={r['surv']} "
          f"VIOLATES={r['viol']}  hand-formula-agrees={r['ok_d1']}")

print()
print("=" * 78)
print("PART B — the detail of the smallest members, so the mechanism is visible")
print("=" * 78)
for k in (3, 4, 5):
    n = 2 * k + 1
    r = examine(n, k, brute=(n <= 11))
    print(f"\nn={n} k={k}: A = {{z=0}} U {{1..{k-1}}}, B = chain {{{k}..{n-1}}}")
    print(f"  e(P) = {r['e']} (hand: {n}), Delta_1 = {r['d1']} "
          f"(hand: {Fraction(n-k, n*min(k,n-k))})")
    print(f"  side A chain? {r['chainA']}   side B chain? {r['chainB']}")
    for (nm, pair, ps, pp, s) in r["detail"]:
        print(f"    side {nm} pair {pair}: p_side={ps} -> p_P={pp}  survives={s}")
    print(f"  VIOLATES U_either: {r['viol']}")

print()
print("=" * 78)
print("PART C — is the SMALLER side the non-chain one? (so U_smaller falls too)")
print("=" * 78)
for k in (3, 5, 10, 50):
    n = 2 * k + 1
    print(f"  k={k} n={n}: |A|={k} |B|={n-k} -> smaller side is "
          f"{'A (the non-chain one)' if k < n-k else 'B'}; "
          f"U_smaller violated = {examine(n,k)['viol']}")

print()
print("=" * 78)
print("CONCLUSION")
print("=" * 78)
print("  In the architecturally required scope (at least one side non-chain):")
print("     inf over the family of Delta_1 = lim_{k->inf} (k+1)/((2k+1)k) = 0")
print("     and EVERY member is a U_either AND U_smaller violator.")
print("  Therefore eps_0(U_either) = eps_0(U_smaller) = 0 in that scope,")
print("  which is not 'bounded by 17/78' -- it is REFUTED at every positive eps.")
print()
print("  In mg-3969's own scope (BOTH sides non-chain) its 17/78 stands:")
print("  the family always has a chain side, so it never enters that population.")
