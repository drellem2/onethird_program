"""x1 — THE WRONG WAY, RUN RATHER THAN ARGUED.  The pre-479c gate, on a legitimate pair.

NOT RUN BY THE GATE.  It needs the 30 s capture and it needs `git`, and neither belongs on
a merge gate that already costs 45 s.  What it establishes is the one thing g1's N3 arm
cannot establish about itself.

WHAT N3 ESTABLISHES, AND WHAT IT DOES NOT
------------------------------------------
g1's arm N3 doubles a real column, declares the factor, and shows the comparison GREEN;
beside it, the same input through `check_groups(..., normalise=False)` is RED.  That is the
FALSE RED the ticket is about — except that `normalise=False` is a flag in code I wrote, and
a demonstration that MY OWN disabled path goes red proves nothing about the gate that has
been on `build.sh` since mg-06d1 landed.  Filed in advance as E7: "showing that the
comparison with normalisation switched off goes RED on a legitimate pair proves nothing
unless that path IS the shipped pre-479c comparison."

So this script loads `libagree.py` AS IT IS ON main, BY BLOB SHA — not by path, not by
`git stash`, not by editing anything — and runs ITS `check_groups` on the same doubled
column.  mg-17aa's `demo_wrong_way.py` is the pattern; a blob-pinned reference cannot drift
when main moves and cannot be accidentally the file I am editing.

WHAT IS DOUBLED, AND WHY THAT IS A LEGITIMATE PAIR AND NOT A DEFECT
--------------------------------------------------------------------
`chain_iv_c_81ff:lambda2_bracket`, one of the nine names for `gamma`, multiplied by exactly
2 and DECLARED to be in a doubled convention with a canonical-frame tolerance recorded.
That is precisely the situation the ticket describes: "two conventions that agree modulo a
factor report as a disagreement".  The doubling is applied to the CAPTURED COLUMN and no
file in any tree is touched — unlike `x0_exhibit.py`, which edits a real library and
restores it, this script writes nothing outside its own transcript.
"""

import os
import subprocess
import sys
import tempfile
import importlib.util
from fractions import Fraction

import libagree as A
import libnorm as N

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
REL = "code/alias_agreement_06d1/libagree.py"
BASE_REF = os.environ.get("X1_BASE_REF", "main")
KEY = ("chain_iv_c_81ff", "lambda2_bracket")


def git(*args):
    return subprocess.run(["git"] + list(args), cwd=REPO, capture_output=True,
                          text=True, check=True).stdout


