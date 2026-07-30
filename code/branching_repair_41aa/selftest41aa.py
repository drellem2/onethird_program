"""Self-test for code/branching_repair_41aa.

Every object this repair uses is rebuilt from its definition, so every object
has to be certified against something published.  The certificates here are
A000112 (posets on n unlabelled points), A000041 (partitions), the hook length
formula, sum_lambda (f^lambda)^2 = n!, the Fibonacci rank sizes and the
differential condition of the Young-Fibonacci lattice, Birkhoff's
representation theorem checked as an equality, and the two standard
non-distributive lattices M3 and N5.

Exit code 1 on any failure, and `run_all.sh` stops if it fails.
"""

import sys
from itertools import permutations
from math import comb, factorial

from kern41aa import (mk, is_poset, canon, iso, all_posets, ideals,
                      ideal_lattice, linear_extensions, partitions, sub, cells,
                      skew_poset, young_interval, interval_poset, conj,
                      hook_length_formula, chain, grid, disjoint_union,
                      is_lattice, is_distributive, join_irreducibles,
                      young_fibonacci, yf_interval_poset)

OUT = sys.stdout
FAILS = []
N = [0]


def check(name, got, want):
    N[0] += 1
    ok = got == want
    if not ok:
        FAILS.append((name, got, want))
    print("  %-3d %-62s %s" % (N[0], name, "PASS" if ok else
                               "FAIL got %r want %r" % (got, want)), file=OUT)


