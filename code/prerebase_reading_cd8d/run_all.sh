#!/bin/sh
# mg-cd8d — r0 first, because r1's answer is one word and a broken harness returns one word.
# NO PIPES ANYWHERE.  Each arm's status is read directly, which is mg-9876's §2 smell avoided
# rather than counted: a `| tee` here would put this directory in that index by construction.
set -u
cd "$(dirname "$0")" || exit 2

worst=0

python3 r0_selftest.py > out_r0_selftest.txt
rc=$?
echo "r0_selftest.py exit $rc"
[ "$rc" -gt "$worst" ] && worst=$rc

python3 r1_prerebase.py > out_r1_prerebase.txt
rc=$?
echo "r1_prerebase.py exit $rc"
[ "$rc" -gt "$worst" ] && worst=$rc

python3 r2_wording.py > out_r2_wording.txt
rc=$?
echo "r2_wording.py exit $rc"
[ "$rc" -gt "$worst" ] && worst=$rc

echo "worst exit: $worst"
exit "$worst"
