#!/usr/bin/env python3
"""mg-9b6b arm e3 — THE DENSITY CEILING IS A DIAL, AND PRICING IT END TO END IS A DIFFERENT
STATEMENT FROM PRICING ONE POINT OF IT.

`mg-0b96` §3 priced the ceiling at ONE value of `D` — the constant `D_needed ≈ 2e-2` that closes
row 8 — and found it worth 84 unreached orders of the conjecture.  That is the right price at that
point.  This arm asks what the FAMILY does, because `(1_D)` is a one-parameter family and the two
ends `mg-0b96` did not evaluate are where the shape shows:

  m1  THE THREE ENDS.  What each `D` is worth (through `ε_sup = d·n/(n+1)`), side by side.
  m2  WHAT EACH ONE DELIVERS, in orders.  `(1_D)` forbids a frozen PRIMITIVE poset at exactly the
      `n` with `2/n > D`, so the family maps `D` to an initial segment of the conjecture.  The
      map is monotone: every step toward a useful `D` buys more of the target.
  m3  WHAT EACH ONE EXEMPTS, which is the same question from the other side and is not the same
      answer.  `{d ≤ D}` is the class a ceiling lets off; at `D_needed` it contains no non-chain
      below `n = 11` and no primitive below `n = 99`.
  m4  THE DATA END.  Feed the dial the ceiling the boundary class ACTUALLY EXHIBITS — F23's
      `4⌊n/3⌋/(n(n−1))` — and it forbids a frozen primitive poset at EVERY `n ≥ 4`: the whole
      conjecture in one step, not 84 orders of it.  The closer a ceiling is to what the data shows,
      the more completely it IS the target.
  m5  THE GAP IN ORDERS RATHER THAN IN `ε`.  `mg-0b96` measured F26's shortfall as `49×` in `ε`
      currency.  In orders it is starker: F26's ceiling delivers ZERO orders at every `n ≥ 4`, and
      any `D` delivering even ONE order past the census frontier must be under `2/15`, against a
      proven ceiling of `1 − Θ(1/n)` — a factor of 7, widening.

⚠️  EVERY USE OF F23's CLOSED FORM ABOVE `n = 9` IS AN EXTRAPOLATION and is marked on the line that
does it.  m4 is therefore reported TWICE: once on the measured maxima at `n ≤ 8` alone, where it is
a fact, and once on the closed form, where it is a conditional.
"""

import sys
from fractions import Fraction

import lib9b6b as Y
import lib6ff4 as L


def rule(t):
    print("-" * 100)
    print(t)


def head(t):
    print("=" * 100)
    print(t)
    print("=" * 100)


FAIL = []


def check(tag, ok, detail=""):
    print("    %-7s %-7s %s" % (tag, "ok" if ok else "FAILED", detail))
    if not ok:
        FAIL.append(tag)


CENSUS = 14          # the conjecture is verified through n = 14 (Gupta, preprint; refereed 11)


def delivered_upto(D_of_n, cap=400):
    """The `n` at which `(1_D)` forbids a frozen PRIMITIVE poset: those with `2/n > D(n)`.

    Primitivity forces `m ≥ n−1`, hence `d ≥ 2/n` (STATE.md ledger row 2).  A frozen poset obeying
    the ceiling would need `2/n ≤ d ≤ D`, so the ceiling forbids one exactly where `2/n > D`."""
    return [n for n in range(3, cap) if Y.primitive_floor(n) > D_of_n(n)]


