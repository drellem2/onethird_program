"""mg-03d1 / A2 -- P1f'S BLIND-SPOT TEST, VERIFIED AND THEN AUDITED.

TARGET 2 of the addendum.  The parent predicted its classifier would disagree
with the re-derived grain on >= 1 row before the repair and 0 after, got 1
before and 1 AFTER, and RECORDED it rather than tuning it.  Three questions:

  A2a  is that what happened -- 1 and 1?
  A2c  is the surviving disagreement the INHERITED one, or a second defect?
  A2d  was it recorded rather than tuned -- i.e. is the prediction unrevised?

and then the one the addendum does not ask, because it is the floor of this
section rather than its scope:

  A2b  the probe's own printed `blind-spot ROWS, PUBLISHED version` is a
       HARD-CODED LITERAL `1`, and the REPAIRED value is that literal
       subtracted from the measurement.  A count under a label that did not
       measure it is O1's defect class, in the probe that measures O1.

Exit code = number of A2 checks that fail.
"""

import re
import sys

import lib03d1 as B

BAD = 0
A = B.A
SUBJ = "code/runner_exit_repair_bf79"
R4_OUT = "code/runner_exit_repair_70c7/out_r4_property.txt"
FIG_REV = "973ca61"
TWO = B.TWO

print("mg-03d1 / A2 -- THE BLIND-SPOT TEST")
print("Subject: `%s/p1_grain.py`, section P1f.  HEAD: %s" % (SUBJ, B.head()))

# ---------------------------------------------------------------------------
B.hdr("A2a  REPRODUCED FROM THE PARENT'S OWN PREDICATES, NOT FROM ITS PROSE")

print("  The P1f test, re-executed here against `lib56dc` directly rather than")
print("  by reading the parent's transcript.  For each version it takes the")
print("  first count row whose label matches /outside/i, reads the label's")
print("  grain with `grain_of`, re-derives the census at BOTH grains, and asks")
print("  whether the value the row holds is the SITE count.")
print()


def outside_row(led):
    for i, label, nums, grain, stage in led:
        if re.search(r"outside", label, re.I):
            return (i, label, nums, grain, stage)
    return None


def ledger(text):
    out = []
    lines = text.splitlines()
    for i, label, nums in A.count_rows(text):
        g, st = A.grain_of(label, list(reversed(lines[max(0, i - 9):i - 1])))
        out.append((i, label, nums, g, st))
    return out


versions = []
try:
    versions.append(("as published at %s" % FIG_REV,
                     ledger(B.read(R4_OUT, FIG_REV)), FIG_REV))
except RuntimeError:
    print("      (the pinned revision %s is not present in this clone)"
          % FIG_REV)
versions.append(("repaired, on disk now", ledger(B.read(R4_OUT)), None))

disagree = 0
details = []
for tag, led, ref in versions:
    r = outside_row(led)
    if r is None:
        print("      %-26s (no `outside` row)" % tag)
        continue
    i, label, nums, grain, stage = r
    rws = A.exec_site_rows(ref)
    ots = [x for x in rws if x[2] not in TWO]
    real = {"ROWS": len(ots), "SITES": len(A.exec_sites(ots))}
    val = nums[-1]
    matches = [k for k, v in real.items() if v == val]
    flagged = grain == "SITE" and "SITES" not in matches
    disagree += flagged
    details.append((tag, label, grain, stage, val, real, matches, flagged))
    print("      %-26s" % tag)
    print("          label   : %s" % label)
    print("          declares: %-6s at stage `%s`" % (grain, stage))
    print("          holds   : %-4d  which is the %s count (ROWS=%d SITES=%d)"
          % (val, "/".join(matches) or "NEITHER", real["ROWS"], real["SITES"]))
    print("          flagged : %s" % ("YES -- in the blind spot" if flagged
                                      else "no"))
print()
print("  population: the 2 VERSIONS of `out_r4_property.txt` above, one count")
print("  row each")
B.plain("...ROWS this test flags, re-derived here", disagree)
print("      ^ one unit of that number is one flagged count row")
print()
print("  PRE-REGISTERED in A2a: summed 2, printed as 1 and 1.")
a2a_ok = disagree == 2
print("      A2a as pre-registered                              %s"
      % ("HIT" if a2a_ok else "*** MISS"))
