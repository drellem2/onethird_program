"""R1 -- THE GRAIN OF THE RETROACTIVE CLEARANCE.  mg-dee4's F1, repaired.

THE FINDING.  mg-7522 wrote *"the 11 discarded statuses read directly, 11 of 11
exit 0, so the corrected population of 45 has now been read in full"*.  Eleven
was a count of SOURCE LINES.  Eight of them are `| tee` pipelines and were
derived from the runners' own bytes; three are `git diff … | wc -c` lines that
sit inside `for pair in …` loops and execute EIGHT `git diff`s between them, and
they were covered by a HAND-LIST of three argv containing two distinct commands.
Four of the eight runs were never executed, and one row was labelled
`state_delegation_audit_16eb/run_all.sh:39` while carrying an argv without the
`':!*.md'` pathspec that line 39 has -- so that form was never run in any shape.

THE REPAIR, and what this probe checks:

  R1a  the executions are DERIVABLE from the runners' bytes -- re-derived here
       under this tree's own parser, which shares no code with `lib7522`;
  R1b  `s2_status.py` no longer contains a hand-list, and the rows it builds
       are exactly the rows derived here;
  R1c  the four runs mg-7522 never executed are named, one at a time;
  R1d  all eight exit 0, so the VERDICT survives and only the arithmetic did
       not -- the finding is about the word DIRECTLY and about the population;
  R1e  the four reader-facing artifacts state the GRAIN in the sentence.

WHY THE PARSER IS WRITTEN TWICE.  `lib7522` now carries the derivation, because
that is where the check lives.  `lib70c7` carries its own, because a repair
that re-derived its subject's number with its subject's parser would agree with
itself by construction -- which is mg-dee4's reason for importing nothing, one
level down.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib70c7 as M

sys.path.insert(0, os.path.join(M.REPO, M.SUBJECT))
import lib7522 as L                                            # noqa: E402

BAD = 0
PRE = M.REPAIR_REV + "^"
RUNNERS = ("code/state_delegation_audit_16eb/run_all.sh",
           "code/state_delegation_repair_0049/run_all.sh")
PIPE = re.compile(r"(?<!\|)\|(?!\|)(?!&)")

M.bar("R1  THE GRAIN -- SITES ARE NOT RUNS")

# ---------------------------------------------------------------------------
M.hdr("R1a  THE EXECUTIONS, RE-DERIVED UNDER AN INDEPENDENT PARSER")

print("  Read at %s -- the bytes mg-7522 repaired -- because that is where" % PRE)
print("  the pipelines still exist.  `lib70c7` implements the loop expansion")
print("  from scratch; `lib7522` now implements it too, and R1b checks that")
print("  the two agree row for row.")
print()

mine = []
for rel in RUNNERS:
    src = M.read(rel, PRE)
    loops = M.for_loops(src)
    print("    %s" % rel)
    for var, items, first, last in loops:
        print("        `for %s in …` at lines %d-%d: %s"
              % (var, first, last,
                 "%d literal item(s)" % len(items) if items
                 else "*** NOT statically expandable ***"))
    for line, it, bind, text in M.pipeline_executions(rel, src, PIPE):
        if "git diff" not in text:
            continue
        if bind is None:
            print("        %4d  *** iteration not derivable ***" % line)
            BAD += 1
            continue
        lp = [l for l in loops if l[2] <= line <= l[3]]
        full = M.loop_bindings(src, lp[0][2], lp[0][3], bind) if lp else bind
        argv = M.argv_of(text.split("|")[0], full)
        if argv is None:
            print("        %4d  *** argv not derivable ***" % line)
            BAD += 1
            continue
        mine.append((rel, line, it, argv))
print()
print("    %-46s %-6s %s" % ("source line", "iter", "argv actually run"))
for rel, line, it, argv in mine:
    print("    %-46s %-6d %s"
          % (rel.replace("code/", "") + ":%d" % line, it, " ".join(argv[1:])))
print()
print("      pipeline SOURCE LINES                        %3d"
      % len({(r, l) for r, l, _i, _a in mine}))
print("      DISCARDED `git diff` EXECUTIONS              %3d" % len(mine))
print("      DISTINCT commands among them                 %3d"
      % len({tuple(a) for _r, _l, _i, a in mine}))

# ---------------------------------------------------------------------------
M.hdr("R1b  `s2_status.py` NO LONGER CARRIES A HAND-LIST")

s2 = M.read("%s/s2_status.py" % M.SUBJECT, None)
handlist = re.findall(r'\["git",\s*"diff"', s2)
print("  A hand-written argv in the source is the thing that drifted from the")
print("  line it was labelled with.  Counted structurally, on the bytes:")
print()
print("      literal `[\"git\", \"diff\", …]` argv in s2_status.py    %3d"
      % len(handlist))
if handlist:
    BAD += len(handlist)
    print("      *** the hand-list is back ***")

theirs = []
for rel in RUNNERS:
    src = L.read(rel, L.PINNED)
    for line, it, bind, text in L.pipeline_executions(src):
        if bind is None:
            continue
        argv = L.argv_of(L.discarded_stages(text)[0], bind)
        if argv:
            theirs.append((rel, line, it, argv))
print()
print("      rows the REPAIRED s2 derivation produces         %3d" % len(theirs))
print("      rows THIS tree's independent parser produces     %3d" % len(mine))
same = sorted(theirs) == sorted(mine)
print("      the two parsers agree row for row                 %s"
      % ("yes" if same else "*** NO ***"))
if not same:
    BAD += 1
    for row in sorted(set(map(str, theirs)) ^ set(map(str, mine))):
        print("          only one side: %s" % row)

# ---------------------------------------------------------------------------
M.hdr("R1c  THE FOUR RUNS mg-7522 NEVER EXECUTED, ONE AT A TIME")

WAS_RUN = [
    ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"],
    ["git", "diff", "3a80d99..HEAD", "--", "code/state_delegation_audit_5644"],
    ["git", "diff", "a4aeeb9..HEAD", "--", "code/state_layer_audit_218d"],
]
print("  mg-7522's three hand-written argv, quoted from `1ee1f1b`:")
for a in WAS_RUN:
    print("      %s" % " ".join(a))
print()
ran = {tuple(a) for a in WAS_RUN}
missed = [(r, l, i, a) for r, l, i, a in mine if tuple(a) not in ran]
print("      EXECUTIONS at run time                       %3d" % len(mine))
print("      ...covered by one of the three argv          %3d"
      % (len(mine) - len(missed)))
print("      ...NEVER RUN by mg-7522                      %3d" % len(missed))
print()
for r, l, i, a in missed:
    print("      %-46s %s" % (r.replace("code/", "") + ":%d#%d" % (l, i),
                              " ".join(a[1:])))
print()
pathspec = [x for x in missed if ":!*.md" in x[3]]
print("  AND THE ROW THAT WAS LABELLED WITH A LINE IT DID NOT RUN.  Line 39 of")
print("  state_delegation_audit_16eb carries a `':!*.md'` pathspec and none of")
print("  the three argv has one, so NO execution of that line's discarded")
print("  stage was ever read: %d of the %d never-run executions are that form."
      % (len(pathspec), len(missed)))

# ---------------------------------------------------------------------------
M.hdr("R1d  ALL EIGHT, READ DIRECTLY -- the verdict, which survives")

print("  LIST argv, no shell, so `returncode` is the target's own status.")
print("  This is mg-c2b3's K3b method and mg-7522's own, at the grain the")
print("  source executes at rather than the grain it is written at.")
print()
print("  %-46s %-40s %s" % ("execution", "discarded stage", "exit"))
nonzero = 0
for r, l, i, a in mine:
    code, _out = M.run_argv(a, M.REPO)
    if code != 0:
        nonzero += 1
    print("  %-46s %-40s %s"
          % (r.replace("code/", "") + ":%d#%d" % (l, i),
             " ".join(a[1:])[:40], "-" if code is None else code))
print()
if nonzero:
    BAD += nonzero
    print("  *** %d of %d exit non-zero -- a status the pipeline hid ***"
          % (nonzero, len(mine)))
else:
    print("  %d of %d exit 0.  SO THE VERDICT SURVIVES AND THE ENUMERATION DID"
          % (len(mine), len(mine)))
    print("  NOT.  Nothing was being swallowed; the finding is that a count of")
    print("  SITES was presented as a count of RUNS, and four of the eight")
    print("  runs had not been looked at when the sentence was written.")

# ---------------------------------------------------------------------------
M.hdr("R1e  DO THE READER-FACING ARTIFACTS STATE THE GRAIN?")

print("  A repair of a number that leaves the sentence alone has repaired")
print("  nothing a reader will see.  Four artifacts carried `11 of 11`:")
print()
ARTIFACTS = ["%s/s2_status.py" % M.SUBJECT,
             "%s/README.md" % M.SUBJECT,
             "%s/OUTCOMES.md" % M.SUBJECT,
             M.DOC]
GRAIN = re.compile(r"\bEXECUTIONS?\b|\bexecution grain\b|\bexecutions\b",
                   re.I)
OLD = re.compile(r"11 of 11|45 of 45")
# A line carrying the old figure is an ASSERTION of it unless it is also
# CORRECTING it.  Same mention-vs-use distinction this arc runs on, one more
# level down -- and see OUTCOMES.md for what the first draft of this check did
# without it.
FIXING = re.compile(r"used to|was a count|mg-dee4|mg-70c7|no longer|"
                    r"same shape as|once said|is not|did not|corrected", re.I)
table = []
for p in ARTIFACTS:
    lines = M.read(p, None).splitlines()
    hits = [(i, l) for i, l in enumerate(lines, 1) if OLD.search(l)]
    asserted = [(i, l) for i, l in hits if not FIXING.search(l)]
    grain = len(GRAIN.findall("\n".join(lines)))
    ok = not asserted and grain > 0
    if not ok:
        BAD += 1
    table.append((os.path.basename(p)[:32],
                  "%d quoted" % len(hits),
                  "%d asserted" % len(asserted),
                  "%d grain word(s) -- %s"
                  % (grain, "OK" if ok else "*** still asserted ***")))
M.rows(table, (34, 10, 12))
for p in ARTIFACTS:
    for i, l in [(i, l) for i, l in enumerate(M.read(p, None).splitlines(), 1)
                 if OLD.search(l) and not FIXING.search(l)]:
        print("      *** %s:%d  %s" % (os.path.basename(p), i, l.strip()[:60]))
print()
print("  QUOTED and ASSERTED are counted separately on purpose.  The first")
print("  draft of this check forbade the string outright, and every artifact")
print("  that had correctly described what it repaired went red for saying so")
print("  -- a check that would have been satisfied by DELETING the record of")
print("  the defect.  Recorded in OUTCOMES.md rather than quietly fixed.")

print()
M.bar("R1 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts an execution this tree's parser could")
print("not derive, a hand-written argv in `s2_status.py`, a disagreement")
print("between the two parsers, a non-zero discarded status among the 8, and")
print("an artifact still carrying the line-grain figure.  It ranges over the 3")
print("`git diff` source lines of 2 runners at %s and the 8 executions they" % PRE)
print("run.  It does NOT range over the 8 `| tee` sites, which mg-7522 derived")
print("correctly and mg-dee4 confirmed, nor over mg-c2b3's own 34, which are")
print("INHERITED from a transcript neither audit re-ran.")
sys.exit(1 if BAD else 0)
