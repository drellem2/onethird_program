"""mg-5562 -- independent re-computation for docs/AUDIT-mg-b852.md.

Written from the audit's own re-derivation (AUDIT-mg-b852.md s2), NOT from
code/ksbft_g_constants_b852/constants.py: every quantity is carried as a float log10
(no Decimal), with the leading-order algebra done by hand.  Deterministic.

Parts
  A  K from KSBFT p.25's printed closed form w <= (442368/e^4) log^2(18432 sqrt3/e^3)
  B  log10 L_AK(w, eps) by the audit's own leading-order formula, and the route floor
  C  what eq (1.5) requires of L, and which width it would need
  D  Thm 1.2's eps from Thm 1.3'' (mg-f218, audited HOLDS in AUDIT-mg-f218.md)
  E  EMPIRICAL: AK25b Thm 2.6 as used -- q(x) >= (2 eps_x)^(|A||B|) on every x of every
     poset on n <= 6 points (exact extension counts), with a firing negative control
"""
import math, itertools, sys

L10 = math.log10
LOG3 = L10(3)
CBFT = (5 - math.sqrt(5)) / 10
def ok(b): return "PASS" if b else "FAIL"

print("== A. K (printed closed form, p.25)")
def width(e):
    return 442368 / e**4 * math.log(18432 * math.sqrt(3) / e**3) ** 2
def lwidth_tiny(le):   # log10 width for e = 10^le too small for floats
    return L10(442368) - 4 * le + 2 * L10(math.log(18432 * math.sqrt(3)) - 3 * le * math.log(10))
lK = lwidth_tiny(-100)
K0 = width(1 / math.e - 1 / 3)
K12 = width(1 / math.e - CBFT)
print("   eps=1e-100      : log10 K  = %.4f   (doc: 411.337)  %s" % (lK, ok(abs(lK - 411.337) < 1e-3)))
print("   eps=1/e-1/3     : K0       = %.4e (doc: 1.301e14) %s" % (K0, ok(abs(K0 / 1.301e14 - 1) < 1e-3)))
print("   eps=1/e-C_BFT   : K12      = %.4e (doc: 1.944e12) %s" % (K12, ok(abs(K12 / 1.944e12 - 1) < 1e-3)))
print("   monotone: width(e) decreasing on (0, 1/e-C_BFT] -> K12 is the least width case (a) can use:",
      ok(all(width(a) > width(b) for a, b in zip([0.001 * k for k in range(1, 91)], [0.001 * k for k in range(2, 92)]))))

print("\n== B. L_AK(w, eps), leading order in x = 1/eta (audit s2.3)")
# eta = q0/(16 sqrt300) to leading order; D = 3 sqrt300 x^1.5; B=2e x; K44 ~ 3 B^2 = 12 e^2 x^2
# TD ~ 4 K44; C = 2 TD D / gam; t ~ 2 TD ln(6x/gam); K32 = 80 C t x / mu^2; L = (2 K32)^2
mu = 0.25; gam = 3 * mu**3 / 160
def lL(w, eps):
    lq0 = w * w * L10(2 * eps)                       # log10 q0 (negative)
    lx = -lq0 + L10(16 * math.sqrt(300))              # log10 (1/eta)
    lK44 = L10(12 * math.e**2) + 2 * lx
    lTD = L10(4) + lK44
    lD = L10(3 * math.sqrt(300)) + 1.5 * lx
    lC = L10(2) + lTD + lD - L10(gam)
    lt = L10(2) + lTD + L10(math.log(6 / gam) + lx * math.log(10))
    lK32 = L10(80) + lC + lt + lx - 2 * L10(mu)
    return lq0, lx, 2 * (L10(2) + lK32)
