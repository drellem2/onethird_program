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

V6 WAS ITSELF THE DEFECT IT WAS BUILT TO CATCH, and mg-fcb2's F2 is the finding
(repaired by mg-8af0).  The row read

    check("every printed count is classified ...", forced == 3 and len(table) == 11)

-- a condition on the LITERAL LIST BESIDE IT.  Add a twelfth count to the
artifact and leave this file alone and the row stays green; the only input that
could ever move it was an edit to its own table.  That is a control that cannot
fail, under a heading that claimed the population "EVERY COUNT THIS REPAIR
PRINTS", and it is exactly why mg-fcb2's F1 survived: the tautological
"corrupted on 86/86" is simply not in the table.  What replaces it is three
rows, each scored against something OUTSIDE this file, each with its population
and grain written into its own name:

  V6a ANCHORED   -- every classified count is still printed in the artifact,
                    matched as a verbatim substring.  Population: the entries of
                    `TABLE`.  Grain: one entry.  RED when a classified count is
                    removed or reworded.
  V6b CENSUS     -- the set of formatted values NEGATIVE CONTROL 4 prints is
                    unchanged since this table was written.  Population: the
                    `%`-format expressions lexically inside
                    `negative_control_incidence` in controls.py.  Grain: one
                    conversion specifier.  RED when a count is added or removed
                    at the source.  It is a TRIPWIRE and says so: it does not
                    check that the entries of `TABLE` are the right ones.
  V6c REGENERATED-- controls_output.txt is byte-identical to a fresh run.  RED
                    when the artifact is hand-edited or goes stale, which is the
                    one channel V6b cannot see.
  V6d REACH      -- V6b's population, split by whether the value actually
                    reaches the artifact: printed / unreached / discarded.
                    Same population, same grain, different ROUTE -- it RUNS the
                    section where V6b reads it.  Added by mg-843d when V6b fired
                    on `de86fee` and the estate could not say, without forty
                    minutes of work, whether the 26 new specifiers were printed
                    content or a `%d` in a branch nobody runs.  RED when the
                    split moves, and it names the sites.

`forced` is still computed and printed.  It is no longer scored: "3 of my own 12
rows say FORCED" is a fact about this file and nothing else, and scoring it is
the move that produced the defect.

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
import io
import itertools
import os
import re
import subprocess
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
# V6's machinery (mg-8af0, landing mg-fcb2's F2).  At module scope, not inside
# `main`, for one reason: the demonstration in
# code/face_geometry_repair_8af0/demo_f2_row_can_go_red.py drives these three
# functions over MUTATED copies of the artifact and of controls.py, and shows
# each row going red.  A control nobody has watched fire is not evidence that it
# can.
# ---------------------------------------------------------------------------

