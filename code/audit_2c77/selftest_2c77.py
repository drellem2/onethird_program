"""selftest_2c77.py -- this audit's own instrument, before it is pointed at
anything.

Every probe below rests on one of four things: that my operand walkers read the
rule the same way the shipped ones do, that my position key cannot merge two
operands into one, that each bend really changes the file it names and refuses
when it cannot, and that `g1`'s IDENTICAL/MOVED test as re-implemented here
gives the same answer on inputs whose answer is known by construction.

THE WALKER AGREEMENT ASSERTION IS THE LOAD-BEARING ONE.  `q3`'s whole finding is
a SUBTRACTION -- every boolean operand in the file, minus the ones inside a
deciding condition.  If my deciding-condition reading were narrower than the
shipped one, the subtraction would manufacture the finding out of my own bug.
So the two are required to agree SPAN FOR SPAN, not in count, on both census
files, and the assertion is written so that it fails if either side is empty.

Exit 0 iff every assertion passes.
"""

import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "face_geometry_instr_5f9a"))

import lib2c77 as L                                              # noqa: E402
import kern5f9a as K                                             # noqa: E402

OK, BAD = [0], []


def ck(cond, what):
    if cond:
        OK[0] += 1
    else:
        BAD.append(what)
    print("   %-5s %s" % ("ok" if cond else "FAIL", what))


L.banner("SELFTEST", "the mg-2c77 instrument, before it is pointed at anything")

# ---------------------------------------------------------------------------
print("\n-- the position key: it must not merge two operands into one")
SRC_DUP = """
def f(a, b):
    if a == b or a is b:
        return 1
    return a == b or b is a
"""
ops = L.all_boolean_operands(SRC_DUP, "dup.py")
ck(len(ops) == 4, "4 operands over two `or`s in a 4-line module: got %d"
   % len(ops))
ck(len({o["pos"] for o in ops}) == 4,
   "the 4 position keys are distinct even though `a == b` occurs twice")
ck(len({o["text"] for o in ops}) == 3,
   "a TEXT key would have merged the two `a == b` into one (3 distinct texts "
   "for 4 operands) -- which is why the key is a span")

# ---------------------------------------------------------------------------
print("\n-- my deciding-condition reading against the shipped one, span for "
      "span")
for rel in (L.FACE_REL, L.POSETS_REL):
    src = L.read_worktree(rel)
    mine = [(f, k, L.pos(c)) for f, k, c in L.deciding_conditions_mine(src)]
    theirs = [(f, k, L.pos(c)) for f, k, c in K.deciding_conditions(src)]
    ck(len(mine) > 0, "%s: my walker found %d deciding condition(s), not 0 -- "
       "an empty walk would make every subtraction below vacuous"
       % (os.path.basename(rel), len(mine)))
    ck(sorted(mine) == sorted(theirs),
       "%s: my deciding conditions and kern5f9a's agree span for span (%d vs "
       "%d)" % (os.path.basename(rel), len(mine), len(theirs)))

print("\n-- my deciding-OPERAND walk against kern5f9a.boolean_operands, span "
      "for span")
for rel in (L.FACE_REL, L.POSETS_REL):
    src = L.read_worktree(rel)
    name = os.path.basename(rel)
    mine = sorted(o["pos"] for o in L.deciding_boolean_operands(src, name))
    theirs = sorted(L.pos(op.node.values[op.index])
                    for op in K.boolean_operands(src, name))
    ck(len(mine) > 0, "%s: %d deciding boolean operand(s), not 0" % (name,
                                                                     len(mine)))
    ck(mine == theirs, "%s: agrees with kern5f9a.boolean_operands span for "
       "span (%d vs %d)" % (name, len(mine), len(theirs)))

print("\n-- the unfiltered walk is a SUPERSET of the deciding one, by "
      "construction")
for rel in (L.FACE_REL, L.POSETS_REL):
    src = L.read_worktree(rel)
    name = os.path.basename(rel)
    allp = {o["pos"] for o in L.all_boolean_operands(src, name)}
    decp = {o["pos"] for o in L.deciding_boolean_operands(src, name)}
    ck(decp <= allp, "%s: every deciding operand is in the unfiltered walk -- "
       "if it were not, the difference would be my bug and not a finding"
       % name)

print("\n-- the unfiltered walk really does see outside a deciding condition")
SRC_OUT = """
def g(xs):
    total = 0
    for x in xs:
        if x > 0 and x < 10:
            total += x
    return total
"""
ck(len(L.all_boolean_operands(SRC_OUT, "o.py")) == 2,
   "an `and` in an `if` whose body only assigns: 2 operands unfiltered")
ck(len(L.deciding_boolean_operands(SRC_OUT, "o.py")) == 0,
   "the same `and`: 0 operands inside a deciding condition -- the `if` "
   "contains no `return`")
ck(K.operand_columns({"o.py": SRC_OUT}, ("o.py",)) ==
   {c: [] for c in K.OPERAND_COLUMNS},
   "and the SHIPPED classifier puts it in NO column: all four columns empty "
   "on a file whose only boolean operator is outside a deciding condition")

print("\n-- and the same operand moved INSIDE a deciding condition is seen")
SRC_IN = """
def g(x):
    if x > 0 and x < 10:
        return 1
    return 0
"""
ck(len(L.deciding_boolean_operands(SRC_IN, "i.py")) == 2,
   "the same `and`, with a `return` in the `if`: 2 deciding operands")
