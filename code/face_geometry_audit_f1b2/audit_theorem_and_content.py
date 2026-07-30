"""mg-f1b2 -- part 3.

(1) THE THEOREM HALF, rebuilt independently.  mg-8a12's [CANNOT FAIL] row leans on
    mg-fcf1's sweep of "every eligible ridge choice (1449/981/1459 for I1/I2/I3)".
    Rebuilt here from the boundary matrix directly, without calling
    top_laplacians' mutation branches at all, so the theorem is checked against a
    second implementation of the corruption rather than against the one it
    describes.

(2) WHAT THE CAUSATION HALF ACTUALLY CONSTRAINS.  mg-8a12 puts
    `caused == app` in the scored condition of I1/I2/I3 in place of the
    absorbability answer it removed, and says of it: "What now stands scored is
    the half that can fail".  Two questions:
      (a) pred = twist(delta) and obs = twist(L_mut) - target, so pred == obs iff
          twist(L_true) == target (CLAIM (1), a proven theorem and also the new
          baseline row) AND L_mut - L_true == delta.  Is the second conjunct an
          identity, or does it have content?
      (b) does it catch a mutation that is NOT the local edit it declares?
          Injected here: a ridge_drop that drops two ridges instead of one.
"""

import sys

sys.path.insert(0, "../face_geometry")

from face_complex import (                                     # noqa: E402
    boundary_matrix, down_laplacian_from_boundary, linear_extensions, perm_sign,
    top_laplacians, at_laplacian, mat_eq, absorbable_by_diagonal_twist,
)
from posets import all_posets                                  # noqa: E402


def true_build(P):
    td = top_laplacians(P)
    M, nr, nc = boundary_matrix(td["facets"], td["ridges"])
    return td, M, nr, nc


def lap(M, nr, nc, interior):
    return down_laplacian_from_boundary(M, nr, nc, allowed_rows=interior)


def part1(nmax=5):
    print("=" * 78)
    print("(1) THE THEOREM HALF over EVERY eligible ridge choice, rebuilt from the")
    print("    boundary matrix (no use of top_laplacians' mutation branches)")
    print("=" * 78)
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    tot = {"I1": [0, 0, 0], "I2": [0, 0, 0], "I3": [0, 0, 0]}
    for P in ps:
        td, M, nr, nc = true_build(P)
        rf = {r: sorted(M.get(r, {}).keys()) for r in range(nr)}
        interior = {r for r in range(nr) if len(rf[r]) == 2}
        free = {r for r in range(nr) if len(rf[r]) == 1}
        L_true = lap(M, nr, nc, interior)
        for tag, elig in (("I1", interior), ("I2", free), ("I3", interior)):
            for r in sorted(elig):
                M2 = {k: dict(v) for k, v in M.items()}
                inter2 = set(interior)
                if tag == "I1":
                    j1, j2 = rf[r]
                    j3 = next((j for j in range(nc) if j not in (j1, j2)), None)
                    if j3 is None:
                        continue
                    M2[r][j3] = M2[r].pop(j2)
                elif tag == "I2":
                    inter2 = interior | {r}
                else:
                    del M2[r]
                    inter2 = interior - {r}
                L_mut = lap(M2, nr, nc, inter2)
                if mat_eq(L_mut, L_true):
                    continue
                tot[tag][0] += 1
                if any(L_mut[i][i] != L_true[i][i] for i in range(nc)):
                    tot[tag][1] += 1
                if absorbable_by_diagonal_twist(L_mut, L_true):
                    tot[tag][2] += 1
    for tag in ("I1", "I2", "I3"):
        a, d, ab = tot[tag]
        print("  %s: %4d eligible ridge choices that bite; diagonal MOVES on %d of "
              "them; reported absorbable on %d" % (tag, a, d, ab))
    print("  mg-fcf1 reported 1449/981/1459 for I1/I2/I3, quoted by mg-8a12's "
          "[CANNOT FAIL] row.")


