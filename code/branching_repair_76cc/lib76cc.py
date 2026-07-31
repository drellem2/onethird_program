"""lib76cc.py -- the apparatus for mg-76cc's repair of mg-957f's two findings.

mg-957f audited mg-7e58 and left two sites open:

  F-1  THE KERNEL HALF OF THE PREDICATE IS GONE.  g1_provenance.py's file-sha
       finding covered TWO files -- c1_branching.py and kern_a218.py, the file
       g1's own section (ii) labels "the measuring half".  What replaced it
       took both sides of its comparison through run_c1(script_rev=REV_A218),
       which loads the kernel from that same revision, so a kernel that moved
       reached neither side.  A predicate over a population of two became one
       over a population of one, and the population shrank without being named.
       This is the first site in this arc where a repair REMOVED DETECTION
       rather than relocating a defect.

  F-2  G-3 IS SHUT AT ONE REVISION.  mg-7e58 closed mg-321d's G-3 -- "the
       documented reproduce command does not reproduce" -- on evidence in which
       1 of 5 committed outputs still reproduces byte for byte.

Three things keep this directory independent of what it repairs:

  * it imports nothing from code/branching_audit_58da/, and nothing from
    lib321d, lib7e58 or lib957f.  run_c1() below takes the script and the
    kernel as two separate SOURCES, because the whole of F-1 is a signature
    that could not say "this script with that kernel";
  * the readers are written on a third mechanic.  lib58da reads c1's own
    vertex sets with one regex per row; lib957f reads them with token splitting
    and ast.literal_eval; this file uses str.partition and imports no `re` at
    all.  Two readers that share an implementation share a blind spot;
  * every comparison against a committed transcript is made in a temp git
    CLONE, because code/branching_audit_58da/run_all.sh redirects into the very
    files under test.

NOTHING HERE WRITES INTO code/branching_audit_58da/,
code/branching_audit_a218/, code/branching_audit_321d/,
code/branching_audit_957f/, code/branching_repair_7e58/ OR
code/branching_locate_db09/.  Every mutation happens in a temp git clone or a
temp scratch tree.
"""

import hashlib
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))

# Revisions, named in full and RESOLVED before use -- a prefix that becomes
# ambiguous later is a claim that rots.
REV_A218 = "286d5030902d09a7eb336a4a5dec18bf7b9de64c"   # reproduction taken here
REV_321D = "ef38841710edf28af76d0accc1c6aaf011ed9490"   # g1 BEFORE mg-7e58
REV_957F = "e006581c2e1185cba3fa58c91a9fd4954bd63eae"   # g1 BEFORE mg-76cc

A218_DIR = "code/branching_audit_a218"
S58DA_DIR = "code/branching_audit_58da"
DB09_DIR = "code/branching_locate_db09"
TARGET_REL = DB09_DIR + "/out_t1_tl.txt"

G1_REL = S58DA_DIR + "/g1_provenance.py"
LIB_REL = S58DA_DIR + "/lib58da.py"
KERN_REL = A218_DIR + "/kern_a218.py"
C1_REL = A218_DIR + "/c1_branching.py"

# The five committed transcripts G-3 is about, in run_all.sh's own order.
FIVE_OUTPUTS = ["out_selftest_58da.txt", "out_g1_provenance.txt",
                "out_g2_redo.txt", "out_g3_findings.txt", "out_g4_fleet.txt"]

# The four scripts that share lib58da.run_c1 with g1 and were NOT edited here.
UNTOUCHED_SCRIPTS = ["selftest_58da.py", "g2_redo.py", "g3_findings.py",
                     "g4_fleet.py"]


# ---------------------------------------------------------------------------
# reporting
# ---------------------------------------------------------------------------

