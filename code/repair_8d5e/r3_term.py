"""r3_term.py -- A-2: THE TERM, QUALIFIED WHERE IT IS A LIVE CLAIM.

mg-2c77's OPEN 2.  `explicit boolean operand` denotes 39 operands in the
census's two files; mg-69d1's table classifies the 17 that lie inside a
deciding condition; 22 are in no column of it.  The finding offers two repairs
-- *fix the walk or fix the term* -- and this ticket fixes the TERM.  Why,
stated before the measurement:

  THE BOUND SENTENCE IS ALREADY RIGHT AND ALREADY NARROW.  mg-69d1 narrowed
  it to DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS OF THE DECIDING
  CONDITIONS IN THE FILES THIS SWEEP VISITS, AND NOTHING ELSE, and mg-2c77
  says so explicitly: *the narrowed BOUND sentence itself is NOT affected: it
  names `the deciding conditions` and is correct.*  Widening `boolean_operands`
  to walk whole modules would not widen the SWEEP by one operand -- the sweep
  deletes top-level operands of deciding conditions and nothing else -- so it
  would relabel 22 operands into a column while leaving the bound saying what
  it says now.  The term is the thing out of step with the bound, and the
  bound is the thing that was measured.

WHAT THIS SCRIPT MEASURES, in order:

  (i)   both populations, WALKED HERE, and the 22 in no column named
  (ii)  the scoring rule -- mg-2c77's, not a wider one -- and its control at
        the revision where mg-2c77's own table was committed
  (iii) the 15 sites in files `d01ff32` touched, each with its KIND DERIVED
        from its path and the treatment that kind gets
  (iv)  every site in the tree NOW, with a disposition each, including this
        deliverable's own files
  (v)   the sweep unmoved: the edit to the shipped classifier is a comment and
        the parsed module is identical

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import ast
import os
import sys

import lib8d5e as L

R = L.Report(
    selfpop="every source read and AST parse this script performs, the "
            "requirement that both census files parse and that neither walk "
            "come back empty, and the requirement that the scoring rule "
            "return more than one label over the tree it scores",
    findpop="every operand of every `and`/`or` in the census's two files "
            "against mg-69d1's four columns; the 15 sites in files d01ff32 "
            "touched, each scored by mg-2c77's rule after the repair; every "
            "site in the tree stating the term, scored for a disposition; "
            "and the parsed module of the shipped classifier before and "
            "after the edit made to it here")

L.banner("R3", "A-2 -- THE TERM, QUALIFIED WHERE IT IS A LIVE CLAIM")
print("""
A count is a number and a population.  `17` was right about the population
`boolean_operands` walks and wrong about the population its own words name,
and the words are what a reader has.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE TWO POPULATIONS, WALKED HERE")
print("""   `anywhere` walks the WHOLE module for `ast.BoolOp` and takes every
   value of every one -- no filter of any kind.  `deciding` restricts
   that to what lies inside a deciding condition, which is what
   `kern5f9a.boolean_operands` computes and what the four columns
   classify.  The selftest requires the second to agree with the
   SHIPPED walker span for span before this table is read, so the
   difference below is a subtraction and not a disagreement.""")
print()
WIDE, NARROW = {}, {}
for fname in L.CENSUS_FILES:
    src = L.census_source(fname)
    WIDE[fname] = L.all_boolean_operands(src, fname)
    NARROW[fname] = L.deciding_boolean_operands(src, fname)
    R.check(bool(WIDE[fname]),
            "the unrestricted walk over %s came back empty; every number "
            "below is vacuous" % fname)
print("   %-18s %-38s %-22s %s"
      % ("file", "operands of every and/or, anywhere", "of those, deciding",
         "difference"))
for fname in L.CENSUS_FILES:
    print("   %-18s %-38d %-22d %d"
          % (fname, len(WIDE[fname]), len(NARROW[fname]),
             len(WIDE[fname]) - len(NARROW[fname])))
wide_n = sum(len(v) for v in WIDE.values())
narrow_n = sum(len(v) for v in NARROW.values())
print("   %-18s %-38d %-22d %d" % ("ALL", wide_n, narrow_n, wide_n - narrow_n))
print()
narrow_spans = {(o["file"], o["span"]) for v in NARROW.values() for o in v}
outside = [o for v in WIDE.values() for o in v
           if (o["file"], o["span"]) not in narrow_spans]
