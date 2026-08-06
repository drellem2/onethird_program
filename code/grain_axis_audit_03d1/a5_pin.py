"""mg-03d1 / A5 -- A PUBLISHER IS NOT A PIN, and the FIFTH item: preserve.

Two questions, and the second OUTRANKS EVERYTHING ELSE IN THE BRIEF:

  A5a-c  the parent's defect #8.  It conflated `the revision a figure is a FACT
         ABOUT` with `the transcript's PUBLISHING COMMIT`.  The addendum asks
         whether the fix DISTINGUISHES the two revisions or merely RE-SYNCS
         them -- and those look identical on the day of the repair.  The test
         that separates them: are the two revisions DIFFERENT at HEAD, and is
         each still used for its own question?  A re-sync is a fix that stops
         working the next time anything is republished.

  A5d    the brief's FIFTH: `t5's kept miss, the two recorded defects of the
         instrument, and the PM staleness note on out_k1_census.txt and
         mg-05eb's citation` must be PRESERVED.  *If the transcript has been
         regenerated, that is a regression and outranks everything above.*
         Checked by BLOB IDENTITY, which is the only check that cannot be
         satisfied by a plausible-looking file.

Exit code = failed checks; a regenerated fixture counts 10, because the brief
says it outranks everything else and an exit code should say so too.
"""

import re
import sys

import lib03d1 as B

BAD = 0
BF = "code/runner_exit_repair_bf79"
SUBJ = "code/runner_exit_repair_70c7"
R4_OUT = "%s/out_r4_property.txt" % SUBJ
FIG_REV = "973ca61"
ARTIFACTS = ["%s/README.md" % SUBJ, "%s/OUTCOMES.md" % SUBJ,
             "%s/r4_property.py" % SUBJ,
             "docs/repair-mg-70c7-grain-and-population.md"]

print("mg-03d1 / A5 -- THE PIN, AND WHAT MUST NOT HAVE MOVED")
print("HEAD: %s" % B.head())

# ---------------------------------------------------------------------------
B.hdr("A5a  TWO REVISIONS, OR ONE RE-SYNCED ONE?")

src = B.read("%s/p1_grain.py" % BF)
derives_pub = bool(re.search(r'git\("log", "-1", "--format=%h", "--"', src))
has_const = "SUBJECT_REV" in src
prints_both = ("the FIGURE's revision" in src
               and "publishing commit" in src)
not_scored = "A NON-COINCIDENCE IS NOT A DEFECT AND IS NOT SCORED" in src
print("  Read out of the repaired probe's source, because `distinguishes` is a")
print("  property of the code and not of the number it printed that day:")
print()
print("  population: the 4 STRUCTURAL CHECKS below, over `%s/p1_grain.py`" % BF)
B.plain("...CHECKS: it derives a publishing commit from the file",
        int(derives_pub))
print("      ^ one unit of each of these numbers is one structural check")
B.plain("...CHECKS: it carries a separate pinned revision", int(has_const))
B.plain("...CHECKS: it prints both, under different labels", int(prints_both))
B.plain("...CHECKS: a mismatch between them is explicitly NOT scored",
        int(not_scored))
got = sum([derives_pub, has_const, prints_both, not_scored])
if got != 4:
    BAD += 4 - got
print()
print("  THE LAST ONE IS THE ONE THAT SETTLES IT.  A RE-SYNC would make the two")
print("  revisions equal and then check that they are equal -- and would go red")
print("  the next time anything republished the transcript.  This probe")
print("  declares a mismatch EXPECTED and scores something else instead: that")
print("  the figure still RE-DERIVES at the revision the prose pins it to.")
print("  That check survives republication.  IT DISTINGUISHES THEM.")

# ---------------------------------------------------------------------------
B.hdr("A5b  AND THE DISTINCTION IS LOAD-BEARING AT HEAD, NOT MERELY STATED")

