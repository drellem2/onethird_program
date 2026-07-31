"""selftest_7e58.py -- this instrument's own apparatus, before it is used.

Every figure k1..k4 report passes through lib7e58's readers, its clone helper
and its corruption helper.  A reader that has quietly gone blind reports
agreement with exactly the confidence of one that works -- which is the whole
subject of this arc -- so the readers are exercised here on input whose answer
is known, on input that is ABSENT, and on input that is HOSTILE: text that
looks like a cell and is not.

Exit 0 iff every assertion holds.  No findings channel: a self-test that has
findings is a self-test that failed.
"""

import os
import sys

import lib7e58 as L

N = 0
BAD = []


def ck(cond, what):
    global N
    N += 1
    if not cond:
        BAD.append(what)


print("=" * 74)
print("SELFTEST  mg-7e58's apparatus, before any of it is believed")
print("=" * 74)
print()

# ---------------------------------------------------------------------------
print("-- the readers, on input whose answer is known ------------------------")
TARGET = L.read_worktree(L.TARGET_REL)
tc = L.target_cells(TARGET)
ck(len(tc) == 24, "target_cells reads 24 cells")
ck(tc[(3, 6)] == (1, 5, 9, 5), "target (3,6) is (1,5,9,5)")
ck(tc[(1, 6)] == (1, 4, 9, 1), "target (1,6) is (1,4,9,1)")
ck(tc[(0, 1)] == (1,), "target (0,1) is (1,)")
ck(set(tc) == set(L.CELLS), "target_cells covers exactly the 24 (beta,n)")

E1 = L.read_worktree("code/branching_audit_d330/out_e1_vertexsets.txt")
ec = L.e1_cells(E1)
ck(len(ec) == 24, "e1_cells reads 24 cells")
ck(ec == tc, "e1 agrees with the target at all 24")

B1 = L.read_worktree("code/branching_audit_2060/out_b1_branching.txt")
bc = L.b1_cells(B1)
ck(len(bc) == 24, "b1_cells reads 24 cells")
ck(bc == tc, "b1 agrees with the target at all 24")

# ---------------------------------------------------------------------------
print("-- the readers, on ABSENCE --------------------------------------------")
for name, fn in (("target_cells", L.target_cells), ("e1_cells", L.e1_cells),
                 ("b1_cells", L.b1_cells), ("c1_cells", L.c1_cells),
                 ("c2_cells", L.c2_cells)):
    ck(fn("") == {}, "%s on empty text returns {}" % name)
    ck(fn("nothing to see here\n" * 20) == {},
       "%s on unrelated text returns {}" % name)
ck(L.target_cells(TARGET.replace(
    "T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT", "XX")) == {},
   "target_cells returns {} when its block header is gone, rather than "
   "falling back to rows elsewhere in the file")

# ---------------------------------------------------------------------------
print("-- the readers, on HOSTILE input --------------------------------------")
HOSTILE = """
T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT
   beta = 3
     n=1  [0:1]
   some prose mentioning n=2  [0:1,1:1] inside a sentence, which is not a row
     n=2  [0:1,1:1]
T1c  SEMISIMPLICITY
"""
h = L.target_cells(HOSTILE)
ck(h == {(3, 1): (1,), (3, 2): (1, 1)},
   "target_cells takes the two real rows and not the one inside prose")
ck(L.target_cells("""
T1b2  THE BRANCHING GRAPH AS VERSHIK-OKOUNKOV DEFINE IT
     n=1  [0:1]
T1c  SEMISIMPLICITY
""") == {}, "a row with no beta header above it is not a cell")
ck(L.b1_cells("    beta=3\n      n=1  vertices p = [0]  dims [1]\n") == {},
   "b1_cells wants the colon its source actually writes")

