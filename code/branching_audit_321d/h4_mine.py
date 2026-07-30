"""h4_mine.py -- THE TWO THINGS I CHOSE, WHICH NO LIST IN THE TICKET NAMES.

Floor, not scope.  The ticket names the two questions, the set-level property
and the grain of the narrowing.  These two are neither, and both were picked
because they are the arc's own shape one level in.

  M1  g1's byte-for-byte confirmation of the committed record never reads the
      file in the tree.  Both sides of its comparison are historical objects.
      The document calls the record 'checkable rather than merely preserved';
      what is checkable is the git blob, not the bytes a reader opens.

  M2  the narrowing covers ABSENCE but not MISREAD.  The repair routes 'I
      cannot find the cell' to SELF-ERROR -- correctly, and at cell grain.  It
      does not route 'I found something that is not the cell' anywhere: the
      count regex still matches ANY line of seven integers whose first field
      is one digit, anywhere in T1b2, first match wins.  So the original
      defect's exact shape -- the instrument accusing the target where its own
      parser is at fault -- survives one branch over.

Both are deletion-tested: each claim is made to fire, and a null probe that
must stay green is run beside it so the battery is not just always-red.
Directions are predicted in PREDICTIONS.md before the run.

Exit 0 iff SELF-ERRORS == 0 and FINDINGS == 0.
"""

import os
import shutil
import subprocess
import sys
import tempfile

import lib321d as L

R = L.Report("h4", "the 3 probes on M1 (g1's record check) and the 4 probes "
                   "on M2 (the misread channel), each with its direction "
                   "predicted before the run")

L.banner("H4", "TWO THINGS I CHOSE: THE RECORD CHECK, AND THE MISREAD CHANNEL")

HEAD = L.head_rev()

# ---------------------------------------------------------------------------
L.rule("M1 (i) WHAT g1 ACTUALLY COMPARES, QUOTED FROM ITS SOURCE")
g1src = L.git_show(HEAD, L.S58DA_DIR + "/g1_provenance.py")
for line in g1src.splitlines():
    s_ = line.strip()
    if s_.startswith("committed = ") or s_.startswith("out_old, rc_old ="):
        print("       %s" % s_)
print("""
   Both sides are objects in git at %s: the committed blob, and a re-run of
   the code as it was AT THAT REVISION.  Neither side opens the file that
   sits in code/branching_audit_a218/ today.  g1's read_worktree() is used
   exactly once, for the TARGET, and never for the record.""" % L.REV_A218[:8])
uses_wt = "read_worktree(L.A218_DIR" in g1src
print()
print("   g1 reads the worktree copy of out_c1_branching.txt : %s" % uses_wt)

# the tree is not corrupt today, and that is worth stating before probing
disk = L.read_worktree(L.A218_DIR + "/out_c1_branching.txt")
blob = L.git_show(L.REV_A218, L.A218_DIR + "/out_c1_branching.txt")
print("   worktree copy vs the %s blob, right now            : %s"
      % (L.REV_A218[:8], "IDENTICAL" if disk == blob else "DIFFER"))
print("   so this is a BLINDNESS, not a wrong answer on today's tree.")

# ---------------------------------------------------------------------------
L.rule("M1 (ii) THE DELETION TEST -- CORRUPT THE RECORD A READER READS")


def scratch_repo():
    """A copy of the three directories g1 needs, plus the .git pointer, so the
    same script runs unmodified against a tree I can corrupt."""
    tmp = tempfile.mkdtemp(prefix="mg321d-m1-")
    os.makedirs(os.path.join(tmp, "code"))
    for d in (L.S58DA_DIR, L.A218_DIR, L.DB09_DIR):
        shutil.copytree(os.path.join(L.REPO, d), os.path.join(tmp, d))
    shutil.copy(os.path.join(L.REPO, ".git"), os.path.join(tmp, ".git"))
    return tmp


def run_g1(tree):
    p = subprocess.run(["python3", "g1_provenance.py"],
                       cwd=os.path.join(tree, L.S58DA_DIR),
                       capture_output=True, text=True)
    return p.stdout + p.stderr, p.returncode


probes = []


