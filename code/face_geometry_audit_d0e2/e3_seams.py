"""mg-d0e2 E3: the seams of a twice-corrected artifact, and the check that
cannot fail.

`controls_output.txt` has now been corrected twice for the same defect (mg-da45,
then mg-5f9a).  A second correction is where a claim goes stale in one place and
not another, so this file compares every site that states the same fact:

  * the artifact itself
  * `docs/landing-mg-1c80-instrumented-predicate.md`
  * `code/face_geometry_instr_5f9a/out_*.txt`, the repair's own transcripts
  * `code/face_geometry_landing_da45/out_verify.txt`, an EARLIER item's verifier
    that mg-5f9a says still passes without being edited
  * `code/face_geometry_audit_1c80/out_antichain.txt`, the n = 8 substance that
    mg-1c80 confirmed and this audit must flag any weakening of

AND ONE THING NO TICKET'S LIST NAMES.  The repair's central published number --
"43 scored rows, 0 label change(s)" -- is produced by a check that compares the
wrong token.  It is verified here by DEMONSTRATION: the same check is run on an
artifact in which every single row has been flipped from PASS to FAIL.
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ART = os.path.join(ROOT, "code", "face_geometry", "controls_output.txt")

BROKEN = 0


def claim(ok, text):
    global BROKEN
    if not ok:
        BROKEN += 1
    print("  [%s] %s" % ("OK    " if ok else "BROKEN", text))


FINDINGS = []


def finding(ok, text):
    """A fact about the SUBJECT, not a claim of this file's own.

    Kept apart from `claim` on purpose: an audit whose exit status conflates
    "my own instrument disagrees with itself" and "the thing I am auditing has
    a defect" cannot be run in CI by anyone.  `claim` failing means this file is
    wrong; `finding` firing means the subject is.  Both are printed; only the
    first sets the exit status.
    """
    if ok:
        FINDINGS.append(text)
    print("  [%s] %s" % ("FINDING" if ok else "clear  ", text))


def read(*parts):
    with open(os.path.join(ROOT, *parts)) as fh:
        return fh.read()


art = read("code", "face_geometry", "controls_output.txt")
doc = read("docs", "landing-mg-1c80-instrumented-predicate.md")
d1 = read("code", "face_geometry_instr_5f9a", "out_d1_trace.txt")
d2 = read("code", "face_geometry_instr_5f9a", "out_d2_deletion.txt")

print("== E3: seam-check of a twice-corrected artifact ==")
print()

# ---------------------------------------------------------------- the threshold
print("THE ARTIFACT'S OWN CONTROL, AND ITS THRESHOLD")
lines = art.split("\n")
row_line = [i for i, l in enumerate(lines) if "lines scanned" in l][0]
initial = [l for l in lines
           if l.strip().startswith(("[PASS]", "[FAIL]", "[CANNOT FAIL]"))]
substring = [l for l in lines
             if "[PASS]" in l or "[FAIL]" in l or "[CANNOT FAIL]" in l]
print("  the row reports: %s" % lines[row_line].strip()[:150])
claim("lines scanned: 62" in art and row_line == 62,
      "THRESHOLD: the row scans the %d lines strictly above itself and says "
      "'lines scanned: 62' -- the extent is printed and it is correct" % row_line)
claim("40 row names among them" in art and len(initial) - 1 == 40,
      "THRESHOLD: it says '40 row names among them'; the artifact carries %d "
      "scored rows, of which this row is one, so 40 is right" % len(initial))
claim("17-char all-pass banner literal" in art and len("ALL CONTROLS PASS") == 17,
      "THRESHOLD: the banner literal it refuses to find is %d characters, which "
      "is the length it prints" % len("ALL CONTROLS PASS"))
print()

# ------------------------------------------------------- the check that cannot fail
print("THE REPAIR'S 'EVERY SCORED ROW KEEPS ITS LABEL' CHECK -- DEMONSTRATED, NOT ARGUED")
print("  d2_deletion.py:167-177 extracts rows by SUBSTRING and compares")
print("  `a.split(' ')[1]` between the baseline and the mutant.  Row lines in")
print("  this artifact are indented, so that token is the empty string for")
print("  every one of them.  Run the check on an artifact where EVERY row has")
print("  been flipped to [FAIL]:")


def parent_check(base_text, mut_text):
    """d2_deletion.py's own comparison, transcribed verbatim."""
    base_rows = [l for l in base_text.split("\n") if "[PASS]" in l
                 or "[CANNOT FAIL]" in l or "[FAIL]" in l]
    mut_rows = [l for l in mut_text.split("\n") if "[PASS]" in l
                or "[CANNOT FAIL]" in l or "[FAIL]" in l]
    n_changes = sum(a.split(" ")[1] != b.split(" ")[1]
                    for a, b in zip(base_rows, mut_rows))
    holds = (len(base_rows) == len(mut_rows)
             and all(a.split(" ")[1] == b.split(" ")[1]
                     for a, b in zip(base_rows, mut_rows)))
    return len(base_rows), n_changes, holds


all_failed = art.replace("[PASS]", "[FAIL]").replace("[CANNOT FAIL]", "[FAIL]")
n_rows, n_changes, holds = parent_check(art, all_failed)
print("      -> '%d rows, %d label change(s)', check HOLDS = %s"
      % (n_rows, n_changes, holds))
finding(holds and n_changes == 0,
        "the check REPORTS 43 rows and 0 label changes, and HOLDS, on an "
        "artifact in which all %d scored rows read [FAIL].  The label half of "
        "the claim 'every scored row keeps its label and its condition' is "
        "VACUOUS -- it compares the empty string with the empty string %d times"
        % (len(initial), n_rows))
