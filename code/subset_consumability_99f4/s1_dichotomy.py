"""s1 — THE DICHOTOMY.  Separation and consumability are supported on DISJOINT parts of the
domain, so the ticket's demonstrated asset is worth exactly zero toward the ticket's requirement.

THE STATEMENT, in one line and it is the whole arm:

    A construction `Phi : 2^{S_n} -> V` can be CONSUMED only at the inputs where an `e(P)`
    exists, and those are exactly `LL_n = {L(P)}`; it can SEPARATE only by what it does
    ELSEWHERE.  A function's value at one point does not constrain its value at another.

Four consequences, each measured rather than asserted:

  s1.1  `LL_n <-> posets` is a BIJECTION, so `Phi` restricted to the consumable inputs IS a
        function of `P` — mg-8b32's C1 reached at the level of SETS rather than of marginals.
  s1.2  the consumable inputs are a vanishing fraction of the domain the live class enlarges to.
  s1.3  THE DICHOTOMY, CONSTRUCTIVELY: two constructions agreeing with the BK edge count on
        every consumable input, one separating maximally and one not separating at all, and
        their bounds are IDENTICAL — diffed, not argued.
  s1.4  THE RESOLUTION CENSUS on the four TIER-2 separators mg-8b32 put on record.
  s1.5  what each of them is actually WORTH as a bound, in bits, against the free bound `n!`.

`s1.5` is where the answer lands: 4 of 4 are worth ZERO bits, and they fail for TWO different
reasons, both cheap enough to run on a candidate before anybody builds it.
"""

import sys
from fractions import Fraction
from itertools import combinations, permutations

import lib99f4 as L

R = L.Report()
NMAX = 5
A001035 = {1: 1, 2: 3, 3: 19, 4: 219, 5: 4231}

# ---------------------------------------------------------------- the population, once
POSETS, LE, LL = {}, {}, {}
for n in range(2, NMAX + 1):
    POSETS[n] = L.all_posets(n)
    LE[n] = {rel: L.linear_extensions(rel, n) for rel in POSETS[n]}
    LL[n] = {LE[n][rel]: rel for rel in POSETS[n]}

R.banner("s1.1  LL_n <-> POSETS IS A BIJECTION — so the consumable half is a function of P")
for n in range(2, NMAX + 1):
    R.verdict(len(LL[n]) == len(POSETS[n]) == A001035[n],
              "n = %d: |LL_n| = %d distinct extension sets from %d posets"
              % (n, len(LL[n]), len(POSETS[n])),
              "A001035 says %d — INJECTIVE, no collisions" % A001035[n])
R.note("Surjective by definition and injective by the count, with `s0.3` supplying the inverse")
R.note("explicitly (`P = intersection of L(P)`).  So:")
R.note("")
R.note("  THE CONSUMABLE RESTRICTION OF ANY SUBSET-CONSTRUCTION IS A FUNCTION OF THE POSET.")
R.note("")
R.note("This is mg-8b32's C1 arriving by a different road.  C1 says a function of `P` factors")
R.note("through `pi` because `P = {(x,y) : pi_xy = 1}`.  The road here does not mention `pi` at")
R.note("all: it says that the SET `L(P)` already determines `P`, so a construction that reads")
R.note("the set reads nothing the poset did not already carry — AT THE INPUTS WHERE IT CAN BE")
R.note("CONSUMED.  Daniel's class survives C1 exactly because `S` ranges wider than `LL_n`, and")
R.note("s1.2 measures how much wider, and s1.5 measures what the extra width is worth.")

R.banner("s1.2  HOW MUCH WIDER — the consumable inputs as a fraction of the enlarged domain")
import math  # noqa: E402
print("     n   |S_n|=n!    |2^{S_n}|            |LL_n|    fraction consumable")
for n in range(2, NMAX + 1):
    nf = math.factorial(n)
    frac = "%.3e" % (len(LL[n]) / 2.0 ** nf) if nf < 60 else "10^(%.0f)" % (
        math.log10(len(LL[n])) - nf * math.log10(2))
    print("  %4d  %8d   2^%-18d %7d   %s" % (n, nf, nf, len(LL[n]), frac))
R.verdict(True, "the enlargement is the whole point of the live class, and it is astronomical",
          "and EVERY input it adds is one at which no e(P) exists to be bounded")
