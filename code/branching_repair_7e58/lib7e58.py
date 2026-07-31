"""lib7e58.py -- the apparatus for mg-7e58's repair of mg-58da's provenance gear.

mg-321d found the same grain error INSIDE the fix that the fix was built to
remove.  Two sites, one root:

  G-1  g1_provenance.py asked "did the measuring half change?" and answered it
       with a FILE SHA.  The repair's own commit moved the file and not the
       measurement, so g1 exited 1 on a finding its own section (iv) refuted.
  G-2  g4_fleet.py attributed by "committed sha vs WORKING-TREE sha", so once
       673b4c0 landed it said ed9cde4 had touched c1_branching.py.  ed9cde4
       never touched it.

Both are repaired in place.  This directory is the instrument that checks the
repair, and it is written to be independent of the thing it checks:

  * it shares NO line with lib58da.py or lib321d.py -- the readers below are
    written from the file formats, not copied;
  * it re-derives the set-level property (10 pairs, 24 cells) from the files
    themselves rather than reading any figure out of g4's or h3's output;
  * scratch_clone() makes a real git clone of this worktree WITH THE WORKING
    TREE COMMITTED, which is the only way to ask the question mg-321d's G-3
    raises: does the repair still hold once it is a commit?

NOTHING HERE WRITES INTO code/branching_audit_58da/, code/branching_audit_a218/
or code/branching_locate_db09/.  Every mutation happens in a temp clone.
"""

import hashlib
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

REV_A218 = "286d5030902d09a7eb336a4a5dec18bf7b9de64c"   # reproduction taken here
REV_13B2 = "ed9cde49ab81002d7efc89d0944cab8e6316c14e"   # widened c2 only
REV_58DA = "673b4c005026f0caa47bd57079e0096afefffc6c"   # widened c1; G-1/G-2 born
REV_321D = "ef38841710edf28af76d0accc1c6aaf011ed9490"   # the audit being answered

S58DA_DIR = "code/branching_audit_58da"
S321D_DIR = "code/branching_audit_321d"
A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
        "c4_seam.py", "c5_record.py"]

BETAS = [3, 2, 1, 0]
NMAX = 6
CELLS = [(b, n) for b in BETAS for n in range(1, NMAX + 1)]   # the 24, ordered


# ---------------------------------------------------------------------------
# reporting.  Two channels, kept apart on purpose: "I could not read it" is a
# fact about THIS instrument and never a finding against anything else.
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
        """Book `msg` as a finding iff `ok` is false.  Returns ok."""
        if not ok:
            self.findings.append(msg)
        return ok

    def emit(self):
        print("-" * 74)
        print("SELF-ERRORS: %d, population: every git read, clone, subprocess "
              "run and parse this script performs" % len(self.self_errors))
        for x in self.self_errors:
            print("   SELF-ERROR: " + x)
        print("FINDINGS: %d, population: %s" % (len(self.findings),
                                                self.population))
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


def commits_touching(path, since, until="HEAD", repo=REPO):
    out = git("log", "--format=%H", "%s..%s" % (since, until), "--", path,
              repo=repo)
    return [h for h in out.split() if h]


def names_in(rev, repo=REPO):
    """Every path a commit touched, from --name-only.  A second, independent
    route to the same fact commits_touching() reports."""
    out = git("show", "--name-only", "--format=", rev, repo=repo)
    return sorted(p for p in out.split("\n") if p.strip())


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def head_rev(repo=REPO):
    return git("rev-parse", "HEAD", repo=repo).strip()


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

