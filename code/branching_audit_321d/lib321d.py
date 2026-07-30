"""lib321d.py -- the reading and re-running apparatus for mg-321d.

mg-321d is the independent audit of mg-58da (673b4c0), which repaired
code/branching_audit_a218/c1_branching.py.  So this instrument must not be one
of mg-a218's five, and it is not: it lives in its own directory, it is not
invoked by mg-a218's run_all.sh, and it writes into neither
code/branching_audit_a218/ nor code/branching_locate_db09/.

IT ALSO MUST NOT BE mg-58da's.  Nothing here imports lib58da, and the vertex
reader below is written differently on purpose:

  * c1's reader (both forms) is regex, and its count form matches seven bare
    integers anywhere in T1b2.
  * lib58da's reader is regex anchored on 'beta = <b>' anywhere in T1b2.
  * THIS reader is not regex at all.  It locates the subsection header
    '(i) THE VERTEX SET' first, stops at '(ii)', and splits the rows on
    literal delimiters.  Anchoring on the SUBSECTION is the difference that
    matters: a stray row of digits elsewhere in T1b2 cannot reach it.

Three readers that disagree about whether a datum is present is exactly the
apparatus this whole arc is about, so the third one is built rather than
borrowed.
"""

import hashlib
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# Named in full, not by prefix.  A revision named by prefix in prose is a
# revision the next reader has to guess at.
REV_A218 = "286d5030902d09a7eb336a4a5dec18bf7b9de64c"   # reproduction taken here
REV_13B2 = "ed9cde49ab81002d7efc89d0944cab8e6316c14e"   # widened c2 only
REV_D330 = "f9f8220"                                     # raised the 24
REV_58DA = "673b4c005026f0caa47bd57079e0096afefffc6c"   # the repair under audit

A218_DIR = "code/branching_audit_a218"
D330_DIR = "code/branching_audit_d330"
S58DA_DIR = "code/branching_audit_58da"
DB09_DIR = "code/branching_locate_db09"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"
DOC_58DA = "docs/OneThird-Bratteli-Path-Algebras-C1Parser-ProvenanceAndFindings.md"

BETAS = [3, 2, 1, 0]
NMAX = 6
CELLS = [(b, n) for b in BETAS for n in range(1, NMAX + 1)]   # the 24, ordered


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args, check=True):
    p = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr))
    return p.stdout


def git_show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def full_rev(rev):
    return git("rev-parse", rev).strip()


def head_rev():
    return full_rev("HEAD")


def subject(rev):
    return git("log", "-1", "--format=%s", rev).strip()


def commits_touching(path, since, until="HEAD"):
    """Every commit in (since, until] that touched `path`.  BY COMMIT.

    This is the honest form of the question 'who touched this file'.  The
    sha-difference form -- sha@A != sha@B -- answers 'did it change between two
    revisions', which is a different question and cannot attribute.
    """
    out = git("log", "--format=%H", "%s..%s" % (since, until), "--", path)
    return [h for h in out.split() if h]


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# re-running mg-a218's c1 at a chosen revision against a chosen target
# ---------------------------------------------------------------------------

def run_c1(target_text, script_rev=REV_A218, script_text=None, kern_rev=None):
    """Run c1_branching.py in a scratch tree.  Returns (stdout+stderr, rc).

    script_rev names where the script comes from; script_text overrides it
    (used to run the REPAIRED c1 out of the working tree).  kern_rev defaults
    to script_rev.  Nothing is written outside the scratch tree.
    """
    kern_rev = kern_rev or script_rev
    tmp = tempfile.mkdtemp(prefix="mg321d-")
    try:
        a = os.path.join(tmp, "audit")
        d = os.path.join(tmp, "branching_locate_db09")
        os.makedirs(a)
        os.makedirs(d)
        src = script_text
        if src is None:
            src = git_show(script_rev, A218_DIR + "/c1_branching.py")
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(src)
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(git_show(kern_rev, A218_DIR + "/kern_a218.py"))
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_in_repo(rel_dir, script, extra_env=None):
    """Run a script in place in the repo, capturing stdout.  Never redirects
    into any committed out_*.txt."""
    env = dict(os.environ)
    if extra_env:
        env.update(extra_env)
    p = subprocess.run(["python3", script], cwd=os.path.join(REPO, rel_dir),
                       capture_output=True, text=True, env=env)
    return p.stdout + p.stderr, p.returncode


# ---------------------------------------------------------------------------
# reading the standard SELF-ERRORS / FINDINGS / TOTAL BAD report
# ---------------------------------------------------------------------------

def totals_of(out):
    s = f = t = None
    for line in out.splitlines():
        if line.startswith("SELF-ERRORS: "):
            s = int(line.split("SELF-ERRORS: ")[1].split(",")[0].split()[0])
        elif line.startswith("FINDINGS: "):
            f = int(line.split("FINDINGS: ")[1].split(",")[0].split()[0])
        elif line.startswith("TOTAL BAD: "):
            t = int(line.split("TOTAL BAD: ")[1].split()[0])
    return s, f, t


def findings_of(out):
    return [l.split("FINDING: ", 1)[1].strip()
            for l in out.splitlines() if l.strip().startswith("FINDING: ")]


def selferrs_of(out):
    return [l.split("SELF-ERROR: ", 1)[1].strip()
            for l in out.splitlines() if l.strip().startswith("SELF-ERROR: ")]


