"""Shared machinery for the mg-6ef4 audit instrument.

A header, a way to run a checker and get back BOTH its exit code and its
stdout, a way to extract a pinned revision, and a probe context that mutates
the REAL worktree and proves it put it back.

WHY THE REAL WORKTREE.  The same reason mg-5040 gives, and it is still the
right reason: a checker silent because nothing is wrong and a checker silent
because it cannot see are the same bytes on stdout.  Nothing here is inferred
from source.

WHERE THIS DIFFERS FROM `kern5040.Probe`, AND WHY IT HAD TO.
`kern5040.Probe` snapshots BYTES.  Its restore proof is `git status
--porcelain --untracked-files=all` plus the full `git diff`, both compared
against the state at entry.  Neither of those can see a **permission mode**
that is not the executable bit, and `Probe.__enter__` skips a file it cannot
read with a bare `except OSError: pass` -- so a file that is unreadable at
entry is absent from the snapshot, un-restorable, and unmentioned.

This audit has to `chmod 000` a tracked file to ask its central question, so
the first thing it had to ask of the borrowed harness was whether that harness
would have noticed.  It would not; `t4_restore.py` measures exactly that
rather than asserting it.  `Probe6ef4` therefore snapshots `st_mode` beside
the bytes, records the files it could not read BY NAME instead of passing, and
proves the restore FOUR ways: porcelain, full diff, bytes, and modes.

THE PIN IS NOT `HEAD`.  mg-821e anchored two comparisons on HEAD and they
stopped comparing anything the moment its own repair landed (mg-4700, via
`41ac5d4`).  `PRE` below is mg-5040's own pin, reused deliberately: "before"
then means the same thing in both instruments and the two runs can be laid
side by side.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))

# mg-5040's pin: the last commit before mg-5040, which is mg-7e58's.  git
# cannot move it.
PRE = "4372fae"

# The four checkers whose printed extent quantifies over a set enumerated by
# walking.  Same population as `kern5040.CHECKERS`, so the two runs compare.
CHECKERS = [
    ("w3_scope.py", "species_remainder_f8fa", "w3_scope.py"),
    ("s1_extent.py", "species_repair_a4ef", "s1_extent.py"),
    ("e1_extents.py", "species_extent_d633", "e1_extents.py"),
    ("e2_crosssection.py", "species_extent_d633", "e2_crosssection.py"),
]

# The three runners the cross-section check is wired into.
RUNNERS = ["species_repair_a4ef", "species_remainder_f8fa",
           "species_repair_6f61"]

# The tree every plant in T1 goes into.  It is `w3_scope.py`'s ENTIRE extent
# and one of `s1_extent.py`'s four, so one plant is measured by two checkers
# that enumerate independently.
PLANT_TREE = "code/species_7d75"


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

    `-B` so no probe leaves a `__pycache__` behind: these walks now REPORT
    `__pycache__` as a declined entry, so writing one is a real perturbation
    of the thing being measured.
    """
    root = root or REPO
    d = os.path.join(root, "code", directory)
    return sh([sys.executable, "-B", script], cwd=d)


def porcelain(root=None):
    """`--untracked-files=all`, and the flag is the whole point: plain
    `--porcelain` collapses an untracked directory to ONE line, and this
    instrument's own directory is such a directory until it is committed."""
    return git(["status", "--porcelain", "--untracked-files=all"],
               cwd=root)[1].strip()


def full_diff(root=None):
    return git(["diff"], cwd=root)[1]


def tracked_regular(root):
    """Every tracked path under `root` that is a regular file and not a
    symlink, absolute."""
    out = []
    for rel in git(["ls-files"], cwd=root)[1].splitlines():
        p = os.path.join(root, rel)
        if os.path.islink(p) or not os.path.isfile(p):
            continue
        out.append(p)
    return out


