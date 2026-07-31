#!/usr/bin/env python3
"""mg-3f3b -- mg-7e39's four findings, repaired and controlled.

FOUR FINDINGS, AND THREE OF THEM ARE ONE SHAPE.  F1, F5 and F2 are each a
statement that READS AS A MEASUREMENT AND IS NOT ONE: an `n/a` reason that
describes the derivation in the grammar of a fact about the site, a sweep
vocabulary hand-listed where the gate prints one more name than the hand, and
a population figure carried in prose that was already wrong at the commit
which published it.  F3 is the parent's own finding one level up: the remedy
was applied at the line it was found on.

  F1  `n/a` IS WHERE A MATRIX HIDES.  A matrix reports FIRE / SILENT / n/a and
      only the first two are measured.  `K11 @ the STATE.md row` declines with
      "no line here has two runs of two or more spaces to shift" -- which is a
      fact about `k_layout`, not about the site.  The site is a MARKDOWN PIPE
      TABLE, whose alignment is the padding inside its cells; an independent
      shift of that padding FIRES, caught by SITE RECORD.

  F3  THE CONSTRUCT IS 1 TOUCHED OF 6.  `"NAME" in row` -- a substring test
      over a whole row where a heading was meant -- existed at 6 sites when
      mg-6df0 landed; it repaired 1 and dispositioned 5.  A DISPOSITION IS A
      REASON, NOT A REPAIR.

  F5  THE SWEEP'S VOCABULARY IS A HAND LIST.  `ROW_NAMES` names 5 by hand;
      the gate prints 6.  The name the hand list misses is `READ AT THE SITE`,
      and it is where the construct entered this arc.

  F2  THE POPULATION IS STALE AT ITS OWN COMMIT.  The committed transcript
      publishes "429 .py files swept"; the tree at the commit that ships that
      transcript holds 448, and so did the commit before it.  Not drift --
      WRONG WHEN WRITTEN.

WHAT THIS INSTRUMENT IS, AND WHAT IT IS NOT.  It does not re-implement the
gate.  It runs the REAL runner on disk as a SUBPROCESS, mutating the tree and
restoring it sha256-verified.  The five mutation derivations in S1 are MINE,
written from the KIND TITLES rather than from `verify_landing.py`'s code, so
"the artifact says n/a" and "no mutation of this kind exists here" are two
different statements that this file can disagree about.  Where a gate row must
be classified it is classified by its HEADING.

THE ORDER IS PART OF THE DELIVERABLE.  This file and `PREDICTIONS.md` are
committed BEFORE the repairs, against the artifact as mg-7e39 audited it, and
S6a re-derives that ordering from `git log` rather than asserting it.

  S1  F1: every `n/a` read as a CLAIM, and the one that is not, on disk --
      with the control that reverts the derivation alone.
  S2  F3: every occurrence of the construct, at all six, and what each one
      selects that it was never meant to.
  S3  F5: the vocabulary, DERIVED -- and shown to follow the gate rather than
      copy it.
  S4  F2: the population, re-derived AT THE COMMIT THAT PUBLISHES IT, from
      `git ls-tree` rather than from the working tree.
  S5  this deliverable checked for its own four shapes.
  S6  the ordering, from git.

Pure Python 3 + git.  No third-party packages.
"""

import ast
import hashlib
import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LANDING_DIR = os.path.join(REPO, "code", "hodge_leverage_landing_e1d0")
LANDING = os.path.join(LANDING_DIR, "verify_landing.py")
LANDING_REL = "code/hodge_leverage_landing_e1d0/verify_landing.py"
RECORDS_REL = "code/hodge_leverage_landing_e1d0/site_records.txt"

SWEEP_REL = "code/hodge_leverage_repair_6df0/repair_ec07.py"
SWEEP_OUT_REL = "code/hodge_leverage_repair_6df0/out_repair_6df0.txt"

STATE = "STATE.md"
DELIV = "docs/OneThird-Hodge-Side-Leverage.md"
HIST = "docs/state-history/attempt-mg-a3d4.md"

# Everything this instrument writes to and restores.  A dirty tree scoped to
# these is a REFUSAL: a restore over an uncommitted edit destroys it.
MUTATED = [STATE, DELIV, HIST, LANDING_REL, RECORDS_REL]

RESULTS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout


def read(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, text):
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def heading(row):
    """THE ROW'S HEADING -- everything before the ` -- ` that introduces its
    explanation.  The remedy under audit, used everywhere in this file that a
    gate row is identified, with ONE declared exception: `by_substring`, which
    performs the construct in order to measure it and says so."""
    return row.split(" -- ")[0]


def by_substring(rows, name):
    """⚠️ THE CONSTRUCT, COMMITTED ON PURPOSE AND IN EXACTLY ONE PLACE.

    A substring test over a whole row is the defect this arc is repairing.
    Measuring it requires performing it -- so it is performed here, once, in a
    function whose NAME says what it is, rather than written inline where a
    sweep can only tell it from the defect by a disposition keyed on its line
    number.  A REASON ON A LINE IS NOT A STRUCTURE."""
    return [r for r in rows if name in r]


def my_vocabulary():
    """THE GATE'S ROW HEADINGS, derived HERE from the rows the runner actually
    emits -- not read out of the sweep's `ROW_NAMES`, whose scope is the thing
    under test.  An instrument that takes its vocabulary from the artifact it
    is measuring cannot report that the artifact's vocabulary is too small."""
    rows = [d for _ok, d in V.figure_gate(V.site_texts(), measured_now())]
    out = set()
    for r in rows:
        m = re.match(r"GATE @ .+?: (?:'.*?' )?([A-Z][A-Z ]+[A-Z])", heading(r))
        if m:
            out.add(m.group(1).strip())
    return sorted(out)


def my_declared_vocabulary(src):
    """The gate's DECLARED row kinds, read here by AST -- my own parse, not a
    call into the sweep, whose scope is the thing under test."""
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "ROW_KINDS" for t in node.targets):
            return sorted(e.value for e in getattr(node.value, "elts", [])
                          if isinstance(e, ast.Constant))
    return []


def repaired_bindings(src, kindname):
    """Names bound by a REPAIRED comparison in `src` -- an assignment whose
    value calls `heading()`/`by_substring` about `kindname`.  Found by AST,
    because the repaired statements wrap across lines and a line-based finder
    reported the two that do wrap as having no binding at all."""
    out = set()
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return out
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Assign, ast.AugAssign)):
            continue
        val = node.value
        names = {getattr(n.func, "id", "") for n in ast.walk(val)
                 if isinstance(n, ast.Call)}
        names |= {getattr(n.func, "attr", "") for n in ast.walk(val)
                  if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute)}
        if not ({"heading", "by_substring"} & names):
            continue
        if not any(isinstance(c, ast.Constant) and c.value == kindname
                   for c in ast.walk(val)):
            continue
        tgts = node.targets if isinstance(node, ast.Assign) else [node.target]
        for t in tgts:
            for n in ast.walk(t):
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                    out.add(n.id)
    return out


