"""k1_prerepair.py -- THE PRE-REPAIR PREDICATE, RUN AGAINST THE SAME INPUTS.

This is the primary target of this audit and it is the one thing that cannot
be replaced by reading the repaired code.  mg-957f's F-1 -- a repair that
silently REMOVED detection -- was visible only by running the predicate that
the repair replaced.  So the same is done to mg-76cc's own patch.

WHAT IS ASKED, AND AT WHICH GRAIN

  Per input, three buckets, and the third is a finding HOWEVER CORRECT THE
  NEW PREDICATE LOOKS:

      BOTH FIRE        both revisions of g1 report something
      BOTH SILENT      neither does
      OLD FIRES, NEW SILENT     <-- coverage went backwards

  Asked at TWO grains, because they are not the same question:

      the EXIT grain     -- rc != 0.  This is the grain mg-76cc's own r3 used.
      the FINDING grain  -- FINDINGS > 0.  A script can exit 1 on a
                            SELF-ERROR alone: it could not build a probe.
                            That is a fact about the script, not a catch,
                            and at the exit grain it is indistinguishable
                            from one.

  And then at a grain neither r3 nor mg-957f used: WHICH FILE EACH FINDING
  NAMES.  Two predicates that both exit 1 on the same input can still
  disagree about what moved, and no count can see it.  A file named by an old
  finding and by no new one is coverage lost inside a green column.

THE INPUTS ARE mg-76cc'S FIVE PLUS TWO IT DOES NOT HAVE

  * a comment appended to kern_a218.py.  mg-76cc's list has a byte-only
    control for c1_branching.py and none for the kernel -- the file the whole
    repair is about.  A restored half that fires on a comment is not restored.
  * THE CANCELLING PAIR: kern_a218.py's dimensions one too big and
    c1_branching.py's one too small, so the printed measurement is restored
    exactly.  This is the input mg-76cc's own rationale for the `both
    together` row NAMES, and nothing in that repair ever built one.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

import libe34a as L

R = L.Report(
    selfpop="every clone, git read, subprocess run and transcript parse this "
            "script performs, plus the requirement that each input really "
            "change the file it claims to change and that each pinned "
            "revision really differ from the repaired one",
    findpop="the per-input coverage comparison over the inputs x predicate "
            "revisions in (iii), at the exit grain and at the finding grain, "
            "and the file-naming comparison in (iv)")

L.banner("K1", "THE PRE-REPAIR PREDICATE, RUN AGAINST THE SAME INPUTS")
print("""
Coverage that went backwards is invisible from the new side by construction:
every forward-looking test passes, because the thing that would have
complained is gone.  The only way to see it is to run the old predicate.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE TWO PREDICATES, ANCHORED ON THE PROPERTY AND ON A PIN")
print("""   `the predicate before this repair` is a claim about a PROPERTY --
   the kernel half being present in the measurement -- so it is derived
   from the property and not from the file's edit history (mg-8d5e, on
   mg-2c77's OPEN 1).

   It used to be derived from the history: the last commit that touched
   g1_provenance.py, and then its first parent.  mg-69d1 then touched
   g1_provenance.py to correct a SENTENCE, and the anchor followed the
   edit -- both sides of this comparison became mg-76cc's ALREADY
   REPAIRED predicate, with every number below unchanged and every one
   of them about a different pair of revisions.  A literal cannot
   notice that the file moved; a derivation cannot notice that it has
   started measuring something else.  So there are now both, and they
   are COMPARED.""")
print()
print("     %-52s %-9s %-9s %s" % ("anchor", "derived", "pinned", ""))
for label, got, pin, verdict in L.anchor_rows():
    print("     %-52s %-9s %-9s %s" % (label, got[:8], pin[:8], verdict))
print()
for label, got, _pin, _v in L.anchor_rows():
    if not label.startswith("  "):
        print("     %s" % label.split(",")[0])
        print("       %s  %s" % (got[:12], L.subject(got)[:78]))
