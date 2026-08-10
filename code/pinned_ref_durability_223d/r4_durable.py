"""mg-223d / R4 -- THE REPAIR, AND THE CONTROL THAT FIRES ON PIN 28.

The ticket's third instruction: *make the dependence durable for whatever
survives.  Options, and the choice needs stating rather than assuming: a tag on
the ref so gc cannot collect it; committing the two tree hashes with the figure;
or vendoring the reconstructed input.  Pick one, say why, and say what it costs.*

Picked: A TAG.  The reasoning is in R4a, the cost is in R4b, and the reason the
other two were not picked is a MEASUREMENT in `x1_gc.py` and not a preference.

R4c is the part that matters more than the 26 tags: a control that answers
`is every ref this arc's code depends on still safe`, over the whole arc, that
can go red, and that goes red on a pin nobody has declared.
"""
import os
import sys

import lib223d as L

led = L.Ledger("mg-223d / R4 -- THE REPAIR: A TAG, AND A CONTROL THAT CAN FIRE")

# ---------------------------------------------------------------------------
led.head("R4a  THE CHOICE, AND WHY THE OTHER TWO LOSE")
# ---------------------------------------------------------------------------
print("""
  (a) A TAG ON THE REF.                                          <- CHOSEN
  (b) COMMITTING THE TWO TREE HASHES WITH THE FIGURE.
  (c) VENDORING THE RECONSTRUCTED INPUT.

  (b) DOES NOT WORK, AND THIS IS MEASURED RATHER THAN ARGUED.  `x1_gc.py`
  arm 3 writes a tree sha down, prunes the branch, runs `git gc --prune=now`,
  and looks for the object: GONE.  A tree sha in a text file is not a ref.
  `gc` collects an unreachable tree exactly as it collects an unreachable
  commit, so option (b) records WHICH object you needed and does nothing
  whatever to keep it.  It is the option a reader reaches for first -- it
  needs no ref, no push and no permission -- and it is a record of the loss
  written in advance in a format that reads like a remedy.

  (c) WORKS AND COSTS THE PROPERTY THAT MADE THE FIGURE WORTH KEEPING.
  Vendoring the 517 files' BYTES does make the census reproducible with no
  git objects at all.  It also converts `a function of two 40-character
  strings and of nothing else on this machine` -- cfd9c's own words for why
  the reconstruction is stable -- into a function of a directory, which is
  what every other figure in this arc already is and every one of which has
  drifted.  And it repairs 1 of 26.

  (a) IS THE ONLY OPTION THAT SCALES AND THE ONLY ONE THAT PRESERVES THE
  SUBJECT.  Six of the pinning directories pin the PRE-REBASE commit BECAUSE
  the pre-rebase commit is their subject (R2c); for them there is nothing to
  vendor and nothing to substitute -- the object itself is the evidence.  A
  tag makes it reachable and changes no figure, no file and no instrument.""")

# ---------------------------------------------------------------------------
led.head("R4b  WHAT IT COSTS -- ALL OF IT, INCLUDING THE HALF THAT IS NOT DONE")
# ---------------------------------------------------------------------------
rows = L.manifest_rows()
tags = sorted(set(r[2] for r in rows))
print()
print("      declared pin rows (unit: TOKEN)                    %5d" % len(rows))
print("      distinct commits behind them (unit: COMMIT)        %5d"
      % len(set(r[1] for r in rows)))
print("      keep-alive tags this implies (unit: REF)           %5d" % len(tags))
print("      bytes of ref, roughly                              %5d" % (len(tags) * 50))
print("""
      AND THE COST THAT IS NOT A NUMBER:

      1. A TAG IS NOT DURABLE UNTIL IT IS PUSHED.  `git tag` writes into this
         machine's object store.  The refinery merges BRANCHES; nothing in the
         merge path carries a tag.  So `mktags.sh --yes` buys protection
         against a local `gc` and NOTHING against this machine.  `--push` is
         the half that survives it, and R4d reports which half actually ran
         rather than asserting durability in general.

      2. A TAG READS LIKE AN ENDORSEMENT.  Someone finding `pin/9f1ecaa` in
         `git tag` has no way to know it means `something depends on this` and
         not `this is a release`.  The prefix and the annotation message and
         PINS.tsv's header are mitigation, not a fix.

      3. IT MAKES THE COMMITS PERMANENT.  That is the point, and it is also
         the cost: 26 commits that would have aged out of the object store now
         will not.  Undoing it is two lines and they are in `mktags.sh`.

      4. IT DOES NOT REPAIR THE 354 RECORDS.  A transcript that says
         `HEAD: <sha>` about a commit nobody pins is still a claim that
         becomes uncheckable if the object goes.  R1g counts them; this repair
         does not touch them, and that is a decision rather than an oversight:
         a record's remedy is to be readable, and 354 more tags would make the
         tag namespace unreadable.""")

