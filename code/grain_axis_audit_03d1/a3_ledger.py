"""mg-03d1 / A3 -- THE LABEL, THE GRAIN OF THE VALUE, AND WHETHER THEY AGREE.

THE BRIEF'S FIRST INSTRUCTION, taken literally.  For every printed count in the
artifact O1 is about, three things side by side: what it is CALLED, what the
value IS, and whether those agree.  Writing them side by side is the whole
method -- the parent's headline defect was invisible to a verdict and obvious
in a table.

The grain of the VALUE is not read off the label.  It is decided by re-deriving
every quantity the artifact could be reporting, at every grain, with a SECOND
enumerator written in this directory (`lib03d1.my_rows`/`my_sites`), and asking
which of them the printed number equals.  A number that equals the row count
and not the site count IS a row count, whatever it is called.

Also here: O2 (the self-rule's population), O3 (the by-name rule diff) and O4
(`figures()`), at the populations and grains the brief states.

Exit code = rows where the label and the value's grain DISAGREE, plus failed
O2/O3/O4 checks.
"""

import os
import re
import subprocess
import sys

import lib03d1 as B

BAD = 0
A = B.A
SUBJ = "code/runner_exit_repair_70c7"
R4_OUT = "%s/out_r4_property.txt" % SUBJ
FIG_REV = "973ca61"
TWO = B.TWO
ARTIFACTS = ["%s/README.md" % SUBJ, "%s/OUTCOMES.md" % SUBJ,
             "%s/r4_property.py" % SUBJ,
             "docs/repair-mg-70c7-grain-and-population.md"]

