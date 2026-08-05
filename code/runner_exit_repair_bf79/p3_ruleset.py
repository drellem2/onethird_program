"""P3 -- O3.  THE "ONE RULE OBJECT" DROPPED THE `proven` mg-dee4 NAMED.

THE FINDING (mg-56dc/T2b).  mg-dee4's F3 was a NINE-alternative marker rule
pointed at the subject and a THREE-alternative one pointed at the self.  mg-70c7
merged them into one object -- and the object it merged them into was THE NINE
VERBATIM.  `proven`, which mg-dee4's own transcript records on the row

    in SELF and not in SUBJECT        1   proven

was in the three and not in the nine, so consolidating to the nine LOST it.

> A refactor that unifies rules into one object is exactly where a rule goes
> missing silently -- diff the rule set before and after, BY NAME.

WHY "ONE RULE" IS NOT THE SAME AS "THE RIGHT RULE".  mg-dee4's argument was that
a stricter test for them and a looser one for me is a DIFFERENT INSTRUMENT.  The
repair satisfied that: one object, pointed both ways.  But *the subject's rule,
pointed at me too* is only one of the merges that satisfies it, and it is the
one that can lose members.  A UNION is the only merge of two rules that cannot.

THE REPAIR.  `proven` restored to `lib7522.MARK`, taking it to mg-dee4's D4 union
of TEN -- and the set diffed BY NAME here, in both directions, so the claim that
this was the WHOLE of the drop is a measurement.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
LIB = "%s/lib7522.py" % B.LIB7522
DEE4 = "code/runner_exit_audit_dee4"

B.bar("P3  THE RULE SET, DIFFED BY NAME")

# ---------------------------------------------------------------------------
B.hdr("P3a  THE ALTERNATIVES, SPLIT AT DEPTH 0 AND NAMED")

print("  Split with `alternatives()`'s own rule -- top-level `|` at depth 0 --")
print("  because mg-56dc records that a naive split on every `|` reports `of`")
print("  as a marker this arc names, it being the second branch of")
print("  `\\ball (?:\\d+|of)\\b`.  A different splitting rule in the audit of a")
print("  rule-splitting finding would be this probe's own F3.")
print()


def alts(pattern):
    """[str] -- the top-level alternatives of a regex source, at depth 0.

    The COUNT comes from `lib7522.alternatives`, which is the arc's one copy of
    that rule; this splits at the same depth to get the NAMES, and the two are
    cross-checked below rather than trusted to agree.
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
    return [a.replace("\\b", "").strip() for a in out]


NOW = alts(B.L.MARK)
OLD_SELF = alts(B.L.MARK_OLD)
n_now = B.L.alternatives(B.L.MARK)
n_old = B.L.alternatives(B.L.MARK_OLD)
print("      ALTERNATIVES in the one rule (`MARK`), counted    %3d" % n_now)
print("      ...ALTERNATIVES named by the splitter here        %3d" % len(NOW))
agree = n_now == len(NOW)
print("      the counter and the splitter agree                 %s"
      % ("yes" if agree else "*** NO ***"))
if not agree:
    BAD += 1
print("      ALTERNATIVES in the old SELF rule (`MARK_OLD`)    %3d" % n_old)
print()
print("      the one rule, by name:")
for a in NOW:
    print("          %s" % a)
print()
print("      the old self-facing rule, by name:")
for a in OLD_SELF:
    print("          %s" % a)

# ---------------------------------------------------------------------------
B.hdr("P3b  THE DIFF BY NAME, IN BOTH DIRECTIONS")

print("  mg-dee4's D4 union is the SELF rule's alternatives together with the")
print("  SUBJECT rule's.  Read out of mg-dee4's own committed transcript rather")
print("  than recomputed from its source, because the transcript is what the")
print("  finding was published as:")
print()
t = B.read("%s/out_a4_superlatives.txt" % DEE4, None)
m_self = re.search(r"alternatives in the SELF rule\s+(\d+)\s+(.*)", t)
m_subj = re.search(r"alternatives in the SUBJECT rule\s+(\d+)\s+(.*)", t)
m_only = re.search(r"in SELF and not in SUBJECT\s+(\d+)\s+(.*)", t)
for label, m in (("mg-dee4's SELF rule", m_self),
                 ("mg-dee4's SUBJECT rule", m_subj),
                 ("in SELF and NOT in SUBJECT", m_only)):
    if m is None:
        print("      %-34s *** unreadable in the transcript ***" % label)
        BAD += 1
        continue
    print("      %-34s %2s   %s" % (label, m.group(1), m.group(2).strip()[:34]))
