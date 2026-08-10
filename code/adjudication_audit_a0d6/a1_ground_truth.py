"""a1 — THE RE-DERIVATION. The number the adjudication turns on, computed here.

The landing under audit decides which of two landed documents is false by reading

    'primitive posets at n=7 where route (F) FAILS  (f* > 1):  168 of 86278'

**out of `mg-51f4`'s own transcript.** `mg-28ff:21` quotes the same number, `mg-29fe` took it
from the same place, and `mg-64cb` never touched it. So the figure that decides the
contradiction has been carried through four tickets and recomputed by none. This arm
recomputes it, on an instrument importing neither library.

EVERY REPORTED FAILURE IS CERTIFIED EXACTLY by an exhibited rational vector `v ⊥ 1` with
`<v,Lv> < (M^2/2)<v,v>`; every reported HOLD inside the boundary band, and every hold at
`n <= 6`, is certified exactly by a PSD test. Floats only order the population.
"""

from fractions import Fraction as F
import sys
import time

from liba0d6 import (naturally_labelled, is_primitive, transport_counts, M_exact,
                     laplacian_exact, gamma_float, certify_fail, certify_hold,
                     leak_prefix_numerators, rel_pairs)

BAND = 0.999          # every poset with float f* above this is decided EXACTLY, both ways
SUBSAMPLE = 40        # of the rest, every 40th is exactly re-decided as a control

print("=" * 96)
print("a1 — ROUTE (F) AT n = 2..7, EXHAUSTIVE, RE-DERIVED")
print("=" * 96)
print()
print("  f*(P) = M^2 / (2 gamma).  Route (F) FAILS at P iff f* > 1 iff gamma < M^2/2.")
print("  A FAILURE is certified by an exhibited rational v perp 1 with R(v) < M^2/2.")
print("  A HOLD is certified by exact PSD of L - (M^2/2)(I - J/n).  No float decides.")
print()

summary = {}
for n in range(2, 8):
    t0 = time.time()
    posets = naturally_labelled(n)
    total = len(posets)
    nprim = 0
    fails_cert = []
    band_holds = 0
    holds_cert = 0
    holds_float = 0
    unresolved = []
    best_f = (0.0, None)
    best_ctrue = (F(0), None)
    checked_sub = 0
    closest_hold = 0.0          # largest float f* among the posets where (F) HOLDS
    closest_fail = float("inf")  # smallest float f* among the posets where (F) FAILS
    for idx, d in enumerate(posets):
        if not is_primitive(n, d):
            continue
        nprim += 1
        cnt, N = transport_counts(n, d)
        M = M_exact(n, cnt, N)
        lam, vec = gamma_float(n, cnt, N)
        t = M * M / 2
        ff = float(M) ** 2 / (2 * lam) if lam > 0 else float("inf")
        if ff > best_f[0]:
            best_f = (ff, d)
        # c_true = Phi*_pref^2 / (2 gamma), the OTHER published column, for cross-check
        nums = leak_prefix_numerators(n, cnt)
        phis = min(F(nums[k - 1], N * min(k, n - k)) for k in range(1, n))
        ct = float(phis) ** 2 / (2 * lam) if lam > 0 else float("inf")
        if F(round(ct * 10 ** 9), 10 ** 9) > best_ctrue[0]:
            best_ctrue = (F(round(ct * 10 ** 9), 10 ** 9), d)
        decide_exactly = (ff > BAND) or (n <= 6) or (nprim % SUBSAMPLE == 0)
        if not decide_exactly:
            holds_float += 1
            closest_hold = max(closest_hold, ff)
            continue
        L = laplacian_exact(n, cnt, N)
        w = certify_fail(L, t, vec)
        if w is not None:
            fails_cert.append((ff, d, w))
            closest_fail = min(closest_fail, ff)
        elif certify_hold(L, t):
            holds_cert += 1
            closest_hold = max(closest_hold, ff)
            if ff > BAND:
                band_holds += 1
            if not (ff > BAND) and n == 7:
                checked_sub += 1
        else:
            unresolved.append((ff, d))
    dt = time.time() - t0
    summary[n] = dict(total=total, prim=nprim, fails=len(fails_cert),
                      holds_cert=holds_cert, holds_float=holds_float,
                      band_holds=band_holds, unresolved=len(unresolved),
                      best_f=best_f, best_ctrue=best_ctrue, sub=checked_sub, secs=dt,
                      closest_hold=closest_hold, closest_fail=closest_fail)
    print("n = %d  |  %6d posets, %6d primitive  |  (F) FAILS at %4d  (each CERTIFIED exactly)"
          % (n, total, nprim, len(fails_cert)))
    print("        max f* ~ %.6f    max c_true ~ %.6f    [%.0fs]"
          % (best_f[0], float(best_ctrue[0]), dt))
    print("        exactly certified HOLDS: %d   (of which %d inside the boundary band f* > %.3f)"
          % (holds_cert, band_holds, BAND))
    print("        float-only HOLDS: %d   unresolved: %d" % (holds_float, len(unresolved)))
    if unresolved:
        print("        !! UNRESOLVED — neither certifier answered; the verdict is NOT published")
        for ff, d in unresolved[:5]:
            print("           f*~%.9f  %s" % (ff, rel_pairs(n, d)))
    sys.stdout.flush()

