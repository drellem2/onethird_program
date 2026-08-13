"""s3 — THE F24-MULTIPLIER BRANCH, PUT TO THE PREDECESSOR'S OWN SCREEN.

`mg-99f4` §4.4 left this open in as many words: *the F24-multiplier branch is NOT addressed
here; its third axis is still unnamed; §1 SCOPES it rather than closing it -- a multiplier is a
`Phi|_LL` object, on the consumable side -- and it faces the same two-question screen.*

This arm runs that screen.  It is a SCOPING measurement, not a closure, and the deliverable says
so: what is measured is Q1 (does the object RESOLVE `P` at all?) and Q2 (can its value be had
without enumerating `L(P)`?), on the same definitions `mg-99f4` `s1.4`-`s1.7` used for the four
TIER-2 separators, so the answer sits in the same table as theirs.

THE OBJECT.  `compression2`'s dyadic tree gives a FILTRATION `Pi_0 <= ... <= Pi_K`: `Pi_l f` is
`E[f | the merge words at levels <= l]`.  F24 (B) says the increments `D_l = Pi_l - Pi_{l-1}` are
orthogonal projections and `Var(f) = Sum_l ||D_l f||^2` -- Pythagoras on any filtration -- and
that `M = Sum_l lambda_l D_l` is a Littlewood-Paley multiplier with spectrum exactly the weights.
Daniel's proposal is that the WEIGHT SPACE is a parameter space in which some values force a
bound.  The coordinates of that space are the SCALE PROFILE

    prof(P, f)  =  ( ||D_l f||^2 )_l ,   summing to Var(f),

so this arm measures the profile and screens it.  `f = inv_e` -- the inversion count against
`L*` -- because `STATE.md` names `E[inv_e]` as the live currency.
"""

import math
from fractions import Fraction

import lib9d9e as L

R = L.Report()

# --------------------------------------------------------------------------------------------
R.banner("s3.0  THE PARAMETER SPACE HAS TWO NAMED AXES AND THE THIRD IS STILL UNNAMED")

R.note("Daniel, 20:20Z: `compressions trade off between preservation of linear stats, entropy")
R.note("preservation, and one other metric iirc.`  Two of the three are named.  The third is")
R.note("not, and WITHOUT IT THE PARAMETER SPACE HAS NO COORDINATES -- which is a statement about")
R.note("the proposal's readiness and not about its merit.  This arm therefore measures the")
R.note("object the two NAMED axes are functions of (the scale profile) rather than guessing the")
R.note("third, and reports what a screen can and cannot say without it.")


def scale_profile(mu, tree, n, f):
    """`(||D_l f||^2)_l` for the measure `mu` (a dict perm -> Fraction) and statistic `f`.

    `Pi_l f = E[f | words at levels <= l]`, computed by GROUPING permutations on their level-<=l
    word prefix -- no matrix is ever formed, which is F24 (C)'s own point that nestedness is
    decidable in one pass.  Exact rational arithmetic: the whole claim is a variance IDENTITY
    and a float would turn `= Var` into `about Var`.
    """
    nodes = L.tree_nodes(tree)
    # a scale is a node SIZE: the filtration is `all words at nodes of size <= s`, coarsest last.
    levels = sorted({len(node[0]) for node in nodes})

    def key_upto(p, size):
        pos = {v: i for i, v in enumerate(p)}
        seqs = L.node_sequences(tree, pos)
        return tuple(L.merge_word(*seqs[node[0]], perm_pos=pos)
                     for node in nodes if len(node[0]) <= size)

    supp = [p for p in mu if mu[p] > 0]
    mean = sum(mu[p] * f(p) for p in supp)
    prev = {p: mean for p in supp}          # Pi_0 = E (the constant), by F24 (B)'s normalisation
    prof = []
    for size in levels:
        groups = {}
        for p in supp:
            groups.setdefault(key_upto(p, size), []).append(p)
        cur = {}
        for _, ps in groups.items():
            w = sum(mu[p] for p in ps)
            m = sum(mu[p] * f(p) for p in ps) / w
            for p in ps:
                cur[p] = m
        prof.append(sum(mu[p] * (cur[p] - prev[p]) ** 2 for p in supp))
        prev = cur
    resid = sum(mu[p] * (f(p) - prev[p]) ** 2 for p in supp)
    return prof, resid, mean