cols_in = K.operand_columns({"i.py": SRC_IN}, ("i.py",))
ck(len(cols_in["swept"]) == 2 and sum(len(v) for v in cols_in.values()) == 2,
   "and the shipped classifier puts both in `swept`")

# ---------------------------------------------------------------------------
print("\n-- the bends: each changes the file it names, and refuses otherwise")
c1 = L.git_show("HEAD", L.C1_REL)
kern = L.git_show("HEAD", L.KERN_REL)
for label, fn, src in (("bend_kern_up", L.bend_kern_up, kern),
                       ("bend_c1_down", L.bend_c1_down, c1),
                       ("conspire_a_kern", L.conspire_a_kern, kern),
                       ("conspire_a_c1", L.conspire_a_c1, c1),
                       ("conspire_b_kern", L.conspire_b_kern, kern),
                       ("conspire_b_c1", L.conspire_b_c1, c1)):
    try:
        bent = fn(src)
        ck(bent != src, "%s really changes its input (%+d bytes)"
           % (label, len(bent) - len(src)))
        ck(ast.parse(bent) is not None,
           "%s leaves a file that still parses" % label)
    except ValueError as e:
        ck(False, "%s raised: %s" % (label, e))

print("\n-- and each refuses on ZERO occurrences and on MANY")
ck_pairs = [("bend_kern_up", L.bend_kern_up), ("bend_c1_down", L.bend_c1_down),
            ("conspire_a_c1", L.conspire_a_c1),
            ("conspire_b_c1", L.conspire_b_c1)]
for label, fn in ck_pairs:
    try:
        fn("nothing here at all\n")
        ck(False, "%s accepted a source with 0 occurrences" % label)
    except ValueError:
        ck(True, "%s refuses on 0 occurrences" % label)
for label, fn, src, needle in (("bend_kern_up", L.bend_kern_up, kern, L.KERN_V),
                               ("bend_c1_down", L.bend_c1_down, c1, L.C1_V),
                               ("conspire_a_c1", L.conspire_a_c1, c1, L.C1_V),
                               ("conspire_b_c1", L.conspire_b_c1, c1, L.C1_V)):
    try:
        fn(src + "\n" + needle + "\n")
        ck(False, "%s accepted a source with 2 occurrences" % label)
    except ValueError:
        ck(True, "%s refuses on 2 occurrences" % label)
for label, fn, src in (("conspire_a_kern", L.conspire_a_kern, kern),
                       ("conspire_b_kern", L.conspire_b_kern, kern)):
    try:
        fn(fn(src))
        ck(False, "%s appended its marker twice" % label)
    except ValueError:
        ck(True, "%s refuses when its marker is already present" % label)

# ---------------------------------------------------------------------------
print("\n-- the IDENTICAL/MOVED test, on inputs whose answer is known")
target = L.git_show("HEAD", L.TARGET_REL)
old_c1 = L.git_show(L.REV_A218, L.C1_REL)
old_kern = L.git_show(L.REV_A218, L.KERN_REL)
base_out, base_rc = L.run_c1(target, old_c1, old_kern)
base_lines = L.vertex_lines(base_out)
ref = (L.sha(L.measuring_half(base_out))[:16], base_lines)
# MISS #1, KEPT.  This assertion first read `base_rc == 0` and FAILED, and the
# instrument was right and I was wrong.  c1 at REV_A218 handed the HEAD target
# exits 1 because its COMPARING half disagrees with a target in the other form
# -- which is the half `C1_SPLIT` cuts off and the half g1 deliberately does not
# read.  g1 itself discards the return code (`out, _ = run_c1(...)`).  An audit
# that had gated on the exit code would have been asking the measuring half a
# question about the comparing half, which is mg-7e58's own G-1 defect.
ck(base_rc in (0, 1),
   "the baseline c1 run terminates with a status this audit does not read: "
   "rc=%d.  The verdict is the MEASURING half, and the comparing half is "
   "where a status lives" % base_rc)
ck(len(base_lines) == 24,
   "the baseline run prints c1's 24 vertex sets: got %d" % len(base_lines))
ck(L.g1_verdict(target, old_c1, old_kern, ref)["same"] is True,
   "the baseline against itself reads IDENTICAL")
ck(L.g1_verdict(target, L.bend_c1_down(old_c1), old_kern, ref)["same"] is False,
   "c1 with every dimension one too small reads MOVED -- the test can go red")

print("\n-- the empty-baseline guard: a run that produces nothing is never "
      "IDENTICAL")
broken = "raise SystemExit('deliberate')\n"
v = L.g1_verdict(target, broken, old_kern, ref)
ck(v["cells"] == 0, "a c1 that dies prints 0 vertex sets")
ck(v["same"] is False,
   "and reads MOVED, not IDENTICAL -- two failed runs cannot agree")

# ---------------------------------------------------------------------------
print("\n-- SWEEP_FILES and REV_A218 are READ, not written down here")
ck(L.SWEEP_FILES == ("face_complex.py",),
   "SWEEP_FILES read out of d2_deletion.py: %r" % (L.SWEEP_FILES,))
ck(len(L.REV_A218) >= 8 and L.REV_A218 == L.git("rev-parse", L.REV_A218).strip(),
   "REV_A218 read out of lib58da.py resolves in this repository: %s"
   % L.REV_A218[:8])

print()
print("-" * 74)
print("ASSERTIONS PASSED: %d, FAILED: %d" % (OK[0], len(BAD)))
for b in BAD:
    print("   FAILED: " + b)
sys.exit(1 if BAD else 0)