print()
R.gate(not L.ANCHOR_DRIFT,
       "the anchors this script measures against do not agree with themselves "
       "on %d point(s): %s.  Every row below is about whichever revision pair "
       "the derivation happens to return, and the numbers cannot say which"
       % (len(L.ANCHOR_DRIFT), "; ".join(L.ANCHOR_DRIFT)))
print("   anchors derived and pinned that disagree : %d" % len(L.ANCHOR_DRIFT))
for row in L.ANCHOR_DRIFT:
    print("      *** %s" % row)
print()
print("""   AND THE ANCHOR THAT RE-POINTED, PRINTED RATHER THAN DELETED.  The
   quantity that moved is the evidence, and a repair that removed it
   would leave the next reader with nothing to check the story
   against.  The distance is the number of commits that touched the
   file without touching the property:""")
print()
_drifted = [("the last commit touching g1_provenance.py -- the OLD anchor",
             L.LAST_TOUCHING_G1, L.REPAIR_REV, "mg-76cc's repair"),
            ("its first parent -- the OLD `before this repair`",
             L.resolve(L.LAST_TOUCHING_G1 + "^"), L.PRE_REV,
             "the pre-repair predicate"),
            ("the 2nd-newest commit touching it -- the OLD `before mg-7e58`",
             L.resolve(L.NTH_TOUCHING_1 + "^"), L.PRE_7E58_REV,
             "before mg-7e58")]
print("     %-58s %-9s %-9s %s"
      % ("what the file's history returns", "history", "property", "apart"))
for label, hist, prop, _what in _drifted:
    print("     %-58s %-9s %-9s %d commit(s)"
          % (label, hist[:8], prop[:8],
             L.distance(prop, hist) if L.is_ancestor(prop, hist)
             else L.distance(hist, prop)))
print()
print("   BOTH history anchors moved, and only one of them was named as a")
print("   finding.  `%s` now holds %s, which is mg-76cc's parent under a"
      % ("the 2nd-newest commit", L.resolve(L.NTH_TOUCHING_1 + "^")[:8]))
print("   label that says mg-7e58: an index into a file's history is an")
print("   anchor derived from that history and re-points for the same reason.")
print()

pre_src = L.git_show(L.PRE_REV, L.G1_REL)
now_src = L.read_worktree(L.G1_REL)
R.check(pre_src != now_src,
        "g1 at %s is byte-identical to the one in this worktree; there is no "
        "pre-repair predicate to run and every row below is vacuous"
        % L.PRE_REV[:8])
print("   g1 at %s vs g1 here : %s"
      % (L.PRE_REV[:8], "DIFFER" if pre_src != now_src else "IDENTICAL"))
print("   lib58da at %s vs here : %s"
      % (L.PRE_REV[:8],
         "DIFFER" if L.git_show(L.PRE_REV, L.LIB_REL)
         != L.read_worktree(L.LIB_REL) else "IDENTICAL"))
print()
print("""   mg-76cc wrote e006581c for this revision.  That is a DIFFERENT
   commit from the parent derived above, and the two agree only if
   g1_provenance.py and lib58da.py are byte-identical at both.  Checked,
   because if they are not then mg-76cc ran something other than the
   predicate its patch replaced:""")
MG76CC_SAID = "e006581c2e1185cba3fa58c91a9fd4954bd63eae"
for rel in (L.G1_REL, L.LIB_REL):
    same = L.git_show(MG76CC_SAID, rel) == L.git_show(L.PRE_REV, rel)
    print("     %-24s at e006581c vs at %s : %s"
          % (rel.split("/")[-1], L.PRE_REV[:8],
             "IDENTICAL" if same else "DIFFER"))
    R.gate(same,
           "%s is not the same at e006581c -- the revision mg-76cc pinned as "
           "`g1 BEFORE mg-76cc` -- as at %s, the actual parent of the repair; "
           "the pre-repair predicate mg-76cc ran is not the one its patch "
           "replaced" % (rel.split("/")[-1], L.PRE_REV[:8]))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE INPUTS, DECLARED BEFORE ANY OF THEM IS RUN")
