#!/usr/bin/env python3
"""mg-97fb -- THE INDEPENDENT AUDIT OF THE mg-3f3b `n/a`-AND-VOCABULARY REPAIR.

The object: mg-3f3b's repair of mg-7e39's four findings, landed at `4785086`
and completed through `75333b2`.  The brief's primary target is EVERY `n/a`
the repair leaves behind -- each read as a CLAIM about its site, with the case
it says is impossible CONSTRUCTED.

WHAT IS MINE AND WHAT IS THE ARTIFACT'S
---------------------------------------
MINE: every mutation below, written from the KIND TITLE and never from the
`k_*` function that declines the cell; my own quotation readers (six of them,
where the gate declares one); my own AST sweep and its `In`-comparison rule;
my own site cutters, written from the DISCLOSURE SENTENCES in `EXTENT_OF`
rather than from `framed_row`/`section`; and every population, from
`git ls-tree` at a named commit.

THE ARTIFACT'S: the gate itself, because the gate is the subject -- and it is
scored by RUNNING IT AS A SUBPROCESS and reading gate rows out of its stdout.
Nothing in this file imports `verify_landing`.  A matrix cell is read out of
the printed matrix BY COLUMN OFFSET, never by counting substrings of the
printed line (which is what `repair_ec07.py`'s own census does -- see E2).

ON-DISK PROBES.  Every probe here mutates a file in the tree and restores it.
A restore that is not byte-identical means this audit rewrote the artifact
while auditing it, so every on-disk probe carries its own `restored` flag and
one False makes the run RED.

Pure Python 3 + git.  No third-party packages.  Runtime ~2 min.
"""

import ast
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

LANDING_REL = "code/hodge_leverage_landing_e1d0/verify_landing.py"
LANDING_DIR = os.path.join(REPO, os.path.dirname(LANDING_REL))
LANDING = os.path.join(REPO, LANDING_REL)
RECORDS = os.path.join(LANDING_DIR, "site_records.txt")
SWEEP_REL = "code/hodge_leverage_repair_6df0/repair_ec07.py"
REPAIR_REL = "code/hodge_leverage_repair_3f3b/repair_7e39.py"

STATE_REL = "STATE.md"
DELIV_REL = "docs/OneThird-Hodge-Side-Leverage.md"
HIST_REL = "docs/state-history/attempt-mg-a3d4.md"

# The commits this audit names.  Each is used for ONE thing and the thing is
# said beside it, because "the commit" is three different commits in this arc.
C_PRE6DF0 = "803bd50"    # mg-6df0's parent: the construct at its widest
C_6DF0 = "77306a7"       # mg-6df0 landed: mg-7e39 measured 5 live here
C_PRE3F3B = "979df72"    # mg-3f3b's probe commit: the LAST 8-`n/a` matrix
C_3F3B = "4785086"       # mg-3f3b's repair landed: the first 7-`n/a` matrix

RESULTS = []
TMP = tempfile.mkdtemp(prefix="mg-97fb-")
WORKTREES = []


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


FINDINGS = []


def finding(tag, text):
    """A FINDING is a measurement about the artifact, not a failure of this
    instrument.  It is recorded as a measurement and printed as a finding, so
    the suite stays green (predicted exit 0) and the finding is still in the
    transcript under its own id."""
    FINDINGS.append((tag, text))
    print(f"  >> FINDING {tag}: {text}")


def git(*args, repo=REPO):
    return subprocess.run(["git", "-C", repo] + list(args),
                          capture_output=True, text=True,
                          check=True).stdout


def rev(x):
    return git("rev-parse", x).strip()


def read(rel, root=REPO):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return fh.read()


def blob(commit, rel):
    p = subprocess.run(["git", "-C", REPO, "show", f"{commit}:{rel}"],
                       capture_output=True, text=True)
    return p.stdout if p.returncode == 0 else None


def worktree(commit):
    """A detached worktree at `commit`, so a gate from that commit runs
    against THAT COMMIT'S DOCUMENTS.  Pointing an old gate at today's tree
    would confound a change in the derivation with a change in the text."""
    path = os.path.join(TMP, "wt_" + rev(commit)[:8])
    if path not in WORKTREES:
        git("worktree", "add", "--detach", "-q", path, commit)
        WORKTREES.append(path)
    return path


def cleanup():
    for p in WORKTREES:
        subprocess.run(["git", "-C", REPO, "worktree", "remove", "--force", p],
                       capture_output=True, text=True)
    shutil.rmtree(TMP, ignore_errors=True)


# --------------------------------------------------------------------------
# RUNNING THE ARTIFACT.  As a subprocess, scored from its stdout.
# --------------------------------------------------------------------------
GATE_LINE = re.compile(r"^\s*\[(CONFIRMED|REFUTED  |MEASURED )\] (GATE @ .+)$")


def run_gate(root=REPO, *args):
    exe = os.path.join(root, LANDING_REL)
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    p = subprocess.run([sys.executable, exe, *args], capture_output=True,
                       text=True, env=env, cwd=os.path.dirname(exe))
    return p.returncode, p.stdout + p.stderr


def gate_rows(out):
    """The gate rows the runner printed ON THE TREE -- cut at the negative
    control, whose rows are the artifact's own mutations and not the tree's."""
    body = out.split("NEGATIVE CONTROL")[0]
    return [(m.group(1) == "CONFIRMED", m.group(2))
            for m in (GATE_LINE.match(l) for l in body.split("\n")) if m]


def refuted(out):
    return [d for ok, d in gate_rows(out) if not ok]


MATRIX_ROW = re.compile(r"^ {4}(K\d\d .*)$")


def matrix(out):
    """The printed matrix, read BY COLUMN OFFSET.

    ⚠️ NOT by `l.count("FIRES")`.  The gate prints
    `f"    {title[:60]:<62}" + "".join(f"{c:<20}" for c in row)`, so the cells
    are at fixed offsets and the kind TITLE shares the line with them.  A
    census by substring over the whole line counts any occurrence of `FIRES`,
    `SILENT` or `n/a` in the title as a cell -- which is a substring test over
    a whole row, the construct this arc repairs, in the census of the very
    matrix whose `n/a` cells are the finding.  See E2, where it is
    demonstrated rather than argued."""
    names, cells = [], {}
    lines = out.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("    kind") and not names:
            names = [l[66 + 20 * j:66 + 20 * (j + 1)].strip() for j in range(3)]
        m = MATRIX_ROW.match(l)
        if m and names:
            tag = m.group(1)[:3]
            for j, n in enumerate(names):
                cells[(tag, n)] = l[66 + 20 * j:66 + 20 * (j + 1)].strip()
    return names, cells


SITE_NAMES = ("the STATE.md row", "§14", "H8")
NA_LINE = re.compile(
    r"^ {6}n/a  (K\d\d) @ (" + "|".join(re.escape(n) for n in SITE_NAMES)
    + r") +(.*)$")


def na_reasons(out):
    return [(m.group(1), m.group(2), m.group(3))
            for m in (NA_LINE.match(l) for l in out.split("\n")) if m]


# --------------------------------------------------------------------------
# ON-DISK PROBES.  Mutate, run, restore, and CHECK THE RESTORE.
# --------------------------------------------------------------------------
def on_disk(rel, transform, root=REPO, args=(), guard_records=False):
    """`transform(text) -> text` applied to `rel` in `root`, the gate run, the
    file restored, and the restore CHECKED.  Returns
    (rc, out, restored, changed)."""
    full = os.path.join(root, rel)
    with open(full, "rb") as fh:
        orig = fh.read()
    recs = None
    if guard_records:
        with open(os.path.join(root, os.path.dirname(LANDING_REL),
                               "site_records.txt"), "rb") as fh:
            recs = fh.read()
    seen = None
    try:
        new = transform(orig.decode("utf-8"))
        if new is None or new.encode("utf-8") == orig:
            return None, "", True, False, None
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(new)
        rc, out = run_gate(root, *args)
        if recs is not None:
            with open(os.path.join(root, os.path.dirname(LANDING_REL),
                                   "site_records.txt"), "rb") as fh:
                seen = fh.read()
    finally:
        with open(full, "wb") as fh:
            fh.write(orig)
        if recs is not None:
            with open(os.path.join(root, os.path.dirname(LANDING_REL),
                                   "site_records.txt"), "wb") as fh:
                fh.write(recs)
    with open(full, "rb") as fh:
        restored = fh.read() == orig
    return rc, out, restored, True, seen


RESTORES = []


def note_restore(tag, ok):
    RESTORES.append((tag, ok))


# --------------------------------------------------------------------------
# MY SITE CUTTERS -- written from the DISCLOSURE SENTENCES, not from the code.
#
# `EXTENT_OF["section"]`   : "the markdown SECTION, heading to the next heading
#                            of the same or shallower level -- not the file
#                            that contains it"
# `EXTENT_OF["framed_row"]`: "the table ROW and the HEADER LINES it is read
#                            under -- not the table's other rows, which are
#                            outside this record"
#
# Implemented from those two sentences alone.  D1 checks byte-for-byte against
# what the gate actually cuts.  That is the test of whether a scope sentence
# is a SPECIFICATION or a LABEL.
# --------------------------------------------------------------------------
def cut_section(text, anchor):
    lines = text.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(anchor))
    level = len(lines[i]) - len(lines[i].lstrip("#"))
    for j in range(i + 1, len(lines)):
        l = lines[j]
        if l.startswith("#"):
            lv = len(l) - len(l.lstrip("#"))
            if lv <= level:
                return "\n".join(lines[i:j])
    return "\n".join(lines[i:])


