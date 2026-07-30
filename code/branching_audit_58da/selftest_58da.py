"""selftest_58da.py -- this instrument's own apparatus, before it is used.

Everything mg-58da concludes rests on three things being right:

  1. the parsers really read the datum, and really return NOTHING when the
     datum is not there -- because "absent" versus "present and disagreeing"
     is the exact distinction the ticket is about, and a parser that guesses
     would decide the answer by accident;
  2. run_c1() really runs the script at the revision it names, against the
     target text it is handed, and reports the exit code faithfully;
  3. replace_once() really refuses to corrupt zero sites or two.

Each assertion is counted and the total names its population.  A decorative
assertion counted in an assertion total is this arc's own worst habit, so
every assertion below is a statement that can fail.
"""

import sys

import lib58da as L

N = 0
BAD = []


def ok(cond, what):
    global N
    N += 1
    if not cond:
        BAD.append(what)


def raises(fn, what):
    global N
    N += 1
    try:
        fn()
    except Exception:
        return
    BAD.append(what)


print("=" * 74)
print("SELFTEST  mg-58da's OWN APPARATUS, BEFORE IT IS USED")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
# 1. git access
# ---------------------------------------------------------------------------
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
new_target = L.read_worktree(L.TARGET_REL)
old_c1 = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")

ok(len(old_target) > 1000, "the 286d503 target is non-trivial")
ok(len(new_target) > 1000, "the working-tree target is non-trivial")
ok(old_target != new_target, "the two targets differ (they must: ed9cde4)")
ok(L.sha(old_target) != L.sha(new_target), "sha distinguishes them")
ok(L.sha(old_target) == L.sha(old_target), "sha is a function")
ok("c1_branching.py" in old_c1 or "THE PRIMARY TARGET" in old_c1,
   "the 286d503 c1 source is c1")
raises(lambda: L.git_show("286d503", "code/no/such/file"),
       "git_show raises on an absent path")

# ---------------------------------------------------------------------------
# 2. the vertex-set parser.  Present, absent, and hostile inputs.
# ---------------------------------------------------------------------------
vs_new = L.parse_vertex_sets(new_target)
vs_old = L.parse_vertex_sets(old_target)

ok(len(vs_new) == 24, "the SET form is read at all 24 cells of the new target")
ok(vs_old == {}, "the SET form is ABSENT from the 286d503 target and the "
                 "parser says so rather than guessing")
ok(vs_new.get((3, 1)) == [(0, 1)], "beta=3 n=1 reads [0:1]")
ok(vs_new.get((3, 6)) == [(0, 1), (1, 5), (2, 9), (3, 5)],
   "beta=3 n=6 reads [0:1,1:5,2:9,3:5]")
ok(vs_new.get((0, 2)) == [(0, 1)], "beta=0 n=2 reads [0:1]")
ok(all(isinstance(p, int) and isinstance(d, int)
       for v in vs_new.values() for (p, d) in v),
   "every parsed entry is a pair of ints")

# a hand-built block: the parser must read it, and must read a CHANGED one
# differently.  This is the parser's own deletion test.
mini = ("head\n" + L.T1B2_START + "\n  beta = 7\n     n=1  [0:1,1:2]\n"
        "  beta = 8\n     n=2  [0:3]\n" + L.T1B2_END + "\ntail\n")
pm = L.parse_vertex_sets(mini)
ok(pm == {(7, 1): [(0, 1), (1, 2)], (8, 2): [(0, 3)]},
   "the parser reads a hand-built block exactly")
mini2 = mini.replace("[0:1,1:2]", "[0:1,1:3]")
ok(L.parse_vertex_sets(mini2)[(7, 1)] == [(0, 1), (1, 3)],
   "a one-digit change to the block changes what the parser returns")
ok(L.parse_vertex_sets(mini2) != pm,
   "and therefore a corruption of the site cannot pass unnoticed")
ok(L.parse_vertex_sets(mini.replace("n=1  [0:1,1:2]", "")) != pm,
   "deleting the line changes what the parser returns")
raises(lambda: L.parse_vertex_sets("nothing here"),
       "parse_vertex_sets raises when there is no T1b2 block at all")
ok(L.parse_vertex_sets(L.T1B2_START + "\n\n" + L.T1B2_END) == {},
   "an empty T1b2 block yields no cells, not invented ones")

# the parser must not read the OLD count table as a set
ok((3, 1) not in vs_old, "the count table is not misread as a set")

# CELL-LOCALITY, swept over all 24.  A parser that returned the right answer
# by reading the wrong line would still pass every assertion above.  For each
# of the 24 cells, corrupt that cell's rendered set on the real target and
# require that (a) the parser's answer changes AT that cell and (b) it changes
# NOWHERE ELSE.  Population: all 24 cells, two assertions each.
for (b, n), verts in sorted(vs_new.items()):
    line = "n=%d  %s" % (n, L.render_set(verts))
    if new_target.count(line) != 1:
        # a rendering that is not unique in the file cannot be corrupted in
        # place unambiguously; anchor it to the beta header instead.
        seg = new_target.split("beta = %d\n" % b, 1)[1]
        pre = new_target.split("beta = %d\n" % b, 1)[0] + "beta = %d\n" % b
        seg = seg.replace(line, line[:-1] + "9", 1)
        cor = pre + seg
    else:
        cor = L.replace_once(new_target, line, line[:-1] + "9")
    got = L.parse_vertex_sets(cor)
    ok(got.get((b, n)) != verts,
       "corrupting beta=%d n=%d changes the parse AT that cell" % (b, n))
    ok(all(got[k] == vs_new[k] for k in vs_new if k != (b, n)),
       "corrupting beta=%d n=%d changes the parse at NO OTHER cell" % (b, n))

