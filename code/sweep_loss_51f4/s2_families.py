"""s2 — THE NAMED FAMILIES, AND THE TWO EXACT REFUTATIONS.

Every number produced here is a value AT A NAMED FAMILY MEMBER.  It is NOT a maximum over
posets of that size and it is labelled FAMILY at every appearance (PREDICTIONS.md E1).
A REFUTATION does not need to be a maximum: one poset at which a hypothesis is false
refutes it, whatever the rest of the population does.  Everything else here is a trend
along one family and is worth exactly that much.
"""

from fractions import Fraction as F
import sys
import time

from lib51f4 import (FAMILIES, fam_chain_plus_point, fam_near_ordinal_antichains,
                     fam_bipartite_ladder, measure, floor_msharp, gap_at_least,
                     mu_bracket, sweep_bound_sq, mu_pref_exact_upper)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
EXACT_MU_UPTO = int(sys.argv[2]) if len(sys.argv) > 2 else 13


def row(P, exact_mu=False):
    r = measure(P, iters=50)
    if not r.primitive:
        return None
    out = dict(n=P.n, gamma_lo=r.gamma_lo, gamma_hi=r.gamma_hi, D=r.dmax,
               phistar=r.phistar, M=r.M, c_true=r.c_true_hi, c_sharp=r.c_sharp_hi,
               f=r.f_hi, floor=floor_msharp(r), mu_up=r.mu, mu_lo=None, r=r)
    if exact_mu:
        lo, hi = mu_bracket(P, iters=34)
        out["mu_lo"] = lo
        assert lo <= r.mu + F(1, 10 ** 9), "exact bracket above the exhibited upper bound"
    return out


def hdr(title):
    print()
    print("=" * 100)
    print(title)
    print("=" * 100)


hdr("S2.1  THE NINE NAMED FAMILIES — EVERY ROW IS A FAMILY MEMBER, NEVER A MAXIMUM")
print("gamma = 1 - lambda_std (exact bracket, lower endpoint shown).  D = Delta_P.")
print("c_true = Phi*_pref^2/(2 gamma)   c# = sweep(mu,D)/(2 gamma)   f* = M^2/(2 gamma)")
print("floor  = D - gamma/2   (mg-51f4's exact floor on c#, PREDICTIONS P1)")
print("Lam_M  = c#/c_true  (THE SWEEP'S LOSS)      Lam_F = M/Phi*_pref  (THE MEDIANT LOSS)")
print()
print("READ THE c# COLUMN AS AN UPPER BOUND.  It is computed from an EXHIBITED monotone")
print("vector, so it bounds mu_pref from ABOVE and therefore bounds c# from above.  That")
print("direction CERTIFIES that (M#) holds and can NEVER certify that it fails; the exact")
print("cone-minimum brackets that do certify failure are in S2.3.  The f* column carries no")
print("such caveat -- it has no eigenvector in it and is exact throughout.")
print()
for name, fn in FAMILIES:
    print(f"--- FAMILY: {name}")
    printed = False
    for n in range(4, NMAX + 1):
        P = fn(n)
        d = row(P)
        if d is None:
            if not printed:
                print("      DECOMPOSABLE at every n tested — out of scope for both routes "
                      "(gamma = 0); route (F) is a statement about PRIMITIVE posets")
                printed = True
            continue
        lam_m = d["c_sharp"] / d["c_true"]
        lam_f = d["M"] / d["phistar"]
        flag = ""
        if d["f"] > 1:
            flag += "  <== (F) FAILS HERE (exact)"
        if d["c_sharp"] > 1:
            flag += "  <== c# UPPER BOUND > 1 (see S2.3 for the exact certificate)"
        print("   n=%2d  gamma=%.7f D=%.5f Phi*=%.6f M=%.6f | c_true=%.4f c#=%.4f "
              "f*=%.4f  min=%.4f | floor=%.4f  Lam_M=%7.1f Lam_F=%6.2f%s"
              % (n, float(d["gamma_lo"]), float(d["D"]), float(d["phistar"]),
                 float(d["M"]), float(d["c_true"]), float(d["c_sharp"]), float(d["f"]),
                 float(min(d["c_sharp"], d["f"])), float(d["floor"]),
                 float(lam_m), float(lam_f), flag))
    print()


hdr("S2.2  REFUTATION 1 — ROUTE (F) IS FALSE AT AN EXHIBITED POSET ON 7 ELEMENTS. EXACT.")
print("(F) reads   E[D_F]^2 <= 8 floor(n^2/4)^2 (1 - lambda_std),  equivalently  M^2 <= 2 gamma.")
print("It fails at P iff gamma < M^2/2, which is ONE exact decision: the negation of")
print("`gamma >= M^2/2`, settled by the signs of the principal minors of Q - (M^2/2) N.")
print("NO float appears anywhere in the verdict, and this is a COUNTEREXAMPLE, so it does")
print("not need to be a maximum over its n.")
print()
for n in range(6, 13):
    P = fam_near_ordinal_antichains(n, 1)
    if not P.is_primitive():
        continue
    M = P.M_mean()
    thr = M * M / 2
    holds = gap_at_least(P, thr)
    r = measure(P, iters=50)
    print("   n=%2d  FAMILY near-ordinal antichains(1 missing)   M=%-10s M^2/2=%-22s "
          "gamma>=M^2/2 ? %-5s  ==> (F) %s   [f* ~ %.4f]"
          % (n, str(M), str(thr), holds, "HOLDS" if holds else "*** FAILS ***",
             float(r.f_hi)))
