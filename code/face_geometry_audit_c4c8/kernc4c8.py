"""mg-c4c8 -- shared kernel for the INDEPENDENT AUDIT of the mg-e7bc repair
(mg-9220 / b6bc2ef).

WHAT THIS FILE IS AND WHAT IT DELIBERATELY IS NOT.  It is a deletion harness
that works on the SYNTAX TREE, not on anchor strings.  The subject's
`kern5f9a.mutate_tree` and mg-e7bc's `kerne7bc` both patch by `text.replace(old,
new)` with `old` a literal block copied out of the source; that is a perfectly
good way to run a mutation someone has already chosen, and it is a useless way
to ENUMERATE the mutations that exist, because the enumeration is then the
author's list rather than the file's contents.

The whole subject of this audit is a UNIT: mg-e7bc found a deletion applied at
the granularity of a gate and read at the granularity of a return.  An auditor
who takes the unit list from the subject cannot find the next one.  So here the
units are read out of `ast`:

  * `returns(path)`      -- EVERY `return` statement in a file, with the
                            function it belongs to.  Not a list; a walk.
  * `delete_return`      -- one of them replaced by `pass` at its own
                            indentation.  `pass` and not deletion-of-lines
                            because a `return` that is the only statement of its
                            block cannot be removed without removing the block,
                            and removing the block is a different mutation.
  * `guard_clauses(path)`-- every top-level `or`/`and` clause of every `if` test
                            that guards a `return`, and every clause of a
                            `return` whose VALUE is a boolean expression.  This
                            is the unit one level below a return, which is where
                            mg-9220 put the statement mg-e7bc found inert.
  * `delete_clause`      -- one clause removed, the rest of the condition kept.

NOTHING UNDER ../face_geometry IS WRITTEN.  Every mutant is a full copy in a
temporary directory and every battery run captures stdout instead of tee-ing it
(mg-f922).

CLAIMS vs FINDINGS.  A [BROKEN] claim means THIS instrument is wrong and sets the
exit status.  A [FINDING] means the subject is; it is counted and printed and
does not set the status.  An audit whose exit code conflates the two cannot be
run in CI by anyone.
"""

import ast
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FG = os.path.join(ROOT, "code", "face_geometry")
INSTR = os.path.join(ROOT, "code", "face_geometry_instr_5f9a")
E7BC = os.path.join(ROOT, "code", "face_geometry_audit_e7bc")
FC = os.path.join(FG, "face_complex.py")
ART = os.path.join(FG, "controls_output.txt")

BAR = "=" * 78

SCORE = []
FINDINGS = []

MARKERS = ("[PASS]", "[FAIL]", "[CANNOT FAIL]")

# The two commits the subject pins.  Re-resolved here and audited in h4; a pin
# is a claim about history and this audit does not take it on trust.
TWO_RETURN_REF = "c7f9673"          # kern5f9a.TWO_RETURN_REF
PRE_REPAIR_REF = "5cae82c^"         # kern5f9a.PRE_REPAIR_REF
REPAIR_COMMIT = "b6bc2ef"           # mg-9220, the repair under audit


def head(title):
    print("\n" + BAR + "\n" + title + "\n" + BAR)


def claim(ok, text, differs_under, detail=""):
    """Score one claim OF THIS INSTRUMENT.  `differs_under` is required by
    position, not by convention: a claim whose author cannot name a change that
    would flip it is measuring something invariant under the failure it is read
    as guarding (mg-d0e2's rule, applied to this file too)."""
    SCORE.append(bool(ok))
    print("  [%s] %s" % ("HOLDS " if ok else "BROKEN", text))
    if detail:
        print("        " + detail)
    print("        WOULD DIFFER UNDER: %s" % differs_under)


def finding(cond, text):
    if cond:
        FINDINGS.append(text)
        print("  [FINDING] %s" % text)
    return bool(cond)


def read(path):
    with open(path) as fh:
        return fh.read()


# --------------------------------------------------------------------------
# the units, read out of the syntax tree
# --------------------------------------------------------------------------

