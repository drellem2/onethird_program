"""mg-eaef -- the harness for an independent audit of the mg-0b07 repair
(`bfd7948`, work item mg-f7e1).

INDEPENDENCE.  Nothing here imports `kern5f9a` -- the subject's kernel, and the
thing that computes both the declaration and the census under audit.  The AST
enumerators, the census, the splicer, the tree builder and the battery runner
are re-derived here from `ast` and `subprocess`.  The subject's `d2_deletion.py`
is RUN, as a subprocess, in a copied tree; it is never imported, so no table of
its is borrowed and every number printed about it is read out of its own stdout.

WHAT A CLAIM IS AND WHAT A FINDING IS.  A `[BROKEN]` claim means THIS instrument
is wrong, and it sets the exit status.  A `[FINDING]` means the SUBJECT is, and
it is counted and printed and does not.  An audit whose findings set the exit
status cannot be run in CI by anyone who does not already know the answer.
"""

import ast
import collections
import os
import shutil
import subprocess
import sys
import tempfile

BAR = "=" * 78
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FG = os.path.join(REPO, "code", "face_geometry")
INSTR = os.path.join(REPO, "code", "face_geometry_instr_5f9a")
AUDIT_0B07 = os.path.join(REPO, "code", "face_geometry_audit_0b07")

# The three files the battery needs.  Named rather than globbed so a stray file
# in the worktree cannot change what a mutated tree contains.
FILES = ("controls.py", "face_complex.py", "posets.py")

_claims = []
_findings = []


def head(title):
    print("\n" + BAR)
    print(title)
    print(BAR)


def claim(text, holds, would_differ, detail=None):
    """A claim about THIS instrument.  A False one sets the exit status."""
    _claims.append((text, bool(holds)))
    print("  [%s] %s" % ("HOLDS " if holds else "BROKEN", text))
    if detail:
        print("        %s" % detail)
    print("        WOULD DIFFER UNDER: %s" % would_differ)


def finding(tag, text, detail=None):
    """A finding about the SUBJECT.  Counted, printed, does not set exit."""
    _findings.append((tag, text))
    print("  [FINDING %s] %s" % (tag, text))
    if detail:
        print("        %s" % detail)


def report():
    print("\n" + BAR)
    bad = [c for c, ok in _claims if not ok]
    print("%d claim(s) scored; %d BROKEN.  %d finding(s)."
          % (len(_claims), len(bad), len(_findings)))
    for tag, text in _findings:
        print("   FINDING %-3s %s" % (tag, text.split(".")[0][:100]))
    print(BAR)
    return 1 if bad else 0


# --------------------------------------------------------------- trees, runs
def show(ref, path):
    """The committed text of `path` at `ref`, read from git."""
    r = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (ref, path)],
                       capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("git show %s:%s failed: %s" % (ref, path, r.stderr))
    return r.stdout


def source_at(ref, fname="face_complex.py"):
    if ref is None:
        return open(os.path.join(FG, fname)).read()
    return show(ref, "code/face_geometry/%s" % fname)


def build_tree(edits=(), ref=None, extra=None):
    """A temporary copy of the three battery files -- from the worktree when
    `ref` is None, else from that commit -- with `edits` applied.

    An anchor that does not occur EXACTLY ONCE is a hard error.  A patch that
    silently failed to apply looks exactly like a patch the battery did not
    notice, which is the confusion this whole lineage is about.
    """
    tmp = tempfile.mkdtemp(prefix="mg-eaef-")
    for f in FILES:
        open(os.path.join(tmp, f), "w").write(source_at(ref, f))
    for fname, text in (extra or {}).items():
        open(os.path.join(tmp, fname), "w").write(text)
    for fname, old, new in edits:
        path = os.path.join(tmp, fname)
        body = open(path).read()
        n = body.count(old)
        if n != 1:
            raise SystemExit("anchor occurs %d times in %s at ref %r:\n%r"
                             % (n, fname, ref, old[:160]))
        open(path, "w").write(body.replace(old, new))
    return tmp


def run_battery(cwd, nmax=5):
    """Run `controls.py` in `cwd`.  Never tee'd: no run here writes anything
    under code/face_geometry."""
    r = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=cwd,
                       capture_output=True, text=True)
    return r.stdout, r.returncode


# ------------------------------------------------------------ the AST census
def _scope(tree):
    out = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    out[sub] = node.name
    return out


