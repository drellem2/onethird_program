"""lib330a.py -- the apparatus for the INDEPENDENT AUDIT of mg-8d5e (dfa263c).

mg-8d5e repaired two sites mg-2c77 left open on the mg-69d1 repair:

  A-1  a DERIVED revision anchor re-pointed when an unrelated SENTENCE was
       edited in the file it derives from, AND THE PRINTED NUMBER DID NOT
       CHANGE.
  A-2  a census term denoted more than the count covered -- 39 operands under
       a phrase whose table classifies 17.

This audit does not check the repair's logic.  It RESOLVES every derived
anchor and looks, it CONSTRUCTS the failure rather than recalling it, and it
re-derives both columns of the kernel-half confirmation from scratch.

WHAT IS WRITTEN FRESH HERE, AND WHY

  * THE ANCHOR TAXONOMY.  mg-8d5e's own r4 enumerates 11 anchors and scopes
    that enumeration to `code/repair_8d5e/`.  The brief for this audit says
    the population of history-derived anchors has never been enumerated, so
    the sweep here is REPO-WIDE and it classifies by HOW the revision is
    obtained rather than by which directory it lives in:

        NEWEST      `git log -1 --format=%H -- <path>`      re-points on ANY
                    edit to <path>.  THIS IS A-1's DEFECT.
        INDEXED     `git log --format=%H -- <path>` then [n]  every index
                    shifts by one on ANY edit.  THIS IS A-1's SECOND HALF.
        OLDEST      `git log --reverse --format=%H -- <path>` then [0]
                    STABLE against later edits: the file's creation does not
                    move when the file is edited.  Named separately because
                    lumping it with NEWEST would count a safe construct as
                    the defect and inflate the population.
        PICKAXE     `git log -S <marker> -- <path>`         derived from a
                    PROPERTY.  A prose edit does not move it.
        TWO-SIDED   `first_introducing(path, marker)`       derived from a
                    property, with the `and not at the first parent` half.
        RANGE       `git log <a>..<b> -- <path>`            a set, not an
                    anchor; it has no single revision to re-point.
        HEAD        an anchor on HEAD.  Re-points on EVERY commit to the
                    repo, not merely to one file -- the loudest version of
                    the same shape, and the one mg-8d5e's own commit message
                    points at in p3_reason.py without repairing.

    The taxonomy is applied to CALL SITES found by parsing each file with
    `ast`, not by grepping lines: a grep for `--format=%H` finds the string
    and cannot tell which flags travel with it in the same call, and the
    whole distinction above is about which flags travel together.

  * EVERY NUMBER NAMES ITS POPULATION.  No bare totals.  Where a number is
    READ out of somebody's transcript rather than counted here, it says so.

  * THE CONTROL IS A COMMIT WHERE THE DEFECT IS STILL PRESENT.  Every new
    detector in this instrument is run at `e2577e5` -- mg-8d5e's own
    predictions commit, the last commit before `dfa263c` -- as well as at
    HEAD.  A detector that has never been seen to go red is a detector whose
    red is unmeasured.

  * MUTATION IS A COMMIT IN A CLONE.  g1 reads c1 and the kernel with
    `git show`; a working-tree edit reaches nothing and comes back silent for
    a reason that has nothing to do with the predicate.

NOTHING HERE WRITES INTO code/branching_audit_e34a/, code/repair_8d5e/,
code/repair_69d1/, code/audit_2c77/, code/face_geometry_instr_5f9a/ or
code/face_geometry/.  Foreign scripts are RUN with their stdout captured;
none of the ones run here writes a file into its own directory.  Every
mutation happens in a clone under the system temp directory.

Pure Python 3, no dependencies, NO NETWORK.
"""

import ast
import hashlib
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# ---------------------------------------------------------------------------
# the revisions this audit is ABOUT.  Pinned, with the reason beside each --
# deriving them as "the newest repair commit" would be A-1, in an audit of
# A-1.
# ---------------------------------------------------------------------------

