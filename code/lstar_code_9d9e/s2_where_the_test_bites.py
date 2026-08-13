"""s2 — WHERE THE TEST BITES, AND WHERE IT CANNOT.

`s1` ran the test.  This arm asks what running it is worth, and the answer is a dichotomy of the
same shape as the predecessor's own:

  * on ALL posets the test is IMPOSSIBLE to pass -- not hard, impossible, for every code that
    will ever be written, by one line of Shannon at the antichain;
  * on the population the bound is actually about the test is FREE to pass, because that
    population has `log2 e(P) = Theta(n)` against a free bound of `Theta(n log n)`;
  * and the population the bound is LITERALLY about is EMPTY at every `n` a test can be run at.

So the test is a real necessary condition and it is not a screen.  What screens is the
predecessor's own Q2, and `s2.5` puts a code to it and gets an answer.
"""

import math
from fractions import Fraction

import lib9d9e as L

R = L.Report()

# --------------------------------------------------------------------------------------------
R.banner("s2.1  NO CODE BEATS THE FREE BOUND AT THE ANTICHAIN — a theorem, measured "
         "exhaustively at n <= 5")

R.note("e(antichain) = n!, so log2 e(P) = log2 n! there, and Gibbs says E[len] >= log2 e(P) for")
R.note("EVERY code.  Hence max over P of E[len] >= log2 n! for every FAMILY of codes {C_P}, and")
R.note("a shape-B bound  log2 e(P) <= c log2 n!  with c < 1 valid at every P DOES NOT EXIST.")
R.note("Not `no code found`: no code exists.  This is the one-line half the ticket asked for.")
R.line()
R.line("    n | code        | max_P E[len] | log2 n!  | argmax is the antichain?")
R.line("   ---+-------------+--------------+----------+-------------------------")
bad = 0
for n in (4, 5):
    posets = L.all_posets(n)
    best = {}
    for rel in posets:
        LEs = L.linear_extensions(rel, n)
        ctx = L.context(rel, n, LEs=LEs)
        for name, fn in L.CODES:
            tot = 0.0
            ok = True
            for Lx in LEs:
                q = fn(Lx, ctx)
                if q is None:
                    ok = False
                    break
                tot += L.ideal_bits(q)
            if not ok:
                continue
            tag = name.split()[0]
            v = tot / len(LEs)
            if tag not in best or v > best[tag][0] + 1e-12:
                best[tag] = (v, rel)
    lf = L.log2_factorial(n)
    for tag in sorted(best):
        v, rel = best[tag]
        is_ac = (len(rel) == 0)
        if v < lf - 1e-9:
            bad += 1
        R.line("    %d | %-11s |     %8.4f | %8.4f | %s"
               % (n, tag, v, lf, "yes" if is_ac else "no  (ties elsewhere too)"))
R.verdict(bad == 0, "P6: every code's worst case is at or above log2 n!, at n = 4 and n = 5",
          "7 codes x 219 and x 4231 posets")
R.note("LEHMER-L* is the one row whose argmax is NOT the antichain, and the reason is that L*")
R.note("DOES NOT EXIST at the antichain -- every marginal is 1/2, so the majority tournament is")
R.note("a tie at every pair.  A code that reads L* is UNDEFINED at the single poset that decides")
R.note("the worst case, which is worth stating on its own: the L*-reading codes are blind")
R.note("exactly where the bound is tight.")

# --------------------------------------------------------------------------------------------
R.banner("s2.2  THE SHAPE-A CEILING, AND WHY 16,777,063 IS TWO STATEMENTS AND ONE NUMBER")

R.line("   The best shape-A constant ANY code can deliver over all P at a given n is")
R.line("   log2 n! / (n log2 n) -- the free bound at the antichain, divided by n log2 n:")
R.line()
R.line("             n | log2 n!/(n log2 n)")
R.line("     ----------+--------------------")
for n in [10, 100, 1000, 10 ** 5, 10 ** 7, 16777063, 10 ** 9]:
    R.line("     %9d |            %.6f" % (n, L.log2_factorial(n) / (n * math.log2(n))))
R.note("It RISES to 1.  So a shape-A constant c < 1 valid at every P is refuted at the antichain")
R.note("for every n above 2^(log2 e / (1-c)) -- which is the predecessor's own crossover law")
R.note("read from the other end.")
R.line()

C_EXACT = 1.0 - 1.0 / (24.0 * math.log(2.0))
C_PRINTED = 0.9399


