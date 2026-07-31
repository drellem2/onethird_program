#!/bin/sh
# mg-6f61 -- the repair of mg-7d75 under mg-a61f's audit.
# Pure Python 3, no dependencies, NO NETWORK.  About 30 seconds, of which
# r2_columns.py is 27.
#
# r3_quotes.py reads code/species_audit_a61f/quotes_a61f.txt -- the poppler
# extraction the audit committed -- rather than re-fetching the PDFs.
# code/species_audit_a61f/fetch_sources.sh is the script that regenerates it,
# and it is the only network script in this cluster.
#
# mg-4adb: the three unguarded steps below -- r1_smallest, r2_columns,
# r3_quotes -- have their status read by `set -e` and by nothing else.  That
# is stated here rather than left to be inferred, and it is MEASURED: section
# V1e of code/species_rung_repair_4adb/v1_population.py deletes `set -e` and
# forces each step red in turn, so the three lines `set -e` carries are named
# in a transcript instead of being three lines nobody has ever tested.  No
# second guard is added beside it: a `||` guard next to a `set -e` is a line
# whose deletion changes no verdict, which is mg-4700's F2 and what mg-5040
# removed.  One rung, measured, is worth more than two that mask each other.
set -e
cd "$(dirname "$0")"

python3 selftest6f61.py > out_selftest.txt || { echo "SELFTEST FAILED"; exit 1; }
python3 r1_smallest.py  > out_r1_smallest.txt
python3 r2_columns.py   > out_r2_columns.txt          # ~27 s
python3 r3_quotes.py    > out_r3_quotes.txt
python3 check_doc.py    > out_check_doc.txt || { echo "CHECK_DOC FAILED"; exit 1; }

echo "done.  Headline lines:"
grep -h '^R[0-9] TOTAL BAD:\|^R2 PREDICTIONS MISSED:\|^CHECK_DOC:\|^selftest6f61' out_*.txt || true
echo
echo "R2 PREDICTIONS MISSED is NOT expected to be zero.  Both misses are"
echo "explained in out_r2_columns.txt R2e and in the repair document; a"
echo "battery whose expectations are written after the run cannot be wrong."
echo

# mg-821e, on mg-6cb9's F2.  THE CROSS-SECTION CHECK, WIRED.
# `e2_crosssection.py` is what closes mg-7dd3's B1: a claim struck in one
# section of a document and standing un-struck in another, which no
# per-section checker can see by construction.  B1 lived in a document THIS
# TREE checks.  The check existed, was correct, was named in every artifact a
# reader meets -- and was called by 0 of the 3 species run_all.sh, so the
# runner that would catch the next B1 did not execute it (mg-6cb9 F2, MAJOR).
# The removal question was asked BEFORE wiring and is answered, with
# measurements, in code/species_sites_821e/p3_wiring.py section P3a and in
# section 2 of docs/OneThird-Species-Hopf-Monoids-Repair-Sites.md: OUTCOME 2,
# the generator is not removable.  The OUTPUT is printed, not just the call
# made: a call present in a script is not evidence of execution.
# mg-5040, on mg-4700's OPEN 2.  ONE STATEMENT, AND IT IS THE ONE THAT HAS A
# RETURN.
# The block this replaces was twenty lines with THREE separable parts, and
# the deletion test mg-821e applied to it was applied to the whole block.
# Measured one part at a time (mg-4700 F2): deleting the `|| { ...; exit 1; }`
# guard alone changed no verdict in 3 of 3 runners, because `set -e` already
# aborts on a failed command substitution -- five lines that moved the MESSAGE
# and not the VERDICT; and deleting the two `echo`s that PRINTED the check's
# output left 3 of 3 exiting 0 with NO TRACE THE CHECK RAN, guarded by
# nothing.  The guard also reported ANY non-zero exit as "a struck claim
# stands un-struck elsewhere", so a crash in e2 was announced as a specific
# finding e2 never made (mg-4700 F5).
# That is the third structure the deletion test has missed -- after the gate
# (mg-9220) and the clause (mg-64b6).  The answer is NOT a fourth level of
# granularity: a test whose grain chases the code's structure never catches
# up.  THE STRUCTURE IS REMOVED.  Running the check and printing its output
# are now the SAME statement, so neither can be deleted without the other and
# there is exactly one unit here that has a return.  Nothing is piped, because
# a pipeline's status in POSIX sh is its LAST command's and `set -o pipefail`
# is not available in dash (mg-c2b3).
#
# mg-4adb, on mg-6ef4's F3.  THE STATEMENT THAT CARRIED THAT RETURN OUT OF
# THIS FILE WAS `set -e`, AT THE TOP.  Deleted alone it turned 3 of 3 runners
# GREEN while they printed e2's finding IN FULL, and it was in NO deletion
# population this arc had used -- so the certificate could never have covered
# the line that made it wrong.  THE FIX IS A MOVE, NOT AN ADDITION: a `||`
# guard beside a `set -e` is a line whose deletion changes no verdict because
# the other one catches it, which is mg-4700's F2 re-committed.  The gate is
# now THE LAST COMMAND OF THIS FILE and a POSIX script's exit status is its
# last command's, so what turns e2's exit code into this runner's is the CALL
# ITSELF -- inside every population that has ever enumerated the block.
# `set -e` stays -- in this file it is also the only rung the three
# unguarded steps above have, but nothing about this gate rests on it, and
# code/species_rung_repair_4adb/v1_population.py measures that by deleting it,
# in a population that is EVERY LINE OF THIS FILE with no exclusion at all.
# NOTHING MAY BE APPENDED BELOW THE CALL: that is the rung, and section V1d
# reads this file's source and goes red the day a line is added after it.
echo "cross-section check (mg-821e), its own output, unfiltered:"
python3 ../species_extent_d633/e2_crosssection.py
