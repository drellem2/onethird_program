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

_ASSIGN = re.compile(r"^\s*(?:local\s+|export\s+)?([A-Za-z_]\w*)=\$\(")


def captured_var(line):
    """The variable this line captures a command substitution's OUTPUT into.

    `n=$(git diff … | wc -c | tr -d ' ')` captures into `n`.  mg-70c7/F6: this
    is the arm the WRITTEN REASON for pulling those three lines in was about --
    *"a `git diff` that failed produced an empty stream, `wc -c` reported 0,
    and the proof read `-> 0 bytes`"* -- which is a claim about the VALUE and
    needs no errexit at all.
    """
    m = _ASSIGN.match(line)
    return m.group(1) if m else None


def var_reads(text, var, exclude_line):
    """[(line, text)] where `$var` is READ, excluding the assignment itself.

    A capture that nobody reads discards nothing that mattered, so the value
    arm is a CONJUNCTION -- captured AND read.  Making it captured-only would
    widen the population by a rule that is not about the defect, which is the
    mirror image of narrowing it by a filename.
    """
    rx = re.compile(r"\$\{%s\b[^}]*\}|\$%s\b" % (re.escape(var),
                                                 re.escape(var)))
    return [(i, l.strip()) for i, l in enumerate(text.splitlines(), 1)
            if i != exclude_line and not l.strip().startswith("#")
            and rx.search(l)]


def consumed(text, line, lineno):
    """(verdict, arm, why) -- is this pipeline's status CONSUMED?

    THE CLAUSE mg-70c7 REPAIRED, and the reason it is a disjunction.  mg-dee4's
    F6: this test used to be `has_set_e(text) and not guarded(line)` -- errexit
    alone, at FILE grain -- while the reason written for the three `git diff`
    lines was about the value.  The two agree on those three lines only because
    both of those files happen to set `-e`, so the difference was invisible in
    the population that produced it.  They come apart at
    `code/branching_audit_a218/c0_repro.sh:47`, which sets `-u` and not `-e`,
    whose discarded `grep` and `tr` can fail, whose value drives `BAD`, and
    whose `BAD` drives `exit 1` read by nine sites in three files.

    TWO NAMED ARMS, and the arm is printed with every row so a reader can
    disagree with one of them without discarding the other:

      ERREXIT  the shell itself reads the pipeline's status -- `set -e` in the
               file and no guard on the line.
      VALUE    the pipeline's OUTPUT is captured into a variable that is read
               elsewhere in the file, so a discarded stage that fails changes
               the value the script goes on to use.

    A pipeline is in the population when EITHER holds.  Both arms are true of
    all three `git diff` lines, which is why mg-7522's own three do not move.
    """
    errexit = has_set_e(text) and not guarded(line)
    var = captured_var(line)
    reads = var_reads(text, var, lineno) if var else []
    value = bool(var) and bool(reads)
    if errexit and value:
        return True, "ERREXIT+VALUE", "`set -e`, and `$%s` is read at %d site(s)" % (
            var, len(reads))
    if errexit:
        return True, "ERREXIT", "`set -e` and no guard on the line"
    if value:
        return True, "VALUE", "captured into `%s`, read at %d site(s): %s" % (
            var, len(reads), ", ".join(str(i) for i, _ in reads[:4]))
    if var:
        return False, "-", "captured into `%s` and never read" % var
    return False, "-", "no `set -e`, and the output is not captured"


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
                    "MARK =", "MARK_OLD", "STALE =", "STRONG =",
                    "<- USE", "<- MENTION")

# ONE RULE, POINTED IN BOTH DIRECTIONS.  mg-dee4's F3: `s3_figure.MARK` -- the
# rule this tree pointed at ITS SUBJECT -- had nine alternatives, and the rule
# it pointed at ITSELF had three; `verified` was named as one of the three
# markers in the D4 docstring, in the README and in the published document and
# was in neither of the three.  A stricter test for them and a looser one for
# me is not a stricter standard applied leniently, it is a DIFFERENT
# INSTRUMENT, and it cannot find what theirs finds.  So there is now exactly
# one marker rule in this tree; `s3_figure` imports it and `s5_self` imports
# it, and a marker added for one is added for both by construction.
MARK = re.compile(r"confirmed exactly|byte-identical|byte for byte|\bverified\b"
                  r"|\(measured\)|\bidentical\b|\bconfirmed\b"
                  r"|\ball (?:\d+|of)\b|\bexactly \d+\b", re.I)
# Kept so S5 can exhibit the disagreement rather than describe it: the old
# self-facing rule, three alternatives, run on the same bytes beside the new.
MARK_OLD = re.compile(r"confirmed exactly|byte-identical|\bproven\b", re.I)
_DELIM = "\"'`*"