class Probe6ef4(object):
    """Plant things in the real worktree, run whatever, put it back, PROVE it.

    Four proofs, and the last two exist because the first two are blind to
    what this audit does:

      porcelain  no tracked file moved and nothing untracked was left
      diff       tracked CONTENT is byte-identical
      bytes      every tracked regular file's bytes match the state at entry
      MODES      every tracked regular file's `st_mode & 0o7777` matches

    `git` records ONE bit of a file's mode.  A probe that leaves a file at
    `000` leaves the first two proofs green, which is measured in
    `t4_restore.py` against `kern5040.Probe` rather than asserted here.

    `unreadable_at_entry` is a LIST, not a `pass`.  A tracked file this
    process cannot read at entry is absent from the byte snapshot and
    therefore un-restorable; that is a fact about the run and it is printed.
    """

    def __init__(self, label, root=None):
        self.label = label
        self.root = root or REPO
        self.made = []
        self.restored = None
        self.why_not = []

    def _pycache(self):
        out = set()
        for dp, dns, _fns in os.walk(os.path.join(self.root, "code")):
            for d in list(dns):
                if d == "__pycache__":
                    out.add(os.path.join(dp, d))
                    dns.remove(d)
        return out

    def __enter__(self):
        self.pycache_at_entry = self._pycache()
        self.base_porcelain = porcelain(self.root)
        self.base_diff = full_diff(self.root)
        self.bytes = {}
        self.modes = {}
        self.unreadable_at_entry = []
        for p in tracked_regular(self.root):
            try:
                self.modes[p] = os.stat(p).st_mode & 0o7777
            except OSError:
                pass
            try:
                with open(p, "rb") as f:
                    self.bytes[p] = f.read()
            except OSError:
                self.unreadable_at_entry.append(
                    os.path.relpath(p, self.root))
        return self

    # -- planting ---------------------------------------------------------

    def path(self, rel):
        return os.path.join(self.root, rel)

    def write(self, rel, text, mode=None):
        """A new or overwritten file, optionally at a named permission mode.

        The PREVIOUS mode is remembered beside the previous bytes.  An earlier
        version put every file back at 0o644 and silently un-executabled three
        `run_all.sh` -- caught by this class's own mode proof, which is the
        one direction a restore checker is worth anything in.  Kept in
        OUTCOMES.md.
        """
        p = self.path(rel)
        prev, prevmode = None, None
        if os.path.exists(p):
            prevmode = os.stat(p).st_mode & 0o7777
            with open(p, "rb") as f:
                prev = f.read()
        with open(p, "wb") as f:
            f.write(text.encode("utf-8") if isinstance(text, str) else text)
        if mode is not None:
            os.chmod(p, mode)
        self.made.append(("write", p, (prev, prevmode)))
        return p

    def chmod_tracked(self, rel, mode):
        """Change the mode of an EXISTING tracked file and remember nothing.

        Deliberately not added to `self.made`: `t4_restore.py` needs a
        perturbation the undo list does not know about, because the question
        there is what the PROOF sees, not what the undo list replays.
        """
        p = self.path(rel)
        os.chmod(p, mode)
        return p

    def symlink_to_file(self, rel, target_text):
        """A symlink whose target IS a regular file, outside the repository.

        Outside on purpose: a target inside the tree is reachable by the
        ordinary walk and the probe would measure the walk finding the real
        path (mg-4700's kept defect 4).
        """
        d = tempfile.mkdtemp(prefix="mg6ef4-")
        t = os.path.join(d, "target.txt")
        with open(t, "w", encoding="utf-8") as f:
            f.write(target_text)
        link = self.path(rel)
        os.symlink(t, link)
        self.made.append(("link", link, d))
        return link

    # -- restoring --------------------------------------------------------

    def __exit__(self, *exc):
        for kind, p, extra in reversed(self.made):
            try:
                if kind == "link":
                    os.unlink(p)
                    shutil.rmtree(extra, ignore_errors=True)
                elif kind == "write":
                    prev, prevmode = extra
                    os.chmod(p, 0o644)
                    if prev is None:
                        os.unlink(p)
                    else:
                        with open(p, "wb") as f:
                            f.write(prev)
                        if prevmode is not None:
                            os.chmod(p, prevmode)
                else:
                    os.unlink(p)
            except OSError as e:
                self.why_not.append("undo %s %s: %s" % (kind, p, e))

        # `__pycache__` DIRECTORIES A RUN LEFT BEHIND.  A probe here EXECUTES
        # `run_all.sh`, and those runners call `python3` without `-B`, so a
        # run writes bytecode directories that were not there at entry.  They
        # are removed only where they were ABSENT at entry, and only under
        # this repository -- an untracked directory is somebody's work until
        # it is shown not to be.
        for d in self._pycache() - self.pycache_at_entry:
            shutil.rmtree(d, ignore_errors=True)

        # modes FIRST -- a file left at 000 cannot have its bytes compared.
        self.mode_bad = []
        for p, m in self.modes.items():
            try:
                now = os.stat(p).st_mode & 0o7777
            except OSError:
                self.mode_bad.append((os.path.relpath(p, self.root), m, None))
                continue
            if now != m:
                os.chmod(p, m)
                self.mode_bad.append((os.path.relpath(p, self.root), m, now))

        self.rewritten = []
        for p, blob in self.bytes.items():
            try:
                cur = None
                if os.path.exists(p):
                    with open(p, "rb") as f:
                        cur = f.read()
                if cur != blob:
                    with open(p, "wb") as f:
                        f.write(blob)
                    self.rewritten.append(os.path.relpath(p, self.root))
            except OSError as e:
                self.why_not.append("rewrite %s: %s" % (p, e))

        now_pc = porcelain(self.root)
        pc = now_pc == self.base_porcelain
        df = full_diff(self.root) == self.base_diff
        if not pc:
            # NAME THE DELTA.  "not restored" with no reason is the failure
            # mode this whole audit is about, in the proof itself.
            was = set(self.base_porcelain.splitlines())
            isnow = set(now_pc.splitlines())
            for ln in sorted(isnow - was)[:6]:
                self.why_not.append("porcelain GAINED: %s" % ln)
            for ln in sorted(was - isnow)[:6]:
                self.why_not.append("porcelain LOST:   %s" % ln)
        if not df:
            self.why_not.append("full diff differs from entry")
        self.restored = pc and df
        return False


