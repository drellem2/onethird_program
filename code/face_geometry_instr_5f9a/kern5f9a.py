"""mg-5f9a -- shared kernel for the instrumented-predicate landing.

WHAT THIS LANDING HAD TO DO DIFFERENTLY.  Two previous tickets wrote a sentence
saying WHY `absorbable_by_diagonal_twist` answered as it did, and both sentences
were produced beside the predicate rather than by it:

  mg-8a12  read `diag_preserved` and printed "the off-diagonal signs actually
           decide".  mg-f1b2 refuted it.
  mg-da45  replaced it with `deciding_gate`, which tested ALL diagonals and then
           ALL magnitudes.  The predicate interleaves the two BY ROW, so the two
           orders named different gates on 57 of the 297 biting pairs, and
           mg-1c80's M2 -- delete the gate the artifact called decisive --
           regenerated the artifact BYTE-IDENTICALLY.

So this landing does not write a third reason.  The predicate is instrumented:
`face_complex.absorb_trace` returns the gate it returned at and the number of
signs it read, and `absorbable_by_diagonal_twist` is a wrapper over it.  What
the rows print comes out of the code path.

WHAT THIS FILE IMPORTS, and it matters (mg-da45's rule, kept).  `face_complex`
and `posets` and nothing else.  `controls.py` is never imported: it is run as a
subprocess and read as bytes, so it cannot supply the evidence that it is right.
The pair (E.L^rel.E, D-A) is rebuilt here from `top_laplacians` and
`at_laplacian` rather than taken from `controls.claim1_pair`.

AND THE DECISION IS RE-DECIDED HERE, twice, without the union-find: by BFS
2-colouring of the sign-constraint graph, and (where m <= 8) by brute force over
all 2^m sign vectors.  A refactor of a decision procedure is only decision-
preserving if something outside it says so.
"""

import ast
import collections
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "..", "face_geometry")))

from face_complex import (                                          # noqa: E402
    top_laplacians, at_laplacian, linear_extensions, perm_sign,
)

FG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",
                                  "face_geometry"))
BAR = "=" * 78

MODES = ["ridge_facets", "split_free_as_interior", "ridge_drop",
         "facet_offbyone"]
ROW = {"ridge_facets": "I1", "split_free_as_interior": "I2",
       "ridge_drop": "I3", "facet_offbyone": "I4"}


def head(title):
    print("\n" + BAR + "\n" + title + "\n" + BAR)


def pair(P, sign_mode="true", incidence_mode="true"):
    """(E . L^rel_top . E, D - A) -- claim (1)'s two sides, rebuilt here."""
    td = top_laplacians(P, sign_mode=sign_mode, incidence_mode=incidence_mode)
    les, L = td["les"], td["L_rel"]
    s = [perm_sign(w) for w in les]
    m = len(les)
    twisted = [[s[i] * L[i][j] * s[j] for j in range(m)] for i in range(m)]
    return twisted, at_laplacian(P)[1]


def eq(A, B):
    return len(A) == len(B) and all(
        len(A[i]) == len(B[i]) and A[i] == B[i] for i in range(len(A)))


