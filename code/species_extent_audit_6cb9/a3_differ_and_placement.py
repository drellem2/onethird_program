"""A3 -- "UNDER WHAT CHANGE WOULD THE ANSWER DIFFER?", MADE; AND WHERE EACH
CORRECTION IS PLACED.

Three things the brief asks for and one it does not.

  A3a  For every check this repair touched, the change the code says would
       flip it, MADE, and the answer compared.  The sharpest form is the
       deletion test: put back the defect the repair removed and see whether
       the artifact moves.  An unmeasured "differs under X" is an assertion
       about a check.
  A3b  The C4 anchor multiplicity, which is where my own prediction Q2 missed:
       the anchor a reader reads can be deleted and the check stays green,
       because the same string is written three times into the file the check
       reads.  Measured per anchor and per site.
  A3c  The placement question asked of the repair itself: for each of its five
       fixes, WHERE the false belief lives, and whether the correction is
       reachable FROM THERE.
  A3d  Every threshold this repair set or kept, with the margin the live tree
       leaves it.  A threshold whose margin nobody has measured is a number.

    python3 code/species_extent_audit_6cb9/a3_differ_and_placement.py
"""

import os
import re
import sys

from kern6cb9 import (hdr, REPO, git_status, Probe, run_checker, plant,
                      replace_once)

bad = 0

DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
REPAIR_DOC = "docs/OneThird-Species-Hopf-Monoids-Repair.md"
CHECK_DOC = "code/species_repair_6f61/check_doc.py"
W3 = "code/species_remainder_f8fa/w3_scope.py"
S1 = "code/species_repair_a4ef/s1_extent.py"
S2 = "code/species_repair_a4ef/s2_seam.py"
E1 = "code/species_extent_d633/e1_extents.py"
E2 = "code/species_extent_d633/e2_crosssection.py"
KERN = "code/species_extent_d633/kernd633.py"

PAD = "\n" * 9
X6A_SRC = ("Define a braid cone to be a cone cut out by inequalities of the "
           "form y(i) <= y(j) for i, j in I.")
X4_SRC = "Of the four columns, three are controls, and they fire."
MID_A = ("A duplicate of a middling paragraph, long enough to clear the "
         "sixty-character floor of the said-twice pass but far short of the "
         "three hundred the older sweep needs.")
X7_STRUCK = ('*"Recall from Section 17.4 that `K̄(Π)` is the algebra of '
             'symmetric functions in\nnoncommuting variables and `K(Π)` is '
             'the familiar Hopf algebra of symmetric functions"*')


def payload(body):
    return PAD + "<!-- 6cb9 probe -->\n" + PAD + body.strip() + "\n" + PAD


# The extension filter mg-d633 removed, put back verbatim in shape: an
# extension rule consulted before anything is read, carried by no sentence.
S1_UNDO = (
    "        if not os.path.isfile(p) or f in EXCLUDE:\n"
    "            continue\n",
    "        if not os.path.isfile(p) or f in EXCLUDE:\n"
    "            continue\n"
    "        if os.path.splitext(f)[1] not in (\".py\", \".txt\", \".md\"):\n"
    "            continue\n")
W3_UNDO = (
    "    if not os.path.isfile(os.path.join(SRC, _f)):\n        continue\n",
    "    if not os.path.isfile(os.path.join(SRC, _f)):\n        continue\n"
    "    if os.path.splitext(_f)[1] not in (\".py\", \".txt\", \".md\"):\n"
    "        continue\n")

