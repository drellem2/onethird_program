"""a2_dictionary -- re-derive mg-76b2's Lemmas 2.1, 3.1, 3.2, 3.3 FROM THE SOURCE.

The ticket says: re-derive from the source rather than checking its steps,
because a step-check inherits a wrong framing.  So every identity below is
stated in the form I derived it in, then checked two ways where two ways exist:
once from the MATRIX (T_P, built from the tex's R(sigma) e_a = e_{sigma(a)})
and once from the DEFINITION (counting |A \\ sigma(A)| over linear extensions).
Agreement of the two is the load-bearing check -- a single path could be wrong
in the same way twice.

Scores PREDICTIONS.md P1, P2, P3.
"""

from fractions import Fraction as F
import math
from libA94 import (all_posets, linear_extensions, T_matrix, is_primitive,
                    spectral_gap, monotone_dominant, threshold_sets,
                    is_prefix_or_suffix, jacobi_eig, laplacian, banner)

NS = [2, 3, 4, 5, 6]
rc = 0


def leak_from_matrix(n, T, A):
    """E|A \\ sigma(A)| = |A| - sum_{x in A} sum_{a in A} T[x][a].

    Derived, not copied: E|A cap sigma(A)| = sum_{x in A} Pr[x in sigma(A)]
    = sum_{x in A} sum_{a in A} Pr[sigma(a) = x]."""
    s = F(0)
    for x in A:
        row = T[x]
        for a in A:
            s += row[a]
    return len(A) - s


def leak_from_definition(n, exts, Amask):
    """E|A \\ sigma(A)| counted directly over L(P), bitmask arithmetic.
    sigma(A) = elements at the POSITIONS in A -- not `perm[:|A|]`."""
    tot = 0
    ka = bin(Amask).count("1")
    for perm in exts:
        img = 0
        m = Amask
        while m:
            b = m & -m
            img |= 1 << perm[b.bit_length() - 1]
            m ^= b
        tot += ka - bin(Amask & img).count("1")
    return F(tot, len(exts))


# --------------------------------------------------------------------------
banner("A. POPULATION -- enumerated independently, then compared to mg-76b2's count")
POP = {}
for n in NS:
    POP[n] = [(rel, linear_extensions(n, rel)) for rel in all_posets(n)]
    print(f"  n = {n}: {len(POP[n]):>5} posets, "
          f"{sum(len(e) for _, e in POP[n]):>7} linear extensions in total, "
          f"{sum(1 for r, _ in POP[n] if is_primitive(n, r)):>5} primitive")
tot = sum(len(POP[n]) for n in NS)
prim = sum(sum(1 for r, _ in POP[n] if is_primitive(n, r)) for n in NS)
print(f"\n  TOTAL {tot} posets ({prim} primitive).  mg-76b2 reports 5230 / 4377.")
print(f"  agree: {tot == 5230} / {prim == 4377}")
if (tot, prim) != (5230, 4377):
    rc = 1

# --------------------------------------------------------------------------
banner("B. THE SOURCE'S OWN IDENTITY (tex:220-227), MATRIX vs DEFINITION")
print("  <1_A,(I-S_P)1_A> = E|A \\ sigma(A)|, over EVERY cut of EVERY poset.\n")
pairs = bad = 0
for n in NS:
    for rel, exts in POP[n]:
        T = T_matrix(n, exts)
        for mask in range(1, (1 << n) - 1):
            A = [i for i in range(n) if mask >> i & 1]
            if leak_from_matrix(n, T, A) != leak_from_definition(n, exts, mask):
                bad += 1
            pairs += 1
    print(f"  n = {n}: cumulative {pairs:>7} (poset, cut) pairs, {bad} disagreements")
print(f"\n  {pairs} (poset, cut) pairs, {bad} disagreements.  "
      f"mg-76b2 reports 310404.  agree: {pairs == 310404}")
if bad or pairs != 310404:
    rc = 1

# --------------------------------------------------------------------------
banner("C. LEMMA 2.1 (the dictionary) -- P1")
print("""  Derived here, independently:  f = 1_{A_k} - (k/n)1 is centred, and
  (I-S_P)1 = 0, so <f,(I-S_P)f> = <1_A,(I-S_P)1_A> = E|A_k \\ sigma(A_k)|;
  ||f||^2 = k(1-k/n)^2 + (n-k)(k/n)^2 = k(n-k)/n.  Hence

      1 - rho(A_k) = n E|A_k \\ sigma(A_k)| / (k(n-k))
                   = n Phi_P(A_k) / max(k, n-k)

  with Phi_P(A_k) = Delta_1 = E|.| / min(k,n-k).  Since 1 <= n/max(k,n-k) <= 2,

      Phi <= 1 - rho <= 2 Phi        for EVERY k.
""")
npairs = f1 = f2 = f3 = attained = 0
for n in NS:
    for rel, exts in POP[n]:
        T = T_matrix(n, exts)
        for k in range(1, n):
            A = list(range(k))
            E = leak_from_matrix(n, T, A)
            phi = E / min(k, n - k)
            omr = F(n) * E / (k * (n - k))
            if omr != F(n) * phi / max(k, n - k):
                f1 += 1
            if not (phi <= omr):
                f2 += 1
            if not (omr <= 2 * phi):
                f3 += 1
            if omr == 2 * phi and phi != 0:
                attained += 1
            npairs += 1
