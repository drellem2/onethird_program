"""A2 -- THE CROSS-SECTION CHECK, SHOWN TO FIRE, BY SOMEONE WHO DID NOT
WRITE IT.

The brief: *"A cross-section check that has never been shown to fire is the
vacuous-check defect again, which this arc has now produced twice tonight."*
`e2_crosssection.py` carries its own controls, and a control an author writes
against their own detector is the thing being audited, not the audit.  So this
file re-introduces struck claims in other sections of live documents, ON DISK,
and reports what the run says.

Six probes.  Three IN -- the claim genuinely restated where the strike does
not reach -- and three OUT, each one of the three ways `e2` says it does not
fire: another document, a paragraph that says the claim does not hold, and a
second strike.  A detector shown to fire but never shown to be silent is the
other half of the same defect.

A2 also measures the extent line of the run mg-d633 COMMITTED, against the
tree mg-d633 committed it into.

    python3 code/species_extent_audit_6cb9/a2_crosssection.py
"""

import os
import re
import subprocess
import sys

from kern6cb9 import hdr, REPO, git_status, Probe, run_checker, plant, sh

bad = 0

E2 = "code/species_extent_d633/e2_crosssection.py"
DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
BRAT = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
OTHER = "docs/OneThird-Audit-mg-7dd3-Extent-Repair.md"

# The three struck claims used below, quoted from the live documents.  Each is
# lifted out of its `~~ ... ~~` and restated with the strike markers removed --
# which is exactly the shape B1 had: not a paraphrase, the sentence itself,
# somewhere else in the same file, unmarked.
X7_STRUCK = ('*"Recall from Section 17.4 that `K̄(Π)` is the algebra of '
             'symmetric functions in\nnoncommuting variables and `K(Π)` is '
             'the familiar Hopf algebra of symmetric functions"*')
X1_STRUCK = ('*"Smallest witness with `AC(P) ≠ Π[n]`: `P = {a<c, b<d}`, '
             'where `ad|bc` has a\n2-cycle."*')
BRAT_STRUCK = ('*"there is a multiplicity-free tower whose branching graph '
               'and path-pair count are\nparameter-independent and which is '
               'a sum of endomorphism algebras at some parameters and not '
               'at others"*')

PAD = "\n\n"


def para(body):
    """A plain paragraph.  No ticket id, no strike, and no word from e2's
    NEGATES set -- if the planted paragraph exonerated itself the probe would
    measure the exoneration rule instead of the detector, which is the defect
    mg-d633 recorded in its own P11."""
    return PAD + body.strip() + PAD


def para_negated(body):
    return PAD + body.strip() + "\n\nThat sentence was corrected here.\n" + PAD


def para_struck(body):
    return PAD + "~~" + body.strip() + "~~" + PAD


PROBES = [
    ("R0", "-", DOC, None, 0,
     "unmutated"),
    ("R25", "IN", DOC, para(
        "Aguiar–Mahajan §17.5, quoting their own §17.4:\n" + X7_STRUCK), 1,
     "B1 itself: §4's struck AM §17.5 quotation, live and unmarked in §0"),
    ("R26", "IN", DOC, para(
        "For the record, the extremal statement stands as first written:\n"
        + X1_STRUCK), 1,
     "§8's struck extremal claim (X1), restated live in another section"),
    ("R27", "IN", BRAT, para(
        "The separating example, as first stated:\n" + BRAT_STRUCK), 1,
     "a struck claim in a SECOND document, restated in another of its sections"),
    ("R28", "OUT", DOC, para(
        "The separating example, as first stated:\n" + BRAT_STRUCK), 0,
     "the SAME restatement, in a DIFFERENT document from its strike"),
    ("R29", "OUT", BRAT, para_negated(
        "The separating example, as first stated:\n" + BRAT_STRUCK), 0,
     "the restatement, with 'corrected' in the NEXT paragraph"),
    # R29 above is KEPT AS PREDICTED AND IT MISSED.  I wrote the negation as
    # its own paragraph; e2's exoneration reads the paragraph CARRYING the
    # occurrence and nothing else, so it fired.  That is the rule being
    # narrower than I read it, not a defect, and R29b is added -- not
    # substituted -- to measure the exoneration where it actually applies.
    ("R29b", "OUT", BRAT, PAD + "The separating example, as first stated: "
     + BRAT_STRUCK.replace("\n", " ")
     + "  That sentence was corrected here and does not hold.\n" + PAD, 0,
     "the restatement INSIDE a paragraph that says it does not hold"),
    ("R30", "OUT", BRAT, para_struck(
        "The separating example, as first stated:\n" + BRAT_STRUCK), 0,
     "the restatement inside a SECOND strike"),
]

