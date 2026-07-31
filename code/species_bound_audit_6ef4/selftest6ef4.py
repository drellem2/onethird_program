"""selftest6ef4 -- this instrument's own contracts.

The two that matter, and both of them are here because a check only ever seen
to PASS is worth nothing:

  * THE RESTORE CONTRACT IN THE DIRECTION THAT MUST FAIL.  A probe that
    deliberately leaves a file behind must be reported NOT restored, and a
    probe that deliberately leaves a MODE behind must be reported by name.
    The second half is the whole of T4: mg-5040's proof has the first and not
    the second.
  * THE CATCH PREDICATE MUST NOT MATCH A LEGEND.  `s1_extent.py` prints a
    legend line reading `!! = STILL ASSERTED` in every run it ever makes.  An
    earlier version of T1's predicate asked whether that string and the
    planted filename both appeared anywhere in the run, and reported a catch
    from a checker that had crashed before reaching its own verdict.

    python3 code/species_bound_audit_6ef4/selftest6ef4.py
"""

import os
import re
import sys
import tempfile

from kern6ef4 import (hdr, PRE, REPO, RUNNERS, Probe6ef4, git, lift,
                      tracked_regular)

fails = 0
n = 0


def ok(label, cond, detail=""):
    global fails, n
    n += 1
    fails += (not cond)
    print("  %-64s %s" % (label[:64], "ok" if cond else "*** FAILED ***"))
    if detail and not cond:
        print("        %s" % detail)


hdr("selftest6ef4 -- contracts")

# --- the pin ---------------------------------------------------------------
code, _ = git(["merge-base", "--is-ancestor", PRE, "HEAD"])
ok("the pin %s is an ancestor of HEAD" % PRE, code == 0)
ok("the pin is a literal revision, not HEAD",
   re.fullmatch(r"[0-9a-f]{7,40}", PRE) is not None)
code, out = git(["rev-parse", PRE])
code2, out2 = git(["rev-parse", "HEAD"])
ok("the pin is not HEAD", out.strip() != out2.strip())

# The pin must NOT already carry the repair being audited, or every "before"
# figure in this instrument compares a thing with itself.
c, pre_src = git(["show", "%s:code/species_remainder_f8fa/w3_scope.py" % PRE])
ok("w3_scope.py at the pin does NOT carry `walk_residue`",
   c == 0 and "walk_residue" not in pre_src)
c, pre_run = git(["show", "%s:code/species_repair_a4ef/run_all.sh" % PRE])
ok("run_all.sh at the pin still has the OLD wiring block",
   c == 0 and "E2OUT" in pre_run)
ok("run_all.sh at the pin already has `set -e`",
   c == 0 and any(l.strip() == "set -e" for l in pre_run.splitlines()),
   "the fifth rung is not something this repair introduced")

# --- lift ------------------------------------------------------------------
w = lift("code/species_repair_a4ef/s1_extent.py", "walk_residue")
ok("lift() returns a callable without running the checker", callable(w))
d = tempfile.mkdtemp(prefix="mg6ef4-st-")
with open(os.path.join(d, "a.txt"), "w", encoding="utf-8") as f:
    f.write("x\n")
files, stated, unstated = w(d)
ok("the lifted walk finds a plain file", files == ["a.txt"], repr(files))
os.makedirs(os.path.join(d, "__pycache__"))
files, stated, unstated = w(d)
ok("the lifted walk carries the SUBJECT's stated directory rule",
   [r for r, _ in stated] == ["__pycache__"], repr(stated))

# --- the restore contract, in the direction that must FAIL ------------------
victim = None
for p in tracked_regular(REPO):
    if p.endswith("code/species_bound_audit_6ef4/PREDICTIONS.md"):
        victim = p
ok("the self-test's victim file is tracked", victim is not None)

