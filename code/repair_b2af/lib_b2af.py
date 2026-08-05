"""lib_b2af.py -- the apparatus for the REPAIR of mg-330a's population and
its two OPENs.

mg-330a audited mg-8d5e and closed both sites it was sent at.  It also left
three things this ticket is about:

  THE POPULATION.  mg-330a asked "is there a fourth anchor" and answered it
  with a repo-wide `ast` sweep.  The brief for this ticket quotes that answer
  as `16 history-derived across 13 directories, of 36 sites`.  mg-330a's own
  committed transcript says `16 / 12 directories / 37 sites`.  Two of the
  seven figures in that sentence disagree with the transcript that produced
  it, and both landed in the same commit.

  F-1.  `ANCHOR_DRIFT` was gated in the two scripts that CHECK the anchor and
  in neither of the two that SPEND it.

  F-2.  `every one a record` reports r3 (iv)'s SCOPE label as r3 (iii)'s KIND
  label -- one word over two populations.

WHAT IS WRITTEN FRESH HERE, AND WHAT IS DELIBERATELY NOT

  * THE CENSUS IS TAKEN WITH mg-330a's OWN CLASSIFIER, IMPORTED.  This is the
    one place in this instrument where the subject's own code is used to
    measure the subject, and it is deliberate: the question is not "how many
    anchors are there" but "does mg-330a's published figure reproduce", and
    that question can only be asked with mg-330a's ruler.  A re-implementation
    would answer a different question and any disagreement would be
    attributable to my classifier rather than to their figure.  Where this
    instrument makes a claim of its own about the sites -- the frozen/moving
    refinement in `refine` below -- the analysis is written here, from the
    parse tree, and the two are reported in separate columns.

  * THE REFINEMENT DOES NOT SHRINK THE DENOMINATOR.  `classify_call` reads
    the flags.  It cannot see that `log -1 --format=%H e5787e1 -- <path>`
    carries a pinned revision and therefore cannot move, while
    `log -1 --format=%H -- <path>` moves on any later edit.  Both are
    `NEWEST`.  The refinement below separates them -- and the population
    stays whatever mg-330a's classifier says it is, with both numbers
    printed.  A repair that makes a defect population smaller by re-reading
    it is the failure this arc exists to catch, and it is the mirror image of
    the OLDEST inflation mg-330a warned about.

  * THE COMMIT A TRANSCRIPT WAS PRODUCED AT IS NOT ASSUMED TO BE THE COMMIT
    IT NOW SITS IN.  The refinery rebases.  A branch's commits get new shas
    and a new base, and a transcript committed on the pre-rebase branch is
    then sitting inside a commit whose tree it was never run against.
    mg-132a named that state DISPLACED.  `PRE_REBASE` below carries the
    pre-rebase twins, found by subject line in the object store rather than
    assumed, and every reproduction check is run at BOTH.

  * NOTHING HERE WRITES INTO ANOTHER TICKET'S DIRECTORY.  The two edits this
    repair makes to `code/branching_audit_e34a/` are the F-1 gate and are the
    subject of t2.  Every mutation for a demonstration happens in a clone
    under the system temp directory.

Pure Python 3, no dependencies, NO NETWORK.
"""

import ast
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# mg-330a's classifier, imported ON PURPOSE -- see the docstring.  The import
# is by path so that this file does not depend on how run_all.sh was invoked.
#
# The SyntaxWarning filter is for lib330a's own docstring, which contains an
# unescaped `\|` in a table.  It is suppressed rather than fixed: lib330a is
# another ticket's file, and editing it to quieten this instrument's output
# would be this repair writing into the directory it is auditing.
import warnings  # noqa: E402

warnings.filterwarnings("ignore", category=SyntaxWarning)
sys.path.insert(0, os.path.join(REPO, "code", "audit_330a"))
import lib330a as A330  # noqa: E402

# ---------------------------------------------------------------------------
# THE REVISIONS THIS REPAIR IS ABOUT.  Pinned, with the reason beside each.
# ---------------------------------------------------------------------------

