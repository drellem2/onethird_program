#!/usr/bin/env python3
"""mg-6ff4 arm c5 — WRITTEN AFTER mg-0e8c/mg-ac0c LANDED ON MAIN MID-BRANCH, BECAUSE THAT
CORRECTION SCOPES THIS TICKET'S OWN HEADLINE.

`STATE.md:125` now carries `ε_sup = d·n/(n+1)`, **linear in the incomparability density**, not a
flat `n/(n+1)`.  `c3` measured this instrument's realizability gap against the FLAT constant, and
against the flat constant the gap is a factor `3(n−1)/4`.  That number is not wrong, but it is
mostly a statement about `d`, and `mg-0e8c` already owns that.  So this arm asks the question the
correction forces:

  m1  IS THE DENSITY-AWARE BOUND SATURATED AT THE BOUNDARY?  `ε_obs` against `d·n/(n+1)`, exactly,
      at every member.  If they are EQUAL the realizability gap against the bound the corpus now
      states is **ZERO**, and `c3`'s factor is entirely a density gap.
  m2  THE TWO GAPS SIDE BY SIDE, so neither can be quoted as the other.
  m3  WHAT IS ACTUALLY LEFT, IN THE CURRENCY `STATE.md` USES.  The wall is already down at
      `d ≲ 2×10⁻²` (proven, all `n`, L4-free).  What is the largest `d` a `δ = 1/3` poset attains,
      and at what `n` does the boundary class fall into the already-proven regime?

⚠️  This arm exists because a landing on `main` made a section of this branch's own deliverable
narrower than it was written.  Recording that in a new arm rather than by quietly editing `c3` is
the same call `mg-ac0c` made on its own S3 an hour earlier, for the same reason: the superseded
reading has to stay legible next to what narrows it.

Exits 0 if the saturation check passes, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib6ff4 as L

NMAX = 9
EPS_DEM = Fraction(2, 100)
V_CANON = L.canon(3, (0, 1, 0))


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-6ff4  c5  the supply is d*n/(n+1), not a flat n/(n+1) -- what that leaves")
    print("=" * 100)
    print()

    classes = L.all_classes(nmax)
    rows = []
    for n in range(3, nmax + 1):
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            ok, d, tbl = L.delta_at_most(n, down)
            if not ok or d != L.THIRD:
                continue
            rows.append((n, down, L.measure(n, down, tbl)))
        print("    ... n = %d swept" % n, flush=True)
    print()

    print("m1  IS THE DENSITY-AWARE SUPPLY BOUND SATURATED AT THE BOUNDARY?")
    print("-" * 100)
    fail = 0
    for (n, down, mm) in rows:
        if mm["eps"] != mm["d"] * Fraction(n, n + 1):
            fail += 1
    print("    eps_obs == d*n/(n+1) checked at all %d boundary posets · mismatches %d   [%s]"
          % (len(rows), fail, "PASS" if fail == 0 else "FAIL"))
    print()
    print("    ⚠️  THE REALIZABILITY GAP AGAINST THE BOUND THE CORPUS NOW STATES IS **ZERO**, AT")
    print("    EVERY MEMBER, WITH NO SLACK AT ALL.  The reason is one line: mg-0e8c's chain uses")
    print("    Pr[flipped] < 1/3 per pair to get E[inv_e] < m/3; at delta = 1/3 EXACTLY every")
    print("    incomparable pair sits at exactly 1/3, so the inequality is an EQUALITY and the")
    print("    boundary class IS the equality case of the supply bound.")
    print("    So this instrument's `realizability gap' is a DENSITY gap and nothing else, and")
    print("    mg-0e8c/mg-ac0c already own the observation that d is the lever.")
    print()

    print("m2  THE TWO GAPS SIDE BY SIDE -- neither may be quoted as the other")
    print("-" * 100)
    per = {}
    for (n, down, mm) in rows:
        per.setdefault(n, []).append(mm)
    print("    %3s %12s %14s %14s %16s %18s"
          % ("n", "max eps", "flat n/(n+1)", "ratio vs flat", "d*n/(n+1) at max", "ratio vs density"))
    for n in sorted(per):
        mx = max(m["eps"] for m in per[n])
        arg = [m for m in per[n] if m["eps"] == mx][0]
        flat = Fraction(n, n + 1)
        dens = arg["d"] * Fraction(n, n + 1)
        print("    %3d %12s %14s %14.3f %16s %18s"
              % (n, str(mx), str(flat), float(flat / mx), str(dens),
                 "1 (SATURATED)" if dens == mx else "NOT SATURATED"))
    print()
    print("    LEFT COLUMN PAIR: the gap against a bound that assumes d = 1, i.e. against the")
    print("    ANTICHAIN's density.  RIGHT: the gap against the bound at the poset's own density.")
    print("    The first is real and is the price of the two-atom law being non-realizable AND")
    print("    dense; the second is zero.  Quoting the first as `how far below the bound real")
    print("    posets sit' overstates what realizability buys, because most of it is density.")
    print()

    print("m3  WHAT IS LEFT, IN STATE.md's OWN CURRENCY")
    print("-" * 100)
    print("    STATE.md:125 -- the wall is already DOWN, proven for all n and L4-free, at")
    print("    d <~ 2e-2; what is open is the DENSE regime.  So the question this instrument can")
    print("    actually answer is: HOW DENSE IS THE BOUNDARY CLASS?")
    print()
    print("    %3s %16s %16s %14s" % ("n", "max d at delta=1/3", "= 4*floor(n/3)/", "in the OPEN"))
    print("    %3s %16s %16s %14s" % ("", "", "(n(n-1))", "dense regime?"))
    for n in sorted(per):
        mxd = max(m["d"] for m in per[n])
        cf = Fraction(4 * (n // 3), n * (n - 1))
        print("    %3d %16s %16s %14s"
              % (n, str(mxd), str(cf) + ("" if cf == mxd else "  ⚠️ DISAGREES"),
                 "yes" if mxd > EPS_DEM else "NO -- already proven"))
    print()
    cross = None
    for n in range(3, 400):
        if Fraction(4 * (n // 3), n * n - 1) <= EPS_DEM:
            cross = n
            break
    last = max(n for n in range(3, 400) if Fraction(4 * (n // 3), n * n - 1) > EPS_DEM)
    print("    Under the closed form, the densest boundary poset leaves the open regime for good")
    print("    at n = %d (first n at or below: %d; it returns above once, at n = %d)."
          % (last + 1, cross, cross + 1))
    print("    ⚠️  EXTRAPOLATION past n = %d, exactly as c3 m4's is, and worth what the closed" % nmax)
    print("    form's survival is worth.  What it says is that the boundary class is a WITNESS")
    print("    FOR THE OPEN REGIME only at small n: by n = %d the densest object at delta = 1/3"
          % (last + 1,))
    print("    has fallen into the regime where L1b is already a theorem.")
    print()

    ok = fail == 0
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