def consumers(src, targets):
    """What reads those names: A RECORDED VERDICT (it reaches `record`,
    `assert` or an `==`) or a printed line.  The distinction is the whole of
    PREDICTIONS.md's third way this repair could be worse than what it
    replaces."""
    feeds = set()
    if not targets:
        return feeds
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return feeds
    def reads(node):
        return any(isinstance(n, ast.Name) and n.id in targets
                   and isinstance(n.ctx, ast.Load) for n in ast.walk(node))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fname = getattr(node.func, "id", "")
            if fname == "print" and reads(node):
                feeds.add("a printed line")
            elif fname in ("record", "assert_") and reads(node):
                feeds.add("A RECORDED VERDICT")
        elif isinstance(node, (ast.Assert, ast.Compare)) and reads(node):
            feeds.add("A RECORDED VERDICT")
    return feeds


def my_hits(rel, name):
    """Lines of `rel` that identify the gate row `name` by a substring test
    over a WHOLE ROW.  My rule, not the sweep's: the sweep's rule is scoped by
    the sweep's vocabulary, and the vocabulary is F5."""
    try:
        src = read(rel)
    except OSError:
        return []
    hv = set()
    for l in src.split("\n"):
        if "heading(" in l or "row_kind(" in l or '.split(" -- ")[0]' in l:
            m = re.match(r"\s*(\w+)\s*(?:=|\+=|\|=)", l)
            if m:
                hv.add(m.group(1))
    out = []
    for i, l in enumerate(src.split("\n"), 1):
        t = l.strip()
        if "heading(" in t or "row_kind(" in t or "by_substring(" in t:
            continue
        bare = re.sub(r"'[^']*'|`[^`]*`", "", t)
        m = re.search(rf'"{name}"\s+(?:not\s+)?in\s+(\w+)', bare)
        if m and m.group(1) not in hv:
            out.append((i, t))
    return out


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.REPO = REPO
    return mod


V = load_module(LANDING, "verify_landing_3f3b")
SWEEP = load_module(os.path.join(REPO, SWEEP_REL), "repair_ec07_3f3b")


def measured_now():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap":  V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


def run_runner():
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("VERIFY_", "HODGE_", "MG_"))}
    r = subprocess.run([sys.executable, LANDING], capture_output=True,
                       text=True, env=env, cwd=REPO)
    return r.returncode, r.stdout + r.stderr


def gate_row(out, site, kind):
    """The verdict of ONE named gate row for ONE site, or None if absent.
    Matched on the row's HEADING, never on the whole row."""
    want = f"GATE @ {site}: {kind}"
    for l in out.split("\n"):
        s = l.strip()
        if not s.startswith("["):
            continue
        body = s[s.index("]") + 2:]
        if heading(body) == want:
            return s.startswith("[CONFIRMED")
    return None


def refuted_rows(out):
    return [l.strip()[len("[REFUTED  ] "):]
            for l in out.split("\n") if l.strip().startswith("[REFUTED")]


def matrix_cells(out):
    """The runner's own KIND x SITE matrix, read out of its stdout: a dict
    keyed (kind tag, site name) -> the cell it printed.  Parsed from the table
    the runner prints, not recomputed here -- this is the ARTIFACT'S claim,
    and S1 measures it against a derivation of mine."""
    lines = out.split("\n")
    hdr = next((i for i, l in enumerate(lines)
                if l.strip().startswith("kind") and "STATE.md" in l), None)
    if hdr is None:
        return {}, {}
    names = [n for n, _p, _f, _a, _s in V.ANCHORS]
    cells = {}
    for l in lines[hdr + 1:]:
        m = re.match(r"\s{4}(K\d\d)\s", l)
        if not m:
            if l.strip() == "" and cells:
                break
            continue
        body = l[4 + 62:]
        for i, name in enumerate(names):
            cells[(m.group(1), name)] = body[i * 20:(i + 1) * 20].strip()
    reasons = {}
    for l in lines:
        m = re.match(r"\s+n/a\s+(K\d\d) @ (.+?)\s{2,}(.*\S)", l)
        if m:
            reasons[(m.group(1), m.group(2).strip())] = m.group(3)
    return cells, reasons


def probe_on_disk(rel, edit, runner=run_runner):
    """Apply `edit` to `rel`, run the real runner, restore, and report whether
    the restoration is sha256-identical."""
    before = read(rel)
    before_sha = sha(rel)
    new = edit(before)
    if new is None or new == before:
        return None, "PROBE NOT APPLIED", True
    write(rel, new)
    try:
        rc, out = runner()
    finally:
        write(rel, before)
    assert sha(rel) == before_sha, f"{rel}: restoration failed"
    return rc, out, sha(rel) == before_sha


# --------------------------------------------------------------------------
# WHICH STATE THIS RUN IS IN.  Each of the four repairs is detected by the
# STRUCTURE it introduces, never by the absence of the string it replaced: the
# repaired files QUOTE the constructs they removed, in docstrings, so an
# absence test reads a repaired tree as unrepaired (mg-6df0's own note).
# --------------------------------------------------------------------------
# ⚠️ KEYED ON THE MUTATION THE CLAUSE PERFORMS, not on a sentence describing
# it.  The repaired `k_layout` QUOTES its own old decline reason in its
# docstring, so a detector reading prose says PRE against a repaired artifact
# -- mg-6df0 met exactly this and wrote it down.
PIPE_CLAUSE = 'return site.replace(l, "|  " + l[2:], 1), None'
FIX_F1 = PIPE_CLAUSE in read(LANDING_REL)


def _row_names_is_derived():
    """`ROW_NAMES` bound to a CALL rather than to a list literal."""
    for node in ast.walk(ast.parse(read(SWEEP_REL))):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "ROW_NAMES" for t in node.targets):
            return isinstance(node.value, ast.Call)
    return False


FIX_F5 = _row_names_is_derived()

