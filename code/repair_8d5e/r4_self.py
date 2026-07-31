"""r4_self.py -- THIS DELIVERABLE, CHECKED FOR THE DEFECTS IT REPAIRS.

mg-2c77 ends with an instruction addressed to whoever writes this:

    This deliverable is of the same kind as the defect it repairs.  Check that
    every anchor you derive still points where you think, and that every term
    you use in a count means the same thing at every site you use it.
    Enumerate what you checked.

So both checks are performed on THIS instrument, by the same means used on the
subjects, and what was checked is enumerated rather than summarised.

  (i)   EVERY ANCHOR THIS DELIVERABLE DERIVES, enumerated, each classified by
        WHAT IT IS ANCHORED ON -- and then PERTURBED: a commit built here that
        touches every file these anchors derive from without touching any of
        the properties.  An anchor that survives is measured; an anchor that
        is merely declared safe is the finding.
  (ii)  EVERY TERM THIS DELIVERABLE USES IN A COUNT, each with the population
        it denotes, scored at every site by the rule that applies to it --
        including the edit this repair made to its OWN prediction file, which
        is booked here rather than left to be noticed.
  (iii) THE KINDS OF ARTIFACT THIS REPAIR EMITS, with a disposition each, over
        a population DERIVED from git rather than listed.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "branching_audit_e34a"))

import lib8d5e as L                                            # noqa: E402
import libe34a as E                                            # noqa: E402

R = L.Report(
    selfpop="every git read, clone and subprocess run this script performs, "
            "plus the requirement that the perturbation commit really touch "
            "every file it names and really leave every property marker in "
            "place",
    findpop="every revision this deliverable's scripts derive or pin, "
            "classified by what it is anchored on and re-derived under a "
            "perturbation; every counted term this deliverable uses, scored "
            "at every site in its own files; and every path this repair "
            "changes, scored against the kinds enumerated here")

L.banner("R4", "THIS DELIVERABLE, CHECKED FOR THE DEFECTS IT REPAIRS")
print("""
A repair for an anchor that re-pointed, anchored on a file's history, would be
the defect wearing the repair's clothes.  So would a repair for a term that
denotes two populations, written with that term in two ways.
""")

# ---------------------------------------------------------------------------
L.rule("(i) EVERY ANCHOR THIS DELIVERABLE DERIVES")
print("""   ANCHORED ON A PROPERTY  the revision is found by asking what the
     file CONTAINS, so an edit that does not change the property does
     not move it.
   PINNED AND CHECKED  the revision is written down AND a derivation
     is run against it, so a pin that rots is loud.
   ANCHORED ON A FILE'S HISTORY  re-points on the next unrelated edit.
     This is the defect; nothing here may depend on one, and the two
     that remain are printed as evidence and used by no measurement.""")
print()

_kern_rel = L.INSTR_DIR + "/kern5f9a.py"
_kern_mark = "THE QUALIFIER IS LOAD-BEARING"
_libe_mark = "def first_introducing("
_base = L.base_before_dir(L.MINE_DIR)

ANCHORS = [
    ("libe34a.REPAIR_REV", E.REPAIR_REV, "property + pin",
     "first commit where g1 carries %r, checked against a pin" % E.MARK_76CC),
    ("libe34a.PRE_REV", E.PRE_REV, "property + pin",
     "its first parent, checked against a pin"),
    ("libe34a.REV_7E58", E.REV_7E58, "property + pin",
     "first commit where g1 carries %r, checked against a pin" % E.MARK_7E58),
    ("libe34a.PRE_7E58_REV", E.PRE_7E58_REV, "property + pin",
     "its first parent, checked against a pin"),
    ("lib8d5e.Q3_REV_PIN", L.Q3_REV_PIN, "pin + derivation",
     "re-derived as the last commit touching mg-2c77's transcript"),
    ("lib8d5e.D01FF32_PIN", L.D01FF32_PIN, "pin + derivation",
     "re-derived as the last commit touching g1 before this repair"),
    ("r1 (v): libe34a before this repair", L.last_lacking(L.LIBE34A_REL,
                                                          _libe_mark),
     "property", "newest revision of libe34a lacking %r" % _libe_mark),
    ("r3 (v): kern5f9a before this repair", L.last_lacking(_kern_rel,
                                                           _kern_mark),
     "property", "newest revision of kern5f9a lacking the comment's marker"),
    ("r4 (iii): the base of this repair's diff", _base, "property",
     "newest revision at which %s does not exist" % L.MINE_DIR),
    ("libe34a.LAST_TOUCHING_G1", E.LAST_TOUCHING_G1, "FILE HISTORY",
     "kept as evidence; used by no anchor and no measurement"),
    ("libe34a.NTH_TOUCHING_1", E.NTH_TOUCHING_1, "FILE HISTORY",
     "kept for the same reason; used by no anchor and no measurement"),
]
print("   %-42s %-9s %-17s %s"
      % ("anchor", "value", "anchored on", "how it is checked"))
for name, value, how, why in ANCHORS:
    print("   %-42s %-9s %-17s %s"
          % (name, (value or "-")[:8], how, why[:52]))
    R.check(value is not None,
            "the anchor %s did not resolve; every row that uses it is "
            "withdrawn" % name)
print()
_history = [n for n, _v, how, _w in ANCHORS if how == "FILE HISTORY"]
print("   anchors derived from a file's HISTORY : %d, and %s"
      % (len(_history),
         "each is declared unused" if _history else "none"))
for n in _history:
    print("      %s" % n)
print()

# derivation-against-pin, for the two pins
R.gate(L.last_touching(L.Q3_TRANSCRIPT_REL) == L.Q3_REV_PIN,
       "Q3_REV_PIN is %s and the last commit touching %s is %s; the pin no "
       "longer names the revision mg-2c77's table is about"
       % (L.Q3_REV_PIN[:8], L.Q3_TRANSCRIPT_REL,
          (L.last_touching(L.Q3_TRANSCRIPT_REL) or "-")[:8]))
_d01_subject = L.subject(L.D01FF32_PIN)
R.gate("mg-69d1" in _d01_subject,
       "D01FF32_PIN %s has the subject %r, which does not name mg-69d1; the "
       "population `the files d01ff32 touched` is not the repair mg-2c77 "
       "audited" % (L.D01FF32_PIN[:8], _d01_subject[:60]))
print("   Q3_REV_PIN re-derived  : %s  (%s)"
      % ((L.last_touching(L.Q3_TRANSCRIPT_REL) or "-")[:8],
         "agrees" if L.last_touching(L.Q3_TRANSCRIPT_REL) == L.Q3_REV_PIN
         else "*** DISAGREES"))
print("   D01FF32_PIN's subject  : %s" % _d01_subject[:66])
print()

print("   AND THE PERTURBATION.  A commit built here appends a comment to")
print("   every file these anchors derive from -- and to nothing else -- so")
print("   `it does not move` is a measurement rather than a property of the")
print("   week this was written in.")
print()
PERTURBED = [L.LIBE34A_REL, _kern_rel, L.MINE_DIR + "/lib8d5e.py"]


def _perturb(tree):
    for rel in PERTURBED:
        p = os.path.join(tree, rel)
        with open(p) as fh:
            src = fh.read()
        with open(p, "w") as fh:
            fh.write(src + "\n# mg-8d5e r4 perturbation: a comment, nothing "
                            "more\n")


tmp, tree = L.clone(mutate=_perturb,
                    message="mg-8d5e r4: a comment in every anchoring file")
try:
    mine_after, mrc, mraw = L.probe_mine(tree)
    e_after, _rows, erc, eraw = L.probe_libe34a(tree)
    R.check(mrc == 0 and e_after and mine_after,
            "the probes did not run in the perturbed clone (rc %d/%d); the "
            "perturbation row is withdrawn: %s"
            % (mrc, erc, (mraw + eraw).strip()[-240:]))
    for rel in PERTURBED:
        moved = L.git_show("HEAD", rel, repo=tree) != L.read_worktree(rel)
        R.check(moved,
                "the perturbation did not change %s, so the row beside it "
                "does not exercise anything" % rel)
    HERE = {"LIBE34A": (L.last_lacking(L.LIBE34A_REL, _libe_mark) or "-")[:8],
            "KERN": (L.last_lacking(_kern_rel, _kern_mark) or "-")[:8],
            "Q3": (L.last_touching(L.Q3_TRANSCRIPT_REL) or "-")[:8]}
    HERE["REPAIR_REV"] = E.REPAIR_REV[:8]
    HERE["PRE_REV"] = E.PRE_REV[:8]
    mine_after["REPAIR_REV"] = e_after.get("REPAIR_REV")
    mine_after["PRE_REV"] = e_after.get("PRE_REV")
    print("   %-16s %-12s %-12s %s"
          % ("anchor", "here", "perturbed", ""))
    drifted = []
    for key in sorted(HERE):
        a, b = HERE[key], mine_after.get(key)
        same = a == b
        print("   %-16s %-12s %-12s %s"
              % (key, a, b, "held" if same else "*** MOVED"))
        if not same:
            drifted.append("%s %s -> %s" % (key, a, b))
    print()
    print("   files perturbed : %d;  anchors that moved : %d"
          % (len(PERTURBED), len(drifted)))
    R.gate(not drifted,
           "%d anchor(s) this deliverable derives MOVED under a commit that "
           "touched their files and none of their properties: %s.  That is "
           "the defect this ticket repairs, present in the repair"
           % (len(drifted), "; ".join(drifted)))
finally:
    L.destroy(tmp)
print()

# ---------------------------------------------------------------------------
L.rule("(ii) EVERY TERM THIS DELIVERABLE USES IN A COUNT")
print("""   A term in a count needs a population, and the population has to be
   the same one at every site.  Each term below is scored across THIS
   deliverable's own files by the rule that applies to it -- for the
   census phrase that is mg-2c77's rule, unchanged, so my count and its
   count are the same measurement.""")
print()

MINE = [p for p in L.changed_paths(_base) if L.is_mine(p)]
print("   this deliverable's own files : %d" % len(MINE))
for p in MINE:
    print("      %s" % p)
print()

TERMS = [
    (L.TERM, L.QUALIFIER,
     "the operands inside a deciding condition -- 17 -- and not the 39 the "
     "bare phrase denotes"),
    ("15 site", "d01ff32",
     "sites stating the census unqualified IN FILES d01ff32 TOUCHED, at "
     "%s -- not tree-wide, where the figure is larger and moves"
     % L.Q3_REV_PIN[:8]),
]
print("   %-30s %-38s %s" % ("term", "the population it denotes", "sites"))
bad_sites = []
for term, needs, population in TERMS:
    sites = [(p, n) for p, n in L.grep_sites(term) if L.is_mine(p)]
    bare = []
    for p, n in sites:
        w = L.window(p, n)
        if term == L.TERM:
            if L.disposition(p, n).startswith("***"):
                bare.append((p, n))
        elif needs not in w:
            bare.append((p, n))
    print("   %-30s %-38s %d, %d without it"
          % ("`%s`" % term, population[:38], len(sites), len(bare)))
    for p, n in bare:
        print("      *** %s:%s" % (p, n))
        bad_sites.append("%s:%s (%s)" % (p, n, term))
    print("      %s" % population)
R.gate(not bad_sites,
       "%d site(s) in this deliverable use a counted term without the "
       "population it denotes -- for the census phrase that population is "
       "the operands inside a deciding condition: %s"
       % (len(bad_sites), ", ".join(bad_sites)))
print()
print("""   AND THE EDIT THIS REPAIR MADE TO ITS OWN PREDICTION FILE, BOOKED
   HERE.  `code/repair_8d5e/PREDICTIONS.md` was committed before any
   script existed, and one row of it -- the sentence describing A-2 --
   was afterwards reworded so that it carries the unhyphenated words
   the scoring rule looks for.  NO PREDICTED VALUE WAS TOUCHED and the
   change is noted in the file itself.

   It is booked here because the alternative was worse in both
   directions: leaving it would have left this deliverable asserting
   the census unqualified in the one file that says what it set out to
   do, and editing it silently would be exactly the treatment this
   ticket refuses to give anybody else's record.  The rule this repair
   states for other people's prediction files -- an addendum, original
   standing -- is the rule it applied to mg-69d1's; its own is
   disclosed instead, and that difference is the finding-shaped part of
   this deliverable.""")
_pred = L.MINE_DIR + "/PREDICTIONS.md"
_disclosed = "clarified after this file was committed" in L.read_worktree(
    _pred)
print()
print("   the edit is disclosed in the file itself : %s"
      % ("yes" if _disclosed else "NO"))
R.gate(_disclosed,
       "this repair edited its own prediction file and the file does not say "
       "so; an undisclosed edit to a pre-run record is the thing this ticket "
       "refuses to do to anybody else's")
print()

# ---------------------------------------------------------------------------
L.rule("(iii) THE KINDS OF ARTIFACT THIS REPAIR EMITS")
print("""   The population is DERIVED, not listed: every path that differs
   between this branch and the newest revision at which %s does
   not exist, plus everything still uncommitted.  A path in no kind is
   a finding, because a list of kinds that does not cover its own
   population is the shape of both defects above.""" % L.MINE_DIR)
print()
R.check(_base is not None,
        "no revision of this branch lacks %s; the diff has no base and "
        "section (iii) is withdrawn" % L.MINE_DIR)
changed = L.changed_paths(_base) if _base else []
print("   base, derived : %s  %s"
      % (_base[:8] if _base else "-",
         L.subject(_base)[:56] if _base else ""))
print("   paths changed : %d" % len(changed))
print()


def kind_of(path):
    base = os.path.basename(path)
    if L.is_mine(path):
        if base.startswith("out_"):
            return ("this repair's transcript",
                    "written by run_all.sh, never by hand")
        if base == "PREDICTIONS.md":
            return ("this repair's pre-run record",
                    "one row reworded, DISCLOSED in (ii) and in the file")
        if path.startswith("docs/"):
            return ("this repair's own document", "new, and scored in (ii)")
        return ("this repair's own source", "new, and self-tested")
    if path.startswith("docs/"):
        return ("a live document", "EDITED to carry the qualifier")
    if base.startswith("out_") and base.endswith(".txt"):
        return ("another ticket's transcript",
                "REGENERATED by that ticket's own runner")
    if base == "PREDICTIONS.md":
        return ("another ticket's pre-run record",
                "ADDENDUM in place, original row standing")
    if base == "README.md":
        return ("another ticket's README",
                "EDITED -- a live claim about what its instrument covers")
    if path.endswith(".py"):
        return ("another ticket's source",
                "EDITED -- prose in (A-2) or the anchor itself (A-1)")
    return (None, None)


print("   %-52s %-30s %s" % ("path", "kind", "disposition"))
unkinded = []
for p in changed:
    k, d = kind_of(p)
    if k is None:
        unkinded.append(p)
        k, d = "*** NOT ACCOUNTED FOR", ""
    print("   %-52s %-30s %s" % (p, k, d))
print()
R.gate(not unkinded,
       "%d path(s) this repair changes fall in no named kind: %s"
       % (len(unkinded), ", ".join(unkinded)))
print("""   AND THE ONE KIND THAT CANNOT BE REPAIRED.  The commit message of
   `d01ff32` states the census unqualified, and mg-76cc's states the
   inverted reason.  A commit message is immutable; its disposition is
   a POINTER and not a fix, and k4 (i) counts the copy in mg-76cc's
   message precisely because the anchor now selects that message
   again -- which is A-1's second consequence stated as a benefit.""")
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT")
print("""   anchors this deliverable derives          : %d, of which %d on a
     property, %d pinned-and-derived, %d on a file's history and unused
   anchors that moved under the perturbation  : 0 required, measured above
   counted terms scored at every site         : %d
   paths this repair changes, all in a kind   : %d
"""
      % (len(ANCHORS),
         len([1 for _n, _v, h, _w in ANCHORS if h == "property"]),
         len([1 for _n, _v, h, _w in ANCHORS
              if h in ("property + pin", "pin + derivation")]),
         len(_history), len(TERMS), len(changed)))

sys.exit(R.emit())
