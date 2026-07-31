"""mg-70c7 -- shared instrument for the six findings of mg-dee4 against 1ee1f1b.

WHAT KIND OF ARTIFACT THIS IS, AND WHAT IT THEREFORE OWES.  Four of the six
findings are about the GRAIN or the POPULATION of a count:

  F1  a count of SOURCE LINES presented as a count of RUNS;
  F3  a rule with three alternatives applied to itself and one with nine
      applied to its subject, over a population that excluded every `.md`;
  F5  a population defined by a list of two NAMES;
  F6  a consumption clause narrower than the reason written for it.

So this file may not itself contain a count whose grain is unstated.  Every
enumerator below returns rows at ONE grain and says which in its docstring, and
`r6_self.py` checks the transcripts mechanically for the site-vs-execution
distinction.

WHAT IT BORROWS AND WHAT IT DOES NOT.  `lib7522` is IMPORTED by the probes, on
purpose and in the opposite direction to mg-dee4's choice: mg-dee4 was AUDITING
those predicates and could not borrow them, while this tree is REPAIRING them
and its job is to exercise the repaired rule at its source.  Everything this
file measures ABOUT those rules -- the alternative counts, the population, the
loop expansion, the value-consumption test -- is written here from scratch, so
a probe can still disagree with the thing it is checking.
"""

import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

TREE = "code/runner_exit_repair_70c7"
SUBJECT = "code/runner_exit_repair_7522"           # mg-7522, the repair audited
SWEEP_TREE = "code/runner_exit_c2b3"               # mg-c2b3, the arc-wide sweep
DOC = "docs/OneThird-RunnerExit-PopulationRepair.md"
MY_DOC = "docs/repair-mg-70c7-grain-and-population.md"

REPAIR_REV = "1ee1f1b"        # mg-7522's repair, the subject of mg-dee4
PINNED = "bee07a1"            # the sweep's pin


def bar(t):
    print("=" * 78)
    print(t)
    print("=" * 78)


def hdr(t):
    print()
    bar(t)
    print()


def rows(pairs, widths, indent="      "):
    """Print a table, WRAPPING the last column rather than truncating it.

    A truncated reason is a reason that has been silently shortened into a
    different one.  Inherited as a rule from `lib7522.rows`, restated here so
    this tree does not depend on the file it is repairing for its own output.
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
        raise RuntimeError("git %s -> %d\n%s" % (" ".join(args), p.returncode,
                                                 p.stderr))
    return p.stdout


def read(path, ref=None):
    if ref is None:
        with open(os.path.join(REPO, path), "r", encoding="utf-8",
                  errors="replace") as fh:
            return fh.read()
    return git("show", "%s:%s" % (ref, path))


# ---------------------------------------------------------------------------
# F1.  SITE vs EXECUTION.  The whole finding is that these are different
# numbers, so they get different functions and different words.
# ---------------------------------------------------------------------------

_FOR = re.compile(r"^\s*for\s+(\w+)\s+in\s+(.*)$")
_DONE = re.compile(r"^\s*done\b")
_WORD = re.compile(r"\"([^\"]*)\"|'([^']*)'|(\S+)")


def _items(header_text):
    """The literal words of a `for VAR in <words>` header, quotes removed.

    Returns None when any word is not a literal -- a `$VAR`, a `$(...)`, a glob
    or a `"$@"` -- because an expansion this parser cannot evaluate must not be
    silently counted as one iteration.  Returning None makes the caller say
    `not statically expandable` instead of guessing, which is the difference
    between a derivation and a hand-list wearing a derivation's clothes.
    """
    body = header_text.split(";")[0]
    body = re.sub(r"\bdo\b\s*$", "", body).strip()
    out = []
    for m in _WORD.finditer(body):
        w = m.group(1) if m.group(1) is not None else (
            m.group(2) if m.group(2) is not None else m.group(3))
        if w in ("\\",):
            continue
        if not w:
            continue
        if "$" in w or "*" in w or "?" in w or "`" in w:
            return None
        out.append(w)
    return out or None


def for_loops(text):
    """[(var, [items], first_body_line, last_body_line)] for every literal `for`.

    GRAIN: one row per `for` STATEMENT in the source.  Line continuations with
    a trailing `\\` are joined before the header is parsed, because a three-item
    loop written over three lines is one loop and three iterations, and a parser
    that read it as one item would under-count the executions -- which is F1
    with the sign flipped.
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
            stack.append((m.group(1), _items(m.group(2)), end + 1))
            continue
        if _DONE.match(line) and stack:
            var, items, first = stack.pop()
            out.append((var, items, first, start - 1))
    return out


