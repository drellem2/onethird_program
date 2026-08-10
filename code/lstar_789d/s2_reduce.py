"""s2 -- THE REDUCTION.  Three candidate structural routes to (L*), all measured on
the same exhaustive n=7 (F)-failing set, so they can be compared rather than asserted.

THE FRAME.  mg-c50b's obstruction says (L*) cannot come from the five scalars.  What it
does NOT say is where it can come from.  This script proposes and tests three places,
each of which is a property of the MATRIX A = (S_P + S_P^T)/2 and not of any scalar
read off it:

  (R1) PREFIX-TIGHTNESS.   r_k := n*leak(A_k) / (gamma * k(n-k))  is >= 1 at every k --
       that is the test-function bound, a theorem.  Put R := min_k r_k >= 1.  Since the
       prefix indicators are monotone, mu_pref <= gamma * R, so rho <= R and

            R * Delta <= 1     ==>     (L*).

       R is not a function of the five scalars: it reads the whole leak profile against
       gamma.

  (R2) REARRANGEMENT.  Let g be a Fiedler vector and g-down its decreasing rearrangement,
       which is monotone and has the same norm.  Then mu_pref <= E(g-down)/||g||^2, so
       with  W := E(g-down)/E(g) >= rho,

            W * Delta <= 1     ==>     (L*).

       W <= 1 is a RIESZ REARRANGEMENT inequality for the kernel a_ij -- it is what would
       hold verbatim if a_ij were a decreasing function of |i-j|.

  (R3) CONE INVARIANCE (the one with a proof attached).  Say P is STOCHASTICALLY ORDERED
       if for every i and every k,   sum_{j<k} a_ij  >=  sum_{j<k} a_{i+1,j} ,
       i.e. the rows of A are stochastically increasing along the natural labelling.

       THEOREM (proved in the accompanying document, S3 here is its machine check).
       If P is stochastically ordered then rho_P = 1, hence (L*) holds at P outright.

       Proof sketch: stochastic ordering of the rows is exactly the statement that A maps
       nonincreasing vectors to nonincreasing vectors, i.e. that A preserves the monotone
       cone C.  Then so does the lazy matrix (I+A)/2, whose spectrum is in [0,1] with the
       constants at 1.  C modulo constants is a proper cone in R^n/1, the lazy matrix acts
       on that quotient preserving it, and its spectral radius there is (1+lambda_2)/2.
       Krein-Rutman gives an eigenvector for the spectral radius inside the cone, i.e. a
       MONOTONE Fiedler vector; so the monotone cone attains gamma and mu_pref = gamma.

  All three are SUFFICIENT for (L*) and all three are strictly stronger than it, so any
  of them can fail while (L*) survives.  Which ones actually hold on the (F)-failing set
  is a measurement, and it is the measurement this script exists to make.
"""

import sys, time, math
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib789d import (P789, gen_posets, height, jacobi_eig, relabel_natural,
                     fam_chain_plus_points, fam_bipartite_minus)


def prefix_defect(P):
    """R = min_k r_k,  r_k = n*leak_k/(gamma*k(n-k));  also returns min_k r_k's k."""
    n, g = P.n, P.gamma_float()
    best, bk = float("inf"), None
    for k in range(1, n):
        lk = P.LK[k] / P.LE
        r = n * lk / (g * k * (n - k))
        if r < best:
            best, bk = r, k
    return best, bk


def fiedler(P):
    n = P.n
    A = P.Amat()
    L = [[(1.0 if i == j else 0.0) - A[i][j] for j in range(n)] for i in range(n)]
    vals, V = jacobi_eig(L, n)
    return [V[r][1] for r in range(n)], vals[1]


def rearrangement_ratio(P):
    """W = E(g_down)/E(g) with g the Fiedler vector.  >= rho always."""
    g, lam = fiedler(P)
    Eg = P.energy_float(g)
    gd = sorted(g, reverse=True)
    Ed = P.energy_float(gd)
    if Eg <= 1e-15:
        return float("inf")
    return Ed / Eg


