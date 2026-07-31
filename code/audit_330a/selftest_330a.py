"""selftest_330a.py -- the assertions this audit's own instrument rests on.

Every derivation written fresh in lib330a is checked here against the shipped
one it is meant to be independent of, and every scoring rule is checked
against a CONSTRUCTED input whose answer is known before the rule runs.

A rule that has only ever been run on the tree it is about has never been
seen to return its other answer.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "branching_audit_e34a"))

import lib330a as L

FAILED = []
N = [0]


def ok(cond, msg):
    N[0] += 1
    if cond:
        print("   ok   %s" % msg)
    else:
        print("   FAIL %s" % msg)
        FAILED.append(msg)


L.banner("SELFTEST-330A", "THE INSTRUMENT, BEFORE ANYTHING RESTS ON IT")

L.rule("(a) the repo, and the two revisions this audit is about")

ok(os.path.isdir(os.path.join(L.REPO, ".git"))
   or os.path.exists(os.path.join(L.REPO, ".git")),
   "REPO resolves to a git repository")
ok(L.resolve(L.REPAIR_8D5E) == L.REPAIR_8D5E,
   "the repair under audit dfa263c resolves")
ok(L.is_ancestor(L.REPAIR_8D5E, "HEAD"),
   "dfa263c is an ancestor of this HEAD -- the repair is in this tree")
ok(L.resolve(L.REPAIR_8D5E + "^") == L.resolve(L.PRE_8D5E),
   "PRE_8D5E is exactly dfa263c's first parent -- the control revision is "
   "derived from the subject, not written down twice")
ok(L.resolve(L.D01FF32) == L.D01FF32,
   "d01ff32 -- the repair mg-2c77 audited -- resolves")

L.rule("(b) my derivations against the shipped ones")

# libe34a is IMPORTED here and only here, to compare implementations.  No
# script of this audit takes a number from it.
import libe34a as E                                          # noqa: E402

ok(L.my_first_introducing(L.G1_REL, L.MARK_76CC)
   == E.first_introducing(E.G1_REL, E.MARK_76CC),
   "my two-sided first_introducing agrees with libe34a's, written from its "
   "sentence rather than by calling it")
ok(L.my_last_touching(L.G1_REL) == E.last_touching(E.G1_REL),
   "my last_touching agrees with libe34a's")
ok(L.my_nth_touching(L.G1_REL, 1) == E.nth_touching(E.G1_REL, 1),
   "my nth_touching agrees with libe34a's")
ok(L.G1_REL == E.G1_REL,
   "and both are about the same path: %s" % L.G1_REL)

L.rule("(c) the anchor taxonomy, on constructed calls whose kind is known "
       "before the classifier runs")

CASES = [
    ('git("log", "-1", "--format=%H", "--", p)', "NEWEST"),
    ('git("log", "--format=%H", "--", p)', "INDEXED"),
    ('git("log", "--reverse", "--format=%H", "--", p)', "OLDEST"),
    ('git("log", "--reverse", "--format=%H", "-S", "def f(", "--", p)',
     "PICKAXE"),
    ('git("log", "--format=%H", "%s..%s" % (a, b), "--", p)', "RANGE"),
    ('git("log", "-1", "--format=%s", "--", p)', None),
    ('git("show", "--name-only", "--format=", r)', None),
    ('git("log", "--format=%H", "--all", "--", p)', "INDEXED"),
    # DEFECT #2 OF THIS INSTRUMENT, KEPT.  `-G` is the regex pickaxe and
    # selects by a property of the content exactly as `-S` does.  The first
    # version of the classifier tested for `-S` only and filed a real `-G`
    # site (repair_8aae.py:499) under INDEXED -- the defect class.  That is
    # A-2's own mistake, a term denoting more than it covers, made inside an
    # audit of A-2.  This row is the one that would have caught it.
    ('git("log", "-G", "pattern", "--format=%H", "--", p)', "PICKAXE"),
]
for src, want in CASES:
    call = ast.parse(src).body[0].value
    got = L.classify_call(L._strings_of(call))
    ok(got == want, "classify %-58s -> %s" % (src, got))

ok(L.classify_call(L._strings_of(
        ast.parse('git("log", "-1", "--format=%H")').body[0].value))
   == "NEWEST-norestrict",
   "a `-1` with NO pathspec is a different kind and is named separately -- "
   "it is an anchor on the branch, not on a file")

L.rule("(d) the operand walks, on a constructed module")

SRC = (
    "def f(a, b, c):\n"
    "    if a and b:\n"
    "        return 1\n"
    "    return c or a\n"
    "\n"
    "def g(x, y):\n"
    "    while x or y:\n"
    "        x = 0\n"
    "    z = x and y\n"
    "    return z\n"
)
allo = L.all_operands(SRC, "constructed.py")
deco = L.deciding_operands(SRC, "constructed.py")
# DEFECT #1 OF THIS INSTRUMENT, KEPT.  This assertion was first written as
# `== 6` with the operands listed beside it as `(a,b / c,a / x,y / x,y)` --
# four PAIRS, which is eight operands.  The walk returned 8 and the selftest
# went red on my own arithmetic before any number of this audit rested on it.
# The expectation was wrong, the walk was right, and the row stays here rather
# than being quietly corrected in place: a selftest that has never gone red on
# its author is a selftest whose red is unmeasured.
ok(len(allo) == 8,
   "all_operands finds 8 on the constructed module -- FOUR BoolOps "
   "(a and b / c or a / x or y / x and y), two operands each -- got %d"
   % len(allo))
ok(len(deco) == 4,
   "deciding_operands finds 4 -- `a and b` guards a return, `c or a` IS a "
   "return; the `while` and the assignment are outside -- got %d" % len(deco))
ok(len(allo) - len(deco) == 4,
   "and the difference is exactly the 4 outside every deciding condition "
   "(the `while` test and the assignment), which is the subtraction A-2 is "
   "about")
ok(len({o["span"] for o in allo}) == len(allo),
   "spans are unique -- the key cannot merge two operands with the same text")

SRC2 = "def h(a, b):\n    return a == b\n"
ok(L.all_operands(SRC2, "x.py") == [],
   "a module with no BoolOp gives 0 operands -- the walk returns its other "
   "answer")

L.rule("(e) the qualifier rule returns BOTH answers, on constructed sites")

Q_YES = ["some prose", "the 17 explicit boolean operands", "inside a "
         "deciding condition of the census's two files"]
Q_NO = ["some prose", "the 17 explicit boolean operands", "in the table"]
Q_HYPH = ["some prose", "the 17 explicit boolean operands",
          "inside a deciding-condition of the census's two files"]

ok(L.score_qualifier(Q_YES, 1) is True,
   "a site with the unhyphenated words within 3 lines scores QUALIFIED")
ok(L.score_qualifier(Q_NO, 1) is False,
   "a site with no qualifier scores UNQUALIFIED")
ok(L.score_qualifier(Q_HYPH, 1) is False,
   "A SITE CARRYING ONLY `deciding-condition` SCORES UNQUALIFIED -- the "
   "ruler is mg-2c77's and this audit cannot close a finding by widening it")
ok(len(L.term_sites("\n".join(Q_YES))) == 1,
   "term_sites finds the one line stating the term")
ok(L.term_sites("nothing here") == [],
   "and none where the term is absent")

L.rule("(f) the sweep parses what it walks")

rows, unparsed = L.sweep_anchor_calls()
ok(not unparsed,
   "every .py under code/ parses: %d unparsed" % len(unparsed))
for rel, why in unparsed:
    print("      UNPARSED %s: %s" % (rel, why))
ok(len(rows) > 0,
   "the sweep is non-empty: %d revision-producing git log call(s)"
   % len(rows))
kinds = sorted({r["kind"] for r in rows})
ok(len(kinds) >= 3,
   "and it returns more than one label over the tree it sweeps: %s"
   % ", ".join(kinds))

helpers = L.sweep_helper_uses()
ok(any(h["what"] == "DEF" for h in helpers),
   "the named-helper sweep finds at least one definition of last_touching / "
   "nth_touching -- a helper hides its flags and a flag sweep alone would "
   "miss it")

L.rule("(g) a clone can be built and committed in")

tree = L.clone_at("HEAD")
try:
    before = L.my_last_touching(L.G1_REL, repo=tree)
    src = L.show_or_empty("HEAD", L.G1_REL, repo=tree)
    ok(bool(src), "g1_provenance.py is readable in the clone")
    new = L.commit_in(tree, L.G1_REL, src + "\n# selftest probe\n",
                      "selftest probe")
    after = L.my_last_touching(L.G1_REL, repo=tree)
    ok(after == new and after != before,
       "a commit in the clone really moves the file's newest-touching "
       "commit -- the mutation reaches git, not only the working tree")
    ok(L.my_first_introducing(L.G1_REL, L.MARK_76CC, repo=tree)
       == L.my_first_introducing(L.G1_REL, L.MARK_76CC),
       "and does NOT move the property derivation -- the instrument can "
       "tell the two apart before any probe rests on it")
finally:
    L.rm_tree(tree)

print("\n" + "-" * 74)
print("SELFTEST-330A: %d assertion(s), %d failed" % (N[0], len(FAILED)))
for m in FAILED:
    print("   FAILED: %s" % m)
print("TOTAL BAD: %d" % len(FAILED))
raise SystemExit(1 if FAILED else 0)