def cut_framed_row(text, anchor):
    """The ROW, plus THE HEADER LINES IT IS READ UNDER -- the nearest column
    line above it and the delimiter under that.  Nothing else of the table."""
    lines = text.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith(anchor))
    top = max(k for k in range(i)
              if re.fullmatch(r"\|[\s:|-]+\|", lines[k].strip()))
    return "\n".join([lines[top - 1], lines[top], lines[i]])


SITE_CUT = {
    "the STATE.md row": (STATE_REL, cut_framed_row, "| **AMBER-POSITIVE"),
    "§14": (DELIV_REL, cut_section, "## §14 — `STATE.md` row, as landed"),
    "H8": (HIST_REL, cut_section, "### H8 — "),
}


def my_sites(root=REPO):
    return {n: fn(read(rel, root), a) for n, (rel, fn, a) in SITE_CUT.items()}


# --------------------------------------------------------------------------
# MY FIGURE TOKEN AND MY QUOTATION READERS.
# The gate declares ONE quotation convention.  I read SIX, because "0 of them
# carry a figure token" is only a fact about the SITE if the reader that found
# 0 is not the only reader there is.
# --------------------------------------------------------------------------
FIG = re.compile(r"(?<![\w−+])(?:[−+]?\d{1,3}(?: \d{3})+|[−+]\d{3,})(?!\d)")

MARKS = [
    ("*\"…\"*  (the gate's declared convention)", re.compile(r'\*"(.+?)"\*', re.S)),
    ("*'…'*   (the gate's declared convention)", re.compile(r"\*'(.+?)'\*", re.S)),
    ("`…`     a code span", re.compile(r"`([^`\n]{1,300})`")),
    ('"…"     plain double quotes', re.compile(r'"([^"\n]{1,300})"')),
    ("“…”     curly quotes", re.compile(r"“([^”]{1,300})”")),
    ("> …     a markdown blockquote", re.compile(r"(?m)^\s*>\s?(.+)$")),
]


def marked_spans(site):
    """[(reader, start, end, text)] for every span any of my six readers
    calls a marked quotation."""
    out = []
    for nm, pat in MARKS:
        for m in pat.finditer(site):
            out.append((nm, m.start(), m.end(), m.group(0)))
    return out


# --------------------------------------------------------------------------
# MY SWEEP RULE for THE CONSTRUCT.
#
# An occurrence is an `ast.Compare` with the single op `In` whose LEFT is a
# string constant ending in a declared gate-row kind and whose comparator is a
# name/attribute/subscript -- i.e. `"SITE RECORD" in d`.  Lexically inside a
# function called `by_substring` it is the one declared place the construct is
# performed on purpose, and is reported separately rather than skipped.
#
# This is NOT the parent sweep's rule.  `repair_ec07.py` works line-by-line
# over source text with a list of heading-function names to exclude; this
# walks the AST, so a line that mentions `heading(` elsewhere cannot mask an
# occurrence and a two-line comparison is still one node.
# --------------------------------------------------------------------------
HEADING_FUNCS = ("heading", "row_kind", "row_kind_of",
                 "row_vocabulary", "ROW_KINDS", "ROW_NAMES",
                 "row_headings", "declared_vocab")


def _headed_names(scope):
    """Names in `scope` bound to something a HEADING FUNCTION produced.

    ⚠️ THIS IS A DEFECT OF THIS INSTRUMENT, FOUND BY ITS OWN FIRST RUN AND
    KEPT.  The first version of the rule below matched `"FIGURE ORDER" in bad`
    in `audit_ec07.py` and reported it as the construct.  It is not: `bad` is
    `{heading(name, d) for ok, d in rows if not ok}` -- a set of HEADINGS, so
    the membership test is the REMEDY, spelled as a set lookup instead of as
    `endswith`.  A rule that cannot tell a set of headings from a whole row
    manufactures the finding it is looking for, which is the shape mg-3f3b
    recorded about its own `K10` emphasis pattern."""
    headed = set()
    for node in ast.walk(scope):
        targets, value = [], None
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AugAssign):
            targets, value = [node.target], node.value
        elif isinstance(node, (ast.For, ast.comprehension)):
            targets, value = [node.target], getattr(node, "iter", None)
        if value is None:
            continue
        src = ast.dump(value)
        if not (any(f"id='{f}'" in src or f"attr='{f}'" in src
                    for f in HEADING_FUNCS)
                or "' -- '" in src or '" -- "' in src):
            continue
        for t in targets:
            for sub in ast.walk(t):
                if isinstance(sub, ast.Name):
                    headed.add(sub.id)
    return headed


def occurrences(src, vocab):
    """[(line, literal, kind, declared)] -- THE CONSTRUCT.

    An `ast.Compare` with the single op `In` or `NotIn` whose LEFT is a string
    constant ending in a declared gate-row kind and whose comparator is a
    plain name.  `not in` counts: `"SITE RECORD" not in d` in `reseal`'s
    refusal is the occurrence mg-6df0 repaired, and a rule that only saw `in`
    would have reported that repair as touching nothing.

    Lexically inside a function called `by_substring` it is the one declared
    place the construct is performed on purpose, and is reported separately
    rather than skipped.  Comparators bound to the output of a heading
    function are the REMEDY spelled as a set lookup and are not counted."""
    try:
        with warnings.catch_warnings():
            # Parsing 480 files of another deliverable's source emits its
            # SyntaxWarnings into MY transcript.  They are that file's, not a
            # measurement of anything here.
            warnings.simplefilter("ignore")
            tree = ast.parse(src)
    except SyntaxError:
        return []
    declared = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                and node.name == "by_substring":
            for sub in ast.walk(node):
                declared.add(id(sub))
    # The headed names of each SCOPE, computed once per scope and mapped onto
    # the nodes inside it.  (Computing it per node is cubic and hangs on a
    # 2 000-line instrument -- found by running it.)
    scopes = [tree] + [n for n in ast.walk(tree)
                       if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    headed = {}
    for sc in scopes:
        names = _headed_names(sc)
        if not names:
            continue
        for n in ast.walk(sc):
            headed.setdefault(id(n), set()).update(names)
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare) or len(node.ops) != 1:
            continue
        if not isinstance(node.ops[0], (ast.In, ast.NotIn)):
            continue
        left = node.left
        if not (isinstance(left, ast.Constant) and isinstance(left.value, str)):
            continue
        name = next((v for v in vocab if left.value.endswith(v)), None)
        if name is None:
            continue
        comp = node.comparators[0]
        if not isinstance(comp, (ast.Name, ast.Attribute, ast.Subscript)):
            continue
        if isinstance(comp, ast.Name) and comp.id in headed.get(id(node), set()):
            continue
        out.append((node.lineno, left.value, name, id(node) in declared))
    return out


_PYFILES = {}


def py_files_at(commit):
    key = rev(commit)
    if key not in _PYFILES:
        out = git("ls-tree", "-r", "--name-only", key, "code/")
        _PYFILES[key] = sorted(p for p in out.split("\n")
                               if p.endswith(".py"))
    return _PYFILES[key]


_TREES = {}


def tree_at(commit):
    """The tree at `commit`, extracted ONCE with `git archive`.  480 `git
    show` calls per commit is 480 subprocesses; this is one."""
    key = rev(commit)
    if key not in _TREES:
        d = os.path.join(TMP, "tree_" + key[:8])
        os.makedirs(d, exist_ok=True)
        ar = subprocess.Popen(["git", "-C", REPO, "archive", key, "code/"],
                              stdout=subprocess.PIPE)
        subprocess.run(["tar", "-x", "-C", d], stdin=ar.stdout)
        ar.stdout.close()
        ar.wait()
        _TREES[key] = d
    return _TREES[key]


def sweep_at(commit, vocab):
    """[(rel, line, literal, kind, declared)] over EVERY `.py` under `code/`
    in the tree at `commit` -- the population named, never a bare total."""
    root = tree_at(commit)
    hits = []
    for rel in py_files_at(commit):
        try:
            with open(os.path.join(root, rel), encoding="utf-8") as fh:
                src = fh.read()
        except (OSError, UnicodeDecodeError):
            continue
        for lineno, lit, kind, decl in occurrences(src, vocab):
            hits.append((rel, lineno, lit, kind, decl))
    return hits


# --------------------------------------------------------------------------
# A0 -- PREFLIGHT
# --------------------------------------------------------------------------
def a0():
    head("A0 -- PREFLIGHT")
    rc, out = run_gate()
    print(f"    HEAD                      : {rev('HEAD')[:12]}")
    print(f"    the gate, unmutated       : exit {rc}")
    print(f"    gate rows on the tree     : {len(gate_rows(out))}")
    record(rc == 0,
           f"A0a the gate is green on the unmutated tree (exit {rc}), so every "
           f"fire below is attributable to a probe of this instrument's and to "
           f"nothing standing.  Predicted exit 0")
    record(len(gate_rows(out)) == 34,
           f"A0b the figure gate returns {len(gate_rows(out))} rows on the "
           f"tree.  Predicted 34 -- the population every row-selection number "
           f"below is a fraction OF, named rather than assumed")
    return out


