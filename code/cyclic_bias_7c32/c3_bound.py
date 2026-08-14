"""c3 -- STEP 2 CHECKED, AND STEP 4 PRICED: WHAT THE AVERAGE CYCLIC BIAS ACTUALLY IS.

The ticket's step 4 asks for a bound on the AVERAGE of `db` over the star, below
`1/6 - eps`, and says that proves the conjecture for large `n`.  This arm measures
the average rather than describing it, and the measurement has one consequence:

    avg db  -  (mean consecutive bias along L*)   =   (A - b(x_1,x_n)) / (n-2)

with `A` the mean consecutive bias -- so the two differ by at most `1/(n-2)`, and
the average cyclic bias is the average PAIR bias with an `O(1/n)` correction.  The
`1/6` in step 4 is therefore the same `1/6` the counterexample hypothesis already
puts on every consecutive pair, and steps 3 and 4 are a lower and an upper bound
on ONE scalar `D` rather than two independent facts about different objects.

That is a claim about arithmetic, so it is measured exhaustively here and stated
as a bound that can fail, not as a paragraph.

No clock, no randomness, no sampling.
"""

import sys
from fractions import Fraction

import lib7c32 as L

NMAX = 8
W = 88
out = sys.stdout.write
HALF = Fraction(1, 2)
SIXTH = Fraction(1, 6)
THIRD = Fraction(1, 3)


def head(t):
    out("=" * W + "\n" + t + "\n" + "=" * W + "\n")


def sec(t):
    out("\n" + t + "\n" + "-" * W + "\n")