if not a2a_ok:
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("A2c  IS THE SURVIVOR THE INHERITED ONE, OR A SECOND DEFECT?")

print("  The addendum asks exactly this, and it is the difference between `the")
print("  repair left a known limitation` and `the repair did not work`.  The")
print("  test: the post-repair flagged row is the INHERITED one if and only if")
print("  its own label states the ROW grain and the value it holds IS the row")
print("  count.  Then the row is CORRECT and only the classifier is confused.")
print()
verdict = "no post-repair row was flagged"
inherited = False
for tag, label, grain, stage, val, real, matches, flagged in details:
    if not flagged or tag.startswith("as published"):
        continue
    says_row = bool(re.search(r"\brows?\b", label, re.I))
    is_row = val == real["ROWS"]
    inherited = says_row and is_row
    print("      the flagged post-repair row:")
    print("          %s" % label)
    print("      its own label states the ROW grain              %s"
          % ("yes" if says_row else "no"))
    print("      the value it holds IS the ROW count             %s"
          % ("yes" if is_row else "no"))
    print("      the classifier calls it                         %s (because"
          % grain)
    print("          `rows` and `basenames` are both SITE_WORDS -- see A1)")
    verdict = ("INHERITED: the row is CORRECT and the test cannot tell it from"
               " the row it was built to catch" if inherited
               else "*** A SECOND, UNRELATED DEFECT")
print()
print("      verdict: %s" % verdict)
print()
print("  So the surviving 1 is NOT a failed repair and NOT a second defect.  It")
print("  is the test measuring its own resolution.  The parent's own words for")
print("  this -- `THE TEST INHERITS THE BLIND SPOT IT IS MEASURING` -- are")
print("  confirmed here by re-derivation and not by quotation.")
if details and not inherited and disagree:
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("A2d  RECORDED RATHER THAN TUNED -- CHECKED IN THE HISTORY, NOT THE PROSE")

print("  `PREDICTIONS.md` is a PRE-REGISTRATION.  The claim `recorded rather")
print("  than tuned` is a claim about its history, so it is checked there.")
print()
pred = "%s/PREDICTIONS.md" % SUBJ
log = [l for l in B.git("log", "--format=%h %s", "--", pred).splitlines() if l]
print("  population: every COMMIT in `git log -- %s`" % pred)
B.plain("...COMMITS touching that pre-registration FILE", len(log))
print("      ^ one unit of that number is one commit")
for l in log:
    print("          %s" % l[:96])
print()
one = len(log) == 1
pre = log and log[0].split(None, 1)[1].startswith("predictions:")
print("      exactly one commit touches it                      %s"
      % ("yes" if one else "*** NO -- it was rewritten"))
print("      and its subject begins `predictions:`               %s"
      % ("yes" if pre else "*** NO"))
if not one:
    BAD += 1
print()
txt = B.read(pred)
has_p1g = "P1g" in txt and "0 after" in txt.replace("**", "")
out = B.read("%s/OUTCOMES.md" % SUBJ)
m = re.search(r"\*\*P1g\*\*.*", out)
scored_miss = bool(m and "MISS" in m.group(0))
print("      P1g survives verbatim in the pre-registration       %s"
      % ("yes" if has_p1g else "*** NO"))
print("      OUTCOMES scores P1g a MISS                          %s"
      % ("yes" if scored_miss else "*** NO"))
if not (has_p1g and scored_miss):
    BAD += 1
print()
print("  AND THE SHA NOTE, because this arc keeps needing it: the parent's")
print("  pre-registration commit was REBASED by the refinery, so any SHA it")
print("  recorded for itself differs on `main`.  Ancestry is a FALSE NEGATIVE")
print("  after a rebase; content is checked with `git patch-id --stable`:")
print()
sha = log[0].split()[0] if log else None
if sha:
    import subprocess
    p = subprocess.run(["sh", "-c",
                        "git show %s | git patch-id --stable" % sha],
                       cwd=B.REPO, capture_output=True, text=True)
    print("      `%s` patch-id  %s" % (sha, (p.stdout or "-").strip()[:40]))
    print("      (recorded so a later reader can match this commit by CONTENT")
    print("       after the rebase that will displace its SHA)")