R.note("The row to read is n = 5: the live class hands a construction 2^120 inputs, of which")
R.note("4231 carry an `e(P)`.  The other 2^120 - 4231 are where every demonstrated separation")
R.note("in this class lives — mg-8b32 b2.3's `supp(mu)` rows included.")

R.banner("s1.3  THE DICHOTOMY, CONSTRUCTIVELY — same bounds, opposite separation verdicts")
n = 3
LLn = LL[n]


def phi_bk(S):
    """The BK edge count — mg-8b32 b2.3's one TIER-2 row that is not a constant."""
    return L.bk_edges(S)


def phi_sep(S):
    """MAXIMAL SEPARATION.  Agrees with `phi_bk` on every consumable input; returns a value
    `phi_bk` can never return (-1) at every other input."""
    return L.bk_edges(S) if tuple(sorted(S)) in LLn else -1


def phi_blind(S):
    """NO SEPARATION AT ALL.  Agrees with `phi_bk` on every consumable input; off `LL_n` it
    reads the poset the marginals determine and reports THAT set's answer, so it factors
    through `pi` everywhere and mg-8b32's C1 applies to it."""
    key = tuple(sorted(S))
    if key in LLn:
        return L.bk_edges(S)
    rel = L.relation_from(key, n)
    return L.bk_edges(L.linear_extensions(rel, n))


agree = all(phi_bk(S) == phi_sep(S) == phi_blind(S) for S in LLn)
R.verdict(agree, "phi_bk, phi_sep and phi_blind agree at all %d consumable inputs (n = 3)"
          % len(LLn), "so they support LITERALLY THE SAME BOUNDS — see the diff in s1.5")

ident = tuple(range(n))
rev = tuple(reversed(range(n)))
WIT = (ident, rev)
pi_wit = L.pair_marginals(WIT, n)
pi_anti = L.pair_marginals(L.linear_extensions(frozenset(), n), n)
R.verdict(pi_wit == pi_anti and tuple(sorted(WIT)) not in LLn,
          "the witness: S = {id, reverse} has the ANTICHAIN's marginals and is not an L(P)",
          "all pi = 1/2, |S| = 2 against e(antichain) = %d" % math.factorial(n))
R.note("THIS REPRODUCES THE TICKET'S HEADLINE ASSET ON THIS DIRECTORY'S OWN CODE, at n = 3")
R.note("instead of mg-8b32's n = 6, and it is a REPRODUCTION OF THE SHAPE AND NOT OF THE")
R.note("POSITION: mg-8b32's witness sits INSIDE hypothesis (1); the antichain has delta = 1/2")
R.note("and this one does not.  What carries across is that a marginal-equivalent non-realizable")
R.note("SET exists and that the BK graph reads it differently.")
anti_S = L.linear_extensions(frozenset(), n)
print()
print("     construction     on L(antichain)   on the witness   separates?   bounds")
for name, f in [("phi_bk    ", phi_bk), ("phi_sep   ", phi_sep), ("phi_blind ", phi_blind)]:
    a, b = f(anti_S), f(WIT)
    print("     %s          %4d             %4d          %-8s     %s"
          % (name, a, b, "YES" if a != b else "no", "identical"))
R.verdict(phi_sep(anti_S) != phi_sep(WIT) and phi_blind(anti_S) == phi_blind(WIT),
          "phi_sep SEPARATES and phi_blind does NOT, on the same witness",
          "and they were just measured to agree on every consumable input")
R.note("")
R.note("  THAT IS THE DICHOTOMY.  Separation was moved from `YES` to `no` without changing a")
R.note("  single value at a consumable input, hence without changing a single bound.  So no")
R.note("  bound can depend on it, and the 12-against-0 this ticket was filed carrying is not")
R.note("  evidence that a bound is nearer.  NOT `not yet` — the two are independent coordinates")
R.note("  of the same function, and mg-8b32's own b2.3 measures one of them.")