# The repair under audit.  Pinned: it is the commit whose content is the
# subject, so re-deriving it would make the subject move when anybody commits.
REPAIR_8D5E = "dfa263cce851c847abc35cda1b718d918823e860"

# The commit BEFORE it -- mg-8d5e's own predictions commit.  Pinned as
# REPAIR_8D5E^ in the selftest rather than written twice.
PRE_8D5E = "e2577e5"

# The repair mg-2c77 audited, and the revision its census transcript is about.
D01FF32 = "d01ff32dd4dce31b98cb8aca9f4ae6e3a8aaebc3"

E34A_DIR = "code/branching_audit_e34a"
G1_REL = "code/branching_audit_58da/g1_provenance.py"
LIB58DA_REL = "code/branching_audit_58da/lib58da.py"
KERN_REL = "code/branching_audit_a218/kern_a218.py"
C1_REL = "code/branching_audit_a218/c1_branching.py"

# mg-76cc's property marker and its pin, RE-DERIVED here rather than imported
# from libe34a: importing the subject's own constant to check the subject is
# a comparison of a value with itself, which is the vacuity this arc is about.
MARK_76CC = "kernel_source="
MARK_7E58 = "def measurement("

# The census's two files and the term under test.  The phrase and the
# qualifier are copied from mg-2c77's q3_operands.py, character for
# character, so this audit cannot close a finding by moving the ruler.
CENSUS_FILES = ("code/face_geometry/face_complex.py",
                "code/face_geometry/posets.py")
TERM = "explicit boolean operand"
QUALIFIER = "deciding condition"


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args), check=True,
                          capture_output=True, text=True).stdout


def git_quiet(*args, **kw):
    repo = kw.pop("repo", REPO)
    p = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else ""


def show_or_empty(rev, path, repo=REPO):
    return git_quiet("show", "%s:%s" % (rev, path), repo=repo)


def resolve(rev, repo=REPO):
    return git("rev-parse", rev, repo=repo).strip()


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def head_rev(repo=REPO):
    return resolve("HEAD", repo=repo)


def distance(a, b, repo=REPO):
    return len([h for h in git("rev-list", "%s..%s" % (a, b),
                               repo=repo).split() if h])


def is_ancestor(a, b, repo=REPO):
    p = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor",
                        a, b], capture_output=True, text=True)
    return p.returncode == 0


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# the two derivations, written FRESH.  Not imported from libe34a: an audit
# that checks a derivation by calling it has checked nothing.
# ---------------------------------------------------------------------------

def my_last_touching(path, rev="HEAD", repo=REPO):
    """The newest commit at or before `rev` touching `path`.  A-1's defect."""
    out = git("log", "-1", "--format=%H", rev, "--", path, repo=repo).strip()
    return out or None


def my_nth_touching(path, n, rev="HEAD", repo=REPO):
    """The n-th newest commit touching `path` (0 = newest).  A-1's other
    half: every index shifts by one when the file is touched for any reason.
    """
    out = git("log", "--format=%H", rev, "--", path, repo=repo).split()
    return out[n] if n < len(out) else None


def my_first_introducing(path, marker, rev="HEAD", repo=REPO):
    """The OLDEST commit at or before `rev` where `marker` ENTERS `path`.

    Written from the sentence in libe34a's docstring -- "the marker is in
    `path` at the commit AND not in `path` at its first parent" -- and NOT by
    calling libe34a.  The two implementations are compared in the selftest;
    two readers that share an implementation share a blind spot.
    """
    hist = [h for h in git("log", "--format=%H", "--reverse", rev, "--", path,
                           repo=repo).split() if h]
    for h in hist:
        if marker not in show_or_empty(h, path, repo=repo):
            continue
        ps = [x for x in git("rev-parse", h + "^@", repo=repo).split() if x]
        if not ps or marker not in show_or_empty(ps[0], path, repo=repo):
            return h
    return None


# ---------------------------------------------------------------------------
# THE ANCHOR SWEEP.  By `ast`, over the repo's own .py files.
# ---------------------------------------------------------------------------

