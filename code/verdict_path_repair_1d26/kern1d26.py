"""KERNEL for mg-1d26 -- the verdict path, derived rather than inherited.

WHAT THIS SHARES WITH THE INSTRUMENTS IT ANSWERS: nothing but the repository.
It does not import `kern4adb.py` or `kern_d53d.py`, does not read either
instrument's transcripts as the source of any figure it prints as its own, and
does not reuse either one's planted strike, sandbox, disposition vocabulary or
population.

THE POPULATION IS DERIVED FROM A RULE, NOT COPIED FROM A LIST.  mg-d53d's
finding is that mg-4adb's certified population (255 lines, three runner files)
was NARROWER THAN THE VERDICT PATH (806 lines, five files).  A repair that
copies mg-d53d's five-file list and certifies that reproduces the error one
level up: an inherited boundary is exactly what was wrong.  So `verdict_path()`
below walks OUTWARD FROM THE RUNNER --

    the runner file
      -> the script its LAST COMMAND invokes
        -> the transitive closure of that script's repository-local imports

-- and whatever that rule returns is the population.  If it returns more than
mg-d53d's five files, the hole is wider than mg-d53d's number too, and that is
the finding rather than an embarrassment.

THE SIX ARE NAMED BY CONTENT AND NEVER BY LINE NUMBER.  mg-7522's S3 recorded
what keying a disposition on a line NUMBER costs when the file it refers to is
the file being edited -- and this repair edits both files, so every one of
mg-d53d's six line numbers is already wrong.  `SIX` below carries each line's
own text AND the text of the line after it, and `locate()` refuses to resolve
an entry that does not match exactly once.

THE SANDBOX IS `git clone --shared`, NEVER THE WORKTREE.  Three of the checkers
these runners call reach for `git`; in a plain file copy two of them print
"git unavailable -- SKIPPED" and a deletion sweep would then be certifying a
runner with two of its own controls silently switched off.  mg-d53d recorded
that and it is obeyed here.

THE TREE IS ALREADY RED, AND THE SWEEP NEUTRALISES THAT ON PURPOSE.  At the
commit this instrument was written against, `code/face_geometry_repair_e35b/
README.md` carries a LIVE standing occurrence -- a real cross-section finding
that nobody planted, struck at line 39 and asserted at line 36.  Both mg-4adb's
and mg-d53d's "3 of 3 runners are GREEN on a clean tree" rows are therefore
false of this tree.  A second live finding MASKS deletions: `kernd633.py:127`
measured GATE HELD on the untouched tree not because the gate held but because
an unrelated occurrence was still firing.  So `neutralise()` removes the strike
markers FROM THAT ONE DOCUMENT IN THE SANDBOX, and `P0` proves the sandbox is
then clean before any deletion is made.  The act is stated, the file is named,
and it is never done to the worktree.
"""

import os
import queue
import re
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# The three runners whose exit status carries the e2 cross-section verdict.
RUNNERS = ["species_repair_a4ef", "species_remainder_f8fa",
           "species_repair_6f61"]

E2 = os.path.join("code", "species_extent_d633", "e2_crosssection.py")
KERN = os.path.join("code", "species_extent_d633", "kernd633.py")

# mg-4adb's own transcript.  Read ONLY as the object of a measurement -- the
# certified population's size and extent -- and never as the source of a figure
# this instrument reports as its own.
V1_TRANSCRIPT = os.path.join(REPO, "code", "species_rung_repair_4adb",
                             "out_v1_population.txt")

# THE PRE-REPAIR CONTENT, CARRIED AS CONTENT.  Not a SHA: the refinery rebases
# before merging, so a recorded revision is displaced on `main` and an ancestry
# check gives a FALSE NEGATIVE (mg-c067, mg-a74f).  These two files are
# byte-identical copies of `e2_crosssection.py` and `kernd633.py` as they stood
# before this ticket, committed beside the probes.  P2 writes them into a
# sandbox to obtain the before-state, and `pre_pair()` is the only way it does.
PRE_E2 = os.path.join(HERE, "pre1d26_e2_crosssection.py")
PRE_KERN = os.path.join(HERE, "pre1d26_kernd633.py")