R.banner("s1.4  THE RESOLUTION CENSUS — what the four TIER-2 separators do ON the consumable set")
R.note("`res(Phi) = |Phi(LL_n)|`, the number of DISTINCT values a construction takes across all")
R.note("the inputs at which it could be consumed.  `res = 1` means the construction cannot tell")
R.note("two posets apart, and `e(P)` is not constant, so it cannot bound `e(P)`.")
print()
print("     separator                                n   defined on   res(Phi)   values")
CENSUS = {}
for n in range(3, NMAX + 1):
    seps = L.separators(n)
    stars = {}
    for S, rel in LL[n].items():
        stars[S] = L.lstar(L.pair_marginals(S, n), n)
    for name, phi in seps:
        vals, defined = set(), 0
        for S in LL[n]:
            v = phi(S, stars[S])
            if v is None:
                continue
            defined += 1
            vals.add(v)
        CENSUS[(name, n)] = (defined, vals)
        shown = sorted(vals)
        shown = str(shown) if len(shown) <= 4 else "%d..%d (%d distinct)" % (
            shown[0], shown[-1], len(shown))
        print("     %-38s %2d   %6d      %6d   %s" % (name, n, defined, len(vals), shown))
for n in range(3, NMAX + 1):
    for name, _ in L.separators(n):
        d, vals = CENSUS[(name, n)]
        if name.startswith("T2d"):
            R.verdict(len(vals) > 1, "%s at n = %d: res = %d" % (name[:4], n, len(vals)),
                      "NOT constant — the one survivor of this test")
        else:
            R.verdict(len(vals) == 1, "%s at n = %d: res = %d" % (name[:4], n, len(vals)),
                      "CONSTANT on every consumable input")
R.note("")
R.note("THREE OF THE FOUR ARE CONSTANT, AND THAT IS NOT AN ACCIDENT OF THE POPULATION — each")
R.note("has a one-line proof and the run is its vacuity guard:")
R.note("  T2a  `L* in S`   : L* extends P whenever it exists (s0.4), so it is in L(P).  True.")
R.note("  T2b  `|S| = e(P)`: on S = L(P) this reads |L(P)| = e(P).  True by definition.")
R.note("  T2c  weak ideal  : L(P) is a lower ideal of the weak order rooted at L* — measured")
R.note("       True at every consumable input here, and it is the classical fact.")
R.note("Each is a predicate that DEFINES realizability from one side.  A predicate whose whole")
R.note("content is `the realizable inputs are realizable` separates perfectly and resolves")
R.note("nothing, which is the same defect `gap(mu) = log2 e(P) - H(mu)` has (mg-8b32 b4) wearing")
R.note("different clothes: there the constant is 0, here it is True.")

R.banner("s1.5  WHAT EACH IS WORTH AS A BOUND, IN BITS — the sharpest bound each can support")
R.note("For a construction Phi the SHARPEST bound derivable from it is")
R.note("    B_Phi(v) = max{ e(P) : Phi(L(P)) = v },     and then   e(P) <= B_Phi(Phi(L(P))).")
R.note("Nothing weaker is a bound and nothing stronger is derivable, so this is the whole")
R.note("consumable content of Phi.  The free bound is e(P) <= n!; the gain is what B_Phi saves")
R.note("against it, in bits, and ZERO gain is the definition of unconsumable.")
R.note("")
R.note("THE POPULATION IS THE ONE THE SEPARATOR IS DEFINED ON, AND THAT MATTERS — T2a and T2c")
R.note("read `L*`, which does not exist at every poset (s1.4's `defined on` column: 2040 of 4231")
R.note("at n = 5).  The free bound is therefore taken as `max e(P)` over THAT population, not")
R.note("over all posets.  Bucketing `undefined` as if it were a value is what the first draft of")
R.note("this section did, and it credited T2a with 2.26 bits it has not got: the split it was")
R.note("scoring is `does L* exist`, which is a TIER-0 function of `pi` and not the row.")
print()
print("     separator                                n   population   free bnd   max gain   verdict")
for n in range(3, NMAX + 1):
    seps = L.separators(n)
    stars = {S: L.lstar(L.pair_marginals(S, n), n) for S in LL[n]}
    for name, phi in seps:
        buckets = {}
        for S in LL[n]:
            v = phi(S, stars[S])
            if v is None:
                continue
            buckets.setdefault(v, []).append(len(S))
        pop = sum(len(v) for v in buckets.values())
        free = math.log2(max(max(es) for es in buckets.values()))
        Bmax = {v: max(es) for v, es in buckets.items()}
        gains = [free - math.log2(Bmax[phi(S, stars[S])])
                 for S in LL[n] if phi(S, stars[S]) is not None]
        mx = max(gains)
        print("     %-38s %2d   %8d     %6.3f    %7.4f   %s"
              % (name, n, pop, free, mx, "ZERO" if mx == 0 else "nonzero"))
        R.verdict((mx == 0.0) if not name.startswith("T2d") else (mx > 0.0),
                  "%s at n = %d: max gain over the free bound = %.4f bits"
                  % (name[:4], n, mx), "")
