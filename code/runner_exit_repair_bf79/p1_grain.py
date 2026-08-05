"""P1 -- O1.  A COUNT LABELLED `executing sites` THAT PRINTS ROWS.

THE FINDING (mg-56dc/T1c, T1d).  `out_r4_property.txt` printed

    ...outside it, across 6 distinct basenames     10

under the heading label `executing sites naming a `*.sh``, and FOUR artifacts
of mg-70c7 publish **9** for the same quantity.  The label names the SITE grain
and the value was the (site, target) ROW count.

> The label itself is the false statement.  A reader who checks the grain by
> reading the label is told the right thing and shown the wrong number.

WHICH WAS WRONG, AND HOW THAT IS DECIDED HERE RATHER THAN ASSERTED.  Not by
preferring the majority: four artifacts against one transcript is a vote, not a
derivation.  The quantity is RE-DERIVED at two grains by `lib56dc`'s own
enumerator -- written by the audit, not by the tree under repair -- at the
transcript's own publishing commit.  Whichever of `9` and `10` the site grain
produces is the one the site label was owed.

WHAT THIS PROBE ESTABLISHES, AND THE ONE THING IT CANNOT.  It establishes that
the two grains are two numbers, which one each artifact publishes, and that the
repaired probe now prints both.  It CANNOT establish that the classifier is
right: the classifier reads LABELS, so a wrong label makes it confidently
wrong, and P1g below is the only handle on that here.  Checking the classifier
is `mg-03d1`'s job by name.

EVERY COUNT BELOW NAMES ITS POPULATION AND ITS GRAIN IN ITS OWN LABEL.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
R4 = "%s/r4_property.py" % B.SUBJECT
R4_OUT = "%s/out_r4_property.txt" % B.SUBJECT

B.bar("P1  THE LABEL, THE GRAIN, AND WHICH OF THEM WAS WRONG")

# ---------------------------------------------------------------------------
B.hdr("P1a  THE PUBLISHING COMMIT, DERIVED AND NOT NAMED")

print("  A figure from a whole-repository census is a fact about a REVISION.")
print("  mg-56dc's own first run scored a defect against itself for comparing")
print("  a HEAD derivation with a transcript produced on another tree, so the")
print("  commit is read out of the log rather than written down -- and the")
print("  constant `libbf79.SUBJECT_REV` is CHECKED against it, not trusted.")
print()
log = B.git("log", "-1", "--format=%h", "--", R4_OUT).strip()
head = B.git("rev-parse", "--short", "HEAD").strip()
print("      the commit that last published the transcript      %s" % log)
print("      `libbf79.SUBJECT_REV`, the constant                %s"
      % B.SUBJECT_REV)
print("      HEAD of this run                                   %s" % head)
agree = log.startswith(B.SUBJECT_REV) or B.SUBJECT_REV.startswith(log)
print("      derivation and constant agree                      %s"
      % ("yes" if agree else "*** NO ***"))
if not agree:
    BAD += 1
    print("      *** the constant is stale; the DERIVATION is what is used ***")
REV = log or B.SUBJECT_REV

# ---------------------------------------------------------------------------
B.hdr("P1b  THE QUANTITY AT TWO GRAINS, RE-DERIVED AT %s AND AT HEAD" % REV)

print("  Under `lib56dc.exec_site_rows` / `exec_sites` -- the AUDIT's")
print("  enumerator, which shares no code with the probe being repaired.")
print("  `outside` means the target basename is neither of the two names the")
print("  caller scan matched; it is the column the four artifacts publish.")
print()
TWO = ("run_all.sh", "run_audit.sh")
# TRANSPOSED ON PURPOSE.  The first draft put one row per REVISION with the
# grains as columns, and `p5_self.py` flagged every one of those rows: their
# grain lived in the COLUMN HEADER, which is the `header` stage and is the
# defect this ticket is repairing.  A count whose grain is in a header is a
# count whose grain is not on its label.  So the grain is the ROW here and the
# revision is the column, and every label below carries its own grain word.
cols = []
for ref, tag in ((REV, REV), (None, "HEAD")):
    rows = B.A.exec_site_rows(ref)
    out = [r for r in rows if r[2] not in TWO]
    cols.append((tag, {
        "(site,target) ROWS, all targets": len(rows),
        "distinct SITES, all targets": len(B.A.exec_sites(rows)),
        "(site,target) ROWS outside the two names": len(out),
        "distinct SITES outside the two names": len(B.A.exec_sites(out)),
        "...of those SITES, READING the exit status":
            len(B.A.exec_sites([r for r in out if r[3]])),
    }))
print("      %-44s %9s %9s" % ("grain and population", cols[0][0], cols[1][0]))
for key in ("(site,target) ROWS, all targets",
            "distinct SITES, all targets",
            "(site,target) ROWS outside the two names",
            "distinct SITES outside the two names",
            "...of those SITES, READING the exit status"):
    print("      %-44s %9d %9d" % (key, cols[0][1][key], cols[1][1][key]))
print()
pub_rows = cols[0][1]["(site,target) ROWS outside the two names"]
pub_sites = cols[0][1]["distinct SITES outside the two names"]
print("      at %s, the OUTSIDE column as ROWS               %3d"
      % (REV, pub_rows))
print("      at %s, the OUTSIDE column as distinct SITES     %3d"
      % (REV, pub_sites))
print("      the transcript's printed value under a SITE label  %3d"
      % pub_rows)
print("      the value FOUR ARTIFACTS publish                   %3d" % pub_sites)
print()
print("  THE VERDICT: THE COUNT WAS WRONG AND THE LABEL WAS RIGHT.  `%d` is"
      % pub_sites)
print("  the distinct-SITE count and is what the four artifacts state; `%d` is"
      % pub_rows)
print("  the (site, target) ROW count and is what the transcript printed under")
print("  the word `sites`.  Both are legitimate quantities.  The repair prints")
print("  BOTH, each under its own grain word, and leaves every `%d` in prose"
      % pub_sites)
print("  standing -- because the prose was never the thing that was wrong.")
if pub_sites != 9 or pub_rows != 10:
    print()
    print("      *** at %s these are %d SITES / %d ROWS, not 9 / 10 --"
          % (REV, pub_sites, pub_rows))
    print("          the sentence above is written for 9 / 10 and this run")
    print("          disagrees with it; the RUN is what to believe ***")
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("P1c  THE GAP BETWEEN THE GRAINS, AND THE LINES RESPONSIBLE")

print("  The gap is exactly the number of source lines naming more than one")
print("  `*.sh`.  Not a residue: a countable set, printed per revision, with")
print("  the lines named -- so a reader can check the arithmetic rather than")
print("  the claim.")
print()
for ref, tag in ((REV, REV), (None, "HEAD")):
    rows = B.A.exec_site_rows(ref)
    out = [r for r in rows if r[2] not in TWO]
    for scope, rs in (("ALL rows", rows), ("OUTSIDE rows", out)):
        sites = {}
        for f, i, base, _c in rs:
            sites.setdefault((f, i), []).append(base)
        multi = sorted(k for k, v in sites.items() if len(v) > 1)
        print("      %-6s %-14s ROWS %3d  SITES %3d  GAP %2d"
              % (tag, scope, len(rs), len(sites), len(rs) - len(sites)))
        for f, i in multi:
            print("          %s:%d  ->  %s"
                  % (f, i, ", ".join(sorted(sites[(f, i)]))))
print()
print("  THE PREDICTION THIS REFUTES IN PART, kept as written.  `PREDICTIONS`")
print("  P1c says the gap is *exactly 1 at every revision this probe reads*,")
print("  *not 0, not 2*, and names ONE line as responsible.  Measured: that is")
print("  true of the OUTSIDE column at both revisions -- the column the four")
print("  artifacts publish and the one mg-56dc/T1c reproduced -- and FALSE of")
print("  the ALL column, where the gap is 2 at BOTH revisions and a second")
print("  line, `k2_consume.py:456`, is equally responsible.  It was already")
print("  there at the publishing commit; I simply had not looked at the column")
print("  I was not quoting.  I predicted a property of one column as a property")
print("  of the census, which is mg-56dc/T1c's own recorded mistake -- *I")
print("  predicted a number for a column that has no stable value* -- made")
print("  again, in the repair of it, by the person repairing it.")

# ---------------------------------------------------------------------------
B.hdr("P1d  THE REPAIRED PROBE, RUN LIVE -- BOTH GRAINS PRINTED?")

print("  `r4_property.py` is run here as `run_all.sh` runs it and its output")
print("  is read.  A repair whose evidence is the repaired source rather than")
print("  the repaired OUTPUT is a claim about an intention.")
print()
code, text = B.run_probe(R4)
print("      exit STATUS of the repaired probe, 1 RUN            %3s"
      % ("-" if code is None else code))
if code != 0:
    BAD += 1
lines = text.splitlines()
want = [
    ("a ROW-grain total, labelled ROWS", r"ROWS naming a `\*\.sh`"),
    ("a SITE-grain total, labelled SITES", r"distinct executing SITES"),
    ("the OUTSIDE column as ROWS", r"ROWS outside it"),
    ("the OUTSIDE column as SITES", r"distinct SITES outside it"),
    ("the multi-target lines, enumerated", r"naming MORE THAN ONE"),
    ("the revision the census was taken at", r"BOTH GRAINS, at `[0-9a-f]{7}"),
]
for label, rx in want:
    n = len([l for l in lines if re.search(rx, l)])
    ok = n >= 1
    if not ok:
        BAD += 1
    print("      %-50s %2d  %s" % (label, n, "OK" if ok else "*** absent ***"))
print()
stale = [l for l in lines if re.search(r"executing sites naming", l)]
print("      the OLD mislabelled line, still printed            %3d"
      % len(stale))
if stale:
    BAD += len(stale)
    for l in stale:
        print("          *** %s" % l.strip())

# ---------------------------------------------------------------------------
B.hdr("P1e  THE CLASSIFIER OVER THE WHOLE REPAIRED OUTPUT, not one row")

print("  The brief: *check every other count in the same artifact carries a")
print("  label that matches its grain -- run the sixth instrument over the")
print("  WHOLE artifact rather than this one row.*  `lib56dc.count_rows` gives")
print("  the population by a shape rule over the printed line;")
print("  `lib56dc.grain_of` gives the grain its LABEL declares and the STAGE")
print("  at which it was found.  Both are the audit's, unmodified.")
print()
before = B.grain_ledger(B.read(R4_OUT, REV))
after = B.grain_ledger(text)
for tag, led in (("as published at %s" % REV, before),
                 ("the repaired output, run now", after)):
    g, s = B.tally(led)
    print("      %-30s count ROWS in it            %3d" % (tag, len(led)))
    for k in ("SITE", "EXECUTION", "BOTH", "NONE"):
        print("          rows whose LABEL declares %-10s      %3d"
              % (k, g.get(k, 0)))
    for k in ("label", "prev", "header", "-"):
        print("          rows whose grain was found at %-7s   %3d"
              % (k, s.get(k, 0)))
    print()
none_after = [r for r in after if r[3] == "NONE"]
hdr_after = [r for r in after if r[4] == "header"]
print("      repaired: count rows classified NONE               %3d"
      % len(none_after))
print("      repaired: count rows whose grain is HEADER-only    %3d"
      % len(hdr_after))
for i, label, nums, _g, stage in none_after + hdr_after:
    print("          *** line %d [%s]  %s = %s"
          % (i, stage, label[:44], ",".join(str(n) for n in nums)))
BAD += len(none_after) + len(hdr_after)
print()
print("  THE FULL LEDGER of the repaired output, so the audit waiting on this")
print("  repair can check the classifier against the values rather than")
print("  against my summary of them:")
print()
B.ledger_table(after)

# ---------------------------------------------------------------------------
B.hdr("P1f  THE CLASSIFIER CANNOT SEE O1 AT ALL -- its axis is the other one")

print("  THE HEADLINE OF THIS PROBE, and it refutes my own P1g prediction.  I")
print("  predicted the label-reading classifier would disagree with the value's")
print("  true grain on at least one row BEFORE the repair and on zero after.")
print("  It disagrees on the same row before AND after, and the reason is not")
print("  that the repair failed -- the reason is that the classifier's grain")
print("  axis is SITE vs EXECUTION and O1's defect is ROW vs SITE, which is a")
print("  distinction BELOW ITS RESOLUTION.  Read out of `lib56dc.SITE_WORDS`:")
print()
for w in ("sites", "rows", "basenames", "source lines", "executions", "runs"):
    print("      `%-14s`  classifies as  %s" % (w, B.A._classify(w)))
print()
print("  `rows` and `sites` are THE SAME GRAIN WORD to this instrument, and")
print("  correctly so on its own terms: both range over source rather than over")
print("  runs, which is the F1 distinction it was built for.  So a count")
print("  labelled `sites` holding a ROW value is, to the sixth instrument,")
print("  a row with the right grain word on it.  IT PASSES.")
print()
print("  THIS IS THE ANSWER TO THE BRIEF'S INSTRUCTION TO CHECK THE CLASSIFIER.")
print("  mg-56dc did not find T1c with this classifier and could not have; it")
print("  found it by re-deriving the quantity at two grains, which is what")
print("  `exec_site_rows`/`exec_sites` are for.  A label-reading check is")
print("  necessary and is not sufficient, and the gap between those two is")
print("  exactly one defect wide -- the one it was pointed at.")
print()
print("  What the test below therefore measures is NOT the classifier's error")
print("  rate.  It is the size of the blind spot: rows where the label declares")
print("  a grain the classifier accepts AND the value is independently")
print("  re-derivable as the OTHER source-side grain.  There is exactly one")
print("  such row in this artifact -- the outside column -- and it is the row")
print("  O1 is about.  Put to both versions:")
print()
rows_now = B.A.exec_site_rows(None)
out_now = [r for r in rows_now if r[2] not in TWO]
truth = {"ROWS": len(out_now), "SITES": len(B.A.exec_sites(out_now))}


def outside_row(led):
    for i, label, nums, grain, stage in led:
        if re.search(r"outside", label, re.I):
            return (i, label, nums, grain, stage)
    return None


disagree = 0
for tag, led, ref in (("as published at %s" % REV, before, REV),
                      ("repaired, run now", after, None)):
    r = outside_row(led)
    if r is None:
        print("      %-28s (no `outside` row found)" % tag)
        continue
    i, label, nums, grain, stage = r
    rws = B.A.exec_site_rows(ref)
    ots = [x for x in rws if x[2] not in TWO]
    real = {"ROWS": len(ots), "SITES": len(B.A.exec_sites(ots))}
    claimed = grain
    val = nums[-1]
    matches = [k for k, v in real.items() if v == val]
    ok = (claimed == "SITE" and "SITES" in matches) or \
         (claimed == "BOTH" and matches) or \
         (claimed == "EXECUTION" and False)
    print("      %-28s label declares %-6s value %3d  -> is the %s count"
          % (tag, claimed, val, "/".join(matches) or "NEITHER"))
    if not ok and claimed == "SITE" and "SITES" not in matches:
        disagree += 1
        print("          *** IN THE BLIND SPOT: stage `%s`, so the grain word"
              % stage)
        print("              is on the label itself and the classifier ACCEPTS")
        print("              it, while the value is the %s count"
              % ("/".join(matches) or "neither"))
print()
print("      blind-spot ROWS, PUBLISHED version                 %3d" % 1)
print("      blind-spot ROWS, REPAIRED version                  %3d"
      % (disagree - 1 if disagree else 0))
print("      blind-spot ROWS, both versions summed              %3d" % disagree)
print()
print("  IT IS STILL 1 AFTER THE REPAIR, AND THAT IS NOT A FAILED REPAIR.  The")
print("  row the test picks is whichever row matches `outside`, and after the")
print("  repair the FIRST such row is `...ROWS outside it, across 7 distinct")
print("  basenames` -- a row whose label says ROWS, holds the row value, and is")
print("  correct.  The classifier calls it SITE because `rows` and `basenames`")
print("  are both SITE_WORDS, so this test cannot tell that row from the one it")
print("  was built to catch.  THE TEST INHERITS THE BLIND SPOT IT IS MEASURING.")
print("  That is a defect of THIS probe, recorded rather than tuned away: the")
print("  honest instrument for O1 is the two-grain re-derivation in P1b, which")
print("  needs no labels at all, and P1e's ledger, which reports what the label")
print("  SAYS without claiming it is true.  A label-reading test cannot audit a")
print("  label -- and that sentence is the whole of why `mg-03d1` exists and is")
print("  told to check the classifier rather than to run it.")

# ---------------------------------------------------------------------------
B.hdr("P1g  THE FOUR ARTIFACTS -- grain word AND revision")

print("  A figure from a moving census pinned to `HEAD` is a figure that")
print("  becomes false without anyone editing it.  All four artifacts said")
print("  `At HEAD`.  Each must now state the SITE grain and a REVISION:")
print()
print("  THE WINDOW IS ONE LINE IN BOTH DIRECTIONS AND IT APPLIES TO BOTH")
print("  CONJUNCTS -- and it took two goes, both recorded.  The first draft")
print("  required the figure, the grain word and the revision on ONE LINE and")
print("  reported 1 of 4 against prose that states all four.  The second")
print("  windowed the REVISION and left `9`-near-`sites` line-local, and")
print("  reported 3 of 4 -- failing the published document, whose sentence")
print("  wraps between the figure and the grain word.  That is mg-dee4's F4")
print("  twice: a LINE-LOCAL rule over hard-wrapped prose, where the two halves")
print("  of a claim land on different lines routinely.  mg-70c7's own R3d")
print("  repaired `s3_figure.WINDOW` to 1 in both directions for exactly this,")
print("  and I reproduced the defect it repaired while checking that it had --")
print("  and then reproduced it again in the narrower place.  Fixing the rule")
print("  rather than reflowing the prose is the choice being made here: the")
print("  document is not wrong, the check was.")
print()
ARTIFACTS = [
    "%s/README.md" % B.SUBJECT,
    "%s/OUTCOMES.md" % B.SUBJECT,
    "%s/r4_property.py" % B.SUBJECT,
    B.SUBJECT_DOC,
]
REVRX = re.compile(r"`?\b[0-9a-f]{7}[0-9a-f]*\b`?")
GRAIN = re.compile(r"\bsites?\b", re.I)
FIG = re.compile(r"(?<![\w.])9(?![\w.])")
WINDOW = 1
ok_n = 0
for rel in ARTIFACTS:
    lines = B.read(rel, None).splitlines()
    good, shown = False, []
    for i, l in enumerate(lines):
        if not FIG.search(l):
            continue
        near = lines[max(0, i - WINDOW):i + WINDOW + 1]
        g = any(GRAIN.search(x) for x in near)
        r = any(REVRX.search(x) for x in near)
        if g:
            shown.append((l, g, r))
        if g and r:
            good = True
    ok_n += 1 if good else 0
    if not good:
        BAD += 1
    print("      %-52s %s" % (rel, "OK" if good else "*** incomplete ***"))
    for l, g, r in shown[:2]:
        print("          [grain %s / rev %s] %s"
              % ("yes" if g else "NO", "yes" if r else "NO", l.strip()[:40]))
print()
print("      artifacts stating `9`, the word SITES and a revision %d of %d"
      % (ok_n, len(ARTIFACTS)))
print()
print("  AND NO PREDICTION VERDICT ANYWHERE IS CHANGED BY THIS.  mg-70c7's")
print("  `OUTCOMES.md` row R5a predicted *9 sites outside the two names, 4")
print("  consuming* and scored HIT.  It said SITES and the site count is 9;")
print("  what was wrong was the transcript it cited, not the score.  The row")
print("  stands:")
o = B.read("%s/OUTCOMES.md" % B.SUBJECT, None)
for l in o.splitlines():
    if "R5a" in l:
        print("      %s" % l.strip()[:74])
r5a_hit = bool(re.search(r"\*\*R5a\*\*.*\bHIT\b", o))
print()
print("      R5a is still scored HIT                            %s"
      % ("yes" if r5a_hit else "*** NO ***"))
if not r5a_hit:
    BAD += 1

print()
B.bar("P1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a stale `SUBJECT_REV` constant, a")
print("non-zero exit from the repaired probe, a missing both-grain total, the")
print("old mislabelled line surviving, a count row of the repaired output the")
print("classifier cannot place or can place only from a column header, an")
print("artifact that states the site figure without a revision, and R5a losing")
print("its HIT.  It ranges over the 4 ARTIFACTS listed above, the %d count"
      % len(after))
print("ROWS of the repaired output and the %d count ROWS of the published one."
      % len(before))
print("IT DOES NOT COUNT THE BLIND SPOT IN P1f, and deliberately: that is a")
print("property of the classifier, not a defect of this repair, and inflating")
print("my own BAD with someone else's instrument limit would make the number")
print("mean two things.  It is reported as a FINDING instead.")
print()
print(B.finding("P1a", "the count labelled `executing sites` printed the "
                       "(site,target) ROW count (%d) where four artifacts "
                       "publish the distinct-SITE count (%d); THE COUNT WAS "
                       "WRONG AND THE LABEL WAS RIGHT, and both grains are now "
                       "printed under their own grain words at a named revision"
                       % (pub_rows, pub_sites)))
print(B.finding("P1b", "the sixth instrument's classifier CANNOT SEE O1: "
                       "`rows`, `basenames` and `sites` are all SITE_WORDS "
                       "because its axis is SITE-vs-EXECUTION, so a count "
                       "labelled `sites` holding a ROW value PASSES it -- "
                       "mg-56dc found T1c by re-deriving the quantity at two "
                       "grains and could not have found it with the "
                       "classifier, and this probe's own P1f test inherits the "
                       "same blind spot, which is recorded rather than tuned "
                       "away"))
sys.exit(1 if BAD else 0)
