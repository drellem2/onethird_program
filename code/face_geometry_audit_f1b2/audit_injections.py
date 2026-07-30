"""mg-f1b2 -- part 4.  A POSITIVE CONTROL ON mg-8a12's REPAIR.

NEGATIVE CONTROL 4 exists to cover CONSTRUCTION errors in the pipeline.  So put
construction errors into the pipeline -- into the TRUE build, the one the probe
uses -- and record which of NEGATIVE CONTROL 4's rows go red.  A row that stays
green under a construction error covers nothing there, whatever it is labelled.

This is mg-5630's line-F experiment ("is this a detection or an accident?") run
on mg-8a12's own new rows, and it is the check the repair itself did not run: the
four defects mg-8a12 injected to show its rows can fail were injected into the
SCORING (a wrong prediction, a corruption that stops biting, a predicate that
reports absorbable, every row forced), not into the CONSTRUCTION the section is
for.

The repository is never touched: face_geometry is copied into a temporary
directory and the copy is patched.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile

SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "face_geometry")

DEFECTS = [
    ("D0 no defect (control)", None, None),
    ("D1 the pipeline's ridge enumeration is incomplete: one interior ridge is\n"
     "     dropped from the TRUE build (the defect row I3 is named for)",
     '    if incidence_mode == "true":\n'
     '        assert interior_rows | free_rows == set(range(nr)), \\\n'
     '            "a ridge lies in 0 or >=3 facets"\n',
     '    if incidence_mode == "true":\n'
     '        assert interior_rows | free_rows == set(range(nr)), \\\n'
     '            "a ridge lies in 0 or >=3 facets"\n'
     '        if interior_rows:\n'
     '            interior_rows = interior_rows - {min(interior_rows)}\n'),
    ("D2 the pipeline's le_to_facet is mis-indexed: the TRUE build uses the\n"
     "     off-by-one map (the defect row I4 is named for)",
     '    elif incidence_mode in INCIDENCE_MODES:\n'
     '        facets = [le_to_facet(w) for w in les]\n',
     '    elif incidence_mode in INCIDENCE_MODES:\n'
     '        facets = [le_to_facet_offbyone(w) for w in les]\n'),
    ("D3 the pipeline's free/interior split is wrong: one free ridge is counted\n"
     "     as interior in the TRUE build (the defect row I2 is named for)",
     '    if incidence_mode == "split_free_as_interior" and free_rows:\n',
     '    if incidence_mode in ("true", "split_free_as_interior") and free_rows:\n'),
]

ROWS = [("instrument check: a genuine", "instrument 1 (diagonal conjugation)"),
        ("instrument check: L^rel with one", "instrument 2 (one diagonal moved)"),
        ("instrument check: the union-find", "instrument 3 (vs brute force)"),
        ("baseline --", "baseline  [NEW in mg-8a12]"),
        ("I1 a ridge", "I1"), ("I2 the free", "I2"), ("I3 the ridge", "I3"),
        ("I4 the facet", "I4"),
        ("PROVEN PROPERTY", "theorem row  [NEW in mg-8a12]"),
        ("routing check", "routing check  [NEW in mg-8a12]")]


def statuses(text):
    out, inside = {}, False
    for line in text.splitlines():
        if line.startswith("NEGATIVE CONTROL 4"):
            inside = True
            continue
        if inside and line.startswith("  measured, not scored"):
            inside = False
        if not inside:
            continue
        m = re.match(r"  \[([A-Z ]+)\] (.*)", line)
        if not m:
            continue
        for tag, _ in ROWS:
            if m.group(2).startswith(tag):
                out[tag] = m.group(1)
    return out


def main():
    print("=" * 78)
    print("mg-f1b2 part 4 -- which NEGATIVE CONTROL 4 rows react to a CONSTRUCTION")
    print("                  error in the pipeline?")
    print("=" * 78)
    tmp = tempfile.mkdtemp(prefix="mg-f1b2-inj-")
    try:
        for f in ("controls.py", "face_complex.py", "posets.py"):
            shutil.copy(os.path.join(SRC_DIR, f), tmp)
        orig = open(os.path.join(tmp, "face_complex.py")).read()
        for name, old, new in DEFECTS:
            src = orig
            if old is not None:
                assert old in src, "patch anchor not found for %s" % name
                src = src.replace(old, new)
            open(os.path.join(tmp, "face_complex.py"), "w").write(src)
            shutil.rmtree(os.path.join(tmp, "__pycache__"), ignore_errors=True)
            p = subprocess.run([sys.executable, "controls.py", "5"], cwd=tmp,
                               capture_output=True, text=True)
            st = statuses(p.stdout)
            print("\n  %s" % name)
            if not st:
                print("      battery did not reach NEGATIVE CONTROL 4 (exit %d): %s"
                      % (p.returncode,
                         (p.stderr.strip().splitlines() or ["-"])[-1]))
                continue
            for tag, label in ROWS:
                print("      %-36s %s" % (label, st.get(tag, "(row absent)")))
            print("      battery exit code %d" % p.returncode)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    print("  READING.  Three genuine construction errors, each one the very defect a "
          "row is named\n  for.  The baseline row and all four mutation rows react "
          "to all three -- the section does\n  cover construction, and that part of "
          "mg-2789 and mg-8a12 stands.  The ROUTING CHECK\n  stays GREEN under D1 "
          "and D3, and reddens under D2 only because the off-by-one build\n  makes "
          "row I4's own mutation vacuous, which row I4 already reports itself.  It "
          "detects\n  nothing that is not already detected, which is what "
          "'cannot fail' means operationally.")


if __name__ == "__main__":
    main()
