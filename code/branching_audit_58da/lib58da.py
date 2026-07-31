"""lib58da.py -- the reading and re-running apparatus for mg-58da.

This ticket asks two questions that are not the same question:

  A. are the 24 findings c1_branching.py now reports REAL?  (about the parser)
  B. does the 198-cell reproduction still stand?            (about provenance)

Neither is a question about Temperley-Lieb.  So there is NO fifth kernel here
and that is deliberate: the mathematics is measured by four instruments already
(mg-db09's t1_tl.py, mg-2060's b1_branching.py, mg-a218's kern_a218.py,
mg-d330's kern_d330.py) and this ticket adds nothing to it.  What this ticket
needs to be independent about is the PARSING and the RE-RUNNING, so that is
what is written fresh:

  * parse_vertex_sets() reads the target's T1b2 vertex block.  It shares no
    line with c1's parser -- c1 matches a beta digit followed by six integers
    on one line, this matches 'n=<k>  [p:d,...]' under a 'beta = <b>' header --
    and it is the reason the two can disagree about whether the datum is there.
  * run_c1() re-runs mg-a218's c1_branching.py AT A NAMED REVISION against a
    target text I choose, in a scratch tree.  Nothing is ever written into
    code/branching_audit_a218/ or code/branching_locate_db09/.

run_c1 is the load-bearing tool.  It lets the same script be run at the old
revision, at the new one, and against a target corrupted one character at a
time -- which is the only way to tell a live comparison from a blind one.
"""

import hashlib
import os
import re
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# The revision at which mg-a218 took the 198-cell reproduction.  Named, not
# implied: a claim about "the old revision" that does not name it is a claim
# nobody can re-run.
REV_A218 = "286d5030902d09a7eb336a4a5dec18bf7b9de64c"
REV_13B2 = "ed9cde49ab81002d7efc89d0944cab8e6316c14e"

A218_DIR = "code/branching_audit_a218"
DB09_DIR = "code/branching_locate_db09"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

BETAS = [3, 2, 1, 0]
NMAX = 6


# ---------------------------------------------------------------------------
# git
# ---------------------------------------------------------------------------

def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True, check=True).stdout


def git_show(rev, path):
    """File content at a revision, as text.  Raises if absent."""
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (rev, path)],
                          capture_output=True, text=True, check=True).stdout


def commits_touching(path, since, until="HEAD"):
    out = git("log", "--format=%H", "%s..%s" % (since, until), "--", path)
    return [h for h in out.split() if h]


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def head_rev():
    return git("rev-parse", "HEAD").strip()


def subject(rev):
    return git("log", "-1", "--format=%s", rev).strip()


# ---------------------------------------------------------------------------
# re-running mg-a218's c1 at a named revision against a chosen target
# ---------------------------------------------------------------------------

def read_worktree(rel):
    with open(os.path.join(REPO, rel)) as fh:
        return fh.read()


def run_c1(target_text, script_rev=REV_A218, script_source=None,
           kernel_rev=None, kernel_source=None):
    """Run c1_branching.py against `target_text`.

    `script_rev` names the revision the SCRIPT is taken from.  `script_source`
    optionally overrides the script text (used to run the repaired c1 out of
    the working tree).  Returns (stdout, returncode).

    `kernel_rev` names the revision kern_a218.py is taken from and DEFAULTS TO
    `script_rev`, so every call written before it existed behaves exactly as it
    did.  `kernel_source` overrides the kernel text outright, the way
    `script_source` overrides the script's.

    THE KERNEL IS A SEPARATE ARGUMENT BECAUSE THE MEASURING HALF IS TWO FILES
    (mg-76cc, on mg-957f's F-1).  This function used to bind the script and its
    kernel to one revision, and g1's section (v) passed REV_A218 for it on both
    sides of its comparison -- which pinned kern_a218.py at REV_A218 for both
    runs, so a kernel that moved between REV_A218 and HEAD could not reach
    either side of the check that was supposed to notice.  A signature that
    cannot express "this script with that kernel" cannot ask the question.

    Everything happens in a temporary directory.  c1 resolves its target as
    dirname(__file__)/../branching_locate_db09/out_t1_tl.txt, so the scratch
    tree mirrors exactly that two-directory shape and nothing else.
    """
    tmp = tempfile.mkdtemp(prefix="mg58da-")
    try:
        a = os.path.join(tmp, "a218")
        d = os.path.join(tmp, "branching_locate_db09")
        os.makedirs(a)
        os.makedirs(d)
        c1 = script_source
        if c1 is None:
            c1 = git_show(script_rev, A218_DIR + "/c1_branching.py")
        kern = kernel_source
        if kern is None:
            kern = git_show(kernel_rev or script_rev,
                            A218_DIR + "/kern_a218.py")
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(c1)
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(kern)
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def findings_of(out):
    return [l.split("FINDING: ", 1)[1].strip()
            for l in out.splitlines() if "   FINDING: " in l]


def selferrs_of(out):
    return [l.split("SELF-ERROR: ", 1)[1].strip()
            for l in out.splitlines() if "   SELF-ERROR: " in l]


def totals_of(out):
    """(self, findings, total_bad) as printed by the script itself."""
    s = f = t = None
    for l in out.splitlines():
        m = re.match(r"SELF-ERRORS: (\d+)", l)
        if m:
            s = int(m.group(1))
        m = re.match(r"FINDINGS: (\d+)", l)
        if m:
            f = int(m.group(1))
        m = re.match(r"TOTAL BAD: (\d+)", l)
        if m:
            t = int(m.group(1))
    return s, f, t


def compared_of(out):
    """The three population lines c1 prints, as ints."""
    got = {}
    for l in out.splitlines():
        m = re.search(r"(vertex counts|vertex cells|vertex sets|"
                      r"vertex dimensions|edge multiplicities): "
                      r"(\d+) cells compared", l)
        if m:
            got[m.group(1)] = int(m.group(2))
    return got


