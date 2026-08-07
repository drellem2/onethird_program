#!/bin/sh
# mg-cf83: the positive control for the summary-block repair of
# code/census_repair_f3ff/s1_rows.py.
#
#     sh run_all.sh          # ~3 min; arm H's loose chain reader dominates
#
# Pure Python 3 + git, no third-party packages.
#
# ⚠️ THIS RUNNER DOES NOT FETCH EITHER SOURCE REPO.  Every arm runs against
# throwaway clones under a scratch directory (`MGCF83_SCRATCH` if set), so
# nothing here fetches, checks out, stashes or pulls in
# /Users/daniel/research/*.  The clones' own remotes are what get broken.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s -- under `set -e` a
# pipeline's exit status is the LAST command's, which is how a transcript
# recording a refutation once came to be committed beside an exit 0 (mg-c2b3).
#
# EXIT: 0 if every check of this control passed.  ⚠️ Unlike the instrument it
# tests, a failure here IS this instrument failing: c1 has no findings to
# report, only checks, and a red check means the repair does not hold.
cd "$(dirname "$0")"

echo "== mg-cf83: the summary block under a REAL fetch failure =="
status=0
python3 c1_summary_guard.py "$@" > out_c1_summary_guard.txt 2>&1 || status=$?
cat out_c1_summary_guard.txt

echo
echo "== mg-cf83 aggregate exit: $status =="
exit "$status"
