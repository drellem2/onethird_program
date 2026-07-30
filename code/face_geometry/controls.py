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

SCORING (mg-5630 section 2.6, landed by mg-1319).  "A control that cannot fail
is not a control" is enforced by the scoring, not merely stated here.  A row
whose corruption provably cannot change the object under test is scored
[CANNOT FAIL] -- never [PASS] -- and its presence makes the bottom line unable
to read ALL CONTROLS PASS.  That row is still checked: if the fact it reports
were false the run FAILS, because a broken theorem is a real failure.  The
defect this replaces: the row for all-+1 signs printed [PASS] under a battery
ending ALL CONTROLS PASS, while the mg-e0ce instrument scored the identical
fact as a FAIL row.  Neither is right; a tautology is a third thing.

AND ONE MORE QUESTION OF EVERY NEGATIVE CONTROL, added by mg-2789 after mg-5630:
IS THE CORRUPTION ABSORBABLE INTO A PARAMETER THE BATTERY ALREADY VARIES?  If
it is, the control varies a gauge and not the construction, however many posets
it rejects.  NEGATIVE CONTROL 3 is the worked example of failing this test -- its
facet-parity corruption equals diag((-1)^j) . L . diag((-1)^j), so it is
isospectral and absorbable into the twist that NEGATIVE CONTROL 2's M1 and M3
already vary.  NEGATIVE CONTROL 4 answers the question with a decision
procedure (`absorbable_by_diagonal_twist`) rather than an argument, on its own
four mutations and on NEGATIVE CONTROL 3's, and prints both answers.

