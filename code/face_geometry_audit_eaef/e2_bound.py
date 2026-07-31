"""mg-eaef e2 -- DOES THE STATED BOUND MATCH WHAT DELETION ACTUALLY REACHES?

mg-f7e1's second move is mg-0b07's option 2: state the instrument's limit as a
count rather than a promise.  The transcript prints

    DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS AND NO
    FURTHER

over a five-column census of two files, and the argument for doing it that way
is exactly right: a limit that is inferred from a green run is read as reaching
further than it does.

A BOUND STATED TOO GENEROUSLY IS WORSE THAN NO BOUND, because it is read as a
guarantee, and this arc has already printed two extents wider than their code.
So the census is re-derived here from the tree with different code, and each
column is then compared against THE SET OF OPERANDS THE SWEEP ACTUALLY DELETES
-- which is not the same question as how many operands exist.

Two of the five columns are checked against the sweep's own behaviour:

  * `operands` is documented in the subject's kernel as "operands the sweep can
    delete" and appears in the landing document under the header "operands the
    sweep deletes".  It is printed for TWO files.  The sweep visits one.
  * `operands` + `compounds` is offered as the decomposition of a deciding
    condition into what deletion reaches and what it cannot.  Every explicit
    boolean operand is supposed to be on the reachable side of that line.

Nothing here is read out of the subject's code as an authority: the census is
recomputed, and the two sentences it is compared against are read out of the
COMMITTED TRANSCRIPT, which is what a reader of that transcript has.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kern_eaef import (                                         # noqa: E402
    BAR, INSTR, boolean_operands, claim, compound_form,
    deciding_conditions, expr_nodes, finding, head, report, source_at,
)

TRANSCRIPT = os.path.join(INSTR, "out_d2_deletion.txt")

# The two sentences the subject's transcript prints about posets.py, quoted so
# the comparison below is between two things a reader actually sees.
NOT_SWEPT = ("NOT SWEPT, and named rather than left out silently: posets.py "
             "has 2 more")
BOUND_LINE = "DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS"


def census(src):
    conds = deciding_conditions(src)
    import ast
    boolean = [c for c in conds if isinstance(c[2], ast.BoolOp)]
    top = [o for o in boolean_operands(src) if not o.nested]
    compounds = []
    for func, kind, cond in conds:
        for node in ast.walk(cond):
            form = compound_form(node)
            if form not in (None, "or", "and"):
                compounds.append((func, kind, form, node))
    return (len(conds), len(boolean), len(top), len(compounds),
            expr_nodes(src))


def main():
    print(BAR)
    print("mg-eaef e2 -- the stated bound against what deletion reaches")
    print(BAR)
    print("\nPREDICTIONS, registered before these runs (PREDICTIONS.md e2):")
    print("   e2.1  the five-column census re-derives exactly: "
          "face_complex.py 73/5/11/11/1002, posets.py 6/1/2/1/55")
    print("   e2.2  the `operands` column reads 2 for posets.py and the sweep "
          "deletes 0 there")
    print("   e2.3  4 explicit boolean operands are in NEITHER the `operands` "
          "column nor\n         the `compounds` column\n")

    fc = source_at(None, "face_complex.py")
    ps = source_at(None, "posets.py")
    text = open(TRANSCRIPT).read()

    head("1.  THE CENSUS, RE-DERIVED")
    print("   %-18s %-6s %-5s %-9s %-10s %s"
          % ("file", "conds", "bool", "operands", "compounds", "expr nodes"))
    fcc, psc = census(fc), census(ps)
    for name, c in (("face_complex.py", fcc), ("posets.py", psc)):
        print("   %-18s %-6d %-5d %-9d %-10d %d" % ((name,) + c))
    claim("THE CENSUS RE-DERIVES FROM DIFFERENT CODE: face_complex.py "
          "%d/%d/%d/%d/%d and posets.py %d/%d/%d/%d/%d, which is what the "
          "subject prints for both files" % (fcc + psc),
          fcc == (73, 5, 11, 11, 1002) and psc == (6, 1, 2, 1, 55),
          "either file changing, or the two enumerators disagreeing -- at "
          "which point everything below is about a number this audit cannot "
          "reproduce and has to say so before using it")
    for line in (BOUND_LINE, NOT_SWEPT):
        claim("THE SENTENCE THIS SECTION IS ABOUT IS IN THE COMMITTED "
              "TRANSCRIPT, exactly once: %r" % line[:64],
              text.count(line) == 1,
              "the transcript being regenerated with that sentence reworded, "
              "which would make the comparison below about a document nobody "
              "has",
              "occurrences: %d" % text.count(line))

    head("2.  THE `operands` COLUMN AGAINST THE OPERANDS THE SWEEP DELETES")
    print("The column's own definition, from the subject's kernel docstring, "
          "is `operands the\nsweep can delete`; the landing document heads it "
          "`operands the sweep deletes`.  It\nis printed on two rows.  Twenty "
          "lines earlier the same transcript prints:\n")
    for ln in text.splitlines():
        if NOT_SWEPT in ln or "deciding clause(s) (_is_transitively" in ln:
            print("      " + ln.strip())
    print("\nSo the sweep's population is the clauses of face_complex.py and "
          "posets.py's two\nare outside it, said plainly and in the right "
          "place.  The census row for\nposets.py is the same fact counted the "
          "other way round, and it is the row a\nreader consults for the "
          "instrument's reach.\n")
    swept_files = ["face_complex.py"]
    print("   %-18s %-24s %-24s" % ("file", "`operands` column says",
                                    "the sweep deletes"))
    for name, c in (("face_complex.py", fcc), ("posets.py", psc)):
        n = c[2] if name in swept_files else 0
        print("   %-18s %-24d %-24d %s"
              % (name, c[2], n, "" if c[2] == n else "  <-- disagree"))
    # THE FIRST WRITING OF THIS CLAIM WAS BROKEN AND IS KEPT IN PREDICTIONS.md:
    # it asserted that `_is_transitively_closed` occurs ONCE in the transcript.
    # It occurs three times -- twice in the NOT SWEPT sentence, which names both
    # its clauses, and once in the compounds table.  The claim was about the
    # SWEEP's rows and was written as a count over the whole file, which is the
    # same substitution of a convenient population for the intended one that
    # this audit is looking for.  Restated over the row it is about:
    swept = ""
    for ln in text.splitlines():
        if "THE CLAUSE SWEEP RAN ON THE ENUMERATED POPULATION" in ln:
            swept = text.splitlines()[text.splitlines().index(ln) + 1]
    claim("THE SWEEP REALLY DOES NOT VISIT posets.py: the line that enumerates "
          "what it swept lists 11 clauses and names no posets.py function",
          "_is_transitively_closed" not in swept and swept.count(";") == 10,
          "a row for `_is_transitively_closed` appearing in the sweep, which "
          "would close this finding by making the census row true",
          "the enumeration line names: %s"
          % "; ".join(sorted({p.strip().split()[0]
                              for p in swept.split(";") if p.strip()})))
    finding("E4", "THE BOUND IS STATED WIDER THAN THE SWEEP ON ONE OF ITS TWO "
            "ROWS: the census prints `2` under `operands` for posets.py -- a "
            "column the kernel documents as `operands the sweep can delete` "
            "and the landing document heads `operands the sweep deletes` -- "
            "and the sweep deletes 0 operands in posets.py.  The transcript "
            "says so itself twenty lines above, so the two statements are in "
            "one document and disagree; the qualifier that travels with the "
            "claim covers only the `compounds` column (`posets.py adds 1 more, "
            "which no claim here covers`) and not this one.",
            "the population is the 2-row census table printed under THE BOUND "
            "OF THIS INSTRUMENT; 1 of its 2 rows is a file the sweep visits")

    head("3.  THE TWO COLUMNS AGAINST THE OPERANDS THAT EXIST")
    print("`operands` and `compounds` are offered as the two sides of one "
          "line: what deletion\nreaches, and what it cannot reach into.  An "
          "EXPLICIT boolean operand is on the\nreachable side by the bound's "
          "own words.  Below, every operand of every `or`/`and`\nanywhere "
          "inside a deciding condition is enumerated and assigned to a "
          "column.\n")
    for name, src in (("face_complex.py", fc), ("posets.py", ps)):
        ops = boolean_operands(src)
        top = [o for o in ops if not o.nested]
        nested = [o for o in ops if o.nested]
        print("   %s: %d explicit boolean operand(s) in deciding conditions"
              % (name, len(ops)))
        print("      counted by `operands`  : %d" % len(top))
        print("      counted by `compounds` : 0  -- the form filter skips "
              "`or` and `and` by name")
        print("      counted by NEITHER     : %d" % len(nested))
        for o in nested:
            print("         %-22s %-6s c%d/%d  %s"
                  % (o.func, o.kind, o.index + 1, o.total,
                     " ".join((o.source or "").split())[:44]))
    fc_nested = [o for o in boolean_operands(fc) if o.nested]
    claim("THE GAP IS IN THE FILTER AND NOT IN THE WALK: the compound "
          "enumerator walks every node of every deciding condition, so it SEES "
          "each nested `and`, and then drops it because its form is named "
          "`and` -- the same two `BoolOp`s this audit finds are inside the "
          "walk it performs",
          len(fc_nested) == 4 and all(o.op in ("or", "and")
                                      for o in fc_nested),
          "the nested operators being of some other form, which would make "
          "this a gap in the form list rather than in the exclusion",
          "; ".join("%s c%d spelled with `%s`" % (o.func, o.index + 1, o.op)
                    for o in fc_nested))
    finding("E5", "THE BOUND NAMES A FLOOR IT DOES NOT REACH: "
            "`DELETION ESTABLISHES COVERAGE DOWN TO EXPLICIT BOOLEAN OPERANDS "
            "AND NO FURTHER` is read as `every explicit boolean operand is on "
            "the reached side`, and 4 of the 15 explicit boolean operands in "
            "face_complex.py's deciding conditions are on neither side of the "
            "census -- not in `operands` (11), not in `compounds` (11).  They "
            "are excluded by name: the compound filter skips the forms `or` "
            "and `and`, on the assumption that anything spelled with an "
            "operator is deletable, and an operator nested under a "
            "comprehension or a quantifier is not.  e1 deletes all 4 and all 4 "
            "change the artifact.",
            "the population is the 15 operands of the 7 `or`/`and` operators "
            "inside face_complex.py's 73 deciding conditions")
    return report()


if __name__ == "__main__":
    sys.exit(main())