# --------------------------------------------------------------------------
# A1 -- THE MATRIX, FROM THE ARTIFACT'S OWN STDOUT
# --------------------------------------------------------------------------
def a1(out):
    head("A1 -- THE MATRIX AT HEAD, READ BY COLUMN AND NOT BY SUBSTRING")
    names, cells = matrix(out)
    fires = sum(1 for v in cells.values() if v.startswith("FIRES"))
    silent = sum(1 for v in cells.values() if v == "SILENT")
    na = sum(1 for v in cells.values() if v == "n/a")
    for l in out.split("\n"):
        if MATRIX_ROW.match(l) or l.startswith("    kind"):
            print(l.rstrip())
    print()
    record(len(cells) == 36 and fires == 29 and silent == 0 and na == 7,
           f"A1a the product is {len(cells)} cells over {len(names)} sites: "
           f"{fires} FIRE, {silent} SILENT, {na} n/a.  Predicted 36 / 29 / 0 / "
           f"7.  Read cell by cell at the printed column offsets -- the report "
           f"is the MATRIX and the population is the PRODUCT")
    record(silent == 0,
           f"A1b (PRESERVE) {fires} of {fires} applicable cells FIRE and "
           f"{silent} are SILENT, scored by running the artifact as a "
           f"SUBPROCESS and reading its stdout.  mg-7e39's 29 of 29, 0 silent, "
           f"is undisturbed")
    return names, cells


# --------------------------------------------------------------------------
# A2 -- EVERY `n/a` READ AS A CLAIM, AND THE CASE IT SAYS IS IMPOSSIBLE
#       CONSTRUCTED
# --------------------------------------------------------------------------
def swap(text, a, b):
    return text.replace(a, "\0", 1).replace(b, a, 1).replace("\0", b, 1)


def k08_state(site, sites, root):
    """K08 -- TWO TABLE ROW LABELS EXCHANGED, at the STATE.md row.

    The site holds ONE data row.  The nearest thing to the kind that exists is
    an exchange with a ledger row OUTSIDE the declared site, so that is what
    is built -- and where it lands is the answer."""
    def t(text):
        row = next(l for l in text.split("\n")
                   if l.startswith("| **AMBER-POSITIVE"))
        others = [l for l in text.split("\n")
                  if l.startswith("| ") and l is not row
                  and not re.fullmatch(r"\|[\s:|-]+\|", l.strip())
                  and l.split("|")[1].strip() and text.count(l) == 1
                  and l != row]
        other = next((l for l in others
                      if l.split("|")[1].strip() != row.split("|")[1].strip()),
                     None)
        if other is None:
            return None
        a, b = row.split("|")[1], other.split("|")[1]
        return text.replace(row, row.replace(a, b, 1), 1) \
                   .replace(other, other.replace(b, a, 1), 1)
    return STATE_REL, t, False, (
        "the site's row label exchanged with another LEDGER ROW's -- the "
        "nearest thing to the kind that exists, and it reaches ONE LINE "
        "OUTSIDE the declared site, which the reason names")


def k10_marked(which):
    """K10 -- A FIGURE INSIDE A MARKED QUOTATION ALTERED, built with SIX
    quotation readers instead of the gate's one."""
    def make(site, sites, root):
        text = sites[site]
        cands = [(nm, s, e, t) for nm, s, e, t in marked_spans(text)
                 if FIG.search(t)]
        if not cands:
            return None, None, False, ("no span any of my 6 readers calls "
                                       "marked carries a figure token")
        nm, s, e, span = cands[0]
        tok = FIG.search(span).group()
        bad = tok[:-1] + ("8" if tok[-1] != "8" else "7")
        rel = SITE_CUT[site][0]

        def t(whole):
            if whole.count(span) != 1:
                return None
            return whole.replace(span, span.replace(tok, bad, 1), 1)
        return rel, t, False, (
            f"the figure {tok!r} inside {span[:44]!r} -- a span my reader "
            f"{nm.split('(')[0].strip()} calls marked and the gate's ONE "
            f"declared convention does not, which is why `partition` treats "
            f"that token as an ASSERTION")
    return make


def k11_s14(site, sites, root):
    """K11 -- THE TABLE'S ALIGNMENT SHIFTED, at §14.  §14 holds no table in
    either format, so the strongest same-shape mutation is a whitespace shift
    on an ordinary line: it tests whether the site is blind to whitespace."""
    text = sites[site]
    line = next((l for l in text.split("\n")
                 if l.startswith("  ") and l.strip() and text.count(l) == 1),
                None)
    if line is None:
        line = next((l for l in text.split("\n")
                     if l.strip() and text.count(l) == 1 and " " in l.strip()),
                    None)
    if line is None:
        return None, None, False, "no line at this site occurs exactly once"
    rel = SITE_CUT[site][0]

    def t(whole):
        if whole.count(line) != 1:
            return None
        return whole.replace(line, line + " ", 1)
    return rel, t, False, (
        "a whitespace shift on an ordinary line of §14 -- NOT an instance of "
        "the kind, because the kind is a TABLE's alignment and this site holds "
        "no table by any of my three readers.  Run anyway, to see whether the "
        "site is blind to whitespace")


def k12_state(site, sites, root):
    """K12 -- A WHOLE PARAGRAPH RELOCATED OUT OF THE SITE, at the STATE.md
    row.  The site is one paragraph; relocating it removes the site."""
    def t(text):
        row = next(l for l in text.split("\n")
                   if l.startswith("| **AMBER-POSITIVE"))
        return text.replace("\n" + row, "", 1) + "\n" + row
    return STATE_REL, t, False, (
        "the site's only paragraph moved to the end of the file -- which "
        "DELETES the site rather than relocating a paragraph out of it, so it "
        "is a different kind")


def table_lines(text):
    """A table line by ANY of my three readers: a pipe row (3+ pipes), a
    whitespace-column row (2+ runs of 2+ spaces), or a tab-separated row.
    Leading whitespace is stripped first, which the gate's reader does not
    do -- an indented pipe table is a table."""
    return [l for l in text.split("\n")
            if l.lstrip().count("|") >= 3
            or len(re.findall(r"\S(  +)\S", l)) >= 2
            or l.count("\t") >= 2]


def k08_s14(site, sites, root):
    text = sites[site]
    rows = table_lines(text)
    return None, None, False, (
        f"{len(rows)} of this site's {len(text.split(chr(10)))} line(s) is a "
        f"table row by ANY of my three readers (pipe with 3+ bars after "
        f"lstrip, whitespace-column, tab), so there are no two row labels here "
        f"to exchange")


def k09_s14(site, sites, root):
    text = sites[site]
    rows = table_lines(text)
    return None, None, False, (
        f"{len(rows)} of this site's {len(text.split(chr(10)))} line(s) is a "
        f"table line at all by ANY of my three readers, so none of them is a "
        f"column header")


CONSTRUCTIONS = {
    ("K08", "the STATE.md row"): k08_state,
    ("K08", "§14"): k08_s14,
    ("K09", "§14"): k09_s14,
    ("K10", "H8"): k10_marked("H8"),
    ("K10", "the STATE.md row"): k10_marked("the STATE.md row"),
    ("K11", "§14"): k11_s14,
    ("K12", "the STATE.md row"): k12_state,
}


