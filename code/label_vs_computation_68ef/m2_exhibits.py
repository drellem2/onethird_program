"""m2 -- THE TWO EXHIBITS, READ OUT OF THE TREE, AND NEITHER IS REACHABLE.

`mg-9d9e` corrected two of its own prose defects by re-reading and the ticket treats them as one
class.  They are not one class, and neither of them is the class the ticket's own sentence names.

⚠️ P6 IS REFUTED BY THE FIRST THING THIS ARM READ, AND THE REFUTATION IS THE FINDING.  The
pre-registration predicted the check would fire on exhibit B's COLUMN at `PRE_CORRECTION` and fall
silent at `AS_OF`.  It does neither, because **the column header was never wrong**: it reads
`note's ceiling 0.9399(a+b)` at both revisions and agrees with the expression that fills it at
both.  What the correction moved was a PROSE NOTE four lines above the table.

Everything is read out of the tree at both revisions and never re-typed (`mg-d2c2`).
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib68ef as L                                                     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
R = L.Report("m2  THE TWO EXHIBITS -- P6 REFUTED: THE MISLABELLED COLUMN IS NOT A COLUMN, AND "
             "THE OTHER EXHIBIT FAILS SAFE-LOOKING")

PRE = L.resolve(L.PRE_CORRECTION)
PIN = L.resolve(L.AS_OF)

R.line()
R.line("   AS_OF          = %s" % PIN)
R.line("   PRE_CORRECTION = %s   (p9d9e's own commit; the correction landed at e9432cd)" % PRE)
R.line("   exhibit B      = %s" % L.EXHIBIT_B)
R.line("   exhibit A      = %s" % L.EXHIBIT_A)
R.line()
R.note("Both revisions are resolved through `git rev-parse --verify`, which REFUSES rather than")
R.note("answering about a commit it cannot find -- every figure here is a small number and an")
R.note("unresolvable pin returns a small number for free.")

# =============================================================================================
R.banner("m2.1  EXHIBIT B IS NOT A MISLABELLED COLUMN.  The column header is byte-identical at "
         "both revisions and AGREES with its computation at both")

R.note("The ticket says: `s1.6's header labelled compression2's per-node ceiling (1-c)(a+b) where")
R.note("the arm computes and the note means c(a+b)`.  Read at the two commits, the word `header`")
R.note("means the SECTION'S PROSE and not the table's column header.  That distinction is the")
R.note("whole of what is buildable here, so it is measured rather than glossed.")
R.line()

state = {}
for rev, tag in ((PRE, "PRE "), (PIN, "AS_OF")):
    src = L.show(rev, L.EXHIBIT_B)
    tree = ast.parse(src)
    assigns = L.local_assignments(tree)
    tables = L.find_tables(L.EXHIBIT_B, src)
    target = [t for t in tables if any("note's ceiling" in c for c in t.cols)]
    if len(target) != 1:
        raise L.Refused("s1.6's table is not where this arm expects it at %s" % tag)
    t = target[0]
    idx = [i for i, c in enumerate(t.cols) if "note's ceiling" in c][0]
    v, lits, elits = L.adjudicate(t.cols[idx], t.args[idx], assigns)
    state[tag] = (t, idx, v, lits, elits, ast.unparse(t.args[idx]),
                  ast.unparse(assigns[t.args[idx].id]) if isinstance(t.args[idx], ast.Name)
                  and t.args[idx].id in assigns else "")
    R.line("   %s  column %d of the s1.6 table" % (tag, idx))
    R.line("        label       %r" % t.cols[idx])
    R.line("        computation `%s`  ->  `%s`" % (state[tag][5], state[tag][6]))
    R.line("        literals    label %-12s computation %-12s   VERDICT %s"
           % (lits, elits, v))

R.line()
R.verdict(state["PRE "][0].cols[state["PRE "][1]] == state["AS_OF"][0].cols[state["AS_OF"][1]],
          "THE COLUMN LABEL IS BYTE-IDENTICAL ACROSS THE CORRECTION",
          "%r at both -- so no check on the column could have fired, whatever it did"
          % state["PRE "][0].cols[state["PRE "][1]])
R.verdict(state["PRE "][2] == L.AGREE and state["AS_OF"][2] == L.AGREE,
          "and it AGREES with its computation at BOTH revisions",
          "0.9399 in the label and 0.9399 in `0.9399 * size * k`; the column was right the whole "
          "time and the number it printed was right the whole time")

R.line()
R.note("SO WHERE WAS THE DEFECT?  In the section's introductory prose, and the diff is one hunk:")
pre_notes = [s for _, s, _ in L._string_constants(ast.parse(L.show(PRE, L.EXHIBIT_B)))
             if "(1-c)" in s]
pin_notes = [s for _, s, _ in L._string_constants(ast.parse(L.show(PIN, L.EXHIBIT_B)))
             if "(1-c)" in s]
for s in pre_notes:
    R.line("      PRE   %r" % s)
for s in pin_notes:
    R.line("      AS_OF %r" % s)
if not pin_notes:
    R.line("      AS_OF (none -- the string is gone)")
R.verdict(len(pre_notes) == 1 and len(pin_notes) == 0,
          "the wrong formula lived in exactly ONE prose string and the correction deleted it",
          "a sentence with NO positional link to any expression -- there is no row template "
          "beneath it, no rule line above it, and nothing that says which computation it is "
          "about")

# =============================================================================================
R.banner("m2.2  AND THE PROSE FORM IS NOT REACHABLE EITHER, MEASURED RATHER THAN ASSERTED -- "
         "the wrong label's only literal is 1, and 1 is in the section's own arithmetic")

R.note("Suppose the check is widened from `the column beside the number` to `any formula in any")
R.note("string, against the arithmetic of the section it sits in`.  That is the loosest form that")
R.note("could still be called a check.  It does not reach this exhibit, and the reason is")
R.note("arithmetic rather than engineering.")
R.line()

wrong_label = "(1-c)(a+b)"
right_label = "0.9399 (a+b)"
R.line("     label            | numeric literals it names")
R.line("    ------------------+--------------------------")
R.line("    %-17s | %s" % (wrong_label, L.label_literals(wrong_label)))
R.line("    %-17s | %s" % (right_label, L.label_literals(right_label)))
R.line()

pre_src = L.show(PRE, L.EXHIBIT_B)
pre_tree = ast.parse(pre_src)
sec_lits = set()
for node in ast.walk(pre_tree):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
            and not isinstance(node.value, bool) and getattr(node, "lineno", 0) >= 185:
        sec_lits.add(float(node.value))
R.line("   the s1.6 section's own numeric literals (lineno >= 185, PRE): %s"
       % sorted(sec_lits))
R.verdict(1.0 in sec_lits,
          "1 IS ONE OF THEM -- so `(1-c)` is fully covered by the section's arithmetic",
          "the literal rule returns AGREE on the WRONG label, and it is right to: nothing about "
          "the literal 1 distinguishes a coefficient from a loop bound")

py = L.tracked_py(PIN)
SRC = L.show_many(PIN, py)
with_one, arms = 0, 0
for p in py:
    if not p.startswith("code/"):
        continue
    arms += 1
    try:
        tree = ast.parse(SRC[p])
    except (SyntaxError, L.Refused):
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) \
                and not isinstance(node.value, bool) and float(node.value) == 1.0:
            with_one += 1
            break
R.line()
R.line("   tracked .py under code/ at AS_OF                      : %d" % arms)
R.line("   ... containing the numeric literal 1 somewhere        : %d  (%.1f%%)"
       % (with_one, 100.0 * with_one / arms))
R.verdict(with_one > 0.9 * arms,
          "AND THAT IS NOT A PROPERTY OF THIS SECTION: %.1f%% of the estate's arms compute with 1"
          % (100.0 * with_one / arms),
          "so a literal-agreement rule is blind to every mislabel whose only literal is 1 -- and "
          "`(1-c)`, `1/n`, `n-1` and `1 - eps` are how coefficients are spelled")

# =============================================================================================
R.banner("m2.3  EXHIBIT A -- THE MISLABELLED COMPLEXITY.  Nothing syntactic reaches it, and the "
         "proxy fails in the direction that LICENSES the wrong claim")

R.note("`feasible_merges` was documented `O(a*b)`; as written it rescans the remaining opposite")
R.note("side at every step, so it is `O(a*b*(a+b))`.  The COST CLAIM survives unchanged --")
R.note("polynomial is what mg-99f4's Q2 asks and enumerating L(P) is what it forbids -- so this is")
R.note("a documentation defect with no consequence for the result, which is exactly why nothing")
R.note("would have caught it.")
R.line()


def claim_and_depth(src):
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "feasible_merges":
            doc = ast.get_docstring(node) or ""
            m = L.BIGO.search(doc)
            if not m:
                raise L.Refused("feasible_merges carries no O(...) claim at this revision")
            return m.group(0), L.claimed_rank(m.group(1)), L.loop_depth(node)
    raise L.Refused("feasible_merges not found -- the exhibit moved and this arm must not answer")


pre_claim, pre_rank, pre_depth = claim_and_depth(L.show(PRE, L.EXHIBIT_A))
pin_claim, pin_rank, pin_depth = claim_and_depth(L.show(PIN, L.EXHIBIT_A))

R.line("     revision | docstring claim   | factors claimed | loop-nesting depth the proxy sees")
R.line("    ----------+-------------------+-----------------+----------------------------------")
R.line("    %-9s | %-17s | %15d | %d" % ("PRE", pre_claim, pre_rank, pre_depth))
R.line("    %-9s | %-17s | %15d | %d" % ("AS_OF", pin_claim, pin_rank, pin_depth))
R.line()

R.verdict(pre_claim == "O(a*b)" and pin_claim == "O(a*b*(a+b))",
          "the two claims are read out of the tree and differ exactly as the commit says",
          "%s -> %s, neither re-typed here" % (pre_claim, pin_claim))
R.verdict(pre_depth == pin_depth,
          "THE BODY DID NOT CHANGE -- the proxy sees the SAME %d at both revisions" % pre_depth,
          "the correction was to the docstring alone, so any instrument reading the body returns "
          "one number for two different claims and cannot be a check on either")
R.verdict(pre_depth != pre_rank and pre_depth != pin_rank,
          "the proxy matches NEITHER the wrong claim (%d) nor the right one (%d)"
          % (pre_rank, pin_rank),
          "so it does not adjudicate; it disagrees with both")
R.verdict(pre_depth < pre_rank,
          "AND IT FAILS IN THE DANGEROUS DIRECTION: %d < %d" % (pre_depth, pre_rank),
          "a check reading `the body has fewer loops than the docstring claims` treats the claim "
          "as CONSERVATIVE and passes it -- so applied as a lint the proxy would have LICENSED "
          "`O(a*b)` rather than flagged it")

R.line()
R.note("THE MECHANISM IS NOT A WEAK REGEX AND WIDENING IT DOES NOT HELP.  The two dimensions of")
R.note("this DP are in the MEMO KEY `(i, j)` and in the recursion, not in any `for`; the one")
R.note("comprehension a walker CAN see -- `any((v, e) in rel for v in right[j:])` -- is the")
R.note("rescan that the corrected claim's THIRD factor is about.  So the proxy sees exactly the")
R.note("factor that was MISSING from the wrong claim and still cannot report it, because it has")
R.note("no way to know the other two exist.  Cost is a property of the recursion's state space")
R.note("and a syntactic depth is not a bound on it in either direction.")

# =============================================================================================
R.banner("m2.4  THE ANSWER TO THE CARRY-FORWARD, IN ONE TABLE")

rows = [
    ("B  the (1-c)(a+b) note", "a prose sentence", "NO",
     "no positional link to any expression; its only literal is 1"),
    ("A  feasible_merges O(a*b)", "a docstring", "NO",
     "the claim is about a recursion's state space, not its loops"),
    ("-- the column check that IS", "a column header", "YES",
     "the value it labels is an expression in the same scope"),
]
R.line("     exhibit                    | where the label lives | check reaches it? | why")
R.line("    ----------------------------+-----------------------+-------------------+-----------")
for a, b, c, d in rows:
    R.line("    %-27s | %-21s | %-17s | %s" % (a, b, c, d))
R.line()
R.note("NEITHER OF THE TICKET'S TWO EXHIBITS IS A MISLABELLED COLUMN.  A label-vs-computation")
R.note("check IS buildable -- m1 builds it and measures how far it reaches -- but the class it")
R.note("reaches does not contain either instance the ticket was filed from.  The estate's own")
R.note("sentence, `a mislabelled column that prints the right number`, names a shape that is")
R.note("checkable; what it was written about is two shapes that are not.")
R.note("⚠️ THIS IS THE HONEST FORM OF THE CARRY-FORWARD'S OWN SECOND OPTION, and the ticket named")
R.note("it in advance: the class is irreducibly a reading problem, and saying so is the")
R.note("deliverable.  What this directory adds is that it is a reading problem FOR A REASON that")
R.note("can be stated and measured, rather than because nobody has tried.")

sys.stdout.write(R.done(os.path.join(HERE, "out_m2_exhibits.txt")))
raise SystemExit(1 if R.bad else 0)
