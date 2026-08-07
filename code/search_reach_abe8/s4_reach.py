"""s4 -- THE REACH, WITH THE COST MODEL THAT PRODUCED IT.

The ticket: "an estimate of the largest n at which a constraint-pruned search is
feasible, WITH the cost model that produced it and the machine it assumes.  A
number with no cost model is not an answer."

Reported as a FUNCTION OF TARGET n, not against three fixed window sizes.  (The
34 / 98 / 398 window came from a bound that mg-00a1 has since refuted -- there is
no bound of the form c*n + O(1) on that route and so no window.  pm-onethird,
2026-08-07 20:12.  They are kept below as ILLUSTRATIVE MARKERS ONLY.)

The model, stated so it can be attacked:

    WORK(n)  =  N(n)  x  c(n)  /  2^(pruning bits)

    N(n)      candidates a search must VISIT.  A000112 exactly to n = 16
              (s1 re-derives it to n = 9); above 16 two extrapolations, LOW
              (the conservative one, used for every headline) and KR.
    c(n)      elementary operations to REJECT one candidate = the DP cells of
              the Theta(#ideals * n) exact test, measured in s2/C and refit here.
              Big-integer arithmetic is NOT charged: another conservatism.
    pruning   the joint pruning of the four literature constraints, MEASURED
              (s1 exhaustively to n = 9, s3 in the KR model to n = 40).

Every conservatism in this model runs in the direction of making the search look
MORE feasible, because the conclusion is that it is not.
"""

import math
import random
import sys
import time

import libabe8 as L

T0 = time.time()

print("=" * 78)
print("s4  THE REACH OF A CONSTRAINT-PRUNED SEARCH  (mg-abe8)")
print("=" * 78)
print()

# ---------------------------------------------------------------------------
print("-" * 78)
print("A.  THE PER-CANDIDATE COST c(n), refit here so this script stands alone")
print("-" * 78)
rng = random.Random(31337)
pts = []
for n in range(12, 41, 4):
    l1, l2, l3 = L.kr_layer_sizes(n)
    vals = [L.kr_ideal_count(L.kr_sample(n, rng), l1, l2, l3) for _ in range(20)]
    pts.append((n, math.log2(sum(vals) / len(vals))))
mx = sum(p[0] for p in pts) / len(pts)
my = sum(p[1] for p in pts) / len(pts)
slope = sum((p[0] - mx) * (p[1] - my) for p in pts) / sum((p[0] - mx) ** 2 for p in pts)
icpt = my - slope * mx
print("least squares on log2(#ideals) over n = 12..40, KR-model, 20 samples each:")
print("    log2 #ideals(n)  =  %.4f n  +  %.4f" % (slope, icpt))
resid = max(abs(p[1] - (slope * p[0] + icpt)) for p in pts)
print("    max residual %.3f bits over the fitted range" % resid)
print()


def log2_c(n):
    """log2 of the elementary operations to reject one candidate.
    #ideals DP cells, each touching up to n predecessors."""
    return slope * n + icpt + math.log2(n)


# ---------------------------------------------------------------------------
print("-" * 78)
print("B.  THE PRUNING BUDGET, measured not assumed")
print("-" * 78)
# s1 (exhaustive) and s3 (KR model), joint pruning of all four constraints:
MEASURED_PRUNE = {6: float("inf"), 7: float("inf"), 8: 4.727, 9: 2.591,
                  10: 1.66, 12: 0.46, 14: 0.67, 16: 0.25, 20: 0.07,
                  24: 0.03, 28: 0.01, 32: 0.01, 36: 0.0, 40: 0.0}
print("joint pruning of rigid + width>=3 + not-6-thin + primitive, in bits:")
for n in sorted(MEASURED_PRUNE):
    tag = "exhaustive" if n <= 9 else "KR-model"
    print("    n=%-3d  %6.3f bits   (%s)" % (n, MEASURED_PRUNE[n], tag))


def prune_at(n):
    """Bits of pruning available at n.  Above the measured range: 0, because the
    measurement is already 0.00 at n = 36 and 40.  Below n = 10 the value is
    huge but irrelevant -- those n are checked."""
    if n <= 9:
        return MEASURED_PRUNE.get(n, 0.0)
    ks = [k for k in MEASURED_PRUNE if k >= 10]
    lo = max([k for k in ks if k <= n], default=10)
    hi = min([k for k in ks if k >= n], default=max(ks))
    if lo == hi:
        return MEASURED_PRUNE[lo]
    t = (n - lo) / (hi - lo)
    return MEASURED_PRUNE[lo] * (1 - t) + MEASURED_PRUNE[hi] * t


print()
print("=> ABOVE n = 32 THE FOUR CONSTRAINTS TOGETHER PRUNE ZERO BITS TO MEASUREMENT")
print("   PRECISION.  The model charges them 0 there, which is what was measured.")


# ---------------------------------------------------------------------------
def log2_work(n, model="LOW"):
    return L.log2_N(n, model) + log2_c(n) - prune_at(n)