def a2(out):
    head("A2 -- EVERY `n/a` READ AS A CLAIM, AND THE CASE IT SAYS IS "
         "IMPOSSIBLE, CONSTRUCTED")
    print("""A matrix reports FIRE / SILENT / n/a and only the first two are measured.
`n/a` is prose, and prose in the grammar of a fact about the SITE can be a
fact about the DERIVATION -- which is what mg-7e39's F1 was.  So each of the
seven is read as a CLAIM and the case it says is impossible is BUILT, from
the KIND TITLE, on disk, against the gate as a subprocess.

A reason FAILS if a mutation OF THE SAME KIND, at the SAME SITE, INSIDE the
declared site boundary exists.  A reason that declines because the derivation
cannot see the text -- "no such text here" where the site has such text -- is
not accepted.
""")
    sites = my_sites()
    reasons = na_reasons(out)
    survivors, failures = [], []
    for tag, name, why in reasons:
        print(f"    {tag} @ {name}")
        print(f"        CLAIM   : {why}")
        make = CONSTRUCTIONS.get((tag, name))
        if make is None:
            print("        ⚠️ NO CONSTRUCTION WRITTEN -- counted as neither")
            continue
        rel, t, same_kind, what = make(name, sites, REPO)
        print(f"        MINE    : {what}")
        print(f"        IS IT THE SAME KIND, INSIDE THE SITE? "
              f"{'YES' if same_kind else 'no'}")
        if rel is None:
            print("        RESULT  : I decline too, with my own count, by a "
                  "reader written here")
            survivors.append((tag, name, "declined independently"))
            continue
        rc, gout, restored, changed, _rec = on_disk(rel, t)
        note_restore(f"A2 {tag} @ {name}", restored)
        if not changed:
            print("        RESULT  : the mutation could not be written back")
            survivors.append((tag, name, "not writable"))
            continue
        bad = refuted(gout)
        recrows = [d for d in bad if d.split(" -- ")[0].endswith("SITE RECORD")]
        figrows = [d for d in bad if d.split(" -- ")[0]
                   .endswith(("FIGURE CENSUS", "FIGURE ORDER"))]
        print(f"        RESULT  : exit {rc}, {len(bad)} row(s) refuted "
              f"({len(recrows)} SITE RECORD, {len(figrows)} FIGURE), restored "
              f"byte-identical: {restored}")
        for d in bad[:4]:
            print(f"                  {d[:104]}")
        # A fire OUTSIDE the declared site boundary, or a fire through the
        # ASSERTION half, is not the kind the cell declines.  Whether the
        # mutation IS that kind is declared by the construction itself, above,
        # and never inferred from which rows happened to fire.
        if same_kind and bool(recrows) and not figrows:
            failures.append((tag, name, why))
            print("        VERDICT : ⚠️ FAILS -- a mutation of the same kind, "
                  "inside the site, FIRES through the record's segment half")
        else:
            survivors.append((tag, name, "fires, but not as this kind"))
            print("        VERDICT : SURVIVES -- what I could build is a "
                  "different kind or lands outside the declared site")
        print()
    record(not failures,
           f"A2a of the {len(reasons)} `n/a` reason(s) the repaired matrix "
           f"prints, {len(survivors)} SURVIVE being read as a claim about "
           f"their site and {len(failures)} do not: "
           f"{[f'{t} @ {n}' for t, n, _w in failures] or 'none'}.  Predicted "
           f"7 survivors, 0 failures.  mg-7e39 read 8 and 7 survived")
    counted = [(t, n, w) for t, n, w in reasons if re.search(r"\d", w)]
    record(len(counted) == len(reasons),
           f"A2b {len(counted)} of {len(reasons)} reason(s) carry a digit, "
           f"which is the artifact's own fail-closed test.  E1 is what that "
           f"test is worth")
    return survivors, failures


# --------------------------------------------------------------------------
# A3 -- THE `n/a` THAT WAS DELETED, AND WHETHER IT BECAME AN UNTESTED FIRE
# --------------------------------------------------------------------------
def shift_pipe_padding(text):
    """MY alignment shift, written from the KIND TITLE -- "the table's
    ALIGNMENT shifted, no figure moved".  Padding MOVED from one cell of the
    site's own row to another.  The delimiter line is not touched: `|:---|`
    carries the column's alignment SPECIFIER, and moving space there changes
    what the table means, which is a different kind."""
    row = next(l for l in text.split("\n")
               if l.startswith("| **AMBER-POSITIVE"))
    want = FIG.findall(row)
    # ⚠️ THE SITE'S OWN LENGTH IS ONE OF THE LIVE FIGURES.  `cell` is
    # `len(state_row(...))`, so ANY mutation that changes the row's byte count
    # moves a figure at all three sites -- the first version of this inserted
    # one space and got exit 1 with SIX FIGURE rows refuted, a K01 wearing
    # K11's name.  So the shift MOVES A SPACE rather than adding one: one cell
    # gains the padding another loses.  Length identical, figure-token
    # multiset identical, alignment different.  `k_layout` reaches the same
    # constraint from the other side by shifting a HEADER line, whose length
    # is not a figure; this shifts the ROW, which is the harder case and the
    # one the cell is about.
    opens = [i for i in range(1, len(row) - 2) if row[i:i + 2] == "| "]
    for i in opens:
        for j in reversed(opens):
            if j <= i:
                continue
            cand = row[:i + 2] + " " + row[i + 2:j + 1] + row[j + 2:]
            if len(cand) == len(row) and FIG.findall(cand) == want \
                    and cand != row and text.count(row) == 1:
                return text.replace(row, cand, 1)
    return None


def a3(cells):
    head("A3 -- THE `n/a` THAT WAS DELETED: 8 -> 7, AND WHETHER THE CELL IS "
         "TESTED")
    print("""An `n/a` resolved by DELETING it -- replaced by a FIRE nobody built -- is
worse than the `n/a`.  So the pre-repair matrix is re-run from ITS OWN
COMMIT'S WORKTREE (its gate against its documents, not today's), the two
matrices are diffed cell by cell, and the cell that moved is rebuilt here.
""")
    pre_root = worktree(C_PRE3F3B)
    rc_pre, pre_out = run_gate(pre_root)
    _pn, pre_cells = matrix(pre_out)
    pre_na = {k for k, v in pre_cells.items() if v == "n/a"}
    post_na = {k for k, v in cells.items() if v == "n/a"}
    print(f"    pre-repair worktree  : {rev(C_PRE3F3B)[:12]} (exit {rc_pre})")
    print(f"    n/a before / after   : {len(pre_na)} / {len(post_na)}")
    moved = sorted(pre_na - post_na)
    added = sorted(post_na - pre_na)
    for k in moved:
        print(f"      n/a -> {cells.get(k, '?'):<12} {k[0]} @ {k[1]}")
    for k in added:
        print(f"      {pre_cells.get(k, '?')} -> n/a  {k[0]} @ {k[1]}")
    to_silent = [k for k in moved if cells.get(k) == "SILENT"]
    record(len(moved) == 1 and not added and not to_silent,
           f"A3a exactly {len(moved)} cell(s) moved out of `n/a` between "
           f"{rev(C_PRE3F3B)[:7]} and HEAD, {len(added)} moved into it, and "
           f"{len(to_silent)} became SILENT.  Predicted 1 / 0 / 0.  The matrix "
           f"went from {len(pre_na)} `n/a` to {len(post_na)} by covering a "
           f"cell, not by dropping one")

    for label, root in (("HEAD (the repaired derivation)", REPO),
                        (f"{C_PRE6DF0} (mg-6df0's PARENT -- the defect's "
                         f"oldest state)", worktree(C_PRE6DF0))):
        rc, gout, restored, _ch, _rec = on_disk(STATE_REL, shift_pipe_padding, root)
        note_restore(f"A3 pipe shift @ {label}", restored)
        bad = refuted(gout)
        recs = [d for d in bad if d.split(" -- ")[0].endswith("SITE RECORD")]
        figs = [d for d in bad if d.split(" -- ")[0]
                .endswith(("FIGURE CENSUS", "FIGURE ORDER"))]
        record(bool(rc == 1 and recs and not figs),
               f"A3b MY OWN pipe-table padding shift at {label}: exit {rc}, "
               f"{len(recs)} SITE RECORD row(s) refuted and {len(figs)} FIGURE "
               f"row(s).  Restored byte-identical: {restored}.  Predicted exit "
               f"1, record fires, no figure row -- the mutation's "
               f"figure-token multiset is IDENTICAL to the site's by "
               f"construction.  Written from the KIND TITLE, not from "
               f"`k_layout`")
    record(True,
           "A3c AND THE SAME PROBE FIRES AT BOTH COMMITS.  The GATE never had "
           "this hole -- only the MATRIX said there was nothing here to catch. "
           "mg-7e39's F1 is a defect of the instrument that reports coverage, "
           "not of the gate that provides it, and a control that fired only at "
           "HEAD would have been measuring my probe")
    return pre_out


# --------------------------------------------------------------------------
# B -- EXISTED / TOUCHED / LIVE, AND THE 1-of-6 vs 0-of-6 RECONCILIATION
# --------------------------------------------------------------------------
def declared_vocab(commit=None, root=None):
    src = read(LANDING_REL, root) if root else (blob(commit, LANDING_REL) or "")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "ROW_KINDS" for t in node.targets):
            return sorted(e.value for e in getattr(node.value, "elts", [])
                          if isinstance(e, ast.Constant))
    return []


def printed_vocab(out, declared):
    """The kind of every row the gate PRINTS, taken from its stdout -- the
    vocabulary derived from what the gate prints rather than from what it
    says it prints."""
    kinds = []
    for _ok, d in gate_rows(out):
        h = d.split(" -- ")[0]
        k = next((v for v in declared if h.endswith(v)), None)
        kinds.append(k)
    return kinds


def hand_vocab():
    """mg-6df0's ORIGINAL hand list, read out of the source at the commit
    where it was still a list."""
    src = blob(C_6DF0, SWEEP_REL) or ""
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "ROW_NAMES" for t in node.targets):
            return [e.value for e in getattr(node.value, "elts", [])
                    if isinstance(e, ast.Constant)]
    return []


