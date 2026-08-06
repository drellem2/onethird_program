"""mg-18dc / V7 -- WHAT THIS INSTRUMENT GETS WRONG.

mg-03d1 recorded seven defects of its own instrument, three of them the very
defect it was auditing.  mg-ec63 recorded twelve.  Neither number is a
confession; both are the only reason to believe the other numbers.

This section is the same in kind and it is written to be read against a
specific risk the brief names: **does the deliverable reproduce its own defect
class in new code?**  For this audit that means -- does anything here count a
population containing the counter, consume an artifact the same run produced,
or print a green row over an empty set?

Exit code = defects of this instrument.
"""

import os
import re
import subprocess
import sys

import lib18dc as B

print("mg-18dc / V7 -- DEFECTS OF THIS INSTRUMENT")
print("HEAD: %s" % B.head())

DEFECTS = []


def d(tag, what, caught_by, cost):
    DEFECTS.append((tag, what, caught_by, cost))


d("SD1", "a selftest row whose NAME was the opposite of its MEASUREMENT: "
        "`a probe reading a transcript THIS RUN emptied is caught`, asserting "
        "that nothing was caught",
  "reading my own selftest output after it went green",
  "none on the numbers -- the fixture builds the STALE case and the assertion "
  "was right; the row name was wrong, which is a standing target of this brief")
d("SD2", "a selftest assertion that COULD NOT FAIL on the property it named: "
        "`A and B or A` makes B unreachable, so `the child's read carries its "
        "own pid` was never tested",
  "re-reading the boolean after it went green",
  "none measured -- split into two assertions, both of which pass")
d("SD3", "THE POPULATION CONTAINS THE COUNTER.  `code/idiom_sweep_audit_18dc` "
        "is a `code/*/run_all.sh` the moment this directory has a runner, so "
        "every HEAD-relative count in V6 includes me",
  "by construction -- it is this arc's recurring defect and it is the third "
  "audit in a row to hit it",
  "V6's totals are printed with and against my own membership, below")
d("SD4", "THE READ SHIM IS BLIND TO A NON-PYTHON READER.  `sys.addaudithook` "
        "sees `open` inside a Python process only; a `cat`, an `awk` or a "
        "`grep` in a runner reads a transcript invisibly",
  "knowing what the hook is",
  "unmeasured, and it biases V3 DOWN -- every V3 count is a lower bound")
d("SD5", "THE STUB CHANGES WHAT THE SHELL DOES.  Replacing `python3` with a "
        "0-exit stub means every `&&`, every `set -e` and every `if` in a "
        "runner takes the success branch.  A runner whose truncation sits "
        "behind a failure branch is not measured",
  "reasoning about the stub rather than about the arc",
  "biases V2 DOWN for failure-path truncation and UP for nothing: a step the "
  "stub reaches that the real run would not still truncated the file when I "
  "watched it")
d("SD6", "V3 RUNS THE ARC FOR REAL AND THE ARC'S PROBES RUN EACH OTHER.  A "
        "probe of tree X that executes tree Y's runner inside X's measurement "
        "window contaminates neither count -- reads are filtered by directory "
        "-- but it does consume X's wall clock and can push X into the timeout",
  "mg-ec63's SD6d, read before this instrument was written",
  "unmeasured; it is a mechanism by which the %d-second timeout kills more "
  "trees than the tree's own work would")
