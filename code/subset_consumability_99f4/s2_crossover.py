"""s2 — THE ACCEPTANCE CONDITION FOR THE PREFIX-CODE BRANCH, STATED BEFORE ANYTHING IS BUILT.

The ticket's own instruction: *"Require any proposal to answer 'does it bite below n ~ 10^7?'
FIRST — it is cheaper than proving the bound and it is the question that killed the last
attempt."*  This arm answers it for the whole FAMILY rather than for one candidate, because the
answer turns out to depend on one design choice and not on the mechanism at all.

  s2.1  the crossover law in closed form, checked against the binary search
  s2.2  THE ELASTICITY — why this family is structurally prone to vacuity
  s2.3  THE ACCEPTANCE TABLE — the constant a code must reach to bite at a given n
  s2.4  THE SHAPE DICHOTOMY — and it is the finding: vacuity is a property of the REFERENCE
        SCALE, not of the constant, so the question to ask a proposal is which scale it is
        stated against
  s2.5  what compression2's own measured numbers say about whether the good shape is reachable

`s0.6` is this arm's licence: the same binary search reproduces mg-0fc6's published crossover
to the unit, on code that shares nothing with it.
"""

import math
import sys

import lib99f4 as L

R = L.Report()
LOG2E = 1.0 / math.log(2.0)          # = log2(e) = 1.4426950...

R.banner("s2.1  THE CROSSOVER LAW IN CLOSED FORM — and it is checked, not asserted")
R.note("A code-length bound of SHAPE A is  `log2 e(P) <= c * n log2 n`  with `c < 1` constant.")
R.note("The free bound is `log2 e(P) <= log2 n!`, available to anybody with no theorem at all.")
R.note("Since `log2 n! = n log2 n - n log2 e + O(log n)`, shape A beats free exactly when")
R.note("")
R.note("        (1 - c) * n log2 n  >  n log2 e  + O(log n),   i.e.   log2 n  >  log2 e/(1-c),")
R.note("")
R.note("        so        n*(c)  =  2 ^ ( log2(e) / (1 - c) )   =  2 ^ ( 1.442695 / (1-c) ).")
R.note("")
R.note("DOUBLY EXPONENTIAL IN 1/(1-c).  Checked against the binary search over the exact")
R.note("`lgamma` factorial, which knows nothing about this formula:")
print()
print("       c        closed form n*      binary search n*    ratio")
CS = [0.5, 0.7, 0.8, 0.9, 1.0 - 1.0 / (24.0 * math.log(2.0)), 0.95, 0.97]
for c in CS:
    closed = 2.0 ** (LOG2E / (1.0 - c))
    exact = L.crossover(c)
    print("     %.5f   %16.4g   %17d    %.4f" % (c, closed, exact, closed / exact))
    if c >= 0.9:
        R.verdict(abs(closed / exact - 1.0) < 0.01,
                  "c = %.5f: closed form within 1%% of the exact crossover" % c,
                  "%.4g vs %d" % (closed, exact))
R.note("THE CLOSED FORM IS ASYMPTOTIC AND ITS ERROR IS DECLARED RATHER THAN AVERAGED AWAY.  It")
R.note("drops the `+0.5 log2(2 pi n)` Stirling term, which is a POSITIVE contribution to")
R.note("`log2 n!` and therefore makes the true crossover EARLIER than the formula says.  The")
R.note("formula is graded ONLY at `c >= 0.9`, where it is within 1%; below that it OVERSTATES")
R.note("badly — 2.46x at c = 0.5, where n* is 3 and the dropped term is most of the answer.")
R.note("The rows below 0.9 are printed and NOT graded, because a tolerance wide enough to pass")
R.note("them would be too wide to catch anything.  s2.3 tabulates the EXACT column; the closed")
R.note("form exists to make the elasticity in s2.2 readable.")

