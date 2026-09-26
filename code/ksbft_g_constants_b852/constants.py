"""mg-b852 -- explicit constants for KSBFT Thm 1.4 (K) and Thm 1.5 = AK25b Thm 1.6 (L(K,eps)).

Every formula below is derived in docs/KSBFT-G-constants.md (section numbers in comments).
Arithmetic is in decimal.Decimal with a huge exponent range, because L* has ~1e29 (or ~1e823)
decimal digits and overflows a float.  All logs natural unless called log10.  No randomness.

Chain for L_AK(w, eps)  (w = width bound, target delta > 1/2 - eps):
  q0   = (2 eps)^(w^2)                        Thm 2.6 -> every x has q(x) >= q0      (sec 3.1)
  S    = 300 / q0^2                           Prop 2.3 explicit: Var <= 294/q^2      (sec 3.2)
  eta  = 1 / (16 sqrt(S+1))                   q <= eta => sigma^2 >= 4(S+1)          (sec 3.3)
  mu   = 1/4                                  Thm 3.1 (mu=1) -> Thm 3.2 (mu/4, 2L)
  sig  = sqrt(300)/eta ; Dw = 3 sig/sqrt(eta) window half-width in (17)            (sec 3.4)
  gam  = 3 mu^3 / 160                         constant in (22)
  B    = ceil(2e/eta) ; K44 = (3B+1)(B+1)     Lemma 4.4 at eps' = eta/2
  TD   = 4 K44 + 1                            T/D
  C    = 2 TD Dw / gam                        spacing constant
  t    = 2 + 2 TD ln(6/(gam eta))             (19)-(21): max chain of ratios
  K32  = 80 C t / (eta mu^2)                  Thm 3.2's K
  K31  = 2 K32 + 2                            Thm 3.1's K
  L    = K31^2                                range bound: pi(P) <= |A||B| < K31^2
"""
from decimal import Decimal as Dm, getcontext
import math

ctx = getcontext(); ctx.prec = 40; ctx.Emax = 10**17; ctx.Emin = -10**17
E = Dm(1).exp(); S3 = Dm(3).sqrt()

def lg(x):  # log10 of a Decimal
    return x.log10()

def width_bound(eps):
    """KSBFT sec 6.4 (and mg-c929 s3): w <= 2 sqrt3 G / eps, G = max(G1, 4A(log A)^2)."""
    eps = Dm(eps)
    G1 = 10 * E * (1 + S3) / eps ** 3
    A = 18432 * S3 / eps ** 3
    G2 = 4 * A * A.ln() ** 2
    assert G2 > A * G2.ln() ** 2          # the 'g <= A log^2 g => g <= 4A log^2 A' step
    return 2 * S3 * max(G1, G2) / eps

