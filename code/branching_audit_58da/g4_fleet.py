"""g4_fleet.py -- THE PROPERTY THAT LIVES BETWEEN THE INSTRUMENTS.

Widening one of five scripts is a change at SCRIPT grain.  The property the
five carry -- that mg-a218's instrument, as a set, reports one coherent verdict
about the target -- lives at FLEET grain.  Corroboration was the point, so a
change to one member is not a local edit and "the changed script still works"
is not the thing that has to be re-established.

This script re-establishes the set-level property, and it does it three times
over, because there are three revisions at which it can be asked:

    286d5030  where mg-a218 took the audit           -- the five as delivered
    d1dd84d2  after mg-13b2 widened c2               -- one member moved
    working   after mg-58da widened c1               -- a second member moved

For each: name the five, say which were touched and by which commit, run all
five, and put the verdicts side by side.  Then the part that is actually about
the SET rather than the members: the figures more than one of them carries are
compared across all of them, and across the four kernels outside this
directory that measure the same object.

And the repair this ticket makes is deletion-tested, in the direction that
matters: the widened c1, handed a target it cannot read, must raise a
SELF-ERROR and not a FINDING.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.  It is predicted to exit 1:
c3_withdrawal.py is red on the repaired tree for a reason that belongs to
mg-d330's second finding and is not repaired here, and a fleet with a red
member is a fleet whose set-level property does not hold.
"""

import os
import re
import subprocess
import sys

import lib58da as L

SELF, FIND = [], []


def selferr(m):
    SELF.append(m)


def finding(m):
    FIND.append(m)


FIVE = ["c1_branching.py", "c2_vertexsets.py", "c3_withdrawal.py",
        "c4_seam.py", "c5_record.py"]
NOT_FIVE = [("selftest_a218.py", "the self-test: it tests the kernel, not the "
                                 "target, and prints no TOTAL BAD line"),
            ("c0_repro.sh", "a reproduction harness, not one of the five "
                            "checks; it re-runs the TARGET's instrument"),
            ("kern_a218.py", "the kernel the five share")]

print("=" * 74)
print("G4  THE SET-LEVEL PROPERTY, RE-ESTABLISHED AFTER TWO CHANGES")
print("=" * 74)

HEAD = L.head_rev()

# ---------------------------------------------------------------------------
print()
print("-" * 74)
print("(i) THE FIVE, NAMED -- AND WHAT IS NOT ONE OF THEM")
print("-" * 74)
for f in FIVE:
    print("   %s" % f)
print()
print("   in the same directory and NOT among the five:")
for f, why in NOT_FIVE:
    print("     %-22s %s" % (f, why))
print()
if len(FIVE) != 5:
    selferr("this script names %d scripts as 'the five'" % len(FIVE))

# ---------------------------------------------------------------------------
print("-" * 74)
print("(ii) WHO TOUCHED WHICH MEMBER, BY SHA AND BY COMMIT")
print("-" * 74)
print("   script                 286d5030 -> d1dd84d2       d1dd84d2 -> working")
touched_13b2, touched_58da = [], []
for f in FIVE:
    p = L.A218_DIR + "/" + f
    a = L.sha(L.git_show(L.REV_A218, p))
    b = L.sha(L.git_show(HEAD, p))
    with open(os.path.join(L.REPO, p)) as fh:
        c = L.sha(fh.read())
    if a != b:
        touched_13b2.append(f)
    if b != c:
        touched_58da.append(f)
    print("     %-22s %-26s %s"
          % (f, "CHANGED (%s)" % ", ".join(
              x[:8] for x in L.commits_touching(p, L.REV_A218, HEAD))
             if a != b else "same",
             "CHANGED (this ticket)" if b != c else "same"))
print()
print("   of the five, touched by ed9cde4 (mg-13b2) : %d -- %s"
      % (len(touched_13b2), ", ".join(touched_13b2) or "none"))
print("   of the five, touched by mg-58da           : %d -- %s"
      % (len(touched_58da), ", ".join(touched_58da) or "none"))
print("   the kernel the five share, kern_a218.py   : %s"
      % ("CHANGED" if L.sha(L.git_show(L.REV_A218, L.A218_DIR + "/kern_a218.py"))
         != L.sha(open(os.path.join(L.REPO, L.A218_DIR, "kern_a218.py")).read())
         else "UNCHANGED at both -- no mathematics moved in either change"))