# ------------------------------------------------------------------ deciders
def absorbable_2colour(A, B):
    """S.A.S == B for a diagonal sign matrix S?  Decided by 2-colouring the
    graph of forced sign products, with no union-find anywhere."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return False
    for i in range(m):
        for j in range(m):
            if abs(A[i][j]) != abs(B[i][j]):
                return False
            if i == j and A[i][j] != B[i][j]:
                return False
    colour = [None] * m
    for root in range(m):
        if colour[root] is not None:
            continue
        colour[root] = 0
        stack = [root]
        while stack:
            x = stack.pop()
            for y in range(m):
                if x == y or A[x][y] == 0:
                    continue
                need = 0 if B[x][y] == A[x][y] else 1
                want = colour[x] ^ need
                if colour[y] is None:
                    colour[y] = want
                    stack.append(y)
                elif colour[y] != want:
                    return False
    return True


def absorbable_bruteforce(A, B):
    """The definition, enumerated: is there s in {+1,-1}^m with s_i A_ij s_j =
    B_ij for every i, j?  Only used where m <= 8."""
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return False
    for bits in range(1 << m):
        s = [1 - 2 * ((bits >> i) & 1) for i in range(m)]
        if all(s[i] * A[i][j] * s[j] == B[i][j]
               for i in range(m) for j in range(m)):
            return True
    return False


# ------------------------------------------------- the reason that was wrong
def priority_gate(A, B):
    """mg-da45's `deciding_gate`, VERBATIM, kept here as the thing this landing
    replaced -- ALL diagonals tested, then ALL magnitudes.

    It is not called by anything in `face_geometry` any more.  It lives here so
    the disagreement mg-1c80 measured can be re-measured against the trace the
    predicate now emits, rather than taken on trust from the audit's transcript.
    """
    m = len(A)
    if m != len(B) or any(len(A[i]) != len(B[i]) for i in range(m)):
        return "shape"
    if any(A[i][i] != B[i][i] for i in range(m)):
        return "diagonal"
    if any(abs(A[i][j]) != abs(B[i][j]) for i in range(m) for j in range(m)):
        return "magnitude"
    return "parity"


# ------------------------------------------------------- mutation machinery
def mutate_tree(edits, src_files=None):
    """Copy `face_geometry` to a temporary directory, apply (file, old, new)
    edits to the copy, and return the directory.

    NOTHING under ../face_geometry is written.  `old` must occur exactly once in
    its file; a patch that does not apply is an error and not a silent pass,
    because a mutation that was never applied looks exactly like a mutation the
    battery did not notice.
    """
    tmp = tempfile.mkdtemp(prefix="mg5f9a-")
    for f in (src_files or os.listdir(FG)):
        s = os.path.join(FG, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(tmp, f))
    for fname, old, new in edits:
        path = os.path.join(tmp, fname)
        text = open(path).read()
        if text.count(old) != 1:
            raise SystemExit("patch anchor occurs %d times in %s, expected 1:\n%r"
                             % (text.count(old), fname, old[:120]))
        open(path, "w").write(text.replace(old, new))
    return tmp


def run_controls(cwd, nmax=5):
    """Run the control battery in `cwd` and return (stdout, exit code).  Never
    tee'd: the committed artifact is not touched by any run in this instrument."""
    r = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout, r.returncode


# ------------------------------------------- the unit a patch removes, DERIVED
# mg-c4c8's OPEN 2, and the reason this section exists rather than a proofreading
# pass.  mg-9220 required every mutation to DECLARE the unit it removes and wrote
# the declarations by hand; on 8 of its 11 the declaration said "one `return`
# statement" and the patch removed the `return` TOGETHER WITH THE `if` THAT
# GUARDS IT, and on one of those it removed a two-clause condition as well.  The
# declaration is what a reader consults instead of the diff, so a declaration
# that understates its patch makes the deletion evidence look finer-grained than
# it is, and it does so invisibly.
#
# A DECLARATION THAT IS COMPUTED FROM THE PATCH CANNOT DISAGREE WITH IT.  That is
# the whole of the fix: not a check that the sentence matches the diff -- which
# is another preserved generator with a gate watching it -- but no sentence.
# These functions take (source, patch) and return the units the patch removes,
# so the declaration is correct at whatever grain the patch operates at without
# anyone deciding in advance which grain that is.  A mutation that starts
# removing a clause, a comprehension or a whole function declares that, on the
# run in which it starts doing it.
UnitDelta = collections.namedtuple(
    "UnitDelta", "returns statements clauses labels where nodes text")


