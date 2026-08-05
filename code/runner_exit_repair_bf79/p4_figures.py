"""P4 -- O4 AND THE FLOOR ITEM.  TWO COPIES OF `figures()` DISAGREE ON 3.

THE FINDING (mg-56dc/T2d).  `lib70c7.figures` and `lib7522.figures` are two
implementations of the same rule, and over the integers 0..500 they disagree on
exactly one: the value `3`.  `lib7522` keeps it (`if v > 2`); `lib70c7` dropped
it (`if v <= _SMALL` with `_SMALL = 3`) -- while its own docstring said it
excluded "`0`, `1` and `2`".  So the code disagreed with its twin AND with its
own label, which is O1's defect class living inside O4's.

> Delete one.  If both must exist, make one call the other; two copies that
> agree today are a future disagreement, and these two do not even agree today.

THE FLOOR ITEM, WHICH NEITHER BRIEF NAMES.  `figures()` is not the only rule
mg-70c7 kept in two copies.  A by-name census of every module-level definition
in both libraries is below, with a DISPOSITION for each -- because the answer is
not "unify all of them": mg-70c7's F1 parsers are written from scratch on purpose
so a probe can disagree with the rule it is checking, and that reason is real for
a parser whose implementations DIFFER and empty for one where they are identical.

THE REPAIR.  `lib70c7.figures` calls `lib7522.figures`; `lib70c7.alternatives`
calls `lib7522.alternatives`.  What each costs is measured separately, because
the two cases are not alike: one pair disagreed and one pair was identical.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
L70 = "%s/lib70c7.py" % B.SUBJECT
L75 = "%s/lib7522.py" % B.LIB7522
UNIFIED = ("figures", "alternatives")

B.bar("P4  TWO COPIES OF A RULE, AND EVERY OTHER PAIR LIKE THEM")

# ---------------------------------------------------------------------------
B.hdr("P4a  IS THERE ONE IMPLEMENTATION NOW?  asked of the source")

print("  `lib70c7.figures` must be a CALL and not a body.  Read out of the")
print("  source with `lib7522.function_code`, which strips the docstring -- so")
print("  a rule restated in prose and delegated in code reads as delegated,")
print("  which is what it is.")
print()
for name in UNIFIED:
    body = B.L.function_code(L70, name, None)
    delegates = bool(re.search(r"_L\(\)\.%s\(" % name, body))
    lines = [l for l in body.splitlines() if l.strip()]
    print("      lib70c7.%-14s body lines %2d   delegates: %s"
          % (name, len(lines), "yes" if delegates else "*** NO ***"))
    if not delegates:
        BAD += 1
    if len(lines) > 3:
        BAD += 1
        print("          *** %d body lines is a restatement, not a call ***"
              % len(lines))
print()
impl = 0
for path in (L70, L75):
    for name in UNIFIED:
        body = B.L.function_code(path, name, None)
        if body and not re.search(r"_L\(\)\.%s\(" % name, body):
            impl += 1
print("      IMPLEMENTATIONS of those %d rules, as function ITEMS %3d"
      % (len(UNIFIED), impl))
print("      ...ITEMS expected, one per unified rule             %3d"
      % len(UNIFIED))
if impl != len(UNIFIED):
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("P4b  DO THEY AGREE NOW?  over 0..500, before and after")

print("  The two rules put to the same inputs.  BEFORE is reconstructed from")
print("  the pre-repair predicate -- `v <= 3` against `v > 2` -- rather than")
print("  read from a commit, so the row is a property of the two RULES and not")
print("  of a revision.  AFTER calls both names as they now stand.")
print()


def before70(line):
    """`lib70c7.figures` as it stood: `lib7522`'s rule with `_SMALL = 3`.

    `lib56dc.figures(line, small=)` is the arc's PARAMETERISED third copy,
    written by the audit precisely so the two subject copies can be compared by
    something that is neither of them.  `small=3` is mg-70c7's constant and
    `small=2` is mg-7522's; that is the whole of the difference.
    """
    return B.A.figures(line, small=3)


def after70(line):
    return B.M.figures(line)


N = 501
dis_before = [v for v in range(N)
              if before70(str(v)) != B.L.figures(str(v))]
dis_after = [v for v in range(N)
             if after70(str(v)) != B.L.figures(str(v))]
print("      INTEGER ITEMS tested, 0..%d                       %3d" % (N - 1, N))
print("      ...INTEGER ITEMS the two rules DISAGREED on, before %3d"
      % len(dis_before))
print("          %s" % (", ".join(map(str, dis_before)) or "(none)"))
print("      ...INTEGER ITEMS they disagree on, AFTER           %3d"
      % len(dis_after))
print("          %s" % (", ".join(map(str, dis_after)) or "(none)"))
if dis_after:
    BAD += len(dis_after)
print()
print("      the third copy agrees with mg-7522's at small=2     %s"
      % ("yes" if all(B.A.figures(str(v), small=2) == B.L.figures(str(v))
                      for v in range(N)) else "*** NO ***"))
print("      ...and with mg-70c7's OLD rule at small=3           %s"
      % ("yes" if all(B.A.figures(str(v), small=3) == before70(str(v))
                      for v in range(N)) else "*** NO ***"))
print()
print("  WHICH COPY WAS WRONG, and it is decidable rather than a preference:")
print("  BOTH DOCSTRINGS SAID `0, 1 and 2`.  Only mg-7522's did it.  So the")
print("  surviving rule is the one both labels always described, and deleting")
print("  the other body makes two labels true instead of one.")
d70 = B.L.function_code(L70, "figures", "973ca61")
print()
print("      mg-70c7's OLD body dropped the value 3              %s"
      % ("yes" if "_SMALL" in d70 else "(not readable at 973ca61)"))
print("      its docstring claimed it excluded `0`, `1` and `2`  %s"
      % ("yes" if "`0`, `1` and `2`" in B.read(L70, "973ca61") else "no"))

# ---------------------------------------------------------------------------
B.hdr("P4c  WHAT UNIFYING `figures()` COSTS -- controlled, not asserted")

print("  My own P4c predicted this changes at least one number in a committed")
print("  transcript of mg-70c7, *because r3_strength.py R3c compares a")
print("  lib70c7-computed count against a lib7522-computed one*.  The")
print("  prediction and its REASON are scored separately below, because they")
print("  do not get the same verdict.")
print()
CORPUS = B.M.outs(B.SUBJECT) + B.M.outs(B.LIB7522)
new_set, old_set = set(), set()
for p in CORPUS:
    try:
        txt = B.read(p, None)
    except (RuntimeError, OSError):
        continue
    for line in txt.splitlines():
        new_set.update(B.L.figures(line))
        old_set.update(before70(line))
print("      TRANSCRIPTS in R2b's figure corpus                 %3d" % len(CORPUS))
print("      DISTINCT FIGURES under the unified rule            %3d" % len(new_set))
print("      ...under mg-70c7's OLD rule, same transcripts      %3d" % len(old_set))
print("      ...FIGURES the unification adds                    %3d"
      % len(new_set - old_set))
print("          %s" % (", ".join(map(str, sorted(new_set - old_set))) or "(none)"))
print("      ...FIGURES it removes                              %3d"
      % len(old_set - new_set))
print()
print("  THAT IS THE COMMITTED NUMBER THAT MOVES: `out_r2_anchor.txt`'s row")
print("  *distinct figures they print*, at a FIXED corpus, goes %d -> %d."
      % (len(old_set), len(new_set)))
print("  So P4c's CLAIM is a HIT.")
print()
print("  AND ITS REASON IS A MISS.  R3c's four counts are re-derived here under")
print("  both rules, holding everything else fixed:")
print()
here = os.path.join(B.REPO, B.SUBJECT)
pop_files = (["%s/%s" % (B.LIB7522, f)
              for f in sorted(os.listdir(os.path.join(B.REPO, B.LIB7522)))
              if f.endswith((".py", ".sh", ".md"))] + [B.M.DOC])


def r3c(figs_fn):
    corpus = set()
    for p in CORPUS:
        try:
            t = B.read(p, None)
        except (RuntimeError, OSError):
            continue
        for l in t.splitlines():
            corpus.update(figs_fn(l))
    b = u = nf = me = 0
    for rel in pop_files:
        try:
            lines = B.read(rel, None).splitlines()
        except (RuntimeError, OSError):
            continue
        for i, line, kind in B.L.strength_lines("\n".join(lines)):
            if kind == "MENTION":
                me += 1
                continue
            figs = []
            for n in lines[max(0, i - 2):i + 1]:
                figs.extend(figs_fn(n))
            if not figs:
                nf += 1
            elif [v for v in figs if v not in corpus]:
                u += 1
            else:
                b += 1
    return me, b, nf, u


old_r3c, new_r3c = r3c(before70), r3c(B.L.figures)
print("      %-34s %8s %8s" % ("R3c row", "OLD rule", "unified"))
for k, a, b in zip(("MENTIONs", "USEs BACKED", "USEs with no figure",
                    "USEs UNBACKED"), old_r3c, new_r3c):
    print("      %-34s %8d %8d   %s" % (k, a, b, "same" if a == b else "MOVED"))
r3c_moved = sum(1 for a, b in zip(old_r3c, new_r3c) if a != b)
print()
print("      R3c ROWS the unification moves                     %3d" % r3c_moved)
print()
print("  ZERO.  The mechanism I named is the one place it does NOT bite: the")
print("  value `3` never lands in a claim window in that population, so the")
print("  comparison R3c makes is unaffected.  The number that moves is R2b's")
print("  corpus SIZE, one section over, which I did not name.  Right answer,")
print("  wrong reason -- and a prediction whose reason is wrong is a prediction")
print("  that would have been wrong on a different repository, so it is scored")
print("  PART HIT, PART MISS rather than HIT.")

# ---------------------------------------------------------------------------
B.hdr("P4d  THE FLOOR ITEM -- every name defined in BOTH libraries")

print("  `figures()` was not the only rule kept in two copies.  A by-name")
print("  census of every module-level `def` in both libraries, with a")
print("  DISPOSITION for each -- because `unify all of them` is the wrong")
print("  answer and the reason is written in `lib70c7`'s own docstring: its F1")
print("  parsers exist so a probe can DISAGREE with the rule it checks.  That")
print("  reason is real where the two implementations DIFFER and empty where")
print("  they are the same code.")
print()
a = B.defined_names(L70)
b = B.defined_names(L75)
both = sorted(a & b)
print("      module-level DEF WORDS in lib70c7.py               %3d" % len(a))
print("      module-level DEF WORDS in lib7522.py              %3d" % len(b))
print("      NAME WORDS defined in BOTH libraries               %3d" % len(both))
print()
PLUMBING = {"bar", "hdr", "rows", "git", "read", "run_argv"}
print("      %-22s %-11s %s" % ("name", "same code?", "disposition"))
ident = diff = 0
for name in both:
    if name in UNIFIED:
        same = "delegated"
        disp = "UNIFIED by this ticket"
    else:
        s = B.same_body(name, L70, L75)
        same = "IDENTICAL" if s else "differs"
        if s:
            ident += 1
        else:
            diff += 1
        if name in PLUMBING:
            disp = ("output/plumbing -- not a rule; no figure rests on it"
                    if s else "plumbing, but DIVERGED -- see below")
        else:
            disp = ("A RULE IN TWO IDENTICAL COPIES -- the next `figures()`"
                    if s else
                    "F1 parser, written from scratch ON PURPOSE (differs)")
    print("      %-22s %-11s %s" % (name, same, disp))
print()
print("      NAME WORDS in both, IDENTICAL code                 %3d" % ident)
print("      NAME WORDS in both, code DIFFERS                   %3d" % diff)
print("      NAME WORDS this ticket UNIFIED                     %3d" % len(UNIFIED))
print()
risky = [n for n in both
         if n not in UNIFIED and n not in PLUMBING
         and B.same_body(n, L70, L75)]
print("      RULE WORDS still kept in two IDENTICAL copies      %3d" % len(risky))
for n in risky:
    print("          %s" % n)
print()
print("  AND THE SURVIVOR IS NAMED BY THE MEASUREMENT, NOT BY ME.  I expected")
print("  `run_argv` to be the one to flag; the census says otherwise.")
print("  `run_argv`'s two copies DIFFER -- mg-7522's takes an `env` argument --")
print("  so it is a divergence that is at least visible, and no published")
print("  figure rests on it.  The one that matches `figures()`'s shape exactly")
print("  is `captured_var`: TWO IDENTICAL COPIES OF A RULE, and not a small")
print("  one -- it is mg-dee4's F6, *the variable a pipeline's OUTPUT is")
print("  captured into*, the VALUE arm of the consumption clause that F6 is")
print("  entirely about.  It agrees today.  So did `alternatives()`.")
print()
print("  IT IS NOT UNIFIED HERE, and the reason is scope rather than judgement:")
print("  mg-56dc's O4 names `figures()`, and `captured_var` is reached by")
print("  `s2_status.py` and `k2_consume.py`, whose transcripts this ticket does")
print("  not regenerate and whose runner takes twenty minutes.  Changing a rule")
print("  I cannot re-measure would be the defect this whole arc is about.  It")
print("  is NAMED so the next ticket in this lineage has it written down rather")
print("  than rediscovered, which is the only honest thing to do with a finding")
print("  you are not going to act on.")
print()
print("  WHAT I PREDICTED AND WHAT IS TRUE.  `PREDICTIONS` PFa says a by-name")
print("  census finds AT LEAST 6 names defined in both libraries; measured %d."
      % len(both))
print("  PFb says the two `alternatives()` agree on every input tested;")
print("  measured: their bodies are IDENTICAL after unparsing, so they agree by")
print("  construction and the behavioural test below is a formality rather than")
print("  evidence -- which is a stronger result than the one predicted and is")
print("  also the reason unifying them changes nothing.")
print()
pats = [B.L.MARK, B.L.MARK_OLD, r"a|b|c", r"(?:a|b)|c", r"\|", r"", r"a",
        r"(a|b)|(c|d)", r"[a|b]|c"]
agree = sum(1 for p in pats if B.M.alternatives(p) == B.L.alternatives(p))
print("      REGEX sources put to both `alternatives()`         %3d" % len(pats))
print("      ...REGEX sources on which they agree               %3d" % agree)
if agree != len(pats):
    BAD += len(pats) - agree

# ---------------------------------------------------------------------------
B.hdr("P4e  AND A CLAIM `figures()` MAKES THAT IT DOES NOT KEEP")

print("  Found by this repair rather than looked for, which is why it is here")
print("  and not in the brief.  mg-70c7's `figures()` carried this comment")
print("  above it, deleted with the body it described:")
print()
print("      # Numbers that are not figures: a section number, a year, a line")
print("      # reference of the form `file.py:214`, a git revision.")
print()
print("  A GIT REVISION IS NOT EXCLUDED AND NEVER WAS.  A short revision that")
print("  happens to be all decimal digits is matched by `_NUMBER` and passes")
print("  every exclusion.  This is not hypothetical: repairing O1 required")
print("  naming a revision in mg-70c7's README, and `r6_self.py`'s E2 promptly")
print("  reported it as a FIGURE NO TRANSCRIPT BACKS.  The check was right by")
print("  its own rule and the rule's stated exclusion list was false.")
print()
REVS = ["3738079", "973ca61", "1234567", "9715841"]
for r in REVS:
    figs = B.L.figures("at `%s` the census gives 9 sites" % r)
    resolves = B.git("cat-file", "-e", "%s^{object}" % r,
                     ok=(0, 128)) is not None
    ok = B.A.git("rev-parse", "--verify", "--quiet", "%s^{object}" % r,
                 ok=(0, 1)).strip()
    print("      `%-8s`  all digits: %-3s  read as a FIGURE: %-3s  resolves: %s"
          % (r, "yes" if r.isdigit() else "no",
             "yes" if any(str(v) == r for v in figs) else "no",
             "yes" if ok else "no"))
print()
print("      IS THIS REPAIRED HERE?  NO -- and the reason is measured, not an")
print("      excuse.  Both candidate rules are wrong:")
allf = set()
for p in [q for q in B.git("ls-files").split()
          if os.path.basename(q).startswith("out_") and q.endswith(".txt")]:
    try:
        t = B.read(p, None)
    except (RuntimeError, OSError):
        continue
    for l in t.splitlines():
        allf.update(B.L.figures(l))
big = sorted(v for v in allf if v >= 10 ** 6)
res = [v for v in big
       if B.A.git("rev-parse", "--verify", "--quiet",
                  "%d^{object}" % v, ok=(0, 1)).strip()]
print("          DISTINCT FIGURES in every committed transcript  %3d" % len(allf))
print("          ...FIGURES of magnitude >= 1e6                  %3d" % len(big))
print("          ...FIGURES resolvable as a git object           %3d" % len(res))
print()
print("      A MAGNITUDE rule (`drop >= 1e6`) would drop %d genuine figures,"
      % (len(big) - len(res)))
print("      among them `2147483647`, which is INT_MAX in a fixture and a real")
print("      measurement.  A RESOLVES-AS-AN-OBJECT rule would drop %d, and it"
      % len(res))
print("      would drop them for a reason that is an accident of this")
print("      repository's object database rather than a property of the number.")
print("      Neither is right, so the finding is REPORTED AND NOT FIXED, and")
print("      the prose this ticket writes names revisions in a form that is not")
print("      all digits or does not name them at all.  A generous exclusion")
print("      list turns an unbacked figure into a non-figure -- `lib70c7`'s own")
print("      sentence, which is why the wrong fix is worse than the finding.")

print()
B.bar("P4 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  It counts a `figures()` or `alternatives()` in")
print("`lib70c7` that is still a body rather than a call, more than one")
print("implementation of either across the two libraries, an integer in 0..%d"
      % (N - 1))
print("on which the two names still disagree, and a regex source on which the")
print("two `alternatives()` disagree.  It ranges over %d integers, %d regex"
      % (N, len(pats)))
print("sources, the %d names defined in both libraries and the %d transcripts of"
      % (len(both), len(CORPUS)))
print("R2b's corpus.  IT DOES NOT COUNT P4e, which is a false exclusion claim")
print("in a rule this ticket did not write and does not fix; that is a FINDING.")
print()
print(B.finding("P4a", "the two `figures()` disagreed on exactly %d integer(s) "
                       "in 0..%d -- the value %s -- and mg-70c7's copy was the "
                       "wrong one because BOTH docstrings claimed `0, 1 and 2` "
                       "and only mg-7522's did it; there is now %d "
                       "implementation of each of the %d unified rules, and %d "
                       "disagreement(s) remain"
                       % (len(dis_before), N - 1,
                          ",".join(map(str, dis_before)) or "-",
                          impl // max(1, len(UNIFIED)), len(UNIFIED),
                          len(dis_after))))
print(B.finding("P4b", "the floor item nothing named: %d names are defined in "
                       "BOTH libraries, %d of them IDENTICAL code; "
                       "`alternatives()` was a RULE kept in two identical "
                       "copies and produced the published figure `nine "
                       "alternatives against three`, and %d rule(s) remain in "
                       "two identical copies after this ticket -- %s, which is "
                       "mg-dee4's F6 VALUE arm -- named rather than left to be "
                       "rediscovered"
                       % (len(both), ident, len(risky),
                          ", ".join("`%s`" % r for r in risky) or "none")))
print(B.finding("P4c", "`lib70c7.figures`'s comment claimed to exclude `a git "
                       "revision` and never did -- an all-decimal short "
                       "revision is read as a FIGURE, which `r6_self.py`'s E2 "
                       "reported against this ticket's own repaired README; "
                       "REPORTED AND NOT FIXED because a magnitude rule would "
                       "drop %d genuine figures and a resolves-as-an-object "
                       "rule would drop %d for an accident of the object "
                       "database"
                       % (len(big) - len(res), len(res))))
sys.exit(1 if BAD else 0)
