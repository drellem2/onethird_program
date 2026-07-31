"""Shared machinery for the mg-4adb repair instrument.

A header, a way to run a runner or a checker and get back BOTH its exit code
and its stdout, and a probe context that mutates the real worktree and proves
it put it back.

WHY THE REAL WORKTREE, AND WHY FROM THE REPOSITORY ROOT.  Every question this
instrument asks is about a SHELL SCRIPT'S EXIT STATUS as a function of its own
lines, and none of it can be answered by reading.  The runners are executed as
`sh code/<tree>/run_all.sh` with the working directory at the repository root,
NOT from inside the runner's own directory: a runner's first act is
`cd "$(dirname "$0")"`, and a probe that has already chdir'd there has made
that line untestable by construction.  mg-5040's and mg-6ef4's wiring probes
both ran from the runner's directory, so `cd` was in their populations and
inert by measurement artefact.  It is in this one and it is not.

THE PIN is the last commit before this ticket.  git cannot move it.  Every
"before" figure is measured against it and never against HEAD -- mg-821e
anchored two comparisons on HEAD and they stopped comparing anything the
moment the repair landed (mg-4700, via 41ac5d4).
"""

import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# The last commit before mg-4adb.  mg-6ef4's F3 was measured against the tree
# at this revision and V1f reproduces it here.
PRE = "77306a7"

# The three runners mg-821e wired the cross-section check into, and the three
# whose fifth rung mg-6ef4 found.
RUNNERS = ["species_repair_a4ef", "species_remainder_f8fa",
           "species_repair_6f61"]

# The gate.  Written as CONTENT and never as a line number: mg-7522's S3
# recorded what keying a disposition on a line NUMBER costs when the file it
# refers to is the file being edited.
CALL = "python3 ../species_extent_d633/e2_crosssection.py"
HEADING = 'echo "cross-section check (mg-821e), its own output, unfiltered:"'
SETE = "set -e"
E2_SAYS = "STANDING UN-STRUCK"

# The document that makes e2 red.  A NEW file in THIS directory, on purpose:
# mg-5040's kept defect 3 was a B1 probe that appended to a document those
# runners' own checkers ALSO read, and 2 of 3 went red without printing
# `STANDING UN-STRUCK` -- a red that proved nothing.  `e2_crosssection.py`
# reads every *.md under code/ and docs/, and no other checker in the three
# runners reads a *.md in this directory.  V1b measures that rather than
# assuming it.
STRIKE_DOC = "code/species_rung_repair_4adb/probe_strike_4adb.md"
CLAIM = ("The eleventh species of the eleventh kind arrives in the eleventh "
         "order at the eleventh hour on every eleventh day of the eleventh "
         "month.")
STRIKE_TEXT = ("# planted by mg-4adb's probes and removed by the same "
               "probe\n\n~~%s~~\n\n%s\n" % (CLAIM, CLAIM))

# A step that FAILS, substituted for a step that passes.  This is how V1e asks
# "if this step goes red, does the runner say so": the command is replaced,
# the redirect and any `||` guard around it are left exactly as they were, so
# what is measured is the runner's wiring and not a rewritten runner.
FORCED = ("python3 -c \"import sys; sys.stderr.write('FORCED RED by mg-4adb "
          "V1e\\n'); sys.exit(1)\"")


def hdr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


def sh(args, cwd=None):
    """(returncode, stdout+stderr)."""
    p = subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def git(args, cwd=None):
    return sh(["git", "-C", cwd or REPO] + args)


def runner_path(rn):
    return os.path.join("code", rn, "run_all.sh")


def read_runner(rn, root=None):
    with open(os.path.join(root or REPO, runner_path(rn)),
              encoding="utf-8") as f:
        return f.read()


def run_runner(rn, root=None):
    """Execute a runner FROM THE REPOSITORY ROOT.  See the module docstring.

    AND CLEAN UP AFTER A MUTANT THAT LOST ITS `cd`.  Running from the root is
    what makes `cd "$(dirname "$0")"` testable, and the cost is that a mutant
    with that line deleted writes its `out_*.txt` AT THE ROOT.  Those files are
    an artefact of the measurement and not a fact about the tree, so they are
    removed here.  Left behind they would be untracked files the probe's own
    restore proof cannot see it created -- a probe that dirties the worktree
    while reporting `restored: True` is the shape of everything this arc has
    been about.
    """
    root = root or REPO
    before = set(glob.glob(os.path.join(root, "out_*.txt")))
    try:
        return sh(["sh", runner_path(rn)], cwd=root)
    finally:
        for p in set(glob.glob(os.path.join(root, "out_*.txt"))) - before:
            try:
                os.unlink(p)
            except OSError:
                pass