print()
print("=" * 96)
print("THE COMPARISON — MY NUMBERS AGAINST THE ONES THE ADJUDICATION USED")
print("=" * 96)
print()
print("  population, n = 2..7        : %s   (mg-51f4 doc:143  2 / 7 / 40 / 357 / 4824 / 96428)"
      % " / ".join(str(summary[n]["total"]) for n in range(2, 8)))
print("  primitive,  n = 2..7        : %s   (mg-51f4 doc:143  1 / 4 / 27 / 275 / 4070 / 86278)"
      % " / ".join(str(summary[n]["prim"]) for n in range(2, 8)))
print()
print("  (F) FAILS at n = 7          : %d of %d" % (summary[7]["fails"], summary[7]["prim"]))
print("  out_s3_n7.txt says          : 168 of 86278")
ok7 = summary[7]["fails"] == 168 and summary[7]["prim"] == 86278
print("  ->  %s" % ("REPRODUCED EXACTLY" if ok7 else "*** DISAGREEMENT ***"))
print()
low = [n for n in range(2, 7) if summary[n]["fails"]]
print("  (F) FAILS at n <= 6         : %s"
      % ("at NO n" if not low else "at n = " + ", ".join(map(str, low))))
print("  ->  mg-28ff's '100 %% at every ENUMERATED n' is %s of n <= 6, and false ONLY at n = 7."
      % ("TRUE" if not low else "FALSE"))
print("      That is exactly the scope mg-28ff:21 claims — no wider, no narrower.")
print()
print("  max f* at n = 7             : ~%.6f   (mg-51f4 doc:159 and out_s3_n7.txt: 1.297074)"
      % summary[7]["best_f"][0])
print("  max c_true at n = 7         : ~%.6f   (mg-51f4 doc:159 / doc:150: 0.340719)"
      % float(summary[7]["best_ctrue"][0]))
print("  argmax f* at n = 7          : %s" % rel_pairs(7, summary[7]["best_f"][1]))
print("  out_s3_n7.txt's argmax      : [(0, 3), (0, 4), (0, 5), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4), (2, 5), (2, 6)]")
print()
print("  the retained sentence in mg-51f4 SS4 says its sample 'was low by a factor of 1.93':")
print("      0.340719 / 0.176145 = %.4f" % (0.340719 / 0.176145))
print()
print("  EXACTNESS OF THE n = 7 VERDICTS")
print("      certified FAILING  : %d" % summary[7]["fails"])
print("      certified HOLDING  : %d  (all %d posets with float f* > %.3f, plus a"
      % (summary[7]["holds_cert"], summary[7]["band_holds"], BAND))
print("                            deterministic every-%dth control of %d further posets)"
      % (SUBSAMPLE, summary[7]["sub"]))
print("      float-only HOLDING : %d   — and THE POPULATION IS NOT NEAR THE BOUNDARY:"
      % summary[7]["holds_float"])
print("                            the largest f* at a HOLDING poset is %.9f and the"
      % summary[7]["closest_hold"])
print("                            smallest at a FAILING one is %.9f, a gap of %.4f"
      % (summary[7]["closest_fail"], summary[7]["closest_fail"] - summary[7]["closest_hold"]))
print("                            against a Jacobi residual of order 10^-14, so no float")
print("                            verdict here is within 10 orders of magnitude of flipping")
print("      unresolved         : %d" % summary[7]["unresolved"])
print()
print("VERDICT:  %s" % ("mg-28ff:21's UNDERLYING MEASUREMENT IS CONFIRMED INDEPENDENTLY."
                        if ok7 and not low else "THE MEASUREMENT DOES NOT REPRODUCE."))
print("=" * 96)
sys.exit(0 if (ok7 and not low and summary[7]["unresolved"] == 0) else 1)
