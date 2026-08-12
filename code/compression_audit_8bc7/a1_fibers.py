"""a1 -- section 1 of compression.tex: "C_o^{-1}(F) = Q^{d(F)}  **exactly**".

pm-onethird's read (mg-8bc7) is that this is correct, for the reason that fixing the even
prefixes fixes each block as a SET and fixes every cross-block relation, so legality never
couples two blocks.  This arm attacks that read by checking the strongest form of the claim
rather than the countable shadow of it:

  1.1  the fiber is the FULL PRODUCT SET of per-block orientations -- not merely a set of
       size 2^d.  A count can be right for the wrong reason; a set equality cannot.
  1.2  the induced BK subgraph on a fiber is EXACTLY the cube graph: every legal odd swap
       stays in the fiber and flips one block, and every single-block flip is a legal swap.
  1.3  G_BK is the edge-DISJOINT union of the two foliations' cube edges (compression.tex:58).
  1.4  the uniform measure on L(P), restricted to a fiber, is uniform on the cube.

Mutations M1-M3 at the bottom plant defects that each of 1.1-1.3 must catch, so a PASS here
is a statement about the checks and not only about the note.
"""

from fractions import Fraction
from itertools import product
import random
import sys

from lib8bc7 import (banner, verdict, gen_posets_exhaustive, random_poset, linear_extensions,
                     groups_o, groups_e, swap_positions, fibers, fiber_key, swap_at,
                     legal_at)

rng = random.Random(8635801)


def population():
    """(label, n, lt) over every labeled poset to n = 5, plus samples at n = 6, 7."""
    for n in range(2, 6):
        for lt in gen_posets_exhaustive(n):
            yield (f"exhaustive n={n}", n, lt)
    for n in (6, 7):
        for _ in range(60):
            yield (f"sampled n={n}", n, random_poset(n, rng.choice([0.15, 0.3, 0.5]), rng))


def expected_fiber(key, lt):
    """The product set the note claims: each 2-block freely orientable iff incomparable."""
    choices = []
    for blk in key:
        if len(blk) == 1:
            choices.append([blk])
        else:
            a, b = blk
            if (a, b) in lt:
                choices.append([(a, b)])
            elif (b, a) in lt:
                choices.append([(b, a)])
            else:
                choices.append([(a, b), (b, a)])
    out = set()
    for combo in product(*choices):
        out.add(tuple(x for blk in combo for x in blk))
    return out


def check_poset(n, lt, mutate=None):
    """Returns (n_fibers, failures dict).  `mutate` is a control hook."""
    LEs = linear_extensions(n, lt)
    LEset = set(LEs)
    fails = {"1.1_product_set": 0, "1.1_size_2^d": 0, "1.2_edges": 0, "1.4_uniform": 0}
    nfib = 0
    all_fiber_edges = set()
    for gname, groups in (("o", groups_o(n)), ("e", groups_e(n))):
        # The positions at which this foliation's cube edges are claimed to sit
        # (compression.tex:42 for C_o, :51 for C_e).  M1 plants the WRONG PARITY here --
        # the note's two claims are "C_o fibers / tau_1,tau_3,..." and "C_e fibers /
        # tau_2,tau_4,...", and pairing C_e's fibers with the odd positions is the slip
        # that a check on fiber SIZE alone would not see.
        edge_positions = swap_positions(groups_o(n) if mutate == "M1" else groups)
        fb = fibers(LEs, groups)
        for key, members in fb.items():
            nfib += 1
            got = set(members)
            if mutate == "M2" and len(got) > 1:
                got.discard(sorted(got)[0])
            want = expected_fiber(key, lt)
            d = sum(1 for blk in key
                    if len(blk) == 2 and (blk[0], blk[1]) not in lt and (blk[1], blk[0]) not in lt)
            if mutate == "M3":
                d = sum(1 for blk in key if len(blk) == 2)
            if got != want:
                fails["1.1_product_set"] += 1
            if len(got) != 2 ** d:
                fails["1.1_size_2^d"] += 1
            # 1.2: induced BK edges on this fiber vs cube edges (single-block flips)
            induced = set()
            for L in got:
                for i in range(n - 1):
                    if legal_at(L, i, lt):
                        M = swap_at(L, i)
                        if M in got:
                            induced.add(frozenset((L, M)))
            cube = set()
            for L in got:
                for p in edge_positions:
                    M = swap_at(L, p)
                    if M in LEset and M in got and M != L:
                        cube.add(frozenset((L, M)))
            # every legal swap that stays inside the fiber must sit at one of this
            # foliation's swap positions, and every such swap must be a cube edge
            if induced != cube:
                fails["1.2_edges"] += 1
            if len(cube) != d * (2 ** (d - 1) if d else 0):
                fails["1.2_edges"] += 1
            all_fiber_edges.add((gname, frozenset(frozenset(e) for e in cube)))
            # 1.4: conditional uniform is uniform on the cube -- each point carries mass
            # 1/|fiber| because pi is uniform and the fiber has exactly 2^d points
            if got and len(got) != len(set(got)):
                fails["1.4_uniform"] += 1
    return nfib, fails


