"""selftest_76cc.py -- the instrument, tested before anything rests on it.

Every helper in lib76cc.py that a finding depends on, asserted to be
NON-VACUOUS as well as correct.  The distinction is the point of this file:

  * a reader that returns {} agrees with everything;
  * a corruption probe that corrupts nothing makes every deletion test say
    whatever it likes;
  * a normalisation that forgives everything reproduces everything;
  * a gate that cannot go red certifies nothing.

Each of those four is asserted here directly, on synthetic inputs where the
right answer is known, so that r1..r4 never have to be trusted about their own
machinery.

Exit 0 iff every assertion holds.
"""

import sys

import lib76cc as L

N = [0]
BAD = []


def ok(cond, what):
    N[0] += 1
    if not cond:
        BAD.append(what)
    print("   %-4s %s" % ("ok" if cond else "FAIL", what))


L.banner("SELFTEST", "lib76cc, ASSERTED BEFORE ANY FINDING RESTS ON IT")
print()

# ---------------------------------------------------------------------------
L.rule("1. THE REVISION CONSTANTS RESOLVE, AND ARE FULL SHAS")
for name, rev in (("REV_A218", L.REV_A218), ("REV_321D", L.REV_321D),
                  ("REV_957F", L.REV_957F)):
    ok(len(rev) == 40, "%s is a full 40-character sha" % name)
    try:
        ok(L.resolve(rev) == rev, "%s resolves to itself" % name)
    except Exception as e:
        ok(False, "%s resolves (%s)" % (name, e))
ok(L.is_ancestor(L.REV_A218, "HEAD"), "REV_A218 is an ancestor of HEAD")
ok(L.is_ancestor(L.REV_321D, "HEAD"), "REV_321D is an ancestor of HEAD")
ok(L.is_ancestor(L.REV_957F, "HEAD"), "REV_957F is an ancestor of HEAD")
ok(L.is_ancestor(L.REV_321D, L.REV_957F),
   "REV_321D is an ancestor of REV_957F -- the three are in the order this "
   "instrument assumes")
ok(not L.is_ancestor(L.REV_957F, L.REV_321D),
   "and not the other way round")
ok(L.distance(L.REV_321D, L.REV_957F) > 0,
   "the distance between them is positive")

# ---------------------------------------------------------------------------
L.rule("2. THE FILES THIS INSTRUMENT NAMES ALL EXIST")
for rel in (L.G1_REL, L.LIB_REL, L.KERN_REL, L.C1_REL, L.TARGET_REL):
    try:
        ok(len(L.read_worktree(rel)) > 0, "%s is present and non-empty" % rel)
    except Exception as e:
        ok(False, "%s is present (%s)" % (rel, e))
for name in L.FIVE_OUTPUTS:
    try:
        ok(len(L.read_worktree(L.S58DA_DIR + "/" + name)) > 0,
           "%s is present and non-empty" % name)
    except Exception as e:
        ok(False, "%s is present (%s)" % (name, e))

# ---------------------------------------------------------------------------
L.rule("3. THE READER IS NOT BLIND -- IT RETURNS CELLS, AND THE RIGHT ONES")
target = L.read_worktree(L.TARGET_REL)
c1 = L.read_worktree(L.C1_REL)
kern = L.read_worktree(L.KERN_REL)
out, rc = L.run_c1(target, c1, kern)
cells = L.c1_own_vertices(out)
ok(len(cells) == 24, "c1_own_vertices reads 24 cells out of a live c1 run")
ok(rc == 0, "that live c1 run exits 0")
ok(all(isinstance(v, list) for v in cells.values()),
   "every cell is a list of (p, dim) pairs")
ok(cells.get((3, 1)) == [(0, 1)], "beta=3, n=1 is [(0, 1)]")
ok(len(cells.get((3, 6), [])) == 4, "beta=3, n=6 has 4 simples")
ok(L.c1_own_vertices("nothing of the sort") == {},
   "the reader returns {} on text that has no section (i), rather than a "
   "partial parse")
ok(L.c1_own_vertices("   beta = 3\n   n=1  count 1  set { p=0:dim }") == {},
   "and {} on a malformed pair, rather than half a cell")

# ---------------------------------------------------------------------------
L.rule("4. THE CORRUPTION PROBES REALLY CORRUPT")
bent_kern = L.bend_kernel(kern)
ok(bent_kern != kern, "bend_kernel changes kern_a218.py")
out_b, _ = L.run_c1(target, c1, bent_kern)
cells_b = L.c1_own_vertices(out_b)
moved = [k for k in cells if cells[k] != cells_b.get(k)]
ok(len(moved) == 24,
   "and the bend REACHES c1's output: 24 of 24 vertex cells move")
ok(L.measuring_half(out) != L.measuring_half(out_b),
   "and c1's sections (i)+(ii) differ under it")
