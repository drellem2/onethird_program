"""mg-dee4 -- the independent audit of mg-7522's repair of mg-05eb's three sites.

WRITTEN FROM SCRATCH.  It does not import `lib7522`, `libc2b3` or `lib05eb` for
anything it MEASURES.  The whole subject of this audit is a PREDICATE -- a
population rule that mg-7522 replaced -- and an instrument that borrowed that
predicate could not disagree with it about the thing that might be wrong.

Where a probe deliberately runs MG-7522'S OWN RULE (to run the pre-repair
predicate against the same inputs, or to turn a rule mg-7522 aimed at its
subject back on mg-7522), it imports `lib7522` EXPLICITLY at the call site and
says in the printed output that it is doing so.  Borrowing a rule to check it
is not the same act as borrowing a rule to rely on it, and the two are kept
visibly apart.

WHAT KIND OF ARTIFACT THIS IS.  It defines populations and enumerates over
them, and it ships a `run_all.sh`.  So it can exhibit every defect it audits,
and `selftestdee4.py` checks that on its own bytes.

THE BRANCH THAT CANNOT EXHIBIT THE PIPELINE DEFECT, with the reason: every
subprocess helper below takes a LIST argv and never passes `shell=True`, so no
shell parses the command, so there is no pipeline, so `returncode` is the
target's own status.  That is structural.  `run_argv` reads `returncode` on
every path; the timeout path returns `None`, which renders as `-` and never
as `0`.
"""

import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

# The revision mg-c2b3 pinned.  Named PINNED, not REF, so that every use below
# has to say whether it is a COMPARISON (correct) or a CENSUS (the defect).
PINNED = "bee07a1"
SWEEP = "52aeaf4"           # mg-c2b3, the arc-wide sweep
AUDIT = "682db2c"           # mg-05eb, the audit that opened the three sites
REPAIR = "1ee1f1b"          # mg-7522, the repair under audit
PRE_REPAIR = "1ee1f1b^"     # the tree as it stood immediately before it

TREE = "code/runner_exit_repair_7522"
DOC = "docs/OneThird-RunnerExit-PopulationRepair.md"


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def hdr(t):
    print()
    bar(t)
    print()


def rows(cells, widths, indent="      "):
    """Print a table, WRAPPING the last column rather than truncating it.

    Truncation is how a reason becomes a decoration.
    """
    import textwrap
    for row in cells:
        head = "".join("%-*s " % (w, str(c)) for w, c in zip(widths, row[:-1]))
        pad = " " * (len(head) + len(indent))
        body = textwrap.wrap(str(row[-1]), 78 - len(pad)) or [""]
        print("%s%s%s" % (indent, head, body[0]))
        for extra in body[1:]:
            print("%s%s" % (pad, extra))


def git(*args, ok=(0,)):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                       text=True)
    if p.returncode not in ok:
        raise RuntimeError("git %s -> %d\n%s"
                           % (" ".join(args), p.returncode, p.stderr))
    return p.stdout


# ---------------------------------------------------------------------------
# The file population.  BY PROPERTY -- and the property is stated including the
# part mg-7522's own primitive leaves implicit.
# ---------------------------------------------------------------------------

def ls_tracked(ref=None, suffixes=(".sh",)):
    """Every tracked file at `ref` whose path ends in one of `suffixes`.

    POPULATION, NAMED.  `ref=None` reads the current world (`git ls-files`),
    which is what a CENSUS must do.  A revision may be passed only by a caller
    that is COMPARING, and every such caller below says so.

    `suffixes` is a parameter and not a constant because A1 needs to ask the
    question mg-7522's `ls_sh(ref=None)` cannot: *is `.sh` itself a name rule?*
    A primitive that hard-codes the extension cannot be pointed at `*.py` to
    find out.
    """
    if ref is None:
        out = git("ls-files")
    else:
        out = git("ls-tree", "-r", "--name-only", ref)
    return sorted(p for p in out.splitlines()
                  if any(p.endswith(s) for s in suffixes))


def read(path, ref=None):
    if ref is None:
        with open(os.path.join(REPO, path), "r", encoding="utf-8",
                  errors="replace") as fh:
            return fh.read()
    return git("show", "%s:%s" % (ref, path))


def exists(path, ref=None):
    try:
        read(path, ref)
        return True
    except (RuntimeError, OSError):
        return False


# ---------------------------------------------------------------------------
# The parser.  Independent of lib7522's, and it agrees with it -- A1 says so
# by re-deriving all five of mg-7522's figures rather than by asserting it.
# ---------------------------------------------------------------------------

_COMMENT = re.compile(r"^\s*#")
_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")
_PIPE = re.compile(r"(?<!\|)\|(?!\|)(?!&)")
_TEE = re.compile(r"(?<!\|)\|(?!\|)\s*tee\b")
_SET_E = re.compile(r"^\s*set\s+(?:-[a-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b)")
_GUARD = re.compile(r"\|\|\s*(?:true\b|:)|\|\|\s*\{|^\s*(?:if|while|until)\b")
_CANNOT_FAIL = ("echo", "printf", "true", ":")

_EXIT_RE = re.compile(r"sys\.exit\(\s*(?!0\s*\))|raise\s+SystemExit\("
                      r"\s*(?!0\s*\))|^\s*exit\(\s*(?!0\s*\))", re.M)
