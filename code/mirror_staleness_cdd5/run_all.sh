#!/bin/sh
# mg-cdd5: THE STALE MAIN-MIRROR, and the sweep for other citations landing on
# superseded text.
#
#     sh run_all.sh          # ~7.5 s MEASURED on this host; pure Python 3 + git, no third-party packages
#
# ⚠️ THIS RUNNER DOES NOT FETCH, DOES NOT CHECK OUT, AND DOES NOT PULL.  It
# reads `git ls-remote` (which asks the remote and moves nothing) to confirm
# the tracking ref is not itself stale, and every content read is
# `git show <rev>:<path>`.  Nothing in the mirror repo's working tree is
# opened for content, and nothing in either repo is written.  The one-shot
# fast-forward that this deliverable RECOMMENDS is a separate, manual act and
# is deliberately not automated here -- see README §4.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s (mg-c2b3): under
# `set -e` a pipeline's exit status is the LAST command's, which is how a
# transcript recording a refutation once came to be committed beside an exit 0.
# Each script redirects; the status is captured; the transcript is then `cat`.
#
# EXIT: 0 if no control of THIS instrument was refuted.  ⚠️ FINDINGS ABOUT THE
# MIRROR DO NOT SET IT.  s2 reports stale citations and this still exits 0: an
# instrument that exited 1 for successfully finding what it was sent to find
# could not distinguish `the subject has a defect` from `the auditor is
# broken`, and those need different responses.
cd "$(dirname "$0")"

echo "== mg-cdd5: the stale main-mirror and the citation sweep =="
status=0
for s in selftest_cdd5 s0_state s1_delta s2_sweep s3_controls; do
    # stderr goes INTO the transcript: a crash and a fired check are both
    # exit 1, and a transcript keeping only stdout ends mid-section with no
    # reason given.
    python3 "$s.py" "$@" > "out_$s.txt" 2>&1 || status=$?
    cat "out_$s.txt"
done

echo
echo "== mg-cdd5 aggregate exit: $status =="
exit "$status"