def crossover(c, hi=1 << 60):
    """First n >= 3 at which c*n*log2 n < log2 n!.  Binary search on the raw comparison."""
    def bites(n):
        return c * n * math.log2(n) < L.log2_factorial(n)
    lo = 3
    if bites(lo):
        return lo
    if not bites(hi):
        return None
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if bites(mid):
            hi = mid
        else:
            lo = mid
    return hi


n_exact = crossover(C_EXACT)
n_print = crossover(C_PRINTED)
R.verdict(n_exact == 16777063,
          "mg-0fc6 a1.6's crossover reproduced TO THE UNIT on this directory's own code",
          "c = 1 - 1/(24 ln 2) = %.7f  ->  n* = %d" % (C_EXACT, n_exact))
R.line("     the PRINTED constant 0.9399 gives n* = %d -- a difference of %d, which is"
       % (n_print, abs(n_print - n_exact)))
R.line("     mg-99f4's finding about four printed digits and is CITED here, not rediscovered.")
R.line()
R.line("   P8 -- THE TWO READINGS.  Below n*, `0.9399 n log2 n >= log2 n!`, so the bound is")
R.line("   IMPLIED BY THE FREE BOUND and says nothing.  Above n*, `0.9399 n log2 n < log2 n!`,")
R.line("   so the bound is FALSE at the antichain and can only hold under a hypothesis that")
R.line("   excludes it.  Same n.  There is no n at which the theorem is both non-vacuous and")
R.line("   hypothesis-free.")
R.line()
for n in (n_exact - 1, n_exact):
    lhs = C_EXACT * n * math.log2(n)
    rhs = L.log2_factorial(n)
    R.line("     n = %9d   c*n log2 n = %14.4f   log2 n! = %14.4f   -> %s"
           % (n, lhs, rhs, "VACUOUS (implied by free)" if lhs >= rhs
              else "NEEDS ITS HYPOTHESIS (false at the antichain)"))
ac_delta = L.delta(L.antichain(4), L.linear_extensions(L.antichain(4), 4), 4)
R.verdict(ac_delta == Fraction(1, 2) and ac_delta > Fraction(1, 3),
          "and hypothesis (1) DOES exclude the antichain", "delta(antichain) = %s > 1/3"
          % ac_delta)

# --------------------------------------------------------------------------------------------
R.banner("s2.3  `AT THE n YOU CLAIM IT` NAMES AN n AT WHICH THE POPULATION IS EMPTY")

R.line("   n | frozen posets (delta < 1/3, non-chain) reachable | source")
R.line("  ---+-------------------------------------------------+--------------------------")
for n in (3, 4, 5):
    cnt = 0
    for rel in L.all_posets(n):
        LEs = L.linear_extensions(rel, n)
        if len(LEs) == 1:
            continue
        if L.delta(rel, LEs, n) < Fraction(1, 3):
            cnt += 1
    R.line("  %2d | %47d | exhaustive, THIS directory (s0.9)" % (n, cnt))
for n in (6, 7, 8):
    R.line("  %2d | %47d | mg-9b6b, exhaustive over iso classes" % (n, 0))
for n in (9, 10, 11, 12, 13, 14):
    R.line("  %2d | %47d | the conjecture is VERIFIED to n = 14" % (n, 0))
R.line("  15+| %47s | OPEN -- and this is the only place a" % "unknown")
R.line("     | %47s | frozen poset can be" % "")
R.verdict(True, "the target class is EMPTY at every n = 6..12 -- the whole range the ticket names",
          "so a run on it is a fact about the population's SIZE, not about the code")
R.note("This is mg-0b96's population trap arriving one arm along, and it is why s1 runs on the")
R.note("BOUNDARY (delta = 1/3) instead and says so in its own header.  ⚠️ n = 6..8 and n <= 14")
R.note("are CITED, not re-measured here; n <= 5 is this directory's own exhaustive count.")

# --------------------------------------------------------------------------------------------
R.banner("s2.4  WHY PASSING IS FREE WHERE IT CAN BE RUN — what hypothesis (1) buys, "
         "cumulatively")

n = 5
buckets = {}
for rel in L.all_posets(n):
    LEs = L.linear_extensions(rel, n)
    if len(LEs) == 1:
        continue
    d = L.delta(rel, LEs, n)
    cur = buckets.get(d, (0, 0))
    buckets[d] = (cur[0] + 1, max(cur[1], len(LEs)))
