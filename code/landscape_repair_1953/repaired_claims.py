#!/usr/bin/env python3
"""
mg-1953 REPAIR instrument 2 of 2 -- THE REPAIRED SENTENCES, EACH MEASURED.

Every sentence this instrument certifies is a sentence mg-1953 REWRITES in
docs/OneThird-Landscape-Where-This-Lives.md.  Nothing here is a re-run of the
target's own measurements; each check is of the REPLACEMENT text, not of the
text it replaces.

  R2  E8 / L1 row H / L2 row H.  The document says Bjorner's greedoid band on
      the poset shelling antimatroid is "A PROPER SUBMONOID OF OURS".  That is
      impossible -- at the antichain the band is strictly LARGER than all of
      F(P) -- and it contradicts the "this is the free LRB" in the same cell.
      The REPLACEMENT sentence is: the word-to-move map is a monoid
      HOMOMORPHISM onto its image, the image is a submonoid of F(P), and it is
      proper exactly for n >= 3.  Measured: homomorphism, image inside F(P),
      image closed under the product, properness, injectivity (it fails), and
      free-LRB-vs-ordered-Bell at the antichain.

  R3  "STRICTLY SHARPER" (the commit subject of 714aceb).  Sharper is a
      comparison, so both sides are run at every level: the repo's triangular
      counting identity solved numerically, and Brown's closed form (REPAIRED,
      i.e. with acyclicity).  The REPLACEMENT phrase is the document's own
      "strictly more informative", and what makes it more informative is
      counted: how many levels are named a-priori as carrying zero.

  R4  The populations behind the corrected arithmetic.  Every number mg-1953
      writes into the document is produced here: classes per n and the
      cumulative counts the corrected sentences are about, moves per n, and
      product pairs per n with the n <= 5 total.

Exhaustive over all isomorphism classes to n = 6 (R3, R4) / n = 5 (R2).
"""

import sys
from itertools import permutations

from core1953 import (iso_classes, set_partitions, ordered_set_partitions,
                      linear_extensions, quotient_is_acyclic,
                      blocks_are_antichains, refines, factorial)


# ============================================================== the monoid ==

def F_of_P(n, rel):
    """The P-compatible ordered set partitions: i < j in P implies the block of
    i is at or before the block of j.  (Equivalently the weakly order-
    preserving surjections P -> chain.)"""
    out = []
    for osp in ordered_set_partitions(n):
        where = {}
        for p, B in enumerate(osp):
            for i in B:
                where[i] = p
        if all(where[i] <= where[j] for (i, j) in rel):
            out.append(osp)
    return out


def product(x, y):
    """The repo's product: non-empty B_p & C_q in lexicographic (p, q) order."""
    out = []
    for B in x:
        for C in y:
            D = B & C
            if D:
                out.append(D)
    return tuple(out)


# ================================== R2 -- Bjorner's band on the shelling AM ==

def feasible_words(n, rel):
    """The poset shelling antimatroid: words of distinct elements every prefix
    of which is a down-set of P.  All lengths 0..n."""
    below = [set() for _ in range(n)]
    for (i, j) in rel:
        below[j].add(i)
    out = []

    def rec(w, used):
        out.append(tuple(w))
        for x in range(n):
            if x not in used and below[x] <= used:
                rec(w + [x], used | {x})

    rec([], frozenset())
    return out


def greedy_product(u, v):
    """Bjorner's greedoid product: u, then the letters of v not already used."""
    return u + tuple(x for x in v if x not in u)


def phi(n, w):
    """word -> move:  ({w_1}, ..., {w_k}, rest), the rest dropped when empty."""
    rest = frozenset(range(n)) - frozenset(w)
    blocks = [frozenset([x]) for x in w]
    if rest:
        blocks.append(rest)
    return tuple(blocks)


def check_R2(n):
    rows = []
    for rel in iso_classes(n):
        FW = feasible_words(n, rel)
        FP = set(F_of_P(n, rel))
        img = set(phi(n, w) for w in FW)
        rows.append(dict(
            nband=len(FW), nFP=len(FP), nimg=len(img),
            injective=len(img) == len(FW),
            band_bigger=len(FW) > len(FP),
            image_inside=img <= FP,
            image_closed=all(product(x, y) in img for x in img for y in img),
            identity_in=phi(n, ()) in img,
            hom=all(phi(n, greedy_product(u, v)) == product(phi(n, u), phi(n, v))
                    for u in FW for v in FW),
            proper=img < FP,
        ))
    return rows


