"""d4_movingref -- A RUN WHOSE STEPS EACH RESOLVE A MOVING REF.

mg-1abe's defect 2, in its own words:

    "This suite resolved `main` once per SCRIPT, and `main` moved between them.
     In its own first full run t1 measured 537 transcripts at `eacc5e1` while
     t2 started at `81214a9`."

Two scripts, one runner, two trees, ONE reported census.  The fix -- resolve
once in `run_all.sh` and pass the sha to every script -- landed in `a7d7fb9`.
This script does two things with that:

  1. CONFIRMS THE FIX IS ON `main`, by ancestry rather than by reading the file
     in the worktree I am standing in.  A file present in my branch is a fact
     about my branch (this item's E7).

  2. SWEEPS FOR THE SAME SHAPE everywhere else.  A defect found in one
     instrument and repaired only there is a defect the arc keeps.

THE SHAPE, stated before the detector so its population is what its name says
(this item's E5, against mg-1abe's own t6 over-collecting by 32x):

  (a) a runner drives TWO OR MORE scripts, AND
  (b) TWO OR MORE of those scripts independently resolve a MOVING REF
      (`main`, `HEAD`, `origin/main`), AND
  (c) the runner passes NO resolved revision down to them.

NOT the shape, and each is printed as a rejected near-miss rather than dropped:

  * ONE script resolving `main` ten times -- that is one process, one tree, and
    no seam between two measurements.
  * a runner that resolves once and hands the sha down -- that is THE FIX.
  * a suite whose scripts never name a moving ref -- it cannot exhibit it.

AND THE SHAPE IS NOT THE DAMAGE.  A suite can carry it for a year and never be
bitten, because nothing merged between its two scripts.  D4d asks the harder
question -- has it FIRED? -- by looking for two committed transcripts of the
same suite that name DIFFERENT revisions in an `as-of` role.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib_f8e5 as L

FIX = "a7d7fb9"
CENSUS = "code/transcript_census_1abe"

_RE_ASOF = re.compile(
    r"^[^\n]*\b(?:as[- ]of|audited as of|measured at|as at|at commit|"
    r"population anchor|revision)\b[^\n]*$", re.I | re.M)


def asof_revs(text):
    """Resolvable commits a transcript names in an `as-of` role."""
    out = []
    for line in _RE_ASOF.findall(text):
        for tok in re.findall(r"\b[0-9a-f]{7,40}\b", line):
            full = L.resolve(tok)
            if full and full not in out:
                out.append(full)
    return out


def main():
    at = L.main_rev()
    rev = L.resolve(at)
    led = L.Ledger("d4 -- THE MOVING-REF SHAPE: A RUN WHOSE STEPS EACH "
                   "RESOLVE A MOVING REF", reads_outside_tree=True)
    print("    as-of: %s" % rev[:12])

    # ------------------------------------------------------------- D4a
    led.head("D4a -- DID THE FIX LAND?  ANCESTRY, NOT THE FILE IN FRONT OF ME")
    full = L.resolve(FIX)
    on_main = bool(full) and L.git_ok("merge-base", "--is-ancestor", full, rev)
    print("    %s resolves                        : %s"
          % (FIX, full[:12] if full else "NO"))
    print("    ...and is an ancestor of %s   : %s" % (rev[:7], on_main))
    led.record(on_main,
               "D4a the single-resolve fix (%s) is an ancestor of %s.  Checked "
               "by ancestry because the file being present in the worktree I am "
               "standing in is a fact about my branch (E7)" % (FIX, rev[:7]))

    sh = L.blob_at(rev, CENSUS + "/run_all.sh")
    text = sh.decode("utf-8", "replace") if sh else ""
    has_once = bool(L._RE_PASSDOWN.search(text))
    has_note = "MOVES BETWEEN THEM" in text.upper() or "eacc5e1" in text
    print("    `run_all.sh` at %s resolves once and passes `$AT` down : %s"
          % (rev[:7], has_once))
    print("    ...and records the incident in its own header          : %s"
          % has_note)
    led.record(has_once and has_note,
               "D4a' and the fix is BOTH halves: the revision is resolved once "
               "and handed to every script, AND the incident that motivated it "
               "is in the runner's own header, where the next person to "
               "'simplify' it will read it")

    # ------------------------------------------------------------- D4b
    led.head("D4b -- THE DETECTOR, SHOWN GOING BOTH WAYS ON ONE SUITE")
    print("""A detector that has only ever printed one answer has not been shown able
