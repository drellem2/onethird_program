"""selftest_69d1.py -- the instrument, tested against constructed inputs.

Every assertion here is about a function in lib69d1.py or in the two kernel
functions this repair added to kern5f9a.py, evaluated on text this file makes
up.  Nothing here reads the tree for its answer: a self-test that consults the
subject is a second copy of the subject.

WHAT IS TESTED AND WHY EACH ONE EXISTS

  the classifier      an operand nested under a comprehension, an operand at
                      the top level, an operand in an unswept file, and a file
                      with no operands at all -- the four cases the columns
                      exist for.  And the TOTALITY property on a source built
                      to have operands at three depths.
  drop_boolean_operand
                      it must remove the named operand and nothing else, and
                      it must produce parseable source, including the case
                      where one operand remains and the `or` goes with it.
  the bends           each must refuse on zero occurrences and on many; a bend
                      that silently did nothing would let a row say whatever
                      it liked.
  the conspiring pair each half must be a NO-OP by construction: the kernel
                      half adds a name, the c1 half reads it with a default of
                      0.  Tested on strings, so a c1 that stopped importing
                      would be caught here rather than by a row reading
                      IDENTICAL for the wrong reason.
  read_literal        the constants this instrument does NOT copy.
  the grep parser     `path:lineno` and `rev:path:lineno` are different
                      shapes, and a mis-parsed path becomes a site that
                      silently cannot be read back off disk.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..",
    "face_geometry_instr_5f9a")))

import lib69d1 as L                                              # noqa: E402
import kern5f9a as K                                             # noqa: E402

OK, BAD = [], []


def check(name, cond, detail=""):
    (OK if cond else BAD).append(name)
    print("  [%s] %s%s" % ("ok  " if cond else "FAIL", name,
                           ("  -- " + detail) if detail and not cond else ""))


print("=" * 74)
print("selftest_69d1 -- the instrument against constructed inputs")
print("=" * 74)

# ---------------------------------------------------------------------------
# The qualifier is the count's population and not decoration (mg-8d5e, on
# mg-2c77's OPEN 2): the classifier's four columns hold the operands inside a
# deciding condition, not every `and`/`or` in the module.
print("\n-- the classifier: every DECIDING-CONDITION explicit boolean operand,"
      " one named column")
print("   (the population is the operands inside a deciding condition, not"
      " every `and`/`or` in the module)")

SRC_TOP = """
def f(a, b):
    if a == 1 or b == 2:
        return True
    return False
"""

SRC_NESTED = """
def g(xs):
    return [x for x in xs if x > 0 and x < 9]
"""

SRC_BOTH = """
def h(a, xs):
    if a or not a:
        return [x for x in xs if x > 0 and x < 9]
    return all(y == 1 or y == 2 for y in xs)
"""

SRC_NONE = """
def i(a):
    return a
