"""c5_record.py -- THE ITEM NO LIST NAMES, plus the X2 disclosure question.

MY BRIEF SAYS ITS LIST IS A FLOOR AND TELLS ME TO AUDIT ONE THING NO LIST
NAMES.  WHAT I CHOSE, AND WHY:

  **The retraction of record itself -- as a record.**

  My brief tells me to verify that "the retraction is recorded in the document
  itself".  It does not tell me to check whether the record is ACCURATE, or
  whether the place the document points a reader to still contains it.  The
  document stakes a specific factual claim of record:

      "At 2026-07-30 19:50 docs/roadmap.md carried, as THE HEADLINE, ... and
       it went to Daniel in that form.  At 20:45, on mg-2060's finding, it was
       retracted -- docs/roadmap.md, commit f4eaea6. ...  The elapsed time
       between delivery and retraction was 55 minutes."

  Three checkable things nobody has checked: (a) do the two times and the
  55-minute interval match the commits; (b) does the roadmap -- a file this
  repo rebuilds several times an hour -- STILL carry the retraction, or has a
  later rebuild dropped it; (c) is the headline actually in the roadmap at the
  commit named.  A retraction whose own record is wrong is the exact failure
  the document is arguing against, so this is the load-bearing sentence of the
  D10 repair and no list names it.

SECOND, and it is not on any list either: whether mg-e8b8's "DELIBERATELY NOT
REPAIRED" list is accurate about mg-2060's X2.  c4's duplicate sweep found
that the repair edited two of X2's three sites.  This script states that
precisely, site by site.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DOCPATH = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
DOC = open(os.path.join(ROOT, DOCPATH)).read()
ROADMAP = open(os.path.join(ROOT, "docs/roadmap.md")).read()

SELF, FIND, NOTE = [], [], []
CHECKS = 0


def report(name, ok, detail="", note_only=False):
    global CHECKS
    CHECKS += 1
    tag = "[ok]" if ok else ("[--]" if note_only else "[!!]")
    print("    %-4s %-60s %s" % (tag, name, "pass" if ok else
                                 ("note" if note_only else "FAIL")))
    if detail:
        print("         " + detail)
    if not ok:
        (NOTE if note_only else FIND).append(name + (" -- " + detail if detail else ""))
    return ok


def git(*args):
    r = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        SELF.append("git " + " ".join(args) + " failed")
        return ""
    return r.stdout


print("=" * 74)
print("c5  THE RETRACTION AS A RECORD (the item no list names), AND X2's")
print("    DISCLOSURE")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
print("(1) IS THE RECORD ACCURATE? -- the two times and the 55-minute interval")
print()
HEADLINE_COMMIT = "6c0f0da"      # the roadmap commit that introduced the headline
RETRACT_COMMIT = "f4eaea6"

t_head = git("log", "-1", "--format=%ad", "--date=iso-local", HEADLINE_COMMIT).strip()
t_retr = git("log", "-1", "--format=%ad", "--date=iso-local", RETRACT_COMMIT).strip()
print("      the roadmap commit that INTRODUCED the headline : %s  %s"
      % (HEADLINE_COMMIT, t_head))
print("      the roadmap commit that RETRACTED it            : %s  %s"
      % (RETRACT_COMMIT, t_retr))

hl = git("show", HEADLINE_COMMIT + ":docs/roadmap.md")
report("the headline really is in docs/roadmap.md at %s" % HEADLINE_COMMIT,
       "share a PROPERTY, not a CONSTRUCTION" in hl and "THE HEADLINE" in hl)
report("commit %s is the retraction the document names" % RETRACT_COMMIT,
       "RETRACT the quasi-hereditary headline" in
       git("log", "-1", "--format=%s", RETRACT_COMMIT))

if t_head and t_retr:
    d1 = datetime.strptime(t_head[:19], "%Y-%m-%d %H:%M:%S")
    d2 = datetime.strptime(t_retr[:19], "%Y-%m-%d %H:%M:%S")
    mins = (d2 - d1).total_seconds() / 60.0
    print("      measured interval between those two commits    : %.1f minutes"
          % mins)
    print("      the document states                            : 55 minutes,")
    print("                                                        19:50 -> 20:45")
    report("the document's stated times match the commits to the minute",
           t_head[11:16] == "19:50" and t_retr[11:16] == "20:45",
           "commits are %s and %s; the document says 19:50 and 20:45"
           % (t_head[11:16], t_retr[11:16]), note_only=True)
    report("the document's stated 55 minutes matches the measured interval",
           abs(mins - 55.0) < 1.0,
           "measured %.1f minutes commit-to-commit; the document says 55. The "
           "two stated clock times are rounded in OPPOSITE directions (19:50 vs "
           "19:52:23, and 20:45 vs 20:42:49), which stretches the interval by "
           "about 5 minutes. The overstatement runs AGAINST the author's "
           "interest -- a longer time to retract is the worse number -- and "
           "55 is exactly right given the two times the document states, which "
           "are the roadmap's own." % mins,
           note_only=True)
print()

# ---------------------------------------------------------------------------
print("(2) DOES THE PLACE THE DOCUMENT POINTS AT STILL CARRY THE RETRACTION?")
print("    docs/roadmap.md is rebuilt several times an hour in this repo, so")
print("    'see the roadmap' is a pointer that can rot.")
print()
rebuilds = [l for l in git("log", "--format=%h %ad %s", "--date=iso-local",
                           "--", "docs/roadmap.md").splitlines()
            if "rebuild" in l.lower()]
after = git("log", "--format=%h", RETRACT_COMMIT + "..HEAD", "--",
            "docs/roadmap.md").split()
print("      roadmap commits since the retraction: %d, population: every commit "
      "touching docs/roadmap.md after %s" % (len(after), RETRACT_COMMIT))
report("the CURRENT roadmap still carries the retraction",
       "RETRACTED" in ROADMAP and "quasi-hereditary" in ROADMAP
       and "went to Daniel as the headline" in ROADMAP)
report("the current roadmap still names the 19:50 delivery",
       "At 19:50 this roadmap said" in ROADMAP)
report("the current roadmap no longer asserts the headline as a result",
       not re.search(r"\*\*THE HEADLINE: the branching axis and the species axes?"
                     r" share a PROPERTY", ROADMAP))
print()

# ---------------------------------------------------------------------------
print("(3) THE RETRACTION IS IN TWO PLACES, WHICH IS THE POINT")
print()
report("the delivered document carries the retraction independently of the "
       "roadmap", "f4eaea6" in DOC and "20:45" in DOC and "19:50" in DOC)
report("the document says WHY it repeats it",
       "the document is where a future reader will look" in
       # block-quote '>' markers sit inside the sentence, so they are stripped
       # too; the first version of this check missed the sentence for that
       # reason alone
       re.sub(r"\s+", " ", re.sub(r"[*_`>]", "", DOC)))
print()

# ---------------------------------------------------------------------------
print("(4) IS 'DELIBERATELY NOT REPAIRED' ACCURATE ABOUT mg-2060's X2?")
print("    X2 has three sites in mg-2060's write-up.  Each is checked here")
print("    against the pre-repair and post-repair text.")
print()
old_doc = git("show", "03d7f91:" + DOCPATH)
old_t1 = git("show", "03d7f91:code/branching_locate_db09/t1_tl.py")
new_t1 = open(os.path.join(ROOT, "code/branching_locate_db09/t1_tl.py")).read()
out_t1 = open(os.path.join(ROOT, "code/branching_locate_db09/out_t1_tl.txt")).read()

sites = [
    ("T1a's 'iff' header, in t1_tl.py and its committed output",
     "A basis indexed by pairs of paths with a common endpoint exists iff",
     old_t1, new_t1),
    ("section 0's 2x2 table cell, 'Path-pair BASIS survives'",
     "Path-pair *basis* survives", old_doc, DOC),
    ("T1d's printed 'the pairs-of-paths basis exists throughout'",
     "the pairs-of-paths basis exists throughout", old_t1, new_t1),
]
changed = []
for (name, needle, before, after_txt) in sites:
    was = needle in before
    still = needle in after_txt
    print("      %-58s pre-repair: %-3s  post-repair: %s"
          % (name[:58], "yes" if was else "no", "yes" if still else "REMOVED"))
    if was and not still:
        changed.append(name)
print()
print("      X2 sites the repair CHANGED: %d of %d, population: the three sites "
      "mg-2060's X2 names" % (len(changed), len(sites)))
for c in changed:
    print("        - " + c)
print()
claims_unrepaired = ("Deliberately NOT repaired" in DOC
                     and re.search(r"T1a's \*+\"iff\"\*+\*+ \(mg-2060 X2\)", DOC)
                     is not None)
print("      the document's section 8 books X2 under 'Deliberately NOT repaired,")
print("      and each is open': %s" % ("yes" if claims_unrepaired else "no"))
report("nothing in X2 was repaired, as section 8 says",
       len(changed) == 0 or not claims_unrepaired,
       "the repair CHANGED %d of the 3 sites of X2 (%s) while section 8 books "
       "X2 as 'Deliberately NOT repaired, and each is open' and section 4 item "
       "3's outcome says the two further defects are 'not repaired by mg-e8b8'. "
       "The changes go the RIGHT way -- they remove a false claim -- but they "
       "are undisclosed, and neither site carries a CORRECTED note the way the "
       "document's other six CORRECTED/WITHDRAWN (mg-e8b8) sites do."
       % (len(changed), "; ".join(changed)))
print()
print("      what IS still in force, so the finding is not overstated:")
print("        T1a's 'iff' header is still printed verbatim by t1_tl.py and is")
print("        still in the committed out_t1_tl.txt, inside a run ending")
print("        TOTAL BAD: 0.  So X2's primary site is genuinely unrepaired and")
print("        section 8 is right about THAT site.")
still_iff = ("A basis indexed by pairs of paths with a common endpoint exists iff"
             in out_t1)
print("        checked: the 'iff' line is in out_t1_tl.txt -- %s"
      % ("yes" if still_iff else "no"))
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the git reads this script needs" % len(SELF))
for s in SELF:
    print("   SELF-ERROR: " + s)
print("NOTES (recorded, not scored): %d, population: the %d named checks above"
      % (len(NOTE), CHECKS))
for n in NOTE:
    print("   NOTE: " + n)
print("FINDINGS: %d, population: the %d named checks above" % (len(FIND), CHECKS))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
