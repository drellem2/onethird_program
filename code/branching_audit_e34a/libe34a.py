"""libe34a.py -- the apparatus for the independent audit of mg-76cc (4755d02).

mg-76cc repaired mg-957f's F-1: the kernel half of g1_provenance.py's
measurement-invariance predicate.  This ticket audits that repair, and the
first instruction it carries is the one that found F-1 in the first place:

    take the predicate AS IT STOOD BEFORE THIS REPAIR, run it against the same
    inputs, and compare what each catches.

So the load-bearing tool here is `install_pinned`, not any reader.  Everything
else exists to make its answer trustworthy.

WHAT IS WRITTEN FRESH, AND WHY

  * `PRE_REV` is DERIVED, not written down.  lib76cc.py carries
    `REV_957F = "e006581c..."` as a literal beside the comment "g1 BEFORE
    mg-76cc".  A literal is a claim that stops being checked the moment the
    file moves.  Here the pre-repair revision is computed: the last commit
    that touched g1_provenance.py, and then its first parent.  If that
    disagrees with what mg-76cc wrote down, the disagreement is a finding and
    not a silent difference -- and it is checked in the selftest.

  * `REV_A218` is READ OUT OF lib58da.py's own source rather than copied.
    Copying a pinned constant into a third file is how three files come to
    disagree about one revision.

  * The transcript readers here parse by SPLITTING ON A COLON and reading a
    leading integer.  lib76cc walks characters with `isdigit`; lib58da uses
    `re`.  Two readers that share an implementation share a blind spot.  And
    this one CROSS-CHECKS the printed count against the number of listed
    lines, which neither of the other two does: a script whose trailer says
    FINDINGS 3 and lists 2 is broken in a way a count-only reader cannot see.

  * Every mutation is a COMMIT in a temp clone, because g1 reads c1 and the
    kernel with `git show` and a working-tree edit reaches nothing at all.
    A probe that comes back silent because it never existed looks exactly
    like a probe that came back silent because the predicate is fine.

NOTHING HERE WRITES INTO code/branching_audit_58da/,
code/branching_audit_a218/, code/branching_audit_957f/ or
code/branching_repair_76cc/.  Every run happens in a clone under /tmp.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

S58DA_DIR = "code/branching_audit_58da"
A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
R76CC_DIR = "code/branching_repair_76cc"

G1_REL = S58DA_DIR + "/g1_provenance.py"
LIB_REL = S58DA_DIR + "/lib58da.py"
C1_REL = A218_DIR + "/c1_branching.py"
KERN_REL = A218_DIR + "/kern_a218.py"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

# the five files code/branching_audit_58da/run_all.sh writes -- enumerated
# from the runner's own source in k2, not from this list; this is the order
# they are reported in.
FIVE_OUTPUTS = ["out_selftest_58da.txt", "out_g1_provenance.txt",
                "out_g2_redo.txt", "out_g3_findings.txt", "out_g4_fleet.txt"]

UNTOUCHED_58DA = ["selftest_58da.py", "g2_redo.py", "g3_findings.py",
                  "g4_fleet.py"]

# c1's output splits here: everything before is what c1 COMPUTES, everything
# after is what it COMPARES.  The same split g1 uses, by the same marker.
C1_SPLIT = "(iii) EVERY CELL, AGAINST"


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    return subprocess.run(["git", "-C", repo] + list(args), check=True,
                          capture_output=True, text=True).stdout


def git_show(rev, path, repo=REPO):
    return git("show", "%s:%s" % (rev, path), repo=repo)


def head_rev(repo=REPO):
    return git("rev-parse", "HEAD", repo=repo).strip()


def resolve(rev, repo=REPO):
    return git("rev-parse", rev, repo=repo).strip()


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def last_touching(path, rev="HEAD", repo=REPO):
    """The most recent commit at or before `rev` that touched `path`."""
    out = git("log", "-1", "--format=%H", rev, "--", path, repo=repo).strip()
    return out or None


def commits_touching(path, since, until="HEAD", repo=REPO):
    out = git("log", "--format=%H", "%s..%s" % (since, until), "--", path,
              repo=repo)
    return [h for h in out.split() if h]


def files_of(rev, repo=REPO):
    out = git("show", "--name-only", "--format=", rev, repo=repo)
    return [p for p in out.split("\n") if p.strip()]


def is_ancestor(a, b, repo=REPO):
    p = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor",
                        a, b], capture_output=True, text=True)
    return p.returncode == 0


def distance(a, b, repo=REPO):
    return len([h for h in git("rev-list", "%s..%s" % (a, b),
                               repo=repo).split() if h])


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# the revisions, DERIVED
# ---------------------------------------------------------------------------

def read_literal(src, name):
    """The string literal assigned to `name` at the top level of `src`.

    Used to take REV_A218 out of lib58da.py rather than copying it here.  A
    pinned revision copied into a third file is how three files come to
    disagree about one revision, and this arc has already had that.
    """
    for line in src.splitlines():
        s = line.strip()
        if not s.startswith(name + " ="):
            continue
        rest = s.split("=", 1)[1].strip()
        if rest.startswith('"'):
            return rest[1:].split('"', 1)[0]
        if rest.startswith("'"):
            return rest[1:].split("'", 1)[0]
    raise ValueError("no top-level string literal %r in the source given"
                     % name)


REV_A218 = read_literal(read_worktree(LIB_REL), "REV_A218")

# THE REPAIR, AND THE PREDICATE AS IT STOOD BEFORE IT -- both derived from the
# log rather than written down.  REPAIR_REV is the last commit that touched
# g1_provenance.py; PRE_REV is its first parent.  Written this way because
# mg-76cc's own lib carries the pre-repair revision as a literal, and a
# literal cannot notice that the file moved again.
REPAIR_REV = last_touching(G1_REL)
PRE_REV = resolve(REPAIR_REV + "^") if REPAIR_REV else None

def nth_touching(path, n, repo=REPO):
    """The n-th most recent commit touching `path` (0 = most recent)."""
    out = git("log", "--format=%H", "--", path, repo=repo).split()
    return out[n] if n < len(out) else None


# g1 as it stood before mg-7e58, for context only: the parent of the commit
# one further back on the same file.  Derived the same way and for the same
# reason as PRE_REV.
_PREV_TOUCH = nth_touching(G1_REL, 1)
PRE_7E58_REV = resolve(_PREV_TOUCH + "^") if _PREV_TOUCH else None


# ---------------------------------------------------------------------------
# reading a transcript.  Split on the colon; cross-check the count against the
# lines.  No `re`, no character walking.
# ---------------------------------------------------------------------------

def _leading_int(s):
    out = ""
    for ch in s.strip():
        if ch.isdigit():
            out += ch
        else:
            break
    return int(out) if out else None


def trailer(out):
    """(SELF-ERRORS, FINDINGS) as the script's own trailer states them.

    None for a script that prints no such line -- which is NOT the same as 0
    and is never shown as 0.
    """
    s = f = None
    for line in out.splitlines():
        if line.startswith("SELF-ERRORS:"):
            s = _leading_int(line.split(":", 1)[1])
        elif line.startswith("FINDINGS:"):
            f = _leading_int(line.split(":", 1)[1])
    return s, f


def listed(out, kind):
    """The finding / self-error lines a script books AS ITS OWN.

    Two discriminators, and both are needed:

      * the line must come AFTER the trailer line that counts them, and
      * it must be indented by EXACTLY three spaces, which is the trailer's
        own indentation.

    Without them a `FINDING:` line QUOTED from a nested transcript is counted
    as the outer script's.  That is not hypothetical: out_g4_fleet.txt at HEAD
    quotes one at six spaces, in a section where g4 is reporting what another
    member's run said, and both lib58da's and lib76cc's readers count it.  k4
    (v) demonstrates it against that committed artifact.
    """
    tag = "   " + kind + ": "
    header = "%sS:" % kind if kind == "FINDING" else "SELF-ERRORS:"
    got, started = [], False
    for line in out.splitlines():
        if line.startswith(header):
            started = True
            continue
        if not started:
            continue
        if line.startswith(tag) and not line.startswith(tag[:3] + " "):
            got.append(line[len(tag):].strip())
    return got


def findings(out):
    return listed(out, "FINDING")


def selferrs(out):
    return listed(out, "SELF-ERROR")


def trailer_consistent(out):
    """(ok, why) -- the printed counts against the printed lines.

    Neither lib58da nor lib76cc asks this.  A trailer that says FINDINGS 3
    over a list of 2 is a defect no count-only reader can see.
    """
    s, f = trailer(out)
    bad = []
    if s is not None and s != len(selferrs(out)):
        bad.append("SELF-ERRORS says %d, %d lines listed"
                   % (s, len(selferrs(out))))
    if f is not None and f != len(findings(out)):
        bad.append("FINDINGS says %d, %d lines listed"
                   % (f, len(findings(out))))
    return (not bad), "; ".join(bad)


def names_files(text, pool=("c1_branching.py", "kern_a218.py",
                            "out_t1_tl.txt")):
    """Which of the reproduction's files a finding NAMES.

    The coverage question is not 'how many findings' but 'what did each one
    say'.  Two predicates that both exit 1 can still disagree about which file
    moved, and a count cannot see it.
    """
    return tuple(sorted(p for p in pool if p in text))


# ---------------------------------------------------------------------------
# clones.  Every mutation is a COMMIT.
# ---------------------------------------------------------------------------

def dirty_paths(repo=REPO):
    out = git("status", "--porcelain", "-z", "--untracked-files=all",
              repo=repo)
    return [e[3:] for e in out.split("\0") if len(e) > 3]


def clone(mutate=None, message="mg-e34a scratch commit", carry=True,
          commit=True):
    """A clone of this worktree with the working tree COMMITTED.

    Committed, because g1 reads c1 and the kernel with `git show`: an edit
    left in the working tree reaches nothing and the probe comes back silent
    for a reason that has nothing to do with the predicate.

    `commit=False` with `carry=False` gives a clone whose HEAD is EXACTLY this
    branch's HEAD -- used by k2, where the question is what the tree AS
    COMMITTED reproduces and an extra scratch commit would put the answer at a
    revision nobody can look up.

    Returns (tmpdir, tree).  The caller destroys tmpdir.
    """
    tmp = tempfile.mkdtemp(prefix="mge34a-")
    tree = os.path.join(tmp, "repo")
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", REPO, tree],
                   check=True, capture_output=True, text=True)
    if carry:
        for rel in dirty_paths():
            src, dst = os.path.join(REPO, rel), os.path.join(tree, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.isfile(src):
                shutil.copy(src, dst)
            elif os.path.isfile(dst):
                os.remove(dst)
    if mutate:
        mutate(tree)
    if commit:
        subprocess.run(["git", "-C", tree, "add", "-A"], check=True,
                       capture_output=True, text=True)
        subprocess.run(["git", "-C", tree, "-c", "user.name=mg-e34a",
                        "-c", "user.email=mg-e34a@local", "commit", "-q",
                        "--allow-empty", "-m", message],
                       check=True, capture_output=True, text=True)
    return tmp, tree


def destroy(tmp):
    shutil.rmtree(tmp, ignore_errors=True)


def install_pinned(tree, rev, name):
    """Put g1_provenance.py AND lib58da.py as of `rev` into `tree`, each under
    a name of its own, and repoint the pinned g1's import at the pinned lib.

    The library has to travel with the predicate.  mg-76cc changed
    lib58da.run_c1's signature in the same commit as g1, so a pre-repair g1
    run against the repaired library is not the pre-repair predicate -- it is
    a third thing that never existed.

    Exactly one substitution is made and it is asserted, so a silently
    unpatched import cannot pass for a pinned run.
    """
    libname = "lib58da_at_%s" % rev[:8]
    src = git_show(rev, G1_REL)
    old = "import lib58da as L"
    if src.count(old) != 1:
        raise ValueError("g1 at %s has %d %r lines, not 1"
                         % (rev[:8], src.count(old), old))
    src = src.replace(old, "import %s as L" % libname, 1)
    with open(os.path.join(tree, S58DA_DIR, libname + ".py"), "w") as fh:
        fh.write(git_show(rev, LIB_REL))
    with open(os.path.join(tree, S58DA_DIR, name), "w") as fh:
        fh.write(src)
    return name


def run_script(directory, name, repo=REPO, timeout=3600):
    p = subprocess.run(["python3", name], cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


def run_sh(directory, name, repo=REPO, timeout=3600):
    p = subprocess.run(["bash", name], cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


# ---------------------------------------------------------------------------
# running c1 with the script and the kernel as SEPARATE sources
# ---------------------------------------------------------------------------

def run_c1(target_text, c1_src, kern_src):
    """c1_branching.py with a chosen kernel, against a chosen target.

    Two sources, never one revision.  mg-957f's F-1 was exactly a signature
    that could not say "this script with that kernel", and an instrument that
    inherits the defect cannot measure it.
    """
    tmp = tempfile.mkdtemp(prefix="mge34a-c1-")
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
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True, timeout=1800)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def measuring_half(out):
    return out.split(C1_SPLIT)[0]


def vertex_cells(out):
    """(beta, n) -> ((p, dim), ...) out of c1's section (i).

    Read by splitting on 'set {' and then on commas -- lib58da uses a regex
    per row, lib957f ast.literal_eval, lib76cc str.partition.  Returns {} on
    an absent form; every caller treats {} as a SELF-ERROR rather than as an
    empty agreement.
    """
    got, beta = {}, None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("beta = ") and line[7:].strip().isdigit():
            beta = int(line[7:].strip())
            continue
        if beta is None or not line.startswith("n=") or "set {" not in line:
            continue
        head, _, body = line.partition("set {")
        n = _leading_int(head[2:])
        body = body.rsplit("}", 1)[0]
        cells = []
        for item in body.split(","):
            item = item.strip()
            if not item.startswith("p="):
                continue
            plabel, _, dlabel = item.partition(":dim")
            pv, dv = _leading_int(plabel[2:]), _leading_int(dlabel)
            if pv is None or dv is None:
                return {}
            cells.append((pv, dv))
        if n is None:
            return {}
        got[(beta, n)] = tuple(cells)
    return got


# ---------------------------------------------------------------------------
# bends.  Every one refuses on zero occurrences and on many.
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old[:60], n))
    return text.replace(old, new, 1)


KERN_V = ("        return [(p, self.dim_L(p)) for p in self.parts "
          "if self.dim_L(p) > 0]")
KERN_V_UP = ("        return [(p, self.dim_L(p) + 1) for p in self.parts "
             "if self.dim_L(p) > 0]")
C1_V = "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()"
C1_V_UP = ("        mine_vertices[(beta, n)] = [(p, d + 1) for p, d in "
           "algebras[(n, beta)].vertices()]")
C1_V_DOWN = ("        mine_vertices[(beta, n)] = [(p, d - 1) for p, d in "
             "algebras[(n, beta)].vertices()]")


def bend_kern_up(src):
    """kern_a218.py: every simple's dimension one too big."""
    return replace_once(src, KERN_V, KERN_V_UP)