def stoch_ordered(P, tol=1e-12):
    """max violation of  sum_{j<k} a_ij >= sum_{j<k} a_{i+1,j}  over i,k.  <=0 means the
    rows of A are stochastically increasing, i.e. A preserves the monotone cone."""
    n = P.n
    A = P.Amat()
    worst = 0.0
    for i in range(n - 1):
        c1 = c2 = 0.0
        for k in range(1, n):
            c1 += A[i][k - 1]
            c2 += A[i + 1][k - 1]
            worst = max(worst, c2 - c1)
    return worst


def tp2_violation(P):
    """max violation of a_ij a_i'j' >= a_ij' a_i'j for i<i', j<j' (TP2)."""
    n = P.n
    A = P.Amat()
    worst = 0.0
    for i in range(n):
        for ip in range(i + 1, n):
            for j in range(n):
                for jp in range(j + 1, n):
                    worst = max(worst, A[i][jp] * A[ip][j] - A[i][j] * A[ip][jp])
    return worst


# =============================================================================
print("=" * 78)
print("S2.1  THE n = 7 (F)-FAILING SET, REBUILT HERE")
print("=" * 78)
t0 = time.time()
FF = []
nearby = 0
for dn in gen_posets(7):
    P = P789(dn, 7)
    if not P.primitive():
        continue
    g = P.gamma_float()
    M = float(P.M())
    if M * M > 2 * g * (1 - 1e-7):
        # exact decision -- (F) fails iff NOT gamma >= M^2/2
        Mx = P.M()
        if not P.gap_ge(Mx * Mx / 2):
            FF.append(dn)
        else:
            nearby += 1
print("  (F)-failing primitive posets on [7]: %d      (%.0fs)" % (len(FF), time.time() - t0))
print("  posets inside the float margin that the EXACT test then cleared: %d" % nearby)
print("  mg-c50b reports 168.  %s" % ("AGREES" if len(FF) == 168 else "*** DISAGREES ***"))
sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S2.2  THE THREE ROUTES ON THAT SET")
print("=" * 78)
rows = []
for dn in FF:
    P = P789(dn, 7)
    g = P.gamma_float()
    D = float(P.Delta())
    mu = P.mu_ub_float()[0]
    R, bk = prefix_defect(P)
    W = rearrangement_ratio(P)
    sv = stoch_ordered(P)
    tv = tp2_violation(P)
    rows.append(dict(dn=dn, gamma=g, Delta=D, rho=mu / g, R=R, W=W, sv=sv, tv=tv,
                     h=height(dn, 7)))

def rep(name, key):
    vals = [r[key] * r["Delta"] for r in rows]
    mx = max(vals)
    arg = rows[vals.index(mx)]["dn"]
    n_ok = sum(1 for v in vals if v <= 1.0)
    print("  %-28s max = %.6f   holds at %d of %d   argmax %s"
          % (name, mx, n_ok, len(rows), str(arg)))
    return mx

print("  quantity * Delta, over the 168 -- each is SUFFICIENT for (L*) if it is <= 1")
m_rho = rep("(L*) itself:  rho*Delta", "rho")
m_R = rep("(R1) prefix:  R*Delta", "R")
m_W = rep("(R2) rearr.:  W*Delta", "W")
print()
print("  (R3) cone invariance -- how many of the 168 have A preserving the monotone cone?")
ci = sum(1 for r in rows if r["sv"] <= 1e-12)
tp = sum(1 for r in rows if r["tv"] <= 1e-12)
rho1 = sum(1 for r in rows if r["rho"] <= 1 + 1e-9)
print("      stochastically ordered rows : %d of %d" % (ci, len(rows)))
print("      totally positive (TP2)      : %d of %d" % (tp, len(rows)))
print("      rho = 1 exactly             : %d of %d   (mg-c50b reports 24)" % (rho1, len(rows)))
print("      stoch-ordered ==> rho = 1   : %s"
      % ("HOLDS at every one" if all(r["rho"] <= 1 + 1e-9 for r in rows if r["sv"] <= 1e-12)
         else "*** VIOLATED -- the theorem in this file's docstring is WRONG ***"))