# The unrelated live finding.  Named, not described.
LIVE = os.path.join("code", "face_geometry_repair_e35b", "README.md")

# THE PLANT.  Written for this instrument.  Reusing mg-4adb's "eleventh" or
# mg-d53d's "seventeenth" sentence would make every figure below a joint
# measurement of two instruments.  The restating paragraph must avoid every
# word in `kernd633.NEGATES` or e2 exonerates the occurrence and the plant
# silently fails to arm -- P0 measures that it arms and never assumes it.
CLAIM = ("The nineteenth species of the nineteenth kind arrives in the "
         "nineteenth order at the nineteenth hour on every nineteenth day of "
         "the nineteenth month.")
STRIKE_REL = os.path.join("code", "verdict_path_repair_1d26",
                          "probe_strike_1d26.md")
STRIKE_TEXT = ("# planted by mg-1d26's probes and removed by the same probe\n"
               "\n~~%s~~\n\n%s\n" % (CLAIM, CLAIM))

E2_SAYS = "STANDING UN-STRUCK"

# THE SENTENCES A RED RUN CAN BE ATTRIBUTED TO.  A deletion that changes the
# verdict must not be able to do so WITHOUT PRINTING -- mg-1d26's third
# instruction -- so a red is only `ATTRIBUTED` if the output names which
# control produced it.  Every entry is a string this repository prints.
ATTRIBUTIONS = [
    (E2_SAYS, "the cross-section finding itself"),
    ("FOUND NOTHING TO CHECK", "the empty-population floor (mg-1d26)"),
    ("NO VERDICT WAS DELIVERED", "the dead man's switch (mg-1d26)"),
    ("THE TWO ENUMERATIONS OF THIS POPULATION DISAGREE",
     "the second enumeration of the population (mg-1d26)"),
    ("THE VERDICT AND THE ROWS DISAGREE",
     "the two-witness verdict (mg-1d26)"),
    ("finding(s), expected 1", "one of E2b's controls"),
    ("FIRES,", "one of E2b's controls"),
    ("*** FIRES ***", "one of E2b's controls"),
    ("declined, NOT STATED", "the walk's unstated residue (mg-5040)"),
]

# THE SIX.  mg-d53d's table, carried as CONTENT: (file, the line's own text,
# the text of the line after it).  The third entry is the one that changed
# shape in the repair, and the correspondence is written down rather than
# implied: `sys.exit(1 if bad else 0)` WAS the only line in e2 that could
# deliver a verdict, and `deliver("E2", ...)` IS.  Deleting "the line that
# delivers the verdict" is the same deletion in both trees; only its text
# moved.
SIX_PRE = [
    (E2, "FILES += _f", "DECLINED_STATED += _st"),
    (E2, "bad += len(fires)", "print()"),
    (E2, "sys.exit(1 if bad else 0)", None),
    (KERN, "spans.append((prev, len(text)))", "outside = []"),
    (KERN, "for dp, dns, fns in os.walk(root, onerror=onerror):", "keep = []"),
    (KERN, "else:", "keep.append(d)"),
]
SIX_POST = [
    (E2, "FILES += _f", "DECLINED_STATED += _st"),
    (E2, "bad += len(fires)", "print()"),
    (E2, 'deliver("E2", bad, len(FILES), POPULATION_SAYS)', None),
    (KERN, "spans.append((prev, len(text)))", "outside = []"),
    (KERN, "for dp, dns, fns in os.walk(root, onerror=onerror):", "keep = []"),
    (KERN, "else:", "keep.append(d)"),
]
SIX_LABEL = ["e2  FILES += _f",
             "e2  bad += len(fires)",
             "e2  the line that delivers the verdict",
             "kernd633  spans.append((prev, len(text)))",
             "kernd633  the os.walk header",
             "kernd633  the else: that keeps a subdirectory"]

TIMEOUT_MARK = "TIMED OUT"


def hdr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