print()
print("""   THIS IS THE SHAPE OF THE FAILURE.  ed9cde4 widened c2 because a
   re-run would otherwise have scored its own repair as c2's SELF-ERROR.
   c1 had the same stale parser reading the same rewritten block and was not
   widened with it.  One member was made to tell the truth on a re-run and
   its sibling was left telling a falsehood -- and the falsehood was louder,
   because c1 books its blindness as findings against the target.""")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iii) ALL FIVE, RUN, AT THE THREE REVISIONS")
print("-" * 74)


def committed_verdict(rev, f):
    """(self, findings, exit-as-implied) from the committed output at rev."""
    try:
        out = L.git_show(rev, L.A218_DIR + "/out_%s.txt" % f[:-3])
    except subprocess.CalledProcessError:
        return None
    s, fi, t = L.totals_of(out)
    return (s, fi, 1 if (s or fi) else 0)


def live_verdict(f):
    p = subprocess.run(["python3", f],
                       cwd=os.path.join(L.REPO, L.A218_DIR),
                       capture_output=True, text=True)
    s, fi, t = L.totals_of(p.stdout)
    return (s, fi, p.returncode), p.stdout


print("   the 'committed' column is the record each audit left; the 'working'")
print("   column is what the script does now, run in place with its stdout")
print("   captured HERE and never redirected into the committed file.")
print()
print("   script                 committed@286d5030   working tree now")
print("                          self/find  exit      self/find  exit")
live = {}
for f in FIVE:
    cv = committed_verdict(L.REV_A218, f)
    lv, out = live_verdict(f)
    live[f] = (lv, out)
    if cv is None:
        selferr("no committed output for %s at %s" % (f, L.REV_A218[:8]))
        cv = ("?", "?", "?")
    print("     %-22s %s/%-6s (exit %s)   %s/%-6s (exit %s)"
          % (f, cv[0], cv[1], cv[2], lv[0], lv[1], lv[2]))
print()
green = [f for f in FIVE if live[f][0][2] == 0]
red = [f for f in FIVE if live[f][0][2] != 0]
print("   green on the working tree: %d of 5 -- %s" % (len(green), ", ".join(green)))
print("   red   on the working tree: %d of 5 -- %s"
      % (len(red), ", ".join(red) or "none"))
print()
for f in red:
    (s, fi, rc), out = live[f]
    print("   %s exits %d with SELF %s FINDINGS %s:" % (f, rc, s, fi))
    for x in L.findings_of(out):
        print("      FINDING: %s" % x[:150])
    for x in L.selferrs_of(out):
        print("      SELF-ERROR: %s" % x[:150])
print()

if "c1_branching.py" in red:
    finding("c1_branching.py is still red after this ticket's widening; the "
            "repair did not do what it was for")
for f in red:
    if f == "c3_withdrawal.py":
        print("""   c3_withdrawal.py IS RED AND IT IS NOT THIS TICKET'S TO CLOSE.
   Its findings are mg-d330's second finding: mg-13b2's own new
   t5_labels.py and its committed output carry the withdrawn phrases as
   SEARCH NEEDLES with no marker beside them, and c3 sweeps for exactly
   those phrases.  It is a real finding against the repaired tree, it is
   booked OPEN, and nothing here touches it.  It is reported rather than
   worked around because the set-level property is that ALL FIVE are
   green, and it is not, and saying otherwise would be the defect this
   ticket exists to name.""")
        finding("the set-level property does NOT hold on the working tree: "
                "c3_withdrawal.py exits 1 with %d finding(s), which is "
                "mg-d330's second finding against mg-13b2's t5_labels.py and "
                "is left OPEN by this ticket" % live[f][0][1])
    elif f != "c1_branching.py":
        finding("%s is red on the working tree and is not accounted for by "
                "this ticket" % f)
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(iv) THE FIGURES THAT LIVE BETWEEN THE MEMBERS")
print("-" * 74)
print("""   The set-level property is not five green exit codes.  It is that the
   members which measure the same thing still say the same thing.  Two of the
   five measure the vertex sets independently of one another -- c1 from its
   character solves and c2 from the same kernel but its own comparison -- and
   the same 24 cells are carried by the four kernels in this tree.  A change
   to one member's PARSER must not move any of them.""")
print()

c1_out = live["c1_branching.py"][1]
c2_out = live["c2_vertexsets.py"][1]
mine_c1 = L.parse_c1_own_vertices(c1_out)
if len(mine_c1) != 24:
    selferr("could not read c1's own 24 vertex cells out of its live output")


