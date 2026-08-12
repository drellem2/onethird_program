#!/usr/bin/env python3
"""mg-688c s1 -- STALE TEXT vs CURRENT TEXT, per affected citation.

The ticket's step 2, and it says to produce this first because everything else
depends on it: for each of the 4 superseded STATE.md citations and the 3
further files, what did the STALE text say and what does the CURRENT text say?
Where a strike removed a claim, NAME THE CLAIM THAT WAS STRUCK.

Both sides are read with `git show <rev>:<path>`.  The working copy of the
mirror repo is never opened -- it is now REPAIRED, so reading it would silently
answer with the current text on both sides.
"""
import sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from lib688c import *  # noqa

print("=" * 78)
print("mg-688c s1 -- WHAT THE STALE TEXT SAID, AND WHAT THE CURRENT TEXT SAYS")
print("=" * 78)
print("""
  stale   = %s   (what the checkout held for the whole window)
  current = %s   (origin/main at the repair)
  read by   git show <rev>:<path>   -- no working copy is opened
""" % (MIRROR_REV, TIP_REV))

# ---------------------------------------------------------------------------
print(rule("="))
print("A. THE CITING SITES -- mg-cdd5's NOT-CLEAN ROWS, RESTATED")
print(rule("="))
print("""
  Taken from mg-cdd5's s2 sweep, which named them.  This step does not re-run
  the citation extraction; it takes that population as given and asks what the
  text at each end of it actually says.
""")

SITES = [
    # (tier, citing file, citing line, cited doc key, mg-cdd5's class)
    (1, "STATE.md", 78, "RC", "CHANGED-WITH-STRIKE"),
    (1, "STATE.md", 112, "RC", "CHANGED-WITH-STRIKE"),
    (1, "STATE.md", 112, "KS", "CHANGED-WITH-STRIKE"),
    (1, "STATE.md", 112, "BK", "CHANGED"),
    (2, "code/row3b_audit_eba7/OUTCOMES.md", 72, "CR", "CHANGED-WITH-STRIKE"),
    (2, "docs/OneThird-Compression-W1-LinearEigenfunction-Provenance-mg-bb60.md",
     126, "KS", "CHANGED-WITH-STRIKE"),
    (2, "docs/state-history/audit-mg-eba7-of-mg-55f2.md", 112, "CR",
     "CHANGED-WITH-STRIKE"),
]
for tier, f, ln, key, cls in SITES:
    print("  tier %d  %-22s %s:%s" % (tier, cls, f, ln))
    print("          -> %s" % DOCS[key])
print("""
  7 citing sites, 4 distinct cited documents, 4 distinct citing files.
  The ticket's "4 of 6 STATE.md citations" are the four tier-1 rows; its
  "3 more in 3 more files" are the three tier-2 rows.
""")

# ---------------------------------------------------------------------------
print(rule("="))
print("B. THE CLAIMS, STALE SIDE AND CURRENT SIDE, READ FROM BOTH REVISIONS")
print(rule("="))

for c in CLAIMS:
    path = DOCS[c["doc"]]
    stale_txt = show(MIRROR_REPO, MIRROR_REV, path)
    cur_txt = show(MIRROR_REPO, TIP_REV, path)
    print()
    print(rule())
    print("%s  [%s]  %s" % (c["id"], c["kind"], c["title"]))
    print("  in %s" % path)
    print("  withdrawn by %s, on origin/main" % c["landed"])
    print(rule())

    for label, txt, loc in (("STALE   (%s)" % MIRROR_REV, stale_txt, c["loc"]),
                            ("CURRENT (%s)" % TIP_REV, cur_txt,
                             c.get("loc_cur", c["loc"]))):
        hits = [(i + 1, ln) for i, ln in enumerate(txt.splitlines())
                if re.search(loc, ln)]
        print("  %s -- locator %r matches %d line(s)" %
              (label, loc, len(hits)))
        if not hits:
            print("      (no match -- for %s that IS the finding)" % c["id"])
        for n, ln in hits[:2]:
            body = re.sub(r"\s+", " ", ln.strip())
            print("      :%-4d %s" % (n, body[:300]))
            if len(body) > 300:
                print("            ...[%d more chars]" % (len(body) - 300))
    print()
    print("  WHAT A READER OF THE STALE TREE SAW:")
    for line in wrap(c["stale"], 4):
        print(line)
    print("  WHAT THE CURRENT TEXT SAYS:")
    for line in wrap(c["current"], 4):
        print(line)

# ---------------------------------------------------------------------------
print()
print(rule("="))
print("C. THE ONE THAT IS NOT A TEXT DIFFERENCE AT ALL")
print(rule("="))
rc_stale = show(MIRROR_REPO, MIRROR_REV, DOCS["RC"])
rc_cur = show(MIRROR_REPO, TIP_REV, DOCS["RC"])
print("""
  RC2 is the sharpest of the seven and it is not a changed sentence: the
  section STATE.md:78 cites BY NAME does not exist in the stale copy.

    "5.0'" occurs in the stale copy:    %d time(s)
    "5.0'" occurs in the current copy:  %d time(s)

  A reader following that citation into the stale tree does not land on
  withdrawn text -- they land on NOTHING, in a file that otherwise reads
  normally, with the refuted bullet standing three lines from where the
  correction should have been.
""" % (len(re.findall(r"5\.0['′]", rc_stale)),
       len(re.findall(r"5\.0['′]", rc_cur))))

print(rule("="))
print("D. TALLY")
print(rule("="))
kinds = {}
for c in CLAIMS:
    kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
for k in sorted(kinds):
    print("  %-22s %d" % (k, kinds[k]))
print("  %-22s %d" % ("claims total", len(CLAIMS)))
print("""
  4 distinct cited documents.  3 carry withdrawals; the fourth (BK-Transport)
  carries a CORRECTION with no strike -- a count changed from 946 to 956 --
  which is why mg-cdd5 classed it CHANGED and not CHANGED-WITH-STRIKE.  It is
  swept here anyway: a reader of the stale copy read a wrong number with no
  indication it was wrong, which is the same shape even without the strike.
""")
print("== s1 exit: 0 ==")