def pipeline_executions(rel, text, pipe_rx):
    """[(line_no, iteration, {var: value}, source_line)] -- the EXECUTION grain.

    One row per RUN of a pipeline line, not one row per line.  A pipeline
    inside a `for` over three literal items is three rows; a pipeline outside
    any loop is one row with an empty binding.

    `pipe_rx` selects which pipeline lines are wanted (a `| tee` shape, or any
    real pipe).  The caller supplies it so this function has no opinion about
    which shape matters -- having an opinion about that was the SHAPE rule.
    """
    loops = for_loops(text)
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("#") or not pipe_rx.search(line):
            continue
        here = [lp for lp in loops if lp[2] <= i <= lp[3]]
        if not here:
            out.append((i, 1, {}, line))
            continue
        # Innermost enclosing loop only: this arc has no nested `for` around a
        # pipeline, and a product over nested loops would be a guess, not a
        # measurement.  If one ever appears, `not statically expandable` is the
        # honest answer and it is what None gives.
        var, items, _f, _l = sorted(here, key=lambda lp: -lp[2])[0]
        if items is None:
            out.append((i, None, None, line))
            continue
        for n, item in enumerate(items, 1):
            out.append((i, n, {var: item}, line))
    return out


def expand(word, binding):
    """`${x%% *}` / `${x#* }` / `$x` against one loop binding, or None.

    Only the three forms this arc's runners actually use are implemented, and
    an unrecognised expansion returns None rather than being left literal: a
    `$dir` that silently survived into an argv would produce a command that was
    never run, which is exactly the row mg-dee4 found labelled `run_all.sh:39`.
    """
    def sub(m):
        name, op = m.group(1) or m.group(3), m.group(2) or ""
        if name not in binding:
            raise KeyError(name)
        v = binding[name]
        if op.startswith("%%"):
            pat = op[2:]
            return v.split(pat.replace("*", "") or " ")[0] if pat else v
        if op.startswith("#"):
            pat = op[1:]
            sep = pat.replace("*", "") or " "
            return v.split(sep, 1)[1] if sep in v else v
        if op:
            raise KeyError(op)
        return v
    try:
        return re.sub(r"\$\{(\w+)([^}]*)\}|\$(\w+)", sub, word)
    except KeyError:
        return None


_SIMPLE_ASSIGN = re.compile(r"^\s*(\w+)=(\$\{[^}]*\}|\$\w+)\s*;?\s*$")


def loop_bindings(text, first, last, binding):
    """`binding` extended by the loop body's own `base=${pair%% *}` assignments.

    The runners in this arc bind ONE loop variable and then split it into two
    with parameter expansion on the next line.  An argv derivation that stopped
    at the loop variable would have to hand-write `base` and `dir`, and a
    hand-written argv is the thing F1 is about.  Only assignments whose whole
    right-hand side is a single expansion are followed; anything else returns
    the binding unchanged and the caller reports `not derivable`.
    """
    out = dict(binding)
    for i, line in enumerate(text.splitlines(), 1):
        if not (first <= i <= last):
            continue
        for part in line.split(";"):
            m = _SIMPLE_ASSIGN.match(part if part.strip() else " ")
            if not m:
                continue
            v = expand(m.group(2), out)
            if v is not None:
                out[m.group(1)] = v
    return out


def argv_of(stage, binding):
    """The argv one pipeline STAGE runs under `binding`, or None if not derivable.

    `shlex` with `posix=True`, so `':!*.md'` survives as one word with its
    quotes removed exactly as the shell would leave it.  None is returned when
    any word still contains a `$` after expansion -- a word this parser could
    not resolve must not be run, because running a DIFFERENT command and
    labelling it with the source line is precisely mg-dee4's F1 row.
    """
    import shlex
    text = stage.strip()
    text = re.sub(r"^\s*(?:local\s+|export\s+)?[A-Za-z_]\w*=", "", text)
    text = text.lstrip("$([{ \t")
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


# ---------------------------------------------------------------------------
# F6.  CONSUMPTION, as a named disjunction rather than one arm of it.
# ---------------------------------------------------------------------------

_ASSIGN = re.compile(r"^\s*(?:local\s+|export\s+)?([A-Za-z_]\w*)=\$\(")


def captured_var(line):
    """The variable a pipeline's OUTPUT is captured into on this line, or None.

    `n=$(git diff … | wc -c | tr -d ' ')` captures into `n`.  This is the arm
    mg-7522's written reason is about -- *"a `git diff` that failed produced an
    empty stream, `wc -c` reported 0, and the proof read `-> 0 bytes`"* -- and
    it is a claim about the VALUE, which is why it does not need errexit.
    """
    m = _ASSIGN.match(line)
    return m.group(1) if m else None