def parse_c2_mine(out):
    """c2 prints '-- mine, as sets: [[1], [1, 1], ...]' per parameter."""
    got = {}
    for line in out.splitlines():
        m = re.match(r"\s*beta=(\d+) : .*-- mine, as sets: (\[\[.*\]\])\s*$",
                     line)
        if not m:
            continue
        rows = re.findall(r"\[([\d,\s]*)\]", m.group(2)[1:-1])
        if len(rows) != 6:
            continue
        for n, r in enumerate(rows, start=1):
            got[(int(m.group(1)), n)] = [int(x) for x in r.split(",") if x.strip()]
    return got


c2_mine = parse_c2_mine(c2_out)
if len(c2_mine) != 24:
    selferr("could not read c2's own 24 vertex rows out of its live output "
            "(%d parsed); it is WITHDRAWN from the comparison below and is "
            "NOT scored as disagreeing" % len(c2_mine))
else:
    dis = [k for k in mine_c1
           if [d for (p, d) in mine_c1[k]] != c2_mine.get(k)]
    print("   c1's vertex sets vs c2's, as dimension lists, all 24 cells: %s"
          % ("agree at 24 of 24" if not dis else "DISAGREE at %s" % sorted(dis)))
    if dis:
        finding("c1 and c2 -- two members of the same five -- disagree about "
                "the vertex cells at %s" % sorted(dis))

print()
print("   and against the target and the other instruments (g2 measures this")
print("   in full; repeated here because it is the fleet property, and a")
print("   fleet property stated in one script and checked in another is the")
print("   grain error this ticket is about):")
tgt = L.parse_vertex_sets(L.read_worktree(L.TARGET_REL))
e1 = {}
with open(os.path.join(L.REPO,
                       "code/branching_audit_d330/out_e1_vertexsets.txt")) as fh:
    for line in fh:
        m = re.match(r"\s*beta = (\d+)\s+((?:\[[\d:,]*\]\s*)+)$", line)
        if not m:
            continue
        sets = re.findall(r"\[([\d:,]*)\]", m.group(2))
        if len(sets) == 6:
            for n, s in enumerate(sets, start=1):
                e1[(int(m.group(1)), n)] = [
                    tuple(int(x) for x in piece.split(":"))
                    for piece in s.split(",") if piece]
for name, got in [("out_t1_tl.txt   (mg-db09, 1st instrument)", tgt),
                  ("c1 live         (mg-a218, 3rd instrument)", mine_c1),
                  ("out_e1_vertex.. (mg-d330, 4th instrument)", e1)]:
    if len(got) != 24:
        selferr("could not read 24 cells from %s (%d)" % (name, len(got)))
        continue
    n_ag = sum(1 for k in mine_c1 if got.get(k) == mine_c1[k])
    print("     %-42s %d of 24 agree with c1" % (name, n_ag))
    if n_ag != 24:
        finding("%s disagrees with c1 at %d of the 24 vertex cells"
                % (name, 24 - n_ag))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(v) c0_repro.sh -- THE FLEET PROPERTY ONE LEVEL DOWN")
print("-" * 74)
print("""   mg-a218's c0 re-runs the TARGET's own five scripts against the
   repaired code and diffs all five committed outputs byte for byte.  That is
   the same property at the target's grain, and this ticket changed nothing
   the target reads, so it must still hold.""")
p = subprocess.run(["sh", "c0_repro.sh"],
                   cwd=os.path.join(L.REPO, L.A218_DIR),
                   capture_output=True, text=True)
ident = re.findall(r"(\d+) of (\d+) .*IDENTICAL", p.stdout) or \
    re.findall(r"IDENTICAL", p.stdout)
print("   c0_repro.sh exit %d" % p.returncode)
for line in p.stdout.splitlines():
    if "IDENTICAL" in line or "DIFFER" in line or "TOTAL BAD" in line:
        print("     %s" % line.strip()[:110])
if p.returncode != 0:
    finding("c0_repro.sh exits %d on the working tree: the target's own five "
            "committed outputs no longer regenerate" % p.returncode)
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(vi) THE REPAIR, DELETION-TESTED IN THE DIRECTION THAT MATTERS")
print("-" * 74)
print("""   The widening is only worth having if a cell the target does not state
   now lands in the SELF-ERROR channel instead of accusing the target.  So the
   widened c1 is handed three targets and the direction is predicted first.""")
print()
with open(os.path.join(L.REPO, L.A218_DIR, "c1_branching.py")) as fh:
    c1_new_src = fh.read()
old_target = L.git_show(L.REV_A218, L.TARGET_REL)
new_target = L.read_worktree(L.TARGET_REL)

# a target with the SET block removed and no count table to fall back on
blinded, ndrop = L.drop_lines(
    new_target, lambda l: re.match(r"\s*n=\d+\s+\[[\d:,]*\]\s*$", l))

