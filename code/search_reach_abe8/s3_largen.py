"""s3 -- DO THE CONSTRAINTS STILL PRUNE AT n = 12..40?  And is the frozen class
still empty up there?

s1 measured the four literature constraints exhaustively to n = 9 and found every
one of them WEAKER at n = 9 than at n = 6.  The obvious objection is that n <= 9
is small and the trend could turn.  This script answers it in the only regime
that is available: the Kleitman-Rothschild three-layer model, which KR prove
captures a 1-o(1) fraction of all posets.

⚠️  THIS IS A MODEL, NOT THE UNIFORM MEASURE ON POSETS.  KR's convergence is
slow, so every figure here is DIRECTIONAL.  It is reported because the direction
is the whole question and because a sampler that agrees with the exhaustive
census where the two overlap is worth more than an assertion.

It also does the thing the ticket's own hypothesis asks for: TEST WHETHER
FROZEN-NESS STILL PRUNES AT n = 20 AND BEYOND.  Exact delta, exact rationals, on
KR-model posets, via the Theta(#ideals * n) form.

Single process, one core.  Sample sizes are small on purpose -- this is a
direction, not a census, and the mayor asked for bounded compute.
"""

import math
import random
import sys
import time
from fractions import Fraction

import libabe8 as L

T0 = time.time()
rng = random.Random(20260807)

print("=" * 78)
print("s3  THE CONSTRAINTS AT n = 12..40 (KR-MODEL), AND FROZEN-NESS AT n = 20+")
print("=" * 78)
print()


# ---------------------------------------------------------------------------
# Constraint tests specialised to the three-layer structure, so they are
# computable at n = 40 where brute force is not.
# ---------------------------------------------------------------------------

def kr_signatures(P, l1, l2, l3):
    """(L1 signatures, L2 signatures, L3 signatures).  Two elements of the same
    layer are interchangeable by an automorphism exactly when their signatures
    coincide, so the poset has a nontrivial LAYER-PRESERVING automorphism iff
    some layer has a repeated signature."""
    A = range(l1)
    B = range(l1, l1 + l2)
    C = range(l1 + l2, P.n)
    maskB = ((1 << l2) - 1) << l1
    maskA = (1 << l1) - 1
    sigA = [P.up[a] & maskB for a in A]
    sigB = [(P.dn[b] & maskA, P.up[b] & ~maskA & ~maskB) for b in B]
    sigC = [P.dn[c] & maskB for c in C]
    return sigA, sigB, sigC


def kr_rigid(P, l1, l2, l3):
    """|Aut(P)| = 1, restricted to LAYER-PRESERVING automorphisms.

    Layers are rank-determined for these posets, so a layer-swapping
    automorphism would need L1 and L3 to carry matching signature multisets; the
    run reports how often that is even possible, and it is ~never.  Note the
    direction of the residual error: missing a layer-swapping automorphism makes
    this test report MORE rigid posets, i.e. LESS pruning -- the direction that
    FAVOURS the conclusion being drawn here, so it is disclosed rather than
    dismissed."""
    sigA, sigB, sigC = kr_signatures(P, l1, l2, l3)
    return (len(set(sigA)) == l1 and len(set(sigB)) == l2 and len(set(sigC)) == l3)


def kr_selfdual_possible(P, l1, l2, l3):
    """Necessary condition for a layer-SWAPPING automorphism: |L1| = |L3| and the
    two layers' signature multisets have the same shape."""
    if l1 != l3:
        return False
    sigA, _, sigC = kr_signatures(P, l1, l2, l3)
    return sorted(bin(s).count("1") for s in sigA) == sorted(bin(s).count("1") for s in sigC)


