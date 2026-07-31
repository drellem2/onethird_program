"""T1 -- OPEN 1.  Did mg-5040 SUBTRACT, or widen a third time?

IT SUBTRACTED, and it subtracted in the right place.  The walk returns its own
residue; a declined entry that is not the one stated `__pycache__` rule is
counted into that checker's TOTAL BAD; `followlinks=True` was NOT added and
the word "total" was NOT used.  This section does not dispute any of that.

THE QUESTION IT ASKS IS THE ONE THE REPAIR INVITES.  mg-5040's own sentence is
that the SILENCE -- not the depth rule, not the symlink rule -- is what
generated the generations, and that the silence is removed.  So: CONSTRUCT THE
NEXT WORLD-CHANGE and see whether the claim VISIBLY STOPS MATCHING or quietly
becomes false.

The set these checkers quantify over is built in TWO layers:

    layer 1   os.walk           -- which entries are REACHED
    layer 2   open(...).read()  -- which reached entries are actually READ

`walk_residue` names everything declined at layer 1.  Layer 2 declines too:
`except (UnicodeDecodeError, OSError)` puts the entry on an UNDECODABLE list
which is PRINTED -- and is not counted into `bad`, and is printed under a
sentence saying the reason was the file's ENCODING.

So the world-change constructed here is A REGULAR FILE THIS PROCESS CANNOT
OPEN.  It is a regular file, so layer 1 reaches it and the residue is empty.
It raises `PermissionError`, so layer 2 drops it.  `PermissionError` is an
`OSError`, so it is filed as "not UTF-8 text" -- which is false: the file is
valid UTF-8 and the reason is its mode.

T1a  the stated bound against the code, measured on the shipped functions
T1b  three plants, four checkers, at HEAD, against a no-plant baseline
T1c  the same plant at the PINNED pre-repair revision -- context, not scored
T1d  are the two layer-2 buckets distinguishable to a reader?

    python3 code/species_bound_audit_6ef4/t1_bound.py
"""

import os
import re
import shutil
import sys
import tempfile

from kern6ef4 import (hdr, CHECKERS, PLANT_TREE, PRE, REPO, RUNNERS,
                      Probe6ef4, extract, lift, prove, run_checker, sh)

bad = 0
missed = 0

# ASSEMBLED, NOT WRITTEN OUT.  `w3_scope.py`'s X4 row forbids this sentence at
# source and this file is a committed file in this repository.  It is not in
# that checker's extent today -- and "not in its extent today" is the exact
# species of assumption this whole arc is about, so the literal never appears
# here.
FORBIDDEN_SENTENCE = "T3d says %s." % " ".join(["three", "are", "controls"])
PLANTED_TEXT = ("# planted by mg-6ef4's T1 probe and removed by the same "
                "probe\nNOTE = \"%s\"\n" % FORBIDDEN_SENTENCE)
PLANT_NAME = "leak6ef4.py"

# The one thing `w3_scope.py` prints when it has caught a live X4 statement.
CAUGHT = "STILL ASSERTED"


def row(label, ok, detail=""):
    """`ok` means: mg-5040's claim HOLDS for this row."""
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
    print("  %-6s predicted %-22s got %-22s %s"
          % (pid, str(predicted), str(got), "" if hit else "*** MISSED ***"))
    return hit


def residue_lines(out):
    return [ln for ln in out.splitlines() if "declined, NOT STATED" in ln]


def false_rows(out):
    return [ln.strip() for ln in out.splitlines() if "*** " in ln]


def caught_here(out):
    """Did the run report the PLANTED file as carrying a live statement?

    On the SAME LINE, and the same-line rule is not fussiness.  The first
    version of this predicate asked whether `STILL ASSERTED` and the filename
    both appeared ANYWHERE in the run, and `s1_extent.py` prints a LEGEND line
    reading `!! = STILL ASSERTED` in every run it ever makes -- so the
    predicate reported a catch for three plants including one the checker
    crashed on before reaching its own verdict.  Kept in OUTCOMES.md.
    """
    return any(CAUGHT in ln and PLANT_NAME in ln for ln in out.splitlines())


def printed_verdict(out):
    """Did the checker print its own `TOTAL BAD` line at all?

    A checker that exits 1 without printing its verdict has not made a
    finding; it has died.  Those two are the same exit code and they are not
    the same event, which is the whole of mg-4700's D2b.
    """
    return bool(re.search(r"^[A-Z0-9]+ TOTAL BAD:|^W3 SCOPE:", out, re.M))


