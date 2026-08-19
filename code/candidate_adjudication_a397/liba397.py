#!/usr/bin/env python3
"""mg-a397 — the shared machinery for ADJUDICATING mg-9876's index.

WHAT THIS TICKET IS AND WHAT IT IS NOT.  mg-9876 produced an INDEX of candidates and said, in
its own module docstring, why it stopped there: "establishing that a particular one DOES
[match something printed unconditionally] requires running it two ways".  This directory does
the running.  Every verdict below is one of

    LAUNDERED                     — measured: the check is satisfied by the GOOD world, so it
                                    cannot report the thing it names having stopped happening.
    DISCRIMINATES                 — measured: the check answers differently on a known-good
                                    and a known-bad input.
    CANNOT-TELL-WITHOUT-RUNNING   — not measured.  A first-class outcome, never rounded to
                                    clean, and the count is reported beside the other two.
    CANNOT-LAUNDER-A-GREEN        — structural: the site's value never reaches a verdict, so
                                    no answer it gives can be read as coverage.

THE DETECTOR IS mg-9876's, IMPORTED, NOT REWRITTEN.  The ticket is explicit that a third
regex producing a fourth number would be the defect this line has been correcting.  `sites()`
below loads `a4_sweep.py` as a module and calls its own `SMELL_MEMBERSHIP` / `_FOR_BINDING` /
`dirs()` / `files()`.  §1 of a1 checks that what we loaded is byte-identical to what is
committed, so "we used c9876's detector" is a checked statement and not a promise.

WHAT WE ADD IS A READING OF THE SITE, NOT A NEW WAY TO FIND ONE.  `classify_site()` parses
the file and answers two questions the regex cannot: what the needle is (a typed literal, or
a value derived from an artifact) and where the membership answer GOES (a verdict, or a
print).  A membership test whose answer only ever reaches a print cannot launder a green,
because nothing reads it as coverage.  That is structural and needs no run — which is why it
is reported separately from the two MEASURED verdicts rather than folded in with them.
"""

import ast
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CODE = os.path.join(ROOT, "code")
C9876 = os.path.join(CODE, "control_audit_9876")

# The three headline figures mg-a397 was filed on.  They are the tree's answer on 2026-08-10
# at c9876's writing, NOT constants: a1 re-measures and prints the drift rather than
# asserting agreement, because the population is `every directory under code/` and this
# repository gains directories daily.  mg-724a already paid for this lesson on a live merge
# request — its gate observed 207 where its author's worktree observed 206, because the gate
# runs on the REBASED tree.
TICKET_FIGURES = {"membership_sites": 202, "membership_dirs": 66,
                  "tee_sites": 18, "tee_dirs": 4, "bare_dirs": 24}


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def rel(path):
    return os.path.relpath(path, ROOT)


def git(*args, cwd=ROOT):
    p = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


# ======================================================================================
# mg-9876's detector, loaded rather than reimplemented
# ======================================================================================

