"""K1 -- the census, re-derived, at the ticket's own revision and on disk.

The ticket says: *"These counts are mine and should be re-derived, not trusted.
Re-derive them and say if they differ."*  They differ in two ways, and both
matter:

  * the DENOMINATOR is 64, not 63 -- `code/hodge_leverage_repair_8eca/` landed
    in `bee07a1`, after the ticket was written.  It has no `| tee`.

  * the NUMERATOR of 23 is the BARE GREP's answer, and six of those twenty-three
    are header comments that say *"NOT `| tee`"*.  Those six trees are the ones
    that already carry the repair.  Counted as pipelines, the repaired trees are
    indistinguishable from the broken ones -- which is the very confusion this
    ticket exists to end.  The real count of runners containing a `| tee`
    PIPELINE is 17.

Both numbers are printed, side by side, with the disagreement enumerated.

  * the PIPEFAIL count.  This docstring used to end "the pipefail count (1) is
    confirmed exactly."  It was not confirmed and it was not this file that got
    it wrong: `libc2b3.PIPEFAIL_RE` matched only `set -o pipefail`, and the one
    runner that sets the option -- `code/state_restructure_34bf/run_all.sh` --
    writes `set -euo pipefail`.  So this file printed `ticket 1 / re-derived 0 /
    DIFFERS` while the README, `OUTCOMES.md`, the published document and this
    docstring all said 1, "confirmed exactly".  THE TICKET WAS RIGHT.  mg-7522
    repaired the regex; the count re-derives as 1 and AGREES.

    The general form, which is the useful half: "confirmed exactly", "verified"
    and "byte-identical" mark where an author STOPPED LOOKING.  They are a
    reason to check FIRST, not a reason to skip.

`out_k1_census.txt` in this directory is the transcript of the run that
produced the sweep's commit, at its own revision, and is left as that record --
it predates the mg-7522 repair and says so.  The corrected reading is published
in `code/runner_exit_repair_7522/out_s3_figure.txt`.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libc2b3 as L

BAD = 0


def hdr(t):
    print()
    L.bar(t)
    print()


L.bar("K1  THE CENSUS, RE-DERIVED -- ticket said 63 / 23 / 1")

for ref, label in ((L.TICKET_REF, "at %s (the revision the ticket cites)"
                    % L.TICKET_REF),
                   (None, "on disk (this worktree, post-repair)")):
    hdr("K1a  ALL run_all.sh %s" % label)
    rs = L.runners(ref)
    srcs = {r: L.read(r, ref) for r in rs}
    grep_hits = {r: L.grep_tee(s) for r, s in srcs.items()}
    pipe_hits = {r: L.tee_pipelines(s) for r, s in srcs.items()}
    pf = [r for r, s in srcs.items() if L.has_pipefail(s)]
    se = [r for r, s in srcs.items() if L.has_set_e(s)]

    print("  run_all.sh in the tree                        %3d"
          % len(rs))
    print("  ...matching the ticket's bare grep `| *tee`   %3d"
          % sum(1 for v in grep_hits.values() if v))
    print("  ...containing a REAL `| tee` PIPELINE         %3d"
          % sum(1 for v in pipe_hits.values() if v))
    print("  ...setting `pipefail`                         %3d" % len(pf))
    print("  ...setting `set -e`                           %3d" % len(se))
    print()
    only_grep = sorted(r for r in rs if grep_hits[r] and not pipe_hits[r])
    print("  THE DISAGREEMENT -- %d runner(s) the bare grep counts and the"
          % len(only_grep))
    print("  parser does not.  Every one is a header comment saying the")
    print("  runner does NOT use `| tee`:")
    for r in only_grep:
        line = grep_hits[r][0]
        print("    %-46s :%-4d %s" % (r, line[0], line[1][:60]))
    print()
    print("  pipefail:")
    for r in pf:
        print("    %s" % r)

    if ref == L.TICKET_REF:
        # The ticket's own three numbers, scored.  Predicted in PREDICTIONS.md.
        print()
        print("  TICKET'S NUMBERS, SCORED AT ITS OWN REVISION")
        for name, theirs, mine in (("run_all.sh in the tree", 63, len(rs)),
                                   ("containing `| tee` (bare grep)", 23,
                                    sum(1 for v in grep_hits.values() if v)),
                                   ("setting pipefail", 1, len(pf))):
            verdict = "AGREES" if theirs == mine else "DIFFERS"
            print("    %-34s ticket %2d   re-derived %2d   %s"
                  % (name, theirs, mine, verdict))
        print("    %-34s ticket  -    re-derived %2d   (the ticket did not"
              % ("containing a `| tee` PIPELINE",
                 sum(1 for v in pipe_hits.values() if v)))
        print("                                                        "
              "separate this)")

# ---------------------------------------------------------------------------
hdr("K1b  THE 17, LINE BY LINE, AS THE TICKET FOUND THEM (%s)" % L.TICKET_REF)

rs = L.runners(L.TICKET_REF)
old = {r: L.read(r, L.TICKET_REF) for r in rs}
affected = [r for r in rs if L.tee_pipelines(old[r])]

print("  Every `| tee` pipeline in the arc, with the file it writes and")
print("  whether an EXPLICIT construct catches the left-hand status.")
print()
print("  %-44s %-5s %-6s %s" % ("runner", "line", "guard?", "command"))
total_lines = 0
for r in affected:
    for n, t in L.tee_pipelines(old[r]):
        total_lines += 1
        print("  %-44s %-5d %-6s %s"
              % (r if total_lines and t == L.tee_pipelines(old[r])[0][1]
                 else "", n, "yes" if L.guarded(t) else "NO",
                 " ".join(t.split())[:70]))
print()
print("  %d runners, %d pipelines.  `guard?` is NO on every one: not a single"
      % (len(affected), total_lines))
print("  `| tee` line in this arc was wrapped in `||`, `if` or `$( )`.")

# ---------------------------------------------------------------------------
hdr("K1c  THE SIX ALREADY-REPAIRED TREES, AND HOW THEY DID IT")

print("  These are the bare grep's false positives.  Naming them is not")
print("  bookkeeping: they are the PRECEDENT, and item 4 of this ticket asks")
print("  which mechanism was used and why.")
print()
for r in sorted(r for r in rs if L.grep_tee(old[r]) and not L.tee_pipelines(old[r])):
    src = old[r]
    mech = []
    if "|| {" in src or "|| status=" in src:
        mech.append("redirect + explicit `||` guard")
    if L.has_pipefail(src):
        mech.append("set -o pipefail")
    print("    %-46s %s" % (r, ", ".join(mech) or "(no pipeline at all)"))
print()
print("  Plus one more that the bare grep does NOT reach, because its repair")
print("  removed the word `tee` from the runner entirely:")
_e1d0 = "code/hodge_leverage_landing_e1d0/run_all.sh"
_s = L.read(_e1d0, L.TICKET_REF)
print("    %-46s %s" % (_e1d0, "redirect + `|| status=$?`"))
print("      its own header: %s"
      % next(l.strip() for l in _s.split("\n") if "used to pipe" in l))
print()
print("  So the defect was FOUND AND FIXED TWICE, one runner at a time, by")
print("  mg-f922/e1d0 and by mg-821e, before this sweep.  Neither generalised")
print("  it; both said so.  That is why the arc-wide count was still 17.")

# ---------------------------------------------------------------------------
hdr("K1d  THE SAME CENSUS ON DISK -- what this repair left behind")

now = {r: L.read(r) for r in L.runners()}
left = {r: L.tee_pipelines(s) for r, s in now.items()}
left = {r: v for r, v in left.items() if v}
print("  runners containing a `| tee` PIPELINE, on disk:  %d" % len(left))
for r, v in sorted(left.items()):
    print("    %s" % r)
    for n, t in v:
        print("      :%d  %s" % (n, " ".join(t.split())[:66]))
if left:
    BAD += len(left)
    print()
    print("  *** NOT ZERO.  Every one above is an unrepaired site. ***")
else:
    print("    (none)")
print()
print("  runners still matching the BARE GREP on disk:     %d"
      % sum(1 for s in now.values() if L.grep_tee(s)))
print("  -- these are comments, and they are supposed to be there.  A sweep")
print("  that also deleted the comments explaining the sweep would leave the")
print("  next reader with the same bare grep and no answer.")

# ---------------------------------------------------------------------------
hdr("K1e  THIS TREE, BY ITS OWN RULES")

_self = "code/runner_exit_c2b3/run_all.sh"
_src = L.read(_self)
print("  %-46s %s" % ("`| tee` pipelines", L.tee_pipelines(_src) or "none"))
print("  %-46s %s" % ("`set -e`", L.has_set_e(_src)))
_ung = [(n, " ".join(t.split())) for n, t in L.logical_lines(_src)
        if L.invocations(t) and not L.guarded(t)
        and not t.strip().startswith("#")]
print("  %-46s %s" % ("commands launched without an explicit guard",
                      _ung or "none"))
if L.tee_pipelines(_src) or _ung:
    BAD += 1
print()
print("  THE BRANCH THAT CANNOT EXHIBIT THE DEFECT, AND WHY.  This runner")
print("  contains no pipeline anywhere -- not one `|` outside a comment on a")
print("  command line.  A pipeline is the only construct in POSIX sh whose")
print("  exit status belongs to a command other than the one being scored, so")
print("  with none present there is nothing for a verdict to hide behind.")
print("  That reason is checkable by reading the file; `set -e is set` would")
print("  not have been, since `set -e` is exactly what the 17 also had.")

print()
L.bar("K1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) runners on disk that still")
print("contain a `| tee` pipeline and (b) this tree's own runner failing its")
print("own rule.  It does NOT count runners whose status is discarded by some")
print("OTHER construct -- k2 asks that question, and answers it for all %d."
      % len(L.runners()))
sys.exit(1 if BAD else 0)
