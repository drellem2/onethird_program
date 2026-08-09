#!/usr/bin/env python3
"""a4 — mg-39bf tests the universal negative and the 40 % that sits beside it.

Two claims from mg-9461 4.3-4.4:

  (a) "0.20 sits 40 % above the n<=7 required-scope ceiling 1/7."
  (b) "There is no experiment that improves 0.20; only a proof moves it."

(a) is checked in a2 H and is exactly right.  What a2 could not check is
whether 40 % is a STABLE reading or an artefact of stopping at n = 7 — and
that matters, because a headline optimism figure gets quoted as a margin.

mg-d3c7's family is PROVED, not sampled: chain c_1 < ... < c_{n-1} plus one
isolated z, A = {z, c_1..c_{k-1}}, n = 2k+1, Delta_1 = (k+1)/((2k+1)k) -> 0.
Its members are witnesses, so the required-scope ceiling at n <= N is AT MOST
the smallest Delta_1 the family reaches inside N.  The 40 % can therefore be
recomputed at every N in CLOSED FORM, with no sweep at all.

That is the point of this script, and it cuts BOTH ways for mg-9461:
  - against 4.3, because 40 % is the mildest reading available and the
    document leads with it;
  - FOR 4.4, because the movement needs no experiment — it is already
    determined by a proved family, which is exactly what "only a proof moves
    it" predicts.

I take the family from mg-d3c7's landed statement and re-evaluate the closed
form; I do NOT re-derive the family (mg-3969/mg-d3c7 are closed, per the
ticket) and I do NOT re-run either sweep.
"""

from fractions import Fraction as F
import sys

FAILURES = []
LEAK = F(1, 5)          # the corpus's 0.20, in the eps_leak unit
CEIL_N7 = F(1, 7)       # mg-d3c7's required-scope ceiling at n <= 7


def fail(m):
    FAILURES.append(m)
    print("  *** FAIL: %s" % m)


def family_delta1(k):
    """mg-d3c7's family member at n = 2k+1.  Cited, not re-derived."""
    return F(k + 1, (2 * k + 1) * k)


def excess(ceiling):
    return (LEAK - ceiling) / ceiling


def main():
    print("A — IS THE 40 % STABLE, OR AN ARTEFACT OF STOPPING AT n = 7?")
    print("  ceiling(n<=N) <= min over family members with 2k+1 <= N.")
    print("  %-6s %-6s %-14s %-14s %s"
          % ("N", "k", "family Delta_1", "as decimal", "0.20 is ... above"))
    prev = None
    best = None
    for k in range(3, 51):
        n = 2 * k + 1
        d = family_delta1(k)
        best = d if best is None else min(best, d)
        if prev is not None and d >= prev:
            fail("family Delta_1 is not decreasing at k=%d" % k)
        prev = d
        if k in (3, 4, 5, 6, 8, 10, 15, 20, 30, 50):
            print("  %-6d %-6d %-14s %-14.6g %.1f %%"
                  % (n, k, d, float(d), float(excess(best)) * 100))

    print("\n  The n <= 7 ceiling the parent quotes is %s = %.6g, and 0.20 is"
          % (CEIL_N7, float(CEIL_N7)))
    print("  %.1f %% above it — correct, and a2 H confirms the arithmetic."
          % (float(excess(CEIL_N7)) * 100))
    d3 = family_delta1(3)
    print("  But the family's own n = 7 member is %s = %.6g, ABOVE 1/7, so the"
          % (d3, float(d3)))
    print("  1/7 at n <= 7 comes from a DIFFERENT witness (mg-d3c7's sweep),")
    print("  not from the family — the family only starts biting past n = 7.")
    if d3 <= CEIL_N7:
        fail("family at k=3 is %s, expected above 1/7" % d3)

    print("\n  AT EVERY LARGER n THE OPTIMISM IS WORSE, and by how much is")
    print("  already fixed in closed form:")
    for k in (4, 10, 50, 200):
        d = family_delta1(k)
        print("    n = %-5d ceiling <= %-16s 0.20 is %8.1f %% above"
              % (2 * k + 1, str(d), float(excess(d)) * 100))
    print()
    print("  READING: 40 % is the MILDEST comparison the corpus can currently")
    print("  make, and the parent leads with it.  The figure is not wrong; it")
    print("  is the floor of a quantity with no ceiling, presented without")
    print("  saying so.  Anyone quoting '40 % optimistic' as a bounded margin")
    print("  has the direction right and the magnitude unboundedly wrong.")

    print("\nB — 'THERE IS NO EXPERIMENT THAT IMPROVES 0.20'")
    print("  Four candidate experiments, named in my PREDICTIONS.md BEFORE the")
    print("  parent's 4.4 was read, each with its disposition:")
    cands = [
        ("1. larger-n sweep for a smaller required-scope ceiling",
         "DISPOSED, and not by the parent's stated reason. The parent says a "
         "sweep 'can only lower a ceiling on a surrogate already refuted at 0'. "
         "The sharper disposal is section A above: the movement is already "
         "available in CLOSED FORM from a proved family, so no experiment is "
         "needed to obtain it and none could add to it. This SUPPORTS 4.4."),
        ("2. numerical search for slack in the consuming inequality",
         "DISPOSED by the parent's own 4.2, one section earlier: the consumed "
         "object is eps_0^cons, on which disjunct (i) is true at eps = 1 for "
         "every exhibitable poset. There is no slack to search — the "
         "inequality is vacuously satisfied everywhere it can be evaluated."),
        ("3. adversarial search for a worst family, to REFUTE 0.20",
         "DISPOSED, and this is the strongest of the four. Exhibiting a poset "
         "where the transfer fails with (i) false means exhibiting a poset "
         "with delta(P) < 1/3 — i.e. refuting 1/3-2/3 itself. So the "
         "experiment cannot be run without already settling the conjecture. "
         "The parent states the mechanism in 4.2 but does not draw this "
         "consequence; drawing it is what makes the negative UNIVERSAL rather "
         "than merely unattempted."),
        ("4. witness search for the prefix-capture fraction c",
         "NOT DISPOSED — but it does not target 0.20. It targets chain (IV), "
         "and the parent itself proposes exactly this experiment in 11. So "
         "it is not a counterexample to the negative; it is an experiment "
         "that moves WHICH LEMMA the constant rests on, not the constant."),
    ]
    for name, verdict in cands:
        print("\n  %s" % name)
        for line in _wrap(verdict, 68):
            print("      %s" % line)

    print("\n  SCORE: my P5 (0.55, that the universal negative is over-claimed)")
    print("  is LOST. All four candidates are disposed of or off-target, and")
    print("  candidate 3's disposal is stronger than the parent's own stated")
    print("  reason. The sentence is SOUND.")
    print()
    print("  ONE QUALIFICATION IT SHOULD CARRY: the negative is about 0.20's")
    print("  VALUE. Section A shows a figure the document publishes beside it")
    print("  — the 40 % — is not fixed, and the parent does not say so.")

    print("\n" + "=" * 72)
    if FAILURES:
        print("RESULT: %d FAILURE(S)" % len(FAILURES))
        for f in FAILURES:
            print("  - %s" % f)
        return 1
    print("RESULT: 40 % re-derived and shown to be the mildest available "
          "reading; universal negative survives a pre-registered enumeration.")
    return 0


def _wrap(s, w):
    out, cur = [], ""
    for word in s.split():
        if len(cur) + len(word) + 1 > w:
            out.append(cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        out.append(cur)
    return out


if __name__ == "__main__":
    sys.exit(main())