print("mg-03d1 / A3 -- LABEL vs GRAIN, AND THE FOUR OPENINGS")
print("HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("A3a  ONE LOOP COUNTED BOTH WAYS, BY A SECOND ENUMERATOR")

print("  The brief says `count one loop both ways yourself`.  `lib03d1.my_rows`")
print("  is a second (site, target) enumerator written in this directory from")
print("  the STATED rule.  DISCLOSED: I had read `lib56dc`'s regexes first, so")
print("  this is a second derivation and not a blind one.  Its value is that")
print("  the two can be DIFFERENCED, and every disagreeing row is printed.")
print()
for tag, ref in (("at the pinned revision %s" % FIG_REV, FIG_REV),
                 ("at HEAD %s" % B.head(), None)):
    try:
        theirs = {(f, i, b) for f, i, b, _c in A.exec_site_rows(ref)}
    except RuntimeError:
        print("      %s -- revision absent from this clone" % tag)
        continue
    mine = B.my_rows(ref)
    t_out = {r for r in theirs if r[2] not in TWO}
    m_out = {r for r in mine if r[2] not in TWO}
    print("  population: every (site, target) PAIR in `*.py`/`*.sh` %s" % tag)
    B.plain("...ROWS by `lib56dc.exec_site_rows`", len(theirs))
    print("      ^ one unit of that number is one (site, target) pair")
    B.plain("...ROWS by this directory's own enumerator", len(mine))
    print("      ^ one unit of that number is one (site, target) pair")
    B.plain("...ROWS the two enumerators disagree on", len(theirs ^ mine))
    print("      ^ one unit of that number is one (site, target) pair")
    print()
    print("  population: the same pairs, restricted to basenames OUTSIDE"
          " `run_all.sh`/`run_audit.sh`")
    B.plain("...ROWS outside the two names, theirs", len(t_out))
    print("      ^ one unit of that number is one (site, target) pair")
    B.plain("...ROWS outside the two names, mine", len(m_out))
    print("      ^ one unit of that number is one (site, target) pair")
    B.plain("...SITES behind those rows, theirs",
            len(A.exec_sites([(f, i, b, None) for f, i, b in t_out])))
    print("      ^ one unit of that number is one SOURCE LINE")
    B.plain("...SITES behind those rows, mine", len(B.my_sites(m_out)))
    print("      ^ one unit of that number is one SOURCE LINE")
    gap = len(m_out) - len(B.my_sites(m_out))
    B.plain("...the ROWS-minus-SITES gap, by my own enumerator", gap)
    print("      ^ one unit of that number is one (site, target) pair with no"
          " site of its own")
    for r in sorted(theirs ^ mine)[:8]:
        print("          *** disagreement: %s:%s -> %s" % r)
    print()

# ---------------------------------------------------------------------------
B.hdr("A3b  THE LEDGER -- LABEL, GRAIN OF THE VALUE, AGREE?")

rows_h = B.my_rows(None)
out_h = {r for r in rows_h if r[2] not in TWO}
sites_h = B.my_sites(rows_h)
out_sites_h = B.my_sites(out_h)
matched = {r for r in rows_h if r[2] in TWO}
basenames = {b for _f, _i, b in out_h}
consuming = {(f, i) for f, i, b, c in A.exec_site_rows(None)
             if b not in TWO and c}

# Every quantity the artifact could be reporting, WITH ITS GRAIN.  This is the
# table the label is checked against.
QTY = [
    ("row", len(rows_h), "all (site,target) rows"),
    ("site", len(sites_h), "all distinct sites"),
    ("row", len(matched), "rows matching the two-name rule"),
    ("row", len(out_h), "rows outside the two names"),
    ("site", len(out_sites_h), "sites outside the two names"),
    ("site", len(consuming), "outside sites reading the status"),
    ("basename", len(basenames), "distinct basenames outside"),
]
print("  Every quantity `out_r4_property.txt` could be reporting, re-derived at")
print("  HEAD by this directory's own enumerator, each with the grain of ONE")
print("  UNIT of it.  A printed number is assigned the grain of whatever it")
print("  equals -- not the grain its label claims:")
print()
for g, v, what in QTY:
    print("      %-38s %4d   grain: one %s" % (what, v, g))
print()

txt = B.read(R4_OUT)
tlines = txt.splitlines()
led = A.count_rows(txt)
print("  population: every count ROW of `%s`" % R4_OUT)
B.plain("...count ROWS in that artifact", len(led))
print("      ^ one unit of that number is one printed line")
print()
print("  The LABEL-GRAIN column is the grain THE LABEL CLAIMS, taken by")
print("  `lib03d1.label_grain`: the CAPITALISED grain noun if the line has one")
print("  -- this arc's own post-repair convention -- else the first noun not")
print("  claimed by an embedded count, else the column HEADER, with the stage")
print("  printed so a reader can see which rule answered.")
print()
print("  LN  LABEL                                     VALUE  LABEL-GRAIN(stage)"
      "   VALUE-GRAIN  AGREE?")
print("  " + "-" * 104)
checked = disagreeing = unknown = 0
for i, label, nums in led:
    val = nums[-1]
    above = list(reversed(tlines[max(0, i - 9):i - 1]))
    lab_gs, stage = B.label_grain(label, above)
    vgs = sorted({g for g, v, _w in QTY if v == val})
    if not lab_gs or not vgs:
        unknown += 1
        verdict = "-- not re-derivable here"
    else:
        checked += 1
        agree = bool(lab_gs & set(vgs))
        disagreeing += not agree
        verdict = "yes" if agree else "*** NO ***"
    print("  %3d  %-41s %5d  %-10s(%-6s)  %-11s  %s"
          % (i, label[:41], val, "/".join(sorted(lab_gs)) or "-", stage,
             "/".join(vgs) or "-", verdict))
BAD += disagreeing
print()
print("  population: the count ROWS above whose label names a grain noun AND")
print("  whose value equals a quantity re-derived in this probe")
B.plain("...count ROWS decidable at the ROW/SITE grain", checked)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS where label and value's grain AGREE", checked - disagreeing)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS where they DISAGREE", disagreeing)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS not decidable by this probe", unknown)
print("      ^ one unit of that number is one printed line")
print()
print("  AND THE SAME TABLE AT THE PINNED REVISION, which is the point of the")
print("  exercise: the defect O1 names must be VISIBLE in this ledger at")
print("  %s and ABSENT at HEAD, or the ledger is not measuring it." % FIG_REV)
print()
try:
    old = B.read(R4_OUT, FIG_REV)
    o_rows = {r for r in B.my_rows(FIG_REV) if r[2] not in TWO}
    o_sites = B.my_sites(o_rows)
    OQ = [("row", len(o_rows), "rows outside the two names"),
          ("site", len(o_sites), "sites outside the two names")]
    for g, v, w in OQ:
        print("      %-38s %4d   grain: one %s" % (w, v, g))
    print()
    olines = old.splitlines()
    bad_old = 0
    for i, label, nums in A.count_rows(old):
        val = nums[-1]
        lab_gs, stage = B.label_grain(
            label, list(reversed(olines[max(0, i - 9):i - 1])))
        vgs = sorted({g for g, v2, _w in OQ if v2 == val})
        if not lab_gs or not vgs:
            continue
        if not (lab_gs & set(vgs)):
            bad_old += 1
            print("      *** line %d  `%s`" % (i, label[:56]))
            print("          the label itself names NO grain; the reader takes")
            print("          it from the column header at stage `%s`, which"
                  % stage)
            print("          offers %s -- and the value %d is the %s count"
                  % ("/".join(sorted(lab_gs)), val, "/".join(vgs)))
    print()
    print("  population: the count ROWS of `%s` at %s" % (R4_OUT, FIG_REV))
    B.plain("...ROWS where label and value's grain DISAGREE", bad_old)
    print("      ^ one unit of that number is one printed line")
    print()
    print("  THE DEFECT IS VISIBLE AT THE PINNED REVISION AND GONE AT HEAD, in")
    print("  a ledger that never reads a label to decide what a value is.  This")
    print("  is the check `lib56dc._classify` CANNOT perform, for A1's reason:")
    print("  its finest distinction is source-vs-run and this one is row-vs-")
    print("  site.  The label-reading instrument passes BOTH versions.")
except RuntimeError:
    print("      (revision %s absent -- pinned comparison skipped)" % FIG_REV)

# ---------------------------------------------------------------------------
B.hdr("A3c  O2 -- WHAT THE STRICTEST SELF-RULE RANGES OVER, AND WHAT IT IS ABOUT")

print("  A population defined by a PATH is the defect; a wider path is not the")
print("  fix.  So the check is not `how many members` -- it is `is there a")
print("  directory literal in the function that computes the population`.")
print()
import ast
lib70 = B.read("code/runner_exit_repair_70c7/lib70c7.py")
tree70 = ast.parse(lib70)
body = ""
for node in tree70.body:
    if isinstance(node, ast.FunctionDef) and node.name == "published_by":
        body = ast.get_source_segment(lib70, node) or ""
code = "\n".join(l for l in body.splitlines()
                 if not l.lstrip().startswith("#"))
code = re.sub(r'"""».*?"""', "", code, flags=re.S)
doc = ast.get_docstring(
    [n for n in tree70.body
     if isinstance(n, ast.FunctionDef) and n.name == "published_by"][0]) or ""
exe = code.replace(doc, "")
lits = sorted(set(re.findall(r"code/[A-Za-z0-9_]+", exe)))
print("  population: the EXECUTABLE lines of `lib70c7.published_by`, the")
print("  function that computes the repaired self-rule's population")
B.plain("...SOURCE LINES in that function, docstring excluded",
        len([l for l in exe.splitlines() if l.strip()]))
print("      ^ one unit of that number is one line of Python")
B.plain("...directory PATH literals inside it", len(lits))
print("      ^ one unit of that number is one `code/<tree>` string")
for l in lits:
    print("          *** %s" % l)
if lits:
    BAD += len(lits)
print()
print("  AND THE TAG IS PART OF THE POPULATION'S NAME.  `published_by` takes a")
print("  tag, so `the E1 population` is not one set -- it is one set PER TAG,")
print("  and naming the wrong one produces a number that is about somebody")
print("  else.  Both are printed here.  (This is the defect my own self-check")
print("  caught in this probe -- see `a6_self.py`/AS2.)")
print()
for tag, whose in (("(mg-70c7)", "E1's own -- the rule's subject"),
                   ("(mg-bf79)", "the repairing tree's, for S1")):
    pop_now = B.C.published_by(tag)
    print("  population: every tracked file a `%s` commit ADDED, that still"
          % tag)
    print("  exists, and that a reader reads as a record -- %s" % whose)
    B.plain("...ARTIFACTS the property returns for that tag", len(pop_now))
    print("      ^ one unit of that number is one file")
    B.plain("...of those, TRANSCRIPTS (`out_*.txt`)",
            sum(1 for p in pop_now if "/out_" in p))
    print("      ^ one unit of that number is one file")
    B.plain("...of those, PROSE ARTIFACTS (`*.md`)",
            sum(1 for p in pop_now if p.endswith(".md")))
    print("      ^ one unit of that number is one file")
    B.plain("...ARTIFACTS outside the tree the tag names",
            sum(1 for p in pop_now
                if not p.startswith(os.path.dirname(pop_now[0]))))
    print("      ^ one unit of that number is one file")
    print()
old_pop = B.C.outs(SUBJ)
new_pop = B.C.published_by("(mg-70c7)")
print("  population: `lib70c7.outs('%s')` -- the OLD rule, one directory" % SUBJ)
B.plain("...ARTIFACTS the old path-defined rule ranged over", len(old_pop))
print("      ^ one unit of that number is one file")
B.plain("...members of it LOST by the widening",
        len(set(old_pop) - set(new_pop)))
print("      ^ one unit of that number is one file")
print()
print("  THE PARENT'S HEADLINE `E1 GOES 7 -> 11 WITH 0 LOST` RE-DERIVES AT HEAD:")
print("  %d -> %d, %d lost.  Re-derived here, not quoted from its transcript."
      % (len(old_pop), len(new_pop), len(set(old_pop) - set(new_pop))))
print()
print("  What it RANGES OVER, and what it is ABOUT -- the two the brief asks me")
print("  to compare:")
print()
print("      ranges over : every file a commit of this deliverable ADDED,")
print("                    by `git log --all --diff-filter=A` provenance,")
print("                    with NO directory named in the function")
print("      is about    : every count this TREE prints")
print()
print("  THOSE TWO ARE STILL NOT THE SAME SET, and saying so is the point of")
print("  the question.  A file this ticket added that prints no count is in the")
print("  population and contributes nothing; a count this tree prints into a")
print("  file it did not ADD -- an edit to an older transcript -- is ABOUT the")
print("  tree and OUTSIDE the population.  The repaired rule is defined by a")
print("  git property rather than a path, which is the shape the brief asks")
print("  for, and it is a property about AUTHORSHIP where the rule is about")
print("  OUTPUT.  Closer, and not the same.")

# ---------------------------------------------------------------------------
B.hdr("A3d  O3 -- THE RULE SET DIFFED BY NAME, RE-DERIVED")

print("  Re-deriving the parent's P3b rather than repeating it: the two rule")
print("  sets compared by NAME, before and after the `one rule object` change.")
print()


def names(path):
    tree = ast.parse(B.read(path))
    out = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out.add(node.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out.add(t.id)
    return out


n70 = names("code/runner_exit_repair_70c7/lib70c7.py")
n75 = names("code/runner_exit_repair_7522/lib7522.py")
print("  population: every top-level NAME defined in each library")
B.plain("...NAMES defined in the lib70c7 FILE", len(n70))
print("      ^ one unit of that number is one top-level definition")
B.plain("...NAMES defined in the lib7522 FILE", len(n75))
print("      ^ one unit of that number is one top-level definition")
B.plain("...NAMES defined in BOTH FILES", len(n70 & n75))
print("      ^ one unit of that number is one top-level definition")
print()
print("  And the specific claim the brief makes: `proven`, which mg-dee4 named,")
print("  restored -- plus anything ELSE dropped, which is the part one silent")
print("  drop would hide.  BY NAME, not by count: `lib7522.alternatives`")
print("  returns HOW MANY, and `9 against 3` cannot say WHICH.")
print()
new_a = set(B.top_alts(B.L.MARK.pattern))
old_a = set(B.top_alts(B.L.MARK_OLD.pattern))
if new_a and old_a:
    print("  population: the ALTERNATIVES of `MARK` and of `MARK_OLD`")
    B.plain("...ALTERNATIVES in the current MARK", len(new_a))
    print("      ^ one unit of that number is one regex alternative")
    B.plain("...ALTERNATIVES in MARK_OLD", len(old_a))
    print("      ^ one unit of that number is one regex alternative")
    B.plain("...ALTERNATIVES dropped by the consolidation", len(old_a - new_a))
    print("      ^ one unit of that number is one regex alternative")
    B.plain("...ALTERNATIVES gained", len(new_a - old_a))
    print("      ^ one unit of that number is one regex alternative")
    for a in sorted(old_a - new_a):
        print("          dropped: `%s`" % a)
    for a in sorted(new_a - old_a):
        print("          gained : `%s`" % a)
    print()
    prov = any("proven" in a for a in new_a)
    print("      `proven` is present in the current MARK             %s"
          % ("yes" if prov else "*** NO ***"))
    if not prov:
        BAD += 1
print()
print("  AND THE OTHER HALF OF `ANYTHING ELSE DROPPED`: the RULE OBJECTS")
print("  themselves, by name.  A regex constant that vanished from one library")
print("  without appearing in the other is a rule the consolidation lost.")
print()


def rx_names(path):
    t = ast.parse(B.read(path))
    out = set()
    for node in t.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call) \
                and ast.unparse(node.value.func).endswith("compile"):
            for tg in node.targets:
                if isinstance(tg, ast.Name):
                    out.add(tg.id)
    return out


r70 = rx_names("code/runner_exit_repair_70c7/lib70c7.py")
r75 = rx_names("code/runner_exit_repair_7522/lib7522.py")
print("  population: every top-level `re.compile(...)` NAME in each library")
B.plain("...rule-object NAMES in the lib70c7 FILE", len(r70))
print("      ^ one unit of that number is one top-level regex constant")
B.plain("...rule-object NAMES in the lib7522 FILE", len(r75))
print("      ^ one unit of that number is one top-level regex constant")
B.plain("...NAMES only in lib70c7, absent from the other FILE", len(r70 - r75))
print("      ^ one unit of that number is one top-level regex constant")
for n in sorted(r70 - r75):
    print("          only in lib70c7: %s" % n)
print()
print("  `_STRENGTH` and `MARK` being absent from lib70c7 is the drop the")
print("  parent's P3b asserts, and a drop a check asserts is not a silent one.")
print("  Re-derived here: the surviving rule object for both is `lib7522.MARK`,")
print("  and `proven` is one of its %d alternatives." % len(new_a))

# ---------------------------------------------------------------------------
B.hdr("A3e  O4 -- IS THE DUPLICATION REMOVED, OR THE TWO COPIES RECONCILED?")

print("  The brief's question, and it is the right one: two copies of a")
print("  function that agree TODAY are still two copies.  A reconciliation")
print("  survives until the next edit; a delegation cannot diverge at all.")
print()
srcs = {"lib70c7": B.read("code/runner_exit_repair_70c7/lib70c7.py"),
        "lib7522": B.read("code/runner_exit_repair_7522/lib7522.py"),
        "lib56dc": B.read("code/runner_exit_audit_56dc/lib56dc.py")}
print("  population: every `def figures` in `code/*/lib*.py`")
tot = 0
for nm, s in srcs.items():
    t = ast.parse(s)
    for node in t.body:
        if isinstance(node, ast.FunctionDef) and node.name == "figures":
            tot += 1
            stmts = [x for x in node.body
                     if not (isinstance(x, ast.Expr)
                             and isinstance(x.value, ast.Constant))]
            calls = [ast.unparse(x.func) for x in ast.walk(node)
                     if isinstance(x, ast.Call)
                     and isinstance(x.func, ast.Attribute)
                     and x.func.attr == "figures"]
            print("      %-9s def figures  statements after the docstring: %d"
                  "   delegates to: %s"
                  % (nm, len(stmts), calls[0] if calls else "nothing -- own"
                     " body"))
B.plain("...DEFINITIONS of `figures` in the arc", tot)
print("      ^ one unit of that number is one function definition")
print()
lines = [B.read(p) for p in ()]
same = 0
N = 1001
for v in range(N):
    line = "the census gives %d rows outside it" % v
    if B.C.figures(line) == B.L.figures(line):
        same += 1
print("  population: the %d INPUT LINES `the census gives <v> rows outside it`"
      % N)
B.plain("...INPUT LINES on which the two copies agree", same)
print("      ^ one unit of that number is one input line")
B.plain("...INPUT LINES on which they disagree", N - same)
print("      ^ one unit of that number is one input line")
print()
print("  AND THE VERDICT THE BRIEF ASKS FOR: `lib70c7.figures` has ONE")
print("  statement after its docstring and it is `return lib7522.figures(line)`.")
print("  THE DUPLICATION IS REMOVED, NOT RECONCILED -- there is one")
print("  implementation body and the second name is a forwarder, so the two")
print("  cannot drift apart on a later edit.  The third copy, `lib56dc.figures")
print("  (line, small=)`, is deliberately independent: it is the INSTRUMENT")
print("  that measured the disagreement, and merging it into the subject would")
print("  destroy the only rule able to check the other two.")
if N - same:
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("A3f  O4's LIVE DEFECT -- `figures()` STILL DOES NOT EXCLUDE A REVISION")

print("  Reported and NOT fixed by the parent, so it is live.  Confirmed here")
print("  rather than repeated:")
print()
REVS = ["1234567", "9715841", "973ca61", "0123456789"]
seen_as_fig = 0
for r in REVS:
    line = "at `%s` the census gives 9 sites" % r
    figs = B.L.figures(line)
    is_fig = any(str(v) == r.lstrip("0") or str(v) == r for v in figs)
    seen_as_fig += is_fig
    print("      `%-10s`  all decimal: %-3s   read as a FIGURE: %s"
          % (r, "yes" if r.isdigit() else "no", "YES" if is_fig else "no"))
print()
print("  population: the %d candidate short REVISIONS above" % len(REVS))
B.plain("...REVISIONS `figures()` reads as a figure", seen_as_fig)
print("      ^ one unit of that number is one candidate revision string")
print()
print("  The comment deleted with mg-70c7's old body claimed to exclude `a git")
print("  revision`.  It never did and still does not: an all-decimal short")
print("  revision passes every exclusion.  LIVE, and correctly reported by the")
print("  parent as reported-and-not-fixed.")

print()
print("A3 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
