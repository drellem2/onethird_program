#!/usr/bin/env python3
"""Independent verification of the mg-e35b repair to NEGATIVE CONTROL 4.

mg-e35b lands the remaining OPEN items of mg-fcf1's audit of mg-2789 -- the
gauge standard applied to the rows KEPT (F1/F2 tail), the two printed
tautologies (F3), the two meanings of "vacuous" (F4), the coverage sizing (F5)
and the "CI-adjacent" minor.  Every number that repair prints is re-derived
here by a route that shares no line with it, and every number is asked the
question mg-fcf1 said to ask of a repair of this kind:

    COULD THIS COUNT HAVE COME OUT DIFFERENTLY?

The answer is printed for each one in section V6, including the answers that
are NO -- a count that cannot come out otherwise is not evidence, and this
instrument's job is to say which of the repair's counts are which rather than
to let a green row imply they all are.

Route disjointness, stated exactly.  This file imports the FACE COMPLEX
(`top_laplacians`, `linear_extensions`, `le_to_facet`, `le_to_facet_offbyone`,
`at_laplacian`, `not_isospectral`) because re-implementing the object under
test would verify a different object.  It does NOT import
`signed_permutation_witness`, `permute_matrix`, `gauge_candidate_perms`,
`mutation_applied_at_site` or `mutated_facet_set_differs` -- the five things
mg-e35b added -- and rebuilds each of them below.  Where a claim is about the
SOURCE rather than about the mathematics (V4a), it is checked against the
source text by `ast`, not by running it.

V6 AND V7 WERE REPAIRED BY mg-8af0, landing mg-fcb2's F2.  V6's completeness
row used to score `forced == 3 and len(table) == 11` against the literal
`table` twenty lines above it: a row whose verdict was a function of a list in
this file, that had never been shown capable of reporting anything else, and
under which a twelfth count added to the artifact stayed GREEN.  That is why
mg-fcb2's F1 survived a table headed "EVERY COUNT THIS REPAIR PRINTS".  V6 now
derives its population from the SOURCE of `negative_control_incidence` and
scores coverage of it; V7 flips each of V6's three verdicts on a constructed
input, because a control nobody has seen fail is not evidence.

Exit 0 iff every check passes.
"""

import ast
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROBE = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
sys.path.insert(0, PROBE)

from face_complex import (                                       # noqa: E402
    linear_extensions, le_to_facet, le_to_facet_offbyone, top_laplacians,
    at_laplacian, twist, perm_sign, mat_eq, not_isospectral,
)
from posets import all_posets                                    # noqa: E402

NMAX = 5
MODES = ["ridge_facets", "split_free_as_interior", "ridge_drop",
         "facet_offbyone", "facet_swap01"]
TAGS = {"ridge_facets": "I1", "split_free_as_interior": "I2",
        "ridge_drop": "I3", "facet_offbyone": "I4",
        "facet_swap01": "swap01"}

FAILED = []
CHECKS = [0]


def check(label, ok, detail=""):
    CHECKS[0] += 1
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  -- " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)
    return ok


# ---------------------------------------------------------------------------
# The pair claim (1) asserts equal, rebuilt here rather than imported from
# controls.py, so that a change to controls.py's own plumbing cannot make this
# file agree with it by construction.
# ---------------------------------------------------------------------------
def pair(P, mode="true"):
    td = top_laplacians(P, incidence_mode=mode)
    les = td["les"]
    s = [perm_sign(w) for w in les]
    L = td["L_rel"]
    L = [[s[i] * L[i][j] * s[j] for j in range(len(les))] for i in range(len(les))]
    _, target = at_laplacian(P)
    return L, target


