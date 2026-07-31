"""selftest_e34a.py -- the instrument, before any finding rests on it.

Every assertion here is about libe34a, not about mg-76cc.  If this exits
non-zero, nothing in k1-k4 may be believed until the failure is understood: a
reader that mis-parses agrees with everything, and a bend that bends nothing
comes back silent for a reason that has nothing to do with the predicate.

The ones that matter most, and why they are here:

  * THE BENDS REALLY BEND.  mg-957f made a probe in a working tree that g1
    reads with `git show` and kept the miss.  Every bend here is asserted to
    change the file, and `replace_once` is asserted to REFUSE on zero
    occurrences and on many rather than silently doing nothing.
  * THE CANCELLING PAIR REALLY CANCELS.  k4's whole finding rests on it, so
    it is measured here before it is used there.
  * THE FINDING READER DISCRIMINATES.  A `FINDING:` line quoted from a nested
    transcript is not this script's finding.  Asserted on a synthetic
    transcript built here, so the assertion does not depend on any committed
    file staying the shape it is.
"""

import os
import sys

import libe34a as L

N, BAD = [0], []


def ok(cond, what):
    N[0] += 1
    if not cond:
        BAD.append(what)
    print("   %-4s %s" % ("ok" if cond else "FAIL", what))


print("=" * 74)
print("SELFTEST  libe34a -- the apparatus for mg-e34a")
print("=" * 74)
print()

print("-" * 74)
print("(1) THE REVISIONS ARE DERIVED, AND THEY RESOLVE")
print("-" * 74)
ok(len(L.REV_A218) == 40 and all(c in "0123456789abcdef" for c in L.REV_A218),
   "REV_A218 read out of lib58da.py's own source is a 40-char sha")
ok(L.REV_A218 == L.read_literal(L.read_worktree(L.LIB_REL), "REV_A218"),
   "read_literal is stable on a second call")
try:
    L.read_literal("X = 1\n", "REV_A218")
    ok(False, "read_literal RAISES when the name is absent")
except ValueError:
    ok(True, "read_literal RAISES when the name is absent")
ok(L.REPAIR_REV and len(L.REPAIR_REV) == 40,
   "REPAIR_REV -- the last commit touching g1_provenance.py -- resolves")
ok(L.PRE_REV == L.resolve(L.REPAIR_REV + "^"),
   "PRE_REV is exactly the first parent of REPAIR_REV")
ok(L.git_show(L.PRE_REV, L.G1_REL) != L.read_worktree(L.G1_REL),
   "g1 at PRE_REV really differs from g1 here -- there is a predicate to run")
ok(L.is_ancestor(L.PRE_REV, "HEAD"),
   "PRE_REV is an ancestor of HEAD")
ok(L.is_ancestor(L.REV_A218, "HEAD"),
   "REV_A218 is an ancestor of HEAD")
ok(not L.is_ancestor("HEAD", L.REV_A218),
   "is_ancestor is not symmetric -- it is answering the question asked")
ok(L.distance(L.PRE_REV, L.head_rev()) >= 1,
   "distance(PRE_REV, HEAD) is at least 1")
ok(L.distance(L.head_rev(), L.head_rev()) == 0,
   "distance from a revision to itself is 0")
ok(L.PRE_7E58_REV and L.is_ancestor(L.PRE_7E58_REV, L.PRE_REV),
   "PRE_7E58_REV is an ancestor of PRE_REV -- the order is the log's order")
print()

print("-" * 74)
print("(2) THE TRANSCRIPT READER, ON TRANSCRIPTS BUILT HERE")
print("-" * 74)
SYN = "\n".join([
    "some prose",
    "      FINDING: a finding QUOTED from a nested run at six spaces",
    "SELF-ERRORS: 1, population: the things",
    "   SELF-ERROR: the one self-error",
    "FINDINGS: 2, population: the other things",
    "   FINDING: the first real finding",
    "   FINDING: the second real finding",
    "TOTAL BAD: 3",
])
ok(L.trailer(SYN) == (1, 2), "trailer reads (1, 2) off the trailer lines")
ok(len(L.findings(SYN)) == 2,
   "the finding reader counts 2 -- the nested six-space quote is NOT one")