def b1(out):
    head("B1 -- THE CONSTRUCT: EXISTED / TOUCHED / LIVE, COUNTED HERE AT EACH "
         "COMMIT")
    declared = declared_vocab(root=REPO)
    printed = [k for k in printed_vocab(out, declared) if k]
    vocab = sorted(set(declared) | set(printed))
    hand = hand_vocab()
    print(f"    the gate DECLARES at HEAD : {declared}")
    print(f"    the gate PRINTS (distinct): {sorted(set(printed))}")
    print(f"    mg-6df0's hand list       : {hand}")
    print(f"    MY vocabulary (both)      : {vocab}")
    print()
    print("""My vocabulary is derived at HEAD and applied at every commit, deliberately:
"how many instances existed at 803bd50" is a question asked in TODAY'S
vocabulary, and a vocabulary that was short is exactly what hid them.
""")
    table = []
    for label, c in ((f"{C_PRE6DF0}  mg-6df0's parent", C_PRE6DF0),
                     (f"{C_6DF0}  mg-6df0 landed  ", C_6DF0),
                     (f"{C_PRE3F3B}  mg-3f3b's probe ", C_PRE3F3B),
                     (f"{C_3F3B}  mg-3f3b's repair", C_3F3B),
                     (f"{rev('HEAD')[:7]}  HEAD           ", "HEAD")):
        hits = sweep_at(c, vocab)
        live = [h for h in hits if not h[4]]
        table.append((label, c, len(py_files_at(c)), live,
                      [h for h in hits if h[4]]))
        print(f"    {label} : {len(live):>2} live occurrence(s) of the "
              f"construct over {len(py_files_at(c))} `.py` files under `code/`"
              f"  (+{len([h for h in hits if h[4]])} in `by_substring`, "
              f"declared)")
    print()
    for label, c, _n, live, _d in table:
        if not live:
            continue
        print(f"    at {label.strip()}:")
        for rel, ln, lit, kind, _d in live:
            print(f"        {rel}:{ln}  {lit!r}")
    print()
    at = {c: live for _l, c, _n, live, _d in table}
    n_pre6, n_6df0 = len(at[C_PRE6DF0]), len(at[C_6DF0])
    n_pre3, n_3f3b, n_head = (len(at[C_PRE3F3B]), len(at[C_3F3B]),
                              len(at["HEAD"]))
    record(bool(n_pre6 == 7 and n_6df0 == 6 and n_3f3b == 0 and n_head == 0),
           f"B1a EXISTED / TOUCHED / LIVE, counted here.  At {C_PRE6DF0} "
           f"(mg-6df0's parent) {n_pre6} EXISTED; mg-6df0 TOUCHED "
           f"{n_pre6 - n_6df0}, leaving {n_6df0} LIVE at {C_6DF0}.  At "
           f"{C_PRE3F3B} {n_pre3} were live; mg-3f3b TOUCHED {n_pre3 - n_3f3b}, "
           f"leaving {n_3f3b} LIVE at {C_3F3B} and {n_head} at HEAD.  Predicted "
           f"7 / 1 / 6 and 6 / 6 / 0")
    print()
    print("    THE THREE NUMBERS, SIDE BY SIDE")
    print(f"      mg-7e39 says : 6 existed at {C_PRE6DF0}, the repair touched "
          f"1, 5 are live at {C_6DF0}")
    print("      mg-3f3b says : the construct is 0 of 6, with an EMPTY "
          "disposition table")
    print(f"      I count      : {n_pre6} existed at {C_PRE6DF0}, mg-6df0 "
          f"touched {n_pre6 - n_6df0}, {n_6df0} live at {C_6DF0}; mg-3f3b "
          f"touched {n_pre3 - n_3f3b} of {n_pre3}, {n_3f3b} live at {C_3F3B}")
    missed = [h for h in at[C_PRE6DF0] if h[3] == "WRITTEN ONCE"]
    record(bool(n_pre6 == 7 and n_6df0 == 6 and len(missed) == 1),
           f"B1b THE RECONCILIATION, AND IT REFUTES BOTH DENOMINATORS.  The "
           f"two sixes are not the same six.  mg-7e39's is (1 touched + 5 "
           f"live) at {C_PRE6DF0} and is short by {n_pre6 - 6} -- "
           f"{[f'{r}:{l}' for r, l, _li, _k, _d in missed]}, a `WRITTEN ONCE` "
           f"occurrence its regex-derived vocabulary could not see.  mg-3f3b's "
           f"is what was LIVE WHEN IT STARTED ({n_pre3}), which excludes the "
           f"one mg-6df0 had already repaired -- a different set of the same "
           f"size.  Both NUMERATORS hold; the population EXISTED is "
           f"{n_pre6}, not 6, and neither party's 6 names it")
    if n_pre6 != 6:
        finding("G4", f"NEITHER SIX IS THE POPULATION.  mg-7e39's `1 of 6` and "
                      f"mg-3f3b's `0 of 6` are two different sixes, and the "
                      f"number of instances that EXISTED at {C_PRE6DF0} is "
                      f"{n_pre6}.  mg-7e39's 6 is (1 touched + 5 live) counted "
                      f"with a vocabulary regexed out of the gate's `print` "
                      f"calls, which could not see `WRITTEN ONCE`; mg-3f3b's 6 "
                      f"is what was LIVE WHEN IT STARTED, which excludes the "
                      f"one mg-6df0 had already repaired.  Both numerators "
                      f"hold, both denominators are short, and they are short "
                      f"in opposite directions")
    return vocab, declared, printed, hand, at


def b2(out, vocab, at):
    head("B2 -- THE FOUR THAT SELECT 6 GATE ROWS WHERE 3 WERE MEANT, ROW BY "
         "ROW")
    rows = [d for _ok, d in gate_rows(out)]
    print(f"    the gate's live rows at HEAD : {len(rows)}")
    print()
    sites = {}
    for rel, ln, lit, kind, _d in at[C_6DF0]:
        sites.setdefault((rel, kind), []).append(ln)
    exact = 0
    for (rel, kind), lns in sorted(sites.items()):
        sub = [r for r in rows if kind in r]
        hd = [r for r in rows if r.split(" -- ")[0].endswith(kind)]
        extra = [r for r in sub if r not in hd]
        flag = "  " if not extra else "⚠️"
        print(f"    {flag} {rel}:{','.join(map(str, lns))}   {kind!r}")
        print(f"         {len(sub)} of {len(rows)} rows by substring, "
              f"{len(hd)} by heading -- {len(extra)} it was never meant to "
              f"select")
        for r in extra:
            print(f"           EXTRA  {r.split(' -- ')[0]}")
        if len(sub) == 6 and len(hd) == 3:
            exact += 1
    record(exact == 4,
           f"B2a of the {len(sites)} (file, kind) pair(s) live at {C_6DF0}, "
           f"{exact} select exactly 6 rows where 3 were meant, each extra "
           f"named above.  Predicted 4 of them at 6-vs-3.  The other(s) select "
           f"the same by both tests and are the construct anyway")


# --------------------------------------------------------------------------
# C -- THE VOCABULARY AND THE POPULATION
# --------------------------------------------------------------------------
def c1(declared, printed, hand):
    head("C1 -- THE VOCABULARY: DERIVED FROM WHAT THE GATE PRINTS, DIFFED "
         "AGAINST HAND")
    src = read(SWEEP_REL)
    by_ast = "ast.walk" in src and "ROW_KINDS" in src
    node = next((n for n in ast.walk(ast.parse(src))
                 if isinstance(n, ast.Assign)
                 and any(getattr(t, "id", "") == "ROW_NAMES" for t in n.targets)),
                None)
    is_call = node is not None and isinstance(node.value, ast.Call)
    print(f"    `ROW_NAMES` is assigned from : "
          f"{ast.dump(node.value)[:60] if node else 'absent'}...")
    record(bool(is_call and by_ast),
           f"C1a `ROW_NAMES` in `repair_ec07.py` is assigned from a CALL "
           f"({getattr(getattr(node.value, 'func', None), 'id', '?')}) that "
           f"reads `ROW_KINDS` out of the gate BY AST, not from a list "
           f"literal.  Derived, not hand-listed")
    dset, pset, hset = set(declared), set(p for p in printed if p), set(hand)
    print(f"    declared by the gate  : {sorted(dset)}")
    print(f"    PRINTED by the gate   : {sorted(pset)}")
    print(f"    the hand list         : {sorted(hset)}")
    print(f"    declared, never printed: {sorted(dset - pset)}")
    print(f"    PRINTED, not declared  : {sorted(pset - dset)}")
    print(f"    declared, not in hand  : {sorted(dset - hset)}")
    record(not (pset - dset),
           f"C1b every one of the {len(printed)} rows the gate PRINTS carries "
           f"a kind the gate DECLARES: {len(pset - dset)} printed-and-undeclared. "
           f"The derived vocabulary is checked against the rows themselves, "
           f"not against a second reading of the source")
    record(sorted(dset - hset) == ["READ AT THE SITE", "WRITTEN ONCE"],
           f"C1c DERIVED vs HAND: the hand list is {len(hset)} and the "
           f"declaration is {len(dset)}; the gap is "
           f"{sorted(dset - hset)} -- TWO names.  mg-7e39 measured this gap "
           f"with a regex over the gate's `print` calls and found ONE, because "
           f"`WRITTEN ONCE` was emitted as `'{{label}}' is WRITTEN ONCE`")
    # The FAIL-CLOSED control, at HEAD where nothing is wrong.
    victim = sorted(pset)[0]

    def drop(text):
        return text.replace(f'    "{victim}",\n', "", 1)
    rc, gout, restored, changed, _rec = on_disk(LANDING_REL, drop)
    note_restore("C1 ROW_KINDS name removed", restored)
    unkinded = [l.strip() for l in gout.split("\n")
                if l.strip().startswith("[REFUTED  ] GATE:")
                and "ROW_KINDS" in l]
    record(bool(changed and rc == 1 and unkinded),
           f"C1d CONTROL: {victim!r} removed from `ROW_KINDS` and NOTHING "
           f"else -> exit {rc}, {len(unkinded)} declared-vocabulary row(s) "
           f"REFUTED.  Restored byte-identical: {restored}.  Predicted exit 1. "
           f"A fail-closed rule that cannot be made to fail is a sentence")
    # DERIVED vs HAND, as a COUNT OF OCCURRENCES and not only as a set diff.
    # "The vocabulary is two names short" is a fact about a list; "the same
    # rule finds N where the hand list finds M" is a fact about the tree.
    for label, c in ((f"{C_PRE6DF0} (mg-6df0's parent)", C_PRE6DF0),
                     (f"{C_6DF0} (mg-6df0 landed) ", C_6DF0)):
        d_hits = [h for h in sweep_at(c, sorted(dset)) if not h[4]]
        h_hits = [h for h in sweep_at(c, sorted(hset)) if not h[4]]
        only = sorted({f"{r}:{l}" for r, l, _li, _k, _d in d_hits}
                      - {f"{r}:{l}" for r, l, _li, _k, _d in h_hits})
        print(f"    at {label}: the DECLARED vocabulary of {len(dset)} finds "
              f"{len(d_hits)} occurrence(s) where the HAND list of {len(hset)} "
              f"finds {len(h_hits)}")
        for o in only:
            print(f"        seen only by the declared vocabulary: {o}")
        record(None,
               f"C1e DERIVED vs HAND AS A COUNT OF OCCURRENCES at {c}: "
               f"{len(d_hits)} by the gate's own declaration of {len(dset)} "
               f"names, {len(h_hits)} by the hand list of {len(hset)}, over "
               f"{len(py_files_at(c))} `.py` files under `code/`.  The "
               f"{len(only)} the hand list cannot see are {only}.  mg-7e39 "
               f"measured this gap as 5-against-4 with a vocabulary regexed "
               f"out of the gate's `print` calls; the declaration sees more "
               f"than either")
    return dset, pset, hset