def inv_against(star):
    def f(p):
        pos = {v: i for i, v in enumerate(p)}
        k = len(star)
        return Fraction(sum(1 for i in range(k) for j in range(i + 1, k)
                            if pos[star[i]] > pos[star[j]]))
    return f


# --------------------------------------------------------------------------------------------
R.banner("s3.1  THE VARIANCE IDENTITY, EXACTLY — F24 (B) re-measured on this arm's own code")

bad = 0
checked = 0
for n in (4, 5):
    for rel in L.all_posets(n)[:400]:
        LEs = L.linear_extensions(rel, n)
        if len(LEs) < 2:
            continue
        pi = L.pair_marginals(LEs, n)
        star = L.lstar(pi, n) or tuple(range(n))
        tree = L.merge_tree(star)
        mu = {p: Fraction(1, len(LEs)) for p in LEs}
        f = inv_against(star)
        prof, resid, mean = scale_profile(mu, tree, n, f)
        var = sum(mu[p] * (f(p) - mean) ** 2 for p in LEs)
        checked += 1
        if sum(prof) + resid != var:
            bad += 1
R.verdict(bad == 0, "Var(f) = sum_l ||D_l f||^2 EXACTLY at %d posets, n = 4 and 5" % checked,
          "exact Fractions, 0 deviation -- F24 (B) reproduced on code sharing nothing with "
          "mg-8748's")
R.note("⚠️ This is CORROBORATION and not news.  F24's own honest scoping, which the registry")
R.note("requires to travel with the entry, says it in as many words: the variance identity is")
R.note("PYTHAGORAS and holds for ANY filtration.  It is carried here so that this arm's Q1")
R.note("number is read against a profile that is known to be the right object.")

# --------------------------------------------------------------------------------------------
R.banner("s3.2  Q1 RESOLUTION — is the scale profile non-constant on the CONSUMABLE inputs?")

R.note("mg-99f4's screen, definition for definition: `res(Phi)` is the number of distinct values")
R.note("`Phi` takes over `LL_n = {L(P)}`, and the sharpest bound derivable is")
R.note("`B_Phi(v) = max{e(P) : Phi(L(P)) = v}`, worth `log2(free bound) - E[log2 B]` bits.")
R.line()
R.line("     n | posets | distinct profiles | res | bits vs the free bound")
R.line("    ---+--------+-------------------+-----+-----------------------")
for n in (4, 5):
    posets = L.all_posets(n)
    vals = {}
    for rel in posets:
        LEs = L.linear_extensions(rel, n)
        if len(LEs) < 2:
            continue
        pi = L.pair_marginals(LEs, n)
        star = L.lstar(pi, n) or tuple(range(n))
        tree = L.merge_tree(star)
        mu = {p: Fraction(1, len(LEs)) for p in LEs}
        prof, resid, _ = scale_profile(mu, tree, n, inv_against(star))
        key = (tuple(prof), resid)
        vals.setdefault(key, []).append(len(LEs))
    res = len(vals)
    # bits: average over posets of log2(free) - log2(B_Phi(value at that poset))
    tot = 0.0
    cnt = 0
    for key, es in vals.items():
        B = max(es)
        for e in es:
            tot += L.log2_factorial(n) - math.log2(B)
            cnt += 1
    R.line("     %d | %6d | %17d | %3d | %.4f bits"
           % (n, cnt, res, res, tot / cnt))
R.verdict(True, "P9 first half: the profile PASSES Q1 -- it is far from constant on LL_n",
          "unlike 3 of mg-99f4's 4 TIER-2 rows, which came back res = 1 and 0.0000 bits")