def alternatives(pattern):
    """How many top-level `|` alternatives a regex source has.

    Counted at depth 0 on the pattern SOURCE, so a `(?:a|b)` inside one
    alternative is not counted twice.  `9 against 3` is the shortest true
    statement of F3 and it is measured here rather than written down.
    """
    src = pattern.pattern if hasattr(pattern, "pattern") else pattern
    depth, n, i = 0, 1, 0
    while i < len(src):
        c = src[i]
        if c == "\\":
            i += 2
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "|" and depth == 0:
            n += 1
        i += 1
    return n


_SPAN = re.compile(r"`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|\"[^\"]+\"|'[^']+'")


def _delimited_spans(line):
    """[(start, end)] of every backtick / quote / emphasis span on the line."""
    return [(m.start(), m.end()) for m in _SPAN.finditer(line)]


def strength_lines(text, rx=None):
    """([(line, text, 'MENTION'|'USE')]) for every strength marker in `text`.

    mg-70c7: a marker is a MENTION when it lies INSIDE a delimited span, not
    only when it exactly fills one.  The old test looked at the single
    character on each side, so `` `verified against the` `` -- a phrase quoted
    whole, with the marker at its start -- scored as a USE, and this file's own
    comment about mg-dee4's F4 was the first thing it flagged.  Containment is
    the rule the delimiters were always standing for.
    """
    rx = rx or MARK
    out = []
    for i, l in enumerate(text.splitlines(), 1):
        spans = _delimited_spans(l)
        for m in rx.finditer(l):
            inside = any(s <= m.start() and m.end() <= e for s, e in spans)
            mention = inside or any(s in l for s in _MENTION_SIGNALS)
            out.append((i, l.strip(), "MENTION" if mention else "USE"))
    return out


# ---------------------------------------------------------------------------
# IS A FIGURE BACKED BY A TRANSCRIPT?  mg-70c7/F2.
#
# `c252f96` stated the rule -- *a number that moves belongs in a transcript* --
# and applied it to the 2x2 totals three paragraphs above a figure it did not
# apply it to.  A rule stated in prose and applied by hand is applied where the
# author was looking; this makes it a check.
# ---------------------------------------------------------------------------

_NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*)(?![\w.])")


def figures(line):
    """[int] -- the numbers on one line that could be a FIGURE, not a label.

    Excludes 0, 1, 2 (structural in prose far more often than measured), and a
    number immediately preceded by `:`, `#` or `-` (a line reference, a
    heading, a range).  The exclusions are listed so a reader can disagree with
    them, and every dropped number is still visible in the line it came from.
    """
    out = []
    for m in _NUMBER.finditer(line):
        before = line[:m.start()]
        if before.endswith(":") or before.endswith("#") or before.endswith("-"):
            continue
        # `on line 89` is a REFERENCE to a line, not a measurement of
        # anything.  Dropped for the same reason `s3_figure.py:154` is:
        # a census that lets a line number back a figure blesses the figure
        # it exists to catch.
        if re.search(r"\blines?\s+$", before):
            continue
        try:
            v = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if v > 2:
            out.append(v)
    return out


def transcript_figures(paths):
    """{int} -- every FIGURE printed by the given committed transcripts.

    Built with `figures()` LINE BY LINE rather than by matching every number in
    the file.  mg-70c7 recorded the reason in its own OUTCOMES: under the
    whole-file rule the figure mg-dee4's F2 is about -- `154 changed files` --
    came back BACKED, by the string `s3_figure.py:154` in `out_s5_self.txt`.
    A LINE NUMBER was backing a measurement.
    """
    seen = set()
    for p in paths:
        try:
            text = read(p, None)
        except (RuntimeError, OSError):
            continue
        for line in text.splitlines():
            seen.update(figures(line))
    return seen


def out_files(tree):
    """The committed `out_*.txt` of one tree, repo-relative and sorted."""
    return sorted(p for p in git("ls-files", "--", "%s/out_*.txt" % tree)
                  .splitlines() if p)


# ---------------------------------------------------------------------------
# SITE vs EXECUTION.  mg-70c7/F1.
#
# mg-dee4's F1: `11 of 11 read directly` counted SOURCE LINES, three of which
# sit inside `for` loops and run eight times between them, and one of the three
# hand-written argv did not match the line it was labelled with.  A source line
# inside a loop is N executions, not one, and an enumeration that counts SITES
# cannot support a claim about RUNS.  These functions return rows at the
# EXECUTION grain and the word is in their names.
# ---------------------------------------------------------------------------

_FOR = re.compile(r"^\s*for\s+(\w+)\s+in\s+(.*)$")
_DONE = re.compile(r"^\s*done\b")
_WORD = re.compile(r"\"([^\"]*)\"|'([^']*)'|(\S+)")
_SIMPLE_ASSIGN = re.compile(r"^\s*(\w+)=(\$\{[^}]*\}|\$\w+)\s*;?\s*$")


