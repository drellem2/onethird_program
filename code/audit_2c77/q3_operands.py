"""q3_operands.py -- COUNT THEM MYSELF, AND ASK WHETHER THE EMPTY COLUMN CAN
EVER BE ANYTHING ELSE.

mg-69d1 says ALL 17 ARE CLASSIFIED and prints a four-column table with
`not determined` reading 0.  Two questions, and neither is answered by reading
the table.

  (a) SEVENTEEN OF WHAT?  `kern5f9a.boolean_operands` walks only inside
      `deciding_conditions`, and `deciding_conditions` admits exactly two
      forms: an `ast.If` with an `ast.Return` somewhere inside it, and an
      `ast.Return` with a value.  An `and` in a `while`, in an assignment, in
      an `assert`, or in an `if` whose body only assigns or only raises, is an
      explicit boolean operator and is in NONE of the four columns.

      mg-eaef wrote the qualifier every time: `15 explicit boolean operand(s)
      IN DECIDING CONDITIONS`.  This script counts both populations with a
      walker written in `lib2c77`, checked against the shipped one span for
      span in the self-test, and then enumerates where the repair states the
      census WITHOUT the qualifier.

  (b) CAN `not determined` EVER READ ANYTHING BUT 0?  The repair's stated
      reason for printing it is that `an explicit not determined is
      CHECKABLE`.  A cell whose value is fixed by the control flow rather than
      by the input is not checkable, whatever it is printed at.  Three ways of
      asking, in increasing strength: the branch structure, a population of
      real files far larger than the census's two, and the deletion test the
      repair itself uses on the column NEXT to it.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import ast
import importlib.util
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "face_geometry_instr_5f9a"))

import lib2c77 as L                                              # noqa: E402
import kern5f9a as K                                             # noqa: E402

R = L.Report(
    selfpop="every source read and AST parse this script performs, the "
            "requirement that the two census files parse and that neither "
            "operand walk come back empty, and the requirement that each "
            "column deletion really remove the branch it names",
    findpop="every operand of every `and`/`or` anywhere in face_complex.py "
            "and posets.py scored against the four columns of mg-69d1's "
            "table; every site in the tree that states the census over "
            "`explicit boolean operands`, scored for the deciding-condition "
            "qualifier; and the `not determined` column asked three ways "
            "whether any input can reach it")

L.banner("Q3", "ALL THE OPERANDS, COUNTED HERE, AND THE COLUMN THAT READS 0")

CENSUS = [(L.FACE_REL, "face_complex.py"), (L.POSETS_REL, "posets.py")]
SOURCES = {name: L.read_worktree(rel) for rel, name in CENSUS}

# ---------------------------------------------------------------------------
L.rule("(i) TWO POPULATIONS, WALKED HERE")
print("""   `all` walks the WHOLE module for `ast.BoolOp` and takes every
   value of every one -- no filter of any kind.  `deciding` restricts
   that to what lies inside a deciding condition, which is what
   `kern5f9a.boolean_operands` computes.  The self-test requires the
   second to agree with the shipped walker SPAN FOR SPAN before this
   table is read, so the difference below is a subtraction and not my
   bug.""")
print()
print("   %-18s %-34s %-34s %s"
      % ("file", "operands of every and/or, anywhere",
         "of those, in a deciding condition", "difference"))
TOTALS = {"all": 0, "deciding": 0}
PER_FILE = {}
for rel, name in CENSUS:
    src = SOURCES[name]
    allo = L.all_boolean_operands(src, name)
    dec = L.deciding_boolean_operands(src, name)
    PER_FILE[name] = (allo, dec)
    TOTALS["all"] += len(allo)
    TOTALS["deciding"] += len(dec)
    print("   %-18s %-34d %-34d %d"
          % (name, len(allo), len(dec), len(allo) - len(dec)))
    R.check(len(allo) > 0, "%s: the unfiltered walk found 0 operands; every "
            "subtraction below would be vacuous" % name)
print("   %-18s %-34d %-34d %d"
      % ("ALL", TOTALS["all"], TOTALS["deciding"],
         TOTALS["all"] - TOTALS["deciding"]))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE FOUR COLUMNS, FED FROM OUTSIDE, AND WHAT FALLS OUTSIDE THEM")
print("""   The SHIPPED classifier is called here -- `kern5f9a.operand_columns`
   with `d2_deletion.SWEEP_FILES`, exactly as `d2` calls it.  Its four
   columns are then subtracted from the unfiltered walk.  An operand in
   the difference is in no column of mg-69d1's table, which is the
   state mg-eaef's E4 was a finding about, one rung out.""")
