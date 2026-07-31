#!/bin/sh
# mg-7d75 -- species / Hopf monoids as the framework behind BOTH S_n
# representation theory and the poset-quotient story.
# Pure Python 3, no dependencies, no network.  ~1 minute.
set -e
cd "$(dirname "$0")"
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
python3 selftest.py > out_selftest.txt || {
    cat out_selftest.txt; echo "selftest.py FAILED"; exit 1; }
cat out_selftest.txt
python3 t1_grading.py          > out_t1_grading.txt
python3 t2_operation.py        > out_t2_operation.txt
python3 t3_bidigare.py         > out_t3_bidigare.txt
python3 t4_one_operation.py    > out_t4_one_operation.txt
python3 t5_hopf_monoid.py      > out_t5_hopf_monoid.txt
python3 t6_fock_and_record.py  > out_t6_fock_and_record.txt
echo
echo "TOTAL BAD across the battery:"
grep -h "TOTAL BAD" out_t*.txt