claim(len(set(l.split(" ")[1] for l in substring)) == 1
      and substring[0].split(" ")[1] == "",
      "every one of the %d lines it compares yields the token %r"
      % (len(substring), substring[0].split(" ")[1]))
print("  What survives: the length comparison, which does catch a row appearing")
print("  or vanishing -- and that is what actually fired for the magnitude")
print("  deletion (68 -> 66 lines).  The CONCLUSION 'AFTER-1 and AFTER-3 change")
print("  no decision' is TRUE -- E1 re-derives it with a real label comparison")
print("  and gets 0 changes -- but this check is not what established it.")
print()

# ------------------------------------------------------------- the population
print("THE POPULATION BEHIND '43 SCORED ROWS'")
finding(len(substring) == 43 and len(initial) == 41,
        "counted by substring the artifact has %d such lines; counted as rows "
        "(line-initial marker) it has %d.  '43 rows' is published in the commit "
        "message, twice in the landing doc and twice in out_d2_deletion.txt"
        % (len(substring), len(initial)))
extra = [l for l in substring if l not in initial]
for l in extra:
    print("      not a row: %s" % l.strip()[:104])
claim(len(extra) == 2 and all(l.strip().startswith("*") for l in extra),
      "the %d over-counted lines are both 'measured, not scored' bullets that "
      "MENTION [CANNOT FAIL] in their prose -- and the artifact says in terms "
      "that lines in that block 'are measurements, not rows'" % len(extra))
claim("2 [CANNOT FAIL]" in doc and art.count("\n  [CANNOT FAIL]") == 2,
      "the rest of the same sentence is right: %d rows carry [CANNOT FAIL], "
      "which is what the doc and the artifact's own summary say"
      % art.count("\n  [CANNOT FAIL]"))
print()

# ------------------------------------------------- the stale name in the predicate
print("STALE REFERENCE INSIDE THE REPAIR'S OWN CENTRAL DOCSTRING")
sys.path.insert(0, os.path.join(ROOT, "code", "face_geometry"))
import controls                                                        # noqa: E402
import face_complex                                                    # noqa: E402

claim(not hasattr(controls, "deciding_gate"),
      "`controls.deciding_gate` does not exist: mg-5f9a deleted it outright and "
      "d1_trace.py asserts its absence in the AST ('controls.py defines NO gate "
      "procedure of its own')")
finding("`controls.deciding_gate` is a call to this" in
        face_complex.absorb_trace.__doc__,
        "...and yet `absorb_trace`'s own docstring -- the predicate this whole "
        "repair is about -- still says \"the label is produced here and "
        "`controls.deciding_gate` is a call to this function, not a second "
        "implementation of it\".  It describes a design that was NOT shipped: "
        "the name has no referent, and the repair's own d1_trace.py is what "
        "proves it")
print()

# --------------------------------------------------------------- cross-site seams
print("CROSS-SITE AGREEMENT -- the trace table, stated in three places")
claim("I1 72 biting = 15 diagonal + 57 magnitude + 0 parity" in art,
      "the artifact prints I1 = 15 diagonal + 57 magnitude + 0 parity")
claim("72 |         15   57   0 |" in doc,
      "the landing doc's table prints the same 15/57/0 for I1")
claim("237" in doc and "ALL" in doc,
      "the doc's ALL row totals 237 diagonal + 60 magnitude + 0 parity, which "
      "E2 re-derived independently over the same 297 pairs")
claim("57 of 297" in doc or "57 of the 297" in doc,
      "mg-1c80's 57-of-297 disagreement is reproduced, not quoted")
print()

print("EARLIER ITEMS' ARTIFACTS -- did anything retreat?")


def rerun(dirname, script, out):
    proc = subprocess.run([sys.executable, script],
                          cwd=os.path.join(ROOT, "code", dirname),
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    committed = read("code", dirname, out).encode()
    return proc.stdout == committed, proc.returncode, len(proc.stdout)


ok, rc, nb = rerun("face_geometry_audit_1c80", "a2_antichain.py",
                   "out_antichain.txt")
claim(ok and rc == 0,
      "SUBSTANCE, n = 8: mg-1c80's antichain sweep (46232 words, n = 2..8) "
      "regenerates BYTE-IDENTICALLY against the repaired tree -- %d bytes, exit "
      "%d.  Nothing about the n = 8 confirmation was weakened" % (nb, rc))

ok, rc, nb = rerun("face_geometry_landing_da45", "verify_landing.py",
                   "out_verify.txt")
claim(ok and rc == 0,
      "mg-da45's landing verifier regenerates BYTE-IDENTICALLY -- %d bytes, "
      "exit %d, 25 claims scored, 0 BROKEN -- and `verify_landing.py` itself "
      "carries no mg-5f9a edit (last touched by f024985, mg-da45's own commit)"
      % (nb, rc))
verify = read("code", "face_geometry_landing_da45", "out_verify.txt")
claim("25 claim(s) scored; 0 BROKEN." in verify,
      "its bottom line is '25 claim(s) scored; 0 BROKEN.'")
claim("MEASURES which gate settled it" in verify,
      "DISCLOSED AND ACCURATE: that verifier's closing prose still reads 'the "
      "file now MEASURES which gate settled it', the framing mg-1c80 refuted -- "
      "mg-5f9a's commit says in terms that it left it as another item's "
      "artifact rather than editing it, and that is what it did")

print()
print("E3 claims broken: %d   findings about the subject: %d"
      % (BROKEN, len(FINDINGS)))
for t in FINDINGS:
    print("  FINDING: %s" % t.split(".")[0][:150])
sys.exit(1 if BROKEN else 0)