def probe(name, predicted, mutate=None):
    tree = scratch_repo()
    try:
        if mutate:
            mutate(tree)
        out, rc = run_g1(tree)
        byte_line = [l.strip() for l in out.splitlines()
                     if "BYTE-IDENTICAL" in l or "NOT byte-identical" in l]
        saw = "BYTE-IDENTICAL" if any("BYTE-IDENTICAL" in l
                                      for l in byte_line) else "fires"
        fires = saw == "fires"
        exp_fires = predicted == "fires"
        probes.append((name, predicted, saw, fires == exp_fires))
        print("     %-52s predicted %-14s actual %-14s %s"
              % (name, predicted, saw, "OK" if fires == exp_fires else "MISS"))
        return out, rc
    finally:
        shutil.rmtree(tree, ignore_errors=True)


def corrupt_record(tree):
    p = os.path.join(tree, L.A218_DIR, "out_c1_branching.txt")
    with open(p) as fh:
        txt = fh.read()
    assert txt.count("TOTAL BAD: 0") == 1
    with open(p, "w") as fh:
        fh.write(txt.replace("TOTAL BAD: 0", "TOTAL BAD: 99"))


def delete_record(tree):
    os.remove(os.path.join(tree, L.A218_DIR, "out_c1_branching.txt"))


print("   g1's record check, on three trees.  'fires' = it reports the record")
print("   as NOT byte-identical.  Direction predicted before each run.")
print()
probe("unmodified tree (NULL PROBE -- must not fire)", "BYTE-IDENTICAL")
probe("record's TOTAL BAD corrupted 0 -> 99 on disk", "BYTE-IDENTICAL",
      corrupt_record)
probe("record DELETED from the worktree entirely", "BYTE-IDENTICAL",
      delete_record)
print()
hits = sum(1 for _, _, _, ok in probes if ok)
print("   probes whose direction was predicted correctly : %d of %d"
      % (hits, len(probes)))
print("   probes that made g1's record check fire        : %d of %d"
      % (sum(1 for _, _, saw, _ in probes if saw == "fires"), len(probes)))
print("   population: the 3 trees above -- unmodified, corrupted, deleted.")
print()
fired = sum(1 for _, _, saw, _ in probes if saw == "fires")
if fired == 0:
    R.finding(
        "M1. g1_provenance.py's byte-for-byte confirmation of the committed "
        "record NEVER READS THE FILE IN THE TREE. Both sides of its "
        "comparison come from git at %s -- `committed = git_show(REV_A218, "
        "out_c1_branching.txt)` against a re-run of the code at that same "
        "revision -- so it certifies a blob against itself. Deletion-tested "
        "on three trees: corrupting the record's own TOTAL BAD line from 0 to "
        "99 on disk, and DELETING the file outright, both leave g1 printing "
        "'BYTE-IDENTICAL. The committed record is what the code does.' 0 of 3 "
        "probes fire; the null probe is among them, so the check is not "
        "merely insensitive, it is looking somewhere else. The document's "
        "section 3 says the record is 'checkable rather than merely "
        "preserved' -- what is checkable is git's copy, and preservation of "
        "the reader's copy is exactly what is not checked. This is the "
        "mg-a318 shape (the gate does not read the figure at the site) one "
        "instrument over" % L.REV_A218[:8])
else:
    print("   g1's record check does read the tree; M1 does not stand.")

# ---------------------------------------------------------------------------
L.rule("M2 (i) THE REGEX THE REPAIR LEFT UNANCHORED")
c1src = L.read_worktree(L.A218_DIR + "/c1_branching.py")
for line in c1src.splitlines():
    if "(?:\\d+\\s+){5}" in line:
        print("       %s" % line.strip())
print("""
   Seven integers, first field one digit, anchored to nothing but the line.
   The repair added a THIRD branch for a cell the target does not state -- at
   CELL grain, correctly -- but a cell the target states WRONGLY, or a line
   that is not the table at all, still lands in the FINDING channel.  The
   distinction the repair draws is present/absent; the distinction that
   matters is 'the target said this' / 'I decided this'.

   mg-58da's own lib58da.py says so, in the docstring of the reader it wrote
   to avoid the problem:""")
lib = L.git_show(HEAD, L.S58DA_DIR + "/lib58da.py")
for line in lib.splitlines():
    if "fooled by an unrelated row of digits" in line:
        print("       \"%s\"" % line.strip())
print("   -- noticed, avoided in the new reader, and not fixed in the old one")
print("   nor booked as a finding.")

