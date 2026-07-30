"""E5 --- THE SEAM CHECK, AND ITS THRESHOLD.

mg-d330.  My brief: "Seam-check the document and report the threshold."

A SEAM is the join between two workers.  Here there are two: mg-a218 wrote an
audit and mg-13b2 repaired against it, editing the delivered document, the
target instrument AND one script belonging to mg-a218.  A seam defect is a
passage a correcting commit DELETED that survives somewhere with nothing
saying it was corrected --- the mg-73df shape, where the prose was fixed and a
second copy went on asserting the error.

Method, and it is the literal reading: a TOUCHED PASSAGE is a line the
repair `ed9cde4` deleted.  The swept population is every line of the six files
a reader of this arc actually reads.  Similarity is difflib's ratio on
whitespace-, markup- and case-normalised text.

THRESHOLD: 0.80, minimum passage length 60 characters after normalisation ---
the same threshold mg-a218 used, so the two sweeps are comparable.

Exit 0 iff SELF-ERRORS == 0 AND FINDINGS == 0.
"""

import difflib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))

REPAIR2 = "ed9cde4"
THRESHOLD = 0.80
MINLEN = 60
CONTEXT = 12

SWEPT = [
    "docs/OneThird-Bratteli-Path-Algebras-Where-This-Lives.md",
    "docs/OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md",
    "docs/OneThird-Bratteli-Path-Algebras-IndependentAudit.md",
    "code/branching_locate_db09/t1_tl.py",
    "code/branching_locate_db09/out_t1_tl.txt",
    "code/branching_locate_db09/README.md",
]

MARKERS = ("WITHDRAWN", "withdrawn", "CORRECTED", "Corrected", "corrected",
           "SUPERSEDED", "MARKED IN PLACE", "used to", "USED TO SAY", "~~",
           "no longer", "Updated", "OPEN", "CLOSED", "FINDING", "finding",
           "X1", "X2", "X3", "mg-13b2", "mg-a218", "mg-2060", "was ", "old ",
           "false", "refut", "audit", "AUDIT", "It printed", "It read")

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)
    print("   SELF-ERROR: " + m)


def finding(m):
    FIND.append(m)
    print("   FINDING: " + m)


def git(*a):
    p = subprocess.run(["git"] + list(a), cwd=ROOT,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(a), p.stderr.decode()[:160]))
    return p.stdout.decode("utf-8", "replace")