# ---------------------------------------------------------------------------
print("-- c1_cells and c2_cells, against live output -------------------------")
c1_out, c1_rc = L.run_script(L.A218_DIR, "c1_branching.py")
c2_out, c2_rc = L.run_script(L.A218_DIR, "c2_vertexsets.py")
c1c = L.c1_cells(c1_out)
c2c = L.c2_cells(c2_out)
ck(len(c1c) == 24, "c1_cells reads 24 cells from c1's live output")
ck(len(c2c) == 24, "c2_cells reads 24 cells from c2's live output")
ck(c1c == tc, "c1's own measurement agrees with the target at all 24")
ck(c2c == tc, "c2's own measurement agrees with the target at all 24")
ck(c1_rc == 0, "c1 exits 0 on the repaired tree")
ck(c2_rc == 0, "c2 exits 0 on the repaired tree")

# ---------------------------------------------------------------------------
print("-- cell locality: one corruption must move one cell -------------------")
for beta, n, old, new in [(3, 6, "n=6  [0:1,1:5,2:9,3:5]",
                           "n=6  [0:1,1:5,2:9,3:8]"),
                          (1, 6, "n=6  [0:1,1:4,2:9,3:1]",
                           "n=6  [0:1,1:4,2:9,3:8]")]:
    lines = [l for l in TARGET.splitlines() if l.strip() == old]
    ck(len(lines) >= 1, "the (%d,%d) row is present in the target" % (beta, n))
    if not lines:
        continue
    mutated = TARGET.replace(lines[0], lines[0].replace(old, new), 1)
    got = L.target_cells(mutated)
    moved = [c for c in L.CELLS if got.get(c) != tc.get(c)]
    ck(len(moved) == 1, "corrupting one row moves exactly one cell (%s)" % moved)

# ---------------------------------------------------------------------------
print("-- replace_once refuses to corrupt zero sites or two ------------------")
ck(L.replace_once("a b a", "b", "c") == "a c a", "replace_once replaces the one")
for text, old in (("a a", "a"), ("a", "z")):
    try:
        L.replace_once(text, old, "x")
        ck(False, "replace_once refuses %r in %r" % (old, text))
    except ValueError:
        ck(True, "replace_once refuses %r in %r" % (old, text))

# ---------------------------------------------------------------------------
print("-- totals_of and findings_of ------------------------------------------")
SAMPLE = ("SELF-ERRORS: 2, population: x\n   SELF-ERROR: one\n"
          "FINDINGS: 3, population: y\n   FINDING: alpha\n   FINDING: beta\n"
          "TOTAL BAD: 5\n")
ck(L.totals_of(SAMPLE) == (2, 3), "totals_of reads both channels")
ck(L.findings_of(SAMPLE) == ["alpha", "beta"], "findings_of reads the findings")
ck(L.totals_of("nothing") == (None, None),
   "totals_of says None rather than 0 when the line is absent")
ck(L.findings_of("") == [], "findings_of on empty text is empty")

# ---------------------------------------------------------------------------
print("-- git helpers --------------------------------------------------------")
for rev in (L.REV_A218, L.REV_13B2, L.REV_58DA, L.REV_321D):
    ck(len(L.subject(rev)) > 10, "%s resolves and has a subject" % rev[:8])
ck(L.commits_touching(L.A218_DIR + "/c1_branching.py", L.REV_A218, L.REV_321D)
   == [L.REV_58DA],
   "git log says 673b4c0 and only 673b4c0 touched c1 in the range")
ck(L.commits_touching(L.A218_DIR + "/c2_vertexsets.py", L.REV_A218, L.REV_321D)
   == [L.REV_13B2],
   "git log says ed9cde4 and only ed9cde4 touched c2 in the range")
ck(L.commits_touching(L.A218_DIR + "/c3_withdrawal.py", L.REV_A218,
                      L.REV_321D) == [],
   "no commit in the range touched c3")
ck(L.A218_DIR + "/c2_vertexsets.py" in L.names_in(L.REV_13B2),
   "--name-only agrees that ed9cde4 touched c2")
ck(L.A218_DIR + "/c1_branching.py" not in L.names_in(L.REV_13B2),
   "--name-only agrees that ed9cde4 did NOT touch c1 -- the false attribution "
   "mg-321d's G-2 reports")