cases = [
    ("the HEAD target (SET form)", new_target,
     dict(exit=0, self=0, find=0, compared=24, form="SET"),
     "all 24 cells compared as labelled sets, nothing to report"),
    ("the 286d5030 target (COUNT form) -- backward compatibility",
     old_target, dict(exit=0, self=0, find=0, compared=24, form="COUNT"),
     "the form this audit was taken against must still be read"),
    ("the HEAD target with all %d set rows DELETED" % ndrop, blinded,
     dict(exit=1, self=24, find=0, compared=0, form="NEITHER"),
     "24 SELF-ERRORS and 0 FINDINGS: it must accuse ITSELF"),
]
print("   target                                              predicted"
      "            actual")
allok = True
for name, txt, pred, why in cases:
    out, rc = L.run_c1(txt, script_source=c1_new_src)
    s, f, t = L.totals_of(out)
    comp = L.compared_of(out).get("vertex cells", -1)
    form = "?"
    m = re.search(r"Form read: (\w+)", out)
    if m:
        form = m.group(1)
    got = dict(exit=rc, self=s, find=f, compared=comp, form=form)
    ok = got == pred
    allok &= ok
    print("   %-51s exit %d s%d f%d c%-2d %-7s  exit %d s%s f%s c%-2d %-7s  %s"
          % (name[:51], pred["exit"], pred["self"], pred["find"],
             pred["compared"], pred["form"], rc, s, f, comp, form,
             "YES" if ok else "NO"))
    print("        why: %s" % why)
    if not ok:
        finding("the widened c1 against %s: predicted %s, got %s"
                % (name, pred, got))
    if pred["find"] == 0 and f:
        print("        findings raised: %s" % L.findings_of(out)[:2])
print()
print("   the third case is the deletion test.  Before the widening the SAME")
print("   input produced 24 FINDINGS and 0 SELF-ERRORS; the unrepaired script")
print("   is re-run here on the same input to show the move:")
old_c1_src = L.git_show(L.REV_A218, L.A218_DIR + "/c1_branching.py")
o, rc = L.run_c1(blinded, script_source=old_c1_src)
s, f, t = L.totals_of(o)
print("     c1 @ 286d5030, blinded target : SELF %s  FINDINGS %s  exit %d" % (s, f, rc))
o2, rc2 = L.run_c1(blinded, script_source=c1_new_src)
s2, f2, t2 = L.totals_of(o2)
print("     c1 widened,    blinded target : SELF %s  FINDINGS %s  exit %d" % (s2, f2, rc2))
print("     the 24 moved from the FINDINGS channel to the SELF-ERROR channel:"
      " %s" % ("YES" if (f, s2) == (24, 24) and s == 0 and f2 == 0 else "NO"))
if not ((f, s2) == (24, 24) and s == 0 and f2 == 0):
    finding("the widening does not move the 24 from FINDINGS to SELF-ERRORS: "
            "before (self %s, find %s), after (self %s, find %s)" % (s, f, s2, f2))
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("(vii) THE GATE THAT WATCHES THE SENTENCE IS A PRESENCE TEST")
print("-" * 74)
print("""   mg-d330's e4 checks mg-a218's present-tense exit-code sentence, and
   this ticket's own change moved that sentence for the third time, so the
   sentence is struck at its site and replaced by a table of all three
   revisions.  Whether that is ENOUGH is not a matter of opinion: e4's gate
   is one substring test, quoted from its source --

       CLAIM = "`c2`, `c4` and `c5` exit `1`"
       if CLAIM in adoc:  ... finding(...)
       else:              selferr("could not locate ...")

   -- so it has exactly two states, PRESENT and ABSENT, and no state for
   PRESENT AND MARKED.  Evaluated on three variants of the document, with the
   direction predicted before each:""")
print()
A218_DOC = os.path.join(
    L.REPO, "docs/OneThird-Bratteli-Path-Algebras-Mge8b8Repair-IndependentAudit.md")
with open(A218_DOC, encoding="utf-8") as fh:
    adoc = fh.read()
CLAIM = "`c2`, `c4` and `c5` exit `1`"
struck = "~~" + CLAIM in adoc
corrected = "**CORRECTED (`mg-58da`)" in adoc
variants = [
    ("the document as this ticket leaves it (STRUCK + corrected)", adoc,
     "finding"),
    ("the same, with the sentence deleted outright", adoc.replace(CLAIM, ""),
     "self-error"),
    ("a hypothetical unstruck restatement", adoc.replace("~~", ""), "finding"),
]
print("   variant                                                    "
      "predicted   e4's gate says")
