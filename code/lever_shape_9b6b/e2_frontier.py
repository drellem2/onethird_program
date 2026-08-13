#!/usr/bin/env python3
"""mg-9b6b arm e2 — THE DENSITY-TO-BALANCE FRONTIER EXISTS, IS EXHAUSTIVELY MEASURABLE, AND RISES.
IT JUST RISES IN THE WRONG PLACE.

One table, read in both directions, over EVERY isomorphism class at `n ≤ 8`:

    G(s) = max{ d(P) : δ(P) ≤ s }      the (R)-shaped reading — a density ceiling under a
                                        BALANCE hypothesis.  This is the object residual (R) asks
                                        for, and `frozen` is `G` at `s = 1/3` read STRICTLY.
    F(t) = min{ δ(P) : d(P) ≥ t }      the mg-0b96 §6 reading — the largest `f` there can be.

WHY THIS IS WORTH MEASURING WHEN THE ANSWER IS ALREADY CLOSED.  Because the closure keeps being
re-derived from four directions, and the reason it keeps looking alive is that the frontier is
REAL: `G` is a genuine, non-trivial, rising function of `s`, computable to the last member, with no
conjecture anywhere in it.  What `e1` establishes about the STATEMENT this arm establishes about
the DATA — that every value of the frontier row 8 could consume sits at, or on the far side of, the
one place where the population goes to zero:

  m1  `G` is non-empty and rising for `s ≥ 1/3` and EMPTY for every `s < 1/3`.  The function has a
      POLE exactly at the hypothesis row 8 needs, and an instrument computing it looks perfectly
      healthy right up to that value.  The population column is printed beside every ceiling for
      that reason: `EMPTY` and `0` are different answers and this arm never prints one as the other.
  m2  `F` — the staircase, every step, at every `n ≤ 8`.  It rises from `1/3` to `1/2`.
  m3  `G(1/3)` reproduces `docs/FACTS.md` F23's closed form.  ⚠️ THROUGH THE SAME LIBRARY F23 WAS
      MEASURED WITH, so this is a CONSISTENCY CHECK ON THIS ARM and not a corroboration of F23.
  m4  ZERO SLACK.  `F(D_needed) = 1/3` EXACTLY at every `n ≤ 8` — so the `f` mg-0b96 §6 asks for
      cannot have any margin at its own threshold: the equality witness is the boundary class,
      which is already on the record and is not going away.

⚠️  NOTHING HERE IS A MEASUREMENT ON THE FROZEN CLASS.  `e0` T6 establishes that class is empty at
every `n ≤ 8`; that emptiness is this arm's SUBJECT, not a caveat on its numbers.
"""

import sys
from fractions import Fraction

import lib9b6b as Y


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