def unit_census(src):
    """(returns, OTHER statements, boolean clauses) of a source text.

    `pass` is not counted as a statement: a patch that replaces a statement with
    `pass` has removed it, and counting the `pass` would report that nothing
    went.  Clauses are counted as `len(values) - 1` per `BoolOp`, so a condition
    written without `and`/`or` contributes none -- which is the state
    `absorb_trace`'s `shape` guard is in after mg-64b6, and the reason there is
    no fourth rung at that site.
    """
    tree = ast.parse(src)
    rets = sum(1 for n in ast.walk(tree) if isinstance(n, ast.Return))
    stmts = sum(1 for n in ast.walk(tree)
                if isinstance(n, ast.stmt) and not isinstance(n, ast.Pass))
    clauses = sum(len(n.values) - 1 for n in ast.walk(tree)
                  if isinstance(n, ast.BoolOp))
    return rets, stmts - rets, clauses


def _strings(src):
    return collections.Counter(
        n.value for n in ast.walk(ast.parse(src))
        if isinstance(n, ast.Constant) and isinstance(n.value, str))


def enclosing_def(src, anchor):
    """The innermost `def` containing the text `anchor` occupies in `src`.

    Derived from the patch's own position, not named beside it: a mutation that
    is moved to another function reports the other function.
    """
    at = src.find(anchor)
    if at < 0:
        return "?"
    first = src.count("\n", 0, at) + 1
    last = first + anchor.rstrip("\n").count("\n")
    best = None
    for node in ast.walk(ast.parse(src)):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if node.lineno <= first and last <= (node.end_lineno or node.lineno):
            if best is None or node.lineno > best.lineno:
                best = node
    return best.name if best is not None else "module level"


def apply_edits(src, edits):
    """`src` with every (file, old, new) of `edits` applied, each anchor
    required to occur exactly once.  The same operation `mutate_tree` performs
    on disk, on a string, so a declaration can be computed from the same
    (source, patch) pair the battery is about to run."""
    out = src
    for _fname, old, new in edits:
        if out.count(old) != 1:
            raise SystemExit("anchor occurs %d times, expected 1: %r"
                             % (out.count(old), old[:80]))
        out = out.replace(old, new)
    return out


def unit_removed(src, edits, nodes=True):
    """THE DECLARATION OF WHAT `edits` REMOVE, COMPUTED FROM `src` AND `edits`.

    `src` must be the source the mutation is actually applied to -- the same
    text, in the same call, so the declaration and the run cannot drift apart by
    one being updated and the other not.  Returns a `UnitDelta` whose `.text` is
    the sentence printed beside the result.

    Nothing here is a reading of English.  The counts come from parsing both
    trees; the labels come from the string constants the patch removes, so a
    patch that deletes `return Trace(False, "shape", 0)` says `shape` because
    the string went, not because someone typed it.

    AND THE COUNT THAT HAS NO GRAIN.  `returns`, `statements` and `clauses` are
    three chosen units, so this function can be wrong about a patch in exactly
    the way mg-9220's sentences were: by removing something none of the three
    names.  `nodes` -- every syntax-tree node, of any kind -- is reported
    alongside them for that reason.  A patch with nodes removed and 0/0/0 in the
    named units is one whose declaration is coarser than its patch, which is
    this file's own defect at the next rung down and is scored as such.
    """
    mut = apply_edits(src, edits)
    before, after = unit_census(src), unit_census(mut)
    r, s, c = (before[0] - after[0], before[1] - after[1], before[2] - after[2])
    gone = _strings(src) - _strings(mut)
    labels = sorted(k for k in gone if k)
    where = sorted({enclosing_def(src, old) for _f, old, _n in edits})
    n_nodes = (len(list(ast.walk(ast.parse(src))))
               - len(list(ast.walk(ast.parse(mut))))) if nodes else 0
    text = ("%d `return`, %d other statement(s), %d boolean clause(s), %d "
            "syntax node(s) in all, from %s"
            % (r, s, c, n_nodes, ", ".join("`%s`" % w for w in where)))
    if labels:
        text += "; string(s) removed with it: %s" % ", ".join(
            repr(x if len(x) <= 24 else x[:21] + "...") for x in labels)
    return UnitDelta(r, s, c, labels, where, n_nodes, text)


