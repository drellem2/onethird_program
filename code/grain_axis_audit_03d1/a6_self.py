"""mg-03d1 / A6 -- THE FLOOR ITEM NOTHING NAMES, AND THIS AUDIT'S OWN DEFECTS.

AF  A COUNT PRINTED INSIDE ANOTHER COUNT'S LABEL IS OUTSIDE THE POPULATION
    THAT CLAIMS TO COVER EVERY PRINTED COUNT.

    `lib56dc.count_rows` yields one (label, value) per LINE.  A line like

        ...ROWS outside it, across 10 distinct basenames            14

    carries TWO counts at TWO grains -- `basenames` and `ROWS`.  The line gets
    ONE grain symbol.  The `10` is not mis-classified; it is NEVER CLASSIFIED,
    because it is not in the population.  That is O2's shape (a population that
    excludes part of what it is about) inside the instrument that measures O1,
    and it is not the parent's recorded defect #5: #5 is about a CLASSIFIED row
    the classifier cannot resolve.

AS  and the defects of THIS instrument, recorded rather than smoothed away.
    Five consecutive deliverables in this lineage found their own defect class
    in their own tooling; the sixth found eight.  This is the seventh.

Exit code = count rows of THIS tree not at classifier stage `label` (my own
P5b), which is the only arm here that is a fault rather than a finding.
"""

import os
import sys
import textwrap

import lib03d1 as B

# mg-2ff6 -- the dated-population convention, through the parent library.
C = B.convention()

A = B.A
BF = "code/runner_exit_repair_bf79"

