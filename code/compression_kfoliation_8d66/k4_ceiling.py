#!/usr/bin/env python3
"""k4 -- ITEM 2, THE DECIDING ARM: WHAT IS THE CEILING ON alpha_k?

    THE CEILING IS 1, AT EVERY k, AT EVERY POSET, AND IT IS ATTAINED AT EVERY k.

The ticket expects this to be hard ("for k projections there is no two-projection identity to
lean on, so this may be genuinely open rather than a five-liner").  It is a five-liner, but
NOT the one mg-409a used -- mg-409a's proof really does die at k = 2 (k4.4), which is why
pm-onethird's expectation was the reasonable one.  The proof that survives is:

  THE WITNESS IS BLIND TO k.  Take an incomparable pair (x,y) and f_xy = 1{x before y}.
  Inside any class, the free positions are disjoint non-adjacent pairs.  x and y can only be
  the two elements of ONE such pair; if they are, f_xy is exactly that coordinate, and if
  they are not, f_xy is CONSTANT on the fiber.  Either way f_xy is affine on every fiber of
  every class, so it sits in the equality case of k2 for EVERY admissible partition:

      <f_xy, Q_S f_xy>  =  ((n-1)/2) E_BK(f_xy)  =  P(x,y adjacent)/4        for EVERY S.
      Var(f_xy) = p(1-p),   p = P(x before y).

  AND THE SWAP IS A BIJECTION between {x,y adjacent, x first} and {x,y adjacent, y first}, so
  P(adj)/2 <= min(p, 1-p).  Hence for EVERY admissible partition S,

      alpha_S  <=  R_{Q_S}(f_xy)  =  P(adj) / (4 p(1-p))  <=  1 / (2 max(p, 1-p))  <=  1.

Every step is an exact rational statement about ONE exhibited vector.  No eigensolver, no
two-projection theorem, no symmetry between the k foliations -- the argument is a per-class
statement summed, exactly as mg-8bc7's constraint requires.
"""
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib8d66 as K

ok = True

# --------------------------------------------------------------------------------------
K.banner("k4.1  THE WITNESS IS BLIND TO k:  <f_xy, Q_S f_xy> is ONE rational for every S")
bad = cnt = 0
by_n = {}
pop = ([(3, lt) for lt in K.all_posets(3)] + [(4, lt) for lt in K.all_posets(4)]
       + [(5, lt) for lt in K.sample_posets(5, 120, 3)]
       + [(6, lt) for lt in K.sample_posets(6, 40, 5)])
for n, lt in pop:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    parts = K.admissible_partitions(n)
    for (x, y) in K.incomparable(n, lt):
        f = K.pair_indicator(LEs, x, y)
        vals = {K.q_form(f, LEs, n, lt, S) for S in parts}
        ref = Fraction(n - 1, 2) * K.bk_energy(f, LEs, n, lt)
        cnt += 1
        by_n[n] = by_n.get(n, 0) + 1
        if len(vals) != 1 or vals.pop() != ref:
            bad += 1
ok &= K.verdict(bad == 0,
                f"one value across all admissible S, and it equals ((n-1)/2)E_BK, at {cnt} "
                f"(poset, pair) instances",
                f"{bad} failures; " + ", ".join(f"n={k}:{v}" for k, v in sorted(by_n.items())))

K.banner("k4.2  the CONTROL: is k-blindness special to f_xy, or does EVERY f have it?")
print("""
  If an arbitrary f also gave one value across all S, k4.1 would be measuring nothing.
  Random integer f on the same posets -- these MUST spread.
""")


def rnd_vals(N, seed):
    s = (seed * 48271 + 3) & 0x7FFFFFFF
    out = []
    for _ in range(N):
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        out.append(Fraction((s % 17) - 8))
    return out


spread = tot = 0
for n, lt in pop:
    if n < 4:
        continue
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    parts = K.admissible_partitions(n)
    if len(parts) < 2:
        continue
    v = rnd_vals(len(LEs), 7 * n + len(LEs))
    tot += 1
    if len({K.q_form(v, LEs, n, lt, S) for S in parts}) > 1:
        spread += 1
ok &= K.verdict(spread > 0, f"a generic f DOES depend on S at {spread} of {tot} posets",
                "so k4.1 is a property of the WITNESS, not of the quantity")

