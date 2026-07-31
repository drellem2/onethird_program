"""mg-56dc -- shared instrument for the independent audit of mg-70c7.

WHAT KIND OF ARTIFACT THIS IS, AND WHAT IT THEREFORE OWES.  The subject of this
audit is a repair whose largest finding is that *a count of SITES cannot support
a claim about RUNS*, and whose second largest is that *a rule applied to your
subject must be applied to you*.  So this file owes two things:

  * every enumerator below returns rows at ONE grain, says which in its
    docstring, and the word is in its name.  `exec_site_rows` returns ROWS and
    `exec_sites` returns SITES, and the whole of T1c is that those are two
    numbers;
  * every rule this file points at mg-70c7 is pointed at mg-56dc in `t5`/`t2`
    over a population that includes this tree's own `*.md` AND the published
    document -- not the `*.py` + `*.sh` population that is F3's other half.

WHAT IT IMPORTS AND WHAT IT DOES NOT.  Nothing that MEASURES mg-70c7 is
borrowed: the loop expansion, the caller-property scan, the figure rule and the
grain classifier are written here from scratch, so a probe can disagree with the
thing it is checking.  `lib7522` and `libc2b3` ARE imported by `t3_population`
and only there, because T3's question is *"is the REPAIRED predicate's
population right"*, and a question about a predicate has to be put to the
predicate that runs.
"""

import os
import re
import subprocess

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                      capture_output=True, text=True,
                      check=True).stdout.strip()

TREE = "code/runner_exit_audit_56dc"                 # mine
SUBJECT = "code/runner_exit_repair_70c7"             # mg-70c7, audited here
S7522 = "code/runner_exit_repair_7522"               # mg-7522, its subject
SWEEP = "code/runner_exit_c2b3"                      # mg-c2b3, the arc sweep
DEE4 = "code/runner_exit_audit_dee4"                 # mg-dee4, the audit landed
A05EB = "code/runner_exit_audit_05eb"                # mg-05eb
SUBJECT_DOC = "docs/repair-mg-70c7-grain-and-population.md"
DOC_7522 = "docs/OneThird-RunnerExit-PopulationRepair.md"
MY_DOC = "docs/audit-mg-56dc-grain-and-population.md"

REPAIR_REV = "1ee1f1b"        # mg-7522's repair
PRE = "1ee1f1b^"              # the fixed pre-repair ref
PINNED = "bee07a1"            # the sweep's pin
SWEEP_REV = "52aeaf4"         # mg-c2b3's commit
DEE4_REV = "ba85387"          # mg-dee4's evidence commit


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

    A truncated reason is a reason silently shortened into a different one.
    Restated here rather than imported, so this tree does not depend on the
    tree it is auditing for its own output.
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


def exists(path, ref=None):
    if ref is None:
        return os.path.exists(os.path.join(REPO, path))
    try:
        git("cat-file", "-e", "%s:%s" % (ref, path))
        return True
    except RuntimeError:
        return False


def outs(tree):
    """The `out_*.txt` of one tree ON DISK, repo-relative and sorted.

    GRAIN: one row per FILE.  On disk and not `git ls-files`, for the reason
    mg-70c7 records in its own `outs()`: a tree's transcripts are untracked on
    the run that first writes them, and an index-built corpus is empty on that
    run.
    """
    import glob
    d = os.path.join(REPO, tree)
    return sorted("%s/%s" % (tree, os.path.basename(p))
                  for p in glob.glob(os.path.join(d, "out_*.txt")))