# Each entry: (count, verdict, why, anchor).  The ANCHOR is the verbatim text
# the artifact prints for that count.  It is what turns a claim about the
# repair's output into something checkable against the output.
TABLE = [
    ("dichotomy: 297 = 288 + 9 + 0", "COULD MOVE",
     "an unclassified pair turns the row red; the 9 is a per-poset decision "
     "and differs by row (6/0/0/3)",
     "297 biting (poset, row) pairs = 288 NON-SIMILAR + 9 GAUGE + 0 unclassified"),
    ("detector positive control: swap01 GAUGE 72/72", "FORCED BY MATHEMATICS",
     "exchanging two columns IS a signed-permutation conjugation; the row is "
     "an instrument check and says so, and fails only if the detector is wrong",
     "classified GAUGE on 72/72 of the posets where it bites"),
    ("detector says NOT-GAUGE on 288 of 297", "COULD MOVE",
     "a detector that accepted everything would print 297 here",
     "saying NOT-GAUGE on 288 of the 297 biting pairs"),
    ("non-identity witness on 72/72 of swap01", "COULD MOVE",
     "a detector answering by diagonal twist alone would print 0",
     "on 72 of them the exhibited permutation is NOT the identity"),
    ("vacuity split I1/I2/I3 = 14/4/4 did-not-apply, 0 unseen", "COULD MOVE",
     "a mutation that applied and left L^rel fixed would land in the other column",
     "I1 14 vacuous = 14 did-not-apply + 0 applied-but-unseen"),
    ("vacuity split I4 = 0 did-not-apply, 25 unseen (24 by facet SET, 14 big)",
     "COULD MOVE", "this is a measurement of blindness and is stated, not scored",
     "I4 25 vacuous = 0 did-not-apply + 25 applied-but-unseen"),
    ("target byte-identical 344/344", "FORCED BY THE CODE PATH",
     "at_laplacian takes no incidence_mode; printed as a property, and the "
     "comparison's ability to move is shown by M4/M5 instead",
     "byte-identical to the uncorrupted target on 344/344 (poset, mutation) pairs"),
    ("no ridge in >= 3 facets, I1/I2/I3 zeros", "FORCED BY CONSTRUCTION",
     "none of the three raises any ridge's facet count; checked in V4b",
     "ridge_facets on 0, split_free_as_interior on 0, ridge_drop on 0"),
    # RELABELLED FROM "COULD MOVE" (mg-fcb2's F3, landed by mg-8af0).  mg-e35b
    # read this zero as the one measurement of the four.  It cannot move at any
    # n: both facet maps are prefix families, so deleting a level of a facet
    # leaves exactly two masks that can be re-inserted.
    ("no ridge in >= 3 facets, I4 zero", "FORCED BY CONSTRUCTION",
     "both facet maps return a chain of masks of sizes 1..n-1, so a ridge -- "
     "that chain with one level deleted -- admits exactly two re-insertions; "
     "premise and bound checked in V4c here and over n <= 6 in "
     "code/face_geometry_repair_8af0/probe_f3_ridge_multiplicity.py",
     "facet_offbyone on 0"),
    ("coverage 61/86 at le_to_facet, 58 non-similar", "COULD MOVE",
     "derived from the two counts above, both of which could move",
     "coverage at `le_to_facet` is 61/86"),
    ("M4 moves the target on 82/86, M5 on 82/86", "COULD MOVE",
     "the 4 posets with |L(P)| = 1 have an empty target that scaling cannot move",
     "moves it on 82/86 posets and M5 (one edge deleted) on 82/86"),
    # THE TWELFTH ENTRY, and the reason the eleven above are not the population
    # the old heading claimed (mg-fcb2's F1, landed by mg-8af0).  This count was
    # printed by the repair, was a tautology, and was NOT IN THE TABLE.
    ("le_to_facet corrupted at the SITE on 86/86", "COULD MOVE",
     "`% (N, N, ...)` -- the same expression twice -- until mg-8af0; measured "
     "now, and it reads 86/87 with n = 1 admitted and 0/86 with the corruption "
     "made a no-op, both constructed in "
     "code/face_geometry_repair_8af0/probe_f1_count_moves.py and re-derived in V7",
     "The named load-bearing site is corrupted on 86/86 posets"),
]