for name, w, eps, doc in [("L(4,1/6) w<=3", 3, 1/6, 119.107), ("L(3,1/6) w<=2", 2, 1/6, 87.8825),
                           ("L* w<=K0", math.floor(K0), 1/6, 1.050046e29),
                           ("Thm1.2 w<=K12,eps=1/2-CBFT", round(K12), 0.5 - CBFT, 1.717081e25)]:
    lq0, lx, l = lL(w, eps)
    print("   %-28s log10(1/q0)=%.6g  log10 L=%.7g  (doc %.7g)  rel.diff %.1e" % (name, -lq0, l, doc, abs(l / doc - 1)))
w = math.floor(K0)
print("   L*: log10 L*/K0^2 = %.4f ; bracket [2 log10 3, 13 log10 3] = [%.4f, %.4f]" % (lL(w, 1/6)[2] / w**2, 2 * LOG3, 13 * LOG3))
# degree check: log10 L / log10(1/eta) -> 13 as eta -> 0
for ww in [10, 1000, 10**6, 10**14]:
    lq0, lx, l = lL(ww, 1/6)
    print("   degree in 1/eta at w=%-8g: %.6f" % (ww, l / lx))
# floors, as log3 L, at the least usable width K12 and eps' <= 1/2 - C_BFT
c = -L10(2 * (0.5 - CBFT)) / LOG3
print("   route floor log3 L >= 2 w^2 log3(1/2eps') at K12 : %.4e  (doc: 5.5e24)" % (2 * c * K12**2))
print("   weaker floor (q0 alone, no squaring)  w^2 log3(1/2eps'): %.4e" % (c * K12**2))
print("   trace (this route)  log3 L at K12 : %.4e  (doc 3.6e25)" % (lL(round(K12), 0.5 - CBFT)[2] / LOG3))

print("\n== C. eq (1.5): eps = 3^-3^(1.6e19)")
p = 16e18
# need eta_L = (L+1)^(-4(L+1))/4096 >= eps, i.e. 4(L+1) log3(L+1) + log3 4096 <= 3^p.
# with u = log3(L+1): u + log3(4u) <= p (the 4096 term is negligible) -> u ~ p - log3(4p)
u = p
for _ in range(50): u = p - math.log(4 * u, 3)
print("   (1.5) valid via Thm 1.3 at D=L  <=>  log3(L+1) <= %.10e  (= p - %.2f)" % (u, p - u))
for lab, eps in [("eps'=1/6", 1/6), ("eps'=1/2-C_BFT", 0.5 - CBFT)]:
    cc = -L10(2 * eps) / LOG3
    print("   width needed, %-15s : floor coef 2: %.4e ; q0 alone (coef 1): %.4e" % (lab, math.sqrt(p / (2 * cc)), math.sqrt(p / cc)))
# which section-6 deficit would print a width of 4e9?  bisection on the printed formula
lo, hi = 1e-6, 0.99
for _ in range(200):
    mid = (lo + hi) / 2
    if width(mid) > 4e9: lo = mid
    else: hi = mid
print("   deficit at which p.25's formula gives 4.0e9: %.4f  (> 1/e - C_BFT = %.4f: not usable for Thm 1.2 %s)"
      % (lo, 1 / math.e - CBFT, ok(lo > 1 / math.e - CBFT)))

print("\n== D. Thm 1.2 eps via Thm 1.3'' at D = L12")
th0 = 0.2764 - CBFT
lL12 = lL(round(K12), 0.5 - CBFT)[2]
lthW = L10(CBFT / (5 + 3 * math.sqrt(5))) - lL12       # theta_W(L) ~ C_BFT/((5+3sqrt5)(L+1))
print("   theta_0 = %.4e ; theta_W(L12) = 10^%.7g  -> eps = min = 10^%.4g" % (th0, lthW, lthW))
print("   0.0236/(L+1) check: log10 = %.7g (doc: -1.717081e25)" % (L10(0.0236) - lL12))
lK0 = lL(math.floor(K0), 1/6)[2]
print("   same at L* (1/3 statement): 10^%.7g (doc -1.050046e29)" % (L10(CBFT / (5 + 3 * math.sqrt(5))) - lK0))
print("   paper Thm 1.3 at L12: log10 log10(1/eta) = %.7g" % (lL12 + L10(4 * lL12)))