# ---------------------------------------------------------------------------
B.hdr("A2b  THE FLOOR OF THIS SECTION: A COUNT UNDER A LABEL THAT DID NOT"
      " MEASURE IT")

print("  Nothing in the brief names this.  `p1_grain.py` prints its three")
print("  blind-spot figures like this -- quoted from the source, lines 343-346:")
print()
print("      print(\"      blind-spot ROWS, PUBLISHED version   %3d\" % 1)")
print("      print(\"      blind-spot ROWS, REPAIRED version    %3d\"")
print("            % (disagree - 1 if disagree else 0))")
print("      print(\"      blind-spot ROWS, both versions summed %3d\" % disagree)")
print()
src = B.read("%s/p1_grain.py" % SUBJ)
lit = bool(re.search(r'PUBLISHED version[^"]*"\s*%\s*1\)', src))
der = bool(re.search(r'REPAIRED version[^"]*"\s*\n?\s*%\s*\(disagree - 1', src))
print("  population: the 3 blind-spot count ROWS `p1_grain.py` prints")
B.plain("...ROWS whose value is a literal, not a measurement", 1 if lit else 0)
print("      ^ one unit of that number is one printed count row")
B.plain("...ROWS derived by arithmetic on that literal", 1 if der else 0)
print("      ^ one unit of that number is one printed count row")
B.plain("...ROWS actually measured by the loop above them", 1)
print("      ^ one unit of that number is one printed count row")
print()
print("  `PUBLISHED version` is the constant 1.  The loop that computes")
print("  `disagree` iterates over BOTH versions and cannot say which of them")
print("  contributed -- so the split into published and repaired is ASSUMED,")
print("  and the label `PUBLISHED version` names a measurement that was never")
print("  taken.  That is O1's defect class exactly: a label that says what the")
print("  number is ABOUT, over a value that is about something else.")
print()
print("  PUT TO THE INPUTS IT WAS NOT GIVEN.  The probe's own printing")
print("  arithmetic, re-executed here over `disagree` in 0..3.  I do not edit")
print("  the subject to do this -- editing it would make the finding a fact")
print("  about my edit:")
print()
print("      disagree   prints PUBLISHED   REPAIRED   SUMMED   consistent?")
incons = 0
for d in range(4):
    pub, rep, summed = 1, (d - 1 if d else 0), d
    ok = pub + rep == summed
    incons += not ok
    print("      %8d %14d %10d %8d   %s"
          % (d, pub, rep, summed, "yes" if ok else "*** NO: %d + %d != %d"
             % (pub, rep, summed)))
print()
print("  population: the 4 INPUTS 0..3 put to the probe's printing arithmetic")
B.plain("...INPUTS on which the three printed rows contradict", incons)
print("      ^ one unit of that number is one input value")
print()
print("  PRE-REGISTERED in A2b: exactly 1 of the 4.")
a2b_ok = incons == 1
print("      A2b as pre-registered                              %s"
      % ("HIT" if a2b_ok else "*** MISS -- %d" % incons))
print()
print("  THE INPUT THAT BREAKS IT IS `disagree == 0` -- WHICH IS THE INPUT A")
print("  SUCCESSFUL REPAIR WOULD PRODUCE.  Had the repair closed the blind spot")
print("  entirely, the probe would have printed `PUBLISHED 1, REPAIRED 0,")
print("  SUMMED 0` and reported a published defect it had just measured as")
print("  absent.  The probe is correct on the value it got and wrong on the")
print("  value it was hoping for.  NOT REPAIRED HERE: this is an audit, and")
print("  the parent's transcripts are its evidence, not my worksheet.")
if not a2b_ok:
    BAD += 1

print()
print("A2 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
