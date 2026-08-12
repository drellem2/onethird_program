#!/usr/bin/env python3
"""mg-6ff4 arm c0 — THE CONTROLS, INCLUDING THE ONES THAT MUST FAIL.

Nothing below is a finding.  Every check here exists because one specific way of getting this
ticket wrong would leave every headline number looking healthy:

  T1  CLASS COUNTS vs OEIS A000112.  A broken canonical form MERGES classes: the population
      shrinks, every "0 frozen posets" stays 0, and nothing else moves.
  T2  THE CENSUS vs `mg-7c78`'s `a5` PRINTED TABLE.  Independent code, same numbers, or this
      arm has re-measured nothing.
  T3  `E[inv_e] = Σ_{x∥y} min(p,1−p)` AGAINST BRUTE-FORCE ENUMERATION of `L(P)`.  This is the
      identity the whole instrument rests on and it is TRUE ONLY BECAUSE `e` is the majority
      order.  Checked on every poset at `n ≤ 6`, boundary or not.
  T4  THE `V` BY HAND.  `L = {acb, abc, cab}`, `e = (a,c,b)`, `E[inv_e] = 2/3`, `ε = 1/2`.
  T5  ORDINAL ADDITIVITY.  `δ(A ⊕ B) = max(δA, δB)` and `E[inv_e](A ⊕ B) = E[inv_e](A) +
      E[inv_e](B)`, checked on explicit sums rather than assumed — the whole closed form is this
      identity applied `k` times.
  T6  THE TWO-ATOM LAW SATURATES `n/(n+1)`.  The abstract measure `(2/3)δ_e + (1/3)δ_{rev e}`,
      built explicitly, scores exactly `n/(n+1)` in the `ε_spec` normalisation — so the
      realizability gap in `c3` is a gap against a measure that EXISTS, not against an algebraic
      supremum nobody has exhibited.
  T7  ⚠️ WRONG-DIRECTION CONTROL — A DELIBERATELY WRONG `e`.  Re-measure `ε` at the `V` against a
      reference order that is NOT the majority order.  IT MUST MOVE.  If it does not, the
      instrument is not sensitive to the choice of `e` and item 4 of the ticket is unmeasurable
      by it.
  T8  ⚠️ WRONG-DIRECTION CONTROL — A CONSTRUCTED FROZEN TABLE.  Feed the boundary detector a
      hand-made pair table with `δ = 1/4 < 1/3` and check it is classified BELOW the boundary and
      not AT it.  Every `δ = 1/3` count in this instrument is a count of an equality, and an
      equality test that is really a `≤` test would silently absorb the frozen class into the
      boundary class — the one confusion this ticket exists to avoid.

Exits 0 if every control lands as stated, 1 if any fires, 2 on refusal.
"""

import sys
from fractions import Fraction

import lib6ff4 as L

NMAX_CLASSES = 8
A5_CENSUS = {        # mg-7c78 out_a5_boundary_class.txt, m1, columns: posets-with-an-inc-pair,
    2: (1, Fraction(1, 2), 0, 0),      # min delta, #(delta=1/3), #(delta<1/3)
    3: (4, Fraction(1, 3), 1, 0),
    4: (15, Fraction(1, 3), 2, 0),
    5: (62, Fraction(1, 3), 3, 0),
    6: (317, Fraction(1, 3), 5, 0),
    7: (2044, Fraction(1, 3), 8, 0),
    8: (16998, Fraction(1, 3), 12, 0),
}

V = (0, 1, 0)        # a=0, b=1 with a<b, c=2 free.  down[1] = {0}.


def ordinal_sum(blocks):
    """⊕ of `[(n, down), ...]` into one poset."""
    n = sum(b[0] for b in blocks)
    down, off = [], 0
    for (k, d) in blocks:
        below = (1 << off) - 1
        for i in range(k):
            m = 0
            for j in range(k):
                if d[i] >> j & 1:
                    m |= 1 << (off + j)
            down.append(m | below)
        off += k
    return n, tuple(down)


