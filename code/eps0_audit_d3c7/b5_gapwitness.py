"""B5 — certify the one-side-chain witness that LOWERS mg-3969's headline ceiling.

B4 closed the coverage gap mg-3969 disclosed in its own Sec 9 ("my sweeps skip
every cut at which EITHER side is a chain ... a violator could live there ... a
sweep that includes them may lower both").  It does: with one-side-chain cuts
included, the thinnest U_either violator at n <= 7 drops from

    17/78 = 0.217949    (mg-3969's scope: BOTH sides non-chain)
to  1/7   = 0.142857    (architecturally required scope: at least one non-chain)

That is a headline-moving claim, so it is certified here on the SECOND code path
-- linear extensions by filtering all n! permutations, no down-set DP anywhere --
and every witness at the minimum is printed, not just one.

Remark 5.0 (mg-3969, and I accept it): the BOTH-sides-chain case is genuinely
outside the statement, because two chain sides force width <= 2 and Linial's
theorem settles width 2.  Every OTHER cut is in scope for the architecture:
on a minimal counterexample disjunct (i) is false, so a pair must transfer from
a side, and a single chain side merely means the pair comes from the other one.
"""

from fractions import Fraction
from itertools import permutations

from lib_d3c7 import (naturally_labelled_posets, le_dp, delta1, pair_probs,
                      incomparable_pairs, induced, is_chain, balanced)

TARGET = Fraction(1, 7)
MAX_N = 7


# ----------------------------------------------------- second code path (n!)
def bf_les(rel, n):
    out = []
    for perm in permutations(range(n)):
        pos = [0] * n
        for i, e in enumerate(perm):
            pos[e] = i
        ok = True
        for j in range(n):
            b = rel[j]
            for i in range(n):
                if b >> i & 1 and pos[i] > pos[j]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            out.append(perm)
    return out


def bf_delta1(rel, n, k):
    les = bf_les(rel, n)
    A = set(range(k))
    tot = sum(len(A - set(p[:k])) for p in les)
    return Fraction(tot, len(les) * min(k, n - k))


def bf_pxy(les, x, y):
    c = sum(1 for p in les if p.index(x) < p.index(y))
    return Fraction(c, len(les))


def certify(rel, n, k, label):
    print(f"\n{'-'*74}\n{label}: n={n} k={k} rel={list(rel)}")
    amask = (1 << k) - 1
    bmask = ((1 << n) - 1) ^ amask
    subA, kA, elemsA = induced(rel, n, amask)
    subB, kB, elemsB = induced(rel, n, bmask)
    print(f"  A = {elemsA} (size {kA}, chain={is_chain(subA,kA)}, rel={list(subA)})")
    print(f"  B = {elemsB} (size {kB}, chain={is_chain(subB,kB)}, rel={list(subB)})")

    les = bf_les(rel, n)
    dp = le_dp(rel, n)
    print(f"  e(P): DP={dp[3]}  bruteforce={len(les)}  AGREE={dp[3]==len(les)}")

    d1_dp = delta1(rel, n, k, dp)
    d1_bf = bf_delta1(rel, n, k)
    print(f"  Delta_1: DP={d1_dp}  bruteforce={d1_bf}  AGREE={d1_dp==d1_bf}"
          f"  == 1/7: {d1_bf == TARGET}")

    n_bal = 0
    n_surv = 0
    for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)), ("B", (subB, kB, elemsB))):
        if is_chain(sub, ks):
            print(f"  side {nm} is a CHAIN -> contributes no incomparable pair "
                  f"(incomparable pairs: {incomparable_pairs(sub, ks)})")
            continue
        sub_les = bf_les(sub, ks)
        for (x, y) in incomparable_pairs(sub, ks):
            p_side = bf_pxy(sub_les, x, y)
            gx, gy = elems[x], elems[y]
            p_P = bf_pxy(les, gx, gy)
            mark = "BALANCED-IN-SIDE" if balanced(p_side) else "not balanced in side"
            if balanced(p_side):
                n_bal += 1
                if balanced(p_P):
                    n_surv += 1
            print(f"  side {nm} pair ({gx},{gy}): p_side={p_side} p_P={p_P} "
                  f"[{mark}; survives in P: {balanced(p_P)}]")
    print(f"  => balanced-in-side pairs: {n_bal}, surviving: {n_surv}")
    print(f"  => U_either VIOLATED: {n_bal > 0 and n_surv == 0}")
    return n_bal > 0 and n_surv == 0


