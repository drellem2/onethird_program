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


_LIB7522 = None


def _L():
    """`lib7522`, imported on first use.  THE ONE COPY of the shared rules.

    LAZY AND NOT AT MODULE SCOPE, on purpose.  This file's own docstring says
    `lib7522` is imported BY THE PROBES, and the probes insert its directory on
    `sys.path` only after importing this module -- so a top-level `import
    lib7522` here would either fail or force every probe to reorder its imports.
    The path is inserted here instead, so `figures()` and `alternatives()` can
    delegate to the single definition of each without changing how anything is
    called.  See those two functions for what mg-56dc/T2d found and what
    delegating costs.
    """
    global _LIB7522
    if _LIB7522 is None:
        import sys
        sys.path.insert(0, os.path.join(REPO, SUBJECT))
        import lib7522
        _LIB7522 = lib7522
    return _LIB7522


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

def figures(line):
    """[int] -- the numbers on one line that could be a FIGURE.  ONE RULE.

    THIS IS `lib7522.figures`, CALLED AND NOT RESTATED.  mg-56dc/T2d, repaired
    by mg-bf79: this file used to carry its own copy, and the two DISAGREED --
    on exactly one integer in 0..500, the value `3`, because the copy here
    dropped `v <= _SMALL` with `_SMALL = 3` while its own docstring said it
    excluded "`0`, `1` and `2`".  So the code and its own label disagreed too,
    which is O1's defect class inside O4's.

    WHICH COPY WAS WRONG, said rather than merged away: THIS ONE.  Both
    docstrings claimed 0/1/2; only `lib7522`'s did it.  Deleting this body
    therefore makes the surviving rule the one both docstrings always described,
    and `3` is a figure again in this tree as it always was in mg-7522's.

    WHAT IS LOST, said too, because it is not nothing.  `r3_strength.py`'s R3c
    used to describe its re-derivation as sharing "no code with `lib7522`'s",
    and after this it shares this rule.  That sentence is corrected there.  The
    independence that mattered -- the population, the window, the corpus -- is
    still written in this tree; what is gone is an independence that existed
    only as a duplicate, and a duplicate that disagrees with its twin on a real
    input was never independence.  Two copies that agree today are a future
    disagreement; these two did not even agree today.
    """
    return _L().figures(line)


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


# mg-70c7's own work item id, as its own commits spell it.  A parameter of the
# provenance query below rather than a literal buried inside it.
MY_TAG = "(mg-70c7)"