# ---------------------------------------------------------------------------
# T1a  THE STATED BOUND, AGAINST THE CODE THAT SHIPS
# ---------------------------------------------------------------------------
hdr("T1a  THE STATED BOUND AGAINST THE CODE -- on the shipped functions")

print("  `walk_residue` is lifted out of each file BY PARSING IT, so what is")
print("  tested is the code that SHIPS and not a copy of it, and lifting it")
print("  does not execute the checker (mg-5040's kept defect 5).  The")
print("  module-level constants come across too, so `stated_dirs=")
print("  STATED_DIR_RULES` is the SUBJECT's directory rule and not this")
print("  file's idea of it.")
print()

WALKS = [
    ("code/species_repair_a4ef/s1_extent.py", "walk_residue"),
    ("code/species_remainder_f8fa/w3_scope.py", "walk_residue"),
    ("code/species_extent_d633/e1_extents.py", "walk_residue"),
]

scratch = tempfile.mkdtemp(prefix="mg6ef4-t1a-")
notdir = os.path.join(scratch, "a-regular-file")
with open(notdir, "w", encoding="utf-8") as f:
    f.write("this path is a file, not a directory\n")

# (i) the printed bound says the walk RETURNS EVERYTHING IT DECLINED.  Its own
#     first statement is an early return with EMPTY residue.
empties = []
for rel, fn in WALKS:
    files, stated, unstated = lift(rel, fn)(notdir)
    if (files, stated, unstated) == ([], [], []):
        empties.append(os.path.basename(rel))
    print("      %-22s walk_residue(<not a directory>) -> %r"
          % (os.path.basename(rel), (files, stated, unstated)))
print()
row("a root that is not a directory lands in the residue (%d of %d copies)"
    % (len(WALKS) - len(empties), len(WALKS)), not empties,
    "`if not os.path.isdir(root): return files, stated, unstated` is the\n"
    "FIRST STATEMENT of the function whose whole contract is that nothing is\n"
    "dropped without landing in one of the last two.  A whole root is.\n"
    "Copies affected: %s" % ", ".join(empties))
score("P1k", "([], [], [])",
      str(tuple(lift(WALKS[0][0], WALKS[0][1])(notdir))))
print()

# (ii) the printed bound says the walk reads no entry that is not a regular
#      file.  `os.path.isfile` FOLLOWS symlinks.
d2 = os.path.join(scratch, "tree")
os.makedirs(d2)
outside = tempfile.mkdtemp(prefix="mg6ef4-t1a-target-")
tgt = os.path.join(outside, "real.txt")
with open(tgt, "w", encoding="utf-8") as f:
    f.write("a regular file, outside the tree\n")
os.symlink(tgt, os.path.join(d2, "slink.txt"))
files, stated, unstated = lift(WALKS[0][0], WALKS[0][1])(d2)
row("the walk 'reads no entry that is not a regular file', as printed",
    "slink.txt" not in files,
    "files=%r residue=%r\nThe entry is a SYMLINK.  `os.path.isfile` follows "
    "it, so it is read, and it\nis not in the residue either -- the printed "
    "sentence is false in the\ndirection nobody checks." % (files, unstated))
shutil.rmtree(scratch, ignore_errors=True)
shutil.rmtree(outside, ignore_errors=True)
print()
print("  Both mismatches are between the SENTENCE and the CODE, which is the")
print("  one thing option 1 exists to make impossible.  Neither is reachable")
print("  by planting anything in a tree: they are properties of the")
print("  enumerator, and they are the two places the enumerator stops being a")
print("  measurement and goes back to being a rule somebody wrote down.")


# ---------------------------------------------------------------------------
# T1b  THREE PLANTS, FOUR CHECKERS, AT HEAD
# ---------------------------------------------------------------------------
hdr("T1b  THE NEXT WORLD-CHANGE, PLANTED IN THE REAL WORKTREE")

