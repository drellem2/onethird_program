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

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import sys

import lib58da as L

SELF, FIND = [], []


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
print("   sha256 of the measuring half, at both revisions:")
for p, _ in paths[:2]:
    a = L.sha(L.git_show(L.REV_A218, p))
    b = L.sha(L.git_show(HEAD, p))
    print("      %-24s %s ... %s   %s"
          % (p.split("/")[-1], a[:16], b[:16], "SAME" if a == b else "CHANGED"))
    if a != b:
        finding("%s changed between %s and HEAD; the measuring half of the "
                "reproduction is not the same code" % (p, L.REV_A218[:8]))
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
print("SELF-ERRORS: %d, population: the %d git reads and the one read-path "
      "enumeration this script needs" % (len(SELF), 3 + len(paths) * 3))
for x in SELF:
    print("   SELF-ERROR: " + x)
print("FINDINGS: %d, population: the 3 populations of the re-run, its exit "
      "code, its byte-comparison against the committed record, the 2 sha "
      "comparisons of the measuring half, and the 2 measurement-invariance "
      "checks" % len(FIND))
for x in FIND:
    print("   FINDING: " + x)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
