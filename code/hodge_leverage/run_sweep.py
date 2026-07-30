"""Sweep: the link-based (local-to-global) bound against the truth, all posets
n <= 6, plus three infinite families pushed further.

Output is committed at `sweep_output.txt`.  Everything here is re-derivable by
`bash run_all.sh`.
"""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry"))

from face_complex import Poset, linear_extensions
from posets import all_posets, cover_string
from links import faces_of, facets_of
from local_to_global import lg_bound, at_lambda2, gammas

MAXN = int(os.environ.get("HL_MAXN", "6"))


def row(P, tag=""):
    facets = facets_of(P)
    faces = faces_of(P)
    b, g = lg_bound(P, facets, faces)
    t = at_lambda2(P)
    nL = len(facets)
    gs = ",".join("%.4f" % g[i][0] for i in sorted(g)) if g else "-"
    ratio = (t / b) if (t is not None and b > 0) else None
    return {
        "n": P.n, "nL": nL, "bound": b, "truth": t, "ratio": ratio,
        "gammas": gs, "maxgamma": max((g[i][0] for i in g), default=None),
        "tag": tag or cover_string(P),
    }


def main():
    print("=" * 78)
    print("A. FULL POPULATION: every poset up to isomorphism, n <= %d" % MAXN)
    print("=" * 78)
    print("bound = the (LG) link-based lower bound on lambda_2(Delta_AT)")
    print("     = 2 * prod_{i=-1}^{n-4} (1 - gamma_i)")
    print("truth = lambda_2(Delta_AT) by Lanczos on the shifted operator")
    print()
    allrows = []
    for n in range(2, MAXN + 1):
        t0 = time.time()
        rows = []
        for P in all_posets(n):
            r = row(P)
            rows.append(r)
            allrows.append(r)
        viol = [r for r in rows if r["truth"] is not None
                and r["truth"] < r["bound"] - 1e-9]
        live = [r for r in rows if r["ratio"] is not None]
        maxg = max((r["maxgamma"] for r in rows if r["maxgamma"] is not None),
                   default=None)
        print("n=%d  posets=%3d   (LG) violations=%d   max gamma over all levels"
              " and all posets=%s" % (n, len(rows), len(viol),
                                      ("%.6f" % maxg) if maxg is not None else "-"))
        if live:
            rs = sorted(r["ratio"] for r in live)
            print("      truth/bound over the %d posets with |L(P)|>=2:"
                  "  min=%.4f  median=%.4f  max=%.4f" %
                  (len(live), rs[0], rs[len(rs) // 2], rs[-1]))
        print("      [%.1fs]" % (time.time() - t0))
        if viol:
            for r in viol[:5]:
                print("      VIOLATION", r)
    print()
    print("gamma_i is bounded by 1/2 on the whole population:",
          all((r["maxgamma"] is None or r["maxgamma"] <= 0.5 + 1e-9)
              for r in allrows))
    eq = [r for r in allrows if r["maxgamma"] is not None
          and abs(r["maxgamma"] - 0.5) < 1e-9]
    print("posets attaining gamma_i = 1/2 at some level: %d of %d"
          % (len(eq), len(allrows)))
    w3 = [r for r in allrows if r["maxgamma"] is not None
          and r["maxgamma"] < 0.5 - 1e-9]
    print("posets with every gamma_i < 1/2: %d  (tags: %s)"
          % (len(w3), "; ".join(r["tag"] for r in w3[:12])))
    print()

    print("=" * 78)
    print("B. THE ANTICHAIN FAMILY -- the bound decays geometrically, the truth")
    print("   polynomially.  truth from Aldous/Caputo-Liggett-Richthammer:")
    print("   lambda_2(Delta_AT(A_n)) = 2 - 2 cos(pi/n)  (verified vs Lanczos)")
    print("=" * 78)
    print("  n   gamma_i (all levels)                bound      truth      ratio")
    for n in range(2, min(MAXN, 6) + 1):
        P = Poset(n, [])
        b, g = lg_bound(P)
        t = at_lambda2(P)
        exact = 2 - 2 * math.cos(math.pi / n)
        assert t is None or abs(t - exact) < 1e-7, (n, t, exact)
        print("  %2d  %-34s %.6f   %.6f   %6.2f"
              % (n, ",".join("%.3f" % g[i][0] for i in sorted(g)) or "-",
                 b, exact, exact / b))
    print("  ... extrapolating gamma_i = 1/2 at every level (observed n<=6,")
    print("      and proved for the top level: the braid hexagon):")
    for n in (8, 12, 20, 40):
        b = 2.0 * 0.5 ** (n - 2)
        exact = 2 - 2 * math.cos(math.pi / n)
        print("  %2d  (1/2 at all %2d levels)%14s %.3e   %.6f   %8.1f"
              % (n, n - 2, "", b, exact, exact / b))
    print()

    print("=" * 78)
    print("C. TWO WIDTH-2 FAMILIES -- no 3-antichain, so no braid hexagon.")
    print("   Does removing the hexagon make the bound competitive?")
    print("=" * 78)
    for name, mk in (("C_a + C_a (two chains)", lambda a: Poset(
                          2 * a, [(i, j) for i in range(a) for j in range(i + 1, a)]
                          + [(a + i, a + j) for i in range(a)
                             for j in range(i + 1, a)])),
                     ("zigzag (fence) N_n", lambda a: None)):
        if mk(1) is None:
            continue
        print("  %s" % name)
        print("    n   |L(P)|   gamma_i                       bound      truth     ratio")
        for a in range(1, 5):
            P = mk(a)
            if P.n > 8:
                break
            b, g = lg_bound(P)
            t = at_lambda2(P)
            print("   %2d   %6d   %-28s %.6f   %.6f   %6.2f"
                  % (P.n, len(linear_extensions(P)),
                     ",".join("%.3f" % g[i][0] for i in sorted(g)) or "-",
                     b, t, t / b))
    print()
    print("  fences (zigzag: 0<1>2<3>4...) -- width 2 for n<=3, wider above")
    print("    n   |L(P)|   gamma_i                       bound      truth     ratio")
    for n in range(3, 8):
        rel = []
        for i in range(n - 1):
            rel.append((i, i + 1) if i % 2 == 0 else (i + 1, i))
        P = Poset(n, rel)
        b, g = lg_bound(P)
        t = at_lambda2(P)
        print("   %2d   %6d   %-28s %.6f   %.6f   %6.2f"
              % (P.n, len(linear_extensions(P)),
                 ",".join("%.3f" % g[i][0] for i in sorted(g)) or "-",
                 b, t, t / b))


if __name__ == "__main__":
    main()