# The five sites mg-7e39 left live, by file.  Named here so that S2 reports
# them one at a time and a sixth appearing anywhere is undispositioned.
CONSTRUCT_SITES = [
    ("code/hodge_leverage_audit_835f/audit_a318_repair.py", "READ AT THE SITE",
     "mg-a318's audit -- the EARLIEST occurrence the sweep finds, and the one "
     "the hand list could not see because `READ AT THE SITE` is not in it"),
    ("code/hodge_leverage_audit_835f/audit_a318_repair.py", "WRITTEN ONCE",
     "⚠️ A SEVENTH, in nobody's population: `WRITTEN ONCE` is a gate row kind "
     "that neither the hand list of 5 nor a regex over the gate's `print` "
     "calls could see, because the row read `'{label}' is WRITTEN ONCE`.  It "
     "appeared the moment the vocabulary came from the gate's own declaration"),
    ("code/hodge_leverage_audit_8aae/audit_8916_repair.py", "FIGURE CENSUS",
     "mg-8aae's audit -- selects 6 gate rows where 3 were meant"),
    ("code/hodge_leverage_repair_8916/repair_835f.py", "FIGURE CENSUS",
     "mg-8916's instrument -- selects 6 gate rows where 3 were meant"),
    ("code/hodge_leverage_audit_ec07/audit_ec07.py", "SITE RECORD",
     "mg-ec07's audit, in the very check that RAISED E-5 -- it measures the "
     "construct, so the repair is to perform it in ONE DECLARED PLACE"),
    (SWEEP_REL, "SITE RECORD",
     "mg-6df0's own R1a -- the same measurement, the same repair"),
]


# --------------------------------------------------------------------------
# S0 -- PREFLIGHT
# --------------------------------------------------------------------------
def s0():
    head("S0 -- PREFLIGHT")
    dirty = [l[3:] for l in git("status", "--porcelain", "--",
                                *MUTATED).split("\n") if l.strip()]
    if dirty:
        print("  REFUSING TO RUN: uncommitted changes to files this")
        print("  instrument mutates and restores.  A restore over an")
        print("  uncommitted edit destroys it.")
        for d in dirty:
            print(f"    {d}")
        raise SystemExit(2)
    rc, out = run_runner()
    print(f"    HEAD                     : {git('rev-parse', 'HEAD').strip()[:12]}")
    print(f"    the runner, unmutated    : exit {rc}")
    for tag, ok in (("F1 (pipe-table alignment)", FIX_F1),
                    ("F5 (derived vocabulary) ", FIX_F5)):
        print(f"    {tag} : {'POST -- repaired' if ok else 'PRE  -- as audited'}")
    record(rc == 0, f"S0a the runner is green on the unmutated tree "
                    f"(exit {rc}), so every fire below is attributable to a "
                    f"probe of this instrument's and to nothing standing")
    return out


# --------------------------------------------------------------------------
# S1 -- F1: EVERY `n/a` READ AS A CLAIM ABOUT THE SITE
#
# The five derivations below are MINE.  They are written from the KIND TITLES
# the artifact prints -- "two table ROW LABELS exchanged", "the table's
# ALIGNMENT shifted" -- and not from `verify_landing.py`'s code, which is the
# only way "the artifact declines here" and "nothing of this kind exists here"
# can be two statements rather than one.
# --------------------------------------------------------------------------
FIGURE = re.compile(r"(?<![\w−+])(?:[−+]?\d{1,3}(?: \d{3})+|[−+]\d{3,})(?!\d)")


def pipe_rows(site):
    """The lines of `site` that are rows of a markdown pipe table, and the
    lines that are its DELIMITER (`|---|---|`), kept apart: a delimiter's
    padding is its alignment specifier and moving it changes meaning."""
    rows, delims = [], []
    for l in site.split("\n"):
        if l.startswith("|") and l.count("|") >= 3:
            (delims if re.fullmatch(r"\|[\s:|-]+\|", l.strip()) else
             rows).append(l)
    return rows, delims


def cells_of(row):
    return row.strip().strip("|").split("|")


def my_k08(site):
    """K08 -- two table ROW LABELS exchanged.  The label is a row's FIRST cell;
    two rows are needed and each must carry a figure, or the exchange moves no
    figure's attachment."""
    rows, _d = pipe_rows(site)
    carrying = [r for r in rows if FIGURE.search(r)]
    if len(carrying) < 2:
        return None, (f"{len(carrying)} of {len(rows)} pipe-table row(s) at "
                      f"this site carry a figure, and an exchange needs two")
    a, b = carrying[0], carrying[1]
    ca, cb = cells_of(a), cells_of(b)
    if ca[0] == cb[0]:
        return None, (f"the {len(carrying)} figure-carrying rows here share "
                      f"one label, so exchanging labels changes nothing")
    new_a = a.replace(ca[0], cb[0], 1)
    new_b = b.replace(cb[0], ca[0], 1)
    return site.replace(a, new_a, 1).replace(b, new_b, 1), None


def my_k09(site):
    """K09 -- two COLUMN HEADERS exchanged.  The header line is the pipe-table
    line immediately above a delimiter line."""
    lines = site.split("\n")
    hdrs = [i for i, l in enumerate(lines[:-1])
            if l.startswith("|") and
            re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip())]
    if not hdrs:
        return None, (f"0 of {len(lines)} line(s) at this site is a pipe-table "
                      f"header (a row directly above a delimiter line)")
    i = hdrs[0]
    c = cells_of(lines[i])
    if len(c) < 2 or c[0].strip() == c[1].strip():
        return None, (f"the header line here has {len(c)} distinguishable "
                      f"column(s), and an exchange needs two")
    lines[i] = "|" + "|".join([c[1], c[0]] + c[2:]) + "|"
    return "\n".join(lines), None


# A MARKED QUOTATION is text a reader is told belongs to somebody else.
# ⚠️ MARKDOWN EMPHASIS IS NOT ONE, and this list carried `*...*` on its first
# run.  That pattern matched ACROSS `**bold**` markers, so `**+1 630**` read as
# a quoted figure and this file reported the artifact's K10 declines at H8 and
# at the STATE.md row as two more instances of F1.  THEY WERE MINE.  Reading
# an `n/a` as a claim cuts both ways: a sloppy independent derivation
# manufactures a finding exactly as easily as a narrow one hides a cell.  The
# miss is kept in PREDICTIONS.md and stated in the report.
QUOTE = [re.compile(r"\*\"(.+?)\"\*", re.S), re.compile(r"\*'(.+?)'\*", re.S),
         re.compile(r"“(.+?)”", re.S)]


def my_k10(site):
    """K10 -- a figure inside a MARKED QUOTATION altered.  A quotation is text
    a reader is told belongs to someone else; a figure inside one is the
    hardest kind to notice moving."""
    spans = sorted((m.start(1), m.end(1)) for p in QUOTE for m in p.finditer(site))
    n = 0
    for s, e in spans:
        m = FIGURE.search(site[s:e])
        n += 1
        if m:
            tok = m.group()
            bad = tok[:-1] + ("8" if tok[-1] != "8" else "7")
            return site[:s] + site[s:e].replace(tok, bad, 1) + site[e:], None
    return None, (f"{n} marked quotation(s) at this site and none carries a "
                  f"figure token")


