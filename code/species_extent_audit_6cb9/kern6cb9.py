"""mg-6cb9 kernel -- IN-PLACE mutation with a verified restore.

mg-d633's E3 mutates a `shutil.copytree` sandbox.  That is safe and it is also
LOSSY: the sandbox has no `.git`, so `s1_extent.py`'s controls (a) at
`ebecd89` and (b) at `83ac472` fall into their `git archive` failure branch and
print "git unavailable -- SKIPPED".  Since `s1_extent.py` does `bad += ctl`,
those two controls contribute nothing to any exit code E3 recorded, and E3's
table does not say so.  A probe that measures a checker with two of its four
controls silently disarmed is measuring a different checker.

So this instrument mutates THE REAL WORKTREE and restores it, and proves the
restore rather than asserting it: `git status --porcelain` is captured before
the probe and compared byte-for-byte after.  If it ever differs the run stops.
A probe harness that can leave the tree dirty is worse than no probe harness.
"""

import os
import subprocess
import sys

__all__ = ["hdr", "REPO", "sh", "git_status", "Probe", "run_checker",
           "flat", "norm_toks"]

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))


def hdr(title):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)
    print()


def sh(args, cwd=None):
    p = subprocess.run(args, cwd=cwd or REPO, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git_status():
    """The porcelain status of the worktree, as the restore contract."""
    return sh(["git", "status", "--porcelain"])[1]


def flat(s):
    return " ".join(s.split())


def norm_toks(s):
    return [t for t in flat(s).lower().split() if t]


def run_checker(rel, args=()):
    """Run a checker where it lives, in the real worktree.  (exit, output).

    PYTHONDONTWRITEBYTECODE IS NOT OPTIONAL HERE AND IT COST ME A RESULT.
    A probe that patches a `.py`, runs it, and restores the source leaves a
    `__pycache__/*.pyc` behind.  Python validates that cache on (source mtime
    in WHOLE SECONDS, source size).  `RUN_FRAC = 0.50` -> `RUN_FRAC = 2.00` is
    the same number of bytes, and the restore lands in the same second as the
    write, so the stale bytecode VALIDATES and every later run in the tree
    imports the mutation from a source file that no longer contains it, with
    `git status` clean throughout.  It happened: A3's D5 disarmed
    `kernd633.RUN_FRAC`, and A3d's seam probe then ran against a poisoned
    cache and reported the opposite of the truth.  Kept in OUTCOMES.md.
    """
    path = os.path.join(REPO, rel)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    # mg-6e4f, on mg-20ee.  A HARNESS THAT PLANTS IN THE WORKTREE MUST RUN THE
    # CHECKER AGAINST THE WORKTREE.  `w3_scope.py` is now AS-OF PINNED -- its
    # corpus default is read out of git at a declared commit -- so a probe that
    # writes `code/species_7d75/NOTES` and then runs it is asking a checker
    # about a tree the plant is not in.  MEASURED before this line existed:
    # Q6 and Q7 went `1 1 as predicted` -> `1 0 *** MISSED ***`, w3's row went
    # `INSIDE 2/2 fired` -> `0/2`, Q10 went `extent TRUE here` -> `*** EXTENT
    # WIDER ***`, and A1 TOTAL BAD went 0 -> 2.
    #
    # A1 GOING RED IS THE RIGHT BEHAVIOUR AND IS WHY THIS IS ONE LINE: this
    # harness caught the pin loudly rather than certifying a checker that had
    # stopped reading anything it plants.  The pin publishes an override for
    # exactly this case and it is used here, per checker, with the reason at
    # the site.
    env.update({"w3_scope.py": {"W3_SCOPE_AT": "WORKTREE"}}
               .get(os.path.basename(path), {}))
    p = subprocess.run([sys.executable, "-B", os.path.basename(path)]
                       + list(args),
                       cwd=os.path.dirname(path), capture_output=True,
                       text=True, env=env)
    return p.returncode, p.stdout + p.stderr


def purge_pycache():
    """Remove every __pycache__ under code/.  Belt as well as braces: -B stops
    THIS instrument writing one, and this stops it reading one somebody else
    left."""
    n = 0
    for root, dirs, files in os.walk(os.path.join(REPO, "code")):
        if os.path.basename(root) == "__pycache__":
            for f in files:
                os.unlink(os.path.join(root, f))
            n += 1
    return n


class Probe(object):
    """One mutation, applied and then undone, with the undo verified.

    `edits` is a list of (relative path, callable) where the callable takes the
    current text (or None if the file does not exist) and returns the new text.
    Returning None means "delete this path".  Directories created for a new
    path are removed on the way out.
    """

    def __init__(self, edits):
        self.edits = edits
        self.saved = {}
        self.made_dirs = []

    def __enter__(self):
        for rel, fn in self.edits:
            p = os.path.join(REPO, rel)
            if os.path.exists(p):
                with open(p, encoding="utf-8", errors="surrogateescape") as fh:
                    old = fh.read()
            else:
                old = None
            self.saved[rel] = old
            d = os.path.dirname(p)
            made = []
            while not os.path.isdir(d) and len(d) > len(REPO):
                made.append(d)
                d = os.path.dirname(d)
            for m in reversed(made):
                os.mkdir(m)
                self.made_dirs.append(m)
            new = fn(old)
            if new is None:
                if os.path.exists(p):
                    os.unlink(p)
            else:
                mode = "wb" if isinstance(new, bytes) else "w"
                if isinstance(new, bytes):
                    with open(p, "wb") as fh:
                        fh.write(new)
                else:
                    with open(p, "w", encoding="utf-8",
                              errors="surrogateescape") as fh:
                        fh.write(new)
        return self

    def __exit__(self, *exc):
        for rel, old in self.saved.items():
            p = os.path.join(REPO, rel)
            if old is None:
                if os.path.exists(p):
                    os.unlink(p)
            else:
                with open(p, "w", encoding="utf-8",
                          errors="surrogateescape") as fh:
                    fh.write(old)
        for d in sorted(self.made_dirs, key=len, reverse=True):
            try:
                os.rmdir(d)
            except OSError:
                pass
        # And drop any bytecode cached from the mutated sources.  See the note
        # on run_checker: the mtime-and-size validation cannot tell a restored
        # file from the mutated one it replaced.
        for rel in self.saved:
            if not rel.endswith(".py"):
                continue
            pc = os.path.join(REPO, os.path.dirname(rel), "__pycache__")
            if os.path.isdir(pc):
                for f in os.listdir(pc):
                    try:
                        os.unlink(os.path.join(pc, f))
                    except OSError:
                        pass
        return False


def plant(text_to_add, where="end"):
    """An edit callable that appends a block to a file, creating it if new."""
    def fn(old):
        if old is None:
            return text_to_add
        if where == "end":
            return old.rstrip("\n") + "\n\n" + text_to_add
        return text_to_add + "\n" + old
    return fn


def replace_once(old_s, new_s):
    """An edit callable that replaces the FIRST occurrence, and insists it was
    there.  A mutation that silently did nothing is a probe that measures
    nothing, and this arc has shipped one."""
    def fn(old):
        if old is None or old_s not in old:
            raise AssertionError("mutation target absent: %r" % old_s[:70])
        return old.replace(old_s, new_s, 1)
    return fn
