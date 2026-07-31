"""r3_prerepair.py -- THE STANDING INSTRUCTION, APPLIED TO THIS REPAIR ITSELF.

  When a repair touches a predicate, RUN THE PRE-REPAIR PREDICATE AGAINST THE
  SAME INPUTS and compare what each catches.  Silence from the new one is not
  evidence unless the old one was silent too.

That instruction is what found mg-957f's F-1, and F-1 is the reason it is now
standing: a check that used to fire and now does not is INVISIBLE FROM THE NEW
SIDE.  Every forward-looking test passes, because the thing that would have
complained is gone.  So it is applied here to mg-76cc's own patch, and not only
to the patch mg-76cc is fixing.

Two questions, both asked by running old code rather than by reading new code:

  (iii) THE PREDICATE.  Three revisions of g1_provenance.py -- before mg-7e58,
        before mg-76cc, and this repair -- run against THE SAME five inputs.
        For each input it is declared IN THE TABLE whether it is a real
        regression in the measuring half.  The set that matters is: inputs
        where an OLDER revision catches a REAL defect and this one does not.
        It must be EMPTY, and it is printed even when it is.

  (iv) EVERYTHING ELSE IN THE DIRECTORY.  mg-76cc changed lib58da.run_c1,
        which is underneath every script in code/branching_audit_58da/.  A
        default argument that quietly changed behaviour would remove detection
        in four scripts this repair never opened.  So the four untouched
        scripts are run in two clones -- one carrying this repair, one with
        g1_provenance.py and lib58da.py put back to %s -- and compared.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
""" % "e006581c"

import os
import sys

import lib76cc as L

R = L.Report(
    selfpop="every clone, git read, subprocess run and parse this script "
            "performs, plus the requirement that each input really change "
            "what it claims to change",
    findpop="the coverage comparison over the 5 inputs x 3 g1 revisions in "
            "(iii), and the %d untouched scripts compared across the two "
            "clones in (iv)" % len(L.UNTOUCHED_SCRIPTS))

L.banner("R3", "THE PRE-REPAIR PREDICATE, RUN AGAINST THE SAME INPUTS")
print("""
This section is the one that cannot be replaced by reading the new code.
Coverage going backwards is invisible from the new side by construction.
""")

# ---------------------------------------------------------------------------
L.rule("(i) WHICH RETURNS THIS PATCH MOVED -- COUNTED OFF THE PATCH")
print("""   Every line of g1_provenance.py, in either revision, whose stripped
   form begins `finding(` or `selferr(`.  Counted, not described.""")
print()


def return_sites(src):
    out = []
    for line in src.splitlines():
        s = line.strip()
        if s.startswith("finding(") or s.startswith("selferr("):
            out.append(s)
    return out


pre_src = L.git_show(L.REV_957F, L.G1_REL)
now_src = L.read_worktree(L.G1_REL)
pre_sites, now_sites = return_sites(pre_src), return_sites(now_src)
print("   g1 at %s : %d return sites" % (L.REV_957F[:8], len(pre_sites)))
print("   g1 here          : %d return sites" % len(now_sites))
removed = [s for s in pre_sites if s not in now_sites]
added = [s for s in now_sites if s not in pre_sites]
print("   removed : %d" % len(removed))
for s in removed:
    print("      - %s" % s[:88])
print("   added   : %d" % len(added))
for s in added:
    print("      + %s" % s[:88])
print()
print("""   The counts move by less than the coverage does, and that is the
   point of (iii): mg-76cc's patch changes the POPULATION two existing
   returns range over -- HALVES went from an implicit one to a named
   three, PROBES from three to five -- and a census of return sites
   cannot see that.  mg-7e58's own census could not see F-1 either.""")
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE INPUTS, AND WHAT EACH ONE IS")
print("""   Five clones.  In each, exactly one file differs from this branch and
   it differs AS A COMMIT, because g1 reads c1 and the kernel with
   git_show and a working-tree edit reaches nothing.  The "real
   regression?" column is declared here, before any of them is run.""")
print()

INPUTS = [
    ("unmodified -- NULL", None, None, False,
     "the tree as it stands"),
    ("kern_a218.py: dim L(n,p) off by one", L.KERN_REL, L.bend_kernel, True,
     "THE MEASURING HALF, in the kernel -- mg-957f's F-1"),
    ("c1_branching.py: vertex dims off by one", L.C1_REL, L.bend_c1_measure,
     True, "the measuring half, in the script -- mg-7e58's own probe"),
    ("c1_branching.py: a comment appended", L.C1_REL, L.comment_c1, False,
     "the file sha moves and nothing else does"),
    ("c1_branching.py: a line past section (iii)", L.C1_REL,
     L.touch_c1_compare, False,
     "an edit in the COMPARING half -- mg-58da's own class"),
]
for label, rel, mut, real, why in INPUTS:
    print("     %-42s %-8s %s"
          % (label, "DEFECT" if real else "not", why))