def published_by(tag, added_only=True):
    """[repo-relative path] -- the ARTIFACTS a deliverable AUTHORED, sorted.

    THE PROPERTY, STATED WHERE THE CHECK LIVES.  mg-56dc/T2a, repaired by
    mg-bf79: *the strictest rule this tree applies to anything ranged over the
    `out_*.txt` of one directory* -- a population defined by a path, which is
    the finding this tree exists to repair, committed by its own self-check.
    E1 asks whether every count this deliverable PRINTS states its grain, and
    the counts it prints are not only in its transcripts: mg-05eb's OPEN 2 was
    one figure wrong in four artifacts and THREE of them were prose.  So the
    population is:

        a tracked file that a commit of this deliverable ADDED, that still
        exists, and that a reader reads as its record -- a transcript
        (`out_*.txt`) or prose (`*.md`).

    Each clause is mechanical and each earns its place:

      ADDED     `--diff-filter=A`.  This tree MODIFIED `lib7522.py` and
                republished mg-c2b3's and mg-7522's transcripts; those are
                artifacts it changed, not artifacts it authored, and a count in
                one of them is not a count it printed.  Without this clause the
                population is 22 and E1 becomes a check on somebody else's
                grain discipline, which is R1's job and not R6's.
      EXISTS    a path deleted since is not an artifact a reader can read.
      A RECORD  the sources are excluded because E1 ranges over PRINTED
                COUNTS, and a `%3d` in a format string is not one.

    WHY THIS IS NOT ANOTHER PATH.  The query is put to the WHOLE repository --
    `git log --all` over every commit -- and no directory is named anywhere in
    this function.  The answer contains
    `docs/repair-mg-70c7-grain-and-population.md`, four directories away, which
    is exactly the member a path could not have reached and exactly the kind of
    artifact mg-05eb found wrong.

    THE LIMIT, stated at the rule rather than left to be found: provenance is
    read from COMMIT SUBJECTS.  An artifact published by a commit whose subject
    omits the tag is invisible here, and a commit naming two work items counts
    for both.  `r6_self.py` prints the tag it searched and the number of commits
    it matched, so a reader sees the query rather than trusting it.

    AND A DEFECT OF THIS FUNCTION, RECORDED RATHER THAN SMOOTHED AWAY.  Its
    first draft selected commits with `--grep='\\(mg-70c7\\)'`, escaping the
    parentheses -- and `git log --grep` is BASIC regex, in which `\\(` opens a
    GROUP rather than matching a paren.  The pattern therefore reduced to the
    bare string `mg-70c7`, matched every commit whose BODY mentions this tree,
    and returned 15 artifacts including mg-56dc's own README, OUTCOMES,
    PREDICTIONS and published document.  A population meant to be *the
    artifacts I authored* silently became *the artifacts of everyone who has
    written about me* -- including my auditor's, which E1 would then have been
    grading.  An escape that means the opposite in the dialect it lands in is
    the same failure as a label that names the wrong grain: the notation says
    one thing and the machine does another.  The subject is now matched in
    Python, where the string is a string.
    """
    subjects = provenance_commits(tag)
    if not subjects:
        return []
    args = ["show", "--format=", "--name-only"]
    if added_only:
        args.append("--diff-filter=A")
    seen, out = set(), []
    for sha, _subj in subjects:
        for path in git(*args, sha).splitlines():
            path = path.strip()
            if not path or path in seen:
                continue
            seen.add(path)
            if not os.path.exists(os.path.join(REPO, path)):
                continue
            base = os.path.basename(path)
            if (base.startswith("out_") and base.endswith(".txt")) \
                    or base.endswith(".md"):
                out.append(path)
    return sorted(out)


def provenance_commits(tag):
    """[(short sha, subject)] -- commits whose SUBJECT carries `tag`, newest first.

    The tag is tested with `in` on the subject line, in Python.  NOT with
    `git log --grep`, and the reason is the defect recorded in `published_by`:
    `--grep` is basic regex, so an escaped `\\(` is a group and the parentheses
    this repository's convention puts around a work-item id cannot be matched
    literally without a dialect argument nobody wants to have.  Reading `%s`
    and testing it here makes the query a fact about the subject line.
    """
    out = []
    for line in git("log", "--all", "--format=%h%x1f%s").splitlines():
        sha, _, subj = line.partition("\x1f")
        if tag in subj:
            out.append((sha.strip(), subj))
    return out


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
    """How many top-level `|` alternatives a regex source has.  ONE RULE.

    THIS IS `lib7522.alternatives`, CALLED AND NOT RESTATED.  The floor item
    mg-bf79 adds, which neither mg-56dc's brief nor mg-70c7's names: `figures()`
    was not the only rule this file kept in two copies.  `alternatives()` is a
    RULE and not a helper -- it produces the published figure *"nine
    alternatives against three"*, which is the shortest true statement of
    mg-dee4's F3.

    AND THESE TWO AGREED.  Their bodies were byte-identical after unparsing, so
    unifying them changes no number anywhere.  That is the point rather than an
    excuse for having left them: two identical copies provide no independence at
    all, only the appearance of it, and they are one edit away from being the
    pair that `figures()` already was.  The census of every name defined in both
    libraries, with a disposition for each, is
    `code/runner_exit_repair_bf79/out_p4_figures.txt`.
    """
    return _L().alternatives(pattern)