class _Qual(ast.NodeVisitor):
    """Qualified names, so a return can be named by the function it is in."""

    def __init__(self):
        self.stack = []
        self.returns = []
        self.ifs = []

    def visit_FunctionDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_ClassDef(self, node):
        self.stack.append(node.name)
        self.generic_visit(node)
        self.stack.pop()

    def visit_Return(self, node):
        self.returns.append((".".join(self.stack), node))
        self.generic_visit(node)

    def visit_If(self, node):
        self.ifs.append((".".join(self.stack), node))
        self.generic_visit(node)


def _walk(src):
    v = _Qual()
    v.visit(ast.parse(src))
    return v


def returns(src):
    """[(index, qualname, lineno, source text, node)] for EVERY return."""
    out = []
    for i, (qual, node) in enumerate(_walk(src).returns, 1):
        out.append((i, qual, node.lineno, ast.get_source_segment(src, node),
                    node))
    return out


def _splice(src, lineno, col, end_lineno, end_col, replacement,
            allow_prefix=False):
    """Replace one source span.  `allow_prefix` is False for STATEMENTS -- a
    statement with code before it on its line cannot be replaced without
    touching the other statement, and silently doing so would be a mutation
    larger than the one being reported.  Expressions (a clause, an `if` test)
    always have code before them and pass True."""
    lines = src.split("\n")
    a, b = lineno - 1, end_lineno - 1
    before = lines[a][:col]
    after = lines[b][end_col:]
    if before.strip() and not allow_prefix:
        raise SystemExit("cannot splice: code precedes the unit at line %d"
                         % lineno)
    return "\n".join(lines[:a] + [before + replacement + after] + lines[b + 1:])


def delete_return(src, node):
    """`src` with exactly this one `return` statement replaced by `pass`.

    The statement is gone; the block it lived in is not.  Deleting the lines
    outright would delete the enclosing `if` on eight of this file's returns,
    which is a strictly larger unit and would put this instrument in the error
    it was written to look for.
    """
    return _splice(src, node.lineno, node.col_offset,
                   node.end_lineno, node.end_col_offset, "pass")


def guard_clauses(src):
    """[(qualname, kind, k, n, clause text, node, whole)] -- one entry per
    top-level clause of a boolean condition that decides a `return`.

    Two kinds, both of them the unit BELOW a return statement:

      "guard"  a clause of the `if` test of an `if` whose body is a single
               `return` -- the shape mg-9220 created when it merged two
               `return`s into one condition with two clauses;
      "value"  a clause of a `return`'s own boolean value expression.
    """
    v = _walk(src)
    out = []
    for qual, node in v.ifs:
        if not isinstance(node.test, ast.BoolOp):
            continue
        if not any(isinstance(s, ast.Return) for s in node.body):
            continue
        vals = node.test.values
        for k, val in enumerate(vals):
            out.append((qual, "guard", k, len(vals),
                        ast.get_source_segment(src, val), val, node.test))
    for qual, node in v.returns:
        if node.value is None or not isinstance(node.value, ast.BoolOp):
            continue
        vals = node.value.values
        for k, val in enumerate(vals):
            out.append((qual, "value", k, len(vals),
                        ast.get_source_segment(src, val), val, node.value))
    return out


def delete_clause(src, boolop, k):
    """`src` with clause `k` removed from `boolop` and the rest kept.

    A one-clause remainder is spliced in bare; two or more are re-joined with
    the original operator.  `ast.unparse` writes the remainder, so the mutant's
    formatting is this file's and not the subject's -- which is the point: a
    mutation generated from the tree cannot silently inherit an anchor string
    the subject chose.
    """
    keep = [v for i, v in enumerate(boolop.values) if i != k]
    if not keep:
        raise SystemExit("removing the only clause is a different mutation")
    new = ast.BoolOp(op=boolop.op, values=keep) if len(keep) > 1 else keep[0]
    return _splice(src, boolop.lineno, boolop.col_offset,
                   boolop.end_lineno, boolop.end_col_offset, ast.unparse(new),
                   allow_prefix=True)


def count_returns(src):
    return len(_walk(src).returns)


def return_labels(src, funcname):
    """The literal gate labels at the `return` sites of one function, in source
    order.  Used to check a mutation removed the return it says it removed."""
    out = []
    for _i, qual, _ln, _txt, node in returns(src):
        if qual != funcname:
            continue
        lab = None
        if isinstance(node.value, ast.Call):
            for a in node.value.args:
                if isinstance(a, ast.Constant) and isinstance(a.value, str):
                    lab = a.value
                    break
        out.append(lab)
    return out


