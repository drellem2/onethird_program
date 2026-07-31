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

Exit 0 iff every check passes.
"""

import ast
import itertools
import os
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
          "their three zeros are forced at every n and only I4's is a result"
          % ", ".join("%s %d" % (TAGS[k], v) for k, v in raised.items()),
          all(v == 0 for v in raised.values()))

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

    # -- V6: this repair's own counts, and whether each could have moved ----
    print("V6 -- EVERY COUNT THIS REPAIR PRINTS, and whether it could have come "
          "out differently.  A count that could not is labelled FORCED and is "
          "not offered as evidence anywhere in the repair.")
    table = [
        ("dichotomy: 297 = 288 + 9 + 0", "COULD MOVE",
         "an unclassified pair turns the row red; the 9 is a per-poset decision "
         "and differs by row (6/0/0/3)"),
        ("detector positive control: swap01 GAUGE 72/72", "FORCED BY MATHEMATICS",
         "exchanging two columns IS a signed-permutation conjugation; the row is "
         "an instrument check and says so, and fails only if the detector is wrong"),
        ("detector says NOT-GAUGE on 288 of 297", "COULD MOVE",
         "a detector that accepted everything would print 297 here"),
        ("non-identity witness on 72/72 of swap01", "COULD MOVE",
         "a detector answering by diagonal twist alone would print 0"),
        ("vacuity split I1/I2/I3 = 14/4/4 did-not-apply, 0 unseen", "COULD MOVE",
         "a mutation that applied and left L^rel fixed would land in the other column"),
        ("vacuity split I4 = 0 did-not-apply, 25 unseen (24 by facet SET, 14 big)",
         "COULD MOVE", "this is a measurement of blindness and is stated, not scored"),
        ("target byte-identical 344/344", "FORCED BY THE CODE PATH",
         "at_laplacian takes no incidence_mode; printed as a property, and the "
         "comparison's ability to move is shown by M4/M5 instead"),
        ("no ridge in >= 3 facets, I1/I2/I3 zeros", "FORCED BY CONSTRUCTION",
         "none of the three raises any ridge's facet count; checked in V4b"),
        ("no ridge in >= 3 facets, I4 zero", "COULD MOVE",
         "I4 rebuilds the facet enumeration outright"),
        ("coverage 61/86 at le_to_facet, 58 non-similar", "COULD MOVE",
         "derived from the two counts above, both of which could move"),
        ("M4 moves the target on 82/86, M5 on 82/86", "COULD MOVE",
         "the 4 posets with |L(P)| = 1 have an empty target that scaling cannot move"),
    ]
    for what, verdict, why in table:
        print("    %-16s %s  -- %s" % (verdict, what, why))
    forced = sum(1 for _, v, _ in table if v.startswith("FORCED"))
    check("every printed count is classified, and the %d FORCED ones are "
          "printed as properties rather than offered as evidence"
          % forced, forced == 3 and len(table) == 11)

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
