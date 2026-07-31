"""k2_selfprov.py -- THE WAYS THIS FIX COULD EXHIBIT THE DEFECT IT REMEDIES.

The defect being repaired is: an apparatus built to answer "where did this come
from" gives a wrong answer ABOUT ITSELF.  A repair for that is another such
apparatus, so it is subject to the same defect, and the only way to know is to
enumerate the branches and check each one.  The list is below.  Where a branch
cannot bite, the reason is stated, because a stated reason is checkable and an
omission is not.

  B1  This repair's own evidence is recorded BEFORE the commit that commits it
      -- which is exactly mg-321d's G-3 against mg-58da.
  B2  g1's new check compares c1's PRINTED measurement.  What is it invariant
      under?  A measurement change that prints nothing.
  B3  g1's check runs on two target forms.  If the two are the same text, or
      drive the same path, the second is one check reported twice.
  B4  g4's attribution derives from `git log <range>`.  The RANGE is a written
      boundary, and a commit outside it is invisible.
  B5  g4's ticket -> commit step reads the commit SUBJECT, which is prose and
      can lie.
  B6  Both new checks could fire on a purpose-built hook rather than on the
      path a real defect takes.
  B7  The repair could weaken the set-level property it was told to preserve.
  B8  The repair's own document could assert figures no instrument reads.
  B9  The repair rewrites committed outputs, which could erase the audit record
      it is answering.

B7 is checked in full by k3 and B8 by k4; both are named here and their verdict
is read from those scripts' committed output rather than restated.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import subprocess
import sys

import lib7e58 as L

R = L.Report("k2", "the 9 branches on which this repair could carry the defect "
                   "it removes, each with a measurement or a stated reason it "
                   "cannot bite")

L.banner("K2", "COULD THIS FIX BE WRONG ABOUT ITS OWN PROVENANCE?")

HEAD = L.head_rev()

# ---------------------------------------------------------------------------
L.rule("B1  DOES THE REPAIR SURVIVE BEING COMMITTED?")
print("""   mg-321d's G-3: mg-58da's committed out_g1_provenance.txt said FINDINGS
   0 and its PREDICTIONS.md said ACTUAL 0 HIT, and both stopped being true the
   instant 673b4c0 landed -- because both were recorded while the change was
   still uncommitted.  Every figure in THIS directory is being recorded under
   exactly the same conditions.

   So it is not argued, it is done: this worktree is cloned, the working tree
   is COMMITTED in the clone, and g1 and g4 are re-run there.  If any figure
   moves, the repair has the defect it is repairing.""")
print()

here = {}
for s in ("g1_provenance.py", "g4_fleet.py"):
    out, rc = L.run_script(L.S58DA_DIR, s)
    here[s] = (L.totals_of(out), rc, sorted(L.findings_of(out)))

tmp, tree = L.scratch_clone(message="mg-7e58: the repair, committed")
try:
    print("   clone HEAD : %s  (this worktree's HEAD is %s)"
          % (L.head_rev(repo=tree)[:8], HEAD[:8]))
    print("   the repair is a COMMIT there, not a working-tree edit.")
    print()
    print("   script                 uncommitted here        committed there")
    for s in ("g1_provenance.py", "g4_fleet.py"):
        out, rc = L.run_script(L.S58DA_DIR, s, repo=tree)
        there = (L.totals_of(out), rc, sorted(L.findings_of(out)))
        (hs, hf), hrc, hfind = here[s]
        (ts, tf), trc, tfind = there
        print("     %-22s self %s find %s exit %d    self %s find %s exit %d  %s"
              % (s, hs, hf, hrc, ts, tf, trc,
                 "SAME" if (hs, hf, hrc) == (ts, tf, trc) else "MOVED"))
        R.check((hs, hf, hrc) == (ts, tf, trc),
                "%s does not survive being committed: uncommitted it is "
                "(self %s, find %s, exit %d) and committed it is (self %s, "
                "find %s, exit %d). That is mg-321d's G-3 reproduced by the "
                "repair for G-3" % (s, hs, hf, hrc, ts, tf, trc))
        R.check(hfind == tfind,
                "%s's finding TEXTS differ between the uncommitted and the "
                "committed tree, even though the counts agree: %s vs %s"
                % (s, hfind, tfind))
finally:
    L.destroy(tmp)
print()
print("   NOT CLAIMED: that no figure anywhere moves.  g1 and g4 both PRINT the")
print("   HEAD sha, and it necessarily differs.  What is checked is that no")
print("   FINDING, SELF-ERROR or EXIT CODE moves -- the channels the exit code")
print("   is derived from, and the ones G-3 was about.")

# ---------------------------------------------------------------------------
L.rule("B2  WHAT IS g1'S NEW COMPARISON INVARIANT UNDER?")
print("""   g1 now decides "did the measuring half move" by diffing c1's printed
   sections (i)+(ii).  So it is blind to a measurement change that prints
   nothing.  THE REASON THAT CANNOT BITE, and it is a fact about c1 rather than
   an assurance: every quantity c1 COMPARES in section (iii) is drawn from the
   two dicts it PRINTS in full in (i)+(ii) -- mine_vertices and mine_edges.
   Printed is therefore a superset of compared, and a measurement change
   invisible to (i)+(ii) cannot move any of the 198 cells either.

   Checked two ways: by reading c1's source for what section (iii) reads, and
   by counting.""")
print()
c1_src = L.git_show(HEAD, L.A218_DIR + "/c1_branching.py")
head, _, tail = c1_src.partition('print("(iii) EVERY CELL, AGAINST')
# What the comparing half INHERITS from the measuring half is the set of
# 'mine_' names it uses without binding: a name it assigns for itself (mine_v,
# mine_c) is a local view of something already inherited, not a second channel
# out of the measurement.  Counting those as inherited is what made this check
# fire on its first run.
bound_tail = set(re.findall(r"^\s*(mine_\w+)\s*=", tail, re.M))
used_tail = set(re.findall(r"\bmine_\w+", tail))
inherited = sorted(used_tail - bound_tail)
printed = sorted(set(re.findall(r"\bmine_\w+", head)))
print("   'mine_' names the comparing half BINDS for itself     : %s"
      % ", ".join(sorted(bound_tail)) or "none")
print("   'mine_' names it inherits from the measuring half     : %s"
      % ", ".join(inherited))
print("   'mine_' names the measuring half PRINTS               : %s"
      % ", ".join(printed))
R.check(bool(inherited) and set(inherited) <= set(printed),
        "c1's comparing half inherits a measured quantity its measuring half "
        "does not print (%s); g1's printed-output comparison is then blind to "
        "a change that could still move the 198 cells"
        % sorted(set(inherited) - set(printed)))

out_g1, _ = L.run_script(L.S58DA_DIR, "g1_provenance.py")
lines125 = re.findall(r"(\d+) lines, c1's own 24 vertex sets", out_g1)
compared = re.findall(r"TOTAL CELLS\s+(\d+)", out_g1)
print()
print("   c1's measuring half, as printed : %s lines"
      % (lines125[0] if lines125 else "?"))
print("   cells c1 compares in (iii)      : %s"
      % (compared[0] if compared else "?"))
R.check(bool(lines125) and bool(compared) and int(compared[0]) == 198,
        "g1 no longer reports 198 compared cells, so this branch's counting "
        "check has nothing to stand on")
print()
print("   RESIDUAL, STATED: a change to c1 that alters neither its printed")
print("   measurement nor its comparison is invisible to g1.  That is correct")
print("   and not a gap -- such a change moves no cell of the reproduction,")
print("   which is the property g1 certifies.")

# ---------------------------------------------------------------------------
L.rule("B3  ARE g1'S TWO TARGET FORMS TWO CHECKS OR ONE REPORTED TWICE?")
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
new_target = L.read_worktree(L.TARGET_REL)
print("   the %s target and the HEAD target are the same text : %s"
      % (L.REV_A218[:8], "YES -- vacuous" if old_target == new_target else "no"))
R.check(old_target != new_target,
        "g1 runs its measurement check on 'both target forms' and the two "
        "texts are identical, so the second is the first reported twice")
print("""   and 'different text' is not yet 'different path'.  g1 does not echo
   c1's stdout, so the form is read by running c1 at HEAD against each target
   here and taking the form off c1's own line.""")


