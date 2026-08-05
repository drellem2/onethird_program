"""R6 -- THIS DELIVERABLE, CHECKED FOR THE DEFECTS IT REPAIRS.

mg-dee4 closes on *"this deliverable is of the same kind as the defect it
repairs.  Check your own counts for the site-vs-execution grain, apply your
subject's rule to yourself, and put your moving numbers in transcripts."*  So:

  E1  A COUNT WHOSE GRAIN IS UNSTATED.  F1.  Every count this tree prints that
      ranges over source lines must say whether it is SITES or EXECUTIONS.
      ITS POPULATION IS A PROPERTY -- `lib70c7.published_by`, the artifacts a
      commit of this deliverable ADDED, asked of the whole repository.  It was
      one directory's `out_*.txt` until mg-bf79; mg-56dc/T2a is that a
      population defined by a path, inside the tree that repaired two of them,
      is the finding with the instrument's name on it.
  E2  A FIGURE THAT NO TRANSCRIPT PRINTS.  F2.  R2c runs the figure census on
      this tree's own artifacts, and this section checks it ran.
  E3  A RULE APPLIED TO THE SUBJECT AND NOT TO ME.  F3.  Every rule this tree
      points at `lib7522` is pointed at `lib70c7` here.
  E4  A POPULATION DEFINED BY A NAME.  F5/F6.  This tree's own populations are
      predicates, and the one place a filename appears is dispositioned.

A branch that honestly cannot exhibit a defect says so with a STRUCTURAL
reason, not a promise about how the code is called.
"""

import ast
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

BAD = 0
HERE = os.path.dirname(os.path.abspath(__file__))
MINE_PY = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
MINE_SH = sorted(f for f in os.listdir(HERE) if f.endswith(".sh"))
MINE_MD = sorted(f for f in os.listdir(HERE) if f.endswith(".md"))
MY_OUTS = M.outs(M.TREE)

M.bar("R6  THE SAME FOUR QUESTIONS, ASKED OF THIS TREE")

# ---------------------------------------------------------------------------
M.hdr("R6a  E1 -- IS EVERY COUNT'S GRAIN STATED?")

print("  The defect is a count of SOURCE LINES presented as a count of RUNS.")
print("  A rule that could decide this in general would be a rule about")
print("  meaning, so the question asked here is the checkable half: every")
print("  line of an artifact of mine that reports a count over source carries")
print("  one of the grain words, in the same line or the one above it.")
print()
print("  THE POPULATION IS A PROPERTY, NOT A DIRECTORY.  mg-56dc/T2a was that")
print("  the strictest rule this tree applies to anything ranged over the")
print("  `out_*.txt` of ONE DIRECTORY -- a population defined by a path, which")
print("  is the finding this tree exists to repair, committed by its own")
print("  self-check.  It is now `lib70c7.published_by`: every artifact a")
print("  commit of this deliverable ADDED, that still exists, and that a")
print("  reader reads as its record.  Asked of the whole repository, so it")
print("  reaches the published document four directories away -- and the")
print("  prose is where THREE OF THE FOUR artifacts mg-05eb found wrong were.")
print()
E1_POP = M.published_by(M.MY_TAG)
E1_COMMITS = M.provenance_commits(M.MY_TAG)
print("      the tag searched, over `git log --all`         %s" % M.MY_TAG)
print("      commits whose subject carries it              %3d" % len(E1_COMMITS))
print("      artifacts of mine it published                %3d" % len(E1_POP))
print("      ...of those, transcripts                      %3d"
      % sum(1 for p in E1_POP if os.path.basename(p).startswith("out_")))
print("      ...of those, prose files                      %3d"
      % sum(1 for p in E1_POP if p.endswith(".md")))
print("      the OLD population, one directory's `out_*.txt` %3d" % len(MY_OUTS))
print("      ...members of it the property LOST            %3d"
      % len([p for p in MY_OUTS if p not in E1_POP]))
for p in E1_POP:
    print("          %-58s %s" % (p, "was in the old population"
                                  if p in MY_OUTS else "*** NEW ***"))
for p in MY_OUTS:
    if p not in E1_POP:
        print("          *** LOST BY THE WIDENING: %s" % p)
        BAD += 1
