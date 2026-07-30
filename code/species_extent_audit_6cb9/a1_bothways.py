"""A1 -- ALL FOUR EXTENTS, RE-MEASURED FROM BOTH SIDES, AT MY OWN SITES.

mg-7dd3 found two of four printed extents WIDER than what the code reads.
mg-d633 repaired those two and measured all five checkers both ways.  The
brief for this audit is explicit: do NOT check only the two, because the
repair may leave a third that nobody measured, and it may WIDEN AN EXTENT
WHILE FIXING IT.  So every probe here is at a site of my choosing, and the
sites are chosen to be ones mg-d633's E3 did not touch:

  * a `run_all.sh` in a tree E3 did not plant one in;
  * an EXTENSIONLESS file, because the repaired sentence is now the strong
    "EVERY REGULAR FILE" and an extension filter is exactly what was removed;
  * a committed `out_*.txt`, which s1's extent explicitly says is NOT skipped;
  * a SUBDIRECTORY of a named tree -- the one shape of "regular file in the
    tree" that neither repaired scan reaches, because both use a
    non-recursive `os.listdir` and `continue` past anything that is not a
    file, by a rule no sentence carries;
  * a 45%-similar long passage, because all three of E3's s2 IN-probes are
    EXACT duplicates and therefore all three fire on the 90% pass mg-d633
    added -- leaving the 45% sweep, the ORIGINAL threshold, exercised by no
    probe in that instrument.

Every probe mutates the REAL worktree and restores it; `git status
--porcelain` is compared before and after and the run aborts if it differs.

    python3 code/species_extent_audit_6cb9/a1_bothways.py
"""

import difflib
import os
import re
import sys

from kern6cb9 import (hdr, REPO, git_status, Probe, run_checker, plant,
                      replace_once, flat)

bad = 0

DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
REPAIR_DOC = "docs/OneThird-Species-Hopf-Monoids-Repair.md"
OTHER_DOC = "docs/OneThird-Audit-mg-7dd3-Extent-Repair.md"

CHECK_DOC = "code/species_repair_6f61/check_doc.py"
W3 = "code/species_remainder_f8fa/w3_scope.py"
S1 = "code/species_repair_a4ef/s1_extent.py"
S2 = "code/species_repair_a4ef/s2_seam.py"
E2 = "code/species_extent_d633/e2_crosssection.py"
E1 = "code/species_extent_d633/e1_extents.py"

PAD = "\n" * 9


def payload(body, marker="6cb9 probe"):
    """A planted block, padded well clear of every exoneration window in this
    arc: kerna4ef's is 6 lines, w3_scope's is 4, e2's is the paragraph.  The
    marker names only this ticket, and no exoneration rule in the repository
    matches `mg-6cb9`."""
    return PAD + "<!-- %s -->\n" % marker + PAD + body.strip() + "\n" + PAD


# The source-code forms.  These are the patterns the checkers search for, in
# their own spelling: `stricken_a4ef.py` matches `y(i) <= y(j)` in ASCII, not
# the document's `≤`.  Each avoids its own row's exoneration regex.
X1_SRC = ("Smallest witness with AC(P) != Pi[n]: P = {a<c, b<d}, where ad|bc "
          "has a 2-cycle.")
X3_SRC = ("T5 passes every Hopf-monoid axiom with 0 failures on 4399 basis "
          "elements.")
X4_SRC = "Of the four columns, three are controls, and they fire."
X5_SRC = "Control (ii) measures how differently the two sides behave."
X6A_SRC = ("Define a braid cone to be a cone cut out by inequalities of the "
           "form y(i) <= y(j) for i, j in I.")
X7_SRC = ("Recall from Section 17.4 that Kbar(Pi) is the algebra of symmetric "
          "functions in noncommuting variables.")

# The document forms, for the probes against `check_doc.py`, which matches the
# flattened document sentence rather than a regex.
X6A_DOC = ("Define a braid cone to be a cone in `(ℝ^I)/ℝ^I` cut out "
           "by inequalities of the form `y(i) ≤ y(j)` for `i, j ∈ "
           "I`")