def deciding_conditions(src):
    """(function, kind, node) for every condition that decides a `return`:
    the test of an `if` that contains one, and the value of a `return`."""
    tree = ast.parse(src)
    scope = _scope(tree)
    out = []
    for fn in [n for n in ast.walk(tree)
               if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        name = "%s.%s" % (scope[fn], fn.name) if fn in scope else fn.name
        for node in ast.walk(fn):
            if isinstance(node, ast.If) and any(
                    isinstance(s, ast.Return) for s in ast.walk(node)):
                out.append((name, "guard", node.test))
            elif isinstance(node, ast.Return) and node.value is not None:
                out.append((name, "value", node.value))
    return out


Operand = collections.namedtuple("Operand", "func kind index total op source "
                                            "node parent nested")


def boolean_operands(src, nested_too=True):
    """EVERY operand of EVERY `or`/`and` inside a deciding condition.

    THE DIFFERENCE FROM THE SUBJECT'S ENUMERATOR IS THE ONE THING THIS FUNCTION
    IS FOR.  `kern5f9a.deciding_clauses` takes the condition, asks whether the
    condition ITSELF is a `BoolOp`, and enumerates its top-level operands.  A
    boolean operator that sits INSIDE the condition -- under a comprehension,
    under a quantifier -- has operands that are explicit, spelled with the
    operator, and invisible to that enumerator.  This one walks.
    """
    out = []
    for func, kind, cond in deciding_conditions(src):
        for node in ast.walk(cond):
            if not isinstance(node, ast.BoolOp):
                continue
            nested = node is not cond
            if nested and not nested_too:
                continue
            op = "or" if isinstance(node.op, ast.Or) else "and"
            for k, value in enumerate(node.values):
                out.append(Operand(func, kind, k, len(node.values), op,
                                   ast.get_source_segment(src, value), value,
                                   node, nested))
    return out


def compound_form(node):
    """The kind of multi-decision package `node` is, or None.  The list is
    chosen; `expr_nodes` below is the total that is not."""
    if isinstance(node, ast.BoolOp):
        return "or" if isinstance(node.op, ast.Or) else "and"
    if isinstance(node, ast.Compare):
        if len(node.ops) > 1:
            return "chained"
        if isinstance(node.ops[0], (ast.In, ast.NotIn)):
            return "membership"
        SEQ = (ast.List, ast.Tuple, ast.Set, ast.ListComp, ast.SetComp,
               ast.GeneratorExp, ast.DictComp, ast.Dict)
        if isinstance(node.left, SEQ) or isinstance(node.comparators[0], SEQ):
            return "sequence"
    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in ("any", "all")):
        return "quantifier"
    return None


def expr_nodes(src):
    """Every expression node inside every deciding condition -- the total that
    depends on no classification."""
    return sum(len(list(ast.walk(c))) for _f, _k, c in deciding_conditions(src))


def drop_operand(src, operand):
    """`src` with ONE operand of ONE boolean operator removed and everything
    else -- the rest of the operator, its condition, its statement -- kept."""
    kept = [v for k, v in enumerate(operand.parent.values)
            if k != operand.index]
    if len(kept) == 1:
        text = ast.get_source_segment(src, kept[0])
    else:
        text = (" %s " % operand.op).join(
            "(%s)" % ast.get_source_segment(src, v) for v in kept)
    return splice(src, operand.parent, text)


def splice(src, node, text):
    """`src` with the source segment of `node` replaced by `text`."""
    lines = src.splitlines(keepends=True)
    starts = [0]
    for line in lines:
        starts.append(starts[-1] + len(line))
    a = starts[node.lineno - 1] + node.col_offset
    b = starts[node.end_lineno - 1] + node.end_col_offset
    return src[:a] + text + src[b:]


# ------------------------------------------------- the unit a patch removes
def _stmt_types(tree):
    return collections.Counter(type(n).__name__ for n in ast.walk(tree)
                               if isinstance(n, ast.stmt))


def _all_exprs(tree):
    return collections.Counter(ast.dump(n) for n in ast.walk(tree)
                               if isinstance(n, ast.expr))


def _operand_dumps(tree):
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.BoolOp):
            out.extend(ast.dump(v) for v in n.values)
    return collections.Counter(out)


def unit_removed(before, after):
    """(returns, other statements, boolean operands, syntax nodes) removed.

    Computed by DIFFING TWO PARSES, so it is correct at whatever grain the patch
    operates at and cannot disagree with the patch.  Three decisions worth
    stating, because each is a place a count of this kind goes wrong:

      * statements are diffed BY TYPE.  A statement whose body changed is not a
        statement that was removed, and a `pass` put in where a statement was
        taken out must not cancel the removal.
      * an operand counts as removed only if NO expression anywhere in the
        patched tree has its shape.  Taking one operand out of a two-operand
        `or` leaves the other one standing as a bare condition: one operand
        removed, not two.
      * `nodes` is the net difference over every node of any kind.  It has no
        grain, so syntax that none of the three named units names is inside it.
    """
    tb, ta = ast.parse(before), ast.parse(after)
    gone = _stmt_types(tb) - _stmt_types(ta)
    rets = gone.get("Return", 0)
    others = sum(gone.values()) - rets
    ops = sum((_operand_dumps(tb) - _all_exprs(ta)).values())
    nodes = len(list(ast.walk(tb))) - len(list(ast.walk(ta)))
    return rets, others, ops, nodes