# id, label, the code's own stated flip condition, the edits, what to run,
# the exit code WITHOUT the change, the predicted exit code WITH it.
FLIPS = [
    ("D1", "s1_extent.py -- the widened scan",
     "'every regular file is read ... there is no extension rule left to "
     "leave out of a sentence'",
     [(S1, replace_once(*S1_UNDO)),
      ("code/species_repair_6f61/run_all.sh",
       plant("\n".join("# " + l for l in payload(X6A_SRC).splitlines())))],
     S1, 1, 0),
    ("D1e", "s1_extent.py -- is the widening GUARDED?",
     "E1b: 'the printed count for each tree is the number of regular files'",
     [(S1, replace_once(*S1_UNDO))], E1, 0, 1),
    ("D2", "w3_scope.py -- the widened scan",
     "'Every regular file is read; anything undecodable is NAMED in the "
     "output rather than dropped by a rule no sentence carries'",
     [(W3, replace_once(*W3_UNDO)),
      ("code/species_7d75/NOTES", lambda _o: payload(X4_SRC))],
     W3, 1, 0),
    ("D2e", "w3_scope.py -- is the widening GUARDED?",
     "E1b: 'reads every regular file in code/species_7d75'",
     [(W3, replace_once(*W3_UNDO))], E1, 0, 1),
    ("D3", "s2_seam.py -- the said-twice pass",
     "'an EXACT duplicate is an exact duplicate at 139 characters, and until "
     "mg-d633 that case exited 0'",
     [(S2, replace_once("REPEAT_RATIO = 0.90", "REPEAT_RATIO = 2.00")),
      (DOC, plant("\n\n" + MID_A + "\n\n" + MID_A + "\n"))],
     S2, 1, 0),
    ("D4", "check_doc.py -- the NARROWED claim",
     "'It reads a SECOND file for section C4's five assertions and for "
     "nothing else'",
     [(CHECK_DOC, replace_once(
         'doc = open(TARGET, encoding="utf-8").read()',
         'doc = open(TARGET, encoding="utf-8").read()\n'
         '_third = open(os.path.join(DOCS, "OneThird-Species-Hopf-Monoids'
         '-Repair.md"), encoding="utf-8").read()\n'
         '_fourth = open(os.path.join(DOCS, "OneThird-Audit-mg-7dd3-Extent'
         '-Repair.md"), encoding="utf-8").read()'))],
     CHECK_DOC, 0, 0),
    ("D4e", "check_doc.py -- is the NARROWED claim GUARDED?",
     "E1b: 'reads exactly two files, and the second is the repair document'",
     [(CHECK_DOC, replace_once(
         'doc = open(TARGET, encoding="utf-8").read()',
         'doc = open(TARGET, encoding="utf-8").read()\n'
         '_fourth = open(os.path.join(DOCS, "OneThird-Audit-mg-7dd3-Extent'
         '-Repair.md"), encoding="utf-8").read()'))],
     E1, 0, 1),
    ("D5", "e2_crosssection.py -- the rule DISARMED",
     "'A run of at least RUN_MIN tokens that is at least RUN_FRAC of the "
     "strike is the claim itself said again'",
     [(KERN, replace_once("RUN_FRAC = 0.50", "RUN_FRAC = 2.00"))],
     E2, 0, 1),
]

hdr("A3a  UNDER WHAT CHANGE WOULD THE ANSWER DIFFER?  THE CHANGE, MADE.")
print("  `without` is the exit code with the planted mutation only.  `with`")
print("  adds the change the code's own sentence says would flip it.  A row")
print("  where `with` == `without` is a sentence nobody has measured.")
print()
print("  %-5s %-44s %-8s %-5s %-5s %s"
      % ("id", "check and the change", "predicted", "w/o", "with", "verdict"))

BASE = git_status()
for pid, label, quoted, edits, runner, without, expect in FLIPS:
    base_edits = [e for e in edits if not e[0].endswith(".py")]
    with Probe(base_edits):
        c0, _ = run_checker(runner)
    with Probe(edits):
        c1, out1 = run_checker(runner)
    if git_status() != BASE:
        print("*** RESTORE FAILED at %s" % pid)
        sys.exit(2)
    ok = (c0 == without and c1 == expect)
    differs = (c0 != c1)
    # D4 is the ONLY row where the answer is expected NOT to differ, and that
    # is the finding, not a pass.  Every other row is a check whose own
    # sentence names a change; if the artifact does not move, the sentence is
    # unmeasured.
    bad += (not ok)
    print("  %-5s %-44s %-8d %-5d %-5d %s"
          % (pid, label[:44], expect, c0, c1,
             ("answer DIFFERS" if differs else "*** ANSWER IS THE SAME ***")
             + ("" if ok else "  *** MISSED ***")))
