"""r1_kernel.py -- OPEN 1.  THE KERNEL HALF OF THE PREDICATE IS BACK.

mg-957f's F-1: g1_provenance.py's file-sha finding covered TWO files --
c1_branching.py and kern_a218.py, the file g1's own section (ii) labels "the
measuring half".  mg-7e58 re-grained the c1 half correctly and DELETED the
kernel half: section (v) took both sides of its comparison through
run_c1(script_rev=REV_A218), which loads the kernel from that revision, so
kern_a218.py was pinned on both sides and a kernel that moved reached neither.

That is coverage going backwards, and it is invisible from the new side.  Every
forward-looking check passed, because the thing that would have complained was
gone.  So this script does not ask "is the repaired g1 green".  It bends
kern_a218.py AS A COMMIT and runs THREE revisions of g1 against that one clone:

  ef388417   g1 before mg-7e58   -- had the kernel, at the FILE grain
  e006581c   g1 before mg-76cc   -- had lost it
  worktree   g1 after mg-76cc    -- has it back, at the MEASUREMENT grain

The middle row is the defect reproduced.  The first and third are what
coverage looks like when it is there.

Everything is a COMMIT.  g1 reads c1 and the kernel with git_show, so a
working-tree bend reaches nothing and comes back silent for the wrong reason --
mg-957f made that mistake and kept it in its predictions.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

import lib76cc as L

R = L.Report(
    selfpop="every git read, clone, subprocess run and parse this script "
            "performs, plus the requirement that each probe really move what "
            "it claims to move",
    findpop="the 3 g1 revisions in the bent-kernel clone (ii), the null clone "
            "(iii), the 4 c1 direction clones (iv), and the 4 per-unit "
            "deletion probes on the units mg-76cc ADDED (v)")

L.banner("R1", "OPEN 1 -- THE KERNEL HALF OF THE PREDICATE")
print("""
The question is not whether the repaired g1 is green.  A predicate that was
removed is green by construction.  The question is what each revision of the
predicate CATCHES, run against the same inputs, and that is the only way this
class is visible at all.
""")

HEAD = L.head_rev()
KERN_HEAD = L.read_worktree(L.KERN_REL)
C1_HEAD = L.read_worktree(L.C1_REL)
TARGET = L.read_worktree(L.TARGET_REL)

L.rule("(i) THE PROBE REALLY MOVES THE MEASUREMENT -- CHECKED BEFORE IT IS USED")
print("""   A corruption probe that corrupts nothing makes every row below say
   whatever it likes.  So kern_a218.py is bent here first, with THIS
   script's own run_c1 -- which takes the script and the kernel as two
   separate sources -- and c1's own vertex cells are counted both ways.""")
print()
out_pin, _ = L.run_c1(TARGET, C1_HEAD, KERN_HEAD)
out_bent, _ = L.run_c1(TARGET, C1_HEAD, L.bend_kernel(KERN_HEAD))
cells_pin = L.c1_own_vertices(out_pin)
cells_bent = L.c1_own_vertices(out_bent)
moved = [k for k in cells_pin if cells_pin[k] != cells_bent.get(k)]
print("   c1 @ HEAD with kern @ HEAD : sections (i)+(ii) sha %s"
      % L.sha(L.measuring_half(out_pin))[:16])
print("   c1 @ HEAD with kern BENT   : sections (i)+(ii) sha %s"
      % L.sha(L.measuring_half(out_bent))[:16])
print("   c1's own vertex cells that move : %d of %d"
      % (len(moved), len(cells_pin)))
R.check(len(cells_pin) == 24,
        "this script's own c1 reader returned %d cells, not 24; every row "
        "below is withdrawn rather than scored" % len(cells_pin))
R.check(len(moved) == 24,
        "the kernel bend moves %d of %d cells, not all 24; it is the probe "
        "that is wrong and nothing below is evidence" % (len(moved),
                                                         len(cells_pin)))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THREE REVISIONS OF g1, ONE CLONE, kern_a218.py BENT AS A COMMIT")
print("""   In this clone c1_branching.py and the target are byte-identical to
   this branch and only kern_a218.py differs -- and it differs as a
   COMMIT.  Each g1 revision is placed beside the repaired one under a
   name of its own, with lib58da AT THE SAME REVISION, so no predicate is
   run against a library it never saw.  g1_provenance.py itself is never
   modified.""")
