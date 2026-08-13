#!/usr/bin/env python3
"""mg-9b6b arm e1 — EVERY READING OF mg-0b96 §6's ESCAPE HATCH LANDS ON THE DIAL, AND ONE OF THEM
IS REFUTED OUTRIGHT BY A CLASS THAT IS ALREADY ON THE RECORD.

`mg-0b96` closed the density lever and then named, in as many words, the one thing that would
change its verdict (§6, last paragraph):

    "A result of the form `δ(P) ≥ f(d)` with `f` increasing and `f(2×10⁻²) ≥ 1/3` — a
     DENSITY-TO-BALANCE bound rather than a structure-to-balance one. ...
     IT IS NOT RULED OUT HERE."

Call that `S_f`.  This arm asks what `S_f` IS, and the answer has three branches, none of which is
open:

  m2  `S_f` ⟹ `(2_D)` ⟹ `(1_D)` at `D = D_needed`, and back through the STEP `f = (1/3)·1[d ≥ D]`.
      So on the flat reading, `S_f` is the statement `mg-0b96` §2 closed — the escape hatch is the
      closed door in unconditional clothing.  The `>`/`≥` gap is exactly one density quantum and is
      MEASURED rather than waved at.
  m3  On the STRICTLY increasing reading — and on any reading with `f(D) > 1/3` — `S_f` is not open
      either: it is FALSE at 63 orders — every `n` from 3 to 66 except 65, computed rather than
      asserted as a range — refuted by an EXPLICIT ordinal-sum family with `δ = 1/3` exactly and
      `d` above `D_needed`.  So `f` is PINNED FLAT at `1/3` across the whole range where the
      boundary class lives, which leaves the step and nothing else.
  m4  THE PRIMITIVITY OBJECTION IS REAL AND IS CONCEDED HERE RATHER THAN ANSWERED.  A minimal
      counterexample is primitive, so a PRIMITIVE-restricted `S_f` would serve row 8 just as well —
      and m3's refuters are ordinal sums.  Measured: over every isomorphism class at `n ≤ 8` there
      is exactly ONE primitive member of the boundary class, at `n = 3`.  The strict reading
      therefore survives the primitive restriction above `n = 3`, and what kills it there is not
      m3 but m2, which is indifferent to the restriction.

WHAT A RUN CAN AND CANNOT DO HERE.  m2 is contraposition and a tautology's warrant cannot be
improved by a sweep; the sweep catches an IMPLEMENTATION in which `frozen` and `δ ≥ 1/3` are not
complements, which is what every number in this directory rests on.  m3 is not a tautology: it is a
refutation, and one witness settles it at universal strength (`STATE.md`'s `FP✗`).
"""

import sys
from fractions import Fraction

import lib9b6b as Y
import lib6ff4 as L


def rule(t):
    print("-" * 100)
    print(t)


def head(t):
    print("=" * 100)
    print(t)
    print("=" * 100)


FAIL = []


def check(tag, ok, detail=""):
    print("    %-7s %-7s %s" % (tag, "ok" if ok else "FAILED", detail))
    if not ok:
        FAIL.append(tag)


def boundary_family(n):
    """`⌊n/3⌋` copies of the poset `{a < b, c}` in ORDINAL SUM, padded with a chain.

    `δ = 1/3` EXACTLY at every `n ≥ 3` and `d = 4⌊n/3⌋/(n(n−1))`, which is F23's maximum.  The
    `δ` claim is a LEMMA and not a census: in an ordinal sum every element of one summand is below
    every element of the next, so `L(P) = L(P₁) × L(P₂) × …`, incomparable pairs never straddle a
    summand, and each pair's bias is computed inside its own summand.  Hence
    `δ(P₁ ⊕ P₂) = max(δ(P₁), δ(P₂))`; a chain summand contributes no pair and `{a<b, c}` contributes
    exactly `1/3` on both of its pairs.  `m1` checks the construction against `delta_exact` anyway,
    because a lemma about the code is not the same as a lemma about posets."""
    down = []
    k = n // 3
    for blk in range(k):
        base = (1 << (3 * blk)) - 1                       # everything in earlier blocks
        down.append(base)                                 # a
        down.append(base | (1 << (3 * blk)))              # b, above a
        down.append(base)                                 # c, incomparable with a and b
    for i in range(3 * k, n):                             # chain padding
        down.append((1 << i) - 1)
    return tuple(down)