print("""   Each is one file changed AS A COMMIT in a clone of this branch.  A
   commit, because g1 reads c1 and the kernel with `git show`: an edit
   left in the working tree reaches nothing and comes back silent for a
   reason that has nothing to do with the predicate.

   `moves the measurement?` is about the tree AS IT WOULD STAND -- both
   files as committed -- and is declared here, not observed later.""")
print()


def _bend(rel, fn):
    def m(tree):
        p = os.path.join(tree, rel)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(fn(src))
    return m


def _bend_pair(tree):
    for rel, fn in ((L.KERN_REL, L.bend_kern_up), (L.C1_REL, L.bend_c1_down)):
        p = os.path.join(tree, rel)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(fn(src))


# (label, mutate, moves-the-measurement?, what it is, whose list it is on)
INPUTS = [
    ("unmodified -- NULL", None, False,
     "the tree as it stands", "mg-76cc"),
    ("kern_a218.py: dim L(n,p) one too big", _bend(L.KERN_REL, L.bend_kern_up),
     True, "the measuring half, in the kernel -- mg-957f's F-1", "mg-76cc"),
    ("c1_branching.py: vertex dims one too big",
     _bend(L.C1_REL, L.bend_c1_up), True,
     "the measuring half, in the script -- mg-7e58's probe", "mg-76cc"),
    ("c1_branching.py: a comment appended", _bend(L.C1_REL, L.comment_c1),
     False, "the file sha moves and nothing else does", "mg-76cc"),
    ("c1_branching.py: a line past section (iii)",
     _bend(L.C1_REL, L.touch_c1_compare), False,
     "an edit in the COMPARING half", "mg-76cc"),
    ("kern_a218.py: a comment appended", _bend(L.KERN_REL, L.comment_kern),
     False, "the kernel's sha moves and nothing else does", "mg-e34a"),
    ("THE CANCELLING PAIR: kern +1 and c1 -1", _bend_pair, False,
     "both files move, the measurement does NOT", "mg-e34a"),
]
print("     %-42s %-8s %-9s %s"
      % ("input", "moves?", "on whose", "what it is"))
for label, mut, moves, why, whose in INPUTS:
    print("     %-42s %-8s %-9s %s"
          % (label, "YES" if moves else "no", whose, why))
print()

REVS = [(L.PRE_7E58_REV, "g1_pre_7e58.py", "before mg-7e58"),
        (L.PRE_REV, "g1_pre_76cc.py", "BEFORE THIS REPAIR"),
        (None, "g1_provenance.py", "this repair")]

# ---------------------------------------------------------------------------
L.rule("(iii) EVERY INPUT, EVERY PREDICATE REVISION")
print("""   Each pinned revision travels WITH ITS OWN lib58da, under a module
   name of its own: mg-76cc changed lib58da.run_c1's signature in the
   same commit as g1, and a pre-repair predicate run against the
   repaired library is a third thing that never existed.
   g1_provenance.py in the clone is never modified.""")
print()
print("   input                                      moves  %-16s %-16s %s"
      % ("before mg-7e58", "BEFORE REPAIR", "this repair"))
print("                                              meas?  exit self find  "
      "exit self find  exit self find")