# mg-330a's two commits AS THEY NOW SIT ON main, after the refinery rebased
# the branch.
INSTR_POST = "ea97d0a"      # "audit: the mg-330a instrument"
DOCS_POST = "fba5f63"       # "docs+audit: independent audit of ..."

# THE SAME TWO COMMITS AS THEY WERE WHEN THEIR TRANSCRIPTS WERE PRODUCED.
# NOT pinned by hand from somebody's prose: `pre_rebase_twin` below finds them
# by matching the subject line over every commit reachable from any ref, and
# the selftest checks that what it finds is NOT an ancestor of main.  They are
# written here as the answer that walk gave, so that a reader can see the
# figures without re-running it, and the walk is run anyway.
INSTR_PRE = "b94cb1e"
DOCS_PRE = "0ef9af9"

# mg-8d5e's repair -- the commit whose summary sentence F-2 is about.
REPAIR_8D5E = "dfa263cce851c847abc35cda1b718d918823e860"

# The term F-2 is about, copied character for character from mg-2c77's
# q3_operands.py by way of mg-330a's lib330a.py, so that this repair cannot
# close a finding by moving the ruler.
TERM = "explicit boolean operand"
QUALIFIER = "deciding condition"
QUOTE_MARKERS = ("NO FURTHER", "is read as")

# The four names `libe34a` derives, and the two scripts F-1 is about.
E34A_DIR = "code/branching_audit_e34a"
ANCHOR_NAMES = ("REPAIR_REV", "PRE_REV", "REV_7E58", "PRE_7E58_REV")

# This ticket's own directory.  Named once, used wherever a population is
# reported both including and excluding it.
MINE_DIR = "code/repair_b2af"

# The kinds mg-330a's classifier calls HISTORY-DERIVED.  Written out rather
# than inferred from the name, because `NEWEST-norestrict` is history-derived
# and does not look it.
HISTORY_KINDS = ("NEWEST", "NEWEST-norestrict", "INDEXED", "UNRESTRICTED")


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


def git_ok(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True).returncode == 0


def resolve(rev, repo=REPO):
    return git("rev-parse", rev, repo=repo).strip()


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def is_ancestor(a, b, repo=REPO):
    return git_ok("merge-base", "--is-ancestor", a, b, repo=repo)


def blob_sha(rev, path, repo=REPO):
    """The sha of the BLOB at `rev:path`, or None.

    Content identity, not commit identity.  Two anchors that resolve to
    different commits can still be pointing at the same file, and a
    distinctness check on commit shas cannot see it -- which is the sharpened
    lesson this ticket is told to preserve.
    """
    out = git_quiet("rev-parse", "%s:%s" % (rev, path), repo=repo).strip()
    return out or None


def first_introducing(path, marker, rev="HEAD", repo=REPO):
    """The OLDEST commit at or before `rev` where `marker` ENTERS `path`.

    Written here from the sentence -- "the marker is in `path` at the commit
    AND not in `path` at its first parent" -- and not imported from libe34a.
    An instrument that checks a derivation by calling that derivation has
    checked nothing.
    """
    hist = [h for h in git_quiet("log", "--format=%H", "--reverse", rev, "--",
                                 path, repo=repo).split() if h]
    for h in hist:
        if marker not in git_quiet("show", "%s:%s" % (h, path), repo=repo):
            continue
        ps = [x for x in git_quiet("rev-parse", h + "^@",
                                   repo=repo).split() if x]
        if not ps or marker not in git_quiet("show", "%s:%s" % (ps[0], path),
                                             repo=repo):
            return h
    return None


# THE COMMIT WHERE THE F-1 GATE LANDS, AND THE ONE BEFORE IT.
#
# DERIVED FROM THE PROPERTY, not pinned -- and the choice is the subject of
# this ticket, so it is worth stating why.  A pin here would be a sha on THIS
# branch, and the refinery rebases before merging: every commit gets a new
# sha, and the pin would be pointing into an unreachable object by the time
# anybody re-ran this.  That is precisely the DISPLACED failure t1 measures in
# mg-330a's own transcript.  The property survives the rebase because it is a
# property of the CONTENT.
E34A_LIB = E34A_DIR + "/libe34a.py"
MARK_GATE = "def gate_spent("