# ---------------------------------------------------------------------------
# V1.  The gauge witness, re-implemented.  Independent of
# `signed_permutation_witness`: this one solves the sign system by GAUSSIAN
# ELIMINATION OVER GF(2) on the exponents rather than by a BFS, and it verifies
# by reconstruction, so a propagation bug in either implementation shows up as
# a disagreement rather than as two matching wrong answers.
# ---------------------------------------------------------------------------
def witness_gf2(A, B, pi):
    """(pi, s) with s_i s_j A[pi[i]][pi[j]] == B[i][j], or None."""
    m = len(A)
    M = [[A[pi[i]][pi[j]] for j in range(m)] for i in range(m)]
    if any(M[i][i] != B[i][i] for i in range(m)):
        return None
    if any(abs(M[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return None
    # x_i in GF(2) with s_i = (-1)^x_i.  Each off-diagonal constraint is
    # x_i + x_j = b, b = 0 if the signs agree and 1 if they differ.
    rows = []
    for i in range(m):
        for j in range(m):
            if i == j or M[i][j] == 0:
                continue
            b = 0 if B[i][j] == M[i][j] else 1
            v = (1 << i) | (1 << j)
            rows.append((v, b))
    basis = {}                       # pivot bit -> (vector, rhs)
    for v, b in rows:
        while v:
            p = v.bit_length() - 1
            if p not in basis:
                basis[p] = (v, b)
                break
            bv, bb = basis[p]
            v ^= bv
            b ^= bb
        else:
            if b:
                return None          # 0 = 1: inconsistent
    # Back-substitution in INCREASING pivot order.  A basis row's pivot is its
    # HIGHEST set bit, so every other variable in that row is lower and must
    # already be decided; taking the pivots in decreasing order instead reads
    # those as 0 and silently returns "no solution" on solvable systems.  It
    # did: the first version of this file reported swap01 as 10 gauge and 62
    # unclassified against controls.py's 72, and disagreed with brute force on
    # 3 of 86 small pairs.  That is the disagreement this second route exists
    # to produce -- recorded rather than quietly corrected, because a
    # cross-check that has never once disagreed is not evidence that it could.
    x = 0
    for p in sorted(basis):
        v, b = basis[p]
        if bin(v & x).count("1") % 2 != b:
            x |= (1 << p)
    s = [-1 if (x >> i) & 1 else 1 for i in range(m)]
    rebuilt = [[s[i] * M[i][j] * s[j] for j in range(m)] for i in range(m)]
    return (list(pi), s) if mat_eq(rebuilt, B) else None


def candidates(P, mode, brute_max=6):
    les = linear_extensions(P)
    m = len(les)
    out = [list(range(m))]
    true_f = [le_to_facet(w) for w in les]
    mut_f = [le_to_facet_offbyone(w) for w in les] if mode == "facet_offbyone" \
        else list(true_f)
    if mode == "facet_swap01" and m >= 2:
        mut_f[0], mut_f[1] = mut_f[1], mut_f[0]
    if sorted(mut_f) == sorted(true_f):
        idx = {f: i for i, f in enumerate(true_f)}
        ind = [idx[f] for f in mut_f]
        if ind not in out:
            out.append(ind)
    if m <= brute_max:
        out.extend(list(p) for p in itertools.permutations(range(m)))
    return out


def gauge(P, mode):
    L_true, _ = pair(P)
    L_mut, _ = pair(P, mode)
    for pi in candidates(P, mode):
        w = witness_gf2(L_true, L_mut, pi)
        if w is not None:
            return w
    return None


def brute_signed_perm(A, B):
    """Exhaustive over ALL permutations and ALL sign vectors -- the definition.
    Only usable at tiny sizes; used in V2 as the ground truth."""
    m = len(A)
    for pi in itertools.permutations(range(m)):
        M = [[A[pi[i]][pi[j]] for j in range(m)] for i in range(m)]
        for bits in range(1 << m):
            s = [-1 if (bits >> i) & 1 else 1 for i in range(m)]
            if all(s[i] * M[i][j] * s[j] == B[i][j]
                   for i in range(m) for j in range(m)):
                return True
    return False


# ---------------------------------------------------------------------------
# THE POPULATION OF PRINTED COUNTS, DERIVED FROM THE SECTION'S SOURCE
# (mg-8af0, landing mg-fcb2's F2).
#
# WHAT WAS WRONG.  V6 used to score `forced == 3 and len(table) == 11`, where
# `table` was the list of string literals defined twenty lines above it.  Both
# operands were functions of that literal alone; nothing in the condition, and
# nothing anywhere else in this file, opened `controls.py` to find out what the
# section actually prints.  So the row reported the same verdict whatever the
# input, and had never been shown capable of reporting anything else.  Adding a
# twelfth printed count to the artifact and leaving this file untouched left it
# GREEN -- which is why mg-fcb2's F1 (`the named load-bearing site is corrupted
# on %d/%d posets`, filled `(N, N)`) survived a table headed "EVERY COUNT THIS
# REPAIR PRINTS".  The count is simply absent from the list.
#
# A ROW THAT SCORES A LITERAL IS NOT A WEAK CONTROL, IT IS NOT A CONTROL.  The
# repair is therefore not "replace the literal with a computation" but "score
# coverage of a population the section itself defines", and every verdict below
# is accompanied in V7 by a constructed input that FLIPS it.
#
#   POPULATION  every `%`-formatting expression carrying at least one `%d`
#               conversion, lexically inside `negative_control_incidence` in
#               `code/face_geometry/controls.py`.  That is the whole section --
#               a wider population than "the lines mg-e35b touched", chosen
#               because the next count will not land only where the last one
#               did.  A `%` nested inside another site's argument tuple is a
#               separate member (the per-row sub-templates are members).
#   GRAIN       one member per `%`-BinOp, NOT per `%d`.  One sentence may carry
#               twelve figures and is classified once.  Each row of the table
#               below declares its site's `%d` count as part of its key, so
#               ADDING A FIGURE TO AN EXISTING SENTENCE breaks the match too.
# ---------------------------------------------------------------------------
CONV_RE = re.compile(r"%[-+ #0]*[0-9]*(?:\.[0-9]+)?([diouxXeEfFgGcrsa%])")


def conversions(fmt):
    """(start, end, type) of each conversion in `fmt`, in order, less `%%`."""
    return [(m.start(), m.end(), m.group(1)) for m in CONV_RE.finditer(fmt)
            if m.group(1) != "%"]


def count_sites(src, func="negative_control_incidence"):
    """The population defined above, read out of `src` by `ast`."""
    fn = next(f for f in ast.walk(ast.parse(src))
              if isinstance(f, ast.FunctionDef) and f.name == func)
    sites = []
    for node in ast.walk(fn):
        if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod)):
            continue
        try:
            fmt = ast.literal_eval(node.left)
        except Exception:
            continue                     # a runtime `%`, not a format literal
        if not isinstance(fmt, str):
            continue
        convs = conversions(fmt)
        if not any(c == "d" for _, _, c in convs):
            continue
        right = node.right
        args = [ast.unparse(e) for e in right.elts] \
            if isinstance(right, ast.Tuple) else [ast.unparse(right)]
        sites.append({"line": node.lineno, "fmt": fmt, "convs": convs,
                      "args": args, "nd": sum(1 for _, _, c in convs if c == "d")})
    sites.sort(key=lambda s: (s["line"], s["nd"]))
    for i, s in enumerate(sites):
        s["idx"] = i
    return sites


def same_expression_ratios(site):
    """Figures of the form `X/Y` in one site whose two halves are filled by THE
    SAME EXPRESSION -- the structural shape of mg-fcb2's F1.

    A SOURCE property, not an output one: plenty of honest ratios read `k/k` on
    a given population (`facet_swap01` is GAUGE on 72/72 and that row can go
    red).  What separates a measurement from a tautology is whether the two
    halves CAN differ, and that is a fact about the code path.
    """
    convs, args = site["convs"], site["args"]
    if len(convs) != len(args):
        return []                        # a `*` width or a mapping key: not scanned
    hits = []
    for i in range(len(convs) - 1):
        if convs[i][2] != "d" or convs[i + 1][2] != "d":
            continue
        if site["fmt"][convs[i][1]:convs[i + 1][0]] != "/":
            continue
        if args[i] == args[i + 1]:
            hits.append((i, args[i]))
    return hits


def claim_population(sites, rows):
    """Match the table's (anchor, %d-count) keys against the population.

    Returns (matches, ambiguous, unclaimed, contested).  `ambiguous` is a row
    matching zero or several sites; `unclaimed` a site no row matches;
    `contested` a site two rows match.  All three are failures, and all three
    are flipped on a constructed input in V7.
    """
    matches, claimed = {}, {}
    for anchor, nd, _, _ in rows:
        got = [s for s in sites if s["nd"] == nd and anchor in s["fmt"]]
        matches[(anchor, nd)] = got
        for s in got:
            claimed.setdefault(s["idx"], []).append(anchor)
    ambiguous = [k for k, v in matches.items() if len(v) != 1]
    unclaimed = [s for s in sites if s["idx"] not in claimed]
    contested = [s for s in sites if len(claimed.get(s["idx"], [])) > 1]
    return matches, ambiguous, unclaimed, contested


# -- the three constructed sources V7 uses, all built by AST so that none of
# -- them depends on the exact text of a line that a later repair may move ----
def inject_extra_count(src, func="negative_control_incidence"):
    """mg-fcb2's F2 demonstration, pointed at the repair: a TWELFTH printed
    count added to the section with this file left untouched."""
    tree = ast.parse(src)
    fn = next(f for f in ast.walk(tree)
              if isinstance(f, ast.FunctionDef) and f.name == func)
    fn.body.extend(ast.parse(
        'print("a count added to the artifact and not to the verifier: '
        '%d/%d" % (len(ps), N))').body)
    return ast.unparse(tree)


def delete_statement(src, anchor, func="negative_control_incidence"):
    """Drop the top-level statement of `func` whose text carries `anchor`."""
    tree = ast.parse(src)
    fn = next(f for f in ast.walk(tree)
              if isinstance(f, ast.FunctionDef) and f.name == func)
    keep = [st for st in fn.body
            if not any(isinstance(n, ast.Constant) and isinstance(n.value, str)
                       and anchor in n.value for n in ast.walk(st))]
    assert len(keep) == len(fn.body) - 1, "expected exactly one statement"
    fn.body = keep
    return ast.unparse(tree)


def make_ratio_tautological(src, anchor, func="negative_control_incidence"):
    """Rewrite the site carrying `anchor` so its first argument becomes the
    same expression as its second -- mg-fcb2's F1 shape, reconstructed."""
    tree = ast.parse(src)
    fn = next(f for f in ast.walk(tree)
              if isinstance(f, ast.FunctionDef) and f.name == func)
    for node in ast.walk(fn):
        if not (isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod)):
            continue
        try:
            fmt = ast.literal_eval(node.left)
        except Exception:
            continue
        if isinstance(fmt, str) and anchor in fmt and isinstance(node.right, ast.Tuple):
            node.right.elts[0] = ast.parse(ast.unparse(node.right.elts[1]),
                                           mode="eval").body
            return ast.unparse(tree)
    raise AssertionError("no site carries %r" % anchor)