def cells_compared(out):
    """The population figures c1 prints, whichever wording it uses.

    Deliberately accepts both the pre-repair wording ('vertex counts:') and the
    post-repair one ('vertex cells:').  A reader keyed on one wording alone
    goes blind when the other is printed -- which is the defect this whole arc
    is about, and this instrument is not going to reproduce it.
    """
    got = {}
    for line in out.splitlines():
        m = re.search(r"(vertex counts|vertex cells|vertex dimensions|"
                      r"edge multiplicities): (\d+) cells compared", line)
        if m:
            key = "vertex" if m.group(1).startswith("vertex c") else m.group(1)
            got[key] = int(m.group(2))
    return got


# ---------------------------------------------------------------------------
# MY reader for the target's vertex cells -- subsection-anchored, no regex
# ---------------------------------------------------------------------------

T1B2 = "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT"
T1C = "T1c  SEMISIMPLICITY"
SUB_I = "(i) THE VERTEX SET"
SUB_II = "(ii)"


def t1b2_block(text):
    if T1B2 not in text or T1C not in text:
        raise ValueError("no T1b2 block")
    return text.split(T1B2, 1)[1].split(T1C, 1)[0]


def vertex_subsection(text):
    """Just subsection (i) of T1b2 -- the vertex cells and nothing else.

    Returns "" if the subsection header is absent.  ABSENCE IS RETURNED AS
    ABSENCE.  It is never rendered as a value, which is the single mistake the
    whole ticket is about.
    """
    seg = t1b2_block(text)
    if SUB_I not in seg:
        return ""
    rest = seg.split(SUB_I, 1)[1]
    return rest.split(SUB_II, 1)[0] if SUB_II in rest else rest


def parse_vertex_cells(text):
    """(beta, n) -> [(p, dim), ...], read out of subsection (i) only.

    No regex.  Rows look like  'n=3  [0:1,1:2]'  under a 'beta = 2' header.
    A cell not present here is simply not in the dict.
    """
    out = {}
    cur = None
    for raw in vertex_subsection(text).splitlines():
        line = raw.strip()
        if line.startswith("beta = ") and line[7:].isdigit():
            cur = int(line[7:])
            continue
        if cur is None or not line.startswith("n=") or not line.endswith("]"):
            continue
        head, _, body = line.partition("[")
        n_txt = head[2:].strip()
        if not n_txt.isdigit():
            continue
        body = body[:-1]
        verts = []
        ok = True
        for piece in [x for x in body.split(",") if x]:
            p, _, d = piece.partition(":")
            if not (p.isdigit() and d.isdigit()):
                ok = False
                break
            verts.append((int(p), int(d)))
        if ok:
            out[(cur, int(n_txt))] = verts
    return out


def parse_c1_own_cells(out):
    """(beta, n) -> [(p, dim)] out of c1's own section (i) of its stdout.

    c1 prints its own measurement before it compares against anything, so this
    is c1's answer independent of what it could read.  Rows look like
    'n=3  count 2  set { p=0:dim 1, p=1:dim 2 }'.
    """
    got = {}
    cur = None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("beta = ") and line[7:].isdigit():
            cur = int(line[7:])
            continue
        if cur is None or not line.startswith("n=") or "set {" not in line:
            continue
        n_txt = line[2:].split()[0]
        if not n_txt.isdigit():
            continue
        body = line.split("set {", 1)[1].rsplit("}", 1)[0].strip()
        verts = []
        for piece in [x.strip() for x in body.split(",") if x.strip()]:
            p = piece.split("p=", 1)[1].split(":", 1)[0]
            d = piece.split("dim", 1)[1].strip()
            verts.append((int(p), int(d)))
        got[(cur, n_txt and int(n_txt))] = verts
    return got


def render(verts):
    return "[" + ",".join("%d:%d" % (p, d) for p, d in verts) + "]"


# ---------------------------------------------------------------------------
# report scaffolding, shared by h1..h4
# ---------------------------------------------------------------------------

class Report(object):
    """SELF-ERRORS and FINDINGS, each with a NAMED population.

    A bare total is a number nobody can check.  `population` is required.
    """

    def __init__(self, title, population):
        self.title = title
        self.population = population
        self.self_errs = []
        self.findings = []

    def selferr(self, m):
        self.self_errs.append(m)

    def finding(self, m):
        self.findings.append(m)

    def check(self, ok, msg):
        """Book `msg` as a finding iff not ok.  Returns ok."""
        if not ok:
            self.finding(msg)
        return ok

    def emit(self):
        print()
        print("-" * 74)
        print("SELF-ERRORS: %d, population: every git read, subprocess run and "
              "parse this script performs" % len(self.self_errs))
        for x in self.self_errs:
            print("   SELF-ERROR: " + x)
        print("FINDINGS: %d, population: %s"
              % (len(self.findings), self.population))
        for x in self.findings:
            print("   FINDING: " + x)
        print("TOTAL BAD: %d" % (len(self.self_errs) + len(self.findings)))
        return 1 if (self.self_errs or self.findings) else 0


def banner(tag, title):
    print("=" * 74)
    print("%s  %s" % (tag, title))
    print("=" * 74)


def rule(title):
    print()
    print("-" * 74)
    print(title)
    print("-" * 74)
