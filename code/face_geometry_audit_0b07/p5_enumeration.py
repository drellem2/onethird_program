"""mg-0b07 p5 -- DID THE ENUMERATION HAPPEN, AND IS EACH ITEM CHECKED OR NAMED?

The question this file asks is NOT whether the repair works.  A repair can be
entirely correct on its stated job and never have asked whether it is an artifact
of the same kind as the defect it repairs; only the second question tests the
discipline.  So:

  * did it produce a LIST?
  * is the list ITS OWN?
  * did it CHECK each item, or name them?
  * where a branch says it cannot exhibit the defect, is the REASON true -- and
    does the reason support the conclusion drawn from it?

A stated reason is a legitimate outcome and is checked here as such; an
unexplained absence is the gap.  Two of the subject's eight carry reasons, and
both reasons are examined rather than counted.

AND THE SAME QUESTION IS ASKED OF THIS AUDIT, at the end, with its own list.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry_instr_5f9a"))

from kern0b07 import (                                          # noqa: E402
    BAR, INSTR, census, claim, finding, head, instrument_copy, report,
    run_instrument, source_at,
)

import d2_deletion as SUBJ                                      # noqa: E402

# The claim each CHECKED branch names, located in the subject's source by a
# distinctive fragment of the claim's own text rather than by line number.
BRANCH_CLAIM = {
    1: "NOT COARSER THAN ITS OWN PATCH",
    # THIS AUDIT'S OWN MISS, KEPT.  The first locator for branch 2 was the
    # printed sentence "The file the battery ran on", which reported MISSING and
    # made this claim BROKEN -- not because the check is absent but because that
    # sentence is split across two adjacent string literals in the source and no
    # contiguous substring of the file contains it.  A locator that reads a
    # printed sentence out of source code is looking for the wrong artifact.  It
    # now locates the MECHANISM, which is what the branch claims: the read-back,
    # and its appearance in the claim's own verdict expression.
    2: "and same_tree",
    3: "THE SWEEP'S OWN GRAIN",
    4: "F1 REPRODUCES AT ITS OWN COMMIT",
    5: "THE ONE-CLAUSE CONDITION IS THE TWO-CLAUSE CONDITION",
    8: "mg-c4c8's H1 ran exactly these four",
}

MAG = '            if abs(A[i][j]) != abs(B[i][j]):\n'
SIGNS_OLD = ("NEW_SIGNS = ('face_complex.py',\n"
             "             '            signs_read += 1\\n',\n"
             "             '            pass\\n')")


def repoint(new_line):
    return (SIGNS_OLD,
            "NEW_SIGNS = ('face_complex.py',\n"
            "             %r,\n"
            "             %r)" % (MAG, new_line))


# One patch that removes syntax NONE of the three named units names, and one
# that removes the same syntax while adding as much back.
FIRING = repoint('            if A[i][j] != B[i][j]:\n')
BLIND = repoint('            if A[i][j] != abs(abs(B[i][j])):\n')


def status_of(text, fragment):
    for ln in text.split("\n"):
        if fragment in ln and (ln.strip().startswith("[HOLDS")
                               or ln.strip().startswith("[BROKEN")):
            return "HOLDS" if "[HOLDS" in ln else "BROKEN"
    return None


def decl_of(text, tag):
    for ln in text.split("\n"):
        if "%s -- " % tag in ln and "UNIT REMOVED" in ln:
            return ln[ln.index("[UNIT REMOVED"):].strip()
    return None


# THIS AUDIT IS AN ARTIFACT OF THE SAME KIND AS THE THING IT AUDITS: an
# independent measurement of a grain, published as a transcript.  So the same
# enumeration is made for it, and each item is checked by a claim here or
# carries the reason it cannot be.
MY_BRANCHES = [
    ("This audit's census could disagree with the subject's, in which case the "
     "8 of 11 is a statement about one implementation and not about the "
     "patches.",
     "CHECKED, p2 section 3: eleven patches measured by a census written here "
     "from `ast` alone, against the subject's, agreeing on all eleven."),
    ("The perturbations in p3 are not DELETIONS, so calling their result a "
     "granularity finding could be an equivocation on the word.",
     "CHECKED by saying so and by cross-running: p3 section 3 applies the same "
     "two sub-conditions at `b6bc2ef`, where they ARE two clauses someone else "
     "enumerated, and gets the same two answers.  The unit is not this "
     "audit's invention."),
    ("The instrument copy in p1 could differ from the subject's own tree, in "
     "which case the perturbed runs measure the harness.",
     "CHECKED, p1 section 1: the UNPERTURBED copy is run first and its eleven "
     "declarations compared with the committed transcript's."),
    ("This audit's reading of mg-9220's eleven English sentences is a reading, "
     "and a reading is a claim.",
     "CHECKED as far as the question admits: read independently here and "
     "compared with mg-c4c8's, 11 of 11.  It CANNOT be checked further without "
     "parsing English, and two independent readings agreeing is not a proof "
     "and is not offered as one."),
    ("The predictions could have been written after their runs, which is the "
     "provenance form of the same defect.",
     "CHECKED by disclosure and by ordering: `PREDICTIONS.md` is committed, and "
     "the one measurement made BEFORE its prediction was registered "
     "(out_d2_deletion.txt) is marked as such in p1 section 5 and scored as a "
     "report rather than as a prediction."),
    ("The floor item could compare a generated file with itself, which is the "
     "`x == x` shape mg-8aae found.",
     "CHECKED, p6: each regenerated control is rebuilt from ITS OWN GENERATOR "
     "and the result compared with the committed bytes, never file against "
     "file."),
    ("This enumeration could be incomplete -- the branch the subject's list "
     "does not have.",
     "NOT CHECKABLE, and the reason is the same one that makes the subject's "
     "list incomplete: an enumeration cannot enumerate what its author did not "
     "think of.  What is available is to say the list is short and to name what "
     "would extend it -- a second auditor, which is what this ticket is to "
     "mg-64b6."),
]


def main():
    print(BAR)
    print("mg-0b07 p5 -- the enumeration: produced, owned, and checked?")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md p5):")
    print("   p5.1  8 branches, 6 CHECKED, 2 with a stated reason")
    print("   p5.2  6 of 6 named claims located in the subject's source")
    print("   p5.3  branch 1's check, fed a patch removing unnamed syntax: "
          "goes RED")
    print("   p5.4  branch 1's check, fed a SIZE-PRESERVING substitution: "
          "stays GREEN while syntax went")
    print("   p5.5  branch 7's stated reason TRUE; its conclusion FALSE")
    print("   p5.6  no branch covers the enumeration's own completeness\n")

    head("1.  THE LIST EXISTS, TRAVELS WITH THE RUN, AND IS THE SUBJECT'S OWN")
    br = SUBJ.SELF_DEFECT_BRANCHES
    checked = [b for b in br if b[1].startswith("CHECKED")]
    reasoned = [b for b in br if not b[1].startswith("CHECKED")]
    for n, (what, where) in enumerate(br, 1):
        print("   %d. %-9s %s" % (n, where.split(":")[0].split(",")[0],
                                  what.split(".")[0][:96]))
    d2src = open(os.path.join(INSTR, "d2_deletion.py")).read()
    printed = "SELF_DEFECT_BRANCHES" in d2src and "for n, (what, where) in" in d2src
    claim("the enumeration is %d branches, %d CHECKED and %d carrying a stated "
          "reason, and it is PRINTED WITH THE RUN rather than living in a "
          "document beside it" % (len(br), len(checked), len(reasoned)),
          len(br) == 8 and len(checked) == 6 and printed,
          "the list being trimmed, or moving into the landing document where a "
          "transcript would not carry it.  A list that does not travel with "
          "the run is a list a re-runner never sees",
          "checked %d, reasoned %d, printed with the run: %s"
          % (len(checked), len(reasoned), printed))

    located = {}
    for n, frag in BRANCH_CLAIM.items():
        located[n] = frag in d2src
    claim("each CHECKED branch names a claim that EXISTS in the subject's "
          "source: %d of %d located by their own text"
          % (sum(located.values()), len(located)),
          all(located.values()),
          "a branch whose 'CHECKED' points at a claim that is not there -- "
          "which is the failure mode of an enumeration written after the "
          "checks: it names them from memory.  Located by claim text, not by "
          "line number, so a moved claim is still found and a deleted one is "
          "not",
          "; ".join("branch %d: %s" % (n, "found" if ok else "MISSING")
                    for n, ok in sorted(located.items())))
    print("\n   THIS AUDIT'S OWN MISS, KEPT.  p5.2 predicted 6 of 6 and the "
          "first run scored 5:\n   branch 2's locator was the sentence the "
          "check PRINTS, and that sentence is split\n   across two adjacent "
          "string literals in the source, so no contiguous substring of\n   the "
          "file contains it.  The check was there the whole time.  A locator "
          "looking\n   for a printed sentence inside source code is looking for "
          "the wrong artifact --\n   a granularity error of exactly this "
          "lineage's kind, committed by the auditor.  It\n   now locates the "
          "MECHANISM, which is what the branch actually claims.\n")
    # AND BRANCH 2's CHECK IS NARROWER THAN ITS SENTENCE.  It reads back
    # `edits[0][0]` -- the FIRST edit's file -- and the branch says "the mutated
    # file".  A mutation touching two files would leave one unverified.
    multifile = [(m[0], sorted({e[0] for e in m[3]})) for m in SUBJ.MUTATIONS
                 if len({e[0] for e in m[3]}) > 1]
    reads_first = "edits[0][0]" in d2src
    claim("and branch 2's read-back covers every file every mutation touches: "
          "%d of %d mutations edit exactly one file, so reading back "
          "`edits[0][0]` misses nothing today"
          % (len(SUBJ.MUTATIONS) - len(multifile), len(SUBJ.MUTATIONS)),
          not multifile and reads_first,
          "a mutation with edits in two files -- `posets.py` and "
          "`face_complex.py`, say.  The read-back would verify the first and "
          "the branch's sentence, 'the mutated file is read back OFF DISK', "
          "would go on covering both.  Latent, not live, and named here rather "
          "than left for the mutation that introduces it",
          "multi-file mutations: %s; reads edits[0][0]: %s"
          % ("; ".join("%s %s" % (t, f) for t, f in multifile) or "none",
             reads_first))

    head("2.  BRANCH 1's CHECK, EXERCISED -- the grain-free channel")
    print("Branch 1 says the derived declaration has a grain of its own -- "
          "`return`, statement\nand clause are three CHOSEN units -- and that "
          "`nodes`, 'the count with no grain',\ncloses it.  Two mutations are "
          "put through the subject's own d2: one that removes\nsyntax none of "
          "the three names, and one that removes the SAME syntax while putting\n"
          "as much back.\n")
    _t1, d1 = instrument_copy([FIRING])
    out1, _c1 = run_instrument(d1)
    _t2, d2 = instrument_copy([BLIND])
    out2, _c2 = run_instrument(d2)
    st1 = status_of(out1, BRANCH_CLAIM[1])
    st2 = status_of(out2, BRANCH_CLAIM[1])
    print("   FIRING  (`abs(...)` dropped from both sides): %s"
          % decl_of(out1, "AFTER-4"))
    print("           the 'not coarser' claim reads [%s]" % st1)
    print("   BLIND   (`abs(...)` dropped on the left, doubled on the right): %s"
          % decl_of(out2, "AFTER-4"))
    print("           the 'not coarser' claim reads [%s]" % st2)
    claim("branch 1's check FIRES on a patch that removes syntax none of the "
          "three named units names: the claim goes [%s]" % st1,
          st1 == "BROKEN",
          "the node count being dropped, or being computed only where the "
          "three units are nonzero.  This is the subject's own check, run on "
          "this audit's mutation rather than on its own -- which is the "
          "difference between a check that is present and a check that works",
          "declaration: %s" % decl_of(out1, "AFTER-4"))
    live = source_at(None)
    blind_delta = census(live)
    blind_after = census(live.replace(
        MAG, '            if A[i][j] != abs(abs(B[i][j])):\n'))
    if st2 == "HOLDS":
        finding("B4",
                "THE GRAIN-FREE CHANNEL HAS A GRAIN, AND IT IS THE SIZE.  "
                "`nodes` is a NET difference of two total node counts, so a "
                "patch that removes syntax and adds as much back reports 0 "
                "returns, 0 statements, 0 clauses AND 0 nodes.  Run through "
                "the subject's own d2: dropping `abs(...)` from the left of "
                "the magnitude comparison and doubling it on the right changes "
                "what the predicate tests, removes %d node(s) on one side, and "
                "the 'not coarser' claim reads [%s]."
                % (2, st2),
                "Branch 1 is the subject's answer to 'the derived declaration "
                "has a grain of its own', and its remedy has the defect the "
                "branch describes, one level further down: `nodes` is offered "
                "as 'the count with no grain' and its grain is that it "
                "measures a DIFFERENCE rather than a SET.  What would close "
                "it: compare the two trees' node MULTISETS, or report removed "
                "and added separately, so a substitution cannot present as a "
                "no-op.  Scale: the FIRING case above shows the check works "
                "wherever the patch is a net removal, which is every mutation "
                "the instrument currently carries -- this is a hole in the "
                "guard, not a wrong number in the transcript.")
    claim("and the blind case is a real blind spot rather than a construction: "
          "the mutated file's total node count equals the original's (%d vs "
          "%d) while `abs` has left one side of the comparison"
          % (blind_after.nodes, blind_delta.nodes),
          blind_after.nodes == blind_delta.nodes,
          "the two counts differing, which would mean the substitution was not "
          "size-preserving and the demonstration proved nothing.  Both counts "
          "are computed here from `ast`, not read from the subject",
          "before %d nodes, after %d nodes; the three named units all 0"
          % (blind_delta.nodes, blind_after.nodes))

    head("3.  BRANCH 7 -- A STATED REASON, CHECKED, AND WHAT IT SUPPORTS")
    print("Branch 7: 'The regress could continue below a clause -- an operand "
          "of `!=`, a call,\na name.'  Its answer: 'CANNOT ARISE FOR THE "
          "DELETION TEST, and the reason is\nstructural: deleting an operand of "
          "a comparison does not leave a condition, so there\nis no smaller "
          "DELETION at this site.'\n")
    gate = None
    for fn in ast.walk(ast.parse(live)):
        if isinstance(fn, ast.FunctionDef) and fn.name == "absorb_trace":
            for node in ast.walk(fn):
                if (isinstance(node, ast.If) and len(node.body) == 1
                        and isinstance(node.body[0], ast.Return)
                        and isinstance(node.body[0].value, ast.Call)
                        and any(isinstance(a, ast.Constant)
                                and a.value == "shape"
                                for a in node.body[0].value.args)):
                    gate = node
    is_compare = isinstance(gate.test, ast.Compare)
    one_comparator = is_compare and len(gate.test.comparators) == 1
    claim("THE STATED REASON IS TRUE: the `shape` gate's condition is a "
          "comparison with %d comparator, so neither operand can be removed "
          "with a condition left behind -- there is no smaller DELETION at "
          "this site" % (len(gate.test.comparators) if is_compare else -1),
          is_compare and one_comparator,
          "the condition becoming a chained comparison (`a < b < c`), where "
          "dropping one comparator DOES leave a condition.  A stated reason is "
          "checkable and an omission is not; this one is checked and it holds",
          "test is %s with %d comparator(s)" % (type(gate.test).__name__,
                                                len(gate.test.comparators)
                                                if is_compare else -1))
    finding("B3",
            "AND THE CONCLUSION DRAWN FROM IT DOES NOT FOLLOW.  Branch 7's "
            "reason is about DELETION and its conclusion is read as 'the "
            "regress stops here'.  p3 shows the regress continuing: the "
            "condition is a disjunction of two sub-conditions written without "
            "an operator, and removing the order half leaves the artifact "
            "byte-identical, exit 0.",
            "This is the one item in the subject's list where the discipline "
            "was applied and the answer is still wrong, and it is scored that "
            "way DELIBERATELY: the branch was named, a reason was given, and "
            "the reason is true.  It is not a gap.  What it shows is that the "
            "reason answers 'can anything smaller be DELETED' and the "
            "question the lineage is about is 'can anything smaller be "
            "PERTURBED and go unseen' -- and those come apart at exactly this "
            "site.  What would close it: state the branch in terms of "
            "perturbation, and run the two sub-conditions beside AFTER-5.")

    head("4.  WHAT THE LIST DOES NOT HAVE")
    text = " ".join(w + " " + h for w, h in br)
    meta = any(k in text.lower() for k in ("this enumeration", "this list",
                                           "the enumeration could",
                                           "incomplete"))
    prov = any(k in text.lower() for k in ("transcript", "regenerate",
                                           "reproduc"))
    claim("no branch covers the ENUMERATION's own completeness (%s) and none "
          "covers the published TRANSCRIPT's provenance (%s) -- the second is "
          "where finding A1 sits"
          % ("absent" if not meta else "present",
             "absent" if not prov else "present"),
          not meta and not prov,
          "either being added.  This is scored as an ABSENCE and not as a "
          "wrong answer: the brief this audit works to says an unexplained "
          "absence is the gap and a stated reason is not, and these two are "
          "absences.  The subject's claim beside its list says WOULD DIFFER "
          "UNDER: nothing -- which is honest and is also the whole exposure",
          "branches: %d; mentioning the enumeration itself: %s; mentioning "
          "transcript reproducibility: %s" % (len(br), meta, prov))

    head("5.  THE SAME QUESTION, ASKED OF THIS AUDIT")
    print("This audit is an artifact of the same kind as the thing it audits: "
          "an independent\nmeasurement of a grain, published as a transcript.  "
          "Its own branches, printed with\nits own run.\n")
    for n, (what, where) in enumerate(MY_BRANCHES, 1):
        print("  %d. %s\n     %s\n" % (n, what, where))
    mine_checked = [b for b in MY_BRANCHES if b[1].startswith("CHECKED")]
    claim("this audit's enumeration is %d branches, %d checked by a claim in "
          "these files and %d carrying the reason it cannot be"
          % (len(MY_BRANCHES), len(mine_checked),
             len(MY_BRANCHES) - len(mine_checked)),
          len(mine_checked) >= 6,
          "nothing -- this claim is a pointer, scored so the list travels with "
          "the transcript.  The claims that do the work are the ones each "
          "branch names.  It is the same self-referential shape the subject's "
          "own list has, and it is left visible rather than dressed up",
          "checked: %d of %d" % (len(mine_checked), len(MY_BRANCHES)))
    return report()


if __name__ == "__main__":
    sys.exit(main())