print()

PINNED = [(L.REV_321D, "g1_pre_mg7e58.py", "before mg-7e58 -- FILE grain"),
          (L.REV_957F, "g1_pre_mg76cc.py", "before mg-76cc -- the hole")]

BENT_FINDINGS = BENT_NAMES_KERN = None
NULL_HITS = NULL_PROBES = None


def _bend(tree):
    p = os.path.join(tree, L.KERN_REL)
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(L.bend_kernel(src))
    for rev, name, _ in PINNED:
        L.install_pinned_g1(tree, rev, name)


def _names_kernel(out):
    return [f for f in L.findings_of(out) if "kern_a218.py" in f]


tmp, tree = L.clone(mutate=_bend,
                    message="mg-76cc probe: bend kern_a218.py (mg-76cc)")
try:
    rows = []
    for rev, name, what in PINNED:
        o, rc = L.run_script(L.S58DA_DIR, name, repo=tree)
        s, f = L.totals_of(o)
        rows.append((rev[:8], what, rc, s, f, _names_kernel(o), o))
    o, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
    s, f = L.totals_of(o)
    rows.append(("worktree", "after mg-76cc -- the repair", rc, s, f,
                 _names_kernel(o), o))

    print("   g1 revision  what it had                     exit self/find  "
          "names kern_a218.py")
    for rev, what, rc, s, f, kern, _o in rows:
        print("     %-10s %-30s %-4s %s/%-5s %s"
              % (rev, what, rc, s, f, "YES" if kern else "no"))
    print()
    for rev, what, rc, s, f, kern, _o in rows:
        for k in kern:
            print("     %s FINDING: %s" % (rev, k[:100]))
            if len(k) > 100:
                print("        ... %s" % k[100:196])
    print()

    pre7e58, pre76cc, post = rows[0], rows[1], rows[-1]
    BENT_FINDINGS = post[4]
    BENT_NAMES_KERN = bool(post[5])

    # The defect, reproduced.  If the middle row is NOT silent the finding
    # mg-957f raised does not exist on this branch and this script says so.
    R.check(bool(pre7e58[5]),
            "g1 at %s does not name kern_a218.py in the bent-kernel clone "
            "either, so there was no coverage to have lost and nothing below "
            "shows anything" % L.REV_321D[:8])
    R.check(not pre76cc[5] and pre76cc[2] == 0,
            "g1 at %s already catches the bent kernel (exit %s, names it %s); "
            "mg-957f's F-1 does not reproduce on this branch and the rest of "
            "this script is withdrawn"
            % (L.REV_957F[:8], pre76cc[2], bool(pre76cc[5])))

    R.gate(post[2] == 1,
           "the REPAIRED g1 exits %s in a clone whose kern_a218.py is bent as "
           "a commit; the kernel half of the predicate is still gone"
           % post[2])
    R.gate(bool(post[5]),
           "the REPAIRED g1 does not name kern_a218.py in a clone whose "
           "kern_a218.py is bent as a commit; whatever it says, it is not "
           "saying which half of the measuring half moved")
    print("   the row that matters: g1 before mg-76cc exits %s and names it %s;"
          % (pre76cc[2], "yes" if pre76cc[5] else "NO"))
    print("   g1 after mg-76cc exits %s and names it %s."
          % (post[2], "YES" if post[5] else "no"))
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE NULL CLONE -- THE REPAIR DID NOT SIMPLY MAKE g1 RED")
print("""   A predicate restored by making it fire on everything is not restored.
   The same clone machinery, no mutation at all.""")
print()
def probe_population(out):
    """(hits, population) off g1's own probe line -- read, not assumed."""
    for line in out.splitlines():
        if "probes whose direction was predicted correctly" in line:
            toks = line.split()
            if len(toks) >= 3 and toks[-1].isdigit() and toks[-3].isdigit():
                return int(toks[-3]), int(toks[-1])
    return None, None


