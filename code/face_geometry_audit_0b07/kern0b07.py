"""mg-0b07 -- independent audit of mg-64b6 (`0fb0e00`): the shared harness.

WHAT IS AND IS NOT IMPORTED FROM THE SUBJECT.  The thing under audit is a
DERIVED DECLARATION, so the one honest way to check it is to compute the same
quantity a second time from the same trees by different code and compare.  This
file therefore re-derives, from `ast` and from nothing else:

  * the unit census (returns / other statements / boolean clauses / raw nodes),
  * the enumeration of `return` statements and of boolean clauses,
  * the source splicer that replaces one node's span,
  * the battery runner and the row parser.

`code/face_geometry_instr_5f9a/kern5f9a.py` is NOT imported anywhere in this
audit.  `d2_deletion.py` IS imported, in `p2_units.py` only, and only for its
DATA TABLES -- `UNITS_AS_SHIPPED`, `SHIPPED_PATCHES`, `MUTATIONS`,
`SELF_DEFECT_BRANCHES`.  Those tables are the object under audit; auditing a
paraphrase of them would be worthless.  Every number this audit prints about
them is computed here.

NOTHING UNDER `code/face_geometry/` IS WRITTEN.  Every mutation is applied to a
copy in a temporary directory, every battery run captures stdout, and no run
uses `| tee` (mg-f922).

CLAIMS vs FINDINGS (mg-c4c8's convention, kept).  A `[BROKEN]` claim means THIS
instrument is wrong and sets the exit status.  A `[FINDING]` means the subject
is; it is counted and printed and does not.  An audit that cannot be run in CI
by someone who does not already know the answer is not an instrument.
"""

import ast
import collections
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FG = os.path.join(REPO, "code", "face_geometry")
INSTR = os.path.join(REPO, "code", "face_geometry_instr_5f9a")
BAR = "=" * 78

SCORE = []
FINDINGS = []


def head(title):
    print("\n" + BAR + "\n" + title + "\n" + BAR)


def claim(text, ok, differs_under, detail=""):
    """Score one claim of THIS audit's own.

    `differs_under` is mg-d0e2's requirement and it is kept: a claim whose
    author cannot name a change that would make it answer differently is
    measuring something invariant under the failure it is read as guarding.
    """
    SCORE.append(bool(ok))
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


def finding(tag, text, detail=""):
    """Record something the SUBJECT gets wrong.  Does not set the exit status."""
    FINDINGS.append(tag)
    print("  [FINDING %s] %s" % (tag, text))
    if detail:
        print("        " + detail)


def report():
    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN.  %d finding(s): %s"
          % (len(SCORE), SCORE.count(False), len(FINDINGS),
             ", ".join(FINDINGS) if FINDINGS else "none"))
    print(BAR)
    return 1 if not all(SCORE) else 0


# ------------------------------------------------------------------ sources
def source_at(ref, fname="face_complex.py", subdir="face_geometry"):
    """The committed text of a repository file at `ref`; the worktree file when
    `ref` is None."""
    rel = "code/%s/%s" % (subdir, fname)
    if ref is None:
        return open(os.path.join(REPO, rel)).read()
    r = subprocess.run(["git", "show", "%s:%s" % (ref, rel)], cwd=REPO,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("cannot read %s:%s" % (ref, rel))
    return r.stdout


# ------------------------------------------------------- the census, re-derived
Census = collections.namedtuple("Census", "returns statements clauses nodes")


def census(src):
    """(returns, OTHER statements, boolean clauses, raw nodes) of a source text.

    Written from the definitions rather than from the subject's `unit_census`,
    and deliberately in a different shape: one walk, four counters, and `nodes`
    included in the same tuple so the four are always read together.

    `pass` is not counted as a statement -- a patch that substitutes `pass` for
    a statement has removed it, and counting the `pass` would report that
    nothing went.  Clauses are `len(values) - 1` per `BoolOp`: a condition
    written with no `and`/`or` contributes none, and `a or b or c` contributes
    two, which is the number of operands that can be dropped while leaving a
    condition behind.
    """
    tree = ast.parse(src)
    r = s = c = n = 0
    for node in ast.walk(tree):
        n += 1
        if isinstance(node, ast.Return):
            r += 1
        elif isinstance(node, ast.stmt) and not isinstance(node, ast.Pass):
            s += 1
        if isinstance(node, ast.BoolOp):
            c += len(node.values) - 1
    return Census(r, s, c, n)


def delta(src, mut):
    """What `mut` removes relative to `src`, in the four channels."""
    a, b = census(src), census(mut)
    return Census(a.returns - b.returns, a.statements - b.statements,
                  a.clauses - b.clauses, a.nodes - b.nodes)


def strings_removed(src, mut):
    gone = (collections.Counter(_strs(src)) - collections.Counter(_strs(mut)))
    return sorted(k for k in gone if k)


def _strs(src):
    return [n.value for n in ast.walk(ast.parse(src))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def apply_edits(src, edits):
    """`src` with every (file, old, new) applied, each anchor required to occur
    exactly once.  A patch that does not apply is an error and never a silent
    pass: a mutation that was never applied looks exactly like one the battery
    did not notice."""
    out = src
    for _f, old, new in edits:
        if out.count(old) != 1:
            raise SystemExit("anchor occurs %d times, expected 1: %r"
                             % (out.count(old), old[:80]))
        out = out.replace(old, new)
    return out


# -------------------------------------------------------------- enumeration
Site = collections.namedtuple("Site", "func line node")


def returns_of(src, funcname):
    """Every `return` statement lexically inside `funcname`, in SOURCE order.

    Source order, not `ast.walk` order.  mg-c4c8's own slip was taking `[-1]`
    of a breadth-first walk and getting a different statement than the one its
    declaration named; the fix is to sort, and it is done here rather than
    inherited.
    """
    tree = ast.parse(src)
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if fn.name != funcname:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Return):
                out.append(Site(funcname, node.lineno, node))
    return sorted(out, key=lambda s: s.line)


def all_boolops(src):
    """EVERY `BoolOp` in a file, wherever it sits.

    The subject enumerates the clauses of conditions that DECIDE A RETURN,
    which is the population its sentence names.  This is the wider one, so the
    two can be compared instead of the narrower being read as the whole.
    """
    return [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.BoolOp)]