bent_c1 = L.bend_c1_measure(c1)
out_c, _ = L.run_c1(target, bent_c1, kern)
ok(L.measuring_half(out_c) != L.measuring_half(out),
   "bend_c1_measure reaches c1's measuring half")
out_d, _ = L.run_c1(target, L.comment_c1(c1), kern)
ok(L.measuring_half(out_d) == L.measuring_half(out),
   "comment_c1 changes the file and NOT the measurement -- the control that "
   "must stay silent")
out_e, _ = L.run_c1(target, L.touch_c1_compare(c1), kern)
ok(L.measuring_half(out_e) == L.measuring_half(out),
   "touch_c1_compare changes the comparing half and NOT the measurement")
try:
    L.bend_kernel(bent_kern)
    ok(False, "bend_kernel refuses to bend an already-bent kernel")
except ValueError:
    ok(True, "bend_kernel refuses to bend an already-bent kernel")
try:
    L.replace_once("aa", "a", "b")
    ok(False, "replace_once refuses two occurrences")
except ValueError:
    ok(True, "replace_once refuses two occurrences")
try:
    L.replace_once("aa", "z", "b")
    ok(False, "replace_once refuses zero occurrences")
except ValueError:
    ok(True, "replace_once refuses zero occurrences")

# ---------------------------------------------------------------------------
L.rule("5. THE SOURCE SURGERY ON g1 IS EXACT, AND EACH PIECE COMPILES")
g1 = L.read_worktree(L.G1_REL)
for name, fn, expect_lines in (("drop_kernel_half", L.drop_kernel_half, 1),
                               ("drop_both_half", L.drop_both_half, 1),
                               ("drop_kernel_probe", L.drop_kernel_probe, 3),
                               ("repin_kernel", L.repin_kernel, 0)):
    try:
        out_src = fn(g1)
        ok(out_src != g1, "%s changes g1_provenance.py" % name)
        removed = len(g1.splitlines()) - len(out_src.splitlines())
        ok(removed == expect_lines,
           "%s removes %d line(s), as declared" % (name, expect_lines))
        compile(out_src, "g1", "exec")
        ok(True, "%s leaves g1_provenance.py compiling" % name)
    except Exception as e:
        ok(False, "%s applies cleanly (%s)" % (name, e))
ok(L.MEASUREMENT_REPAIRED in g1,
   "the repaired measurement() call is present in g1 -- the anchor repin "
   "rests on")
ok(L.HALF_KERNEL_ROW in g1, "the kern_a218.py row of HALVES is present in g1")
compile(L.repin_kernel(g1).replace(L.MEASUREMENT_REPINNED,
                                   L.MEASUREMENT_REPAIRED), "g1", "exec")
ok(L.repin_kernel(g1).replace(L.MEASUREMENT_REPINNED,
                              L.MEASUREMENT_REPAIRED) == g1,
   "repin_kernel is exactly invertible -- it touches that call and nothing "
   "else")

# ---------------------------------------------------------------------------
L.rule("6. THE PINNED PREDICATES CAN BE BUILT, WITH THEIR OWN LIBRARY")
for rev in (L.REV_321D, L.REV_957F):
    try:
        src = L.git_show(rev, L.G1_REL)
        lib = L.git_show(rev, L.LIB_REL)
        ok(src.count("import lib58da as L") == 1,
           "g1 at %s has exactly one lib58da import to repoint" % rev[:8])
        ok(len(lib) > 0, "lib58da at %s is readable" % rev[:8])
        compile(src, "g1", "exec")
        ok(True, "g1 at %s compiles" % rev[:8])
    except Exception as e:
        ok(False, "g1 at %s can be pinned (%s)" % (rev[:8], e))
ok(L.git_show(L.REV_957F, L.G1_REL) != g1,
   "g1 at REV_957F differs from g1 here -- there is a patch to test at all")
ok("kernel_source" not in L.git_show(L.REV_957F, L.LIB_REL),
   "lib58da at REV_957F has no kernel_source argument -- the hole is really "
   "there in the revision this repair is measured against")
ok("kernel_source" in L.read_worktree(L.LIB_REL),
   "and it is here")

# ---------------------------------------------------------------------------
L.rule("7. THE NORMALISATION IS NEITHER BLIND NOR A BLANKET")
rev = "abcdef0123456789abcdef0123456789abcdef01"
subj = "a subject line"
text = ("head %s tail\nshort %s\nshorter %s\nsubject: %s\nkeep 286d5030\n"
        % (rev, rev[:12], rev[:8], subj))
norm, nsub = L.normalize(text, rev, subj)
ok(nsub == 4, "normalize makes exactly the 4 substitutions present")
ok(L.REV_PLACEHOLDER in norm, "the revision is replaced")
ok(L.SUBJ_PLACEHOLDER in norm, "the subject is replaced")
ok("286d5030" in norm,
   "a DIFFERENT revision in the same text is left alone -- pinned constants "
   "must still reproduce byte for byte")