def direction(declared, measured):
    """Which way a declaration misses its patch.  UNDERSTATES makes the
    evidence look FINER than it is, which is the defect; OVERSTATES makes it
    look coarser, which is harmless.  A verdict column that cannot tell them
    apart cannot report either."""
    if measured == declared:
        return "AGREES"
    if all(m >= d for m, d in zip(measured, declared)):
        return "UNDERSTATES"
    if all(m <= d for m, d in zip(measured, declared)):
        return "OVERSTATES"
    return "MIXED"


# ------------------------------------------------------- the subject, as text
SHAPE_GUARD = ("    if len(shape_A) != len(shape_B) or any(\n"
               "            a != b for a, b in zip(shape_A, shape_B)):")
SHAPE_GUARD_ORDER_ONLY = "    if len(shape_A) != len(shape_B):"
SHAPE_GUARD_WIDTH_ONLY = ("    if any(\n"
                          "            a != b for a, b in zip(shape_A, "
                          "shape_B)):")

# The pair the subject NAMES as the one line that would cover the order half,
# written out as a row of `UNREACHED_GATE_PAIRS["shape"]`.  The subject asserts
# what adding it would do; e5 runs it.
SEPARATOR_ANCHOR = ('        ("the accepting side: identical 2x2 matrices, '
                    's = (+1,+1)", True,')
SEPARATOR_ROW = (
    '        ("SAME WIDTHS AT EVERY COMMON ROW, DIFFERENT ORDERS -- 2x2 '
    'against "\n'
    '         "a three-row B whose first two rows are 2 wide.  `zip` stops "\n'
    '         "at the shorter shape profile, so the WIDTH half of the "\n'
    '         "`shape` guard cannot see this pair and the ORDER half rejects "\n'
    '         "it unaided (mg-eaef)", False,\n'
    '         [[0, 1], [1, 0]],\n'
    '         [[0, 1], [1, 0], [0, 0]]),\n'
    + SEPARATOR_ANCHOR)


# ------------------------------------------- the subject's instrument, RUNNABLE
def instrument_copy(edits=()):
    """A runnable copy of `code/face_geometry_instr_5f9a`, with `edits` --
    (old, new) pairs -- applied to its `d2_deletion.py`.

    WHY A COPY.  The question "is the declaration DERIVED, or a written value
    that a restructuring quietly reverted to?" is answered by changing the patch
    and reading whether the declaration follows, with NO declaration touched.
    Doing that in the worktree would leave the subject modified while its answer
    was being read, which is the one state in which a green run proves nothing.

    The layout is preserved because `kern5f9a` computes the predicate directory
    and the repository root from `__file__`, and the worktree's `.git` pointer
    is carried across so the pinned commits still resolve.
    """
    tmp = tempfile.mkdtemp(prefix="mg-eaef-instr-")
    os.makedirs(os.path.join(tmp, "code"))
    dot = os.path.join(REPO, ".git")
    if os.path.isfile(dot):
        shutil.copy2(dot, os.path.join(tmp, ".git"))
    else:
        os.symlink(dot, os.path.join(tmp, ".git"))
    os.symlink(FG, os.path.join(tmp, "code", "face_geometry"))
    os.symlink(AUDIT_0B07, os.path.join(tmp, "code",
                                        "face_geometry_audit_0b07"))
    dst = os.path.join(tmp, "code", "face_geometry_instr_5f9a")
    shutil.copytree(INSTR, dst)
    path = os.path.join(dst, "d2_deletion.py")
    text = open(path).read()
    for old, new in edits:
        n = text.count(old)
        if n != 1:
            raise SystemExit("instrument anchor occurs %d times, expected 1:\n%r"
                             % (n, old[:200]))
        text = text.replace(old, new)
    open(path, "w").write(text)
    return dst


def run_instrument(dst, script="d2_deletion.py"):
    r = subprocess.run([sys.executable, script], cwd=dst, capture_output=True,
                       text=True)
    return r.stdout + r.stderr, r.returncode


def declared_row(text, tag):
    """The subject's own DERIVED DECLARATION for `tag`, taken out of its own
    stdout by the tag it prints rather than by line number.

    Returns (ret, stmt, cls, nodes, sentence) or None.
    """
    for line in text.split("\n"):
        parts = line.split()
        if len(parts) > 5 and parts[0] == tag and parts[1].isdigit():
            try:
                nums = tuple(int(p) for p in parts[1:5])
            except ValueError:
                return None
            return nums + (" ".join(parts[5:]),)
    return None
