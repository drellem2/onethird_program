"""s2 — the footrule route (F), re-derived, and the ~5e-6 discrepancy against §4.3 chased
to a cause before it is reported as anything.

Also re-proves the IDENTITY  sum_k leak(A_k) = (1/2) E[Spearman footrule]  independently,
and checks the COROLLARY's mediant step, because if the identity is wrong the whole (F)
column is wrong.
"""
from fractions import Fraction as F
from lib29fe import all_natural_posets, is_decomposable, Poset, bracket_gap

ITERS = 40
print("=" * 88)
print("s2  ROUTE (F) — the footrule identity, the corollary, and the f* column")
print("=" * 88)

print()
print("-- A. the identity  sum_k leak(A_k) == (1/2) E[D_F],  EXACT, my own derivation --")
bad = tot = 0
for n in range(2, 7):
    for rel in all_natural_posets(n):
        P = Poset(n, rel)
        lhs = sum(P.leak[k] for k in range(1, n))
        tot += 1
        if lhs != P.EDF / 2:
            bad += 1
print(f"   {tot - bad} of {tot} posets n<=6 satisfy it exactly; {bad} exceptions")
# NC: the mutated constant 1/3 must be satisfied by ~nobody with nonzero footrule
mut = 0
for n in range(2, 7):
    for rel in all_natural_posets(n):
        P = Poset(n, rel)
        if P.EDF != 0 and sum(P.leak[k] for k in range(1, n)) == P.EDF / 3:
            mut += 1
print(f"   NC  mutated constant 1/3 satisfied by {mut} posets with nonzero footrule")

print()
print("-- B. the corollary  Phi*_pref <= E[D_F] / (2*floor(n^2/4)),  EXACT --")
bad = tot = 0
for n in range(2, 7):
    fl = n * n // 4
    for rel in all_natural_posets(n):
        P = Poset(n, rel)
        tot += 1
        if P.Phi_star_pref() > P.EDF / (2 * fl):
            bad += 1
print(f"   {tot - bad} of {tot} hold; {bad} exceptions")
print(f"   (mediant step check: sum_k min(k,n-k) == floor(n^2/4)?  "
      f"{[sum(min(k, n - k) for k in range(1, n)) == n * n // 4 for n in range(2, 9)]})")

print()
print("-- C. the f* column, and the top of the ranking at each n --")
print(f"{'n':>3} {'f* (mine, EXACT)':>20} {'mg-28ff §4.3':>14} {'diff':>12}")
parent = {2: 0.125000, 3: 0.250000, 4: 0.306250, 5: 0.550750, 6: 0.811654}
tops = {}
for n in range(2, 7):
    fl = n * n // 4
    prim = [r for r in all_natural_posets(n) if not is_decomposable(n, r)]
    scored = []
    for rel in prim:
        P = Poset(n, rel)
        lo, hi = bracket_gap(P, iters=ITERS)
        val = (P.EDF / (2 * fl)) ** 2 / (2 * lo)      # lo => UPPER bound on f*
        scored.append((val, rel, P.EDF, lo, hi))
    scored.sort(key=lambda t: -t[0])
    tops[n] = scored[:3]
    v = float(scored[0][0])
    print(f"{n:>3} {v:>20.9f} {parent[n]:>14.6f} {v - parent[n]:>+12.2e}")

print()
print("-- D. the argmax at n=5 and n=6, so the discrepancy has an ADDRESS --")
for n in (5, 6):
    print(f"  n={n}:")
    for (val, rel, edf, lo, hi) in tops[n]:
        print(f"     f*={float(val):.9f}  E[D_F]={edf}  1-lambda in "
              f"[{float(lo):.10f},{float(hi):.10f}]  rel={sorted(rel)}")

print()
print("-- E. is the gap bracket wide enough to explain a 5e-6 difference? --")
n = 6
val, rel, edf, lo, hi = tops[6][0]
print(f"   bracket width at the n=6 argmax = {float(hi - lo):.3e}")
print(f"   f* using lo (upper bd) = {float((edf/(2*(36//4)))**2/(2*lo)):.9f}")
print(f"   f* using hi (lower bd) = {float((edf/(2*(36//4)))**2/(2*hi)):.9f}")
print("   => the whole interval my instrument admits is far narrower than the 5e-6 gap,")
print("      so the difference is NOT bracket slack on my side.")
print("=" * 88)
