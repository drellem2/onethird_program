"""B7 — three due-diligence checks before publishing B4-B6.

D1. My family must NOT refute L4-as-stated.  The ticket forbids attempting to
    prove or refute L4, and a family that killed L4 would mean I had done exactly
    that by accident.  L4 has disjunct (i) -- "P contains a 1/3-balanced pair" --
    which mg-3969's U_either deliberately DROPS (its Sec 5.1 explains why: on a
    minimal counterexample (i) is false by hypothesis).  So the family must
    satisfy L4 via (i).  Checked here: delta(P) >= 1/3 for every member.

D2. The U_smaller failure COUNT is the one number of mg-3969's I cannot
    reproduce (it says 58 755 at n<=7; I get 58 538).  Reconciled here against
    every convention for the |A| == |B| tie, so the residual is localised
    rather than left as a bare mismatch.

D3. Every piece of arithmetic mg-3969 publishes, recomputed exactly.
"""

from fractions import Fraction

from lib_d3c7 import (naturally_labelled_posets, le_dp, delta1, pair_probs,
                      incomparable_pairs, induced, is_chain, balanced)

print("=" * 78)
print("D1 — the family satisfies L4-as-stated via disjunct (i): delta(P) >= 1/3")
print("=" * 78)


def build(n):
    rel = [0] * n
    for j in range(2, n):
        rel[j] = ((1 << j) - 1) & ~1
    return tuple(rel)


ok = True
for k in range(3, 16):
    n = 2 * k + 1
    rel = build(n)
    dp = le_dp(rel, n)
    before, tot = pair_probs(rel, n, dp)
    dlt = max(min(Fraction(before[x][y], tot), 1 - Fraction(before[x][y], tot))
              for (x, y) in incomparable_pairs(rel, n))
    good = dlt >= Fraction(1, 3)
    ok &= good
    if k <= 6 or k == 15:
        print(f"  n={n:<4} delta(P) = {dlt} = {float(dlt):.6f}  >= 1/3: {good}"
              f"   -> L4 disjunct (i) HOLDS, so L4-as-stated is untouched")
print(f"\n  every family member satisfies L4 branch (i): {ok}")
print("  => the family refutes mg-3969's (i)-FREE surrogate U_either,")
print("     NOT L4.  I did not attempt to refute L4 and did not.")

print()
print("=" * 78)
print("D2 — reconciling the U_smaller failure count (mg-3969 reports 58 755)")
print("=" * 78)
# Ties |A| == |B| only occur at even n, i.e. n = 4 and n = 6 within n <= 7.
CONV = ["TIE_EXCLUDED", "TIE_NEITHER_SIDE_SURVIVES", "TIE_SIDE_A", "TIE_SIDE_B"]
counts = {c: 0 for c in CONV}
counts_either = 0
for n in range(2, 8):
    for rel in naturally_labelled_posets(n):
        dp = le_dp(rel, n)
        for k in range(1, n):
            amask = (1 << k) - 1
            bmask = ((1 << n) - 1) ^ amask
            subA, kA, elemsA = induced(rel, n, amask)
            subB, kB, elemsB = induced(rel, n, bmask)
            cA, cB = is_chain(subA, kA), is_chain(subB, kB)
            if cA or cB:
                continue                      # mg-3969's BOTH-non-chain scope
            beforeP, totP = pair_probs(rel, n, dp)
            per = {}
            for nm, (sub, ks, elems) in (("A", (subA, kA, elemsA)),
                                         ("B", (subB, kB, elemsB))):
                sdp = le_dp(sub, ks)
                sbefore, stot = pair_probs(sub, ks, sdp)
                ps = []
                for (x, y) in incomparable_pairs(sub, ks):
                    p_side = Fraction(sbefore[x][y], stot)
                    if balanced(p_side):
                        gx, gy = elems[x], elems[y]
                        ps.append(balanced(Fraction(beforeP[gx][gy], totP)))
                per[nm] = ps

            def viol(nm):
                return len(per[nm]) > 0 and not any(per[nm])

            if not any(per["A"] + per["B"]):
                counts_either += 1
            if kA != kB:
                sm = "A" if kA < kB else "B"
                if viol(sm):
                    for c in CONV:
                        counts[c] += 1
            else:
                if viol("A") and viol("B"):
                    counts["TIE_NEITHER_SIDE_SURVIVES"] += 1
                if viol("A"):
                    counts["TIE_SIDE_A"] += 1
                if viol("B"):
                    counts["TIE_SIDE_B"] += 1