print()
for pid, label, quoted, edits, runner, without, expect in FLIPS:
    print("  %-5s the code says it flips under: %s" % (pid, quoted[:60]))
    if len(quoted) > 60:
        print("        %s" % quoted[60:])
print()
print("  D4 is the one that matters.  check_doc.py's repair was a CLAIM")
print("  NARROWING -- the sentence changed and no line of code did.  Making")
print("  it read two MORE files changes nothing it prints and nothing it")
print("  exits: the narrowed sentence is unguarded AT ITS OWN SITE.  D4e")
print("  shows it is guarded one layer out, by E1, which is a different")
print("  claim and a weaker one, because E1 lives in the audit instrument")
print("  and check_doc.py's own run_all.sh does not call it.")
print()
print("  D5 is the other one.  Neutering e2's rule so it can never fire")
print("  still exits 1 -- because e2's OWN controls (a)-(e) catch it.  A")
print("  check that goes red when you disarm it is the shape the other four")
print("  do not have.")
print()

# ---------------------------------------------------------------------------
# A3b  the C4 anchors, and how many copies of each the file carries
# ---------------------------------------------------------------------------
hdr("A3b  THE C4 ANCHORS -- A PRESENCE TEST OVER A FILE THAT SAYS IT THRICE")
print("  My prediction Q2 said that deleting C4's `2 of 45` anchor from the")
print("  repair document makes check_doc.py exit 1.  It exited 0, and this")
print("  is why.  KEPT, not retuned: the miss is the finding.")
print()
ANCHORS = [
    ("names its target", "OneThird-Species-Hopf-Monoids-Where-This-Lives"),
    ("names the audit", "mg-a61f"),
    ("names the instrument", "code/species_repair_6f61"),
    ("records the missed predictions", "2 of 45"),
    ("records what it did NOT repair", "WHAT THIS REPAIR DID NOT DO"),
]
rep = open(os.path.join(REPO, REPAIR_DOC), encoding="utf-8").read()
print("  %-34s %-6s %-8s %s" % ("anchor", "copies", "1 site", "all sites"))
multi = 0
for label, s in ANCHORS:
    n = rep.count(s)
    multi += (n > 1)
    with Probe([(REPAIR_DOC, replace_once(s, "XX" + s[2:]))]):
        c1, _ = run_checker(CHECK_DOC)
    with Probe([(REPAIR_DOC, lambda old, s=s: old.replace(s, "XX" + s[2:]))]):
        cn, _ = run_checker(CHECK_DOC)
    print("  %-34s %-6d exit %-3d exit %d   %s"
          % (label, n, c1, cn,
             "ok -- one site is enough" if c1 == 1 else
             "*** DELETING THE SITE A READER READS LEAVES IT GREEN ***"))
if git_status() != BASE:
    print("*** RESTORE FAILED in A3b")
    sys.exit(2)
bad += multi > 0
print()
print("  %d of %d anchors are written more than once into the file the check"
      % (multi, len(ANCHORS)))
print("  reads.  For those, the check is a PRESENCE TEST over the whole")
print("  document, not a check on any site, and the site a reader meets can")
print("  be wrong or gone with the run still green.  mg-8a5c found exactly")
print("  this ('the gate is a presence test'), mg-a318 repaired it in the")
print("  Hodge tree by writing each figure ONCE PER SITE, and mg-835f")
print("  confirmed the repair.  The species tree still has it.")
print()

