"""t3_term.py -- OPEN 2 (F-2): KIND AND SCOPE ARE TWO LABELS.

mg-8d5e's summary: `20 sites remain unqualified in the tree, every one a
record, named individually in r3 (iv)`.

  r3 (iii) derives a site's KIND from its PATH -- `out_*.txt` is a
  transcript, `PREDICTIONS.md` is a record, anything else is a LIVE CLAIM --
  and THAT is the rule that decides whether a site gets edited.
  r3 (iv) labels the same residue by SCOPE -- whose ticket owns the file.

The summary reports the SCOPE label as though it were the KIND label.  Under
the repair's own path rule 15 of the 20 are live claims, where the sentence
says 0.

  (i)   THE RESIDUE, RE-DERIVED at this tree by mg-2c77's rule unchanged.
  (ii)  BOTH LABELS, IN TWO COLUMNS -- which is the repair.
  (iii) THIS INSTRUMENT'S OWN FILES, SCORED BY THE SAME RULE.
  (iv)  THE CORRECTED SENTENCE, and the gate that it reports two labels.
  (v)   WHAT CANNOT BE REPAIRED, and why it is a finding rather than a fix.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import collections
import os
import sys

import lib_b2af as L

R = L.Report(
    selfpop="every grep, file read and scoring this script performs, plus "
            "the requirement that the scoring rule be the one mg-2c77 wrote "
            "and that it still distinguish more than one label",
    findpop="every site in the tree stating the term, scored for the "
            "qualifier, labelled by KIND and by SCOPE, and the summary "
            "sentence of dfa263c scored against both labels wherever that "
            "sentence is written")

L.banner("T3", "OPEN 2 (F-2) -- ONE WORD OVER TWO POPULATIONS")

# ---------------------------------------------------------------------------
L.rule("(i) THE RULER WAS NOT MOVED, AND THE RESIDUE RE-DERIVED")
# ---------------------------------------------------------------------------
print("""   The term and the qualifier are mg-2c77's, character for
   character, by way of mg-330a's lib330a.py.  A repair that widens the
   rule closes sites without writing a word, so the rule is checked on
   two constructed inputs whose answers are known before it runs.
""")

HYPH = ["prose above", "the 17 %ss" % L.TERM,
        "inside a %s-of the two files" % L.QUALIFIER.replace(" ", "-"),
        "prose below"]
UNHY = ["prose above", "the 17 %ss" % L.TERM,
        "inside a %s of the two files" % L.QUALIFIER, "prose below"]


def score_lines(lines, idx):
    w = "\n".join(lines[max(0, idx - 3):idx + 4])
    if any(m in w for m in L.QUOTE_MARKERS):
        return "quotes the wide BOUND"
    if L.QUALIFIER in w:
        return "census, QUALIFIED"
    return "*** census, UNQUALIFIED"


print("   constructed site carrying the HYPHENATED form   : %s"
      % score_lines(HYPH, 1))
print("   constructed site carrying the UNHYPHENATED form : %s"
      % score_lines(UNHY, 1))
R.check(score_lines(HYPH, 1).startswith("***"),
        "the scoring rule accepts the hyphenated form as a qualifier -- the "
        "ruler has been widened and sites close without a word being written")
R.check(not score_lines(UNHY, 1).startswith("***"),
        "the scoring rule rejects the unhyphenated form too, so it "
        "distinguishes nothing")

resid = L.residue(exclude=(L.MINE_DIR + "/",))
resid_all = L.residue()
every = L.grep_sites(L.TERM)
labels = collections.Counter(L.disposition(p, n) for p, n in every)
print()
print("   sites in the tree stating the term (untracked included) : %d"
      % len(every))
print("   NON-VACUITY -- distinct labels the rule returned : %d"
      % len(labels))
for lab, k in sorted(labels.items()):
    print("      %-28s %d" % (lab, k))
R.check(len(labels) >= 2,
        "the rule returned one label for every site, so every table below "
        "says nothing")
print()
print("   THE RESIDUE -- sites stating the term UNQUALIFIED,")
print("   excluding this ticket's own files : %d" % len(resid))
print("   mg-330a re-derived 20 at %s." % L.DOCS_POST)

# ---------------------------------------------------------------------------
L.rule("(ii) BOTH LABELS, IN TWO COLUMNS.  THIS IS THE REPAIR.")
# ---------------------------------------------------------------------------
print("""   The two rules are two functions in lib_b2af.py -- `kind_of` reads
   the PATH, `scope_of` reads whose ticket owns the file -- because two
   rules that are one function are two rules that can be confused for
   one another again.