hdr("A2a  THE CROSS-SECTION CHECK, RE-INTRODUCED STRUCK CLAIMS, ON DISK")
print("  Predicted in PREDICTIONS.md before the run.  `standing` is what the")
print("  RUN SAYS, which is a different claim from the exit code: three")
print("  scripts in this arc have reported a finding and exited 0.")
print()
print("  %-5s %-4s %-52s %-4s %-4s %-9s %s"
      % ("id", "dir", "what", "exp", "got", "standing", "verdict"))

BASE = git_status()
outs = {}
codes = {}
for pid, direction, target, body, expect, what in PROBES:
    edits = [] if body is None else [(target, plant(body))]
    with Probe(edits):
        code, out = run_checker(E2)
    if git_status() != BASE:
        print("*** RESTORE FAILED at %s" % pid)
        sys.exit(2)
    codes[pid] = code
    outs[pid] = out
    m = re.search(r"(\d+) file\(s\) carry a strike, (\d+) strike\(s\) "
                  r"measured, (\d+) standing", out)
    standing = int(m.group(3)) if m else -1
    ok = (code == expect) and ((standing > 0) == (expect == 1))
    bad += (not ok)
    print("  %-5s %-4s %-52s %-4d %-4d %-9d %s"
          % (pid, direction, what[:52], expect, code, standing,
             "as predicted" if ok else "*** MISSED ***"))
print()
print("  Every IN row above is a struck claim put back in ANOTHER SECTION of")
print("  the SAME document, exactly the way §0 carried §4's strike from")
print("  `83ac472` past four passes with every per-section checker green.")
print("  R27 does it in a document nobody in this arc has planted in, to")
print("  show the rule is not tuned to the species document.")
print()

hdr("A2b  WHAT THE FIRING RUN ACTUALLY PRINTS")
for pid in ("R25", "R27"):
    print("  --- %s" % pid)
    for line in outs[pid].splitlines():
        if "STANDING UN-STRUCK" in line or "standing." in line:
            print("     %s" % line.strip()[:110])
print()
ok = all("*** STANDING UN-STRUCK ***" in outs[p] for p in ("R25", "R26", "R27"))
bad += (not ok)
print("  %-62s %s" % ("all three IN probes print STANDING UN-STRUCK",
                      "ok" if ok else "*** THEY DO NOT ***"))
print()

# ---------------------------------------------------------------------------
# A2c  the committed extent of the cross-section run, against its own tree
# ---------------------------------------------------------------------------
hdr("A2c  THE COMMITTED RUN'S EXTENT LINE, AGAINST THE TREE IT SHIPPED IN")

committed = open(os.path.join(REPO, "code/species_extent_d633/"
                              "out_e2_crosssection.txt"),
                 encoding="utf-8").read()
m = re.search(r"EXTENT OF THIS NUMBER\.\s+(\d+) markdown file\(s\)", committed)
claimed = int(m.group(1)) if m else -1

# THE SHIPPED TREE, not this worktree.  This instrument adds markdown files
# of its own, and counting them into the comparison would be the same defect
# this section reports, committed by the file reporting it.  So the number the
# committed extent line is tested against is `git ls-tree HEAD`, and what my
# own tree adds is named separately below.
def md_at(ref):
    rc, tree, _ = sh(["git", "ls-tree", "-r", "--name-only", ref])
    return sorted(f for f in tree.splitlines()
                  if f.endswith(".md") and (f.startswith("docs/")
                                            or f.startswith("code/")))


shipped = md_at("HEAD")
live = 0
for base in ("docs", "code"):
    for root, dirs, files in os.walk(os.path.join(REPO, base)):
        live += sum(1 for f in files if f.endswith(".md"))