GATE_FALLBACK = []      # human-readable rows; [] means the derivation worked


def gate_landed(repo=REPO):
    """(the commit that introduced `gate_spent`, the commit before it).

    Returns (None, None) with a row in GATE_FALLBACK when the marker is in no
    commit -- which is the true state while this repair is still uncommitted.
    Reported, never silently treated as "no drift": a control that cannot be
    located is not a control that passed.
    """
    got = first_introducing(E34A_LIB, MARK_GATE, repo=repo)
    if got is None:
        GATE_FALLBACK.append(
            "the marker %r is in no commit of %s, so the commit where the "
            "F-1 gate lands could not be derived.  This is the expected "
            "state while the repair is uncommitted; the transcript that "
            "ships must be regenerated by the commit that ships it"
            % (MARK_GATE, E34A_LIB))
        return None, None
    return got, resolve(got + "^", repo=repo)


def clone_at(rev, into=None):
    """A clone of this repo checked out at `rev`, in a temp directory.

    A CLONE and not a worktree: the probes commit, and a worktree commit
    would land in the real repository's object store and be visible from it.
    """
    d = into or tempfile.mkdtemp(prefix="mgb2af-")
    tree = os.path.join(d, "tree")
    subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "checkout", "--quiet", rev],
                   check=True, capture_output=True, text=True)
    return tree


def cosmetic_commit(tree, rel, note="# mg-b2af cosmetic probe line\n"):
    """Append a comment to `rel` in `tree` and commit it.

    A COMMENT, so the file's history moves and none of its properties do.
    That is the whole input the frozen/moving distinction is tested on.
    """
    full = os.path.join(tree, rel)
    with open(full, "a") as fh:
        fh.write(note)
    subprocess.run(["git", "-C", tree, "add", rel],
                   check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "-c", "user.email=b2af@probe",
                    "-c", "user.name=mg-b2af probe",
                    "commit", "--quiet", "-m", "cosmetic: a comment line"],
                   check=True, capture_output=True, text=True)
    return resolve("HEAD", repo=tree)


def pre_rebase_twin(post_rev, repo=REPO):
    """The commit with the same SUBJECT as `post_rev` that is NOT reachable
    from it -- i.e. the pre-rebase original, if it survives.

    The refinery rebases a branch before merging it.  Every commit gets a new
    sha and a new base, and a transcript committed on the pre-rebase branch
    ends up sitting inside a commit whose tree it was never run against.  The
    original usually survives in the object store, unreferenced, and can be
    found because the rebase copies the subject line verbatim.

    Returns [] when nothing is found, which is a real answer and not an
    error: the pre-rebase commits are unreferenced and can be garbage
    collected at any time.
    """
    want = subject(post_rev, repo=repo)
    out = git_quiet("log", "--all", "--reflog", "--format=%H %s", repo=repo)
    got = []
    for line in out.splitlines():
        h, _, s = line.partition(" ")
        if s == want and h != resolve(post_rev, repo=repo) \
                and not is_ancestor(h, post_rev, repo=repo):
            got.append(h)
    return got


# ---------------------------------------------------------------------------
# THE CENSUS.  mg-330a's sweep, imported, plus the directory counts the
# published figures are stated in.
# ---------------------------------------------------------------------------