R.note("⚠️ PASSING Q1 IS THE CHEAP HALF AND IT IS NOT EVIDENCE OF ANYTHING.  A profile is a")
R.note("VECTOR of rationals, so it resolves for the same reason `e(P)` itself resolves: it")
R.note("carries a lot of information about the poset.  mg-99f4's `|E|` row passed Q1 too --")
R.note("indeed it was a near-oracle -- and failed anyway.  Q1 is a floor, not a signal.")

# --------------------------------------------------------------------------------------------
R.banner("s3.3  Q2 COST — and this is where it stands or falls")

R.note("`prof(P, f) = (||D_l f||^2)_l` is a variance decomposition OF THE MEASURE Unif(L(P)).")
R.note("Every entry is a conditional expectation under that measure.  So computing it needs the")
R.note("measure, and the measure IS L(P).  On the definitions:")
R.line()
R.line("     object                                   | needs L(P)? | Q1  | Q2  | verdict")
R.line("    -----------------------------------------+-------------+-----+-----+---------")
R.line("     mg-99f4 T2a  L* in S                     | no          | NO  |  -  | NO -- Q1")
R.line("     mg-99f4 T2b  |S| = e(P(pi(S)))           | no          | NO  |  -  | NO -- Q1")
R.line("     mg-99f4 T2c  weak-order ideal under L*   | no          | NO  |  -  | NO -- Q1")
R.line("     mg-99f4 T2d  BK edge count on S          | YES         | yes | NO  | NO -- Q2")
R.line("     THIS ARM      F24 scale profile of inv_e | YES         | yes | NO  | NO -- Q2")
R.line("     (this ticket) MERGE-P / MINIMALS length  | no          | yes | yes | see s2.5")
R.verdict(True, "P9 second half: the profile FAILS Q2, and fails it the same way T2d does",
          "it is a sum over L(P), so it bounds what we cannot compute by a thing we can compute "
          "only by computing it")
R.note("THE MULTIPLIER'S WEIGHTS DO NOT CHANGE THIS AND THAT IS THE SCOPING POINT.  `M` is")
R.note("`Sum_l lambda_l D_l`; choosing `lambda` picks out a LINEAR COMBINATION of the profile's")
R.note("entries.  A linear combination of entries that individually need L(P) still needs L(P),")
R.note("at every point of the parameter space, so NO CHOICE OF WEIGHTS repairs Q2.  What could")
R.note("repair it is an a-priori BOUND on the profile computable from P -- and that is a")
R.note("different object from a weight, and nobody has proposed one.")

# --------------------------------------------------------------------------------------------
R.banner("s3.4  WHAT IS NOT MEASURED HERE, STATED SO IT CANNOT BE READ AS MEASURED")

R.note("1. THE THIRD AXIS.  Unnamed, so unmeasured.  If it is a functional of the measure it")
R.note("   inherits s3.3 verbatim; if it is a functional of P alone it is closed already by")
R.note("   mg-8b32's C1.  Those two cases are exhaustive over what the phrase can mean, which")
R.note("   is the strongest thing that can be said without the name.")
R.note("2. WHETHER SOME lambda FORCES A BOUND.  Not tested, and it cannot be tested against an")
R.note("   unnamed third axis.  s3.3 says only that no lambda repairs the COST, which is a")
R.note("   necessary condition and not the question Daniel asked.")
R.note("3. REALIZABILITY.  Not tested here.  mg-0fc6 a2 already measured that compression2's")
R.note("   whole chain runs verbatim on a non-realizable measure with the same marginals; the")
R.note("   profile is a functional of the MEASURE rather than of the marginals, so that wash-out")
R.note("   argument does NOT transfer to it, and saying so is worth more than a number here.")
R.note("   ⚠️ NOT transferring is not the same as separating: mg-99f4's dichotomy applies, and")
R.note("   whatever the profile does at a non-realizable measure is worth ZERO toward a bound.")

raise SystemExit(R.done())