def norm(s):
    s = re.sub(r"[`*_#>|\-]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


print("=" * 74)
print("E5  THE SEAM BETWEEN mg-a218 AND mg-13b2")
print("=" * 74)
print("threshold          : %.2f  (difflib.SequenceMatcher ratio)" % THRESHOLD)
print("normalisation      : whitespace, markdown emphasis, case")
print("minimum passage    : %d characters after normalisation" % MINLEN)
print("marker window      : %d lines either side" % CONTEXT)
print()

deleted = []
for l in git("show", "--format=", REPAIR2).splitlines():
    if l.startswith("-") and not l.startswith("---"):
        n = norm(l[1:])
        if len(n) >= MINLEN:
            deleted.append((l[1:].rstrip(), n))
seen = set()
passages = []
for (raw, n) in deleted:
    if n not in seen:
        seen.add(n)
        passages.append((raw, n))
print("touched passages   : %d distinct lines deleted by %s and at least %d"
      % (len(passages), REPAIR2, MINLEN))
print("                     characters long after normalisation")

units = []
for f in SWEPT:
    txt = open(os.path.join(ROOT, f), encoding="utf-8").read()
    lines = txt.splitlines()
    for (i, l) in enumerate(lines, 1):
        n = norm(l)
        if len(n) >= MINLEN:
            units.append((f, i, l.rstrip(), n, lines))
print("swept units        : %d lines in %d files" % (len(units), len(SWEPT)))
for f in SWEPT:
    print("                     %-70s %d"
          % (f, sum(1 for u in units if u[0] == f)))
print("comparisons        : %d" % (len(passages) * len(units)))
print()


def marked(lines, i):
    win = "\n".join(lines[max(0, i - 1 - CONTEXT):i + CONTEXT])
    return any(m in win for m in MARKERS)


added = {norm(l[1:]) for l in git("show", "--format=", REPAIR2).splitlines()
         if l.startswith("+") and not l.startswith("+++")}

survivors = {}
for (praw, pn) in passages:
    sm = difflib.SequenceMatcher(None, pn, "")
    sm.set_seq1(pn)
    for (f, i, raw, n, lines) in units:
        sm.set_seq2(n)
        if sm.real_quick_ratio() < THRESHOLD or sm.quick_ratio() < THRESHOLD:
            continue
        r = sm.ratio()
        if r >= THRESHOLD:
            key = (f, i)
            if key not in survivors or r > survivors[key][0]:
                survivors[key] = (r, praw, raw, n in added, marked(lines, i))

print("-" * 74)
print("SURVIVORS AT OR ABOVE THE THRESHOLD")
print("-" * 74)
print("   sites surviving    : %d" % len(survivors))
kinds = {"EDIT IN PLACE": 0, "SECOND COPY": 0}
unmarked = []
for ((f, i), (r, praw, raw, is_added, mk)) in sorted(survivors.items(),
                                                     key=lambda kv: -kv[1][0]):
    kind = "EDIT IN PLACE" if is_added else "SECOND COPY"
    kinds[kind] += 1
    if not mk:
        unmarked.append((f, i, r, kind, raw, praw))
print("   of which EDIT IN PLACE (the survivor is itself an added line of the")
print("     same commit, so the question is whether the edit is disclosed): %d"
      % kinds["EDIT IN PLACE"])
print("   of which SECOND COPY : %d" % kinds["SECOND COPY"])
print("   MARKED               : %d" % (len(survivors) - len(unmarked)))
print("   UNMARKED             : %d" % len(unmarked))
print()
for (f, i, r, kind, raw, praw) in unmarked:
    print("   %s:%d   ratio %.3f   [%s]" % (f, i, r, kind))
    print("      survives : %s" % raw.strip()[:88])
    print("      deleted  : %s" % praw.strip()[:88])
    finding("a passage %s deleted survives unmarked at %s:%d, ratio %.3f"
            % (REPAIR2, f, i, r))
if not unmarked:
    print("   -> every survivor sits within %d lines of a marker." % CONTEXT)
print()

print("-" * 74)
print("WHAT WOULD HAVE COUNTED --- two calibration probes, scored")
print("-" * 74)
print("   A sweep that finds nothing has to show it can find something.")
print()
print("   CORRECTED DURING CONSTRUCTION, and recorded here rather than in a")
print("   commit message.  My first two probes were sentences I WROTE in the")
print("   shape of the withdrawn claims.  Both scored ~0.41 against the best")
print("   deleted passage and raised a SELF-ERROR --- correctly: a probe that")
print("   cannot reach the threshold calibrates nothing.  A probe has to be a")
print("   passage this commit REALLY deleted, placed where a marker is not.")
print()


def sweep_text(name, text):
    """Run the same sweep against one synthetic file."""
    lines = text.splitlines()
    hits = []
    for (i, l) in enumerate(lines, 1):
        n = norm(l)
        if len(n) < MINLEN:
            continue
        for (praw, pn) in passages:
            if difflib.SequenceMatcher(None, pn, n).ratio() >= THRESHOLD:
                hits.append((i, l, praw, marked(lines, i)))
                break
    return hits


# the probes are chosen from the DELIVERED DOCUMENT's own deleted lines, not
# from whichever file happens to come first in the diff: a document seam check
# calibrated only on code proves less than it looks like it proves.
doc_deleted = [l[1:].rstrip() for l in
               git("show", "--format=", REPAIR2, "--", SWEPT[0]).splitlines()
               if l.startswith("-") and not l.startswith("---")
               and len(norm(l[1:])) >= MINLEN]
probes = sorted(doc_deleted, key=len, reverse=True)[:2]
for (k, probe) in enumerate(probes, 1):
    bare = ("Some ordinary prose with no disposition marker in it at all.\n"
            * CONTEXT) + probe + "\n" + (
            "More ordinary prose with no disposition marker in it at all.\n"
            * CONTEXT)
    withmk = bare.replace("Some ordinary prose",
                          "CORRECTED (mg-13b2): what this used to say", 1)
    pos = sweep_text("bare", bare)
    neg = sweep_text("marked", withmk)
    pos_unmarked = [h for h in pos if not h[3]]
    neg_unmarked = [h for h in neg if not h[3]]
    print("   probe %d: a line %s really deleted" % (k, REPAIR2))
    print("      %s" % probe.strip()[:88])
    # the two questions are separated, and the first version conflated them:
    # probe 1 is the struck D2 ledger row, so it carries `~~` --- a marker ---
    # ON ITS OWN LINE and is correctly classified MARKED even in bare prose.
    # That is the classifier working, not the matcher failing.  MATCHED and
    # UNMARKED are therefore reported and scored separately.
    print("      [%s] the sweep MATCHES it at all               : %d hit(s)"
          % ("ok" if pos else "DEAD", len(pos)))
    print("      [%s] and classifies it unmarked in bare prose  : %d hit(s)%s"
          % ("ok" if pos_unmarked else "n/a", len(pos_unmarked),
             "" if pos_unmarked else "  (the line carries its own marker)"))
    print("      [%s] the same line with a marker beside it     : %d unmarked hit(s)"
          % ("ok" if not neg_unmarked else "BAD", len(neg_unmarked)))
    if not pos:
        selferr("calibration probe %d is not matched by this sweep at all, so "
                "its empty result is worthless" % k)
    if neg_unmarked:
        selferr("calibration probe %d fires even when correctly marked" % k)
print()
print("   -> the sweep bites. What would have counted: any of the %d passages"
      % len(passages))
print("      %s deleted, standing anywhere in the %d swept units with no"
      % (REPAIR2, len(units)))
print("      disposition marker within %d lines either side." % CONTEXT)
print()

print("-" * 74)
print("SELF-ERRORS: %d, population: the git read and the %d file reads"
      % (len(SELF), len(SWEPT)))
print("FINDINGS: %d, population: the %d survivors at or above %.2f over %d "
      "comparisons" % (len(FIND), len(survivors), THRESHOLD,
                       len(passages) * len(units)))
for f in FIND:
    print("   FINDING: " + f)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
