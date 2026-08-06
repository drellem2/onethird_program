"""mg-2de0 A4 — PRIORITY 3: the 3/eps_leak claim. Are the two requirements compared AT
THE SAME eps_leak, and is the ratio 3/eps_leak?

mg-2de0's (a), verbatim:
    direct    E[inv_e] <= (eps_leak(1-4beta^2)/4) n^2
    spectral  E[inv_e] <= (eps_spec/6) n^2 = (eps_leak^2/12) n^2
    Ratio 3/eps_leak: 15x weaker at eps_leak=0.20, 150x at 0.02.

FOUR separate questions:
  Q1  Is eps_leak the SAME on both sides? (If not, there is no comparison.)
  Q2  Is the ratio 3/eps_leak, exactly, and at WHICH beta?
  Q3  What does the corpus's own (n^2-1) do to it, vs mg-00b9's n^2?
  Q4  Item (b): direct 2mu vs Cheeger sqrt(6mu), "wins by 1.22/sqrt(mu) >= 2.1 at EVERY
      admissible mu. No crossover. Check this."

The spectral side is the corpus's, cited: E[inv_e] <= (eps_spec/6)(n^2-1)
  (docs/OneThird-lambda-std-Operative-Form.md sec 6.2), with eps_spec = eps_leak^2/2 forced
  by the sweep half (Phi*)^2/2 <= 1-lambda_std at Phi* = eps_leak.
The direct side is Lemma B, in BOTH forms: mg-00b9's as written, and the A2.5 repair.

OPERATOR SCOPE: eps_spec is the TRANSPORT gap parameter (1-lambda_std <= eps_spec, the
OPERATIVE form of mg-88bd/mg-e35c at STATE.md:132), eps_leak the leakage/Delta_1 parameter.
Transport axis throughout. Not Delta_AT, not Hodge.
"""

import sys
from fractions import Fraction as F

from lib2de0 import denom_exact, denom_claimed, k_range, BETAS

BAD = 0


def report(label, bad, total, grain, population, fatal=True):
    global BAD
    if fatal:
        BAD += bad
    flag = "OK  " if bad == 0 else ("BAD " if fatal else "MEAS")
    print(f"  {flag} {label}: {bad} / {total}")
    print(f"       population: {population}")
    print(f"       grain:      {grain}")


print("=" * 78)
print("A4 — PRIORITY 3: the 3/eps_leak requirement comparison")
print("=" * 78)

# ---------------------------------------------------------------------------
print()
print("A4.1  Q1 — SAME eps_leak? Traced symbol by symbol.")
print("      DIRECT:   deliver min_k Delta_1(A_k) <= eps_leak.")
print("                Lemma B bound <= eps_leak  <=>  E[D] <= 2 eps_leak * denom;")
print("                DG lower half E[inv] >= E[D]/2 is the WRONG direction, so the")
print("                sufficient inv-form uses DG UPPER half E[D] <= 2E[inv]:")
print("                E[inv] <= eps_leak * denom  ==>  bound <= eps_leak.")
print("      SPECTRAL: deliver Phi* <= eps_leak. Sweep half forces 1-lambda_std <=")
print("                eps_leak^2/2 =: eps_spec, then the master bound gives")
print("                E[inv] <= (eps_spec/6)(n^2-1) = eps_leak^2 (n^2-1)/12.")
print("      => BOTH sides are the requirement for the SAME conclusion, `leak parameter")
print("         <= eps_leak`, at the same eps_leak. Q1: YES, SAME eps_leak. The comparison")
print("         is well-posed.")
print("      => BUT the two CONCLUSIONS are not the same strength: direct delivers it for")
print("         a PREFIX, spectral for the minimising ARBITRARY cut. A3.4 measured that")
print("         Phi* <= min over prefixes always, so the direct conclusion is the")
print("         STRONGER one. The comparison understates the direct route.")

# ---------------------------------------------------------------------------
print()
print("A4.2  Q2/Q3 — the exact ratio. Direct budget / spectral budget, as a multiple of")
print("      1/eps_leak. Claimed: 3/eps_leak (mg-00b9's headline), or 3(1-4beta^2)/eps_leak")
print("      if the (1-4beta^2) in its own direct requirement is carried through.")
print()
print("      ratio = [eps_leak * denom(n,beta)] / [eps_leak^2 (n^2-1)/12]")
print("            = (1/eps_leak) * 12 denom(n,beta) / (n^2-1)")
print("      so the eps_leak-free multiplier is  M(n,beta) = 12 denom(n,beta)/(n^2-1).")
print()
print(f"       {'n':>3s} {'beta':>6s} {'M exact (repaired)':>20s} {'M claimed 3(1-4b^2)':>21s}"
      f" {'M headline 3':>13s}")
