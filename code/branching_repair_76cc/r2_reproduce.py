"""r2_reproduce.py -- OPEN 2.  G-3, CLOSED ON FIVE OUTPUTS INSTEAD OF ONE.

mg-957f's F-2: mg-321d's G-3 -- "the documented reproduce command does not
reproduce" -- was closed by mg-7e58 on evidence in which 1 of 5 committed
outputs still reproduced byte for byte.  A gate shut on one-fifth of its
evidence is shut on the strength of the fifth that happened to work.

The other four are dealt with here, and the answer is in three parts.

  1.  WHY THEY DIFFER, PROVEN LINE BY LINE.  Every differing line is the same
      thing: a revision printed into a file that is then committed.  Not
      asserted -- each differing line is shown to become identical under ONE
      named substitution and no other.

  2.  WHY BYTE-IDENTITY CANNOT BE HAD AT ALL, DEMONSTRATED.  A transcript that
      prints HEAD is generated BEFORE the commit that commits it, and that
      commit moves HEAD.  The fixed point does not exist.  Shown rather than
      argued: the same tree at TWO different revisions, where the raw
      difference is the same set of lines both times and vanishes both times
      under the substitution.

  3.  THE CLAIM, NARROWED TO WHAT IT CAN HOLD, AND GATED.  "Reproduces byte for
      byte" is false for four of the five and will stay false.  What is true,
      and is checked here at 5 of 5, is:

        * every transcript names the revision it was taken at;
        * the FRESH run names the revision it was actually run at -- exactly,
          not approximately;
        * the committed record's revision is an ANCESTOR of the tree it sits
          in, and how stale it is is a number, printed;
        * after that ONE revision is normalised away in both, ZERO lines
          differ, in all five.

      The third and fourth are what "reproduces" now means, and the count of
      lines that the normalisation does NOT explain -- which must be 0 -- is
      the gate.

WHAT REMAINS is stated and not buried: the revision token itself is not
reproduced and cannot be.  A record that named some OTHER real revision would
normalise clean, and only the ancestry and staleness rows constrain it.  §(vi)
is a control that shows the normalisation is not a blanket -- a real,
non-revision difference must still be caught, and is.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import sys

import lib76cc as L

R = L.Report(
    selfpop="every clone, run_all.sh invocation, transcript read and "
            "normalisation this script performs",
    findpop="for each of the %d committed outputs: that it names a revision "
            "where it prints one, that the fresh run names its own HEAD "
            "exactly, that the recorded revision is an ancestor, and that 0 "
            "lines survive the normalisation -- plus the 2 impossibility rows "
            "in (v) and the 2 controls in (vi)" % len(L.FIVE_OUTPUTS))

L.banner("R2", "OPEN 2 -- G-3 WAS SHUT AT ONE REVISION")
print("""
1 of 5 is not shut.  Either the other four reproduce, or the claim is wrong
about what it is claiming.  Both are settled below, and the second turns out
to be the true one -- which is why the claim is narrowed here rather than
re-asserted.
""")

CLAIM = ("`./run_all.sh` in `code/branching_audit_58da/` now reproduces its "
         "committed outputs")
DOC_REL = "docs/OneThird-Bratteli-Path-Algebras-Mg7e58ProvenanceRepair.md"

L.rule("(i) THE CLAIM, AS mg-7e58 WROTE IT")
print("   %s" % DOC_REL)
print("     \"%s\"" % CLAIM)
print()
print("   Read out of the file, not remembered:")
doc = L.read_worktree(DOC_REL)
present = CLAIM.replace("`", "").replace("\n", " ") in \
    " ".join(doc.replace("`", "").split())
print("     the ABSOLUTE form is still in the document : %s"
      % ("yes" if present else "no -- it has been narrowed"))
print()

# ---------------------------------------------------------------------------
L.rule("(ii) run_all.sh IN A CLONE, AND WHAT REPRODUCES BYTE FOR BYTE")
print("""   In a clone, because run_all.sh redirects into the very files under
   test: run it in place and the record and the re-run are the same
   bytes for the reason that they were written by the same command.""")
print()

RUNALL = "./run_all.sh"


def run_all_in(tree):
    import subprocess
    p = subprocess.run([RUNALL], cwd=os.path.join(tree, L.S58DA_DIR),
                       capture_output=True, text=True, timeout=7200)
    return p.stdout + p.stderr, p.returncode


COMMITTED = {}
for name in L.FIVE_OUTPUTS:
    COMMITTED[name] = L.read_worktree(L.S58DA_DIR + "/" + name)

REC = L.recorded_rev(COMMITTED["out_g1_provenance.txt"])
R.check(REC is not None,
        "the committed out_g1_provenance.txt does not name the revision it "
        "was taken at, so nothing below can be scored against it")
REC_FULL = L.resolve(REC) if REC else None
REC_SUBJ = L.subject(REC_FULL) if REC_FULL else ""

print("   the committed record names its own revision : %s" % REC)
print("     %s" % REC_SUBJ[:88])
print()

tmp, tree = L.clone(message="mg-76cc: G-3, run_all.sh in a clone (mg-76cc)")
FRESH = {}
try:
    out, rc = run_all_in(tree)
    print("   run_all.sh exit %s (g4 is expected to exit 1 -- mg-d330's second"
          % rc)
    print("   finding, booked OPEN by mg-58da and not closed here)")
    print()
    for name in L.FIVE_OUTPUTS:
        with open(os.path.join(tree, L.S58DA_DIR, name)) as fh:
            FRESH[name] = fh.read()
    NEW_REV = L.head_rev(repo=tree)
    NEW_SUBJ = L.subject(NEW_REV, repo=tree)
finally:
    L.destroy(tmp)

print("   file                        committed  re-run  differing  "
      "reproduces")
print("                               lines      lines   lines      "
      "byte for byte")
raw_total = 0
raw_ok = 0
DIFFS = {}
for name in L.FIVE_OUTPUTS:
    a, b = COMMITTED[name], FRESH[name]
    d = L.differing_lines(a, b)
    DIFFS[name] = d
    raw_total += len(d)
    raw_ok += (len(d) == 0)
    print("     %-26s %-10d %-7d %-10d %s"
          % (name, len(a.splitlines()), len(b.splitlines()), len(d),
             "YES" if not d else "no"))
print()
print("   %d of %d reproduce byte for byte, over %d differing lines in all."
      % (raw_ok, len(L.FIVE_OUTPUTS), raw_total))
print("   Population: the %d files code/branching_audit_58da/run_all.sh "
      "writes." % len(L.FIVE_OUTPUTS))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) EVERY DIFFERING LINE, AND WHAT EXPLAINS IT")
print("""   Not "they are all revisions" -- each line is shown to become
   identical under ONE substitution, the recorded revision for the
   recorded one and the clone's own HEAD for the fresh one, and lines
   that do NOT are printed in full and counted.""")
print()
unexplained = []
for name in L.FIVE_OUTPUTS:
    for lineno, x, y in DIFFS[name]:
        nx, _ = L.normalize(x or "", REC_FULL or "", REC_SUBJ)
        ny, _ = L.normalize(y or "", NEW_REV, NEW_SUBJ)
        ok = nx == ny
        print("     %-26s line %-4d %s"
              % (name, lineno, "revision substitution" if ok
                 else "NOT EXPLAINED"))
        print("       committed: %s" % ((x or "<absent>")[:92]))
        print("       re-run   : %s" % ((y or "<absent>")[:92]))
        if not ok:
            unexplained.append((name, lineno, x, y))
print()
print("   differing lines explained by ONE revision substitution : %d of %d"
      % (raw_total - len(unexplained), raw_total))
print()

# ---------------------------------------------------------------------------
L.rule("(iv) THE FIVE, COMPARED WITH THAT ONE REVISION NORMALISED AWAY")
print("""   The normalisation's population, named: the 40-, 12- and 8-character
   forms of ONE revision, and that revision's subject truncated to the
   %d characters g1 truncates it to.  Nothing else is touched -- 286d5030
   and ed9cde49 are pinned constants in these transcripts and MUST still
   reproduce byte for byte, and they do, or the rows below would not be
   zero.""" % L.SUBJ_WIDTH)
print()
print("   file                        substitutions  substitutions  lines")
print("                               (committed)    (re-run)       differing")
norm_ok = 0
norm_total = 0
for name in L.FIVE_OUTPUTS:
    na, ca = L.normalize(COMMITTED[name], REC_FULL or "", REC_SUBJ)
    nb, cb = L.normalize(FRESH[name], NEW_REV, NEW_SUBJ)
    d = L.differing_lines(na, nb)
    norm_total += len(d)
    norm_ok += (len(d) == 0)
    print("     %-26s %-14d %-14d %d" % (name, ca, cb, len(d)))
    for lineno, x, y in d[:6]:
        print("       line %-4d  -%s" % (lineno, (x or "<absent>")[:80]))
        print("                  +%s" % ((y or "<absent>")[:80]))
    R.gate(len(d) == 0,
           "%s does not reproduce even with the one revision it names "
           "normalised away: %d lines still differ, and they are not "
           "revisions" % (name, len(d)))
print()
print("   REPRODUCE UNDER THE NAMED NORMALISATION : %d of %d, %d lines "
      "unexplained." % (norm_ok, len(L.FIVE_OUTPUTS), norm_total))
print()

# the transcript must be honest about where it was taken
FRESH_REC = L.recorded_rev(FRESH["out_g1_provenance.txt"])
print("   the fresh run names its own revision  : %s" % FRESH_REC)
print("   the clone's actual HEAD               : %s" % NEW_REV[:12])
R.gate(FRESH_REC == NEW_REV[:12],
       "the fresh run's transcript names %s and the clone's HEAD is %s; the "
       "transcript is not naming the revision it was taken at, and then the "
       "normalisation is normalising away a claim rather than a fact"
       % (FRESH_REC, NEW_REV[:12]))
if REC_FULL:
    anc = L.is_ancestor(REC_FULL, "HEAD")
    dist = L.distance(REC_FULL, L.head_rev()) if anc else None
    print("   the committed record's revision       : %s" % REC)
    print("     an ancestor of this branch          : %s"
          % ("yes" if anc else "NO"))
    print("     commits from it to this HEAD        : %s" % dist)
    print("       0 means the record was taken at the tree's current HEAD and")
    print("       has NOT yet been committed; it becomes 1 the moment it is,")
    print("       and 1 is the freshest a committed record can ever be.  (v)")
    print("       is why it can never be 0 once committed.")
    R.gate(anc,
           "the committed record names %s, which is NOT an ancestor of this "
           "branch; the transcript claims a provenance this history does not "
           "have" % REC)
print()

# ---------------------------------------------------------------------------
L.rule("(v) WHY BYTE-IDENTITY CANNOT BE HAD -- DEMONSTRATED, NOT ARGUED")
print("""   The transcript prints HEAD.  Committing the transcript makes a new
   commit, so HEAD is not what the transcript says by the time the
   transcript is in the tree.  A record that reproduced byte for byte
   would have to name the commit that contains it, which is a sha over
   its own bytes.  No such file exists.

   Shown, rather than argued: the SAME tree at TWO revisions -- the clone
   above, and a clone with one further empty commit.  If the difference
   were incidental, the two would differ in different places, or one of
   them would come back clean.""")
print()
tmp, tree = L.clone(empty_extra=True,
                    message="mg-76cc: G-3, second revision (mg-76cc)")
try:
    out2, rc2 = run_all_in(tree)
    FRESH2 = {}
    for name in L.FIVE_OUTPUTS:
        with open(os.path.join(tree, L.S58DA_DIR, name)) as fh:
            FRESH2[name] = fh.read()
    NEW_REV2 = L.head_rev(repo=tree)
    NEW_SUBJ2 = L.subject(NEW_REV2, repo=tree)
finally:
    L.destroy(tmp)

print("   revision                 raw differing lines   normalised")
rows = [(NEW_REV[:12], FRESH, NEW_REV, NEW_SUBJ),
        (NEW_REV2[:12], FRESH2, NEW_REV2, NEW_SUBJ2)]
sets = []
for rev, fresh, r, s in rows:
    raw = sum(len(L.differing_lines(COMMITTED[n], fresh[n]))
              for n in L.FIVE_OUTPUTS)
    nrm = 0
    for n in L.FIVE_OUTPUTS:
        na, _ = L.normalize(COMMITTED[n], REC_FULL or "", REC_SUBJ)
        nb, _ = L.normalize(fresh[n], r, s)
        nrm += len(L.differing_lines(na, nb))
    lines = set()
    for n in L.FIVE_OUTPUTS:
        for lineno, _x, _y in L.differing_lines(COMMITTED[n], fresh[n]):
            lines.add((n, lineno))
    sets.append(lines)
    print("     %-22s %-21d %d" % (rev, raw, nrm))
print()
same_set = sets[0] == sets[1]
print("   the two revisions differ from the record at THE SAME %d (file, line)"
      % len(sets[0]))
print("   positions : %s" % ("yes" if same_set else "NO"))
R.gate(same_set,
       "two different revisions of the same tree differ from the committed "
       "record at DIFFERENT places (%d vs %d, %d in common); then the "
       "difference is not the revision and the account in (iii) is wrong"
       % (len(sets[0]), len(sets[1]), len(sets[0] & sets[1])))
R.gate(len(sets[0]) > 0,
       "the committed record reproduces byte for byte at the clone's own "
       "revision, so the impossibility argument in (v) is about nothing and "
       "this whole section is withdrawn")
print()

# ---------------------------------------------------------------------------
L.rule("(vi) THE NORMALISATION IS NOT A BLANKET -- TWO CONTROLS")
print("""   A comparison that forgives everything reproduces everything.  So two
   perturbations of the COMMITTED side, each of which must still be
   caught after normalisation: one a figure, one a whole line.""")
print()

CONTROLS = [
    ("a figure changed in out_g3_findings.txt",
     "out_g3_findings.txt", "24 FINDINGS", "23 FINDINGS"),
    ("a line changed in out_g4_fleet.txt",
     "out_g4_fleet.txt", "TOTAL BAD: 2", "TOTAL BAD: 0"),
]
print("   control                                     applied  caught after")
print("                                                        normalisation")
for label, name, old, new in CONTROLS:
    src = COMMITTED[name]
    if src.count(old) < 1:
        R.selferr("the control %r could not be applied: %r does not occur in "
                  "%s.  It is DROPPED from the population rather than counted "
                  "as passing" % (label, old, name))
        print("     %-42s no       DROPPED" % label[:42])
        continue
    bent = src.replace(old, new, 1)
    na, _ = L.normalize(bent, REC_FULL or "", REC_SUBJ)
    nb, _ = L.normalize(FRESH[name], NEW_REV, NEW_SUBJ)
    caught = len(L.differing_lines(na, nb)) > 0
    print("     %-42s yes      %s" % (label[:42], "YES" if caught else "NO"))
    R.gate(caught,
           "the control %r survives the normalisation: a real, non-revision "
           "difference in %s is not caught, so '0 lines differ' means nothing"
           % (label, name))
print()

# ---------------------------------------------------------------------------
L.rule("VERDICT ON OPEN 2")
print("""   G-3 IS CLOSED ON FIVE, AND THE CLAIM IS THE NARROWED ONE.

     %d of %d committed outputs reproduce byte for byte.  That number
     cannot be raised, and (v) shows why: a transcript that names HEAD is
     written before the commit that commits it.

     %d of %d reproduce with that ONE revision normalised away, over %d
     substitutions on the committed side, with %d lines unexplained -- and
     the two controls in (vi) show the normalisation still catches a real
     difference.

   WHAT REMAINS, stated rather than buried: the revision token itself is
   not reproduced.  A transcript naming some other real revision would
   normalise clean; what constrains it is the ancestry row and the
   staleness figure in (iv), and those are weaker than bytes.  The
   absolute claim is withdrawn in the document rather than re-asserted.
""" % (raw_ok, len(L.FIVE_OUTPUTS), norm_ok, len(L.FIVE_OUTPUTS),
       sum(L.normalize(COMMITTED[n], REC_FULL or "", REC_SUBJ)[1]
           for n in L.FIVE_OUTPUTS),
       norm_total))

sys.exit(R.emit())