def finest_unit(delta):
    """The FINEST unit this patch perturbs, named from the same measurement.

    mg-c4c8's OPEN 1, second half: state beside the test the finest unit it
    perturbs, so a reader knows what the evidence covers instead of assuming it
    reaches all the way down.  A deletion result is a claim about the removed
    text AS A WHOLE; if that text contains a boolean clause, the clause is not
    what was tested, and this says so in the line the result is read on.
    """
    if delta.clauses > 0:
        return ("a CONDITION of %d clause(s) -- and the clauses inside it are "
                "NOT individually tested by this line" % (delta.clauses + 1))
    if delta.returns > 0 and delta.statements > 0:
        return ("a `return` together with the %d statement(s) that carry it -- "
                "no clause is removed, so nothing finer than this exists in the "
                "removed text" % delta.statements)
    if delta.returns > 0:
        return "one `return` statement, and nothing finer is removed"
    if delta.statements > 0:
        return "%d statement(s), no `return` among them" % delta.statements
    return ("no statement and no clause: the patch REWRITES rather than "
            "removes, and the unit is the rewritten expression")


def splice(src, node, text):
    """Replace the source span of `node` with `text`.

    Used for the clause sweep, where the mutation is 'this operand of this
    `or`', which no string anchor can name without naming the rest of the
    condition too.
    """
    lines = src.split("\n")
    starts = [0]
    for ln in lines:
        starts.append(starts[-1] + len(ln) + 1)
    a = starts[node.lineno - 1] + node.col_offset
    b = starts[node.end_lineno - 1] + node.end_col_offset
    return src[:a] + text + src[b:]


DecidingClause = collections.namedtuple(
    "DecidingClause", "func kind index total node op source")