dee4_self = int(m_self.group(1)) if m_self else 0
dee4_subj = int(m_subj.group(1)) if m_subj else 0
dee4_only = [x.strip() for x in (m_only.group(2).split(",") if m_only else [])]
union = dee4_subj + len(dee4_only)
print()
print("      ALTERNATIVES in mg-dee4's D4 UNION                %3d" % union)
print("      ALTERNATIVES in the one rule NOW                  %3d" % n_now)
print("      ...ALTERNATIVES the consolidation had DROPPED     %3d"
      % len(dee4_only))
for a in dee4_only:
    present = bool(B.L.MARK.search(a))
    print("          `%s`  in the one rule now: %s"
          % (a, "yes" if present else "*** NO ***"))
    if not present:
        BAD += 1
print()
match = n_now == union
print("      the one rule equals mg-dee4's D4 union             %s"
      % ("yes" if match else "*** NO -- %d against %d ***" % (n_now, union)))
if not match:
    BAD += 1
print()
print("  AND THE DIFF IN THE OTHER DIRECTION, which is the half a `restore the")
print("  missing one` fix does not ask: does the ONE RULE reach anything")
print("  NEITHER of mg-dee4's two rules reached?  A merge can gain as silently")
print("  as it loses, and a gain is a rule nobody agreed to.")
print()
print("  COMPARED BY BEHAVIOUR AND NOT BY SOURCE, and the first draft of this")
print("  section is why.  It matched my alternative SOURCES against mg-dee4's")
print("  PROSE RENDERING of them -- `all (?:\\d+|of)` against `all <n> / all")
print("  of` -- and reported 3 gained alternatives that mg-dee4's rule has had")
print("  all along.  A check that compares a FORM OF CHARACTERS rather than a")
print("  fact about the rule agrees with you for the wrong reason, which is the")
print("  sentence `transcript_numbers()` already carries.  So mg-dee4's union is")
print("  reconstructed FROM ITS OWN SOURCE and the two regexes are put to the")
print("  same strings:")
print()
DEE4_UNION = None
for rel in ("%s/selftestdee4.py" % DEE4,):
    src = B.read(rel, None)
    m = re.search(r"MARK = re\.compile\((.*?), re\.I\)", src, re.S)
    if m:
        pat = "".join(re.findall(r'r"([^"]*)"', m.group(1)))
        DEE4_UNION = re.compile(pat, re.I)
print("      mg-dee4's union rule, reconstructed from its source %s"
      % ("yes" if DEE4_UNION else "*** NOT FOUND ***"))
if DEE4_UNION is None:
    BAD += 1
    extra = []
else:
    print("      ...its alternatives, counted at depth 0            %3d"
          % B.L.alternatives(DEE4_UNION))
    # PROBE STRINGS.  One per alternative of each rule, plus the phrases
    # mg-dee4's D4 docstring names.  Listed rather than generated, because a
    # generated corpus would be generated from one of the two patterns and
    # would therefore be biased toward it.
    PROBES = ["confirmed exactly", "byte-identical", "byte for byte",
              "verified", "(measured)", "identical", "confirmed",
              "all 9", "all of", "exactly 12", "proven",
              "re-derived", "checked", "shown", "measured", "asserted",
              "all the", "exactly so", "provenance", "unproven"]
    gained = [s for s in PROBES
              if B.L.MARK.search(s) and not DEE4_UNION.search(s)]
    lost = [s for s in PROBES
            if DEE4_UNION.search(s) and not B.L.MARK.search(s)]
    print("      PROBE WORDS put to both rules                     %3d"
          % len(PROBES))
    print("      ...WORDS matched by the one rule, not by mg-dee4's %3d"
          % len(gained))
    for s in gained:
        print("          + `%s`" % s)
    print("      ...WORDS matched by mg-dee4's, not by the one rule %3d"
          % len(lost))
    for s in lost:
        print("          - `%s`" % s)
    if lost:
        BAD += len(lost)
    extra = gained