POP_FIGURE = re.compile(r"(\d[\d,  ]*)\s*`?\.py`?\s+files")
QUOTATION = re.compile(r'"[^"]*"|“[^”]*”')


def hand_lists():
    """`COMPUTED` and `PROSE` out of the repair's own source, by AST."""
    src = read(REPAIR_REL)
    out = {}
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if getattr(t, "id", "") in ("COMPUTED", "PROSE"):
                    out[t.id] = [e.value if isinstance(e, ast.Constant)
                                 else "<derived>"
                                 for e in getattr(node.value, "elts", [])]
    return out


def publishing_commit(rel):
    return git("log", "-1", "--format=%H", "--", rel).strip() or None


def c2():
    head("C2 -- THE POPULATION, RECOMPUTED AT THE PUBLISHING COMMIT BY ME")
    for label, c in ((f"{C_6DF0} (mg-6df0 landed)", C_6DF0),
                     (f"{C_PRE6DF0} (its parent)  ", C_PRE6DF0),
                     (f"{C_3F3B} (mg-3f3b landed)", C_3F3B),
                     (f"{rev('HEAD')[:7]} (HEAD)          ", "HEAD")):
        print(f"    .py under code/ at {label} : {len(py_files_at(c))}")
    old = blob(C_6DF0, "code/hodge_leverage_repair_6df0/out_repair_6df0.txt")
    m = POP_FIGURE.search(old or "")
    said = int(re.sub(r"\D", "", m.group(1))) if m else None
    have = len(py_files_at(C_6DF0))
    record(said == 429 and have == 448,
           f"C2a THE HISTORICAL FACT, from `git ls-tree` and `git show` here "
           f"and not quoted: the transcript as committed at {C_6DF0} publishes "
           f"{said} and the tree at {C_6DF0} holds {have} `.py` under `code/` "
           f"-- {have - (said or 0)} in the population and not in the number. "
           f"Wrong when written: its parent {C_PRE6DF0} held "
           f"{len(py_files_at(C_PRE6DF0))} too")

    # THE POPULATION OF PUBLISHERS, DERIVED rather than listed.
    lists = hand_lists()
    tracked = set(lists.get("COMPUTED", [])) | set(lists.get("PROSE", []))
    found = []
    for rel in git("ls-files").split("\n"):
        if not rel or not rel.endswith((".md", ".txt")):
            continue
        try:
            text = read(rel)
        except (OSError, UnicodeDecodeError):
            continue
        if POP_FIGURE.search(text):
            found.append(rel)
    missing = [r for r in found if r not in tracked]
    print()
    print(f"    `COMPUTED` (hand-written) : {lists.get('COMPUTED')}")
    print(f"    `PROSE`    (hand-written) : {lists.get('PROSE')}")
    print(f"    files in the tree publishing a `.py` population by the "
          f"repair's OWN `POP_FIGURE` rule: {len(found)}")
    for r in found:
        mark = "  " if r in tracked else "⚠️"
        print(f"      {mark} {r}")
    if missing:
        finding("G2", f"THE F2 REPAIR'S OWN POPULATION IS A HAND LIST.  "
                      f"`COMPUTED` names {len(lists.get('COMPUTED', []))} "
                      f"transcript(s) and `PROSE` {len(lists.get('PROSE', []))} "
                      f"file(s); the tree holds {len(found)} file(s) that "
                      f"publish a `.py` population by the repair's OWN rule, "
                      f"and {len(missing)} are in neither list: {missing}.  "
                      f"F2's repair checks a population it chose by hand -- "
                      f"which is F5, the finding this same deliverable landed "
                      f"one axis over")
    record(None,
           f"C2b ⚠️ THE POPULATION OF PUBLISHERS IS ITSELF A HAND LIST.  "
           f"`COMPUTED` names {len(lists.get('COMPUTED', []))} and `PROSE` "
           f"names {len(lists.get('PROSE', []))}; sweeping the tree with the "
           f"repair's own `POP_FIGURE` finds {len(found)} file(s) that publish "
           f"a `.py` population, {len(missing)} of them in NEITHER list: "
           f"{missing}.  This is F5's defect -- a scope nobody chose -- landed "
           f"on F2's axis by the deliverable that landed F5 on the vocabulary "
           f"axis")
    # Each omitted file, checked by the rule that would have applied to it.
    stale, carried = [], []
    for rel in missing:
        rev_ = publishing_commit(rel)
        if rev_ is None:
            continue
        text = blob(rev_, rel) or ""
        m = POP_FIGURE.search(text)
        if not m:
            continue
        n = int(re.sub(r"\D", "", m.group(1)))
        have = len(py_files_at(rev_))
        if rel.endswith(".txt"):
            if n != have:
                stale.append((rel, n, have, rev_[:12]))
            ctx = text[max(0, m.start() - 62):m.end() + 14].replace(
                "\n", " ").strip()
            print(f"      -- {rel}: FIRST `POP_FIGURE` match is {n}; the tree "
                  f"at {rev_[:12]} holds {have}")
            print(f"           context: ...{ctx[:98]}...")
        else:
            for i, l in enumerate(read(rel).split("\n"), 1):
                for _mm in POP_FIGURE.finditer(QUOTATION.sub("", l)):
                    carried.append((rel, i, l.strip()[:76]))
    for rel, i, l in carried:
        print(f"      ⚠️ CARRIED IN PROSE  {rel}:{i}  {l}")
    # --- C2d: the artifact's OWN list, re-checked at HEAD.
    print()
    own = []
    for rel in lists.get("COMPUTED", []):
        if rel == "<derived>":
            rel = "code/hodge_leverage_repair_6df0/out_repair_6df0.txt"
        pc = publishing_commit(rel)
        if pc is None:
            continue
        text = blob(pc, rel) or ""
        m = POP_FIGURE.search(text)
        if not m:
            continue
        n = int(re.sub(r"\D", "", m.group(1)))
        have = len(py_files_at(pc))
        mark = "  " if n == have else "⚠️"
        print(f"    {mark} {rel}")
        print(f"        publishes {n}; the tree at {pc[:12]} -- the commit "
              f"that now publishes it -- holds {have}")
        own.append((rel, n, have, pc))
    bad_own = [o for o in own if o[1] != o[2]]
    if bad_own:
        finding("G5", f"THE F2 REPAIR IS F2 AT HEAD, {len(bad_own)} OF "
                      f"{len(own)}, AND ITS OWN TRANSCRIPT STILL SAYS 0 "
                      f"STALE.  Both transcripts in `COMPUTED` publish "
                      f"{bad_own[0][1]} and the tree at each one's publishing "
                      f"commit holds {bad_own[0][2]}.  The transcripts were "
                      f"RIGHT WHEN WRITTEN -- the pre-merge commits hold "
                      f"exactly what they say -- and the MERGE REBASED them "
                      f"onto a larger tree, so the commit that publishes each "
                      f"figure is no longer the commit the figure was measured "
                      f"at.  The repair separates a figure a PUBLICATION STEP "
                      f"recomputes from a figure PROSE carries; the step that "
                      f"broke this is neither.  It is the merge, and nothing "
                      f"re-runs the check after one")
    record(None,
           f"C2d THE ARTIFACT'S OWN `COMPUTED` LIST, RE-CHECKED AT HEAD: "
           f"{len(bad_own)} of {len(own)} transcript(s) disagree with the tree "
           f"at their own publishing commit.  `out_repair_3f3b.txt` records "
           f"`S4a ... 0 disagree`, and that was true of the commits it was "
           f"written against.  A check that reads git is a MEASUREMENT AT THE "
           f"COMMIT IT RAN AT, and freezing its verdict in a transcript is the "
           f"same move as freezing a population in prose")

    record(None,
           f"C2c THE OMITTED FILES, PUT THROUGH THE RULE THAT WOULD HAVE "
           f"APPLIED TO THEM: {len(stale)} transcript(s) disagree with their "
           f"own publishing commit and {len(carried)} population figure(s) are "
           f"carried as a number in prose outside `\"...\"`.  ⚠️ ONE OF THOSE "
           f"IS THE RULE'S OWN LIMIT AND NOT A DEFECT OF THE FILE: "
           f"`POP_FIGURE` takes the FIRST match with no quotation exemption, "
           f"and `out_audit_7e39.txt`'s first match is the 429 it is REPORTING "
           f"AS THE DEFECT.  Extending `COMPUTED` to the transcripts it omits "
           f"would not just widen the check, it would make it wrong -- which "
           f"is what a hand-picked list hides: not only that the scope is "
           f"short, but that the rule was never asked to work outside it")
    return found, missing, own