ok(len(L.selferrs(SYN)) == 1, "the self-error reader counts 1")
ok(L.trailer_consistent(SYN)[0],
   "the trailer's counts agree with the lines it lists")
BADSYN = SYN.replace("FINDINGS: 2", "FINDINGS: 3")
ok(not L.trailer_consistent(BADSYN)[0],
   "a trailer saying 3 over 2 listed lines is caught")
ok(L.trailer("nothing here") == (None, None),
   "a transcript with no trailer reads (None, None), which is not (0, 0)")
ok(L.findings("   FINDING: before any trailer line") == [],
   "a FINDING line BEFORE the trailer is not counted -- position matters too")
ok(L.names_files("c1's own measurement moved when kern_a218.py is moved")
   == ("kern_a218.py",),
   "names_files reports the one file a finding names")
ok(L.names_files("nothing named here") == (),
   "names_files reports nothing when a finding names nothing")
ok(L._leading_int(" 12, population: 34") == 12,
   "the leading integer is read and the rest of the line is not")
ok(L._leading_int("no digits") is None,
   "a line with no leading integer reads None, not 0")
print()

print("-" * 74)
print("(3) THE BENDS REALLY BEND, AND REFUSE WHEN THEY CANNOT")
print("-" * 74)
head_c1 = L.git_show("HEAD", L.C1_REL)
head_k = L.git_show("HEAD", L.KERN_REL)
old_c1 = L.git_show(L.REV_A218, L.C1_REL)
old_k = L.git_show(L.REV_A218, L.KERN_REL)
for name, fn, src in (("bend_c1_up", L.bend_c1_up, head_c1),
                      ("bend_c1_down", L.bend_c1_down, head_c1),
                      ("bend_kern_up", L.bend_kern_up, head_k),
                      ("comment_c1", L.comment_c1, head_c1),
                      ("comment_kern", L.comment_kern, head_k),
                      ("touch_c1_compare", L.touch_c1_compare, head_c1)):
    try:
        out = fn(src)
        ok(out != src, "%s changes the file it is given" % name)
    except ValueError as e:
        ok(False, "%s raised (%s)" % (name, e))
try:
    L.replace_once("aaa", "a", "b")
    ok(False, "replace_once REFUSES when the anchor occurs many times")
except ValueError:
    ok(True, "replace_once REFUSES when the anchor occurs many times")
try:
    L.replace_once("aaa", "z", "b")
    ok(False, "replace_once REFUSES when the anchor occurs zero times")
except ValueError:
    ok(True, "replace_once REFUSES when the anchor occurs zero times")
try:
    L.bend_kern_up(L.bend_kern_up(head_k))
    ok(False, "bending an already-bent kernel REFUSES rather than double-bending")
except ValueError:
    ok(True, "bending an already-bent kernel REFUSES rather than double-bending")
print()

print("-" * 74)
print("(4) run_c1 TAKES THE SCRIPT AND THE KERNEL AS TWO SOURCES")
print("-" * 74)
target = L.git_show("HEAD", L.TARGET_REL)
base_out, _ = L.run_c1(target, old_c1, old_k)
base_m = L.sha(L.measuring_half(base_out))
base_v = L.vertex_cells(base_out)
ok(len(base_v) == 24, "c1's own vertex sets parse back as 24 cells")
ok(all(len(v) > 0 for v in base_v.values()),
   "every one of the 24 parsed cells is non-empty")
ok(L.vertex_cells("no c1 output here") == {},
   "the vertex reader returns {} on an absent form, not a partial parse")
kern_out, _ = L.run_c1(target, old_c1, L.bend_kern_up(old_k))
ok(L.sha(L.measuring_half(kern_out)) != base_m,
   "bending ONLY the kernel moves the measurement -- the kernel argument is "
   "live")
c1_out, _ = L.run_c1(target, L.bend_c1_up(old_c1), old_k)
ok(L.sha(L.measuring_half(c1_out)) != base_m,
   "bending ONLY the script moves the measurement -- the script argument is "
   "live")
