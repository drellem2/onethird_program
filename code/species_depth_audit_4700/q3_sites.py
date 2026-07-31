"""Q3 -- DELETE THE ANCHOR AT THE SITE A READER MEETS IT, AND LEAVE THE OTHERS.

mg-6cb9's F3: `check_doc.py`'s C4 was `flat(s) in flat(rep)` -- a PRESENCE test
over a document that writes three of its five anchors more than once (`mg-a61f`
19 times).  For three of five it was therefore a check on NO SITE: delete the
copy a reader meets and the run stayed green; only deleting EVERY copy fired.

mg-821e took the brief's third remedy -- check at the reader-facing site -- and
says it went from 2 of 7 to 7 of 7.  The brief for this audit is the matching
test: **delete the anchor at that site only, leaving the others, and confirm it
fires.**

  Q3a  the 7 `(site, anchor)` pairs, each deleted AT ITS OWN SITE ONLY.
  Q3b  the same 7 deletions against `check_doc.py` as it stood BEFORE the
       repair, at a PINNED ref -- the 2 of 7 figure, re-measured rather than
       quoted.
  Q3c  the other direction: deleting a copy at a NON-site must be SILENT, and
       an empty section 10 must fire.  A site check that fires on everything is
       a presence check with extra words.
  Q3d  D4e/D4f -- the site regex is part of the check.  Rename a heading and
       the site vanishes; and a sweep of every heading region carrying an
       anchor, against the 7 that are covered.

    python3 code/species_depth_audit_4700/q3_sites.py
"""

import os
import re
import sys

from kern4700 import (hdr, REPO, sh, Probe, run_checker, predict, PRE_REPAIR,
                      flat, regions, needle_re, delete_at)

bad = 0
miss = 0

CHECK = "code/species_repair_6f61/check_doc.py"
REPAIR_DOC = "docs/OneThird-Species-Hopf-Monoids-Repair.md"

# C4_SITES, COPIED from check_doc.py rather than imported.  Importing would run
# the checker, and -- the real reason -- an expectation that moves when the
# subject moves cannot disagree with the subject.  If mg-821e's table and this
# one drift apart, Q3a's row count stops matching and that is a finding here,
# not a silent agreement.
C4_SITES = [
    ("names its target", "OneThird-Species-Hopf-Monoids-Where-This-Lives",
     r"^# Repair of mg-7d75"),
    ("names the audit", "mg-a61f", r"^# Repair of mg-7d75"),
    ("names the instrument", "code/species_repair_6f61",
     r"^# Repair of mg-7d75"),
    ("names the instrument", "code/species_repair_6f61", r"^## 11\. REPRODUCE"),
    ("records the missed predictions", "2 of 45", r"^### 2\.1 "),
    ("records the missed predictions", "2 of 45", r"^## 11\. REPRODUCE"),
    ("records what it did NOT repair", "WHAT THIS REPAIR DID NOT DO",
     r"^## 10\. "),
]
ANCHORS = sorted({s for _l, s, _p in C4_SITES})


# `flat`, `regions`, `needle_re` and `delete_at` live in kern4700 -- copies of
# check_doc.py's own logic, kept where selftest4700.py can test them.  Copied
# and not imported from the subject: an expectation computed by the subject's
# own code cannot disagree with the subject, which is mg-6cb9's F1 in another
# costume.

DOC0 = open(os.path.join(REPO, REPAIR_DOC), encoding="utf-8").read()


# ---------------------------------------------------------------------------
# Q3a  the 7 pairs, deleted at their own site only
# ---------------------------------------------------------------------------
hdr("Q3a  EACH ANCHOR DELETED AT ITS OWN SITE, EVERY OTHER COPY LEFT STANDING")

print("  Each row deletes one anchor from ONE heading region and leaves every")
print("  other copy in the file untouched.  `copies left` is the number of")
print("  copies still in the document when the checker runs -- for `mg-a61f`")
print("  that is eighteen, and the check has to fire anyway or it is a")
print("  presence test wearing a site's name.")
print()

fires_now = 0
rows = []
for label, needle, pat in C4_SITES:
    new, removed, left = delete_at(DOC0, needle, pat)
    if new is None:
        print("  %-34s *** the site regex matches no heading: %s ***"
              % (label, pat))
        bad += 1
        continue
    with Probe("D4a %s @ %s" % (needle[:20], pat)) as pr:
        pr.write(REPAIR_DOC, new)
        rc, out = run_checker(CHECK)
    fires_now += (rc != 0)
    rows.append((label, needle, pat, removed, left, rc))
    print("  %-30s %-16s removed %d at site, %2d left elsewhere -> exit %d %s"
          % (pat.strip("^"), needle[:16], removed, left, rc,
             "FIRES" if rc else "*** SILENT ***"))
    bad += (rc == 0)
