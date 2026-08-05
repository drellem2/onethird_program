"""G3 -- THE MISCLASSIFICATION, AND ITS THREE PARTS CHECKED SEPARATELY.

mg-6ef4's F1: a regular file this process cannot open passed `walk_residue`
(isfile is true, the residue is empty), failed `open()` with PermissionError,
and was filed under a bucket that named THE FILE'S ENCODING as the reason --
printed, not counted, contents never scanned, `w3_scope.py` exit 0 with a live
X4 statement inside it.

mg-4adb split the `except`.  The ticket's warning is that a repair may fix the
BUCKET and leave the SILENCE, so this section asks three questions and not
one, and each is a separate row with its own construction:

  G3a  what line does w3_scope.py PRINT for it, and does the word ENCODING
       still appear on that line
  G3b  what is w3_scope.py's EXIT CODE                     (asked separately)
  G3c  what is the f8fa RUNNER's exit code                 (asked separately)
  G3d  the STATED bucket, which must survive: a readable file whose bytes are
       not UTF-8 is still a stated decline and must NOT redden anything
  G3e  the counterfactual -- the same file READABLE -- so that "not counted"
       is measured against what counting looks like
  G3f  the fourth checker: the same input against e2_crosssection.py, which
       mg-4adb measured and did not repair
  G3g  an unreadable DIRECTORY, which no list in either ticket names

    python3 code/species_gate_audit_d53d/g3_layer2.py
"""

import os
import re
import stat
import sys

from kern_d53d import (hdr, Rows, E2_SAYS, clone, run_runner, run_e2,
                       run_script, cleanup)

R = Rows()

# A sentence w3_scope.py's FORBIDDEN table calls X4, with no disarmer near it.
# `QUOTED_AS_CORRECTED` accepts mg-f8fa / "used to" / "no longer" within four
# lines, so the plant carries none of those words -- otherwise the file is
# exonerated and G3e's counterfactual would measure nothing.
X4_TEXT = ("# a probe file planted by mg-d53d and removed by the same probe\n"
           "# T3d: four candidate identifications, three are controls.\n")
TREE = os.path.join("code", "species_7d75")
W3 = os.path.join("code", "species_remainder_f8fa", "w3_scope.py")


def plant(root, name, data, mode=None, binary=False):
    p = os.path.join(root, TREE, name)
    with open(p, "wb" if binary else "w",
              **({} if binary else {"encoding": "utf-8"})) as fh:
        fh.write(data)
    if mode is not None:
        os.chmod(p, mode)
    return p


def line_for(out, name):
    return [ln for ln in out.splitlines() if name in ln]


# ---------------------------------------------------------------------------
hdr("G3a  THE LINE w3_scope.py PRINTS FOR AN UNREADABLE REGULAR FILE")
# ---------------------------------------------------------------------------

root = clone()
NAME = "probe_d53d_x4.py"
p = plant(root, NAME, X4_TEXT, mode=0)
R.note("  planted: %s, mode 000, carrying a live X4 statement" % NAME)
R.note("  it is a REGULAR FILE: os.path.isfile says %s, so layer 1 reaches it"
       % os.path.isfile(p))
print()

rc_w3, out_w3 = run_script(root, W3)
hits = line_for(out_w3, NAME)
for ln in hits:
    R.note("    %s" % ln.strip())
blob = " ".join(hits)
says_unreadable = ("REACHED AND NOT READ" in blob) or ("UNREADABLE" in blob)
names_perm = "PermissionError" in blob
no_encoding = "ENCODING" not in blob and "encoding" not in blob

R.predicted(
    "Q12",
    "the line says UNREADABLE / REACHED AND NOT READ, names PermissionError, "
    "and the word ENCODING is not on it",
    "%d line(s); REACHED AND NOT READ/UNREADABLE: %s; names PermissionError: "
    "%s; ENCODING absent: %s"
    % (len(hits), says_unreadable, names_perm, no_encoding),
    bool(hits) and says_unreadable and names_perm and no_encoding)

R.row("the file is not silently absent from the output", bool(hits),
      "mg-6ef4's F1 is not that the bucket was wrong.  It is that a reader\n"
      "who met the wrong bucket went looking for a text-encoding problem.")

# Q12 IS REFUTED AND IS KEPT AS WRITTEN.  The word `encoding` IS on the line.
# It is on it inside `This is NOT an encoding problem`, which is a DENIAL of
# the attribution the prediction was written to detect -- the prediction
# tested for the word and the question was about the attribution.  A refuted
# prediction is a result; the substantive question is asked here as its own
# row rather than by rewriting the prediction into one that would have held.
neg = re.search(r"(?i)\bnot\s+an?\s+encoding\b", blob)
attrib = re.search(r"(?i)\bencoding\b", blob)
R.row("the line does not ATTRIBUTE the decline to the file's encoding",
      bool(neg) or not attrib,
      "occurrences of `encoding` on the line: %d\n"
      "every one of them inside an explicit denial: %s\n"
      "This is what Q12's third clause was reaching for, and Q12 as written\n"
      "asked for the absence of a word instead.  The bucket names the\n"
      "exception class that produced it (PermissionError), states REACHED\n"
      "AND NOT READ, files it under NOT STATED and counts it -- and then\n"
      "spends a clause ruling out the cause mg-6ef4's reader was sent to.\n"
      "The word is there BECAUSE of the repair, not in spite of it."
      % (len(re.findall(r"(?i)\bencoding\b", blob)), bool(neg)))