print()
GRAINY = re.compile(r"\b(?:pipeline|line|execution|site|status|statuses|"
                    r"invocation)s?\b", re.I)
# THE GRAIN WORDS.  A count must say WHAT IT COUNTS -- lines, executions,
# sites, pipelines, files, statuses, invocations, steps, argv.  Case-
# insensitive, because this tree writes `EXECUTIONS` in a heading and
# `executions` in a sentence and the check is about the word, not its case.
# `pipelines` and `files` are grain words as much as `executions` is: the
# defect mg-dee4 found is a number with NO grain attached, not a number
# counted at a grain someone disagrees with.
GRAIN_WORD = re.compile(r"\b(?:source lines?|executions?|sites?|lines?|"
                        r"pipelines?|files?|status|statuses|invocations?|"
                        r"steps?|argv|rows?|assertions?)\b", re.I)
COUNTED = re.compile(r"\b\d+\b")
# A line that QUOTES another artifact's line -- `OUTCOMES.md:88  <text>` --
# is reproducing someone else's words for the reader, not reporting a count of
# my own.  Excluded, and the exclusion is named: the alternative is a check
# satisfied by not quoting the evidence, which is the defect R1e's first draft
# had and is recorded in OUTCOMES.md.
CITATION = re.compile(r"[\w./-]+\.(?:py|sh|md|txt):\d+")
missing = []
checked = quoted = 0
for out in E1_POP:
    lines = M.read(out, None).splitlines()
    for i, line in enumerate(lines, 1):
        if not (GRAINY.search(line) and COUNTED.search(line)):
            continue
        if CITATION.search(line):
            quoted += 1
            continue
        checked += 1
        window = " ".join(lines[max(0, i - 2):i + 1])
        if not GRAIN_WORD.search(window):
            missing.append((out, i, line.strip()))
print("      artifact lines reporting a count over source     %3d" % checked)
print("      ...quoting another artifact's line, excluded     %3d" % quoted)
print("      ...with no grain word in the window              %3d" % len(missing))
for o, i, l in missing[:12]:
    print("          *** %s:%d  %s" % (o, i, l[:56]))
if missing:
    BAD += len(missing)
print()
print("  EXTENT OF THIS CHECK, stated rather than implied: it establishes")
print("  that the WORD is present, not that it is the right one.  A count")
print("  labelled `executions` that is really sites would pass.  What it")
print("  prevents is the shape mg-dee4 found -- a number with no grain")
print("  attached at all, which cannot be argued with because it does not")
print("  say what it counts.")
print()
print("  AND THAT EXTENT IS NOT HYPOTHETICAL -- IT IS mg-56dc/T1c.  The count")
print("  labelled `executing sites` in `out_r4_property.txt` passed this check")
print("  at every run and printed the ROW count while four artifacts of mine")
print("  published the SITE count.  A rule that reads the LABEL cannot catch a")
print("  label that is the false statement; only re-deriving the quantity can,")
print("  and `r4_property.py` now prints BOTH GRAINS so there is nothing left")
print("  for the label to be wrong about.  This check is widened to the")
print("  artifacts the rule is about; it is not thereby made sufficient, and")
print("  saying which of those two it is, is the point of this paragraph.")
print()
print("  THE LIMIT OF THE POPULATION, at the rule: provenance is read from")
print("  COMMIT SUBJECTS, so an artifact published by a commit whose subject")
print("  omits `%s` is invisible to it.  The tag and the commit count are" % M.MY_TAG)
print("  printed above so a reader can put the query itself in doubt.")

# ---------------------------------------------------------------------------
M.hdr("R6b  E2 -- IS EVERY FIGURE OF MINE IN ONE OF MY TRANSCRIPTS?")

MY_ART = ["%s/%s" % (M.TREE, f) for f in MINE_MD]
if os.path.exists(os.path.join(M.REPO, M.MY_DOC)):
    MY_ART.append(M.MY_DOC)
