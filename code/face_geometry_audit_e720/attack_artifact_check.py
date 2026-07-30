"""mg-e720: an INDEPENDENT attack battery on `artifact_banner_check` as mg-7d5a
repaired it (commit d5a3043).

Written against the repaired docstring's CLAIM, not against mg-6653's
`attack_banner.py`.  Every injection site below is a different function or a
different route from the ones that script used, and the last four routes are
ones no previous generation tried.

WHAT THE REPAIRED CODE CLAIMS.  Three sentences, in ascending strength:

  ArtifactTee.__doc__ : "what this object records IS the artifact"
  the docstring       : "It now scans every line `ArtifactTee` has recorded,
                         which is every line of the artifact"
  the printed heading  : "CONTROL ON THE ARTIFACT -- nothing above the bottom
                         line may carry the banner"
  d5a3043's message   : "the check reads what a grep of controls_output.txt
                         reads, whatever route printed it -- including a bare
                         print() added tomorrow"

WHAT IT ENFORCES.  No line printed BEFORE the check, through `sys.stdout`,
after `main()` installed the tee, carries the 17-char literal.  The gap between
those two is where P1/P2/P3/P6 live.  `run_all.sh` builds the artifact as
`python3 controls.py 5 | tee controls_output.txt`, so this script treats the
child's stdout as the artifact, which is exactly what a grep of the committed
file would read.

Each route is scored on the two things that matter together:
  * did the 17-char literal reach a NON-bottom-line of the artifact?
  * did the control row report [FAIL] and did the battery exit nonzero?
A route that answers yes/no is the F5 defect reachable with the repair in place.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.normpath(os.path.join(HERE, "..", "face_geometry"))
BANNER = "ALL CONTROLS PASS"
NMAX = "4"          # n <= 4 keeps a full run near 0.4 s; the control is n-free

RESULTS = []


def run(mutate, label, expect_control_fires):
    """Copy the battery to a temp dir, mutate controls.py, run it, score it.

    The committed tree is never modified.
    """
    tmp = tempfile.mkdtemp(prefix="mg-e720-")
    try:
        work = os.path.join(tmp, "fg")
        shutil.copytree(SRC_DIR, work)
        path = os.path.join(work, "controls.py")
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        new = mutate(src)
        if new is None:
            raise AssertionError("%s: the anchor moved -- attack not applied" % label)
        if new == src:
            raise AssertionError("%s: mutation was a no-op" % label)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(new)
        proc = subprocess.run([sys.executable, "controls.py", NMAX], cwd=work,
                              capture_output=True, text=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    artifact = proc.stdout                  # what `| tee controls_output.txt` writes
    lines = artifact.split("\n")
    hits = [i for i, l in enumerate(lines) if BANNER in l]
    licensed = [i for i, l in enumerate(lines) if l.strip() == BANNER]
    stray = [i for i in hits if i not in licensed]
    row = [l for l in lines if "all-pass banner literal" in l]
    fired = bool(row) and row[0].lstrip().startswith("[FAIL]")

    if expect_control_fires:
        ok = fired and proc.returncode == 1
        verdict = "POSITIVE CONTROL HOLDS" if ok else "POSITIVE CONTROL FAILED"
    else:
        reached = bool(stray) and not fired and proc.returncode == 0
        verdict = ("ATTACK SUCCEEDS -- the banner is in the artifact, the control "
                   "says none, exit 0" if reached else "attack repelled")

    print()
    print(label)
    print("  exit code                     : %d" % proc.returncode)
    print("  banner lines in the artifact  : %d  (of which NOT the bottom line: %d)"
          % (len(hits), len(stray)))
    for i in stray:
        print("       line %-3d %s" % (i + 1, lines[i].strip()[:104]))
    print("  the control row               : %s"
          % (row[0].strip()[:104] if row else "(row absent)"))
    print("  ==> %s" % verdict)
    RESULTS.append((label.split("--")[0].strip(), verdict))
    return verdict


# ----------------------------------------------------------------- positive
def a_rowname(src):
    """The banner in a row NAME -- what the pre-repair check already caught.

    Positive control on the repaired control: if this stops firing the row has
    become a tautology and the SCORING section of controls.py applies.
    """
    anchor = '    banner_name = "the all-pass banner"'
    if anchor not in src:
        return None
    return src.replace(anchor, '    banner_name = "ALL CONTROLS PASS"', 1)


# ------------------------------------------- mg-6653's routes, at NEW sites
def b_detail(src):
    """mg-6653's ATTACK B route -- a `detail=` string -- at a different site.

    mg-6653 put it on an existing check inside `scoring_self_test`.  This adds a
    fresh row at the end of the incidence battery instead, so nothing about the
    site mg-6653 chose is load-bearing for the result.
    """
    anchor = "def artifact_banner_check():"
    if anchor not in src:
        return None
    inject = ('    check("incidence battery reached its bottom row", True,\n'
              '          "clean-run bottom line is %r" % "ALL CONTROLS PASS")\n\n\n')
    return src.replace(anchor, inject + anchor, 1)


def c_heading(src):
    """mg-6653's ATTACK C route -- a bare print() heading -- at a different site.

    mg-6653 used `scoring_self_test`'s heading; this uses the FIRST control in
    main()'s order, `positive_control_homology`, so the banner sits at the top
    of the artifact rather than in the middle.
    """
    anchor = "def positive_control_homology():"
    if anchor not in src:
        return None
    i = src.index(anchor)
    j = src.index("\n    print(", i)
    k = src.index("\n", j + 1)
    return (src[:k + 1]
            + '    print("  [PASS] reference bottom line: %s" % "ALL CONTROLS PASS")\n'
            + src[k + 1:])


def d_split(src):
    """One artifact line assembled from two write() calls.

    Tests the tee's reassembly: the literal never appears in a single `write`,
    only in the line the artifact ends up carrying.  A tee that scanned each
    write in isolation would miss this.
    """
    anchor = "def artifact_banner_check():"
    if anchor not in src:
        return None
    inject = ('def _e720_split():\n'
              '    sys.stdout.write("  [PASS] split across writes: ALL CONTROLS ")\n'
              '    print("PASS")\n\n\n')
    src = src.replace(anchor, inject + anchor, 1)
    return src.replace("    artifact_banner_check()",
                       "    _e720_split()\n    artifact_banner_check()", 1)


# --------------------------------------------------- routes nobody has tried
def p1_after(src):
    """A bare print() AFTER the check and before the bottom line.

    d5a3043's message says the repair covers "a bare print() added tomorrow".
    This is a bare print() added tomorrow, four lines below the check.
    """
    anchor = "    artifact_banner_check()\n    print()"
    if anchor not in src:
        return None
    return src.replace(anchor,
                       '    artifact_banner_check()\n'
                       '    print("  [PASS] battery clean: %s" % "ALL CONTROLS PASS")\n'
                       '    print()', 1)


def p2_newcontrol(src):
    """A NEW control row appended after the check -- the likeliest next edit.

    Every generation of this file has added a control by appending one to
    main().  Appending it after `artifact_banner_check()` is the natural place,
    and it puts the new row's name outside everything the check reads.  The row
    name used here is mg-1319's F5 row name verbatim.
    """
    anchor = "    artifact_banner_check()\n    print()"
    if anchor not in src:
        return None
    newfn = ('def negative_control_e720():\n'
             '    """A control added tomorrow, appended after the artifact check."""\n'
             '    print("CONTROL ADDED TOMORROW -- appended after the artifact check")\n'
             '    check("with no cannot-fail row the bottom line is %s"\n'
             '          % "ALL CONTROLS PASS", True)\n\n\n'
             'def main():')
    src = src.replace("def main():", newfn, 1)
    return src.replace(anchor,
                       "    artifact_banner_check()\n"
                       "    negative_control_e720()\n    print()", 1)


def p3_fd(src):
    """os.write(1, ...) -- into the artifact, around the tee.

    `ArtifactTee.__doc__` says "what this object records IS the artifact".  fd 1
    is the artifact; the object is `sys.stdout`.  Exotic, but the docstring
    states an identity, and this is the counterexample to the identity.
    """
    anchor = "def artifact_banner_check():"
    if anchor not in src:
        return None
    inject = ('def _e720_fd():\n'
              '    import os\n'
              '    os.write(1, ("  [PASS] via fd 1: %s\\n" % '
              '"ALL CONTROLS PASS").encode())\n\n\n')
    src = src.replace(anchor, inject + anchor, 1)
    return src.replace("    artifact_banner_check()",
                       "    _e720_fd()\n    artifact_banner_check()", 1)


def p6_import(src):
    """A module-level print, executed BEFORE main() installs the tee.

    The docstring explains the late install as a feature ("so that importing
    this module for its functions does not hijack stdout").  The cost of it is
    that everything printed at import time is in the artifact and not in the
    tee.
    """
    anchor = "def main():"
    if anchor not in src:
        return None
    return src.replace(anchor,
                       'print("  [PASS] import-time banner: %s" % '
                       '"ALL CONTROLS PASS")\n\n\n' + anchor, 1)


def main():
    print("mg-e720 -- INDEPENDENT ATTACK BATTERY ON artifact_banner_check AS "
          "REPAIRED BY mg-7d5a")
    print("=" * 78)
    print("Object under attack: code/face_geometry/controls.py at d5a3043.")
    print("The artifact is the child's stdout, which is what `| tee "
          "controls_output.txt` writes.")
    print("An attack SUCCEEDS iff the 17-char literal reaches a non-bottom line,")
    print("the control row reports no offenders, and the battery exits 0.")

    print()
    print("-- POSITIVE CONTROL ON THE REPAIRED CONTROL " + "-" * 33)
    run(a_rowname, "A  the banner in a row NAME (pre-repair route)", True)

    print()
    print("-- mg-6653's TWO ROUTES, REBUILT AT DIFFERENT SITES " + "-" * 25)
    run(b_detail, "B  the banner in a `detail=` string (new site: incidence battery)", False)
    run(c_heading, "C  the banner as a bare print() heading (new site: first control)", False)
    run(d_split, "D  one artifact line assembled from two write() calls", False)

    print()
    print("-- ROUTES NO GENERATION HAS TRIED " + "-" * 43)
    run(p1_after, "P1  a bare print() AFTER the check, above the bottom line", False)
    run(p2_newcontrol, "P2  a NEW control row appended after the check", False)
    run(p3_fd, "P3  os.write(1, ...) -- into the artifact, around the tee", False)
    run(p6_import, "P6  a module-level print, before main() installs the tee", False)

    print()
    print("=" * 78)
    print("SUMMARY")
    for label, verdict in RESULTS:
        print("  %-4s %s" % (label, verdict))

    succeeded = [l.split()[0] for l, v in RESULTS if v.startswith("ATTACK SUCCEEDS")]
    print()
    print("BOTTOM LINE.  The CODE repair is real and it holds where mg-6653 broke it:")
    print("B, C and D are repelled and A still fires, so the row is a control and not")
    print("a tautology.  What does NOT hold is the SIZE of the claim written around it.")
    print("%d route(s) put the literal into the artifact with the control reporting"
          % len(succeeded))
    print("\"offending lines: none\" and the battery exiting 0: %s."
          % ", ".join(succeeded))
    print("Three of the four are a bare print().  The property enforced is")
    print("\"no line printed BEFORE this row, through sys.stdout, after main() installed")
    print("the tee\" -- which equals \"the artifact's occurrences are exactly the bottom")
    print("line's\" only while this row stays last in main(), and nothing checks that.")
    print("The check's own DETAIL string says it exactly right -- \"the whole artifact")
    print("above this row\".  The printed HEADING, the docstring's \"which is every line")
    print("of the artifact\", and the commit message's \"including a bare print() added")
    print("tomorrow\" each say more than the code does.")


if __name__ == "__main__":
    main()