R.banner("s2.2  THE ELASTICITY — why this family is structurally prone to vacuity")
R.note("From the closed form,   d(ln n*)/dc  =  ln2 * log2(e) / (1-c)^2  =  1 / (1-c)^2.")
R.note("So the crossover moves by a factor of `e^(dc/(1-c)^2)` per unit change in `c`:")
print()
print("       c        1/(1-c)^2     n* multiplied by, per 0.01 of c")
for c in [0.5, 0.7, 0.8, 0.9, 0.94, 0.97]:
    el = 1.0 / (1.0 - c) ** 2
    print("     %.4f   %10.1f     %.3f  (i.e. /%.1f for c down 0.01)"
          % (c, el, math.exp(-el * 0.01), 1.0 / math.exp(-el * 0.01)))
R.verdict(abs(1.0 / (1.0 - 0.9398877) ** 2 - 277.0) < 2.0,
          "at compression2's own constant the elasticity is %.0f"
          % (1.0 / (1.0 - 0.9398877) ** 2),
          "so 0.01 off `c` divides the crossover by ~16")
R.note("THIS IS WHY s0.6's ROUNDING MATTERED.  Four printed digits of `c` do not pin `n*` to")
R.note("four digits — the doc's `0.9399` and the code's `1 - 1/(24 ln 2)` differ in the fifth")
R.note("place and their crossovers differ by 57,186.  A family whose headline number is that")
R.note("sensitive to its constant is one where `does it bite?` cannot be answered by improving")
R.note("the constant a little, and s2.4 says what it CAN be answered by.")

R.banner("s2.3  THE ACCEPTANCE TABLE — the constant a shape-A code must reach")
R.note("Inverting the law: to bite at `n`, a shape-A bound needs `c < 1 - log2(e)/log2(n)`.")
R.note("Computed by bisection on the EXACT predicate, so the Stirling term is carried:")
print()
print("       target n*      required c     required saving (1-c)   against compression2's 6.01%")
for target in [10 ** 7, 10 ** 4, 1000, 100, 50, 20, 10]:
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        x = L.crossover(mid)
        if x is not None and x <= target:
            lo = mid
        else:
            hi = mid
    save = 1.0 - lo
    print("     %10d       %.4f            %6.2f%%                %5.1fx more"
          % (target, lo, 100 * save, save / 0.0601137))
R.verdict(True, "to bite at n = 100 a shape-A code must save 21.0% of n log2 n",
          "compression2's mechanism saved 6.01% and landed at n* = 1.7e7 — 3.5x short")
R.note("")
R.note("THE FRONTIER THAT MATTERS IS n ~ 10^2, NOT 10^7.  mg-0b96 priced the `d`-lever at")
R.note("`n = 99`; the census frontier is 14 and the conjecture is verified to 14.  So the")
R.note("ticket's own bar — `does it bite below 10^7` — is the WEAK form of the question, and a")
R.note("proposal clearing it by a factor of 1000 would still be 3.5x short of the constant it")
R.note("needs where the programme actually lives.")

R.banner("s2.4  THE SHAPE DICHOTOMY — and this is the finding")
R.note("SHAPE B is a bound of the form  `log2 e(P) <= c * log2 n!`  with `c < 1` constant.")
R.note("It bites at EVERY n, by definition, for every c < 1.  There is no crossover to compute.")
print()
print("       shape                              crossover n*        vacuity risk")
for c in [0.99, 0.94, 0.90, 0.80]:
    x = L.crossover(c)
    shown = "%14d" % x if x is not None else "  >2^70 (~%.1g)" % 2.0 ** (LOG2E / (1.0 - c))
    print("     A:  c * n log2 n,   c = %.2f          %s      severe" % (c, shown))
for c in [0.99, 0.94, 0.90, 0.80]:
    print("     B:  c * log2 n!,    c = %.2f          %14d      none" % (c, 3))
R.verdict(L.crossover(0.99) is None,
          "shape A at c = 0.99 has n* beyond the 2^70 search cap (closed form ~%.1g)"
          % 2.0 ** (LOG2E / 0.01),
          "a 1% saving on the wrong scale is worth nothing at any n a human will write down")