PROBES = []


def probe(pid, checker, direction, what, expect, edits, extra=None):
    PROBES.append((pid, checker, direction, what, expect, edits, extra))


# ---------------------------------------------------------------------------
# check_doc.py -- "over ONE FILE ... a SECOND file for section C4's five
# assertions and for nothing else ... It reads no code."
# ---------------------------------------------------------------------------
probe("Q0a", CHECK_DOC, "-", "unmutated", 0, [])
probe("Q1", CHECK_DOC, "IN", "un-strike X6b (`y(i) <= y(j)`) in the document",
      1, [(DOC, replace_once(
          "§12 defines a braid cone by ~~`y(i) ≤ y(j)`~~",
          "§12 defines a braid cone by `y(i) ≤ y(j)`"))])
probe("Q2", CHECK_DOC, "IN", "delete C4's `2 of 45` anchor from the repair doc",
      1, [(REPAIR_DOC, replace_once("2 of 45", "two of forty-five"))])
probe("Q3", CHECK_DOC, "OUT", "X6a asserted live in a THIRD docs/*.md",
      0, [(OTHER_DOC, plant(payload(X6A_DOC)))])
probe("Q4", CHECK_DOC, "OUT", "X6a asserted live in code/species_7d75",
      0, [("code/species_7d75/README.md", plant(payload(X6A_DOC)))])
probe("Q5", CHECK_DOC, "OUT",
      "an un-struck X1 in the repair doc, away from C4 -- 'and for nothing else'",
      0, [(REPAIR_DOC, plant(payload(X1_SRC)))])

# ---------------------------------------------------------------------------
# w3_scope.py -- "X4 and X5 plus the character-ring rule, over ONE tree: N
# file(s), every regular file in it, with no extension rule"
# ---------------------------------------------------------------------------
probe("Q0b", W3, "-", "unmutated", 0, [])
probe("Q6", W3, "IN", "X5 in a committed out_*.txt in species_7d75",
      1, [("code/species_7d75/out_t5_hopf_monoid.txt", plant(payload(X5_SRC)))])
probe("Q7", W3, "IN", "X4 in a NEW EXTENSIONLESS file species_7d75/NOTES",
      1, [("code/species_7d75/NOTES", lambda _o: payload(X4_SRC))])
probe("Q8", W3, "OUT", "X5 in species_remainder_f8fa -- another tree",
      0, [("code/species_remainder_f8fa/README.md", plant(payload(X5_SRC)))])
probe("Q9", W3, "OUT", "X7 -- not on w3's two-item list -- in species_7d75",
      0, [("code/species_7d75/README.md", plant(payload(X7_SRC)))])
probe("Q10", W3, "WIDE", "X4 in species_7d75/sub/leak.md -- a SUBDIRECTORY",
      0, [("code/species_7d75/sub/leak.md", lambda _o: payload(X4_SRC))])

# ---------------------------------------------------------------------------
# s1_extent.py -- "11 corrections over the document and 4 code trees, EVERY
# REGULAR FILE of each, less the 5 named above and the N named as undecodable"
# ---------------------------------------------------------------------------
probe("Q0c", S1, "-", "unmutated", 0, [])
probe("Q11", S1, "IN", "X6a in species_repair_6f61/run_all.sh",
      1, [("code/species_repair_6f61/run_all.sh",
           plant("\n".join("# " + l for l in payload(X6A_SRC).splitlines())))])
probe("Q12", S1, "IN", "X1 in a NEW EXTENSIONLESS species_repair_a4ef/NOTES",
      1, [("code/species_repair_a4ef/NOTES", lambda _o: payload(X1_SRC))])
probe("Q13", S1, "IN", "X4 in a committed out_*.txt -- 'NOT skipped'",
      1, [("code/species_7d75/out_t5_hopf_monoid.txt", plant(payload(X4_SRC)))])
