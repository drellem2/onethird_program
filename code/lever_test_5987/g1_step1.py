#!/usr/bin/env python3
"""mg-5987 `g1` — STEP 1 OF mg-9b6b's TEST: *is the hypothesis `frozen`?*

`mg-9b6b`'s step 1 says: if the hypothesis is `frozen`, the population is empty at every reachable
`n` and no census addresses the statement — but the CONTRAPOSITIVE may be measurable, and that
reading is what steps 2 and 3 price.  Run on `(B-cov)` and `(EQ)` it returns three things, and the
second and third are not what `(R)` returned:

    (a) the population is empty, re-established here rather than quoted;
    (b) there is NO unconditional reading of either statement at any constant — `(R)` HAS one
        (F26), so the hypothesis is load-bearing for these two in a way it is not for `(R)`;
    (c) the conclusions do not merely BECOME FALSE off the class, they stop REFERRING: both name
        `e`, and `e` is fully decided exactly on the empty class.

(c) is the half `mg-9b6b` did not have to deal with, and it is why this directory has a reading
argument at all.  It is settled by measurement in both directions rather than by picking a
convention: the envelope over ALL reference orders is computed, and where `e` does exist it is
checked against the stand-in this directory uses everywhere else.
"""

import sys
from fractions import Fraction

import lib5987 as M
import lib6ff4 as L

print("=" * 96)
print("mg-5987  g1 — STEP 1: IS THE HYPOTHESIS `frozen`?   (B-cov) and (EQ), both at once")
print("=" * 96)

CL = L.all_classes(7)
THIRD = Fraction(1, 3)

print("""
§1. THE POPULATION.  Both statements quantify over the frozen class, so the first question is how
    many members of it any census here can see.  Re-established rather than quoted, because a
    directory that prints zeros over a class it did not check is printing zeros about nothing.
""")
print("    n | classes | non-chain | primitive | δ < 1/3 (frozen) | δ ≤ 1/3 (weak)")
print("   ---+---------+-----------+-----------+------------------+---------------")
for n in range(3, 8):
    nc = M.non_chains(CL, n)
    pm = M.primitives(CL, n)
    strict = weak = 0
    for d in nc:
        ok, delta, _ = L.delta_at_most(n, d, THIRD)
        if ok:
            weak += 1
            strict += (delta < THIRD)
    print(f"   {n:2d} | {len(CL[n]):7d} | {len(nc):9d} | {len(pm):9d} | {strict:16d} | {weak:14d}")
print("""
    The frozen class is EMPTY at every n ≤ 7 and the weak class has ONE member, at n = 3 — the
    boundary poset, δ = 1/3 EXACTLY.  So step 1 bites on (B-cov) and (EQ) exactly as it bites on
    (R), and for the same reason: there is no member to measure either statement at.
""")

print("""
§2. IS THERE AN UNCONDITIONAL READING?  For (R) there IS one — docs/FACTS.md F26 gives an
    unconditional density ceiling `d ≤ 1 − ⌈(n−1)/2⌉/C(n,2)`, which owes nothing to the conjecture
    and is what mg-9b6b priced as the dial's PROVABLE end.  Asked of these two, the answer is NO at
    every constant, and it is a PROOF rather than a census: the antichain refutes both at every n.
""")
print("    n  | A_n: max_x |h − rank_e|  | A_n: Σ C_x / E[inv_e] |  checked against profile()")
print("   ----+--------------------------+-----------------------+---------------------------")
for n in (3, 4, 6, 8, 10, 40, 100):
    cf = M.antichain_closed_form(n)
    if n <= 10:
        a = M.antichain(n)
        pr = M.profile(n, a)
        r = M.rank_of(M.barycentric(n, pr["h"]))
        ok = (M.bias(n, pr, r) == cf["bias"] and M.rho(n, a, pr, r) == cf["rho"])
        tag = "term for term" if ok else "MISMATCH"
    else:
        tag = "closed form only"
    print(f"   {n:3d} | {str(cf['bias']):24s} | {str(cf['rho']):21s} |  {tag}")
print("""
    Both are (n−1)/2 and (n−2)/3 — UNBOUNDED, so no constant `C` makes either statement true
    unconditionally, at any n ≥ 4.  And the witness is reading-independent, which is the only
    reason this section can come BEFORE §3 chooses a reading: `h` is constant on A_n, so every
    reference order is a permutation of the same rank vector and the bias is (n−1)/2 at all of
    them.  ⚠️  A_n is PRIMITIVE, so the restriction to primitives does not rescue either.
""")

print("""
§3. AND THE CONCLUSIONS DO NOT REFER.  STATE.md's glossary: `e` is *"the >2/3-majority order all
    biases align with — reference, not a choice"*, and its λ_std row says in as many words that
    *"frozen removes the choice ... that is a hypothesis, not a convention"*.  Both of these
    statements name `e` — (EQ) in `rank_e`, (B-cov) in `E[inv_e]` — so off the frozen class they
    do not merely become false, they stop having a subject.  Measured:
""")
print("    n  | primitives | `e` FULLY decided (every pair ≥2/3) | = δ(P) ≤ 1/3 ?")
print("   ----+------------+-------------------------------------+----------------")
for n in range(3, 8):
    pm = M.primitives(CL, n)
    dec = 0
    same = True
    for d in pm:
        pr = M.profile(n, d)
        _, full = M.majority_reference(n, d, pr)
        ok, _, _ = L.delta_at_most(n, d, THIRD)
        dec += full
        same &= (full == ok)
    print(f"   {n:2d} | {len(pm):10d} | {dec:35d} | {'yes, at every member' if same else 'NO'}")