# ---------------------------------------------------------------------------
# the T1b2 block, read three ways.  None of these shares a line with c1.
# ---------------------------------------------------------------------------

T1B2_START = "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT"
T1B2_END = "T1c  SEMISIMPLICITY"


def t1b2(text):
    if T1B2_START not in text:
        raise ValueError("no T1b2 block")
    seg = text.split(T1B2_START, 1)[1]
    return seg.split(T1B2_END, 1)[0]


def parse_vertex_sets(text):
    """(beta, n) -> [(p, dim), ...] out of the SET form mg-13b2 installed.

    The set form looks like

        beta = 3
           n=1  [0:1]
           n=6  [0:1,1:5,2:9,3:5]

    Returns {} if the form is not present.  It does NOT fall back to the count
    form and it does NOT invent a cell: absence here means absence, which is
    the distinction the whole ticket turns on.
    """
    seg = t1b2(text)
    out = {}
    cur = None
    for line in seg.splitlines():
        m = re.match(r"\s*beta = (\d+)\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = re.match(r"\s*n=(\d+)\s+\[([\d:,]*)\]\s*$", line)
        if m and cur is not None:
            n = int(m.group(1))
            body = m.group(2)
            verts = []
            if body:
                for piece in body.split(","):
                    p, d = piece.split(":")
                    verts.append((int(p), int(d)))
            out[(cur, n)] = verts
    return out


def parse_vertex_counts_oldform(text):
    """(beta, n) -> count out of the COUNT table the old T1b2 (i) carried.

    The old form is a header row and then four rows of 'beta  c1..c6'.  This
    is read by ANCHORING ON THE HEADER, not by matching seven bare integers
    anywhere in the block, which is what c1 does and is why c1's parser can be
    fooled by an unrelated row of digits.  Returns {} if absent.
    """
    seg = t1b2(text)
    lines = seg.splitlines()
    out = {}
    for i, line in enumerate(lines):
        if not re.match(r"\s*beta\s+n=1\s+n=2\s+n=3\s+n=4\s+n=5\s+n=6\s*$", line):
            continue
        for row in lines[i + 1:i + 1 + 8]:
            m = re.match(r"\s*(\d+)((?:\s+\d+){6})\s*$", row)
            if not m:
                if row.strip() == "":
                    continue
                break
            b = int(m.group(1))
            nums = [int(x) for x in m.group(2).split()]
            for n, c in enumerate(nums, start=1):
                out[(b, n)] = c
    return out


def parse_edges(text):
    """(beta, n, p, q) -> multiplicity, and (beta, n, p) -> dim.

    Read off the 'L(n,p) dim d  ->  [L(n-1,q)]=m ...' lines of T1b2 (ii).
    """
    seg = t1b2(text)
    dims, edges = {}, {}
    cur = None
    for line in seg.splitlines():
        m = re.match(r"\s*-+\s*beta = (\d+)\s*-+\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = re.match(r"\s*L\((\d+),(\d+)\) dim (\d+)\s+->\s+(.*)$", line)
        if m and cur is not None:
            n, p, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
            dims[(cur, n, p)] = d
            for mm in re.finditer(r"\[L\((\d+),(\d+)\)\]=(\d+)", m.group(4)):
                edges[(cur, n, p, int(mm.group(2)))] = int(mm.group(3))
    return dims, edges


def render_set(verts):
    return "[" + ",".join("%d:%d" % (p, d) for p, d in verts) + "]"


# ---------------------------------------------------------------------------
# c1's own measurement, read out of its own stdout
# ---------------------------------------------------------------------------

def parse_c1_own_vertices(out):
    """(beta, n) -> [(p, dim)] out of c1's section (i).

    c1 prints its OWN measurement before it compares against anything, so this
    is c1's answer independent of whatever it could or could not read.
    """
    got = {}
    cur = None
    for line in out.splitlines():
        m = re.match(r"\s*beta = (\d+)\s*$", line)
        if m:
            cur = int(m.group(1))
            continue
        m = re.match(r"\s*n=(\d+)\s+count (\d+)\s+set \{ (.*) \}\s*$", line)
        if m and cur is not None:
            n = int(m.group(1))
            verts = []
            body = m.group(3).strip()
            if body:
                for piece in body.split(", "):
                    mm = re.match(r"p=(\d+):dim (\d+)$", piece.strip())
                    verts.append((int(mm.group(1)), int(mm.group(2))))
            got[(cur, n)] = verts
    return got


# ---------------------------------------------------------------------------
# corruption
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    """Replace exactly one occurrence, and refuse if there is not exactly one.

    A corruption probe that silently changed nothing, or changed three things,
    would make the deletion test say whatever it liked.
    """
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old, n))
    return text.replace(old, new, 1)


def replace_in_t1b2(text, old, new):
    """Replace exactly one occurrence INSIDE the T1b2 block.

    Scoped to the block because out_t1_tl.txt prints similar rows in other
    sections, and a probe that corrupted the wrong section would be testing
    something other than what it claims to test.
    """
    head, rest = text.split(T1B2_START, 1)
    seg, tail = rest.split(T1B2_END, 1)
    n = seg.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r inside T1b2, "
                         "found %d" % (old, n))
    return head + T1B2_START + seg.replace(old, new, 1) + T1B2_END + tail


def drop_lines(text, pred):
    """Delete every line for which pred(line) is true.  Returns (text, ndropped)."""
    keep, dropped = [], 0
    for line in text.splitlines(keepends=True):
        if pred(line.rstrip("\n")):
            dropped += 1
        else:
            keep.append(line)
    return "".join(keep), dropped