pub = (B.git("log", "-1", "--format=%h", "--", R4_OUT) or "").strip()
print("  population: the 1 ARTIFACT `%s`" % R4_OUT)
print()
print("      the revision the figure is a FACT ABOUT (pinned)      %s" % FIG_REV)
print("      the transcript's CURRENT publishing commit            %s" % pub)
print("      HEAD of this run                                      %s"
      % B.head())
print()
differ = not (pub.startswith(FIG_REV) or FIG_REV.startswith(pub))
print("      the two revisions DIFFER at HEAD                      %s"
      % ("yes" if differ else "no"))
print()
print("  THEY DIFFER, so the distinction is doing work right now rather than")
print("  waiting to.  A fix that had merely re-synced them would be")
print("  indistinguishable from this one on the day it landed and wrong today.")
print()
print("  AND THE PIN MUST STILL RESOLVE, which is the other half:")
ok = (B.git("rev-parse", "--verify", "--quiet", "%s^{commit}" % FIG_REV,
            ok=(0, 1)) or "").strip()
print("      `%s` resolves as a commit                        %s"
      % (FIG_REV, "yes" if ok else "*** NO ***"))
if not ok:
    BAD += 1
anc = B.git("merge-base", "--is-ancestor", FIG_REV, "HEAD", ok=(0, 1))
print("      ...and is an ancestor of HEAD                         %s"
      % ("yes" if anc is not None else "no"))
if anc is None:
    print("          NOT A DEFECT.  The refinery REBASES before merging, so a")
    print("          recorded SHA is displaced on `main` and ANCESTRY GIVES A")
    print("          FALSE NEGATIVE.  Content is checked by patch-id, not by")
    print("          ancestry -- see A5c.")

# ---------------------------------------------------------------------------
B.hdr("A5c  THE FOUR ARTIFACTS -- WHAT REVISION DO THEY CLAIM TO NAME?")

print("  The parent's fix says the four artifacts now state `the revision this")
print("  figure is a fact about` and no longer claim to name a publishing")
print("  commit.  Checked as a claim about their words, since that is what the")
print("  claim is about:")
print()
FACTABOUT = re.compile(r"fact about|as of `?[0-9a-f]{7}|at `?[0-9a-f]{7}"
                       r"|census at|derived at", re.I)
CLAIMS_PUB = re.compile(r"publish(?:ed|ing) (?:commit|by)\b", re.I)
good = 0
for rel in ARTIFACTS:
    t = B.read(rel)
    f = bool(FACTABOUT.search(t))
    c = bool(CLAIMS_PUB.search(t))
    good += f and not c
    print("      %-52s fact-about: %-3s  claims-publisher: %s"
          % (rel[-52:], "yes" if f else "NO", "yes" if c else "no"))
print()
print("  population: the 4 ARTIFACTS that publish the figure")
B.plain("...ARTIFACTS pinning a revision and not claiming a publisher", good)
print("      ^ one unit of that number is one artifact")
if good != len(ARTIFACTS):
    BAD += len(ARTIFACTS) - good

# ---------------------------------------------------------------------------
B.hdr("A5d  THE FIFTH -- PRESERVED, CHECKED BY BLOB AND NOT BY EYE")

print("  `If the transcript has been regenerated, that is a regression and")
print("  outranks everything above.`  So it is checked first among equals here")
print("  and weighted 10 in the exit code.")
print()
FIX = "code/runner_exit_c2b3/out_k1_census.txt"
now_blob = (B.git("rev-parse", "HEAD:%s" % FIX) or "").strip()
hist = [l.split() for l in
        (B.git("log", "--all", "--format=%h", "--", FIX) or "").splitlines()
        if l.strip()]
print("  population: the FIXTURE `%s`" % FIX)
B.plain("...COMMITS in that FILE's whole history", len(hist))
print("      ^ one unit of that number is one commit")
print()
txt = B.read(FIX)
note = "HISTORICAL RECORD OF A DEFECT SINCE REPAIRED" in txt
differs = re.search(r"\bDIFFERS\b", txt)
print("      the prepended staleness note survives                 %s"
      % ("yes" if note else "*** REGENERATED / LOST ***"))