tmp, tree = L.clone(message="mg-76cc probe: null clone (mg-76cc)")
try:
    o, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
    s, f = L.totals_of(o)
    NULL_HITS, NULL_PROBES = probe_population(o)
    print("     unmodified clone, repaired g1        predicted exit 0   "
          "actual exit %s   %s/%s" % (rc, s, f))
    print("     its own direction probes: %s of %s" % (NULL_HITS, NULL_PROBES))
    for x in L.findings_of(o):
        print("       FINDING: %s" % x[:96])
    R.gate(rc == 0 and (s, f) == (0, 0),
           "the repaired g1 exits %s with %s self-errors and %s findings on an "
           "UNMODIFIED clone; the kernel half was restored by making the "
           "predicate fire on the tree as it stands" % (rc, s, f))
    R.check(NULL_PROBES is not None,
            "this script could not read g1's probe population line out of its "
            "stdout; the deletion probes in (v) that rest on it are withdrawn")
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE c1 HALF IS UNDISTURBED -- mg-7e58's OWN 4 DIRECTIONS, RE-RUN")
print("""   Restoring one half of a predicate is a way to break the other.  So
   mg-7e58's four c1 clones are re-run against the REPAIRED g1, with the
   mutation always made to c1_branching.py and always as a commit.""")
print()

C1_CLONES = [("unmodified -- NULL PROBE", None, 0,
              "the tree as it stands"),
             ("c1's vertex DIMENSIONS off by one", L.bend_c1_measure, 1,
              "the measuring half really moved"),
             ("a comment appended to c1", L.comment_c1, 0,
              "the file sha moves and nothing else does"),
             ("a line appended past c1's section (iii)", L.touch_c1_compare, 0,
              "an edit in the COMPARING half -- mg-58da's own class")]

print("   clone                                    predicted  actual  self/find")
nhit = 0
for label, mut, pred_rc, why in C1_CLONES:
    def _m(tree, mut=mut):
        if mut is None:
            return
        p = os.path.join(tree, L.C1_REL)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(mut(src))
    try:
        tmp, tree = L.clone(mutate=_m,
                            message="mg-76cc probe: %s (mg-76cc)" % label)
    except ValueError as e:
        R.selferr("could not build the c1 clone %r (%s); it is DROPPED from "
                  "the population rather than counted as passing"
                  % (label, e))
        continue
    try:
        o, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
        s, f = L.totals_of(o)
        ok = rc == pred_rc
        nhit += ok
        print("     %-40s %-10s %-7s %s/%s   %s"
              % (label[:40], "exit %d" % pred_rc, "exit %s" % rc, s, f,
                 "HIT" if ok else "MISS"))
        print("       why: %s" % why)
        R.gate(ok,
               "the repaired g1 on the c1 clone %r: predicted exit %d, got %s "
               "-- restoring the kernel half moved the c1 half"
               % (label, pred_rc, rc))
    finally:
        L.destroy(tmp)
print()
print("   c1 clones whose direction was predicted correctly: %d of %d"
      % (nhit, len(C1_CLONES)))
print("   population: the 4 clones above.  In each, g1_provenance.py is")
print("   byte-identical to the file on this branch and only c1_branching.py")
print("   differs, as a COMMIT.")
print()

# ---------------------------------------------------------------------------
L.rule("(v) DELETE EACH UNIT mg-76cc ADDED, ONE AT A TIME")
print("""   "The check is there" is a claim about source.  What is measured here
   is what goes away when each added unit is removed ALONE -- three rows
   of section (v)'s two populations, and the one-line repair inside
   measurement() that made either of them able to see the kernel at all.

   The last is the F-1 REINTRODUCTION: put the kernel back on a pin and
   the repaired g1 must go red on its own probe.  A gate that does not
   catch the defect being repaired is a claim, not a gate.

   Each unit is deleted in the tree where its effect EXISTS.  A deletion
   tested in the wrong tree comes back a no-op for a reason that has
   nothing to do with the unit: the kernel PROBE cannot be seen in a
   clone whose kernel is already bent, because g1 cannot build that probe
   there at all and drops it with a self-error either way.""")
print()

# (unit, mutation, bend the kernel too?, what must change)
DELETIONS = [
    ("the kern_a218.py row of HALVES", L.drop_kernel_half, True,
     "no finding may name kern_a218.py", "kernel-half-row"),
    ("the both-together row of HALVES", L.drop_both_half, True,
     "fewer findings than the repaired g1 books in the same clone",
     "both-row"),
    ("the kernel row of PROBES", L.drop_kernel_probe, False,
     "the probe population must shrink", "kernel-probe"),
    ("mg-76cc's one-line repair inside measurement()", L.repin_kernel, False,
     "F-1 REINTRODUCED: g1's own kernel probe must MISS", "repin"),
]