def main():
    head("mg-9b6b  e1  every reading of mg-0b96 §6's escape hatch lands on the dial")
    tab = Y.table(8)
    rows = Y.frontier(tab)

    # ------------------------------------------------------------------ m1
    rule("m1  THE EXPLICIT FAMILY, AND ITS `δ` COMPUTED RATHER THAN ARGUED")
    print("    `boundary_family(n)` is floor(n/3) copies of {a<b, c} in ordinal sum plus a chain.")
    print("    The ordinal-sum lemma gives delta = 1/3 at every n; here it is CHECKED against the")
    print("    same delta_exact every other number in this directory uses, and its density is")
    print("    checked against F23's closed form 4*floor(n/3)/(n(n-1)).")
    print()
    print("      %3s  %-10s %-10s %-12s %s" % ("n", "delta", "d", "F23 form", "primitive?"))
    okd = okf = 0
    for n in range(3, 10):
        fam = boundary_family(n)
        dl = Y.delta_exact(n, fam)
        d = Y.density(n, fam)
        f23 = Y.d_boundary(n)
        okd += (dl == Y.THIRD)
        okf += (d == f23)
        print("      %3d  %-10s %-10s %-12s %s"
              % (n, dl, d, f23, "yes" if L.is_primitive(n, fam) else "no -- an ordinal sum"))
    check("m1.a", okd == 7, "delta = 1/3 EXACTLY at every n = 3..9")
    check("m1.b", okf == 7, "and its density is F23's maximum at every n = 3..9")

    # ------------------------------------------------------------------ m2
    rule("m2  THE FLAT READING: `S_f` = `(2_D)` = `(1_D)`, INSTANTIATED")
    print("    The three predicates are computed through DIFFERENT comparisons -- (1_D) tests")
    print("    `delta < beta` then `d > D`, (2_D) tests `d > D` then `delta < beta`, S_f tests")
    print("    `d >= D` then `delta < beta` over the WHOLE population with no hypothesis filter.")
    print("    A tautology cannot be strengthened by a run; what a run catches is these three")
    print("    disagreeing, which would mean `frozen` and `delta >= 1/3` are not complements as")
    print("    this instrument computes them.")
    print()
    grid = [Fraction(0), Fraction(1, 50), Fraction(1, 10), Fraction(1, 4), Fraction(1, 2),
            Fraction(3, 4)]
    print("      %3s %-6s %-8s %10s %10s %10s %10s %s"
          % ("n", "beta", "D", "|1_D hyp|", "|2_D hyp|", "ce(1_D)", "ce(2_D)", "ce(S_f) extra"))
    cells = same = 0
    quantum_seen = 0
    for beta in (Y.THIRD, Fraction(2, 5)):
        for n in range(3, 8):
            for D in grid:
                h1, c1 = Y.one_D(rows[n], D, beta)
                h2, c2 = Y.two_D(rows[n], D, beta)
                _, cs = Y.s_f(rows[n], D, beta)
                cells += 1
                if sorted(c1) == sorted(c2):
                    same += 1
                extra = sorted(set(cs) - set(c2))
                if extra:
                    quantum_seen += 1
                if beta == Y.THIRD and n == 7:
                    print("      %3d %-6s %-8s %10d %10d %10d %10d %s"
                          % (n, beta, D, h1, h2, len(c1), len(c2),
                             "%d (d == D exactly)" % len(extra) if extra else "0"))
    check("m2.a", same == cells,
          "(1_D) and (2_D) have the SAME counterexample set in all %d (n, beta, D) cells" % cells)
    print()
    print("    THE HYPOTHESIS POPULATIONS ARE NOT THE SAME AND THAT IS THE WHOLE ASYMMETRY:")
    print("    at beta = 1/3 the (1_D) column is 0 at every n and every D -- the frozen class is")
    print("    empty (e0 T6) -- while the (2_D) column is the entire non-chain population.  The")
    print("    two readings agree on the VERDICT because they are contrapositives; they differ")
    print("    completely on what a sweep actually looks at.")
    print()
    print("    THE `>` / `>=` GAP.  mg-0b96 §6 writes `f(2e-2) >= 1/3`, which reads the threshold")
    print("    CLOSED; (2_D) reads it open.  The two differ exactly on posets with d == D, i.e. by")
    print("    one density quantum 1/C(n,2) -> 0.  Measured above: the `ce(S_f) extra` column is")
    print("    non-zero in %d of %d cells, always exactly the posets sitting ON the threshold."
          % (quantum_seen, cells))

    # ------------------------------------------------------------------ m3
    rule("m3  THE STRICT READING IS NOT OPEN -- IT IS FALSE, AND THE REFUTERS ARE ON THE RECORD")
    print("    If `f` is STRICTLY increasing at D (or if f(D) > 1/3 at all), then f(d) > 1/3 for")
    print("    every d > D, so S_f demands delta > 1/3 STRICTLY on every poset denser than D.")
    print("    The boundary class sits at delta = 1/3 EXACTLY.  So S_f is refuted at every n where")
    print("    the boundary class reaches above D_needed(n) -- and m1's family is exactly that.")
    print()
    print("      %3s  %-12s %-12s %-10s %s"
          % ("n", "family d", "D_needed(n)", "d > D?", "strict reading"))
    for n in list(range(3, 10)) + [14, 15, 40, 64, 65, 66, 67, 99]:
        d = Y.d_boundary(n)
        Dn = Y.d_needed(n)
        hit = d > Dn
        print("      %3d  %-12s %-12s %-10s %s"
              % (n, d, Dn, "yes" if hit else "no",
                 "REFUTED" if hit else "not refuted by this family"))
    print()
    print("    THE WITNESS SET IS COMPUTED, NOT ASSERTED AS A RANGE, AND IT IS RAGGED:")
    wit = [n for n in range(3, 400) if Y.d_boundary(n) > Y.d_needed(n)]
    gaps = [n for n in range(3, wit[-1] + 1) if n not in wit]
    print("      refuted at %d values of n, from %d to %d; the ONLY gap below the top is %s,"
          % (len(wit), wit[0], wit[-1], gaps))
    print("      and above %d there is none at all." % wit[-1])
    check("m3.a", gaps == [65] and wit[-1] == 66,
          "n = 65 is a HOLE INSIDE the range and it is the floor's doing: 65 = 3*21+2, so "
          "floor(n/3) sticks at 21 while D_needed keeps falling")
    check("m3.b", all(Y.d_boundary(n) <= Y.d_needed(n) for n in range(67, 400)),
          "and every n from 67 to 399 is outside, searched rather than asserted")
    print()
    print("    ⚠️  `every n <= 66` WOULD HAVE BEEN FALSE AT EXACTLY ONE VALUE, and only computing")
    print("    the set says so.  The hole is not an artefact of choosing this family: F23's")
    print("    closed form IS the maximum over the whole boundary class, so if it continues then")
    print("    at n = 65 NO delta = 1/3 poset reaches D_needed and the strict reading is")
    print("    unrefuted there by any witness of this kind.")
    print()
    print("    THE CROSSING IS EXACT ARITHMETIC, NOT A SWEEP: 4*floor(n/3)/(n(n-1)) > eps_dem*(n+1)/n")
    print("    fails first at n = 67, where F23's ceiling itself drops below the density row 8")
    print("    needs.  Below that the strict reading is FALSE; above it, this family stops being a")
    print("    witness and the arm claims nothing.")
    print()
    print("    KIND.  The refutation is `FP✗`-shaped -- one witness kills a universal -- but its")
    print("    witness is a CONSTRUCTION, not a census: m1 verifies the family at n <= 9 and the")
    print("    ordinal-sum lemma carries it to every n.  The `n <= 66` bound is arithmetic on")
    print("    F23's CLOSED FORM, and F23's closed form is `FP` to n = 9.  ⚠️  SO THE REFUTATION")
    print("    ABOVE n = 9 RESTS ON THE FAMILY'S OWN delta AND d, WHICH THE LEMMA GIVES, AND NOT")
    print("    ON F23's MAXIMALITY, WHICH IT DOES NOT NEED.")

    # ------------------------------------------------------------------ m4
    rule("m4  THE PRIMITIVITY OBJECTION, MEASURED AND CONCEDED")
    print("    A minimal counterexample is primitive (STATE.md ledger row 2), so a version of S_f")
    print("    restricted to PRIMITIVE posets would serve row 8 just as well -- and every refuter")
    print("    in m3 is an ordinal sum, which is exactly what primitive excludes.  So: how much of")
    print("    the boundary class is primitive?")
    print()
    print("      %3s  %14s  %14s  %s" % ("n", "delta = 1/3", "of those, prim", "their densities"))
    prim_total = bnd_total = 0
    for n in range(3, 9):
        b = [(d, pr) for (d, dl, pr, _) in tab[n] if dl == Y.THIRD]
        p = [d for (d, pr) in b if pr]
        prim_total += len(p)
        bnd_total += len(b)
        print("      %3d  %14d  %14d  %s" % (n, len(b), len(p), [str(x) for x in p] or "--"))
    check("m4.a", prim_total == 1,
          "exactly ONE primitive boundary poset over every class at n <= 8, and it is n = 3")
    print()
    print("    SO m3 DOES NOT SURVIVE THE PRIMITIVE RESTRICTION ABOVE n = 3, and that is stated")
    print("    here rather than left for a reader to find.  What kills the primitive-restricted")
    print("    S_f is m2, which does not care: restricted to primitives, S_f is (2_D) restricted")
    print("    to primitives, and mg-0b96's price ALREADY RAN THROUGH PRIMITIVITY (its d2 uses")
    print("    d >= 2/n to reach n = 99).  The restriction changes the class and not the price.")
    print()
    print("    ⚠️  AND F23's OWN WARNING IS THE SAME OBSERVATION FROM THE OTHER SIDE: `48 of the 49")
    print("    are ORDINAL SUMS`.  This arm re-measures it on its own population (%d of %d at"
          % (bnd_total - prim_total, bnd_total))
    print("    n <= 8, F23's own frame runs to n = 9) and reads it FORWARD: the class that pins")
    print("    `f` and the class row 8 quantifies over are disjoint above n = 3.")

    rule("VERDICT")
    if FAIL:
        print("    RED -- %d check(s) failed: %s" % (len(FAIL), ", ".join(FAIL)))
        return 1
    print("    THE ESCAPE HATCH HAS EXACTLY ONE SURVIVING SHAPE AND IT IS THE CLOSED DOOR.")
    print("    Flat reading  -> (2_D) -> (1_D), which mg-0b96 §2 closed.")
    print("    Strict reading-> FALSE at 63 orders (3..66 except 65), by an ordinal-sum family.")
    print("    Primitive-restricted -> m3 lapses, m2 does not; same statement, same price.")
    print()
    print("    WHAT IS LEFT OF §6, AND IT IS NOT NOTHING: §6's own sentence says the object would")
    print("    be `a statement about COUNT` where every known exclusion is `a statement about")
    print("    STRUCTURE`.  That is a claim about METHOD, and it survives every line above.  A")
    print("    method is not a lever: it changes who might pay the price, not what the price is.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