print("   IN NO COLUMN OF mg-69d1's TABLE : %d" % len(outside))
print()
print("   and they are NAMED, because a count of what is uncovered that")
print("   cannot be pointed at is the same silence as no count at all:")
print()
print("     %-18s %-28s %-5s %-4s %s"
      % ("file", "function", "line", "op", "operand text"))
for o in sorted(outside, key=lambda x: (x["file"], x["line"])):
    print("     %-18s %-28s %-5d %-4s %s"
          % (o["file"], o["func"], o["line"], o["op"],
             " ".join((o["text"] or "").split())[:40]))
print()
R.check(wide_n >= narrow_n,
        "the unrestricted walk (%d) returned FEWER operands than the "
        "restricted one (%d); one of the two walks is wrong and the "
        "subtraction is meaningless" % (wide_n, narrow_n))
print("   THE REPAIR IS TO THE TERM AND NOT TO THE WALK, so both numbers are")
print("   expected to be exactly what mg-2c77 measured -- 39 and 17 -- and a")
print("   change in either would mean this ticket moved something it said it")
print("   was leaving alone.")
R.gate((wide_n, narrow_n) == (39, 17),
       "the two populations read %d and %d where mg-2c77 measured 39 and 17.  "
       "This ticket repairs the TERM and not the WALK, so a movement in "
       "either is a change nothing here asked for"
       % (wide_n, narrow_n))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE SCORING RULE, AND ITS CONTROL")
print("""   THE RULE IS mg-2c77's, character for character.  A site is
   QUALIFIED if the words `deciding condition` stand within 3 lines of
   it in the same file; it QUOTES THE WIDE BOUND if `NO FURTHER` or
   `is read as` stands in the same window; otherwise it asserts the
   census unqualified.

   THE UNHYPHENATED WORDS ARE THE TEST.  mg-2c77's rule does not accept
   `deciding-condition`: its own q3_operands.py lines carrying the
   hyphenated form were scored UNQUALIFIED by it.  Widening the rule to
   accept the hyphen would have closed this finding by moving the
   ruler, so every site repaired here carries the unhyphenated words in
   the window as well as the hyphenated term in its sentence.

   THE CONTROL.  The rule is run at %s -- the revision where mg-2c77's
   table was committed -- and required to return that table's own 15
   in-`d01ff32` sites.  Two rules that agree on constructed inputs can
   still disagree on a tree.""" % L.Q3_REV_PIN[:8])
print()
touched = L.files_of(L.D01FF32_PIN)
then = L.score_all(rev=L.Q3_REV_PIN)
then_unq = sorted((p, n) for p, n, d in then
                  if d.startswith("***") and p in touched)
print("   sites stating the term at %s      : %d" % (L.Q3_REV_PIN[:8],
                                                     len(then)))
print("   of those, UNQUALIFIED                    : %d"
      % len([1 for _p, _n, d in then if d.startswith("***")]))
print("   of those, in files d01ff32 touched       : %d" % len(then_unq))
print("   mg-2c77's finding names                  : 15")
print()
R.check(len(then_unq) == 15,
        "the rule returns %d in-d01ff32 unqualified sites at %s where "
        "mg-2c77's finding names 15; the control fails and section (iii) "
        "rests on a rule that does not reproduce the table it is repairing"
        % (len(then_unq), L.Q3_REV_PIN[:8]))
_labels_then = set(d for _p, _n, d in then)
R.check(len(_labels_then) >= 2,
        "the rule returned one label for every site at %s; it is not "
        "distinguishing and every table below says nothing" % L.Q3_REV_PIN[:8])
print("   NON-VACUITY -- distinct labels the rule returned over that tree: %d"
      % len(_labels_then))
for lab in sorted(_labels_then):
    print("      %s" % lab)
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE 15, EACH WITH ITS KIND -- AND THE KIND IS DERIVED")
print("""   THE RULE FOR WHAT A SITE GETS, stated before the table:

     a LIVE CLAIM about what the instrument covers  -- source, prose,
       documentation -- is EDITED to carry the qualifier.
     a TRANSCRIPT is not edited.  The source line that PRINTS it is
       edited and the script is re-run by its own runner; a transcript
       is a measurement and hand-editing one is falsifying it.
     a RECORD committed before its own run -- a PREDICTIONS file -- gets
       an ADDENDUM with the original text left standing.  A later
       ticket does not get to rewrite what an earlier one predicted.

   The KIND IS DERIVED from the path, not listed: `out_*.txt` is a
   transcript, `PREDICTIONS.md` is a record, anything else is live.""")