print()
cols = K.operand_columns(SOURCES, L.SWEEP_FILES)
placed = set()
for cname in K.OPERAND_COLUMNS:
    for op in cols[cname]:
        placed.add((op.file, L.pos(op.node.values[op.index])))
print("   %-18s %-7s %-17s %-19s %-16s %s"
      % ("file", "swept", "not swept: file", "not swept: nested",
         "not determined", "in the table"))
for rel, name in CENSUS:
    row = [len([o for o in cols[c] if o.file == name])
           for c in K.OPERAND_COLUMNS]
    print("   %-18s %-7d %-17d %-19d %-16d %d"
          % ((name,) + tuple(row) + (sum(row),)))
allrow = [len(cols[c]) for c in K.OPERAND_COLUMNS]
print("   %-18s %-7d %-17d %-19d %-16d %d"
      % (("ALL",) + tuple(allrow) + (sum(allrow),)))
print()
print("   independent walk of the same two files, unfiltered : %d"
      % TOTALS["all"])
print("   the four columns of mg-69d1's table                : %d"
      % sum(allrow))

outside = []
for rel, name in CENSUS:
    for o in PER_FILE[name][0]:
        if (name, o["pos"]) not in placed:
            outside.append(o)
print("   IN NO COLUMN AT ALL                                : %d"
      % len(outside))
print()
print("   and they are NAMED, because a count of what is uncovered that cannot")
print("   be pointed at is the same silence as no count at all:")
print()
print("     %-18s %-26s %-5s %-4s %s"
      % ("file", "function", "line", "op", "operand text"))
for o in sorted(outside, key=lambda x: (x["file"], x["line"])):
    text = (o["text"] or "").replace("\n", " ")
    print("     %-18s %-26s %-5d %-4s %s"
          % (o["file"], o["func"], o["line"], o["op"], text[:44]))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) WHERE THE CENSUS IS STATED, AND WHETHER IT CARRIES THE "
       "QUALIFIER")
print("""   The population is READ FROM THE TREE, not listed here.  Every line
   containing `explicit boolean operand` is found with `git grep` over
   the working tree, untracked files included.

   THE RULE, STATED BEFORE THE TABLE.  A site is QUALIFIED if the words
   `deciding condition` stand within 3 lines of it, in the same file.
   A site is a QUOTATION rather than an assertion of the census if
   `NO FURTHER` or `is read as` stands in the same window -- those are
   the two markers of the wide BOUND being quoted in order to correct
   it, which is a different sentence about a different thing.

   MISS #2, KEPT.  This section first CONTROLLED on `mg-eaef qualified
   the census every time`, and gated a self-error on it.  The self-error
   fired: mg-eaef's own README says `4 of the 15 explicit boolean
   operands in the file it counts`, with no qualifier either.  The
   premise was mine and it was wrong, and the instrument said so before
   the finding did.  What survives is not a claim about who wrote a
   word; it is the SUBTRACTION in (i) and (ii), which does not depend
   on any site's wording.  The table below is kept as CONTEXT and the
   finding no longer rests on it.

   THE POPULATION OF THE REPAIR'S OWN OUTPUT IS DERIVED, not listed: the
   files `d01ff32` touched, read out of `git show --name-only`.  This
   audit's own files are in the table too, and marked -- excluding them
   by path would be the path list this lineage keeps rebuilding.""")
print()


def window(path, lineno, span=3):
    try:
        lines = L.read_worktree(path).splitlines()
    except (IOError, OSError):
        return ""
    i = int(lineno) - 1
    return "\n".join(lines[max(0, i - span):i + span + 1])