# ============================ R3 -- "sharper" run as a two-sided comparison ==

def AC_of_P(n, rel, flats):
    return [X for X in flats if quotient_is_acyclic(rel, X)]


def induced_extension_count(n, rel, B):
    elts = sorted(B)
    idx = {x: k for k, x in enumerate(elts)}
    sub = {(idx[a], idx[b]) for (a, b) in rel if a in B and b in B}
    return len(linear_extensions(len(elts), sub))


def repo_solve(n, rel, AC):
    """The repo's recipe: solve  sum_{Y in AC, Y refines X} m_Y =
    prod_B |L(P|_B)|  from the finest level upwards.  No closed form used."""
    order = sorted(range(len(AC)), key=lambda i: len(AC[i]), reverse=True)
    ref = {}
    m = {}
    for a in order:
        X = AC[a]
        rhs = 1
        for B in X:
            rhs *= induced_extension_count(n, rel, B)
        s = 0
        for b in order:
            if b == a:
                continue
            key = (b, a)
            if key not in ref:
                ref[key] = refines(AC[b], X)
            if ref[key]:
                s += m[b]
        m[a] = rhs - s
    return m


def brown_closed_form(rel, AC):
    """Brown's Theorem 2 as REPAIRED: antichain blocks AND acyclic quotient.
    On AC(P) acyclicity holds by construction, so the live condition here is
    the antichain one -- which is exactly why the target's restriction to
    AC(P) could not see the missing clause (see closed_form_outside_AC.py)."""
    out = {}
    for a, X in enumerate(AC):
        if blocks_are_antichains(rel, X):
            p = 1
            for B in X:
                p *= factorial(len(B) - 1)
            out[a] = p
        else:
            out[a] = 0
    return out


def check_R3(n):
    flats = set_partitions(n)
    s = dict(classes=0, levels=0, disagreements=0, posets_bad=0,
             zero_levels=0, nonzero_levels=0)
    for rel in iso_classes(n):
        s['classes'] += 1
        AC = AC_of_P(n, rel, flats)
        s['levels'] += len(AC)
        mr = repo_solve(n, rel, AC)
        mb = brown_closed_form(rel, AC)
        bad = sum(1 for a in range(len(AC)) if mr[a] != mb[a])
        s['disagreements'] += bad
        if bad:
            s['posets_bad'] += 1
        s['zero_levels'] += sum(1 for a in range(len(AC)) if mr[a] == 0)
        s['nonzero_levels'] += sum(1 for a in range(len(AC)) if mr[a] != 0)
    return s


# =========================================== R4 -- the populations, rebuilt ==

def check_R4(n):
    flats = set_partitions(n)
    classes = iso_classes(n)
    moves = 0
    pairs = 0
    levels = 0
    connected = 0
    for rel in iso_classes(n):
        FP = F_of_P(n, rel)
        moves += len(FP)
        pairs += len(FP) ** 2
        levels += len(AC_of_P(n, rel, flats))
    return dict(classes=len(classes), moves=moves, pairs=pairs, levels=levels)


# ============================================================================

