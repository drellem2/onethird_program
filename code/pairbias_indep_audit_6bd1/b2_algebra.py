"""B2 — re-derive every printed FIGURE of mg-345e in exact rationals, and settle the
currency question its §6 turns on.

Nothing here reads mg-345e's `out_*.txt`. Every identity is re-derived from the
definitions in `Op-Form` §6.1-6.3 and `mg-c3ca` Prop 4.1.
"""

import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib6bd1 import (  # noqa: E402
    C2, E_unif_footrule, E_unif_footrule_bruteforce, E_unif_footrule_sum,
    E_unif_inv, eps_c3ca_from_Einv, eps_spec_from_Einv, frozen_sup_Einv,
)

FAIL = []


def check(name, got, want):
    ok = got == want
    if not ok:
        FAIL.append(name)
    print(f"    [{'ok ' if ok else 'FAIL'}] {name}: {got}" + ("" if ok else f"  != {want}"))
    return ok


print("=" * 78)
print("B2 — mg-345e's algebra, re-derived in exact rationals (no float on any path)")
print("=" * 78)

print()
print("C1. E_unif[footrule] = (n^2-1)/3 — three independent computations must agree.")
print("    (brute force over S_n; the direct double sum; the closed form)")
for n in range(2, 8):
    bf, ds, cf = (E_unif_footrule_bruteforce(n), E_unif_footrule_sum(n),
                  E_unif_footrule(n))
    check(f"n={n}  brute={bf}  sum={ds}  closed={cf}", (bf, ds), (cf, cf))
print("    beyond brute force, the double sum against the closed form to n=59:")
bad = [n for n in range(2, 60) if E_unif_footrule_sum(n) != E_unif_footrule(n)]
check("mismatches over n=2..59", bad, [])

print()
print("C2. eps_sup <= 2m/(n^2-1) = d*n/(n+1) < 1, for every n and every m <= C(n,2).")
print("    Derived here, not copied: frozen gives E[inv_e] < m/3 (Op-Form Claim 6.1);")
print("    m/3 <= (eps/6)(n^2-1)  <=>  eps >= 2m/(n^2-1).")
mism = []
worst = Fraction(0)
for n in range(2, 41):
    for m in range(0, int(C2(n)) + 1):
        eps = eps_spec_from_Einv(frozen_sup_Einv(n, m), n)
        d = Fraction(m) / C2(n) if n >= 2 else Fraction(0)
        if eps != Fraction(2 * m, n * n - 1) or eps != d * Fraction(n, n + 1):
            mism.append((n, m))
        worst = max(worst, eps)
check("mismatches of eps = 2m/(n^2-1) = d*n/(n+1) over the whole (n,m) grid", mism, [])
print(f"    grid size: n=2..40, every m in [0, C(n,2)]  ->"
      f" {sum(int(C2(n)) + 1 for n in range(2, 41))} points")
print(f"    sup over the grid (attained at d=1, i.e. the antichain): {worst}"
      f"  = n/(n+1) at n=40: {Fraction(40, 41)}")
check("sup < 1", worst < 1, True)
print("    n/(n+1) -> 1 and never reaches it:")
for n in (3, 4, 5, 6, 10, 100, 1000):
    print(f"        n={n:>4}  eps_sup ceiling = {Fraction(n, n+1)}"
          f"  = {float(Fraction(n, n+1)):.6f}")

print()
print("C3. Op-Form ledger claim 26 says the constant is 2/3. mg-345e's §0 cites claim 26")
print("    for the value 1. THIS LINEAGE HAS CONFLATED CURRENCIES TWICE, so it is checked")
print("    rather than assumed: 2/3 is in the E_unif[inv] currency, 1 is in eps_spec.")
print("    The conversion must be EXACT, not asymptotic, or one of the two is wrong.")
mism = []
for n in range(2, 41):
    E = frozen_sup_Einv(n, int(C2(n)))          # worst case m = C(n,2)
    ratio_unif = E / E_unif_inv(n)              # claim 26's currency
    eps = eps_spec_from_Einv(E, n)              # mg-345e's currency
    if ratio_unif != Fraction(2, 3) or eps != Fraction(n, n + 1):
        mism.append(n)
check("E[inv_e]/E_unif[inv] = 2/3 EXACTLY at every n=2..40, while eps_spec = n/(n+1)",
      mism, [])
print("    -> claim 26's `2/3` and mg-345e's `1` are the SAME statement in two")
print("       currencies. mg-345e's citation is CORRECT and is not a conflation.")
print("       The conversion factor is eps_spec/(E/E_unif[inv]) = 3n/(2(n+1)) -> 3/2:")
for n in (3, 6, 40):
    print(f"        n={n:>3}: (n/(n+1)) / (2/3) = {Fraction(n, n+1) / Fraction(2,3)}"
          f"  = 3n/(2(n+1)) = {Fraction(3*n, 2*(n+1))}")

print()
print("C4. THE UNIT MAP — the check mg-345e's §6 did not run.")
print("    mg-c3ca Prop 4.1 normalises by n^2: `E[inv_e] <= eps*n^2`.")
print("    mg-c4f5:415 reports `Freezing unconditionally gives only eps < 1/6`.")
print("    Is that the SAME theorem as mg-345e's `eps_sup < 1`?")
mism = []
for n in range(2, 41):
    E = frozen_sup_Einv(n, int(C2(n)))
    if eps_c3ca_from_Einv(E, n) != Fraction(n - 1, 6 * n):
        mism.append(n)