print()


def kind_of(path):
    base = os.path.basename(path)
    if base.startswith("out_") and base.endswith(".txt"):
        return "transcript"
    if base == "PREDICTIONS.md":
        return "record, pre-run"
    return "live claim"


TREATMENT = {"transcript": "re-run by its own runner",
             "record, pre-run": "ADDENDUM, original standing",
             "live claim": "EDITED to carry the qualifier"}

now = L.score_all()
now_by_site = {(p, n): d for p, n, d in now}
print("   %-52s %-5s %-16s %-28s %s"
      % ("site (line as at %s)" % L.Q3_REV_PIN[:8], "line", "kind",
         "treatment", "now"))
still_unq = []
for path, lineno in then_unq:
    k = kind_of(path)
    # the site MOVED if the file was edited, so it is re-found by content
    # rather than by line number -- a line number is an anchor into a file's
    # text and re-points when the text is edited, which is A-1 in miniature.
    here = [n for (p, n) in now_by_site if p == path]
    worst = "gone"
    if here:
        labels = [now_by_site[(path, n)] for n in here]
        worst = ("*** census, UNQUALIFIED"
                 if any(x.startswith("***") for x in labels)
                 else sorted(set(labels))[0])
    print("   %-52s %-5s %-16s %-28s %s"
          % (path, lineno, k, TREATMENT[k], worst))
    if worst.startswith("***"):
        still_unq.append(path)
print()
print("   files that carried an unqualified site and still carry one : %d"
      % len(set(still_unq)))
R.gate(not still_unq,
       "%d file(s) in the repair's own population still state the census "
       "without the deciding-condition qualifier after this repair: %s"
       % (len(set(still_unq)), ", ".join(sorted(set(still_unq)))))
print()
print("   The `now` column is scored PER FILE and not per line, because a")
print("   line number is an anchor into a file's text: editing the file moves")
print("   every site below the edit.  Scoring the old line number in the new")
print("   file would be A-1 in miniature -- the same number, about a")
print("   different line.")
print()

# ---------------------------------------------------------------------------
L.rule("(iv) EVERY SITE IN THE TREE NOW, WITH A DISPOSITION")
print("""   The population is READ FROM THE TREE, untracked files included --
   this deliverable's own files are in it and are marked.  Excluding
   them by path would be the path list this lineage keeps rebuilding.

   THE RESIDUE IS NAMED, NOT COUNTED.  Sites outside the repair's
   population are not edited here, and each one says why: it is a
   RECORD -- an audit's statement of what it found, or a transcript, or
   a prediction file -- and rewriting another ticket's record to make
   this ticket's count come out is the failure this arc exists to
   avoid.""")
print()


def scope_of(path):
    if L.is_mine(path):
        return "THIS REPAIR"
    if path in touched:
        return "in d01ff32"
    if path.startswith("code/audit_2c77/"):
        return "mg-2c77's record"
    if path.startswith("code/face_geometry_audit_eaef/") \
            or "audit-mg-eaef" in path:
        return "mg-eaef's record"
    return "elsewhere"


print("   %-56s %-5s %-18s %s"
      % ("site", "line", "scope", "disposition"))
counts = {}
unq_now = []
for path, lineno, disp in now:
    sc = scope_of(path)
    counts[(sc, disp.startswith("***"))] = \
        counts.get((sc, disp.startswith("***")), 0) + 1
    if disp.startswith("***"):
        unq_now.append((path, lineno, sc))
    print("   %-56s %-5s %-18s %s" % (path, lineno, sc, disp))
print()
print("   %d site(s) in all; %d state the census without the "
      "deciding-condition\n   qualifier." % (len(now), len(unq_now)))
print()
print("   %-24s %s" % ("scope", "unqualified sites remaining"))
for sc in sorted(set(s for _p, _n, s in unq_now)) or ["-- none --"]:
    print("   %-24s %d" % (sc, len([1 for _p, _n, s in unq_now if s == sc])))
