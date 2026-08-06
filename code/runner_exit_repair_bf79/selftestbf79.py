"""selftestbf79 -- the predicates of this repair, put to inputs with KNOWN answers.

Every probe here measures the repository, and a probe that measures the
repository cannot tell a wrong answer from a surprising one.  So each predicate
this tree relies on is first put to a hand-built input whose answer is fixed by
construction, in BOTH directions -- a case it must accept and a case it must
reject.  mg-56dc's T3d found *0 direction tests in either membership predicate*
and that is the finding this file exists not to repeat.

FIXTURES ARE STRINGS AND TEMPORARY FILES, NEVER TRACKED BYTES.  Nothing here
writes into a tracked file; the one on-disk fixture is a `mkdtemp` removed in a
`finally`, and `git status --porcelain` is compared before and after.
"""

import os
import re
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import libbf79 as B

BAD = 0
PORCELAIN_BEFORE = B.git("status", "--porcelain")

B.bar("selftestbf79  EVERY PREDICATE, BOTH DIRECTIONS, KNOWN ANSWERS")


def ck(label, got, want):
    global BAD
    ok = got == want
    if not ok:
        BAD += 1
    print("      %-56s %-14s %s"
          % (label, repr(got)[:14], "OK" if ok else "*** want %r ***" % (want,)))


# ---------------------------------------------------------------------------
B.hdr("T1  count_rows and grain_of -- the CLASSIFIER, both directions")

print("  The population rule first: a count row is a SHAPE over the printed")
print("  line, so a sentence with a number in it must NOT be one.")
print()
ACCEPT = "      distinct executing SITES behind those rows     51"
REJECT = "  The gap is exactly the number of source lines naming 2 scripts."
ck("a `label   <spaces>   N` row is a count row",
   len(B.A.count_rows(ACCEPT)), 1)
ck("...a prose sentence containing a number is NOT",
   len(B.A.count_rows(REJECT)), 0)
ck("...a row with no letters in its label is NOT",
   len(B.A.count_rows("      ---     12")), 0)
ck("...a row with no digits is NOT",
   len(B.A.count_rows("      sites behind those rows     many")), 0)
print()
print("  AND THE CLASSIFIER, on the distinction O1 turns on.  These two rows")
print("  MUST come back the same, and that is the FINDING, not a bug: the")
print("  classifier's axis is SITE-vs-EXECUTION, so it cannot separate a row")
print("  count from a site count.  A self-test that asserted they differ would")
print("  be asserting a property the instrument does not have.")
print()
ck("`sites` classifies as SITE", B.A._classify("sites"), "SITE")
ck("`rows` ALSO classifies as SITE -- the blind spot",
   B.A._classify("rows"), "SITE")
ck("`executions` classifies as EXECUTION",
   B.A._classify("executions"), "EXECUTION")
ck("a label with no grain word classifies as NONE",
   B.A._classify("the thing I counted"), "NONE")
ck("a label with both classifies as BOTH",
   B.A._classify("sites and executions"), "BOTH")
print()
print("  AND THE STAGE, which is what S1 holds this tree to:")
ck("grain on the label itself -> stage `label`",
   B.grain_ledger("      SITES outside it      9")[0][4], "label")
ck("grain one line above -> stage `prev`",
   B.grain_ledger("  counted over SITES\n      outside it      9")[0][4],
   "prev")
ck("grain only in a header 4 lines up -> stage `header`",
   B.grain_ledger("  the SITES table\n  x\n  y\n  z\n"
                  "      outside it      9")[0][4], "header")
ck("no grain anywhere -> stage `-`",
   B.grain_ledger("      outside it      9")[0][4], "-")

# ---------------------------------------------------------------------------
B.hdr("T2  exec_site_rows / exec_sites -- the TWO GRAINS, by construction")

print("  A fixture with a KNOWN answer: one file, two executing lines, one of")
print("  which names two scripts.  So the answer is 3 ROWS and 2 SITES by")
print("  construction, and any parser that returns 3 and 3 or 2 and 2 is wrong")
print("  in a way this fixture can see.")
print()
print("  THE FIXTURE IS INTENT-TO-ADDED, and the first draft of this section is")
print("  why.  `exec_site_rows` builds its population from `git ls-files`, so a")
print("  fixture written only to DISK is invisible to it and the four rows below")
print("  came back 0 -- which reads as a broken parser and is actually an")
print("  untracked file.  That is `lib70c7.outs()`'s own recorded defect,")
print("  reproduced from the other side: *a tree's transcripts are untracked on")
print("  the run that first produces them, so a corpus built from the index is")
print("  EMPTY on that run*.  `git add -N` puts the path in the index without")
print("  its content, and it is removed in the `finally`; T6 below is what")
print("  establishes that the index came back.")
print()
tmp = tempfile.mkdtemp(prefix="_bf79_", dir=os.path.dirname(
    os.path.abspath(__file__)))
