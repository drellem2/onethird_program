"""mg-05eb -- shared instrument for the independent audit of the `| tee` sweep.

Written from scratch rather than imported from `code/runner_exit_c2b3/libc2b3.py`.
An audit that borrows the parser it is auditing cannot disagree with it about what
a pipeline is, and disagreeing about that is half of what this audit is for.

THE GENERAL FORM, ON THIS FILE.  The defect under audit is `a status thrown away
by a pipeline`.  Every subprocess helper here takes a LIST argv and never passes
`shell=True`, so there is no shell, so there is no pipeline, so `returncode` is
the target's own status.  That is the branch that CANNOT exhibit the defect and
the reason is structural, not a promise about how it is called.  The one place a
shell is unavoidable -- running a `run_all.sh` -- runs `/bin/sh <path>` as argv[0]
and argv[1], which is still not a pipeline.
"""

import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

# The revision the sweep pinned its census and its caller scan to.
PINNED = "bee07a1"
# The sweep's own commit.
SWEEP = "52aeaf4"


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def hdr(t):
    print()
    bar(t)
    print()


def git(*args, ok=(0,)):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                       text=True)
    if p.returncode not in ok:
        raise RuntimeError("git %s -> %d\n%s" % (" ".join(args),
                                                 p.returncode, p.stderr))
    return p.stdout


def ls_sh(ref=None):
    """Every `*.sh` tracked at `ref` (or on disk when ref is None), repo-relative.

    POPULATION, NAMED: files whose path ends in `.sh`, anywhere under the
    repository, at any depth, tracked by git.  NOT restricted to `run_all.sh`
    -- that restriction is the hole this audit is testing for.
    """
    if ref is None:
        out = git("ls-files", "--", "*.sh")
    else:
        out = git("ls-tree", "-r", "--name-only", ref)
    return sorted(p for p in out.splitlines() if p.endswith(".sh"))


def read(path, ref=None):
    if ref is None:
        with open(os.path.join(REPO, path), "r", encoding="utf-8",
                  errors="replace") as fh:
            return fh.read()
    return git("show", "%s:%s" % (ref, path))


# ---------------------------------------------------------------------------
# The parser.
# ---------------------------------------------------------------------------

_COMMENT = re.compile(r"^\s*#")


def command_lines(text):
    """[(1-based line number, line)] for lines that are shell COMMANDS.

    A line is not a command when it is blank or when its first non-blank
    character is `#`.  That is deliberately the *whole* rule and it is stated
    rather than buried: it is why a header comment containing the words
    `| tee` is not counted, which is the six-runner disagreement the sweep
    found in the ticket's bare grep -- and this instrument reproduces that
    disagreement from its own rule rather than inheriting the answer.
    """
    out = []
    for i, l in enumerate(text.splitlines(), 1):
        if not l.strip() or _COMMENT.match(l):
            continue
        out.append((i, l))
    return out


_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def unquoted(line):
    """The line with single- and double-quoted spans blanked out.

    A `|` inside quotes is an argument, not a pipe -- `grep -h 'A\|B' f` is one
    command.  This is the same distinction as `a comment mentioning | tee is
    not a pipeline`, one level down, and it is here because S6 caught this
    instrument's own runner with it: the headline `grep` at the end of
    `run_all.sh` carries a `\|` alternation inside single quotes and the first
    draft of the check called it a pipeline.
    """
    return _QUOTED.sub(lambda m: " " * len(m.group(0)), line)


# `|` that is not `||` and not `|&`, followed by optional space and `tee`.
_TEE = re.compile(r"(?<!\|)\|(?!\|)\s*tee\b")
_PIPE = re.compile(r"(?<!\|)\|(?!\|)")


def tee_pipelines(text):
    """[(line number, line)] -- every REAL `| tee` pipeline on a command line."""
    return [(i, l) for i, l in command_lines(text) if _TEE.search(unquoted(l))]


def any_pipelines(text):
    """[(line number, line)] -- every pipeline of ANY kind on a command line."""
    return [(i, l) for i, l in command_lines(text) if _PIPE.search(unquoted(l))]


def bare_grep_tee(text):
    """The ticket's instrument: `grep '| *tee'`, over ALL lines, comments too."""
    pat = re.compile(r"\|\s*tee")
    return [(i, l) for i, l in enumerate(text.splitlines(), 1) if pat.search(l)]


def has_set_e(text):
    return any(re.match(r"^\s*set\s+(-[a-zA-Z]*e|-o\s+errexit)", l)
               for _i, l in command_lines(text))


def has_pipefail(text):
    return any("pipefail" in l for _i, l in command_lines(text))


def redirect_guard_sites(text):
    """[(line number, target, has_cat_in_guard)] for the repair's own idiom.

    The idiom is `CMD > FILE || { ... exit 1; }`, possibly with the guard body
    on the following line.  `has_cat_in_guard` records whether the guard body
    prints the transcript -- see J4c.
    """
    lines = text.splitlines()
    out = []
    for i, l in enumerate(lines, 1):
        if _COMMENT.match(l) or not l.strip():
            continue
        m = re.search(r">\s*(\S+\.txt)\s*\|\|\s*\{(.*)$", l)
        if not m:
            continue
        body = m.group(2)
        j = i
        while "}" not in body and j < len(lines):
            body += "\n" + lines[j]
            j += 1
        out.append((i, m.group(1), bool(re.search(r"\bcat\b", body))))
    return out


# ---------------------------------------------------------------------------
# Running things.  List argv, never shell=True.
# ---------------------------------------------------------------------------

def run_sh(path, timeout=1800, cwd=None, env=None):
    """(exit code or None on timeout, stdout+stderr) for one shell script."""
    d = cwd or os.path.dirname(os.path.join(REPO, path))
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    e.update(env or {})
    try:
        p = subprocess.run(["/bin/sh", os.path.basename(path)], cwd=d,
                           capture_output=True, text=True, timeout=timeout,
                           env=e)
    except subprocess.TimeoutExpired as e:
        return None, (e.stdout or b"").decode("utf-8", "replace") \
            + (e.stderr or b"").decode("utf-8", "replace")
    return p.returncode, p.stdout + p.stderr


# This audit's own untracked artifacts.  Excluded from `porcelain()` because
# they are untracked while being written and would otherwise make every
# before/after comparison report a difference that is me.  Named explicitly
# rather than matched loosely: J3's first run reported the worktree DIRTY on
# account of this audit's own document, which is a false positive of exactly
# the kind these comparisons exist to catch.
MINE = ("code/runner_exit_audit_05eb",
        "docs/OneThird-RunnerExit-ArcWideSweep-IndependentAudit.md")


def porcelain():
    """`git status --porcelain`, with this audit's own artifacts excluded."""
    return "\n".join(l for l in git("status", "--porcelain").splitlines()
                     if not any(m in l for m in MINE))


def restore_tracked():
    """Put every tracked file back.  Untracked files are NOT removed -- this
    audit's own tree is untracked and removing it would delete the instrument."""
    git("checkout", "--", ".")


class Sandbox:
    """Edit tracked files, then put them back -- even if the body raises."""

    def __init__(self):
        self.touched = []

    def __enter__(self):
        return self

    def write(self, rel, text):
        self.touched.append(rel)
        with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
            fh.write(text)

    def append(self, rel, text):
        self.touched.append(rel)
        with open(os.path.join(REPO, rel), "a", encoding="utf-8") as fh:
            fh.write(text)

    def __exit__(self, *a):
        restore_tracked()
        return False