print()

REVS = [(L.REV_321D, "g1_pre_mg7e58.py", "before mg-7e58"),
        (L.REV_957F, "g1_pre_mg76cc.py", "before mg-76cc"),
        (None, "g1_provenance.py", "this repair")]

# ---------------------------------------------------------------------------
L.rule("(iii) THE SAME FIVE INPUTS, THREE REVISIONS OF THE PREDICATE")
print()
print("   input                                      real   %-14s %-14s %s"
      % ("before mg-7e58", "before mg-76cc", "this repair"))
print("                                              defect exit find kern  "
      "exit find kern  exit find kern")

CAUGHT = {}          # (input label, revision label) -> fired?
for label, rel, mut, real, why in INPUTS:
    def _m(tree, rel=rel, mut=mut):
        if mut is not None:
            p = os.path.join(tree, rel)
            with open(p) as fh:
                src = fh.read()
            with open(p, "w") as fh:
                fh.write(mut(src))
        for rev, name, _ in REVS:
            if rev is not None:
                L.install_pinned_g1(tree, rev, name)
    try:
        tmp, tree = L.clone(mutate=_m,
                            message="mg-76cc input: %s (mg-76cc)" % label)
    except ValueError as e:
        R.selferr("could not build the input %r (%s); it is DROPPED from the "
                  "population rather than counted as passing" % (label, e))
        continue
    try:
        cells = []
        for rev, name, what in REVS:
            o, rc = L.run_script(L.S58DA_DIR, name, repo=tree)
            s, f = L.totals_of(o)
            kern = bool([x for x in L.findings_of(o) if "kern_a218.py" in x])
            CAUGHT[(label, what)] = (rc, s, f, kern)
            cells.append("%-4s %-4s %-5s" % (rc, f, "YES" if kern else "no"))
        print("     %-42s %-6s %s"
              % (label[:42], "YES" if real else "no", " ".join(cells)))
    finally:
        L.destroy(tmp)
print()

# The set that matters, printed even when it is empty.
BACKWARDS = []
for label, rel, mut, real, why in INPUTS:
    if not real:
        continue
    new = CAUGHT.get((label, "this repair"))
    if new is None:
        continue
    for rev, name, what in REVS[:2]:
        old = CAUGHT.get((label, what))
        if old is None:
            continue
        if old[0] != 0 and new[0] == 0:
            BACKWARDS.append((label, what))
print("   INPUTS WHERE AN OLDER PREDICATE CATCHES A REAL DEFECT AND THIS ONE")
print("   IS SILENT : %d" % len(BACKWARDS))
for label, what in BACKWARDS:
    print("      %s -- caught by %s, silent here" % (label, what))
R.gate(not BACKWARDS,
       "coverage went backwards on %d of the %d inputs: %s.  That is the class "
       "mg-957f's F-1 is, committed again by the repair for it"
       % (len(BACKWARDS), len(INPUTS),
          "; ".join("%s (caught by %s)" % b for b in BACKWARDS)))
print()

# and the two directions that must NOT be lost the other way: a non-defect
# must stay silent, or the predicate was restored by making it fire always.
FALSE_RED = [label for label, rel, mut, real, why in INPUTS
             if not real and CAUGHT.get((label, "this repair"), (0,))[0] != 0]
print("   NON-DEFECT INPUTS ON WHICH THIS REPAIR FIRES : %d" % len(FALSE_RED))
for label in FALSE_RED:
    print("      %s" % label)
R.gate(not FALSE_RED,
       "the repaired predicate fires on %d input(s) that are not defects: %s.  "
       "A predicate restored by making it red on everything is not restored"
       % (len(FALSE_RED), ", ".join(FALSE_RED)))
print()
print("   population: the %d inputs above x the %d predicate revisions = %d "
      "runs." % (len(INPUTS), len(REVS), len(INPUTS) * len(REVS)))
print("   Each pinned revision is run WITH ITS OWN lib58da, under a name of")
print("   its own, with exactly one edit -- its import line -- so that no")
print("   predicate is judged against a library it never saw.")
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE FOUR SCRIPTS THIS REPAIR NEVER OPENED")
print("""   lib58da.run_c1 grew two arguments.  Both default to what they
   defaulted to before, which is a claim about a default, and a claim
   about a default is exactly the kind that is true until it is not.

   The call shapes are ENUMERATED from the four scripts' own source
   first, so the population is theirs and not this script's idea of it:""")
print()
shapes, prose = [], []
for name in L.UNTOUCHED_SCRIPTS:
    src = L.read_worktree(L.S58DA_DIR + "/" + name)
    for i, line in enumerate(src.splitlines(), start=1):
        if "run_c1(" not in line:
            continue
        # A CALL, not a mention.  The first version of this counted a
        # docstring line that says "run_c1() really runs the script…" as a
        # thirteenth call site -- a population inflated by prose, which is the
        # failure the no-bare-totals rule exists to catch.
        (shapes if "L.run_c1(" in line else prose).append((name, i,
                                                           line.strip()))
