"""K2 -- per runner and per line, IS THE EXIT STATUS ACTUALLY CONSUMED?

The ticket is explicit that this is not a uniform fix: *"`| tee` is only
dangerous where something consumes the status.  A runner whose result is read
only as committed output may be unaffected; say which, per runner, rather than
fixing all 23 uniformly."*

Three things can consume a runner's verdict, and they are measured separately:

  C1  `set -e` INSIDE the runner.  A failing command aborts the run, so the
      later steps do not execute and the runner exits non-zero.  With the
      pipeline in place `set -e` sees `tee`'s 0 and the run CONTINUES -- so the
      damage is not only the exit code, it is that everything downstream ran on
      an unchecked precondition.
  C2  AN EXTERNAL CALLER that reads the runner's status.
  C3  THE TARGET'S OWN ABILITY TO FAIL.  A pipeline over a script with no
      non-zero exit path discards nothing.  This is measured, not assumed:
      every tee'd target is parsed for `sys.exit(<non-zero>)` and friends.

The verdict per line is the conjunction: a line is AFFECTED when something
consumes the status (C1 or C2) AND the target can produce a non-zero one (C3).

All of it is measured at %s, the revision the ticket cites, because after the
repair there is nothing left to classify -- which is exactly the trap mg-821e
recorded: a comparison anchored to HEAD stops comparing the moment the repair
lands.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libc2b3 as L

BAD = 0
REF = L.TICKET_REF


def hdr(t):
    print()
    L.bar(t)
    print()


# C3 is measured as "does this target have a DESIGNED way to report failure",
# not "could it ever exit non-zero" -- every Python script can crash.  Three
# designed routes are recognised, and which one it is gets printed, because
# `assert` was the answer for four of the self-tests and a rule that only knew
# about `sys.exit` would have called them incapable of failing.
EXIT_RE = re.compile(r"sys\.exit\(\s*(?!0\s*\))|raise\s+SystemExit\("
                     r"\s*(?!0\s*\))|^\s*exit\(\s*(?!0\s*\))", re.M)
ASSERT_RE = re.compile(r"^\s*assert\s", re.M)
RAISE_RE = re.compile(r"^\s*raise\s+(?!SystemExit)", re.M)


def can_fail(runner_rel, script):
    """(verdict, why) -- can this tee'd target exit non-zero BY DESIGN?"""
    d = os.path.dirname(runner_rel)
    rel = os.path.normpath(os.path.join(d, script))
    try:
        src = L.read(rel, REF)
    except subprocess.CalledProcessError:
        return None, "not readable at %s" % REF
    if script.endswith(".sh"):
        # a shell script under `set -e` fails on any unguarded command
        return (L.has_set_e(src),
                "`set -e`" if L.has_set_e(src) else "no set -e")
    for rx, name in ((EXIT_RE, "sys.exit"), (ASSERT_RE, "assert"),
                     (RAISE_RE, "raise")):
        m = rx.search(src)
        if m:
            return True, "%s at %s:%d" % (name, os.path.basename(rel),
                                          src[:m.start()].count("\n") + 1)
    return False, "NO designed failure route (only a crash)"


L.bar("K2  IS THE STATUS CONSUMED?  per runner, per line, at %s" % REF)

runners = L.runners(REF)
srcs = {r: L.read(r, REF) for r in runners}
affected = [r for r in runners if L.tee_pipelines(srcs[r])]

# ---------------------------------------------------------------------------
hdr("K2a  C2 -- EXTERNAL CALLERS that read a runner's exit status")

print("  Only EXECUTABLE sources are searched -- `.py` and `.sh`.  A `.md` or a")
print("  committed `out_*.txt` that names a runner is prose about a run, not a")
print("  caller of one, and counting those would inflate the exposure with")
print("  files that cannot read an exit status at all.  (Prose claims are not")
print("  dropped, they are K3's subject.)  A line counts as an EXECUTION when")
print("  it both names a `run_all.sh` and carries an executing construct")
print("  (`subprocess.`, `sh <path>`, `./run_all.sh`, or a helper that does).")
print("  It counts as CONSUMING when the status is then read -- `returncode`")
print("  or `check=True` within the next 25 lines for Python, `set -e` with no")
print("  guard on the line for sh.")
print()

