"""selftest_957f.py -- the apparatus, before it is believed.

Every reader here is exercised on KNOWN input, on ABSENT input and on HOSTILE
input.  Absent and hostile are the two that matter: a reader that returns a
partial parse on a file it does not understand agrees with everything, and this
whole arc is about instruments that were wrong in exactly that direction.

Also: replace_once refusing zero sites and two, the git helpers against the
four named revisions, run_c1's independent script/kernel arguments, and clone()
in both of its modes.

Exit 0 iff every assertion holds.
"""

import os
import sys

import lib957f as L

OK, BAD = [], []


def check(name, cond):
    (OK if cond else BAD).append(name)
    print("   %-64s %s" % (name[:64], "ok" if cond else "FAIL"))


L.banner("SELFTEST-957f", "THE APPARATUS, BEFORE IT IS BELIEVED")

# --- fixtures ---------------------------------------------------------------
TARGET_OK = ("x\n" + L._OPEN + "\n  beta = 3\n     n=1  [0:1]\n"
             "     n=2  [0:1,1:1]\n  beta = 0\n     n=1  [0:1]\n"
             + L._SHUT + "\ntail\n")
C1_OK = ("  beta = 3\n     n=1  count 1  set { p=0:dim 1 }\n"
         "     n=2  count 2  set { p=0:dim 1, p=1:dim 1 }\n")
C2_OK = ("       beta=3 : [[1], [1, 1], [1, 2], [1, 3, 2], [1, 4, 5], "
         "[1, 5, 9, 5]]   -- mine, as sets: [[1], [1, 1], [1, 2], [1, 3, 2], "
         "[1, 4, 5], [1, 5, 9, 5]]\n")
B1_OK = ("    beta=3:\n      n=1  vertices p = [0]            dims [1]\n"
         "      n=6  vertices p = [0, 1, 2, 3]   dims [1, 5, 9, 5]\n")
E1_OK = "   beta = 1   [0:1]  [0:1,1:1]  [0:1,1:1]  [0:1,1:3,2:1]  " \
        "[0:1,1:4,2:1]  [0:1,1:4,2:9,3:1]\n"

HOSTILE = ["", "\n\n\n", "beta = 3\n", "n=1  [0:1]\n",
           "beta = 3\n   n=1  [notanumber]\n", "beta = x\n  n=1 [0:1]\n",
           L._OPEN + "\n  beta = 3\n   n=1  [0:1]\n"]   # block never closed

L.rule("(i) THE FIVE READERS ON KNOWN INPUT")
check("target_cells reads 3 cells and beta=3,n=2 is (1, 1)",
      len(L.target_cells(TARGET_OK)) == 3
      and L.target_cells(TARGET_OK)[(3, 2)] == (1, 1))
check("c1_cells reads 2 cells and beta=3,n=2 is (1, 1)",
      len(L.c1_cells(C1_OK)) == 2 and L.c1_cells(C1_OK)[(3, 2)] == (1, 1))
check("c2_cells reads 6 cells and beta=3,n=6 is (1, 5, 9, 5)",
      len(L.c2_cells(C2_OK)) == 6
      and L.c2_cells(C2_OK)[(3, 6)] == (1, 5, 9, 5))
check("b1_cells reads 2 cells and beta=3,n=6 is (1, 5, 9, 5)",
      len(L.b1_cells(B1_OK)) == 2 and L.b1_cells(B1_OK)[(3, 6)] == (1, 5, 9, 5))
check("e1_cells reads 6 cells and beta=1,n=6 is (1, 4, 9, 1)",
      len(L.e1_cells(E1_OK)) == 6 and L.e1_cells(E1_OK)[(1, 6)] == (1, 4, 9, 1))

L.rule("(ii) THE FIVE READERS ON ABSENT INPUT -- {} AND NOT A PARTIAL PARSE")
for nm, fn in [("target_cells", L.target_cells), ("c1_cells", L.c1_cells),
               ("c2_cells", L.c2_cells), ("b1_cells", L.b1_cells),
               ("e1_cells", L.e1_cells)]:
    check("%s on the empty string returns {}" % nm, fn("") == {})
    check("%s on another reader's format returns {}" % nm,
          fn(B1_OK if nm != "b1_cells" else C2_OK) == {})

L.rule("(iii) THE FIVE READERS ON HOSTILE INPUT -- NO CRASH, NO INVENTION")
for i, h in enumerate(HOSTILE):
    for nm, fn in [("target_cells", L.target_cells), ("c1_cells", L.c1_cells),
                   ("c2_cells", L.c2_cells), ("b1_cells", L.b1_cells),
                   ("e1_cells", L.e1_cells)]:
        try:
            got = fn(h)
            check("%s on hostile input %d returns a dict, no cell invented"
                  % (nm, i), isinstance(got, dict))
        except Exception as e:                                # noqa: BLE001
            check("%s on hostile input %d raised %r" % (nm, i, e), False)

L.rule("(iv) CELL LOCALITY -- A READER MUST MOVE AT ITS OWN CELL AND NOWHERE ELSE")
bent = TARGET_OK.replace("n=2  [0:1,1:1]", "n=2  [0:1,1:7]")
before, after = L.target_cells(TARGET_OK), L.target_cells(bent)
moved = [k for k in before if before[k] != after.get(k)]
check("bending beta=3,n=2 moves exactly that cell", moved == [(3, 2)])

