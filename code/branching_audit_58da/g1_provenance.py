"""g1_provenance.py -- QUESTION B, and it is answered by RE-RUNNING.

  Does the 198-cell reproduction still stand?

This is a question about provenance, not about the parser, and it is settled
the cheap way: take mg-a218's c1_branching.py AT THE REVISION WHERE THE
REPRODUCTION WAS TAKEN, hand it the target as it stood at that revision, and
run it.  Whatever it prints is what mg-a218 was entitled to claim.

Then the second half, which is the half that decides whether the claim needs
redoing: did the change touch the path that produced it?  That is not a
judgement call either.  c1 reads exactly one external file.  Either a commit
between the two revisions touched that file or it did not, and `git log` says
which.

REPAIRED BY mg-7e58 (mg-321d finding G-1).  This script used to answer "did the
measuring half change?" by comparing THE SHA OF A FILE, and booked any
difference as "the measuring half of the reproduction is not the same code".
mg-58da's own commit edited c1's COMPARING half, so the file moved and the
measurement did not -- and this script exited 1 on a finding its own section
(iv) refuted.  A provenance apparatus wrong about its own provenance.

The question is now asked at the grain it is about.  "The measuring half" is
not a file; it is what c1 computes before it compares against anything.  So
section (v) RUNS BOTH SCRIPT REVISIONS AGAINST THE SAME TARGET and diffs c1's
sections (i)+(ii) and its own 24 vertex sets.  The file shas are still printed
-- they are facts, and they name which commits are in play -- but they no
longer decide anything.  Section (v) carries a CONTROL: a c1 whose measurement
genuinely moves must make the check fire, and a c1 whose comparing half moves
must not.  The finding was not silenced; its predicate was moved to the grain
of the property, and the new predicate is shown firing.

AND THE POPULATION IS TWO (mg-76cc, on mg-957f's finding F-1).  The predicate
mg-7e58 removed ran over paths[:2] -- c1_branching.py AND kern_a218.py, the
file section (ii) itself labels "the measuring half".  Its first replacement
took both sides of its comparison through run_c1(script_rev=REV_A218), which
loads the kernel from that same revision, so kern_a218.py was pinned at
REV_A218 on both sides and a kernel that moved reached neither.  The c1 half
had been re-grained; the kernel half had been deleted.  Section (v) now moves
EACH HALF ON ITS OWN, with the other held at REV_A218 -- so a finding names
the file that moved -- and then moves the two TOGETHER, because a CONSPIRING
pair passes both halves separately.  Its direction probes run over the same two
files for the same reason.

THE REASON FOR THE `both together` ROW WAS BACKWARDS, AND IS CORRECTED HERE
(mg-69d1, on mg-e34a's E-1).  It read "because a pair of changes that cancel
would pass both halves separately", and that is the one input the row does NOT
catch: build a cancelling pair -- the kernel's dim L(n,p) one too big, c1's
vertex dims one too small -- and both HALF rows MOVE while `both together`
prints IDENTICAL, because the two files' errors restore the printed measurement
exactly.  The halves catch a cancelling pair; this row is the one it passes.
What this row is for is a CONSPIRING pair: each file's change harmless on its
own, the two together moving the measurement.  That input passes both halves
and is caught HERE, by this row and by nothing else.  Both directions are
BUILT and measured in code/repair_69d1/p3_reason.py rather than argued -- a
rationale is a claim, this one names an input, and the input can be built.
The row itself is unchanged and was always right; only its reason was wrong,
because mg-76cc's repair added a ROW and a REASON and only the row was checked.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import sys

import lib58da as L

SELF, FIND = [], []

# The git reads are COUNTED, not written down.  The population line at the
# bottom used to carry the expression `3 + len(paths) * 3`, which was a figure
# written beside the code rather than taken from it: it did not move when
# mg-76cc added the two kernel reads section (v) needs, and it had never
# counted the reads run_c1 makes on this script's behalf.  A declared unit that
# cannot move when its own patch moves is not derived from it.
GITREADS = [0]
_git, _git_show = L.git, L.git_show


def _counted_git(*a, **kw):
    GITREADS[0] += 1
    return _git(*a, **kw)


def _counted_git_show(*a, **kw):
    GITREADS[0] += 1
    return _git_show(*a, **kw)


L.git = _counted_git
L.git_show = _counted_git_show


def selferr(m):
    SELF.append(m)


def finding(m):
    FIND.append(m)


print("=" * 74)
print("G1  QUESTION B -- DOES THE 198-CELL REPRODUCTION STILL STAND?")
print("=" * 74)
print("""
Answered by re-running at the old revision, which is the cheap and decisive
route.  Nothing here is inferred from a diff being 'small' or from the
mathematics being 'untouched': the script is run and its own output is read.
""")

HEAD = L.head_rev()

print("-" * 74)
print("(i) THE REVISION, NAMED")
print("-" * 74)
for rev, what in [(L.REV_A218, "mg-a218 -- where the reproduction was taken"),
                  (L.REV_13B2, "mg-13b2 -- the repair that widened one script"),
                  (HEAD, "HEAD of this branch")]:
    print("   %s  %s" % (rev[:12], what))
    print("      %s" % L.subject(rev)[:96])
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) c1'S READ PATH, FOUND IN ITS SOURCE RATHER THAN ASSUMED")
print("-" * 74)
c1_src = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")
opens = [l.strip() for l in c1_src.splitlines() if "open(" in l]
print("   every open() in c1_branching.py at %s:" % L.REV_A218[:12])
for o in opens:
    print("      %s" % o)
if len(opens) != 1:
    selferr("c1 has %d open() calls; this script assumes the read path is "
            "enumerable and it is not" % len(opens))
print()
print("   the one external file c1 reads:  %s" % L.TARGET_REL)
print()
print("   commits touching each part of the reproduction, %s..%s:"
      % (L.REV_A218[:8], HEAD[:8]))
paths = [(L.A218_DIR + "/c1_branching.py", "the script"),
         (L.A218_DIR + "/kern_a218.py", "its kernel -- the measuring half"),
         (L.TARGET_REL, "the target it compares against -- the read path")]
touched = {}
for p, what in paths:
    cs = L.commits_touching(p, L.REV_A218, HEAD)
    touched[p] = cs
    print("      %-46s %s" % (p.split("/")[-1] + "  (%s)" % what[:22],
                              ", ".join(c[:8] for c in cs) or "NONE"))
print()
print("   sha256 of c1 and its kernel, at both revisions -- REPORTED, and")
print("   NOTHING IS CONCLUDED FROM IT (mg-7e58 / mg-321d G-1: a file sha is")
print("   the wrong grain for the question 'did the measurement move'; that")
print("   is settled by running both revisions, in (v)):")
file_moved = {}
for p, _ in paths[:2]:
    a = L.sha(L.git_show(L.REV_A218, p))
    b = L.sha(L.git_show(HEAD, p))
    file_moved[p] = a != b
    print("      %-24s %s ... %s   %s"
          % (p.split("/")[-1], a[:16], b[:16], "SAME" if a == b else "CHANGED"))
print()

if not touched[L.TARGET_REL]:
    print("   THE CHANGE DID NOT TOUCH THE READ PATH.  The reproduction stands")
    print("   unchanged and needs only re-stating with the revision named.")
    path_touched = False
else:
    print("   THE CHANGE DID TOUCH THE READ PATH: %s."
          % ", ".join(c[:8] for c in touched[L.TARGET_REL]))
    print("   So the reproduction as taken -- c1's measurement against that")
    print("   file -- has to be REDONE against the file as it now stands.")
    print("   That is g2's job.  What g1 settles is what was true at %s."
          % L.REV_A218[:8])
    path_touched = True
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) THE RE-RUN AT %s" % L.REV_A218[:12])
print("-" * 74)
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
out_old, rc_old = L.run_c1(old_target, script_rev=L.REV_A218)
s, f, t = L.totals_of(out_old)
pops = L.compared_of(out_old)
print("   c1_branching.py @ %s, against %s @ %s"
      % (L.REV_A218[:8], L.TARGET_REL.split("/")[-1], L.REV_A218[:8]))
print("      SELF-ERRORS %s   FINDINGS %s   TOTAL BAD %s   exit %d"
      % (s, f, t, rc_old))
for k in ("vertex counts", "vertex dimensions", "edge multiplicities"):
    print("      %-22s %3d cells compared" % (k, pops.get(k, -1)))
print("      %-22s %3d" % ("TOTAL CELLS", sum(pops.values())))
print()

if sum(pops.values()) != 198:
    finding("the re-run at %s compares %d cells, not the 198 mg-a218 claimed"
            % (L.REV_A218[:8], sum(pops.values())))
if (pops.get("vertex counts"), pops.get("vertex dimensions"),
        pops.get("edge multiplicities")) != (24, 53, 121):
    finding("the re-run's three populations are not 24 / 53 / 121: %s" % pops)
if (s, f) != (0, 0):
    finding("the re-run at %s does not reproduce: SELF %s FINDINGS %s"
            % (L.REV_A218[:8], s, f))
if rc_old != 0:
    finding("the re-run at %s exits %d, not 0" % (L.REV_A218[:8], rc_old))

committed = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
print("   against the committed out_c1_branching.txt at that revision:")
print("      re-run   sha256 %s" % L.sha(out_old)[:32])
print("      committed sha256 %s" % L.sha(committed)[:32])
if out_old == committed:
    print("      BYTE-IDENTICAL.  The committed record is what the code does.")
else:
    finding("the re-run at %s is NOT byte-identical to the committed "
            "out_c1_branching.txt" % L.REV_A218[:8])
    a, b = out_old.splitlines(), committed.splitlines()
    print("      DIFFERS: %d vs %d lines" % (len(a), len(b)))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iv) DID THE MEASUREMENT MOVE, OR ONLY THE COMPARISON?")
print("-" * 74)
print("""   c1's output has three parts: (i) its own vertex sets, (ii) its own
   edge table, and (iii) the comparison against the target.  Parts (i) and
   (ii) read nothing outside this instrument.  If they are byte-identical
   across the two runs then no mathematics moved and the whole question is
   about (iii), which is a question about reading.""")
new_target = L.read_worktree(L.TARGET_REL)
out_new, rc_new = L.run_c1(new_target, script_rev=L.REV_A218)
MARK = "(iii) EVERY CELL, AGAINST"
head_old = out_old.split(MARK)[0]
head_new = out_new.split(MARK)[0]
print()
print("   sections (i)+(ii), old-target run : sha256 %s" % L.sha(head_old)[:32])
print("   sections (i)+(ii), new-target run : sha256 %s" % L.sha(head_new)[:32])
if head_old == head_new:
    print("   BYTE-IDENTICAL -- %d lines.  NO MATHEMATICS MOVED."
          % len(head_old.splitlines()))
else:
    finding("c1's own measurement differs between the two runs; the change is "
            "not confined to the comparison")
mine_old = L.parse_c1_own_vertices(out_old)
mine_new = L.parse_c1_own_vertices(out_new)
print("   c1's own 24 vertex sets, both runs, cell by cell: %s"
      % ("all 24 equal" if mine_old == mine_new and len(mine_old) == 24
         else "DIFFER"))
if mine_old != mine_new or len(mine_old) != 24:
    finding("c1's own 24 vertex sets are not identical across the two runs")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(v) DID THE MEASURING HALF MOVE?  ASKED OF THE MEASUREMENT, NOT THE FILE")
print("-" * 74)
print("""   REPAIRED HERE (mg-7e58, on mg-321d's finding G-1).  Section (ii) used
   to book "c1_branching.py's sha changed" as "the measuring half of the
   reproduction is not the same code" and exit 1 on it.  That is a provenance
   question answered at the grain of a FILE.  The property is about a
   MEASUREMENT, and the two grains give opposite answers on this very tree:
   mg-58da edited c1's COMPARING half, so the file moved and the measurement
   did not.

   So it is measured.  Both script revisions are run against THE SAME target
   -- both target forms, because a check run on one form says nothing about
   the other -- and c1's sections (i)+(ii), which read nothing outside the
   instrument, are diffed byte for byte, together with its own 24 vertex sets
   parsed back out of them.

   AND THE MEASURING HALF IS TWO FILES, so the population here is two and each
   is named (mg-76cc, on mg-957f's F-1).  c1_branching.py and kern_a218.py are
   moved to HEAD ONE AT A TIME with the other held at %s, so a finding says
   WHICH file moved the measurement; then both are moved together, because a
   CONSPIRING pair -- each file's change harmless on its own, the two together
   moving the measurement -- passes each half and is caught only here.

   THAT REASON IS CORRECTED, THE ROW IS NOT (mg-69d1, on mg-e34a's E-1).  It
   read "because two changes that cancel would pass each half on its own",
   which names the one input this row does NOT catch.  Built and measured:
   on a CANCELLING pair both HALF rows MOVE and `both together` prints
   IDENTICAL; on a CONSPIRING pair both HALF rows print IDENTICAL and `both
   together` MOVES.  Section (v) as a whole still catches both -- which is
   why the row is load-bearing and was never the thing that was wrong.""" %
      L.REV_A218[:8])
print()
head_c1 = L.git_show(HEAD, L.A218_DIR + "/c1_branching.py")
old_c1 = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")
head_kern = L.git_show(HEAD, L.A218_DIR + "/kern_a218.py")
old_kern = L.git_show(L.REV_A218, L.A218_DIR + "/kern_a218.py")


def measurement(script_src, kern_src, target_text):
    """(sections (i)+(ii) verbatim, c1's own 24 vertex sets) for one run.

    BOTH halves of the measuring half are arguments.  They used to be one:
    run_c1(script_rev=...) took the script and its kernel from the same
    revision and this section passed REV_A218 for it on both sides, which
    pinned kern_a218.py at REV_A218 for every run made here.  A signature that
    cannot express "this script with that kernel" cannot ask the question.
    """
    out, _ = L.run_c1(target_text, script_source=script_src,
                      kernel_source=kern_src)
    return out.split(MARK)[0], L.parse_c1_own_vertices(out)


FORMS = [("the %s target (COUNT form)" % L.REV_A218[:8], old_target),
         ("the HEAD target (SET form)", new_target)]

# The two files section (ii) enumerates as the measuring half, each moved to
# HEAD alone, and then together.  paths[:2] is the same population the deleted
# file-sha predicate ran over -- restored here at the measurement grain.
# The row's LABEL is part of its reason, and it named the case the row does not
# catch (mg-69d1, on mg-e34a's E-1).  `conspiracy` is the case it does catch and
# the only one it catches alone; the (script, kernel) pair the row measures is
# unchanged.
HALVES = [("c1_branching.py", "the script", head_c1, old_kern),
          ("kern_a218.py", "its kernel", old_c1, head_kern),
          ("both together", "conspiracy", head_c1, head_kern)]

print("   target form / half moved to HEAD              @ %s        @ HEAD"
      % L.REV_A218[:8])
moved_on = []
for fname, ftext in FORMS:
    ref_m, ref_v = measurement(old_c1, old_kern, ftext)
    print("     %s -- %d lines at %s"
          % (fname, len(ref_m.splitlines()), L.REV_A218[:8]))
    for hname, hwhat, c1s, ks in HALVES:
        m, v = measurement(c1s, ks, ftext)
        same = m == ref_m and v == ref_v and len(v) == 24
        print("       %-24s %-16s %-16s  %s"
              % (hname + " (%s)" % hwhat, L.sha(ref_m)[:16], L.sha(m)[:16],
                 "IDENTICAL" if same else "MOVED"))
        print("         c1's own 24 vertex sets %s"
              % ("equal" if v == ref_v and len(v) == 24 else "DIFFER"))
        if not same:
            moved_on.append((fname, hname))
print()
print("   the file grain, for contrast -- from (ii), and nothing is concluded")
print("   from it:")
for p, _ in paths[:2]:
    print("     %-24s %s" % (p.split("/")[-1],
                             "CHANGED" if file_moved[p] else "SAME"))
print()
for hname, hwhat, _c1s, _ks in HALVES:
    hit = [f for f, h in moved_on if h == hname]
    if hit:
        finding("c1's own measurement is not the same at %s and at HEAD when "
                "%s is moved and the rest of the measuring half is held at %s "
                "(on %s); the measuring half of the reproduction really is not "
                "the same code and the 198 cells have to be re-taken"
                % (L.REV_A218[:8], hname, L.REV_A218[:8], ", ".join(hit)))
if not moved_on:
    print("   THE FILE MOVED AND THE MEASUREMENT DID NOT.  c1_branching.py's")
    print("   sha differs across the range and its measurement is byte-for-byte")
    print("   the same on both target forms, with kern_a218.py moved alone and")
    print("   with both moved together, so mg-58da's edit is confined to the")
    print("   comparing half and the 198 cells stand as re-run in (iii).")
print()
print("   AND THE CHECK IS SHOWN FIRING -- a check that cannot go red certifies")
print("   nothing, and 'g1 stopped exiting 1' is exactly what silencing it")
print("   would look like.  The probes run over BOTH files of the measuring")
print("   half, one varied at a time, direction predicted first:")
print()


def mutate_measure(src):
    """A regression in the MEASURING half: every simple's dimension off by one.

    This is the shape a real defect takes -- the kernel handing back different
    numbers -- and not a hook planted for the probe to find.
    """
    return L.replace_once(
        src,
        "        mine_vertices[(beta, n)] = algebras[(n, beta)].vertices()",
        "        mine_vertices[(beta, n)] = [(p, d + 1) for p, d in "
        "algebras[(n, beta)].vertices()]")


def mutate_compare(src):
    """An edit confined to the COMPARING half -- the class mg-58da's edit is
    in.  Appended past section (iii), which is where the comparison lives."""
    return src + '\nprint("   [mg-7e58 control: comparing half touched]")\n'


def mutate_kernel(src):
    """The same regression one file down, in kern_a218.py itself.

    vertices() is where c1's numbers come from, and kern_a218.py is the file
    section (ii) labels "the measuring half".  Until mg-76cc no probe here
    touched it, so nothing here could have shown that the kernel was outside
    the check at all.
    """
    return L.replace_once(
        src,
        "        return [(p, self.dim_L(p)) for p in self.parts "
        "if self.dim_L(p) > 0]",
        "        return [(p, self.dim_L(p) + 1) for p in self.parts "
        "if self.dim_L(p) > 0]")


# The probes are built from c1's and the kernel's SOURCE, so they can fail to
# be built -- and an anchor this script could not find is a fact about THIS
# SCRIPT, not a finding against anyone.  It goes to the SELF-ERROR channel and
# the probe is named as dropped, so a shrinking population stays visible.
# (Written this way on mg-7e58's own k1, which ran g1 in a tree whose c1 was
# already mutated and found it raising ValueError instead.)
#
# Each probe varies ONE of the two files and holds the other at REV_A218, which
# is the same shape as the checks above and is what makes a red probe name a
# file.
PROBES = [("c1 @ %s (unmodified -- NULL PROBE)" % HEAD[:8],
           head_c1, old_kern, False, "the tree as it stands; must not fire"),
          ("kern @ %s (unmodified -- NULL PROBE)" % HEAD[:8],
           old_c1, head_kern, False, "the tree as it stands; must not fire")]
for _label, _base, _mut, _which, _pred, _why in [
        ("c1 @ HEAD with the vertex DIMENSIONS off by one", head_c1,
         mutate_measure, "c1", True,
         "the measuring half really moved, in the script; must fire"),
        ("c1 @ HEAD with a line added past section (iii)", head_c1,
         mutate_compare, "c1", False,
         "the file moved, the measurement did not; must not fire"),
        ("kern @ HEAD with dim L(n,p) off by one", head_kern,
         mutate_kernel, "kern", True,
         "the measuring half really moved, in the kernel; must fire")]:
    try:
        _bent = _mut(_base)
    except ValueError as _e:
        selferr("could not build the probe %r out of %s at HEAD (%s); it is "
                "DROPPED from the population below rather than counted as "
                "passing" % (_label, _which, _e))
        continue
    if _which == "c1":
        PROBES.append((_label, _bent, old_kern, _pred, _why))
    else:
        PROBES.append((_label, old_c1, _bent, _pred, _why))

# the baseline the check uses: both halves at REV_A218
ref_m, ref_v = measurement(old_c1, old_kern, new_target)
print("   measuring half varied                            predicted  actual")
nprobe_ok = 0
for pname, psrc, pkern, pred_fires, why in PROBES:
    pm, pv = measurement(psrc, pkern, new_target)
    fires = not (pm == ref_m and pv == ref_v and len(pv) == 24)
    ok = fires == pred_fires
    nprobe_ok += ok
    print("     %-48s %-10s %-8s %s"
          % (pname[:48], "FIRES" if pred_fires else "silent",
             "FIRES" if fires else "silent", "HIT" if ok else "MISS"))
    print("       why: %s" % why)
    if not ok:
        finding("g1's measurement-grain check on %r: predicted %s, got %s -- "
                "the check that replaced the file-sha finding does not "
                "discriminate as claimed"
                % (pname, "fires" if pred_fires else "silent",
                   "fires" if fires else "silent"))
print()
print("   probes whose direction was predicted correctly : %d of %d"
      % (nprobe_ok, len(PROBES)))
print("   population: the %d (c1, kernel) pairs above -- %d over c1 and %d over"
      % (len(PROBES), len([p for p in PROBES if p[2] is old_kern]),
         len([p for p in PROBES if p[2] is not old_kern])))
print("   kern_a218.py -- each run against the HEAD target and diffed against")
print("   c1 @ %s WITH ITS OWN KERNEL on the same target."
      % L.REV_A218[:8])
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("VERDICT ON QUESTION B, derived from the rows above and not asserted")
print("-" * 74)
stands = (s, f) == (0, 0) and sum(pops.values()) == 198 and out_old == committed
print("""   THE 198-CELL REPRODUCTION STANDS AT %s.
   Re-run there just now: 24 vertex-count + 53 vertex-dimension + 121 edge
   cells = %d compared, %s disagreements, exit %d, and the output is
   %s the committed record.
   Re-stated with the revision named, which is what a reproduction needs:

     >> At %s, mg-a218's c1_branching.py -- a third instrument sharing
     >> no code with the two it audits -- measured the branching graph of
     >> TL_n(beta) for beta in {3,2,1,0} and 1 <= n <= 6 and agreed with
     >> mg-e8b8's committed out_t1_tl.txt in all 198 cells.
""" % (L.REV_A218[:12], sum(pops.values()), f, rc_old,
       "byte-identical to" if out_old == committed else "NOT identical to",
       L.REV_A218[:12]))
if not stands:
    finding("the re-run does not reproduce mg-a218's E1 at %s" % L.REV_A218[:8])
print("""   AND IT NEEDS REDOING AT HEAD, because %s touched the read
   path.  The claim above is about a comparison against a FILE, and that
   file was rewritten.  g2 redoes it.
""" % (", ".join(c[:8] for c in touched[L.TARGET_REL]) or "nothing"))
if not path_touched:
    print("   (the read path was NOT touched, so no redoing is needed)")

print("-" * 74)
print("SELF-ERRORS: %d, population: the %d git reads this script and the "
      "re-runs it makes actually performed -- COUNTED, not written -- and the "
      "one read-path enumeration it needs" % (len(SELF), GITREADS[0]))
for x in SELF:
    print("   SELF-ERROR: " + x)
print("FINDINGS: %d, population: the 3 populations of the re-run, its exit "
      "code, its byte-comparison against the committed record, the 2 "
      "measurement-invariance checks across targets in (iv), the %d "
      "measurement-invariance checks across script revisions in (v) -- %d "
      "target forms x the %d halves of the measuring half, which are "
      "c1_branching.py, kern_a218.py and the two together -- and the %d "
      "direction probes on (v)'s own check.  The 2 file-sha comparisons are "
      "REPORTED and are not in this population (mg-7e58 / mg-321d G-1); the "
      "kernel they used to cover is in it at the measurement grain instead "
      "(mg-76cc / mg-957f F-1)"
      % (len(FIND), len(FORMS) * len(HALVES), len(FORMS), len(HALVES),
         len(PROBES)))
for x in FIND:
    print("   FINDING: " + x)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