def part2a(nmax=5):
    print()
    print("=" * 78)
    print("(2a) IS `L_mut - L_true == predicted delta` AN IDENTITY?")
    print("=" * 78)
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    for tag, mode in (("I1", "ridge_facets"), ("I2", "split_free_as_interior"),
                      ("I3", "ridge_drop")):
        ok = app = 0
        for P in ps:
            td, M, nr, nc = true_build(P)
            rf = {r: sorted(M.get(r, {}).keys()) for r in range(nr)}
            interior = {r for r in range(nr) if len(rf[r]) == 2}
            L_true = lap(M, nr, nc, interior)
            L_mut = top_laplacians(P, incidence_mode=mode)["L_rel"]
            if mat_eq(L_mut, L_true):
                continue
            app += 1
            r = top_laplacians(P, incidence_mode=mode)["mutated_ridge"]
            row = M.get(r, {})

            def outer(vec, sgn=1):
                D = [[0] * nc for _ in range(nc)]
                for a, va in vec.items():
                    for b, vb in vec.items():
                        D[a][b] += sgn * va * vb
                return D
            if mode == "split_free_as_interior":
                d = outer(row)
            elif mode == "ridge_drop":
                d = outer(row, -1)
            else:
                j1, j2 = sorted(row.keys())
                j3 = next(j for j in range(nc) if j not in (j1, j2))
                g, l = outer({j1: row[j1], j3: row[j2]}), outer(row, -1)
                d = [[g[i][j] + l[i][j] for j in range(nc)] for i in range(nc)]
            ok += mat_eq([[L_mut[i][j] - L_true[i][j] for j in range(nc)]
                          for i in range(nc)], d)
        print("  %s: identity holds on %d/%d biting posets, UNTWISTED -- so the "
              "twisted comparison mg-8a12 scores adds exactly one further "
              "requirement: twist(L_true) == target, i.e. CLAIM (1)." % (tag, ok, app))


def part2b(nmax=5):
    print()
    print("=" * 78)
    print("(2b) DOES THE CAUSATION HALF CATCH A MUTATION THAT IS NOT THE LOCAL EDIT")
    print("     IT DECLARES?  Injected: ridge_drop drops TWO interior ridges.")
    print("=" * 78)
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    app = caused = absorb = diag_mv = 0
    for P in ps:
        td, M, nr, nc = true_build(P)
        rf = {r: sorted(M.get(r, {}).keys()) for r in range(nr)}
        interior = sorted(r for r in range(nr) if len(rf[r]) == 2)
        if len(interior) < 2:
            continue
        L_true = lap(M, nr, nc, set(interior))
        M2 = {k: dict(v) for k, v in M.items()}
        del M2[interior[0]], M2[interior[1]]
        inter2 = set(interior) - {interior[0], interior[1]}
        L_mut = lap(M2, nr, nc, inter2)
        if mat_eq(L_mut, L_true):
            continue
        app += 1
        s = [perm_sign(w) for w in td["les"]]
        target = at_laplacian(P)[1]
        row = M.get(interior[0], {})
        d = [[0] * nc for _ in range(nc)]
        for a, va in row.items():
            for b, vb in row.items():
                d[a][b] -= va * vb
        pred = [[s[i] * d[i][j] * s[j] for j in range(nc)] for i in range(nc)]
        obs = [[L_mut[i][j] * s[i] * s[j] - target[i][j] for j in range(nc)]
               for i in range(nc)]
        caused += mat_eq(pred, obs)
        tw = [[s[i] * L_mut[i][j] * s[j] for j in range(nc)] for i in range(nc)]
        absorb += absorbable_by_diagonal_twist(tw, target)
        diag_mv += any(tw[i][i] != target[i][i] for i in range(nc))
    print("  a two-ridge drop declared as a one-ridge drop: bites on %d posets" % app)
    print("  the ABSORBABILITY half mg-8a12 removed  would score: absorbable on "
          "%d/%d, diagonal moves on %d/%d  ->  row still GREEN" % (absorb, app, diag_mv, app))
    print("  the CAUSATION half mg-8a12 added        would score: residual == "
          "prediction on %d/%d  ->  row RED" % (caused, app))
    print("  So the causation half has content the absorbability half did not: it "
          "constrains the mutation to be\n  the edit it declares.  It is not a "
          "tautology.  What it does not do is make the row able to fail on a\n  "
          "defect in the CONSTRUCTION the section exists to test -- for that, see "
          "part 4.")


if __name__ == "__main__":
    part1()
    part2a()
    part2b()