def my_k11(site):
    """K11 -- the table's ALIGNMENT shifted, no figure moved.

    IN EITHER TABLE FORMAT, which is the whole of F1.  A whitespace-column
    table is aligned by runs of spaces between its columns; A MARKDOWN PIPE
    TABLE IS ALIGNED BY THE PADDING INSIDE ITS CELLS.  A derivation that knows
    only the first declines at a pipe table and reports it as a fact about the
    site."""
    for l in site.split("\n"):
        runs = list(re.finditer(r"\S(  +)\S", l))
        if len(runs) >= 2:
            a, b = runs[0].span(1), runs[1].span(1)
            new = (l[:a[0]] + " " * (a[1] - a[0] - 1) + l[a[1]:b[0]]
                   + " " * (b[1] - b[0] + 1) + l[b[1]:])
            return site.replace(l, new, 1), None
    rows, _d = pipe_rows(site)
    for l in rows:
        if l.startswith("| ") and site.count(l) == 1:
            return site.replace(l, "|  " + l[2:], 1), None
    return None, (f"0 of {len(site.split(chr(10)))} line(s) at this site is a "
                  f"table row whose alignment can shift, in either format")


def my_k12(site):
    """K12 -- a whole PARAGRAPH relocated out of the site."""
    paras = site.split("\n\n")
    free = [p for p in paras[1:] if p.strip() and not FIGURE.search(p)]
    if not free:
        return None, (f"this site is {len(paras)} paragraph(s) and 0 after the "
                      f"first are figure-free, so there is nothing to relocate "
                      f"out of it")
    return site.replace("\n\n" + free[0], "", 1), None


MY_KINDS = {"K08": my_k08, "K09": my_k09, "K10": my_k10,
            "K11": my_k11, "K12": my_k12}


def apply_my_kind(tag, name, base_files):
    """My mutation of kind `tag` at site `name`, spliced into THE FILE through
    the artifact's own write-back, then the sites re-cut from the file."""
    fn = MY_KINDS[tag]
    base = V.texts_from(base_files)
    new_site, why = fn(base[name])
    if new_site is None or new_site == base[name]:
        return None, why or (f"the derivation returned the site unchanged at "
                             f"all {len(base[name])} of its characters")
    files = V.with_site(base_files, name, new_site)
    if files is None:
        return None, (f"the mutation is {len(new_site.splitlines())} line(s) "
                      f"where the site is {len(base[name].splitlines())}, so "
                      f"it cannot be written back into the file")
    return files, None


def s1(base_out):
    head("S1 -- F1: EVERY `n/a` READ AS A CLAIM ABOUT THE SITE")
    print("""A matrix reports FIRE / SILENT / n/a, and only the first two are measured.
`n/a` is prose.  It is printed in the grammar of a fact about the SITE -- "no
line here has ..." -- and it can equally be a fact about the DERIVATION, in
which case a matrix that reads as complete is hiding a cell.

So every `n/a` the runner prints is read here as a CLAIM and tried with a
mutation of the same kind derived from the KIND TITLE, written in this file.
""")
    cells, reasons = matrix_cells(base_out)
    if not cells:
        record(False, "S1 the runner's matrix could not be parsed out of its "
                      "stdout -- nothing below is measured")
        return
    na = sorted(k for k, v in cells.items() if v == "n/a")
    fires = sorted(k for k, v in cells.items() if v.startswith("FIRES"))
    print(f"    cells in the product     : {len(cells)}")
    print(f"    the artifact says FIRES  : {len(fires)}")
    print(f"    the artifact says n/a    : {len(na)}")
    print()

    # --- S1a: the RULE.  A reason with no count is a sentence, not a
    # measurement.  This is mechanically checkable and the whole of F1's
    # general lesson.
    countless = [(k, reasons.get(k, "")) for k in na
                 if not re.search(r"\d", reasons.get(k, ""))]
    for k in na:
        why = reasons.get(k, "(no reason printed)")
        mark = "  " if re.search(r"\d", why) else "⚠️"
        print(f"    {mark} n/a  {k[0]} @ {k[1]:<18} {why[:96]}")
    print()
    record(not countless,
           f"S1a of the {len(na)} `n/a` reason(s) the runner prints, "
           f"{len(na) - len(countless)} carry a COUNT MEASURED AT THE SITE and "
           f"{len(countless)} are sentences with no measurement in them.  A "
           f"reason with no count cannot be checked by a reader, which is what "
           f"lets a fact about the derivation wear the grammar of a fact about "
           f"the site")

    # --- S1b: every n/a cell tried with MY derivation of the same kind.
    base_files = V.files_now()
    disagree, agree, unbuildable = [], [], []
    for tag, name in na:
        if tag not in MY_KINDS:
            unbuildable.append((tag, name, "no independent derivation written "
                                           "here for this kind"))
            continue
        files, why = apply_my_kind(tag, name, base_files)
        if files is None:
            agree.append((tag, name, why))
            print(f"       agree  {tag} @ {name:<18} mine declines too: {why[:70]}")
            continue
        path = [p for _n, p, _f, _a, _s in V.ANCHORS if _n == name][0]
        rc, out, _ok = probe_on_disk(path, lambda _s, f=files, p=path: f[p])
        rows = refuted_rows(out)
        rec = any(heading(d).endswith("SITE RECORD") for d in rows)
        fig = not any(heading(d).endswith(("FIGURE CENSUS", "FIGURE ORDER"))
                      for d in rows)
        disagree.append((tag, name, rc, rec, fig))
        print(f"    ⚠️ DIFFER {tag} @ {name:<18} the artifact says n/a; my "
              f"mutation of the same kind -> exit {rc}, "
              f"{'SITE RECORD refuted' if rec else 'SITE RECORD green'}, "
              f"{'every figure row green' if fig else 'a FIGURE row also fired'}")
    print()
    record(not disagree,
           f"S1b of the artifact's {len(na)} `n/a` cell(s), {len(agree)} are "
           f"also declined by a derivation written independently from the kind "
           f"title, {len(disagree)} are NOT, and {len(unbuildable)} have no "
           f"independent derivation here.  A cell that is n/a for one "
           f"derivation and applicable for another is a fact about the "
           f"DERIVATION printed in the grammar of a fact about the SITE")

    # --- S1c: K11 @ the STATE.md row, the cell mg-7e39 named, on disk.
    name = "the STATE.md row"
    files, why = apply_my_kind("K11", name, base_files)
    if files is None:
        record(False, f"S1c K11 @ {name}: my own pipe-table alignment shift "
                      f"could not be derived ({why}) -- the probe below is "
                      f"not evidence of anything")
    else:
        path = [p for _n, p, _f, _a, _s in V.ANCHORS if _n == name][0]
        rc, out, restored = probe_on_disk(path, lambda _s, f=files, p=path: f[p])
        rows = refuted_rows(out)
        rec = [d for d in rows if heading(d).endswith("SITE RECORD")]
        figs = [d for d in rows if heading(d).endswith(("FIGURE CENSUS",
                                                        "FIGURE ORDER"))]
        record(rc == 1 and rec and not figs,
               f"S1c K11 @ {name} ON DISK: the site's pipe-table padding "
               f"shifted by one space, NO FIGURE MOVED -> exit {rc}, "
               f"{len(rec)} SITE RECORD row(s) refuted and {len(figs)} FIGURE "
               f"row(s).  The gate catches it; only the matrix said there was "
               f"nothing here to catch.  Restored byte-identical: {restored}")

    # --- S1d: the artifact's own cell, before and after.
    cell = cells.get(("K11", name))
    record(cell is not None and cell.startswith("FIRES") if FIX_F1
           else cell == "n/a",
           f"S1d the artifact's own matrix at K11 @ {name} reads "
           f"{cell!r}.  PREDICTED "
           f"{'FIRES -- the derivation now covers the pipe-table format' if FIX_F1 else 'n/a -- this is the state mg-7e39 audited'}")

    # --- S1e: the control.  Revert the derivation alone.
    if FIX_F1:
        def strip_pipe_clause(src):
            """`k_layout` REVERTED TO ITS PRE-REPAIR DERIVATION, and nothing
            else in the file touched.  Located by AST rather than by matching
            text, so the control is keyed on the FUNCTION and not on a string
            that a docstring could also contain.

            ⚠️ The clause and its decline reason go together: the reason
            COUNTS what the clause looked for (`{len(once)} of {len(pipe)}`),
            so removing the statements and leaving the sentence is not the
            pre-repair state -- it is a NameError.  Reverting a derivation
            means reverting what it says about itself."""
            tree = ast.parse(src)
            fn = next((n for n in ast.walk(tree)
                       if isinstance(n, ast.FunctionDef)
                       and n.name == "k_layout"), None)
            if fn is None:
                return None
            lines = src.split("\n")
            cut = next((i for i in range(fn.lineno - 1, fn.end_lineno)
                        if lines[i].startswith("    pipe = ")), None)
            if cut is None:
                return None
            old = ('    return None, "no line here has two runs of two or '
                   'more spaces to shift"')
            return "\n".join(lines[:cut] + [old] + lines[fn.end_lineno:])

        rc, out, restored = probe_on_disk(LANDING_REL, strip_pipe_clause)
        if rc is None:
            record(False, "S1e the control could not be applied: the "
                          "pipe-table clause was not found where expected, so "
                          "S1d is uncontrolled")
        else:
            back, _r = matrix_cells(out)
            got = back.get(("K11", name))
            record(got == "n/a",
                   f"S1e CONTROL: the pipe-table clause of `k_layout` removed "
                   f"and NOTHING ELSE -- K11 @ {name} reads {got!r} again "
                   f"(exit {rc}).  The cell moves with that clause, so the "
                   f"clause is what is doing the work.  Restored "
                   f"byte-identical: {restored}")
    else:
        record(None, "S1e the control is not applicable in the PRE state: "
                     "there is no clause to revert yet")


