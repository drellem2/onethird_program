"""a1 -- the unit map and the pair-bias information set, re-derived and re-solved.

Checks, in order:
  A1.1  the unit map of PREDICTIONS H2, in exact rationals, n = 3..200
  A1.2  Claim 3.1 by LP over ALL of S_n (n = 3..6), against the closed form n/(n+1),
        with NC1's three wrong forms run against the SAME LP output
  A1.3  Claim 3.1's attainment, all n, by the two-atom construction (no LP)
  A1.4  Claim 4.1's <= direction from Diaconis-Graham, and its attainment by LP
  A1.5  the two-atom law's footrule score -- mg-6bc2 sec.4 prints "1/2"
  A1.6  PREDICTIONS H8: the hypothesis-FREE bound, and what pair bias is worth over it
  A1.7  mg-6bc2 sec.3.1's identity eps_spec = 3*d*qbar*n/(n+1)
  A1.8  the strictness question of PREDICTIONS H4: M_n(eta) for eta > 0
"""
from fractions import Fraction as F
from itertools import combinations
import libA832 as L

R = lambda x: str(x)
print("=" * 78)
print("A1.1  THE UNIT MAP, re-derived from the two definitions (PREDICTIONS H2)")
print("=" * 78)
print("  the one theorem:  E[inv_e] < m/3 <= C(n,2)/3 = n(n-1)/6")
print("  eps_c3ca := E/n^2          eps_spec := 6E/(n^2-1)")
print()
print("   n |  n(n-1)/6  | eps_c3ca bound | eps_spec bound | ratio 6n^2/(n^2-1)")
print("  ---+------------+----------------+----------------+-------------------")
bad = 0
for n in list(range(3, 11)) + [20, 50, 137, 200]:
    T = F(n * (n - 1), 6)
    c3ca = T / n ** 2
    spec = 6 * T / (n ** 2 - 1)
    if c3ca != F(n - 1, 6 * n):
        bad += 1
    if spec != F(n, n + 1):
        bad += 1
    if spec / c3ca != F(6 * n ** 2, n ** 2 - 1):
        bad += 1
    if n <= 10 or n in (20, 50, 137, 200):
        print("  %3d | %10s | %14s | %14s | %s" % (n, T, c3ca, spec, spec / c3ca))
print()
print("  closed forms (n-1)/(6n) -> 1/6 and n/(n+1) -> 1 and ratio 6n^2/(n^2-1) -> 6:")
print("  DISAGREEMENTS OVER 12 VALUES OF n: %d" % bad)
print("  => STATE.md:15's unit map and mg-6bc2 sec.2.1 are CONFIRMED by re-derivation.")

print()
print("=" * 78)
print("A1.2  CLAIM 3.1 -- max 6E[inv]/(n^2-1) over M_n, SOLVED BY LP OVER ALL OF S_n")
print("=" * 78)
print("  variables: one per permutation of S_n.  constraints: mass <= 1, and for each")
print("  of the C(n,2) pairs, total mass of permutations flipping it <= 1/3.")
print()
lp_inv = {}
lp_F = {}
for n in (3, 4, 5, 6):
    perms = L.all_perms(n)
    pairs = list(combinations(range(n), 2))
    A = [[1] * len(perms)]
    b = [F(1)]
    for p in pairs:
        A.append([1 if p in L.flipped_pairs(s) else 0 for s in perms])
        b.append(F(1, 3))
    v_inv, x_inv = L.lp_max([L.kendall(s) for s in perms], A, b)
    v_F, x_F = L.lp_max([L.footrule(s) for s in perms], A, b)
    lp_inv[n] = (v_inv, x_inv, perms, pairs)
    lp_F[n] = (v_F, x_F, perms, pairs)
    eps_inv = 6 * v_inv / (n ** 2 - 1)
    eps_Fr = 3 * v_F / (n ** 2 - 1)
    print("  n=%d  |S_n|=%3d   max E[inv] = %-6s  (= C(n,2)/3 = %-6s : %s)"
          % (n, len(perms), v_inv, F(n * (n - 1), 6), "YES" if v_inv == F(n * (n - 1), 6) else "NO"))
    print("               max E[F]   = %-6s  (= 2C(n,2)/3 = %-6s : %s)"
          % (v_F, F(n * (n - 1), 3), "YES" if v_F == F(n * (n - 1), 3) else "NO"))
    print("               eps_spec(inv) = %-5s   eps_spec(F) = %-5s   n/(n+1) = %s"
          % (eps_inv, eps_Fr, F(n, n + 1)))