# A call is a revision-producing git log iff its string arguments contain a
# "log" and a format that yields a full hash.  Both must be in the SAME call,
# which is why this is done over the parsed call node and not over lines.
_HASH_FORMATS = ("--format=%H", "--pretty=%H", "--format=format:%H")


def _strings_of(call):
    """Every string constant that is a direct argument of `call`.

    Direct arguments only.  A string buried inside a nested call belongs to
    that call, and attributing it here would let one call's `--reverse` be
    read as another's.
    """
    out = []
    for a in list(call.args) + [k.value for k in call.keywords]:
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            out.append(a.value)
        elif isinstance(a, ast.List):
            for e in a.elts:
                if isinstance(e, ast.Constant) and isinstance(e.value, str):
                    out.append(e.value)
        elif isinstance(a, ast.BinOp):
            # "%s..%s" % (since, until) -- keep the template, it is what
            # carries the `..` that makes this a RANGE
            for sub in ast.walk(a):
                if isinstance(sub, ast.Constant) and isinstance(sub.value,
                                                                str):
                    out.append(sub.value)
    return out


def classify_call(strs):
    """The taxonomy, applied to one call's own string arguments.

    Returns a kind from the module docstring, or None if this call does not
    produce a revision at all.
    """
    if not any(s == "log" or s.endswith("log") for s in strs):
        return None
    if not any(f in strs for f in _HASH_FORMATS):
        return None
    has_path = "--" in strs
    if any(".." in s for s in strs if "%" not in s or ".." in s):
        if any(".." in s for s in strs):
            return "RANGE"
    # DEFECT #2 OF THIS INSTRUMENT, KEPT.  This test was first written for
    # `-S` alone, and s1's first run classified
    # code/hodge_leverage_repair_8eca/repair_8aae.py:499 -- a `git log -G` --
    # as INDEXED, i.e. as the defect class.  `-G` is the regex pickaxe: it
    # selects commits by a property of the CONTENT exactly as `-S` does, and
    # calling it history-derived would have inflated the defect population by
    # one.  Which is A-2's mistake -- a term denoting more than it covers --
    # committed inside an audit of A-2.  Found by reading the sweep's own
    # named rows, which is why the rows are named.
    if any(s in ("-S", "-G") or s.startswith("-S") or s.startswith("-G")
           for s in strs):
        return "PICKAXE"
    if "--reverse" in strs:
        return "OLDEST"
    if "-1" in strs:
        return "NEWEST" if has_path else "NEWEST-norestrict"
    if has_path:
        return "INDEXED"
    return "UNRESTRICTED"


def sweep_anchor_calls(repo=REPO, subdir="code"):
    """[{file, line, kind, strs, src}] for every revision-producing git log
    call in the repo's own Python.

    The population is stated where it is used: every `.py` file under
    `<repo>/code`, walked, parsed and searched.  Files that do not parse are
    reported, never skipped silently.
    """
    rows, unparsed = [], []
    root = os.path.join(repo, subdir)
    for dirpath, _dirs, files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, repo)
            try:
                with open(full) as fh:
                    src = fh.read()
                tree = ast.parse(src)
            except (SyntaxError, UnicodeDecodeError) as exc:
                unparsed.append((rel, str(exc)))
                continue
            lines = src.splitlines()
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                strs = _strings_of(node)
                kind = classify_call(strs)
                if kind is None:
                    continue
                rows.append({"file": rel, "line": node.lineno, "kind": kind,
                             "strs": strs,
                             "src": lines[node.lineno - 1].strip()
                                    if node.lineno <= len(lines) else ""})
    return rows, unparsed


