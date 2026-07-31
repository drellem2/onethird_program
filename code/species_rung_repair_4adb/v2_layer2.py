"""V2 -- OPEN 2.  AN UNREADABLE REGULAR FILE IS NOT A MIS-ENCODED ONE.

mg-6ef4's F1: the set these checkers quantify over is built in TWO layers.

    layer 1   os.walk           -- which entries are REACHED
    layer 2   open(...).read()  -- which reached entries are READ

mg-5040 installed a residue at layer 1: every entry the walk declined is
returned with its reason, and an entry declined for a reason no sentence
carries is counted into that checker's own TOTAL BAD.  Layer 2 was left as it
was -- one `except (UnicodeDecodeError, OSError)` and a printed sentence
saying the reason was the file's ENCODING.

So A REGULAR FILE THIS PROCESS CANNOT OPEN passed layer 1 (os.path.isfile
true, residue empty), failed layer 2 with `PermissionError`, and was filed
under a bucket naming a cause it does not have: printed, not counted, contents
never scanned, `w3_scope.py` exit 0 and its runner GREEN over a live X4
statement.

THREE DEFECTS IN ONE PATH, and the ticket orders them: the failure is
MISCLASSIFIED, the scope check goes SILENT rather than erroring, and the
runner is green.  The classification is repaired first, because a wrong bucket
sends every later reader to the wrong hypothesis -- that is worse than no
bucket, and it is the half of F1 that outlives the exit code.

WHAT IS COUNTED AND WHAT IS NOT, and why they differ.  Layer 2's two declines
are separated by the exception that produced them and treated by the rule
layer 1 already uses:

  ENCODING     UnicodeDecodeError.  STATED, printed, NOT counted.  A sentence
               has carried this exclusion since mg-d633 -- the printed extent
               says the run covers every regular file LESS the ones named as
               undecodable -- and mg-6cb9's a1_bothways.py Q18 asserts exit 0
               for exactly this case.  A stated rule a reader meets before the
               surprise is not the defect; the defect is a rule no sentence
               carries.
  UNREADABLE   OSError.  NOT STATED, printed, COUNTED.  No extent line in this
               repository has ever put a regular file this process cannot open
               outside the claim.

  V2a  the baseline -- no plant, everything green
  V2b  an UNREADABLE regular file with a live X4 statement
  V2c  the attribution control -- the same statement, readable
  V2d  a readable file whose bytes are not UTF-8
  V2e  are the two printed lines distinguishable?  (mg-6ef4's P1d, inverted)
  V2f  the same plant at the pin -- F1 reproduced, and closed
  V2g  the fourth checker, measured and NOT repaired here

    python3 code/species_rung_repair_4adb/v2_layer2.py
"""

import os
import sys

from kern4adb import (hdr, RUNNERS, Probe, prove, run_checker, run_runner,
                      show, PRE)

bad = 0
missed = 0

# The plant is NOT a *.md.  `e2_crosssection.py` reads every *.md under code/
# and docs/ with an unguarded `open`, so an unreadable *.md makes e2 raise --
# and every runner would go red through a traceback in a checker that has
# nothing to do with this finding.  A red that proves the wrong thing is
# mg-5040's kept defect 3.  V2g measures that separately and says so.
PLANT = "code/species_7d75/mg4adb_plant.txt"
BLOB = "code/species_7d75/mg4adb_blob.bin"
READABLE = "code/species_7d75/mg4adb_readable.txt"

# A LIVE X4 STATEMENT.  X4 is `w3_scope.py`'s first FORBIDDEN row: T3d's
# "four candidate identifications, three are controls".  The text below
# matches that row's pattern and carries no marker quoting it as corrected, so
# a checker that READS this file must report STILL ASSERTED.
X4 = ("A planted paragraph for mg-4adb: of the four candidate "
      "identifications, three are controls.\n")

# Bytes that are not valid UTF-8 and are not a permission problem.
NOT_UTF8 = b"\xff\xfe\x00\x01mg-4adb"

W3 = ("species_remainder_f8fa", "w3_scope.py")
S1 = ("species_repair_a4ef", "s1_extent.py")
E1 = ("species_extent_d633", "e1_extents.py")
E2 = ("species_extent_d633", "e2_crosssection.py")

UNREADABLE_WORDS = ("REACHED AND NOT READ", "PermissionError")


def row(label, ok, detail=""):
    global bad
    bad += (not ok)
    print("  %-64s %s" % (label[:64], "ok" if ok else "*** FINDING ***"))
    for ln in detail.splitlines():
        if ln:
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