def main():
    head("mg-9b6b  e3  the density ceiling is a dial, priced end to end")

    # ------------------------------------------------------------------ m1
    rule("m1  THE THREE ENDS OF THE DIAL, AND WHAT EACH IS WORTH")
    print("    eps_sup = d*n/(n+1) is the supply bound (mg-0e8c, STATE.md row 8); the wall is")
    print("    already down wherever eps_sup <= eps_dem = %s." % Y.EPS_DEM)
    print()
    print("      %4s  %-16s %-16s %-16s | %-9s %-9s %-9s"
          % ("n", "PROVABLE (F26)", "NEEDED (row 8)", "DATA (F23)",
             "eps@F26", "eps@need", "eps@data"))
    for n in (8, 15, 40, 66, 99, 300):
        a, b, c = Y.d_provable(n), Y.d_needed(n), Y.d_boundary(n)
        mark = "" if n <= 9 else "   <- F23 EXTRAPOLATED"
        print("      %4d  %-16s %-16s %-16s | %-9.4f %-9.4f %-9.4f%s"
              % (n, "%.4f" % float(a), "%.4f" % float(b), "%.4f" % float(c),
                 float(Y.eps_sup(n, a)), float(Y.eps_sup(n, b)), float(Y.eps_sup(n, c)), mark))
    check("m1.a", all(Y.eps_sup(n, Y.d_provable(n)) > Y.EPS_DEM for n in (8, 15, 40, 99, 300)),
          "F26's proven ceiling never brings eps_sup to eps_dem at any n listed")
    check("m1.b", all(Y.eps_sup(n, Y.d_boundary(n)) <= Y.EPS_DEM for n in (67, 99, 300)),
          "the DATA end does, at every n >= 67 listed -- if F23's form continues")

    # ------------------------------------------------------------------ m2
    rule("m2  WHAT EACH `D` DELIVERS, IN ORDERS OF THE CONJECTURE")
    print("    A frozen poset obeying `d <= D` and primitive would need 2/n <= D.  So (1_D)")
    print("    forbids one at every n with 2/n > D, and a minimal counterexample is primitive --")
    print("    the ceiling hands you the conjecture on an initial segment.  Census frontier: %d."
          % CENSUS)
    print()
    print("      %-26s %-16s %-8s %s"
          % ("D", "forbids up to n", "orders", "of those, UNREACHED (n > %d)" % CENSUS))
    rowsout = []
    for label, fn in (("1/2", lambda n: Fraction(1, 2)),
                      ("1/7", lambda n: Fraction(1, 7)),
                      ("2/15", lambda n: Fraction(2, 15)),
                      ("1/10", lambda n: Fraction(1, 10)),
                      ("eps_dem*(n+1)/n  ROW 8", Y.d_needed),
                      ("1/100", lambda n: Fraction(1, 100)),
                      ("F26's 1-ceil((n-1)/2)/C  PROVEN", Y.d_provable),
                      ("F23's 4*floor(n/3)/n(n-1)  DATA", Y.d_boundary)):
        got = delivered_upto(fn)
        top = max(got) if got else None
        unreached = [n for n in got if n > CENSUS]
        rowsout.append((label, got))
        print("      %-26s %-16s %-8s %s"
              % (label,
                 ("n = %d" % top) if top is not None else "nothing",
                 len(got),
                 len(unreached) if unreached else 0))
    d_needed_orders = [n for n in delivered_upto(Y.d_needed) if n > CENSUS]
    check("m2.a", len(d_needed_orders) == 84 and max(d_needed_orders) == 98,
          "ROW 8's ceiling delivers exactly 84 unreached orders, n = 15..98 -- mg-0b96 d2's "
          "figure, reproduced here from a different direction as a control on this arm")
    check("m2.b", not delivered_upto(Y.d_provable),
          "F26's PROVEN ceiling delivers NOTHING at any n in 3..399")

    # ------------------------------------------------------------------ m3
    rule("m3  WHAT THE CEILING EXEMPTS -- the same question from the other side")
    print("    `{d <= D}` is the class (1_D) lets off.  If it is empty, the ceiling is not a")
    print("    weakening of the conjecture at that n; it is the conjecture at that n.")
    print()
    first_nonchain = next(n for n in range(3, 400)
                          if Fraction(2, n * (n - 1)) <= Y.d_needed(n))
    first_prim = next(n for n in range(3, 400) if Y.primitive_floor(n) <= Y.d_needed(n))
    print("      the sparsest non-chain has d = 1/C(n,2) = 2/(n(n-1))")
    print("      first n at which ANY non-chain poset is exempt at D_needed:   n = %d" % first_nonchain)
    print("      first n at which a PRIMITIVE poset is exempt at D_needed:     n = %d" % first_prim)
    check("m3.a", first_nonchain == 11,
          "so at every n <= 10 the row-8 ceiling exempts NOT ONE non-chain poset -- it is the "
          "conjecture verbatim there, with no restriction at all")
    check("m3.b", first_prim == 99, "and it exempts no primitive poset below n = 99, which is "
          "mg-0b96 d2's crossing arrived at from the exemption side")

    # ------------------------------------------------------------------ m4
    rule("m4  THE DATA END -- the ceiling the boundary class actually exhibits")
    print("    (a) ON THE MEASURED MAXIMA ALONE, no extrapolation: G(1/3) at n <= 8, re-measured")
    print("        in this arm rather than copied across from e2.")
    print()
    # MEASURED HERE, NOT COPIED FROM e2's TRANSCRIPT.  Two hand-kept copies of the same six
    # numbers is exactly how a table goes stale in the one direction nothing regenerates
    # (mg-1344).  The early exit in `delta_at_most` is legitimate at THIS use and not at e2's:
    # here only MEMBERSHIP of {δ ≤ 1/3} is read, where e2 reads the value.
    measured = {}
    classes = L.all_classes(8)
    for n in range(3, 9):
        best = None
        for down in classes[n]:
            ok, _, _ = L.delta_at_most(n, down, Y.THIRD)
            if ok:
                d = Y.density(n, down)
                if best is None or d > best:
                    best = d
        measured[n] = best
    print("      %3s  %-10s %-10s %s" % ("n", "G(1/3)", "2/n", "does the ceiling forbid a frozen "
                                         "primitive at this n?"))
    forbid = 0
    for n in range(3, 9):
        g, p = measured[n], Y.primitive_floor(n)
        hit = p > g
        forbid += hit
        print("      %3d  %-10s %-10s %s" % (n, g, p, "YES" if hit else "no"))
    check("m4.a", forbid == 5,
          "at every measured n = 4..8; n = 3 is the one exception and it is the boundary poset "
          "itself, which is primitive and has d = 2/3 = 2/n exactly")
    print()
    print("    (b) ON F23's CLOSED FORM -- ⚠️ AN EXTRAPOLATION ABOVE n = 9, and the conclusion is")
    print("        conditional on that form continuing:")
    got = delivered_upto(Y.d_boundary)
    missing = [n for n in range(3, 400) if n not in got]
    print("        (1_{F23}) forbids a frozen primitive at every n in 3..399 EXCEPT %s." % missing)
    check("m4.b", missing == [3],
          "so the data end delivers the conjecture at every n >= 4 -- the WHOLE target in one "
          "step, not 84 orders of it")
    print()
    print("    THE DIRECTION IS THE POINT.  A ceiling closer to what the data shows is a STRONGER")
    print("    statement, not a more plausible one: it exempts less, so it asserts more.  The dial")
    print("    has no setting at which it stops being the conjecture and starts being a lemma --")
    print("    mg-0b96 §2's sentence -- and this arm adds the quantitative half: the settings get")
    print("    monotonically more expensive in exactly the direction the evidence points.")

    # ------------------------------------------------------------------ m5
    rule("m5  THE SHORTFALL IN ORDERS RATHER THAN IN `ε`")
    print("    mg-0b96 measured F26's shortfall as 49x in eps currency at n = 99.  The same")
    print("    shortfall in the currency this arm uses:")
    print()
    bar = Fraction(2, CENSUS + 1)
    print("    A constant ceiling D delivers order n exactly when 2/n > D, so it reaches PAST the")
    print("    frontier only if D < 2/%d = %.4f.  The bound is STRICT and the supremum is NOT"
          % (CENSUS + 1, float(bar)))
    print("    ATTAINED: D = %s itself delivers nothing past the frontier, and m5.a tests both"
          % bar)
    print("    sides of that rather than asserting one.")
    print()
    print("      %4s  %-16s %-16s %s" % ("n", "F26 proves d <=", "must be under", "factor"))
    for n in (15, 40, 99, 300):
        a = Y.d_provable(n)
        print("      %4d  %-16.4f %-16.4f %.1fx" % (n, float(a), float(bar), float(a / bar)))
    check("m5.a", not [n for n in delivered_upto(lambda n: bar) if n > CENSUS]
          and [n for n in delivered_upto(lambda n: bar - Fraction(1, 10 ** 6)) if n > CENSUS],
          "D = 2/%d delivers no unreached order and anything below it delivers n = 15 -- the "
          "threshold is exactly 2/%d and it is not attained" % (CENSUS + 1, CENSUS + 1))
    check("m5.b", all(Y.d_provable(n) > bar for n in (15, 40, 99, 300)),
          "and F26's proven ceiling is above that threshold at every n listed, by a factor that "
          "WIDENS -- 7.0x at n = 15 to 7.5x at n = 300")

    rule("VERDICT")
    if FAIL:
        print("    RED -- %d check(s) failed: %s" % (len(FAIL), ", ".join(FAIL)))
        return 1
    print("    NO SETTING OF THE DIAL IS BOTH PROVABLE AND WORTH ANYTHING, and the reason is not")
    print("    that the gap is large.  It is that value and price are THE SAME QUANTITY here:")
    print("    what a ceiling delivers is measured in orders of the conjecture, so a ceiling that")
    print("    delivers more IS a stronger statement.  mg-0b96 read that off one point; the")
    print("    family says it at every point, and says it hardest at the end the data points to.")
    print()
    print("    WHAT THIS ARM DOES NOT SHOW.  Nothing here shows any (1_D) is FALSE -- every one of")
    print("    them is true if the conjecture is.  And m1's and m4(b)'s F23 values above n = 9 are")
    print("    an extrapolation of an FP closed form; m4(a) is the same finding without it, and")
    print("    it is the one to quote.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
