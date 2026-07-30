"""P3 -- OPEN 2: THE REMOVAL QUESTION FIRST, THEN THE WIRE, THEN THE RUN.

mg-6cb9's F2, MAJOR: `e2_crosssection.py` -- the check that closes mg-7dd3's
B1 -- existed, was correct, was named in every artifact a reader meets, and was
called by 0 of the 3 species `run_all.sh`.  Present in the tree, absent from
every run.

THE AMENDMENT SAYS TO ASK BEFORE WIRING, AND THIS FILE ASKS.

    Can whatever makes B1 breakable be removed, so that no check is needed?

A check with zero callers is the cheapest possible moment to ask whether it
should exist at all, because nothing depends on it yet.  P3a answers the
question with measurements rather than with a shrug, and reaches OUTCOME 2 --
the generator is not removable, so the check is wired and the reason removal
was rejected is recorded here so nobody re-asks.  P3b and P3c are the wiring,
verified the only way it can be: BY RUNNING EACH `run_all.sh` AND READING THE
CHECK'S OWN OUTPUT.  A call written into a script is not evidence of
execution -- a guarded branch, an early exit or a swallowed error all leave the
line in place.

  P3a  the removal question, three candidate removals, each MEASURED.
  P3b  each runner run: does the check's output appear?  And the deletion
       test -- take the wiring out and it disappears.
  P3c  B1 ITSELF, restored on disk, against all three runners wired and
       unwired.  This is the historical failure reproduced and then closed.

    python3 code/species_sites_821e/p3_wiring.py
"""

import os
import re
import sys

from kern821e import (hdr, REPO, git_status, Probe, run_checker, run_runner,
                      out_files, replace_once, preserve, WIRE_MARK, unwire)

bad = 0

TREES = ["species_repair_6f61", "species_remainder_f8fa", "species_repair_a4ef"]
DOC = "docs/OneThird-Species-Hopf-Monoids-Where-This-Lives.md"
E2 = "code/species_extent_d633/e2_crosssection.py"

# `WIRE_MARK` and `unwire` are imported from the kernel: taking the block out
# is one unit, and the self-test needs the same function this file uses, from a
# module it can import without running twelve `run_all.sh`.
#
# B1 itself.  §0's paragraph as it stood from `83ac472` until mg-d633: the
# Aguiar-Mahajan §17.5 sentence asserted live, unmarked, as a direct quotation
# with a section citation, 310 lines above the §4 strike that retracts it.
# Restored by REVERSING the repair, not by splicing a copy in beside it: an
# occurrence sitting in the paragraph that corrects it is exonerated, and
# correctly, so a control that splices restores nothing (mg-d633 recorded two
# earlier versions of this control that were themselves the defect).
CORRECTION = re.compile(
    r"(?s)Aguiar–Mahajan §17\.5, quoting their own §17\.4, records both "
    r"values.*?rest of its own document\.\n")
B1 = ('Aguiar–Mahajan §17.5, quoting their own §17.4: '
      '*"`K̄(Π)` is the algebra of\nsymmetric functions in '
      'noncommuting variables and `K(Π)` is the familiar Hopf algebra '
      'of\nsymmetric functions."*\n')


def restore_b1(old):
    if old is None or not CORRECTION.search(old):
        raise AssertionError("§0's corrected paragraph is not where this "
                             "probe expects it -- the probe cannot run")
    return CORRECTION.sub(lambda _m: B1, old, count=1)


def strip_strikes(old):
    """Delete every `~~struck~~` span outright, keeping the text it wrapped.

    This is candidate removal (a) in P3a made concrete: stop MARKING false
    sentences and just delete the marking.
    """
    return re.sub(r"~~(.+?)~~", r"\1", old, flags=re.S)


BASE = git_status()


def guarded(edits, fn):
    with Probe(edits):
        r = fn()
    after = git_status()
    if after != BASE:
        print("\n*** THE RESTORE DID NOT RESTORE -- stopping.")
        print(after)
        sys.exit(2)
    return r


# ---------------------------------------------------------------------------
# P3a  THE REMOVAL QUESTION
# ---------------------------------------------------------------------------
hdr("P3a  CAN THE GENERATOR BE REMOVED, SO THAT NO CHECK IS NEEDED?")

print("  The generator, stated precisely so that it can be argued with: A")
print("  CLAIM STRUCK AT ONE SITE OF A DOCUMENT CAN STAND UN-STRUCK AT")
print("  ANOTHER SITE OF THE SAME DOCUMENT, because striking is per")
print("  occurrence and a document may state one claim in more than one")
print("  place.  Three candidate removals, each measured.")
print()