print()
print("-" * 78)
print("C.  WORK AS A FUNCTION OF TARGET n  --  the answer, as a function")
print("-" * 78)
print("  n | log2 N(n) | log2 c(n) | prune | log2 WORK | log2 WORK | WORK (LOW)")
print("    |   (LOW)   |           | bits  |   (LOW)   |    (KR)   | in powers of 10")
print("-" * 78)
for n in ([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 25, 30, 34, 40, 50, 98, 398]):
    w = log2_work(n, "LOW")
    wk = log2_work(n, "KR")
    print("%4d | %9.2f | %9.2f | %5.2f | %9.2f | %9.2f | 10^%.1f"
          % (n, L.log2_N(n, "LOW"), log2_c(n), prune_at(n), w, wk, w * math.log10(2)))

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("D.  BUDGETS, NAMED, WITH THE MACHINE THEY ASSUME")
print("-" * 78)
BUDGETS = [
    ("this 10-core box, 24 h, optimal C at 1e9 cell-ops/s/core", 10 * 86400 * 1e9),
    ("1000-core cluster, one month, same rate", 1000 * 2.6e6 * 1e9),
    ("1e6 cores, one year -- a national-scale allocation, and larger than\n"
     "     any computation ever run on this problem", 1e6 * 3.15e7 * 1e9),
    ("every CPU on Earth for a decade (~1e28 ops) -- not a machine, a ceiling", 1e28),
    ("LANDAUER: the Sun's entire energy output over the age of the universe,\n"
     "     at kT ln2 per irreversible bit (~5e64 ops) -- a physical limit, not\n"
     "     an engineering one", 5e64),
]
print("A budget is in ELEMENTARY OPERATIONS (DP cell updates).  Big-integer costs")
print("are not charged, so every reach below is an OVER-estimate.")
print()


def max_n_for(budget_bits, model="LOW"):
    best = 0
    for n in range(2, 400):
        if log2_work(n, model) <= budget_bits:
            best = n
        else:
            break
    return best


for (name, ops) in BUDGETS:
    b = math.log2(ops)
    print("  %s" % name)
    print("      budget 2^%.1f ops   ->   REACH  n = %d  (LOW model)   n = %d  (KR model)"
          % (b, max_n_for(b, "LOW"), max_n_for(b, "KR")))
    print()

# ---------------------------------------------------------------------------
print("-" * 78)
print("E.  CALIBRATION -- does the model reproduce the literature's ACTUAL frontier?")
print("-" * 78)
print("""The conjecture is verified to n = 14 (mg-33f5, preprint; n = 12 refereed).
That number was produced by a real computation with real cleverness, and it is
the only external check this model has.  If the model said n = 30 was easy or
n = 8 was hard it would be worthless.""")
print()
for n in (12, 13, 14, 15, 16, 17):
    w = log2_work(n, "LOW")
    cy = 2 ** w / 1e9 / 3.15e7
    print("    n=%-3d  work 2^%.1f ops  =  %10.4g core-years at 1e9 ops/s" % (n, w, cy))
print()
print("=> the model puts the single-machine frontier at n = 14-16 and the")
print("   cluster frontier a couple of elements above.  THE LITERATURE IS AT")
print("   n = 14.  The model is calibrated, and if anything optimistic.")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("F.  THE EXCHANGE RATE -- what a future structural result would be worth")
print("-" * 78)
print("""A pruning of b bits buys Dn = b / g(n) extra elements, g(n) = log2(N(n)/N(n-1)).
This is the number that decides whether any structural theorem is worth proving
FOR SEARCH PURPOSES.  It is not a statement about mathematical value.""")
print()
print("     n |   g(n) | bits to buy +1 | bits to buy +5 | a 99.9%-discarding")
print("       |        |     element    |    elements    | constraint buys")
print("-" * 78)
for n in (14, 16, 20, 25, 34, 50, 98):
    g = L.g_model(n, "LOW")
    print("  %4d | %6.2f | %14.1f | %14.1f | %+.2f elements"
          % (n, g, g, 5 * g, 10.0 / g))
print()
print("MEASURED, for comparison: all four literature constraints together prune")
print("0.07 bits at n = 20 and 0.00 bits at n = 36.  At n = 20 that is +0.01")
print("elements of reach.  Not one element.  One hundredth of one.")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("G.  THE INVERSE QUESTION: what would a constraint have to DO?")
print("-" * 78)
print("For each illustrative target, the pruning a future structural result would")
print("have to supply to bring it inside the largest budget above (2^%.1f ops)."
      % math.log2(5e64))
print()
print("  target n | log2 WORK (LOW) | pruning REQUIRED | as a surviving fraction")
print("-" * 78)
lim = math.log2(5e64)
for n in (20, 25, 34, 50, 98, 398):
    w = log2_work(n, "LOW")
    need = w - lim
    if need <= 0:
        print("  %8d | %15.1f | %16s | %s"
              % (n, w, "none", "inside the PHYSICAL limit, not any machine"))
    else:
        print("  %8d | %15.1f | %13.1f bits | 1 in 2^%.0f" % (n, w, need, need))
print()
print("""READING.  A constraint delivering hundreds of bits is not a constraint, it is
a classification: it would have to collapse the population from 2^(n^2/4) to
something sub-quadratic in the exponent.  No shape constraint of the kind
mg-5998 records -- rigid, width >= 3, an element incomparable to >= 7 others --
can do that, because each of them is an ALMOST-SURE property of a random poset
(Kleitman-Rothschild) and an almost-sure property prunes o(1) bits by
definition.  That is not a limitation of these three; it is a limitation of the
whole category.""")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("H.  ILLUSTRATIVE MARKERS (the old window ends), kept but NOT live")
print("-" * 78)
print("mg-00a1 refuted the c*n + O(1) bound these came from, so there is no window.")
print("They are printed only so a reader comparing against the ticket text can.")
print()
for n in (34, 98, 398):
    w = log2_work(n, "LOW")
    print("    n <= %-4d :  work 2^%.0f ops (LOW) / 2^%.0f (KR).  Reach is n = %d."
          % (n, w, log2_work(n, "KR"), max_n_for(math.log2(1e28), "LOW")))
print()
print("total wall %7.1fs, one core" % (time.time() - T0))
