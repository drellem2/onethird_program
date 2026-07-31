"""lib957f.py -- the apparatus for mg-957f's independent audit of mg-7e58.

mg-7e58 repaired mg-58da's provenance gear on mg-321d's findings G-1 and G-2:

  G-1  g1_provenance.py asked "did the measuring half change?" and answered
       with a FILE SHA, so mg-58da's own commit made it exit 1 on a finding
       its own section (iv) refutes.
  G-2  g4_fleet.py attributed by "committed sha vs WORKING-TREE sha", so the
       instant 673b4c0 landed it said ed9cde4 had touched c1_branching.py.

This directory audits that repair.  Three things make it independent of both
the repair and the repair's own instrument:

  * every attribution is RE-DERIVED HERE from `git log`, by two routes, and
    then compared against what g4 prints.  Nothing is read out of g4's output
    and then checked against g4;
  * the readers below share no line with lib58da.py, lib321d.py or lib7e58.py.
    They are written on different mechanics -- token splitting and
    ast.literal_eval rather than one regex per row -- because two readers that
    share an implementation share a blind spot;
  * run_c1() here takes the SCRIPT and the KERNEL at independently chosen
    revisions.  mg-58da's own run_c1 binds both to one `script_rev`, which is
    the whole of finding F-1 below and cannot be seen with an instrument that
    inherits the same signature.

NOTHING HERE WRITES INTO code/branching_audit_58da/, code/branching_audit_a218/,
code/branching_audit_321d/, code/branching_repair_7e58/ OR
code/branching_locate_db09/.  Every mutation happens in a temp git clone or a
temp scratch tree.
"""

import ast
import hashlib
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

REV_A218 = "286d5030902d09a7eb336a4a5dec18bf7b9de64c"   # reproduction taken here
REV_13B2 = "ed9cde49ab81002d7efc89d0944cab8e6316c14e"   # widened c2 only
REV_58DA = "673b4c005026f0caa47bd57079e0096afefffc6c"   # widened c1; G-1/G-2 born
REV_321D = "ef38841710edf28af76d0accc1c6aaf011ed9490"   # the audit being answered
REV_7E58 = "4372fae9"                                   # resolved, never assumed

A218_DIR = "code/branching_audit_a218"
S58DA_DIR = "code/branching_audit_58da"
S321D_DIR = "code/branching_audit_321d"
DB09_DIR = "code/branching_locate_db09"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"
B1_REL = "code/branching_audit_2060/out_b1_branching.txt"
E1_REL = "code/branching_audit_d330/out_e1_vertexsets.txt"

FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
        "c4_seam.py", "c5_record.py"]

BETAS = [3, 2, 1, 0]
NMAX = 6
CELLS = [(b, n) for b in BETAS for n in range(1, NMAX + 1)]   # the 24, ordered


# ---------------------------------------------------------------------------
# reporting.  Two channels kept apart: "I could not read it" is a fact about
# THIS instrument and is never a finding against the thing being audited.
# ---------------------------------------------------------------------------

class Report(object):
    def __init__(self, name, population):
        self.name = name
        self.population = population
        self.self_errors = []
        self.findings = []

    def selferr(self, msg):
        self.self_errors.append(msg)

    def finding(self, msg):
        self.findings.append(msg)

    def check(self, ok, msg):
        if not ok:
            self.findings.append(msg)
        return ok

    def emit(self):
        print("-" * 74)
        print("SELF-ERRORS: %d, population: every git read, clone, subprocess "
              "run and parse this script performs" % len(self.self_errors))
        for x in self.self_errors:
            print("   SELF-ERROR: " + x)
        print("FINDINGS: %d, population: %s"
              % (len(self.findings), self.population))
        for x in self.findings:
            print("   FINDING: " + x)
        print("TOTAL BAD: %d" % (len(self.self_errors) + len(self.findings)))
        return 1 if (self.self_errors or self.findings) else 0


def banner(tag, title):
    print("=" * 74)
    print("%s  %s" % (tag, title))
    print("=" * 74)


def rule(title):
    print()
    print("-" * 74)
    print(title)
    print("-" * 74)


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True, check=True).stdout


