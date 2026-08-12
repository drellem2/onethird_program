#!/usr/bin/env python3
"""mg-7564 d3 — A CEILING ON EVERY CHAIN, NOT ONLY THE FOUR ENUMERATED.

mg-76b2 §6 enumerates four chains and says in as many words: "If a reader holds a fifth
reading, the table is where it should be added."  Nobody has added one.  So every
demand-side price in this corpus is an ENUMERATION statement and is open to a fifth chain.

This arm closes that, from an input the corpus already records as PROVEN.

    THE CHEEGER SANDWICH (source :318-324, mg-9461 §5.2 row 1, status PROVEN):

        (Phi*)^2 / 2  <=  1 - lambda_std  <=  2 * Phi*

    The RIGHT half — the easy direction — rearranges to

        Phi*  >=  (1 - lambda_std) / 2                                     (*)

    Phi* is the minimum of Delta_1 over ALL cuts, so EVERY cut, prefix or not,
    has Delta_1 >= (1 - lambda_std)/2.

    Step 5's conclusion is `Delta_1(A_k, A_k^c) <= eps_leak` at SOME prefix.
    By (*) that conclusion is FALSE at every poset with

        1 - lambda_std  >  2 * eps_leak.

    So NO derivation of Step 5's conclusion from `1 - lambda_std <= eps_spec` can be
    sound for eps_spec > 2*eps_leak — whatever route it takes, whatever constants it
    carries, whether or not it pays a Cheeger square.

PROVENANCE OF (*), WHICH MATTERS BECAUSE THE SOURCE .tex IS NOT IN THIS REPOSITORY.
The right half of the sandwich does NOT have to be taken on the source's word.  It
follows from two things this corpus holds directly:

    (a) mg-76b2 Lemma 2.1, `Phi <= 1-rho <= 2*Phi` for every k — PROVEN, and verified
        at 25684 pairs, EXACT, 0 exceptions (mg-76b2 §9 row 2);
    (b) the variational characterisation of lambda_std as the MAXIMUM of the Rayleigh
        quotient on 1-perp, so rho(v) <= lambda_std for every test vector v.

Take v = the centred indicator of a cut A* attaining Phi*.  Then
    1 - lambda_std  <=  1 - rho(1_{A*})  <=  2*Phi(A*)  =  2*Phi*.
So (*) rests on a lemma measured inside this corpus, not only on an unread file.

WHAT THIS IS AND IS NOT.  It is one line of rearrangement on a PROVEN input, and its
whole content is that it is CHAIN-INDEPENDENT.  It is not a new bound on any poset; (*)
is the sandwich's own easy half.  Its NON-VACUITY caveat is stated and checked below
rather than buried: see §C.
"""

from fractions import Fraction as F

import lib7564 as L

Lk = L.EPS_LEAK
ARCH = L.dem_III(Lk, F(1))
CEIL = L.Spec(2 * Lk.v)


def dec(x, p=6):
    return f"{float(x):.{p}f}"


print("=" * 78)
print("mg-7564 d3 — THE CHAIN-INDEPENDENT CEILING")
print("=" * 78)

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("A. THE CEILING")
print("-" * 78)
print(f"   eps_leak                          = {Lk.v} ({dec(Lk.v, 2)})   EMPIRICAL, L4's threshold")
print(f"   CEILING  eps_dem <= 2 * eps_leak  = {CEIL.v} ({dec(CEIL.v, 2)})")
print(f"     in the d*qbar currency          <= {L.dq_from_spec(CEIL)} "
      f"= 1 in {float(1 / L.dq_from_spec(CEIL)):.4g}")
print(f"     as a density (qbar = 1/3)       <= {dec(L.density_from_spec(CEIL), 4)} "
      f"({dec(100 * L.density_from_spec(CEIL), 1)}% of pairs incomparable)")
print(f"   RESIDUAL WALL AT THE CEILING      >= {dec(L.wall(CEIL), 2)}x "
      f"(eps_sup = 1, PROVEN, an EQUALITY)")