def run_checker(directory, script, args=(), root=None):
    """Run one checker IN ITS OWN DIRECTORY.  (exit code, stdout+stderr).

    `-B` so that no probe leaves a `__pycache__` behind: these walks REPORT
    `__pycache__` as a declined entry, so writing one is a real perturbation.
    """
    d = os.path.join(root or REPO, "code", directory)
    return sh([sys.executable, "-B", script] + list(args), cwd=d)


def disposition(rc, names_finding):
    """The three things a mutant runner can be, and they are not the same.

    GATE LOST   exit 0.  The runner reports success.  Whether it printed the
                finding is recorded separately, because printing it WHILE
                exiting 0 is the whole class this ticket is about.
    gate fired  non-zero, and e2's own sentence is in the output, so the red
                is ATTRIBUTABLE to the check and not to the mutation.
    BROKE EARLY non-zero, and e2 never spoke.  The deletion broke the runner
                before the gate.  That is not a silent green and it is not a
                working gate; it is its own row.

    Collapsing the last two is how a red run gets read as a working gate.
    """
    if rc == 0:
        return "GATE LOST"
    return "gate fired" if names_finding else "BROKE EARLY"


def without(text, needle):
    """`text` with the single line equal to `needle` removed.

    Raises if it is not there exactly once.  A deletion test that silently
    deletes nothing is a green run that means nothing (mg-6ef4's selftest
    asserts the same thing about its own helper, and this one is asserted in
    selftest4adb.py in both directions).
    """
    lines = text.splitlines(True)
    hits = [i for i, ln in enumerate(lines) if ln.strip() == needle]
    if len(hits) != 1:
        raise RuntimeError("%r appears %d times, expected 1"
                           % (needle, len(hits)))
    del lines[hits[0]]
    return "".join(lines)


def drop_index(text, i):
    """`text` with line `i` (0-based) removed.  The population's operator."""
    lines = text.splitlines(True)
    if not 0 <= i < len(lines):
        raise IndexError("line %d is not in a %d-line file" % (i, len(lines)))
    del lines[i]
    return "".join(lines)


def steps(text):
    """[(index, line)] for every line that INVOKES a checker.

    The rule is written out because it is a population and populations in this
    arc are stated: a step is a line whose first word is `python3`.  A
    continuation line of a `|| { ... }` guard is not one; a `cat` of a
    transcript is not one -- it is a heading and carries no verdict.
    """
    out = []
    for i, ln in enumerate(text.splitlines()):
        if ln.strip().startswith("python3 "):
            out.append((i, ln))
    return out


def force_step(text, i):
    """`text` with the command on line `i` replaced by one that exits 1,
    leaving the redirect and any guard around it untouched."""
    lines = text.splitlines(True)
    ln = lines[i]
    stripped = ln.lstrip()
    indent = ln[:len(ln) - len(stripped)]
    # `python3 <script> <rest of the line>` -> `<forced> <rest of the line>`
    parts = stripped.split(None, 2)
    rest = parts[2] if len(parts) > 2 else ""
    lines[i] = "%s%s %s\n" % (indent, FORCED, rest.rstrip("\n"))
    return "".join(lines)


def porcelain(root=None):
    # `--untracked-files=all`, and the flag is the whole point: plain
    # `--porcelain` COLLAPSES an untracked directory to one line, so a file
    # planted inside a directory git has not seen before changes nothing in
    # the output (mg-5040).
    return git(["status", "--porcelain", "--untracked-files=all"],
               cwd=root)[1].strip()


def full_diff(root=None):
    return git(["diff"], cwd=root)[1]