# ---------------------------------------------------------------------------
# THE CLASSIFICATION.  (anchor, `%d` count, verdict, why).
#
# The verdicts are judgements and are written here; WHAT IS NOT WRITTEN HERE is
# the population they must cover, which is read out of `controls.py` above.
# That is the whole of mg-fcb2's F2: the old table was BOTH the list and the
# thing the list was scored against.
#
# The `%d` count is part of the key on purpose.  A site's anchor identifies the
# sentence; its figure count identifies how much of the sentence this row is
# taking responsibility for.  Add a figure to an existing sentence and the key
# stops matching, which is the hole a by-sentence-only key would leave.
#
# A site may carry figures of both kinds -- one sentence, twelve figures, not
# all of them the same sort of thing.  Those are MIXED and the `why` says which
# figure is which.  Pretending a sentence has one verdict because the table has
# one column is how "its zero is the only one of the four that is a result"
# got printed (mg-fcb2's F3).
# ---------------------------------------------------------------------------
V6_ROWS = [
    ("a genuine diagonal +-1 conjugation of L^rel is reported absorbable on", 2,
     "COULD MOVE",
     "`yes` is a sum over the population; a predicate that answered NOT "
     "absorbable on a genuine conjugation lowers it.  This is the positive half "
     "of an instrument check and exists in order to be capable of failing."),
    ("L^rel with one diagonal entry moved by 1 is reported NOT absorbable", 2,
     "COULD MOVE",
     "the negative half of the same instrument check; a predicate that accepted "
     "everything prints 0/86 here."),
    ("the union-find absorbability decision agrees with brute force", 2,
     "COULD MOVE",
     "`agree < cases` the moment the decision procedure and the enumeration of "
     "all 2^m sign vectors disagree on any one pair."),
    ("which NO (poset, mutation) pair anywhere in this battery reaches", 7,
     "COULD MOVE",
     "the constructed pairs for the unreached branch: `agree_bf` and "
     "`agree_reg` are compared against `absorbable_bruteforce` and against an "
     "answer registered before the run, and either can come out short."),
    ("baseline -- with NO corruption", 3, "MIXED",
     "`n_base` is a sum over the uncorrupted pipeline and moves the day it "
     "rejects anything uncorrupted -- COULD MOVE, and it is the row every "
     "rejection below depends on.  THE THIRD FIGURE IS NOT A COUNT AT ALL: "
     "`nmax` echoes the command-line argument.  Population: none; grain: the "
     "input."),
    ("vacuous posets are ones where the mutation DID NOT", 3,
     "FORCED BY THE BRANCH GUARD",
     "NOT IN mg-e35b'S TABLE AT ALL, and found by deriving this population "
     "rather than by reading the artifact (mg-8af0 OPEN 1).  The sentence is "
     "printed only when `blind == 0`, and its parenthetical is filled "
     "`(vac - blind, vac)`: inside that branch the two are equal by arithmetic, "
     "so `(%d of %d)` can only ever print `(k of k)`.  The structural scan does "
     "NOT flag it -- the two expressions differ, and only their VALUES are "
     "forced -- so it is a second species of the F1 defect and is recorded, not "
     "quietly rewritten."),
    ("AND THE VACUOUS COUNT HERE IS NOT", 4, "COULD MOVE",
     "`blind`, `blind_set` and `blind_big` are three independent sums over "
     "I4's vacuous posets; all three fall the day I4's blindness is fixed, "
     "which is the direction this measurement is pointed."),
    ("GAUGE DICHOTOMY over the", 4, "COULD MOVE",
     "`app`, `nonsim`, `gauge`, `unclassified` are per-row decisions and differ "
     "by row (I1 72/66/6/0 against I4 61/58/3/0); an unclassified pair is "
     "reachable and turns the row red."),
    ("So this row's evidence that the corruption is not a gauge covers", 4,
     "COULD MOVE",
     "printed only where `gauge > 0`, and `nonsim < app` exactly there; the "
     "figures are the same per-row decisions as the site above."),
    ("the claim-(1) test rejects on", 5, "COULD MOVE",
     "the row line itself: `rej`, `app`, `vac` and `spec` all differ by row, and "
     "`rej == app` is half of what the row scores."),
    ("The residual equals a perturbation predicted from the corrupted site alone",
     5, "COULD MOVE",
     "`caused == app` is the scored half of I1/I2/I3; a residual that failed to "
     "match the perturbation predicted from the named site lowers it."),
    ("The mutation re-indexes the whole facet enumeration", 3, "COULD MOVE",
     "I4's branch of the same clause; `residual_max` and `shape_ok` are "
     "measured over its biting population."),
    ("Absorbability is NOT scored in this row", 1, "COULD MOVE",
     "`app`, the row's biting population, which is a measurement -- what is "
     "forced here is the ANSWER, and mg-8a12 moved that to the [CANNOT FAIL] "
     "row rather than leaving it scored."),
    ("and this row DOES score it.", 14, "MIXED",
     "I4's surviving scored clause.  `absorb == 0` COULD MOVE and is scored.  "
     "`signs_read` is a trace of what the predicate read and is a measurement.  "
     "The `|s_i s_j| = 1` clause is FORCED on the 3 posets where I4's diagonal "
     "survives (mg-f1b2 F1) and the row says so in its own text; removing it is "
     "a scoring change deferred by mg-e35b to its own item and NOT made here."),
    ("PROVEN PROPERTY, not a control row", 6, "MIXED",
     "the [CANNOT FAIL] row.  `len(forced_rows)` COULD MOVE -- mg-8a12 decides "
     "it from the population by `forced = (diag_preserved == 0)`, so a mutation "
     "whose diagonal survives leaves its row scored.  The absorbability figures "
     "it reports are FORCED and that is the row's entire point."),
    ("%s on %d/%d", 2, "COULD MOVE",
     "the per-row `not absorbable on a - ab of a` sub-template of the "
     "[CANNOT FAIL] row; `a - ab` and `a` are different expressions and the "
     "difference is what the row would report if the theorem failed."),
    ("routing check on the mg-8a12 repair", 9, "COULD MOVE",
     "`0 < len(forced_rows) < len(muts)` is the scored condition and BOTH "
     "bounds are reachable: a battery whose mutations all moved the diagonal "
     "would route every row to the theorem and turn it red."),
    ("the GAUGE/NON-SIMILAR dichotomy is COMPLETE on every row", 5, "COULD MOVE",
     "an unclassified pair turns the row red; the 9 is a per-poset decision and "
     "differs by row (6/0/0/3).  Re-derived in V1 by a route sharing no line "
     "with it."),
    ("non-similar, %d gauge", 3, "COULD MOVE",
     "the per-row sub-template of the dichotomy total above."),
    ("the gauge detector says GAUGE on the corruption this section REJECTED", 7,
     "MIXED",
     "`sw_g_gauge == sw_g_app` is FORCED BY MATHEMATICS -- exchanging two "
     "columns IS a signed-permutation conjugation -- and the row is an "
     "instrument check that says so, failing only if the detector is wrong.  "
     "`sw_g_wit`, the count with a NON-IDENTITY witness, COULD MOVE: a detector "
     "answering by diagonal twist alone prints 0.  mg-fcb2's F4: the `why` "
     "mg-e35b printed for the NOT-GAUGE figure -- `a detector that accepted "
     "everything would print 297` -- IS FALSE, and mg-fcb2 showed the "
     "substitution REACHED (297 calls) and still printing 288, because the "
     "binning is `if not_isospectral: ... elif witness:` and the 288 spectrally "
     "separated pairs never reach the detector.  The figure still moves; the "
     "population moves it.  Corrected here and nowhere else in F4's scope."),
    ("FORCED BY THE CODE PATH, NOT A RESULT", 6, "MIXED",
     "`same_target == 4 * N` is FORCED BY THE CODE PATH -- `at_laplacian` takes "
     "no `incidence_mode` argument, checked from the AST in V4a -- and the "
     "section prints it as a property.  The four figures after it (M4 and M5 "
     "moving the target on 82/86) COULD MOVE and are what shows the comparison "
     "itself is capable of moving; the 4 posets with |L(P)| = 1 have an empty "
     "target that scaling cannot move."),
    ("no ridge lies in >= 3 facets under any of the four mutations", 1, "MIXED",
     "THE FIGURE IN THIS SENTENCE IS NOT A COUNT: it is `N`, the population "
     "size, echoed.  The four zeros the sentence is about are printed by the "
     "sub-template below and are classified there."),
    ("%s on %d", 1, "FORCED BY THE CHAIN STRUCTURE OF BOTH FACET MAPS",
     "the four per-mode `>= 3 facets` zeros.  mg-e35b called three of them "
     "FORCED and I4's `a result`; ALL FOUR ARE FORCED (mg-fcb2's F3).  Both "
     "`le_to_facet` and `le_to_facet_offbyone` return a chain of masks of sizes "
     "1, 2, ..., n-1, so a ridge omits the level-k mask and the two masks "
     "bracketing it differ in exactly two elements -- exactly two candidates to "
     "re-insert, hence at most two facets on any ridge, at every n, under "
     "either map.  Measured in V4b over every poset with n <= 6 under both "
     "maps."),
    ("THE TWO MEANINGS OF 'VACUOUS'", 2, "COULD MOVE",
     "the two totals sum the per-row blindness; a mutation that applied and "
     "left L^rel fixed lands in the other column.  Deliberately not scored by "
     "the section, for the reason its own text gives."),
    ("vacuous = %d did-not-apply", 3, "COULD MOVE",
     "the per-row sub-template of the vacuity split; I1/I2/I3 print 14/4/4 "
     "did-not-apply and I4 prints 0 + 25, which is the whole point of the "
     "separation."),
    ("WHERE THE PREDICATE RETURNED, per row", 5, "COULD MOVE",
     "the gate trace, emitted by `absorb_trace` at the return that fired; the "
     "totals move with the population and with the order the gates are tested "
     "in, which is why the section warns against reading a gate NAME as a "
     "cause."),
    ("biting = %d diagonal + %d magnitude", 7, "COULD MOVE",
     "the per-row sub-template of the trace above."),
    ("applied to NEGATIVE CONTROL 3's facet-parity corruption instead", 8,
     "MIXED",
     "`nc3_absorb == nc3_app` and `nc3_spec == 0` are FORCED BY MATHEMATICS: "
     "NC3's corruption is D.L.D by construction, hence absorbable and "
     "isospectral, and this line exists to say so.  `nc3_parity`, `nc3_signs` "
     "and `tot_signs_read` COULD MOVE and are what makes the line a witness "
     "that the predicate can return absorbable at all."),
    ("NEGATIVE CONTROL 3's own lines are", 4, "COULD MOVE",
     "mg-5630's line-F experiment run inside this battery: `plus_same` and "
     "`par_bite` are measured under each of the four corruptions in turn, and "
     "the sentence itself branches on whether they moved."),
    ("a CANDIDATE THIS SECTION REJECTED", 9, "COULD MOVE",
     "`sw_app`, `sw_absorb` and `sw_spec` are three sums over the population "
     "for `facet_swap01`; the row that quotes them is the one this section "
     "rejected its own candidate on, and it reports 72/86 rather than 86/86."),
    ("WHERE A ROW REPORTS THE SPECTRUM MOVING ON FEWER THAN ALL", 1,
     "COULD MOVE",
     "`tot_gauge`, the size of the remainder the withdrawn hedge used to cover; "
     "it is 9 and would be 0 if no biting pair were a gauge."),
    ("COVERAGE AT `le_to_facet`, SIZED", 15, "COULD MOVE",
     "mg-fcb2's F1, repaired.  The first figure was filled `(N, N)` -- the same "
     "expression twice -- so `the named load-bearing site is corrupted on 86/86 "
     "posets` could not come out otherwise, and one poset outside the shipped "
     "population the SENTENCE WAS FALSE: at n = 1 both facet maps return the "
     "empty chain, the truth is 86 of 87, and the expression printed 87/87.  "
     "The numerator is now `site_corrupted`, a sum over the population, and it "
     "is shown taking THREE different values on three inputs in V7's FLIP 4 "
     "where the expression it replaced takes one.  The remaining figures were "
     "already measurements.  THIS ROW'S KEY WENT FROM 12 FIGURES TO 15 AND THE "
     "MECHANISM CAUGHT IT: naming the population and the grain in the sentence "
     "added three figures to it, the key stopped matching, and the coverage row "
     "REFUTED on my own edit -- which is the hole a sentence-only key would "
     "have left open.  That transcript is kept at "
     "code/face_geometry_repair_8af0/out_verify_e35b_F3GRAIN_exit1.txt."),
]


