"""mg-ec63 / S4 -- THE DAMAGE.  WHAT WAS PUBLISHED ON THE STRENGTH OF IT?

S3 says what the probe failed to see.  This says what was said out loud on the
strength of not having seen it, which is the only part of this ticket that
cannot be recovered later.  A transcript can be regenerated at any time.  A
sentence in a README that a human read and believed cannot be un-read.

THE TEST, PER DIFFERING STEP.  Take the lines where A (the defect) and B (a
real transcript) disagree.  Pull every integer out of the A-side of those lines
-- those are the figures the arc computed while reading an empty file.  Then ask
whether any of them was CARRIED OUT OF THE TRANSCRIPT into prose:

    (i)   the tree's own README.md / OUTCOMES.md / PREDICTIONS.md
    (ii)  the commit subjects that ship that tree
    (iii) any other tree's prose that cites this one

A figure that never left its transcript is a defect with NO DAMAGE, and that is
a result, not an absence.  A figure that reached a README is the damage.

AND THE OTHER DIRECTION, WHICH IS EASIER TO MISS.  A NEVER-EXERCISED probe
published nothing wrong -- it published a transcript of a probe that has never
been shown to work.  Its damage is that a control was counted as green.  That is
reported separately, because "no figure changed" is true of it and beside the
point.

Exit code = published claims found resting on an empty-file reading.
"""

import difflib
import os
import re
import sys

import lib_ec63 as B

print("mg-ec63 / S4 -- WHAT WAS PUBLISHED ON THE STRENGTH OF THE EMPTY FILE")
print("HEAD: %s" % B.head())

sweep = B.load("sweep")
if not sweep:
    print("  (run s3_sweep.py first -- it writes the ledger this reads)")
    sys.exit(1)
ROWS = sweep["rows"]
DIFF = [r for r in ROWS if r["verdict"] == "DIFFERENT"]
NEVER = [r for r in ROWS if r["verdict"] == "NEVER EXERCISED"]

PROSE = ("README.md", "OUTCOMES.md", "PREDICTIONS.md", "NOTES.md",
         "FINDINGS.md", "ADDENDUM.md")
INT = re.compile(r"(?<![\w.])(\d{1,7})(?![\w.])")


def prose_of(tree):
    out = {}
    d = os.path.join(B.REPO, tree)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f in PROSE or f.endswith(".md"):
                try:
                    out["%s/%s" % (tree, f)] = B.read("%s/%s" % (tree, f))
                except OSError:
                    pass
    return out


def subjects(tree):
    txt = B.git("log", "--format=%h%x09%s", "--", tree)
    return [ln for ln in txt.splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
B.hdr("S4a  THE FIGURES THAT MOVED")

print("  population: the %d DIFFERENT STEPS of S3a" % len(DIFF))
print()
if not DIFF:
    print("      (none -- S3 found no step whose answer changes.  That is the")
    print("      result, and it is stated rather than implied by silence.)")

damage = []
nodamage = []
for row in DIFF:
    al = row["A_text"].splitlines()
    bl = row["B_text"].splitlines()
    sm = difflib.SequenceMatcher(None, al, bl)
    a_only, b_only = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            a_only += al[i1:i2]
        if tag in ("replace", "insert"):
            b_only += bl[j1:j2]
    a_ints = set()
    for ln in a_only:
        a_ints |= set(INT.findall(ln))
    b_ints = set()
    for ln in b_only:
        b_ints |= set(INT.findall(ln))
    moved = sorted(a_ints - b_ints, key=lambda x: (-len(x), x))

    print()
    print("  ----------------------------------------------------------------")
    print("  %s  ::  %s" % (row["tree"].replace("code/", ""),
                            os.path.basename(row["probe"])))
    print("  lines only in A (the defect): %d      only in B (real file): %d"
          % (len(a_only), len(b_only)))
    print("  integers on the A side that are NOT on the B side: %s"
          % (", ".join(moved[:14]) if moved else "(none)"))

    hits = []
    docs = prose_of(row["tree"])
    for n in moved:
        if len(n) < 2:
            continue                      # 0..9 match everything; excluded and
            # the exclusion is stated, not silent
        for path, txt in docs.items():
            for ln in txt.splitlines():
                if re.search(r"(?<![\w.])%s(?![\w.])" % re.escape(n), ln):
                    hits.append((n, path, ln.strip()[:120]))
        for s in subjects(row["tree"]):
            if re.search(r"(?<![\w.])%s(?![\w.])" % re.escape(n), s):
                hits.append((n, "COMMIT SUBJECT", s.strip()[:120]))
    seen, uniq = set(), []
    for h in hits:
        if h[:2] not in seen:
            seen.add(h[:2])
            uniq.append(h)
    if uniq:
        damage.append((row, uniq))
        print("  PUBLISHED CLAIMS CARRYING ONE OF THOSE FIGURES:")
        for n, path, ln in uniq[:10]:
            print("      %-6s %-28s %s" % (n, os.path.basename(path), ln))
        if len(uniq) > 10:
            print("      ... and %d more" % (len(uniq) - 10))
    else:
        nodamage.append(row)
        print("  NO PUBLISHED CLAIM carries any of those figures.  The delta is")
        print("  confined to the transcript.  A REAL RESULT, recorded as one.")

# ---------------------------------------------------------------------------
B.hdr("S4b  THE NEVER-EXERCISED PROBES -- A DIFFERENT KIND OF DAMAGE")

print("  population: the %d NEVER-EXERCISED STEPS of S3a" % len(NEVER))
print()
print("  These published no wrong figure.  They published a GREEN CONTROL that")
print("  has never been shown to work on real input, which is the shape this")
print("  arc has now hit five times in one night: an exit 0 over zero gate runs,")
print("  four verdicts pinned to the literal False, a row scoring a string")
print("  literal, a checker returning 0 for an absent document, and this.")
print()
for row in NEVER:
    print("      %-40s %-24s A exit %s / B exit %s"
          % (row["tree"].replace("code/", ""),
             os.path.basename(row["probe"]), row["A_exit"], row["B_exit"]))
    for ln in row["B_text"].splitlines()[-6:]:
        print("          B: %s" % ln[:120])
if not NEVER:
    print("      (none.  Stated rather than left to silence: NO probe in the")
    print("      emptied population fails against a populated transcript.)")

# ---------------------------------------------------------------------------
B.hdr("S4c  THE TALLY")

print("  population: the %d DIFFERENT STEPS of S3a" % len(DIFF))
B.plain("...STEPS whose changed figure REACHED PROSE (damage)", len(damage),
        "one step")
B.plain("...STEPS whose delta never left the transcript", len(nodamage),
        "one step")
print()
print("  population: the %d EMPTIED STEPS swept in S3a" % len(ROWS))
B.plain("...STEPS costing the arc a published figure", len(damage), "one step")
B.plain("...STEPS costing the arc an unexercised control", len(NEVER),
        "one step")
B.plain("...STEPS costing the arc nothing", len(ROWS) - len(damage) - len(NEVER),
        "one step")

B.save("damage", {"damage": [[r["tree"], r["probe"], h] for r, h in damage],
                  "nodamage": [[r["tree"], r["probe"]] for r in nodamage],
                  "never": [[r["tree"], r["probe"]] for r in NEVER]})

print()
print("S4 TOTAL PUBLISHED CLAIMS RESTING ON AN EMPTY FILE: %d" % len(damage))
sys.exit(min(len(damage), 120))