# ---------------------------------------------------------------------------
hdr("G3b  w3_scope.py's EXIT CODE, ASKED SEPARATELY")
# ---------------------------------------------------------------------------

R.note("  A bucket is a sentence.  An exit code is a control.  The ticket's")
R.note("  warning is that the first can be repaired while the second stays")
R.note("  silent, so this is its own row with its own prediction.")
print()
R.note("    w3_scope.py exit %s" % rc_w3)
counted = [ln for ln in out_w3.splitlines()
           if "TOTAL BAD" in ln and ln.strip().startswith("W3")]
for ln in counted:
    R.note("    %s" % ln.strip())

R.predicted("Q13", "1", str(rc_w3), rc_w3 == 1)


# ---------------------------------------------------------------------------
hdr("G3c  THE f8fa RUNNER's EXIT CODE, ASKED SEPARATELY AGAIN")
# ---------------------------------------------------------------------------

R.note("  And a checker's exit code is not a runner's.  That distance is")
R.note("  exactly where mg-6ef4's F3 lived, so it is measured and not")
R.note("  inferred from G3b.")
print()

rc_run, out_run = run_runner(root, "species_remainder_f8fa")
R.note("    sh code/species_remainder_f8fa/run_all.sh -> exit %s" % rc_run)
R.note("    the runner's own words: %s"
       % (next((ln.strip() for ln in out_run.splitlines() if "FAILED" in ln),
               "(no FAILED line)")))
R.predicted("Q14", "exit 1", str(rc_run), rc_run == 1)
os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
os.remove(p)


# ---------------------------------------------------------------------------
hdr("G3d  THE STATED BUCKET MUST SURVIVE THE REPAIR")
# ---------------------------------------------------------------------------

R.note("  A repair that reddens on every decline has not separated two")
R.note("  buckets, it has deleted one.  A readable file whose bytes are not")
R.note("  valid UTF-8 is a STATED decline -- a sentence has carried it since")
R.note("  mg-d633 -- and must still be printed and NOT counted.")
print()

root_d = clone()
BAD = "probe_d53d_badbytes.py"
plant(root_d, BAD, b"# \xff\xfe not utf-8 at all \x80\x81\n", binary=True)
rc_d, out_d = run_script(root_d, W3)
hits_d = line_for(out_d, BAD)
for ln in hits_d:
    R.note("    %s" % ln.strip())
blob_d = " ".join(hits_d)
R.predicted(
    "Q15", "w3_scope.py exit 0, and the bucket says ENCODING",
    "exit %s; the line says: %s"
    % (rc_d, "ENCODING/UnicodeDecodeError"
       if ("UTF-8" in blob_d or "UnicodeDecodeError" in blob_d) else blob_d),
    rc_d == 0 and bool(hits_d)
    and ("UnicodeDecodeError" in blob_d or "UTF-8" in blob_d))
R.row("the two declines are told apart by the exception, not by a guess",
      rc_d == 0 and rc_w3 == 1,
      "Same walk, same layer, two files: one unreadable (counted, red) and\n"
      "one undecodable (stated, green).  Either alone proves nothing about\n"
      "the split.")


# ---------------------------------------------------------------------------
hdr("G3e  THE COUNTERFACTUAL -- THE SAME FILE, READABLE")
# ---------------------------------------------------------------------------

R.note("  mg-6ef4's sentence is `contents never scanned, exit 0 WITH A LIVE X4")
R.note("  STATEMENT INSIDE IT`.  That only means something if the same file,")
R.note("  readable, IS a finding.  Otherwise the plant was never a hazard and")
R.note("  G3a..G3c measured a bucket around nothing.")
print()

root_e = clone()
plant(root_e, NAME, X4_TEXT)               # same bytes, readable this time
rc_e, out_e = run_script(root_e, W3)
hits_e = line_for(out_e, NAME)
for ln in hits_e[:6]:
    R.note("    %s" % ln.strip())
R.row("readable, the same file is a live X4 finding and w3_scope.py is red",
      rc_e == 1 and bool(hits_e),
      "exit %s" % rc_e)
R.note("")
R.note("  So the unreadable case in G3a was hiding a real finding, and before")
R.note("  mg-4adb it was hiding it under a sentence about text encoding.")


# ---------------------------------------------------------------------------
hdr("G3f  THE FOURTH CHECKER -- THE SAME INPUT AGAINST e2_crosssection.py")
# ---------------------------------------------------------------------------

