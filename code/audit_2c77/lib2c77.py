"""lib2c77.py -- the apparatus for the mg-2c77 audit of the mg-69d1 repair.

THIS IS AN INDEPENDENT INSTRUMENT.  It does not import `lib69d1`, and its AST
walkers, its `run_c1`, its bends and its report class are written here rather
than borrowed, because an audit that runs the repair's own helpers can only
find defects those helpers do not have.

Where it DOES import the subject -- `kern5f9a.deciding_clauses` and
`kern5f9a.operand_columns` in `q2` and `q3` -- that is deliberate and is the
point of those probes: the shipped classifier is fed inputs from OUTSIDE the
tree it was written against, and what it does with them is the measurement.
Every such import is named at its call site.

WHAT THIS AUDIT WILL NOT DO

  * It will not compare the bound's sentence with the sweep's source and call
    the agreement a check.  `q2` perturbs the tree on each side of the boundary
    the bound draws and watches the sweep's own enumerated population.
  * It will not read the repair's counts back out of the repair's transcript.
    `q3` walks `face_complex.py` and `posets.py` with a walker written here.

NOTHING HERE WRITES ANYWHERE IN THE REPOSITORY.  Every mutation is made in a
temporary directory that is removed on the way out; every subject script is run
as a subprocess with its stdout captured, never redirected over a committed
transcript.  No `| tee` anywhere (mg-c2b3, mg-f922): `run_all.sh` redirects and
re-reads `$?`.
"""

import ast
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

FG_DIR = "code/face_geometry"
INSTR_DIR = "code/face_geometry_instr_5f9a"
S58DA_DIR = "code/branching_audit_58da"
A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
E34A_DIR = "code/branching_audit_e34a"
R69D1_DIR = "code/repair_69d1"
R76CC_DIR = "code/branching_repair_76cc"

FACE_REL = FG_DIR + "/face_complex.py"
POSETS_REL = FG_DIR + "/posets.py"
D2_REL = INSTR_DIR + "/d2_deletion.py"
KERN5F9A_REL = INSTR_DIR + "/kern5f9a.py"
LIB58DA_REL = S58DA_DIR + "/lib58da.py"
C1_REL = A218_DIR + "/c1_branching.py"
KERN_REL = A218_DIR + "/kern_a218.py"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

# c1's output splits here: before it is what c1 COMPUTES, after it is what it
# COMPARES.  The same marker g1 uses, and it is a fact about c1's output rather
# than a choice this audit is entitled to make differently.
C1_SPLIT = "(iii) EVERY CELL, AGAINST"


# ---------------------------------------------------------------------------
# git, files, hashing
# ---------------------------------------------------------------------------

def git(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def git_show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def head_rev():
    return git("rev-parse", "HEAD").strip()


def read_worktree(rel):
    with open(os.path.join(REPO, rel)) as fh:
        return fh.read()


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_literal(src, name):
    """A module-level assignment's value, out of the SOURCE and not by import.

    Importing runs the module.  REV_A218 and SWEEP_FILES are both read this
    way so that this file does not become one more opinion about either.
    """
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)


REV_A218 = read_literal(read_worktree(LIB58DA_REL), "REV_A218")
SWEEP_FILES = tuple(read_literal(read_worktree(D2_REL), "SWEEP_FILES"))


# ---------------------------------------------------------------------------
# THE OPERAND WALKERS.  Written here, from the spec, not imported.
# ---------------------------------------------------------------------------

def pos(node):
    """The one key this audit compares operands by.

    Not the source text: `a == b` occurs more than once in `face_complex.py`
    and a text key would silently merge two operands into one.  Not the
    (function, kind, text) triple the repair's own comparison uses either --
    that triple is undefined for an operand outside every deciding condition,
    which is precisely the population `q3` is about.  A span cannot collide.
    """
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def deciding_conditions_mine(src):
    """[(function name, kind, condition node)] -- MY reading of the rule.

    The rule, as `kern5f9a` states it: 'decides a return' is either the test of
    an `if` whose body returns, or the value of a `return` itself.  Implemented
    here from that sentence.  `selftest_2c77` runs this against the shipped
    `deciding_conditions` on both census files and requires the two to agree
    span for span -- so if my reading is wrong, the self-test says so before
    any finding rests on it.
    """
    tree = ast.parse(src)
    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner[sub] = node.name
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        name = ("%s.%s" % (owner[fn], fn.name)) if fn in owner else fn.name
        for node in ast.walk(fn):
            if isinstance(node, ast.If):
                if any(isinstance(s, ast.Return) for s in ast.walk(node)):
                    out.append((name, "guard", node.test))
            elif isinstance(node, ast.Return) and node.value is not None:
                out.append((name, "value", node.value))
    return out