to print the other.  So it is run on the SAME directory at the commit BEFORE
the fix and at `main` -- the only pair in this repository known in advance to
straddle the defect.
""")
    before = L.resolve(FIX + "^")
    arms = []
    for label, r in (("before the fix (%s)" % (before or "?")[:7], before),
                     ("at %s" % rev[:7], rev)):
        if r is None:
            led.self_error("cannot resolve %s" % label)
            continue
        v, detail = L.moving_ref_scan(CENSUS, r)
        arms.append((label, v, detail))
        print("    %-28s -> %-14s  %d script(s) driven, %d naming a moving ref"
              % (label, v, len(detail["scripts"]), len(detail.get("movers", []))))
        for m in detail.get("movers", [])[:4]:
            print("        %s" % m)
    if len(arms) == 2:
        led.record(arms[0][1] == "SHAPE",
                   "D4b the detector FINDS the shape in mg-1abe's own suite at "
                   "the commit before its fix -- where mg-1abe says it was")
        led.record(arms[1][1] == "PASSES-DOWN",
                   "D4b' and does NOT find it at %s, after the fix.  Both "
                   "answers on the same directory" % rev[:7])

    # ------------------------------------------------------------- D4c
    led.head("D4c -- THE SWEEP, OVER EVERY SUITE INCLUDING THIS ONE")
    dirs = L.suite_dirs(rev)
    buckets = {}
    shaped = []
    for d in dirs:
        v, detail = L.moving_ref_scan(d, rev)
        buckets.setdefault(v, []).append((d, detail))
        if v == "SHAPE":
            shaped.append((d, detail))
    print("    population: every `code/<dir>` at %s holding a tracked "
          "`.py` or `.sh`: %d" % (rev[:7], len(dirs)))
    print()
    for v in ("SHAPE", "PASSES-DOWN", "ONE-SCRIPT", "NO-MOVING-REF",
              "NO-RUNNER"):
        print("    %-16s %d" % (v, len(buckets.get(v, []))))
    print()
    print("    EVERY SUITE CARRYING THE SHAPE, NAMED IN FULL (nothing "
          "truncated):")
    for d, detail in shaped:
        print("      %-44s %d scripts, %d resolve a moving ref: %s"
              % (d[5:], len(detail["scripts"]), len(detail["movers"]),
                 ", ".join(detail["movers"][:3])
                 + (" ..." if len(detail["movers"]) > 3 else "")))
    print()
    print("    REJECTED NEAR-MISSES, so the detector's population is what its "
          "name says:")
    for v, why in (("PASSES-DOWN", "the runner resolves once and hands the sha "
                                   "down -- this is THE FIX, not the defect"),
                   ("ONE-SCRIPT", "fewer than two scripts resolve a moving ref "
                                  "-- one process, one tree, no seam")):
        names = [d[5:] for d, _ in buckets.get(v, [])]
        print("      %-14s %3d   %s" % (v, len(names), why))
        if names:
            print("                     %s" % ", ".join(names[:6])
                  + (" ..." if len(names) > 6 else ""))
    led.record(not shaped,
               "D4c THE SHAPE IS PRESENT IN %d OF %d SUITES AT %s.  mg-1abe "
               "found it in its own instrument and repaired it there; it is a "
               "property of how this arc writes runners, not of that suite"
               % (len(shaped), len(dirs), rev[:7]))

    # ------------------------------------------------------------- D4d
    led.head("D4d -- HAS IT FIRED?  THE SHAPE IS NOT THE DAMAGE")
    print("""A suite can carry the shape for a year and never be bitten: if nothing
