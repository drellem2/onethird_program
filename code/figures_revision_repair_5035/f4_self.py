"""F4 -- THIS TREE HELD TO ITS OWN STANDARD.

The defect repaired here is a label that did not describe its code.  The one
unforgivable outcome is to repair that while committing it, so:

  F4a  DID THE TRIPWIRES FIRE?  Two selftests in the arc asserted the false
       exclusion AS FALSE precisely so a real fix would turn them red.  This
       proves they went red rather than asserting they did.
  F4b  IS THERE STILL ONE IMPLEMENTATION?  A repair of *two copies of a rule*
       may not leave three.
  F4c  IS THE POSITIVE CONTROL STILL UNREPAIRED?
  F4d  DOES EVERY COUNT ROW THIS TREE PRINTS NAME ITS POPULATION AND GRAIN?
  F4e  WHAT THIS TREE CANNOT SEE ABOUT ITSELF, said rather than left out.
"""

import ast
import os
import re
import sys
import warnings

# Parsing other trees' sources raises SyntaxWarning for regex-in-plain-string
# idioms this ticket is not repairing.  Silenced so the transcript carries this
# probe's findings and not another tree's lint.
warnings.filterwarnings("ignore", category=SyntaxWarning)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib5035 as B                                              # noqa: E402

BAD = 0
HERE = "code/figures_revision_repair_5035"

B.bar("F4  THIS TREE HELD TO ITS OWN STANDARD")

# ---------------------------------------------------------------------------
B.hdr("F4a  DID THE TRIPWIRES FIRE?  proved, not asserted")

print("  Two selftests in the arc carried the false exclusion ASSERTED AS")
print("  FALSE, each with a comment saying a later fix would turn it red and")
print("  name itself.  A ticket that edits them and says `they fired` has")
print("  proved nothing.  So the OLD assertions are re-run here against the")
print("  REPAIRED rule; each must now be false.")
print()
OLD = [
    ("selftestbf79.py  (mg-bf79/P4e)",
     lambda: B.L.figures("at 3738079 the census") == [3738079]),
    ("selftest03d1.py  (mg-03d1)",
     lambda: 1234567 in B.L.figures("at `1234567` the census gives 9 sites")),
]
fired = 0
for name, fn in OLD:
    still = fn()
    fired += (not still)
    print("      %-34s old assertion holds: %-5s  %s"
          % (name, still, "FIRED" if not still else "*** DID NOT FIRE ***"))
    if still:
        BAD += 1
print()
print("  population: the %d TRIPWIRES in the arc that assert this exclusion"
      % len(OLD))
print("  as false")
B.plain("...TRIPWIRES that went red on this repair", fired)
print("      ^ one unit of that number is one selftest case")
print()
print("  AND THEY ARE RE-POINTED, NOT DELETED.  Both files now assert the new")
print("  truth AND keep a sentence recording that the claim was false for the")
print("  whole life of the rule.  Checked by reading the source:")
for p in ("code/runner_exit_repair_bf79/selftestbf79.py",
          "code/grain_axis_audit_03d1/selftest03d1.py"):
    src = B.read(p)
    keeps = "mg-5035" in src and ("FIRED" in src or "fired" in src)
    print("      %-52s records that it fired: %s"
          % (p, "yes" if keeps else "*** NO ***"))
    if not keeps:
        BAD += 1

# ---------------------------------------------------------------------------
B.hdr("F4b  IS THERE STILL ONE IMPLEMENTATION OF `figures`?")

print("  mg-bf79's O4 was *two copies of this rule disagree*.  Repairing the")
print("  rule by adding a fourth copy would be the same defect wearing this")
print("  ticket's name.  population: every `def figures` in `code/*/lib*.py`")
print("  plus every file in this tree.")
print()
# DEFECT OF THIS PROBE, RECORDED: the first version added every tracked file
# under this tree, not every tracked `.py`, and `ast.parse` on `run_all.sh`
# took the whole probe down after F4b had already printed.  A census whose
# population rule is looser than what it does with the members is this arc's
# recurring shape, found here in the probe that checks for it.
libs = [p for p in B.git("ls-files").split()
        if re.match(r"code/[^/]+/lib[^/]*\.py$", p)] + \
       [p for p in B.git("ls-files").split()
        if p.startswith(HERE) and p.endswith(".py")]
tot, own_body = 0, 0
for p in sorted(set(libs)):
    try:
        tree = ast.parse(B.read(p))
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "figures":
            tot += 1
            stmts = [x for x in node.body
                     if not (isinstance(x, ast.Expr)
                             and isinstance(x.value, ast.Constant))]
            delegates = any(isinstance(x, ast.Call)
                            and isinstance(x.func, ast.Attribute)
                            and x.func.attr == "figures"
                            for x in ast.walk(node))
            body = "own body" if not delegates else "delegates"
            own_body += (not delegates)
            print("      %-52s %-10s %d stmt(s)" % (p, body, len(stmts)))
print()
B.plain("...DEFINITIONS of `figures` in the arc", tot)
print("      ^ one unit of that number is one function definition")
B.plain("...of those that carry their OWN BODY", own_body)
print("      ^ one unit of that number is one function definition")
print()
print("  EXPECTED: 3 definitions, 2 with own bodies -- `lib7522` (the repaired")
print("  implementation) and `lib56dc` (the untouched control) -- and")
print("  `lib70c7` delegating.  THIS TREE DEFINES NONE.")
here_defs = sum(1 for p in libs if p.startswith(HERE)
                for node in ast.walk(ast.parse(B.read(p)))
                if isinstance(node, ast.FunctionDef) and node.name == "figures")
