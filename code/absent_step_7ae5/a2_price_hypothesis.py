"""mg-7ae5 / A2 — PRICE THE HYPOTHESIS: how much does 'thin prefix' buy?

(T) is the 1/3-2/3 conjecture with an extra hypothesis: P has a prefix cut
with Delta_1 <= eps_0.  Its price is therefore the STRENGTH OF THAT
RESTRICTION, and nobody has measured it.  Op-Form §7.2 establishes exactly one
thing — the antichain is excluded (Delta_1 >= 1/2 on every prefix) — and
concludes the condition is 'genuinely restrictive' from that single object.

This section measures the class.  Exhaustive, exact, every poset on n <= 6.

Two populations, both reported, because they answer different questions:

  NORMAL-FORM  (poset, distinguished order) pairs — what Step 4 could hand
               the argument if the spectral argument delivered THIS order.
               A class with many linear extensions offers many chances.
  CLASS        isomorphism classes — thin if ANY order and ANY prefix works.
               The most generous reading of the hypothesis class.

And the stratification that matters: by delta(P).  No frozen poset exists (that
is the conjecture), so the frozen proxy is the LOW-delta stratum — the posets
closest to the boundary delta = 1/3 that exist at all.  P4 bets the hypothesis
is no more restrictive there than on the population; if that holds, the extra
hypothesis buys nothing where Step 6 has to spend it.
"""

from fractions import Fraction
from itertools import permutations
import sys

from lib7ae5 import (poset_iter, linear_extensions, incomparable, density,
                     delta, delta1, is_ordinal_sum_at)

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6

EPS = [Fraction(0), Fraction(1, 50), Fraction(1, 7), Fraction(1, 5),
       Fraction(17, 78), Fraction(1, 2), Fraction(1)]
EPS_LABEL = ['0', '1/50', '1/7', '1/5', '17/78', '1/2', '1']


def canonical(n, rel):
    """Isomorphism-class key: min over relabellings of the sorted relation."""
    best = None
    for p in permutations(range(n)):
        key = tuple(sorted((p[a], p[b]) for (a, b) in rel))
        if best is None or key < best:
            best = key
    return (n, best)


print("=" * 78)
print("mg-7ae5 / A2 — THE PRICE OF THE 'THIN PREFIX' HYPOTHESIS, n <= %d" % NMAX)
print("=" * 78)

rows = []          # one per normal form: (n, canon, minDelta1, delta, d, e)
for n in range(3, NMAX + 1):
    for rel in poset_iter(n):
        exts = linear_extensions(n, rel)
        inc = incomparable(n, rel)
        if not inc:
            continue                       # the chain: no pair, not a candidate
        md = min(delta1(n, rel, exts, k) for k in range(1, n))
        rows.append((n, canonical(n, rel), md, delta(n, rel, exts),
                     density(n, rel), len(exts)))

print("\nA. THE CLASS, ON BOTH POPULATIONS")
print("\n   NORMAL-FORM population — (poset, distinguished order) pairs")
print("   %-4s %-8s %s" % ('n', 'total', '  '.join('%7s' % l for l in EPS_LABEL)))
for n in range(3, NMAX + 1):
    sub = [r for r in rows if r[0] == n]
    line = []
    for e in EPS:
        c = sum(1 for r in sub if r[2] <= e)
        line.append('%7s' % ('%.4f' % (c / len(sub))))
    print("   %-4d %-8d %s" % (n, len(sub), '  '.join(line)))

print("\n   CLASS population — thin if ANY order and ANY prefix is thin")
print("   %-4s %-8s %s" % ('n', 'classes', '  '.join('%7s' % l for l in EPS_LABEL)))
class_min = {}
for (n, canon, md, dl, d, e) in rows:
    if canon not in class_min or md < class_min[canon][0]:
        class_min[canon] = (md, n, dl, d)
for n in range(3, NMAX + 1):
    sub = [v for v in class_min.values() if v[1] == n]
    line = []
    for e in EPS:
        c = sum(1 for v in sub if v[0] <= e)
        line.append('%7s' % ('%.4f' % (c / len(sub))))
    print("   %-4d %-8d %s" % (n, len(sub), '  '.join(line)))

print("""
   Read: the fraction of the population admitting a prefix cut at or below
   each eps.  The eps = 0 column is EXACTLY the ordinal-sum-decomposable
   fraction (a0 §B proves the identity by exhaustion, both directions).""")

