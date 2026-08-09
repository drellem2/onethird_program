"""s1 — ITEMS 1 and 2.

Re-derives `c_true` INDEPENDENTLY (item 1: is the increment sequence really monotone
decreasing?) and then SEPARATES the causes of the routes' divergence (item 2: what
licenses blaming "the Cheeger sweep"?).

THE DECOMPOSITION.  Route (M#)'s constant is

    c#(P) = mu_pref (2 Delta_P - mu_pref) / (2(1-lambda_std)).

Write rho = mu_pref/(1-lambda_std) >= 1 — the price of the QUANTIFIER MOVE, i.e. how far
the best MONOTONE vector is from the true optimum.  Substituting mu_pref = rho(1-lambda):

    c#  =  rho * Delta_P  -  rho^2 (1-lambda_std) / 2                       (IDENTITY)

so, since Delta_P <= 1 always,   c#  <=  rho * Delta_P  <=  rho.

Two consequences that are ALGEBRA, not measurement:

  (A) If rho = 1 — i.e. L2's first disjunct holds — then
          c#  =  Delta_P - (1-lambda_std)/2  <  1   at EVERY poset and EVERY n.
      The sharpened sweep, fed an optimal vector, CANNOT reach 1.  Ever.
  (B) Therefore c# > 1 REQUIRES rho > 1/Delta_P > 1.  The only channel through which
      route (M#) can fail is the MONOTONE-CONE RELAXATION.

This script measures the three columns that separate them:

    c_true      the truth                            (exact)
    c_sweepL2   Delta_P - (1-lambda_std)/2           (exact)  = what the sweep costs ALONE
    max Delta_P                                      (exact)

`c_sweepL2` is the whole of the sweep's loss with the cone price switched OFF.  If the
sweep were "what degrades", c_sweepL2 would be the column that climbs to 1.
"""
import sys, time
from fractions import Fraction as F
from lib29fe import all_natural_posets, is_decomposable, Poset, bracket_gap

ITERS = 34


def fmt(x, p=6):
    return f"{float(x):.{p}f}"


print("=" * 90)
print("s1  ITEM 1 (the rising-constants table) and ITEM 2 (what actually degrades)")
print("=" * 90)
print(f"ALL columns EXACT.  Gap bracketed by PSD bisection, {ITERS} dyadic steps")
print(f"(bracket width 2^-{ITERS} ~ {2.0**-ITERS:.2e}); every max below is reported from")
print("the end of the bracket that makes it an UPPER bound on the true value.")
print()

rows = []
for n in range(2, 7):
    t0 = time.time()
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    best_true = None; arg_true = None
    best_sw = None;  arg_sw = None
    best_del = None; arg_del = None
    best_f = None
    for rel in prim:
        P = Poset(n, rel)
        lo, hi = bracket_gap(P, iters=ITERS)
        phi = P.Phi_star_pref()
        # c_true upper bound uses the LOW end of the gap bracket
        ct = phi * phi / (2 * lo)
        if best_true is None or ct > best_true:
            best_true, arg_true = ct, (rel, P.Delta, lo, hi, phi)
        # c_sweepL2 = Delta_P - (1-lambda)/2 : upper bound uses the LOW end too
        sw = P.Delta - lo / 2
        if best_sw is None or sw > best_sw:
            best_sw, arg_sw = sw, (rel, P.Delta, lo)
        if best_del is None or P.Delta > best_del:
            best_del, arg_del = P.Delta, rel
        # footrule route (F)
        fl = n * n // 4
        fs = (P.EDF / (2 * fl)) ** 2 / (2 * lo)
        if best_f is None or fs > best_f:
            best_f = fs
    rows.append((n, len(prim), best_true, best_sw, best_del, best_f, arg_true, arg_sw))
    print(f"  n={n} done ({len(prim)} primitive, {time.time()-t0:.1f}s)")