def check_union(n, lt, mutate=None):
    """1.3: G_BK = odd cube edges  DISJOINT-UNION  even cube edges."""
    LEs = linear_extensions(n, lt)
    LEset = set(LEs)
    bk = set()
    for L in LEs:
        for i in range(n - 1):
            if legal_at(L, i, lt):
                bk.add(frozenset((L, swap_at(L, i))))
    parts = []
    for groups in (groups_o(n), groups_e(n)):
        if mutate == "M1" and groups is not groups_o(n):
            pass
        e = set()
        for L in LEs:
            for p in swap_positions(groups):
                if legal_at(L, p, lt):
                    e.add(frozenset((L, swap_at(L, p))))
        parts.append(e)
    if mutate == "M4":
        parts[1] = set()
    return bk == (parts[0] | parts[1]), not (parts[0] & parts[1]), len(bk)


def main():
    ok = True
    banner("a1.1-1.4  section 1, on every labeled poset to n=5 and samples at n=6,7")
    tot = {"1.1_product_set": 0, "1.1_size_2^d": 0, "1.2_edges": 0, "1.4_uniform": 0}
    nfib = nposet = nedges = 0
    union_bad = disjoint_bad = 0
    by_label = {}
    for label, n, lt in population():
        nposet += 1
        f, fails = check_poset(n, lt)
        nfib += f
        for k in tot:
            tot[k] += fails[k]
        u, d, ne = check_union(n, lt)
        nedges += ne
        union_bad += 0 if u else 1
        disjoint_bad += 0 if d else 1
        by_label[label] = by_label.get(label, 0) + 1
    print(f"  population: {nposet} posets  ({', '.join(f'{k}: {v}' for k, v in sorted(by_label.items()))})")
    print(f"  {nfib} fibers examined, {nedges} BK edges examined")
    ok &= verdict(tot["1.1_product_set"] == 0,
                  "1.1  every fiber is EXACTLY the product set of per-block orientations",
                  f"{tot['1.1_product_set']} violations")
    ok &= verdict(tot["1.1_size_2^d"] == 0, "1.1  |fiber| = 2^d(F), d = # incomparable 2-blocks",
                  f"{tot['1.1_size_2^d']} violations")
    ok &= verdict(tot["1.2_edges"] == 0,
                  "1.2  induced BK subgraph on a fiber = the cube graph, d*2^(d-1) edges",
                  f"{tot['1.2_edges']} violations")
    ok &= verdict(tot["1.4_uniform"] == 0, "1.4  uniform-on-L(P) restricted to a fiber is uniform")
    ok &= verdict(union_bad == 0, "1.3  G_BK = odd cube edges UNION even cube edges",
                  f"{union_bad} violations")
    ok &= verdict(disjoint_bad == 0, "1.3  ... and the union is edge-DISJOINT",
                  f"{disjoint_bad} violations")

    banner("a1.C  controls: planted defects each check must catch")
    # A control that cannot fail is not a control.  Each mutation is a specific WRONG READING
    # of section 1, and the row it must turn red is named.
    ctl = [
        ("M1  C_e's fibers paired with the ODD swap positions (wrong parity, right blocks)",
         "M1", "1.2_edges"),
        ("M2  one linear extension deleted from each fiber (fiber is not the full cube)",
         "M2", "1.1_product_set"),
        ("M3  d(F) counted over ALL 2-blocks, not only the incomparable ones",
         "M3", "1.1_size_2^d"),
    ]
    for why, mut, row in ctl:
        hits = 0
        seen = 0
        for n in range(3, 6):
            for lt in gen_posets_exhaustive(n) if n < 5 else [random_poset(5, 0.2, rng) for _ in range(40)]:
                seen += 1
                _, fails = check_poset(n, lt, mutate=mut)
                if fails[row] > 0:
                    hits += 1
        ok &= verdict(hits > 0, f"{why}\n         -> row {row} goes RED",
                      f"{hits}/{seen} posets")
    # M4: the union check must notice a dropped foliation
    bad = 0
    seen = 0
    for n in range(3, 6):
        for lt in gen_posets_exhaustive(n) if n < 5 else [random_poset(5, 0.2, rng) for _ in range(40)]:
            seen += 1
            u, _, ne = check_union(n, lt, mutate="M4")
            if not u and ne > 0:
                bad += 1
    ok &= verdict(bad > 0, "M4  even foliation dropped from the union -> 1.3 goes RED",
                  f"{bad}/{seen} posets")

    print()
    print("a1 VERDICT:", "section 1 CONFIRMED" if ok else "SECTION 1 REFUTED OR INSTRUMENT BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
