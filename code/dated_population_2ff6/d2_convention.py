"""mg-2ff6 / D2 -- THE SCORE, BY cfd9c's OWN CHECKER, RUN AND NOT COPIED.

THE TICKET'S TRAP, IN FULL: *cfd9c respecified S4c's checker after it failed on
its own tree, moving its score from 1-of-2 to 5-of-5.  The structural reason is
plausible and cfd9c flagged it.  If you find S4c failing on mg-03d1 or mg-9160,
DO NOT respecify it -- that is the second time the same checker would have been
reshaped by the thing it is checking.  Fix the probe or record the failure.*

So this probe contains no checker.  It RUNS `s4_convention.py` as a subprocess,
in cfd9c's own directory, at whatever revision that file is at, and reads its
answer off the output.  There is no code here that could respecify anything:
the rule is not imported, not re-typed, and not parameterised.  The only thing
I extract from cfd9c's source is the SELECTOR, and only so that `d1` can put a
`*` beside a row; the VERDICT is always the subprocess's.

  D2a  THE BEFORE, from cfd9c's own committed transcript at `5c0849a`
  D2b  THE AFTER, from a live run of the same file
  D2c  THE PER-TREE TABLE, both readings side by side
  D2d  THE FIVE I DID NOT TOUCH, and why 27 was never the right target

Exit code = 1 if the arc's dated count did not rise, else 0.  That is the one
thing this ticket can fail at that nothing else here would notice.
"""

import re
import sys

import lib2ff6 as U

BAD = 0

U.bar("mg-2ff6 / D2 -- THE SCORE, BY cfd9c's OWN CHECKER")
print("HEAD: %s" % U.head())

# ---------------------------------------------------------------------------
U.hdr("D2a  THE BEFORE, FROM cfd9c's OWN COMMITTED TRANSCRIPT")

BEFORE_PATH = "code/corpus_fixedpoint_fd9c/out_s4_convention.txt"
before_txt = U.read(BEFORE_PATH, U.PUBLISHED_AT)
before = U.s4c_scores(before_txt)
before_tree = U.s4c_per_tree(before_txt)
U.pop("the S4c block of `%s`, as committed" % BEFORE_PATH.split("/", 1)[1],
      ref=U.PUBLISHED_AT)
U.plain("...ARC-WIDE FIGURES S4c found, AS COMMITTED", before[0][0])
print("      ^ one unit of that number is one printed count row")
U.plain("...of them DATED, AS COMMITTED", before[0][1])
print("      ^ one unit of that number is one printed count row")
print()
print("  THAT TRANSCRIPT IS NOT RE-RUN BY THIS TICKET AND MUST NOT BE.  It is")
print("  the BEFORE reading of the score I am about to move; a probe of mine")
print("  that regenerated it would have erased its own control.  cfd9c's suite")
print("  is left exactly as committed.")

# ---------------------------------------------------------------------------
U.hdr("D2b  THE AFTER, FROM A LIVE RUN OF THE SAME FILE")

code, out = U.s4c()
after = U.s4c_scores(out)
after_tree = U.s4c_per_tree(out)
print("  `python3 -B s4_convention.py`, run in cfd9c's own directory, exit %d."
      % code)
print("  Its output is not edited here; the two numbers below are read off it")
print("  with one regex and nothing else decides them.")
print()
U.pop("the S4c block of a live run of `s4_convention.py`")
if len(after) < 1:
    print("      *** S4c PRINTED NO SCORE.  Its output follows verbatim.")
    for ln in out.splitlines()[-40:]:
        print("      |%s" % ln)
    BAD += 1
    after = [(0, 0)]
    after_tree = {}
U.plain("...ARC-WIDE FIGURES S4c found in the arc", after[0][0])
print("      ^ one unit of that number is one printed count row")
U.plain("...of them carrying a DATED population line", after[0][1])
print("      ^ one unit of that number is one printed count row")
print()
print("  AND cfd9c's OWN TREE, which the same run scores in the same way:")
print()
if len(after) > 1:
    U.pop("the S4c block for cfd9c's own transcripts, live")
    U.plain("...ARC-WIDE FIGURES in cfd9c's own tree", after[1][0])
    print("      ^ one unit of that number is one printed count row")
    U.plain("...of them DATED, in cfd9c's own tree", after[1][1])
    print("      ^ one unit of that number is one printed count row")

rose = after[0][1] > before[0][1]
BAD += not rose
print()
print("      the arc's DATED count rose across this ticket             %s"
      % ("yes" if rose else "*** NO"))

# ---------------------------------------------------------------------------
U.hdr("D2c  THE PER-TREE TABLE, BOTH READINGS")