class Rows(object):
    """A section's findings and its predictions, kept apart on purpose.

    `bad` builds the exit code.  `missed` counts predictions of PREDICTIONS.md
    this run did not meet, and does NOT redden the run: a refuted prediction is
    a RESULT, and an instrument that goes red because its author guessed wrong
    punishes its own honesty."""

    def __init__(self):
        self.bad = 0
        self.missed = 0
        self.scored = 0

    def row(self, label, ok, detail=""):
        self.bad += (not ok)
        print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
        self._detail(detail)

    def note(self, label, detail=""):
        print("  %s" % label)
        self._detail(detail)

    def predicted(self, pid, said, got, hit, detail=""):
        self.scored += 1
        self.missed += (not hit)
        print("  %-6s %s" % (pid, "HELD" if hit else "*** MISSED ***"))
        print("        predicted: %s" % said)
        print("        measured:  %s" % got)
        self._detail(detail)

    def disclosed(self, pid, said, got, detail=""):
        """A measurement PREDICTIONS.md discloses as already made.  Printed so
        a reader can see the disclosure was true; never scored as a hit."""
        print("  %-6s DISCLOSED (not a prediction, not scored)" % pid)
        print("        disclosed: %s" % said)
        print("        measured:  %s" % got)
        self._detail(detail)

    @staticmethod
    def _detail(detail):
        for ln in str(detail).splitlines():
            if ln:
                print("        %s" % ln)

    def tail(self, name):
        print()
        print("=" * 78)
        print("%s TOTAL BAD: %d" % (name, self.bad))
        print("%s PREDICTIONS SCORED: %d, MISSED: %d"
              % (name, self.scored, self.missed))
        print("=" * 78)


# ---------------------------------------------------------------------------
# Processes
# ---------------------------------------------------------------------------
def sh(args, cwd=None, timeout=1800):
    """(returncode, stdout+stderr).  Nothing is piped: a pipeline's status in
    POSIX sh is its LAST command's, which is the defect this arc is about.

    A deletion can leave a script that never returns.  A timeout is its own
    disposition and is never silently a pass."""
    try:
        p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        got = e.output or b""
        return None, got.decode("utf-8", "replace") + "\n" + TIMEOUT_MARK
    return p.returncode, p.stdout.decode("utf-8", "replace")


def run_e2(root, timeout=300):
    return sh([sys.executable, "-B", "e2_crosssection.py"],
              cwd=os.path.join(root, "code", "species_extent_d633"),
              timeout=timeout)


def run_runner(root, runner, timeout=1800):
    return sh(["sh", os.path.join("code", runner, "run_all.sh")],
              cwd=root, timeout=timeout)


def attribution(out):
    """Which printed sentence, if any, a red run can be attributed to.

    mg-d53d's vocabulary had two red dispositions -- the gate firing, and the
    runner dying before the gate.  That collapses `a DIFFERENT control fired
    and said so` into `died`, and this repair adds five controls whose whole
    purpose is to fire instead of the finding.  So the question asked here is
    not `did e2 speak` but `does the output NAME what produced the red`."""
    for needle, what in ATTRIBUTIONS:
        if needle in out:
            return what
    return None


def disposition(rc, out):
    """The four states a mutated verdict path can leave a reader in.

    GATE LOST              exit 0.  The reader is told success.  Decided on the
                           EXIT CODE ALONE, because that is what a reader's
                           `&&` sees; whether a finding was printed anyway is a
                           separate column and never a mitigation.
    GATE HELD, ATTRIBUTED  non-zero, and the output NAMES the control that
                           produced it.
    GATE HELD, UNATTRIBUTED  non-zero, and nothing in the output says why.  Red
                           and mute -- a traceback, or a checker that stopped.
                           Not a silent green, and not a working control either.
    TIMED OUT              its own row.  Never a pass."""
    if rc is None:
        return "TIMED OUT", None
    if rc == 0:
        return "GATE LOST", None
    what = attribution(out)
    if what:
        return "GATE HELD, ATTRIBUTED", what
    return "GATE HELD, UNATTRIBUTED", None


# ---------------------------------------------------------------------------
# Sandboxes
# ---------------------------------------------------------------------------
_TMP = []


def cleanup():
    for d in _TMP:
        shutil.rmtree(d, ignore_errors=True)
    del _TMP[:]