rel = os.path.relpath(os.path.join(tmp, "fx.py"), B.REPO)
try:
    with open(os.path.join(tmp, "fx.py"), "w") as fh:
        fh.write("import subprocess\n"
                 "subprocess.run(['sh', 'alpha.sh'])\n"
                 "subprocess.run(['sh', 'beta.sh', 'gamma.sh'])\n")
    B.git("add", "-N", "--", rel)
    listed = rel in B.git("ls-files", "--", rel).split()
    ck("the fixture is in the population `ls-files` returns", listed, True)
    rows = B.A.exec_site_rows(None)
    mine = [r for r in rows if r[0] == rel]
    ck("(site,target) ROWS in the fixture", len(mine), 3)
    ck("...distinct SITES behind them", len(B.A.exec_sites(mine)), 2)
    ck("...the gap is the multi-target line",
       len(mine) - len(B.A.exec_sites(mine)), 1)
    ck("...the targets, sorted", sorted(r[2] for r in mine),
       ["alpha.sh", "beta.sh", "gamma.sh"])
finally:
    B.git("rm", "--cached", "--quiet", "--force", "--", rel, ok=(0, 1, 128))
    shutil.rmtree(tmp, ignore_errors=True)
print()
print("      fixture directory removed                          %s"
      % ("yes" if not os.path.exists(tmp) else "*** NO ***"))
if os.path.exists(tmp):
    BAD += 1
print("      fixture removed from the index                     %s"
      % ("yes" if rel not in B.git("ls-files", "--", rel).split()
         else "*** NO ***"))
if rel in B.git("ls-files", "--", rel).split():
    BAD += 1

# ---------------------------------------------------------------------------
B.hdr("T3  published_by -- a PROPERTY, and the escaping defect it had")

print("  The direction that matters: a tag that matches NOTHING must return an")
print("  EMPTY population, not everything.  This is the exact test the first")
print("  draft would have failed -- `--grep='\\(nonexistent\\)'` in BASIC regex")
print("  reduces to the bare string and matches whatever it happens to contain.")
print()
ck("a tag no commit subject carries -> empty population",
   B.published_by("(mg-zzzz-no-such-item)"), [])
ck("...and no commits", B.provenance_commits("(mg-zzzz-no-such-item)"), [])
print()
print("  AND THE PARENTHESES ARE LITERAL, which is the whole of the fix.  The")
print("  bare id must NOT select the same commits as the parenthesised one,")
print("  because a body mentioning `mg-70c7` is not a commit that published it:")
print()
paren = B.provenance_commits("(mg-70c7)")
bare = [c for c in B.provenance_commits("mg-70c7")]
ck("commits whose subject carries `(mg-70c7)`", len(paren), 6)
print("      COMMIT ITEMS merely containing `mg-70c7`           %3d" % len(bare))
ck("...strictly more than the parenthesised ones", len(bare) > len(paren), True)
print()
print("  AND THE POPULATION'S CLAUSES, each with a case that must be EXCLUDED:")
pop = B.published_by("(mg-70c7)")
ck("the population contains a transcript of the subject",
   "%s/out_r4_property.txt" % B.SUBJECT in pop, True)
ck("...and the published document, 4 directories away",
   B.SUBJECT_DOC in pop, True)
ck("...and NOT `lib7522.py`, which it MODIFIED not added",
   "%s/lib7522.py" % B.LIB7522 in pop, False)
ck("...and NOT a `*.py` of its own, which is not a printed count",
   "%s/r4_property.py" % B.SUBJECT in pop, False)
ck("...and NOT mg-56dc's README, whose BODY names mg-70c7",
   "%s/README.md" % B.AUDIT in pop, False)
ck("the population size", len(pop), 11)

# ---------------------------------------------------------------------------
B.hdr("T4  figures / alternatives -- ONE rule each, and the 3")

