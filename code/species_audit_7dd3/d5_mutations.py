"""D5 -- THE BOUNDARY, PROBED FROM BOTH SIDES, ONE MUTATION AT A TIME.

pm-onethird's strengthening of mg-7dd3, in full:

  1. take the printed extent and verify it against what the code actually
     reads;
  2. plant a mutation in something the extent CLAIMS to cover and confirm the
     checker FIRES;
  3. mutate something the extent does NOT claim and confirm it stays SILENT;
  4. report per checker, both directions.

Every mutation below carries the exit code PREDICTED for it in
`PREDICTIONS.md`, written before any of this ran.  The prediction is printed
beside the result and the misses are counted, not corrected.

Each mutation is applied to a fresh scratch copy of `docs/` and the five
species trees, the named checker is run in that copy, and the copy is thrown
away.  The repository is never modified.  In the scratch copy there is no
`.git`, so `s1_extent.py`'s controls (a) and (b) print "git unavailable --
SKIPPED" and do not count -- which is itself PREDICTED and checked as M0.

    python3 code/species_audit_7dd3/d5_mutations.py
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

from kern7dd3 import hdr
from statements7dd3 import DOC

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TREES = ["species_7d75", "species_repair_6f61", "species_remainder_f8fa",
         "species_repair_a4ef", "species_audit_73df"]
DOCREL = "docs/" + DOC
X3_SENTENCE = ("T5 measured it against every Hopf monoid axiom with 0 "
               "failures\non 4399 basis elements.\n")
X8_SENTENCE = ("The dictionary is stated in three independent agreements "
               "about the term.\n")
X4_SENTENCE = "T3d has four candidate identifications, three are controls.\n"

missed = []
results = []


def build(tmp):
    root = os.path.join(tmp, "repo")
    os.makedirs(os.path.join(root, "code"))
    shutil.copytree(os.path.join(REPO, "docs"), os.path.join(root, "docs"))
    for t in TREES:
        shutil.copytree(os.path.join(REPO, "code", t),
                        os.path.join(root, "code", t))
    return root


def at(commit, path):
    r = subprocess.run(["git", "show", "%s:%s" % (commit, path)],
                       cwd=REPO, capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def run(root, rel, argv=()):
    d = os.path.dirname(os.path.join(root, rel))
    r = subprocess.run([sys.executable, os.path.basename(rel)] + list(argv),
                       cwd=d, capture_output=True, text=True)
    return r.returncode, r.stdout


def probe(tag, what, mutate, script, predicted, argv=(), grep=None):
    """Apply `mutate` to a scratch copy, run `script`, compare to the
    prediction written before any of this ran."""
    tmp = tempfile.mkdtemp(prefix="a7dd3_")
    try:
        root = build(tmp)
        mutate(root)
        code, out = run(root, script, argv)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = (code == predicted)
    missed.append(not ok)
    results.append((tag, code, predicted, ok))
    print("  %-4s %-52s %-16s exit %d, predicted %d  %s"
          % (tag, what[:52], os.path.basename(script), code, predicted,
             "ok" if ok else "*** PREDICTION MISSED ***"))
    if grep:
        for line in out.splitlines():
            if re.search(grep, line):
                print("           | %s" % line.strip()[:88])
    return code, out


def edit(rel, fn):
    def go(root):
        p = os.path.join(root, rel)
        with open(p, encoding="utf-8") as fh:
            t = fh.read()
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(fn(t))
    return go


def restore(commit, rel):
    body = at(commit, rel)

    def go(root):
        if body is None:
            raise SystemExit("git unavailable -- cannot build the mutation")
        with open(os.path.join(root, rel), "w", encoding="utf-8") as fh:
            fh.write(body)
    return go


def plant(rel, body):
    def go(root):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a", encoding="utf-8") as fh:
            fh.write("\n" + body)
    return go


def nothing(root):
    return None


S1 = "code/species_repair_a4ef/s1_extent.py"
S2 = "code/species_repair_a4ef/s2_seam.py"
CD = "code/species_repair_6f61/check_doc.py"
W3 = "code/species_remainder_f8fa/w3_scope.py"
C4 = "code/species_audit_73df/c4_scope.py"

# ---------------------------------------------------------------------------
hdr("D5a  M0 -- THE UNMUTATED SCRATCH COPY (control on this harness)")
probe("M0a", "no mutation", nothing, S1, 0, grep=r"git unavailable|TOTAL BAD")
probe("M0b", "no mutation", nothing, S2, 0, grep=r"TOTAL BAD")
probe("M0c", "no mutation", nothing, CD, 0, grep=r"CHECK_DOC:")
probe("M0d", "no mutation", nothing, W3, 0, grep=r"W3 SCOPE:")
print()

# ---------------------------------------------------------------------------
hdr("D5b  s1_extent.py -- INSIDE the extent it claims: MUST FIRE")
probe("M1", "restore ebecd89's t6_fock_and_record.py",
      restore("ebecd89", "code/species_7d75/t6_fock_and_record.py"), S1, 1,
      grep=r"STILL ASSERTED  X3")
probe("M2", "restore ebecd89's out_t6_fock_and_record.txt",
      restore("ebecd89", "code/species_7d75/out_t6_fock_and_record.txt"),
      S1, 1, grep=r"STILL ASSERTED  X3")
probe("M3", "restore ebecd89's t4_one_operation.py",
      restore("ebecd89", "code/species_7d75/t4_one_operation.py"), S1, 1,
      grep=r"STILL ASSERTED  Y2")
probe("M4", "restore ebecd89's document", restore("ebecd89", DOCREL), S1, 1,
      grep=r"LEFT|MISSING")
probe("M6", "§0's headline box back to the plain isomorphism",
      edit(DOCREL, lambda t: t.replace(
          "the left side is **anti-isomorphic to Solomon's\n>   descent "
          "algebra**", "the left side is **Solomon's descent algebra**")),
      S1, 1, grep=r"Y2 |LEFT")
probe("M13", "X3 planted in a NEW .md inside code/species_7d75",
      plant("code/species_7d75/NOTE.md", X3_SENTENCE), S1, 1,
      grep=r"STILL ASSERTED  X3")
print()

hdr("D5c  s1_extent.py -- OUTSIDE the extent it claims: MUST STAY SILENT")
probe("M19", "X3 planted in code/species_audit_73df (declared silent)",
      plant("code/species_audit_73df/NOTE.md", X3_SENTENCE), S1, 0)
probe("M20", "X3 planted in another docs/ file (declared silent)",
      plant("docs/OneThird-Species-Hopf-Monoids-Repair-Extent.md",
            X3_SENTENCE), S1, 0)
print("       Both silences are DECLARED, in the extent line, by name.")
print()

hdr("D5d  s1_extent.py -- THE BOUNDARY: A FILE THE EXTENT CLAIMS AND SKIPS")
probe("M12", "X3 planted in code/species_7d75/run_all.sh",
      plant("code/species_7d75/run_all.sh", "# " + X3_SENTENCE), S1, 0)
print("       code/species_7d75 is one of the FOUR TREES the extent names.")
print("       run_all.sh is inside it and is not one of the FIVE SKIPPED")
print("       FILES the run prints.  It is dropped by an extension filter")
print("       that appears in no extent line and in no printed list.")
print()

hdr("D5e  s1_extent.py -- IS THE MARKER LOAD-BEARING?")
probe("M10", "delete the 'CORRECTED AT SOURCE (mg-a4ef' line only",
      edit("code/species_7d75/t6_fock_and_record.py",
           lambda t: t.replace(
               'print("  CORRECTED AT SOURCE (mg-a4ef, on mg-a61f\'s X3 via '
               'mg-73df).  What")\n', "")), S1, 0)


def strip_window(t):
    """Delete the marker AND every other exonerating phrase in its window."""
    t = t.replace('print("  CORRECTED AT SOURCE (mg-a4ef, on mg-a61f\'s X3 '
                  'via mg-73df).  What")\n', "")
    t = t.replace("mg-6f61 struck it in the document and left it", "it stood")
    t = t.replace("in force here; mg-f8fa's w3_scope.py does not carry it "
                  "on its list.", "in force here.")
    t = t.replace("WHAT 4399 BASIS ELEMENTS MEASURE IS CLOSURE, AND ONLY",
                  "WHAT 4399 BASIS ELEMENTS MEASURE IS A PROPERTY, ONLY")
    t = t.replace("of the document STRIKES:", "of the document says:")
    t = t.replace("stood here -- and in this file's committed output, "
                  "inside a run that", "stands here, in a run that")
    return t


probe("M11", "delete the marker AND every other clause in the window",
      edit("code/species_7d75/t6_fock_and_record.py", strip_window), S1, 1,
      grep=r"STILL ASSERTED  X3")


def strip_window2(t):
    """M11 MISSED ITS PREDICTION AND THE PREDICTION IS KEPT AS WRITTEN.

    The reason is mine, not the checker's: the source reads "IS CLOSURE, AND
    ONLY CLOSURE.", M11 rewrote the first CLOSURE and left the second, so the
    per-statement negation `CLOSURE` still matched.  M11b is the mutation M11
    meant to be, added AFTER the miss and labelled as such.  What M10 settles
    is unaffected: the marker the repair points at is not what holds the
    number up.
    """
    return strip_window(t).replace("PROPERTY, ONLY CLOSURE.  Of",
                                   "PROPERTY, ONLY THAT.  Of")


probe("M11b", "the same, with the SECOND 'closure' removed too (added after "
      "M11 missed)",
      edit("code/species_7d75/t6_fock_and_record.py", strip_window2), S1, 1,
      grep=r"STILL ASSERTED  X3")
print("       M10 vs M11 is the over-determination of D2e, measured: 59% of")
print("       the occurrences inside the extent are held by two or more")
print("       independent clauses, so deleting the marker the repair points")
print("       at need not move the number.")
print()

# ---------------------------------------------------------------------------
hdr("D5f  check_doc.py -- BOTH DIRECTIONS")
probe("M18", "un-strike §4's AM 17.5 quotation (INSIDE its extent)",
      edit(DOCREL, lambda t: t.replace(
          '~~*"Recall from Section 17.4', '*"Recall from Section 17.4', 1)
          .replace('symmetric functions"*~~.', 'symmetric functions"*.', 1)),
      CD, 1, grep=r"AM §17.5|STILL ASSERTED")
probe("M2b", "X3 asserted in code/species_7d75 (OUTSIDE its extent)",
      plant("code/species_7d75/NOTE.md", X3_SENTENCE), CD, 0,
      grep=r"CHECK_DOC:")
print("       The second is declared: 'It reads no code.'  True, measured.")
print()

hdr("D5g  w3_scope.py -- BOTH DIRECTIONS")
probe("M21", "X4 asserted in code/species_7d75 (INSIDE its extent)",
      plant("code/species_7d75/NOTE.md", X4_SENTENCE), W3, 1,
      grep=r"W3 SCOPE:|STILL ASSERTED AT")
probe("M22", "X4 asserted in code/species_repair_6f61 (OUTSIDE it)",
      plant("code/species_repair_6f61/NOTE.md", X4_SENTENCE), W3, 0,
      grep=r"W3 SCOPE:")
print("       Both as declared: 'over ONE tree'.")
print()

hdr("D5h  s2_seam.py -- BOTH DIRECTIONS, AND ITS BOUNDARY")
probe("M5", "restore ebecd89's document -- the duplicate box returns",
      restore("ebecd89", DOCREL), S2, 1, grep=r"NEAR-DUPLICATE")
probe("M8", "delete the 'Eight things changed' banner",
      edit(DOCREL, lambda t: t.replace("Eight things changed",
                                       "Several things changed")), S2, 1,
      grep=r"banner")
probe("M9", "rename the heading '### 14.2' to '### 14.5'",
      edit(DOCREL, lambda t: t.replace("### 14.2", "### 14.5")), S2, 1,
      grep=r"REFERS TO NOTHING|DANGLING|NOT RESOLVED")

LONG_Q = None
SHORT_Q = None
_doc = open(os.path.join(REPO, DOCREL), encoding="utf-8").read()
_lines = _doc.splitlines()
LONG_Q = "\n".join(_lines[118:137])          # lines 119-137, ~1495 chars
SHORT_Q = "\n".join(_lines[471:473])         # lines 472-473, ~139 chars

probe("M17", "an EXACT duplicate of a LONG block quote (>300 chars)",
      edit(DOCREL, lambda t: t + "\n\n" + LONG_Q + "\n"), S2, 1,
      grep=r"NEAR-DUPLICATE")
probe("M16", "an EXACT duplicate of a SHORT block quote (139 chars)",
      edit(DOCREL, lambda t: t + "\n\n" + SHORT_Q + "\n"), S2, 0,
      grep=r"worst pair")
SHORT_P = "\n".join(_lines[152:154])        # lines 153-154, a 98-char paragraph
probe("M25", "an EXACT duplicate of a SHORT prose paragraph (98 chars)",
      edit(DOCREL, lambda t: t + "\n\n" + SHORT_P + "\n"), S2, 0,
      grep=r"prose paragraphs")
print("       M16 is 100%% similar, inside the ONE document the extent says")
print("       it sweeps, and the run reports 'worst pair 5%'.  The EXTENT")
print("       paragraph names two limits -- cross-document, and paraphrase")
print("       below 45%% -- and neither is this one.")
print()

# ---------------------------------------------------------------------------
hdr("D5i  X8 -- THE ELEVENTH STRIKE, ON NO LIST")
probe("M14a", "un-strike §1's 'three independent agreements'",
      edit(DOCREL, lambda t: t.replace(
          "~~as three independent agreements about the term~~",
          "as three independent agreements about the term")), CD, 0,
      grep=r"CHECK_DOC:")
probe("M14b", "the same mutation", edit(DOCREL, lambda t: t.replace(
    "~~as three independent agreements about the term~~",
    "as three independent agreements about the term")), S1, 0,
    grep=r"TOTAL BAD")
probe("M14c", "the same mutation", edit(DOCREL, lambda t: t.replace(
    "~~as three independent agreements about the term~~",
    "as three independent agreements about the term")), S2, 0,
    grep=r"TOTAL BAD")
probe("M15a", "X8 asserted unmarked in code/species_7d75",
      plant("code/species_7d75/NOTE.md", X8_SENTENCE), S1, 0)
probe("M15b", "the same, against mg-73df's own c4_scope.py",
      plant("code/species_7d75/NOTE.md", X8_SENTENCE), C4, 1,
      grep=r"X8|STILL ASSERTED")
print("       A statement the document withdrew, restored to live prose, and")
print("       every checker in the arc reports clean -- except the one whose")
print("       list carries it, which is the one this repair did not union.")
print()

# ---------------------------------------------------------------------------
hdr("D5j  THE DELETED BOX PUT BACK, AND w3_scope.py AIMED AT BOTH HISTORIES")

_box = at("ebecd89", DOCREL)
if _box is not None:
    _lines = _box.splitlines()
    DUP = "\n".join(_lines[1009:1019])       # lines 1010-1019, the deleted copy
    probe("M7", "re-insert ONLY the deleted duplicate box into §14",
          edit(DOCREL, lambda t: t.replace(
              "### 14.1 The correction ran in BOTH directions",
              DUP + "\n\n### 14.1 The correction ran in BOTH directions")),
          S2, 1, grep=r"NEAR-DUPLICATE")
else:
    print("  M7   git unavailable -- NOT RUN, and this line is the record")

hdr("     w3_scope.py against the two trees its own docstring cites")
for tag, commit, pred in [("M23", "83ac472", 1), ("M24", "ebecd89", 0)]:
    tmp = tempfile.mkdtemp(prefix="a7dd3_")
    try:
        tar = subprocess.run(["git", "archive", commit, "code/species_7d75"],
                             cwd=REPO, capture_output=True)
        if tar.returncode != 0:
            print("  %-4s git unavailable -- NOT RUN" % tag)
            continue
        subprocess.run(["tar", "-x", "-C", tmp], input=tar.stdout, check=True)
        d = os.path.join(REPO, "code", "species_remainder_f8fa")
        r = subprocess.run([sys.executable, "w3_scope.py",
                            os.path.join(tmp, "code", "species_7d75")],
                           cwd=d, capture_output=True, text=True)
        missed.append(r.returncode != pred)
        results.append((tag, r.returncode, pred, r.returncode == pred))
        print("  %-4s w3_scope.py against the tree at %-9s exit %d, "
              "predicted %d  %s"
              % (tag, commit, r.returncode, pred,
                 "ok" if r.returncode == pred else "*** PREDICTION MISSED ***"))
        for line in r.stdout.splitlines():
            if re.search(r"W3 SCOPE:", line):
                print("           | %s" % line.strip())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
print("       M23 is the exit-code fix mg-a4ef disclosed beyond mg-73df's")
print("       five, measured: 12 problems and a nonzero exit.  M24 is")
print("       mg-73df's control (b) -- w3_scope PASSES the tree its own")
print("       MAJOR was found in.")
print()

# ---------------------------------------------------------------------------
print("=" * 78)
print("D5 PREDICTIONS MISSED: %d of %d" % (sum(missed), len(missed)))
print("=" * 78)
for tag, code, pred, ok in results:
    if not ok:
        print("    MISSED  %-6s exit %d, predicted %d" % (tag, code, pred))
print()
print("EXTENT OF THIS NUMBER.  D5 runs %d mutations against 5 checkers in a"
      % len(results))
print("scratch copy of docs/ and 5 code trees.  It probes the boundary of")
print("each checker's PRINTED extent in both directions and nothing else: it")
print("does not test the mathematics, does not mutate the code trees'")
print("algorithms, and cannot show that a checker is right -- only where it")
print("stops.  A mutation this file does not contain is a boundary nobody")
print("has probed.")
sys.exit(1 if sum(missed) else 0)
