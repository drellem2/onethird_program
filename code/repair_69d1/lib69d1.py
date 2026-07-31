"""lib69d1.py -- the apparatus for the mg-69d1 repair.

TWO SITES, TWO KINDS OF DEFECT, ONE MECHANISM.

  OPEN 1 (mg-eaef, E5 and E4)  A STATED BOUND WIDER THAN THE SWEEP IT
      DESCRIBES, with 4 of face_complex.py's 15 explicit boolean operands in
      NEITHER census column.  `neither column` is not a third state; it is the
      absence of an answer, and it is exactly the ambiguity a stated bound
      exists to remove.

  OPEN 2 (mg-e34a, E-1)  A ROW THAT IS RIGHT AND A REASON THAT IS INVERTED.
      mg-76cc added a row to g1's section (v) AND a reason for it, and only the
      row was checked.

THE MECHANISM IS THE SAME IN BOTH: a repair's output is more than one artifact.
mg-f7e1 produced a sweep AND a sentence about the sweep; only the sweep was
measured.  mg-76cc produced a row AND a reason; only the row was measured.
Verification that covers the primary artifact and not its accompanying
explanation leaves the explanation unaudited BY CONSTRUCTION.  So this
instrument's p4 enumerates the KINDS of artifact each repair emits -- rows,
reasons, labels, comments, docstrings, source anchors, transcripts, documents,
commit text -- and states a disposition for every copy it finds.

WHAT IS DERIVED RATHER THAN WRITTEN DOWN

  * `REV_A218` is read out of lib58da.py's own source, exactly as libe34a does
    it, so a fourth file does not become a fourth opinion about one revision.
  * The bound's file population is read out of d2_deletion.py's own
    `SWEEP_FILES` constant, not copied here.  If d2 starts sweeping a second
    file, p1 sweeps it too.
  * The reason under test is found by grepping the tree, so a copy this
    instrument did not remember is still in the population.

NOTHING HERE WRITES INTO code/face_geometry/, code/face_geometry_instr_5f9a/,
code/branching_audit_58da/, code/branching_audit_a218/,
code/branching_audit_e34a/ OR code/branching_repair_76cc/.  Every mutation
happens in a temporary directory; every subject script is RUN as a subprocess
with its stdout captured, never redirected over its committed transcript.

NO `| tee` ANYWHERE (mg-f922, mg-c2b3): run_all.sh redirects and re-reads $?.
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

# ---------------------------------------------------------------------- paths
FG_DIR = "code/face_geometry"
INSTR_DIR = "code/face_geometry_instr_5f9a"
S58DA_DIR = "code/branching_audit_58da"
A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
R76CC_DIR = "code/branching_repair_76cc"
E34A_DIR = "code/branching_audit_e34a"
EAEF_DIR = "code/face_geometry_audit_eaef"

D2_REL = INSTR_DIR + "/d2_deletion.py"
KERN5F9A_REL = INSTR_DIR + "/kern5f9a.py"
G1_REL = S58DA_DIR + "/g1_provenance.py"
LIB58DA_REL = S58DA_DIR + "/lib58da.py"
LIB76CC_REL = R76CC_DIR + "/lib76cc.py"
C1_REL = A218_DIR + "/c1_branching.py"
KERN_REL = A218_DIR + "/kern_a218.py"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

# c1's output splits here: before it is what c1 COMPUTES, after it is what it
# COMPARES.  The same marker g1 and libe34a use.
C1_SPLIT = "(iii) EVERY CELL, AGAINST"


# ---------------------------------------------------------------------------
# git and files
# ---------------------------------------------------------------------------

def git(*args, **kw):
    repo = kw.pop("repo", REPO)
    p = subprocess.run(["git", "-C", repo] + list(args),
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.strip()))
    return p.stdout


def git_show(rev, path, repo=REPO):
    return git("show", "%s:%s" % (rev, path), repo=repo)


def head_rev(repo=REPO):
    return git("rev-parse", "HEAD", repo=repo).strip()


def resolve(rev, repo=REPO):
    return git("rev-parse", rev, repo=repo).strip()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_literal(src, name):
    """The value of a module-level assignment, read out of the SOURCE.

    Importing would run the module; parsing reads the constant the file
    actually carries.  Used for REV_A218 and for d2's SWEEP_FILES, so neither
    is copied into this file to drift.
    """
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == name:
                    return ast.literal_eval(node.value)
    raise KeyError(name)


REV_A218 = read_literal(read_worktree(LIB58DA_REL), "REV_A218")

# The sweep's file population, read out of d2_deletion.py rather than repeated.
# mg-eaef's E4 was two populations about one thing, derived separately, twenty
# lines apart, disagreeing; a third copy here would be a third chance to.
SWEEP_FILES = tuple(read_literal(read_worktree(D2_REL), "SWEEP_FILES"))


# ---------------------------------------------------------------------------
# grep -- the population of a written claim
# ---------------------------------------------------------------------------

def grep(needle, rev=None):
    """[(path, line number)] for a fixed string.

    A claim written in five places is five claims.  Enumerating them with
    `git grep` rather than from a list means a copy nobody remembered is still
    in the population -- which is how mg-76cc's reason reached a source anchor
    in a file the repair never opened.

    `rev=None` reads the WORKING TREE, untracked files included, and that is
    the default on purpose: this is a repair, and a repair whose own population
    is read out of HEAD is scoring the defect rather than the fix.  Pass a
    revision to ask the same question of committed history.
    """
    args = ["git", "-C", REPO, "grep", "-n", "-F"]
    args += ([needle, rev] if rev else ["--untracked", needle])
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise RuntimeError("git grep: %s" % p.stderr.strip())
    got = []
    for line in p.stdout.splitlines():
        if not line.strip():
            continue
        # `rev:path:lineno:text` when a revision was named, `path:lineno:text`
        # when it was not.  Parsed by DROPPING the revision when one was asked
        # for rather than by guessing from the shape -- a path with a digit in
        # it would defeat a guess, and a mis-parsed path silently becomes a
        # site that cannot be read back off disk.
        rest = line.partition(":")[2] if rev else line
        path, _, tail = rest.partition(":")
        got.append((path, tail.split(":", 1)[0]))
    return got


def commit_message(rev):
    return git("log", "-1", "--format=%B", rev)


# ---------------------------------------------------------------------------
# running c1 with the script and the kernel as SEPARATE sources
# ---------------------------------------------------------------------------

def run_c1(target_text, c1_src, kern_src):
    """c1_branching.py with a chosen kernel, against a chosen target.

    Two sources, never one revision -- mg-957f's F-1 was exactly a signature
    that could not say "this script with that kernel".  An instrument that
    inherits the defect cannot measure the repair of it.
    """
    tmp = tempfile.mkdtemp(prefix="mg69d1-c1-")
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

    Returns {} on an absent form.  Every caller treats {} as a SELF-ERROR and
    never as an empty agreement: two runs that both failed to produce the form
    would otherwise compare equal, which is the "the run failed the same way"
    reading a comparison must never make.
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


def _leading_int(s):
    out = ""
    for ch in s.strip():
        if ch.isdigit():
            out += ch
        else:
            break
    return int(out) if out else None


# ---------------------------------------------------------------------------
# THE TWO PAIRS.  Every bend refuses on zero occurrences and on many, so a bend
# that silently did nothing cannot make a row below say whatever it likes.
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
C1_V_DOWN = ("        mine_vertices[(beta, n)] = [(p, d - 1) for p, d in "
             "algebras[(n, beta)].vertices()]")

# THE CONSPIRING HALVES.  Each is inert against the OTHER file as it stands and
# they move the measurement only together, which is the input `both together`
# exists for and which nothing in mg-76cc or mg-e34a ever built.
#
#   kern' defines a name old c1 never reads   -> harmless with old c1
#   c1'  reads that name with a default of 0  -> harmless with old kern
#   the two together                          -> every printed dimension +1
#
# The default is 0 and not 1: a conspiring half must be a NO-OP on its own, and
# a default that already shifted would make the c1 half a cancelling half.
KERN_CONSPIRE_TAIL = "\n\nDIM_SHIFT_69D1 = 1\n"
C1_V_CONSPIRE = (
    "        import kern_a218 as _k69d1\n"
    "        mine_vertices[(beta, n)] = [\n"
    "            (p, d + getattr(_k69d1, \"DIM_SHIFT_69D1\", 0))\n"
    "            for p, d in algebras[(n, beta)].vertices()]")


def bend_kern_up(src):
    """kern_a218.py: every simple's dimension one too BIG."""
    return replace_once(src, KERN_V, KERN_V_UP)


def bend_c1_down(src):
    """c1_branching.py: dimensions one too SMALL -- the cancelling half."""
    return replace_once(src, C1_V, C1_V_DOWN)


def conspire_kern(src):
    """kern_a218.py gains a module global that the shipped c1 never reads."""
    if "DIM_SHIFT_69D1" in src:
        raise ValueError("kern already carries DIM_SHIFT_69D1")
    return src + KERN_CONSPIRE_TAIL


def conspire_c1(src):
    """c1_branching.py reads that global, defaulting to a shift of 0."""
    return replace_once(src, C1_V, C1_V_CONSPIRE)


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


def finish(report):
    sys.exit(report.emit())