print("\nB. STRATIFIED BY delta(P) — the frozen proxy")
print("   No poset has delta < 1/3 (that is the conjecture).  The stratum that")
print("   matters is the one closest to it.\n")
for n in range(3, NMAX + 1):
    sub = [r for r in rows if r[0] == n]
    dmin = min(r[3] for r in sub)
    print("   n = %d   min delta over all posets = %s   (%d normal forms)"
          % (n, dmin, len(sub)))
    bands = [('delta = 1/3 exactly', lambda r: r[3] == Fraction(1, 3)),
             ('1/3 < delta <= 0.40', lambda r: Fraction(1, 3) < r[3] <= Fraction(2, 5)),
             ('delta > 0.40', lambda r: r[3] > Fraction(2, 5)),
             ('ALL', lambda r: True)]
    print("      %-22s %-7s %s" % ('band', 'count', '  '.join('%7s' % l for l in EPS_LABEL)))
    for label, pred in bands:
        band = [r for r in sub if pred(r)]
        if not band:
            print("      %-22s %-7d  — empty —" % (label, 0))
            continue
        line = []
        for e in EPS:
            c = sum(1 for r in band if r[2] <= e)
            line.append('%7s' % ('%.4f' % (c / len(band))))
        print("      %-22s %-7d %s" % (label, len(band), '  '.join(line)))
    print()

print("C. P3 / P4, SCORED")
n = NMAX
sub = [r for r in rows if r[0] == n]
frac_pop = sum(1 for r in sub if r[2] <= Fraction(1, 5)) / len(sub)
low = [r for r in sub if r[3] == Fraction(1, 3)]
frac_low = (sum(1 for r in low if r[2] <= Fraction(1, 5)) / len(low)) if low else None
print("   at n = %d, eps = 1/5 (the live calibration):" % n)
print("     whole population        %.4f" % frac_pop)
print("     delta = 1/3 stratum     %s"
      % ('%.4f' % frac_low if frac_low is not None else 'empty'))
mono = [sum(1 for r in rows if r[0] == k and r[2] <= Fraction(1, 5))
        / max(1, sum(1 for r in rows if r[0] == k)) for k in range(3, NMAX + 1)]
print("     by n: %s" % '  '.join('%.4f' % m for m in mono))
print("     rising in n?            %s"
      % all(mono[i] <= mono[i + 1] for i in range(len(mono) - 1)))
print("""
   P3 predicted 40-85 % at n = 6 and rising in n.
   P4 predicted the low-delta stratum is at least as thin-prefixed as the
   population — i.e. the hypothesis does NOT bite harder where it must.""")

print("\nD'. THE HYPOTHESIS CLASS AFTER MINIMALITY — the section that prices (T)")
print("""
   a0 §B4 checks exhaustively that delta(P[A] (+) P[B]) = max(delta P[A],
   delta P[B]).  So a DECOMPOSABLE frozen poset has a frozen SIDE, and a
   MINIMAL counterexample cannot be decomposable.  Step 6 therefore never sees
   any poset in the eps = 0 column: minimality removes it, unconditionally and
   for free.  What is left is the population (T) has content on.\n""")
print("   %-4s %-9s %-9s %-14s %s"
      % ('n', 'forms', 'indecomp', 'min Delta_1>0', 'delta = 1/3 among indecomposable'))
for n in range(3, NMAX + 1):
    sub = [r for r in rows if r[0] == n]
    ind = [r for r in sub if r[2] > 0]
    mp = min((r[2] for r in ind), default=None)
    at13 = sum(1 for r in ind if r[3] == Fraction(1, 3))
    print("   %-4d %-9d %-9d %-14s %d"
          % (n, len(sub), len(ind), str(mp), at13))
print("""
   ⚠ THE RIGHT-HAND COLUMN IS NOT A FINDING OF THIS TICKET — IT IS A
   REPRODUCTION.  mg-832f's independent audit published it before this ticket
   existed (`:327`, verbatim: *'Above n = 3, every poset with delta <= 1/3 is an
   ORDINAL SUM' — 0 primitive at n = 4,5,6,7*), together with the n = 3
   exception and the delta <= 1/3 counts 3, 6, 9, 21.  a0 §C11 reproduces all
   four on this independent code path and they agree exactly.  What is new here
   is not the fact but its CURRENCY: because Delta_1 = 0 at a cut IFF the cut is
   an ordinal-sum split (a0 §B1/B2), mg-832f's structural fact is a statement
   about L4's hypothesis class — those posets sit at Delta_1 = 0, the CENTRE of
   it.\n""")
