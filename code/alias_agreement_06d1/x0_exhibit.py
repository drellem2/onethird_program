"""x0 — THE EXHIBIT.  One perturbed tree, and the merge gate going RED because of it.

STEP 4 OF THE TICKET, AND IT IS NOT OPTIONAL: "perturb one tree's value and show the gate
goes RED naming both aliases.  Without it this is a check that has only ever seen
agreement, which is the exact condition mg-9876 was filed about."

g1's eight planted worlds falsify the CHECK — they mutate the captured value matrix, which
is the right way to falsify a comparison cheaply and the reason the whole falsification
suite costs 0.55 s instead of four minutes.  What they do NOT establish is that a real edit
to a real library, made by a real author, reaches that comparison at all.  Between a
tree's source and g1's verdict sit lib0d1b's adapter, the module loader, run_all.sh's exit
capture, build.sh's worst-exit loop and the refinery's gate invocation, and mg-724a's
exhibit found a probe that could not fire only by RUNNING it end to end.  So this runs the
real command against a real edit.

WHAT IS PLANTED.  `code/sweep_loss_51f4/lib51f4.py`'s `E_footrule` gains `+ 1/10^9`.  That
is a one-line, one-term change to an exact rational return value, in one of the four trees
that compute the footrule, and the `E_footrule` row of INDEX.md is pinned at tolerance
0.000e+00 — so the gate must name `sweep_loss_51f4:E_footrule` and one of the other three.

THE FILE IS RESTORED BYTE-IDENTICALLY UNDER A CHECKED DIGEST, in a finally block, and the
restore is verified against git as well as against the digest.  mg-724a's D5 was that its
gate left four tracked files modified in two directories that were not its own; this
exhibit edits a directory that is not mine and must not be the same finding twice.
"""

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
TARGET = os.path.join(REPO, "code", "sweep_loss_51f4", "lib51f4.py")

BEFORE = '        self._m["DF"] = F(tot, N)\n'
AFTER = '        self._m["DF"] = F(tot, N) + F(1, 10 ** 9)\n'