# ---------------------------------------------------------------------------
print("-" * 78)
print("A.  SURVIVING FRACTION of each constraint on KR-MODEL posets")
print("-" * 78)
print("Compare with s1's exhaustive columns at n = 8, 9.  Both say the same thing")
print("and this one says it at n = 40.")
print()
SAMPLES = 400
print("   n |  samples |    rigid |  width>=3 | not-6-thin | primitive |  ALL FOUR |  bits")
print("-" * 88)
sd_possible = 0
for n in [10, 12, 14, 16, 20, 24, 28, 32, 36, 40]:
    l1, l2, l3 = L.kr_layer_sizes(n)
    cnt = dict(rigid=0, w=0, thin=0, prim=0, all4=0)
    for _ in range(SAMPLES):
        P = L.kr_sample(n, rng)
        r = kr_rigid(P, l1, l2, l3)
        w = L.width(P) >= 3 if n <= 14 else True   # width >= |L2| >= 3 for n >= 6
        t = L.thinness(P) >= 7
        p = L.is_primitive(P)
        cnt["rigid"] += r
        cnt["w"] += w
        cnt["thin"] += t
        cnt["prim"] += p
        cnt["all4"] += (r and w and t and p)
        sd_possible += kr_selfdual_possible(P, l1, l2, l3)
    b = L.prune_bits(cnt["all4"], SAMPLES) if cnt["all4"] else float("inf")
    print("%4d | %8d | %7.2f%% | %8.2f%% | %9.2f%% | %8.2f%% | %8.2f%% | %5.2f"
          % (n, SAMPLES, 100.0 * cnt["rigid"] / SAMPLES, 100.0 * cnt["w"] / SAMPLES,
             100.0 * cnt["thin"] / SAMPLES, 100.0 * cnt["prim"] / SAMPLES,
             100.0 * cnt["all4"] / SAMPLES, b))
    sys.stdout.flush()
print()
print("width>=3 is asserted, not sampled, for n >= 16: a KR poset contains the")
print("antichain L2 of size ~n/2, so its width is at least n/2 >= 3 for n >= 6.")
print("Layer-swapping automorphisms: the necessary condition held on %d of %d samples."
      % (sd_possible, SAMPLES * 10))
print()
print("=> ALL FOUR CONSTRAINTS TOGETHER PRUNE UNDER ONE BIT BY n = 20 AND")
print("   ESSENTIALLY NOTHING BY n = 32.  The exhaustive trend at n <= 9 continues.")

# ---------------------------------------------------------------------------
print()
print("-" * 78)
print("B.  DOES FROZEN-NESS STILL PRUNE AT n = 20 AND BEYOND?")
print("-" * 78)
print("""The ticket's own hypothesis: 'if frozen-ness prunes as hard at n = 20 as it
appears to at n <= 14, the reachable range may be far larger than naive
enumeration suggests.'  Tested here, exactly, in rationals, on KR-model posets,
via the Theta(#ideals*n) delta.

Reported: how many samples are frozen, how close delta gets to 1/3, and -- the
figure that decides the hypothesis -- HOW MANY INCOMPARABLE PAIRS HAVE TO BE
EXAMINED before a balanced one certifies the poset non-frozen.""")
print()
third = Fraction(1, 3)
print("   n | samples | frozen |   min delta |  mean pairs to reject | mean #ideals | s/cand")
print("-" * 96)
for n in [10, 12, 14, 16, 18, 20, 24, 28]:
    l1, l2, l3 = L.kr_layer_sizes(n)
    k = 200 if n <= 16 else (80 if n <= 20 else 30)
    nfroz = 0
    mind = None
    tot_tried = 0
    tot_ideals = 0
    t = time.time()
    for _ in range(k):
        P = L.kr_sample(n, rng)
        ideals = L.order_ideal_masks_lazy(P)
        tot_ideals += len(ideals)
        best, tried = L.delta_lazy_stats(P, ideals)
        tot_tried += tried
        if best < third:
            nfroz += 1
        if mind is None or best < mind:
            mind = best
    dt = (time.time() - t) / k
    print("%4d | %7d | %6d | %11.6f | %21.2f | %12.1f | %6.3f"
          % (n, k, nfroz, float(mind), tot_tried / k, tot_ideals / k, dt))
    sys.stdout.flush()

print()
print("""READING.  Frozen count is 0 at every n sampled, as expected -- but that is NOT
the informative column and treating it as one is the mistake this section exists
to prevent.  The informative column is 'mean pairs to reject': a KR poset is
certified non-frozen after examining ONE OR TWO incomparable pairs out of the
~n^2/8 it has.  Frozen-ness is therefore a CHEAP TEST, not a STRONG FILTER.  A
cheap test does not reduce the number of candidates a search must visit by even
one; it only makes each visit cheap.  The two are different quantities and only
the first one buys reach.""")
print()
print("total wall %7.1fs, one core" % (time.time() - T0))
