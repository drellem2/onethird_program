"""P2 -- OPEN 3: C4 IS CHECKED AT THE SITE A READER READS.

mg-6cb9's F3, MAJOR, and the THIRD instance of one shape on this document.
`check_doc.py`'s C4 was `flat(s) in flat(rep)` -- a presence test over the
whole repair document.  Three of its five anchors occur more than once in that
file (`mg-a61f` 19 times, `code/species_repair_6f61` twice, `2 of 45` three
times), so for three of five it was a check on NO SITE: delete the copy a
reader meets and the run stayed green, and only deleting EVERY copy fired.
mg-8a5c wrote this finding in the Hodge tree, mg-a318 repaired it there by
writing each figure once per site, mg-835f measured that repair at 12 of 12.
The species tree had not had the pass.

WHICH REMEDY, SAID OUT LOUD.  The brief ranks them: one copy; failing that,
derive the others from it; failing that, check at the reader-facing site.  One
copy is unavailable and not for want of effort -- `mg-a61f` is a ticket id in
running prose and a repair document that names the audit it answers exactly
once is a worse document.  Deriving is unavailable: these are markdown files
with no generator, and building one to hold a ticket id would be a new machine
to keep alive.  So it is the third remedy, and the work is in doing it
properly: SEVEN (site, anchor) pairs, each checked in the heading region a
reader meets it in, with multiplicity elsewhere printed as a number that has no
vote.

  P2a  every site, deleted ONE AT A TIME, against the repaired checker AND
       against the checker as it stood at HEAD.  The difference is the repair.
  P2b  the OTHER direction: deleting a NON-site copy is not a finding.
  P2c  the count that made this possible, per anchor.

    python3 code/species_sites_821e/p2_sites.py
"""

import os
import subprocess
import sys

from kern821e import (hdr, REPO, git_status, Probe, run_checker, flat,
                      sections, delete_at_site, replace_once)

bad = 0

CHECK_DOC = "code/species_repair_6f61/check_doc.py"
BEFORE = "code/species_repair_6f61/_before_821e.py"
REPAIR_DOC = "docs/OneThird-Species-Hopf-Monoids-Repair.md"

FRONT = r"^# Repair of mg-7d75"
S11 = r"^## 11\. REPRODUCE"
S21 = r"^### 2\.1 "
S10 = r"^## 10\. "

# (id, assertion, needle, replacement, site regex, human name of the site)
SITES = [
    ("S1", "names its target",
     "OneThird-Species-Hopf-Monoids-Where-This-Lives",
     "OneThird-Species-Hopf-Monoids-Somewhere-Else", FRONT, "front matter"),
    ("S2", "names the audit", "mg-a61f", "mg-0000", FRONT, "front matter"),
    ("S3", "names the instrument", "code/species_repair_6f61",
     "code/species_repair_0000", FRONT, "front matter"),
    ("S4", "names the instrument", "code/species_repair_6f61",
     "code/species_repair_0000", S11, "section 11 REPRODUCE"),
    ("S5", "records the missed predictions", "2 of 45", "two of forty-five",
     S21, "section 2.1"),
    ("S6", "records the missed predictions", "2 of 45", "two of forty-five",
     S11, "section 11 REPRODUCE"),
    ("S7", "records what it did NOT repair", "WHAT THIS REPAIR DID NOT DO",
     "WHAT WAS LEFT ALONE", S10, "section 10's heading"),
]


def before_checker(old):
    """`check_doc.py` as committed at HEAD, dropped in beside the live one.

    Run from the same directory, so it resolves `docs/` identically.  This is
    the reproduction: the finding is not quoted from mg-6cb9, it is re-measured
    against the code that carried it.
    """
    p = subprocess.run(["git", "show", "HEAD:" + CHECK_DOC], cwd=REPO,
                       capture_output=True, text=True)
    if p.returncode != 0 or "C4  the repair document" not in p.stdout:
        raise AssertionError("cannot read check_doc.py at HEAD")
    return p.stdout


def replace_everywhere(needle, repl):
    def fn(old):
        if old is None or needle not in old:
            raise AssertionError("needle absent: %r" % needle[:40])
        return old.replace(needle, repl)
    return fn


BASE = git_status()


def run(edits, which=CHECK_DOC):
    with Probe(edits):
        code, out = run_checker(which)
    after = git_status()
    if after != BASE:
        print("\n*** THE RESTORE DID NOT RESTORE -- stopping.")
        print(after)
        sys.exit(2)
    return code, out


# ---------------------------------------------------------------------------
# P2a  one site at a time, both checkers
# ---------------------------------------------------------------------------
hdr("P2a  DELETE THE COPY A READER MEETS -- ONE SITE AT A TIME")

print("  Each row deletes ONE anchor from ONE heading region and leaves every")
print("  other copy in the file untouched.  `HEAD` is `check_doc.py` as")
print("  committed before this ticket, run from the same directory against the")
print("  same mutated document: a presence test over the whole file.")
print()
print("  %-4s %-32s %-22s %-6s %-6s %s"
      % ("id", "anchor", "site", "HEAD", "now", "verdict"))