# --------------------------------------------------------------------------
# S2 -- F3: THE CONSTRUCT, AT ALL SIX
# --------------------------------------------------------------------------
def s2():
    head("S2 -- F3: THE CONSTRUCT, AT ALL SIX")
    print("""mg-6df0 found the construct at 6 sites, repaired 1 and gave the other 5 a
DISPOSITION KEYED ON ITS EXACT LINE.  A disposition makes a new occurrence
red; it does not make an existing one right.  1 of 6 is the scope the repair
chose, and the parent's own finding is that a fix applied where the defect was
FOUND rather than where it OCCURS is a fix with a scope nobody chose.

Two of the five PERFORM the construct in order to MEASURE it.  For those the
repair is not `heading()` -- that would delete the measurement -- it is to
perform it in ONE DECLARED FUNCTION, so a sweep meets a name instead of a line
number.
""")
    rows = [d for _ok, d in V.figure_gate(V.site_texts(), measured_now())]
    live, repaired = [], []
    for rel, kindname, note in CONSTRUCT_SITES:
        found = my_hits(rel, kindname)
        sub = len(by_substring(rows, kindname))
        hd = len([r for r in rows if heading(r).endswith(kindname)])
        print(f"    {rel}")
        print(f"        {note}")
        print(f"        '{kindname}' over the {len(rows)} live gate rows: "
              f"{sub} by substring, {hd} by heading "
              f"-- {sub - hd} row(s) it was never meant to select")
        if found:
            for ln, s in found:
                print(f"        :{ln}  {s[:88]}")
                print(f"        -> LIVE")
            live.append(rel)
        else:
            print(f"        -> REPAIRED: no line in this file identifies a "
                  f"gate row by a substring of the whole row")
            repaired.append(rel)
    print()
    theirs = [c for c in CONSTRUCT_SITES if not c[2].startswith("⚠️")]
    record(not live,
           f"S2a {len(repaired)} of {len(CONSTRUCT_SITES)} occurrence(s) are "
           f"repaired and {len(live)} remain.  Predicted 0 remaining.  "
           f"{len(theirs)} of them are the ones mg-7e39 measured live in the "
           f"commit mg-6df0 landed in; "
           f"{len(CONSTRUCT_SITES) - len(theirs)} is a SEVENTH that appeared "
           f"only once the vocabulary came from the gate's own declaration.  "
           f"The two numbers mg-7e39 asked for were 1 touched of 6; the two "
           f"this run reports are {len(repaired)} of "
           f"{len(theirs) + 1} known when it started")

    # WHAT THE REPAIR MOVED IN SOMEBODY ELSE'S INSTRUMENT.  Three of the five
    # sites are other deliverables' shipped instruments under committed
    # transcripts.  PREDICTIONS.md named the way this repair could be WORSE
    # than the disposition it replaces: if `heading()` moves a VERDICT rather
    # than a printed line, it has silently rewritten another deliverable's
    # evidence.  So the consumer of each repaired binding is classified.
    print()
    verdicts = []
    for rel, kindname, _note in CONSTRUCT_SITES:
        try:
            src = read(rel)
        except OSError:
            continue
        targets = repaired_bindings(src, kindname)
        feeds = consumers(src, targets)
        what = ", ".join(sorted(feeds)) or "nothing this rule can see"
        print(f"    {rel}  ({kindname})")
        print(f"        the repaired binding(s) {sorted(targets)} feed: {what}")
        if "A RECORDED VERDICT" in feeds:
            verdicts.append(rel)
    verdicts = sorted(set(verdicts))
    record(None,
           f"S2d {len(verdicts)} of {len(CONSTRUCT_SITES)} repaired site(s) "
           f"feed a RECORDED VERDICT rather than only a printed line: "
           f"{verdicts}.  Those are re-run BY HAND at this tree and the "
           f"verdicts compared to the committed transcript -- "
           f"`out_a318_rerun.txt`, 12 of 12 and 10 of 12 before and after.  "
           f"The rest feed a `print` of one example row.  A repair inside "
           f"another deliverable's instrument that moves its verdict has "
           f"rewritten its evidence, which is worse than the disposition it "
           f"replaces")

    # The declared measuring sites, found by STRUCTURE rather than by line.
    declared = []
    for rel in {r for r, _k, _n in CONSTRUCT_SITES} | {
            SWEEP_REL, MINE, "code/hodge_leverage_audit_7e39/audit_7e39.py"}:
        try:
            src = read(rel)
        except OSError:
            continue
        if "def by_substring(" not in src:
            continue
        calls = [i for i, l in enumerate(src.split("\n"), 1)
                 if re.search(r"\bby_substring\(", l)
                 and not l.strip().startswith("def ")]
        declared.append((rel, calls))
    for rel, calls in sorted(declared):
        print(f"    DECLARED MEASUREMENT  {rel}  "
              f"definition + {len(calls)} call site(s) at "
              f"{', '.join(str(c) for c in calls)}")
    record(bool(declared),
           f"S2b {len(declared)} file(s) perform the construct through a "
           f"DECLARED function whose name is what it does, found here by "
           f"searching for the name rather than by reading a disposition "
           f"table.  A structure a sweep can see is not the same object as a "
           f"reason a reader must be handed")

    # And the whole tree, by the parent's own rule with the derived vocabulary.
    files = SWEEP.py_files()
    vocab = my_declared_vocabulary(read(LANDING_REL)) or my_vocabulary()
    allhits = sorted({(rel, ln, t) for rel in files for nm in vocab
                      for ln, t in my_hits(rel, nm)})
    undisp = [(rel, ln, t) for rel, ln, t in allhits
              if not SWEEP.DISPOSITIONS.get((rel, t))]
    for rel, ln, t in allhits:
        print(f"    still in the tree     {rel}:{ln}  {t[:70]}")
    record(not allhits,
           f"S2c the whole tree -- {len(files)} .py files under `code/` in "
           f"the working tree -- swept by MY rule over MY vocabulary of "
           f"{len(vocab)}: {len(allhits)} line(s) identify a gate row by a "
           f"substring test over the whole row, {len(undisp)} of them without "
           f"even a disposition.  Predicted 0 and 0.  A disposition table with "
           f"nothing in it is the repair; a disposition table with four rows "
           f"in it and a fifth occurrence its vocabulary cannot see is the "
           f"finding")