print("      rho = 1 ==> stoch-ordered   : %s   (the converse; expected FALSE)"
      % ("holds" if all(r["sv"] <= 1e-12 for r in rows if r["rho"] <= 1 + 1e-9) else "FALSE"))
print()
print("  max Delta on the set = %.6f    max rho = %.6f    max R = %.6f   max W = %.6f"
      % (max(r["Delta"] for r in rows), max(r["rho"] for r in rows),
         max(r["R"] for r in rows), max(r["W"] for r in rows)))
print("  heights on the set: %s" % str(sorted(set(r["h"] for r in rows))))
sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S2.3  THE SAME THREE ROUTES WHERE (L*)'s CONCLUSION IS KNOWN TO FAIL")
print("=" * 78)
print("""  chain(n-1) + one isolated point: rho*Delta EXCEEDS 1 from n = 10.  (F) holds there,
  so (L*) is untouched -- but any route that is to prove (L*) must also fail here, or it
  would be proving something false.  This is the negative control for R1/R2/R3.
""")
print("   n | rho*Delta | R*Delta  | W*Delta  | stoch-ord viol | TP2 viol | (F) fails")
for nn in (8, 10, 12, 14, 16):
    dn, n = fam_chain_plus_points(nn - 1, 1)
    P = P789(dn, n)
    g = P.gamma_float()
    D = float(P.Delta())
    mu = P.mu_ub_float()[0]
    R, _ = prefix_defect(P)
    W = rearrangement_ratio(P)
    M = float(P.M())
    print("  %2d | %9.5f | %8.5f | %8.5f | %14.2e | %8.2e | %s"
          % (n, mu * D / g, R * D, W * D, stoch_ordered(P), tp2_violation(P),
             "YES" if M * M > 2 * g else "no"))
sys.stdout.flush()

# =============================================================================
print()
print("=" * 78)
print("S2.4  IS THE (F) HYPOTHESIS WHAT TURNS THE ROUTES ON?")
print("=" * 78)
print("""  If a route only works on the (F)-failing set it must be BECAUSE (F) fails there.
  Measured across ALL primitive posets at n = 6 and n = 7, split by whether (F) fails.
""")
print("  n | set              |  count | max rho*D | max R*D  | max W*D  | stoch-ord frac")
for n in (6, 7):
    buckets = {True: [], False: []}
    for dn in gen_posets(n):
        P = P789(dn, n)
        if not P.primitive():
            continue
        g = P.gamma_float()
        if g <= 1e-13:
            continue
        M = float(P.M())
        ff = M * M > 2 * g
        D = float(P.Delta())
        mu = P.mu_ub_float()[0]
        R, _ = prefix_defect(P)
        W = rearrangement_ratio(P)
        buckets[ff].append((mu * D / g, R * D, W * D, stoch_ordered(P) <= 1e-12))
    for ff in (True, False):
        b = buckets[ff]
        if not b:
            print("  %d | %-16s |      0 |" % (n, "(F) FAILS" if ff else "(F) holds"))
            continue
        print("  %d | %-16s | %6d | %9.5f | %8.5f | %8.5f | %6.1f%%"
              % (n, "(F) FAILS" if ff else "(F) holds", len(b),
                 max(x[0] for x in b), max(x[1] for x in b), max(x[2] for x in b),
                 100.0 * sum(1 for x in b if x[3]) / len(b)))
    sys.stdout.flush()

print()
print("=" * 78)
print("S2.5  SUMMARY")
print("=" * 78)
print("  (L*)  max rho*Delta on the n=7 (F)-failing set = %.6f" % m_rho)
print("  (R1)  max R*Delta   = %.6f   %s" % (m_R, "SUFFICES" if m_R <= 1 else "DOES NOT SUFFICE"))
print("  (R2)  max W*Delta   = %.6f   %s" % (m_W, "SUFFICES" if m_W <= 1 else "DOES NOT SUFFICE"))
print("  (R3)  covers %d of %d posets OUTRIGHT (rho = 1 there, so Delta <= 1 finishes)"
      % (ci, len(rows)))