def load_pinned_libagree():
    """Import `libagree` as of BASE_REF, pinned BY BLOB SHA and loaded from a temp file.

    Pinned by blob rather than by ref: a ref moves, and mg-a71f's D-series is a list of
    checks that named the wrong commit because `main` had advanced under them.  The sha is
    printed, so the transcript says exactly which bytes were run.
    """
    blob = git("rev-parse", "%s:%s" % (BASE_REF, REL)).strip()
    src = git("cat-file", "blob", blob)
    tmpdir = tempfile.mkdtemp(prefix="x1_pre479c_")
    path = os.path.join(tmpdir, "libagree_pre479c.py")
    with open(path, "w") as fh:
        fh.write(src)
    # The pre-479c module resolves BASELINE.json relative to its own directory, which is now
    # a temp dir.  Point it back at the committed one rather than copying the file: a copy
    # is a second baseline and this exhibit must compare against the real expectation.
    spec = importlib.util.spec_from_file_location("libagree_pre479c", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["libagree_pre479c"] = mod
    spec.loader.exec_module(mod)
    mod.BASELINE_PATH = os.path.join(HERE, "BASELINE.json")
    return blob, mod


def main():
    L = A.L
    A.banner("x1  THE WRONG WAY — the pre-479c gate on a legitimate normalisation pair")

    blob, OLD = load_pinned_libagree()
    print()
    print("  reference:  %s:%s" % (BASE_REF, REL))
    print("  blob sha:   %s" % blob)
    print("  it returns a %d-tuple from check_groups; mg-479c's returns a 3-tuple (the "
          "third is REFUSALS)" % 2)
    if hasattr(OLD, "NORM"):
        print("\n  REFUSED — the pinned reference already imports libnorm, so it is not the "
              "pre-479c code and this exhibit would be comparing mg-479c with itself.")
        return A.BROKEN

    BL = A.load_baseline()
    POP_ALL = L.population(L.POP_SPEC)
    POP = [(n, dn) for (n, dn) in POP_ALL if L.primitive_here(dn, n)]
    NS = [n for (n, _dn) in POP]
    DECLS = N.load()

    print()
    print("  capturing %d trees over %d primitive posets ..." % (len(L.ADAPTERS), len(POP)))
    COLS, _KIND, BROKEN = A.capture(POP)
    if BROKEN:
        print("  REFUSED — trees failed to run: %s" % BROKEN)
        return A.BROKEN

    # ---- 0.  THE UNMUTATED INPUT IS SCORED FIRST, on BOTH instruments.  mg-9876's guard:
    #          a probe already satisfied by the good input is unfalsifiable, and a wrong-way
    #          demonstration whose reference is red before the mutation shows nothing.
    A.banner("x1a  THE GOOD INPUT, on both instruments")
    old_v, old_red = OLD.check_groups(COLS, {}, BL)
    new_v, new_red, new_ref = A.check_groups(COLS, {}, BL, decls=DECLS, ns=NS)
    print()
    print("  pre-479c   %d of %d groups red" % (old_red, len(old_v)))
    print("  mg-479c    %d of %d groups red, %d refusals" % (new_red, len(new_v),
                                                             len(new_ref)))
    same = all(o["spread"] == n_["spread"] for o, n_ in zip(old_v, new_v))
    print("  all twelve spreads identical between the two instruments: %s" % same)
    if old_red or new_red or new_ref or not same:
        print("\n  REFUSED — the good input is not good on one of the two instruments, so "
              "nothing below distinguishes them.")
        return A.BROKEN

    # ---- 1.  THE LEGITIMATE PAIR.
    A.banner("x1b  %s:%s DOUBLED, and DECLARED doubled" % KEY)
    doubled = A.clone(COLS)
    doubled[KEY] = [None if v is None else float(v * Fraction(2)) for v in doubled[KEY]]
    gam = [g for g in BL["groups"] if g["label"] == "gamma"][0]

    d = N.Declarations(DECLS.raw)
    d.decls = dict(DECLS.decls)
    d.tolerances = dict(DECLS.tolerances)
    d.decls["%s:%s" % KEY] = {
        "convention": "gamma (doubled convention, PLANTED by x1)",
        "factor": N.Factor([1], [2]),
        "source": "PLANTED by x1_wrongway.py — not committed"}
    d.tolerances["gamma"] = {"tolerance": gam["tolerance"],
                             "source": "PLANTED by x1_wrongway.py — not committed"}

    old_v, old_red = OLD.check_groups(doubled, {}, BL)
    print()
    print("  PRE-479c — the gate that has been on build.sh since mg-06d1 landed:")
    OLD.report(old_v, quiet=True)
    print("      %d of %d groups RED" % (old_red, len(old_v)))

    new_v, new_red, new_ref = A.check_groups(doubled, {}, BL, decls=d, ns=NS)
    print()
    print("  mg-479c — the same input, the same baseline, the declaration read:")
    A.report(new_v, quiet=True)
    gv = [v for v in new_v if v["label"] == "gamma"][0]
    print("      %d of %d groups RED, %d refusals; `gamma` spread %.3e against tolerance "
          "%.3e in the %s frame"
          % (new_red, len(new_v), len(new_ref), gv["spread"], gv["tolerance"], gv["frame"]))

    # ---- 2.  AND THE OTHER DIRECTION, so this is not a one-sided demonstration.  mg-789d's
    #          D1 was a one-sided control read as two-sided; the same doubling with NO
    #          declaration must be RED on BOTH instruments, because it is a real 2x error.
    A.banner("x1c  THE SAME DOUBLING WITH NO DECLARATION — both instruments must be RED")
    old_v2, old_red2 = OLD.check_groups(doubled, {}, BL)
    new_v2, new_red2, new_ref2 = A.check_groups(doubled, {}, BL, decls=DECLS, ns=NS)
    print()
    print("  pre-479c   %d of %d groups red" % (old_red2, len(old_v2)))
    print("  mg-479c    %d of %d groups red, %d refusals" % (new_red2, len(new_v2),
                                                             len(new_ref2)))
    for grp in new_v2:
        for kindname, _who, detail in grp["problems"]:
            if kindname == "DISAGREE":
                print()
                for line in detail.split("\n"):
                    print("      %s" % line.strip())

    A.banner("x1 RESULT")
    ok = (old_red == 1 and new_red == 0 and not new_ref
          and old_red2 == 1 and new_red2 == 1)
    print("""
  THE FALSE RED, MEASURED AGAINST THE SHIPPED CODE AND NOT AGAINST A FLAG.

    a legitimate normalisation pair   pre-479c %d red   ·   mg-479c %d red, %d refused
    a genuine 2x error                pre-479c %d red   ·   mg-479c %d red, %d refused

  The pre-479c gate gives the SAME ANSWER to both, which is the ticket in one line: "a
  factor of 2 between two live conventions and a genuine 2x error are the same signal".
  mg-479c separates them, and the RED message above names the ratio and says whether the two
  names share a convention.

  WHAT THIS DOES NOT SHOW.  It does not show that the declaration in the first case is TRUE.
  Nothing here can: a declared factor is an escape hatch and this machinery cannot close it
  (README §7).  What changed is that the factor is now written down, in a committed file,
  with a source and an author, and printed on every run.
""" % (old_red, new_red, len(new_ref), old_red2, new_red2, len(new_ref2)))
    print("  x1 %s" % ("as expected" if ok else "UNEXPECTED — read the numbers above"))
    return A.GREEN if ok else A.BROKEN


if __name__ == "__main__":
    sys.exit(main())
