"""r2_kernel_half.py -- k1 RE-RUN, AND THE KERNEL-HALF CONFIRMATION RE-DERIVED.

mg-2c77's OPEN 1 closes with a second instruction: *then re-run k1 and
re-derive the kernel-half confirmation, which is currently unsupported.*  It
is unsupported because of what the drift did to the shape of k1's table and
not merely to its labels.

  THE CONFIRMATION IS A DIFFERENCE BETWEEN TWO COLUMNS.  mg-957f's F-1 was
  that the kernel half of the predicate had been DELETED: bend kern_a218.py
  and the predicate stayed silent.  mg-76cc restored it.  The evidence that
  it is back is that the PRE-repair predicate is SILENT on that bend and the
  REPAIRED one FIRES.

  WITH THE DRIFTED ANCHOR BOTH COLUMNS WERE THE SAME PREDICATE -- mg-76cc's
  repaired g1, differing only in the prose mg-69d1 edited -- so the row read
  `both fire` and could not have shown the difference whatever the truth was.
  0 backwards is what a comparison of a thing with itself always prints.

So this script runs k1 unmodified, and then scores the ONE ROW that carries
the confirmation, at the exit grain and the finding grain, against what each
must read for the confirmation to exist at all.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "branching_audit_e34a"))

import lib8d5e as L                                            # noqa: E402
import libe34a as E                                            # noqa: E402

R = L.Report(
    selfpop="the subprocess runs of k1_prerepair.py and of mg-2c77's q3 and "
            "q4, the parse of k1's anchor "
            "table, its per-input grid, its bucket table and its verdict "
            "block, and the read of its committed transcript",
    findpop="k1's three coverage numbers; its finding SET against the "
            "committed transcript after normalising revisions; the anchor "
            "pair the run states; the kernel-bend row at both grains, which "
            "is the row the kernel-half confirmation IS; and mg-2c77's own "
            "q3 and q4 re-run unmodified, scored for whether A-2's finding "
            "survives and whether the two derivations of `g1 BEFORE mg-76cc` "
            "agree on the FILES")

KERN_BEND = "kern_a218.py: dim L(n,p) one too big"

L.banner("R2", "k1 RE-RUN, AND THE KERNEL-HALF CONFIRMATION RE-DERIVED")
print("""
mg-69d1 re-ran k4_cancel.py from this suite and did not re-run k1.  k1 is the
script whose subject its own commit moved.
""")

# ---------------------------------------------------------------------------
L.rule("(i) k1_prerepair.py, RUN UNMODIFIED")
print("   %s, as a subprocess, nothing edited." % L.K1_REL)
print("   21 pinned g1 runs across 7 clones; several minutes.")
print()
out, rc = L.run_script(L.E34A_DIR, "k1_prerepair.py")
ok = R.check(bool(out.strip()), "k1_prerepair.py produced no output; every "
                                "section below is withdrawn")
print("   exit %d" % rc)
selferrs, findings_n = L.trailer_counts(out)
print("   SELF-ERRORS %s, FINDINGS %s" % (selferrs, findings_n))
print()


def _verdict_number(label):
    for line in out.splitlines():
        s = line.strip()
        if s.startswith(label):
            tail = s.split(":", 1)[1] if ":" in s else ""
            return L._leading_int(tail)
    return None


NUMBERS = [("Backwards at the exit grain", 0),
           ("Backwards at the finding grain", 0),
           ("Files named by an old finding and by no new one", 0)]
print("   %-52s %-8s %s" % ("what k1 measures", "at HEAD", "required"))
for label, want in NUMBERS:
    got = _verdict_number(label)
    print("   %-52s %-8s %-8s %s"
          % (label, got, want, "ok" if got == want else "***"))
    R.check(got is not None,
            "k1's verdict block does not carry %r; the number cannot be read "
            "and the row is withdrawn" % label)
    R.gate(got == want,
           "k1 reports %s = %s where the confirmation requires %s"
           % (label, got, want))
print()
R.check(selferrs == 0,
        "k1 books %s SELF-ERROR(s); its own apparatus is reporting a problem "
        "and its numbers are not yet evidence" % selferrs)

# ---------------------------------------------------------------------------
print()
L.rule("(ii) THE ANCHOR PAIR THE RUN STATES, OUT OF ITS OWN STDOUT")
print("""   A number is only about a revision pair if the run says which pair.
   Read back out of k1's own output rather than from the library this
   script also imports -- two readings of one value that cannot
   disagree are one reading.""")
print()
_stated = [ln.strip() for ln in out.splitlines()
           if "agrees" in ln or "DISAGREES" in ln]
for ln in _stated:
    print("     %s" % ln[:96])
print()
_disagree = [ln for ln in _stated if "DISAGREES" in ln]
R.gate(not _disagree,
       "k1's own anchor table reports %d anchor(s) disagreeing with their "
       "pins: %s" % (len(_disagree), "; ".join(_disagree)))
_pre_stated = ("at %s" % E.PRE_REV[:8]) in out
print("   k1 names %s as the pre-repair predicate : %s"
      % (E.PRE_REV[:8], "yes" if _pre_stated else "NO"))
R.gate(_pre_stated,
       "k1's output does not name %s -- the pinned pre-repair revision -- so "
       "its numbers are not attached to the pair this repair installed"
       % E.PRE_REV[:8])
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE KERNEL-HALF CONFIRMATION, WHICH IS ONE ROW")
print("""   mg-957f's F-1: bend kern_a218.py's dim L(n,p) one too big and the
   predicate says nothing, because the kernel half had been deleted.
   mg-76cc restored it.  The confirmation is not a 0 in a verdict
   block; it is a DIFFERENCE between the two columns on this one
   input:

       the PRE-repair predicate  SILENT
       the REPAIRED predicate    FIRES

   Both are gated.  Under the drifted anchor this row read `both
   fire`, because both columns were the same predicate -- and `both
   fire` is what a comparison of a thing with itself prints whatever
   the truth is.""")
print()


def _grid_cells(label):
    """[rc, self, find] x 3 revisions, out of k1's own (iii) grid row.

    The label occurs on FOUR lines of k1's output -- the input
    declaration in (ii), the grid in (iii), the buckets in (iv) and the
    over-firing table in (v) -- so a row is only the grid row if its first
    nine tokens after the moves-column are each a number or a `-`.  Matching
    on the label alone returns (ii)'s prose and reads every cell as absent,
    which is a parse that fails by agreeing with nothing.
    """
    for line in out.splitlines():
        s = line.strip()
        if not s.startswith(label):
            continue
        toks = s[len(label):].strip().split()
        if toks and toks[0] in ("YES", "no"):
            toks = toks[1:]
        if len(toks) < 9:
            continue
        head = toks[:9]
        if not all(t == "-" or t.isdigit() for t in head):
            continue
        vals = [None if t == "-" else int(t) for t in head]
        return [vals[0:3], vals[3:6], vals[6:9]]
    return None


cells = _grid_cells(KERN_BEND)
R.check(cells is not None,
        "k1's grid has no row starting %r; section (iii) is withdrawn"
        % KERN_BEND)
if cells:
    names = ["before mg-7e58", "BEFORE THIS REPAIR", "this repair"]
    print("     %-22s %-6s %-6s %s" % ("predicate revision", "exit", "self",
                                       "findings"))
    for name, (rc_, s_, f_) in zip(names, cells):
        print("     %-22s %-6s %-6s %s" % (name, rc_, s_, f_))
    print()
    pre_rc, pre_s, pre_f = cells[1]
    new_rc, new_s, new_f = cells[2]
    pre_silent = (pre_rc == 0) and not (pre_f or 0)
    new_fires = (new_rc != 0) and (new_f or 0) > 0
    print("   the PRE-repair predicate is SILENT on the kernel bend : %s"
          % ("YES" if pre_silent else "NO"))
    print("   the REPAIRED predicate FIRES on it                    : %s"
          % ("YES" if new_fires else "NO"))
    print()
    R.gate(pre_silent,
           "the predicate at %s FIRES on the kernel bend (exit %s, findings "
           "%s).  mg-957f's F-1 is that it should be silent there -- the "
           "kernel half was deleted -- so either the pre-repair column is not "
           "the pre-repair predicate or F-1 was never what it was said to be"
           % (E.PRE_REV[:8], pre_rc, pre_f))
    R.gate(new_fires,
           "the repaired predicate does NOT fire on the kernel bend (exit "
           "%s, findings %s); the kernel half is not back and the "
           "confirmation is false" % (new_rc, new_f))
    R.gate(not (pre_silent and new_fires) or cells[1] != cells[2],
           "the two columns read identically on this input, which is what a "
           "comparison of a predicate with itself prints")

    bucket = None
    for line in out.splitlines():
        s = line.strip()
        if s.startswith(KERN_BEND):
            tail = s[len(KERN_BEND):].strip()
            if "fire" in tail or "silent" in tail:
                bucket = " ".join(tail.split())
    print("   k1's own bucket for this input : %s" % (bucket or "not found"))
    R.check(bucket is not None,
            "k1's bucket table has no row for %r; the second grain is "
            "unread" % KERN_BEND)
    if bucket:
        R.gate("new fires, old silent" in bucket,
               "k1 buckets the kernel bend as %r.  The confirmation that the "
               "kernel half is back requires `new fires, old silent` at both "
               "grains" % bucket)
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE FINDING SET, AGAINST THE COMMITTED TRANSCRIPT")
print("""   A count that did not move can still be a different set.  Both
   lists are compared after normalising every hex token of 7 or more
   characters: a revision that moved is not a finding that changed.

   The comparison is against the transcript AS COMMITTED AT HEAD.  This
   repair regenerates that transcript by mg-e34a's own runner, so the
   two agreeing is the point and not an accident -- what would be a
   finding is a difference this repair did not intend.""")
print()
committed = L.git_show("HEAD", L.OUT_K1_REL)
R.check(bool(committed.strip()),
        "k1's committed transcript could not be read at HEAD; section (iv) "
        "is withdrawn")
now_f = [L.normalise_revs(x) for x in L.findings_of(out)]
was_f = [L.normalise_revs(x) for x in L.findings_of(committed)]
print("   findings in this run                 : %d" % len(now_f))
print("   findings in the committed transcript : %d" % len(was_f))
print()
new_only = [x for x in now_f if x not in was_f]
gone = [x for x in was_f if x not in now_f]
for x in now_f:
    print("     [%s] %s" % ("*** NEW" if x in new_only else "also in record",
                            x[:96]))
for x in gone:
    print("     [*** NO LONGER BOOKED] %s" % x[:96])
print()
print("   %d new, %d no longer booked." % (len(new_only), len(gone)))
R.gate(not new_only,
       "this run books %d finding(s) that the committed transcript does not: "
       "%s" % (len(new_only), " | ".join(x[:80] for x in new_only)))
R.gate(not gone,
       "the committed transcript books %d finding(s) this run does not: %s"
       % (len(gone), " | ".join(x[:80] for x in gone)))
print()
print("   AND THE TWO THAT ARE GONE FOR GOOD.  At the pre-repair HEAD k1")
print("   booked two findings saying its own pre-repair revision was not the")
print("   one mg-76cc pinned -- the drift, reported by the drifted")
print("   instrument.  Both are absent from this run because the anchor now")
print("   agrees with lib76cc's pin on the FILES, which k1 (i) checks:")
for line in out.splitlines():
    if "at e006581c vs at" in line:
        print("     %s" % line.strip()[:96])
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE AUDITOR'S OWN INSTRUMENT, RE-RUN UNMODIFIED")
print("""   mg-2c77 raised both sites.  Its own scripts are run here against
   the repaired tree with not one character changed, and what is
   scored is WHICH of its findings survive -- not its verdict, because
   its finding population is wider than this ticket's two open sites.""")
