"""lib_0ba7.py -- the apparatus for the INDEPENDENT AUDIT of mg-b2af (14c6c3b).

mg-b2af repaired mg-330a's anchor-population census and its two OPENs.  This
audit was PRE-FILED IN THE SAME ACTION AS THAT REPAIR: `mg-0ba7` and `mg-b2af`
were created together, so the questions were fixed before either the repair or
its answers existed.

THE ONE INSTRUCTION THIS FILE IS BUILT AROUND

    RE-DERIVE THE POPULATION BY AST YOURSELF.  Do not accept the repair's
    count.  The parent's own finding was that a flag-grep misses call sites
    with no `--format=%H`, so a grep-based re-derivation would reproduce the
    very defect under audit.

So nothing here imports `classify_call` from `code/audit_330a/lib330a.py`.
The taxonomy below is written fresh from mg-330a's own DOCSTRING -- the prose
statement of the rule -- and then the two implementations are run over the
same call sites and compared row by row.  An audit that imports the subject's
classifier has compared a value with itself.

WHAT IS WRITTEN FRESH HERE, AND WHY

  * A SECOND CLASSIFIER (`kind_of`).  Same taxonomy, independent code.  a1
    prints every row where the two disagree.

  * IMPORT-RESOLVED CLOSURE (`bindings_of`, `helper_closure`).  The parent's
    no-`--format=%H` population is `sweep_helper_uses`, whose body carries the
    literal tuple `("last_touching", "nth_touching")`.  A search by FLAG has a
    population defined by a flag -- that is the parent's own headline.  A
    search by NAME has a population defined by a NAME-LIST, and this one has
    two entries while the repo defines eleven such functions and three
    different `last_touching`s.

    So the closure here is derived: SEED = every function whose body directly
    contains a history-derived revision call AND whose return value is
    tainted by it; CALL SITES = every call that reaches one of those
    definitions THROUGH THE CALLING FILE'S OWN BINDINGS (`from m import f`,
    `import m` + `m.f`, or a definition in the same module).  A bare-name
    match cannot tell `libe34a.last_touching` from `lib8d5e.last_touching`,
    and it counts every `main()` in the repository as a call to whichever
    `main` happened to contain a git call.

  * THE FLOOR (`REV_COMMANDS`).  `classify_call` returns None unless the call
    carries `log` AND a hash format.  `git rev-list`, `git rev-parse`,
    `git merge-base` and `git describe` produce revisions and carry neither.
    `rev_command_sites` counts them.  They are in NO published population of
    this arc.

  * EVERY NUMBER NAMES ITS POPULATION AND ITS GRAIN.  `Report` refuses a
    total that does not.  Where a number is READ out of somebody else's
    transcript it says READ.

  * MUTATION IS A COMMIT IN A CLONE.  Nothing here writes into
    `code/audit_330a/`, `code/repair_b2af/`, `code/branching_audit_e34a/`,
    `code/repair_8d5e/` or `code/repair_69d1/`.

Pure Python 3, no dependencies, NO NETWORK.
"""

import ast
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# ---------------------------------------------------------------------------
# the revisions this audit is ABOUT.  Pinned, with the reason beside each.
# Deriving "the newest commit of code/repair_b2af/" would be A-1's defect
# committed inside an audit of A-1's repair, and worse: the refinery rebases,
# so a derivation over a branch that has been rewritten answers about a tree
# nobody has.
# ---------------------------------------------------------------------------

# mg-b2af's three commits AS THEY SIT ON THIS BRANCH.  Pinned because they are
# the SUBJECT: re-deriving them would make the subject move when anybody
# commits.  They WILL be rewritten by the refinery -- see README, and see
# `same_content`, which is how this audit checks a commit survived a rebase.
B2AF_PREDICTIONS = "06c9271"
B2AF_REPAIR = "14c6c3b"
B2AF_EVIDENCE = "b1c3467"

# mg-330a's two, as they sit on main after the rebase the parent found.
A330A_REPAIR = "fba5f63"
A330A_PRE = "ea97d0a"

E34A_DIR = "code/branching_audit_e34a"
B2AF_DIR = "code/repair_b2af"
A330A_DIR = "code/audit_330a"
G1_REL = "code/branching_audit_58da/g1_provenance.py"

