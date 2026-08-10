"""s1 -- THE INDEPENDENT RE-DERIVATION the ticket demands.

"onethird_program HAS NO QUALITY GATES ... the n=7 enumeration underneath this entire
ticket is UNVERIFIED BY ANY GATE ... RE-DERIVE THEM INDEPENDENTLY.  A merge is not a
check."   This file is that re-derivation, on an instrument that shares no source line
with `code/sweep_loss_51f4/` (PREDICTIONS.md H3).

EXACTNESS.  Every VERDICT below is exact:
  (F) FAILS         <=>  NOT PSD(Q - (M^2/2) N)                     -- integer matrices
  (M#) HOLDS        <=   2 gamma >= sweep(mu_ub), mu_ub an EXHIBITED vector's exact R
  (M#) FAILS        <=   2 gamma <  sweep(mu_lo), mu_lo a COPOSITIVITY lower bound
Values (c_true, c#, f*, c_or, rho, gamma) are floats and are labelled as such; the
maxima are re-bracketed exactly at their argmax in s2.
"""
import sys, time
from fractions import Fraction
from libc50b import (gen_posets, Poset, height, width, mu_exhaustive, exact_ub_from,
                     m_sharp_exact)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
GBINS = [(0.0, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, 0.30), (0.30, 0.50), (0.50, 1.01)]

print("=" * 78)
print("S1.  POPULATION AND ROUTE CENSUS -- EXHAUSTIVE, n = 2 ..", NMAX)
print("=" * 78)

rows = []
viol = {k: 0 for k in ("gamma<=mu", "mu<=2Phi", "Phi<=M", "M<=Delta", "phi<=Delta",
                       "Delta<=1", "gamma<=2Phi")}
checked = 0
store = {}