print("  S4c prints its own per-tree split.  Both readings are its own; the")
print("  only arithmetic here is the subtraction in the last column.")
print()
U.pop("every TREE S4c names in either reading")
print("      %-40s %13s %13s" % ("tree", "at " + U.PUBLISHED_AT, "now"))
for k in sorted(set(before_tree) | set(after_tree)):
    b = before_tree.get(k, (0, 0))
    a = after_tree.get(k, (0, 0))
    print("      %-40s %6d/%-6d %6d/%-6d   %s"
          % (k, b[1], b[0], a[1], a[0],
             "+%d dated" % (a[1] - b[1]) if a[1] != b[1] else ""))
print("      ^ each cell is DATED/FOUND, one unit of each is one count row")
print()
print("  AND THE TOTAL ROSE ON BOTH SIDES, WHICH IS MY OWN E3 ARRIVING IN MY")
print("  OWN NUMBER.  This tree's transcripts are `code/*/out_*.txt` too, so")
print("  the moment they exist S4c finds arc-wide figures in THEM -- all of")
print("  them dated, because every population line here is printed by a")
print("  function that has no form omitting the ref.  So `27` is not the")
print("  denominator any more.  Both readings, and the reader should have")
print("  both:")
print()
mine_tree = U.TREE.split("/")[1]
mine = after_tree.get(mine_tree, (0, 0))
old_found = sum(a for k, (a, _b) in after_tree.items() if k != mine_tree)
old_dated = sum(b for k, (_a, b) in after_tree.items() if k != mine_tree)
U.pop("the same rule, with this ticket's own tree taken out of the corpus")
U.plain("...ARC-WIDE FIGURES in the arc EXCLUDING this tree", old_found)
print("      ^ one unit of that number is one printed count row")
U.plain("...of them DATED, EXCLUDING this tree", old_dated)
print("      ^ one unit of that number is one printed count row")
U.plain("...ARC-WIDE FIGURES this ticket's own tree ADDED", mine[0])
print("      ^ one unit of that number is one printed count row")
U.plain("...of those, DATED", mine[1])
print("      ^ one unit of that number is one printed count row")

# ---------------------------------------------------------------------------
U.hdr("D2d  THE FIVE I DID NOT TOUCH, AND WHY 27 WAS NEVER THE TARGET")

print("  S4c says so in its own text, and it is worth quoting because my")
print("  ticket's title does not:")
print()
src = U.read("code/corpus_fixedpoint_fd9c/s4_convention.py")
m = re.search(r'print\("  AND IT OVER-COLLECTS.*?print\(\)', src, re.S)
if m:
    for ln in re.findall(r'print\("(.*?)"\)', m.group(0)):
        if ln:
            print("      %s" % ln.replace('\\"', '"'))
print()
print("  So `27` is an UPPER BOUND on arc-wide figures, and the five outside")
print("  the two trees this ticket is scoped to are, by their own labels:")
print()
U.pop("the count ROWS S4c flags outside `grain_axis_audit_03d1` and "
      "`grain_arity_9160`")
rx = U.corpus_label_rx()
outside = []
for p in U.B.all_transcripts():
    tree = p.split("/")[1]
    if tree in ("grain_axis_audit_03d1", "grain_arity_9160",
                "corpus_fixedpoint_fd9c", U.TREE.split("/")[1]):
        continue
    try:
        txt = U.read(p)
    except OSError:
        continue
    for i, label, nums in U.A.count_rows(txt):
        if rx.search(label):
            outside.append((p, label, nums))
for p, label, nums in outside:
    print("      %-44.44s %-34.34s %s"
          % (p.split("/", 1)[1], label, U.fmt_nums(nums)))
U.plain("...FLAGGED ROWS outside the two trees in scope", len(outside))
print("      ^ one unit of that number is one printed count row")
print()
print("  READ THE LABELS.  `transcripts in the corpus` is a THIRTEEN-file")
print("  per-tree census; `CONTROL invented ids found in the corpus` is a")
print("  control that is meant to read 0; `count ROWS in them` in")
print("  `out_p5_self.txt` is a tree counting its OWN rows.  Not one of them")
print("  is a figure about the arc-wide corpus.  They are flagged because")
print("  S4c's selector is a rule about the LABEL, which is the safe")
print("  direction and which S4c says it is.")
print()
U.note("D2", "THE ARC'S DATED COUNT MOVED %d -> %d OF %d BY cfd9c's OWN "
       "CHECKER, RUN AND NOT RESPECIFIED.  The residue is %d rows in four "
       "trees this ticket is not scoped to, and every one of them is a "
       "PER-TREE census or a control that S4c's label rule over-collects -- "
       "so the honest arc-wide total is %d and not %d, and finishing at "
       "%d of %d would have meant editing four more trees to make a checker "
       "print a rounder number."
       % (before[0][1], after[0][1], after[0][0], len(outside),
          after[0][0] - len(outside), after[0][0], after[0][0], after[0][0]))

print()
print("D2 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