# The kinds mg-330a's taxonomy calls history-derived.  Written out here rather
# than imported, so that a change to the subject's tuple is a DISAGREEMENT
# this audit reports rather than a change this audit silently adopts.
HISTORY_KINDS = ("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED")

# Formats that make `git log` emit a revision.  `%h` is the abbreviated form
# and is a revision by any use; mg-330a's set is checked against this one in
# a1 rather than assumed equal.
HASH_FORMATS = ("--format=%H", "--pretty=%H", "--format=format:%H",
                "--format=%h", "--pretty=%h", "--format=format:%h",
                "%H", "%h")

# mg-330a's set, COPIED CHARACTER FOR CHARACTER from `lib330a._HASH_FORMATS`
# rather than imported, so that a1 can print the difference as a difference
# rather than adopt it.  The gap is one letter and it is the headline.
FORMATS_330A = ("--format=%H", "--pretty=%H", "--format=format:%H")

# THE FLOOR.  Four commands that produce a revision and carry no hash format
# at all, so no `log`+format rule can see them.
REV_COMMANDS = ("rev-list", "rev-parse", "merge-base", "describe")


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    p = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, text=True)
    return p


def gout(*args, **kw):
    p = git(*args, **kw)
    return p.stdout.strip() if p.returncode == 0 else ""


def resolve(rev, repo=REPO):
    return gout("rev-parse", "--verify", "%s^{commit}" % rev, repo=repo)


def subject(rev, repo=REPO):
    return gout("log", "-1", "--format=%s", rev, repo=repo)


def patch_id(rev, repo=REPO):
    """The stable patch-id of one commit.

    ANCESTRY GIVES A FALSE NEGATIVE AFTER A REBASE.  The refinery rebases
    before merging, so a commit that landed has a different sha and the same
    content.  `git patch-id --stable` is the identity that survives it.
    """
    p = subprocess.run(
        "git -C %s diff-tree -p --no-color %s | git patch-id --stable"
        % (repo, rev), shell=True, capture_output=True, text=True)
    out = p.stdout.split()
    return out[0] if out else ""


def same_content(a, b, repo=REPO):
    pa, pb = patch_id(a, repo), patch_id(b, repo)
    return bool(pa) and pa == pb


def blob_sha(rev, rel, repo=REPO):
    return gout("rev-parse", "%s:%s" % (rev, rel), repo=repo)


def show(rev, rel, repo=REPO):
    p = git("show", "%s:%s" % (rev, rel), repo=repo)
    return p.stdout if p.returncode == 0 else None


# ---------------------------------------------------------------------------
# THE SECOND CLASSIFIER -- written from mg-330a's docstring, not its code
# ---------------------------------------------------------------------------

def direct_strings(call):
    """Every string constant that is a DIRECT argument of `call`.

    Direct only: a string inside a nested call belongs to that call.  Written
    independently of `_strings_of`; the two are compared in a1 on constructed
    inputs as well as on the repo.
    """
    out = []

    def flat(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            out.append(node.value)
        elif isinstance(node, (ast.List, ast.Tuple)):
            for e in node.elts:
                flat(e)
        elif isinstance(node, ast.BinOp):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Constant) and isinstance(sub.value,
                                                                str):
                    out.append(sub.value)
        elif isinstance(node, ast.Starred):
            flat(node.value)
    for a in list(call.args) + [k.value for k in call.keywords]:
        flat(a)
    return out


def kind_of(strs):
    """The taxonomy of mg-330a's module docstring, implemented fresh.

    Returns a kind, or None when the call produces no revision.  The order of
    the tests below is the order the DOCSTRING states the classes in, which
    is not the order `classify_call` tests them in -- that is deliberate, and
    any row where the orders disagree is a row a1 prints.
    """
    if not any(s == "log" or s.endswith("log") for s in strs):
        return None
    if not any(s in HASH_FORMATS for s in strs):
        return None
    has_path = "--" in strs
    # RANGE first: `a..b` is a SET, and a set has no single revision to
    # re-point, whatever other flags travel with it.
    if any(".." in s for s in strs):
        return "RANGE"
    # PICKAXE: `-S` (string) and `-G` (regex) both select by a property of the
    # CONTENT.  A prose edit does not move either.
    if any(s.startswith("-S") or s.startswith("-G") for s in strs):
        return "PICKAXE"
    # OLDEST: the file's creation.  Stable against later edits, and named
    # apart so that lumping it with NEWEST cannot inflate the defect count.
    if "--reverse" in strs:
        return "OLDEST"
    if "-1" in strs:
        return "NEWEST" if has_path else "NEWEST-norestrict"
    if has_path:
        return "INDEXED"
    return "UNRESTRICTED"


