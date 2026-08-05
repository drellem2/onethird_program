#!/bin/sh
# mg-f3ff: the dropped-verdict census of 2026-07-31, RE-DERIVED FROM THE TREE,
# and the METHOD repaired.
#
#     sh run_all.sh          # ~50 s; s1's loose chain reader dominates
#
# Pure Python 3 + git, no third-party packages.
#
# ⚠️ THIS RUNNER FETCHES.  Every script calls `git fetch origin` in both repos
# and derives against `origin/main`, because that is the ticket's addendum and
# because a census run against a stale checkout reports the same wrong answer
# with the authority of having read the tree.  It does NOT check out, pull,
# stash, or otherwise touch either working tree -- `fetch` moves remote refs
# only, and both repos may hold uncommitted user state.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s.  Under `set -e` a
# pipeline's exit status is the LAST command's, which is how a transcript
# recording a refutation once came to be committed beside an exit 0 (mg-c2b3).
# Each script redirects; the status is captured; the transcript is then `cat`.
#
# EXIT: 0 if no control of THIS instrument was refuted.  ⚠️ FINDINGS ABOUT THE
# CENSUS DO NOT SET IT, and neither do missed predictions.  s1 reports 2 of 4
# census rows wrong and s2/s3 report 2 missed predictions, and this still exits
# 0: an instrument that exited 1 for successfully finding what it was sent to
# find could not distinguish `the subject has a defect` from `the auditor is
# broken`, and those need different responses.
cd "$(dirname "$0")"

echo "== mg-f3ff: the dropped-verdict census re-derived from the commit log =="
status=0
for s in selftest_f3ff s0_freshness s1_rows s2_controls s3_graph \
         s4_crosscheck; do
    # stderr goes INTO the transcript: a crash and a fired check are both
    # exit 1, and a transcript keeping only stdout ends mid-section with no
    # reason given.
    python3 "$s.py" "$@" > "out_$s.txt" 2>&1 || status=$?
    cat "out_$s.txt"
done

echo
echo "== mg-f3ff aggregate exit: $status =="
exit "$status"