print("  Each plant is its own probe, planted ALONE, so an exit code is")
print("  attributable to one structure.  The restore proof is printed after")
print("  every one of them, and it is MODE-AWARE -- which mg-5040's is not,")
print("  measured rather than asserted in t4_restore.py.")
print()
print("  FOUR COLUMNS AND THEY ARE NOT THE SAME QUESTION.  `names` is whether")
print("  the run prints the planted FILENAME anywhere.  `CAUGHT` is whether a")
print("  SINGLE LINE carries `%s` and that filename -- the one thing" % CAUGHT)
print("  a checker prints when it has found a live X4 statement.  `verdict`")
print("  is whether the checker printed its own `TOTAL BAD` line AT ALL: a")
print("  checker that exits 1 without one has not made a finding, it has")
print("  died, and those are the same exit code.  `residue` is the count of")
print("  `declined, NOT STATED` lines, which is the mechanism under audit.")
print()


def measure(root=None):
    out = {}
    for label, d, script in CHECKERS:
        code, text = run_checker(d, script, root=root)
        out[label] = {"exit": code,
                      "names": PLANT_NAME in text,
                      "caught": caught_here(text),
                      "verdict": printed_verdict(text),
                      "residue": len(residue_lines(text)),
                      "false": false_rows(text),
                      "text": text}
    return out


def show(tag, m):
    print("  --- %s" % tag)
    for label, _d, _s in CHECKERS:
        v = m[label]
        print("      %-22s exit %d  names %-3s CAUGHT %-3s verdict %-3s "
              "residue %d"
              % (label, v["exit"], "yes" if v["names"] else "no",
                 "YES" if v["caught"] else "no",
                 "yes" if v["verdict"] else "NO", v["residue"]))


print("  BASELINE -- nothing planted.  Without it a green run proves nothing")
print("  about the plants, and a red one is not attributable.")
BASE = measure()
show("BASELINE", BASE)
print()

PLANTS = [
    ("UNREADABLE",
     "a REGULAR FILE THIS PROCESS CANNOT OPEN, valid UTF-8, live statement",
     PLANTED_TEXT, 0o000, None),
    ("READABLE",
     "the SAME statement in a READABLE file -- the attribution control",
     PLANTED_TEXT, 0o644, None),
    ("UNDECODABLE",
     "a READABLE file whose BYTES are not valid UTF-8 -- the bucket control",
     None, 0o644, b"\xff\xfe\x00\x01" + PLANTED_TEXT.encode("utf-8")),
]

RESULTS = {}
for tag, what, text, mode, raw in PLANTS:
    rel = os.path.join(PLANT_TREE, PLANT_NAME)
    with Probe6ef4(tag) as pr:
        pr.write(rel, raw if raw is not None else text, mode=mode)
        RESULTS[tag] = measure()
    show("%s: %s" % (tag, what), RESULTS[tag])
    prove(pr)
    print()

u = RESULTS["UNREADABLE"]
r = RESULTS["READABLE"]
b = RESULTS["UNDECODABLE"]

print("  THE ROWS")
row("w3_scope.py CATCHES the statement in an unreadable regular file",
    u["w3_scope.py"]["caught"],
    "exit %d, and `%s` does not appear.  The tree this checker is the\n"
    "WHOLE extent of now holds a live X4 statement and the run is silent\n"
    "about it -- while printing the filename under a sentence that gives\n"
    "the wrong reason.  Baseline exit was %d, so the exit code did not move."
    % (u["w3_scope.py"]["exit"], CAUGHT, BASE["w3_scope.py"]["exit"]))
row("the unreadable file appears in SOME checker's residue",
    any(v["residue"] for v in u.values()),
    "0 residue entries in 4 of 4 checkers.  The mechanism mg-5040 installed\n"
    "for exactly this class does not fire, because the decline happens at\n"
    "layer 2 and the residue is computed at layer 1.")
row("the attribution control fires (else the silence above means nothing)",
    r["w3_scope.py"]["caught"] and r["w3_scope.py"]["exit"] == 1,
    "readable plant: exit %d, CAUGHT %s"
    % (r["w3_scope.py"]["exit"], r["w3_scope.py"]["caught"]))