def prove(probe):
    """Print the restore proof of one probe.  Called after EVERY probe."""
    print("    RESTORED: %s   (%d tracked file(s) rewritten, %d mode(s) put "
          "back)" % ("yes" if probe.restored else "*** NO ***",
                     len(probe.rewritten), len(probe.mode_bad)))
    for r in probe.rewritten[:6]:
        print("        rewritten: %s" % r)
    for rel, was, now in probe.mode_bad[:6]:
        print("        mode put back: %s  %s -> %s"
              % (rel, oct(was), oct(now) if now is not None else "gone"))
    for w in probe.why_not[:6]:
        print("        %s" % w)
    if probe.unreadable_at_entry:
        print("        UNREADABLE AT ENTRY, so absent from the byte snapshot "
              "and NOT restorable: %s"
              % ", ".join(probe.unreadable_at_entry[:4]))


def extract(rev, dest):
    """`git archive <rev>` into `dest`, which is created.  Returns dest.

    The extraction has no `.git`.  A checker that asks git for its anchor gets
    no answer there and says so in its own output; that is stated wherever a
    number from an extraction is printed.
    """
    os.makedirs(dest, exist_ok=True)
    tar = subprocess.Popen(["git", "-C", REPO, "archive", rev],
                           stdout=subprocess.PIPE)
    untar = subprocess.Popen(["tar", "-x", "-C", dest], stdin=tar.stdout)
    tar.stdout.close()
    untar.communicate()
    if untar.returncode != 0:
        raise RuntimeError("git archive %s failed" % rev)
    return dest


def lift(rel, name):
    """Lift ONE top-level function out of a script WITHOUT executing it.

    mg-5040 kept this as its defect 5: `from s1_extent import walk_residue`
    runs the whole checker.  Parsing has the side benefit that the test reads
    the code that SHIPS rather than a copy of it.

    The module-level CONSTANT assignments are lifted too, and they have to be:
    `walk_residue`'s own default argument is `stated_dirs=STATED_DIR_RULES`,
    so a lift that supplied that value from here would be testing this file's
    idea of the stated directory rule instead of the subject's.  Only
    assignments whose value is a literal are taken -- nothing that could run.
    """
    import ast
    src = open(os.path.join(REPO, rel), encoding="utf-8").read()
    tree = ast.parse(src)
    ns = {"os": os}
    # Only these node kinds may appear in a value that is lifted.  A `Name`
    # is allowed so that `STATED_DIR_RULES = (PYCACHE,)` -- the subject's own
    # spelling -- comes across; `Call`, `Attribute` and everything else are
    # not, so nothing lifted here can run.
    INERT = (ast.Constant, ast.Tuple, ast.List, ast.Set, ast.Dict, ast.Name,
             ast.Load, ast.UnaryOp, ast.USub)
    consts, fn = [], None
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name):
            if all(isinstance(n, INERT) for n in ast.walk(node.value)):
                consts.append(node)
        elif isinstance(node, ast.FunctionDef) and node.name == name:
            fn = node
    if fn is None:
        raise LookupError("%s not found in %s" % (name, rel))
    mod = ast.Module(body=consts + [fn], type_ignores=[])
    exec(compile(mod, rel, "exec"), ns)
    return ns[name]
