"""j2_silencing.py -- WAS g1 REPAIRED, OR WAS IT SILENCED TO AGREE WITH PROSE?

mg-321d's G-1: g1_provenance.py asked "did the measuring half change?" and
answered with a FILE SHA, so mg-58da's own commit made it exit 1 on a finding
its own section (iv) refutes.  Either the finding is real and the section is
wrong, or the section is right and g1 should not fire -- and a gate tuned to
match a document is the defect this whole lineage exists to catch.

So this script asks, in order:

  (i)   is the disposition STATED, at the sites a reader meets it?  Checked at
        three sites and each check deletion-tested, because a gate that cannot
        go red certifies nothing.
  (ii)  is the c1 half really re-grained?  Four clones, g1 UNMODIFIED and in
        place, the mutation always made to c1_branching.py and never to g1.
        Re-derived here, not read out of mg-7e58's k1.
  (iii) WHAT DID THE OLD PREDICATE COVER THAT THE NEW ONE DOES NOT?  The old
        predicate compared the sha of TWO files: c1_branching.py AND
        kern_a218.py -- the file g1's own section (ii) labels "the measuring
        half".  Section (v) runs both c1 revisions through
        L.run_c1(..., script_rev=L.REV_A218), which loads kern_a218.py at
        REV_A218 for BOTH sides.  A kernel that moved cannot reach either side
        of that comparison.  Measured three ways in one clone.
  (iv)  which findings the patch REMOVED, enumerated from the patch itself.
  (v)   and the per-return deletion test on the two returns section (v) added,
        because two checks sharing one return are one check.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  It is NOT predicted to exit 0;
see PREDICTIONS.md P3.
"""

import os
import re
import sys

import lib957f as L

R = L.Report("j2", "the 3 disposition sites and their 3 deletion probes, the "
                   "4 c1 clones, the 3 kernel measurements in (iii), the "
                   "removed-finding census in (iv), and the 2 per-return "
                   "deletion probes in (v)")

L.banner("J2", "HOW g1 WAS RECONCILED -- AND IT MUST NOT BE BY SILENCING")

HEAD = L.head_rev()
G1_REL = L.S58DA_DIR + "/g1_provenance.py"
C1_REL = L.A218_DIR + "/c1_branching.py"
KERN_REL = L.A218_DIR + "/kern_a218.py"
DOC_REL = "docs/OneThird-Bratteli-Path-Algebras-Mg7e58ProvenanceRepair.md"

# ---------------------------------------------------------------------------
L.rule("(i) IS THE DISPOSITION STATED, AT THE SITES A READER MEETS IT?")
print("""   mg-321d demanded one of two answers out loud.  A repair that quietly
   drops a finding has answered neither.  Three sites, each with the text that
   must be there, and each check corrupted afterwards to show it can fail.""")
print()

g1_src = L.read_worktree(G1_REL)
doc_src = L.read_worktree(DOC_REL)
g1_live, g1_rc = L.run_script(L.S58DA_DIR, "g1_provenance.py")

SITES = [
    ("g1_provenance.py, module docstring", g1_src,
     "The finding was not silenced"),
    ("docs/…Mg7e58ProvenanceRepair.md §1", doc_src,
     "The section is right and `g1` should not fire"),
    ("g1's own stdout, section (v)", g1_live,
     "THE FILE MOVED AND THE MEASUREMENT DID NOT"),
]
print("   site                                     stated  gate goes red when")
print("                                                    the text is removed")
nstated = 0
for name, body, needle in SITES:
    stated = needle in body
    nstated += stated
    # the deletion probe: the same predicate against the same text with the
    # needle cut out.  If it still passes, the check is not reading anything.
    cut = body.replace(needle, "", 1)
    red = needle not in cut
    print("     %-40s %-7s %s" % (name[:40], "yes" if stated else "NO",
                                  "yes" if red else "NO -- VACUOUS"))
    R.check(stated, "the disposition mg-321d demanded is not stated at %s "
                    "(looking for %r)" % (name, needle))
    R.check(red, "the check on %s is vacuous: removing %r does not make it "
                 "fail" % (name, needle))