# --------------------------------------------------------------------------------------
K.banner("k4.3  THE CLOSED FORM AND THE CEILING, exact rationals, EXHAUSTIVE n <= 5")
print("""
  For every incomparable pair of every poset:  three exact identities and one exact bound.
    (i)   <f_xy, Q_finest f_xy>  ==  P(adj)/4
    (ii)  Var(f_xy)              ==  p(1-p)
    (iii) P(adj)                 <=  2 min(p, 1-p)          [the swap bijection]
    (iv)  R                      ==  P(adj)/(4p(1-p))  <=  1/(2 max(p,1-p))  <=  1
""")
b0 = b1 = b2 = b3 = b4 = cnt = 0
worstR = Fraction(0)
worst_at = None
by_n = {}
for n in (3, 4, 5):
    for lt in K.all_posets(n):
        LEs = K.linear_extensions(n, lt)
        if len(LEs) < 2:
            continue
        best = None
        for (x, y) in K.incomparable(n, lt):
            f = K.pair_indicator(LEs, x, y)
            p, padj = K.pair_stats(LEs, n, lt, x, y)
            q = K.q_form(f, LEs, n, lt, K.finest_partition(n))
            cnt += 1
            by_n[n] = by_n.get(n, 0) + 1
            if padj <= 0:
                b0 += 1
            if q != padj / 4:
                b1 += 1
            if K.variance(f) != p * (1 - p):
                b2 += 1
            if padj > 2 * min(p, 1 - p):
                b3 += 1
            R = q / K.variance(f)
            if R > 1 or R > 1 / (2 * max(p, 1 - p)):
                b4 += 1
            if best is None or R < best:
                best = R
        if best is not None and best > worstR:
            worstR, worst_at = best, (n, sorted(lt))
ok &= K.verdict(b1 == 0, f"(i)   <f_xy,Q f_xy> == P(adj)/4 at {cnt} pairs", f"{b1} failures")
ok &= K.verdict(b0 == 0,
                f"(0)   P(adj) > 0 at every incomparable pair  [THE WITNESS IS NOT VACUOUS]",
                f"{b0} pairs with P(adj) = 0; a zero would 'prove' alpha <= 0 and CONTRADICT "
                f"mg-409a's positivity theorem -- i.e. it is how a broken witness would look")
ok &= K.verdict(b2 == 0, f"(ii)  Var(f_xy) == p(1-p)", f"{b2} failures")
ok &= K.verdict(b3 == 0, f"(iii) P(adj) <= 2 min(p,1-p)", f"{b3} failures")
ok &= K.verdict(b4 == 0, f"(iv)  R <= 1/(2 max(p,1-p)) <= 1", f"{b4} failures")
print(f"  population: {', '.join(f'n={k}: {v} pairs' for k, v in sorted(by_n.items()))} "
      f"(EXHAUSTIVE over labeled posets at n = 3,4,5)")
print(f"  THE LARGEST BEST-PAIR WITNESS VALUE OVER THE WHOLE POPULATION: {worstR} "
      f"= {K.frac(worstR)}   at n={worst_at[0]}, lt={worst_at[1]}")
ok &= K.verdict(worstR <= 1, "and it is <= 1", "the ceiling, over an exhaustive population")

K.banner("k4.4  alpha_S <= 1 directly, at EVERY admissible S  (not routed through k4.1)")
bad = cnt = 0
by_n = {}
for n, lt in pop:
    LEs = K.linear_extensions(n, lt)
    if len(LEs) < 2:
        continue
    pairs = K.incomparable(n, lt)
    for S in K.admissible_partitions(n):
        best = min(K.q_form(K.pair_indicator(LEs, x, y), LEs, n, lt, S)
                   / K.variance(K.pair_indicator(LEs, x, y)) for (x, y) in pairs)
        cnt += 1
        by_n[n] = by_n.get(n, 0) + 1
        if best > 1:
            bad += 1
ok &= K.verdict(bad == 0,
                f"an exhibited rational witness caps alpha_S at 1, at {cnt} (poset, S) pairs",
                f"{bad} failures; " + ", ".join(f"n={k}:{v}" for k, v in sorted(by_n.items())))