def main():
    ps = [P for n in range(2, NMAX + 1) for P in all_posets(n)]
    N = len(ps)
    print("VERIFY mg-e35b -- independent re-derivation of the repair's numbers")
    print("population: %d posets up to isomorphism, 2 <= n <= %d" % (N, NMAX))

    # -- V1: the dichotomy, per row ----------------------------------------
    print("V1 -- the GAUGE / NON-SIMILAR dichotomy, re-derived")
    dich = {}
    for mode in MODES:
        app = nonsim = gau = unc = 0
        for P in ps:
            L_true, _ = pair(P)
            L_mut, _ = pair(P, mode)
            if mat_eq(L_mut, L_true):
                continue
            app += 1
            if not_isospectral(L_mut, L_true):
                nonsim += 1
            elif gauge(P, mode) is not None:
                gau += 1
            else:
                unc += 1
        dich[mode] = (app, nonsim, gau, unc)
        check("%-7s %d biting = %d non-similar + %d gauge + %d unclassified"
              % (TAGS[mode], app, nonsim, gau, unc), unc == 0)
    expect = {"ridge_facets": (72, 66, 6, 0), "split_free_as_interior": (82, 82, 0, 0),
              "ridge_drop": (82, 82, 0, 0), "facet_offbyone": (61, 58, 3, 0),
              "facet_swap01": (72, 0, 72, 0)}
    check("the four scored rows carry 9 gauge (poset,row) pairs in total",
          sum(dich[m][2] for m in MODES if m != "facet_swap01") == 9)
    check("every per-row split matches the value mg-fcf1 reported independently",
          all(dich[m] == expect[m] for m in MODES),
          "; ".join("%s %s" % (TAGS[m], dich[m]) for m in MODES))

    # -- V2: the witness search against brute force ------------------------
    print("V2 -- the witness search against EXHAUSTIVE search over perms x signs")
    agree = tested = 0
    for mode in MODES:
        for P in ps:
            if len(linear_extensions(P)) > 4:
                continue                       # 24 perms x 16 signs is the bound
            L_true, _ = pair(P)
            L_mut, _ = pair(P, mode)
            if mat_eq(L_mut, L_true):
                continue
            tested += 1
            agree += (gauge(P, mode) is not None) == brute_signed_perm(L_true, L_mut)
    check("the GF(2) witness search agrees with brute force on %d/%d pairs "
          "with |L(P)| <= 4" % (agree, tested), tested > 0 and agree == tested)
    # AND AGAINST THE SHIPPED IMPLEMENTATION, PAIR BY PAIR.  V1 already shows
    # the two agree in TOTAL per row; totals can agree while the pairs behind
    # them disagree in both directions, so the shipped predicate is imported
    # HERE ONLY -- nothing above derives an answer from it -- and compared on
    # every biting pair.
    from controls import signed_permutation_witness as shipped   # noqa: E402
    same = pairs = 0
    for mode in MODES:
        for P in ps:
            L_true, _ = pair(P)
            L_mut, _ = pair(P, mode)
            if mat_eq(L_mut, L_true):
                continue
            pairs += 1
            mine = gauge(P, mode) is not None
            theirs = shipped(L_true, L_mut, candidates(P, mode)) is not None
            same += mine == theirs
    check("the GF(2) search and controls.py's BFS agree PAIR BY PAIR on %d/%d "
          "biting pairs, not merely in the per-row totals" % (same, pairs),
          pairs > 0 and same == pairs)

    # -- V3: the two meanings of vacuous -----------------------------------
    print("V3 -- vacuity: 'did not apply' vs 'applied and unseen'")
    vac = {}
    for mode in MODES:
        v = noap = blind = bset = big = 0
        for P in ps:
            L_true, _ = pair(P)
            L_mut, _ = pair(P, mode)
            if not mat_eq(L_mut, L_true):
                continue
            v += 1
            td_t, td_m = top_laplacians(P), top_laplacians(P, incidence_mode=mode)
            applied = (td_m["facets"] != td_t["facets"]
                       if mode in ("facet_offbyone", "facet_swap01")
                       else td_m["mutated_ridge"] is not None)
            if applied:
                blind += 1
                if sorted(td_m["facets"]) != sorted(td_t["facets"]):
                    bset += 1
                    big += len(linear_extensions(P)) >= 3
            else:
                noap += 1
        vac[mode] = (v, noap, blind, bset, big)
        print("    %-7s %d vacuous = %d did-not-apply + %d applied-but-unseen "
              "(facet SET differs on %d, of which %d have |L(P)| >= 3)"
              % (TAGS[mode], v, noap, blind, bset, big))
    check("I1/I2/I3 vacuity is EXACTLY 'the mutation did not apply' -- 0 "
          "applied-but-unseen in all three",
          all(vac[m][2] == 0 for m in
              ("ridge_facets", "split_free_as_interior", "ridge_drop")))
    check("I4 vacuity is the OTHER fact -- the mutation applied on all %d and "
          "the pipeline saw none of them; the facet SET differs on %d, %d with "
          "|L(P)| >= 3" % (vac["facet_offbyone"][0], vac["facet_offbyone"][3],
                           vac["facet_offbyone"][4]),
          vac["facet_offbyone"][1] == 0 and vac["facet_offbyone"][3] == 24
          and vac["facet_offbyone"][4] == 14)

    # -- V4a: the target byte-identity is FORCED, checked in the source -----
    print("V4 -- the two counts mg-fcf1 called tautologies")
    src = open(os.path.join(PROBE, "face_complex.py")).read()
    tree = ast.parse(src)
    at_sig = next(f for f in ast.walk(tree)
                  if isinstance(f, ast.FunctionDef) and f.name == "at_laplacian")
    at_args = [a.arg for a in at_sig.args.args] + \
              [a.arg for a in at_sig.args.kwonlyargs]
    ctl = ast.parse(open(os.path.join(PROBE, "controls.py")).read())
    c1 = next(f for f in ast.walk(ctl)
              if isinstance(f, ast.FunctionDef) and f.name == "claim1_pair")
    at_calls = [c for c in ast.walk(c1)
                if isinstance(c, ast.Call) and getattr(c.func, "id", None) == "at_laplacian"]
    check("`at_laplacian` takes no incidence argument (%s) and `claim1_pair` "
          "calls it with %s -- so 344/344 byte-identical targets is FORCED BY "
          "THE CODE PATH and could not have come out otherwise"
          % (at_args, ["%d positional, %d keyword" % (len(c.args), len(c.keywords))
                       for c in at_calls]),
          "incidence_mode" not in at_args and len(at_calls) == 1
          and not at_calls[0].keywords)
    m4 = sum(1 for P in ps
             if not mat_eq(pair(P)[1], [[2 * t for t in r] for r in pair(P)[1]]))
    check("and the comparison CAN come out otherwise: scaling the target by 2 "
          "moves it on %d/%d posets by the same equality test" % (m4, N),
          0 < m4 < N)

    # -- V4b: the >=3-facets zeros -----------------------------------------
    adds = {}
    for mode in MODES[:4]:
        worse = 0
        for P in ps:
            t = top_laplacians(P)["ridge_facets"]
            m = top_laplacians(P, incidence_mode=mode)["ridge_facets"]
            worse += any(len(v) >= 3 for v in m.values())
            adds[mode] = worse
    check("no ridge lies in >= 3 facets under any of the four mutations (%s)"
          % ", ".join("%s %d" % (TAGS[k], v) for k, v in adds.items()),
          all(v == 0 for v in adds.values()))
    # forcedness of three of the four, checked as a property of the incidence
    # data rather than argued: I1/I2/I3 never RAISE any ridge's facet count.
    raised = {}
    for mode in ("ridge_facets", "split_free_as_interior", "ridge_drop"):
        r = 0
        for P in ps:
            t = top_laplacians(P)["ridge_facets"]
            m = top_laplacians(P, incidence_mode=mode)["ridge_facets"]
            r += any(len(m.get(k, [])) > len(v) for k, v in t.items())
        raised[mode] = r
    check("I1/I2/I3 never RAISE any ridge's facet count on any poset (%s), so "
          "their three zeros are forced at every n"
          % ", ".join("%s %d" % (TAGS[k], v) for k, v in raised.items()),
          all(v == 0 for v in raised.values()))
    # AND I4'S IS FORCED TOO (mg-fcb2's F3, landed by mg-8af0).  mg-e35b landed
    # "only I4's is a result" here and in the artifact.  It is not a result: the
    # forcing is a property of the two facet MAPS, not of the mutation.  Both
    # return a chain of masks of sizes 1, 2, ..., n-1, so a ridge omits the
    # level-k mask and the two masks bracketing it differ in exactly two
    # elements -- exactly two candidates to re-insert.  Both halves are
    # measured: the premise (every family has that level-size profile) and the
    # conclusion (no ridge in >= 3 facets), over a WIDER population than the
    # section runs on, because a claim made "at every n" should not be checked
    # only at the n the artifact happens to use.
    fams = worst = profile_ok = multi = 0
    for n in range(1, 7):
        for P in all_posets(n):
            les = linear_extensions(P)
            for mp in (le_to_facet, le_to_facet_offbyone):
                fams += 1
                facets = {mp(w) for w in les}
                profile_ok += all(
                    tuple(bin(m).count("1") for m in f) == tuple(range(1, len(f) + 1))
                    for f in facets)
                mult = {}
                for f in facets:
                    for i in range(len(f)):
                        key = (i, f[:i] + f[i + 1:])
                        mult[key] = mult.get(key, 0) + 1
                worst = max([worst] + list(mult.values()))
                multi += any(v >= 3 for v in mult.values())
    check("and SO IS I4'S, which mg-e35b called 'the only one of the four that "
          "is a result' (mg-fcb2 F3): every facet under BOTH maps is a chain of "
          "masks of sizes 1..n-1 (%d/%d families), so a ridge leaves exactly two "
          "candidates to re-insert -- largest number of facets sharing a ridge "
          "%d, families with a ridge in >= 3 facets %d.  Population: every poset "
          "up to isomorphism with n <= 6 under each of the two maps, %d "
          "families; grain: the ridge.  Forced at every n, by a property of the "
          "MAPS and not of the mutation"
          % (profile_ok, fams, worst, multi, fams),
          profile_ok == fams and worst == 2 and multi == 0 and fams == 810)

    # -- V5: the committed artifact agrees ---------------------------------
    print("V5 -- the committed artifact states these numbers")
    art = open(os.path.join(PROBE, "controls_output.txt")).read()
    wanted = [
        ("297 biting (poset, row) pairs = 288 NON-SIMILAR + 9 GAUGE + 0 unclassified",
         "the dichotomy total"),
        ("I1 66/72 non-similar, 6 gauge", "row I1's split"),
        ("I4 58/61 non-similar, 3 gauge", "row I4's split"),
        ("GAUGE on 72/72 of the posets where it bites", "the detector's positive control"),
        ("I4 25 vacuous = 0 did-not-apply + 25 applied-but-unseen", "I4's vacuity"),
        ("coverage at `le_to_facet` is 61/86", "the coverage sizing"),
        ("COULD NOT HAVE COME OUT OTHERWISE", "the forced-target disclosure"),
    ]
    for lit, what in wanted:
        check("artifact carries %s" % what, lit in art, repr(lit[:52]))
    # The old sentence must be gone AS AN ASSERTION.  It is still present as a
    # QUOTATION -- the replacement text names what it replaced -- so the check
    # is keyed on the assertion's own wording and not on the phrase, which
    # would go red on the correction itself.
    check("the artifact no longer ASSERTS the hedge (the old wording is absent; "
          "the phrase survives only inside the sentence that withdraws it)",
          "THIS FILE makes no claim either way on the remainder" not in art
          and "WHAT IS IN THE REMAINDER IS NOW STATED" in art)

    # -- V6: every count the SECTION prints, over a population derived from
    # -- its source rather than listed here (mg-8af0, landing mg-fcb2's F2) --
    print("V6 -- EVERY COUNT `negative_control_incidence` PRINTS, classified, "
          "over a population READ OUT OF ITS SOURCE and not listed in this file "
          "(mg-8af0, landing mg-fcb2's F2).  A count that could not have come "
          "out otherwise is labelled FORCED and is not offered as evidence.")
    ctl_src = open(os.path.join(PROBE, "controls.py")).read()
    sites = count_sites(ctl_src)
    matches, ambiguous, unclaimed, contested = claim_population(sites, V6_ROWS)
    by_key = {k: v[0] for k, v in matches.items() if len(v) == 1}
    print("    population: the %d `%%`-format sites carrying at least one `%%d` "
          "inside `negative_control_incidence`, carrying %d `%%d` conversions "
          "between them.  Grain: one row per SITE, not per figure."
          % (len(sites), sum(s["nd"] for s in sites)))
    for anchor, nd, verdict, why in V6_ROWS:
        s = by_key.get((anchor, nd))
        print("    controls.py:%-5s %-2d figures  %-34s %s"
              % (s["line"] if s else "??", nd, verdict, anchor))
        print("        %s" % why)
    forced = sum(1 for _, _, v, _ in V6_ROWS if v.startswith("FORCED"))
    mixed = sum(1 for _, _, v, _ in V6_ROWS if v.startswith("MIXED"))
    print("    %d of the %d sites are FORCED outright and %d carry figures of "
          "both kinds; population for those two counts: the rows of this table, "
          "grain: the site.  NEITHER IS SCORED -- a hand-written tally of a "
          "hand-written column is the defect being repaired, and what is scored "
          "below is coverage of a population this file did not write."
          % (forced, len(V6_ROWS), mixed))
    check("every one of the %d count-bearing sites in `negative_control_"
          "incidence` is claimed by exactly one row of the table above -- so a "
          "count added anywhere in the section leaves a member of the "
          "population unclaimed and turns this row RED" % len(sites),
          not unclaimed and not contested,
          "unclaimed: %s; contested: %s"
          % ([s["line"] for s in unclaimed], [s["line"] for s in contested]))
    check("and every row of the table claims exactly one site, so an anchor "
          "that has rotted off the source cannot be mistaken for coverage",
          not ambiguous,
          "rows matching %s sites"
          % [len(matches[k]) for k in ambiguous] if ambiguous else "")
    taut = [(s, hits) for s in sites for hits in [same_expression_ratios(s)] if hits]
    check("no site in the section fills an `X/Y` figure from THE SAME "
          "EXPRESSION TWICE -- the structural shape of mg-fcb2's F1, which no "
          "count that is evidence can have",
          not taut,
          "; ".join("controls.py:%d prints `%s/%s`" % (s["line"], e, e)
                    for s, hs in taut for _, e in hs) or "0 of %d sites flagged"
          % len(sites))

    # -- V7: every verdict V6 makes real, FLIPPED on a constructed input -----
    print("V7 -- THE VERDICTS OF V6, SHOWN CAPABLE OF GOING THE OTHER WAY "
          "(mg-8af0).  A control nobody has seen fail is not evidence, so each "
          "of V6's three scored rows is re-run against an input built to "
          "REFUTE it.  All three constructions are AST rewrites of "
          "`controls.py`, so none depends on the text of a line a later repair "
          "may move.")
    round_trip = count_sites(ast.unparse(ast.parse(ctl_src)))
    check("instrument check on the constructions themselves: an `ast` "
          "round-trip of `controls.py` yields the same %d sites with the same "
          "figure counts, AS A MULTISET, so the three sources below differ from "
          "the shipped one only by what they inject, delete or rewrite.  IT IS "
          "A MULTISET AND NOT A SEQUENCE BECAUSE THIS CHECK FIRED ON ME FIRST "
          "(mg-8af0 P-12, and the failing transcript is kept at "
          "code/face_geometry_repair_8af0/out_verify_e35b_FIRSTFORM_exit1.txt): "
          "its first form compared two line-ordered lists, and `ast.unparse` "
          "puts each statement on one line, which collapses a nested `%%` site "
          "onto its parent's and reorders the population without changing it.  "
          "The population was identical the whole time and the instrument said "
          "otherwise" % len(sites),
          sorted((s["nd"], s["fmt"]) for s in round_trip)
          == sorted((s["nd"], s["fmt"]) for s in sites),
          "%d sites after round-trip" % len(round_trip))
    inj = count_sites(inject_extra_count(ctl_src))
    _, _, inj_unclaimed, _ = claim_population(inj, V6_ROWS)
    check("FLIP 1 -- a TWELFTH count added to the section with this file left "
          "untouched (mg-fcb2's own F2 demonstration, pointed back at the "
          "repair) leaves exactly 1 site unclaimed and REFUTES the coverage "
          "row.  Under `forced == 3 and len(table) == 11` it stayed GREEN.",
          len(inj) == len(sites) + 1 and len(inj_unclaimed) == 1,
          "%d sites, %d unclaimed" % (len(inj), len(inj_unclaimed)))
    RIDGE = "no ridge lies in >= 3 facets under any of the four mutations"
    dele = count_sites(delete_statement(ctl_src, RIDGE))
    del_matches, del_ambiguous, _, _ = claim_population(dele, V6_ROWS)
    check("FLIP 2 -- the ridge-multiplicity sentence DELETED from the section "
          "refutes in the OTHER direction: 2 rows of the table (the sentence "
          "and its per-mode sub-template) then claim no site at all, rather "
          "than the check passing on a table that has quietly stopped "
          "describing anything",
          len(dele) == len(sites) - 2 and len(del_ambiguous) == 2
          and all(not del_matches[k] for k in del_ambiguous),
          "%d sites, %d rows claiming %s"
          % (len(dele), len(del_ambiguous),
             [len(del_matches[k]) for k in del_ambiguous]))
    COVERAGE = "COVERAGE AT `le_to_facet`, SIZED"
    taut_src = count_sites(make_ratio_tautological(ctl_src, COVERAGE))
    taut_hits = [(s, h) for s in taut_src for h in [same_expression_ratios(s)] if h]
    check("FLIP 3 -- the coverage site's numerator rewritten to the same "
          "expression as its denominator (mg-fcb2's F1, reconstructed) is "
          "flagged by the scan, on exactly 1 site, and it is that one -- so "
          "the scan's silence on the shipped source is a result and not the "
          "answer of a scan that never fires",
          len(taut_hits) == 1 and COVERAGE in taut_hits[0][0]["fmt"],
          "%d flagged: %s" % (len(taut_hits),
                              [s["line"] for s, _ in taut_hits]))

    # -- FLIP 4: the repaired F1 numerator, run on three populations ---------
    # Route disjointness: `mutation_applied_at_site` is one of the five things
    # mg-e35b added and this file does not import, so "is the named site
    # corrupted" is asked here of the facet MAPS directly, without building a
    # Laplacian at all.
    def site_corrupted(pop, mut_map):
        n = 0
        for P in pop:
            les = linear_extensions(P)
            n += [le_to_facet(w) for w in les] != [mut_map(w) for w in les]
        return n

    wide = [P for n in range(1, NMAX + 1) for P in all_posets(n)]
    shipped = site_corrupted(ps, le_to_facet_offbyone)
    widened = site_corrupted(wide, le_to_facet_offbyone)
    noop = site_corrupted(ps, le_to_facet)
    check("FLIP 4 -- mg-fcb2's F1 numerator, repaired, takes THREE DIFFERENT "
          "VALUES on the three inputs where the expression it replaced takes "
          "one: %d/%d on the shipped population, %d/%d when n = 1 is admitted "
          "(both facet maps return the empty chain there, so the site is not "
          "corrupted and the old `(N, N)` printed 87/87 with the truth 86 of "
          "87), and %d/%d when the corruption is made a no-op.  Population: "
          "posets up to isomorphism; grain: the poset, counted corrupted when "
          "the ORDERED facet list differs -- at the facet-SET grain the shipped "
          "answer is 82, not 86, and the sentence says which it means"
          % (shipped, len(ps), widened, len(wide), noop, len(ps)),
          (shipped, widened, noop) == (86, 86, 0)
          and len({shipped, widened, noop}) > 1,
          "old expression would print %d/%d, %d/%d, %d/%d"
          % (len(ps), len(ps), len(wide), len(wide), len(ps), len(ps)))
    art_now = open(os.path.join(PROBE, "controls_output.txt")).read()
    check("and the artifact prints exactly that numerator: `corrupted on "
          "%d/%d posets`" % (shipped, len(ps)),
          "corrupted on %d/%d posets" % (shipped, len(ps)) in art_now)

    print()
    if FAILED:
        print("%d checks, %d REFUTED:" % (CHECKS[0], len(FAILED)))
        for f in FAILED:
            print("  - %s" % f)
        return 1
    print("%d checks, 0 refuted." % CHECKS[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
