#!/usr/bin/env python3
"""mg-7e39 -- INDEPENDENT AUDIT of the mg-6df0 repair of the mg-ec07 verdict.

The repair under audit is the commit that keys `reseal()`'s refusal on
`heading()` and replaces the kind-per-site battery with a SITES x KINDS
matrix.  It is derived from git here, never named as a sha in this file.

WHAT IS MINE AND WHAT IS THE ARTIFACT'S, stated up front because
"replication is not corroboration when the copies share a source":

  MINE      the site cutters (`my_section`, `my_framed_row`), the twelve kind
            derivations, the write-back, the AST sweep, every population, and
            the scoring -- which reads the runner's STDOUT from a SUBPROCESS.
            No cell of B1's matrix is decided by anything imported from the
            artifact.
  THEIRS    the figure-token grammar and the figure/segment seam (`partition`)
            in B6, and the gate itself everywhere.  The gate is the SUBJECT;
            calling it is the measurement.  Where a population would otherwise
            be defined by their regex, B6a cross-checks the token count with a
            naive one of mine and prints both.

B1's matrix and B3's refusal probes touch the WORKING TREE.  Every file is
snapshotted as bytes before the first probe and restored and re-hashed after
each one; B0c is the check that the restore held, and it is fail-closed.
"""
import ast
import hashlib
import importlib.util
import itertools
import os
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))

LANDING_REL = "code/hodge_leverage_landing_e1d0/verify_landing.py"
RECORDS_REL = "code/hodge_leverage_landing_e1d0/site_records.txt"
LANDING = os.path.join(REPO, LANDING_REL)
RUNDIR = os.path.dirname(LANDING)

RESULTS = []
FINDINGS = []


# --------------------------------------------------------------------------
# plumbing
# --------------------------------------------------------------------------
def git(*args):
    return subprocess.run(["git", "-C", REPO] + list(args),
                          capture_output=True, text=True).stdout


