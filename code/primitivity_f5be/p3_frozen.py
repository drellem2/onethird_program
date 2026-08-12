"""p3 -- THE FROZEN CLASS.  Ticket step 3, second half.

pm-onethird's tighter ceiling is conditioned on FROZEN: every incomparable pair outside
[1/3, 2/3], i.e. delta(P) < 1/3, i.e. P is a counterexample to (1/3)-(2/3).  The ticket
already warns (from mg-145f) that this class may be EMPTY at every enumerable n, and that
an empty class must be reported as VACUOUS and not as a maximum of zero (PREDICTIONS E3).

This arm does three things:
  p3.1  measure the class.  It is empty, and the emptiness is reported as emptiness.
  p3.2  show the bound is not vacuous as ARITHMETIC even though the class is -- the chain
        holds at every poset, so `alpha <= 1/(2(1-mu))` is a real, non-conditional bound,
        and it bites hardest exactly where delta is smallest.
  p3.3  measure the NEAR-frozen class -- the posets that come closest to frozen in range --
        which is the only non-vacuous thing that can be said about the direction.
"""

import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libf5be as F  # noqa: E402
import lib409a as L  # noqa: E402

ok = True

def cover(n, lt):
    cov = [(a, b) for (a, b) in lt
           if not any((a, c) in lt and (c, b) in lt for c in range(n))]
    return "{" + ", ".join(f"{a}<{b}" for (a, b) in sorted(cov)) + "}" if cov else "{} (antichain)"

ROWS = []
for n in (2, 3, 4, 5, 6):
    for lt in F.posets_up_to_iso(n):
        LEs = L.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        st = F.all_pair_stats(n, lt, LEs)
        if not st:
            continue
        t1, t2 = F.chain_bound(st)
        ROWS.append({"n": n, "lt": lt, "N": len(LEs),
                     "delta": F.delta_of(st), "mu": F.mu_of(st),
                     "alpha": F.alpha_power(LEs, n), "t1": t1, "t2": t2,
                     "prime": F.is_primitive_proper(n, lt)})

# --------------------------------------------------------------------------------------
F.banner("p3.1  THE FROZEN CLASS -- delta(P) < 1/3.  IS IT INHABITED IN RANGE?")

print(f"  {'n':>2}  {'posets (|L|>=2)':>16}  {'FROZEN':>8}  {'min delta':>12}  "
      f"{'min delta as float':>19}")
total_frozen = 0
for n in (2, 3, 4, 5, 6):
    R = [r for r in ROWS if r["n"] == n]
    fr = [r for r in R if r["delta"] < Fraction(1, 3)]
    total_frozen += len(fr)
    md = min(r["delta"] for r in R)
    print(f"  {n:>2}  {len(R):>16}  {len(fr):>8}  {str(md):>12}  {F.frac(md):>19}")

ok &= F.verdict(total_frozen == 0,
                "THE FROZEN CLASS IS EMPTY at every n <= 6 -- (1/3)-(2/3) holds there",
                f"({total_frozen} frozen posets found)")

print("""
      SO THE FROZEN-CLASS MEASUREMENT IS VACUOUS, and that is the honest report.  It is
      NOT "max alpha over frozen posets = 0"; there is no maximum, because there is no
      poset.  This is exactly what the ticket anticipated from mg-145f and what
      PREDICTIONS E3 planted as an error to avoid.""")

# E3's control, made operational: the max over the frozen class must RAISE, not return 0.
frozen_rows = [r for r in ROWS if r["delta"] < Fraction(1, 3)]
raised = False
try:
    max(r["alpha"] for r in frozen_rows)
except ValueError:
    raised = True
ok &= F.verdict(raised, "max over the frozen class RAISES ValueError rather than printing a number",
                "(E3 control, and it fires)")

# --------------------------------------------------------------------------------------
F.banner("p3.2  THE CHAIN IS NOT CONDITIONAL -- it bounds alpha at EVERY poset, frozen or not")

# The frozen hypothesis is used ONLY to convert `mu < 1/3` into the number 3/4.  The bound
# alpha <= 1/(2(1-mu)) itself is unconditional.  Check it everywhere, exactly.
bad = 0
for r in ROWS:
    b = 1 / (2 * (1 - r["mu"]))
    if r["alpha"] > float(b) + 1e-9:
        bad += 1
    if b != r["t2"]:
        bad += 1
