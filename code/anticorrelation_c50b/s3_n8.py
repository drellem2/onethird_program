"""s3 -- THE POPULATION NOBODY HAS ENUMERATED: all 2800472 naturally labelled posets
on [8] (2600369 primitive).  The count is this run's own output; the 2903405 written
here before the run was mine from memory and was wrong.

This is outcome (b)'s only exhaustive arm.  It is a TWO-STAGE pass and the first stage
is a RIGOROUS screen, not a sample:

    mu_pref <= 2 Phi*_pref            (proved: the centred prefix indicator is monotone
                                       and n/max(k,n-k) <= 2)
    t -> t(2D-t) increases on [0,D]   (mg-28ff  §2)
  =>  c#  <=  c#_UB := sweep(min(2 Phi*, Delta), Delta) / (2 gamma)

so any poset with min(c#_UB, f*) <= THRESH provably has min(c#, f*) <= THRESH and
CANNOT be a counterexample to the disjunction, nor the argmax of c_or(8) once one
survivor beats THRESH.  Stage two gives every survivor the full exact treatment of s1.

THE ONE FLOAT ON THE SCREEN PATH is gamma, used at 1e-6 relative slack in the
CONSERVATIVE direction (a smaller gamma makes both c#_UB and f* larger, i.e. makes the
screen keep MORE).  Every survivor's verdict is then decided on integers.
"""
import sys, time, pickle
from fractions import Fraction
from libc50b import (gen_posets, Poset, height, mu_exhaustive, exact_ub_from,
                     m_sharp_exact)

N = 8
THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 0.85

print("s3.  EXHAUSTIVE n = 8 -- rigorous two-stage screen at THRESH = %.2f" % THRESH)
print("     stage-1 bound:  c# <= sweep(min(2 Phi*, Delta), Delta) / (2 gamma)")
sys.stdout.flush()

t0 = time.time()
tot = prim = kept = 0
best = (0.0, None)
survivors = []
for dn in gen_posets(N):
    tot += 1
    P = Poset(dn, N)
    if not P.primitive():
        continue
    prim += 1
    g = P.gamma_float() * (1.0 - 1e-6)
    Mf = float(P.M())
    fstar = Mf * Mf / (2 * g)
    if fstar > THRESH:
        d = float(P.Delta())
        mu_ub = min(2.0 * float(P.Phi_star()), d)
        c_ub = (mu_ub * (2 * d - mu_ub) if mu_ub <= d else d * d) / (2 * g)
        m = min(c_ub, fstar)
        if m > THRESH:
            kept += 1
            survivors.append(dn)
    if prim % 200000 == 0:
        print("   ... %8d primitive, %5d survivors, %.0fs" % (prim, kept, time.time() - t0))
        sys.stdout.flush()

print("\n  posets on [8]: %d      primitive: %d" % (tot, prim))
print("  stage-1 survivors (min(c#_UB, f*) > %.2f): %d" % (THRESH, kept))
print("  stage-1 elapsed %.0f s" % (time.time() - t0))
sys.stdout.flush()

print("\n  STAGE 2 -- full exact treatment of every survivor")
Ffail = Mfail = both = refuse = 0
hF, hM = {}, {}
bestrow = None
for dn in survivors:
    P = Poset(dn, N)
    g = P.gamma_float()
    mu, bv = mu_exhaustive(P)
    d = float(P.Delta())
    cs = (mu * (2 * d - mu) if mu <= d else d * d) / (2 * g)
    fs = float(P.M()) ** 2 / (2 * g)
    mn = min(cs, fs)
    h = height(dn, N)
    f_fail = P.F_fails()
    mu_ub = exact_ub_from(P, bv[0], bv[1]) if bv else None
    mv, _ = m_sharp_exact(P, mu_ub)
    if f_fail:
        Ffail += 1
        hF[h] = hF.get(h, 0) + 1
    if mv == "FAILS":
        Mfail += 1
        hM[h] = hM.get(h, 0) + 1
    elif mv == "REFUSE":
        refuse += 1
    if f_fail and mv == "FAILS":
        both += 1
        print("  *** BOTH ROUTES FAIL *** %s  c#=%.6f f*=%.6f" % (dn, cs, fs))
    if mn > best[0]:
        best = (mn, dn)
        bestrow = (cs, fs, g, h, str(P.Delta()), str(P.Phi_star()), str(P.M()))

print("  (F)  fails at %d SURVIVORS   [a LOWER BOUND on the n=8 count, NOT a census:\n         the screen also demands c#_UB > THRESH -- see s5_n8_scope.py]" % Ffail)
print("  (M#) fails at %d SURVIVORS   [i.e. no poset has (M#) failing AND f* > THRESH;\n         says NOTHING about (M#)'s failure count at n=8 -- see s5_n8_scope.py]" % Mfail)
print("  BOTH FAIL  at %d of %d primitive   [EXHAUSTIVE: every both-failing poset\n         provably survives the screen]" % (both, prim))
print("  REFUSED: %d" % refuse)
print("  (F)  fail heights: %s" % dict(sorted(hF.items())))
print("  (M#) fail heights: %s" % dict(sorted(hM.items())))
print("\n  c_or(8) = %.6f   [EXHAUSTIVE: every excluded poset provably has min <= %.2f]"
      % (best[0], THRESH))
print("  argmax dn = %s" % (best[1],))
if bestrow:
    print("  at the argmax: c# = %.6f  f* = %.6f  gamma = %.6f  height = %d" % bestrow[:4])
    print("                 Delta = %s  Phi* = %s  M = %s" % bestrow[4:])
print("  total elapsed %.0f s" % (time.time() - t0))
with open("out_s3_survivors.pkl", "wb") as fh:
    pickle.dump(survivors, fh)