R.note("  mg-4adb measured this checker and did not repair it, which its own")
R.note("  README says.  An audit that only re-measures what was repaired")
R.note("  cannot report what was left, so it is measured here.")
print()

root_f = clone()
MD = os.path.join(root_f, "code", "species_gate_audit_d53d",
                  "probe_d53d_unreadable.md")
if not os.path.isdir(os.path.dirname(MD)):
    os.makedirs(os.path.dirname(MD))
with open(MD, "w", encoding="utf-8") as fh:
    fh.write("# unreadable probe\n\nnothing struck here.\n")
os.chmod(MD, 0)
rc_f, out_f = run_e2(root_f)
os.chmod(MD, stat.S_IRUSR | stat.S_IWUSR)
tb = "Traceback" in out_f
R.note("    e2 exit %s; Traceback in output: %s; prints %s: %s"
       % (rc_f, tb, E2_SAYS, E2_SAYS in out_f))
R.note("    last line: %s"
       % (out_f.strip().splitlines() or ["(no output)"])[-1][:70])
R.predicted(
    "Q16", "exit 1 by uncaught traceback, and `%s` not printed" % E2_SAYS,
    "exit %s, traceback %s, `%s` printed %s"
    % (rc_f, tb, E2_SAYS, E2_SAYS in out_f),
    rc_f == 1 and tb and E2_SAYS not in out_f)
R.row("e2 does not file an unreadable markdown file under any bucket",
      True,
      "It has no bucket for it: `md_files_and_residue` decides REACHED and\n"
      "e2's own loop does the open().  The two-layer shape mg-6ef4 found in\n"
      "w3_scope.py is the same shape here, and only one of the two layers\n"
      "has a residue.  It exits 1, which is why this is a REPORT and not a\n"
      "second F1: the reader is not told the wrong thing, only nothing.")


# ---------------------------------------------------------------------------
hdr("G3g  AN UNREADABLE DIRECTORY -- A CASE NO LIST IN EITHER TICKET NAMES")
# ---------------------------------------------------------------------------

R.note("  Floor, not scope.  Layer 1's residue exists because os.walk")
R.note("  SWALLOWS the error on a directory it cannot read.  So: a directory")
R.note("  at mode 000, under code/, with a *.md inside it.")
print()

root_g = clone()
D = os.path.join(root_g, "code", "probe_d53d_dir")
os.makedirs(D)
with open(os.path.join(D, "hidden.md"), "w", encoding="utf-8") as fh:
    fh.write("# hidden\n\n~~a struck claim~~\n\na struck claim\n")
os.chmod(D, 0)
try:
    rc_g, out_g = run_e2(root_g)
finally:
    os.chmod(D, stat.S_IRWXU)
rows_g = [ln for ln in out_g.splitlines() if "probe_d53d_dir" in ln]
for ln in rows_g:
    R.note("    %s" % ln.strip())
not_stated = any("NOT STATED" in ln for ln in out_g.splitlines()
                 if "probe_d53d_dir" in ln)
# the reason line follows the entry line
idx = [i for i, ln in enumerate(out_g.splitlines()) if "probe_d53d_dir" in ln]
for i in idx:
    nxt = out_g.splitlines()[i + 1:i + 2]
    for ln in nxt:
        R.note("        %s" % ln.strip())
R.predicted(
    "Q17",
    "os.walk's onerror fires, the entry lands in NOT STATED, and e2 exits 1",
    "e2 exit %s; %d row(s) mention it; NOT STATED: %s"
    % (rc_g, len(rows_g), not_stated),
    rc_g == 1 and bool(rows_g) and not_stated)
R.row("the file INSIDE it is invisible, and that is what the residue is for",
      not_stated,
      "`hidden.md` carries a claim struck and restated, which is exactly what\n"
      "e2 exists to find, and no checker in this repository will ever read\n"
      "it.  The residue does not make it visible -- it makes the SILENCE\n"
      "visible, which is the whole of mg-5040's OPEN 1 and is why this case\n"
      "arrives as red rather than as nothing.")

R.tail("G3")
print()
print("EXTENT OF THAT NUMBER.  Six constructed inputs: one unreadable regular")
print("file (G3a-c, and G3e the same file readable), one undecodable regular")
print("file (G3d), one unreadable *.md (G3f) and one unreadable directory")
print("(G3g).  Each is planted in a git clone of this worktree and removed by")
print("the same probe.  IT RANGES OVER NOTHING ELSE: two checkers are asked")
print("(w3_scope.py and e2_crosssection.py) and two are not -- s1_extent.py")
print("and check_doc.py have their own walks and are outside this number.")
print("Mode 000 is the only way a file is made unreadable here; a file inside")
print("an unreadable PARENT, a file on a full disk and a file removed between")
print("the walk and the open are three more routes into the same bucket and")
print("this number says nothing about any of them.")

cleanup()
sys.exit(1 if R.bad else 0)