same_out, _ = L.run_c1(target, old_c1, old_k)
ok(L.sha(L.measuring_half(same_out)) == base_m,
   "the same two sources twice give the same measurement -- the run is "
   "deterministic")
print()

print("-" * 74)
print("(5) THE CANCELLING PAIR REALLY CANCELS -- k4's FINDING RESTS ON IT")
print("-" * 74)
pair_out, _ = L.run_c1(target, L.bend_c1_down(head_c1), L.bend_kern_up(head_k))
pair_m = L.sha(L.measuring_half(pair_out))
ok(pair_m == base_m,
   "kern +1 with c1 -1 restores the measurement EXACTLY, against the "
   "unbent baseline")
ok(L.vertex_cells(pair_out) == base_v,
   "and c1's own 24 vertex cells come back equal, cell by cell")
half_a, _ = L.run_c1(target, L.bend_c1_down(head_c1), old_k)
half_b, _ = L.run_c1(target, old_c1, L.bend_kern_up(head_k))
ok(L.sha(L.measuring_half(half_a)) != base_m,
   "and EACH half of that pair on its own does move it (the c1 half)")
ok(L.sha(L.measuring_half(half_b)) != base_m,
   "and EACH half of that pair on its own does move it (the kernel half)")
print()

print("-" * 74)
print("(6) CLONES AND PINNED PREDICATES")
print("-" * 74)
tmp, tree = L.clone(carry=False, commit=False)
try:
    ok(L.head_rev(repo=tree) == L.head_rev(),
       "clone(carry=False, commit=False) has EXACTLY this branch's HEAD")
    ok(os.path.isfile(os.path.join(tree, L.G1_REL)),
       "the clone carries g1_provenance.py")
    name = L.install_pinned(tree, L.PRE_REV, "g1_pinned_test.py")
    pinned = open(os.path.join(tree, L.S58DA_DIR, name)).read()
    libname = "lib58da_at_%s" % L.PRE_REV[:8]
    ok("import %s as L" % libname in pinned,
       "the pinned g1's import is repointed at the pinned library")
    ok("import lib58da as L" not in pinned,
       "and no unpatched `import lib58da as L` is left in it")
    ok(pinned.count("import %s as L" % libname) == 1,
       "the substitution happened exactly once")
    ok(os.path.isfile(os.path.join(tree, L.S58DA_DIR, libname + ".py")),
       "the pinned lib58da travels with it, under a name of its own")
    ok(open(os.path.join(tree, L.S58DA_DIR, libname + ".py")).read()
       == L.git_show(L.PRE_REV, L.LIB_REL),
       "and it is byte-identical to lib58da at that revision")
    ok(open(os.path.join(tree, L.G1_REL)).read() == L.read_worktree(L.G1_REL),
       "g1_provenance.py itself is NEVER modified in the clone")
finally:
    L.destroy(tmp)
ok(not os.path.exists(tmp), "destroy() removes the clone")


def _touch(t):
    p = os.path.join(t, L.KERN_REL)
    with open(p) as fh:
        s = fh.read()
    with open(p, "w") as fh:
        fh.write(L.comment_kern(s))


tmp2, tree2 = L.clone(mutate=_touch, message="mg-e34a selftest clone")
try:
    ok(L.head_rev(repo=tree2) != L.head_rev(),
       "a mutating clone COMMITS, so its HEAD is a new revision")
    ok(L.git_show("HEAD", L.KERN_REL, repo=tree2)
       != L.git_show("HEAD", L.KERN_REL),
       "and the mutation is visible to `git show HEAD:` -- not left in the "
       "working tree, where g1 would never see it")
    ok(L.git_show("HEAD", L.KERN_REL, repo=tree2).startswith(
        L.git_show("HEAD", L.KERN_REL)),
       "and it is the ONLY change to that file")
finally:
    L.destroy(tmp2)
print()

print("-" * 74)
print("SELFTEST: %d assertions, %d failed" % (N[0], len(BAD)))
for b in BAD:
    print("   FAILED: %s" % b)
sys.exit(1 if BAD else 0)