# The census, DECLARED.  Measured by `census()` from the source of
# `negative_control_incidence`; see that function for the population and the
# grain.  This is a literal, and unlike the one it replaces it is a literal on
# the WRONG SIDE of the comparison: the measured side comes from another file.
# Any count added to or removed from the section moves it.
#
# --- 184 -> 210, and WHY, because the number moving is the whole event -------
# THE TRIPWIRE FIRED ON A REAL INPUT AND THIS IS THE ANSWER TO IT (mg-843d).
# `de86fee` (mg-17aa) rewrote `negative_control_incidence` and measured 210
# against this declared 184; `de86fee~1` measures 184.  The verifier exited 1
# from 2026-08-10 to 2026-08-13 with nothing in the estate running it, and the
# one repair that was NOT available was moving this number on its own -- that
# is the edit that silences a live disagreement instead of answering it.
#
# WHAT WAS ASKED: do the 26 belong in the census?  The population is stated in
# `census()` and it is LEXICAL -- `%`-format expressions inside the function --
# so the question is whether `de86fee`'s new expressions are that.  Measured at
# the SITE grain, not asserted:
#
#     184  declared, at de86fee~1                     (34 sites)
#     -28  five sites REMOVED by mg-17aa               1 + 9 + 1 + 9 + 8
#     +54  eleven sites ADDED by mg-17aa               4+16+2+1+11+5+2+8+1+2+2
#     ---
#     210  measured, at de86fee                       (40 sites)
#
# EVERY ONE OF THE FIVE REMOVALS AND ELEVEN ADDITIONS IS mg-17aa's ROW
# REWRITE: the mg-8a12 routing row and its `DIAGONAL_MOVES` clause left, and
# the [CANNOT FAIL] row over all four I-rows, the falsifiability check and its
# per-row planted-worlds lines arrived.  They are inside the function, they are
# `%`-format expressions, and 194 of the 210 reach the artifact VERBATIM -- so
# by the population this census declares, they belong, and the DECLARATION is
# what was stale.  The values are not the defect; `de86fee` not re-declaring
# was.  The site-level derivation is in README.md ("The census question").
#
# WHAT THE COUNT MOVING DID *NOT* SETTLE, and why V6d exists.  Of the 26, only
# 11 are new PRINTED values; 14 sit in a branch mg-17aa keeps on purpose and
# the run never reaches (controls.py's "THIS BRANCH IS REACHED ONLY BY A
# MUTATION SET WITH A PAIR THAT CLEARS BOTH FORCED GATES"), and 2 are a
# `dict.get` default that Python evaluates eagerly and throws away.  That split
# is the thing that made this question take forty minutes instead of one look,
# so it is now MEASURED and scored as V6d rather than written here as prose.
CENSUS_DECLARED = {
    "specifiers": 210,          # conversion specifiers, all types
    "d": 162,                   # of which integer conversions
    "s": 48,                    # of which string conversions
    "fstrings": 0,              # channel bound: an f-string is invisible here
    "format_calls": 0,          # channel bound: so is "...".format(...)
    "str_calls": 0,             # channel bound: so is str()/repr()/format()
    "nonliteral_mod": 1,        # `%` sites whose left operand is not a literal
}

# The census, SPLIT BY WHETHER THE VALUE REACHES THE ARTIFACT.  Measured by
# `census_reach()`, which runs the section rather than reading it.  Same
# population as `CENSUS_DECLARED`, finer grain: each specifier is assigned to
# exactly one of three fates, and the three sum to `specifiers` above -- an
# identity this file scores, so the split cannot drift into a fourth number.
#
# WHY IT IS A SEPARATE DECLARATION AND NOT A FIELD OF THE CENSUS: `census()` is
# pure-source and `demo_f2_row_can_go_red.py` drives it over MUTATED copies of
# controls.py without running them.  Running is a different route and it is the
# route that tells a printed value from a lexical one.
CENSUS_REACH_DECLARED = {
    "printed": 194,     # the site's string appears in controls_output.txt
    "unreached": 14,     # the site is never evaluated (one branch, kept on purpose)
    "discarded": 2,      # evaluated and thrown away (the MAGNITUDE_MOVES `.get` default)
}

_SPEC = re.compile(r"%[-#0 +]*[0-9*]*(?:\.[0-9*]+)?([diouxXeEfFgGcrsa%])")