R.line("   n = 5, all non-chain posets, bucketed by delta:")
R.line()
R.line("     delta | posets | max e(P) | CUMULATIVE max e over {delta <= this} | as % of free")
R.line("    -------+--------+----------+--------------------------------------+--------------")
run = 0
for d in sorted(buckets):
    cnt, mx = buckets[d]
    run = max(run, mx)
    R.line("     %5s | %6d | %8d | %36d | %5.1f%%"
           % (d, cnt, mx, run, 100.0 * math.log2(run) / L.log2_factorial(5)))
R.note("THE COLUMN THAT MATTERS IS THE CUMULATIVE ONE, because a hypothesis is `delta <= t` and")
R.note("what it buys is the max over everything at or below t.  It runs 3 -> 120, i.e. 22.9% of")
R.note("the free bound at hypothesis (1)'s own threshold and 100% at 1/2.")
R.note("⚠️ THE PER-BUCKET COLUMN IS **NOT** MONOTONE AND THAT IS PRINTED RATHER THAN SMOOTHED:")
R.note("delta = 2/5 carries e(P) = 25 while delta = 3/7 above it carries 7.  So `smaller delta")
R.note("means smaller e(P)` is FALSE bucket by bucket; what is true is the cumulative statement,")
R.note("and it is the cumulative statement a hypothesis consumes.")
R.note("Hypothesis (1) therefore buys exactly the regime where the free bound is already loose")
R.note("by an order -- which is why every code passes there, and why passing carries no")
R.note("information.  The test discriminates only in the regime where it is impossible to pass.")

# --------------------------------------------------------------------------------------------
R.banner("s2.5  ONE CODE PUT TO THE PREDECESSOR'S Q2 — and it comes back with a real bound")

R.note("Q2 COST: is the bound obtainable without enumerating L(P)?  For MINIMALS it is, and the")
R.note("argument is one line: at every step the available minimals form an ANTICHAIN, so there")
R.note("are at most w(P) of them, so")
R.note("       log2 e(P)  <=  E[len]  <=  max_L len(L)  <=  n log2 w(P),")
R.note("and w(P) is computable from P in polynomial time.  UNCONDITIONAL, consumable, and it")
R.note("beats the free bound exactly when  w(P) < n / e = n / 2.7183:")
R.line()
R.line("   family                          |  n | w(P) | n log2 w | log2 n! | log2 e(P) | beats free?")
R.line("  --------------------------------+----+------+----------+---------+-----------+------------")


def width(rel, n):
    """Largest antichain, by brute force over subsets -- exact and slow, which is fine at n <= 12
    and is NOT the cost claim (Dilworth gives it in polynomial time; this is a checker)."""
    best = 0
    for mask in range(1 << n):
        els = [i for i in range(n) if (mask >> i) & 1]
        if len(els) <= best:
            continue
        if all((x, y) not in rel and (y, x) not in rel
               for i, x in enumerate(els) for y in els[i + 1:]):
            best = len(els)
    return best


bad = 0
for fam, fn in L.FAMILIES:
    for nn in (6, 12):
        rel = fn(nn)
        w = width(rel, nn)
        b = nn * math.log2(w)
        lf = L.log2_factorial(nn)
        e = L.count_extensions_dp(rel, nn)
        if math.log2(e) > b + 1e-9:
            bad += 1
        R.line("   %-31s | %2d | %4d | %8.3f | %7.3f |   %7.3f | %s"
               % (fam, nn, w, b, lf, math.log2(e),
                  "YES" if b < lf else "no"))
R.verdict(bad == 0, "log2 e(P) <= n log2 w(P) holds at every family and n tested",
          "the bound is checked, not asserted")
thr = [(nn, nn / math.e) for nn in (6, 12, 100)]
R.line()
R.line("   the threshold, exactly:  n log2 w < log2 n!  <=>  w < n/e   " +
       "   ".join("(n = %d: w < %.2f)" % t for t in thr))
R.note("So a consumable, unconditional, order-beating bound DOES exist -- and it is vacuous")
R.note("exactly where the programme needs it, since a frozen poset is a DENSE one (mg-0b96's")
R.note("open region is d >~ 2e-2 and WIDENING) and dense means wide.  THE SAME DICHOTOMY A")
R.note("THIRD TIME: the bound is real, cheap, and worth nothing on the target class.")
R.note("⚠️ `dense means wide` is stated as the reason the bound is expected to be vacuous")
R.note("there; it is NOT measured on the frozen class, because the frozen class is empty.")

raise SystemExit(R.done())