class Probe(object):
    """Plant things in the worktree, run whatever, put it back, and PROVE it.

    Restoration is proved two ways because one of them can be fooled: an
    unchanged `git status --porcelain --untracked-files=all` says no tracked
    file moved and nothing untracked was left, and an unchanged full `git
    diff` says the tracked content is byte-identical.  Both are compared
    against the state AT ENTRY and not against "clean" -- this instrument runs
    in a worktree that already carries the repair.

    mg-6ef4's F5, kept as a limitation and not repaired here: this proof
    cannot see a PERMISSION MODE.  A tracked file left at 400 restores to
    `restored=True` with the mode wrong, because git compares content.  V2
    plants an unreadable file and therefore restores the mode explicitly in
    `__exit__` and re-reads it to prove it, rather than trusting this class
    for the one thing it is known not to cover.
    """

    def __init__(self, label, root=None):
        self.label = label
        self.root = root or REPO
        self.made = []
        self.restored = None
        self.modes = {}

    def __enter__(self):
        self.base_porcelain = porcelain(self.root)
        self.base_diff = full_diff(self.root)
        # EVERY TRACKED FILE, SNAPSHOTTED, with its MODE.  A probe here
        # EXECUTES `run_all.sh`, and a runner REGENERATES the committed
        # `out_*.txt` beside it -- so "put back what I wrote" is not enough:
        # the side effects include files the probe never touched.
        self.snapshot = {}
        for rel in git(["ls-files"], cwd=self.root)[1].splitlines():
            p = os.path.join(self.root, rel)
            if not os.path.isfile(p) or os.path.islink(p):
                continue
            try:
                with open(p, "rb") as f:
                    self.snapshot[p] = f.read()
                self.modes[p] = os.stat(p).st_mode & 0o7777
            except OSError:
                # mg-6ef4's F5 again: a tracked file unreadable AT ENTRY is
                # absent from the snapshot and no field said so.  It says so
                # now.
                self.unreadable_at_entry = getattr(
                    self, "unreadable_at_entry", [])
                self.unreadable_at_entry.append(os.path.relpath(p, self.root))
        return self

    def path(self, rel):
        return os.path.join(self.root, rel)

    def write(self, rel, text, mode=None):
        p = self.path(rel)
        prev = None
        prev_mode = None
        if os.path.exists(p):
            prev_mode = os.stat(p).st_mode & 0o7777
            with open(p, "rb") as f:
                prev = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        if mode is not None:
            os.chmod(p, mode)
        self.made.append(("write", p, (prev, prev_mode)))
        return p

    def write_bytes(self, rel, blob, mode=None):
        p = self.path(rel)
        prev = None
        prev_mode = None
        if os.path.exists(p):
            prev_mode = os.stat(p).st_mode & 0o7777
            with open(p, "rb") as f:
                prev = f.read()
        with open(p, "wb") as f:
            f.write(blob)
        if mode is not None:
            os.chmod(p, mode)
        self.made.append(("write", p, (prev, prev_mode)))
        return p

    def __exit__(self, *exc):
        for kind, p, extra in reversed(self.made):
            if kind == "write":
                prev, prev_mode = extra
                # Restore the MODE FIRST.  A file left at 000 cannot be
                # rewritten, and the failure would arrive as an OSError inside
                # the restore rather than as a report.
                try:
                    os.chmod(p, 0o644)
                except OSError:
                    pass
                if prev is None:
                    os.unlink(p)
                else:
                    with open(p, "wb") as f:
                        f.write(prev)
                    if prev_mode is not None:
                        os.chmod(p, prev_mode)
            else:
                os.unlink(p)
        self.rewritten = []
        self.modes_rewritten = []
        for p, blob in self.snapshot.items():
            try:
                if not os.path.exists(p):
                    cur = None
                else:
                    with open(p, "rb") as f:
                        cur = f.read()
                if cur != blob:
                    with open(p, "wb") as f:
                        f.write(blob)
                    self.rewritten.append(os.path.relpath(p, self.root))
                if os.path.exists(p) \
                        and (os.stat(p).st_mode & 0o7777) != self.modes[p]:
                    os.chmod(p, self.modes[p])
                    self.modes_rewritten.append(os.path.relpath(p, self.root))
            except OSError:
                pass
        self.restored = (porcelain(self.root) == self.base_porcelain
                         and full_diff(self.root) == self.base_diff)
        return False


def prove(pr):
    """Print a probe's restore proof.  MODE IS PART OF IT (mg-6ef4 F5)."""
    print("      restored: %s   (files rewritten: %d, modes rewritten: %d)"
          % (pr.restored, len(getattr(pr, "rewritten", [])),
             len(getattr(pr, "modes_rewritten", []))))
    if not pr.restored:
        print("      *** THE WORKTREE WAS NOT RESTORED -- every figure after")
        print("          this line was measured against a tree this probe")
        print("          left modified.  `git status` before reading on. ***")


def extract(rev, dest):
    """`git archive <rev>` into `dest`, which is created.  Returns dest."""
    os.makedirs(dest, exist_ok=True)
    tar = subprocess.Popen(["git", "-C", REPO, "archive", rev],
                           stdout=subprocess.PIPE)
    untar = subprocess.Popen(["tar", "-x", "-C", dest], stdin=tar.stdout)
    tar.stdout.close()
    untar.communicate()
    if untar.returncode != 0:
        raise RuntimeError("could not extract %s" % rev)
    return dest


def show(rev, rel):
    """One file's content at a revision."""
    rc, out = git(["show", "%s:%s" % (rev, rel)])
    if rc != 0:
        raise RuntimeError("git show %s:%s failed: %s" % (rev, rel, out))
    return out


def cleanup(path):
    shutil.rmtree(path, ignore_errors=True)