class Report(object):
    """SELF-ERRORS and FINDINGS kept apart, each naming its own population.

    A SELF-ERROR is a fact about THIS instrument -- an anchor it could not
    find, a clone it could not build.  A FINDING is a fact about the thing
    under test.  Folding the first into the second is how an instrument that
    stopped working reads as a clean run.
    """

    def __init__(self, selfpop, findpop):
        self.selfpop, self.findpop = selfpop, findpop
        self.self_, self.find = [], []

    def selferr(self, msg):
        self.self_.append(msg)

    def finding(self, msg):
        self.find.append(msg)

    def check(self, ok, msg):
        """Book `msg` as a SELF-ERROR unless `ok`.  For the instrument's own
        preconditions -- a probe that changed nothing, a clone that did not
        clone."""
        if not ok:
            self.selferr(msg)
        return ok

    def gate(self, ok, msg):
        """Book `msg` as a FINDING unless `ok`.  For the thing under test."""
        if not ok:
            self.finding(msg)
        return ok

    def emit(self):
        print("-" * 74)
        print("SELF-ERRORS: %d, population: %s" % (len(self.self_),
                                                   self.selfpop))
        for m in self.self_:
            print("   SELF-ERROR: " + m)
        print("FINDINGS: %d, population: %s" % (len(self.find), self.findpop))
        for m in self.find:
            print("   FINDING: " + m)
        print("TOTAL BAD: %d" % (len(self.self_) + len(self.find)))
        return 1 if (self.self_ or self.find) else 0


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
    return git("rev-parse", rev, repo=repo).strip()


def head_rev(repo=REPO):
    return resolve("HEAD", repo=repo)


def subject(rev, repo=REPO):
    return git("log", "-1", "--format=%s", rev, repo=repo).strip()


def is_ancestor(a, b, repo=REPO):
    p = subprocess.run(["git", "-C", repo, "merge-base", "--is-ancestor", a, b],
                       capture_output=True, text=True)
    return p.returncode == 0


def distance(a, b, repo=REPO):
    """Commits in a..b, i.e. how stale `a` is relative to `b`."""
    return int(git("rev-list", "--count", "%s..%s" % (a, b),
                   repo=repo).strip())


def last_touching(path, repo=REPO):
    out = git("log", "-1", "--format=%H", "--", path, repo=repo).strip()
    return out or None


def sha(text):
    if isinstance(text, str):
        text = text.encode()
    return hashlib.sha256(text).hexdigest()


def read_worktree(rel, repo=REPO):
    with open(os.path.join(repo, rel)) as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# running
# ---------------------------------------------------------------------------

def run_script(directory, name, repo=REPO, timeout=3600):
    p = subprocess.run(["python3", "-u", name],
                       cwd=os.path.join(repo, directory),
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


def run_c1(target_text, c1_src, kern_src):
    """Run mg-a218's c1_branching.py with the SCRIPT and the KERNEL chosen
    INDEPENDENTLY, against a target text supplied here.

    The two are separate arguments because "the measuring half" is two files.
    An instrument that binds them to one revision -- which is what
    lib58da.run_c1 did until mg-76cc -- cannot ask whether the kernel moved,
    and an instrument that cannot ask cannot find F-1.

    c1 resolves its target as dirname(__file__)/../branching_locate_db09/…, so
    the scratch tree mirrors that two-directory shape and nothing else.
    """
    tmp = tempfile.mkdtemp(prefix="mg76cc-c1-")
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
                           capture_output=True, text=True, timeout=3600)
        return p.stdout + p.stderr, p.returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


C1_SPLIT = "(iii) EVERY CELL, AGAINST"


def measuring_half(out):
    """c1's sections (i)+(ii) -- what it computes BEFORE comparing anything."""
    return out.split(C1_SPLIT)[0]


# ---------------------------------------------------------------------------
# reading what a script printed.  No `re` anywhere in this file.
# ---------------------------------------------------------------------------

