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

# mg-7522 / OPEN 3.  THE ANCHOR OF A CENSUS IS NOT THE ANCHOR OF A COMPARISON.
#
#   A PINNED baseline is CORRECT for COMPARING and BLIND for ENUMERATING.
#
# Everything else in this file is a COMPARISON -- it classifies the runner text
# as it stood at REF, because after the repair there is nothing left to
# classify (mg-821e's own finding, and the pin is the right fix for it).  This
# block is not a comparison.  It is a CENSUS: it asks "what, in the world,
# reads a runner's exit status".  Run at REF it could only ever see callers
# that existed at REF, and `code/species_depth_audit_4700/` -- which executes
# three affected runners twenty-one times and scores them on `rc == 0` at eight
# sites -- landed in 5c16f5c, AFTER the pin.  It was therefore outside the
# enumeration by the choice of anchor, not by any failure of the rule.
#
# So the file list and the file bodies below come from HEAD, unpinned, while
# `affected` above stays at REF.  The two uses are named where they meet.
CALLER_REF = None          # None == the current world.  Do not pin this.

print("  ANCHORS.  The runner classification above is a COMPARISON and is")
print("  taken at the pinned %s.  This caller scan is a CENSUS and is taken" % REF)
print("  at HEAD, unpinned: a census must see the current world, and a caller")
print("  added after the pin is invisible to a pinned scan (mg-7522/OPEN 3).")
print()
print("  Only EXECUTABLE sources are searched -- `.py` and `.sh`.  A `.md` or a")
print("  committed `out_*.txt` that names a runner is prose about a run, not a")
print("  caller of one, and counting those would inflate the exposure with")
print("  files that cannot read an exit status at all.  (Prose claims are not")
print("  dropped, they are K3's subject.)  A line counts as an EXECUTION when")
print("  it carries an executing construct (`subprocess.`, `sh <path>`,")
print("  `./run_*.sh`, or a helper that does) AND NAMES A SHELL SCRIPT -- any")
print("  `*.sh`, which is the property; mg-70c7 replaced the two-name list")
print("  `(?:run_all|run_audit)\\.sh` that stood here (mg-dee4/F5).")
print("  It counts as CONSUMING when the status is then read -- `returncode`")
print("  or `check=True` within the next 25 lines for Python, `set -e` with no")
print("  guard on the line for sh.")
print()

# `sh` must be a COMMAND, not the tail of `run_all.sh`: the negative
# lookbehind is what stops the string "X3 in species_7d75/run_all.sh " from
# being read as an invocation.  That false positive was in the first draft of
# this table and is the reason the rule is written this way.
EXEC = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh"
                  r"|run_runner\(")
# `git show <ref>:<path>/run_all.sh` READS a runner; it does not run one.
NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
# NOT a bare `code`: every path in this repository contains the word.
READ = re.compile(r"returncode|check\s*=\s*True")

# THE TARGET RULE, AS A PROPERTY.  mg-70c7, on mg-dee4's F5.
#
# This was `run_all\.sh`.  mg-7522 made it `(?:run_all|run_audit)\.sh`, which
# is one filename replaced by two -- and mg-dee4 measured what two names still
# cannot see: 9 executing sites at HEAD name a `*.sh` whose basename is
# neither, across 6 distinct target scripts, 4 of them READING the exit status;
# and 0 sites name the `run_audit.sh` the widening added, so the widening was
# not exercised by anything in the arc.  mg-7522's own library states the
# property in a comment that says the name rule "is widened here to the
# property" -- HERE being the library, not the file that was repaired.  A
# property stated where the check does not live is a property nothing enforces.
#
# THE PROPERTY, STATED WHERE THE CHECK LIVES:
#
#     A CALLER IS A LINE THAT EXECUTES SOMETHING AND NAMES A SHELL SCRIPT.
#
# Not a line that names a script with a particular NAME.  A runner's exit
# status can be swallowed by whatever executes it, and what the file is called
# is a fact about its author's habits.  The rule is `libc2b3.targets` -- this
# tree's own library, with both-senses fixtures in this tree's own self-test,
# so the property, the check that uses it and the test that pins it are all
# in the same directory.
# THE LIMITS THAT REMAIN, named rather than left as an absence.  (1) The TREE
# is read from a directory component on the same line, so a target invoked as
# `./c0_repro.sh` or `"sh", "run_all.sh"` with `cwd=` elsewhere is counted as a
# site with tree `-`.  (2) A path assembled at run time is invisible to any
# line-local rule whatever the anchor; the complete runtime-path census is in
# `code/runner_exit_repair_7522/out_s4_unpin.txt`.  Neither limit is a name
# rule, and both are checkable.

CALLERS = []
# mg-7522: unpinned -- `git ls-files` is the current world.  The former call
# was `git ls-tree -r --name-only REF`, which is the pinned form and is the
# defect this block carried.
out = subprocess.run(["git", "-C", L.REPO, "ls-files", "--", "*.py", "*.sh"],
                     capture_output=True, text=True).stdout
