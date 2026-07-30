"""Controls for the mg-276d probe.

Two kinds, and both are required before any result from `run_probe.py` may be
believed:

  POSITIVE controls -- the machinery reproduces answers that are known
  independently of this program (Betti numbers of standard complexes, the
  A000112 poset counts, the two independent enumerations of Sur_iso agreeing).

  NEGATIVE controls -- the *identity test used by the probe* is shown to RETURN
  FALSE on deliberately corrupted inputs whose answer is known to be "not
  equal".  A control that cannot fail is not a control.  Each mutation below is
  a specific, named way of getting the construction wrong; the control passes
  only if the test rejects it, and the report states on how many posets each
  mutation was rejected.

Run:  python3 controls.py
"""

import sys

from face_complex import (
    Poset, boundary_matrix, chains_of_ideals, face_from_sur_iso, sur_iso,
    linear_extensions, le_to_facet, facet_to_le, top_laplacians, at_laplacian,
    coxeter_compression, twist, mat_eq, mat_sub, is_diagonal, reduced_betti,
    rank_mod_p, rank_exact, adjacent_transposition_graph, perm_sign,
)
from posets import all_posets, POSET_COUNTS, cover_string

FAIL = []


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print("  [%s] %s%s" % (status, name, ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)
    return ok


# --------------------------------------------------------------------------
# POSITIVE CONTROL 1 -- homology of standard complexes
# --------------------------------------------------------------------------

def complex_from_facets(facets):
    """Build the full face dict (including the empty face) from a facet list.
    Vertices are given a fixed total order by their sort order."""
    faces = {-1: [()]}
    allf = set()
    for f in facets:
        f = tuple(sorted(f))
        for k in range(1, len(f) + 1):
            from itertools import combinations
            for c in combinations(f, k):
                allf.add(c)
    for c in allf:
        faces.setdefault(len(c) - 1, []).append(c)
    for d in faces:
        faces[d].sort()
    return faces


def positive_control_homology():
    print("POSITIVE CONTROL 1 -- reduced Betti numbers of standard complexes")
    cases = [
        ("boundary of a triangle = S^1", [(0, 1), (1, 2), (0, 2)], {0: 0, 1: 1}),
        ("filled triangle = disc (contractible)", [(0, 1, 2)], {0: 0, 1: 0, 2: 0}),
        ("boundary of the octahedron = S^2",
         [(0, 2, 4), (0, 2, 5), (0, 3, 4), (0, 3, 5),
          (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5)],
         {0: 0, 1: 0, 2: 1}),
        ("two disjoint edges (b0 = 1 reduced)", [(0, 1), (2, 3)], {0: 1, 1: 0}),
        ("wedge of two circles", [(0, 1), (1, 2), (0, 2), (0, 3), (3, 4), (0, 4)],
         {0: 0, 1: 2}),
    ]
    for name, facets, expected in cases:
        faces = complex_from_facets(facets)
        b = reduced_betti(faces, use_exact=True)
        got = {d: b.get(d, 0) for d in expected}
        check("%s -> reduced betti %s" % (name, got), got == expected,
              "expected %s" % expected)


# --------------------------------------------------------------------------
# NEGATIVE CONTROL 1 -- the homology code is sign-sensitive and can fail
# --------------------------------------------------------------------------

def negative_control_signs():
    print("NEGATIVE CONTROL 1 -- corrupt the simplicial signs; homology must break")
    faces = complex_from_facets([(0, 1), (1, 2), (0, 2)])   # S^1, b1 = 1

    def bad_boundary(faces_d, faces_dm1):
        row_idx = {f: i for i, f in enumerate(faces_dm1)}
        M = {}
        for j, f in enumerate(faces_d):
            for i in range(len(f)):
                g = f[:i] + f[i + 1:]
                r = row_idx[g]
                M.setdefault(r, {})
                M[r][j] = M[r].get(j, 0) + 1        # <-- all +1, no alternation
        return M, len(faces_dm1), len(faces_d)

    rk = {}
    for d in (0, 1):
        M, nr, nc = bad_boundary(faces[d], faces[d - 1])
        rk[d] = rank_exact(M, nr, nc)
    rk[2] = 0
    b = {d: len(faces[d]) - rk[d] - rk[d + 1] for d in (0, 1)}
    check("all-+1 boundary gives WRONG betti for S^1: got %s, truth {0: 0, 1: 1}" % b,
          b != {0: 0, 1: 1},
          "the control fires -- the homology code is not sign-blind")


# --------------------------------------------------------------------------
# POSITIVE CONTROL 2 -- poset enumeration counts (OEIS A000112)
# --------------------------------------------------------------------------

def positive_control_poset_counts(nmax):
    print("POSITIVE CONTROL 2 -- poset counts up to isomorphism (A000112)")
    for n in range(1, nmax + 1):
        ps = all_posets(n)
        check("n=%d: %d posets" % (n, len(ps)), len(ps) == POSET_COUNTS[n],
              "expected %d" % POSET_COUNTS[n])


# --------------------------------------------------------------------------
# POSITIVE CONTROL 3 -- two independent constructions of F(P) agree
# --------------------------------------------------------------------------

def positive_control_face_complex(nmax):
    print("POSITIVE CONTROL 3 -- Sur_iso(P,[k]) (brute force) == chains of proper "
          "ideals, and d.d = 0, and facets == L(P), and every ridge is in 1 or 2 facets")
    ok_sur = ok_dd = ok_fac = ok_pm = True
    tested = 0
    for n in range(1, nmax + 1):
        for P in all_posets(n):
            tested += 1
            faces = chains_of_ideals(P)
            # (a) surjective isotone maps <-> chains, degree by degree
            for k in range(1, n + 1):
                brute = sur_iso(P, k)
                viachain = faces.get(k - 2, [])
                imgs = sorted(face_from_sur_iso(P, f) for f in brute)
                if imgs != sorted(viachain) or len(set(imgs)) != len(brute):
                    ok_sur = False
            # (b) d.d = 0
            dims = sorted(d for d in faces if d >= 0)
            for d in dims:
                if d - 1 < 0:
                    continue
                M1, nr1, nc1 = boundary_matrix(faces[d], faces[d - 1])
                M2, nr2, nc2 = boundary_matrix(faces[d - 1], faces[d - 2])
                # compose
                comp = {}
                for r, row in M2.items():
                    for (c, v) in row.items():
                        for r2, row2 in M1.items():
                            if r2 == c:
                                for (c2, v2) in row2.items():
                                    comp[(r, c2)] = comp.get((r, c2), 0) + v * v2
                if any(v != 0 for v in comp.values()):
                    ok_dd = False
            # (c) facets are exactly the linear extensions
            les = linear_extensions(P)
            top = faces.get(n - 2, [])
            if sorted(le_to_facet(w) for w in les) != sorted(top):
                ok_fac = False
            if any(facet_to_le(f, n) not in set(les) for f in top):
                ok_fac = False
            # (d) pseudomanifold-with-boundary: every ridge in 1 or 2 facets
            td = top_laplacians(P)
            if any(len(v) not in (1, 2) for v in td["ridge_facets"].values()):
                ok_pm = False
    check("Sur_iso == chains of proper ideals (all posets n<=%d)" % nmax, ok_sur)
    check("boundary^2 = 0 (all posets n<=%d)" % nmax, ok_dd)
    check("facets of F(P) == L(P) (all posets n<=%d)" % nmax, ok_fac)
    check("every ridge lies in exactly 1 or 2 facets (all posets n<=%d)" % nmax, ok_pm,
          "%d posets tested" % tested)


# --------------------------------------------------------------------------
# POSITIVE CONTROL 4 -- homology of F(P) against a known theorem
# --------------------------------------------------------------------------

def positive_control_FP_homology(nmax):
    print("POSITIVE CONTROL 4 -- reduced homology of F(P) = order complex of the "
          "proper part of J(P): S^{n-2} iff P is an antichain, otherwise acyclic")
    ok = True
    detail = []
    for n in range(2, nmax + 1):
        for P in all_posets(n):
            faces = chains_of_ideals(P)
            b = reduced_betti(faces, use_exact=True)
            nz = {d: v for d, v in b.items() if v}
            expect = {n - 2: 1} if P.is_antichain() else {}
            if nz != expect:
                ok = False
                detail.append("n=%d %s: got %s expected %s"
                              % (n, cover_string(P), nz, expect))
    check("reduced homology of F(P) matches the known answer (n<=%d)" % nmax, ok,
          "; ".join(detail[:3]))


# --------------------------------------------------------------------------
# THE IDENTITY TEST (this is the object the probe uses)
# --------------------------------------------------------------------------

def claim1_pair(P, use_twist=True, use_relative=True, sign_fn=perm_sign,
                perturb_edge=False, normalise=False, sign_mode="true"):
    """Return the pair (LHS, RHS) that claim (1) asserts to be equal:

        LHS = E . L^rel_top . E        (E = diag(sgn w), the orientation twist)
        RHS = D - A                    (the adjacent-transposition Laplacian)

    All the knobs exist so the negative controls can corrupt one ingredient at
    a time; the probe itself always runs with the defaults.

    `sign_mode` corrupts the CONSTRUCTION of L^rel from the complex (the
    simplicial signs of the boundary matrix); every other knob corrupts the
    comparison or the target.  See NEGATIVE CONTROL 3.
    """
    td = top_laplacians(P, sign_mode=sign_mode)
    les = td["les"]
    L = td["L_rel"] if use_relative else td["L_abs"]
    if use_twist:
        s = [sign_fn(w) for w in les]
        L = [[s[i] * L[i][j] * s[j] for j in range(len(les))] for i in range(len(les))]
    _, target = at_laplacian(P)
    if perturb_edge:
        m = len(les)
        done = False
        target = [row[:] for row in target]
        for i in range(m):
            for j in range(m):
                if i != j and target[i][j] != 0:
                    target[i][j] = 0
                    target[j][i] = 0
                    done = True
                    break
            if done:
                break
    if normalise:
        target = [[t * 2 for t in row] for row in target]
    return L, target


def claim1_test(P, **kw):
    L, target = claim1_pair(P, **kw)
    return mat_eq(L, target)


def claim2_test(P, use_twist=True):
    td = top_laplacians(P)
    les = td["les"]
    L = td["L_abs"]
    if use_twist:
        s = [perm_sign(w) for w in les]
        L = [[s[i] * L[i][j] * s[j] for j in range(len(les))] for i in range(len(les))]
    _, target = coxeter_compression(P)
    return mat_eq(L, target)


def claim3_test(P):
    """Claim (3), at the level of the Laplacians: L^abs - L^rel is diagonal and
    its (w,w) entry is the number of FORBIDDEN adjacent transpositions at w."""
    td = top_laplacians(P)
    les = td["les"]
    D = mat_sub(td["L_abs"], td["L_rel"])
    if not is_diagonal(D):
        return False
    _, A, deg = adjacent_transposition_graph(P)
    return all(D[i][i] == (P.n - 1) - deg[i] for i in range(len(les)))


def claim3_bijection_test(P):
    """Claim (3), at the level of the complex, which is the stronger reading:
    for each linear extension w, the FREE ridges of the facet of w correspond
    bijectively to the positions i where s_i is forbidden at w."""
    td = top_laplacians(P)
    les, facets = td["les"], td["facets"]
    ridge_index = {r: i for i, r in enumerate(td["ridges"])}
    for wi, w in enumerate(les):
        f = facets[wi]
        free_positions = set()
        for i in range(len(f)):
            r = f[:i] + f[i + 1:]
            if len(td["ridge_facets"][ridge_index[r]]) == 1:
                free_positions.add(i)      # ridge obtained by deleting the i-th ideal
        forbidden = set()
        for t in range(P.n - 1):
            if P.comparable(w[t], w[t + 1]):
                forbidden.add(t)
        # deleting the i-th ideal of the chain (0-indexed) unlocks positions i,i+1
        # of the word, i.e. corresponds to generator s_{i+1} = position index i
        if free_positions != forbidden:
            return False
    return True


def negative_control_identity(nmax):
    """Show the identity test REJECTS each named corruption, and say on how many.

    APPLICABILITY IS COMPUTED, NOT ASSERTED.  A mutation is counted only on
    posets where it actually changes one of the two matrices being compared;
    on the rest it is not a mutation at all and demanding rejection there would
    be demanding a false negative.  The count of skipped posets is reported, so
    the reader can see how much of the population each mutation reached.

    (Worked example of why this matters: M3 replaces the sign twist by "-1 on
    one facet, +1 elsewhere".  When |L(P)| = 2 there is exactly one edge and
    both sign patterns give the product -1 across it, so the mutated matrix
    equals the correct one -- the mutation is vacuous, not undetected.)
    """
    print("NEGATIVE CONTROL 2 -- the claim-(1) test must FAIL on corrupted inputs")
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    tally, applicable, skipped, vac_sizes = {}, {}, {}, {}
    M1 = "M1 no sign twist (L^rel compared to D-A directly)"
    M2 = "M2 absolute Laplacian in place of the relative one"
    M3 = "M3 wrong twist (sgn replaced by -1 on one facet, +1 elsewhere)"
    M4 = "M4 target Laplacian scaled by 2"
    M5 = "M5 one edge deleted from the target graph"
    for P in ps:
        first = linear_extensions(P)[0]
        truth = claim1_pair(P)
        muts = [
            (M1, lambda P=P: claim1_pair(P, use_twist=False)),
            (M2, lambda P=P: claim1_pair(P, use_relative=False)),
            (M3, lambda P=P, f=first: claim1_pair(
                P, sign_fn=lambda w, f=f: (-1 if w == f else 1))),
            (M4, lambda P=P: claim1_pair(P, normalise=True)),
            (M5, lambda P=P: claim1_pair(P, perturb_edge=True)),
        ]
        for name, fn in muts:
            mut = fn()
            if mat_eq(mut[0], truth[0]) and mat_eq(mut[1], truth[1]):
                skipped[name] = skipped.get(name, 0) + 1   # vacuous here
                vac_sizes.setdefault(name, set()).add(len(linear_extensions(P)))
                continue
            applicable[name] = applicable.get(name, 0) + 1
            if not mat_eq(mut[0], mut[1]):
                tally[name] = tally.get(name, 0) + 1
    for name in sorted(applicable):
        n_app = applicable[name]
        n_rej = tally.get(name, 0)
        check("%s -- rejected on %d/%d posets where the mutation bites "
              "(%d vacuous, on |L(P)| in %s)"
              % (name, n_rej, n_app, skipped.get(name, 0),
                 sorted(vac_sizes.get(name, set()))),
              n_rej == n_app)
    # And the uncorrupted test must PASS on those same posets.
    n_pass = sum(1 for P in ps if claim1_test(P) is True)
    check("uncorrupted claim-(1) test passes on %d/%d posets" % (n_pass, len(ps)),
          n_pass == len(ps))


def negative_control_construction(nmax):
    """NEGATIVE CONTROL 3 -- corrupt the CONSTRUCTION of the Laplacian.

    Adopted from the mg-e0ce independent audit (finding F2, `audit_extra.py`
    X3).  Of the five mutations in NEGATIVE CONTROL 2, M1 and M3 corrupt the
    twist, M4 and M5 corrupt the target, and only M2 touches the construction
    at all (it swaps which of the two Laplacians is built from the complex).
    NONE of them perturbs the boundary matrix that both are built from -- and
    NEGATIVE CONTROL 1, which looks as though it does, runs on the homology
    path and never reaches top_laplacians.  This control closes that gap.

    Two sign corruptions are run, and the difference between them is the point:

      all-+1 signs  do NOT change either top Laplacian, so this corruption
                    CANNOT fire here.  Reported, not hidden: it is why
                    NEGATIVE CONTROL 1 was never a construction-side control.
                    (The alternating sign is load-bearing for the homology of
                    F(P), where NEGATIVE CONTROL 1 does fire -- just not for
                    claims (1)-(3).)

      facet-parity  flips the sign of every incidence of the odd-indexed
                    facets.  This does change the off-diagonal part, and the
                    identity test must reject it.

    The true-sign build passes throughout: the instrument was never wrong, the
    argument for trusting it was missing this control.
    """
    print("NEGATIVE CONTROL 3 -- corrupt the CONSTRUCTION of L^rel (mg-e0ce F2)")
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    bites = [P for P in ps if len(linear_extensions(P)) >= 2]
    n_true = sum(1 for P in ps if claim1_test(P, sign_mode="true") is True)
    check("true simplicial signs: claim (1) holds on %d/%d posets" % (n_true, len(ps)),
          n_true == len(ps))

    plus_same = sum(1 for P in ps
                    if mat_eq(claim1_pair(P, sign_mode="allplus")[0],
                              claim1_pair(P)[0]))
    plus_pass = sum(1 for P in ps if claim1_test(P, sign_mode="allplus") is True)
    check("all-+1 signs leave both top Laplacians UNCHANGED on %d/%d posets, so "
          "claim (1) still holds on %d -- this corruption cannot fire on the "
          "construction (reported, not a pass)" % (plus_same, len(ps), plus_pass),
          plus_same == len(ps) and plus_pass == len(ps))

    par_app = [P for P in bites
               if not mat_eq(claim1_pair(P, sign_mode="parity")[0],
                             claim1_pair(P)[0])]
    par_rej = sum(1 for P in par_app if not claim1_test(P, sign_mode="parity"))
    check("facet-parity signs -- rejected on %d/%d posets with |L(P)| >= 2 where "
          "the mutation bites (%d posets have |L(P)| = 1: a single facet, no "
          "second column to flip against)"
          % (par_rej, len(par_app), len(ps) - len(bites)),
          par_rej == len(par_app) and len(par_app) == len(bites))


def main():
    nmax_cheap = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    positive_control_homology()
    negative_control_signs()
    positive_control_poset_counts(nmax_cheap)
    positive_control_face_complex(min(nmax_cheap, 4))
    positive_control_FP_homology(min(nmax_cheap, 5))
    negative_control_identity(min(nmax_cheap, 5))
    negative_control_construction(min(nmax_cheap, 5))
    print()
    if FAIL:
        print("CONTROLS FAILED: %d" % len(FAIL))
        for f in FAIL:
            print("   - " + f)
        sys.exit(1)
    print("ALL CONTROLS PASS")


if __name__ == "__main__":
    main()