def main():
    head("mg-9b6b  e2  the frontier is real, it rises, and it rises in the wrong place")
    tab = Y.table(8)
    rows = Y.frontier(tab)

    # ------------------------------------------------------------------ m1
    rule("m1  G(s) = max{ d : δ ≤ s } — THE (R)-SHAPED READING, AND ITS POLE")
    print("    Residual (R) asks for a density ceiling under a BALANCE hypothesis.  Here is that")
    print("    ceiling, computed exhaustively.  The `members` column is printed beside every one")
    print("    because a ceiling over an EMPTY class is not a ceiling of 0, it is not a ceiling.")
    print()
    grid = [(Fraction(1, 4), "<= 1/4"), (Fraction(3, 10), "<= 3/10"),
            (Y.THIRD, "<  1/3   FROZEN -- what row 8 needs"),
            (Y.THIRD, "<= 1/3   the boundary class"),
            (Fraction(7, 20), "<= 7/20"), (Fraction(2, 5), "<= 2/5"),
            (Fraction(9, 20), "<= 9/20"), (Y.HALF, "<= 1/2   everything")]
    print("      %3s  %-34s %10s %12s" % ("n", "hypothesis", "members", "max d"))
    empty_below = 0
    checked_below = 0
    rises = 0
    for n in range(4, 9):
        prev = None
        up = True
        for i, (s, label) in enumerate(grid):
            strict = "<  " in label
            members, mx = Y.ceiling_at(rows[n], s, strict=strict)
            if s <= Y.THIRD and strict:
                checked_below += 1
                if members == 0:
                    empty_below += 1
            if s < Y.THIRD:
                checked_below += 1
                if members == 0:
                    empty_below += 1
            print("      %3d  %-34s %10d %12s"
                  % (n, label, members, mx if mx is not None else "EMPTY"))
            if mx is not None:
                if prev is not None and mx < prev:
                    up = False
                prev = mx
        rises += up
        print()
    check("m1.a", empty_below == checked_below,
          "EVERY hypothesis strictly below the 1/3 boundary is empty at every n = 4..8 "
          "(%d of %d cells)" % (empty_below, checked_below))
    check("m1.b", rises == 5, "and G is non-decreasing in s at every n = 4..8 where it is defined")
    print("    THE POLE IS THE FINDING.  G is a real function everywhere it has members, and it")
    print("    has none on the frozen side.  An instrument computing (R) therefore returns a")
    print("    healthy, rising, exactly-computed answer at every hypothesis EXCEPT the one row 8")
    print("    consumes, where it returns nothing at all -- and `nothing at all` is what a ceiling")
    print("    of `d <= anything` looks like from inside the tool.  That is why this route reads")
    print("    as open from the instrument side however many times it is closed from the logic")
    print("    side (e1 m2).")

    # ------------------------------------------------------------------ m2
    rule("m2  F(t) = min{ δ : d ≥ t } — THE mg-0b96 §6 READING, EVERY STEP")
    print("    This is the largest `f` there can be: any true `δ ≥ f(d)` has f(t) <= F(t) at every")
    print("    t.  So the whole question `does a density-to-balance bound exist` is a question")
    print("    about THIS staircase and nothing else.")
    print()
    for n in range(3, 9):
        steps = Y.staircase(rows[n], "envelope")
        print("      n=%d  %2d steps" % (n, len(steps)))
        print("            " + "  ".join("d>=%s: %s" % (t, v) for t, v in steps))
    n8 = Y.staircase(rows[8], "envelope")
    check("m2.a", len(n8) >= 4, "%d distinct steps at n = 8 -- the relation is real, not flat"
          % len(n8))
    check("m2.b", n8[0][1] == Y.THIRD and n8[-1][1] == Y.HALF,
          "it runs from 1/3 at the sparse end to 1/2 at the antichain")

    # ------------------------------------------------------------------ m3
    rule("m3  G(1/3) AGAINST docs/FACTS.md F23 — A CONSISTENCY CHECK, NOT A CORROBORATION")
    print("    F23 says max{ d : δ = 1/3 } = 4*floor(n/3)/(n(n-1)), FP exhaustive n = 3..9.")
    print("    ⚠️  THIS ARM COMPUTES IT THROUGH lib6ff4, WHICH IS THE LIBRARY mg-6ff4 MEASURED F23")
    print("    WITH.  Agreement therefore says this arm's enumeration and delta agree with F23's;")
    print("    it does NOT independently corroborate F23, and a disagreement would impeach this")
    print("    directory first.  It is here because everything below reads G(1/3) off this table.")
    print()
    print("      %3s  %14s  %14s  %s" % ("n", "G(1/3) measured", "F23 closed form", ""))
    agree = 0
    for n in range(3, 9):
        _, mx = Y.ceiling_at(rows[n], Y.THIRD)
        f23 = Y.d_boundary(n)
        agree += (mx == f23)
        print("      %3d  %14s  %14s  %s" % (n, mx, f23, "agree" if mx == f23 else "DISAGREE"))
    check("m3.a", agree == 6, "agrees at every n = 3..8")

    # ------------------------------------------------------------------ m4
    rule("m4  ZERO SLACK AT THE THRESHOLD ROW 8 NEEDS")
    print("    mg-0b96 §6 wants f(D_needed) >= 1/3.  F(D_needed) is the largest value f can take")
    print("    there.  If those two are EQUAL, the asked-for bound is tight -- it has to be exactly")
    print("    sharp at its own threshold, with no room for any argument that loses anything.")
    print()
    print("      %3s  %-12s %12s %12s  %s"
          % ("n", "D_needed(n)", "F(D_needed)", "slack", "equality witness"))
    tight = 0
    for n in range(3, 9):
        Dn = Y.d_needed(n)
        members, mn = Y.envelope_at(rows[n], Dn)
        slack = mn - Y.THIRD
        tight += (slack == 0)
        wit = [d for (d, dl) in rows[n] if dl == mn and d >= Dn]
        print("      %3d  %-12s %12s %12s  %d poset(s), densest at d = %s"
              % (n, Dn, mn, slack, len(wit), max(wit)))
    check("m4.a", tight == 6, "slack is EXACTLY ZERO at every n = 3..8")
    print()
    print("    AND THE WITNESSES ARE THE BOUNDARY CLASS, WHICH IS NOT GOING AWAY.  e1 m1's")
    print("    ordinal-sum family puts a delta = 1/3 poset above D_needed at 63 orders (n = 3..66")
    print("    except 65), so the zero slack is not a small-n artefact: it is a construction that")
    print("    runs out only where F23's own ceiling drops below D_needed, at n = 67.")

    rule("VERDICT")
    if FAIL:
        print("    RED -- %d check(s) failed: %s" % (len(FAIL), ", ".join(FAIL)))
        return 1
    print("    THE FRONTIER IS REAL AND IT IS UNCONSUMABLE, WHICH ARE NOT THE SAME SENTENCE.")
    print()
    print("    Everything G says is said about a class with delta >= 1/3.  Row 8 consumes G at")
    print("    delta < 1/3.  The two do not overlap, and the gap between them is not a matter of")
    print("    reaching a larger n: the class is empty at every n IF THE CONJECTURE HOLDS THERE,")
    print("    so a census can never populate it and can never fail to.  The measurable half of")
    print("    the frontier and the consumable half are disjoint by construction.")
    print()
    print("    WHAT THIS ARM DOES NOT SHOW.  It does not show a density-to-balance bound is FALSE")
    print("    -- e1 m3 shows the strict reading is, on the unrestricted class, and nothing here")
    print("    touches the flat one, which is true if and only if the conjecture is.  And every")
    print("    number here is kind FP at n <= 8: the staircase above 1/3 is unconditional")
    print("    information, but it is information about 20 000 posets, not about all of them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
