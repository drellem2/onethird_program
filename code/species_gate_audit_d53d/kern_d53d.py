"""KERNEL for mg-d53d -- an INDEPENDENT audit of the mg-4adb rung repair.

WHAT THIS SHARES WITH THE THING IT MEASURES: nothing but the repository.  It
does not import `kern4adb.py`, does not read mg-4adb's transcripts as a source
for any figure, and does not reuse its planted strike, its sandbox, its
disposition vocabulary or its population.  Where a number of mg-4adb's is
quoted it is re-derived here first and the two are printed side by side.

THE SANDBOX IS A GIT CLONE, NOT A FILE COPY.  Three of the checkers these
runners call reach for `git` -- `s1_extent.py` replays its detector at
`ebecd89` and `83ac472` via `git archive`, and `e2_crosssection.py` anchors its
census with `git rev-parse`.  In a plain `cp -a` sandbox those steps print
"git unavailable -- SKIPPED" and the deletion sweep would then be certifying a
runner with two of its controls silently switched off -- which is this arc's
own defect committed by its auditor.  So every sandbox here is
`git clone --shared`, whose HEAD is this worktree's HEAD, whose `git archive`
resolves, and whose `git status` is clean.  G0c measures that rather than
asserting it: it runs one control that needs git and reports what it printed.

WHAT A SANDBOX STILL IS NOT.  A clone carries only tracked files, so it has no
`__pycache__` anywhere.  Two committed transcripts move on such a tree --
`out_s1_extent.txt`'s `DECLINED, STATED` count and `out_w3_scope.txt`'s
`stated` count -- and PREDICTIONS.md discloses that as an observation (G5a),
made before this file existed.  No verdict moves with them; G0d prints both
numbers so a reader never has to take that on trust.

    python3 code/species_gate_audit_d53d/g1_population.py    (etc.)
"""

import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# mg-6ef4's before-state.  Every new control in this instrument is also run
# here, because a control demonstrated only against the tree that already
# passes it has not been demonstrated at all.
PIN = "77306a7"

# The three runners mg-4adb's population certifies.  Their line counts are
# re-derived in G1a; the numbers in PREDICTIONS.md were counted from the
# source before any probe existed and are scored against that re-derivation.
RUNNERS = ["species_repair_a4ef", "species_remainder_f8fa",
           "species_repair_6f61"]

# The fourth species runner.  Named in no list in mg-6ef4's ticket, in no
# deletion population in this arc, and in mg-4adb's P3h only as evidence that
# the repair does not redden a clean tree.  G5 is the floor item.
FOURTH = "species_7d75"

# The rest of the verdict path.  The runner's exit status is its last
# command's; that last command is `e2_crosssection.py`, which imports
# `kernd633.py`, which computes the finding.  mg-4adb's certificate covers the
# 255 runner lines and none of these 551.
E2 = os.path.join("code", "species_extent_d633", "e2_crosssection.py")
KERN = os.path.join("code", "species_extent_d633", "kernd633.py")

CALL = "python3 ../species_extent_d633/e2_crosssection.py"
SETE = "set -e"
E2_SAYS = "STANDING UN-STRUCK"
E2_TOTAL = "E2 TOTAL BAD:"

# THE PLANT.  Written for this audit, not borrowed: mg-4adb's probe uses an
# "eleventh" sentence and reusing it would make every figure below a joint
# measurement of two instruments.  The restating paragraph must avoid every
# word in `kernd633.NEGATES` -- refut/struck/strikes/misquot/corrected/
# correction/retract/no longer/does not hold and the rest -- or e2 exonerates
# the occurrence and the plant silently fails to arm.  G0b measures that the
# plant arms; it is not assumed anywhere.
CLAIM = ("The seventeenth species of the seventeenth kind arrives in the "
         "seventeenth order at the seventeenth hour on every seventeenth day "
         "of the seventeenth month.")
STRIKE_REL = os.path.join("code", "species_gate_audit_d53d",
                          "probe_strike_d53d.md")