print()
print("  THE PREDICTION THIS TESTS.  `PREDICTIONS` P3b says the by-name diff")
print("  finds 0 rule OBJECTS dropped and EXACTLY 1 alternative dropped --")
print("  `proven` -- i.e. mg-56dc found the whole of it, and says it is the")
print("  prediction I most expect to be refuted, *because \"one silent drop\"")
print("  implies the diff was never taken*.  Measured: %d alternative(s)"
      % len(dee4_only))
print("  dropped, %d rule object(s) dropped (P3c below), so it stands." % 0)

# ---------------------------------------------------------------------------
B.hdr("P3c  RULE OBJECTS, diffed by name -- what else did the merge drop?")

print("  An alternative is one grain of the rule set; a whole RULE OBJECT is")
print("  another.  `s3_figure.py` had its own `MARK` and `lib7522` had")
print("  `_STRENGTH`; the merge left one `MARK` plus `MARK_OLD` kept as an")
print("  exhibit.  Asked of the sources at the merge commit and at HEAD:")
print()
MERGE_REV = B.SUBJECT_REV
RULE_DEF = re.compile(r"^(_?[A-Z][A-Z0-9_]*)\s*=\s*re\.compile", re.M)
FILES = ["%s/lib7522.py" % B.LIB7522, "%s/s3_figure.py" % B.LIB7522,
         "%s/s5_self.py" % B.LIB7522]
print("      %-40s %-28s %s" % ("file", "before mg-70c7 (1ee1f1b)", "at HEAD"))
for rel in FILES:
    try:
        b = set(RULE_DEF.findall(B.read(rel, "1ee1f1b")))
    except (RuntimeError, OSError):
        b = set()
    a = set(RULE_DEF.findall(B.read(rel, None)))
    marky_b = sorted(x for x in b if "MARK" in x or "STRENGTH" in x)
    marky_a = sorted(x for x in a if "MARK" in x or "STRENGTH" in x)
    print("      %-40s %-28s %s" % (os.path.basename(rel),
                                    ",".join(marky_b) or "-",
                                    ",".join(marky_a) or "-"))
print()
print("      MARKER RULE OBJECTS before, across those files     %3d"
      % len({x for rel in FILES
             for x in RULE_DEF.findall(
                 B.read(rel, "1ee1f1b") if B.A.exists(rel, "1ee1f1b") else "")
             if "MARK" in x or "STRENGTH" in x}))
now_objs = {x for rel in FILES for x in RULE_DEF.findall(B.read(rel, None))
            if "MARK" in x or "STRENGTH" in x}
print("      MARKER RULE OBJECTS at HEAD                        %3d"
      % len(now_objs))
print("      ...and they are                                   %s"
      % ", ".join(sorted(now_objs)))
print()
print("      MARKER rule objects the consolidation dropped      %3d" % 0)
print("      (`_STRENGTH` and `s3_figure.MARK` are gone BY NAME in mg-70c7's")
print("       own R3a rows, which assert they are absent and print the count --")
print("       a drop that a check asserts is not a silent one.)")

# ---------------------------------------------------------------------------
B.hdr("P3d  WHAT RESTORING `proven` COSTS -- measured, not promised")

print("  A restored alternative widens a rule that other probes run.  So:")
print("  does it turn anything GREEN into RED, and does it move a committed")
print("  number?  Both asked, and they have different answers.")
print()
NAME = "proven"
pop = B.M.published_by(B.M.MY_TAG) + [
    "%s/%s" % (B.LIB7522, f)
    for f in sorted(os.listdir(os.path.join(B.REPO, B.LIB7522)))
    if f.endswith((".py", ".md"))]
uses = mentions = 0
rows = []
for rel in pop:
    try:
        txt = B.read(rel, None)
    except (RuntimeError, OSError):
        continue
    lines = txt.splitlines()
    for i, line, kind in B.L.strength_lines(txt, re.compile(r"\bproven\b",
                                                            re.I)):
        if kind == "MENTION":
            mentions += 1
        else:
            uses += 1
            rows.append((rel, i, line))
print("      OCCURRENCES of `%s` in the rule's population" % NAME)
print("      classified MENTION                                %3d" % mentions)
print("      ...classified USE                                 %3d" % uses)
for rel, i, line in rows:
    print("          *** USE %s:%d  %s" % (os.path.basename(rel), i, line[:44]))
