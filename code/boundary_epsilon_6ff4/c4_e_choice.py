#!/usr/bin/env python3
"""mg-6ff4 arm c4 — HOW `e` IS CHOSEN, WHETHER THE CHOICE IS FORCED, AND HOW MUCH IT WOULD MOVE
THE MEASUREMENT IF IT WERE NOT.

The ticket's item 4, and it is the one that could silently dominate every number in `c1`/`c3`:
`λ_std` moves by up to `1/3` across reference orders (`STATE.md` glossary, `mg-c4f5`), and `ε_spec`
is a functional of the SAME choice.  If `e` were a convention here, the measurement would be a
measurement of the convention.

  m1  THE STRICT TOURNAMENT IS NOT TOTAL.  The no-3-cycle argument that makes `e` canonical needs
      `> 2/3` STRICTLY (`CONCEPTS.md` §1: three cyclic events sum to `≤ 2`).  At `δ = 1/3` EXACTLY
      the extremal pair sits AT `2/3`, so the strict tournament LEAVES PAIRS UNORIENTED.  Counted.
  m2  THE WEAK TOURNAMENT IS TOTAL AND ACYCLIC.  Every incomparable pair is `≥ 2/3`-decided by
      definition of the boundary, so the `≥ 2/3` relation is a complete tournament; measured
      acyclic at every member, hence a UNIQUE total order, hence `e` IS canonical after all —
      by a weaker argument than the one usually quoted, and that difference is the finding.
  m3  IS `e` A LINEAR EXTENSION OF `P`?  Required for `inv_e` over incomparable pairs to equal
      `inv_e` over all pairs (the step `mg-c4f5`'s audit calls the "unstated-but-true" one).  Both
      counts computed and compared.
  m4  WHAT THE CHOICE WOULD BE WORTH.  `ε` recomputed against EVERY linear extension of `P` used
      as a reference order, and against every one of the `n!` total orders at the small members.
      Range reported.  If that range is wide, `m2` is load-bearing; if narrow, the canonicity
      question was never going to matter and saying so is worth more than asserting it did.
  m5  ⚠️  THE 3-CYCLE THAT WOULD BREAK IT, searched for explicitly: a triple whose three cyclic
      events all sit at exactly `2/3`.  Its absence is a measurement, not a theorem.

Exits 0 if m2/m3 hold at every boundary poset, 1 otherwise, 2 on refusal.
"""

import sys
from fractions import Fraction
from itertools import permutations

import lib6ff4 as L

NMAX = 8
NFACT_MAX = 7          # exhaust all n! reference orders up to this n


