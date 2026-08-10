"""s4 -- THEOREM A, and its machine check at corpus scale.

THEOREM A (this ticket).  Let P be a naturally labelled poset on [n] and let
A = (S_P + S_P^T)/2.  Say P is STOCHASTICALLY ORDERED if the rows of A are
stochastically increasing along the labelling:

    (SO)   for every i < n and every k :   sum_{j<=k} a_{i,j}  >=  sum_{j<=k} a_{i+1,j}.

If P is stochastically ordered then  mu_pref(P) = gamma(P).  Hence rho_P = 1 and
mu_pref * Delta_P <= gamma at P outright -- no (F) hypothesis needed.

PROOF.
 (1) (SO) is EXACTLY the statement that A maps the monotone cone C = {f_1 >= ... >= f_n}
     into itself.  For f in C, (Af)_i - (Af)_{i+1} = sum_j u_j f_j with u_j = a_ij -
     a_{i+1,j}; sum_j u_j = 0 because both rows of a doubly stochastic matrix sum to 1,
     so Abel summation gives sum_j u_j f_j = sum_{k<n} U_k (f_k - f_{k+1}) with
     U_k = sum_{j<=k} u_j >= 0, and every term is a product of two nonnegatives.
     (Conversely f = 1_{A_k} in C forces U_k >= 0, so the two statements are equivalent.)
 (2) A' = (I + A)/2 is symmetric doubly stochastic with spectrum in [0,1], the constants
     sitting at 1, and A' C subset C because both I and A preserve C.
 (3) In V = R^n / <1> the image Cbar of C is a PROPER cone: C's lineality space is
     exactly the constants (f and -f both nonincreasing forces f constant), so Cbar is
     closed and pointed, and the strictly decreasing vectors are interior, so it is solid.
     A' descends to Abar on V with Abar Cbar subset Cbar.
 (4) The spectrum of Abar is {(1+lambda_i)/2 : i >= 2} where 1 = lambda_1 >= lambda_2 >=
     ... are the eigenvalues of A.  All of these are >= 0, so the spectral radius of Abar
     is (1 + lambda_2)/2.
 (5) Perron-Frobenius for cone-preserving maps (Krein-Rutman; finite-dimensional form,
     Berman-Plemmons Ch.1 Thm 3.2): a linear map preserving a proper cone has its
     spectral radius as an eigenvalue with an eigenvector IN the cone.  So there is a
     nonzero vbar in Cbar with Abar vbar = ((1+lambda_2)/2) vbar.
 (6) Lift vbar to the representative f in C with sum_i f_i = 0 (C is closed under adding
     constants, so this representative exists and is still nonincreasing).  Then
     A'f = ((1+lambda_2)/2) f + c*1 for some c; pairing with 1 and using 1'A' = 1' gives
     0 = 1'f = c*n, so c = 0 and A f = lambda_2 f.
 (7) f is nonincreasing, centred and nonzero, and its Rayleigh quotient is
     E(f)/||f||^2 = 1 - lambda_2 = gamma.  Since mu_pref is a minimum over the cone and
     mu_pref >= gamma always, mu_pref = gamma.   []

WHAT THIS IS AND IS NOT.  It is a SUFFICIENT structural condition for (L*), uniform in
n, that is invisible to the five scalars -- it reads the whole matrix A.  It is NOT a
proof of (L*): the check below measures how much of the (F)-failing set it covers, and
the answer is small.  It is reported at its true coverage.
"""

import sys, time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import P789, gen_posets, height, fam_chain_plus_points, fam_bipartite_minus


def so_violation(P):
    n, A = P.n, P.Amat()
    worst = 0.0
    for i in range(n - 1):
        c1 = c2 = 0.0
        for k in range(n):
            c1 += A[i][k]
            c2 += A[i + 1][k]
            worst = max(worst, c2 - c1)
    return worst