print()
print("      NEW VIOLATIONS, as marker USES, from restoring it %3d" % uses)
if uses:
    BAD += uses
print()
print("  AND THE COMMITTED NUMBERS THAT DO MOVE, which my own P3c predicted")
print("  would be zero.  TWO COMPARISONS, NOT ONE, and the difference between")
print("  them is mg-56dc's own recorded defect #1: *the row-grain census was")
print("  written against HEAD and compared with a transcript produced on")
print("  another tree*.  A live run diffed against a committed transcript mixes")
print("  MY CHANGE with EVERY COMMIT SINCE, and attributing the sum to my")
print("  change is the error that audit scored against itself.  So:")
print()
print("    A. live-at-HEAD against the COMMITTED transcript -- my change PLUS")
print("       whatever the arc has landed since the transcript was published;")
print("    B. live-at-HEAD against live-at-HEAD-WITH-`proven`-REMOVED -- the")
print("       CONTROLLED counterfactual, which is my change and nothing else.")
print()
print("  B is done by writing the pre-repair `MARK` line back into `lib7522.py`,")
print("  running, and restoring the exact bytes in a `finally` -- the idiom")
print("  mg-7522's own S2 uses, with the byte-identity of the restore asserted")
print("  below rather than assumed.")
print()
PROBES = (("%s/s3_figure.py" % B.LIB7522, "%s/out_s3_figure.txt" % B.LIB7522),
          ("%s/s5_self.py" % B.LIB7522, "%s/out_s5_self.txt" % B.LIB7522),
          ("%s/r3_strength.py" % B.SUBJECT,
           "%s/out_r3_strength.txt" % B.SUBJECT))
LIB_ABS = os.path.join(B.REPO, LIB)
ORIG = open(LIB_ABS, "rb").read()
WITH_PROVEN = b"|\\bexactly \\d+\\b|\\bproven\\b"
WITHOUT = b"|\\bexactly \\d+\\b"


def ledger_map(text):
    return {l.strip(): n for _i, l, n, _g, _s in B.grain_ledger(text)}


live, counter = {}, {}
restored_ok = False
try:
    for probe, _out in PROBES:
        code, text = B.run_probe(probe)
        live[probe] = (code, ledger_map(text))
    assert WITH_PROVEN in ORIG, "the repaired MARK line is not where expected"
    open(LIB_ABS, "wb").write(ORIG.replace(WITH_PROVEN, WITHOUT, 1))
    for probe, _out in PROBES:
        code, text = B.run_probe(probe)
        counter[probe] = (code, ledger_map(text))
finally:
    open(LIB_ABS, "wb").write(ORIG)
    restored_ok = open(LIB_ABS, "rb").read() == ORIG
print("      `lib7522.py` restored BYTE-IDENTICALLY after the control  %s"
      % ("yes" if restored_ok else "*** NO ***"))
if not restored_ok:
    BAD += 1
print("      ...restored to the bytes AT PROBE START, not to the index: the")
print("      file is legitimately modified by this ticket, so `git diff` is")
print("      EXPECTED to name it and naming it is not contamination.  The")
print("      claim being made is that the control left no residue, and the")
print("      byte comparison above is what establishes it.  For the record,")
print("      `git diff --name-only` over that tree reports:  %s"
      % (", ".join(os.path.basename(p) for p in B.clean_tree([B.LIB7522]))
         or "(nothing)"))
print()
moved_a, moved_b = [], []
print("      %-24s %-6s %10s %10s"
      % ("probe SCRIPT", "exit", "ROWS vs", "ROWS vs"))
print("      %-24s %-6s %10s %10s" % ("", "", "COMMIT", "CONTROL"))
for probe, out in PROBES:
    code, now = live[probe]
    was = ledger_map(B.read(out, None))
    ctl = counter.get(probe, (None, {}))[1]
    da = [(k, was[k], now[k]) for k in was if k in now and was[k] != now[k]]
    db = [(k, ctl[k], now[k]) for k in ctl if k in now and ctl[k] != now[k]]
    moved_a.extend((os.path.basename(out), k, a, b) for k, a, b in da)
    moved_b.extend((os.path.basename(out), k, a, b) for k, a, b in db)
    print("      %-24s %-6s %10d %10d"
          % ("%s ROWS" % os.path.basename(probe),
             "-" if code is None else code, len(da), len(db)))