Run:  python3 controls.py
"""

import sys

from face_complex import (
    Poset, boundary_matrix, chains_of_ideals, face_from_sur_iso, sur_iso,
    linear_extensions, le_to_facet, facet_to_le, top_laplacians, at_laplacian,
    coxeter_compression, twist, mat_eq, mat_sub, is_diagonal, reduced_betti,
    rank_mod_p, rank_exact, adjacent_transposition_graph, perm_sign,
    absorbable_by_diagonal_twist, not_isospectral,
)
from posets import all_posets, POSET_COUNTS, cover_string

FAIL = []
CANNOT_FAIL = []


def score(ok, cannot_fail):
    """The label a row gets.  Three outcomes, not two."""
    if not ok:
        return "FAIL"          # a false tautology is a failure, not a vacuous row
    return "CANNOT FAIL" if cannot_fail else "PASS"


def check(name, ok, detail="", cannot_fail=False):
    """Score one row.

    `cannot_fail=True` marks a row whose corruption provably cannot change the
    object under test.  Such a row is NOT a pass: it is recorded separately and
    printed as [CANNOT FAIL], and it suppresses the ALL CONTROLS PASS bottom
    line.  It is still verified -- `ok` false lands in FAIL as usual, because a
    theorem that does not hold is a genuine failure, not a vacuous row.
    """
    status = score(ok, cannot_fail)
    print("  [%s] %s%s" % (status, name, ("  -- " + detail) if detail else ""))
    if not ok:
        FAIL.append(name)
    elif cannot_fail:
        CANNOT_FAIL.append(name)
    return ok


def summarise(fails, cannot_fail_rows):
    """Return (lines, exit_code) for the bottom line.

    Pure function of the two tallies so that it can be exercised directly --
    see `scoring_self_test`.  The single invariant it enforces: the string
    "ALL CONTROLS PASS" is reachable only when BOTH tallies are empty.
    """
    lines = []
    if fails:
        lines.append("CONTROLS FAILED: %d" % len(fails))
        lines.extend("   - " + f for f in fails)
        return lines, 1
    if cannot_fail_rows:
        lines.append("CONTROLS: 0 failures, but %d row(s) CANNOT FAIL and are "
                     "NOT scored as passes:" % len(cannot_fail_rows))
        lines.extend("   - " + (t if len(t) <= 78 else t[:75] + "...")
                     for t in cannot_fail_rows)
        lines.append("A row that cannot fail covers nothing, so this battery's "
                     "bottom line is NOT 'all controls pass'.")
        return lines, 0
    lines.append("ALL CONTROLS PASS")
    return lines, 0


def scoring_self_test():
    """A control on the scoring logic itself.

    The repair in mg-1319 changed scoring LOGIC, so the logic gets a control of
    its own -- the mg-4ad1 discipline applied to the instrument that reports it.
    Stated exactly, because overstating what a control covers is the defect this
    whole change is landing: TWO of the five rows below FIRE on the pre-repair
    behaviour (it labelled a tautological row PASS, and printed ALL CONTROLS
    PASS over it).  The other three pin behaviour that must not change -- a real
    failure still reports first and exits nonzero, a false tautology is still a
    failure, and a clean run still reaches the ALL CONTROLS PASS bottom line.
    """
    print("CONTROL ON THE SCORING -- a tautological row must not read as a pass")
    banner = "ALL CONTROLS PASS"
    taut_lines, taut_code = summarise([], ["a row that cannot fail"])
    clean_lines, clean_code = summarise([], [])
    fail_lines, fail_code = summarise(["a real failure"], ["a row that cannot fail"])
    check("a row that cannot fail is labelled %r, not %r"
          % (score(True, True), score(True, False)),
          score(True, True) == "CANNOT FAIL" and score(True, False) == "PASS")
    check("a cannot-fail row whose reported fact is FALSE is still a %r"
          % score(False, True), score(False, True) == "FAIL")
    check("a cannot-fail row suppresses the %r bottom line" % banner,
          banner not in "\n".join(taut_lines) and taut_code == 0)
    check("with no cannot-fail row the bottom line is %r" % banner,
          clean_lines == [banner] and clean_code == 0)
    check("a real failure still exits nonzero and is reported first",
          fail_code == 1 and fail_lines[0].startswith("CONTROLS FAILED"))


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
                perturb_edge=False, normalise=False, sign_mode="true",
                incidence_mode="true"):
    """Return the pair (LHS, RHS) that claim (1) asserts to be equal:

        LHS = E . L^rel_top . E        (E = diag(sgn w), the orientation twist)
        RHS = D - A                    (the adjacent-transposition Laplacian)

    All the knobs exist so the negative controls can corrupt one ingredient at
    a time; the probe itself always runs with the defaults.

    `sign_mode` corrupts the CONSTRUCTION of L^rel from the complex (the
    simplicial signs of the boundary matrix); `incidence_mode` corrupts the
    INCIDENCE STRUCTURE it is built on (which facets a ridge meets, which
    ridges are free, how L(P) is mapped to facets).  Every other knob corrupts
    the comparison or the target.  See NEGATIVE CONTROLS 3 and 4.
    """
    td = top_laplacians(P, sign_mode=sign_mode, incidence_mode=incidence_mode)
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


def claim2_test(P, use_twist=True, sign_mode="true"):
    td = top_laplacians(P, sign_mode=sign_mode)
    les = td["les"]
    L = td["L_abs"]
    if use_twist:
        s = [perm_sign(w) for w in les]
        L = [[s[i] * L[i][j] * s[j] for j in range(len(les))] for i in range(len(les))]
    _, target = coxeter_compression(P)
    return mat_eq(L, target)


def claim3_test(P, sign_mode="true"):
    """Claim (3), at the level of the Laplacians: L^abs - L^rel is diagonal and
    its (w,w) entry is the number of FORBIDDEN adjacent transpositions at w."""
    td = top_laplacians(P, sign_mode=sign_mode)
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
                    CANNOT fire here -- and that is a THEOREM, not an
                    observation on 86 posets (mg-5630 section 2.2(a)): a ridge
                    omits exactly one ideal cardinality, so the deletion index
                    is fixed by the ridge alone and d_true = diag(row signs) .
                    d_allplus, a row rescaling that d^T d cannot see.  Scored
                    [CANNOT FAIL], not [PASS].  It is why NEGATIVE CONTROL 1
                    was never a construction-side control.  (The alternating
                    sign is load-bearing for the homology of F(P), where
                    NEGATIVE CONTROL 1 does fire -- just not for claims
                    (1)-(3).)

      facet-parity  flips the sign of every incidence of the odd-indexed
                    facets.  This does change the off-diagonal part, and the
                    identity test must reject it.  Read the row narrowly: the
                    corruption is the diagonal +-1 conjugation
                    L_parity = D . L_true . D with D = diag((-1)^j), so it is
                    ISOSPECTRAL and ABSORBABLE into the twist (claim (1) with
                    parity signs and twist E.D passes again on 86/86).  It is
                    the M1/M3 content reached through the construction's code
                    path, and it CANNOT FAIL on a construction error that is
                    not a per-facet sign convention -- demonstrated in
                    code/face_geometry_audit_5630/out_nc3.txt line F, where a
                    mis-indexed facet enumeration leaves this row rejecting
                    82/82 verbatim.  So the battery covers ONE ABSORBABLE SIGN
                    GAUGE of the construction, not the construction; le_to_facet
                    is the named uncovered site.

    The true-sign build passes throughout: the instrument was never wrong, the
    argument for trusting it was missing this control.
    """
    print("NEGATIVE CONTROL 3 -- corrupt the CONSTRUCTION of L^rel (mg-e0ce F2)")
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    bites = [P for P in ps if len(linear_extensions(P)) >= 2]
    n_true = sum(1 for P in ps if claim1_test(P, sign_mode="true") is True)
    check("true simplicial signs: claim (1) holds on %d/%d posets" % (n_true, len(ps)),
          n_true == len(ps))

    # "BOTH top Laplacians unchanged" and "claims (1)-(3) survive" are MEASURED,
    # each on the object named (mg-5630 section 3.2): the previous version of
    # this row printed "both top Laplacians UNCHANGED" while comparing only the
    # twisted L^rel, and never re-ran claims (2) or (3) under sign_mode at all.
    # A printed control message must not assert more than the code printing it
    # verifies -- the same defect as scoring a tautology [PASS].
    plus_rel = plus_abs = 0
    for P in ps:
        td_true, td_plus = top_laplacians(P), top_laplacians(P, sign_mode="allplus")
        plus_rel += mat_eq(td_plus["L_rel"], td_true["L_rel"])
        plus_abs += mat_eq(td_plus["L_abs"], td_true["L_abs"])
    plus_c1 = sum(1 for P in ps if claim1_test(P, sign_mode="allplus") is True)
    plus_c2 = sum(1 for P in ps if claim2_test(P, sign_mode="allplus") is True)
    plus_c3 = sum(1 for P in ps if claim3_test(P, sign_mode="allplus") is True)
    check("all-+1 signs leave both top Laplacians UNCHANGED -- L^rel on %d/%d, "
          "L^abs on %d/%d, each compared -- and claims (1)/(2)/(3) re-run under "
          "the corruption still hold on %d/%d/%d.  PROVABLE for every finite "
          "poset (the simplicial sign depends only on the ridge, so d_true = "
          "diag(row signs) . d_allplus and d^T d cannot see it), so this row is "
          "a theorem and not a test of the construction"
          % (plus_rel, len(ps), plus_abs, len(ps), plus_c1, plus_c2, plus_c3),
          plus_rel == plus_abs == plus_c1 == plus_c2 == plus_c3 == len(ps),
          cannot_fail=True)

    par_app = [P for P in bites
               if not mat_eq(claim1_pair(P, sign_mode="parity")[0],
                             claim1_pair(P)[0])]
    par_rej = sum(1 for P in par_app if not claim1_test(P, sign_mode="parity"))
    check("facet-parity signs -- rejected on %d/%d posets with |L(P)| >= 2 where "
          "the mutation bites (%d posets have |L(P)| = 1: a single facet, no "
          "second column to flip against).  Scope of this row, stated narrowly: "
          "the corruption is the diagonal conjugation L -> D.L.D, D = diag((-1)^j), "
          "so it is isospectral and absorbable into the twist -- it covers ONE "
          "SIGN GAUGE of the construction and cannot fail on a non-sign "
          "construction error (out_nc3.txt line F)"
          % (par_rej, len(par_app), len(ps) - len(bites)),
          par_rej == len(par_app) and len(par_app) == len(bites))


