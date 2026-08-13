"""c3 — WHAT THE IMAGE LOOKS LIKE INSIDE HYPOTHESIS (1).  THIS ARM IS CORROBORATION, NOT DISCOVERY.

READ THIS FIRST.  Everything this arm measures about the boundary class is ALREADY REGISTERED as
`docs/FACTS.md` F23 (from `mg-6ff4` §5.1) and F19 (from `mg-7c78` §5.3), and F23 is EXHAUSTIVE TO
`n = 9` where this arm reaches `n = 7`.  F23 states the density maximum
`max{ d(P) : delta(P) = 1/3 } = 4*floor(n/3)/(n(n-1))`, the saturation `eps_spec = d*n/(n+1)`
exactly at every member, and the class counts `sum_k C(n-2k, k)`.  This arm was written before its
author read F23; it is kept, and re-framed, for three reasons and NOT as a finding:

  1. it reaches the same numbers by a THIRD route — full labelled extension sweep at `n <= 6`
     against `mg-6ff4`'s isomorphism-class census and `mg-7c78`'s width sweep — and `2/3, 1/3,
     1/5, 4/15, 4/21` at `n = 3..7` agrees with F23's closed form at every term;
  2. it is where `mg-8b32`'s two homeless facts get re-derived independently (c3.4), which is
     what this ticket exists to file; and
  3. the population warning below has to be re-established on THIS instrument's own population
     before any of its other arms may quote a boundary number.

WHAT THE ARM IS FOR, THEN, IS THE CONSEQUENCE RATHER THAN THE MEASUREMENT: F23 says the boundary
class sits EXACTLY ON the pair-marginal supply bound, so the image contributes no slack there, and
`c2` says the image has no convex shadow anywhere.  Those two together are the scoping
recommendation, and neither of them is a number this arm produces.

NOW THE POPULATION WARNING, BECAUSE EVERY NUMBER BELOW IS INSIDE IT.  `delta(P) < 1/3` is the
counterexample condition and the (1/3)-(2/3) conjecture is verified to `n = 14` (`mg-33f5`,
cited), so THE STRICTLY FROZEN POPULATION IS EMPTY AT EVERY `n` AN INSTRUMENT CAN ENUMERATE.
c3.1 re-establishes that here exhaustively at `n <= 6` rather than quoting it.  Everything after
c3.1 is therefore measured on the CLOSED boundary `delta(P) <= 1/3`, which is a different set
from the hypothesis, and `docs/FACTS.md` F1's warning applies verbatim: a clean sweep over an
empty population carries no information, so the boundary is used because it is the largest
non-empty set the hypothesis touches, not because it is the hypothesis.

    B_n := { P : pi_ji <= 1/3 for every i < j }, i.e. hypothesis (1) with `L*` relabelled to the
    identity.  `mg-8b32`'s `b4.3` calls this same set "the hypothesis population" — its `72 of
    219` at `n = 4` is reproduced here as 48 non-total posets plus the 24 total orders.

    T3 (BOUNDARY RIGIDITY — **F23, corroborated here, not found here**).  Every poset in `B_n`
        has EVERY incomparable pair at flip EXACTLY `1/3`, so `sum of flips = m/3` and

            eps_spec(P) = 6 * (m/3) / (n^2 - 1) = d(P) * n/(n+1) = eps_sup(P) EXACTLY,

        i.e. `mg-0e8c`'s pair-marginal supply is not a bound at these points, it is an EQUALITY.
        F23 has this as `U-id` arithmetic plus an `FP` census to `n = 9`; this arm reproduces it
        at `n <= 7` from a different enumeration.

    C2 (THE SCOPING CONSEQUENCE, which is this ticket's business rather than F23's).  If the
        image contributes no slack where it meets hypothesis (1), then the whole remaining
        question row 8 can ask OF THE IMAGE is: how large can `d` be for a FROZEN poset?  That is
        F23's own `NOT` field — *"this is not a realizability fact and it is the opposite of
        one"* — reached from the image side, and it is why `c2`'s no-convex-shadow result closes
        the target rather than narrowing it.

c3.4 gives `mg-8b32`'s two homeless facts a second, independent derivation — this instrument's
marginal DP and rank computation share no code with `lib8b32`'s `kernel_basis` — and a REASON
for the first of them, which is stronger than a re-measurement.
"""