# `sh` must be a COMMAND, not the tail of `run_all.sh`: the negative
# lookbehind is what stops the string "X3 in species_7d75/run_all.sh " from
# being read as an invocation.  That false positive was in the first draft of
# this table and is the reason the rule is written this way.
EXEC = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_all\.sh"
                  r"|run_runner\(")
# `git show <ref>:<path>/run_all.sh` READS a runner; it does not run one.
NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
# NOT a bare `code`: every path in this repository contains the word.
READ = re.compile(r"returncode|check\s*=\s*True")

CALLERS = []
out = subprocess.run(["git", "-C", L.REPO, "ls-tree", "-r", "--name-only",
                      REF], capture_output=True, text=True).stdout
files = [f for f in out.split("\n")
         if (f.endswith(".py") or f.endswith(".sh"))
         and not f.endswith("/run_all.sh")]
for f in files:
    try:
        src = L.read(f, REF)
    except subprocess.CalledProcessError:
        continue
    lines = src.split("\n")
    for i, line in enumerate(lines, 1):
        m = re.search(r"([\w./]*?([\w]+)/run_all\.sh)", line)
        if not m or not EXEC.search(line) or NOT_EXEC.search(line):
            continue
        if "%s" in m.group(1):        # a path built from a variable
            continue
        window = "\n".join(lines[i - 1:i + 25])
        if f.endswith(".sh"):
            consumes = L.has_set_e(src) and not L.guarded(line)
        else:
            consumes = bool(READ.search(window))
        CALLERS.append((f, i, m.group(2), consumes, line.strip()))

# `run_runner(t)` in p3_wiring.py builds the path from a variable, so the
# literal `.../run_all.sh` is on a different line from the execution.  That is
# a real limitation of a line-local scan and it is named rather than papered
# over: the row is added explicitly, and the two hand-added rows are named
# in K2f so the table cannot be read as fully mechanical.
# `( cd "$T" && ./run_all.sh )` names no tree on its own line -- the tree comes
# from the `cp -R` two lines above -- and a line-local scan cannot resolve it.
CALLERS.append(("code/branching_audit_2060/b0_repro.sh", 10,
                "branching_locate_db09", True,
                '( cd "$T" && ./run_all.sh >/dev/null 2>&1 )'))
CALLERS.append(("code/species_sites_821e/p3_wiring.py", 214,
                "species_repair_a4ef / species_remainder_f8fa / "
                "species_repair_6f61", True,
                "code, out = guarded(keep, lambda t=t: run_runner(t))"))

print("  %-50s %-9s %s" % ("caller", "consumes?", "target tree"))
for f, i, tree, consumes, line in CALLERS:
    mark = "  <-- AFFECTED" if any("/%s/" % tree.split()[0] in a
                                   for a in affected) else ""
    print("  %-50s %-9s %s%s" % ("%s:%d" % (f, i),
                                 "YES" if consumes else "no", tree, mark))
print()
print("  Read in full, the status-reading callers of an AFFECTED runner are:")
print()
print("  1. code/branching_audit_2060/b0_repro.sh:10")
print("       ( cd \"$T\" && ./run_all.sh >/dev/null 2>&1 )   under `set -e`")
print("       -- runs mg-db09's runner in a scratch copy.  CONSUMES the status.")
print("  2. code/species_sites_821e/p3_wiring.py:214,247")
print("       run_runner(t) for three species trees, and the verdict is built")
print("       from the returned CODE:  `ok = (code == 0 and present and ...)`,")
print("       `caught = (code_w != 0 and ...)`, `missed = (code_u == 0)`.")
print("       CONSUMES the status, in BOTH directions.  Two of its three trees")
print("       -- species_repair_a4ef and species_remainder_f8fa -- were")
print("       affected.  K3 takes this apart claim by claim; it is the single")
print("       biggest retroactive exposure in the arc.")
print()
print("  Every other caller found above targets a tree with no `| tee`")
print("  pipeline (the state_* trees), so no repair of theirs is at issue.")

# ---------------------------------------------------------------------------
hdr("K2b  THE PER-LINE VERDICT")

print("  C1  something in the runner consumes it (`set -e`)")
print("  C2  an external caller reads the runner's exit status")
print("  C3  the tee'd target has an explicit non-zero exit path")
print("  A line is AFFECTED when (C1 or C2) and C3.")
print()
print("  %-40s %-4s %-3s %-3s %-3s %-9s %s"
      % ("runner / tee'd target", "line", "C1", "C2", "C3", "verdict",
         "C3 evidence"))