def run_argv(argv, cwd, timeout=1800, env=None):
    """(exit code or None on timeout, combined output).

    LIST argv, never `shell=True`, so no shell parses the command, so there is
    no pipeline and `returncode` is the target's own status.  The timeout path
    returns None, which renders as `-` and never as 0.
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


# ---------------------------------------------------------------------------
# THE GRAIN CLASSIFIER.  The primary target: for every count a transcript
# prints, does its own label say SITES or EXECUTIONS?
# ---------------------------------------------------------------------------

# A PRINTED COUNT ROW in this arc's transcripts is a label followed by white
# space and one or more integers, with the last integer ending the line (or
# followed only by a unit word).  Restricting to that shape rather than to
# "any line with a digit" is what keeps this from being a census of prose:
# a sentence is not a count row, and counting it as one would make the grain
# question unanswerable by construction.
_COUNT_ROW = re.compile(r"^(?P<label>\s{2,}[^\d\n][^\n]*?)\s{2,}"
                        r"(?P<nums>\d[\d\s./]*?)\s*$")

# EXECUTION grain: the label says the number counts things that HAPPENED.
EXEC_WORDS = re.compile(
    r"\bexecutions?\b|\binvocations?\b|\bruns?\b|\biterations?\b"
    r"|\bread directly\b|\bat run ?time\b|\bexecuted\b|\bstatuses read\b", re.I)
# SITE grain: the label says the number counts things that are WRITTEN, or
# containers of them.  `files`, `pipelines`, `rows` and `argv` are site-grain
# words for the same reason `lines` is -- they range over source, not over runs.
SITE_WORDS = re.compile(
    r"\bsites?\b|\bsource lines?\b|\blines?\b|\bpipelines?\b|\bfiles?\b"
    r"|\brows?\b|\bargv\b|\bsteps?\b|\bartifacts?\b|\btranscripts?\b"
    r"|\bfigures?\b|\balternatives?\b|\bclaims?\b|\buses?\b|\bmentions?\b"
    r"|\bfilters?\b|\bfixtures?\b|\banchors?\b|\bbasenames?\b|\bcall sites?\b"
    r"|\bpath\b|\bstages?\b|\bmarkers?\b|\bcommands?\b|\brunners?\b"
    r"|\bscripts?\b|\bitems?\b|\bchecks?\b|\bpredicates?\b|\bassertions?\b"
    r"|\bmembers?\b|\bcolumns?\b|\bwords?\b|\bstring\b|\bregex\b", re.I)


def count_rows(text):
    """[(line no, label, [ints])] -- every PRINTED COUNT ROW in a transcript.

    GRAIN: one row per printed LINE, which is the only grain available for a
    census over output.  The rows this returns are the population of the grain
    question, and the population is a shape rule over the line, not a list of
    interesting labels -- a hand-list of labels is how this check would become
    the thing it is auditing.
    """
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        m = _COUNT_ROW.match(line.rstrip())
        if not m:
            continue
        nums = [int(n) for n in re.findall(r"\d+", m.group("nums"))]
        if not nums:
            continue
        label = m.group("label").strip()
        if not re.search(r"[A-Za-z]", label):
            continue
        out.append((i, label, nums))
    return out


def _classify(text):
    e = bool(EXEC_WORDS.search(text))
    s = bool(SITE_WORDS.search(text))
    if e and s:
        return "BOTH"
    if e:
        return "EXECUTION"
    if s:
        return "SITE"
    return "NONE"


HEADER_LOOKBACK = 8


def grain_of(label, above=()):
    """('EXECUTION'|'SITE'|'BOTH'|'NONE', where it was found) for one count row.

    WIDENED IN STAGES, and the stage is returned rather than folded away:

      `label`   the label of the count itself carries the grain word;
      `prev`    it is on one of the TWO lines above -- the window mg-70c7's own
                E1 check uses, because this arc hard-wraps its prose;
      `header`  it is only in a COLUMN HEADER further up.  A table row's grain
                lives in the header, which can be six lines away, and a rule
                with a two-line window steps over it -- which is F4's defect
                (line-locality) asked of the grain check rather than of the
                marker check.

    Widening in stages rather than all at once is deliberate: a single wide
    window would classify almost everything and answer nothing.  `above` is
    the preceding lines, NEAREST FIRST.
    """
    c = _classify(label)
    if c != "NONE":
        return c, "label"
    for ln in list(above)[:2]:
        c = _classify(ln)
        if c != "NONE":
            return c, "prev"
    for ln in list(above)[2:HEADER_LOOKBACK]:
        # A column header is a line with words and no digits.  Anything with a
        # digit is another count row, not a header for this one.
        if re.search(r"\d", ln):
            continue
        c = _classify(ln)
        if c != "NONE":
            return c, "header"
    return "NONE", "-"


# ---------------------------------------------------------------------------
# THE LOOP EXPANDER.  Written from scratch: T1b's whole point is to count one
# loop both ways WITHOUT the parser whose answer is being checked.
# ---------------------------------------------------------------------------

_FOR = re.compile(r"^\s*for\s+(\w+)\s+in\s+(.*)$")
_DONE = re.compile(r"^\s*done\b")
_PIPE = re.compile(r"(?<!\|)\|(?!\|)(?!&)")
_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")


def unquoted(line):
    """The line with quoted spans blanked: a `|` inside quotes is an argument."""
    return _QUOTED.sub(lambda m: " " * len(m.group(0)), line)


def _join_continuations(text):
    """[(first line no, last line no, joined text)] -- trailing `\\` joined.

    A three-item `for` list written over three lines is ONE loop and THREE
    iterations.  A parser that read it as one item would under-count the
    executions, which is F1 with the sign flipped.
    """
    raw = text.splitlines()
    out, i = [], 0
    while i < len(raw):
        line, start = raw[i], i + 1
        while line.rstrip().endswith("\\") and i + 1 < len(raw):
            i += 1
            line = line.rstrip()[:-1] + " " + raw[i].strip()
        out.append((start, i + 1, line))
        i += 1
    return out


def loop_items(header_body):
    """The literal words of a `for VAR in <words>` header, or None.

    None whenever a word holds a `$`, a glob or a backtick.  An expansion this
    parser cannot evaluate must NOT be counted as one iteration: `not statically
    expandable` is the honest answer, and silently counting it as 1 is exactly
    the site-for-run substitution this audit is about.
    """
    body = re.sub(r"\bdo\b\s*$", "", header_body.split(";")[0]).strip()
    out = []
    for m in re.finditer(r"\"([^\"]*)\"|'([^']*)'|(\S+)", body):
        w = next(g for g in m.groups() if g is not None)
        if not w or w == "\\":
            continue
        if any(c in w for c in "$*?`"):
            return None
        out.append(w)
    return out or None


def for_loops(text):
    """[(var, items or None, first body line, last body line)] -- one per `for`.

    GRAIN: one row per `for` STATEMENT in the source.
    """
    out, stack = [], []
    for start, end, line in _join_continuations(text):
        m = _FOR.match(line)
        if m:
            stack.append((m.group(1), loop_items(m.group(2)), end + 1))
        elif _DONE.match(line) and stack:
            var, items, first = stack.pop()
            out.append((var, items, first, start - 1))
    return out


def pipeline_sites(text, want=None):
    """[(line no, line)] -- pipeline SOURCE LINES.  One row per LINE.

    `want` is an optional substring the line must contain, supplied by the
    caller so this function has no opinion about which shape matters.
    """
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("#") or not line.strip():
            continue
        if not _PIPE.search(unquoted(line)):
            continue
        if want and want not in line:
            continue
        out.append((i, line))
    return out


def pipeline_executions(text, want=None):
    """[(line no, iteration or None, binding, line)] -- one row per RUN.

    A pipeline inside a `for` over three literal items is THREE rows; one
    outside any loop is ONE row; one inside a loop this parser cannot expand is
    a single row with `iteration=None`, printed as `not derivable` and never
    silently counted as 1.
    """
    loops = for_loops(text)
    out = []
    for i, line in pipeline_sites(text, want):
        here = [lp for lp in loops if lp[2] <= i <= lp[3]]
        if not here:
            out.append((i, 1, {}, line))
            continue
        var, items, _f, _l = sorted(here, key=lambda lp: -lp[2])[0]
        if items is None:
            out.append((i, None, None, line))
            continue
        for n, item in enumerate(items, 1):
            out.append((i, n, {var: item}, line))
    return out


# ---------------------------------------------------------------------------
# THE CALLER SCAN, AT TWO GRAINS.  T1c is that these are two numbers.
# ---------------------------------------------------------------------------

_EXEC = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh"
                   r"|run_runner\(")
_NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
_READ = re.compile(r"returncode|check\s*=\s*True")
_ANY_SH = re.compile(r"(?:([\w./-]+)/)?(\w[\w-]*\.sh)\b")
_SET_E = re.compile(r"^\s*set\s+(?:-[a-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b)",
                    re.M)


def exec_site_rows(ref=None):
    """[(file, line, target basename, consumes)] -- one row per (SITE, TARGET).

    A line that executes something and names TWO different shell scripts
    produces TWO rows.  That is the grain `out_r4_property.txt` prints under
    the label `executing sites`, and the difference between this function and
    `exec_sites` below is the whole of T1c.
    """
    files = [f for f in git("ls-files", "--", "*.py", "*.sh").splitlines()
             if f] if ref is None else \
        [f for f in git("ls-tree", "-r", "--name-only", ref).splitlines()
         if f.endswith((".py", ".sh"))]
    out = []
    for f in files:
        try:
            src = read(f, ref)
        except (RuntimeError, OSError):
            continue
        lines = src.split("\n")
        se = bool(_SET_E.search(src))
        for i, line in enumerate(lines, 1):
            if not _EXEC.search(line) or _NOT_EXEC.search(line):
                continue
            seen = set()
            for m in _ANY_SH.finditer(line):
                d, base = m.group(1) or "", m.group(2)
                if "%s" in d or d.startswith("/") or base in seen:
                    continue
                if d and os.path.normpath("%s/%s" % (d, base)) == \
                        os.path.normpath(f):
                    continue
                seen.add(base)
                window = "\n".join(lines[i - 1:i + 25])
                consumes = (se and "||" not in line) if f.endswith(".sh") \
                    else bool(_READ.search(window))
                out.append((f, i, base, consumes))
    return out


def exec_sites(rows_):
    """{(file, line)} -- the DISTINCT SITES behind a list of `exec_site_rows`.

    One source line is one site however many scripts it names.  Both numbers
    are legitimate; publishing one under the other's name is not.
    """
    return {(f, i) for f, i, _b, _c in rows_}


# ---------------------------------------------------------------------------
# FIGURES.  Two copies of this rule already exist in the subject arc and they
# DISAGREE -- see T2d.  This is a third, written here so the disagreement can
# be measured by something that is not either of them.
# ---------------------------------------------------------------------------

_NUMBER = re.compile(r"(?<![\w.])(\d[\d,]*)(?![\w.])")


def figures(line, small=2):
    """[int] -- the numbers on one line that could be a FIGURE, not a label.

    `small` is a PARAMETER here and a constant in both subject copies, which is
    the point: the two copies differ in that constant and nothing measures the
    difference.  Default 2 matches `lib7522`; `small=3` matches `lib70c7`.
    """
    out = []
    for m in _NUMBER.finditer(line):
        before = line[:m.start()]
        if before.endswith(":") or before.endswith("#") or before.endswith("-"):
            continue
        if re.search(r"\blines?\s+$", before, re.I):
            continue
        try:
            v = int(m.group(1).replace(",", ""))
        except ValueError:
            continue
        if v <= small:
            continue
        out.append(v)
    return out


# ---------------------------------------------------------------------------
# FINDINGS.  Printed at the end of every probe, one line each, so `run_all.sh`
# can collect them with a `grep` over the transcripts.
# ---------------------------------------------------------------------------

def finding(fid, text):
    return "FINDING: %s %s" % (fid, text)