ck(L.A218_DIR + "/c1_branching.py" in L.names_in(L.REV_58DA),
   "--name-only agrees that 673b4c0 touched c1")
ck(L.sha("") ==
   "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
   "sha() is sha256")

# ---------------------------------------------------------------------------
print("-- scratch_clone ------------------------------------------------------")
tmp, tree = L.scratch_clone(message="selftest probe")
try:
    ck(os.path.isdir(os.path.join(tree, ".git")), "the clone is a repository")
    ck(L.head_rev(repo=tree) != L.head_rev(),
       "the clone's HEAD is a NEW commit, so the working tree really is "
       "committed there")
    ck(L.subject(L.head_rev(repo=tree), repo=tree) == "selftest probe",
       "the clone's HEAD carries the message it was given")
    ck(L.git("status", "--porcelain", repo=tree).strip() == "",
       "the clone has nothing uncommitted left")
    for rel in (L.S58DA_DIR + "/g1_provenance.py",
                L.S58DA_DIR + "/g4_fleet.py"):
        ck(L.read_worktree(rel, repo=tree) == L.read_worktree(rel),
           "%s crossed into the clone verbatim" % rel.split("/")[-1])
    ck(os.path.isfile(os.path.join(tree, "code/branching_repair_7e58",
                                   "lib7e58.py")),
       "an UNTRACKED file of this new directory crossed too -- the clone would "
       "otherwise be testing a tree without the repair's own instrument")


    def mut(t):
        p = os.path.join(t, L.A218_DIR, "c3_withdrawal.py")
        with open(p, "a") as fh:
            fh.write("\n# selftest probe\n")

finally:
    L.destroy(tmp)
ck(not os.path.exists(tmp), "destroy() removes the clone")

tmp2, tree2 = L.scratch_clone(mutate=mut, message="selftest mutate probe")
try:
    ck(L.A218_DIR + "/c3_withdrawal.py"
       in L.names_in(L.head_rev(repo=tree2), repo=tree2),
       "a mutation passed to scratch_clone lands IN the commit, which is what "
       "makes the g4 attribution probe a real commit and not a dirty file")
finally:
    L.destroy(tmp2)

tmp3, tree3 = L.scratch_clone(carry=False)
try:
    ck(L.read_worktree(L.S58DA_DIR + "/g1_provenance.py", repo=tree3)
       == L.git_show("HEAD", L.S58DA_DIR + "/g1_provenance.py"),
       "carry=False gives the tree AS COMMITTED, which is what the BEFORE "
       "state has to be measured on")
finally:
    L.destroy(tmp3)

# ---------------------------------------------------------------------------
print("-- the Report channels stay apart -------------------------------------")
import contextlib
import io

# emit() prints; it is swallowed here so this file's own totals are the only
# SELF-ERRORS/FINDINGS/TOTAL BAD lines in it.
r = L.Report("probe", "nothing")
with contextlib.redirect_stdout(io.StringIO()):
    empty_rc = r.emit()
    r.selferr("x")
    selferr_rc = r.emit()
ck(empty_rc == 0, "an empty report exits 0")
ck(selferr_rc == 1, "a self-error alone exits 1")
r2 = L.Report("probe", "nothing")
r2.check(False, "boom")
ck(len(r2.findings) == 1 and not r2.self_errors,
   "check(False) books a FINDING and never a self-error")
r3 = L.Report("probe", "nothing")
ck(r3.check(True, "boom") is True and not r3.findings,
   "check(True) books nothing and returns True")

# ---------------------------------------------------------------------------
print()
print("-" * 74)
print("   assertions: %d, population: the readers on known, absent and hostile "
      "input; cell locality; replace_once; the output parsers; the git "
      "helpers against the four named revisions; scratch_clone in its three "
      "modes; and the Report channels" % N)
print("   failures  : %d" % len(BAD))
for b in BAD:
    print("      FAILED: %s" % b)
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
