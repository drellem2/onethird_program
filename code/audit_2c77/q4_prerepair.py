"""q4_prerepair.py -- DO NOT DISTURB WHAT IS CONFIRMED.

mg-e34a's confirmation that the kernel half is genuinely back is `the pre-repair
predicate run against 7 inputs with 0 going backwards at either grain`.  mg-69d1
edited `g1_provenance.py` -- which IS the predicate `k1_prerepair.py` runs on
both sides of that comparison -- and re-ran mg-e34a's `k4_cancel.py` but not its
`k1_prerepair.py`.  So it is re-run here, unmodified, as a subprocess, at
`d01ff32`.

A REGRESSION HERE OUTRANKS EVERYTHING ELSE THIS AUDIT REPORTS, and the gates are
written so that it cannot be lost among them: the three coverage numbers are
gated one at a time, each with its own message.

k1 EXITS 1 AND THAT IS NOT A REGRESSION.  It books mg-e34a's own three findings,
which mg-69d1 named as NOT CLOSED (E-2 and the two pin findings).  Gating on k1's
exit code would be requiring this audit's subject to have closed tickets it said
it was not closing.  So the gate is on the three COVERAGE numbers, and separately
on the finding SET: a finding at HEAD that is not in the committed transcript is
a regression even when the count is unchanged.

NOTHING IS WRITTEN.  k1's stdout is captured; `out_k1_prerepair.txt` is read and
never opened for writing.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lib2c77 as L                                              # noqa: E402

R = L.Report(
    selfpop="the subprocess run of k1_prerepair.py, the parse of its verdict "
            "block and of its finding list, and the read of its committed "
            "transcript",
    findpop="the three coverage numbers of mg-e34a's pre-repair comparison -- "
            "backwards at the exit grain, backwards at the finding grain, and "
            "files named by an old finding and by no new one -- each gated "
            "separately; the declared input count; and the finding SET at "
            "d01ff32 against the finding set in the committed transcript")

L.banner("Q4", "mg-e34a's PRE-REPAIR PREDICATE, RE-RUN AT THIS HEAD")

HEAD = L.head_rev()
K1 = os.path.join(L.REPO, L.E34A_DIR, "k1_prerepair.py")
print()
print("   HEAD                     : %s" % HEAD[:8])
print("   the script, run unmodified: %s" % (L.E34A_DIR + "/k1_prerepair.py"))
print("   mg-69d1 re-ran k4_cancel.py from this suite and did not re-run this")
print("   one; g1_provenance.py, which it edited, is the predicate this script")
print("   runs on both sides.")
print()

if not os.path.exists(K1):
    R.selferr("%s does not exist; the whole of this script is DROPPED rather "
              "than counted as passing" % K1)
    out, rc = "", None
else:
    p = subprocess.run([sys.executable, "k1_prerepair.py"],
                       cwd=os.path.dirname(K1), capture_output=True,
                       text=True, timeout=3600)
    out, rc = p.stdout + p.stderr, p.returncode

L.rule("(i) THE VERDICT BLOCK, PARSED OUT OF ITS OWN STDOUT")


def number_after(text, label):
    m = re.search(re.escape(label) + r"\s*:\s*(\d+)", text)
    return int(m.group(1)) if m else None


GRAINS = [
    ("Backwards at the exit grain", 0,
     "coverage went backwards at the EXIT grain on %s input(s) after mg-69d1 "
     "edited g1_provenance.py; mg-e34a's confirmation that the kernel half is "
     "back was 0 at this grain and this OUTRANKS every other finding in this "
     "audit"),
    ("Backwards at the finding grain", 0,
     "coverage went backwards at the FINDING grain on %s input(s) after "
     "mg-69d1 edited g1_provenance.py; mg-e34a's confirmation was 0 at this "
     "grain and this OUTRANKS every other finding in this audit"),
    ("Files named by an old finding and by no new one", 0,
     "%s file(s) are named by an old finding and by no new one -- coverage "
     "lost inside a green column, at the grain neither r3 nor mg-957f used"),
]
print()
print("   %-52s %-8s %-8s %s" % ("what k1 measures", "at HEAD", "required",
                                 "verdict"))
for label, want, msg in GRAINS:
    got = number_after(out, label)
    if got is None:
        R.selferr("`%s` could not be parsed out of k1's stdout; that gate is "
                  "DROPPED rather than counted as passing" % label)
        continue
    print("   %-52s %-8d %-8d %s"
          % (label, got, want, "ok" if got == want else "*** REGRESSION"))
    R.gate(got == want, msg % got)
print()

inputs = re.search(r"against the same (\d+) inputs", out)
n_inputs = int(inputs.group(1)) if inputs else None
print("   inputs k1 declares and runs : %s" % n_inputs)
R.gate(n_inputs == 7,
       "k1 ran against %s inputs and mg-e34a's confirmation is stated over 7; "
       "a comparison over a different population is a different comparison"
       % n_inputs)
print("   k1's exit code              : %s   (1 is expected: it books "
      "mg-e34a's own\n                                 three findings, which "
      "mg-69d1 named as NOT CLOSED)" % rc)
print()

# ---------------------------------------------------------------------------
L.rule("(ii) THE FINDING SET, AGAINST THE COMMITTED TRANSCRIPT")
print("""   A count that did not move can still be a different set.  Both
   finding lists are parsed and compared after normalising every hex
   token of 7 or more characters -- a revision that moved is not a
   finding that changed.""")
print()


def findings_of(text):
    got = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("FINDING:"):
            got.append(re.sub(r"\b[0-9a-f]{7,}\b", "<rev>", s[8:].strip()))
    return got


now = findings_of(out)
try:
    then = findings_of(L.read_worktree(L.E34A_DIR + "/out_k1_prerepair.txt"))
except (IOError, OSError) as e:
    R.selferr("the committed transcript could not be read (%s); the set "
              "comparison is DROPPED rather than counted as passing" % e)
    then = None

print("   findings at %s          : %d" % (HEAD[:8], len(now)))
if then is not None:
    print("   findings in the committed transcript : %d" % len(then))
    new = [f for f in now if f not in then]
    gone = [f for f in then if f not in now]
    print()
    for f in now:
        mark = "*** NEW" if f in new else "also in the transcript"
        print("     [%s] %s" % (mark, f[:110]))
    if gone:
        print()
        for f in gone:
            print("     [no longer booked] %s" % f[:110])
    print()
    R.gate(not new,
           "k1 books %d finding(s) at %s that are not in its committed "
           "transcript: %s.  A finding count that did not move is not a "
           "finding set that did not move"
           % (len(new), HEAD[:8], " | ".join(f[:90] for f in new)))
    print("   %d new, %d no longer booked." % (len(new), len(gone)))
print()

# ---------------------------------------------------------------------------
L.rule("(iii) WHAT k1 IS COMPARING NOW, AND WHAT IT WAS COMPARING BEFORE")
print("""   The two new findings are not noise.  `libe34a` derives the subject
   of the comparison rather than writing it down:

       REPAIR_REV = the last commit that touched g1_provenance.py
       PRE_REV    = its first parent

   and mg-69d1 TOUCHED g1_provenance.py.  So the derivation now returns
   mg-69d1's own commit, and `the predicate as it stood before the
   repair` is no longer mg-76cc's predecessor -- it is mg-69d1's.

   The check is done here by importing libe34a and reading the values
   the instrument actually uses, and by asking git the same question
   from the repair's parent.""")
print()
sys.path.insert(0, os.path.join(L.REPO, L.E34A_DIR))
try:
    import libe34a as E                                          # noqa: E402
    repair_rev, pre_rev = E.REPAIR_REV, E.PRE_REV
except Exception as e:                                           # noqa: BLE001
    R.selferr("libe34a could not be imported (%s); section (iii) is DROPPED "
              "rather than counted as passing" % e)
    repair_rev = pre_rev = None

pinned = None
for line in L.read_worktree(L.R76CC_DIR + "/lib76cc.py").splitlines():
    if line.strip().startswith("REV_957F"):
        pinned = line.split('"')[1]
at_parent = L.git("log", "--format=%H", "-1", "e5787e1", "--",
                  L.S58DA_DIR + "/g1_provenance.py").strip()

if repair_rev:
    print("   %-56s %s" % ("libe34a.REPAIR_REV, as the instrument derives it "
                           "now", repair_rev[:8]))
    print("   %-56s %s" % ("libe34a.PRE_REV -- `the predicate before the "
                           "repair`", (pre_rev or "?")[:8]))
    print("   %-56s %s" % ("lib76cc.REV_957F -- `g1 BEFORE mg-76cc`, the "
                           "pin", (pinned or "?")[:8]))
    print("   %-56s %s" % ("the same derivation run from d01ff32's PARENT "
                           "(e5787e1)", at_parent[:8]))
    print()
    print("   at e5787e1 the derivation returned mg-76cc's repair and PRE_REV")
    print("   agreed with the pin.  At this HEAD it returns mg-69d1's commit,")
    print("   and `before the repair` means before MG-69D1 -- which is")
    print("   mg-76cc's ALREADY-REPAIRED predicate on both sides.")
    print()
    R.gate(pre_rev == pinned,
           "mg-e34a's PRE-REPAIR COMPARISON NO LONGER COMPARES MG-76CC's "
           "REPAIR.  `libe34a.REPAIR_REV` is derived as the last commit "
           "touching g1_provenance.py and mg-69d1 touched it, so REPAIR_REV "
           "moved from %s (mg-76cc's repair) to %s (mg-69d1's own) and "
           "PRE_REV moved from %s -- lib76cc's pin, `g1 BEFORE mg-76cc` -- to "
           "%s.  Both sides of the comparison are now mg-76cc's REPAIRED "
           "predicate, differing only in the prose mg-69d1 edited.  The three "
           "coverage numbers still read 0/0/0 and they are 0 for a different "
           "reason: `the pre-repair predicate run against 7 inputs with 0 "
           "going backwards` is the confirmation that the kernel half is "
           "back, and this run does not re-derive it.  k1 says so itself, in "
           "the two findings above, and mg-69d1 re-ran k4_cancel.py from this "
           "suite but not k1"
           % (at_parent[:8], repair_rev[:8], (pinned or "?")[:8],
              (pre_rev or "?")[:8]))
print()

L.finish(R)