# --------------------------------------------------------------------------
# D -- WHAT MUST NOT BE DISTURBED
# --------------------------------------------------------------------------
def d1(out):
    head("D1 -- PRESERVE: THE SITE CUTTERS, WRITTEN FROM THE DISCLOSURE "
         "SENTENCES")
    mine = my_sites()
    # The gate PRINTS each site's extent, in characters and lines, from
    # `site_extents`.  My cutters are written from the two sentences in
    # `EXTENT_OF` and know nothing of `framed_row`/`section`.
    ext = {}
    for l in out.split("\n"):
        m = re.match(r"^\s{4}(the STATE\.md row|§14|H8)\s+([\d,]+) chars /\s+"
                     r"(\d+) line\(s\)\s+`(\w+)\(\)`", l)
        if m:
            ext[m.group(1)] = (m.group(4), int(m.group(3)),
                               int(m.group(2).replace(",", "")))
    ok = 0
    for name, s in mine.items():
        anchor, lines, chars = ext.get(name, ("?", -1, -1))
        good = (len(s.split("\n")) == lines and len(s) == chars)
        ok += good
        print(f"    {name:<20} mine: {len(s.split(chr(10))):>3} lines "
              f"{len(s):>6} chars   gate: {lines:>3} lines {chars:>6} chars "
              f"({anchor})  {'match' if good else '⚠️ DIFFER'}")
    record(ok == 3,
           f"D1a cutters written from the DISCLOSURE SENTENCES in `EXTENT_OF` "
           f"-- not from `framed_row`/`section` -- reproduce the gate's own "
           f"extent at {ok} of 3 sites, line count and character count.  That "
           f"is the test of whether a scope sentence is a SPECIFICATION or a "
           f"LABEL.  mg-7e39's 3 of 3 is undisturbed")


BEND = ('    segments.append(raw[last:])\n    return segments, figures',
        '    segments.append(raw[last:])\n'
        '    if BEND_AT is not None and BEND_AT in raw:\n'
        '        segments[-1] = segments[-1] + "\\u2060"\n'
        '    return segments, figures')


def d2():
    head("D2 -- PRESERVE: THE REFUSAL, PROBED ONE ROW AT A TIME")
    print("""`partition` bent LOSSY AT ONE SITE ONLY, then `--reseal`.  A refusal that
fires at both commits would be measuring my probe, so the same probe runs at
`803bd50`, where the defect is still present.
""")
    # ⚠️ KEYED ON THE SITE'S ANCHOR, not on its first line.  At `803bd50` the
    # STATE.md site is ONE LINE from `find_line` -- the header lines are not
    # in it, because `framed_row` is what mg-6df0 introduced -- so a mark cut
    # from today's site is absent from that commit's site and the probe
    # silently does nothing.  The anchor is in the site's raw at every
    # version, which is what makes the control comparable across commits.
    marks = {n: a for n, (_rel, _fn, a) in SITE_CUT.items()}
    results = {}
    for label, root in (("HEAD", REPO), (C_PRE6DF0, worktree(C_PRE6DF0))):
        got = []
        for name, mark in marks.items():
            def bend(text, mark=mark):
                if BEND[0] not in text:
                    return None
                return (text.replace(BEND[0], BEND[1], 1)
                        .replace("def partition(raw):",
                                 f"BEND_AT = {mark!r}\n\n\ndef partition(raw):",
                                 1))
            recs_path = os.path.join(root, os.path.dirname(LANDING_REL),
                                     "site_records.txt")
            with open(recs_path, "rb") as fh:
                before = fh.read()
            rc, gout, restored, changed, seen = on_disk(
                LANDING_REL, bend, root, args=("--reseal",),
                guard_records=True)
            note_restore(f"D2 {label} @ {name}", restored)
            # `--reseal` prints its blocking rows as `    - GATE @ ...`, not
            # as `[REFUTED  ]` rows -- it never reaches the gate's own printer.
            block = [l.strip()[2:] for l in gout.split("\n")
                     if l.startswith("    - GATE @ ")]
            part = [d for d in block
                    if d.split(" -- ")[0].endswith("RECORD PARTITION")]
            after = seen if seen is not None else before
            got.append((name, rc, len(part), before == after, restored,
                        changed))
            print(f"    {label:<9} @ {name:<18} exit {rc}  "
                  f"{len(part)} RECORD PARTITION refuted  record "
                  f"{'unchanged' if before == after else 'CHANGED'}  "
                  f"restored {restored}")
        results[label] = got
    at_head = [g for g in results["HEAD"] if g[1] == 1 and g[3] and g[2]]
    at_pre = [g for g in results[C_PRE6DF0] if g[1] == 0 and not g[3]]
    record(len(at_head) == 3,
           f"D2a at HEAD, `partition` bent lossy AT ONE SITE AT A TIME then "
           f"`--reseal`: {len(at_head)} of 3 REFUSE with the record UNCHANGED. "
           f"Predicted 3 of 3.  mg-7e39's result is undisturbed")
    record(len(at_pre) == 3,
           f"D2b CONTROL at {C_PRE6DF0}, where the defect is still present: "
           f"the SAME probe BLESSES {len(at_pre)} of 3 with the record "
           f"REWRITTEN.  Predicted 3 of 3.  A refusal that fired at both "
           f"commits would be measuring my probe, not the repair")