# ---------------------------------------------------------------------------
# 3. the old count-table parser
# ---------------------------------------------------------------------------
oc_old = L.parse_vertex_counts_oldform(old_target)
oc_new = L.parse_vertex_counts_oldform(new_target)
ok(len(oc_old) == 24, "the COUNT form is read at all 24 cells of the old target")
ok(oc_new == {}, "the COUNT form is ABSENT from the working-tree target")
ok(oc_old.get((3, 6)) == 4 and oc_old.get((0, 1)) == 1,
   "the old count table reads 4 at beta=3 n=6 and 1 at beta=0 n=1")
ok([oc_old[(0, n)] for n in range(1, 7)] == [1, 1, 2, 2, 3, 3],
   "the old beta=0 row is 1,1,2,2,3,3")

# ---------------------------------------------------------------------------
# 4. the edge/dim parser
# ---------------------------------------------------------------------------
dims_new, edges_new = L.parse_edges(new_target)
dims_old, edges_old = L.parse_edges(old_target)
ok(len(dims_new) == 53, "53 dimension cells read from the new target")
ok(len(dims_old) == 53, "53 dimension cells read from the old target")
ok(dims_new == dims_old,
   "T1b2 (ii)'s dimension cells are IDENTICAL across ed9cde4")
ok(edges_new == edges_old,
   "T1b2 (ii)'s edge cells are IDENTICAL across ed9cde4")
ok(len(edges_new) > 100, "the edge table is populated")
ok(edges_new.get((1, 4, 1, 0)) == 2,
   "the named multiplicity-2 edge [L(4,1):L(3,0)] at beta=1 reads 2")

# ---------------------------------------------------------------------------
# 5. replace_once refuses to lie
# ---------------------------------------------------------------------------
ok(L.replace_once("abcabX", "abX", "abY") == "abcabY", "replace_once replaces")
raises(lambda: L.replace_once("abc", "zzz", "y"),
       "replace_once raises on zero occurrences")
raises(lambda: L.replace_once("abab", "ab", "y"),
       "replace_once raises on two occurrences")
t, nd = L.drop_lines("a\nb\na\n", lambda l: l == "a")
ok((t, nd) == ("b\n", 2), "drop_lines drops exactly the matching lines")

# ---------------------------------------------------------------------------
# 6. run_c1 -- the load-bearing tool
# ---------------------------------------------------------------------------
out_old, rc_old = L.run_c1(old_target)
out_new, rc_new = L.run_c1(new_target)

ok(rc_old == 0, "c1@286d503 against the 286d503 target exits 0")
ok(rc_new == 1, "c1@286d503 against the working-tree target exits 1")
ok(L.totals_of(out_old) == (0, 0, 0), "and reports 0/0/0")
ok(L.totals_of(out_new)[1] == 24, "and 24 findings on the new target")
ok(len(L.findings_of(out_new)) == 24, "24 findings are printed individually")
ok(len(L.findings_of(out_old)) == 0, "no findings are printed on the old")
ok(L.selferrs_of(out_new) == [], "and none of them is a SELF-ERROR")

# it really is the TARGET that decides, not the working tree: hand it the old
# target while the working tree holds the new one, and it goes green.
ok(rc_old == 0 and L.read_worktree(L.TARGET_REL) != old_target,
   "run_c1 reads the target it is handed, not the one on disk")

# c1's own measurement is the same either way -- it does not depend on what it
# could read.
mine_from_old = L.parse_c1_own_vertices(out_old)
mine_from_new = L.parse_c1_own_vertices(out_new)
ok(len(mine_from_old) == 24, "c1's own section (i) is read at all 24 cells")
ok(mine_from_old == mine_from_new,
   "c1's own MEASUREMENT does not depend on the target it is compared against")
ok(mine_from_old.get((3, 6)) == [(0, 1), (1, 5), (2, 9), (3, 5)],
   "c1's own beta=3 n=6 vertex set is [0:1,1:5,2:9,3:5]")

# the committed record
committed = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
ok(out_old == committed,
   "the re-run at 286d503 is byte-identical to the committed out_c1_branching.txt")

# populations
ok(L.compared_of(out_old) == {"vertex counts": 24, "vertex dimensions": 53,
                              "edge multiplicities": 121},
   "the three populations at 286d503 are 24 / 53 / 121")
ok(sum(L.compared_of(out_old).values()) == 198, "and they sum to 198")

# ---------------------------------------------------------------------------
# 7. the corruption harness really moves c1
# ---------------------------------------------------------------------------
# one digit of one edge cell, on the OLD target where the comparison is known
# to be live in every channel
bad = L.replace_once(old_target, "L(5,2) dim 1  ->  [L(4,0)]=0  [L(4,1)]=0  [L(4,2)]=1",
                     "L(5,2) dim 1  ->  [L(4,0)]=0  [L(4,1)]=0  [L(4,2)]=7")
o, rc = L.run_c1(bad)
ok(rc == 1, "a one-digit edge corruption of the old target makes c1 red")
ok(any("disagrees" in f for f in L.findings_of(o)),
   "and it is reported as a disagreement")
o2, rc2 = L.run_c1(old_target)
ok(rc2 == 0, "restoring the target makes c1 green again")

print("assertions: %d, population: every statement above about the parsers, "
      "the git reads, the corruption harness and run_c1" % N)
for b in BAD:
    print("   FAILED: " + b)
print("failures: %d" % len(BAD))
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
