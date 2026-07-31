#!/bin/sh
# The instrument for mg-330a -- the INDEPENDENT AUDIT of the mg-8d5e
# anchor-and-term repair (dfa263c), pre-filed in the same action as its
# parent.
#
#   s1  EVERY DERIVED ANCHOR, RESOLVED.  Not its logic -- its answer, against
#       the pair its own prose names and against the subject of the commit it
#       lands on.  Plus the REPO-WIDE sweep for a fourth: every
#       revision-producing git log call under code/, classified by HOW the
#       revision is obtained.
#
#   s2  THE FAILURE, CONSTRUCTED.  A cosmetic commit to g1_provenance.py at
#       HEAD and again at e2577e5, WHERE THE DEFECT IS STILL PRESENT.  Plus
#       the three constructed failures of the repaired anchor, scored for
#       whether any two of them fail the same way.
#
#   s3  BOTH COLUMNS OF THE KERNEL-HALF CONFIRMATION, RE-DERIVED -- the
#       pinned predicate installed with its OWN lib58da and run against a
#       committed kernel bend.  And the same bend under the DRIFTED anchor,
#       run rather than argued, so the vacuity is a measurement.
#
#   s4  THE TERM.  39 / 17 / 22 by an independent AST walk, the 22 named; the
#       qualifier at all 15 sites; the hyphenated-form control on the ruler;
#       and the same rule RE-SCOPED TO HEAD, which is on no list in the brief.
#
#   s5  WHAT MUST STILL BE THERE.  The fourth input that is neither case, the
#       second conspiring pair of a different shape, the edge probe, `AND
#       NOTHING ELSE`, and the parsed module of the one file the repair
#       touched that all four rest on.
#
# Pure Python 3, no dependencies, NO NETWORK.
#
# EXIT-CODE CONVENTION, taken from code/repair_8d5e/run_all.sh so the ruler is
# theirs and not a second one that agrees today.  Every s*.py exits 0 iff
# SELF-ERRORS == 0 AND FINDINGS == 0.  A non-zero exit means "this script has
# something to report", never "this script is broken"; the two numbers are
# printed separately and every count names its population.  PREDICTIONS.md
# holds the exit code predicted for each script BEFORE any of them existed,
# with the misses kept as written.
#
# NO PIPE ANYWHERE (mg-c2b3, mg-f922): each script's stdout is REDIRECTED and
# `$?` is read on the next line.  A pipeline's status in POSIX sh is the LAST
# command's, so `| tee` would let a red verifier hide under a green runner.
#
# NOTHING HERE WRITES INTO code/branching_audit_e34a/, code/repair_8d5e/,
# code/repair_69d1/, code/audit_2c77/, code/branching_audit_58da/,
# code/branching_audit_a218/, code/face_geometry_instr_5f9a/ or
# code/face_geometry/.  s2, s3 and s5 RUN foreign scripts -- selftest_e34a.py,
# k1_prerepair.py, q1_reason.py, q2_bound_edge.py -- and capture their stdout;
# none of the four writes a file.  Every mutation is a commit in a clone under
# the system temp directory.
#
# RUNTIME.  s3 runs k1_prerepair.py (21 pinned g1 runs across 7 clones) and
# four g1 runs of its own; s5 runs q1 and q2.  Roughly ten minutes in all;
# s1, s2 and s4 are each well under a minute.
set -u
cd "$(dirname "$0")"
WORST=0

run() {
    printf '%s\n' "----- $1 -----"
    python3 -u "$1" > "out_${1%.*}.txt" 2>&1
    RC=$?
    tail -1 "out_${1%.*}.txt"
    if [ "$RC" -gt "$WORST" ]; then WORST=$RC; fi
    printf 'exit %s\n\n' "$RC"
}

run selftest_330a.py
run s1_anchors.py
run s2_perturb.py
run s3_kernel_half.py
run s4_term.py
run s5_preserve.py

printf 'WORST EXIT: %s\n' "$WORST"
exit "$WORST"
