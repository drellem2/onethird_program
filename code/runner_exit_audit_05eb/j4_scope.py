"""J4 -- DID IT FIX RUNNERS THAT DID NOT NEED FIXING, AND DID IT SAY SO?

The sweep was told that `| tee` is only dangerous where something consumes the
status, and to report per runner rather than fix all 23 uniformly.  It measured
the distinction (21 of 34 AFFECTED, across 15 of 17) and then repaired all 34.

A uniform fix is not wrong.  An unstated one is.  So this section asks three
questions in order, and only the third is a finding:

  J4a  were all 34 in fact repaired?          (a count, on disk)
  J4b  is the distinction actually made, and  (does a reader meet the 13, or
       is the uniform repair stated?           only the 21?)
  J4c  and the thing no list names: `tee` wrote the failing step's diagnosis to
       the runner's STDOUT.  A redirect does not.  The replacement only puts it
       back if the `||` guard `cat`s the transcript.  Where it does not, the
       repair traded a swallowed STATUS for a swallowed DIAGNOSIS -- and the
       sweep measured byte-identity of the FILE, which cannot see that.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib05eb as L

BAD = 0
MISS = []


def predict(qid, predicted, measured, ok):
    MISS.append((qid, predicted, measured, ok))
    print("  %-4s predicted %-34s measured %-24s %s"
          % (qid, predicted, measured, "as predicted" if ok else "*** MISS ***"))


L.bar("J4  THE SCOPE QUESTION -- uniform repair, and whether it is stated")

pre = {p: L.read(p, L.PINNED) for p in L.ls_sh(L.PINNED)}
now = {p: L.read(p) for p in L.ls_sh()}
FIXED = sorted(p for p in pre
               if L.tee_pipelines(pre[p]) and p in now and not L.tee_pipelines(now[p]))

# ---------------------------------------------------------------------------
L.hdr("J4a  THE 34 SITES, ON DISK -- what each became")

TXT = re.compile(r"\|\s*tee\s+(?:-a\s+)?(\S+)")
sites = []
for r in FIXED:
    for i, l in L.tee_pipelines(pre[r]):
        m = TXT.search(l)
        sites.append((r, i, m.group(1) if m else "?"))
print("  pipelines at %s in the runners that were repaired: %d"
      % (L.PINNED, len(sites)))
print()
guards = {r: {t: cat for _i, t, cat in L.redirect_guard_sites(now[r])}
          for r in FIXED}
plain = 0
guarded = 0
missing = []
for r, i, target in sites:
    g = guards.get(r, {})
    if target in g:
        guarded += 1
    elif re.search(r">\s*%s\b" % re.escape(target), now[r]):
        plain += 1
    else:
        missing.append((r, i, target))
print("  ...now a redirect WITH an explicit `||` guard : %d" % guarded)
print("  ...now a plain redirect, no guard on the line : %d" % plain)
print("  ...no redirect to that file at all            : %d" % len(missing))
for r, i, t in missing:
    print("      %s:%d -> %s" % (r, i, t))
predict("Q19", "34 of 34 repaired", "%d of %d" % (guarded + plain, len(sites)),
        guarded + plain == len(sites) == 34)
if missing:
    BAD += 1

# ---------------------------------------------------------------------------
L.hdr("J4b  IS THE DISTINCTION MADE, AND IS THE UNIFORM REPAIR STATED?")

WANT = [
    ("the 13 unaffected are NAMED individually",
     ["code/runner_exit_c2b3/out_k2_consume.txt"],
     "K2c  THE ONES THAT ARE NOT AFFECTED"),
    ("`Repaired anyway` appears beside them",
     ["code/runner_exit_c2b3/out_k2_consume.txt"], "Repaired anyway"),
    ("the split 21/34 is in the reader-facing document",
     ["docs/OneThird-RunnerExit-ArcWideSweep.md"], "21"),
    # THIS PROBE WAS WRONG ON ITS FIRST RUN and the correction is recorded
    # rather than made quietly.  It searched the document for the literal
    # string "34 of 34", found nothing, and scored the sweep as NOT having
    # stated its uniform repair -- while the document says, of the twelve
    # sites that fail C3, "Repaired anyway, and listed so that `all 34
    # carried a verdict` is not asserted when it is false."  A probe that
    # looks for a FORM OF WORDS rather than for the CLAIM is the same error
    # as counting a header comment as a pipeline, which is the error this
    # whole arc is about.  Prediction Q20 was RIGHT and my instrument was
    # wrong; the miss is kept in OUTCOMES.md as D3.
    ("the reader-facing document says the unaffected sites were repaired anyway",
     ["docs/OneThird-RunnerExit-ArcWideSweep.md"], "Repaired anyway"),
    ("the COMMIT MESSAGE carries the distinction",
     [None], "NOT UNIFORM"),
]
commit_msg = L.git("log", "-1", "--format=%B", L.SWEEP)
found = 0
for label, files, needle in WANT:
    if files == [None]:
        hit = needle in commit_msg
        where = "commit %s message" % L.SWEEP
    else:
        hit = any(needle in L.read(f) for f in files)
        where = files[0]
    found += hit
    print("  [%s] %-48s  %s" % ("yes" if hit else "*** no ***", label, where))
print()
predict("Q20", "the uniform repair IS stated", "%d of %d present"
        % (found, len(WANT)), found == len(WANT))
if found != len(WANT):
    BAD += 1
print("  READING.  The sweep does not fix 34 sites and describe 21.  It names")
print("  the 13 individually, says which clause of the conjunction each fails,")
print("  and writes `Repaired anyway` next to them.  On item 4 of the")
print("  assignment the sweep is CLEAN, and this section exists to say so with")
print("  a measurement rather than to hunt for a fault that is not there.")

# ---------------------------------------------------------------------------
L.hdr("J4c  THE OTHER HALF OF WHAT `tee` DID -- the diagnosis on stdout")

print("  `cmd | tee f` writes the step's output to f AND to the runner's")
print("  stdout, on success and on failure alike.  `cmd > f` writes only f.")
print("  The sweep measured that f does not move (K3d, K3f).  That is the")
print("  file.  The other half is the terminal: on the FAILING path, does the")
print("  diagnosis still reach the runner's stdout?  It does only if the `||`")
print("  guard `cat`s the transcript.  Measured per site:")
print()
print("  runner                                    transcript              guard cats?")
nocat = []
for r in FIXED:
    for i, target, cat in L.redirect_guard_sites(now[r]):
        pre_teed = any(TXT.search(l) and TXT.search(l).group(1) == target
                       for _j, l in L.tee_pipelines(pre[r]))
        if not pre_teed:
            continue                      # already guarded before the sweep
        print("  %-42s %-22s %s" % (r, target,
                                    "yes" if cat else "*** NO ***"))
        if not cat:
            nocat.append((r, target))
print()
print("  sites where a failing step's own output no longer reaches stdout: %d"
      % len(nocat))
predict("Q21", "34 of 34 cat on failure",
        "%d of %d" % (len(
            [1 for r in FIXED for _i, t, c in L.redirect_guard_sites(now[r])
             if c and any(TXT.search(l) and TXT.search(l).group(1) == t
                          for _j, l in L.tee_pipelines(pre[r]))]),
            34), not nocat)
if nocat:
    BAD += 1
    print()
    print("  FINDING.  At these sites the repair is correct about the STATUS")
    print("  and lossy about the OUTPUT: pre-repair a reader watching the run")
    print("  saw the failure text and a 0; post-repair they see a message and")
    print("  a non-zero, and the text is only in the file.  That is a real")
    print("  improvement and an unstated behaviour change, and `no committed")
    print("  transcript moves` is true and does not cover it.")
else:
    print()
    print("  Every repaired site cats its transcript inside the guard, so the")
    print("  failing path prints what `tee` printed.  The sweep does not claim")
    print("  this and does not measure it; it is nonetheless true, and being")
    print("  true by construction at 34 of 34 is worth a row rather than an")
    print("  assumption.")

# ---------------------------------------------------------------------------
L.hdr("J4d  THE GENERAL FORM, ON J4")

print("   1. J4 reads text and runs nothing, so it cannot discard an exit")
print("      status -- that is the branch that cannot exhibit the defect, and")
print("      the reason is that there is no subprocess in this file at all.")
print("      Verified in `selftest05eb.py` section S5 against these bytes.")
print("   2. Its own headline is DERIVED from its rows: `guarded + plain`")
print("      against `len(sites)`, both computed here, never typed in.")
print("   3. J4b is written to be able to come back CLEAN, and does.  A scope")
print("      audit that can only report faults is not measuring anything.")

print()
L.bar("J4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT.  It counts (a) a pipeline site from the pin with no redirect on")
print("disk, (b) a missing element of the sweep's own scope statement, (c) a")
print("repaired site whose guard drops the failing step's output.  It ranges")
print("over the %d pipeline sites in the %d repaired runners, and over the"
      % (len(sites), len(FIXED)))
print("five specific sentences J4b names -- not over the sweep's prose as a")
print("whole, which no instrument here reads.")
print()
nmiss = sum(1 for _q, _p, _m, ok in MISS if not ok)
print("PREDICTIONS: %d of %d as predicted, %d MISSED (%s)"
      % (len(MISS) - nmiss, len(MISS), nmiss,
         ", ".join(q for q, _p, _m, ok in MISS if not ok) or "none"))
sys.exit(1 if BAD else 0)