def sweep_helper_uses(repo=REPO, subdir="code"):
    """Call sites of the two NAMED history derivations, `last_touching` and
    `nth_touching`, wherever they are defined or used.

    Separate from `sweep_anchor_calls` because a helper hides its flags: a
    call to `last_touching(p)` contains no `--format=%H` at all, and a sweep
    that only looks for the flags would miss exactly the construct mg-8d5e's
    own repair is about.
    """
    out = []
    root = os.path.join(repo, subdir)
    for dirpath, _dirs, files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".py"):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, repo)
            try:
                with open(full) as fh:
                    src = fh.read()
                tree = ast.parse(src)
            except (SyntaxError, UnicodeDecodeError):
                continue
            lines = src.splitlines()
            for node in ast.walk(tree):
                name = None
                if isinstance(node, ast.Call):
                    f = node.func
                    if isinstance(f, ast.Name):
                        name = f.id
                    elif isinstance(f, ast.Attribute):
                        name = f.attr
                elif isinstance(node, (ast.FunctionDef,)):
                    name = node.name
                if name in ("last_touching", "nth_touching"):
                    kind = ("DEF" if isinstance(node, ast.FunctionDef)
                            else "CALL")
                    out.append({"file": rel, "line": node.lineno,
                                "name": name, "what": kind,
                                "src": lines[node.lineno - 1].strip()
                                       if node.lineno <= len(lines) else ""})
    return out


# ---------------------------------------------------------------------------
# clones
# ---------------------------------------------------------------------------

def clone_at(rev, into=None):
    """A clone of this repo checked out at `rev`, in a temp directory.

    A CLONE and not a worktree: the probes commit, and a worktree commit
    would land in the real repository's object store and be visible from it.
    """
    d = into or tempfile.mkdtemp(prefix="mg330a-")
    tree = os.path.join(d, "tree")
    subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "checkout", "--quiet", rev],
                   check=True, capture_output=True, text=True)
    return tree


def commit_in(tree, rel, new_text, message):
    """Write `new_text` to `rel` in `tree` and COMMIT it.  Returns the sha."""
    p = os.path.join(tree, rel)
    with open(p, "w") as fh:
        fh.write(new_text)
    subprocess.run(["git", "-C", tree, "add", rel], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "-c", "user.name=mg-330a",
                    "-c", "user.email=mg-330a@local", "commit", "--quiet",
                    "-m", message], check=True, capture_output=True,
                   text=True)
    return subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"],
                          check=True, capture_output=True,
                          text=True).stdout.strip()


def rm_tree(tree):
    shutil.rmtree(os.path.dirname(tree), ignore_errors=True)


def run_py(script, cwd, extra_env=None, timeout=1800):
    """(exit, stdout+stderr) for `python3 -u script` run in `cwd`."""
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["python3", "-u", script], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def run_py_src(src, cwd, name, timeout=1800):
    """Write `src` as `name` inside `cwd` and run it there.

    Used to import a CLONE's own module rather than this tree's: the code
    under test must be the code at the revision named, and importing the
    module from here would make every probe agree with this HEAD by
    construction.  The file is removed afterwards; `cwd` is always a clone
    under the system temp directory, never a directory of this repository.
    """
    p = os.path.join(cwd, name)
    with open(p, "w") as fh:
        fh.write(src)
    try:
        return run_py(name, cwd, timeout=timeout)
    finally:
        try:
            os.unlink(p)
        except OSError:
            pass


# ---------------------------------------------------------------------------
# the operand walks, written FRESH from kern5f9a's own sentence
# ---------------------------------------------------------------------------

def _owner_map(tree):
    where = {}
    cls = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    cls[sub] = node.name
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            name = ("%s.%s" % (cls[fn], fn.name)) if fn in cls else fn.name
            for node in ast.walk(fn):
                where.setdefault(node, name)
    return where


def _span(node):
    """The source span.  Not the text: `a == b` occurs more than once in
    face_complex.py and a text key merges two operands into one."""
    return (node.lineno, node.col_offset, node.end_lineno, node.end_col_offset)


def all_operands(src, fname):
    """EVERY operand of EVERY `and`/`or` ANYWHERE in the module.

    No filter of any kind.  This is what `explicit boolean operand` denotes
    when it is written without its qualifier -- i.e. NOT restricted to the
    operands inside a deciding condition, which is the narrower population
    the census's four columns classify.
    """
    tree = ast.parse(src)
    where = _owner_map(tree)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.BoolOp):
            for v in node.values:
                out.append({"file": fname, "func": where.get(node, "<module>"),
                            "op": "or" if isinstance(node.op, ast.Or)
                                  else "and",
                            "text": ast.get_source_segment(src, v),
                            "span": _span(v)})
    return out


