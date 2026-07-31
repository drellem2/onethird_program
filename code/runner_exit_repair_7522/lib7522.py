"""mg-7522 -- shared instrument for the three open sites of mg-05eb.

Written from scratch rather than imported from `code/runner_exit_c2b3/libc2b3.py`
or `code/runner_exit_audit_05eb/lib05eb.py`.  Two of the three defects being
repaired here are defects OF a parser (a population rule that keyed on a filename,
and a `pipefail` rule that matched one spelling of one option), so a repair that
borrowed either parser could not disagree with it about the thing that was wrong.

WHAT KIND OF ARTIFACT THIS IS, AND THE DEFECT IT MUST BE CHECKED FOR.  This tree
DEFINES POPULATIONS AND ENUMERATES OVER THEM.  Its subjects' defects were (a) a
population defined by NAME rather than by PROPERTY and (b) an enumeration run
against a PINNED revision, which cannot see anything added after the pin.  So the
two properties this file owes are:

  P1  Every population here is defined by a PREDICATE over content, and the
      predicate is named in the docstring of the function that computes it.
      `ls_sh()` is the only file-listing primitive and it takes NO name filter.
  P2  Every call that ENUMERATES defaults to the current world (`ref=None`, which
      reads the worktree / `git ls-files`).  A revision may be passed, but only
      by a caller that is COMPARING, and every such call site says which it is.
      `callers()` carries the rule in its own docstring, because that is the
      function where a census and a comparison meet.

The branch that CANNOT exhibit the pipeline defect, with the reason: every
subprocess helper below takes a LIST argv and never passes `shell=True`, so no
shell parses the command, so there is no pipeline, so `returncode` is the
target's own status.  That is structural, not a promise about how it is called.
`s5_self.py` checks both claims mechanically over this tree's own bytes.
"""

import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

# The revision the sweep pinned its census AND its caller scan to.  Keeping the
# name `PINNED` rather than `REF` is deliberate: every use of it below is either
# a COMPARISON (correct) or is being shown to be a CENSUS (the defect).
PINNED = "bee07a1"
SWEEP = "52aeaf4"          # mg-c2b3, the arc-wide sweep
AUDIT = "682db2c"          # mg-05eb, the audit that found these three sites

# The two runners the sweep's filename-defined population could not contain.
OUTSIDE = ("code/face_geometry_audit_f1b2/run_audit.sh",
           "code/face_geometry_audit_fcf1/run_audit.sh")


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def hdr(t):
    print()
    bar(t)
    print()


def rows(pairs, widths, indent="      "):
    """Print a table, wrapping the LAST column instead of truncating it.

    Truncation is how a reason becomes a decoration.  Every table in this tree
    that carries a `why` column uses this, so no reason is ever cut off at a
    column boundary and silently shortened into something else.
    """
    import textwrap
    for cells in pairs:
        head = "".join("%-*s " % (w, str(c)) for w, c in zip(widths, cells[:-1]))
        pad = " " * (len(head) + len(indent))
        body = textwrap.wrap(str(cells[-1]), 78 - len(pad)) or [""]
        print("%s%s%s" % (indent, head, body[0]))
        for extra in body[1:]:
            print("%s%s" % (pad, extra))


def git(*args, ok=(0,)):
    p = subprocess.run(["git", "-C", REPO, *args], capture_output=True,
                       text=True)
    if p.returncode not in ok:
        raise RuntimeError("git %s -> %d\n%s" % (" ".join(args),
                                                 p.returncode, p.stderr))
    return p.stdout


# ---------------------------------------------------------------------------
# The file population.  BY PROPERTY.
# ---------------------------------------------------------------------------