print("""   THE COLUMN ON THE RIGHT IS THE PRICE, AND ITS FIRST ROW IS AN EXCEPTION
   THAT MUST BE CARRIED RATHER THAN ROUNDED AWAY.

     n = 3   THREE posets attain delta = 1/3 and are INDECOMPOSABLE.  They are
             Op-Form Cl. 3.3's P0 = {a<b} u {c} and its relabellings — the
             object that document uses to prove minimality supplies no interior
             slack.  So the sentence 'delta = 1/3 forces decomposability' is
             FALSE, and it is false at the smallest n where it could be tested.
     n = 4,5,6   ZERO.  Every poset attaining delta = 1/3 exactly is ordinal-sum
             DECOMPOSABLE, hence carries a frozen side, hence is excluded by
             minimality before Step 6 ever runs.

   On the range where a minimal counterexample could live (n >= 15, Peczarski /
   Gupta via mg-33f5) the enumerable evidence is the second row, and it says:
   the objects closest to frozen that exist are exactly the objects Step 6 never
   has to handle, and they sit at Delta_1 = 0 — the CENTRE of L4's hypothesis
   class, not its edge.  The enumerable population therefore carries almost no
   evidence about the region where (T) has content.
   [FP over n <= %d, and n = 3 is a live exception inside it.  This is a
    non-refutation, not a theorem, and it says nothing above n = %d.]""" % (NMAX, NMAX))

print("""
   E. THE SHARPEST FROZEN PROXY THERE IS: the PRIMITIVE MINIMUM of delta —
      the poset closest to frozen that Step 6 could actually be handed.
      mg-832f measured the minimum (2/5, 4/11, 5/14 at n = 4,5,6; a0 §C11c).
      What nobody has asked is whether those minimisers have a THIN PREFIX,
      i.e. whether (T)'s hypothesis even reaches them.\n""")
print("      %-4s %-9s %-9s %s" % ('n', 'min delta', 'minimisers', 'their min Delta_1 over prefixes'))
for n in range(4, NMAX + 1):
    ind = [r for r in rows if r[0] == n and r[2] > 0]
    if not ind:
        continue
    pm = min(r[3] for r in ind)
    mins = [r for r in ind if r[3] == pm]
    vals = sorted(set(r[2] for r in mins))
    print("      %-4d %-9s %-9d %s"
          % (n, str(pm), len(mins), ', '.join(str(v) for v in vals)))
print("""
      Read against the live calibration eps_leak = 1/5 and the required-scope
      ceiling 1/7: a minimiser whose min Delta_1 is at or below those numbers is
      inside L4's hypothesis class, so (T) has to cover it.""")

print("\n   And what survives, per delta band, on the INDECOMPOSABLE population:")
print("      %-4s %-22s %-7s %s"
      % ('n', 'band', 'count', '  '.join('%7s' % l for l in EPS_LABEL)))
for n in range(4, NMAX + 1):
    ind = [r for r in rows if r[0] == n and r[2] > 0]
    for label, pred in [('delta = 1/3 exactly', lambda r: r[3] == Fraction(1, 3)),
                        ('1/3 < delta <= 0.40', lambda r: Fraction(1, 3) < r[3] <= Fraction(2, 5)),
                        ('delta > 0.40', lambda r: r[3] > Fraction(2, 5))]:
        band = [r for r in ind if pred(r)]
        if not band:
            print("      %-4d %-22s %-7d  — EMPTY —" % (n, label, 0))
            continue
        line = ['%7s' % ('%.4f' % (sum(1 for r in band if r[2] <= e) / len(band)))
                for e in EPS]
        print("      %-4d %-22s %-7d %s" % (n, label, len(band), '  '.join(line)))

print("\nD. WHAT THE eps = 0 COLUMN MEANS, STATED SO IT IS NOT OVERREAD")
print("""   Delta_1 = 0 at a cut IFF P = P[A] (+) P[B] there (a0 §B1/B2, exhaustive
   n <= 6, both directions, 0 violations).  So L4's name — 'near-ordinal-sum
   stability' — is literally accurate: eps_0 is a DISTANCE TO DECOMPOSABILITY,
   and (T) says every frozen poset within eps_0 of decomposable has a balanced
   pair.  A decomposable poset P[A] (+) P[B] is not special to the conjecture:
   it inherits its pairs from its two sides, which is what makes the transfer
   look plausible and what mg-d3c7's family shows is not enough.""")