STRIKE_TEXT = ("# planted by mg-d53d's probes and removed by the same probe\n"
               "\n~~%s~~\n\n%s\n" % (CLAIM, CLAIM))

# A step that fails, substituted for a step that passes.  The redirect and any
# `||` guard around the step are left exactly as they were, so what is
# measured is the runner's wiring and not a runner this audit rewrote.
FORCED = ("python3 -c \"import sys; sys.stderr.write('FORCED RED by mg-d53d"
          "\\n'); sys.exit(1)\"")


def hdr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


class Rows(object):
    """A section's findings.  `bad` is what the exit code is built from and
    `missed` counts predictions of PREDICTIONS.md this run did not meet -- the
    two are separate on purpose: a refuted prediction is a RESULT, and a run
    that goes red because its author guessed wrong is an instrument that
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
        """Score one prediction of PREDICTIONS.md.  A miss is printed as a
        miss and does not redden the run."""
        self.scored += 1
        self.missed += (not hit)
        print("  %-6s %s" % (pid, "HELD" if hit else "*** MISSED ***"))
        print("        predicted: %s" % said)
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
TIMEOUT = "TIMED OUT"


def sh(args, cwd=None, env=None, timeout=900):
    """(returncode, stdout+stderr).  Nothing here is piped: a pipeline's exit
    status in POSIX sh is its LAST command's, which is the defect this whole
    arc is about.

    A deletion can leave a script that never returns, and a sweep that hangs
    on one of 806 lines reports nothing about the other 805.  A timeout is
    reported as its own disposition, never silently as a pass."""
    try:
        p = subprocess.run(args, cwd=cwd, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as e:
        got = e.output or b""
        return None, got.decode("utf-8", "replace") + "\n" + TIMEOUT
    return p.returncode, p.stdout.decode("utf-8", "replace")


def run_runner(root, runner, timeout=900):
    return sh(["sh", os.path.join(root, "code", runner, "run_all.sh")],
              timeout=timeout)


def run_e2(root, timeout=180):
    return sh([sys.executable, "e2_crosssection.py"],
              cwd=os.path.join(root, "code", "species_extent_d633"),
              timeout=timeout)


def run_script(root, rel, args=(), timeout=900):
    return sh([sys.executable, os.path.basename(rel)] + list(args),
              cwd=os.path.dirname(os.path.join(root, rel)), timeout=timeout)


def disposition(rc, out):
    """The three-way classification this audit uses, defined once.

    GATE LOST is the class mg-6ef4 found and mg-4adb repaired: the checker
    made its finding and the reader was told nothing.  It is decided on the
    EXIT CODE ALONE, because that is what a reader's `&&` sees -- whether the
    finding was also printed is a separate column and never a mitigation."""
    if rc is None:
        return "TIMED OUT"
    if rc == 0:
        return "GATE LOST"
    return "GATE HELD" if E2_SAYS in out else "DIED BEFORE THE GATE"


# ---------------------------------------------------------------------------
# Sandboxes.  `git clone --shared` -- see the module docstring.
# ---------------------------------------------------------------------------
_TMP = []


def _tmpdir(prefix):
    d = tempfile.mkdtemp(prefix=prefix)
    _TMP.append(d)
    return d


def cleanup():
    for d in _TMP:
        shutil.rmtree(d, ignore_errors=True)
    del _TMP[:]


def clone(rev=None):
    """A sandbox at `rev`, or at this worktree's HEAD.  Never the worktree
    itself: every probe below deletes lines out of files the repository
    tracks, and a probe that can leave the repository changed is not a probe."""
    dest = os.path.join(_tmpdir("d53d_"), "tree")
    rc, out = sh(["git", "clone", "--shared", "--quiet", REPO, dest])
    if rc:
        raise RuntimeError("git clone failed: %s" % out)
    if rev:
        rc, out = sh(["git", "-C", dest, "checkout", "--quiet",
                      "--detach", rev])
        if rc:
            raise RuntimeError("git checkout %s failed: %s" % (rev, out))
    return dest


def clone_copies(n, template=None):
    """`n` sandboxes, cloned once and copied.  `cp -a` preserves mtimes, so
    each copy's index still matches its files and `git status` stays clean;
    the alternates file is an absolute path into this repository and stays
    valid in a copy."""
    tpl = template or clone()
    out = [tpl]
    for _ in range(n - 1):
        dest = os.path.join(_tmpdir("d53d_"), "tree")
        shutil.copytree(tpl, dest, symlinks=True)
        out.append(dest)
    return out


class Pool(object):
    """Sandboxes handed out one per concurrent task.  The work is subprocess
    bound, so threads are enough and nothing has to be picklable.

    Every task gets a WHOLE TREE to itself and puts it back as it found it.
    That is not an optimisation: two deletions sharing a tree would each be
    measuring the other's runner transcripts."""

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

        def work(i, item):
            root = self.q.get()
            try:
                out[i] = fn(root, item)
            except Exception as e:                       # noqa: BLE001
                # A task that raises must not become a silently missing row:
                # this whole audit is about a failure that printed nothing.
                errors.append((item, repr(e)))
            finally:
                self.q.put(root)
            with lock:
                done[0] += 1
                if progress and done[0] % progress == 0:
                    sys.stderr.write("    ... %d/%d\n" % (done[0], len(items)))
                    sys.stderr.flush()

        threads = []
        it = list(enumerate(items))
        pos = [0]

        def loop():
            while True:
                with lock:
                    if pos[0] >= len(it):
                        return
                    i, item = it[pos[0]]
                    pos[0] += 1
                work(i, item)

        for _ in range(min(self.n, len(items))):
            t = threading.Thread(target=loop)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        if errors:
            raise RuntimeError("%d task(s) raised, first: %s %s"
                               % (len(errors), errors[0][0], errors[0][1]))
        return out