import math
from fractions import Fraction
from itertools import combinations

import lib_c776 as L

third = Fraction(1, 3)

# ------------------------------------------------------------------ c3.1

L.banner("c3.1  THE POPULATION — the strictly frozen set is empty, so this is the boundary; and\n"
         "      the chain restriction, VERIFIED on the full population before it is used at n = 7")
# ONE PASS over all 134 492 labelled posets at n <= 6, answering three questions at once: how
# many are strictly frozen (none), how many sit on the boundary, and whether every boundary
# poset has a coherent L* that it is a subrelation of.  The third is what makes c3.3's n = 7
# sweep exhaustive rather than a sample, and it is measured on the FULL population rather than
# on the restricted one — a restriction validated only inside its own image validates nothing.
tot = 0
LABELLED = {}
bad_l = bad_sub = seen = 0
for n in (3, 4, 5, 6):
    strict = boundary = chains = 0
    for up in L.all_posets(n):
        d, t, m = L.delta_and_flip(up, n, cap=third)
        if m == 0:
            chains += 1
            continue
        if d > third:
            continue
        boundary += 1
        if d < third:
            strict += 1
        seen += 1
        e, pi = L.e_and_marginals(up, n)
        st = L.lstar(pi, n)
        if st is None:
            bad_l += 1
            continue
        pos = {x: i for i, x in enumerate(st)}
        for x in range(n):
            for y in range(n):
                if up[x] >> y & 1 and pos[x] > pos[y]:
                    bad_sub += 1
    tot += strict
    LABELLED[n] = boundary
    L.note(f"n = {n}: {boundary} non-total posets with delta <= 1/3, {chains} total orders "
           f"(mg-8b32 b4.3's count = {boundary + chains}), delta < 1/3: {strict}")
L.verdict(tot == 0, "no poset at n <= 6 is strictly frozen",
          "exhaustive over all 134 492 labelled posets at n = 3,4,5,6")
L.note("The conjecture is verified to n = 14 (mg-33f5, cited), so this is not a gap this")
L.note("instrument could close by going one n further — the population is empty as far as")
L.note("anybody has looked, and every number below is on the CLOSED boundary delta <= 1/3.")
L.verdict(bad_l == 0, "every boundary poset has a coherent majority order L*", f"{seen} posets")
L.verdict(bad_sub == 0, "and is a subrelation of it — so relabelling L* to the identity loses "
                        "nothing", "which is what makes the n = 7 sweep exhaustive rather than "
                        "a sample")

# ------------------------------------------------------------------ c3.3

L.banner("c3.3  T3 — BOUNDARY RIGIDITY, and the table row 8 needs")
print()
print("   n | |B_n| | labelled | e(P)   | m       | max m | d_max  | eps_max | ceiling | ratio")
print("  ---+-------+----------+--------+---------+-------+--------+---------+---------+-------")
notallthird = 0
POP = {}
for n in (3, 4, 5, 6, 7):
    fam = []
    for up in L.chain_subrelations(n):
        e, pi = L.e_and_marginals(up, n)
        if any(pi[(j, i)] > third for i, j in combinations(range(n), 2)):
            continue
        pairs = L.incomparable_pairs(up, n)
        if not pairs:
            continue
        if any(pi[(j, i)] != third for i, j in pairs):
            notallthird += 1
        fam.append((up, e, len(pairs)))
    POP[n] = fam
    C = n * (n - 1) // 2
    mx = max(m for _, _, m in fam)
    es = sorted(set(e for _, e, _ in fam))
    ms = sorted(set(m for _, _, m in fam))
    d = Fraction(mx, C)
    eps = Fraction(2 * mx, n * n - 1)
    print(f"   {n} | {len(fam):5d} | {len(fam) * math.factorial(n):8d} | "
          f"{','.join(map(str, es)):6} | {','.join(map(str, ms)):7} | {mx:5d} | {str(d):>6} | "
          f"{str(eps):>7} | {str(Fraction(n, n + 1)):>7} | {str(Fraction(eps, Fraction(n, n+1))):>5}")