d("SD12", "THIS SUITE'S OWN V4 TRANSCRIPT WAS DESTROYED BY THIS SUITE, and "
         "what was left was a 19-BYTE FILE CONTAINING THE STUB'S MARKER -- a "
         "vacuous pass of exactly this ticket's shape, produced by the audit "
         "for it.  `run_all.sh` exports `V18_WORK`; the arc's runners inherit "
         "the environment; this directory became a `code/*/run_all.sh` the "
         "moment it had a runner, so V6's sweep of HEAD RAN MY OWN RUNNER, "
         "which redirected `$V18_WORK/out_v4_outcomes.txt` while V4 was "
         "writing it.  THE RE-ENTRANCY GUARD DID NOT FIRE: `V18_RUNNING` is "
         "set by `run_all.sh`, and the collision came from a probe invoked "
         "DIRECTLY.  A GUARD ON THE RUNNER DOES NOT PROTECT A PROBE",
  "the transcript being 19 bytes long -- not by any check in this suite",
  "V4 was re-run from nothing.  Repaired STRUCTURALLY rather than with a "
  "second guard, the way mg-ec63 repaired its own (c1bb466): everything this "
  "suite executes now gets its own throwaway `$V18_WORK` under `$WORK/child/`, "
  "so the collision path no longer exists.  See `lib18dc.child_work`")
d("SD9", "A COMMENT READ AS CODE, TWICE.  My `pipefail` rule matched the "
        "string anywhere in a runner and reported 31 of 117 setting it; 29 of "
        "those are COMMENTS saying `set -o pipefail` is NOT used because "
        "/bin/sh is dash on Linux -- the most repeated line in this arc's "
        "runners.  The same rule read `.new`+`mv` out of a comment and turned "
        "a 2 into a 4, including THIS runner, which uses neither",
  "grepping the arc by hand after the number looked too big",
  "31 -> 2 and 23 -> 1 on `tee`; 4 -> 2 on the fix.  P6 goes from a hit to a "
  "MISS as a direct result, and is kept as written.  All of MY rules over "
  "runner source now go through `lib18dc.code_of`; the rules I REPRODUCE from "
  "mg-03d1 deliberately do not, because re-deriving its 86 means running its "
  "rule as written")
d("SD10", "A ROW NAME THAT WAS NOT ITS MEASUREMENT: V6b printed `RUNNERS in "
         "BOTH populations` while intersecting ALL `tee` users with the "
         "truncating set, directly under a row that had just defined the "
         "population of interest as `tee` WITHOUT `pipefail`",
  "reading the two rows next to each other",
  "no count moved at the time -- the two sets happened to coincide -- and "
  "both intersections are now printed separately")
d("SD8", "AN `ALL` OVER AN EMPTY SET, IN MY OWN OUTPUT.  V3b's false-positive "
        "rows shipped for one draft as `%d own-tree reads, all of populated "
        "files`, which over n == 0 reads `all 0 of them were fine` -- a "
        "universal asserted over nothing.  That is ALL_PASS over an empty set, "
        "which is one of the SIX SIBLING DEFECTS this brief lists, committed by "
        "the audit sent to look for it",
  "reading my own V3 transcript after the first full pass, not the code",
  "no count moved -- the classification was right and the SENTENCE was empty. "
  "The n == 0 case is now a differently-named row, because `never read one at "
  "all` and `read them and they were fine` are different findings")
d("SD7", "A TIMEOUT IS RECORDED AS NOT-BITING.  V3 kills a runner at 240 s and "
        "counts no empty read for it.  That is `not known`, printed as though "
        "it were `not found`",
  "arithmetic: the killed trees are listed in V3a and are inside the "
  "denominator of V3b",
  "every V3 count is a LOWER BOUND and V3a says so where the number is printed")

# ---------------------------------------------------------------------------
B.hdr("V7a  THE DEFECTS")

print("  population: the defects of this instrument I can name")
B.plain("...DEFECTS recorded", len(DEFECTS), "one defect")
print()
for tag, what, caught, cost in DEFECTS:
    print("  %s  %s" % (tag, what))
    print("      caught by:  %s" % caught)
    print("      cost:       %s" % cost)
    print()

# ---------------------------------------------------------------------------
B.hdr("V7b  SD3 IN NUMBERS -- MY OWN RUNNER IN MY OWN POPULATION")