def lines_naming(out, needle):
    """Every output line that names `needle`.

    A disposition is read off ONE LINE and never off the whole run: mg-6ef4's
    P1f matched a marker in a legend and a filename hundreds of lines apart
    and recorded three catches that had not happened.  So the caller is given
    the lines and picks the one carrying the marker it is asking about, and
    the COUNT is printed -- a file named on four lines and a file named on one
    are different facts and this instrument does not flatten them.
    """
    return [l for l in out.splitlines() if needle in l]


def line_with(out, needle, marker):
    """The single line naming `needle` AND carrying `marker`, or ''."""
    hits = [l for l in lines_naming(out, needle) if marker in l]
    return hits[0] if len(hits) == 1 else ""


# ---------------------------------------------------------------------------
# V2a  BASELINE
# ---------------------------------------------------------------------------
hdr("V2a  BASELINE -- NO PLANT.  A REPAIR THAT REDDENS A CLEAN TREE HAS MOVED "
    "THE PROBLEM")

CLEAN = {}
for lab, (d, s) in (("w3_scope.py", W3), ("s1_extent.py", S1),
                    ("e1_extents.py", E1), ("e2_crosssection.py", E2)):
    rc, out = run_checker(d, s)
    CLEAN[lab] = rc
    note("%s" % lab, "exit %d" % rc)
for rn in RUNNERS:
    rc, _o = run_runner(rn)
    CLEAN[rn] = rc
    note("code/%s/run_all.sh" % rn, "exit %d" % rc)
print()
row("4 of 4 checkers and 3 of 3 runners are GREEN with no plant",
    all(v == 0 for v in CLEAN.values()),
    "\n".join("%s: exit %d" % (k, v) for k, v in sorted(CLEAN.items())
              if v != 0))
score("P3h", True, all(v == 0 for v in CLEAN.values()))
print()


# ---------------------------------------------------------------------------
# V2b  THE UNREADABLE FILE
# ---------------------------------------------------------------------------
hdr("V2b  A REGULAR FILE AT MODE 000, CARRYING A LIVE X4 STATEMENT")

print("  It is a REGULAR FILE: `os.path.isfile` is true and layer 1's residue")
print("  is empty, so nothing the walk reports mentions it.  It fails at")
print("  layer 2, where until this ticket the only bucket said ENCODING.")
print()

UNREAD = {}
with Probe("v2b") as pr:
    pr.write(PLANT, X4, mode=0o000)
    for lab, (d, s) in (("w3_scope.py", W3), ("s1_extent.py", S1),
                        ("e1_extents.py", E1)):
        rc, out = run_checker(d, s)
        hits = lines_naming(out, os.path.basename(PLANT))
        line = line_with(out, os.path.basename(PLANT), "NOT STATED") \
            or (hits[0] if hits else "")
        UNREAD[lab] = (rc, bool(hits), line)
        print("      %-18s exit %d   lines naming the file: %d"
              % (lab, rc, len(hits)))
        for h in hits:
            print("          %s" % h.strip()[:104])
    for rn in RUNNERS:
        rc, out = run_runner(rn)
        UNREAD[rn] = (rc, os.path.basename(PLANT) in out, "")
        print("      %-18s exit %d" % ("code/%s" % rn, rc))
prove(pr)
print()

row("`w3_scope.py` EXITS 1 -- the silent scope check is the ticket's OPEN 2",
    UNREAD["w3_scope.py"][0] == 1)
row("and it NAMES the file", UNREAD["w3_scope.py"][1])
row("on a line saying REACHED AND NOT READ and naming PermissionError",
    all(w in UNREAD["w3_scope.py"][2] for w in UNREADABLE_WORDS),
    "line: %s" % UNREAD["w3_scope.py"][2].strip()[:110])
row("and that line does NOT attribute it to the file's ENCODING",
    "NOT an encoding problem" in UNREAD["w3_scope.py"][2]
    and "not valid UTF-8" not in UNREAD["w3_scope.py"][2],
    "A wrong bucket sends the next reader to the wrong hypothesis.  This is\n"
    "the half of F1 that outlives the exit code, which is why the ticket\n"
    "asks for the classification FIRST.")
row("`s1_extent.py` exits 1", UNREAD["s1_extent.py"][0] == 1)
row("`e1_extents.py` exits 1", UNREAD["e1_extents.py"][0] == 1)
row("`e1_extents.py` names it -- the tracer no longer counts a failed open "
    "as a read", UNREAD["e1_extents.py"][1])
row("the f8fa runner is RED over the live statement",
    UNREAD["species_remainder_f8fa"][0] == 1)
row("the a4ef runner is RED over the live statement",
    UNREAD["species_repair_a4ef"][0] == 1)
score("P3a", 1, UNREAD["w3_scope.py"][0])
score("P3b", True,
      "NOT an encoding problem" in UNREAD["w3_scope.py"][2]
      and "not valid UTF-8" not in UNREAD["w3_scope.py"][2])