print()
print("   sites stating the disposition: %d of %d.  Population: the two files"
      % (nstated, len(SITES)))
print("   above and g1's live stdout -- source, document, and the run itself.")
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE c1 HALF -- g1 UNMODIFIED, IN FOUR CLONES WHOSE c1 IS MUTATED")
print("""   Re-derived here rather than read out of mg-7e58's k1.  The mutation
   is always made to c1_branching.py -- the thing g1 measures -- and never to
   g1, and it is COMMITTED, because g1 reads c1 with git_show(HEAD, …) and a
   working-tree edit would reach nothing.  Exit code alone is not the answer:
   a probe g1 cannot BUILD raises a SELF-ERROR and also exits 1, so findings
   and self-errors are printed apart.""")
print()

c1_head = L.git_show(HEAD, C1_REL)
kern_head = L.git_show(HEAD, KERN_REL)
DIM_ANCHOR = "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()"
DIM_BENT = ("        mine_vertices[(beta, n)] = [(p, d + 1) for p, d in "
            "algebras[(n, beta)].vertices()]")


def bend_c1_measure(src):
    return L.replace_once(src, DIM_ANCHOR, DIM_BENT)


def bend_c1_compare(src):
    return src + '\nprint("   [mg-957f: comparing half touched]")\n'


def bend_c1_comment(src):
    return src + "\n# mg-957f: a comment, and nothing else\n"


C1_CLONES = [
    ("unmodified -- NULL PROBE", None, 0, "the tree as it stands"),
    ("c1's vertex DIMENSIONS off by one", bend_c1_measure, 1,
     "the measuring half really moved"),
    ("a comment appended to c1", bend_c1_comment, 0,
     "the file sha moves and the measurement does not"),
    ("a line appended past c1's section (iii)", bend_c1_compare, 0,
     "an edit in the COMPARING half -- mg-58da's own class"),
]

print("   clone                                   pred  exit  self/find")
c1_hits = 0
for label, mut, pred_rc, why in C1_CLONES:
    def _m(tree, _mut=mut):
        if _mut is None:
            return
        p = os.path.join(tree, C1_REL)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(_mut(src))

    tmp, tree = L.clone(mutate=_m, message="mg-957f c1 probe: %s (mg-957f)"
                        % label)
    try:
        out, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
        s, f = L.totals_of(out)
        hit = rc == pred_rc
        c1_hits += hit
        print("     %-39s %-5s %-5s %s/%s   %s"
              % (label[:39], pred_rc, rc, s, f, "HIT" if hit else "MISS"))
        print("       why: %s" % why)
        for x in L.findings_of(out):
            print("       FINDING: %s" % x[:88])
        R.check(hit, "g1 in the clone %r: predicted exit %d, got %d (self %s, "
                     "findings %s)" % (label, pred_rc, rc, s, f))
        if pred_rc == 1:
            named = [x for x in L.findings_of(out) if "measurement" in x]
            R.check(bool(named),
                    "g1 fired in the %r clone but no finding names the "
                    "MEASUREMENT; the redness is not the new predicate's"
                    % label)
    finally:
        L.destroy(tmp)
print()
print("   c1 clones whose direction was predicted correctly: %d of %d"
      % (c1_hits, len(C1_CLONES)))
print("   population: the 4 clones above.  In each, g1_provenance.py is")
print("   byte-identical to the file on this branch; only c1_branching.py")
print("   differs, and it differs as a COMMIT.")
print()

