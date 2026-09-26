#!/usr/bin/env python3
"""appA_check.py (mg-3c5b): numeric/exact checks of KSBFT_v7 Appendix A (proof of Lemma 2.3)
and of the 67/242 claim, plus the theta_0 / D_0 arithmetic of Thm 1.3''.

What this checks (EMPIRICAL on grids unless marked EXACT):
  P1  packed sequences built from the DEFINITION (App. A, p.28) exist and their H equals formula (A.2)
  P2  Claim A.1 second inequality H(q,1) >= (5-11q)/2 on q in (0,0.2764]  (the first, H(q,u)>=H(q,1),
      is BFT95 Lem 2.3 = an import; we only spot-check it numerically)
  P3  v_q in (3/5,1) for q in [6/11-T, T]; (A.5) lower bound 1/12 on [1/2,1]
  P4  Claim A.2 (A.6) in both sub-cases, on a grid, for T = 0.2764 and T = 67/242
  P5  final arithmetic EXACT (Fraction): 5-11T+1/22 > 2 iff T < 67/242; = 2 at T = 67/242;
      first branch 5-11T+1/12 > 2 iff T < 37/132
  NEG negative control: at T = 0.2770 > 67/242 the final line FAILS (must print FIRES)
  TH  theta_0, D_0 = 3471; theta_0' = 67/242 - C_BFT, D_0'
Everything is deterministic; runtime < 1 min, single process.
"""
from fractions import Fraction as Fr
from math import sqrt

fails = []
def check(name, ok):
    print(f"{name}: {'ok' if ok else 'FAIL'}")
    if not ok: fails.append(name)

def packed(q, u, kmax=10**6):
    """All (k, case, H) satisfying the App. A definition of a packed pair with parameters (q,u)."""
    sols = []
    Sb = q / u                      # sum_i i*b_i = q*u * sum i(1-u)^(i-1) = q/u  (u in (0,1])
    a = []; sa = 0.0; wa = 0.0          # a_1..a_k, their sum, and sum i*a_i
    for k in range(1, kmax):
        ak = q*u*(1+u)**(k-1); a.append(ak); sa += ak; wa += k*ak
        rem = 1 - q - sa
        if rem < -1e-15: break
        # case (i): k>=2, a_{k+2}=0, u/(1+u) <= a_{k+1}/a_k <= 1
        if k >= 2 and u/(1+u) - 1e-12 <= rem/ak <= 1 + 1e-12:
            H = wa + (k+1)*rem - Sb
            sols.append((k, 'i', H))
        # case (ii): a_{k+1} = a_k + a_{k+2}, 1 <= a_{k+1}/a_k <= 1+u
        a1 = (rem + ak) / 2; a2 = (rem - ak) / 2
        if a2 >= -1e-15 and 1 - 1e-12 <= a1/ak <= 1 + u + 1e-12:
            H = wa + (k+1)*a1 + (k+2)*a2 - Sb
            sols.append((k, 'ii', H))
    return sols

def H_formula(q, u, k, case):
    if case == 'i':
        return k + 1 - q*(1+u)**(k+1)/u
    return k + 1.5 - q*(1+u)**(k-1)*(4*u*u + 5*u + 2)/(2*u)

def H(q, u):
    s = packed(q, u)
    assert s, (q, u)
    return s[0][2]

# ---- P1: definition vs formula (A.2)
worst = 0.0; nsol_hist = {}; spread = 0.0
for i in range(1, 60):
    q = 0.2764 * i / 59
    for j in range(1, 60):
        u = j / 59
        s = packed(q, u)
        nsol_hist[len(s)] = nsol_hist.get(len(s), 0) + 1
        for (k, c, h) in s:
            worst = max(worst, abs(h - H_formula(q, u, k, c)))
        if s:
            hs = [h for (_, _, h) in s]; spread = max(spread, max(hs) - min(hs))
print("P1 #packed solutions per (q,u) histogram:", dict(sorted(nsol_hist.items())))
print(f"P1 max |H(def) - H(A.2)| = {worst:.3e};  max spread of H among multiple solutions = {spread:.3e}")
check("P1 existence (no (q,u) without a packed pair)", 0 not in nsol_hist)
check("P1 formula (A.2) matches definition", worst < 1e-9)
check("P1 H well defined (multiple solutions agree = boundary cases)", spread < 1e-9)

# ---- P2: Claim A.1
w2 = min(H(q, 1.0) - (5 - 11*q)/2 for q in [0.2764*i/2000 for i in range(1, 2001)])
check(f"P2 H(q,1) >= (5-11q)/2 on (0,0.2764]  (min slack {w2:.3e})", w2 >= -1e-12)
w2m = min(H(q, u) - H(q, 1.0) for q in [0.2764*i/120 for i in range(1, 121)] for u in [j/120 for j in range(1, 121)])
check(f"P2 [spot check of import BFT95 Lem 2.3] H(q,u) >= H(q,1)  (min slack {w2m:.3e})", w2m >= -1e-12)