def totals_of(out):
    """(SELF-ERRORS, FINDINGS) as the script itself printed them."""
    s = f = None
    for line in out.splitlines():
        for prefix, which in (("SELF-ERRORS: ", "s"), ("FINDINGS: ", "f")):
            if line.startswith(prefix):
                tail = line[len(prefix):]
                digits = ""
                for ch in tail:
                    if ch.isdigit():
                        digits += ch
                    else:
                        break
                if digits:
                    if which == "s":
                        s = int(digits)
                    else:
                        f = int(digits)
    return s, f


def findings_of(out):
    return [line.split("FINDING: ", 1)[1].strip()
            for line in out.splitlines() if "   FINDING: " in line]


def selferrs_of(out):
    return [line.split("SELF-ERROR: ", 1)[1].strip()
            for line in out.splitlines() if "   SELF-ERROR: " in line]


HEXDIGITS = set("0123456789abcdef")


def is_hex(tok):
    return bool(tok) and all(c in HEXDIGITS for c in tok)


def c1_own_vertices(out):
    """(beta, n) -> [(p, dim)] out of c1's section (i), read by partitioning.

    lib58da matches this with one regex per row and lib957f with
    ast.literal_eval; this walks the line with str.partition so that a defect
    in either of theirs cannot be a defect in this one too.  Returns {} rather
    than a partial parse when the form is absent, and every caller treats {}
    as a SELF-ERROR.
    """
    got, cur = {}, None
    for raw in out.splitlines():
        line = raw.strip()
        if line.startswith("beta = ") and line[7:].strip().isdigit():
            cur = int(line[7:].strip())
            continue
        if cur is None or not line.startswith("n="):
            continue
        head, sep, body = line.partition("set {")
        if not sep or not body.rstrip().endswith("}"):
            continue
        n_tok = head.split()[0][2:]
        if not n_tok.isdigit():
            continue
        inner = body.rstrip()[:-1].strip()
        verts = []
        broken = False
        if inner:
            for piece in inner.split(","):
                p_tok, s2, d_tok = piece.strip().partition(":dim ")
                if not s2 or not p_tok.startswith("p=") \
                        or not p_tok[2:].isdigit() or not d_tok.isdigit():
                    broken = True
                    break
                verts.append((int(p_tok[2:]), int(d_tok)))
        if broken:
            continue
        got[(cur, int(n_tok))] = verts
    return got


# ---------------------------------------------------------------------------
# the revision a committed transcript names, and the normalization G-3 needs
# ---------------------------------------------------------------------------

HEAD_MARK = "  HEAD of this branch"
REV_PLACEHOLDER = "<HEAD-REVISION>"
SUBJ_PLACEHOLDER = "<HEAD-SUBJECT>"
SUBJ_WIDTH = 96          # g1 prints subject(rev)[:96]


def recorded_rev(text):
    """The revision a transcript SAYS it was taken at, read out of itself.

    g1 prints `   <sha12>  HEAD of this branch`.  That line is the transcript
    naming its own provenance, and it is the only place any of the five says
    where it was taken.  Returns None if the transcript does not say.
    """
    for raw in text.splitlines():
        line = raw.strip()
        if line.endswith(HEAD_MARK.strip()) and line.endswith("HEAD of this branch"):
            tok = line.split()[0]
            if len(tok) == 12 and is_hex(tok):
                return tok
    return None


def normalize(text, rev, subj):
    """Replace one revision, and the subject line that goes with it, by
    placeholders.  Returns (normalized text, substitutions made).

    THE POPULATION IS NAMED AND IT IS SMALL: the 40-, 12- and 8-character forms
    of one revision, and that revision's subject truncated the way g1 truncates
    it.  Nothing else is touched -- 286d5030 and ed9cde49 are pinned constants
    in these transcripts and MUST still reproduce byte for byte.
    """
    n = 0
    for k in (40, 12, 8):
        n += text.count(rev[:k])
        text = text.replace(rev[:k], REV_PLACEHOLDER)
    if subj:
        n += text.count(subj[:SUBJ_WIDTH])
        text = text.replace(subj[:SUBJ_WIDTH], SUBJ_PLACEHOLDER)
    return text, n


