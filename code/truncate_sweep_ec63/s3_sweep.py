"""mg-ec63 / S3 -- THE SWEEP.  WHAT DID THE PROBE FAIL TO SEE?

This is the deliverable.  For every step S2 confirmed EMPTIED, the probe is run
a second time at the SAME TREE STATE with its own transcript EMPTIED FIRST --
exactly what `>` does -- and that is compared with the run S2 already did with
the transcript populated.

    A   the defect reproduced.  What the arc has been publishing.
    B   the same probe, same tree, same second, with a real transcript.

`diff(A, B)` is attributable to the shape and to nothing else.  Neither run is
ever redirected onto a transcript; the tree is restored after every probe.

THREE OUTCOMES, AND THEY ARE NOT COLLAPSED:

    SAME              A == B.  A harmless ordering bug.  A REAL RESULT.
    DIFFERENT         A != B.  The probe reports something else once it can
                      see the file, so a published figure may be wrong.
    NEVER EXERCISED   B cannot run at all where A could -- the probe has only
                      ever been run against an empty file, and nobody has seen
                      it work.  THIS IS THE WORST AND THE EASIEST TO MISS,
                      because in the transcript it looks exactly like a probe
                      that ran and found nothing.

AND A CONTROL THE THREE-WAY SPLIT NEEDS.  A probe that is simply not
deterministic would show up as DIFFERENT for a reason that has nothing to do
with the shape.  So every candidate DIFFERENT is re-run a THIRD time under the
B conditions: if B != B', the step is NONDETERMINISTIC and is not counted as
DIFFERENT.  Without this control the headline number is an artefact.

Exit code = steps in DIFFERENT + NEVER-EXERCISED.
"""

import difflib
import os
import sys

import lib_ec63 as B

print("mg-ec63 / S3 -- THE SWEEP: WHAT THE PROBE FAILED TO SEE")
print("HEAD: %s" % B.head())

bite = B.load("bite")
if not bite:
    print("  (run s2_bite.py first -- it writes the ledger this reads)")
    sys.exit(1)
RECS = [r for r in bite["recs"] if r["own"]]
TIMEOUT = int(os.environ.get("EC63_TIMEOUT", "45"))

# ---------------------------------------------------------------------------
B.hdr("S3a  RUNNING EVERY EMPTIED STEP AGAINST THE DEFECT")

print("  population: the %d EMPTIED STEPS of S2b" % len(RECS))
print()

rows = []
for r in RECS:
    tree, rel = r["tree"], os.path.relpath(r["probe"], r["tree"])
    ob = os.path.basename(r["out"])
    a = B.run_probe(tree, rel, ob, empty_first=True, timeout=TIMEOUT)
    row = {"tree": tree, "probe": r["probe"], "out": r["out"],
           "A_text": a["text"], "A_exit": a["exit"], "A_to": a["timeout"],
           "B_text": r["B_text"], "B_exit": r["exit"], "B_to": r["timeout"]}
    rows.append(row)

# --- the determinism control, only where it changes an answer --------------
ndet = 0
for row in rows:
    if row["A_text"] == row["B_text"]:
        continue
    r2 = B.run_probe(row["tree"], os.path.relpath(row["probe"], row["tree"]),
                     os.path.basename(row["out"]), empty_first=False,
                     timeout=TIMEOUT)
    row["Bp_text"] = r2["text"]
    row["nondet"] = (r2["text"] != row["B_text"])
    if row["nondet"]:
        ndet += 1

# --- and the drift control -------------------------------------------------
for row in rows:
    try:
        committed = B.read(row["out"])
    except OSError:
        committed = None
    row["reproduces"] = (committed is not None
                         and committed.strip() == row["A_text"].strip())


def classify(row):
    # A timeout in the DEFECT run is not a comparison at all: A never finished,
    # so `A != B` says nothing about the shape.  It gets its own name instead
    # of being counted as a difference, which is what a two-way split would do.
    if row["A_to"] and not row["B_to"]:
        return "A TIMED OUT"
    if row["A_to"] and row["B_to"]:
        return "BOTH TIMED OUT"
    if row.get("nondet"):
        return "NONDETERMINISTIC"
    b_broke = row["B_to"] or (row["B_exit"] is not None
                              and "Traceback" in row["B_text"])
    a_ok = (not row["A_to"]) and "Traceback" not in row["A_text"]
    if b_broke and a_ok:
        return "NEVER EXERCISED"
    if row["A_text"] == row["B_text"]:
        return "SAME"
    return "DIFFERENT"