B.plain("...DEFINITIONS of `figures` in mg-5035's own tree", here_defs)
print("      ^ one unit of that number is one function definition")
if here_defs:
    BAD += 1
if own_body != 2 or tot != 3:
    BAD += 1
    print("      *** the population moved; read the rows above before trusting")
    print("          any A/B number in this tree ***")

# ---------------------------------------------------------------------------
B.hdr("F4c  IS THE POSITIVE CONTROL STILL UNREPAIRED?")

c = B.read("code/runner_exit_audit_56dc/lib56dc.py")
clean = "_REV_SHAPE" not in c and "_is_declared_revision" not in c
print("      `lib56dc.py` carries none of mg-5035's rule: %s"
      % ("yes" if clean else "*** NO ***"))
print("      lib56dc still reads `at 1234567 ...` as a figure:      %s"
      % ("yes" if 1234567 in B.A.figures("at `1234567` the census", small=2)
         else "*** NO ***"))
if not clean:
    BAD += 1
print()
print("  A negative needs an instrument that could have shown the positive.")
print("  This is that instrument, and it is checked every run rather than")
print("  assumed to have stayed put.")

# ---------------------------------------------------------------------------
B.hdr("F4d  DOES EVERY COUNT ROW HERE NAME ITS POPULATION AND ITS GRAIN?")

print("  mg-bf79's standard, adopted: the grain lives in the row, not in a")
print("  column header.  Measured over this tree's OWN committed transcripts.")
print()
# TWO DEFECTS OF THIS PROBE, BOTH FOUND BY READING ITS OWN OUTPUT.
#   (1) `out_run_all.txt` is a CONCATENATION of the other transcripts, so every
#       row in it was counted twice.
#   (2) `^      \.\.\.` also matches a SELFTEST CASE NAME beginning with
#       `...`, which is not a count row and has no grain to name.  A count row
#       is `B.plain`'s format and ENDS IN AN INTEGER; that is the discriminator.
# Reported 59 of 67 before the fix, and all 8 "failures" were this probe's.
outs = [p for p in B.git("ls-files").split()
        if p.startswith(HERE) and os.path.basename(p).startswith("out_")
        and os.path.basename(p) != "out_run_all.txt"]
rows, graine = 0, 0
for p in sorted(outs):
    lines = B.read(p).splitlines()
    for i, l in enumerate(lines):
        if not re.match(r"^      \.\.\..*\s+\d+$", l):
            continue
        rows += 1
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if "one unit of that number is" in nxt:
            graine += 1
        else:
            print("      *** no grain line: %s: %s" % (p, l.strip()[:60]))
print("  population: the %d committed transcripts of this tree" % len(outs))
B.plain("...COUNT ROWS printed by this tree", rows)
print("      ^ one unit of that number is one printed count row")
B.plain("...COUNT ROWS whose next line names the grain of the value", graine)
print("      ^ one unit of that number is one printed count row")
if rows and graine != rows:
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("F4e  WHAT THIS TREE CANNOT SEE ABOUT ITSELF")

print("  (1) THIS TREE IS INSIDE THE CORPUS IT CENSUSES.  `F2a` ranges over")
print("      every tracked `.md`/`.txt`/`.py`, and that now includes this")
print("      directory.  Two of the excluded tokens F1c prints are in")
print("      `PREDICTIONS.md` and in `lib7522.py`'s own new comment: the rule")
print("      excludes the counter-example its documentation writes down,")
print("      because a sentence explaining `at HEAD is 431723379` is itself a")
print("      line declaring a revision.  That is not a bug and it is not")
print("      hidden; it is the reason F1c prints every non-resolving exclusion")
print("      by file and line instead of only counting them.")
print()
print("  (2) F4d CANNOT SEE ITS OWN TRANSCRIPT ON A FIRST RUN.  `run_all.sh`")
print("      writes to `out_*.txt.new` and moves at the end, so this probe")
print("      reads the PREVIOUS run's `out_f4_self.txt`.  On a clean tree that")
print("      file does not exist and its rows are simply absent from the")
print("      count above.  mg-bf79's defect #7 and mg-03d1's A4 are about")
print("      exactly this; the `.new`+`mv` idiom is inherited from them and")
print("      the residue is stated rather than claimed away.")
print()
print("  (3) THE ORACLE IS NOT TRUTH.  F1c scores against `git rev-parse`.")
print("      Its 4 disagreements are all lines that NAME a revision which")
print("      simply does not exist in this repository -- a `REVS = [...]`")
print("      fixture and two sentences about the defect.  Read as revisions")
print("      by a human, the rule is right and the oracle is wrong on all")
print("      four.  I did not adjust either; both readings are printed.")

print()
B.bar("F4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a tripwire that did not fire, a")
print("tripwire edited without recording that it had, a `figures` definition")
print("in this tree, a population of definitions that is not 3-with-2-bodies,")
print("a repaired positive control, and a count row of this tree with no")
print("grain line under it.")
print()
print(B.finding("F4a", "%d of %d arc tripwires asserting this exclusion as "
                       "false went RED on the repair and both are re-pointed "
                       "rather than deleted; `figures` has %d definition(s) "
                       "in the arc with %d own body(ies) and %d in this tree; "
                       "%d of %d count rows here name their grain"
                % (fired, len(OLD), tot, own_body, here_defs, graine, rows)))
sys.exit(min(BAD, 120))