EXT = {"code/branching_locate_db09/run_all.sh": "b0_repro.sh (set -e)",
       "code/species_repair_a4ef/run_all.sh": "p3_wiring.py",
       "code/species_remainder_f8fa/run_all.sh": "p3_wiring.py"}

rows = []
for r in affected:
    c1 = L.has_set_e(srcs[r])
    c2 = r in EXT
    first = True
    for n, t in L.tee_pipelines(srcs[r]):
        script = L.invocations(t)[0][1]
        c3, why = can_fail(r, script)
        aff = bool((c1 or c2) and c3)
        rows.append((r, n, script, c1, c2, c3, aff, why))
        print("  %-40s %-4d %-3s %-3s %-3s %-9s %s"
              % ((r.replace("code/", "").replace("/run_all.sh", "")
                  + " / " + os.path.basename(script)) if True else "",
                 n, "y" if c1 else "-", "y" if c2 else "-",
                 "y" if c3 else "-",
                 "AFFECTED" if aff else "no", why))
        first = False

n_aff = sum(1 for x in rows if x[6])
print()
print("  %d of %d pipelines are AFFECTED, across %d of %d runners."
      % (n_aff, len(rows), len({x[0] for x in rows if x[6]}), len(affected)))

# ---------------------------------------------------------------------------
hdr("K2c  THE ONES THAT ARE NOT AFFECTED, AND WHY -- named, not omitted")

print("  Thirteen pipelines are NOT affected, and they fail the conjunction in")
print("  two different places.  The distinction is kept because collapsing it")
print("  would let `not affected` mean two things at once:")
print()
print("    C3 FALSE  -- the target has no designed failure route, so the")
print("                 pipeline discarded no VERDICT.  It still discarded a")
print("                 CRASH: an ImportError or a missing input exits 1 and")
print("                 the runner would not have seen it.  Repaired anyway,")
print("                 and counted here so that `all 34 carried a verdict`")
print("                 is not asserted when it is false.")
print("    C1+C2 FALSE -- the target CAN fail, but nothing read the runner\'s")
print("                 status, so removing the pipeline alone changes")
print("                 nothing.  There is exactly one of these and it needs")
print("                 more than a de-pipelining; see K2d.")
print()
print("  %-46s %-8s %s" % ("pipeline", "fails at", "detail"))
for r, n, script, c1, c2, c3, aff, why in rows:
    if aff:
        continue
    where = "C3" if not c3 else "C1+C2"
    print("  %-46s %-8s %s"
          % ("%s:%d %s" % (r.replace("code/", "").replace("/run_all.sh", ""),
                           n, os.path.basename(script)), where, why))
print()

# ---------------------------------------------------------------------------
hdr("K2d  THE RUNNER WITHOUT `set -e` -- a different defect, named separately")

r7 = "code/species_audit_7dd3/run_all.sh"
s7 = srcs[r7]
print("  %s is the one affected runner with NO `set -e`." % r7)
print("  Its own header says:")
_h = s7.split("\n")
for i, line in enumerate(_h):
    if "self-test is the only file" in line:
        print("      %s" % line.strip())
        print("      %s" % _h[i + 1].strip())
print()
print("  So its self-test's status IS meant to be load-bearing.  It was not,")
print("  and `| tee` is only half the reason: with no `set -e` and every other")
print("  step ending in `|| true`, the last command of the script is an")
print("  `echo`, so THE RUNNER EXITED 0 UNCONDITIONALLY -- with or without the")
print("  pipeline.  Removing the pipeline alone would not have fixed it.")
print("  The repair is therefore an explicit `|| { ...; exit 1; }` guard on")
print("  the self-test, which is what makes the header true; the `|| true` on")
print("  d1..d6 is deliberate and is left exactly as it was.")
print()
now7 = L.read(r7)
_ok = ("selftest7dd3.py FAILED" in now7 and "exit 1" in now7
       and not L.tee_pipelines(now7))
print("  on disk now: guard present = %s" % _ok)
if not _ok:
    BAD += 1

# ---------------------------------------------------------------------------
hdr("K2e  THE FIX, AND WHY THIS MECHANISM")