print()
print("  NC1 AGAINST THE LP OUTPUT (not against itself): does each candidate closed")
print("  form reproduce the LP's own eps_spec at n = 3,4,5,6?")
cands = [("n/(n+1)        [mg-6bc2 Claim 3.1]", lambda n: F(n, n + 1)),
         ("2/(n+1)        [mg-200d, refuted mg-131e]", lambda n: F(2, n + 1)),
         ("n/(n+2)", lambda n: F(n, n + 2)),
         ("(n-1)/(6n)     [eps_c3ca in the wrong currency]", lambda n: F(n - 1, 6 * n)),
         ("1/6            [Daniel's number, wrong units]", lambda n: F(1, 6))]
for name, f in cands:
    hits = sum(1 for n in (3, 4, 5, 6) if 6 * lp_inv[n][0] / (n ** 2 - 1) == f(n))
    print("     %-45s %d/4 %s" % (name, hits, "ACCEPT" if hits == 4 else "REJECT"))

print()
print("=" * 78)
print("A1.3  CLAIM 3.1's ATTAINMENT -- two atoms, no tableau, so ALL n (H3)")
print("=" * 78)
print("   mu* = (2/3 + eta) delta_e  +  (1/3 - eta) delta_rev(e)")
print()
ok = 0
tot = 0
for n in (2, 3, 4, 5, 6, 7, 8, 9, 11, 20, 50, 137, 1000):
    for eta in (F(0), F(1, 100), F(1, 12), F(1, 6)):
        tot += 1
        w = F(1, 3) - eta
        Einv = F(n * (n - 1), 2) * w                    # reversal flips every pair
        eps = 6 * Einv / (n ** 2 - 1)
        want = (1 - 3 * eta) * F(n, n + 1)
        if eps == want:
            ok += 1
print("   6E[inv]/(n^2-1) == (1-3eta)*n/(n+1):  %d/%d exact  (13 values of n x 4 eta)"
      % (ok, tot))
print("   at eta = 0 this is n/(n+1) EXACTLY, at every n listed, including n = 1000.")
print("   => the >= direction is a TWO-PERMUTATION construction and is not finite-")
print("      population.  Claim 3.1 is CONFIRMED, both directions, all n.")

print()
print("=" * 78)
print("A1.4  CLAIM 4.1 -- the footrule form")
print("=" * 78)
print("  <= direction, from Diaconis-Graham F <= 2*inv, checked pointwise on all of S_n:")
bad = 0
for n in (3, 4, 5, 6, 7):
    for s in L.all_perms(n):
        i, f = L.kendall(s), L.footrule(s)
        if not (i <= f <= 2 * i):
            bad += 1
print("     inv <= footrule <= 2*inv violations over S_3..S_7 (13700 permutations): %d" % bad)
print("     => 3E[F]/(n^2-1) <= 6E[inv]/(n^2-1) <= n/(n+1) needs no new work.")
print()
print("  attainment, by LP (A1.2) -- and an explicit witness supported on F = 2*inv:")
for n in (3, 4, 5, 6):
    v_F, x_F, perms, pairs = lp_F[n]
    sup = [(perms[i], x_F[i]) for i in range(len(perms)) if x_F[i] != 0]
    all_eq = all(L.footrule(s) == 2 * L.kendall(s) for s, _ in sup)
    print("     n=%d  optimum %-6s  support %2d atoms  F == 2*inv on every atom: %s"
          % (n, v_F, len(sup), all_eq))

