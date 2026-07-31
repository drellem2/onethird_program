#!/bin/sh
# mg-c2b3 -- the arc-wide sweep of `| tee` in run_all.sh, and the retroactive
# question that a forward fix leaves open.
#
#   K1  the census, RE-DERIVED at the ticket's own revision and on disk.
#       63/23/1 becomes 64 / 23-by-bare-grep / 17-by-parse / 1.
#   K2  per runner and per line: is the exit status ACTUALLY CONSUMED, and by
#       what -- `set -e`, an explicit guard, or an external caller.
#   K3  WHICH PAST "CLEAN RUN" CLAIMS DEPENDED ON AN AFFECTED RUNNER'S EXIT
#       CODE.  Each claim is dispositioned, and the ones settled by a committed
#       byte-comparison are marked SAFE with the comparison named.
#   K4  the positive control, per fixed runner: the checked script is made to
#       fail on purpose and the RUNNER's exit code is read -- against the
#       pre-repair text (must exit 0, the defect) and the post-repair text
#       (must exit non-zero, the repair).
#
# Pure Python 3, no dependencies, NO NETWORK.  About 4 minutes, almost all of
# it K3's direct re-run of every script the pipelines used to swallow.
#
# THIS RUNNER CONTAINS NO PIPELINE.  Not one `|` outside a comment.  That is
# not a style choice: a pipeline is the only construct in POSIX sh whose exit
# status belongs to a command other than the one being scored, so an instrument
# that reports on discarded exit statuses and contains no pipeline has no place
# to discard its own.  `selftestc2b3.py` section H measures that on this file.
#
# WHY REDIRECT-AND-GUARD AND NOT `set -o pipefail`: the shebang is `/bin/sh`.
# On Linux that is usually dash, which has no `pipefail`; `set -o pipefail`
# there prints "Illegal option" and returns non-zero, which under `set -e`
# aborts the runner at line 1.  `${PIPESTATUS[0]}` is bash-only for the same
# reason.  Redirect + `||` is POSIX, and it is what mg-821e and mg-e1d0 already
# used in this repository -- three mechanisms would have been worse than one.
set -e
cd "$(dirname "$0")"

python3 -B selftestc2b3.py > out_selftest.txt || {
    cat out_selftest.txt; echo "SELFTEST FAILED"; exit 1; }
cat out_selftest.txt

python3 -B k1_census.py   > out_k1_census.txt   || {
    cat out_k1_census.txt;   echo "K1 FAILED"; exit 1; }
cat out_k1_census.txt

python3 -B k2_consume.py  > out_k2_consume.txt  || {
    cat out_k2_consume.txt;  echo "K2 FAILED"; exit 1; }
cat out_k2_consume.txt

python3 -B k3_retro.py    > out_k3_retro.txt    || {
    cat out_k3_retro.txt;    echo "K3 FAILED"; exit 1; }
cat out_k3_retro.txt

python3 -B k4_control.py  > out_k4_control.txt  || {
    cat out_k4_control.txt;  echo "K4 FAILED"; exit 1; }
cat out_k4_control.txt

echo
echo "Headline lines:"
grep -h '^K[1234] TOTAL BAD:\|^selftestc2b3 TOTAL BAD:' out_*.txt || true
echo
echo "Each of those totals is followed IN THE OUTPUT by a statement of what"
echo "it ranged over.  K1 counts unrepaired sites, K2 counts consumers whose"
echo "verdict is unsupported, K3 counts past claims left UNSETTLED, and K4"
echo "counts positive controls that did not behave in BOTH directions."