print("""
    `e` is fully decided at 1 primitive over n ≤ 7 — the n = 3 boundary poset — and at NONE from
    n = 4 on.  The two columns agree at every member because they are the same predicate: every
    incomparable pair ≥2/3-decided IS δ(P) ≤ 1/3.  The definedness of the notation and the
    emptiness of the class are ONE fact, not two.
""")

print("""
§4. SO THE READING IS PRICED RATHER THAN PICKED.  This directory evaluates both statements at the
    BARYCENTRIC reference — sort by `h(x) = E[pos_σ x]`, always a linear extension because `x < y`
    forces `h(x) < h(y)`.  Two measurements justify it, and the first is the one that makes every
    later verdict reading-proof.
""")
print("   (a) the ENVELOPE over ALL linear extensions as reference, n ≤ 6, primitives.  Every")
print("       number is a FLOOR over the class — the smallest value the primitives take under that")
print("       reading — because the floor is what step 2 prices.  ⚠️  THE FAVOURABLE END IS NOT THE")
print("       SAME END FOR THE TWO OBJECTS, which is measured here rather than assumed: a LOWER")
print("       floor delivers FEWER orders, so `min over e` is the reading most favourable to the")
print("       lever, and the barycentric order sits at that end for (EQ) and at the OTHER end for")
print("       (B-cov) — it roughly minimises inversions, and inversions are (B-cov)'s DENOMINATOR.")
print("             (EQ): max_x |h − rank_e|                     (B-cov): Σ C_x / E[inv_e]")
print("        min over e | max over e | bary at min |  min over e | max over e | bary at max")
print("       ------------+------------+-------------+-------------+------------+------------")
for n in range(3, 7):
    pm = M.primitives(CL, n)
    bl = bh = rl = rh = None
    bat = rat = 0
    for d in pm:
        pr = M.profile(n, d)
        rb = M.rank_of(M.barycentric(n, pr["h"]))
        lo, is_bary, hi = M.envelope(n, d, pr, lambda r: M.bias(n, pr, r))
        bat += is_bary
        bl = lo if bl is None or lo < bl else bl
        bh = hi if bh is None or hi < bh else bh
        lo, _, hi = M.envelope(n, d, pr, lambda r: M.rho(n, d, pr, r))
        rat += (M.rho(n, d, pr, rb) == hi)
        rl = lo if rl is None or lo < rl else rl
        rh = hi if rh is None or hi < rh else rh
    print(f"   n={n}   {str(bl):9s} | {str(bh):10s} | {bat:4d}/{len(pm):<6d} |  {str(rl):10s} |"
          f" {str(rh):10s} | {rat:4d}/{len(pm)}")
print("""
       So the barycentric reading is the MOST favourable one for (EQ) — it is the argmin at every
       primitive in the population, so (EQ)'s price under it is a lower bound on its price under
       every reading — and the LEAST favourable one for (B-cov), where it sits at the max over `e`
       at every primitive.  Each verdict below is therefore stated at the end that cannot flatter
       it.  What no reading changes is the shape: BOTH columns are bounded at every `n` here, so
       *"the floor does not run away"* is a fact about the objects and not about the choice — and
       that is the only property step 2 consumes.
""")
print("   (b) where STATE.md's own `e` EXISTS, it IS the barycentric order — the wrong-direction")
print("       control, taken on the relaxed class β = 2/5 where the population is NOT empty:")
tot_hits = tot_agree = 0
for beta in (Fraction(1, 3), Fraction(2, 5)):
    hits = agree = 0
    for n in range(3, 8):
        for d in M.primitives(CL, n):
            pr = M.profile(n, d)
            e, full = M.majority_reference(n, d, pr, beta)
            if full:
                hits += 1
                agree += (e is not None and e == M.barycentric(n, pr["h"]))
    print(f"       β = {str(beta):3s}: fully decided at {hits:3d} primitives (n ≤ 7),"
          f" majority == barycentric at {agree} of {hits}")
    tot_hits += hits
    tot_agree += agree
print(f"       TOTAL {tot_agree} of {tot_hits}.  The stand-in is not a convention chosen to be")
print( "       convenient; it is the same order wherever the real one is defined at all.")

print("""
§5. VERDICT ON STEP 1 — IT BITES ON BOTH, AND HARDER THAN ON (R).

    (R)  hypothesis frozen ⟹ population empty ......................... yes
         an unconditional reading exists (F26) ........................ YES
         the conclusion `d ≤ D` refers off the class .................. yes, `d` needs no reference

    (EQ) and (B-cov)
         hypothesis frozen ⟹ population empty ......................... yes, re-established §1
         an unconditional reading exists .............................. NO, at any constant (§2)
         the conclusion refers off the class .......................... NO — `e` is decided only
                                                                        where the class is (§3)

    So neither escapes at step 1.  What is measurable is the contrapositive, exactly as mg-9b6b
    said — and pricing it is step 2, which is `g2`.
""")
sys.exit(0)
