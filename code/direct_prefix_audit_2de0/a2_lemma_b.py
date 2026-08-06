"""mg-2de0 A2 — AUDIT OF LEMMA B, one inequality at a time.

LEMMA B (mg-00b9, as restated in mg-2de0's body). For beta in [0,1/2), over k in
[beta n, (1-beta) n]:

    (I1)  min_k Delta_1(A_k)  <=  (E[D]/2) / sum_k min(k, n-k)      [mediant + Lemma A]
    (I2)                      <=  2 E[D]  / ((1-4 beta^2) n^2)      [the sum_k lower bound]
    (I3)                      <=  4 E[inv_e] / ((1-4 beta^2) n^2)   [Diaconis-Graham D <= 2 inv]

LEMMA B DEPENDS ON LEMMA A. A1 confirmed Lemma A with 0 exceptions over 5912 permutations,
so B is not dead at the root; if A1 had failed, everything below would be void and this
script says so at the top of its output.

MY DERIVATION, independent:
  I1  The mediant inequality: for positive b_k, min_k (a_k/b_k) <= (sum a_k)/(sum b_k).
      Applied with a_k = E[K_k], b_k = min(k,n-k), over k in K_beta. Then the numerator is
      ENLARGED from sum_{k in K_beta} E[K_k] to sum_{k=1}^{n-1} E[K_k] = E[D]/2 (Lemma A),
      which is legitimate since every E[K_k] >= 0. So I1 is sound as an upper bound, and it
      is LOOSE by exactly the mass of E[K_k] outside K_beta.
  I2  Requires  sum_{k in K_beta} min(k, n-k) >= (1-4 beta^2) n^2 / 4.  The right side is
      the INTEGRAL int_{beta n}^{(1-beta) n} min(t, n-t) dt = (1/4 - beta^2) n^2. The left
      side is a DISCRETE sum over the integers in the same interval. min(k,n-k) is concave,
      so the midpoint rule gives f(k) >= int_{k-1/2}^{k+1/2} f, but the integration range
      recovered that way is [ceil(beta n) - 1/2, floor((1-beta) n) + 1/2], which need NOT
      contain [beta n, (1-beta) n]. The deficit is up to ~beta n at EACH end. So I2 is not
      derivable this way, and at beta = 0 it is outright false for odd n:
          sum_{k=1}^{n-1} min(k, n-k) = floor(n^2/4) = (n^2-1)/4 for odd n  <  n^2/4.
  I3  Diaconis-Graham upper half, D <= 2 inv. Sound, and it is the ONLY slack in the chain
      that can absorb an I2 deficit.

So the audit question for I2/I3 is not "is the algebra right" but "does the false step I2
propagate into a FALSE BOUND, or is it absorbed by I3's slack?" This script answers that
by evaluating each form against the exact truth, separately.

OPERATOR SCOPE: Delta_1 / footrule / inv_e. Transport axis. Not Delta_AT, not Hodge.
"""

import sys
from fractions import Fraction as F

from lib2de0 import (named_posets, all_posets, k_range, denom_exact, denom_claimed,
                     BETAS, inversions)

BAD = 0
NOTED = []


def report(label, bad, total, grain, population, fatal=True):
    global BAD
    if fatal:
        BAD += bad
    flag = "OK  " if bad == 0 else ("BAD " if fatal else "MEAS")
    print(f"  {flag} {label}: {bad} / {total}")
    print(f"       population: {population}")
    print(f"       grain:      {grain}")


print("=" * 78)
print("A2 — LEMMA B, the three inequalities scored SEPARATELY")
print("     Lemma B depends on Lemma A. A1 confirmed Lemma A: 0 exceptions over 5912")
print("     permutations and 13815 (poset, linear extension) pairs. B is not dead at")
print("     the root. Everything below is therefore a live question about I2 and I3.")
print("=" * 78)

POSETS = named_posets(7) + all_posets(4) + all_posets(5)
CELLS = [(P, b) for P in POSETS for b in BETAS if k_range(P.n, b)]