print("\n== E. EMPIRICAL: Thm 2.6 as used, all posets n <= %s" % (sys.argv[1] if len(sys.argv) > 1 else 6))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
def posets(n):
    # all strict orders on [n] that are compatible with 0<1<..<n-1 (labelled naturally): every
    # poset has such a labelling, so this covers every isomorphism type (with repeats)
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for bits in range(1 << len(pairs)):
        rel = [[False] * n for _ in range(n)]
        for k, (i, j) in enumerate(pairs):
            if bits >> k & 1: rel[i][j] = True
        good = True
        for i, j in pairs:
            if rel[i][j]:
                for k in range(j + 1, n):
                    if rel[j][k] and not rel[i][k]: good = False; break
            if not good: break
        if good: yield rel
def check(n, expo):
    worst = 0; viol = 0; cnt = 0
    for rel in posets(n):
        exts = [p for p in itertools.permutations(range(n))
                if all(not rel[p[b]][p[a]] for a in range(n) for b in range(a + 1, n))]
        E = len(exts)
        pos = [[0] * n for _ in range(n)]          # pos[x][k] = #ext with f(x)=k
        before = [[0] * n for _ in range(n)]       # before[x][y] = #ext with x before y
        for p in exts:
            for k, x in enumerate(p):
                pos[x][k] += 1
                for y in p[k + 1:]: before[x][y] += 1
        for x in range(n):
            inc = [y for y in range(n) if y != x and not rel[x][y] and not rel[y][x]]
            if not inc: continue
            dx = max(min(before[x][y], before[y][x]) / E for y in inc)
            if dx >= 0.5 - 1e-12: continue
            eps = 0.5 - dx
            Dn = [y for y in range(n) if y != x and before[y][x] / E >= 0.5 + eps - 1e-12]
            U = [y for y in range(n) if y != x and before[x][y] / E >= 0.5 + eps - 1e-12]
            A = [a for a in Dn if not any(rel[a][b] for b in Dn)]
            B = [b for b in U if not any(rel[a][b] for a in U)]
            q = max(pos[x]) / E
            e_ = expo(len(A), len(B))
            cnt += 1
            bound = (2 * eps) ** e_
            if q < bound - 1e-12:
                viol += 1
                if expo(len(A), len(B)) == len(A) * len(B) and A and B: raise SystemExit("violation with A,B nonempty: %r x=%d" % (rel, x))
            worst = max(worst, bound / q)
    return cnt, viol, worst
# The literal exponent |A||B| is WRONG when A or B is empty (x minimal or maximal): then the
# bound reads q >= 1.  AK25b's proof then gives prod_b P(x<b) >= (1/2+eps)^|B|, so the right
# exponent is max(|A|,1) max(|B|,1) (<= w^2).  Both are run; the literal one is expected to fail.
for n in range(2, N + 1):
    for lab, ex, want in [("|A||B|        ", lambda a, b: a * b, False),
                          ("max(|A|,1)max(|B|,1)", lambda a, b: max(a, 1) * max(b, 1), True)]:
        cnt, viol, worst = check(n, ex)
        print("   n=%d: %6d (poset,x) cases, delta_x<1/2 ; q>=(2eps)^(%s): violations %5d ; max bound/q %.4f  %s"
              % (n, cnt, lab, viol, worst, ("PASS" if viol == 0 else "FAIL") if want
                 else ("no cases" if cnt == 0 else "literal exponent fails as predicted (all violations have A or B empty)" if viol > 0 else "UNEXPECTED")))
# negative control: the false 'q >= (2 eps)^(1/2)' (exponent below 1) must be violated
cnt, viol, worst = check(N, lambda a, b: 0.5)
print("   negative control q>=(2eps)^(1/2) at n=%d: violations = %d  %s" % (N, viol, "FIRES" if viol > 0 else "DOES NOT FIRE"))