def _loop_items(header):
    """The literal words of a `for VAR in <words>` header, or None.

    None whenever any word is not a literal -- a `$VAR`, a `$(…)`, a glob.
    An expansion this parser cannot evaluate must not be silently counted as
    one iteration; `not statically expandable` is the honest answer and it is
    what None makes the caller print.
    """
    body = re.sub(r"\bdo\b\s*$", "", header.split(";")[0]).strip()
    out = []
    for m in _WORD.finditer(body):
        w = next(g for g in m.groups() if g is not None)
        if not w or w == "\\":
            continue
        if any(c in w for c in "$*?`"):
            return None
        out.append(w)
    return out or None


def for_loops(text):
    """[(var, items or None, first body line, last body line)] -- one per `for`.

    Trailing-backslash continuations are joined before the header is parsed: a
    three-item list written over three lines is one loop and three iterations,
    and reading it as one item would be F1 with the sign flipped.
    """
    raw = text.splitlines()
    joined, i = [], 0
    while i < len(raw):
        line, start = raw[i], i + 1
        while line.rstrip().endswith("\\") and i + 1 < len(raw):
            i += 1
            line = line.rstrip()[:-1] + " " + raw[i].strip()
        joined.append((start, i + 1, line))
        i += 1
    out, stack = [], []
    for start, end, line in joined:
        m = _FOR.match(line)
        if m:
            stack.append((m.group(1), _loop_items(m.group(2)), end + 1))
        elif _DONE.match(line) and stack:
            var, items, first = stack.pop()
            out.append((var, items, first, start - 1))
    return out


def expand(word, binding):
    """`${x%% *}`, `${x#* }` and `$x` against one binding -- or None.

    Only the forms this arc's runners use are implemented, and an unrecognised
    expansion returns None rather than surviving literally.  A `$dir` left in
    an argv would produce a command that was never run, labelled with a source
    line that never ran it -- which is mg-dee4's F1 row exactly.
    """
    def sub(m):
        name, op = m.group(1) or m.group(3), m.group(2) or ""
        if name not in binding:
            raise KeyError(name)
        v = binding[name]
        if op.startswith("%%"):
            sep = op[2:].replace("*", "") or " "
            return v.split(sep)[0]
        if op.startswith("#"):
            sep = op[1:].replace("*", "") or " "
            return v.split(sep, 1)[1] if sep in v else v
        if op:
            raise KeyError(op)
        return v
    try:
        return re.sub(r"\$\{(\w+)([^}]*)\}|\$(\w+)", sub, word)
    except KeyError:
        return None


def loop_bindings(text, first, last, binding):
    """`binding` extended by the loop body's own `base=${pair%% *}` assignments.

    The runners here bind one loop variable and split it into two on the next
    line.  A derivation that stopped at the loop variable would have to
    hand-write `base` and `dir`, and a hand-written argv is what F1 is about.
    """
    out = dict(binding)
    for i, line in enumerate(text.splitlines(), 1):
        if not (first <= i <= last):
            continue
        for part in line.split(";"):
            m = _SIMPLE_ASSIGN.match(part)
            if not m:
                continue
            v = expand(m.group(2), out)
            if v is not None:
                out[m.group(1)] = v
    return out


def argv_of(stage, binding):
    """The argv one pipeline STAGE runs under `binding`, or None if not derivable.

    `shlex` with `posix=True`, so `':!*.md'` survives as one word with its
    quotes removed exactly as the shell leaves it -- the pathspec mg-7522's
    hand-list dropped.  None when any word still holds a `$`: a word this
    parser could not resolve must not be run.
    """
    import shlex
    text = re.sub(r"^\s*(?:local\s+|export\s+)?[A-Za-z_]\w*=", "",
                  stage.strip()).lstrip("$([{ \t")
    try:
        words = shlex.split(text, posix=True)
    except ValueError:
        return None
    out = []
    for w in words:
        v = expand(w, binding)
        if v is None or "$" in v:
            return None
        out.append(v)
    return out or None


def pipeline_executions(text, pipe_rx=None):
    """[(line, iteration or None, binding or None, source line)] -- EXECUTIONS.

    One row per RUN of a pipeline line, not one row per line.  A pipeline in a
    `for` over three literal items is three rows; one outside any loop is one
    row with an empty binding; one inside a loop this parser cannot expand is a
    single row with `iteration=None`, which prints as `not derivable` and is
    never silently counted as 1.
    """
    pipe_rx = pipe_rx or _PIPE
    loops = for_loops(text)
    out = []
    for i, line in command_lines(text):
        if not pipe_rx.search(unquoted(line)):
            continue
        here = [lp for lp in loops if lp[2] <= i <= lp[3]]
        if not here:
            out.append((i, 1, {}, line))
            continue
        var, items, first, last = sorted(here, key=lambda lp: -lp[2])[0]
        if items is None:
            out.append((i, None, None, line))
            continue
        for n, item in enumerate(items, 1):
            out.append((i, n, loop_bindings(text, first, last, {var: item}),
                        line))
    return out