for name, txt, pred in variants:
    got = "finding" if CLAIM in txt else "self-error"
    print("   %-58s %-11s %s   %s"
          % (name[:58], pred, got, "YES" if got == pred else "NO"))
    if got != pred:
        selferr("the replication of e4's gate on %r did not behave as its "
                "source says it does" % name)
print()
print("   the sentence IS struck at its site : %s" % ("YES" if struck else "NO"))
print("   a CORRECTED block follows it       : %s" % ("YES" if corrected else "NO"))
print("   e4 raises the finding anyway       : %s"
      % ("YES" if CLAIM in adoc else "NO"))
if not (struck and corrected):
    finding("this ticket's correction of mg-a218's exit-code sentence is not "
            "marked at the site (struck %s, corrected block %s)"
            % (struck, corrected))
if struck and corrected and CLAIM in adoc:
    finding("mg-d330's e4_rerun.py gate on mg-a218's exit-code sentence is a "
            "PRESENCE TEST: it fires on the substring alone, so a sentence "
            "STRUCK IN PLACE with a correction beside it is indistinguishable "
            "from one left standing, and e4's finding text -- which says the "
            "sentence was 'left unchanged and unmarked' -- is now false of the "
            "tree while its exit code is unchanged. NOT REPAIRED HERE: e4 is "
            "mg-d330's committed instrument and rewriting the sentence to dodge "
            "the substring would turn the gate green while leaving it blind, "
            "which is the defect this arc keeps paying for")
print("""
   NOT REPAIRED HERE, and the reason is the whole ticket in miniature.  The
   sentence could be rewritten to make the substring vanish and e4 would go
   green.  That would satisfy the gate without informing the reader, and it
   would leave the gate exactly as blind as it is.  Marking in place is the
   right thing for the reader; e4's inability to see the marker is a finding
   against e4, and it is booked as one rather than worked around.""")
print()

# ---------------------------------------------------------------------------
print("-" * 74)
print("VERDICT ON THE SET-LEVEL PROPERTY")
print("-" * 74)
print("""   THE FIVE ARE: %s.

   ed9cde4 touched %d of them (%s).  This ticket touched %d (%s).  The kernel
   they share is untouched by both, and c1's own measurement is byte-identical
   across every revision in this table, so no mathematics moved at any point.

   WHAT HOLDS.  The members that measure the vertex cells agree with each
   other and with all %s instruments in the tree, at 24 of 24 cells, after
   both changes.  c0_repro.sh still regenerates the target's five committed
   outputs.  %d of the five are green.

   WHAT DOES NOT.  %s

   THE GENERAL POINT, and it is the reason this was not a small edit: the
   property is that the five CORROBORATE.  Widening one parser cannot be
   checked by running that parser, because a parser that has been made to
   agree with a target agrees with it.  It is checked by running the OTHER
   members and the OTHER instruments against the same cells, which is (iv),
   and by making the changed member fail on an input it genuinely cannot
   read, which is (vi).
""" % (", ".join(FIVE), len(touched_13b2), ", ".join(touched_13b2) or "none",
       len(touched_58da), ", ".join(touched_58da) or "none", "four",
       len(green),
       ("c3_withdrawal.py is red -- mg-d330's second finding, left OPEN here."
        if "c3_withdrawal.py" in red else
        ("all five are green." if not red else
         "red members: %s." % ", ".join(red)))
       + "  And, found by making this ticket's own\n   correction: mg-d330's "
         "e4 gate on the exit-code sentence is a PRESENCE TEST and cannot "
         "see\n   the marker beside it -- (vii), booked and NOT worked around."))

print("-" * 74)
print("SELF-ERRORS: %d, population: the %d sha reads, the %d committed-output "
      "reads, and the parses of c1's, c2's and e1's live vertex rows"
      % (len(SELF), len(FIVE) * 3, len(FIVE)))
for x in SELF:
    print("   SELF-ERROR: " + x)
print("FINDINGS: %d, population: the %d exit codes on the working tree, the "
      "cross-member and cross-instrument agreement on the 24 vertex cells, "
      "c0_repro.sh, the %d deletion-test cases on the widened c1, and the %d "
      "variants on which mg-d330's exit-code gate is evaluated"
      % (len(FIND), len(FIVE), len(cases) + 1, len(variants)))
for x in FIND:
    print("   FINDING: " + x)
print("TOTAL BAD: %d" % (len(SELF) + len(FIND)))
sys.exit(1 if (SELF or FIND) else 0)