def git_show(rev, path, repo=REPO):
    return subprocess.run(["git", "-C", repo, "show", "%s:%s" % (rev, path)],
                          capture_output=True, text=True, check=True).stdout


def resolve(rev, repo=REPO):
    """A revision as a full sha.  Written-down prefixes are resolved, never
    compared as strings: a prefix that no longer names a commit must raise."""
    return git("rev-parse", "%s^{commit}" % rev, repo=repo).strip()


def head_rev(repo=REPO):
    return resolve("HEAD", repo=repo)


def log_paths(rev_range, path, repo=REPO):
    """ROUTE ONE: the commits in `rev_range` that touched `path`."""
    out = git("log", "--format=%H", rev_range, "--", path, repo=repo)
    return [h for h in out.split() if h]


def show_names(rev, repo=REPO):
    """ROUTE TWO: every path one commit touched.  Independent of route one --
    it asks the commit what it did rather than asking the log about a path."""
    out = git("show", "--name-only", "--format=", rev, repo=repo)
    return sorted(p for p in out.split("\n") if p.strip())


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# running things
# ---------------------------------------------------------------------------

def run_script(directory, name, repo=REPO, timeout=1800):
    p = subprocess.run(["python3", "-u", name],
                       cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


def totals_of(out):
    """(self, findings) as the script itself printed them, or (None, None)."""
    s = f = None
    for line in out.splitlines():
        if line.startswith("SELF-ERRORS: "):
            s = int(line.split("SELF-ERRORS: ", 1)[1].split(",")[0].split()[0])
        if line.startswith("FINDINGS: "):
            f = int(line.split("FINDINGS: ", 1)[1].split(",")[0].split()[0])
    return s, f


def findings_of(out):
    return [line.split("FINDING: ", 1)[1].strip()
            for line in out.splitlines() if "   FINDING: " in line]


def run_c1(target_text, c1_src, kern_src):
    """Run mg-a218's c1_branching.py with the SCRIPT and the KERNEL chosen
    INDEPENDENTLY, against a target text supplied here.

    mg-58da's own run_c1 takes one `script_rev` and loads both the script and
    kern_a218.py from it, so it cannot express "this c1 with that kernel".
    Every question about whether a KERNEL change reaches c1's measurement needs
    exactly that, which is why this signature differs.

    c1 resolves its target as dirname(__file__)/../branching_locate_db09/…, so
    the scratch tree mirrors that two-directory shape and nothing else.
    """
    tmp = tempfile.mkdtemp(prefix="mg957f-c1-")
    try:
        a = os.path.join(tmp, "a218")
        d = os.path.join(tmp, "branching_locate_db09")
        os.makedirs(a)
        os.makedirs(d)
        for name, body in (("c1_branching.py", c1_src),
                           ("kern_a218.py", kern_src)):
            with open(os.path.join(a, name), "w") as fh:
                fh.write(body)
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True, timeout=1800)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


C1_SPLIT = "(iii) EVERY CELL, AGAINST"


def measuring_half(out):
    """c1's sections (i)+(ii) -- what it computes BEFORE comparing anything."""
    return out.split(C1_SPLIT)[0]


# ---------------------------------------------------------------------------
# clones
# ---------------------------------------------------------------------------

def dirty_paths(repo=REPO):
    """Every changed FILE, not directory: --porcelain collapses an untracked
    directory to a single entry and copying that as a file is an error."""
    out = git("status", "--porcelain", "-z", "--untracked-files=all", repo=repo)
    return [e[3:] for e in out.split("\0") if len(e) > 3]


def clone(mutate=None, message="mg-957f scratch commit", carry=True):
    """A real git clone of this worktree, with the working tree COMMITTED.

    `mutate(tree)` may edit the clone before the commit is made, so a probe can
    ask "what does this instrument say once THIS has landed as a commit" --
    which is the only grain at which G-2's defect exists at all.

    Returns (tmpdir, tree); the caller destroys tmpdir.
    """
    tmp = tempfile.mkdtemp(prefix="mg957f-")
    tree = os.path.join(tmp, "repo")
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    if carry:
        for rel in dirty_paths():
            src = os.path.join(REPO, rel)
            dst = os.path.join(tree, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isfile(src):
                shutil.copy(src, dst)
            elif os.path.isfile(dst):
                os.remove(dst)
    if mutate:
        mutate(tree)
    subprocess.run(["git", "-C", tree, "add", "-A"], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "-c", "user.name=mg-957f",
                    "-c", "user.email=mg-957f@local",
                    "commit", "-q", "--allow-empty", "-m", message],
                   check=True, capture_output=True, text=True)
    return tmp, tree