print("=" * 78)
print("S4.1  THEOREM A CHECKED AT CORPUS SCALE  (every primitive poset, n = 2..7)")
print("=" * 78)
print("""  Two arms per n, and the SECOND is the one that could kill the theorem:
    arm 1  -- of the posets satisfying (SO), how many have rho = 1?   must be ALL.
    arm 2  -- of the posets with rho = 1, how many satisfy (SO)?      expected NOT all,
              because otherwise (SO) would be a restatement rather than a criterion.
""")
print("   n | primitive | (SO) holds |  (SO) => rho=1  | rho=1 count | (SO) is strictly")
print("     |           |            |                 |             | stronger?")
tot_so = tot_prim = 0
BAD = []
for n in (2, 3, 4, 5, 6, 7):
    t0 = time.time()
    nprim = nso = nrho1 = nso_rho1 = 0
    for dn in gen_posets(n):
        P = P789(dn, n)
        if not P.primitive():
            continue
        nprim += 1
        g = P.gamma_float()
        if g <= 1e-13:
            continue
        so = so_violation(P) <= 1e-12
        mu = P.mu_ub_float()[0]
        r1 = (mu / g) <= 1 + 1e-9
        if so:
            nso += 1
            if r1:
                nso_rho1 += 1
            else:
                BAD.append((n, dn, mu / g))
        if r1:
            nrho1 += 1
    tot_so += nso
    tot_prim += nprim
    print("   %d | %9d | %10d | %7d of %-6d| %11d | %s   (%.0fs)"
          % (n, nprim, nso, nso_rho1, nso, nrho1,
             "yes" if nrho1 > nso else "NO -- (SO) == rho=1 here", time.time() - t0))
    sys.stdout.flush()

print()
if BAD:
    print("  *** THEOREM A IS FALSE.  Counterexamples: ***")
    for n, dn, r in BAD[:10]:
        print("      n=%d  %s  rho=%.9f" % (n, str(dn), r))
else:
    print("  THEOREM A holds at every one of the %d primitive posets with (SO), out of"
          % tot_so)
    print("  %d primitive posets at n <= 7.  No exception at any n." % tot_prim)

print()
print("=" * 78)
print("S4.2  (SO) IS NOT VACUOUS AND NOT UNIVERSAL -- the two ways it could be worthless")
print("=" * 78)
print("  chain(n-1) + point, where rho > 1 and (L*)'s CONCLUSION fails from n = 10:")
print("   n | rho      | (SO) violation | (SO) holds")
for nn in (8, 10, 12, 14, 16):
    dn, n = fam_chain_plus_points(nn - 1, 1)
    P = P789(dn, n)
    r = P.mu_ub_float()[0] / P.gamma_float()
    v = so_violation(P)
    print("  %2d | %.6f | %14.6f | %s" % (n, r, v, "yes" if v <= 1e-12 else "NO"))
print()
print("  antichains and near-antichains, where (SO) should hold:")
for n in (4, 6, 8):
    P = P789(tuple([0] * n), n)
    print("   antichain n=%d : (SO) violation %.3e   rho = %.9f"
          % (n, so_violation(P), P.mu_ub_float()[0] / P.gamma_float()))
for a, b in ((3, 3), (4, 4), (4, 3)):
    dn, n = fam_bipartite_minus(a, b, [(a - 1, b - 1)])
    P = P789(dn, n)
    print("   K_{%d,%d} - 1 : (SO) violation %.3e   rho = %.9f"
          % (a, b, so_violation(P), P.mu_ub_float()[0] / P.gamma_float()))

print()
print("=" * 78)
print("S4.3  COVERAGE OF (L*) BY THEOREM A -- reported at its true, small, value")
print("=" * 78)
t0 = time.time()
FF = []
for dn in gen_posets(7):
    P = P789(dn, 7)
    if not P.primitive():
        continue
    g = P.gamma_float()
    M = float(P.M())
    if M * M > 2 * g * (1 - 1e-7):
        Mx = P.M()
        if not P.gap_ge(Mx * Mx / 2):
            FF.append(dn)
cov = sum(1 for dn in FF if so_violation(P789(dn, 7)) <= 1e-12)
r1 = sum(1 for dn in FF if P789(dn, 7).mu_ub_float()[0] / P789(dn, 7).gamma_float() <= 1 + 1e-9)
print("  (F)-failing at n = 7 : %d" % len(FF))
print("  covered by Theorem A : %d  (%.1f%%)" % (cov, 100.0 * cov / len(FF)))
print("  have rho = 1 anyway  : %d  (%.1f%%)  <- the ceiling any rho=1 argument can reach"
      % (r1, 100.0 * r1 / len(FF)))
print("  So Theorem A settles %d of the 168 outright, and CANNOT settle the other %d,"
      % (cov, len(FF) - cov))
print("  because %d of those have rho > 1 strictly and (L*) there is a genuine"
      % (len(FF) - r1))
print("  inequality between two numbers rather than an identity.   (%.0fs)" % (time.time() - t0))
