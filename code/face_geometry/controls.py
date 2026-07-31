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

AND THE ANSWER TO THAT QUESTION IS NOT AUTOMATICALLY A CONTROL ROW (mg-8a12,
landing mg-fcf1's F2).  Asking it is right; SCORING it is right only where the
predicate could have answered either way.  For three of NEGATIVE CONTROL 4's
four mutations the answer is forced by arithmetic -- s_i^2 = 1 pins every
diagonal entry, so a corruption that moves one can never be absorbed -- and a
forced answer scored [PASS] is exactly the defect this file's SCORING section
exists to stop.  NEGATIVE CONTROL 4 now COMPUTES which of its rows are in that
position (`diag_preserved`, below) instead of asserting it either way, and
routes them to a [CANNOT FAIL] row.

AND THE ANSWER IS FORCED ON ALL FOUR, NOT THREE (mg-f1b2's F1, landed by
mg-da45).  The predicate has TWO forced gates and not one -- its own docstring
says so: `s_i^2 = 1` pins every diagonal entry AND `|s_i s_j| = 1` pins every
absolute value; only what survives both is a parity system where a sign is
consulted.  mg-8a12 routed on the first and printed a preserved diagonal as
proof that "the off-diagonal signs actually decide" for the one row it keeps
absorbability scored in.  They do not: 0 of the 297 biting (poset, mutation)
pairs in the section reach the parity system at all.

AND THE SECOND ATTEMPT AT SAYING WHY WAS ALSO NOT A TRACE (mg-1c80's F1, landed
by mg-5f9a).  This is the THIRD version of one sentence, and the first two
failed the same way: a reason written ALONGSIDE the procedure it is about.
mg-da45's `deciding_gate` tested all diagonals and then all magnitudes; the
predicate interleaves the two BY ROW, so the two orders named different gates on
57 of the 297 pairs, and DELETING THE GATE THE ARTIFACT CALLED DECISIVE LEFT THE
ARTIFACT BYTE-IDENTICAL.  A reason a deletion cannot disturb is not the reason
the code has.

SO NO THIRD REASON IS WRITTEN HERE.  The predicate is INSTRUMENTED instead
(`face_complex.absorb_trace`): it returns the gate it returned at and the number
of signs it read, and `absorbable_by_diagonal_twist` is a wrapper over it, so
what the rows print is emitted by the code path rather than asserted beside it.
Three questions that mg-da45 answered with one function are now three functions
-- `diagonal_moves` (a property of the matrices; drives the routing and is the
theorem's hypothesis), `absorb_trace` (one execution; ORDER-DEPENDENT, and every
row that quotes a gate says so), `gate_violations` (exhaustive, so it measures
whether the gate named was load-bearing: on 294 of the 297 pairs both forced
gates are violated and neither is).  What the rows now rest on is `signs_read`,
which no ordering can move.  Verified by the deletion test that caught the last
version, in code/face_geometry_instr_5f9a/: delete a gate from the predicate and
the artifact must CHANGE.

What deliberately did NOT change: row I4 keeps `absorb == 0` in its scored
condition.  The clause is true, it is not evidence, and removing it is a scoring
change that belongs to its own item -- this one corrects a printed reason.

Run:  python3 controls.py
"""

import itertools
import sys

from face_complex import (
    Poset, boundary_matrix, chains_of_ideals, face_from_sur_iso, sur_iso,
    linear_extensions, le_to_facet, facet_to_le, top_laplacians, at_laplacian,
    coxeter_compression, twist, mat_eq, mat_sub, is_diagonal, reduced_betti,
    rank_mod_p, rank_exact, adjacent_transposition_graph, perm_sign,
    absorbable_by_diagonal_twist, absorb_trace, gate_violations, diagonal_moves,
    not_isospectral, le_to_facet_offbyone,
)
from posets import all_posets, POSET_COUNTS, cover_string

FAIL = []
CANNOT_FAIL = []
ROW_NAMES = []      # every row's printed name, for the artifact check in main()


class ArtifactTee:
    """Records every line this run writes to stdout, verbatim, while writing it.

    `run_all.sh` builds `controls_output.txt` as `python3 controls.py 5 >
    controls_output.txt` -- it piped into `tee` until mg-c2b3, and the bytes it
    writes are the same either way; only the exit status differs.  So what this
    object records IS the artifact.  It is
    installed as `sys.stdout` in `main()` so that the artifact check reads what
    a grep of the file would read, whatever route printed it -- a row name, a
    `detail=` string, a section heading, or a bare `print()` added tomorrow.

    Why at the stream and not at `check()` (mg-7d5a, from mg-6653's A2): the
    previous version of the check scanned `ROW_NAMES` only, so ATTACKS B and C
    reached the artifact by printing through a route the check did not model.
    A check that enumerates the routes it knows about can always be evaded by a
    new one; a check on the byte stream cannot.
    """

    def __init__(self, stream):
        self._stream = stream
        self._partial = ""
        self._lines = []

    def write(self, s):
        self._stream.write(s)
        self._partial += s
        while "\n" in self._partial:
            line, self._partial = self._partial.split("\n", 1)
            self._lines.append(line)

    def flush(self):
        self._stream.flush()

    def lines_so_far(self):
        """Every complete line written, plus any unterminated tail."""
        return list(self._lines) + ([self._partial] if self._partial else [])


ARTIFACT = None     # the ArtifactTee installed by main(); None when unused


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
    ROW_NAMES.append(name)
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
    failure, and a clean run still reaches the all-pass bottom line.

    THE ROW NAMES BELOW MUST NOT CONTAIN THE BANNER LITERAL (mg-f7bc F5, landed
    by mg-f2e1).  As first written they did, so this self-test put two
    [PASS]-prefixed copies of the all-pass banner into the first five lines of
    `controls_output.txt` -- above a bottom line that explicitly denies it.  Any
    grep for the banner on the artifact then returned two false positives before
    the one true answer, i.e. the A4 repair reintroduced, in the artifact, the
    exact reads-as-covered defect it exists to remove: output text claiming more
    than the code that prints it verifies.  The assertions still compare against
    `banner`; only the printed NAME is indirect, so the artifact contains the
    string once and only where it is true.
    """
    print("CONTROL ON THE SCORING -- a tautological row must not read as a pass")
    banner = "ALL CONTROLS PASS"
    banner_name = "the all-pass banner"          # never the literal; see above
    taut_lines, taut_code = summarise([], ["a row that cannot fail"])
    clean_lines, clean_code = summarise([], [])
    fail_lines, fail_code = summarise(["a real failure"], ["a row that cannot fail"])
    check("a row that cannot fail is labelled %r, not %r"
          % (score(True, True), score(True, False)),
          score(True, True) == "CANNOT FAIL" and score(True, False) == "PASS")
    check("a cannot-fail row whose reported fact is FALSE is still a %r"
          % score(False, True), score(False, True) == "FAIL")
    check("a cannot-fail row keeps %s out of the bottom line" % banner_name,
          banner not in "\n".join(taut_lines) and taut_code == 0)
    check("with no cannot-fail row the bottom line IS %s" % banner_name,
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


# Why each single-site incidence corruption provably moves a DIAGONAL entry of
# L^rel, which is what makes its "not absorbable into a diagonal twist" answer a
# theorem rather than a measurement (mg-8a12, mg-fcf1 F2).  Read out by the
# [CANNOT FAIL] row of NEGATIVE CONTROL 4 for whichever rows are forced, so the
# printed argument always names the rows it is actually about.
DIAGONAL_MOVES = {
    "split_free_as_interior":
        "I2 is exactly L_true + e_j.e_j^T, j the free ridge's one facet, so one "
        "diagonal entry rises by 1",
    "ridge_drop":
        "I3 is L_true minus that ridge's rank-one outer product, so both its "
        "facets' diagonal entries drop by 1",
    "ridge_facets":
        "I1 moves a rank-one term from one facet to another, so the abandoned "
        "facet's diagonal entry drops by 1",
}


# NO GATE PROCEDURE LIVES IN THIS FILE ANY MORE (mg-1c80's F1, landed by
# mg-5f9a).  There used to be one -- `deciding_gate` -- and it was the defect:
# it tested ALL diagonals and then ALL magnitudes, which is not the order
# `absorbable_by_diagonal_twist` uses (that one interleaves the two BY ROW), so
# the two named different gates on 57 of the 297 biting pairs and the artifact
# printed the wrong split.  Deleting the gate it called decisive from the
# predicate left the artifact BYTE-IDENTICAL, which is the proof that the name
# was not the code's.
#
# The replacement is not a better procedure alongside the predicate; it is the
# predicate reporting itself.  `face_complex.absorb_trace` returns the gate it
# returned at and how many signs it read, and `absorbable_by_diagonal_twist` is
# a wrapper over it, so a caller cannot get a gate from one execution and an
# answer from another.  Rows below call `absorb_trace` directly -- a local alias
# would be one more place for the two to drift apart.


def entry_mismatches(A, B):
    """(magnitude mismatches, sign-only mismatches) between two same-shape
    matrices, counted by ENTRY.

    The second number counts entries a sign decision COULD have been made on:
    |A[i][j]| == |B[i][j]| and A[i][j] != B[i][j].

    IT IS NOT THE MEASURE OF WHETHER A SIGN WAS CONSULTED, and mg-da45 read it
    that way ("zero of them means the predicate never consulted a sign").  That
    is an inference about the predicate drawn from outside it, which is the
    error this lineage keeps repeating.  The predicate now reports the thing
    directly -- `Trace.signs_read`, the number of off-diagonal constraints its
    union-find loop actually consumed -- and that is what the rows quote.  This
    stays because "how far apart are these two matrices" is a fair question in
    its own right, and because a nonzero count here with `signs_read == 0` is
    exactly the disagreement worth seeing.
    """
    m = len(A)
    mag = sum(1 for i in range(m) for j in range(m)
              if abs(A[i][j]) != abs(B[i][j]))
    sgn = sum(1 for i in range(m) for j in range(m)
              if abs(A[i][j]) == abs(B[i][j]) and A[i][j] != B[i][j])
    return mag, sgn


def absorbable_bruteforce(A, B):
    """Is there s in {+1,-1}^len(A) with s_i . A_ij . s_j == B_ij for every i, j?

    THE DEFINITION, ENUMERATED.  No union-find, no gates, no short-circuit, and
    no line of code in common with `absorb_trace` -- the comparison is `mat_eq`,
    so a shape mismatch is simply an equality that no s can satisfy.  Exponential
    in len(A) and only ever called on the four hand-built 2x2/3x3 pairs below.

    IT EXISTS TO BE AN INDEPENDENT EXPECTED VALUE (mg-d0e2 OUTSTANDING 2).  A
    check that compares the predicate against ITSELF -- against its own earlier
    output, or against a label it printed -- passes whenever the predicate is
    stably wrong, which is the one case it was supposed to exclude.  This is what
    the rows below compare against instead.
    """
    m = len(A)
    for bits in range(1 << m):
        s = [1 - 2 * ((bits >> i) & 1) for i in range(m)]
        conj = [[s[i] * A[i][j] * s[j] for j in range(len(A[i]))]
                for i in range(m)]
        if mat_eq(conj, B):
            return True
    return False


# ---------------------------------------------------------------------------
# THE GAUGE DETECTOR (mg-e35b), and WHY IT LIVES IN THIS FILE.
#
# It belongs beside `absorbable_bruteforce` above and for the same reason: it is
# a DERIVED expected value, not part of the object under test.  `absorb_trace`
# lives in face_complex.py because it is the predicate NEGATIVE CONTROL 4 scores;
# this is a second, independent answer to an overlapping question, and the whole
# value of it is that the two can disagree.
#
# AND THERE IS A SECOND, MEASURED REASON, recorded because the first draft of
# mg-e35b put both functions in face_complex.py and it cost two instruments.
# mg-0b07's p3 (re-run at HEAD by code/face_geometry_instr_5f9a/d4) runs THIS
# tree's controls.py against a PINNED face_complex.py from b6bc2ef.  A new
# function in face_complex.py that controls.py imports makes that mix an
# ImportError -- the battery produced 0 bytes and exit 1, both of p3's pinned
# rows went MISS, and d4 went from 0 BROKEN to 5.  A file two instruments pin
# is a file whose import surface is load-bearing outside this repository's own
# runner, and adding to it is not free.
#
# WHAT THAT COSTS, said rather than left as a silent gain: d2's clause sweep
# reads its population from face_complex.py and posets.py, so the two clauses of
# `signed_permutation_witness`'s shape guard are NOT swept here, exactly as
# posets.py's two are not.  When they were in face_complex.py the sweep found
# them, and its verdict was NOT COVERED -- deletion establishes nothing about
# them, because no call site in this battery passes matrices of different order
# or a ragged one.  That verdict is the same either way; what is lost is that
# the sweep would have printed it.
# ---------------------------------------------------------------------------

def permute_matrix(L, pi):
    """Relabel the facet indices of L by `pi`:  (Pi^T . L . Pi)[i][j] =
    L[pi[i]][pi[j]], with Pi the permutation matrix of `pi`.

    Separated from the sign question on purpose.  `absorbable_by_diagonal_twist`
    decides the DIAGONAL half of the gauge group; this supplies the PERMUTATION
    half, and the two together are the signed permutations -- the family
    NEGATIVE CONTROL 4 rejected `facet_swap01` for lying in.
    """
    m = len(L)
    return [[L[pi[i]][pi[j]] for j in range(m)] for i in range(m)]


def signed_permutation_witness(A, B, perms):
    """Exhibit a signed permutation carrying A to B, or return None.

    Searches `perms` for a pi and a sign vector s with

        s_i . s_j . A[pi[i]][pi[j]] == B[i][j]   for all i, j,

    i.e. B = S . (Pi^T . A . Pi) . S -- A and B differ by a relabelling of the
    facet set composed with a re-orientation.  Returns (pi, s) or None.

    WHAT MAKES THE ANSWER A WITNESS AND NOT AN OPINION.  The sign vector is
    SOLVED (a BFS over the off-diagonal support, propagating s_j = s_i . t with
    t = B[i][j] / A[pi[i]][pi[j]]) and then the product S . (Pi^T A Pi) . S is
    RECONSTRUCTED IN FULL and compared with B by `mat_eq`.  A caller therefore
    gets a pair it can check itself, and a bug in the propagation cannot return
    a false positive -- the reconstruction would not match.  That is the same
    standard mg-fcf1 applied to `absorb_trace` (independent BFS plus explicit
    reconstruction, agreeing with brute force on 306/306), applied here to the
    larger family.  A NEGATIVE answer is weaker and is bounded by `perms`: it
    says no permutation IN THE CANDIDATE LIST works, not that none exists.
    Callers must state which list they passed -- see `gauge_candidate_perms` in
    controls.py, which passes every permutation when |L(P)| is small enough to
    enumerate and named candidates otherwise.

    WHY IT IS NOT `absorbable_by_diagonal_twist(permute_matrix(A, pi), B)`.
    That composition would answer the same question and is the obvious way to
    write it, but it would make every gauge classification in this battery
    depend on the predicate whose own gate labelling has been repaired three
    times (mg-8a12 -> mg-da45 -> mg-5f9a).  This function shares no line with
    it, so the dichotomy row in NEGATIVE CONTROL 4 and the absorbability rows
    above it are two independent measurements of overlapping questions, and
    they can disagree -- which is what makes the consistency between them worth
    printing.
    """
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return None
    for pi in perms:
        M = permute_matrix(A, pi)
        if any(M[i][i] != B[i][i] for i in range(m)):
            continue                      # s_i^2 = 1 pins the diagonal
        if any(abs(M[i][j]) != abs(B[i][j])
               for i in range(m) for j in range(m)):
            continue                      # |s_i s_j| = 1 pins the magnitudes
        s = [0] * m
        ok = True
        for root in range(m):
            if s[root]:
                continue
            s[root] = 1
            stack = [root]
            while stack and ok:
                i = stack.pop()
                for j in range(m):
                    if j == i or M[i][j] == 0:
                        continue
                    t = 1 if B[i][j] == M[i][j] else -1
                    if s[j] == 0:
                        s[j] = s[i] * t
                        stack.append(j)
                    elif s[j] != s[i] * t:
                        ok = False
                        break
            if not ok:
                break
        if not ok:
            continue
        # RECONSTRUCT AND COMPARE.  Nothing above is trusted: the returned pair
        # is only returned if it reproduces B entry for entry.
        rebuilt = [[s[i] * M[i][j] * s[j] for j in range(m)] for i in range(m)]
        if mat_eq(rebuilt, B):
            return (list(pi), s)
    return None

# THE TWO GATES NOTHING IN THIS BATTERY REACHES (mg-d0e2 OUTSTANDING 1, landed
# by mg-04a8).
#
# mg-d0e2 ran the deletion test on nine mutations of the code this file's
# sentences name, and seven moved the artifact.  TWO MOVED NOT ONE BYTE:
# `absorb_trace`'s `shape` returns and its `parity` contradiction branch.  Not
# because the branches are wrong -- because nothing this battery constructs ever
# reaches them.  Measured by that audit over all four populations the section
# feeds the predicate (297 NC4 biting + 306 brute-force + 82 NC3 + 172 instrument
# = 857 pairs): 0 pairs decided NOT ABSORBABLE at the parity gate, 0 pairs with a
# shape mismatch anywhere.  A predicate that had LOST the ability to reject a
# contradictory sign system, or to notice that the two sides are not the same
# shape, would have agreed with every question the battery asked it, and every
# row here would still have been green.
#
# So the two branches are exercised on CONSTRUCTED pairs, and the answer they are
# scored against is not written down: it is DERIVED by `absorbable_bruteforce`.
#
# EACH ROW'S ANSWER WOULD DIFFER UNDER:
#   the shape row  -- deleting the one `return Trace(False, "shape", 0)`.  Both
#                     pairs then fall through to the sign system, are reported
#                     ABSORBABLE, and brute force still says no s exists.
#                     THERE IS ONE RETURN BECAUSE mg-9220 MERGED TWO.  With two,
#                     deleting BOTH changed the artifact and deleting the FIRST
#                     ALONE did not -- the 2x2-against-3x3 pair simply fell
#                     through to the second, which answers False at `shape` just
#                     the same (mg-e7bc).  So the deletion bit on the PAIR, not
#                     on each return, and the inert one was REMOVED rather than
#                     covered by a third pair: this row is not asked to detect
#                     it, and no row here was added for it.
#                     AND ITS CONDITION IS A TWO-CLAUSE DISJUNCTION AGAIN,
#                     SPELLED WITH AN OPERATOR ON PURPOSE (mg-0b07).  mg-64b6
#                     wrote it as one comparison of the two row-shape profiles
#                     and reported that there was no clause left to delete.
#                     That was true and it was not the floor: a list comparison
#                     IS a disjunction, and its ORDER half -- `len(A) != len(B)`
#                     -- could be taken out with the width half standing for
#                     BYTE-IDENTICAL, exit 0, every row here green.  Merging had
#                     removed the handle, not the rung.  The `or` is back so the
#                     two halves are operands a deletion test can take out one
#                     at a time.
#                     WHICH HALF THIS ROW CAN SEE, AND WHICH IT CANNOT.  Its
#                     second pair is RAGGED at the same order, so it covers the
#                     WIDTH clause: delete that clause alone and this row fails
#                     (24,909 bytes, exit 1).  NO PAIR HERE SEPARATES THE ORDER
#                     CLAUSE.  The first pair differs in order AND in width, so
#                     the width half rejects it unaided; delete the order clause
#                     alone and every row here is still green.
#                     AND STILL NO ROW WAS ADDED FOR IT, which is a choice and
#                     is stated rather than left as an absence.  A pair with
#                     len(A) != len(B) and no ragged row -- a 2x2 against a
#                     three-row B whose first two rows are 2 wide -- would cover
#                     it in one line.  It is not added because the question this
#                     lineage keeps failing is not "is this branch watched" but
#                     "does the evidence say what it is read as saying": the
#                     uncovered half is now NAMED, on the line its result is
#                     read on (d2_deletion.py, section PER CLAUSE), and a reader
#                     who wants it covered can add the pair here and watch that
#                     line turn.  What is not acceptable is silence, and this is
#                     the end of it.
#   the parity row -- deleting the `return Trace(False, "parity", signs_read)`
#                     branch.  The contradictory pair is then reported
#                     ABSORBABLE against a brute force that enumerated all 8 sign
#                     vectors and found none.
# Both deletions are RUN and not argued: code/face_geometry_instr_5f9a/
# d2_deletion.py, cases AFTER-5 and AFTER-6.  Before this row existed they were
# invisible: the artifact regenerated byte-identically with either branch gone.
#
# Each list carries a pair the branch must ACCEPT as well as one it must REJECT.
# Without it the row would pass on a predicate that answered "not absorbable" to
# everything -- the [CANNOT FAIL] defect this section already carries one scar
# from (mg-2789 -> mg-8a12).
UNREACHED_GATE_PAIRS = {
    "shape": [
        ("different orders -- 2x2 against 3x3, so S.A.S is not even comparable "
         "to B", False,
         [[0, 1], [1, 0]],
         [[0, 1, 0], [1, 0, 0], [0, 0, 0]]),
        ("same order, RAGGED -- row 0 has 2 entries on one side and 3 on the "
         "other, which comparing the two ORDERS alone does not see", False,
         [[0, 1], [1, 0]],
         [[0, 1, 0], [1, 0]]),
        ("the accepting side: identical 2x2 matrices, s = (+1,+1)", True,
         [[0, 1], [1, 0]],
         [[0, 1], [1, 0]]),
    ],
    "parity": [
        ("a CONTRADICTORY sign system -- s0.s1 = +1 and s0.s2 = +1 force "
         "s1.s2 = +1, and the pair demands s1.s2 = -1", False,
         [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
         [[0, 1, 1], [1, 0, -1], [1, -1, 0]]),
        ("the accepting side, same support and same magnitudes: s = "
         "(+1,-1,-1) realises it", True,
         [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
         [[0, -1, -1], [-1, 0, 1], [-1, 1, 0]]),
    ],
}


def predicted_incidence_delta(P, mode):
    """The perturbation `mode` is PREDICTED to make to the untwisted L^rel,
    computed from the corrupted site alone.  None if the mutation did not apply.

    THIS IS THE CAUSATION EVIDENCE (mg-8a12, C4(c)).  "The test rejects" is not
    by itself evidence that the test SAW the corruption: mg-5630's line F found
    a row that appeared to fire only because a bite-count moved 82 -> 78, an
    accident of a len() comparison rather than a detection.  So each of I1, I2
    and I3 is required to reject with a residual that MATCHES a prediction made
    without looking at the corrupted matrix.

    The prediction reads only the TRUE build: L^rel = sum over interior ridges r
    of d_r^T d_r, so changing what one ridge contributes changes L^rel by
    exactly that rank-one term.  With d_r the true boundary row of the ridge the
    mutation touches (`mutated_ridge`):

      I2 split_free_as_interior   ridge r joins the relative complex:  + d_r^T d_r
      I3 ridge_drop               ridge r leaves it:                   - d_r^T d_r
      I1 ridge_facets             r's second incidence moves from facet j2 to a
                                  facet j3 it does not meet: d_r^T d_r is
                                  replaced by d_r'^T d_r' with that entry moved

    I4 (facet_offbyone) re-indexes the whole facet enumeration, so it has no
    single site and gets no prediction here -- see the row itself.
    """
    r = top_laplacians(P, incidence_mode=mode)["mutated_ridge"]
    if r is None:
        return None
    td = top_laplacians(P)
    M, _, nc = boundary_matrix(td["facets"], td["ridges"])
    row = M.get(r, {})

    def outer(vec, sgn=1):
        D = [[0] * nc for _ in range(nc)]
        for a, va in vec.items():
            for b, vb in vec.items():
                D[a][b] += sgn * va * vb
        return D

    if mode == "split_free_as_interior":
        return outer(row)
    if mode == "ridge_drop":
        return outer(row, -1)
    if mode == "ridge_facets":
        j1, j2 = sorted(row.keys())
        j3 = next(j for j in range(nc) if j not in (j1, j2))
        gained, lost = outer({j1: row[j1], j3: row[j2]}), outer(row, -1)
        return [[gained[i][j] + lost[i][j] for j in range(nc)] for i in range(nc)]
    return None


# The largest |L(P)| at which `gauge_candidate_perms` enumerates EVERY
# permutation.  Above it the candidate list is the named relabelling the
# mutation itself induces, and nothing else -- so a NOT-GAUGE answer above this
# bound is bounded by the list and says so wherever it is printed (mg-e35b).
PERM_BRUTE_MAX = 6


def gauge_candidate_perms(P, mode):
    """The permutations of the facet index set offered to
    `signed_permutation_witness` when asking whether `mode` is a GAUGE on P.

    THREE SOURCES, and the bound is the point (mg-e35b, landing mg-fcf1's F2
    tail).  The question "is the corrupted complex the true one relabelled?" is
    the same question this section already used to REJECT `facet_swap01` -- *a
    relabelling of the facet set is a signed-permutation conjugation, hence
    isospectral*.  mg-fcf1 applied that standard to the rows this section KEPT
    and found it disqualifies 9 (poset, row) pairs, so the standard has to be
    asked of every row, by this file, on this file's own population.  Deciding
    it in general is a graph-isomorphism-shaped search; what is offered instead
    is an explicitly bounded candidate list:

      1. the IDENTITY.  A pure diagonal twist is a signed permutation with
         pi = id, so this makes the gauge question a widening of the
         absorbability question rather than a different one.
      2. the RELABELLING THE MUTATION INDUCES, when the mutated facet list is a
         permutation of the true one: facet i of the corrupted complex is then
         facet pi(i) of the true one and the whole complex is a relabelling.
         This is the case that catches `facet_swap01` (pi = the transposition)
         and row I4 on the antichains (pi = cyclic rotation of L(P) = S_n).
      3. EVERY permutation, when |L(P)| <= PERM_BRUTE_MAX.  This is what settles
         row I1's six -- there the facet SET is untouched, so source 2 offers
         only the identity, and the relabelling is a genuine search.

    A GAUGE answer is a witness and needs no bound.  A NOT-GAUGE answer is
    bounded by this list, and the row that prints it says so.
    """
    les = linear_extensions(P)
    m = len(les)
    perms = [list(range(m))]
    true_facets = [le_to_facet(w) for w in les]
    mut_facets = [le_to_facet_offbyone(w) for w in les] \
        if mode == "facet_offbyone" else list(true_facets)
    if mode == "facet_swap01" and m >= 2:
        mut_facets[0], mut_facets[1] = mut_facets[1], mut_facets[0]
    if sorted(mut_facets) == sorted(true_facets):
        idx = {f: i for i, f in enumerate(true_facets)}
        induced = [idx[f] for f in mut_facets]
        if induced not in perms:
            perms.append(induced)
    if m <= PERM_BRUTE_MAX:
        perms.extend(list(p) for p in itertools.permutations(range(m)))
    return perms


def mutation_applied_at_site(P, mode):
    """Did `mode` change the object it names, whatever it then did to L^rel?

    THE TWO MEANINGS OF "VACUOUS", SEPARATED (mg-e35b, landing mg-fcf1's F4).
    Every row of NEGATIVE CONTROL 4 reports a vacuous count, and until now the
    label covered two categorically different facts:

      the mutation DID NOT APPLY -- there was no eligible ridge to re-target,
        drop or re-split, so the corrupted build IS the true build and there is
        nothing for the pipeline to see.  This is I1, I2 and I3's whole vacuous
        population.
      the mutation APPLIED AND THE PIPELINE DID NOT SEE IT -- a different
        complex was built and claim (1) still holds on it.  That is not vacuity,
        it is BLINDNESS at the site the row is named after, and it is I4's whole
        vacuous population.

    Returning "did the site change" separately from "did L^rel change" is what
    lets a row say which of the two it is reporting.  For the three ridge
    mutations the site is `mutated_ridge` (None when no eligible ridge exists);
    for the two facet-enumeration mutations it is the facet list itself.
    """
    td_mut = top_laplacians(P, incidence_mode=mode)
    if mode in ("facet_offbyone", "facet_swap01"):
        return td_mut["facets"] != top_laplacians(P)["facets"]
    return td_mut["mutated_ridge"] is not None


def mutated_facet_set_differs(P, mode):
    """Does `mode` build a DIFFERENT SET of facets, not merely a different
    ordering of the same set?  The stronger half of `mutation_applied_at_site`,
    and the one that makes I4's vacuous posets a blindness rather than a
    relabelling: on those the complex under test is genuinely not F(P).
    """
    td_mut = top_laplacians(P, incidence_mode=mode)
    return sorted(td_mut["facets"]) != sorted(top_laplacians(P)["facets"])


def negative_control_incidence(nmax):
    """NEGATIVE CONTROL 4 -- corrupt the INCIDENCE STRUCTURE of F(P) (mg-2789,
    repaired by mg-8a12 after the mg-fcf1 audit).

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
    (b) that the rejection is CAUSED by the corruption rather than by a side
    effect, and (c) that it is not absorbable into a parameter the battery
    already varies.  NEGATIVE CONTROL 3's "still rejects 82/82" did not separate
    these, which is what mg-5630 found and what this section is built not to
    repeat.

    (b) IS THE HALF mg-2789 LEFT IMPLICIT, and mg-8a12 supplies it: on every
    biting poset the residual L_mut - (D - A) is required to equal a prediction
    made from the corrupted site alone, without reading the corrupted matrix
    (`predicted_incidence_delta`).  That is what separates "the test saw the
    corruption" from "something else moved and the comparison noticed", which is
    the failure mg-5630's line F caught.  The shape of the compared matrices is
    checked too, so no rejection can be a dimension mismatch.

    (c) IS COMPUTED, NOT ASSERTED.  For every poset where a mutation bites,
    `absorbable_by_diagonal_twist` decides exactly whether the corrupted matrix
    is S . (target) . S for SOME diagonal sign matrix S -- the family that
    contains the orientation twist E, M3's one-facet twist, and NEGATIVE
    CONTROL 3's D.  Reported alongside, where it can be proved: that a spectral
    invariant moves, which rules out any similarity transform whatever, diagonal
    or not.

    AND (c) IS SCORED ONLY WHERE THE PREDICATE COULD HAVE SAID EITHER THING
    (mg-8a12, landing mg-fcf1's F2 -- this is the repair).  `s_i^2 = 1` pins
    every diagonal entry, so `absorbable_by_diagonal_twist` returns False the
    instant a diagonal entry moves.  On a mutation that provably moves one,
    "absorbable on 0 of N" is arithmetic at every n and cannot fail -- it is a
    THEOREM being read out as an 82-poset count, mg-78c0's defect shape.  So
    each row measures `diag_preserved`, the number of its biting posets on which
    the diagonal is unchanged -- asked directly, of the two matrices, by
    `diagonal_moves` (mg-5f9a; mg-da45 read it off a gate label instead, which is
    a different question) -- and routes on it:

      diag_preserved > 0   absorbability stays in the row's scored condition
                           (this is I4: 3 of 61)
      diag_preserved == 0  the diagonal moved on every one of them, and a moved
                           diagonal is not absorbable for ANY sign vector, so
                           absorbability is REMOVED from the row and stated as a
                           proven property in a single [CANNOT FAIL] row (this is
                           I1, I2 and I3)

    mg-2789 scored the forced answer as part of four passing rows and printed
    that it had added no [CANNOT FAIL] row.  Both are corrected here.  The
    mathematics is untouched: the corruptions are not gauges, and that is a
    stronger statement than mg-2789 claimed for it, just not a measured one.

    AND `diag_preserved` IS NOT THE GATE THAT DECIDES (mg-f1b2's F1, landed by
    mg-da45).  This docstring used to call it "the number of its biting posets
    on which the diagonal is unchanged AND THE OFF-DIAGONAL SIGNS ACTUALLY
    DECIDE", and the row it keeps scored printed the same thing.  The second
    conjunct was never measured and is false: the predicate's second gate,
    `|s_i s_j| = 1`, is forced by the same arithmetic as the first, and it is the
    gate that fires on all three posets row I4 cites -- 2 off-diagonal magnitudes
    per row of L^rel differ there and not one entry differs in SIGN alone, so no
    sign is ever consulted.  It is forced at every n and not merely measured to
    n = 5: the off-diagonal support of L^rel is the adjacent-transposition graph
    (claim (1), proven), and the off-by-one map is prefixes_true(rot(w)) with rot
    the cyclic rotation of POSITIONS, which carries n-2 of the n-1 generators to
    generators and one out of the set, so exactly one neighbour of every vertex
    changes: 2|L(P)| mismatched entries at every n >= 3.

    AND THE SECOND ATTEMPT TO SAY WHICH GATE WAS ALSO NOT A TRACE (mg-1c80's F1,
    landed by mg-5f9a).  mg-da45 answered it with `deciding_gate`, which tested
    all diagonals and then all magnitudes; the predicate interleaves the two BY
    ROW, so the two orders named different gates on 57 of the 297 biting pairs,
    and deleting the gate the artifact called decisive left the artifact
    BYTE-IDENTICAL.  The predicate now REPORTS its own gate and its own count of
    signs read (`face_complex.absorb_trace`), every row that quotes a gate says
    the label is the first one REACHED, and `gate_violations` measures the rest:
    on 294 of the 297 pairs BOTH forced gates are violated, so on those no gate
    name is load-bearing.  What the rows rest on instead is the sign count, which
    no ordering can move.  Still no new scored row -- scoring "my routing
    quantity is the right one" is the move that produced two generations of the
    defect, and the deletion test in code/face_geometry_instr_5f9a/ is what
    checks this one instead.

    WHAT WAS NOT CHANGED, and it is a choice.  Row I4 keeps `absorb == 0` in its
    scored condition: the count is true, the correction owed was to the reason
    printed for keeping it.  Dropping the clause and extending the [CANNOT FAIL]
    row to all four corruptions is a scoring change with its own consequences
    (the routing row's condition is one of them) and belongs to its own item.
    Nor is the premise corrected where it ORIGINATED, and that is left visible on
    purpose: it is printed by mg-fcf1's own instrument
    (`code/face_geometry_audit_fcf1/audit_nc4.py`, out_nc4.txt:27 -- "the
    predicate does real work on 3 poset(s): the diagonal matches and the
    off-diagonal signs decide"), and mg-8a12 adopted it from there rather than
    measuring it.  Agreeing with the auditor was the transmission path; the file
    that acts on a number is the file that has to measure it.

    AND THE GAUGE STANDARD IS NOW ASKED OF THE ROWS KEPT, NOT ONLY OF THE ROW
    REJECTED (mg-fcf1's F1/F2 tail, landed by mg-e35b).  `facet_swap01` was
    rejected on one sentence -- *a relabelling of the facet set is a
    signed-permutation conjugation, hence isospectral* -- and that sentence was
    never turned on the four rows kept.  Turned on them it disqualifies NINE
    (poset, row) pairs: row I4's off-by-one is prefixes_true(rot(w)) with rot
    the cyclic rotation, so on an ANTICHAIN (L(P) = S_n, rot a bijection of it)
    the mutated facet SET is the true facet set and the mutation is a bare
    permutation conjugation -- and those three antichains are exactly row I4's
    "spectrum moved on 58 of 61" remainder.  Row I1's six are the same shape.
    So the sentence this file used to print about that remainder -- *"no claim
    is made either way"* -- pointed at precisely the pairs where the answer is
    known and adverse.  A HEDGE IS NOT AUTOMATICALLY HONEST: check what is IN
    the remainder before writing one.  There is now no remainder to hedge:
    `signed_permutation_witness` classifies every biting pair GAUGE (with an
    exhibited permutation and sign vector, reconstructed and compared) or
    NON-SIMILAR (spectral proof), the completeness is a scored row, and the
    detector has a positive control on the corruption whose answer this section
    committed to by rejecting it.  The classification is computed HERE and not
    quoted from mg-fcf1, because adopting an auditor's number instead of
    measuring it is the transmission path mg-8a12 was caught on.

    WHAT THAT DID AND DID NOT CHANGE.  It did NOT change any row's scored
    condition: the rejections are real on all 297 pairs, and a gauge pair is
    still a pair where the corrupted matrix differs from the target.  What it
    changes is what a rejection is EVIDENCE FOR -- on the nine gauge pairs it
    is not evidence that the battery can tell a construction error from a
    re-labelling -- and that is carried by the coverage line at the foot of the
    section rather than by re-scoring.  Rescoping row I4's condition remains
    deferred, for the reason recorded above it.

    WHAT THIS SECTION DOES NOT SHOW.  It tests the four sites above, on the
    posets stated in each row, and nothing wider.  It does not certify the rest
    of the construction: linear_extensions is not corrupted here (it is checked
    positively against A000112 and against Sur_iso in POSITIVE CONTROLS 2
    and 3), nor is the ideal-chain path chains_of_ideals, which claims (1)-(3)
    do not use.
    """
    print("NEGATIVE CONTROL 4 -- corrupt the INCIDENCE STRUCTURE of F(P), at four "
          "named sites (mg-2789, scoring repaired by mg-8a12, gauge standard "
          "applied to the rows kept by mg-e35b)")
    ps = [P for n in range(2, nmax + 1) for P in all_posets(n)]
    N = len(ps)
    # The third field says whether the mutation has a SINGLE named site, so that
    # its effect on L^rel can be predicted from that site alone (C4(c)).  It is a
    # statement about the shape of the mutation, not about how it scores -- what
    # scores is computed below.
    muts = [
        ("I1 a ridge's facet list (one interior ridge re-targeted onto a facet it "
         "does not meet)", "ridge_facets", True),
        ("I2 the free/interior split (one free ridge counted as interior)",
         "split_free_as_interior", True),
        ("I3 the ridge enumeration (one interior ridge missing from the complex)",
         "ridge_drop", True),
        ("I4 the facet enumeration le_to_facet (mis-indexed by one)",
         "facet_offbyone", False),
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
        for mode in ["true", "facet_swap01"] + [md for _, md, _ in muts]:
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
    # ... and the two branches of the predicate that NO pair above reaches, on
    # pairs built for them.  The table, and what each row's answer would differ
    # under, is at `UNREACHED_GATE_PAIRS` (mg-d0e2 OUTSTANDING 1, mg-04a8).
    for gate in ("shape", "parity"):
        pairs = UNREACHED_GATE_PAIRS[gate]
        agree_bf = agree_reg = at_gate = n_rej = 0
        told = []
        for why, registered, A, B in pairs:
            tr = absorb_trace(A, B)                       # the shipped predicate
            truth = absorbable_bruteforce(A, B)           # the definition, enumerated
            agree_bf += tr.absorbable == truth
            agree_reg += tr.absorbable == registered
            if not registered:
                n_rej += 1
                at_gate += tr.gate == gate                # it reached THIS branch
            told.append("%s: predicate says %s at gate '%s', brute force says %s"
                        % (why, tr.absorbable, tr.gate, truth))
        check("instrument check: the predicate's `%s` branch, which NO (poset, "
              "mutation) pair anywhere in this battery reaches, decides %d/%d "
              "constructed pairs the way BRUTE FORCE OVER ALL 2^m SIGN VECTORS "
              "does, and %d/%d agree with the answer registered beside each pair "
              "before it was run; the %d built to be REJECTED return at the `%s` "
              "gate on %d of %d.  THE EXPECTED VALUE IS DERIVED AND NOT COPIED: "
              "`absorbable_bruteforce` is the definition enumerated and shares no "
              "line with `absorb_trace`, so a stably WRONG answer fails this row "
              "-- comparing the predicate to its own previous output would not "
              "(mg-d0e2 OUTSTANDING 2).  WHY THE ROW EXISTS: over the 857 pairs "
              "the four populations of this section feed the predicate, 0 are "
              "decided at `%s`, so DELETING THAT BRANCH USED TO LEAVE THE "
              "ARTIFACT BYTE-IDENTICAL and every row green (mg-d0e2 OUTSTANDING "
              "1).  That 857 is mg-d0e2's count over the FOUR populations that "
              "existed before this row, re-derived by its own e2_parity.py and "
              "scored under d4_auditor_rerun.py -- these constructed pairs are a "
              "fifth set and are not in it.  Each pair, and what it got: %s"
              % (gate, agree_bf, len(pairs), agree_reg, len(pairs), n_rej, gate,
                 at_gate, n_rej, gate, "; ".join(told)),
              agree_bf == len(pairs) and agree_reg == len(pairs)
              and at_gate == n_rej and n_rej > 0)

    # C4(a) (mg-8a12): the corruptions are measured against an UNCORRUPTED run of
    # the same code path, and that run is a scored row rather than an assumption.
    # Without it, a pipeline that rejected everything would score four perfect
    # rows below; with it, "rejects on all of them" means something.
    n_base = sum(1 for P in ps if claim1_test(P, incidence_mode="true") is True)
    check("baseline -- with NO corruption (incidence_mode='true') the claim-(1) test "
          "does NOT reject, on %d/%d posets: every poset up to isomorphism with "
          "2 <= n <= %d.  This is the population every count below is taken over, and "
          "the reason a rejection below is a detection rather than a pipeline that "
          "rejects everything" % (n_base, N, nmax), n_base == N)

    same_target = 0
    multi_ridge = {}
    forced_rows = []
    theorem_app = theorem_diag = theorem_absorb = theorem_both = 0
    # WHICH GATE settles each absorbability answer, tallied over every biting
    # pair the section scores (mg-f1b2 F1, mg-da45).  `gate_rows` is read out in
    # the measured block below; `tot_*` carry the section-wide totals the routing
    # row now has to state.
    gate_rows = []
    tot_app = tot_shape = tot_parity = tot_sign = tot_signs_read = tot_both = 0
    # mg-e35b: the section-wide dichotomy and the vacuity split, per row, for
    # the three rows added below and for the coverage sentence.
    dich_rows = []
    tot_nonsim = tot_gauge = tot_unclassified = 0
    vac_rows = []
    for name, mode, localised in muts:
        app = rej = absorb = spec = 0
        caused = shape_ok = diag_preserved = diag_moved = residual_max = 0
        gates = {"diagonal": 0, "magnitude": 0, "parity": 0}
        mag_entries = sign_entries = 0
        signs_read = both_gates = only_mag = sign_any = 0
        vac, vac_sizes = 0, set()
        # THE GAUGE DICHOTOMY (mg-e35b, landing mg-fcf1's F2 tail) and THE TWO
        # MEANINGS OF VACUOUS (mg-fcf1's F4).  Both are computed here, in the
        # same sweep as everything else the row prints, so that the row states
        # them about its own population rather than citing an audit for them.
        nonsim = gauge = unclassified = 0
        blind = blind_set = blind_big = 0
        for P in ps:
            L_true, target = claim1_pair(P)
            L_mut, target_mut = claim1_pair(P, incidence_mode=mode)
            same_target += mat_eq(target, target_mut)
            multi_ridge[mode] = multi_ridge.get(mode, 0) + (
                top_laplacians(P, incidence_mode=mode)["n_multi_ridges"] > 0)
            if mat_eq(L_mut, L_true):
                vac += 1
                vac_sizes.add(len(linear_extensions(P)))
                # Which KIND of vacuous?  "The mutation did not apply" and "it
                # applied and the pipeline is blind to it" are different facts
                # and were printed under one word (mg-fcf1 F4).
                if mutation_applied_at_site(P, mode):
                    blind += 1
                    if mutated_facet_set_differs(P, mode):
                        blind_set += 1
                        blind_big += len(linear_extensions(P)) >= 3
                continue
            app += 1
            if not mat_eq(L_mut, target):
                rej += 1
            if absorbable_by_diagonal_twist(L_mut, target):
                absorb += 1
            # THE DICHOTOMY, classified per poset with no third bucket allowed.
            # NON-SIMILAR is a spectral PROOF (no similarity transform at all,
            # so in particular no signed permutation); GAUGE is an EXHIBITED
            # witness, reconstructed and compared.  Anything neither is
            # UNCLASSIFIED and turns the dichotomy row below red.
            if not_isospectral(L_mut, L_true):
                spec += 1
                nonsim += 1
            elif signed_permutation_witness(
                    L_true, L_mut, gauge_candidate_perms(P, mode)) is not None:
                gauge += 1
            else:
                unclassified += 1
            # C4(c): is the comparison even of the same shape, and does the
            # residual match a prediction made from the corrupted site WITHOUT
            # reading L_mut?  I.e. is this a detection or a len() accident of the
            # kind mg-5630's line F caught?  Shape is settled FIRST: on a
            # mismatch there is no residual to speak of, the row fails on
            # shape_ok, and nothing below may index into a ragged matrix.
            m = len(L_true)
            if len(L_mut) != m or any(len(L_mut[i]) != len(L_true[i])
                                      for i in range(m)):
                continue                   # counted in app, absent from shape_ok
            shape_ok += 1
            # THREE DIFFERENT QUESTIONS, ASKED SEPARATELY (mg-1c80 F1, mg-5f9a).
            # mg-da45 asked them with one function and printed the answer to one
            # as the answer to another:
            #
            #  (a) DID THE DIAGONAL MOVE?  A property of the two matrices.  It
            #      is the hypothesis of the theorem the forced rows route to
            #      (s_i^2 = 1 pins the diagonal), it holds at every n, and it
            #      says nothing about what the code tested first -- so it is
            #      asked directly, by `diagonal_moves`, and drives the routing.
            #  (b) WHERE DID THE PREDICATE RETURN?  A fact about one execution,
            #      emitted by the predicate itself.  Order-dependent: the two
            #      forced gates are interleaved by row, so this is the first
            #      gate REACHED and not the reason for the answer.
            #  (c) WHICH GATES WOULD HAVE CAUGHT IT AT ALL?  Exhaustive, so
            #      order-free.  This is what says whether (b) is load-bearing:
            #      a pair violating both gates is rejected with either deleted.
            moved = diagonal_moves(L_mut, target)               # (a)
            tr = absorb_trace(L_mut, target)                    # (b)
            gates[tr.gate] = gates.get(tr.gate, 0) + 1
            signs_read += tr.signs_read
            viol = gate_violations(L_mut, target)               # (c)
            both_gates += len(viol & {"diagonal", "magnitude"}) == 2
            only_mag += viol == frozenset(["magnitude"])
            # the sign census over EVERY same-shape pair, not just the ones
            # whose diagonal survived: the section total is printed as "anywhere"
            # and mg-1c80's F2 found it summed over 3 of the 297 (mg-5f9a).
            sign_any += entry_mismatches(L_mut, target)[1]
            if moved:
                diag_moved += 1            # the theorem's hypothesis holds here
            else:
                diag_preserved += 1        # the diagonal survived: absorbability
                dm, ds = entry_mismatches(L_mut, target)   # stays scored on these
                mag_entries += dm
                sign_entries += ds
            delta = predicted_incidence_delta(P, mode) if localised else None
            if delta is not None:
                s = [perm_sign(w) for w in linear_extensions(P)]
                pred = [[s[i] * delta[i][j] * s[j] for j in range(m)] for i in range(m)]
                obs = [[L_mut[i][j] - target[i][j] for j in range(m)] for i in range(m)]
                caused += mat_eq(pred, obs) and any(v for r_ in pred for v in r_)
            residual_max = max(residual_max, sum(
                1 for i in range(m) for j in range(m) if L_mut[i][j] != target[i][j]))
        # THE REPAIR (mg-8a12, landing mg-fcf1's F2), and the lesson it carries.
        #
        # PROVING A PROPERTY AND TESTING FOR IT ARE DIFFERENT OPERATIONS.  A
        # requirement phrased "show that X holds" will be implemented as a green
        # row when the surrounding artifact is a control battery -- which is
        # exactly what happened: mg-2789's acceptance bar said "show your
        # corruption is NOT absorbable into a parameter the battery already
        # varies", the polecat showed it, and the showing became three passing
        # control rows that no possible construction error could have turned red.
        # The mandated guard became the thing that cannot fail.  This is the
        # FOURTH generation of one defect (mg-09ea -> mg-60d3 -> mg-5630/NC3 ->
        # NC4) and the first caused by the remedy's own specification.
        #
        # So which half of this row is a measurement is DECIDED HERE, from the
        # population, rather than written in by hand: a hand-written answer is
        # the failure mode being repaired.  If the predicate could not have said
        # "absorbable" on any poset this row counts, its answer is a theorem and
        # belongs in the [CANNOT FAIL] row below, not in a scored condition.
        forced = (diag_preserved == 0)
        cond = app > 0 and rej == app and shape_ok == app
        if localised:
            cond = cond and caused == app
        if forced:
            forced_rows.append((name, mode, app, absorb))
            theorem_app += app
            theorem_diag += diag_moved     # counted, not derived: a poset whose
                                           # shape moved is verified for neither
            theorem_absorb += absorb
            theorem_both += both_gates    # how many of them the OTHER
                                          # forced gate also catches
        else:
            cond = cond and absorb == 0
        # WHAT THE VACUOUS COUNT MEANS IN THIS ROW, said in the row (mg-e35b,
        # landing mg-fcf1's F4).  The word covered two facts; which one it is
        # here is measured, not assumed, and for I4 it is the adverse one.
        vac_note = ("" if vac == 0 else
                    (" All %d vacuous posets are ones where the mutation DID NOT "
                     "APPLY -- no eligible ridge, so the corrupted build IS the "
                     "true build and there is nothing here for the pipeline to "
                     "miss (%d of %d)." % (vac, vac - blind, vac)) if blind == 0 else
                    (" AND THE VACUOUS COUNT HERE IS NOT 'THE MUTATION DID NOT "
                     "APPLY': on %d of those %d the mutation DID apply -- a "
                     "different facet enumeration was built -- and claim (1) still "
                     "holds on it, so the pipeline is BLIND to the site this row is "
                     "named after on those posets.  On %d of them the facet SET "
                     "itself differs (not merely its order), %d of those with "
                     "|L(P)| >= 3.  That is a categorically different fact from "
                     "I1/I2/I3's vacuity and was printed under the same word "
                     "(mg-fcf1 F4, landed by mg-e35b)."
                     % (blind, vac, blind_set, blind_big)))
        # WHAT THE ROW COVERS ONCE THE SECTION'S OWN GAUGE STANDARD IS APPLIED
        # TO IT (mg-e35b, landing mg-fcf1's F2 tail).
        gauge_note = (
            " GAUGE DICHOTOMY over the %d biting posets, by the SAME standard "
            "this section used to reject facet_swap01 -- a relabelling of the "
            "facet set is a signed-permutation conjugation, hence isospectral: "
            "%d NON-SIMILAR (spectral proof) + %d GAUGE (an exhibited "
            "permutation and sign vector, reconstructed and compared) + %d "
            "unclassified.%s"
            % (app, nonsim, gauge, unclassified,
               (" So this row's evidence that the corruption is not a gauge "
                "covers %d of its %d biting posets, NOT all %d: on the other %d "
                "the corrupted complex IS the true one with its facets "
                "relabelled, which is the ground facet_swap01 was rejected on.  "
                "The rejection count above is unaffected and is not restated "
                "narrower -- the test does reject there; what is narrower is "
                "what the rejection is evidence FOR, and that is the coverage "
                "line at the foot of this section." % (nonsim, app, app, gauge))
               if gauge else
               " No poset of this row is a gauge, so its coverage is its whole "
               "biting population."))
        check("%s -- the claim-(1) test rejects on %d/%d posets where the corruption "
              "changes L^rel (%d vacuous, on |L(P)| in %s); spectrum provably moved on "
              "%d of those %d.%s%s  %s  %s"
              % (name, rej, app, vac, sorted(vac_sizes), spec, app,
                 vac_note, gauge_note,
                 ("The residual equals a perturbation predicted from the corrupted "
                  "site alone on %d/%d and has at most %d nonzero entr%s on any poset, "
                  "and the compared matrices have the same shape on %d/%d: the "
                  "rejection is CAUSED by this corruption, not by a size change or a "
                  "moved count (mg-5630 line F)." % (caused, app, residual_max,
                                                     "y" if residual_max == 1 else "ies",
                                                     shape_ok, app))
                 if localised else
                 ("The mutation re-indexes the whole facet enumeration, so it has no "
                  "single site and no residual prediction is made; up to %d matrix "
                  "entries move.  Shape unchanged on %d/%d, so the rejection is not a "
                  "size mismatch." % (residual_max, shape_ok, app)),
                 ("Absorbability is NOT scored in this row: the diagonal moves on all "
                  "%d, so 'not absorbable' is forced -- see the [CANNOT FAIL] row "
                  "below (mg-8a12)." % app) if forced else
                 ("Absorbable into a diagonal +-1 twist on %d of those %d, and this "
                  "row DOES score it.  WHAT THE PREDICATE DID, reported by the "
                  "predicate itself and not by a procedure standing next to it "
                  "(mg-1c80 F1, landed by mg-5f9a): over the %d same-shape pairs it "
                  "read %d off-diagonal SIGNS in total, so no sign entered any answer "
                  "in this row.  The diagonal is preserved on %d of the %d, and of "
                  "those, %d are settled by |s_i s_j| = 1 -- and on those %d that "
                  "gate is the ONLY one violated, measured exhaustively rather than "
                  "inferred from the order, so there it is load-bearing and not "
                  "merely first: %d off-diagonal magnitudes differ on them and %d "
                  "entries differ in SIGN ALONE -- while %d reach the parity system "
                  "where a sign is consulted at all.  So 'the predicate had to decide "
                  "on the off-diagonal signs and could have returned absorbable' is "
                  "false, which is mg-f1b2's F1.  WHAT IS NOT CLAIMED HERE, because "
                  "mg-da45 claimed it and mg-1c80 refuted it: that a gate NAME "
                  "explains the other %d pairs.  Both forced gates are violated on "
                  "%d of the %d, so on those the gate a trace names is a fact about "
                  "the order the code tests in, and deleting either one leaves their "
                  "answers alone.  The clause is kept in the condition because it is "
                  "TRUE, not because it is evidence; dropping it and extending the "
                  "[CANNOT FAIL] row to this corruption is a SCORING change and is "
                  "deliberately NOT made here."
                  % (absorb, app, shape_ok, signs_read,
                     diag_preserved, app, gates["magnitude"], only_mag,
                     mag_entries, sign_entries, gates["parity"],
                     app - only_mag, both_gates, app))),
              cond)
        gate_rows.append((name.split(" ")[0], app, gates["diagonal"],
                          gates["magnitude"], gates["parity"], signs_read,
                          both_gates, diag_moved))
        dich_rows.append((name.split(" ")[0], app, nonsim, gauge, unclassified))
        vac_rows.append((name.split(" ")[0], vac, blind, blind_set, blind_big))
        tot_nonsim += nonsim
        tot_gauge += gauge
        tot_unclassified += unclassified
        tot_app += app
        tot_shape += shape_ok
        tot_parity += gates["parity"]
        tot_sign += sign_any
        tot_signs_read += signs_read
        tot_both += both_gates

    # The property removed from those rows, stated once, as what it is.  Same
    # treatment mg-1319 gave the all-+1 row: still verified, never a pass.  It is
    # emitted only if some row was in fact forced -- if a later mutation set makes
    # every absorbability answer a real decision, this row disappears rather than
    # failing, because "no theorem to report" is not a broken theorem.
    if forced_rows:
        check("PROVEN PROPERTY, not a control row -- the corruptions %s are NOT "
              "absorbable into a diagonal +-1 twist (%s), and those counts are FORCED "
              "at every n, so this is scored [CANNOT FAIL] and NOT as %d passing "
              "controls.  The argument, in two lines: (i) S.A.S = B with s_i^2 = 1 "
              "pins every diagonal entry, so a corruption that moves one can never be "
              "absorbed into a diagonal twist; (ii) each of these moves one -- %s.  "
              "Both lines are checked, not asserted: the diagonal moves on %d/%d "
              "biting posets and the predicate reports absorbable on %d, and mg-fcf1 "
              "swept every eligible ridge choice (1449/981/1459 for I1/I2/I3), not "
              "just the first one this file mutates.  A FALSE theorem is still a "
              "failure: if the diagonal stopped moving, or the predicate did report "
              "absorbable, this row FAILS.  AND WHAT LINE (i) IS NOT: a claim about "
              "which test in the code fires.  It is an implication -- moved diagonal "
              "=> not absorbable -- and the implementation realises it REDUNDANTLY, "
              "which is measured here and not argued: on %d of these %d pairs the "
              "|s_i s_j| = 1 gate is violated TOO (it runs over j == i), so deleting "
              "the s_i^2 = 1 gate from the predicate changes no answer on any of "
              "them.  mg-da45 printed a gate name as though it were this argument; "
              "the argument stands and the gate name was not evidence for it "
              "(mg-1c80 F1, mg-5f9a)"
              % (", ".join(n.split(" ")[0] for n, _, _, _ in forced_rows),
                 ", ".join("%s on %d/%d" % (n.split(" ")[0], a - ab, a)
                           for n, _, a, ab in forced_rows),
                 len(forced_rows),
                 "; ".join(DIAGONAL_MOVES.get(
                     m, "%s moves one, though no closed form for it is recorded "
                        "in DIAGONAL_MOVES" % n.split(" ")[0])
                     for n, m, _, _ in forced_rows),
                 theorem_diag, theorem_app, theorem_absorb,
                 theorem_both, theorem_app),
              theorem_absorb == 0 and theorem_diag == theorem_app,
              cannot_fail=True)

    # A POSITIVE CONTROL ON THE REPAIR ITSELF.  RELABELLING IS NOT DETECTING: a
    # repair that routed every row to [CANNOT FAIL] would look attended to and
    # cover nothing, which is worse than the defect it replaces.  So the routing
    # has to be shown to separate on this population, the same way the gauge
    # detector and the absorbability instrument are shown to separate above.
    check("routing check on the mg-8a12 repair: the MOVED-DIAGONAL split SEPARATES on "
          "this population -- %d of the %d rows have their absorbability answer forced "
          "by a moved diagonal and are stated as a theorem; on the remaining %d the "
          "diagonal survives and absorbability stays scored. "
          "If it routed every row one way it would be a relabelling of the whole "
          "section, not a decision about each row.  IT ROUTES ON `diagonal_moves`, a "
          "question about the two matrices, and NOT on which gate the predicate "
          "returned at -- those are different questions and mg-da45 asked them with "
          "one function (mg-1c80 F1, mg-5f9a).  WHAT THIS DOES NOT SHOW, and mg-8a12 "
          "printed that it did: that the answer on the row it keeps is a DECISION.  "
          "Measured over all four rows, from the predicate's own execution: it read "
          "%d off-diagonal SIGNS in total, reached the parity system on "
          "%d of the %d biting (poset, mutation) pairs, and %d entries anywhere in "
          "the %d same-shape pairs differ in sign alone.  A count of signs read is "
          "what this sentence can support; a gate name is not, because the two forced "
          "gates are interleaved by row and %d of the pairs violate BOTH"
          % (len(forced_rows), len(muts), len(muts) - len(forced_rows),
             tot_signs_read, tot_parity, tot_app, tot_sign, tot_shape, tot_both),
          0 < len(forced_rows) < len(muts))

    # THE GAUGE STANDARD, APPLIED TO THE ROWS THIS SECTION KEPT (mg-e35b,
    # landing mg-fcf1's F2 tail).  `facet_swap01` was rejected because a
    # relabelling of the facet set is a signed-permutation conjugation, hence
    # isospectral.  That standard was never asked of the four rows kept, and it
    # disqualifies 9 (poset, row) pairs of them.  It is asked here, of every
    # biting poset of every row, and the answer is required to be a DICHOTOMY
    # with no unclassified remainder -- the previous state of this section was
    # "the spectrum did not separate these and no claim is made either way",
    # which named a remainder without saying what was in it.
    check("the GAUGE/NON-SIMILAR dichotomy is COMPLETE on every row -- %d biting "
          "(poset, row) pairs = %d NON-SIMILAR + %d GAUGE + %d unclassified, per row "
          "%s.  A pair is NON-SIMILAR only on a spectral PROOF (no similarity "
          "transform of any kind, so in particular no signed permutation) and GAUGE "
          "only on an EXHIBITED witness -- a permutation and a sign vector, "
          "reconstructed in full by `signed_permutation_witness` and compared to the "
          "corrupted matrix entry by entry, so a bug in the search cannot return a "
          "false gauge.  THIS ROW CAN FAIL: a pair that neither invariant separates "
          "nor any candidate permutation realises is UNCLASSIFIED and turns it red, "
          "which is what the sentence it replaces (%s) was hiding -- mg-fcf1 settled "
          "that remainder adversely, and citing an audit for a number this file acts "
          "on is the transmission path mg-8a12 was caught by.  THE BOUND ON A "
          "NOT-GAUGE ANSWER, stated because it is the weak half: the candidate list "
          "is the identity, the relabelling the mutation itself induces when the "
          "mutated facet list is a permutation of the true one, and EVERY "
          "permutation when |L(P)| <= %d.  A GAUGE answer is a witness and needs no "
          "bound; a NOT-GAUGE answer above that size is bounded by the list -- but "
          "here every not-gauge pair is settled by the spectral proof instead, so no "
          "answer in this row rests on the bound"
          % (tot_app, tot_nonsim, tot_gauge, tot_unclassified,
             "; ".join("%s %d/%d non-similar, %d gauge" % (t, ns, a, g)
                       for t, a, ns, g, _ in dich_rows),
             "'no claim is made either way on the remainder'", PERM_BRUTE_MAX),
          tot_unclassified == 0 and tot_app > 0)

    # A POSITIVE CONTROL ON THE GAUGE DETECTOR ITSELF, on the corruption whose
    # answer this section committed to in advance by rejecting it (mg-fcf1).
    sw_g_app = sw_g_gauge = sw_g_wit = 0
    for P in ps:
        L_true, _ = claim1_pair(P)
        L_sw, _ = claim1_pair(P, incidence_mode="facet_swap01")
        if mat_eq(L_sw, L_true):
            continue
        sw_g_app += 1
        w = signed_permutation_witness(L_true, L_sw,
                                       gauge_candidate_perms(P, "facet_swap01"))
        if w is not None:
            sw_g_gauge += 1
            sw_g_wit += w[0] != list(range(len(L_true)))   # a NON-identity pi
    check("instrument check: the gauge detector says GAUGE on the corruption this "
          "section REJECTED for being one -- facet_swap01 (facets 0 and 1 exchanged) "
          "is classified GAUGE on %d/%d of the posets where it bites, and on %d of "
          "them the exhibited permutation is NOT the identity, so the answer is not "
          "the diagonal-twist question wearing a new name.  WHAT THIS ROW IS, said "
          "plainly rather than dressed as a discovery: the answer is KNOWN IN ADVANCE "
          "-- exchanging two columns conjugates L^rel by a signed permutation matrix, "
          "so a correct detector MUST say GAUGE here at every n.  It is scored for "
          "the same reason the three absorbability instrument checks above are: it "
          "fails if the detector is wrong, and on nothing else.  WHAT IT ADDS OVER "
          "THE DICHOTOMY ROW, since a row that only repeats another row's coverage is "
          "the kind of green this section keeps having to remove: a detector that "
          "NEVER says GAUGE already turns the dichotomy row RED -- those %d pairs "
          "would be unclassified, not non-similar -- so that end is policed there.  "
          "The end that is NOT policed there is a detector that says GAUGE too "
          "readily: one returning a witness for everything would make the dichotomy "
          "row green with %d gauges and no remainder.  This row pins both ends -- "
          "GAUGE on every poset of a corruption whose answer this section committed "
          "to in advance, with a NON-IDENTITY permutation each time, while saying "
          "NOT-GAUGE on %d of the %d biting pairs of the four scored rows"
          % (sw_g_gauge, sw_g_app, sw_g_wit, tot_gauge, tot_app,
             tot_app - tot_gauge, tot_app),
          sw_g_app > 0 and sw_g_gauge == sw_g_app and sw_g_wit == sw_g_app
          and tot_gauge < tot_app)

    # ---- measurements, deliberately NOT scored as PASS/FAIL rows ----------
    print("  measured, not scored:")
    m4_moves = sum(1 for P in ps
                   if not mat_eq(claim1_pair(P)[1], claim1_pair(P, normalise=True)[1]))
    m5_moves = sum(1 for P in ps
                   if not mat_eq(claim1_pair(P)[1],
                                 claim1_pair(P, perturb_edge=True)[1]))
    print("    * FORCED BY THE CODE PATH, NOT A RESULT (mg-fcf1 F3, landed by "
          "mg-e35b): the target D-A is byte-identical to the uncorrupted target on "
          "%d/%d (poset, mutation) pairs, and it COULD NOT HAVE COME OUT OTHERWISE "
          "-- `claim1_pair` builds the target with `at_laplacian(P)`, which takes no "
          "`incidence_mode` argument, so no incidence mutation can reach it at any n. "
          "The property is worth printing (all four mutations are construction-side "
          "only, unlike M4 and M5); the count is not evidence for it and was printed "
          "as though it were.  THAT THE COMPARISON ITSELF CAN COME OUT OTHERWISE is "
          "the part that needed showing, and is shown by the two mutations that DO "
          "reach the target: the same equality test finds M4 (target scaled by 2) "
          "moves it on %d/%d posets and M5 (one edge deleted) on %d/%d"
          % (same_target, 4 * N, m4_moves, N, m5_moves, N))
    print("    * no ridge lies in >= 3 facets under any of the four mutations on "
          "any of the %d posets (%s), so the corrupted complexes still satisfy "
          "the 1-or-2-facets property POSITIVE CONTROL 3 verifies: that check "
          "would not have caught these either.  READ THE FOUR ZEROS DIFFERENTLY "
          "(mg-fcf1 F3, landed by mg-e35b): three of them are FORCED and one is a "
          "measurement.  None of I1, I2, I3 ADDS an incidence -- I1 moves a ridge's "
          "second incidence from one facet to another and leaves the count at 2, I2 "
          "changes no incidence at all (only which rows are relative), I3 deletes a "
          "row -- so no ridge's facet count can rise above 2 under them at any n, and "
          "their zeros cannot come out otherwise.  I4 rebuilds the facet enumeration "
          "outright, so a ridge there CAN lie in >= 3 facets; its zero is the only "
          "one of the four that is a result"
          % (N, ", ".join("%s on %d" % (m, c) for m, c in multi_ridge.items())))
    print("    * THE TWO MEANINGS OF 'VACUOUS', separated per row and deliberately "
          "NOT scored (mg-fcf1 F4, landed by mg-e35b): %s.  A row that scored 'the "
          "split separates' would go RED the day somebody FIXED I4's blindness, "
          "which is the wrong direction for a control to point; and 'blind + "
          "did-not-apply == vacuous' is arithmetic.  So this is stated, and the "
          "adverse half is stated in row I4 itself rather than only here.  For "
          "I1/I2/I3 vacuity means only that the mutation did not apply; for I4 the "
          "mutation applies on every poset it is vacuous on, and on %d of those it "
          "builds a genuinely different FACET SET (%d of them with |L(P)| >= 3) on "
          "which claim (1) still holds -- the pipeline does not see a corrupted "
          "`le_to_facet` there at all, and that is the site NEGATIVE CONTROL 4 exists "
          "to cover"
          % ("; ".join("%s %d vacuous = %d did-not-apply + %d applied-but-unseen"
                       % (t, v, v - b, b) for t, v, b, _, _ in vac_rows),
             sum(bs for _, _, _, bs, _ in vac_rows),
             sum(bb for _, _, _, _, bb in vac_rows)))
    print("    * WHERE THE PREDICATE RETURNED, per row -- a TRACE, emitted by "
          "`absorb_trace` at the return statement that fired, not a second procedure "
          "run alongside it (mg-1c80 F1, mg-5f9a): %s.  READ THE THIRD COLUMN BEFORE "
          "QUOTING THE FIRST TWO.  The gates are not exclusive and this is the first "
          "one REACHED: the two forced tests are interleaved BY ROW inside the "
          "predicate, so the diagonal/magnitude split depends on the order and on how "
          "the rows happen to be indexed.  'both' counts pairs that violate BOTH "
          "forced gates and would be rejected with either one deleted -- on those the "
          "gate named is a fact about this execution and nothing else.  WHAT DOES NOT "
          "DEPEND ON THE ORDER, and is the number the section's claims rest on: the "
          "predicate read %d off-diagonal SIGNS in total over the %d biting (poset, "
          "mutation) pairs and reached the parity system on %d, with %d entr%s "
          "differing in sign alone across all %d same-shape pairs.  This is a "
          "MEASUREMENT and not a row: scoring 'my routing quantity is the right one' "
          "is the move that produced two generations of this defect"
          % ("; ".join("%s %d biting = %d diagonal + %d magnitude + %d parity "
                       "(both forced gates violated on %d; diagonal moved on %d; "
                       "%d signs read)"
                       % (tag, a, d, mg, pa, bo, dm, sr)
                       for tag, a, d, mg, pa, sr, bo, dm in gate_rows),
             tot_signs_read, tot_app, tot_parity,
             tot_sign, "y" if tot_sign == 1 else "ies", tot_shape))
    nc3_app = nc3_absorb = nc3_spec = nc3_parity = nc3_signs = 0
    for P in ps:
        L_true, target = claim1_pair(P)
        L_par, _ = claim1_pair(P, sign_mode="parity")
        if mat_eq(L_par, L_true):
            continue
        nc3_app += 1
        tr = absorb_trace(L_par, target)          # the predicate, instrumented
        nc3_absorb += tr.absorbable
        nc3_spec += not_isospectral(L_par, L_true)
        nc3_parity += tr.gate == "parity"
        nc3_signs += tr.signs_read
    print("    * the absorbability predicate -- which after mg-8a12 scores ONE row "
          "(I4) and is stated as a theorem for I1/I2/I3 -- applied to NEGATIVE "
          "CONTROL 3's facet-parity corruption instead, would score it FAIL: that "
          "corruption is absorbable into a diagonal +-1 twist on %d/%d of the posets "
          "where it bites and its spectrum provably moves on %d/%d. It is also the "
          "ONLY corruption anywhere in this section that reaches the parity system "
          "(%d/%d), so it is a witness that the PREDICATE can return absorbable, and "
          "it is the gauge this section exists to get past (mg-5630). IT IS NOT A "
          "WITNESS THAT ROW I4 IS FALSIFIABLE, and mg-8a12 printed that it was "
          "(mg-f1b2 F1, corrected by mg-da45): NC3's corruption is D.L.D by "
          "construction, so its magnitudes ARE the target's and a sign is what is "
          "left to decide, while row I4's magnitudes differ on every poset where its "
          "diagonal survives. SAID AS THE PREDICATE'S OWN EXECUTION REPORTS IT rather "
          "than as a gate name (mg-1c80 F1, mg-5f9a): here it READ %d off-diagonal "
          "signs, and over the whole of NEGATIVE CONTROL 4 it read %d. That is the "
          "separation -- not that the two are 'settled at different gates', which "
          "depends on the order the gates are tested in. It is NOT a witness for "
          "I1/I2/I3 either: no witness exists there, which is the point of the "
          "[CANNOT FAIL] row."
          % (nc3_absorb, nc3_app, nc3_spec, nc3_app, nc3_parity, nc3_app,
             nc3_signs, tot_signs_read))
    for name, mode, _ in muts:
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
          "in le_to_facet, whose spectrum moves on %d of the %d posets where it "
          "bites -- NOT on all of them: mg-2789 wrote 'whose spectrum does move' and "
          "that is false as written (mg-fcf1 F1). On the 3 antichains the off-by-one "
          "is prefixes_true(rot(w)), rot maps L(P) = S_n onto itself, and the "
          "mutation is a bare permutation conjugation -- the same gauge, now "
          "classified as one by THIS FILE'S detector and not on the audit's word "
          "(mg-e35b). AND THE SAME QUESTION IS NOW ASKED OF EVERY ROW rather than "
          "only of the candidate rejected: it disqualifies %d (poset, row) pairs of "
          "the four kept, which is the dichotomy row above."
          % (sw_app, N, sw_absorb, sw_app, sw_spec, sw_app,
             dich_rows[3][2], dich_rows[3][1], tot_gauge))
    print("    * WHERE A ROW REPORTS THE SPECTRUM MOVING ON FEWER THAN ALL OF ITS "
          "BITING POSETS, WHAT IS IN THE REMAINDER IS NOW STATED (mg-fcf1 F1/F2, "
          "landed by mg-e35b). This file used to print 'no claim is made either way "
          "on the remainder' -- honest-looking, and it covered exactly the %d pairs "
          "where the answer is known and ADVERSE: every one of them is a "
          "signed-permutation conjugate, i.e. a GAUGE, which is the ground this "
          "section rejected facet_swap01 on. A hedge is not automatically honest; "
          "check what is IN the remainder before writing one. The spectral "
          "invariants used here (the trace, the sum of squared entries and "
          "det(. - k.I) mod (2^31-1) for k in {3,5,7,11,13}) still do not separate "
          "those pairs -- that limit is real and unchanged -- but the pairs are no "
          "longer unclassified: the dichotomy row above settles each of them with an "
          "exhibited witness. Non-isospectrality remains the stronger one-sided "
          "extra; the diagonal-twist decision is exact on every pair either way."
          % tot_gauge)
    print("    * COVERAGE AT `le_to_facet`, SIZED (mg-fcf1 F5, landed by mg-e35b). "
          "mg-2789's commit message said this section 'closes the gap mg-5630 "
          "relocated'; a commit message cannot be edited, so the correct sizing is "
          "printed HERE. STATE.md already carries the qualitative half of the "
          "correction ('relocation, not closure') and is pm-onethird's ledger: the "
          "numbers below are routed to them rather than written into it from this "
          "file, which is the same choice mg-2789 made about the Probe.md passage it "
          "flagged and did not edit. The named load-bearing site is "
          "corrupted on %d/%d posets, the corruption reaches L^rel on %d of them, "
          "and of those %d are NON-SIMILAR and %d are a GAUGE -- so coverage at "
          "`le_to_facet` is %d/%d, of which %d carry evidence that a construction "
          "error is distinguishable from a re-labelling. On the remaining %d the "
          "pipeline does not see the corruption at all. ACROSS THE SECTION: %d of "
          "the four rows still SCORES its absorbability answer as a measurement and "
          "the other %d have it removed to the [CANNOT FAIL] row as a theorem, and "
          "%d (poset, row) pairs of the four are gauges. That is a relocation of the "
          "gap, narrower than before and not closed."
          % (N, N, dich_rows[3][1], dich_rows[3][2], dich_rows[3][3],
             dich_rows[3][1], N, dich_rows[3][2], N - dich_rows[3][1],
             len(muts) - len(forced_rows), len(forced_rows), tot_gauge))
    print("    * row scoring, and who owns it: every row above is vacuous on the "
          "sub-population named in it, exactly as NEGATIVE CONTROL 2's M1-M5 are, "
          "and the scoring does not model vacuity -- only the [CANNOT FAIL] label, "
          "which mg-1319 landed and OWNS (see SCORING at the top of this file). "
          "mg-2789 printed here that it 'added no [CANNOT FAIL] row: each of the "
          "four rows above fails if its corruption stops biting or turns out "
          "absorbable'. THAT WAS FALSE, and this is the correction (mg-8a12, landing "
          "mg-fcf1 F2). For I1, I2 and I3 neither failure mode was reachable: the "
          "diagonal moves, so the corruption cannot stop biting AND cannot be "
          "absorbable, both by arithmetic at every n. Three of the four rows were "
          "[CANNOT FAIL] rows scored as passes, under a battery whose own SCORING "
          "section forbids exactly that. What now stands scored is the half that can "
          "fail: that each corruption reaches the population at all, and that the "
          "rejection is caused by the corruption (residual == prediction). The "
          "unreachable half is stated once, as a theorem, in the [CANNOT FAIL] row. "
          "AND THE ABSORBABILITY ANSWER WAS FORCED ON ALL FOUR, NOT THREE (mg-f1b2 "
          "F1, corrected by mg-da45): on all four the predicate answered without "
          "reading a single off-diagonal sign, which the trace above counts. mg-da45 "
          "said this as 'three at the diagonal gate and I4 at the absolute-value "
          "gate'; THAT SENTENCE IS WITHDRAWN (mg-1c80 F1, mg-5f9a) -- it named a gate "
          "per row, the naming came from a procedure that tested the gates in an "
          "order the predicate does not use, and on I1 the predicate's own order "
          "gives 15 diagonal + 57 magnitude and not 72 + 0. What was true in it is "
          "the word FORCED, and that is now carried by the sign count. mg-8a12 removed the "
          "clause from the three; row I4 still carries a forced clause in a scored "
          "condition and now SAYS SO in its own row rather than claiming the "
          "off-diagonal signs decide it. Removing it -- and with it the reason this "
          "section's routing exists -- is a scoring change and is left to its own "
          "item. The lines in this block are measurements, not rows, and are "
          "deliberately unscored.")


def artifact_banner_check():
    """Nothing this run prints may carry the all-pass banner except the bottom line.

    Added by mg-f2e1 from the mg-f7bc audit's F5.  The A4 scoring repair
    (mg-1319) suppressed the banner in the BOTTOM LINE and then emitted it twice
    in `scoring_self_test`'s row names, on [PASS]-prefixed lines four lines from
    the top of `controls_output.txt`, above a bottom line reading "...is NOT 'all
    controls pass'".  Pre-repair the string occurred exactly once in the
    artifact, as the true bottom line; after the repair a grep for it returned
    two false positives first.

    WIDENED FROM ROW NAMES TO THE BYTE STREAM (mg-7d5a, from mg-6653's A2).  As
    mg-f2e1 wrote it this scanned `ROW_NAMES` only, while its own docstring
    concluded that it "makes the artifact's occurrences of the banner exactly
    the bottom line's".  It did not, and mg-6653 CONSTRUCTED the false positive
    twice with the check in place: ATTACK B put the banner in a `detail=` string
    (printed on the SAME line as the row name, behind the same [PASS] prefix, so
    a grep cannot tell them apart) and ATTACK C printed it as a bare section
    heading.  Both reached the artifact with the check reporting "offending
    rows: none" and the battery exiting 0 -- the F5 defect in full, one
    generation on, inside the control built to remove it.  It now scans every
    line `ArtifactTee` has recorded, which is every line of the artifact.

    Scoped exactly, and this is what it now buys.  (a) It reads the lines
    written BEFORE it runs.  Everything after it is `summarise`'s bottom line,
    which is the one place the banner is licensed -- so "the artifact's
    occurrences of the banner are exactly the bottom line's" is now the property
    enforced rather than the property claimed.  (b) It scans for the exact
    17-character literal, case-sensitive: a row name carrying the banner with a
    doubled space is not detected and should not be (mg-6653's ATTACK D fixes
    that boundary).  (c) It says nothing about this FILE's prose, which never
    reaches the artifact, nor about text a caller appends to
    `controls_output.txt` outside the `tee`.

    It remains a control and not a proven property: mg-6653's ATTACKS A, B and C
    each make it FAIL and exit 1.  If it is ever narrowed to a scope where no
    constructible mutation can trip it, the SCORING section above applies and it
    must be re-scored [CANNOT FAIL].

    The offender report MASKS the banner rather than quoting it.  A control that
    printed the offending text verbatim would put the string back into the
    artifact on precisely the run that objects to it, which is the defect one
    level up.
    """
    print("CONTROL ON THE ARTIFACT -- nothing above the bottom line may carry the banner")
    banner = "ALL CONTROLS PASS"
    mask = "<all-pass-banner>"
    scanned = ARTIFACT.lines_so_far() if ARTIFACT is not None else list(ROW_NAMES)
    offenders = ["line %d: %s" % (i + 1, line.strip().replace(banner, mask))
                 for i, line in enumerate(scanned) if banner in line]
    check("no line this run printed carries the %d-char all-pass banner literal, "
          "and in particular no control row's own text contains it" % len(banner),
          not offenders,
          "lines scanned: %d (the whole artifact above this row; %d row names "
          "among them); offending lines: %s (banner masked as %s)"
          % (len(scanned), len(ROW_NAMES), offenders if offenders else "none", mask))


def main():
    global ARTIFACT
    # Everything below this line is the artifact; `artifact_banner_check` reads
    # it back.  Installed here rather than at import so that importing this
    # module for its functions does not hijack stdout.
    ARTIFACT = ArtifactTee(sys.stdout)
    sys.stdout = ARTIFACT
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
    artifact_banner_check()
    print()
    lines, code = summarise(FAIL, CANNOT_FAIL)
    for line in lines:
        print(line)
    if code:
        sys.exit(code)


if __name__ == "__main__":
    main()