# ---------------------------------------------------------------------------
# Mutation
# ---------------------------------------------------------------------------
def read_lines(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read().split("\n")


def write_lines(root, rel, lines):
    with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def source_lines(root, rel):
    """The file's lines as `wc -l` counts them: a trailing newline does not
    make a final empty line.  THE POPULATION IS EVERY ONE OF THESE, with no
    exclusion list -- mg-4adb's rule, applied here to three files mg-4adb's
    population does not contain."""
    lines = read_lines(root, rel)
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return lines


class Deletion(object):
    """One line of one file, deleted, with the file restored afterwards."""

    def __init__(self, root, rel, i):
        self.root, self.rel, self.i = root, rel, i
        self.path = os.path.join(root, rel)

    def __enter__(self):
        with open(self.path, encoding="utf-8") as fh:
            self.orig = fh.read()
        lines = self.orig.split("\n")
        trailing = lines and lines[-1] == ""
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


def plant_strike(root):
    p = os.path.join(root, STRIKE_REL)
    d = os.path.dirname(p)
    if not os.path.isdir(d):
        os.makedirs(d)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(STRIKE_TEXT)
    return p


def unplant_strike(root):
    p = os.path.join(root, STRIKE_REL)
    if os.path.exists(p):
        os.remove(p)


def force_step(root, runner, step_index):
    """Replace the command of the `step_index`-th `python3 ...` step of a
    runner with one that fails, leaving its redirect and guard untouched.
    Returns the line as it was."""
    rel = os.path.join("code", runner, "run_all.sh")
    lines = read_lines(root, rel)
    hits = [i for i, ln in enumerate(lines) if ln.startswith("python3 ")]
    i = hits[step_index]
    was = lines[i]
    rest = was[len("python3 "):]
    # keep everything from the first redirect or guard onward
    cut = len(rest)
    for mark in (" >", ">", " ||", " #"):
        j = rest.find(mark)
        if j != -1:
            cut = min(cut, j)
    lines[i] = FORCED + rest[cut:]
    write_lines(root, rel, lines)
    return rel, i, was


def steps_of(root, runner):
    """The `python3` steps of a runner, in order, as (line number, text)."""
    rel = os.path.join("code", runner, "run_all.sh")
    return [(i + 1, ln) for i, ln in enumerate(read_lines(root, rel))
            if ln.startswith("python3 ")]