ALIASES = ["sweep_loss_51f4:E_footrule", "direct_prefix_audit_2de0:E_footrule",
           "l2_audit_29fe:EDF", "l2_conditionality_28ff:E_footrule"]


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def build():
    """Run the REAL gate command — ./build.sh, what .pogo/refinery.toml names."""
    p = subprocess.run(["sh", "build.sh"], cwd=REPO, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def banner(s):
    print()
    print("=" * 78)
    print(s)
    print("=" * 78)


def main():
    print("x0  THE EXHIBIT — a real edit to a real tree, and the real gate command")
    print()
    print("  target   %s" % os.path.relpath(TARGET, REPO))
    digest0 = sha(TARGET)
    print("  sha256   %s  (before)" % digest0)

    with open(TARGET) as fh:
        src = fh.read()
    if src.count(BEFORE) != 1:
        print("\n  REFUSED — the anchor line appears %d times, not once.  The exhibit "
              "will not guess where to plant." % src.count(BEFORE))
        return 2

    banner("E0  THE GATE ON THE UNMODIFIED TREE — scored FIRST")
    rc0, out0 = build()
    print("  ./build.sh  exit %d" % rc0)
    for line in out0.splitlines():
        if "alias-agreement worst exit" in line or "worst suite exit" in line:
            print("    %s" % line.strip())
    if rc0 != 0:
        print("""
  REFUSED — the gate is ALREADY RED before anything was planted, so nothing below could
  distinguish a catch from the standing state.  mg-9876's guard: a probe satisfied by the
  good input is UNFALSIFIABLE and is never CAUGHT.""")
        return 2

    banner("E1  PLANT — E_footrule gains 1/10^9 in ONE of the four trees that compute it")
    ok = False
    try:
        with open(TARGET, "w") as fh:
            fh.write(src.replace(BEFORE, AFTER))
        print("  planted:  %s" % AFTER.strip())
        print("  sha256    %s  (planted)" % sha(TARGET))

        banner("E2  THE GATE ON THE PLANTED TREE")
        rc1, out1 = build()
        print("  ./build.sh  exit %d" % rc1)
        # The finding itself, not every line in the corpus that contains the word
        # "spread": take the contiguous block the alias suite prints for a RED group.
        #
        # mg-479c: THIS WAS A FIXED `lines[i:i+4]` AND MY OWN CHANGE MADE THE BLOCK LONGER.
        # The RED message now carries the declared conventions and factors, so a four-line
        # window cuts it off mid-sentence — an exhibit whose job is to show what the gate
        # said, showing part of it.  That is D3 of README §5 arriving a second time through
        # a different door, so the window is no longer a count: it takes the RED line and
        # every CONTINUATION line under it, and stops at the next line that is not one.
        lines = out1.splitlines()
        blk = []
        for i, ln in enumerate(lines):
            if ln.startswith("  RED "):
                blk = [ln]
                for nxt in lines[i + 1:]:
                    if not nxt.startswith("       "):
                        break
                    blk.append(nxt)
                break
        print()
        print("  the finding, as the gate printed it:")
        for ln in blk:
            print("    %s" % ln.rstrip())

        named = [a for a in ALIASES if a.replace(":", ":") in out1]
        print()
        print("  exit non-zero                      : %s" % (rc1 != 0))
        print("  names the perturbed alias          : %s" % (ALIASES[0] in out1))
        print("  names at least one OTHER alias     : %s"
              % (len([a for a in named if a != ALIASES[0]]) >= 1))
        print("  aliases named in the gate output   : %s" % ", ".join(named))
        ok = (rc1 != 0 and ALIASES[0] in out1
              and len([a for a in named if a != ALIASES[0]]) >= 1)
    finally:
        banner("E3  RESTORE — byte-identically, under a checked digest")
        with open(TARGET, "w") as fh:
            fh.write(src)
        digest1 = sha(TARGET)
        print("  sha256   %s  (after restore)" % digest1)
        print("  identical to before                : %s" % (digest0 == digest1))
        g = subprocess.run(["git", "diff", "--quiet", "--", TARGET], cwd=REPO)
        print("  git reports the file unmodified    : %s" % (g.returncode == 0))
        if digest0 != digest1 or g.returncode != 0:
            print("  RESTORE FAILED — do not commit; the planted edit is still in the tree.")
            return 2

    banner("x0 RESULT")
    if ok:
        print("  CAUGHT.  A one-term edit to one of four trees computing the footrule made")
        print("  `./build.sh` — the command .pogo/refinery.toml names — exit non-zero and")
        print("  name both aliases.  The tree is restored byte-identically.")
        return 0
    print("  MISSED.  The planted disagreement did not reach the gate's verdict.")
    return 1


TRANSCRIPT = os.path.join(HERE, "out_x0_exhibit.txt")


def run_and_transcribe():
    """Run, then write `out_x0_exhibit.txt` — LAST, and by this script rather than by a
    shell redirect.

    mg-479c.  THIS SCRIPT WAS PREVIOUSLY INVOKED AS `python3 x0_exhibit.py > out_x0...txt`
    AND THAT NO LONGER WORKS, for a reason that did not exist when it was written.  This
    exhibit runs `./build.sh`, and `./build.sh` now ends with mg-f771's control, which
    compares every tracked `code/**/out_*.txt` against its committed copy.  Under a shell
    redirect, `out_x0_exhibit.txt` is TRUNCATED AND HALF-WRITTEN at the moment f771 reads
    it, so f771 grades the exhibit's own transcript DISAGREES, the gate exits 1, and E0
    refuses with "the gate is ALREADY RED before anything was planted" — on every run,
    forever.  The refusal is CORRECT (the gate really was red) and its cause is this
    invocation.

    So the output is buffered and the file is written after the last `./build.sh` has
    finished.  During the run the worktree copy is whatever is committed, which is what
    f771 needs it to be, and the exhibit stops interfering with the gate it is exhibiting.
    """
    import io
    # mg-502f.  THE REPAIR ABOVE CHANGED THE DEFAULT INVOCATION; IT DID NOT REMOVE THE OLD
    # ONE.  `python3 x0_exhibit.py > out_x0_exhibit.txt` is still published — in build.sh's
    # own mg-479c block, three paragraphs of it, and in mg-502f's ticket body — and typing
    # it truncates this file at the moment the shell opens the redirect, whether or not
    # this function later rewrites it.  So the invocation is REFUSED rather than left to be
    # re-typed.  mg-502f swept the estate for the class and found this file and one other.
    sys.path.insert(0, os.path.join(REPO, "code", "self_red_sweep_502f"))
    import guard_502f
    guard_502f.refuse_if_self_red("x0_exhibit.py")

    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        rc = main()
    finally:
        sys.stdout = real
    text = buf.getvalue()
    real.write(text)
    with open(TRANSCRIPT, "w") as fh:
        fh.write(text)
    return rc


if __name__ == "__main__":
    sys.exit(run_and_transcribe())