def destroy(tmp):
    shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# readers.  Five sources, five readers, written from the file formats on
# token-splitting and ast.literal_eval.  No line here is copied from
# lib58da.py, lib321d.py or lib7e58.py.
#
# Every one returns {} rather than a partial parse when the form it expects is
# absent, and every CALLER treats {} as a SELF-ERROR that withdraws the source.
# A blind reader agrees with everything, so silence must never be scored.
# ---------------------------------------------------------------------------

_OPEN = "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT"
_SHUT = "T1c  SEMISIMPLICITY"


def _t1b2(text):
    if _OPEN not in text or _SHUT not in text.split(_OPEN, 1)[1]:
        return None
    return text.split(_OPEN, 1)[1].split(_SHUT, 1)[0]


def _beta_of(tokens):
    """`beta = 3` and `beta=3:` and `beta=3` all name a parameter.  Returns the
    int or None, from TOKENS rather than from a regex over the line."""
    joined = "".join(tokens).rstrip(":")
    if not joined.startswith("beta="):
        return None
    tail = joined[len("beta="):]
    return int(tail) if tail.isdigit() else None


def _dims_from_pairs(body):
    """'0:1,1:5,2:9' -> (1, 5, 9).  The dim is the second half of each pair."""
    out = []
    for piece in body.split(","):
        piece = piece.strip()
        if not piece:
            continue
        if ":" not in piece:
            return None
        out.append(int(piece.split(":")[1]))
    return tuple(out)


def target_cells(text):
    """(beta, n) -> dims, from out_t1_tl.txt's T1b2 (i) block.

    Anchored on the block AND on the beta header, so a row of digits elsewhere
    in the file is not a cell.  Rows look like `n=6  [0:1,1:5,2:9,3:5]`.
    """
    seg = _t1b2(text)
    if seg is None:
        return {}
    cells, beta = {}, None
    for line in seg.splitlines():
        tok = line.split()
        if len(tok) in (1, 3) and _beta_of(tok) is not None:
            beta = _beta_of(tok)
            continue
        if beta is None or len(tok) != 2:
            continue
        if not tok[0].startswith("n=") or not tok[0][2:].isdigit():
            continue
        if not (tok[1].startswith("[") and tok[1].endswith("]")):
            continue
        dims = _dims_from_pairs(tok[1][1:-1])
        if dims is not None:
            cells[(beta, int(tok[0][2:]))] = dims
    return cells


def c1_cells(out):
    """(beta, n) -> dims, from c1_branching.py's own section (i), live.

    Rows look like `n=6  count 4  set { p=0:dim 1, p=1:dim 5, ... }`.  Read by
    splitting on the braces, not by matching the row as a whole.
    """
    cells, beta = {}, None
    for line in out.splitlines():
        tok = line.split()
        if len(tok) in (1, 3) and _beta_of(tok) is not None:
            beta = _beta_of(tok)
            continue
        if beta is None or "{" not in line or "}" not in line:
            continue
        if not tok or not tok[0].startswith("n=") or not tok[0][2:].isdigit():
            continue
        body = line.split("{", 1)[1].rsplit("}", 1)[0]
        dims = []
        for piece in body.split(","):
            piece = piece.strip()
            if not piece:
                continue
            if ":dim " not in piece:
                dims = None
                break
            dims.append(int(piece.split(":dim ")[1]))
        if dims is not None:
            cells[(beta, int(tok[0][2:]))] = tuple(dims)
    return cells