ok &= F.verdict(bad == 0,
                f"alpha <= 1/(2(1-mu)) = min-over-pairs TERM2 at all {len(ROWS)} posets, n<=6",
                f"{bad} violations")

# --------------------------------------------------------------------------------------
F.banner("p3.3  THE NEAR-FROZEN CLASS -- the only non-vacuous version of the question")

print("""  If no poset in range is frozen, the closest thing to pm-onethird's restriction that
  can actually be measured is: order the posets by delta (how close to a counterexample
  they are) and look at what the chain, and alpha itself, do at the bottom of that order.""")

ROWS.sort(key=lambda r: (r["delta"], -r["n"]))
print(f"\n  {'n':>2}  {'poset':<44} {'delta':>7} {'mu':>7} {'TERM2':>10} {'TERM1':>10} "
      f"{'alpha':>11} {'prim':>5}")
for r in ROWS[:14]:
    print(f"  {r['n']:>2}  {cover(r['n'], r['lt']):<44} {str(r['delta']):>7} {str(r['mu']):>7} "
          f"{F.frac(r['t2'], 4):>10} {F.frac(r['t1'], 4):>10} {r['alpha']:>11.6f} "
          f"{'yes' if r['prime'] else '-':>5}")

md = ROWS[0]["delta"]
print(f"""
  The smallest delta available anywhere in range is {md} = {F.frac(md)}.  For reference the
  best known unconditional bound is delta >= (5-sqrt5)/10 = 0.2763932..., so the enumeration
  reaches posets essentially at the extremal value and still finds no counterexample.

  AT THAT POSET the chain returns TERM2 = {F.frac(ROWS[0]['t2'])} and TERM1 =
  {F.frac(ROWS[0]['t1'])}, while alpha is actually {ROWS[0]['alpha']:.6f}.""")

# The headline comparison the ticket wants: what the chain would give on a hypothetical
# frozen poset, versus what is measured at the least-balanced posets that exist.
print(f"""
  {'':4}{'restriction':<34}{'ceiling':>12}   status
  {'':4}{'-'*34}{'-'*12}   {'-'*28}
  {'':4}{'none (every poset)':<34}{'1':>12}   PROVED (mg-409a section 3)
  {'':4}{'frozen: delta < 1/3':<34}{'3/4':>12}   VACUOUS -- class is empty to n=14
  {'':4}{'primitive (n>=4)':<34}{'0.3877':>12}   MEASURED exhaustively to n=7
  {'':4}{'the bar the route must clear':<34}{'>= 2':>12}   PROVED (mg-409a section 2)""")

# --------------------------------------------------------------------------------------
F.banner("p3.4  WOULD A FROZEN POSET EVEN HELP?  -- the bound, evaluated hypothetically")

print("""  A frozen poset has every pair outside [1/3,2/3], hence mu < 1/3, hence
  alpha <= 1/(2(1-mu)) < 3/4.  Since the bar is a constant >= 2 (mg-409a section 2), the
  shortfall goes from a factor of 2 to a factor of 8/3.  Both are shortfalls.  The
  arithmetic below is unconditional -- it needs no poset to exist.""")
for mu_v in [Fraction(1, 3), Fraction(3, 10), Fraction(1, 4), Fraction(1, 5), Fraction(0)]:
    b = 1 / (2 * (1 - mu_v))
    print(f"      mu = {str(mu_v):>6}   ceiling 1/(2(1-mu)) = {F.frac(b)}   "
          f"bar/ceiling >= {F.frac(2 / b, 4)}")
ok &= F.verdict(1 / (2 * (1 - Fraction(1, 3))) == Fraction(3, 4),
                "at mu = 1/3 the ceiling is exactly 3/4", "pm-onethird's number confirmed")
ok &= F.verdict(all(1 / (2 * (1 - Fraction(a, 100))) < 2 for a in range(0, 34)),
                "for every mu < 1/3 the ceiling is STILL below the bar of 2",
                "the strengthening does not change the verdict, only the margin")

print()
print("=" * 88)
print("p3 OVERALL: " + ("PASS" if ok else "FAIL"))
print("=" * 88)
sys.exit(0 if ok else 1)