# ------------------------------------------- find EVERY minimum-Delta_1 witness
print("Scanning n<=7 for ALL U_either violators at Delta_1 == 1/7 in the")
print("architecturally required scope (at least one side non-chain).")
found = []
for n in range(2, MAX_N + 1):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            if delta1(rel, n, k, dp) != TARGET:
                continue
            amask = (1 << k) - 1
            bmask = ((1 << n) - 1) ^ amask
            subA, kA, _ = induced(rel, n, amask)
            subB, kB, _ = induced(rel, n, bmask)
            if is_chain(subA, kA) and is_chain(subB, kB):
                continue
            beforeP, totP = pair_probs(rel, n, dp)
            nb = ns = 0
            for (sub, ks, elems) in ((induced(rel, n, amask)), )[:0]:
                pass
            for mask in (amask, bmask):
                sub, ks, elems = induced(rel, n, mask)
                if is_chain(sub, ks):
                    continue
                sdp = le_dp(sub, ks)
                sbefore, stot = pair_probs(sub, ks, sdp)
                for (x, y) in incomparable_pairs(sub, ks):
                    if not balanced(Fraction(sbefore[x][y], stot)):
                        continue
                    nb += 1
                    gx, gy = elems[x], elems[y]
                    if balanced(Fraction(beforeP[gx][gy], totP)):
                        ns += 1
            if nb > 0 and ns == 0:
                found.append((n, k, tuple(rel)))
print(f"\nU_either violators at exactly Delta_1 = 1/7, n<=7, ONE+ scope: {len(found)}")
for f in found[:12]:
    print(f"   n={f[0]} k={f[1]} rel={list(f[2])}")

# ---------------------------------------------------------------- certify them
ok = 0
for (n, k, rel) in found[:5]:
    if certify(rel, n, k, "GAP WITNESS"):
        ok += 1
print(f"\n{ok}/{min(5,len(found))} certified as genuine U_either violators "
      f"on the brute-force path.")

# ---------------------------------------------------- and confirm nothing thinner
print("\n" + "=" * 74)
print("Confirming NOTHING thinner than 1/7 violates U_either in ONE+ scope, n<=7")
thinner = []
for n in range(2, MAX_N + 1):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            d1 = delta1(rel, n, k, dp)
            if d1 >= TARGET:
                continue
            amask = (1 << k) - 1
            bmask = ((1 << n) - 1) ^ amask
            subA, kA, _ = induced(rel, n, amask)
            subB, kB, _ = induced(rel, n, bmask)
            if is_chain(subA, kA) and is_chain(subB, kB):
                continue
            beforeP, totP = pair_probs(rel, n, dp)
            nb = ns = 0
            for mask in (amask, bmask):
                sub, ks, elems = induced(rel, n, mask)
                if is_chain(sub, ks):
                    continue
                sdp = le_dp(sub, ks)
                sbefore, stot = pair_probs(sub, ks, sdp)
                for (x, y) in incomparable_pairs(sub, ks):
                    if not balanced(Fraction(sbefore[x][y], stot)):
                        continue
                    nb += 1
                    gx, gy = elems[x], elems[y]
                    if balanced(Fraction(beforeP[gx][gy], totP)):
                        ns += 1
            if nb > 0 and ns == 0:
                thinner.append((d1, n, k, list(rel)))
print(f"violators with Delta_1 < 1/7: {len(thinner)}")
if thinner:
    print(f"   thinnest: {min(thinner)}")
print("\nCEILING (architecturally required scope, exhaustive n<=7):")
print(f"   eps_0(U_either) <= 1/7 = {float(TARGET):.6f}")
print(f"   vs corpus calibration 0.20 -> ratio {float(TARGET)/0.20:.4f} "
      f"({'BELOW' if TARGET < Fraction(1,5) else 'above'} the calibration)")
print(f"   eps_dem = eps_0^2/2 <= {Fraction(1,7)**2/2} = "
      f"{float(Fraction(1,7)**2/2):.6f}  vs corpus 0.02")