# ---- P3 / P4 / P5 for both thresholds
def vq(q):  # positive root of (1+v)(1+2v) = 1/q  <=>  2v^2+3v+1-1/q = 0
    return (-3 + sqrt(9 - 8*(1 - 1/q))) / 4

for T, tag in ((0.2764, "0.2764"), (67/242, "67/242")):
    lo = 6/11 - T
    vs = [vq(lo + (T - lo)*i/1000) for i in range(1001)]
    check(f"P3[{tag}] p,p' in [{lo:.5f},{T:.5f}] subset (1/5,3/10); v_q in [{min(vs):.4f},{max(vs):.4f}] subset (3/5,1)",
          0.2 < lo and T < 0.3 and 0.6 < min(vs) and max(vs) < 1)
    a5 = min((-3*v*v + 6*v - 2)/(2*v*(1+v)*(1+2*v)) for v in [0.5 + 0.5*i/5000 for i in range(5001)])
    check(f"P3[{tag}] (A.5) (-3v^2+6v-2)/(2v(1+v)(1+2v)) >= 1/12 on [1/2,1]  (min {a5:.6f}, 1/12={1/12:.6f})", a5 >= 1/12 - 1e-12)
    # (A.5) identity H(p,v)-H(p,1) at p = 1/((1+v)(1+2v)) via definition
    idw = max(abs((H(p, v) - H(p, 1.0)) - (-3*v*v + 6*v - 2)/(2*v*(1+v)*(1+2*v)))
              for v in [vq(lo) + (vq(T) - vq(lo))*i/200 for i in range(201)] for p in [1/((1+v)*(1+2*v))])
    # (valid only where p >= 1/5, i.e. v <= 0.8508, since it uses (A.3); the proof needs only p in [lo,T])
    check(f"P3[{tag}] (A.5) identity via definition (max err {idw:.2e})", idw < 1e-9)
    # P4: Claim A.2: for p in [lo,T], t in (v_p, 1]:  H(p,t)-H(p,1) >= p(1-t)/2
    m4 = 1e9
    for i in range(0, 301):
        p = lo + (T - lo)*i/300
        v = vq(p)
        for j in range(1, 301):
            t = v + (1 - v)*j/300
            m4 = min(m4, H(p, t) - H(p, 1.0) - p*(1 - t)/2)
    check(f"P4[{tag}] (A.6) H(p,t)-H(p,1) >= p(1-t)/2 for t > v_p  (min slack {m4:.3e})", m4 >= -1e-12)

C = (5 - sqrt(5)) / 10
Tf = Fr(67, 242)
check("P5 EXACT 5 - 11*(67/242) + 1/22 == 2", 5 - 11*Tf + Fr(1, 22) == 2)
check("P5 EXACT 5 - 11*T + 1/22 > 2 at T = 0.2764 (value %s)" % float(5 - 11*Fr(2764, 10000) + Fr(1, 22)),
      5 - 11*Fr(2764, 10000) + Fr(1, 22) > 2)
check("P5 EXACT first branch threshold: 5 - 11T + 1/12 > 2 iff T < 37/132 (37/132 = %.5f)" % (37/132),
      5 - 11*Fr(37, 132) + Fr(1, 12) == 2)
check("P5 67/242 < 37/132 and 67/242 < 1-1/sqrt2 and 67/242 < 1/e", 67/242 < 37/132 and 67/242 < 1 - 1/sqrt(2) and 67/242 < 0.36787)
# ---- NEG: above 67/242 the chain does not close
TN = Fr(2770, 10000)
neg = not (5 - 11*TN + Fr(1, 22) > 2)
print(f"NEG CONTROL T=0.2770: 5-11T+1/22 = {float(5 - 11*TN + Fr(1, 22)):.5f} <= 2 -> {'FIRES' if neg else 'SILENT'}")
if not neg: fails.append("NEG")

# ---- TH: theta numbers
K = 5 + 3*sqrt(5)
thW = lambda D: C / (K*(D + 1) + 1)
for T, tag in ((0.2764, "theta_0"), (67/242, "theta_0'")):
    th = T - C
    D0 = max(d for d in range(2, 10**5) if thW(d) > th)
    print(f"TH {tag} = {th:.6e};  D_0 = {D0}  (theta_W(D_0) = {thW(D0):.6e}, theta_W(D_0+1) = {thW(D0+1):.6e})")
print(f"TH C_BFT = {C:.9f};  C_BFT/(5+3sqrt5) = {C/K:.6f};  1/(20+2sqrt5) = {1/(20+2*sqrt(5)):.6f}")
check("TH theta_W(D) < 1/((20+2sqrt5)(D+1)) for all D in 2..10^5",
      all(thW(d) < 1/((20 + 2*sqrt(5))*(d + 1)) for d in range(2, 10**5)))

print("ALL OK" if not fails else "FAILED: " + ", ".join(fails))
