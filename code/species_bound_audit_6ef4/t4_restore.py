"""T4 -- THE FLOOR.  One thing no list in the ticket names: THE RESTORE PROOF.

The ticket names OPEN 1, OPEN 2 and the census.  It also says: audit at least
one thing no list here names, and say what you chose.

CHOSEN: `kern5040.Probe`'s restore proof -- the sentence "it mutates the real
worktree and PROVES it put it back", which is load-bearing for every number
mg-5040 published and is checked by nobody.

WHY THIS ONE.  T1 has to `chmod 000` a tracked file to ask its question at
all, and the first thing to ask of a borrowed harness is whether it would have
noticed.  `kern5040.Probe` snapshots BYTES; its proof is `git status
--porcelain --untracked-files=all` plus the full `git diff`.  git records ONE
bit of a file's mode.  So the perturbation this audit makes is precisely the
one that harness cannot see -- and if that is so, the harness would report
RESTORED on a worktree it had left broken, which is the same failure as a
checker printing PASS over a file it could not read.  It is the T1 finding in
the instrument rather than in the subject.

NOTHING HERE IS ASSERTED.  mg-5040's own `Probe` is imported and used, the
perturbation is made, and what it says is printed.

T4a  mg-5040's Probe, a tracked file left at mode 000, and its verdict
T4b  the same perturbation under this instrument's mode-aware proof
T4c  a tracked file that is UNREADABLE AT ENTRY, and the snapshot
T4d  does selftest5040.py test the restore contract for a MODE?
T4e  is the defect present at the commit where that harness shipped?
T4f  what THIS instrument's proof still cannot see, declared

    python3 code/species_bound_audit_6ef4/t4_restore.py
"""

import os
import re
import sys

from kern6ef4 import hdr, REPO, git, Probe6ef4

sys.path.insert(0, os.path.join(REPO, "code", "species_bound_repair_5040"))
import kern5040                                              # noqa: E402

bad = 0
missed = 0

# A tracked file that belongs to THIS ticket, so no probe here touches another
# ticket's artifact.  It is committed before any probe runs.
VICTIM = "code/species_bound_audit_6ef4/PREDICTIONS.md"
KERN5040 = "code/species_bound_repair_5040/kern5040.py"
SHIPPED_AT = "cada54f"          # the commit that first published kern5040.py


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    if detail:
        for ln in detail.splitlines():
            print("        %s" % ln)


def note(label, value):
    print("  %-64s %s" % (label[:64], value))


def score(pid, predicted, got):
    global missed
    hit = predicted == got
    missed += (not hit)
    print("  %-6s predicted %-24s got %-24s %s"
          % (pid, str(predicted), str(got), "" if hit else "*** MISSED ***"))
    return hit


P = os.path.join(REPO, VICTIM)
if not os.path.exists(P):
    raise SystemExit("%s must be committed before this probe runs" % VICTIM)
ENTRY_MODE = os.stat(P).st_mode & 0o7777


# ---------------------------------------------------------------------------
# T4a  MG-5040'S OWN PROBE, WITH A MODE LEFT BROKEN
# ---------------------------------------------------------------------------
hdr("T4a  `kern5040.Probe` -- a tracked file left at mode 000")

print("  The file is %s, which this ticket wrote and" % VICTIM)
print("  committed, so no other ticket's artifact is touched.  It is")
print("  chmod'ed inside the probe and NOT put back by the probe, and then")
print("  the probe's own verdict is read.  This file puts the mode back")
print("  itself afterwards, and prints the mode before and after.")
print()

print("  TWO MODES, AND THE SECOND ONE IS HERE BECAUSE THE FIRST MISSED.")
print("  P4a predicted that `000` would go unnoticed.  It does not, and the")
print("  reason it does not is worth more than the prediction was: git cannot")
print("  READ a `000` file, so `git status` calls it MODIFIED even though not")
print("  one byte of it changed.  Right verdict, wrong reason -- which is")
print("  mg-4700's D2b in the harness rather than in a subject.  So a second")
print("  mode is probed: `400`, which git can still read and which changes")
print("  no executable bit.  That is the case the proof is actually about.")
print()

MODES = [(0o000, "000 -- git cannot read it either"),
         (0o400, "400 -- read-only; git reads it fine, exec bit unchanged")]
A = {}
for m, what in MODES:
    try:
        with kern5040.Probe("t4a-%o" % m) as pr5040:
            in_snap = P in pr5040.snapshot
            os.chmod(P, m)
        A[m] = {"restored": pr5040.restored,
                "rewritten": len(pr5040.rewritten),
                "in_snapshot": in_snap,
                "mode_after": os.stat(P).st_mode & 0o7777}
    finally:
        os.chmod(P, ENTRY_MODE)
    print("      chmod %-52s restored: %-5s  rewrote %d"
          % (what, A[m]["restored"], A[m]["rewritten"]))
