"""D6 -- THE EXIT CODE, ACROSS EVERY INSTRUMENT IN THE ARC.

mg-a4ef found and disclosed one of these, beyond mg-73df's five:

    "`w3_scope.py` ended with `sys.exit(0)` UNCONDITIONALLY, so a run printing
     `W3 SCOPE: FAIL (12 problems)` still exited 0.  That is the same shape as
     the finding the file exists to carry -- a clean signal that does not mean
     what it reads as.  It now exits 1 on failure.  `check_doc.py` already
     did."

Two files named, both fixed or already right.  This file asks the same
question of ALL of them, because the sentence above is a statement about two
files and reads as a statement about the instrument.

The two that matter are `c4_scope.py` and `c5_doc.py`: mg-a4ef re-ran them
UNMODIFIED as its independent corroboration and committed their output as
`out_c4_scope_73df_after.txt` / `out_c5_doc_73df_after.txt`.  One of those
committed outputs ends `C5 TOTAL BAD: 1`.

    python3 code/species_audit_7dd3/d6_exitcodes.py
"""

import os
import re
import subprocess
import sys

from kern7dd3 import hdr

bad = 0
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", ".."))
TREES = ["species_7d75", "species_repair_6f61", "species_remainder_f8fa",
         "species_repair_a4ef", "species_audit_73df", "species_audit_a61f"]
VERDICT = re.compile(r"(?m)^\s*(?:[A-Z0-9]+ )?(?:TOTAL BAD|STILL ASSERTED "
                     r"AT SOURCE|PREDICTIONS MISSED):\s*(\d+)\s*$"
                     r"|^(CHECK_DOC|W3 SCOPE):\s*(\w+)")

hdr("D6a  IS THE FINAL EXIT CONDITIONAL?  (static, every script in the arc)")
rows = []
for t in TREES:
    root = os.path.join(REPO, "code", t)
    if not os.path.isdir(root):
        continue
    for f in sorted(os.listdir(root)):
        if not f.endswith(".py") or f.startswith(("kern", "hopf", "stricken")):
            continue
        src = open(os.path.join(root, f), encoding="utf-8").read()
        exits = re.findall(r"(?m)^sys\.exit\((.*)\)\s*$", src)
        if not exits:
            continue
        last = exits[-1]
        cond = last.strip() not in ("0",)
        rows.append((t, f, last, cond))

for t, f, last, cond in rows:
    print("      code/%-22s %-22s sys.exit(%s)%s"
          % (t, f, last, "" if cond else "   <- UNCONDITIONAL 0"))
uncond = [r for r in rows if not r[3]]
print()
print("  %d script(s) with a final exit; %d exit 0 unconditionally."
      % (len(rows), len(uncond)))
print()

hdr("D6b  DOES ANY OF THEM PRINT A NONZERO VERDICT AND EXIT 0?")
print("  Run, not inferred.  Only the two mg-a4ef re-ran as its own")
print("  corroboration, because those are the ones it stands on.")
print()
for t, f in [("species_audit_73df", "c4_scope.py"),
             ("species_audit_73df", "c5_doc.py")]:
    d = os.path.join(REPO, "code", t)
    r = subprocess.run([sys.executable, f], cwd=d, capture_output=True,
                       text=True)
    nums = [int(m.group(1)) for m in
            re.finditer(r"(?m)^C\d (?:TOTAL BAD|STILL ASSERTED AT SOURCE): "
                        r"(\d+)$", r.stdout)]
    lines = [l for l in r.stdout.splitlines()
             if re.match(r"^C\d (TOTAL BAD|STILL ASSERTED AT SOURCE):", l)]
    print("      code/%s/%s" % (t, f))
    for l in lines:
        print("          %s" % l)
    print("          exit code %d" % r.returncode)
    inconsistent = any(nums) and r.returncode == 0
    bad += inconsistent
    print("          %s" % ("*** REPORTS A FINDING AND EXITS 0 ***"
                            if inconsistent else "consistent"))
    print()

print("  mg-a4ef's disclosure -- 'It now exits 1 on failure.  check_doc.py")
print("  already did.' -- is true of the two files it names.  The instrument")
print("  it re-ran UNMODIFIED to corroborate itself has the same defect, and")
print("  the committed out_c5_doc_73df_after.txt ends C5 TOTAL BAD: 1 with an")
print("  exit code of 0.  This is mg-73df's code and not mg-a4ef's; what is")
print("  mg-a4ef's is standing on it and saying the shape was closed.")
print()

print("=" * 78)
print("D6 TOTAL BAD: %d" % bad)
print("=" * 78)
print()
print("EXTENT OF THIS NUMBER.  D6 reads the LAST `sys.exit(...)` at column 0")
print("in every non-kernel .py in the six species trees -- %d script(s) --"
      % len(rows))
print("and RUNS exactly two of them.  A script whose exit is conditional but")
print("on the wrong variable would pass D6a, and a script D6b does not run is")
print("a static reading only.  It says nothing about any tree outside")
print("code/species_*.")
sys.exit(1 if bad else 0)