def c2_cells(out):
    """(beta, n) -> dims, from c2_vertexsets.py's `-- mine, as sets:` row, live.

    One line per parameter carrying all six levels as a list of lists, so the
    tail is handed to ast.literal_eval rather than matched.  A parameter whose
    row does not carry exactly NMAX levels is dropped, not padded.
    """
    cells = {}
    for line in out.splitlines():
        if "-- mine, as sets:" not in line:
            continue
        head, tail = line.split("-- mine, as sets:", 1)
        beta = _beta_of(head.split(":")[0].split())
        if beta is None:
            continue
        try:
            levels = ast.literal_eval(tail.strip())
        except (ValueError, SyntaxError):
            continue
        if not isinstance(levels, list) or len(levels) != NMAX:
            continue
        for n, lv in enumerate(levels, start=1):
            cells[(beta, n)] = tuple(int(x) for x in lv)
    return cells


def b1_cells(text):
    """(beta, n) -> dims, from mg-2060's out_b1_branching.txt.

    b1 heads its groups `beta=3:` and lays each level out as
    `n=6  vertices p = [...]   dims [...]`.  The dims list is taken by
    splitting on the word `dims` and evaluating what follows -- mg-321d's h3
    and mg-7e58's first b1 reader both foundered on matching the whole row.
    """
    cells, beta = {}, None
    for line in text.splitlines():
        tok = line.split()
        if len(tok) in (1, 3) and _beta_of(tok) is not None:
            beta = _beta_of(tok)
            continue
        if beta is None or " dims " not in line or not tok:
            continue
        if not tok[0].startswith("n=") or not tok[0][2:].isdigit():
            continue
        try:
            dims = ast.literal_eval(line.split(" dims ", 1)[1].strip())
        except (ValueError, SyntaxError):
            continue
        if isinstance(dims, list):
            cells[(beta, int(tok[0][2:]))] = tuple(int(x) for x in dims)
    return cells


def e1_cells(text):
    """(beta, n) -> dims, from mg-d330's out_e1_vertexsets.txt.

    e1 puts all six levels on the `beta = 3   [..]  [..] …` line itself, so the
    beta header and the cells are the same line and the reader splits rather
    than iterating a state machine.
    """
    cells = {}
    for line in text.splitlines():
        if "[" not in line:
            continue
        head, rest = line.split("[", 1)
        beta = _beta_of(head.split())
        if beta is None:
            continue
        groups = [g for g in ("[" + rest).replace("]", "] ").split()
                  if g.startswith("[") and g.endswith("]")]
        if len(groups) != NMAX:
            continue
        ok = {}
        for n, g in enumerate(groups, start=1):
            dims = _dims_from_pairs(g[1:-1])
            if dims is None:
                ok = None
                break
            ok[(beta, n)] = dims
        if ok:
            cells.update(ok)
    return cells


# ---------------------------------------------------------------------------
# corruption
# ---------------------------------------------------------------------------

KERN_VERTICES = ("        return [(p, self.dim_L(p)) for p in self.parts "
                 "if self.dim_L(p) > 0]")
KERN_VERTICES_BENT = ("        return [(p, self.dim_L(p) + 1) for p in "
                      "self.parts if self.dim_L(p) > 0]")


def bend_kernel(kern_src):
    """A real regression in kern_a218.py -- every simple's dimension off by one.

    The kernel is the file g1's own section (ii) labels "the measuring half",
    so this is the defect that label describes, made at the site the label
    names.  It is NOT a hook: it is the same shape as mg-7e58's own c1 probe,
    moved one file down to where c1 gets its numbers from.
    """
    return replace_once(kern_src, KERN_VERTICES, KERN_VERTICES_BENT)


def replace_once(text, old, new):
    """Replace exactly one occurrence, refusing on zero and on many.

    A probe that silently changed nothing, or changed three things, makes every
    deletion test below say whatever it likes.
    """
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old, n))
    return text.replace(old, new, 1)


def replace_in_block(text, old, new):
    """replace_once, scoped INSIDE the T1b2 block.  out_t1_tl.txt prints
    similar rows in other sections and a probe that hit the wrong section would
    be testing something other than what it claims to."""
    seg = _t1b2(text)
    if seg is None:
        raise ValueError("no T1b2 block")
    head, rest = text.split(_OPEN, 1)
    body, tail = rest.split(_SHUT, 1)
    if body.count(old) != 1:
        raise ValueError("expected exactly 1 occurrence of %r inside T1b2, "
                         "found %d" % (old, body.count(old)))
    return head + _OPEN + body.replace(old, new, 1) + _SHUT + tail