def L_AK(w, eps, verbose=False):
    """Returns log10 of each stage (Decimal) for width <= w, target 1/2 - eps."""
    w = Dm(w); eps = Dm(eps)
    log10_q0 = w * w * lg(2 * eps)                     # q0 = (2eps)^(w^2)
    # S = 300/q0^2 ; eta = 1/(16 sqrt(S+1)) ~ q0/(16 sqrt 300) (S+1 ~ S unless w tiny)
    q0 = Dm(10) ** log10_q0 if log10_q0 > -10**6 else None
    if q0 is not None:
        S = 300 / q0 ** 2
        eta = 1 / (16 * (S + 1).sqrt())
        log10_eta = lg(eta)
    else:
        log10_eta = log10_q0 - lg(16 * Dm(300).sqrt())
    mu = Dm(1) / 4
    gam = 3 * mu ** 3 / 160
    # everything below is poly(1/eta); work in log10 with exact leading terms
    # B = ceil(2e/eta) -> K44 = (3B+1)(B+1) <= 3 (2e/eta + 2)^2 ; log form for tiny eta
    def P(a):  # 10^a
        return Dm(10) ** a
    if log10_eta > -300:
        eta_ = P(log10_eta)
        B = Dm(math.ceil(2 * float(E) / float(eta_)))
        K44 = (3 * B + 1) * (B + 1)
        TD = 4 * K44 + 1
        sig = Dm(300).sqrt() / eta_
        Dw = 3 * sig / eta_.sqrt()
        C = 2 * TD * Dw / gam
        t = 2 + 2 * TD * (6 / (gam * eta_)).ln()
        K32 = 80 * C * t / (eta_ * mu * mu)
        K31 = 2 * K32 + 2
        lgL = 2 * lg(K31)
        parts = dict(log10_eta=log10_eta, K44=K44, TD=TD, Dw=Dw, C=C, t=t, K32=K32, K31=K31)
    else:
        # leading order (relative error < 1e-100 in L's log10): x = 1/eta
        lx = -log10_eta
        lnx = lx * Dm(10).ln()
        lg_K44 = lg(Dm(12)) + 2 * lg(E) + 2 * lx          # 3 (2e x)^2
        lg_TD = lg(Dm(4)) + lg_K44
        lg_Dw = lg(3 * Dm(300).sqrt()) + Dm('1.5') * lx
        lg_C = lg(Dm(2)) + lg_TD + lg_Dw - lg(gam)
        lg_t = lg(Dm(2)) + lg_TD + lg((6 / gam).ln() + lnx)
        lg_K32 = lg(Dm(80)) + lg_C + lg_t + lx - 2 * lg(mu)
        lgL = 2 * (lg(Dm(2)) + lg_K32)
        parts = dict(log10_eta=log10_eta, log10_C=lg_C, log10_t=lg_t, log10_K32=lg_K32)
    if verbose:
        for k, v in parts.items():
            print("     %-10s = %s" % (k, fmt(v)))
    return log10_q0, lgL

def fmt(x):
    x = Dm(x)
    if abs(x) < Dm(10) ** 15:
        return "%.6g" % float(x)
    if abs(x) < Dm(10) ** 300:
        return "%.6e" % float(x)
    return ("-" if x < 0 else "") + "10^%.6f" % float(lg(abs(x)))

def show(label, w, eps):
    print("   %s: width <= %s, eps = %s" % (label, fmt(w), fmt(eps)))
    lq, lL = L_AK(w, eps, verbose=True)
    print("     log10(1/q0) = %s ;  log10 L = %s" % (fmt(-lq), fmt(lL)))
    return lL

print("== 1. K (KSBFT Thm 1.4 / sec 6.4)")
K100 = width_bound(Dm(10) ** -100)
eps0 = 1 / E - Dm(1) / 3
K0 = width_bound(eps0)
C_BFT = (5 - Dm(5).sqrt()) / 10
eps12 = 1 / E - C_BFT
K12 = width_bound(eps12)
print("   eps = 1e-100          : w <= %s   (log10 = %s)" % (fmt(K100), fmt(lg(K100))))
print("   eps0 = 1/e - 1/3      : w <= %s   (mg-c929's number, recomputed)" % fmt(K0))
print("   eps = 1/e - C_BFT     : w <= %s   (best deficit usable for Thm 1.2)" % fmt(K12))
print("   printed formula check : (442368/e^4) log^2(18432 sqrt3/e^3) at 1e-100 = %s"
      % fmt(Dm(442368) / Dm(10) ** -400 * (18432 * S3 / Dm(10) ** -300).ln() ** 2))

print("\n== 2. L(K, eps) = L_AK(width <= K-1, eps)")
sixth = Dm(1) / 6
lL4 = show("L(4,1/6)         ", 3, sixth)
lL3 = show("L(3,1/6) (w<=2)  ", 2, sixth)
lLs0 = show("L* with K=K0     ", Dm(math.floor(K0)), sixth)     # width <= K0 (L(K0+1,1/6))
lLs1 = show("L* with K=K_1e-100", K100.to_integral_value(), sixth)
epsT = Dm(1) / 2 - C_BFT
lL12 = show("Thm 1.2 case (b) : width <= K12, eps=1/2-C_BFT", K12.to_integral_value(), epsT)

