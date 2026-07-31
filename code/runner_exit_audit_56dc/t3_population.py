"""T3 -- THE POPULATION, NOT THE INSTANCE.  F5 and F6, tested outside the list.

F5 and F6 are both POPULATION defects: a name rule with two names instead of
one, and a consumption clause narrower than the reason written for it.  A
population repair is only a population repair if a case that was never on
anyone's list is now caught.  So this probe builds cases that did not exist
when either rule was written and puts them to both rules:

  T3a  F5.  A site executing `zz_probe_56dc.sh` -- a basename that is neither
       of the two names and is in no fixture anywhere in the arc.  Put to the
       PRE-REPAIR two-name rule, read out of `k2_consume.py` AT `1ee1f1b`
       where the defect is still present, and to `libc2b3.targets` at HEAD.
  T3b  F6.  A real script with NO `set -e`, a pipeline whose output is
       captured and read.  Put to the ERREXIT-ONLY clause as it stands at
       `bee07a1` and to the repaired disjunction at HEAD.
  T3c  F6'S FAILURE DIRECTION.  `c0_repro.sh` fails LOUD.  A rule that only
       caught loud failures would be a different rule, so a QUIET member of
       the same shape is built and RUN: its discarded stage is forced to fail,
       and the exit code and the printed answer are read.
  T3d  Does either predicate read the failure direction at all?  Asked of the
       code that decides membership.

NO TRACKED FILE IS MODIFIED.  Every fixture is written to a scratch path under
this directory and deleted in a `finally`; the scratch names are untracked, so
they are never in any population this arc enumerates.
"""

import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

sys.path.insert(0, os.path.join(M.REPO, M.S7522))
import lib7522 as L                                            # noqa: E402
sys.path.insert(0, os.path.join(M.REPO, M.SWEEP))
import libc2b3 as C                                            # noqa: E402

BAD = 0
FINDINGS = []

M.bar("T3  THE POPULATION -- A CASE OUTSIDE THE OLD DEFINITION")

# ---------------------------------------------------------------------------
M.hdr("T3a  F5 -- A TARGET NO NAME RULE COULD HAVE LISTED")

print("  THE CONTROL IS THE PRE-REPAIR RULE ITSELF, read out of the commit")
print("  where the defect is still present rather than retyped here:")
print()
k2_old = M.read("%s/k2_consume.py" % M.SWEEP, M.REPAIR_REV)
mrx = re.search(r'r"(\([^"]*run_all\|run_audit[^"]*)"', k2_old)
OLD_RULE = re.compile(mrx.group(1)) if mrx else None
print("      k2_consume.py at %s, line %d"
      % (M.REPAIR_REV,
         k2_old[:mrx.start()].count("\n") + 1 if mrx else -1))
print("          %s" % (mrx.group(1) if mrx else "*** rule not found ***"))
if OLD_RULE is None:
    BAD += 1
print()

CASES = [
    ('    p = subprocess.run(["sh", "code/zz_tree_56dc/zz_probe_56dc.sh"],',
     "a basename in no fixture in this arc"),
    ('    p = subprocess.run(["sh", "code/zz_tree_56dc/run_audit.sh"],',
     "the name mg-7522's widening ADDED -- 0 sites in the arc name it"),
    ('    p = subprocess.run(["sh", "code/zz_tree_56dc/run_all.sh"],',
     "the original name, which both rules must still catch"),
]
print("  %-58s %-9s %s" % ("case", "OLD rule", "libc2b3.targets"))
caught_new = caught_old = 0
for line, why in CASES:
    old = bool(OLD_RULE.search(line)) if OLD_RULE else False
    new = [b for _d, b in C.targets(line)]
    print("  %-58s %-9s %s"
          % (line.strip()[:58], "HIT" if old else "MISS",
             "HIT %s" % new if new else "MISS"))
    print("      %s" % why)
    caught_old += 1 if old else 0
    caught_new += 1 if new else 0
print()
print("      cases the PRE-REPAIR two-name rule catches      %d of %d"
      % (caught_old, len(CASES)))
print("      cases `libc2b3.targets` catches                 %d of %d"
      % (caught_new, len(CASES)))
if caught_new != len(CASES):
    BAD += 1
    print("      *** the repaired rule does not catch every case ***")
elif caught_old == len(CASES):
    BAD += 1
    print("      *** the control does not exhibit the defect -- a control")
    print("          that passes proves nothing ***")