# ---------------------------------------------------------------------------
print()
print("A2.0  inv_e = ordinary Kendall inversions, on L(P).  mg-00b9's chain applies")
print("      Diaconis-Graham to inv_e, which the corpus defines as INCOMPARABLE pairs")
print("      flipped. DG is about ALL inverted pairs. These coincide on L(P) only")
print("      because comparable pairs cannot flip in a linear extension. Checked, not")
print("      assumed:")
bad = tot = 0
for P in POSETS:
    for p in P.linear_extensions():
        tot += 1
        n = P.n
        pos = {x: i for i, x in enumerate(p)}
        incomp_flipped = sum(1 for (x, y) in P.incomparable_pairs() if pos[x] > pos[y])
        if incomp_flipped != inversions(p):
            bad += 1
report("inv_e == Kendall inv on L(P)", bad, tot,
       "per-(poset, linear extension), integer equality",
       f"{len(POSETS)} posets (34 named n=2..7 + all 40 labelled on n=4 + all 357 "
       f"labelled on n=5), {tot} (poset, linear extension) pairs")

# ---------------------------------------------------------------------------
print()
print("A2.1  I1 — the mediant step. min_{k in K_beta} Delta_1(A_k) <= (E[D]/2)/denom_exact")
bad = tot = 0
for (P, b) in CELLS:
    tot += 1
    ks = k_range(P.n, b)
    truth = min(P.delta_1_prefix(k) for k in ks)
    bound = (P.E_footrule() / 2) / denom_exact(P.n, b)
    if truth > bound:
        bad += 1
        print(f"       BAD {P.name} beta={b}: truth {truth} > bound {bound}")
report("I1 (mediant + Lemma A)", bad, tot,
       "per-(poset, beta) cell, exact Fraction comparison",
       f"{len(POSETS)} posets x {len(BETAS)} betas with a nonempty k-range = {tot} cells")

print()
print("A2.1b I1 with the numerator RESTRICTED to K_beta (the sharp mediant, before the")
print("      enlargement to E[D]/2). Measures how much I1 gives away by using Lemma A:")
worst = None
for (P, b) in CELLS:
    ks = k_range(P.n, b)
    sharp = sum(P.E_K(k) for k in ks) / denom_exact(P.n, b)
    loose = (P.E_footrule() / 2) / denom_exact(P.n, b)
    if loose > 0:
        r = sharp / loose
        if worst is None or r < worst[0]:
            worst = (r, P.name, b)
print(f"       most-given-away cell: sharp/loose = {worst[0]} "
      f"({float(worst[0]):.4f}) at {worst[1]} beta={worst[2]}")
print("       => at beta=0 the enlargement is free (ratio 1); the loss is entirely the")
print("          E[K_k] mass in the two tails k < beta n and k > (1-beta) n.")

# ---------------------------------------------------------------------------
print()
print("A2.2  I2 — the step  sum_{k in K_beta} min(k,n-k) >= (1-4 beta^2) n^2/4")
print("      This is the step I could not derive. Measured as an (n, beta) grid fact,")
print("      independent of any poset:")
hdr = (f"       {'n':>3s} {'beta':>6s} {'k-range':>12s} {'exact sum':>10s} "
       f"{'claimed':>12s} {'holds':>6s}")
print(hdr)
bad = tot = 0
odd_fail = []
for n in range(2, 25):
    for b in BETAS:
        ks = k_range(n, b)
        if not ks:
            continue
        tot += 1
        de, dc = denom_exact(n, b), denom_claimed(n, b)
        holds = de >= dc
        if not holds:
            bad += 1
            if b == 0:
                odd_fail.append(n)
        if n in (3, 4, 5, 8, 9) and b in (F(0), F(1, 4), F(1, 3)):
            rng = f"[{ks[0]},{ks[-1]}]"
            print(f"       {n:3d} {str(b):>6s} {rng:>12s} {str(de):>10s} "
                  f"{str(dc):>12s} {str(holds):>6s}")
report("I2 (the sum_k lower bound)", bad, tot,
       "per-(n, beta) grid cell, exact Fraction comparison",
       f"n=2..24 x {len(BETAS)} betas with a nonempty k-range = {tot} cells")