def deciding_clauses(src):
    """Every top-level clause of every boolean condition that DECIDES A RETURN,
    read out of the tree.

    'Decides a return' is either the test of an `if` whose body returns, or the
    value of a `return` itself.  The population is enumerated rather than
    listed, so a clause added to the predicate layer appears here without anyone
    remembering to add it -- which is the treatment mg-c4c8 asked for one level
    up ("run the deletion test over the enumerated returns of the predicate
    layer rather than over a hand-written table").
    """
    tree = ast.parse(src)
    scope = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    scope[sub] = node.name
    out = []

    def name_of(fn):
        base = scope.get(fn)
        return "%s.%s" % (base, fn.name) if base else fn.name

    for fn in [n for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        for node in ast.walk(fn):
            cond, kind = None, None
            if isinstance(node, ast.If) and any(
                    isinstance(s, ast.Return) for s in ast.walk(node)):
                cond, kind = node.test, "guard"
            elif isinstance(node, ast.Return) and node.value is not None:
                cond, kind = node.value, "value"
            if not isinstance(cond, ast.BoolOp):
                continue
            op = "or" if isinstance(cond.op, ast.Or) else "and"
            for k, value in enumerate(cond.values):
                out.append(DecidingClause(
                    name_of(fn), kind, k, len(cond.values), cond, op,
                    ast.get_source_segment(src, value)))
    return out


def drop_clause(src, clause):
    """`src` with one clause of one boolean condition removed and the rest of
    the condition kept.  The whole statement stays: this is the deletion test
    one level below a `return`."""
    kept = [v for k, v in enumerate(clause.node.values) if k != clause.index]
    text = (" %s " % clause.op).join(
        "(%s)" % ast.get_source_segment(src, v) for v in kept)
    if len(kept) == 1:
        text = ast.get_source_segment(src, kept[0])
    return splice(src, clause.node, text)


def tree_with_source(fname, text, src_files=None):
    """A copy of `face_geometry` with `fname` replaced by `text`, for a mutation
    that is computed rather than spelled as a (old, new) pair."""
    tmp = mutate_tree([], src_files)
    with open(os.path.join(tmp, fname), "w") as fh:
        fh.write(text)
    return tmp


def source_at(ref, fname="face_complex.py"):
    """The committed text of a `face_geometry` file at `ref`; the live worktree
    file when `ref` is None."""
    if ref is None:
        return open(os.path.join(FG, fname)).read()
    repo = os.path.abspath(os.path.join(FG, "..", ".."))
    r = subprocess.run(["git", "show", "%s:code/face_geometry/%s" % (ref, fname)],
                       cwd=repo, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("cannot read %s:code/face_geometry/%s" % (ref, fname))
    return r.stdout


PRE_REPAIR_REF = "5cae82c^"
"""The tree the BEFORE half of the deletion test is about: the commit before
mg-5f9a instrumented the predicate.

IT WAS `main`, AND `main` IS A MOVING TARGET (mg-04a8).  As written this file
read `main:code/face_geometry/...`, which was the pre-repair tree only until
mg-5f9a merged.  After that merge the BEFORE half was reading the tree it was
supposed to be contrasting with, and its first claim -- "main's committed
controls_output.txt regenerates from main's sources" -- became a statement that
this tree regenerates from itself.  It cannot go red for any reason a reader of
that sentence would care about.  The deletion it then attempts does not even
apply: re-running the shipped file today stops at `BEFORE-1: anchor occurs 0
times in main's face_complex.py`.

A check pinned to a branch answers a question about whatever that branch holds
today.  A check pinned to a commit answers the question it was written to ask.
"""


TWO_RETURN_REF = "c7f9673"
"""The tree the PER RETURN half of the deletion test is about: mg-04a8, the last
commit in which `absorb_trace`'s `shape` gate had TWO `return` statements.

mg-9220 merged them into one, so the granularity finding cannot be reproduced on
this tree -- there is nothing left to delete one of.  It is reproduced against
this commit instead, for the reason `PRE_REPAIR_REF` gives: a check pinned to a
commit answers the question it was written to ask, and "delete only the first of
the two `shape` returns" is a question about a tree where there are two.
"""


def load_module(path, name):
    """Import a single .py file under a chosen module name.

    Used to hold THIS tree's `absorb_trace` and the pinned tree's side by side
    in one process.  `face_complex.py` imports nothing local, so a file loaded
    this way is the whole implementation and not a stub over the live one.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_ref_tree(files, ref=PRE_REPAIR_REF):
    """Materialise a named commit's copy of the named face_geometry files in a
    temp dir, and return (dir, resolved sha).

    Used for the BEFORE half of the deletion test: mg-1c80's finding is that the
    deletion left the artifact byte-identical AT THAT COMMIT, and a landing that
    only shows the AFTER half is asking to be believed about the before.  The
    resolved sha is returned so the transcript records WHICH tree was measured
    rather than a branch name that will mean something else next week.
    """
    tmp = tempfile.mkdtemp(prefix="mg5f9a-ref-")
    repo = os.path.abspath(os.path.join(FG, "..", ".."))
    sha = subprocess.run(["git", "rev-parse", ref], cwd=repo,
                         capture_output=True, text=True)
    if sha.returncode != 0:
        raise SystemExit("cannot resolve %s" % ref)
    for f in files:
        blob = subprocess.run(["git", "show", "%s:code/face_geometry/%s" % (ref, f)],
                              cwd=repo, capture_output=True)
        if blob.returncode != 0:
            raise SystemExit("cannot read %s:code/face_geometry/%s" % (ref, f))
        open(os.path.join(tmp, f), "wb").write(blob.stdout)
    return tmp, sha.stdout.strip()
