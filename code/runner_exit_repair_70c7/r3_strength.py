"""R3 -- THE RULE IT APPLIED TO ITSELF.  mg-dee4's F3 and F4, repaired.

F3.  mg-7522 pointed a NINE-alternative marker rule at its subject
(`s3_figure.MARK`) and a THREE-alternative one at itself
(`lib7522._STRENGTH`) -- and `verified`, named as one of the three markers in
`s5_self.py`'s own D4 docstring, in the README and in the published document,
was in the nine and not in the three.  The self-facing population was
`MINE_PY + MINE_SH`, so the README, `OUTCOMES.md`, `PREDICTIONS.md` and the
published document were all outside it, and THREE OF THE FOUR ARTIFACTS
mg-05eb's OPEN 2 found wrong were exactly that kind.

> A nine-alternative test for them and a three-alternative one for you is not a
> stricter standard applied leniently.  It is a DIFFERENT INSTRUMENT, and it
> will not find what theirs finds.

F4.  The rule that produces the subject-facing count is LINE-LOCAL: a claim is
a LINE carrying both a marker and a number.  In hard-wrapped prose the marker
and its figure land on different lines routinely, and the claim mg-dee4 most
wanted to check -- `runner_exit_repair_7522/OUTCOMES.md:88`, *"…counts the same
bytes the pipeline did, verified against the"*, figure on line 89 -- scored as
neither line.

WHAT THIS PROBE CHECKS.  That there is now ONE rule object; that it reaches
`verified`; that the self-facing population contains the `.md`; that the
verdict is BACKED-or-UNBACKED rather than a count of uses; and that the window
is one line in either direction, with the 20 -> 24 and 31 -> 40 movements
re-derived here under this tree's own copy of the rule.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

sys.path.insert(0, os.path.join(M.REPO, M.SUBJECT))
import lib7522 as L                                            # noqa: E402

BAD = 0
NUM = re.compile(r"\b\d+\b")

M.bar("R3  APPLY TO YOURSELF THE RULE YOU APPLY TO YOUR SUBJECT")

# ---------------------------------------------------------------------------
M.hdr("R3a  ONE RULE OBJECT, POINTED IN BOTH DIRECTIONS")

s3 = M.read("%s/s3_figure.py" % M.SUBJECT, None)
s5 = M.read("%s/s5_self.py" % M.SUBJECT, None)
lib = M.read("%s/lib7522.py" % M.SUBJECT, None)

print("  Read out of the SOURCE, not taken from the prose.  Two rules cannot")
print("  be kept in step by intention; they can be kept in step by being one")
print("  object.")
print()
own_marks = re.findall(r"^MARK\s*=\s*re\.compile", s3, re.M)
shared = re.findall(r"^MARK\s*=\s*L\.MARK\s*$", s3, re.M)
lib_mark = re.findall(r"^MARK\s*=\s*re\.compile", lib, re.M)
# A `>=` where the point is "at least one, and none of its own" and an `==`
# where the point is "exactly one object".  Counting call SITES exactly would
# be a rule about how often a function is called, which is not the property.
rows = [
    ("s3_figure.py defines its OWN marker regex", len(own_marks), 0, "=="),
    ("s3_figure.py uses the library's", len(shared), 1, "=="),
    ("s5_self.py defines its OWN marker regex",
     len(re.findall(r"^\s*(?:_STRENGTH|MARK)\s*=\s*re\.compile", s5, re.M)),
     0, "=="),
    ("s5_self.py calls the library's rule", len(re.findall(
        r"L\.strength_lines\(", s5)), 1, ">="),
    ("lib7522.py defines the one rule", len(lib_mark), 1, "=="),
]
for label, got, want, op in rows:
    ok = (got == want) if op == "==" else (got >= want)
    if not ok:
        BAD += 1
    print("      %-52s %d   %s" % (label, got,
                                   "OK" if ok else "*** want %s%d ***"
                                   % (op, want)))
print()
print("      alternatives in the rule pointed at the SUBJECT   %2d"
      % M.alternatives(L.MARK))
print("      alternatives in the rule it used on ITSELF        %2d   (kept as"
      % M.alternatives(L.MARK_OLD))
print("                                                             MARK_OLD,")
print("                                                             for the")
print("                                                             exhibition")
print("                                                             below)")
print()
NAMED = ("confirmed exactly", "verified", "byte-identical")
print("  THE THREE MARKERS THE D4 DOCSTRING NAMES, each put to both rules:")
print()
print("      %-22s %-12s %s" % ("marker", "old rule", "the one rule"))
for w in NAMED:
    a = bool(L.MARK_OLD.search(w))
    b = bool(L.MARK.search(w))
    print("      %-22s %-12s %s" % ("`%s`" % w, "yes" if a else "NO",
                                    "yes" if b else "*** NO ***"))
    if not b:
        BAD += 1
print()
print("  `verified` is the one the docstring named and the rule did not have.")

# ---------------------------------------------------------------------------
M.hdr("R3b  THE POPULATION -- does the self-check see its own prose?")

pop = re.findall(r"MINE_ALL\s*=", s5)
md = re.findall(r"MINE_MD\s*=", s5)
doc = "docs/OneThird-RunnerExit-PopulationRepair.md" in s5
print("      s5_self.py builds a population including `*.md`     %s"
      % ("yes" if md else "*** NO ***"))
print("      ...and the published document                       %s"
      % ("yes" if doc else "*** NO ***"))
print("      ...and uses it for D4                               %s"
      % ("yes" if pop else "*** NO ***"))
if not (md and doc and pop):
    BAD += 1
print()
here = os.path.join(M.REPO, M.SUBJECT)
n_py = len([f for f in os.listdir(here) if f.endswith(".py")])
n_sh = len([f for f in os.listdir(here) if f.endswith(".sh")])
n_md = len([f for f in os.listdir(here) if f.endswith(".md")])
print("      the OLD population  (`*.py` + `*.sh`)               %2d file(s)"
      % (n_py + n_sh))
print("      the population now  (+ `*.md` + the document)       %2d file(s)"
      % (n_py + n_sh + n_md + 1))
print()
print("  mg-05eb's OPEN 2 was one figure wrong in FOUR artifacts.  Three of")
print("  them -- the README, `OUTCOMES.md` and the published document -- are")
print("  of the kind the old population could not contain.  A self-check")
print("  whose population stops at two suffixes has a population defined by")
print("  a name, which is the finding one directory over.")

# ---------------------------------------------------------------------------
M.hdr("R3c  THE VERDICT -- BACKED or UNBACKED, re-derived independently")

print("  A bare marker beside a figure the tree COMPUTED is not the defect;")
print("  a bare marker beside a figure nothing here produces is.  Re-derived")
print("  under this tree's own `figures()` and `transcript_numbers()`, which")
print("  share no code with `lib7522`'s:")
print()
MY_OUTS = M.outs(M.SUBJECT) + M.outs(M.TREE)
CORPUS = M.transcript_numbers(MY_OUTS)
pop_files = (["%s/%s" % (M.SUBJECT, f) for f in sorted(os.listdir(here))
              if f.endswith((".py", ".sh", ".md"))] + [M.DOC])
backed = unbacked = nofig = mentions = 0
rows = []
for rel in pop_files:
    lines = M.read(rel, None).splitlines()
    for i, line, kind in L.strength_lines("\n".join(lines)):
        if kind == "MENTION":
            mentions += 1
            continue
        figs = []
        for n in lines[max(0, i - 2):i + 1]:
            figs.extend(M.figures(n))
        if not figs:
            nofig += 1
        elif [v for v in figs if v not in CORPUS]:
            unbacked += 1
            rows.append((rel, i, line, [v for v in figs if v not in CORPUS]))
        else:
            backed += 1
print("      MENTIONs                                   %3d" % mentions)
print("      USEs BACKED by a transcript                %3d" % backed)
print("      USEs with no figure in the window          %3d" % nofig)
print("      USEs UNBACKED                              %3d" % unbacked)
print()
for rel, i, line, miss in rows:
    print("      *** %s:%d  %s" % (os.path.basename(rel), i, line[:52]))
    print("          unbacked: %s" % ", ".join(str(v) for v in miss))
if unbacked:
    BAD += unbacked
else:
    print("      Every figure a marker is applied to in that tree is printed")
    print("      by one of its own transcripts.")
print()
print("  AND THE SAME QUESTION PUT TO `out_s5_self.txt`, so this is a check")
print("  on the repaired probe and not a second opinion about the tree:")
try:
    t = M.read("%s/out_s5_self.txt" % M.SUBJECT, None)
    m = re.search(r"USEs, UNBACKED\s+(\d+)", t)
    theirs = int(m.group(1)) if m else None
    print("      s5_self.py's own transcript reports UNBACKED   %s"
          % ("-" if theirs is None else theirs))
    if theirs is not None and theirs != unbacked:
        BAD += 1
        print("      *** the two derivations disagree (%d here) ***" % unbacked)
except (RuntimeError, OSError):
    print("      (no transcript yet -- first pass of run_all.sh)")

# ---------------------------------------------------------------------------
M.hdr("R3d  F4 -- THE CLAIM WINDOW, both populations, both widths")

print("  A CLAIM is a strength marker with a number near it.  `near` was")
print("  `on the same line`.  Both widths are run over both populations here,")
print("  so the movement is a measured row and not an assertion:")
print()
TOUCHED = [p for p in M.git("show", "--name-only", "--format=", "52aeaf4")
           .split() if p]
C2B3 = [p for p in sorted(TOUCHED)
        if (p.startswith("code/runner_exit_c2b3/")
            or (p.startswith("docs/") and p.endswith(".md")))
        and not os.path.basename(p).startswith("out_")]
MINE7522 = [p for p in sorted(os.listdir(here))
            if p.endswith((".py", ".sh", ".md"))]
MINE7522 = ["%s/%s" % (M.SUBJECT, p) for p in MINE7522] + [M.DOC]


def claims(paths, window):
    n, added = 0, []
    for p in paths:
        lines = M.read(p, None).splitlines()
        for i, line in enumerate(lines, 1):
            if not L.MARK.search(line):
                continue
            near = lines[max(0, i - 1 - window):i + window]
            if any(NUM.search(x) for x in near):
                n += 1
                if not NUM.search(line):
                    added.append((p, i, line.strip()))
    return n, added


for label, paths, expect in (("mg-c2b3's artifacts (S3a's subject)", C2B3,
                              (20, 24)),
                             ("mg-7522's own artifacts", MINE7522, None)):
    w0, _a0 = claims(paths, 0)
    w1, a1 = claims(paths, 1)
    print("      %-42s window 0: %3d   window 1: %3d   (+%d)"
          % (label, w0, w1, w1 - w0))
    if expect and (w0, w1) != expect:
        print("          (mg-dee4 measured %d and %d)" % expect)
    for p, i, line in a1:
        print("          + %s:%d  %s" % (os.path.basename(p), i, line[:56]))
print()
print("  THE ONE THE FINDING IS ABOUT is in the second population:")
try:
    o = M.read("%s/OUTCOMES.md" % M.SUBJECT, None).splitlines()
    idx = [i for i, l in enumerate(o, 1) if "counts the same bytes" in l]
    for i in idx:
        print("      OUTCOMES.md:%d  %s" % (i, o[i - 1].strip()[:62]))
        print("      OUTCOMES.md:%d  %s" % (i + 1, o[i].strip()[:62]))
        print("          marker on the first line, figure on the second --")
        print("          a line-local rule sees neither as a claim.")
except (RuntimeError, OSError, IndexError):
    pass
print()
w = re.findall(r"^WINDOW\s*=\s*(\d+)", s3, re.M)
print("      `s3_figure.WINDOW` is now                          %s"
      % (w[0] if w else "*** absent ***"))
sym = "max(0, i - 1 - WINDOW)" in s3
print("      ...and applied in BOTH directions                  %s"
      % ("yes" if sym else "*** NO ***"))
if not w or w[0] != "1" or not sym:
    BAD += 1

print()
M.bar("R3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a second marker regex in the subject")
print("tree, a named marker the one rule does not reach, a self-facing")
print("population that cannot see its own `*.md`, an UNBACKED use, a")
print("disagreement between this derivation and `out_s5_self.txt`, and a")
print("claim window that is not one line in both directions.  It ranges over")
print("mg-7522's %d artifacts and mg-c2b3's %d.  It does NOT judge whether a"
      % (len(MINE7522), len(C2B3)))
print("BACKED figure is backed by the RIGHT measurement -- that is the weak")
print("direction of the backing test and it is stated in `lib7522` where the")
print("rule lives.")
sys.exit(1 if BAD else 0)