print()
print("-" * 90)
print("TABLE 1 — c_true, RE-DERIVED INDEPENDENTLY (item 1)")
print("-" * 90)
print(f"{'n':>3} {'primitive':>10} {'c_true':>12} {'delta':>10} {'mg-28ff c_true':>16} {'agree?':>8}")
parent_true = {2: "0.125000", 3: "0.222222", 4: "0.271353", 5: "0.308339", 6: "0.327508"}
prev = None
deltas = []
for (n, k, ct, sw, dl, fs, at, asw) in rows:
    d = "" if prev is None else fmt(ct - prev, 6)
    if prev is not None:
        deltas.append(ct - prev)
    agree = "YES" if fmt(ct) == parent_true[n] else "**NO**"
    print(f"{n:>3} {k:>10} {fmt(ct):>12} {d:>10} {parent_true[n]:>16} {agree:>8}")
    prev = ct

print()
print("  INCREMENTS, to the precision at which the ticket states them:")
print(f"    4 d.p.  {[fmt(d,4) for d in deltas]}")
print(f"    3 d.p.  {[fmt(d,3) for d in deltas]}")
mono = all(deltas[i] > deltas[i + 1] for i in range(len(deltas) - 1))
print(f"    strictly decreasing? {mono}")
print("    NOTE: the ticket body quotes the increments as .097 .049 .037 .019 from the")
print("    3-d.p. values 0.222/0.271/0.308/0.328.  Differencing THOSE gives .049/.037/.020.")
print("    The 6-d.p. table in the document is the one that is self-consistent.")

print()
print("-" * 90)
print("TABLE 2 — THE SEPARATION (item 2).  Which column actually climbs to 1?")
print("-" * 90)
print(f"{'n':>3} {'c_true':>10} {'c_sweepL2':>11} {'max Delta_P':>12} {'f* (F route)':>13}"
      f"  {'mg-28ff c#':>11}")
print("     (truth)   (SWEEP ALONE, cone price OFF)")
parent_csharp = {2: 0.125000, 3: 0.500000, 4: 0.636846, 5: 0.803289, 6: 0.943151}
for (n, k, ct, sw, dl, fs, at, asw) in rows:
    print(f"{n:>3} {fmt(ct):>10} {fmt(sw):>11} {fmt(dl):>12} {fmt(fs):>13}"
          f"  {parent_csharp[n]:>11.6f}")

print()
print("  max Delta_P per n (EXACT rationals):",
      [str(r[4]) for r in rows])
print("  NOTE: max Delta_P is NOT 1-1/n and is NOT attained at the antichain -- I filed")
print("  that guess and it is false (the antichain gives 1-1/n = 3/4 at n=4, but 5/6 is")
print("  reached).  What matters for section 3 is only Delta_P <= 1, which is a probability")
print("  complement (Delta_P = max_i Pr[pos(i) != i]) and needs no population fact at all.")
print()
print("  READ THIS COLUMN-WISE, NOT ROW-WISE:")
print("   * c_sweepL2 = Delta_P - (1-lambda_std)/2 is the constant route (M#) yields when")
print("     the cone price rho is switched OFF (rho = 1, i.e. L2's first disjunct holds).")
print("     It is BOUNDED BY Delta_P <= 1 at every n, ALGEBRAICALLY -- Delta_P is a")
print("     probability complement, so this needs no fact about the population.")
print("   * So the sweep, on its own, CANNOT deliver a constant >= 1 at any n.")
print("   * THE COLUMNS ABOVE ARE MAXIMA AT DIFFERENT POSETS, so differencing them is NOT")
print("     the per-poset cone price.  The pointwise instrument is the floor evaluated at")
print("     c#'s OWN argmax -- 1.0000, 1.0000, 0.9129, 0.8593 at n=3..6 (mg-51f4), i.e. a")
print("     14.1% cone price at n=6.  That correction is mg-51f4's and it is adopted here.")
print("   * Either way the conclusion is the same: the term that can carry c# past 1 is")
print("     rho, not the sweep, and section 4.5 of mg-28ff does not name it.")

print()
print("-" * 90)
print("ARGMAX POSETS (so the claim is falsifiable at a named object)")
print("-" * 90)
for (n, k, ct, sw, dl, fs, at, asw) in rows:
    rel, delta, lo, hi, phi = at
    print(f"  n={n}  c_true argmax: Delta_P={fmt(delta)}  1-lambda in [{fmt(lo,8)},{fmt(hi,8)}]"
          f"  Phi*_pref={phi}")
    print(f"        relation = {sorted(rel)}")
print()
print("=" * 90)
