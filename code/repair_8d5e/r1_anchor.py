"""r1_anchor.py -- A-1: THE ANCHOR, RE-POINTED AT THE PROPERTY AND PINNED.

mg-2c77's OPEN 1.  `libe34a` derived `REPAIR_REV` as the last commit that
touched g1_provenance.py, and mg-69d1 touched g1_provenance.py to correct a
SENTENCE.  The anchor followed the edit: `REPAIR_REV` 4755d02 -> d01ff32,
`PRE_REV` 3bc2cf76 -> e5787e11.  Both sides of k1's pre-repair comparison
became mg-76cc's ALREADY-REPAIRED predicate, and every number k1 printed was
unchanged and about a different pair of revisions.

WHAT THIS SCRIPT MEASURES, in order:

  (i)   the anchor as it now stands: DERIVED from a property, PINNED, and the
        two COMPARED -- with the file-history derivation kept and printed
        beside it, because the quantity that moved is the evidence
  (ii)  THE DEFECT REPRODUCED: a commit built here that touches
        g1_provenance.py and does not touch the property.  The file-history
        anchor moves; the property anchor does not.  If that pair of
        outcomes cannot be produced, the repair is a rewording
  (iii) THE FIX FAILING LOUDLY, three ways -- a wrong pin, an unfindable
        marker, and a marker that stops being monotone.  A check that cannot
        be made to fail is not a check
  (iv)  THE SECOND CONSEQUENCE, IN A SECOND SCRIPT.  mg-2c77 named k1.  The
        same anchor is `REPAIR_REV` in k4_cancel.py, where it selects the
        commit MESSAGE that is scanned for the sentence under test -- and at
        the pre-repair HEAD it scanned mg-69d1's message instead of mg-76cc's,
        so a copy of that sentence silently left the count
  (v)   AND NOTHING ELSE: every revision constant libe34a exports, before and
        after, with a disposition each

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "branching_audit_e34a"))

import lib8d5e as L                                            # noqa: E402
import libe34a as E                                            # noqa: E402

R = L.Report(
    selfpop="every clone, git read and subprocess run this script performs, "
            "plus the requirement that each constructed commit really change "
            "the file it claims to change and really leave the property "
            "marker where it was",
    findpop="the four anchors libe34a derives, each against its pin; the two "
            "outcomes of the reproduced drift in (ii); the three loud "
            "failures in (iii); k4's commit-message selection in (iv) against "
            "k4's own committed transcript; and every revision constant "
            "libe34a exports, scored in (v) for whether it moved and whether "
            "it was supposed to")

L.banner("R1", "A-1 -- THE ANCHOR, RE-POINTED AT THE PROPERTY AND PINNED")
print("""
A literal cannot notice that the file moved.  That is why mg-e34a derived.
A derivation cannot notice that it has started measuring something else --
and that failure is quieter, because the number is identical and means
something else.  So the anchor is now both, and they are compared.
""")

# ---------------------------------------------------------------------------
L.rule("(i) THE ANCHOR AS IT NOW STANDS: DERIVED, PINNED, COMPARED")
print("""   The property is named by a marker that IS the repair rather than a
   description of it.  `kernel_source=` is mg-76cc's two-source
   signature -- the thing that makes "this script with that kernel"
   expressible at all, and whose absence WAS mg-957f's F-1.  A commit
   that edits prose in the same file does not move it.""")
print()
print("     %-52s %-9s %-9s %s" % ("anchor", "derived", "pinned", ""))
for label, got, pin, verdict in E.anchor_rows():
    print("     %-52s %-9s %-9s %s" % (label, got[:8], pin[:8], verdict))
    R.gate(got == pin,
           "the anchor %r derives to %s and is pinned at %s; one of the two "
           "is wrong and this run cannot say which"
           % (label.strip(), got[:8], pin[:8]))
print()
R.gate(not E.ANCHOR_DRIFT,
       "libe34a reports %d anchor disagreement(s): %s"
       % (len(E.ANCHOR_DRIFT), "; ".join(E.ANCHOR_DRIFT)))
print("   libe34a.ANCHOR_DRIFT : %d row(s)" % len(E.ANCHOR_DRIFT))
for row in E.ANCHOR_DRIFT:
    print("      *** %s" % row)
print()
print("   AND THE DERIVATION THAT RE-POINTED, KEPT AND PRINTED.  Deleting the")
print("   quantity that moved would leave the next reader nothing to check")
print("   the story against:")
print()
_hist = [("the last commit touching g1_provenance.py", E.LAST_TOUCHING_G1,
          E.REPAIR_REV, "mg-76cc's repair"),
         ("its first parent -- the OLD `before this repair`",
          E.resolve(E.LAST_TOUCHING_G1 + "^"), E.PRE_REV,
          "the pre-repair predicate"),
         ("the 2nd-newest commit touching it, parent -- OLD `before mg-7e58`",
          E.resolve(E.NTH_TOUCHING_1 + "^"), E.PRE_7E58_REV, "before mg-7e58")]
print("     %-62s %-9s %s" % ("derived from the FILE'S HISTORY", "gives",
                              "the PROPERTY gives"))
for label, hist, prop, _what in _hist:
    print("     %-62s %-9s %s" % (label, hist[:8], prop[:8]))
print()
_moved = [x for x in _hist if x[1] != x[2]]
print("   history anchors that no longer point where the property does : %d "
      "of %d" % (len(_moved), len(_hist)))
print()
print("   BOTH of them moved, and mg-2c77 named one.  An index into a file's")
print("   history is an anchor derived from that history: mg-69d1's commit")
print("   pushed every index along by one, so the column k1 labels `before")
print("   mg-7e58` came to hold mg-76cc's parent.  The same defect, in the")
print("   same file, in a constant nobody looked at.")
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE DEFECT REPRODUCED -- A COMMIT THAT MOVES THE FILE AND NOT "
       "THE PROPERTY")
print("""   Built here, as a COMMIT in a clone, because every derivation under
   test reads `git log` and an edit left in the working tree is
   invisible to all of them.  The commit appends a comment to
   g1_provenance.py: the file moves, `kernel_source=` does not.

   TWO outcomes are required and both are gated.  A repair whose
   property anchor also moved would be no repair; a repair whose
   file-history derivation did NOT move would mean the input never
   exercised the defect and the row below would be vacuous.""")
print()


def _touch_g1_prose(tree):
    p = os.path.join(tree, E.G1_REL)
    with open(p) as fh:
        src = fh.read()
    if "kernel_source=" not in src:
        raise ValueError("g1 in the clone does not carry the marker; the "
                         "input cannot be built")
    with open(p, "w") as fh:
        fh.write(src + "\n# mg-8d5e control: a comment, and nothing more\n")


tmp, tree = L.clone(mutate=_touch_g1_prose,
                    message="mg-8d5e input: a sentence in g1_provenance.py")
try:
    after, rows, rc, raw = L.probe_libe34a(tree)
    R.check(rc == 0 and after,
            "libe34a did not import in the clone (rc %d); section (ii) is "
            "withdrawn: %s" % (rc, raw.strip()[-300:]))
    marker_still = "kernel_source=" in L.git_show("HEAD", E.G1_REL, repo=tree)
    R.check(marker_still,
            "the constructed commit removed the property marker from g1; it "
            "is not the input this section declares and the row is withdrawn")
    print("     %-46s %-14s %s" % ("", "at this HEAD", "after the commit"))
    print("     %-46s %-14s %s"
          % ("the last commit touching g1 (FILE HISTORY)",
             E.LAST_TOUCHING_G1[:8], after.get("LAST_TOUCHING_G1")))
    print("     %-46s %-14s %s"
          % ("REPAIR_REV (THE PROPERTY)", E.REPAIR_REV[:8],
             after.get("REPAIR_REV")))
    print("     %-46s %-14s %s"
          % ("PRE_REV (THE PROPERTY)", E.PRE_REV[:8], after.get("PRE_REV")))
    print("     %-46s %-14s %s"
          % ("the marker still in g1?", "yes",
             "yes" if marker_still else "NO"))
    print()
    hist_moved = after.get("LAST_TOUCHING_G1") != E.LAST_TOUCHING_G1[:8]
    prop_held = (after.get("REPAIR_REV") == E.REPAIR_REV[:8]
                 and after.get("PRE_REV") == E.PRE_REV[:8])
    print("   the FILE-HISTORY derivation moved : %s" % ("YES" if hist_moved
                                                         else "no"))
    print("   the PROPERTY anchor held          : %s" % ("YES" if prop_held
                                                         else "NO"))
    print("   anchor disagreements reported in the clone : %s"
          % after.get("DRIFT"))
    R.check(hist_moved,
            "the constructed commit did not move the file-history "
            "derivation, so this input does not exercise the defect and the "
            "row beside it is vacuous")
    R.gate(prop_held,
           "the property anchor MOVED on a commit that touched "
           "g1_provenance.py without touching the property: REPAIR_REV %s -> "
           "%s.  That is the defect this repair is for, still present"
           % (E.REPAIR_REV[:8], after.get("REPAIR_REV")))
    R.gate(after.get("DRIFT") == "0",
           "the clone reports %s anchor disagreement(s) on an input that "
           "should not have moved any anchor: %s"
           % (after.get("DRIFT"), "; ".join(rows)))
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE FIX FAILING LOUDLY -- THREE BREAKS, EACH BUILT")
print("""   A check that cannot be made to fail is not a check.  Each break
   below is a COMMIT in its own clone, and what is measured is whether
   mg-e34a's own selftest goes red and says why -- not whether this
   script noticed.  The instrument under test is the one that ships.""")
print()

BREAKS = [
    ("the PIN made wrong",
     ('REPAIR_REV_PIN = "4755d0292fc9175815739e9a77fa24dc6b8baf48"',
      'REPAIR_REV_PIN = "4372fae95881bb421099bc715d1924c37d98b7b3"'),
     "the pin now names mg-7e58's commit; the derivation still finds "
     "mg-76cc's"),
    ("the MARKER made unfindable",
     ('MARK_76CC = "kernel_source="',
      'MARK_76CC = "kernel_source_that_is_in_no_revision="'),
     "the property cannot be derived at all; the pin must be used AND the "
     "fallback said out loud"),
]
print("     %-30s %-8s %-7s %s"
      % ("break", "selftest", "drift", "what it must say"))
for label, (old, new), why in BREAKS:
    def _break(tree, old=old, new=new):
        p = os.path.join(tree, L.LIBE34A_REL)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(L.replace_once(src, old, new))
    try:
        tmp, tree = L.clone(mutate=_break, message="mg-8d5e break: %s" % label)
    except ValueError as e:
        R.selferr("could not build the break %r (%s); it is DROPPED from the "
                  "population rather than counted as passing" % (label, e))
        continue
    try:
        out, rc = L.run_script(L.E34A_DIR, "selftest_e34a.py", repo=tree)
        _after, rows, _rc2, _raw = L.probe_libe34a(tree)
        print("     %-30s %-8s %-7s %s"
              % (label, "exit %d" % rc, _after.get("DRIFT", "?"), why))
        for row in rows:
            print("        says: %s" % row[:88])
        R.gate(rc != 0,
               "mg-e34a's selftest exits 0 with %s; the break is silent and "
               "the check does not check" % label)
        R.gate(int(_after.get("DRIFT", "0")) > 0,
               "ANCHOR_DRIFT is empty with %s; the disagreement is not "
               "recorded anywhere a reader would see it" % label)
    finally:
        L.destroy(tmp)


def _break_monotone(tree):
    p = os.path.join(tree, E.G1_REL)
    with open(p) as fh:
        src = fh.read()
    with open(p, "w") as fh:
        fh.write(src.replace("kernel_source=", "kern_src_renamed="))


tmp, tree = L.clone(mutate=_break_monotone,
                    message="mg-8d5e break: the marker removed from g1")
try:
    out, rc = L.run_script(L.E34A_DIR, "selftest_e34a.py", repo=tree)
    mono_line = [ln for ln in out.splitlines() if "monotone" in ln]
    print("     %-30s %-8s %-7s %s"
          % ("the MARKER made non-monotone", "exit %d" % rc, "-",
             "present, then absent again -- `first introducing` would answer "
             "about the first of two"))
    for ln in mono_line:
        print("        %s" % ln.strip()[:92])
    R.gate(rc != 0,
           "mg-e34a's selftest exits 0 when the property marker is removed "
           "from g1 at a later commit; `first_introducing` would keep "
           "answering with the first introduction and nothing would say so")
finally:
    L.destroy(tmp)
print()
print("   population: the %d breaks declared above, each built as a commit in "
      "a clone of\n   this branch and each scored by mg-e34a's own selftest "
      "rather than by this one." % (len(BREAKS) + 1))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE SECOND CONSEQUENCE, IN A SECOND SCRIPT -- k4's COMMIT "
       "MESSAGE")
print("""   mg-2c77 named k1.  The same constant is `REPAIR_REV` in
   k4_cancel.py, where it selects WHICH COMMIT MESSAGE is scanned for
   the sentence under test.  So the drift did not merely re-label k1's
   columns: it moved a population.

   The arbiter is k4's OWN COMMITTED TRANSCRIPT, which was written when
   the anchor still pointed at mg-76cc.  It is a third party to this
   repair and it is not edited here.""")
print()
_committed = L.git_show("HEAD", L.OUT_K4_REL) or L.read_worktree(L.OUT_K4_REL)
_recorded = [ln.strip() for ln in _committed.splitlines()
             if "in the COMMIT MESSAGE of" in ln]
R.check(bool(_recorded),
        "k4's committed transcript carries no `in the COMMIT MESSAGE of` "
        "line; section (iv) has no arbiter and is withdrawn")
_rec_rev = _recorded[0].split("of ")[1].split(" ")[0] if _recorded else ""
_rec_yes = _recorded and _recorded[0].rstrip().endswith("yes")

CLAIM = "cancelling pair would pass each half"
_prop_msg = L.git("log", "-1", "--format=%B", E.REPAIR_REV)
_hist_msg = L.git("log", "-1", "--format=%B", E.LAST_TOUCHING_G1)
print("     %-46s %-10s %s" % ("which commit message k4 scans", "revision",
                               "carries the sentence?"))
print("     %-46s %-10s %s"
      % ("k4's committed transcript recorded", _rec_rev,
         "yes" if _rec_yes else "no"))
print("     %-46s %-10s %s"
      % ("under the FILE-HISTORY anchor (pre-repair)", E.LAST_TOUCHING_G1[:8],
         "yes" if CLAIM in _hist_msg else "NO"))
print("     %-46s %-10s %s"
      % ("under the PROPERTY anchor (this repair)", E.REPAIR_REV[:8],
         "yes" if CLAIM in _prop_msg else "no"))
print()
R.gate(E.REPAIR_REV.startswith(_rec_rev.rstrip(":").strip()) if _rec_rev
       else False,
       "the anchor k4 uses (%s) is not the revision k4's own committed "
       "transcript says it used (%s); the population it scans is not the one "
       "the record is about" % (E.REPAIR_REV[:8], _rec_rev))
R.gate((CLAIM in _prop_msg) == bool(_rec_yes),
       "the property anchor's commit message %s the sentence under test, "
       "and k4's committed transcript records %s"
       % ("carries" if CLAIM in _prop_msg else "does not carry",
          "yes" if _rec_yes else "no"))
print("   Under the drifted anchor the scan reads mg-69d1's message, which")
print("   does not carry the sentence, and a copy left the count without any")
print("   number moving that a reader could see.  That is the shape of the")
print("   whole finding: the figure is identical and it is about something")
print("   else.")
print()

# ---------------------------------------------------------------------------
L.rule("(v) AND NOTHING ELSE -- EVERY REVISION CONSTANT libe34a EXPORTS")
print("""   The population is DERIVED, not listed: libe34a as it stood before
   this repair is reached by the property -- the newest commit at which
   the file does not carry `def first_introducing(` -- and run in a
   clone beside the repaired one.  Naming a revision here would have
   been this ticket's own version of A-1.""")