rows = []
for n in (3, 4, 5, 8, 9, 12, 16, 20):
    for b in (F(0), F(1, 4), F(1, 3)):
        if not k_range(n, b):
            continue
        M_exact = F(12 * denom_exact(n, b), n * n - 1)
        M_claim = 3 * (1 - 4 * b * b)
        rows.append((n, b, M_exact, M_claim))
        print(f"       {n:3d} {str(b):>6s} {str(M_exact):>20s} {str(M_claim):>21s} "
              f"{'3':>13s}")

print()
print("A4.2a is the HEADLINE 3 right? Only at beta=0. Scored:")
bad = tot = 0
for n in range(3, 40):
    tot += 1
    M = F(12 * denom_exact(n, F(0)), n * n - 1)
    if M < 3:
        bad += 1
report("M(n,0) >= 3  (headline 3/eps_leak is ATTAINED at beta=0)", bad, tot,
       "per-n, exact Fraction comparison against 3",
       "n=3..39 at beta=0")
print("       M(n,0) = 12*floor(n^2/4)/(n^2-1) = 3 exactly for ODD n, 3n^2/(n^2-1) > 3")
print("       for EVEN n. So at beta=0 the headline 3/eps_leak is exact (odd n) or")
print("       slightly conservative (even n). CONFIRMED at beta=0.")

print()
print("A4.2b is the headline 3 right at the beta the route's own selling point needs?")
print("      mg-2de0 item (d): the balanced-prefix guarantee min(k,n-k) >= beta_0 n is")
print("      what discharges the GEOMETRIC half of F-bal, 'at a cost of (1-4beta^2) --")
print("      25% at beta=1/4'. At beta=0 there is NO balance guarantee at all: the")
print("      k-range is all of [1,n-1] and the selected k may be 1.")
bad = tot = 0
nonbinding = []
for n in range(4, 40):
    tot += 1
    M = F(12 * denom_exact(n, F(1, 4)), n * n - 1)
    ks = k_range(n, F(1, 4))
    if M >= 3:
        bad += 1
        nonbinding.append((n, ks[0], ks[-1], M))
report("M(n,1/4) >= 3 (headline 3 still available)", bad, tot,
       "per-n, EXACT Fraction comparison against 3 (no float in this verdict)",
       "n=4..39 at beta=1/4", fatal=False)
for (n, lo, hi, M) in nonbinding:
    print(f"       EXCEPTION n={n}: k-range [{lo},{hi}] -- IDENTICAL to the beta=0 range")
    print(f"                 [1,{n-1}], so the beta=1/4 balance restriction is VACUOUS")
    print(f"                 at this n and M = {M} >= 3 for that reason, not because the")
    print(f"                 headline survives a real balance constraint.")
print("       and the same measurement for n >= 5, where the window actually binds:")
bad2 = tot2 = 0
for n in range(5, 40):
    tot2 += 1
    if F(12 * denom_exact(n, F(1, 4)), n * n - 1) >= 3:
        bad2 += 1
report("M(n,1/4) >= 3 for n >= 5 (window binds)", bad2, tot2,
       "per-n, exact Fraction comparison against 3",
       "n=5..39 at beta=1/4")
print("       => THE HEADLINE FACTOR AND THE BALANCE GUARANTEE CANNOT BOTH BE CLAIMED.")
print("          At beta=1/4 the honest multiplier is 3*(3/4) = 9/4 = 2.25, so:")
for eps, name in ((F(1, 5), "0.20 (mg-e35c F5 calibration)"), (F(1, 50), "0.02")):
    print(f"          eps_leak={name}: headline {float(3/eps):.1f}x  vs  "
          f"beta=1/4 honest {float(F(9,4)/eps):.2f}x")
print("       => mg-00b9's own (a) writes (1-4beta^2) INTO the direct requirement and then")
print("          reports the ratio WITHOUT it. That is the one place the comparison is")
print("          across different parameter settings -- not in eps_leak (Q1: same), but")
print("          in beta.")

print()
print("A4.2c Q3 — the n^2 vs (n^2-1) rendering. mg-00b9 writes the SPECTRAL requirement")
print("      as (eps_spec/6) n^2; the corpus has (eps_spec/6)(n^2-1).")
bad = tot = 0
for n in range(3, 40):
    tot += 1
    if not F(n * n - 1) < F(n * n):
        bad += 1