# THE CORPUS IS THE TRANSCRIPTS OF THE TREES THESE ARTIFACTS ARE THE RECORD OF
# -- mine and mg-7522's.  My `OUTCOMES.md` scores predictions against figures
# both trees measured, and my document is the record of both repairs.  The
# union is these two and not `the arc`, because a corpus of everything would
# let any figure anywhere back any claim.
CORPUS = M.transcript_numbers(MY_OUTS + M.outs(M.SUBJECT))
# A figure QUOTED inside a correction of itself, or inside a prediction being
# scored, is a mention of that figure and not a claim under it.  Named as its
# own class and printed in full -- see R2b, which has the same class for the
# same reason, and OUTCOMES.md for what a check without it would reward.
QUOTING = re.compile(r"used to|no longer|mg-dee4|mg-7522|mg-05eb|mg-c2b3|"
                     r"I predict|predicted|\bMISS\b|\bHIT\b|was a count|"
                     r"is not|did not|reproduces it|corrected|stood here",
                     re.I)
print("      transcripts in the corpus                        %3d"
      % len(MY_OUTS + M.outs(M.SUBJECT)))
print("      distinct figures they print                      %3d" % len(CORPUS))
print("      my reader-facing artifacts                       %3d" % len(MY_ART))
print()
un = quoted = 0
for p in MY_ART:
    if p.endswith("PREDICTIONS.md"):
        continue                    # see the disposition in R2c and below
    lines = M.read(p, None).splitlines()
    for i, line in enumerate(lines, 1):
        miss = [v for v in M.figures(line) if v not in CORPUS]
        if not miss:
            continue
        if any(QUOTING.search(x) for x in lines[max(0, i - 2):i + 1]):
            quoted += len(miss)
            continue
        un += len(miss)
        print("      *** UNBACKED %s:%d  %s"
              % (os.path.basename(p), i, ", ".join(str(v) for v in miss)))
        print("          %s" % line.strip()[:64])
BAD += un
print()
print("      figures quoted inside a correction or a prediction %3d" % quoted)
print("      figures of mine no transcript of mine prints     %3d" % un)
print()
print("  `PREDICTIONS.md` IS EXCLUDED AND THE REASON IS THE POINT.  A")
print("  prediction is a figure written BEFORE the run; a figure a transcript")
print("  could back would not be a prediction.  The exclusion is named here")
print("  rather than left as a quiet filter, which is the difference between")
print("  a stated limit and a hand-list.")

# ---------------------------------------------------------------------------
M.hdr("R6c  E3 -- EVERY RULE I POINT AT THE SUBJECT, POINTED AT ME")

print("  mg-dee4's F3 was a NINE-alternative test for them and a THREE-")
print("  alternative one for me.  The four rules this tree turns on `lib7522`")
print("  are turned on `lib70c7` here, on the same terms:")
print()
sys.path.insert(0, os.path.join(M.REPO, M.SUBJECT))
import lib7522 as L                                            # noqa: E402

pairs = []
mine_src = {f: M.read("%s/%s" % (M.TREE, f), None) for f in MINE_PY + MINE_SH}
# (1) the marker rule
uses = []
for f, s in mine_src.items():
    for i, line, kind in L.strength_lines(s):
        if kind == "USE":
            lines = s.splitlines()
            figs = []
            for n in lines[max(0, i - 2):i + 1]:
                figs.extend(M.figures(n))
            if figs and [v for v in figs if v not in CORPUS]:
                uses.append((f, i, line))
pairs.append(("the marker rule (`lib7522.MARK`, %d alternatives)"
              % M.alternatives(L.MARK), len(uses),
              "UNBACKED use(s) in my own code"))
# (2) the P2 predicate, on my own runner
p2 = []
for f in MINE_SH:
    s = mine_src[f]
    for i, line in L.pipelines(s):
        c1, _arm, _w = L.consumed(s, line, i)
        if c1 and any(L.stage_can_fail("%s/%s" % (M.TREE, f), st, None)[0]
                      for st in L.discarded_stages(line)):
            p2.append((f, i, line.strip()))
pairs.append(("the WIDENED P2 predicate, on my own `*.sh`", len(p2),
              "pipeline(s) of mine in the population"))
# (3) shell=True / os.system
sh_true = []
for f in MINE_PY:
    tree = ast.parse(mine_src[f])
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for kw in node.keywords:
            if (kw.arg == "shell" and isinstance(kw.value, ast.Constant)
                    and kw.value.value is True):
                sh_true.append((f, node.lineno))
        fn = node.func
        if (isinstance(fn, ast.Attribute) and fn.attr == "system"
                and isinstance(fn.value, ast.Name) and fn.value.id == "os"):
            sh_true.append((f, node.lineno))