def clone():
    """A `git clone --shared` of this worktree.  Never the worktree itself:
    every probe here deletes lines out of tracked files."""
    d = tempfile.mkdtemp(prefix="mg1d26_")
    _TMP.append(d)
    dest = os.path.join(d, "tree")
    rc, out = sh(["git", "clone", "--shared", "--quiet", REPO, dest])
    if rc:
        raise RuntimeError("git clone failed: %s" % out)
    # The clone carries committed content.  This instrument is developed and
    # run against the WORKTREE's copies of the two files it repairs, so those
    # two are written in from the worktree: a sweep certifying the committed
    # copy while the repair sits uncommitted beside it would be certifying a
    # file nobody is going to ship.
    for rel in (E2, KERN):
        shutil.copyfile(os.path.join(REPO, rel), os.path.join(dest, rel))
    return dest


def clone_copies(n):
    tpl = clone()
    out = [tpl]
    for _ in range(n - 1):
        d = tempfile.mkdtemp(prefix="mg1d26_")
        _TMP.append(d)
        dest = os.path.join(d, "tree")
        shutil.copytree(tpl, dest, symlinks=True)
        out.append(dest)
    return out


class Pool(object):
    """One whole sandbox per concurrent task.  Not an optimisation: two
    deletions sharing a tree would each be measuring the other's transcripts."""

    def __init__(self, n):
        self.n = n
        self.roots = clone_copies(n)
        self.q = queue.Queue()
        for r in self.roots:
            self.q.put(r)

    def map(self, items, fn, progress=None):
        out = [None] * len(items)
        lock = threading.Lock()
        done = [0]
        errors = []
        it = list(enumerate(items))
        pos = [0]

        def work(i, item):
            root = self.q.get()
            try:
                out[i] = fn(root, item)
            except Exception as e:                        # noqa: BLE001
                # A task that raises must not become a silently missing row.
                errors.append((item, repr(e)))
            finally:
                self.q.put(root)
            with lock:
                done[0] += 1
                if progress and done[0] % progress == 0:
                    sys.stderr.write("    ... %d/%d\n" % (done[0], len(items)))
                    sys.stderr.flush()

        def loop():
            while True:
                with lock:
                    if pos[0] >= len(it):
                        return
                    i, item = it[pos[0]]
                    pos[0] += 1
                work(i, item)

        threads = [threading.Thread(target=loop)
                   for _ in range(min(self.n, len(items)))]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        if errors:
            raise RuntimeError("%d task(s) raised, first: %s %s"
                               % (len(errors), errors[0][0], errors[0][1]))
        return out


# ---------------------------------------------------------------------------
# The tree the sweep runs against
# ---------------------------------------------------------------------------
def plant(root):
    p = os.path.join(root, STRIKE_REL)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(STRIKE_TEXT)
    return p


def unplant(root):
    p = os.path.join(root, STRIKE_REL)
    if os.path.exists(p):
        os.remove(p)


def neutralise(root):
    """Remove the strike markers from the ONE document that carries a live,
    unplanted standing occurrence.  Returns (path, number of `~~` removed).

    This is done in the sandbox and never in the worktree, and it is not a
    repair of that document: it is what makes the sweep's finding attributable
    to the plant.  See the module docstring."""
    p = os.path.join(root, LIVE)
    if not os.path.exists(p):
        return LIVE, 0
    with open(p, encoding="utf-8") as fh:
        t = fh.read()
    n = len(re.findall("~~", t))
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(t.replace("~~", ""))
    return LIVE, n


def pre_pair(root):
    """Write the PRE-REPAIR content of both files into `root`, from the
    committed copies in this directory.  Content, never a revision."""
    shutil.copyfile(PRE_E2, os.path.join(root, E2))
    shutil.copyfile(PRE_KERN, os.path.join(root, KERN))


def post_pair(root):
    """Write the repaired content of both files into `root`."""
    shutil.copyfile(os.path.join(REPO, E2), os.path.join(root, E2))
    shutil.copyfile(os.path.join(REPO, KERN), os.path.join(root, KERN))


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------
def source_lines(root, rel):
    """The file's lines as `wc -l` counts them: a trailing newline does not
    make a final empty line.  THE POPULATION IS EVERY ONE OF THESE."""
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