def _enclosing_function(tree):
    """{node: function name} for every node under every function def."""
    owner = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    owner[sub] = node.name
    where = {}
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        name = ("%s.%s" % (owner[fn], fn.name)) if fn in owner else fn.name
        for node in ast.walk(fn):
            # innermost wins: the walk visits outer functions first, so only
            # overwrite when the current owner is an ancestor of this one.
            where.setdefault(node, name)
            if fn is not node:
                where[node] = where.get(node, name)
    return where


def all_boolean_operands(src, fname):
    """EVERY operand of EVERY `and`/`or` ANYWHERE IN THE MODULE.

    No filter of any kind: not by statement form, not by whether the condition
    decides a return, not by nesting.  This is the population the phrase
    `every explicit boolean operand` denotes when it is written without a
    qualifier, and it exists here so that the phrase can be scored rather than
    granted.
    """
    tree = ast.parse(src)
    where = _enclosing_function(tree)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.BoolOp):
            continue
        for k, value in enumerate(node.values):
            out.append({
                "file": fname,
                "func": where.get(node, "<module>"),
                "op": "or" if isinstance(node.op, ast.Or) else "and",
                "text": ast.get_source_segment(src, value),
                "pos": pos(value),
                "line": value.lineno,
            })
    return out


def deciding_boolean_operands(src, fname):
    """The same walk, restricted to what is INSIDE a deciding condition.

    This is what `kern5f9a.boolean_operands` computes.  Recomputed here so that
    the difference between the two populations is a subtraction this audit
    performed rather than a difference it was told about.
    """
    out = []
    for func, kind, cond in deciding_conditions_mine(src):
        for node in ast.walk(cond):
            if not isinstance(node, ast.BoolOp):
                continue
            for k, value in enumerate(node.values):
                out.append({
                    "file": fname,
                    "func": func,
                    "kind": kind,
                    "top": node is cond,
                    "op": "or" if isinstance(node.op, ast.Or) else "and",
                    "text": ast.get_source_segment(src, value),
                    "pos": pos(value),
                    "line": value.lineno,
                })
    return out


# ---------------------------------------------------------------------------
# running c1 with the script and the kernel as SEPARATE sources
# ---------------------------------------------------------------------------

def run_c1(target_text, c1_src, kern_src):
    """c1_branching.py with a chosen kernel, against a chosen target.

    Two sources, never one revision.  The signature is forced: mg-957f's F-1
    was a signature that could not say 'this script with that kernel', and an
    instrument that inherits that defect cannot measure the repair of it.
    """
    tmp = tempfile.mkdtemp(prefix="mg2c77-c1-")
    try:
        a = os.path.join(tmp, A218_DIR.split("/")[-1])
        d = os.path.join(tmp, DB09_DIR.split("/")[-1])
        os.makedirs(a)
        os.makedirs(d)
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(c1_src)
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(kern_src)
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run([sys.executable, "c1_branching.py"], cwd=a,
                           capture_output=True, text=True, timeout=1800)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def measuring_half(out):
    return out.split(C1_SPLIT)[0]


def vertex_lines(out):
    """c1's own printed vertex sets, as raw lines, out of the measuring half.

    Returned as a LIST and never as a count alone.  A run that produced none is
    an empty list, and every caller treats empty as a SELF-ERROR rather than as
    an empty agreement -- two runs that both failed to print the form would
    otherwise compare equal, which is the one reading a comparison must never
    make.
    """
    got = []
    for raw in measuring_half(out).splitlines():
        line = raw.strip()
        if line.startswith("n=") and "set {" in line:
            got.append(line)
    return got


def g1_verdict(target, c1_src, kern_src, ref):
    """g1's own IDENTICAL / MOVED test for one (script, kernel) row.

    g1 asks: the measuring half byte for byte, AND c1's own 24 vertex sets,
    AND that there are 24 of them.  The vertex sets are printed inside the
    measuring half, so the byte comparison already covers them; the count is
    kept as the empty-baseline guard it is there to be.
    """
    out, _rc = run_c1(target, c1_src, kern_src)
    lines = vertex_lines(out)
    digest = sha(measuring_half(out))[:16]
    same = (digest == ref[0] and lines == ref[1] and len(lines) == 24)
    return {"sha": digest, "cells": len(lines), "same": same}


# ---------------------------------------------------------------------------
# THE BENDS.  Every one refuses on zero occurrences and on many.
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old[:60], n))
    return text.replace(old, new, 1)


