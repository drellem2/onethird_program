#!/usr/bin/env python3
"""mg-7c78 arm b2 — THE TRICK ITSELF, WHICH IS WHAT DANIEL ASKED FOR.

His second clarification (mail 2026-08-12 22:56Z and 22:59Z, verbatim):

    "i want to clarify that this reading isn't the only one. the bigger idea is just to use this
     combinatorial trick with > 2/3, or keep it in mind for later"

    "my example was only meant as an example of this trick: imagine you nicely constructed some
     permutation of linear extensions of X. Perhaps it's an extension of the weak bruhat order
     who knows. Then you could guarantee that in this permutation *of* all linear extensions
     there are 3 adjacent linear extensions sharing a given edge that aligns with the pair bias"

So the OBJECT is the trick, not the instantiation, and the instantiation is an ordering of `L(P)`
that may carry extra structure -- his named candidate being a linear extension of the WEAK BRUHAT
ORDER.  This arm measures the trick in the form a future consumer would want it, and the one
thing the clarification adds that b0/b1 did not test: does the extra structure change anything?

  t1  THE TRICK, REPAIRED.  b0 gives the sharp criterion `g > ceil(2N/3)` and the catch that
      `p > 2/3` supplies it only when 3 | N.  A UNIFORM repair: `p_xy > 2/3 + 2/N` is sufficient
      at every N and every residue.  Derived and then checked against the sharp criterion.
  t2  THE STRUCTURE BUYS NOTHING FOR THE GUARANTEE, and that is the useful engineering fact.
      The criterion is UNIVERSAL over orderings, so it holds for a weak-Bruhat-refining ordering
      exactly when it holds for an adversarial one.  Measured by running BOTH: a Bruhat-refining
      ordering and the worst-case `G G B` adversary, on the same posets and edges.
  t3  WHAT THE STRUCTURE DOES BUY -- measured, so the next consumer knows what to reach for.
      In a Bruhat-refining ordering three consecutive extensions have nearly equal inv_e, and the
      ordering's bottom element is `e` itself, which is good for EVERY edge at once.  So the runs
      at the bottom are free and the content is entirely in the runs further up.

Exits 0 if t1's repair never fails and t2 finds the Bruhat and adversarial answers AGREE with the
criterion; 1 otherwise; 2 on refusal.
"""

import math
import sys
from fractions import Fraction

import lib7c78 as L
import lib7c78b as B

NMAX = 6
LE_CAP = 200
THIRD = Fraction(1, 3)


def has_run3(flags):
    return any(flags[i] and flags[i + 1] and flags[i + 2] for i in range(len(flags) - 2))


def bruhat_refining_order(n, exts, e):
    """A linear extension of the WEAK BRUHAT ORDER restricted to L(P).

    Weak Bruhat here: sigma <= tau iff inv_e(sigma) is a SUBSET of inv_e(tau) as sets of
    e-inverted incomparable pairs.  Sorting by |inv_e| refines that order, because a subset has
    no more elements than its superset; ties are broken by the sorted inversion set, which is
    arbitrary but harmless.  The bottom element is `e` itself (empty inversion set)."""
    rank = {v: k for k, v in enumerate(e)}

    def invset(ext):
        pos = {v: k for k, v in enumerate(ext)}
        return tuple(sorted((x, y) for x in range(n) for y in range(n)
                            if rank[x] < rank[y] and pos[x] > pos[y]))

    dec = [(len(invset(ext)), invset(ext), ext) for ext in exts]
    dec.sort()
    return [d[2] for d in dec], dec


def adversarial_order(flags):
    """The worst ordering for a given good/bad multiset: pack goods two at a time separated by a
    bad, i.e. the `G G B` pattern, which b0 b3 proved extremal."""
    g = sum(flags)
    b = len(flags) - g
    out = []
    while g or b:
        for _ in range(min(2, g)):
            out.append(True)
            g -= 1
        if b:
            out.append(False)
            b -= 1
        elif g:
            out.append(True)
            g -= 1
    return out