def read_rel(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return fh.read()


def write_rel(rel, text):
    with open(os.path.join(REPO, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def record(ok, detail):
    RESULTS.append((detail, ok))
    mark = {True: "[CONFIRMED]", False: "[REFUTED  ]", None: "[MEASURED ]"}[ok]
    print(f"  {mark} {detail}")


def finding(tag, detail):
    FINDINGS.append((tag, detail))
    print(f"  >> FINDING {tag}: {detail}")


def head(title):
    print()
    print(title)
    print("-" * len(title))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V = load_module(LANDING, "vl_head_7e39")

TMP = tempfile.mkdtemp(prefix="mg-7e39-")


def blob_module(commit, name):
    """`verify_landing.py` as of `commit`, importable, with REPO pointed back
    at the real tree so it reads the same documents."""
    src = git("show", f"{commit}:{LANDING_REL}")
    path = os.path.join(TMP, f"{name}.py")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src)
    mod = load_module(path, name)
    mod.REPO = REPO
    return mod


def repair_commits():
    """(the commit that LANDS the refusal fix, its PARENT).  Derived from git
    by searching for the fix's own text, never asserted as a sha here -- a sha
    written into an audit is a claim that rots."""
    log = git("log", "--reverse", "--format=%H", "-S",
              'not heading(d).endswith("SITE RECORD")', "--",
              LANDING_REL).split()
    fix = log[0]
    return fix, git("rev-parse", f"{fix}^").strip()


def census_commits():
    """(the commit that lands mg-ff3e's census, its parent) -- the parent is
    where the LOSSLESS claim is still false, and is mg-ec07's control."""
    log = git("log", "--reverse", "--format=%H", "-S", "def partition(",
              "--", LANDING_REL).split()
    fix = log[0]
    return fix, git("rev-parse", f"{fix}^").strip()


def measured_now():
    a = len(V.state_row(V.tree(V.STATE)))
    b = len(V.deliv_row(V.tree(V.DELIV)))
    h = len(V.tree(V.HIST))
    return {"gap":  V.doc_num(a - b, signed=True),
            "both": V.doc_num(a + h - b, signed=True),
            "cell": V.doc_num(a), "hist": V.doc_num(h), "copy": V.doc_num(b)}


# --------------------------------------------------------------------------
# MY OWN SITE CUTTERS.  Written from the disclosure sentences, not from the
# artifact's code, so that B5 is a test of the sentences and B0d is a test of
# whether two readings of them agree.
# --------------------------------------------------------------------------
def my_section(text, prefix):
    """"the markdown SECTION, heading to the next heading of the same or
    shallower level -- not the file that contains it", implemented from that
    sentence alone."""
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(idx) != 1:
        return None
    i = idx[0]
    depth = len(lines[i]) - len(lines[i].lstrip("#"))
    for j in range(i + 1, len(lines)):
        d = len(lines[j]) - len(lines[j].lstrip("#"))
        if 0 < d <= depth:
            return "\n".join(lines[i:j])
    return "\n".join(lines[i:])


def my_framed_row(text, prefix):
    """"the table ROW and the HEADER LINES it is read under -- not the table's
    other rows", implemented from that sentence alone."""
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(idx) != 1:
        return None
    i = idx[0]
    top = i
    while top > 0 and lines[top - 1].startswith("|"):
        top -= 1
    if top > i - 2:
        return None
    return "\n".join([lines[top], lines[top + 1], lines[i]])


def my_splice_section(raw, prefix, new_site):
    old = my_section(raw, prefix)
    if old is None or raw.count(old) != 1:
        return None
    return raw.replace(old, new_site, 1)


def my_splice_framed_row(raw, prefix, new_site):
    lines = raw.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if len(idx) != 1:
        return None
    i = idx[0]
    top = i
    while top > 0 and lines[top - 1].startswith("|"):
        top -= 1
    parts = new_site.split("\n")
    if len(parts) != 3:
        return None
    lines[top], lines[top + 1], lines[i] = parts
    return "\n".join(lines)


# name -> (relative file, cutter, anchor, splicer).  Independently written; B0d
# checks it against the artifact's ANCHORS table.
MY_SITES = [
    ("the STATE.md row", "STATE.md", my_framed_row, "| **AMBER-POSITIVE",
     my_splice_framed_row),
    ("§14", "docs/OneThird-Hodge-Side-Leverage.md", my_section,
     "## §14 — `STATE.md` row, as landed", my_splice_section),
    ("H8", "docs/state-history/attempt-mg-a3d4.md", my_section,
     "### H8 — ", my_splice_section),
]
MY_NAMES = [n for n, _p, _f, _a, _s in MY_SITES]
MY_FILES = sorted({p for _n, p, _f, _a, _s in MY_SITES})


def my_texts(files):
    out = {}
    for name, path, fn, anchor, _s in MY_SITES:
        out[name] = fn(files[path], anchor)
    return out


def files_from_disk():
    return {p: read_rel(p) for p in MY_FILES}


def my_with_site(files, name, new_site):
    for n, path, _f, anchor, sp in MY_SITES:
        if n == name:
            raw = sp(files[path], anchor, new_site)
            if raw is None:
                return None
            out = dict(files)
            out[path] = raw
            return out
    return None


# --------------------------------------------------------------------------
# RUNNING THE ARTIFACT AS A BLACK BOX
# --------------------------------------------------------------------------
GATE_LINE = re.compile(r"^\s*\[(CONFIRMED|REFUTED  |MEASURED )\] (GATE @ .+)$")


def run_runner(*args):
    p = subprocess.run([sys.executable, "verify_landing.py", *args],
                       cwd=RUNDIR, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def gate_rows(out):
    """The gate rows the runner printed ON THE TREE.  Cut at the negative
    control, whose rows are the artifact's own mutations and not mine."""
    body = out.split("NEGATIVE CONTROL")[0]
    rows = []
    for l in body.split("\n"):
        m = GATE_LINE.match(l)
        if m:
            rows.append((m.group(1) == "CONFIRMED", m.group(2)))
    return rows


def by_substring(rows, name):
    """⚠️ THE CONSTRUCT, COMMITTED ON PURPOSE AND IN EXACTLY ONE PLACE.

    A substring test over a whole gate row is the defect this arc repairs, and
    MEASURING it requires PERFORMING it.  So it is performed here, once, in a
    function whose name says what it is -- rather than written inline, where a
    sweep of the tree can only tell it from the defect by a disposition keyed
    on its line number.  A REASON ON A LINE IS NOT A STRUCTURE: it has to be
    read, it has to be maintained, and it goes stale the moment the line moves.

    ⚠️ ADDED BY mg-3f3b (mg-7e39 F3): 6 instances of the construct existed
    when mg-6df0 landed, it repaired 1 and dispositioned 5."""
    return [r for r in rows if name in r]


def row_kind(detail):
    """The row's kind -- SITE RECORD, RECORD PARTITION, FIGURE CENSUS, ... --
    read off the heading.  MY parse of the heading, not the artifact's."""
    h = detail.split(" -- ")[0]
    tail = h.split(": ", 1)[1] if ": " in h else h
    m = re.match(r"^([A-Z][A-Z ]+[A-Z])\b", tail)
    return m.group(1) if m else tail[:40]


def inject(src, code):
    """`src` with `code` spliced in BEFORE its `if __name__ == "__main__"`
    block.

    ⚠️ Appending it to the end does nothing, because `main()` has already run
    by then -- which is how the first version of B3 and B5c reported the
    artifact BLESSING a lossy record and a renamed anchor staying green: a
    probe that never reached the code it was probing, reading as a fact about
    the artifact.  That is the same shape as the finding B2 makes, in this
    instrument, and it is kept in the misses table."""
    marker = 'if __name__ == "__main__":'
    if marker not in src:
        return src + code
    i = src.index(marker)
    return src[:i] + code + "\n\n" + src[i:]


BASELINE = {}


def snapshot():
    for rel in MY_FILES + [LANDING_REL, RECORDS_REL]:
        BASELINE[rel] = read_rel(rel)


def restore():
    for rel, text in BASELINE.items():
        if read_rel(rel) != text:
            write_rel(rel, text)
    return all(read_rel(rel) == text for rel, text in BASELINE.items())


# --------------------------------------------------------------------------
# B0 -- PREFLIGHT
# --------------------------------------------------------------------------
def b0():
    head("B0 -- PREFLIGHT: the tree, the artifact, and my cutters against theirs")
    rc, out = run_runner()
    rows = gate_rows(out)
    bad = [d for ok, d in rows if not ok]
    record(rc == 0 and not bad,
           f"B0a the runner on a clean tree: exit {rc}, {len(rows)} gate rows, "
           f"{len(bad)} refuted.  Predicted exit 0 / 0 refuted")
    record(len(rows) == 34,
           f"B0b the figure gate returns {len(rows)} rows.  Predicted 34, "
           f"derived: 3 sites x 4 census rows = 12, plus 12 READ AT THE SITE "
           f"rows over the 12 (site, key) pairs, plus 10 WRITTEN ONCE rows")
    kinds = {}
    for _ok, d in rows:
        kinds[row_kind(d)] = kinds.get(row_kind(d), 0) + 1
    print(f"    rows by kind: " + ", ".join(f"{k} {v}" for k, v in
                                            sorted(kinds.items())))
    files = files_from_disk()
    mine = my_texts(files)
    theirs = V.site_texts()
    agree = [n for n in MY_NAMES if mine[n] == theirs[n]]
    record(len(agree) == 3,
           f"B0d my cutters, written from the DISCLOSURE SENTENCES alone, "
           f"reproduce the artifact's sites at {len(agree)} of 3: "
           + "; ".join(f"{n} {len(mine[n]):,} chars" for n in MY_NAMES)
           + ".  Two readings of the same sentence landing on the same bytes "
             "is what makes the sentence a specification rather than a label")
    return rows


# --------------------------------------------------------------------------
# MY TWELVE KIND DERIVATIONS
#
# One per enumerated kind, written against the KIND rather than against the
# artifact's implementation of it -- which is the whole point of building the
# product again.  Each returns (new_site, reason): a reason is a claim about
# THE SITE and B2 tests every one of them.
# --------------------------------------------------------------------------
WRONG_FIG = {True: "+9 999", False: "99 999"}


def live_here(name, live):
    """The first LIVE figure this site is licensed to write, and its value."""
    keys = dict((n, k) for n, _r, k in V.SITES)[name]
    for k in keys:
        if V.FIGURES[k][1]:
            return k, live[k]
    return None, None


def append_inline(site, name, live, sentence):
    """Append to the LINE carrying the site's first live figure, so the line
    COUNT does not move and a 3-line row can take the mutation too."""
    _k, val = live_here(name, live)
    if not val:
        return None
    lines = site.split("\n")
    for i, l in enumerate(lines):
        if val in l:
            lines[i] = l + " " + sentence
            return "\n".join(lines)
    return None


def pipe_rows(site):
    return [l for l in site.split("\n") if l.startswith("|") and l.count("|") >= 3]


def ws_rows(site):
    return [l for l in site.split("\n")
            if len(re.findall(r"\S(  +)\S", l)) >= 2]


def any_table_rows(site):
    """Rows of a table in EITHER format.  The site is a table if this is
    non-empty -- a claim about the site, not about a parser."""
    return pipe_rows(site) + ws_rows(site)


def cells_of(line):
    if line.startswith("|"):
        return line.split("|")[1:-1]
    return re.split(r"\s{2,}", line.strip())


def has_figure(s):
    return bool(V.FIGURE_TOKEN.search(s))


def swap_once(text, a, b):
    return text.replace(a, "\0", 1).replace(b, a, 1).replace("\0", b, 1)


def k01_figure(name, site, live):
    _k, val = live_here(name, live)
    if not val or site.count(val) != 1:
        return None, "no live figure is written exactly once in this site"
    return site.replace(val, WRONG_FIG[val[0] in "+−"], 1), None


def k02_duplicate(name, site, live):
    _k, val = live_here(name, live)
    if not val:
        return None, "no live figure at this site"
    return append_inline(site, name, live, f"(restated: {val})"), None


def k03_prose(name, site, live):
    return append_inline(site, name, live,
                         "The gap is now +9 999 characters."), None


def k04_roster(name, site, live):
    known = sorted(V.HISTORICAL[name])
    if not known:
        return None, "no historical figure is declared for this site"
    return append_inline(site, name, live,
                         f"The gap is now {known[0]} characters."), None


def k05_undeclared(name, site, live):
    return append_inline(site, name, live,
                         "A new figure of 12 345 characters appears."), None


def k06_transpose(name, site, live):
    seg, figs = V.partition(site)
    pair = next(((i, j) for i in range(len(figs))
                 for j in range(i + 1, len(figs)) if figs[i] != figs[j]), None)
    if pair is None:
        return None, "fewer than two asserted figures of differing value here"
    figs = list(figs)
    i, j = pair
    figs[i], figs[j] = figs[j], figs[i]
    return V.rejoin(seg, figs), None


def bold_labels(name, site):
    anchor = next(a for n, _p, _f, a, _s in MY_SITES if n == name)
    start = site.index(anchor) + len(anchor) if anchor in site else 0
    return [m.group(0) for m in re.finditer(r"\*\*(.+?)\*\*", site, re.S)
            if not has_figure(m.group(1)) and site.count(m.group(0)) == 1
            and m.start() >= start]


def k07_label(name, site, live):
    spans = bold_labels(name, site)
    if len(spans) < 2:
        return None, "fewer than two uniquely-occurring figure-free bold labels"
    return swap_once(site, spans[0], spans[1]), None


def k08_row_label(name, site, live):
    rows = [l for l in any_table_rows(site) if has_figure(l)]
    if len(rows) < 2:
        return None, (f"only {len(rows)} table row(s) carrying a figure lie "
                      f"INSIDE this site, in either table format")
    pair = next((((x, y)) for i, x in enumerate(rows) for y in rows[i + 1:]
                 if cells_of(x)[0].strip() and cells_of(y)[0].strip()
                 and cells_of(x)[0] != cells_of(y)[0]
                 and site.count(x) == 1 and site.count(y) == 1), None)
    if pair is None:
        return None, "no two figure-carrying rows here carry distinct unique labels"
    x, y = pair
    a, b = cells_of(x)[0], cells_of(y)[0]
    out = site.replace(x, x.replace(a, b, 1), 1)
    return out.replace(y, y.replace(b, a, 1), 1), None


def header_line(name, site):
    """The line naming the columns the site's figures are read under, IN
    EITHER TABLE FORMAT."""
    lines = site.split("\n")
    for i, l in enumerate(lines):
        if l.startswith("|") and l.count("|") >= 3 and not has_figure(l) \
                and not re.fullmatch(r"\|[\s:|-]+\|", l.strip()):
            if any(has_figure(x) for x in lines[i + 1:i + 5]):
                return l
    for i, l in enumerate(lines):
        if len(re.findall(r"\S(  +)\S", l)) >= 2 and not has_figure(l) \
                and any(has_figure(x) for x in lines[i + 1:i + 4]):
            return l
    return None


def k09_col_header(name, site, live):
    line = header_line(name, site)
    if line is None:
        return None, "no column-header line inside this site, in either format"
    cells = [c for c in cells_of(line) if c.strip()]
    if len(cells) < 2 or cells[0] == cells[1]:
        return None, "the header line has fewer than two distinct columns"
    return site.replace(line, swap_once(line, cells[0], cells[1]), 1), None


def k10_quoted(name, site, live):
    for s, e in V.quoted_spans(site):
        m = V.FIGURE_TOKEN.search(site[s:e])
        if m:
            tok = m.group()
            bad = tok[:-1] + ("8" if tok[-1] != "8" else "7")
            return site[:s] + site[s:e].replace(tok, bad, 1) + site[e:], None
    return None, (f"{len(V.quoted_spans(site))} marked quotation(s) at this "
                  f"site and none carries a figure token")


def k11_layout(name, site, live):
    """THE TABLE'S ALIGNMENT, SHIFTED -- in either table format.

    ⚠️ The artifact's `k_layout` shifts runs of two or more spaces, which is
    the alignment of a WHITESPACE-COLUMN table and is not how a markdown pipe
    table is aligned.  A markdown table is aligned by the padding inside its
    cells, so that is what this shifts.  The kind is the same; the grammar of
    the site is not."""
    for l in site.split("\n"):
        runs = list(re.finditer(r"\S(  +)\S", l))
        if len(runs) >= 2:
            a, b = runs[0].span(1), runs[1].span(1)
            new = (l[:a[0]] + " " * (a[1] - a[0] - 1) + l[a[1]:b[0]]
                   + " " * (b[1] - b[0] + 1) + l[b[1]:])
            return site.replace(l, new, 1), None
    for l in site.split("\n"):
        if l.startswith("| ") and l.count("|") >= 3 \
                and not re.fullmatch(r"\|[\s:|-]+\|", l.strip()) \
                and site.count(l) == 1:
            return site.replace(l, "|  " + l[2:], 1), None
    return None, "this site contains no table row whose alignment can shift"


def k12_relocate(name, site, live):
    paras = site.split("\n\n")
    body = [p for p in paras[1:] if p.strip() and not has_figure(p)]
    if not body:
        return None, (f"this site is {len(paras)} paragraph(s) and none after "
                      f"the first is figure-free, so there is nothing to "
                      f"relocate out of it")
    return site.replace("\n\n" + body[0], "", 1), None


MY_KINDS = [
    ("K01 the LIVE figure a reader meets, corrupted", k01_figure),
    ("K02 the figure DUPLICATED at the site", k02_duplicate),
    ("K03 a WRONG figure in ORDINARY PROSE", k03_prose),
    ("K04 wrong prose REUSING a figure on the roster", k04_roster),
    ("K05 a NEW undeclared historical figure", k05_undeclared),
    ("K06 two DECLARED FIGURES exchanged", k06_transpose),
    ("K07 two LABELS exchanged, no figure moved", k07_label),
    ("K08 two table ROW LABELS exchanged", k08_row_label),
    ("K09 two COLUMN HEADERS exchanged (mg-ec07's X1)", k09_col_header),
    ("K10 a figure inside a MARKED QUOTATION altered", k10_quoted),
    ("K11 the table's ALIGNMENT shifted, no figure moved", k11_layout),
    ("K12 a whole PARAGRAPH relocated out of the site", k12_relocate),
]
LABEL_SIDE = ("K07", "K08", "K09", "K10", "K11")


# --------------------------------------------------------------------------
# B1 -- THE MATRIX, BUILT BY ME AND SCORED FROM OUTSIDE
# --------------------------------------------------------------------------
def probe_on_disk(files):
    """Write mutated files, run the runner as a SUBPROCESS, restore, and hash
    everything back.  Returns (rc, rows)."""
    for path, text in files.items():
        write_rel(path, text)
    try:
        rc, out = run_runner()
    finally:
        ok = restore()
    if not ok:
        raise SystemExit("FAIL-CLOSED: the tree did not restore")
    return rc, gate_rows(out)


def b1(live):
    head("B1 -- SITES x KINDS, BUILT AGAIN: my derivations, my write-back, "
         "scored from the runner's stdout")
    print("""THE MATRIX IS THE GRAIN THE PARENT FAILED AT, so a matrix printed by the
party under audit is the thing being audited and not the evidence for it.
Every cell below is a mutation I derived, spliced into THE FILE by my own
write-back, with `verify_landing.py` then run AS A SUBPROCESS and its gate
rows read out of its stdout.  Nothing the artifact computes decides a cell.
""")
    base_files = files_from_disk()
    base = my_texts(base_files)
    cells, reasons = {}, []
    fires = na = silent = crash = 0
    lab_cells = lab_rec = 0
    print(f"    {'kind':<52}" + "".join(f"{n[:18]:<22}" for n in MY_NAMES))
    for title, fn in MY_KINDS:
        tag = title[:3]
        row = []
        for name in MY_NAMES:
            new_site, why = fn(name, base[name], live)
            if new_site is None or new_site == base[name]:
                cells[(tag, name)] = ("n/a", why or "the derivation produced "
                                                    "no change", None, [])
                reasons.append((tag, name, why or "the derivation produced "
                                                  "no change"))
                na += 1
                row.append("n/a")
                continue
            files = my_with_site(base_files, name, new_site)
            if files is None:
                cells[(tag, name)] = ("n/a", "the mutation cannot be written "
                                             "back without moving the site's "
                                             "line count", None, [])
                reasons.append((tag, name, "the mutation cannot be written "
                                           "back without moving the site's "
                                           "line count"))
                na += 1
                row.append("n/a")
                continue
            rc, rows = probe_on_disk(files)
            bad = [d for ok, d in rows if not ok]
            kinds = sorted({row_kind(d) for d in bad})
            if not rows:
                crash += 1
                cells[(tag, name)] = ("CRASH", "", rc, [])
                row.append(f"CRASH rc={rc}")
                continue
            if bad:
                fires += 1
                rec = "SITE RECORD" in kinds
                figfree = not ({"FIGURE CENSUS", "FIGURE ORDER"} & set(kinds))
                cells[(tag, name)] = ("FIRES", "", rc, kinds)
                row.append("FIRES" + (" (rec)" if rec and figfree else ""))
                if tag in LABEL_SIDE:
                    lab_cells += 1
                    lab_rec += rec and figfree
            else:
                silent += 1
                cells[(tag, name)] = ("SILENT", "", rc, [])
                row.append(f"SILENT rc={rc}")
        print(f"    {title[:50]:<52}" + "".join(f"{c:<22}" for c in row))
    print()
    for tag, name, why in reasons:
        print(f"      n/a  {tag} @ {name:<18} {why}")
    print()
    applicable = fires + silent + crash
    record(silent == 0 and crash == 0,
           f"B1b {fires} of {applicable} APPLICABLE cells of the "
           f"{len(MY_KINDS)}x{len(MY_NAMES)} = {len(MY_KINDS) * len(MY_NAMES)} "
           f"SITES x KINDS product FIRE; {silent} SILENT, {crash} crashed, "
           f"{na} n/a.  Population: the product, not a total -- the matrix "
           f"above is the finding and this line is its summary")
    rcs = {c[2] for c in cells.values() if c[0] == "FIRES"}
    record(rcs == {1},
           f"B1c every firing cell exits {sorted(rcs)}.  Predicted exit 1 at "
           f"every one; a mutated tree that exits 0 is a silent cell wearing "
           f"a fire's clothes")
    record(lab_rec == lab_cells,
           f"B1d {lab_rec} of {lab_cells} applicable LABEL-SIDE cells (K07-K11)"
           f" are caught BY SITE RECORD with every FIGURE CENSUS and FIGURE "
           f"ORDER row green -- the attribution claim, over the product")
    return cells


def b1e(cells):
    head("B1e -- MY MATRIX AGAINST THE ARTIFACT'S OWN, CELL BY CELL")
    rc, out = run_runner()
    theirs = {}
    for l in out.split("\n"):
        if not re.match(r"^ {4}K\d\d ", l) or len(l) <= 66:
            continue
        tag = l[4:7]
        rest = l[66:]
        chunks = [rest[i:i + 20].strip() for i in range(0, 60, 20)]
        for name, c in zip(MY_NAMES, chunks):
            if c:
                theirs[(tag, name)] = c
    if not theirs:
        record(None, "B1e the artifact's matrix could not be parsed from its "
                     "stdout; comparison skipped and said so")
        return
    agree = disagree = 0
    lines = []
    for (tag, name), (verdict, _why, _rc, _k) in sorted(cells.items()):
        t = theirs.get((tag, name), "?")
        m = "FIRES" if verdict == "FIRES" else verdict
        same = (t.startswith("FIRES") and m == "FIRES") or (t == m)
        agree += same
        disagree += not same
        if not same:
            lines.append(f"      {tag} @ {name:<18} mine {m:<8} theirs {t}")
    for l in lines:
        print(l)
    record(disagree == 0 or all("n/a" in l for l in lines),
           f"B1e {agree} of {agree + disagree} cells agree with the artifact's "
           f"own matrix; {disagree} disagree, and every disagreement above is "
           f"about APPLICABILITY rather than about FIRES/SILENT")
    return theirs


# --------------------------------------------------------------------------
# B2 -- THE n/a CELLS: a fact about the SITE, or about the DERIVATION?
# --------------------------------------------------------------------------
def b2(cells, theirs, live):
    head("B2 -- EVERY n/a REASON READ AS A CLAIM ABOUT THE SITE, AND FALSIFIED")
    print("""`n/a` IS WHERE A MATRIX HIDES.  The parent's own predictions record that its
first matrix reported 19 applicable cells because a write-back was failing
silently, and say in as many words that A DERIVATION THAT FAILS SILENTLY READS
EXACTLY LIKE A SITE THAT HAS NO SUCH TEXT.  So every n/a reason below is read
as a CLAIM ABOUT THE SITE and measured against the site independently.
""")
    base = my_texts(files_from_disk())
    facts = {}
    for name in MY_NAMES:
        s = base[name]
        quoted = V.quoted_spans(s)
        facts[name] = {
            "pipe rows": len(pipe_rows(s)),
            "whitespace-column rows": len(ws_rows(s)),
            "table rows carrying a figure": len([l for l in any_table_rows(s)
                                                 if has_figure(l)]),
            "column-header line": header_line(name, s) is not None,
            "marked quotations": len(quoted),
            "  ... of them carrying a figure":
                sum(1 for a, b in quoted if has_figure(s[a:b])),
            "paragraphs": len(s.split("\n\n")),
            "figure-free paragraphs after the first":
                len([p for p in s.split("\n\n")[1:]
                     if p.strip() and not has_figure(p)]),
        }
    for name in MY_NAMES:
        print(f"    {name}")
        for k, v in facts[name].items():
            print(f"        {k:<44} {v}")
    print()
    their_na = sorted(k for k, v in (theirs or {}).items() if v == "n/a")
    mine_na = sorted(k for k, v in cells.items() if v[0] == "n/a")
    print(f"    the artifact reports {len(their_na)} n/a cells; I report "
          f"{len(mine_na)}")
    only_theirs = [k for k in their_na if k not in mine_na]
    for tag, name in only_theirs:
        v = cells.get((tag, name))
        print(f"      {tag} @ {name}: the artifact says n/a, I derived a "
              f"mutation and the runner said {v[0] if v else '?'}")
    record(None,
           f"B2a of the artifact's {len(their_na)} n/a cells, "
           f"{len(their_na) - len(only_theirs)} are also n/a for a derivation "
           f"written independently and {len(only_theirs)} are not -- "
           f"{[f'{t} @ {n}' for t, n in only_theirs]}.  A cell that is n/a "
           f"for one derivation and applicable for another is a fact about "
           f"the DERIVATION printed in the grammar of a fact about the SITE")
    if only_theirs:
        for tag, name in only_theirs:
            v = cells.get((tag, name))
            if v and v[0] == "FIRES":
                finding("F1", f"{tag} @ {name} is reported `n/a` by the "
                              f"repair's own matrix with a reason phrased as "
                              f"a property of the site, and it is a property "
                              f"of the derivation: an independent mutation of "
                              f"the same kind FIRES at that cell, caught by "
                              f"{', '.join(v[3])}.  The published matrix is "
                              f"{len(their_na)} n/a where it should be "
                              f"{len(their_na) - len(only_theirs)}, and the "
                              f"cell it understates is on the K09/K11 "
                              f"label-side rows that carry the whole X1 "
                              f"argument.  It UNDERSTATES coverage and hides "
                              f"no hole -- the cell fires -- which is why it "
                              f"is a finding about the instrument and not "
                              f"about the gate")
            elif v and v[0] == "SILENT":
                finding("F1", f"{tag} @ {name}: reported n/a, derivable, and "
                              f"the gate is SILENT on it.  THIS IS A HOLE")
    for tag, name in mine_na:
        why = cells[(tag, name)][1]
        print(f"      mine n/a {tag} @ {name:<18} {why}")


# --------------------------------------------------------------------------
# B3 -- THE REFUSAL, OVER ALL 34 ROWS AND AT EACH OF THE 3 EXCLUDED ONES
# --------------------------------------------------------------------------
LOSSY = '''

# ---- mg-7e39 probe: `partition` bent lossy AT ONE SITE ONLY ----
_MG7E39_MARK = {mark!r}
_mg7e39_partition = partition


def partition(raw):
    seg, figs = _mg7e39_partition(raw)
    if _MG7E39_MARK in raw:
        seg = list(seg)
        i = max(range(len(seg)), key=lambda k: len(seg[k]))
        seg[i] = seg[i][:-1]
    return seg, figs
'''


def b3(rows_head):
    head("B3 -- THE REFUSAL: all 34 rows, and each of the 3 that the substring "
         "test excluded")
    details = [d for _ok, d in rows_head]
    by_sub = by_substring(details, "SITE RECORD")
    by_head = [d for d in details
               if d.split(" -- ")[0].endswith("SITE RECORD")]
    diff = [d for d in by_sub if d not in by_head]
    record(len(by_sub) == 6 and len(by_head) == 3,
           f"B3a of the {len(details)} gate rows, 'SITE RECORD' as a SUBSTRING "
           f"selects {len(by_sub)} and as a HEADING selects {len(by_head)}.  "
           f"The {len(diff)} that differ: "
           + "; ".join(sorted(row_kind(d) + " @ " + d.split(":")[0][7:]
                              for d in diff)))
    record(len(details) - len(by_head) == 31,
           f"B3b {len(details) - len(by_head)} of {len(details)} rows BLOCK a "
           f"reseal when refuted and {len(by_head)} are excluded by design "
           f"(the SITE RECORD rows, which are what a reseal exists to "
           f"rewrite).  Under the substring test it was "
           f"{len(details) - len(by_sub)} blocking and {len(by_sub)} excluded: "
           f"the {len(diff)} rows in between are the ones that license 'the "
           f"record is lossless'")

    fix, pre = repair_commits()
    print(f"    the repair lands at   : {fix[:7]}")
    print(f"    the control runs at   : {pre[:7]}  (the defect still present)")
    print()
    base = my_texts(files_from_disk())
    marks = {}
    for name in MY_NAMES:
        anchor = next(a for n, _p, _f, a, _s in MY_SITES if n == name)
        hits = [n for n in MY_NAMES if anchor in base[n]]
        if hits != [name]:
            raise SystemExit(f"FAIL-CLOSED: {anchor!r} is not unique to {name}")
        marks[name] = anchor

    pre_src = git("show", f"{pre}:{LANDING_REL}")
    pre_rec = git("show", f"{pre}:{RECORDS_REL}")
    head_src = BASELINE[LANDING_REL]
    head_rec = BASELINE[RECORDS_REL]

    def reseal_with(src, rec, mark):
        write_rel(LANDING_REL, inject(src, LOSSY.format(mark=mark)))
        write_rel(RECORDS_REL, rec)
        before = sha(read_rel(RECORDS_REL))
        try:
            rc, out = run_runner("--reseal")
        finally:
            after = sha(read_rel(RECORDS_REL))
            if not restore():
                raise SystemExit("FAIL-CLOSED: the tree did not restore")
        return rc, out, before, after

    post_ok = pre_blessed = 0
    for name in MY_NAMES:
        rc, out, b, a = reseal_with(head_src, head_rec, marks[name])
        refused = "REFUSED" in out
        blocking = [l.strip()[2:] for l in out.split("\n")
                    if l.strip().startswith("- GATE @")]
        ok = rc == 1 and refused and a == b
        post_ok += ok
        record(ok,
               f"B3c @ {name}: `partition` bent lossy AT THIS SITE ONLY, then "
               f"`--reseal` -> exit {rc}, {'REFUSED' if refused else 'BLESSED'}"
               f", record sha {b} -> {a} "
               f"({'unchanged' if a == b else 'CHANGED'}).  Blocking rows: "
               + ("; ".join(sorted({row_kind(x) + " @ " + x.split(':')[0][7:]
                                    for x in blocking})) or "none"))
    for name in MY_NAMES:
        rc, out, b, a = reseal_with(pre_src, pre_rec, marks[name])
        blessed = "REFUSED" not in out
        pre_blessed += rc == 0 and blessed and a != b
        record(rc == 0 and blessed and a != b,
               f"B3d CONTROL @ {name}, at {pre[:7]} where the defect is still "
               f"present: the SAME probe -> exit {rc}, "
               f"{'BLESSED' if blessed else 'REFUSED'}, record sha {b} -> {a} "
               f"({'CHANGED' if a != b else 'unchanged'}).  A refusal that "
               f"fires at both commits would be measuring my probe, not the "
               f"repair")
    record(post_ok == 3 and pre_blessed == 3,
           f"B3 THE REFUSAL COVERS THE THREE ROWS THE SUBSTRING TEST EXCLUDED: "
           f"{post_ok} of 3 refuse at HEAD and {pre_blessed} of 3 BLESS at "
           f"{pre[:7]}, one site at a time -- the parent demonstrated this "
           f"once with all three sites bent together, which is one cell of a "
           f"three-cell population")

    # B3e -- the half that already worked, at three sites rather than one.
    live = measured_now()
    kept = 0
    for name in MY_NAMES:
        new_site, _why = k01_figure(name, base[name], live)
        files = my_with_site(files_from_disk(), name, new_site)
        for path, text in files.items():
            write_rel(path, text)
        before = sha(read_rel(RECORDS_REL))
        try:
            rc, out = run_runner("--reseal")
        finally:
            after = sha(read_rel(RECORDS_REL))
            if not restore():
                raise SystemExit("FAIL-CLOSED: the tree did not restore")
        ok = rc == 1 and "REFUSED" in out and before == after
        kept += ok
        record(ok,
               f"B3e @ {name}: a WRONG LIVE FIGURE on disk, then `--reseal` -> "
               f"exit {rc}, {'REFUSED' if 'REFUSED' in out else 'BLESSED'}, "
               f"record unchanged.  The half of the refusal that already "
               f"worked is not weakened")
    record(kept == 3, f"B3e {kept} of 3 sites still refuse a wrong live figure")


# --------------------------------------------------------------------------
# B4 -- THE CONSTRUCT: HOW MANY EXIST, HOW MANY THE REPAIR TOUCHED
# --------------------------------------------------------------------------
def row_vocabulary():
    """The gate row names, DERIVED FROM THE CODE THAT PRINTS THEM rather than
    hand-listed.  The parent's sweep keys on a hand-written list of five, and
    a hand list is a scope nobody chose one level up -- which is the finding
    it is sweeping for."""
    src = BASELINE[LANDING_REL]
    return sorted(set(re.findall(r"GATE @ \{name\}: ([A-Z][A-Z ]+[A-Z])", src))
                  | set(re.findall(r"GATE @ \{name\}: '\{label\}' ([A-Z][A-Z ]+[A-Z])",
                                   src)))


# The functions that PARSE A HEADING out of a row.  `heading` is the
# artifact's; `row_kind` is mine, in this file.  A comparison whose operand
# came through one of these is the REMEDY -- it is keyed on the heading -- and
# a comparison against the whole row is the CONSTRUCT.
HEADING_FUNCS = {"heading", "row_kind"}


def heading_names(tree):
    """Names in this file that are ever bound to something derived from a
    heading parse -- the remedy, not the defect."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            val = node.value
            if val is None:
                continue
            if any(isinstance(n, ast.Call)
                   and getattr(n.func, "id", "") in HEADING_FUNCS
                   for n in ast.walk(val)):
                targets = node.targets if isinstance(node, ast.Assign) \
                    else [node.target]
                for t in targets:
                    for n in ast.walk(t):
                        # ⚠️ STORE ONLY.  `kinds[row_kind(d)] = ...` binds
                        # `kinds`; the `d` inside the subscript is READ.  The
                        # first version of this whitelisted `d` and reported 0
                        # occurrences in this very file -- a check that
                        # exonerates its author is this arc's own defect, so
                        # it is kept here as a comment rather than a story.
                        if isinstance(n, ast.Name) \
                                and isinstance(n.ctx, ast.Store):
                            out.add(n.id)
    return out


def is_heading_expr(node, hnames):
    """Is this operand A HEADING rather than a whole row?  Three ways to be
    one: it came through `heading()`/`row_kind()`, it is a name bound from one
    of those, or it is the heading parse WRITTEN INLINE -- `x.split(" -- ")[0]`
    -- which is the same remedy spelled out."""
    for n in ast.walk(node):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") in HEADING_FUNCS:
            return True
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr in ("split", "partition") and n.args \
                and isinstance(n.args[0], ast.Constant) \
                and n.args[0].value == " -- ":
            return True
        if isinstance(n, ast.Name) and n.id in hnames:
            return True
    return False


def ast_hits(src, vocab):
    """EVERY comparison in this source that identifies a gate row by matching
    a row NAME against something, classified.

    Mine is an AST walk, so it sees a right operand that is not a bare name,
    a comparison split over two lines, and `.find` / `.startswith` /
    `re.search` -- none of which the parent's line regex can see.  It also
    takes its vocabulary from the code that prints the rows."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    hnames = heading_names(tree)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            for op, right in zip(node.ops, node.comparators):
                if not isinstance(op, (ast.In, ast.NotIn)):
                    continue
                left = node.left
                if isinstance(left, ast.Constant) and left.value in vocab:
                    hits.append((node.lineno, left.value,
                                 "REMEDY" if is_heading_expr(right, hnames)
                                 else "CONSTRUCT",
                                 f"{left.value!r} in {ast.unparse(right)}"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("startswith", "endswith", "find",
                                       "index", "count", "split", "partition"):
            for a in node.args:
                consts = [a] if isinstance(a, ast.Constant) else \
                    (list(a.elts) if isinstance(a, ast.Tuple) else [])
                for c in consts:
                    if isinstance(c, ast.Constant) and c.value in vocab:
                        recv = node.func.value
                        hits.append((node.lineno, c.value,
                                     "REMEDY" if is_heading_expr(recv, hnames)
                                     else "CONSTRUCT",
                                     f"{ast.unparse(recv)[:40]}."
                                     f"{node.func.attr}({c.value!r})"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr in ("search", "match", "findall") \
                and node.args and isinstance(node.args[0], ast.Constant) \
                and node.args[0].value in vocab:
            hits.append((node.lineno, node.args[0].value, "CONSTRUCT",
                         f"re.{node.func.attr}({node.args[0].value!r}, ...)"))
    return hits


def their_rule_hits(src, vocab):
    """The parent's OWN rule, re-implemented, so that B4a/B4b measure the
    population question and not the rule question."""
    hvars = set()
    for l in src.split("\n"):
        m = re.match(r"\s*(\w+)\s*=.*heading\(", l)
        if m:
            hvars.add(m.group(1))
    quoted = re.compile(r"'[^']*'|`[^`]*`")
    out = []
    for i, l in enumerate(src.split("\n"), 1):
        s = l.strip()
        if "heading(" in s:
            continue
        bare = quoted.sub("", s)
        for name in vocab:
            m = re.search(rf'"{name}"\s+(?:not\s+)?in\s+(\w+)', bare)
            if m and m.group(1) not in hvars:
                out.append((i, name, s))
                break
    return out


def their_vocabulary():
    """The parent's own `ROW_NAMES`, read out of its source by AST rather than
    copied by hand -- so that "a hand list of five" is a measurement of their
    file and not a claim about it."""
    src = read_rel("code/hodge_leverage_repair_6df0/repair_ec07.py")
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Assign) \
                and any(getattr(t, "id", "") == "ROW_NAMES"
                        for t in node.targets):
            return [e.value for e in node.value.elts]
    return []


def exposure(rows, name):
    """How many gate rows the SUBSTRING test selects that a HEADING test does
    not.  A property of the rows, so it is the same wherever the hit lives."""
    sub = [d for d in rows if name in d]
    hd = [d for d in rows if name in d.split(" -- ")[0]]
    return len(sub), len(hd)


def py_files_at(commit):
    return sorted(p for p in git("ls-tree", "-r", "--name-only", commit,
                                 "--", "code").split("\n")
                  if p.endswith(".py"))


def b4(rows_head):
    head("B4 -- THE CONSTRUCT: HOW MANY EXIST, HOW MANY THE REPAIR TOUCHED")
    vocab = row_vocabulary()
    theirs_vocab = their_vocabulary()
    print(f"    row vocabulary, DERIVED from the code that prints the rows: "
          f"{vocab}")
    print(f"    the parent's `ROW_NAMES`, a HAND LIST read out of its source: "
          f"{theirs_vocab}")
    print(f"    in the derived vocabulary and not in the hand list: "
          f"{sorted(set(vocab) - set(theirs_vocab))}")
    fix, pre = repair_commits()

    # ⚠️ THE POPULATION IS THE TREE THE REPAIR SHIPPED IN, not HEAD: at HEAD
    # this audit's own probe file has joined it, and a sweep that counts the
    # file doing the counting is mg-ec07's own B0.  HEAD is reported beside it.
    at_fix = py_files_at(fix)
    at_probe = py_files_at(pre)
    at_head = py_files_at("HEAD")
    published = 429
    record(None,
           f"B4a `.py` files under `code/`: {len(at_fix)} at {fix[:7]}, the "
           f"commit that SHIPS the transcript; {len(at_probe)} at its parent "
           f"{pre[:7]}, the commit the repair was measured against; and "
           f"{len(at_head)} at HEAD, which is {len(at_head) - len(at_fix)} more "
           f"because this audit's own probe file has joined the population it "
           f"counts.  The committed transcript publishes {published}")
    if len(at_fix) != published:
        finding("F2", f"THE SWEEP'S OWN POPULATION IS A STALE FIGURE AT ITS "
                      f"OWN COMMIT.  `out_repair_6df0.txt` publishes "
                      f"'{published} .py files swept'; the tree at the commit "
                      f"that ships that transcript holds {len(at_fix)}, and so "
                      f"did the commit before it ({len(at_probe)}) -- so the "
                      f"gap is not a merge that landed after the run, it was "
                      f"already there when the run was taken.  "
                      f"{len(at_fix) - published} files are in the population "
                      f"and not in the number a reader is given.  The "
                      f"instrument is live and re-derives the count every run; "
                      f"what is frozen is the figure in the evidence.  This is "
                      f"mg-f922 B/C -- a figure stale in the commit that "
                      f"publishes it -- inside the sweep whose whole argument "
                      f"is that THE REPORTED LINE IS NEVER THE POPULATION")

    def sweep(commit, files):
        mine, theirs, theirs_own = [], [], []
        for rel in files:
            src = git("show", f"{commit}:{rel}")
            for ln, name, cls, expr in ast_hits(src, vocab):
                mine.append((rel, ln, name, cls, expr))
            for ln, name, s in their_rule_hits(src, vocab):
                theirs.append((rel, ln, name, s))
            for ln, name, s in their_rule_hits(src, theirs_vocab):
                theirs_own.append((rel, ln, name, s))
        return mine, theirs, theirs_own

    mine_head, theirs_head, own_head = sweep(fix, at_fix)
    mine_pre, theirs_pre, own_pre = sweep(pre, at_probe)

    con_head = [h for h in mine_head if h[3] == "CONSTRUCT"]
    con_pre = [h for h in mine_pre if h[3] == "CONSTRUCT"]
    print()
    print(f"    THE CONSTRUCT AT {fix[:7]}, by my rule, with each hit's "
          f"EXPOSURE over the 34 live rows:")
    for rel, ln, name, cls, expr in sorted(con_head):
        nsub, nhd = exposure([d for _ok, d in rows_head], name)
        print(f"      {rel}:{ln}")
        print(f"          {expr}")
        print(f"          exposure: {nsub} of 34 rows by substring, {nhd} by "
              f"heading -- {nsub - nhd} row(s) it was never meant to select"
              + ("" if nsub != nhd else "  (harmless here, and still the "
                                        "construct)"))
    print()
    print("    ... and the REMEDY sites, which are the same shape keyed "
          "correctly:")
    for rel, ln, name, cls, expr in sorted(h for h in mine_head
                                           if h[3] == "REMEDY"):
        print(f"      {rel}:{ln}  {expr}")
    print()
    record(None,
           f"B4c INSTANCES THAT EXIST at {fix[:7]}, over the same "
           f"{len(at_fix)} files, by three rules: {len(con_head)} by MY rule "
           f"(AST + derived vocabulary), {len(theirs_head)} by the PARENT'S "
           f"RULE with the derived vocabulary, and {len(own_head)} by the "
           f"parent's rule with its OWN hand list of "
           f"{len(theirs_vocab)} names -- which is the number its transcript "
           f"publishes.  THE RULE IS NOT WHAT HIDES THE EXTRA ONE; THE HAND "
           f"LIST IS")
    if len(own_head) < len(con_head):
        hidden = [h for h in con_head if h[2] not in theirs_vocab]
        finding("F5", f"THE SWEEP'S VOCABULARY IS A HAND LIST, WHICH IS A "
                      f"SCOPE NOBODY CHOSE ONE LEVEL UP.  `ROW_NAMES` in "
                      f"`repair_ec07.py` names {len(theirs_vocab)} row "
                      f"headings by hand; the gate prints {len(vocab)}.  The "
                      f"same rule with a vocabulary derived from the code that "
                      f"prints the rows finds {len(con_head)} occurrences "
                      f"where the hand list finds {len(own_head)}: "
                      + "; ".join(f"{r}:{l} `{e}`"
                                  for r, l, _n, _c, e in hidden)
                      + ".  The sweep exists because a hand-picked SITE is a "
                        "scope nobody chose; it picks its VOCABULARY the same "
                        "way")

    touched = [h for h in con_pre if (h[0], h[2], h[4]) not in
               {(x[0], x[2], x[4]) for x in con_head}]
    record(None,
           f"B4d INSTANCES THE REPAIR TOUCHED: {len(touched)} -- "
           + ("; ".join(f"{r}:{l} {e}" for r, l, _n, _c, e in touched)
              or "none")
           + f".  THE TWO NUMBERS ARE THE FINDING: {len(con_pre)} instances "
             f"existed at {pre[:7]} and the repair changed {len(touched)} of "
             f"them, leaving {len(con_head)} live in the commit it landed in")
    if len(con_head) > 0:
        finding("F3", f"{len(con_head)} instance(s) of the construct are LIVE "
                      f"in the commit the repair landed in, after a repair "
                      f"that touched {len(touched)}.  Each carries a declared "
                      f"disposition in the parent's `DISPOSITIONS` table keyed "
                      f"on its exact line, so a new one anywhere is red -- but "
                      f"a disposition is a REASON, not a repair, and "
                      f"{len(touched)} of {len(con_pre)} is the scope the "
                      f"repair chose.  The brief asked for these two numbers "
                      f"and they are 1 and {len(con_pre)}")

    landing_hits = [h for h in mine_head if h[0] == LANDING_REL]
    landing_con = [h for h in landing_hits if h[3] == "CONSTRUCT"]
    record(not landing_con,
           f"B4e in `verify_landing.py` itself: {len(landing_hits)} row-"
           f"identifying comparison(s), {len(landing_con)} by substring and "
           f"{len(landing_hits) - len(landing_con)} through `heading()`.  The "
           f"claim under test is '`heading()` is now the only way any caller "
           f"in that file names a row'")

    # non-.py
    tracked = [p for p in git("ls-files").split("\n") if p and
               not p.endswith(".py")]
    shell = []
    for p in tracked:
        if not p.endswith((".sh", ".bash", ".zsh")):
            continue
        try:
            src = read_rel(p)
        except (OSError, UnicodeDecodeError):
            continue
        for i, l in enumerate(src.split("\n"), 1):
            if any(f'"{v}"' in l or f"'{v}'" in l for v in vocab) \
                    and re.search(r"\bgrep\b|\bcase\b|\[\[", l):
                shell.append((p, i, l.strip()))
    record(not shell,
           f"B4f shell runners keying on a gate row name: {len(shell)}.  The "
           f"parent's sweep is over `.py` under `code/` only, so a `grep "
           f"\"SITE RECORD\"` in a runner would be outside its population "
           f"entirely -- checked here rather than assumed")
    return con_head, touched


# --------------------------------------------------------------------------
# B5 -- THE SCOPE SENTENCES, EACH TESTED AT EVERY SITE
# --------------------------------------------------------------------------
def b5():
    head("B5 -- EVERY SCOPE SENTENCE THE REPAIR WRITES, TESTED AT EVERY SITE")
    print("""The sentence the repair INHERITED was false at 1 of 3 sites and nobody had
checked the third.  So each sentence it writes is read here as a CLAIM and
tried at all three, by an implementation written from the sentence rather than
from the code.
""")
    files = files_from_disk()
    mine = my_texts(files)
    theirs = V.site_texts()
    anchors = V.site_anchors()

    # B5a / B5b -- EXTENT_OF, sentence by sentence
    for fname, sentence in sorted(V.EXTENT_OF.items()):
        sites = [n for n in MY_NAMES if anchors[n] == fname]
        ok = all(mine[n] == theirs[n] for n in sites)
        record(ok,
               f"B5a `EXTENT_OF[{fname!r}]` -- \"{sentence[:70]}...\" -- "
               f"claimed of {len(sites)} site(s) ({', '.join(sites)}) and "
               f"reproduced from the sentence alone at "
               f"{sum(mine[n] == theirs[n] for n in sites)} of {len(sites)}")

    # THE TABLE THIS ROW IS A ROW OF -- walked out from the row itself, not
    # every pipe line in the file.
    lines = files["STATE.md"].split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith("| **AMBER-POSITIVE"))
    top, bot = i, i
    while top > 0 and lines[top - 1].startswith("|"):
        top -= 1
    while bot + 1 < len(lines) and lines[bot + 1].startswith("|"):
        bot += 1
    table = lines[top:bot + 1]
    body = [l for l in table if not re.fullmatch(r"\|[\s:|-]+\|", l.strip())]
    inside = [l for l in table if l in mine["the STATE.md row"].split("\n")]
    record(len(inside) == 3,
           f"B5b the framed_row sentence's SECOND HALF -- 'not the table's "
           f"other rows' -- the ledger table this row belongs to is "
           f"{len(table)} line(s), {len(body)} of them header-or-verdict rows; "
           f"{len(inside)} lines are inside the site.  "
           f"{len(body) - (len(inside) - 1)} verdict rows of this table remain "
           f"outside every record, which is mg-ec07's X2 and is declared open "
           f"with its cost measured")

    # B5c -- fail-closed on an anchor with no declared extent
    src = inject(BASELINE[LANDING_REL], '''

# ---- mg-7e39 probe: an anchor whose function has NO declared extent ----
def framed_row_mg7e39(text, prefix):
    return framed_row(text, prefix)


ANCHORS[0] = (ANCHORS[0][0], ANCHORS[0][1], framed_row_mg7e39,
              ANCHORS[0][3], ANCHORS[0][4])
''')
    write_rel(LANDING_REL, src)
    try:
        rc, out = run_runner()
    finally:
        if not restore():
            raise SystemExit("FAIL-CLOSED: the tree did not restore")
    red = any("DECLARED extent" in l and "REFUTED" in l
              for l in out.split("\n"))
    record(rc == 1 and red,
           f"B5c 'a site whose anchor has no declared extent makes the run "
           f"RED' -- the cutting function renamed and nothing else changed: "
           f"exit {rc}, the DECLARED extent row "
           f"{'REFUTED' if red else 'still green'}.  A fail-closed rule that "
           f"cannot be made to fail is a sentence")

    # B5d -- contiguity
    contig = {n: files[dict((a, b) for a, b, _c, _d, _e in MY_SITES)[n]]
              .count(mine[n]) for n in MY_NAMES}
    record(sum(1 for v in contig.values() if v == 0) == 1,
           f"B5d 'a site is no longer a CONTIGUOUS SUBSTRING of its file at 1 "
           f"of 3 sites' -- occurrences of each site in its own file: "
           + ", ".join(f"{n} {v}" for n, v in contig.items())
           + ".  Exactly the sites with 0 are non-contiguous")

    # B5e -- the record grew by 43, and the reseal diff is two lines
    fix, pre = repair_commits()
    pre_mod = blob_module(pre, "vl_pre_7e39")
    old = sum(len(t) for t in pre_mod.site_texts().values())
    new = sum(len(t) for t in mine.values())
    diff = git("show", "--numstat", "--format=", fix, "--", RECORDS_REL).split()
    record(new - old == 43,
           f"B5e the record population: {old:,} -> {new:,} chars, +{new - old}."
           f"  The repair states 43 and states the `site_records.txt` diff as "
           f"exactly two added lines; the diff is "
           f"+{diff[0] if diff else '?'}/-{diff[1] if len(diff) > 1 else '?'}"
           f" line(s)")

    # B5f -- the residue
    files_all = sum(len(files[p]) for p in MY_FILES)
    inside_all = sum(len(t) for t in mine.values())
    outside = files_all - inside_all
    record(outside == 282600 and files_all == 320509,
           f"B5f the residue, re-derived: {inside_all:,} of {files_all:,} "
           f"chars of the three files are inside a record "
           f"({100.0 * inside_all / files_all:.1f}%); {outside:,} are outside "
           f"every record ({100.0 * outside / files_all:.1f}%).  The repair "
           f"states 282 600 of 320 509 and 88.2%")

    # B5g -- 'the mutation goes through the FILE'
    src_l = BASELINE[LANDING_REL]
    km = src_l[src_l.index("def kind_matrix("):src_l.index("def negative_control(")]
    nc = src_l[src_l.index("def negative_control("):]
    through_file = km.count("with_site(") + nc.count("with_site(")
    in_memory = len(re.findall(r"figure_gate\((?!texts\b)", nc))
    cells = len(V.KINDS) * len(V.SITES)
    record(None,
           f"B5g 'the negative control now MUTATES THE FILE and re-cuts the "
           f"sites from it' -- `kind_matrix`, called from `negative_control`, "
           f"routes all {cells} of its attempts through `with_site` "
           f"({through_file} call site(s) in the two functions).  The "
           f"{in_memory} further `figure_gate(...)` probes in "
           f"`negative_control`'s OWN body are still handed MUTATED SITE TEXTS "
           f"in memory.  Measured, not argued")
    if in_memory:
        finding("F4", f"the repair's own commit message says THE NEGATIVE "
                      f"CONTROL NOW MUTATES THE FILE AND RE-CUTS THE SITES "
                      f"FROM IT.  The SITES x KINDS matrix it added does -- "
                      f"all {cells} attempts go through `with_site`.  The "
                      f"{in_memory} probes in `negative_control`'s own body do "
                      f"not: they still mutate site TEXT in memory, which is "
                      f"the construction the repair itself names as unable to "
                      f"exhibit a site-boundary defect ('a battery that "
                      f"mutates site texts in place cannot exhibit a "
                      f"site-boundary defect').  The claim is true of the part "
                      f"the repair built and is written of the whole "
                      f"function.  The 19 probes are figure-side, so nothing "
                      f"below them is known to be missed -- what is wrong is "
                      f"the scope of the sentence, which is this repair's own "
                      f"subject")


# --------------------------------------------------------------------------
# B6 -- DO NOT DISTURB WHAT IS CONFIRMED
# --------------------------------------------------------------------------
NAIVE_FIG = re.compile(r"(?<![\d])[−+]?\d{1,3}(?:[  ]\d{3})+(?![\d])")


def b6():
    head("B6 -- DO NOT DISTURB: the byte census and the exchange census, "
         "re-derived")
    print("""⚠️  A FIXTURE, declared: B6 calls the gate on strings in memory, as mg-ec07's
A1 did.  B1 and B3 are the on-disk evidence.  The POPULATION here is mine --
every character of every site, and every unordered pair of asserted figure
slots with differing values -- and the seam that says what an asserted figure
IS remains the artifact's `partition`, because that seam is the definition
under audit.  The token counts are cross-checked against a naive regex of my
own below.
""")
    fix, pre_c = census_commits()
    PRE = blob_module(pre_c, "vl_census_pre_7e39")
    print(f"    the census lands at   : {fix[:7]}")
    print(f"    the control runs at   : {pre_c[:7]}  (lossless not yet true)")
    # memoize the declared record: a pure read of a file that does not change
    # during this run, called once per mutation otherwise.
    cache = V.declared_records()
    V.declared_records = lambda: cache
    if hasattr(PRE, "declared_records"):
        pcache = PRE.declared_records()
        PRE.declared_records = lambda: pcache

    measured = measured_now()
    texts = my_texts(files_from_disk())
    tot = {"n": 0, "head": 0, "pre": 0}
    per_row = {}
    for name in MY_NAMES:
        raw = texts[name]
        toks = V.partition(raw)[1]
        naive = set(NAIVE_FIG.findall(raw))
        missed = sorted({t for t in toks if t not in naive})
        print(f"    {name:<20} {len(raw):>7,} chars   asserted figure slots "
              f"{len(toks):>3} (`partition`)   {len(naive):>3} distinct by my "
              f"naive regex; it misses {len(missed)} distinct token(s) of the "
              f"form it does not spell ({', '.join(missed[:3]) or 'none'}) -- "
              f"the SIGNED-RUN form `+755`, which is why the seam stays theirs")
        nhead = npre = 0
        for i in range(len(raw)):
            mut = raw[:i] + ("X" if raw[i] != "X" else "Y") + raw[i + 1:]
            bad = [d for ok, d in V.census_gate(name, mut, measured) if not ok]
            if bad:
                nhead += 1
                for d in bad:
                    k = row_kind(d)
                    per_row[k] = per_row.get(k, 0) + 1
            if any(not ok for ok, _ in PRE.census_gate(name, mut, measured)):
                npre += 1
        record(nhead == len(raw),
               f"B6a {name}: {nhead} of {len(raw)} characters of this site "
               f"cannot be substituted in silence")
        record(None,
               f"B6b-control {name}: the SAME instrument against the gate at "
               f"{pre_c[:7]} catches {npre} of {len(raw)} "
               f"({100.0 * npre / len(raw):.1f}%)")
        tot["n"] += len(raw)
        tot["head"] += nhead
        tot["pre"] += npre
    record(tot["head"] == tot["n"],
           f"B6a TOTAL {tot['head']} of {tot['n']} characters over the 3 sites "
           f"fire at HEAD.  mg-ec07 confirmed 37 866 of 37 866; the population "
           f"is now {tot['n']} because the repair widened the STATE.md site by "
           f"43 characters.  REPORTING IT AS 37 866 WOULD BE THE STALE FIGURE "
           f"ONE LEVEL UP")
    record(tot["pre"] == 462,
           f"B6b TOTAL {tot['pre']} of {tot['n']} fire against the pre-census "
           f"gate at {pre_c[:7]} -- {100.0 * tot['pre'] / tot['n']:.1f}% "
           f"against {100.0 * tot['head'] / tot['n']:.1f}%.  mg-ec07 measured "
           f"462 of 37 866; the 43 new characters are a markdown header and "
           f"delimiter carrying no figure token, so the control does not move")
    print()
    for k in sorted(per_row, key=lambda x: -per_row[x]):
        print(f"      {k:<20} {per_row[k]:>6}")
    record(per_row.get("RECORD PARTITION", 0) == 0,
           f"B6c RECORD PARTITION fires on {per_row.get('RECORD PARTITION', 0)}"
           f" of {tot['n']} point mutations -- unfalsifiable by any document "
           f"edit, which is why B3 had to bend the CODE to move it")

    # the exchange census
    head("B6d -- 847 FIGURE EXCHANGES, RE-ENUMERATED")
    tot_ex = fired = ford = srec = rpart = 0
    per_site = []
    for name in MY_NAMES:
        raw = texts[name]
        seg, figs = V.partition(raw)
        pairs = [(i, j) for i, j in itertools.combinations(range(len(figs)), 2)
                 if figs[i] != figs[j]]
        n = 0
        for i, j in pairs:
            f = list(figs)
            f[i], f[j] = f[j], f[i]
            mut = V.rejoin(seg, f)
            rows = V.census_gate(name, mut, measured)
            bad = {row_kind(d) for ok, d in rows if not ok}
            good = {row_kind(d) for ok, d in rows if ok}
            n += bool(bad)
            ford += "FIGURE ORDER" in bad
            srec += "SITE RECORD" in good and "SITE RECORD" not in bad
            rpart += "RECORD PARTITION" in good and "RECORD PARTITION" not in bad
        per_site.append((name, n, len(pairs)))
        tot_ex += len(pairs)
        fired += n
    record(fired == tot_ex and tot_ex == 847,
           f"B6d {fired} of {tot_ex} figure exchanges fire -- "
           + " / ".join(f"{n} of {t} at {s}" for s, n, t in per_site)
           + f".  mg-ec07 confirmed 847 of 847 (127/116/604) and the two lines "
             f"the STATE.md site gained carry no figure token, so the "
             f"population does not move")
    record(ford == tot_ex and srec == tot_ex and rpart == tot_ex,
           f"B6e on those {tot_ex}: FIGURE ORDER refuted on {ford}, SITE "
           f"RECORD green on {srec}, RECORD PARTITION green on {rpart}.  The "
           f"attribution mg-9207 established is undisturbed")


# --------------------------------------------------------------------------
# B7 -- THIS DELIVERABLE, CHECKED FOR THE DEFECT IT AUDITS
# --------------------------------------------------------------------------
def b7(con_head):
    head("B7 -- THIS DELIVERABLE, CHECKED FOR THE DEFECT IT AUDITS")
    mine = os.path.relpath(os.path.abspath(__file__), REPO)
    first = git("log", "--reverse", "--format=%H", "--", mine).split()
    trans = git("log", "--reverse", "--format=%H", "--",
                os.path.join(os.path.dirname(mine),
                             "out_audit_7e39.txt")).split()
    record(bool(first) and (not trans or first[0] != trans[0]),
           f"B7a the probe file and the predictions precede the transcript in "
           f"git: probe first appears at "
           f"{first[0][:7] if first else '(uncommitted)'}, transcript at "
           f"{trans[0][:7] if trans else '(uncommitted)'}.  Re-derived from "
           f"`git log`, not asserted")
    src = read_rel(mine)
    vocab = row_vocabulary()
    hits = ast_hits(src, vocab)
    con = [h for h in hits if h[2] == "CONSTRUCT"]
    print(f"    my own row-identifying comparisons: {len(hits)}, of which "
          f"{len(con)} by substring")
    for ln, name, cls, expr in con:
        print(f"      {mine}:{ln}  {expr}")
    record(len(con) <= 2,
           f"B7b this instrument contains {len(con)} substring comparison(s) "
           f"against a row name, and each is B3a MEASURING the substring test "
           f"itself -- declared, because measuring the defect is not "
           f"committing it.  Every other row identification here goes through "
           f"`row_kind`, my own heading parse")


# --------------------------------------------------------------------------
def main():
    print("mg-7e39 -- INDEPENDENT AUDIT of the mg-6df0 repair")
    print("=" * 78)
    print(__doc__.split("\n", 1)[1].strip())
    snapshot()
    fix, pre = repair_commits()
    print()
    print(f"  repair under audit : {fix[:7]}   (parent {pre[:7]})")
    print(f"  tree              : {git('rev-parse', 'HEAD').strip()[:7]}")
    live = measured_now()
    rows = b0()
    cells = b1(live)
    theirs = b1e(cells)
    b2(cells, theirs, live)
    b3(rows)
    con_head, touched = b4(rows)
    b5()
    b6()
    b7(con_head)

    head("BOTTOM LINE")
    bad = [t for t, ok in RESULTS if ok is False]
    print(f"  checks recorded : {len(RESULTS)}")
    print(f"  measurements    : {sum(1 for _, ok in RESULTS if ok is None)}")
    print(f"  confirmed       : {sum(1 for _, ok in RESULTS if ok is True)}")
    print(f"  refuted         : {len(bad)}")
    print(f"  findings        : {len(FINDINGS)}")
    print()
    for tag, d in FINDINGS:
        print(f"    {tag}: {d[:160]}")
    print()
    if not restore():
        print("  THE TREE DID NOT RESTORE -- fail-closed")
        return 2
    print("  the three site files, verify_landing.py and site_records.txt are "
          "restored byte-identical")
    if bad:
        print()
        print("  REFUTED:")
        for t in bad:
            print(f"    - {t}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