def var_reads(text, var, exclude_line):
    """[(line, text)] where `$var` / `${var}` is READ, excluding its assignment.

    A capture nobody reads discards nothing that matters, so the value arm is a
    conjunction: captured AND read.  Making it captured-only would widen the
    population by a rule that is not about the defect, which is the mirror of
    defining it by a filename.
    """
    rx = re.compile(r"\$\{%s\b[^}]*\}|\$%s\b" % (re.escape(var),
                                                 re.escape(var)))
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if i == exclude_line or line.strip().startswith("#"):
            continue
        if rx.search(line):
            out.append((i, line.strip()))
    return out


# ---------------------------------------------------------------------------
# F2 / F3.  IS A FIGURE BACKED BY A TRANSCRIPT?
# ---------------------------------------------------------------------------

_NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*)(?![\w.])")
# Numbers that are not figures: a section number, a year, a line reference of
# the form `file.py:214`, a git revision.  Listed rather than tuned, because a
# generous exclusion list here turns an unbacked figure into a non-figure.
_SMALL = 3


def figures(line):
    """[int] -- the numbers on one line that could be a FIGURE.

    Excludes `0`, `1` and `2`, which are structural in prose ("both", "one at a
    time", "2x2") far more often than they are measurements, and excludes a
    number immediately preceded by `:` (a line reference) or by `#` (a heading
    or an issue).  The exclusion is stated so a reader can disagree with it;
    every figure it drops is still visible in the line it came from.
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
        if re.search(r"\blines?\s+$", before, re.I):
            continue
        try:
            v = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if v <= _SMALL:
            continue
        out.append(v)
    return out


def transcript_numbers(paths):
    """{int} -- every FIGURE printed by the given committed transcripts.

    The backing test is deliberately WEAK in one direction and stated as such:
    it asks whether the figure appears anywhere in a transcript, not whether it
    appears as the answer to the same question.  A weak test that runs is worth
    more than a strong one that is a promise, and the rows print the figure so
    a reader can check the sense by eye.

    A DEFECT IN THIS FUNCTION, RECORDED RATHER THAN SMOOTHED AWAY.  Its first
    draft matched every number in the transcript text, `_NUMBER` over the whole
    file.  Under that rule the figure mg-dee4's F2 is about -- `154 changed
    files` -- came back BACKED, by the string `s3_figure.py:154` in
    `out_s5_self.txt`.  A LINE NUMBER was backing a measurement.  The corpus is
    now built with the same `figures()` rule the claim side uses, applied line
    by line, so a `:`-prefixed number is not a figure on either side.  The
    lesson is the one this arc keeps re-learning: a check that reads a FORM OF
    CHARACTERS rather than a fact about the run will agree with you for the
    wrong reason.
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


def outs(tree):
    """The `out_*.txt` of one tree ON DISK, repo-relative and sorted.

    ON DISK and not `git ls-files`, and the difference is a defect this file
    had.  A tree's transcripts are untracked on the run that first produces
    them, so a corpus built from the index is EMPTY on that run -- and an empty
    corpus makes every figure UNBACKED, which reads as 108 findings about the
    prose rather than one fact about the index.  The disk is what the probes
    just wrote, and a transcript is a record of a run whether or not it has
    been committed yet.

    ORDERING NOTE, since it is a real limit: `run_all.sh` truncates each
    transcript with `>` before its probe runs, so a probe reading the corpus
    sees the CURRENT run's output for probes that already finished and the
    PREVIOUS run's for those that have not.  A second consecutive run therefore
    reads a complete corpus, and the committed transcripts are from such a run.
    """
    import glob
    d = os.path.join(REPO, tree)
    return sorted("%s/%s" % (tree, os.path.basename(p))
                  for p in glob.glob(os.path.join(d, "out_*.txt")))


# ---------------------------------------------------------------------------
# Running things.  LIST argv, never `shell=True`.
# ---------------------------------------------------------------------------

def run_argv(argv, cwd, timeout=1800):
    """(exit code or None on timeout, combined output).

    `returncode` is read on every path; the timeout path returns None, which
    renders as `-` and never as 0.
    """
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    try:
        p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired as ex:
        return None, ((ex.stdout or b"").decode("utf-8", "replace")
                      + (ex.stderr or b"").decode("utf-8", "replace"))
    return p.returncode, p.stdout + p.stderr


def alternatives(pattern):
    """How many top-level `|` alternatives a regex source has.

    F3 is a comparison of two rules by their reach, and `9 alternatives against
    3` is the shortest true statement of it.  Counted on the pattern SOURCE at
    depth 0 so a `(?:a|b)` group inside one alternative is not counted twice.
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