def census(repo=REPO):
    """Every figure the two published summaries state, from one sweep.

    Keyed by the name the summary uses, so that a comparison table cannot
    quietly compare two different things.
    """
    rows, unparsed = A330.sweep_anchor_calls(repo=repo)
    helpers = A330.sweep_helper_uses(repo=repo)
    hist = [r for r in rows if r["kind"] in HISTORY_KINDS]
    calls = [h for h in helpers if h["what"] == "CALL"]
    defs = [h for h in helpers if h["what"] == "DEF"]
    kinds = {}
    for r in rows:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    dirs_hist = {os.path.dirname(r["file"]) for r in hist}
    dirs_help = {os.path.dirname(h["file"]) for h in helpers}
    return {
        "ALL": len(rows),
        "HISTORY": len(hist),
        "NEWEST": kinds.get("NEWEST", 0),
        "INDEXED": kinds.get("INDEXED", 0),
        "UNRESTRICTED": kinds.get("UNRESTRICTED", 0),
        "OLDEST": kinds.get("OLDEST", 0),
        "PICKAXE": kinds.get("PICKAXE", 0),
        "RANGE": kinds.get("RANGE", 0),
        "helper_rows": len(helpers),
        "helper_CALL": len(calls),
        "helper_DEF": len(defs),
        "dirs_history": len(dirs_hist),
        "dirs_history_union_helpers": len(dirs_hist | dirs_help),
        "unparsed": len(unparsed),
        "_rows": rows,
        "_hist": hist,
        "_helpers": helpers,
    }


# ---------------------------------------------------------------------------
# THE REFINEMENT.  Written here, from the parse tree.  What `classify_call`
# cannot see: whether the revision is PINNED and whether the path is a
# LITERAL.
# ---------------------------------------------------------------------------

def _is_hexish(s):
    """A string that could be a revision written down: >=7 hex characters.

    Deliberately narrow.  `HEAD` is a revision and is NOT pinned -- it moves
    on every commit to the repo, which is the loudest version of the very
    defect being classified -- so it must not be counted as frozen.
    """
    return len(s) >= 7 and all(c in "0123456789abcdef" for c in s.lower())


def module_constants(abspath, _depth=0):
    """`{NAME: "literal"}` for module-level string assignments in `abspath`,
    following ONE level of `import <mod> as <alias>` for `alias.NAME`.

    Bounded on purpose.  A resolver that chases arbitrarily far would start
    guessing, and a guessed path silently produces a wrong answer for a site
    this instrument then reports as pinned.  Anything it cannot resolve comes
    back absent and the site is reported UNRESOLVED, never assumed.
    """
    try:
        with open(abspath) as fh:
            src = fh.read()
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError, IOError, OSError):
        return {}
    out, aliases = {}, {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for al in node.names:
                aliases[al.asname or al.name] = al.name
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            val = _fold(node.value, out, aliases, abspath, _depth)
            if val is not None:
                out[node.targets[0].id] = val
    if _depth == 0:
        # second pass: assignments that referred to a later import or to a
        # cross-module name now resolvable
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                    and isinstance(node.targets[0], ast.Name) \
                    and node.targets[0].id not in out:
                val = _fold(node.value, out, aliases, abspath, _depth)
                if val is not None:
                    out[node.targets[0].id] = val
    return out


def _fold(node, consts, aliases, abspath, depth):
    """A string constant, or None.  Constant / Name / alias.NAME / a + b /
    a % b -- and nothing else."""
    if isinstance(node, ast.Constant):
        return node.value if isinstance(node.value, str) else None
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        if depth > 0:
            return None
        mod = aliases.get(node.value.id)
        if not mod:
            return None
        other = os.path.join(os.path.dirname(abspath), mod + ".py")
        if not os.path.exists(other):
            return None
        return module_constants(other, _depth=depth + 1).get(node.attr)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a = _fold(node.left, consts, aliases, abspath, depth)
        b = _fold(node.right, consts, aliases, abspath, depth)
        return None if a is None or b is None else a + b
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mod):
        tmpl = _fold(node.left, consts, aliases, abspath, depth)
        if tmpl is None or tmpl.count("%s") != 1:
            return None
        arg = _fold(node.right, consts, aliases, abspath, depth)
        return None if arg is None else tmpl % arg
    return None


def _argv_of(call):
    """The git-log argv of `call`, as ast nodes, or None if this is not a
    shape this analysis understands.

    Two shapes occur in this repo: `git("log", ...)` where the wrapper
    supplies `git -C <repo>`, and `subprocess.run(["git", ..., "log", ...])`
    where it does not.  Both are reduced to the arguments AFTER the `log`
    token, which is the only part the taxonomy is about.
    """
    args = list(call.args)
    if args and isinstance(args[0], (ast.List, ast.Tuple)):
        args = list(args[0].elts)
    for i, a in enumerate(args):
        if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                and (a.value == "log" or a.value.endswith("log")):
            return args[i + 1:]
    return None