def py_files(repo=REPO, subdir="code"):
    """[(rel, src, tree)] for every parseable `.py` under `<repo>/<subdir>`.

    POPULATION: files on disk at the worktree, walked.  GRAIN: one entry per
    FILE.  Unparseable files are returned separately and never skipped
    silently.
    """
    ok, bad = [], []
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
                ok.append((rel, src, ast.parse(src)))
            except (SyntaxError, UnicodeDecodeError) as exc:
                bad.append((rel, str(exc)))
    return sorted(ok), bad


def anchor_sites(repo=REPO, subdir="code"):
    """[{file,line,kind,strs,src}] -- MY census.

    POPULATION: every `ast.Call` node in every parseable `.py` under
    `<repo>/<subdir>`.  GRAIN: one row per CALL SITE.  Not per file, not per
    anchor, not per name.
    """
    rows = []
    files, bad = py_files(repo, subdir)
    for rel, src, tree in files:
        lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            strs = direct_strings(node)
            k = kind_of(strs)
            if k is None:
                continue
            rows.append({"file": rel, "line": node.lineno, "kind": k,
                         "strs": strs,
                         "src": lines[node.lineno - 1].strip()
                                if node.lineno <= len(lines) else ""})
    return rows, bad


def rev_command_sites(repo=REPO, subdir="code"):
    """THE FLOOR: calls to `rev-list` / `rev-parse` / `merge-base` /
    `describe`.

    POPULATION: every `ast.Call` under `<repo>/<subdir>` whose direct string
    arguments contain one of `REV_COMMANDS`.  GRAIN: one row per CALL SITE.

    Every one of these produces a revision and NONE of them can be seen by a
    rule that requires `log` plus a hash format.  `rev-parse HEAD` is the
    UNRESTRICTED defect written in four fewer characters.
    """
    rows = []
    files, _bad = py_files(repo, subdir)
    for rel, src, tree in files:
        lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            strs = direct_strings(node)
            hit = [s for s in strs if s in REV_COMMANDS]
            if not hit:
                continue
            # A `rev-parse` of a literal sha is a normalisation, not an
            # anchor; a `rev-parse` of HEAD or of a symbolic ref is an anchor.
            args = [s for s in strs if s not in REV_COMMANDS]
            moving = ("HEAD" in " ".join(args)) or not args
            rows.append({"file": rel, "line": node.lineno, "cmd": hit[0],
                         "strs": strs, "moving": moving,
                         "src": lines[node.lineno - 1].strip()
                                if node.lineno <= len(lines) else ""})
    return rows


# ---------------------------------------------------------------------------
# THE CLOSURE, RESOLVED BY IMPORT
# ---------------------------------------------------------------------------