print()
q3out, q3rc = L.run_script("code/audit_2c77", "q3_operands.py")
q4out, q4rc = L.run_script("code/audit_2c77", "q4_prerepair.py")
R.check(bool(q3out.strip()) and bool(q4out.strip()),
        "one of mg-2c77's scripts produced no output; section (v) is "
        "withdrawn")
q3f, q4f = L.findings_of(q3out), L.findings_of(q4out)
print("   %-24s %-8s %s" % ("script", "exit", "findings"))
print("   %-24s %-8s %s" % ("q3_operands.py", q3rc, len(q3f)))
print("   %-24s %-8s %s" % ("q4_prerepair.py", q4rc, len(q4f)))
print()
_census = [f for f in q3f if "WIDER THAN THE ONE IT CLASSIFIES" in f]
print("   A-2's finding -- `THE CENSUS IS STATED OVER A POPULATION WIDER")
print("   THAN THE ONE IT CLASSIFIES` -- is booked by q3 now : %s"
      % ("YES" if _census else "no, it is GONE"))
R.gate(not _census,
       "mg-2c77's own q3 still books the census finding this ticket set out "
       "to close: %s" % (_census[0][:200] if _census else ""))
print()
print("   q3's OTHER findings are mg-2c77's and are NOT this ticket's open")
print("   sites.  Named rather than counted, so `2 remain` cannot read as")
print("   `2 unrepaired`:")
for f in q3f:
    print("      %s" % f[:96])