def negative_control_incidence(nmax):
    """NEGATIVE CONTROL 4 -- corrupt the INCIDENCE STRUCTURE of F(P) (mg-2789).

    WHY THIS EXISTS.  Until this control, every negative control in the battery
    was either a comparison-side mutation or a sign gauge.  NEGATIVE CONTROL 2:
    M1 and M3 vary the twist, M4 and M5 vary the target, M2 swaps which of the
    two Laplacians is compared.  NEGATIVE CONTROL 3: its facet-parity
    corruption is a diagonal +-1 conjugation, L_parity = D . L . D with
    D = diag((-1)^j) -- isospectral, and absorbable into the very twist that M1
    and M3 already vary, so it varies a gauge rather than the construction
    (mg-5630; the demonstration is in
    code/face_geometry_audit_5630/out_nc3.txt).  Nothing perturbed the
    INCIDENCE STRUCTURE, and that gap was not hypothetical: the same audit's
    line-F harness showed both of NEGATIVE CONTROL 3's negative lines stay
    SILENT on a mis-indexed facet enumeration, and that on a dropped ridge only
    a bite-count moves.  It could not fail on a construction error that was not
    a sign convention.  Both experiments are re-run below on this battery's own
    mutations, with this file's own counts.

    THE FOUR SITES corrupted here, one mutation each, all inside
    top_laplacians (see `incidence_mode` in face_complex.py):

      I1  a ridge's facet list       -- one interior ridge's second incidence
                                        re-targeted onto a facet it does not
                                        meet; row weight and signs untouched,
                                        so the free/interior split is untouched
      I2  the free/interior split    -- one FREE ridge counted as interior,
                                        i.e. dF(P) taken one ridge too small,
                                        with the boundary matrix exactly right
      I3  the ridge enumeration      -- one interior ridge missing from the
                                        complex altogether
      I4  the facet enumeration      -- le_to_facet mis-indexed by one (the
                                        prefixes of w[1:] instead of w[:-1]),
                                        which is the named uncovered site

    PROVENANCE, stated exactly.  I3 is mg-5630's line-F "drop a ridge",
    adopted with one change: it drops an INTERIOR ridge, so that the mutation is
    defined by what it does to the relative complex.  I4 is NOT mg-5630's other
    line-F corruption -- that one exchanged two facets, and by the test this
    section applies to itself, exchanging two columns is a (signed) permutation
    conjugation and therefore isospectral, i.e. a gauge.  It was measured, it
    was rejected on that ground, and the measurement is printed below rather
    than dropped; I4 is an off-by-one in le_to_facet instead, at the same site.
    I1 and I2 are the two remaining incidence sites.  None of the four is a
    diagonal conjugation.

    WHAT "REJECTS" DOES AND DOES NOT PROVE HERE -- read this before quoting a
    row.  Claim (1) holds on the uncorrupted build, so ANY corruption that
    changes L^rel is necessarily rejected by an equality test: the rejection
    count is arithmetic, not evidence.  The informative parts of each row are
    (a) that the corruption BITES at all, on the stated part of the population,
    and (b) that it is not absorbable into a parameter the battery already
    varies.  NEGATIVE CONTROL 3's "still rejects 82/82" did not separate those
    two, which is what mg-5630 found and what this section is built not to
    repeat.

    (b) IS COMPUTED, NOT ASSERTED.  For every poset where a mutation bites,
    `absorbable_by_diagonal_twist` decides exactly whether the corrupted matrix
    is S . (target) . S for SOME diagonal sign matrix S -- the family that
    contains the orientation twist E, M3's one-facet twist, and NEGATIVE
    CONTROL 3's D.  One absorbable poset fails the row.  Reported alongside,
    where it can be proved: that a spectral invariant moves, which rules out
    any similarity transform whatever, diagonal or not.

    WHAT THIS SECTION DOES NOT SHOW.  It tests the four sites above, on the
    posets stated in each row, and nothing wider.  It does not certify the rest
    of the construction: linear_extensions is not corrupted here (it is checked
    positively against A000112 and against Sur_iso in POSITIVE CONTROLS 2
    and 3), nor is the ideal-chain path chains_of_ideals, which claims (1)-(3)
    do not use.
    """
    print("NEGATIVE CONTROL 4 -- corrupt the INCIDENCE STRUCTURE of F(P), at four "
          "named sites (mg-2789)")
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    N = len(ps)
    muts = [
        ("I1 a ridge's facet list (one interior ridge re-targeted onto a facet it "
         "does not meet)", "ridge_facets"),
        ("I2 the free/interior split (one free ridge counted as interior)",
         "split_free_as_interior"),
        ("I3 the ridge enumeration (one interior ridge missing from the complex)",
         "ridge_drop"),
        ("I4 the facet enumeration le_to_facet (mis-indexed by one)",
         "facet_offbyone"),
    ]
    # A POSITIVE CONTROL ON THIS CONTROL'S OWN INSTRUMENT, run before the
    # instrument is used on anything.  "absorbable on 0/N" is worthless if it is
    # the answer of a test that always says no, so: conjugate the true matrix by
    # a genuine mixed diagonal sign matrix (must be reported absorbable), and
    # move one diagonal entry (must be reported NOT absorbable, since s_i^2 = 1
    # pins the diagonal).
    yes = no = 0
    for P in ps:
        L, _ = claim1_pair(P)
        m = len(L)
        s = [-1 if i % 3 == 0 else 1 for i in range(m)]
        conj = [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]
        shifted = [row[:] for row in L]
        shifted[0][0] += 1
        yes += absorbable_by_diagonal_twist(conj, L)
        no += not absorbable_by_diagonal_twist(shifted, L)
    check("instrument check: a genuine diagonal +-1 conjugation of L^rel is "
          "reported absorbable on %d/%d posets" % (yes, N), yes == N)
    check("instrument check: L^rel with one diagonal entry moved by 1 is reported "
          "NOT absorbable on %d/%d posets" % (no, N), no == N)
    # ... and the union-find decision procedure itself against brute force over
    # all 2^m sign vectors, on every matrix this section will judge, wherever m
    # is small enough to enumerate.  Without this, "absorbable on 0/N" could be
    # the answer of a buggy solver rather than a fact about the corruption.
    agree = cases = 0
    for P in ps:
        L_true, target = claim1_pair(P)
        m = len(L_true)
        if m > 8:
            continue
        for mode in ["true", "facet_swap01"] + [md for _, md in muts]:
            A = claim1_pair(P, incidence_mode=mode)[0]
            brute = False
            for bits in range(1 << m):
                s = [-1 if bits >> i & 1 else 1 for i in range(m)]
                if all(s[i] * A[i][j] * s[j] == target[i][j]
                       for i in range(m) for j in range(m)):
                    brute = True
                    break
            cases += 1
            agree += (brute == absorbable_by_diagonal_twist(A, target))
    check("instrument check: the union-find absorbability decision agrees with "
          "brute force over all 2^m sign vectors on %d/%d (poset, mutation) pairs "
          "with |L(P)| <= 8" % (agree, cases), agree == cases and cases > 0)

    same_target = 0
    multi_ridge = {}
    for name, mode in muts:
        app = rej = absorb = spec = 0
        vac, vac_sizes = 0, set()
        for P in ps:
            L_true, target = claim1_pair(P)
            L_mut, target_mut = claim1_pair(P, incidence_mode=mode)
            same_target += mat_eq(target, target_mut)
            multi_ridge[mode] = multi_ridge.get(mode, 0) + (
                top_laplacians(P, incidence_mode=mode)["n_multi_ridges"] > 0)
            if mat_eq(L_mut, L_true):
                vac += 1
                vac_sizes.add(len(linear_extensions(P)))
                continue
            app += 1
            if not mat_eq(L_mut, target):
                rej += 1
            if absorbable_by_diagonal_twist(L_mut, target):
                absorb += 1
            if not_isospectral(L_mut, L_true):
                spec += 1
        check("%s -- the claim-(1) test rejects on %d/%d posets where the corruption "
              "changes L^rel (%d vacuous, on |L(P)| in %s); absorbable into a diagonal "
              "+-1 twist on %d of those %d; spectrum provably moved on %d of those %d"
              % (name, rej, app, vac, sorted(vac_sizes), absorb, app, spec, app),
              app > 0 and rej == app and absorb == 0)

    # ---- measurements, deliberately NOT scored as PASS/FAIL rows ----------
    print("  measured, not scored:")
    print("    * the target D-A is byte-identical to the uncorrupted target on "
          "%d/%d (poset, mutation) pairs -- all four mutations are "
          "construction-side only, unlike M4 and M5" % (same_target, 4 * N))
    print("    * no ridge lies in >= 3 facets under any of the four mutations on "
          "any of the %d posets (%s), so the corrupted complexes still satisfy "
          "the 1-or-2-facets property POSITIVE CONTROL 3 verifies: that check "
          "would not have caught these either"
          % (N, ", ".join("%s on %d" % (m, c) for m, c in multi_ridge.items())))
    nc3_app = nc3_absorb = nc3_spec = 0
    for P in ps:
        L_true, target = claim1_pair(P)
        L_par, _ = claim1_pair(P, sign_mode="parity")
        if mat_eq(L_par, L_true):
            continue
        nc3_app += 1
        nc3_absorb += absorbable_by_diagonal_twist(L_par, target)
        nc3_spec += not_isospectral(L_par, L_true)
    print("    * the predicate that scores the four rows above, applied to NEGATIVE "
          "CONTROL 3's facet-parity corruption instead, would score it FAIL: that "
          "corruption is absorbable into a diagonal +-1 twist on %d/%d of the posets "
          "where it bites and its spectrum provably moves on %d/%d. So the four rows "
          "are falsifiable and this is the witness -- it is the gauge this section "
          "exists to get past (mg-5630)."
          % (nc3_absorb, nc3_app, nc3_spec, nc3_app))
    for name, mode in muts:
        plus_same = par_bite = 0
        for P in ps:
            base = claim1_pair(P, incidence_mode=mode)[0]
            plus_same += mat_eq(claim1_pair(P, sign_mode="allplus",
                                            incidence_mode=mode)[0], base)
            par_bite += not mat_eq(claim1_pair(P, sign_mode="parity",
                                               incidence_mode=mode)[0], base)
        print("    * with %s in place, NEGATIVE CONTROL 3's own lines are: line 2 "
              "all-+1-unchanged %d/%d (%s), line 3 parity bites on %d posets vs %d "
              "uncorrupted (%s). NEGATIVE CONTROL 4's row for the same corruption "
              "fires. This is mg-5630's line-F experiment run inside this battery; "
              "the corruptions are this file's own instances, so are the counts."
              % (mode, plus_same, N, "SILENT" if plus_same == N else "differs",
                 par_bite, nc3_app,
                 "unchanged, so that row reads the same verbatim"
                 if par_bite == nc3_app else "changed, so that row moves by accident"))
    sw_app = sw_absorb = sw_spec = 0
    for P in ps:
        L_true, target = claim1_pair(P)
        L_sw, _ = claim1_pair(P, incidence_mode="facet_swap01")
        if mat_eq(L_sw, L_true):
            continue
        sw_app += 1
        sw_absorb += absorbable_by_diagonal_twist(L_sw, target)
        sw_spec += not_isospectral(L_sw, L_true)
    print("    * a CANDIDATE THIS SECTION REJECTED, by the same question, before "
          "submitting: exchanging facets 0 and 1 (mg-5630's line-F first "
          "corruption). It bites on %d/%d posets and is not absorbable into a "
          "diagonal +-1 twist (%d/%d) -- but exchanging two columns conjugates "
          "L^rel by a signed permutation matrix, so it is isospectral, and the "
          "spectrum provably moves on %d/%d. A relabelling of the facet set is a "
          "gauge, so it is not scored above; row I4 replaces it with an off-by-one "
          "in le_to_facet, whose spectrum does move."
          % (sw_app, N, sw_absorb, sw_app, sw_spec, sw_app))
    print("    * where a row reports the spectrum moving on fewer than all of its "
          "biting posets, NO claim is made either way on the remainder: the trace, "
          "the sum of squared entries and det(. - k.I) mod (2^31-1) for k in "
          "{3,5,7,11,13} did not separate those. The diagonal-twist decision is "
          "exact on every one of them, and that is the absorbability question; "
          "non-isospectrality is the stronger one-sided extra.")
    print("    * row scoring, and who owns it: every row above is vacuous on the "
          "sub-population named in it, exactly as NEGATIVE CONTROL 2's M1-M5 are, "
          "and the scoring does not model vacuity -- only the [CANNOT FAIL] label, "
          "which mg-1319 landed and OWNS (see SCORING at the top of this file). "
          "mg-2789 added no [CANNOT FAIL] row: each of the four rows above fails if "
          "its corruption stops biting or turns out absorbable. The lines in this "
          "block are measurements, not rows, and are deliberately unscored.")


def main():
    nmax_cheap = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    scoring_self_test()
    positive_control_homology()
    negative_control_signs()
    positive_control_poset_counts(nmax_cheap)
    positive_control_face_complex(min(nmax_cheap, 4))
    positive_control_FP_homology(min(nmax_cheap, 5))
    negative_control_identity(min(nmax_cheap, 5))
    negative_control_construction(min(nmax_cheap, 5))
    negative_control_incidence(min(nmax_cheap, 5))
    print()
    lines, code = summarise(FAIL, CANNOT_FAIL)
    for line in lines:
        print(line)
    if code:
        sys.exit(code)


if __name__ == "__main__":
    main()
