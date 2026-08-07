"""mg-200d V1b -- the n=6 SURROGATE values on their own.

`v1_forms.py 6` runs the LITERAL forms first, and at n=6 those are 720 columns against 75
EQUALITY rows, so phase 1 carries 76 artificials and does not finish in this run's budget.
The surrogate forms are inequality-only, so the origin-adjacent start is cheap.  This script
solves just those, so that §3's "buys nothing" row has its n=6 entry from a measurement
rather than from an extrapolation off n <= 5.
"""
import sys
from fractions import Fraction as F
from lp200d import relaxation, measure_report, eps_spec, inv_count

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
base = F(n * (n - 1), 6)
print(f"n = {n}   C(n,2)/3 = {base}   n/(n+1) = {F(n, n+1)}")
for label, form in (("baseline", "none"), ("SURROGATE per-slot", "slot_le"),
                    ("SURROGATE aggregate", "agg_le")):
    val, mu = relaxation(n, form)
    rep = measure_report(n, mu)
    print(f"  {label:22s} max E[inv] = {str(val):>8}  eps_spec = {str(eps_spec(n, val)):>8}"
          f"  x baseline = {val/base}  atoms {len(mu)}  mass {rep['mass']}"
          f"  max flip {rep['max_flip']}")
