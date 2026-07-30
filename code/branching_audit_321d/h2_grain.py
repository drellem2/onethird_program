"""h2_grain.py -- THE SAME GRAIN ERROR, LOOKED FOR INSIDE THE FIX.

This lineage has produced one error at four grains in one night: scope, extent,
granularity, and now set level.  The repair under audit narrows c1's blind
region.  So the question is whether the NARROWING is at the grain of the
BLINDNESS, or at the grain of some container that happens to hold it.

It is, in c1 itself: the blindness is per CELL and the repair's SELF-ERROR
channel is per cell.  That is checked in h4.

But mg-58da's OWN provenance apparatus is not, and that is what this script
measures.  Two sites, one root:

  g1  asks 'did the measuring half change' and answers it by comparing the
      SHA OF A FILE.  This ticket's own edit changed that file and did not
      change the measurement.
  g4  asks 'which of the five did WHICH COMMIT touch' and answers it by
      comparing committed sha against WORKING-TREE sha.  That expression is
      true for exactly as long as the change is uncommitted.

Both are provenance questions answered at the grain of a container -- a file,
and 'whatever is not yet committed' -- rather than at the grain of the thing
asked about: a measurement, and a commit.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import subprocess
import sys

import lib321d as L

R = L.Report("h2", "the 2 sites of the provenance-grain question -- g1's "
                   "measuring-half check and g4's attribution summary -- and "
                   "the 4 measurements that decide each")

L.banner("H2", "IS THE NARROWING AT THE GRAIN OF THE BLINDNESS?")

HEAD = L.head_rev()
print()
print("   HEAD of this branch : %s" % HEAD)
print("   %s" % L.subject(HEAD)[:96])
print("   the repair under audit IS HEAD : %s" % (HEAD == L.REV_58DA))

# ---------------------------------------------------------------------------
L.rule("(i) THE FILE MOVED.  DID THE MEASUREMENT?")
print("""   c1_branching.py has two halves: it MEASURES the branching graph from
   its own kernel, and it COMPARES that measurement against a file.  mg-58da
   edited the comparing half.  Whether the measuring half moved is not a
   question about the file -- it is a question about the output, and it is
   answered by running both revisions against the SAME target and diffing.""")
print()
a = L.sha(L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py"))
b = L.sha(L.git_show(HEAD, L.A218_DIR + "/c1_branching.py"))
ka = L.sha(L.git_show(L.REV_A218, L.A218_DIR + "/kern_a218.py"))
kb = L.sha(L.git_show(HEAD, L.A218_DIR + "/kern_a218.py"))
print("   FILE GRAIN:")
print("      c1_branching.py  %s ... %s   %s"
      % (a[:16], b[:16], "SAME" if a == b else "CHANGED"))
print("      kern_a218.py     %s ... %s   %s"
      % (ka[:16], kb[:16], "SAME" if ka == kb else "CHANGED"))
print()

old_target = L.git_show(L.REV_A218, L.TARGET_REL)
head_c1 = L.git_show(HEAD, L.A218_DIR + "/c1_branching.py")
out_a, rc_a = L.run_c1(old_target, script_rev=L.REV_A218)
out_b, rc_b = L.run_c1(old_target, script_rev=L.REV_A218, script_text=head_c1)
MARK = "(iii) EVERY CELL, AGAINST"
meas_a = out_a.split(MARK)[0]
meas_b = out_b.split(MARK)[0]
print("   MEASUREMENT GRAIN -- both script revisions, THE SAME target"
      " (@%s):" % L.REV_A218[:8])
print("      sections (i)+(ii), c1 @ %s : sha256 %s"
      % (L.REV_A218[:8], L.sha(meas_a)[:32]))
print("      sections (i)+(ii), c1 @ %s : sha256 %s"
      % (HEAD[:8], L.sha(meas_b)[:32]))
same_meas = meas_a == meas_b
print("      %s -- %d lines"
      % ("BYTE-IDENTICAL" if same_meas else "DIFFER", len(meas_a.splitlines())))
cells_a = L.parse_c1_own_cells(out_a)
cells_b = L.parse_c1_own_cells(out_b)
same_cells = cells_a == cells_b and len(cells_a) == 24
print("      c1's own 24 vertex sets, both revisions : %s"
      % ("all 24 equal" if same_cells else "DIFFER"))
print("      kernel sha across the edit              : %s"
      % ("UNCHANGED" if ka == kb else "CHANGED"))
print()
print("   the two grains give OPPOSITE answers: the file CHANGED, the")
print("   measurement did NOT.  Which one is 'the measuring half of the")
print("   reproduction' is the whole question.")
R.check(same_meas and same_cells,
        "the repair DID move c1's own measurement; then g1's file-grain "
        "finding is right for the wrong reason and this ticket's claim that "
        "no mathematics moved needs re-examining")

# ---------------------------------------------------------------------------
L.rule("(ii) SITE 1 -- g1 ON THE TREE AS COMMITTED")
print("""   g1_provenance.py, run in place, unmodified, at HEAD.  Its committed
   out_g1_provenance.txt reports FINDINGS 0 and PREDICTIONS.md records
   'P2 g1_provenance.py ACTUAL 0 HIT'.  Both were taken before this ticket's
   own commit existed.""")
print()
g1out, g1rc = L.run_in_repo(L.S58DA_DIR, "g1_provenance.py")
gs, gf, gt = L.totals_of(g1out)
print("   live now : SELF-ERRORS %s   FINDINGS %s   exit %d" % (gs, gf, g1rc))
committed_g1 = L.git_show(HEAD, L.S58DA_DIR + "/out_g1_provenance.txt")
cs, cf, ct = L.totals_of(committed_g1)
print("   committed: SELF-ERRORS %s   FINDINGS %s   exit 0 (implied by 0/0)"
      % (cs, cf))
print()
for x in L.findings_of(g1out):
    print("   live FINDING: %s" % x)
print()
predictions = L.git_show(HEAD, L.S58DA_DIR + "/PREDICTIONS.md")
pred_line = [l.strip() for l in predictions.splitlines()
             if l.strip().startswith("P2  g1_provenance.py")]
print("   its own PREDICTIONS.md : %s" % (pred_line[0] if pred_line else "?"))
print()
file_grain = [x for x in L.findings_of(g1out)
              if "c1_branching.py" in x and "measuring half" in x]
if file_grain and same_meas:
    R.finding(
        "g1_provenance.py exits %d on the tree as committed, with a finding "
        "its own section (iv) refutes: it compares c1_branching.py BY FILE "
        "SHA and books any difference as 'the measuring half of the "
        "reproduction is not the same code', but this ticket's edit changed "
        "the comparing half only -- run at both revisions against the same "
        "target, c1's sections (i)+(ii) are byte-identical (%d lines, sha256 "
        "%s) and its own 24 vertex sets are equal, and kern_a218.py -- the "
        "file g1 itself labels 'the measuring half' -- is unchanged. The "
        "provenance question is asked at the grain of a FILE where the "
        "property is about a MEASUREMENT, so the repair trips its own "
        "instrument. The committed out_g1_provenance.txt (FINDINGS 0) and "
        "PREDICTIONS.md ('P2 ... ACTUAL 0 HIT') were both recorded before "
        "this commit existed and neither reproduces at HEAD"
        % (g1rc, len(meas_a.splitlines()), L.sha(meas_a)[:16]))
else:
    print("   g1 does not emit the file-grain finding at HEAD.")
R.check(gf == cf,
        "g1's live FINDINGS (%s) differ from its committed record (%s): the "
        "documented reproduce command does not reproduce the committed output"
        % (gf, cf))

# ---------------------------------------------------------------------------
L.rule("(iii) SITE 2 -- g4'S ATTRIBUTION, BY COMMIT vs BY WORKING TREE")
print("""   g4 answers 'which of the five were touched, and by whom'.  This is
   the exact question this audit's ticket asks.  Its expression is

       if sha@286d5030 != sha@HEAD:      touched_13b2.append(f)
       if sha@HEAD     != sha@worktree:  touched_58da.append(f)

   which attributes by 'is it committed yet', not by commit.  git log
   attributes by commit and cannot drift.""")
print()
FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
        "c4_seam.py", "c5_record.py"]
print("   script                  git log %s..HEAD             sha-diff verdict"
      % L.REV_A218[:8])
truth_13b2, truth_58da = [], []
g4_13b2, g4_58da = [], []
for f in FIVE:
    p = L.A218_DIR + "/" + f
    cs_ = L.commits_touching(p, L.REV_A218, HEAD)
    who = [c[:8] for c in cs_]
    if any(c.startswith(L.REV_13B2[:8]) for c in cs_):
        truth_13b2.append(f)
    if any(c == L.REV_58DA for c in cs_):
        truth_58da.append(f)
    sa = L.sha(L.git_show(L.REV_A218, p))
    sb = L.sha(L.git_show(HEAD, p))
    sc = L.sha(L.read_worktree(p))
    if sa != sb:
        g4_13b2.append(f)
    if sb != sc:
        g4_58da.append(f)
    print("     %-22s  %-26s  %s"
          % (f, ", ".join(who) or "NONE",
             ("13b2" if sa != sb else "") + ("+58da" if sb != sc else "")
             or "none"))
print()
print("   TRUTH, by commit:  ed9cde4 touched %d -- %s"
      % (len(truth_13b2), ", ".join(truth_13b2) or "none"))
print("                      673b4c0 touched %d -- %s"
      % (len(truth_58da), ", ".join(truth_58da) or "none"))
print("   g4's expression :  '13b2'  %d -- %s"
      % (len(g4_13b2), ", ".join(g4_13b2) or "none"))
print("                      '58da'  %d -- %s"
      % (len(g4_58da), ", ".join(g4_58da) or "none"))
print()

g4out, g4rc = L.run_in_repo(L.S58DA_DIR, "g4_fleet.py")
said = {}
for line in g4out.splitlines():
    s_ = line.strip()
    if s_.startswith("of the five, touched by ed9cde4"):
        said["13b2"] = s_.split(":", 1)[1].strip()
    elif s_.startswith("of the five, touched by mg-58da"):
        said["58da"] = s_.split(":", 1)[1].strip()
hdr = [l for l in g4out.splitlines()
       if l.strip().startswith("script") and "->" in l]
print("   what g4 PRINTS, run in place at HEAD:")
print("      ed9cde4 : %s" % said.get("13b2", "(line not found)"))
print("      mg-58da : %s" % said.get("58da", "(line not found)"))
print("      column header : %s" % (hdr[0].strip() if hdr else "(not found)"))
print()
rowline = [l.strip() for l in g4out.splitlines()
           if l.strip().startswith("c1_branching.py") and "CHANGED" in l]
print("   and g4's own ROW for c1_branching.py, which names the commit:")
print("      %s" % (rowline[0] if rowline else "(row not found)"))
print("   BELIEVE THE ROWS: the row names 673b4c00.  The summary attributes")
print("   the same file to ed9cde4.")
print()

wrong = (said.get("13b2", "").split("--")[0].strip() != str(len(truth_13b2))
         or said.get("58da", "").split("--")[0].strip() != str(len(truth_58da)))
if wrong:
    R.finding(
        "g4_fleet.py's set-level attribution is FALSE on the tree as "
        "committed: it says 'touched by ed9cde4 (mg-13b2): %s' and 'touched "
        "by mg-58da: %s', where git log says ed9cde4 touched %d (%s) and "
        "673b4c0 touched %d (%s). c1_branching.py is attributed to a commit "
        "that never touched it. The cause is the same grain error as g1's: "
        "attribution is computed as 'committed sha vs WORKING-TREE sha', "
        "which identifies this ticket's change with 'whatever is not yet "
        "committed' -- true for exactly as long as the change is uncommitted, "
        "and false the instant it lands. g4's own ROW is right (it prints "
        "'CHANGED (673b4c00)' via git log); only the SUMMARY drifts. The "
        "verdict paragraph in section (vii) repeats the false attribution, "
        "and the column header is the hard-coded literal 'd1dd84d2 -> "
        "working' while the column is computed from HEAD = %s"
        % (said.get("13b2"), said.get("58da"), len(truth_13b2),
           ", ".join(truth_13b2) or "none", len(truth_58da),
           ", ".join(truth_58da) or "none", HEAD[:8]))
else:
    print("   g4's attribution agrees with git log.")

sys.exit(R.emit())