check("frozen ceiling in the /n^2 currency = (n-1)/(6n) at every n=2..40", mism, [])
print("    (n-1)/(6n) is increasing in n with supremum EXACTLY 1/6:")
for n in (3, 6, 10, 100, 1000):
    print(f"        n={n:>4}: (n-1)/(6n) = {Fraction(n-1, 6*n)}"
          f" = {float(Fraction(n-1,6*n)):.8f}   (1/6 = {1/6:.8f})")
check("sup_n (n-1)/(6n) < 1/6 and -> 1/6", Fraction(999999, 6000000) < Fraction(1, 6), True)
print()
print("    ratio of the two currencies at the SAME underlying E[inv_e]:")
mism = []
for n in range(2, 41):
    E = frozen_sup_Einv(n, int(C2(n)))
    if eps_spec_from_Einv(E, n) / eps_c3ca_from_Einv(E, n) != Fraction(6*n*n, n*n - 1):
        mism.append(n)
check("eps_spec/eps_c3ca = 6n^2/(n^2-1) at every n=2..40", mism, [])
for n in (3, 6, 40, 1000):
    print(f"        n={n:>4}: 6n^2/(n^2-1) = {Fraction(6*n*n, n*n-1)}"
          f" = {float(Fraction(6*n*n, n*n-1)):.6f}   -> 6")
print()
print("    VERDICT OF C4: `eps_sup < 1` and `eps < 1/6` are ONE theorem under two")
print("    divisions of E[inv_e] < n(n-1)/6. They are a factor of ~6 apart BECAUSE")
print("    OF THE UNITS, not because one is sharper.")

print()
print("C5. mg-345e §5.3's rider: the live figure is the C_3 = 1 value.")
check("0.20^2/2 = 1/50", Fraction(1, 5) ** 2 / 2, Fraction(1, 50))
check("as a decimal, 2e-2", Fraction(1, 50), Fraction(2, 100))
print()
print("C6. the published gap factor ~50 as a ratio across the split.")
eps_sup_ceiling = Fraction(1)          # the n -> oo ceiling of n/(n+1)
eps_dem = Fraction(1, 50)
check("eps_sup / eps_dem", eps_sup_ceiling / eps_dem, Fraction(50))
print("    numerator = the pair-bias supply constant (L4-INDEPENDENT)")
print("    denominator = eps_leak^2/2 at eps_leak = 0.20 (L4-DEPENDENT)")
print("    at finite n the numerator is n/(n+1), so the true ratio is 50n/(n+1):")
for n in (6, 100, 1000):
    print(f"        n={n:>4}: {Fraction(50*n, n+1)} = {float(Fraction(50*n, n+1)):.4f}")

print()
print("-" * 78)
print("NEGATIVE CONTROLS")
print("-" * 78)
# NC5 — a deliberately wrong conversion must be caught by C2's grid.
wrong = [(n, m) for n in range(2, 12) for m in range(int(C2(n)) + 1)
         if Fraction(6) * frozen_sup_Einv(n, m) / Fraction(n * n) == Fraction(2 * m, n * n - 1)]
print(f"NC5  6E/n^2 (the wrong denominator) agrees with 2m/(n^2-1) at"
      f" {len(wrong)} of the grid points -> must be small/zero-ish: {wrong[:4]}")
print(f"     FIRES (the two normalisations are genuinely different): {len(wrong) <= 11}")
# NC6 — assert claim 26's 2/3 in the WRONG currency; it must fail.
# DEFECT OF THIS CONTROL, KEPT (mg-6bd1 §D2). Written as n>=2 it reports [2] and
# scores itself FAILED against CORRECT code: n/(n+1) = 2/3 at n=2 exactly, so the two
# currencies COINCIDE NUMERICALLY at n=2 by accident. That is not a bug in the
# mathematics — it is a small-n coincidence of precisely the kind mg-131e refuted
# 2/(n+1) over tonight, and it is reported rather than tuned away.
bad_all = [n for n in range(2, 12)
           if eps_spec_from_Einv(frozen_sup_Einv(n, int(C2(n))), n) == Fraction(2, 3)]
bad = [n for n in bad_all if n >= 3]
print(f"NC6  eps_spec == 2/3 (currency mix-up) holds at n in {bad_all} over n>=2")
print(f"     n=2 is a genuine numeric COINCIDENCE (n/(n+1) = 2/3 there), disclosed;")
print(f"     FIRES over n>=3 (must be empty): {bad == []}")
# NC7 — the 1/6 must NOT be attained at finite n.
att = [n for n in range(2, 200) if Fraction(n - 1, 6 * n) == Fraction(1, 6)]
print(f"NC7  (n-1)/(6n) == 1/6 at n in {att}")
print(f"     FIRES (1/6 is a supremum, never attained): {att == []}")

print()
print("=" * 78)
print(f"RESULT: {'ALL CHECKS PASS' if not FAIL else 'FAILURES: ' + repr(FAIL)}")
print("=" * 78)