for row in rows:
    row["verdict"] = classify(row)

order = ["DIFFERENT", "NEVER EXERCISED", "NONDETERMINISTIC", "A TIMED OUT",
         "BOTH TIMED OUT", "SAME"]
counts = dict((k, sum(1 for r in rows if r["verdict"] == k)) for k in order)

B.plain("...EMPTIED STEPS swept", len(rows), "one step")
for k in order:
    B.plain("...of those, %s" % k, counts[k], "one step")
print()
B.plain("...RUNNERS with at least one DIFFERENT or NEVER-EXERCISED step",
        len(set(r["tree"] for r in rows
                if r["verdict"] in ("DIFFERENT", "NEVER EXERCISED"))),
        "one `run_all.sh`")
print()
print("  A SAME row is a real result and is reported as one: for those steps")
print("  the ordering bug cost the arc nothing, and saying so is the only way")
print("  the DIFFERENT rows mean anything.")

# ---------------------------------------------------------------------------
B.hdr("S3b  THE DRIFT CONTROL -- DOES THE DEFECT RUN STILL MATCH WHAT SHIPPED?")

repro = [r for r in rows if r["reproduces"]]
print("  `diff(A, B)` isolates the shape.  It does NOT by itself tell you a")
print("  published figure is wrong: if the tree has moved since the transcript")
print("  was committed, A no longer matches what shipped either, and the")
print("  published-claim question has to be asked against the COMMITTED bytes.")
print()
print("  population: the %d EMPTIED STEPS of S3a" % len(rows))
B.plain("...STEPS where A reproduces the committed transcript", len(repro),
        "one step")
B.plain("...STEPS where the tree has DRIFTED since publication",
        len(rows) - len(repro), "one step")
print()
print("  Only the reproducing rows license the sentence 'the published figure")
print("  was computed under the defect'.  For the drifted rows S4 goes to the")
print("  committed bytes directly.")

# ---------------------------------------------------------------------------
B.hdr("S3c  EVERY DIFFERENT AND NEVER-EXERCISED ROW, WITH ITS DELTA")

interesting = [r for r in rows
               if r["verdict"] in ("DIFFERENT", "NEVER EXERCISED")]
for row in interesting:
    print()
    print("  ----------------------------------------------------------------")
    print("  %s  ::  %s" % (row["tree"].replace("code/", ""),
                            os.path.basename(row["probe"])))
    print("  verdict: %-16s A exits %s / B exits %s / A reproduces committed: %s"
          % (row["verdict"], row["A_exit"], row["B_exit"],
             "yes" if row["reproduces"] else "NO -- tree drifted"))
    al = row["A_text"].splitlines()
    bl = row["B_text"].splitlines()
    print("  lines: A=%d  B=%d" % (len(al), len(bl)))
    d = [x for x in difflib.unified_diff(al, bl, "A(empty)", "B(populated)",
                                         n=1, lineterm="")]
    shown = 0
    for x in d:
        if shown > 40:
            print("      ... (%d further diff lines)" % (len(d) - shown))
            break
        print("      %s" % x[:150])
        shown += 1

# ---------------------------------------------------------------------------
B.hdr("S3d  AND THE SAME ROWS, LISTED, BECAUSE A NULL RESULT IS A RESULT")

for row in rows:
    if row["verdict"] == "SAME":
        print("      SAME  %-40s %s" % (row["tree"].replace("code/", ""),
                                        os.path.basename(row["probe"])))
for row in rows:
    if row["verdict"] == "NONDETERMINISTIC":
        print("      NDET  %-40s %s   (excluded from DIFFERENT by the control)"
              % (row["tree"].replace("code/", ""),
                 os.path.basename(row["probe"])))

B.restore_arc()

B.save("sweep", {"rows": [{k: v for k, v in r.items()
                           if k not in ("Bp_text",)} for r in rows]})

n = counts["DIFFERENT"] + counts["NEVER EXERCISED"]
print()
print("S3 TOTAL DIFFERENT + NEVER-EXERCISED: %d" % n)
sys.exit(min(n, 120))