def ls_sh(ref=None):
    """Every tracked `*.sh`, repo-relative, at `ref` -- or on disk when None.

    POPULATION, NAMED: files whose path ends in `.sh`, at any depth, tracked by
    git.  There is deliberately NO name argument and no `run_all.sh` special
    case: the whole of OPEN 1 is that `run_all.sh` is a naming convention and a
    convention is not a property.  A caller that wants a sub-population filters
    the result by a PREDICATE OVER CONTENT, and every one below does.

    `ref=None` is the default because this is the primitive underneath every
    census here, and a census must see the current world (P2).
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


def sources(paths, ref=None):
    """{path: text} for the paths that exist at `ref`; missing ones are dropped."""
    out = {}
    for p in paths:
        try:
            out[p] = read(p, ref)
        except (RuntimeError, OSError):
            continue
    return out


# ---------------------------------------------------------------------------
# The parser.
# ---------------------------------------------------------------------------

_COMMENT = re.compile(r"^\s*#")


def command_lines(text):
    """[(1-based line number, line)] for lines that are shell COMMANDS.

    Blank lines and lines whose first non-blank character is `#` are not
    commands.  That is the whole rule, and it is why a header comment that
    quotes `| tee` is not a pipeline -- the disagreement the sweep found in the
    ticket's bare grep, re-derived here from this file's own rule.
    """
    return [(i, l) for i, l in enumerate(text.splitlines(), 1)
            if l.strip() and not _COMMENT.match(l)]


_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def unquoted(line):
    """The line with single- and double-quoted spans blanked out.

    A `|` inside quotes is an argument, not a pipe: `grep 'A\\|B' f` is one
    command.  mg-05eb's own no-pipeline self-check was caught by this and the
    rule is inherited as a rule, not as an answer.
    """
    return _QUOTED.sub(lambda m: " " * len(m.group(0)), line)


# `|` that is neither `||` nor `|&`.
_PIPE = re.compile(r"(?<!\|)\|(?!\|)(?!&)")
_TEE = re.compile(r"(?<!\|)\|(?!\|)\s*tee\b")


def pipelines(text):
    """[(line, text)] -- every REAL pipeline of ANY kind on a command line.

    ANY kind, not `| tee`.  `| tee` was the SHAPE the sweep found; `a pipeline
    whose status is consumed` is the PROPERTY, and OPEN 1 is precisely that the
    two are not the same set.  s1 reports both and the difference between them.
    """
    return [(i, l) for i, l in command_lines(text) if _PIPE.search(unquoted(l))]


def tee_pipelines(text):
    """[(line, text)] -- the sweep's shape: a real `| tee` on a command line."""
    return [(i, l) for i, l in command_lines(text) if _TEE.search(unquoted(l))]


def bare_grep_tee(text):
    """The ticket's instrument: `grep '| *tee'` over ALL lines, comments too."""
    pat = re.compile(r"\|\s*tee")
    return [(i, l) for i, l in enumerate(text.splitlines(), 1) if pat.search(l)]


_SET_E = re.compile(r"^\s*set\s+(?:-[a-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b)")


def has_set_e(text):
    return any(_SET_E.match(l) for _i, l in command_lines(text))


# THE FIGURE OF OPEN 2, AT ITS SOURCE.  `libc2b3.PIPEFAIL_RE` was
# `^\s*set\s+-o\s+pipefail`, which matches ONE spelling.  The single runner in
# the arc that sets the option writes `set -euo pipefail`, so the instrument
# re-derived 0 where the ticket said 1 -- and four reader-facing artifacts then
# said "confirmed exactly" about the number the instrument had disagreed with.
# The rule below is "a `set` builtin that mentions the option, however spelled".
PIPEFAIL_RE = re.compile(r"^\s*set\s+[^#]*\bpipefail\b")
# Kept so s3 can reproduce the defect rather than describe it.
PIPEFAIL_RE_OLD = re.compile(r"^\s*set\s+-o\s+pipefail")


def has_pipefail(text, rx=None):
    rx = rx or PIPEFAIL_RE
    return any(rx.match(l) for _i, l in command_lines(text))


def shebang(text):
    first = (text.splitlines() or [""])[0]
    return first if first.startswith("#!") else ""


# ---------------------------------------------------------------------------
# C1 / C2 / C3 -- IS THE STATUS CONSUMED?  The sweep's conjunction, re-derived.
# ---------------------------------------------------------------------------

_GUARD = re.compile(r"\|\|\s*(true\b|:)|\|\|\s*\{|^\s*(if|while|until)\b")


def guarded(line):
    """Does this line's own syntax already stop `set -e` from reading it?

    `cmd || true`, `cmd || { ... }`, and a line that IS an `if`/`while`/`until`
    condition.  A guarded pipeline's status is not consumed by errexit, so it
    is not in the population -- the same conjunction the sweep used, restated
    over pipelines of any shape rather than over the `| tee` shape.

    NOT in this list, deliberately and against the sweep's rule: `VAR=$(...)`.
    POSIX gives a simple command made only of assignments the exit status of
    the last command substitution, so `n=$(false)` DOES abort under `set -e`.
    Calling it guarded would have quietly shrunk the population by a rule that
    is not true of the shell -- which is the same kind of mistake as defining
    the population by a filename, one level down.
    """
    return bool(_GUARD.search(line.strip()))