# --------------------------------------------------------------------------
# running the battery
# --------------------------------------------------------------------------

def tree_from_worktree(files=None):
    """A copy of ../face_geometry in a temp dir."""
    tmp = tempfile.mkdtemp(prefix="mgc4c8-")
    for f in (files or os.listdir(FG)):
        s = os.path.join(FG, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(tmp, f))
    return tmp


def tree_from_ref(ref, files=("face_complex.py", "posets.py", "controls.py",
                              "run_probe.py")):
    """A named commit's copy of the same files, plus the resolved sha."""
    tmp = tempfile.mkdtemp(prefix="mgc4c8-ref-")
    sha = subprocess.run(["git", "rev-parse", ref], cwd=ROOT,
                         capture_output=True, text=True)
    if sha.returncode != 0:
        raise SystemExit("cannot resolve %s" % ref)
    for f in files:
        blob = subprocess.run(
            ["git", "show", "%s:code/face_geometry/%s" % (ref, f)],
            cwd=ROOT, capture_output=True)
        if blob.returncode != 0:
            raise SystemExit("cannot read %s:%s" % (ref, f))
        with open(os.path.join(tmp, f), "wb") as fh:
            fh.write(blob.stdout)
    return tmp, sha.stdout.strip()


def run_battery(cwd, nmax=5, timeout=120):
    """(stdout, exit code).  stderr is dropped on purpose: a mutant that
    tracebacks writes to stderr, and the ARTIFACT is stdout.  What the battery
    would have committed is what is compared."""
    try:
        r = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=cwd,
                           capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "", 124
    return r.stdout, r.returncode


def run_with_source(base_dir, filename, src, nmax=5):
    """Write `src` over one file of a copy of `base_dir` and run the battery."""
    tmp = tempfile.mkdtemp(prefix="mgc4c8-mut-")
    for f in os.listdir(base_dir):
        s = os.path.join(base_dir, f)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(tmp, f))
    with open(os.path.join(tmp, filename), "w") as fh:
        fh.write(src)
    out, code = run_battery(tmp, nmax)
    shutil.rmtree(tmp, ignore_errors=True)
    return out, code


def load_source(src, name):
    """Import a source string as a module.  `face_complex.py` imports nothing
    local, so a module loaded this way is the whole implementation."""
    import importlib.util
    tmp = tempfile.mkdtemp(prefix="mgc4c8-mod-")
    path = os.path.join(tmp, name + ".py")
    with open(path, "w") as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# artifact parsing -- re-derived here, not imported from the subject
# --------------------------------------------------------------------------

def scored_rows(text):
    """(marker, name) for every line whose first non-space characters are a
    marker.  Re-derived: the subject's `scored_rows` and mg-e7bc's are two more
    copies of the same four lines, and three independent copies that agree is
    worth more than one imported one."""
    rows = []
    for ln in text.split("\n"):
        s = ln.strip()
        for m in MARKERS:
            if s.startswith(m):
                rows.append((m, s[len(m):].strip()))
                break
    return rows


def retag(text, marker, pick=None):
    """Every scored row's marker replaced (optionally only where `pick(i)`)."""
    out, i = [], 0
    for ln in text.split("\n"):
        s = ln.lstrip()
        hit = next((m for m in MARKERS if s.startswith(m)), None)
        if hit is None:
            out.append(ln)
            continue
        keep = pick is not None and not pick(i)
        out.append(ln if keep
                   else ln[:len(ln) - len(s)] + marker + s[len(hit):])
        i += 1
    return "\n".join(out)


def summary_fail_names(text):
    names, mode = [], False
    for ln in text.split("\n"):
        if ln.startswith("CONTROLS FAILED:"):
            mode = True
            continue
        if mode and ln.startswith("   - "):
            names.append(ln[5:].rstrip().rstrip("."))
            continue
        if mode and ln and not ln.startswith("   - "):
            mode = False
    return names


def footer():
    print("\n" + BAR)
    print("%d claim(s) scored; %d BROKEN.  %d FINDING(s)."
          % (len(SCORE), SCORE.count(False), len(FINDINGS)))
    for f in FINDINGS:
        print("  FINDING: %s" % f)
    print(BAR)
    return 1 if not all(SCORE) else 0