def deciding_conditions(src):
    """[(function, kind, node)] -- `decides a return` written from kern5f9a's
    own sentence: the test of an `if` whose body returns, or the value of a
    `return`.
    """
    tree = ast.parse(src)
    cls = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for sub in node.body:
                if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    cls[sub] = node.name
    out = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        name = ("%s.%s" % (cls[fn], fn.name)) if fn in cls else fn.name
        for node in ast.walk(fn):
            if isinstance(node, ast.If):
                if any(isinstance(s, ast.Return) for s in ast.walk(node)):
                    out.append((name, "guard", node.test))
            elif isinstance(node, ast.Return) and node.value is not None:
                out.append((name, "value", node.value))
    return out


def deciding_operands(src, fname):
    """Every operand of every `and`/`or` INSIDE a deciding condition."""
    out, seen = [], set()
    for name, kind, cond in deciding_conditions(src):
        for node in ast.walk(cond):
            if isinstance(node, ast.BoolOp):
                for v in node.values:
                    key = _span(v)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({"file": fname, "func": name, "kind": kind,
                                "op": "or" if isinstance(node.op, ast.Or)
                                      else "and",
                                "text": ast.get_source_segment(src, v),
                                "span": key})
    return out


# ---------------------------------------------------------------------------
# the qualifier rule.  mg-2c77's, character for character.
# ---------------------------------------------------------------------------

QUOTE_MARKERS = ("NO FURTHER", "is read as")


def score_qualifier(lines, idx, window=3):
    """QUALIFIED iff the UNHYPHENATED words `deciding condition` stand within
    `window` lines of the site.

    THE UNHYPHENATED FORM ONLY.  A site carrying `deciding-condition` scores
    UNQUALIFIED, exactly as mg-2c77's rule scored mg-2c77's own lines.  This
    audit cannot close a finding by widening the ruler, and the constructed
    site in the selftest asserts it.
    """
    lo, hi = max(0, idx - window), min(len(lines), idx + window + 1)
    near = "\n".join(lines[lo:hi])
    return QUALIFIER in near


def term_sites(text):
    """[(line index, line)] for every line stating the term."""
    lines = text.splitlines()
    return [(i, ln) for i, ln in enumerate(lines) if TERM in ln]


# ---------------------------------------------------------------------------
# the report
# ---------------------------------------------------------------------------

def rule(title):
    print("\n" + "-" * 74)
    print(title)
    print("-" * 74)


def banner(tag, title):
    print("=" * 74)
    print("%s  %s" % (tag, title))
    print("=" * 74)


class Report(object):
    """SELF-ERRORS and FINDINGS, counted separately and each naming its
    population.  Exit 0 iff both are 0.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop = selfpop
        self.findpop = findpop
        self.selferrs = []
        self.findings = []

    def selferr(self, msg):
        self.selferrs.append(msg)
        print("   *** SELF-ERROR: %s" % msg)

    def finding(self, msg):
        self.findings.append(msg)
        print("   *** FINDING: %s" % msg)

    def gate(self, ok, msg):
        """Book `msg` as a finding iff `ok` is false.  Returns `ok`."""
        if not ok:
            self.finding(msg)
        return ok

    def selfgate(self, ok, msg):
        if not ok:
            self.selferr(msg)
        return ok

    def done(self):
        print("\n" + "-" * 74)
        print("SELF-ERRORS: %d, population: %s" % (len(self.selferrs),
                                                   self.selfpop))
        for m in self.selferrs:
            print("   SELF-ERROR: %s" % m)
        print("FINDINGS: %d, population: %s" % (len(self.findings),
                                                self.findpop))
        for m in self.findings:
            print("   FINDING: %s" % m)
        bad = len(self.selferrs) + len(self.findings)
        print("TOTAL BAD: %d" % bad)
        raise SystemExit(1 if bad else 0)