def _params_in_scope(tree, lineno):
    """Every parameter name of the innermost FunctionDef containing `lineno`.

    This is what makes "the path comes from a parameter" a measurement rather
    than a guess about naming: a lowercase name is not evidence, being bound
    as an argument is.
    """
    best, best_span = set(), None
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        end = getattr(node, "end_lineno", None)
        if end is None or not (node.lineno <= lineno <= end):
            continue
        span = end - node.lineno
        if best_span is None or span < best_span:
            a = node.args
            names = [x.arg for x in
                     list(getattr(a, "posonlyargs", [])) + list(a.args)
                     + list(a.kwonlyargs)]
            if a.vararg:
                names.append(a.vararg.arg)
            if a.kwarg:
                names.append(a.kwarg.arg)
            best, best_span = set(names), span
    return best


def refine(row, repo=REPO):
    """One site, analysed for what `classify_call` cannot see.

    Returns a dict with:
      rev       "PINNED" / "HEAD" / "VARIABLE" / "NONE"
      path      "LITERAL" / "PARAMETER" / "UNRESOLVED" / "NONE"
      literal   the resolved path, when there is one
      frozen    True iff a later commit to the path cannot move the answer
      spendable True iff this site can be re-resolved from outside, i.e. its
                path resolves to a literal AND its revision is a constant or
                absent.  That is the population that can go in ANCHORS.tsv.
    """
    abspath = os.path.join(repo, row["file"])
    try:
        with open(abspath) as fh:
            src = fh.read()
        tree = ast.parse(src)
    except (SyntaxError, UnicodeDecodeError, IOError, OSError):
        return {"rev": "UNRESOLVED", "path": "UNRESOLVED", "literal": None,
                "frozen": False, "spendable": False, "note": "did not parse"}
    call = None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.lineno == row["line"]:
            if _argv_of(node) is not None:
                call = node
                break
    if call is None:
        return {"rev": "UNRESOLVED", "path": "UNRESOLVED", "literal": None,
                "frozen": False, "spendable": False,
                "note": "the call at that line is not a shape this analysis "
                        "understands"}
    argv = _argv_of(call)
    consts = module_constants(abspath)
    params = _params_in_scope(tree, row["line"])

    sep = None
    for i, a in enumerate(argv):
        if isinstance(a, ast.Constant) and a.value == "--":
            sep = i
            break
    head = argv if sep is None else argv[:sep]
    tail = [] if sep is None else argv[sep + 1:]

    # revision candidates: anything before `--` that is not a flag
    revs = []
    for a in head:
        if isinstance(a, ast.Constant) and isinstance(a.value, str) \
                and a.value.startswith("-"):
            continue
        if isinstance(a, ast.keyword):
            continue
        revs.append(a)
    revs = [a for a in revs if not (isinstance(a, ast.Constant)
                                    and not isinstance(a.value, str))]

    rev_kind, rev_literal = "NONE", None
    for a in revs:
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            if _is_hexish(a.value):
                rev_kind, rev_literal = "PINNED", a.value
            else:
                rev_kind = "HEAD" if a.value == "HEAD" else "VARIABLE"
        else:
            rev_kind = "VARIABLE"
        break

    path_kind, literal = "NONE", None
    if tail:
        a = tail[0]
        literal = _fold(a, consts, {}, abspath, 0)
        if literal is None:
            literal = _fold(a, consts, _aliases_of(tree), abspath, 0)
        if literal is not None:
            path_kind = "LITERAL"
        elif isinstance(a, ast.Name) and a.id in params:
            path_kind = "PARAMETER"
        else:
            path_kind = "UNRESOLVED"

    frozen = rev_kind == "PINNED"
    spendable = (path_kind == "LITERAL"
                 and rev_kind in ("PINNED", "NONE")
                 and literal is not None)
    return {"rev": rev_kind, "rev_literal": rev_literal, "path": path_kind,
            "literal": literal, "frozen": frozen, "spendable": spendable,
            "note": ""}