# ---------------------------------------------------------------------------
led.head("R4c  THE CONTROL -- AND IT IS THE PART THAT OUTLIVES THE TAGS")
# ---------------------------------------------------------------------------
print("""
  26 tags fix today.  The DEFECT is that nothing in the arc records that a
  figure depends on a ref remaining reachable, so pin 28 will be written by
  someone who has never read this tree.  `L.check_pins()` is the convention
  made checkable, and its verdicts are four different remedies:

      OK-TAGGED    a tag holds it.  Nothing to do.
      OK-ON-MAIN   it is an ancestor of main.  (Filtered out before display;
                   this is the overwhelming majority and it is not news.)
      AT-RISK      it resolves, and every holder is a prunable branch.
                   REMEDY: `mktags.sh --push`.
      DEAD         declared and unresolvable.  NO REMEDY from inside this
                   repository -- and that is precisely why the verdict exists.
      UNDECLARED   tracked code pins it and PINS.tsv does not list it.
                   REMEDY: add the row, then `mktags.sh --push`.  This is the
                   verdict that fires on pin 28.""")

v = L.check_pins()
by = {}
for _s, k, _d in v:
    by[k] = by.get(k, 0) + 1
print()
for k in ("UNDECLARED", "AT-RISK", "DEAD", "OK-TAGGED"):
    print("      %-12s %5d" % (k, by.get(k, 0)))
print("      %-12s %5d" % ("(total)", len(v)))
print()
for s, k, d in v:
    if k != "OK-TAGGED":
        print("        %-10s %-11s %s" % (s, k, d[:52]))

bad = [r for r in v if r[1] in ("UNDECLARED", "AT-RISK", "DEAD")]
led.record(not bad, "pins that are not yet held by something gc cannot "
           "collect: %d of %d" % (len(bad), len(v)))

# ---------------------------------------------------------------------------
led.head("R4d  WHICH HALF ACTUALLY RAN -- MEASURED HERE, NOT ASSERTED")
# ---------------------------------------------------------------------------
local_tags = [t for t in L.git("tag", "-l", "pin/*").split() if t]
remote_out = L.git("ls-remote", "--tags", "origin", "refs/tags/pin/*")
remote_tags = sorted(set(l.split("refs/tags/")[-1].replace("^{}", "")
                         for l in remote_out.split("\n") if "refs/tags/" in l))
want = sorted(set(r[2] for r in rows))
print()
print("      keep-alive tags DECLARED in PINS.tsv               %5d" % len(want))
print("      keep-alive tags present LOCALLY                    %5d" % len(local_tags))
print("      keep-alive tags present ON ORIGIN                  %5d" % len(remote_tags))
missing_local = [t for t in want if t not in local_tags]
missing_remote = [t for t in want if t not in remote_tags]
led.record(not missing_local,
           "declared tags missing locally: %d" % len(missing_local))
led.record(not missing_remote,
           "declared tags missing on origin -- the half that survives this "
           "machine: %d" % len(missing_remote))
if missing_remote:
    print("      REMEDY: sh mktags.sh --push")
print("""
      THIS ARM IS P6, AND IT IS HERE BECAUSE `DURABLE` IS THE EASIEST WORD IN
      THIS TICKET TO SAY WITHOUT EARNING.  A run of this suite on a machine
      that has the tags and a remote that does not will print two different
      numbers on the two lines above, and the second one is the true one.""")

# ---------------------------------------------------------------------------
led.head("R4e  WHAT THIS REPAIR IS NOT")
# ---------------------------------------------------------------------------
print("""
  IT IS NOT A PROMOTION OF THE RECONSTRUCTION.  cfd9c's constraint, kept: the
  reconstruction is an ARCHIVAL ACT, not an instrument.  It still cannot see
  an untracked file, still cannot be computed from any single commit, still
  cannot say which write regime produced a figure, and still needs two refs
  worked out BY HAND once per figure.  A tag makes the two refs SURVIVE.  It
  is not a method for finding out which two refs to tag, and nothing in this
  tree makes that step cheaper.

  IT IS NOT A CLAIM THAT THE 26 PINS ARE ALL WORTH KEEPING.  Some of them
  probably are not.  Deciding that is a reading of 13 directories by their
  owners; what this tree does is make the decision reversible in the direction
  that matters, because a tag can be deleted and a collected object cannot be
  restored.

  IT IS NOT A REPAIR OF ANY FIGURE.  No published number moved.  R5c measures
  that as a multiset over every tracked file rather than asserting it.""")

sys.exit(led.done())