# The stages of a pipeline, in order.  Splitting on a real `|` in the unquoted
# line: everything but the LAST stage has its status discarded by the shell.
def stages(line):
    """[stage text] for one pipeline line, in order; the last one owns the status."""
    u = unquoted(line)
    cuts = [m.start() for m in _PIPE.finditer(u)]
    out, prev = [], 0
    for c in cuts:
        out.append(line[prev:c])
        prev = c + 1
    out.append(line[prev:])
    return out


def discarded_stages(line):
    """The stages whose exit status the pipeline THROWS AWAY -- all but the last.

    This is the property `| tee` was one SHAPE of.  `python3 x.py | tee out.txt`
    throws away the python status; `echo "$V" | grep -E p` throws away `echo`'s,
    and `echo` has no failure mode, so that pipeline discards nothing that could
    have mattered.  Reading the shape instead of the property is how a sweep
    ends up with a population it cannot state a predicate for.
    """
    return stages(line)[:-1]


# Commands that have no failure mode in the usages found in this arc.  Named
# individually rather than matched loosely, because a too-generous list here
# shrinks the population and shrinking the population is the defect on repair.
_CANNOT_FAIL = ("echo", "printf", "true", ":")


def stage_can_fail(runner_rel, stage, ref=None):
    """(verdict, why) for ONE discarded pipeline stage.

    Three cases, in order:
      1. the stage runs a SCRIPT (`python3 x.py`, `sh y.sh`) -- ask `can_fail`
         of that script, which is the sweep's own C3 rule, unchanged;
      2. the stage is one of the shell builtins that cannot fail as used here;
      3. anything else is an external command that can return non-zero, and is
         counted as able to fail.  The default is the CONSERVATIVE direction:
         an unknown command counts as able to fail, so an unknown does not fall
         out of the population by being unknown.
    """
    inv = invocation(stage)
    if inv:
        v, why = can_fail(runner_rel, inv[1], ref)
        return v, why
    text = unquoted(stage).strip()
    if not text:
        # A line beginning with `|` is the CONTINUATION of a pipeline whose
        # first stage is on an earlier line.  A line-local parser cannot see
        # that stage, so the conservative answer is "can fail" and the reason
        # says why rather than inventing a command name.
        return True, "pipeline continued from the previous line (not line-local)"
    # Strip an assignment prefix (`n=$(git diff ...`) and any subshell opener,
    # so the command NAME is what gets classified and not the variable it is
    # being assigned to.
    text = re.sub(r"^[A-Za-z_]\w*=", "", text)
    text = text.lstrip("$([{ \t")
    head = (text.split() or [""])[0]
    base = os.path.basename(head)
    if base in _CANNOT_FAIL:
        return False, "`%s` has no failure mode as used" % base
    return True, "external command `%s` can return non-zero" % (base or "?")


# C3 -- a DESIGNED failure route, not "could it ever crash".  Three routes are
# recognised and which one it is gets printed: `assert` is the answer for
# several targets here and a rule that only knew `sys.exit` would have called
# them incapable of failing.
_EXIT_RE = re.compile(r"sys\.exit\(\s*(?!0\s*\))|raise\s+SystemExit\("
                      r"\s*(?!0\s*\))|^\s*exit\(\s*(?!0\s*\))", re.M)
_ASSERT_RE = re.compile(r"^\s*assert\s", re.M)
_RAISE_RE = re.compile(r"^\s*raise\s+(?!SystemExit)", re.M)

_INVOKE = re.compile(r"(?:^|[;&|]\s*)\s*(python3?|sh|bash|/bin/sh)\s+"
                     r"(?:-\S+\s+)*([\w./-]+\.(?:py|sh))")


def invocation(line):
    """(interpreter, script) for the first command of a pipeline, or None."""
    m = _INVOKE.search(unquoted(line))
    return (m.group(1), m.group(2)) if m else None


def arguments(line, script):
    """The argv tail that belongs to `script`, stopping at the pipe.

    `; tail -1 out.txt` after a pipeline is a SEPARATE command, and passing it
    as an argument would run the target with spurious argv and still exit 0 --
    which is this defect wearing the instrument's clothes.
    """
    toks = unquoted(line).split()
    if script not in toks:
        return []
    out = []
    for t in toks[toks.index(script) + 1:]:
        if t in ("|", ";", "&&", "||") or t.startswith("|") or t.startswith(">"):
            break
        out.append(t)
    return out