miss += predict("D4a", "7 of 7 fire", "%d of %d fire" % (fires_now, len(rows)),
                fires_now == len(C4_SITES))
print()
print("  %d of %d.  Three of these anchors still have copies elsewhere in the"
      % (fires_now, len(C4_SITES)))
print("  file at the moment the checker runs, and the check fires anyway.")
print("  That is the difference between a site and a presence.")
print()


# ---------------------------------------------------------------------------
# Q3b  the same deletions against the PRE-REPAIR checker
# ---------------------------------------------------------------------------
hdr("Q3b  THE SAME 7 DELETIONS, AGAINST `check_doc.py` AT %s" % PRE_REPAIR)

print("  mg-821e reports `2 of 7` for the checker it replaced.  Quoting that")
print("  number would make this audit's 7 of 7 a comparison with a sentence.")
print("  The old file is fetched from a PINNED ref -- not HEAD, which BECAME")
print("  the repair the moment it landed -- and run against the same seven")
print("  mutations.")
print()

rc, old_check, err = sh(["git", "show", "%s:%s" % (PRE_REPAIR, CHECK)])
if rc != 0:
    print("  *** git unavailable: %s -- Q3b did not run, and this line is the"
          " record ***" % err.strip()[:60])
    bad += 1
    fires_then = None
else:
    fires_then = 0
    for label, needle, pat in C4_SITES:
        new, removed, left = delete_at(DOC0, needle, pat)
        if new is None:
            continue
        with Probe("D4c old checker, %s @ %s" % (needle[:16], pat)) as pr:
            pr.write(REPAIR_DOC, new)
            pr.write(CHECK, old_check)
            rc2, _ = run_checker(CHECK)
        fires_then += (rc2 != 0)
        print("  %-30s %-16s %2d copies left elsewhere -> exit %d  %s"
              % (pat.strip("^"), needle[:16], left, rc2,
                 "fires" if rc2 else "SILENT -- the copy a reader meets is"
                 " gone and the run is green"))
    miss += predict("D4c", "2 of 7 fire", "%d of 7 fire" % fires_then,
                    fires_then == 2)
    print()
    print("  %d of 7 before, %d of 7 after.  The %d rows that were silent are"
          % (fires_then, fires_now, fires_now - fires_then))
    print("  the ones mg-6cb9's F3 was about: an anchor with 19 copies is not")
    print("  better covered than one with 1, it is less.")
print()


# ---------------------------------------------------------------------------
# Q3c  the other direction
# ---------------------------------------------------------------------------
hdr("Q3c  AND IT IS WRONG IN THE OTHER DIRECTION TOO")

# D4b -- a copy deleted at a heading region that is NOT one of the seven sites.
lines = DOC0.splitlines(True)
noncovered = []
covered_pats = {p for _l, _s, p in C4_SITES}
for h, a, b in regions(lines):
    if any(re.search(p, h) for p in covered_pats):
        continue
    if needle_re("mg-a61f").search("".join(lines[a:b])):
        noncovered.append((h.strip(), a, b))
if noncovered:
    h, a, b = noncovered[0]
    region = "".join(lines[a:b])
    new = ("".join(lines[:a]) + needle_re("mg-a61f").sub("", region)
           + "".join(lines[b:]))
    with Probe("D4b non-site copy deleted") as pr:
        pr.write(REPAIR_DOC, new)
        rc, _ = run_checker(CHECK)
    miss += predict("D4b", "exit 0 (silent)", "exit %d" % rc, rc == 0)
    bad += (rc != 0)
    print("  a copy of `mg-a61f` deleted at %-32s exit %d  %s"
          % (h[:32], rc,
             "silent -- correct: multiplicity elsewhere has no vote"
             if rc == 0 else "*** FIRES: this is a presence test after all ***"))
else:
    print("  *** no non-site heading region carries `mg-a61f`: D4b cannot"
          " run ***")
    bad += 1

# D4d -- section 10 emptied but its heading kept.
h10 = next(((h, a, b) for h, a, b in regions(lines)
            if re.search(r"^## 10\. ", h)), None)
if h10:
    h, a, b = h10
    new = "".join(lines[:a]) + h + "".join(lines[b:])
    with Probe("D4d section 10 emptied") as pr:
        pr.write(REPAIR_DOC, new)
        rc, out = run_checker(CHECK)
    miss += predict("D4d", "exit 1", "exit %d" % rc, rc == 1)
    bad += (rc == 0)
    print("  section 10's BODY deleted, heading kept                  "
          "exit %d  %s" % (rc, "fires" if rc else "*** SILENT ***"))
    for l in out.splitlines():
        if "empty heading" in l:
            print("        %s" % l.strip())