def form_read(target_text):
    """The form c1 says it read, from c1's own output."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="mg7e58-f-")
    try:
        a = os.path.join(tmp, "a218")
        d = os.path.join(tmp, "branching_locate_db09")
        os.makedirs(a)
        os.makedirs(d)
        with open(os.path.join(a, "c1_branching.py"), "w") as fh:
            fh.write(L.git_show(HEAD, L.A218_DIR + "/c1_branching.py"))
        with open(os.path.join(a, "kern_a218.py"), "w") as fh:
            fh.write(L.git_show(HEAD, L.A218_DIR + "/kern_a218.py"))
        with open(os.path.join(d, "out_t1_tl.txt"), "w") as fh:
            fh.write(target_text)
        p = subprocess.run(["python3", "c1_branching.py"], cwd=a,
                           capture_output=True, text=True)
        m = re.search(r"Form read: (\w+)", p.stdout + p.stderr)
        return m.group(1) if m else None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


forms = {}
for tname, ttext in (("the %s target" % L.REV_A218[:8], old_target),
                     ("the HEAD target", new_target)):
    forms[tname] = form_read(ttext)
    print("     %-24s c1 reports  Form read: %s" % (tname, forms[tname]))
seen = {v for v in forms.values() if v}
R.check(len(seen) >= 2,
        "c1 reports reading %s against both targets, so the two forms do not "
        "drive different paths in the comparing half and g1's second run is "
        "the first reported twice" % (sorted(seen) or "nothing"))
if len(seen) >= 2:
    print("   two distinct forms are read, so the two runs are two checks.")

# ---------------------------------------------------------------------------
L.rule("B4  g4'S RANGE IS A WRITTEN BOUNDARY -- WHAT FALLS OUTSIDE IT?")
print("""   `git log 286d5030..HEAD -- <path>` cannot see a commit outside the
   range, and 286d5030 is written into lib58da.py by hand.  Two things are done
   about that rather than asserted away: the endpoints are RESOLVED (a range
   naming a revision that does not exist would silently return nothing), and
   every commit touching each member across ALL of history is listed, so what
   the range excludes is visible instead of merely absent.""")
print()
for name, rev in (("REV_A218", L.REV_A218), ("HEAD", HEAD)):
    try:
        got = L.git("rev-parse", "--verify", rev + "^{commit}").strip()
        print("   %-9s resolves : %s" % (name, got[:12]))
    except subprocess.CalledProcessError:
        R.selferr("%s (%s) does not resolve in this repository" % (name, rev))
print()
print("   member                  in 286d5030..HEAD   before 286d5030   after")
for f in L.FIVE:
    p = L.A218_DIR + "/" + f
    inside = L.commits_touching(p, L.REV_A218, HEAD)
    allc = [h for h in L.git("log", "--format=%H", "--all", "--", p).split() if h]
    outside = [h for h in allc if h not in inside]
    print("     %-22s %-19s %d" % (f, ", ".join(x[:8] for x in inside) or "none",
                                   len(outside)))
R.check(True, "")   # nothing to fail here; the listing is the point
print()
print("   the commits before 286d5030 are the ones that CREATED the five.  They")
print("   are outside the range on purpose -- the question is what moved SINCE")
print("   the reproduction was taken -- and the boundary is named in the output")
print("   rather than implied, which is the whole of what this branch asks.")
print()
print("   AND the in-range answer is cross-checked: g4 gates its own summary")
print("   against its own rows, once per member plus the union.  That gate is")
print("   what would fire if the range dropped an in-range commit; it is")
print("   deletion-tested in B6.")

# ---------------------------------------------------------------------------
L.rule("B5  THE TICKET -> COMMIT STEP READS PROSE")
print("""   g4 labels its attribution rows with the mg-id in each commit's
   SUBJECT.  A subject is prose and can be wrong.  What is load-bearing is the
   member -> commit map, which comes from `git log -- <path>` and never passes
   through a subject; the id is a label on top of it.  Checked: each in-range
   commit carries exactly one id, no two share one, and the id g4 resolves for
   mg-13b2 is the sha lib58da names.""")
print()
range_commits = L.commits_touching(L.A218_DIR, L.REV_A218, HEAD)
ids = {}
for h in range_commits:
    m = re.search(r"\(mg-([0-9a-f]{4})\)\s*$", L.subject(h).strip())
    tid = "mg-" + m.group(1) if m else None
    print("     %s  subject id : %s" % (h[:8], tid or "NONE"))
    if tid is None:
        R.selferr("commit %s carries no (mg-xxxx) id in its subject, so g4's "
                  "ticket label for it cannot be derived" % h[:8])
        continue
    ids.setdefault(tid, []).append(h)
dupes = {k: v for k, v in ids.items() if len(v) > 1}
print()
print("   ids shared by more than one in-range commit : %s"
      % (dupes or "none"))
R.check(not dupes,
        "two in-range commits carry the same mg-id (%s), so g4's ticket -> "
        "commit step is ambiguous and its label could name either" % dupes)
resolved = ids.get("mg-13b2", [None])[0]
print("   mg-13b2 resolves to %s; lib58da names REV_13B2 = %s : %s"
      % (resolved[:8] if resolved else "nothing", L.REV_13B2[:8],
         "agree" if resolved == L.REV_13B2 else "DISAGREE"))
R.check(resolved == L.REV_13B2,
        "the commit whose subject carries (mg-13b2) is %s, but lib58da names "
        "REV_13B2 = %s: the prose route and the written constant disagree"
        % (resolved, L.REV_13B2))

# ---------------------------------------------------------------------------
L.rule("B6  DO THE NEW CHECKS FIRE ON A REAL DEFECT'S PATH?")
print("""   g1's: k1 (iii) makes the mutation to c1_branching.py -- the object g1
   measures -- and never to g1, and runs g1 unmodified and in place.  Its four
   clones and their directions are k1's; the count is read from k1's committed
   output below rather than restated here.

   g4's: the path a real defect takes is A COMMIT LANDING, which is exactly how
   G-2 was born.  So one lands.  A clone gets a real commit that touches
   c3_withdrawal.py, and g4's attribution -- which named c3 nowhere before --
   must pick it up, from git log, with no other change.""")
print()
try:
    with open(os.path.join(L.HERE, "out_k1_grain.txt")) as fh:
        k1out = fh.read()
    m = re.search(r"probes whose direction was predicted correctly : "
                  r"(\d+) of (\d+)", k1out)
    print("   k1's g1 deletion probes, from its committed output : %s of %s"
          % (m.group(1), m.group(2)) if m else "   (not found)")
    if m:
        R.check(m.group(1) == m.group(2),
                "k1 reports %s of %s deletion probes on g1 predicted correctly"
                % (m.group(1), m.group(2)))
except IOError:
    print("   out_k1_grain.txt not present yet (first run); k1 is the gate.")


def add_commit_touching_c3(tree):
    p = os.path.join(tree, L.A218_DIR, "c3_withdrawal.py")
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(src + "\n# mg-7e58 B6 probe: a real commit touching c3\n")


tmp, tree = L.scratch_clone(mutate=add_commit_touching_c3,
                            message="mg-7e58 B6 probe (mg-7e58)")
try:
    out, rc = L.run_script(L.S58DA_DIR, "g4_fleet.py", repo=tree)
    rows = [l.strip() for l in out.splitlines()
            if l.strip().startswith("touches:")]
    print()
    print("   g4's attribution rows in the probe clone:")
    for r in rows:
        print("      %s" % r[:100])
    picked = any("c3_withdrawal.py" in r for r in rows)
    print("   c3_withdrawal.py appears in the attribution : %s"
          % ("YES" if picked else "NO"))
    R.check(picked,
            "a real commit touching c3_withdrawal.py landed and g4's "
            "attribution did not pick it up; the attribution is not derived "
            "from the history after all")
    dis = [x for x in L.findings_of(out) if "disagree" in x and "attribution" in x]
    print("   g4's SUMMARY-vs-ROWS gate reports a disagreement : %s"
          % ("YES -- wrong" if dis else "no"))
    R.check(not dis,
            "g4's summary-vs-rows gate fires on a tree where the summary and "
            "the rows agree: %s" % dis)
finally:
    L.destroy(tmp)

# ---------------------------------------------------------------------------
L.rule("B7 / B8  THE PROPERTY AND THE DOCUMENT -- CHECKED ELSEWHERE, NAMED HERE")
print("""   B7 (did the repair weaken the set-level property?) is k3's whole job:
   five sources, ten pairs, twenty-four cells, all five members re-run.  B8
   (does this repair's own document assert figures?) is k4's: every figure
   gated at its own site against a committed out_k*.txt, each deletion-tested.
   Neither verdict is restated here -- restating it is how a figure becomes an
   assertion -- and run_all.sh runs all four.""")
for name in ("k3_setlevel", "k4_doccheck"):
    p = os.path.join(L.HERE, "out_%s.txt" % name)
    if os.path.exists(p):
        with open(p) as fh:
            body = fh.read()
        s, f = L.totals_of(body)
        print("   %-14s committed output : SELF %s  FINDINGS %s" % (name, s, f))
    else:
        print("   %-14s no committed output yet (first run)" % name)

# ---------------------------------------------------------------------------
L.rule("B9  DOES THE REPAIR ERASE THE RECORD IT IS ANSWERING?")
print("""   This repair regenerates mg-58da's committed out_g*.txt, because
   mg-321d's G-3 is precisely that they no longer reproduce.  It must not touch
   the records that are EVIDENCE: mg-a218's out_c1_branching.txt (the artifact
   g1 confirms byte for byte) and mg-321d's own out_h*.txt (the audit this
   repair answers).  Checked against the blobs, not asserted.""")
print()
FROZEN = [(L.A218_DIR + "/out_c1_branching.txt", L.REV_A218,
           "mg-a218's record, confirmed byte for byte by g1")]
for name in ("h1_questions", "h2_grain", "h3_setlevel", "h4_mine",
             "h5_doccheck", "selftest_321d"):
    FROZEN.append((L.S321D_DIR + "/out_%s.txt" % name, L.REV_321D,
                   "mg-321d's audit record"))
for path, rev, why in FROZEN:
    blob = L.sha(L.git_show(rev, path))
    disk = L.sha(L.read_worktree(path))
    print("     %-52s %s" % (path.split("/")[-1] + " @ " + rev[:8],
                             "IDENTICAL" if blob == disk else "CHANGED"))
    R.check(blob == disk,
            "this repair changed %s, which is %s and must not move" % (path, why))
print()
print("   population: the %d committed records above, each compared against its"
      % len(FROZEN))
print("   own blob at the revision that wrote it.")

sys.exit(R.emit())