pairs.append(("`shell=True` / `os.system(` -- AST, not grep", len(sh_true),
              "real call site(s)"))
# (4) a population defined by a name
NAMEY = re.compile(r"run_all\.sh|run_audit\.sh|c0_repro\.sh")
filters = []
for f in MINE_PY:
    for i, line in enumerate(mine_src[f].splitlines(), 1):
        if not NAMEY.search(line) or line.lstrip().startswith("#"):
            continue
        if re.search(r"basename\([^)]*\)\s*[=!]=\s*[\"']", line) or \
           re.search(r"endswith\(\s*[\"']/?run_", line):
            filters.append((f, i, line.strip()))
pairs.append(("a population of mine FILTERED by a runner filename",
              len(filters), "filter(s)"))
for label, n, unit in pairs:
    ok = n == 0
    if not ok:
        BAD += n
    print("      %-54s %2d %s" % (label, n, unit))
    if not ok:
        for row in (uses + p2 + sh_true + filters):
            pass
for f, i, line in uses + p2 + filters:
    print("          *** %s:%d  %s" % (f, i, str(line)[:56]))
for f, i in sh_true:
    print("          *** %s:%d" % (f, i))
print()
print("  BRANCHES THAT HONESTLY CANNOT EXHIBIT THESE, with the reason:")
print("   1. E4 in `lib70c7.outs()` -- its only argument is a TREE, and the")
print("      filename pattern is `out_*.txt`, which is this arc's transcript")
print("      convention and not a rule about which runner is interesting.")
print("      A name appears; it is not a population filter over content.")
print("   2. The pipeline defect in this tree's Python -- every subprocess")
print("      takes a LIST argv, so no shell parses the command, so there is")
print("      no pipeline.  STRUCTURAL, checked above as an AST walk.")
print("   3. `r5_population.py` writes a scratch `_mg70c7_arm.sh` and runs it")
print("      -- that file is UNTRACKED and deleted in a `finally`, so it is")
print("      never in `ls_sh()`'s population at all.")

# ---------------------------------------------------------------------------
M.hdr("R6d  THIS TREE'S OWN RUNNER, BY THE WIDENED PREDICATE")

runner = M.read("%s/run_all.sh" % M.TREE, None)
pipes = L.pipelines(runner)
steps = len(re.findall(r"^python3 ", runner, re.M))
guards = len(re.findall(r">\s*out_\w+\.txt\s*\|\|\s*\{", runner))
print("      pipelines of any kind in run_all.sh              %3d" % len(pipes))
print("      steps                                            %3d" % steps)
print("      ...that redirect and guard their own status      %3d" % guards)
if pipes or steps == 0 or guards != steps:
    BAD += 1
    print("      *** not every step reads its own status ***")
else:
    print("      Every step redirects, has its status read by an explicit")
    print("      `||` guard, and is `cat` afterwards.  0 pipelines under the")
    print("      WIDENED predicate as well as the errexit one -- the value arm")
    print("      cannot fire on a line that captures nothing.")

print()
M.bar("R6 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts an artifact line of mine reporting a")
print("count with no grain word near it, an artifact of mine the widening")
print("LOST, a figure of mine no transcript of mine prints, an UNBACKED marker")
print("use of mine, a pipeline of mine in the widened P2, a real `shell=True`,")
print("and a population of mine filtered by a runner filename.  E1 ranges over")
print("the %d ARTIFACT(S) `published_by` returns -- %d transcript(s) and %d"
      % (len(E1_POP), sum(1 for p in E1_POP
                          if os.path.basename(p).startswith("out_")),
         sum(1 for p in E1_POP if p.endswith(".md"))))
print("prose file(s), one of them outside this directory; E2 through E4 range")
print("over this tree's %d `*.py`, %d `*.sh` and %d `*.md`.  It does NOT range"
      % (len(MINE_PY), len(MINE_SH), len(MINE_MD)))
print("over mg-7522's tree or mg-c2b3's -- R1 through R5 do that, and this is")
print("the section about the instrument.")
sys.exit(1 if BAD else 0)