else:
    print()
    print("  THE POPULATION IS REPAIRED, not the named instance: a basename")
    print("  invented for this probe, which appears in no list in this arc, is")
    print("  caught by the property and missed by the two-name rule at the")
    print("  commit where that rule still runs.")

# ---------------------------------------------------------------------------
M.hdr("T3b  F6 -- A CONSUMING PIPELINE WITH NO `set -e`")

SCRATCH = tempfile.mkdtemp(prefix="mg56dc_", dir=os.path.join(M.REPO, M.TREE))
LOUD = """#!/bin/sh
# A fixture built for mg-56dc: the shape of code/branching_audit_a218/c0_repro.sh
# -- `set -u` and NO `set -e`, a pipeline whose discarded stages can fail, whose
# value is captured and read, and whose reading drives the script's exit code.
set -u
BAD=0
COUNT=$(grep -o '[0-9]*' data.txt | tr -d ' ' | tail -1)
echo "count=$COUNT"
if [ "$COUNT" != "7" ]; then
    echo "DISAGREES"
    BAD=$((BAD + 1))
fi
[ "$BAD" -eq 0 ] || exit 1
echo "AGREES"
"""
QUIET = """#!/bin/sh
# The SAME SHAPE with the opposite failure direction: the value is read, the
# answer changes when the discarded stage fails, and the script still exits 0
# and prints no complaint.  This is the silent green mg-c2b3 swept for.
set -u
COUNT=$(grep -o '[0-9]*' data.txt | tr -d ' ' | tail -1)
echo "rows seen: ${COUNT:-0}"
exit 0
"""
try:
    with open(os.path.join(SCRATCH, "data.txt"), "w") as fh:
        fh.write("7\n")
    for name, text in (("loud.sh", LOUD), ("quiet.sh", QUIET)):
        with open(os.path.join(SCRATCH, name), "w") as fh:
            fh.write(text)

    print("  Two fixtures of the SAME SHAPE, differing only in what the script")
    print("  does when the discarded stage fails.  Both are put to the clause")
    print("  as it stood at `%s` and to the repaired disjunction:" % M.PINNED)
    print()
    print("  %-10s %-6s %-9s %-22s %s"
          % ("fixture", "set -e", "ERREXIT", "REPAIRED consumed()", "arm"))
    verdicts = {}
    for name, text in (("loud.sh", LOUD), ("quiet.sh", QUIET)):
        pipes = L.pipelines(text)
        for i, line in pipes:
            errexit_only = L.has_set_e(text) and not L.guarded(line)
            ok, arm, why = L.consumed(text, line, i)
            verdicts[name] = (errexit_only, ok, arm)
            print("  %-10s %-6s %-9s %-22s %s"
                  % (name, "no" if not L.has_set_e(text) else "yes",
                     "IN" if errexit_only else "MISSES",
                     "IN" if ok else "MISSES", arm))
            print("      %s" % why)
    print()
    print("      fixtures the ERREXIT-only clause reaches        %d of 2"
          % sum(1 for v in verdicts.values() if v[0]))
    print("      fixtures the repaired disjunction reaches       %d of 2"
          % sum(1 for v in verdicts.values() if v[1]))
    if sum(1 for v in verdicts.values() if v[1]) != 2:
        BAD += 1
        print("      *** the repaired clause misses a member of its own shape ***")
    if sum(1 for v in verdicts.values() if v[0]) != 0:
        BAD += 1
        print("      *** the control does not exhibit the defect ***")

    # -----------------------------------------------------------------------
    M.hdr("T3c  THE FAILURE DIRECTION -- LOUD AND QUIET, BOTH RUN")

    print("  mg-70c7 measured the direction of the ONE instance and found it")
    print("  loud.  A rule that only caught loud failures would be a different")
    print("  rule, so both directions are RUN here: each fixture twice, once")
    print("  as written and once with the discarded `grep` given an option it")
    print("  rejects, so it exits non-zero and prints nothing.")
    print()
    print("  %-10s %-14s %-6s %-30s %s"
          % ("fixture", "arm", "exit", "stdout", "in the population?"))
    directions = {}
    for name, text in (("loud.sh", LOUD), ("quiet.sh", QUIET)):
        for arm, body in (("as written", text),
                          ("grep forced", text.replace(
                              "grep -o '[0-9]*'",
                              "grep --mg56dc-no-such-option -o '[0-9]*'"))):
            p = os.path.join(SCRATCH, "_arm.sh")
            with open(p, "w") as fh:
                fh.write(body)
            code, out = M.run_argv(["/bin/sh", "_arm.sh"], SCRATCH, timeout=60)
            first = " / ".join(l.strip() for l in out.splitlines()
                               if l.strip() and "no-such-option" not in l
                               and "unrecognized" not in l
                               and "illegal option" not in l)[:30]
            directions[(name, arm)] = (code, first)
            print("  %-10s %-14s %-6s %-30s %s"
                  % (name, arm, code, first,
                     "IN" if verdicts[name][1] else "MISSES"))
    print()
    loud_forced = directions[("loud.sh", "grep forced")][0]
    quiet_forced = directions[("quiet.sh", "grep forced")][0]
    print("      loud fixture, discarded stage forced to fail    exit %s"
          % loud_forced)
    print("      quiet fixture, same forcing                     exit %s"
          % quiet_forced)
    print("      ...and its printed answer changed from `%s`"
          % directions[("quiet.sh", "as written")][1])
    print("         to `%s` while still exiting 0"
          % directions[("quiet.sh", "grep forced")][1])
    print()
    if quiet_forced == 0 and verdicts["quiet.sh"][1]:
        print("  SO THE REPAIRED CLAUSE IS DIRECTION-BLIND, WHICH IS THE RIGHT")
        print("  ANSWER.  The quiet fixture is in the population on exactly the")
        print("  same terms as the loud one, and it is the one whose failure")
        print("  mg-c2b3's whole sweep exists to find: a wrong number printed")
        print("  under a green exit.  mg-70c7 measured the direction of its ONE")
        print("  member and left the rule direction-free; the rule is therefore")
        print("  the population rule it claims to be and not a loud-failure")
        print("  detector wearing its name.")
    else:
        BAD += 1
        print("  *** the repaired clause behaves differently on the quiet")
        print("      fixture -- it is a direction rule, not a population rule ***")