score("P3c", 1, UNREAD["species_remainder_f8fa"][0])
score("P3f", 1, UNREAD["s1_extent.py"][0])
score("P3g", 1, UNREAD["e1_extents.py"][0])
print()


# ---------------------------------------------------------------------------
# V2c  THE ATTRIBUTION CONTROL
# ---------------------------------------------------------------------------
hdr("V2c  THE SAME STATEMENT IN A READABLE FILE -- IS THE MODE THE REASON?")

print("  Without this row, V2b shows a checker going red with a file planted")
print("  and nothing more.  This one puts the SAME text in a file the process")
print("  can read: if the checker reports STILL ASSERTED here, then V2b's")
print("  silence-before and red-now are about the MODE and not about the")
print("  statement.  mg-6ef4 ran this control and it is kept.")
print()

with Probe("v2c") as pr:
    pr.write(READABLE, X4)
    rc, out = run_checker(*W3)
    asserted = [l for l in out.splitlines()
                if "STILL ASSERTED AT" in l and os.path.basename(READABLE) in l]
    print("      w3_scope.py        exit %d   STILL ASSERTED lines naming it: %d"
          % (rc, len(asserted)))
    for l in asserted:
        print("          %s" % l.strip())
prove(pr)
print()
row("a readable copy of the same statement is caught and NAMED",
    rc == 1 and len(asserted) == 1,
    "So the checker's extent does cover this text, and what V2b measures is\n"
    "the difference the MODE makes -- not a statement outside the list.")
print()


# ---------------------------------------------------------------------------
# V2d  THE NON-UTF-8 FILE
# ---------------------------------------------------------------------------
hdr("V2d  A READABLE FILE WHOSE BYTES ARE NOT UTF-8 -- THE STATED DECLINE")

ENC = {}
with Probe("v2d") as pr:
    pr.write_bytes(BLOB, NOT_UTF8)
    for lab, (d, s) in (("w3_scope.py", W3), ("s1_extent.py", S1)):
        rc, out = run_checker(d, s)
        hits = lines_naming(out, os.path.basename(BLOB))
        line = line_with(out, os.path.basename(BLOB), "UTF-8") \
            or (hits[0] if hits else "")
        ENC[lab] = (rc, bool(hits), line)
        print("      %-18s exit %d   lines naming the file: %d"
              % (lab, rc, len(hits)))
        for h in hits:
            print("          %s" % h.strip()[:104])
prove(pr)
print()
row("`w3_scope.py` exits 0 -- a STATED decline is not a finding",
    ENC["w3_scope.py"][0] == 0,
    "The sentence that carries it has been in the printed extent since\n"
    "mg-d633, and mg-6cb9's a1_bothways.py Q18 asserts this exit code for\n"
    "this exact plant.  Counting it would redden a landed audit's control\n"
    "and would make the two buckets differ only in wording, which is the\n"
    "defect wearing a second coat.")
row("and it NAMES the file, so the exclusion cannot grow unseen",
    ENC["w3_scope.py"][1])
row("the line says UTF-8 and does NOT say the file could not be opened",
    "UTF-8" in ENC["w3_scope.py"][2]
    and "PermissionError" not in ENC["w3_scope.py"][2])
row("`s1_extent.py` exits 0 for the same plant", ENC["s1_extent.py"][0] == 0)
score("P3d", 0, ENC["w3_scope.py"][0])
score("P3i", 0, ENC["s1_extent.py"][0])
print()


# ---------------------------------------------------------------------------
# V2e  ARE THE TWO LINES DISTINGUISHABLE?
# ---------------------------------------------------------------------------
hdr("V2e  THE TWO PRINTED LINES, SIDE BY SIDE -- mg-6ef4's P1d, INVERTED")

print("  mg-6ef4 predicted these two would be indistinguishable to a reader:")
print("  same list, same sentence, and the sentence FALSE for the unreadable")
print("  one.  That prediction was a hit against the code as it stood.  The")
print("  same two lines now:")
print()
print("      UNREADABLE: %s" % UNREAD["w3_scope.py"][2].strip()[:110])
print("      ENCODING:   %s" % ENC["w3_scope.py"][2].strip()[:110])
print()
row("the two lines differ, and each names the exception that produced it",
    UNREAD["w3_scope.py"][2].strip() != ENC["w3_scope.py"][2].strip()
    and "PermissionError" in UNREAD["w3_scope.py"][2]
    and "UnicodeDecodeError" in ENC["w3_scope.py"][2])
row("the unreadable one is in the NOT STATED list and the other is not",
    "NOT STATED" in UNREAD["w3_scope.py"][2]
    and "NOT STATED" not in ENC["w3_scope.py"][2],
    "STATED / NOT STATED is layer 1's own vocabulary (mg-5040).  Layer 2\n"
    "uses it rather than inventing a second one, so a reader who has read\n"
    "the walk's residue already knows what the second list means.")