def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("=" * 78)
    print("mg-1953 REPAIR 2 -- THE REPLACEMENT SENTENCES, EACH MEASURED.")
    print("=" * 78)
    print()

    print("-" * 78)
    print("R2  E8 / row H.  Document: 'A PROPER SUBMONOID OF OURS'.")
    print("    Replacement: the word-to-move map is a monoid HOMOMORPHISM whose")
    print("    IMAGE is a submonoid of F(P), proper exactly for n >= 3.")
    print("-" * 78)
    print("%3s %8s %10s %10s %10s %11s %11s %11s %11s %11s"
          % ("n", "classes", "hom", "img<=F(P)", "img closed", "1 in img",
             "PROPER", "injective", "band>|F(P)|", "img==F(P)"))
    for n in range(2, min(nmax, 5) + 1):
        rows = check_R2(n)
        N = len(rows)
        f = lambda k: "%d of %d" % (sum(r[k] for r in rows), N)
        print("%3d %8d %10s %10s %10s %11s %11s %11s %11s %11s"
              % (n, N, f('hom'), f('image_inside'), f('image_closed'),
                 f('identity_in'), f('proper'), f('injective'),
                 f('band_bigger'),
                 "%d of %d" % (sum(not r['proper'] for r in rows), N)))
    print()
    print("    The antichain in detail -- the case the document's own cell names")
    print("    'the free LRB' while also calling it a submonoid:")
    print("%3s %22s %22s %14s"
          % ("n", "|band| (free LRB)", "|F(antichain)|", "band > F(P)?"))
    for n in range(2, min(nmax, 5) + 1):
        anti = frozenset()
        b = len(feasible_words(n, anti))
        f = len(F_of_P(n, anti))
        print("%3d %22d %22d %14s" % (n, b, f, "YES" if b > f else "no"))
    print()
    print("    |band| = sum_k n!/(n-k)! (A000522, the free left regular band on")
    print("    n generators); |F(antichain)| = the ordered Bell number A000670.")
    print("    A set strictly larger than F(P) cannot be a submonoid of F(P).")
    print()

    print("-" * 78)
    print("R3  'STRICTLY SHARPER' vs 'strictly more informative'.  Both sides")
    print("    run at EVERY level: the repo's triangular solve, and Brown's")
    print("    closed form.  Sharper would need a level where they differ.")
    print("-" * 78)
    print("%3s %8s %9s %11s %20s %14s %16s"
          % ("n", "classes", "levels", "cum.levels", "disagreeing levels",
             "posets bad", "levels named 0"))
    cum = 0
    tot_zero = 0
    for n in range(2, nmax + 1):
        s = check_R3(n)
        cum += s['levels']
        tot_zero += s['zero_levels']
        print("%3d %8d %9d %11d %20s %14s %16s"
              % (n, s['classes'], s['levels'], cum,
                 "%d of %d" % (s['disagreements'], s['levels']),
                 "%d of %d" % (s['posets_bad'], s['classes']),
                 "%d of %d" % (s['zero_levels'], s['levels'])))
    print()
    print("    0 disagreeing levels anywhere: Brown's answer IS the repo's")
    print("    answer.  What Theorem 2 adds is that the last column is known")
    print("    BEFORE the solve -- more informative, not sharper.")
    print()

    print("-" * 78)
    print("R4  The populations behind the corrected arithmetic.")
    print("-" * 78)
    print("%3s %9s %9s %9s %14s %14s"
          % ("n", "classes", "moves", "levels", "product pairs", "cum.classes"))
    cum_cls = 0
    cum_pairs = 0
    cum_by_n = {}
    for n in range(1, nmax + 1):
        r = check_R4(n)
        cum_cls += r['classes']
        cum_pairs += r['pairs']
        cum_by_n[n] = (cum_cls, cum_pairs, r)
        print("%3d %9d %9d %9d %14d %14d"
              % (n, r['classes'], r['moves'], r['levels'], r['pairs'], cum_cls))
    print()
    print("    The three populations the corrected sentences are about:")
    if nmax >= 5:
        c5, p5, _ = cum_by_n[5]
        print("      n <= 5, ALL classes incl. n=1 (the chains_in_JP table's own")
        print("      range):  %d classes,  %d product pairs" % (c5, p5))
        print("        -- the document said 63 classes and 922 073 pairs, which")
        print("           are the n = 5 ROW: %d and %d"
              % (cum_by_n[5][2]['classes'], cum_by_n[5][2]['pairs']))
    if nmax >= 6:
        c6 = cum_by_n[6][0]
        n1 = cum_by_n[1][2]['classes']
        n2 = cum_by_n[2][2]['classes']
        print("      n = 2..6 (identify_lattice's own range, E3's population):"
              "  %d classes" % (c6 - n1))
        print("        -- the document said 405, which is n = 1..6: %d" % c6)
        print("      n = 3..6 (P2's population; P2 is n/a for n < 3):  %d classes"
              % (c6 - n1 - n2))
        print("        -- the document's section 6 item 5 said 405 there too")
    print()
    print("=" * 78)


if __name__ == "__main__":
    main()