def deciding_boolops(src):
    """The subject's population, re-derived: the top-level boolean condition of
    an `if` whose body returns, or of a `return`'s own value."""
    tree = ast.parse(src)
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            cond = None
            if isinstance(node, ast.If) and any(
                    isinstance(s, ast.Return) for s in ast.walk(node)):
                cond = node.test
            elif isinstance(node, ast.Return) and node.value is not None:
                cond = node.value
            if isinstance(cond, ast.BoolOp):
                out.append((fn.name, cond))
    return out


def splice(src, node, text):
    """`src` with the source span of `node` replaced by `text`."""
    lines = src.split("\n")
    starts = [0]
    for ln in lines:
        starts.append(starts[-1] + len(ln) + 1)
    a = starts[node.lineno - 1] + node.col_offset
    b = starts[node.end_lineno - 1] + node.end_col_offset
    return src[:a] + text + src[b:]


def replace_stmt_with_pass(src, node):
    """`node`, a statement, replaced by `pass` at its own indentation.

    Not deleted as LINES.  Many of these returns are the only statement of
    their block, and removing the lines would remove the enclosing `if` -- a
    LARGER unit than the one declared, which is the error this whole lineage is
    about and which an auditor can commit as easily as a repairer.
    """
    return splice(src, getattr(node, "node", node), "pass")


# ---------------------------------------------------------------- the battery
def tree_with(fname, text, files=("face_complex.py", "posets.py",
                                  "controls.py", "run_probe.py")):
    """A copy of `code/face_geometry` with `fname` replaced by `text`."""
    tmp = tempfile.mkdtemp(prefix="mg0b07-")
    for f in files:
        s = os.path.join(FG, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(tmp, f))
    with open(os.path.join(tmp, fname), "w") as fh:
        fh.write(text)
    return tmp


def run_battery(cwd, nmax=5):
    """`controls.py nmax` in `cwd`; returns (stdout, exit code).  Never tee'd."""
    r = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout, r.returncode


def baseline():
    """The unmutated battery, run here rather than read from the committed
    artifact -- a committed artifact is a claim about a tree and this audit is
    about whether such claims hold."""
    return run_battery(tree_with("face_complex.py", source_at(None)))


def scored_rows(text):
    """(marker, text) for every line whose FIRST token is a scored marker.

    Re-derived: a substring scan counts prose bullets that quote a marker as
    rows, which is one half of the defect mg-d0e2 found in the shipped check.
    """
    out = []
    for ln in text.split("\n"):
        s = ln.strip()
        for m in ("[PASS]", "[FAIL]", "[CANNOT FAIL]"):
            if s.startswith(m):
                out.append((m, s[len(m):].strip()))
                break
    return out


# --------------------------------------------- a copy of the subject's instrument
def instrument_copy(edits=()):
    """A runnable copy of `code/face_geometry_instr_5f9a` in a temp tree, with
    `edits` -- (old, new) pairs -- applied to its `d2_deletion.py`.

    WHY A COPY AND NOT AN EDIT IN PLACE.  The question "is the declaration
    derived, or regenerated by hand?" is answered by changing the patch and
    seeing whether the declaration follows WITHOUT anyone touching the
    declaration.  Doing that to the worktree would leave the subject's own
    files modified while the answer was being read, which is the one state in
    which a green run proves nothing.

    The copy keeps the subject's own directory layout, because `kern5f9a`
    computes both the predicate directory and the repository root from
    `__file__`: `code/face_geometry` is symlinked (nothing writes to it) and
    the worktree's `.git` pointer file is copied so `git show` resolves the
    pinned commits exactly as it does in place.
    """
    tmp = tempfile.mkdtemp(prefix="mg0b07-instr-")
    os.makedirs(os.path.join(tmp, "code"))
    dot = os.path.join(REPO, ".git")
    if os.path.isfile(dot):
        shutil.copy2(dot, os.path.join(tmp, ".git"))
    else:
        os.symlink(dot, os.path.join(tmp, ".git"))
    os.symlink(FG, os.path.join(tmp, "code", "face_geometry"))
    dst = os.path.join(tmp, "code", "face_geometry_instr_5f9a")
    shutil.copytree(INSTR, dst)
    path = os.path.join(dst, "d2_deletion.py")
    text = open(path).read()
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit("instrument anchor occurs %d times, expected 1: %r"
                             % (text.count(old), old[:100]))
        text = text.replace(old, new)
    with open(path, "w") as fh:
        fh.write(text)
    return tmp, dst


def run_instrument(dst, script="d2_deletion.py"):
    r = subprocess.run([sys.executable, script], cwd=dst, capture_output=True,
                       text=True)
    return r.stdout + r.stderr, r.returncode


def declaration_line(text, tag):
    """The subject's own printed declaration for `tag`, taken out of its
    transcript by the marker it prints rather than by line number."""
    want = "%s -- " % tag
    for ln in text.split("\n"):
        if want in ln and "UNIT REMOVED, DERIVED FROM THE PATCH" in ln:
            return ln[ln.index("[UNIT REMOVED"):].strip()
    return None