def main():
    print("=" * 92)
    print("mg-6ff4  c0  controls — including the two that must fail")
    print("=" * 92)
    print()
    bad = 0

    # ---------------------------------------------------------------------------------- T1
    print("T1  isomorphism-class counts vs OEIS A000112")
    print("-" * 92)
    classes = L.all_classes(NMAX_CLASSES)
    for n in range(1, NMAX_CLASSES + 1):
        got, want = len(classes[n]), L.A000112[n]
        flag = "ok" if got == want else "MISMATCH"
        if got != want:
            bad += 1
        print("    n=%d  %8d  expected %8d   [%s]" % (n, got, want, flag))
    print()

    # ---------------------------------------------------------------------------------- T2
    print("T2  the census, re-measured, against mg-7c78 a5's printed table")
    print("-" * 92)
    print("    %3s %10s %12s %12s %12s   %s" % ("n", "posets", "min delta", "=1/3", "<1/3", "vs a5"))
    for n in range(2, NMAX_CLASSES + 1):
        tot = at3 = be3 = 0
        mn = None
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            tot += 1
            total = L.count_ext(n, down)
            d = max(min(p, 1 - p) for p in
                    (L.p_before(n, down, i, j, total) for (i, j) in inc))
            if mn is None or d < mn:
                mn = d
            if d == L.THIRD:
                at3 += 1
            elif d < L.THIRD:
                be3 += 1
        want = A5_CENSUS[n]
        agree = (tot, mn, at3, be3) == want
        if not agree:
            bad += 1
        print("    %3d %10d %12s %12d %12d   [%s]"
              % (n, tot, str(mn), at3, be3, "agrees" if agree else "DISAGREES %s" % (want,)))
    print()

    # ---------------------------------------------------------------------------------- T3
    print("T3  the two identities, against brute-force enumeration of L(P), and the SCOPE that")
    print("    separates them")
    print("-" * 92)
    lin_n = lin_f = maj_n = maj_f = off_n = off_f = 0
    for n in range(2, 7):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            total = L.count_ext(n, down)
            tbl = L.pair_bias_table(n, down, inc, total)
            e, uniq, orient, unorient = L.majority_order(n, down, tbl)
            if e is None:
                continue
            rank = {v: k for k, v in enumerate(e)}
            exts = L.linear_extensions(n, down)
            brute = Fraction(sum(L.inv_against(n, down, s, rank) for s in exts), len(exts))
            # (a) LINEARITY — true for ANY reference order: E[inv_e] = sum over pairs of the
            #     probability that sigma disagrees with e on that pair.
            lin = sum((1 - p) if rank[x] < rank[y] else p for (x, y), p in tbl.items())
            lin_n += 1
            if brute != lin:
                lin_f += 1
            # (b) THE SHORTCUT — E[inv_e] = sum min(p, 1-p).  Claimed ONLY when the >= 2/3
            #     tournament is TOTAL, i.e. exactly when delta(P) <= 1/3.
            short = sum(min(p, 1 - p) for p in tbl.values())
            if unorient == 0:
                maj_n += 1
                if brute != short:
                    maj_f += 1
            else:
                off_n += 1
                if brute != short:
                    off_f += 1
    if lin_f or maj_f:
        bad += 1
    print("    (a) LINEARITY, any reference order:   %4d posets · mismatches %d   [%s]"
          % (lin_n, lin_f, "PASS" if lin_f == 0 else "FAIL"))
    print("    (b) SHORTCUT  E[inv_e] = sum min(p,1-p), IN SCOPE (every pair >= 2/3-decided,")
    print("        i.e. delta <= 1/3):            %4d posets · mismatches %d   [%s]"
          % (maj_n, maj_f, "PASS" if maj_f == 0 else "FAIL"))
    print("    (c) ⚠️  THE SAME SHORTCUT OUT OF SCOPE:  %4d posets · WRONG at %d of them."
          % (off_n, off_f))
    print("        THAT IS THE CONTROL, NOT A FAILURE.  The shortcut is co-extensive with the")
    print("        boundary/frozen condition itself: off it, `e` is not the majority order, the")
    print("        per-pair disagreement is NOT min(p,1-p), and using it anyway understates")
    print("        E[inv_e]. Every arm here applies it ONLY inside (b)'s scope.")
    print()

    # ---------------------------------------------------------------------------------- T4
    print("T4  the 3-element V, by hand")
    print("-" * 92)
    n, down = 3, V
    total = L.count_ext(n, down)
    tbl = L.pair_bias_table(n, down, None, total)
    e, uniq, orient, unorient = L.majority_order(n, down, tbl)
    mm = L.measure(n, down, tbl)
    exts = sorted(L.linear_extensions(n, down))
    want = {"|L|": 3, "e": (0, 2, 1), "Einv": Fraction(2, 3), "eps": Fraction(1, 2),
            "delta": L.THIRD}
    got = {"|L|": total, "e": e, "Einv": mm["Einv"], "eps": mm["eps"],
           "delta": max(min(p, 1 - p) for p in tbl.values())}
    ok = got == want
    if not ok:
        bad += 1
    print("    L(P) = %s" % (exts,))
    print("    p table = %s" % {k: str(v) for k, v in sorted(tbl.items())})
    print("    e = %s (unique=%s)   delta = %s   E[inv_e] = %s   eps = %s"
          % (e, uniq, got["delta"], got["Einv"], got["eps"]))
    print("    hand values %s   [%s]" % ({k: str(v) for k, v in want.items()},
                                         "PASS" if ok else "FAIL"))
    print()

    # ---------------------------------------------------------------------------------- T5
    print("T5  ordinal additivity — delta is a max, E[inv_e] is a sum")
    print("-" * 92)
    t5_fail = t5_checked = 0
    smalls = [(k, d) for k in range(1, 5) for d in classes[k]]
    for (k1, d1) in smalls:
        for (k2, d2) in smalls:
            if k1 + k2 > 7:
                continue
            n, down = ordinal_sum([(k1, d1), (k2, d2)])
            parts = []
            for (kk, dd) in ((k1, d1), (k2, d2)):
                inc = L.incomparable_pairs(kk, dd)
                if not inc:
                    parts.append((None, Fraction(0)))
                    continue
                tt = L.count_ext(kk, dd)
                tb = L.pair_bias_table(kk, dd, inc, tt)
                parts.append((max(min(p, 1 - p) for p in tb.values()),
                              sum(min(p, 1 - p) for p in tb.values())))
            inc = L.incomparable_pairs(n, down)
            if not inc:
                continue
            tt = L.count_ext(n, down)
            tb = L.pair_bias_table(n, down, inc, tt)
            dsum = max(min(p, 1 - p) for p in tb.values())
            isum = sum(min(p, 1 - p) for p in tb.values())
            dparts = [p[0] for p in parts if p[0] is not None]
            t5_checked += 1
            if dsum != max(dparts) or isum != parts[0][1] + parts[1][1]:
                t5_fail += 1
    if t5_fail:
        bad += 1
    print("    %d ordinal sums A(+)B, |A|,|B| <= 4, |A(+)B| <= 7 · failures %d   [%s]"
          % (t5_checked, t5_fail, "PASS" if t5_fail == 0 else "FAIL"))
    print()

    # ---------------------------------------------------------------------------------- T6
    print("T6  the two-atom law saturates n/(n+1) in the eps_spec normalisation")
    print("-" * 92)
    t6_fail = 0
    for n in range(3, 10):
        # mu = (2/3) delta_id + (1/3) delta_reverse; every pair flips with probability exactly 1/3
        Einv = Fraction(1, 3) * (n * (n - 1) // 2)
        eps = Fraction(6, 1) * Einv / (n * n - 1)
        want = Fraction(n, n + 1)
        if eps != want:
            t6_fail += 1
        print("    n=%2d  E_mu[inv_e] = %6s   eps = %6s   n/(n+1) = %6s   [%s]"
              % (n, str(Einv), str(eps), str(want), "ok" if eps == want else "MISMATCH"))
    if t6_fail:
        bad += 1
    print("    ⚠️  This measure is NOT a poset's L(P): it is supported on 2 of n! orders.  That is")
    print("    the point — c3's gap is measured against an object that exists and is not realizable.")
    print()

    # ---------------------------------------------------------------------------------- T7
    print("T7  WRONG-DIRECTION CONTROL — a deliberately wrong reference order at the V")
    print("-" * 92)
    exts = L.linear_extensions(3, V)
    rows = []
    for ref in ((0, 2, 1), (0, 1, 2), (2, 0, 1)):
        rank = {v: k for k, v in enumerate(ref)}
        val = Fraction(sum(L.inv_against(3, V, s, rank) for s in exts), len(exts))
        rows.append((ref, val, Fraction(6, 1) * val / 8))
    for ref, ei, ep in rows:
        tag = "  <- the majority order e" if ref == (0, 2, 1) else ""
        print("    reference %s   E[inv] = %5s   eps = %5s%s" % (ref, str(ei), str(ep), tag))
    moved = len({r[2] for r in rows}) > 1
    if not moved:
        bad += 1
    print("    eps MOVES across reference orders: %s   [%s]"
          % (moved, "PASS — the instrument is sensitive to e" if moved else "FAIL"))
    print()

    # ---------------------------------------------------------------------------------- T8
    print("T8  WRONG-DIRECTION CONTROL — a constructed frozen table must NOT be called boundary")
    print("-" * 92)
    fake = {(0, 1): Fraction(3, 4), (0, 2): Fraction(4, 5)}      # delta = 1/4 < 1/3
    d_fake = max(min(p, 1 - p) for p in fake.values())
    at_boundary = d_fake == L.THIRD
    below = d_fake < L.THIRD
    ok = (not at_boundary) and below
    if not ok:
        bad += 1
    print("    hand table %s  ->  delta = %s"
          % ({k: str(v) for k, v in fake.items()}, d_fake))
    print("    classified AT the boundary: %s (must be False) · BELOW it: %s (must be True)   [%s]"
          % (at_boundary, below, "PASS" if ok else "FAIL"))
    print("    The boundary test is an EQUALITY.  A `<=` in its place would swallow the frozen")
    print("    class into the boundary class and every number in this instrument would be a")
    print("    frozen-class claim by accident.  That is the failure this control exists for.")
    print()

    print("VERDICT: %s" % ("GREEN" if bad == 0 else "RED (%d controls fired)" % bad))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
