"""mg-f1b2 -- part 5.  The battery at its other supported populations.

`controls.py` takes nmax on the command line (`main()`: nmax_cheap = sys.argv[1]),
and run_all.sh calls it with 5.  mg-8a12's merge note records that "n<=3 and n<=4
also run clean".  n<=2 is the population it does not mention, and it is where the
routing check's answer flips -- which is the point: the row is a statement about
the population, not about the construction.
"""

import os
import re
import subprocess
import sys

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "face_geometry")


def run(nmax):
    p = subprocess.run([sys.executable, "controls.py", str(nmax)], cwd=SRC_DIR,
                       capture_output=True, text=True)
    return p.stdout, p.returncode


def main():
    print("=" * 78)
    print("mg-f1b2 part 5 -- the two rows mg-8a12 adds, at every supported nmax")
    print("=" * 78)
    for nmax in (2, 3, 4, 5):
        out, rc = run(nmax)
        rout = [l for l in out.splitlines()
                if "routing check" in l and l.startswith("  [")]
        thm = [l for l in out.splitlines()
               if "PROVEN PROPERTY" in l and l.startswith("  [")]
        print("\n  ---- python3 controls.py %d   (exit %d) ----" % (nmax, rc))
        for l in rout:
            m = re.match(r"  \[([A-Z ]+)\] .*?-- (\d+) of the (\d+) rows", l)
            print("    routing check: [%s]  %s of %s rows forced"
                  % (m.group(1), m.group(2), m.group(3)) if m else "    " + l[:120])
        for l in thm:
            st = re.match(r"  \[([A-Z ]+)\]", l).group(1)
            names = re.search(r"the corruptions ([^ ]+(?:, [^ ]+)*) are NOT", l)
            fall = "I4 moves one, though no closed form" in l
            print("    theorem row:   [%s]  covers %s%s"
                  % (st, names.group(1) if names else "?",
                     "   <-- and PRINTS 'I4 moves one, though no closed form for it "
                     "is recorded in DIAGONAL_MOVES'" if fall else ""))
        bad = [l for l in out.splitlines() if l.startswith("CONTROLS FAILED")]
        if bad:
            print("    %s" % bad[0])
    print()
    print("  READING.  At n <= 2 the routing check FAILS (4 of 4 forced) and the "
          "theorem row prints\n  'I4 moves one' -- an assertion that the off-by-one "
          "moves a diagonal entry, which the same\n  file measures as FALSE on 3 "
          "posets at n >= 3 (diagonal preserved).  The row's guard is\n  "
          "`theorem_absorb == 0 and theorem_diag == theorem_app`, an aggregate over "
          "the posets where\n  the mutation applies; at n <= 2 the off-by-one "
          "applies nowhere, so 0 == 0 and the guard\n  cannot see the false "
          "sentence it prints.  'A FALSE theorem is still a failure' does not "
          "hold\n  for the per-row half of what the row asserts.")


if __name__ == "__main__":
    main()