print(f"  (poset, prefix) pairs        : {npairs}   (mg-76b2 reports 25684: "
      f"{npairs == 25684})")
print(f"  1-rho = n Phi / max(k,n-k)   : {f1} exceptions")
print(f"  Phi <= 1-rho                 : {f2} exceptions")
print(f"  1-rho <= 2 Phi               : {f3} exceptions")
print(f"  upper factor 2 attained      : {attained} times (k = n/2, Phi != 0)")
print(f"\n  P1: {'HELD' if (f1 or f2 or f3) == 0 else 'MISSED'}")
if f1 or f2 or f3 or npairs != 25684:
    rc = 1

# --------------------------------------------------------------------------
banner("D. LEMMA 3.2 -- Phi_P is a function of the CUT, not the side")
print("  |A \\ sigma(A)| = |A^c \\ sigma(A^c)| for every permutation and cut.\n")
perms = 0
ppairs = pbad = 0
for n in NS:
    from itertools import permutations as _perm
    for perm in _perm(range(n)):
        perms += 1
        for mask in range(1, (1 << n) - 1):
            cmask = ((1 << n) - 1) ^ mask
            for m in (mask, cmask):
                img = 0
                mm = m
                while mm:
                    b = mm & -mm
                    img |= 1 << perm[b.bit_length() - 1]
                    mm ^= b
                if m == mask:
                    a = bin(mask).count("1") - bin(mask & img).count("1")
                else:
                    b2 = bin(cmask).count("1") - bin(cmask & img).count("1")
            if a != b2:
                pbad += 1
            ppairs += 1
print(f"  {perms} permutations, {ppairs} (permutation, cut) pairs, {pbad} exceptions")
print(f"  mg-76b2 reports 872 permutations / 48616 pairs: "
      f"{perms == 872} / {ppairs == 48616}")
if pbad or ppairs != 48616:
    rc = 1

# --------------------------------------------------------------------------
banner("E. LEMMA 3.1's CONCLUSION (the Cheeger sweep) -- P2")
print("""  Not the proof -- the CONCLUSION, measured: does SOME level set S of a
  minimiser v, with 0 < |S| <= n/2, satisfy Phi_P(S) <= sqrt(2(1-lambda_std))?

  NOTE ON TIES.  Level sets are grouped by VALUE.  An order-slice of the sorted
  labels is NOT a level set, and the antichain (whose eigenvector ties
  everywhere) is where that distinction bites -- mg-76b2 records exactly this
  as a defect of its first sweep routine, and this routine avoids it by
  construction rather than by having been corrected.
""")
sweeps = swfail = degenerate = zero_gap = 0
worst = 0.0
for n in NS:
    for rel, exts in POP[n]:
        T = T_matrix(n, exts)
        gap, v, vals, vecs = spectral_gap(n, T)
        if gap < 1e-12:
            zero_gap += 1
            continue
        best = None
        for S in threshold_sets(v, n):
            E = leak_from_matrix(n, T, sorted(S))
            phi = float(E) / min(len(S), n - len(S))
            best = phi if best is None else min(best, phi)
        sweeps += 1
        if best is None or best > math.sqrt(2 * gap) + 1e-9:
            swfail += 1
        else:
            worst = max(worst, best * best / (2 * gap))
print(f"  posets with a positive gap swept : {sweeps}")
print(f"  posets with 1-lambda_std = 0     : {zero_gap}")
print(f"  sweeps failing Phi <= sqrt(2 gap): {swfail}")
print(f"  worst Phi^2/(2(1-lambda_std))    : {worst:.4f}")
print(f"\n  P2: {'HELD' if swfail == 0 else 'MISSED'}")
if swfail:
    rc = 1

# --------------------------------------------------------------------------
banner("F. LEMMA 3.3 -- monotone v ==> every level set is a prefix or a suffix -- P3")
mono = nonmono = undec = 0
lsets = lsbad = 0
nm_escape = 0
for n in NS:
    for rel, exts in POP[n]:
        T = T_matrix(n, exts)
        st = monotone_dominant(n, T)
        if st == "UNDECIDED":
            undec += 1
            continue
        gap, v, vals, vecs = spectral_gap(n, T)
        sets = threshold_sets(v, n)
        if st == "YES":
            mono += 1
            for S in sets:
                lsets += 1
                if not is_prefix_or_suffix(n, S):
                    lsbad += 1
        else:
            nonmono += 1
            if any(not is_prefix_or_suffix(n, S) for S in sets):
                nm_escape += 1
print(f"  monotone dominant eigenvector    : {mono}")
print(f"  non-monotone                     : {nonmono}")
print(f"  UNDECIDED (degenerate top space) : {undec}   [declared as B3]")
print(f"  level sets of monotone v         : {lsets}")
print(f"  ... not a prefix or a suffix     : {lsbad}")
print(f"  RED DRILL -- non-monotone posets whose level sets DO leave the")
print(f"  prefix family                    : {nm_escape} of {nonmono}")
print(f"\n  P3: {'HELD' if lsbad == 0 else 'MISSED'}")
print("  The red drill is what makes P3 non-vacuous: the hypothesis is doing")
print("  work, because without it the level sets genuinely do escape.")
if lsbad:
    rc = 1

banner("EXIT")
print(f"rc = {rc}")
raise SystemExit(rc)