# --------------------------------------------------------------------------
# S3 -- F5: THE VOCABULARY, DERIVED
# --------------------------------------------------------------------------
def s3():
    head("S3 -- F5: THE VOCABULARY, DERIVED FROM WHAT THE GATE PRINTS")
    print("""The sweep exists because a hand-picked SITE is a scope nobody chose.  It then
picked its VOCABULARY the same way: `ROW_NAMES`, five headings written out by
hand, against a gate with SEVEN row kinds.  The lesson transferred to the axis
it was learned on and not to the next one -- and mg-7e39 measured the gap with
a regex over the gate's `print` calls, which sees six.  A derived vocabulary
derived from the wrong thing is a hand list with extra steps, so the gate
DECLARES the vocabulary and fails closed on a row that does not use it.
""")
    src = read(LANDING_REL)
    hand = ["SITE RECORD", "RECORD PARTITION", "FIGURE CENSUS",
            "FIGURE ORDER", "CENSUS ROSTER"]
    printed = my_declared_vocabulary(src)
    live = my_vocabulary()
    now = list(SWEEP.ROW_NAMES)
    stray = sorted(set(live) - set(printed))
    print(f"    the gate DECLARES         : {printed}")
    print(f"    its live rows use         : {live}"
          + (f"   ⚠️ undeclared: {stray}" if stray else ""))
    print(f"    mg-6df0's hand list       : {hand}")
    print(f"    the sweep uses            : {now}")
    print(f"    in the gate and not in the hand list: "
          f"{sorted(set(printed) - set(hand))}")
    record(sorted(now) == printed and not stray,
           f"S3a the sweep's vocabulary is {len(now)} name(s) and the gate "
           f"DECLARES {len(printed)}; they are "
           f"{'THE SAME SET' if sorted(now) == printed else 'DIFFERENT SETS'}, "
           f"and {len(stray)} of the kinds its live rows use are undeclared.  "
           f"The hand list is {len(hand)} and misses "
           f"{sorted(set(printed) - set(hand))} -- ⚠️ TWO names, not one: "
           f"mg-7e39 measured the gap against a vocabulary regexed out of the "
           f"gate's `print` calls, which could not see `WRITTEN ONCE` because "
           f"that row read `'{{label}}' is WRITTEN ONCE`.  A derived "
           f"vocabulary derived from the wrong thing is a hand list with extra "
           f"steps")

    # DERIVED, not copied: rename a row in a COPY of the gate's source and the
    # derivation must follow it.  A hand list cannot.
    if FIX_F5:
        probe = src.replace('    "CENSUS ROSTER",', '    "CENSUS MANIFEST",')
        moved = set(SWEEP.row_vocabulary(probe))
        followed = moved >= {"CENSUS MANIFEST"} and not moved & {"CENSUS ROSTER"}
        record(followed,
               f"S3b DERIVED RATHER THAN COPIED: one row heading renamed in a "
               f"COPY of the gate's source and the sweep's vocabulary follows "
               f"it -- `CENSUS ROSTER` -> `CENSUS MANIFEST` gives "
               f"{sorted(moved)}.  A "
               f"hand list returns the same five whatever the gate prints, "
               f"which is what makes it a scope nobody chose")
        empty_ok = False
        try:
            SWEEP.row_vocabulary("# a source that prints no gate rows\n")
        except SystemExit:
            empty_ok = True
        record(empty_ok,
               "S3c FAIL-CLOSED: a source from which no row heading can be "
               "derived is a REFUSAL, not an empty vocabulary.  A sweep with "
               "an empty vocabulary finds nothing and reads exactly like a "
               "tree with nothing in it -- which is F1's shape on this axis")
    else:
        record(None, "S3b/S3c not applicable in the PRE state: the vocabulary "
                     "is a literal, so there is nothing for a rename to move")

    # What the extra name actually finds.
    extra = sorted(set(printed) - set(hand))
    found = sorted({(rel, ln, t) for rel in SWEEP.py_files() for nm in extra
                    for ln, t in my_hits(rel, nm)})
    for rel, ln, t in found:
        print(f"    the hand list could not see  {rel}:{ln}  {t[:70]}")
    record(None,
           f"S3d with {extra} in the vocabulary the same rule finds "
           f"{len(found)} occurrence(s) the hand list cannot see.  mg-7e39 "
           f"measured 1 at `audit_a318_repair.py:326`, the earliest occurrence "
           f"in the arc; this run finds {len(found)} because that line is "
           f"repaired above")


