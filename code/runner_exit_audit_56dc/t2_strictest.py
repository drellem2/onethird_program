"""T2 -- THE STRICTEST RULE THIS REPAIR APPLIES, RUN AGAINST ITS OWN PROSE.

mg-dee4's F3 was that mg-7522 judged its subject by a nine-alternative rule and
itself by a three-alternative one, over a population that excluded every `.md`.
mg-70c7 repaired that.  So the question here is the same one, one level up.

  T2a  THE STRICTEST RULE.  `r6_self.py`'s E1 -- *every count over source
       carries a grain word* -- is the strictest thing this repair applies to
       anything: it is the rule that repairs its largest finding.  Its
       population is `M.outs(M.TREE)`, the `out_*.txt` of ONE DIRECTORY.  The
       README, `OUTCOMES.md`, `PREDICTIONS.md` and the published document are
       outside it.  The rule is reproduced here and pointed at them.
  T2b  EVERY MARKER NAMED IN PROSE, PUT TO THE RULE THAT PRODUCES THE NUMBER.
       `verified` was named in three places and was in no rule; that is F3's
       instance.  The merged `MARK` is checked here against every marker any
       artifact in this arc NAMES, not against the three its docstring names.
  T2c  THE MARKER RULE'S SELF-FACING POPULATION.  `r6_self.py` runs it over
       `MINE_PY + MINE_SH`.
  T2d  THE FLOOR ITEM, which nothing in the brief names: `lib70c7.figures()`
       and `lib7522.figures()` are two copies of one rule and they DISAGREE.

A self-check that stops at its own directory has a population defined by a
path, and that is the sentence this probe exists to test rather than repeat.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib56dc as M

sys.path.insert(0, os.path.join(M.REPO, M.S7522))
import lib7522 as L                                            # noqa: E402

sys.path.insert(0, os.path.join(M.REPO, M.SUBJECT))
import lib70c7 as N                                            # noqa: E402

BAD = 0
FINDINGS = []

M.bar("T2  THE STRICTEST RULE, RUN AGAINST THE REPAIR'S OWN ARTIFACTS")

# ---------------------------------------------------------------------------
M.hdr("T2a  E1, THE GRAIN RULE -- POINTED AT THE PROSE IT EXEMPTED")

# `r6_self.py`'s E1, transcribed from its source rather than imported, so this
# probe can disagree with it.  The three regexes and the two-line window are
# byte-for-byte what R6a runs; only the POPULATION is different, and that
# difference is the finding.
GRAINY = re.compile(r"\b(?:pipeline|line|execution|site|status|statuses|"
                    r"invocation)s?\b", re.I)
GRAIN_WORD = re.compile(r"\b(?:source lines?|executions?|sites?|lines?|"
                        r"pipelines?|files?|status|statuses|invocations?|"
                        r"steps?|argv|rows?|assertions?)\b", re.I)
COUNTED = re.compile(r"\b\d+\b")
CITATION = re.compile(r"[\w./-]+\.(?:py|sh|md|txt):\d+")

MY_OUTS = M.outs(M.SUBJECT)
PROSE = ["%s/README.md" % M.SUBJECT, "%s/OUTCOMES.md" % M.SUBJECT,
         "%s/PREDICTIONS.md" % M.SUBJECT, M.SUBJECT_DOC]

src_e1 = M.read("%s/r6_self.py" % M.SUBJECT, None)
pop_line = [l.strip() for l in src_e1.splitlines()
            if re.match(r"\s*for out in MY_OUTS", l)]
print("  THE RULE, and the one line that defines what it ranges over:")
print()
print("      MY_OUTS = M.outs(M.TREE)          <- `out_*.txt` of one directory")
print("      %s" % (pop_line[0] if pop_line else "(population line not found)"))
print()
print("  `R2c` in the same tree names four artifacts as *my reader-facing")
print("  artifacts* and censuses them for FIGURES in `R6b`.  E1 -- the rule")
print("  that repairs F1, the largest finding -- never reaches them.  Its")
print("  population is a glob over a path, which is the shape of F5.")
print()


def e1(paths, label):
    checked = quoted = 0
    missing = []
    for p in paths:
        lines = M.read(p, None).splitlines()
        for i, line in enumerate(lines, 1):
            if not (GRAINY.search(line) and COUNTED.search(line)):
                continue
            if CITATION.search(line):
                quoted += 1
                continue
            checked += 1
            window = " ".join(lines[max(0, i - 2):i + 1])
            if not GRAIN_WORD.search(window):
                missing.append((p, i, line.strip()))
    print("      %-44s %3d lines checked, %d quoted, %d with NO grain word"
          % (label, checked, quoted, len(missing)))
    return checked, quoted, missing


in_checked, _q1, in_missing = e1(MY_OUTS, "the population E1 HAS (7 transcripts)")
out_checked, _q2, out_missing = e1(PROSE, "the four artifacts E1 has NOT")
print()
print("  THE LINES E1 WOULD HAVE FLAGGED IF ITS POPULATION HAD REACHED THEM.")
print("  Every one is printed with its file and line, not summarised:")
print()
for p, i, line in out_missing:
    print("      *** %s:%d" % (os.path.basename(p), i))
    print("          %s" % line[:70])
if not out_missing:
    print("      (none -- the prose passes the rule it was not run under)")
print()
print("      count lines inside E1's population       %3d, %d flagged"
      % (in_checked, len(in_missing)))
print("      count lines outside it                   %3d, %d flagged"
      % (out_checked, len(out_missing)))
print()
FINDINGS.append(M.finding(
    "T2a",
    "the strictest rule mg-70c7 applies to anything -- `r6_self.py`'s E1, "
    "*every count over source carries a grain word* -- has a population of "
    "`M.outs(M.TREE)`: the `out_*.txt` of one directory.  The README, "
    "OUTCOMES.md, PREDICTIONS.md and the published document, which the same "
    "tree's R2c names as *my reader-facing artifacts* and censuses for "
    "FIGURES in R6b, are outside it.  Run unchanged over those four here, the "
    "rule examines %d count lines it never saw and flags %d.  A self-check "
    "whose population is a glob over a path is the shape of F5, in the "
    "section that repairs F1"
    % (out_checked, len(out_missing))))
if len(out_missing) == 0:
    print("  NOTE, kept rather than softened: the rule flags nothing in that")
    print("  prose.  The finding is the POPULATION and not a body count -- a")
    print("  rule that is not run cannot be said to have passed, which is")
    print("  mg-dee4's own argument about `0 USES` over `*.py` + `*.sh`.")

# ---------------------------------------------------------------------------
M.hdr("T2b  EVERY MARKER NAMED IN PROSE, PUT TO THE RULE THAT COUNTS")

print("  mg-dee4's F3 instance: `verified` was NAMED as a marker in three")
print("  places and was in no rule.  `R3a` repaired that by putting THE THREE")
print("  MARKERS THE D4 DOCSTRING NAMES to the merged rule.  Three is not the")
print("  population.  The population is every marker any artifact in this arc")
print("  names AS a marker, collected here from the sources:")
print()
def top_level_alts(pattern):
    """The `|` alternatives of a regex source AT DEPTH 0, as written.

    Splitting on every `|` would cut `\\ball (?:\\d+|of)\\b` in half and report
    `of` as a marker this arc names, which it is not.  Counting at depth 0 is
    the same rule `alternatives()` uses to say `nine against three`, and using
    a different one here would be this audit's own F3.
    """
    src = pattern.pattern if hasattr(pattern, "pattern") else pattern
    out, depth, cur, i = [], 0, "", 0
    while i < len(src):
        c = src[i]
        if c == "\\":
            cur += src[i:i + 2]
            i += 2
            continue
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == "|" and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return [a for a in out if a]


NAMED = set()
NAMED_AT = {}
# A marker is NAMED when it is written inside a delimited span on a line that
# is talking about markers -- the `_MENTION_SIGNALS` / marker-vocabulary lines
# and the alternatives of any rule kept in the arc's sources.  Collected by
# reading the RULES, because a rule's alternatives are the arc's own statement
# of what counts as a marker; a hand-list here would be the defect.
DEE4_RULE = re.compile(r"confirmed exactly|byte-identical|byte for byte"
                       r"|\bverified\b|\(measured\)|\bidentical\b|\bconfirmed\b"
                       r"|\ball (?:\d+|of)\b|\bexactly \d+\b|\bproven\b", re.I)


def sample(alt):
    """A string the alternative `alt` should match, DERIVED from `alt` itself.

    Derived and not hand-listed: a hand-list of sample strings would be a
    second statement of the rule, and two statements of one rule drifting
    apart is the finding this section is about.
    """
    s = alt.replace(r"\b", "")
    s = re.sub(r"\(\?:([^)]*)\)", lambda m: m.group(1).split("|")[0], s)
    s = s.replace(r"\d+", "8")
    s = re.sub(r"\\(.)", r"\1", s)
    return s.strip()


for rel, obj in (("lib7522.MARK", L.MARK),
                 ("lib7522.MARK_OLD", L.MARK_OLD),
                 ("mg-dee4's own D4 union", DEE4_RULE)):
    for alt in top_level_alts(obj):
        NAMED.add(alt)
        NAMED_AT.setdefault(alt, []).append(rel)

print("      %-22s %-11s %-11s %-11s %s"
      % ("marker", "MARK (9)", "MARK_OLD(3)", "mg-dee4(10)",
         "in the merged rule?"))
missing_marker = []
for w in sorted(NAMED, key=sample):
    t = sample(w)
    a = bool(L.MARK.search(t))
    b = bool(L.MARK_OLD.search(t))
    c = bool(DEE4_RULE.search(t))
    print("      %-22s %-11s %-11s %-11s %s"
          % ("`%s`" % t, "yes" if a else "no", "yes" if b else "no",
             "yes" if c else "no", "yes" if a else "*** NO ***"))
    if not a and (b or c):
        missing_marker.append(t)
print()
print("      alternatives in the merged `MARK`                 %2d"
      % N.alternatives(L.MARK))
print("      alternatives in the old self-facing `MARK_OLD`    %2d"
      % N.alternatives(L.MARK_OLD))
print("      alternatives in mg-dee4's own D4 union            %2d"
      % N.alternatives(DEE4_RULE))
print("      markers in an arc rule and NOT in the merged one  %2d   %s"
      % (len(missing_marker), ", ".join("`%s`" % w for w in missing_marker)))
print()
if missing_marker:
    dee4_out = M.read("%s/out_a4_superlatives.txt" % M.DEE4, None)
    cite = [l.strip() for l in dee4_out.splitlines()
            if "in SELF and not in SUBJECT" in l]
    print("  AND mg-dee4's OWN TRANSCRIPT NAMES IT, which is what makes this a")
    print("  regression rather than a preference:")
    print("      %s" % (cite[0] if cite else "(row not found)"))
    print()
    FINDINGS.append(M.finding(
        "T2b",
        "the *one rule object* mg-70c7 merged is the SUBJECT's nine "
        "alternatives verbatim, not the union: %s was an alternative of the "
        "old self-facing `MARK_OLD` and of mg-dee4's own D4 union, and is not "
        "in the merged `MARK`.  mg-dee4's transcript names it in a row of its "
        "own -- `in SELF and not in SUBJECT 1 proven`.  `R3a` cannot see this "
        "because it puts only the THREE markers the D4 docstring names to the "
        "rule, and three is not the population of markers this arc names"
        % ", ".join("`%s`" % w for w in missing_marker)))
    print("      *** a marker the arc's own rules name is not in the rule ***")
    print("      *** that produces the number                             ***")

# ---------------------------------------------------------------------------
M.hdr("T2c  THE MARKER RULE'S SELF-FACING POPULATION -- `.md` again")

here = os.path.join(M.REPO, M.SUBJECT)
MINE_PY = sorted(f for f in os.listdir(here) if f.endswith(".py"))
MINE_SH = sorted(f for f in os.listdir(here) if f.endswith(".sh"))
MINE_MD = sorted(f for f in os.listdir(here) if f.endswith(".md"))
print("  `r6_self.py` builds `mine_src` from `MINE_PY + MINE_SH` and runs the")
print("  marker rule over it.  `R3b` in the same tree faults mg-7522 for")
print("  exactly that population, in these words:")
print()
print("      \"A self-check whose population stops at two suffixes has a")
print("       population defined by a name, which is the finding one")
print("       directory over.\"")
print()
print("      mg-70c7's self-facing marker population   %2d file(s)  (%d py, %d sh)"
      % (len(MINE_PY) + len(MINE_SH), len(MINE_PY), len(MINE_SH)))
print("      its own `*.md`, OUTSIDE it                %2d file(s)" % len(MINE_MD))
for f in MINE_MD:
    print("          %s/%s" % (M.SUBJECT, f))
print("      its published document, OUTSIDE it         1 file(s)")
print("          %s" % M.SUBJECT_DOC)
print()
CORPUS = N.transcript_numbers(MY_OUTS + M.outs(M.S7522))
# R6b's OWN exclusion, transcribed rather than invented: a figure quoted inside
# a correction of itself or inside a prediction being scored is a mention of
# that figure, not a claim under it.  Using a different rule here would make
# the comparison unfair in my favour, which is the defect this arc keeps
# finding one level down.
QUOTING = re.compile(r"used to|no longer|mg-dee4|mg-7522|mg-05eb|mg-c2b3|"
                     r"I predict|predicted|\bMISS\b|\bHIT\b|was a count|"
                     r"is not|did not|reproduces it|corrected|stood here",
                     re.I)
uses = backed = unbacked = nofig = mentions = quoted_fig = 0
rows_u = []
for rel in ["%s/%s" % (M.SUBJECT, f) for f in MINE_MD] + [M.SUBJECT_DOC]:
    lines = M.read(rel, None).splitlines()
    for i, line, kind in L.strength_lines("\n".join(lines)):
        if kind == "MENTION":
            mentions += 1
            continue
        uses += 1
        figs = []
        for n in lines[max(0, i - 2):i + 1]:
            figs.extend(N.figures(n))
        miss = [v for v in figs if v not in CORPUS]
        if not figs:
            nofig += 1
        elif not miss:
            backed += 1
        elif any(QUOTING.search(x) for x in lines[max(0, i - 2):i + 1]):
            quoted_fig += 1
        else:
            unbacked += 1
            rows_u.append((rel, i, line, miss))
print("  THE MERGED RULE, RUN OVER THE FOUR ARTIFACTS IT DOES NOT REACH,")
print("  scored under R6b's OWN quoting exclusion so the comparison is fair:")
print()
print("      MENTIONs                                  %3d" % mentions)
print("      USEs                                      %3d" % uses)
print("      ...BACKED by a transcript of this arc     %3d" % backed)
print("      ...with no figure in the window           %3d" % nofig)
print("      ...quoted inside a correction or a scored prediction %3d"
      % quoted_fig)
print("      ...UNBACKED                               %3d" % unbacked)
for rel, i, line, miss in rows_u:
    print("      *** %s:%d  %s" % (os.path.basename(rel), i, line[:50]))
    print("          unbacked: %s" % ", ".join(str(v) for v in miss))
print()
FINDINGS.append(M.finding(
    "T2c",
    "mg-70c7's own self-facing marker check (`r6_self.py` R6c) runs over "
    "`MINE_PY + MINE_SH` -- %d files -- and its own %d `*.md` plus the "
    "published document are outside it.  That is the population half of F3 "
    "reproduced in the section that repairs F3, and the same tree's R3b "
    "faults mg-7522 for it in those words.  Run over the four here, the "
    "merged rule finds %d USEs (%d BACKED, %d with no figure, %d quoted in a "
    "correction, %d UNBACKED) that its self-check never examined"
    % (len(MINE_PY) + len(MINE_SH), len(MINE_MD), uses, backed, nofig,
       quoted_fig, unbacked)))
if unbacked == 0:
    print("  NOTE, kept rather than softened: nothing UNBACKED escaped.  The")
    print("  finding is that %d USEs were outside the population, not that a" % uses)
    print("  figure got through -- R6b's FIGURE census does reach these files,")
    print("  and that is why the escape is a reach and not a hole.")

# ---------------------------------------------------------------------------
M.hdr("T2d  THE FLOOR ITEM -- two copies of one rule that disagree")

print("  NOTHING IN THE BRIEF NAMES THIS, and it is what I chose to audit on")
print("  my own account.  mg-70c7's answer to F3 is *one rule object*:")
print()
print("      \"Two rules cannot be kept in step by intention; they can be kept")
print("       in step by being one object.\"")
print()
print("  `MARK` is one object.  `figures()` is not: `lib7522.figures` and")
print("  `lib70c7.figures` are two copies of the same rule, with the same")
print("  docstring, the same exclusions -- and a different threshold.")
print()
n_src = M.read("%s/lib70c7.py" % M.SUBJECT, None)
l_src = M.read("%s/lib7522.py" % M.S7522, None)
print("      lib70c7.py   %s"
      % ([l.strip() for l in n_src.splitlines() if "_SMALL" in l
          and "=" in l and not l.strip().startswith("#")][0]))
print("      lib70c7.py   %s"
      % ([l.strip() for l in n_src.splitlines()
          if "v <= _SMALL" in l][0]))
print("      lib7522.py   %s"
      % ([l.strip() for l in l_src.splitlines() if "if v > 2" in l][0]))
print()
disagree = [v for v in range(0, 501)
            if bool(N.figures("x %d y" % v)) != bool(L.figures("x %d y" % v))]
print("      integers 0..500 where the two copies DISAGREE   %3d   %s"
      % (len(disagree), disagree))
print("      ...and where they agree                         %3d"
      % (501 - len(disagree)))
print()
print("  WHERE IT BITES, traced rather than asserted.  `r3_strength.py` R3c")
print("  computes an UNBACKED count with `lib70c7.figures` and then compares")
print("  it against the number `out_s5_self.txt` printed, which was computed")
print("  with `lib7522.figures`.  The two derivations are declared equal and")
print("  a disagreement raises BAD:")
print()
r3 = M.read("%s/r3_strength.py" % M.SUBJECT, None)
for l in r3.splitlines():
    if "the two derivations disagree" in l or "theirs != unbacked" in l:
        print("      %s" % l.strip()[:70])
print()
print("      a figure of exactly 3 in a marker's window is a FIGURE to")
print("      `lib7522` and NOT a figure to `lib70c7`, so the two sides of")
print("      that equality are not computing the same predicate.  Neither")
print("      docstring says which threshold it is at; both say `Excludes 0, 1")
print("      and 2`, and one of them excludes 3 as well.")
print()
say_2 = len(re.findall(r"Excludes `?0`?, `?1`? and `?2`?", n_src))
print("      lib70c7's docstring says it excludes 0, 1 and 2   %d time(s)"
      % say_2)
print("      ...and its code excludes 0, 1, 2 and             %s"
      % ("3" if 3 in disagree else "(no extra value)"))
if disagree:
    FINDINGS.append(M.finding(
        "T2d",
        "FLOOR ITEM, chosen by me and named in no list: `lib70c7.figures()` "
        "and `lib7522.figures()` are two copies of one rule that disagree on "
        "exactly the value(s) %s -- `v <= _SMALL` with `_SMALL = 3` against "
        "`v > 2` -- while both docstrings say they exclude *0, 1 and 2*.  "
        "mg-70c7's answer to F3 is that two rules cannot be kept in step by "
        "intention and must be ONE OBJECT; it made `MARK` one object and left "
        "`figures()` two, and `r3_strength.py` R3c raises BAD when its own "
        "`lib70c7`-computed UNBACKED count differs from the "
        "`lib7522`-computed one in `out_s5_self.txt`"
        % ", ".join(str(v) for v in disagree)))
    print()
    print("      *** two copies of one rule, disagreeing, in the repair of ***")
    print("      *** the finding that two rules cannot be kept in step     ***")

print()
M.bar("T2 TOTAL FINDINGS: %d   TOTAL BAD: %d" % (len(FINDINGS), BAD))
print()
for f in FINDINGS:
    print(f)
print()
print("EXTENT OF THOSE NUMBERS.  TOTAL FINDINGS counts a rule whose population")
print("cannot reach the artifacts its own tree calls reader-facing, a marker")
print("named by a rule in this arc and absent from the rule that produces the")
print("number, a self-facing population that stops at two suffixes, and two")
print("copies of one rule that disagree.  It ranges over mg-70c7's %d `*.py`,"
      % len(MINE_PY))
print("%d `*.sh`, %d `*.md`, its published document and its %d transcripts,"
      % (len(MINE_SH), len(MINE_MD), len(MY_OUTS)))
print("plus the two libraries and mg-dee4's committed A4 transcript.  It does")
print("NOT judge whether a grain WORD is the right one, and it does not")
print("re-measure mg-c2b3's 34.")
sys.exit(min(len(FINDINGS) + BAD, 120))
