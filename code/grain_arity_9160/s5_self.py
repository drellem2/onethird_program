"""mg-9160 / S5 -- MY OWN DEFECTS, THE SCORING, AND WHAT I DID NOT DO.

The ticket ends with three instructions and this probe answers all three:

    CORRECT MY FRAMING -- it has already been corrected once on this ticket,
    by the auditor, and correctly.
    STATE WHAT YOU DID NOT DO.

  S5a  the eight bets of PREDICTIONS.md, scored, including the one that MISSES.
  S5b  the defects of THIS instrument, recorded rather than smoothed away.
  S5c  the two O4 items my ticket carries, and their status here.
  S5d  what I did not do.

Exit code = number of S5 checks that fail.  A MISSED PREDICTION IS NOT A
FAILING CHECK -- a bet that cannot lose is not a bet.
"""

import sys
import textwrap

import lib9160 as G

BAD = 0
A = G.A


def para(t, bullet="  * ", cont="    "):
    body = textwrap.wrap(" ".join(t.split()), 70)
    print(bullet + body[0])
    for extra in body[1:]:
        print(cont + extra)
    print()


G.bar("mg-9160 / S5 -- MY OWN DEFECTS AND WHAT I DID NOT DO")
print("HEAD: %s" % G.head())

# ---------------------------------------------------------------------------
G.hdr("S5a  THE BETS, SCORED")

SCORE = [
    ("P1", 0.97, "HIT",
     "arity forces 210 of the 623; 413 -- 66.3% -- are the word lists. "
     "The ticket's `a property of its ARITY, NOT its VOCABULARY` is false "
     "at two thirds of its own evidence.  S2b."),
    ("P2", 0.90, "HIT",
     "the six-axis graph is a FOREST and `chromatic` returns 2, with a "
     "triangle control that returns 3.  A TWO-valued vocabulary of "
     "`_classify`'s exact form separates all six axes; `_classify` "
     "separates 3, of which 1 by two words it knows.  S2d."),
    ("P3", 0.85, "HIT",
     "at the corpus's 400 nouns the floor is 19800 of 79800 and the "
     "observed collapse is 68596 -- arity is 28.9% of it.  S2c."),
    ("P4", 0.80, "HIT",
     "the open-set classifier splits BOTH pairs A1f adjudicated SAME. "
     "Kept, not special-cased, and asserted by a selftest arm.  S4b."),
    ("P5", 0.75, "HIT",
     "2268 trailing integers against 1191 count rows.  The population "
     "rule collapses a second time and the ticket's 626 understates the "
     "uncounted set by 3.4x: 2107 of 2894 integers have no grain of "
     "their own.  S3a."),
    ("P6", 0.60, "SPLIT",
     "the repaired population reaches all 5 of AF2's rows and gives each "
     "integer its own noun -- but `reaches` was the wrong word for what "
     "it buys.  4 of the 5 come back with the parent's DETAIL LINE "
     "naming the noun one column right, which is a finding I did not "
     "predict, and 8 integers move.  S3c."),
    ("P7", 0.55, "MISS",
     "I bet all four figures reproduce EXACTLY AT `9f1ecaa`.  They do "
     "not -- at that ref the corpus is 510 files and 1068 rows.  They "
     "reproduce at a RECONSTRUCTION (9f1ecaa + mg-03d1's own seven "
     "transcripts as published) which my bet did not name.  The HEAD "
     "half lands: not one of the five reproduces there.  S1b."),
    ("P8", 0.50, "HIT",
     "`silently returns NONE` is my own wording and it is wrong.  373 of "
     "1191 rows -- 31.3% -- get their grain from a DIFFERENT LINE and "
     "`grain_of` returns the stage that says so.  The defect is "
     "attribution, not silence.  S1c."),
]
print("      %-5s %-6s %-7s %s" % ("bet", "prior", "outcome", "what happened"))
for pid, prior, out, why in SCORE:
    body = textwrap.wrap(" ".join(why.split()), 52)
    print("      %-5s %-6.2f %-7s %s" % (pid, prior, out, body[0]))
    for extra in body[1:]:
        print("      %-5s %-6s %-7s %s" % ("", "", "", extra))
print()
G.pop("the 8 bets of PREDICTIONS.md, one row each")
G.row("...BETS scored HIT", sum(1 for s in SCORE if s[2] == "HIT"), "bet")
G.row("...BETS scored SPLIT", sum(1 for s in SCORE if s[2] == "SPLIT"), "bet")
G.row("...BETS scored MISS", sum(1 for s in SCORE if s[2] == "MISS"), "bet")
print()
para("P7 STAYS A MISS AND IS NOT RESCUED.  The reconstruction reproduces "
     "all five figures exactly, which is a better result than the bet "
     "asked for -- and it is a DIFFERENT POPULATION from the one I named. "
     "Scoring it as a hit would be the post-hoc refinement A1e refused to "
     "make about its own 1-versus-3, in the tree that praises A1e for "
     "refusing.", bullet="  ")