def run_script(directory, name, repo=REPO, timeout=900):
    p = subprocess.run(["python3", "-u", name],
                       cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


def totals_of(out):
    """(self, findings) as the script itself printed them, or (None, None)."""
    s = f = None
    for line in out.splitlines():
        m = re.match(r"SELF-ERRORS: (\d+)", line)
        if m:
            s = int(m.group(1))
        m = re.match(r"FINDINGS: (\d+)", line)
        if m:
            f = int(m.group(1))
    return s, f


def findings_of(out):
    return [line.split("FINDING: ", 1)[1].strip()
            for line in out.splitlines() if "   FINDING: " in line]


def scratch_clone(mutate=None, message="mg-7e58 scratch commit", carry=True):
    """A real git clone of this worktree with the WORKING TREE COMMITTED.

    This exists for one reason.  mg-321d's G-3 is that mg-58da's committed
    evidence was recorded while its own change was still uncommitted, and
    stopped reproducing the instant the commit landed.  A repair for that
    defect is itself evidence recorded before its own commit exists, so the
    only honest way to ask whether the repair survives being committed is to
    commit it somewhere and re-run.  `mutate(tree)` may edit the clone before
    the commit is made.

    Returns the clone's path; the caller destroys it.
    """
    tmp = tempfile.mkdtemp(prefix="mg7e58-")
    tree = os.path.join(tmp, "repo")
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    # carry the uncommitted working tree across; a clone only has HEAD
    if carry:
        for rel in _dirty_paths():
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
    subprocess.run(["git", "-C", tree, "-c", "user.name=mg-7e58",
                    "-c", "user.email=mg-7e58@local",
                    "commit", "-q", "--allow-empty", "-m", message],
                   check=True, capture_output=True, text=True)
    return tmp, tree


def _dirty_paths():
    """Every changed FILE, not directory: `--porcelain` collapses an untracked
    directory to one entry, and copying that as a file is an error."""
    out = git("status", "--porcelain", "-z", "--untracked-files=all")
    paths = []
    for entry in out.split("\0"):
        if len(entry) > 3:
            paths.append(entry[3:])
    return paths


def destroy(tmp):
    shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# readers.  Written from the file formats.  None of these is copied from
# lib58da.py or lib321d.py, which is the point: two readers that share a line
# share a blind spot, and a blind spot is what this whole arc is about.
# ---------------------------------------------------------------------------

_BLOCK_OPEN = "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT"
_BLOCK_SHUT = "T1c  SEMISIMPLICITY"


def target_cells(text):
    """(beta, n) -> tuple of dims, from out_t1_tl.txt's T1b2 vertex block.

    Anchored on the block and on the 'beta = <b>' header above each group, so
    a row of digits elsewhere in the file cannot be mistaken for a cell.
    """
    if _BLOCK_OPEN not in text:
        return {}
    seg = text.split(_BLOCK_OPEN, 1)[1].split(_BLOCK_SHUT, 1)[0]
    cells, beta = {}, None
    for line in seg.splitlines():
        head = re.match(r"\s*beta = (\d+)\s*$", line)
        if head:
            beta = int(head.group(1))
            continue
        row = re.match(r"\s*n=(\d+)\s+\[([0-9:,]*)\]\s*$", line)
        if row and beta is not None:
            body = row.group(2)
            dims = tuple(int(x.split(":")[1]) for x in body.split(",") if x)
            cells[(beta, int(row.group(1)))] = dims
    return cells


def c1_cells(out):
    """(beta, n) -> tuple of dims, from c1_branching.py's own section (i)."""
    cells, beta = {}, None
    for line in out.splitlines():
        head = re.match(r"\s*beta = (\d+)\s*$", line)
        if head:
            beta = int(head.group(1))
            continue
        row = re.match(r"\s*n=(\d+)\s+count \d+\s+set \{(.*)\}\s*$", line)
        if row and beta is not None:
            body = row.group(2).strip()
            dims = tuple(int(m.group(1)) for m in
                         re.finditer(r"p=\d+:dim (\d+)", body))
            cells[(beta, int(row.group(1)))] = dims
    return cells


def c2_cells(out):
    """(beta, n) -> tuple of dims, from c2_vertexsets.py's 'mine, as sets' row.

    c2 prints one line per parameter carrying all six levels as a list of
    lists, so the row is split rather than matched level by level.
    """
    cells = {}
    for line in out.splitlines():
        m = re.match(r"\s*beta=(\d+) : .*-- mine, as sets: \[\[(.*)\]\]\s*$",
                     line)
        if not m:
            continue
        groups = re.findall(r"\[([0-9,\s]*)\]", "[" + m.group(2) + "]")
        if len(groups) != NMAX:
            continue
        for n, g in enumerate(groups, start=1):
            cells[(int(m.group(1)), n)] = tuple(
                int(x) for x in g.split(",") if x.strip())
    return cells


def b1_cells(text):
    """(beta, n) -> tuple of dims, from mg-2060's out_b1_branching.txt.

    b1 heads its groups 'beta=3:' -- not 'beta = 3' -- and lays each level out
    as 'n=6  vertices p = [...]   dims [...]'.  mg-321d's h3 was first written
    with the other header form, read nothing, and booked FOUR findings against
    an instrument that agrees at 24 of 24.

    This reader was written with that on the page and STILL got it wrong on its
    first run: it accepted both header forms and then matched a row shape b1
    does not use, so it returned 0 cells.  It is left recorded because the
    lesson is not the header -- it is that a reader is checked by running it.
    The control flow is what makes the miss harmless: a parse yielding no cells
    is a SELF-ERROR at the call site and the source is WITHDRAWN, never scored
    as disagreeing.
    """
    cells, beta = {}, None
    for line in text.splitlines():
        head = re.match(r"\s*beta\s*=\s*(\d+)\s*:\s*$", line)
        if head:
            beta = int(head.group(1))
            continue
        row = re.match(r"\s*n=(\d+)\s+vertices p = \[[0-9,\s]*\]\s+"
                       r"dims \[([0-9,\s]*)\]\s*$", line)
        if row and beta is not None:
            dims = tuple(int(x) for x in row.group(2).split(",") if x.strip())
            cells[(beta, int(row.group(1)))] = dims
    return cells


def e1_cells(text):
    """(beta, n) -> tuple of dims, from mg-d330's out_e1_vertexsets.txt.

    e1 lays all six levels on the 'beta = <b>' line itself.
    """
    cells = {}
    for line in text.splitlines():
        m = re.match(r"\s*beta = (\d+)\s+((?:\[[0-9:,]*\]\s*)+)$", line)
        if not m:
            continue
        groups = re.findall(r"\[([0-9:,]*)\]", m.group(2))
        if len(groups) != NMAX:
            continue
        for n, g in enumerate(groups, start=1):
            cells[(int(m.group(1)), n)] = tuple(
                int(x.split(":")[-1]) for x in g.split(",") if x)
    return cells


# ---------------------------------------------------------------------------
# corruption
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    """Replace exactly one occurrence, refusing on zero or many.

    A probe that changed nothing, or changed three things, would make every
    deletion test below say whatever it liked.
    """
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old, n))
    return text.replace(old, new, 1)