print()
_pre_rev = L.last_lacking(L.LIBE34A_REL, "def first_introducing(")
R.check(_pre_rev is not None,
        "no revision of libe34a.py lacks the repair's own marker; the before "
        "column cannot be built and section (v) is withdrawn")
if _pre_rev:
    print("   libe34a before this repair, derived : %s  %s"
          % (_pre_rev[:8], L.subject(_pre_rev)[:60]))
    print()

    def _install_old(tree):
        with open(os.path.join(tree, L.LIBE34A_REL), "w") as fh:
            fh.write(L.git_show(_pre_rev, L.LIBE34A_REL))

    tmp, tree = L.clone(mutate=_install_old,
                        message="mg-8d5e: libe34a as it stood before")
    try:
        before, _rows, brc, braw = L.probe_libe34a(tree)
        R.check(brc == 0 and before,
                "the pre-repair libe34a did not import in the clone (rc %d); "
                "section (v) is withdrawn: %s" % (brc, braw.strip()[-200:]))
        after = {"REV_A218": E.REV_A218[:8], "REPAIR_REV": E.REPAIR_REV[:8],
                 "PRE_REV": E.PRE_REV[:8], "REV_7E58": E.REV_7E58[:8],
                 "PRE_7E58_REV": E.PRE_7E58_REV[:8],
                 "LAST_TOUCHING_G1": E.LAST_TOUCHING_G1[:8],
                 "NTH_TOUCHING_1": E.NTH_TOUCHING_1[:8]}
        WHY = {
            "REV_A218": ("unchanged -- read out of lib58da's own source, "
                         "not from any history"),
            "REPAIR_REV": "MOVED, and that is the repair: back onto mg-76cc",
            "PRE_REV": "MOVED, and that is the repair: back onto its parent",
            "REV_7E58": "NEW -- the mg-7e58 anchor, named where it was not",
            "PRE_7E58_REV": ("MOVED: it held mg-76cc's parent under a label "
                             "saying mg-7e58"),
            "LAST_TOUCHING_G1": ("NEW -- the derivation that re-pointed, kept "
                                 "as evidence and used by no anchor"),
            "NTH_TOUCHING_1": ("NEW -- the second history derivation, kept "
                               "for the same reason and used by no anchor"),
        }
        print("     %-18s %-10s %-10s %s"
              % ("constant", "before", "after", "disposition"))
        unexplained = []
        for name in sorted(set(list(before) + list(after)) - {"DRIFT"}):
            b, a = before.get(name, "-"), after.get(name, "-")
            why = WHY.get(name)
            if why is None:
                unexplained.append(name)
                why = "*** NOT ACCOUNTED FOR"
            print("     %-18s %-10s %-10s %s" % (name, b, a, why))
        print()
        R.gate(not unexplained,
               "%d revision constant(s) of libe34a have no disposition here: "
               "%s.  A list of what changed that does not cover the "
               "population is the shape of the defect above"
               % (len(unexplained), ", ".join(unexplained)))
        R.gate(before.get("REPAIR_REV") != after.get("REPAIR_REV"),
               "REPAIR_REV reads the same before and after this repair (%s); "
               "either the drift was not present or it was not repaired"
               % after.get("REPAIR_REV"))
        R.gate(before.get("REV_A218") == after.get("REV_A218"),
               "REV_A218 moved (%s -> %s) and this repair had no business "
               "moving it" % (before.get("REV_A218"), after.get("REV_A218")))
    finally:
        L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(vi) A THIRD INSTANCE, OBSERVED AND NOT REPAIRED")