probe("Q14", S1, "OUT", "X1 in a NAMED exclusion (a4ef/PREDICTIONS.md)",
      0, [("code/species_repair_a4ef/PREDICTIONS.md", plant(payload(X1_SRC)))])
probe("Q15", S1, "OUT", "X1 in code/species_extent_d633 -- a disclaimed tree",
      0, [("code/species_extent_d633/README.md", plant(payload(X1_SRC)))])
probe("Q16", S1, "OUT", "X1 in docs/ other than the one document",
      0, [(OTHER_DOC, plant(payload(X1_SRC)))])
probe("Q17", S1, "WIDE", "X3 in species_7d75/sub/leak.md -- a SUBDIRECTORY",
      0, [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC))])
probe("Q18", S1, "IN", "a non-UTF-8 file added to species_7d75",
      0, [("code/species_7d75/blob.bin", lambda _o: b"\xff\xfe\x00\x01probe")],
      extra=("blob.bin", "the undecodable list NAMES it"))
probe("Q17e", E1, "WIDE",
      "with Q17's subdirectory in place, does E1 say the extent is true?",
      0, [("code/species_7d75/sub/leak.md", lambda _o: payload(X3_SRC))])

# ---------------------------------------------------------------------------
# s2_seam.py -- passages, two passes, and what neither compares
# ---------------------------------------------------------------------------
LONG_A = (
    "The measured coincidence between the two towers is recorded here as a "
    "coincidence and nothing more, because the construction that would make "
    "it a theorem has not been carried out in this document and no reader "
    "should take the table below as evidence that it has been. Every entry "
    "in it was produced by the same enumeration and shares that enumeration's "
    "assumptions about the ground field and about the ordering conventions.")
LONG_B = (
    "The measured coincidence between the two towers is recorded here as a "
    "coincidence and nothing more, because the argument that would make "
    "it a theorem has not been attempted in this section and no auditor "
    "should read the diagram below as evidence that it has. Each cell "
    "in it came out of a different enumeration and carries that program's "
    "own choices about the base ring and about the labelling conventions.")
MID_A = ("A duplicate of a middling paragraph, long enough to clear the "
         "sixty-character floor of the said-twice pass but far short of the "
         "three hundred the older sweep needs.")
MID_B = ("A duplicate of a middling paragraph, wide enough to clear the "
         "sixty-character floor of the repeated pass but well short of the "
         "three hundred the earlier sweep wants.")
SHORT_A = "A short line that is compared to nothing at all."
TABLE_ROW = "| a probe row | duplicated verbatim | for mg-6cb9 |"
HEADING = "#### A probe heading duplicated verbatim"


def two_blocks(a, b):
    return "\n\n" + a + "\n\n" + b + "\n"


probe("Q0d", S2, "-", "unmutated", 0, [])
probe("Q19", S2, "IN", "a 60-300 char PROSE paragraph duplicated verbatim",
      1, [(DOC, plant(two_blocks(MID_A, MID_A)))])
probe("Q20", S2, "IN",
      "a >300 char paragraph pair at 45-90% -- the 45% sweep ALONE",
      1, [(DOC, plant(two_blocks(LONG_A, LONG_B)))])
probe("Q21", S2, "OUT", "a HEADING duplicated verbatim",
      0, [(DOC, plant(two_blocks(HEADING, HEADING)))])
probe("Q22", S2, "OUT", "a <=60 char passage duplicated verbatim",
      0, [(DOC, plant(two_blocks(SHORT_A, SHORT_A)))],
      # The needle here was `compared by neither` in the first version of
      # this file: the run prints that header in CAPITALS, so Q22 read
      # *** NOT NAMED *** against a run that names the passage twice.  My
      # defect, kept in OUTCOMES.md.  Corrected to the PASSAGE ITSELF rather
      # than to the header, because the header prints whether or not any
      # passage is under the floor and a needle that is always present tests
      # nothing -- which is the presence-test defect this arc found in
      # mg-8a5c, committed by the file auditing it.
      extra=("a short line that is compared to nothing",
             "it is LISTED, one per line"))
