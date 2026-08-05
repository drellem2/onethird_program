"""R4 -- WIDENING A NAME LIST IS NOT MAKING IT A PROPERTY.  mg-dee4's F5.

THE FINDING.  `k2_consume.py`'s caller scan matched `run_all\\.sh`.  mg-7522
made it `(?:run_all|run_audit)\\.sh` -- one filename replaced by two -- and
stated the property in `lib7522`, whose comment says the name rule *"is widened
here to the property"*, HERE being the library and not the file that was
repaired.  At `973ca61` -- the revision this figure is a fact about -- 9
distinct executing SITES name a `*.sh` whose basename is neither, 4 of them
reading the status, and 0 sites name the `run_audit.sh` the widening added.
The same census gives 10 (site, target) ROWS at that revision, and it MOVES
with the repository, which is why the figure carries a revision here and not
the word `HEAD`.  The value at the HEAD of any given run is printed by the
probe itself, in the section below, and is not written into this docstring --
a number in prose cannot be re-measured, which is how `At HEAD` became false
without anyone editing it.

> A property stated where the check does not live is a property nothing
> enforces.

THE REPAIR.  `libc2b3.targets` -- the sweep's OWN library, used by the sweep's
own scan, pinned by the sweep's own self-test.  The property, the check and the
test in one directory.  This probe re-derives the census under a parser written
here, so `9 outside, 4 consuming, 0 run_audit` is a measurement and not a
citation of mg-dee4.

TWO GRAINS, EACH UNDER ITS OWN GRAIN WORD.  mg-56dc/T1c, repaired by mg-bf79.
The scan below produces one row per (SITE, TARGET) pair, because a single source
line that executes something and names two different `*.sh` is two targets --
and its totals were printed under the label `executing sites`.  THE LABEL WAS
RIGHT AND THE COUNT WAS WRONG: `9` is the distinct-SITE count and is what this
tree's README, its `OUTCOMES.md`, this docstring and the published document all
state; `10` is the ROW count and is what the transcript printed under the site
word.  Both numbers are legitimate and both are now printed, each with its own
grain in its own label, at a NAMED REVISION -- because this census ranges over
the whole repository and therefore moves while the arc is landing, which is the
half of T1c that does not reproduce and is said here rather than discovered.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

BAD = 0
K2 = "%s/k2_consume.py" % M.SWEEP_TREE

# Written here rather than imported: this probe's job is to disagree with the
# repaired rule if the repaired rule is wrong.
EXEC = re.compile(r"subprocess\.|(?<![\w.])sh\s+[\"'./$]|\./run_\w*\.sh"
                  r"|run_runner\(")
NOT_EXEC = re.compile(r"[\"']git[\"']|git show|git -C|ls-tree")
READ = re.compile(r"returncode|check\s*=\s*True")
ANY_SH = re.compile(r"(?:([\w./-]+)/)?(\w[\w-]*\.sh)\b")
TWO_NAMES = ("run_all.sh", "run_audit.sh")
_SET_E = re.compile(r"^\s*set\s+(?:-[a-zA-Z]*e[a-zA-Z]*\b|-o\s+errexit\b)", re.M)

M.bar("R4  THE CALLER SCAN'S TARGET RULE, AS A PROPERTY")

# ---------------------------------------------------------------------------
M.hdr("R4a  THE CENSUS AT HEAD, UNDER THE PROPERTY -- derived here")

files = [f for f in M.git("ls-files", "--", "*.py", "*.sh").splitlines() if f]
sites = []
for f in files:
    try:
        src = M.read(f, None)
    except (RuntimeError, OSError):
        continue
    lines = src.split("\n")
    se = bool(_SET_E.search(src))
    for i, line in enumerate(lines, 1):
        if not EXEC.search(line) or NOT_EXEC.search(line):
            continue
        seen = set()
        for m in ANY_SH.finditer(line):
            d, base = m.group(1) or "", m.group(2)
            if "%s" in d or d.startswith("/") or base in seen:
                continue
            if d and os.path.normpath("%s/%s" % (d, base)) == os.path.normpath(f):
                continue
            seen.add(base)
            window = "\n".join(lines[i - 1:i + 25])
            consumes = (se and "||" not in line) if f.endswith(".sh") \
                else bool(READ.search(window))
            sites.append((f, i, base, consumes))

by = {}
for _f, _i, base, c in sites:
    n, k = by.get(base, (0, 0))
    by[base] = (n + 1, k + (1 if c else 0))
# THE COLUMN IS `sites` AND IS CORRECT PER ROW, which is worth saying because
# it is not where the defect was: within one source line the `seen` set above
# admits each basename once, so a basename's own count cannot double-count a
# line.  Only the TOTALS below can, and only across basenames -- one line
# naming two different scripts lands in two of these rows.
print("    %-20s %6s %10s   %s" % ("target basename", "sites", "consuming",
                                   "the two-name rule sees it?"))
for base in sorted(by, key=lambda b: (-by[b][0], b)):
    n, c = by[base]
    print("    %-20s %6d %10d   %s"
          % (base, n, c, "yes" if base in TWO_NAMES else "NO"))
out = [s for s in sites if s[2] not in TWO_NAMES]


def _sites(rowset):
    """{(file, line)} -- the DISTINCT SITES behind a list of (site, target) rows.

    One source line is one site however many scripts it names.  Written here
    rather than imported for the reason the module docstring gives: this probe's
    job is to be able to disagree with the rule it checks.
    """
    return {(f, i) for f, i, _b, _c in rowset}


HEAD_REV = M.git("rev-parse", "--short", "HEAD").strip()
print()
print("  BOTH GRAINS, at `%s`.  The row grain is what the scan produces; the"
      % HEAD_REV)
print("  site grain is what the four artifacts publish.  The gap between them")
print("  is exactly the number of source lines naming more than one `*.sh`.")
print()
print("      (site,target) ROWS naming a `*.sh`            %3d" % len(sites))
print("      distinct executing SITES behind those rows    %3d"
      % len(_sites(sites)))
print("      ...ROWS the two-name rule matches             %3d"
      % (len(sites) - len(out)))
print("      ...ROWS outside it, across %d distinct basenames %3d"
      % (len({s[2] for s in out}), len(out)))
print("      ...distinct SITES outside it                  %3d"
      % len(_sites(out)))
print("      ...of those SITES, READING the exit status    %3d"
      % len(_sites([s for s in out if s[3]])))
print("      ...ROWS naming `run_audit.sh`, the name ADDED %3d"
      % by.get("run_audit.sh", (0, 0))[0])
print()
multi = sorted(k for k in _sites(sites)
               if len([s for s in sites if (s[0], s[1]) == k]) > 1)
print("      source lines naming MORE THAN ONE `*.sh`      %3d" % len(multi))
for f, i in multi:
    names = sorted(s[2] for s in sites if (s[0], s[1]) == (f, i))
    print("          %s:%d  ->  %s" % (f, i, ", ".join(names)))
print()
print("  THE ROWS THEMSELVES -- one per (site, target) pair, so a reader can")
print("  disagree with the rule rather than with a total, and can count the")
print("  sites by eye.  A `file:line` appearing twice is ONE site with two")
print("  targets.  Some are fixtures inside a self-test and some are live")
print("  invocations; both are printed and neither is folded away:")
print()
for f, i, base, c in out:
    print("      %-50s %-6s %s" % ("%s:%d" % (f, i), "READS" if c else "-",
                                   base))

# ---------------------------------------------------------------------------
M.hdr("R4b  IS THE PROPERTY STATED WHERE THE CHECK LIVES?")

k2 = M.read(K2, None)
libc = M.read("%s/libc2b3.py" % M.SWEEP_TREE, None)
self_t = M.read("%s/selftestc2b3.py" % M.SWEEP_TREE, None)
# A RULE, not a mention of one.  `k2_consume.py` names the old two-name rule
# three times -- once in a comment saying what it replaced and twice in prose
# it PRINTS, so a reader of the transcript can see what the column means.  A
# check that could not tell those from a regex would force the explanation to
# be deleted in order to pass, which is the mention-for-occurrence defect
# mg-05eb recorded in its own self-test and mg-7522 hit again.  So the question
# asked here is whether the alternation is the argument of a REGEX CALL.
RULE = re.compile(r"re\.(?:compile|search|findall|match|finditer)\("
                  r"[^)]*run_all\|run_audit")
checks = [
    ("k2_consume.py no longer holds a two-name rule (regex calls only)",
     len(RULE.findall(k2)), 0),
    ("...and calls the property rule", len(re.findall(r"L\.targets\(", k2)), 1),
    ("libc2b3.py defines it", len(re.findall(r"^def targets\(", libc, re.M)), 1),
    ("...and states the property in its own words",
     len(re.findall(r"executes something and names a shell script"
                    r"|THE PROPERTY IS", libc + k2, re.I)), 2),
    ("selftestc2b3.py pins it in BOTH senses",
     len(re.findall(r"L\.targets\(", self_t)), 5),
]
for label, got, want in checks:
    ok = got == want if want in (0,) else got >= want
    if not ok:
        BAD += 1
    print("      %-52s %2d   %s" % (label, got, "OK" if ok else "*** want %d ***"
                                    % want))
print()
print("  mg-7522's own stated-limit comment named the LITERAL-PATH limit")
print("  correctly and did not name this one.  Both limits are named at the")
print("  rule now: the tree is read from a directory component on the same")
print("  line, and a path assembled at run time is invisible to any")
print("  line-local rule whatever the anchor.")
print()
lim = len(re.findall(r"THE LIMITS THAT REMAIN", k2))
print("      k2_consume.py states BOTH remaining limits at the rule   %s"
      % ("yes" if lim else "*** NO ***"))
if not lim:
    BAD += 1

# ---------------------------------------------------------------------------
M.hdr("R4c  DOES THE WIDENING LOSE ANYTHING?  both directions")

print("  A widened rule that drops a row it used to have is not a widening.")
print("  The old rule's hits are computed here and checked to be a SUBSET:")
print()
old = []
for f in files:
    try:
        src = M.read(f, None)
    except (RuntimeError, OSError):
        continue
    lines = src.split("\n")
    for i, line in enumerate(lines, 1):
        m = re.search(r"([\w./]*?([\w]+)/(?:run_all|run_audit)\.sh)", line)
        if not m or not EXEC.search(line) or NOT_EXEC.search(line):
            continue
        if "%s" in m.group(1):
            continue
        old.append((f, i))
new_keys = {(f, i) for f, i, _b, _c in sites}
lost = [k for k in old if k not in new_keys]
print("      SITES the two-name rule found                 %3d" % len(old))
print("      ...SITES still found under the property       %3d"
      % (len(old) - len(lost)))
print("      ...SITES LOST by the widening                 %3d" % len(lost))
for f, i in lost:
    print("          *** %s:%d" % (f, i))
if lost:
    BAD += len(lost)

print()
M.bar("R4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a two-name regex still in")
print("`k2_consume.py`, a property that is not stated where the check is, a")
print("missing both-senses fixture, an unstated limit, and a site the old rule")
print("found that the new one does not.  It ranges over every tracked `*.py`")
print("and `*.sh` at `%s`.  THE TOTALS ABOVE MOVE WITH HEAD -- they are a"
      % HEAD_REV)
print("whole-repository census, and the figure the four artifacts publish is")
print("pinned to a NAMED REVISION for that reason and not to `HEAD`, which is")
print("the half of mg-56dc/T1c that does not reproduce.")
print("It does NOT range over targets whose path is")
print("assembled at run time -- that is the stated limit, and the runtime-path")
print("census is `%s/out_s4_unpin.txt`." % M.SUBJECT)
sys.exit(1 if BAD else 0)