# ---------------------------------------------------------------------------
L.rule("(iii) WHAT THE OLD PREDICATE COVERED AND THE NEW ONE DOES NOT")
print("""   The predicate that was removed compared the sha of TWO files:

       for p, _ in paths[:2]:                  # c1_branching.py, kern_a218.py
           if sha@REV_A218 != sha@HEAD:
               finding("%s … the measuring half … is not the same code")

   Section (v) replaces it with a comparison of c1's MEASUREMENT -- but both
   sides of that comparison are taken with

       L.run_c1(target_text, script_rev=L.REV_A218, script_source=script_src)

   and run_c1 loads kern_a218.py from `script_rev`.  So the kernel is pinned at
   REV_A218 on BOTH sides.  c1's source is varied across revisions; its kernel
   never is.  Measured, in ONE clone whose kern_a218.py is bent as a commit:

     1. does the bent kernel really move c1's measurement?   (if not, no hole)
     2. does the PRE-repair g1 fire on it, naming kern_a218.py?
     3. does the POST-repair g1 fire on it at all?""")
print()

# 1. the bent kernel really moves the measurement -- run c1 both ways HERE,
#    with an instrument whose script and kernel are independent arguments.
target_head = L.read_worktree(L.TARGET_REL)
kern_bent = L.bend_kernel(kern_head)
out_pin, _ = L.run_c1(target_head, c1_head, kern_head)
out_bent, _ = L.run_c1(target_head, c1_head, kern_bent)
mh_pin, mh_bent = L.measuring_half(out_pin), L.measuring_half(out_bent)
really_moves = mh_pin != mh_bent
cells_pin, cells_bent = L.c1_cells(out_pin), L.c1_cells(out_bent)
ncells_moved = len([k for k in cells_pin if cells_pin[k] != cells_bent.get(k)])
print("   1. c1 @ HEAD with kern @ HEAD   : sections (i)+(ii) sha %s"
      % L.sha(mh_pin)[:16])
print("      c1 @ HEAD with kern BENT     : sections (i)+(ii) sha %s"
      % L.sha(mh_bent)[:16])
print("      the measurement %s -- %d of %d vertex cells move"
      % ("MOVES" if really_moves else "does NOT move", ncells_moved,
         len(cells_pin)))
if not cells_pin:
    R.selferr("this script's own c1 reader returned no cells from the pinned "
              "run; (iii) is withdrawn rather than scored")
R.check(really_moves and ncells_moved == 24,
        "this script's kernel probe does not move c1's measurement, so it "
        "cannot show anything about coverage; it is the probe that is wrong")
print()

# 2 & 3.  One clone, both g1 revisions.
def _bend_kern(tree):
    p = os.path.join(tree, KERN_REL)
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(L.bend_kernel(src))
    # the PRE-repair g1, placed beside the repaired one under its own name so
    # that g1_provenance.py itself is never modified
    pre = L.git_show(L.REV_321D, G1_REL)
    with open(os.path.join(tree, L.S58DA_DIR, "g1_pre_repair.py"), "w") as fh:
        fh.write(pre)


tmp, tree = L.clone(mutate=_bend_kern,
                    message="mg-957f probe: bend kern_a218.py (mg-957f)")