for n in range(2, NMAX + 1):
    t0 = time.time()
    tot = prim = 0
    Ffail = Mfail = both = refuse = 0
    mx = {"c_true": (0.0, None), "csharp": (0.0, None), "fstar": (0.0, None),
          "c_or": (0.0, None), "rho": (0.0, None), "LamM": (0.0, None), "LamF": (0.0, None)}
    bins = [dict(cnt=0, rho=0.0, spread=0.0, cs=0.0, fs=0.0, mn=0.0) for _ in GBINS]
    hF, hM, hAll = {}, {}, {}
    Flist, Mlist = [], []
    for dn in gen_posets(n):
        tot += 1
        P = Poset(dn, n)
        if not P.primitive():
            continue
        prim += 1
        g = P.gamma_float()
        Delta = P.Delta()
        Phi = P.Phi_star()
        M = P.M()
        mu, bv = mu_exhaustive(P)
        rho = mu / g if g > 0 else float("inf")
        c_true = float(Phi) ** 2 / (2 * g)
        fstar = float(M) ** 2 / (2 * g)
        dfl = float(Delta)
        csharp = (mu * (2 * dfl - mu) if mu <= dfl else dfl * dfl) / (2 * g)
        c_or = min(csharp, fstar)
        h = height(dn, n)
        hAll[h] = hAll.get(h, 0) + 1

        # ---- the unconditional inequality list (PREDICTIONS.md E7's guard) ----
        checked += 1
        if not (g <= mu + 1e-12):
            viol["gamma<=mu"] += 1
        if not (mu <= 2 * float(Phi) + 1e-12):
            viol["mu<=2Phi"] += 1
        if not (Phi <= M):
            viol["Phi<=M"] += 1
        if not (M <= Delta):
            viol["M<=Delta"] += 1
        if any(P.phi(k) > Delta for k in range(1, n)):
            viol["phi<=Delta"] += 1
        if Delta > 1:
            viol["Delta<=1"] += 1
        if not (g <= 2 * float(Phi) + 1e-12):
            viol["gamma<=2Phi"] += 1

        # ---- EXACT verdicts ----
        f_fail = P.F_fails()
        mu_ub = exact_ub_from(P, bv[0], bv[1]) if bv else None
        mverd, mlo = m_sharp_exact(P, mu_ub)
        if f_fail:
            Ffail += 1
            hF[h] = hF.get(h, 0) + 1
            Flist.append((dn, fstar, csharp, g, h))
        if mverd == "FAILS":
            Mfail += 1
            hM[h] = hM.get(h, 0) + 1
            Mlist.append((dn, csharp, fstar, g, h))
        elif mverd == "REFUSE":
            refuse += 1
        if f_fail and mverd == "FAILS":
            both += 1

        for key, val in (("c_true", c_true), ("csharp", csharp), ("fstar", fstar),
                         ("c_or", c_or), ("rho", rho),
                         ("LamM", csharp / c_true if c_true else 0.0),
                         ("LamF", float(M) / float(Phi))):
            if val > mx[key][0]:
                mx[key] = (val, dn)
        for bi, (lo, hi) in enumerate(GBINS):
            if lo <= g < hi:
                b = bins[bi]
                b["cnt"] += 1
                b["rho"] = max(b["rho"], rho)
                b["spread"] = max(b["spread"], float(M) / float(Phi))
                b["cs"] = max(b["cs"], csharp)
                b["fs"] = max(b["fs"], fstar)
                b["mn"] = max(b["mn"], c_or)
                break
    store[n] = dict(Flist=Flist, Mlist=Mlist, mx=mx)
    rows.append((n, tot, prim, mx["c_true"][0], mx["csharp"][0], mx["fstar"][0],
                 mx["c_or"][0], mx["rho"][0], Ffail, Mfail, both, refuse))
    print()
    print("--- n = %d -------------------------------------------------- %.1fs" % (n, time.time() - t0))
    print("  posets %7d   primitive %7d" % (tot, prim))
    print("  (F)  FAILS at %6d of %6d   [EXACT: one PSD decision per poset]" % (Ffail, prim))
    print("  (M#) FAILS at %6d of %6d   [EXACT: copositivity bracket]" % (Mfail, prim))
    print("  BOTH FAIL  at %6d of %6d   <-- the disjunction" % (both, prim))
    print("  instrument REFUSED a verdict at %d posets" % refuse)
    print("  max c_true %.6f  max c# %.6f  max f* %.6f  max c_or %.6f  max rho %.6f"
          % (mx["c_true"][0], mx["csharp"][0], mx["fstar"][0], mx["c_or"][0], mx["rho"][0]))
    print("  max Lambda_M %.3f   max Lambda_F %.3f" % (mx["LamM"][0], mx["LamF"][0]))
    print("  height distribution   all:%s" % dict(sorted(hAll.items())))
    print("                   (F) fails:%s" % dict(sorted(hF.items())))
    print("                  (M#) fails:%s" % dict(sorted(hM.items())))
    if n >= 6:
        print("  gamma bins  |   count | max rho | max M/Phi* | max c# | max f* | max min")
        for (lo, hi), b in zip(GBINS, bins):
            if not b["cnt"]:
                continue
            print("   [%.2f,%.2f) | %7d | %7.4f | %10.3f | %6.4f | %6.4f | %6.4f"
                  % (lo, hi, b["cnt"], b["rho"], b["spread"], b["cs"], b["fs"], b["mn"]))
    sys.stdout.flush()

print()
print("=" * 78)
print("S1.1  THE TABLE")
print("=" * 78)
print(" n | posets | primitive |  c_true  |    c#    |    f*    |   c_or   | (F)fail (M#)fail BOTH")
for (n, tot, prim, ct, cs, fs, co, rho, Ff, Mf, bo, rf) in rows:
    print("%2d | %6d | %9d | %.6f | %.6f | %.6f | %.6f | %7d %8d %4d"
          % (n, tot, prim, ct, cs, fs, co, Ff, Mf, bo))

print()
print("=" * 78)
print("S1.2  THE UNCONDITIONAL INEQUALITY LIST -- machine-checked at every primitive poset")
print("      (PREDICTIONS.md E7: an inequality that fails here comes OUT of the list")
print("       used by s2's feasibility argument.)")
print("=" * 78)
print("  primitive posets checked: %d" % checked)
for k, v in viol.items():
    print("   %-14s violations: %d   %s" % (k, v, "OK" if v == 0 else "*** NOT AN INEQUALITY ***"))

import pickle
with open("out_s1_store.pkl", "wb") as fh:
    pickle.dump({n: dict(Flist=[(d, a, b, c, e) for (d, a, b, c, e) in v["Flist"]],
                         Mlist=v["Mlist"]) for n, v in store.items()}, fh)
print("\n[stored failure sets for s2 in out_s1_store.pkl]")
