"""E2 --- IS "EVERY DISPOSITION LABEL" EVERY DISPOSITION LABEL?

mg-d330, on the mg-13b2 repair.  My brief's primary target:

    "For each label, read the diff and confirm the label is true.  Report per
     label, both directions.  A label is a claim.  Treat it exactly as you
     would a number in the prose."

    "No bare totals; name the population."

The repair's own claim is `29 labels, 100 checks` and that **every**
disposition label in the delivered document is measured.  `29` is a numerator.
This script derives the DENOMINATOR independently --- by sweeping the document
for the disposition vocabulary the target's own docstring names --- and
reports which label sites no check in `t5_labels.py` reads.

It also checks the three self-referential figures the repair prints about its
own instrument, because those are claims in the prose and nothing in the tree
compares them to what the instrument produces.

Exit 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
"""

import importlib.util
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
TARGET_DIR = os.path.join(ROOT, "code", "branching_locate_db09")
DOC_REL = "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md"
DOC = os.path.join(ROOT, DOC_REL)
T5 = os.path.join(TARGET_DIR, "t5_labels.py")
O5 = os.path.join(TARGET_DIR, "out_t5_labels.txt")
RDM = os.path.join(TARGET_DIR, "README.md")

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)
    print("   SELF-ERROR: " + m)


def finding(m):
    FIND.append(m)
    print("   FINDING: " + m)


# The disposition vocabulary.  Taken from t5_labels.py's OWN docstring ---
# "WITHDRAWN, CORRECTED, SUPERSEDED, 'Updated', 'Deliberately NOT repaired',
# CLOSED, OPEN" --- plus the four further markers the document actually uses
# and that docstring does not list.  Listed separately so the second group can
# be read as an answer in itself.
VOCAB_NAMED = ["WITHDRAWN", "Withdrawn", "withdrawn",
               "CORRECTED", "Corrected", "corrected",
               "SUPERSEDED", "Superseded",
               "Updated (", "Deliberately NOT repaired",
               "**CLOSED", "CLOSED —", "**OPEN", "OPEN.", "OPEN,"]
VOCAB_UNNAMED = ["MARKED IN PLACE", "UPGRADED", "OUTCOME (", "RETRACT",
                 "PARTLY EVALUATED", "NOT ESTABLISHED", "NOT CHECKED",
                 "NOT VERIFIED", "NOT read", "NOT evaluated", "STANDS"]

print("=" * 74)
print("E2  THE LABEL POPULATION, AND WHAT READS IT")
print("=" * 74)
print()

doc = open(DOC, encoding="utf-8").read()
lines = doc.splitlines()

# ---------------------------------------------------------------------------
# (i) the denominator
# ---------------------------------------------------------------------------
print("-" * 74)
print("(i) THE DENOMINATOR --- every disposition-marked line in the document")
print("-" * 74)
sites = {}
for (i, line) in enumerate(lines, 1):
    hit = [v for v in VOCAB_NAMED + VOCAB_UNNAMED if v in line]
    if hit:
        sites[i] = hit
named_only = {i: h for (i, h) in sites.items()
              if any(v in VOCAB_NAMED for v in h)}
unnamed_only = {i: h for (i, h) in sites.items()
                if not any(v in VOCAB_NAMED for v in h)}
print("   population: the %d lines of %s" % (len(lines), os.path.basename(DOC)))
print("   lines carrying a marker from t5's OWN named vocabulary : %d"
      % len(named_only))
print("   lines carrying only a marker t5's docstring does NOT name : %d"
      % len(unnamed_only))
print("   lines carrying any disposition marker                  : %d"
      % len(sites))
print()

# ---------------------------------------------------------------------------
# (ii) what t5 actually reads
# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) WHICH OF THOSE LINES DOES t5_labels.py READ?")
print("-" * 74)
spec = importlib.util.spec_from_file_location("t5_d330", T5)
t5 = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(t5)
except Exception as exc:                                   # pragma: no cover
    selferr("could not import t5_labels.py: %s" % exc)
    t5 = None

