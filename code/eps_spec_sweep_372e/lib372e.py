#!/usr/bin/env python3
"""mg-372e's corpus, READ AT ONE COMMIT (`mg-528e`, mg-20ee's condition 2).

Until `mg-528e` all three scripts here read the WORKING TREE: `s1` walked it with
`os.walk(ROOT)`, `s2` and `s3` opened their ledger documents off disk.  So every
figure in the three committed transcripts was a function of *when you ran it*,
and they drifted -- `288` form-hits at the commit that carries them against
`717` today.  `mg-188d` measured that drift and DECLINED to regenerate, for three
reasons, and the third is the one this file answers:

    "Regenerating would overwrite the only dated reading there is, with an
     undated one."

**A pin is not a regeneration.**  The reading below is dated BY CONSTRUCTION --
`AS_OF` is in the transcript, on the second line -- and it is dated to the very
commit the hand classification was made at, so the record `mg-188d` was
protecting is preserved rather than overwritten.  `s1`'s census at `AS_OF`
reproduces the committed per-file count for **50 of the 50 files** the committed
transcript lists, exactly; see the README for the residue and where it comes
from.

WHAT A PIN COSTS HERE, AND IT IS PAID RATHER THAN GLOSSED.  `s2` and `s3` are not
censuses, they are CHECKS, and a check pinned to a commit stops being a check on
the repository you have -- `pinnable.py`'s own `state_relocation_audit_b0ae`
lesson, *"a pin there would not repair the section; it would DELETE THE QUESTION
THE SECTION ASKS"*.  So both keep their live half: the PINNED reading is on
**stdout** and is the committed transcript, and the same check re-run against the
**working tree** rides on **stderr** and on the **exit code**.  That is
`mg-724a`'s recorded/gated split, and it is why `run_all.sh` no longer pipes
through `tee` -- a pipeline's exit status is `tee`'s, so the alarm would be
swallowed by the runner.

THE READ IS ANCHORED AND FULL-TREE, BOTH, AND THAT IS NOT BELT-AND-BRACES FOR ITS
OWN SAKE: `git ls-tree -r` run from a subdirectory lists ONLY that subtree, so an
instrument that `cd`s into its own directory quietly measures itself instead of
the estate (`mg-68ef` lost 1252 files to exactly that and caught it with a hand
table).  `run_all.sh` does `cd` here, so the failure is reachable rather than
hypothetical, and `P58` plants it.
"""

import os
import subprocess

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "..", ".."))

# The commit this sweep's corpus is read at.
#
#   * CONDITION 1: `git merge-base --is-ancestor dafe759 origin/main` is YES.
#   * CONDITION 2: it is the commit that CARRIES all three transcripts and all
#     three scripts -- `mg-372e`'s own landing.  Not its parent: this sweep
#     EDITED the documents it sweeps, so the state it read is the post-edit one,
#     which is this commit's tree and not its parent's.  README AS_OF rule 1
#     ("the newest ancestor that reproduces"), established by measurement.
AS_OF = "dafe759"

# Bigger than this and the original `s1` skipped the file, by `os.path.getsize`.
# Kept character-for-character so the population is the same population; the size
# now comes from `git ls-tree -l`, which is the blob's size at AS_OF rather than
# the working tree's.
MAX_BYTES = 4_000_000


def git(*args):
    """git, ANCHORED AT ROOT.  Never inherits the caller's working directory."""
    got = subprocess.run(["git", "-C", ROOT, *args], capture_output=True)
    if got.returncode != 0:
        raise SystemExit("lib372e: git %s failed: %s"
                         % (" ".join(args),
                            got.stderr.decode("utf-8", "replace").strip()))
    return got.stdout


def blobs(rev=None):
    """[(path, sha, size)] for every blob at `rev`, in git's own sorted order.

    `--full-tree` AND `-C ROOT`: either one alone is enough today and neither is
    enough against the other's failure, and the cost of both is one flag.
    """
    out = []
    for ln in git("ls-tree", "-r", "-l", "--full-tree",
                  rev or AS_OF).decode("utf-8").splitlines():
        meta, path = ln.split("\t", 1)
        _mode, typ, sha, size = meta.split()
        if typ != "blob":
            continue
        out.append((path, sha, int(size) if size != "-" else 0))
    out.sort()
    return out


def corpus(rev=None):
    """Yield (path, lines) for every readable text blob at `rev`.

    ONE `git cat-file --batch` for the whole tree rather than one `git show` per
    file: 3 000 subprocesses is a minute, one is a second, and the ANSWER is the
    same -- checked, because a faster read that changed the answer would be a
    different measurement wearing the same transcript.
    """
    entries = [(p, sha) for p, sha, size in blobs(rev) if size <= MAX_BYTES]
    if not entries:
        return
    proc = subprocess.Popen(["git", "-C", ROOT, "cat-file", "--batch"],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc.stdin.write(("".join(sha + "\n" for _p, sha in entries)).encode())
    proc.stdin.close()
    try:
        for path, _sha in entries:
            header = proc.stdout.readline().split()
            size = int(header[2])
            body = proc.stdout.read(size)
            proc.stdout.read(1)          # the newline git appends
            try:
                yield path, body.decode("utf-8").splitlines()
            except UnicodeDecodeError:
                continue                 # `s1` skipped these too
    finally:
        proc.stdout.close()
        proc.wait()


def read_lines(path, rev=None):
    """One file's lines at `rev`.  Raises SystemExit if it is not in that tree."""
    return git("show", "%s:%s" % (rev or AS_OF, path)).decode("utf-8").splitlines()


def read_worktree(path):
    """One file's lines AS IT STANDS.  The gated half -- never on stdout."""
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read().splitlines()


def exists(path, rev=None):
    got = subprocess.run(["git", "-C", ROOT, "cat-file", "-e",
                          "%s:%s" % (rev or AS_OF, path)], capture_output=True)
    return got.returncode == 0


def banner():
    """The AS_OF block, printed by all three scripts in the same words.

    Deliberately plain `print("literal" + AS_OF)` and not an f-string, so that
    `permuted.py`'s `print_literals` can source a declaration line back to this
    file's SOURCE -- `script` provenance, the strong half, and the reason a
    declaration is not just a list of the lines you wanted excused.
    """
    print("-- corpus, PINNED (mg-528e) --")
    print("   AS_OF : " + AS_OF + "  -- an ancestor of origin/main (condition 1)")
    print("   read  : git ls-tree -r --full-tree + git cat-file, an ordered read")
    print("           of ONE COMMIT.  The working tree is not read for this")
    print("           transcript; the live re-check is on stderr.")
    print()