def _tainted_return(fd):
    """True iff `fd` RETURNS a value derived from a history-derived call.

    A function that merely contains such a call (a `main` that prints one) is
    not a wrapper: its callers do not obtain an anchor from it.  This is a
    grain distinction and it is the difference between 269 call sites and the
    number a1 reports.
    """
    hist = set()
    for n in ast.walk(fd):
        if isinstance(n, ast.Call) and kind_of(direct_strings(n)) in \
                HISTORY_KINDS:
            hist.add(n)
    if not hist:
        return False, False
    tainted = set()
    # DEFECT #1 OF THIS INSTRUMENT, KEPT.  This propagation was first written
    # over `ast.Assign` alone.  `lib8d5e.last_lacking` and
    # `lib8d5e.base_before_dir` both do
    #     for h in git("log", "--format=%H", ...).split(): ... return h
    # -- the anchor arrives through a FOR TARGET, never through an
    # assignment -- so both scored `returns=False` and were dropped from the
    # closure.  Two real anchor helpers, excluded by a population defined by
    # the syntax I happened to think of first, inside an audit whose subject
    # is populations defined by what the searcher happened to look for.
    # Found by reading the seed table's own named rows, which is why the rows
    # are named.  Both readings are printed in a1 (iii).
    def _targets(node):
        if isinstance(node, ast.Assign):
            return node.targets, node.value
        if isinstance(node, ast.AnnAssign) and node.value is not None:
            return [node.target], node.value
        if isinstance(node, (ast.For, ast.AsyncFor)):
            return [node.target], node.iter
        if isinstance(node, ast.NamedExpr):
            return [node.target], node.value
        if isinstance(node, ast.withitem) and node.optional_vars is not None:
            return [node.optional_vars], node.context_expr
        return None, None

    for _ in range(3):                      # three rounds of propagation
        for n in ast.walk(fd):
            tgts, val = _targets(n)
            if tgts is None:
                continue
            src_hit = any(s in hist for s in ast.walk(val)) or any(
                isinstance(s, ast.Name) and s.id in tainted
                for s in ast.walk(val))
            if src_hit:
                for t in tgts:
                    for nm in ast.walk(t):
                        if isinstance(nm, ast.Name):
                            tainted.add(nm.id)
    for n in ast.walk(fd):
        if isinstance(n, ast.Return) and n.value is not None:
            if any(s in hist for s in ast.walk(n.value)):
                return True, True
            if any(isinstance(s, ast.Name) and s.id in tainted
                   for s in ast.walk(n.value)):
                return True, True
    return True, False


