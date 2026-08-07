#!/bin/sh
# mg-7085: the rest of mg-cf83's sweep -- s2_controls.py, s3_graph.py and
# s4_crosscheck.py in code/census_repair_f3ff/, run rather than read.
#
#     sh run_all.sh          # ~12 min; the two healthy arms dominate, because
#                            # s1's loose chain reader runs six times in total
#
# Pure Python 3 + git, no third-party packages.
#
# ⚠️ THIS RUNNER DOES NOT FETCH EITHER SOURCE REPO.  Every arm runs against
# throwaway clones of FROZEN BARE MIRRORS under a scratch directory, so nothing
# here fetches, checks out, stashes or pulls in /Users/daniel/research/*.  The
# clones' own remotes are what get broken, and they are broken AFTER cloning so
# origin/main still resolves -- an UNKNOWN is then a FAILED FETCH and not an
# absent ref.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s -- under `set -e` a
# pipeline's exit status is the LAST command's, which is how a transcript
# recording a refutation once came to be committed beside an exit 0 (mg-c2b3).
#
# EXIT: 0 if THIS INSTRUMENT ran.  ⚠️ FINDINGS ABOUT THE SUBJECT DO NOT SET IT --
# the rule run_all.sh states for mg-f3ff, for the same reason: an instrument that
# exited 1 for successfully finding what it was sent to find could not
# distinguish `the subject has a defect` from `the auditor is broken`, and those
# need different responses.  A failed check OF THIS HARNESS does set it.
cd "$(dirname "$0")"

echo "== mg-7085: the rest of the sweep, three arms, before and after =="
status=0
python3 r1_sweep.py "$@" > out_r1_sweep.txt 2>&1 || status=$?
cat out_r1_sweep.txt

echo
echo "== mg-7085 aggregate exit: $status =="
exit "$status"