print()
print(f"   Against the architecture as written ({ARCH.v}), the ceiling is a relaxation")
print(f"   of at most {dec(CEIL.v / ARCH.v, 2)}x — and NOT 50x, which is what closing")
print("   the wall would need.  The gap does not close from the demand side, and this")
print("   is now a PROOF rather than an exhausted enumeration.")

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("B. THE FOUR ENUMERATED CHAINS ALL RESPECT IT — and it is not tight for any")
print("-" * 78)
ROWS = [
    ("(I)",             L.dem_I(Lk)),
    ("(III) C=1",       L.dem_III(Lk, F(1))),
    ("(II)  g=1",       L.dem_II(Lk, F(1))),
    ("(II)  g=10.1654", L.dem_II(Lk, F(10.1654).limit_denominator(10 ** 6))),
    ("(IV)  c=1",       L.dem_IV(Lk, F(1))),
    ("(IV)  c=0.9258259", L.dem_IV(Lk, F(0.9258259).limit_denominator(10 ** 7))),
]
print(f"{'chain':20} {'eps_dem':>10} {'<= ceiling?':>12} {'headroom to ceiling':>21}")
worst = None
for name, e in ROWS:
    ok = e.v <= CEIL.v
    print(f"{name:20} {dec(e.v):>10} {('yes' if ok else '**NO**'):>12} "
          f"{dec(CEIL.v / e.v, 3) + 'x':>21}")
    if worst is None or e.v > worst[1].v:
        worst = (name, e)
print()
print(f"   The enumeration's own ceiling is {worst[0].strip()} at eps_dem = {worst[1].v}")
print(f"   = eps_leak exactly.  The chain-independent ceiling is 2*eps_leak.")
print("   ==> A FIFTH CHAIN IS WORTH AT MOST 2x MORE THAN CHAIN (IV)'s CEILING,")
print("       AND WOULD LEAVE THE WALL AT 2.5x.  That is the price of the search.")
print()
print("   NEGATIVE CONTROL — a hypothetical chain claiming eps_dem = 3*eps_leak must")
print("   be REFUSED by the ceiling test, or the test is vacuous:")
bogus = L.Spec(3 * Lk.v)
print(f"     bogus chain eps_dem = {dec(bogus.v)}  ceiling test says: "
      f"{'ACCEPT (BUG)' if bogus.v <= CEIL.v else 'REFUSED, as designed'}")

# ---------------------------------------------------------------------------
print("\n" + "-" * 78)
print("C. THE NON-VACUITY CAVEAT, STATED AND NOT BURIED")
print("-" * 78)
print("   The argument shows Step 5's CONCLUSION is false at any poset with")
print(f"   1 - lambda_std > 2*eps_leak = {dec(CEIL.v, 2)}.  The DEMAND is an implication")
print("   over the FROZEN class, so it could still hold vacuously at a larger")
print("   eps_spec if the frozen class contains no poset in the window")
print(f"   ({dec(CEIL.v, 2)}, eps_spec].  Two things to say about that, and they")
print("   both point the same way:")
print()
print("   1. IF the frozen class IS empty in that window, then `frozen ==> 1-lambda_std")
print(f"      <= {dec(CEIL.v, 2)}` is TRUE — which is L1b itself, at eps_spec = {CEIL.v}.")
print("      That is the wall proved, not the demand relaxed, and it is a strictly")
print("      harder statement than anything on the demand ladder.  So this branch")
print("      cannot be assumed; assuming it assumes the open lemma.")
print("   2. IF it is NOT empty, the ceiling BINDS and eps_dem <= 2*eps_leak.")
print()
print("   EITHER WAY the demand side is capped at 2*eps_leak, and either way the")
print("   residual wall is at least " + dec(L.wall(CEIL), 2) + "x.  The disjunction is the result;")
print("   neither branch is a closure.")
print()
print("   ⚠️ AND THE CAP MOVES WITH eps_leak, WHICH ERRS OPTIMISTIC (mg-9461 §4.3).")
print("      At mg-d3c7's required-scope n<=7 ceiling eps_leak <= 1/7 the cap is")
print(f"      {2 * F(1, 7)} = {dec(2 * F(1, 7))} and the wall is at least "
      f"{dec(1 / (2 * F(1, 7)), 2)}x; at the uniform value 0 the cap is 0.")

print("\n" + "=" * 78)
print("d3 COMPLETE")
print("=" * 78)