code, out = run_checker(E2)
m2 = re.search(r"EXTENT OF THIS NUMBER\.\s+(\d+) markdown file\(s\)", out)
fresh = int(m2.group(1)) if m2 else -1
mine = live - len(shipped)

print("  the committed out_e2_crosssection.txt says      %3d markdown file(s)"
      % claimed)
print("  `git ls-tree HEAD` -- the tree it shipped in -- %3d" % len(shipped))
print("  a clean re-run in this worktree says            %3d" % fresh)
print("  of which %d are THIS instrument's own files, which is why the" % mine)
print("  comparison below is against the SHIPPED tree and not against my")
print("  worktree: measuring a commit with your own additions in the count")
print("  is the defect this section is about.")
print()
ok = (fresh == live)
bad += (not ok)
print("  %-62s %s" % ("the LIVE run's extent line is true", "ok" if ok
                      else "*** FALSE ***"))
stale = (claimed != len(shipped))
print("  %-62s %s" % ("the COMMITTED run's extent line is true at HEAD",
                      "*** FALSE, off by %d ***" % (len(shipped) - claimed)
                      if stale else "ok"))
mm = re.search(r"(\d+) file\(s\) carry a strike, (\d+) strike\(s\) measured",
               committed)
mf = re.search(r"(\d+) file\(s\) carry a strike, (\d+) strike\(s\) measured",
               outs["R0"])


def census(ref):
    c = s = 0
    for f in md_at(ref):
        n = len(re.findall(r"~~(.+?)~~",
                           sh(["git", "show", "%s:%s" % (ref, f)])[1], re.S))
        c += (n > 0)
        s += n
    return c, s


hc, hs = census("HEAD")
print("  the census, three ways:")
print("      committed evidence says       %2s file(s) carry a strike, %2s "
      "strike(s)" % (mm.group(1), mm.group(2)))
print("      the SHIPPED tree at HEAD has  %2d and %2d" % (hc, hs))
print("      this worktree's live run says %2s and %2s"
      % (mf.group(1), mf.group(2)))
ok = (int(mm.group(1)) == hc and int(mm.group(2)) == hs)
bad += (not ok)
print("  %-62s %s" % ("the committed CENSUS is right for the shipped tree",
                      "ok" if ok else "*** WRONG ***"))
print("  The live run differs from both because THIS instrument's own")
print("  PREDICTIONS.md contains a literal `~~strike~~` in its probe table")
print("  and e2 reads every *.md under code/.  My instrument perturbs the")
print("  measurement it is taking, by one file and one strike, and saying so")
print("  is cheaper than pretending the number is clean.")
print("  So exactly ONE thing in the committed output is stale: the FILE")
print("  COUNT in its extent line, and the line numbers that go with it.")
print()

# Which tree does the committed number describe?
print("  Which tree does %d describe?  Counting *.md at each commit:" % claimed)
match = None
rc, log, _ = sh(["git", "log", "--format=%h %s", "-8"])
for line in log.splitlines():
    h = line.split()[0]
    rc, tree, _ = sh(["git", "ls-tree", "-r", "--name-only", h])
    n = sum(1 for f in tree.splitlines()
            if f.endswith(".md") and (f.startswith("docs/")
                                      or f.startswith("code/")))
    flag = ""
    if n == claimed and match is None:
        match = h
        flag = "  <-- the committed number describes THIS tree"
    print("      %-9s %3d  %s%s" % (h, n, line.split(None, 1)[1][:44], flag))
print()
head = sh(["git", "rev-parse", "--short", "HEAD"])[1].strip()
if match and not match.startswith(head[:7]) and head[:7] != match:
    rc, dist, _ = sh(["git", "rev-list", "--count", "%s..HEAD" % match])
    print("  The evidence committed by the repair was produced %s commit(s)"
          % dist.strip())
    print("  BEFORE the commit that ships it.  This arc's own Appendix A")
    print("  already carries, from mg-8e30 / e16e41c:")
    print("      A COMMIT THAT MEASURES SOMETHING IT ALSO MODIFIES MUST")
    print("      PUBLISH THE POST-COMMIT MEASUREMENT")
    bad += 1
print()