L.verdict(notallthird == 0, "EVERY incomparable pair of EVERY boundary poset sits at exactly 1/3",
          "n = 3..7, exhaustive; so sum of flips = m/3 and eps_spec = d * n/(n+1) EXACTLY")
L.verdict(all(len(POP[n]) * math.factorial(n) == LABELLED[n] for n in (3, 4, 5, 6)),
          "and the `labelled` column agrees with c3.1's independent full sweep",
          "|B_n| * n! against the count of every labelled poset with delta <= 1/3, n = 3..6")
L.note("`|B_n|` counts the posets with L* = the identity; `labelled` is that times n!, and at")
L.note("n = 4 it reads 48, which is mg-8b32 b4.3's `72 of 219` minus its 24 total orders.")
L.note("THE RATIO COLUMN IS d ITSELF, and it is the whole slack of the M_n ceiling at these")
L.note("points: 2/3, 1/3, 1/5, 4/15, 4/21.  eps_sup is ATTAINED here, not merely valid, so no")
L.note("fact about the image can lower eps except by bounding d.")
L.note("AND EVERY ONE OF THOSE FIVE TERMS IS F23's, ALREADY REGISTERED: mg-6ff4 has the closed")
L.note("form 4*floor(n/3)/(n(n-1)) exhaustive over isomorphism classes to n = 9.  This table is")
L.note("a third route agreeing with it, and it is reported as corroboration, not as a finding.")

# ------------------------------------------------------------------ c3.4

L.banner("c3.4  the two facts mg-8b32 left homeless, re-derived here and given a reason")
for n in (3, 4, 5, 6, 7):
    L.note(f"n = {n}: the hypothesis population with L* = identity is {len(POP[n])} posets"
           + ("   [mg-8b32 b1.3 reports 5 at n = 6]" if n == 6 else ""))
L.verdict(len(POP[6]) == 5, "n = 6: 5 posets — mg-8b32's figure, reached by a different "
                            "enumeration", "full labelled extension sweep and the chain "
                            "restriction agree")
L.verdict(all(len(POP[n]) == sum(math.comb(n - 2 * k, k) for k in range(1, n // 2 + 1)
                                 if n - 2 * k >= k) for n in (3, 4, 5, 6, 7)),
          "and |B_n| agrees with mg-6ff4's class count sum_k C(n-2k, k) at n = 3..7",
          "1, 2, 3, 5, 8 — two enumerations agreeing on the size of the population")
L.note("The sequence runs 1, 2, 3, 5, 8 at n = 3..7 — which is mg-6ff4's class count")
L.note("sum_k C(n-2k, k) at every one of those n, so the two enumerations agree on the SIZE of")
L.note("the population as well as on its extremes.  The closed form is F23's and is cited, not")
L.note("re-derived: this arm measures five terms and mg-6ff4 measured seven.")

# the marginal fiber, by rank rather than by kernel construction
firstn = None
for n in (3, 4, 5, 6, 7):
    worst = 0
    for up, e, m in POP[n]:
        S = L.linexts(up, n)
        rows = [[Fraction(1)] * len(S)]
        for x, y in combinations(range(n), 2):
            rows.append([Fraction(1) if sig.index(x) < sig.index(y) else Fraction(0) for sig in S])
        dimker = len(S) - L.rank_over_Q(rows)
        if dimker > worst:
            worst = dimker
    L.note(f"n = {n}: largest marginal-fiber dimension over the hypothesis population = {worst}")
    if worst > 0 and firstn is None:
        firstn = n
L.verdict(firstn == 6, "no hypothesis-population poset below n = 6 has a non-trivial marginal "
                       "fiber", "so a2.3-style weight witnesses cannot exist below n = 6 — its "
                       "n was forced")
L.note("AND THE REASON, which a re-measurement alone would not give: below n = 6 every poset in")
L.note("the population has e(P) = 3 with m = 2 pairs at 1/3, and the marginal map is injective")
L.note("on a 3-point support with 2 independent pair coordinates.  The first e(P) = 9 poset")
L.note("appears at n = 6, and that is where the fiber first has room.")

L.finish()