def census(controls_src, fn_name="negative_control_incidence"):
    """Every formatted value NEGATIVE CONTROL 4 prints, counted from the source.

    POPULATION: the `%`-format expressions lexically inside `fn_name` in
    controls.py.  GRAIN: one conversion specifier -- not one distinct value and
    not one printed line, so a count printed twice counts twice and two counts
    on one line count twice.

    WHAT IT DOES NOT SEE, enumerated rather than hoped about.  A value can reach
    the artifact through four other channels: an f-string, a `.format` call, a
    `str()`/`repr()`/`format()` call, and a `%` whose left operand is not a
    string literal (which `ast` cannot tell from arithmetic).  Each is counted
    and each is part of the declared census, so a channel OPENING is itself a
    red row.  The one non-literal `%` site in the section today is `i % 3`
    inside a sign vector -- arithmetic, not formatting -- and it is declared as
    1 rather than exempted, because an exemption nobody counts is how the
    channel this file exists to police got there.
    """
    tree = ast.parse(controls_src)
    fn = next((f for f in ast.walk(tree)
               if isinstance(f, ast.FunctionDef) and f.name == fn_name), None)
    if fn is None:
        raise ValueError("no function %r in the source given" % (fn_name,))
    out = {"specifiers": 0, "d": 0, "s": 0, "fstrings": 0,
           "format_calls": 0, "str_calls": 0, "nonliteral_mod": 0}
    for node in ast.walk(fn):
        if isinstance(node, ast.JoinedStr):
            out["fstrings"] += 1
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute) and node.func.attr == "format":
                out["format_calls"] += 1
            elif getattr(node.func, "id", None) in ("str", "repr", "format"):
                out["str_calls"] += 1
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            left = node.left
            if isinstance(left, ast.Constant) and isinstance(left.value, str):
                for conv in _SPEC.findall(left.value):
                    if conv == "%":
                        continue                 # a literal per cent, not a value
                    out["specifiers"] += 1
                    if conv in out:
                        out[conv] += 1
            else:
                out["nonliteral_mod"] += 1
    return out


def unanchored(artifact, table=TABLE):
    """The entries of `table` whose count is no longer printed in `artifact`."""
    return [what for what, _, _, anchor in table if anchor not in artifact]


def regenerate(probe_dir, nmax=5):
    """A fresh `controls.py <nmax>` run, as text.  Nothing is written to disk."""
    proc = subprocess.run([sys.executable, "controls.py", str(nmax)],
                          cwd=probe_dir, capture_output=True, text=True)
    return proc.stdout


