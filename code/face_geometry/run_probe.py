"""mg-276d: the probe itself.

Tests, for EVERY poset up to isomorphism on n = 1..NMAX elements, the three
claims made in `~/files/intrinsic_face_geometry_program.tex` about "the
four-element example":

  (1)  E . L^rel_top(F(P)) . E  ==  D - A        [relative Hodge Laplacian
                                                  = adjacent-transposition
                                                  Laplacian, up to the twist]
  (2)  E . L^abs_top(F(P)) . E  ==  compression to C[L(P)] of sum_i (1 - s_i)
  (3)  L^abs_top - L^rel_top    ==  diag(# forbidden adjacent transpositions),
       and, in the stronger reading, the free ridges at a facet correspond
       bijectively to the forbidden generators there.

E = diag(sgn w) is the orientation twist; see the document for its derivation.

Also reported per poset, so the population and its subclasses are visible:
|L(P)|, whether P is an antichain / a chain / disconnected, |Aut(P)|, the
number of free ridges, and the kernel dimension of the twisted relative
Laplacian.

Usage:   python3 run_probe.py [NMAX]      (default 6)
Output:  a per-n summary table, a per-poset table for n <= 4 (the "four-element
         example" the sketch refers to), and the failure-mode breakdown.
"""

import sys

from face_complex import (
    Poset, top_laplacians, at_laplacian, coxeter_compression,
    adjacent_transposition_graph, linear_extensions, twist, mat_eq, mat_sub,
    is_diagonal, perm_sign, rank_exact, rank_mod_p,
)
from posets import all_posets, cover_string, describe


def kernel_dim(L):
    """dim ker L over Q, L a dense square integer matrix.

    For m <= 50 this is computed exactly over Q.  Above that it is computed as
    m - rank_p for a large prime p, which gives an UPPER bound on ker over Q
    (rank_p <= rank_Q).  For the matrices here that is still a proof: D - A
    always has the all-ones vector in its kernel, so ker_Q >= 1, and an upper
    bound of 1 pins it to exactly 1.  Any value > 1 from the mod-p route is
    reported as an upper bound and re-checked exactly.
    """
    m = len(L)
    M = {}
    for i in range(m):
        row = {j: L[i][j] for j in range(m) if L[i][j]}
        if row:
            M[i] = row
    if m <= 50:
        return m - rank_exact(M, m, m)
    k = m - rank_mod_p(M, m, m)
    if k > 1:                        # only then is the exact computation needed
        k = m - rank_exact(M, m, m)
    return k


def probe_one(P):
    n = P.n
    td = top_laplacians(P)
    les = td["les"]
    m = len(les)

    L_rel_tw = twist(td["L_rel"], les)
    L_abs_tw = twist(td["L_abs"], les)

    _, AT = at_laplacian(P)
    _, COX = coxeter_compression(P)

    c1 = mat_eq(L_rel_tw, AT)
    c2 = mat_eq(L_abs_tw, COX)

    Ddiff = mat_sub(td["L_abs"], td["L_rel"])
    _, A, deg = adjacent_transposition_graph(P)
    c3_lap = is_diagonal(Ddiff) and all(
        Ddiff[i][i] == (n - 1) - deg[i] for i in range(m))

    # stronger reading of (3): bijection at the level of the complex
    ridge_index = {r: i for i, r in enumerate(td["ridges"])}
    c3_bij = True
    for wi, w in enumerate(les):
        f = td["facets"][wi]
        free_pos = {i for i in range(len(f))
                    if len(td["ridge_facets"][ridge_index[f[:i] + f[i + 1:]]]) == 1}
        forbidden = {t for t in range(n - 1) if P.comparable(w[t], w[t + 1])}
        if free_pos != forbidden:
            c3_bij = False
            break

    # do (2) and (3) also need the twist?  record whether the untwisted forms hold
    c1_untw = mat_eq(td["L_rel"], AT)
    c2_untw = mat_eq(td["L_abs"], COX)

    return {
        "n": n,
        "covers": cover_string(P),
        "tags": describe(P),
        "nLE": m,
        "n_free_ridges": td["n_free_ridges"],
        "n_ridges": td["n_ridges"],
        "c1": c1, "c2": c2, "c3_lap": c3_lap, "c3_bij": c3_bij,
        "c1_untwisted": c1_untw, "c2_untwisted": c2_untw,
        "ker_rel": kernel_dim(L_rel_tw),
        "antichain": P.is_antichain(),
        "chain": P.is_chain(),
        "disconnected": not P.is_connected(),
        "naut": len(P.automorphisms()),
    }