para("AND THE PRIORS WERE TOO LOW BECAUSE THE EXPOSURE WAS TOTAL.  Six of "
     "eight land outright and a seventh splits, and H1 says why: my ticket body printed every figure "
     "and P1-P3 are arithmetic I did on paper before the directory "
     "existed.  A 0.97 that lands is not a calibrated forecast, it is a "
     "sum checked twice.", bullet="  ")

# ---------------------------------------------------------------------------
G.hdr("S5b  THE DEFECTS OF THIS INSTRUMENT")

DEFECTS = [
    ("D1", "MY OWN `row()` PRINTS A NOUN THAT IS NOT THE UNIT, AND I FOUND "
     "IT IN MY OWN OUTPUT.  `row()` checks each label against my open-set "
     "extractor and prints the noun it reads.  On `...count ROWS whose "
     "grain reads BOTH` it prints `read`, and on `...AXES to be separated` "
     "it prints `separated`.  The extractor takes the LAST content word, "
     "and my labels end in the SYMBOL rather than in the unit.  So the "
     "check I substituted for mg-03d1's cannot fail on vocabulary and CAN "
     "mislead -- E7 said it would be weaker and did not say it would be "
     "wrong on my own rows.  NOT REPAIRED: the alternative is to write my "
     "labels to satisfy my extractor, which is AS3 happening to me with "
     "an extractor of my own choosing."),
    ("D2", "`column_shape` WAS DESIGNED AFTER SEEING THE ROWS IT SEPARATES. "
     "Its strict-alternation rule is not fitted to a constant, but it was "
     "written with AF2's five rows on the screen, and it agrees with my "
     "hand reading of exactly those five.  There is no labelled set, so "
     "its 233 resolutions over 626 integers are a rule's output and not a "
     "measured accuracy.  Stated at the definition, in `s3_population.py`, "
     "and here."),
    ("D3", "MY OPEN-SET CLASSIFIER DROPS 32 OF THE 400 NOUNS BEFORE "
     "CLASSIFYING ANYTHING.  `grain_open` commits to ONE noun per label "
     "where A1d's extractor returns the SET, so a label carrying two "
     "grains gets one of them -- the very defect S3 measures in "
     "`count_rows`, committed by the function I wrote to fix it.  Found by "
     "my own S4a printing both counts side by side, and kept side by side."),
    ("D4", "I INHERIT AS5 IN FULL AND EVERY RATIO OVER THE 400 CARRIES IT. "
     "`grain_nouns` over-collects: `about`, `anyway`, `bfd` and `y` are "
     "among the 400 and are printed in S4a's list.  I import the parent's "
     "extractor rather than trimming it, for the parent's reason -- a "
     "trimmed list makes the collapse ratio a fact about my trimming."),
    ("D5", "THE ADJUDICATION TABLE IS SEVEN PAIRS WIDE AND I SCORE TWO "
     "INSTRUMENTS ON IT.  `SAME_GRAIN`/`DIFF_GRAIN` are mg-03d1's "
     "judgements, quoted, and 7 of the 11 have both poles inside the "
     "corpus's 400 nouns.  A scoreboard 7 rows long over a population of "
     "79800 pairs is an anecdote with arithmetic on it, and S4c says so on "
     "the line above the numbers.  I did not extend the table: adding "
     "adjudications of my own would make the third verdict's count a fact "
     "about how long I sat there."),
    ("D6", "THE CORPUS INCLUDES ITS AUDITORS, MINE INCLUDED.  7 of the 517 "
     "files are mg-03d1's own transcripts.  Once this tree lands, its own "
     "transcripts join the same glob and every figure here shifts for "
     "whoever runs next -- which is why S1b prints three corpus views and "
     "why every count in this tree names the reconstruction rather than "
     "`the corpus`."),
]
G.pop("the DEFECT ITEMS of this tree's own instrument")
G.row("...DEFECT ITEMS recorded", len(DEFECTS), "defect item")
print()
for did, text in DEFECTS:
    print("  %s" % did)
    para(text, bullet="      ", cont="      ")

# ---------------------------------------------------------------------------
G.hdr("S5c  THE TWO O4 ITEMS MY TICKET CARRIES")

para("THE `excludes a git revision` CLAIM IS NOT TOUCHED HERE.  My ticket "
     "says so itself: mg-5035 owns it, filed earlier from mg-bf79's own "
     "report, and my ticket's mention is a second confirmation, not a "
     "second ticket.  I have re-derived nothing about it and printed no "
     "number about it.  Any figure about that claim in this tree would be "
     "a duplicate of somebody else's open work.")

FIG = "code/runner_exit_repair_70c7/lib70c7.py"
src = G.read(FIG)
import re                                                    # noqa: E402
m = re.search(r"^def figures\(.*?(?=^def |\Z)", src, re.M | re.S)
body = [ln for ln in (m.group(0).splitlines()[1:] if m else [])
        if ln.strip() and not ln.strip().startswith(("'''", '"""', "#"))]