# ---------------------------------------------------------------------------
L.rule("M2 (ii) THE DELETION TEST -- ABSENT vs MISREAD, SAME CELLS")
head_target = L.read_worktree(L.TARGET_REL)
repaired = L.read_worktree(L.A218_DIR + "/c1_branching.py")


def drop_beta2_sets(text):
    """Remove the six SET rows for beta = 2 from subsection (i) only."""
    seg = L.vertex_subsection(text)
    assert seg, "no vertex subsection"
    keep, cur, dropped = [], None, 0
    for raw in seg.splitlines(keepends=True):
        s_ = raw.strip()
        if s_.startswith("beta = ") and s_[7:].isdigit():
            cur = int(s_[7:])
        elif cur == 2 and s_.startswith("n=") and s_.endswith("]"):
            dropped += 1
            continue
        keep.append(raw)
    assert dropped == 6, "expected to drop 6 rows, dropped %d" % dropped
    return text.replace(seg, "".join(keep), 1)


STRAY = "     2      9      9      9      9      9      9\n"


def add_stray(text):
    """One line of seven integers inside T1b2, first field '2'.

    Not a vertex table.  It is the shape of a row that could be printed by any
    future rendering -- a per-parameter tally, a timing table, a checksum row.
    """
    marker = "  (i) THE VERTEX SET"
    assert text.count(marker) == 1
    return text.replace(marker, STRAY + marker, 1)


cases = [
    ("HEAD target, untouched (NULL PROBE)", head_target, (0, 0, 0)),
    ("beta=2 SET rows deleted -- ABSENT", drop_beta2_sets(head_target),
     (6, 0, 1)),
    ("the same, plus one stray 7-integer row -- MISREAD",
     add_stray(drop_beta2_sets(head_target)), (0, 6, 1)),
    ("stray row alone, SET rows intact -- SET wins",
     add_stray(head_target), (0, 0, 0)),
]
print("   the REPAIRED c1, run against four targets.  Predicted self/find/exit")
print("   is in PREDICTIONS.md and is printed beside the actual.")
print()
print("     target                                              predicted"
      "        actual")
misread = None
m2_hits = 0
for name, txt, pred in cases:
    out, rc = L.run_c1(txt, script_rev=L.REV_A218, script_text=repaired)
    s_, f_, _ = L.totals_of(out)
    got = (s_, f_, rc)
    ok = got == pred
    m2_hits += ok
    print("     %-50s %-15s %-15s %s"
          % (name, "%d/%d/%d" % pred, "%d/%d/%d" % got,
             "HIT" if ok else "MISS"))
    if name.startswith("the same, plus"):
        misread = (out, got)
print()
print("   directions predicted correctly : %d of %d" % (m2_hits, len(cases)))
print("   population: the four targets above -- untouched, absent, misread,")
print("   and stray-row-with-sets-intact.")
print()
if misread:
    out, got = misread
    print("   what the MISREAD run says, quoted from its own stdout:")
    for x in L.findings_of(out)[:3]:
        print("      FINDING: %s" % x)
    for line in out.splitlines():
        if line.strip().startswith("vertex cells:"):
            print("      %s" % line.strip()[:150])
    print()
    if got[1] > 0 and got[0] == 0:
        R.finding(
            "M2. The repair's narrowing is at the grain of the blindness for "
            "ABSENCE and at no grain at all for MISREAD. Same six cells, two "
            "targets one line apart: with the beta=2 SET rows deleted the "
            "REPAIRED c1 reports SELF-ERRORS 6 / FINDINGS 0 -- correct, and "
            "per cell. Add one stray line of seven integers anywhere in T1b2 "
            "whose first field is '2' -- not a vertex table, matched only "
            "because the count regex is anchored to nothing -- and the same "
            "six cells report SELF-ERRORS 0 / FINDINGS %d, accusing the "
            "target of stating vertex counts it never stated. That is the "
            "defect mg-d330 raised, in the branch the repair kept: the third "
            "branch distinguishes present from absent, where the distinction "
            "that matters is 'the target said this' from 'I decided this'. "
            "mg-58da's own lib58da.py docstring records that c1's parser 'can "
            "be fooled by an unrelated row of digits' and writes a "
            "subsection-anchored reader to avoid it; the old parser was not "
            "anchored with it and the residue is not booked in the document's "
            "NOT CLAIMED section" % got[1])

sys.exit(R.emit())
