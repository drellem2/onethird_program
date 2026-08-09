"""b2_census — THE MEASUREMENT THAT DECIDES THE TICKET.

THE THEOREM BEING MEASURED (proved in the document, L2-free):

    For every poset P and EVERY g perp 1 that is monotone along e,
        Phi*_pref^2  <=  R(g) * (2 Delta_P - R(g)),        Delta_P = max_i (1 - (S_P)_ii).

    This is `mg-76b2` Lemma 3.1 with its hypothesis moved: that lemma sweeps the OPTIMAL
    vector and then needs L2 to make it monotone (its Lemma 3.3); this sweeps a MONOTONE
    vector and needs nothing to make it near-optimal, paying for it in the constant.

So `C_3^(III) = 1` — i.e. `Phi*_pref^2 <= 2(1-lambda_std)` — follows with NO L2 whenever

    (M#)   mu_pref (2 Delta_P - mu_pref)  <=  2 (1 - lambda_std),
           mu_pref = min{ R(g) : g perp 1, g monotone along e }.

and more generally `C_3^(III) <= c` whenever the left side is <= 2c(1-lambda_std).
The headline is therefore

    c# = max over PRIMITIVE posets of  mu_pref(2 Delta_P - mu_pref) / (2(1-lambda_std)).

Two directions, two epistemic statuses, kept apart (PREDICTIONS.md E7):
  * the CERTIFICATE direction (there IS a monotone g doing the job) is a theorem at each
    poset and is verified EXACTLY, by rationalising the search's output and calling
    `gap_at_least`, which decides `r <= 1-lambda_std` by exact PSD;
  * the EXTREMAL direction (c# cannot be lowered) rests on a float cone minimisation and
    is labelled a MEASUREMENT.

Decomposable posets are excluded from every ratio: there `1-lambda_std = 0` and
`mu_pref = 0` (the cut-point prefix has zero leak), so `c#` is 0/0.  The architecture's
Step 1 reduces to ordinal-sum-indecomposable posets anyway.
"""

from fractions import Fraction as F

from lib28ff import (all_posets, named_posets, sample_posets, pencil, from_coeffs,
                     is_monotone, rayleigh, gap_at_least, pencil_eigs, cone_min,
                     rationalise, sweep_bound_sq)

TOL = 1e-9
LADDER = [F(1, 2), F(3, 4), F(9, 10), F(1), F(11, 10), F(5, 4), F(3, 2), F(2)]


def analyse(P):
    n = P.n
    Q, N = pencil(P)
    mu2_f = pencil_eigs(Q, N)[0][0]                   # FLOAT 1 - lambda_std
    mupref_f, c_f = cone_min(Q, N)                    # FLOAT search over the monotone cone
    dmax = P.delta_max()
    phi_pref, kstar = P.phi_star_prefix()

    # ---- EXACT: the target itself, Phi*_pref^2 <= 2(1-lambda_std)
    target = gap_at_least(P, phi_pref * phi_pref / 2)

    # ---- EXACT: what the rationalised cone minimiser actually certifies
    bnd = None                                        # exact upper bound on Phi*_pref^2
    if c_f is not None:
        g = from_coeffs(n, rationalise(c_f, den=840))
        assert is_monotone(g), "cone_min vector is not monotone after rationalising"
        if sum(x * x for x in g) != 0:
            bnd = sweep_bound_sq(dmax, rayleigh(P, g))

    return dict(P=P, n=n, mu2_f=mu2_f, mupref_f=mupref_f, dmax=dmax,
                phi_pref=phi_pref, kstar=kstar, target=target, bnd=bnd,
                prim=P.is_primitive())


def csharp(r):
    """The FLOAT measurement mu_pref(2 Delta - mu_pref) / (2(1-lambda_std))."""
    d, m = float(r["dmax"]), r["mupref_f"]
    num = d * d if m >= d else m * (2 * d - m)
    return num / (2 * r["mu2_f"])


def report(rows, label):
    print(f"\n=== {label} — {len(rows)} posets ===")
    tf = [r for r in rows if not r["target"]]
    print(f"[EXACT] target Phi*_pref^2 <= 2(1-lambda_std): "
          f"{len(rows)-len(tf)}/{len(rows)} hold, {len(tf)} fail")
    for r in tf[:4]:
        print(f"        FAIL {sorted(r['P'].rel)}")

    prim = [r for r in rows if r["prim"]]
    print(f"        split: {len(prim)} primitive, {len(rows)-len(prim)} decomposable "
          f"(decomposable carry no ratio: 1-lambda_std = 0)")
    if not prim:
        return

    l2 = [r for r in prim if r["mupref_f"] <= r["mu2_f"] + TOL]
    nl2 = [r for r in prim if r["mupref_f"] > r["mu2_f"] + TOL]
    print(f"[FLOAT] L2's first disjunct (the top standard eigenspace meets the monotone "
          f"cone, i.e. mu_pref == 1-lambda_std): holds {len(l2)}, FAILS {len(nl2)} "
          f"of {len(prim)} primitive")

    rs = sorted(prim, key=csharp, reverse=True)
    print(f"[FLOAT / MEASUREMENT] c# = {csharp(rs[0]):.6f}   over {len(prim)} primitive posets")
    print("        top 5:")
    for r in rs[:5]:
        print(f"          c#={csharp(r):.6f}  n={r['n']}  Delta={float(r['dmax']):.6f}  "
              f"mu_pref={r['mupref_f']:.6f}  1-lam={r['mu2_f']:.6f}  "
              f"L2={'yes' if r['mupref_f'] <= r['mu2_f']+TOL else 'NO '}  "
              f"{sorted(r['P'].rel) if r['P'].rel else '(antichain)'}")
    if nl2:
        print(f"        over the {len(nl2)} primitive posets where L2 FAILS: "
              f"c# = {max(csharp(r) for r in nl2):.6f}")
    if l2:
        print(f"        over the {len(l2)} primitive posets where L2 HOLDS:  "
              f"c# = {max(csharp(r) for r in l2):.6f}  "
              f"(= max(Delta_P - (1-lambda_std)/2) <= 1 by the theorem)")

    print("[EXACT] certificate ladder — a rational monotone g with "
          "R(g)(2Delta-R(g)) <= 2c(1-lambda_std):")
    for c in LADDER:
        good = sum(1 for r in prim
                   if r["bnd"] is not None and gap_at_least(r["P"], r["bnd"] / (2 * c)))
        flag = "  <-- C_3 = 1 here" if c == 1 else ""
        print(f"          c = {str(c):>6}: certified at {good}/{len(prim)} primitive{flag}")


if __name__ == "__main__":
    allrows = []
    for n in range(2, 7):
        rows = [analyse(P) for P in all_posets(n)]
        report(rows, f"ALL POSETS n = {n}")
        allrows += rows

    print("\n" + "=" * 78)
    print("POOLED, n = 2..6, EXHAUSTIVE")
    report(allrows, "pooled n = 2..6")
    prim = [r for r in allrows if r["prim"]]
    print("\nper-n c# (PRIMITIVE only) — PREDICTIONS.md P8 asked whether it RISES:")
    for n in range(2, 7):
        sub = [r for r in prim if r["n"] == n]
        if sub:
            print(f"   n={n}: {len(sub):5d} primitive,  c# = {max(csharp(r) for r in sub):.6f}")

    print("\n=== n = 7 SPOT CHECKS (named families + deterministic sample) ===")
    rows7 = [analyse(P) for P in named_posets(7) + sample_posets(7, 90)]
    report(rows7, "n = 7 named + sample")