if victim:
    entry_mode = os.stat(victim).st_mode & 0o7777
    # (a) a file deliberately left behind must be reported NOT restored
    stray = os.path.join(REPO, "code", "species_bound_audit_6ef4",
                         "_selftest_stray_6ef4.txt")
    try:
        with Probe6ef4("must-fail-file") as pr:
            with open(stray, "w", encoding="utf-8") as f:
                f.write("left behind on purpose\n")
        ok("a probe that leaves a FILE behind reports NOT restored",
           pr.restored is False, "restored=%r" % pr.restored)
        ok("and it says WHY, by name",
           any("porcelain GAINED" in x for x in pr.why_not),
           repr(pr.why_not[:3]))
    finally:
        if os.path.exists(stray):
            os.unlink(stray)

    # (b) a MODE deliberately left behind must be reported by name
    try:
        with Probe6ef4("must-fail-mode") as pr2:
            os.chmod(victim, 0o000)
        rels = [r for r, _w, _n in pr2.mode_bad]
        ok("a probe that leaves a MODE behind is reported by name",
           any(r.endswith("PREDICTIONS.md") for r in rels), repr(rels[:4]))
        ok("and the mode is actually put back",
           (os.stat(victim).st_mode & 0o7777) == entry_mode,
           oct(os.stat(victim).st_mode & 0o7777))
    finally:
        os.chmod(victim, entry_mode)

    # (c) the direction that must PASS
    with Probe6ef4("must-pass") as pr3:
        pass
    ok("a probe that changes nothing reports RESTORED", pr3.restored is True)
    ok("and reports no mode differences", pr3.mode_bad == [])

# --- the catch predicate must not match a legend ---------------------------
LEGEND = "        !! = STILL ASSERTED\n"
HIT = "        STILL ASSERTED AT  leak6ef4.py:2\n"


def caught_here(out, name="leak6ef4.py"):
    return any("STILL ASSERTED" in ln and name in ln
               for ln in out.splitlines())


ok("the catch predicate is silent on a legend line", not caught_here(LEGEND))
ok("the catch predicate fires on a real hit line", caught_here(HIT))
ok("and is silent when the filename is on a DIFFERENT line",
   not caught_here(LEGEND + "        code/species_7d75/leak6ef4.py\n"))

# --- the figure regex ------------------------------------------------------
FIG = re.compile(r"A2 TOTAL BAD[^0-9\n]{0,30}?(\d+)")
for text, want in [("A2 TOTAL BAD: 1", ["1"]),
                   ("A2 TOTAL BAD is 2", ["2"]),
                   ("A2 TOTAL BAD stays 1", ["1"]),
                   ("(`A2 TOTAL BAD` remains **1**,", ["1"]),
                   ("A2 TOTAL BAD 1, the one row", ["1"]),
                   ("A2 TOTAL BAD", [])]:
    ok("figures(%r) == %r" % (text[:34], want), FIG.findall(text) == want,
       repr(FIG.findall(text)))

# --- the deletion helper ---------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def without(text, needle):
    lines = text.splitlines(True)
    hits = [i for i, ln in enumerate(lines) if ln.strip() == needle]
    if len(hits) != 1:
        raise RuntimeError("%r appears %d times, expected 1"
                           % (needle, len(hits)))
    del lines[hits[0]]
    return "".join(lines)


raised = False
try:
    without("a\nb\n", "set -e")
except RuntimeError:
    raised = True
ok("a deletion that would delete NOTHING raises instead of passing", raised,
   "a green run from a deletion test that deleted nothing is the same shape "
   "as everything else in this arc")

for rn in RUNNERS:
    src = open(os.path.join(REPO, "code", rn, "run_all.sh"),
               encoding="utf-8").read()
    ok("%s: `set -e` appears exactly once" % rn,
       len([l for l in src.splitlines() if l.strip() == "set -e"]) == 1)

# --- no comparison in this instrument is anchored on HEAD ------------------
HERE = os.path.dirname(os.path.abspath(__file__))
bad_anchor = []
for fn in sorted(os.listdir(HERE)):
    if not fn.endswith(".py"):
        continue
    src = open(os.path.join(HERE, fn), encoding="utf-8").read()
    # A before/after comparison anchored on HEAD stops comparing anything the
    # moment the thing it measures lands (mg-821e, via mg-4700).  `HEAD` as
    # ONE OF SEVERAL NAMED revisions in a census table is a different use and
    # is spelled inside the REVS list, which is checked for by name.
    for m in re.finditer(r'extract\(\s*"HEAD"|PRE\s*=\s*"HEAD"', src):
        bad_anchor.append("%s: %s" % (fn, m.group(0)))
ok("no before/after comparison here is anchored on HEAD", not bad_anchor,
   repr(bad_anchor))

print()
print("=" * 78)
print("selftest6ef4: %d assertions, %d failed" % (n, fails))
print("=" * 78)
sys.exit(1 if fails else 0)