print()
print("""   AND q4 STILL FIRES, WHICH IS A DEFECT IN THE AUDITOR AND NOT IN
   THE REPAIR.  Its gate is `PRE_REV == lib76cc.REV_957F` -- a
   comparison of REVISION IDENTITY.  The property is FILE identity:
   `e006581c` and the true parent of mg-76cc's repair are different
   commits at which g1_provenance.py and lib58da.py are byte-identical,
   which is what mg-e34a's own design says and what k1 (i) checks.
   Both comparisons are made here so the difference is on the page:""")
print()
_pinned = None
for _line in L.read_worktree("code/branching_repair_76cc/lib76cc.py"
                             ).splitlines():
    if _line.strip().startswith("REV_957F"):
        _pinned = _line.split('"')[1]
R.check(_pinned is not None,
        "lib76cc.REV_957F could not be read; the row below is withdrawn")
if _pinned:
    print("     %-46s %s" % ("lib76cc.REV_957F, the pin", _pinned[:8]))
    print("     %-46s %s" % ("libe34a.PRE_REV, this repair", E.PRE_REV[:8]))
    print("     %-46s %s"
          % ("the same REVISION?", "yes" if _pinned == E.PRE_REV else "NO"))
    for rel in (E.G1_REL, E.LIB_REL):
        same = L.git_show(_pinned, rel) == L.git_show(E.PRE_REV, rel)
        print("     %-46s %s"
              % ("the same FILE -- %s?" % rel.split("/")[-1],
                 "yes" if same else "NO"))
        R.gate(same,
               "%s is not byte-identical at lib76cc's pin %s and at PRE_REV "
               "%s; the two derivations of `g1 BEFORE mg-76cc` disagree about "
               "the file and not merely about the revision"
               % (rel.split("/")[-1], _pinned[:8], E.PRE_REV[:8]))
