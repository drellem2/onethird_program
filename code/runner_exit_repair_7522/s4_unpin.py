"""S4 -- A PINNED BASELINE IS CORRECT FOR COMPARING AND BLIND FOR ENUMERATING.

mg-821e found that a comparison anchored to `HEAD` stops comparing the moment
the repair lands, and pinned it.  That was the right fix.  mg-c2b3 inherited the
pin and used it for its CALLER SCAN as well -- and a caller scan is not a
comparison, it is a CENSUS.  `code/species_depth_audit_4700/` executes three
affected runners twenty-one times and scores them on `rc == 0` at eight sites;
it landed in `5c16f5c`, after the pin, so no run of the scan could ever have
seen it.

    SAME REMEDY, OPPOSITE EFFECT, DEPENDING ON WHETHER THE THING DOWNSTREAM
    IS A COMPARISON OR A CENSUS.

The fix is to unpin the scan for the enumeration while keeping the pin for the
comparison.  Both halves are MEASURED here rather than argued, and so is a third
thing the ticket's remedy does not cover: unpinning is NECESSARY AND NOT
SUFFICIENT.  The 4700 site is invisible for TWO independent reasons -- the
anchor, and a line-local rule that demands a literal `<tree>/run_all.sh` on the
executing line, which `run_runner(t)` and `subprocess.run(["sh", "run_all.sh"],
cwd=d)` do not have.  S4b is the 2x2 that separates them.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib7522 as L

BAD = 0

L.bar("S4  THE ANCHOR OF A CENSUS IS NOT THE ANCHOR OF A COMPARISON")

# ---------------------------------------------------------------------------
L.hdr("S4a  THE RULE, STATED ONCE")

print("  A baseline pinned to a revision is:")
print()
print("      CORRECT for a COMPARISON.  The question is `did this move`, and")
print("      the answer needs a fixed side.  Anchored to HEAD, a comparison")
print("      compares the repaired tree with itself and reports no change")
print("      forever -- mg-821e's finding, and the reason for the pin.")
print()
print("      BLIND for a CENSUS.  The question is `what exists`, and the")
print("      answer must see the current world.  Anchored to a revision, a")
print("      census cannot contain anything added after it -- not because the")
print("      rule is wrong but because the world it is asked about is stale.")
print()
print("  The two uses want different anchors.  Where both appear in one file,")
print("  they are named; S4e checks that they are.")

# ---------------------------------------------------------------------------
L.hdr("S4b  THE 2x2 -- anchor x rule, MEASURED")

LITERAL = re.compile(r"([\w./]*?([\w]+)/(?:run_all|run_audit)\.sh)")
RUNTIME = re.compile(r"[\"']\w*run\w*\.sh[\"']|(?<!def )run_runner\(|\./run_\w*\.sh")
EXEC = re.compile(r"subprocess\.(?:run|Popen|call|check_output|check_call)\("
                  r"|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh|(?<!def )run_runner\(")
NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
READ = re.compile(r"returncode|check\s*=\s*True")
ASSIGN = re.compile(r"^\s*([A-Za-z_]\w*)(?:\s*,\s*([A-Za-z_]\w*))*\s*=\s*\S")


def scan(ref, runtime_rule):
    """[(file, line, target, consumes, text)] under one anchor and one rule."""
    files = [f for f in L._sources_at(ref)]
    out = []
    for f in files:
        try:
            src = L.read(f, ref)
        except (RuntimeError, OSError):
            continue
        lines = src.split("\n")
        for i, line in enumerate(lines, 1):
            if line.lstrip().startswith("#") or NOT_EXEC.search(line):
                continue
            if not EXEC.search(line):
                continue
            m = LITERAL.search(line)
            if m and "%" not in m.group(1):
                target = m.group(2)
            elif runtime_rule and RUNTIME.search(line):
                target = "(path built at run time)"
            else:
                continue
            window = "\n".join(lines[i - 1:i + 25])
            if f.endswith(".sh"):
                consumes = L.has_set_e(src) and not L.guarded(line)
            else:
                consumes = bool(READ.search(window))
                am = ASSIGN.match(line)
                if not consumes and am:
                    for name in [g for g in am.groups() if g]:
                        if re.search(r"\b%s\b\s*(?:==|!=)" % name, window):
                            consumes = True
                            break
            out.append((f, i, target, consumes, line.strip()))
    return out


CELLS = {}
for aname, ref in (("PINNED %s" % L.PINNED, L.PINNED), ("HEAD (unpinned)", None)):
    for rname, rt in (("literal path only", False), ("+ runtime path", True)):
        CELLS[(aname, rname)] = scan(ref, rt)

print("  Each cell is the number of EXECUTION sites found, and in brackets the")
print("  number that also READ the status.  The rule is a property of the scan;")
print("  the anchor is a property of the question.")
print()
print("  %-22s %-24s %-24s" % ("", "literal path only", "+ runtime path"))
for aname in ("PINNED %s" % L.PINNED, "HEAD (unpinned)"):
    row = []
    for rname in ("literal path only", "+ runtime path"):
        c = CELLS[(aname, rname)]
        row.append("%d sites  [%d read]" % (len(c), len([x for x in c if x[3]])))
    print("  %-22s %-24s %-24s" % (aname, row[0], row[1]))
print()

TARGET_TREE = "code/species_depth_audit_4700"
print("  WHERE `%s` APPEARS -- the site mg-05eb found" % TARGET_TREE)
print("  outside the enumeration.  One cell of four, and it is the one that")
print("  needs BOTH fixes:")
print()
found_in = []
for key, c in sorted(CELLS.items()):
    hits = [x for x in c if x[0].startswith(TARGET_TREE)]
    reading = [x for x in hits if x[3]]
    mark = "FOUND" if hits else "not found"
    print("      %-22s %-20s %-10s %d site(s), %d reading the status"
          % (key[0], key[1], mark, len(hits), len(reading)))
    if hits:
        found_in.append(key)
print()
if found_in == [("HEAD (unpinned)", "+ runtime path")]:
    print("  EXACTLY ONE CELL.  Unpinning alone does not find it and widening")
    print("  the rule alone does not find it: the pin and the literal-path")
    print("  rule are two INDEPENDENT reasons the same site fell outside the")
    print("  enumeration, and the ticket's remedy names one of the two.")
    print("  Both are reported; only the anchor half is a change to mg-c2b3's")
    print("  own scan, and the rule half lives here with its limit stated.")
else:
    BAD += 1
    print("  *** the 2x2 does not separate as the repair predicts ***")
    print("  found in: %s" % (found_in,))
print()
for x in sorted(CELLS[("HEAD (unpinned)", "+ runtime path")]):
    if x[0].startswith(TARGET_TREE):
        print("      %s:%d  %-8s %s" % (x[0], x[1],
                                        "READS" if x[3] else "no", x[4][:64]))

# ---------------------------------------------------------------------------
L.hdr("S4c  THE COMPARISON THAT MUST KEEP ITS PIN -- measured both ways")

print("  mg-c2b3's K3d asks `did any committed transcript move`.  It is a")
print("  COMPARISON.  Run it at the pin and again anchored to HEAD:")
print()


def changed_since(ref):
    args = ["diff", "--name-only"] + ([ref] if ref else []) + ["--"]
    return [f for f in L.git(*args).split() if f]


pin_changed = changed_since(L.PINNED)
head_changed = changed_since(None)
pin_out = [f for f in pin_changed if "/out" in f or f.endswith("_output.txt")]
head_out = [f for f in head_changed if "/out" in f or f.endswith("_output.txt")]
print("      anchored to %-12s  %4d file(s) changed, %d transcript(s)"
      % (L.PINNED, len(pin_changed), len(pin_out)))
print("      anchored to %-12s  %4d file(s) changed, %d transcript(s)"
      % ("HEAD", len(head_changed), len(head_out)))
print()
print("  Anchored to HEAD the question is `does the worktree differ from")
print("  itself`.  On a COMMITTED tree the answer is 0 BY CONSTRUCTION -- it")
print("  would print a clean bill for any repair whatsoever.  The %d above is"
      % len(head_changed))
print("  this probe's own uncommitted edits if it is run mid-repair, and 0")
print("  once they land; either way it is a fact about the worktree and not")
print("  about the repair.  The pin is the whole content of that check.")
print()
if len(pin_changed) <= len(head_changed):
    BAD += 1
    print("  *** the pinned comparison is not more informative than the")
    print("      HEAD-anchored one; the demonstration did not reproduce ***")
else:
    print("  MEASURED: the pinned side sees %d files, the HEAD side sees %d."
          % (len(pin_changed), len(head_changed)))

# ---------------------------------------------------------------------------
L.hdr("S4d  THE PAST CLAIM THAT SAT OUTSIDE THE ENUMERATION")

print("  mg-05eb's F3: `%s/q2_wiring.py` scores three" % TARGET_TREE)
print("  species runners on their exit status, and its committed transcript")
print("  asserts `exit 0 ... SWALLOWED` for two runners that were AFFECTED.")
print("  That is an R3 claim by mg-c2b3's own routing, and it was not among")
print("  the nine -- because the caller scan could not reach it.")
print()
landed = L.git("log", "--format=%h", "-1", "--", TARGET_TREE).strip()
is_after = subprocess.run(
    ["git", "-C", L.REPO, "merge-base", "--is-ancestor", L.PINNED, landed],
    capture_output=True).returncode == 0
print("      the pin                          %s" % L.PINNED)
print("      the tree's most recent commit    %s" % landed)
print("      the pin is an ancestor of it     %s" % ("YES" if is_after else "no"))
print()
if not is_after:
    BAD += 1
    print("  *** the tree does not post-date the pin; the diagnosis does not")
    print("      reproduce ***")
else:
    print("  So the tree post-dates the pin and a pinned scan could not")
    print("  contain it -- measured from git, not read off mg-05eb's prose.")
print()
q2 = os.path.join(TARGET_TREE, "out_q2_wiring.txt")
try:
    txt = L.read(q2, None)
    rows = [l for l in txt.splitlines() if "SWALLOWED" in l]
    print("      `SWALLOWED` rows in %s: %d" % (q2, len(rows)))
    for r in rows[:6]:
        print("          %s" % r.strip()[:88])
except (RuntimeError, OSError):
    print("      (%s not present at HEAD)" % q2)
print()
print("  WHAT IS AND IS NOT SETTLED HERE.  S4 puts the site INSIDE the")
print("  enumeration; it does not re-run the claim.  mg-05eb's J2c already")
print("  measured that both rows flip when the probe is re-run at HEAD, and")
print("  that measurement is not repeated -- naming which probe settled it is")
print("  stronger than a second copy of the same run.")

# ---------------------------------------------------------------------------
L.hdr("S4e  SAY SO WHERE BOTH APPEAR -- checked on the bytes")

K2 = "code/runner_exit_c2b3/k2_consume.py"
src = L.read(K2, None)
checks = [
    ("names the CENSUS use", re.search(r"CENSUS", src)),
    ("names the COMPARISON use", re.search(r"COMPARISON", src)),
    ("carries the rule in one sentence",
     re.search(r"CORRECT for COMPARING and BLIND for ENUMERATING", src)),
    ("the caller scan is unpinned",
     re.search(r"CALLER_REF\s*=\s*None", src)),
    ("the runner classification is still pinned",
     re.search(r"L\.read\(r, REF\)|srcs = \{r: L\.read\(r, REF\)", src)),
    ("the residual literal-path limit is stated",
     re.search(r"literal-path rule", src)),
]
print("  %s, where a census and a comparison meet:" % K2)
print()
for name, ok in checks:
    print("      %-42s %s" % (name, "yes" if ok else "*** NO ***"))
    if not ok:
        BAD += 1

# ---------------------------------------------------------------------------
L.hdr("S4f  THE GENERAL FORM, ON THIS SECTION")

print("  S4 is a probe about the anchor of an enumeration, so the question it")
print("  owes is what ITS OWN enumerations are anchored to.  Every call, with")
print("  which kind it is:")
print()
print("   1. S4b `scan(ref=None, ...)`   CENSUS      -- unpinned, on purpose.")
print("   2. S4b `scan(ref=PINNED, ...)` COMPARISON  -- pinned, because the")
print("      pinned answer is one side of the 2x2 being compared.")
print("   3. S4c `changed_since(PINNED)` COMPARISON  -- pinned, and S4c is the")
print("      row that shows why removing that pin would empty it.")
print("   4. S4d `git log -1 -- <tree>`  CENSUS      -- unpinned; it asks when")
print("      the tree last moved in the world as it stands.")
print("   5. S4e `L.read(K2, None)`      CENSUS      -- unpinned; it reads the")
print("      file as it is now, which is the only state whose wording matters.")
print()
print("  The branch that CANNOT exhibit the defect, with the reason: S4 makes")
print("  no claim that anything is ABSENT from the world.  Every negative it")
print("  prints is `not found by THIS rule at THIS anchor`, and all four")
print("  combinations are printed, so a reader can see the rule and the anchor")
print("  that produced each answer instead of one number with neither.")
print()
print("  THE LIMIT, stated rather than omitted: the runtime-path rule finds")
print("  the SITE but cannot name the TARGET TREE, because the path is")
print("  assembled from a variable and this is a line-local scan.  Rows in")
print("  that state print `(path built at run time)` rather than being")
print("  dropped -- a row that says `I cannot name the target` is a census")
print("  entry and a dropped row is not.")

print()
L.bar("S4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) the 2x2 not separating as the")
print("repair predicts, (b) the pinned comparison not being more informative")
print("than the HEAD-anchored one, (c) the 4700 tree not post-dating the pin,")
print("and (d) a missing sentence in %s.  It ranges over" % K2)
print("every tracked `*.py` and `*.sh` at HEAD and at %s." % L.PINNED)
sys.exit(1 if BAD else 0)