needles = []
if t5 is not None:
    for (sec, label, asserts, checks) in t5.LABELS:
        for check in checks:
            if len(check) == 3:
                for arg in check[2]:
                    if isinstance(arg, str) and arg not in (
                            t5.DOC, t5.T1, t5.O1, t5.RDM, t5.T2, t5.T3,
                            t5.T4, t5.O2, t5.O3, t5.O4, t5.DELIVERED,
                            t5.REPAIR, t5.RETRACT):
                        needles.append(arg)
    for (name, path, old, new, expect) in t5.MUTATIONS:
        needles.append(old)
    print("   t5 declares %d labels and %d checks."
          % (len(t5.LABELS), sum(len(c[3]) for c in t5.LABELS)))
print("   string needles t5 looks for anywhere: %d" % len(needles))
print()
print("   CRITERION, stated so it cannot be read as wider than it is: a marked")
print("   line is REACHED if some t5 needle is a substring of it or of the")
print("   line above or below it (needles span wrapped lines).  A line no")
print("   needle touches is a disposition the label instrument cannot see.")
print()


def reached(i):
    window = "\n".join(lines[max(0, i - 2):i + 1])
    flat = " ".join(window.split())
    for nd in needles:
        f = " ".join(nd.split())
        if len(f) >= 8 and (f in window or f in flat):
            return True
    return False


unreached = sorted(i for i in sites if not reached(i))
print("   marked lines REACHED by at least one t5 needle : %d of %d"
      % (len(sites) - len(unreached), len(sites)))
print("   marked lines NO t5 needle reaches              : %d of %d"
      % (len(unreached), len(sites)))
print()
print("   A LINE IS NOT A LABEL, so an unreached line is not yet a finding: a")
print("   label spans a block, and t5 may reach it through a different line of")
print("   the same block.  Each marked line is therefore assigned to its BLOCK")
print("   (paragraph, or table row), and a block counts as covered if ANY of")
print("   its lines is reached.  Only a marked line in a block t5 reaches")
print("   NOWHERE is a disposition the instrument cannot see.")
print()
blocks = []           # (first_line, last_line)
start = 1
for (i, line) in enumerate(lines, 1):
    if not line.strip():
        if start < i:
            blocks.append((start, i - 1))
        start = i + 1
if start <= len(lines):
    blocks.append((start, len(lines)))


def block_of(i):
    for (a, b) in blocks:
        if a <= i <= b:
            return (a, b)
    return (i, i)


marked_blocks = sorted({block_of(i) for i in sites})
# CORRECTED DURING CONSTRUCTION, and recorded here rather than in a commit
# message.  The first version asked whether any MARKED line of a block was
# reached, which is the wrong question: t5 reaches a label through whatever
# line carries its needle, marked or not.  Two blocks scored dark that t5
# plainly checks (section 3's "are all multiplicity-free" correction and
# section 8's scope correction).  A block is covered if ANY of its lines is
# reached.  The correction moves blocks OUT of the finding, against this
# instrument's interest.
covered_blocks = sorted({(a, b) for (a, b) in marked_blocks
                         if any(reached(i) for i in range(a, b + 1))})
dark_blocks = [b for b in marked_blocks if b not in covered_blocks]
print("   blocks carrying a disposition marker  : %d" % len(marked_blocks))
print("   of those, blocks t5 reaches somewhere : %d" % len(covered_blocks))
print("   blocks t5 reaches NOWHERE             : %d" % len(dark_blocks))
print()
print("   the dark blocks, in document order --- these are the dispositions")
print("   the label instrument does not see at all:")
for (a, b) in dark_blocks:
    marks = sorted({m for i in range(a, b + 1) for m in sites.get(i, [])})
    print("     lines %d-%d   markers %s" % (a, b, marks))
    for i in range(a, b + 1):
        if i in sites:
            print("        %4d  %s" % (i, lines[i - 1].strip()[:92]))