print("  The unification, put to the value it turned on:")
print()
ck("`3` is a figure under the one rule", B.L.figures("3"), [3])
ck("...and under `lib70c7.figures`, which now calls it",
   B.M.figures("3"), [3])
ck("...and was NOT under the old `lib70c7` rule",
   B.A.figures("3", small=3), [])
ck("`2` is a figure under neither", B.L.figures("2") + B.M.figures("2"), [])
ck("a `:`-prefixed number is not a figure",
   B.L.figures("s3_figure.py:154"), [])
ck("`on line 89` is not a figure", B.L.figures("on line 89"), [])
print()
print("  THE FALSE EXCLUSION WAS ASSERTED AS FALSE HERE, so that a later")
print("  ticket fixing `figures()` would turn this row red and name itself.")
print("  IT FIRED.  mg-5035 repaired the rule and this row went red, which is")
print("  the only reason it is being edited now -- the tripwire worked and is")
print("  re-pointed at the new truth rather than deleted, because a deleted")
print("  tripwire leaves nothing to say the claim was ever false:")
ck("an all-digit DECLARED revision is NOT a figure (P4e closed by mg-5035)",
   B.L.figures("at 3738079 the census"), [])
print("      ^ was `[3738079]` from mg-70c7 until mg-5035.  The claim")
print("        `figures() excludes a git revision` was FALSE for the whole")
print("        life of the rule and is true from `mg-5035` on.")
ck("...and a revision-shaped number with NO declaration is still a figure",
   B.L.figures("brute force over all 33554432 relations"), [33554432])
print()
ck("the two `alternatives()` agree on `MARK`",
   B.M.alternatives(B.L.MARK) == B.L.alternatives(B.L.MARK), True)
ck("`MARK` has mg-dee4's D4 union of ten", B.L.alternatives(B.L.MARK), 10)
ck("...and `proven` is one of them", bool(B.L.MARK.search("proven")), True)
ck("...and was NOT before the restoration",
   bool(re.compile(B.L.MARK.pattern.replace(r"|\bproven\b", ""),
                   re.I).search("proven")), False)
ck("a `(?:a|b)` group is one alternative", B.L.alternatives(r"x|(?:a|b)"), 2)
ck("an escaped `\\|` is not an alternative", B.L.alternatives(r"a\|b"), 1)

# ---------------------------------------------------------------------------
B.hdr("T5  same_body / defined_names -- the duplicate census")

L70 = "%s/lib70c7.py" % B.SUBJECT
L75 = "%s/lib7522.py" % B.LIB7522
ck("`bar` is IDENTICAL in both libraries", B.same_body("bar", L70, L75), True)
ck("`for_loops` DIFFERS", B.same_body("for_loops", L70, L75), False)
ck("`figures` is now a delegation, so it differs",
   B.same_body("figures", L70, L75), False)
ck("`defined_names` finds a module-level def",
   "published_by" in B.defined_names(L70), True)
ck("...and does NOT find a nested one",
   "sub" in B.defined_names(L75), False)

# ---------------------------------------------------------------------------
B.hdr("T6  NO TRACKED BYTE MOVED")

after = B.git("status", "--porcelain")
same = after == PORCELAIN_BEFORE
print("      `git status --porcelain` unchanged across this run  %s"
      % ("yes" if same else "*** NO ***"))
if not same:
    BAD += 1
    was = set(PORCELAIN_BEFORE.splitlines())
    for line in after.splitlines():
        if line not in was:
            print("          *** %s" % line)
print()
print("  P3d DOES write `lib7522.py` and restore it, which is why that probe")
print("  asserts byte-identity itself rather than relying on this row: this")
print("  file's run and that one's are different processes.")

print()
B.bar("selftestbf79 TOTAL BAD: %d" % BAD)
print()
print("EXTENT OF THAT NUMBER.  Every row above is a predicate put to an input")
print("whose answer is fixed by construction or by another tree's committed")
print("transcript, in BOTH directions -- mg-56dc/T3d found 0 direction tests in")
print("either membership predicate and this file is the answer to that.  It")
print("does NOT establish that the predicates are the RIGHT ones; it establishes")
print("that they compute what their docstrings say.  T1's `rows`-is-SITE row is")
print("the clearest case of the difference: the assertion is that the")
print("classifier has the blind spot, not that the blind spot is correct.")
sys.exit(1 if BAD else 0)