print("\n== 3. consequences")
for name, lL in [("K0", lLs0), ("K_1e-100", lLs1)]:
    print("   [%s] n0 = 50 L* + 1 : log10 n0 = %s" % (name, fmt(lL + lg(Dm(50)))))
    print("   [%s] n L*/2 vs C n (C = 2.964e17, mg-c929): log10(L*/2 / C) = %s"
          % (name, fmt(lL - lg(Dm(2)) - lg(Dm('2.964e17')))))
    print("   [%s] mg-f218 eps = 0.0236/(L*+1): log10 eps = %s" % (name, fmt(-(lL) + lg(Dm('0.0236')))))
    # mg-d707: (D+1)^(-3(D+1))/12 at D = L*: log10(1/eps) ~ 3 L* log10 L*
    print("   [%s] mg-d707 eps at D=L*: log10 log10 (1/eps) = %s"
          % (name, fmt(lg(Dm(3)) + lL + lg(lL))))
    print("   [%s] paper Thm 1.3 eps at D=L*: log10 log10 (1/eps) = %s"
          % (name, fmt(lg(Dm(4)) + lL + lg(lL))))
print("   [Thm1.2-optimal] L = L_AK(K12, 1/2-C_BFT): log10 L = %s" % fmt(lL12))
print("   [Thm1.2-optimal] mg-f218 eps: log10 eps = %s" % fmt(-lL12 + lg(Dm('0.0236'))))
print("   [Thm1.2-optimal] paper Thm 1.3: log10 log10(1/eps) = %s" % fmt(lg(Dm(4)) + lL12 + lg(lL12)))
p = Dm(16) * Dm(10) ** 18
print("   paper eq (1.5): eps = 3^-3^(1.6e19): log10 log10(1/eps) = %s"
      % fmt(p * lg(Dm(3)) + lg(lg(Dm(3)))))
# L implied by (1.5) if eps = eta_L = (L+1)^(-4(L+1))/4096: 4 L log3 L ~ 3^p
print("   implied L from (1.5) via eta_D: log3 L ~ %s  (vs route: log3 L = %s at K12)"
      % (fmt(p - lg(4 * p * Dm(1)) / lg(Dm(3))), fmt(lL12 / lg(Dm(3)))))
print("   width w needed for 0.7322 w^2 = 1.6e19 (Thm 2.6 floor alone): %s"
      % fmt((p / (-lg(2 * epsT) / lg(Dm(3)))).sqrt()))

print("\n== 4. controls")
# (a) Lemma 4.4 ratio (12) vs brute-force path counts, and the K44 bound, on a grid
from math import comb
bad = 0; worst = 9
for m in range(3, 40, 3):
    for n in range(3, 60, 4):
        for i in range(1, m + 1):
            for j in range(1, n):
                c = lambda l: comb(i - 1 + l, i - 1) * comb(m - i + n - l, m - i)
                for l in range(1, j + 1):
                    lhs = c(l - 1) / c(l)
                    rhs = (1 + (m - i) / (n - l + 1)) / (1 + (i - 1) / l)
                    if abs(lhs - rhs) > 1e-9 * rhs: bad += 1
print("   (12) identity vs exact binomials, m<40,n<60: mismatches = %d  %s" % (bad, "PASS" if bad == 0 else "FAIL"))
# negative control: a wrong (12) (swap i-1 -> i) must mismatch
bad2 = sum(1 for (m, n, i, l) in [(5, 7, 2, 3), (9, 11, 4, 5)]
           if abs(comb(i-1+l-1,i-1)*comb(m-i+n-l+1,m-i)/(comb(i-1+l,i-1)*comb(m-i+n-l,m-i))
                  - (1+(m-i)/(n-l+1))/(1+i/l)) > 1e-9)
