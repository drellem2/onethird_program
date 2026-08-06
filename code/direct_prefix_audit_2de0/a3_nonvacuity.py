"""mg-2de0 A3 — PRIORITY 2: the NON-VACUITY claim, and whether it is like-for-like.

mg-00b9 reports: at the antichain Lemma B gives 2/3 against a truth of 1/2 (factor 4/3),
while Cheeger at the same input gives Phi* <= sqrt(2), i.e. VACUOUS.

Both numbers verified here. Three separate questions, because they have three answers:

  Q1 is 2/3 right, and is "a truth of 1/2" right?
  Q2 is sqrt(2) right, and is it vacuous?
  Q3 is the comparison LIKE-FOR-LIKE? The direct route bounds min over PREFIXES;
     Cheeger's Phi* is min over ALL CUTS. Those are different numbers in general.

The spectral chain being compared is the corpus's own, cited not re-derived:
    1 - lambda_std <= 3 E[D]/(n^2-1) <= 6 E[inv]/(n^2-1)      STATE.md:130, Op-Form:320
    (Phi*)^2/2 <= 1 - lambda_std                              the SWEEP half, NO ledger row
=>  Phi* <= sqrt(6 E[D]/(n^2-1)).

NOTE ON THE SWEEP HALF: it is asserted in the source as "the usual Cheeger inequalities"
and appears in NO ledger row (mg-2de0 item 4). This script EVALUATES it as stated; it does
not verify it for S_P, and it cannot -- see the README. lambda_std is never computed here.

OPERATOR SCOPE: Phi_P / Delta_1 / footrule, and the corpus's BOUND on 1-lambda_std.
Transport axis. Not Delta_AT, not A(P), not Hodge.
"""

import sys
from fractions import Fraction as F

from lib2de0 import named_posets, all_posets

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
print("A3 — PRIORITY 2: the non-vacuity claim (2/3 vs 1/2 vs sqrt(2))")
print("=" * 78)

POSETS = named_posets(7) + all_posets(4) + all_posets(5)

# ---------------------------------------------------------------------------
print()
print("A3.1  Q1 — the direct number at the antichain, and the 'truth of 1/2'.")
print("      Closed forms verified in A2.5b: E[K_k]=k(n-k)/n, Delta_1(A_k)=max(k,n-k)/n,")
print("      E[D]=(n^2-1)/3. So min_k Delta_1(A_k) = ceil(n/2)/n exactly.")
print()
print(f"       {'n':>3s} {'truth':>7s} {'repaired bnd':>13s} {'mg-00b9 bnd':>13s} "
      f"{'factor(rep)':>12s}")