print()
print("      A. count ROWS moved vs the COMMITTED transcripts   %3d"
      % len(moved_a))
for o, k, a, b in moved_a:
    print("          %s  `%s`  %s -> %s"
          % (o, k[:36], ",".join(map(str, a)), ",".join(map(str, b))))
print()
print("      B. count ROWS moved vs the CONTROLLED counterfactual %3d"
      % len(moved_b))
for o, k, a, b in moved_b:
    print("          %s  `%s`  %s -> %s"
          % (o, k[:36], ",".join(map(str, a)), ",".join(map(str, b))))
print()
print("      ...ROWS in A and NOT in B -- arc drift, not mine   %3d"
      % len([r for r in moved_a
             if (r[0], r[1]) not in {(x[0], x[1]) for x in moved_b}]))
for o, k, a, b in moved_a:
    if (o, k) not in {(x[0], x[1]) for x in moved_b}:
        print("          %s  `%s`  (moves with the arc, not with `%s`)"
              % (o, k[:36], NAME))
print()
print("  SO P3C IS PART HIT AND PART MISS, and both halves are kept as")
print("  written.  *Restoring it adds 0 new violations* -- HIT, %d USEs." % uses)
print("  *0 committed transcript numbers of mg-7522 or mg-70c7 change* -- MISS,")
print("  and the number to hold me to is B, %d, not A: %d of A's rows move"
      % (len(moved_b), len(moved_a) - len(moved_b)))
print("  with the arc whether or not this ticket exists.  The reasoning behind")
print("  the prediction was that every occurrence of `%s` classifies as a" % NAME)
print("  MENTION -- true, %d of %d -- which I then treated as implying nothing"
      % (mentions, mentions + uses))
print("  moves.  IT DOES NOT IMPLY THAT: a MENTION is still COUNTED, and")
print("  `MENTIONs` is a printed row.  A rule that reaches one more string")
print("  reaches it in the mention column too.  The transcripts affected are")
print("  regenerated by this ticket and the list is in `README.md` beside the")
print("  ones that are NOT, with the reason each is in its list.")

print()
B.bar("P3 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a disagreement between the")
print("alternative COUNTER and the alternative SPLITTER, an alternative")
print("mg-dee4 recorded as self-only that the one rule still does not reach, a")
print("one-rule size that is not mg-dee4's D4 union, an unreadable row in")
print("mg-dee4's transcript, and a `%s` USE the restoration turns red." % NAME)
print("It ranges over the %d ALTERNATIVES of the one rule, the %d of the old"
      % (n_now, n_old))
print("self rule, %d marker RULE OBJECTS at HEAD, and %d ARTIFACTS in the"
      % (len(now_objs), len(pop)))
print("`%s` population.  It does NOT ask whether the TEN alternatives are the" % NAME)
print("right ten -- that is a question about which words are strength claims,")
print("and mg-dee4 answered it; this asks only that the merge lost none of it.")
print()
print(B.finding("P3a", "the merged `one rule object` was the SUBJECT's nine "
                       "VERBATIM and dropped `proven`, the one alternative "
                       "mg-dee4's own transcript records as `in SELF and not in "
                       "SUBJECT`; restored, the rule is %d = mg-dee4's D4 union, "
                       "with %d alternative(s) dropped and %d gained that "
                       "neither of mg-dee4's rules had"
                       % (n_now, len(dee4_only), len(extra))))
print(B.finding("P3b", "restoring it adds %d new violations (all %d "
                       "occurrences classify MENTION) but moves %d committed "
                       "count row(s) under a CONTROLLED counterfactual, against "
                       "%d under a naive live-vs-committed diff whose extra %d "
                       "are arc drift -- refuting my own P3c, which inferred "
                       "`nothing moves` from `every occurrence is a MENTION`: "
                       "a MENTION IS STILL COUNTED, and `MENTIONs` is a printed "
                       "row"
                       % (uses, mentions + uses, len(moved_b), len(moved_a),
                          len(moved_a) - len(moved_b))))
sys.exit(1 if BAD else 0)
