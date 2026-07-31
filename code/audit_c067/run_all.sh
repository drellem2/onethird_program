#!/bin/sh
# mg-c067: INDEPENDENT AUDIT of the mg-132a publication-anchor repair.
#
#     sh run_all.sh                 # ~40 s
#     sh run_all.sh --at <rev>      # the same audit as of any commit
#                                   # ⚠️ RUN THIS AFTER A MERGE
#
# Pure Python 3 + git, no third-party packages.
#
# READ-ONLY apart from its own six transcripts.  One probe (`C4c`) writes to
# `out_anchor_132a.txt` in the working tree in order to prove that the parent
# ignores the working tree; it restores the bytes in a `finally:` and then
# VERIFIES the restore byte-for-byte, and the row is red if the restore failed.
#
# ⚠️ THE RUNNER REPORTS THE INSTRUMENT'S STATUS, NOT `tee`'s.  Under `set -e` a
# pipeline's exit status is the LAST command's, which is how a transcript
# recording a refutation once came to be committed beside an exit 0 (mg-c2b3).
# Each script redirects; the status is captured; the transcript is then `cat`.
#
# EXIT: 0 if no control of THIS instrument was refuted.  ⚠️ FINDINGS ABOUT THE
# PARENT DO NOT SET IT.  An audit that exited 1 because it successfully found
# what it was sent to find could not distinguish `the subject has a defect`
# from `the auditor is broken`, and those need different responses.
cd "$(dirname "$0")"

echo "== mg-c067: independent audit of the mg-132a publication-anchor repair =="
status=0
for s in c1_rebase c2_anchors c3_shopping c4_independence c5_vocab \
         selftest_c067; do
    # stderr goes INTO the transcript: a crash and a fired check are both
    # exit 1, and a transcript keeping only stdout ends mid-section with no
    # reason given.
    python3 "$s.py" "$@" > "out_$s.txt" 2>&1 || status=$?
    cat "out_$s.txt"
done

echo
echo "== mg-c067 aggregate exit: $status =="
exit "$status"