print()
R.gate(not [1 for _p, _n, sc in unq_now if sc == "in d01ff32"],
       "%d site(s) in files d01ff32 touched still state the census "
       "unqualified: %s"
       % (len([1 for _p, _n, sc in unq_now if sc == "in d01ff32"]),
          ", ".join("%s:%s" % (p, n) for p, n, sc in unq_now
                    if sc == "in d01ff32")))
R.gate(not [1 for _p, _n, sc in unq_now if sc == "THIS REPAIR"],
       "%d site(s) in THIS DELIVERABLE'S OWN FILES state the census "
       "unqualified: %s.  A repair for a term that means two things cannot "
       "use it in two ways"
       % (len([1 for _p, _n, sc in unq_now if sc == "THIS REPAIR"]),
          ", ".join("%s:%s" % (p, n) for p, n, sc in unq_now
                    if sc == "THIS REPAIR")))
R.gate(not [1 for _p, _n, sc in unq_now if sc == "elsewhere"],
       "%d unqualified site(s) fall in no named scope: %s.  Every one that "
       "is not repaired here must be a record and must be said to be one"
       % (len([1 for _p, _n, sc in unq_now if sc == "elsewhere"]),
          ", ".join("%s:%s" % (p, n) for p, n, sc in unq_now
                    if sc == "elsewhere")))
print("   WHAT REMAINS, AND WHY IT REMAINS.  Every site left unqualified is")
print("   an audit's own record -- mg-2c77's finding text and transcripts,")
print("   mg-eaef's instrument and its write-up.  Each states what that audit")
print("   found at the moment it ran.  They are pointed at here and left")
print("   standing; the phrase in them is wide, and this ticket's answer to")
print("   that is this table, not an edit to their record.")
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE SWEEP IS UNMOVED -- THE CLASSIFIER'S EDIT IS A COMMENT")
print("""   The one file this repair touches that anything EXECUTES is
   `kern5f9a.py`, and what was written there is a comment.  Measured
   rather than asserted: the module is parsed before and after and the
   two abstract syntax trees are compared.  Identical trees cannot
   behave differently.

   `before` is reached by the property -- the newest revision of the
   file that does not carry the comment's own marker -- so this row is
   correct both before this repair is committed and after.""")
print()
KERN_REL = L.INSTR_DIR + "/kern5f9a.py"
MARK = "THE QUALIFIER IS LOAD-BEARING"
pre = L.last_lacking(KERN_REL, MARK)
R.check(pre is not None,
        "no revision of kern5f9a.py lacks this repair's marker; the before "
        "column cannot be built and section (v) is withdrawn")
if pre:
    before_src = L.git_show(pre, KERN_REL)
    after_src = L.read_worktree(KERN_REL)
    same_ast = ast.dump(ast.parse(before_src)) == ast.dump(ast.parse(
        after_src))
    print("   kern5f9a.py before this repair, derived : %s" % pre[:8])
    print("   the source text differs                 : %s"
          % ("yes" if before_src != after_src else "no"))
    print("   the PARSED MODULE differs               : %s"
          % ("YES" if not same_ast else "no"))
    R.check(before_src != after_src,
            "kern5f9a.py is byte-identical before and after; the row above is "
            "vacuous because no edit was made")
    R.gate(same_ast,
           "the edit to kern5f9a.py changed the parsed module, so it is not "
           "the comment this repair says it is and the sweep's behaviour is "
           "not known to be unmoved")
print()

L.rule("VERDICT")
print("""   The term is qualified wherever it is a live claim, and the walk
   is untouched.

   the two populations                          : %d anywhere, %d deciding
   operands in no column of mg-69d1's table     : %d, named in (i)
   sites in files d01ff32 touched, unqualified  : %d (was 15)
   sites in this deliverable's own files        : %d
   sites left unqualified anywhere, all records : %d
   the shipped classifier's parsed module       : %s
"""
      % (wide_n, narrow_n, len(outside),
         len([1 for _p, _n, sc in unq_now if sc == "in d01ff32"]),
         len([1 for _p, _n, sc in unq_now if sc == "THIS REPAIR"]),
         len(unq_now),
         "unchanged" if pre and same_ast else "MOVED"))

sys.exit(R.emit())