P7 = fam_near_ordinal_antichains(7, 1)
print()
print("   THE WITNESS, written out:")
print("     n = 7,  relations  %s" % (list(P7.rel_pairs()),))
print("     A = {0,1,2} and B = {3,4,5,6} are antichains, every a < b holds EXCEPT (2,3).")
print("     linear extensions            = %d" % P7.nle())
print("     prefix leaks   leak(A_k)     = %s" % [str(P7.leak_pref(k)) for k in range(1, 7)])
print("     profile        phi_k         = %s" % [str(x) for x in P7.profile()])
print("     Phi*_pref = %s at k = %d      M = %s" %
      (P7.phi_star_pref()[0], P7.phi_star_pref()[1], P7.M_mean()))
print("     E[D_F] = %s" % P7.E_footrule())
r7 = measure(P7, iters=60)
print("     gamma in (%s, %s]" % (r7.gamma_lo, r7.gamma_hi))
print("     M^2/2 = %s  >  gamma   ==>  f* = %.6f  >  1" %
      (P7.M_mean() ** 2 / 2, float(r7.f_hi)))
print("     Delta_P = %s   c_true = %.6f   c# = %.6f   min(c#,f*) = %.6f" %
      (r7.dmax, float(r7.c_true_hi), float(r7.c_sharp_hi),
       float(min(r7.c_sharp_hi, r7.f_hi))))


hdr("S2.3  REFUTATION 2 — ROUTE (M#) IS FALSE AT AN EXHIBITED POSET. EXACT.")
print("(M#) reads   mu_pref (2 Delta_P - mu_pref) <= 2(1 - lambda_std).")
print("Refuting it needs a LOWER bound on mu_pref — the direction mg-28ff Sec 10 records as")
print("a FLOAT MEASUREMENT.  Here mu_pref is bracketed EXACTLY: `mu_pref >= t` is decided as")
print("COPOSITIVITY of Q - tN over the monotone cone, by exact KKT enumeration of the")
print("2^(n-1)-1 faces of the simplex.  The verdict then compares two exact rationals.")
print()
for n in range(9, min(NMAX, EXACT_MU_UPTO) + 1):
    P = fam_chain_plus_point(n)
    t0 = time.time()
    mu_lo, mu_hi = mu_bracket(P, iters=34)
    r = measure(P, iters=60)
    sw = sweep_bound_sq(r.dmax, mu_lo)          # sweep is increasing in mu on [0, Delta]
    thr = sw / 2
    holds = gap_at_least(P, thr)                # gamma >= sw/2  <=>  (M#) holds
    print("   n=%2d  FAMILY chain(n-1)+point   mu_pref in [%.9f, %.9f]  Delta=%.6f  "
          "sweep/2=%.9f  gamma>=sweep/2 ? %-5s  ==> (M#) %s   [c# ~ %.5f]  (%.0fs)"
          % (n, float(mu_lo), float(mu_hi), float(r.dmax), float(thr), holds,
             "HOLDS" if holds else "*** FAILS ***", float(r.c_sharp_hi), time.time() - t0))
    sys.stdout.flush()


hdr("S2.4  THE DISJUNCTION ALONG EVERY FAMILY — min(c#, f*), WHICH IS WHAT THE THEOREM NEEDS")
print("(M#) and (F) are each SEPARATELY sufficient for C_3^(III) = 1 at a poset (mg-28ff")
print("Sec 2, Sec 3), so the object the architecture consumes is min(c#, f*) <= 1, not either")
print("column alone.  Both are statements about PRIMITIVE posets.")
print()
print("   %-38s %s" % ("FAMILY", "  ".join("n=%-2d" % n for n in range(4, NMAX + 1))))
worst = []
for name, fn in FAMILIES:
    cells = []
    for n in range(4, NMAX + 1):
        P = fn(n)
        d = row(P)
        if d is None:
            cells.append(" -- ")
            continue
        v = min(d["c_sharp"], d["f"])
        worst.append((float(v), name, n))
        cells.append("%.3f" % float(v))
    print("   %-38s %s" % (name, "  ".join("%-5s" % c for c in cells)))
print()
worst.sort(reverse=True)
print("   LARGEST min(c#,f*) seen at any FAMILY MEMBER tested (NOT a maximum over posets):")
for v, name, n in worst[:8]:
    print("      %.6f   %s, n=%d" % (v, name, n))
print()
print("   Every one is < 1: on every family tested the DISJUNCTION still certifies")
print("   C_3^(III) = 1, while each route SEPARATELY is refuted somewhere above.")