head = B.git("rev-parse", "HEAD").strip()
here = B.runners_at(head)
mine_in = B.MINE in here
print("  population: the runners tracked at my own HEAD")
B.plain("...RUNNERS at HEAD, including this audit's own", len(here),
        "one `run_all.sh`")
B.plain("...RUNNERS at HEAD, excluding this audit's own",
        len(here) - (1 if mine_in else 0), "one `run_all.sh`")
print()
print("      this audit's own runner is in the population:  %s"
      % ("YES" if mine_in else "not yet -- this section ran before it landed"))
print()
print("  BOTH NUMBERS ARE PRINTED and neither is the one I would pick to")
print("  protect a sentence.  mg-03d1 hit this and printed both; mg-ec63 hit it")
print("  and printed three; it is the third consecutive audit in this lineage")
print("  to acquire a member of the set it counts by doing the counting.")

# ---------------------------------------------------------------------------
B.hdr("V7c  AND DOES MY OWN RUNNER CARRY THE DEFECT I AM AUDITING?")

print("  Measured the way everything else here is measured -- by running it")
print("  under the stub and watching, not by reading its source.  mg-ec63's")
print("  own S6a got this wrong in the other direction: its resolver called")
print("  its runner TRUNC because an untraceable `$VAR/` prefix is ASSUMED to")
print("  be inside the tree, and mg-ec63 corrected it in prose.  An execution")
print("  measurement cannot make that mistake, because it looks at the file.")
print()
sbx = B.sandbox(head, tag="head-v7")
if os.path.isdir(os.path.join(sbx, B.MINE)):
    res, err = B.stub_run(sbx, B.MINE, timeout=180)
    if err or not res:
        print("      (could not run: %s)" % (err or "no result"))
    else:
        st = B.emptied_steps(res)
        print("  population: the probe invocations of my own runner")
        B.plain("...INVOCATIONS observed", len(res["rows"]), "one invocation")
        B.plain("...INVOCATIONS starting on an EMPTY transcript of this tree",
                len(st), "one invocation")
        print()
        if st:
            print("      *** MY OWN RUNNER CARRIES THE DEFECT I AM SWEEPING FOR ***")
            for s in st:
                print("          %s" % ", ".join(s["zero"]))
        else:
            print("      My transcripts are written under `$V18_WORK`, outside the")
            print("      repository, and copied in after the last probe exits.  No")
            print("      probe of mine ever starts on an empty transcript OF THIS")
            print("      TREE.  That is mg-ec63's structural repair, adopted.")
    B.sandbox_reset(sbx)
else:
    print("      this tree is not yet in the commit under test -- SD3's other")
    print("      face: the instrument cannot measure itself until it has landed,")
    print("      and once it lands the measurement is of a different tree.")

# ---------------------------------------------------------------------------
B.hdr("V7d  THE ONE CLAIM I CANNOT CHECK FROM INSIDE")

print("  Everything above is measured against a CLONE of this repository.  If")
print("  the clone differs from the worktree, every number here is about the")
print("  wrong tree and nothing in this suite would notice.  The check:")
print()
sb = B.sandbox(head, tag="head-v7")
a = subprocess.run(["git", "rev-parse", "HEAD^{tree}"], cwd=sb,
                   capture_output=True, text=True).stdout.strip()
b = B.git("rev-parse", "HEAD^{tree}").strip()
print("      clone tree hash     %s" % a)
print("      worktree HEAD tree  %s" % b)
print("      identical:          %s" % ("yes" if a == b else "*** NO ***"))
print()
print("  It compares the clone to the COMMIT, not to the worktree's files.  An")
print("  uncommitted edit in the worktree would not show here, and this suite")
print("  would be measuring the last commit while the author read the file.")
print("  That is a real hole and it is not closed; it is named.")

print()
print("V7 TOTAL DEFECTS OF THIS INSTRUMENT: %d" % len(DEFECTS))
sys.exit(min(len(DEFECTS), 120))