def _aliases_of(tree):
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Import):
            for al in node.names:
                out[al.asname or al.name] = al.name
    return out


def resolve_site(row, ref, repo=REPO):
    """What a spendable site's derivation ANSWERS, at `ref`.

    Reconstructed from the site's own kind and its resolved path -- NEWEST
    takes the newest, INDEXED takes the list, OLDEST takes the oldest -- and
    run as a git command.  This is the only way to say "frozen" or "moving"
    by observation rather than by reading the flags a second time.
    """
    r = refine(row, repo=repo)
    if not r["spendable"]:
        return None
    args = ["log", "--format=%H"]
    if row["kind"] == "NEWEST":
        args.append("-1")
    if row["kind"] == "OLDEST":
        args.append("--reverse")
    # THE SITE'S OWN REVISION ARGUMENT, KEPT.  Dropping it would make a site
    # that pins its revision look like one that does not, and the whole point
    # of the refinement is that those two are different.  `ref` is used only
    # where the site itself names no revision, which is exactly where git
    # would default to HEAD.
    where = [r["rev_literal"]] if r["rev"] == "PINNED" else (
        [ref] if ref else [])
    out = git_quiet(*(args + where + ["--", r["literal"]]), repo=repo)
    hits = [h for h in out.split() if h]
    return hits[0] if hits else None


# ---------------------------------------------------------------------------
# ANCHORS.tsv -- ONE file, so that drift in thirteen directories becomes loud
# in one place.
# ---------------------------------------------------------------------------

ANCHORS_TSV = os.path.join(HERE, "ANCHORS.tsv")
TSV_HEADER = ("file", "line", "kind", "path", "rev", "resolved", "subject")


def read_anchors(path=ANCHORS_TSV):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != len(TSV_HEADER):
                continue
            if parts[0] == "file":
                continue
            rows.append(dict(zip(TSV_HEADER, parts)))
    return rows


def repin(path=ANCHORS_TSV, repo=REPO):
    """(Re)write ANCHORS.tsv from the tree as it stands.

    DELIBERATELY NOT RUN BY t1.  A pin that regenerates itself whenever it
    disagrees with the tree is not a pin -- it is a second copy of the tree
    that can never differ from it, and it would report green through exactly
    the drift it exists to catch.  t1 READS this file and compares.  When a
    site legitimately moves, a human runs:

        python3 -c "import lib_b2af as L; L.repin()"

    and the diff of this file is the record of what moved.
    """
    rows = []
    for r in sorted(census(repo=repo)["_hist"],
                    key=lambda x: (x["file"], x["line"])):
        ref = refine(r, repo=repo)
        if not ref["spendable"]:
            continue
        got = resolve_site(r, None, repo=repo)
        rows.append({
            "file": r["file"], "line": r["line"], "kind": r["kind"],
            "path": ref["literal"],
            "rev": ref["rev_literal"] or "(none -- defaults to HEAD)",
            "resolved": got or "",
            "subject": subject(got, repo=repo)[:70] if got else "",
        })
    write_anchors(rows, path=path)
    return rows


def write_anchors(rows, path=ANCHORS_TSV):
    with open(path, "w") as fh:
        fh.write("# mg-b2af -- THE PIN-AND-COMPARE FILE.\n")
        fh.write("# One row per history-derived site whose answer can be\n")
        fh.write("# re-resolved from outside the script that owns it.  t1\n")
        fh.write("# re-resolves every row and compares.  Drift in any of the\n")
        fh.write("# directories below becomes loud HERE, in one place.\n")
        fh.write("# A site is absent from this file when its path or its\n")
        fh.write("# revision comes from a parameter -- see t1 (iii), where\n")
        fh.write("# the absent ones are counted and named rather than\n")
        fh.write("# quietly dropped.\n")
        fh.write("\t".join(TSV_HEADER) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[k]) for k in TSV_HEADER) + "\n")