def grep(needle):
    import subprocess
    p = subprocess.run(["git", "-C", L.REPO, "grep", "-n", "-F", "--untracked",
                        needle], capture_output=True, text=True)
    if p.returncode not in (0, 1):
        raise RuntimeError(p.stderr.strip())
    out = []
    for line in p.stdout.splitlines():
        if not line.strip():
            continue
        path, _, tail = line.partition(":")
        out.append((path, tail.split(":", 1)[0]))
    return out


touched = set(L.git("show", "--name-only", "--format=", "d01ff32").split())
sites = grep("explicit boolean operand")
print("   %-56s %-5s %-8s %s" % ("site", "line", "in d01ff32", "disposition"))
unqualified, repair_unqualified = [], []
seen_disp = set()
for path, lineno in sites:
    w = window(path, lineno)
    quoted = ("NO FURTHER" in w) or ("is read as" in w)
    qualified = "deciding condition" in w
    mine = path.startswith("code/audit_2c77/")
    if quoted:
        disp = "quotes the wide BOUND, not the census"
    elif qualified:
        disp = "census, QUALIFIED"
    else:
        disp = "*** census, UNQUALIFIED"
        unqualified.append((path, lineno))
        if path in touched:
            repair_unqualified.append((path, lineno))
    seen_disp.add(disp)
    print("   %-56s %-5s %-8s %s"
          % (path, lineno, "yes" if path in touched else
             ("THIS AUDIT" if mine else "no"), disp))
print()
print("   %d site(s) in all; %d state the census without the "
      "deciding-condition\n   qualifier; %d of those are in files d01ff32 "
      "touched." % (len(sites), len(unqualified), len(repair_unqualified)))
print("   NON-VACUITY -- the rule returned %d distinct dispositions over the "
      "population,\n   so it is not labelling every site the same way: %s"
      % (len(seen_disp), "; ".join(sorted(seen_disp))))
print()
R.check(len(seen_disp) >= 2,
        "the disposition rule returned one label for every site; it is not "
        "distinguishing and the table above says nothing")
R.gate(not (TOTALS["all"] > sum(allrow) and repair_unqualified),
       "THE CENSUS IS STATED OVER A POPULATION WIDER THAN THE ONE IT "
       "CLASSIFIES.  `explicit boolean operand` denotes %d operands in "
       "face_complex.py and posets.py; mg-69d1's table classifies %d and %d "
       "are in NO column of it -- 20 in face_complex.py and 2 in posets.py, "
       "named in (ii) above.  `boolean_operands` walks only inside "
       "`deciding_conditions`, and an `and` in a `while`, in an assignment, "
       "or in an `if` whose body does not return is outside every column.  "
       "The claim is written without the deciding-condition qualifier at %d "
       "site(s) in files d01ff32 touched: %s.  This is mg-eaef's E4 state -- "
       "operands in neither column -- one rung out, in the artifact that "
       "repairs E4, and the narrowed BOUND sentence itself is NOT affected: "
       "it names `the deciding conditions` and is correct"
       % (TOTALS["all"], sum(allrow), len(outside),
          len(repair_unqualified),
          ", ".join("%s:%s" % s for s in repair_unqualified)))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) `not determined` -- CAN ANY INPUT REACH IT?")
print("""   The repair's reason for printing the column at 0 is that `an
   explicit not determined is CHECKABLE, and an empty cell is the
   absence of an answer`.  That reason is the thing under test.  Asked
   three ways.""")
print()

print("   (iv-a) THE BRANCH STRUCTURE.  `operand_columns`' chain is parsed out")
print("   of kern5f9a.py and its guards printed:")
print()
k5_src = L.read_worktree(L.KERN5F9A_REL)
fn = None
for node in ast.walk(ast.parse(k5_src)):
    if isinstance(node, ast.FunctionDef) and node.name == "operand_columns":
        fn = node
if fn is None:
    R.selferr("operand_columns could not be found in kern5f9a.py; (iv-a) is "
              "DROPPED rather than counted as passing")
    guards = []