# (1) is the generator live at all?
code, out = run_checker(E2)
m = re.search(r"(\d+) file\(s\) carry a strike, (\d+) strike\(s\) measured",
              out)
nfiles, nstrikes = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
ctl_a = "(a) B1 restored" in out and "fires, 1 finding -- ok" in out
ok = (code == 0 and nstrikes > 0 and ctl_a)
bad += (not ok)
print("  (1) IS THE GENERATOR LIVE?")
print("      %d document(s) carry a strike and %d strike(s) are measured"
      % (nfiles, nstrikes))
print("      e2's own control (a) restores B1 and it fires: %s"
      % ("yes" if ctl_a else "*** NO -- this measurement is void ***"))
print("      -> LIVE.  %s" % ("ok" if ok else "*** UNMEASURED ***"))
print()

# (2) candidate removal (a): stop striking; delete the false sentence instead.
def measure_stripped():
    return run_checker(E2)


stripped_code, stripped_out = guarded(
    [(DOC, lambda o: strip_strikes(restore_b1(o)))], measure_stripped)
m2 = re.search(r"(\d+) file\(s\) carry a strike, (\d+) strike\(s\) measured",
               stripped_out)
s_files, s_strikes = (int(m2.group(1)), int(m2.group(2))) if m2 else (-1, -1)
# the target document's own strike count, before and after
def doc_strikes(text):
    return len(re.findall(r"~~(.+?)~~", text, re.S))


live_doc = open(os.path.join(REPO, DOC), encoding="utf-8").read()
n_doc = doc_strikes(live_doc)
standing = len(re.findall(r"STANDING UN-STRUCK", stripped_out))
ok = (s_strikes == nstrikes - n_doc and standing == 0)
bad += (not ok)
print("  (2) REMOVAL (a): STOP MARKING.  Delete every `~~ ~~` in the target")
print("      document -- keep the text, drop the strike -- and put B1 back.")
print("      the document's %d strike(s) go to 0; the repo-wide count goes"
      % n_doc)
print("      %d -> %d, and the SWEEP reports %d standing.  THE FALSE BELIEF IS"
      % (nstrikes, s_strikes, standing))
print("      STILL IN §0 AND NOTHING CAN SEE IT.  Removal (a) does not make")
print("      the class impossible, it makes it INVISIBLE.  %s"
      % ("REJECTED, measured" if ok else "*** measurement failed ***"))
print("      PREDICTION MISSED, KEPT: I wrote `exit 0` and the exit is %d."
      % stripped_code)
print("      Not the sweep -- e2's own CONTROL (a).  That control restores B1")
print("      by REVERSING §0's repair, and with the strikes deleted the")
print("      paragraph it reverses into is gone, so it prints `the control")
print("      cannot run` and books itself as failed.  The detector reports")
print("      ITSELF broken instead of reporting the false belief, which")
print("      sharpens the conclusion rather than softening it: removal (a)")
print("      takes out the detector and the evidence in one move.")
print()

# (3) candidate removal (b): forbid restatement -- one copy per claim.
exon = len(re.findall(r"exonerated: ", out))
below = len(re.findall(r"below the rule", out))
ok = exon > 0
bad += (not ok)
print("  (3) REMOVAL (b): FORBID RESTATEMENT.  One copy per claim, so a strike")
print("      has nothing to be compared against.")
print("      %d of the %d strike(s) measured are EXONERATED: the claim IS"
      % (exon, nstrikes))
print("      restated, and legitimately -- quoted back in order to correct it.")
print("      A rule that forbids restating a struck claim forbids correcting")
print("      one.  %d more sit below the rule as shared lead-ins.  There is no"
      % below)
print("      generator to delete either: these are markdown files written by")
print("      hand.  %s" % ("REJECTED, measured" if ok else "*** no data ***"))
print()

# (4) candidate removal (c): has B1 been closed for another reason?
print("  (4) HAS B1 BEEN CLOSED FOR ANOTHER REASON?  No: (1)'s control")
print("      restores it and it fires, which is the definition of can-still-")
print("      arise.  And the per-section checkers are all still green while it")
print("      stands -- P3c measures exactly that.")
print()
print("  OUTCOME 2.  The generator is not removable; the check is wired into")
print("  all three runners.  Removal was rejected because (a) converts a")
print("  detectable defect into an undetectable one and (b) forbids the")
print("  correction of a struck claim.  Recorded here so the next person does")
print("  not re-ask -- and if either measurement above stops holding, the")
print("  question is open again.")
print()


