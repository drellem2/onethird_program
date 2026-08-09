"""s3 — n = 7, EXHAUSTIVE.

`mg-28ff`'s evidence stops at `n = 6`; every `n = 7` figure in it is a deterministic sample
of 40-200 posets out of a population of order 10^6 and is labelled NOT A MAXIMUM at each
appearance.  This driver enumerates the population instead, so the `n = 7` row below IS a
maximum over a fully enumerated population.  It streams: each poset is measured and
discarded, so nothing is cached across the run.

The verdicts are exact.  `gamma` is bracketed by exact bisection on the signs of the
principal minors of `Q - rN`; `mu_pref` enters only through an EXHIBITED monotone vector
whose Rayleigh quotient is exact, which is an UPPER bound on `mu_pref` and therefore an
UPPER bound on `c#` -- the direction a ceiling needs.  The reported maxima of `c#` and of
`c_or` are therefore upper bounds on the true maxima; `c_true` and `f*` carry no such caveat.
"""

from fractions import Fraction as F
import sys
import time

from lib51f4 import (all_posets, measure, floor_msharp, gap_at_least)

N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
TOPK = 12

t0 = time.time()
posets = all_posets(N)
print("n=%d: %d posets with the identity a linear extension  (enumerated in %.0fs)"
      % (N, len(posets), time.time() - t0))
sys.stdout.flush()

best = {k: [] for k in ("c_true", "c_sharp", "f", "c_or", "floor", "lam_m", "lam_f")}
nprim = 0
f_fail = 0
m_fail_ub = 0
both_fail = 0
bins = {}
t0 = time.time()
for i, P in enumerate(posets):
    if i and i % 5000 == 0:
        print("   ... %d/%d  (%.0fs)" % (i, len(posets), time.time() - t0))
        sys.stdout.flush()
    r = measure(P, iters=44)
    if not r.primitive:
        continue
    nprim += 1
    cor = min(r.c_sharp_hi, r.f_hi)
    rel = P.rel_pairs()
    for key, val in (("c_true", r.c_true_hi), ("c_sharp", r.c_sharp_hi), ("f", r.f_hi),
                     ("c_or", cor), ("floor", floor_msharp(r)),
                     ("lam_m", r.c_sharp_lo / r.c_true_hi), ("lam_f", r.M / r.phistar)):
        b = best[key]
        b.append((val, rel, r.gamma_lo, r.dmax, r.phistar, r.M, r.c_true_hi,
                  r.c_sharp_hi, r.f_hi))
        if len(b) > 400:
            b.sort(key=lambda t: -t[0])
            del b[TOPK:]
    if r.f_hi > 1:
        f_fail += 1
    if r.c_sharp_hi > 1:
        m_fail_ub += 1
        if r.f_hi > 1:
            both_fail += 1
    # gamma bins
    g = float(r.gamma_lo)
    key = 0 if g < 0.05 else 1 if g < 0.1 else 2 if g < 0.2 else 3 if g < 0.3 else 4 if g < 0.5 else 5
    e = bins.setdefault(key, [0, 0.0, 0.0, 0.0, 0.0, 0.0])
    e[0] += 1
    e[1] = max(e[1], float(r.mu / r.gamma_hi))
    e[2] = max(e[2], float(r.M / r.phistar))
    e[3] = max(e[3], float(r.c_sharp_hi))
    e[4] = max(e[4], float(r.f_hi))
    e[5] = max(e[5], float(cor))
for k in best:
    best[k].sort(key=lambda t: -t[0])
    del best[k][TOPK:]
print("   done in %.0fs;  %d primitive of %d" % (time.time() - t0, nprim, len(posets)))


def hdr(t):
    print()
    print("=" * 104)
    print(t)
    print("=" * 104)


hdr("S3.1  n = 7, EXHAUSTIVE — THE FOUR CONSTANTS, EACH A MAXIMUM OVER A FULLY "
    "ENUMERATED POPULATION")
print("Population: all %d primitive posets on [%d] with the identity a linear extension."
      % (nprim, N))
print("This row is NOT a sample.  mg-28ff's n=7 rows ARE samples and are not quoted here.")
print()
for k, label in (("c_true", "c_true  (the truth, route-independent)"),
                 ("c_sharp", "c#      (route (M#); UPPER bound -- exhibited vector)"),
                 ("f", "f*      (route (F))"),
                 ("c_or", "c_or    (the DISJUNCTION min(c#,f*); UPPER bound)"),
                 ("floor", "floor   (max of Delta_P - gamma/2)")):
    v = best[k][0]
    print("  %-52s = %.6f" % (label, float(v[0])))
    print("       at  %s" % (list(v[1]),))
    print("       gamma=%.6f Delta=%.5f Phi*=%.6f M=%.6f | c_true=%.4f c#=%.4f f*=%.4f"
          % (float(v[2]), float(v[3]), float(v[4]), float(v[5]), float(v[6]),
             float(v[7]), float(v[8])))
print()
print("  primitive posets at n=7 where route (F) FAILS  (f* > 1):            %6d of %d"
      % (f_fail, nprim))
print("  primitive posets at n=7 where route (M#) fails on the exhibited")
print("      vector (c#_upper > 1; an upper bound, so this OVERCOUNTS):      %6d of %d"
      % (m_fail_ub, nprim))
print("  primitive posets at n=7 where BOTH fail (the disjunction dies):     %6d of %d"
      % (both_fail, nprim))

hdr("S3.2  THE TOP OF EACH COLUMN AT n = 7 (EXHAUSTIVE)")
for k in ("c_or", "f", "c_sharp", "lam_m", "lam_f"):
    print("  --- largest %s" % k)
    for v in best[k][:6]:
        print("      %.6f   gamma=%.6f D=%.4f c_true=%.4f c#=%.4f f*=%.4f   %s"
              % (float(v[0]), float(v[2]), float(v[3]), float(v[6]), float(v[7]),
                 float(v[8]), list(v[1])))

hdr("S3.3  THE ANTI-CORRELATION AT n = 7 (EXHAUSTIVE) — cf. S1.7 at n <= 6")
print("   gamma bin      | count | max mu/gamma | max M/Phi* | max c# | max f* | max min(c#,f*)")
print("  ---------------+-------+--------------+------------+--------+--------+---------------")
lab = ["[0.00,0.05)", "[0.05,0.10)", "[0.10,0.20)", "[0.20,0.30)", "[0.30,0.50)",
       "[0.50,   1]"]
for key in sorted(bins):
    e = bins[key]
    print("   %-13s | %5d | %12.4f | %10.3f | %6.4f | %6.4f | %13.4f"
          % (lab[key], e[0], e[1], e[2], e[3], e[4], e[5]))