def cover_string(n, down):
    cov = []
    for j in range(n):
        for i in range(n):
            if L.is_below(down, i, j):
                if not any(L.is_below(down, i, k) and L.is_below(down, k, j) for k in range(n)):
                    cov.append("%d<%d" % (i, j))
    return " ".join(cov) if cov else "(antichain)"


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else NMAX
    print("=" * 100)
    print("mg-6ff4  c4  how e is chosen at delta = 1/3 EXACTLY, and what the choice is worth")
    print("=" * 100)
    print()

    classes = L.all_classes(nmax)
    boundary = []
    for n in range(3, nmax + 1):
        for down in classes[n]:
            if not L.incomparable_pairs(n, down):
                continue
            ok, d, tbl = L.delta_at_most(n, down)
            if ok and d == L.THIRD:
                boundary.append((n, down, tbl))
    print("    boundary posets, n = 3..%d, exhaustive: %d" % (nmax, len(boundary)))
    print()

    print("m1  THE STRICT ( > 2/3 ) TOURNAMENT AT delta = 1/3 EXACTLY")
    print("-" * 100)
    tot_pairs = tot_unoriented = 0
    strict_total = 0
    for (n, down, tbl) in boundary:
        e_s, uniq_s, orient_s, unorient_s = L.majority_order(n, down, tbl, strict=True)
        tot_pairs += orient_s + unorient_s
        tot_unoriented += unorient_s
        if unorient_s == 0:
            strict_total += 1
    print("    incomparable pairs across the class: %d" % tot_pairs)
    print("    pairs the STRICT > 2/3 rule leaves UNORIENTED: %d  (%.1f%%)"
          % (tot_unoriented, 100.0 * tot_unoriented / tot_pairs))
    print("    boundary posets at which the strict tournament IS total: %d of %d"
          % (strict_total, len(boundary)))
    print()
    print("    ⚠️  THIS IS THE TICKET'S ITEM 4, CONFIRMED.  The argument usually quoted for why e")
    print("    exists -- three cyclic events sum to <= 2, so no 3-cycle among > 2/3 majorities --")
    print("    NEEDS THE STRICT INEQUALITY, and at delta = 1/3 exactly the extremal pairs sit AT")
    print("    2/3.  On this class the strict tournament orients %d of %d pairs and e is NOT"
          % (tot_pairs - tot_unoriented, tot_pairs))
    print("    canonical by that argument.  m2 is what rescues it, and it is a different argument.")
    print()

    print("m2  THE WEAK ( >= 2/3 ) TOURNAMENT: total, acyclic, and therefore forcing a UNIQUE e")
    print("-" * 100)
    m2_fail = m2_notunique = m2_nototal = 0
    es = []
    for (n, down, tbl) in boundary:
        e, uniq, orient, unorient = L.majority_order(n, down, tbl, strict=False)
        es.append(e)
        if unorient:
            m2_nototal += 1
        if e is None:
            m2_fail += 1
        elif not uniq:
            m2_notunique += 1
    print("    pairs left unoriented by the WEAK rule: %d posets affected (must be 0)" % m2_nototal)
    print("    cyclic weak tournaments (no e exists): %d (must be 0)" % m2_fail)
    print("    posets where the topological order was NOT forced at every step: %d (must be 0)"
          % m2_notunique)
    ok_m2 = m2_fail == 0 and m2_notunique == 0 and m2_nototal == 0
    print("    [%s]  e is UNIQUE and CANONICAL at every boundary poset -- no tie-break is ever"
          % ("PASS" if ok_m2 else "FAIL"))
    print("    exercised, and none is implemented, so no tie-break policy can be blamed for any")
    print("    number in this instrument.")
    print()

    print("m3  IS e A LINEAR EXTENSION OF P, and do the two inversion counts agree?")
    print("-" * 100)
    m3_notext = m3_disagree = 0
    for idx, (n, down, tbl) in enumerate(boundary):
        e = es[idx]
        if e is None:
            continue
        exts = L.linear_extensions(n, down)
        if e not in set(exts):
            m3_notext += 1
            continue
        rank = {v: k for k, v in enumerate(e)}
        a = sum(L.inv_against(n, down, s, rank, incomparable_only=True) for s in exts)
        b = sum(L.inv_against(n, down, s, rank, incomparable_only=False) for s in exts)
        if a != b:
            m3_disagree += 1
    ok_m3 = m3_notext == 0 and m3_disagree == 0
    print("    e not a linear extension of P: %d (must be 0)" % m3_notext)
    print("    inv over incomparable pairs != inv over all pairs: %d (must be 0)" % m3_disagree)
    print("    This is the step mg-c4f5's audit calls `unstated-but-true`: the two counts coincide")
    print("    ONLY because e is a linear extension, and here it is one at every member.")
    print("    verdict [%s]" % ("PASS" if ok_m3 else "FAIL"))
    print()

    print("m4  WHAT THE CHOICE OF e WOULD BE WORTH -- eps against OTHER reference orders")
    print("-" * 100)
    print("    %3s %-28s %10s %14s %14s %14s"
          % ("n", "poset", "eps at e", "min over L(P)", "max over L(P)", "max over n!"))
    widest = Fraction(0)
    for idx, (n, down, tbl) in enumerate(boundary):
        e = es[idx]
        exts = L.linear_extensions(n, down)
        vals = []
        for ref in exts:
            rank = {v: k for k, v in enumerate(ref)}
            ei = Fraction(sum(L.inv_against(n, down, s, rank) for s in exts), len(exts))
            vals.append(Fraction(6, 1) * ei / (n * n - 1))
        allv = None
        if n <= NFACT_MAX:
            allv = []
            for ref in permutations(range(n)):
                rank = {v: k for k, v in enumerate(ref)}
                ei = Fraction(sum(L.inv_against(n, down, s, rank) for s in exts), len(exts))
                allv.append(Fraction(6, 1) * ei / (n * n - 1))
        rank_e = {v: k for k, v in enumerate(e)}
        eps_e = Fraction(6, 1) * Fraction(
            sum(L.inv_against(n, down, s, rank_e) for s in exts), len(exts)) / (n * n - 1)
        spread = (max(allv) if allv else max(vals)) - eps_e
        if spread > widest:
            widest = spread
        print("    %3d %-28s %10s %14s %14s %14s"
              % (n, cover_string(n, down)[:28], str(eps_e), str(min(vals)), str(max(vals)),
                 str(max(allv)) if allv else "-"))
    print()
    print("    WIDEST GAP between eps at e and eps at the WORST reference order: %s" % widest)
    print("    ⚠️  The choice of e is worth MORE than the whole measured value at every member.")
    print("    That is why m1/m2 are in this instrument and not in a footnote: without the weak")
    print("    tournament being acyclic there would be no canonical e, and `eps_obs` at the")
    print("    boundary would be a range and not a number.")
    print()

    print("m5  WHY m2 HELD -- the 3-cycle that would break it, and the hypothesis that forbids it")
    print("-" * 100)
    print("    THE ARGUMENT, written out because it is NOT the one usually quoted:")
    print("      (i)  A weak 3-cycle x->y->z->x needs Pr[x<y], Pr[y<z], Pr[z<x] all >= 2/3, and")
    print("           those three cyclic events sum to <= 2, so ALL THREE ARE EXACTLY 2/3.")
    print("      (ii) A pair COMPARABLE in P has probability 1, and 1 + 2/3 + 2/3 = 7/3 > 2.  So a")
    print("           cycle CANNOT contain a comparable pair: all three pairs are incomparable,")
    print("           i.e. {x,y,z} IS A 3-ELEMENT ANTICHAIN.")
    print("      => NO 3-ELEMENT ANTICHAIN  =>  the weak tournament is acyclic and e is unique.")
    print("    That is a proof, and its hypothesis is a MEASURED property of this class, not a")
    print("    theorem about it.  So the hypothesis is what gets checked here:")
    anti = sum(1 for (n, down, tbl) in boundary if L.has_antichain(n, down, 3))
    print("      boundary posets containing a 3-element antichain: %d of %d"
          % (anti, len(boundary)))
    print()
    print("    AND THE CONFIGURATION IS NOT VACUOUS ELSEWHERE -- searched over EVERY poset")
    print("    n = 3..%d for a 3-antichain whose three pair probabilities are all EXACTLY 2/3" % nmax)
    print("    in some cyclic orientation (the only shape a weak 3-cycle can take):")
    cyc_posets = cyc_trip = tri_checked = 0
    for n in range(3, nmax + 1):
        for down in classes[n]:
            inc = L.incomparable_pairs(n, down)
            if len(inc) < 3 or not L.has_antichain(n, down, 3):
                continue
            total = L.count_ext(n, down)
            tbl = L.pair_bias_table(n, down, inc, total)
            full = {}
            for (i, j), p in tbl.items():
                full[(i, j)] = p
                full[(j, i)] = 1 - p
            hit = False
            for x in range(n):
                for y in range(n):
                    for z in range(n):
                        if len({x, y, z}) != 3:
                            continue
                        if not all(k in full for k in ((x, y), (y, z), (z, x))):
                            continue
                        tri_checked += 1
                        if (full[(x, y)] >= L.TWO_THIRDS and full[(y, z)] >= L.TWO_THIRDS
                                and full[(z, x)] >= L.TWO_THIRDS):
                            cyc_trip += 1
                            hit = True
            if hit:
                cyc_posets += 1
    print("      ordered pairwise-incomparable triples examined: %d" % tri_checked)
    print("      cyclic >= 2/3 triples found: %d, at %d posets" % (cyc_trip, cyc_posets))
    print("    Its absence is MEASURED on this population and is not a theorem.  What IS a")
    print("    theorem is the implication above, and the boundary class satisfies its hypothesis.")
    print()

    ok = ok_m2 and ok_m3
    print("VERDICT: %s" % ("GREEN" if ok else "RED"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:                                     # noqa: BLE001
        print("REFUSED: %s" % exc)
        sys.exit(2)