# --------------------------------------------------------------------------
# S4 -- F2: THE POPULATION, AT THE COMMIT THAT PUBLISHES IT
# --------------------------------------------------------------------------
POP_FIGURE = re.compile(r"(\d[\d,  ]*)\s*`?\.py`?\s+files")

# A figure inside a QUOTATION is being discussed, not asserted -- the same
# convention `repair_ec07.py` already uses for the scope sentence.  It is what
# lets a correction note state the wrong figure it is correcting without the
# rule reading the note as a fresh copy of it.  ⚠️ ONE rule with no exceptions,
# rather than a skip-list of files or of phrasings: a list of things not to
# look at is a scope nobody chose, which is the finding.
QUOTATION = re.compile(r'"[^"]*"|“[^”]*”')


def py_files_at(rev):
    """Every `.py` under `code/` IN THE TREE AT `rev` -- from `git ls-tree`,
    not from the working directory.  The working directory is a different
    object from the commit that publishes a figure, and confusing the two is
    exactly how 429 came to be committed beside a tree of 448."""
    out = git("ls-tree", "-r", "--name-only", rev, "code/")
    return sorted(p for p in out.split("\n") if p.endswith(".py"))


def publishing_commit(rel):
    """The commit that last changed `rel` -- the commit whose tree a figure
    inside `rel` is a figure ABOUT.  None when the file has never been
    committed.

    ⚠️ THE WORKING TREE IS DELIBERATELY IGNORED.  What a reader meets is what
    is PUBLISHED, and an uncommitted regeneration is not published.  An earlier
    version of this returned None whenever the file was dirty, which made this
    deliverable's own transcript permanently exempt: every run rewrites it (it
    embeds HEAD), so it was always dirty and the row always read "not yet
    published".  A check that is structurally unable to fail on its author is
    the shape this whole deliverable is about."""
    return git("log", "-1", "--format=%H", "--", rel).strip() or None


# Every place in this arc that PUBLISHES a `.py` population for the sweep.
# Transcripts are computed by the publication step; prose must POINT rather
# than carry, because prose has no publication step to recompute it.
COMPUTED = [SWEEP_OUT_REL, "code/hodge_leverage_repair_3f3b/out_repair_3f3b.txt"]
PROSE = ["code/hodge_leverage_repair_6df0/README.md",
         "docs/OneThird-Hodge-Side-Leverage-Mg9207RepairAudit-Repair.md",
         "code/hodge_leverage_repair_3f3b/README.md",
         "docs/OneThird-Hodge-Side-Leverage-Mg6df0RepairAudit-Repair.md"]


def s4():
    head("S4 -- F2: THE POPULATION, RE-DERIVED AT THE COMMIT THAT PUBLISHES IT")
    print(""""429 .py files swept" was not a figure that went stale.  The tree at the
commit which SHIPS that transcript holds 448, and so did the commit before it:
19 files were in the population and not in the number on the day it was
written.  The instrument was live and re-derived the count every run -- what
was frozen was the figure in the evidence, which is the one a reader meets.

So the count is re-derived here FROM `git ls-tree` AT A NAMED COMMIT, and the
two ways a figure can be published are separated: a TRANSCRIPT is recomputed
by the publication step, and PROSE must point at a transcript rather than
carry a number, because prose has no publication step.
""")
    head_rev = git("rev-parse", "HEAD").strip()
    parent = git("rev-parse", "HEAD^").strip()
    landing_rev = "77306a7"
    for label, rev in (("77306a7 (mg-6df0 landed)", landing_rev),
                       ("803bd50 (its parent)   ", "803bd50"),
                       (f"HEAD^  {parent[:7]}      ", parent),
                       (f"HEAD   {head_rev[:7]}      ", head_rev)):
        n = len(py_files_at(rev))
        print(f"    .py under code/ at {label} : {n}")
    print(f"    .py under code/ in the WORKING TREE       : "
          f"{len(SWEEP.py_files())}")
    print()

    # ⚠️ EACH TRANSCRIPT IS READ FROM GIT, NOT FROM THE WORKING TREE.  That is
    # what "the commit that publishes it" means -- and it is also the only way
    # this check can see THIS instrument's own transcript, which is truncated
    # on disk by the redirect that is about to write it.  A check that cannot
    # be applied to its author is a check with a scope nobody chose.
    stale, unpublished = [], []
    for rel in COMPUTED:
        rev = publishing_commit(rel)
        if rev is None:
            unpublished.append(rel)
            print(f"    -- {rel}")
            print(f"        NEVER COMMITTED, so nothing is published yet.  "
                  f"This row becomes a measurement at the commit that lands it")
            continue
        text = git("show", f"{rev}:{rel}")
        m = POP_FIGURE.search(text)
        if not m:
            print(f"    -- {rel}: publishes no population figure at {rev[:12]}")
            continue
        said = int(re.sub(r"\D", "", m.group(1)))
        have = len(py_files_at(rev))
        mark = "  " if said == have else "⚠️"
        print(f"    {mark} {rel}")
        print(f"        publishes {said}, and the tree at {rev[:12]} -- the "
              f"commit that last wrote it -- holds {have}")
        if said != have:
            stale.append((rel, said, have, rev))
    print()
    record(not stale,
           f"S4a of the {len(COMPUTED) - len(unpublished)} committed "
           f"transcript(s) that publish a `.py` population, {len(stale)} "
           f"disagree with the tree AT THE "
           f"COMMIT THAT PUBLISHES THEM.  This is the check mg-7e39's F2 is "
           f"the failure of, and it is keyed on each transcript's OWN "
           f"publishing commit rather than on HEAD -- so a merge that lands "
           f"elsewhere cannot make it red, and a transcript committed beside a "
           f"tree it does not describe cannot make it green.  "
           f"{len(unpublished)} are not yet published at any commit and are "
           f"named rather than counted as passes")

    carried = []
    for rel in PROSE:
        try:
            text = read(rel)
        except OSError:
            continue
        for i, l in enumerate(text.split("\n"), 1):
            for m in POP_FIGURE.finditer(QUOTATION.sub("", l)):
                carried.append((rel, i, l.strip()[:88]))
    for rel, i, l in carried:
        print(f"    ⚠️ CARRIED IN PROSE  {rel}:{i}  {l}")
    record(not carried,
           f"S4b {len(carried)} population figure(s) are CARRIED as a number "
           f"in the {len(PROSE)} prose file(s) this arc publishes for the "
           f"sweep.  Predicted 0: prose points at the transcript line, because "
           f"a number in prose has no publication step that recomputes it and "
           f"goes stale silently at the next merge.  A figure inside a "
           f"QUOTATION is exempt, and that is ONE rule rather than a "
           f"skip-list -- it is how a correction note states the figure it "
           f"corrects")

    # The parent's figure, as a historical fact, stated from git rather than
    # quoted from the audit.
    at_landing = len(py_files_at(landing_rev))
    old = POP_FIGURE.search(git("show", f"{landing_rev}:{SWEEP_OUT_REL}") or "")
    old_n = int(re.sub(r"\D", "", old.group(1))) if old else None
    record(None,
           f"S4c THE HISTORICAL FACT, FROM GIT: the transcript as committed at "
           f"{landing_rev} publishes {old_n} and the tree at {landing_rev} "
           f"holds {at_landing} `.py` files under `code/` -- "
           f"{at_landing - (old_n or 0)} in the population and not in the "
           f"number.  Re-derived here from `git ls-tree` at that commit, not "
           f"quoted from mg-7e39")