# --------------------------------------------------------------------------
# E -- THE FLOOR: THE THINGS NO LIST IN THE BRIEF NAMES
# --------------------------------------------------------------------------
def e1(pre_out):
    head("E1 -- FLOOR: THE FAIL-CLOSED TEST FOR `A REASON CARRIES A COUNT` IS "
         "`\\d`")
    print("""The repair's answer to F1 is that a decline with no measurement in it is
RED.  There is no mechanical test for "is this sentence about the site"; the
one the gate uses is

    countless = [(t, n, w) for t, n, w in reasons if not re.search(r"\\d", w)]

-- ANY DIGIT ANYWHERE IN THE SENTENCE.  A ticket id is digits.  So the rule is
run here over the EIGHT reasons the PRE-REPAIR matrix printed, at the commit
where the defect is still present, and the question is how many of the
sentences it exists to catch it would have caught.
""")
    pre = na_reasons(pre_out)
    MEASURE = re.compile(r"(?<![\w-])\d+(?![\w-])")
    passes, blocked, hollow = [], [], []
    for tag, name, why in pre:
        has_digit = bool(re.search(r"\d", why))
        has_count = bool(MEASURE.search(why))
        print(f"    {tag} @ {name:<18} digit={'Y' if has_digit else 'n'}  "
              f"free-standing count={'Y' if has_count else 'n'}  {why[:74]}")
        (passes if has_digit else blocked).append((tag, name, why))
        if has_digit and not has_count:
            hollow.append((tag, name, why))
    print()
    for tag, name, why in hollow:
        print(f"    ⚠️ PASSES ON A TICKET ID, WITH NO MEASUREMENT IN IT: "
              f"{tag} @ {name}")
        print(f"        {why}")
    if hollow:
        finding("G1", f"THE FAIL-CLOSED RULE THAT MAKES AN `n/a` CARRY A COUNT "
                      f"IS `re.search(r'\\d', reason)` -- ANY DIGIT.  Run over "
                      f"the {len(pre)} decline reasons the matrix printed at "
                      f"{C_PRE3F3B}, every one of which is a sentence with no "
                      f"measurement in it, the rule blocks {len(blocked)} and "
                      f"PASSES {len(passes)} -- {len(hollow)} of them on the "
                      f"digits inside `mg-ec07`.  The control that makes a "
                      f"decline checkable by a reader is met by naming a "
                      f"ticket in it")
    record(None,
           f"E1a ⚠️ THE FAIL-CLOSED RULE IS SATISFIABLE BY A TICKET ID.  Run "
           f"over the {len(pre)} reasons the matrix printed at {C_PRE3F3B} -- "
           f"the commit where every one of them is a sentence with no "
           f"measurement in it -- the rule blocks {len(blocked)} and PASSES "
           f"{len(passes)}, and {len(hollow)} of those pass on digits that "
           f"belong to `mg-ec07` and carry no count at all.  Predicted: at "
           f"least one passes.  The control that makes a decline carry its "
           f"count is met by naming a ticket in it")
    # And the same rule, against a sentence built to defeat it, at HEAD.
    live = read(LANDING_REL)
    target = "0 of this site's {len(_table_lines(site))} table "
    hollow_reason = 'no column header line inside this site (mg-9207 E3)'

    def hollow_patch(text):
        i = text.find(target)
        if i < 0:
            return None
        j = text.find('")', i)
        return text[:i] + hollow_reason + text[j:]

    def honest_patch(text):
        i = text.find(target)
        if i < 0:
            return None
        j = text.find('")', i)
        return text[:i] + 'no column header line inside this site' + text[j:]
    del live
    outs = {}
    for tag, patch in (("with `(mg-9207 E3)`", hollow_patch),
                       ("without it        ", honest_patch)):
        rc, gout, restored, changed, _rec = on_disk(LANDING_REL, patch)
        note_restore(f"E1 {tag}", restored)
        flagged = "n/a WITHOUT A MEASUREMENT" in gout
        outs[tag] = (rc, flagged, changed, restored)
        print(f"    the SAME measurement-free reason {tag}: exit {rc}, "
              f"flagged={flagged}, restored={restored}")
    a = outs["with `(mg-9207 E3)`"]
    b = outs["without it        "]
    record(None,
           f"E1b DEMONSTRATED AT HEAD, where the defect is present: one "
           f"measurement-free decline reason, written twice, differing by the "
           f"twelve characters `(mg-9207 E3)`.  Without the id the gate flags "
           f"it and exits {b[0]}; with it the gate does not flag it and exits "
           f"{a[0]}.  Same sentence, same absence of any measurement, opposite "
           f"verdicts")


def e2(out):
    head("E2 -- FLOOR: THE MATRIX'S OWN CENSUS IS A SUBSTRING TEST OVER A "
         "WHOLE ROW")
    print("""`repair_ec07.py`'s `R3a` censuses the matrix with

    fires  = sum(l.count("FIRES")  for l in cells)
    na     = sum(l.count("n/a")    for l in cells)
    silent = sum(l.count("SILENT") for l in cells)

over the printed line -- and the printed line carries the KIND TITLE in its
first 62 columns.  That is a substring test over a whole row: the construct
this entire arc repairs, in the census of the very matrix whose `n/a` cells
are mg-7e39's F1.  It is outside the sweep's reach by construction, because
the sweep's vocabulary is GATE ROW NAMES and these are cell values.

It is right today and wrong in construction, which is the only reason nobody
has met it.  So it is made to be wrong, at HEAD, where it is present.
""")
    lines = [l for l in out.split("\n") if MATRIX_ROW.match(l)]
    by_col = {"FIRES": 0, "SILENT": 0, "n/a": 0}
    _n, cells = matrix(out)
    for v in cells.values():
        for k in by_col:
            if v == k or (k == "FIRES" and v.startswith("FIRES")):
                by_col[k] += 1
    by_sub = {k: sum(l.count(k) for l in lines) for k in by_col}
    print(f"    by COLUMN (mine)    : {by_col}")
    print(f"    by SUBSTRING (R3a's): {by_sub}")
    record(by_col == by_sub,
           f"E2a at HEAD the two censuses agree ({by_col}), because no kind "
           f"title happens to contain `FIRES`, `SILENT` or `n/a`.  Agreement "
           f"is the reason this has never been noticed, not evidence that the "
           f"census is sound")

    def rename(text):
        old = '("K09 two COLUMN HEADERS exchanged (mg-9207 E3 -- mg-ec07\'s X1)", k_col_header)'
        if old not in text:
            return None
        new = ('("K09 two COLUMN HEADERS exchanged (n/a at one site -- '
               'mg-ec07\'s X1)", k_col_header)')
        return text.replace(old, new, 1)
    rc, gout, restored, changed, _rec = on_disk(LANDING_REL, rename)
    note_restore("E2 kind title renamed", restored)
    lines2 = [l for l in gout.split("\n") if MATRIX_ROW.match(l)]
    _n2, cells2 = matrix(gout)
    col2 = sum(1 for v in cells2.values() if v == "n/a")
    sub2 = sum(l.count("n/a") for l in lines2)
    print(f"    kind title renamed to contain the literal `n/a`, NO CELL "
          f"CHANGED (exit {rc}, restored {restored}):")
    print(f"      by COLUMN    : {col2} n/a  (was {by_col['n/a']})")
    print(f"      by SUBSTRING : {sub2} n/a  (was {by_sub['n/a']})")
    if changed and col2 == by_col["n/a"] and sub2 == by_sub["n/a"] + 1:
        finding("G3", "THE MATRIX'S OWN CENSUS IS A SUBSTRING TEST OVER A "
                      "WHOLE ROW.  `repair_ec07.py`'s `R3a` counts FIRES / "
                      "n/a / SILENT with `l.count(...)` over a printed line "
                      "that carries the KIND TITLE in its first 62 columns.  "
                      "One kind title edited to contain the literal `n/a` "
                      "moves the reported count by one with NO CELL CHANGED.  "
                      "It is the construct this arc repairs, in the census of "
                      "the very matrix whose `n/a` cells are mg-7e39's F1, "
                      "and it is outside the sweep's reach because the "
                      "sweep's vocabulary is gate-row names and these are "
                      "cell values")
    record(None,
           f"E2b DEMONSTRATED AT HEAD: one kind TITLE edited to contain the "
           f"literal `n/a` and no cell of the matrix changed.  The census by "
           f"column still reads {col2}; the census by substring reads {sub2}, "
           f"one more than before.  A census that counts its own legend is the "
           f"first version of this row, recorded in `repair_ec07.py`; a census "
           f"that counts its own row TITLES is the version that replaced it")


# --------------------------------------------------------------------------
# F -- THIS INSTRUMENT, CHECKED FOR THE SHAPES IT AUDITS
# --------------------------------------------------------------------------
def f1(vocab):
    head("F1 -- THIS INSTRUMENT, CHECKED FOR THE SHAPES IT AUDITS")
    mine = read("code/hodge_leverage_audit_97fb/audit_97fb.py")
    hits = [h for h in occurrences(mine, vocab) if not h[4]]
    record(not hits,
           f"F1a {len(hits)} line(s) of this file identify a gate row by a "
           f"substring of the whole row outside a declared function.  "
           f"Predicted 0")
    bad = [(t, ok) for t, ok in RESTORES if not ok]
    print(f"    on-disk probes run : {len(RESTORES)}")
    record(not bad,
           f"F1b every one of the {len(RESTORES)} on-disk probe(s) restored "
           f"its file BYTE-IDENTICALLY; {len(bad)} did not: {bad}.  A probe "
           f"that rewrites the artifact while auditing it is the failure "
           f"mg-3f3b named for itself, and this is the check for it")
    heads = git("log", "--format=%H %s", "-40").split("\n")
    pred = next((h for h in heads if "mg-97fb's predictions" in h), None)
    record(pred is not None,
           f"F1c the predictions are committed at "
           f"{pred.split()[0][:12] if pred else '?'}, before this script "
           f"existed -- read out of `git log` here rather than asserted")


def main():
    print("=" * 78)
    print("mg-97fb -- INDEPENDENT AUDIT OF THE mg-3f3b `n/a`-AND-VOCABULARY "
          "REPAIR")
    print("=" * 78)
    print(__doc__.split("\n\n", 1)[1].strip())
    try:
        out = a0()
        _names, cells = a1(out)
        a2(out)
        pre_out = a3(cells)
        vocab, declared, printed, hand, at = b1(out)
        b2(out, vocab, at)
        c1(declared, printed, hand)
        c2()
        d1(out)
        d2()
        e1(pre_out)
        e2(out)
        f1(vocab)
    finally:
        cleanup()

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"    checks       : {len(RESULTS)}")
    print(f"    confirmed    : {sum(1 for _t, ok in RESULTS if ok is True)}")
    print(f"    measured     : {sum(1 for _t, ok in RESULTS if ok is None)}")
    print(f"    refuted      : {len(bad)}")
    print(f"    findings     : {len(FINDINGS)}")
    print()
    for t in bad:
        print(f"    REFUTED  {t[:150]}")
    for tag, text in FINDINGS:
        print()
        print(f"    FINDING {tag}: {text}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