# ---------------------------------------------------------------------------
# F-2: the term, and the two labels.
# ---------------------------------------------------------------------------

def grep_sites(needle, repo=REPO):
    """[(path, line)] for every line stating `needle` in the worktree.

    `--untracked`, because this instrument's own files are untracked at the
    moment it runs and a population that excludes them by accident is a
    population drawn to pass.  mg-330a's rule, unchanged.
    """
    out = git_quiet("grep", "-n", "-F", "--untracked", needle, repo=repo)
    got = []
    for line in out.splitlines():
        if not line.strip():
            continue
        path, _, tail = line.partition(":")
        got.append((path, tail.split(":", 1)[0]))
    return got


_LINES = {}


def lines_of(path, repo=REPO):
    key = (repo, path)
    if key not in _LINES:
        try:
            with open(os.path.join(repo, path)) as fh:
                _LINES[key] = fh.read().splitlines()
        except (IOError, OSError, UnicodeDecodeError):
            _LINES[key] = []
    return _LINES[key]


def disposition(path, lineno, repo=REPO):
    """mg-2c77's three labels, from mg-2c77's rule, character for character."""
    lines = lines_of(path, repo=repo)
    i = int(lineno) - 1
    w = "\n".join(lines[max(0, i - 3):i + 4])
    if any(m in w for m in QUOTE_MARKERS):
        return "quotes the wide BOUND"
    if QUALIFIER in w:
        return "census, QUALIFIED"
    return "*** census, UNQUALIFIED"


def kind_of(path):
    """r3 (iii)'s rule: a site's KIND from its PATH.  This is the rule that
    decides whether a site gets EDITED."""
    base = os.path.basename(path)
    if base.startswith("out_") and base.endswith(".txt"):
        return "transcript"
    if base == "PREDICTIONS.md":
        return "record, pre-run"
    return "live claim"


def scope_of(path, mine=MINE_DIR):
    """r3 (iv)'s rule: a site's SCOPE from whose ticket owns the file.

    THE SECOND LABEL, written down separately BECAUSE it is the second label.
    F-2 is that these two were reported as one, and two rules that are one
    function are two rules that can be confused for one another again.
    """
    if path.startswith(mine + "/"):
        return "MINE"
    if path.startswith("code/audit_330a/"):
        return "the auditor's"
    return "another ticket's"


def residue(repo=REPO, exclude=()):
    """[(path, line, kind, scope)] for every site stating the term
    unqualified, excluding any path under a prefix in `exclude`."""
    got = []
    for p, n in grep_sites(TERM, repo=repo):
        if any(p.startswith(x) for x in exclude):
            continue
        if disposition(p, n, repo=repo).startswith("***"):
            got.append((p, n, kind_of(p), scope_of(p)))
    return sorted(got)


# ---------------------------------------------------------------------------
# reporting.  The convention is taken from code/branching_audit_e34a's
# run_all.sh so that the ruler for "did this pass" is somebody else's.
# ---------------------------------------------------------------------------

def banner(tag, title):
    print("=" * 74)
    print("%s -- %s" % (tag, title))
    print("=" * 74)


def rule(title):
    print("-" * 74)
    print(title)
    print("-" * 74)


class Report(object):
    """SELF-ERRORS and FINDINGS, kept apart and each with its population.

    Exit 0 iff both are 0.  A non-zero exit means THIS SCRIPT HAS SOMETHING
    TO REPORT, never that it is broken.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop, self.findpop = selfpop, findpop
        self.self_errors, self.findings = [], []

    def selferr(self, msg):
        self.self_errors.append(msg)

    def finding(self, msg):
        self.findings.append(msg)

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


def score(report, tag, predicted, actual, note=""):
    """Print one PREDICTIONS.md row scored against what was measured.

    A miss is PRINTED, never corrected.  It is a result.
    """
    hit = predicted == actual if not callable(predicted) else predicted(actual)
    print("   %-6s predicted %-28s measured %-16s %s%s"
          % (tag, predicted if not callable(predicted) else note,
             actual, "HIT" if hit else "*** MISS",
             "" if hit else "  <- kept as written"))
    return hit
