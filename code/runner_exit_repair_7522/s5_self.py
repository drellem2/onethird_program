"""S5 -- THIS DELIVERABLE, CHECKED FOR THE DEFECTS IT REPAIRS.

WHAT KIND OF ARTIFACT THIS IS.  It DEFINES POPULATIONS AND ENUMERATES OVER
THEM, and it is also a set of shell and Python scripts.  So it can exhibit all
three of the defects it repairs, and each is checked here on this tree's own
bytes rather than promised in a README:

  D1  A POPULATION DEFINED BY A NAME instead of by a property.  OPEN 1.
  D2  AN ENUMERATION ANCHORED TO A STALE REVISION.  OPEN 3.
  D3  A PIPELINE WHOSE STATUS IS DISCARDED.  The forward defect itself -- this
      tree ships a `run_all.sh`, so it is a member of its own population.

and one more, because the second half of OPEN 2 is a habit and not a figure:

  D4  A STRENGTH MARKER STANDING IN FOR A CHECK -- "confirmed exactly",
      "verified", "byte-identical" used where nothing was re-derived.

Where a branch honestly cannot exhibit a defect, the reason is stated and it is
a STRUCTURAL reason, not a promise about how the code is called.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

HERE = os.path.dirname(os.path.abspath(__file__))
TREE = "code/runner_exit_repair_7522"
BAD = 0

MINE_PY = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
MINE_SH = sorted(f for f in os.listdir(HERE) if f.endswith(".sh"))

L.bar("S5  THE GENERAL FORM, APPLIED TO THIS TREE")

# ---------------------------------------------------------------------------
L.hdr("S5a  D3 -- IS THIS TREE'S OWN RUNNER IN ITS OWN POPULATION?")

print("  The strongest form of this check is the instrument turned on itself:")
print("  run S1's P2 predicate over this tree's own `*.sh`.  If an edit ever")
print("  puts a pipeline back into `run_all.sh`, this goes red naming the line.")
print()
for name in MINE_SH:
    rel = "%s/%s" % (TREE, name)
    src = L.read(rel, None)
    se = L.has_set_e(src)
    ps = L.pipelines(src)
    bad_lines = []
    for i, line in ps:
        if not (se and not L.guarded(line)):
            continue
        if any(L.stage_can_fail(rel, st, None)[0]
               for st in L.discarded_stages(line)):
            bad_lines.append((i, line.strip()))
    print("      %-34s set -e: %-4s pipelines: %d   in P2: %d"
          % (name, "yes" if se else "no", len(ps), len(bad_lines)))
    for i, line in bad_lines:
        print("          *** %4d  %s" % (i, line[:70]))
    BAD += len(bad_lines)
print()
print("  And the idiom is present rather than merely the pipeline absent --")
print("  a runner with no steps at all would also score 0 above:")
guards = len(re.findall(r">\s*out_\w+\.txt\s*\|\|\s*\{",
                        L.read("%s/run_all.sh" % TREE, None)))
steps = len(re.findall(r"^python3 ", L.read("%s/run_all.sh" % TREE, None),
                       re.M))
print("      steps in run_all.sh                    %d" % steps)
print("      ...that redirect and guard their status %d" % guards)
if steps == 0 or guards != steps:
    BAD += 1
    print("      *** not every step reads its own status ***")

# ---------------------------------------------------------------------------
L.hdr("S5b  D1 -- IS ANY POPULATION HERE DEFINED BY A NAME?")

print("  Every mention of a runner FILENAME in this tree's Python, with what")
print("  it is doing there.  The rule this tree must satisfy: a filename may")
print("  appear as the SWEEP'S rule being measured, or as a specific file")
print("  being repaired, and never as this tree's own population filter.")
print()
NAMEY = re.compile(r"run_all\.sh|run_audit\.sh")
rows = []
for name in MINE_PY:
    src = L.read("%s/%s" % (TREE, name), None)
    for i, line in enumerate(src.splitlines(), 1):
        if NAMEY.search(line):
            rows.append((name, i, line.strip()))
print("      mentions: %d" % len(rows))
print()
# A filename used as a POPULATION FILTER looks like a comparison or a
# membership test on a path.  Quoted prose, a repaired file's own path, and a
# row that is explicitly labelled the sweep's rule are not that.
FILTERS = []
for name, i, line in rows:
    if line.lstrip().startswith("#"):
        continue
    if 'print(' in line or line.lstrip().startswith('"') or "'''" in line:
        continue
    if re.search(r"basename\([^)]*\)\s*[=!]=\s*[\"']run_all\.sh[\"']", line):
        FILTERS.append((name, i, line))
    elif re.search(r"endswith\(\s*[\"']/?run_all\.sh[\"']", line):
        FILTERS.append((name, i, line))
print("      lines that FILTER a population by that name: %d" % len(FILTERS))
for name, i, line in FILTERS:
    print("          %s:%d  %s" % (name, i, line[:72]))
print()
print("  Each of those is checked by hand, because `is this filter the sweep's")
print("  rule under measurement or is it mine` is not a syntactic question:")
print()
ALLOWED = {
    ("s1_population.py", "the sweep's NAME rule, being counted next to the "
                         "property rule -- S1a prints both"),
    ("s3_figure.py", "the `run_all.sh` sub-population of the census whose "
                     "figures S3b/S3c are re-deriving, which is the sweep's "
                     "own population by construction"),
}
table = []
for name, i, line in FILTERS:
    why = [w for n, w in ALLOWED if n == name]
    if why:
        table.append(("%s:%d" % (name, i), "ALLOWED", why[0]))
    else:
        BAD += 1
        table.append(("%s:%d" % (name, i), "UNACCOUNTED", "*** no disposition"
                      " for this filter -- it may be this tree's own ***"))
L.rows(table, (24, 12))
print()
print("  `lib7522.ls_sh()` -- the only file-listing primitive in this tree --")
print("  takes NO name argument at all, so a name filter cannot be applied")
print("  inside it.  That is the STRUCTURAL half: the population primitive")
print("  cannot exhibit D1, and the reason is its signature and not a promise.")
sigs = re.findall(r"def ls_sh\(([^)]*)\)", L.read("%s/lib7522.py" % TREE, None))
print("      def ls_sh(%s)" % (sigs[0] if sigs else "?"))
if not sigs or "name" in sigs[0]:
    BAD += 1
    print("      *** ls_sh has grown a name parameter ***")

# ---------------------------------------------------------------------------
L.hdr("S5c  D2 -- WHAT IS EVERY ENUMERATION HERE ANCHORED TO?")

print("  Every line in this tree that pins an anchor, and which kind of")
print("  question it serves.  A CENSUS pinned to a revision is the defect;")
print("  a COMPARISON not pinned is mg-821e's.")
print()
PINS = []
for name in MINE_PY:
    src = L.read("%s/%s" % (TREE, name), None)
    for i, line in enumerate(src.splitlines(), 1):
        if re.search(r"\bL?\.?PINNED\b", line) and not line.lstrip().startswith("#"):
            PINS.append((name, i, line.strip()))
KIND = {
    ("lib7522.py",): ("definition", "the constant itself, plus the docstring "
                      "that states the rule"),
    ("s1_population.py",): ("COMPARISON", "S1a prints the census at the pin "
                            "AND at HEAD, side by side -- the pinned side is "
                            "one half of a comparison"),
    ("s2_status.py",): ("COMPARISON", "the PRE-repair runner text, which must "
                        "come from a fixed revision or there is no `pre`"),
    ("s3_figure.py",): ("COMPARISON", "the figures are re-derived at the "
                        "revision the sweep quoted them at"),
    ("s4_unpin.py",): ("COMPARISON", "the pinned cells of the 2x2 and the "
                       "byte-comparison, both of which are comparisons"),
    ("s5_self.py",): ("PATTERN", "the one hit is this scanner's own regex "
                      "literal; the file itself reads only the current world"),
    ("selftest7522.py",): ("COMPARISON", "the pinned side of the rules' "
                           "both-senses fixtures"),
    ("sitecustomize_mg7522.py",): ("none", "an injected hook; it reads no "
                                   "revision at all"),
}
table = []
for name in MINE_PY:
    hits = [p for p in PINS if p[0] == name]
    kind, why = next((v for k, v in KIND.items() if name in k),
                     ("UNCLASSIFIED", "*** no disposition for this file's "
                      "anchors ***"))
    table.append((name, "%d pin(s)" % len(hits), kind, why))
    if kind == "UNCLASSIFIED" and hits:
        BAD += 1
L.rows(table, (24, 9, 11))
print()
print("  THE CENSUS SIDE, checked structurally: every population primitive in")
print("  `lib7522.py` defaults to the current world, so a census that forgets")
print("  to think about its anchor gets the RIGHT one by default and a")
print("  comparison has to ask for the pin explicitly.  That is the direction")
print("  the defaults should point and it is checked here, not asserted:")
for fn in ("ls_sh", "read", "sources", "callers", "_sources_at"):
    m = re.search(r"def %s\(([^)]*)\)" % fn, L.read("%s/lib7522.py" % TREE, None))
    sig = m.group(1) if m else "?"
    ok = "ref=None" in sig or "ref" not in sig
    print("      %-14s(%-28s) default is the current world: %s"
          % (fn, sig[:28], "yes" if ok else "*** NO ***"))
    if not ok:
        BAD += 1

# ---------------------------------------------------------------------------
L.hdr("S5d  D4 -- DOES THIS TREE USE A STRENGTH MARKER INSTEAD OF A CHECK?")

print("  A marker written INSIDE quotes, backticks or emphasis is a MENTION --")
print("  the arc's way of naming a form of words it is discussing.  Written")
print("  BARE, applied to a figure, it is a USE.  That distinction is the same")
print("  one as `a comment quoting | tee is not a pipeline`, one level up, and")
print("  the first draft of this check did not make it: it counted its own")
print("  detecting regex as a violation, which is the arc's recurring defect")
print("  in the instrument built to find it.  Recorded in OUTCOMES.md.")
print()
uses, mentions = [], 0
for name in MINE_PY + MINE_SH:
    for i, line, kind in L.strength_lines(L.read("%s/%s" % (TREE, name), None)):
        if kind == "USE":
            uses.append((name, i, line))
        else:
            mentions += 1
print("      MENTIONs in this tree                      %3d" % mentions)
print("      USEs in this tree                          %3d" % len(uses))
for name, i, line in uses:
    print("          *** %s:%d  %s" % (name, i, line[:64]))
if uses:
    BAD += len(uses)
    print("  *** each of those is a place a reader will not check ***")
else:
    print()
    print("  Every figure this tree prints is printed next to the predicate")
    print("  that produced it, in the same run -- which is the thing a")
    print("  strength marker is usually standing in for.")

# ---------------------------------------------------------------------------
L.hdr("S5e  THE PIPELINE DEFECT CANNOT ARISE IN THE PYTHON -- structurally")

sh_true = []
for name in MINE_PY:
    for lineno, what in L.shell_true_sites("%s/%s" % (TREE, name), None):
        sh_true.append((name, lineno, what))
print("  Walked as an AST, not grepped.  A grep for `shell=True` matches the")
print("  sentence that says `shell=True` is never used -- mg-05eb recorded")
print("  exactly that defect in its own self-test, and the first draft of this")
print("  check reproduced it on four of this tree's own files.")
print()
print("      REAL `shell=True` / `os.system(` CALL sites in this tree: %d"
      % len(sh_true))
for name, lineno, what in sh_true:
    print("          *** %s:%s  %s" % (name, lineno, what))
if sh_true:
    BAD += len(sh_true)
else:
    print("      Every subprocess takes a LIST argv, so no shell parses the")
    print("      command, so there is no pipeline, so `returncode` is the")
    print("      target's own status.  STRUCTURAL: it follows from the call")
    print("      shape, not from a promise about how these are invoked.")
print()
print("      And `returncode` is read on every path: `lib7522.run_argv`")
print("      returns None on timeout, which prints `-` and never 0.")
tmo = "return None, ((ex.stdout" in L.read("%s/lib7522.py" % TREE, None)
print("      timeout path returns None rather than 0:  %s"
      % ("yes" if tmo else "*** NO ***"))
if not tmo:
    BAD += 1

# ---------------------------------------------------------------------------
L.hdr("S5f  BRANCHES THAT HONESTLY CANNOT EXHIBIT THESE DEFECTS, WITH REASONS")

print("   1. D1 in `ls_sh()` -- the signature has no name parameter, so no")
print("      name filter can be applied inside the primitive.  Checked in S5b.")
print("   2. D2 in `s5_self.py` -- this file reads only the current world; it")
print("      asks what THIS TREE says right now, and a pinned answer to that")
print("      question would be about a tree that no longer exists.  0 pins.")
print("   3. D3 in the Python -- list argv, no shell, no pipeline.  S5e.")
print("   4. D3 in `selftest7522.py`'s fixtures -- they are STRINGS parsed by")
print("      the rules, never executed, so no status exists to discard.")
print("   5. D4 in the figures -- every one is recomputed in the run that")
print("      prints it, so there is nothing for a strength marker to stand in")
print("      for.  S5d checks that no marker is USED as well; MENTIONs are")
print("      counted and allowed, because this tree's whole subject is those")
print("      words and a rule that banned naming them would ban the finding.")
print()
print("  WHAT IS NOT CHECKED HERE, stated rather than omitted:")
print("   * That the PROSE in README.md / OUTCOMES.md agrees with these")
print("     transcripts.  A probe cannot check a sentence it does not know")
print("     about; S3e does that job for mg-c2b3's artifacts and the same")
print("     job for this tree's is done by a reader with both files open.")
print("   * That the property predicate is the RIGHT one.  It is stated in")
print("     full in `lib7522.pipelines` / `discarded_stages` / `guarded` so")
print("     that disagreeing with it is possible; a predicate nobody can")
print("     disagree with is not a definition.")

print()
L.bar("S5 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts, over this tree's %d `*.py` and %d"
      % (len(MINE_PY), len(MINE_SH)))
print("`*.sh` files only: a pipeline of this tree's own in P2, a step that")
print("does not read its status, an unaccounted name filter, a mis-defaulted")
print("population primitive, an unclassified anchor, a strength marker, and")
print("`shell=True`.  It does not range over the rest of the repository --")
print("S1 through S4 do that, and this is the section about the instrument.")
sys.exit(1 if BAD else 0)