report("(n^2-1) < n^2, so the corpus form is STRICTER", bad, tot,
       "per-n, exact", "n=3..39")
print("       => mg-00b9's rendering gives the spectral route a LARGER budget than the")
print("          corpus does, i.e. it UNDERSTATES the spectral requirement and therefore")
print("          understates its own advantage. An error AGAINST mg-00b9's conclusion.")
print("          Direction confirmed; magnitude O(1/n^2).")

# ---------------------------------------------------------------------------
print()
print("A4.3  Q4 — item (b). mu = E[D]/n^2 <= 1/3. direct 2mu vs Cheeger sqrt(6mu).")
print("      Ratio sqrt(6mu)/(2mu) = sqrt(6)/(2 sqrt(mu)) = 1.224745/sqrt(mu).")
print()
print(f"       {'mu':>8s} {'direct 2mu':>11s} {'Cheeger sqrt(6mu)':>18s} "
      f"{'ratio b=0':>10s} {'ratio b=1/4':>12s}")
for mu in (F(1, 3), F(1, 4), F(1, 6), F(1, 10), F(1, 100), F(1, 1000)):
    d0 = 2 * mu
    d4 = 2 * mu / F(3, 4)
    ch = (6 * float(mu)) ** 0.5
    print(f"       {str(mu):>8s} {float(d0):>11.5f} {ch:>18.5f} "
          f"{ch/float(d0):>10.4f} {ch/float(d4):>12.4f}")
print()
print("       => at beta=0 the ratio is 1.2247/sqrt(mu), = 2.1213 at mu=1/3, growing")
print("          without bound as mu -> 0. NO CROSSOVER in mu <= 1/3. (b) CONFIRMED")
print("          AT beta=0, including its '>= 2.1' and 'no crossover'.")
print("       => at beta=1/4 it degrades to 0.9186/sqrt(mu) = 1.5910 at mu=1/3. Still no")
print("          crossover (that would need mu > 0.8438 > 1/3), but the '>= 2.1' figure is")
print("          a beta=0 figure and does not survive the balance guarantee. Same defect")
print("          as A4.2b, same cause.")
bad = tot = 0
for num in range(1, 34):
    mu = F(num, 100)
    tot += 1
    # exact: is (sqrt(6mu))^2 > (2mu/(3/4))^2 ?  i.e. 6mu > (8mu/3)^2
    if not 6 * mu > (F(8, 3) * mu) ** 2:
        bad += 1
report("no crossover at beta=1/4 for mu <= 0.33", bad, tot,
       "per-mu (exact, comparing squares to avoid floats in the verdict)",
       "mu = 1/100 .. 33/100 in steps of 1/100")

print()
print("A4.4  the residual (R) re-pricing of item (f), arithmetic only.")
print("      mg-2de0 (f): direct needs incomparability density D <= 1.5*eps_leak where")
print("      STATE.md:130 records D <= eps_spec. Ratio 1.5 eps_leak / eps_spec with")
print("      eps_spec = eps_leak^2/2 is 3/eps_leak -- the SAME factor as A4.2, as it must")
print("      be, since it is the same square. Checked:")
bad = tot = 0
for den in (5, 10, 20, 50, 100):
    eps = F(1, den)
    tot += 1
    if F(3, 2) * eps / (eps * eps / 2) != 3 / eps:
        bad += 1
report("(f)'s ratio == A4.2's ratio", bad, tot,
       "per-eps_leak, exact Fraction identity",
       "eps_leak in {1/5, 1/10, 1/20, 1/50, 1/100}")
print("       => (f) is NOT an independent second win. It is A4.2's factor re-expressed")
print("          on the density axis. Reporting both as separate gains double-counts one")
print("          Cheeger square.")
print("       => and the n >= 2/eps_spec -> n >= 2/(1.5 eps_leak) claim compares a")
print("          2/eps_spec artifact against a 2/(1.5 eps_leak) artifact -- two DIFFERENT")
print("          formulas. 2/0.02 = 100 and 2/(1.5*0.2) = 6.667 are both correct")
print("          arithmetic, but the '100 -> 6.7' drop mixes eps_spec=0.02 with")
print("          eps_leak=0.20, which are not the same calibration (eps_spec = eps_leak^2/2")
print("          would be 0.02 at eps_leak=0.2). NOT AUDITED FURTHER: item (f) is outside")
print("          this ticket's Priority 1-3 and I did not re-derive the n>=2/eps_spec")
print("          artifact itself.")

print()
print("=" * 78)
print(f"A4 TOTAL BAD: {BAD}")
print("=" * 78)
sys.exit(0 if BAD == 0 else 1)