def main():
    print("=" * 78, file=OUT)
    print("SELF-TEST  code/branching_repair_41aa", file=OUT)
    print("=" * 78, file=OUT)
    print(file=OUT)

    # ---- the poset enumeration, against A000112 -------------------------
    classes = {n: all_posets(n) for n in range(0, 7)}
    check("A000112: posets on 0..6 points",
          [len(classes[n]) for n in range(0, 7)], [1, 1, 2, 5, 16, 63, 318])
    check("every enumerated relation is a poset",
          all(is_poset(P) for n in classes for P in classes[n]), True)
    check("enumerated classes are pairwise non-isomorphic (n = 5)",
          len({canon(P) for P in classes[5]}), 63)

    # ---- canon and iso ---------------------------------------------------
    bad = 0
    for P in classes[4]:
        n, down = P
        for p in permutations(range(n)):
            pairs = [(p[a], p[b]) for b in range(n) for a in range(n)
                     if down[b] >> a & 1]
            if canon(mk(n, pairs)) != canon(P):
                bad += 1
    check("canon is invariant under all 24 relabellings (all 16 posets, n=4)",
          bad, 0)
    bad = 0
    for P in classes[4]:
        for Q in classes[4]:
            if (iso(P, Q) is not None) != (canon(P) == canon(Q)):
                bad += 1
    check("iso agrees with canon on all 256 ordered pairs (n = 4)", bad, 0)

    # ---- order ideals ----------------------------------------------------
    check("|J(antichain_n)| = 2^n for n <= 6",
          [len(ideals(mk(n, []))) for n in range(1, 7)],
          [2 ** n for n in range(1, 7)])
    check("|J(chain_n)| = n+1 for n <= 6",
          [len(ideals(chain(n))) for n in range(1, 7)],
          [n + 1 for n in range(1, 7)])
    check("|L(antichain_n)| = n! for n <= 5",
          [len(linear_extensions(mk(n, []))) for n in range(1, 6)],
          [factorial(n) for n in range(1, 6)])

    # ---- Birkhoff, as an equality ---------------------------------------
    bad = nonlat = nondist = 0
    for n in range(1, 5):
        for P in classes[n]:
            J, _ = ideal_lattice(P)
            if not is_lattice(J):
                nonlat += 1
            if not is_distributive(J)[0]:
                nondist += 1
            JI, _ = join_irreducibles(J)
            if iso(JI, P) is None:
                bad += 1
    check("J(P) is a lattice, every P with n <= 4", nonlat, 0)
    check("J(P) is distributive, every P with n <= 4", nondist, 0)
    check("Birkhoff: join-irreducibles of J(P) = P, every P with n <= 4", bad, 0)

    # ---- M3 and N5, the two forbidden sublattices ------------------------
    M3 = mk(5, [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 4)])
    N5 = mk(5, [(0, 1), (1, 4), (0, 2), (2, 3), (3, 4)])
    check("M3 is a lattice", is_lattice(M3), True)
    check("M3 is NOT distributive", is_distributive(M3)[0], False)
    check("N5 is a lattice", is_lattice(N5), True)
    check("N5 is NOT distributive", is_distributive(N5)[0], False)
    B3, _ = ideal_lattice(mk(3, []))
    check("the Boolean lattice B_3 IS distributive", is_distributive(B3)[0], True)

    # ---- partitions, against A000041 ------------------------------------
    check("A000041: partitions of 1..8",
          [len(partitions(n)) for n in range(1, 9)],
          [1, 2, 3, 5, 7, 11, 15, 22])
    check("conjugation is an involution on partitions of 7",
          all(conj(conj(l)) == l for l in partitions(7)), True)

    # ---- shapes and tableaux --------------------------------------------
    bad = 0
    for n in range(1, 7):
        for lam in partitions(n):
            P, _ = skew_poset(lam)
            if len(linear_extensions(P)) != hook_length_formula(lam):
                bad += 1
    check("e(D_lambda) = hook length formula, every lambda with |lambda| <= 6",
          bad, 0)
    check("sum_lambda (f^lambda)^2 = n! for n <= 7",
          [sum(hook_length_formula(l) ** 2 for l in partitions(n))
           for n in range(1, 8)],
          [factorial(n) for n in range(1, 8)])
    check("f^(3,2,1) = 16 (standard textbook value)",
          hook_length_formula((3, 2, 1)), 16)

    # ---- intervals of Young's lattice ------------------------------------
    check("|[empty, (3,2)]| = 9 sub-diagrams, counted by hand",
          len(young_interval((), (3, 2))), 9)
    bad = 0
    for lam in partitions(5):
        IP, elems = interval_poset((), lam)
        P, _ = skew_poset(lam)
        J, _ = ideal_lattice(P)
        if iso(J, IP) is None:
            bad += 1
    check("J(D_lambda) = [empty, lambda], every lambda |- 5", bad, 0)
    Q, _ = skew_poset((2, 1), (1,))
    check("the skew shape (2,1)/(1) is the 2-element ANTICHAIN",
          canon(Q), canon(mk(2, [])))
    check("(2,1)/(1) is not a straight cell poset",
          canon(Q) in {canon(skew_poset(l)[0]) for l in partitions(2)}, False)
    check("straight cell poset classes, n = 1..7",
          [len({canon(skew_poset(l)[0]) for l in partitions(n)})
           for n in range(1, 8)], [1, 1, 2, 3, 4, 6, 8])

    # ---- the grid --------------------------------------------------------
    check("|grid(p,q)| = (p+1)(q+1) for p,q <= 4",
          [grid(p, q)[0][0] for p in range(1, 5) for q in range(1, 5)],
          [(p + 1) * (q + 1) for p in range(1, 5) for q in range(1, 5)])
    bad = 0
    for p in range(1, 5):
        for q in range(1, 5):
            G, _ = grid(p, q)
            J, _ = ideal_lattice(disjoint_union(chain(p), chain(q)))
            if iso(G, J) is None:
                bad += 1
    check("grid(p,q) = J(C_p + C_q) for all 16 pairs p,q <= 4", bad, 0)

    # ---- the box bound ---------------------------------------------------
    def parts_in_box(b):
        out = set()

        def rec(i, cap, cur):
            if i == b:
                out.add(tuple(x for x in cur if x > 0))
                return
            for v in range(min(cap, b), -1, -1):
                cur.append(v)
                rec(i + 1, v, cur)
                cur.pop()
        rec(0, b, [])
        return out
    check("partitions in the b x b box = C(2b, b), b = 1..5",
          [len(parts_in_box(b)) for b in range(1, 6)],
          [comb(2 * b, b) for b in range(1, 6)])

    # ---- Young-Fibonacci -------------------------------------------------
    ranks, covers = young_fibonacci(6)
    check("Young-Fibonacci rank sizes to rank 6 are Fibonacci",
          [len(ranks[r]) for r in range(7)], [1, 1, 2, 3, 5, 8, 13])
    dn = {}
    for v, us in covers.items():
        for x in us:
            dn.setdefault(x, set()).add(v)
    bad = 0
    for r in range(0, 6):
        for v in ranks[r]:
            du, ud = {}, {}
            for u in covers[v]:
                for x in dn.get(u, ()):
                    du[x] = du.get(x, 0) + 1
            for y in dn.get(v, ()):
                for z in covers[y]:
                    ud[z] = ud.get(z, 0) + 1
            diff = {k: du.get(k, 0) - ud.get(k, 0)
                    for k in set(du) | set(ud) if du.get(k, 0) != ud.get(k, 0)}
            if diff != {v: 1}:
                bad += 1
    check("Young-Fibonacci: DU - UD = I below the top rank", bad, 0)
    ivs = [w for r in range(0, 7) for w in ranks[r]]
    check("Young-Fibonacci intervals [0-hat, w], rank(w) <= 6", len(ivs), 33)
    nd = 0
    for w in ivs:
        P, _ = yf_interval_poset(w, ranks, covers)
        if not is_lattice(P):
            nd = -1
            break
        if not is_distributive(P)[0]:
            nd += 1
    check("of those, non-distributive (af28's T8 says 5)", nd, 5)

    # ---- guards ----------------------------------------------------------
    try:
        mk(3, [(0, 1), (1, 2), (2, 0)])
        raised = False
    except AssertionError:
        raised = True
    check("mk rejects a cycle", raised, True)

    from r3_rescope import drop_ligatures
    check("the ligature-dropping reader renders 'finite' as 'nite'",
          drop_ligatures("finite"), "nite")
    check("... and 'different' as 'dierent'",
          drop_ligatures("different"), "dierent")

    print(file=OUT)
    print("=" * 78, file=OUT)
    print("SELF-TEST: %d assertions, %d failed" % (N[0], len(FAILS)), file=OUT)
    print("=" * 78, file=OUT)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