""")

by_kind = collections.Counter(k for _p, _n, k, _s in resid)
by_scope = collections.Counter(s for _p, _n, _k, s in resid)

print("   %-55s %-18s %s" % ("site", "KIND (r3 iii)", "SCOPE (r3 iv)"))
for p, n, k, s in resid:
    print("   %-55s %-18s %s" % ("%s:%s" % (p, n), k, s))

print()
print("   BY KIND -- the path rule, which decides TREATMENT:")
for k in ("live claim", "transcript", "record, pre-run"):
    print("      %-24s %d" % (k, by_kind.get(k, 0)))
print("      %-24s %d" % ("records (both kinds)",
                          by_kind.get("transcript", 0)
                          + by_kind.get("record, pre-run", 0)))
print()
print("   BY SCOPE -- whose ticket owns the file:")
for s, c in sorted(by_scope.items()):
    print("      %-24s %d" % (s, c))
print()
print("   THE TWO COLUMNS DO NOT AGREE, AND THAT IS THE WHOLE FINDING.")
print("   Under SCOPE every one of the %d is another ticket's -- so"
      % len(resid))
print("   `every one a record` is TRUE if `record` means `somebody")
print("   else's record of what they found`.  Under KIND, %d of the %d"
      % (by_kind.get("live claim", 0), len(resid)))
print("   are LIVE CLAIMS -- source and prose -- and the sentence is")
print("   FALSE.  One word, two populations.")

live = by_kind.get("live claim", 0)
records = len(resid) - live
R.check(live + records == len(resid),
        "the KIND labels do not partition the residue")

# ---------------------------------------------------------------------------
L.rule("(iii) THIS INSTRUMENT'S OWN FILES, BY THE SAME RULE")
# ---------------------------------------------------------------------------
print("""   A rule that exempts its author is not a rule.  Every file this
   ticket adds is scored by the same rule as everybody else's.
""")

mine_sites = [(p, n) for p, n in every if p.startswith(L.MINE_DIR + "/")]
mine_unq = [(p, n, k, s) for p, n, k, s in resid_all
            if p.startswith(L.MINE_DIR + "/")]
print("   sites in %s stating the term          : %d"
      % (L.MINE_DIR, len(mine_sites)))
for p, n in sorted(mine_sites):
    print("      %-55s %s" % ("%s:%s" % (p, n), L.disposition(p, n)))
print("   of those, UNQUALIFIED (i.e. added to the residue) : %d"
      % len(mine_unq))
print()
print("   residue excluding this ticket's files : %d" % len(resid))
print("   residue including them                : %d" % len(resid_all))
R.gate(not mine_unq,
       "%d site(s) in this ticket's own files state the census unqualified: "
       "%s.  Scored by the same rule as everybody else's"
       % (len(mine_unq), ", ".join("%s:%s" % (p, n)
                                   for p, n, _k, _s in mine_unq)))

# ---------------------------------------------------------------------------
L.rule("(iv) THE CORRECTED SENTENCE -- BOTH LABELS, REPORTED AS TWO")
# ---------------------------------------------------------------------------

CORRECTED = (
    "%d sites remain unqualified in the tree.  By SCOPE -- r3 (iv) -- every "
    "one is another ticket's.  By KIND -- r3 (iii), the path rule that "
    "decides treatment -- %d are records (%d transcripts, %d prediction "
    "files) and %d are LIVE CLAIMS."
    % (len(resid), records, by_kind.get("transcript", 0),
       by_kind.get("record, pre-run", 0), live))

print("   THE SENTENCE AS WRITTEN, in dfa263c's summary:")
print()
print("     `%d sites remain unqualified in the tree, every one a record,"
      % len(resid))
print("      named individually in r3 (iv).`")
print()
print("   THE SENTENCE WITH THE TWO LABELS SEPARATED:")
print()
for line in ("     " + CORRECTED).split("  "):
    if line.strip():
        print("     %s" % line.strip())
print()

# THE GATE: the corrected sentence must report TWO labels, and the counts it
# reports must be the ones measured above.  A sentence that names one label
# is the defect restated.
names_kind = "KIND" in CORRECTED and "r3 (iii)" in CORRECTED
names_scope = "SCOPE" in CORRECTED and "r3 (iv)" in CORRECTED
counts_ok = (str(live) in CORRECTED and str(records) in CORRECTED
             and str(len(resid)) in CORRECTED)
print("   the corrected sentence names the KIND rule  : %s" % names_kind)
print("   the corrected sentence names the SCOPE rule : %s" % names_scope)
print("   its counts are the ones measured in (ii)    : %s" % counts_ok)
R.check(names_kind and names_scope,
        "the corrected sentence does not report both labels, which is the "
        "defect restated rather than repaired")
R.check(counts_ok,
        "the corrected sentence's counts are not the ones measured above")

# AND IT IS WRITTEN DOWN WHERE A READER WILL FIND IT.
README = os.path.join(L.HERE, "README.md")
readme = ""
if os.path.exists(README):
    with open(README) as fh:
        readme = fh.read()
print()
print("   and the same two-label statement in this ticket's README : %s"
      % ("yes" if ("By KIND" in readme and "By SCOPE" in readme) else "NO"))
R.check("By KIND" in readme and "By SCOPE" in readme,
        "the two-label statement is in the transcript but not in "
        "%s, so a reader of the deliverable does not meet it" % README)

# ---------------------------------------------------------------------------
L.rule("(v) WHAT CANNOT BE REPAIRED, AND WHY THAT IS A FINDING")
# ---------------------------------------------------------------------------
print("""   The sentence is in the COMMIT MESSAGE of %s.  A commit
   message is immutable without rewriting history, and rewriting a
   merged commit to make this ticket's summary come out is a far worse
   act than the defect it would hide.

   So the finding STANDS, and it is named rather than closed.  Every
   copy of the sentence is enumerated from the tree, so a copy this
   script did not remember is still in the population.
