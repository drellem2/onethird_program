"""p2_rerun.py -- THE SUBJECTS AND THE AUDITORS, RE-RUN UNMODIFIED.

A repair that only runs its own instrument has measured its own opinion.  This
script runs, as subprocesses, with their stdout captured and their committed
transcripts untouched:

  d2_deletion.py   the instrument whose BOUND was narrowed (mg-eaef E5/E4)
  g1_provenance.py the script whose REASON was corrected  (mg-e34a E-1)
  k4_cancel.py     THE AUDITOR'S OWN INSTRUMENT, unedited -- the script that
                   raised E-1, re-run against the repaired tree

AND THE ONE THING THIS REPAIR DOES NOT CLOSE IS NAMED RATHER THAN COUNTED.
`d2_deletion.py` EXITS 1 AT HEAD and has since `bfd7948`: mg-eaef's E8, the
claim `AND THE PIN IS WHAT IT SAYS IT IS`, which is broken because `bfd7948` is
itself a commit with a two-clause `shape` guard and is newer than the pin.  That
is out of this ticket's scope.  It is REQUIRED here -- named, and required to be
the only broken claim -- so that "d2 is red" cannot be read as "d2 is red for a
reason nobody looked at", and so that a SECOND claim breaking is a finding.

k4 IS EXPECTED TO STILL BOOK ITS FINDING and that is not a failure of this
repair.  k4 greps the tree for the inverted sentence and counts every copy,
including the copies in its OWN transcript and prediction file, which are the
record of what it found and must not be edited.  What this script scores is
whether the copies it finds are still LIVE ASSERTIONS -- p3 (i) answers that --
and whether k4's MEASUREMENT, the three rows on a cancelling pair, still reads
the way it read before.  It must: this repair did not touch the row.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib69d1 as L                                              # noqa: E402

R = L.Report(
    selfpop="the 3 subprocess runs this script makes and the requirement "
            "that each produce a scoreable transcript",
    findpop="d2_deletion.py's claim scoreboard with the ONE claim mg-eaef's "
            "E8 is about named and excluded, g1_provenance.py's trailer and "
            "the reason its section (v) prints, and k4_cancel.py's three "
            "measured rows on a cancelling pair")

# The one claim this repair does not close, named rather than counted.
E8_CLAIM = "AND THE PIN IS WHAT IT SAYS IT IS"

L.banner("P2", "THE SUBJECTS AND THE AUDITOR, RE-RUN UNMODIFIED")
print("""
Nothing here is edited to stay green.  Each script is run where it lives, its
stdout captured, and its committed transcript left alone.
""")


def run(rel, timeout=3600):
    d = os.path.join(L.REPO, os.path.dirname(rel))
    p = subprocess.run([sys.executable, "-u", os.path.basename(rel)], cwd=d,
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout + p.stderr, p.returncode


# ---------------------------------------------------------------------------
L.rule("(i) d2_deletion.py -- THE NARROWED BOUND, IN ITS OWN RUN")
out, rc = run(L.D2_REL)
ok = R.check(bool(out.strip()), "d2_deletion.py produced no output; section "
                                "(i) is withdrawn rather than counted as "
                                "passing")
broken = [ln.strip() for ln in out.splitlines() if ln.strip().startswith("[BROKEN]")]
scored = [ln for ln in out.splitlines() if ln.strip().startswith("[HOLDS")
          or ln.strip().startswith("[BROKEN]")]
summary = [ln for ln in out.splitlines() if "claim(s) scored" in ln]
print("   exit %d, %d claim line(s), %d BROKEN" % (rc, len(scored), len(broken)))
for ln in summary:
    print("     %s" % ln.strip())
for ln in broken:
    print("     %s" % ln[:150])
print()
if ok:
    e8_only = (len(broken) == 1 and E8_CLAIM in broken[0])
    R.gate(e8_only,
           "d2_deletion.py has %d BROKEN claim(s) and mg-eaef's E8 accounts "
           "for exactly one of them (`%s`).  Any other broken claim is this "
           "repair's, and the ones this repair added are the two in THE BOUND "
           "OF THIS INSTRUMENT" % (len(broken), E8_CLAIM))
    for needle, what in (
            ("THE BOUND IS NOT WIDER THAN THE SWEEP", "the bound-vs-sweep claim"),
            ("EVERY EXPLICIT BOOLEAN OPERAND IS IN EXACTLY ONE NAMED COLUMN",
             "the totality claim"),
            ("not determined", "the `not determined` column"),
            ("DELETION REACHES THE TOP-LEVEL BOOLEAN OPERANDS",
             "the narrowed sentence")):
        present = needle in out
        print("   %-38s in d2's own stdout : %s"
              % (what, "yes" if present else "NO"))
        R.gate(present,
               "%s is not in d2_deletion.py's own output; it exists in the "
               "source and not in the artifact a reader sees" % what)
print()

# ---------------------------------------------------------------------------
L.rule("(ii) g1_provenance.py -- THE CORRECTED REASON, IN ITS OWN RUN")
g1out, g1rc = run(L.G1_REL)
ok = R.check(bool(g1out.strip()), "g1_provenance.py produced no output; "
                                  "section (ii) is withdrawn")
print("   exit %d" % g1rc)
for ln in g1out.splitlines():
    if ln.startswith(("SELF-ERRORS:", "FINDINGS:", "TOTAL BAD:")):
        print("     %s" % ln[:110])
print()
if ok:
    R.gate(g1rc == 0,
           "g1_provenance.py exits %d after this repair; it exited 0 before, "
           "and the repair changed prose and one label" % g1rc)
    for needle, what in (
            ("CONSPIRING pair", "the corrected reason"),
            ("both together (conspiracy)", "the corrected row LABEL"),
            ("mg-69d1", "the correcting ticket id")):
        present = needle in g1out
        print("   %-28s in g1's own stdout : %s"
              % (what, "yes" if present else "NO"))
        R.gate(present,
               "%s is not in g1_provenance.py's own output" % what)
    # THE SAME DISCRIMINATOR p3 (i) USES, applied to the artifact rather than
    # to the tree.  g1 does still print the old sentence -- inside the
    # paragraph that corrects it -- and a bare substring test would call that
    # a relapse.  What is scored is whether any copy stands WITHOUT its
    # correction, which is the property a reader of the transcript is exposed
    # to.
    lines = g1out.splitlines()
    stale = []
    for i, ln in enumerate(lines):
        if "changes that cancel would pass" not in ln:
            continue
        window = "\n".join(lines[max(0, i - 25):i + 26])
        if "mg-69d1" not in window:
            stale.append(i + 1)
    print("   %-28s in g1's own stdout : %d copy/copies, %d of them without a "
          "correction\n%swithin 25 lines"
          % ("the INVERTED reason",
             sum(1 for ln in lines
                 if "changes that cancel would pass" in ln),
             len(stale), " " * 34))
    R.gate(not stale,
           "g1_provenance.py PRINTS the inverted reason at line(s) %s with no "
           "correction within 25 lines, so the committed transcript carries it "
           "as an assertion whatever the source says"
           % ", ".join(str(x) for x in stale))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) k4_cancel.py -- THE AUDITOR'S OWN INSTRUMENT, UNEDITED")
print("""   k4 raised E-1.  It is re-run here against the repaired tree with
   not one character changed.  It is EXPECTED to still book its finding:
   it counts every copy of the sentence in the tree, and the copies that
   remain are in its own transcript and prediction file -- the record of
   what it found, which a repair does not get to edit.

   WHAT IS SCORED IS ITS MEASUREMENT, not its verdict.  The three rows
   it takes on a cancelling pair must read exactly as they read before,
   because this repair did not touch the row.  A repair that moved them
   would have repaired the row and left the reason, which is the
   opposite of the finding.""")
print()
k4out, k4rc = run(L.E34A_DIR + "/k4_cancel.py")
ok = R.check(bool(k4out.strip()), "k4_cancel.py produced no output; section "
                                  "(iii) is withdrawn")
if ok:
    print("   exit %d" % k4rc)
    rows = [ln.strip() for ln in k4out.splitlines()
            if ln.strip().startswith(("c1_branching.py (", "kern_a218.py (",
                                      "both together ("))]
    for ln in rows:
        print("     %s" % ln[:96])
    print()
    verdicts = {}
    for ln in rows:
        name = ln.split(" (")[0]
        verdicts[name] = "IDENTICAL" if ln.rstrip().endswith("IDENTICAL") \
            else "MOVED"
    print("   measured by the auditor, on this tree: %s"
          % "; ".join("%s %s" % (k, verdicts[k]) for k in sorted(verdicts)))
    R.gate(verdicts.get("c1_branching.py") == "MOVED"
           and verdicts.get("kern_a218.py") == "MOVED"
           and verdicts.get("both together") == "IDENTICAL",
           "k4's three rows on a cancelling pair do not read as they read "
           "before this repair (%s); the repair was supposed to touch the "
           "REASON and not the row"
           % "; ".join("%s %s" % (k, verdicts[k]) for k in sorted(verdicts)))
    findings = [ln.strip() for ln in k4out.splitlines()
                if ln.strip().startswith("FINDING:")]
    print("   k4 books %d finding(s); its rationale finding is EXPECTED and "
          "is not scored\n   as this repair's failure -- p3 (i) is where the "
          "copies are classified." % len(findings))
print()

L.finish(R)