# ---------------------------------------------------------------------------
# P3b  the wiring, verified by running
# ---------------------------------------------------------------------------
hdr("P3b  EACH RUNNER RUN, AND THE CHECK'S OWN OUTPUT READ FROM IT")

NEEDLE = "E2 TOTAL BAD:"
CENSUS = re.compile(r"\d+ strike\(s\) measured")

_wired = open(os.path.join(REPO, "code", TREES[0], "run_all.sh"),
              encoding="utf-8").read()
_unit = len(_wired.splitlines()) - len(unwire(_wired).splitlines())
print("  A runner is not asked whether it MENTIONS the check.  It is run, and")
print("  its stdout is searched for the check's own output.  The deletion test")
print("  removes the wiring block -- ONE unit, %d lines, counted from the"
      % _unit)
print("  patch itself -- and the check's output must disappear with it.")
print()
print("  %-26s %-8s %-24s %s"
      % ("runner", "exit", "check's output present?", "unwired"))
for t in TREES:
    rel = "code/%s/run_all.sh" % t
    keep = [(f, preserve) for f in out_files(t)]
    code, out = guarded(keep, lambda t=t: run_runner(t))
    present = NEEDLE in out and bool(CENSUS.search(out))
    code_u, out_u = guarded([(rel, unwire)] + keep, lambda t=t: run_runner(t))
    gone = (NEEDLE not in out_u)
    ok = (code == 0 and present and code_u == 0 and gone)
    bad += (not ok)
    print("  %-26s %-8d %-24s %s"
          % (t, code, "YES" if present else "*** NO ***",
             "output gone, exit %d -- ok" % code_u if gone
             else "*** STILL THERE ***"))
    for ln in out.splitlines():
        if NEEDLE in ln or CENSUS.search(ln):
            print("        %s" % ln.strip())
print()
print("  3 of 3 runners execute it.  mg-6cb9 measured 0 of 3.")
print()


# ---------------------------------------------------------------------------
# P3c  B1 itself, on disk, against all three runners
# ---------------------------------------------------------------------------
hdr("P3c  B1 RESTORED ON DISK -- THE HISTORICAL FAILURE, REPRODUCED")

print("  §0's corrected paragraph is REVERSED back to the misquotation it")
print("  carried from `83ac472` until mg-d633.  Every per-section checker was")
print("  green for that whole time and every extent line was true.  Each")
print("  runner is then run twice: as it is now, and with the wiring block")
print("  removed.  The second column is the state mg-6cb9 measured.")
print()
print("  %-26s %-22s %s" % ("runner", "wired (now)", "unwired (before)"))
for t in TREES:
    rel = "code/%s/run_all.sh" % t
    keep = [(f, preserve) for f in out_files(t)]
    code_w, out_w = guarded([(DOC, restore_b1)] + keep,
                            lambda t=t: run_runner(t))
    code_u, out_u = guarded([(DOC, restore_b1), (rel, unwire)] + keep,
                            lambda t=t: run_runner(t))
    caught = (code_w != 0 and "STANDING UN-STRUCK" in out_w)
    missed = (code_u == 0)
    ok = caught and missed
    bad += (not ok)
    print("  %-26s %-22s %s"
          % (t,
             "exit %d, CAUGHT" % code_w if caught
             else "*** exit %d, MISSED ***" % code_w,
             "exit %d, green -- as it was" % code_u if missed
             else "*** exit %d ***" % code_u))
print()
print("  That is the whole of OPEN 2.  The artifact was present and the")
print("  behaviour was absent; the behaviour is now in the run, and the")
print("  deletion test above shows the wiring is what put it there.")
print()

print("=" * 78)
print("P3 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  THREE runners -- %s -- each executed as a"
      % ", ".join("code/" + t for t in TREES))
print("script four times: unmutated, unwired, with B1 restored, and with B1")
print("restored and unwired.  It says NOTHING about `code/species_7d75`, which")
print("has no checker in it, and nothing about `code/species_extent_d633`,")
print("which already called the check.  It measures WHETHER THE CHECK RUNS and")
print("whether it fires on B1; it says nothing about the other holes e2's own")
print("extent line names -- a claim restated in ANOTHER document, or restated")
print("in different words, both of which remain invisible to it and are named")
print("as invisible there.  The removal question in P3a is answered for THIS")
print("generator only.")
sys.exit(1 if bad else 0)