print("""   `code/repair_69d1/p3_reason.py` (i-b) runs its discriminator
   AGAINST HEAD, described as `the committed tree, where the defect is
   still present`, and self-errors if it finds 0 live assertions
   there.  HEAD is an anchor that moves on every commit: mg-69d1's own
   repair landing is what removed the last live assertion, so the
   control has been vacuous since the moment the repair it belongs to
   was committed.

   THE SAME SHAPE AS A-1 -- a reference that follows an edit and keeps
   printing -- in a script mg-2c77 did not name.  It is NOT repaired
   here: this ticket's population is mg-2c77's two open sites, and
   widening it would be a decision nobody asked for.  What is done is
   to establish that this repair did not CAUSE it, by running the
   script at the revision before this repair began.""")
print()
_p3_base = L.base_before_dir(L.MINE_DIR)
_p3_rel = L.R69D1_DIR + "/p3_reason.py"
R.check(_p3_base is not None,
        "no revision of this branch lacks %s; the before column cannot be "
        "built and section (vi) is withdrawn" % L.MINE_DIR)
if _p3_base:
    tmp, tree = L.clone_at(_p3_base)
    try:
        base_out, base_rc = L.run_script(L.R69D1_DIR, "p3_reason.py",
                                         repo=tree)
    finally:
        L.destroy(tmp)
    here_out = L.read_worktree(L.R69D1_DIR + "/out_p3_reason.txt")
    base_se, _bf = L.trailer_counts(base_out)
    here_se, _hf = L.trailer_counts(here_out)
    print("     %-46s %-10s %s" % ("p3_reason.py", "exit", "SELF-ERRORS"))
    print("     %-46s %-10s %s"
          % ("at %s, before this repair began" % _p3_base[:8], base_rc,
             base_se))
    print("     %-46s %-10s %s"
          % ("at this HEAD, after it", "1" if here_se else "0", here_se))
    print()
    R.check(base_rc is not None, "p3 produced no exit code at the base")
    R.gate(base_rc != 0,
           "p3_reason.py exits 0 at %s and non-zero here, so this repair "
           "caused the break rather than merely observing it" % _p3_base[:8])
    print("   It was already red before this repair touched anything, with the")
    print("   same self-error.  Noted, pointed at, and left for whoever owns")
    print("   the population it belongs to.")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   The anchor is derived from the PROPERTY, PINNED, and the two are
   COMPARED, with the derivation that re-pointed kept and printed.

   anchors derived and pinned that agree      : %d of %d
   history anchors that had re-pointed        : %d of %d
   breaks built, each red in mg-e34a's own selftest : %d
   the second script the same anchor reaches  : k4_cancel.py (iv)
"""
      % (len([1 for _l, g, p, _v in E.anchor_rows() if g == p]),
         len(E.anchor_rows()), len(_moved), len(_hist), len(BREAKS) + 1))

sys.exit(R.emit())