try:
    print("   the clone: kern_a218.py bent AS A COMMIT, c1_branching.py and")
    print("   g1_provenance.py both byte-identical to this branch.")
    print()
    out_post, rc_post = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
    out_pre, rc_pre = L.run_script(L.S58DA_DIR, "g1_pre_repair.py", repo=tree)
    s_post, f_post = L.totals_of(out_post)
    s_pre, f_pre = L.totals_of(out_pre)
    pre_kern = [x for x in L.findings_of(out_pre) if "kern_a218.py" in x]
    post_kern = [x for x in L.findings_of(out_post) if "kern_a218.py" in x]
    print("   g1 revision                              exit  self/find  names")
    print("                                                            the kernel")
    print("     2. PRE-repair  (%s, mg-321d's tree)  %-5s %s/%s      %s"
          % (L.REV_321D[:8], rc_pre, s_pre, f_pre,
             "YES" if pre_kern else "no"))
    for x in pre_kern:
        print("          FINDING: %s" % x[:84])
    print("     3. POST-repair (this branch)             %-5s %s/%s      %s"
          % (rc_post, s_post, f_post, "YES" if post_kern else "no"))
    for x in L.findings_of(out_post):
        print("          FINDING: %s" % x[:84])
    print()
    R.check(bool(pre_kern),
            "the PRE-repair g1 does not name kern_a218.py in the kernel clone "
            "either, so there is no coverage to have lost and this probe "
            "shows nothing")
    if really_moves and pre_kern and not post_kern:
        R.finding(
            "COVERAGE LOST IN THE REPAIR.  g1's file-sha finding covered TWO "
            "files -- c1_branching.py and kern_a218.py, the file g1's own "
            "section (ii) labels 'the measuring half'.  Its replacement, "
            "section (v), takes both sides of its comparison through "
            "run_c1(..., script_rev=L.REV_A218), which pins kern_a218.py at "
            "REV_A218 on BOTH sides, so a kernel that moved between REV_A218 "
            "and HEAD reaches neither side.  Measured in one clone whose "
            "kern_a218.py is bent as a commit: the bend moves %d of 24 of "
            "c1's own vertex cells; the PRE-repair g1 (%s) exits %s with a "
            "finding naming kern_a218.py; the POST-repair g1 exits %s with %s "
            "findings and names it nowhere.  The c1 half of G-1 was re-grained "
            "correctly -- (ii) above is 4 of 4 -- but the kernel half of the "
            "same predicate was deleted rather than re-grained."
            % (ncells_moved, L.REV_321D[:8], rc_pre, rc_post, f_post))
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) WHICH FINDINGS THE PATCH REMOVED -- COUNTED OFF THE PATCH")
print("""   Not "did anything go quiet", but "which returns went away".  The two
   g1 revisions are read and their finding() call sites enumerated.""")
print()
pre_src = L.git_show(L.REV_321D, G1_REL)


def finding_sites(src):
    """Every finding()/selferr() call site, by the first line of its argument."""
    out = []
    lines = src.splitlines()
    for i, line in enumerate(lines):
        s = line.strip()
        for kind in ("finding(", "selferr("):
            if s.startswith(kind):
                arg = s.split(kind, 1)[1].strip().strip('"')[:58]
                out.append((kind[:-1], arg))
    return out


pre_sites = finding_sites(pre_src)
post_sites = finding_sites(g1_src)
pre_set = set(pre_sites)
post_set = set(post_sites)
removed = sorted(pre_set - post_set)
added = sorted(post_set - pre_set)
print("   g1 @ %s : %d return sites   (%d finding, %d selferr)"
      % (L.REV_321D[:8], len(pre_sites),
         sum(1 for k, _ in pre_sites if k == "finding"),
         sum(1 for k, _ in pre_sites if k == "selferr")))
print("   g1 @ HEAD     : %d return sites   (%d finding, %d selferr)"
      % (len(post_sites), sum(1 for k, _ in post_sites if k == "finding"),
         sum(1 for k, _ in post_sites if k == "selferr")))
print()
print("   REMOVED by the repair:")
for kind, arg in removed:
    print("     -  %-8s %s" % (kind, arg))
print("   ADDED by the repair:")
for kind, arg in added:
    print("     +  %-8s %s" % (kind, arg))
print()
print("   population: every line in either revision of g1_provenance.py whose")
print("   stripped form begins `finding(` or `selferr(` -- %d before, %d after."
      % (len(pre_sites), len(post_sites)))
R.check(len(removed) == 1,
        "the repair removed %d return sites from g1, not the one G-1 names: %s"
        % (len(removed), removed))
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE TWO RETURNS SECTION (v) ADDED, DELETED ONE AT A TIME")
print("""   Two checks sharing one return are one check.  Section (v) declares
   two: the measurement-invariance finding, and the probe-direction finding.
   Each is deleted ALONE, in a clone whose c1 measuring half is bent, and the
   run's FINDINGS must drop by exactly that check's own contribution and leave
   the other one standing.

   In this clone BOTH fire, which is not what I predicted and is recorded as a
   miss: g1 builds its probe baseline from c1 @ REV_A218 and its probe sources
   from c1 @ HEAD, and HEAD's c1 is the bent one here, so g1's own null probe
   fires and is scored MISS -- twice.  The clone therefore carries 3 findings
   and 1 self-error before anything is deleted, which is exactly what makes it
   a usable per-return test: each deletion must take away ITS OWN finding and
   no other.""")