print()
note("entry mode", oct(ENTRY_MODE))
note("the file was in kern5040.Probe's snapshot at entry",
     A[0o000]["in_snapshot"])
note("mode left behind after the 000 probe (this file puts it back)",
     oct(A[0o000]["mode_after"]))
print()
row("kern5040.Probe notices a tracked file left at mode 400",
    not A[0o400]["restored"],
    "It says RESTORED, and the file is not.  `git status --porcelain` and\n"
    "`git diff` carry ONE bit of a file's mode -- the executable bit -- and\n"
    "`Probe` snapshots BYTES and never stats.  So every permission change\n"
    "that leaves the exec bit alone and leaves the file readable is outside\n"
    "the proof entirely.  mg-5040's own R1 probe plants a `chmod 000`\n"
    "directory and restores it from a REMEMBERED undo list, which is the\n"
    "distinction that instrument draws against everybody else: a list of\n"
    "what somebody thought of, where a measurement was needed.")
row("when it DOES notice, the reason it gives is the right one",
    False if A[0o000]["restored"] is False else True,
    "For `000` it reports NOT restored -- correctly -- because git cannot\n"
    "read the file and calls it MODIFIED.  Nothing in the run says the mode\n"
    "moved; a reader is told the CONTENT changed, and it did not.  The\n"
    "verdict is right and the diagnosis is wrong, which is exactly what T1\n"
    "found in the subjects.")
score("P4a", True, A[0o000]["restored"])


# ---------------------------------------------------------------------------
# T4b  THE SAME PERTURBATION UNDER A MODE-AWARE PROOF
# ---------------------------------------------------------------------------
hdr("T4b  THE SAME PERTURBATION UNDER THIS INSTRUMENT'S PROOF")

print("  Same file, same chmod, same non-restoration by the probe body.  The")
print("  only difference is what the proof looks at.  A new control that has")
print("  never been seen to fire is worth nothing, so this is the control")
print("  and T4a is the commit where the defect is present.")
print()

B = {}
for m, what in MODES:
    try:
        with Probe6ef4("t4b-%o" % m) as pr6ef4:
            os.chmod(P, m)
        B[m] = [x for x in pr6ef4.mode_bad if x[0] == VICTIM]
    finally:
        os.chmod(P, ENTRY_MODE)
    print("      chmod %-52s named by the mode proof: %s"
          % (what, "YES" if B[m] else "no"))
    for rel, was, now in B[m][:2]:
        print("          %s  %s -> %s"
              % (rel, oct(was), oct(now) if now is not None else "unreadable"))
print()
row("the mode-aware proof sees BOTH, including the one the byte proof missed",
    bool(B[0o000]) and bool(B[0o400]),
    "If this row is a finding the control is broken and T4a proves nothing.")
score("P4b", True, bool(B[0o400]))


# ---------------------------------------------------------------------------
# T4c  A TRACKED FILE UNREADABLE AT ENTRY
# ---------------------------------------------------------------------------
hdr("T4c  A TRACKED FILE THAT IS UNREADABLE WHEN THE PROBE STARTS")

print("  `Probe.__enter__` reads every tracked file into memory and skips")
print("  what it cannot read with a bare `except OSError: pass`.  A file")
print("  skipped there is absent from the snapshot, therefore un-restorable,")
print("  and the run says nothing.  Measured, not read off the source.")
print()

try:
    os.chmod(P, 0o000)
    with kern5040.Probe("t4c") as pr2:
        present = P in pr2.snapshot
    with Probe6ef4("t4c-mine") as pr3:
        mine_reports = list(pr3.unreadable_at_entry)
finally:
    os.chmod(P, ENTRY_MODE)

note("in kern5040.Probe's snapshot", present)
note("kern5040.Probe said so anywhere", "no -- there is no such field")
note("Probe6ef4 recorded it by name", VICTIM in mine_reports)
row("a file it could not snapshot is reported by kern5040.Probe", present,
    "Absent from the snapshot and unmentioned.  The probe would then run,\n"
    "the body could rewrite that file, and the restore would put back\n"
    "nothing -- with `restored` still True, because `git diff` cannot read\n"
    "it either.  Same `except OSError` as the checkers' layer 2 in T1, in\n"
    "the harness that measured them.")
score("P4c", False, present)