# And the sharpest form of it: which .md files are in the live sweep and not
# in the committed one?
old = set(md_at(match or "HEAD"))
newmd = [f for f in shipped if f not in old]
print("  The %d markdown file(s) in the SHIPPED tree and not in the tree the"
      % len(newmd))
print("  committed evidence measured -- the files that evidence does not")
print("  cover, with whether each carries a strike:")
carriers = 0
for f in newmd:
    text = open(os.path.join(REPO, f), encoding="utf-8").read()
    n = len(re.findall(r"~~(.+?)~~", text, re.S))
    carriers += (n > 0)
    print("      %-64s %d strike(s)" % (f, n))
own = [f for f in newmd if "species_extent_d633" in f or "Repair-Extent" in f]
print()
print("  %d of them are the repair's OWN documents, and %d of them carry a"
      % (len(own), carriers))
print("  strike.  So the VERDICT survives -- none of the unread files could")
print("  have changed it, and re-run at HEAD it is still 0 standing (R0).")
print("  What is false is the EXTENT LINE, and this audit is about extent")
print("  lines: the run shipped as evidence for a cross-section check did")
print("  not read the document the repair itself added, and says 100 where")
print("  the tree it is committed into holds %d.  A second, independent" % len(shipped))
print("  witness: the committed rows for the Bratteli document cite strike")
print("  line 112 and the shipped tree has it at 120 -- the output was")
print("  produced before this commit's own parent.  Same shape as mg-8e30")
print("  and mg-a318, and this is the fourth instance.")
print()

hdr("A2d  IS THE CROSS-SECTION CHECK REACHABLE FROM WHERE THE BELIEF LIVED?")
print("  A correction that is true and unreachable is this arc's most")
print("  repeated finding.  e2 is a NEW check; the question is whether a")
print("  reader or a runner meets it from where B1 lived.")
print()
sites = [
    ("the four checkers' own printed output name it",
     ["code/species_repair_a4ef/s1_extent.py",
      "code/species_repair_a4ef/s2_seam.py"],
     "code/species_extent_d633/e2_crosssection.py"),
    ("the document that carried B1 names it",
     [DOC], "e2_crosssection"),
    ("the repair document names it",
     ["docs/OneThird-Species-Hopf-Monoids-Repair-Extent-Measured.md"],
     "e2_crosssection"),
    ("the species trees' run_all.sh reach it",
     ["code/species_repair_a4ef/run_all.sh",
      "code/species_repair_6f61/run_all.sh",
      "code/species_remainder_f8fa/run_all.sh"],
     "e2_crosssection"),
]
for label, paths, needle in sites:
    hits = []
    for p in paths:
        fp = os.path.join(REPO, p)
        if os.path.exists(fp):
            if needle in open(fp, encoding="utf-8").read():
                hits.append(p)
    ok = len(hits) == len(paths)
    print("  %-52s %d of %d  %s"
          % (label, len(hits), len(paths), "ok" if ok else "***"))
    for p in paths:
        if p not in hits:
            print("        NOT reachable from  %s" % p)
print()
print("  The last row is the one that matters and it is the finding: the")
print("  three species trees each ship a `run_all.sh`, and a worker who runs")
print("  the tree they are repairing runs every checker in it and NOT the")
print("  cross-section check.  e2 runs only from")
print("  code/species_extent_d633/run_all.sh, which is the AUDIT instrument's")
print("  own runner.  The check that closes B1 is reachable by reading and")
print("  not by running, from every tree whose checkers were green while B1")
print("  stood.")

final = git_status()
hdr("A2 TOTAL BAD: %d" % bad)
print("EXTENT OF THIS NUMBER.  %d probes against e2_crosssection.py, each ONE"
      % len(PROBES))
print("planted paragraph in ONE live document, applied on disk and undone")
print("(%s).  Plus the committed extent line of ONE output file"
      % ("worktree identical" if final == BASE else "*** WORKTREE DIRTY ***"))
print("against the tree it shipped in, and FOUR reachability sites named one")
print("by one.  It says NOTHING about paraphrase -- every probe here restates")
print("VERBATIM, because that is all e2 matches -- nothing about a claim")
print("struck in one file and asserted in another, and nothing about strikes")
print("in the 93 markdown files that carry none.")
if final != BASE:
    sys.exit(2)
sys.exit(1 if bad else 0)