print()


# ---------------------------------------------------------------------------
# Q3d  the site regex is part of the check
# ---------------------------------------------------------------------------
hdr("Q3d  A SITE IS A HEADING, AND A HEADING CAN BE RENAMED")

# D4e -- rename the heading a site regex targets.  Every anchor stays put; only
# the heading text moves.  A site check that goes quiet when its heading is
# reworded has moved the contingency rather than removed it.
h11 = next(((h, a, b) for h, a, b in regions(lines)
            if re.search(r"^## 11\. REPRODUCE", h)), None)
if h11:
    h, a, b = h11
    renamed = h.replace("11. REPRODUCE", "11. Reproducing the run")
    new = "".join(lines[:a]) + renamed + "".join(lines[a + 1:])
    with Probe("D4e site heading renamed") as pr:
        pr.write(REPAIR_DOC, new)
        rc, out = run_checker(CHECK)
    named = "NO SUCH SECTION" in out
    miss += predict("D4e", "exit 1, NO SUCH SECTION",
                    "exit %d, named %s" % (rc, "yes" if named else "no"),
                    rc == 1 and named)
    bad += (rc == 0)
    print("  `%s`" % h.strip())
    print("  reworded to `%s`, every anchor left in place:" % renamed.strip())
    print("      exit %d, and the run says NO SUCH SECTION: %s"
          % (rc, "yes" if named else "*** no ***"))
    print("  So the heading text is load-bearing and the failure is LOUD,")
    print("  which is the right way round: a renamed heading is a site that")
    print("  moved, and the checker says so instead of going quiet.")
print()

# D4f -- the sweep.  Which heading regions carry an anchor, and which of them
# are checked?
hdr("Q3e  THE SWEEP -- every heading region carrying an anchor, against the 7")

print("  C4 checks the sites mg-821e chose.  F3 was that an anchor can be")
print("  written at a site nobody checks; the remedy names sites, so the")
print("  question the remedy raises is WHICH ONES.  Every heading region of")
print("  the repair document carrying each anchor is listed, and the ones")
print("  covered by a C4 row are marked.")
print()
ncov = nreg = 0
for needle in ANCHORS:
    rx = needle_re(needle)
    pats = [p for _l, s, p in C4_SITES if s == needle]
    print("  %s" % needle)
    for h, a, b in regions(lines):
        n = len(rx.findall("".join(lines[a:b])))
        if not n:
            continue
        nreg += 1
        cov = any(re.search(p, h) for p in pats)
        ncov += cov
        print("      %-3s %2d cop%s  %s"
              % ("[x]" if cov else "[ ]", n, "y " if n == 1 else "ies",
                 h.strip()[:58]))
    print()
miss += predict("D4f", "more regions than pairs",
                "%d regions, %d covered" % (nreg, ncov), nreg > ncov)
print("  %d heading region(s) carry an anchor; %d of them are checked."
      % (nreg, ncov))
print("  The uncovered ones are NOT a defect on their own -- C4's extent line")
print("  says a copy elsewhere `neither helps nor is required`, and that is")
print("  a true and deliberate statement.  What the sweep shows is where the")
print("  remedy's cost sits: the set of reader-facing sites is a JUDGEMENT")
print("  written into a table by hand, and nothing checks the table against")
print("  the document.  Add a section 12 that a reader would meet the")
print("  instrument's name in, and it joins the unchecked column silently --")
print("  which is F3's own shape at one remove, and the price the third")
print("  remedy charges where one copy or a derivation would not.")
print()


print("=" * 78)
print("Q3 TOTAL BAD: %d" % bad)
print("Q3 PREDICTIONS MISSED: %d" % miss)
print("=" * 78)
print()
print("EXTENT OF THOSE NUMBERS.  Q3 covers section C4 of")
print("code/species_repair_6f61/check_doc.py and the %d (site, anchor) pairs"
      % len(C4_SITES))
print("its own table declares, over ONE document,")
print("docs/OneThird-Species-Hopf-Monoids-Repair.md.  Every mutation is made")
print("on disk in the real worktree and restored, and the checker is RUN.")
print("It says nothing about C1, C2 or C3 of that file, nothing about the")
print("OTHER document check_doc.py enforces over, and nothing about whether")
print("the seven sites are the RIGHT seven -- Q3e reports that question and")
print("does not score it, because C4's extent line answers it explicitly and")
print("in the reader's favour.")
sys.exit(1 if bad else 0)