RUN = {}      # (input label, revision label) -> (rc, self, find, out)
for label, mut, moves, why, whose in INPUTS:
    def _m(tree, mut=mut):
        if mut is not None:
            mut(tree)
        for rev, name, _what in REVS:
            if rev is not None:
                L.install_pinned(tree, rev, name)
    try:
        tmp, tree = L.clone(mutate=_m, message="mg-e34a input: %s" % label)
    except ValueError as e:
        R.selferr("could not build the input %r (%s); it is DROPPED from the "
                  "population rather than counted as passing" % (label, e))
        continue
    try:
        cells = []
        for rev, name, what in REVS:
            out, rc = L.run_script(L.S58DA_DIR, name, repo=tree)
            s, f = L.trailer(out)
            ok, why_bad = L.trailer_consistent(out)
            R.check(ok, "g1 (%s) on the input %r printed a trailer that does "
                        "not match its own listed lines: %s"
                        % (what, label, why_bad))
            RUN[(label, what)] = (rc, s, f, out)
            cells.append("%-4s %-4s %-5s"
                         % (rc, "-" if s is None else s,
                            "-" if f is None else f))
        print("     %-42s %-6s %s"
              % (label[:42], "YES" if moves else "no", " ".join(cells)))
    finally:
        L.destroy(tmp)
print()
print("   population: the %d inputs above x the %d predicate revisions = %d "
      "runs." % (len(INPUTS), len(REVS), len(INPUTS) * len(REVS)))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE THREE BUCKETS, PER INPUT, UNFILTERED")
print("""   OLD = the predicate at %s, the parent of this repair.  NEW = the
   predicate this repair ships.  EVERY input is bucketed -- not only the
   ones an input list calls a defect.  mg-76cc's own r3 restricts its
   backwards set to inputs it has declared `real defects`, which makes
   the answer depend on the declaration; here the declaration is printed
   beside the bucket and does not filter it.""" % L.PRE_REV[:8])
print()
print("   input                                      exit grain          "
      "finding grain")
BUCK = {}
for label, mut, moves, why, whose in INPUTS:
    old = RUN.get((label, "BEFORE THIS REPAIR"))
    new = RUN.get((label, "this repair"))
    if old is None or new is None:
        R.selferr("input %r did not produce both a pre-repair and a repaired "
                  "run; it is DROPPED from the buckets" % label)
        continue

    def bucket(o, n):
        if o and n:
            return "both fire"
        if not o and not n:
            return "both silent"
        return "OLD FIRES, NEW SILENT" if o else "new fires, old silent"

    be = bucket(old[0] != 0, new[0] != 0)
    bf = bucket((old[2] or 0) > 0, (new[2] or 0) > 0)
    BUCK[label] = (be, bf)
    print("     %-42s %-19s %s" % (label[:42], be, bf))
print()
back_e = [k for k, v in BUCK.items() if v[0].startswith("OLD FIRES")]
back_f = [k for k, v in BUCK.items() if v[1].startswith("OLD FIRES")]
print("   INPUTS WHERE THE OLD PREDICATE FIRES AND THIS ONE IS SILENT")
print("     at the exit grain    : %d" % len(back_e))
for k in back_e:
    print("        %s" % k)
print("     at the finding grain : %d" % len(back_f))
for k in back_f:
    print("        %s" % k)
R.gate(not back_e,
       "coverage went backwards at the EXIT grain on %d input(s): %s"
       % (len(back_e), "; ".join(back_e)))
R.gate(not back_f,
       "coverage went backwards at the FINDING grain on %d input(s): %s"
       % (len(back_f), "; ".join(back_f)))
print()

print("   AND WHAT EACH FINDING NAMES.  A bucket of `both fire` is not the")
print("   same as `the same thing was caught`.  Every file named by a")
print("   pre-repair finding, against every file named by a repaired one:")
print()
print("     %-42s %-24s %s" % ("input", "named by OLD", "named by NEW"))
lost_names = []
for label, mut, moves, why, whose in INPUTS:
    old, new = RUN.get((label, "BEFORE THIS REPAIR")), RUN.get((label,
                                                                "this repair"))
    if old is None or new is None:
        continue
    on = set()
    for f in L.findings(old[3]):
        on |= set(L.names_files(f))
    nn = set()
    for f in L.findings(new[3]):
        nn |= set(L.names_files(f))
    print("     %-42s %-24s %s"
          % (label[:42], ", ".join(sorted(on)) or "-",
             ", ".join(sorted(nn)) or "-"))
    for miss in sorted(on - nn):
        lost_names.append((label, miss))
