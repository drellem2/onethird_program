"""mg-200d V1 -- the BRANCH-FREE forms: baseline, the two literal forms, the two surrogates.

For each n it prints max E[inv_e], the resulting eps_spec = 6E/(n^2-1), the ratio against the
baseline n/(n+1), and whether the optimum is attained (it always is -- these are LPs over
non-empty compact polytopes -- so what is printed is the WITNESS).

Read the LITERAL rows with §2 of the document open: they are computed to be reported as
UNSOUND, not as bounds.  The surrogate rows are the sound branch-free numbers.
"""

import sys
from fractions import Fraction as F

from lp200d import Infeasible, inv_count, relaxation, measure_report, eps_spec

NS = [int(a) for a in sys.argv[1:]] or [3, 4, 5]

FORMS = [
    ("baseline  M_n only", "none", "sound (mg-6bc2's theorem)"),
    ("LITERAL per-slot  J_k(x,y)=J_k(y,x)", "slot_eq", "UNSOUND -- excludes every poset"),
    ("LITERAL aggregate J(x,y)=J(y,x)", "agg_eq", "UNSOUND -- excludes every poset"),
    ("SURROGATE per-slot  J_k(y,x)<=J_k(x,y)", "slot_le", "sound, branch-free"),
    ("SURROGATE aggregate J(y,x)<=J(x,y)", "agg_le", "sound, branch-free"),
]

print("=" * 78)
print("V1  BRANCH-FREE FORMS.  max E[inv_e] over measures on S_n, every pair flipped <= 1/3.")
print("    No posets are enumerated.")
print("=" * 78)

for n in NS:
    base = F(n * (n - 1), 6)
    print(f"\n### n = {n}   C(n,2)/3 = {base}   baseline eps_spec = n/(n+1) = {F(n, n + 1)}")
    for label, form, kind in FORMS:
        try:
            val, mu = relaxation(n, form)
        except Infeasible as e:
            print(f"  {label:42s} INFEASIBLE  ({e})     [{kind}]")
            continue
        es = eps_spec(n, val)
        ratio = val / base if base else F(0)
        rep = measure_report(n, mu)
        print(f"  {label:42s} max E[inv] = {str(val):>8}"
              f"   eps_spec = {str(es):>8} = {float(es):.6f}"
              f"   x baseline = {ratio}")
        print(f"  {'':42s} witness: {len(mu)} atoms, mass {rep['mass']},"
              f" max flip {rep['max_flip']},"
              f" per-slot-eq violations {len(rep['slot_eq_violations'])},"
              f" agg-eq {len(rep['agg_eq_violations'])}")
    print("  -- witness for the SURROGATE per-slot form (the sound branch-free optimum):")
    try:
        val, mu = relaxation(n, "slot_le")
        for p, w in sorted(mu.items(), key=lambda t: (-t[1], t[0])):
            print(f"       mass {str(w):>8}  perm {p}  inv={inv_count(p)}")
    except Infeasible as e:
        print(f"       INFEASIBLE ({e})")