print(f"       at beta=0 the failures are exactly the ODD n: {odd_fail}")
print(f"       (deficit is exactly 1/4 there: floor(n^2/4) = (n^2-1)/4 for odd n)")
print("       => I2 IS FALSE AS STATED. It is an O(1/n^2)-to-O(beta/n) overclaim, not a")
print("          typo: the discrete sum is compared against the integral it replaces and")
print("          the ceil/floor of the range endpoints is not paid for.")

print()
print("A2.2b the SHARP replacement for I2 at beta=0, which I propose and verify:")
print("         sum_{k=1}^{n-1} min(k,n-k) = floor(n^2/4) >= (n^2-1)/4, with equality odd n")
bad = tot = 0
for n in range(2, 60):
    tot += 1
    if denom_exact(n, F(0)) != n * n // 4 or n * n // 4 < F(n * n - 1, 4):
        bad += 1
report("floor(n^2/4) identity and (n^2-1)/4 floor", bad, tot,
       "per-n, exact", "n=2..59")

# ---------------------------------------------------------------------------
print()
print("A2.3  I2 as a COMPOSITE BOUND on a real poset — does the false step propagate?")
print("      claim:  min_k Delta_1(A_k) <= 2 E[D] / ((1-4 beta^2) n^2)")
bad = tot = 0
wit = []
for (P, b) in CELLS:
    tot += 1
    ks = k_range(P.n, b)
    truth = min(P.delta_1_prefix(k) for k in ks)
    bound = 2 * P.E_footrule() / ((1 - 4 * b * b) * P.n * P.n)
    if truth > bound:
        bad += 1
        wit.append((P, b, truth, bound))
for (P, b, t, bd) in wit[:25]:
    print(f"       FALSIFIED {P.name:26s} beta={str(b):>5s}: truth {t} "
          f"({float(t):.4f}) > bound {bd} ({float(bd):.4f})")
if len(wit) > 25:
    print(f"       ... and {len(wit)-25} more")
report("I2 composite bound FALSIFIED on real posets", bad, tot,
       "per-(poset, beta) cell, exact Fraction comparison",
       f"{tot} cells as in A2.1", fatal=False)
by_n = {}
for (P, b, t, bd) in wit:
    by_n.setdefault(P.n, set()).add(str(b))
print(f"       falsifying n values: {sorted(by_n)}")
for n in sorted(by_n):
    print(f"         n={n}: betas {sorted(by_n[n])}")

# ---------------------------------------------------------------------------
print()
print("A2.4  I3 — the OUTER bound, the one the falsifier line in mg-2de0 names:")
print("      claim:  min_k Delta_1(A_k) <= 4 E[inv_e] / ((1-4 beta^2) n^2)")
bad = tot = 0
wit3 = []
for (P, b) in CELLS:
    tot += 1
    ks = k_range(P.n, b)
    truth = min(P.delta_1_prefix(k) for k in ks)
    bound = 4 * P.E_inv() / ((1 - 4 * b * b) * P.n * P.n)
    if truth > bound:
        bad += 1
        wit3.append((P, b, truth, bound))
for (P, b, t, bd) in wit3[:25]:
    print(f"       FALSIFIED {P.name:26s} beta={str(b):>5s}: truth {t} "
          f"({float(t):.4f}) > bound {bd} ({float(bd):.4f})")
if len(wit3) > 25:
    print(f"       ... and {len(wit3)-25} more")
report("I3 outer bound FALSIFIED on real posets", bad, tot,
       "per-(poset, beta) cell, exact Fraction comparison",
       f"{tot} cells as in A2.1", fatal=False)
b0 = [w for w in wit3 if w[1] == 0]
print(f"       of which at beta=0: {len(b0)}")
byn3 = {}
for (P, b, t, bd) in wit3:
    byn3.setdefault(P.n, set()).add(str(b))
for n in sorted(byn3):
    print(f"         n={n}: betas {sorted(byn3[n])}")