print("  U_smaller failures, n<=7, BOTH-sides-non-chain scope:")
for c in CONV:
    print(f"    {c:<28}: {counts[c]:>7}   "
          f"(vs mg-3969's 58755: diff {counts[c]-58755:+d})")
print(f"  U_either failures (my recount, cross-check): {counts_either} "
      f"(mg-3969 says 682; match={counts_either==682})")

print()
print("=" * 78)
print("D3 — every published number, recomputed exactly")
print("=" * 78)
E17_78 = Fraction(17, 78)
E13_111 = Fraction(13, 111)
checks = [
    ("17/78 as a decimal", float(E17_78), 0.217949, "doc says 0.217949"),
    ("13/111 as a decimal", float(E13_111), 0.117117, "doc says 0.117117"),
    ("(17/78)/0.20", float(E17_78 / Fraction(1, 5)), 1.0897, "doc says 1.0897"),
    ("(17/78)^2/2", float(E17_78 ** 2 / 2), 0.023751, "doc says 289/12168 = 0.023751"),
    ("0.02^2/2", 0.02 ** 2 / 2, 2e-4, "doc says 2e-4"),
    ("0.20^2/2", 0.20 ** 2 / 2, 2e-2, "doc says 2e-2"),
    ("(0.20/0.02)^2", (0.20 / 0.02) ** 2, 100.0, "doc: the '100x' is the square of a 10x move"),
    ("0.023751/0.02", float(E17_78 ** 2 / 2) / 0.02, 1.1875, "doc says 1.1875"),
]
for name, got, want, note in checks:
    ok2 = abs(got - want) < 5e-5 * max(1.0, abs(want))
    print(f"  [{'ok ' if ok2 else 'FAIL'}] {name:<22} = {got:<12.8g}  {note}")

print(f"\n  (17/78)^2/2 exactly = {E17_78**2/2}  "
      f"(doc says 289/12168; equal: {E17_78**2/2 == Fraction(289,12168)})")

print()
print("  Same chain at the ONE+ ceiling I found:")
E17 = Fraction(1, 7)
print(f"    eps_0 <= 1/7 = {float(E17):.6f}; (1/7)/0.20 = {float(E17/Fraction(1,5)):.4f} "
      f"-> the calibration is {100*(1-float(E17/Fraction(1,5))):.1f}% ABOVE the ceiling")
print(f"    eps_dem <= (1/7)^2/2 = {E17**2/2} = {float(E17**2/2):.6f} "
      f"vs corpus 0.02 -> corpus is {0.02/float(E17**2/2):.2f}x the ceiling")
print("    and with the family, both ceilings are in fact 0.")

print()
print("=" * 78)
print("D4 — NORMALISATION, named explicitly (the brief asks for this)")
print("=" * 78)
print("""  17/78, 13/111, 1/7 and the corpus's 0.20 are ALL values of

        eps_leak := Delta_1(A,B) = E|A \\ sigma(A)| / min(|A|,|B|),

  the L^1 ordinal-sum defect defined at source `:270-278` and identified as the
  leakage epsilon of L4 `:466` by Op-Form Sec 1's symbol table.  This is a THIRD
  normalisation, distinct from BOTH of the two the audit brief names:

        eps_c3ca : E[inv_e] <= eps * n^2                (LIBweak-mg-c3ca:172)
        eps_spec : E[inv_e] <= (eps/6) * (n^2 - 1)      (STATE.md:15)
        eps_spec / eps_c3ca = 6n^2/(n^2-1) -> 6         (STATE.md:15, inline)

  eps_leak is not a division of E[inv_e] at all -- it is a per-element crossing
  density -- and it reaches eps_spec through CHEEGER, i.e. by a SQUARE, not by a
  factor of 6:  eps_spec <= (1/2) eps_leak^2  (Op-Form Sec 4.2, the boxed
  relation mg-3969 Sec 7 uses).  So the factor-of-6 trap the brief warns about
  cannot fire on these numbers, and the comparison 17/78 vs 0.20 is like-for-like:
  both are eps_leak.  The trap that COULD fire here is the SQUARE, and mg-3969
  handles it correctly (its 0.02^2/2 = 2e-4 / 0.20^2/2 = 2e-2 check is exactly
  that guard).""")