def load_c9876():
    """Import `a4_sweep.py` as a module.  It is a script, but it guards nothing at import
    time except `import lib9876`, so loading it is cheap and gives us its compiled patterns.
    """
    if C9876 not in sys.path:
        sys.path.insert(0, C9876)
    spec = importlib.util.spec_from_file_location("a4_sweep_a397",
                                                  os.path.join(C9876, "a4_sweep.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sites(a4=None):
    """Every membership candidate mg-9876's §1 counts, as records rather than printed lines."""
    a4 = a4 or load_c9876()
    out = []
    for name, path in a4.dirs():
        for f in a4.files(path, (".py",)):
            for i, line in enumerate(read(f).split("\n"), 1):
                s = line.strip()
                if s.startswith("#") or not a4.SMELL_MEMBERSHIP.search(s):
                    continue
                if a4._FOR_BINDING.search(s):
                    continue
                out.append({"dir": name, "file": rel(f), "line": i, "src": line.rstrip()})
    return out


def tee_sites(a4=None):
    a4 = a4 or load_c9876()
    out = []
    for name, path in a4.dirs():
        for f in a4.files(path, (".sh",)):
            for i, line in enumerate(read(f).split("\n"), 1):
                s = line.strip()
                if s.startswith("#") or not a4.SMELL_TEE.search(s):
                    continue
                out.append({"dir": name, "file": rel(f), "line": i, "src": s})
    return out


def bare_dirs(a4=None):
    """mg-9876 §3's third bucket: ships code, no file named for a control, no transcript
    carrying a red token.  Recomputed here with c9876's own two regexes."""
    a4 = a4 or load_c9876()
    out = []
    for name, path in a4.dirs():
        srcs = list(a4.files(path, (".py", ".sh")))
        txts = list(a4.files(path, (".txt", ".md")))
        neg = any(a4.NEGATIVE_NAMES.search(os.path.basename(f)) for f in srcs)
        red = any(a4.RED_TOKENS.search(read(f)) for f in txts)
        if srcs and not neg and not red:
            out.append(name)
    return out


# ======================================================================================
# the reading a regex cannot do: where does the membership answer GO?
# ======================================================================================

HAYSTACKS = {"out", "output", "stdout", "text", "txt", "report", "blob", "body",
             "content", "contents", "combined"}

# Roles that reach a verdict.  A membership answer inside an `assert`, an `if` that guards a
# failure path, a `return`, a lambda handed to a harness, or a value later compared or
# accumulated, is read as coverage by somebody.  PRINT is the one role that is not: a
# diagnostic line nobody branches on cannot certify anything.
VERDICT_ROLES = {"assert", "branch", "return", "lambda", "collected", "assigned-used",
                 "call-arg", "boolop-verdict"}
PRINT_ROLES = {"print", "assigned-unused"}


class _Sitefinder(ast.NodeVisitor):
    """Find the In/NotIn compares that mg-9876's regex is pointing at, and record the parent
    chain so the role can be read off it."""

    def __init__(self):
        self.found = []          # (lineno, node, parents)
        self._stack = []

    def generic_visit(self, node):
        self._stack.append(node)
        super().generic_visit(node)
        self._stack.pop()

    def visit_Compare(self, node):
        for op, right in zip(node.ops, node.comparators):
            if not isinstance(op, (ast.In, ast.NotIn)):
                continue
            nm = _basename(right)
            if nm in HAYSTACKS:
                self.found.append((node.lineno, node, list(self._stack)))
        self.generic_visit(node)


def _basename(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None


def _needle_kind(node):
    """LITERAL: a string typed by the author, which is the shape both known instances had
    (`"8 9"`, `4fcb`).  DERIVED: a value that came from somewhere — a pin, a captured
    artifact, a loop variable.  mg-724a's rule is that a mutation must be derived rather than
    typed; the same asymmetry applies to an expectation."""
    left = node.left
    if isinstance(left, ast.Constant) and isinstance(left.value, str):
        return "literal", left.value
    if isinstance(left, ast.JoinedStr):
        return "derived", None
    if isinstance(left, (ast.Name, ast.Attribute, ast.Subscript, ast.Call, ast.BinOp)):
        return "derived", None
    return "other", None


def _role(node, parents, tree):
    """Read the role off the parent chain, outermost decision wins."""
    p = list(reversed(parents))
    for anc in p:
        if isinstance(anc, ast.Assert):
            return "assert"
        if isinstance(anc, ast.Lambda):
            return "lambda"
        if isinstance(anc, ast.Return):
            return "return"
        if isinstance(anc, (ast.If, ast.While, ast.IfExp)):
            # only a role if we are inside the TEST, not the body
            if _contains(anc.test, node):
                return "branch"
        if isinstance(anc, ast.Call):
            fn = _basename(anc.func)
            if fn in ("print", "emit", "say", "write"):
                return "print"
            return "call-arg"
        if isinstance(anc, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            targets = getattr(anc, "targets", None) or [getattr(anc, "target", None)]
            names = [t.id for t in targets if isinstance(t, ast.Name)]
            if isinstance(anc, ast.AugAssign):
                return "collected"
            if not names:
                return "collected"
            if _name_used_in_verdict(tree, names[0], anc.lineno):
                return "assigned-used"
            return "assigned-unused"
        if isinstance(anc, ast.Expr):
            return "expr-discarded"
    return "unknown"


def _contains(root, node):
    for n in ast.walk(root):
        if n is node:
            return True
    return False


_VERDICT_NAMES = re.compile(r"(fail|bad|red|miss|hole|caught|refus|error|wrong|ok|pass|"
                            r"clean|good|drift|verdict|status|rc|problem|finding)", re.I)


def _name_used_in_verdict(tree, name, after_line):
    """A conservative reaching check: is the assigned name later read inside an assert, an if
    test, a return, a comparison, or an append?  Conservative in the direction that matters —
    when in doubt we call it verdict-bearing, because the cheap error here is to excuse a
    check that somebody does read."""
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id == name and isinstance(n.ctx, ast.Load) \
                and getattr(n, "lineno", 0) >= after_line:
            return True
    return bool(_VERDICT_NAMES.search(name))


def classify_file(path):
    """-> {lineno: [record, ...]}"""
    try:
        tree = ast.parse(read(path))
    except SyntaxError:
        return {}
    f = _Sitefinder()
    f.visit(tree)
    out = {}
    for lineno, node, parents in f.found:
        kind, needle = _needle_kind(node)
        role = _role(node, parents, tree)
        out.setdefault(lineno, []).append(
            {"needle_kind": kind, "needle": needle, "role": role,
             "negated": any(isinstance(o, ast.NotIn) for o in node.ops)})
    return out


def classify_site(site, cache):
    """Attach the AST reading to one of mg-9876's sites.  A site the parser cannot place is
    reported UNPLACED rather than guessed at — the regex and the parser disagreeing is a fact
    about this instrument and is printed as one."""
    path = os.path.join(ROOT, site["file"])
    if path not in cache:
        cache[path] = classify_file(path)
    recs = cache[path].get(site["line"], [])
    if not recs:
        return {"needle_kind": "unplaced", "needle": None, "role": "unplaced",
                "negated": None}
    # a line can hold two compares; prefer the literal-needle one, which is the shape both
    # known instances had.
    for r in recs:
        if r["needle_kind"] == "literal":
            return r
    return recs[0]


# ======================================================================================
# the healthy record: what did this instrument actually print when nothing was wrong?
# ======================================================================================

def transcripts(dirname):
    d = os.path.join(CODE, dirname)
    out = []
    for root, _dn, fns in os.walk(d):
        for fn in sorted(fns):
            if fn.endswith(".txt"):
                out.append(os.path.join(root, fn))
    return out


def anchoredness(needle, dirname):
    """mg-724a's rule, applied to a candidate instead of to a gate field: `0 means the suite
    never reached its decision and 2 means the pattern no longer names one fact`.  Counted
    over the directory's own committed transcripts — its record of what it printed on a
    healthy run.

    THIS IS A STRATUM, NOT A VERDICT.  A needle occurring twice in the healthy record is
    instance 3's exact shape (`"8 9"` matched section 1's row-set listing as well as section
    2's worklist) but it is not proof: the two occurrences could both be inside the thing
    being checked.  It is used here to CHOOSE what to run two ways, which is the only thing
    a stratum is good for.
    """
    if not needle:
        return None
    n = 0
    for t in transcripts(dirname):
        n += read(t).count(needle)
    return n
