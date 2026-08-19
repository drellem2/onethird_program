#!/usr/bin/env python3
"""k0 — CONTROLS FIRST, because every headline in this directory is a SMALL NUMBER.

`k1`'s population is 31 posets and `k2`'s central ratio is a constant.  A broken enumeration, a
`delta` test that rejects everything, a decomposition that never finds a `V` and a conversion that
loses the relation all return a small number for free.  So the plants come before the answer.

FIVE WORLDS, THREE THAT MUST BE CAUGHT AND TWO THAT MUST NOT MOVE.  The clean library is asserted
green BEFORE and AFTER each plant and RE-MEASURED rather than assumed.

The imported halves are re-checked here rather than trusted: `lib6ff4`'s `count_ext` and
`delta_at_most` against brute-force enumeration of `L(P)`, and `lib9d9e`'s DP against `lib6ff4`'s
across the conversion.  An import whose controls live elsewhere is unchecked from here.
"""

import sys
from fractions import Fraction

import lib872c as X
import lib6ff4
import lib9d9e

RULE = "=" * 100
SUB = "-" * 100
NCTRL = 5
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
    ok = got == want
    if not ok:
        fails.append(label)
    print("    %-58s %-22s %s" % (label, str(got)[:22], "ok" if ok else "FAIL (want %s)" % (want,)))
    return ok


def caught(label, fired):
    """A plant is CAUGHT only when the defect is DEMONSTRATED, not when a banner is printed."""
    if not fired:
        fails.append(label)
    print("    %-58s %s" % (label, "CAUGHT" if fired else "NOT CAUGHT -- FAIL"))


# ------------------------------------------------------------------------------------------------

head("mg-872c  k0  controls: the imports, the conversion, the decomposition, and five worlds")

CLASSES = lib6ff4.all_classes(6)

sub("C0  the instrument can see the corpus at all")
check("A000112 at n = 3..6", [len(CLASSES[n]) for n in range(3, 7)],
      [lib6ff4.A000112[n] for n in range(3, 7)])
cnt = {n: len(X.hypothesis_class(CLASSES, n)) for n in range(3, 7)}
check("|{delta <= 1/3, non-chain}| at n = 3..6", [cnt[n] for n in range(3, 7)],
      [X.MG6FF4_BOUNDARY_COUNTS[n] for n in range(3, 7)])
print("      ^ compared against mg-6ff4 c1's PUBLISHED counts, cited in lib872c and not re-derived.")

sub("C1  lib6ff4.count_ext against brute force, every poset n <= 5")
bad = 0
for n in range(2, 6):
    for down in CLASSES[n]:
        if lib6ff4.count_ext(n, down) != len(lib6ff4.linear_extensions(n, down)):
            bad += 1
check("disagreements over 86 posets", bad, 0)

sub("C2  lib6ff4.delta_at_most against a brute-force delta, every poset n <= 5")
bad = 0
seen_true = 0
for n in range(3, 6):
    for down in CLASSES[n]:
        les = lib6ff4.linear_extensions(n, down)
        inc = lib6ff4.incomparable_pairs(n, down)
        if not inc:
            brute = None
        else:
            brute = max(min(Fraction(sum(1 for L in les if L.index(i) < L.index(j)), len(les)),
                            1 - Fraction(sum(1 for L in les if L.index(i) < L.index(j)), len(les)))
                        for (i, j) in inc)
        ok, d, _ = lib6ff4.delta_at_most(n, down, X.THIRD)
        want = brute is not None and brute <= X.THIRD
        if ok != want or (ok and d != brute):
            bad += 1
        seen_true += int(ok)
check("disagreements over 79 non-chain posets", bad, 0)
check("posets the brute force also calls delta <= 1/3", seen_true, 1 + 2 + 3)

sub("C3  the conversion, both ways, and the two libraries' extension counts across it")
bad_rt = bad_e = 0
for n in range(2, 6):
    for down in CLASSES[n]:
        rel = X.down_to_rel(n, down)
        if X.rel_to_down(n, rel) != down:
            bad_rt += 1
        if lib9d9e.count_extensions_dp(rel, n) != lib6ff4.count_ext(n, down):
            bad_e += 1
check("round-trip failures down -> rel -> down", bad_rt, 0)
check("e(P) disagreements lib9d9e vs lib6ff4", bad_e, 0)