probe("Q23", S2, "OUT", "a 60-300 char pair at 45-90%, not 90%+",
      0, [(DOC, plant(two_blocks(MID_A, MID_B)))])
probe("Q24", S2, "OUT", "a TABLE ROW duplicated verbatim",
      0, [(DOC, plant(two_blocks(TABLE_ROW, TABLE_ROW)))])


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------
def norm_s2(s):
    s = re.sub(r"[*`~>|#]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


hdr("A1a  THE SIMILARITY OF THE s2 PROBE PAIRS, MEASURED BEFORE THEY RUN")
print("  A probe that claims to sit between two thresholds and does not is a")
print("  probe about nothing.  difflib.SequenceMatcher on the normalised text,")
print("  which is exactly what s2_seam.py compares:")
print()
for label, a, b in [("Q19  MID_A vs MID_A", MID_A, MID_A),
                    ("Q20  LONG_A vs LONG_B", LONG_A, LONG_B),
                    ("Q23  MID_A vs MID_B", MID_A, MID_B)]:
    r = difflib.SequenceMatcher(None, norm_s2(a), norm_s2(b)).ratio()
    la, lb = len(norm_s2(a)), len(norm_s2(b))
    print("  %-24s %3d and %3d normalised chars, %.1f%% similar"
          % (label, la, lb, 100 * r))
print()
print("  s2_seam.py's floors: 60 chars for the 90% said-twice pass, 300 for")
print("  the 45% sweep.  Q20 is the only probe in EITHER instrument that is")
print("  above 300 and below 90%, so it is the only one that can fire on the")
print("  45% sweep alone.")
print()

hdr("A1b  EVERY PROBE, PREDICTED EXIT FIRST")
print("  `exp` was written into PREDICTIONS.md before any of this ran.")
print("  IN  = inside what the printed extent claims -> must FIRE (exit 1).")
print("  OUT = outside it                            -> must be SILENT (0).")
print("  WIDE= a site the printed extent CLAIMS and I predicted the code")
print("        does not read.  A WIDE row whose `got` is 0 is a false extent.")
print()
print("  %-6s %-20s %-4s %-52s %-4s %-4s %s"
      % ("id", "checker", "dir", "mutation", "exp", "got", "verdict"))

BASE = git_status()
results = {}
outputs = {}
for pid, checker, direction, what, expect, edits, extra in PROBES:
    with Probe(edits):
        code, out = run_checker(checker)
    after = git_status()
    if after != BASE:
        print("\n*** THE RESTORE DID NOT RESTORE -- stopping.  probe %s" % pid)
        print(after)
        sys.exit(2)
    results[pid] = code
    outputs[pid] = out
    ok = (code == expect)
    if direction == "WIDE":
        verdict = "extent TRUE here" if code == 1 else "*** EXTENT WIDER ***"
    else:
        verdict = "as predicted" if ok else "*** MISSED ***"
        bad += (not ok)
    print("  %-6s %-20s %-4s %-52s %-4d %-4d %s"
          % (pid, os.path.basename(checker), direction, what[:52], expect,
             code, verdict))
print()
print("  The WIDE rows are scored separately and do NOT count into A1 TOTAL")
print("  BAD: their predicted value IS the defect, so counting a matched")
print("  prediction as a pass would book a false extent as a clean result.")
print("  They are reported in A1d.")
print()

hdr("A1c  PER CHECKER, BOTH DIRECTIONS, WHICH IS THE DELIVERABLE")
print("  This audit is about extents, so its own findings name theirs.")
print()
for checker in [CHECK_DOC, W3, S1, S2]:
    rows = [p for p in PROBES if p[1] == checker]
    base = [p for p in rows if p[2] == "-"]
    ins = [p for p in rows if p[2] == "IN"]
    outs = [p for p in rows if p[2] == "OUT"]
    wides = [p for p in rows if p[2] == "WIDE"]
    nin = sum(1 for p in ins if results[p[0]] == p[4])
    nout = sum(1 for p in outs if results[p[0]] == p[4])
    bl = "clean" if all(results[p[0]] == 0 for p in base) else "*** NOT CLEAN"
    print("  %-14s baseline %s | INSIDE %d/%d fired | OUTSIDE %d/%d silent%s"
          % (os.path.basename(checker), bl, nin, len(ins), nout, len(outs),
             " | %d WIDE site(s) NOT READ" % sum(
                 1 for p in wides if results[p[0]] == 0) if wides else ""))
    print("       sites IN : %s" % "; ".join(p[3][:60] for p in ins))
    print("       sites OUT: %s" % "; ".join(p[3][:60] for p in outs))
    for p in wides:
        print("       site WIDE: %s -> exit %d" % (p[3][:60], results[p[0]]))
print()

hdr("A1d  THE WIDE SITES -- a claimed region the code does not read")
wide_bad = 0
for pid, checker, direction, what, expect, edits, extra in PROBES:
    if direction != "WIDE":
        continue
    got = results[pid]
    fired = got == 1
    if not fired:
        wide_bad += 1
    print("  %-6s %-20s %s" % (pid, os.path.basename(checker), what))
    print("         exit %d -- %s" % (got, "fired, the extent is true here"
                                      if fired else
                                      "SILENT.  The printed extent claims "
                                      "this file and no pass reads it."))
print()
if wide_bad:
    print("  %d WIDE site(s) are silent.  Both repaired scans read" % wide_bad)
    print("  `os.listdir(root)` and `continue` past anything that is not")
    print("  `os.path.isfile`.  A directory is therefore dropped BY A RULE NO")
    print("  SENTENCE CARRIES -- word for word the defect mg-d633 removed one")
    print("  layer up, and the printed sentence is now STRONGER than the one")
    print("  that was false: 'EVERY REGULAR FILE in each tree is read -- there")
    print("  is no extension rule'.  The undecodable list is printed 'one by")
    print("  one, as it is found, so it cannot grow unseen'; a subdirectory")
    print("  grows unseen.  Today no tree under code/species_* has one, so")
    print("  the sentence is true BY ACCIDENT OF THE TREE and nothing makes")
    print("  it fail on the day it stops being.")
print()

hdr("A1e  THE TWO PROBES WHOSE ANSWER IS NOT AN EXIT CODE")
for pid, checker, direction, what, expect, edits, extra in PROBES:
    if not extra:
        continue
    needle, claim = extra
    seen = needle in outputs[pid]
    ok = seen
    bad += (not ok)
    print("  %-6s %-40s %s" % (pid, claim, "ok -- '%s' appears in the run"
                               % needle if ok else "*** NOT NAMED ***"))
print()
print("  Q18: a file that cannot be decoded must be NAMED, not filtered.")
print("  Q22: a passage compared by neither pass must be PRINTED, not")
print("  counted.  Both are the same claim -- an exclusion that is not")
print("  enumerated can grow -- and both are the claim mg-d633 shipped.")
print()

hdr("A1g  DID THE REPAIR NARROW THE CLAIM OR WIDEN THE CODE, AND DOES IT SAY?")
print("  A silent narrowing reads as a fix and is a reduction in coverage.")
print("  For each of the four, what the repair did, and whether the artifact")
print("  a reader meets SAYS which.")
print()
KINDS = [
    ("s1_extent.py", "CODE WIDENED",
     "code/species_repair_a4ef/out_s1_extent.txt",
     ["EVERY REGULAR FILE", "there is no extension rule"],
     "code/species_repair_a4ef/s1_extent.py",
     ["THE CODE WAS WIDENED, NOT THE CLAIM NARROWED"]),
    ("w3_scope.py", "CODE WIDENED",
     "code/species_remainder_f8fa/out_w3_scope.txt",
     ["every regular file in it", "no extension rule"],
     "code/species_remainder_f8fa/w3_scope.py",
     ["THE CODE IS WIDENED, not the claim"]),
    ("s2_seam.py", "CODE WIDENED",
     "code/species_repair_a4ef/out_s2_seam.txt",
     ["said-twice", "COMPARED BY NEITHER"],
     "code/species_repair_a4ef/s2_seam.py",
     ["THE CODE WAS WIDENED, NOT THE CLAIM NARROWED"]),
    ("check_doc.py", "CLAIM NARROWED",
     "code/species_repair_6f61/out_check_doc.txt",
     ["NARROWER than what the code read", "SECOND file"],
     "code/species_repair_6f61/check_doc.py",
     ["NARROWER than what the code read"]),
]
for name, kind, out_rel, out_needles, src_rel, src_needles in KINDS:
    o = open(os.path.join(REPO, out_rel), encoding="utf-8").read()
    sfile = open(os.path.join(REPO, src_rel), encoding="utf-8").read()
    in_out = all(n in o for n in out_needles)
    in_src = all(n in sfile for n in src_needles)
    ok = in_out and in_src
    bad += (not ok)
    print("  %-14s %-14s committed output: %-8s source: %s"
          % (name, kind, "says so" if in_out else "*** SILENT ***",
             "says so" if in_src else "*** SILENT ***"))
print()
print("  Three widened the code and one narrowed the claim, and all four say")
print("  which, in the run a reader reads AND in the source.  The one that")
print("  narrowed is check_doc.py, and A3's D4 measures what that costs: a")
print("  narrowed sentence with no code behind it is guarded by nothing at")
print("  its own site.")
print()

hdr("A1f  THE SANDBOX SEAM mg-d633's OWN E3 RUNS IN")
code, out = run_checker(S1)
live_ctl = [l for l in out.splitlines() if "git unavailable" in l]
print("  Run here, in the real worktree, s1_extent.py's controls (a) and (b)")
print("  are ARMED: %d 'git unavailable' line(s) in this run." % len(live_ctl))
sandbox_note = os.path.join(REPO, "code/species_extent_d633/kernd633.py")
src = open(sandbox_note, encoding="utf-8").read()
copies_git = ".git" in src
print("  kernd633.sandbox() copies docs/ and the named trees; it mentions")
print("  `.git`: %s.  So in every one of E3's 28 probes those two controls"
      % ("yes" if copies_git else "NO"))
print("  take their `git archive` failure branch and print 'SKIPPED, and this")
print("  line is the record that it was not run' -- and since s1_extent.py")
print("  does `bad += ctl`, two of its four controls contribute nothing to")
print("  any exit code E3 recorded.  E3's table does not carry that.")
ok = (len(live_ctl) == 0 and not copies_git)
bad += (not ok)
print("  %-62s %s" % ("controls armed here AND absent from the d633 sandbox",
                      "ok" if ok else "*** NOT AS DESCRIBED ***"))
print()

final = git_status()
hdr("A1 TOTAL BAD: %d" % bad)
print("EXTENT OF THIS NUMBER.  %d probes over 5 checkers, each ONE mutation"
      % len(PROBES))
print("applied to THE REAL WORKTREE and undone, with `git status --porcelain`")
print("compared before and after every one of them (%s).  It counts a probe"
      % ("identical" if final == BASE else "*** DIFFERENT ***"))
print("as bad when its exit code differs from the prediction written before")
print("the run -- EXCEPT the WIDE rows, whose prediction is the defect and")
print("which are reported separately in A1d.  It says NOTHING about")
print("mutations nobody planted, about more than one mutation at a time,")
print("about any statement not in `stricken_a4ef.py`, or about whether these")
print("checkers' RULES are right -- only about whether the region each one")
print("PRINTS as its extent is the region it reads.  Each probe's site is")
print("named above so a successor can see which regions were never touched:")
print("no probe here plants inside `docs/OneThird-Species-Hopf-Monoids-")
print("Repair.md`'s C4 anchors other than Q2, none tests a checker against a")
print("mutation of its own source, and none tests two trees at once.")
if final != BASE:
    print()
    print("*** THE WORKTREE IS NOT AS IT WAS FOUND ***")
    sys.exit(2)
sys.exit(1 if bad else 0)
