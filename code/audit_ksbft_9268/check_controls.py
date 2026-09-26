#!/usr/bin/env python3
"""check_controls.py (mg-9268) -- asserts that every NEGATIVE CONTROL in
out_controls.txt actually fired, and that the clean runs are clean.  Prints
CAUGHT per fired control; exits 1 (and prints FAILED TO FIRE) otherwise."""
import re, sys
t = open(sys.argv[1] if len(sys.argv) > 1 else "out_controls.txt").read()
checks = [
    ("target [0.34,0.66] flags exactly the 2+1 forms (tree.c and aud, D=3,4,5)",
     t.count("COUNTEREXAMPLE-TO-THRESHOLD N=3 [0,0,2]") == 3 and t.count("VIOLATION n=3 [0,0,1]") == 3
     and len(re.findall(r"COUNTEREXAMPLE-TO-THRESHOLD", t)) == 6 and len(re.findall(r"^VIOLATION n=", t, re.M)) == 6),
    ("target [0.39,0.61] violates and does not terminate (D=3)", re.search(r"front [1-9]\d*", t) is not None),
    ("tree.c mutant cut+1 reports FOUND-VIOLATION at D=3,4,5", t.count("RESULT FOUND-VIOLATION") >= 6),
    ("aud badcut caught by end-to-end probe at D=3,5,7",
     all(int(m) > 0 for m in re.findall(r"random indecomposable posets.*failures (\d+)", t)) and len(re.findall(r"failures (\d+)", t)) == 3),
    ("aud badcut: P=[0,0,1,1,7,11] falsely certified at depth 5, k=4", "FOLLOW n=6 depth=5 CERT k=4 1,2" in t),
    ("aud badcut caught by sample probe (SAFE CUT FAILS count > 0)", re.search(r"expect SAFE CUT FAILS\n([1-9]\d*)", t) is not None),
]
bad = 0
for name, ok in checks:
    print(("NEGATIVE CONTROL CAUGHT: " if ok else "NEGATIVE CONTROL FAILED TO FIRE: ") + name)
    bad += not ok
print("ALL CONTROLS FIRED" if not bad else f"{bad} CONTROLS FAILED TO FIRE")
sys.exit(1 if bad else 0)