def differing_lines(a, b):
    """[(lineno, a_line, b_line)] with None past the end of the shorter."""
    la, lb = a.splitlines(), b.splitlines()
    out = []
    for i in range(max(len(la), len(lb))):
        x = la[i] if i < len(la) else None
        y = lb[i] if i < len(lb) else None
        if x != y:
            out.append((i + 1, x, y))
    return out


# ---------------------------------------------------------------------------
# clones
# ---------------------------------------------------------------------------

def dirty_paths(repo=REPO):
    """Every changed FILE, not directory: --porcelain collapses an untracked
    directory to a single entry and copying that as a file is an error."""
    out = git("status", "--porcelain", "-z", "--untracked-files=all", repo=repo)
    return [e[3:] for e in out.split("\0") if len(e) > 3]


def clone(mutate=None, message="mg-76cc scratch commit", carry=True,
          empty_extra=False):
    """A real git clone of this worktree, with the working tree COMMITTED.

    Committed, because every question here is a question about a COMMIT: g1
    reads c1 and the kernel with git_show, so a working-tree edit reaches
    nothing and a probe made in the worktree would come back silent for the
    wrong reason.  mg-957f made exactly that mistake and kept it.

    `empty_extra` adds one further empty commit, which is how the G-3
    impossibility is shown rather than argued: the same tree at two different
    revisions.

    Returns (tmpdir, tree); the caller destroys tmpdir.
    """
    tmp = tempfile.mkdtemp(prefix="mg76cc-")
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
    _commit(tree, message)
    if empty_extra:
        _commit(tree, "mg-76cc: one further commit, to move HEAD")
    return tmp, tree


def _commit(tree, message):
    subprocess.run(["git", "-C", tree, "add", "-A"], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", tree, "-c", "user.name=mg-76cc",
                    "-c", "user.email=mg-76cc@local",
                    "commit", "-q", "--allow-empty", "-m", message],
                   check=True, capture_output=True, text=True)


def destroy(tmp):
    shutil.rmtree(tmp, ignore_errors=True)


def install_pinned_g1(tree, rev, name):
    """Put g1_provenance.py AND lib58da.py AS OF `rev` into the clone, under
    names of their own, so that g1_provenance.py itself is never modified.

    The pinned g1 gets exactly ONE edit -- its `import lib58da as L` line is
    repointed at the pinned library -- because a predicate run against a
    LATER library is not the pre-repair predicate.  That single substitution is
    asserted to have happened exactly once.
    """
    libname = "lib58da_at_%s" % rev[:8]
    lib = git_show(rev, LIB_REL)
    src = git_show(rev, G1_REL)
    old = "import lib58da as L"
    if src.count(old) != 1:
        raise ValueError("g1 at %s has %d `%s` lines, not 1"
                         % (rev[:8], src.count(old), old))
    src = src.replace(old, "import %s as L" % libname, 1)
    with open(os.path.join(tree, S58DA_DIR, libname + ".py"), "w") as fh:
        fh.write(lib)
    with open(os.path.join(tree, S58DA_DIR, name), "w") as fh:
        fh.write(src)


# ---------------------------------------------------------------------------
# corruption.  Every probe REFUSES on zero occurrences and on many.
# ---------------------------------------------------------------------------

def replace_once(text, old, new):
    n = text.count(old)
    if n != 1:
        raise ValueError("expected exactly 1 occurrence of %r, found %d"
                         % (old, n))
    return text.replace(old, new, 1)


KERN_VERTICES = ("        return [(p, self.dim_L(p)) for p in self.parts "
                 "if self.dim_L(p) > 0]")
KERN_VERTICES_BENT = ("        return [(p, self.dim_L(p) + 1) for p in "
                      "self.parts if self.dim_L(p) > 0]")

C1_VERTICES = "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()"
C1_VERTICES_BENT = ("        mine_vertices[(beta, n)] = [(p, d + 1) for p, d "
                    "in algebras[(n, beta)].vertices()]")