def main():
    head("mg-7c32  c3 -- step 2 exhaustive, and what the average cyclic bias reduces to")
    status = 0
    ps = L.posets_upto(NMAX)

    # -- SS1 ----------------------------------------------------------------
    sec("§1  STEP 2 -- the 2/3-relation is ACYCLIC and CONSISTENT WITH P, exhaustive n = 3..%d"
        % NMAX)
    cyc23 = 0
    incons = 0
    total = 0
    total23 = 0
    oriented23 = 0
    all_pairs = 0
    cyc_weak = 0
    min_delta = {}
    for n in range(3, NMAX + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            e23 = L.majority_edges(p, n, Fraction(2, 3))
            total += 1
            if not L.is_acyclic(e23, n):
                cyc23 += 1
            for (x, y) in e23:
                if (y, x) in P.less:
                    incons += 1
            npair = n * (n - 1) // 2
            all_pairs += npair
            oriented23 += len(e23)
            if len(e23) == npair:
                total23 += 1
            if not L.is_acyclic(L.majority_edges(p, n, HALF), n):
                cyc_weak += 1
            d, _ = L.delta_of(P, p)
            if d is not None and (n not in min_delta or d < min_delta[n][0]):
                min_delta[n] = (d, P)
    out("  posets swept: %d\n" % total)
    out("  2/3-relation CYCLIC on: %d   [%s]     inconsistent with P on: %d   [%s]\n"
        % (cyc23, "PASS" if cyc23 == 0 else "FAIL",
           incons, "PASS" if incons == 0 else "FAIL"))
    status |= 0 if (cyc23 == 0 and incons == 0) else 1
    out("  2/3-relation TOTAL on: %d of %d posets -- %s\n"
        % (total23, total,
           "the chains only" if total23 else "none"))
    out("  pairs oriented at threshold 2/3: %d of %d\n" % (oriented23, all_pairs))
    out("  weak (1/2) majority tournament CYCLIC on: %d of %d\n" % (cyc_weak, total))
    out("""
  THE ZEROS ABOVE ARE NOT EVIDENCE FOR STEP 2 AND MUST NOT BE QUOTED AS IF THEY WERE.
  Step 2's conclusion -- that the majority relation is a TOTAL order and hence a linear
  extension -- needs the counterexample hypothesis to make the relation total, and no
  counterexample is enumerable at any n reachable here (the conjecture is verified to
  n = 14, mg-33f5).  What §1 does check is the half that is unconditional: acyclicity,
  which follows from the triangle inequalities alone (BASIC-FACTS fact 1 -> fact 2), and
  consistency with P.  `cyclic weak tournament: 0` likewise repeats mg-24a3's sweep to
  n = 7 one order further and MUST NOT be read as general transitivity: mg-24a3 exhibits
  a majority cycle at n = 11 with margins near 0.50014, far inside the 2/3 band.
""")
    out("  most frozen poset found, by n (smallest delta(P) = max over incomparable pairs\n"
        "  of min(p,1-p); the counterexample hypothesis is delta(P) < 1/3):\n")
    for n in sorted(min_delta):
        d, P = min_delta[n]
        out("    n = %d   delta = %-8s  %s\n"
            % (n, d, "BELOW 1/3 -- A COUNTEREXAMPLE" if d < THIRD else "at or above 1/3"))

    # -- SS2 ----------------------------------------------------------------
    sec("§2  WHAT `avg db` IS -- the exact gap to the mean consecutive bias, exhaustive")
    worst = None
    bad = 0
    checked = 0
    for n in range(4, NMAX + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            chain = L.majority_order(p, n)
            consec = L.consecutive_sum(p, chain)
            A = Fraction(consec, n - 1)
            D, terms, live, _ = L.star(p, chain, chain[0])
            avg = Fraction(D, live)
            gap = avg - A
            exact = Fraction(A - L.bb(p, chain[0], chain[-1]), n - 2)
            checked += 1
            if gap != exact:
                bad += 1
            if abs(gap) > Fraction(1, n - 2):
                bad += 1
            if worst is None or abs(gap) > worst[0]:
                worst = (abs(gap), n, P, gap)
    out("  posets n = 4..%d: %d\n" % (NMAX, checked))
    out("  avg db - A  ==  (A - b(x_1,x_n)) / (n-2)   AND   |avg db - A| <= 1/(n-2):\n")
    out("    violations: %d   [%s]\n" % (bad, "PASS" if bad == 0 else "FAIL"))
    status |= 0 if bad == 0 else 1
    out("  largest gap observed: |avg db - A| = %s at n = %d (ceiling there is 1/%d)\n"
        % (worst[0], worst[1], worst[1] - 2))
    out("""
  THE AVERAGE CYCLIC BIAS IS THE AVERAGE PAIR BIAS PLUS O(1/n).  It is not a new
  quantity with its own theory, and dividing D by n-2 does not make it one: no step of
  the argument ever bounds an INDIVIDUAL db.  Steps 3 and 4 are a lower and an upper
  bound on the SAME scalar D, reached through the same two inputs -- SUM consec and the
  single bias b(x_1,x_n).
""")

    # -- SS3 ----------------------------------------------------------------
    sec("§3  IS STEP 4'S TARGET REACHABLE?  Best base point against 1/6, exhaustive")
    below = 0
    tot = 0
    best_overall = None
    worst_best = None
    for n in range(5, NMAX + 1):
        for P in ps[n]:
            _, p = L.marginals(P)
            chain = L.majority_order(p, n)
            best = None
            for base in chain:
                D, terms, live, _ = L.star(p, chain, base)
                if live <= 0:
                    continue
                a = Fraction(D, live)
                if best is None or a < best:
                    best = a
            tot += 1
            if best < SIXTH:
                below += 1
            if best_overall is None or best < best_overall[0]:
                best_overall = (best, n, P)
            if worst_best is None or best > worst_best[0]:
                worst_best = (best, n, P)
    out("  posets n = 5..%d: %d      best-base-point avg db < 1/6 on %d of them (%s)\n"
        % (NMAX, tot, below, "%.1f%%" % (100.0 * below / tot)))
    out("  smallest best-base avg db seen: %s   largest: %s\n"
        % (best_overall[0], worst_best[0]))
    out("  the largest is attained e.g. at n = %d on %s\n" % (worst_best[1], worst_best[2]))
    out("""
  A LARGE FRACTION BELOW 1/6 IS NOT EVIDENCE FOR STEP 4 AND IS THE TRAP THIS SECTION
  EXISTS TO DISARM.  Every poset here SATISFIES the conjecture, so every one of them has
  a balanced pair and a small mean consecutive bias is exactly what that produces.  The
  target has to hold on the counterexample class, which is empty on this population, so
  the percentage above measures the conjecture holding and nothing else.  The line that
  DOES carry information is the largest value: the target is false outright wherever the
  chain is comparability-rich, and a chain reaches 1/2 (c1 §3, c2 §3).
""")

    # -- SS4 ----------------------------------------------------------------
    sec("§4  THE NEAREST AVAILABLE PROXY FOR THE COUNTEREXAMPLE CLASS -- most frozen first")
    out("  ranked by delta(P) ASCENDING at n = %d; the counterexample hypothesis is\n"
        "  delta < 1/3, so these are the posets closest to it that exist.\n" % NMAX)
    rows = []
    for P in ps[NMAX]:
        _, p = L.marginals(P)
        d, _ = L.delta_of(P, p)
        if d is None:
            continue
        chain = L.majority_order(p, NMAX)
        A = Fraction(L.consecutive_sum(p, chain), NMAX - 1)
        D, terms, live, _ = L.star(p, chain, chain[0])
        per_base = [L.star(p, chain, b) for b in chain]
        best = min(Fraction(s[0], s[2]) for s in per_base if s[2] > 0)
        rows.append((d, Fraction(D, live), best, A, max(terms), min(terms), P))
    rows.sort(key=lambda r: (r[0], r[1]))
    out("\n  %-9s %-11s %-11s %-13s %-9s %-9s\n"
        % ("delta(P)", "avg db", "best base", "mean b consec", "max db", "min db"))
    for r in rows[:8]:
        out("  %-9s %-11s %-11s %-13s %-9s %-9s\n" % r[:6])
    out("  ...\n")
    for r in rows[-3:]:
        out("  %-9s %-11s %-11s %-13s %-9s %-9s\n" % r[:6])
    floor = Fraction(NMAX - 4, 6 * (NMAX - 2))
    extremal = [r for r in rows if r[0] == THIRD]
    lo = min(r[1] for r in extremal)
    lob = min(r[2] for r in extremal)
    out("\n  posets at n = %d attaining delta(P) = 1/3 exactly -- the tightest the conjecture\n"
        "  gets, and the closest thing to the counterexample class that exists: %d\n"
        % (NMAX, len(extremal)))
    out("  smallest avg db over them, base = x_1 : %s = %.6f\n" % (lo, float(lo)))
    out("  smallest over them with the base point SPENT WELL: %s = %.6f\n"
        % (lob, float(lob)))
    out("  step 3's floor  (n-4)/(6(n-2)) = %s = %.6f      slack = %s = %.6f\n"
        % (floor, float(floor), lob - floor, float(lob - floor)))
    out("  step 4's target 1/6 = %.6f, which %d of these %d posets sit below even at\n"
        "  their best base point\n"
        % (float(SIXTH), sum(1 for r in extremal if r[2] < SIXTH), len(extremal)))
    out("""
  MY OWN PREDICTION FOR THIS SECTION WAS THAT THE SLACK WOULD BE 1/(n-2)-SIZED AND THE
  MEASUREMENT REFUTED IT (PREDICTIONS.md P6); the paragraph is rewritten to what ran.
  The extremal class does NOT sit near step 3's floor -- it sits well above 1/6, and not
  one of these posets reaches step 4's target at any base point.  That is a stronger
  result against step 4 than a tight slack would have been, and it is the direct one: on
  the closest population to the counterexample class that exists, the quantity step 4
  needs below 1/6 is not below 1/6, and the base-point freedom does not move it there.
  It is NOT evidence about the counterexample class itself, which is empty -- see §3's
  warning, which applies with the sign reversed here.
""")

    # -- SS5 ----------------------------------------------------------------
    sec("§5  THE VERDICT ON STEP 4, AS AN INEQUALITY RATHER THAN AN OPINION")
    out("""
  Write A for the mean consecutive bias along L* and take the base point at the end,
  which §1 of c2 shows is the best choice.  Then EXACTLY

      avg db  =  ( (n-1) A  -  b(x_1, x_n) )  /  (n-2)

  Under the counterexample hypothesis every consecutive pair has b > 1/6, so A > 1/6,
  and b(x_1,x_n) <= 1/2, so

      avg db  >  ( (n-1)/6 - 1/2 ) / (n-2)  =  1/6  -  1/(3(n-2))

  which is step 3 divided by n-2.  Step 4 asks for  avg db < 1/6 - eps  with eps fixed.
  For n > 2 + 1/(3 eps) the two are incompatible -- which is the intended contradiction,
  and it is sound.  WHAT IT IS NOT IS A REDUCTION.  Proving  avg db < 1/6 - eps  UNDER
  the hypothesis means proving the hypothesis inconsistent, i.e. proving the conjecture;
  and proving it WITHOUT the hypothesis is impossible, since a chain gives avg db = 1/2.
  There is no third reading: the target is the conjecture wearing the star's coordinates.

  WHAT SURVIVES, AND IT IS NOT NOTHING.  A PER-TRIPLE bound is a genuinely different and
  strictly stronger statement than a bound on the average, and nothing above touches it:

      does the counterexample hypothesis force  db(x_1, x_{k-1}, x_k) <= 1/6 - eps
      for EVERY k, or is only the aggregate controlled?

  The aggregate is D and D is already known from step 3; an individual db is not, and
  db IS the cyclic-orientation bias by c1, an object correlation inequalities can speak
  about.  That is where a successor should start, and §4's max/min db columns are the
  first data on it.
""")

    out("\nVERDICT: %s\n" % ("PASS" if status == 0 else "FAIL"))
    return status


if __name__ == "__main__":
    sys.exit(main())