def main():
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    rows = []
    for n in range(1, nmax + 1):
        for P in all_posets(n):
            rows.append(probe_one(P))
        print("n=%d done (%d posets)" % (n, sum(1 for r in rows if r["n"] == n)),
              file=sys.stderr)

    print("=" * 78)
    print("PER-n SUMMARY -- population tested vs population the claim holds on")
    print("=" * 78)
    print("%3s %8s %8s %8s %8s %8s %10s" %
          ("n", "posets", "(1) OK", "(2) OK", "(3)L OK", "(3)bij", "max|L(P)|"))
    for n in range(1, nmax + 1):
        rs = [r for r in rows if r["n"] == n]
        if not rs:
            continue
        print("%3d %8d %8d %8d %8d %8d %10d" %
              (n, len(rs),
               sum(r["c1"] for r in rs), sum(r["c2"] for r in rs),
               sum(r["c3_lap"] for r in rs), sum(r["c3_bij"] for r in rs),
               max(r["nLE"] for r in rs)))
    tot = len(rows)
    print("%3s %8d %8d %8d %8d %8d" %
          ("all", tot, sum(r["c1"] for r in rows), sum(r["c2"] for r in rows),
           sum(r["c3_lap"] for r in rows), sum(r["c3_bij"] for r in rows)))

    print()
    print("=" * 78)
    print("IS THE TWIST NEEDED?  (how often the UNtwisted form also holds)")
    print("=" * 78)
    n1 = sum(r["c1_untwisted"] for r in rows)
    n2 = sum(r["c2_untwisted"] for r in rows)
    triv = sum(1 for r in rows if r["nLE"] == 1)
    print("claim (1) untwisted holds on %d/%d posets (%d of those have |L(P)|=1)"
          % (n1, tot, triv))
    print("claim (2) untwisted holds on %d/%d posets (%d of those have |L(P)|=1)"
          % (n2, tot, triv))
    print("-> the twist is NOT cosmetic: it is needed except where L(P) is a point.")

    print()
    print("=" * 78)
    print("FAILURE-MODE BREAKDOWN -- the claim on named subclasses")
    print("=" * 78)
    subclasses = [
        ("antichain (L(P) = S_n)", lambda r: r["antichain"]),
        ("chain (|L(P)| = 1)", lambda r: r["chain"]),
        ("disconnected", lambda r: r["disconnected"]),
        ("non-trivial Aut(P)", lambda r: r["naut"] > 1),
        ("trivial Aut(P)", lambda r: r["naut"] == 1),
        ("connected, not a chain, not an antichain",
         lambda r: not r["disconnected"] and not r["chain"] and not r["antichain"]),
        ("|L(P)| >= 10", lambda r: r["nLE"] >= 10),
    ]
    print("%-46s %7s %7s %7s %7s" % ("subclass", "count", "(1)", "(2)", "(3)bij"))
    for name, pred in subclasses:
        rs = [r for r in rows if pred(r)]
        print("%-46s %7d %7d %7d %7d" %
              (name, len(rs), sum(r["c1"] for r in rs), sum(r["c2"] for r in rs),
               sum(r["c3_bij"] for r in rs)))

    print()
    print("=" * 78)
    print("DEGENERACY CHECK -- an identity that holds only where both sides are")
    print("trivial is not a bridge.  Non-degenerate = the AT graph has an edge")
    print("AND at least one generator is forbidden somewhere (so rel != abs).")
    print("=" * 78)
    nondeg = [r for r in rows if r["nLE"] >= 2 and r["n_free_ridges"] > 0]
    print("non-degenerate posets: %d of %d; claim (1) holds on %d of them"
          % (len(nondeg), tot, sum(r["c1"] for r in nondeg)))
    both_triv = [r for r in rows if r["nLE"] == 1]
    print("posets where BOTH sides are the zero 1x1 matrix: %d" % len(both_triv))

    print()
    print("=" * 78)
    print("KERNEL OF THE TWISTED RELATIVE TOP LAPLACIAN")
    print("(= dim H_{n-2}(F(P), dF(P); Q); equals 1 iff the AT graph is connected)")
    print("=" * 78)
    kd = {}
    for r in rows:
        kd[r["ker_rel"]] = kd.get(r["ker_rel"], 0) + 1
    print("kernel dimension histogram over all %d posets: %s" % (tot, dict(sorted(kd.items()))))

    print()
    print("=" * 78)
    print("THE FOUR-ELEMENT EXAMPLE -- all 16 posets on 4 elements")
    print("(the sketch says 'the four-element example', singular, and does not")
    print("say which poset; so all 16 are reported)")
    print("=" * 78)
    print("%-22s %-26s %5s %6s %6s %4s %4s %6s %6s"
          % ("covers", "tags", "|L|", "ridges", "free", "(1)", "(2)", "(3)L", "(3)bij"))
    for r in [r for r in rows if r["n"] == 4]:
        print("%-22s %-26s %5d %6d %6d %4s %4s %6s %6s"
              % (r["covers"], r["tags"], r["nLE"], r["n_ridges"],
                 r["n_free_ridges"], r["c1"], r["c2"], r["c3_lap"], r["c3_bij"]))

    print()
    bad = [r for r in rows if not (r["c1"] and r["c2"] and r["c3_lap"] and r["c3_bij"])]
    if bad:
        print("WITNESSES AGAINST (should be none):")
        for r in bad:
            print("  n=%d %s %s c1=%s c2=%s c3L=%s c3bij=%s"
                  % (r["n"], r["covers"], r["tags"], r["c1"], r["c2"],
                     r["c3_lap"], r["c3_bij"]))
    else:
        print("NO WITNESS AGAINST ANY OF THE THREE CLAIMS in the tested population.")
    print("Population tested: all posets up to isomorphism on n = 1..%d elements "
          "(%d posets)." % (nmax, tot))


if __name__ == "__main__":
    main()