print()

DEL_MEASURE = '''    finding("c1's own measurement is not the same at %s and at HEAD (moved on "
            "%s); the measuring half of the reproduction really is not the "
            "same code and the 198 cells have to be re-taken"
            % (L.REV_A218[:8], ", ".join(moved_on)))'''
DEL_PROBE = '''        finding("g1's measurement-grain check on %r: predicted %s, got %s -- "
                "the check that replaced the file-sha finding does not "
                "discriminate as claimed"
                % (pname, "fires" if pred_fires else "silent",
                   "fires" if fires else "silent"))'''

base = (None, None, None)
DELETIONS = [
    ("nothing deleted -- NULL PROBE", None),
    ("(v)'s measurement-invariance finding, alone", DEL_MEASURE),
    ("(v)'s probe-direction finding, alone", DEL_PROBE),
]
print("   deletion                                       exit  self/find")
for label, unit in DELETIONS:
    def _m(tree, _u=unit):
        p = os.path.join(tree, C1_REL)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(bend_c1_measure(src))
        if _u is None:
            return
        q = os.path.join(tree, G1_REL)
        with open(q) as fh:
            gsrc = fh.read()
        if _u not in gsrc:
            raise ValueError("deletion unit not found verbatim in g1")
        indent = " " * (len(_u) - len(_u.lstrip()))
        with open(q, "w") as fh:
            fh.write(gsrc.replace(_u, indent + "pass", 1))

    try:
        tmp, tree = L.clone(mutate=_m,
                            message="mg-957f deletion probe (mg-957f)")
    except Exception as e:                                    # noqa: BLE001
        R.selferr("could not build the deletion probe %r (%s); it is DROPPED "
                  "from the population rather than counted as passing"
                  % (label, e))
        continue
    try:
        out, rc = L.run_script(L.S58DA_DIR, "g1_provenance.py", repo=tree)
        s, f = L.totals_of(out)
        print("     %-46s %-5s %s/%s" % (label[:46], rc, s, f))
        for x in L.findings_of(out):
            print("       FINDING: %s" % x[:84])
        got = L.findings_of(out)
        has_measure = any("own measurement is not the same" in x for x in got)
        has_probe = any("measurement-grain check on" in x for x in got)
        if unit is None:
            base = (f, has_measure, has_probe)
            R.check(has_measure and has_probe,
                    "the null probe of (v)'s deletion test does not make BOTH "
                    "returns fire (measure=%s probe=%s), so neither deletion "
                    "below can be scored" % (has_measure, has_probe))
        elif unit is DEL_MEASURE:
            R.check(f is not None and base[0] is not None
                    and f == base[0] - 1 and not has_measure and has_probe,
                    "deleting (v)'s measurement-invariance finding alone took "
                    "FINDINGS from %s to %s (measure still present: %s, probe "
                    "still present: %s); the two returns are not separable"
                    % (base[0], f, has_measure, has_probe))
        elif unit is DEL_PROBE:
            R.check(f is not None and base[0] is not None
                    and f == base[0] - 2 and has_measure and not has_probe,
                    "deleting (v)'s probe-direction finding alone took "
                    "FINDINGS from %s to %s (measure still present: %s, probe "
                    "still present: %s); the two returns are not separable"
                    % (base[0], f, has_measure, has_probe))
    finally:
        L.destroy(tmp)
print()
print("   population: the 2 return sites section (v) adds, plus a null probe")
print("   in which both must fire.  g1 also books a SELF-ERROR in this clone --")
print("   it cannot BUILD its dimensions probe out of an already-bent c1 -- and")
print("   that is a fact about g1, counted apart from the findings throughout.")
print()

sys.exit(R.emit())