else:
    chain, node = [], None
    for st in ast.walk(fn):
        if isinstance(st, ast.If):
            chain.append(st)
    # the outermost If of the classification chain is the one whose orelse
    # chains to another If
    head = None
    for st in chain:
        if st.orelse and isinstance(st.orelse[0], ast.If):
            if head is None or st.lineno < head.lineno:
                head = st
    guards = []
    cur = head
    while cur is not None:
        guards.append(ast.unparse(cur.test))
        nxt = cur.orelse[0] if (cur.orelse
                                and isinstance(cur.orelse[0], ast.If)) else None
        if nxt is None and cur.orelse:
            guards.append("else  ->  %s" % ast.unparse(cur.orelse[0]).strip())
        cur = nxt
    for g in guards:
        print("     %s" % g)
print()
last_two = [g for g in guards if g in ("not op.top", "op.top")]
has_else = any(g.startswith("else ") for g in guards)
print("   `op.top` is `node is cond` -- a bool.  `not op.top` and `op.top` are")
print("   exhaustive over a bool, so the `else` after them is unreachable for")
print("   every possible input, not merely for this tree.")
print("   the two exhaustive guards are present : %s"
      % ("yes: %s" % ", ".join(last_two) if len(last_two) == 2 else "NO"))
print("   an `else` stands after them           : %s"
      % ("yes" % () if has_else else "no"))
print("   kern5f9a marks it                     : %s"
      % ("# pragma: no cover" if "# pragma: no cover" in k5_src else "not "
         "marked"))
print()

print("   (iv-b) A POPULATION LARGER THAN THE CENSUS'S TWO.  The shipped")
print("   classifier is run over EVERY python file in the repository that")
print("   parses -- each as though it were the swept file, so `not swept:")
print("   file` cannot absorb anything -- and `not determined` is read off:")
print()
pyfiles = []
for root, dirs, files in os.walk(os.path.join(L.REPO, "code")):
    dirs[:] = [d for d in dirs if not d.startswith(".")]
    for f in sorted(files):
        if f.endswith(".py"):
            pyfiles.append(os.path.join(root, f))
scanned, unparsable, nd_total, op_total = 0, 0, 0, 0
for path in sorted(pyfiles):
    rel = os.path.relpath(path, L.REPO)
    try:
        with open(path) as fh:
            src = fh.read()
        ast.parse(src)
    except (SyntaxError, UnicodeDecodeError, IOError, OSError):
        unparsable += 1
        continue
    name = os.path.basename(path)
    c = K.operand_columns({name: src}, (name,))
    scanned += 1
    nd_total += len(c["not determined"])
    op_total += sum(len(v) for v in c.values())
print("     python files under code/ : %d" % len(pyfiles))
print("     parsed and classified    : %d   (unparsable, skipped: %d)"
      % (scanned, unparsable))
print("     operands classified      : %d" % op_total)
print("     landing in `not determined` : %d" % nd_total)
R.check(op_total > 0, "the repository-wide scan classified 0 operands; "
        "(iv-b) says nothing")
print()

print("   (iv-c) THE DELETION TEST, PERFORMED TWO WAYS.")
print("   p1 (v) prints `with not swept: nested DELETED FROM THE CLASSIFIER`")
print("   and reports the totality claim GOES RED.  What it does is")
print("   `{c: v for c, v in cols.items() if c != 'not swept: nested'}` -- it")
print("   drops a key from the RESULT dict and re-sums.  The classifier is")
print("   never re-run.  Both operations are done here, on both columns, and")
print("   the difference between them is the measurement:")
print()


def classify_with(source, tag):
    """Import a mutated kern5f9a from a temp dir and run its classifier."""
    tmp = tempfile.mkdtemp(prefix="mg2c77-k5-")
    try:
        p = os.path.join(tmp, "k5_%s.py" % tag)
        with open(p, "w") as fh:
            fh.write(source)
        spec = importlib.util.spec_from_file_location("k5_%s" % tag, p)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        c = mod.operand_columns(SOURCES, L.SWEEP_FILES)
        return len(c), sum(len(v) for v in c.values())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


ND_BRANCH = ("            else:                                   "
             "# pragma: no cover\n"
             "                cols[\"not determined\"].append(op)\n")
NESTED_BRANCH = ("            elif not op.top:\n"
                 "                cols[\"not swept: nested\"].append(op)\n")