print()
if dark_blocks:
    finding("t5_labels.py is documented, in the delivered document and in its "
            "README, as measuring EVERY disposition label in this document. "
            "%d of the %d disposition-marked BLOCKS are reached by no needle "
            "it looks for. Its population is a hand-written list of %d labels "
            "with no denominator derived from the document, so 'every' is "
            "unmeasured and the count 29 has no population beside it."
            % (len(dark_blocks), len(marked_blocks),
               len(t5.LABELS) if t5 else -1))
print()

# ---------------------------------------------------------------------------
# (iii) the self-referential figures
# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) THE FIGURES THE DOCUMENT PRINTS ABOUT ITS OWN LABEL INSTRUMENT")
print("-" * 74)
print("   These are numbers in the prose about a script in the same commit.")
print("   mg-a318's standing rule for this repo is that a gate must read the")
print("   figure AT THE SITE rather than restate it, and mg-8e30's is that a")
print("   duplicated literal is the defect.  Measured against a live run.")
print()
p = subprocess.run([sys.executable, "-u", "t5_labels.py"], cwd=TARGET_DIR,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
live = p.stdout.decode("utf-8", "replace")
print("   t5_labels.py, run now: exit %d" % p.returncode)


def live_int(pattern):
    m = re.search(pattern, live, re.M)
    return int(m.group(1)) if m else None


LIVE = {
    "labels": live_int(r"^\s*labels checked\s*:\s*(\d+)"),
    "checks": live_int(r"^\s*individual checks\s*:\s*(\d+)"),
    "muts": live_int(r"^\s*corruptions applied\s*:\s*(\d+)"),
}
LIVE["fired"] = len(re.findall(r"^\s*\[fires\]", live, re.M))
print("   live: labels %s, checks %s, corruptions %s, of which firing %s"
      % (LIVE["labels"], LIVE["checks"], LIVE["muts"], LIVE["fired"]))
print()

CLAIMS = [
    (DOC_REL, "29 labels, 100 checks", ("labels", 29), ("checks", 100)),
    (DOC_REL, "**29 of\n   them, 100 checks**", ("labels", 29), ("checks", 100)),
    ("code/branching_locate_db09/README.md", "29 labels, 100 checks",
     ("labels", 29), ("checks", 100)),
    (DOC_REL, "**7-mutation corruption battery**", ("muts", 7), None),
    (DOC_REL, "**All 7 fire.**", ("fired", 7), None),
    (DOC_REL, "**and all 7 fire**", ("fired", 7), None),
    ("code/branching_locate_db09/README.md", "all 7 fire", ("fired", 7), None),
]
print("   every site at which a figure about t5 is RESTATED:")
n_sites = 0
for (relpath, needle, c1, c2) in CLAIMS:
    txt = open(os.path.join(ROOT, relpath), encoding="utf-8").read()
    cnt = txt.count(needle)
    n_sites += cnt
    verdict = []
    for c in (c1, c2):
        if c is None:
            continue
        key, want = c
        verdict.append("%s: stated %d, live %s %s"
                       % (key, want, LIVE[key],
                          "agree" if LIVE[key] == want else "DISAGREE"))
        if LIVE[key] != want:
            finding("%s restates %r but a live run gives %s = %s"
                    % (relpath, needle, key, LIVE[key]))
    print("     %-52s x%d in %s" % (repr(needle)[:52], cnt, relpath))
    for v in verdict:
        print("         %s" % v)
print()
print("   sites at which these figures are written : %d" % n_sites)
print("   sites at which a gate DERIVES them       : 0")
print("     -- no check in t5_labels.py, and nothing in run_all.sh, compares")
print("        the document's stated 29/100/7 to what the script produces.")
print("        The figures are correct today; nothing keeps them correct.")
if n_sites > 1:
    finding("the figures describing t5_labels.py are written at %d sites and "
            "derived at 0: adding or removing one label makes the document "
            "and its README wrong with every gate in the tree still green"
            % n_sites)
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the import of t5_labels.py and the "
      "%d file reads above" % (len(SELF), len(CLAIMS) + 1))
print("FINDINGS: %d, population: the %d disposition-marked lines and the %d "
      "restated figures" % (len(FIND), len(sites), n_sites))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
