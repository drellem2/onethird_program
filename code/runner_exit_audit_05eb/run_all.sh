#!/bin/sh
# mg-05eb -- INDEPENDENT AUDIT of the arc-wide `| tee` sweep (mg-c2b3, 52aeaf4).
#
# Pure Python 3, no dependencies, no network.  About 25 minutes: J3 executes
# every repaired runner twice (once with its first scored step forced to fail,
# once unmodified) and that is most of the wall clock.
#
# THIS RUNNER CONTAINS NO PIPELINE OF ANY KIND.  Not `| tee`, not `| grep`, not
# `| head`.  That is the branch which cannot exhibit the defect under audit, and
# the reason is structural: a pipeline is the only POSIX-sh construct whose exit
# status belongs to a command other than the one being scored.  `selftest05eb.py`
# section S6 measures it on this file's own bytes, so the claim is checked rather
# than asserted -- and S6 fails if a later edit adds one.
#
# Every step below redirects and has its status read by an explicit `||` guard
# that CATS the transcript first, so a failing section prints what it found
# before this runner stops.  Not `set -o pipefail`: `/bin/sh` is dash on Linux,
# which rejects the option -- and, separately, J1e shows this repository already
# contains one runner that sets it in the combined `set -euo pipefail` form.
set -e
cd "$(dirname "$0")"

python3 selftest05eb.py > out_selftest_05eb.txt || {
    cat out_selftest_05eb.txt; echo "selftest05eb.py FAILED"; exit 1; }
cat out_selftest_05eb.txt

echo
python3 j1_census.py > out_j1_census.txt || {
    cat out_j1_census.txt
    echo "J1 reports findings -- see J1 TOTAL BAD above"; }
cat out_j1_census.txt

echo
python3 j2_retro.py > out_j2_retro.txt || {
    cat out_j2_retro.txt
    echo "J2 reports findings -- see J2 TOTAL BAD above"; }
cat out_j2_retro.txt

echo
python3 j3_control.py > out_j3_control.txt || {
    cat out_j3_control.txt; echo "j3_control.py FAILED"; exit 1; }
cat out_j3_control.txt

echo
python3 j4_scope.py > out_j4_scope.txt || {
    cat out_j4_scope.txt; echo "j4_scope.py FAILED"; exit 1; }
cat out_j4_scope.txt

echo
echo "Headline lines:"
grep -h '^J[1-4] TOTAL BAD:\|^S TOTAL BAD:\|^PREDICTIONS:' out_*.txt || true
echo
echo "J1 and J2 carry FINDINGS about the audited sweep, so their non-zero exit"
echo "is expected and does not stop this runner; J3, J4 and the self-test are"
echo "checks on this instrument and do stop it.  Which is which is stated here"
echo "rather than left to the exit code, because a runner that cannot fail and"
echo "a runner that is allowed to fail look identical from outside."