print("   negative control (wrong (12)): mismatches = %d  %s" % (bad2, "FIRES" if bad2 == 2 else "DOES NOT FIRE"))
# (b) Lemma 4.4 constant: under hypotheses with K=(3B+1)(B+1), R(l) >= 1-1/(B+1) on (j-B, j]
import random
random.seed(852)
viol = 0; tried = 0
for B in (2, 5, 20):
    K = (3 * B + 1) * (B + 1)
    for _ in range(20000):
        j = K + 1 + random.randrange(3 * K); n = j + K + 1 + random.randrange(3 * K)
        i = 1 + random.randrange(5 * K)
        # choose m-i so that (n-j)/(m-i) < (1+1/K) j/i, near the boundary
        lo = (n - j) * i / ((1 + 1 / K) * j)
        mi = math.floor(lo) + 1 + random.randrange(3)
        m = i + mi
        if not (n - j) / (m - i) < (1 + 1 / K) * j / i: continue
        tried += 1
        for l in range(j - B + 1, j + 1):
            R = (1 + (m - i) / (n - l + 1)) / (1 + (i - 1) / l)
            if R < 1 - 1 / (B + 1): viol += 1
print("   Lemma 4.4 K=(3B+1)(B+1): %d instances, violations = %d  %s" % (tried, viol, "PASS" if viol == 0 else "FAIL"))
# negative control: K too small (K = B) must produce violations
viol2 = 0
for B in (5, 20):
    K = B + 1
    for _ in range(5000):
        j = K + 1 + random.randrange(3 * K); n = j + K + 1 + random.randrange(K)
        i = 5 * j; m = i + max(1, math.floor((n - j) * i / ((1 + 1 / K) * j)) + 1)
        for l in range(j - B + 1, j + 1):
            if (1 + (m - i) / (n - l + 1)) / (1 + (i - 1) / l) < 1 - 1 / (B + 1): viol2 += 1
print("   negative control (K = B+1): violations = %d  %s" % (viol2, "FIRES" if viol2 > 0 else "DOES NOT FIRE"))
# (c) Prop 2.3 explicit (Var <= 294/q^2) and easy direction (Var >= 1/(64 q^2), q<=1/4)
def stats(p):
    s = sum(p); p = [x / s for x in p]
    mu = sum(k * x for k, x in enumerate(p)); v = sum((k - mu) ** 2 * x for k, x in enumerate(p))
    return v, max(p)
worst_up = 0; worst_lo = 1e9
fams = []
for r in [0.1, 0.5, 0.9, 0.99, 0.999]:
    fams.append([r ** k for k in range(20000)])                        # geometric
for N in [1, 5, 50, 500]:
    fams.append([comb(N, k) for k in range(N + 1)])                    # binomial
for a in [3, 30, 300]:
    fams.append([1.0] * a)                                             # uniform
    fams.append([min(k + 1, a - k) for k in range(a)])                 # triangular
for p in fams:
    v, q = stats(p)
    worst_up = max(worst_up, v * q * q)
    if q <= 0.25: worst_lo = min(worst_lo, v * q * q)
print("   Prop 2.3: max Var*q^2 over test families = %.4f (bound 294)  %s" % (worst_up, "PASS" if worst_up <= 294 else "FAIL"))
print("   easy dir: min Var*q^2 (q<=1/4) = %.4f (bound 1/64=0.0156)  %s" % (worst_lo, "PASS" if worst_lo >= 1 / 64 else "FAIL"))
# negative control: a NON-log-concave law (two far atoms + spread) breaks Var <= 294/q^2
p = [0.0] * 200001; p[0] = 0.5; p[-1] = 0.5
v, q = stats(p)
print("   negative control (bimodal, not log-concave): Var*q^2 = %.3g  %s" % (v * q * q, "FIRES" if v * q * q > 294 else "DOES NOT FIRE"))