_ASSERT_RE = re.compile(r"^\s*assert\s", re.M)
_RAISE_RE = re.compile(r"^\s*raise\s+(?!SystemExit)", re.M)
_INVOKE = re.compile(r"(?:^|[;&|]\s*)\s*(python3?|sh|bash|/bin/sh)\s+"
                     r"(?:-\S+\s+)*([\w./-]+\.(?:py|sh))")


def command_lines(text):
    """[(1-based line, text)] for lines that are shell COMMANDS.

    A blank line is not a command and a line whose first non-blank character is
    `#` is a comment.  That is the whole rule, and it is why a header comment
    quoting `| tee` is not a pipeline.
    """
    return [(i, l) for i, l in enumerate(text.splitlines(), 1)
            if l.strip() and not _COMMENT.match(l)]


def unquoted(line):
    """The line with quoted spans blanked.  A `|` in quotes is an argument."""
    return _QUOTED.sub(lambda m: " " * len(m.group(0)), line)


def pipelines(text):
    """[(line, text)] -- every REAL pipeline of any kind on a command line."""
    return [(i, l) for i, l in command_lines(text) if _PIPE.search(unquoted(l))]


def tee_pipelines(text):
    """[(line, text)] -- the sweep's SHAPE: a real `| tee` on a command line."""
    return [(i, l) for i, l in command_lines(text) if _TEE.search(unquoted(l))]


def has_set_e(text):
    return any(_SET_E.match(l) for _i, l in command_lines(text))


def guarded(line):
    """Does the line's own syntax stop `set -e` reading its status?

    `cmd || true`, `cmd || { ... }`, or a line that IS an `if`/`while`/`until`
    condition.  NOT `VAR=$(...)`: POSIX gives an assignment-only simple command
    the status of its last command substitution, so `n=$(false)` does abort
    under `set -e`.
    """
    return bool(_GUARD.search(line.strip()))


def stages(line):
    """[stage] for one pipeline line, in order.  The LAST one owns the status."""
    u = unquoted(line)
    cuts = [m.start() for m in _PIPE.finditer(u)]
    out, prev = [], 0
    for c in cuts:
        out.append(line[prev:c])
        prev = c + 1
    out.append(line[prev:])
    return out


def discarded_stages(line):
    """Every stage whose status the pipeline throws away -- all but the last."""
    return stages(line)[:-1]


def invocation(line):
    m = _INVOKE.search(unquoted(line))
    return (m.group(1), m.group(2)) if m else None


def can_fail(runner_rel, script, ref=None):
    """(verdict, why) -- can this target exit non-zero BY DESIGN?"""
    rel = os.path.normpath(os.path.join(os.path.dirname(runner_rel), script))
    try:
        src = read(rel, ref)
    except (RuntimeError, OSError):
        return None, "not readable at %s" % (ref or "HEAD")
    if script.endswith(".sh"):
        return (has_set_e(src), "`set -e`" if has_set_e(src) else "no set -e")
    for rx, name in ((_EXIT_RE, "sys.exit"), (_ASSERT_RE, "assert"),
                     (_RAISE_RE, "raise")):
        m = rx.search(src)
        if m:
            return True, "%s at %s:%d" % (name, os.path.basename(rel),
                                          src[:m.start()].count("\n") + 1)
    return False, "no designed failure route (only a crash)"


def stage_can_fail(runner_rel, stage, ref=None):
    """(verdict, why) for ONE discarded stage.  Unknown counts as CAN FAIL."""
    inv = invocation(stage)
    if inv:
        return can_fail(runner_rel, inv[1], ref)
    text = unquoted(stage).strip()
    if not text:
        return True, "pipeline continued from an earlier line (not line-local)"
    text = re.sub(r"^[A-Za-z_]\w*=", "", text).lstrip("$([{ \t")
    head = (text.split() or [""])[0]
    base = os.path.basename(head)
    if base in _CANNOT_FAIL:
        return False, "`%s` has no failure mode as used" % base
    return True, "external command `%s` can return non-zero" % (base or "?")


def p2_pipelines(path, ref=None):
    """[(line, text)] -- mg-7522's P2 over one file, re-derived independently.

    P2 = a pipeline whose status is CONSUMED (`set -e` at file level, and the
    line not self-guarded) AND at least one DISCARDED stage that can fail.
    """
    src = read(path, ref)
    se = has_set_e(src)
    out = []
    for i, line in pipelines(src):
        if not (se and not guarded(line)):
            continue
        if any(stage_can_fail(path, s, ref)[0] for s in discarded_stages(line)):
            out.append((i, line))
    return out


# ---------------------------------------------------------------------------
# Running things.  LIST argv, never shell=True -- see the module docstring.
# ---------------------------------------------------------------------------

def run_argv(argv, cwd, timeout=1800, env=None):
    """(exit code or None on timeout, combined output).

    `returncode` is read on EVERY path.  The timeout path returns None, which
    renders as `-` and never as `0`: a timeout printed as 0 would be this
    audit's own subject wearing a different hat.
    """
    e = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    e.update(env or {})
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, env=e)
    except subprocess.TimeoutExpired as ex:
        return None, ((ex.stdout or b"").decode("utf-8", "replace")
                      + (ex.stderr or b"").decode("utf-8", "replace"))
    return p.returncode, p.stdout + p.stderr


def code_str(c):
    """A rendering in which a timeout is never mistaken for a success."""
    return "-" if c is None else str(c)


def porcelain():
    return git("status", "--porcelain")
