"""mg-ec63 / S4 -- THE DAMAGE.  WHAT WAS PUBLISHED ON THE STRENGTH OF IT?

S3 says what the probe failed to see.  This says what was said out loud on the
strength of not having seen it, which is the only part of this ticket that
cannot be recovered later.  A transcript can be regenerated at any time.  A
sentence in a README that a human read and believed cannot be un-read.

THE TEST, PER DIFFERING STEP.  Take the lines where A (the defect) and B (a
real transcript) disagree.  Pull every integer out of the A-side of those lines
-- those are the figures the arc computed while reading an empty file.  Then ask
whether any of them was CARRIED OUT OF THE TRANSCRIPT into prose: the tree's
own .md files, and the commit subjects that ship it.

AN INTEGER MATCH IS A CANDIDATE AND NOT A PROOF, and S4a labels it as one.  A
README saying `20` and a transcript saying `20` may be the same 20 or two
different ones, and only reading the sentence settles it.  The check that
settles it WITHOUT reading is in S4a2: does run A come out byte-identical to
the COMMITTED transcript?  Where it does, the shipped bytes are a defect run
and the attribution is arithmetic.  Where the tree has drifted, the honest
statement is `suspect`, and `suspect` is not `wrong`.

AND THE OTHER DIRECTION, WHICH IS EASIER TO MISS.  A NEVER-EXERCISED probe
published nothing wrong -- it published a transcript of a probe that has never
been shown to work.  Its damage is that a control was counted as green.  That is
reported separately, because "no figure changed" is true of it and beside the
point.

Exit code = candidate prose claims (S4a), which is the LARGER of the two
numbers here and deliberately the one that does NOT license a conclusion.
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
        print("  PROSE CARRYING ONE OF THOSE INTEGERS -- A CANDIDATE, NOT A")
        print("  PROOF.  An integer match is a coincidence until the sentence")
        print("  is read; S4a2 is the row that does not need reading:")
        for n, path, ln in uniq[:10]:
            print("      %-6s %-28s %s" % (n, os.path.basename(path), ln))
        if len(uniq) > 10:
            print("      ... and %d more" % (len(uniq) - 10))
    else:
        nodamage.append(row)
        print("  NO PUBLISHED CLAIM carries any of those figures.  The delta is")
        print("  confined to the transcript.  A REAL RESULT, recorded as one.")

# ---------------------------------------------------------------------------
B.hdr("S4a2  THE ROWS WHERE PUBLICATION CAN ACTUALLY BE ATTRIBUTED")

print("  `diff(A, B)` proves the SHAPE changes the answer TODAY.  It does not")
print("  by itself prove a PUBLISHED figure is wrong, and conflating the two")
print("  would be this arc's own recurring error.  The bridge is one check:")
print()
print("      does run A -- the defect, reproduced -- come out BYTE-IDENTICAL")
print("      to the transcript that is committed in the tree?")
print()
print("  Where it does, the committed transcript IS a run under the defect and")
print("  the attribution is arithmetic.  Where it does not, the tree has moved")
print("  since publication and the published figure cannot be recomputed")
print("  without checking out the publishing revision -- which this ticket did")
print("  NOT do, and says so rather than reaching for the integer match.")
print()
attrib = [r for r in DIFF if r.get("reproduces")]
drift = [r for r in DIFF if not r.get("reproduces")]
print("  population: the %d DIFFERENT STEPS of S3a" % len(DIFF))
B.plain("...STEPS whose committed transcript IS the defect run", len(attrib),
        "one step")
B.plain("...STEPS whose tree has drifted since publication", len(drift),
        "one step")
print()
for row in attrib:
    print("      ATTRIBUTED  %-38s %s"
          % (row["tree"].replace("code/", ""),
             os.path.basename(row["probe"])))
    print("          the bytes in %s were produced by a run that could not"
          % row["out"])
    print("          see that file.  What a run that CAN see it reports is the")
    print("          B side of S3c, and the difference is the damage.")
for row in drift:
    print("      DRIFTED     %-38s %s"
          % (row["tree"].replace("code/", ""),
             os.path.basename(row["probe"])))
if drift:
    print()
    print("  FOR THE DRIFTED ROWS THE HONEST STATEMENT IS THE WEAKER ONE: this")
    print("  probe's answer is sensitive to the shape, so any figure it")
    print("  published while the shape was live is SUSPECT.  `suspect` is not")
    print("  `wrong`, and the work that would turn one into the other -- run")
    print("  each probe at its own publishing revision -- is named in")
    print("  README.md under WHAT I DID NOT DO.")

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
B.plain("...STEPS whose changed figure has an INTEGER MATCH in prose",
        len(damage),
        "one step")
B.plain("...STEPS whose delta never left the transcript", len(nodamage),
        "one step")
print()
print("  population: the %d EMPTIED STEPS swept in S3a" % len(ROWS))
B.plain("...STEPS with an integer match in prose (candidate)", len(damage),
        "one step")
B.plain("...STEPS where the committed transcript IS the defect run (proven)",
        len([r for r in DIFF if r.get("reproduces")]), "one step")
B.plain("...STEPS costing the arc an unexercised control", len(NEVER),
        "one step")
B.plain("...STEPS costing the arc nothing", len(ROWS) - len(damage) - len(NEVER),
        "one step")

B.save("damage", {"damage": [[r["tree"], r["probe"], h] for r, h in damage],
                  "nodamage": [[r["tree"], r["probe"]] for r in nodamage],
                  "never": [[r["tree"], r["probe"]] for r in NEVER]})

print()
print("S4 TOTAL PUBLISHED TRANSCRIPTS PROVEN TO BE DEFECT RUNS: %d"
      % len([r for r in DIFF if r.get("reproduces")]))
print("S4 TOTAL CANDIDATE PROSE CLAIMS BY INTEGER MATCH: %d" % len(damage))
sys.exit(min(len(damage), 120))
