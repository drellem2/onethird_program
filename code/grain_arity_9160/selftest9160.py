"""mg-9160 / SELFTEST -- forced arms for every rule this tree writes.

Every case below is an arm that CAN fail.  Two of them are negative controls
whose only job is to fire if the correction is wrong: `E1` (is `BOTH`
reachable, without which the arity floor is the wrong number) and `AXES` (is
the six-axis graph really 2-colourable, without which the headline is empty).

Exit code = number of failing cases.
"""

import sys

import lib9160 as G

BAD = 0


def case(name, got, want):
    global BAD
    ok = got == want
    if not ok:
        BAD += 1
    print("  %-6s %-58s %s"
          % ("ok" if ok else "*FAIL", name,
             "" if ok else "got %r want %r" % (got, want)))


G.bar("mg-9160 / SELFTEST")
print("HEAD: %s" % G.head())

print()
print("-- the arity floor: arithmetic, checked against hand-computed values --")
case("min_collapse(43,4) = 3*C(11,2)+C(10,2)", G.min_collapse(43, 4), 210)
case("min_collapse(400,4) = 4*C(100,2)", G.min_collapse(400, 4), 19800)
case("min_collapse(43,1) = C(43,2) -- one value collapses everything",
     G.min_collapse(43, 1), 903)
case("min_collapse(43,43) = 0 -- one value per word collapses nothing",
     G.min_collapse(43, 43), 0)
case("min_collapse(43,3) = 287 -- the E1 world where BOTH is unreachable",
     G.min_collapse(43, 3), 287)

print()
print("-- E1's NEGATIVE CONTROL: is the fourth cell reachable at all? --")
print("   If no string classifies BOTH, `_classify` is 3-valued in practice")
print("   and the floor above is 287, not 210.  This arm decides it.")
case("`rows executed` classifies BOTH under the SUBJECT classifier",
     G.A._classify("rows executed"), "BOTH")
case("a string in neither list classifies NONE",
     G.A._classify("zzzz"), "NONE")

print()
print("-- collapse(): counted by RUNNING, so it can disagree with A1c --")
case("a 2-block partition of 4 words collapses 2 pairs",
     G.collapse(G.two_test({"a", "b"}, {"c", "d"}),
                ["a", "b", "c", "d"]), (6, 4, 2))
case("an all-distinct classifier collapses 0",
     G.collapse(lambda w: w, ["a", "b", "c", "d"]), (6, 6, 0))

print()
print("-- two_test(): EXACTLY `_classify`'s form, four cells all reachable --")
f = G.two_test({"x", "z"}, {"y", "z"})
case("two_test EXECUTION cell", f("x"), "EXECUTION")
case("two_test SITE cell", f("y"), "SITE")
case("two_test BOTH cell", f("z"), "BOTH")
case("two_test NONE cell", f("q"), "NONE")

print()
print("-- AXES' NEGATIVE CONTROL: a graph that is NOT 2-colourable --")
print("   A triangle needs three colours.  If `chromatic` returned 2 here the")
print("   headline `two colours suffice` would be worthless.")
case("triangle needs 3 colours",
     G.chromatic(["a", "b", "c"],
                 [("a", "b"), ("b", "c"), ("a", "c")])[0], 3)
case("a single edge needs 2",
     G.chromatic(["a", "b"], [("a", "b")])[0], 2)
case("no edges need 1", G.chromatic(["a", "b"], [])[0], 1)

print()
print("-- attribute(): the disagreement with the parent's `embedded_counts` --")
lab = "973ca61 OUTSIDE rows   ROWS  10  SITES   9  GAP"
sp = lab.index("10"), lab.index("10") + 2
case("both neighbours are words -> AMBIGUOUS", G.attribute(lab, sp)[2],
     "AMBIGUOUS")
case("...and the LEFT neighbour is `rows`", G.attribute(lab, sp)[0], "rows")
case("...where the parent's rule takes `sites`",
     G.B.embedded_counts(lab)[0], (10, "sites"))
case("a trailing integer with no word after it -> PREV",
     G.attribute("rows  7", (6, 7))[2], "PREV")

print()
print("-- column_shape(): the tie-break, on the two shapes it separates --")
case("a strictly alternating table row is NOUN-VALUE",
     G.column_shape("973ca61 ALL rows   ROWS  49  SITES  47  GAP", [2]),
     "NOUN-VALUE")
case("prose with an embedded count is VALUE-NOUN",
     G.column_shape("...ROWS outside it, across 10 distinct basenames", [14]),
     "VALUE-NOUN")

print()
print("-- grain_open(): open value set, and the failure names the label --")
case("the noun is returned, de-pluralised",
     G.grain_open("...count ROWS in them"), ("WORD", "row"))
case("a label with no noun names itself rather than returning a symbol",
     G.grain_open("...  the  of  in")[0], "NO-NOUN")

print()
print("-- verdict(): the THIRD value, which no per-word symbol can carry --")
case("an adjudicated synonym pair", G.verdict("steps", "iterations")[0], "SAME")
case("an adjudicated distinct pair", G.verdict("rows", "sites")[0],
     "DIFFERENT")
case("a pair nobody has adjudicated", G.verdict("poset", "antichain")[0],
     "UNADJUDICATED")
case("the same noun, pluralised, is one grain",
     G.verdict("row", "rows")[0], "SAME")

print()
print("-- MY OWN MIRROR DEFECT, asserted rather than hidden (P4) --")
print("   The open-set classifier SPLITS the two pairs A1f adjudicated SAME.")
print("   This arm asserts that it does.  If it ever stops, I have special-")
print("   cased the words and the ratio in s4 is a fact about my hand list.")
case("grain_open splits `steps` from `iterations`",
     G.grain_open("...steps")[1] != G.grain_open("...iterations")[1], True)
case("grain_open splits `commands` from `invocations`",
     G.grain_open("...commands")[1] != G.grain_open("...invocations")[1], True)

print()
print("-- parent_corpus(): two refs, not one --")
pc = G.parent_corpus()
case("the reconstruction carries mg-03d1's own 7 transcripts",
     sum(1 for p, r in pc if p.startswith(G.PARENT + "/")), 7)
case("...and every one of them is read at the PUBLISHING commit",
     {r for p, r in pc if p.startswith(G.PARENT + "/")}, {G.PARENT_PUB})

print()
print("SELFTEST TOTAL BAD: %d" % BAD)
sys.exit(BAD)