indoc = False
stmts = []
for ln in (m.group(0).splitlines()[1:] if m else []):
    s = ln.strip()
    if s.startswith('"""'):
        indoc = not indoc or s.count('"""') == 2 and False
        if s.count('"""') >= 2:
            indoc = False
        continue
    if indoc or not s or s.startswith("#"):
        continue
    stmts.append(s)
print("  `lib70c7.figures`, as it stands on disk now:")
print()
for s in stmts:
    print("      %s" % s[:66])
print()
G.pop("the executable STATEMENTS of `lib70c7.figures` after its docstring")
G.row("...STATEMENTS in the body", len(stmts), "python statement")
G.row("...of those, STATEMENTS that DELEGATE the figure RULE",
      sum(1 for s in stmts if re.search(r"\.figures\s*\(", s)),
      "python statement")
print()
para("DUPLICATION REMOVED, NOT RECONCILED -- CONFIRMED BY READING, AND "
     "MEASURED AT NOTHING ELSE.  The body is a call.  So `1001 of 1001 "
     "agree` is true BY CONSTRUCTION and cannot fail: whatever the two "
     "copies disagreed about before, the check that would have caught it "
     "is now a check that a function agrees with itself.  If they were "
     "ever two independent readings of `what is a figure`, that property "
     "is gone and no number in this arc records what it was worth.")

para("AND I DID NOT MEASURE IT FURTHER, DELIBERATELY.  Establishing what "
     "the lost independence was worth means running the PRE-delegation "
     "copies over the corpus and differencing them, which is a second "
     "tree's work on mg-70c7's subject, not a line item in a ticket about "
     "the classifier's arity.  It is stated here so it is on the record "
     "and not folded into a count.")

# ---------------------------------------------------------------------------
G.hdr("S5d  WHAT I DID NOT DO")

for t in [
    "I DID NOT ADD `ROW_WORDS`, OR ANY WORD, TO `SITE_WORDS` OR "
    "`EXEC_WORDS`.  The ticket forbids it and S2 gives a second reason: "
    "the six axes are separable at TWO values, so the vocabulary can be "
    "re-cut to fit any six axes known in advance and fits the seventh no "
    "better.  Nothing in this tree proposes a vocabulary.",

    "I DID NOT MIGRATE ANY CALL SITE.  `lib56dc`, `lib03d1`, `libbf79` and "
    "`lib70c7` are byte-identical to their published state; no transcript "
    "of another tree is regenerated; no published number moves.  The eight "
    "integers of S3c are a correction to a DETAIL LINE in mg-03d1's AF2, "
    "and AF2's count of 5 is unchanged.",

    "I DID NOT REPAIR `embedded_counts`.  I disagree with its rule and "
    "S3b prints the disagreement row by row, but an auditor's tree is its "
    "evidence.  What a repair would need is in S3b; whether to apply it is "
    "mg-03d1's or its successor's call.",

    "I DID NOT GIVE THE 1481 SHARED-GRAIN INTEGERS THEIR OWN NOUNS.  That "
    "needs a column-header parser and this arc has none.  They are counted "
    "and named as SHARED and left there.",

    "I DID NOT VERIFY THAT ANY ATTACHED NOUN IS THE RIGHT GRAIN FOR ITS "
    "INTEGER.  E6.  Being in the population is not being classified "
    "correctly, and only a re-derivation beside the row settles it.",

    "I DID NOT EXTEND THE ADJUDICATION TABLE.  Seven usable pairs out of "
    "79800 is the honest state of this arc's knowledge and enlarging it by "
    "hand would make the third verdict's headline a fact about me.",

    "I DID NOT TOUCH mg-5035's SUBJECT, and I did not measure what "
    "`lib70c7.figures`' delegation cost.",

    "I DID NOT SCORE P7 AS A HIT even though the reconstruction reproduces "
    "all five figures exactly.",
]:
    para(t)

print("S5 TOTAL BAD: %d" % BAD)
print()
print(G.finding("F1", "arity forces 210 of 623 collapsed pairs; 413 are the "
                      "word lists -- the ticket's stated cause is a minority "
                      "share of its own evidence"))
print(G.finding("F2", "the six named grain axes form a FOREST and are "
                      "separable at TWO values, so `nowhere in a four-valued "
                      "function to put a third distinction` is false"))
print(G.finding("F3", "2107 of the corpus's 2894 printed integers have no "
                      "grain of their own, against the 626 the ticket names "
                      "-- 3.4x"))
print(G.finding("F4", "`lib03d1.embedded_counts` names the noun one column "
                      "right on 8 integers across 4 of AF2's 5 rows; AF2's "
                      "count of 5 stands"))
print(G.finding("F5", "the arc has adjudicated 7 of 79800 grain pairs and "
                      "both instruments answer all 79800"))
sys.exit(BAD)