row("s1_extent.py, when loud, is loud ABOUT THE PLANTED STATEMENT",
    u["s1_extent.py"]["exit"] == 0 or u["s1_extent.py"]["caught"],
    "exit %d, CAUGHT %s, printed its own verdict line: %s.\n"
    "It does not reach `S1 TOTAL BAD` at all: `shutil.copytree` in its own\n"
    "injection control raises `Permission denied` on the planted file, so the\n"
    "diagnosis a reader is handed is that the CONTROL broke.  Nothing in the\n"
    "run says a forbidden statement is live in code/species_7d75.  That is\n"
    "mg-4700's D2b and mg-5040's P1e for a THIRD structure, and neither of\n"
    "them planted this one."
    % (u["s1_extent.py"]["exit"], u["s1_extent.py"]["caught"],
       "yes" if u["s1_extent.py"]["verdict"] else "NO"))

# E1's certifying row, by name, for each plant.
print()
print("  E1's EXTENT ROW, PER PLANT -- the row whose whole job is deciding")
print("  whether a printed extent is TRUE:")


def cert_row(m):
    for ln in m["e1_extents.py"]["text"].splitlines():
        if "reads every non-excluded regular file" in ln:
            return ln.rstrip()
    return "(row not printed)"


for tag in ("UNREADABLE", "READABLE", "UNDECODABLE"):
    print("      %-12s %s" % (tag, cert_row(RESULTS[tag]).strip()))
certified = "ok" in cert_row(u)
print()
row("e1_extents.py does not certify the extent over a file never read",
    not certified,
    "`trace_open.py` records the path BEFORE calling the real `open`, so an\n"
    "attempt that RAISES is recorded as a read and `want <= got` holds.  E1\n"
    "walks independently of the subject -- mg-5040's answer to 'an instrument\n"
    "that computes its expectation the subject's way cannot disagree' -- and\n"
    "the two still agree here, through the TRACER instead of through the walk.")
note("e1_extents.py rows that DID fail on the unreadable plant",
     len(u["e1_extents.py"]["false"]))
for ln in u["e1_extents.py"]["false"][:4]:
    print("        %s" % ln)

print()
print("  PREDICTIONS")
score("P1a", 0, u["w3_scope.py"]["exit"])
score("P1b", 1, r["w3_scope.py"]["exit"])
score("P1c", 0, b["w3_scope.py"]["exit"])
score("P1e", 0, sum(v["residue"] for v in u.values()))
score("P1f", (1, False), (u["s1_extent.py"]["exit"], u["s1_extent.py"]["caught"]))
score("P1g", True, certified)
score("P1h", 1, u["e1_extents.py"]["exit"])


# ---------------------------------------------------------------------------
# T1bb  WHAT A RUN OF THE ARC SAYS -- the three runners, on disk
# ---------------------------------------------------------------------------
hdr("T1bb  THE THREE RUNNERS, WITH THE UNREADABLE PLANT ON DISK")

print("  A checker's exit code is not what a reader meets.  `run_all.sh` is.")
print("  So the same plant is left in place and each of the three runners is")
print("  EXECUTED, unmodified, and its own exit code read.")
print()

RUNNER_OUT = {}
with Probe6ef4("runners") as pr:
    pr.write(os.path.join(PLANT_TREE, PLANT_NAME), PLANTED_TEXT, mode=0o000)
    for rn in RUNNERS:
        code, text = sh(["sh", "run_all.sh"],
                        cwd=os.path.join(REPO, "code", rn))
        RUNNER_OUT[rn] = (code, caught_here(text))
        print("      %-26s exit %d   CAUGHT %s"
              % (rn, code, "YES" if RUNNER_OUT[rn][1] else "no"))
prove(pr)
print()
green = [r for r in RUNNERS if RUNNER_OUT[r][0] == 0]
row("no runner is GREEN with a live X4 statement in code/species_7d75",
    not green,
    "green: %s\n`code/species_remainder_f8fa/run_all.sh` is the runner that\n"
    "executes `w3_scope.py`, whose ENTIRE extent is code/species_7d75.  It\n"
    "exits 0.  The one runner that goes red does so through a `copytree`\n"
    "crash in a different tree's checker." % ", ".join(green))
row("the runner that DOES go red names the statement",
    all(RUNNER_OUT[r][1] for r in RUNNERS if RUNNER_OUT[r][0] != 0),
    "0 of %d red runners print `%s` against the planted file."
    % (len([r for r in RUNNERS if RUNNER_OUT[r][0] != 0]), CAUGHT))


# ---------------------------------------------------------------------------
# T1c  THE SAME PLANT AT THE PINNED PRE-REPAIR REVISION -- NOT SCORED
# ---------------------------------------------------------------------------
hdr("T1c  THE SAME PLANT AT %s -- context, and NOT scored" % PRE)