def seed_defs(repo=REPO, subdir="code"):
    """[{file,line,name,returns}] -- functions that OBTAIN a history-derived
    revision.

    POPULATION: every `FunctionDef` / `AsyncFunctionDef` under
    `<repo>/<subdir>`.  GRAIN: one row per DEFINITION.  `returns` is the
    taint test above: True means callers get the anchor, False means the
    function keeps it.
    """
    out = []
    files, _bad = py_files(repo, subdir)
    for rel, _src, tree in files:
        for fd in ast.walk(tree):
            if not isinstance(fd, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            has, ret = _tainted_return(fd)
            if has:
                out.append({"file": rel, "line": fd.lineno, "name": fd.name,
                            "returns": ret})
    return out


def _module_file(rel, modname, files_by_rel):
    """Resolve `modname` to a repo-relative `.py`, the way the scripts here
    actually import: same directory first (they all `sys.path.insert(0,
    HERE)`), then anywhere under `code/` as a unique basename.

    Returns None when the name is ambiguous or absent -- reported by the
    caller, never guessed.
    """
    top = modname.split(".")[0]
    same = os.path.join(os.path.dirname(rel), top + ".py")
    if same in files_by_rel:
        return same
    cands = [r for r in files_by_rel
             if os.path.basename(r) == top + ".py"]
    return cands[0] if len(cands) == 1 else None


def bindings_of(rel, tree, files_by_rel):
    """{local name -> (defining file, defined name)} for one module.

    Covers the three forms these scripts use:
        from m import f            -> f      -> (m.py, f)
        from m import f as g       -> g      -> (m.py, f)
        import m as L; L.f(...)    -> "L.f"  -> (m.py, f)      [alias form]
        def f(...)                 -> f      -> (this file, f)
    An `import *` is reported by the caller as UNRESOLVED rather than
    guessed.
    """
    b, aliases, star = {}, {}, False
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            if n.module is None:
                continue
            tgt = _module_file(rel, n.module, files_by_rel)
            for a in n.names:
                if a.name == "*":
                    star = True
                    continue
                if tgt:
                    b[a.asname or a.name] = (tgt, a.name)
        elif isinstance(n, ast.Import):
            for a in n.names:
                tgt = _module_file(rel, a.name, files_by_rel)
                if tgt:
                    aliases[a.asname or a.name.split(".")[0]] = tgt
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            b.setdefault(n.name, (rel, n.name))
    return b, aliases, star


def helper_closure(repo=REPO, subdir="code"):
    """THE POPULATION WITH NO `--format=%H`, DERIVED RATHER THAN NAMED.

    Returns (rows, unresolved, star_files).

    POPULATION: every `ast.Call` under `<repo>/<subdir>` that resolves,
    THROUGH THE CALLING FILE'S OWN BINDINGS, to a definition in `seed_defs`
    whose `returns` is True.  GRAIN: one row per CALL SITE.

    `unresolved` holds calls whose bare name matches a seed name but whose
    binding this instrument could not resolve -- counted and named, never
    dropped, because a population that quietly discards what it cannot handle
    is the shape this whole arc is about.
    """
    files, _bad = py_files(repo, subdir)
    files_by_rel = {r: t for r, _s, t in files}
    seeds = [s for s in seed_defs(repo, subdir) if s["returns"]]
    seed_key = {(s["file"], s["name"]) for s in seeds}
    seed_names = {s["name"] for s in seeds}

    rows, unresolved, stars = [], [], []
    for rel, src, tree in files:
        binds, aliases, star = bindings_of(rel, tree, files_by_rel)
        if star:
            stars.append(rel)
        lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            target = None
            bare = None
            if isinstance(f, ast.Name):
                bare = f.id
                target = binds.get(f.id)
            elif isinstance(f, ast.Attribute):
                bare = f.attr
                base = f.value
                if isinstance(base, ast.Name) and base.id in aliases:
                    target = (aliases[base.id], f.attr)
            if bare not in seed_names:
                continue
            row = {"file": rel, "line": node.lineno, "bare": bare,
                   "src": lines[node.lineno - 1].strip()
                          if node.lineno <= len(lines) else ""}
            if target is None:
                unresolved.append(row)
            elif target in seed_key:
                row["defined_in"] = target[0]
                rows.append(row)
            else:
                # Resolves to a real definition that is NOT a seed -- a name
                # collision.  This is the row a bare-name match gets wrong.
                row["defined_in"] = target[0]
                row["collision"] = True
                unresolved.append(row)
    return rows, unresolved, stars


def bare_name_closure(names, repo=REPO, subdir="code"):
    """The parent's method, reimplemented: match a BARE NAME anywhere.

    Kept so a1 can print both populations side by side.  GRAIN: one row per
    CALL SITE (the parent's `sweep_helper_uses` also emits DEF rows and sums
    the two into one figure; that is its own headline finding and this
    function does not repeat it).
    """
    rows = []
    files, _bad = py_files(repo, subdir)
    for rel, src, tree in files:
        lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            nm = (f.id if isinstance(f, ast.Name)
                  else f.attr if isinstance(f, ast.Attribute) else None)
            if nm in names:
                rows.append({"file": rel, "line": node.lineno, "bare": nm,
                             "src": lines[node.lineno - 1].strip()
                                    if node.lineno <= len(lines) else ""})
    return rows


# ---------------------------------------------------------------------------
# clones
# ---------------------------------------------------------------------------

def clone_at(rev, into=None):
    d = into or tempfile.mkdtemp(prefix="a0ba7_")
    p = subprocess.run(["git", "clone", "--quiet", "--no-hardlinks",
                        REPO, d], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError("clone failed: %s" % p.stderr)
    subprocess.run(["git", "-C", d, "checkout", "--quiet", rev],
                   capture_output=True, text=True)
    return d


def commit_in(tree, rel, new_text, message):
    full = os.path.join(tree, rel)
    with open(full, "w") as fh:
        fh.write(new_text)
    subprocess.run(["git", "-C", tree, "add", rel],
                   capture_output=True, text=True)
    p = subprocess.run(["git", "-C", tree, "commit", "--quiet", "-m", message],
                       capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError("commit failed: %s %s" % (p.stdout, p.stderr))
    return subprocess.run(["git", "-C", tree, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def rm_tree(d):
    shutil.rmtree(d, ignore_errors=True)


def run_py(script, cwd, timeout=1800):
    p = subprocess.run(["python3", script], cwd=cwd, capture_output=True,
                       text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------------------
# the two labels (F-2), re-derived
# ---------------------------------------------------------------------------

def kind_by_path(rel):
    """KIND, from the PATH -- the rule that decides treatment.

    A transcript and a prediction file are RECORDS: they state what was true
    at a run, and editing one falsifies it.  Everything else is a LIVE CLAIM
    -- a statement about the tree as it stands, which an edit can correct.
    """
    base = os.path.basename(rel)
    if base.startswith("out_") or base.endswith(".txt"):
        return "RECORD"
    if base == "PREDICTIONS.md":
        return "RECORD"
    return "LIVE CLAIM"


def scope_by_dir(rel, mine="code/anchor_population_audit_0ba7"):
    """SCOPE -- whose ticket owns the file.  A different question with a
    different answer, and the parent's finding is that mg-8d5e's summary
    reported this one as though it were `kind_by_path`.
    """
    return "MINE" if rel.startswith(mine) else "ANOTHER TICKET'S"


# ---------------------------------------------------------------------------
# output
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
    """SELF-ERRORS and FINDINGS, counted separately, each naming its
    population.  Exit 0 iff both are 0.

    `total` refuses to print a bare number: every count goes through it with
    a POPULATION and a GRAIN, because label/grain mismatch is what this whole
    lineage keeps finding.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop = selfpop
        self.findpop = findpop
        self.selferrs = []
        self.findings = []
        self.notes = []

    def selferr(self, msg):
        self.selferrs.append(msg)
        print("   *** SELF-ERROR: %s" % msg)

    def finding(self, msg):
        self.findings.append(msg)
        print("   *** FINDING: %s" % msg)

    def note(self, msg):
        self.notes.append(msg)
        print("   NOTE: %s" % msg)

    def gate(self, ok, msg):
        if not ok:
            self.finding(msg)
        return ok

    def selfgate(self, ok, msg):
        if not ok:
            self.selferr(msg)
        return ok

    def total(self, label, n, population, grain):
        if not population or not grain:
            self.selferr("a count was printed without a population or a "
                         "grain: %r" % label)
        print("   %-52s %6s   [population: %s; grain: %s]"
              % (label, n, population, grain))
        return n

    def done(self):
        print("\n" + "-" * 74)
        print("SELF-ERRORS: %d, population: %s"
              % (len(self.selferrs), self.selfpop))
        for m in self.selferrs:
            print("   SELF-ERROR: %s" % m)
        print("FINDINGS: %d, population: %s"
              % (len(self.findings), self.findpop))
        for m in self.findings:
            print("   FINDING: %s" % m)
        print("NOTES: %d (not scored)" % len(self.notes))
        for m in self.notes:
            print("   NOTE: %s" % m)
        bad = len(self.selferrs) + len(self.findings)
        print("TOTAL BAD: %d" % bad)
        raise SystemExit(1 if bad else 0)


def score(report, tag, predicted, actual, note="", hit=None):
    """Score one PREDICTIONS.md row.  A miss is PRINTED and KEPT; it is not a
    finding against the subject and it is not a self-error.  A refuted
    prediction is a RESULT.

    DEFECT #2 OF THIS INSTRUMENT, KEPT.  This function first scored `hit` as
    `predicted == actual` and nothing else.  Every RANGE row in
    PREDICTIONS.md -- `25..45 sites`, `21..30 sites`, `1..6` -- is a string
    beside an int, so `==` is False and a4's first transcript scored three
    HITS as MISSES, including one that was right by a margin of one.  A
    scorer whose comparison cannot express the prediction it is scoring will
    report a suite as worse than it was, which is the same class of error as
    reporting it as better.  Callers now pass `hit=` when the row is not an
    equality.

    THE FAILING TRANSCRIPT IS KEPT as `out_a4_labels_FIRSTFORM_miss3.txt`,
    and it is a REGENERATION, not the original bytes: a4 was re-run at the
    shipping commit with only the `hit=` arguments removed.  The original run
    went to a terminal and was never redirected to a file, and saying so is
    cheaper than letting a regenerated transcript pass for a captured one.
    The defect itself is also asserted live, on constructed input, in
    `selftest_0ba7.py` (10) -- so it is a running check and not only a story.
    """
    if hit is None:
        hit = (predicted == actual)
    print("   %-6s predicted %-24s measured %-24s %s%s"
          % (tag, repr(predicted), repr(actual),
             "HIT" if hit else "*** MISS",
             ("  -- " + note) if note else ""))
    return hit
