"""a4 -- THEOREM A, audited as a PROOF and then as a machine check.

  THEOREM A (mg-789d).  Let A = (S_P + S_P^T)/2 and say P is STOCHASTICALLY ORDERED
  (SO) if  sum_{j<=k} a_{i,j} >= sum_{j<=k} a_{i+1,j}  for every i < n and every k.
  Then mu_pref(P) = gamma(P), hence rho = 1.

THE PROOF, step by step, with what each step needs.  (This is the audit; 90655
machine agreements do not establish a theorem, and the machine check below is a
CONTROL on the theorem, not its evidence.)

  (1)  (SO) <=> A C subset C, C = {f_1 >= ... >= f_n}.
       (Af)_i - (Af)_{i+1} = sum_j u_j f_j, u_j = a_ij - a_{i+1,j}.  A is doubly
       stochastic so sum_j u_j = 0, hence U_n = 0 and Abel summation gives
       sum_j u_j f_j = sum_{k<n} U_k (f_k - f_{k+1}) + U_n f_n
                     = sum_{k<n} U_k (f_k - f_{k+1}),
       a sum of products of nonnegatives when (SO) holds and f is in C.  Converse:
       f = 1_{A_k} is in C and gives (Af)_i - (Af)_{i+1} = U_k >= 0.       VALID.
       NEEDS: A doubly stochastic (true: S_P is, so its symmetrisation is).

  (2)  A' = (I+A)/2 is symmetric doubly stochastic, spectrum in [0,1], constants at
       1, and A'C subset C (C is a convex cone, I C subset C, A C subset C). VALID.
       NEEDS: spec(A) subset [-1,1], true for symmetric doubly stochastic A.
       WHY THE SHIFT IS THERE: without it the spectral radius of the induced map is
       max(|lambda_2|, |lambda_n|), which need not be lambda_2.  The shift is
       load-bearing and the document states it.

  (3)  In V = R^n/<1> the image K of C is a PROPER cone.  C is closed convex with
       lineality space exactly <1> (f and -f both nonincreasing => f constant), so K
       is closed, pointed and convex; strictly decreasing vectors are interior, so K
       is solid.                                                            VALID.

  (4)  A' preserves <1>, so it induces T on V with spec(T) = {(1+lambda_i)/2 : i>=2},
       all in [0,1], so r(T) = (1+lambda_2)/2.                              VALID.

  (5)  Perron-Frobenius for cone-preserving maps (Krein-Rutman; Berman-Plemmons
       Ch.1 Thm 3.2): T K subset K with K proper => r(T) is an eigenvalue of T with
       an eigenvector in K \\ {0}.  No irreducibility is needed for this form.  VALID.

  (6)  Let f be the centred representative.  A'f = r f + c*1 for some c; pairing with
       1 and using 1'A' = 1' and 1'f = 0 forces c = 0.  So Af = lambda_2 f.   VALID.

  (7)  C is invariant under adding constants, so the centred representative of a class
       in K is itself in C: f is nonincreasing, centred, nonzero.  Its Rayleigh
       quotient is 1 - lambda_2 = gamma, so mu_pref <= gamma; and mu_pref >= gamma
       always because the cone sits inside 1^perp.  Hence mu_pref = gamma.    VALID.

  VERDICT ON THE PROOF: no gap found.  Every step is finite-dimensional and every
  hypothesis it uses (A symmetric doubly stochastic; C closed convex with lineality
  <1>) is discharged.  The theorem is UNIFORM IN n and does not depend on primitivity.

WHAT THE MACHINE CHECK IS FOR.  A theorem cannot be established by agreement, but a
FALSE theorem is usually refuted by one.  Sections below re-run it, with the converse
and a negative control, so the check could have failed.
"""
import sys
import time
from fractions import Fraction
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib5cba import P5, gen_posets, mu_pref_float, gamma_float

FAIL = 0


def arm(name, cond, got=""):
    global FAIL
    print("  [%s] %-62s %s" % ("ok " if cond else "FAIL", name, got))
    if not cond:
        FAIL += 1


def so_holds(p):
    """(SO): every row's prefix sums dominate the next row's, exactly on integers."""
    n = p.n
    AI = p.AI
    for i in range(n - 1):
        s = 0
        for k in range(n):
            s += AI[i][k] - AI[i + 1][k]
            if s < 0:
                return False
    return True


def so_violation(p):
    """The worst prefix-sum deficit, as a float (0 iff (SO) holds)."""
    n = p.n
    AI = p.AI
    worst = 0.0
    for i in range(n - 1):
        s = 0
        for k in range(n):
            s += AI[i][k] - AI[i + 1][k]
            if s < 0:
                worst = max(worst, -s / (2.0 * p.LE))
    return worst


print("=" * 78)
print("a4  THEOREM A -- the proof audited, then machine-checked")
print("=" * 78)
print(__doc__[__doc__.index("THE PROOF"):__doc__.index("WHAT THE MACHINE")])