ok(rev[:8] not in norm, "no 8-character remnant survives")
other = text.replace("keep 286d5030", "keep 286d5031")
norm2, _ = L.normalize(other, rev, subj)
ok(L.differing_lines(norm, norm2),
   "a real, non-revision difference is still caught after normalisation")
ok(not L.differing_lines(norm, norm),
   "and identical texts come back with no differing lines")
n3, _ = L.normalize(text, rev, "")
ok(L.SUBJ_PLACEHOLDER not in n3,
   "an empty subject substitutes nothing rather than everything")

# ---------------------------------------------------------------------------
L.rule("8. differing_lines COUNTS, INCLUDING PAST THE END")
ok(L.differing_lines("a\nb", "a\nb") == [], "identical texts: no rows")
ok(len(L.differing_lines("a\nb", "a\nc")) == 1, "one changed line: one row")
ok(len(L.differing_lines("a", "a\nb")) == 1, "one extra line: one row")
ok(L.differing_lines("a", "a\nb")[0][1] is None,
   "and the absent side is None, not empty string")
ok(len(L.differing_lines("a\nb\nc", "x\nb\ny")) == 2, "two changed: two rows")

# ---------------------------------------------------------------------------
L.rule("9. THE TRANSCRIPT READERS READ THE REAL TRANSCRIPTS")
g1out = L.read_worktree(L.S58DA_DIR + "/out_g1_provenance.txt")
rec = L.recorded_rev(g1out)
ok(rec is not None and len(rec) == 12,
   "recorded_rev finds a 12-character revision in out_g1_provenance.txt")
ok(L.is_hex(rec or ""), "and it is hexadecimal")
ok(L.recorded_rev("no such line here") is None,
   "and returns None rather than a guess when the line is absent")
ok(L.totals_of(g1out)[0] is not None and L.totals_of(g1out)[1] is not None,
   "totals_of reads both totals out of a real transcript")
ok(L.totals_of("SELF-ERRORS: 3, population: x\nFINDINGS: 7, population: y")
   == (3, 7), "totals_of reads the numbers and not the populations")
ok(L.totals_of("nothing") == (None, None),
   "and returns (None, None) rather than (0, 0) when there is nothing to read")
ok(L.findings_of("   FINDING: one\n   FINDING: two") == ["one", "two"],
   "findings_of splits on the printed marker")
ok(L.findings_of("FINDINGS: 0, population: x") == [],
   "and does not mistake the population line for a finding")

# ---------------------------------------------------------------------------
L.rule("10. A CLONE IS A REAL CLONE, AND ITS MUTATION IS A COMMIT")
tmp, tree = L.clone(message="mg-76cc selftest clone")
try:
    ok(L.head_rev(repo=tree) != "", "the clone has a HEAD")
    ok(L.read_worktree(L.G1_REL, repo=tree) == g1,
       "the clone carries this worktree's g1_provenance.py")
finally:
    L.destroy(tmp)


def _bend(t):
    import os as _os
    p = _os.path.join(t, L.KERN_REL)
    with open(p) as fh:
        s = fh.read()
    with open(p, "w") as fh:
        fh.write(L.bend_kernel(s))


tmp, tree = L.clone(mutate=_bend, message="mg-76cc selftest bent clone")
try:
    ok(L.git_show("HEAD", L.KERN_REL, repo=tree) != kern,
       "a mutated clone's change is visible to git_show at HEAD -- it is a "
       "COMMIT and not a working-tree edit")
    ok(L.read_worktree(L.KERN_REL, repo=tree) != kern,
       "and it is in the working tree too")
finally:
    L.destroy(tmp)

tmp, tree = L.clone(empty_extra=True, message="mg-76cc selftest two commits")
try:
    ok(L.distance(L.head_rev(), L.head_rev(repo=tree), repo=tree) == 2,
       "empty_extra puts the clone exactly two commits ahead of this branch")
finally:
    L.destroy(tmp)

# ---------------------------------------------------------------------------
L.rule("11. THE REPORT SEPARATES THE TWO CHANNELS AND CAN GO RED")
r = L.Report("s", "f")
ok(r.emit() == 0, "an empty report exits 0")
r.check(False, "x")
ok(len(r.self_) == 1 and len(r.find) == 0,
   "check() books a SELF-ERROR and not a finding")
r.gate(False, "y")
ok(len(r.find) == 1, "gate() books a FINDING")
ok(r.emit() == 1, "and the report then exits 1 -- the gate can go red")
r2 = L.Report("s", "f")
r2.check(True, "x")
r2.gate(True, "y")
ok(r2.emit() == 0, "and stays green when both hold")

# ---------------------------------------------------------------------------
print()
print("-" * 74)
print("ASSERTIONS: %d, population: every helper in lib76cc.py that a finding "
      "in r1..r4 rests on" % N[0])
print("FAILED: %d" % len(BAD))
for b in BAD:
    print("   FAILED: " + b)
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
