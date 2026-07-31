"""A4 -- THE REPAIR'S OWN STRONGEST WORDING, CHECKED FIRST.

mg-7522 states a general form and states it three times:

    "Confirmed exactly", "verified", "byte-identical" and their relatives mark
     the place where the author stopped looking.  They are a reason to check
     FIRST, not a reason to skip.

It then applies that form to its SUBJECT with a nine-alternative rule
(`s3_figure.MARK`), finds 20 strength-marked numeric claims and dispositions
every one.  And it applies it to ITSELF with a different rule
(`lib7522._STRENGTH`) over a different population (`MINE_PY + MINE_SH`), and
reports **0 USES, 19 MENTIONs**.

This probe does not dispute the 0.  It measures the two rules and the two
populations against each other, and then does the one thing that settles it:
runs mg-7522's OWN subject-facing rule over mg-7522's OWN artifacts.

  A4a  THE TWO RULES, SIDE BY SIDE.  Alternative by alternative.
  A4b  THE TWO POPULATIONS.  What `MINE_PY + MINE_SH` contains, and what the
       four reader-facing artifacts of mg-7522 are.
  A4c  MG-7522'S SUBJECT RULE, TURNED ON MG-7522.  `MARK` + `NUM` over the
       artifacts of `1ee1f1b`, derived from `git show --name-only` exactly as
       S3a derives the sweep's.
  A4d  THE ONE PLACE A SUPERLATIVE IS DOING WORK NO INSTRUMENT DOES.  Every
       occurrence of a marker in mg-7522's artifacts is checked for whether
       a probe in its own tree prints the figure it is attached to.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libdee4 as L

BAD = 0
FINDINGS = []

L.bar("A4  THE REPAIR'S OWN STRONGEST WORDING")

# The two rules, copied from mg-7522's source so that the comparison is with
# what RUNS and not with what is written about what runs.
STRENGTH_SELF = re.compile(r"confirmed exactly|byte-identical|\bproven\b", re.I)
MARK_SUBJECT = re.compile(r"confirmed exactly|byte-identical|byte for byte"
                          r"|\bverified\b|\(measured\)|\bidentical\b"
                          r"|\bconfirmed\b|\ball (?:\d+|of)\b|\bexactly \d+\b",
                          re.I)
NUM = re.compile(r"\b\d+\b")
DELIM = "\"'`*"
MENTION_SIGNALS = ("re.compile", "ck(", "_STRENGTH", "strength_lines",
                   "MARK =", "STALE =", "STRONG =", "<- USE", "<- MENTION")

# ---------------------------------------------------------------------------
L.hdr("A4a  THE RULE IT JUDGES ITSELF BY, AND THE RULE IT JUDGES ITS SUBJECT BY")

SELF_ALTS = ["confirmed exactly", "byte-identical", "proven"]
SUBJ_ALTS = ["confirmed exactly", "byte-identical", "byte for byte",
             "verified", "(measured)", "identical", "confirmed",
             "all <n> / all of", "exactly <n>"]
NAMED = ["confirmed exactly", "verified", "byte-identical"]

print("  The three markers mg-7522 NAMES, in `s5_self.py`'s D4 docstring, in")
print("  its README and in the published document:")
print()
for m in NAMED:
    in_self = m in SELF_ALTS
    in_subj = m in SUBJ_ALTS
    print("      %-20s in the SELF rule: %-5s   in the SUBJECT rule: %s"
          % ("`%s`" % m, in_self, in_subj))
    if not in_self:
        BAD += 1
        FINDINGS.append(
            "A4a `%s` is named as one of the three markers in the D4 "
            "docstring, in the README and in the published document, and is "
            "absent from `lib7522._STRENGTH` -- the rule that produces the "
            "`0 USES` those documents print" % m)
print()
print("      alternatives in the SELF rule    %2d   %s"
      % (len(SELF_ALTS), ", ".join(SELF_ALTS)))
print("      alternatives in the SUBJECT rule %2d   %s"
      % (len(SUBJ_ALTS), ", ".join(SUBJ_ALTS)))
print("      in SELF and not in SUBJECT       %2d   %s"
      % (len([a for a in SELF_ALTS if a not in SUBJ_ALTS]),
         ", ".join(a for a in SELF_ALTS if a not in SUBJ_ALTS)))
print("      in SUBJECT and not in SELF       %2d   %s"
      % (len([a for a in SUBJ_ALTS if a not in SELF_ALTS]),
         ", ".join(a for a in SUBJ_ALTS if a not in SELF_ALTS)))
print()
print("  THE DOCSTRING OF THE CHECK, verbatim, next to the regex that runs it:")
s5 = L.read("%s/s5_self.py" % L.TREE, None)
for l in s5.splitlines():
    if "A STRENGTH MARKER STANDING IN FOR A CHECK" in l or (
            '"verified", "byte-identical"' in l):
        print("      %s" % l.strip())
lib = L.read("%s/lib7522.py" % L.TREE, None)
for i, l in enumerate(lib.splitlines(), 1):
    if l.startswith("_STRENGTH"):
        print("      lib7522.py:%d  %s" % (i, l.strip()))

# ---------------------------------------------------------------------------
L.hdr("A4b  THE TWO POPULATIONS")

HERE_FILES = sorted(f for f in L.git("ls-files", "--", "%s/*" % L.TREE).split()
                    if f)
mine = [f for f in HERE_FILES if f.endswith((".py", ".sh"))]
md = [f for f in HERE_FILES if f.endswith(".md")]
print("      `MINE_PY + MINE_SH`, the D4 population          %2d files" % len(mine))
print("      `*.md` in the same directory, OUTSIDE it        %2d files" % len(md))
for f in md:
    print("          %s" % f)
print("      the published document, OUTSIDE it               1 file")
print("          %s" % L.DOC)
print()
print("  WHY THAT MATTERS HERE AND NOT IN GENERAL.  mg-05eb's OPEN 2 -- the")
print("  defect this section of mg-7522 repairs -- was a figure wrong in FOUR")
print("  reader-facing artifacts: the README, `OUTCOMES.md`, the published")
print("  document, and one docstring.  Three of those four are file kinds the")
print("  D4 population excludes.  The check is aimed away from where its own")
print("  subject's defect lived.")
print()
print("  MG-7522 STATES THIS EXTENT -- in the transcript, not in the summary:")
for l in L.read("%s/out_s5_self.txt" % L.TREE, None).splitlines():
    if "does not range over the rest" in l or "`*.sh` files only" in l or (
            "EXTENT OF THAT NUMBER" in l):
        print("      %s" % l.strip())
print()
readme = L.read("%s/README.md" % L.TREE, None)
doc = L.read(L.DOC, None)
for name, text in (("README.md", readme), ("the published document", doc)):
    lines = [l.strip() for l in text.splitlines()
             if "USES" in l or ("0 uses" in l)]
    for l in lines:
        carries = "py" in l.lower() and "sh" in l.lower()
        print("      %-24s %s" % (name, l[:52]))
        if not carries:
            BAD += 1
            FINDINGS.append(
                "A4b %s prints `0 USES` without the extent its own transcript "
                "states -- the count ranges over `*.py` and `*.sh` only, and "
                "the README, OUTCOMES.md and the published document are "
                "outside it" % name)
print()
print("  THAT IS MG-7522'S OWN F3, WITH THE ROLES UNCHANGED: the instrument")
print("  was right, printed its extent, and the summary dropped it.")

# ---------------------------------------------------------------------------
L.hdr("A4c  MG-7522'S SUBJECT RULE, TURNED ON MG-7522")

print("  S3a's predicate, verbatim: a reader-facing artifact is a file the")
print("  commit touched, under the instrument's directory or under `docs/`,")
print("  that is not a committed transcript.  A CLAIM is a line carrying BOTH")
print("  a strength marker and a number.  Here the commit is %s." % L.REPAIR)
print()
TOUCHED = [p for p in L.git("show", "--name-only", "--format=", L.REPAIR).split()
           if p]
ART = sorted(p for p in TOUCHED
             if p.startswith("%s/" % L.TREE)
             or (p.startswith("docs/") and p.endswith(".md")))
ART = [p for p in ART if not os.path.basename(p).startswith("out_")]
print("      artifacts: %d" % len(ART))
for p in ART:
    print("          %s" % p)
print()
CLAIMS = []
for p in ART:
    if not L.exists(p, None):
        continue
    for i, line in enumerate(L.read(p, None).splitlines(), 1):
        if MARK_SUBJECT.search(line) and NUM.search(line):
            CLAIMS.append((p, i, line.strip()))
print("      strength-marked numeric claims in mg-7522's own artifacts: %d"
      % len(CLAIMS))
print()

# Disposition rules, keyed on a SUBSTRING OF THE LINE -- not on a line number,
# because a key that the act of repairing invalidates is the defect this arc
# keeps finding.  Coverage is checked in BOTH directions.
DISP = [
    ("quotation", r"confirmed exactly|`\| \*tee`|ticket 1|all 34 carried|"
     r"all 64|all 23 uniformly|byte for byte|past green is confirmed|"
     r"used to read|docstring all|the population of every number|"
     r"34 tee'd targets|at exactly 3|reach is identical|bare grep|"
     r"printed `ticket 1|About 4 minutes|at all 17 runners",
     "mg-c2b3's OWN wording, being dispositioned by S3b; a mention"),
    ("own rule", r"MARK = re\.compile|STALE = re\.compile|_STRENGTH|"
     r"NOT A CLAIM|WAS WRONG, NOW FIXED|HOLDS",
     "a detecting regex or a disposition verdict; a mention"),
    ("re-derived", r"11 of 11|8 of 8|59 of 64|all 11 discarded|all 8 pre-repair|"
     r"exactly one|EXACTLY ONE",
     "a figure a probe in this tree recomputes in the run that prints it"),
    ("prose about the subject", r"read directly|the sweep said it had "
     r"confirmed|34 of 34, all 0|discarded status of everything outside",
     "a sentence describing mg-c2b3's result or this tree's own layout; the "
     "number in it is mg-c2b3's population, re-derived in S1 and A1a"),
    ("stated runtime", r"About 20 minutes",
     "a stated wall-clock, not a measurement of the subject; the same "
     "disposition S3b gives mg-c2b3's `About 4 minutes` row"),
]
table, undisp, uses = [], [], []
for p, ln, line in CLAIMS:
    hit = [d for d in DISP if re.search(d[1], line)]
    if not hit:
        undisp.append((p, ln, line))
        table.append(("%s:%d" % (os.path.basename(p), ln), "UNDISPOSITIONED",
                      "*** no rule matches this line ***"))
        continue
    d = hit[0]
    if d[0] == "verified byte counts":
        uses.append((p, ln, line))
    table.append(("%s:%d" % (os.path.basename(p), ln), d[0], d[2]))
print("    %-30s %-22s %s" % ("artifact", "disposition", "how it was checked"))
L.rows(table, (30, 22), indent="    ")
print()
counts = {}
for _a, v, _h in table:
    counts[v] = counts.get(v, 0) + 1
print("      %d claims: %s" % (len(CLAIMS),
                               ", ".join("%d %s" % (n, k)
                                         for k, n in sorted(counts.items()))))
print()
print("  COVERAGE, BOTH DIRECTIONS.  A hit with no rule and a rule with no hit")
print("  are each an error -- mg-7522's own standard, applied to mg-7522.")
for name, rx, _why in DISP:
    n = len([1 for _p, _l, line in CLAIMS if re.search(rx, line)])
    print("      rule %-22s matched %d line(s)  %s"
          % ("`%s`" % name, n, "" if n else "*** ROTTED ***"))
    if not n:
        BAD += 1
        FINDINGS.append("A4c disposition rule `%s` matches nothing" % name)
if undisp:
    BAD += len(undisp)
    for p, ln, line in undisp:
        FINDINGS.append("A4c undispositioned strength-marked claim %s:%d  %s"
                        % (p, ln, line[:60]))
print()
print("      claims mg-7522's SELF rule would have caught: %d"
      % len([1 for _p, _l, line in CLAIMS if STRENGTH_SELF.search(line)]))
print("      claims mg-7522's SUBJECT rule catches:        %d" % len(CLAIMS))
print()
print("  THE POINT IS NOT THAT %d IS ALARMING.  Almost every one is mg-c2b3's" % len(CLAIMS))
print("  own wording being quoted while it is dispositioned -- which is what")
print("  a repair of a wording defect looks like.  The point is that the")
print("  number mg-7522 published about itself is 0, and 0 is what you get")
print("  when the rule has three alternatives instead of nine and the")
print("  population excludes every `.md`.")

# ---------------------------------------------------------------------------
L.hdr("A4d  THE CLAIM RULE IS LINE-LOCAL, AND THE STRONGEST CLAIM WRAPPED")

print("  S3a scores a CLAIM as a LINE carrying both a marker and a number.")
print("  In a hard-wrapped markdown paragraph the marker and its figure land")
print("  on different lines routinely.  The claim this audit most wanted to")
print("  check is exactly such a case:")
print()
oc = L.read("%s/OUTCOMES.md" % L.TREE, None).split("\n")
for i, l in enumerate(oc, 1):
    if "verified against" in l:
        print("      OUTCOMES.md:%d  %s" % (i, l.strip()))
        print("                     ^ marker `verified`, digits on this line: %s"
              % bool(NUM.search(l)))
        print("      OUTCOMES.md:%d  %s" % (i + 1, oc[i].strip()))
        print("                     ^ the figure.  A line-local rule sees")
        print("                       neither line as a claim.")
print()
print("  THE SAME RULE WITH A ONE-LINE WINDOW, over both populations:")
print()


def claims(paths, window):
    out = []
    for p in paths:
        if not L.exists(p, None):
            continue
        ls = L.read(p, None).split("\n")
        for i, line in enumerate(ls, 1):
            if not MARK_SUBJECT.search(line):
                continue
            near = "\n".join(ls[max(0, i - 1 - window):i + window])
            if NUM.search(near):
                out.append((p, i, line.strip()))
    return out


SWEEP_TOUCHED = [p for p in L.git("show", "--name-only", "--format=",
                                  L.SWEEP).split() if p]
SWEEP_ART = [p for p in sorted(SWEEP_TOUCHED)
             if (p.startswith("code/runner_exit_c2b3/")
                 or (p.startswith("docs/") and p.endswith(".md")))
             and not os.path.basename(p).startswith("out_")]
for label, paths, published in (("mg-c2b3's artifacts (S3a's own subject)",
                                 SWEEP_ART, 20),
                                ("mg-7522's own artifacts", ART, None)):
    n0 = len(claims(paths, 0))
    n1 = len(claims(paths, 1))
    print("      %-42s window 0: %3d   window 1: %3d   (+%d)"
          % (label, n0, n1, n1 - n0))
    if published is not None:
        print("          mg-7522 published %d for this population."
              % published)
        if n1 > n0:
            FINDINGS.append(
                "A4d S3a's CLAIM rule is LINE-LOCAL: a marker and its figure "
                "on adjacent lines is not scored.  Widening the window by one "
                "line takes mg-c2b3's own artifacts from %d to %d claims, so "
                "the published `%d strength-marked numeric claims, every one "
                "dispositioned` is a count under a rule that a hard wrap can "
                "step over" % (n0, n1, published))
print()
print("  DOES ANY PROBE IN MG-7522'S TREE PRODUCE THAT FIGURE?  Asked of the")
print("  OUTPUT, not of the source.  A grep of the source for `wc -c` scores")
print("  the comment that explains why `wc -c` is no longer in a pipeline --")
print("  which is the mention-for-occurrence defect mg-7522 recorded three")
print("  times in its own OUTCOMES.md.  So the question is put to the")
print("  committed transcripts instead: does the number appear in any of them?")
print()
TRANSCRIPTS = [f for f in HERE_FILES if os.path.basename(f).startswith("out_")]
byte_probe = []
for f in TRANSCRIPTS:
    if re.search(r"\b2111\b", L.read(f, None)):
        byte_probe.append(f)
print("      committed transcripts in mg-7522's tree            %2d"
      % len(TRANSCRIPTS))
print("      of those printing the figure `2111`                %2d"
      % len(byte_probe))
for f in byte_probe:
    print("          %s" % f)
print()
if not byte_probe:
    FINDINGS.append(
        "A4d `verified against the pre-repair output (0 / 0 / 0 / 0 / 2111 / "
        "0, unchanged)` is carried by the word `verified` alone -- no probe in "
        "mg-7522's tree computes a byte count.  A2d runs both arms and the "
        "claim HOLDS at 8 of 8; the finding is that mg-7522's own general form "
        "was not applied to it")
    print("  SO: the marker is doing the work of an instrument, in the tree")
    print("  whose thesis is that markers should not.  A2d ran both arms on")
    print("  the same inputs and the claim HOLDS -- which is the outcome that")
    print("  makes this reportable rather than damning.  `verified` was")
    print("  checkable, was not checked by its author, and turned out true.")

print()
L.bar("A4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a named marker missing from the rule")
print("that produces `0 USES`, a summary printing that 0 without the extent")
print("its own transcript states, an undispositioned strength-marked claim in")
print("mg-7522's own artifacts, and a disposition rule that matches nothing.")
print("It ranges over the %d artifacts of %s and over mg-7522's own two rules."
      % (len(ART), L.REPAIR))
print("It does NOT range over the transcripts, which are records of a run.")
print()
for f in FINDINGS:
    print("FINDING: %s" % f)
sys.exit(1 if BAD else 0)