"""

ops_top = K.boolean_operands(SRC_TOP, "top.py")
check("a top-level `or` yields 2 operands, both top",
      len(ops_top) == 2 and all(o.top for o in ops_top),
      "got %r" % [(o.top, o.source) for o in ops_top])

ops_nested = K.boolean_operands(SRC_NESTED, "nested.py")
check("an `and` inside a comprehension yields 2 operands, NEITHER top",
      len(ops_nested) == 2 and not any(o.top for o in ops_nested),
      "got %r" % [(o.top, o.source) for o in ops_nested])
check("...and the sweep's own enumerator finds 0 of them",
      len(K.deciding_clauses(SRC_NESTED)) == 0)
check("...and the compound census does not hold them either -- NEITHER column",
      not any("x > 0" in (c.source or "")
              for c in K.implicit_disjunctions(SRC_NESTED)))

ops_none = K.boolean_operands(SRC_NONE, "none.py")
check("a file with no boolean operator yields 0 operands", not ops_none)

cols = K.operand_columns({"a.py": SRC_BOTH, "b.py": SRC_TOP}, ("a.py",))
total = K.operand_columns_total({"a.py": SRC_BOTH, "b.py": SRC_TOP})
check("the partition is TOTAL over two files at three depths",
      sum(len(v) for v in cols.values()) == total and total > 0,
      "columns %d, walk %d" % (sum(len(v) for v in cols.values()), total))
check("an operand in an UNSWEPT file lands in `not swept: file`, whatever its "
      "depth",
      len(cols["not swept: file"]) == 2
      and all(o.file == "b.py" for o in cols["not swept: file"]))
check("a NESTED operand in a swept file lands in `not swept: nested`",
      len(cols["not swept: nested"]) == 4
      and all(o.file == "a.py" and not o.top
              for o in cols["not swept: nested"]))
check("`not determined` exists as a column even when it is empty",
      "not determined" in cols and cols["not determined"] == [])
check("every column name is one of OPERAND_COLUMNS",
      set(cols) == set(K.OPERAND_COLUMNS))
check("no operand appears in two columns",
      len({id(o) for v in cols.values() for o in v})
      == sum(len(v) for v in cols.values()))

# ---------------------------------------------------------------------------
print("\n-- drop_boolean_operand: it removes ONE operand and nothing else")

nested_and = [o for o in K.boolean_operands(SRC_NESTED, "n.py")
              if "x > 0" in (o.source or "")][0]
cut = K.drop_boolean_operand(SRC_NESTED, nested_and)
check("deleting the nested operand really changes the source", cut != SRC_NESTED)
try:
    ast.parse(cut)
    parsed = True
except SyntaxError:
    parsed = False
check("...and the result still parses", parsed)
check("...and the operand it named is gone", "x > 0" not in cut)
check("...and the other operand is kept", "x < 9" in cut)
check("...and one operand left means the operator goes too",
      " and " not in cut.split("if", 1)[1])

three = "def f(a):\n    if a == 1 or a == 2 or a == 3:\n        return 1\n"
ops3 = K.boolean_operands(three, "t.py")
cut3 = K.drop_boolean_operand(three, ops3[1])
check("with three operands, deleting one keeps the operator",
      "a == 1" in cut3 and "a == 3" in cut3 and "a == 2" not in cut3
      and " or " in cut3, cut3)

# ---------------------------------------------------------------------------
print("\n-- the bends: every one refuses on zero occurrences and on many")

for name, fn, anchor in (("bend_kern_up", L.bend_kern_up, L.KERN_V),
                         ("bend_c1_down", L.bend_c1_down, L.C1_V),
                         ("conspire_c1", L.conspire_c1, L.C1_V)):
    for label, text in (("zero", "nothing here"),
                        ("two", anchor + "\n" + anchor)):
        try:
            fn(text)
            refused = False
        except ValueError:
            refused = True
        check("%s refuses on %s occurrence(s)" % (name, label), refused)
    got = fn(anchor)
    check("%s applied to exactly one occurrence changes it" % name,
          got != anchor)

try:
    L.conspire_kern("DIM_SHIFT_69D1 = 0")
    refused = False
except ValueError:
    refused = True
check("conspire_kern refuses when the name is already there", refused)

# ---------------------------------------------------------------------------
print("\n-- the conspiring pair is a pair of NO-OPS, by construction")

k_before = "X = 1\n"
k_after = L.conspire_kern(k_before)
check("the kernel half only APPENDS", k_after.startswith(k_before))
check("...a module-level assignment and nothing else",
      [type(n).__name__ for n in ast.parse(k_after[len(k_before):]).body]
      == ["Assign"])
c_after = L.conspire_c1(L.C1_V)
check("the c1 half reads the name with a DEFAULT",
      'getattr(_k69d1, "DIM_SHIFT_69D1", 0)' in c_after)
check("...and the default is 0, so the half alone shifts nothing",
      ', "DIM_SHIFT_69D1", 0)' in c_after)
check("...and the shifted value is d + <that>, not d + 1",
      "d + getattr" in c_after and "d + 1" not in c_after)

# ---------------------------------------------------------------------------
print("\n-- read_literal: the constants this instrument does not copy")

check("read_literal finds a string", L.read_literal("A = 'x'\n", "A") == "x")
check("read_literal finds a tuple",
      L.read_literal("B = ('p', 'q')\n", "B") == ("p", "q"))
try:
    L.read_literal("A = 1\n", "Z")
    raised = False
except KeyError:
    raised = True
check("read_literal raises on an absent name", raised)
check("REV_A218 is a 40-character sha read out of lib58da",
      len(L.REV_A218) == 40 and all(c in "0123456789abcdef"
                                    for c in L.REV_A218))
check("SWEEP_FILES is non-empty and read out of d2_deletion.py",
      bool(L.SWEEP_FILES) and "face_complex.py" in L.SWEEP_FILES)

# ---------------------------------------------------------------------------
print("\n-- the grep parser: two output shapes, one of them with a revision")

hits = L.grep("SWEEP_FILES")
check("a worktree grep returns readable paths",
      bool(hits) and all(os.path.exists(os.path.join(L.REPO, p))
                         for p, _ln in hits),
      "unreadable: %r" % [p for p, _ in hits
                          if not os.path.exists(os.path.join(L.REPO, p))])
check("...and every line number is an integer",
      all(str(ln).isdigit() for _p, ln in hits))
rev_hits = L.grep("REV_A218", rev="HEAD")
check("a revision grep drops the revision and keeps the path",
      bool(rev_hits) and all("/" in p or p.endswith(".md")
                             for p, _ln in rev_hits),
      "%r" % rev_hits[:3])

# ---------------------------------------------------------------------------
print("\n" + "=" * 74)
for name in BAD:
    print("   FAILED: %s" % name)
# The count goes LAST so that `tail -1` in run_all.sh reports it.  A runner
# whose one-line summary is a row of `=` tells the reader nothing.
print("%d assertion(s): %d ok, %d FAILED" % (len(OK) + len(BAD), len(OK),
                                             len(BAD)))
sys.exit(1 if BAD else 0)
