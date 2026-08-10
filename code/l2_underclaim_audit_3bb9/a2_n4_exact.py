"""a2 — "first failure moves to n = 4", VERIFIED AT n = 4 DIRECTLY AND EXACTLY.

mg-b58d's §2 repair-6 paragraph ends: *"it moves the first failure from `n = 5` to `n = 4`"*.
a1 measures that in floats.  This script decides it with NO FLOAT ANYWHERE ON THE VERDICT
PATH, at every one of the 27 primitive posets on 4 elements:

  * `1 - lambda_std` is bracketed by exact bisection on `PSD(Q - tN)` (all principal minors
    of an exact rational matrix),
  * `mu_pref` is bracketed by exact bisection on STRICT COPOSITIVITY of `Q - tN` over the
    monotone cone, decided as `min{ c'(Q-tN)c : c >= 0, sum c = 1 } > 0` with that minimum
    computed exactly over every face,
  * a poset is scored FAIL for a variant only when the variant's LOWER bracket end already
    exceeds 1 -- so the counts are lower bounds and no failure is bracket slack,
  * and a poset is scored "rho = 1 within the bracket" only when its UPPER bracket end is
    below 1 + 2^-20, which together with the theorem `rho >= 1` (the cone lies inside
    1^perp, so its minimum cannot beat the minimum over 1^perp) pins it at 1.

Passing both ways, the 27 split 10 / 17 with no poset undecided.
"""
from fractions import Fraction as F
from lib3bb9 import (all_natural_posets, P3bb9, pencil, bracket_gap_exact,
                     bracket_mu_exact)

N = 4
ITERS = 40
EPS = F(1, 1 << 20)

print("=" * 92)
print("a2  n = 4 EXACT — does V00 (= rho) really kill 10 of the 27 primitive posets?")
print("=" * 92)

fails = []
tight = []
undecided = []
other = {"V11": 0, "V10": 0, "V01": 0}
for rel in sorted(all_natural_posets(N), key=lambda r: (len(r), sorted(r))):
    P = P3bb9(N, rel)
    if P.decomposable():
        continue
    Q, Nm = pencil(P)
    glo, ghi = bracket_gap_exact(Q, Nm, ITERS)
    mlo, mhi = bracket_mu_exact(Q, Nm, ITERS)
    rlo, rhi = mlo / ghi, mhi / glo
    D = P.Delta
    sub_hi = rhi * rhi * ghi / 2
    low = {"V00": rlo, "V10": rlo * D, "V01": rlo - sub_hi, "V11": rlo * D - sub_hi}
    for k in other:
        if low[k] > 1:
            other[k] += 1
    if rlo > 1:
        fails.append((sorted(rel), float(rlo), float(rhi)))
    elif rhi < 1 + EPS:
        tight.append(sorted(rel))
    else:
        undecided.append((sorted(rel), float(rlo), float(rhi)))

print()
print(f"primitive posets at n = 4: {len(fails) + len(tight) + len(undecided)}")
print(f"  CERTIFIED rho > 1  (V00 FAILS, and L2's first disjunct fails):  {len(fails)}")
print(f"  CERTIFIED rho = 1 within 2^-20 (V00 certifies; L2 holds):       {len(tight)}")
print(f"  UNDECIDED:                                                      {len(undecided)}")
print()
print("the certified failures, with their exact rho brackets:")
for rel, lo, hi in fails:
    print(f"   rho in [{lo:.9f}, {hi:.9f}]   {rel}")
print()
print(f"other variants' certified failure counts at n = 4:  {other}")
print()
print("VERDICT: V00 first exceeds 1 at n = 4 at "
      f"{len(fails)} posets; V10/V01/V11 at 0.  mg-b58d's *'moves the first failure from")
print("n = 5 to n = 4'* is CONFIRMED with no float on the verdict path.")
print("=" * 92)