def can_fail(runner_rel, script, ref=None):
    """(verdict, why) -- can this target exit non-zero BY DESIGN?"""
    rel = os.path.normpath(os.path.join(os.path.dirname(runner_rel), script))
    try:
        src = read(rel, ref)
    except (RuntimeError, OSError):
        return None, "not readable at %s" % (ref or "HEAD")
    if script.endswith(".sh"):
        return (has_set_e(src),
                "`set -e`" if has_set_e(src) else "no set -e")
    for rx, name in ((_EXIT_RE, "sys.exit"), (_ASSERT_RE, "assert"),
                     (_RAISE_RE, "raise")):
        m = rx.search(src)
        if m:
            return True, "%s at %s:%d" % (name, os.path.basename(rel),
                                          src[:m.start()].count("\n") + 1)
    return False, "NO designed failure route (only a crash)"


# ---------------------------------------------------------------------------
# C2 -- the caller scan.  THIS IS WHERE OPEN 3 LIVES.
# ---------------------------------------------------------------------------

_EXEC = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh"
                   r"|run_runner\(")
_NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
_READ = re.compile(r"returncode|check\s*=\s*True")
# Any `*.sh` under `code/`, not only `run_all.sh`.  The sweep's caller scan
# matched `([\w./]*?([\w]+)/run_all\.sh)` and additionally EXCLUDED every file
# named `run_all.sh` from being a caller; both are name rules, and both are
# widened here to the property "an executable source that runs a shell script".
_TARGET = re.compile(r"([\w./-]*?([\w-]+)/(\w+\.sh))")


def callers(ref=None):
    """[(file, line, target tree, target script, consumes?, line text)].

    THE RULE THAT OPEN 3 IS ABOUT, stated where both uses meet:

        A PINNED baseline is CORRECT for a COMPARISON and BLIND for a CENSUS.

    This function is a CENSUS -- it answers "what, in the world as it stands,
    reads a runner's exit status".  So `ref` defaults to None (the current
    world) and a census caller must leave it that way.  Passing a revision here
    is legitimate ONLY when the answer is being COMPARED with another revision's
    answer, which is what `s4_unpin.py` does and says it is doing.

    The sweep called the equivalent scan at its pinned `bee07a1`, correctly for
    its byte-comparison and wrongly for this.  `code/species_depth_audit_4700/`
    landed after that pin, executes three affected runners twenty-one times and
    scores them on `rc == 0`, and was therefore invisible to the enumeration --
    not by an error of the rule but by the choice of anchor.
    """
    files = [f for f in _sources_at(ref)
             if f.endswith(".py") or f.endswith(".sh")]
    out = []
    for f in files:
        try:
            src = read(f, ref)
        except (RuntimeError, OSError):
            continue
        lines = src.split("\n")
        for i, line in enumerate(lines, 1):
            m = _TARGET.search(line)
            if not m or not _EXEC.search(line) or _NOT_EXEC.search(line):
                continue
            if "%s" in m.group(1) or m.group(1).startswith("/"):
                continue
            if os.path.normpath(m.group(1)) == os.path.normpath(f):
                continue          # a script naming itself
            window = "\n".join(lines[i - 1:i + 25])
            if f.endswith(".sh"):
                consumes = has_set_e(src) and not guarded(line)
            else:
                consumes = bool(_READ.search(window))
            out.append((f, i, m.group(2), m.group(3), consumes, line.strip()))
    return out


def _sources_at(ref=None):
    if ref is None:
        return sorted(git("ls-files", "--", "*.py", "*.sh").splitlines())
    return sorted(p for p in git("ls-tree", "-r", "--name-only", ref).splitlines()
                  if p.endswith(".py") or p.endswith(".sh"))


# ---------------------------------------------------------------------------
# Running things.  LIST argv, never shell=True -- see the module docstring.
# ---------------------------------------------------------------------------