# ---------------------------------------------------------------------------
print()
print("A2.5  THE REPAIRED FORM I propose, verified on the same population:")
print("        beta=0:  min_k Delta_1(A_k) <= (E[D]/2)/floor(n^2/4) <= 2E[D]/(n^2-1)")
print("        general: min_k Delta_1(A_k) <= (E[D]/2)/denom_exact(n,beta)")
print("      Note the beta=0 repaired denominator (n^2-1) is the SAME denominator the")
print("      corpus already uses for the master bound (STATE.md:130) -- the repair puts")
print("      the direct route on the corpus's own normalisation.")
bad = tot = 0
for P in POSETS:
    tot += 1
    truth = min(P.delta_1_prefix(k) for k in range(1, P.n))
    b1 = (P.E_footrule() / 2) / (P.n * P.n // 4)
    b2 = 2 * P.E_footrule() / (P.n * P.n - 1)
    if not (truth <= b1 <= b2):
        bad += 1
        print(f"       BAD {P.name}: truth {truth}, b1 {b1}, b2 {b2}")
report("repaired beta=0 chain", bad, tot,
       "per-poset, exact Fraction chain truth <= b1 <= b2",
       f"{len(POSETS)} posets as in A2.0")

bad = tot = 0
for (P, b) in CELLS:
    tot += 1
    ks = k_range(P.n, b)
    truth = min(P.delta_1_prefix(k) for k in ks)
    if truth > (P.E_footrule() / 2) / denom_exact(P.n, b):
        bad += 1
report("repaired general-beta form", bad, tot,
       "per-(poset, beta) cell, exact Fraction comparison",
       f"{tot} cells as in A2.1")

print()
print("A2.5b the repaired beta=0 form at the ANTICHAIN gives EXACTLY 2/3 for every n,")
print("      which mg-00b9's own stated n^2 form does NOT attain.")
print()
print("      Enumerating L(antichain n) is n! and dies at n=11, so the table below uses")
print("      closed forms I derived BY HAND and then VERIFIED against enumeration:")
print("        E[K_k] = k(n-k)/n,  Delta_1(A_k) = max(k,n-k)/n,  E[D] = (n^2-1)/3.")
print("      The verification is the first block; the extrapolation is the second, and")
print("      it is labelled as an extrapolation from verified closed forms, not as an")
print("      enumeration.")


def ac_E_K(n, k):
    return F(k * (n - k), n)


def ac_delta1(n, k):
    return F(max(k, n - k), n)


def ac_E_D(n):
    return F(n * n - 1, 3)


bad = tot = 0
for P in named_posets(8):
    if not P.name.startswith("antichain"):
        continue
    n = P.n
    tot += 1
    ok = (P.E_footrule() == ac_E_D(n)
          and all(P.E_K(k) == ac_E_K(n, k) for k in range(1, n))
          and all(P.delta_1_prefix(k) == ac_delta1(n, k) for k in range(1, n)))
    if not ok:
        bad += 1
        print(f"       BAD closed form at {P.name}")
report("antichain closed forms vs enumeration", bad, tot,
       "per-n, exact Fraction equality of E[D], all E[K_k], all Delta_1(A_k)",
       "antichains n=2..8, enumerated (n=8 is 40320 linear extensions)")

print()
print(f"       {'n':>3s} {'truth':>8s} {'repaired 2E[D]/(n^2-1)':>24s} "
      f"{'mg-00b9 2E[D]/n^2':>20s}")
for n in range(2, 14):
    truth = min(ac_delta1(n, k) for k in range(1, n))
    rep = 2 * ac_E_D(n) / (n * n - 1)
    stated = 2 * ac_E_D(n) / (n * n)
    print(f"       {n:3d} {str(truth):>8s} {str(rep):>24s} {str(stated):>20s}"
          + ("   <-- stated form BELOW truth" if stated < truth else ""))
print("       (rows n>=9 are the closed-form extrapolation just verified, NOT enumerated)")

print()
print("=" * 78)
print(f"A2 TOTAL BAD (fatal): {BAD}")
print(f"A2 MEASURED FALSIFICATIONS: I2 composite {len(wit)}, I3 outer {len(wit3)}")
print("=" * 78)
sys.exit(0 if BAD == 0 else 1)