def bend_kernel(kern_src):
    """A real regression in kern_a218.py -- every simple's dimension off by one.

    kern_a218.py is the file g1's own section (ii) labels "the measuring half",
    and vertices() is where c1's numbers come from.  This is not a hook: it is
    the same shape as mg-7e58's own c1 probe, one file down.
    """
    return replace_once(kern_src, KERN_VERTICES, KERN_VERTICES_BENT)


def bend_c1_measure(c1_src):
    """The same regression in c1_branching.py -- mg-7e58's own probe."""
    return replace_once(c1_src, C1_VERTICES, C1_VERTICES_BENT)


def touch_c1_compare(c1_src):
    """An edit confined to c1's COMPARING half -- mg-58da's own class.  The
    file sha moves and the measurement does not."""
    return c1_src + '\nprint("   [mg-76cc control: comparing half touched]")\n'


def comment_c1(c1_src):
    """A comment appended to c1.  The file sha moves and nothing else does."""
    return c1_src + "\n# mg-76cc control: a comment, and nothing more\n"


# The pre-repair shape of g1's section (v) measurement(), restored verbatim
# from REV_957F.  Putting it back is how the repair's own probe is shown to be
# load-bearing: re-pin the kernel and the kernel probe must go silent again.
MEASUREMENT_REPAIRED = ("    out, _ = L.run_c1(target_text, "
                        "script_source=script_src,\n"
                        "                      kernel_source=kern_src)")
MEASUREMENT_REPINNED = ("    out, _ = L.run_c1(target_text, "
                        "script_rev=L.REV_A218,\n"
                        "                      script_source=script_src)")


def repin_kernel(g1_src):
    """Undo mg-76cc's repair inside measurement() and nothing else.

    This is the F-1 REINTRODUCTION.  If g1's own probes do not go red on it,
    they would not have caught F-1 either, and the repair is a claim rather
    than a gate.
    """
    return replace_once(g1_src, MEASUREMENT_REPAIRED, MEASUREMENT_REPINNED)


# The three units of section (v) that mg-76cc ADDED, each deleted on its own.
# These are exact source spans, not line numbers: a deletion test anchored on a
# line number stops testing the moment the file is edited above it.
HALF_KERNEL_ROW = ('          ("kern_a218.py", "its kernel", old_c1, '
                   'head_kern),\n')
# mg-69d1: the label in this anchor moved from "cancellation" to "conspiracy"
# when mg-e34a's E-1 was repaired.  IT IS AN ANCHOR IN A DIFFERENT FILE, and
# nothing about "fix the reason for the row" said so -- `drop_both_half` would
# have raised `expected exactly 1 occurrence` and r1's whole section would have
# gone red on a repair that changed one word of prose.  Enumerating the KINDS
# of artifact a repair produces is what found it.
HALF_BOTH_ROW = (',\n          ("both together", "conspiracy", head_c1, '
                 'head_kern)]')
PROBE_KERNEL_ROW = (',\n        ("kern @ HEAD with dim L(n,p) off by one", '
                    'head_kern,\n'
                    '         mutate_kernel, "kern", True,\n'
                    '         "the measuring half really moved, in the '
                    'kernel; must fire")]:')


def drop_kernel_half(g1_src):
    """Delete the kern_a218.py row of section (v)'s HALVES -- the finest unit
    that has a finding of its own -- and nothing else."""
    return replace_once(g1_src, HALF_KERNEL_ROW, "")


def drop_both_half(g1_src):
    """Delete the both-together row of section (v)'s HALVES, and nothing
    else."""
    return replace_once(g1_src, HALF_BOTH_ROW, "]")


def drop_kernel_probe(g1_src):
    """Delete the kernel direction probe from section (v)'s PROBES, and
    nothing else."""
    return replace_once(g1_src, PROBE_KERNEL_ROW, "]:")