# ---------------------------------------------------------------------------
# A3c  placement
# ---------------------------------------------------------------------------
hdr("A3c  EVERY FIX IS A CORRECTION.  WHERE DOES THE FALSE BELIEF LIVE?")
print("  A correction that is true and unreachable is the finding this arc")
print("  has produced five times.  For each fix: the artifact a reader or a")
print("  runner meets the false belief IN, and whether the correction is IN")
print("  THAT ARTIFACT -- not merely recorded somewhere true.")
print()
PLACES = [
    ("A1  s1_extent.py's exclusion count",
     "code/species_repair_a4ef/out_s1_extent.txt",
     ["EVERY REGULAR FILE", "mg-d633"],
     "the run's own printed extent, which is where the false count was read"),
    ("A1  w3_scope.py's 'over ONE tree'",
     "code/species_remainder_f8fa/out_w3_scope.txt",
     ["every regular file in it", "no extension rule"],
     "the same"),
    ("A2  s2_seam.py's omitted MIN_CHARS",
     "code/species_repair_a4ef/out_s2_seam.txt",
     ["COMPARED BY NEITHER", "said-twice"],
     "the same"),
    ("C1  check_doc.py's 'ONE FILE'",
     "code/species_repair_6f61/out_check_doc.txt",
     ["SECOND file", "NARROWER than what the code read"],
     "the same"),
    ("B1  the AM §17.5 quotation in §0",
     DOC,
     ["is a\nMISQUOTATION", "310 lines above the §4 strike"],
     "the paragraph in §0 that carried it, 310 lines from the §4 strike"),
]
for label, artifact, needles, why in PLACES:
    p = os.path.join(REPO, artifact)
    text = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
    hits = [n for n in needles if n in text]
    ok = len(hits) == len(needles)
    bad += (not ok)
    print("  %-38s %s" % (label, "reachable AT the site" if ok
                          else "*** NOT AT THE SITE ***"))
    print("        belief lives in : %s" % artifact)
    print("        which is        : %s" % why)
    for n in needles:
        print("        %-46s %s" % ('correction phrase "%s"' % n[:40],
                                    "present" if n in text else "*** ABSENT"))
print()
print("  All five are reachable from where the belief lived.  The one that")
print("  is NOT is the repair's own new check: see A2d -- e2_crosssection.py")
print("  is named in every artifact a READER meets and is called by no")
print("  run_all.sh a RUNNER of the three species trees executes.")
print()

# ---------------------------------------------------------------------------
# A3d  thresholds and the margin the live tree leaves them
# ---------------------------------------------------------------------------
hdr("A3d  EVERY THRESHOLD, AND THE SEAM IT SITS IN")
c, s2out = run_checker(S2)
c, e2out = run_checker(E2)
worst_mid = [int(m) for m in re.findall(
    r"worst pair among the \d+ over 60 chars: (\d+)%", s2out)]
worst_big = [int(m) for m in re.findall(
    r"worst pair among the \d+ over 300 chars: (\d+)%", s2out)]
rows = []
for line in e2out.splitlines():
    m = re.search(r"run\s+(\d+) of\s+(\d+) \(\s*\d+%\)\s+restated at line"
                  r"\s+\S+\s+(below the rule|exonerated|\*)", line)
    if m:
        rows.append((int(m.group(1)), int(m.group(2)), m.group(3)))
minfail = max([r[0] for r in rows if r[0] < 8 and r[0] >= 0.5 * r[1]] or [0])
fracfail = max([r[0] / r[1] for r in rows if r[0] >= 8 and r[0] < 0.5 * r[1]]
               or [0])
exon = [r for r in rows if r[2] == "exonerated"]

print("  %-40s %-10s %s" % ("threshold", "value", "margin in the live tree"))
print("  %-40s %-10s worst live pair over the floor %d%%, so %d points"
      % ("s2 REPEAT_RATIO (said twice)", "0.90", max(worst_mid or [0]),
         90 - max(worst_mid or [0])))