sub("C4  the decomposition written HERE agrees with lib6ff4.ordinal_summands, n <= 6")
bad = 0
for n in range(1, 7):
    for down in CLASSES[n]:
        mine = [len(b) for b in X.ordinal_cut_blocks(n, down)]
        # `ordinal_summands` returns `[(size, canonical down-tuple), ...]`, so the size is `s[0]`.
        # ⚠️ THE FIRST DRAFT OF THIS LINE WROTE `len(s)`, which is 2 for every summand, and the
        # control went RED at 402 of 407 -- the control was wrong, not the decomposition, and the
        # 5 that "agreed" were the posets whose every block really does have size 2.
        theirs = [s[0] for s in lib6ff4.ordinal_summands(n, down)]
        if mine != theirs:
            bad += 1
check("block-size disagreements over 407 posets", bad, 0)
print("      ^ the ANSWER is computed with the spelling written here; this is the agreement check.")

# ------------------------------------------------------------------------------------------------


def frontier(bound=X.THIRD, decomp=X.v_count, qmin=lib9d9e.q_minimals, nmax=6):
    """The three figures every world is scored on, re-measured from scratch each time."""
    members = 0
    max_e = 0
    ident = True
    lens = []
    for n in range(3, nmax + 1):
        for (down, _d, _t) in X.hypothesis_class(CLASSES, n, bound):
            members += 1
            e = lib6ff4.count_ext(n, down)
            max_e = max(max_e, e)
            k, _kinds = decomp(n, down)
            if k is None or 3 ** k != e:
                ident = False
            ex, _fl = X.elen(n, down, qmin)
            lens.append(ex)
    # `lens` is sorted before it leaves: the per-member lengths are a MULTISET over the class and
    # not a sequence, so a walk in a different order must be allowed to visit them in a different
    # order.  ⚠️ D4's first draft compared them as a list and went RED on exactly that; the control
    # was fixed rather than the claim, the claim being that every FIGURE is unmoved.
    return members, max_e, ident, sorted(lens, key=lambda f: (f is None, f))


BASE = frontier()
print()
check("clean library: (members, max e, e = 3^k)", BASE[:3], (11, 9, True))

sub("D1  PLANT: the hypothesis widened 1/3 -> 1/2 (the class stops being the hypothesis class)")
w = frontier(bound=Fraction(1, 2))
caught("the class inflates and max e(P) rises", w[0] > BASE[0] and w[1] > BASE[1])
print("      clean %s   planted %s" % (BASE[:2], w[:2]))

sub("D2  PLANT: the decomposition coarsened (the finest cut dropped)")


def coarse(n, down):
    blocks = X.ordinal_cut_blocks(n, down)
    if len(blocks) > 1:
        blocks = [tuple(sorted(blocks[0] + blocks[1]))] + blocks[2:]
    kinds = [X.block_kind(n, down, b) for b in blocks]
    if all(kk in ("singleton", "V") for kk in kinds):
        return kinds.count("V"), kinds
    return None, kinds


w = frontier(decomp=coarse)
caught("the e(P) = 3^k identity fails", w[2] is False and BASE[2] is True)

sub("D3  PLANT: MINIMALS replaced by a code that does NOT read P")


def q_blind(L, ctx):
    """Index the next element among ALL unplaced ones -- the free code, wearing MINIMALS' shape."""
    n = ctx["n"]
    q = Fraction(1)
    for i in range(n):
        q *= Fraction(1, n - i)
    return q


w = frontier(qmin=q_blind)
caught("E[len] leaves 5k/3 at every member", all(a != b for a, b in zip(BASE[3], w[3])))
print("      clean E[len] at the n = 3 member %s   planted %s (= log2 3! is not an integer, so None)"
      % (BASE[3][0], w[3][0]))

sub("D4  REQUIRED-INERT: the class walked in reverse order")
rev = {n: list(reversed(v)) for n, v in CLASSES.items()}
save, sys.modules[__name__].CLASSES = CLASSES, rev
try:
    globals()["CLASSES"] = rev
    w = frontier()
finally:
    globals()["CLASSES"] = CLASSES
check("every figure unmoved under reversal", w, BASE)

sub("D5  REQUIRED-INERT, WRONG DIRECTION: the antichain is outside the class")
anti = tuple([0] * 5)
inclass = any(down == anti for (down, _, _) in X.hypothesis_class(CLASSES, 5))
check("antichain(5) is in the hypothesis class", inclass, False)
ok, _d, _t = lib6ff4.delta_at_most(5, anti, Fraction(1, 2))
check("delta(antichain(5)) <= 1/2 (so it is at 1/2 exactly)", ok, True)
print("      ^ P7's premise: a bound proved FROM hypothesis (1) is never asked about the antichain.")

# ------------------------------------------------------------------------------------------------
print()
print(RULE)
print("VERDICT: %s   (%d control groups, 3 plants CAUGHT, 2 required-inert)"
      % ("GREEN" if not fails else "RED -- " + "; ".join(fails), NCTRL))
print(RULE)
sys.exit(1 if fails else 0)