def run_argv(argv, cwd, timeout=1800, env=None):
    """(exit code or None on timeout, combined output).

    `returncode` is read on EVERY path.  The timeout path returns None, which
    renders as `-`, never as 0: a timeout printed as 0 would be this repair's
    own subject wearing a different hat.
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


def run_sh_text(text, cwd, timeout=1800, env=None, name="_mg7522_arm.sh"):
    """Run runner TEXT from `cwd` without touching the tracked runner's bytes.

    The pre-repair and post-repair arms are both run this way, so neither arm
    edits a tracked file and the worktree comparison in s2 stays meaningful.
    """
    path = os.path.join(cwd, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    try:
        return run_argv(["/bin/sh", name], cwd, timeout=timeout, env=env)
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass


# This tree's own untracked artifacts, excluded from `porcelain()` so that a
# before/after comparison does not report ME as a change.  Named explicitly
# rather than matched loosely.
MINE = ("code/runner_exit_repair_7522",
        "docs/OneThird-RunnerExit-PopulationRepair.md")


def porcelain():
    return "\n".join(l for l in git("status", "--porcelain").splitlines()
                     if not any(m in l for m in MINE))


# ---------------------------------------------------------------------------
# MENTION vs OCCURRENCE.  Three of this tree's own checks failed on their own
# documentation before these existed, which is the same defect this arc keeps
# finding: a probe that searches for a FORM OF WORDS instead of for the thing.
# `command_lines()` is the shell-side version of this distinction; these are
# the Python-side version, and they are STRUCTURAL -- an AST walk cannot
# mistake a docstring for a call, whereas a regex over lines always can.
# ---------------------------------------------------------------------------

def shell_true_sites(path, ref=None):
    """[(line, what)] -- REAL `shell=True` kwargs and `os.system(` calls.

    A grep for `shell=True` matches the sentence "every subprocess here takes a
    LIST argv and never passes `shell=True`", which is the opposite of the
    thing it is looking for.  mg-05eb recorded exactly that defect in its own
    self-test; this walks the AST instead.
    """
    import ast
    try:
        tree = ast.parse(read(path, ref))
    except SyntaxError:
        return [("?", "unparseable")]
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if (kw.arg == "shell" and isinstance(kw.value, ast.Constant)
                    and kw.value.value is True):
                out.append((node.lineno, "shell=True"))
        fn = node.func
        if (isinstance(fn, ast.Attribute) and fn.attr == "system"
                and isinstance(fn.value, ast.Name) and fn.value.id == "os"):
            out.append((node.lineno, "os.system("))
    return out


def function_code(path, name, ref=None):
    """The source of one function with its DOCSTRING removed.

    `ls_sh` must contain no runner-filename literal in its CODE.  Its docstring
    names `run_all.sh` on purpose -- it explains why there is no name rule --
    and a check that could not tell the two apart would force the explanation
    to be deleted to make the check pass.
    """
    import ast
    tree = ast.parse(read(path, ref))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                body = body[1:]
            return "\n".join(ast.unparse(b) for b in body)
    return ""


# A strength marker is a MENTION when it is DELIMITED -- written inside quotes,
# backticks or emphasis, which is how this arc writes a form of words it is
# talking ABOUT.  It is a USE when it is written bare, applied to a figure:
#
#     | setting `pipefail` | 1 | **1** — confirmed exactly |     <- USE
#     the README said "confirmed exactly" about a number that     <- MENTION
#
# This is the same distinction as `a comment quoting | tee is not a pipeline`,
# one level up, and it is the distinction three of this tree's own checks got
# wrong before it existed.  A second signal list catches the cases where the
# line is machinery for detecting the marker rather than prose at all.
# `<- USE` / `<- MENTION` label a line as an ILLUSTRATION of the rule rather
# than an assertion under it -- the two example lines above are exactly that,
# and without this the rule classifies its own worked example as a violation.
# It is listed here, in the open, rather than special-cased at the call site.
_MENTION_SIGNALS = ("re.compile", "ck(", "_STRENGTH", "strength_lines",
                    "MARK =", "STALE =", "STRONG =", "<- USE", "<- MENTION")
_STRENGTH = re.compile(r"confirmed exactly|byte-identical|\bproven\b", re.I)
_DELIM = "\"'`*"


def strength_lines(text):
    """([(line, text, 'MENTION'|'USE')]) for every strength marker in `text`."""
    out = []
    for i, l in enumerate(text.splitlines(), 1):
        for m in _STRENGTH.finditer(l):
            a = l[m.start() - 1] if m.start() else ""
            b = l[m.end()] if m.end() < len(l) else ""
            delimited = a in _DELIM and b in _DELIM
            mention = delimited or any(s in l for s in _MENTION_SIGNALS)
            out.append((i, l.strip(), "MENTION" if mention else "USE"))
    return out
