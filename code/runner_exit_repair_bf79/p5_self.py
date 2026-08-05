"""P5 -- THIS DELIVERABLE, CHECKED FOR THE DEFECTS IT REPAIRS.

The four openings and the floor item, each turned back on this tree:

  S1  A LABEL THAT NAMES A DIFFERENT GRAIN FROM ITS VALUE.  O1.  Every count
      this tree prints must carry a grain word ON ITS OWN LABEL -- stage
      `label`, not `prev`, not `header` -- because the audit waiting on this
      repair (`mg-03d1`) is instructed to report, for every printed count, the
      label, the grain of the value, and whether they agree.  A count of mine
      whose grain lives in a column header would be O1's defect class found in
      the repair of O1.
  S2  A POPULATION DEFINED BY A PATH.  O2.  My own populations are properties,
      and every place a name appears is dispositioned.
  S3  A RULE KEPT IN TWO COPIES.  O3/O4/F.  `libbf79.py` defines no rule that
      already exists in the arc; every predicate is imported from the tree that
      owns it.
  S4  AN AUDIT'S EVIDENCE, MODIFIED.  mg-56dc's tree is READ and not WRITTEN.

A branch that honestly cannot exhibit a defect says so with a STRUCTURAL
reason, not a promise about how the code is called.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
HERE = os.path.dirname(os.path.abspath(__file__))
MINE_PY = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
MINE_SH = sorted(f for f in os.listdir(HERE) if f.endswith(".sh"))
MY_OUTS = B.M.outs(B.TREE)

B.bar("P5  THE SAME FOUR QUESTIONS, ASKED OF THIS TREE")

# ---------------------------------------------------------------------------
B.hdr("S1  EVERY COUNT OF MINE, WITH ITS GRAIN ON ITS OWN LABEL")

print("  The ledger this repair asks of its subject, asked of itself, with the")
print("  same instrument: `lib56dc.count_rows` for the population and")
print("  `lib56dc.grain_of` for the grain and the STAGE.  The bar is higher")
print("  here than the one `r6_self.py`'s E1 sets -- E1 accepts a grain word")
print("  anywhere in a two-line window, and this requires stage `label`.")
print()
print("  WHY HIGHER, since a self-imposed harder test is the shape mg-dee4's F3")
print("  is about in reverse: `mg-03d1` reads LABELS, so a grain word of mine")
print("  that is only reachable from a header is a count my auditor will")
print("  classify by looking two lines up -- and if it looks two lines up it is")
print("  reading a row that is not mine to control.  Putting the word on the")
print("  label is the only version of this I can guarantee.")
print()
led = []
for out in MY_OUTS:
    for row in B.grain_ledger(B.read(out, None)):
        led.append((os.path.basename(out),) + row)
stages, grains = {}, {}
for o, _i, _l, _n, g, s in led:
    stages[s] = stages.get(s, 0) + 1
    grains[g] = grains.get(g, 0) + 1
print("      TRANSCRIPTS of mine on disk                        %3d" % len(MY_OUTS))
print("      count ROWS they print                              %3d" % len(led))
for k in ("SITE", "EXECUTION", "BOTH", "NONE"):
    print("      ...ROWS of mine whose LABEL declares %-9s %3d"
          % (k, grains.get(k, 0)))
for k in ("label", "prev", "header", "-"):
    print("      ...ROWS of mine whose grain is at stage %-6s %3d"
          % (k, stages.get(k, 0)))
print()
bad_stage = [r for r in led if r[5] != "label"]
print("      count ROWS of mine NOT at stage `label`            %3d"
      % len(bad_stage))
for o, i, label, nums, g, s in bad_stage:
    print("          *** %s:%d [%s/%s]  %s = %s"
          % (o, i, g, s, label[:40], ",".join(map(str, nums))))
BAD += len(bad_stage)
if not MY_OUTS:
    print("      (no transcripts on disk yet -- first pass of run_all.sh;")
    print("       the committed run is a second consecutive one)")

# ---------------------------------------------------------------------------
B.hdr("S1b  AND THE POPULATION AND GRAIN NAMED IN THE SAME LABEL")

print("  A grain word is half of it.  `10 sites` does not say WHICH sites, and")
print("  mg-56dc/T1e is exactly that defect: one quantity published as `10")
print("  sites in 5 files / nine sites in four files / nine sites in three")
print("  files / 9 sites in - files`, with no artifact saying which reading it")
print("  is at.  So the check here is that each of my TOTAL rows names a")
print("  population as well as a grain -- a qualifier, not a bare unit.")
print()
POP_WORD = re.compile(
    r"\bof mine\b|\bmy own\b|\bin (?:both|the|this|that|its|mine)\b"
    r"|\bacross\b|\bthe (?:one|old|new|two|four|property|census|corpus)\b"
    r"|\bthis tree\b|\bthey (?:print|had)\b|\bit (?:published|had)\b"
    r"|\btested\b|\bput to\b|\breturns\b|\bthe rule\b|\bboth\b"
    r"|\bmg-\w+\b|\boutside\b|\bunder\b|\bat HEAD\b|\bfound\b|\bmoved\b"
    r"|\bstill\b|\bremain\b|\bdropped\b|\badds\b|\bexcluded\b|\bLOST\b", re.I)
naked = [r for r in led if not POP_WORD.search(r[2])]
print("      count ROWS of mine                                 %3d" % len(led))
print("      ...whose label names a POPULATION as well as a")
print("         grain                                           %3d"
      % (len(led) - len(naked)))
print("      ...NAKED -- a grain with no population             %3d" % len(naked))
for o, i, label, nums, _g, _s in naked[:14]:
    print("          *** %s:%d  %s = %s"
          % (o, i, label[:44], ",".join(map(str, nums))))
if len(naked) > 14:
    print("          ... %d more" % (len(naked) - 14))
print()
print("  THIS ROW IS NOT ADDED TO `BAD` and the reason is stated rather than")
print("  quiet: `names a population` is a rule about MEANING approximated by a")
print("  word list, and a word list is exactly the hand-list this arc keeps")
print("  finding.  It is printed as a measurement a reader can disagree with,")
print("  and the naked rows are named in full so the disagreement can be about")
print("  specific rows rather than about a total.  Counting it would let me")
print("  tune a regex until my own number was zero, which is the mg-fcb2")
print("  tautology one step removed.")

# ---------------------------------------------------------------------------
B.hdr("S2  MY OWN POPULATIONS -- properties, or paths?")

print("  Every population this tree ranges over, with how it is defined:")
print()
POPS = [
    ("P1's four artifacts", "a HAND LIST of four paths",
     "DISPOSITIONED: it is mg-56dc/T1d's finding VERBATIM -- *4 artifacts "
     "state 9* -- and the list IS the finding. Widening it would be auditing "
     "a different claim."),
    ("P1/P2's E1 population", "`lib70c7.published_by`, a PROPERTY",
     "provenance over the whole repository; no directory named"),
    ("P3's `proven` population", "`published_by` + a suffix rule",
     "the artifacts of the deliverable plus the library's own sources"),
    ("P4's duplicate census", "every module-level `def` in both libraries",
     "a PROPERTY of the source, not a list of interesting names"),
    ("P4e's figure census", "`git ls-files` + the `out_*.txt` convention",
     "the whole repository; the name pattern is this arc's transcript "
     "convention, the same disposition `r6_self.py` gives `outs()`"),
    ("S1's population", "`lib70c7.outs(TREE)`, my own transcripts",
     "a PATH, and it is the right one: the question is which counts I PRINT"),
]
for name, how, why in POPS:
    print("      %-28s %s" % (name, how))
    print("          %s" % why)
print()
print("      POPULATIONS of mine, in total                      %3d" % len(POPS))
print("      ...defined by a PROPERTY                           %3d" % 4)
print("      ...defined by a PATH or a LIST, dispositioned      %3d" % 2)
print()
print("  AND S1'S POPULATION BEING A PATH IS NOT THE DEFECT O2 NAMES, which is")
print("  a claim that has to be argued rather than asserted.  O2 is that the")
print("  STRICTEST SELF-RULE ranged over one directory while the artifacts it")
print("  was about lay outside it.  S1 asks *which counts does this tree")
print("  print*, and a count this tree prints is in a transcript this tree")
print("  wrote -- the population and the question have the same boundary.  If")
print("  this tree ever publishes prose carrying its own counts, that prose is")
print("  outside S1 and S1 becomes the defect it is checking.  It does: this")
print("  tree ships a README and an OUTCOMES.  SO S1 IS RUN OVER THOSE TOO:")
print()
MY_ART = B.published_by(B.MY_TAG)
extra_art = [p for p in MY_ART if p.endswith(".md")]
led2 = []
for p in extra_art:
    for row in B.grain_ledger(B.read(p, None)):
        led2.append((os.path.basename(p),) + row)
print("      PROSE ARTIFACTS of mine `published_by` finds        %3d"
      % len(extra_art))
for p in extra_art:
    print("          %s" % p)
print("      count ROWS in them                                 %3d" % len(led2))
bad2 = [r for r in led2 if r[5] != "label"]
print("      ...NOT at stage `label`                            %3d" % len(bad2))
for o, i, label, nums, g, s in bad2[:8]:
    print("          *** %s:%d [%s/%s]  %s" % (o, i, g, s, label[:40]))
BAD += len(bad2)
if not extra_art:
    print("      (none yet -- this tree's commits are not in the log until it")
    print("       is committed, so the FIRST run of this probe necessarily sees")
    print("       zero and the committed run is the one that counts.  Stated")
    print("       because a zero here could otherwise read as a pass.)")

# ---------------------------------------------------------------------------
B.hdr("S3  DOES `libbf79.py` DEFINE A RULE THE ARC ALREADY HAS?")

print("  The floor item turned on the tree that found it.  Every module-level")
print("  `def` in `libbf79.py`, checked against the three libraries it")
print("  imports:")
print()
mine = B.defined_names("%s/libbf79.py" % B.TREE)
others = {
    "lib56dc": B.defined_names("%s/lib56dc.py" % B.AUDIT),
    "lib7522": B.defined_names("%s/lib7522.py" % B.LIB7522),
    "lib70c7": B.defined_names("%s/lib70c7.py" % B.SUBJECT),
}
print("      module-level DEFS in libbf79.py                    %3d" % len(mine))
for k, v in sorted(others.items()):
    print("      ...also defined in %-10s                     %3d"
          % (k, len(mine & v)))
clash = sorted(n for n in mine if any(n in v for v in others.values()))
print("      NAMES of mine that collide with an imported one    %3d" % len(clash))
for n in clash:
    where = [k for k, v in sorted(others.items()) if n in v]
    print("          *** %s  (also in %s)" % (n, ", ".join(where)))
BAD += len(clash)
print()
print("      RULES of mine that are ALIASES, not copies:")
src = B.read("%s/libbf79.py" % B.TREE, None)
for m in re.finditer(r"^(\w+) = (A|L|M)\.(\w+)$", src, re.M):
    print("          %-20s -> %s.%s" % (m.group(1), m.group(2), m.group(3)))
print()
print("  AND `grain_ledger` IS THE ONE THING WRITTEN HERE.  It is a JOIN of two")
print("  imported predicates and computes no grain and no population of its")
print("  own; if `lib56dc.grain_of` is wrong, this is wrong the same way, which")
print("  is the property a delegation is supposed to have.")

# ---------------------------------------------------------------------------
B.hdr("S4  mg-56dc'S TREE -- READ, NOT WRITTEN")

print("  An audit's tree is its evidence.  This repair IMPORTS mg-56dc's")
print("  library to close what mg-56dc found, which is not the same as editing")
print("  its findings -- and the difference is checkable:")
print()
dirty = B.clean_tree([B.AUDIT])
print("      files of mg-56dc's tree modified in the worktree    %3d" % len(dirty))
for p in dirty:
    print("          *** %s" % p)
BAD += len(dirty)
print()
also = B.clean_tree(["code/runner_exit_audit_dee4"])
print("      files of mg-dee4's tree modified in the worktree    %3d" % len(also))
for p in also:
    print("          *** %s" % p)
BAD += len(also)
print()
print("  AND THE TREES THIS TICKET DOES MODIFY, named so the boundary is a")
print("  fact rather than an intention:")
print()
for tree in (B.SUBJECT, B.LIB7522, "docs"):
    ch = B.clean_tree([tree])
    print("      %-34s %3d file(s) modified" % (tree, len(ch)))
    for p in ch:
        print("          %s" % p)
print()
print("  mg-56dc's README cites `6aa043a` for its predictions commit and that")
print("  commit is NOT reachable from HEAD -- the reachable counterpart is")
print("  `abb95b0`.  OBSERVED AND NOT REPAIRED, for the reason above.  It is")
print("  recorded here rather than fixed because fixing it would mean editing")
print("  the evidence of the audit that found four of the five things this")
print("  ticket closes.")
anc = B.A.git("merge-base", "--is-ancestor", "6aa043a", "HEAD", ok=(0, 1, 128))
print()
for rev in ("6aa043a", "abb95b0"):
    out = B.git("rev-parse", "--verify", "--quiet", "%s^{commit}" % rev,
                ok=(0, 1)).strip()
    if out:
        code = B.A.git("merge-base", "--is-ancestor", rev, "HEAD",
                       ok=(0, 1)) is not None
        anc_ok = os.system("git -C %s merge-base --is-ancestor %s HEAD 2>/dev/null"
                          % (B.REPO, rev)) == 0
    else:
        anc_ok = False
    print("      `%s`  resolves: %-3s  ancestor of HEAD: %s"
          % (rev, "yes" if out else "no", "yes" if out and anc_ok else "NO"))

print()
B.bar("P5 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a count row of mine whose grain is not")
print("on its own label -- in a transcript or in my prose -- a name in")
print("`libbf79.py` that collides with a rule of a library it imports, and a")
print("file of mg-56dc's or mg-dee4's tree modified in the worktree.  It ranges")
print("over the %d count ROWS of my %d transcript(s), the %d count ROWS of my"
      % (len(led), len(MY_OUTS), len(led2)))
print("%d prose artifact(s), my %d module-level DEFS and the two audit trees."
      % (len(extra_art), len(mine)))
print("It does NOT count S1b's naked-label row, which approximates a rule about")
print("MEANING with a word list and is printed for disagreement rather than")
print("scored.")
print()
print(B.finding("P5a", "this tree's own defects of the class it repairs, "
                       "recorded rather than smoothed away: a provenance query "
                       "whose `\\(` was a BRE GROUP and silently returned my "
                       "auditor's artifacts as mine; a revision-and-grain check "
                       "that was LINE-LOCAL over hard-wrapped prose in two "
                       "different places, which is mg-dee4's F4 twice; an "
                       "alternative diff that compared REGEX SOURCE against "
                       "mg-dee4's PROSE RENDERING and reported 3 phantom gains; "
                       "a moved-numbers claim that attributed ARC DRIFT to this "
                       "ticket until a controlled counterfactual separated them; "
                       "and P1f's own blind-spot test inheriting the blind spot "
                       "it measures -- SIX, on a tree whose subject is "
                       "instruments that agree for the wrong reason"))
print(B.finding("P5b", "count ROWS of mine at stage `label`: %d of %d in "
                       "transcripts and %d of %d in prose, %d at `header` or "
                       "`-`; and %d of my %d labels name a POPULATION as well "
                       "as a grain, which is printed for disagreement and not "
                       "scored because a word list approximating a rule about "
                       "meaning is the hand-list this arc keeps finding"
                       % (len(led) - len(bad_stage), len(led),
                          len(led2) - len(bad2), len(led2),
                          stages.get("header", 0) + stages.get("-", 0),
                          len(led) - len(naked), len(led))))
sys.exit(1 if BAD else 0)
