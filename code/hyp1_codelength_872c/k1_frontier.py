#!/usr/bin/env python3
"""k1 — WHAT HYPOTHESIS (1) FORCES `e(P)` TO BE, on the class where it can be instantiated.

The ticket's honest question, in its own words: *"what does hypothesis (1) actually force `e(P)`
to be?  Not `<= c n log2 n` -- the boundary says `Theta(n)`."*

This arm answers it with a number rather than an order, and the number is a COROLLARY of a
structure result `mg-6ff4` `c1` `m4` already published rather than a new census:

    a boundary poset is  k >= 1  copies of V  ordinally summed with  n - 3k  singletons,

so  e(P) = 3^k  and  E(n) := max{ e(P) : delta(P) <= 1/3, non-chain }  =  3^floor(n/3).

⚠️ THE FROZEN CLASS `delta < 1/3` IS EMPTY AT EVERY `n` REACHED and that emptiness is this arm's
SUBJECT, not a caveat on its numbers (`mg-9b6b` §0's wording).  `EMPTY` is printed, never `0`.
"""

import sys

import lib872c as X
import lib6ff4

RULE = "=" * 100
SUB = "-" * 100
NMAX = 8
fails = []


def head(t):
    print(RULE)
    print(t)
    print(RULE)


def sub(t):
    print()
    print(t)
    print(SUB)


def check(label, got, want):
    if got != want:
        fails.append(label)
    print("    %-62s %-18s %s" % (label, str(got)[:18], "ok" if got == want else "FAIL (want %s)" % (want,)))


head("mg-872c  k1  the frontier of e(P) under hypothesis (1), n = 3..%d exhaustive" % NMAX)

CLASSES = lib6ff4.all_classes(NMAX)
CLASS = {n: X.hypothesis_class(CLASSES, n) for n in range(3, NMAX + 1)}

sub("m1  the population, and the two classes that must not be printed the same way")
print("      n   iso classes   {delta <= 1/3, non-chain}   {delta < 1/3} = FROZEN        mg-6ff4 c1")
for n in range(3, NMAX + 1):
    strict = sum(1 for (_d, d, _t) in CLASS[n] if d < X.THIRD)
    print("     %2d   %11d   %24d   %-27s  %d"
          % (n, len(CLASSES[n]), len(CLASS[n]), X.fmt_empty(strict, "frozen poset"),
             X.MG6FF4_BOUNDARY_COUNTS[n]))
check("counts reproduce mg-6ff4 c1's published table",
      [len(CLASS[n]) for n in range(3, NMAX + 1)],
      [X.MG6FF4_BOUNDARY_COUNTS[n] for n in range(3, NMAX + 1)])
check("total members at n <= 8 (docs/FACTS.md F19's 31)", sum(len(CLASS[n]) for n in CLASS), 31)
print("      ⚠️  The FROZEN column is EMPTY, not 0, and it carries NO information: delta < 1/3 IS")
print("          the counterexample condition and the conjecture is verified to n = 14 (mg-33f5).")
print("      ⚠️  So every figure below is about the BOUNDARY delta = 1/3, which is the closest")
print("          instantiable population to hypothesis (1) and is NOT the frozen class.")

sub("m2  the structure, re-derived here through lib872c's own decomposition")
bad = 0
kdist = {}
for n in range(3, NMAX + 1):
    for (down, _d, _t) in CLASS[n]:
        k, kinds = X.v_count(n, down)
        if k is None or k < 1:
            bad += 1
        else:
            kdist[(n, k)] = kdist.get((n, k), 0) + 1
check("members that are NOT k>=1 V's ordinally summed with singletons", bad, 0)
print("      per-n distribution of k (the number of V summands):")
for n in range(3, NMAX + 1):
    row = ", ".join("k=%d: %d" % (k, c) for (nn, k), c in sorted(kdist.items()) if nn == n)
    print("        n = %d   %s" % (n, row))
print("      ⚠️  CORROBORATION OF mg-6ff4 c1 m4, NOT NEWS.  It is re-taken because every figure")
print("          below is arithmetic on it, and a re-statement drifts (mg-d2c2).")