TOTAL = K.operand_columns_total(SOURCES)
BRANCHES = {"not determined": ND_BRANCH, "not swept: nested": NESTED_BRANCH}
print("     %-20s %-32s %-7s %-18s %s"
      % ("column", "how it is deleted", "sum", "independent walk", "verdict"))
print("     %-20s %-32s %-7d %-18d %s"
      % ("-- none --", "as shipped", sum(allrow), TOTAL,
         "GREEN" if sum(allrow) == TOTAL else "RED"))
RESULT = {}
for colname in ("not swept: nested", "not determined"):
    # (1) p1's operation: drop the key from the RESULT dict and re-sum.
    short = {c: v for c, v in cols.items() if c != colname}
    ssum = sum(len(v) for v in short.values())
    RESULT[(colname, "dict")] = (ssum == TOTAL)
    print("     %-20s %-32s %-7d %-18d %s"
          % (colname, "p1's: drop the result key", ssum, TOTAL,
             "GREEN" if ssum == TOTAL else "RED"))
    # (2) the operation p1's own sentence names: delete the branch from
    #     `operand_columns` and re-run the classifier.
    branch = BRANCHES[colname]
    n = k5_src.count(branch)
    if n != 1:
        R.selferr("the `%s` branch was found %d times in kern5f9a.py by exact "
                  "match and not once; that deletion is DROPPED rather than "
                  "counted as passing" % (colname, n))
        continue
    try:
        ncols, nsum = classify_with(k5_src.replace(branch, "", 1),
                                    colname.split(":")[-1].strip())
    except Exception as e:                                # noqa: BLE001
        R.selferr("deleting the `%s` branch produced a module that would not "
                  "run (%s); that deletion is DROPPED" % (colname, e))
        continue
    RESULT[(colname, "source")] = (nsum == TOTAL)
    print("     %-20s %-32s %-7d %-18d %s"
          % (colname, "the branch, out of the source", nsum, TOTAL,
             "GREEN" if nsum == TOTAL else "RED"))
print()
print("   READ THE `not swept: nested` PAIR.  Dropping the key subtracts 4 and")
print("   the sum misses.  Deleting the BRANCH leaves the sum at %d, because" %
      TOTAL)
print("   the 4 nested operands fall through to `not determined`, which is the")
print("   fall-through the docstring says it is.  So the column IS load-bearing")
print("   -- against an edit to the classifier, which no sentence in the repair")
print("   claims -- and it is still unreachable by any INPUT.")
print()
nested_dict_red = RESULT.get(("not swept: nested", "dict")) is False
nested_src_green = RESULT.get(("not swept: nested", "source")) is True
R.gate(not (nested_dict_red and nested_src_green),
       "`deleting the not swept: nested column makes the totality claim go "
       "red` is true of the operation p1 PERFORMS and false of the operation "
       "p1 NAMES.  p1 (v) prints `with not swept: nested deleted from the "
       "classifier` and drops a key from the result dict; delete the branch "
       "from `operand_columns` itself and the totality claim stays GREEN at "
       "%d of %d, because the 4 nested operands fall through into `not "
       "determined`.  The row's numbers are right for what the row does; the "
       "sentence beside it names something else -- which is the shape of the "
       "defect this repair was written to fix" % (TOTAL, TOTAL))
R.gate(not (nd_total == 0 and len(last_two) == 2),
       "`not determined` cannot be reached by any INPUT: its two preceding "
       "guards, `not op.top` and `op.top`, are exhaustive over a bool, "
       "kern5f9a marks the branch `# pragma: no cover`, and %d operand(s) "
       "landed there across %d python files under code/ carrying %d operands "
       "-- a population 36x the census's two files.  The stated reason for "
       "printing it is that `an explicit not determined is CHECKABLE` and "
       "that `nothing lands there ON THIS TREE`; both read as claims about "
       "the tree, and the 0 is a property of the control flow that no tree "
       "can move.  What CAN move it is an edit to the classifier, as the "
       "row above shows -- and that is not what either sentence says"
       % (nd_total, scanned, op_total))
print()

L.finish(R)