def census_reach(probe_dir, nmax=5, fn_name="negative_control_incidence"):
    """The census SPLIT BY FATE: printed, unreached, or evaluated-and-discarded.

    POPULATION: identical to `census()`'s -- the `%`-format expressions with a
    string-literal left operand lexically inside `fn_name`.  GRAIN: one
    conversion specifier, as there.  What is different is the ROUTE: `census()`
    reads the source, this RUNS it, and the two answers are about different
    things.  A specifier can be lexically present and never printed, and until
    mg-843d nothing here could tell those apart -- which is exactly what made
    "do the 26 values `de86fee` added belong in the census?" expensive.

    Every qualifying `%`-expression is wrapped, in the AST, in a probe that
    records the string it produced; the section is then run with stdout
    captured, and each SITE lands in one of three buckets:

      printed    -- the site evaluated and one of its results is a substring of
                    the artifact.  This is the census's own headline claim
                    ("every formatted value NEGATIVE CONTROL 4 prints"), and it
                    is the only bucket that claim was ever about.
      unreached  -- the site never evaluated.  Nothing is wrong with that: a
                    branch kept so the routing can put a clause back with no
                    edit is a branch that should not fire today.  It is counted
                    rather than exempted, for the reason `census()` gives about
                    the one non-literal `%`.
      discarded  -- the site evaluated and its string reached no output.  The
                    one today is a `dict.get` default, which Python evaluates
                    before it knows it will not be used.

    A site whose string is FURTHER transformed before printing would be scored
    `discarded` here.  There is none today; if one arrives, this row goes red
    and says which site, which is the right outcome for a tripwire.

    Nothing is written to disk and nothing of controls.py's is imported: the
    module is executed in a private namespace.

    THE PROBE'S OWN OUTPUT IS RETURNED so that the caller can check the wrap
    changed nothing.  An instrument that perturbs what it measures would report
    a `printed` count about a document that does not exist, and the whole of
    V6b/V6c would be measuring one artifact while this row measured another.
    """
    src_path = os.path.join(probe_dir, "controls.py")
    src = open(src_path).read()
    tree = ast.parse(src)
    fn = next((f for f in ast.walk(tree)
               if isinstance(f, ast.FunctionDef) and f.name == fn_name), None)
    if fn is None:
        raise ValueError("no function %r in %s" % (fn_name, src_path))

    # KEYED BY A SITE INDEX AND NOT BY A LINE NUMBER.  Two `%`-sites can share
    # a line -- `ast.unparse` produces exactly that, and so does any hand-edit
    # that joins two statements -- and keying the probe's records on the line
    # would silently merge them, so one site's fate would be reported for both.
    # The demonstration in demo_v6d_row_can_go_red.py found this row doing it,
    # which is what a demonstration is for.  The line is kept for REPORTING.
    wanted = {}                       # id(BinOp) -> (site index, lineno, nspecs)
    for node in ast.walk(fn):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
            left = node.left
            if isinstance(left, ast.Constant) and isinstance(left.value, str):
                convs = [c for c in _SPEC.findall(left.value) if c != "%"]
                if convs:
                    wanted[id(node)] = (len(wanted), left.lineno, len(convs))

    probe_name = "__census_reach_probe"

    class _Wrap(ast.NodeTransformer):
        def visit_BinOp(self, node):
            self.generic_visit(node)
            if id(node) in wanted:
                idx, _, _ = wanted[id(node)]
                return ast.Call(func=ast.Name(id=probe_name, ctx=ast.Load()),
                                args=[ast.Constant(value=idx), node],
                                keywords=[])
            return node

    # `visit` mutates in place, so the ids captured above stay valid.
    ast.fix_missing_locations(_Wrap().visit(tree))

    seen = {}                                 # site index -> [produced strings]

    def _probe(idx, value):
        seen.setdefault(idx, []).append(value)
        return value

    ns = {"__name__": "__main__", "__file__": src_path, probe_name: _probe}
    argv, stdout = sys.argv, sys.stdout
    buf = io.StringIO()
    sys.argv, sys.stdout = ["controls.py", str(nmax)], buf
    try:
        exec(compile(tree, src_path, "exec"), ns)
    except SystemExit:
        pass
    finally:
        sys.argv, sys.stdout = argv, stdout
    art = buf.getvalue()

    out = {"printed": 0, "unreached": 0, "discarded": 0}
    where = {"printed": [], "unreached": [], "discarded": []}
    for idx, lineno, nspecs in wanted.values():
        if idx not in seen:
            fate = "unreached"
        elif any(v in art for v in seen[idx]):
            fate = "printed"
        else:
            fate = "discarded"
        out[fate] += nspecs
        where[fate].append(lineno)
    for k in where:
        where[k].sort()
    return out, where, art


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
          "their three zeros are forced at every n"
          % ", ".join("%s %d" % (TAGS[k], v) for k, v in raised.items()),
          all(v == 0 for v in raised.values()))
    # -- V4c: I4's zero is forced TOO (mg-fcb2's F3, landed by mg-8af0) ------
    # The clause "and only I4's is a result" used to close the row above.  It
    # is false.  The forcing is a property of the FACET FAMILY, not of the
    # mutation: both maps are prefix families, so every facet is a chain of
    # masks of sizes 1..n-1, a ridge is that chain with one level deleted, and
    # a mask of the missing size k must sit between the surviving levels of
    # sizes k-1 and k+1 -- two sets differing in exactly two elements, so
    # exactly two candidates.  The PREMISE is what is checkable, and it is
    # checked here on n <= 5 and in the 8af0 probe on n <= 6.  n = 2 is the
    # case the argument does not cover and it is counted separately.
    chain_bad = 0
    facets_seen = 0
    max_mult = 0
    n2_degenerate = 0
    for mode in MODES:
        for P in ps:
            td = top_laplacians(P, incidence_mode=mode)
            for f in td["facets"]:
                facets_seen += 1
                if [bin(m).count("1") for m in f] != list(range(1, P.n)):
                    chain_bad += 1
            max_mult = max(max_mult, max((len(v) for v in
                                          td["ridge_facets"].values()),
                                         default=0))
            if P.n == 2 and len(td["facets"]) == 2:
                n2_degenerate += 1
    check("I4's zero is FORCED TOO: every facet under every one of the %d modes "
          "is a chain of masks of sizes 1..n-1 (%d violations over %d facets) "
          "and no ridge lies in more than %d facets, so the two-re-insertions "
          "bound holds and mg-e35b's 'its zero is the only one of the four that "
          "is a result' is refuted"
          % (len(MODES), chain_bad, facets_seen, max_mult),
          chain_bad == 0 and max_mult == 2,
          "the n = 2 posets are NOT covered by that argument -- there the "
          "unique ridge is the empty chain and lies in every facet; %d "
          "(poset, mode) build%s hits that case and is bounded by |L(P)| <= 2 "
          "instead" % (n2_degenerate, "" if n2_degenerate == 1 else "s"))

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
    # THE HEADING IS NARROWER THAN IT WAS, AND THAT IS THE REPAIR (mg-fcb2's
    # F2, landed by mg-8af0).  It used to read "EVERY COUNT THIS REPAIR PRINTS"
    # while the row beneath it measured the length of the list below.  The
    # section carries 210 formatted values; this table classifies the ones the
    # repair OFFERS AS EVIDENCE.  Those are two populations and they are now
    # two rows -- V6a over this table, V6b over the 210.  The number is quoted
    # from the declaration rather than written in, because it moved once
    # (mg-843d) and a second copy of it is a second thing to forget.
    print("V6 -- the counts this repair OFFERS AS EVIDENCE, each classified and "
          "each ANCHORED in the artifact.  A count that could not have come out "
          "otherwise is labelled FORCED and is not offered as evidence anywhere "
          "in the repair.  This table is NOT every value the section prints -- "
          "that population is V6b's, and it is %d (of which %d are printed; see "
          "V6d)." % (CENSUS_DECLARED["specifiers"],
                     CENSUS_REACH_DECLARED["printed"]))
    for what, verdict, why, _ in TABLE:
        print("    %-22s %s  -- %s" % (verdict, what, why))
    forced = sum(1 for _, v, _, _ in TABLE if v.startswith("FORCED"))
    print("    (%d of the %d entries are FORCED.  PRINTED, NOT SCORED: it is a "
          "count of this file's own rows, and scoring it is what mg-fcb2's F2 "
          "was about.)" % (forced, len(TABLE)))

    missing = unanchored(art)
    check("V6a ANCHORED -- every one of the %d classified counts is still "
          "printed in the artifact, matched verbatim (population: the entries "
          "of TABLE; grain: one entry)" % len(TABLE),
          not missing, "unanchored: %s" % (missing if missing else "none"))

    got = census(open(os.path.join(PROBE, "controls.py")).read())
    check("V6b CENSUS -- NEGATIVE CONTROL 4 prints %d formatted values and no "
          "count has been added or removed since this table was written "
          "(population: the %%-format expressions lexically inside "
          "`negative_control_incidence`; grain: one conversion specifier).  A "
          "TRIPWIRE: it does not check that the %d entries above are the right "
          "ones, only that the set of printed values has not moved underneath "
          "them" % (CENSUS_DECLARED["specifiers"], len(TABLE)),
          got == CENSUS_DECLARED,
          "measured %s; declared %s" % (got, CENSUS_DECLARED))

    # V6d.  THE ROW THAT ANSWERS V6b'S NEXT FIRING (mg-843d).  V6b says the set
    # of formatted values moved; it has never been able to say WHICH KIND of
    # value, and that is the whole distance between "the artifact gained a
    # count nobody classified" -- the thing this instrument exists to catch --
    # and "a branch nobody runs gained a `%d`".  Both move V6b by the same
    # amount and they are opposite events.  Here they are separated, and the
    # separation is checked to PARTITION the census rather than to sit beside
    # it: the three fates sum to V6b's own declared total, so a specifier
    # cannot fall out of both rows at once.
    reach, where, probed_art = census_reach(PROBE)
    total = sum(reach.values())
    check("V6d REACH -- of the %d formatted values V6b counts, %d are PRINTED "
          "in the artifact, %d sit in a branch the run never reaches and %d are "
          "evaluated and discarded (population: V6b's; grain: one conversion "
          "specifier, assigned to exactly one fate).  The three sum to V6b's "
          "declared total, and the probed run is byte-identical to the "
          "committed artifact -- both scored here and neither assumed, so this "
          "row cannot report a split of a different number, or of a different "
          "document, than the one V6b and V6c guard"
          % (CENSUS_DECLARED["specifiers"], CENSUS_REACH_DECLARED["printed"],
             CENSUS_REACH_DECLARED["unreached"],
             CENSUS_REACH_DECLARED["discarded"]),
          reach == CENSUS_REACH_DECLARED
          and total == CENSUS_DECLARED["specifiers"]
          and probed_art == art,
          "measured %s (sum %d against V6b's %d); declared %s; unreached at "
          "controls.py line(s) %s, discarded at line(s) %s; probed run %d bytes "
          "against the artifact's %d"
          % (reach, total, CENSUS_DECLARED["specifiers"], CENSUS_REACH_DECLARED,
             where["unreached"] or "none", where["discarded"] or "none",
             len(probed_art), len(art)))

    # -- V7: the count mg-fcb2's F1 was about, re-derived ------------------
    # The site count is asked here of `top_laplacians` directly, not of
    # `mutation_applied_at_site`, so a change to that helper cannot make this
    # file agree with controls.py by construction.  What this row CANNOT do is
    # tell whether 86/86 is the right answer for the right reason -- it is one
    # more route to one number.  The evidence that the number is a MEASUREMENT
    # and not a property is the pair of constructed inputs that move it, and
    # that lives in probe_f1_count_moves.py, not here.
    print("V7 -- the site count mg-fcb2's F1 was about (mg-8af0)")
    site = sum(1 for P in ps
               if top_laplacians(P, incidence_mode="facet_offbyone")["facets"]
               != top_laplacians(P)["facets"])
    check("`le_to_facet` is corrupted at the SITE on %d/%d posets (population: "
          "the 86 posets 2 <= n <= 5; grain: one poset), re-derived from "
          "top_laplacians, and the artifact prints the SAME numerator -- which "
          "it did before the repair too, because the tautology `%% (N, N, ...)` "
          "had the right digits and the wrong sentence" % (site, N),
          site == 86 and "corrupted on %d/%d posets" % (site, N) in art,
          "the two inputs that separate the measurement from the tautology are "
          "run in code/face_geometry_repair_8af0/probe_f1_count_moves.py, not "
          "here: n = 1 admitted gives 86/87 and a no-op corruption gives 0/86, "
          "against 87/87 and 86/86 from the expression this replaces")

    fresh = regenerate(PROBE)
    check("V6c REGENERATED -- controls_output.txt is byte-identical to a fresh "
          "`controls.py 5`, so a count cannot be added to the artifact without "
          "moving V6b (this closes the one channel V6b cannot see: a "
          "hand-edited or stale artifact)",
          fresh == art,
          "fresh %d bytes / %d lines, committed %d bytes / %d lines"
          % (len(fresh), fresh.count("\n"), len(art), art.count("\n")))

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