print("-" * 78)
print("4.1  MACHINE CHECK -- every primitive poset with n <= 7")
print("-" * 78)
tot = 0
soc = {}
rho1 = {}
bad = 0
badex = None
for n in range(2, 8):
    t0 = time.time()
    cnt = c_so = c_r1 = c_so_r1 = 0
    for dn in gen_posets(n):
        p = P5(dn, n)
        if not p.primitive():
            continue
        cnt += 1
        s = so_holds(p)
        g = gamma_float(p)
        mu, _ = mu_pref_float(p)
        r1 = (mu <= g * (1 + 1e-9))
        if s:
            c_so += 1
            if r1:
                c_so_r1 += 1
            else:
                bad += 1
                badex = (n, dn, mu, g)
        if r1:
            c_r1 += 1
    tot += cnt
    soc[n] = (cnt, c_so, c_so_r1, c_r1)
    print("   n=%d  primitive %6d   (SO) %4d   (SO) with rho=1 %4d   rho=1 %5d  (%.0fs)"
          % (n, cnt, c_so, c_so_r1, c_r1, time.time() - t0))
print("   TOTAL primitive posets, n = 2..7: %d" % tot)
arm("the population is 90655 primitive posets at n <= 7", tot == 90655, str(tot))
tso = sum(soc[n][1] for n in soc)
tso6 = sum(soc[n][1] for n in soc if n <= 6)
print("   (SO) holds at %d of them   [n <= 6 subtotal: %d]" % (tso, tso6))
arm("2500 of them satisfy (SO) -- mg-789d's OWN out_s4_theoremA.txt says 2500",
    tso == 2500, str(tso))
arm("the DOCUMENT's '338 of them satisfy (SO)' is the n <= 6 SUBTOTAL, "
    "mis-scoped to n <= 7", tso6 == 338, str(tso6))
arm("THEOREM A holds at every one of them: rho = 1, NO EXCEPTION",
    bad == 0, "%d exceptions %s" % (bad, badex if badex else ""))

print("\n" + "-" * 78)
print("4.2  THE CONVERSE IS FALSE -- so (SO) is a criterion, not a restatement")
print("-" * 78)
for n in (3, 4, 5, 6, 7):
    cnt, c_so, _, c_r1 = soc[n]
    print("   n=%d   rho=1 at %5d   (SO) at %4d   converse fails at %5d"
          % (n, c_r1, c_so, c_r1 - c_so))
arm("n=6: 906 posets have rho = 1 but only 281 satisfy (SO)",
    soc[6][3] == 906 and soc[6][1] == 281, "%d / %d" % (soc[6][3], soc[6][1]))
arm("the converse fails at every n >= 3",
    all(soc[n][3] > soc[n][1] for n in (3, 4, 5, 6, 7)))

print("\n" + "-" * 78)
print("4.3  NEGATIVE CONTROL -- chain(n-1)+point violates (SO), exactly where rho > 1")
print("-" * 78)
for n in range(8, 17, 2):
    dn = tuple([0] + [(1 << i) - 1 for i in range(1, n - 1)] + [0])
    dn = tuple((1 << (i - 1)) - 1 if 1 <= i <= n - 2 else 0 for i in range(n))
    # chain on 0..n-2 plus an isolated point n-1
    dn = tuple(((1 << i) - 1) if i <= n - 2 else 0 for i in range(n))
    p = P5(dn, n)
    g = gamma_float(p)
    mu, _ = mu_pref_float(p)
    print("   n=%2d  chain(%d)+point   (SO) violation %.4f   rho = %.6f"
          % (n, n - 1, so_violation(p), mu / g))
    arm("  n=%d: (SO) FAILS and rho > 1" % n,
        (not so_holds(p)) and mu / g > 1 + 1e-9)

print("\n" + "-" * 78)
print("4.4  COVERAGE OF THE (F)-FAILING SET AT n = 7 -- the honest, small number")
print("-" * 78)
FF = [dn for dn in gen_posets(7) if P5(dn, 7).primitive() and P5(dn, 7).F_fails()]
nso = sum(1 for dn in FF if so_holds(P5(dn, 7)))
nr1 = 0
for dn in FF:
    p = P5(dn, 7)
    if mu_pref_float(p)[0] <= gamma_float(p) * (1 + 1e-9):
        nr1 += 1
print("   (F)-failing at n = 7 : %d      (SO) among them : %d      rho = 1 among them : %d"
      % (len(FF), nso, nr1))
arm("(SO) covers 4 of the 168", nso == 4, str(nso))
arm("the CEILING on any rho=1 argument is 24 of the 168", nr1 == 24, str(nr1))
arm("so 144 of the 168 need a genuine inequality, not an identity", len(FF) - nr1 == 144,
    str(len(FF) - nr1))

print("\n" + "=" * 78)
print("a4 RESULT: %s   (%d failing arms)" % ("ALL ARMS PASS" if FAIL == 0 else "FAILURES", FAIL))
print("=" * 78)
sys.exit(1 if FAIL else 0)