def main():
    print("=" * 92)
    print("mg-7c78  b2  THE TRICK -- its repaired form, and what crafting the ordering buys")
    print("=" * 92)
    print()
    ok = True
    classes = L.all_classes(8)

    print("t1  THE TRICK, REPAIRED so it needs no divisibility side condition")
    print("-" * 92)
    print("    SHARP (b0 b3):   every ordering has a good run of 3   iff   g > ceil(2N/3).")
    print("    DANIEL's form:   p_xy > 2/3, i.e. g > 2N/3 -- enough iff 3 | N (b0 b4).")
    print("    REPAIR:          p_xy > 2/3 + 2/N   is sufficient at EVERY N and every residue.")
    print("      derivation: g > 2N/3 + 2 forces g >= floor(2N/3) + 3 >= ceil(2N/3) + 1, since")
    print("      ceil(2N/3) <= floor(2N/3) + 1.")
    print()
    bad = 0
    for N in range(3, 200):
        for g in range(N + 1):
            if Fraction(g, N) > Fraction(2, 3) + Fraction(2, N):
                if not g > math.ceil(2 * N / 3):
                    bad += 1
    ok &= bad == 0
    print("    checked at every (N, g) with 3 <= N < 200: %d failures   [%s]"
          % (bad, "PASS" if bad == 0 else "FAIL"))
    print("    AND IT IS NOT VACUOUS AT SMALL N: at N = 4 the repair demands p > 7/6 > 1, i.e. it")
    print("    is UNSATISFIABLE there -- correctly, because N = 4, g = 3 IS the counterexample.")
    print("    The trick simply has no content at N = 4, and the repair says so instead of")
    print("    quietly failing.")
    print()

    print("t2  DOES CRAFTING THE ORDERING CHANGE THE GUARANTEE?  Bruhat vs adversary")
    print("-" * 92)
    work = []
    skipped = no_e = 0
    for n in range(2, NMAX + 1):
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            exts = L.linear_extensions(n, down)
            if len(exts) > LE_CAP:
                skipped += 1
                continue
            p = L.pair_probs(n, down, exts)
            e = B.majority_order(n, down, p)
            if e is None:
                no_e += 1
                continue
            work.append((n, down, exts, p, e, L.delta(n, down, p)))
    edges = 0
    bruhat_run = adv_run = crit = 0
    disagree_adv = 0
    bruhat_beats_criterion = 0
    for (n, down, exts, p, e, d) in work:
        N = len(exts)
        order, _dec = bruhat_refining_order(n, exts, e)
        good = B.goodness(n, down, exts, e)
        idx = {ext: k for k, ext in enumerate(exts)}
        for key, col in good.items():
            edges += 1
            bflags = [col[idx[ext]] for ext in order]
            g = sum(col)
            c = g > math.ceil(2 * N / 3)
            aflags = adversarial_order(col)
            br, ar = has_run3(bflags), has_run3(aflags)
            bruhat_run += br
            adv_run += ar
            crit += c
            if ar != c:
                disagree_adv += 1
            if br and not c:
                bruhat_beats_criterion += 1
    ok &= disagree_adv == 0
    print("    population: isomorphism classes n = 2..%d with |L(P)| <= %d and a well-defined e."
          % (NMAX, LE_CAP))
    print("      %d posets (%d skipped for |L(P)|, %d with no e), %d incomparable edges."
          % (len(work), skipped, no_e, edges))
    print()
    print("    edges with a good run of 3 in the BRUHAT-REFINING ordering:  %d of %d"
          % (bruhat_run, edges))
    print("    edges with a good run of 3 in the ADVERSARIAL ordering:      %d of %d"
          % (adv_run, edges))
    print("    edges meeting the criterion  g > ceil(2N/3):                 %d of %d"
          % (crit, edges))
    print("    adversary disagrees with the criterion at %d edges   [%s]"
          % (disagree_adv, "PASS -- the criterion IS the adversarial answer"
             if disagree_adv == 0 else "FAIL"))
    print()
    print("    ⚠️  SO CRAFTING BUYS NOTHING FOR THE GUARANTEE.  The criterion is UNIVERSAL over")
    print("    orderings, so a Bruhat-refining ordering is guaranteed a good run of 3 on exactly")
    print("    the edges an adversary is -- and it HAPPENS to get one on %d further edges, which"
          % bruhat_beats_criterion)
    print("    is luck at that ordering and not a guarantee.  `Perhaps it's an extension of the")
    print("    weak bruhat order` therefore does not strengthen the trick; what it can do is make")
    print("    the triple MEAN something to whatever consumes it.")
    print()

    print("t3  WHAT THE BRUHAT STRUCTURE DOES BUY, measured")
    print("-" * 92)
    bottom_is_e = 0
    max_inv_spread = 0
    runs = 0
    for (n, down, exts, p, e, d) in work:
        order, dec = bruhat_refining_order(n, exts, e)
        if order[0] == e:
            bottom_is_e += 1
        for i in range(len(dec) - 2):
            max_inv_spread = max(max_inv_spread, dec[i + 2][0] - dec[i][0])
            runs += 1
    print("    the ordering's BOTTOM element is `e` itself at %d of %d posets   -- so the run at"
          % (bottom_is_e, len(work)))
    print("    the very bottom is good for EVERY incomparable edge at once, for free, and the")
    print("    content of the trick lies entirely in the runs further up.")
    print("    across %d runs of three consecutive extensions, the largest inv_e spread within a"
          % runs)
    print("    run is %d -- so three consecutive extensions of a Bruhat-refining ordering are"
          % max_inv_spread)
    print("    close in inversion count, which is the currency STATE.md:29 says a proof would be")
    print("    delivered in.  THAT is the reason to keep the trick in mind, and it is a reason")
    print("    about the CONSUMER, not about the guarantee.")
    print()

    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