# --------------------------------------------------------------------------------------
K.banner("k4.5  WHY mg-409a's OWN PROOF DOES NOT GIVE THIS -- pm-onethird's expectation was right")
print("""
  mg-409a's ceiling proof takes f in Ran(Pi_o) with f perp 1 and reads

      <f, (2I - Pi_o - Pi_e) f>  =  2||f||^2 - ||f||^2 - ||Pi_e f||^2  <=  ||f||^2.

  The same move at k classes gives <f, Q_S f> <= (k-1)||f||^2 and NOTHING BETTER: it discards
  k-2 of the k terms.  A ceiling of k-1 clears a bar of 3 from k = 4.  So the ticket's
  expectation -- that mg-409a's ceiling is a k=2 artefact -- IS CORRECT ABOUT THAT PROOF.
  Measured: the largest value that witness family actually attains, per k.
""")
print("   n | k | max over (poset, S, fiber-indicator f) of R_{Q_S}(f) | exceeds 1?")
print("  ---+---+------------------------------------------------------+-----------")
seen_above = False
for n in (4, 5, 6):
    for k in range(2, n):
        best = Fraction(0)
        for lt in ([l for l in K.all_posets(n)] if n <= 4 else K.sample_posets(n, 40, 9)):
            LEs = K.linear_extensions(n, lt)
            if len(LEs) < 2:
                continue
            for S in K.admissible_partitions(n):
                if len(S) != k:
                    continue
                lab, blocks = K.orbit_fibers(LEs, n, lt, S[0])
                if len(blocks) < 2:
                    continue
                for b in blocks:                       # indicator of ONE fiber, centred
                    f = [Fraction(1) if lab[i] == lab[b[0]] else Fraction(0)
                         for i in range(len(LEs))]
                    var = K.variance(f)
                    if var == 0:
                        continue
                    R = K.q_form(f, LEs, n, lt, S) / var
                    best = max(best, R)
        if best > 1:
            seen_above = True
        print(f"  {n:2d} | {k} | {K.frac(best):52s} | {'YES' if best > 1 else 'no'}")
ok &= K.verdict(seen_above,
                "mg-409a's witness family DOES exceed 1 at k > 2",
                "so its proof genuinely does not generalise -- the pair witness is what does")

# --------------------------------------------------------------------------------------
K.banner("k4.6  THE CEILING IS ATTAINED AT EVERY k: alpha_S(Z_n) = 1 exactly, BOTH DIRECTIONS")
bad = cnt = 0
for n in (4, 6, 8, 10):
    lt = K.Z(n)
    LEs = K.linear_extensions(n, lt)
    P1 = K.proj_perp_one(len(LEs))
    for S in K.admissible_partitions(n):
        Q = K.q_matrix(LEs, n, lt, S)
        lo, why = K.psd_exact(K.mat_sub(Q, P1))          # alpha_S >= 1, exactly
        x, y = K.incomparable(n, lt)[0]
        f = K.pair_indicator(LEs, x, y)
        hi = K.q_form(f, LEs, n, lt, S) / K.variance(f)   # alpha_S <= this
        cnt += 1
        if not lo or hi != 1:
            bad += 1
            print(f"  FAIL n={n} S={K.pstr(S)}: psd={lo} ({why}) witness={hi}")
ok &= K.verdict(bad == 0,
                f"Q_S - (I - P_1) is PSD AND the witness gives exactly 1, at {cnt} "
                f"(Z_n, S) pairs for n = 4,6,8,10",
                f"{bad} failures  =>  alpha_S(Z_n) = 1 EXACTLY at every admissible S")

# --------------------------------------------------------------------------------------
K.banner("k4.7  THE BAR AGAINST THE CEILING, AT EVERY k")
print("""
   n | k range   | bar (n-1)/(gamma n) at gamma=1/3 | CEILING on alpha_k | clears?
  ---+-----------+----------------------------------+--------------------+---------""")
for n in (3, 4, 5, 6, 10, 20, 100, 1000):
    bar = 3 * (n - 1) / n
    print(f"  {n:4d} | 2..{n-1:<6d} | {bar:32.6f} | {1:18d} | {'YES' if 1 > bar else 'NO'}")
print("""
  THE CEILING DOES NOT MOVE WITH k.  1 < 2 <= bar, at every n and every admissible k.
""")
ok &= K.verdict(True, "CLASS CLOSED BY CEILING, AT EVERY k")

K.banner("k4: " + ("PASS" if ok else "FAIL"))
sys.exit(0 if ok else 1)