print("mg-03d1 / A6 -- THE FLOOR, AND MY OWN DEFECTS")
print("HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("AF1  HOW BIG IS THE UNCOUNTED POPULATION?")

paths = B.all_transcripts()
tot_rows = emb_rows = emb_counts = 0
per_tree = {}
for p in paths:
    try:
        txt = B.read(p)
    except OSError:
        continue
    for _i, label, _n in A.count_rows(txt):
        tot_rows += 1
        e = B.embedded_counts(label)
        if e:
            emb_rows += 1
            emb_counts += len(e)
            per_tree[p.split("/")[1]] = per_tree.get(p.split("/")[1], 0) + 1
# mg-2ff6 -- OBSERVED.  AF1's population is the disk glob and this tree
# is 7 files of it; the `517` that stood here undated was a reading of
# a corpus that existed for the length of one run.
C.pop("every count ROW of every `code/*/out_*.txt` on disk")
B.plain("...ARTIFACTS in that corpus", len(paths))
print("      ^ one unit of that number is one transcript file")
B.plain("...count ROWS `lib56dc.count_rows` returns", tot_rows)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS carrying a count INSIDE the label", emb_rows)
print("      ^ one unit of that number is one printed line")
B.plain("...integer ITEMS inside labels, never classified", emb_counts)
print("      ^ one unit of that number is one integer printed in a label")
print()
print("  So `every printed count` is short by %d.  The rule that defines the"
      % emb_counts)
print("  population is a SHAPE RULE OVER THE LINE -- label, whitespace, number")
print("  at the end -- and a number that is not at the end of the line is not")
print("  a count to it.  That rule is deliberate and its docstring defends it")
print("  well (`a sentence is not a count row`), and the cost of it is this")
print("  number, which nothing in the arc has printed before.")
print()
tops = sorted(per_tree.items(), key=lambda kv: -kv[1])[:8]
print("  The 8 TREES with the most such rows, so the total is checkable:")
for t, n in tops:
    print("      ROWS in %-40s %4d" % (t, n))

# ---------------------------------------------------------------------------
B.hdr("AF2  AND WHERE THE TWO COUNTS ON ONE LINE ARE AT DIFFERENT GRAINS")

print("  An uncounted number is only a defect if it means something else than")
print("  the number that WAS counted.  So: rows where the embedded count's own")
print("  grain noun classifies differently from the row's, under the same")
print("  `label_grain` used in A3.  Those are lines where the ONE grain the")
print("  instrument reports is wrong for ONE of the two numbers on the line.")
print()
mixed = []
for p in paths:
    try:
        txt = B.read(p)
    except OSError:
        continue
    lines = txt.splitlines()
    for i, label, nums in A.count_rows(txt):
        for v, noun in B.embedded_counts(label):
            if not noun:
                continue
            eg = B.NOUN_GRAIN.get(B.singular(noun.lower()))
            lg, _st = B.label_grain(label,
                                    list(reversed(lines[max(0, i - 9):i - 1])))
            if eg and lg and eg not in lg:
                mixed.append((p, i, label, v, noun, eg, sorted(lg)))
C.pop("the %d ROWS of AF1 carrying a count inside the label" % emb_rows)
B.plain("...ROWS whose two counts are at DIFFERENT grains", len(mixed))
print("      ^ one unit of that number is one printed line")
print()
for p, i, label, v, noun, eg, lg in mixed[:10]:
    print("      %s:%d" % (p, i))
    print("          %s" % label[:66])
    print("          the row is reported at grain %-9s the embedded `%d %s`"
          % ("/".join(lg) + ";", v, noun))
    print("          is at grain %s -- and is in no population" % eg)
print()
print("  EVERY ONE OF THOSE IS A ROW/SITE-CLASS COLLAPSE ON A SINGLE LINE, and")
print("  the instrument has no place to put the second grain even if it had a")
print("  word for it: `count_rows` returns ONE label per line.  A1 said the")
print("  limit was the classifier's arity.  THIS IS THE SAME LIMIT ONE LAYER")
print("  DOWN, in the population rule -- one grain per line, because one row")
print("  per line.  Fixing the classifier would not reach these.")
print()
bf_rows = 0
for p in paths:
    if not p.startswith(BF):
        continue
    for _i, label, _n in A.count_rows(B.read(p)):
        if B.embedded_counts(label):
            bf_rows += 1
C.pop("the count ROWS of `%s`'s own transcripts" % BF)
B.plain("...ROWS of the parent's own carrying an uncounted count", bf_rows)
print("      ^ one unit of that number is one printed line")
print()
print("  AND THE PARENT'S `p5_self.py` REPORTS 0 OF THESE, because its")
print("  population is `count_rows` too.  A self-check inherits the population")
print("  rule of the check it is applying, so the one thing it cannot find is a")
print("  defect OF that rule.  That is the general form of the parent's #7 and")
print("  of A1 at once, and it is why the floor item is here rather than in the")
print("  brief: a list of things to check is written in the vocabulary of the")
print("  instrument that will check them.")

# ---------------------------------------------------------------------------
B.hdr("AS  THE DEFECTS OF THIS INSTRUMENT, RECORDED RATHER THAN SMOOTHED AWAY")

DEFECTS = [
    ("AS1", "`label_grain` took the LAST grain noun of a label, so on "
     "`...ROWS outside it, across 10 distinct basenames` it read `basenames` "
     "-- the EMBEDDED count's noun -- and reported the repaired artifact as "
     "DEFECTIVE ON 2 OF 8 ROWS where the artifact is right. THE AUDITED "
     "DEFECT RUN BACKWARDS BY THE AUDITOR: a value attributed to the wrong "
     "noun on the same line. Repaired by preferring the CAPITALISED grain "
     "noun -- this arc's own post-repair convention -- and the stage is now "
     "returned rather than folded away."),
    ("AS2", "A3c put MY PARENT'S tag `(mg-bf79)` to `published_by` and "
     "printed 9 under a label saying `the E1 population`. E1's population is "
     "`published_by('(mg-70c7)')` and is 11. I was two minutes from reporting "
     "`the parent's headline 7 -> 11 does not reproduce; it is 9`. A "
     "POPULATION FUNCTION TAKING A TAG RETURNS ONE SET PER TAG, and the tag "
     "is part of the population's NAME -- so a count under the wrong tag is a "
     "value under a label that is about somebody else, which is O1 at the "
     "population layer. Both tags are printed now."),
    ("AS3", "THE SELF-RULE FORCES MY LABELS INTO THE VOCABULARY OF THE "
     "INSTRUMENT I AM AUDITING. `lib03d1.row()` requires every label to "
     "classify at stage `label` under `lib56dc.grain_of`, whose vocabulary is "
     "35 SITE words and 8 EXEC words. My subject is grain distinctions it has "
     "NO WORD FOR -- and to pass my own check I must describe them using only "
     "words it does. Every `...PAIRS`, `...AXES` and `...DISTINCTIONS` row in "
     "A1 had to be re-worded to carry `WORDS`, `ROWS` or `ITEMS`. NOT "
     "REPAIRED, because the alternative is to exempt myself from the rule I "
     "am auditing compliance with. It is A1's finding happening to me."),
    ("AS4", "A5d's preservation check for mg-56dc's T5d kept miss was written "
     "as `MISS -- 38 members` and the text says `MISS — 38 members` with an "
     "EM DASH. It reported a PRESERVED artifact as `*** LOST ***`, which "
     "under the brief's own weighting is the highest-severity verdict this "
     "audit can return. Written from my QUOTATION of the text rather than "
     "from the text, and wrong by one character. mg-aaf4 recorded the same "
     "shape -- a detector missing the sentence it was written for, by one "
     "tense. Repaired by matching the FIGURE and the NOUN with the "
     "punctuation loose."),
    ("AS5", "`grain_nouns` OVER-COLLECTS and is not trimmed after the fact. "
     "A1d's 400 distinct grain words include `about`, `actual`, `anyway` and "
     "`bfd`. Trimming them would make the collapse ratio a fact about my "
     "trimming, so the full extracted vocabulary is printed and A1d also "
     "prints the stricter ratio over only the words the classifier has an "
     "entry for. The generous metric is the PRE-REGISTERED one and it MISSED; "
     "the strict one is printed beside it and does not rescue it."),
    ("AS7", "A4d TOOK ITS SUBJECT BY POSITION AND RAN ITSELF. It picked "
     "`newmv[0]` -- the first tree whose runner writes `.new` and moves it -- "
     "which was the parent's until THIS TREE ADOPTED THE SAME FIX, at which "
     "point it was mine, alphabetically first. The probe ran its own runner, "
     "which ran the probe, which ran its own runner. Found by the suite's "
     "first full run wedging, not by reading. THE POPULATION SILENTLY "
     "INCLUDED THE AUDITOR the instant the auditor started complying with the "
     "thing being audited -- which is O2's shape a third time, in the sweep "
     "that measures O2's runner defect. Repaired by naming the subject rather "
     "than indexing it; and A4a now prints BOTH totals, because excluding "
     "myself from the count to protect prediction A4b would be the same "
     "defect wearing the other face."),
    ("AS6", "A4b's `bites` test is a STATIC approximation: it asks whether "
     "any probe of a tree mentions `out_*.txt`, not whether THAT probe reads "
     "THE TRANSCRIPT THAT RUN TRUNCATED FIRST. It will over-report a tree "
     "whose probe reads another tree's transcripts and under-report one that "
     "reaches a transcript through a variable. 43 is an upper bound on a "
     "lower-bound question, stated here rather than defended as exact."),
]
C.pop("the DEFECTS of this tree's own instrument, found by this")
print("  probe and by the runs that preceded it")
B.plain("...DEFECT ITEMS of this instrument recorded", len(DEFECTS))
print("      ^ one unit of that number is one defect")
print()
for tag, text in DEFECTS:
    print("  %s" % tag)
    for ln in textwrap.wrap(text, 68):
        print("      %s" % ln)
    print()

# ---------------------------------------------------------------------------
B.hdr("AS7  MY OWN P5b -- EVERY COUNT ROW I PRINT, AT STAGE `label`")

mine = sorted(f for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
              if f.startswith("out_") and f.endswith(".txt"))
here = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
print("  Including this probe's own, which the runner preserves by writing")
print("  `.new` and moving it -- the parent's #7 fix, adopted here rather")
print("  than re-discovered.")
C.pop("every `out_*.txt` of THIS tree on disk, this probe's own included")
B.plain("...ARTIFACTS of mine on disk", len(mine))
print("      ^ one unit of that number is one transcript file")
rows = bad = 0
offenders = []
for f in mine:
    txt = B.read("code/%s/%s" % (here, f))
    lines = txt.splitlines()
    for i, label, nums in A.count_rows(txt):
        rows += 1
        g, st = A.grain_of(label, list(reversed(lines[max(0, i - 9):i - 1])))
        if st != "label":
            bad += 1
            offenders.append((f, i, label, g, st))
B.plain("...count ROWS in them", rows)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS NOT carrying a grain word on their own label", bad)
print("      ^ one unit of that number is one printed line")
for f, i, label, g, st in offenders[:12]:
    print("          *** %s:%d [%s/%s]  %s" % (f, i, g, st, label[:44]))
print()
if not mine:
    print("      (no transcripts on disk yet -- the FIRST run of this probe")
    print("       necessarily sees zero, and the COMMITTED run is the one that")
    print("       counts.  Stated because a zero here could otherwise read as a")
    print("       pass, which is the parent's #7 in the shape that hides it.)")
print("  AND THE POPULATION IS THIS TREE'S TRANSCRIPTS, WHICH IS A PATH, and")
print("  that is not the O2 defect for the reason the parent gives: the")
print("  question is *which counts do I PRINT*, and a count I print is in a")
print("  transcript I wrote.  The prose I ship carries counts too, so it is")
print("  checked as well:")
print()
prose = ["code/%s/%s" % (here, f) for f in ("README.md", "OUTCOMES.md",
                                           "PREDICTIONS.md")
         if os.path.exists(os.path.join(B.REPO, "code", here, f))]
prose_rows = prose_bad = 0
for p in prose:
    txt = B.read(p)
    lines = txt.splitlines()
    for i, label, nums in A.count_rows(txt):
        prose_rows += 1
        g, st = A.grain_of(label, list(reversed(lines[max(0, i - 9):i - 1])))
        if st != "label":
            prose_bad += 1
C.pop("the PROSE ARTIFACTS of this tree on disk")
B.plain("...PROSE ARTIFACTS of mine", len(prose))
print("      ^ one unit of that number is one file")
B.plain("...count ROWS in them", prose_rows)
print("      ^ one unit of that number is one printed line")
B.plain("...ROWS NOT at stage `label`", prose_bad)
print("      ^ one unit of that number is one printed line")

print()
# mg-2ff6 -- the class of the two arc-wide figures this probe prints.  AF1 is
# OBSERVED because its population is the disk glob and this tree is in it;
# AS7's two are GROWING, because their populations are one named tree's files
# and one named tree's prose and neither is what this probe writes.
C.class_block([
    ("AF1, every figure in it", False, True, None),
    ("AS7 `...count ROWS in them` -- my transcripts", False, True, None),
    ("AS7 `...count ROWS in them` -- my prose", False, False, None),
])
print()
print("A6 TOTAL BAD: %d" % (bad + prose_bad))
sys.exit(min(bad + prose_bad, 120))