merged between its two scripts, both measured the same tree.  What FIRING looks
like is two committed transcripts of ONE suite naming DIFFERENT revisions in an
`as-of` role -- which is exactly the evidence mg-1abe had for its own defect
(t1 at `eacc5e1`, t2 at `81214a9`).

⚠️ THIS IS A LOWER BOUND AND THE REASON IS WORTH STATING.  Most transcripts in
this arc print no revision at all -- mg-1abe measured 310 of 541 naming no
commit anywhere in their own bytes.  A suite that was bitten and never printed
an `as-of` is invisible here.  A finding is evidence; a zero is not.
""")
    fired = []
    silent = 0
    for d, _ in shaped:
        seen = {}
        for p in L.transcripts(rev):
            if os.path.dirname(p) != d:
                continue
            b = L.blob_at(rev, p)
            if b is None:
                continue
            revs = asof_revs(b.decode("utf-8", "replace"))
            if revs:
                seen[os.path.basename(p)] = revs
        if len(seen) < 2:
            silent += 1
            continue
        allrevs = {r for v in seen.values() for r in v}
        if len(allrevs) > 1:
            fired.append((d, seen))
    print("    suites carrying the shape                        : %d"
          % len(shaped))
    print("    ...where fewer than 2 transcripts name a revision : %d "
          "(INVISIBLE, not clean)" % silent)
    print("    ...where two transcripts name DIFFERENT revisions : %d"
          % len(fired))
    for d, seen in fired:
        print()
        print("      %s" % d[5:])
        for name in sorted(seen):
            print("        %-40s %s"
                  % (name, ", ".join(s[:7] for s in seen[name][:4])))
    led.record(not fired,
               "D4d %d of the %d suites carrying the shape have two committed "
               "transcripts naming DIFFERENT revisions -- the shape has FIRED "
               "there, on the same evidence mg-1abe had for its own. %d more "
               "are invisible to this test because fewer than two of their "
               "transcripts name a revision at all"
               % (len(fired), len(shaped), silent))

    # ------------------------------------------------------------- D4e
    led.head("D4e -- AND THIS SUITE IS IN ITS OWN POPULATION")
    print("""⚠️ SCANNED AT `HEAD`, NOT AT `main`, AND THE REASON IS THIS SCRIPT'S OWN
SUBJECT.  At the revision every other row above is a fact about, this directory
does not exist yet -- it is the branch that carries it.  A self-check that
looked at `main` would report NO-RUNNER and pass, which is mg-1abe's defect 6
(a check that cannot see the end of its own output) wearing a different hat.
So this one row is a fact about the branch, and it says so.
""")
    head = L.resolve("HEAD")
    listed = L.git("ls-tree", "--name-only", "%s:code/%s"
                   % (head, L.SELF_DIR)).split()
    if not listed:
        led.self_error("D4e code/%s does not exist at HEAD (%s), so this "
                       "suite cannot be scanned against its own detector"
                       % (L.SELF_DIR, head[:7]))
    else:
        mine, det = L.moving_ref_scan("code/" + L.SELF_DIR, head)
        print("    code/%s at HEAD %s -> %s   (%d scripts driven, %d "
              "resolving a moving ref)"
              % (L.SELF_DIR, head[:7], mine, len(det["scripts"]),
                 len(det.get("movers", []))))
        led.record(mine == "PASSES-DOWN",
                   "D4e this suite does NOT carry the shape it hunts and is "
                   "not merely absent from the population: its `run_all.sh` "
                   "resolves the revision ONCE and passes `--at` to every "
                   "script, which is the same fix and the same row mg-1abe's "
                   "suite scores (E8)")
    return led.done()


if __name__ == "__main__":
    sys.exit(main())