score("P3e", True,
      UNREAD["w3_scope.py"][2].strip() != ENC["w3_scope.py"][2].strip())
print()


# ---------------------------------------------------------------------------
# V2f  THE SAME PLANT AT THE PIN
# ---------------------------------------------------------------------------
hdr("V2f  THE SAME PLANT AGAINST THE PRE-REPAIR CHECKERS (%s)" % PRE)

print("  The before-figure is re-derived rather than quoted.  The three files")
print("  this ticket changed are written back at the pin, the SAME plant is")
print("  made, and the same checkers are run.  Everything else is at HEAD,")
print("  which is stated because it is what this comparison cannot hold")
print("  fixed.")
print()

PINNED_FILES = [
    "code/species_remainder_f8fa/w3_scope.py",
    "code/species_repair_a4ef/s1_extent.py",
    "code/species_extent_d633/trace_open.py",
    "code/species_extent_d633/e1_extents.py",
]
PIN = {}
with Probe("v2f") as pr:
    for rel in PINNED_FILES:
        pr.write(rel, show(PRE, rel))
    pr.write(PLANT, X4, mode=0o000)
    for lab, (d, s) in (("w3_scope.py", W3), ("s1_extent.py", S1),
                        ("e1_extents.py", E1)):
        rc, out = run_checker(d, s)
        hits = lines_naming(out, os.path.basename(PLANT))
        line = hits[0] if hits else ""
        PIN[lab] = (rc, line)
        print("      %-18s exit %d   line naming it: %s"
              % (lab, rc, line.strip()[:70] if line else "(none)"))
    rc, out = run_runner("species_remainder_f8fa")
    PIN["runner"] = (rc, "")
    print("      %-18s exit %d" % ("f8fa run_all.sh", rc))
prove(pr)
print()
row("at the PIN, `w3_scope.py` exits 0 over the live statement",
    PIN["w3_scope.py"][0] == 0,
    "This row being `ok` is mg-6ef4's F1 reproduced independently.  If it\n"
    "is a FINDING then the before-state was not what F1 described.")
row("at the PIN, its runner is GREEN over the live statement",
    PIN["runner"][0] == 0)
row("at the PIN the file is filed under the ENCODING sentence",
    "UTF-8" in PIN["w3_scope.py"][1] or "decodable" in PIN["w3_scope.py"][1],
    "pin line:  %s" % PIN["w3_scope.py"][1].strip()[:110])
row("AT HEAD IT IS EXIT 1, NAMED, AND IN THE RIGHT BUCKET",
    UNREAD["w3_scope.py"][0] == 1
    and all(w in UNREAD["w3_scope.py"][2] for w in UNREADABLE_WORDS))
print()


# ---------------------------------------------------------------------------
# V2g  THE FOURTH CHECKER, MEASURED AND NOT REPAIRED
# ---------------------------------------------------------------------------
hdr("V2g  `e2_crosssection.py` ON AN UNREADABLE *.md -- MEASURED, NOT FIXED")

print("  e2 reads every *.md under code/ and docs/ with an unguarded `open`.")
print("  This ticket does not change that, and the reason is a distinction")
print("  the ticket itself draws: OPEN 2 is about a failure filed under the")
print("  WRONG NAME and a checker going SILENT.  e2 does neither -- it")
print("  raises, and a traceback is loud.  It is measured here so that the")
print("  choice is a measurement in a transcript rather than an omission,")
print("  and it is left for whoever takes the next verdict.")
print()

with Probe("v2g") as pr:
    pr.write("code/species_7d75/mg4adb_plant.md", X4, mode=0o000)
    rc, out = run_checker(*E2)
    traceback = "PermissionError" in out or "Traceback" in out
    print("      e2_crosssection.py exit %d   raises: %s   silent: %s"
          % (rc, "yes" if traceback else "no",
             "no" if (rc != 0 or traceback) else "YES"))
prove(pr)
print()
note("disposition", "NOTED, NOT REPAIRED -- loud, not silent")
row("it does not go silently green, which is what OPEN 2 is about",
    rc != 0 or traceback)
print()


print("=" * 78)
print("V2 TOTAL BAD: %d" % bad)
print("V2 PREDICTIONS MISSED: %d" % missed)
print("=" * 78)
print()
print("EXTENT OF THAT NUMBER.  Four checkers and three runners, over ONE")
print("planted unreadable file, ONE planted non-UTF-8 file and ONE readable")
print("control, in code/species_7d75 only, at HEAD and at %s.  It says" % PRE)
print("NOTHING about a file that becomes unreadable BETWEEN the two layers,")
print("about a directory this process cannot read (mg-5040 measured that at")
print("layer 1), or about any tree other than the four these checkers name.")
sys.exit(1 if bad else 0)