print()
print("   FILES A PRE-REPAIR FINDING NAMES AND NO REPAIRED FINDING DOES : %d"
      % len(lost_names))
for label, miss in lost_names:
    print("      %s -- on the input %s" % (miss, label))
R.gate(not lost_names,
       "on %d (input, file) pair(s) the pre-repair predicate names a file in "
       "a finding and the repaired one names it in none: %s"
       % (len(lost_names),
          "; ".join("%s on %s" % (m, la) for la, m in lost_names)))
print()

# ---------------------------------------------------------------------------
L.rule("(v) THE OTHER DIRECTION -- WHAT THE REPAIRED PREDICATE FIRES ON")
print("""   A predicate restored by making it red on everything is not
   restored.  Every input declared NOT to move the measurement, against
   what EACH predicate did with it -- the pre-repair column is here so
   that a pre-existing over-firing is not booked against this repair.""")
print()
print("     %-42s %-14s %s" % ("input", "OLD findings", "NEW findings"))
false_red, false_red_old = [], []
for label, mut, moves, why, whose in INPUTS:
    if moves:
        continue
    new, old = RUN.get((label, "this repair")), RUN.get((label,
                                                         "BEFORE THIS REPAIR"))
    if new is None or old is None:
        continue
    fired, fired_old = (new[2] or 0) > 0, (old[2] or 0) > 0
    print("     %-42s %-14s %s"
          % (label[:42],
             "%s %s" % (old[2], "FIRES" if fired_old else "silent"),
             "%s %s" % (new[2], "FIRES" if fired else "silent")))
    if fired:
        false_red.append(label)
        for f in L.findings(new[3]):
            print("        NEW FINDING: %s" % f[:92])
    if fired_old:
        false_red_old.append(label)
print()
print("   INPUTS THAT DO NOT MOVE THE MEASUREMENT ON WHICH A FINDING IS")
print("   BOOKED :  by this repair %d,  by the pre-repair predicate %d"
      % (len(false_red), len(false_red_old)))
for x in false_red:
    print("      this repair : %s" % x)
for x in false_red_old:
    print("      pre-repair  : %s" % x)
R.gate(not false_red,
       "the repaired predicate books a FINDING on %d input(s) whose "
       "measurement at HEAD is byte-identical to the measurement at %s: %s.  "
       "Its own `both together` row -- the only one of the three that asks "
       "the question the tree actually poses -- prints IDENTICAL on the same "
       "run, and the findings that outvote it come from half-moved trees "
       "that exist nowhere.  %d of these were already booked by the "
       "pre-repair predicate, so the class is not new; what is new is that "
       "mg-76cc's own rationale for the `both together` row NAMES this input "
       "and states the opposite outcome (k4 demonstrates it)"
       % (len(false_red), L.REV_A218[:8], ", ".join(false_red),
          len(false_red_old)))
print()
print("   population: the %d of %d inputs above declared in (ii) not to move "
      "the" % (len([i for i in INPUTS if not i[2]]), len(INPUTS)))
print("   measurement.  The declaration is checked, not assumed: k4 measures")
print("   the cancelling pair's measurement directly and prints the shas.")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   The pre-repair predicate was RUN, at %s, with its own lib58da,
   against the same %d inputs as the repaired one -- %d of them mg-76cc's
   own and %d it does not have.

   Backwards at the exit grain    : %d
   Backwards at the finding grain : %d
   Files named by an old finding and by no new one : %d
   Inputs that do not move the measurement on which the repair fires : %d
""" % (L.PRE_REV[:8], len(INPUTS),
       len([i for i in INPUTS if i[4] == "mg-76cc"]),
       len([i for i in INPUTS if i[4] == "mg-e34a"]),
       len(back_e), len(back_f), len(lost_names), len(false_red)))

sys.exit(R.emit())