# --------------------------------------------------------------------------
# S5 -- THIS DELIVERABLE, CHECKED FOR ITS OWN FOUR SHAPES
# --------------------------------------------------------------------------
MINE = "code/hodge_leverage_repair_3f3b/repair_7e39.py"


def s5():
    head("S5 -- THIS DELIVERABLE, CHECKED FOR THE FOUR SHAPES IT REPAIRS")
    src = read(MINE)

    # F1's shape: does THIS file decline anywhere without a count?
    #
    # ⚠️ SCOPED BY AST, not by a regex over the whole file.  The first version
    # of this check searched every `return None, "..."` in the file and
    # reported two "countless reasons" that were a 3-tuple in `probe_on_disk`
    # and a runaway match across `strip_pipe_clause`.  A check that reports
    # the wrong population is the finding it is checking for, one level in.
    tree = ast.parse(src)
    bad, reasons = [], 0
    for fn in [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
               and (n.name.startswith("my_k") or n.name == "apply_my_kind")]:
        for node in ast.walk(fn):
            if not isinstance(node, ast.Return):
                continue
            v = node.value
            if not (isinstance(v, ast.Tuple) and len(v.elts) == 2):
                continue
            first, why = v.elts
            if not (isinstance(first, ast.Constant) and first.value is None):
                continue
            reasons += 1
            measured = any(
                isinstance(x, ast.FormattedValue)
                or (isinstance(x, ast.Constant) and isinstance(x.value, str)
                    and re.search(r"\d", x.value))
                for x in ast.walk(why))
            if not measured:
                bad.append(f"{fn.name}:{node.lineno}")
    record(not bad,
           f"S5a F1's shape here: {reasons} decline reason(s) are written by "
           f"this file's own kind derivations and {len(bad)} carry no measured "
           f"count -- {bad}.  Predicted 0.  An instrument that writes `n/a` "
           f"reasons while auditing `n/a` reasons is the first place to look, "
           f"and this is the same rule the artifact now fails closed on")

    # F5's shape: does THIS file hand-list a vocabulary it could derive?
    lits = re.findall(r'^\s*(?:hand|printed|now)\s*=\s*\[', src, re.M)
    record(None,
           f"S5b F5's shape here: this file names {len(lits)} vocabulary "
           f"literal(s).  The one it keeps is `hand`, which IS the parent's "
           f"list and must be written out to be compared against -- a literal "
           f"quoted as the object under test is not the same as a literal used "
           f"as a scope.  `printed` is derived from the live rows")

    # F3's shape: is the construct performed here anywhere but in the declared
    # function?
    inline = sorted({(ln, t) for nm in my_vocabulary()
                     for ln, t in my_hits(MINE, nm)})
    for i, t in inline:
        print(f"    ⚠️ {MINE}:{i}  {t[:80]}")
    record(not inline,
           f"S5c F3's shape here: {len(inline)} line(s) of this file identify "
           f"a gate row by a substring of the whole row outside "
           f"`by_substring`.  Predicted 0")

    # F2's shape: does THIS file carry a population figure?
    record(None,
           "S5d F2's shape here: every population figure this deliverable "
           "publishes is computed by S4 at a named commit and printed into the "
           "transcript by the run.  Its README and report point at the "
           "transcript line; S4b is the check, and it reads this deliverable's "
           "own prose as well as the parent's")


# --------------------------------------------------------------------------
# S6 -- THE ORDERING, FROM GIT
# --------------------------------------------------------------------------
def s6():
    head("S6 -- THE ORDERING, RE-DERIVED FROM GIT")
    probe = git("log", "--format=%H", "--reverse", "--", MINE).split("\n")
    probe = [c for c in probe if c.strip()]
    fix = git("log", "--format=%H", "--reverse", "--", LANDING_REL).split("\n")
    fix = [c for c in fix if c.strip()]
    if not probe:
        record(None, "S6a this instrument is not committed yet, so the "
                     "ordering it claims is not yet a fact in the repository. "
                     "This row becomes a measurement at the commit that lands "
                     "the file")
        return
    first_probe = probe[0]
    order = git("rev-list", "--count", f"{first_probe}..HEAD").strip()
    print(f"    this instrument first committed at : {first_probe[:12]}")
    print(f"    commits from there to HEAD          : {order}")
    print(f"    `verify_landing.py` last changed at : "
          f"{(fix[-1] if fix else '?')[:12]}")
    record(None,
           f"S6a the predictions and this instrument are committed at "
           f"{first_probe[:12]}, {order} commit(s) before HEAD.  "
           f"'Predict before measuring' is a claim about the repository and is "
           f"read out of `git log` here rather than asserted in prose")


def main():
    print("=" * 78)
    print("mg-3f3b -- mg-7e39's four findings, repaired and controlled")
    print("=" * 78)
    base_out = s0()
    s1(base_out)
    s2()
    s3()
    s4()
    s5()
    s6()

    head("SUMMARY")
    ok = sum(1 for _d, v in RESULTS if v is True)
    meas = sum(1 for _d, v in RESULTS if v is None)
    bad = [d for d, v in RESULTS if v is False]
    print(f"    checks          : {len(RESULTS)}")
    print(f"    confirmed       : {ok}")
    print(f"    measured        : {meas}")
    print(f"    refuted         : {len(bad)}")
    for d in bad:
        print(f"      REFUTED: {d[:150]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