""" % L.REPAIR_8D5E[:8])

PHRASE = "every one a record"
copies = L.grep_sites(PHRASE)
msg = L.git_quiet("log", "-1", "--format=%B", L.REPAIR_8D5E)
in_msg = PHRASE in msg
print("   copies of `%s` in the tree : %d" % (PHRASE, len(copies)))
for p, n in sorted(copies):
    print("      %-55s %s" % ("%s:%s" % (p, n), L.kind_of(p)))
print("   in the commit message of %s : %s"
      % (L.REPAIR_8D5E[:8], "yes" if in_msg else "no"))
R.check(in_msg,
        "the sentence under test is not in %s's commit message; this "
        "script is scoring a claim that is not there" % L.REPAIR_8D5E[:8])

R.gate(not in_msg,
       "dfa263c's summary sentence `20 sites remain unqualified in the tree, "
       "EVERY ONE A RECORD` reports r3 (iv)'s SCOPE label as r3 (iii)'s KIND "
       "label.  Re-derived at this tree the residue is %d sites -- the same "
       "%d, none missed -- and under the repair's OWN path rule %d of them "
       "are LIVE CLAIMS where the sentence says 0.  The sentence is in a "
       "COMMIT MESSAGE and cannot be edited; the corrected two-label "
       "statement is published in %s/README.md instead, and this finding is "
       "left standing rather than closed"
       % (len(resid), len(resid), live, L.MINE_DIR))

# ---------------------------------------------------------------------------
L.rule("PREDICTIONS SCORED")
# ---------------------------------------------------------------------------
L.score(R, "P-6a", 20, len(resid), note="the residue at this tree")
print("          -- PREDICTIONS.md calls this `the one I am least sure of`.")
L.score(R, "P-6b", (5, 15), (records, live),
        note="5 records, 15 live claims")
L.score(R, "P-6c", lambda n: 2 <= n <= 8, len(resid_all) - len(resid),
        note="between 2 and 8 more, including my own files")
print("          -- the row reasoned that THIS ticket's prose would state the")
print("             census unqualified.  It does not, for a reason the row "
      "did not")
print("             see: the residue is scored on `%s`, and" % L.TERM)
print("             the word THIS ticket argues about is `record`.  The")
print("             prediction ran two different `words under test` together")
print("             -- one word over two populations, in the prediction for "
      "the")
print("             repair of one word over two populations.  Kept as "
      "written.")
L.score(R, "P-6d", (True, True), (names_kind, names_scope),
        note="both labels reported, and gated")

L.rule("VERDICT")
print("""   F-2 IS ANSWERED BUT NOT CLOSED, and the difference is the point.

   The two labels are now two functions, two columns and two counts,
   and the corrected sentence reports both.  What cannot be done is
   edit a merged commit message, so the finding against dfa263c's
   summary stands -- named, quantified and left standing.  A repair
   that reported this as closed would be claiming to have changed a
   sentence it cannot reach.
""")

sys.exit(R.emit())