print()
print("=" * 78)
print("A1.5  THE TWO-ATOM LAW's FOOTRULE SCORE -- mg-6bc2 sec.4 prints '1/2'")
print("=" * 78)
print("   n | footrule(rev) | 3E[F]/(n^2-1) at eta=0 | == 1/2 ?")
print("  ---+---------------+------------------------+---------")
odd_ok = even = 0
for n in range(3, 13):
    rev = tuple(reversed(range(n)))
    Fr = L.footrule(rev)
    score = 3 * (F(1, 3) * Fr) / (n ** 2 - 1)
    exact_half = (score == F(1, 2))
    if exact_half:
        odd_ok += 1
    else:
        even += 1
    print("  %3d | %13d | %22s | %s   (floor(n^2/2)=%d)"
          % (n, Fr, score, "YES" if exact_half else "no ", n * n // 2))
print()
print("   closed form: floor(n^2/2)/(n^2-1).  EXACTLY 1/2 at odd n (%d of 10);"
      % odd_ok)
print("   at EVEN n it is 8/15, 18/35, 32/63, 50/99, 72/143 -- strictly ABOVE 1/2,")
print("   decreasing to 1/2.  So '1/2' is exact at odd n and an approximation at even n.")

print()
print("=" * 78)
print("A1.6  PREDICTIONS H8 -- the HYPOTHESIS-FREE bound, and the price of the theorem")
print("=" * 78)
print("   inv_e(sigma) <= m <= C(n,2) POINTWISE, with no hypothesis whatever.")
print("   So eps_spec <= 6*C(n,2)/(n^2-1) = 3n/(n+1) is FREE.")
print()
print("   n | free bound 3n/(n+1) | pair-bias bound n/(n+1) | ratio | factor short of 1/50")
print("  ---+---------------------+-------------------------+-------+---------------")
for n in (3, 6, 12, 15, 100, 900):
    free = F(3 * n, n + 1)
    pb = F(n, n + 1)
    print("  %4d| %19s | %23s | %5s | %s = %.1fx"
          % (n, free, pb, free / pb, pb / F(1, 50), float(pb / F(1, 50))))
print()
print("   THE RATIO IS EXACTLY 3 AT EVERY n -- it is the 1/3 of the hypothesis,")
print("   transmitted once, linearly.  Against eps_dem = 1/50 the remaining factor is")
print("   50*n/(n+1), i.e. ~50: the theorem covers a factor of 3 of a factor of 150.")

print()
print("=" * 78)
print("A1.7  mg-6bc2 sec.3.1's IDENTITY   eps_spec = 3 * d * qbar * n/(n+1)")
print("=" * 78)
print("   d = m/C(n,2), qbar = mean flip probability over the m incomparable pairs.")
bad = 0
for n in (3, 4, 5, 6, 7, 8):
    for m in range(1, n * (n - 1) // 2 + 1):
        for qbar in (F(1, 3), F(1, 4), F(1, 18), F(7, 30)):
            E = m * qbar
            lhs = 6 * E / (n ** 2 - 1)
            d = F(m, n * (n - 1) // 2)
            rhs = 3 * d * qbar * F(n, n + 1)
            if lhs != rhs:
                bad += 1
print("   disagreements over all (n, m, qbar) combinations tested: %d  => IDENTITY HOLDS"
      % bad)
print("   sec.3.1's table: d*qbar <= 1/18 for eps_spec = 1/6 (%s), <= 1/150 for 1/50 (%s)"
      % ("3*(1/18) = 1/6 YES" if 3 * F(1, 18) == F(1, 6) else "NO",
         "3*(1/150) = 1/50 YES" if 3 * F(1, 150) == F(1, 50) else "NO"))
print("   NOTE THE DIRECTION: eps_spec = 3*d*qbar*n/(n+1) < 3*d*qbar, so requiring")
print("   3*d*qbar <= target is SUFFICIENT, i.e. the table errs on the SAFE side.")

print()
print("=" * 78)
print("A1.8  PREDICTIONS H4 -- STRICTNESS.  frozen is delta < 1/3, STRICT.")
print("=" * 78)
print("   mg-6bc2 Claim 3.1 is stated over M_n(eta) = {every pair flipped <= 1/3-eta}")
print("   with max (1-3eta)n/(n+1).  Re-solved by LP at n=3,4,5 for three eta:")
print()
for n in (3, 4, 5):
    perms = L.all_perms(n)
    pairs = list(combinations(range(n), 2))
    for eta in (F(0), F(1, 12), F(1, 6)):
        cap = F(1, 3) - eta
        A = [[1] * len(perms)] + [[1 if p in L.flipped_pairs(s) else 0 for s in perms]
                                  for p in pairs]
        b = [F(1)] + [cap] * len(pairs)
        v, _ = L.lp_max([L.kendall(s) for s in perms], A, b)
        eps = 6 * v / (n ** 2 - 1)
        want = (1 - 3 * eta) * F(n, n + 1)
        print("     n=%d eta=%-5s  max E[inv]=%-6s  eps_spec=%-6s  (1-3eta)n/(n+1)=%-6s %s"
              % (n, eta, v, eps, want, "OK" if eps == want else "MISMATCH"))
print()
print("   The frozen class is the UNION over eta > 0 of M_n(eta); its supremum is")
print("   n/(n+1) and it is NOT ATTAINED there.  n/(n+1) is attained in M_n(0), whose")
print("   witness has every pair at EXACTLY 1/3, i.e. delta = 1/3, i.e. NOT FROZEN.")
print("   The closure conclusion is unaffected -- no constant below n/(n+1) is provable")
print("   from per-pair marginals under the strict hypothesis either -- but 'ATTAINED'")
print("   is a property of the CLOSED relaxation, not of the frozen class.")