print("   unit deleted                              kernel exit self/find "
      "names probes")
print("                                             bent               "
      "     kern")
for label, mut, bend, expect, tag in DELETIONS:
    def _m(tree, mut=mut, bend=bend):
        p = os.path.join(tree, L.G1_REL)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(mut(src))
        if bend:
            pk = os.path.join(tree, L.KERN_REL)
            with open(pk) as fh:
                ks = fh.read()
            with open(pk, "w") as fh:
                fh.write(L.bend_kernel(ks))
    try:
        tmp, tree = L.clone(mutate=_m,
                            message="mg-76cc deletion: %s (mg-76cc)" % label)
    except ValueError as e:
        R.selferr("could not build the deletion probe %r (%s); it is DROPPED "
                  "from the population rather than counted as passing"
                  % (label, e))
        continue
    try:
        o, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
        s, f = L.totals_of(o)
        kern = _names_kernel(o)
        hits, pop = probe_population(o)
        print("     %-40s %-6s %-4s %s/%-8s %-5s %s of %s"
              % (label[:40], "yes" if bend else "no", rc, s, f,
                 "YES" if kern else "no", hits, pop))
        print("       must change: %s" % expect)
        if tag == "kernel-half-row":
            R.gate(BENT_NAMES_KERN and not kern,
                   "deleting the kern_a218.py row of HALVES is a no-op: g1 "
                   "still names kern_a218.py in the bent-kernel clone, so that "
                   "row is not the unit that names it and the deletion test is "
                   "measuring the wrong thing")
        elif tag == "both-row":
            R.gate(f is not None and BENT_FINDINGS is not None
                   and f < BENT_FINDINGS,
                   "deleting the both-together row of HALVES moves nothing: "
                   "%s findings with it and %s without, in the same clone.  "
                   "Then the conspiracy case was never a check of its own"
                   % (BENT_FINDINGS, f))
        elif tag == "kernel-probe":
            R.gate(pop is not None and NULL_PROBES is not None
                   and pop < NULL_PROBES,
                   "deleting the kernel row of PROBES moves nothing: %s probes "
                   "with it and %s without.  Then it was never in the "
                   "population it is counted in" % (NULL_PROBES, pop))
        elif tag == "repin":
            missed = [x for x in L.findings_of(o)
                      if "kern @ HEAD with dim L(n,p) off by one" in x]
            print("       g1's own kernel probe MISSED: %s"
                  % ("yes" if missed else "NO"))
            R.gate(bool(missed) and rc == 1,
                   "re-pinning the kernel inside measurement() -- which is "
                   "exactly F-1 put back, on an UNMODIFIED tree -- does not "
                   "make g1's own kernel probe MISS (exit %s, probe finding "
                   "%s).  The probe would not have caught F-1 and it will not "
                   "catch its return"
                   % (rc, "present" if missed else "absent"))
    finally:
        L.destroy(tmp)
print()
print("   population: the %d units mg-76cc added or changed in section (v)"
      % len(DELETIONS))
print("   that have a return, a row or a call of their own, each deleted")
print("   ALONE, each in the tree where its effect exists.")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT ON OPEN 1")
print("""   THE KERNEL HALF IS BACK, AND IT IS BACK AT THE MEASUREMENT GRAIN.
   The predicate mg-7e58 removed compared the SHA of two files; what
   replaced it compared the measurement of one.  Section (v) now moves
   each of the two files to HEAD on its own, with the other held at
   %s, and then moves both together -- so the population is two
   again, each half is named, and a cancelling pair cannot pass.

   THAT LAST CLAUSE IS ABOUT SECTION (v) AS A WHOLE and it is true; the
   clause mg-76cc wrote about which ROW catches a cancelling pair was
   backwards and is repaired in mg-69d1.  The two HALF rows are what
   catch a cancelling pair -- both MOVE on one, while `both together`
   prints IDENTICAL.  `both together` is what catches a CONSPIRING pair,
   which passes both halves.  Both are built and measured in
   code/repair_69d1/p3_reason.py.

   It was found by running the pre-repair predicate, and it is confirmed
   by the same means: bend kern_a218.py as a commit, and the repaired
   predicate fires NAMING IT where the predicate it replaces was silent.
""" % L.REV_A218[:8])

sys.exit(R.emit())