print("  Not scored, and the reason is the whole point of the section: this")
print("  is a generation the subtraction DID NOT REACH, not a regression it")
print("  introduced.  Counting it into TOTAL BAD would say mg-5040 broke")
print("  something, and it did not.")
print()
print("  The extraction has NO `.git`.  A checker that asks git for an anchor")
print("  gets no answer there and says so in its own output; no number taken")
print("  from this extraction depends on one.")
print()

tmp = tempfile.mkdtemp(prefix="mg6ef4-pin-")
try:
    extract(PRE, tmp)
    p = os.path.join(tmp, PLANT_TREE, PLANT_NAME)
    with open(p, "w", encoding="utf-8") as f:
        f.write(PLANTED_TEXT)
    os.chmod(p, 0o000)
    PINNED = measure(root=tmp)
    show("AT %s, UNREADABLE PLANT" % PRE, PINNED)
    os.chmod(p, 0o644)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
note("w3_scope.py at the pin: exit / CAUGHT",
     "%d / %s" % (PINNED["w3_scope.py"]["exit"],
                  PINNED["w3_scope.py"]["caught"]))
note("w3_scope.py at HEAD:    exit / CAUGHT",
     "%d / %s" % (u["w3_scope.py"]["exit"], u["w3_scope.py"]["caught"]))
note("the repair moved this checker's answer for this structure",
     "NO" if PINNED["w3_scope.py"]["exit"] == u["w3_scope.py"]["exit"]
     else "yes")
score("P1i", 0, PINNED["w3_scope.py"]["exit"])


# ---------------------------------------------------------------------------
# T1d  ARE THE TWO LAYER-2 BUCKETS DISTINGUISHABLE?
# ---------------------------------------------------------------------------
hdr("T1d  ONE BUCKET, TWO WORLDS -- the printed sentence, side by side")


def bucket(out):
    """`w3_scope.py` prints its layer-2 bucket across TWO lines; both."""
    lines = out.splitlines()
    for i, ln in enumerate(lines):
        if "skipped as not" in ln:
            return " ".join(x.lstrip("# ").rstrip()
                            for x in lines[i:i + 2])
    return "(no bucket line printed)"


ub, bb, rb = bucket(u["w3_scope.py"]["text"]), \
    bucket(b["w3_scope.py"]["text"]), bucket(r["w3_scope.py"]["text"])
print("  UNREADABLE  (valid UTF-8, mode 000, live forbidden statement):")
print("      %s" % ub)
print("  UNDECODABLE (readable, invalid UTF-8 bytes):")
print("      %s" % bb)
print("  READABLE    (the control -- what the same line says when nothing")
print("               was dropped):")
print("      %s" % rb)
print()
same = re.sub(r"\d+", "N", ub) == re.sub(r"\d+", "N", bb)
row("the two are distinguishable in what the run PRINTS", not same,
    "Identical up to the file counts.  The sentence a reader is handed says\n"
    "the reason was the file's ENCODING.  For the first it is the file's\n"
    "MODE, the file is valid UTF-8, and the statement inside it is live.")
print()
print("  'A checker silent because nothing is wrong and a checker silent")
print("  because it cannot see are the same bytes on stdout.'  That sentence")
print("  is mg-5040's own, from the header of kern5040.py.  It is true of")
print("  layer 2 of its own four subjects.")
score("P1d", True, same)


# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("T1 TOTAL BAD: %d" % bad)
print("T1 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THESE NUMBERS.  FOUR checkers -- the four in")
print("kern6ef4.CHECKERS, which is kern5040.CHECKERS unchanged -- against a")
print("no-plant BASELINE and THREE plants in ONE tree, code/species_7d75, at")
print("HEAD, plus one of the three at %s, which is not scored.  It" % PRE)
print("says NOTHING about any other walk in this repository, nothing about")
print("the mathematics, and nothing about whether e2_crosssection.py is the")
print("right check.  `T1 TOTAL BAD` counts rows that contradict MG-5040'S OWN")
print("CLAIMS; `T1 PREDICTIONS MISSED` counts predictions in PREDICTIONS.md")
print("that were wrong.  The two are separate on purpose: a wrong prediction")
print("about code this ticket did not write is information, not a defect.")
sys.exit(1 if bad else 0)