KERN_V = ("        return [(p, self.dim_L(p)) for p in self.parts "
          "if self.dim_L(p) > 0]")
C1_V = "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()"


def bend_kern_up(src):
    """kern_a218.py: every simple's dimension one too BIG."""
    return replace_once(src, KERN_V,
                        "        return [(p, self.dim_L(p) + 1) for p in "
                        "self.parts if self.dim_L(p) > 0]")


def bend_c1_down(src):
    """c1_branching.py: every dimension one too SMALL -- the cancelling half."""
    return replace_once(src, C1_V,
                        "        mine_vertices[(beta, n)] = [(p, d - 1) for "
                        "p, d in algebras[(n, beta)].vertices()]")


# CONSPIRING PAIR A -- the one mg-69d1 built, rebuilt here from its description
# rather than imported, so that "mg-69d1's measurement reproduces" is a second
# measurement and not the same one read twice.
def conspire_a_kern(src):
    if "DIM_SHIFT_69D1" in src:
        raise ValueError("kern already carries DIM_SHIFT_69D1")
    return src + "\n\nDIM_SHIFT_69D1 = 1\n"


def conspire_a_c1(src):
    return replace_once(
        src, C1_V,
        "        import kern_a218 as _k2c77\n"
        "        mine_vertices[(beta, n)] = [\n"
        "            (p, d + getattr(_k2c77, \"DIM_SHIFT_69D1\", 0))\n"
        "            for p, d in algebras[(n, beta)].vertices()]")


# CONSPIRING PAIR B -- A DIFFERENT SHAPE, AND IT IS NEW HERE.  Pair A conspires
# by SHIFTING a printed value through an integer default of 0.  Pair B conspires
# by ADDING a vertex that is not there, through a BOOLEAN default of False.  A
# demonstration built once with one mechanism is a demonstration of that
# mechanism; the row's claim is about conspiracy, not about integer defaults.
def conspire_b_kern(src):
    if "EXTRA_VERTEX_2C77" in src:
        raise ValueError("kern already carries EXTRA_VERTEX_2C77")
    return src + "\n\nEXTRA_VERTEX_2C77 = True\n"


def conspire_b_c1(src):
    return replace_once(
        src, C1_V,
        "        import kern_a218 as _k2c77\n"
        "        mine_vertices[(beta, n)] = (\n"
        "            algebras[(n, beta)].vertices()\n"
        "            + ([(0, 99)] if getattr(_k2c77, \"EXTRA_VERTEX_2C77\","
        " False)\n"
        "               else []))")


# A THIRD INPUT, AND IT IS NEITHER.  The corrected reason is stated as a pair of
# cases; a reader takes a pair of named cases for a partition unless something
# says otherwise.  A one-sided defect is neither cancelling nor conspiring and
# is what the two HALF rows are for.  Built so the reason's two rows can be read
# against a row that belongs to neither of them.
def lone_kern(src):
    """kern alone: dimensions one too big, with c1 left as it stands."""
    return bend_kern_up(src)


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

BAR = "=" * 74


def banner(tag, title):
    print(BAR)
    print("%s -- %s" % (tag, title))
    print(BAR)


def rule(title):
    print("-" * 74)
    print(title)
    print("-" * 74)


class Report(object):
    """SELF-ERRORS and FINDINGS, kept apart, each carrying its POPULATION.

    A non-zero exit means THIS SCRIPT HAS SOMETHING TO REPORT.  It never means
    the script is broken -- that is what SELF-ERRORS are for, and they are
    counted and named separately so the two cannot be read as one number.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop, self.findpop = selfpop, findpop
        self.self_errors, self.findings = [], []

    def selferr(self, msg):
        self.self_errors.append(msg)
        return False

    def finding(self, msg):
        self.findings.append(msg)
        return False

    def gate(self, ok, msg):
        if not ok:
            self.finding(msg)
        return ok

    def check(self, ok, msg):
        if not ok:
            self.selferr(msg)
        return ok

    def emit(self):
        print("-" * 74)
        print("SELF-ERRORS: %d, population: %s"
              % (len(self.self_errors), self.selfpop))
        for x in self.self_errors:
            print("   SELF-ERROR: " + x)
        print("FINDINGS: %d, population: %s"
              % (len(self.findings), self.findpop))
        for x in self.findings:
            print("   FINDING: " + x)
        print("TOTAL BAD: %d" % (len(self.self_errors) + len(self.findings)))
        return 1 if (self.self_errors or self.findings) else 0


def finish(report):
    sys.exit(report.emit())
