"""s4 — THE ONE FAMILY ON WHICH BOTH ROUTE CONSTANTS RISE TOGETHER.

n = 7 exhaustive (s3) shows the two routes dying at DISJOINT sets of posets: 168 where (F)
fails, 4 where (M#) fails, intersection EMPTY.  This driver asks the obvious next question --
is the emptiness structural, or just small-n? -- by building the one construction that
combines both failure mechanisms and pushing it as far as exact arithmetic reaches.

EVERY ROW IS A FAMILY MEMBER.  NONE OF THEM IS A MAXIMUM OVER ITS n.
"""
from fractions import Fraction as F
import sys, time
from lib51f4 import (fam_near_ordinal_plus_point, measure, floor_msharp, gap_at_least,
                     mu_bracket, sweep_bound_sq)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22
EXACT_UPTO = int(sys.argv[2]) if len(sys.argv) > 2 else 15

print("FAMILY: near-ordinal sum of two antichains on {0..n-2}, PLUS one isolated element.")
print("The near-ordinal part supplies the thin bottleneck that kills (F); the isolated")
print("element supplies the non-monotone Fiedler direction that kills (M#).")
print()
print("  n | gamma      D       c#      f*      min     floor  | (F) fails? | (M#) fails?")
print(" ---+------------+-------+-------+-------+-------+-------+------------+------------")
for n in range(8, NMAX + 1):
    t0 = time.time()
    P = fam_near_ordinal_plus_point(n)
    if not P.is_primitive():
        print("  %2d | DECOMPOSABLE" % n)
        continue
    r = measure(P, iters=50)
    M = P.M_mean()
    ffail = not gap_at_least(P, M * M / 2)
    if n <= EXACT_UPTO:
        lo, _ = mu_bracket(P, iters=34)
        mfail = not gap_at_least(P, sweep_bound_sq(r.dmax, lo) / 2)
        mtag = "EXACT: " + ("FAILS" if mfail else "holds")
    else:
        mtag = "n/a (c# upper bd %.4f)" % float(r.c_sharp_hi)
    print("  %2d | %.8f | %.5f | %.4f | %.4f | %.4f | %.4f | %-10s | %s   (%.0fs)"
          % (n, float(r.gamma_lo), float(r.dmax), float(r.c_sharp_hi), float(r.f_hi),
             float(min(r.c_sharp_hi, r.f_hi)), float(floor_msharp(r)),
             "EXACT: FAILS" if ffail else "holds", mtag, time.time() - t0))
    sys.stdout.flush()
print()
print("EPISTEMIC SPLIT, stated where it cannot be separated from the numbers:")
print("  * `(F) fails` is EXACT at every n above: one decision, gamma < M^2/2.")
print("  * `(M#) fails` is EXACT only to n = %d, where mu_pref is bracketed by exact" % EXACT_UPTO)
print("    copositivity over 2^(n-1)-1 simplex faces.  Past that the c# column is computed")
print("    from an EXHIBITED monotone vector, so it is an UPPER bound on c#: it can certify")
print("    that (M#) HOLDS and can NEVER certify that it fails.  A c# above 1 there is a")
print("    MEASUREMENT and is labelled `n/a`, not `FAILS`.")
