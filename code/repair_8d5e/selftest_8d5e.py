"""selftest_8d5e.py -- the instrument, before any finding rests on it.

Every assertion here is about lib8d5e, not about mg-69d1 or mg-e34a.  If this
exits non-zero nothing in r1-r4 may be believed until the failure is
understood: a walk that misses agrees with every count, and a scoring rule
that labels every site the same way says nothing while looking like a table.

The ones that carry the weight, and why:

  * MY DECIDING-CONDITION WALK AGAINST THE SHIPPED ONE, SPAN FOR SPAN.  A-2 is
    a SUBTRACTION between two populations.  If the narrow side is taken from
    the thing under test, the difference is whatever that thing says it is.
    So both walks are written here and the narrow one is required to agree
    with `kern5f9a.boolean_operands` operand for operand -- not count for
    count, which is what let 2 match 0 in mg-eaef's E4.

  * THE SCORING RULE IS mg-2c77's AND NOT A WIDER ONE.  Asserted on
    constructed inputs, including the case that matters most: a site carrying
    only the HYPHENATED `deciding-condition` scores UNQUALIFIED, because that
    is what mg-2c77's rule does to it.  A repair that widened the rule to
    accept the hyphen would close the finding by moving the ruler.

  * AND AGAINST mg-2c77's OWN COMMITTED TABLE.  The rule is run at the
    revision where that transcript was committed and required to return the
    same 15 in-`d01ff32` sites, path and line.  Two rules that agree on
    constructed inputs can still disagree on a tree.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "face_geometry_instr_5f9a"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "branching_audit_e34a"))

import lib8d5e as L                                            # noqa: E402
import kern5f9a as K                                           # noqa: E402
import libe34a as E                                            # noqa: E402

N, BAD = [0], []


def ok(cond, what):
    N[0] += 1
    if not cond:
        BAD.append(what)
    print("   %-4s %s" % ("ok" if cond else "FAIL", what))


print("=" * 74)
print("SELFTEST  lib8d5e -- the apparatus for mg-8d5e")
print("=" * 74)

# ---------------------------------------------------------------------------
print()
L.rule("(1) THE TWO OPERAND WALKS, AND THE NARROW ONE AGAINST THE SHIPPED ONE")

for fname in L.CENSUS_FILES:
    src = L.census_source(fname)
    wide = L.all_boolean_operands(src, fname)
    narrow = L.deciding_boolean_operands(src, fname)
    shipped = K.boolean_operands(src, fname)
    mine_spans = sorted(o["span"] for o in narrow)
    ship_spans = sorted(L.span(v)
                        for func, kind, cond in K.deciding_conditions(src)
                        for node in __import__("ast").walk(cond)
                        if isinstance(node, __import__("ast").BoolOp)
                        for v in node.values)
    ok(mine_spans == ship_spans,
       "%s: my deciding-condition walk and the SHIPPED kern5f9a walk agree "
       "SPAN FOR SPAN (%d operands)" % (fname, len(mine_spans)))
    ok(len(shipped) == len(narrow),
       "%s: and they agree on the count too (%d)" % (fname, len(narrow)))
    ok(set(o["span"] for o in narrow) <= set(o["span"] for o in wide),
       "%s: every deciding-condition operand is also in the unrestricted "
       "walk -- the narrow population is a SUBSET and the subtraction is "
       "well defined" % fname)
    ok(len(wide) >= len(narrow) and len(narrow) > 0,
       "%s: the unrestricted walk (%d) is at least the restricted one (%d) "
       "and neither is empty" % (fname, len(wide), len(narrow)))

_toy = ("def f(a, b, c):\n"
        "    while a and b:\n"                 # not a deciding condition
        "        c = a or b\n"                 # not a deciding condition
        "    if a and b:\n"                    # deciding: its body returns
        "        return c or a\n"              # deciding: a return value
        "    return 0\n")
ok(len(L.all_boolean_operands(_toy, "toy.py")) == 8,
   "on a constructed file the unrestricted walk finds all 8 operands, "
   "including the `while` and the assignment")
ok(len(L.deciding_boolean_operands(_toy, "toy.py")) == 4,
   "and the deciding-condition walk finds 4 -- the `while` and the "
   "assignment are outside every deciding condition")
ok(len(L.deciding_boolean_operands(_toy, "toy.py"))
   == len(K.boolean_operands(_toy, "toy.py")),
   "NON-VACUITY: the shipped walker agrees on that constructed file too, so "
   "the two walks differ by the restriction and not by a parsing accident")

# ---------------------------------------------------------------------------
print()
L.rule("(2) THE SCORING RULE, ON SITES CONSTRUCTED HERE")

_tmp = tempfile.mkdtemp(prefix="mg8d5e-rule-")
try:
    def _site(name, body):
        with open(os.path.join(_tmp, name), "w") as fh:
            fh.write(body)
        for i, line in enumerate(body.splitlines(), 1):
            if L.TERM in line:
                return L.disposition(name, i, repo=_tmp)
        raise AssertionError("the constructed site does not contain the term")

    # The bodies below are CONSTRUCTED FIXTURES, not claims about this
    # repair: each carries the term with the words `deciding condition` at a
    # measured distance, so the window's width can be tested at its edge.
    ok(_site("bare.md", "prose\nevery explicit boolean operand is covered\n"
                        "more prose\n") == "*** census, UNQUALIFIED",
       "a site with the bare term and nothing near it scores UNQUALIFIED")
    ok(_site("near.md", "a\nb\nc\nevery explicit boolean operand\n"
                        "inside a deciding condition\n")
       == "census, QUALIFIED",
       "the qualifier one line away scores QUALIFIED")
    ok(_site("edge3.md", "every explicit boolean operand\na\nb\n"
                         "inside a deciding condition\n")
       == "census, QUALIFIED",
       "the qualifier exactly 3 lines away is still inside the window")
    ok(_site("edge4.md", "every explicit boolean operand\na\nb\nc\n"
                         "inside a deciding condition\n")
       == "*** census, UNQUALIFIED",
       "and 4 lines away is OUTSIDE it -- the window is the width it says")
    ok(_site("hyph.md", "every explicit boolean operand\n"
                        "with the deciding-condition qualifier\n")
       == "*** census, UNQUALIFIED",
       "THE RULE IS mg-2c77's: a site carrying only the HYPHENATED "
       "`deciding-condition` scores UNQUALIFIED, so this repair cannot close "
       "the finding by widening the ruler")
    ok(_site("quote.md", "the bound said explicit boolean operands\n"
                         "AND NO FURTHER, which is wider than the sweep\n")
       == "quotes the wide BOUND, not the census",
       "a site quoting the wide BOUND is not scored as an assertion of the "
       "census")
    ok(_site("both.md", "every explicit boolean operand\n"
                        "inside a deciding condition\nAND NO FURTHER\n")
       == "quotes the wide BOUND, not the census",
       "and the quotation marker WINS over the qualifier, as it does in "
       "mg-2c77's rule -- the precedence is the same precedence")
finally:
    import shutil
    shutil.rmtree(_tmp, ignore_errors=True)

# ---------------------------------------------------------------------------
print()
L.rule("(3) THE RULE AGAINST mg-2c77'S OWN COMMITTED TABLE")
print("   Two rules that agree on constructed inputs can still disagree on a")
print("   tree.  Scored at the revision where that transcript was committed,")
print("   because a transcript can only be reproduced at the revision it is")
print("   about -- which is the whole of A-1 stated as a method.")
print()

_derived_q3 = L.last_touching(L.Q3_TRANSCRIPT_REL)
ok(_derived_q3 == L.Q3_REV_PIN,
   "Q3_REV_PIN %s is the last commit touching %s -- the pin and the "
   "derivation agree" % (L.Q3_REV_PIN[:8], L.Q3_TRANSCRIPT_REL.split("/")[-1]))

_touched = L.files_of(L.D01FF32_PIN)
_scored = L.score_all(rev=L.Q3_REV_PIN)
_unq_then = sorted((p, n) for p, n, d in _scored
                   if d.startswith("***") and p in _touched)
_transcript = L.git_show(L.Q3_REV_PIN, L.Q3_TRANSCRIPT_REL)
_claimed = []
for _line in _transcript.splitlines():
    if "The claim is written without the deciding-condition qualifier at" \
            in _line:
        _tail = _line.split("touched: ", 1)[1]
        for _item in _tail.split(".  This is")[0].split(", "):
            _p, _, _n = _item.strip().rpartition(":")
            if _p:
                _claimed.append((_p, _n))
_claimed = sorted(_claimed)
ok(bool(_claimed),
   "mg-2c77's finding text names its in-d01ff32 sites and they were parsed "
   "out of the committed transcript (%d named)" % len(_claimed))
ok(_unq_then == _claimed,
   "MY RULE REPRODUCES mg-2c77's %d in-d01ff32 unqualified sites at %s, path "
   "and line -- %d matched, %d only mine, %d only its"
   % (len(_claimed), L.Q3_REV_PIN[:8], len(set(_unq_then) & set(_claimed)),
      len(set(_unq_then) - set(_claimed)), len(set(_claimed) - set(_unq_then))))
ok(len(set(d for _p, _n, d in _scored)) >= 2,
   "NON-VACUITY: the rule returned more than one label over that tree (%d "
   "distinct), so it is not stamping every site the same way"
   % len(set(d for _p, _n, d in _scored)))

# ---------------------------------------------------------------------------
print()
L.rule("(4) THE ANCHORS THIS REPAIR INSTALLED, READ BACK OUT OF libe34a")
ok(not E.ANCHOR_DRIFT,
   "libe34a reports 0 anchor disagreements (%s)"
   % ("; ".join(E.ANCHOR_DRIFT) or "derived == pinned, four for four"))
for _label, _got, _pin, _verdict in E.anchor_rows():
    ok(_got == _pin, "%s: derived %s == pinned %s"
       % (_label.strip(), _got[:8], _pin[:8]))
ok(E.first_introducing(E.G1_REL, E.MARK_76CC) != E.last_touching(E.G1_REL),
   "NON-VACUITY: on this tree the property anchor (%s) and the file-history "
   "anchor (%s) are DIFFERENT commits, so the distinction is one this tree "
   "exhibits rather than one that is merely stated"
   % (E.first_introducing(E.G1_REL, E.MARK_76CC)[:8],
      E.last_touching(E.G1_REL)[:8]))
ok(E.first_introducing(E.G1_REL, "a marker in no revision of this file")
   is None,
   "first_introducing returns None for a marker in no commit rather than "
   "falling back to the file's creation")

# ---------------------------------------------------------------------------
print()
L.rule("(5) THE TRANSCRIPT READERS AND THE BENDS")
_syn = "\n".join([
    "prose",
    "      FINDING: quoted from a nested run at six spaces",
    "SELF-ERRORS: 0, population: things",
    "FINDINGS: 2, population: other things",
    "   FINDING: the first one",
    "   FINDING: the second one",
    "TOTAL BAD: 2",
])
ok(L.findings_of(_syn) == ["the first one", "the second one"],
   "the finding reader counts 2 -- the six-space nested quote is NOT one")
ok(L.trailer_counts(_syn) == (0, 2),
   "the trailer reader reads (0, 2) off the trailer lines")
ok(L.normalise_revs("moved from 4755d029 to d01ff32d")
   == L.normalise_revs("moved from e006581c to e5787e11"),
   "normalise_revs makes two findings that differ only in revisions equal -- "
   "a revision that moved is not a finding that changed")
ok(L.normalise_revs("names c1_branching.py") != L.normalise_revs("names x.py"),
   "and it does NOT make two findings that differ in a filename equal")
try:
    L.replace_once("aXa", "a", "b")
    ok(False, "replace_once REFUSES on many occurrences")
except ValueError:
    ok(True, "replace_once REFUSES on many occurrences")
try:
    L.replace_once("aaa", "z", "b")
    ok(False, "replace_once REFUSES on zero occurrences")
except ValueError:
    ok(True, "replace_once REFUSES on zero occurrences")

print()
print("-" * 74)
print("SELFTEST: %d assertions, %d failed" % (N[0], len(BAD)))
for x in BAD:
    print("   FAILED: %s" % x)
sys.exit(1 if BAD else 0)