for n in range(2, 15):
    truth = F(max(1, -((-n) // 2)), n)          # ceil(n/2)/n
    ED = F(n * n - 1, 3)
    rep = 2 * ED / (n * n - 1)                  # = 2/3 always
    stated = 2 * ED / (n * n)
    print(f"       {n:3d} {str(truth):>7s} {str(rep):>13s} {str(stated):>13s} "
          f"{float(rep/truth):>12.4f}")
print()
print("       => 2/3 is CONFIRMED, but only as the REPAIRED bound 2E[D]/(n^2-1).")
print("          mg-00b9's own stated form 2E[D]/n^2 gives 16/27 at n=3, which is BELOW")
print("          the truth 2/3 -- it is not a looser 2/3, it is a FALSE bound (A2.3).")
print("       => 'a truth of 1/2' is an EVEN-n statement. At odd n the truth is")
print("          (n+1)/(2n) > 1/2, and at n=3 it is 2/3 = the bound exactly, so the")
print("          'factor 4/3' is 1.0000 at n=3 and reaches 4/3 only at even n / large n.")
print("          The factor column above is the grain the 4/3 figure needs.")

# ---------------------------------------------------------------------------
print()
print("A3.2  Q2 — sqrt(2), and whether it is vacuous. First: Phi_P(A) <= 1 for EVERY")
print("      cut of every poset, which is what makes any bound >= 1 vacuous.")
bad = tot = 0
from itertools import combinations
for P in POSETS:
    for size in range(1, P.n):
        for S in combinations(range(P.n), size):
            tot += 1
            if P.phi(frozenset(S)) > 1:
                bad += 1
report("Phi_P(A) <= 1 for every cut", bad, tot,
       "per-(poset, cut), exact Fraction comparison",
       f"{len(POSETS)} posets (34 named n=2..7 + all 40 labelled n=4 + all 357 labelled "
       f"n=5), all 2^n-2 proper cuts each = {tot} (poset, cut) pairs")
print("       => any upper bound on Phi* that is >= 1 carries no information.")
print("          sqrt(2) = 1.41421... >= 1, so it is VACUOUS. CONFIRMED.")

print()
print("A3.3  WHERE the sqrt(2) vacuity actually comes from. mg-00b9 attributes the gap")
print("      to the Cheeger SQUARE. Measured at the antichain, the master bound alone:")
print(f"       {'n':>3s} {'3E[D]/(n^2-1)':>14s} {'=> 1-lam_std <=':>16s} "
      f"{'sqrt(6E[D]/(n^2-1))':>20s}")
bad = tot = 0
for n in range(2, 15):
    tot += 1
    ED = F(n * n - 1, 3)
    mb = 3 * ED / (n * n - 1)
    if mb != 1:
        bad += 1
    ch2 = 6 * ED / (n * n - 1)                  # = 2 always; sqrt is sqrt(2)
    print(f"       {n:3d} {str(mb):>14s} {str(mb):>16s} sqrt({str(ch2)}) = "
          f"{float(ch2) ** 0.5:.5f}")
report("master bound == 1 at the antichain, every n", bad, tot,
       "per-n, exact Fraction equality against 1",
       "antichains n=2..14, closed form E[D]=(n^2-1)/3 (verified vs enumeration in A2.5b)")
print("       => THE SPECTRAL CHAIN IS ALREADY VACUOUS AT ITS FIRST STEP. The master")
print("          bound gives 1-lambda_std <= 1, which every lambda_std in [-1,1] already")
print("          satisfies. sqrt(2) is vacuous because its INPUT is vacuous, not because")
print("          the Cheeger square is lossy. This is the corpus's own observation")
print("          (STATE.md:130 'equality at the antichain'; Op-Form:328), re-derived here.")
print("       => mg-00b9's attribution of the antichain gap to 'the Cheeger SQUARE")
print("          (tex:318-324), paid only for the detour' is therefore NOT SUPPORTED AT")
print("          THAT INPUT. The square's price is real and is measured correctly in the")
print("          REQUIREMENT comparison (A4) -- but the antichain cannot show it, because")
print("          the antichain kills the chain one step earlier than the square.")
print("          The conclusion (direct is non-vacuous where spectral is vacuous) SURVIVES;")
print("          the stated REASON does not.")

# ---------------------------------------------------------------------------
print()
print("A3.4  Q3 — IS IT LIKE-FOR-LIKE? min over PREFIXES vs min over ALL CUTS.")
print("      Direct route bounds  m_pre = min_k Delta_1(A_k).")
print("      Cheeger bounds       Phi*  = min over ALL cuts A of Phi_P(A).")
print("      Phi* <= m_pre always (prefixes are a subfamily), so the direct route bounds")
print("      the LARGER, HARDER number. Checked, not assumed:")
bad = tot = 0
strict = 0
for P in POSETS:
    tot += 1
    m_pre = min(P.delta_1_prefix(k) for k in range(1, P.n))
    ps = P.phi_star()
    if ps > m_pre:
        bad += 1
        print(f"       BAD {P.name}: Phi* {ps} > m_pre {m_pre}")
    if ps < m_pre:
        strict += 1
report("Phi* <= min over prefixes", bad, tot,
       "per-poset, exact Fraction comparison",
       f"{len(POSETS)} posets as in A3.2")
print(f"       strictly smaller on {strict} of {tot} posets; EQUAL on {tot - strict}")
print("       => the comparison is CONSERVATIVE IN THE DIRECT ROUTE'S FAVOUR: direct gets")
print("          the better number for the harder quantity. It is not an inflated")
print("          comparison, it is an understated one.")

print()
print("A3.5  and at the ANTICHAIN specifically, Phi* EQUALS min over prefixes, so at the")
print("      one input where mg-00b9 evaluates both, the two routes bound the SAME number")
print("      and the comparison is EXACTLY like-for-like:")
bad = tot = 0
for P in POSETS:
    if not P.name.startswith("antichain"):
        continue
    tot += 1
    m_pre = min(P.delta_1_prefix(k) for k in range(1, P.n))
    if P.phi_star() != m_pre:
        bad += 1
        print(f"       BAD {P.name}: Phi* {P.phi_star()} != m_pre {m_pre}")
report("Phi* == min over prefixes at the antichain", bad, tot,
       "per-n, exact Fraction equality",
       "antichains n=2..7 (n=7 is 5040 linear extensions x 126 cuts)")
print("       => at the antichain the prefix family already attains the global cut")
print("          minimum, so 'prefix vs arbitrary cut' costs NOTHING there. The 2/3 vs")
print("          sqrt(2) comparison is like-for-like AT THE ANTICHAIN, and conservative")
print("          in the direct route's favour everywhere else (A3.4).")

print()
print("A3.6  the SUMMARY table of Priority 2, all three numbers with their status:")
print("       quantity                          value    status")
print("       truth  min_k Delta_1 (even n)      1/2      re-derived here (A3.1)")
print("       truth  min_k Delta_1 (n=3)         2/3      re-derived; NOT 1/2")
print("       direct bound, REPAIRED             2/3      CONFIRMED (A2.5b, A3.1)")
print("       direct bound, mg-00b9 AS WRITTEN   16/27    FALSE at n=3 (A2.3)")
print("       Cheeger bound                      sqrt(2)  CONFIRMED and VACUOUS (A3.2)")
print("       factor direct/truth                4/3      even n only; 1 at n=3 (A3.1)")

print()
print("=" * 78)
print(f"A3 TOTAL BAD: {BAD}")
print("=" * 78)
sys.exit(0 if BAD == 0 else 1)