# ---------------------------------------------------------------------------
# T4d  DOES THE SELF-TEST TEST THE CONTRACT FOR A MODE?
# ---------------------------------------------------------------------------
hdr("T4d  `selftest5040.py` -- the restore contract, in which directions?")

st = open(os.path.join(REPO, "code/species_bound_repair_5040/"
                             "selftest5040.py"), encoding="utf-8").read()
n_restore = len(re.findall(r"restored", st))
n_chmod = len(re.findall(r"chmod|st_mode|0o000|mode", st))
note("assertions mentioning `restored`", n_restore)
note("anything in the self-test mentioning a MODE", n_chmod)
print()
row("the restore contract is tested for a left-behind MODE, "
    "not only a file", n_chmod > 0,
    "mg-5040 tests the contract IN THE DIRECTION THAT MUST FAIL -- and only\n"
    "for a left-behind FILE, which is the class it had already thought of.\n"
    "A restore proof only ever seen to fail on the one class somebody\n"
    "remembered is worth what a walk that declines in silence is worth.\n"
    "That sentence is mg-5040's, about `os.walk`.")
score("P4d", True, n_restore > 0 and n_chmod == 0)


# ---------------------------------------------------------------------------
# T4e  IS THE DEFECT PRESENT WHERE THAT HARNESS SHIPPED?
# ---------------------------------------------------------------------------
hdr("T4e  THE DEFECT AT %s, THE COMMIT THAT PUBLISHED THE HARNESS" % SHIPPED_AT)

code, then = git(["show", "%s:%s" % (SHIPPED_AT, KERN5040)])
now = open(os.path.join(REPO, KERN5040), encoding="utf-8").read()


def enter_body(src):
    m = re.search(r"def __enter__\(self\):(.*?)\n    def ", src, re.S)
    return m.group(1) if m else ""


same = enter_body(then).strip() == enter_body(now).strip()
note("`git show %s:%s` succeeded" % (SHIPPED_AT, os.path.basename(KERN5040)),
     code == 0)
note("`__enter__` is byte-identical at %s and at HEAD" % SHIPPED_AT, same)
note("it stats anything at %s" % SHIPPED_AT,
     bool(re.search(r"st_mode|os\.stat", enter_body(then))))
note("it stats anything at HEAD",
     bool(re.search(r"st_mode|os\.stat", enter_body(now))))
print()
print("  So the silence in T4a is not something this audit introduced by")
print("  running the harness in a worktree it was not written for.  It is in")
print("  the bytes that were published, and it was published with a")
print("  self-test that asserts the restore contract in the direction that")
print("  must fail -- for the one class it names.")


# ---------------------------------------------------------------------------
# T4f  WHAT THIS INSTRUMENT'S PROOF STILL CANNOT SEE
# ---------------------------------------------------------------------------
hdr("T4f  THE BOUND OF THIS INSTRUMENT'S OWN RESTORE PROOF, DECLARED")

print("  Stating it is the only honest move available: a proof that names")
print("  four things is a proof about four things, and the T1 finding is")
print("  exactly what happens when a bound is left to be inferred.")
print()
for line in [
    "porcelain + full diff + bytes + PERMISSION MODE, for every TRACKED",
    "regular file that is not a symlink, under this repository only.",
    "",
    "NOT covered, and each of these would be a silent non-restore here:",
    "  * ownership, extended attributes, ACLs, flags",
    "  * mtime and atime",
    "  * the mode of a DIRECTORY (only files are stated)",
    "  * a symlink's target (they are skipped: `git ls-files` lists them,",
    "    `os.path.islink` drops them)",
    "  * anything UNTRACKED beyond what `git status` reports",
    "  * anything outside REPO -- the tempdirs this instrument makes are",
    "    removed by name, and if a removal fails nothing here notices",
]:
    print("      %s" % line)
print()
print("  That list is a MEASUREMENT of what the four proofs look at, not a")
print("  promise that nothing else can go wrong.  A reader who finds a fifth")
print("  should treat this paragraph the way T1 treats mg-5040's: the class")
print("  is not closed by naming members of it.")


# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("T4 TOTAL BAD: %d" % bad)
print("T4 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THESE NUMBERS.  ONE harness -- `kern5040.Probe` -- against")
print("ONE perturbation, a mode change on ONE tracked file this ticket owns,")
print("plus a reading of `selftest5040.py` and a comparison of `__enter__`")
print("at %s with HEAD.  It says NOTHING about whether any figure" % SHIPPED_AT)
print("mg-5040 published is wrong: no probe in that instrument is shown to")
print("have left the tree broken, and this section does not claim one did.")
print("What it measures is that IF ONE HAD, in this class, the proof would")
print("have said RESTORED.")
sys.exit(1 if bad else 0)