print("  MECHANISM USED: redirect the script to its transcript, read the")
print("  status with an explicit `||` guard, then `cat` the transcript.")
print()
print("      python3 x.py > out_x.txt || {")
print("          cat out_x.txt; echo \"x.py FAILED\"; exit 1; }")
print("      cat out_x.txt")
print()
_sh = sum(1 for v in srcs.values() if v.startswith("#!/bin/sh"))
print("  WHY NOT `set -o pipefail`.  The shebang is `#!/bin/sh` on %d of the %d"
      % (_sh, len(runners)))
print("  runners -- measured, not assumed.  On Linux that is normally dash,")
print("  which has no `pipefail`:")
print("  `set -o pipefail` there writes \"Illegal option -o pipefail\" and")
print("  returns non-zero, and under `set -e` that aborts the runner at the")
print("  line that was supposed to make it safer.  It would work on macOS,")
print("  where /bin/sh is bash in POSIX mode, and fail on the other half of")
print("  the world -- the worst possible split for a control.")
print()
print("  WHY NOT `${PIPESTATUS[0]}`.  Bash-only, for the same reason, and it")
print("  needs a separate `if` after every pipeline anyway -- more source than")
print("  the redirect form, with a portability cliff attached.")
print()
print("  WHY THIS ONE.  It is POSIX; it is what mg-e1d0 and mg-821e already")
print("  used in this repository, so the arc now has ONE idiom instead of")
print("  three; and it writes the transcript with the same bytes `tee` wrote,")
print("  so no committed out_*.txt changes and no byte-comparison anywhere in")
print("  the arc is disturbed.  K3 checks that claim rather than asserting it.")
print()
print("  WHAT IT COSTS, stated because it is a real regression: `tee` streams,")
print("  a redirect does not.  On the two long runners (branching_audit_2060,")
print("  ~20 min; species_audit_7dd3, ~3 min) the transcript now appears at")
print("  the end of each step instead of live.  Correctness over progress")
print("  bars; the alternative that keeps streaming is `pipefail`, and it is")
print("  not available here.")

# ---------------------------------------------------------------------------
hdr("K2f  THE GENERAL FORM, ON THIS INSTRUMENT")

print("  This file consumes exit statuses too: `can_fail()` shells out to")
print("  `git show` through `L.read`, and K2a shells out to `git ls-tree`.")
print("  Enumerated, with the reason each cannot exhibit the defect:")
print()
print("   1. L.read/L.runners use subprocess.run(..., check=True) with NO")
print("      shell and NO pipe -- there is no last-command status to inherit.")
print("      A failing `git show` raises CalledProcessError, which is caught")
print("      exactly once, at can_fail(), and returns the verdict `None` that")
print("      K2b prints as `-` rather than silently as `no`.")
print("   2. The `git ls-tree` in K2a is NOT check=True, deliberately: its")
print("      output is then USED, so a failure shows up as an empty caller")
print("      table rather than as a pass.  An empty table would be visible")
print("      here in a way an unread status would not.")
print("   3. This script has no pipeline of its own and is invoked by")
print("      run_all.sh through a redirect and an explicit guard, not a pipe.")
print("      selftestc2b3.py section H measures that on the runner's bytes.")
print()
print("  AND WHAT IS NOT MECHANICAL, said plainly.  Two rows of K2a's table")
print("  are HAND-ADDED, because a line-local scan cannot resolve either:")
print("    * b0_repro.sh:10 runs `./run_all.sh` in a directory whose identity")
print("      comes from a `cp -R` two lines earlier;")
print("    * p3_wiring.py:214 runs `run_runner(t)`, where `t` is a loop")
print("      variable over three tree names.")
print("  Both were read by hand and both are in the AFFECTED column.  A table")
print("  that silently dropped them would have reported one caller instead of")
print("  three and made this ticket look smaller than it is.")
print()
_bad_reads = 0
for r, n, script, c1, c2, c3, aff, why in rows:
    if c3 is None:
        _bad_reads += 1
print("  targets whose source could not be read at %s: %d" % (REF, _bad_reads))
BAD += _bad_reads

print()
L.bar("K2 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts (a) tee'd targets whose source could")
print("not be read at %s, and (b) the 7dd3 guard being absent on disk." % REF)
print("It does NOT count AFFECTED lines -- %d of %d lines are affected and"
      % (n_aff, len(rows)))
print("that is the finding, not a fault.  It also does not range over runners")
print("outside this arc: the state_* and pogo/macguffin trees were verified")
print("clean by the mayor and by K1's census, and nothing here re-opens them.")
sys.exit(1 if BAD else 0)