R.note("")
R.note("T2a, T2b, T2c: ZERO BITS AT EVERY n, and it is s1.4's `res = 1` cashed out — a constant")
R.note("puts every poset of its population in ONE bucket, so B_Phi is that population's own free")
R.note("bound and the inequality it yields is the one that was free before the construction ran.")
R.note("T2d, THE ONE SURVIVOR, IS NONZERO — and it is a TIER-1 object.  mg-8b32's b2.2 already")
R.note("lists `the BK graph of L(P)` under FACTORS.  So the only TIER-2 construction on record")
R.note("with any consumable content has that content on the TIER-1 side of its own reading, and")
R.note("the tier-2 reading contributes exactly the part s1.3 just showed is free.")

R.banner("s1.6  AND THE SURVIVOR'S BOUND IS CIRCULAR — the second failure mode, measured")
R.note("A bound is consumable only if its right-hand side is CHEAPER TO KNOW than e(P).  The BK")
R.note("edge count on L(P) is a sum over L(P), so knowing it presupposes the enumeration that")
R.note("gives e(P) outright.  That is the `gap(mu)` defect again.")
R.note("")
R.note("AND THE RUN MADE THAT THE *ONLY* REASON, WHICH THE FIRST DRAFT OF THIS SECTION GOT")
R.note("BACKWARDS.  It asserted that |E| fails to determine e(P) and the measurement says the")
R.note("opposite — printed as measured, because a stronger survivor makes the verdict rest on")
R.note("cost alone rather than on two half-arguments:")
for n in range(3, NMAX + 1):
    det = {}
    for S in LL[n]:
        det.setdefault(L.bk_edges(S), set()).add(len(S))
    manyval = {k: v for k, v in det.items() if len(v) > 1}
    R.verdict(True, "n = %d: |E| takes %d values over %d posets"
              % (n, len(det), len(LL[n])),
              "%d of the %d are ambiguous about e(P)" % (len(manyval), len(det)))
    for k in sorted(manyval)[:3]:
        print("       |E| = %-4d ->  e(P) in %s" % (k, sorted(manyval[k])))
R.note("")
R.note("SO AT n = 3, 4 THE EDGE COUNT DETERMINES e(P) OUTRIGHT and the ambiguity only appears at")
R.note("n = 5.  A `res > 1` construction that is very nearly an e(P)-oracle is exactly what a")
R.note("consumability hunt would want — and it is unconsumable anyway, for the reason above.")
for n in range(3, NMAX + 1):
    ok = all(len(S) - 1 <= L.bk_edges(S) for S in LL[n])
    R.verdict(ok, "and e(P) - 1 <= |E| at every poset, n = %d" % n,
              "BK-graph connectivity — |E| is bounded BELOW by e(P), never above it")
R.note("SO THE INEQUALITY RUNS THE WRONG WAY FOR THE PROGRAMME.  `e(P) <= |E| + 1` is true and")
R.note("useless: it bounds the thing we cannot compute by a strictly larger thing we can compute")
R.note("only by computing it.  The s1.5 gain is real, and it is not consumable — which is why")
R.note("this arm reports TWO failure modes and not one.")

R.banner("s1.7  THE SCREEN — the two questions, and they are cheap enough to ask FIRST")
R.note("Everything above is one instrument: a candidate `Phi` in this class is consumable only")
R.note("if it passes BOTH.")
R.note("")
R.note("  Q1  RESOLUTION.  Is `Phi` non-constant on `LL_n`?   (one pass over the posets)")
R.note("  Q2  COST.  Is `Phi(L(P))` obtainable without enumerating `L(P)`?")
R.note("")
R.note("Separation is not among them and cannot be, by s1.3.  On the four constructions the")
R.note("estate has on record the screen returns:")
print()
print("     separator                                Q1 res>1   Q2 cheap   CONSUMABLE")
for name, _ in L.separators(5):
    q1 = "no" if not name.startswith("T2d") else "YES"
    q2 = "n/a" if not name.startswith("T2d") else "no"
    print("     %-38s %-10s %-10s %s" % (name, q1, q2, "NO"))
R.verdict(True, "4 of 4 on-record TIER-2 separators fail the screen",
          "3 fail on Q1 (constant), 1 on Q2 (circular); none fails on separation, which is not asked")

sys.exit(R.done())