print("  %-40s %-10s worst live pair over 300 chars %d%%, so %d points"
      % ("s2 THRESHOLD (the 45% sweep)", "0.45", max(worst_big or [0]),
         45 - max(worst_big or [0])))
print("  %-40s %-10s what it excludes is PRINTED, one passage per line"
      % ("s2 REPEAT_FLOOR", "60 chars"))
print("  %-40s %-10s no longer an exclusion: the 90%% pass covers below it"
      % ("s2 MIN_CHARS", "300 chars"))
print("  %-40s %-10s closest non-firing run that clears the fraction: %d"
      % ("e2 RUN_MIN", "8 tokens", minfail))
print("  %-40s %-10s closest non-firing fraction at >= 8 tokens: %.0f%%"
      % ("e2 RUN_FRAC", "0.50", 100 * fracfail))
print("  %-40s %-10s %d strike(s) held silent by it alone"
      % ("e2 exoneration (paragraph/table)", "-", len(exon)))
print("  %-40s %-10s not numeric; every hit prints its line"
      % ("kerna4ef exoneration window", "6 lines"))
print("  %-40s %-10s the same" % ("w3 QUOTED_AS_CORRECTED window", "4 lines"))
print()
print("  THE SEAM TO REPORT IS e2's RUN_MIN, AND IT IS TWO TOKENS WIDE.")
print("  mg-d633 states the margin for s2's 90% pass (37 points) and this")
print("  audit reproduces it.  Nobody states this one.  The closest")
print("  non-firing strike in the tree is %d tokens against a floor of 8,"
      % minfail)
print("  and the document B1 lived in carries a SEVEN-token strike.")
print()
SHORT = "as three independent agreements about the term"
n_short = len([w for w in SHORT.split()])
with Probe([(DOC, plant("\n\nFor the record, the reading stands: " + SHORT
                        + ".\n"))]):
    cs, souts = run_checker(E2)
ok = (cs == 0)
bad += (not ok)
print("  SEAM PROBE.  `%s`" % SHORT)
print("  is struck in %s" % DOC)
print("  and is %d tokens.  Restated VERBATIM in another section of that same"
      % n_short)
print("  document, e2 exits %d." % cs)
print("  %-62s %s"
      % ("a verbatim restatement of a 7-token strike is INVISIBLE",
         "CONFIRMED -- silent" if ok else "it fired; the seam is not there"))
print()
print("  e2's EXTENT paragraph names two holes: another document, and a claim")
print("  'restated in different words, at any length'.  It does not name")
print("  this one -- a claim restated in the SAME words, in the SAME")
print("  document, in another section, and invisible because the claim is")
print("  SHORT.  That is an extent line narrower than the code's own")
print("  limitation, in the check written to close an extent finding, and")
print("  the live tree already contains a strike one token below the floor.")
print()

final = git_status()
hdr("A3 TOTAL BAD: %d" % bad)
print("EXTENT OF THIS NUMBER.  %d flip tests, each one running ONE checker"
      % len(FLIPS))
print("twice -- once with the mutation and once with the mutation plus the")
print("change the code's own sentence names -- plus %d anchors probed at one"
      % len(ANCHORS))
print("site and at every site, plus %d placement sites read for the phrases"
      % len(PLACES))
print("their corrections must carry, plus 7 thresholds read out of source and")
print("2 margins measured from live runs.  Worktree %s.  It says NOTHING"
      % ("identical" if final == BASE else "*** DIRTY ***"))
print("about checks this repair did not touch, about flip conditions the code")
print("does NOT state -- an unstated one cannot be tested this way and its")
print("absence is reported instead -- or about whether a correction a reader")
print("CAN reach is one they WILL.")
if final != BASE:
    sys.exit(2)
sys.exit(1 if bad else 0)