rep_text = open(os.path.join(REPO, REPAIR_DOC), encoding="utf-8").read()
frep = flat(rep_text)
rows = []
for sid, label, needle, repl, site_pat, site_name in SITES:
    edit = (REPAIR_DOC, delete_at_site(site_pat, needle, repl))
    now, _ = run([edit])
    was, _ = run([edit, (BEFORE, before_checker)], which=BEFORE)
    copies = frep.count(flat(needle))
    ok = (now == 1)
    bad += (not ok)
    rows.append((sid, label, needle, site_name, was, now, copies))
    print("  %-4s %-32s %-22s %-6d %-6d %s"
          % (sid, label[:32], site_name, was, now,
             "FIRES" if ok else "*** STILL GREEN ***"))
print()
fired_head = sum(1 for r in rows if r[4] == 1)
fired_now = sum(1 for r in rows if r[5] == 1)
print("  %d of %d fired at HEAD.  %d of %d fire now."
      % (fired_head, len(rows), fired_now, len(rows)))
print("  The rows where HEAD is 0 are mg-6cb9's F3: an anchor with more copies")
print("  was LESS covered, because the surviving copies stood in for the one a")
print("  reader had lost.")
print()


# ---------------------------------------------------------------------------
# P2b  the other direction, and the case the old check did catch
# ---------------------------------------------------------------------------
hdr("P2b  THE OTHER DIRECTION -- and the one case a presence test caught")

print("  A site check has to be wrong in the other direction too, or it is")
print("  just a stricter presence test.  Deleting a copy that is NOT at a")
print("  declared site must be silent: those copies are prose, they are not")
print("  the anchor, and the extent line says so.")
print()

OUT_PROBES = [
    ("S8", "an `mg-a61f` copy in section 5, not a declared site",
     (REPAIR_DOC, delete_at_site(r"^## 5\. ", "mg-a61f", "mg-0000")), 0),
    ("S9", "a `2 of 45` copy in section 8, not a declared site",
     (REPAIR_DOC, delete_at_site(r"^## 8\. ", "2 of 45", "two of forty-five")),
     0),
    ("S10", "a whole unrelated section's prose rewritten",
     (REPAIR_DOC, replace_once("**What was wrong.**", "**The defect.**")), 0),
]
for pid, what, edit, expect in OUT_PROBES:
    code, _ = run([edit])
    ok = (code == expect)
    bad += (not ok)
    print("  %-5s %-58s exit %d  %s"
          % (pid, what[:58], code, "silent -- ok" if ok else "*** FIRES ***"))
print()

print("  And the case the presence test DID catch -- every copy deleted.  Both")
print("  checkers must fire; this is the only mutation the old one could see.")
print()
for sid, label, needle, repl, _sp, _sn in SITES[:5]:
    if sid in ("S4", "S6"):
        continue
    edit = (REPAIR_DOC, replace_everywhere(needle, repl))
    now, _ = run([edit])
    was, _ = run([edit, (BEFORE, before_checker)], which=BEFORE)
    ok = (was == 1 and now == 1)
    bad += (not ok)
    print("  %-4s every copy of %-34s HEAD %d, now %d  %s"
          % (sid, ("`%s`" % needle)[:34], was, now,
             "both fire -- ok" if ok else "*** ONE DID NOT ***"))
print()


# ---------------------------------------------------------------------------
# P2c  multiplicity, printed
# ---------------------------------------------------------------------------
hdr("P2c  THE MULTIPLICITY THAT MADE IT POSSIBLE")

print("  %-38s %-8s %s" % ("anchor", "copies", "declared site(s)"))
seen = {}
for sid, label, needle, repl, site_pat, site_name in SITES:
    seen.setdefault(needle, []).append(site_name)
for needle, where in seen.items():
    print("  %-38s %-8d %s" % (("`%s`" % needle)[:38], frep.count(flat(needle)),
                               "; ".join(where)))
print()
print("  mg-a318 closed the same shape in the Hodge tree by DERIVING each")
print("  figure from one source so that each was written once per site.  That")
print("  is the better remedy and it is not available for a ticket id in")
print("  prose.  What is available is naming the site, which is what the rows")
print("  above are.  The counts are printed because they are the reason: an")
print("  anchor with 19 copies was the LEAST covered of the five.")
print()

print("=" * 78)
print("P2 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  %d site deletions, %d non-site mutations and %d"
      % (len(SITES), len(OUT_PROBES),
         len([s for s in SITES[:5] if s[0] not in ("S4", "S6")])))
print("delete-every-copy mutations, all against ONE checker -- `check_doc.py`")
print("-- and ONE file, `docs/OneThird-Species-Hopf-Monoids-Repair.md`.  Each")
print("mutation is applied to the REAL worktree and undone, with `git status")
print("--porcelain` compared before and after.  It says NOTHING about C1, C2")
print("or C3 of that checker, which were already per-site: C1 requires each")
print("stricken sentence to occur outside no strike, and that is a check at")
print("every site by construction.  It says nothing about the OTHER documents")
print("in this arc, and nothing about whether the anchors are the RIGHT five.")
sys.exit(1 if bad else 0)