# mg-7522: `and not f.endswith("/run_all.sh")` used to be part of this filter.
# It excluded every runner from being a CALLER by its NAME, and a runner that
# invokes another runner is a caller like any other.  The exclusion was a
# second name rule in the same scan as the pin, and mg-05eb reported the hole
# it opened as EMPTY -- 3 executions invisible to it, none of them targeting an
# affected runner.  Empty is a measurement, not a licence to keep the rule.
files = [f for f in out.split("\n") if f.endswith(".py") or f.endswith(".sh")]
for f in files:
    try:
        src = L.read(f, CALLER_REF)
    except (subprocess.CalledProcessError, OSError):
        continue
    lines = src.split("\n")
    for i, line in enumerate(lines, 1):
        if not EXEC.search(line) or NOT_EXEC.search(line):
            continue
        for d, base in L.targets(line):
            if "%s" in d or d.startswith("/"):   # a path built from a variable
                continue
            path = ("%s/%s" % (d, base)) if d else base
            if d and os.path.normpath(path) == os.path.normpath(f):
                continue                          # a script naming itself
            window = "\n".join(lines[i - 1:i + 25])
            if f.endswith(".sh"):
                consumes = L.has_set_e(src) and not L.guarded(line)
            else:
                consumes = bool(READ.search(window))
            # `.` and `..` name no tree; the tree is not on this line.
            tree = d.split("/")[-1] if d and d.strip(".") else "-"
            CALLERS.append((f, i, tree, consumes, line.strip(), base))

# `run_runner(t)` in p3_wiring.py builds the path from a variable, so the
# literal `.../run_all.sh` is on a different line from the execution.  That is
# a real limitation of a line-local scan and it is named rather than papered
# over: the row is added explicitly, and the two hand-added rows are named
# in K2f so the table cannot be read as fully mechanical.
# `( cd "$T" && ./run_all.sh )` names no tree on its own line -- the tree comes
# from the `cp -R` two lines above -- and a line-local scan cannot resolve it.
#
# mg-7522, ON THAT LIMIT.  Unpinning this scan was necessary and is NOT
# sufficient.  `code/species_depth_audit_4700/` executes three affected runners
# through `run_runner(t)` and `subprocess.run(["sh", "run_all.sh"], cwd=d)`, so
# it is invisible to the LITERAL-PATH rule above whatever the anchor.  The pin
# and the literal-path rule are two independent reasons the same site fell
# outside the enumeration, and fixing one does not fix the other.  The complete
# runtime-path census -- every executing site whose runner path is assembled at
# run time, and whether each reads the status -- is in
# `code/runner_exit_repair_7522/out_s4_unpin.txt`, and it is stated here rather
# than left as an absence.
CALLERS.append(("code/branching_audit_2060/b0_repro.sh", 10,
                "branching_locate_db09", True,
                '( cd "$T" && ./run_all.sh >/dev/null 2>&1 )', "run_all.sh"))
CALLERS.append(("code/species_sites_821e/p3_wiring.py", 214,
                "species_repair_a4ef / species_remainder_f8fa / "
                "species_repair_6f61", True,
                "code, out = guarded(keep, lambda t=t: run_runner(t))",
                "run_all.sh"))

print("  %-50s %-9s %-16s %s"
      % ("caller", "consumes?", "target script", "target tree"))
for f, i, tree, consumes, line, base in CALLERS:
    mark = "  <-- AFFECTED" if any("/%s/" % tree.split()[0] in a
                                   for a in affected) else ""
    print("  %-50s %-9s %-16s %s%s" % ("%s:%d" % (f, i),
                                       "YES" if consumes else "no", base,
                                       tree, mark))
print()
# mg-70c7: the table by TARGET BASENAME, so what the old two-name rule could
# and could not see is a measured row rather than an argument.
_by = {}
for f, i, tree, consumes, line, base in CALLERS:
    n, c = _by.get(base, (0, 0))
    _by[base] = (n + 1, c + (1 if consumes else 0))
_TWO_NAMES = ("run_all.sh", "run_audit.sh")
print("  BY TARGET BASENAME -- and whether the two-name rule mg-7522 left")
print("  behind could see it (mg-dee4/F5):")
print()
print("    %-20s %6s %9s   %s" % ("target basename", "sites", "consuming",
                                  "visible to `(?:run_all|run_audit)\\.sh`?"))
for base in sorted(_by, key=lambda b: (-_by[b][0], b)):
    n, c = _by[base]
    print("    %-20s %6d %9d   %s"
          % (base, n, c, "yes" if base in _TWO_NAMES
             else "NO -- invisible to it"))
_out = sum(n for b, (n, _c) in _by.items() if b not in _TWO_NAMES)
_outc = sum(c for b, (_n, c) in _by.items() if b not in _TWO_NAMES)
print()
print("      executing sites naming a `*.sh`                %3d" % len(CALLERS))
print("      ...whose basename the two-name rule matched    %3d"
      % (len(CALLERS) - _out))
print("      ...outside it, across %d distinct basenames     %3d"
      % (len({b for b in _by if b not in _TWO_NAMES}), _out))
print("      ...of those, READING the exit status           %3d" % _outc)
print("      executing sites naming `run_audit.sh`          %3d"
      % _by.get("run_audit.sh", (0, 0))[0])
print()
print("  The last row is the name mg-7522 ADDED to the rule.  Widening a name")
print("  list is not making it a property, and the property is now stated at")
print("  the rule above rather than in a library one directory over.")
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
print("  pipeline, so no repair of theirs is at issue.  mg-70c7 widened the")
print("  target rule from two names to the property, which is why that")
print("  sentence now covers %d sites rather than the handful the name rule"
      % len(CALLERS))
print("  returned; the AFFECTED set it is about did not move.")
_aff_sites = [c for c in CALLERS
              if any("/%s/" % c[2].split()[0] in a for a in affected)]
print()
print("  CHECKED, not asserted: sites whose target tree is AFFECTED   %d"
      % len(_aff_sites))
for c in _aff_sites:
    print("      %s:%d  %s" % (c[0], c[1], c[2]))

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