def locate(root, rel, text, nxt):
    """The 0-based index of the ONE line equal to `text` whose successor is
    `nxt`.  Raises if it is not there exactly once.

    A lookup that silently resolves to the wrong line, or to none, is a probe
    that measures nothing while reporting a row -- which is the shape of
    everything this arc is about."""
    body = source_lines(root, rel)
    hits = [i for i, ln in enumerate(body)
            if ln.strip() == text
            and (nxt is None
                 or (i + 1 < len(body) and body[i + 1].strip() == nxt))]
    if len(hits) != 1:
        raise RuntimeError("%s: %r followed by %r appears %d time(s), "
                           "expected exactly 1" % (rel, text, nxt, len(hits)))
    return hits[0]


class Deletion(object):
    """One line of one file, deleted, and the file put back afterwards."""

    def __init__(self, root, rel, i):
        self.root, self.rel, self.i = root, rel, i
        self.path = os.path.join(root, rel)

    def __enter__(self):
        with open(self.path, encoding="utf-8") as fh:
            self.orig = fh.read()
        lines = self.orig.split("\n")
        trailing = bool(lines) and lines[-1] == ""
        body = lines[:-1] if trailing else lines
        self.text = body[self.i]
        del body[self.i]
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(body) + ("\n" if trailing else ""))
        return self

    def __exit__(self, *exc):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(self.orig)
        return False


# ---------------------------------------------------------------------------
# THE POPULATION, DERIVED
# ---------------------------------------------------------------------------
LAST_COMMAND = re.compile(r"^\s*python3\s+(\S+)")
IMPORTS = re.compile(r"(?m)^\s*(?:from\s+([A-Za-z_][\w.]*)\s+import"
                     r"|import\s+([A-Za-z_][\w.]*))")


def last_command(root, runner):
    """The runner's LAST COMMAND, read out of its source.

    A POSIX script's exit status is its last command's, so this is the line
    that decides what the runner returns.  A COMMENT is not a command and a
    blank line is not a command; nothing else is excluded."""
    rel = os.path.join("code", runner, "run_all.sh")
    body = [ln for ln in source_lines(root, rel)
            if ln.strip() and not ln.lstrip().startswith("#")]
    return rel, (body[-1].strip() if body else "")


def local_imports(root, rel):
    """The repository-local modules `rel` imports, resolved against its own
    directory.  (resolved, unresolved) -- and an unresolved name is RETURNED
    rather than dropped, because a module this rule cannot find is a piece of
    the verdict path it cannot certify."""
    d = os.path.dirname(os.path.join(root, rel))
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        src = fh.read()
    names = []
    for m in IMPORTS.finditer(src):
        names.append((m.group(1) or m.group(2)).split(".")[0])
    resolved, unresolved = [], []
    for n in sorted(set(names)):
        cand = os.path.join(d, n + ".py")
        if os.path.isfile(cand):
            resolved.append(os.path.relpath(cand, root))
        elif n in sys.stdlib_module_names:
            continue
        else:
            unresolved.append(n)
    return sorted(set(resolved)), sorted(set(unresolved))


def verdict_path(root, runner):
    """THE RULE, APPLIED.  (runner_rel, last command, [files], [unresolved]).

    The verdict path of a runner is the runner file, plus the script its last
    command invokes, plus the transitive closure of that script's
    repository-local imports.  Nothing is excluded and nothing is inherited
    from any list."""
    rel, cmd = last_command(root, runner)
    files = [rel]
    unresolved = []
    m = LAST_COMMAND.match(cmd)
    if not m:
        return rel, cmd, files, ["the last command is not a python3 call"]
    d = os.path.dirname(os.path.join(root, rel))
    entry = os.path.relpath(os.path.normpath(os.path.join(d, m.group(1))),
                            root)
    queue_ = [entry]
    seen = set()
    while queue_:
        cur = queue_.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        if not os.path.isfile(os.path.join(root, cur)):
            unresolved.append(cur)
            continue
        files.append(cur)
        res, unres = local_imports(root, cur)
        unresolved += unres
        queue_ += res
    return rel, cmd, files, sorted(set(unresolved))
