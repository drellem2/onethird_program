#!/usr/bin/env python3
"""mg-7564 d0 — SELFTEST.  A GATE: d1 and d2 do not run unless this passes.

Every control below has a LIVE NEGATIVE ARM: a deliberately wrong world in which the
control must fire.  A control with no negative arm is a control that cannot be shown to
discriminate, which is the defect `mg-d2c2` found in a sweep that declared it was
watching a number produced by an uncontrolled detector.
"""

import sys
from fractions import Fraction as F

import lib7564 as L

FAILS = []


def check(label, got, want):
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got}, want {want}")
    if not ok:
        FAILS.append(label)


def check_raises(label, fn, exc):
    try:
        fn()
    except exc as e:
        print(f"  [PASS] {label}: raised as designed — {e}")
        return
    except Exception as e:  # noqa: BLE001
        print(f"  [FAIL] {label}: raised the WRONG thing — {type(e).__name__}: {e}")
        FAILS.append(label)
        return
    print(f"  [FAIL] {label}: did NOT raise")
    FAILS.append(label)


print("=" * 78)
print("mg-7564 d0 — SELFTEST")
print("=" * 78)

# ---------------------------------------------------------------------------
print("\nA. PLUG-BACK — eps_dem solved from a chain must saturate that chain's own bound.")
print("   Phi(eps_dem) must equal eps_leak EXACTLY, and must EXCEED it above.")
print("   The bump is (101/100)^2 and not (101/100), for a stated reason: on the")
print("   square-root chains the smaller bump lands on an IRRATIONAL root, and")
print("   `_sqrt` refuses rather than floating it — the refusal is the C control")
print("   below working, so the bump is chosen to keep every arm exact.")
# ---------------------------------------------------------------------------
Lk = L.EPS_LEAK

for name, dem, phi, args in [
    ("(I)",             L.dem_I,   L.phi_I,   ()),
    ("(III) C=1",       L.dem_III, L.phi_III, (F(1),)),
    ("(III) C=2",       L.dem_III, L.phi_III, (F(2),)),
    ("(II)  g=3/2",     L.dem_II,  L.phi_II,  (F(3, 2),)),
    ("(II)  g=10",      L.dem_II,  L.phi_II,  (F(10),)),
    ("(IV)  c=1",       L.dem_IV,  L.phi_IV,  (F(1),)),
    ("(IV)  c=40/49",   L.dem_IV,  L.phi_IV,  (F(40, 49),)),
    ("(IV)  c=9/10",    L.dem_IV,  L.phi_IV,  (F(9, 10),)),
]:
    e = dem(Lk, *args)
    check(f"{name} saturates", phi(e, *args), Lk.v)
    above = L.Spec(e.v * F(101, 100) ** 2)
    worse = phi(above, *args) > Lk.v
    check(f"{name} strictly worse above", worse, True)

print("\n   NEGATIVE ARM — a chain (IV) mis-derived to pay a Cheeger square must NOT saturate.")


def dem_IV_wrong(eps_leak, c):
    return L.Spec((1 - (1 - eps_leak.v) / F(c)) ** 2 / 2)


bad = dem_IV_wrong(Lk, F(9, 10))
check("mis-derived (IV) fails plug-back", L.phi_IV(bad, F(9, 10)) == Lk.v, False)

# ---------------------------------------------------------------------------
print("\nB. TYPE GUARD — a Spec where a Leak belongs must RAISE.")
# ---------------------------------------------------------------------------
check_raises("dem_I(Spec)", lambda: L.dem_I(L.Spec(F(1, 5))), L.TypeGuard)
check_raises("phi_II(Leak)", lambda: L.phi_II(L.Leak(F(1, 50)), F(2)), L.TypeGuard)
print("   NEGATIVE ARM — the correctly typed call must NOT raise:")
check("dem_I(Leak) works", L.dem_I(L.Leak(F(1, 5))).v, F(1, 50))

# ---------------------------------------------------------------------------
print("\nC. NO FLOAT ON A DECISION PATH — an irrational root must REFUSE, not round.")
# ---------------------------------------------------------------------------
check_raises("sqrt(3) refuses", lambda: L._sqrt(F(3)), ValueError)
check("sqrt(4/25) is exact", L._sqrt(F(4, 25)), F(2, 5))

# ---------------------------------------------------------------------------
print("\nD. CURRENCY JOIN — dq_from_spec and spec_from_dq must invert, at every n.")
# ---------------------------------------------------------------------------
for n in [None, 3, 6, 12, 25, 400]:
    e = L.Spec(F(1, 50))
    dq = L.dq_from_spec(e, n)
    check(f"round-trip at n={n}", L.spec_from_dq(dq, n).v, e.v)

print("   NEGATIVE ARM — dropping the n/(n+1) factor must BREAK the round trip at finite n:")
bad_dq = L.Spec(F(1, 50)).v / 3
check("wrong join fails at n=6", L.spec_from_dq(bad_dq, 6).v == F(1, 50), False)
check("wrong join HAPPENS to pass in the limit", L.spec_from_dq(bad_dq, None).v, F(1, 50))

# ---------------------------------------------------------------------------
print("\nE. THE 10x IS EXACTLY 2/eps_leak, AT EVERY C3 — C3 cancels.")
print("   (II)/(III) = (L/C) / (L^2/(2C)) = 2/L.  A ratio that MOVES with C3 is a bug.")
# ---------------------------------------------------------------------------
for c3 in [F(1), F(3, 2), F(7, 3), F(10), F(1000)]:
    r = L.dem_II(Lk, c3).v / L.dem_III(Lk, c3).v
    check(f"ratio at C3={c3}", r, 2 / Lk.v)

# ---------------------------------------------------------------------------
print("\nF. THE WALL — eps_sup/eps_dem, and chain (II)'s closed form 5*C3^gap.")
# ---------------------------------------------------------------------------
for g in [F(1), F(2), F(5), F(10)]:
    check(f"wall(II) at C3^gap={g}", L.wall(L.dem_II(Lk, g)), 5 * g)
check("chain (II) meets chain (III) at C3^gap = 10",
      L.dem_II(Lk, F(10)).v, L.dem_III(Lk, F(1)).v)

# ---------------------------------------------------------------------------
print("\n" + "=" * 78)
if FAILS:
    print(f"d0 RED — {len(FAILS)} control(s) failed: {FAILS}")
    print("=" * 78)
    sys.exit(1)
print("d0 GREEN — every control passed and every negative arm fired.")
print("=" * 78)
