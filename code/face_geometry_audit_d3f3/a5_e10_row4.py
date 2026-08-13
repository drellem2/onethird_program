#!/usr/bin/env python3
"""mg-d3f3 a5 -- THE ONE PREDICTION mg-8af0 SCORED WITHOUT RUNNING IT.

mg-8af0's `PREDICTIONS.md` E10 is a table of five exit codes, and the README
scores the whole table **"HIT, 5/5"**.  Four of the five have a committed
artefact behind them.  The fourth does not:

    | `verify_e35b.py` **repaired**, against the **pre-repair** artifact | **1** |

Nothing in the repository builds that world.  `run_all.sh` runs the repaired
verifier against the repaired tree; `demo_f2_row_can_go_red.py` mutates copies of
`controls.py`; and the transcripts committed at all three of mg-8af0's repair
commits report **0 refuted** (a4.4).  So "5/5" is four measurements and one
assertion, in a scoring table whose entire purpose is to separate those.

THIS FILE BUILDS THE MISSING WORLD, from git, and scores the row.

    W  code/face_geometry/ AT `5f542f0` -- mg-e35b's tree, before any of
       mg-8af0 -- with `verify_e35b.py` AT `66130f8`, the last commit of
       mg-8af0.  That is "the repaired verifier against the pre-repair
       artifact", built from the two commits the prediction is about rather than
       from today's tree, which has moved twice since (mg-36f5, mg-843d).

WHY IT IS WORTH BUILDING RATHER THAN JUST NOTING.  A row scored HIT without
being run is a defect whichever way the run comes out, but the two outcomes are
different findings: if it exits 1 the claim is TRUE-AND-UNEVIDENCED, and if it
exits 0 the scoring table contains a false cell.  Guessing which would be doing
the same thing the row did.

Exit 0 iff the world builds and the row is scored either way.  a5.3 records the
outcome; it does not require a particular one.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

import lib_d3f3 as L

REPO = os.path.normpath(os.path.join(L.CODE, ".."))
PRE = "5f542f0"      # mg-e35b, before mg-8af0
POST = "66130f8"     # mg-8af0's last repair commit (F3), rebased onto main


def git(*args):
    p = subprocess.run(["git", "-C", REPO] + list(args),
                       capture_output=True, text=True)
    return p.stdout, p.returncode


def ls(rev, path):
    out, _ = git("ls-tree", "--name-only", "%s:%s" % (rev, path))
    return [x for x in out.split("\n") if x]


def build(root, rev_probe, rev_verify):
    """code/face_geometry/ at one commit, code/face_geometry_repair_e35b/ at another."""
    for rev, sub in ((rev_probe, "face_geometry"),
                     (rev_verify, "face_geometry_repair_e35b")):
        d = os.path.join(root, sub)
        os.makedirs(d)
        for f in ls(rev, "code/" + sub):
            if not f.endswith((".py", ".txt", ".sh")):
                continue
            blob, _ = git("show", "%s:code/%s/%s" % (rev, sub, f))
            open(os.path.join(d, f), "w").write(blob)
    return root


def run_verifier(root):
    p = subprocess.run([sys.executable, "verify_e35b.py"],
                       cwd=os.path.join(root, "face_geometry_repair_e35b"),
                       capture_output=True, text=True)
    rows = {}
    for line in p.stdout.splitlines():
        m = re.match(r"^\s*\[(PASS|FAIL)\]\s+(.*)$", line)
        if m:
            rows[m.group(2)] = m.group(1) == "PASS"
    return p.returncode, rows, p.stdout + p.stderr


def main():
    R = L.Report("mg-d3f3 a5 -- E10's fourth row, built and scored")

    # -- a5.1: the row is claimed, and nothing runs it --------------------
    pred = " ".join(open(os.path.join(L.EIGHT, "PREDICTIONS.md")).read().split())
    readme = " ".join(open(os.path.join(L.EIGHT, "README.md")).read().split())
    row4 = ("| `verify_e35b.py` **repaired**, against the **pre-repair** "
            "artifact | **1** |")
    scored = "| E10 | five exit codes | **HIT, 5/5** |"
    R.check("a5.1 THE ROW AND ITS SCORE BOTH EXIST, verbatim: E10 predicts exit "
            "1 for the repaired verifier against the pre-repair artifact, and "
            "the README scores the table HIT, 5/5",
            row4 in pred and scored in readme,
            "row present: %s; score present: %s"
            % (row4 in pred, scored in readme))

    builders = []
    for d in (L.REPAIR, L.EIGHT, L.PROBE):
        for f in sorted(os.listdir(d)):
            if f.endswith((".py", ".sh")):
                s = open(os.path.join(d, f)).read()
                if PRE in s or "git show" in s or "git -C" in s:
                    builders.append(f)
    R.check("a5.2 AND NOTHING IN THE REPAIR BUILDS THAT WORLD.  No artefact "
            "under face_geometry/, _repair_e35b/ or _repair_8af0/ reads a blob "
            "out of git or names the pre-repair commit as an input; the one "
            "file that mentions %s does so in a comment about TRANSCRIBING the "
            "old condition, not about running against the old tree.  So the "
            "cell is scored HIT with no run behind it" % PRE,
            builders == ["demo_f2_row_can_go_red.py"],
            "artefacts naming %s or shelling to git: %s" % (PRE, builders))
    R.count("cells of E10 with a committed artefact behind them", 4,
            "COULD MOVE",
            "run_all.sh's two exit codes, mg-e35b's own committed transcript, "
            "and out_demo_f2.txt; a fifth artefact would move it to 5, which is "
            "what this file recommends and does not perform")

    # -- a5.3: build the world and score the row -------------------------
    print()
    root = tempfile.mkdtemp(prefix="mgd3f3-e10-")
    try:
        build(root, PRE, POST)
        code, rows, out = run_verifier(root)
        red = sorted(k for k, v in rows.items() if not v)
        tail = out.strip().splitlines()[-1] if out.strip() else "(no output)"
        R.check("a5.3 THE WORLD BUILDS AND THE ROW IS SCORED: face_geometry/ at "
                "%s with verify_e35b.py at %s exits %d.  E10 predicted 1.  The "
                "row is therefore %s -- and it was TRUE-BY-CONSTRUCTION rather "
                "than measured, which is the finding either way"
                % (PRE, POST, code, "a HIT" if code == 1 else "a MISS"),
                code in (0, 1),
                "exit %d; %d rows red: %s; last line %r"
                % (code, len(red), [r[:44] for r in red] or "none", tail))
        R.count("exit code of E10's fourth world, measured here for the first "
                "time", code, "COULD MOVE",
                "it is a property of two commits and it is what E10 bet on; a "
                "repaired verifier that did not classify the F1 count would "
                "print 0")
        print()
        print("    the rows that fire in E10's fourth world, in full:")
        for r in red:
            print("      RED  %s" % r[:150])
        if not red:
            print("      (none)")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    # -- a5.4: the row is AMBIGUOUS, so all three readings are built ------
    print()
    print("    \"the pre-repair artifact\" has three available readings and the "
          "row does not")
    print("    pick one, so each is built rather than argued:")
    root = tempfile.mkdtemp(prefix="mgd3f3-e10b-")
    try:
        build(root, POST, POST)
        blob, _ = git("show", "%s:code/face_geometry/controls_output.txt" % PRE)
        open(os.path.join(root, "face_geometry", "controls_output.txt"),
             "w").write(blob)
        code_b, rows_b, _ = run_verifier(root)
        red_b = sorted(k for k, v in rows_b.items() if not v)
    finally:
        shutil.rmtree(root, ignore_errors=True)

    tx, _ = git("show",
                "0c3a2ba:code/face_geometry_repair_e35b/out_verify_e35b.txt")
    code_c = 0 if "0 refuted" in tx else 1

    readings = [
        ("R-a  the whole pre-repair TREE, repaired verifier", code, 1),
        ("R-b  the repaired tree with a STALE artifact from %s" % PRE, code_b, 1),
        ("R-c  the real tree at the F2 commit (a4.4's transcript)", code_c, 1),
    ]
    print()
    print("      %-58s %-8s %s" % ("reading", "measured", "E10 said"))
    for name, got, want in readings:
        print("      %-58s %-8d %d   %s" % (name, got, want,
                                            "HIT" if got == want else "MISS"))
    hits = sum(1 for _, g, w in readings if g == w)
    R.check("a5.4 E10's FOURTH ROW IS A HIT UNDER %d OF THE 3 READINGS AND A "
            "MISS UNDER %d, and nothing in the repository picks the reading or "
            "runs any of them.  The one that comes out 1 is the STALE-ARTIFACT "
            "reading, where V6c fires -- and V6c is a row about staleness, not "
            "about F1.  Under the two readings that are about F1 the answer is "
            "0" % (hits, 3 - hits),
            hits == 1,
            "R-b's red rows: %s" % ([r[:44] for r in red_b] or "none"))
    R.count("readings of E10 row 4 under which it is a HIT", hits, "COULD MOVE",
            "a fourth reading, or a repair that made the F1 defect visible, "
            "would move it")

    print()
    R.note("AND THE SHARPEST FORM OF a1, WHICH FALLS OUT OF R-a: mg-8af0's "
           "COMPLETE repaired verifier, run against the tree AS IT WAS BEFORE "
           "mg-8af0 TOUCHED IT, reports 28 checks and 0 refuted.  The "
           "instrument does not separate the repaired tree from the unrepaired "
           "one.  Every difference the repair made is in prose, in the operand "
           "of one `%` expression, and in the verifier's own TABLE -- and none "
           "of those three is a thing any row of the verifier reads.")

    R.note("WHAT THIS DOES NOT SAY.  It does not say the prediction was wrong "
           "to be believed -- it is the kind of claim a careful author can be "
           "confident of from reading.  It says a table headed with the word "
           "SCORED contains one cell that was reasoned to and four that were "
           "run, and does not distinguish them.  mg-8af0 draws exactly that "
           "distinction elsewhere, repeatedly and at its own expense (the E6a "
           "miss, the E9 half-miss, R0-style disclosure of paper derivations), "
           "which is why the one place it does not is worth a row.")
    return R.finish()


if __name__ == "__main__":
    sys.exit(main())