_selfcontra = [f for f in q4f
               if "moved from %s (mg-76cc's repair) to %s"
               % (E.REPAIR_REV[:8], E.REPAIR_REV[:8]) in f]
print()
print("   q4's own finding text now names THE SAME REVISION on both sides of")
print("   its `moved from X to Y` clause : %s"
      % ("YES -- %s -> %s" % (E.REPAIR_REV[:8], E.REPAIR_REV[:8])
         if _selfcontra else "no"))
print("""
   That is the tell.  A gate whose message says a value moved from a
   revision to itself is not measuring movement; it is measuring
   whether two identifiers are equal, and the identifiers were never
   the property.  It is mg-2c77's instrument and this ticket does not
   edit it -- the same rule applied to every other record here -- but
   it is measured and pointed at rather than left to look like an
   unclosed site.""")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   k1 was re-run unmodified against the repaired anchor.

   Backwards at the exit grain / finding grain / files named : %s / %s / %s
   The kernel bend: pre-repair %s, repaired %s
   Findings, this run against the committed transcript       : %d vs %d
   k1's exit code                                            : %d
"""
      % (_verdict_number("Backwards at the exit grain"),
         _verdict_number("Backwards at the finding grain"),
         _verdict_number("Files named by an old finding and by no new one"),
         "SILENT" if cells and (cells[1][0] == 0 and not (cells[1][2] or 0))
         else "FIRES",
         "FIRES" if cells and cells[2][0] != 0 else "silent",
         len(now_f), len(was_f), rc))
print("""   k1 exits 1 and that is its predicted exit: it books the finding
   about the cancelling pair, which mg-69d1 named as NOT CLOSED and
   which this ticket does not close either.  What changed is that the
   three coverage numbers are now about mg-76cc's repair.""")

sys.exit(R.emit())
