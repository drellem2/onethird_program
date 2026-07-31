"""Shared machinery for the mg-5040 repair instrument.

Three things and no more: a header, a way to run a checker and get back BOTH
its exit code and its stdout, and a probe context that mutates the real
worktree and proves it put it back.

WHY THE REAL WORKTREE.  Two of mg-4700's three OPEN items are about a
distinction that is invisible by reading: a checker that is silent because
nothing is wrong and a checker that is silent because it cannot see are the
same bytes on stdout, and a shell block that carries a verdict and one that
moves a message are the same bytes on disk.  Nothing here is inferred from
source.  Structures are planted and runners are executed.

The one exception is stated where it is used: the PRE-REPAIR comparison runs
against a `git archive` extraction of a PINNED revision, because the point of
that comparison is what the code did before this ticket, and the worktree no
longer contains it.  The revision is a constant in this file.  It is not
`HEAD`: mg-821e anchored two comparisons on HEAD and they stopped comparing
anything the moment the repair landed (mg-4700, via mg-821e's own 41ac5d4).
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# THE PINNED PRE-REPAIR REVISION.  The last commit before mg-5040, which is
# mg-7e58's.  git cannot move it.  Every "before" figure in this instrument is
# measured against an extraction of this revision and never against HEAD.
PRE = "4372fae"

# The four checkers whose printed extent quantifies over a set enumerated by
# walking.  (label, directory, script).
CHECKERS = [
    ("w3_scope.py", "species_remainder_f8fa", "w3_scope.py"),
    ("s1_extent.py", "species_repair_a4ef", "s1_extent.py"),
    ("e1_extents.py", "species_extent_d633", "e1_extents.py"),
    ("e2_crosssection.py", "species_extent_d633", "e2_crosssection.py"),
]

# The three runners mg-821e wired the cross-section check into.
RUNNERS = ["species_repair_a4ef", "species_remainder_f8fa",
           "species_repair_6f61"]


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


def run_checker(directory, script, root=None):
    """Run one checker IN ITS OWN DIRECTORY.  (exit code, stdout+stderr).

    `-B` so that no probe leaves a `__pycache__` behind -- which would be a
    real perturbation here, because the walks this instrument measures now
    REPORT `__pycache__` as a declined entry.
    """
    root = root or REPO
    d = os.path.join(root, "code", directory)
    return sh([sys.executable, "-B", script], cwd=d)


def porcelain(root=None):
    # `--untracked-files=all`, and the flag is the whole point.  Plain
    # `--porcelain` COLLAPSES an untracked directory to one line, so a file
    # planted inside a directory git has not seen before changes nothing in
    # the output -- and this instrument's own directory is exactly such a
    # directory until the moment it is committed.  The self-test caught this
    # by asserting the restore proof in the direction that must FAIL: a probe
    # that deliberately leaves a file behind was reported as restored.
    return git(["status", "--porcelain", "--untracked-files=all"],
               cwd=root)[1].strip()


def full_diff(root=None):
    return git(["diff"], cwd=root)[1]


class Probe(object):
    """Plant things in a tree, run whatever, put it back, and PROVE it.

    Restoration is proved two ways, because one of them can be fooled: a
    `git status --porcelain` that is empty says no TRACKED file moved and
    nothing UNTRACKED was left, and the full `git diff` says the tracked
    content is byte-identical.  Both are compared against the state at
    entry, not against "clean" -- this instrument runs in a worktree that
    already carries the repair, so "clean" is not the baseline.
    """

    def __init__(self, label, root=None):
        self.label = label
        self.root = root or REPO
        self.made = []
        self.restored = None

    def __enter__(self):
        self.base_porcelain = porcelain(self.root)
        self.base_diff = full_diff(self.root)
        # EVERY TRACKED FILE THE PROBE COULD REACH, SNAPSHOTTED.
        # A probe here EXECUTES `run_all.sh`, and a runner REGENERATES the
        # committed `out_*.txt` beside it.  So "put back what I wrote" is not
        # enough: the probe's side effects include files it never touched, and
        # the first version of this class proved its own restore had failed
        # while the reason was a transcript a runner rewrote.  Restoring by
        # `git checkout` is not available -- this worktree carries an
        # uncommitted repair and checkout would destroy it -- so the bytes are
        # held in memory and written back.
        self.snapshot = {}
        for rel in git(["ls-files"], cwd=self.root)[1].splitlines():
            p = os.path.join(self.root, rel)
            if not os.path.isfile(p) or os.path.islink(p):
                continue
            try:
                with open(p, "rb") as f:
                    self.snapshot[p] = f.read()
            except OSError:
                pass
        return self

    def path(self, rel):
        return os.path.join(self.root, rel)

    def symlink_dir(self, rel, contents):
        """A symlinked DIRECTORY whose target is OUTSIDE the repository.

        Outside on purpose.  A hidden directory created INSIDE the tree and
        linked to from the same tree is reachable by the ordinary walk, so
        the probe would measure the walk finding the real path and report a
        checker seeing what it cannot see (mg-4700's own kept defect 4).
        """
        target = tempfile.mkdtemp(prefix="mg5040-")
        for name, text in contents.items():
            with open(os.path.join(target, name), "w", encoding="utf-8") as f:
                f.write(text)
        link = self.path(rel)
        os.symlink(target, link)
        self.made.append(("link", link, target))
        return link

    def fifo(self, rel):
        p = self.path(rel)
        os.mkfifo(p)
        self.made.append(("file", p, None))
        return p

    def broken_symlink(self, rel):
        p = self.path(rel)
        os.symlink(os.path.join(tempfile.gettempdir(), "mg5040-nonexistent"),
                   p)
        self.made.append(("file", p, None))
        return p

    def unreadable_dir(self, rel):
        p = self.path(rel)
        os.makedirs(os.path.join(p, "inner"))
        with open(os.path.join(p, "inner", "leak.md"), "w",
                  encoding="utf-8") as f:
            f.write("planted\n")
        os.chmod(p, 0o000)
        self.made.append(("noread", p, None))
        return p

    def write(self, rel, text):
        p = self.path(rel)
        prev = None
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                prev = f.read()
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        self.made.append(("write", p, prev))
        return p

    def __exit__(self, *exc):
        for kind, p, extra in reversed(self.made):
            if kind == "link":
                os.unlink(p)
                shutil.rmtree(extra, ignore_errors=True)
            elif kind == "noread":
                os.chmod(p, 0o755)
                shutil.rmtree(p, ignore_errors=True)
            elif kind == "write":
                if extra is None:
                    os.unlink(p)
                else:
                    with open(p, "w", encoding="utf-8") as f:
                        f.write(extra)
            else:
                os.unlink(p)
        self.rewritten = []
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
            except OSError:
                pass
        self.restored = (porcelain(self.root) == self.base_porcelain
                         and full_diff(self.root) == self.base_diff)
        return False


def extract(rev, dest):
    """`git archive <rev>` into `dest`, which is created.  Returns dest.

    The extraction has no `.git`, which is stated wherever it matters: a
    checker that asks git for its anchor gets no answer there and says so in
    its own output rather than printing a number with nothing behind it.
    """
    os.makedirs(dest, exist_ok=True)
    tar = subprocess.Popen(["git", "-C", REPO, "archive", rev],
                           stdout=subprocess.PIPE)
    untar = subprocess.Popen(["tar", "-x", "-C", dest], stdin=tar.stdout)
    tar.stdout.close()
    untar.communicate()
    if untar.returncode != 0:
        raise RuntimeError("could not extract %s" % rev)
    return dest


def extract_with_git(rev, dest):
    """`git archive <rev>` into `dest`, then make `dest` a git repository whose
    HEAD tree is that revision's.

    mg-6cb9's `a2_crosssection.py` asks `git ls-tree HEAD` for the tree its
    subject shipped in, so a bare `git archive` extraction -- which has no
    `.git` -- cannot run it.  A fresh repository initialised in the extraction
    gives it a HEAD whose tree is byte-for-byte the pinned revision's, without
    touching this repository's git directory at all: no `git worktree add`, no
    shared state, nothing to clean up outside `dest`.
    """
    extract(rev, dest)
    ident = ["-c", "user.name=mg-5040", "-c", "user.email=mg-5040@local"]
    for args in (["init", "-q"], ["add", "-A"],
                 ["commit", "-q", "-m", "pinned extraction of %s" % rev]):
        rc, out = sh(["git", "-C", dest] + ident + args)
        if rc != 0 and args[0] != "commit":
            raise RuntimeError("git %s failed in %s: %s" % (args[0], dest, out))
    return dest


def commit_messages():
    """[(sha, subject, body)] for every commit reachable from the pin.

    From the pin and not from HEAD, so that this census does not grow a row
    every time somebody commits on top of it.  A census that moves under the
    reader is the defect mg-4700's F3 is about.
    """
    rc, out = git(["log", "--format=%H%x1f%s%x1f%B%x1e", PRE])
    if rc != 0:
        return []
    rows = []
    for rec in out.split("\x1e"):
        rec = rec.strip("\n")
        if not rec:
            continue
        parts = rec.split("\x1f")
        if len(parts) >= 3:
            rows.append((parts[0], parts[1], parts[2]))
    return rows