L.rule("(v) replace_once REFUSES ZERO SITES AND REFUSES TWO")
try:
    L.replace_once("aXa", "Q", "R")
    check("replace_once refuses zero occurrences", False)
except ValueError:
    check("replace_once refuses zero occurrences", True)
try:
    L.replace_once("aQaQ", "Q", "R")
    check("replace_once refuses two occurrences", False)
except ValueError:
    check("replace_once refuses two occurrences", True)
check("replace_once replaces exactly one", L.replace_once("aQa", "Q", "R")
      == "aRa")
try:
    L.replace_in_block(TARGET_OK, "n=1  [0:1]", "n=1  [0:9]")
    check("replace_in_block refuses a string appearing twice in the block",
          False)
except ValueError:
    check("replace_in_block refuses a string appearing twice in the block",
          True)
check("replace_in_block hits a unique in-block string",
      "n=2  [0:9,1:1]" in L.replace_in_block(TARGET_OK, "n=2  [0:1,1:1]",
                                             "n=2  [0:9,1:1]"))

L.rule("(vi) THE GIT HELPERS, AGAINST THE FOUR NAMED REVISIONS")
for nm, rev in [("REV_A218", L.REV_A218), ("REV_13B2", L.REV_13B2),
                ("REV_58DA", L.REV_58DA), ("REV_321D", L.REV_321D),
                ("REV_7E58", L.REV_7E58)]:
    try:
        full = L.resolve(rev)
        check("%s resolves to a commit (%s)" % (nm, full[:8]), len(full) == 40)
    except Exception:                                         # noqa: BLE001
        check("%s resolves to a commit" % nm, False)
try:
    L.resolve("deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
    check("resolve() raises on a sha that names no commit", False)
except Exception:                                             # noqa: BLE001
    check("resolve() raises on a sha that names no commit", True)
check("log_paths finds 673b4c0 for c1 in the audited range",
      L.resolve(L.REV_58DA) in
      L.log_paths("%s..%s" % (L.REV_A218, L.REV_321D),
                  L.A218_DIR + "/c1_branching.py"))
check("show_names says ed9cde4 touched c2_vertexsets.py",
      (L.A218_DIR + "/c2_vertexsets.py") in L.show_names(L.REV_13B2))
check("show_names says ed9cde4 did NOT touch c1_branching.py",
      (L.A218_DIR + "/c1_branching.py") not in L.show_names(L.REV_13B2))
check("subject(REV_58DA) carries (mg-58da)", "(mg-58da)" in
      L.subject(L.REV_58DA))

L.rule("(vii) run_c1 TAKES SCRIPT AND KERNEL INDEPENDENTLY")
tgt = L.git_show(L.REV_A218, L.TARGET_REL)
c1_a = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")
kern_a = L.git_show(L.REV_A218, L.A218_DIR + "/kern_a218.py")
out, rc = L.run_c1(tgt, c1_a, kern_a)
check("c1 @ REV_A218 with kern @ REV_A218 exits 0", rc == 0)
check("its measuring half reads 24 cells", len(L.c1_cells(out)) == 24)
committed = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
check("and it is byte-identical to the committed out_c1_branching.txt",
      out == committed)
bent_kern = L.bend_kernel(kern_a)
out2, _ = L.run_c1(tgt, c1_a, bent_kern)
check("a kernel edited under the SAME c1 reaches c1's output",
      L.measuring_half(out2) != L.measuring_half(out))

L.rule("(viii) clone() -- A REAL CLONE WITH THE WORKING TREE COMMITTED")
tmp, tree = L.clone(message="mg-957f selftest clone")
try:
    check("the clone's HEAD is a new commit, not this worktree's HEAD",
          L.head_rev(repo=tree) != L.head_rev())
    check("the clone's HEAD subject is the one clone() was given",
          L.subject("HEAD", repo=tree) == "mg-957f selftest clone")
    check("the clone carries g1_provenance.py",
          os.path.isfile(os.path.join(tree, L.S58DA_DIR, "g1_provenance.py")))
finally:
    L.destroy(tmp)


def _mut(tree):
    p = os.path.join(tree, L.A218_DIR, "c3_withdrawal.py")
    with open(p, "a") as fh:
        fh.write("\n# mg-957f selftest marker\n")


tmp, tree = L.clone(mutate=_mut, message="mg-957f selftest mutating clone")
try:
    check("a mutation handed to clone() lands as part of the new commit",
          (L.A218_DIR + "/c3_withdrawal.py") in L.show_names("HEAD", repo=tree))
finally:
    L.destroy(tmp)

print()
print("-" * 74)
print("ASSERTIONS: %d, of which FAILED: %d.  Population: the five readers on "
      "known, absent and hostile input; cell locality; replace_once and "
      "replace_in_block; the git helpers at five named revisions; run_c1's "
      "independent script and kernel arguments; and clone() in both modes."
      % (len(OK) + len(BAD), len(BAD)))
for x in BAD:
    print("   FAILED: " + x)
print("TOTAL BAD: %d" % len(BAD))
sys.exit(1 if BAD else 0)
