#!/bin/sh
# The instrument for mg-db09.  Pure Python 3, no dependencies, NO NETWORK.
# `fetch_sources.sh` is the one network script and this file does not call it.
set -e
D=$(dirname "$0")
cd "$D"
# mg-c2b3: every step in this file that is followed by a bare `cat` of its
# own transcript used to pipe into `tee` instead of redirecting.  A pipeline's
# exit status in POSIX sh is its LAST command's, which is tee's and is 0 --
# so the step could print failures, exit 1, and leave this runner exiting 0.
# Each now redirects and has its status read by an explicit `||` guard.  The
# other steps in this file were already guarded and are untouched.
# `set -o pipefail` is not used: `/bin/sh` is dash on Linux, which rejects the
# option and would abort the runner at the line meant to make it safer.
# This note deliberately avoids writing the old pipeline out, so that a plain
# grep for it over the arc still counts only the sites that still have one.
python3 -u selftestdb09.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftestdb09.py FAILED"; exit 1; }
cat out_selftest.txt
python3 -u t1_tl.py        > out_t1_tl.txt     ; tail -1 out_t1_tl.txt
python3 -u t2_gz.py        > out_t2_gz.txt     ; tail -1 out_t2_gz.txt
python3 -u t3_ours.py      > out_t3_ours.txt   ; tail -1 out_t3_ours.txt
python3 -u t4_quotes.py    > out_t4_quotes.txt ; tail -1 out_t4_quotes.txt
# t5 checks the delivered document's disposition labels against the tree and
# against named historical commits, so unlike t1..t4 it needs a git checkout.
# It is the one script here that exits non-zero when it fails, because a label
# that has stopped being true is a gate and not a report.
if git rev-parse --git-dir > /dev/null 2>&1; then
    python3 -u t5_labels.py > out_t5_labels.txt ; tail -1 out_t5_labels.txt
else
    echo "t5_labels.py NOT RUN: this is not a git checkout, and t5 reads the"
    echo "diffs of 03d7f91, 2e66d03 and f4eaea6.  Its committed output stands."
fi