def bend_c1_up(src):
    """c1_branching.py: the same regression one file up -- mg-7e58's probe."""
    return replace_once(src, C1_V, C1_V_UP)


def bend_c1_down(src):
    """c1_branching.py: dimensions one too SMALL.

    The half of the cancelling pair.  Paired with bend_kern_up the printed
    measurement is restored exactly, which is the input mg-76cc's own
    rationale for the `both together` row names and which nothing in that
    repair ever built.
    """
    return replace_once(src, C1_V, C1_V_DOWN)


def comment_c1(src):
    return src + "\n# mg-e34a control: a comment, and nothing more\n"


def comment_kern(src):
    """A comment appended to the KERNEL.

    mg-76cc's input list has a byte-only control for c1_branching.py and none
    for kern_a218.py -- the file the repair is about.  A restored half that
    fires on a comment is not restored.
    """
    return src + "\n# mg-e34a control: a comment in the kernel, and nothing more\n"


def touch_c1_compare(src):
    return src + '\nprint("   [mg-e34a control: comparing half touched]")\n'


# ---------------------------------------------------------------------------
# the report footer every script here shares
# ---------------------------------------------------------------------------

def banner(tag, title):
    print("=" * 74)
    print("%s  %s" % (tag, title))
    print("=" * 74)


def rule(title):
    print("-" * 74)
    print(title)
    print("-" * 74)


class Report(object):
    """SELF-ERRORS and FINDINGS, kept apart and each with its population.

    A script here exits 0 iff both are 0.  A non-zero exit means THIS SCRIPT
    HAS SOMETHING TO REPORT, never that it is broken.
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