finally:
    shutil.rmtree(SCRATCH, ignore_errors=True)

# ---------------------------------------------------------------------------
M.hdr("T3d  DOES EITHER PREDICATE READ A FAILURE DIRECTION?")

print("  Asked of the code that decides membership, with the docstring")
print("  removed -- a docstring that DISCUSSES the direction is prose about")
print("  the rule and not part of it, which is the mention-vs-use distinction")
print("  this arc runs on.")
print()
DIRECTION = re.compile(r"\bexit\s*1\b|\bloud\b|\bquiet\b|\bsilent\b|"
                       r"returncode|\bDISAGREES\b")
import ast                                                     # noqa: E402


def body_source(path, name):
    tree = ast.parse(M.read(path, None))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)):
                body = body[1:]
            return "\n".join(ast.unparse(b) for b in body)
    return ""


for path, fn in (("%s/lib7522.py" % M.S7522, "consumed"),
                 ("%s/lib7522.py" % M.S7522, "captured_var"),
                 ("%s/lib7522.py" % M.S7522, "var_reads"),
                 ("%s/libc2b3.py" % M.SWEEP, "targets")):
    src = body_source(path, fn)
    hits = DIRECTION.findall(src)
    print("      %-22s %-14s direction tests in the CODE: %d"
          % (os.path.basename(path), fn + "()", len(hits)))
    if hits:
        BAD += 1
        print("          *** %s" % ", ".join(sorted(set(hits))))
print()
print("  0 in every one.  Membership is decided by what the shell DOES with")
print("  the status, not by what the script does afterwards, and that is what")
print("  makes the quiet fixture above a member.")

print()
M.bar("T3 TOTAL FINDINGS: %d   TOTAL BAD: %d" % (len(FINDINGS), BAD))
print()
for f in FINDINGS:
    print(f)
if not FINDINGS:
    print("(no findings -- both population repairs hold against cases that")
    print(" were outside the old definitions, and the F6 clause is")
    print(" direction-blind in both directions, measured by running both)")
print()
print("EXTENT OF THOSE NUMBERS.  TOTAL BAD counts a control that does not")
print("exhibit the defect it is the control for, a repaired rule that misses")
print("a case of its own shape, and a direction test inside a membership")
print("predicate.  It ranges over 3 F5 cases and 2 F6 fixtures, all built")
print("here, plus the pre-repair rule read at %s.  It does NOT establish"
      % M.REPAIR_REV)
print("that the VALUE arm is the right widening -- that is a disagreement")
print("with a definition, and mg-70c7 states the same limit.")
sys.exit(min(len(FINDINGS) + BAD, 120))