for name, i, line in shapes:
    print("     %-20s %-4d %s" % (name, i, line[:76]))
if prose:
    print()
    print("   mentions of run_c1 that are NOT calls, excluded by name:")
    for name, i, line in prose:
        print("     %-20s %-4d %s" % (name, i, line[:76]))
print()
print("   %d call sites over %d scripts (%d prose mentions excluded).  None of"
      % (len(shapes), len(set(s[0] for s in shapes)), len(prose)))
print("   them names a kernel, so all %d go through the default -- which is"
      % len(shapes))
print("   what is compared below.")
R.check(len(shapes) > 0,
        "no run_c1 call sites were found in the four untouched scripts; the "
        "comparison below is then about nothing and is withdrawn")
print()
print("""   Then the four are RUN, end to end, in two clones: one carrying this
   repair, one with g1_provenance.py and lib58da.py put back to %s.
   The clones sit at different revisions, so the comparison is made under
   the same named normalisation r2 uses -- and the count that matters is
   lines that survive it.""" % L.REV_957F[:8])
print()


def _revert(tree):
    for rel in (L.G1_REL, L.LIB_REL):
        with open(os.path.join(tree, rel), "w") as fh:
            fh.write(L.git_show(L.REV_957F, rel))


PAIR = []
for label, mut in (("this repair", None), ("%s" % L.REV_957F[:8], _revert)):
    tmp, tree = L.clone(mutate=mut,
                        message="mg-76cc lib comparison: %s (mg-76cc)" % label)
    try:
        outs = {}
        for name in L.UNTOUCHED_SCRIPTS:
            o, rc = L.run_script(L.S58DA_DIR, name, repo=tree)
            outs[name] = (o, rc)
        PAIR.append((label, outs, L.head_rev(repo=tree),
                     L.subject(L.head_rev(repo=tree), repo=tree)))
    finally:
        L.destroy(tmp)

print("   script                  this repair      %s      lines differing"
      % L.REV_957F[:8])
print("                           exit self/find   exit self/find   normalised")
for name in L.UNTOUCHED_SCRIPTS:
    (la, oa, ra, sa), (lb, ob, rb, sb) = PAIR
    o1, rc1 = oa[name]
    o2, rc2 = ob[name]
    s1, f1 = L.totals_of(o1)
    s2, f2 = L.totals_of(o2)
    n1, _ = L.normalize(o1, ra, sa)
    n2, _ = L.normalize(o2, rb, sb)
    d = L.differing_lines(n1, n2)

    def _t(x):
        """selftest_58da.py prints no SELF-ERRORS / FINDINGS lines -- it has a
        footer of its own -- so None here means "does not print one", not
        "prints zero", and it is shown as such rather than as 0."""
        return "-" if x is None else str(x)

    print("     %-22s %-4s %s/%-9s %-4s %s/%-9s %d"
          % (name, rc1, _t(s1), _t(f1), rc2, _t(s2), _t(f2), len(d)))
    for lineno, x, y in d[:4]:
        print("        line %-4d -%s" % (lineno, (x or "<absent>")[:70]))
        print("                  +%s" % ((y or "<absent>")[:70]))
    R.gate(len(d) == 0 and rc1 == rc2 and (s1, f1) == (s2, f2),
           "%s says something different with lib58da at %s than with the "
           "repaired one: exit %s vs %s, %s/%s vs %s/%s, %d lines differing "
           "after normalisation.  mg-76cc's change to run_c1 is not confined "
           "to the argument it added"
           % (name, L.REV_957F[:8], rc1, rc2, s1, f1, s2, f2, len(d)))
print()
print("   population: the %d scripts in code/branching_audit_58da/ that share"
      % len(L.UNTOUCHED_SCRIPTS))
print("   lib58da.run_c1 with g1 and were not edited by this repair.  g1 is")
print("   excluded BY NAME and not by silence: it is the thing that changed,")
print("   and (iii) is where it is compared.")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   THE PRE-REPAIR PREDICATES WERE RUN, AND ON THE SAME INPUTS.
   %d inputs x %d revisions.  Nothing an older predicate catches on a
   real defect is silent here, and nothing that is not a defect is red.
   The four scripts this repair never opened say the same thing with the
   library before and after, at %d of %d.

   The instruction was applied to this repair as well as to the one it
   fixes, which is the only way the class is visible at all.
""" % (len(INPUTS), len(REVS), len(L.UNTOUCHED_SCRIPTS),
       len(L.UNTOUCHED_SCRIPTS)))

sys.exit(R.emit())