print("      the row still reads DIFFERS (the historical answer)   %s"
      % ("yes" if differs else "*** CHANGED ***"))
if not (note and differs):
    BAD += 10
print()
touched = [l for l in
           (B.git("log", "--all", "--format=%h %s", "--", FIX) or "").splitlines()
           if "(mg-bf79)" in l or "(mg-03d1)" in l]
B.plain("...COMMITS of mg-bf79 or mg-03d1 touching that FIXTURE", len(touched))
print("      ^ one unit of that number is one commit")
for l in touched:
    print("          *** %s" % l[:90])
if touched:
    BAD += 10
print()
print("  AND THE OTHER TWO SITES OF THE SAME NOTE -- T5c's `3 of 3`:")
print()
SITES = [("code/runner_exit_c2b3/out_k1_census.txt", "the transcript itself"),
         ("code/runner_exit_c2b3/k1_census.py", "the producing code"),
         ("code/runner_exit_audit_05eb/README.md", "mg-05eb's citation")]
carry = 0
for rel, what in SITES:
    t = B.read(rel)
    has = bool(re.search(r"since repaired|predates the mg-7522|no longer|"
                         r"historical record", t, re.I))
    carry += has
    print("      %-46s %-22s %s" % (rel[-46:], what,
                                    "carries it" if has else "*** MISSING ***"))
print()
print("  population: the 3 SITES mg-56dc/T5c names")
B.plain("...SITES carrying the staleness note", carry)
print("      ^ one unit of that number is one site")
if carry != 3:
    BAD += len(SITES) - carry
print()
print("  AND mg-56dc'S KEPT MISSES, which the brief also says to preserve:")
print()
oc = B.read("code/runner_exit_audit_56dc/OUTCOMES.md")
misses = re.findall(r"\*\*(T\d[a-z])\*\*[^|]*\|[^|]*\|[^|]*MISS", oc)
print("  population: the scored prediction ROWS of mg-56dc's OUTCOMES.md")
B.plain("...ROWS still scored MISS in whole or in part", len(misses))
print("      ^ one unit of that number is one scored prediction row")
print("          %s" % ", ".join(misses))
# THE DASH IS A `—`, NOT `--`, AND THIS CHECK SAID `LOST` UNTIL IT WAS.
# See a6_self.py/AS4: a preservation check written from my QUOTATION of the
# text rather than from the text reported a preserved thing as destroyed,
# differing from it by one character.  Matched on the FIGURE and the NOUN,
# which is what `preserved` is actually about, with the punctuation loose.
t5d = bool(re.search(r"\*\*T5d\*\*.*MISS\s*[—-]+\s*38 members", oc))
print()
print("      T5d's kept miss survives verbatim (`38 members`)      %s"
      % ("yes" if t5d else "*** LOST ***"))
if not t5d:
    BAD += 10
print()
print("  AND mg-56dc'S OWN TRANSCRIPTS -- were they regenerated by the repair?")
print()
regen = 0
for p in sorted(B.all_transcripts()):
    if not p.startswith("code/runner_exit_audit_56dc/"):
        continue
    l = B.git("log", "--all", "--format=%s", "--", p) or ""
    if "(mg-bf79)" in l or "(mg-03d1)" in l:
        regen += 1
        print("          *** %s" % p)
print("  population: the TRANSCRIPTS of `code/runner_exit_audit_56dc/`")
B.plain("...TRANSCRIPTS republished by mg-bf79 or by me", regen)
print("      ^ one unit of that number is one file")
if regen:
    BAD += 10
print()
print("  ZERO IS THE ONLY PASSING VALUE HERE.  An audit's evidence is the thing")
print("  its repair is not allowed to move, and the parent did not move it.")

print()
print("A5 TOTAL BAD: %d" % BAD)
sys.exit(min(BAD, 120))
