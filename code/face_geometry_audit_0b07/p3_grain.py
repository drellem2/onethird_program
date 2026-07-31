"""mg-0b07 p3 -- THE GRAIN REGRESS: WHERE THE FLOOR ACTUALLY IS.

Gate -> return -> clause, three generations, each one the previous sentence with
a smaller noun.  The subject's answer is that the fourth rung does not exist:
`absorb_trace`'s `shape` condition is now

    if [len(row) for row in A] != [len(row) for row in B]:

with no boolean operator, so nothing inside it can be deleted alone and the
`return` is the finest deletable unit at that site.  That is read out of the
tree and it is TRUE.

IT IS ALSO NOT THE QUESTION.  The regress is not about boolean operators; it is
about the difference between the unit a test PERTURBS and the unit its result is
READ AT.  A list comparison is a disjunction:

    [w for w in A] != [w for w in B]   <=>   len(A) != len(B)
                                        or   some common row width differs

Two conditions, one operator, no `or`.  So this file does not ask whether a
clause can be deleted; it asks what the FINEST UNIT IS WHOSE PERTURBATION THE
BATTERY CAN SEE, and answers it by perturbing each half of that disjunction
alone on the live tree and running the whole battery for each.

The two halves are then perturbed at `b6bc2ef` as well, where they coincide with
mg-c4c8's two clauses, so that the semantic units here and the syntactic units
there can be shown to be the same units under a different spelling rather than
asserted to be.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern0b07 import (                                          # noqa: E402
    BAR, all_boolops, claim, deciding_boolops, census, finding, head,
    report, run_battery, scored_rows, source_at, splice, tree_with,
)

MG9220 = "b6bc2ef"

# The two halves of the live `shape` condition, written as source.  Each is the
# condition with ONE of its two meanings removed and the other left standing --
# the deletion test one level below a `return`, at the only level that is left.
ORDER_ONLY = "len(A) != len(B)"
WIDTH_ONLY = ("any(len(A[i]) != len(B[i]) "
              "for i in range(min(len(A), len(B))))")

# The same two at mg-9220's tree, where they ARE the two clauses.
MERGED_ORDER_ONLY = "m != len(B)"
MERGED_WIDTH_ONLY = "any(len(A[i]) != len(B[i]) for i in range(m))"


def shape_gate(src):
    """The `if` whose body is `absorb_trace`'s `shape` return, located by what
    it returns rather than by line number."""
    for fn in ast.walk(ast.parse(src)):
        if not (isinstance(fn, ast.FunctionDef) and fn.name == "absorb_trace"):
            continue
        for node in ast.walk(fn):
            if not isinstance(node, ast.If) or len(node.body) != 1:
                continue
            b = node.body[0]
            if (isinstance(b, ast.Return) and isinstance(b.value, ast.Call)
                    and any(isinstance(a, ast.Constant) and a.value == "shape"
                            for a in b.value.args)):
                return node
    raise SystemExit("no `shape` gate found")


def perturb(src, text):
    return splice(src, shape_gate(src).test, text)


def run(src, label, base, want_change, want_exit):
    out, code = run_battery(tree_with("face_complex.py", src))
    changed = out != base
    ok = (changed == want_change) and (code == want_exit)
    print("   %-46s %-16s exit %d  %6d bytes  %s"
          % (label, "CHANGES" if changed else "BYTE-IDENTICAL", code,
             len(out), "match" if ok else "MISS"))
    return changed, code, len(out), ok, out


def main():
    print(BAR)
    print("mg-0b07 p3 -- the grain regress: is `clause` the floor?")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md p3):")
    print("   p3.1  absorb_trace has 0 BoolOp of ANY kind")
    print("   p3.2  face_complex.py has BoolOps the subject's enumerator does "
          "not reach: at least 1")
    print("   p3.3  no enumerated clause contains a BoolOp anywhere below it")
    print("   p3.4  S1 order half alone   -> CHANGES,        exit 1")
    print("   p3.5  S2 width half alone   -> BYTE-IDENTICAL, exit 0")
    print("   p3.6  S3 condition = False  -> CHANGES,        exit 1\n")

    live = source_at(None)
    head("1.  THE SYNTACTIC FLOOR -- checked, and the subject is right about it")
    at_bo = [n for n in ast.walk(
        next(f for f in ast.walk(ast.parse(live))
             if isinstance(f, ast.FunctionDef) and f.name == "absorb_trace"))
        if isinstance(n, ast.BoolOp)]
    dec = deciding_boolops(live)
    allb = all_boolops(live)
    dec_at = [f for f, _c in dec if f == "absorb_trace"]
    claim("`absorb_trace` contains %d boolean operator of ANY kind -- not %d "
          "'deciding' ones, %d full stop.  The subject's claim is exact under "
          "the wider reading as well as its own" % (len(at_bo), len(dec_at),
                                                    len(at_bo)),
          not at_bo and not dec_at,
          "a boolean operator returning anywhere in that function, in a "
          "condition that decides a return or in one that does not.  The "
          "subject counts only the first kind; this counts both, so a clause "
          "hidden in a `while`, a comprehension guard or a non-returning `if` "
          "would be caught here and not there",
          "BoolOps in absorb_trace: %d; deciding: %d" % (len(at_bo),
                                                         len(dec_at)))
    missed = len(allb) - len(dec)
    print("   the wider population, for scale: %d BoolOp(s) in "
          "face_complex.py, %d of them\n   in a condition that decides a "
          "return.  The %d others sit in conditions whose\n   body does not "
          "return, and no claim of the subject's covers them -- correctly, "
          "since\n   its sentence names the deciding ones." % (len(allb),
                                                               len(dec), missed))
    claim("and the subject's enumerated population is a PROPER SUBSET of the "
          "file's boolean operators (%d of %d), which is what its sentence "
          "says and is worth printing beside the sentence" % (len(dec),
                                                              len(allb)),
          len(dec) <= len(allb) and missed >= 1,
          "the two populations coinciding, at which point 'deciding' is doing "
          "no work.  This is not a finding: it is the scope of the subject's "
          "claim, measured, so a reader does not take 'every boolean condition' "
          "for 'every boolean operator'",
          "all %d, deciding %d, outside %d" % (len(allb), len(dec), missed))
    deep = [(f, c) for f, c in dec
            for v in c.values
            if any(isinstance(x, ast.BoolOp) for x in ast.walk(v))]
    claim("no enumerated clause contains a boolean operator ANYWHERE below it "
          "(%d of %d) -- the subject checks only whether a clause IS a BoolOp, "
          "which is one rung coarser than this, and on this population the two "
          "agree" % (len(deep), len(dec)),
          not deep,
          "a condition like `a or f(b and c)`: the subject's check tests "
          "`values[i]` for being a BoolOp and would pass, while a clause with a "
          "boolean operator inside it is exactly the case its sentence -- "
          "'top-level clause and clause name the same thing' -- denies.  It is "
          "latent here and not live",
          "clauses with a nested BoolOp: %s"
          % ("; ".join(f for f, _c in deep) if deep else "none"))

    head("2.  THE FLOOR THE SUBJECT DID NOT LOOK FOR")
    print("`[len(row) for row in A] != [len(row) for row in B]` is TRUE exactly "
          "when the two\nlists have different LENGTHS or differ at a common "
          "INDEX.  Two conditions joined\nby a disjunction that Python spells "
          "with no operator.  The subject's docstring says\nthe two clauses "
          "'were saying one thing'; below, each of the two things is removed\n"
          "alone and the whole battery is run for it.\n")
    base, base_code = run_battery(tree_with("face_complex.py", live))
    print("   %-46s %-16s exit %d  %6d bytes  %s"
          % ("S0 -- unperturbed baseline", "-", base_code, len(base),
             "reference"))
    s1 = run(perturb(live, ORDER_ONLY),
             "S1 -- ORDER half alone (%s)" % ORDER_ONLY, base, True, 1)
    s2 = run(perturb(live, WIDTH_ONLY),
             "S2 -- WIDTH half alone", base, False, 0)
    s3 = run(perturb(live, "False"), "S3 -- the whole condition -> False",
             base, True, 1)
    hits = sum(1 for r in (s1, s2, s3) if r[3])
    claim("three perturbations of the ONE-CLAUSE condition, each removing one "
          "of its two meanings and leaving the other standing, %d of 3 "
          "predictions matched" % hits,
          hits == 3,
          "either half ceasing to be separable -- which would need the "
          "condition to stop being a comparison of two lists.  These are not "
          "deletions of syntax and are not offered as such: they are the "
          "finest PERTURBATIONS the site admits, which is the unit the "
          "question is about",
          "S1 %s/%d, S2 %s/%d, S3 %s/%d"
          % ("CHANGES" if s1[0] else "IDENTICAL", s1[1],
             "CHANGES" if s2[0] else "IDENTICAL", s2[1],
             "CHANGES" if s3[0] else "IDENTICAL", s3[1]))

    head("3.  AND THEY ARE mg-c4c8'S TWO CLAUSES, SHOWN AND NOT ASSERTED")
    print("The same two meanings at %s, where the condition still has an `or` "
          "and where\nremoving one of them IS deleting a clause.  If the live "
          "S1/S2 pair and the pinned\nclause-2/clause-1 pair give the same two "
          "answers, the units are the same units.\n" % MG9220)
    print("ONLY `face_complex.py` IS TAKEN FROM THE PIN, and that is "
          "deliberate: the rest of\nthe battery is this tree's, so the two "
          "halves of the comparison differ in the\ncondition and in nothing "
          "else.  It is not that commit's artifact and is not read as\none -- "
          "M0 below is its own baseline.\n")
    merged = source_at(MG9220)
    mbase, mcode = run_battery(tree_with("face_complex.py", merged))
    print("   %-46s %-16s exit %d  %6d bytes  %s"
          % ("M0 -- %s's absorb_trace, this battery" % MG9220, "-", mcode,
             len(mbase), "reference"))
    m1 = run(perturb(merged, MERGED_ORDER_ONLY),
             "M1 -- ORDER half alone (= clause 2 deleted)", mbase, True, 1)
    m2 = run(perturb(merged, MERGED_WIDTH_ONLY),
             "M2 -- WIDTH half alone (= clause 1 deleted)", mbase, False, 0)
    same_shape = (s1[0], s1[1]) == (m1[0], m1[1]) and (s2[0], s2[1]) == (m2[0],
                                                                         m2[1])
    claim("the live tree's two sub-conditions answer exactly as the pinned "
          "tree's two CLAUSES do: order half CHANGES/exit %d on both, width "
          "half BYTE-IDENTICAL/exit %d on both" % (s1[1], s2[1]),
          same_shape and m1[3] and m2[3],
          "the rewrite having changed what either half does.  It did not -- "
          "the subject's 28,900-pair equivalence says so and this says it "
          "again from the battery's side.  Which is the point: the rewrite "
          "preserved the behaviour AND the inertness, and removed only the "
          "syntax that let a deletion test name it",
          "live: S1 %s/%d S2 %s/%d || pinned: M1 %s/%d M2 %s/%d"
          % ("CHANGES" if s1[0] else "IDENTICAL", s1[1],
             "CHANGES" if s2[0] else "IDENTICAL", s2[1],
             "CHANGES" if m1[0] else "IDENTICAL", m1[1],
             "CHANGES" if m2[0] else "IDENTICAL", m2[1]))

    if not s2[0] and s2[1] == 0:
        d = census(live)
        p = census(perturb(live, WIDTH_ONLY))
        finding("B1",
                "THE THIRD RUNG WAS RESPELLED, NOT REMOVED.  On the live tree "
                "the `shape` condition's ORDER half -- `len(A) != len(B)` -- "
                "can be taken out with the width half left standing and the "
                "artifact comes back BYTE-IDENTICAL at %d bytes, exit 0, every "
                "row green.  That is mg-e7bc's sentence with `return` replaced "
                "by `clause` replaced by `sub-condition`, on the tree this "
                "commit shipped." % s2[2],
                "The subject's claim -- 'no boolean operator, so the smallest "
                "deletable unit inside this gate IS the `return`' -- is TRUE "
                "and is about DELETION.  A list comparison is a disjunction "
                "written without an operator, so what changed is that the "
                "inert half stopped being nameable, not that it stopped being "
                "inert.  The subject's own docstring says the two clauses "
                "'were saying one thing'; they were saying two, and one of "
                "them is still invisible to the battery.  AND THE BATTERY "
                "CANNOT TELL THE WIDTH HALF FROM THE WHOLE GATE: S1 and S3 "
                "produce the same %d-byte artifact, so on this population the "
                "order half contributes nothing the width half does not "
                "already contribute.  In the subject's own units this "
                "perturbation is %d return, %d statement, %d clause and a NET "
                "%+d syntax node(s) -- nonzero, so its branch 1 check would "
                "flag it; the exposure is not in the declaration, it is that "
                "no test in the instrument makes this perturbation at all."
                % (s1[2], d.returns - p.returns, d.statements - p.statements,
                   d.clauses - p.clauses, d.nodes - p.nodes))
        finding("B2",
                "AND THE LINE A READER CONSULTS SAYS THE OPPOSITE.  AFTER-5 "
                "prints `FINEST UNIT THIS LINE PERTURBS: one `return` "
                "statement, and nothing finer is removed`.  Nothing finer is "
                "removed BY THAT PATCH; the sentence is read as 'the evidence "
                "reaches all the way down at this site', and it does not.",
                "The ticket mg-c4c8 answered asked for the finest unit to be "
                "stated BESIDE THE TEST so a reader need not assume the "
                "evidence reaches the bottom.  The sentence that was added "
                "states the finest unit OF THE PATCH, which is a different "
                "quantity, and the two differ at exactly this site.  What "
                "would close it: one clause on that line naming the "
                "sub-conditions the guard's condition still separates, or the "
                "S1/S2 pair above run beside AFTER-5.")

    head("4.  A CONDITION WHOSE REMOVAL IS MASKED BY ANOTHER")
    print("The brief also asks for one of these.  `absorb_trace`'s docstring "
          "names it: the\nmagnitude test runs over `j == i` too, so on matrices "
          "with the diagonals this\nbattery builds every `diagonal` violation "
          "is also a magnitude violation.  Deleting\nthe `diagonal` return "
          "should therefore move the TRACE and no DECISION.\n")
    diag = None
    for fn in ast.walk(ast.parse(live)):
        if isinstance(fn, ast.FunctionDef) and fn.name == "absorb_trace":
            for node in ast.walk(fn):
                if (isinstance(node, ast.Return)
                        and isinstance(node.value, ast.Call)
                        and any(isinstance(a, ast.Constant)
                                and a.value == "diagonal"
                                for a in node.value.args)):
                    diag = node
    out, code = run_battery(tree_with("face_complex.py",
                                      splice(live, diag, "pass")))
    fails = [t for m, t in scored_rows(out) if m == "[FAIL]"]
    claim("the `diagonal` return deleted alone: artifact %s, exit %d, %d row(s) "
          "fail -- the gate is MASKED by the magnitude gate that follows it, "
          "and the deletion moves labels rather than answers"
          % ("CHANGES" if out != base else "BYTE-IDENTICAL", code, len(fails)),
          out != base and code == 0 and not fails,
          "a battery pair whose diagonal differs and whose magnitudes agree, "
          "which no poset in this population produces.  This is DISCLOSED in "
          "the subject's docstring and confirmed here rather than found: it is "
          "the masking the brief asks about, and it is the one place where a "
          "deletion changing the artifact is not evidence that anything "
          "depends on the deleted code",
          "%d bytes vs %d baseline; failing rows: %s"
          % (len(out), len(base), fails or "none"))
    return report()


if __name__ == "__main__":
    sys.exit(main())