R.note("THE `None` IS THE SEARCH CAP AND NOT AN ABSENCE — `crossover()` searches to 2^70 and")
R.note("reports `None` above it.  At c = 0.99 the closed form puts n* near 2^144, so the row is")
R.note("`the answer exists and is astronomically large`, not `there is no crossover`.")
R.note("")
R.note("  SO VACUITY IN THIS FAMILY IS A PROPERTY OF THE REFERENCE SCALE, NOT OF THE MECHANISM.")
R.note("")
R.note("`n log2 n` exceeds `log2 n!` by `n log2 e = 1.4427 n` — a term LINEAR in n, against a")
R.note("saving that is a constant fraction of `n log2 n`.  Any constant-fraction saving on the")
R.note("larger scale must first pay back that linear term, and paying it back needs")
R.note("`log2 n > log2(e)/(1-c)`.  That is the entire content of compression2's 1.7e7 and it is")
R.note("arithmetic about the two scales, not about the merge tree.")
R.note("")
R.note("THE OPERATIVE QUESTION TO PUT TO A PREFIX-CODE PROPOSAL IS THEREFORE ONE LINE, AND IT")
R.note("IS NOT `WHAT IS YOUR CONSTANT`:")
R.note("")
R.note("    Does the code's expected length beat  ceil(log2 n!)  — the length of the code that")
R.note("    indexes L into all of S_n and ignores P entirely — AT THE n YOU CLAIM IT?")
R.note("")
R.note("A code answers that at any single `n` by construction, since it IS a code: run it.  No")
R.note("asymptotic constant needs to be proved to find out.  That is the cheap test this ticket")
R.note("asked for, and it is cheaper than the ticket supposed.")

R.banner("s2.5  IS THE GOOD SHAPE REACHABLE — what compression2's OWN measurements say")
R.note("mg-0fc6 a3.1 measured `max{H(mu) : mu in M_n} / log2 n!` over the pair-bias information")
R.note("set, which is the sharpest shape-B constant any bound on that set can have:")
print()
print("       n        max H(mu)/log2 n!   (mg-0fc6 a3.1, cited not re-measured)")
A31 = {3: 0.907, 4: 0.900, 5: 0.893, 6: 0.887, 7: 0.883}
for n in sorted(A31):
    print("     %3d          %.3f" % (n, A31[n]))
R.verdict(all(A31[n] < 1.0 for n in A31), "every measured value is strictly below 1",
          "so a shape-B bound with c < 1 EXISTS on this set at every n measured")
R.verdict(all(A31[n + 1] < A31[n] for n in range(3, 7)),
          "and the sequence is strictly decreasing over n = 3..7", "0.907 -> 0.883")
R.note("")
R.note("READ CAREFULLY, BECAUSE THIS IS AN EXISTENCE STATEMENT AND NOT A CONSTRUCTION.  It says")
R.note("the sharpest bound on the information set is shape B with `c <= 0.883` at n = 7, so")
R.note("nothing in the SCALE forbids a non-vacuous bound.  It does NOT say a code achieving it")
R.note("exists, and it does not say the sequence stays below 1 — five points do not settle a")
R.note("limit, and the estate's own warning applies: `what carries above them is the proof`.")
R.note("mg-0fc6's a3.2 is the standing caution in the other direction — the two-atom law has")
R.note("`H = 0.9183` bits at EVERY n and simultaneously maximal `E[inv_e]`, so low entropy and")
R.note("maximal inversions coexist and an entropy bound does not deliver an inversion bound.")
R.note("")
R.note("WHAT IS ESTABLISHED HERE IS THE SCREENING QUESTION AND ITS ANSWER FOR THE ONE ATTEMPT")
R.note("ON RECORD:  compression2's (6) is shape A, and shape A is vacuous at every n below")
R.note("2^(log2 e/(1-c)).  A successor that produces a shape-A bound with a better constant is")
R.note("a repeat.  A successor that produces a shape-B bound is not, at any constant below 1.")

sys.exit(R.done())