sub("m3  e(P) = 3^k at every member, and the frontier E(n) = max e(P)")
bad = 0
print("      n   E(n) = max e(P)   3^floor(n/3)   log2 E(n)   argmax (k)   log2 E(n) / n")
for n in range(3, NMAX + 1):
    best_e, best_k = 0, None
    for (down, _d, _t) in CLASS[n]:
        k, _ = X.v_count(n, down)
        e = lib6ff4.count_ext(n, down)
        if k is None or 3 ** k != e:
            bad += 1
        if e > best_e:
            best_e, best_k = e, k
    closed = 3 ** (n // 3)
    if best_e != closed:
        fails.append("E(%d) != 3^floor(n/3)" % n)
    print("     %2d   %15d   %12d   %9.4f   %10s   %13.4f"
          % (n, best_e, closed, X.log2_e_exact(best_k), "k = %d" % best_k,
             X.log2_e_exact(best_k) / n))
check("members where e(P) != 3^k", bad, 0)
print("      So  log2 E(n) = floor(n/3)*log2 3  ->  0.5283 n,  against a free bound of")
print("      log2 n! ~ n log2 n - 1.4427 n.  THETA(n), and the constant is exact.")
print("      ⚠️  The LOWER half E(n) >= 3^floor(n/3) holds at EVERY n and needs no census: it is")
print("          mg-9b6b §3's explicit family (floor(n/3) V's ordinally summed, chain-padded),")
print("          whose delta is 1/3 exactly by the ordinal-sum lemma.  The UPPER half is FP.")

sub("m4  the width, which is docs/FACTS.md F19 and is CITED rather than claimed here")
widths = sorted({lib6ff4.width(n, down) for n in CLASS for (down, _d, _t) in CLASS[n]})
check("widths present over all 31 members", widths, [2])
print("      F19 (FP, n <= 8, 31 members) already banks this.  What it buys HERE is that")
print("      mg-9d9e §5.3's benchmark  log2 e(P) <= n log2 w(P)  reads  n  bits on this class.")

sub("m5  MUST-FIRE: at delta <= 2/5 the same machinery returns a NON-degenerate answer")
print("      Without this, a sweep that had silently narrowed to nothing would print the same")
print("      small numbers and the same verdict (mg-9b6b's wrong-direction control).")
print("      n   |{delta <= 2/5}|   max e(P)   max w(P)   3^floor(n/3)   e strictly above?")
above_from5 = 0
widest = 0
for n in range(4, 8):
    cls25 = X.hypothesis_class(CLASSES, n, X.TWO_FIFTHS)
    me = max(lib6ff4.count_ext(n, d) for (d, _x, _y) in cls25)
    mw = max(lib6ff4.width(n, d) for (d, _x, _y) in cls25)
    widest = max(widest, mw)
    if n >= 5 and me > 3 ** (n // 3):
        above_from5 += 1
    print("     %2d   %16d   %9d   %8d   %12d   %s"
          % (n, len(cls25), me, mw, 3 ** (n // 3), "YES" if me > 3 ** (n // 3) else "no"))
check("n = 5,6,7 where max e(P) exceeds the 1/3 frontier", above_from5, 3)
check("the delta <= 2/5 class reaches width >= 3 (the 1/3 class does not)", widest >= 3, True)
print("      ⚠️  THE FIRST DRAFT OF THIS CONTROL REQUIRED BOTH AT EVERY n AND WENT RED AT n = 4,")
print("          where max e(P) = 5 > 3 but the widest member is still width 2.  P8 claimed width")
print("          >= 3 OF THE CLASS and a bigger e(P) from n >= 5; the control was corrected to the")
print("          claim actually made, and n = 4's width-2 row is printed rather than absorbed.")

print()
print(RULE)
print("VERDICT: %s" % ("GREEN" if not fails else "RED -- " + "; ".join(fails)))
print(RULE)
sys.exit(1 if fails else 0)
